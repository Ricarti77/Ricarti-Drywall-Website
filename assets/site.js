/* Ricarti Drywall — site search (works on every page) */
(function () {
  var dlg = document.getElementById('rd-search');
  var input = document.getElementById('rd-q');
  var list = document.getElementById('rd-res');
  var sugg = document.getElementById('rd-sugg');
  var index = null, loading = null;
  var LG = (document.documentElement.lang || 'en').slice(0, 2);
  var L = ({
    pt: { idx: '/pt/search-index.json', page: '/pt/busca', none: 'Nada encontrado para “%s”. Tente “espuma”, “nível 5” ou “acústico”, ou ligue para ' },
    es: { idx: '/es/search-index.json', page: '/es/buscar', none: 'No encontramos nada para “%s”. Pruebe “espuma”, “Nivel 5” o “insonorización”, o llame al ' },
    fr: { idx: '/fr/search-index.json', page: '/fr/recherche', none: 'Aucun résultat pour « %s ». Essayez « mousse », « niveau 5 » ou « insonorisation », ou appelez au ' },
    it: { idx: '/it/search-index.json', page: '/it/cerca', none: 'Nessun risultato per “%s”. Provate “schiuma”, “Livello 5” o “insonorizzazione”, oppure chiamate il ' }
  })[LG] || { idx: '/search-index.json', page: '/search', none: 'Nothing matched “%s”. Try “spray foam”, “Level 5” or “soundproofing”, or call ' };

  function load() {
    if (index) return Promise.resolve(index);
    if (!loading) loading = fetch(L.idx).then(function (r) { return r.json(); }).then(function (j) { index = j; return j; });
    return loading;
  }
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[–—]/g, '-'); }
  var STEM = { pt: /(acoes|acao|mente|cos|cas|cao|oes|os|as|es|o|a|e|s)$/, es: /(aciones|acion|ciones|cion|mente|es|os|as|o|a|e|s)$/,
               fr: /(ations?|ements?|euses?|eurs?|ees?|es|e|s|x)$/, it: /(azioni|azione|zioni|zione|mente|i|e|o|a)$/, en: /(ations?|ing|ion|ers|ed|es|s|e)$/ };
  function stem(t) { return t.length > 5 ? t.replace(STEM[LG] || STEM.en, '') : t; }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var STOP = { de: 1, da: 1, do: 1, das: 1, dos: 1, para: 1, com: 1, um: 1, uma: 1, que: 1, como: 1, em: 1, no: 1, na: 1, e: 1, o: 1, os: 1, as: 1, the: 1, and: 1, for: 1, you: 1, how: 1, what: 1, does: 1, with: 1, are: 1, can: 1, do: 1, of: 1, to: 1, in: 1, a: 1, my: 1, is: 1, an: 1, or: 1 };

  function search(q) {
    var terms = norm(q).split(/[^a-z0-9]+/).filter(function (t) { return t && !STOP[t]; }).map(stem);
    if (!terms.length) return [];
    var out = [];
    index.forEach(function (p) {
      var T = norm(p.t), D = norm(p.d), X = norm(p.x), score = 0, all = true;
      terms.forEach(function (t) {
        var s = (T.indexOf(t) > -1 ? 8 : 0) + (D.indexOf(t) > -1 ? 4 : 0) + (X.split(t).length - 1 > 0 ? Math.min(X.split(t).length - 1, 6) : 0);
        if (!s) all = false;
        score += s;
      });
      if (all && score) out.push({ p: p, s: score });
    });
    out.sort(function (a, b) { return b.s - a.s; });
    return out.slice(0, 8).map(function (o) { return { p: o.p, terms: terms }; });
  }
  function snippet(p, terms) {
    var X = norm(p.x), at = -1;
    for (var i = 0; i < terms.length && at < 0; i++) at = X.indexOf(terms[i]);
    var raw = at < 0 ? p.d : p.x.slice(Math.max(0, at - 70), at + 150);
    var s = esc((at > 70 ? '… ' : '') + raw + (at < 0 ? '' : ' …'));
    terms.forEach(function (t) { if (t.length > 2) s = s.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[a-z]*)', 'gi'), '<mark>$1</mark>'); });
    return s;
  }
  function render(q, ul, empty) {
    var r = search(q);
    if (!q.trim()) { ul.innerHTML = ''; if (empty) empty.hidden = false; return; }
    if (empty) empty.hidden = true;
    ul.innerHTML = r.length ? r.map(function (o) {
      return '<li><a href="' + o.p.u + '"><span class="u">' + esc(o.p.k) + '</span><span class="t">' + esc(o.p.t) + '</span><span class="s">' + snippet(o.p, o.terms) + '</span></a></li>';
    }).join('') : '<li class="rd-sugg">' + L.none.replace('%s', esc(q)) + '<a href="tel:+16474821139">(647) 482-1139</a>.</li>';
  }
  window.rdSearch = { load: load, render: render };

  if (!dlg) return;
  function open(e) {
    if (e) e.preventDefault();
    if (typeof dlg.showModal === 'function') dlg.showModal(); else { location.href = L.page; return; }
    input.focus(); input.select(); load().then(function () { render(input.value, list, sugg); });
  }
  document.querySelectorAll('[data-open-search]').forEach(function (b) { b.addEventListener('click', open); });
  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase();
    if ((e.key === '/' && tag !== 'input' && tag !== 'textarea') || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) open(e);
  });
  input.addEventListener('input', function () { load().then(function () { render(input.value, list, sugg); }); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  document.getElementById('rd-sclose').addEventListener('click', function () { dlg.close(); });
  // close the mobile menu when a link inside it is used
  document.querySelectorAll('.rd-mnav a').forEach(function (a) { a.addEventListener('click', function () { a.closest('details').open = false; }); });
})();

/* Ricarti Drywall — project photo album and per-project galleries (open in place, no redirect)
   Main album: <ul class="rd-album"> + triggers [data-lb="index"].
   Project galleries: <ul data-gallery-list="id"> + triggers [data-gallery="id"] (optional data-start). */
(function () {
  var main = document.querySelector('.rd-album');
  var lists = {};
  function read(ul) { return [].map.call(ul.querySelectorAll('li'), function (li) { return { src: li.getAttribute('data-src'), cap: li.textContent }; }); }
  if (main) lists._main = read(main);
  document.querySelectorAll('ul[data-gallery-list]').forEach(function (ul) { lists[ul.getAttribute('data-gallery-list')] = read(ul); });
  if (!Object.keys(lists).length) return;
  var L = ({
    pt: { close: 'Fechar', prev: 'Foto anterior', next: 'Próxima foto', of: ' de ', title: 'Álbum de obras' },
    es: { close: 'Cerrar', prev: 'Foto anterior', next: 'Foto siguiente', of: ' de ', title: 'Álbum de proyectos' },
    fr: { close: 'Fermer', prev: 'Photo précédente', next: 'Photo suivante', of: ' sur ', title: 'Album de projets' },
    it: { close: 'Chiudi', prev: 'Foto precedente', next: 'Foto successiva', of: ' di ', title: 'Album dei progetti' }
  })[(document.documentElement.lang || 'en').slice(0, 2)] || { close: 'Close', prev: 'Previous photo', next: 'Next photo', of: ' of ', title: 'Project album' };
  var items = [], i = 0, opener = null, dlg = document.createElement('dialog');
  dlg.className = 'rd-lbx'; dlg.setAttribute('aria-label', L.title);
  dlg.innerHTML = '<div class="rd-lbx-top"><span class="rd-lbx-n"></span><button type="button" class="rd-lbx-x">' + L.close + ' ✕</button></div>' +
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button type="button" class="rd-lbx-p" aria-label="' + L.prev + '">‹</button><button type="button" class="rd-lbx-f" aria-label="' + L.next + '">›</button>' +
    '<div class="rd-lbx-th" role="list"></div>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector('img'), cap = dlg.querySelector('figcaption'), n = dlg.querySelector('.rd-lbx-n'), th = dlg.querySelector('.rd-lbx-th');
  var prevB = dlg.querySelector('.rd-lbx-p'), nextB = dlg.querySelector('.rd-lbx-f');
  function load(list, title) {
    items = list; dlg.setAttribute('aria-label', title || L.title);
    th.innerHTML = items.map(function (it, k) { return '<button type="button" role="listitem" data-k="' + k + '" aria-label="' + it.cap.replace(/"/g, '&quot;') + '"><img src="' + it.src + '" alt="" loading="lazy"></button>'; }).join('');
    var single = items.length < 2; prevB.hidden = single; nextB.hidden = single; th.hidden = single;
  }
  function show(k) {
    i = (k + items.length) % items.length;
    img.src = items[i].src; img.alt = items[i].cap; cap.textContent = items[i].cap;
    n.textContent = (i + 1) + L.of + items.length;
    [].forEach.call(th.children, function (b, k2) { b.toggleAttribute('aria-current', k2 === i); });
    var cur = th.children[i]; if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'nearest', inline: 'center' });
    [i + 1, i - 1].forEach(function (k3) { var p = new Image(); p.src = items[(k3 + items.length) % items.length].src; });
  }
  function open(list, k, title, el) {
    load(list, title); show(k); opener = el || null;
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    document.documentElement.style.overflow = 'hidden';
  }
  dlg.addEventListener('close', function () { document.documentElement.style.overflow = ''; if (opener && opener.focus) opener.focus(); });
  document.querySelectorAll('[data-lb]').forEach(function (el) {
    el.addEventListener('click', function (e) { if (!lists._main) return; e.preventDefault(); open(lists._main, +el.getAttribute('data-lb'), L.title, el); });
  });
  document.querySelectorAll('[data-gallery]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      var id = el.getAttribute('data-gallery'); if (!lists[id]) return;
      e.preventDefault(); open(lists[id], +(el.getAttribute('data-start') || 0), el.getAttribute('data-gallery-title') || L.title, el);
    });
  });
  dlg.querySelector('.rd-lbx-x').addEventListener('click', function () { dlg.close(); });
  prevB.addEventListener('click', function () { show(i - 1); });
  nextB.addEventListener('click', function () { show(i + 1); });
  th.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) show(+b.getAttribute('data-k')); });
  dlg.addEventListener('keydown', function (e) { if (items.length < 2) return; if (e.key === 'ArrowLeft') show(i - 1); if (e.key === 'ArrowRight') show(i + 1); });
  var x0 = null;
  dlg.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  dlg.addEventListener('touchend', function (e) { if (x0 === null || items.length < 2) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1)); x0 = null; });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
})();

/* Ricarti Drywall — portfolio filters (all projects stay visible without JavaScript) */
(function () {
  var bar = document.querySelector('.rd-pf-filters');
  if (!bar) return;
  var cards = document.querySelectorAll('.rd-pf-item');
  var status = document.querySelector('.rd-pf-status');
  var grid = document.querySelector('.rd-pf-grid');
  bar.hidden = false;
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-filter]'); if (!b) return;
    var f = b.getAttribute('data-filter'), shown = 0;
    bar.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    cards.forEach(function (c) { var on = f === 'all' || (' ' + c.getAttribute('data-cats') + ' ').indexOf(' ' + f + ' ') > -1; c.hidden = !on; if (on) shown++; });
    if (grid) grid.classList.toggle('is-filtered', f !== 'all');
    if (status) status.textContent = status.getAttribute(shown === 1 ? 'data-one' : 'data-many').replace('%d', shown);
  });
})();

/* Concept D: header over hero, full-screen menu, services dropdown, language menu, reveals */
(function () {
  var root = document.documentElement; root.classList.add('js');
  var head = document.querySelector('.rd-head');
  if (head && head.classList.contains('rd-over')) {
    var solid = function () { head.classList.toggle('is-solid', window.scrollY > 80); };
    solid(); window.addEventListener('scroll', solid, { passive: true });
  }
  var mq = window.matchMedia('(max-width: 900px)');

  /* full-screen menu: scroll lock with position restore, focus trap, Esc, back button closes it */
  var menu = document.querySelector('.rd-menu');
  if (menu) {
    var panel = menu.querySelector('.rd-panel-m'), sum = menu.querySelector('summary'), bar = document.querySelector('.rd-mbar');
    var svcd = menu.querySelector('.rd-pm-svcd'), y = 0, locked = false, pushed = false, pending = null;
    var preY = null; menu.querySelector('summary').addEventListener('click', function () { if (!menu.open) preY = window.scrollY; }, true);
    function lock() { if (locked) return; locked = true; y = preY != null ? preY : window.scrollY; preY = null; document.documentElement.classList.add('rd-menu-open'); var b = document.body.style; b.position = 'fixed'; b.top = -y + 'px'; b.left = '0'; b.right = '0'; b.width = '100%'; }
    function unlock() { if (!locked) return; locked = false; document.documentElement.classList.remove('rd-menu-open'); var b = document.body.style; b.position = b.top = b.left = b.right = b.width = ''; window.scrollTo(0, y); }
    function close(viaHistory) {
      if (menu.open) menu.open = false;
      unlock();
      if (pushed && !viaHistory) { pushed = false; history.back(); } else { pushed = false; }
    }
    menu.addEventListener('toggle', function () {
      if (bar) bar.classList.toggle('is-hidden', menu.open);
      if (menu.open) {
        try { history.pushState({ rdMenu: 1 }, ''); pushed = true; } catch (e) {}
        lock();
        if (svcd) svcd.open = !mq.matches;
        var f = panel.querySelector('a,button'); if (f) f.focus();
      } else {
        close(false); sum.focus({ preventScroll: true });
      }
    });
    window.addEventListener('popstate', function () {
      if (pending) { var h = pending; pending = null; if (h.charAt(0) === '#') location.hash = h; else location.href = h; return; }
      if (menu.open) { pushed = false; menu.open = false; unlock(); }
    });
    panel.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]'); if (!a || e.metaKey || e.ctrlKey || e.shiftKey || a.target) return;
      var href = a.getAttribute('href');
      if (/^(tel:|mailto:|https?:)/.test(href)) { return; }
      e.preventDefault();
      var wasPushed = pushed; pushed = false; menu.open = false; unlock();
      var url = new URL(href, location.href), same = url.pathname === location.pathname && url.search === location.search;
      var target = same && url.hash ? url.hash : url.href;
      if (wasPushed) { pending = target; history.back(); setTimeout(function () { if (pending) { var p = pending; pending = null; if (p.charAt(0) === '#') location.hash = p; else location.href = p; } }, 400); }
      else if (target.charAt(0) === '#') location.hash = target; else location.href = target;
    });
    panel.querySelectorAll('[data-open-search]').forEach(function (b) { b.addEventListener('click', function () { close(false); }, true); });
    document.addEventListener('keydown', function (e) {
      if (!menu.open) return;
      if (e.key === 'Escape') { e.preventDefault(); menu.open = false; return; }
      if (e.key !== 'Tab') return;
      var f = [sum].concat([].slice.call(panel.querySelectorAll('a[href],button,summary'))).filter(function (el) { return el.offsetParent !== null || el === sum; });
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* desktop services dropdown and language menu: one open at a time, close on outside click or Esc */
  var drops = [].slice.call(document.querySelectorAll('.rd-svcdd,.rd-lang'));
  drops.forEach(function (d) {
    d.addEventListener('toggle', function () { if (d.open) drops.forEach(function (o) { if (o !== d) o.open = false; }); });
    if (d.classList.contains('rd-svcdd') && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      var t; d.addEventListener('mouseenter', function () { clearTimeout(t); if (!d.open) { d.open = true; d._hov = Date.now(); } });
      d.querySelector('summary').addEventListener('click', function (e) { if (d.open && d._hov && Date.now() - d._hov < 700) { e.preventDefault(); d._hov = 0; } });
      d.addEventListener('mouseleave', function () { t = setTimeout(function () { d.open = false; }, 220); });
    }
  });
  document.addEventListener('click', function (e) { drops.forEach(function (d) { if (d.open && !d.contains(e.target)) d.open = false; }); });
  document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; drops.forEach(function (d) { if (d.open) { d.open = false; d.querySelector('summary').focus(); } }); });
  document.querySelectorAll('.rd-svcdd-p a').forEach(function (a) { a.addEventListener('click', function () { a.closest('details').open = false; }); });

  var rv = document.querySelectorAll('.rd-rv');
  if (rv.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -10% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('is-in'); }); }
})();

/* Lead-source preparation for a future CRM (GoHighLevel). Nothing is sent anywhere:
   inquiry entry points are only classified, kept in this browser session, and copied into
   hidden fields of the estimate form so each email says where the inquiry came from. */
(function () {
  window.RD_CRM = window.RD_CRM || { provider: 'gohighlevel', enabled: false };
  var KEY = 'rd_lead';
  function kind(a) {
    var h = a.getAttribute('href') || '', d = a.getAttribute('data-cta');
    if (d) return d === 'estimate' && /type=builder/.test(h) ? 'builder-inquiry' : d;
    if (/^tel:/.test(h)) return 'call';
    if (/^mailto:/.test(h)) return 'email';
    if (/wa\.me/.test(h)) return 'whatsapp';
    if (/\/(estimate|orcamento|cotizacion|soumission|preventivo)\b[^#]*type=builder/.test(h)) return 'builder-inquiry';
    if (/\/(estimate|orcamento|cotizacion|soumission|preventivo)\b/.test(h)) return 'estimate';
    return null;
  }
  function where(a) { return a.getAttribute('data-cta-loc') || (a.closest('header,.rd-panel-m,.rd-mbar,footer,.rd-hero,section,main') || {}).className || 'page'; }
  function save(ev) {
    try {
      var s = JSON.parse(sessionStorage.getItem(KEY) || '{}');
      if (!s.first) s.first = ev; s.last = ev;
      if (!s.landing) s.landing = location.pathname + location.search;
      sessionStorage.setItem(KEY, JSON.stringify(s));
    } catch (e) {}
    (window.rdLeadEvents = window.rdLeadEvents || []).push(ev);
    try { document.dispatchEvent(new CustomEvent('rd:lead', { detail: ev })); } catch (e) {}
  }
  try { var s0 = JSON.parse(sessionStorage.getItem(KEY) || '{}'); if (!s0.landing) { s0.landing = location.pathname + location.search; s0.referrer = document.referrer || ''; sessionStorage.setItem(KEY, JSON.stringify(s0)); } } catch (e) {}
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href],[data-cta]'); if (!a) return;
    var k = kind(a); if (!k || k === 'search') return;
    save({ type: k, from: String(where(a)).split(' ')[0], page: location.pathname, t: Date.now() });
  }, true);
  var form = document.getElementById('rd-form');
  if (form) form.addEventListener('submit', function () {
    var s = {}; try { s = JSON.parse(sessionStorage.getItem(KEY) || '{}'); } catch (e) {}
    var file = form.querySelector('input[type=file]'), ct = form.querySelector('input[name="customer_type"]:checked'), builder = ct ? ct.value === 'builder' : /type=builder/.test(location.search);
    var type = file && file.files && file.files.length ? 'drawing-upload' : builder ? 'builder-inquiry' : 'estimate-request';
    function put(n, v) { var i = form.querySelector('input[name="' + n + '"]'); if (!i) { i = document.createElement('input'); i.type = 'hidden'; i.name = n; form.appendChild(i); } i.value = v || ''; }
    put('lead_type', type); put('lead_entry', s.first ? s.first.type + ' / ' + s.first.from + ' / ' + s.first.page : 'direct');
    put('landing_page', s.landing); put('referrer', s.referrer);
    save({ type: type, from: 'estimate-form', page: location.pathname, t: Date.now() });
  }, true);
})();

/* Language preference: remembered only when the visitor picks a language. No location or browser-language redirects. */
(function () {
  var KEY = 'rd_lang', HOMES = { en: '/', pt: '/pt/', es: '/es/', fr: '/fr/', it: '/it/' };
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[hreflang]');
    if (!a) return;
    var code = (a.getAttribute('hreflang') || '').slice(0, 2);
    if (HOMES[code]) { try { localStorage.setItem(KEY, code); } catch (err) {} }
  }, true);
  /* Only the English homepage, only on a fresh visit from outside the site (not back/forward, not an internal link),
     and only to a language the visitor chose before. ?lang=en always shows English. */
  var pref = get();
  if (location.pathname !== '/' || !pref || pref === 'en' || !HOMES[pref] || /[?&]lang=en\b/.test(location.search)) return;
  var nav = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
  if (nav && nav.type !== 'navigate') return;
  try { if (document.referrer && new URL(document.referrer).origin === location.origin) return; } catch (e) {}
  location.replace(HOMES[pref]);
})();
