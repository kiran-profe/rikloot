#!/usr/bin/env python3
"""Builds the RikLoot static site into ../docs.

Usage:  python3 site-src/build.py

Edit guides.py (category guides) or guides_more.py (articles), then re-run.
assets/site.css and assets/site.js in docs/ are edited directly, not generated.
"""
import os, sys, html, glob
from urllib.parse import quote_plus
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art_data import ART_BODY
from guides import GUIDES
from guides_more import ARTICLES
ALL = GUIDES + ARTICLES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'docs')
TAG = 'rikloot-21'           # Amazon Associates tracking ID
EMAIL = 'rickloot.official@gmail.com'
UPDATED = '27 November 2026'
e = html.escape

def amz(q):
    return f'https://www.amazon.in/s?k={quote_plus(q)}&tag={TAG}'

def art(name, cls='', decorative=True):
    a = ' aria-hidden="true"' if decorative else f' role="img" aria-label="{e(name.capitalize())} illustration"'
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 240 200" xmlns="http://www.w3.org/2000/svg"{a} focusable="false">{ART_BODY[name]}</svg>'

ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
EXT = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
PIN_MARK = '<svg viewBox="0 0 34 44" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M17 43s15-13.6 15-25.5a15 15 0 0 0-30 0C2 29.4 17 43 17 43z" fill="#E2432A"/><rect x="9.5" y="10" width="15" height="13" rx="2" fill="#FFC12E"/><path d="M17 10v13M9.5 15h15" stroke="#15213D" stroke-width="2"/></svg>'
STAR = '<svg class="rl-mq__star" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 1l2.8 8.2L23 12l-8.2 2.8L12 23l-2.8-8.2L1 12l8.2-2.8z"/></svg>'
DISCLOSURE = 'As an Amazon Associate I earn from qualifying purchases.'

def dots(pid, fill='currentColor', cls='rl-dots-bg'):
    return f'<svg class="{cls}" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="{pid}" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="{fill}"/></pattern></defs><rect width="100%" height="100%" fill="url(#{pid})"/></svg>'

NAV = [('index.html', 'Home'), ('guides.html', 'Guides'), ('about.html', 'About'), ('contact.html', 'Contact')]

def page(title, desc, body, current):
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{l}</a>' for h, l in NAV)
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#15213D">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Grandstander:wght@700;800&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<script src="assets/site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<div class="rl-announce color-scheme-3"><a href="disclosure.html">Honest buying guides for Indian homes · {e(DISCLOSURE)}</a></div>

<header class="rl-header">
  <div class="rl-container rl-header__inner">
    <a class="rl-wordmark" href="index.html" aria-label="RikLoot home">{PIN_MARK}RikLoot</a>
    <button class="rl-burger" type="button" aria-expanded="false" aria-controls="rl-nav" aria-label="Menu">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="rl-nav" id="rl-nav" aria-label="Main">
      {nav}
      <a class="rl-nav__cta" href="guides.html">Browse guides</a>
    </nav>
  </div>
</header>

<main id="main">
{body}
</main>

{NEWSLETTER}
{marquee(['Independent picks', 'Plain-language guides', 'Made for Indian homes', 'Updated regularly', 'Real people, real help'], 'red')}
{FOOTER}
</body>
</html>
'''

def marquee(items, tone, tilt=False):
    def group(hidden):
        inner = ''.join(f'<span class="rl-mq__item">{e(t)}</span>{STAR}' for _ in range(2) for t in items)
        return f'<div class="rl-mq__group"{" aria-hidden=\"true\"" if hidden else ""}>{inner}</div>'
    return f'<div class="rl-mq-wrap"><section class="rl-mq rl-mq--{tone}{" rl-mq--tilt" if tilt else ""}" aria-label="Highlights"><div class="rl-mq__track">{group(False)}{group(True)}</div></section></div>'

NEWSLETTER = '''<section class="rl-nl" aria-labelledby="rl-nl-h">
  <div class="rl-nl__card">
    <svg class="rl-nl__art" viewBox="0 0 220 180" aria-hidden="true" focusable="false">
      <path class="rl-nl__trail" d="M10 160 C60 170 70 120 110 130" fill="none" stroke="#15213D" stroke-width="6" stroke-dasharray=".1 16" stroke-linecap="round"/>
      <g class="rl-nl__env"><rect x="70" y="40" width="130" height="90" rx="10" fill="#fff"/><path d="M70 50 L135 96 L200 50" fill="none" stroke="#15213D" stroke-width="6" stroke-linejoin="round"/><rect x="150" y="56" width="34" height="26" rx="4" fill="#E2432A"/><rect x="164" y="56" width="6" height="26" fill="#FFC12E"/></g>
      <path d="M40 30l4 10 10 4-10 4-4 10-4-10-10-4 10-4z" fill="#E2432A"/>
    </svg>
    <div>
      <h2 id="rl-nl-h">Get new guides first</h2>
      <p class="rl-nl__sub">New buying guides, seasonal picks and useful finds, straight to your inbox.</p>
    </div>
    <form class="rl-nl__form" data-rl-newsletter novalidate>
      <p data-msg hidden tabindex="-1" role="status"></p>
      <label class="visually-hidden" for="RlNlEmail">Email address</label>
      <div class="rl-nl__field">
        <input class="rl-nl__input" id="RlNlEmail" type="email" name="email" autocomplete="email" autocapitalize="off" placeholder="you@example.com" required>
        <button type="submit" class="rl-nl__btn">Count me in
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/></svg>
        </button>
      </div>
      <p class="rl-nl__note">No spam. Unsubscribe anytime.</p>
    </form>
  </div>
</section>'''

def ic(path): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'
IC_MAIL = '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'
IC_PHONE = '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>'
IC_WA = '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>'
IC_CLOCK = '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'
IC_PIN = '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'

guide_links = ''.join(f'<li><a href="guide-{g["slug"]}.html">{e(g["name"])}</a></li>' for g in GUIDES)
FOOTER = f'''<footer class="rl-section rl-ft">
  <div class="rl-container">
    <div class="rl-ft__route" aria-hidden="true">
      <span class="rl-ft__route-start"></span><span class="rl-ft__route-line"></span>
      <span class="rl-ft__route-label">Picked for Indian homes</span>
      <svg class="rl-ft__route-end" viewBox="0 0 34 44" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M17 43s15-13.6 15-25.5a15 15 0 0 0-30 0C2 29.4 17 43 17 43z" fill="currentColor"/><rect x="9.5" y="10" width="15" height="13" rx="2" fill="#FFC12E"/><path d="M17 10v13M9.5 15h15" stroke="#15213D" stroke-width="2"/></svg>
    </div>
    <div class="rl-ft__grid">
      <div class="rl-ft__brand">
        <a href="index.html" aria-label="RikLoot home"><span class="rl-ft__wordmark">{PIN_MARK}RikLoot</span></a>
        <p class="rl-ft__caption">Useful finds, honestly picked</p>
        <p class="rl-ft__blurb">Plain-language buying guides for kitchen helpers, storage, crafts, décor, gadgets and everyday essentials — written for Indian homes.</p>
      </div>
      <nav aria-labelledby="ft-guides">
        <h2 class="rl-ft__heading" id="ft-guides">Guides</h2>
        <ul class="rl-ft__list" role="list"><li><a href="guides.html">All guides</a></li>{guide_links}</ul>
      </nav>
      <nav aria-labelledby="ft-quick">
        <h2 class="rl-ft__heading" id="ft-quick">Quick links</h2>
        <ul class="rl-ft__list" role="list">
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About us</a></li>
          <li><a href="contact.html">Contact us</a></li>
          <li><a href="contact.html#form">Suggest a guide</a></li>
        </ul>
      </nav>
      <nav aria-labelledby="ft-pol">
        <h2 class="rl-ft__heading" id="ft-pol">Policies</h2>
        <ul class="rl-ft__list" role="list">
          <li><a href="disclosure.html">Affiliate disclosure</a></li>
          <li><a href="privacy.html">Privacy policy</a></li>
          <li><a href="terms.html">Terms of use</a></li>
        </ul>
      </nav>
      <div class="rl-ft__helpcol">
        <h2 class="rl-ft__heading">Need help?</h2>
        <ul class="rl-ft__help" role="list">
          <li data-cfg-item>{ic(IC_MAIL)}<span><a data-cfg="email" href="mailto:{EMAIL}">{EMAIL}</a></span></li>
          <li data-cfg-item>{ic(IC_PHONE)}<span><a data-cfg="phone" href="tel:+917510380758">+91 75103 80758</a></span></li>
          <li data-cfg-item hidden>{ic(IC_WA)}<span><a data-cfg-href="whatsapp" href="#" target="_blank" rel="noopener">Chat on WhatsApp</a></span></li>
          <li data-cfg-item>{ic(IC_CLOCK)}<span data-cfg="hours">Mon–Sat, 10 am – 6 pm IST</span></li>
          <li data-cfg-item hidden>{ic(IC_PIN)}<span data-cfg="address"></span></li>
        </ul>
      </div>
    </div>
    <div class="rl-ft__bottom">
      <p class="rl-ft__copy">&copy; <span data-year>2026</span> <a href="index.html">RikLoot</a>. All rights reserved.</p>
      <p class="rl-ft__copy rl-ft__disc">{e(DISCLOSURE)} <a href="disclosure.html">Learn more</a>.</p>
    </div>
  </div>
</footer>'''

def page_hero(heading, sub, art_name, scheme, crumbs):
    a = art(art_name, 'rl-ph__art') if art_name else ''
    cr = ''.join(f'<li><a href="{h}">{e(l)}</a></li>' for h, l in crumbs[:-1]) + f'<li aria-current="page">{e(crumbs[-1][1])}</li>'
    return f'''<section class="rl-ph rl-section color-{scheme}">
  {dots('ph-dots')}
  <div class="rl-container"><div class="rl-ph__grid">
    <div>
      <nav aria-label="Breadcrumb"><ol class="rl-ph__crumbs">{cr}</ol></nav>
      <h1>{e(heading)}</h1>
      <p class="rl-ph__sub">{e(sub)}</p>
    </div>
    {a}
  </div></div>
</section>'''

def cat_grid(cards, heading, sub, link, scheme, pad, sec_id='categories'):
    cells = []
    for i, (title, cap, artn, tone, wide, href) in enumerate(cards, 1):
        cells.append(f'''<div class="rl-cat-cell reveal{" rl-cat-card--wide" if wide else ""}" style="--animation-order: {i};">
        <a href="{href}" class="rl-cat-card rl-cat-card--{tone}">
          {art(artn, 'rl-cat-card__art')}
          <span class="rl-cat-card__foot"><span><span class="rl-cat-card__name" role="heading" aria-level="3">{e(title)}</span><span class="rl-cat-card__count">{e(cap)}</span></span>
          <span class="rl-cat-card__go" aria-hidden="true">{ARROW}</span></span>
        </a></div>''')
    lk = f'<a class="rl-link-arrow" href="{link[0]}">{e(link[1])} {ARROW}</a>' if link else ''
    head = f'<div class="rl-head reveal"><div><h2 class="rl-head__title">{e(heading)}</h2><p class="rl-head__sub">{e(sub)}</p></div>{lk}</div>' if heading else ''
    return f'''<section id="{sec_id}" class="rl-cats rl-section color-{scheme}" style="padding:{pad[0]}px 0 {pad[1]}px">
  <div class="rl-container">
    {head}
    <div class="rl-cat-grid">{''.join(cells)}</div>
  </div>
</section>'''

def steps(items, heading, sub):
    lis = ''.join(f'<li class="rl-step reveal" style="--animation-order: {i};"><span class="rl-step__badge" aria-hidden="true">{i}</span><h3 class="rl-step__title">{e(t)}</h3><p class="rl-step__text">{e(x)}</p></li>' for i, (t, x) in enumerate(items, 1))
    return f'''<section class="rl-steps-sec rl-section color-scheme-2">
  {dots('steps-dots')}
  <div class="rl-container" style="position:relative">
    <div class="rl-head reveal"><div><h2 class="rl-head__title">{e(heading)}</h2><p class="rl-head__sub">{e(sub)}</p></div></div>
    <div style="position:relative">
      <span class="rl-route" aria-hidden="true"><span class="rl-route__parcel"><svg viewBox="0 0 40 40" width="40" height="40"><path d="M20 38C14 30 6 25 6 16a14 14 0 1 1 28 0c0 9-8 14-14 22z" fill="#E2432A"/><circle cx="20" cy="16" r="10" fill="#fff"/><rect x="13.5" y="12" width="13" height="9" rx="1" fill="#FFC12E"/><rect x="18.8" y="12" width="2.2" height="9" fill="#15213D"/></svg></span></span>
      <ol class="rl-steps" role="list">{lis}</ol>
    </div>
  </div>
</section>'''

def faq(items, open_first=False):
    return ''.join(f'<details{" open" if (i == 0 and open_first) else ""}><summary>{e(q)}</summary><div class="rl-faq__a">{a}</div></details>' for i, (q, a) in enumerate(items))

def pick_cards(picks):
    out = []
    for name, why, q in picks:
        out.append(f'''<li class="rl-pick">
        <h3 class="rl-pick__name">{e(name)}</h3>
        <p class="rl-pick__why">{e(why)}</p>
        <a class="rl-pick__btn" href="{e(amz(q))}" target="_blank" rel="sponsored nofollow noopener">See options on Amazon {EXT}</a>
      </li>''')
    return f'<ul class="rl-picks" role="list">{"".join(out)}</ul>'

DISC_NOTE = f'<p class="rl-disc-note"><strong>Disclosure:</strong> RikLoot is a participant in the Amazon Associates Programme. {e(DISCLOSURE)} Links to Amazon on this page are affiliate links — buying through them costs you nothing extra. <a href="disclosure.html">How we earn</a>.</p>'

# ---------------- HOME ----------------
chips = ''.join(f'<a class="rl-chip" href="guide-{g["slug"]}.html">{e(g["name"])}</a>' for g in GUIDES[:5])
HERO = f'''<section class="rl-hero" aria-labelledby="hero-h">
  {dots('heroDots', '#fff', 'rl-dots')}
  <div class="rl-wrap">
    <div class="rl-grid">
      <div class="rl-copy">
        <span class="rl-badge"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" style="color: var(--rl-accent)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>Useful finds, honestly picked</span>
        <h1 class="rl-title" id="hero-h">Grab the <span>good stuff.</span> Skip the hunt.</h1>
        <p class="rl-sub">Plain-language buying guides for kitchen helpers, storage, crafts, décor and everyday essentials — so you know exactly what to look for before you buy.</p>
        <div class="rl-ctas">
          <a class="rl-btn rl-btn--primary" href="guides.html">Read the guides {ARROW}</a>
          <a class="rl-btn rl-btn--ghost" href="#shop">See quick picks</a>
        </div>
        <div class="rl-trust">
          <span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" style="color: var(--rl-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/></svg>Independent picks</span>
          <span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" style="color: var(--rl-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16v16H4z"/><path d="M8 9h8M8 13h8M8 17h5"/></svg>Plain-language advice</span>
          <span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" style="color: var(--rl-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/></svg>Updated regularly</span>
        </div>
      </div>
      <svg class="rl-art" viewBox="0 0 560 560" role="img" aria-label="A location pin holding a parcel on a dotted route from a shop shelf to a house" xmlns="http://www.w3.org/2000/svg">
        <circle cx="280" cy="240" r="215" fill="#fff" opacity=".05"/>
        <path class="rl-route-flow" d="M58 488 C150 540 200 450 280 470 S420 545 502 482" fill="none" stroke="var(--rl-accent)" stroke-width="8" stroke-dasharray="0.1 18" stroke-linecap="round"/>
        <circle cx="58" cy="488" r="30" fill="#fff"/>
        <g fill="none" stroke="var(--rl-ground)" stroke-width="2.4" stroke-linecap="round"><path d="M44 480h28M44 496h28M44 472v32M72 472v32"/></g>
        <rect x="48" y="483" width="7" height="9" fill="var(--rl-pop)"/><rect x="59" y="485" width="9" height="7" fill="var(--rl-accent)"/>
        <text x="58" y="540" text-anchor="middle" font-family="Outfit, sans-serif" font-size="15" font-weight="600" fill="#D5DDEE">Good finds</text>
        <circle cx="502" cy="482" r="30" fill="var(--rl-accent)"/>
        <g fill="none" stroke="var(--rl-ground)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M488 484l14-12 14 12"/><path d="M492 481v14h20v-14"/><path d="M499 495v-7h6v7"/></g>
        <text x="502" y="534" text-anchor="middle" font-family="Outfit, sans-serif" font-size="15" font-weight="600" fill="#D5DDEE">Your home</text>
        <ellipse class="rl-shadow" cx="280" cy="474" rx="46" ry="9" fill="#000" opacity=".25"/>
        <g class="rl-pin">
          <path d="M280 466 C222 392 132 334 132 232 A148 148 0 1 1 428 232 C428 334 338 392 280 466 Z" fill="var(--rl-pop)"/>
          <path d="M176 168 C196 132 226 112 262 106" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="9" stroke-linecap="round"/>
          <circle cx="280" cy="232" r="104" fill="#fff"/>
          <g transform="rotate(-6 280 236)">
            <rect x="220" y="204" width="120" height="88" rx="6" fill="var(--rl-accent)"/>
            <rect x="210" y="184" width="140" height="28" rx="6" fill="#E59A00"/>
            <rect x="272" y="184" width="16" height="108" fill="var(--rl-ground)"/>
            <rect x="232" y="252" width="30" height="22" rx="3" fill="#FFF6E6"/>
            <path d="M237 259h20M237 266h13" stroke="var(--rl-ground)" stroke-width="2" stroke-linecap="round"/>
            <path d="M280 184 C262 160 246 166 254 180 M280 184 C298 160 314 166 306 180" fill="none" stroke="var(--rl-ground)" stroke-width="3.5" stroke-linecap="round"/>
          </g>
        </g>
        <g class="rl-tile rl-tile--1"><circle cx="86" cy="118" r="40" fill="#22375F"/><g fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M70 104h24v20a8 8 0 0 1-8 8h-8a8 8 0 0 1-8-8z"/><path d="M94 109h4a5 5 0 0 1 0 10h-4"/></g><path d="M78 96c0-4 4-4 4-8M86 96c0-4 4-4 4-8" fill="none" stroke="var(--rl-accent)" stroke-width="2.6" stroke-linecap="round"/></g>
        <g class="rl-tile rl-tile--2"><circle cx="478" cy="94" r="40" fill="#22375F"/><path d="M466 104h24l-4 18h-16z" fill="none" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/><path d="M478 104V88M478 94c-8 0-12-6-12-10 6 0 12 3 12 10zM478 90c8 0 12-6 12-10-6 0-12 3-12 10z" fill="none" stroke="#7FD1A8" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>
        <g class="rl-tile rl-tile--3"><circle cx="506" cy="300" r="36" fill="#22375F"/><path d="M494 300l8-18h8l8 18z" fill="none" stroke="var(--rl-accent)" stroke-width="2.6" stroke-linejoin="round"/><path d="M506 300v12M498 314h16" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></g>
        <g class="rl-tile rl-tile--4"><circle cx="52" cy="318" r="36" fill="#22375F"/><g fill="none" stroke="var(--rl-pop)" stroke-width="2.6" stroke-linecap="round"><circle cx="52" cy="318" r="14"/><path d="M42 308c6 4 14 4 20 0M40 320c8 4 16 4 24 0"/></g><path d="M64 330l10 10" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></g>
        <path class="rl-twinkle" fill="var(--rl-accent)" d="M176 70l4 10 10 4-10 4-4 10-4-10-10-4 10-4z"/>
        <path class="rl-twinkle rl-twinkle--2" fill="var(--rl-accent)" d="M410 410l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"/>
        <path class="rl-twinkle rl-twinkle--3" fill="#fff" d="M470 200l2.5 6 6 2.5-6 2.5-2.5 6-2.5-6-6-2.5 6-2.5z"/>
      </svg>
    </div>
    <nav class="rl-chips" aria-label="Buying guides">{chips}</nav>
  </div>
</section>'''

tab_btns = ''.join(f'<button type="button" class="rl-tab" role="tab" id="rl-tab-{g["slug"]}" aria-controls="rl-panel-{g["slug"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span class="rl-tab__dot" aria-hidden="true"></span>{e(g["tab"])}</button>' for i, g in enumerate(GUIDES))
panels = ''.join(f'''<div class="rl-panel" role="tabpanel" id="rl-panel-{g["slug"]}" aria-labelledby="rl-tab-{g["slug"]}" tabindex="0"{"" if i == 0 else " hidden"}>
      {pick_cards(g["picks"][:3])}
      <div class="rl-panel__foot"><a class="button button--secondary" href="guide-{g["slug"]}.html">Read the full {e(g["name"].lower())} guide {ARROW}</a></div>
    </div>''' for i, g in enumerate(GUIDES))
SHOWCASE = f'''<section id="shop" class="rl-show rl-section color-scheme-1" data-rl-tabs>
  <div class="rl-container">
    <div class="rl-head reveal"><div><h2 class="rl-head__title">Quick picks</h2><p class="rl-head__sub">A few of the most useful things from each guide, with a short reason why.</p></div></div>
    <div class="rl-tabs" role="tablist" aria-label="Quick picks by category">{tab_btns}</div>
    {panels}
    {DISC_NOTE}
  </div>
</section>'''

guide_cards = [(g['name'], g['short'], g['art'], g['tone'], g['slug'] == 'gifts', f'guide-{g["slug"]}.html') for g in GUIDES]
article_cards = [(a['name'], a['short'], a['art'], a['tone'], i in (0, 5), f'guide-{a["slug"]}.html') for i, a in enumerate(ARTICLES)]
LATEST = cat_grid(article_cards, 'Latest articles', 'Practical how-tos for real situations — first kitchens, winter, work-from-home and more.', ('guides.html#latest', 'All articles'), 'scheme-4', (72, 72), 'latest')
home_cards = [(g['name'], c, g['art'], g['tone'], w, h) for g, (_, c, _, _, w, h) in zip(GUIDES, guide_cards)]
HOW = steps([('We research', 'We read specifications, compare materials and go through buyer reviews to learn what really matters.'),
             ('We write it up', 'Each guide explains what to look for and what to avoid, in plain language.'),
             ('You choose', 'Use the guide to decide what suits your home, space and budget.'),
             ('You buy on Amazon', 'Our links take you to Amazon India, where you check the latest price, delivery and returns.')],
            'How RikLoot works', 'We do the homework so you can buy with confidence.')
home_body = '\n'.join([
  HERO,
  marquee([g['name'] for g in GUIDES], 'yellow', tilt=True),
  cat_grid(home_cards, 'Buying guides by category', 'From the kitchen counter to the craft table — pick a shelf and start reading.', ('guides.html', 'All guides'), 'scheme-1', (72, 56)),
  SHOWCASE,
  LATEST,
  HOW,
])

# ---------------- GUIDES INDEX ----------------
guides_body = '\n'.join([
  page_hero('Buying guides', 'Practical, plain-language guides to help you choose things that actually get used. Pick a category to start.', 'pin', 'scheme-3', [('index.html', 'Home'), ('', 'Guides')]),
  cat_grid(guide_cards, 'Guides by category', 'Everything you need to know before buying, one category at a time.', None, 'scheme-1', (64, 56), 'all-guides'),
  LATEST,
])

# ---------------- GUIDE PAGES ----------------
def guide_page(g):
    same = [o for o in ALL if o is not g and o.get('kind') == g.get('kind')]
    rest = [o for o in ALL if o is not g and o.get('kind') != g.get('kind')]
    others = ''.join(f'<li><a href="guide-{o["slug"]}.html">{e(o["name"])}</a></li>' for o in (same + rest)[:8])
    secs = ''.join(f'<h2>{e(h)}</h2>{body}' for h, body in g['sections'])
    return '\n'.join([
      page_hero(g['title'], g['sub'], g['art'], 'scheme-2', [('index.html', 'Home'), ('guides.html', 'Guides'), ('', g['name'])]),
      f'''<section class="rl-rp rl-section color-scheme-1">
  <div class="rl-container"><div class="rl-rp__grid">
    <aside class="rl-rp__aside">
      <nav class="rl-rp__box" aria-label="On this page" data-rl-toc-wrap hidden><p class="rl-rp__box-title">On this page</p><ol class="rl-rp__toc" data-rl-toc></ol></nav>
      <div class="rl-rp__box"><p class="rl-rp__box-title">More guides</p><ul class="rl-rp__policies" role="list">{others}</ul></div>
    </aside>
    <div>
      <span class="rl-pill rl-rp__updated">Last updated: {UPDATED}</span>
      {DISC_NOTE}
      <article class="rl-prose" data-rl-prose>
        {g['intro']}
        {secs}
        <h2>Our quick picks</h2>
        <p>Use these as a starting point. Each link opens Amazon India with options that match what this guide recommends — compare ratings, recent reviews and the latest price before you buy.</p>
      </article>
      {pick_cards(g['picks'])}
      <div class="rl-prose"><h2>Frequently asked questions</h2></div>
      <div class="rl-faq">{faq(g['faqs'])}</div>
      <p class="rl-guide-foot">Have a question this guide didn’t answer? <a href="contact.html#form">Ask us</a> — we read every message and use them to improve our guides.</p>
    </div>
  </div></div>
</section>''',
    ])

# ---------------- ABOUT ----------------
VAL_IC = {
 'star': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
 'tag': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12l-8 8-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
 'pin': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'chat': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
}
values = [('star', 'Handpicked, not random', 'We only recommend types of products that are genuinely useful, and we explain why.'),
          ('tag', 'Honest about how we earn', 'Some links are Amazon affiliate links. They never change what we recommend or what you pay.'),
          ('pin', 'Made for Indian homes', 'Our advice considers Indian kitchens, climate, power supply and budgets.'),
          ('chat', 'Real people, real help', 'Have a question or a guide you want us to write? Message us and a real person will reply.')]
vals = ''.join(f'<li class="rl-value reveal" style="--animation-order: {i};"><span class="rl-value__icon" aria-hidden="true">{VAL_IC[icn]}</span><h3>{e(t)}</h3><p>{e(x)}</p></li>' for i, (icn, t, x) in enumerate(values, 1))
ABOUT = f'''<section class="rl-about rl-section color-scheme-1">
  <div class="rl-container">
    <div class="rl-about__story">
      <div class="rl-about__media reveal">{art('team')}<span class="rl-about__tag">Est. 2026</span></div>
      <div>
        <h2>Good finds shouldn't be hard to find</h2>
        <div class="rl-about__body"><p>RikLoot started with a simple frustration: the genuinely useful things — a clever kitchen tool, a drawer organiser that actually fits, a craft kit that is right for a beginner — are buried under thousands of listings that all look the same.</p><p>So we started writing the guides we wished existed. Each one explains what to look for, which specifications matter, which mistakes to avoid and what suits an Indian home, in plain language. We cover kitchen helpers, storage, crafts, home décor, gadgets, gifts and everyday essentials.</p><p>When you are ready to buy, our links take you to Amazon India, where you can check the latest price, delivery and return options. If you buy through those links we may earn a small commission, at no extra cost to you. That is how we keep the guides free.</p></div>
        <p class="rl-about__sign">— Team RikLoot</p>
      </div>
    </div>
    <div class="rl-values">
      <div class="rl-head"><h2 class="rl-head__title">What we promise</h2></div>
      <ul class="rl-values__grid" role="list">{vals}</ul>
    </div>
    <div class="rl-about__cta"><h3>Ready to find some good stuff?</h3><a class="button" href="guides.html">Browse the guides</a></div>
  </div>
</section>'''
GTK = f'''<section class="rl-gtk rl-section color-scheme-1">
  <div class="rl-container">
    <div class="rl-head"><h2 class="rl-head__title">Good to know</h2></div>
    <div class="rl-faq rl-gtk__box">{faq([
      ('Does RikLoot sell products?', '<p>No. RikLoot is a buying-guide website. When you click a product link you go to Amazon India, and your purchase is made on Amazon.</p>'),
      ('How does RikLoot make money?', '<p>RikLoot is a participant in the Amazon Associates Programme. If you buy through our links we may earn a small commission, at no extra cost to you. See our <a href="disclosure.html">affiliate disclosure</a>.</p>'),
      ('Who handles delivery, payment and returns?', '<p>Amazon and the seller you buy from. Check the delivery and return details on the Amazon product page before ordering.</p>'),
      ('Why don’t you show prices?', '<p>Prices on Amazon change often, so we link you straight to Amazon where you always see the current price.</p>'),
      ('How do I reach you?', '<p>Use our <a href="contact.html">Contact page</a> or the email in the footer. We reply within one business day.</p>'),
    ], open_first=True)}</div>
  </div>
</section>'''
about_body = '\n'.join([
  page_hero('About RikLoot', 'Plain-language buying guides for the little things that make life easier — written for Indian homes.', 'pin', 'scheme-3', [('index.html', 'Home'), ('', 'About')]),
  ABOUT,
  cat_grid(home_cards[:4], "What we write about", 'A little bit of everything, explained with a lot of care.', ('guides.html', 'All guides'), 'scheme-4', (72, 72)),
  HOW,
  GTK,
])

# ---------------- CONTACT ----------------
CONTACT = f'''<section class="rl-contact rl-section color-scheme-1">
  <div class="rl-container">
    <div class="rl-c__grid">
      <div>
        <h2>We're here to help</h2>
        <p class="rl-c__intro">Questions about a guide, a product suggestion, or a topic you want us to cover? Reach us any way you like.</p>
        <ul class="rl-c__cards" role="list">
          <li data-cfg-item hidden><a class="rl-c__card rl-c__card--wa" data-cfg-href="whatsapp" href="#" target="_blank" rel="noopener"><span class="rl-c__ic" aria-hidden="true">{ic(IC_WA)}</span><span><span class="rl-c__label">WhatsApp</span><span class="rl-c__value" data-cfg="whatsapp"></span></span></a></li>
          <li data-cfg-item><a class="rl-c__card" data-cfg-href="email" href="mailto:{EMAIL}"><span class="rl-c__ic" aria-hidden="true">{ic(IC_MAIL)}</span><span><span class="rl-c__label">Email</span><span class="rl-c__value" data-cfg="email">{EMAIL}</span></span></a></li>
          <li data-cfg-item><a class="rl-c__card" data-cfg-href="phone" href="tel:+917510380758"><span class="rl-c__ic" aria-hidden="true">{ic(IC_PHONE)}</span><span><span class="rl-c__label">Phone</span><span class="rl-c__value" data-cfg="phone">+91 75103 80758</span></span></a></li>
          <li data-cfg-item><div class="rl-c__card"><span class="rl-c__ic" aria-hidden="true">{ic(IC_CLOCK)}</span><span><span class="rl-c__label">Support hours</span><span class="rl-c__value" data-cfg="hours">Mon–Sat, 10 am – 6 pm IST</span></span></div></li>
          <li data-cfg-item hidden><div class="rl-c__card"><span class="rl-c__ic" aria-hidden="true">{ic(IC_PIN)}</span><span><span class="rl-c__label">Address</span><span class="rl-c__value" data-cfg="address"></span></span></div></li>
        </ul>
      </div>
      <div class="rl-c__form reveal" id="form">
        <h2>Send us a message</h2>
        <form id="RlContactForm" novalidate>
          <p data-msg hidden tabindex="-1" role="status"></p>
          <div class="rl-c__row rl-c__row--2">
            <div><label for="RlName">Your name</label><input class="rl-c__input" id="RlName" type="text" name="name" autocomplete="name"></div>
            <div><label for="RlEmail">Email <span aria-hidden="true">*</span></label><input class="rl-c__input" id="RlEmail" type="email" name="email" autocomplete="email" required spellcheck="false" autocapitalize="off"></div>
          </div>
          <div class="rl-c__row rl-c__row--2">
            <div><label for="RlPhone">Phone</label><input class="rl-c__input" id="RlPhone" type="tel" name="phone" autocomplete="tel" pattern="[0-9\\-\\+\\s]*"></div>
            <div><label for="RlTopic">Topic</label>
              <select class="rl-c__input" id="RlTopic" name="topic"><option>Question about a guide</option><option>Suggest a guide or product</option><option>Correction or feedback</option><option>Partnership</option><option>Something else</option></select></div>
          </div>
          <div class="rl-c__row"><div><label for="RlBody">Message <span aria-hidden="true">*</span></label><textarea class="rl-c__input" id="RlBody" name="body" required></textarea></div></div>
          <button type="submit" class="rl-c__submit">Send message</button>
          <p class="rl-c__note">We usually reply within one working day.</p>
        </form>
      </div>
    </div>
    <div class="rl-faq">
      <div class="rl-head"><h2 class="rl-head__title">Quick answers</h2></div>
      {faq([
        ('I bought something through a RikLoot link. Who do I contact about my order?', '<p>Orders, delivery, payments and returns are handled by Amazon and the seller. Go to <em>Your Orders</em> in your Amazon account for help with any order.</p>'),
        ('Can you recommend something for my specific needs?', '<p>Yes — send us a message with what you need, your space and your budget, and we will point you in the right direction.</p>'),
        ('Do brands pay you to be featured?', '<p>No. We do not accept payment for placement. We earn only through affiliate commissions, as explained in our <a href="disclosure.html">affiliate disclosure</a>.</p>'),
        ('I found a mistake in a guide.', '<p>Thank you! Please tell us using the form, and we will check and correct it.</p>'),
      ])}
    </div>
  </div>
</section>'''
contact_body = '\n'.join([
  page_hero('Contact us', 'Real people, quick replies. Tell us how we can help.', 'gifts', 'scheme-3', [('index.html', 'Home'), ('', 'Contact')]),
  CONTACT,
])

# ---------------- POLICY PAGES ----------------
def rich(prose):
    return f'''<section class="rl-rp rl-section color-scheme-1">
  <div class="rl-container"><div class="rl-rp__grid">
    <aside class="rl-rp__aside">
      <nav class="rl-rp__box" aria-label="On this page" data-rl-toc-wrap hidden><p class="rl-rp__box-title">On this page</p><ol class="rl-rp__toc" data-rl-toc></ol></nav>
      <div class="rl-rp__box"><p class="rl-rp__box-title">Policies</p><ul class="rl-rp__policies" role="list"><li><a href="disclosure.html">Affiliate disclosure</a></li><li><a href="privacy.html">Privacy policy</a></li><li><a href="terms.html">Terms of use</a></li><li><a href="contact.html">Contact us</a></li></ul></div>
    </aside>
    <div>
      <span class="rl-pill rl-rp__updated">Last updated: {UPDATED}</span>
      <article class="rl-prose" data-rl-prose>{prose}</article>
    </div>
  </div></div>
</section>'''

DISCLOSURE_PROSE = f'''<h2>Our affiliate relationship</h2>
<p>RikLoot is a participant in the Amazon Associates Programme, an affiliate advertising programme designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.in.</p>
<p><strong>{e(DISCLOSURE)}</strong></p>
<h2>What this means for you</h2>
<ul><li>When you click a link to Amazon on RikLoot and then make a purchase, we may receive a small commission.</li><li>You do not pay anything extra. The price you pay on Amazon is the same whether or not you use our link.</li><li>Links that may earn us a commission are marked with “See options on Amazon” and open Amazon India in a new tab.</li></ul>
<h2>How we choose what to recommend</h2>
<p>Our guides are written to help you choose well, not to sell you more. We recommend types of products based on materials, specifications, safety marks and what buyers report after long-term use. Commissions do not influence what we recommend, and brands cannot pay to be featured.</p>
<h2>Prices and availability</h2>
<p>We do not show prices on RikLoot because they change often. Product prices and availability are accurate as of the date and time indicated on Amazon and are subject to change. Any price and availability information displayed on Amazon at the time of purchase will apply to the purchase of the product.</p>
<h2>Orders, delivery and returns</h2>
<p>RikLoot does not sell, ship or handle returns for any product. All purchases are made on Amazon and are covered by Amazon’s and the seller’s terms, delivery and return policies.</p>
<h2>Questions</h2>
<p>If you have any questions about this disclosure, write to us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'''

PRIVACY_PROSE = f'''<h2>Who we are</h2>
<p>RikLoot (“we”, “us”) publishes buying guides at this website. You can reach us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Information we collect</h2>
<p>RikLoot does not have user accounts and does not run its own analytics or advertising trackers. We only receive personal information when you choose to send it to us:</p>
<ul><li><strong>Contact form and email</strong> — the contact and newsletter forms open your own email app. We receive whatever you include in the email you send, such as your name, email address, phone number and message.</li></ul>
<h2>How we use it</h2>
<p>We use the information you send only to reply to you, to add you to our mailing list if you asked to join, and to improve our guides. We do not sell or rent your personal information.</p>
<h2>Third-party services</h2>
<ul><li><strong>Amazon</strong> — when you click a link to Amazon, Amazon may set cookies to track the referral so that we can earn a commission. Amazon’s own privacy notice applies on their website.</li><li><strong>Website hosting</strong> — our hosting provider may record standard server logs (such as IP address, browser type and the pages requested) for security and reliability.</li><li><strong>Google Fonts</strong> — our pages load fonts from Google, which receives your IP address when the font files are requested.</li></ul>
<h2>Mailing list</h2>
<p>If you join our mailing list, you can unsubscribe at any time by replying to any of our emails or writing to us. We will remove you promptly.</p>
<h2>Your rights</h2>
<p>You can ask us to access, correct or delete the personal information you have sent us by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The date at the top of this page shows when it was last changed.</p>'''

TERMS_PROSE = f'''<h2>About these terms</h2>
<p>By using RikLoot you agree to these terms. If you do not agree, please do not use the website.</p>
<h2>Our content</h2>
<p>Our guides are for general information only. We work to keep them accurate and up to date, but products, specifications and prices change. Always check the product listing, safety information and the manufacturer’s instructions before buying or using a product.</p>
<h2>We are not a seller</h2>
<p>RikLoot does not sell products. Links on our website take you to Amazon India, where any purchase is a contract between you and Amazon or the seller. Payment, delivery, warranty and returns are governed by their terms.</p>
<h2>Affiliate links</h2>
<p>Some links on RikLoot are affiliate links. {e(DISCLOSURE)} See our <a href="disclosure.html">affiliate disclosure</a> for details.</p>
<h2>Intellectual property</h2>
<p>The text, illustrations and design of RikLoot belong to us. You may share links to our pages, but please do not copy our content without permission. Product names and trademarks belong to their respective owners.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, RikLoot is not liable for any loss arising from the use of our content or from products bought through third-party websites.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of India.</p>
<h2>Contact</h2>
<p>Questions about these terms? Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'''

def pol(title, sub, prose):
    return '\n'.join([page_hero(title, sub, None, 'scheme-2', [('index.html', 'Home'), ('', title)]), rich(prose)])

nf_body = f'''<section class="rl-404 rl-section color-scheme-1"><div class="rl-container">
  {art('pin')}
  <h1>This parcel took a wrong turn</h1>
  <p>We couldn't find that page. Let's get you back on the route.</p>
  <a class="button" href="index.html">Back to home</a>
</div></section>'''

pages = {
  'index.html': ('RikLoot — Honest buying guides for Indian homes', 'Plain-language buying guides for kitchen helpers, storage, crafts, décor, gadgets and everyday essentials.', home_body, 'index.html'),
  'guides.html': ('Buying guides — RikLoot', 'Practical, plain-language buying guides for Indian homes.', guides_body, 'guides.html'),
  'about.html': ('About RikLoot', 'Plain-language buying guides for the little things that make life easier.', about_body, 'about.html'),
  'contact.html': ('Contact us — RikLoot', 'Questions about a guide or a product suggestion? Get in touch.', contact_body, 'contact.html'),
  'disclosure.html': ('Affiliate disclosure — RikLoot', 'How RikLoot earns money through the Amazon Associates Programme.', pol('Affiliate disclosure', 'How RikLoot earns money, in plain language.', DISCLOSURE_PROSE), ''),
  'privacy.html': ('Privacy policy — RikLoot', 'How RikLoot handles your information.', pol('Privacy policy', 'What we collect, why, and what we never do with it.', PRIVACY_PROSE), ''),
  'terms.html': ('Terms of use — RikLoot', 'The terms for using the RikLoot website.', pol('Terms of use', 'The fine print, written to be read.', TERMS_PROSE), ''),
  '404.html': ('Page not found — RikLoot', 'This page could not be found.', nf_body, ''),
}
for g in ALL:
    pages[f'guide-{g["slug"]}.html'] = (f'{g["title"]} — RikLoot', g['sub'], guide_page(g), 'guides.html')

for fn, (t, d, b, cur) in pages.items():
    with open(os.path.join(OUT, fn), 'w', encoding='utf-8') as f:
        f.write(page(t, d, b, cur))
print('wrote', len(pages), 'pages')
