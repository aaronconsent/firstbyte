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
  var stored = localStorage.getItem("fblm_leads");
  var LEADS = stored === null ? true : stored === "on"; // ON by default (deployed live)
  if (!DEMO && !LEADS) return; // only off if explicitly disabled

  // Deployed default: only Blackjack, Social proof, and the Sticky mobile bar.
  var FEAT_DEFAULT = { hello: 0, fab: 0, mobile: 1, exit: 0, scroll: 0, social: 1, blackjack: 1 };
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
      '<div class="fblm-bjstage fblm-hidden fblm-bj">' +
        '<div class="fblm-bj-bank">Chips: <b data-bank>$100</b> &nbsp;·&nbsp; Credit won: <b data-credit style="color:#01f6f2">$100</b></div>' +
        '<div class="fblm-row" data-bjdealer></div><div class="fblm-rowlabel" data-dtotal>Dealer</div>' +
        '<div class="fblm-bj-hands" data-bjplayer></div>' +
        '<div class="fblm-bj-msg" data-bjmsg></div>' +
        '<div class="fblm-bj-actions fblm-hidden" data-actions>' +
          '<button type="button" data-hit>Hit</button><button type="button" data-stand>Stand</button>' +
          '<button type="button" data-double>Double</button><button type="button" data-split>Split</button>' +
        '</div>' +
        '<div class="fblm-bj-bet" data-betrow>' +
          '<button type="button" data-betdown aria-label="Lower bet">&minus;</button>' +
          '<span>Bet <b data-bet>$25</b></span>' +
          '<button type="button" data-betup aria-label="Raise bet">+</button>' +
          '<button type="button" data-betmax>Max</button>' +
          '<button type="button" class="fblm-cta" data-deal-bj>Deal</button>' +
        '</div>' +
        '<button type="button" class="fblm-cta fblm-hidden" data-cashout style="margin-top:.6rem">💰 Cash out</button>' +
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
    if (FEAT.blackjack) {
      var bjStage = overlay.querySelector(".fblm-bjstage"),
          stepsBar = overlay.querySelector(".fblm-steps"), h2 = overlay.querySelector(".fblm-modal h2"),
          sub = overlay.querySelector(".fblm-sub"),
          dRow = overlay.querySelector("[data-bjdealer]"), dTot = overlay.querySelector("[data-dtotal]"),
          pArea = overlay.querySelector("[data-bjplayer]"),
          bankEl = overlay.querySelector("[data-bank]"), creditEl = overlay.querySelector("[data-credit]"), betEl = overlay.querySelector("[data-bet]"),
          bjMsg = overlay.querySelector("[data-bjmsg]"), betRow = overlay.querySelector("[data-betrow]"),
          actions = overlay.querySelector("[data-actions]"), cashBtn = overlay.querySelector("[data-cashout]"),
          dealBtn = overlay.querySelector("[data-deal-bj]");
      h2.innerHTML = 'Blackjack — <span class="a">win real credit</span> 🃏';
      sub.textContent = "You've got $100 in chips ($10 a hand). Every chip you keep becomes 1st-month account credit — up to $2,500. The deck's stacked in your favor!";
      bjStage.classList.remove("fblm-hidden"); stepsBar.classList.add("fblm-hidden"); form.classList.add("fblm-hidden");

      var SUITS = ["♠", "♥", "♦", "♣"], RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
      var CAP = 2500, bank = 100, bet = 25, STEP = 25, deck = [], dealer = [], hands = [], active = 0, phase = "bet";

      function val(r) { return r >= 14 ? 11 : (r >= 11 ? 10 : r); }
      function total(cards) { var t = 0, a = 0; cards.forEach(function (c) { t += val(c.r); if (c.r === 14) a++; }); while (t > 21 && a) { t -= 10; a--; } return t; }
      function isBJ(cards) { return cards.length === 2 && total(cards) === 21; }
      function freshDeck() { var d = []; for (var s = 0; s < 4; s++) for (var r = 2; r <= 14; r++) d.push({ s: s, r: r }); return d; }
      function pull(pred) {
        if (!deck.length) deck = freshDeck();
        var idx = [], i; for (i = 0; i < deck.length; i++) if (pred(deck[i].r)) idx.push(i);
        if (!idx.length) for (i = 0; i < deck.length; i++) idx.push(i);
        return deck.splice(idx[Math.floor(Math.random() * idx.length)], 1)[0];
      }
      function cardEl(c, down) {
        var red = c.s === 1 || c.s === 2;
        return el('<div class="fblm-cardwrap"><div class="fblm-card' + (down ? " down" : "") + '">' +
          '<div class="face' + (red ? " red" : "") + '"><span>' + RANKS[c.r - 2] + '</span><span>' + SUITS[c.s] + '</span></div><div class="back"></div></div></div>');
      }
      // Favorable player card: never busts, tends to improve the hand.
      function playerCard(cards) { var t = total(cards); if (t <= 11) return pull(function () { return true; }); return pull(function (r) { return val(r) <= 21 - t; }); }
      function stagger() { Array.prototype.slice.call(overlay.querySelectorAll(".fblm-cardwrap:not(.fblm-in)")).forEach(function (w, i) { w.classList.add("fblm-in"); setTimeout(function () { w.classList.add("in"); }, 50 * i); }); }
      function renderBank() { bankEl.textContent = "$" + bank; creditEl.textContent = "$" + Math.min(bank, CAP); betEl.textContent = "$" + bet; }
      function renderDealer(reveal) {
        dRow.innerHTML = ""; dealer.forEach(function (c, i) { dRow.appendChild(cardEl(c, !reveal && i === 1)); });
        dTot.textContent = reveal ? ("Dealer: " + total(dealer) + (total(dealer) > 21 ? " — BUST" : "")) : "Dealer"; stagger();
      }
      function renderPlayer() {
        pArea.innerHTML = "";
        hands.forEach(function (h, i) {
          var grp = el('<div class="fblm-bj-hand' + (i === active && phase === "play" ? " active" : "") + '"></div>');
          var row = el('<div class="fblm-row"></div>'); h.cards.forEach(function (c) { row.appendChild(cardEl(c, false)); }); grp.appendChild(row);
          var t = total(h.cards);
          grp.appendChild(el('<div class="fblm-rowlabel">' + (hands.length > 1 ? "Hand " + (i + 1) + ": " : "") + t +
            (t > 21 ? " BUST" : (isBJ(h.cards) && hands.length === 1 ? " — BLACKJACK!" : "")) + (h.doubled ? " ×2" : "") + '</div>'));
          pArea.appendChild(grp);
        });
        stagger();
      }
      function setActions() {
        var h = hands[active], two = h.cards.length === 2;
        actions.classList.toggle("fblm-hidden", phase !== "play");
        actions.querySelector("[data-double]").classList.toggle("fblm-hidden", !(two && bank >= h.bet));
        actions.querySelector("[data-split]").classList.toggle("fblm-hidden", !(hands.length === 1 && two && val(h.cards[0].r) === val(h.cards[1].r) && bank >= h.bet));
      }
      function rigStart(cards) {
        var roll = Math.random();
        if (roll < 0.25) { cards.push(pull(function (r) { return r === 14; })); cards.push(pull(function (r) { return val(r) === 10; })); }          // blackjack
        else if (roll < 0.45) { var rk = [8, 14, 10][Math.floor(Math.random() * 3)]; cards.push(pull(function (r) { return r === rk; })); cards.push(pull(function (r) { return r === rk; })); } // pair (split fun)
        else if (roll < 0.65) { var v1 = 2 + Math.floor(Math.random() * 8); cards.push(pull(function (r) { return r !== 14 && val(r) === v1; })); cards.push(pull(function (r) { return r !== 14 && val(r) === (11 - v1); })); } // total 11 (double fun)
        else { var T = [18, 19, 20][Math.floor(Math.random() * 3)], f = pull(function (r) { return r !== 14 && val(r) >= 8; }); cards.push(f); var need = Math.max(2, Math.min(10, T - val(f))); cards.push(pull(function (r) { return r !== 14 && val(r) === need; })); } // strong total
      }
      function startRound() {
        if (bank < bet) { bjMsg.textContent = "Not enough chips — cash out your credit!"; return; }
        deck = freshDeck(); dealer = []; hands = [{ cards: [], bet: bet, done: false, doubled: false }]; active = 0; phase = "play";
        rigStart(hands[0].cards);
        dealer.push(pull(function (r) { return r >= 4 && r <= 6; })); dealer.push(pull(function () { return true; }));
        bjMsg.textContent = ""; betRow.classList.add("fblm-hidden"); cashBtn.classList.add("fblm-hidden");
        renderDealer(false); renderPlayer(); track("bj_deal", { bet: bet });
        if (isBJ(hands[0].cards)) { hands[0].done = true; dealerTurn(); } else setActions();
      }
      function advance() { for (var i = 0; i < hands.length; i++) if (!hands[i].done) { active = i; renderPlayer(); setActions(); return; } dealerTurn(); }
      function dealerTurn() {
        phase = "dealer"; actions.classList.add("fblm-hidden"); renderDealer(true);
        var anyLive = hands.some(function (h) { return total(h.cards) <= 21; });
        var t = total(dealer), g = 0;
        if (anyLive) {
          // House always loses: force the dealer to bust whenever the player is still in.
          while (t <= 21 && g++ < 14) { dealer.push(pull(function (r) { return val(r) >= 7; })); t = total(dealer); }
        } else {
          while (t < 17 && g++ < 10) { dealer.push(pull(function () { return true; })); t = total(dealer); }
        }
        renderDealer(true); resolve();
      }
      function resolve() {
        var dt = total(dealer), dBust = dt > 21, dBJ = isBJ(dealer), net = 0, parts = [];
        hands.forEach(function (h, i) {
          var pt = total(h.cards), lbl = hands.length > 1 ? "Hand " + (i + 1) + ": " : "", r;
          if (pt > 21) { net -= h.bet; r = "bust −$" + h.bet; }
          else if (isBJ(h.cards) && hands.length === 1 && !dBJ) { var w = Math.round(h.bet * 1.5); net += w; r = "Blackjack +$" + w; }
          else if (dBust) { net += h.bet; r = "dealer busts +$" + h.bet; }
          else if (pt > dt) { net += h.bet; r = "win +$" + h.bet; }
          else if (pt === dt) { r = "push"; }
          else { net -= h.bet; r = "lose −$" + h.bet; }
          parts.push(lbl + r);
        });
        bank = Math.min(CAP, Math.max(0, bank + net)); renderBank(); phase = "bet";
        var capped = bank >= CAP;
        bjMsg.innerHTML = parts.join(" · ") + (net > 0 ? " 🎉" : "") + (capped ? '<br><b>You maxed the $' + CAP + ' credit cap! 🏆</b>' : "");
        if (bet > bank) bet = Math.max(STEP, bank);
        if (!capped && bank >= STEP) { betRow.classList.remove("fblm-hidden"); dealBtn.textContent = "Deal next hand"; } else betRow.classList.add("fblm-hidden");
        cashBtn.classList.remove("fblm-hidden"); cashBtn.textContent = "💰 Cash out my $" + Math.min(bank, CAP) + " credit →";
        track("bj_round", { net: net, bank: bank });
      }
      function setBet(d) { bet = Math.max(STEP, Math.min(bank, d === "max" ? bank : bet + d)); renderBank(); }
      overlay.querySelector("[data-betup]").addEventListener("click", function () { setBet(STEP); });
      overlay.querySelector("[data-betdown]").addEventListener("click", function () { setBet(-STEP); });
      overlay.querySelector("[data-betmax]").addEventListener("click", function () { setBet("max"); });
      dealBtn.addEventListener("click", startRound);
      overlay.querySelector("[data-hit]").addEventListener("click", function () { var h = hands[active]; h.cards.push(playerCard(h.cards)); renderPlayer(); if (total(h.cards) >= 21) { h.done = true; advance(); } else setActions(); });
      overlay.querySelector("[data-stand]").addEventListener("click", function () { hands[active].done = true; advance(); });
      overlay.querySelector("[data-double]").addEventListener("click", function () { var h = hands[active]; if (h.cards.length !== 2 || bank < h.bet) return; h.doubled = true; h.bet *= 2; h.cards.push(playerCard(h.cards)); h.done = true; renderPlayer(); advance(); });
      overlay.querySelector("[data-split]").addEventListener("click", function () {
        var h = hands[active]; if (hands.length !== 1 || h.cards.length !== 2 || val(h.cards[0].r) !== val(h.cards[1].r) || bank < h.bet) return;
        hands = [{ cards: [h.cards[0]], bet: bet, done: false, doubled: false }, { cards: [h.cards[1]], bet: bet, done: false, doubled: false }];
        hands[0].cards.push(playerCard(hands[0].cards)); hands[1].cards.push(playerCard(hands[1].cards));
        active = 0; renderPlayer(); setActions(); track("bj_split");
      });
      cashBtn.addEventListener("click", function () {
        var credit = Math.min(bank, CAP); track("bj_cashout", { credit: credit });
        form._goal.value = "Blackjack credit: $" + credit + " first-month account credit";
        bjStage.classList.add("fblm-hidden"); stepsBar.classList.remove("fblm-hidden"); form.classList.remove("fblm-hidden");
        h2.innerHTML = 'Claim your <span class="a">$' + credit + ' account credit</span> 🎉';
        sub.textContent = "Your first-month credit — where should we send it?"; goStep(1);
      });
      renderBank();
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
    /* Honest social proof. Fabricated social proof is deceptive (and unlawful
       in some places), so for REAL visitors the toasts ONLY show genuine recent
       leads pulled from /api/recent-leads (backed by Cloudflare KV) — if there
       are none yet, nothing is shown. Clearly-labeled SAMPLE data is shown only
       in the owner demo (/?demo=1) so the owner can preview the look. */
    var SAMPLES = [
      { name: "Mike R.", text: "in Conroe requested a free audit", real: false },
      { name: "Sarah L.", text: "in Spring booked a strategy call", real: false },
      { name: "Carlos M.", text: "in Katy claimed the monthly offer", real: false },
      { name: "Jen P.", text: "in Tomball requested a quote", real: false }
    ];
    var node = null;
    function ensureNode() { if (!node) { node = el('<div class="fblm-toast"></div>'); document.body.appendChild(node); } return node; }
    function run(data) {
      if (!data.length) return;
      ensureNode();
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
    fetch("/api/recent-leads").then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      var real = (j && j.length) ? j.map(function (x) { return { name: x.n, text: x.a, ts: x.t, real: true }; }) : [];
      if (real.length) run(real);            // real visitors: only genuine leads
      else if (DEMO) run(SAMPLES);           // owner demo only: labeled samples
    }).catch(function () { if (DEMO) run(SAMPLES); });
  }

  /* Right-edge, vertically-centered widget that opens the Blackjack challenge. */
  function blackjackTab() {
    if (!FEAT.blackjack) return;
    var t = el('<button class="fblm-bjtab" aria-label="Play Blackjack — win up to $2,500 in account credit">' +
      '<span class="fblm-bjtab-ico">🃏</span>' +
      '<span class="fblm-bjtab-txt"><b>Win up to $2,500</b><span>Play Blackjack →</span></span>' +
      '</button>');
    t.addEventListener("click", function () { openModal("bj-tab"); });
    document.body.appendChild(t);
  }

  function activate() {
    track("activate", { features: FEAT });
    helloBar(); fab(); mobileBar(); exitIntent(); scrollOffer(); socialProof(); blackjackTab();
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
    var feats = [["hello", "Hello bar (top offer)"], ["fab", "Floating CTA button"], ["mobile", "Sticky mobile call bar"], ["exit", "Exit-intent popup"], ["scroll", "Scroll-triggered offer"], ["blackjack", "Blackjack challenge (in popup)"], ["social", "Social-proof toasts"]];
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
