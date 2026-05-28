#!/usr/bin/env python3
"""Rebuild the 4 thin taxonomy-archive service pages into real landing pages.

Idempotent: all injected HTML is wrapped in <!-- seo-landing --> markers and
removed/re-inserted on each run. Removes the WP sidebar widget cruft, widens
content to full width, and adds intro + benefits + FAQ + CTA. Keeps the real
case-study articles as a "Selected Work" section.

Run AFTER crawl.py / rewrite.py / enhance.py:  python3 service_pages.py
"""
import os
import re
import json
import html as htmllib

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
CONTACT = "/contact/"

SERVICES = {
    "web-design-development": {
        "name": "Web Design",
        "intro": [
            "Your website is the hardest-working member of your sales team — and in a competitive market like The Woodlands, a slow or dated site quietly costs you customers every single day. First Byte designs and builds custom websites that load fast, look sharp on every device, and are engineered to turn visitors into phone calls and form fills.",
            "We don't hand you a template. Every First Byte website starts with your goals, your customers, and the search terms your buyers actually use — then we build a site that ranks, converts, and grows with your business.",
        ],
        "benefits": [
            "Custom, conversion-focused design — built around your goals, not a stock theme",
            "Mobile-first and lightning fast, tuned for Core Web Vitals",
            "SEO built in from day one so you rank in The Woodlands and beyond",
            "Easy-to-manage CMS your team can actually update",
            "Local optimization for The Woodlands & Greater Houston",
        ],
        "faqs": [
            ("How much does a website cost in The Woodlands?",
             "Most small-business websites we build range from a few thousand dollars to the low five figures, depending on page count and functionality. We scope every project to your goals and budget — book a call for a fixed quote."),
            ("How long does a website take to build?",
             "A typical timeline is 4–8 weeks from kickoff to launch, depending on scope and how quickly content is ready."),
            ("Do you work with businesses outside The Woodlands?",
             "Yes. We're based in The Woodlands and serve Spring, Conroe, Montgomery, Tomball, Magnolia and Greater Houston, plus clients nationwide."),
        ],
    },
    "performance-marketing": {
        "name": "Performance Marketing",
        "intro": [
            "Ad spend without strategy is just expensive guessing. First Byte runs performance marketing campaigns — Google Ads, Meta, and beyond — measured against one thing: leads and revenue, not vanity metrics.",
            "For businesses in The Woodlands and across Greater Houston, we build, test, and scale paid campaigns that put your offer in front of ready-to-buy customers and prove their ROI down to the dollar.",
        ],
        "benefits": [
            "Google & Meta ad management, end to end",
            "Landing pages built to convert the traffic you pay for",
            "Conversion tracking and transparent, lead-focused reporting",
            "Continuous A/B testing and optimization",
            "Local and national targeting that reaches the right buyers",
        ],
        "faqs": [
            ("What ad budget do I need to start?",
             "We recommend a minimum monthly media budget so campaigns gather enough data to optimize. We'll right-size it to your market on a strategy call."),
            ("How fast will I see results from paid ads?",
             "Paid campaigns can generate leads within days of launch. The first 30–60 days are about gathering data and optimizing toward your best-performing audiences."),
            ("Will I see what my ad spend is doing?",
             "Yes — you get transparent reporting tied to leads and revenue, not just clicks and impressions."),
        ],
    },
    "brand-development": {
        "name": "Brand Development",
        "intro": [
            "A strong brand is the difference between being a choice and being the choice. First Byte builds brands that are memorable, consistent, and built to command trust — from naming and logo to voice, visual identity, and the strategy behind it all.",
            "Whether you're launching something new or repositioning an established Woodlands business, we craft an identity that resonates with your customers and scales cleanly across every channel.",
        ],
        "benefits": [
            "Brand strategy and market positioning",
            "Logo and complete visual identity",
            "Messaging and brand voice",
            "Brand guidelines that keep your team consistent",
            "Collateral and launch support",
        ],
        "faqs": [
            ("What's included in brand development?",
             "Strategy, positioning, naming if needed, logo and visual identity, messaging, and a complete brand guideline so your team stays consistent everywhere."),
            ("How is branding different from just a logo?",
             "A logo is one piece. Branding is the full system — strategy, voice, and visuals — that makes your business instantly recognizable and trusted."),
            ("Can you refresh an existing brand?",
             "Absolutely. We do both ground-up brand builds and strategic refreshes for established businesses."),
        ],
    },
    "influencer-marketing": {
        "name": "Influencer Marketing",
        "intro": [
            "The right creator can put your brand in front of thousands of engaged, local buyers far more authentically than a banner ad ever could. First Byte runs end-to-end influencer marketing — from finding and vetting the right creators to managing campaigns and measuring the impact.",
            "We connect The Woodlands and Greater Houston brands with influencers whose audiences actually convert, turning social reach into real customers.",
        ],
        "benefits": [
            "Creator sourcing and vetting based on real audience fit",
            "Campaign strategy and hands-on management",
            "Content collaboration and approvals",
            "Performance tracking tied to your goals",
            "FTC-compliant partnerships that protect your brand",
        ],
        "faqs": [
            ("How do you pick the right influencers?",
             "We match creators to your audience based on real engagement and audience fit — not just follower count — and vet every partner before outreach."),
            ("Does influencer marketing work for local businesses?",
             "Yes. Local and micro-influencers often drive the highest conversion for service businesses because their audiences trust them and are nearby."),
            ("How do you measure influencer results?",
             "We track reach, engagement, clicks, and conversions tied back to your goals, with clear reporting throughout the campaign."),
        ],
    },
}

STYLE = ' style="margin-top:2.5rem;"'


def esc(s):
    return htmllib.escape(s)


def intro_cell(svc):
    paras = "".join(f"<p>{esc(p)}</p>\n" for p in svc["intro"])
    bullets = "".join(f"<li>{esc(b)}</li>\n" for b in svc["benefits"])
    return (
        '<!-- seo-landing -->\n'
        f'<div class="cell small-12 service-intro"{STYLE}>\n'
        f'{paras}'
        f'<h2{STYLE}>What\'s included</h2>\n'
        f'<ul>\n{bullets}</ul>\n'
        f'<p{STYLE}><a class="button-secondary" href="{CONTACT}">Let’s Talk</a></p>\n'
        '</div>\n<!-- /seo-landing -->'
    )


def faq_cta_cell(svc):
    faqs = ""
    for q, a in svc["faqs"]:
        faqs += f'<h3{STYLE}>{esc(q)}</h3>\n<p>{esc(a)}</p>\n'
    return (
        '<!-- seo-landing -->\n'
        f'<div class="cell small-12 service-faq"{STYLE}>\n'
        f'<h2>{esc(svc["name"])} FAQs</h2>\n'
        f'{faqs}'
        f'<p{STYLE}>Ready to grow your business in The Woodlands? '
        f'<a class="button-secondary" href="{CONTACT}">Let’s Talk</a></p>\n'
        '</div>\n<!-- /seo-landing -->'
    )


def faq_jsonld(svc):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"https://firstbyte.agency/work_tax/{svc['slug']}/#faq",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in svc["faqs"]
        ],
    }
    return ('<script type="application/ld+json" data-seo-enhance="faq">'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "</script>")


def transform(slug, svc):
    path = os.path.join(OUT, "work_tax", slug, "index.html")
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as f:
        h = f.read()
    orig = h

    # 1) strip previously injected landing blocks (idempotency)
    h = re.sub(r"<!-- seo-landing -->.*?<!-- /seo-landing -->\s*", "", h, flags=re.S)

    # 2) remove the WP sidebar widget block
    h = re.sub(r"<!-- BEGIN of Sidebar -->.*?<!-- END of Sidebar -->", "", h, flags=re.S)

    # 3) widen the content column to full width
    h = h.replace('<div class="large-8 medium-8 small-12 cell">',
                  '<div class="large-12 medium-12 small-12 cell">', 1)

    # 4) insert intro + benefits right after the H1 cell
    h = re.sub(r"(</h1>\s*</div>)", r"\1\n" + intro_cell(svc).replace("\\", "\\\\"), h, count=1)

    # 5) label the kept case studies as "Selected Work"
    h = h.replace(
        "<!-- BEGIN of Archive Content -->",
        '<!-- BEGIN of Archive Content -->\n<!-- seo-landing -->'
        f'<h2 class="cell small-12"{STYLE}>Selected {esc(svc["name"])} Work</h2>'
        '<!-- /seo-landing -->', 1)

    # 6) append FAQ + CTA after the archive content
    h = h.replace("<!-- END of Archive Content -->",
                  faq_cta_cell(svc) + "\n<!-- END of Archive Content -->", 1)

    # 7) FAQ schema for AEO (replace existing marked block)
    h = re.sub(r'\s*<script[^>]*data-seo-enhance="faq"[^>]*>.*?</script>', "", h, flags=re.S)
    h = h.replace("</head>", "  " + faq_jsonld(svc) + "\n</head>", 1)

    if h != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(h)
        return True
    return False


def main():
    n = 0
    for slug, svc in SERVICES.items():
        svc["slug"] = slug
        if transform(slug, svc):
            n += 1
            print(f"  rebuilt {slug}")
    print(f"\nService pages rebuilt: {n}")


if __name__ == "__main__":
    main()
