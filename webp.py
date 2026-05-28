#!/usr/bin/env python3
"""Convert uploaded JPG/PNG images to WebP and repoint image-loading
references to them (CWV win). Originals are kept on disk, and a reference is
only rewritten when the .webp file exists — so this can never create a
broken image. Only rendering attributes (src/srcset/data-lazy-*) are touched;
og:image / schema image refs are left as-is for social-preview compatibility.

Idempotent. Run before the final enhance.py.
"""
import os
import re
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
UPLOADS = os.path.join(OUT, "wp-content", "uploads")
QUALITY = 82

URL_RE = re.compile(r'(/wp-content/uploads/[^"\s,]+?)\.(jpe?g|png)', re.I)
ATTR_RE = re.compile(r'(src|srcset|data-lazy-src|data-lazy-srcset)="([^"]*)"', re.I)


def convert_all():
    made = 0
    if not os.path.isdir(UPLOADS):
        return made
    for root, _, files in os.walk(UPLOADS):
        for fn in files:
            low = fn.lower()
            if not low.endswith((".jpg", ".jpeg", ".png")):
                continue
            src = os.path.join(root, fn)
            dst = os.path.splitext(src)[0] + ".webp"
            if os.path.exists(dst):
                continue
            try:
                im = Image.open(src)
                if im.mode in ("P", "LA"):
                    im = im.convert("RGBA")
                elif im.mode not in ("RGB", "RGBA"):
                    im = im.convert("RGB")
                im.save(dst, "WEBP", quality=QUALITY, method=6)
                made += 1
            except Exception as e:  # noqa
                print(f"  ! convert fail {src}: {e}")
    return made


def _repl_url(m):
    webp_rel = (m.group(1) + ".webp").lstrip("/")
    if os.path.exists(os.path.join(OUT, webp_rel)):
        return m.group(1) + ".webp"
    return m.group(0)


def _repl_attr(m):
    return f'{m.group(1)}="{URL_RE.sub(_repl_url, m.group(2))}"'


def rewrite_refs():
    changed = 0
    for root, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(root, fn)
            with open(p, encoding="utf-8") as f:
                h = f.read()
            h2 = ATTR_RE.sub(_repl_attr, h)
            if h2 != h:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(h2)
                changed += 1
    return changed


def main():
    made = convert_all()
    changed = rewrite_refs()
    print(f"WebP created: {made} | HTML files repointed: {changed}")


if __name__ == "__main__":
    main()
