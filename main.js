/* Solar Technik BwM – Skript. GSAP + ScrollTrigger + Lenis (CDN). Tweens nur auf transform/opacity; Blenden per clip-path. */
(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const fmt = (n, d = 0) => n.toLocaleString('de-DE', { minimumFractionDigits: d, maximumFractionDigits: d });
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  const motion = !reduce && hasGsap;
  root.classList.add(motion ? 'js-motion' : 'no-motion');
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // ---------- Lenis, gekoppelt an ScrollTrigger ----------
  let lenis;
  if (motion && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  // ---------- Kopfzeile: Ausklappmenüs, Verhalten beim Scrollen ----------
  const head = $('#head');
  const dds = $$('.has-dd');
  const setDd = (li, open) => { li.classList.toggle('open', open); $('button', li).setAttribute('aria-expanded', open ? 'true' : 'false'); };
  const closeDds = except => dds.forEach(li => li !== except && setDd(li, false));
  dds.forEach(li => {
    const b = $('button', li);
    b.addEventListener('click', () => { const o = !li.classList.contains('open'); closeDds(li); setDd(li, o); });
    if (fine) { li.addEventListener('mouseenter', () => { closeDds(li); setDd(li, true); }); li.addEventListener('mouseleave', () => setDd(li, false)); }
    li.addEventListener('focusout', e => { if (!li.contains(e.relatedTarget)) setDd(li, false); });
  });
  document.addEventListener('click', e => { if (!e.target.closest('.has-dd')) closeDds(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { const o = dds.find(li => li.classList.contains('open')); if (o) { setDd(o, false); $('button', o).focus(); } } });
  const sceneEl = $('.scene');
  let lastY = scrollY;
  const onScrollHead = () => {
    const y = scrollY;
    const overUntil = sceneEl && motion ? sceneEl.offsetHeight - innerHeight - 8 : (sceneEl ? 40 : -1);
    const over = !!sceneEl && motion && y < overUntil && !document.body.classList.contains('menu-open');
    head.classList.toggle('over', over);
    if (!document.body.classList.contains('menu-open') && !dds.some(li => li.classList.contains('open'))) {
      if (!over && y > 300 && y > lastY + 6 && y - lastY < 400) head.classList.add('hide');
      else if (y < lastY - 6 || over || y < 300) head.classList.remove('hide');
    }
    lastY = y;
    const sc = $('.sticky-cta'); if (sc) sc.classList.toggle('show', y > (sceneEl && motion ? sceneEl.offsetHeight - innerHeight * .5 : 500));
  };
  addEventListener('scroll', onScrollHead, { passive: true });
  onScrollHead();
  // Menü (Handy)
  const menu = $('#menu'), menuBtn = $('.menu-btn');
  $$('li', menu).forEach((li, i) => li.style.setProperty('--i', i));
  let lastFocus;
  const closeMenu = () => {
    if (!menu.classList.contains('open')) return;
    document.body.classList.remove('menu-open'); menu.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false'); $('.lbl', menuBtn).textContent = 'Menü';
    lenis && lenis.start(); onScrollHead(); lastFocus && lastFocus.focus();
  };
  const openMenu = () => {
    lastFocus = document.activeElement;
    document.body.classList.add('menu-open'); menu.classList.add('open'); head.classList.remove('hide'); head.classList.remove('over');
    menuBtn.setAttribute('aria-expanded', 'true'); $('.lbl', menuBtn).textContent = 'Schließen';
    lenis && lenis.stop(); setTimeout(() => $('a', menu).focus(), 350);
  };
  menuBtn.addEventListener('click', () => menu.classList.contains('open') ? closeMenu() : openMenu());
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.classList.contains('open')) { closeMenu(); menuBtn.focus(); }
    if (e.key === 'Tab' && menu.classList.contains('open')) {
      const f = $$('a', menu); const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); menuBtn.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); menuBtn.focus(); }
      else if (!e.shiftKey && document.activeElement === menuBtn) { e.preventDefault(); first.focus(); }
    }
  });
  addEventListener('resize', () => { if (innerWidth > 1020) closeMenu(); });

  // ---------- Wort-für-Wort ----------
  $$('.split').forEach(el => {
    const words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', words.join(' '));
    el.innerHTML = words.map(w => `<span class="split-line" aria-hidden="true"><span class="w">${esc(w)}</span></span>`).join(' ');
  });

  // ---------- Vorhang: Intro beim ersten Besuch, Blende beim Seitenwechsel ----------
  let seen = false; try { seen = sessionStorage.getItem('bwm-intro'); } catch (e) {}
  const intro = $('.curtain.intro');
  let introDelay = 0;
  if (!seen && motion) {
    try { sessionStorage.setItem('bwm-intro', '1'); } catch (e) {}
    document.body.classList.add('intro-on');
    const svg = $('svg', intro), word = $('span', intro);
    gsap.fromTo(svg, { rotation: -90, scale: .5, opacity: 0 }, { rotation: 0, scale: 1, opacity: 1, duration: .6, ease: 'power3.out' });
    gsap.fromTo(word, { x: -16, opacity: 0 }, { x: 0, opacity: 1, duration: .5, delay: .25, ease: 'power3.out' });
    gsap.to(intro, { yPercent: -101, duration: .7, ease: 'power3.inOut', delay: 1, onComplete: () => document.body.classList.remove('intro-on') });
    introDelay = 1.3;
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('a'); if (!a || !motion) return;
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:') || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey || e.defaultPrevented) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || (url.pathname === location.pathname && url.hash)) return;
    e.preventDefault(); document.body.classList.add('leaving'); setTimeout(() => location.href = a.href, 420);
  });
  addEventListener('pageshow', e => { if (e.persisted) document.body.classList.remove('leaving'); });
  // Anker-Links weich scrollen
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id === '#') { e.preventDefault(); lenis ? lenis.scrollTo(0) : scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); return; }
    const t = $(id); if (!t) return; e.preventDefault();
    lenis ? lenis.scrollTo(t, { offset: -80, duration: 1.4 }) : t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
  }));
  // Sprung zu #werkzeug von einer anderen Seite: nach dem Aufbau genau hinscrollen
  if (location.hash) {
    const t = $(location.hash);
    if (t) addEventListener('load', () => setTimeout(() => { hasGsap && ScrollTrigger.refresh(); lenis ? lenis.scrollTo(t, { offset: -80, immediate: true }) : t.scrollIntoView(); head.classList.remove('hide'); }, 60));
  }

  // ---------- Fortschrittsbalken ----------
  const prog = $('#progress');
  if (hasGsap) gsap.to(prog, { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: .3 } });

  // ---------- Magnetische Buttons mit Lichtreflex ----------
  if (fine && motion) $$('.mag').forEach(b => {
    const xTo = gsap.quickTo(b, 'x', { duration: .4, ease: 'power3' }), yTo = gsap.quickTo(b, 'y', { duration: .4, ease: 'power3' });
    b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); const x = e.clientX - r.left, y = e.clientY - r.top; b.style.setProperty('--mx', x + 'px'); b.style.setProperty('--my', y + 'px'); xTo((x - r.width / 2) * .2); yTo((y - r.height / 2) * .3); });
    b.addEventListener('pointerleave', () => { xTo(0); yTo(0); });
  });
  // 3D-Neigung auf Karten
  if (fine && motion) $$('.more-list a, .plist a, .card').forEach(c => {
    const rx = gsap.quickTo(c, 'rotationX', { duration: .5, ease: 'power3' }), ry = gsap.quickTo(c, 'rotationY', { duration: .5, ease: 'power3' });
    const k = c.classList.contains('card') ? 1.5 : 5;
    gsap.set(c, { transformPerspective: 1000 });
    c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); ry(((e.clientX - r.left) / r.width - .5) * k); rx(-((e.clientY - r.top) / r.height - .5) * k); });
    c.addEventListener('pointerleave', () => { rx(0); ry(0); });
  });

  // ---------- Reveals ----------
  if (motion) {
    ScrollTrigger.batch('.reveal', { start: 'top 88%', once: true, onEnter: els => gsap.to(els, { opacity: 1, y: 0, duration: .9, ease: 'expo.out', stagger: .08 }) });
    $$('.split').forEach(el => {
      gsap.from($$('.w', el), { yPercent: 110, duration: .9, ease: 'expo.out', stagger: .045, delay: el.closest('.bh') ? introDelay * .8 : 0, scrollTrigger: { trigger: el, start: 'top 92%', once: true } });
    });
  } else if (hasGsap && reduce) {
    // Stufe 2: kurze Blende ohne Weg
    $$('.reveal').forEach(el => gsap.fromTo(el, { opacity: 0 }, { opacity: 1, duration: .15, scrollTrigger: { trigger: el, start: 'top 95%', once: true } }));
  }

  // Ersatzfassung der Szene (reduzierte Bewegung): Fotos nur laden, wenn sie gezeigt wird
  if (!motion) $$('img[data-st-src]').forEach(i => { i.srcset = i.dataset.stSrcset; i.src = i.dataset.stSrc; i.loading = 'lazy'; });
  else { const st = $('.scene-static'); if (st) st.remove(); }
  // Späte Bilder (Szene ab Foto 2 erst nach dem load-Ereignis)
  const late = () => $$('img[data-late]').forEach(i => { if (i.dataset.srcset) i.srcset = i.dataset.srcset; if (i.dataset.src) i.src = i.dataset.src; });
  if (!motion) $$('.scene-pin img[data-late]').forEach(i => i.removeAttribute('data-late'));
  else if (document.readyState === 'complete') late(); else addEventListener('load', late);
  if (hasGsap) { addEventListener('load', () => ScrollTrigger.refresh()); document.fonts && document.fonts.ready.then(() => ScrollTrigger.refresh()); }

  // ---------- Bemaßungs-Kopf der Unterseiten ----------
  const bh = $('.bh');
  if (bh && motion) {
    const d = introDelay * .8;
    gsap.fromTo($$('.dimline i', bh), { scaleX: 0 }, { scaleX: 1, duration: 1, ease: 'expo.out', delay: d + .1 });
    gsap.fromTo($$('.dimline span', bh), { opacity: 0 }, { opacity: 1, duration: .4, delay: d + .5 });
    const img = $('.bh-img', bh);
    if (img) {
      gsap.fromTo(img, { scale: .6, rotation: -8, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 1.2, ease: 'expo.out', delay: d + .15 });
      gsap.fromTo($('.bh-line', bh), { scale: .92, opacity: 0 }, { scale: 1, opacity: .8, duration: 1.2, ease: 'expo.out', delay: d + .35 });
      gsap.fromTo($('.bh-dim-v i', bh), { scaleY: 0 }, { scaleY: 1, duration: 1, ease: 'expo.out', delay: d + .5 });
      gsap.to($('.bh-img img', bh), { yPercent: 8, ease: 'none', scrollTrigger: { trigger: bh, start: 'top top', end: 'bottom top', scrub: .6 } });
    }
  }

  // =================== STARTSEITE ===================
  // Szene „Was eine Anlage trägt“: Schiene → Blechdach → Flachdach → Ziegeldach → Bruchsteinhaus.
  // Fester Zeitplan: Text raus → Blende → nächster Text rein. Nie zwei Texte gleichzeitig.
  const scene = $('.scene');
  if (scene && motion) {
    const fr = $$('.frame', scene), caps = $$('.cap', scene), pin = $('.scene-pin', scene);
    const bar = $('.sr-bar b', scene), clamps = $$('.srail i', scene);
    const W = () => pin.clientWidth, Hh = () => pin.clientHeight;
    // Profil-Maske: Querschnitt der Schiene wächst über den Rand
    const PROF = [[0, 0], [38, 0], [38, 8], [28, 8], [28, 24], [72, 24], [72, 8], [62, 8], [62, 0], [100, 0], [100, 100], [62, 100], [62, 92], [72, 92], [72, 76], [28, 76], [28, 92], [38, 92], [38, 100], [0, 100]];
    const mask = p => {
      if (p >= 1) { fr[1].style.clipPath = 'none'; return; }
      const w = W(), h = Hh(), s0 = Math.min(w, h) * .2, s1 = Math.max(2.05 * h, 1.05 * w);
      const e = p * p * (3 - 2 * p), S = s0 + (s1 - s0) * e, ox = w / 2 - S / 2, oy = h / 2 - S / 2;
      fr[1].style.clipPath = 'polygon(' + PROF.map(([x, y]) => `${(ox + x * S / 100).toFixed(1)}px ${(oy + y * S / 100).toFixed(1)}px`).join(',') + ')';
    };
    // Sonnenbogen: ein Kreis zieht auf einer Bahn über den Himmel und wird zum Bild
    const sun = p => {
      if (p >= 1) { fr[3].style.clipPath = 'none'; return; }
      const a = Math.PI * (1 - Math.min(1, p * 1.25)), cx = 50 - 40 * Math.cos(a) * (1 - p * .2), cy = 88 - 62 * Math.sin(a);
      const r = p < .55 ? 4 + p * 6 : 7.3 + Math.pow((p - .55) / .45, 2) * 150;
      fr[3].style.clipPath = `circle(${r.toFixed(2)}% at ${cx.toFixed(2)}% ${cy.toFixed(2)}%)`;
    };
    // Giebel-Blende: ein Giebeldreieck steigt auf und öffnet sich zum ganzen Bild
    const gable = p => {
      if (p >= 1) { fr[4].style.clipPath = 'none'; return; }
      const e = p * p * (3 - 2 * p), wd = 26 + 160 * e, l = 50 - wd / 2, r = 50 + wd / 2, eav = 132 - 150 * e, apx = eav - 30 - 10 * e;
      fr[4].style.clipPath = `polygon(${l.toFixed(2)}% 101%, ${l.toFixed(2)}% ${eav.toFixed(2)}%, 50% ${apx.toFixed(2)}%, ${r.toFixed(2)}% ${eav.toFixed(2)}%, ${r.toFixed(2)}% 101%)`;
    };
    mask(0); sun(0); gable(0);
    gsap.set(fr[2], { rotationX: 84, transformOrigin: '50% 100%', transformPerspective: 1100 });
    const T = { in: .32, out: .3, hold: .8, move: 1.1 };
    const arrive = [0];
    const tl = gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: scene, start: 'top top', end: 'bottom bottom', scrub: .7, invalidateOnRefresh: true,
      onUpdate: () => { const tt = tl.time(); clamps.forEach((c, k) => c.classList.toggle('on', tt >= arrive[k] - .01)); },
      onRefresh: () => { const p = pr.m; mask(p); } } });
    const pr = { m: 0, s: 0, g: 0 };
    const capIn = (c, at) => tl.fromTo(c, { autoAlpha: 0, y: 34 }, { autoAlpha: 1, y: 0, duration: T.in, ease: 'power2.out', immediateRender: false }, at);
    const capOut = (c, at) => tl.to(c, { autoAlpha: 0, y: -34, duration: T.out, ease: 'power2.in' }, at);
    const railTo = (k, at) => tl.to(bar, { scaleX: k / 4, duration: T.move, ease: 'power2.inOut' }, at);
    // Einstieg: Text steht beim Laden
    gsap.fromTo(caps[0], { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 1, ease: 'expo.out', delay: introDelay + .1 });
    gsap.fromTo($('img', fr[0]), { scale: 1.14 }, { scale: 1.04, duration: 2.4, ease: 'power2.out', delay: introDelay });
    let t = .55;
    capOut(caps[0], t); t += T.out;
    // 1 → 2: Profil-Maske
    tl.set(fr[1], { visibility: 'visible' }, t);
    tl.to(pr, { m: 1, duration: T.move * 1.15, ease: 'power1.inOut', onUpdate: () => mask(pr.m) }, t);
    tl.fromTo($('img', fr[1]), { scale: 1.18 }, { scale: 1, duration: T.move * 1.15 + T.in + T.hold, immediateRender: false }, t);
    tl.to($('.fimg', fr[0]), { scale: 1.2, opacity: .5, duration: T.move * 1.15, ease: 'power1.in' }, t);
    railTo(1, t); t += T.move * 1.15; arrive[1] = t;
    tl.set(fr[0], { visibility: 'hidden' }, t);
    capIn(caps[1], t); t += T.in + T.hold; capOut(caps[1], t); t += T.out;
    // 2 → 3: Aufständerung (das Foto klappt aus der Waagerechten hoch wie ein Modul auf dem Gestell)
    tl.set(fr[2], { visibility: 'visible' }, t);
    tl.to(fr[2], { rotationX: 0, duration: T.move, ease: 'power2.out' }, t);
    tl.to($('.fimg', fr[1]), { opacity: .35, duration: T.move }, t);
    tl.fromTo($('img', fr[2]), { scale: 1.12 }, { scale: 1, duration: T.move + T.in + T.hold, immediateRender: false }, t);
    railTo(2, t); t += T.move; arrive[2] = t;
    tl.set(fr[1], { visibility: 'hidden' }, t);
    capIn(caps[2], t); t += T.in + T.hold; capOut(caps[2], t); t += T.out;
    // 3 → 4: Sonnenbogen
    tl.set(fr[3], { visibility: 'visible' }, t);
    tl.to(pr, { s: 1, duration: T.move * 1.3, ease: 'none', onUpdate: () => sun(pr.s) }, t);
    tl.fromTo($('img', fr[3]), { scale: 1.1 }, { scale: 1, duration: T.move * 1.3 + T.in + T.hold, immediateRender: false }, t);
    tl.to($('.fimg', fr[2]), { opacity: .45, duration: T.move * 1.3 }, t);
    railTo(3, t); t += T.move * 1.3; arrive[3] = t;
    tl.set(fr[2], { visibility: 'hidden' }, t);
    capIn(caps[3], t); t += T.in + T.hold; capOut(caps[3], t); t += T.out;
    // 4 → 5: Giebel-Blende
    tl.set(fr[4], { visibility: 'visible' }, t);
    tl.to(pr, { g: 1, duration: T.move * 1.1, ease: 'none', onUpdate: () => gable(pr.g) }, t);
    tl.fromTo($('img', fr[4]), { scale: 1.14 }, { scale: 1, duration: T.move * 1.1 + T.in + T.hold, immediateRender: false }, t);
    tl.to($('.fimg', fr[3]), { opacity: .4, duration: T.move * 1.1 }, t);
    railTo(4, t); t += T.move * 1.1; arrive[4] = t;
    tl.set(fr[3], { visibility: 'hidden' }, t);
    capIn(caps[4], t); t += T.in;
    tl.to({}, { duration: 1 }, t);
    addEventListener('resize', () => { mask(pr.m); });
  }

  // ---------- Dreiländereck: Grenzen zeichnen sich ----------
  const map = $('.map');
  if (map && motion) {
    const tlm = gsap.timeline({ scrollTrigger: { trigger: '.region', start: 'top 75%', end: 'center 45%', scrub: .8 } });
    tlm.fromTo($$('.border', map), { strokeDashoffset: 1 }, { strokeDashoffset: 0, stagger: .15, duration: 1, ease: 'none' }, 0);
    tlm.fromTo($$('.pl', map), { opacity: 0, y: 10 }, { opacity: 1, y: 0, stagger: .08, duration: .3 }, .5);
    tlm.fromTo($$('.ctry, .tri, .tri-l', map), { opacity: 0 }, { opacity: 1, duration: .4 }, .2);
    gsap.fromTo($('.pl.home .ring', map), { scale: .6, opacity: .7, transformOrigin: '50% 50%' }, { scale: 1.6, opacity: 0, duration: 1.8, repeat: -1, ease: 'power2.out' });
  }

  // ---------- Schichtaufbau: die Zeichnung fährt auseinander (kurzer Pin) ----------
  const layers = $('.layers');
  if (layers) {
    const svg = $('.layers-svg', layers), items = $$('.layers-list li', layers);
    const order = ['klemme', 'modul', 'schiene', 'haken', 'dach'];
    const mark = k => items.forEach(li => li.classList.toggle('on', li.dataset.l === order[k]));
    if (motion) {
      svg.setAttribute('viewBox', '0 20 900 410');
      const g = l => $(`.ly[data-l="${l}"]`, svg);
      const dims = $('.dims', svg);
      gsap.set(dims, { opacity: 0 });
      const tly = gsap.timeline({ defaults: { ease: 'power2.inOut' }, scrollTrigger: { trigger: layers, start: 'top top', end: '+=170%', pin: true, scrub: .7, anticipatePin: 1,
        onUpdate: s => mark(Math.min(4, Math.floor(s.progress * 5.2))) } });
      order.slice(0, 4).forEach((l, i) => tly.to(g(l), { y: +g(l).dataset.dy, duration: 1 }, i * .8));
      tly.to(dims, { opacity: 1, duration: .6 }, 3.6);
      tly.to({}, { duration: .5 });
      mark(0);
    } else {
      // Ohne Bewegung: fertig auseinandergezogene Zeichnung
      svg.setAttribute('viewBox', '0 20 900 410');
      $$('.ly', svg).forEach(g => g.setAttribute('transform', `translate(0 ${g.dataset.dy})`));
    }
  }

  // ---------- Leistungs-Schiene: Klemmen gleiten an ihren Platz ----------
  const rail = $('.rail-wrap');
  if (rail && motion) {
    const mm = gsap.matchMedia();
    const its = $$('.ri', rail);
    mm.add('(min-width: 701px)', () => {
      // Gleicher Weg für alle, die vorderen starten früher: so überholt nie eine Klemme die andere (keine überlagerten Buchstaben)
      gsap.fromTo(its, { x: () => innerWidth * .3, opacity: 0 }, { x: 0, opacity: 1, ease: 'power2.out', stagger: .12, scrollTrigger: { trigger: rail, start: 'top 88%', end: 'top 40%', scrub: .8, invalidateOnRefresh: true } });
      gsap.fromTo($('.rail-bar', rail), { scaleX: .2, transformOrigin: '0 50%' }, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: rail, start: 'top 90%', end: 'top 45%', scrub: .8 } });
    });
    mm.add('(max-width: 700px)', () => {
      its.forEach(it => gsap.fromTo(it, { x: 60, opacity: 0 }, { x: 0, opacity: 1, ease: 'power2.out', scrollTrigger: { trigger: it, start: 'top 92%', end: 'top 65%', scrub: .6 } }));
      gsap.fromTo($('.rail-bar', rail), { scaleY: 0, transformOrigin: '50% 0' }, { scaleY: 1, ease: 'none', scrollTrigger: { trigger: rail, start: 'top 80%', end: 'bottom 70%', scrub: .6 } });
    });
  }

  // ---------- Dachform-Wähler ----------
  const roofs = $('.roof-ui');
  if (roofs) {
    const SH = { flachdach: '60,190 60,95 200,95 200,95 340,95 340,190', satteldach: '60,190 60,115 200,40 200,40 340,115 340,190', pultdach: '60,190 60,60 200,85 200,85 340,110 340,190', freiflaeche: '40,190 40,190 200,190 200,190 360,190 360,190' };
    const TX = {
      flachdach: ['Flachdach', 'Die Module stehen in Reihen auf Gestellen, beschwert mit Betonsteinen. Neigung und Reihenabstand planen wir so, dass sich die Reihen nicht verschatten.', 'flachdach-reihen', 'Aufgeständerte Modulreihen auf einem Flachdach'],
      satteldach: ['Satteldach', 'Dachhaken aus Edelstahl laufen unter der Pfanne hindurch, darauf liegen die Schienen und darauf die Module, parallel zur Dachfläche.', 'ziegeldach', 'Solarmodule auf einem dunklen Ziegeldach'],
      pultdach: ['Pultdach', 'Eine Dachfläche, eine Richtung. Je nach Eindeckung setzen wir Dachhaken oder Trapezblechschuhe. Im Bild: ein Blechdach mit Trapezblechschuhen.', 'blechdach-weit', 'Solarmodule auf einem Blechdach'],
      freiflaeche: ['Freifläche', 'Auf der Wiese steht das Gestell auf dem Boden. Neigung und Ausrichtung bestimmen wir frei, weil kein Dach sie vorgibt.', null, ''],
    };
    const tabs = $$('[role=tab]', roofs), house = $('.house', roofs), panel = $('#rp');
    const photo = $('.roof-photo', roofs), img = $('.rp-img', roofs);
    const setRoof = (k, focus) => {
      tabs.forEach(b => { const on = b.dataset.roof === k; b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; if (on && focus) b.focus(); });
      panel.setAttribute('aria-labelledby', 'rt-' + k);
      if (hasGsap && !reduce) gsap.to(house, { attr: { points: SH[k] }, duration: .7, ease: 'expo.out' }); else house.setAttribute('points', SH[k]);
      $$('.rm', roofs).forEach(g => g.classList.toggle('on', g.classList.contains('rm-' + k)));
      const [t, d, ph, alt] = TX[k];
      $('.roof-t', roofs).textContent = t; $('.roof-d', roofs).textContent = d;
      photo.classList.toggle('none', !ph);
      if (ph) { img.style.opacity = 0; setTimeout(() => { img.srcset = `img/${ph}-m.webp 800w, img/${ph}-l.webp 1600w`; img.src = `img/${ph}-m.webp`; img.alt = alt; img.onload = () => img.style.opacity = 1; if (img.complete) img.style.opacity = 1; }, 180); }
      // Dachform ins Formular übernehmen
      const r = $$('#anfrage input[name=dachform]').find(x => x.value === t); if (r) r.checked = true;
      try { sessionStorage.setItem('bwm-dach', t); } catch (e) {}
    };
    tabs.forEach((b, i) => {
      b.addEventListener('click', () => setRoof(b.dataset.roof));
      b.addEventListener('keydown', e => { const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (d) { e.preventDefault(); setRoof(tabs[(i + d + tabs.length) % tabs.length].dataset.roof, true); } });
    });
    $('.rm-flachdach', roofs).classList.add('on');
    if (motion) {
      const len = 700;
      gsap.fromTo(house, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, ease: 'none', scrollTrigger: { trigger: roofs, start: 'top 85%', end: 'top 35%', scrub: .8 }, onComplete: () => house.style.strokeDasharray = 'none' });
      gsap.fromTo('.roof-draw', { y: 60, opacity: .3 }, { y: 0, opacity: 1, ease: 'none', scrollTrigger: { trigger: roofs, start: 'top 90%', end: 'top 45%', scrub: .8 } });
      gsap.fromTo('.roof-info', { y: 90 }, { y: 0, ease: 'none', scrollTrigger: { trigger: roofs, start: 'top 90%', end: 'top 35%', scrub: .8 } });
    }
  }

  // ---------- Baustellen mit Maßlinien ----------
  const bs = $('.bs');
  if (bs) {
    const figs = $$('.bs-f', bs), btns = $$('.bs-thumbs button', bs);
    btns.forEach(b => b.addEventListener('click', () => {
      const i = +b.dataset.i;
      figs.forEach(f => f.classList.toggle('on', +f.dataset.i === i));
      btns.forEach(x => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
    }));
    if (motion) {
      const tlb = gsap.timeline({ scrollTrigger: { trigger: bs, start: 'top 85%', end: 'top 30%', scrub: .8 } });
      tlb.fromTo($('.bs-dim.h i', bs), { scaleX: 0 }, { scaleX: 1, ease: 'none', duration: 1 }, 0);
      tlb.fromTo($('.bs-dim.v i', bs), { scaleY: 0 }, { scaleY: 1, ease: 'none', duration: 1 }, .1);
      tlb.fromTo($('.bs-frame', bs), { scale: .9 }, { scale: 1, ease: 'power1.out', duration: 1 }, 0);
      tlb.fromTo(btns, { x: 40, opacity: 0 }, { x: 0, opacity: (i, el) => el.getAttribute('aria-pressed') === 'true' ? 1 : .65, stagger: .08, duration: .5, clearProps: 'opacity' }, .3);
    }
  }

  // ---------- Selbst ausprobieren: Maßband wächst mit ----------
  const tape = $('.tape i');
  if (tape && motion) {
    gsap.fromTo(tape, { scaleY: 0 }, { scaleY: 1, ease: 'none', scrollTrigger: { trigger: '.tools-list', start: 'top 75%', end: 'bottom 60%', scrub: .6 } });
    $$('.tl').forEach(li => gsap.fromTo(li, { x: 30, opacity: 0 }, { x: 0, opacity: 1, ease: 'power2.out', scrollTrigger: { trigger: li, start: 'top 90%', end: 'top 70%', scrub: .6 } }));
  }
  // ---------- Anfrage-Blatt schiebt sich hoch ----------
  const sheet = $('.ask .ask-sheet');
  if (sheet && motion) {
    gsap.fromTo(sheet, { y: 90, rotation: 1.2 }, { y: 0, rotation: 0, ease: 'none', scrollTrigger: { trigger: '.ask', start: 'top 90%', end: 'top 25%', scrub: .8 } });
    gsap.fromTo($$('.reg', sheet), { scale: 2.2, opacity: 0 }, { scale: 1, opacity: 1, stagger: .05, ease: 'none', scrollTrigger: { trigger: '.ask', start: 'top 60%', end: 'top 25%', scrub: .8 } });
  }

  // =================== WERKZEUGE ===================
  const chipGroup = (g, cb) => $$('.chip', g).forEach(c => c.addEventListener('click', () => {
    $$('.chip', g).forEach(x => { x.classList.toggle('on', x === c); x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
    cb(c.dataset.v, c);
  }));
  const num = v => { const n = parseFloat(String(v).replace(/\./g, '').replace(',', '.').replace(/[^\d.-]/g, '')); return isFinite(n) ? n : NaN; };

  // Anfrage-Steckbrief
  const brief = $('[data-tool=brief]');
  if (brief) {
    const st = {}; $$('.chips', brief).forEach(g => { st[g.dataset.k] = $('.chip.on', g).dataset.v; chipGroup(g, v => { st[g.dataset.k] = v; draw(); }); });
    const kwh = $('[data-in=kwh]', brief);
    const draw = () => {
      const k = num(kwh.value);
      const rows = [['Dachform', st.dach], ['Stromverbrauch', k > 0 ? fmt(k) + ' kWh pro Jahr' : 'noch offen'], ['Heizung', st.heizung], ['Warmwasser', st.ww], ['E-Auto', st.auto], ['Speicher', st.speicher]];
      $('.bo-dl', brief).innerHTML = rows.map(([a, b]) => `<dt>${a}</dt><dd>${esc(b)}</dd>`).join('');
      $('.bo-hint', brief).textContent = k > 0 ? 'Fotos von Dach und Zählerschrank schicken Sie nach dem Absenden einfach per E-Mail hinterher.' : 'Tipp: Den Jahresverbrauch finden Sie auf Ihrer letzten Stromabrechnung.';
      const q = new URLSearchParams({ thema: 'planung', dach: st.dach, heizung: st.heizung, ww: st.ww, notiz: `E-Auto: ${st.auto}. Speicher: ${st.speicher}.` });
      if (k > 0) q.set('kwh', String(Math.round(k)));
      $('[data-brief-link]', brief).href = 'kontakt.html?' + q.toString();
    };
    kwh.addEventListener('input', draw); draw();
  }

  // Befestigung nach Eindeckung
  const cover = $('[data-tool=cover]');
  if (cover) {
    const data = JSON.parse($('.co-data', cover).textContent);
    const img = $('.co-photo', cover);
    chipGroup($('.chips', cover), v => {
      const d = data[v];
      $('.co-b', cover).textContent = d.b; $('.co-d', cover).textContent = d.d;
      $('.co-parts', cover).innerHTML = d.parts.map(x => `<li>${esc(x)}</li>`).join('');
      img.style.opacity = 0;
      setTimeout(() => { img.removeAttribute('srcset'); img.src = d.img; img.alt = d.b; img.onload = () => img.style.opacity = 1; if (img.complete) img.style.opacity = 1; }, 160);
      if (motion) gsap.fromTo($$('.co-parts li', cover), { x: 16, opacity: 0 }, { x: 0, opacity: 1, stagger: .06, duration: .35, ease: 'power2.out' });
    });
  }

  // Tagesplan der Geräte
  const day = $('[data-tool=day]');
  if (day) {
    const H = { morgens: 8, mittags: 12.5, nachmittags: 16, abends: 20, nachts: 2 };
    const SUN = { morgens: .5, mittags: 1, nachmittags: .65, abends: .05, nachts: 0 };
    const LBL = { wasch: 'Waschen', spuel: 'Spülen', trock: 'Trocknen', auto: 'E-Auto', ww: 'Warmwasser' };
    const st = {};
    const draw = () => {
      const used = {}; let sunny = 0, n = 0, svg = '';
      Object.entries(st).forEach(([k, v]) => {
        n++; if (SUN[v] >= .5) sunny++;
        const x = 20 + H[v] / 24 * 460, lvl = used[v] = (used[v] || 0) + 1;
        const y = 140 - 110 * Math.max(.05, SUN[v]) - (lvl - 1) * 22 + 6;
        svg += `<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)})"><circle r="5"/><text y="-9">${LBL[k]}</text></g>`;
      });
      $('.day-marks', day).innerHTML = svg;
      $('.day-out', day).textContent = sunny === n ? `Alle ${n} Geräte laufen, wenn die Sonne scheint.` : `${sunny} von ${n} Geräten laufen, wenn die Sonne scheint.` + (sunny < n ? ' Mit Startzeitvorwahl lassen sich Waschmaschine und Spülmaschine oft auf den Mittag legen.' : '');
    };
    $$('.dv', day).forEach(r => { const g = $('.chips', r); st[r.dataset.d] = $('.chip.on', g).dataset.v; chipGroup(g, v => { st[r.dataset.d] = v; draw(); }); });
    draw();
  }

  // Symptom-Wegweiser
  const sym = $('[data-tool=sym]');
  if (sym) {
    const bs_ = $$('.sym', sym);
    bs_.forEach(b => b.addEventListener('click', () => {
      bs_.forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      $$('.sym-p', sym).forEach(p => p.classList.toggle('on', p.dataset.p === b.dataset.v));
    }));
  }

  // Hitze-Rechner
  const heat = $('[data-tool=heat]');
  if (heat) {
    let T = +$('.chip.on', heat).dataset.v;
    const own = $('[data-in=t]', heat);
    const draw = () => {
      const P = 405 * (1 - .0035 * (T - 25)), d = (P / 405 - 1) * 100;
      $('[data-o=w]', heat).textContent = fmt(Math.round(P));
      $('.ho-bar i', heat).style.transform = `scaleX(${Math.max(0, Math.min(1.1, P / 405 * .88)).toFixed(3)})`;
      $('[data-o=eq]', heat).textContent = T === 25 ? 'Bei 25 °C liefert das Modul seine volle Nennleistung.' : `405 W × (1 ${T > 25 ? '−' : '+'} 0,35 % × ${fmt(Math.abs(T - 25))}) = ${fmt(Math.round(P))} W, also ${fmt(Math.abs(d), 1)} % ${d < 0 ? 'weniger' : 'mehr'}.`;
    };
    chipGroup($('.chips', heat), v => { T = +v; own.value = ''; draw(); });
    own.addEventListener('input', () => { const v = num(own.value); if (isFinite(v) && v >= -40 && v <= 85) { T = v; $$('.chip', heat).forEach(c => { c.classList.remove('on'); c.setAttribute('aria-pressed', 'false'); }); draw(); } });
    draw();
  }

  // Stückliste
  const bom = $('[data-tool=bom]');
  if (bom) {
    let o = 'hoch';
    const nI = $('[data-in=n]', bom), rI = $('[data-in=r]', bom), svg = $('.bom-svg', bom);
    const draw = () => {
      const n = Math.max(1, Math.min(30, Math.round(num(nI.value) || 1))), r = Math.max(1, Math.min(10, Math.round(num(rI.value) || 1)));
      const w = o === 'hoch' ? 996 : 2015, h = o === 'hoch' ? 2015 : 996;
      const L = n * w + (n - 1) * 20 + 100, per = Math.ceil(L / 6000);
      const out = [['Module', fmt(n * r)], ['Leistung', fmt(n * r * .405, 2) + ' kWp'], ['Schiene gesamt', fmt(r * 2 * L / 1000, 1) + ' m'], ['Schienenstücke à 6 m', fmt(r * 2 * per)],
        ['Schienenverbinder', fmt(r * 2 * (per - 1))], ['Endklemmen', fmt(r * 4)], ['Mittelklemmen', fmt(r * (n - 1) * 2)], ['Modulfläche', fmt(n * r * 2.015 * .996, 1) + ' m²']];
      $('.bom-out', bom).innerHTML = out.map(([a, b]) => `<div><dt>${a}</dt><dd>${b}</dd></div>`).join('');
      // Zeichnung
      const totW = L, totH = r * h + (r - 1) * 300, sc = Math.min(560 / totW, 190 / totH), ox = (600 - totW * sc) / 2, oy = (220 - totH * sc) / 2;
      let s = '';
      for (let j = 0; j < r; j++) {
        const y0 = oy + j * (h + 300) * sc;
        [.25, .75].forEach(f => s += `<rect class="rl" x="${ox.toFixed(1)}" y="${(y0 + h * f * sc - 1.5).toFixed(1)}" width="${(totW * sc).toFixed(1)}" height="3"/>`);
        for (let i = 0; i < n; i++) {
          const x0 = ox + (50 + i * (w + 20)) * sc;
          s += `<rect class="m" x="${x0.toFixed(1)}" y="${y0.toFixed(1)}" width="${(w * sc).toFixed(1)}" height="${(h * sc).toFixed(1)}" rx="1"/>`;
        }
        for (let i = 0; i <= n; i++) {
          const xc = ox + (50 + i * (w + 20) - 10) * sc;
          [.25, .75].forEach(f => s += `<rect class="cl" x="${(xc - 2).toFixed(1)}" y="${(y0 + h * f * sc - 3).toFixed(1)}" width="4" height="6"/>`);
        }
      }
      svg.innerHTML = s;
    };
    chipGroup($('.chips', bom), v => { o = v; draw(); });
    [nI, rI].forEach(i => i.addEventListener('input', draw));
    draw();
  }

  // Wechselrichter-Finder
  const inv = $('[data-tool=inv]');
  if (inv) {
    const data = JSON.parse($('.inv-data', inv).textContent), nI = $('[data-in=n]', inv);
    const draw = () => {
      const n = Math.max(1, Math.min(40, Math.round(num(nI.value) || 1))), dc = n * .405;
      $('.inv-sum', inv).textContent = `${n} ${n === 1 ? 'Modul' : 'Module'} × 405 W = ${fmt(dc, 2)} kWp`;
      $('.inv-list', inv).innerHTML = data.map(d => {
        const ok = dc <= d.dc, ac = parseFloat(d.ac.replace(',', '.'));
        const st = ok ? (dc < ac * .7 ? 'passt, eher groß' : 'passt') : 'zu klein';
        const txt = ok ? `Bis ${fmt(d.dc, 1)} kW Modulleistung ausgelegt, Sie liegen bei ${fmt(dc / d.dc * 100)} %.` : `Ausgelegt bis ${fmt(d.dc, 1)} kW Modulleistung, Sie liegen ${fmt(dc - d.dc, 2)} kW darüber.`;
        return `<li class="${ok ? 'ok' : ''}"><b>${d.t} · ${d.ac} kW</b><span class="st">${st}</span><span class="bar"><i style="transform:scaleX(${Math.min(1, dc / d.dc).toFixed(3)})"></i></span><small>${txt}</small></li>`;
      }).join('') + (data.every(d => dc > d.dc) ? '<li><b>Mehr als 12 Module</b><span class="st">größeres Gerät</span><small>Für diese Anlagengröße planen wir einen größeren oder dreiphasigen Wechselrichter. Sprechen Sie uns an.</small></li>' : '');
    };
    $$('[data-step]', inv).forEach(b => b.addEventListener('click', () => { nI.value = Math.max(1, Math.min(40, (Math.round(num(nI.value)) || 0) + +b.dataset.step)); draw(); }));
    nI.addEventListener('input', draw); draw();
  }

  // Nacht-Rechner
  const night = $('[data-tool=night]');
  if (night) {
    const st = {}; const own = $('[data-in=w]', night);
    $$('.chips', night).forEach(g => { st[g.dataset.k] = +$('.chip.on', g).dataset.v; chipGroup(g, v => { st[g.dataset.k] = +v; if (g.dataset.k === 'w') own.value = ''; draw(); }); });
    $('.nt', night).innerHTML = [20, 22, 0, 2, 4, 6, 8].map((h, i) => `<text x="${10 + i * 2 / 12 * 580}" y="30">${h} Uhr</text><path d="M${10 + i * 2 / 12 * 580} 38v44" stroke="#dfe2e7"/>`).join('');
    const draw = () => {
      const h = st.cap * 1000 / st.w;
      $('[data-o=h]', night).textContent = fmt(h, h < 10 ? 1 : 0);
      $('.nb', night).setAttribute('width', (Math.min(12, h) / 12 * 580).toFixed(1));
      const end = (20 + h) % 24, hh = Math.floor(end), mm = Math.round((end - hh) * 60 / 15) * 15;
      $('[data-o=t]', night).textContent = h >= 10 ? `Ab 20 Uhr reicht der Speicher bis in den Morgen, wenn die Anlage wieder liefert.` : `Ab 20 Uhr reicht der Speicher bis etwa ${hh}:${String(mm % 60).padStart(2, '0')} Uhr.`;
    };
    own.addEventListener('input', () => { const v = num(own.value); if (v >= 50 && v <= 5000) { st.w = v; $$('[data-k=w] .chip', night).forEach(c => { c.classList.remove('on'); c.setAttribute('aria-pressed', 'false'); }); draw(); } });
    draw();
  }

  // =================== FORMULAR ===================
  $$('[data-form]').forEach(f => {
    const q = new URLSearchParams(location.search);
    const setSel = (name, val) => { const s = $(`[name=${name}]`, f); if (!s || !val) return; const o = [...s.options].find(o => o.value === val || o.text === val || o.text.startsWith(val)); if (o) s.value = o.value; };
    setSel('thema', q.get('thema')); setSel('heizung', q.get('heizung')); setSel('warmwasser', q.get('ww'));
    let dach = q.get('dach'); if (!dach) { try { dach = sessionStorage.getItem('bwm-dach'); } catch (e) {} }
    if (dach) { const r = $$('input[name=dachform]', f).find(x => x.value === dach); if (r) r.checked = true; }
    if (q.get('kwh')) $('[name=stromverbrauch]', f).value = q.get('kwh');
    if (q.get('notiz')) $('[name=nachricht]', f).value = q.get('notiz') + '\n';
    const err = $('.f-err', f);
    f.addEventListener('submit', e => {
      const bad = [];
      $$('.fld, .chk', f).forEach(x => x.classList.remove('bad'));
      const need = [['name', 'Name'], ['email', 'E-Mail'], ['nachricht', 'Nachricht']];
      need.forEach(([n, l]) => { const i = $(`[name=${n}]`, f); if (!i.value.trim() || (n === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(i.value.trim()))) { bad.push(l); i.closest('.fld').classList.add('bad'); } });
      const ds = $('[name=datenschutz]', f); if (!ds.checked) { bad.push('Einverständnis'); ds.closest('.chk').classList.add('bad'); }
      if (bad.length) { e.preventDefault(); err.textContent = 'Bitte prüfen: ' + bad.join(', ') + '.'; const first = $('.bad input, .bad textarea', f); first && first.focus(); return; }
      err.textContent = '';
      // Vorschau ohne Netlify (lokal, GitHub Pages): direkt zur Danke-Seite
      if (!/netlify\.app$|solar-bwm\.com$/.test(location.hostname)) { e.preventDefault(); location.href = 'danke.html'; }
    });
  });

  // Karte erst per Klick
  const km = $('.k-map');
  if (km) $('button', km).addEventListener('click', () => { km.innerHTML = `<iframe src="${km.dataset.map}" title="Karte: Solar Technik BwM in Lontzen" loading="lazy"></iframe>`; km.classList.add('loaded'); });

  // Lightbox Referenzen
  const lb = $('.lb');
  if (lb) {
    const bts = $$('.lb-open'); let cur = 0, opener;
    const show = i => { cur = (i + bts.length) % bts.length; const b = bts[cur], im = $('img', b); $('img', lb).src = b.dataset.full; $('img', lb).alt = im.alt; $('figcaption', lb).textContent = im.alt + ` (${cur + 1} / ${bts.length})`; };
    const close = () => { lb.hidden = true; lenis && lenis.start(); opener && opener.focus(); };
    bts.forEach((b, i) => b.addEventListener('click', () => { opener = b; show(i); lb.hidden = false; lenis && lenis.stop(); $('.lb-x', lb).focus(); }));
    $('.lb-x', lb).addEventListener('click', close);
    $('.lb-p', lb).addEventListener('click', () => show(cur - 1));
    $('.lb-n', lb).addEventListener('click', () => show(cur + 1));
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    document.addEventListener('keydown', e => {
      if (lb.hidden) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') show(cur - 1); else if (e.key === 'ArrowRight') show(cur + 1);
      else if (e.key === 'Tab') { const f = $$('button', lb); const i = f.indexOf(document.activeElement); e.preventDefault(); f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus(); }
    });
  }
})();
