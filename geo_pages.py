#!/usr/bin/env python3
"""Generate Web Design geo/service-area landing pages for nearby cities.

Clones the theme shell from the Web Design service page and injects unique,
city-specific copy + schema. Idempotent: regenerates each page from the
template every run. Output: site/web-design-<city>-tx/index.html

Run after enhance.py + service_pages.py:  python3 geo_pages.py
Then re-run enhance.py once to refresh sitemap.xml and site-wide schema.
"""
import os
import re
import json
import html as htmllib

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://firstbyte.agency"
TEMPLATE = os.path.join(OUT, "work_tax", "web-design-development", "index.html")
CONTACT = "/contact/"
MAIN_SERVICE = "/work_tax/web-design-development/"

STYLE = ' style="margin-top:2.5rem;"'

# Each city gets genuinely unique copy (no doorway duplication).
CITIES = {
    "spring": {
        "city": "Spring",
        "intro": [
            "Spring businesses compete in one of the fastest-growing corridors in Texas — and a website that loads slow or looks dated quietly sends those customers to the competitor down I-45. First Byte builds custom web design for Spring, TX companies that turns local searches into booked calls.",
            "We're right next door in The Woodlands, so we understand the Spring market firsthand: the mix of established neighborhoods, new development, and small businesses fighting for visibility against national chains. Every site we build is engineered to rank locally and convert the traffic it earns.",
        ],
        "why": "Spring's growth means more competition for the same local searches. A fast, conversion-focused website is how local businesses win the click before a national brand does — and First Byte builds exactly that, with local SEO baked in.",
        "faqs": [
            ("Do you build websites for businesses in Spring, TX?",
             "Yes. We're based in neighboring The Woodlands and regularly build and optimize websites for Spring businesses across every industry."),
            ("How much does web design cost in Spring?",
             "Most Spring small-business websites range from a few thousand dollars to the low five figures depending on scope. Book a call and we'll give you a fixed quote."),
            ("Will my Spring business show up in local Google searches?",
             "That's the goal of every build — we optimize your site and structure for local search so Spring customers find you first."),
        ],
    },
    "conroe": {
        "city": "Conroe",
        "intro": [
            "As the seat of Montgomery County and one of the fastest-growing cities in the country, Conroe is full of opportunity — and full of businesses competing for it. First Byte designs and builds web sites for Conroe, TX companies that load fast, look professional, and are built to generate leads.",
            "From downtown Conroe to the Lake Conroe waterfront, local buyers are searching on their phones before they ever pick one. We make sure your business is the one they find, trust, and call.",
        ],
        "why": "Conroe's rapid growth rewards businesses that look established online. A polished, fast website signals trust to new residents and visitors who don't know the local players yet — and First Byte builds sites that earn that trust instantly.",
        "faqs": [
            ("Do you work with Conroe, TX businesses?",
             "Absolutely. First Byte serves Conroe and all of Montgomery County from our base in The Woodlands."),
            ("How long does a Conroe website take to launch?",
             "Typically 4–8 weeks from kickoff, depending on scope and how fast your content is ready."),
            ("Can you help my Conroe business rank on Google?",
             "Yes — local SEO is built into every site so Conroe and Lake Conroe customers can find you in search and on the map."),
        ],
    },
    "montgomery": {
        "city": "Montgomery",
        "intro": [
            "Montgomery blends small-town Texas charm with a steady stream of visitors and new residents drawn to Lake Conroe and the historic district. For local businesses, a strong website is the difference between being discovered and being overlooked. First Byte builds custom web design for Montgomery, TX that does exactly that.",
            "We craft fast, mobile-friendly sites that capture the character of your business while ranking for the searches your customers actually make — whether they're locals or weekenders exploring the lake.",
        ],
        "why": "In a destination market like Montgomery, much of your traffic is mobile and ready to act. A website that loads instantly and makes it easy to call or book is what converts that visitor into a customer — and that's how First Byte builds.",
        "faqs": [
            ("Do you design websites for Montgomery, TX businesses?",
             "Yes. First Byte serves Montgomery and the Lake Conroe area from nearby The Woodlands."),
            ("I run a small Montgomery business — is a custom site worth it?",
             "For most local businesses, yes. A fast, well-built site pays for itself in leads and credibility. We scope every project to your budget."),
            ("Will my site work well for mobile visitors?",
             "Every First Byte website is mobile-first — critical in a market like Montgomery where most searches happen on a phone."),
        ],
    },
    "houston": {
        "city": "Houston",
        "intro": [
            "Houston is one of the most competitive markets in the country — which means an average website simply won't cut through. First Byte builds custom web design for Houston, TX businesses that's fast, conversion-focused, and engineered to compete with brands spending far more.",
            "Whether you serve a neighborhood or the whole metro, we build sites that rank for the searches that matter, load in a blink, and turn visitors into customers. No templates, no fluff — just websites that work as hard as you do.",
        ],
        "why": "In a market as large and competitive as Houston, technical performance and conversion design are what separate the businesses that grow online from the ones that get buried. First Byte builds for both — speed that satisfies Google and design that satisfies your customers.",
        "faqs": [
            ("Do you build websites for Houston businesses?",
             "Yes. First Byte is based in The Woodlands and builds and optimizes websites for businesses across Greater Houston."),
            ("How do you help a Houston site stand out in a competitive market?",
             "Through fast, custom design, conversion-focused structure, and SEO built in from day one — so you compete on substance, not just ad budget."),
            ("How much does web design cost in Houston?",
             "It depends on scope; most projects range from a few thousand to the low five figures. Book a call for a fixed quote tailored to your goals."),
        ],
    },
}

BENEFITS = [
    "Custom, conversion-focused design built around your goals",
    "Mobile-first and lightning fast (tuned for Core Web Vitals)",
    "Local SEO built in so you rank in your city and beyond",
    "Easy-to-manage CMS your team can actually update",
    "Ongoing support from a local team that knows the market",
]


def esc(s):
    return htmllib.escape(s)


def inner_main(slug, d):
    city = d["city"]
    h1 = f"Web Design in {city}, TX"
    paras = "".join(f"<p>{esc(p)}</p>\n" for p in d["intro"])
    bullets = "".join(f"<li>{esc(b)}</li>\n" for b in BENEFITS)
    faqs = "".join(f'<h3{STYLE}>{esc(q)}</h3>\n<p>{esc(a)}</p>\n' for q, a in d["faqs"])
    return f"""<main class="main-content">
\t<div class="grid-container">
\t\t<div class="grid-x grid-padding-x posts-list">
\t\t\t<div class="cell small-12">
\t\t\t\t<h1 class="page-title page-title--archive"><span>{esc(h1)}</span></h1>
\t\t\t</div>
\t\t\t<div class="cell small-12"{STYLE}>
{paras}<h2{STYLE}>What's included</h2>
<ul>
{bullets}</ul>
<h2{STYLE}>Why {esc(city)} businesses choose First Byte</h2>
<p>{esc(d["why"])}</p>
<p{STYLE}>See examples of our <a href="{MAIN_SERVICE}">web design work</a>, then <a href="{CONTACT}">get in touch</a> to talk about your project.</p>
<p{STYLE}><a class="button-secondary" href="{CONTACT}">Let’s Talk</a></p>
<h2{STYLE}>Web Design in {esc(city)} — FAQs</h2>
{faqs}<p{STYLE}>Ready to grow your {esc(city)} business? <a class="button-secondary" href="{CONTACT}">Let’s Talk</a></p>
\t\t\t</div>
\t\t</div>
\t</div>
</main>"""


def page_schema(slug, d):
    url = f"{BASE}/web-design-{slug}-tx/"
    city = d["city"]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": url + "#webpage", "url": url,
             "name": f"Web Design in {city}, TX | First Byte",
             "isPartOf": {"@id": BASE + "/#website"},
             "about": {"@id": BASE + "/#localbusiness"}},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Web Design", "item": BASE + MAIN_SERVICE},
                 {"@type": "ListItem", "position": 3, "name": f"Web Design {city}", "item": url}]},
            {"@type": "FAQPage", "@id": url + "#faq",
             "mainEntity": [
                 {"@type": "Question", "name": q,
                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                 for q, a in d["faqs"]]},
        ],
    }
    return ('<script type="application/ld+json" data-seo-enhance="geo">'
            + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>")


def build(slug, d):
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    prefix = tpl.split('<main class="main-content">', 1)[0]
    suffix = tpl.split("</main>", 1)[1]

    page = prefix + inner_main(slug, d) + suffix

    url = f"{BASE}/web-design-{slug}-tx/"
    city = d["city"]
    title = f"Web Design in {city}, TX | First Byte"
    desc = (f"Custom web design and development for {city}, TX businesses. "
            f"First Byte builds fast, conversion-focused websites that turn "
            f"local visitors into customers. Let's talk.")

    # remove inherited schema scripts (AIOSEO @graph, web-design faq/geo)
    page = re.sub(r'\s*<script[^>]*class="aioseo-schema"[^>]*>.*?</script>',
                  "", page, flags=re.S | re.I)
    page = re.sub(r'\s*<script[^>]*data-seo-enhance="(faq|geo)"[^>]*>.*?</script>',
                  "", page, flags=re.S | re.I)

    # head: title, canonical, description
    page = re.sub(r"<title>[^<]*</title>", f"<title>{esc(title)}</title>", page, count=1)
    page = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>',
                  f'<link rel="canonical" href="{url}" />', page, count=1)
    page = re.sub(r'\s*<meta[^>]*data-seo-enhance="description"[^>]*>', "", page)
    metas = (f'<meta name="description" content="{esc(desc)}" data-seo-enhance="description" />\n'
             f'  <meta property="og:title" content="{esc(title)}" data-seo-enhance="geo-og" />\n'
             f'  <meta property="og:description" content="{esc(desc)}" data-seo-enhance="geo-og" />\n'
             f'  <meta property="og:url" content="{url}" data-seo-enhance="geo-og" />')
    page = re.sub(r'\s*<meta[^>]*data-seo-enhance="geo-og"[^>]*>', "", page)
    page = page.replace("</head>", "  " + metas + "\n  " + page_schema(slug, d) + "\n</head>", 1)

    outdir = os.path.join(OUT, f"web-design-{slug}-tx")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def main():
    for slug, d in CITIES.items():
        build(slug, d)
        print(f"  built /web-design-{slug}-tx/")
    print(f"\nGeo pages built: {len(CITIES)}")


if __name__ == "__main__":
    main()
