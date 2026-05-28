#!/usr/bin/env python3
"""Build /services/ and /service-areas/ hub pages that link to every service
and geo page (hub-and-spoke internal linking + nav destinations).

Idempotent. Run after geo_pages.py; re-run enhance.py after.
"""
import os
import re
import json
import html as htmllib

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://firstbyte.agency"
S = ' style="margin-top:2.5rem;"'
TEMPLATE = os.path.join(OUT, "work_tax", "web-design-development", "index.html")

from geo_pages import SERVICES, CITIES  # reuse the matrix definitions


def esc(s):
    return htmllib.escape(s)


def shell(inner, title, canonical, desc, schema):
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    prefix = tpl.split('<main class="main-content">', 1)[0]
    suffix = tpl.split("</main>", 1)[1]
    page = prefix + inner + suffix
    page = re.sub(r'\s*<script[^>]*class="aioseo-schema"[^>]*>.*?</script>', "", page, flags=re.S | re.I)
    page = re.sub(r'\s*<script[^>]*data-seo-enhance="(faq|geo)"[^>]*>.*?</script>', "", page, flags=re.S | re.I)
    page = re.sub(r'\s*<meta[^>]*data-seo-enhance="(description|geo-og)"[^>]*>', "", page)
    page = re.sub(r"<title>[^<]*</title>", f"<title>{esc(title)}</title>", page, count=1)
    page = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>',
                  f'<link rel="canonical" href="{canonical}" />', page, count=1)
    metas = (f'<meta name="description" content="{esc(desc)}" data-seo-enhance="description" />\n'
             f'  <meta property="og:title" content="{esc(title)}" data-seo-enhance="geo-og" />\n'
             f'  <meta property="og:url" content="{canonical}" data-seo-enhance="geo-og" />')
    page = page.replace("</head>", "  " + metas + "\n  " + schema + "\n</head>", 1)
    return page


def write(path_parts, page):
    outdir = os.path.join(OUT, *path_parts)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_services():
    cards = ""
    for slug, svc in SERVICES.items():
        cards += (f'<h2{S}><a href="{svc["main"]}">{esc(svc["name"])}</a></h2>\n'
                  f'<p>{esc(svc["value"])}</p>\n')
    inner = f"""<main class="main-content">
\t<div class="grid-container">
\t\t<div class="grid-x grid-padding-x posts-list">
\t\t\t<div class="cell small-12">
\t\t\t\t<h1 class="page-title page-title--archive"><span>Our Services</span></h1>
\t\t\t</div>
\t\t\t<div class="cell small-12"{S}>
<p>First Byte is a full-service digital marketing agency in The Woodlands, TX. Explore what we do for businesses across Greater Houston.</p>
{cards}<p{S}><a class="button-secondary" href="/contact/">Let’s Talk</a></p>
\t\t\t</div>
\t\t</div>
\t</div>
</main>"""
    url = BASE + "/services/"
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                            "@id": url + "#webpage", "url": url, "name": "Our Services | First Byte",
                            "about": {"@id": BASE + "/#localbusiness"}},
                           ensure_ascii=False, separators=(",", ":")) + "</script>")
    page = shell(inner, "Our Services | First Byte", url,
                 "Digital marketing services from First Byte: web design, performance marketing, brand development and influencer marketing for The Woodlands & Greater Houston.",
                 schema)
    write(["services"], page)


def build_service_areas():
    blocks = ""
    for cslug, city in CITIES.items():
        cn = city["name"]
        links = " · ".join(
            f'<a href="/{sslug}-{cslug}-tx/">{esc(svc["name"])}</a>'
            for sslug, svc in SERVICES.items())
        blocks += f'<h2{S}>{esc(cn)}, TX</h2>\n<p>{links}</p>\n'
    inner = f"""<main class="main-content">
\t<div class="grid-container">
\t\t<div class="grid-x grid-padding-x posts-list">
\t\t\t<div class="cell small-12">
\t\t\t\t<h1 class="page-title page-title--archive"><span>Service Areas</span></h1>
\t\t\t</div>
\t\t\t<div class="cell small-12"{S}>
<p>First Byte is based in The Woodlands, TX and serves businesses across Greater Houston. Find your city below.</p>
{blocks}<p{S}><a class="button-secondary" href="/contact/">Let’s Talk</a></p>
\t\t\t</div>
\t\t</div>
\t</div>
</main>"""
    url = BASE + "/service-areas/"
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                            "@id": url + "#webpage", "url": url, "name": "Service Areas | First Byte",
                            "about": {"@id": BASE + "/#localbusiness"}},
                           ensure_ascii=False, separators=(",", ":")) + "</script>")
    page = shell(inner, "Service Areas | First Byte", url,
                 "First Byte serves The Woodlands, Spring, Conroe, Montgomery, Tomball, Magnolia and Houston with web design, marketing, branding and influencer marketing.",
                 schema)
    write(["service-areas"], page)


def main():
    build_services()
    print("  built /services/")
    build_service_areas()
    print("  built /service-areas/")


if __name__ == "__main__":
    main()
