// Cloudflare Worker for firstbyte.agency.
//
// Serves the static site from ./site via env.ASSETS, and handles these routes:
//   POST /api/contact       -> Resend email + KV writes (recent-anon + full lead)
//   GET  /api/recent-leads  -> anonymized recent leads for social-proof toasts (public)
//   GET  /api/leads         -> FULL lead history as JSON  (Basic Auth required)
//   GET  /admin/leads       -> HTML lead inbox            (Basic Auth required)
//
// Required secret (for outbound email):
//   RESEND_API_KEY   ->  npx wrangler secret put RESEND_API_KEY
// Required secrets (for admin lead inbox):
//   ADMIN_USER       ->  npx wrangler secret put ADMIN_USER
//   ADMIN_PASS       ->  npx wrangler secret put ADMIN_PASS
// Optional bindings / vars (see wrangler.jsonc):
//   CONTACT_TO, CONTACT_FROM, LEADS_KV

const DEFAULT_TO = "sean@firstbyte.agency";
const DEFAULT_FROM = "First Byte <noreply@firstbyte.agency>";
const LEADS_KEY = "leads:all";      // full leads, capped at MAX_LEADS
const RECENT_KEY = "recent";        // anonymized, for social-proof toasts
const MAX_LEADS = 500;              // rolling cap on stored lead history

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const p = url.pathname;

    if (p === "/api/contact" && request.method === "POST") return handleContact(request, env);
    if (p === "/api/recent-leads" && request.method === "GET") return handleRecentLeads(env);

    if (p === "/api/leads" && request.method === "GET") {
      const auth = requireAdmin(request, env); if (auth) return auth;
      return handleLeadsJson(env);
    }
    if ((p === "/admin/leads" || p === "/admin/leads/") && request.method === "GET") {
      const auth = requireAdmin(request, env); if (auth) return auth;
      return handleLeadsAdmin(env);
    }

    // Anything else: static asset (or 404 if none matches).
    return env.ASSETS.fetch(request);
  },
};

/* ---------------- /api/contact ---------------- */

async function handleContact(request, env) {
  try {
    const data = await readBody(request);

    // Honeypot: real users never fill the hidden "company" field.
    if (data.company) return json({ ok: true });

    const name = str(data.name);
    const email = str(data.email);
    const phone = str(data.phone);
    const message = str(data.message);

    if (!name || !message || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return respond(request, false, "Please add your name, a valid email, and a message.", 400);
    }

    if (!env.RESEND_API_KEY) {
      return respond(request, false, "Email isn’t configured yet. Please call us at (713) 578-0634.", 500);
    }
    const to = env.CONTACT_TO || DEFAULT_TO;
    const from = env.CONTACT_FROM || DEFAULT_FROM;

    const text = `Name: ${name}\nEmail: ${email}\nPhone: ${phone || "—"}\n\n${message}`;
    const html = `<h2>New website enquiry</h2>
<p><strong>Name:</strong> ${esc(name)}</p>
<p><strong>Email:</strong> ${esc(email)}</p>
<p><strong>Phone:</strong> ${esc(phone || "—")}</p>
<p><strong>Message:</strong></p>
<p>${esc(message).replace(/\n/g, "<br>")}</p>`;

    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: email,
        subject: `New website enquiry from ${name}`,
        text,
        html,
      }),
    });

    if (!res.ok) {
      return respond(request, false, "Couldn’t send your message. Please call us at (713) 578-0634.", 502);
    }

    // Persist to KV (both the anonymized recent list AND the full lead history).
    try { await saveLead(env, request, { name, email, phone, message }); } catch (_e) { /* never block on log */ }

    return respond(request, true, "Thanks! We’ll be in touch shortly.", 200);
  } catch (_e) {
    return respond(request, false, "Something went wrong. Please try again or call (713) 578-0634.", 500);
  }
}

/* ---------------- KV storage ---------------- */

async function saveLead(env, request, lead) {
  if (!env.LEADS_KV) return;

  // 1) Full lead history (used by /api/leads + /admin/leads).
  const source = request.headers.get("referer") || "";
  const ua = request.headers.get("user-agent") || "";
  const ip = request.headers.get("cf-connecting-ip") || "";
  const country = request.cf?.country || "";
  const entry = {
    id: `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`,
    ts: Date.now(),
    name: lead.name,
    email: lead.email,
    phone: lead.phone || "",
    message: lead.message,
    source,
    ip,
    country,
    ua,
  };
  const raw = await env.LEADS_KV.get(LEADS_KEY);
  const list = raw ? safeJson(raw, []) : [];
  list.unshift(entry);
  if (list.length > MAX_LEADS) list.length = MAX_LEADS;
  await env.LEADS_KV.put(LEADS_KEY, JSON.stringify(list));

  // 2) Anonymized recent list for the public social-proof toasts.
  const first = (lead.name.split(/\s+/)[0] || "Someone").slice(0, 40);
  const rraw = await env.LEADS_KV.get(RECENT_KEY);
  const rlist = rraw ? safeJson(rraw, []) : [];
  rlist.unshift({ n: first, a: "requested a free plan", t: entry.ts });
  await env.LEADS_KV.put(RECENT_KEY, JSON.stringify(rlist.slice(0, 20)));
}

async function handleRecentLeads(env) {
  let items = [];
  try {
    if (env.LEADS_KV) {
      const raw = await env.LEADS_KV.get(RECENT_KEY);
      if (raw) items = safeJson(raw, []);
    }
  } catch (_e) { items = []; }

  const safe = (Array.isArray(items) ? items : []).slice(0, 8).map((x) => ({
    n: String(x.n || "Someone").slice(0, 40),
    a: String(x.a || "requested a free plan").slice(0, 80),
    t: Number(x.t) || Date.now(),
  }));
  return new Response(JSON.stringify(safe), {
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}

/* ---------------- /api/leads (admin, JSON) ---------------- */

async function handleLeadsJson(env) {
  if (!env.LEADS_KV) {
    return json({ ok: false, error: "LEADS_KV not bound.", leads: [] }, 500);
  }
  const raw = await env.LEADS_KV.get(LEADS_KEY);
  const list = raw ? safeJson(raw, []) : [];
  return new Response(JSON.stringify({ ok: true, count: list.length, leads: list }, null, 2), {
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}

/* ---------------- /admin/leads (admin HTML inbox) ---------------- */

async function handleLeadsAdmin(env) {
  const kvOk = !!env.LEADS_KV;
  const raw = kvOk ? await env.LEADS_KV.get(LEADS_KEY) : null;
  const list = raw ? safeJson(raw, []) : [];

  const rows = list.map((l) => {
    const d = new Date(l.ts || Date.now());
    const when = d.toISOString().replace("T", " ").slice(0, 19) + " UTC";
    const src = l.source ? l.source.replace(/^https?:\/\/[^/]+/, "") : "";
    return `<details class="lead">
  <summary>
    <span class="when">${esc(when)}</span>
    <span class="who"><b>${esc(l.name || "(no name)")}</b> &middot; <a href="mailto:${esc(l.email || "")}">${esc(l.email || "(no email)")}</a>${l.phone ? ` &middot; <a href="tel:${esc(l.phone)}">${esc(l.phone)}</a>` : ""}</span>
    ${src ? `<span class="src">${esc(src)}</span>` : ""}
  </summary>
  <div class="body">
    <div class="meta">
      <span>${esc(l.country || "?")}</span>
      <span>${esc(l.ip || "")}</span>
      <span class="ua" title="${esc(l.ua || "")}">${esc((l.ua || "").slice(0, 80))}${(l.ua || "").length > 80 ? "…" : ""}</span>
    </div>
    <pre>${esc(l.message || "")}</pre>
  </div>
</details>`;
  }).join("\n");

  const empty = list.length === 0
    ? `<p class="empty">${kvOk
        ? "No leads yet — every form submission will appear here going forward."
        : "⚠️ <b>LEADS_KV isn't bound to the Worker</b>. Bind a KV namespace in wrangler.jsonc and redeploy, then leads will start appearing here."}</p>`
    : "";

  const body = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>First Byte — Lead Inbox</title>
<style>
  :root{color-scheme:dark;--bg:#0d0c0e;--card:#171518;--line:rgba(255,255,255,.08);--teal:#01f6f2;--dim:hsla(0,0%,100%,.55);--text:#fff;}
  body{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;}
  header{padding:1.6rem 1.2rem;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;}
  header h1{font:700 1.35rem/1 "Funnel Display","Figtree",sans-serif;margin:0;}
  header .count{color:var(--teal);font-weight:700;}
  header a{color:var(--dim);text-decoration:none;font-size:.85rem;margin-left:1rem;}
  header a:hover{color:var(--teal);}
  main{max-width:960px;margin:0 auto;padding:1rem 1.2rem 4rem;}
  .empty{background:var(--card);border:1px dashed var(--line);border-radius:.7rem;padding:1.4rem;color:var(--dim);text-align:center;}
  .lead{background:var(--card);border:1px solid var(--line);border-radius:.7rem;margin:.55rem 0;overflow:hidden;transition:border-color .15s;}
  .lead:hover{border-color:rgba(35,255,244,.35);}
  .lead[open]{border-color:var(--teal);}
  .lead summary{cursor:pointer;padding:.8rem 1rem;list-style:none;display:grid;grid-template-columns:180px 1fr auto;gap:1rem;align-items:center;}
  .lead summary::-webkit-details-marker{display:none;}
  .lead .when{color:var(--dim);font-size:.82rem;font-variant-numeric:tabular-nums;}
  .lead .who{color:var(--text);font-size:.95rem;}
  .lead .who a{color:var(--teal);text-decoration:none;}
  .lead .who a:hover{text-decoration:underline;}
  .lead .src{color:var(--dim);font-size:.78rem;justify-self:end;}
  @media(max-width:640px){.lead summary{grid-template-columns:1fr;gap:.35rem;} .lead .src{justify-self:start;}}
  .body{padding:0 1rem 1rem;border-top:1px solid var(--line);}
  .body .meta{display:flex;gap:.7rem;color:var(--dim);font-size:.75rem;margin:.7rem 0;flex-wrap:wrap;}
  .body .ua{max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  .body pre{white-space:pre-wrap;background:#0d0c0e;border:1px solid var(--line);border-radius:.5rem;padding:.9rem 1rem;margin:0;font:13px/1.55 ui-monospace,SFMono-Regular,Consolas,monospace;color:hsla(0,0%,100%,.9);}
</style>
</head>
<body>
<header>
  <div><h1>First Byte lead inbox</h1></div>
  <div>
    <span class="count">${list.length}</span> lead${list.length === 1 ? "" : "s"}
    <a href="/api/leads" target="_blank">JSON</a>
    <a href="/">← site</a>
  </div>
</header>
<main>
${empty}
${rows}
</main>
</body>
</html>`;

  return new Response(body, {
    headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex, nofollow" },
  });
}

/* ---------------- Basic Auth gate ---------------- */

function requireAdmin(request, env) {
  const user = env.ADMIN_USER, pass = env.ADMIN_PASS;
  if (!user || !pass) {
    return new Response("Admin credentials not configured on the Worker.", { status: 503 });
  }
  const header = request.headers.get("authorization") || "";
  if (header.startsWith("Basic ")) {
    let decoded = "";
    try { decoded = atob(header.slice(6)); } catch (_e) { decoded = ""; }
    const i = decoded.indexOf(":");
    if (i > 0) {
      const u = decoded.slice(0, i), p = decoded.slice(i + 1);
      if (constantTimeEqual(u, user) && constantTimeEqual(p, pass)) return null; // OK
    }
  }
  return new Response("Authentication required.", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="First Byte Admin", charset="UTF-8"',
      "content-type": "text/plain; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function constantTimeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

/* ---------------- helpers ---------------- */

async function readBody(request) {
  const ct = request.headers.get("content-type") || "";
  if (ct.includes("application/json")) return await request.json();
  const form = await request.formData();
  const out = {};
  for (const [k, v] of form.entries()) out[k] = typeof v === "string" ? v : "";
  return out;
}

function respond(request, ok, msg, status) {
  const accept = request.headers.get("accept") || "";
  // No-JS form post -> redirect back to the contact page with a status flag.
  if (!accept.includes("application/json")) {
    const url = new URL("/contact/", request.url);
    url.searchParams.set("sent", ok ? "1" : "0");
    return Response.redirect(url.toString(), 303);
  }
  return json({ ok, error: ok ? undefined : msg, message: ok ? msg : undefined }, status);
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json" } });
}

function str(v) { return (v == null ? "" : String(v)).trim(); }

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function safeJson(s, fallback) {
  try { return JSON.parse(s); } catch (_e) { return fallback; }
}
