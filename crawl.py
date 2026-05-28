#!/usr/bin/env python3
"""Static mirror of firstbyte.agency for Cloudflare Pages hosting."""
import os
import re
import sys
import time
import gzip
import io
from collections import deque
from urllib.parse import urljoin, urlparse, unquote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "https://firstbyte.agency"
HOST = urlparse(BASE).netloc
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

SEEDS = [
    "/",
    "/contact/",
    "/terms-of-service/",
    "/work_tax/brand-development/",
    "/work_tax/performance-marketing/",
    "/work_tax/web-design-development/",
    "/work_tax/influencer-marketing/",
]

visited = set()
saved_assets = set()
queue = deque()


JUNK = re.compile(r'(/wp-json/|/xmlrpc\.php|/feed/?$|/feed/|oembed|/comments/feed|wp-login|/wp-admin)', re.I)


def is_junk(url):
    return bool(JUNK.search(url))


def fetch(url, retries=3):
    last = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            with urlopen(req, timeout=45) as r:
                data = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
                ctype = r.headers.get("Content-Type", "")
                return data, ctype
        except Exception as e:  # noqa
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise last


def url_to_path(url):
    """Map a URL on our host to a local file path under OUT."""
    p = urlparse(url)
    path = unquote(p.path)
    if path.endswith("/") or path == "":
        path = path + "index.html"
    # path with no extension and not ending in / -> treat as page dir
    elif "." not in os.path.basename(path):
        path = path + "/index.html"
    local = os.path.join(OUT, path.lstrip("/"))
    return local


def same_host(url):
    return urlparse(url).netloc in ("", HOST)


def save(local, data):
    os.makedirs(os.path.dirname(local), exist_ok=True)
    with open(local, "wb") as f:
        f.write(data)


# Regexes for asset discovery
RE_HREF = re.compile(r'(href|src|data-lazy-src|data-src|data-bg|data-background|poster)\s*=\s*["\']([^"\']+)["\']', re.I)
RE_SRCSET = re.compile(r'(?:data-lazy-srcset|data-srcset|srcset)\s*=\s*["\']([^"\']+)["\']', re.I)
RE_CSS_URL = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', re.I)
RE_LINK_HREF = re.compile(r'<link[^>]+href\s*=\s*["\']([^"\']+)["\']', re.I)


def discover_from_html(html, base_url):
    pages, assets = set(), set()
    for m in RE_HREF.finditer(html):
        attr, val = m.group(1), m.group(2).strip()
        if val.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
            continue
        absu = urljoin(base_url, val)
        absu = absu.split("#")[0]
        if not same_host(absu) or is_junk(absu):
            continue
        if attr.lower() == "href" and looks_like_page(absu):
            # Skip WP dynamic/shortlink URLs (?p=, ?page_id=, ?share=, ?replytocom=)
            # — they are duplicates of canonical pages and collide on disk.
            if urlparse(absu).query:
                continue
            pages.add(absu)
        else:
            assets.add(absu)
    for m in RE_SRCSET.finditer(html):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if u and not u.startswith("data:"):
                absu = urljoin(base_url, u).split("#")[0]
                if same_host(absu):
                    assets.add(absu)
    # css/js referenced via link rel even if caught above; meta og:image etc.
    for m in re.finditer(r'content\s*=\s*["\'](https?://[^"\']+\.(?:png|jpe?g|webp|gif|svg|ico))["\']', html, re.I):
        absu = m.group(1).split("#")[0]
        if same_host(absu):
            assets.add(absu)
    return pages, assets


def looks_like_page(url):
    p = urlparse(url)
    base = os.path.basename(p.path)
    if "." in base:
        ext = base.rsplit(".", 1)[1].lower()
        return ext in ("html", "htm", "php")
    return True  # no extension -> a page route


def discover_from_css(css, base_url):
    assets = set()
    for m in RE_CSS_URL.finditer(css):
        u = m.group(1).strip()
        if u.startswith("data:"):
            continue
        absu = urljoin(base_url, u).split("#")[0].split("?")[0]
        if same_host(absu):
            assets.add(absu)
    return assets


def process():
    for s in SEEDS:
        queue.append(urljoin(BASE, s))

    # Crawl pages (BFS), collecting assets
    assets = set()
    while queue:
        url = queue.popleft().split("#")[0]
        if url in visited or is_junk(url):
            continue
        visited.add(url)
        try:
            data, ctype = fetch(url)
        except Exception as e:
            print(f"  ! page fail {url}: {e}")
            continue
        if "text/html" not in ctype:
            assets.add(url)
            continue
        html = data.decode("utf-8", "replace")
        local = url_to_path(url)
        save(local, html.encode("utf-8"))
        print(f"  page {url} -> {os.path.relpath(local, OUT)}")
        pages, a = discover_from_html(html, url)
        assets |= a
        for pg in pages:
            if pg not in visited:
                queue.append(pg)
        time.sleep(0.2)

    # Download assets (one pass; CSS may add more)
    asset_queue = deque(assets)
    while asset_queue:
        url = asset_queue.popleft().split("#")[0]
        key = url
        if key in saved_assets or is_junk(url):
            continue
        saved_assets.add(key)
        try:
            data, ctype = fetch(url)
        except Exception as e:
            print(f"  ! asset fail {url}: {e}")
            continue
        local = url_to_path(url)
        # don't treat asset query strings as dirs; strip ?ver=
        save(local, data)
        print(f"  asset {url} -> {os.path.relpath(local, OUT)}")
        if "css" in ctype or url.endswith(".css"):
            try:
                more = discover_from_css(data.decode("utf-8", "replace"), url)
                for m in more:
                    if m not in saved_assets:
                        asset_queue.append(m)
            except Exception:
                pass
        time.sleep(0.1)

    print(f"\nPages: {len([v for v in visited])}, Assets: {len(saved_assets)}")


if __name__ == "__main__":
    process()
