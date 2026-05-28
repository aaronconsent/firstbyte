#!/usr/bin/env python3
"""Build the /industries/ hub + 8 industry landing pages, each linking up to
all 7 service pages and the service-area hub. Uses the shared theme_ui design.

Idempotent. Run after new_services.py/geo_pages.py (so service pages exist),
before navigation.py; re-run enhance.py after for sitemap + schema.
"""
import json
import theme_ui as tu
from geo_pages import SERVICES

BASE = tu.BASE

# Per-industry icons (teal stroke).
ICONS = {
    "retail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
    "technology": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>',
    "service": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 0 5.4-5.4l-2.7 2.7-2-2 2.7-2.7z"/></svg>',
    "banking": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10 12 3l9 7"/><path d="M5 10v9M19 10v9M9 10v9M15 10v9M3 21h18"/></svg>',
    "ecommerce": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2 3h2l2.5 13h12L21 7H6"/></svg>',
    "live-entertainment": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2 2 2 0 0 0 0 4 2 2 0 0 1-2 2H5a2 2 0 0 1-2-2 2 2 0 0 0 0-4z"/><path d="M9 6v12"/></svg>',
    "hospitality": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"/><path d="M2 16h20M6 10V7a2 2 0 0 1 2-2h3v5"/></svg>',
    "restaurants": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7a3 3 0 0 0 6 0V2M6 2v20M16 2c-1.5 0-3 1.5-3 5s1.5 5 3 5v10"/></svg>',
}

INDUSTRIES = {
    "retail": {
        "name": "Retail",
        "h1": 'Retail Marketing in <span class="accent">The Woodlands &amp; Greater Houston</span>',
        "lead": "Retail is a fight for attention and foot traffic. First Byte helps Houston-area retailers get found online, draw shoppers in, and keep them coming back.",
        "intro": [
            "Whether you run a boutique in Market Street or a multi-location store across the metro, today's shoppers research online before they ever walk in. If you're not visible when they search, you're losing sales to the store — or the website — that is.",
            "First Byte builds the online presence that drives real-world traffic: a fast site, a dominant local search footprint, and campaigns that turn browsers into buyers.",
        ],
        "tactics": [
            "Local SEO so nearby shoppers find your store first",
            "Google Business Profile optimization with photos, hours, and offers",
            "Conversion-focused website that showcases products",
            "Paid social and search ads that drive foot traffic and sales",
            "Reviews and reputation that build trust before the visit",
        ],
        "faqs": [
            ("How do you drive foot traffic to a retail store?",
             "A mix of strong local SEO, an optimized Google Business Profile, and geo-targeted ads puts your store in front of nearby shoppers exactly when they're looking."),
            ("Can you help a retail store that also sells online?",
             "Absolutely — we connect your in-store and online presence so both reinforce each other and you capture sales through whichever channel the customer prefers."),
        ],
    },
    "technology": {
        "name": "Technology",
        "h1": 'Technology &amp; SaaS Marketing in <span class="accent">Greater Houston</span>',
        "lead": "Tech buyers are skeptical and do their homework. First Byte builds the credibility, content, and pipeline that turn technical audiences into customers.",
        "intro": [
            "Marketing a technology or SaaS company is different — longer sales cycles, multiple decision-makers, and an audience that sees through hype. Generic marketing falls flat; you need substance and a steady pipeline.",
            "First Byte helps tech companies in the Houston area look credible, rank for the terms buyers search, and generate qualified leads that sales can actually close.",
        ],
        "tactics": [
            "Clear, credible web design that earns technical trust",
            "SEO and content that rank for high-intent industry terms",
            "Lead-generation campaigns built for longer B2B cycles",
            "Brand positioning that differentiates you from competitors",
            "Conversion tracking tied to pipeline, not just clicks",
        ],
        "faqs": [
            ("Do you understand B2B and SaaS sales cycles?",
             "Yes — we build campaigns and content around multi-touch, multi-stakeholder buying journeys, measuring pipeline and qualified leads rather than vanity metrics."),
            ("Can you help an early-stage tech company on a budget?",
             "We focus your spend on the highest-leverage channels first, so even a lean budget builds real, compounding visibility and pipeline."),
        ],
    },
    "service": {
        "name": "Service Businesses",
        "h1": 'Marketing for Service Businesses in <span class="accent">The Woodlands &amp; Houston</span>',
        "lead": "For home and professional services, the phone ringing is everything. First Byte builds the local visibility and lead flow that keep your schedule full.",
        "intro": [
            "Whether you're an HVAC company, a law firm, a clinic, or a contractor, your customers search \"near me\" and call the business that shows up first and looks trustworthy. Local search is your storefront.",
            "First Byte gets service businesses across Greater Houston ranking in the map pack, earning reviews, and converting searchers into booked jobs — consistently.",
        ],
        "tactics": [
            "Map-pack and \"near me\" local SEO",
            "Google Business Profile and review-generation systems",
            "Fast, mobile-first site with one-tap calling",
            "Google Local Services & Search Ads for instant leads",
            "Service-area pages across the cities you cover",
        ],
        "faqs": [
            ("How fast can a service business get more leads?",
             "Paid search and Local Services Ads can produce calls within days, while local SEO and reviews compound into steady, lower-cost leads over the following months."),
            ("Do you cover businesses with a large service area?",
             "Yes — we build out service-area pages and local signals so you rank across every city you serve, not just where you're based."),
        ],
    },
    "banking": {
        "name": "Banking & Finance",
        "h1": 'Banking &amp; Finance Marketing in <span class="accent">Greater Houston</span>',
        "lead": "In finance, trust is the product. First Byte builds the credible, compliant online presence that wins customers in a regulated, relationship-driven industry.",
        "intro": [
            "Banks, credit unions, and financial firms compete on trust and reputation as much as rates. Customers research carefully and choose institutions that feel established, secure, and local.",
            "First Byte helps financial businesses in the Houston area project that credibility online, rank for local financial searches, and turn reputation into new accounts and relationships.",
        ],
        "tactics": [
            "Professional, trust-building web design",
            "Local SEO for branch and service-area visibility",
            "Reputation and review management",
            "Content that demonstrates expertise and builds confidence",
            "Targeted advertising for specific products and audiences",
        ],
        "faqs": [
            ("Can you work within financial compliance requirements?",
             "Yes — we build messaging and campaigns mindful of the disclosures and standards financial marketing requires, and coordinate closely with your compliance team."),
            ("How does marketing help a local bank or credit union?",
             "By making you the visible, trusted, local choice — strong local search presence, reviews, and clear content turn nearby searchers into account holders."),
        ],
    },
    "ecommerce": {
        "name": "eCommerce",
        "h1": 'eCommerce Marketing in <span class="accent">The Woodlands &amp; Beyond</span>',
        "lead": "Online stores live or die by traffic and conversion. First Byte drives qualified shoppers to your store and turns more of them into buyers.",
        "intro": [
            "An eCommerce business doesn't have a salesperson on the floor — your website and your ads do all the selling. Every percentage point of conversion and every dollar of ad efficiency goes straight to your bottom line.",
            "First Byte helps online retailers grow profitably: product-focused SEO, paid campaigns that scale with ROAS, and conversion optimization that lifts revenue from the traffic you already have.",
        ],
        "tactics": [
            "Conversion-rate optimization across the funnel",
            "Google Shopping and Meta ads tuned for ROAS",
            "Product and category SEO",
            "Retargeting to recover abandoned shoppers",
            "Fast, mobile-first storefront design",
        ],
        "faqs": [
            ("How do you grow an online store profitably?",
             "We balance traffic and conversion — driving qualified shoppers through paid and organic channels while optimizing your store so more of them check out, protecting your margins."),
            ("Do you work with our existing eCommerce platform?",
             "Yes — we work across the major platforms, focusing on the marketing, ads, and conversion improvements that move revenue regardless of your tech stack."),
        ],
    },
    "live-entertainment": {
        "name": "Live Entertainment",
        "h1": 'Live Entertainment Marketing in <span class="accent">Greater Houston</span>',
        "lead": "Empty seats can't be sold twice. First Byte drives awareness and ticket sales for events, venues, and shows — on a deadline.",
        "intro": [
            "Live entertainment marketing is a race against the calendar. You have a fixed window to fill seats, and every campaign has to create buzz and convert it into ticket sales fast.",
            "First Byte builds the high-energy, time-sensitive campaigns that sell out events across the Houston area — combining paid reach, social momentum, and creator partnerships.",
        ],
        "tactics": [
            "Time-boxed paid social and search campaigns",
            "Influencer and creator partnerships for buzz",
            "Event landing pages built to convert to tickets",
            "Retargeting to push undecided buyers over the line",
            "Social content that builds anticipation",
        ],
        "faqs": [
            ("Can you run a campaign on a tight event timeline?",
             "Yes — fast-launch paid and social campaigns are exactly where we excel, scaling spend toward whatever's selling as the event approaches."),
            ("How do influencers help sell tickets?",
             "The right local creators put your event in front of engaged, nearby audiences with built-in trust — one of the most effective ways to drive ticket sales."),
        ],
    },
    "hospitality": {
        "name": "Hospitality",
        "h1": 'Hospitality Marketing in <span class="accent">The Woodlands &amp; Houston</span>',
        "lead": "Guests book what looks great and reads well. First Byte drives direct bookings for hotels, resorts, and hospitality brands across the metro.",
        "intro": [
            "In hospitality, your online presence is the first impression — and often the deciding one. Travelers compare options visually, read reviews obsessively, and book the property that earns their confidence.",
            "First Byte helps hospitality brands in the Houston area win that confidence: a beautiful, fast website, strong reviews, and campaigns that capture both local and visitor demand for direct bookings.",
        ],
        "tactics": [
            "Visually-driven, fast website that drives direct bookings",
            "Local and travel-intent SEO",
            "Reputation and review management",
            "Paid campaigns targeting visitors and locals",
            "Social content that showcases the experience",
        ],
        "faqs": [
            ("How do you increase direct bookings?",
             "By making your own site the easiest, most appealing place to book — strong visuals, fast performance, trust signals, and campaigns that send demand to you instead of third-party sites."),
            ("Can you reach both tourists and locals?",
             "Yes — we layer travel-intent and local targeting so you capture out-of-town visitors and nearby guests alike."),
        ],
    },
    "restaurants": {
        "name": "Restaurants",
        "h1": 'Restaurant Marketing in <span class="accent">The Woodlands &amp; Houston</span>',
        "lead": "Hungry customers decide fast and decide local. First Byte keeps your tables full with the visibility, reviews, and orders that drive growth.",
        "intro": [
            "When someone's deciding where to eat, they search, they scroll, and they read reviews — all in minutes. The restaurant that shows up looking great with strong ratings wins the visit.",
            "First Byte helps restaurants across the Houston area dominate local search, build a mouth-watering online presence, and turn searchers into diners and online orders.",
        ],
        "tactics": [
            "Local SEO and Google Business Profile optimization",
            "Review generation and reputation management",
            "Appetizing, fast, mobile-first website and menus",
            "Social content that drives cravings and visits",
            "Online-ordering and reservation promotion",
        ],
        "faqs": [
            ("How do you get more customers into a restaurant?",
             "Dominate local search, look irresistible online, and stack up recent five-star reviews — that combination is what turns a quick phone search into someone walking through your door."),
            ("Can you help with online ordering and delivery?",
             "Yes — we promote your ordering and reservation channels and make them easy to find, so more searches turn into orders and bookings."),
        ],
    },
}


def services_block(name):
    pills = " · ".join(
        f'<a href="{svc["main"]}">{tu.esc(svc["name"])}</a>' for svc in SERVICES.values())
    return (f'<section class="fb-section"><div class="fb-wrap">'
            f'<div class="fb-section-head"><h2 class="fb-h2">Services for {tu.esc(name)}</h2>'
            f'<p class="fb-sub">Every First Byte service, tailored to {tu.esc(name.lower())}.</p></div>'
            f'<p class="fb-prose" style="margin:0 auto;text-align:center;">{pills}</p></div></section>')


def areas_block(name):
    return ('<section class="fb-section"><div class="fb-wrap fb-narrow"><div class="fb-prose" style="text-align:center;">'
            f'<h2 class="fb-h2" style="margin-bottom:1rem;">Serving {tu.esc(name)} across Greater Houston</h2>'
            '<p>Based in The Woodlands, we work with '
            f'{tu.esc(name.lower())} in Spring, Conroe, Montgomery, Tomball, Magnolia, Houston and beyond. '
            'See <a href="/service-areas/">all the areas we serve</a>.</p></div></div></section>')


def build_page(slug, d):
    name = d["name"]
    url = f"{BASE}/industries/{slug}/"
    intro = "".join(f"<p>{tu.esc(p)}</p>" for p in d["intro"])
    bullets = "".join(f"<li>{tu.esc(b)}</li>" for b in d["tactics"])
    inner = (
        tu.hero(f"{name} Industry", d["h1"], d["lead"])
        + f'<section class="fb-section"><div class="fb-wrap fb-narrow"><div class="fb-prose">{intro}</div></div></section>'
        + '<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">What we do for {tu.esc(name.lower())}</h2></div>'
          f'<ul class="fb-checklist">{bullets}</ul></div></section>'
        + services_block(name)
        + areas_block(name)
        + '<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-section-head"><h2 class="fb-h2">{tu.esc(name)} Marketing FAQs</h2></div>'
          f'{tu.faqlist(d["faqs"])}</div></section>'
        + tu.cta(f"Ready to grow your {name.lower()} business?",
                 "Let’s talk about what First Byte can do for you.")
    )
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": url + "#webpage", "url": url,
             "name": f"{name} Marketing | First Byte",
             "isPartOf": {"@id": BASE + "/#website"},
             "about": {"@id": BASE + "/#localbusiness"}},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Industries", "item": BASE + "/industries/"},
                {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
            {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]},
        ],
    }
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps(graph, separators=(",", ":")) + "</script>")
    desc = f"{name} marketing for The Woodlands & Greater Houston. {d['lead']}"[:300]
    page = tu.render(inner, f"{name} Marketing in The Woodlands, TX | First Byte", url, desc, schema)
    tu.write(["industries", slug], page)


def build_hub():
    cards = ""
    for slug, d in INDUSTRIES.items():
        cards += (f'<a class="fb-card" href="/industries/{slug}/">'
                  f'<div class="fb-ico">{ICONS[slug]}</div>'
                  f'<h3>{tu.esc(d["name"])}</h3>'
                  f'<p>{tu.esc(d["lead"])}</p>'
                  f'<span class="fb-more">Explore {tu.esc(d["name"])} &rarr;</span></a>')
    inner = (
        tu.hero("Industries", 'Marketing built for <span class="accent">your industry</span>',
                "First Byte brings deep, industry-specific marketing to businesses across The Woodlands and Greater Houston. Find yours below.")
        + '<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-grid">{cards}</div></div></section>'
        + tu.cta("Don’t see your industry?", "We work across many more — let’s talk about yours.")
    )
    url = BASE + "/industries/"
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps({"@context": "https://schema.org", "@type": "WebPage",
                            "@id": url + "#webpage", "url": url, "name": "Industries | First Byte",
                            "about": {"@id": BASE + "/#localbusiness"}}, separators=(",", ":")) + "</script>")
    page = tu.render(inner, "Industries We Serve | First Byte", url,
                     "First Byte delivers industry-specific digital marketing for retail, technology, service, banking, eCommerce, live entertainment, hospitality and restaurants across Greater Houston.",
                     schema)
    tu.write(["industries"], page)


def main():
    build_hub()
    print("  built /industries/")
    for slug, d in INDUSTRIES.items():
        build_page(slug, d)
        print(f"  built /industries/{slug}/")


if __name__ == "__main__":
    main()
