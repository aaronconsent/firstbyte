#!/usr/bin/env python3
"""Inject site-wide header + footer navigation into every page. Idempotent
(marked blocks are replaced each run). Header nav is hidden under 900px
(no hamburger), so the footer nav carries discovery on mobile.

Run late in the pipeline (after hubs.py), before the final enhance.py.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

NAV_LINKS = [
    ("Services", "/services/"),
    ("Service Areas", "/service-areas/"),
    ("Blog", "/blog/"),
    ("Contact", "/contact/"),
]

SERVICES_FOOTER = [
    ("Web Design", "/work_tax/web-design-development/"),
    ("Performance Marketing", "/work_tax/performance-marketing/"),
    ("Brand Development", "/work_tax/brand-development/"),
    ("Influencer Marketing", "/work_tax/influencer-marketing/"),
]
COMPANY_FOOTER = [
    ("Home", "/"),
    ("Services", "/services/"),
    ("Service Areas", "/service-areas/"),
    ("Blog", "/blog/"),
    ("Contact", "/contact/"),
    ("Terms of Service", "/terms-of-service/"),
]

STYLE = """<style>
.seo-mainnav{display:flex;flex-wrap:nowrap;align-items:center;gap:1.25rem;margin:0 1rem;flex:1;justify-content:center;}
.seo-mainnav a{color:#fff;text-decoration:none;font-weight:600;font-size:.9rem;white-space:nowrap;}
.seo-mainnav a:hover{color:#00fff2;}
@media (max-width:900px){.seo-mainnav{display:none;}}
.seo-footernav{display:flex;flex-wrap:wrap;gap:3rem;margin:2.5rem 0;}
.seo-footernav h3{color:#fff;font-size:1rem;margin:0 0 .75rem;}
.seo-footernav a{display:block;color:rgba(255,255,255,.75);text-decoration:none;margin:.4rem 0;font-size:.9rem;}
.seo-footernav a:hover{color:#00fff2;}
</style>"""


def header_nav():
    links = "".join(f'<a href="{u}">{t}</a>' for t, u in NAV_LINKS)
    return ('<!-- seo-nav:header -->' + STYLE
            + f'<nav class="seo-mainnav" aria-label="Primary">{links}</nav>'
            + '<!-- /seo-nav:header -->')


def footer_nav():
    svc = "".join(f'<a href="{u}">{t}</a>' for t, u in SERVICES_FOOTER)
    comp = "".join(f'<a href="{u}">{t}</a>' for t, u in COMPANY_FOOTER)
    return ('<!-- seo-nav:footer --><div class="seo-footernav">'
            f'<div><h3>Services</h3>{svc}</div>'
            f'<div><h3>Company</h3>{comp}</div>'
            '</div><!-- /seo-nav:footer -->')


def inject(html):
    # remove prior injected blocks (and any trailing whitespace we added)
    html = re.sub(r'<!-- seo-nav:header -->.*?<!-- /seo-nav:header -->\s*', "", html, flags=re.S)
    html = re.sub(r'<!-- seo-nav:footer -->.*?<!-- /seo-nav:footer -->\s*', "", html, flags=re.S)
    # header nav before the right-hand block (no added whitespace -> idempotent)
    if '<div class="header-block-right">' in html:
        html = html.replace('<div class="header-block-right">',
                             header_nav() + '<div class="header-block-right">', 1)
    # footer nav before the footer title
    if '<div class="footer-main-title">' in html:
        html = html.replace('<div class="footer-main-title">',
                             footer_nav() + '<div class="footer-main-title">', 1)
    return html


def main():
    n = 0
    for root, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(root, fn)
            with open(p, encoding="utf-8") as f:
                h = f.read()
            h2 = inject(h)
            if h2 != h:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(h2)
                n += 1
    print(f"Navigation injected into {n} pages")


if __name__ == "__main__":
    main()
