#!/usr/bin/env python3
"""Strip leftover WordPress cruft from the static mirror:
  - "Written by <author> on <date>" bylines that link to dead /author/ pages
  - dead WP discovery <link> tags in <head> (/feed/, /wp-json/, oEmbed,
    api.w.org REST, xmlrpc RSD)

Idempotent. Run late in the pipeline (after navigation.py), before the
final enhance.py so the sitemap reflects the cleaned pages.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

# 1) Author bylines (the only place /author/ links appear).
BYLINE = re.compile(
    r'\s*<p class="preview__meta">Written by <a [^>]*href="/author/[^"]*"[^>]*>[^<]*</a> on [^<]*</p>',
    re.I)

# 2) Dead WP discovery <link> tags in <head>.
DEAD_LINKS = [
    re.compile(r'\s*<link[^>]*type=["\']application/rss\+xml["\'][^>]*>', re.I),   # RSS feed
    re.compile(r'\s*<link[^>]*type=["\']application/rsd\+xml["\'][^>]*>', re.I),   # xmlrpc RSD
    re.compile(r'\s*<link[^>]*rel=["\']https://api\.w\.org/["\'][^>]*>', re.I),    # REST root
    re.compile(r'\s*<link[^>]*href=["\'][^"\']*/wp-json/[^"\']*["\'][^>]*>', re.I),  # oEmbed + JSON
    re.compile(r'\s*<link[^>]*href=["\'][^"\']*xmlrpc\.php[^"\']*["\'][^>]*>', re.I),
    re.compile(r'\s*<link[^>]*href=["\'][^"\']*/feed/?["\'][^>]*>', re.I),
]


def clean(html):
    html = BYLINE.sub("", html)
    for pat in DEAD_LINKS:
        html = pat.sub("", html)
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
            h2 = clean(h)
            if h2 != h:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(h2)
                n += 1
    print(f"Cleaned WP cruft from {n} pages")


if __name__ == "__main__":
    main()
