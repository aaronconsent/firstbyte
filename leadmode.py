#!/usr/bin/env python3
"""Inject the Lead Engine demo assets (CSS + JS) site-wide, before </body>.

The engine is OFF by default and renders nothing for normal visitors — it only
activates via the hidden demo control panel (/?demo=1) or /?leads=on. So this
injection is safe to ship to production. Idempotent (marker-guarded).

Run late in the pipeline (after navigation/cleanup), before the final enhance.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
START = "<!-- fb-lead-engine -->"
END = "<!-- /fb-lead-engine -->"
BLOCK = (START +
         '<link rel="stylesheet" href="/assets/leadmode.css?v=7">'
         '<script src="/assets/leadmode.js?v=7" defer></script>' + END)


def main():
    n = 0
    for root, _, files in os.walk(OUT):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(root, fn)
            with open(p, encoding="utf-8") as f:
                h = f.read()
            h2 = re.sub(re.escape(START) + ".*?" + re.escape(END), "", h, flags=re.S)
            if "</body>" in h2:
                h2 = h2.replace("</body>", BLOCK + "</body>", 1)
            if h2 != h:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(h2)
                n += 1
    print(f"Lead Engine injected into {n} pages")


if __name__ == "__main__":
    main()
