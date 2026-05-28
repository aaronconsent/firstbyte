#!/usr/bin/env python3
"""Rebuild /contact/ as a polished page with a working contact form that
POSTs to the /api/contact Pages Function (Resend). Replaces the dead
Gravity Forms. Idempotent. Run after hubs.py; navigation/cleanup/enhance after.
"""
import theme_ui as tu

BASE = tu.BASE
SERVICE_AREA = "The Woodlands & Greater Houston, TX"
PHONE_DISPLAY = tu.PHONE_DISPLAY
PHONE = tu.PHONE
# Service-area business: show the region, not a home address.
MAP_Q = "The+Woodlands,+TX"

PIN = '<svg class="ic" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>'
TEL = '<svg class="ic" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.7a2 2 0 0 1-.5 2.1L8 9.6a16 16 0 0 0 6 6l1.1-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.5 2.7.6a2 2 0 0 1 1.7 2z"/></svg>'
CLOCK = '<svg class="ic" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'

FORM = f"""<div class="fb-formcard"><h3>Send us a message</h3>
<form id="fb-contactform" action="/api/contact" method="POST">
<div class="fb-field"><label for="cf-name">Name</label><input id="cf-name" name="name" type="text" required></div>
<div class="fb-field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" required></div>
<div class="fb-field"><label for="cf-phone">Phone (optional)</label><input id="cf-phone" name="phone" type="tel"></div>
<div class="fb-field"><label for="cf-msg">How can we help?</label><textarea id="cf-msg" name="message" required></textarea></div>
<input class="fb-hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="button-primary" type="submit">Send message</button>
<div class="fb-formmsg" id="fb-formmsg" role="status" aria-live="polite"></div>
</form></div>
<script>
(function(){{
  var f=document.getElementById('fb-contactform'); if(!f) return;
  var msg=document.getElementById('fb-formmsg');
  var p=new URLSearchParams(location.search);
  if(p.get('sent')==='1'){{msg.className='fb-formmsg ok';msg.textContent='Thanks! We\\u2019ll be in touch shortly.';}}
  else if(p.get('sent')==='0'){{msg.className='fb-formmsg err';msg.textContent='Sorry, that didn\\u2019t send. Please call us at {PHONE_DISPLAY}.';}}
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var btn=f.querySelector('button[type=submit]');btn.disabled=true;
    msg.className='fb-formmsg';msg.textContent='Sending\\u2026';
    fetch('/api/contact',{{method:'POST',headers:{{'Accept':'application/json'}},body:new FormData(f)}})
      .then(function(r){{return r.json().catch(function(){{return {{ok:r.ok}};}});}})
      .then(function(d){{ if(d.ok){{f.reset();msg.className='fb-formmsg ok';msg.textContent=(d.message||'Thanks! We\\u2019ll be in touch shortly.');}}
        else {{msg.className='fb-formmsg err';msg.textContent=(d.error||'Something went wrong. Please call us.');}} }})
      .catch(function(){{msg.className='fb-formmsg err';msg.textContent='Network error. Please call us at {PHONE_DISPLAY}.';}})
      .finally(function(){{btn.disabled=false;}});
  }});
}})();
</script>"""

INFO = f"""<div class="fb-infocard"><h3>Get in touch</h3>
<div class="fb-inforow">{PIN}<div><strong style="color:#fff;">Service area</strong><br>{tu.esc(SERVICE_AREA)}</div></div>
<div class="fb-inforow">{TEL}<div><strong style="color:#fff;">Call</strong><br><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></div></div>
<div class="fb-inforow">{CLOCK}<div><strong style="color:#fff;">Hours</strong><br>Mon–Fri, 9am–5pm CT</div></div>
<div class="fb-inforow">{CLOCK}<div><strong style="color:#fff;">#SundayByte</strong><br>A free weekly marketing tip — ask us to add you.</div></div>
</div>"""

MAP = (f'<div class="fb-map" style="margin-top:1.5rem;"><iframe title="First Byte location map" loading="lazy" '
       f'referrerpolicy="no-referrer-when-downgrade" '
       f'src="https://www.google.com/maps?q={MAP_Q}&z=11&output=embed"></iframe></div>')


def build():
    inner = (
        tu.hero("Contact", 'Let’s grow your <span class="accent">business</span>',
                "Tell us what you’re working on and we’ll get back to you fast. Based in The Woodlands, serving all of Greater Houston.")
        + '<section class="fb-section"><div class="fb-wrap">'
          f'<div class="fb-contact"><div>{INFO}{MAP}</div>{FORM}</div>'
          '</div></section>'
        + tu.cta("Prefer to talk?", f"Call us anytime at {PHONE_DISPLAY} — we’d love to hear from you.")
    )
    url = BASE + "/contact/"
    schema = ('<script type="application/ld+json" data-seo-enhance="geo">'
              + '{"@context":"https://schema.org","@type":"ContactPage","@id":"' + url
              + '#webpage","url":"' + url + '","name":"Contact First Byte",'
              + '"about":{"@id":"' + BASE + '/#localbusiness"}}</script>')
    page = tu.render(inner, "Contact First Byte — The Woodlands, TX", url,
                     "Contact First Byte, a digital marketing agency in The Woodlands, TX. Call (713) 578-0634 or send a message to grow your business.",
                     schema)
    tu.write(["contact"], page)
    print("  rebuilt /contact/ (working form)")


if __name__ == "__main__":
    build()
