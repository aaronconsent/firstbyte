#!/usr/bin/env python3
"""Generate a blog hub + cornerstone posts targeting local + informational
search intent. Clones the theme shell; idempotent (regenerates every run).

Output: site/blog/index.html and site/blog/<slug>/index.html
Run after enhance.py; re-run enhance.py once after to refresh sitemap.
"""
import os
import re
import json
import html as htmllib
from datetime import date, timedelta
import theme_ui as tu
import blog_posts

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://firstbyte.agency"
TEMPLATE = os.path.join(OUT, "work_tax", "web-design-development", "index.html")
CONTACT = "/contact/"
S = ' style="margin-top:2.5rem;"'

# Each post: slug, title, excerpt, list of (kind, text) content blocks.
# kind: 'p' paragraph (HTML allowed for links), 'h2' subhead.
ORIGINALS = [
    {
        "slug": "how-much-does-a-website-cost-the-woodlands",
        "title": "How Much Does a Website Cost in The Woodlands, TX? (2026 Guide)",
        "date": "2026-02-04",
        "excerpt": "A straight-talking breakdown of what a professional website "
                   "actually costs for a Woodlands business in 2026 — and what "
                   "drives the price up or down.",
        "body": [
            ("p", "It's the first question almost every business owner asks us: <em>what's this going to cost?</em> The honest answer is \"it depends\" — but that's not helpful, so here's the real breakdown for businesses in The Woodlands and Greater Houston in 2026."),
            ("h2", "The short answer"),
            ("p", "Most professional small-business websites in The Woodlands land between roughly $3,000 and $15,000. A simple, polished brochure site sits at the lower end; a larger site with custom design, many pages, integrations, or e-commerce climbs toward the top."),
            ("p", "Be cautious with anything advertised at a few hundred dollars — that's almost always a generic template with no strategy, no real SEO, and no support when something breaks. It usually costs more to fix later than to do right the first time."),
            ("h2", "What actually drives the price"),
            ("p", "Five things move the number: the number of pages, how custom the design is, functionality (booking, payments, integrations), whether you need copywriting and photography, and whether SEO is built in from the start. Each one adds real work — and real value."),
            ("h2", "Why \"cheap\" usually costs more"),
            ("p", "A slow, templated site that doesn't rank or convert isn't an asset — it's a liability that quietly loses you customers every day. A well-built site pays for itself in leads. That's the lens we'd encourage every owner to use: not \"what's the cheapest,\" but \"what generates the most business.\""),
            ("h2", "What you get with First Byte"),
            ("p", "Every site we build is custom, fast, mobile-first, and has local SEO baked in — see our <a href=\"/work_tax/web-design-development/\">web design services</a> for the full picture. We scope each project to your goals and budget and give you a fixed quote up front, so there are no surprises."),
            ("p", "Want a real number for your project? <a href=\"" + CONTACT + "\">Get in touch</a> and we'll walk through it with you."),
        ],
    },
    {
        "slug": "seo-vs-paid-ads-woodlands-business",
        "title": "SEO vs. Paid Ads: Where Should Your Woodlands Business Spend First?",
        "date": "2026-03-10",
        "excerpt": "Both work — but they work differently. Here's how to decide "
                   "where a local business should put its first marketing dollars.",
        "body": [
            ("p", "If you only have so much to spend, where should it go — SEO or paid ads? It's one of the most common questions we hear from Woodlands business owners, and the answer comes down to timing and goals."),
            ("h2", "Paid ads: fast, but you rent the traffic"),
            ("p", "Paid advertising (Google and Meta) can put your offer in front of ready-to-buy customers within days. The catch: the moment you stop paying, the traffic stops. It's the right first move when you need leads <em>now</em> or you're testing a new offer. See how we approach this in <a href=\"/work_tax/performance-marketing/\">performance marketing</a>."),
            ("h2", "SEO: slower, but you own the asset"),
            ("p", "SEO compounds. It takes months to build momentum, but once you rank, the traffic keeps coming without paying per click. For a local business, ranking in the map pack and organic results is one of the highest-ROI investments you can make over time."),
            ("h2", "The honest recommendation"),
            ("p", "For most local businesses, the answer isn't either/or — it's both, in sequence. Start paid ads to generate leads immediately, and invest in SEO in parallel so that over the next 6–12 months you're earning free traffic and relying less on ad spend."),
            ("p", "The exact mix depends on your margins, timeline, and competition. If you'd like a second opinion tailored to your business, <a href=\"" + CONTACT + "\">let's talk</a> — no pressure."),
        ],
    },
    {
        "slug": "signs-your-website-needs-a-redesign",
        "title": "7 Signs Your Small Business Website Needs a Redesign",
        "date": "2026-04-15",
        "excerpt": "Not sure if your site is helping or hurting? These seven "
                   "warning signs mean it's time for a refresh.",
        "body": [
            ("p", "Your website is often the first impression a customer gets — and an outdated one quietly costs you business. Here are seven signs it's time for a redesign."),
            ("h2", "1. It's slow to load"),
            ("p", "If your site takes more than a few seconds to load, visitors leave before they ever see it. Speed is also a Google ranking factor, so a slow site hurts twice."),
            ("h2", "2. It doesn't work on phones"),
            ("p", "Most local searches happen on mobile. If your site is hard to read or tap on a phone, you're losing the majority of your visitors."),
            ("h2", "3. It looks dated"),
            ("p", "Design trends move fast. A site that looked great five years ago can read as \"this business might not still be around\" today."),
            ("h2", "4. You can't update it yourself"),
            ("p", "If changing a phone number means emailing a developer and waiting a week, your site is working against you."),
            ("h2", "5. It doesn't show up on Google"),
            ("p", "If customers can't find you when they search, the site isn't doing its core job. Modern sites are built with SEO from the ground up."),
            ("h2", "6. It doesn't generate leads"),
            ("p", "A website should drive calls and form fills — not just exist. If yours isn't converting, the design and structure likely need rethinking."),
            ("h2", "7. You're embarrassed to share it"),
            ("p", "If you hesitate to send customers to your own site, that's the clearest sign of all."),
            ("p", "Recognize a few of these? A modern, fast, conversion-focused site fixes all seven. Explore our <a href=\"/work_tax/web-design-development/\">web design services</a> or <a href=\"" + CONTACT + "\">get in touch</a> for a free look at your current site."),
        ],
    },
]

# Full library: 49 cornerstone posts + 3 originals = 52, chronological (oldest
# first). Assign one publish date per week ending the most recent Thursday so
# the archive spans ~12 months.
POSTS = list(blog_posts.POSTS) + ORIGINALS
_LAST = date(2026, 5, 21)
_START = _LAST - timedelta(weeks=len(POSTS) - 1)
for _i, _p in enumerate(POSTS):
    _p["date"] = (_START + timedelta(weeks=_i)).isoformat()


def esc(s):
    return htmllib.escape(s)


def render_body(blocks):
    out = ""
    for kind, text in blocks:
        if kind == "h2":
            out += f"<h2>{tu.esc(text)}</h2>"
        else:
            out += f"<p>{text}</p>"  # links pre-escaped in source
    return out


def article_schema(post):
    url = f"{BASE}/blog/{post['slug']}/"
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": url + "#article",
        "headline": post["title"],
        "description": post["excerpt"],
        "datePublished": post["date"],
        "dateModified": post["date"],
        "author": {"@type": "Organization", "name": "First Byte", "url": BASE + "/"},
        "publisher": {"@id": BASE + "/#localbusiness"},
        "mainEntityOfPage": url,
    }
    return ('<script type="application/ld+json" data-seo-enhance="geo">'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>")


def build_post(post):
    url = f"{BASE}/blog/{post['slug']}/"
    inner = (
        tu.hero("Article", tu.esc(post["title"]), post["excerpt"])
        + '<section class="fb-section"><div class="fb-wrap"><article class="fb-article">'
        + f'<p class="fb-meta">Published {tu.esc(post["date"])} · First Byte</p>'
        + render_body(post["body"])
        + f'<p style="margin-top:2rem;"><a class="button-primary" href="{tu.CONTACT}">Let’s Talk</a></p>'
        + '<a class="fb-backlink" href="/blog/">&larr; Back to all articles</a>'
        + '</article></div></section>'
        + tu.cta("Ready to grow your business?",
                 "Let’s talk about putting these ideas to work for you.")
    )
    page = tu.render(inner, post["title"] + " | First Byte", url, post["excerpt"], article_schema(post))
    tu.write(["blog", post["slug"]], page)


def build_index():
    cards = ""
    for p in reversed(POSTS):  # newest first
        cards += (f'<a class="fb-card fb-postcard" href="/blog/{p["slug"]}/">'
                  f'<div class="date">{tu.esc(p["date"])}</div>'
                  f'<h3>{tu.esc(p["title"])}</h3>'
                  f'<p>{tu.esc(p["excerpt"])}</p>'
                  f'<span class="fb-more">Read more &rarr;</span></a>')
    inner = (
        tu.hero("Blog", 'First Byte <span class="accent">Blog</span>',
                "Marketing, web design, and growth insights for businesses in The Woodlands and Greater Houston.")
        + f'<section class="fb-section"><div class="fb-wrap"><div class="fb-grid">{cards}</div></div></section>'
        + tu.cta("Want results like these?", "Let’s talk about growing your business.")
    )
    desc = "Marketing, web design, and growth insights for The Woodlands & Greater Houston businesses, from the First Byte team."
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps({"@context": "https://schema.org", "@type": "Blog",
                            "@id": BASE + "/blog/#blog", "name": "First Byte Blog",
                            "url": BASE + "/blog/",
                            "publisher": {"@id": BASE + "/#localbusiness"}},
                           ensure_ascii=False, separators=(",", ":")) + "</script>")
    page = tu.render(inner, "Blog | First Byte", BASE + "/blog/", desc, schema)
    tu.write(["blog"], page)


def main():
    build_index()
    print("  built /blog/")
    for p in POSTS:
        build_post(p)
        print(f"  built /blog/{p['slug']}/")
    print(f"\nBlog pages built: {len(POSTS) + 1}")


if __name__ == "__main__":
    main()
