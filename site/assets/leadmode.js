/* First Byte — Lead Engine (demo).
 * OFF by default. Nothing renders for normal visitors.
 * Activate the hidden demo control panel:   /?demo=1   (turn off: /?demo=0)
 * Force lead capture on/off directly:        /?leads=on  |  /?leads=off
 * Real submissions POST to /api/contact (Resend) -> reach the owner's inbox.
 */
(function () {
  "use strict";
  var qs = new URLSearchParams(location.search);
  if (qs.has("demo")) { qs.get("demo") === "0" ? localStorage.removeItem("fblm_demo") : localStorage.setItem("fblm_demo", "1"); }
  if (qs.has("leads")) { localStorage.setItem("fblm_leads", qs.get("leads") === "off" ? "off" : "on"); }

  var DEMO = localStorage.getItem("fblm_demo") === "1";
  var LEADS = localStorage.getItem("fblm_leads") === "on"; // OFF by default
  if (!DEMO && !LEADS) return; // normal visitors: do nothing

  var FEAT_DEFAULT = { hello: 1, fab: 1, mobile: 1, exit: 1, scroll: 1, social: 1, poker: 1 };
  var FEAT = Object.assign({}, FEAT_DEFAULT, JSON.parse(localStorage.getItem("fblm_feat") || "{}"));
  var PHONE = "+1-713-578-0634", PHONE_D = "(713) 578-0634";
  // Owner: replace with your real Calendly (or other) booking link.
  var CALENDLY = "https://calendly.com/firstbyte-agency/free-audit";
  var fired = {};

  function track(ev, data) { try { window.dataLayer = window.dataLayer || []; window.dataLayer.push(Object.assign({ event: "lead_engine_" + ev }, data || {})); } catch (e) {} }
  function el(html) { var d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; }
  function once(k) { if (fired[k]) return false; fired[k] = 1; return true; }

  /* ---------------- Modal (shared offer + multi-step form) ---------------- */
  var overlay;
  function monthEnd() { var n = new Date(); return new Date(n.getFullYear(), n.getMonth() + 1, 0, 23, 59, 59); }
  function buildModal() {
    if (overlay) return overlay;
    overlay = el('<div class="fblm-overlay" role="dialog" aria-modal="true"></div>');
    overlay.innerHTML =
      '<div class="fblm-modal">' +
      '<button class="fblm-close" aria-label="Close">&times;</button>' +
      '<span class="fblm-badge">Free • Limited this month</span>' +
      '<h2>Get your <span class="a">free 2026 growth plan</span></h2>' +
      '<p class="fblm-sub">A no-obligation website + local-SEO audit for your business — what\'s working, what\'s leaking leads, and the 3 fastest wins. ($500 value.)</p>' +
      '<div class="fblm-count" data-count></div>' +
      '<div class="fblm-pokerstage fblm-hidden fblm-poker">' +
        '<div class="fblm-row" data-dealer></div><div class="fblm-rowlabel">Dealer</div>' +
        '<div class="fblm-row" data-player></div><div class="fblm-rowlabel" data-holdhint>Your hand</div>' +
        '<button type="button" class="fblm-cta" data-deal>🃏 Deal me in</button>' +
        '<p class="fblm-spinresult fblm-hidden" style="margin:.9rem 0 0;font-size:1rem;line-height:1.5" data-pkresult></p>' +
      '</div>' +
      '<div class="fblm-steps"><i class="on"></i><i></i><i></i></div>' +
      '<form class="fblm-form" novalidate>' +
        '<input class="fblm-hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">' +
        '<input type="hidden" name="_goal" value="">' +
        '<div class="fblm-step on" data-step="0">' +
          '<div class="fblm-field"><label>What do you most want to fix?</label></div>' +
          '<div class="fblm-choices">' +
            '<button type="button" data-goal="Get more leads / calls">📈 Get more leads &amp; calls</button>' +
            '<button type="button" data-goal="New or rebuilt website">🎨 A new / better website</button>' +
            '<button type="button" data-goal="Rank higher on Google">🔍 Rank higher on Google</button>' +
            '<button type="button" data-goal="Not sure — need a plan">🤝 Not sure, I want a plan</button>' +
          '</div>' +
        '</div>' +
        '<div class="fblm-step" data-step="1">' +
          '<div class="fblm-field"><label>Your name</label><input name="name" autocomplete="name" placeholder="Jane Smith"></div>' +
          '<div class="fblm-field"><label>Email</label><input name="email" type="email" autocomplete="email" placeholder="you@business.com"></div>' +
          '<button type="button" class="fblm-cta" data-next>Continue &rarr;</button>' +
        '</div>' +
        '<div class="fblm-step" data-step="2">' +
          '<div class="fblm-field"><label>Best phone (for your free audit call)</label><input name="phone" type="tel" autocomplete="tel" placeholder="(713) 555-0123"></div>' +
          '<div class="fblm-field"><label>Anything we should know? (optional)</label><textarea name="message" rows="2" placeholder="Tell us about your business"></textarea></div>' +
          '<button type="submit" class="fblm-cta">🚀 Send me my free plan</button>' +
        '</div>' +
        '<div class="fblm-msg" role="status" aria-live="polite"></div>' +
      '</form>' +
      '<p class="fblm-fine">No spam, ever. Or call <a href="tel:' + PHONE + '">' + PHONE_D + '</a> now.</p>' +
      '</div>';
    document.body.appendChild(overlay);

    var form = overlay.querySelector(".fblm-form"), msg = overlay.querySelector(".fblm-msg");
    var steps = overlay.querySelectorAll(".fblm-step"), dots = overlay.querySelectorAll(".fblm-steps i");
    function goStep(n) { steps.forEach(function (s, i) { s.classList.toggle("on", i === n); }); dots.forEach(function (d, i) { d.classList.toggle("on", i <= n); }); }
    // Spin-to-win pre-stage (gamified). Everyone wins a genuinely offered prize.
    if (FEAT.poker) {
      var pkStage = overlay.querySelector(".fblm-pokerstage"),
          stepsBar = overlay.querySelector(".fblm-steps"), h2 = overlay.querySelector(".fblm-modal h2"),
          sub = overlay.querySelector(".fblm-sub"),
          dealerRow = overlay.querySelector("[data-dealer]"), playerRow = overlay.querySelector("[data-player]"),
          holdHint = overlay.querySelector("[data-holdhint]"), dealBtn = overlay.querySelector("[data-deal]"),
          pkResult = overlay.querySelector("[data-pkresult]");
      h2.innerHTML = 'Beat the dealer, <span class="a">win a prize</span> 🃏';
      sub.textContent = "Play one hand of 5-card draw. Every player wins a real prize — beat the dealer and it upgrades.";
      pkStage.classList.remove("fblm-hidden"); stepsBar.classList.add("fblm-hidden"); form.classList.add("fblm-hidden");

      var SUITS = ["♠", "♥", "♦", "♣"], RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
      // Real, deliverable prizes ordered low->high ($150–$500). Index by hand strength.
      var PRIZES = [
        { full: "Free 30-Minute Strategy Call", val: 150 },
        { full: "Free Brand Mini-Review", val: 200 },
        { full: "$250 off your first project", val: 250 },
        { full: "Free Google Business Profile Tune-Up", val: 300 },
        { full: "Free Competitor Analysis Report", val: 350 },
        { full: "Free Website Audit", val: 500 }
      ];
      var CAT2PRIZE = [0, 1, 2, 3, 4, 4, 5, 5, 5];
      var CATNAME = ["High Card", "a Pair", "Two Pair", "Three of a Kind", "a Straight", "a Flush", "a Full House", "Four of a Kind", "a Straight Flush"];

      function newDeck() { var d = []; for (var s = 0; s < 4; s++) for (var r = 2; r <= 14; r++) d.push({ s: s, r: r }); for (var i = d.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = d[i]; d[i] = d[j]; d[j] = t; } return d; }
      function cardEl(card, down) {
        var red = card.s === 1 || card.s === 2;
        return el('<div class="fblm-cardwrap"><div class="fblm-card' + (down ? " down" : "") + '">' +
          '<div class="face' + (red ? " red" : "") + '"><span>' + RANKS[card.r - 2] + '</span><span>' + SUITS[card.s] + '</span></div>' +
          '<div class="back"></div></div></div>');
      }
      function evalHand(cards) {
        var rs = cards.map(function (c) { return c.r; }).sort(function (a, b) { return b - a; });
        var cnt = {}; rs.forEach(function (r) { cnt[r] = (cnt[r] || 0) + 1; });
        var groups = Object.keys(cnt).map(function (r) { return { r: +r, c: cnt[r] }; }).sort(function (a, b) { return b.c - a.c || b.r - a.r; });
        var flush = cards.every(function (c) { return c.s === cards[0].s; });
        var uniq = rs.filter(function (v, i) { return rs.indexOf(v) === i; });
        var sHigh = 0;
        if (uniq.length === 5) { if (uniq[0] - uniq[4] === 4) sHigh = uniq[0]; else if (uniq[0] === 14 && uniq[1] === 5 && uniq[4] === 2) sHigh = 5; }
        var pat = groups.map(function (g) { return g.c; }).join(""), cat, score, gr = groups.map(function (g) { return g.r; });
        if (sHigh && flush) { cat = 8; score = [sHigh]; }
        else if (pat === "41") { cat = 7; score = gr; }
        else if (pat === "32") { cat = 6; score = gr; }
        else if (flush) { cat = 5; score = rs; }
        else if (sHigh) { cat = 4; score = [sHigh]; }
        else if (pat === "311") { cat = 3; score = gr; }
        else if (pat === "221") { cat = 2; score = gr; }
        else if (pat === "2111") { cat = 1; score = gr; }
        else { cat = 0; score = rs; }
        return { cat: cat, score: score };
      }
      function cmp(a, b) { if (a.cat !== b.cat) return a.cat - b.cat; for (var i = 0; i < 5; i++) { var x = a.score[i] || 0, y = b.score[i] || 0; if (x !== y) return x - y; } return 0; }

      var deck, player, dealer, held, phase = "predeal";
      function render(revealDealer) {
        dealerRow.innerHTML = ""; dealer.forEach(function (c) { dealerRow.appendChild(cardEl(c, !revealDealer)); });
        playerRow.innerHTML = "";
        player.forEach(function (c, idx) {
          var w = cardEl(c, false), card = w.querySelector(".fblm-card");
          if (held[idx]) card.classList.add("held");
          if (phase === "draw") { w.style.cursor = "pointer"; w.title = "Tap to hold"; w.addEventListener("click", function () { held[idx] = !held[idx]; card.classList.toggle("held"); }); }
          playerRow.appendChild(w);
        });
        Array.prototype.slice.call(overlay.querySelectorAll(".fblm-cardwrap")).forEach(function (w, i) { setTimeout(function () { w.classList.add("in"); }, 55 * i); });
      }
      dealBtn.addEventListener("click", function () {
        if (phase === "predeal") {
          deck = newDeck(); player = []; dealer = [];
          for (var i = 0; i < 5; i++) { player.push(deck.pop()); dealer.push(deck.pop()); }
          held = [false, false, false, false, false]; phase = "draw"; render(false);
          holdHint.textContent = "Tap cards to HOLD, then draw"; dealBtn.textContent = "🔄 Draw & reveal dealer"; track("poker_deal");
        } else if (phase === "draw") {
          phase = "done"; dealBtn.disabled = true;
          for (var k = 0; k < 5; k++) { if (!held[k]) player[k] = deck.pop(); }
          render(true); holdHint.textContent = "";
          var pe = evalHand(player), de = evalHand(dealer), c = cmp(pe, de), idx = CAT2PRIZE[pe.cat], won = c > 0;
          if (won) idx = Math.min(idx + 1, PRIZES.length - 1);
          var prize = PRIZES[idx];
          var verdict = c > 0 ? "You beat the dealer! 🎉" : (c < 0 ? "Dealer edged you — but you still win! 🎁" : "A tie — you still win! 🎁");
          track("poker_result", { player: pe.cat, dealer: de.cat, win: won, prize: prize.full, value: prize.val });
          pkResult.classList.remove("fblm-hidden");
          pkResult.innerHTML = 'You: <b>' + CATNAME[pe.cat] + '</b> &nbsp;·&nbsp; Dealer: <b>' + CATNAME[de.cat] + '</b><br>' + verdict +
            '<br>Prize: <b style="color:#01f6f2">' + prize.full + '</b> ($' + prize.val + ' value)' + (won ? ' <b>— upgraded!</b>' : '');
          form._goal.value = "Poker game prize: " + prize.full + " ($" + prize.val + " value)";
          setTimeout(function () {
            pkStage.classList.add("fblm-hidden"); stepsBar.classList.remove("fblm-hidden"); form.classList.remove("fblm-hidden");
            h2.innerHTML = 'Claim your <span class="a">' + prize.full + '</span> 🎁';
            sub.textContent = "Worth $" + prize.val + " — where should we send it?"; goStep(1);
          }, 2800);
        }
      });
    }
    overlay.querySelectorAll("[data-goal]").forEach(function (b) {
      b.addEventListener("click", function () { form._goal.value = b.dataset.goal; track("step", { step: 1, goal: b.dataset.goal }); goStep(1); });
    });
    overlay.querySelector("[data-next]").addEventListener("click", function () {
      if (!form.name.value.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email.value)) { msg.className = "fblm-msg err"; msg.textContent = "Please add your name and a valid email."; return; }
      msg.textContent = ""; track("step", { step: 2 }); goStep(2);
    });
    overlay.querySelector(".fblm-close").addEventListener("click", closeModal);
    overlay.addEventListener("click", function (e) { if (e.target === overlay) closeModal(); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]'); btn.disabled = true; msg.className = "fblm-msg"; msg.textContent = "Sending…";
      var fd = new FormData();
      fd.append("name", form.name.value); fd.append("email", form.email.value); fd.append("phone", form.phone.value); fd.append("company", form.company.value);
      fd.append("message", "[Lead Engine • " + (form._goal.value || "popup") + "] " + (form.message.value || ""));
      track("submit", { goal: form._goal.value });
      fetch("/api/contact", { method: "POST", headers: { Accept: "application/json" }, body: fd })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d.ok) {
            overlay.querySelector(".fblm-modal").innerHTML =
              '<button class="fblm-close" aria-label="Close">&times;</button>' +
              '<div style="text-align:center;padding:.5rem 0">' +
              '<div style="font-size:3rem">🎉</div>' +
              '<h2>You\'re in!</h2>' +
              '<p class="fblm-sub">Your free plan is reserved. <b style="color:#fff">Skip the wait</b> — grab a time on the calendar right now and we\'ll walk through it live.</p>' +
              '<a class="fblm-cta" style="display:inline-block;text-decoration:none;max-width:300px" href="' + CALENDLY + '" target="_blank" rel="noopener" data-book>📅 Book your free call now</a>' +
              '<p class="fblm-fine">Prefer the phone? Call <a href="tel:' + PHONE + '">' + PHONE_D + '</a>.</p>' +
              '</div>';
            overlay.querySelector(".fblm-close").addEventListener("click", closeModal);
            var bk = overlay.querySelector("[data-book]"); if (bk) bk.addEventListener("click", function () { track("book_click"); });
            track("success");
          }
          else { msg.className = "fblm-msg err"; msg.textContent = d.error || "Something went wrong — please call us."; btn.disabled = false; }
        })
        .catch(function () { msg.className = "fblm-msg err"; msg.textContent = "Network error — please call " + PHONE_D + "."; btn.disabled = false; });
    });
    startCountdown(overlay.querySelector("[data-count]"));
    return overlay;
  }
  function openModal(src) { buildModal(); requestAnimationFrame(function () { overlay.classList.add("fblm-show"); }); track("open", { source: src || "?" }); }
  function closeModal() { if (overlay) overlay.classList.remove("fblm-show"); }

  function startCountdown(node) {
    function tick() {
      var ms = monthEnd() - new Date(); if (ms < 0) ms = 0;
      var d = Math.floor(ms / 864e5), h = Math.floor(ms / 36e5) % 24, m = Math.floor(ms / 6e4) % 60, s = Math.floor(ms / 1e3) % 60;
      node.innerHTML = [["Days", d], ["Hrs", h], ["Min", m], ["Sec", s]].map(function (x) { return '<div><b>' + String(x[1]).padStart(2, "0") + '</b><span>' + x[0] + '</span></div>'; }).join("");
    }
    tick(); setInterval(tick, 1000);
  }

  /* ---------------- Individual mechanisms ---------------- */
  function helloBar() {
    if (!FEAT.hello) return;
    var bar = el('<div class="fblm-hellobar"><span>🎯 <b>This month only:</b> free website + SEO audit for ' + new Date().toLocaleString("en-US", { month: "long" }) + ' — limited spots.</span><button>Claim mine</button><button class="fblm-x" aria-label="Dismiss">&times;</button></div>');
    document.body.appendChild(bar);
    bar.querySelector("button").addEventListener("click", function () { openModal("hellobar"); });
    bar.querySelector(".fblm-x").addEventListener("click", function () { bar.classList.remove("fblm-show"); });
    setTimeout(function () { bar.classList.add("fblm-show"); }, 600);
  }
  function fab() {
    if (!FEAT.fab) return;
    var b = el('<button class="fblm-fab">💬 Get my free plan</button>');
    b.addEventListener("click", function () { openModal("fab"); });
    document.body.appendChild(b);
  }
  function mobileBar() {
    if (!FEAT.mobile) return;
    var b = el('<div class="fblm-mobilebar"><a class="fblm-call" href="tel:' + PHONE + '">📞 Call now</a><button class="fblm-quote">⚡ Free quote</button></div>');
    b.querySelector(".fblm-quote").addEventListener("click", function () { openModal("mobilebar"); });
    document.body.appendChild(b);
  }
  function exitIntent() {
    if (!FEAT.exit) return;
    document.addEventListener("mouseout", function (e) { if (e.clientY <= 0 && once("exit")) openModal("exit-intent"); });
    // mobile proxy: fast scroll to top
    var ly = window.scrollY;
    window.addEventListener("scroll", function () { if (window.innerWidth < 768 && window.scrollY < ly - 240 && window.scrollY < 400 && once("exit")) openModal("exit-intent-mobile"); ly = window.scrollY; }, { passive: true });
  }
  function scrollOffer() {
    if (!FEAT.scroll) return;
    function onScroll() {
      var p = window.scrollY / (document.body.scrollHeight - window.innerHeight);
      if (p > 0.5 && once("scroll")) { openModal("scroll-50"); window.removeEventListener("scroll", onScroll); }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
  }
  function relTime(ts) {
    var s = Math.max(1, Math.floor((Date.now() - ts) / 1000));
    if (s < 60) return s + " seconds ago";
    var m = Math.floor(s / 60); if (m < 60) return m + (m === 1 ? " minute ago" : " minutes ago");
    var h = Math.floor(m / 60); if (h < 24) return h + (h === 1 ? " hour ago" : " hours ago");
    return Math.floor(h / 24) + " days ago";
  }
  function socialProof() {
    if (!FEAT.social) return;
    /* Sample fallback — clearly labeled. Fabricated social proof is deceptive
       (and unlawful in some places), so on a live site the toasts pull REAL
       recent leads from /api/recent-leads (backed by Cloudflare KV). The
       sample data only shows when no real data is available (e.g. local demo). */
    var SAMPLES = [
      { name: "Mike R.", text: "in Conroe requested a free audit", real: false },
      { name: "Sarah L.", text: "in Spring booked a strategy call", real: false },
      { name: "Carlos M.", text: "in Katy claimed the monthly offer", real: false },
      { name: "Jen P.", text: "in Tomball requested a quote", real: false }
    ];
    var data = SAMPLES, node = el('<div class="fblm-toast"></div>');
    document.body.appendChild(node);
    fetch("/api/recent-leads").then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (j && j.length) data = j.map(function (x) { return { name: x.n, text: x.a, ts: x.t, real: true }; });
    }).catch(function () {});
    var i = 0;
    function show() {
      var s = data[i % data.length]; i++;
      var when = s.real ? relTime(s.ts) + " • verified lead" : "recently • sample";
      node.dataset.kind = s.real ? "live" : "sample";
      node.innerHTML = '<div><span class="fblm-t-name">' + s.name + '</span> ' + s.text + '.</div><div class="fblm-t-time">' + when + '</div>';
      node.classList.add("fblm-show");
      setTimeout(function () { node.classList.remove("fblm-show"); }, 5200);
    }
    setTimeout(function () { show(); setInterval(show, 12000); }, 4000);
  }

  function activate() {
    track("activate", { features: FEAT });
    helloBar(); fab(); mobileBar(); exitIntent(); scrollOffer(); socialProof();
  }

  /* ---------------- Demo control panel ---------------- */
  function panel() {
    var p = el('<div class="fblm-panel"><button class="fblm-collapse" title="Minimize">_</button>' +
      '<h4>⚡ Lead Engine — Demo</h4><p class="fblm-p-sub">Owner preview. Off by default for real visitors.</p>' +
      '<div class="fblm-body">' +
      '<div class="fblm-master"><span>Lead Capture</span><label class="fblm-switch"><input type="checkbox" id="fblm-master"><span class="fblm-slider"></span></label></div>' +
      '<div class="fblm-feats"></div>' +
      '<button class="fblm-cta" id="fblm-preview" style="margin-top:.7rem;padding:.6rem;font-size:.9rem">Preview the popup ▶</button>' +
      '<p class="fblm-note">Real submissions are emailed to the owner via Resend. Social-proof toasts use sample data in this demo.</p>' +
      '</div></div>');
    var feats = [["hello", "Hello bar (top offer)"], ["fab", "Floating CTA button"], ["mobile", "Sticky mobile call bar"], ["exit", "Exit-intent popup"], ["scroll", "Scroll-triggered offer"], ["poker", "Poker challenge (in popup)"], ["social", "Social-proof toasts"]];
    var fc = p.querySelector(".fblm-feats");
    feats.forEach(function (f) {
      var row = el('<label class="fblm-feat"><input type="checkbox" data-f="' + f[0] + '"' + (FEAT[f[0]] ? " checked" : "") + '> ' + f[1] + '</label>');
      fc.appendChild(row);
    });
    document.body.appendChild(p);
    var master = p.querySelector("#fblm-master"); master.checked = LEADS;
    master.addEventListener("change", function () { localStorage.setItem("fblm_leads", master.checked ? "on" : "off"); location.reload(); });
    fc.querySelectorAll("input").forEach(function (cb) {
      cb.addEventListener("change", function () { FEAT[cb.dataset.f] = cb.checked ? 1 : 0; localStorage.setItem("fblm_feat", JSON.stringify(FEAT)); if (LEADS) location.reload(); });
    });
    p.querySelector("#fblm-preview").addEventListener("click", function () { openModal("preview"); });
    p.querySelector(".fblm-collapse").addEventListener("click", function () { p.classList.toggle("fblm-min"); });
  }

  function init() {
    if (LEADS) activate();
    if (DEMO) panel();
  }
  if (document.readyState !== "loading") init(); else document.addEventListener("DOMContentLoaded", init);
})();
