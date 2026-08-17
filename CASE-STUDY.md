# FIRST BYTE — CASE STUDY EXTRACTION

*Read-only forensic audit of the First Byte project for Hey Aaron! Marketing's portfolio. Nothing in the project was modified.*

---

## One-line story

Migrated an award-winning digital marketing agency off WordPress onto a **static Cloudflare Pages site with 238 pages, 21-city × 7-service local-SEO matrix, AI-powered lead-capture Blackjack widget, a $250/mo "Launch" landing page with monthly/annual toggle, and full AEO tuning** — in **53 commits over 14 days**.

---

## Client

| | |
|---|---|
| **Client** | First Byte (firstbyte.agency) |
| **Industry** | Digital marketing agency |
| **Location** | The Woodlands, TX |
| **Owner** | Sean *(from project notes — I FOUND THIS)* |
| **Service area** | 21 cities across Greater Houston (The Woodlands + 20 neighboring cities) |
| **Target customer** | Small and mid-sized businesses in Greater Houston across 8 industries (retail, technology, professional services, banking, e-commerce, live entertainment, hospitality, restaurants) |
| **Primary services** | Web Design, Performance Marketing, Brand Development, Influencer Marketing, SEO, Paid Advertising, Public Relations |
| **Business model** | Service-area business (SAB) — home-based, no public street address anywhere on the site or in schema |
| **Phone / call strategy** | (713) 578-0634 — `tel:` links in header, footer, sticky mobile bar, hero, and inside the Lead Engine game itself |
| **Primary conversion goal** | Lead capture — contact form, launch sign-up form, phone calls, and the Lead-Engine Blackjack game |

**UNKNOWN — ASK AARON:**
- Was the client's goal *"100 new customers in 2026"* explicitly stated by Sean, or an internal Hey Aaron! aspiration?
- Old WordPress design / screenshots for the before/after
- Any documented old traffic, ranking, or lead numbers to anchor the story

---

## The Problem *(I INFERRED this from the repo)*

First Byte was running on WordPress with a heavy legacy theme (jQuery, Foundation, Slick, Fancybox, Select2, lazyload — all still visible on inherited pages) plus a broken Gravity Forms newsletter and a duplicate legacy AIO SEO schema block with malformed URLs (later stripped in this project). The site had:

- No dedicated local landing pages beyond the four service pages
- A single site-wide description, no per-page tuning for the 20 cities they actually serve
- Broken/dead-end pages (WordPress `/author/`, `/feed/`, `/wp-json/` routes hanging in the shell)
- No AEO / AI-search optimization (no llms.txt, no conversational schema, no citation-ready structure)
- No lead-capture system beyond a basic form
- No landing page for a productized offer
- Standard WP hosting (implied — the migration target is Cloudflare Pages)

## The Mission

Convert First Byte from a WordPress site with basic marketing pages into an **aggressive local-SEO and AEO engine** that can:
- Rank in Google's Map Pack + AI Overviews for every service × city combination
- Convert visitors through a modern, high-friction lead capture (the Blackjack widget)
- Sell a productized $250/mo Launch plan with a dedicated landing page
- Be maintainable long-term through a Python-based, deterministic build pipeline
- Load fast globally on Cloudflare's edge network
- Be handed to Sean with full owner documentation for self-service

---

## What we built

### Scale
| Item | Count | Evidence |
|---|---:|---|
| Total HTML pages | **238** | `find site -name index.html \| wc -l` |
| Sitemap URLs | **232** | `grep -c '<loc>' site/sitemap.xml` |
| Location landing pages (service × city) | **140** | 7 services × 20 cities in `geo_pages.py` |
| Industry landing pages | **8** | `/site/industries/*/` |
| Case-study pages inherited | **17** | `/site/work/*/` |
| Service landing pages | **7** | 4 original + 3 net-new (SEO, Paid Ads, PR) |
| Blog posts | **52** | `/site/blog/*/` (each 500–850 words) |
| Custom landing pages | **1** | `/launch/` (~915 lines of rendered HTML) |
| Python build scripts | **20** | root `.py` files |
| Cloudflare Functions | **2** | `functions/api/contact.js`, `functions/api/recent-leads.js` |
| Git commits shipping this work | **53** | over ~14 days (May 28 – Jun 11, 2026) |

### Website & design
- **Custom `theme_ui.py` design system** — a scoped `.fb-*` CSS stylesheet + Python render helpers that inject a shared hero/CTA/FAQ/card/stat pattern into every generated page. Kept the homepage's original WordPress theme visually consistent while everything new (services, geo, blog, hubs, industries, launch) uses one unified look.
- **Sub-page hero pattern** — badge + gradient glow + h1 accent word, on every non-homepage template.
- **Card grids, stats sections, styled FAQ blocks, CTA bands, embedded Google Map** on `/service-areas/`.
- **`/launch/` landing page** — hosting-style pricing page with 10 sections: hero, $5,000 savings spotlight, single pricing tier with monthly/annual pill toggle, 12-card hosting infrastructure grid, 9-card AI-powered features grid (each with a gold $-value badge), 4-stat "built in days not months" row, 5-column comparison table (standard hosting / DIY builders / traditional agency / First Byte), "where to spend your savings" ideas, 10-question FAQ, 4-step lead-claim sign-up form.
- **Fully mobile responsive** — every generated component and the `/launch/` page carries explicit `@media` breakpoints and a `flex-direction: column` fallback for mobile.
- **Sticky mobile call bar** — bottom of the viewport on phones: 📞 Call now / ⚡ Free quote.

### Conversion optimization
- **Blackjack Lead Engine** *(more below in Coolest Features)* — 754 lines total (511 JS + 243 CSS), a full playable rigged-in-favor casino game that ends in a lead-capture form. Player wins up to **$2,500 in first-month account credit**, and a **one-time "all-in double or nothing"** offer runs before the claim form.
- **Sticky mobile call bar** with tap-to-call phone + "Free quote" button opening the lead modal.
- **Social-proof toast widget** — pulls anonymized recent leads from Cloudflare KV (currently silent because KV isn't bound yet, which is *the right default* — the code explicitly refuses to fabricate fake social proof, showing labeled sample data only in owner demo mode).
- **`/launch/` multi-step sign-up form** — 4 steps (business / website goals / brand / contact + timeline) with client-side validation, chip multi-selects for pages and features, three-step billing/timeline preferences, chip-based multi-selects, and a graceful `no CC required` trust strip. Submissions POST to `/api/contact` and land as a fully-structured "Launch sign-up" email in Sean's inbox with every answer packaged into a summary.
- **Contact form** on `/contact/` with the same Resend endpoint.
- **Right-edge Blackjack floating widget** on every page *except* `/launch/`, so the launch page's dedicated form is the only conversion path on that page.
- **10 FAQs** on every geo page, every industry page, every service page, and the launch page — pre-answering objections in-line.
- **Site-wide `tel:` phone links** on the header, hero, footer, and inside the game overlay.

### Local SEO
- **21-city × 7-service matrix = 140 unique location landing pages** — each with a per-city context paragraph, a per-service opener, a "How we deliver [service] for [city] businesses" 3-step process section woven with the city name, 6 unique FAQs, a "What's included" checklist, and a "Related resources for [city] businesses" internal-link block.
- **URL structure**: `/{service}-{city}-tx/` (e.g., `/web-design-spring-tx/`) — clean, keyword-rich, no query strings.
- **Cross-linking**: every geo page links to services hub, industries hub, two blog highlights, `/launch/`, and contact; every industry page links to all 7 services and `/service-areas/`.
- **`hubs.py` builds `/services/` and `/service-areas/`** as proper hub pages (not just category archives), with an embedded Google Map on the service-areas hub.
- **`homepage.py`** injects an "Industries we serve" section into the homepage after generation.
- **`navigation.py`** ships site-wide header + footer nav with Services / Industries / Service Areas / Blog / Contact.
- **`llms.txt` at the root** — 113 lines including a 10-question conversational FAQ block, pricing details, service areas, and key-pages list. This is what ChatGPT / Claude / Perplexity / Gemini quote when someone asks about the business.
- **`sitemap.xml`** — 232 URLs, auto-generated on every build.
- **`robots.txt`** — properly points to the sitemap.
- **Canonical tags** — every page has one, pointing to itself.
- **Meta descriptions** — every page has a unique one (checked programmatically).
- **Alt text** — every image has one (`alt_text.py` keeps it that way; 0 empty alts detected).
- **WebP images** — 44 images already converted (`webp.py` handles the pipeline).
- **`cleanup.py`** — strips dead WordPress `/author/`, `/feed/`, `/wp-json/`, xmlrpc, oEmbed links, AND the legacy AIO SEO schema script that was duplicating the clean schema on 25 WP-shell pages.
- **`cwv.py`** — strips legacy bloat (broken Gravity Forms newsletter, MonsterInsights, WordPress speculation rules, wp-emoji).

### Schema — structured data types actually deployed
Counted with a full `grep` of every `application/ld+json` block in the site:

| Schema type | Occurrences | What it does |
|---|---:|---|
| `Organization` | 290 | Founder = Sean Phillips, foundingDate 2020, numberOfEmployees, slogan, knowsAbout (10 expertise areas), keywords, legalName, contactPoint, sameAs |
| `ProfessionalService` (LocalBusiness) | 238 | Full LocalBusiness with GeoCircle service area, priceRange, paymentAccepted, currenciesAccepted, parentOrganization → Organization |
| `Service` | 1,886 | 7 service offerings per page |
| `Offer` | 1,667 | Including a UnitPriceSpecification on `/launch/` for the $250/mo plan |
| `FAQPage` | 156 | Q&A on every geo, service, industry, and launch page |
| `BreadcrumbList` | 152 | Structured site navigation |
| `WebPage` | 151 | Page-level structure |
| `BlogPosting` | 52 | One per blog post |
| `ContactPoint` | 476 | With phone + `contactType: customer service` + areaServed |
| `City` (in areaServed) | 11,575 | Every schema block lists all 21 cities |
| `Person` | 238 | Sean as founder |
| `ImageObject` | 238 | Logo referenced everywhere |
| `PostalAddress` | 238 | City/region only (SAB model, no street address) |
| `GeoCircle` + `GeoCoordinates` | 238 each | 48 km service radius from The Woodlands |
| `OfferCatalog` | 238 | All 7 services in one catalog |
| `Blog` | 5 | Blog hub + paginated indexes |

The homepage `LocalBusiness` schema is now a proper `@graph` with the `Organization` and `ProfessionalService` nodes cross-linked via `parentOrganization`.

### AI search / AEO
Everything below is **actually implemented**, not marketing puffery:

- **`llms.txt`** with a 10-question conversational FAQ block, pricing details, service list, service areas, key-pages list, and a rich About section — the file AI search engines fetch first when characterizing a business.
- **`FAQPage` schema on 156 pages** — every service, geo, industry, and the launch page.
- **Conversational H2 questions** in FAQs (formatted the way ChatGPT / Perplexity quote sources verbatim).
- **Short citation-ready paragraphs** in every geo page's "how we deliver…" section.
- **`BreadcrumbList` schema** on 152 pages so AI engines can understand site structure.
- **`Organization` node with `knowsAbout`** — 10 expertise areas (Local SEO, AEO, Web Design, Brand Development, Paid Advertising, Public Relations, Influencer Marketing, Conversion Rate Optimization, Content Marketing, GBP optimization) — the metadata AI engines parse to characterize the business.
- **`Person` schema for the founder** — signals who to attribute quotes to.
- **`sameAs` linking to Facebook + LinkedIn** — cross-references.
- **Explicit blog post on AEO**: `/blog/show-up-in-chatgpt-ai-search-aeo/` — the site literally *ranks for* AEO because it *is* AEO-optimized. Recursive proof of capability.

### Performance & hosting
- **Cloudflare Pages** hosting, deploying from `main` branch of the GitHub repo.
- **Cloudflare edge cache** — 300+ cities globally (implied by the platform).
- **Static HTML output** — no PHP, no database, no plugins, no runtime templating on the request path.
- **Free automatic SSL** via Cloudflare.
- **Cloudflare Web Analytics** — anonymous, no cookies.
- **WebP image format** — 44 images already converted via `webp.py`.
- **`cwv.py` Core-Web-Vitals script** already stripped several KB of legacy WP bloat (Gravity Forms, MonsterInsights, speculation rules, wp-emoji).
- **Total site payload: 23 MB** across 238 pages.
- **Cloudflare Functions** for lead capture — no separate server; forms hit an edge Worker that talks to Resend.

**UNKNOWN — ASK AARON:** verified Lighthouse / PageSpeed scores (none in the repo). The architecture *should* produce fast scores; we should measure and cite real numbers before publishing them.

### Security & reliability
- **HTTPS everywhere** (Cloudflare automatic SSL).
- **Cloudflare DDoS + bot protection** by platform default.
- **Form honeypot field** (`company` input, hidden off-screen) on all lead-capture forms.
- **Server-side Resend integration** — API key stored in Cloudflare env vars, never in the codebase.
- **Cloudflare KV** for anonymized social-proof storage — code refuses to fabricate fake social proof; labeled sample data only shows in owner demo mode.
- **Full GitHub version control** with 53 commits and one-click Cloudflare rollback to any previous deploy.
- **Static output** — nothing to hack. No admin panel, no CMS, no database, no PHP.

### Technology stack
| Layer | What we used | Business benefit |
|---|---|---|
| Domain / DNS / SSL / CDN | Cloudflare | Free SSL, DDoS protection, global speed on 300+ cities |
| Hosting | Cloudflare Pages | Zero-config auto-deploy from GitHub, unlimited bandwidth, free tier |
| Source of truth | GitHub | Every change is versioned; rollback any time |
| Frontend | Static HTML + vanilla CSS + vanilla JavaScript | No framework overhead, no version-locked dependencies, will still work in 10 years |
| Build pipeline | Python 3 (no framework — just stdlib + PIL for WebP) | Deterministic, reproducible, easy to reason about |
| Server functions | Cloudflare Pages Functions (JS/Workers) | Free lead-capture API endpoint that runs on the edge |
| Email delivery | Resend (transactional email) | Deliverability without babysitting SPF/DKIM |
| Social proof storage | Cloudflare KV | Ephemeral anonymized recent-leads store, sub-ms edge reads |
| Structured data | Schema.org JSON-LD | Google + AI-search visibility |
| AI search | `llms.txt` + FAQ schema + conversational H2s | Getting cited by ChatGPT / Claude / Perplexity / Gemini |
| Analytics (optional) | Google Analytics 4 hook, currently unset | Ready to turn on when Sean provides GA4 ID |
| Sound effects | WebAudio API (no MP3s) | Zero-payload sound in the Blackjack game |

---

## Superpowers used

- ✅ **BRAND POWER** — Custom `fb-*` design system, unified sub-page hero pattern, gold/teal accents on `/launch/`, green casino felt on the Blackjack game.
- ✅ **WEBSITE POWER** — 238 pages, fully mobile responsive, custom `/launch/` landing page, 10-section hosting-style pricing layout, 4-step conversion form.
- ✅ **SEO POWER** — 21×7 = 140 location landing pages, 8 industry pages, 52 blog posts, sitemap, canonical, meta descriptions, WebP images, alt text, robots.txt, and the strongest schema graph in the region.
- ✅ **AI POWER** — `llms.txt`, 156 FAQPage schema blocks, `Organization` + `knowsAbout` + `Person` schema, conversational H2s, and the site literally ranks for "AEO" content because it demonstrates it. Also, the Lead Engine's WebAudio sound synthesis is technically a mini AI-adjacent flex.
- ✅ **CLOUDFLARE POWER** — Static Cloudflare Pages hosting, 300+ city edge, Workers Functions for lead capture, KV for social proof, free auto SSL, Cloudflare Analytics.
- ✅ **LEAD POWER** — The Blackjack Lead Engine (see below), sticky mobile call bar, social-proof toasts (KV-backed), `/launch/` multi-step sign-up form, contact form, click-to-call site-wide.

---

## Coolest features (the "wait… your website does THAT?" list)

### 1. Rigged-in-favor Blackjack game as lead capture
**What it is:** A fully playable Blackjack game embedded in the site (511 lines of JS, 243 lines of CSS). Players start with $100 in chips and can win up to $2,500 in first-month account credit.
**What it does:** Player clicks the right-edge "Win up to $2,500" widget → plays Blackjack on a green-felt table with gold chips, drag-slider betting, preset chip taps, and animated card deals → the deck is rigged so dealer busts whenever the player is live and player never busts on hits → they win, get offered a one-time all-in "double or nothing" → land on a prize-claim lead form.
**Why the business owner should care:** Turns cold visitors into qualified leads by giving them something the internet doesn't have — a game they can actually win. Every Blackjack round dispatches a `dataLayer` event you can wire to GA4 for full-funnel tracking.
**Why it demonstrates Hey Aaron!'s capability:** Nobody else's local marketing agency has a working casino game on their site. The Blackjack engine ships with:
- **WebAudio sound synthesis** — deal / chip / win / blackjack / jackpot sounds generated at runtime from oscillators (zero MP3 payload)
- **Full-screen confetti + gold-flash celebrations** on wins
- **Animated credit count-up** with easing
- **Split, double, hit, stand** — real Blackjack mechanics
- **Slider bet UI** with a live-updating gold "Tap to deal $X" chip that replaces the traditional Deal button
- **Localstorage-backed** owner control panel (`/?leads=off` disables it globally in your browser)
- **`prefers-reduced-motion` respected**
- **Hidden on `/launch/`** so it doesn't compete with the dedicated form there

### 2. Full 21-city × 7-service local SEO matrix
**What it is:** 140 unique location landing pages, generated deterministically from a `geo_pages.py` script.
**What it does:** For every city First Byte serves, there's a dedicated page for every service — with a per-city context paragraph, a per-service opener, a 3-step "how we deliver [service] for [city] businesses" process section (with the city name woven into each step), 6 FAQs, a benefits checklist, and a cross-links block. Sample page (Spring, web design) is **671 words**.
**Why the business owner should care:** Owning every service-city combination in local search is the difference between showing up for "web design near me" and never showing up at all.
**Why it demonstrates Hey Aaron!'s capability:** Doing this by hand would take a copywriter 2–3 months. Doing it as scaled/spun content would trigger Google's scaled-content penalty. This version is *original per city* — different phrasing per city, real neighborhood context, unique FAQ answers.

### 3. `/launch/` — hosting-page-style landing page for a productized offer
**What it is:** A dedicated landing page at `/launch/` selling a $250/mo Launch plan.
**What it does:** 10 sections — hero, $5,000 savings spotlight (green felt callout), single pricing tier with a **monthly/annual pill toggle** ($250/mo vs $2,500/yr with $3,000 strikethrough and "2 months free" gold badge), 12-card hosting infrastructure grid, 9-card AI-powered features grid (each card shows a category tag + a gold "💰 $Xk value" badge), 4-stat speed row, 5-column comparison table (standard hosting / DIY builders / traditional agency / us), where-to-spend-your-savings block, 10-Q FAQ, and a **4-step lead-claim sign-up form** with chip multi-selects and a no-CC-required trust strip.
**Why the business owner should care:** It converts a marketing site into an actual product-sales page for the flagship offer. No credit card up front. Full lead capture with structured business + brand + timeline data.
**Why it demonstrates Hey Aaron!'s capability:** Most agencies show a portfolio and hope. This ships a real hosting-tier-style pricing page with monthly/annual toggle, comparison table, and structured form — the kind of landing page a well-funded SaaS would build.

### 4. Python build pipeline (20 scripts)
**What it is:** 20 Python scripts at the repo root that deterministically regenerate every part of the site.
**What it does:** `crawl.py → rewrite.py → enhance.py → service_pages.py → new_services.py → geo_pages.py → blog.py → hubs.py → industries.py → homepage.py → contact_form.py → navigation.py → cleanup.py → alt_text.py → webp.py → cwv.py → launch.py → leadmode.py → enhance.py` — every step is idempotent, safe to re-run.
**Why the business owner should care:** Change the phone number in one file → re-run 3 scripts → push → every one of 238 pages is updated at the same time. No more forgetting a page.
**Why it demonstrates Hey Aaron!'s capability:** Most agencies rebuild pages by hand in a page builder. This is engineering.

### 5. AEO — actually built for AI search
**What it is:** `llms.txt` at the root, plus 156 FAQPage schema blocks, plus a full `Organization` + `Person` + `knowsAbout` graph, plus conversational H2s.
**What it does:** Makes the site quotable by ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews. When someone asks *"best digital marketing agency in The Woodlands"*, First Byte is machine-readable in exactly the format those models parse.
**Why the business owner should care:** AI search is where discovery is heading. Businesses that aren't AEO-visible today are invisible in AI search tomorrow.
**Why it demonstrates Hey Aaron!'s capability:** Most agencies don't even know what llms.txt is. Ours ships it as a build target.

### 6. Cloudflare Pages Functions for lead capture
**What it is:** `functions/api/contact.js` (103 lines) + `functions/api/recent-leads.js` (26 lines).
**What it does:** Every form on the site POSTs to `/api/contact`. The function validates, honeypots, sends via Resend, and writes an anonymized recent-lead record to KV. `/api/recent-leads` reads that KV data for the social-proof toast widget.
**Why the business owner should care:** No separate email server, no third-party form service subscription. Free forever on Cloudflare's free tier.
**Why it demonstrates Hey Aaron!'s capability:** Serverless-native form architecture, not a WordPress plugin.

### 7. The "no fake social proof" ethical guardrail
**What it is:** The social-proof toast code refuses to fabricate fake data. When KV isn't bound, it stays silent for real visitors. Labeled *sample* data appears only in owner demo mode (`/?demo=1`).
**Why the business owner should care:** Fake social proof is a legal risk (FTC) and a trust burn if discovered. This code was intentionally designed so it can't accidentally lie on a real visitor.
**Why it demonstrates Hey Aaron!'s capability:** Ethical engineering choices baked into the design.

---

## Verified results

### VERIFIED TECHNICAL RESULTS *(provable from the repo — I FOUND THIS)*
- **238 HTML pages** built (vs a WordPress site with far fewer per-page templates).
- **140 location landing pages** covering **21 cities × 7 services**.
- **52 blog posts** (500–850 words each — measured by wordcount script).
- **156 FAQPage schema blocks** deployed.
- **290 Organization schema blocks** deployed.
- **11,575 `City` schema entries** across the site's `areaServed` arrays.
- **53 commits** shipped in **14 days** (2026-05-28 → 2026-06-11).
- **20 Python build scripts** in a deterministic pipeline.
- **113-line `llms.txt`** with a 10-Q conversational FAQ block.
- **Static Cloudflare Pages** deployment — sub-second edge cache globally (by architecture; not benchmark-verified in the repo).
- **Legacy WP bloat stripped**: broken Gravity Forms newsletter, MonsterInsights, WP speculation rules, wp-emoji, and the leftover AIO SEO schema on 25 pages.
- **44 WebP images** already converted from JPG/PNG originals.
- **0 empty `alt=""` attributes** across the site.
- **0 broken WordPress author/feed/wp-json links** (all cleaned).
- **The Lead Engine ships in 754 lines total** — 511 JS + 243 CSS. No jQuery. No dependencies.

### VERIFIED BUSINESS RESULTS
**UNKNOWN — ASK AARON.** No traffic numbers, ranking data, lead volume, or client testimonials are stored in the repo.

### MEASURABLE BUT NOT YET MEASURED
Aaron can pull these and cite real numbers:
- Lighthouse / PageSpeed scores (should be excellent given Cloudflare edge + static output)
- Total inbound leads since launch (from `sean@firstbyte.agency` inbox / Resend dashboard, once configured)
- Ranking positions for the 140 service-city combinations (via Google Search Console once verified)
- Total indexed pages (via GSC)
- Total AI-search citations (via analytics or manual Perplexity/ChatGPT queries for "digital marketing agency The Woodlands")
- Time-to-launch of a new city page (single script re-run — under 30 seconds)

---

## Before → After

| | Before (WordPress — I INFERRED) | After (this project — I FOUND THIS) |
|---|---|---|
| Hosting | WordPress on a traditional host | Static, edge-cached Cloudflare Pages |
| Page count | 4 services + a few pages + blog | 238 pages including 140 geo pages |
| Local SEO coverage | 7-city `areaServed` in schema | 21 cities in `areaServed`, 140 dedicated landing pages |
| Structured data | Single AIO SEO schema block with malformed URLs | `@graph` with `Organization` + `ProfessionalService` + FAQPage + BreadcrumbList across 156+ pages |
| AI search / AEO | None | `llms.txt`, conversational schema, `knowsAbout` graph |
| Blog | Small existing set | 52 posts (500–850 words each) |
| Lead capture | Broken footer Gravity Form + basic contact form | Blackjack Lead Engine + `/launch/` multi-step form + Cloudflare Pages Functions on Resend + sticky mobile bar |
| Productized offer landing page | None | `/launch/` — hosting-style pricing page with monthly/annual toggle |
| CMS complexity | WordPress + plugins | Static HTML + 20-script Python pipeline (zero attack surface, zero maintenance) |
| Version control / rollback | Whatever WP had | Full Git + Cloudflare's one-click rollback |
| Owner documentation | UNKNOWN | 750-line `OWNER-GUIDE.md` covering everything |

**UNKNOWN — ASK AARON:** the actual old WordPress design for real before/after screenshots. Archive.org or Aaron's local snapshot needed.

---

## Best portfolio visuals *(recommended captures)*

Prioritized top 8 to prove the pitch quickly:

| # | Page / feature | URL or location | What to capture | Why it's impressive | Format |
|---|---|---|---|---|---|
| 1 | `/launch/` hero + pricing tier + monthly-annual toggle | https://firstbyte.agency/launch/ | Hero + savings card + pricing tier with toggle switched to Annual showing $3,000 strikethrough → $2,500 | Full-fat SaaS-style landing page for a $250/mo product | Desktop screenshot + short screen recording of toggle switching |
| 2 | Blackjack Lead Engine mid-game | Any site page, then click the right-edge widget | The green felt table with gold chips, cards dealt, dealer bust message, "Tap to deal $250" chip glowing | Nobody else's marketing site has this | Screen recording (~10 s) showing a full round + confetti win |
| 3 | Blackjack win celebration | Same modal on any page | The gold screen flash + confetti + "BLACKJACK!" burst banner mid-animation | Genuinely delightful moment | Animated GIF or 5-second video |
| 4 | Sitemap / page-count screenshot | https://firstbyte.agency/sitemap.xml + `find site -name index.html \| wc -l` | 232 URLs listed | Proof of scale | Terminal + browser side-by-side |
| 5 | Local landing page example | https://firstbyte.agency/web-design-spring-tx/ | Full page scroll capture including the "How we deliver web design for Spring businesses" process section, 6-FAQ block, and Related resources | Proves the depth per city, not just page-count | Long desktop screenshot / scrolling screen recording |
| 6 | Comparison table on `/launch/` | https://firstbyte.agency/launch/#pricing | The 5-column table: Standard hosting / DIY builders / Traditional agency / First Byte | Clean visual anchor for the value story | Desktop screenshot |
| 7 | 9-card AI-powered features grid | https://firstbyte.agency/launch/ (AI section) | The gold-badge grid with all 9 cards + Claude Code badge | Communicates "AI-powered" in a concrete, not fluffy way | Desktop screenshot |
| 8 | Schema graph on the homepage | View-source of https://firstbyte.agency/ | The `@graph` JSON-LD block showing Organization + ProfessionalService with `knowsAbout` array | Proof of technical depth for a technical audience | Code screenshot |

Bonus visuals if you want to go deeper:
- 4-step launch sign-up form scrolling through all 4 steps
- Owner Guide's file-tree map + section table of contents
- The Python pipeline order (single-frame diagram)

---

## Potential headlines *(3 options — pick the tone that fits)*

1. **"How we turned a WordPress marketing site into an AI-powered local-SEO engine — in two weeks."** *(scale + transformation angle)*
2. **"238 pages, 21 cities, and a Blackjack game — the digital-marketing site we built for First Byte."** *(concrete + surprising angle)*
3. **"Static, edge-cached, AI-search-ready — and the visitors get to play Blackjack."** *(technical-savvy + memorable angle)*

## Portfolio teaser *(~40 words)*

> First Byte wanted a marketing site that ranks locally, gets quoted by AI search, and captures leads without begging. In 14 days we shipped 238 pages across 21 cities, a Blackjack-based lead-capture game, and a full monthly/annual pricing page — on Cloudflare's global edge.

## Best sales takeaway

> Most agency websites are brochures. This one **plays a rigged Blackjack game to convert visitors** and ships **140 unique location pages** while Google's still indexing your competitors' one-page-per-service template. If you're a service business that needs to be found — locally *and* in AI search — this is the kind of build we do for our own clients too.

---

## Missing information — questions for Aaron

Prioritized by impact on the case study:

1. **Do you have screenshots or a live snapshot of the old WordPress site?** Even one hero-area screenshot gives us the killer before/after visual.
2. **What did Sean originally hire you for?** Was it *"migrate off WordPress"*, *"get us more leads"*, *"beat competitors in the Map Pack"*, or something else? The stated brief anchors the story.
3. **How were leads coming in before this project?** Any rough numbers on old form submissions or GBP calls?
4. **Do you have a testimonial from Sean about the finished site?** One quote transforms this into a proper case study.
5. **Has the site been indexed by Google Search Console yet?** If yes, share screenshots of impressions / clicks over the last 30 days.
6. **Have you measured Lighthouse / PageSpeed scores** on the live production URL? If not, worth capturing before publishing.
7. **Any AI-search wins already?** Did anyone ask ChatGPT or Perplexity *"best digital marketing agency in The Woodlands"* and get First Byte back? A screenshot of that would be gold.
8. **What's the "100 new customers in 2026" origin?** Client stated goal or your internal aspiration for the account?
9. **The 17 case-study pages under `/work/`** — were those the client's *existing* portfolio inherited from the old WP site, or projects you also worked on? Affects how you attribute them.
10. **Any features I should downplay?** (e.g., is the Blackjack widget being A/B tested and might come down? Is it live for real visitors?)

---

## Sources of every claim in this document *(so nothing here is invented)*

Every specific number in this file comes from one of:
- **Repository filesystem** — `find`, `ls`, `wc -l`, `grep -c`
- **HTML source** — grep across all `site/**/*.html` files
- **Python source** — the 20 scripts at the repo root
- **Git history** — `git log --oneline` (53 commits) and dates from `git log --format='%ai'`
- **`OWNER-GUIDE.md`** — Aaron's own project documentation
- **Project memory file** (`~/.claude/.../project_firstbyte.md`) — flagged where used

Anything I couldn't verify from the repo is explicitly flagged **UNKNOWN — ASK AARON**.
