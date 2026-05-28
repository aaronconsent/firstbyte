#!/usr/bin/env python3
"""Build polished, visual /services/ and /service-areas/ hub pages using the
shared theme_ui design system. Idempotent. Run after geo_pages.py; enhance.py after.
"""
import json
import theme_ui as tu
from geo_pages import SERVICES, CITIES  # reuse matrix definitions

BASE = tu.BASE

# Inline stroke icons (teal via currentColor), one per service.
ICONS = {
    "web-design": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="14" rx="2"/><path d="M2 9h20M7 14l-2 2 2 2M13 14l2 2-2 2"/></svg>',
    "performance-marketing": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-5 4 4 8-8"/><path d="M21 8v5M21 8h-5"/></svg>',
    "brand-development": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.5 5.5L20 11l-5.5 2.5L12 19l-2.5-5.5L4 11l5.5-2.5z"/></svg>',
    "influencer-marketing": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11v3a1 1 0 0 0 1 1h3l5 4V6L7 10H4a1 1 0 0 0-1 1z"/><path d="M16 8a4 4 0 0 1 0 8"/></svg>',
}
TAGLINE = {
    "web-design": "Fast, custom websites that turn visitors into customers.",
    "performance-marketing": "Google & Meta ads measured against leads and revenue.",
    "brand-development": "Memorable brands that command trust and scale.",
    "influencer-marketing": "Creator-led campaigns that convert real audiences.",
}
WOODLANDS = {"name": "The Woodlands",
             "blurb": "Our home base — a master-planned community and one of Houston's premier business hubs."}
CITY_BLURB = {
    "spring": "A fast-growing corridor just south of The Woodlands along I-45.",
    "conroe": "The seat of Montgomery County and one of the nation's fastest-growing cities.",
    "montgomery": "Small-town charm with steady Lake Conroe tourism and new growth.",
    "tomball": "Historic roots meeting rapid suburban growth northwest of Houston.",
    "magnolia": "A fast-growing community along the booming FM-1488 corridor.",
    "houston": "One of the largest, most competitive markets in the country.",
}


def build_services():
    cards = ""
    for slug, svc in SERVICES.items():
        cards += (f'<a class="fb-card" href="{svc["main"]}">'
                  f'<div class="fb-ico">{ICONS[slug]}</div>'
                  f'<h3>{tu.esc(svc["name"])}</h3>'
                  f'<p>{tu.esc(TAGLINE[slug])}</p>'
                  f'<span class="fb-more">Explore {tu.esc(svc["name"])} &rarr;</span></a>')
    stats = "".join(f'<div class="fb-stat"><div class="num">{n}</div><div class="lbl">{tu.esc(l)}</div></div>'
                    for n, l in [("$195M+", "in marketing funds managed"),
                                 ("50+", "businesses served"), ("10+", "industries")])
    inner = (
        tu.hero("What We Do", 'Marketing that grows your business, <span class="accent">one byte at a time</span>',
                "First Byte is a full-service digital marketing agency in The Woodlands, TX. From websites to ad campaigns to brand identity, we build the systems that bring you customers.")
        + '<section class="fb-section"><div class="fb-wrap">'
          '<div class="fb-section-head"><h2 class="fb-h2">Our Services</h2>'
          '<p class="fb-sub">Everything you need to get found, get chosen, and grow — under one roof.</p></div>'
          f'<div class="fb-grid">{cards}</div></div></section>'
        + f'<section class="fb-section"><div class="fb-wrap"><div class="fb-stats">{stats}</div></div></section>'
        + tu.cta("Ready to grow?", "Let's talk about what First Byte can do for your business.")
    )
    url = BASE + "/services/"
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                            "@id": url + "#webpage", "url": url, "name": "Our Services | First Byte",
                            "about": {"@id": BASE + "/#localbusiness"}}, separators=(",", ":")) + "</script>")
    page = tu.render(inner, "Digital Marketing Services in The Woodlands, TX | First Byte", url,
                     "Digital marketing services from First Byte: web design, performance marketing, brand development and influencer marketing for The Woodlands & Greater Houston.",
                     schema)
    tu.write(["services"], page)


def city_card(name, blurb, links):
    pills = "".join(f'<a href="{u}">{tu.esc(t)}</a>' for t, u in links)
    return (f'<div class="fb-citycard"><h3>{tu.esc(name)}</h3>'
            f'<p class="blurb">{tu.esc(blurb)}</p><div class="fb-pills">{pills}</div></div>')


def build_service_areas():
    cards = city_card(WOODLANDS["name"], WOODLANDS["blurb"],
                      [(svc["name"], svc["main"]) for svc in SERVICES.values()])
    for cslug, city in CITIES.items():
        links = [(svc["name"], f"/{sslug}-{cslug}-tx/") for sslug, svc in SERVICES.items()]
        cards += city_card(f'{city["name"]}, TX', CITY_BLURB.get(cslug, ""), links)

    map_q = "9000+Six+Pines+Dr,+The+Woodlands,+TX+77380"
    map_embed = (f'<div class="fb-map"><iframe title="First Byte service area map" loading="lazy" '
                 f'referrerpolicy="no-referrer-when-downgrade" '
                 f'src="https://www.google.com/maps?q={map_q}&z=10&output=embed"></iframe></div>')
    inner = (
        tu.hero("Service Areas", 'Serving The Woodlands &amp; <span class="accent">Greater Houston</span>',
                "Based in The Woodlands, First Byte helps businesses across the region get found online and grow. Find your city below.")
        + '<section class="fb-section"><div class="fb-wrap">'
          '<div class="fb-section-head"><h2 class="fb-h2">Where we work</h2>'
          '<p class="fb-sub">Local expertise across The Woodlands, Montgomery County, and the greater Houston metro.</p></div>'
          f'{map_embed}'
          '<p class="fb-prose" style="margin:2.5rem auto 0;text-align:center;">First Byte is rooted in '
          '<strong style="color:#fff;">The Woodlands, TX</strong> and partners with businesses throughout '
          'Spring, Conroe, Montgomery, Tomball, Magnolia and Houston — pairing local market knowledge with '
          'web design, marketing, branding and advertising that drives measurable results.</p></div></section>'
        + '<section class="fb-section"><div class="fb-wrap">'
          '<div class="fb-section-head"><h2 class="fb-h2">Find your city</h2>'
          '<p class="fb-sub">Pick your location to see the services we offer nearby.</p></div>'
          f'<div class="fb-grid">{cards}</div></div></section>'
        + tu.cta("Not sure where to start?", "Wherever you are in Greater Houston, we'll help you grow. Let's talk.")
    )
    url = BASE + "/service-areas/"
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                            "@id": url + "#webpage", "url": url, "name": "Service Areas | First Byte",
                            "about": {"@id": BASE + "/#localbusiness"}}, separators=(",", ":")) + "</script>")
    page = tu.render(inner, "Service Areas — The Woodlands & Greater Houston | First Byte", url,
                     "First Byte serves The Woodlands, Spring, Conroe, Montgomery, Tomball, Magnolia and Houston with web design, marketing, branding and influencer marketing.",
                     schema)
    tu.write(["service-areas"], page)


def main():
    build_services()
    print("  built /services/ (visual)")
    build_service_areas()
    print("  built /service-areas/ (visual)")


if __name__ == "__main__":
    main()
