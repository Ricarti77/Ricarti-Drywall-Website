/* Ricarti Drywall — site search (works on every page) */
(function () {
  var dlg = document.getElementById('rd-search');
  var input = document.getElementById('rd-q');
  var list = document.getElementById('rd-res');
  var sugg = document.getElementById('rd-sugg');
  var index = null, loading = null;
  var PT = /^pt/.test(document.documentElement.lang);
  var L = PT ? { idx: '/pt/search-index.json', page: '/pt/busca', none: 'Nada encontrado para “%s”. Tente “espuma”, “nível 5” ou “acústico”, ou ligue para ' }
             : { idx: '/search-index.json', page: '/search', none: 'Nothing matched “%s”. Try “spray foam”, “Level 5” or “soundproofing”, or call ' };

  function load() {
    if (index) return Promise.resolve(index);
    if (!loading) loading = fetch(L.idx).then(function (r) { return r.json(); }).then(function (j) { index = j; return j; });
    return loading;
  }
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[–—]/g, '-'); }
  function stem(t) { return t.length > 5 ? (PT ? t.replace(/(acoes|acao|mente|cos|cas|cao|oes|os|as|es|o|a|e|s)$/, '') : t.replace(/(ations?|ing|ion|ers|ed|es|s|e)$/, '')) : t; }
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
  var PT = /^pt/.test(document.documentElement.lang);
  var L = PT ? { close: 'Fechar', prev: 'Foto anterior', next: 'Próxima foto', of: ' de ', title: 'Álbum de obras' }
             : { close: 'Close', prev: 'Previous photo', next: 'Next photo', of: ' of ', title: 'Project album' };
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
