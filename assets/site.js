/* Ricarti Drywall — site search (works on every page) */
(function () {
  var dlg = document.getElementById('rd-search');
  var input = document.getElementById('rd-q');
  var list = document.getElementById('rd-res');
  var sugg = document.getElementById('rd-sugg');
  var index = null, loading = null;

  function load() {
    if (index) return Promise.resolve(index);
    if (!loading) loading = fetch('/search-index.json').then(function (r) { return r.json(); }).then(function (j) { index = j; return j; });
    return loading;
  }
  function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[–—]/g, '-'); }
  function stem(t) { return t.length > 5 ? t.replace(/(ations?|ing|ion|ers|ed|es|s|e)$/, '') : t; }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var STOP = { the: 1, and: 1, for: 1, you: 1, how: 1, what: 1, does: 1, with: 1, are: 1, can: 1, do: 1, of: 1, to: 1, in: 1, a: 1, my: 1, is: 1, an: 1, or: 1 };

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
    }).join('') : '<li class="rd-sugg">Nothing matched “' + esc(q) + '”. Try “spray foam”, “Level 5” or “soundproofing”, or call <a href="tel:+16474821139">(647) 482-1139</a>.</li>';
  }
  window.rdSearch = { load: load, render: render };

  if (!dlg) return;
  function open(e) {
    if (e) e.preventDefault();
    if (typeof dlg.showModal === 'function') dlg.showModal(); else { location.href = '/search'; return; }
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
