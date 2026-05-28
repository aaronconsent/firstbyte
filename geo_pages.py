#!/usr/bin/env python3
"""Generate the full service x city geo landing-page matrix.

4 services x 6 cities = 24 unique pages at /{service}-{city}-tx/.
Each page combines a unique per-combination opener + per-city context +
per-service value + service benefits + city-specific FAQ, so no two pages
are near-duplicates (avoids doorway-page penalties).

Clones the theme shell from the matching service page. Idempotent.
Run after service_pages.py; re-run enhance.py after to refresh sitemap.
"""
import os
import re
import json
import html as htmllib
import theme_ui as tu

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://firstbyte.agency"
CONTACT = "/contact/"
S = ' style="margin-top:2.5rem;"'

SERVICES = {
    "web-design": {
        "name": "Web Design",
        "main": "/work_tax/web-design-development/",
        "value": "First Byte builds custom, fast, mobile-first websites engineered to turn local searches into phone calls and form fills — no templates, with SEO baked in from day one.",
        "benefits": [
            "Custom, conversion-focused design built around your goals",
            "Mobile-first and lightning fast (tuned for Core Web Vitals)",
            "Local SEO built in so you rank in your city and beyond",
            "Easy-to-manage CMS your team can actually update",
            "Ongoing support from a local team that knows the market",
        ],
        "faq": ("How much does web design cost in {city}?",
                "Most {city} small-business websites range from a few thousand dollars to the low five figures depending on scope. Book a call for a fixed quote."),
        "opener": "A slow or dated website quietly sends {city} customers to your competitors every day.",
    },
    "performance-marketing": {
        "name": "Performance Marketing",
        "main": "/work_tax/performance-marketing/",
        "value": "First Byte runs Google and Meta ad campaigns measured against leads and revenue — not vanity metrics — and builds the landing pages and tracking to prove every dollar's ROI.",
        "benefits": [
            "Google & Meta ad management, end to end",
            "Landing pages built to convert the traffic you pay for",
            "Conversion tracking and transparent, lead-focused reporting",
            "Continuous A/B testing and optimization",
            "Local and national targeting that reaches the right buyers",
        ],
        "faq": ("What ad budget do {city} businesses need to start?",
                "We recommend a minimum monthly media budget so campaigns gather enough data to optimize, then right-size it to the {city} market on a strategy call."),
        "opener": "Ad spend without strategy is just expensive guessing for {city} businesses.",
    },
    "brand-development": {
        "name": "Brand Development",
        "main": "/work_tax/brand-development/",
        "value": "First Byte builds memorable brands — strategy, naming, logo, voice and a full visual identity — that command trust and scale cleanly across every channel.",
        "benefits": [
            "Brand strategy and market positioning",
            "Logo and complete visual identity",
            "Messaging and brand voice",
            "Brand guidelines that keep your team consistent",
            "Collateral and launch support",
        ],
        "faq": ("Can you refresh an existing {city} brand?",
                "Absolutely. We do both ground-up brand builds and strategic refreshes for established {city} businesses."),
        "opener": "In {city}, a strong brand is the difference between being a choice and being the choice.",
    },
    "influencer-marketing": {
        "name": "Influencer Marketing",
        "main": "/work_tax/influencer-marketing/",
        "value": "First Byte runs influencer campaigns end to end — sourcing and vetting the right creators, managing the partnership, and measuring real conversions, not just reach.",
        "benefits": [
            "Creator sourcing and vetting based on real audience fit",
            "Campaign strategy and hands-on management",
            "Content collaboration and approvals",
            "Performance tracking tied to your goals",
            "FTC-compliant partnerships that protect your brand",
        ],
        "faq": ("Does influencer marketing work for {city} businesses?",
                "Yes. Local and micro-influencers often drive the highest conversion for {city} service businesses because their audiences trust them and are nearby."),
        "opener": "The right creator can put your {city} brand in front of thousands of engaged local buyers.",
    },
}

CITIES = {
    "spring": {"name": "Spring",
               "context": "Spring sits in one of the fastest-growing corridors in Texas, just south of The Woodlands along I-45, where local businesses compete hard for the same customers against national chains.",
               "why": "Spring's growth means more competition for the same local searches, so looking established and loading fast is how local businesses win the click first."},
    "conroe": {"name": "Conroe",
               "context": "As the seat of Montgomery County and one of the fastest-growing cities in the country, Conroe is full of opportunity — and full of businesses competing for it, from downtown to the Lake Conroe waterfront.",
               "why": "Conroe's rapid growth rewards businesses that look established online, signaling trust to the new residents and visitors who don't yet know the local players."},
    "montgomery": {"name": "Montgomery",
                   "context": "Montgomery blends small-town Texas charm with a steady stream of visitors and new residents drawn to Lake Conroe and its historic district.",
                   "why": "In a destination market like Montgomery, much of the audience is mobile and ready to act, so a fast site that makes it easy to call or book is what converts."},
    "tomball": {"name": "Tomball",
                "context": "Tomball pairs its historic small-town roots with rapid suburban growth on the northwest edge of Houston, drawing both longtime locals and new families.",
                "why": "Tomball's mix of established and new residents means businesses that show up clearly online capture customers who are still choosing who to trust."},
    "magnolia": {"name": "Magnolia",
                 "context": "Magnolia is a fast-growing community where established local businesses and a wave of new arrivals compete for the same customers along the FM-1488 corridor.",
                 "why": "Magnolia's steady growth rewards businesses that invest early in visibility, before the market gets more crowded."},
    "houston": {"name": "Houston",
                "context": "Houston is one of the largest and most competitive markets in the country, where an average online presence simply gets buried.",
                "why": "In a market as large as Houston, technical performance and conversion design separate the businesses that grow online from the ones that disappear."},
}


def esc(s):
    return htmllib.escape(s)


def inner_main(svc_slug, svc, city_slug, city):
    cn = city["name"]
    h1 = f"{svc['name']} in {cn}, TX"
    opener = svc["opener"].format(city=cn)
    fq, fa = svc["faq"]
    faqs = [
        (fq.format(city=cn), fa.format(city=cn)),
        (f"Do you work with businesses in {cn}, TX?",
         f"Yes — First Byte is based in nearby The Woodlands and regularly delivers {svc['name'].lower()} for {cn} businesses across every industry."),
        (f"Will this help my {cn} business get found online?",
         f"That's the goal of every engagement. We build with local search in mind so {cn} customers find you first."),
    ]
    bullets = "".join(f"<li>{tu.esc(b)}</li>" for b in svc["benefits"])
    h1_html = f'{tu.esc(svc["name"])} in <span class="accent">{tu.esc(cn)}, TX</span>'
    lead = f"{opener} {svc['value']}"
    inner = (
        tu.hero(svc["name"], h1_html, lead)
        + f'<section class="fb-section"><div class="fb-wrap fb-narrow"><div class="fb-prose">'
          f'<p>{tu.esc(city["context"])}</p>'
          f'<p>{tu.esc(city["why"])} See our <a href="{svc["main"]}">{tu.esc(svc["name"].lower())} work</a>, '
          f'then <a href="{tu.CONTACT}">get in touch</a>.</p></div></div></section>'
        + f'<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">What’s included</h2></div>'
          f'<ul class="fb-checklist">{bullets}</ul></div></section>'
        + f'<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">{tu.esc(svc["name"])} in {tu.esc(cn)} — FAQs</h2></div>'
          f'{tu.faqlist(faqs)}</div></section>'
        + tu.cta(f"Ready to grow your {cn} business?",
                 "Let’s talk about what First Byte can do for you.")
    )
    return inner, h1, faqs


def page_schema(url, svc, city, h1, faqs):
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": url + "#webpage", "url": url,
             "name": f"{h1} | First Byte",
             "isPartOf": {"@id": BASE + "/#website"},
             "about": {"@id": BASE + "/#localbusiness"}},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": svc["name"], "item": BASE + svc["main"]},
                 {"@type": "ListItem", "position": 3, "name": h1, "item": url}]},
            {"@type": "FAQPage", "@id": url + "#faq",
             "mainEntity": [{"@type": "Question", "name": q,
                             "acceptedAnswer": {"@type": "Answer", "text": a}}
                            for q, a in faqs]},
        ],
    }
    return ('<script type="application/ld+json" data-seo-enhance="geo">'
            + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>")


def build(svc_slug, svc, city_slug, city):
    inner, h1, faqs = inner_main(svc_slug, svc, city_slug, city)
    url = f"{BASE}/{svc_slug}-{city_slug}-tx/"
    title = f"{h1} | First Byte"
    cn = city["name"]
    desc = (f"{svc['name']} for {cn}, TX businesses. First Byte helps {cn} "
            f"companies grow with {svc['name'].lower()} that drives real results. Let's talk.")
    template = os.path.join(OUT, svc["main"].strip("/"), "index.html")
    page = tu.render(inner, title, url, desc, page_schema(url, svc, city, h1, faqs), template=template)
    tu.write([f"{svc_slug}-{city_slug}-tx"], page)


def main():
    n = 0
    for svc_slug, svc in SERVICES.items():
        for city_slug, city in CITIES.items():
            build(svc_slug, svc, city_slug, city)
            n += 1
    print(f"Geo matrix pages built: {n} (4 services x 6 cities)")


if __name__ == "__main__":
    main()
