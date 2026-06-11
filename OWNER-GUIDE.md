# First Byte Site — Owner's Guide

This guide explains how your site is built, hosted, and updated. You don't need to read all of it — jump to the section you need.

> **TL;DR** — Your site lives at **firstbyte.agency**. It is a fast, static site hosted on **Cloudflare Pages**, deployed automatically from a **GitHub repository**. Any change you push to the `main` branch goes live in about a minute. You do **not** need WordPress anymore.

---

## Table of contents

1. [The big picture](#1-the-big-picture)
2. [The tech stack](#2-the-tech-stack)
3. [GitHub: where the site lives](#3-github-where-the-site-lives)
4. [Editing the site](#4-editing-the-site)
5. [Deploys (how a change goes live)](#5-deploys-how-a-change-goes-live)
6. [Cloudflare Pages — what to know](#6-cloudflare-pages--what-to-know)
7. [Forms & email (Resend + Cloudflare KV)](#7-forms--email-resend--cloudflare-kv)
8. [All JavaScript installed on the site](#8-all-javascript-installed-on-the-site)
9. [The Lead Engine (Blackjack widget, etc.)](#9-the-lead-engine-blackjack-widget-etc)
10. [The Python build pipeline](#10-the-python-build-pipeline)
11. [Common tasks (cheat sheet)](#11-common-tasks-cheat-sheet)
12. [Backups, rollbacks, and "oh no"](#12-backups-rollbacks-and-oh-no)
13. [Domains, DNS, and SSL](#13-domains-dns-and-ssl)
14. [Where to get help](#14-where-to-get-help)

---

## 1. The big picture

* **Public URL:** [firstbyte.agency](https://firstbyte.agency)
* **What it is:** A static website — every page is a pre-built HTML file. No database, no PHP, no plugins, no admin login to babysit.
* **Where the source lives:** GitHub — `github.com/aaronconsent/firstbyte`
* **Where it's hosted:** Cloudflare Pages, served from 300+ edge cities worldwide.
* **How updates work:** Edit on GitHub (or locally) → push to `main` branch → Cloudflare builds and deploys automatically.
* **WordPress status:** The original WordPress site is **frozen and no longer the source of truth**. All edits happen in this static repo.
* **Site size:** ~238 pages (home, services, geo pages, industries, blog, launch landing page, etc.).

---

## 2. The tech stack

| Layer | What it is | Where it lives |
|---|---|---|
| **Domain & DNS** | Registrar of record + DNS routing | Cloudflare DNS |
| **CDN + hosting** | Edge cache + SSL + DDoS protection | Cloudflare Pages |
| **Source code** | All files for the site | GitHub repo `aaronconsent/firstbyte` |
| **Frontend** | Plain HTML, CSS, vanilla JavaScript | `site/` folder in repo |
| **Build pipeline** | Python scripts that generate pages | Repo root (`*.py` files) |
| **Server-side functions** | `/api/contact`, `/api/recent-leads` | `functions/api/*.js` (Cloudflare Workers) |
| **Email send** | Transactional email | Resend (resend.com) |
| **Social proof storage** | Anonymized recent-lead names | Cloudflare KV (namespace `LEADS_KV`) |
| **Analytics (optional)** | Google Analytics 4 | Set `GA4_ID` in `enhance.py` |

Nothing is on a self-managed server. Nothing requires updates or security patches.

---

## 3. GitHub: where the site lives

### 3.1 The repository

* **URL:** [github.com/aaronconsent/firstbyte](https://github.com/aaronconsent/firstbyte)
* **Main branch:** `main` — every commit here triggers a production deploy on Cloudflare.

### 3.2 Getting access

If you're not already a collaborator on the repo, ask Aaron to add your GitHub username:
1. Create a free account at [github.com](https://github.com) if you don't have one.
2. Send Aaron your GitHub username.
3. He'll send you an invite from `github.com/aaronconsent/firstbyte/settings/access`. Click **Accept**.

You'll now have full read/write access via the GitHub web UI — no developer tools required for everyday edits.

### 3.3 Cloning the repo locally (optional, advanced)

If you want to edit on your own computer:

```bash
# Install git first if you don't have it: https://git-scm.com/downloads
git clone https://github.com/aaronconsent/firstbyte.git
cd firstbyte
```

You can then open files in any editor (VS Code is free and excellent). When you're ready to publish:

```bash
git add .
git commit -m "Update phone number on homepage"
git push origin main
```

That's it — Cloudflare picks it up automatically.

---

## 4. Editing the site

There are three ways to edit, listed easiest → most advanced.

### 4.1 Easy: edit one page on GitHub.com

Best for: small text changes, phone number, hours, swapping a paragraph.

1. Go to the repo on github.com.
2. Click **`site/`**, then drill down to the page you want to edit. Example: `site/contact/index.html` for the Contact page.
3. Click the pencil icon (✏️) in the top-right of the file view.
4. Edit the HTML directly in your browser.
5. Scroll down. Add a one-line commit message like *"Update phone in contact page"*.
6. Click **Commit changes**.
7. Wait ~1 minute. The change is live.

### 4.2 Moderate: regenerate sections via the Python build pipeline

If you want to rebuild **a lot of pages** at once (e.g., add a new city to the service-area matrix, change a phone number everywhere, add a blog post), use the Python scripts. See **[Section 10](#10-the-python-build-pipeline)** for the full pipeline.

You need Python 3 installed (Mac comes with it; Windows: [python.org](https://python.org/downloads)).

### 4.3 Advanced: full rebuild

Re-crawl the original WP site (if it ever comes back online) and regenerate everything from scratch:

```bash
python3 crawl.py
python3 rewrite.py
python3 enhance.py
python3 service_pages.py
python3 new_services.py
python3 geo_pages.py
python3 blog.py
python3 hubs.py
python3 industries.py
python3 homepage.py
python3 contact_form.py
python3 navigation.py
python3 cleanup.py
python3 alt_text.py
python3 webp.py
python3 cwv.py
python3 launch.py
python3 leadmode.py
python3 enhance.py        # final pass for sitemap + schema
```

Each script is idempotent — safe to re-run.

---

## 5. Deploys (how a change goes live)

```
You commit to main on GitHub
        ↓
Cloudflare Pages sees the push
        ↓
It runs the build (none needed — site/ is shipped as-is)
        ↓
Files copied to 300+ edge cities worldwide
        ↓
Live at firstbyte.agency (~30–60 seconds total)
```

You can watch the deploy in real-time:

* **Cloudflare dashboard** → Pages → `firstbyte` (or whatever the project is named) → Deployments.

If a deploy fails, the previous version stays live — your site never goes down because of a broken commit.

---

## 6. Cloudflare Pages — what to know

* **Dashboard:** [dash.cloudflare.com](https://dash.cloudflare.com) → Pages → your project.
* **Build settings:** Build command is empty. Build output directory is `site`. Source branch is `main`.
* **Custom domain:** `firstbyte.agency` is mapped under **Custom domains**. SSL is automatic.
* **Preview deployments:** Every commit to any branch other than `main` gets its own preview URL — useful for testing changes before merging.
* **Logs:** Each deployment has its own build log under **Deployments**.

---

## 7. Forms & email (Resend + Cloudflare KV)

### 7.1 Contact + Launch sign-up forms

Both forms POST to `/api/contact`, which is a small Cloudflare Pages Function (`functions/api/contact.js`). It uses **Resend** to send the email to **`sean@firstbyte.agency`**.

### 7.2 Required environment variables

These are set in Cloudflare, **not** in the code. Dashboard path:
**Cloudflare Pages → your project → Settings → Environment variables**.

| Variable | What it is | Where to get it |
|---|---|---|
| `RESEND_API_KEY` | API key from Resend (secret) | resend.com → API Keys |
| `CONTACT_TO` | Where to send leads | usually `sean@firstbyte.agency` |
| `CONTACT_FROM` | Verified sender address | something like `noreply@firstbyte.agency` (Resend must verify the domain) |

After adding/editing env vars, you must **trigger a redeploy** for them to take effect (just re-deploy the latest commit from the dashboard).

### 7.3 Resend setup

1. Sign in at [resend.com](https://resend.com).
2. Add `firstbyte.agency` as a verified sending domain (Resend will give you DNS records to add to Cloudflare DNS — paste them in).
3. Create an API key → paste it into `RESEND_API_KEY` in Cloudflare Pages env vars.
4. Test by submitting the Contact form on the live site.

### 7.4 Social-proof toasts (optional)

The Lead Engine can show real recent leads on the site (e.g. *"Mike R. in Conroe requested a free audit"*). For this to show real (not labeled-sample) data, you need:

1. In Cloudflare → Workers & Pages → KV → Create a namespace called `LEADS_KV`.
2. In your Pages project → Settings → Functions → KV bindings → bind it as `LEADS_KV`.
3. Redeploy.

Once bound, `contact.js` writes anonymized first-name+timestamp records to KV, and `recent-leads.js` reads them so the social-proof widget shows real recent activity. Without KV, the widget shows nothing (it does **not** fabricate fake data).

---

## 8. All JavaScript installed on the site

> "JavaScript" here means anything that runs in a visitor's browser **or** server-side on Cloudflare Workers.

### 8.1 Custom files we control

| File | Purpose | Notes |
|---|---|---|
| `site/assets/leadmode.js` | The **Lead Engine** — Blackjack tab, social-proof toasts, sticky mobile call bar, popup, multi-step lead form. | See **[Section 9](#9-the-lead-engine-blackjack-widget-etc)**. Loaded on every page. Versioned (`?v=15`) for cache busting. |
| Inline `<script>` in `site/launch/index.html` | Powers the Launch landing page: Monthly/Annual billing toggle, 4-step sign-up form, chip multi-selects, form submission to `/api/contact`. | Only on `/launch/`. |
| Inline `<script>` in `site/contact/index.html` | Contact form submit handler (POSTs to `/api/contact`). | Only on `/contact/`. |
| Inline JSON-LD scripts in every page | Structured data for SEO/AEO — `LocalBusiness`, `Service`, `FAQPage`, `BlogPosting`, `BreadcrumbList`, `Offer`, etc. | Not executable JS — data only. Read by Google, ChatGPT, Perplexity. |

### 8.2 Cloudflare Pages Functions (server-side, run on Workers)

| File | What it does |
|---|---|
| `functions/api/contact.js` | Receives form POSTs, validates fields, sends an email via Resend, writes an anonymized lead record to KV. |
| `functions/api/recent-leads.js` | Returns the last few anonymized leads from KV so the social-proof widget can display them. |

These run on Cloudflare's edge — no separate server. They're triggered by browser requests to `/api/contact` and `/api/recent-leads`.

### 8.3 Inherited WordPress theme scripts (still present on some pages)

When we migrated from WordPress, the original theme's HTML and assets were kept as the "shell" so the design stayed consistent. That shell still references some WordPress-era scripts on the homepage and `/work/*` case-study pages. They're harmless but bloat the page weight a bit. They can be removed in a future pass.

| Script | Purpose | Pages still using it |
|---|---|---|
| `jquery.min.js` (v3.7.1) | jQuery library — used by the theme's interactions. | Homepage + work pages |
| `foundation.min.js` (v6.8.1) | Foundation CSS framework's JS for menus / accordions. | Homepage + work pages |
| `global.js` | Custom theme JS — sliders, menu toggles. | Homepage + work pages |
| `slick.min.js` | Carousel/slider library. | Homepage + work pages |
| `jquery.fancybox.v3.js` | Lightbox for portfolio images. | Work pages |
| `select2.full.min.js` | Pretty styled select dropdowns. | Homepage (legacy form) |
| `lazyload.min.js` | Lazy-loads images. | Homepage + work pages |
| WordPress core JS bundles (`wp-includes/js/dist/*`) | Tiny utilities (i18n, hooks, dom-ready, a11y). | A few pages |
| `cloudflareinsights.com/beacon.min.js` | Cloudflare Web Analytics (anonymous, no cookies). | Site-wide |

### 8.4 What was already removed

The `cwv.py` script (Core Web Vitals cleanup) already stripped:

* The broken Gravity Forms newsletter from the footer site-wide
* Legacy MonsterInsights tracking
* WordPress speculation rules
* The wp-emoji styles + script

You can run `python3 cwv.py` again any time after content changes.

### 8.5 Analytics (optional)

There's a hook in `enhance.py` for **Google Analytics 4**. To enable it:

1. Edit `enhance.py`, find `GA4_ID = ""`, replace with your GA4 measurement ID (`G-XXXXXXXXXX`).
2. Run `python3 enhance.py`.
3. Commit + push.

GA4 will be injected site-wide. Until then, nothing is sent to Google.

---

## 9. The Lead Engine (Blackjack widget, etc.)

The Lead Engine is the right-edge **🃏 Win up to $2,500 / Play Blackjack →** widget you see on most pages. It's a single self-contained file (`site/assets/leadmode.js`) that ships these tactics:

* **Blackjack challenge** — a rigged-in-the-player's-favor blackjack game that ends in a lead-capture form. The player can win up to $2,500 in first-month account credit.
* **Sticky mobile call bar** — bottom of the screen on phones: 📞 Call now / ⚡ Free quote.
* **Social-proof toasts** — bottom-left toasts showing real recent leads (only when KV is configured; otherwise hidden).

### 9.1 Owner controls (URL-based)

| URL | Effect |
|---|---|
| `/?leads=off` | Turn the entire Lead Engine off in your browser (stored in localStorage). |
| `/?leads=on` | Turn it back on. |
| `/?demo=1` | Enable demo mode (used to show labeled sample data when KV isn't configured). |

These only affect *your* browser — visitors are not impacted by what you toggle.

### 9.2 Hidden on certain pages

The Blackjack widget is intentionally **hidden on `/launch/`** so it doesn't compete with the dedicated launch sign-up form.

### 9.3 Editing the Lead Engine

The whole engine lives in `site/assets/leadmode.js`. To change wording, default features, or game logic:

1. Edit `site/assets/leadmode.js` directly.
2. Bump the version in `leadmode.py` (e.g., change `?v=15` to `?v=16`).
3. Run `python3 leadmode.py` so every page re-references the new version (this avoids browser caches serving the old file).
4. Commit + push.

---

## 10. The Python build pipeline

Every page is generated by a Python script. Re-running a script regenerates its pages with the latest data — perfect for site-wide updates (change a phone number once, run the relevant script, commit, push, done).

| Script | What it builds | When to re-run |
|---|---|---|
| `crawl.py` | Mirrors the legacy WordPress site (frozen — rarely needed). | Only if you somehow need to re-pull the WP source. |
| `rewrite.py` | Cleans up the crawled WP HTML (fixes links, removes cruft). | After `crawl.py`. |
| `enhance.py` | Injects `LocalBusiness` schema, meta tags, robots.txt, sitemap.xml, llms.txt, GA4 (if set). | After any content change — always end the pipeline with this. |
| `service_pages.py` | Builds the 4 original service landing pages + area links. | When you change service copy. |
| `new_services.py` | Builds 3 new service pages (SEO, Paid Ads, PR). | When you change those. |
| `geo_pages.py` | Builds 7 services × 20 cities = 140 location pages. | When you add a city or a service. |
| `blog.py` + `blog_posts.py` | Builds the blog hub + 52 posts. | When you add or edit a post. |
| `hubs.py` | Builds `/services/` and `/service-areas/` hub pages. | When you add a service or area. |
| `industries.py` | Builds the 8 industry pages + hub. | When you change industry copy. |
| `homepage.py` | Injects an "Industries we serve" section into the homepage. | When you change industry list. |
| `contact_form.py` | Builds the `/contact/` page form. | When you change the contact page. |
| `navigation.py` | Site-wide header + footer nav. | When you add/remove a page from nav. |
| `cleanup.py` | Strips dead WordPress links (`/author/`, `/feed/`, `/wp-json/`). | After any rebuild. |
| `alt_text.py` | Fills empty `alt=""` attributes on images. | After adding new images. |
| `webp.py` | Converts JPG/PNG → WebP for performance. | After adding new images. |
| `cwv.py` | Strips legacy bloat (broken forms, MonsterInsights, speculation rules). | After any rebuild. |
| `launch.py` | Builds the `/launch/` landing page. | When you change Launch plan content. |
| `leadmode.py` | Injects the Lead Engine `<script>` tag into every page. | When you edit `leadmode.js` or bump its version. |
| `theme_ui.py` | Shared design system (not run directly — imported by others). | Edit when you want a global look-and-feel change. |

**Standard order** for a full rebuild (after content/code changes):

```
enhance → service_pages → new_services → geo_pages → blog → hubs →
industries → homepage → contact_form → navigation → cleanup →
alt_text → webp → cwv → launch → leadmode → enhance
```

You almost never need the full chain — for everyday edits, only run the one or two scripts that touch what you changed, then push.

---

## 11. Common tasks (cheat sheet)

### Change the phone number site-wide
1. Edit `theme_ui.py` — change `PHONE` and `PHONE_DISPLAY` near the top.
2. Edit `enhance.py` (same constants).
3. Re-run the relevant generators: `python3 enhance.py && python3 service_pages.py && python3 new_services.py && python3 geo_pages.py && python3 hubs.py && python3 launch.py && python3 contact_form.py`.
4. Commit + push.

### Add a new blog post
1. Open `blog_posts.py`.
2. Add a new entry to the `POSTS` list following the same format as existing posts.
3. Run `python3 blog.py && python3 enhance.py`.
4. Commit + push.

### Edit a single existing page (text change)
* Just edit the file in `site/...` directly on GitHub. Done.

### Add a new city to the service-area matrix
1. Open `geo_pages.py`, add the city to the `CITIES` dict.
2. Run `python3 geo_pages.py && python3 hubs.py && python3 navigation.py && python3 enhance.py`.
3. Commit + push.

### Change the Launch plan pricing or features
1. Edit `launch.py` (the `LAUNCH_PLAN` dict near the top).
2. Run `python3 launch.py`.
3. Commit + push.

### Change a hero headline or copy on the Launch page
1. Edit the relevant section function in `launch.py` (e.g., `section_hero()`).
2. Run `python3 launch.py`. Commit + push.

### Disable the Lead Engine site-wide
* You probably don't want to do this in code; instead use `/?leads=off` in your own browser. To kill it for everyone, edit `site/assets/leadmode.js` and change the default near the top: `var LEADS = stored === null ? true : stored === "on";` → set the default to `false`.

---

## 12. Backups, rollbacks, and "oh no"

* **Every change is in git history.** You can always view, diff, or revert any commit on GitHub.
* **Cloudflare keeps every deploy** — you can roll back to any previous version with one click in the Pages dashboard → Deployments → click the older deploy → **Rollback to this deployment**.
* **Daily/automatic backups** are not configured separately — the GitHub repo *is* the backup, and Cloudflare retains the last ~50 deploys.
* **If you delete something accidentally on GitHub**, you can recover it from a previous commit in the **Commits** history.

---

## 13. Domains, DNS, and SSL

* **Domain registrar:** Cloudflare (or whoever Aaron originally pointed it to).
* **DNS:** Cloudflare — managed in dash.cloudflare.com → DNS for the `firstbyte.agency` zone.
* **SSL:** Automatic and free, courtesy of Cloudflare. Never expires, never needs renewing.
* **Email DNS records:** When you set up Resend, you'll add a few `TXT` and `CNAME` records here for sending-domain verification (SPF, DKIM, DMARC).

---

## 14. Where to get help

* **Aaron Phillips** built and manages this site. Email or call him — he has full context on every script and decision.
* **Cloudflare Pages docs:** [developers.cloudflare.com/pages](https://developers.cloudflare.com/pages/)
* **GitHub docs:** [docs.github.com](https://docs.github.com/)
* **Resend docs:** [resend.com/docs](https://resend.com/docs)
* **For Python:** [python.org/about/gettingstarted/](https://www.python.org/about/gettingstarted/)

---

## Appendix: file/folder map

```
firstbyte/
├─ OWNER-GUIDE.md              ← (you are here)
├─ site/                       ← The actual website. This is what Cloudflare ships.
│  ├─ index.html               ← Homepage
│  ├─ contact/                 ← /contact/ page
│  ├─ launch/                  ← /launch/ landing page
│  ├─ services/                ← Services hub
│  ├─ service-areas/           ← Service areas hub
│  ├─ industries/              ← Industries hub + 8 industry pages
│  ├─ blog/                    ← Blog hub + 52 posts
│  ├─ assets/
│  │  └─ leadmode.{js,css}     ← The Lead Engine
│  ├─ {service}-{city}-tx/     ← 140 geo landing pages
│  ├─ work/                    ← Case study pages (legacy WP)
│  ├─ work_tax/                ← Service pages (legacy WP shell)
│  ├─ sitemap.xml              ← Auto-generated
│  ├─ robots.txt               ← Auto-generated
│  └─ llms.txt                 ← AI-engine-readable site summary
├─ functions/
│  └─ api/
│     ├─ contact.js            ← Lead-form receiver → Resend → KV
│     └─ recent-leads.js       ← Social-proof JSON endpoint
├─ *.py                        ← The build pipeline (see Section 10)
└─ README.md                   ← Project notes (technical)
```

---

*Last updated when this file was written. If something below contradicts a newer change, the code wins — Aaron can update this guide.*
