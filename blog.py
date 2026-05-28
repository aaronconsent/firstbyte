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
            ("p", "It's the first question almost every business owner asks us: <em>what's this going to cost?</em> The honest answer is \"it depends\" — but that's not helpful, so here's the real breakdown for businesses in The Woodlands and Greater Houston in 2026, including the ranges we actually quote, the factors that move them, and how to make sure you're spending on an asset instead of a liability."),
            ("p", "A website isn't a one-time expense like a piece of equipment — it's the hardest-working member of your sales team, available 24/7. So the right question isn't just \"what does it cost,\" but \"what will it return.\" Keep that lens as you read."),
            ("h2", "The short answer: typical price ranges"),
            ("p", "Most professional small-business websites in The Woodlands land between roughly $3,000 and $15,000. A simple, polished brochure site of five to ten pages sits at the lower end. A larger site with custom design, many service or location pages, integrations, or e-commerce climbs toward — and sometimes past — the top of that range."),
            ("p", "As a rough guide: a clean starter site for a new local business often runs $3,000–$6,000; a established service business that needs service-area pages and lead capture typically lands $6,000–$12,000; and a custom or e-commerce build with bookings, payments, or a large catalog starts around $12,000 and scales with complexity."),
            ("p", "Be cautious with anything advertised at a few hundred dollars. That's almost always a generic template with no strategy, no real SEO, and no support when something breaks — and it usually costs more to fix (or rebuild) later than it would have cost to do right the first time."),
            ("h2", "What actually drives the price"),
            ("p", "Five things move the number more than anything else. <strong>Page count</strong> is the most obvious — every page is design, copy, and testing. <strong>Design customization</strong> is next: a thoughtfully custom layout costs more than a lightly-edited template, but it's also what makes you look credible against bigger competitors."),
            ("p", "<strong>Functionality</strong> is the third lever — online booking, payments, member logins, or CRM integrations all add real engineering. <strong>Content</strong> is the fourth: if you need professional copywriting and photography rather than supplying your own, budget for it (it's usually worth it). And <strong>SEO</strong> is the fifth — a site built for search from the start costs a little more up front and pays for itself many times over."),
            ("h2", "Why \"cheap\" usually costs more"),
            ("p", "A slow, templated site that doesn't rank or convert isn't an asset — it's a liability that quietly loses you customers every day. If a bargain site brings in even one fewer client a month than a well-built one would, the \"savings\" evaporate almost immediately for most service businesses."),
            ("p", "We've rebuilt countless sites for owners who went cheap the first time, paid again to patch it, and ultimately paid a third time to do it properly. The math almost always favors building it right once. Judge the investment by what it generates, not by the sticker price alone."),
            ("h2", "Ongoing costs to budget for"),
            ("p", "Beyond the build, plan for a few predictable running costs: domain registration (around $15–$25/year), hosting (often modest or even free on modern static platforms), and optional ongoing support, updates, or SEO. Be wary of agencies that lock you into expensive mandatory monthly plans just to keep your own site online."),
            ("h2", "How to get an accurate quote"),
            ("p", "The best way to get a real number is a short conversation about your goals: how many pages, what the site needs to do, whether you have content ready, and what \"success\" looks like for your business. Any reputable agency should scope from there and give you a fixed, written quote — no surprises."),
            ("h2", "What you get with First Byte"),
            ("p", "Every site we build is custom, fast, mobile-first, and has local SEO baked in — see our <a href=\"/work_tax/web-design-development/\">web design services</a> for the full picture. We scope each project to your goals and budget, give you a fixed quote up front, and build something engineered to bring in customers, not just sit there looking nice."),
            ("p", "Want a real number for your project? <a href=\"" + CONTACT + "\">Get in touch</a> and we'll walk through it with you — no pressure, just a straight answer."),
        ],
    },
    {
        "slug": "seo-vs-paid-ads-woodlands-business",
        "title": "SEO vs. Paid Ads: Where Should Your Woodlands Business Spend First?",
        "date": "2026-03-10",
        "excerpt": "Both work — but they work differently. Here's how to decide "
                   "where a local business should put its first marketing dollars.",
        "body": [
            ("p", "If you only have so much to spend, where should it go — SEO or paid ads? It's one of the most common questions we hear from Woodlands business owners, and the honest answer is that they do different jobs. One rents you traffic today; the other builds an asset that pays off for years. Here's how to decide where your first marketing dollars belong."),
            ("h2", "Paid ads: fast, but you rent the traffic"),
            ("p", "Paid advertising — Google Search, Google Local Services, Meta — can put your offer in front of ready-to-buy customers within days. You set a budget, your ads go live, and qualified clicks start arriving almost immediately. For a business that needs the phone ringing this month, nothing beats it for speed."),
            ("p", "The catch is right there in the name: the moment you stop paying, the traffic stops. You're renting visibility, not owning it. That makes paid ads the right first move when you need leads <em>now</em>, you're launching, or you're testing a new offer or market. See how we approach this in <a href=\"/work_tax/performance-marketing/\">performance marketing</a>."),
            ("h2", "SEO: slower, but you own the asset"),
            ("p", "SEO is the opposite trade-off. It takes months to build momentum — typically three to six before you see real movement in a competitive market like Greater Houston. But once you rank, the traffic keeps coming without paying per click, and it compounds: every page you build and every review you earn strengthens the whole."),
            ("p", "For a local business, ranking in the Google map pack and organic results is one of the highest-ROI investments you can make over time. A blog post or service page that climbs the rankings can quietly generate leads for years at no marginal cost — the closest thing local marketing has to a flywheel."),
            ("h2", "A simple way to decide"),
            ("p", "If you need leads urgently or have a short-term promotion, weight toward paid. If you have a longer runway and want to lower your cost per lead over time, weight toward SEO. Most businesses sit in between — which is why the real answer is rarely either/or."),
            ("h2", "The honest recommendation: do both, in sequence"),
            ("p", "For most local businesses, the winning play is to <em>start</em> with paid ads to generate leads immediately, while investing in SEO in parallel. Over the next 6–12 months, your organic traffic grows, your cost per lead drops, and you can dial back ad spend — or reinvest it to scale faster — because you're no longer dependent on renting every visit."),
            ("p", "Think of paid ads as the lead engine you switch on today and SEO as the equity you build underneath it. Run together, they cost less per lead over time than either alone."),
            ("h2", "Don't forget the page they land on"),
            ("p", "Whichever you choose, the destination matters as much as the source. Sending traffic — paid or organic — to a slow or unfocused page wastes it. A fast, conversion-focused <a href=\"/work_tax/web-design-development/\">website</a> is what turns those hard-won clicks into actual customers."),
            ("p", "The exact mix depends on your margins, timeline, and competition. If you'd like a second opinion tailored to your business, <a href=\"" + CONTACT + "\">let's talk</a> — no pressure, just a straight recommendation."),
        ],
    },
    {
        "slug": "signs-your-website-needs-a-redesign",
        "title": "7 Signs Your Small Business Website Needs a Redesign",
        "date": "2026-04-15",
        "excerpt": "Not sure if your site is helping or hurting? These seven "
                   "warning signs mean it's time for a refresh.",
        "body": [
            ("p", "Your website is often the first impression a customer gets of your business — and an outdated one quietly costs you sales every day without you ever seeing the lost lead. Most owners don't redesign because the site \"broke\"; they redesign because it slowly stopped pulling its weight. Here are seven clear signs it's time, and what each one is really costing you."),
            ("p", "If you recognize even two or three of these, your site is likely working against you rather than for you. The good news: every one of them is fixable."),
            ("h2", "1. It's slow to load"),
            ("p", "If your site takes more than about three seconds to load, a large share of visitors leave before they ever see what you offer — and on mobile data, the bar is even lower. Speed is also a confirmed Google ranking factor through Core Web Vitals, so a slow site hurts twice: fewer people see it, and it ranks lower so fewer people find it in the first place."),
            ("h2", "2. It doesn't work well on phones"),
            ("p", "The majority of local searches happen on a phone. If your site requires pinching and zooming, has tiny tap targets, or pushes the phone number off-screen, you're frustrating most of your visitors at the exact moment they're ready to act. Google also indexes the mobile version of your site first, so a poor mobile experience drags down your rankings everywhere — even on desktop."),
            ("h2", "3. It looks dated"),
            ("p", "Design trends move fast, and customers judge credibility in seconds. A site that looked sharp five years ago can now read as \"is this business even still around?\" — especially next to a competitor with a clean, modern presence. Fair or not, an outdated design makes people assume an outdated business."),
            ("h2", "4. You can't update it yourself"),
            ("p", "If changing a phone number, price, or holiday hours means emailing a developer and waiting a week, your site is a bottleneck instead of a tool. Modern sites give you straightforward control over the things that change often, so your site always reflects reality — which matters for both customers and local SEO."),
            ("h2", "5. It doesn't show up on Google"),
            ("p", "If customers can't find you when they search for what you do, the site isn't doing its core job. Many older sites were never built with SEO in mind — no proper structure, no local signals, no content targeting the terms buyers actually use. A modern build bakes search optimization in from the ground up so you're discoverable, not buried."),
            ("h2", "6. It doesn't generate leads"),
            ("p", "A website should drive calls and form fills, not just exist as a digital business card. If yours gets visitors but few inquiries, the problem is usually structure and clarity: no obvious next step, a buried phone number, weak proof, or a confusing path to contact. Conversion-focused design fixes the leak between traffic and leads."),
            ("h2", "7. You're embarrassed to share it"),
            ("p", "This is the most honest test of all. If you hesitate before sending a prospect to your own website — or you'd rather just text them instead — that gut feeling is telling you something your analytics already know. Your site should be an asset you're proud to point people to."),
            ("h2", "What to do about it"),
            ("p", "You don't have to fix all seven at once, but if several ring true, a redesign will pay for itself faster than you'd expect — usually in recovered leads within the first few months. The key is to rebuild around your customers and your goals, not just a fresh coat of paint."),
            ("p", "Recognize a few of these? A modern, fast, conversion-focused site fixes all seven. Explore our <a href=\"/work_tax/web-design-development/\">web design services</a> or <a href=\"" + CONTACT + "\">get in touch</a> for a free, honest look at your current site."),
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


PER_PAGE = 12


def postcard(p):
    return (f'<a class="fb-card fb-postcard" href="/blog/{p["slug"]}/">'
            f'<div class="date">{tu.esc(p["date"])}</div>'
            f'<h3>{tu.esc(p["title"])}</h3>'
            f'<p>{tu.esc(p["excerpt"])}</p>'
            f'<span class="fb-more">Read more &rarr;</span></a>')


def reading_time(post):
    words = sum(len(re.sub(r"<[^>]+>", "", t).split()) for _k, t in post["body"])
    return max(1, round(words / 200))


def page_href(n):
    return "/blog/" if n == 1 else f"/blog/page/{n}/"


def pagination(cur, total):
    if total <= 1:
        return ""
    out = ['<nav class="fb-pagination" aria-label="Blog pages">']
    out.append(f'<a class="{"disabled" if cur == 1 else ""}" href="{page_href(cur-1)}">&larr; Prev</a>'
               if cur > 1 else '<span class="disabled">&larr; Prev</span>')
    for n in range(1, total + 1):
        out.append(f'<span class="cur">{n}</span>' if n == cur else f'<a href="{page_href(n)}">{n}</a>')
    out.append(f'<a href="{page_href(cur+1)}">Next &rarr;</a>'
               if cur < total else '<span class="disabled">Next &rarr;</span>')
    out.append("</nav>")
    return "".join(out)


def build_post(post):
    url = f"{BASE}/blog/{post['slug']}/"
    related = [p for p in reversed(POSTS) if p["slug"] != post["slug"]][:3]
    related_cards = "".join(postcard(p) for p in related)
    inner = (
        '<section class="fb-hero"><div class="fb-wrap">'
        '<span class="fb-badge">Article</span>'
        f'<h1 class="fb-h1 fb-h1--article">{tu.esc(post["title"])}</h1>'
        f'<p class="fb-postmeta">{tu.esc(post["date"])} · {reading_time(post)} min read · First Byte</p>'
        '</div></section>'
        + '<section class="fb-section"><div class="fb-wrap"><article class="fb-article">'
        + render_body(post["body"])
        + f'<p style="margin-top:2rem;"><a class="button-primary" href="{tu.CONTACT}">Let’s Talk</a></p>'
        + '<a class="fb-backlink" href="/blog/">&larr; Back to all articles</a>'
        + '</article></div></section>'
        + '<section class="fb-section"><div class="fb-wrap">'
          '<div class="fb-section-head"><h2 class="fb-h2">Keep reading</h2></div>'
          f'<div class="fb-grid">{related_cards}</div></div></section>'
        + tu.cta("Ready to grow your business?",
                 "Let’s talk about putting these ideas to work for you.")
    )
    page = tu.render(inner, post["title"] + " | First Byte", url, post["excerpt"], article_schema(post))
    tu.write(["blog", post["slug"]], page)


def build_index():
    posts = list(reversed(POSTS))  # newest first
    pages = [posts[i:i + PER_PAGE] for i in range(0, len(posts), PER_PAGE)]
    total = len(pages)
    desc = "Marketing, web design, and growth insights for The Woodlands & Greater Houston businesses, from the First Byte team."
    for idx, chunk in enumerate(pages):
        pageno = idx + 1
        url = BASE + page_href(pageno)
        cards = "".join(postcard(p) for p in chunk)
        sub = ("Marketing, web design, and growth insights for businesses in The Woodlands and Greater Houston."
               if pageno == 1 else f"More articles from First Byte — page {pageno} of {total}.")
        inner = (
            tu.hero("Blog", 'First Byte <span class="accent">Blog</span>', sub)
            + f'<section class="fb-section"><div class="fb-wrap"><div class="fb-grid">{cards}</div>'
              f'{pagination(pageno, total)}</div></section>'
            + tu.cta("Want results like these?", "Let’s talk about growing your business.")
        )
        schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
                  + json.dumps({"@context": "https://schema.org", "@type": "Blog",
                                "@id": BASE + "/blog/#blog", "name": "First Byte Blog",
                                "url": BASE + "/blog/",
                                "publisher": {"@id": BASE + "/#localbusiness"}},
                               ensure_ascii=False, separators=(",", ":")) + "</script>")
        title = "Blog | First Byte" if pageno == 1 else f"Blog (Page {pageno}) | First Byte"
        page = tu.render(inner, title, url, desc, schema)
        tu.write(["blog"] if pageno == 1 else ["blog", "page", str(pageno)], page)
    return total


def main():
    n = build_index()
    print(f"  built /blog/ (+{n - 1} paginated pages)")
    for p in POSTS:
        build_post(p)
    print(f"\nBlog pages built: {len(POSTS)} posts + {n} index page(s)")


if __name__ == "__main__":
    main()
