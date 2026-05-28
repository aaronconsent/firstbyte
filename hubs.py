#!/usr/bin/env python3
"""Build polished, visual /services/ and /service-areas/ hub pages.

These are full landing pages (sub-page hero + card grids + stats + map + CTA)
styled to match the homepage, using the theme's dark palette and fonts via a
scoped fb-* stylesheet. Idempotent. Run after geo_pages.py; enhance.py after.
"""
import os
import re
import json
import html as htmllib

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://firstbyte.agency"
TEMPLATE = os.path.join(OUT, "work_tax", "web-design-development", "index.html")
CONTACT = "/contact/"
PHONE = "+1-713-578-0634"
PHONE_DISPLAY = "(713) 578-0634"

from geo_pages import SERVICES, CITIES  # reuse matrix definitions

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

# Service-area cities (The Woodlands first; it links to the main service pages).
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

STYLE = """<style>
.fb-wrap{max-width:1180px;margin:0 auto;padding:0 1.5rem;}
.fb-hero{position:relative;overflow:hidden;padding:5.5rem 0 4rem;text-align:center;}
.fb-hero::before{content:"";position:absolute;left:50%;top:-10%;width:46rem;height:46rem;transform:translateX(-50%);
  background:radial-gradient(closest-side, rgba(1,246,242,.16), rgba(0,84,255,.10) 45%, rgba(190,0,187,.06) 70%, transparent 75%);
  filter:blur(10px);pointer-events:none;z-index:0;}
.fb-hero>*{position:relative;z-index:1;}
.fb-badge{display:inline-block;padding:.45rem 1rem;border:1px solid rgba(35,255,244,.5);border-radius:2rem;
  color:#23fff4;font-size:.72rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-bottom:1.5rem;}
.fb-h1{font-family:"Funnel Display",sans-serif;color:#fff;font-weight:700;line-height:1.05;
  font-size:clamp(2.4rem,6vw,4.5rem);margin:0 0 1.25rem;}
.fb-h1 .accent{color:#01f6f2;}
.fb-lead{max-width:42rem;margin:0 auto 2rem;font-size:1.12rem;line-height:1.7;color:hsla(0,0%,100%,.72);}
.fb-actions{display:flex;gap:.9rem;justify-content:center;flex-wrap:wrap;}
.fb-section{padding:3.5rem 0;}
.fb-section-head{text-align:center;max-width:42rem;margin:0 auto 2.75rem;}
.fb-h2{font-family:"Funnel Display",sans-serif;color:#fff;font-weight:700;font-size:clamp(1.9rem,4vw,3rem);line-height:1.1;margin:0 0 .9rem;}
.fb-sub{color:hsla(0,0%,100%,.65);font-size:1.05rem;line-height:1.6;margin:0;}
.fb-grid{display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fit,minmax(15.5rem,1fr));}
.fb-card{background:#171518;border:1px solid rgba(255,255,255,.08);border-radius:1.1rem;padding:1.9rem 1.6rem;
  transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;text-decoration:none;display:block;}
.fb-card:hover{transform:translateY(-4px);border-color:rgba(35,255,244,.45);box-shadow:0 14px 40px rgba(1,246,242,.08);}
.fb-ico{width:3rem;height:3rem;border-radius:.8rem;display:flex;align-items:center;justify-content:center;
  background:rgba(1,246,242,.10);color:#01f6f2;margin-bottom:1.1rem;}
.fb-ico svg{width:1.5rem;height:1.5rem;}
.fb-card h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.35rem;margin:0 0 .5rem;}
.fb-card p{color:hsla(0,0%,100%,.65);font-size:.95rem;line-height:1.55;margin:0 0 1rem;}
.fb-more{color:#01f6f2;font-weight:600;font-size:.9rem;}
.fb-stats{display:flex;flex-wrap:wrap;gap:1rem;justify-content:center;}
.fb-stat{flex:1 1 12rem;background:linear-gradient(180deg,#1b181c,#141215);border:1px solid rgba(255,255,255,.07);
  border-radius:1.1rem;padding:1.8rem 1.4rem;text-align:center;}
.fb-stat .num{font-family:"Funnel Display",sans-serif;color:#fff;font-size:2.4rem;line-height:1;}
.fb-stat .lbl{color:hsla(0,0%,100%,.6);font-size:.9rem;margin-top:.5rem;}
.fb-map{border:1px solid rgba(255,255,255,.1);border-radius:1.1rem;overflow:hidden;line-height:0;}
.fb-map iframe{width:100%;height:420px;border:0;filter:grayscale(.3) contrast(1.05);}
.fb-citycard{background:#171518;border:1px solid rgba(255,255,255,.08);border-radius:1.1rem;padding:1.6rem;}
.fb-citycard h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.3rem;margin:0 0 .4rem;}
.fb-citycard .blurb{color:hsla(0,0%,100%,.6);font-size:.9rem;line-height:1.5;margin:0 0 1rem;}
.fb-pills{display:flex;flex-wrap:wrap;gap:.4rem;}
.fb-pills a{font-size:.8rem;color:hsla(0,0%,100%,.82);text-decoration:none;border:1px solid rgba(255,255,255,.14);
  border-radius:2rem;padding:.3rem .8rem;transition:.18s;}
.fb-pills a:hover{border-color:#01f6f2;color:#01f6f2;}
.fb-cta{position:relative;overflow:hidden;text-align:center;background:linear-gradient(135deg,#161416,#0f0d10);
  border:1px solid rgba(35,255,244,.22);border-radius:1.4rem;padding:3.5rem 1.5rem;margin:1rem 0 0;}
.fb-cta h2{font-family:"Funnel Display",sans-serif;color:#fff;font-size:clamp(1.8rem,4vw,2.8rem);margin:0 0 .8rem;}
.fb-cta p{color:hsla(0,0%,100%,.7);margin:0 0 1.6rem;}
.fb-local{color:hsla(0,0%,100%,.72);font-size:1.05rem;line-height:1.75;max-width:48rem;}
.fb-local strong{color:#fff;}
</style>"""


def esc(s):
    return htmllib.escape(s)


def hero(badge, h1_html, lead):
    return f"""<section class="fb-hero"><div class="fb-wrap">
<span class="fb-badge">{esc(badge)}</span>
<h1 class="fb-h1">{h1_html}</h1>
<p class="fb-lead">{esc(lead)}</p>
<div class="fb-actions">
<a class="button-primary" href="{CONTACT}">Let’s Talk</a>
<a class="button-secondary" href="tel:{PHONE}">Call {PHONE_DISPLAY}</a>
</div></div></section>"""


def cta(title, text):
    return f"""<section class="fb-section"><div class="fb-wrap"><div class="fb-cta">
<h2>{esc(title)}</h2><p>{esc(text)}</p>
<div class="fb-actions"><a class="button-primary" href="{CONTACT}">Let’s Talk</a>
<a class="button-secondary" href="tel:{PHONE}">Call {PHONE_DISPLAY}</a></div>
</div></div></section>"""


def shell(inner, title, canonical, desc, schema):
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    prefix = tpl.split('<main class="main-content">', 1)[0]
    suffix = tpl.split("</main>", 1)[1]
    page = prefix + '<main class="main-content">' + STYLE + inner + "</main>" + suffix
    page = re.sub(r'\s*<script[^>]*class="aioseo-schema"[^>]*>.*?</script>', "", page, flags=re.S | re.I)
    page = re.sub(r'\s*<script[^>]*data-seo-enhance="(faq|geo)"[^>]*>.*?</script>', "", page, flags=re.S | re.I)
    page = re.sub(r'\s*<meta[^>]*data-seo-enhance="(description|geo-og)"[^>]*>', "", page)
    page = re.sub(r"<title>[^<]*</title>", f"<title>{esc(title)}</title>", page, count=1)
    page = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>', f'<link rel="canonical" href="{canonical}" />', page, count=1)
    metas = (f'<meta name="description" content="{esc(desc)}" data-seo-enhance="description" />\n'
             f'  <meta property="og:title" content="{esc(title)}" data-seo-enhance="geo-og" />\n'
             f'  <meta property="og:url" content="{canonical}" data-seo-enhance="geo-og" />')
    page = page.replace("</head>", "  " + metas + "\n  " + schema + "\n</head>", 1)
    return page


def write(parts, page):
    d = os.path.join(OUT, *parts)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_services():
    cards = ""
    for slug, svc in SERVICES.items():
        cards += (f'<a class="fb-card" href="{svc["main"]}">'
                  f'<div class="fb-ico">{ICONS[slug]}</div>'
                  f'<h3>{esc(svc["name"])}</h3>'
                  f'<p>{esc(TAGLINE[slug])}</p>'
                  f'<span class="fb-more">Explore {esc(svc["name"])} &rarr;</span></a>')
    stats = "".join(f'<div class="fb-stat"><div class="num">{n}</div><div class="lbl">{esc(l)}</div></div>'
                    for n, l in [("$195M+", "in marketing funds managed"),
                                 ("50+", "businesses served"),
                                 ("10+", "industries")])
    inner = f"""{hero("What We Do", 'Marketing that grows your business, <span class="accent">one byte at a time</span>', "First Byte is a full-service digital marketing agency in The Woodlands, TX. From websites to ad campaigns to brand identity, we build the systems that bring you customers.")}
<section class="fb-section"><div class="fb-wrap">
<div class="fb-section-head"><h2 class="fb-h2">Our Services</h2><p class="fb-sub">Everything you need to get found, get chosen, and grow — under one roof.</p></div>
<div class="fb-grid">{cards}</div>
</div></section>
<section class="fb-section"><div class="fb-wrap"><div class="fb-stats">{stats}</div></div></section>
{cta("Ready to grow?", "Let's talk about what First Byte can do for your business.")}"""
    url = BASE + "/services/"
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                            "@id": url + "#webpage", "url": url, "name": "Our Services | First Byte",
                            "about": {"@id": BASE + "/#localbusiness"}}, separators=(",", ":")) + "</script>")
    page = shell(inner, "Digital Marketing Services in The Woodlands, TX | First Byte", url,
                 "Digital marketing services from First Byte: web design, performance marketing, brand development and influencer marketing for The Woodlands & Greater Houston.",
                 schema)
    write(["services"], page)


def city_card(name, blurb, links):
    pills = "".join(f'<a href="{u}">{esc(t)}</a>' for t, u in links)
    return (f'<div class="fb-citycard"><h3>{esc(name)}</h3>'
            f'<p class="blurb">{esc(blurb)}</p><div class="fb-pills">{pills}</div></div>')


def build_service_areas():
    cards = ""
    # The Woodlands -> main service pages
    wl_links = [(svc["name"], svc["main"]) for svc in SERVICES.values()]
    cards += city_card(WOODLANDS["name"], WOODLANDS["blurb"], wl_links)
    # other cities -> geo matrix pages
    for cslug, city in CITIES.items():
        links = [(svc["name"], f"/{sslug}-{cslug}-tx/") for sslug, svc in SERVICES.items()]
        cards += city_card(f'{city["name"]}, TX', CITY_BLURB.get(cslug, ""), links)

    map_q = "9000+Six+Pines+Dr,+The+Woodlands,+TX+77380"
    map_embed = (f'<div class="fb-map"><iframe title="First Byte service area map" loading="lazy" '
                 f'referrerpolicy="no-referrer-when-downgrade" '
                 f'src="https://www.google.com/maps?q={map_q}&z=10&output=embed"></iframe></div>')

    inner = f"""{hero("Service Areas", 'Serving The Woodlands &amp; <span class="accent">Greater Houston</span>', "Based in The Woodlands, First Byte helps businesses across the region get found online and grow. Find your city below.")}
<section class="fb-section"><div class="fb-wrap">
<div class="fb-section-head"><h2 class="fb-h2">Where we work</h2><p class="fb-sub">Local expertise across The Woodlands, Montgomery County, and the greater Houston metro.</p></div>
{map_embed}
<p class="fb-local" style="margin:2.5rem auto 0;text-align:center;">First Byte is rooted in <strong>The Woodlands, TX</strong> and partners with businesses throughout <strong>Spring, Conroe, Montgomery, Tomball, Magnolia</strong> and <strong>Houston</strong>. We pair local market knowledge with web design, marketing, branding and advertising that drives measurable results.</p>
</div></section>
<section class="fb-section"><div class="fb-wrap">
<div class="fb-section-head"><h2 class="fb-h2">Find your city</h2><p class="fb-sub">Pick your location to see the services we offer nearby.</p></div>
<div class="fb-grid">{cards}</div>
</div></section>
{cta("Not sure where to start?", "Wherever you are in Greater Houston, we'll help you grow. Let's talk.")}"""
    url = BASE + "/service-areas/"
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                            "@id": url + "#webpage", "url": url, "name": "Service Areas | First Byte",
                            "about": {"@id": BASE + "/#localbusiness"}}, separators=(",", ":")) + "</script>")
    page = shell(inner, "Service Areas — The Woodlands & Greater Houston | First Byte", url,
                 "First Byte serves The Woodlands, Spring, Conroe, Montgomery, Tomball, Magnolia and Houston with web design, marketing, branding and influencer marketing.",
                 schema)
    write(["service-areas"], page)


def main():
    build_services()
    print("  built /services/ (visual)")
    build_service_areas()
    print("  built /service-areas/ (visual)")


if __name__ == "__main__":
    main()
