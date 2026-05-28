#!/usr/bin/env python3
"""Strip provably-dead, non-layout weight from the WP-mirrored pages to
improve Core Web Vitals — without touching anything that affects rendering
or theme behavior. Idempotent.

Removes site-wide:
  - MonsterInsights / legacy Google Analytics (we have our own GA4 hook now)
  - <script type="speculationrules"> blocks
  - WordPress emoji, wp-embed, and comment-reply scripts

Run after alt_text.py/webp.py and BEFORE the final enhance.py (so the GA4
hook, if enabled, is injected after this strips the legacy analytics).
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

# Inline <script> (no src) whose body contains a dead-weight signature.
_INLINE = lambda kw: re.compile(
    r'\s*<script\b(?![^>]*\bsrc=)[^>]*>(?:(?!</script>).)*?' + kw + r'(?:(?!</script>).)*?</script>',
    re.S | re.I)

PATTERNS = [
    _INLINE(r'MonsterInsights'),
    _INLINE(r'__gaTracker'),
    _INLINE(r'_wpemojiSettings'),
    re.compile(r'\s*<script\b[^>]*type="speculationrules"[^>]*>.*?</script>', re.S | re.I),
    # External scripts (analytics + WP cruft) — self-closing </script>
    re.compile(r'\s*<script\b[^>]*src="[^"]*(?:monsterinsights|googletagmanager\.com/gtag|google-analytics\.com)[^"]*"[^>]*>\s*</script>', re.I),
    re.compile(r'\s*<script\b[^>]*src="[^"]*wp-emoji-release[^"]*"[^>]*>\s*</script>', re.I),
    re.compile(r'\s*<script\b[^>]*src="[^"]*wp-includes/js/wp-embed[^"]*"[^>]*>\s*</script>', re.I),
    re.compile(r'\s*<script\b[^>]*src="[^"]*comment-reply[^"]*"[^>]*>\s*</script>', re.I),
    re.compile(r'\s*<style\b[^>]*>img\.wp-smiley[^<]*</style>', re.I),
    # Dead MonsterInsights HTML comments
    re.compile(r'\s*<!--(?:(?!-->).)*?MonsterInsights(?:(?!-->).)*?-->', re.S | re.I),
]

# Gravity Forms removal — the footer newsletter form is non-functional on a
# static host and is ~20KB/page. Strip the form, its inline scripts, external
# JS and CSS, and replace it with a simple subscribe link.
GF_FORM = re.compile(r"\s*<div[^>]*gform_wrapper[^>]*>.*?</form>\s*</div>", re.S | re.I)
GF_INLINE = _INLINE(r'(?:gform|gravityforms|GF_AJAX)')
GF_JS = re.compile(r'\s*<script\b[^>]*src="[^"]*(?:gravityforms\.min|placeholders\.jquery|jquery\.json)[^"]*"[^>]*>\s*</script>', re.I)
GF_CSS = re.compile(r'\s*<link\b[^>]*href="[^"]*(?:gravity-forms|gravityforms)[^"]*"[^>]*>', re.I)
GF_CTA = ('<div class="footer-bottom-right-form"><p style="color:hsla(0,0%,100%,.7);margin:0;">'
          'Want our weekly #SundayByte marketing tip? '
          '<a href="/contact/" style="color:#01f6f2;">Email us to subscribe &rarr;</a></p>')


def clean(html):
    for pat in PATTERNS:
        html = pat.sub("", html)
    if "gform_wrapper" in html:  # Gravity Forms present -> strip it (idempotent guard)
        html = GF_FORM.sub("", html)
        html = GF_INLINE.sub("", html)
        html = GF_JS.sub("", html)
        html = GF_CSS.sub("", html)
        html = html.replace('<div class="footer-bottom-right-form">', GF_CTA, 1)
    return html


def main():
    changed = 0
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
                changed += 1
    print(f"CWV: stripped dead weight from {changed} pages")


if __name__ == "__main__":
    main()
