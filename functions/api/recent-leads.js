// Cloudflare Pages Function — GET /api/recent-leads
// Returns a small list of recent, anonymized leads for social-proof toasts.
// Records are written by /api/contact when a KV namespace named LEADS_KV is
// bound to the project (Settings -> Functions -> KV namespace bindings).
// If no KV is bound, returns an empty array (the front-end then shows clearly
// labeled sample data instead of anything fabricated).

export async function onRequestGet(context) {
  const { env } = context;
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
