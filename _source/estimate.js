/* Ricarti Drywall — estimate form (Task 010). Two paths, private uploads, verified delivery. No CRM connection. */
(function () {
  var form = document.getElementById('rd-form'); if (!form) return;
  var T0 = Date.now(), LANG = document.documentElement.lang || 'en-CA', LG = LANG.slice(0, 2);
  var T = {
    en: { req: 'Please fill in this field.', email: 'Please enter a valid email address, for example name@example.com.', phone: 'Please enter a valid phone number.',
      check: 'Please check the highlighted fields.', type: 'File type not accepted. Use PDF, JPG, PNG, WebP or HEIC.', size: 'This file is larger than 50 MB.',
      many: 'You can attach up to 20 files.', total: 'The files add up to more than 200 MB. Please send fewer or smaller files.', dup: 'This file is already in the list.', empty: 'This file is empty.',
      remove: 'Remove', ready: 'Ready', waiting: 'Will not be uploaded', uploading: 'Uploading… %p%', uploaded: 'Uploaded', upfail: 'Upload failed',
      upmsg: 'Uploading file %i of %n…', sending: 'Sending your enquiry…', upErr: '“%f” could not be uploaded.', sendErr: 'We could not send your enquiry.', netErr: 'The connection was interrupted.', unk: 'We could not confirm that your enquiry arrived (reference %r).',
      files: '%n file(s) received in private storage.', removed: '%f removed.', added: '%n file(s) added.' },
    pt: { req: 'Preencha este campo.', email: 'Informe um e-mail válido, por exemplo nome@exemplo.com.', phone: 'Informe um telefone válido.',
      check: 'Verifique os campos destacados.', type: 'Tipo de arquivo não aceito. Use PDF, JPG, PNG, WebP ou HEIC.', size: 'Este arquivo tem mais de 50 MB.',
      many: 'Você pode anexar até 20 arquivos.', total: 'Os arquivos somam mais de 200 MB. Envie menos arquivos ou arquivos menores.', dup: 'Este arquivo já está na lista.', empty: 'Este arquivo está vazio.',
      remove: 'Remover', ready: 'Pronto', waiting: 'Não será enviado', uploading: 'Enviando… %p%', uploaded: 'Enviado', upfail: 'Falha no envio',
      upmsg: 'Enviando arquivo %i de %n…', sending: 'Enviando sua solicitação…', upErr: 'Não foi possível enviar “%f”.', sendErr: 'Não foi possível enviar sua solicitação.', netErr: 'A conexão foi interrompida.', unk: 'Não conseguimos confirmar se a sua solicitação chegou (referência %r).',
      files: '%n arquivo(s) recebido(s) em armazenamento privado.', removed: '%f removido.', added: '%n arquivo(s) adicionado(s).' },
    es: { req: 'Complete este campo.', email: 'Ingrese un correo electrónico válido, por ejemplo nombre@ejemplo.com.', phone: 'Ingrese un número de teléfono válido.',
      check: 'Revise los campos resaltados.', type: 'Tipo de archivo no aceptado. Use PDF, JPG, PNG, WebP o HEIC.', size: 'Este archivo supera los 50 MB.',
      many: 'Puede adjuntar hasta 20 archivos.', total: 'Los archivos suman más de 200 MB. Envíe menos archivos o archivos más pequeños.', dup: 'Este archivo ya está en la lista.', empty: 'Este archivo está vacío.',
      remove: 'Quitar', ready: 'Listo', waiting: 'No se subirá', uploading: 'Subiendo… %p%', uploaded: 'Subido', upfail: 'Error al subir',
      upmsg: 'Subiendo archivo %i de %n…', sending: 'Enviando su solicitud…', upErr: 'No se pudo subir “%f”.', sendErr: 'No pudimos enviar su solicitud.', netErr: 'Se interrumpió la conexión.', unk: 'No pudimos confirmar si su solicitud llegó (referencia %r).',
      files: '%n archivo(s) recibido(s) en almacenamiento privado.', removed: '%f quitado.', added: '%n archivo(s) agregado(s).' },
    fr: { req: 'Veuillez remplir ce champ.', email: 'Veuillez entrer une adresse courriel valide, par exemple nom@exemple.com.', phone: 'Veuillez entrer un numéro de téléphone valide.',
      check: 'Veuillez vérifier les champs indiqués.', type: 'Type de fichier non accepté. Utilisez PDF, JPG, PNG, WebP ou HEIC.', size: 'Ce fichier dépasse 50 Mo.',
      many: 'Vous pouvez joindre jusqu’à 20 fichiers.', total: 'Les fichiers dépassent 200 Mo au total. Envoyez moins de fichiers ou des fichiers plus légers.', dup: 'Ce fichier est déjà dans la liste.', empty: 'Ce fichier est vide.',
      remove: 'Retirer', ready: 'Prêt', waiting: 'Ne sera pas téléversé', uploading: 'Téléversement… %p %', uploaded: 'Téléversé', upfail: 'Échec du téléversement',
      upmsg: 'Téléversement du fichier %i sur %n…', sending: 'Envoi de votre demande…', upErr: 'Impossible de téléverser « %f ».', sendErr: 'Nous n’avons pas pu envoyer votre demande.', netErr: 'La connexion a été interrompue.', unk: 'Nous n’avons pas pu confirmer la réception de votre demande (référence %r).',
      files: '%n fichier(s) reçu(s) en stockage privé.', removed: '%f retiré.', added: '%n fichier(s) ajouté(s).' },
    it: { req: 'Compilate questo campo.', email: 'Inserite un indirizzo email valido, ad esempio nome@esempio.com.', phone: 'Inserite un numero di telefono valido.',
      check: 'Controllate i campi evidenziati.', type: 'Tipo di file non accettato. Usate PDF, JPG, PNG, WebP o HEIC.', size: 'Questo file supera i 50 MB.',
      many: 'Potete allegare fino a 20 file.', total: 'I file superano in totale i 200 MB. Inviate meno file o file più leggeri.', dup: 'Questo file è già nell’elenco.', empty: 'Questo file è vuoto.',
      remove: 'Rimuovi', ready: 'Pronto', waiting: 'Non verrà caricato', uploading: 'Caricamento… %p%', uploaded: 'Caricato', upfail: 'Caricamento non riuscito',
      upmsg: 'Caricamento del file %i di %n…', sending: 'Invio della richiesta…', upErr: 'Impossibile caricare “%f”.', sendErr: 'Non è stato possibile inviare la richiesta.', netErr: 'La connessione si è interrotta.', unk: 'Non è stato possibile confermare se la richiesta è arrivata (riferimento %r).',
      files: '%n file ricevuti in archiviazione privata.', removed: '%f rimosso.', added: '%n file aggiunti.' }
  };
  var L = T[LG] || T.en;
  function fmt(s, o) { return s.replace(/%(\w)/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  var $ = function (id) { return document.getElementById(id); };
  var MAX_FILES = 20, MAX_BYTES = 50 * 1024 * 1024, MAX_TOTAL = 200 * 1024 * 1024;
  var EXT = { pdf: 'application/pdf', jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp', heic: 'image/heic', heif: 'image/heif' };
  var uploads = { enabled: false, checked: false }, files = [], busy = false, enquiryId = null, seq = 0;
  var status = $('rd-status'), alertBox = $('rd-alert'), list = $('rd-files'), drop = $('rd-drop'), input = $('f-files');

  /* ---------- path: homeowner / builder ---------- */
  function path() { var r = form.querySelector('input[name="customer_type"]:checked'); return r ? r.value : 'homeowner'; }
  function render() {
    var p = path() === 'builder' ? 'builder' : 'home';
    document.querySelectorAll('.rd-eq-card [data-path]').forEach(function (el) {
      var v = el.getAttribute('data-path'), on = v === 'both' || v === p;
      el.hidden = !on;
      el.querySelectorAll && [el].concat([].slice.call(el.querySelectorAll('input,select,textarea'))).forEach(function (c) {
        if (/^(INPUT|SELECT|TEXTAREA)$/.test(c.tagName) && c.type !== 'radio' && c.name !== '_honey') c.disabled = !!c.closest('[hidden]');
      });
    });
    try { var u = new URL(location.href); if (p === 'builder') u.searchParams.set('type', 'builder'); else u.searchParams.delete('type'); history.replaceState(history.state, '', u); } catch (e) {}
  }
  form.querySelectorAll('input[name="customer_type"]').forEach(function (r) { r.addEventListener('change', render); });
  if (/[?&]type=builder\b/.test(location.search)) form.querySelector('input[value="builder"]').checked = true;
  render();

  /* ---------- upload availability (private storage) ---------- */
  function checkUploads() {
    var ctl = window.AbortController ? new AbortController() : null, to = setTimeout(function () { ctl && ctl.abort(); }, 5000);
    return fetch('/api/uploads/config', { signal: ctl && ctl.signal, headers: { Accept: 'application/json' }, cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; })
      .then(function (c) { clearTimeout(to); uploads.enabled = !!(c && c.enabled === true); uploads.checked = true; $('up-off').hidden = uploads.enabled; paint(); return uploads.enabled; });
  }
  var ready = checkUploads();

  /* ---------- files ---------- */
  function ext(n) { var m = /\.([a-z0-9]+)$/i.exec(n || ''); return m ? m[1].toLowerCase() : ''; }
  function size(b) { return b < 1048576 ? Math.max(1, Math.round(b / 1024)) + ' KB' : (b / 1048576).toFixed(b < 10485760 ? 1 : 0) + ' MB'; }
  function total() { return files.filter(function (f) { return !f.err; }).reduce(function (a, f) { return a + f.file.size; }, 0); }
  function add(fl) {
    var n = 0;
    [].forEach.call(fl, function (file) {
      var e = null, x = ext(file.name);
      if (files.some(function (f) { return f.file.name === file.name && f.file.size === file.size; })) e = L.dup;
      else if (!EXT[x]) e = L.type;
      else if (!file.size) e = L.empty;
      else if (file.size > MAX_BYTES) e = L.size;
      else if (files.filter(function (f) { return !f.err; }).length >= MAX_FILES) e = L.many;
      else if (total() + file.size > MAX_TOTAL) e = L.total;
      files.push({ id: ++seq, file: file, type: EXT[x] || file.type || 'application/octet-stream', err: e, state: e ? 'bad' : 'ready', p: 0, ref: null });
      if (!e) n++;
    });
    paint(); if (n) say(fmt(L.added, { n: n }));
  }
  function paint() {
    list.innerHTML = '';
    files.forEach(function (f) {
      var li = document.createElement('li'); li.className = f.err ? 'is-bad' : f.state === 'done' ? 'is-done' : '';
      var nm = document.createElement('span'); nm.className = 'n'; nm.textContent = f.file.name;
      var m = document.createElement('span'); m.className = 'm';
      m.textContent = size(f.file.size) + ' · ' + (f.err || (f.state === 'uploading' ? fmt(L.uploading, { p: f.p }) : f.state === 'done' ? L.uploaded : f.state === 'failed' ? L.upfail : uploads.checked && !uploads.enabled ? L.waiting : L.ready));
      var x = document.createElement('button'); x.type = 'button'; x.className = 'x'; x.textContent = L.remove; x.disabled = busy;
      x.setAttribute('aria-label', L.remove + ': ' + f.file.name);
      x.addEventListener('click', function () { files = files.filter(function (g) { return g !== f; }); paint(); say(fmt(L.removed, { f: f.file.name })); input.focus(); });
      li.appendChild(nm); li.appendChild(x); li.appendChild(m);
      if (!f.err && uploads.enabled) { var bar = document.createElement('span'); bar.className = 'bar'; bar.setAttribute('aria-hidden', 'true'); var i = document.createElement('i'); i.style.width = (f.state === 'done' ? 100 : f.p) + '%'; bar.appendChild(i); li.appendChild(bar); }
      list.appendChild(li);
    });
  }
  input.addEventListener('change', function () { add(input.files); input.value = ''; });
  ['dragenter', 'dragover'].forEach(function (t) { drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.add('is-over'); }); });
  ['dragleave', 'dragend', 'drop'].forEach(function (t) { drop.addEventListener(t, function (e) { if (t !== 'dragleave' || !drop.contains(e.relatedTarget)) drop.classList.remove('is-over'); }); });
  drop.addEventListener('drop', function (e) { e.preventDefault(); if (e.dataTransfer && e.dataTransfer.files) add(e.dataTransfer.files); });
  window.addEventListener('dragover', function (e) { if (!drop.contains(e.target)) e.preventDefault(); });
  window.addEventListener('drop', function (e) { if (!drop.contains(e.target)) e.preventDefault(); });

  /* ---------- validation ---------- */
  function setErr(el, msg) {
    var e = $('e-' + el.name); el.setAttribute('aria-invalid', msg ? 'true' : 'false');
    if (e) { e.textContent = msg || ''; e.hidden = !msg; if (msg) el.setAttribute('aria-describedby', e.id); else el.removeAttribute('aria-describedby'); }
  }
  function validate() {
    var bad = [];
    var name = form.elements.name, email = form.elements.email, phone = form.elements.phone;
    [name, email, phone].forEach(function (el) { setErr(el, ''); });
    if (!name.value.trim()) { setErr(name, L.req); bad.push(name); }
    if (!email.value.trim()) { setErr(email, L.req); bad.push(email); }
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) { setErr(email, L.email); bad.push(email); }
    if (phone.value.trim() && phone.value.replace(/\D/g, '').length < 7) { setErr(phone, L.phone); bad.push(phone); }
    return bad;
  }
  ['name', 'email', 'phone'].forEach(function (n) { form.elements[n].addEventListener('blur', function () { if (this.getAttribute('aria-invalid') === 'true') validate(); }); });

  /* ---------- helpers ---------- */
  function say(t) { status.textContent = t || ''; }
  function fail(msg, unknown) { $('rd-alert-t').textContent = msg; $('rd-alert-unk').hidden = !unknown; $('rd-alert-none').hidden = !!unknown; alertBox.hidden = false; alertBox.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
  function lock(on) { busy = on; $('rd-submit').disabled = on; form.setAttribute('aria-busy', on ? 'true' : 'false'); paint(); }
  function newId() {
    var d = new Date(), p = function (n) { return (n < 10 ? '0' : '') + n; }, a = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789', r = '';
    var b = new Uint8Array(5); (window.crypto || {}).getRandomValues ? crypto.getRandomValues(b) : b.forEach(function (_, i) { b[i] = Math.random() * 256; });
    b.forEach(function (x) { r += a[x % a.length]; });
    return 'RD-' + String(d.getFullYear()).slice(2) + p(d.getMonth() + 1) + p(d.getDate()) + '-' + r;
  }
  function val(n) { var el = form.elements[n]; if (!el) return ''; if (el.length && !el.tagName) { for (var i = 0; i < el.length; i++) if (!el[i].disabled) return el[i].value.trim(); return ''; } return el.disabled ? '' : String(el.value || '').trim(); }
  function txt(sel) { var el = form.querySelector(sel); return el ? el.options[el.selectedIndex].text : ''; }
  function lead() {
    var s = {}; try { s = JSON.parse(sessionStorage.getItem('rd_lead') || '{}'); } catch (e) {}
    var utm = {}; try { var q = new URL(location.origin + (s.landing || location.pathname + location.search)).searchParams; ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'].forEach(function (k) { if (q.get(k)) utm[k] = q.get(k); }); } catch (e) {}
    return { channel: 'website', form: 'estimate', page: location.pathname, landing_page: s.landing || '', referrer: s.referrer || document.referrer || '',
      first_touch: s.first || null, last_touch: s.last || null, utm: utm };
  }

  /* ---------- upload one file to private storage ---------- */
  function uploadOne(f, i, n) {
    say(fmt(L.upmsg, { i: i, n: n }));
    return fetch('/api/uploads/sign', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ enquiry: enquiryId, index: i, name: f.file.name, type: f.type, size: f.file.size }) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || !j.url || !j.pathname) throw new Error(j.error || 'sign'); return j; }); })
      .then(function (j) {
        return new Promise(function (res, rej) {
          var x = new XMLHttpRequest(); f.state = 'uploading'; f.p = 0; paint();
          x.open('PUT', j.url); x.setRequestHeader('Content-Type', f.type);
          x.upload.onprogress = function (e) { if (e.lengthComputable) { f.p = Math.round(e.loaded / e.total * 100); var li = list.children[files.indexOf(f)]; if (li) { var b = li.querySelector('.bar i'); if (b) b.style.width = f.p + '%'; li.querySelector('.m').textContent = size(f.file.size) + ' · ' + fmt(L.uploading, { p: f.p }); } } };
          x.onload = function () { if (x.status >= 200 && x.status < 300) { f.state = 'done'; f.p = 100; f.ref = { ref: j.pathname, name: f.file.name, size: f.file.size, type: f.type, storage: 'vercel-blob-private' }; paint(); res(); } else { f.state = 'failed'; paint(); rej(new Error('put ' + x.status)); } };
          x.onerror = x.onabort = function () { f.state = 'failed'; paint(); rej(new Error('network')); };
          x.send(f.file);
        });
      });
  }

  /* ---------- submit ---------- */
  form.addEventListener('submit', function (e) {
    e.preventDefault(); if (busy) return;
    alertBox.hidden = true;
    if (form.elements._honey.value) return;                          // bots: nothing is sent, nothing is shown
    var bad = validate();
    if (bad.length) { say(L.check); bad[0].focus(); return; }
    enquiryId = enquiryId || newId();
    lock(true);
    ready.then(function () {
      var good = files.filter(function (f) { return !f.err; });
      var todo = uploads.enabled ? good.filter(function (f) { return f.state !== 'done'; }) : [];
      var chain = Promise.resolve(), k = 0;
      todo.forEach(function (f) { chain = chain.then(function () { return uploadOne(f, ++k, todo.length); }).catch(function (err) { throw { file: f, err: err }; }); });
      return chain.then(function () { return send(good); });
    }).then(function (stored) {
      done(stored);
    }).catch(function (x) {
      lock(false); say('');
      if (x && x.file) fail(fmt(L.upErr, { f: x.file.file.name }));
      else if (x && x.net) { if (window.console) console.warn('[enquiry] delivery status unknown', x.detail || ''); fail(fmt(L.unk, { r: enquiryId }), true); }
      else { if (window.console) console.warn('[enquiry] delivery refused', x && x.server); fail(L.sendErr); }
    });
  });

  function send(good) {
    say(L.sending);
    var who = path(), services = [].map.call(form.querySelectorAll('input[name="services"]:checked:not(:disabled)'), function (c) { return c.value; });
    var serviceNames = [].map.call(form.querySelectorAll('input[name="services"]:checked:not(:disabled)'), function (c) { return c.parentNode.textContent.trim(); });
    var stored = good.filter(function (f) { return f.ref; }).map(function (f) { return f.ref; });
    var notUp = good.filter(function (f) { return !f.ref; }).map(function (f) { return { name: f.file.name, size: f.file.size, type: f.type, reason: uploads.enabled ? 'upload-failed' : 'uploads-not-enabled' }; });
    var tl = who === 'builder' ? '#f-btimeline' : '#f-timeline';
    var payload = {
      schema: 'ricarti.enquiry.v1', id: enquiryId, submitted_at: new Date().toISOString(),
      customer_type: who,
      contact: { name: val('name'), company: who === 'builder' ? val('company') : '', email: val('email'), phone: val('phone') },
      project: { type: who === 'builder' ? val('project_type') : '', location: val('address'), timeline: form.querySelector(tl).value, description: val('notes') },
      services: services,
      preferred_language: LANG,
      lead_source: lead(),
      consent: { privacy_notice: 'shown-' + LG, marketing_opt_in: !!form.querySelector('input[name="marketing_opt_in"]').checked },
      attachments: stored, attachments_not_received: notUp,
      crm: { provider: (window.RD_CRM || {}).provider || 'gohighlevel', connected: false }
    };
    payload._honey = form.elements._honey.value;
    payload.elapsed_ms = Date.now() - T0;
    // Our own server function validates it and emails it to the office through our email provider (Resend).
    var ctl = window.AbortController ? new AbortController() : null, to = setTimeout(function () { ctl && ctl.abort(); }, 30000);
    return fetch('/api/enquiry', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload), signal: ctl && ctl.signal })
      .catch(function (e) { clearTimeout(to); throw { net: true, detail: (e && e.name) || '' }; })
      .then(function (r) {
        clearTimeout(to);
        return r.json().catch(function () { return null; }).then(function (j) {
          var st = j && j.status;
          if (st === 'accepted') return { stored: stored.length, missing: notUp.length, payload: payload };
          if (st === 'failed') throw { server: (j && j.code) || r.status };
          throw { net: true, detail: (j && j.code) || 'http-' + r.status };      // 'uncertain' or an unreadable reply
        });
      });
  }

  function done(res) {
    lock(false); say('');
    var ev = { type: res.payload.customer_type === 'builder' ? 'builder-inquiry-sent' : 'estimate-sent', from: 'estimate-form', page: location.pathname, t: Date.now(), id: enquiryId, files: res.stored };
    (window.rdLeadEvents = window.rdLeadEvents || []).push(ev);
    try { document.dispatchEvent(new CustomEvent('rd:lead', { detail: ev })); } catch (e) {}
    $('rd-done-id').textContent = enquiryId;
    var fl = $('rd-done-files'); fl.hidden = !res.stored; fl.textContent = res.stored ? fmt(L.files, { n: res.stored }) : '';
    $('rd-done-nofiles').hidden = !res.missing;
    form.hidden = true; var d = $('rd-done'); d.hidden = false; d.focus(); d.scrollIntoView({ block: 'start', behavior: 'smooth' });
  }
  $('rd-again').addEventListener('click', function () {
    form.reset(); files = []; enquiryId = null; paint(); render(); alertBox.hidden = true;
    $('rd-done').hidden = true; form.hidden = false; form.elements.name.focus();
  });
})();
