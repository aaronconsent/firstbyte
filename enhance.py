#!/usr/bin/env python3
"""Post-process the static mirror with Local SEO + AEO enhancements.

Idempotent: safe to run after every crawl.py/rewrite.py. All injected blocks
carry a data-seo-enhance marker and are replaced (not duplicated) on re-run.

Usage:  python3 enhance.py
"""
import os
import re
import json
import html as htmllib
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://firstbyte.agency"
TODAY = date.today().isoformat()
# Set to Sean's GA4 Measurement ID (e.g. "G-XXXXXXXXXX") to enable analytics
# site-wide. Left empty = no analytics injected.
GA4_ID = ""

# ---- Business facts (verified from the live site) -------------------------
BUSINESS = {
    "name": "First Byte",
    "legalName": "First Byte",
    "description": "Award-winning digital marketing and advertising agency in "
                   "The Woodlands, TX helping brands grow through web design, "
                   "SEO, branding, paid advertising, PR and influencer marketing.",
    "telephone": "+1-713-578-0634",
    # Service-area business (home-based): no public street address.
    "addressLocality": "The Woodlands",
    "addressRegion": "TX",
    "addressCountry": "US",
    "lat": 30.1693,
    "lng": -95.4646,
    "serviceRadius_m": 48000,  # ~30 mi service radius around The Woodlands
    "logo": BASE + "/wp-content/uploads/2025/02/474564578_122209849448190241_1671659700825052575_n.jpg",
    "sameAs": [
        "https://www.facebook.com/FirstByteAgency",
        "https://www.linkedin.com/company/firstbyteagency/",
    ],
    "areaServed": ["The Woodlands", "Spring", "Conroe", "Montgomery",
                   "Tomball", "Magnolia", "Houston"],
    "services": ["Web Design & Development", "Performance Marketing",
                 "Brand Development", "Influencer Marketing",
                 "Search Engine Optimization", "Paid Advertising",
                 "Public Relations"],
}

# ---- Money-page overrides: path -> (h1, title, meta) ----------------------
MONEY = {
    "work_tax/web-design-development": (
        "Web Design in The Woodlands, TX",
        "Web Design in The Woodlands, TX | First Byte",
        "Custom web design and development for The Woodlands & Greater Houston "
        "businesses. First Byte builds fast, conversion-focused websites that "
        "turn visitors into customers. Let's talk.",
    ),
    "work_tax/performance-marketing": (
        "Performance Marketing in The Woodlands, TX",
        "Performance Marketing in The Woodlands, TX | First Byte",
        "Data-driven paid advertising and performance marketing for The "
        "Woodlands, TX. First Byte runs Google & Meta ad campaigns that "
        "generate measurable leads and ROI.",
    ),
    "work_tax/brand-development": (
        "Brand Development in The Woodlands, TX",
        "Brand Development in The Woodlands, TX | First Byte",
        "Strategic brand development and identity design in The Woodlands, TX. "
        "First Byte builds memorable brands that stand out and drive growth "
        "for Greater Houston businesses.",
    ),
    "work_tax/influencer-marketing": (
        "Influencer Marketing in The Woodlands, TX",
        "Influencer Marketing in The Woodlands, TX | First Byte",
        "Influencer marketing campaigns for The Woodlands & Houston brands. "
        "First Byte connects your business with the right creators to reach "
        "and convert new audiences.",
    ),
}

# Pages to exclude from sitemap (pagination, junk archives)
SITEMAP_EXCLUDE = re.compile(r"/page/\d+/")


def rel_url(path):
    """Local file path under OUT -> absolute site URL."""
    rel = os.path.relpath(path, OUT).replace(os.sep, "/")
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return BASE + "/" + rel if rel else BASE + "/"


# ---------------------------------------------------------------------------
def local_business_jsonld():
    b = BUSINESS
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": BASE + "/#localbusiness",
        "name": b["name"],
        "description": b["description"],
        "url": BASE + "/",
        "telephone": b["telephone"],
        "image": b["logo"],
        "logo": b["logo"],
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": b["addressLocality"],
            "addressRegion": b["addressRegion"],
            "addressCountry": b["addressCountry"],
        },
        "serviceArea": {
            "@type": "GeoCircle",
            "geoMidpoint": {"@type": "GeoCoordinates", "latitude": b["lat"], "longitude": b["lng"]},
            "geoRadius": str(b["serviceRadius_m"]),
        },
        "areaServed": [{"@type": "City", "name": c} for c in b["areaServed"]],
        "sameAs": b["sameAs"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Digital Marketing Services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}}
                for s in b["services"]
            ],
        },
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def inject_block(html, marker, block):
    """Replace an existing data-seo-enhance block with `marker`, else insert
    before </head>. Idempotent. Removes script- and meta-form blocks
    precisely so it never spans into unrelated <script>…</script> regions."""
    m = re.escape(marker)
    html = re.sub(r'\s*<script[^>]*data-seo-enhance="%s"[^>]*>.*?</script>' % m,
                  "", html, flags=re.S | re.I)
    html = re.sub(r'\s*<meta[^>]*data-seo-enhance="%s"[^>]*>' % m,
                  "", html, flags=re.I)
    return html.replace("</head>", "  " + block + "\n</head>", 1)


def meta_for(rel):
    """Return a meta description for a page that lacks one, or None to skip."""
    key = rel[:-len("/index.html")] if rel.endswith("/index.html") else rel
    key = key.lstrip("./")
    if key in MONEY:
        return MONEY[key][2]
    if key.startswith("work/"):
        return None  # handled per-case-study below
    if key == "contact":
        return ("Contact First Byte, a digital marketing agency in The "
                "Woodlands, TX. Call (713) 578-0634 or reach out to grow your "
                "business with web design, SEO and paid advertising.")
    if key == "terms-of-service":
        return None
    return None


def case_study_meta(html):
    m = re.search(r"<title>([^<]*)</title>", html)
    name = (m.group(1) if m else "").split(" - First Byte")[0].strip()
    if not name:
        return None
    return (f"{name} — a First Byte client case study. Digital marketing, web "
            f"design, branding and advertising by First Byte, The Woodlands, TX.")


def enhance_page(path):
    rel = "./" + os.path.relpath(path, OUT).replace(os.sep, "/")
    with open(path, encoding="utf-8") as f:
        html = f.read()
    orig = html
    key = rel[2:][:-len("/index.html")] if rel.endswith("/index.html") else rel[2:]

    # 1) LocalBusiness schema (every page, single stable @id)
    block = ('<script type="application/ld+json" data-seo-enhance="localbusiness">'
             + local_business_jsonld() + "</script>")
    html = inject_block(html, "localbusiness", block)

    # 1b) GA4 analytics (only when an ID is configured)
    if GA4_ID:
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}" data-seo-enhance="ga4"></script>'
              f'<script data-seo-enhance="ga4">window.dataLayer=window.dataLayer||[];'
              f'function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());'
              f'gtag("config","{GA4_ID}");</script>')
        html = inject_block(html, "ga4", ga)

    # 2) Meta description if missing
    if "<meta name=\"description\"" not in re.sub(
            r'<meta[^>]*data-seo-enhance="description"[^>]*>', "", html):
        desc = meta_for(rel)
        if desc is None and key.startswith("work/"):
            desc = case_study_meta(html)
        if desc:
            tag = ('<meta name="description" content="%s" data-seo-enhance="description" />'
                   % htmllib.escape(desc, quote=True))
            html = inject_block(html, "description", tag)

    # 3) Money pages: H1 + title
    if key in MONEY:
        h1_text, title, _ = MONEY[key]
        label = key.split("/")[-1]
        # promote the archive <h2> to a geo-optimized <h1>
        html = re.sub(
            r'<h2 class="page-title page-title--archive">.*?</h2>',
            '<h1 class="page-title page-title--archive"><span>%s</span></h1>' % htmllib.escape(h1_text),
            html, count=1, flags=re.S)
        html = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % htmllib.escape(title), html, count=1)

    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def write_robots():
    ai_bots = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "PerplexityBot",
               "ClaudeBot", "Claude-Web", "Google-Extended", "Applebot-Extended",
               "CCBot", "Bytespider"]
    lines = ["User-agent: *", "Allow: /", ""]
    for bot in ai_bots:
        lines += [f"User-agent: {bot}", "Allow: /", ""]
    lines += [f"Sitemap: {BASE}/sitemap.xml", ""]
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("\n".join(lines))


def write_sitemap():
    urls = []
    for root, _, files in os.walk(OUT):
        for fn in files:
            if fn != "index.html":
                continue
            p = os.path.join(root, fn)
            u = rel_url(p)
            if SITEMAP_EXCLUDE.search(u):
                continue
            urls.append(u)
    urls = sorted(set(urls))
    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        prio = "1.0" if u == BASE + "/" else ("0.9" if "/work_tax/" in u else "0.7")
        body += ["  <url>", f"    <loc>{u}</loc>",
                 f"    <lastmod>{TODAY}</lastmod>",
                 f"    <priority>{prio}</priority>", "  </url>"]
    body.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(body))
    return len(urls)


def write_llms():
    b = BUSINESS
    txt = f"""# First Byte

> {b['description']}

First Byte is a digital marketing and advertising agency based in
{b['addressLocality']}, {b['addressRegion']}, serving clients across the
Greater Houston area. Phone: (713) 578-0634. Service areas:
{', '.join(b['areaServed'])}.

## Services
""" + "".join(f"- {s}\n" for s in b["services"]) + f"""
## Key pages
- [Home]({BASE}/): Overview of First Byte's digital marketing services.
- [Web Design]({BASE}/work_tax/web-design-development/): Custom websites for The Woodlands businesses.
- [Performance Marketing]({BASE}/work_tax/performance-marketing/): Paid advertising and lead generation.
- [Brand Development]({BASE}/work_tax/brand-development/): Branding and identity design.
- [Influencer Marketing]({BASE}/work_tax/influencer-marketing/): Creator-led campaigns.
- [Contact]({BASE}/contact/): Get in touch to grow your business.

## About
First Byte is an award-winning agency helping brands in The Woodlands, TX and
Greater Houston grow their customer base through measurable digital marketing.
"""
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(txt)


def main():
    changed = 0
    for root, _, files in os.walk(OUT):
        for fn in files:
            if fn.endswith(".html"):
                if enhance_page(os.path.join(root, fn)):
                    changed += 1
    write_robots()
    n = write_sitemap()
    write_llms()
    print(f"HTML pages enhanced: {changed}")
    print(f"sitemap.xml: {n} URLs")
    print("robots.txt + llms.txt written")


if __name__ == "__main__":
    main()
