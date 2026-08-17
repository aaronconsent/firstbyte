// Cloudflare Worker for firstbyte.agency.
//
// Serves the static site from ./site via env.ASSETS, and handles two API routes:
//   POST /api/contact       -> Resend email + optional KV write for social proof
//   GET  /api/recent-leads  -> anonymized recent leads for social-proof toasts
//
// Required secret (set with `wrangler secret put RESEND_API_KEY`):
//   RESEND_API_KEY
// Optional bindings / vars (see wrangler.jsonc):
//   CONTACT_TO, CONTACT_FROM, LEADS_KV
//
// Ported verbatim from the earlier Pages Functions at
// functions/api/{contact,recent-leads}.js.

const DEFAULT_TO = "sean@firstbyte.agency";
const DEFAULT_FROM = "First Byte <noreply@firstbyte.agency>";

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/api/contact" && request.method === "POST") {
      return handleContact(request, env);
    }
    if (url.pathname === "/api/recent-leads" && request.method === "GET") {
      return handleRecentLeads(env);
    }
    // Anything else: static asset (or 404 if none matches).
    return env.ASSETS.fetch(request);
  },
};

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

    // Record an anonymized entry for social-proof toasts (only if KV is bound).
    try {
      if (env.LEADS_KV) {
        const first = (name.split(/\s+/)[0] || "Someone").slice(0, 40);
        const raw = await env.LEADS_KV.get("recent");
        const list = raw ? JSON.parse(raw) : [];
        list.unshift({ n: first, a: "requested a free plan", t: Date.now() });
        await env.LEADS_KV.put("recent", JSON.stringify(list.slice(0, 20)));
      }
    } catch (_e) { /* never block the lead on logging */ }

    return respond(request, true, "Thanks! We’ll be in touch shortly.", 200);
  } catch (_e) {
    return respond(request, false, "Something went wrong. Please try again or call (713) 578-0634.", 500);
  }
}

async function handleRecentLeads(env) {
  let items = [];
  try {
    if (env.LEADS_KV) {
      const raw = await env.LEADS_KV.get("recent");
      if (raw) items = JSON.parse(raw);
    }
  } catch (_e) { items = []; }

  // Only expose first name + action + timestamp (no email/phone/last name).
  const safe = (Array.isArray(items) ? items : []).slice(0, 8).map((x) => ({
    n: String(x.n || "Someone").slice(0, 40),
    a: String(x.a || "requested a free plan").slice(0, 80),
    t: Number(x.t) || Date.now(),
  }));
  return new Response(JSON.stringify(safe), {
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}

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
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
