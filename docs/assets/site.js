/* =========================================================
   RikLoot static site
   ---------------------------------------------------------
   EDIT YOUR CONTACT DETAILS HERE. Everything on the site
   (footer, contact page, forms) reads from this one place.
   Leave a value as '' to hide it.
   ========================================================= */
var RIKLOOT = {
  email: 'rickloot.official@gmail.com', // support email — contact + newsletter forms send here
  whatsapp: '',                       // with country code, e.g. '+91 98765 43210'
  phone: '+91 75103 80758',            // e.g. '+91 98765 43210'
  hours: 'Mon–Sat, 10 am – 6 pm IST',
  address: '',
  grievance: ''                       // grievance officer name + email (India e-commerce rules)
};

(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var C = RIKLOOT;
  var digits = function (s) { return String(s).replace(/[^\d+]/g, ''); };

  /* ---- Fill contact details from config ---- */
  document.querySelectorAll('[data-cfg]').forEach(function (el) {
    var key = el.getAttribute('data-cfg');
    var val = C[key];
    var holder = el.closest('[data-cfg-item]') || el;
    if (!val) { holder.hidden = true; return; }
    holder.hidden = false;
    el.textContent = val;
    if (el.tagName === 'A') {
      if (key === 'email') el.href = 'mailto:' + val;
      if (key === 'phone') el.href = 'tel:' + digits(val);
      if (key === 'whatsapp') el.href = 'https://wa.me/' + digits(val).replace('+', '');
    }
  });
  document.querySelectorAll('[data-cfg-href="whatsapp"]').forEach(function (el) {
    var li = el.closest('[data-cfg-item]') || el;
    if (!C.whatsapp) { li.hidden = true; return; }
    el.href = 'https://wa.me/' + digits(C.whatsapp).replace('+', '');
  });
  document.querySelectorAll('[data-cfg-href="email"]').forEach(function (el) {
    if (C.email) el.href = 'mailto:' + C.email;
  });
  document.querySelectorAll('[data-cfg-href="phone"]').forEach(function (el) {
    var li = el.closest('[data-cfg-item]') || el;
    if (!C.phone) { li.hidden = true; return; }
    el.href = 'tel:' + digits(C.phone);
  });

  /* ---- Year ---- */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---- Mobile nav ---- */
  var burger = document.querySelector('.rl-burger');
  var nav = document.getElementById('rl-nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); burger.focus(); }
    });
  }

  /* ---- Header shadow on scroll ---- */
  var header = document.querySelector('.rl-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 4); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---- Tabs (category showcase) ---- */
  document.querySelectorAll('[data-rl-tabs]').forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (n) { e.preventDefault(); select(n); n.focus(); }
      });
    });
    // Category cards / chips can open a specific tab: href="#shop" data-tab="rl-tab-kitchen"
    document.querySelectorAll('[data-tab]').forEach(function (a) {
      a.addEventListener('click', function () {
        var t = document.getElementById(a.getAttribute('data-tab'));
        if (t && root.contains(t)) select(t);
      });
    });
  });

  /* ---- Reveal on scroll ---- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---- "On this page" table of contents (policy pages) ---- */
  var prose = document.querySelector('[data-rl-prose]');
  var list = document.querySelector('[data-rl-toc]');
  var wrap = document.querySelector('[data-rl-toc-wrap]');
  if (prose && list && wrap) {
    var heads = prose.querySelectorAll('h2');
    if (heads.length >= 2) {
      var links = [];
      heads.forEach(function (h, i) {
        if (!h.id) h.id = 'sec-' + (i + 1) + '-' + h.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40);
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = '#' + h.id;
        a.textContent = h.textContent.trim();
        li.appendChild(a); list.appendChild(li); links.push(a);
      });
      wrap.hidden = false;
      if ('IntersectionObserver' in window) {
        var tio = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) links.forEach(function (l) { l.classList.toggle('is-active', l.getAttribute('href') === '#' + en.target.id); });
          });
        }, { rootMargin: '-20% 0px -70% 0px' });
        heads.forEach(function (h) { tio.observe(h); });
      }
    }
  }

  /* ---- Forms: GitHub Pages has no server, so forms open the
          visitor's email app with the message pre-filled. ---- */
  function mailto(subject, body) {
    return 'mailto:' + encodeURIComponent(C.email).replace('%40', '@') +
      '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }
  function showMsg(form, cls, text) {
    var m = form.querySelector('[data-msg]');
    if (!m) return;
    m.className = cls; m.textContent = text; m.hidden = false; m.focus();
  }

  var contact = document.getElementById('RlContactForm');
  if (contact) {
    contact.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!contact.reportValidity()) return;
      var f = contact.elements;
      var topic = f.topic.value;
      var body = [
        f.body.value, '',
        '— — —',
        'Name: ' + (f.name.value || '-'),
        'Email: ' + f.email.value,
        'Phone: ' + (f.phone.value || '-')
      ].join('\n');
      window.location.href = mailto('RikLoot: ' + topic, body);
      showMsg(contact, 'rl-c__msg', 'Your email app should open with your message ready to send. If it didn’t, write to us at ' + C.email + '.');
    });
  }

  document.querySelectorAll('[data-rl-newsletter]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var email = form.querySelector('input[type="email"]').value;
      window.location.href = mailto('Newsletter sign-up', 'Please add me to the RikLoot list: ' + email);
      showMsg(form, 'rl-nl__msg', 'Almost there! Hit send in your email app and you’re on the list.');
    });
  });
})();
