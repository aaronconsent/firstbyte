// Cloudflare Pages Function — POST /api/contact
// Sends contact-form submissions as email via the Resend API.
// Required env vars (set in Pages → Settings → Environment variables):
//   RESEND_API_KEY  (secret)  — your Resend API key
//   CONTACT_TO      — recipient address, e.g. hello@firstbyte.agency
//   CONTACT_FROM    — verified Resend sender, e.g. "First Byte <noreply@firstbyte.agency>"

export async function onRequestPost(context) {
  const { request, env } = context;
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

    if (!env.RESEND_API_KEY || !env.CONTACT_TO || !env.CONTACT_FROM) {
      return respond(request, false, "Email isn’t configured yet. Please call us at (713) 578-0634.", 500);
    }

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
        from: env.CONTACT_FROM,
        to: [env.CONTACT_TO],
        reply_to: email,
        subject: `New website enquiry from ${name}`,
        text,
        html,
      }),
    });

    if (!res.ok) {
      return respond(request, false, "Couldn’t send your message. Please call us at (713) 578-0634.", 502);
    }
    return respond(request, true, "Thanks! We’ll be in touch shortly.", 200);
  } catch (_e) {
    return respond(request, false, "Something went wrong. Please try again or call (713) 578-0634.", 500);
  }
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
