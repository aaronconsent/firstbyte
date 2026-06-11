#!/usr/bin/env python3
"""Build the $250/mo "Launch" landing page at /launch/.

Pitch: free custom website (no upfront cost) + monthly local SEO,
hosting and management for $250/month. Big "Save $5,000" hook,
ideas where to spend the savings, value stack, multi-step lead form
that POSTs to /api/contact (Resend) with a Launch-specific subject.

Idempotent. Run after enhance.py (needs the theme template). Re-run
enhance.py after to refresh sitemap + schema for the new URL.
"""
import json
import theme_ui as tu

BASE = tu.BASE
URL = BASE + "/launch/"

VALUE_STACK = [
    ("☁️", "Hosted on Cloudflare",
     "Enjoy lightning-fast loading worldwide, built-in protection from attacks, and uptime that rarely ever blinks."),
    ("📦", "Never run out of room",
     "Your storage grows as your site grows. There are no hard drives filling up and hitting your limit."),
    ("⚡", "Fast, even when it's busy",
     "When a crowd shows up, your site speeds up to handle them. No slowdowns, no \"upgrade your plan\" surprise."),
    ("📈", "Go viral, no penalty",
     "As many visitors as you can get, with no caps and no overage bills. Other hosts say \"unlimited,\" then throttle you."),
    ("🌍", "Fast everywhere on earth",
     "Your site is copied to 300+ cities, so every visitor loads it from the one nearest them. Local feel, worldwide."),
    ("🔒", "The padlock is always on",
     "That little lock in the address bar? It's free, automatic, and it never expires. Visitors trust you on day one."),
    ("↩️", "An easy undo button",
     "Every change is saved automatically. Something break? Roll back to how it looked yesterday in one click."),
    ("🛡️", "Keeps the bad guys out",
     "Attacks and junk bots get blocked before they ever reach your site — protection that's built in, not an add-on."),
    ("🚚", "We move you over for free",
     "Already have a site? We rebuild it cleaner and faster, then hand it back ready to go. You don't lift a finger."),
    ("🆙", "Ditch WordPress",
     "Tired of slow, clunky WordPress and endless plugin headaches? We move you onto a faster, modern setup — quickly, with none of the old baggage."),
    ("✉️", "Unlimited email forwards",
     "Set up as many addresses at your domain as you want — you@, info@, sales@, hello@ — all routed to the inboxes you already check. No new accounts to babysit."),
    ("🧱", "A site that won't fall apart",
     "Built as solid, modern code — not a stack of plugins that break, slow you down, or get hacked."),
]

SPEND_IDEAS = [
    ("📢", "Local paid ads", "Google Ads or Facebook campaigns to fill the funnel while SEO ramps up."),
    ("🚚", "Branded vehicle wrap", "A rolling billboard your prospects see every day — typically $2,500–4,000."),
    ("📸", "Professional photography", "Real photos of your team, work, and location convert better than stock."),
    ("🪧", "Signage & print", "Storefront signage, business cards, brochures, vehicle magnets."),
    ("📦", "Inventory or equipment", "Reinvest in the tools that grow your bottom line."),
    ("👥", "Hiring help", "Free up your time so you can run the business, not the website."),
]

# Launch plan — one plan, billed monthly ($250/mo) or annually ($2,500/yr, 2 months free).
LAUNCH_PLAN = {
    "name": "Launch",
    "tag": "The Launch Plan",
    "subtitle": "Custom website + monthly local SEO + AI-powered features — one flat price.",
    "monthly_price": 250,
    "annual_price": 2500,
    "annual_save_note": "2 months free vs monthly",
    "features": [
        "Custom-designed website — no up-front cost",
        "Premium Cloudflare hosting + SSL + daily backups",
        "Monthly local SEO (Google Business Profile, citations, on-page)",
        "Up to 2 content updates per month",
        "AI-assisted copywriting baked into the build",
        "Custom integrations available (CRM, calendar, booking, etc.)",
        "Monthly performance report (plain-English)",
        "Direct access to your local team",
        "Launch in 2–3 days",
    ],
}

# AI / Claude-Code-powered features — web-native, conversion-focused.
# Tuple: (icon, title, category, description, value-range badge)
AI_FEATURES = [
    ("🗺️", "Hyper-local landing pages", "Local SEO",
     "Unique, on-brand pages per neighborhood, zip, or service combo — original content, not spun, seasonally refreshed so they keep ranking.",
     "$4K value"),
    ("✍️", "Auto-blogging on autopilot", "Auto-blogging",
     "Weekly AI-drafted posts targeted at the keywords your customers actually search. Old posts auto-refreshed with new stats and fresh dates.",
     "$2K value"),
    ("💬", "AEO-optimized FAQ blocks", "AEO",
     "Question-and-answer blocks formatted the exact way ChatGPT, Perplexity, Gemini, and Claude search quote sources — with the structured data to back it up.",
     "$1K value"),
    ("📡", "AI-readable site structure", "AEO",
     "Proper llms.txt, conversational H2s, clean schema, and short citation-ready paragraphs so AI engines reliably surface and quote your business.",
     "$2K value"),
    ("📋", "Smart conversational quote forms", "Quote forms",
     "Multi-step forms where each question depends on the previous answer (residential vs commercial → totally different paths), with a ballpark range shown before submit.",
     "$1K value"),
    ("🧩", "Adaptive site widgets", "Widgets",
     "Quote CTAs, click-to-call bars, exit-intent offers, social-proof toasts, live Google-reviews carousel — all context-aware by page, device, and source.",
     "$1K value"),
    ("📣", "AI-ready OG images + RSS-ready pages", "Distribution",
     "Auto-generated on-brand social-share previews for every page (perfect in LinkedIn, Facebook, iMessage, Slack) plus proper RSS feeds so AI agents, aggregators, and readers can pull your content.",
     "$1K value"),
    ("🧪", "Always-on A/B testing", "Split tests",
     "Headlines, buttons, and offers automatically rotate against each other; the statistically-significant winner gets promoted — no manual setup.",
     "$2K value"),
    ("🎯", "Personalized hero variants by source", "Conversions",
     "Headline, image, and CTA swap based on where the visitor came from — Google ad → emergency-focused hero, Facebook → seasonal offer hero — no extra landing pages.",
     "$1K value"),
]

# Speed advantage — what AI-assisted dev unlocks.
SPEED_STATS = [
    ("🚀", "2–3 days", "From signup to live site"),
    ("⚡", "Days, not months", "New features and changes"),
    ("🧠", "Claude Code + AI", "Behind every build"),
    ("🔧", "Custom included", "Integrations & widgets"),
]

# 4-way comparison: standard hosting / DIY builders / traditional agency / us.
COMPARE = {
    "headers": [
        "",
        "Standard hosting<br><span class='sm'>GoDaddy, Bluehost</span>",
        "DIY builder<br><span class='sm'>Wix, Squarespace</span>",
        "Traditional agency",
        "First Byte Launch",
    ],
    "rows": [
        ("Up-front website cost", "Free template", "Free template", "$5,000+", "$0"),
        ("Monthly cost", "$10–40", "$25–60", "$0 hosting only", "$250 all-in"),
        ("Custom-designed site", "No — template", "No — template", "Yes (slow)", "Yes (fast)"),
        ("Typical launch time", "Hours (DIY)", "Hours (DIY)", "8–12 weeks", "2–3 days"),
        ("Local SEO", "DIY", "DIY", "Extra $800+/mo", "Included"),
        ("Hosting + SSL + backups", "Basic", "Basic", "Sometimes", "Premium (Cloudflare)"),
        ("Monthly content updates", "DIY", "DIY", "Billed hourly", "Included (up to 2/mo)"),
        ("AI features (chatbot, etc.)", "Plugins you DIY", "Limited apps", "Quoted per project", "Built-in"),
        ("Custom integrations", "Buy a plugin", "App marketplace", "$$$ per project", "Included"),
        ("New features", "Buy a plugin", "Wait for an app", "Quote + months", "Days"),
        ("Real reporting", "Basic analytics", "Basic analytics", "Rare", "Monthly"),
        ("Who answers when you call", "Overseas chat", "Help center", "Sales then queue", "Your local team"),
    ],
}

FAQS = [
    ("Is the website really free up-front?",
     "Yes. We design, build, and launch your website with zero upfront cost. You commit to the $250/month plan for 12 months. After that, you can keep going month-to-month or take the site with you — your choice."),
    ("Why $250/month? What's the catch?",
     "No catch. We make sustainable revenue from the monthly plan instead of a one-time payday, which means we're invested in your long-term results — not just shipping a site and disappearing. Most agencies charge $5,000 up front and then nothing happens; we flip that model."),
    ("What's included for $250/month?",
     "A fully custom website, premium hosting, daily backups, monthly local SEO, up to 2 content updates per month, monthly performance reporting, and direct access to a real local team. Effectively $1,800+/month of value for $250."),
    ("Do I own the website?",
     "Yes — after 12 months you own the design and content outright and can take the site to any host. We just ask for the first 12 months to recoup the build cost."),
    ("How long does it take to launch?",
     "Most launches go live in 2–3 days from signup. Faster if you have logos, photos, and copy ready; a bit longer if we need to gather everything from scratch. We build with Claude Code and modern AI tooling, which compresses what traditional agencies need weeks for down to days."),
    ("What does 'AI-powered' actually mean?",
     "Two things. First, we build faster using AI-assisted development (Claude Code), so custom features that would cost $10,000+ at a traditional agency can ship in days. Second, we install real AI tools on your site as needed — a chatbot trained on your business, lead scoring, auto-drafted review responses, AI-generated content, and custom integrations with whatever software you already use."),
    ("Monthly or annual — which should I pick?",
     "Annual saves you $500/year (two months free) and locks in your rate. Monthly gives you maximum flexibility and the same plan, same features. Either way, no payment is collected until your site is approved and ready to launch."),
    ("What if I already have a website?",
     "Even better — we can redesign and migrate it, often improving speed and SEO in the process. The $250/month plan still applies."),
    ("Can I cancel?",
     "After the initial 12 months, yes — cancel any time with 30 days' notice. During the first 12 months we ask you stick with us so we can recoup the website build."),
    ("Where are you based?",
     "The Woodlands, TX. We serve businesses across Greater Houston — Spring, Conroe, Montgomery, Tomball, Magnolia, Katy, Sugar Land, Pearland and more."),
]


STYLE = """<style>
/* Launch landing page — scoped to .lp- */
.lp-hero{padding:5.5rem 0 2.5rem;position:relative;overflow:hidden;text-align:center;}
.lp-hero::before{content:"";position:absolute;left:50%;top:-10%;width:54rem;height:54rem;transform:translateX(-50%);
  background:radial-gradient(closest-side,rgba(1,246,242,.20),rgba(0,84,255,.10) 45%,rgba(190,0,187,.06) 70%,transparent 75%);
  filter:blur(8px);pointer-events:none;z-index:0;}
.lp-hero>*{position:relative;z-index:1;}
.lp-eyebrow{display:inline-block;padding:.5rem 1.1rem;border:1px solid rgba(255,215,0,.5);border-radius:2rem;
  background:radial-gradient(circle at 50% 30%,rgba(255,224,138,.18),rgba(255,179,0,.05));
  color:#ffd24a;font-size:.72rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;margin-bottom:1.2rem;}
.lp-hero h1{font-family:"Funnel Display",sans-serif;color:#fff;font-weight:700;line-height:1.04;
  font-size:clamp(2.4rem,6vw,4.4rem);margin:0 0 1.1rem;}
.lp-hero h1 .accent{color:#01f6f2;}
.lp-hero h1 .gold{background:linear-gradient(90deg,#ffe08a,#ffc233 60%,#ff9d00);-webkit-background-clip:text;background-clip:text;color:transparent;}
.lp-lead{max-width:46rem;margin:0 auto 1.6rem;color:hsla(0,0%,100%,.78);font-size:1.18rem;line-height:1.65;}
.lp-pricepill{display:inline-flex;align-items:baseline;gap:.4rem;background:linear-gradient(135deg,#01f6f2,#00d4ff);
  color:#03282a;font-weight:800;padding:.55rem 1.1rem;border-radius:2rem;margin-bottom:1.8rem;box-shadow:0 10px 28px rgba(1,246,242,.28);}
.lp-pricepill .amt{font-size:1.3rem;font-family:"Funnel Display",sans-serif;line-height:1;}
.lp-pricepill .per{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;opacity:.8;}
.lp-ctas{display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap;margin-bottom:.8rem;}
.lp-ctaprimary{cursor:pointer;display:inline-block;text-decoration:none;font-weight:800;font-size:1.05rem;
  padding:1rem 1.6rem;border-radius:.8rem;border:0;background:linear-gradient(90deg,#01f6f2,#00d4ff);color:#03282a;
  box-shadow:0 14px 36px rgba(1,246,242,.35);transition:filter .15s,transform .1s;}
.lp-ctaprimary:hover{filter:brightness(1.05);}
.lp-ctaprimary:active{transform:scale(.98);}
.lp-ctaghost{display:inline-block;text-decoration:none;font-weight:700;font-size:1.02rem;
  padding:1rem 1.4rem;border-radius:.8rem;border:1px solid rgba(255,255,255,.18);color:#fff;}
.lp-ctaghost:hover{border-color:#01f6f2;color:#01f6f2;}
.lp-microtrust{color:hsla(0,0%,100%,.55);font-size:.83rem;}
.lp-microtrust b{color:#fff;}

/* Savings spotlight */
.lp-savings{padding:1.2rem 0 3.5rem;}
.lp-savecard{max-width:760px;margin:0 auto;background:radial-gradient(120% 90% at 50% 0,#1a8a55,#0d6b3e 55%,#083c24);
  border:1px solid rgba(255,215,0,.4);border-radius:1.4rem;padding:2.4rem 1.8rem;text-align:center;
  box-shadow:0 30px 80px rgba(0,0,0,.55),inset 0 0 60px rgba(0,0,0,.35);position:relative;overflow:hidden;}
.lp-savecard::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  background:repeating-linear-gradient(45deg,rgba(255,255,255,.03) 0 3px,transparent 3px 7px);}
.lp-savecard>*{position:relative;}
.lp-savecard .lbl{color:#ffe87a;font-size:.78rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.6rem;}
.lp-savecard .big{font-family:"Funnel Display",sans-serif;color:#fff;font-size:clamp(3.4rem,9vw,5.4rem);line-height:1;margin:0 0 .6rem;
  text-shadow:0 0 26px rgba(255,200,0,.55);}
.lp-savecard .big .dollar{color:#ffd24a;}
.lp-savecard p{color:#e7fff5;font-size:1.08rem;line-height:1.6;max-width:42rem;margin:0 auto;}
.lp-savecard p b{color:#fff;}

/* Generic sections */
.lp-section{padding:3.5rem 0;}
.lp-head{text-align:center;max-width:44rem;margin:0 auto 2.4rem;}
.lp-head h2{font-family:"Funnel Display",sans-serif;color:#fff;font-weight:700;font-size:clamp(1.9rem,4.2vw,2.9rem);line-height:1.1;margin:0 0 .8rem;}
.lp-head h2 .accent{color:#01f6f2;}
.lp-head p{color:hsla(0,0%,100%,.7);font-size:1.05rem;line-height:1.65;margin:0;}

/* Value stack */
.lp-stack{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(16.5rem,1fr));}
.lp-item{background:#171518;border:1px solid rgba(255,255,255,.08);border-radius:1rem;padding:1.5rem 1.3rem;
  position:relative;transition:transform .2s,border-color .2s,box-shadow .2s;}
.lp-item:hover{transform:translateY(-3px);border-color:rgba(35,255,244,.45);box-shadow:0 14px 36px rgba(1,246,242,.08);}
.lp-item .ic{font-size:1.7rem;margin-bottom:.7rem;display:block;}
.lp-item h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.15rem;margin:0 0 .45rem;}
.lp-item p{color:hsla(0,0%,100%,.7);font-size:.93rem;line-height:1.55;margin:0 0 .8rem;}
.lp-item .val{display:inline-block;font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;
  color:#01f6f2;background:rgba(1,246,242,.10);border:1px solid rgba(1,246,242,.3);border-radius:2rem;padding:.25rem .65rem;}
.lp-stack-total{margin-top:2rem;text-align:center;color:hsla(0,0%,100%,.7);font-size:1rem;}
.lp-stack-total b{color:#fff;font-weight:800;}
.lp-stack-total .you{color:#01f6f2;font-weight:800;}

/* Single Launch plan with billing toggle */
.lp-billbox{display:flex;flex-direction:column;align-items:center;max-width:460px;margin:0 auto;}
.lp-billtoggle{display:inline-flex;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.20);border-radius:2rem;padding:.32rem;gap:.25rem;margin-bottom:1.5rem;}
.lp-billtoggle button{background:transparent;border:0;color:hsla(0,0%,100%,.75);font-family:inherit;font-weight:700;font-size:.92rem;
  padding:.65rem 1.3rem;border-radius:2rem;cursor:pointer;transition:.18s;display:inline-flex;align-items:center;gap:.55rem;line-height:1;}
.lp-billtoggle button:hover{color:#fff;}
.lp-billtoggle button.on{background:linear-gradient(90deg,#01f6f2,#00d4ff);color:#03282a;box-shadow:0 6px 20px rgba(1,246,242,.35);}
.lp-billtoggle .save{font-size:.6rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;background:rgba(255,210,74,.20);color:#ffd24a;
  border:1px solid rgba(255,210,74,.4);padding:.22rem .5rem;border-radius:2rem;line-height:1;}
.lp-billtoggle button.on .save{background:rgba(3,40,42,.20);color:#03282a;border-color:rgba(3,40,42,.35);}
/* Toggle drives which price/save text is visible */
.lp-billbox[data-bill="monthly"] [data-annual]{display:none;}
.lp-billbox[data-bill="annual"] [data-monthly]{display:none;}
.lp-tier{position:relative;display:flex;flex-direction:column;width:100%;background:#171518;border:1px solid rgba(255,255,255,.10);
  border-radius:1.1rem;padding:2.3rem 1.9rem 1.8rem;transition:transform .2s,border-color .2s,box-shadow .2s;}
.lp-tier:hover{transform:translateY(-4px);border-color:rgba(35,255,244,.35);box-shadow:0 18px 50px rgba(0,0,0,.45);}
.lp-tier.featured{border:2px solid #01f6f2;background:linear-gradient(180deg,#1c1a21,#15131a);box-shadow:0 28px 70px rgba(1,246,242,.22);}
.lp-tier-price .strike{display:block;color:hsla(0,0%,100%,.45);font-size:1rem;text-decoration:line-through;margin-bottom:.2rem;line-height:1;}
.lp-tier-fine{margin:.9rem 0 0;text-align:center;color:hsla(0,0%,100%,.55);font-size:.78rem;line-height:1.45;}
.lp-tier-fine b{color:#fff;}
.lp-tier-tag{position:absolute;top:-.85rem;left:50%;transform:translateX(-50%);background:linear-gradient(90deg,#01f6f2,#00d4ff);
  color:#03282a;font-size:.66rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;
  padding:.4rem .9rem;border-radius:2rem;box-shadow:0 6px 20px rgba(1,246,242,.5);white-space:nowrap;}
.lp-tier h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.6rem;margin:0 0 .35rem;}
.lp-tier .sub{color:hsla(0,0%,100%,.65);font-size:.92rem;line-height:1.45;margin:0 0 1.3rem;min-height:2.7rem;}
.lp-tier-price{display:flex;align-items:baseline;gap:.35rem;margin-bottom:.3rem;}
.lp-tier-price .amt{font-family:"Funnel Display",sans-serif;color:#fff;font-size:2.7rem;line-height:1;}
.lp-tier-price .per{color:hsla(0,0%,100%,.6);font-size:.92rem;}
.lp-tier-save{color:#01f6f2;font-size:.84rem;font-weight:700;margin-bottom:1.4rem;display:block;}
.lp-tier ul{list-style:none;padding:0;margin:0 0 1.5rem;display:grid;gap:.6rem;}
.lp-tier li{position:relative;padding-left:1.7rem;color:hsla(0,0%,100%,.85);font-size:.92rem;line-height:1.5;}
.lp-tier li::before{content:"";position:absolute;left:0;top:.1rem;width:1.15rem;height:1.15rem;border-radius:50%;background:rgba(1,246,242,.16);}
.lp-tier li::after{content:"";position:absolute;left:.42rem;top:.3rem;width:.28rem;height:.58rem;border:solid #01f6f2;border-width:0 2px 2px 0;transform:rotate(45deg);}
.lp-tier-cta{margin-top:auto;display:block;text-align:center;text-decoration:none;font-weight:800;font-size:1rem;
  padding:.95rem;border-radius:.7rem;background:rgba(255,255,255,.05);color:#fff;border:1.5px solid rgba(255,255,255,.20);transition:.15s;cursor:pointer;}
.lp-tier-cta:hover{border-color:#01f6f2;color:#01f6f2;}
.lp-tier.featured .lp-tier-cta{background:linear-gradient(90deg,#01f6f2,#00d4ff);color:#03282a;border:0;box-shadow:0 12px 30px rgba(1,246,242,.35);}
.lp-tier.featured .lp-tier-cta:hover{filter:brightness(1.06);color:#03282a;}
.lp-tier-foot{text-align:center;color:hsla(0,0%,100%,.55);font-size:.86rem;margin-top:1.6rem;}
.lp-tier-foot b{color:#fff;}

/* AI / Claude-Code-powered features grid */
.lp-aibadge{display:inline-flex;align-items:center;gap:.4rem;font-size:.66rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;
  color:#ffd24a;background:rgba(255,210,74,.10);border:1px solid rgba(255,210,74,.45);border-radius:2rem;padding:.35rem .85rem;margin-bottom:1rem;}
.lp-ai{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));}
.lp-aicard{background:linear-gradient(180deg,#1a181d,#141215);border:1px solid rgba(255,255,255,.08);
  border-radius:1rem;padding:1.6rem 1.4rem;position:relative;overflow:hidden;transition:.2s;}
.lp-aicard:hover{border-color:rgba(35,255,244,.4);box-shadow:0 14px 36px rgba(1,246,242,.06);}
.lp-aicard::before{content:"";position:absolute;top:0;right:0;width:9rem;height:9rem;
  background:radial-gradient(closest-side,rgba(1,246,242,.13),transparent);transform:translate(2rem,-3rem);pointer-events:none;}
.lp-aicard>*{position:relative;}
.lp-aicard{display:flex;flex-direction:column;}
.lp-aicard .ic{font-size:1.85rem;margin-bottom:.55rem;display:block;}
.lp-aicard .cat{display:inline-block;align-self:flex-start;font-size:.6rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;
  color:#23fff4;background:rgba(35,255,244,.10);border:1px solid rgba(35,255,244,.35);border-radius:2rem;padding:.25rem .65rem;margin-bottom:.65rem;line-height:1;}
.lp-aicard h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.15rem;margin:0 0 .5rem;}
.lp-aicard p{color:hsla(0,0%,100%,.78);font-size:.92rem;line-height:1.55;margin:0;}
.lp-aicard p{margin-bottom:1.1rem;}
.lp-aicard .aival{display:inline-flex;align-self:flex-start;align-items:center;gap:.35rem;
  margin-top:auto;padding:.45rem .85rem;border-radius:2rem;line-height:1;
  font-size:.72rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;
  color:#ffd24a;background:rgba(255,210,74,.10);border:1.5px solid rgba(255,210,74,.45);}

/* Speed advantage stat row */
.lp-speed{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(12rem,1fr));margin-top:.5rem;max-width:1000px;margin-left:auto;margin-right:auto;}
.lp-stat{text-align:center;padding:1.5rem 1.1rem 1.4rem;background:#171518;border:1px solid rgba(255,255,255,.08);border-radius:1rem;transition:.2s;}
.lp-stat:hover{border-color:rgba(35,255,244,.35);}
.lp-stat .ic{font-size:1.9rem;margin-bottom:.55rem;}
.lp-stat .num{font-family:"Funnel Display",sans-serif;color:#01f6f2;font-size:1.55rem;line-height:1.1;margin-bottom:.3rem;}
.lp-stat .lbl{color:hsla(0,0%,100%,.65);font-size:.86rem;line-height:1.4;}

/* Compare table — 5 columns now (label + 4 contenders) */
.lp-compare{max-width:1080px;margin:0 auto;background:#141215;border:1px solid rgba(255,255,255,.08);border-radius:1.1rem;overflow:hidden;}
.lp-comparewrap{overflow-x:auto;}
.lp-comparerow{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr 1fr;border-top:1px solid rgba(255,255,255,.07);min-width:780px;}
.lp-comparerow:first-child{border-top:0;background:rgba(255,255,255,.03);}
.lp-comparerow>div{padding:.85rem .95rem;color:hsla(0,0%,100%,.85);font-size:.9rem;line-height:1.4;}
.lp-comparerow .label{color:hsla(0,0%,100%,.65);font-weight:600;}
.lp-comparerow .vs{color:#ff9e9e;}
.lp-comparerow .us{color:#01f6f2;font-weight:700;border-left:1px solid rgba(35,255,244,.30);background:rgba(1,246,242,.04);}
.lp-comparerow.head>div{font-family:"Funnel Display",sans-serif;font-weight:700;color:#fff;font-size:.9rem;line-height:1.25;}
.lp-comparerow.head .sm{display:block;color:hsla(0,0%,100%,.45);font-weight:500;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;margin-top:.2rem;}

/* Where to spend */
.lp-ideas{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(15.5rem,1fr));}
.lp-idea{background:linear-gradient(180deg,#1b181c,#141215);border:1px solid rgba(255,255,255,.08);border-radius:1rem;
  padding:1.4rem 1.3rem;display:flex;gap:1rem;align-items:flex-start;}
.lp-idea .ic{font-size:1.6rem;flex:0 0 auto;}
.lp-idea h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.05rem;margin:0 0 .3rem;}
.lp-idea p{color:hsla(0,0%,100%,.65);font-size:.88rem;line-height:1.5;margin:0;}

/* Form */
.lp-formwrap{max-width:680px;margin:0 auto;background:#171518;border:1px solid rgba(35,255,244,.28);
  border-radius:1.3rem;padding:2.2rem 1.9rem 2rem;box-shadow:0 30px 80px rgba(0,0,0,.55);}
.lp-formhead{text-align:center;margin-bottom:1.4rem;}
.lp-formhead h3{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.6rem;margin:0 0 .35rem;}
.lp-formhead p{color:hsla(0,0%,100%,.65);font-size:.95rem;margin:0;}
.lp-progress{display:flex;gap:.4rem;margin-bottom:1.5rem;}
.lp-progress i{flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.10);transition:background .25s;}
.lp-progress i.on{background:#01f6f2;}
.lp-step{display:none;animation:lp-fade .3s;}
.lp-step.on{display:block;}
@keyframes lp-fade{from{opacity:0;transform:translateX(8px);}to{opacity:1;transform:none;}}
.lp-step h4{font-family:"Funnel Display",sans-serif;color:#fff;font-size:1.1rem;margin:0 0 1.1rem;}
.lp-field{margin-bottom:1rem;}
.lp-field label{display:block;color:hsla(0,0%,100%,.82);font-size:.85rem;margin-bottom:.4rem;font-weight:600;}
.lp-field input,.lp-field select,.lp-field textarea{width:100%;box-sizing:border-box;background:rgba(255,255,255,.07);
  border:1.5px solid rgba(255,255,255,.25);border-radius:.6rem;padding:.85rem 1rem;color:#fff;font-family:inherit;font-size:1rem;
  transition:border-color .15s,background .15s,box-shadow .15s;line-height:1.3;}
.lp-field input::placeholder,.lp-field textarea::placeholder{color:hsla(0,0%,100%,.55);}
.lp-field input:hover,.lp-field select:hover,.lp-field textarea:hover{border-color:rgba(35,255,244,.45);background:rgba(255,255,255,.09);}
.lp-field input:focus,.lp-field select:focus,.lp-field textarea:focus{outline:none;border-color:#01f6f2;background:rgba(1,246,242,.07);box-shadow:0 0 0 3px rgba(1,246,242,.20);}
.lp-field select{appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'><path d='M1 1l5 5 5-5' stroke='%2301f6f2' stroke-width='2' fill='none'/></svg>");background-repeat:no-repeat;background-position:right 1rem center;padding-right:2.5rem;}
.lp-field select option{background:#171518;color:#fff;}
.lp-field textarea{min-height:92px;resize:vertical;}
.lp-field .hint{display:block;color:hsla(0,0%,100%,.55);font-size:.78rem;font-weight:400;margin-top:.4rem;font-style:italic;}
.lp-row2{display:grid;gap:1rem;grid-template-columns:1fr 1fr;}
@media(max-width:520px){.lp-row2{grid-template-columns:1fr;}}
.lp-radios{display:grid;gap:.55rem;}
.lp-radios label{display:flex;align-items:center;gap:.7rem;cursor:pointer;background:rgba(255,255,255,.05);
  border:1.5px solid rgba(255,255,255,.20);border-radius:.6rem;padding:.85rem 1rem;color:#fff;font-size:.98rem;transition:.15s;}
.lp-radios label:hover{border-color:rgba(35,255,244,.5);background:rgba(255,255,255,.08);}
.lp-radios input{appearance:none;-webkit-appearance:none;width:20px;height:20px;border-radius:50%;border:2px solid rgba(255,255,255,.5);
  flex:0 0 auto;margin:0;background:rgba(255,255,255,.06);cursor:pointer;position:relative;}
.lp-radios input:checked{border-color:#01f6f2;}
.lp-radios input:checked::after{content:"";position:absolute;inset:3px;border-radius:50%;background:#01f6f2;}
.lp-radios label:has(input:checked){border-color:#01f6f2;background:rgba(1,246,242,.10);}
/* Multi-select chips (pages / features) */
.lp-chips{display:flex;flex-wrap:wrap;gap:.55rem;}
.lp-chip{cursor:pointer;display:inline-flex;align-items:center;gap:.5rem;background:rgba(255,255,255,.06);
  border:1.5px solid rgba(255,255,255,.22);border-radius:2rem;padding:.55rem 1rem;color:#fff;font-size:.9rem;font-family:inherit;
  transition:.15s;line-height:1;}
.lp-chip:hover{border-color:rgba(35,255,244,.5);background:rgba(255,255,255,.09);}
.lp-chip .ck{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:50%;
  border:1.5px solid hsla(0,0%,100%,.55);background:transparent;font-size:.7rem;line-height:1;color:transparent;flex:0 0 auto;}
.lp-chip.on{border-color:#01f6f2;background:rgba(1,246,242,.15);color:#01f6f2;font-weight:700;}
.lp-chip.on .ck{background:#01f6f2;border-color:#01f6f2;color:#03282a;}
.lp-chip.on .ck::after{content:"✓";font-weight:900;font-size:.72rem;}
/* No-CC trust strip + section note */
.lp-trust{display:flex;flex-wrap:wrap;gap:.55rem;justify-content:center;margin-bottom:1.5rem;}
.lp-trust>div{display:inline-flex;align-items:center;gap:.4rem;background:rgba(1,246,242,.10);
  border:1px solid rgba(1,246,242,.35);border-radius:2rem;padding:.42rem .85rem;color:#fff;font-size:.78rem;font-weight:600;}
.lp-trust>div span{font-size:.95rem;line-height:1;}
.lp-secnote{color:hsla(0,0%,100%,.72);font-size:.86rem;text-align:center;margin:.2rem 0 1rem;line-height:1.45;
  background:rgba(1,246,242,.06);border:1px solid rgba(1,246,242,.22);border-radius:.6rem;padding:.7rem .9rem;}
.lp-secnote b{color:#01f6f2;}
.lp-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden;}
.lp-nav{display:flex;justify-content:space-between;gap:.7rem;margin-top:1.2rem;}
.lp-nav button{cursor:pointer;font-family:inherit;font-weight:700;font-size:.98rem;padding:.85rem 1.3rem;border-radius:.7rem;border:0;}
.lp-nav .back{background:transparent;border:1px solid rgba(255,255,255,.18);color:#fff;}
.lp-nav .back:hover{border-color:#01f6f2;color:#01f6f2;}
.lp-nav .next,.lp-nav .submit{background:linear-gradient(90deg,#01f6f2,#00d4ff);color:#03282a;flex:1;
  box-shadow:0 10px 28px rgba(1,246,242,.30);}
.lp-nav .next:disabled,.lp-nav .submit:disabled{opacity:.5;cursor:default;}
.lp-formmsg{margin-top:.9rem;font-size:.9rem;min-height:1.1rem;text-align:center;}
.lp-formmsg.err{color:#ff7a7a;}
.lp-formmsg.ok{color:#01f6f2;}
.lp-formfine{margin-top:1.1rem;text-align:center;color:hsla(0,0%,100%,.5);font-size:.78rem;}

/* Sticky mobile CTA */
.lp-stickym{display:none;position:fixed;left:0;right:0;bottom:0;z-index:1500;padding:.7rem 1rem;
  background:rgba(15,13,16,.92);backdrop-filter:blur(6px);border-top:1px solid rgba(35,255,244,.25);}
.lp-stickym a{display:block;text-align:center;text-decoration:none;font-weight:800;font-size:.98rem;
  padding:.85rem;border-radius:.7rem;background:linear-gradient(90deg,#01f6f2,#00d4ff);color:#03282a;}
@media(max-width:640px){.lp-stickym{display:block;} .lp-pad-mobile{padding-bottom:6rem;}}
</style>"""


def section_value_stack():
    items = "".join(
        f'<div class="lp-item"><span class="ic">{ico}</span>'
        f'<h3>{tu.esc(name)}</h3><p>{tu.esc(desc)}</p></div>'
        for (ico, name, desc) in VALUE_STACK
    )
    return (
        '<section class="lp-section" id="whats-included"><div class="fb-wrap">'
        '<div class="lp-head">'
        '<h2>Hosting and infrastructure — <span class="accent">built to scale with you</span></h2>'
        '<p>The same foundational tech the biggest sites in the world use, baked into every Launch plan. Most agencies bolt these on as separate paid add-ons; we just include them.</p>'
        '</div>'
        f'<div class="lp-stack">{items}</div>'
        '</div></section>'
    )


def section_compare():
    head = '<div class="lp-comparerow head">' + "".join(
        f'<div>{h}</div>' for h in COMPARE["headers"]
    ) + "</div>"
    body = ""
    for row in COMPARE["rows"]:
        label = row[0]
        cells = row[1:]
        cell_html = "".join(
            f'<div class="us">{tu.esc(c)}</div>' if i == len(cells) - 1
            else f'<div class="vs">{tu.esc(c)}</div>'
            for i, c in enumerate(cells)
        )
        body += f'<div class="lp-comparerow"><div class="label">{tu.esc(label)}</div>{cell_html}</div>'
    return (
        '<section class="lp-section"><div class="fb-wrap">'
        '<div class="lp-head"><h2>How we compare — <span class="accent">across the board</span></h2>'
        "<p>Standard hosting is cheap but you build it. DIY builders lock you in. Traditional agencies bill $5,000 up front. We do all of it — for $250/month.</p></div>"
        f'<div class="lp-compare"><div class="lp-comparewrap">{head}{body}</div></div>'
        '</div></section>'
    )


def section_tiers():
    p = LAUNCH_PLAN
    feats = "".join(f"<li>{tu.esc(f)}</li>" for f in p["features"])
    monthly_total = p["monthly_price"] * 12
    save_amt = monthly_total - p["annual_price"]
    card = (
        '<div class="lp-billbox" data-bill="monthly">'
        '<div class="lp-billtoggle" role="tablist" aria-label="Billing period">'
        '  <button type="button" data-bill="monthly" class="on" role="tab" aria-selected="true">Monthly</button>'
        '  <button type="button" data-bill="annual" role="tab" aria-selected="false">'
        f'    Annual <span class="save">2 months free</span>'
        '  </button>'
        '</div>'
        '<div class="lp-tier featured">'
        f'<span class="lp-tier-tag">{tu.esc(p["tag"])}</span>'
        f'<h3>{tu.esc(p["name"])}</h3>'
        f'<p class="sub">{tu.esc(p["subtitle"])}</p>'
        '<div class="lp-tier-price" data-monthly>'
        f'<span class="amt">${p["monthly_price"]}</span><span class="per">/mo</span>'
        '</div>'
        '<div class="lp-tier-price" data-annual>'
        f'<span class="strike">${monthly_total:,}</span>'
        f'<span class="amt">${p["annual_price"]:,}</span><span class="per">/yr</span>'
        '</div>'
        '<span class="lp-tier-save" data-monthly>Save $5,000 up-front · billed monthly</span>'
        f'<span class="lp-tier-save" data-annual>Save $5,000 up-front + <b>${save_amt} a year</b> ({tu.esc(p["annual_save_note"])})</span>'
        f"<ul>{feats}</ul>"
        '<a class="lp-tier-cta" href="#claim">Start my sign-up →</a>'
        '<p class="lp-tier-fine">No credit card now. You only pay once your site is approved and ready to go live.</p>'
        '</div>'
        '</div>'
    )
    js = r"""<script>
(function () {
  var box = document.querySelector(".lp-billbox"); if (!box) return;
  box.querySelectorAll(".lp-billtoggle [data-bill]").forEach(function (b) {
    b.addEventListener("click", function () {
      var mode = b.dataset.bill;
      box.setAttribute("data-bill", mode);
      box.querySelectorAll(".lp-billtoggle [data-bill]").forEach(function (x) {
        var on = x.dataset.bill === mode;
        x.classList.toggle("on", on); x.setAttribute("aria-selected", on ? "true" : "false");
      });
    });
  });
})();
</script>"""
    return (
        '<section class="lp-section" id="pricing"><div class="fb-wrap">'
        '<div class="lp-head">'
        '<h2>One simple plan — <span class="accent">monthly or annual</span></h2>'
        '<p>Choose how you pay. Annual is the same plan, with two months on the house.</p>'
        '</div>'
        f'{card}{js}'
        '</div></section>'
    )


def section_ai():
    cards = "".join(
        f'<div class="lp-aicard"><span class="ic">{ico}</span>'
        f'<span class="cat">{tu.esc(cat)}</span>'
        f'<h3>{tu.esc(name)}</h3><p>{tu.esc(desc)}</p>'
        f'<span class="aival">💰 {tu.esc(val)}</span></div>'
        for (ico, name, cat, desc, val) in AI_FEATURES
    )
    return (
        '<section class="lp-section"><div class="fb-wrap">'
        '<div class="lp-head">'
        '<span class="lp-aibadge">🤖 AI-Powered · Built with Claude Code</span>'
        '<h2>9 things we can now do that <span class="accent">used to be impossible</span></h2>'
        "<p>Built with Claude Code and modern AI tooling, the Launch plan ships features that would've cost thousands to build by hand — and weren't even on the menu at most small-business sites a year ago.</p>"
        '</div>'
        f'<div class="lp-ai">{cards}</div>'
        '</div></section>'
    )


def section_speed():
    stats = "".join(
        f'<div class="lp-stat"><div class="ic">{ico}</div>'
        f'<div class="num">{tu.esc(num)}</div>'
        f'<div class="lbl">{tu.esc(lbl)}</div></div>'
        for (ico, num, lbl) in SPEED_STATS
    )
    return (
        '<section class="lp-section"><div class="fb-wrap">'
        '<div class="lp-head">'
        '<h2>Built in <span class="accent">days, not months</span></h2>'
        '<p>Traditional agencies spend 2–3 months on a custom site. We use AI-assisted development to compress that to weeks — and ship new features whenever you ask.</p>'
        '</div>'
        f'<div class="lp-speed">{stats}</div>'
        '</div></section>'
    )


def section_savings():
    return (
        '<section class="lp-section lp-savings"><div class="fb-wrap">'
        '<div class="lp-savecard">'
        '<div class="lbl">Your up-front savings</div>'
        '<div class="big"><span class="dollar">$</span>5,000</div>'
        "<p>That's the average cost of a custom small-business website — money that usually leaves your account "
        '<b>before you book a single new customer</b>. With Launch, that $5,000 stays in your business, where it can actually grow it.</p>'
        '</div></div></section>'
    )


def section_spend():
    items = "".join(
        f'<div class="lp-idea"><span class="ic">{ico}</span>'
        f'<div><h3>{tu.esc(name)}</h3><p>{tu.esc(desc)}</p></div></div>'
        for (ico, name, desc) in SPEND_IDEAS
    )
    return (
        '<section class="lp-section"><div class="fb-wrap">'
        '<div class="lp-head">'
        '<h2>Where smart owners put the <span class="accent">$5,000 they saved</span></h2>'
        '<p>The website pays you back when people see it. These are the moves that get more eyeballs on it — fast.</p>'
        '</div>'
        f'<div class="lp-ideas">{items}</div>'
        '</div></section>'
    )


def section_faqs():
    return (
        '<section class="lp-section"><div class="fb-wrap">'
        '<div class="lp-head"><h2>Common questions</h2></div>'
        f'{tu.faqlist(FAQS)}'
        '</div></section>'
    )


def section_hero():
    return (
        '<section class="lp-hero"><div class="fb-wrap">'
        '<span class="lp-eyebrow">🤖 AI-Powered · First Byte Launch · The Woodlands, TX</span>'
        '<h1>A custom website <span class="gold">for $0 up-front</span><br>'
        '+ monthly marketing — <span class="accent">$250/month flat.</span></h1>'
        '<p class="lp-lead">Save the <b style="color:#fff">$5,000</b> you\'d normally pay an agency to build your site. We design it, host it, '
        "and market it every single month — for one flat $250. No contracts past 12 months, no surprise bills.</p>"
        '<div class="lp-pricepill"><span class="amt">$250</span><span class="per">per month · all-in</span></div>'
        '<div class="lp-ctas">'
        '<a class="lp-ctaprimary" href="#claim">🚀 Claim my $5,000 savings →</a>'
        '<a class="lp-ctaghost" href="#pricing">See pricing</a>'
        '</div>'
        '<p class="lp-microtrust">Limited launches each month · <b>The Woodlands</b> &amp; Greater Houston</p>'
        '</div></section>'
    )


def section_form():
    # Comprehensive 4-step sign-up. POSTs to /api/contact (Resend) with a full
    # project brief packed into the message body so Sean can quote/start fast.
    return r"""
<section class="lp-section" id="claim"><div class="fb-wrap">
<div class="lp-head"><h2>Start your <span class="accent">$0-down</span> sign-up</h2>
<p>Tell us about your business and what you want — we'll reach out the same business day to confirm the plan.</p></div>

<div class="lp-formwrap">
  <div class="lp-formhead"><h3>Website sign-up</h3>
  <p>4 quick steps · about 2 minutes</p></div>

  <div class="lp-trust">
    <div><span>🪙</span> No credit card required</div>
    <div><span>✅</span> Pay only after you approve the site</div>
    <div><span>🚀</span> We launch on your green light</div>
  </div>

  <div class="lp-progress" aria-hidden="true"><i class="on"></i><i></i><i></i><i></i></div>

  <form class="lp-form" id="lp-form" novalidate>
    <input class="lp-hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
    <input type="hidden" name="_source" value="Launch sign-up ($250/mo)">

    <!-- Step 1: Your business -->
    <div class="lp-step on" data-step="0">
      <h4>1. Your business</h4>
      <div class="lp-field"><label for="lp-biz">Business name <span style="color:#ff8e8e">*</span></label>
        <input id="lp-biz" name="business" type="text" autocomplete="organization" placeholder="Acme Plumbing"></div>
      <div class="lp-row2">
        <div class="lp-field"><label for="lp-industry">Industry</label>
          <select id="lp-industry" name="industry">
            <option value="">Pick one…</option>
            <option>Home services (HVAC, plumbing, electrical, roofing…)</option>
            <option>Restaurant / Hospitality</option>
            <option>Retail / E-commerce</option>
            <option>Professional services (legal, accounting, consulting)</option>
            <option>Health &amp; wellness</option>
            <option>Real estate</option>
            <option>Automotive</option>
            <option>Beauty / Salon / Spa</option>
            <option>Construction / Contracting</option>
            <option>Live entertainment / Events</option>
            <option>Nonprofit</option>
            <option>Other</option>
          </select></div>
        <div class="lp-field"><label for="lp-years">Years in business</label>
          <select id="lp-years" name="years">
            <option value="">Pick one…</option>
            <option>Brand new / pre-launch</option>
            <option>Less than 1 year</option>
            <option>1–3 years</option>
            <option>4–10 years</option>
            <option>10+ years</option>
          </select></div>
      </div>
      <div class="lp-row2">
        <div class="lp-field"><label for="lp-city">City / service area</label>
          <input id="lp-city" name="city" type="text" placeholder="The Woodlands, TX"></div>
        <div class="lp-field"><label for="lp-existing">Existing website</label>
          <input id="lp-existing" name="existing" type="url" inputmode="url" placeholder="https:// — or leave blank"></div>
      </div>
      <div class="lp-field"><label for="lp-desc">In one line, what do you do? <span style="color:#ff8e8e">*</span></label>
        <input id="lp-desc" name="description" type="text" placeholder="e.g. 24/7 emergency HVAC repair in Spring &amp; The Woodlands">
        <span class="hint">This becomes your headline — we can polish it later.</span></div>
      <div class="lp-nav">
        <button type="button" class="next" data-next>Continue →</button>
      </div>
    </div>

    <!-- Step 2: Your website -->
    <div class="lp-step" data-step="1">
      <h4>2. What you want from the site</h4>
      <div class="lp-field"><label>Main goal</label>
        <div class="lp-radios">
          <label><input type="radio" name="goal" value="Get more leads & calls"> 📈 Get more leads &amp; calls</label>
          <label><input type="radio" name="goal" value="Modernize / rebrand"> 🎨 Modernize / rebrand</label>
          <label><input type="radio" name="goal" value="Launch a brand-new business"> 🆕 Launch a brand-new business</label>
          <label><input type="radio" name="goal" value="Rank higher on Google"> 🔍 Rank higher on Google</label>
          <label><input type="radio" name="goal" value="Sell online"> 🛒 Sell online</label>
          <label><input type="radio" name="goal" value="Not sure — recommend a plan"> 🤝 Not sure — recommend a plan</label>
        </div></div>
      <div class="lp-field"><label>Pages you'd like <span class="hint" style="display:inline">(tap any that apply)</span></label>
        <div class="lp-chips" data-chipgroup="pages">
          <button type="button" class="lp-chip" data-val="Home"><span class="ck"></span>Home</button>
          <button type="button" class="lp-chip" data-val="About"><span class="ck"></span>About</button>
          <button type="button" class="lp-chip" data-val="Services"><span class="ck"></span>Services</button>
          <button type="button" class="lp-chip" data-val="Pricing"><span class="ck"></span>Pricing</button>
          <button type="button" class="lp-chip" data-val="Contact"><span class="ck"></span>Contact</button>
          <button type="button" class="lp-chip" data-val="Blog"><span class="ck"></span>Blog</button>
          <button type="button" class="lp-chip" data-val="Portfolio"><span class="ck"></span>Portfolio</button>
          <button type="button" class="lp-chip" data-val="Testimonials"><span class="ck"></span>Testimonials</button>
          <button type="button" class="lp-chip" data-val="FAQ"><span class="ck"></span>FAQ</button>
          <button type="button" class="lp-chip" data-val="Team"><span class="ck"></span>Team</button>
          <button type="button" class="lp-chip" data-val="Gallery"><span class="ck"></span>Gallery</button>
        </div></div>
      <div class="lp-field"><label>Features you'd like</label>
        <div class="lp-chips" data-chipgroup="features">
          <button type="button" class="lp-chip" data-val="Online booking"><span class="ck"></span>Online booking</button>
          <button type="button" class="lp-chip" data-val="Contact form"><span class="ck"></span>Contact form</button>
          <button type="button" class="lp-chip" data-val="Photo gallery"><span class="ck"></span>Photo gallery</button>
          <button type="button" class="lp-chip" data-val="Blog / news"><span class="ck"></span>Blog / news</button>
          <button type="button" class="lp-chip" data-val="E-commerce / store"><span class="ck"></span>E-commerce / store</button>
          <button type="button" class="lp-chip" data-val="Customer login"><span class="ck"></span>Customer login</button>
          <button type="button" class="lp-chip" data-val="Maps & directions"><span class="ck"></span>Maps &amp; directions</button>
          <button type="button" class="lp-chip" data-val="Newsletter signup"><span class="ck"></span>Newsletter signup</button>
          <button type="button" class="lp-chip" data-val="Reviews widget"><span class="ck"></span>Reviews widget</button>
          <button type="button" class="lp-chip" data-val="Live chat"><span class="ck"></span>Live chat</button>
        </div></div>
      <div class="lp-field"><label for="lp-insp">Websites you like (inspiration)</label>
        <textarea id="lp-insp" name="inspiration" rows="2" placeholder="Paste a URL or two — or describe the vibe you want"></textarea></div>
      <div class="lp-nav">
        <button type="button" class="back" data-back>← Back</button>
        <button type="button" class="next" data-next>Continue →</button>
      </div>
    </div>

    <!-- Step 3: Your brand -->
    <div class="lp-step" data-step="2">
      <h4>3. Your brand</h4>
      <div class="lp-field"><label>Do you have a logo?</label>
        <div class="lp-radios">
          <label><input type="radio" name="logo" value="Yes — I'll send it"> ✅ Yes — I'll send it</label>
          <label><input type="radio" name="logo" value="No — please design one for me"> 🎨 No — please design one for me</label>
          <label><input type="radio" name="logo" value="Have one but want it refreshed"> ♻️ Have one but want it refreshed</label>
        </div></div>
      <div class="lp-row2">
        <div class="lp-field"><label for="lp-colors">Brand colors</label>
          <input id="lp-colors" name="colors" type="text" placeholder="e.g. navy + gold, or 'open to ideas'"></div>
        <div class="lp-field"><label for="lp-tag">Tagline (optional)</label>
          <input id="lp-tag" name="tagline" type="text" placeholder="Your one-liner / slogan"></div>
      </div>
      <div class="lp-field"><label for="lp-diff">What makes you different from competitors? (optional)</label>
        <textarea id="lp-diff" name="differentiator" rows="2" placeholder="Faster, family-owned, certified, 24/7, lifetime warranty…"></textarea></div>
      <div class="lp-nav">
        <button type="button" class="back" data-back>← Back</button>
        <button type="button" class="next" data-next>Continue →</button>
      </div>
    </div>

    <!-- Step 4: Contact + timeline -->
    <div class="lp-step" data-step="3">
      <h4>4. Where should we reach you?</h4>
      <p class="lp-secnote"><b>No payment now — no credit card required.</b> We only collect a card once you've approved your finished website and we're ready to launch it.</p>
      <div class="lp-row2">
        <div class="lp-field"><label for="lp-name">Your name <span style="color:#ff8e8e">*</span></label>
          <input id="lp-name" name="name" type="text" autocomplete="name" placeholder="Jane Smith"></div>
        <div class="lp-field"><label for="lp-email">Email <span style="color:#ff8e8e">*</span></label>
          <input id="lp-email" name="email" type="email" autocomplete="email" placeholder="you@business.com"></div>
      </div>
      <div class="lp-row2">
        <div class="lp-field"><label for="lp-phone">Best phone</label>
          <input id="lp-phone" name="phone" type="tel" autocomplete="tel" placeholder="(713) 555-0123"></div>
        <div class="lp-field"><label for="lp-time">Best time to call</label>
          <select id="lp-time" name="besttime">
            <option value="">Any time</option><option>Morning</option><option>Midday</option><option>Afternoon</option><option>Evening</option>
          </select></div>
      </div>
      <div class="lp-field"><label>Desired launch timeline</label>
        <div class="lp-radios">
          <label><input type="radio" name="timeline" value="ASAP"> 🚀 ASAP</label>
          <label><input type="radio" name="timeline" value="Within a week"> ⚡ Within a week</label>
          <label><input type="radio" name="timeline" value="1 month"> 📅 1 month</label>
          <label><input type="radio" name="timeline" value="2+ months"> 🕒 2+ months</label>
          <label><input type="radio" name="timeline" value="Flexible — your recommendation"> 🤷 Flexible — your recommendation</label>
        </div></div>
      <div class="lp-field"><label for="lp-notes">Anything else? (optional)</label>
        <textarea id="lp-notes" name="notes" rows="3" placeholder="Hours of operation, special offers, photos you have ready, deadlines, etc."></textarea></div>
      <div class="lp-nav">
        <button type="button" class="back" data-back>← Back</button>
        <button type="submit" class="submit">🚀 Send my sign-up</button>
      </div>
    </div>

    <div class="lp-formmsg" role="status" aria-live="polite"></div>
  </form>
  <p class="lp-formfine">No spam, no surprises. By submitting you agree to be contacted about your project. Cancel anytime after the initial 12-month launch term.</p>
</div>
</div></section>

<script>
(function () {
  var form = document.getElementById("lp-form"); if (!form) return;
  var steps = form.querySelectorAll(".lp-step"), dots = form.parentElement.querySelectorAll(".lp-progress i");
  var msg = form.querySelector(".lp-formmsg"), cur = 0;
  function setStep(n) {
    cur = n;
    steps.forEach(function (s, i) { s.classList.toggle("on", i === n); });
    dots.forEach(function (d, i) { d.classList.toggle("on", i <= n); });
    msg.textContent = ""; msg.className = "lp-formmsg";
    var f = steps[n].querySelector("input:not([type=radio]):not(.lp-hp),select,textarea"); if (f) try { f.focus({preventScroll:true}); } catch (e) {}
    try { document.getElementById("claim").scrollIntoView({behavior:"smooth", block:"start"}); } catch (e) {}
  }
  function valid(n) {
    if (n === 0) {
      if (!form.business.value.trim()) { msg.className="lp-formmsg err"; msg.textContent="Please add your business name."; return false; }
      if (!form.description.value.trim()) { msg.className="lp-formmsg err"; msg.textContent="A one-line description helps us get started."; return false; }
    } else if (n === 3) {
      if (!form.name.value.trim()) { msg.className="lp-formmsg err"; msg.textContent="Please add your name."; return false; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email.value)) { msg.className="lp-formmsg err"; msg.textContent="Please add a valid email."; return false; }
    }
    return true;
  }
  // Chip multi-select (pages + features)
  form.querySelectorAll(".lp-chips").forEach(function (group) {
    group.addEventListener("click", function (e) {
      var b = e.target.closest(".lp-chip"); if (!b || !group.contains(b)) return;
      b.classList.toggle("on"); b.setAttribute("aria-pressed", b.classList.contains("on") ? "true" : "false");
    });
  });
  function chipsOf(name) {
    return Array.from(form.querySelectorAll('[data-chipgroup="' + name + '"] .lp-chip.on')).map(function (b) { return b.dataset.val; }).join(", ") || "—";
  }
  form.querySelectorAll("[data-next]").forEach(function (b) { b.addEventListener("click", function () { if (valid(cur)) setStep(cur + 1); }); });
  form.querySelectorAll("[data-back]").forEach(function (b) { b.addEventListener("click", function () { setStep(cur - 1); }); });
  form.addEventListener("submit", function (e) {
    e.preventDefault(); if (!valid(3)) return;
    var btn = form.querySelector(".submit"); btn.disabled = true;
    msg.className = "lp-formmsg"; msg.textContent = "Sending…";
    var goal = (form.querySelector('input[name="goal"]:checked') || {}).value || "—";
    var logo = (form.querySelector('input[name="logo"]:checked') || {}).value || "—";
    var timeline = (form.querySelector('input[name="timeline"]:checked') || {}).value || "—";
    var summary =
      "[Launch sign-up — $250/mo plan]\n\n" +
      "— BUSINESS —\n" +
      "Name: " + form.business.value + "\n" +
      "Industry: " + (form.industry.value || "—") + "\n" +
      "Years in business: " + (form.years.value || "—") + "\n" +
      "City / service area: " + (form.city.value || "—") + "\n" +
      "Existing site: " + (form.existing.value || "(none)") + "\n" +
      "What they do: " + form.description.value + "\n\n" +
      "— WEBSITE —\n" +
      "Primary goal: " + goal + "\n" +
      "Pages wanted: " + chipsOf("pages") + "\n" +
      "Features wanted: " + chipsOf("features") + "\n" +
      "Inspiration: " + (form.inspiration.value || "—") + "\n\n" +
      "— BRAND —\n" +
      "Logo: " + logo + "\n" +
      "Colors: " + (form.colors.value || "—") + "\n" +
      "Tagline: " + (form.tagline.value || "—") + "\n" +
      "Differentiator: " + (form.differentiator.value || "—") + "\n\n" +
      "— CONTACT —\n" +
      "Best time: " + (form.besttime.value || "Any") + "\n" +
      "Launch timeline: " + timeline + "\n" +
      "Notes: " + (form.notes.value || "—");
    var fd = new FormData();
    fd.append("name", form.name.value);
    fd.append("email", form.email.value);
    fd.append("phone", form.phone.value);
    fd.append("company", form.company.value);
    fd.append("message", summary);
    fetch("/api/contact", { method: "POST", headers: { Accept: "application/json" }, body: fd })
      .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
      .then(function (d) {
        if (d.ok) {
          form.parentElement.innerHTML =
            '<div style="text-align:center;padding:1rem 0">' +
              '<div style="font-size:3rem">🎉</div>' +
              '<h3 style="font-family:\'Funnel Display\',sans-serif;color:#fff;font-size:1.7rem;margin:.4rem 0">You\'re signed up!</h3>' +
              '<p style="color:hsla(0,0%,100%,.78);margin:0 0 .6rem;line-height:1.6">' +
                'We\'ll review your sign-up and reach out the same business day to confirm your launch plan. ' +
                '<b style="color:#fff">You don\'t pay a thing until your site is approved and ready to go live.</b>' +
              '</p>' +
              '<p style="color:hsla(0,0%,100%,.55);margin:.4rem 0 1.2rem;font-size:.85rem">Want to skip the wait? Grab a time on the calendar now.</p>' +
              '<a class="lp-ctaprimary" style="text-decoration:none;display:inline-block" ' +
                'href="https://calendly.com/firstbyte-agency/free-audit" target="_blank" rel="noopener">📅 Book your launch call</a>' +
            '</div>';
          try { window.dataLayer = window.dataLayer || []; window.dataLayer.push({event:"launch_signup_success"}); } catch (e) {}
        } else {
          msg.className = "lp-formmsg err";
          msg.textContent = (d && d.error) ? d.error : "Something went wrong — please try again or call (713) 578-0634.";
          btn.disabled = false;
        }
      })
      .catch(function () {
        msg.className = "lp-formmsg err";
        msg.textContent = "Network error — please call (713) 578-0634.";
        btn.disabled = false;
      });
  });
})();
</script>

<div class="lp-stickym"><a href="#claim">🚀 Start my sign-up</a></div>
"""


def build():
    inner = STYLE + '<div class="lp-pad-mobile">' + (
        section_hero()
        + section_savings()
        + section_tiers()
        + section_value_stack()
        + section_ai()
        + section_speed()
        + section_compare()
        + section_spend()
        + section_faqs()
        + section_form()
    ) + "</div>"

    title = "Launch a custom website for $0 down — $250/mo all-in | First Byte"
    desc = ("Save $5,000 on your business website. First Byte Launch: a custom-designed site, premium hosting, "
            "and monthly local SEO + content updates for $250/month flat. Based in The Woodlands, TX.")
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Offer", "@id": URL + "#offer",
             "name": "First Byte Launch — custom website + monthly marketing",
             "url": URL,
             "description": desc,
             "price": "250.00", "priceCurrency": "USD",
             "priceSpecification": {"@type": "UnitPriceSpecification",
                                    "price": "250.00", "priceCurrency": "USD", "unitText": "MONTH"},
             "seller": {"@id": BASE + "/#localbusiness"}},
            {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Launch", "item": URL},
             ]},
            {"@type": "FAQPage", "@id": URL + "#faq", "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]},
        ],
    }
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + json.dumps(graph, separators=(",", ":")) + "</script>")
    page = tu.render(inner, title, URL, desc, schema)
    tu.write(["launch"], page)


def main():
    build()
    print("  built /launch/")


if __name__ == "__main__":
    main()
