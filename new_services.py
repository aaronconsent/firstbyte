#!/usr/bin/env python3
"""Build the 3 net-new service landing pages (SEO, Paid Advertising, Public
Relations) using the shared theme_ui design — hero, value prose, benefits,
service-area links, FAQ, CTA, and Service/WebPage/FAQ schema.

Idempotent. Run after enhance.py (needs the web-design template) and before
geo_pages.py/hubs.py. Re-run enhance.py after for sitemap + schema.
"""
import json
import theme_ui as tu
from geo_pages import SERVICES, CITIES
from industries import INDUSTRIES

BASE = tu.BASE
NEW = ["seo", "paid-advertising", "public-relations"]


def faqs_for(svc):
    name = svc["name"]
    q, a = svc["faq"]
    return [
        (q.format(city="The Woodlands"), a.format(city="The Woodlands")),
        (f"Do you offer {name.lower()} outside The Woodlands?",
         "Yes — we're based in The Woodlands and serve Spring, Conroe, Montgomery, Tomball, Magnolia, Houston and the wider Greater Houston area."),
        (f"How do you report on {name.lower()} results?",
         "You get transparent reporting tied to leads and revenue — the numbers that matter — not just vanity metrics."),
    ]


def build(slug):
    svc = SERVICES[slug]
    name = svc["name"]
    url = f"{BASE}{svc['main']}"
    h1 = f"{name} in The Woodlands, TX"
    opener = svc["opener"].format(city="The Woodlands")
    bullets = "".join(f"<li>{tu.esc(b)}</li>" for b in svc["benefits"])
    area_links = " · ".join(
        f'<a href="/{slug}-{cs}-tx/">{tu.esc(c["name"])}</a>' for cs, c in CITIES.items())
    industry_links = " · ".join(
        f'<a href="/industries/{isl}/">{tu.esc(idata["name"])}</a>' for isl, idata in INDUSTRIES.items())
    faqs = faqs_for(svc)

    inner = (
        tu.hero(name, f'{tu.esc(name)} in <span class="accent">The Woodlands, TX</span>',
                opener + " " + svc["value"])
        + '<section class="fb-section"><div class="fb-wrap">'
          '<div class="fb-section-head"><h2 class="fb-h2">What’s included</h2>'
          f'<p class="fb-sub">Everything you need from {tu.esc(name.lower())}, handled by a local team.</p></div>'
          f'<ul class="fb-checklist">{bullets}</ul></div></section>'
        + '<section class="fb-section"><div class="fb-wrap fb-narrow"><div class="fb-prose">'
          f'<p>First Byte is a digital marketing agency based in The Woodlands, TX. We pair real local market knowledge with {tu.esc(name.lower())} that’s measured against one thing: new customers for your business.</p>'
          '<p>Explore our <a href="/services/">full services</a> or see the <a href="/service-areas/">areas we serve</a> across Greater Houston.</p>'
          '</div></div></section>'
        + '<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">{tu.esc(name)} across Greater Houston</h2></div>'
          f'<p class="fb-prose" style="margin:0 auto;text-align:center;">Based in The Woodlands, we also serve: {area_links}.</p></div></section>'
        + '<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">{tu.esc(name)} by industry</h2></div>'
          f'<p class="fb-prose" style="margin:0 auto;text-align:center;">We tailor {tu.esc(name.lower())} to your industry, including: {industry_links}.</p></div></section>'
        + '<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">{tu.esc(name)} FAQs</h2></div>'
          f'{tu.faqlist(faqs)}</div></section>'
        + tu.cta(f"Ready to grow with {name.lower()}?",
                 "Let’s talk about what First Byte can do for your business.")
    )

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Service", "@id": url + "#service", "name": name,
             "serviceType": name, "url": url,
             "provider": {"@id": BASE + "/#localbusiness"},
             "areaServed": [{"@type": "City", "name": c["name"]} for c in CITIES.values()],
             "description": svc["value"]},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": BASE + "/services/"},
                {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
            {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
        ],
    }
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps(graph, separators=(",", ":")) + "</script>")
    desc = f"{name} for The Woodlands & Greater Houston businesses. {svc['value']}"[:300]
    page = tu.render(inner, f"{h1} | First Byte", url, desc, schema)
    tu.write(svc["main"].strip("/").split("/"), page)


def main():
    for slug in NEW:
        build(slug)
        print(f"  built {SERVICES[slug]['main']}")


if __name__ == "__main__":
    main()
