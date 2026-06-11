#!/usr/bin/env python3
"""Generate the full service x city geo landing-page matrix.

4 services x 6 cities = 24 unique pages at /{service}-{city}-tx/.
Each page combines a unique per-combination opener + per-city context +
per-service value + service benefits + city-specific FAQ, so no two pages
are near-duplicates (avoids doorway-page penalties).

Clones the theme shell from the matching service page. Idempotent.
Run after service_pages.py; re-run enhance.py after to refresh sitemap.
"""
import os
import re
import json
import html as htmllib
import theme_ui as tu

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://firstbyte.agency"
CONTACT = "/contact/"
S = ' style="margin-top:2.5rem;"'

SERVICES = {
    "web-design": {
        "name": "Web Design",
        "main": "/work_tax/web-design-development/",
        "value": "First Byte builds custom, fast, mobile-first websites engineered to turn local searches into phone calls and form fills — no templates, with SEO baked in from day one.",
        "benefits": [
            "Custom, conversion-focused design built around your goals",
            "Mobile-first and lightning fast (tuned for Core Web Vitals)",
            "Local SEO built in so you rank in your city and beyond",
            "Easy-to-manage CMS your team can actually update",
            "Ongoing support from a local team that knows the market",
        ],
        "faq": ("How much does web design cost in {city}?",
                "Most {city} small-business websites range from a few thousand dollars to the low five figures depending on scope. Book a call for a fixed quote."),
        "opener": "A slow or dated website quietly sends {city} customers to your competitors every day.",
        "process": [
            ("Discover", "We start with a short call to learn what {city} customers you want, how you want to be found, and what's working (or leaking leads) today."),
            ("Design & build", "We design a custom site — no template — wired for speed, mobile, and conversion. You see and approve every page before it ships."),
            ("Launch & grow", "We launch, hand it back ready to go, and keep it improving month after month with measurable SEO and content updates."),
        ],
    },
    "performance-marketing": {
        "name": "Performance Marketing",
        "main": "/work_tax/performance-marketing/",
        "value": "First Byte runs Google and Meta ad campaigns measured against leads and revenue — not vanity metrics — and builds the landing pages and tracking to prove every dollar's ROI.",
        "benefits": [
            "Google & Meta ad management, end to end",
            "Landing pages built to convert the traffic you pay for",
            "Conversion tracking and transparent, lead-focused reporting",
            "Continuous A/B testing and optimization",
            "Local and national targeting that reaches the right buyers",
        ],
        "faq": ("What ad budget do {city} businesses need to start?",
                "We recommend a minimum monthly media budget so campaigns gather enough data to optimize, then right-size it to the {city} market on a strategy call."),
        "opener": "Ad spend without strategy is just expensive guessing for {city} businesses.",
        "process": [
            ("Audit", "We audit your current funnel, offer, and any past ad data for {city} relevance, then map the customer journey end to end."),
            ("Launch", "We build landing pages, dial in audience targeting around {city} and the surrounding market, and launch with full conversion tracking."),
            ("Scale what works", "Weekly optimization rolls budget into the creatives and audiences delivering real {city} leads — and ruthlessly kills the rest."),
        ],
    },
    "brand-development": {
        "name": "Brand Development",
        "main": "/work_tax/brand-development/",
        "value": "First Byte builds memorable brands — strategy, naming, logo, voice and a full visual identity — that command trust and scale cleanly across every channel.",
        "benefits": [
            "Brand strategy and market positioning",
            "Logo and complete visual identity",
            "Messaging and brand voice",
            "Brand guidelines that keep your team consistent",
            "Collateral and launch support",
        ],
        "faq": ("Can you refresh an existing {city} brand?",
                "Absolutely. We do both ground-up brand builds and strategic refreshes for established {city} businesses."),
        "opener": "In {city}, a strong brand is the difference between being a choice and being the choice.",
        "process": [
            ("Position", "We start with how {city} customers actually choose, then craft positioning that makes the choice obvious."),
            ("Design", "We build the full identity — logo, color, type, voice — wired for both digital and print, ready for the {city} market."),
            ("Apply & launch", "Brand guidelines, asset libraries, and launch collateral so your team can stay consistent everywhere customers see you."),
        ],
    },
    "influencer-marketing": {
        "name": "Influencer Marketing",
        "main": "/work_tax/influencer-marketing/",
        "value": "First Byte runs influencer campaigns end to end — sourcing and vetting the right creators, managing the partnership, and measuring real conversions, not just reach.",
        "benefits": [
            "Creator sourcing and vetting based on real audience fit",
            "Campaign strategy and hands-on management",
            "Content collaboration and approvals",
            "Performance tracking tied to your goals",
            "FTC-compliant partnerships that protect your brand",
        ],
        "faq": ("Does influencer marketing work for {city} businesses?",
                "Yes. Local and micro-influencers often drive the highest conversion for {city} service businesses because their audiences trust them and are nearby."),
        "opener": "The right creator can put your {city} brand in front of thousands of engaged local buyers.",
        "process": [
            ("Source", "We identify creators whose {city} audience actually overlaps with your customers — real engagement, not vanity follower counts."),
            ("Brief & approve", "We brief, manage, and approve every piece of content so your brand stays on-message and FTC-compliant."),
            ("Track & repeat", "We measure conversions, not just impressions, then re-invest in the creators delivering real {city} customers."),
        ],
    },
    "seo": {
        "name": "SEO",
        "main": "/services/seo/",
        "value": "First Byte gets your business found on Google — local SEO, technical optimization, and content that ranks and brings in customers month after month.",
        "benefits": [
            "Local SEO and Google Business Profile optimization",
            "Technical SEO and Core Web Vitals",
            "Keyword and content strategy",
            "On-page optimization that targets buyer intent",
            "Transparent ranking and traffic reporting",
        ],
        "faq": ("How long does SEO take to work in {city}?",
                "Local SEO usually shows movement in 3–6 months and compounds from there. We prioritize the fastest local wins first for {city} businesses."),
        "opener": "If customers can't find you on Google, growth in {city} stalls before it starts.",
        "process": [
            ("Audit & strategy", "We audit your site, Google Business Profile, citations, and the {city} competitive landscape, then map the fastest wins."),
            ("Build the foundation", "Technical SEO, schema, on-page optimization, GBP cleanup, and AEO content tuned for {city} customer searches."),
            ("Compound", "Monthly content and citation work that keeps you climbing in {city} search and the new AI engines."),
        ],
    },
    "paid-advertising": {
        "name": "Paid Advertising",
        "main": "/services/paid-advertising/",
        "value": "First Byte runs Google, Local Services, and social ad campaigns that put your offer in front of ready-to-buy customers and prove their return down to the dollar.",
        "benefits": [
            "Google Search and Local Services Ads",
            "Meta (Facebook & Instagram) advertising",
            "Conversion-focused landing pages",
            "Full conversion tracking and attribution",
            "Transparent, ROI-focused reporting",
        ],
        "faq": ("How fast will paid ads bring {city} leads?",
                "Paid campaigns can generate {city} leads within days of launch, then improve as we optimize toward your best-performing audiences over the first 30–60 days."),
        "opener": "Want new customers in {city} this week, not next quarter?",
        "process": [
            ("Setup", "Account structure, conversion tracking, and {city}-tight targeting on day one so every dollar is measurable from the start."),
            ("Launch", "Tightly-themed campaigns with landing pages built for the {city} customer journey — speed, clarity, single CTA."),
            ("Optimize", "We move budget toward what's working weekly, with transparent reporting tied to leads and revenue, not impressions."),
        ],
    },
    "public-relations": {
        "name": "Public Relations",
        "main": "/services/public-relations/",
        "value": "First Byte builds your reputation and visibility — media coverage, local press, and a brand story that earns trust and keeps you top of mind.",
        "benefits": [
            "Media outreach and press releases",
            "Local press and community visibility",
            "Online reputation management",
            "Thought-leadership content",
            "Crisis communication support",
        ],
        "faq": ("Is PR worth it for a small {city} business?",
                "Yes — local press and a strong reputation build the trust that turns {city} searchers into customers, and it amplifies every other channel you run."),
        "opener": "Great {city} businesses deserve to be known, not just found.",
        "process": [
            ("Position", "We find the story angles {city} press and customers actually care about — local impact, expertise, milestones."),
            ("Pitch", "We pitch {city} and Greater-Houston media, manage interviews, and place the story in front of the right audience."),
            ("Amplify", "We promote the coverage on your site, social, and search so it earns trust well beyond the original publication."),
        ],
    },
}

CITIES = {
    "spring": {"name": "Spring",
               "context": "Spring sits in one of the fastest-growing corridors in Texas, just south of The Woodlands along I-45, where local businesses compete hard for the same customers against national chains.",
               "why": "Spring's growth means more competition for the same local searches, so looking established and loading fast is how local businesses win the click first."},
    "conroe": {"name": "Conroe",
               "context": "As the seat of Montgomery County and one of the fastest-growing cities in the country, Conroe is full of opportunity — and full of businesses competing for it, from downtown to the Lake Conroe waterfront.",
               "why": "Conroe's rapid growth rewards businesses that look established online, signaling trust to the new residents and visitors who don't yet know the local players."},
    "montgomery": {"name": "Montgomery",
                   "context": "Montgomery blends small-town Texas charm with a steady stream of visitors and new residents drawn to Lake Conroe and its historic district.",
                   "why": "In a destination market like Montgomery, much of the audience is mobile and ready to act, so a fast site that makes it easy to call or book is what converts."},
    "tomball": {"name": "Tomball",
                "context": "Tomball pairs its historic small-town roots with rapid suburban growth on the northwest edge of Houston, drawing both longtime locals and new families.",
                "why": "Tomball's mix of established and new residents means businesses that show up clearly online capture customers who are still choosing who to trust."},
    "magnolia": {"name": "Magnolia",
                 "context": "Magnolia is a fast-growing community where established local businesses and a wave of new arrivals compete for the same customers along the FM-1488 corridor.",
                 "why": "Magnolia's steady growth rewards businesses that invest early in visibility, before the market gets more crowded."},
    "houston": {"name": "Houston",
                "context": "Houston is one of the largest and most competitive markets in the country, where an average online presence simply gets buried.",
                "why": "In a market as large as Houston, technical performance and conversion design separate the businesses that grow online from the ones that disappear."},
    "kingwood": {"name": "Kingwood",
                 "context": "Kingwood, the 'Livable Forest,' is an affluent, family-oriented community on Houston's northeast edge where residents expect polish and reliability from the businesses they hire.",
                 "why": "Kingwood customers research before they buy, so a professional, fast website and strong reviews are what earn the click and the call."},
    "humble": {"name": "Humble",
               "context": "Humble sits at a busy crossroads near Bush Intercontinental Airport, mixing established local businesses with constant new traffic and growth.",
               "why": "In a high-traffic hub like Humble, being easy to find and quick to act on is what turns passersby and searchers into customers."},
    "atascocita": {"name": "Atascocita",
                   "context": "Atascocita is one of the fastest-growing communities in the Houston area, with a young, expanding population of families near Lake Houston.",
                   "why": "Atascocita's steady influx of new residents rewards businesses that show up first in local search, before competitors are even on the radar."},
    "cypress": {"name": "Cypress",
                "context": "Cypress is a booming northwest Houston suburb where rapid residential growth has created strong, ongoing demand for local services.",
                "why": "Cypress's growth means new customers searching every day — businesses with solid local SEO capture that demand instead of leaving it on the table."},
    "katy": {"name": "Katy",
             "context": "Katy is a thriving, family-heavy suburb west of Houston known for its top schools and one of the region's most competitive local business markets.",
             "why": "Katy's competitive market rewards businesses that stand out with a fast, modern site and a strong reputation, not just a listing."},
    "sugar-land": {"name": "Sugar Land",
                   "context": "Sugar Land is an affluent, master-planned city in Fort Bend County with discerning customers and established, professional competition.",
                   "why": "Sugar Land buyers expect credibility, so a polished online presence and genuine social proof are what win their business."},
    "pearland": {"name": "Pearland",
                 "context": "Pearland is one of the fastest-growing cities in Texas, a large and expanding market south of Houston with plenty of room for local businesses to grow.",
                 "why": "Pearland's scale and growth mean real opportunity for businesses that invest in being found across the city, not just one neighborhood."},
    "willis": {"name": "Willis",
               "context": "Willis sits just north of Conroe near Lake Conroe, a smaller community seeing steady growth as the metro expands northward.",
               "why": "In a growing small town like Willis, early investment in local visibility lets a business own its market before it gets crowded."},
    "shenandoah": {"name": "Shenandoah",
                   "context": "Shenandoah is a small but commercially dense city right beside The Woodlands, packed with retail, dining, and service businesses along I-45.",
                   "why": "With heavy commercial competition in a tiny footprint, Shenandoah businesses live or die by how well they rank and convert online."},
    "porter": {"name": "Porter",
               "context": "Porter is a fast-developing community northeast of Houston near the Grand Parkway, drawing new families and businesses as the area expands.",
               "why": "Porter's rapid development means a wave of new customers — visibility now is how local businesses capture that growth early."},
    "new-caney": {"name": "New Caney",
                  "context": "New Caney is a growing community near the Valley Ranch and Grand Parkway corridor, with new retail and residential development reshaping the area.",
                  "why": "As New Caney grows, the businesses that show up first in local search build a lead that's hard for newcomers to catch."},
    "huntsville": {"name": "Huntsville",
                   "context": "Huntsville, home to Sam Houston State University, blends a steady student population with a established local community north of the metro.",
                   "why": "Huntsville's mix of students and locals rewards businesses that are easy to find on a phone and quick to respond."},
    "pinehurst": {"name": "Pinehurst",
                  "context": "Pinehurst is a growing community west of The Woodlands along the FM-1488 corridor, sharing in the area's strong residential expansion.",
                  "why": "Pinehurst's growth alongside Magnolia and The Woodlands makes early local visibility a smart, low-cost advantage."},
    "oak-ridge-north": {"name": "Oak Ridge North",
                        "context": "Oak Ridge North is a small, established city directly south of The Woodlands with a dense mix of local businesses along the I-45 corridor.",
                        "why": "In a compact, competitive market like Oak Ridge North, a fast site and strong reviews are what tip a nearby searcher your way."},
}


def esc(s):
    return htmllib.escape(s)


def inner_main(svc_slug, svc, city_slug, city):
    cn = city["name"]
    h1 = f"{svc['name']} in {cn}, TX"
    opener = svc["opener"].format(city=cn)
    fq, fa = svc["faq"]
    faqs = [
        (fq.format(city=cn), fa.format(city=cn)),
        (f"Do you work with businesses in {cn}, TX?",
         f"Yes — First Byte is based in nearby The Woodlands and regularly delivers {svc['name'].lower()} for {cn} businesses across every industry."),
        (f"Will this help my {cn} business get found online?",
         f"That's the goal of every engagement. We build with local search in mind so {cn} customers find you first."),
        (f"How is First Byte different from other {cn} agencies?",
         f"We're a local Greater-Houston team, not a national factory. Every {cn} project is led by a senior strategist, built with modern AI-assisted tooling so we ship in days instead of months, and tied to leads and revenue — not vanity metrics."),
        (f"Do you serve businesses outside {cn}?",
         "Yes — we serve the whole Greater Houston area from our base in The Woodlands, including Spring, Conroe, Montgomery, Tomball, Magnolia, Katy, Sugar Land, Pearland, Kingwood, Cypress, Atascocita, Humble, Huntsville and beyond."),
        (f"What does it cost to get started?",
         "Our flagship Launch plan is $250/month all-in, with no up-front website cost and no payment collected until your site is approved and ready to go live. See /launch/ for the full breakdown."),
    ]
    bullets = "".join(f"<li>{tu.esc(b)}</li>" for b in svc["benefits"])
    h1_html = f'{tu.esc(svc["name"])} in <span class="accent">{tu.esc(cn)}, TX</span>'
    lead = f"{opener} {svc['value']}"

    # Per-service 3-step process, with city woven into each step.
    proc_html = ""
    if svc.get("process"):
        steps = "".join(
            f'<div class="fb-card"><div class="fb-ico"><b>{i+1}</b></div>'
            f'<h3>{tu.esc(name)}</h3><p>{tu.esc(text.format(city=cn))}</p></div>'
            for i, (name, text) in enumerate(svc["process"])
        )
        proc_html = (
            '<section class="fb-section"><div class="fb-wrap">'
            f'<div class="fb-section-head"><h2 class="fb-h2">How we deliver {tu.esc(svc["name"].lower())} for {tu.esc(cn)} businesses</h2>'
            f'<p class="fb-sub">A clear, three-step approach so you always know what\'s next.</p></div>'
            f'<div class="fb-grid">{steps}</div></div></section>'
        )

    # Related resources — internal-link audit cross-links to industries, blog, and other services.
    related = (
        '<section class="fb-section"><div class="fb-wrap fb-narrow"><div class="fb-prose">'
        f'<h2 class="fb-h2" style="font-size:1.4rem;margin-bottom:.8rem">Related resources for {tu.esc(cn)} businesses</h2>'
        f'<p>Explore our full <a href="/services/">services hub</a> or browse the <a href="/industries/">industries we serve</a>. '
        f'Already have a website that\'s underperforming? Read <a href="/blog/10-website-mistakes-costing-customers/">10 website mistakes costing customers</a> '
        f'or our <a href="/blog/local-seo-checklist-the-woodlands/">local SEO checklist</a>. '
        f'Ready for a quote? Check out the <a href="/launch/">$250/mo Launch plan</a> or <a href="{tu.CONTACT}">get in touch</a>.</p>'
        '</div></div></section>'
    )

    inner = (
        tu.hero(svc["name"], h1_html, lead)
        + f'<section class="fb-section"><div class="fb-wrap fb-narrow"><div class="fb-prose">'
          f'<p>{tu.esc(city["context"])}</p>'
          f'<p>{tu.esc(city["why"])} See our <a href="{svc["main"]}">{tu.esc(svc["name"].lower())} work</a>, '
          f'then <a href="{tu.CONTACT}">get in touch</a>.</p></div></div></section>'
        + f'<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">What’s included</h2></div>'
          f'<ul class="fb-checklist">{bullets}</ul></div></section>'
        + proc_html
        + f'<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">{tu.esc(svc["name"])} in {tu.esc(cn)} — FAQs</h2></div>'
          f'{tu.faqlist(faqs)}</div></section>'
        + related
        + tu.cta(f"Ready to grow your {cn} business?",
                 "Let’s talk about what First Byte can do for you.")
    )
    return inner, h1, faqs


def page_schema(url, svc, city, h1, faqs):
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": url + "#webpage", "url": url,
             "name": f"{h1} | First Byte",
             "isPartOf": {"@id": BASE + "/#website"},
             "about": {"@id": BASE + "/#localbusiness"}},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": svc["name"], "item": BASE + svc["main"]},
                 {"@type": "ListItem", "position": 3, "name": h1, "item": url}]},
            {"@type": "FAQPage", "@id": url + "#faq",
             "mainEntity": [{"@type": "Question", "name": q,
                             "acceptedAnswer": {"@type": "Answer", "text": a}}
                            for q, a in faqs]},
        ],
    }
    return ('<script type="application/ld+json" data-seo-enhance="geo">'
            + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>")


def build(svc_slug, svc, city_slug, city):
    inner, h1, faqs = inner_main(svc_slug, svc, city_slug, city)
    url = f"{BASE}/{svc_slug}-{city_slug}-tx/"
    title = f"{h1} | First Byte"
    cn = city["name"]
    desc = (f"{svc['name']} for {cn}, TX businesses. First Byte helps {cn} "
            f"companies grow with {svc['name'].lower()} that drives real results. Let's talk.")
    template = os.path.join(OUT, svc["main"].strip("/"), "index.html")
    page = tu.render(inner, title, url, desc, page_schema(url, svc, city, h1, faqs), template=template)
    tu.write([f"{svc_slug}-{city_slug}-tx"], page)


def main():
    n = 0
    for svc_slug, svc in SERVICES.items():
        for city_slug, city in CITIES.items():
            build(svc_slug, svc, city_slug, city)
            n += 1
    print(f"Geo matrix pages built: {n}")


if __name__ == "__main__":
    main()
