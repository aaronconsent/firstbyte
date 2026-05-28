#!/usr/bin/env python3
"""Fill empty image alt attributes with page-context-derived text for
accessibility, image SEO, and AEO. Idempotent (only touches alt="").

Derives the subject from each page's <title> (minus the brand suffix), so
images get alt text relevant to the page they're on. Run late in the
pipeline (after content is generated), before the final enhance.py.
"""
import os
import re
import html as htmllib

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")


def subject_of(html):
    m = re.search(r"<title>([^<]*)</title>", html)
    t = (m.group(1) if m else "First Byte").strip()
    for suf in (" | First Byte", " - First Byte", " — First Byte"):
        if t.endswith(suf):
            t = t[: -len(suf)]
    return htmllib.unescape(t).strip() or "First Byte"


def fill(html):
    subj = subject_of(html)
    alt = htmllib.escape(subj, quote=True)
    n = [0]

    def repl(m):
        n[0] += 1
        return m.group(0).replace('alt=""', f'alt="{alt}"', 1)

    html = re.sub(r'<img\b[^>]*\balt=""[^>]*>', repl, html)
    return html, n[0]


def main():
    total = 0
    for root, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(root, fn)
            with open(p, encoding="utf-8") as f:
                h = f.read()
            h2, c = fill(h)
            if c:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(h2)
                total += c
    print(f"Filled {total} empty alt attributes")


if __name__ == "__main__":
    main()
