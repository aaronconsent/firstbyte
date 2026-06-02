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
    ("🎨", "Custom-designed website",
     "Built from scratch for your business — not a template. Mobile-first, fast, conversion-focused.",
     "$5,000 value"),
    ("⚡", "Hosting, SSL & daily backups",
     "Lightning-fast Cloudflare hosting, free SSL, automated backups, 99.9% uptime monitoring.",
     "$540/yr value"),
    ("🔍", "Monthly local SEO",
     "Google Business Profile optimization, citations, on-page SEO, and local ranking work — every month.",
     "$800/mo value"),
    ("✍️", "Content updates",
     "Up to 2 page edits or content updates per month — fresh photos, new offers, holiday hours, you name it.",
     "$300/mo value"),
    ("📊", "Monthly performance report",
     "Plain-English report on rankings, traffic, leads, and what we did to move the needle.",
     "$200/mo value"),
    ("📞", "Real humans on call",
     "Text, call, or email your local team in The Woodlands when you need a change — same-day response.",
     "Priceless"),
]

SPEND_IDEAS = [
    ("📢", "Local paid ads", "Google Ads or Facebook campaigns to fill the funnel while SEO ramps up."),
    ("🚚", "Branded vehicle wrap", "A rolling billboard your prospects see every day — typically $2,500–4,000."),
    ("📸", "Professional photography", "Real photos of your team, work, and location convert better than stock."),
    ("🪧", "Signage & print", "Storefront signage, business cards, brochures, vehicle magnets."),
    ("📦", "Inventory or equipment", "Reinvest in the tools that grow your bottom line."),
    ("👥", "Hiring help", "Free up your time so you can run the business, not the website."),
]

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
     "Most launches go live in 2–3 weeks from signup. Faster if you have logos, photos, and copy ready; a bit longer if we need to gather everything from scratch."),
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

/* Compare table */
.lp-compare{max-width:780px;margin:0 auto;background:#141215;border:1px solid rgba(255,255,255,.08);border-radius:1.1rem;overflow:hidden;}
.lp-comparerow{display:grid;grid-template-columns:1.4fr 1fr 1fr;border-top:1px solid rgba(255,255,255,.07);}
.lp-comparerow:first-child{border-top:0;background:rgba(255,255,255,.03);}
.lp-comparerow>div{padding:.9rem 1rem;color:hsla(0,0%,100%,.85);font-size:.92rem;line-height:1.4;}
.lp-comparerow .label{color:hsla(0,0%,100%,.65);font-weight:600;}
.lp-comparerow .vs{color:#ff8e8e;}
.lp-comparerow .us{color:#01f6f2;font-weight:700;border-left:1px solid rgba(35,255,244,.25);}
.lp-comparerow.head>div{font-family:"Funnel Display",sans-serif;font-weight:700;color:#fff;font-size:.95rem;}

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
.lp-field input,.lp-field select,.lp-field textarea{width:100%;box-sizing:border-box;background:#0f0d10;
  border:1px solid rgba(255,255,255,.14);border-radius:.6rem;padding:.78rem .95rem;color:#fff;font-family:inherit;font-size:.98rem;}
.lp-field input:focus,.lp-field select:focus,.lp-field textarea:focus{outline:none;border-color:#01f6f2;}
.lp-field textarea{min-height:90px;resize:vertical;}
.lp-row2{display:grid;gap:1rem;grid-template-columns:1fr 1fr;}
@media(max-width:520px){.lp-row2{grid-template-columns:1fr;}}
.lp-radios{display:grid;gap:.55rem;}
.lp-radios label{display:flex;align-items:center;gap:.7rem;cursor:pointer;background:#0f0d10;border:1px solid rgba(255,255,255,.12);
  border-radius:.6rem;padding:.75rem .9rem;color:#fff;font-size:.95rem;transition:.15s;}
.lp-radios label:hover{border-color:rgba(35,255,244,.4);}
.lp-radios input{appearance:none;-webkit-appearance:none;width:18px;height:18px;border-radius:50%;border:2px solid rgba(255,255,255,.4);
  flex:0 0 auto;margin:0;background:#0f0d10;cursor:pointer;position:relative;}
.lp-radios input:checked{border-color:#01f6f2;}
.lp-radios input:checked::after{content:"";position:absolute;inset:3px;border-radius:50%;background:#01f6f2;}
.lp-radios label:has(input:checked){border-color:#01f6f2;background:rgba(1,246,242,.06);}
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
        f'<h3>{tu.esc(name)}</h3><p>{tu.esc(desc)}</p>'
        f'<span class="val">{tu.esc(val)}</span></div>'
        for (ico, name, desc, val) in VALUE_STACK
    )
    return (
        '<section class="lp-section" id="whats-included"><div class="fb-wrap">'
        '<div class="lp-head">'
        '<h2>Everything you need to launch + grow — <span class="accent">for $250/month</span></h2>'
        '<p>Most agencies charge $5,000 up front and then go silent. We build, host, and actively market your site every month, for one flat price.</p>'
        '</div>'
        f'<div class="lp-stack">{items}</div>'
        '<p class="lp-stack-total">Total monthly value: <b>$1,800+</b> &nbsp;·&nbsp; '
        'You pay: <span class="you">$250/month</span></p>'
        '</div></section>'
    )


def section_compare():
    rows = [
        ("Up-front website cost", "$5,000+", "$0"),
        ("Monthly cost", "$0–250 (just hosting)", "$250 all-in"),
        ("Local SEO included", "No — extra $800+/mo", "Yes"),
        ("Hosting + SSL + backups", "Sometimes", "Yes"),
        ("Monthly content updates", "Billed hourly", "Included (up to 2/mo)"),
        ("Real reporting", "Rare", "Monthly"),
        ("Who answers when you call?", "Sales rep, then a queue", "Your local team"),
    ]
    headcells = '<div class="lp-comparerow head"><div></div><div>Typical agency</div><div>First Byte Launch</div></div>'
    body = "".join(
        f'<div class="lp-comparerow"><div class="label">{tu.esc(l)}</div>'
        f'<div class="vs">{tu.esc(a)}</div><div class="us">{tu.esc(b)}</div></div>'
        for (l, a, b) in rows
    )
    return (
        '<section class="lp-section"><div class="fb-wrap">'
        '<div class="lp-head"><h2>How this compares</h2>'
        '<p>Same launch. Same quality. Without the $5,000 up-front bite.</p></div>'
        f'<div class="lp-compare">{headcells}{body}</div>'
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
        '<span class="lp-eyebrow">First Byte Launch · The Woodlands, TX</span>'
        '<h1>A custom website <span class="gold">for $0 up-front</span><br>'
        '+ monthly marketing — <span class="accent">$250/month flat.</span></h1>'
        '<p class="lp-lead">Save the <b style="color:#fff">$5,000</b> you\'d normally pay an agency to build your site. We design it, host it, '
        "and market it every single month — for one flat $250. No contracts past 12 months, no surprise bills.</p>"
        '<div class="lp-pricepill"><span class="amt">$250</span><span class="per">per month · all-in</span></div>'
        '<div class="lp-ctas">'
        '<a class="lp-ctaprimary" href="#claim">🚀 Claim my $5,000 savings →</a>'
        '<a class="lp-ctaghost" href="#whats-included">See what\'s included</a>'
        '</div>'
        '<p class="lp-microtrust">Limited launches each month · <b>The Woodlands</b> &amp; Greater Houston</p>'
        '</div></section>'
    )


def section_form():
    # Multi-step form posts to /api/contact (Resend) and packages all answers into the message body.
    return r"""
<section class="lp-section" id="claim"><div class="fb-wrap">
<div class="lp-head"><h2>Start your <span class="accent">$0-down</span> launch</h2>
<p>Three quick steps — about 60 seconds. We'll review and reach out the same business day.</p></div>

<div class="lp-formwrap">
  <div class="lp-formhead"><h3>Claim your launch spot</h3>
  <p>No payment now. We confirm the plan with you on a quick call.</p></div>

  <div class="lp-progress" aria-hidden="true"><i class="on" data-dot="0"></i><i data-dot="1"></i><i data-dot="2"></i></div>

  <form class="lp-form" id="lp-form" novalidate>
    <input class="lp-hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
    <input type="hidden" name="_source" value="Launch page ($250/mo)">

    <!-- Step 1: Business basics -->
    <div class="lp-step on" data-step="0">
      <h4>1. Tell us about your business</h4>
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
            <option>Live entertainment / events</option>
            <option>Other</option>
          </select></div>
        <div class="lp-field"><label for="lp-city">City you serve</label>
          <input id="lp-city" name="city" type="text" placeholder="The Woodlands, TX"></div>
      </div>
      <div class="lp-field"><label for="lp-existing">Existing website (if any)</label>
        <input id="lp-existing" name="existing" type="url" inputmode="url" placeholder="https:// — or leave blank if none"></div>
      <div class="lp-nav">
        <button type="button" class="next" data-next>Continue →</button>
      </div>
    </div>

    <!-- Step 2: Goals -->
    <div class="lp-step" data-step="1">
      <h4>2. What's the main goal for your new site?</h4>
      <div class="lp-radios">
        <label><input type="radio" name="goal" value="Get more leads & calls"> 📈 Get more leads &amp; calls</label>
        <label><input type="radio" name="goal" value="Modernize / rebrand"> 🎨 Modernize / rebrand</label>
        <label><input type="radio" name="goal" value="Launch a brand-new business"> 🆕 Launch a brand-new business</label>
        <label><input type="radio" name="goal" value="Rank higher on Google"> 🔍 Rank higher on Google</label>
        <label><input type="radio" name="goal" value="Not sure — recommend a plan"> 🤝 Not sure — recommend a plan</label>
      </div>
      <div class="lp-field" style="margin-top:1rem"><label for="lp-pages">Rough idea on pages? (optional)</label>
        <select id="lp-pages" name="pages">
          <option value="">Pick one…</option>
          <option>1–3 (simple)</option>
          <option>4–7 (standard)</option>
          <option>8–15 (multi-service)</option>
          <option>15+ (large)</option>
          <option>Not sure — you tell me</option>
        </select></div>
      <div class="lp-nav">
        <button type="button" class="back" data-back>← Back</button>
        <button type="button" class="next" data-next>Continue →</button>
      </div>
    </div>

    <!-- Step 3: Contact -->
    <div class="lp-step" data-step="2">
      <h4>3. Where should we reach you?</h4>
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
      <div class="lp-field"><label for="lp-notes">Anything else? (optional)</label>
        <textarea id="lp-notes" name="notes" rows="3" placeholder="Logo, branding, deadlines, ideas…"></textarea></div>
      <div class="lp-nav">
        <button type="button" class="back" data-back>← Back</button>
        <button type="submit" class="submit">🎁 Claim my $5,000 savings</button>
      </div>
    </div>

    <div class="lp-formmsg" role="status" aria-live="polite"></div>
  </form>
  <p class="lp-formfine">By submitting you agree to be contacted about your project. No spam. Cancel anytime after 12 months.</p>
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
    var f = steps[n].querySelector("input,select,textarea"); if (f) try { f.focus({preventScroll:true}); } catch (e) {}
    try { document.getElementById("claim").scrollIntoView({behavior:"smooth", block:"start"}); } catch (e) {}
  }
  function valid(n) {
    if (n === 0) {
      if (!form.business.value.trim()) { msg.className="lp-formmsg err"; msg.textContent="Please add your business name."; return false; }
    } else if (n === 2) {
      if (!form.name.value.trim()) { msg.className="lp-formmsg err"; msg.textContent="Please add your name."; return false; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email.value)) { msg.className="lp-formmsg err"; msg.textContent="Please add a valid email."; return false; }
    }
    return true;
  }
  form.querySelectorAll("[data-next]").forEach(function (b) { b.addEventListener("click", function () { if (valid(cur)) setStep(cur + 1); }); });
  form.querySelectorAll("[data-back]").forEach(function (b) { b.addEventListener("click", function () { setStep(cur - 1); }); });
  form.addEventListener("submit", function (e) {
    e.preventDefault(); if (!valid(2)) return;
    var btn = form.querySelector(".submit"); btn.disabled = true;
    msg.className = "lp-formmsg"; msg.textContent = "Sending…";
    var goal = (form.querySelector('input[name="goal"]:checked') || {}).value || "Not specified";
    var summary =
      "[Launch lead — $250/mo plan]\n" +
      "Business: " + form.business.value + "\n" +
      "Industry: " + (form.industry.value || "—") + "\n" +
      "City: " + (form.city.value || "—") + "\n" +
      "Existing site: " + (form.existing.value || "(none)") + "\n" +
      "Primary goal: " + goal + "\n" +
      "Pages: " + (form.pages.value || "—") + "\n" +
      "Best time: " + (form.besttime.value || "Any") + "\n" +
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
              '<h3 style="font-family:\'Funnel Display\',sans-serif;color:#fff;font-size:1.7rem;margin:.4rem 0">You\'re on the list!</h3>' +
              '<p style="color:hsla(0,0%,100%,.75);margin:0 0 1.2rem;line-height:1.6">' +
                'We\'ll review your info and reach out the same business day. Want to skip the wait? ' +
                'Grab a time on the calendar now.' +
              '</p>' +
              '<a class="lp-ctaprimary" style="text-decoration:none;display:inline-block" ' +
                'href="https://calendly.com/firstbyte-agency/free-audit" target="_blank" rel="noopener">📅 Book your launch call</a>' +
            '</div>';
          try { window.dataLayer = window.dataLayer || []; window.dataLayer.push({event:"launch_lead_success"}); } catch (e) {}
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

<div class="lp-stickym"><a href="#claim">🚀 Claim my $5,000 savings</a></div>
"""


def build():
    inner = STYLE + '<div class="lp-pad-mobile">' + (
        section_hero()
        + section_savings()
        + section_value_stack()
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
