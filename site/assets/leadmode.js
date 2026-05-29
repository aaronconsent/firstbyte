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

  /* ---------------- Sound engine (WebAudio, no asset files) ---------------- */
  var AC = null, MUTE = localStorage.getItem("fblm_mute") === "1";
  function actx() {
    try { if (!AC) AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return null; }
    if (AC && AC.state === "suspended") { try { AC.resume(); } catch (e) {} }
    return AC;
  }
  function tone(freq, dur, type, vol, when) {
    var ac = actx(); if (!ac || MUTE) return;
    var t0 = ac.currentTime + (when || 0);
    var o = ac.createOscillator(), g = ac.createGain();
    o.type = type || "sine"; o.frequency.setValueAtTime(freq, t0);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(Math.max(0.001, vol || 0.18), t0 + 0.012);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    o.connect(g); g.connect(ac.destination); o.start(t0); o.stop(t0 + dur + 0.02);
  }
  var sfx = {
    deal: function () { tone(300, 0.07, "triangle", 0.12); tone(180, 0.05, "sine", 0.08, 0.01); },
    chip: function () { tone(1200, 0.05, "square", 0.06); tone(1750, 0.05, "square", 0.04, 0.03); },
    bet: function () { tone(700, 0.05, "square", 0.07); },
    flip: function () { tone(520, 0.06, "triangle", 0.1); },
    win: function () {[523, 659, 784, 1047].forEach(function (f, i) { tone(f, 0.2, "triangle", 0.17, i * 0.085); }); },
    lose: function () { tone(220, 0.28, "sine", 0.13); tone(165, 0.4, "sine", 0.11, 0.09); },
    blackjack: function () {[523, 659, 784, 1047, 1319].forEach(function (f, i) { tone(f, 0.22, "triangle", 0.18, i * 0.075); }); tone(1047, 0.55, "sine", 0.1, 0.42); },
    jackpot: function () { for (var i = 0; i < 9; i++) tone(440 * Math.pow(1.1225, i), 0.15, "triangle", 0.15, i * 0.065); for (var j = 0; j < 4; j++) tone(1600 + j * 200, 0.4, "sine", 0.08, 0.6 + j * 0.05); }
  };

  /* ---------------- Celebration: confetti + flash ---------------- */
  function celebrate(level) {
    if (!overlay) return;
    var colors = ["#ffd700", "#ffec80", "#ffb300", "#01f6f2", "#ffffff", "#ffcf3f"];
    var n = level === "jackpot" ? 160 : (level === "big" ? 110 : 60);
    var flash = el('<div class="fblm-flash"></div>'); overlay.appendChild(flash);
    setTimeout(function () { flash.remove(); }, 700);
    for (var i = 0; i < n; i++) {
      var c = document.createElement("i");
      c.className = "fblm-confetti";
      var shape = Math.random();
      if (shape > 0.6) c.style.borderRadius = "50%";
      c.style.left = (Math.random() * 100) + "vw";
      c.style.background = colors[i % colors.length];
      c.style.animationDelay = (Math.random() * 0.35) + "s";
      c.style.animationDuration = (1 + Math.random() * 1.1) + "s";
      c.style.setProperty("--dx", (Math.random() * 280 - 140) + "px");
      c.style.setProperty("--rot", (Math.random() * 900 - 450) + "deg");
      overlay.appendChild(c);
      (function (node) { setTimeout(function () { node.remove(); }, 2400); })(c);
    }
  }
  function countUp(node, from, to, fmt) {
    var start = null, dur = 650;
    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min(1, (ts - start) / dur), e = 1 - Math.pow(1 - p, 3);
      node.textContent = fmt(Math.round(from + (to - from) * e));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------------- Modal (shared offer + multi-step form) ---------------- */
  var overlay;
  function buildModal() {
    if (overlay) return overlay;
    overlay = el('<div class="fblm-overlay" role="dialog" aria-modal="true"></div>');
    overlay.innerHTML =
      '<div class="fblm-modal">' +
      '<button class="fblm-close" aria-label="Close">&times;</button>' +
      '<span class="fblm-badge">Free • Limited this month</span>' +
      '<h2>Get your <span class="a">free 2026 growth plan</span></h2>' +
      '<p class="fblm-sub">A no-obligation website + local-SEO audit for your business — what\'s working, what\'s leaking leads, and the 3 fastest wins. ($500 value.)</p>' +
      '<div class="fblm-bjstage fblm-hidden fblm-bj">' +
        '<button type="button" class="fblm-mute" data-mute aria-label="Toggle sound">🔊</button>' +
        '<div class="fblm-bj-burst fblm-hidden" data-burst></div>' +
        '<div class="fblm-bj-bank">' +
          '<span class="fblm-stat">Chips <span class="fblm-chip" data-bankchip><b data-bank>100</b></span></span>' +
          '<span class="fblm-stat">Credit won <span class="fblm-chip fblm-chip-teal" data-creditchip><b data-credit>100</b></span></span>' +
        '</div>' +
        '<div class="fblm-row" data-bjdealer></div><div class="fblm-rowlabel" data-dtotal>Dealer</div>' +
        '<div class="fblm-bj-hands" data-bjplayer></div>' +
        '<div class="fblm-bj-msg" data-bjmsg></div>' +
        '<div class="fblm-bj-actions fblm-hidden" data-actions>' +
          '<button type="button" data-hit>Hit</button><button type="button" data-stand>Stand</button>' +
          '<button type="button" data-double>Double</button><button type="button" data-split>Split</button>' +
        '</div>' +
        '<div class="fblm-bj-bet" data-betrow>' +
          '<div class="fblm-presets" data-presets>' +
            '<button type="button" class="fblm-preset" data-preset="25">$25</button>' +
            '<button type="button" class="fblm-preset" data-preset="100">$100</button>' +
            '<button type="button" class="fblm-preset fblm-preset-max" data-preset="max">Max</button>' +
          '</div>' +
          '<div class="fblm-betslide">' +
            '<span class="fblm-betslide-end">$25</span>' +
            '<input type="range" class="fblm-betslider" data-betslider min="25" max="100" step="25" value="25" aria-label="Bet amount — drag right to bet more">' +
            '<span class="fblm-betslide-end" data-slidemax>$100</span>' +
          '</div>' +
          '<button type="button" class="fblm-dealchip" data-deal-bj data-betchip>' +
            '<span class="fblm-dealchip-lbl" data-deallbl>Tap to deal</span><b data-bet>$25</b>' +
          '</button>' +
        '</div>' +
        '<button type="button" class="fblm-cta fblm-hidden" data-cashout style="margin-top:.6rem">💰 Cash out</button>' +
        '<div class="fblm-final fblm-hidden" data-final>' +
          '<div class="fblm-final-q" data-finalq></div>' +
          '<button type="button" class="fblm-cta fblm-allin" data-allin></button>' +
          '<button type="button" class="fblm-final-skip" data-claimnow></button>' +
        '</div>' +
      '</div>' +
      '<div class="fblm-steps"><i class="on"></i><i></i><i></i></div>' +
      '<form class="fblm-form" novalidate>' +
        '<input class="fblm-hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">' +
        '<input type="hidden" name="_goal" value="">' +
        '<input type="hidden" name="_credit" value="">' +
        '<div class="fblm-step on" data-step="0">' +
          '<div class="fblm-field"><label data-spendlabel>How would you like to put your credit to work?</label></div>' +
          '<div class="fblm-choices">' +
            '<button type="button" data-goal="More leads &amp; calls">📈 Get more leads &amp; calls</button>' +
            '<button type="button" data-goal="A new / refreshed website">🎨 A new or refreshed website</button>' +
            '<button type="button" data-goal="Rank higher on Google (SEO)">🔍 Rank higher on Google</button>' +
            '<button type="button" data-goal="Launch paid ad campaigns">📣 Launch paid ad campaigns</button>' +
            '<button type="button" data-goal="Not sure — recommend a plan">🤝 Not sure — recommend a plan</button>' +
          '</div>' +
        '</div>' +
        '<div class="fblm-step" data-step="1">' +
          '<div class="fblm-field"><label>Your name</label><input name="name" autocomplete="name" placeholder="Jane Smith"></div>' +
          '<div class="fblm-field"><label>Email (where we send your credit details)</label><input name="email" type="email" autocomplete="email" placeholder="you@business.com"></div>' +
          '<button type="button" class="fblm-cta" data-next>Continue &rarr;</button>' +
        '</div>' +
        '<div class="fblm-step" data-step="2">' +
          '<div class="fblm-field"><label>Best phone (so we can set up your credit)</label><input name="phone" type="tel" autocomplete="tel" placeholder="(713) 555-0123"></div>' +
          '<div class="fblm-field"><label>Anything we should know about your business? (optional)</label><textarea name="message" rows="2" placeholder="Tell us a bit about your business"></textarea></div>' +
          '<button type="submit" class="fblm-cta" data-claimbtn>🎁 Claim my credit</button>' +
        '</div>' +
        '<div class="fblm-msg" role="status" aria-live="polite"></div>' +
      '</form>' +
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
          bankChip = overlay.querySelector("[data-bankchip]"), creditChip = overlay.querySelector("[data-creditchip]"),
          bjMsg = overlay.querySelector("[data-bjmsg]"), betRow = overlay.querySelector("[data-betrow]"),
          actions = overlay.querySelector("[data-actions]"), cashBtn = overlay.querySelector("[data-cashout]"),
          burstEl = overlay.querySelector("[data-burst]"), muteBtn = overlay.querySelector("[data-mute]"),
          finalBox = overlay.querySelector("[data-final]"), finalQ = overlay.querySelector("[data-finalq]"),
          allInBtn = overlay.querySelector("[data-allin]"), claimNowBtn = overlay.querySelector("[data-claimnow]"),
          slider = overlay.querySelector("[data-betslider]"), slideMax = overlay.querySelector("[data-slidemax]"),
          dealLbl = overlay.querySelector("[data-deallbl]"), dealBtn = overlay.querySelector("[data-deal-bj]");
      muteBtn.textContent = MUTE ? "🔇" : "🔊";
      muteBtn.addEventListener("click", function () { MUTE = !MUTE; localStorage.setItem("fblm_mute", MUTE ? "1" : "0"); muteBtn.textContent = MUTE ? "🔇" : "🔊"; if (!MUTE) sfx.chip(); });
      function popBurst(txt, level) {
        burstEl.textContent = txt; burstEl.className = "fblm-bj-burst fblm-burst-" + (level || "win");
        burstEl.classList.remove("fblm-hidden"); void burstEl.offsetWidth; burstEl.classList.add("fblm-go");
        setTimeout(function () { burstEl.classList.add("fblm-hidden"); burstEl.classList.remove("fblm-go"); }, 1900);
      }
      h2.innerHTML = 'Blackjack — <span class="a">win real credit</span> 🃏';
      sub.textContent = "You've got $100 in chips ($10 a hand). Every chip you keep becomes 1st-month account credit — up to $2,500. The deck's stacked in your favor!";
      bjStage.classList.remove("fblm-hidden"); stepsBar.classList.add("fblm-hidden"); form.classList.add("fblm-hidden");

      var SUITS = ["♠", "♥", "♦", "♣"], RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
      var CAP = 2500, bank = 100, bet = 25, STEP = 25, deck = [], dealer = [], hands = [], active = 0, phase = "bet";
      var finalOffered = false, lastHand = false;

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
      function stagger() { Array.prototype.slice.call(overlay.querySelectorAll(".fblm-cardwrap:not(.fblm-in)")).forEach(function (w, i) { w.classList.add("fblm-in"); setTimeout(function () { w.classList.add("in"); sfx.deal(); }, 110 * i); }); }
      function paintSlider() {
        var mx = Math.max(STEP, bank), pct = mx > STEP ? ((bet - STEP) / (mx - STEP)) * 100 : 100;
        slider.style.background = "linear-gradient(90deg,#ffcb37 0%,#ffb300 " + pct + "%,rgba(0,0,0,.45) " + pct + "%,rgba(0,0,0,.45) 100%)";
      }
      function renderBank() {
        bankEl.textContent = "$" + bank; creditEl.textContent = "$" + Math.min(bank, CAP); betEl.textContent = "$" + bet;
        slider.max = Math.max(STEP, bank); slider.value = bet; slideMax.textContent = "$" + Math.max(STEP, bank); paintSlider();
      }
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
        actions.querySelector("[data-double]").classList.toggle("fblm-hidden", !(two && !lastHand && bank > h.bet));
        actions.querySelector("[data-split]").classList.toggle("fblm-hidden", !(hands.length === 1 && two && !lastHand && val(h.cards[0].r) === val(h.cards[1].r) && bank > h.bet));
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
        bjStage.classList.remove("fblm-win", "fblm-lose"); sfx.chip();
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
        var dt = total(dealer), dBust = dt > 21, dBJ = isBJ(dealer), net = 0, parts = [], wasBJ = false;
        hands.forEach(function (h, i) {
          var pt = total(h.cards), lbl = hands.length > 1 ? "Hand " + (i + 1) + ": " : "", r;
          if (pt > 21) { net -= h.bet; r = "bust −$" + h.bet; }
          else if (isBJ(h.cards) && hands.length === 1 && !dBJ) { var w = Math.round(h.bet * 1.5); net += w; r = "Blackjack +$" + w; wasBJ = true; }
          else if (dBust) { net += h.bet; r = "dealer busts +$" + h.bet; }
          else if (pt > dt) { net += h.bet; r = "win +$" + h.bet; }
          else if (pt === dt) { r = "push"; }
          else { net -= h.bet; r = "lose −$" + h.bet; }
          parts.push(lbl + r);
        });
        var oldCredit = Math.min(bank, CAP);
        bank = Math.min(CAP, Math.max(0, bank + net)); betEl.textContent = "$" + bet;
        bankEl.textContent = "$" + bank; phase = "bet";
        var newCredit = Math.min(bank, CAP), capped = bank >= CAP;
        if (net > 0) {
          countUp(creditEl, oldCredit, newCredit, function (v) { return "$" + v; });
          creditChip.classList.remove("fblm-pulse"); void creditChip.offsetWidth; creditChip.classList.add("fblm-pulse");
          bankChip.classList.remove("fblm-pulse"); void bankChip.offsetWidth; bankChip.classList.add("fblm-pulse");
          bjStage.classList.add("fblm-win");
          if (capped) { sfx.jackpot(); celebrate("jackpot"); popBurst("🏆 MAX $" + CAP + "! 🏆", "jackpot"); }
          else if (wasBJ) { sfx.blackjack(); celebrate("big"); popBurst("BLACKJACK! +$" + net, "big"); }
          else { sfx.win(); celebrate(net >= 100 ? "big" : "win"); popBurst("WIN +$" + net + " 🎉", "win"); }
        } else {
          creditEl.textContent = "$" + newCredit;
          if (net < 0) { sfx.lose(); bjStage.classList.add("fblm-lose"); }
        }
        bjMsg.innerHTML = parts.join(" · ") + (net > 0 ? " 🎉" : "") + (capped ? '<br><b>You maxed the $' + CAP + ' credit cap! 🏆</b>' : "");
        if (bet > bank) bet = Math.max(STEP, bank); betEl.textContent = "$" + bet;
        if (!capped && !lastHand && bank >= STEP) { betRow.classList.remove("fblm-hidden"); dealLbl.textContent = "Tap to deal"; slider.max = Math.max(STEP, bank); slider.value = bet; slideMax.textContent = "$" + Math.max(STEP, bank); paintSlider(); } else betRow.classList.add("fblm-hidden");
        cashBtn.classList.remove("fblm-hidden");
        cashBtn.textContent = (finalOffered ? "🎁 Claim my $" : "💰 Cash out my $") + Math.min(bank, CAP) + " credit →";
        track("bj_round", { net: net, bank: bank });
      }
      var betTick = 0;
      function setBet(v) { bet = Math.max(STEP, Math.min(bank, v)); betEl.textContent = "$" + bet; slider.value = bet; paintSlider(); sfx.chip(); }
      slider.addEventListener("input", function () {
        bet = Math.max(STEP, Math.min(bank, parseInt(slider.value, 10) || STEP));
        betEl.textContent = "$" + bet; paintSlider();
        var now = Date.now(); if (now - betTick > 55) { betTick = now; sfx.bet(); }
      });
      overlay.querySelectorAll("[data-preset]").forEach(function (b) {
        b.addEventListener("click", function () { setBet(b.dataset.preset === "max" ? bank : parseInt(b.dataset.preset, 10)); });
      });
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
      function goToForm() {
        var credit = Math.min(bank, CAP); track("bj_cashout", { credit: credit });
        sfx.jackpot(); celebrate("jackpot");
        form._goal.value = "Blackjack prize claim";
        form._credit.value = "$" + credit;
        bjStage.classList.add("fblm-hidden"); stepsBar.classList.remove("fblm-hidden"); form.classList.remove("fblm-hidden");
        h2.innerHTML = 'Claim your <span class="a">$' + credit + ' account credit</span> 🎉';
        sub.textContent = "You won $" + credit + " in first-month account credit! Let's put it to work — just answer a couple quick questions and it's yours.";
        var sl = overlay.querySelector("[data-spendlabel]"); if (sl) sl.textContent = "How would you like to put your $" + credit + " credit to work?";
        var cb = overlay.querySelector("[data-claimbtn]"); if (cb) cb.innerHTML = "🎁 Claim my $" + credit + " credit";
        goStep(0);
      }
      function showFinalOffer() {
        var credit = Math.min(bank, CAP), pot = Math.min(CAP, credit * 2);
        // Already at the cap, or no upside left — go straight to the claim form.
        if (credit >= CAP || pot <= credit) { goToForm(); return; }
        finalQ.innerHTML = "One last shot! Go <b>all-in</b> with your $" + credit + " and you could walk away with <b>$" + pot + "</b> in credit.";
        allInBtn.innerHTML = "🎲 ALL-IN — bet all $" + credit + " on one final hand";
        claimNowBtn.textContent = "No thanks — claim my $" + credit + " now →";
        actions.classList.add("fblm-hidden"); betRow.classList.add("fblm-hidden"); cashBtn.classList.add("fblm-hidden");
        bjMsg.textContent = ""; finalBox.classList.remove("fblm-hidden");
        track("bj_final_offer", { credit: credit });
      }
      allInBtn.addEventListener("click", function () {
        finalOffered = true; lastHand = true; bet = bank;
        finalBox.classList.add("fblm-hidden"); track("bj_allin", { bet: bet });
        startRound();
      });
      claimNowBtn.addEventListener("click", function () { finalBox.classList.add("fblm-hidden"); goToForm(); });
      cashBtn.addEventListener("click", function () { if (finalOffered) goToForm(); else showFinalOffer(); });
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
      var creditStr = form._credit.value || "";
      var fd = new FormData();
      fd.append("name", form.name.value); fd.append("email", form.email.value); fd.append("phone", form.phone.value); fd.append("company", form.company.value);
      fd.append("message", "[Lead Engine • Blackjack prize claim" + (creditStr ? " " + creditStr + " credit" : "") + " • wants to spend on: " + (form._goal.value || "?") + "] " + (form.message.value || ""));
      track("submit", { goal: form._goal.value, credit: creditStr });
      fetch("/api/contact", { method: "POST", headers: { Accept: "application/json" }, body: fd })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d.ok) {
            overlay.querySelector(".fblm-modal").innerHTML =
              '<button class="fblm-close" aria-label="Close">&times;</button>' +
              '<div style="text-align:center;padding:.5rem 0">' +
              '<div style="font-size:3rem">🎉</div>' +
              '<h2>Your credit is reserved!</h2>' +
              '<p class="fblm-sub">Your <b style="color:#fff">' + (creditStr || "account") + ' credit</b> is locked in. <b style="color:#fff">Skip the wait</b> — grab a time on the calendar now and we\'ll map out exactly how to put it to work.</p>' +
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
    return overlay;
  }
  function openModal(src) { buildModal(); requestAnimationFrame(function () { overlay.classList.add("fblm-show"); }); track("open", { source: src || "?" }); }
  function closeModal() { if (overlay) overlay.classList.remove("fblm-show"); }

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

  function init() {
    if (LEADS) activate();
  }
  if (document.readyState !== "loading") init(); else document.addEventListener("DOMContentLoaded", init);
})();
