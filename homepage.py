#!/usr/bin/env python3
"""Surface a featured "Industries we serve" section on the homepage, styled
with the shared fb-* design. Idempotent (marker-guarded). Run after
industries.py, before the final enhance.py.
"""
import os
import re
import theme_ui as tu
from industries import INDUSTRIES, ICONS

INDEX = os.path.join(tu.OUT, "index.html")
FEATURED = ["restaurants", "retail", "ecommerce", "hospitality", "service", "technology"]
START = "<!-- fb-home-industries -->"
END = "<!-- /fb-home-industries -->"


def build():
    if not os.path.exists(INDEX):
        return
    with open(INDEX, encoding="utf-8") as f:
        h = f.read()
    # remove any prior injection (idempotent)
    h = re.sub(re.escape(START) + ".*?" + re.escape(END), "", h, flags=re.S)

    cards = ""
    for slug in FEATURED:
        d = INDUSTRIES[slug]
        cards += (f'<a class="fb-card" href="/industries/{slug}/">'
                  f'<div class="fb-ico">{ICONS[slug]}</div>'
                  f'<h3>{tu.esc(d["name"])}</h3>'
                  f'<p>{tu.esc(d["lead"])}</p>'
                  f'<span class="fb-more">Explore {tu.esc(d["name"])} &rarr;</span></a>')

    section = (
        START + tu.STYLE
        + '<section class="fb-section" style="background:#0d0c0e;border-top:1px solid rgba(255,255,255,.06);">'
          '<div class="fb-wrap"><div class="fb-section-head">'
          '<h2 class="fb-h2">Industries we serve</h2>'
          '<p class="fb-sub">Industry-specific marketing for businesses across The Woodlands &amp; Greater Houston.</p></div>'
          f'<div class="fb-grid">{cards}</div>'
          '<p style="text-align:center;margin-top:2.25rem;"><a class="button-primary" href="/industries/">See all industries</a></p>'
          '</div></section>' + END
    )
    h = h.replace("</main>", section + "</main>", 1)
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(h)
    print("  injected featured industries on homepage")


if __name__ == "__main__":
    build()
