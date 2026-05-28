#!/usr/bin/env python3
"""Shared visual design system (scoped fb-* CSS + render helpers) used by
hubs.py, geo_pages.py and blog.py so every generated page matches the
homepage look. Clones the theme shell (header/footer/head) from a template
page and injects the fb-* stylesheet + custom <main> content.
"""
import os
import re
import html as htmllib

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://firstbyte.agency"
CONTACT = "/contact/"
PHONE = "+1-713-578-0634"
PHONE_DISPLAY = "(713) 578-0634"
TEMPLATE = os.path.join(OUT, "work_tax", "web-design-development", "index.html")

STYLE = """<style>
.fb-wrap{max-width:1180px;margin:0 auto;padding:0 1.5rem;}
.fb-narrow{max-width:760px;}
.fb-hero{position:relative;overflow:hidden;padding:5rem 0 3.5rem;text-align:center;}
.fb-hero::before{content:"";position:absolute;left:50%;top:-10%;width:46rem;height:46rem;transform:translateX(-50%);
  background:radial-gradient(closest-side, rgba(1,246,242,.16), rgba(0,84,255,.10) 45%, rgba(190,0,187,.06) 70%, transparent 75%);
  filter:blur(10px);pointer-events:none;z-index:0;}
.fb-hero>*{position:relative;z-index:1;}
.fb-badge{display:inline-block;padding:.45rem 1rem;border:1px solid rgba(35,255,244,.5);border-radius:2rem;
  color:#23fff4;font-size:.72rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-bottom:1.4rem;}
.fb-h1{font-family:"Funnel Display",sans-serif;color:#fff;font-weight:700;line-height:1.05;
  font-size:clamp(2.2rem,5.5vw,4.2rem);margin:0 0 1.2rem;}
.fb-h1 .accent{color:#01f6f2;}
.fb-lead{max-width:42rem;margin:0 auto 2rem;font-size:1.12rem;line-height:1.7;color:hsla(0,0%,100%,.72);}
.fb-actions{display:flex;gap:.9rem;justify-content:center;flex-wrap:wrap;}
.fb-section{padding:3.25rem 0;}
.fb-section-head{text-align:center;max-width:42rem;margin:0 auto 2.5rem;}
.fb-h2{font-family:"Funnel Display",sans-serif;color:#fff;font-weight:700;font-size:clamp(1.8rem,4vw,2.8rem);line-height:1.1;margin:0 0 .9rem;}
.fb-sub{color:hsla(0,0%,100%,.65);font-size:1.05rem;line-height:1.6;margin:0;}
.fb-grid{display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fit,minmax(15.5rem,1fr));}
.fb-card{background:#171518;border:1px solid rgba(255,255,255,.08);border-radius:1.1rem;padding:1.9rem 1.6rem;
  transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;text-decoration:none;display:block;}
.fb-card:hover{transform:translateY(-4px);border-color:rgba(35,255,244,.45);box-shadow:0 14px 40px rgba(1,246,242,.08);}
.fb-ico{width:3rem;height:3rem;border-radius:.8rem;display:flex;align-items:center;justify-content:center;
  background:rgba(1,246,242,.10);color:#01f6f2;margin-bottom:1.1rem;}
.fb-ico svg{width:1.5rem;height:1.5rem;}
.fb-card h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.3rem;margin:0 0 .5rem;}
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
.fb-checklist{list-style:none;margin:0;padding:0;display:grid;gap:.85rem;grid-template-columns:repeat(auto-fit,minmax(17rem,1fr));}
.fb-checklist li{position:relative;padding-left:2rem;color:hsla(0,0%,100%,.8);line-height:1.5;}
.fb-checklist li::before{content:"";position:absolute;left:0;top:.05rem;width:1.3rem;height:1.3rem;border-radius:50%;background:rgba(1,246,242,.12);}
.fb-checklist li::after{content:"";position:absolute;left:.5rem;top:.28rem;width:.32rem;height:.6rem;border:solid #01f6f2;border-width:0 2px 2px 0;transform:rotate(45deg);}
.fb-prose{max-width:48rem;color:hsla(0,0%,100%,.78);font-size:1.06rem;line-height:1.75;}
.fb-prose p{margin:0 0 1.1rem;}
.fb-prose a{color:#01f6f2;}
.fb-faqlist{max-width:48rem;margin:0 auto;}
.fb-faq-item{border-top:1px solid rgba(255,255,255,.1);padding:1.3rem 0;}
.fb-faq-item h3{color:#fff;font-size:1.12rem;margin:0 0 .5rem;font-family:"Funnel Display",sans-serif;}
.fb-faq-item p{color:hsla(0,0%,100%,.66);margin:0;line-height:1.65;}
.fb-article{max-width:46rem;margin:0 auto;}
.fb-article h2{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.6rem;margin:2.2rem 0 .8rem;}
.fb-article p{color:hsla(0,0%,100%,.8);line-height:1.85;margin:0 0 1.15rem;font-size:1.06rem;}
.fb-article a{color:#01f6f2;}
.fb-meta{color:#01f6f2;font-size:.85rem;font-weight:600;margin:0 0 1.4rem;}
.fb-postcard .date{color:#01f6f2;font-size:.82rem;font-weight:600;margin-bottom:.45rem;}
.fb-postcard h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.3rem;margin:0 0 .6rem;line-height:1.25;}
.fb-postcard p{color:hsla(0,0%,100%,.65);font-size:.95rem;line-height:1.55;margin:0 0 1rem;}
.fb-cta{position:relative;overflow:hidden;text-align:center;background:linear-gradient(135deg,#161416,#0f0d10);
  border:1px solid rgba(35,255,244,.22);border-radius:1.4rem;padding:3.25rem 1.5rem;}
.fb-cta h2{font-family:"Funnel Display",sans-serif;color:#fff;font-size:clamp(1.7rem,4vw,2.6rem);margin:0 0 .8rem;}
.fb-cta p{color:hsla(0,0%,100%,.7);margin:0 0 1.5rem;}
.fb-backlink{display:inline-block;margin-top:2rem;color:hsla(0,0%,100%,.6);text-decoration:none;}
.fb-backlink:hover{color:#01f6f2;}
.fb-contact{display:grid;gap:1.5rem;grid-template-columns:1fr 1.15fr;align-items:start;}
@media(max-width:820px){.fb-contact{grid-template-columns:1fr;}}
.fb-infocard,.fb-formcard{background:#171518;border:1px solid rgba(255,255,255,.08);border-radius:1.1rem;padding:1.9rem;}
.fb-infocard h3,.fb-formcard h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.3rem;margin:0 0 1.1rem;}
.fb-inforow{display:flex;gap:.85rem;align-items:flex-start;margin-bottom:1.2rem;color:hsla(0,0%,100%,.78);font-size:.98rem;line-height:1.5;}
.fb-inforow .ic{color:#01f6f2;flex:0 0 auto;margin-top:.15rem;}
.fb-inforow a{color:#fff;text-decoration:none;}
.fb-inforow a:hover{color:#01f6f2;}
.fb-field{margin-bottom:1rem;}
.fb-field label{display:block;color:hsla(0,0%,100%,.8);font-size:.84rem;margin-bottom:.4rem;}
.fb-field input,.fb-field textarea{width:100%;box-sizing:border-box;background:#0f0d10;border:1px solid rgba(255,255,255,.14);
  border-radius:.6rem;padding:.72rem .9rem;color:#fff;font-family:inherit;font-size:.95rem;}
.fb-field input:focus,.fb-field textarea:focus{outline:none;border-color:#01f6f2;}
.fb-field textarea{min-height:130px;resize:vertical;}
.fb-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden;}
.fb-formmsg{margin-top:1rem;font-size:.92rem;min-height:1.2rem;}
.fb-formmsg.ok{color:#01f6f2;}
.fb-formmsg.err{color:#ff7a7a;}
.fb-formcard button[type=submit]{cursor:pointer;}
.fb-formcard button[disabled]{opacity:.6;cursor:default;}
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


def faqlist(faqs):
    items = "".join(f'<div class="fb-faq-item"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in faqs)
    return f'<div class="fb-faqlist">{items}</div>'


def render(inner, title, canonical, desc, schema, template=TEMPLATE):
    """Clone the theme shell and inject the fb-* stylesheet + custom main."""
    with open(template, encoding="utf-8") as f:
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
             f'  <meta property="og:description" content="{esc(desc)}" data-seo-enhance="geo-og" />\n'
             f'  <meta property="og:url" content="{canonical}" data-seo-enhance="geo-og" />')
    page = page.replace("</head>", "  " + metas + "\n  " + schema + "\n</head>", 1)
    return page


def write(parts, page):
    d = os.path.join(OUT, *parts)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
