#!/usr/bin/env python3
"""Rewrite absolute firstbyte.agency URLs to root-relative so the mirror is
portable (works on *.pages.dev preview and the production domain alike)."""
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
EXTS = (".html", ".htm", ".css", ".js", ".xml", ".json", ".svg")

# Order matters: handle escaped-slash JSON variants first.
REPLACEMENTS = [
    (r"https:\/\/firstbyte.agency", r"\/"),   # escaped JSON: https:\/\/host -> \/
    (r"http:\/\/firstbyte.agency", r"\/"),
    ("https://firstbyte.agency", ""),          # https://host/x -> /x
    ("http://firstbyte.agency", ""),
    ("//firstbyte.agency", ""),                # protocol-relative -> /x
]


def main():
    changed = 0
    for root, _, files in os.walk(OUT):
        for fn in files:
            if not fn.lower().endswith(EXTS):
                continue
            path = os.path.join(root, fn)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            orig = text
            for a, b in REPLACEMENTS:
                text = text.replace(a, b)
            if text != orig:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                changed += 1
                print(f"  rewrote {os.path.relpath(path, OUT)}")
    print(f"\nFiles rewritten: {changed}")


if __name__ == "__main__":
    main()
