import { draw, loadHistory, saveHistory, newSeed } from './deck.js?v=203';
import { compose, INDUSTRIES, STAGES } from './oracle.js?v=203';
import { startBg, revealFx, tiltCard, enableGyro, startAmbient, stopAmbient, setTheme, resetTheme, sparkleCard, flickerTitle, cursorSparks } from './fx.js?v=203';
import { initAnalytics, track, enabled as gaEnabled, consent as gaConsent, setConsent as gaSetConsent } from './analytics.js?v=203';
import { shareImage } from './share.js?v=203';
import { start as startAudio, sfx, toggleMute, isMuted, audioError } from './audio.js?v=203';

const $ = s => document.querySelector(s);
const OFFER = 'https://whosz.pl/offer/?utm_source=tarot&utm_medium=app&utm_campaign=wrozba';
const ROMAN = ['0','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI'];
// Emoji: pikselowe PNG z SerenityOS (BSD-2, img/emoji/LICENSE), nazwane kodem Unicode.
const SIGN = { aries:'2648', taurus:'2649', gemini:'264A', cancer:'264B', leo:'264C', virgo:'264D', libra:'264E', scorpio:'264F', sagittarius:'2650', capricorn:'2651', aquarius:'2652', pisces:'2653' };
const ELEM = { fire:'1F525', earth:'1F30D', air:'1F4A8', water:'1F4A7' };
const SYM = { wands: '1F525', cups: '1F377', swords: '2694', pentacles: '1FA99', major: '1F319' };
const params = new URLSearchParams(location.search);
const store = { get: k => { try { return localStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch {} } };
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Always starts in Polish (English only via the switch or ?lang=en in the link).
let lang = params.get('lang') || 'pl';
if (!['pl', 'en'].includes(lang)) lang = 'pl';
let untilt = () => {}, preview = null;
let appStale = false, ui, grammar, zodiac, cards, seed = params.get('s'), cur, screen = 's-intro', tab = 'fortune';

$('#view').addEventListener('scroll', () => $('.bar').classList.toggle('scrolled', $('#view').scrollTop > 2), { passive: true });
document.addEventListener('selectstart', e => { if (!e.target.closest?.('input, textarea, select')) e.preventDefault(); });
document.addEventListener('dragstart', e => e.preventDefault());

// Install: Chrome/Android via beforeinstallprompt, iOS and the rest via a hint; the button is hidden in the installed app.
let installEvt = null;
const standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone;
if (standalone) $('#install').hidden = true;
addEventListener('beforeinstallprompt', e => { e.preventDefault(); installEvt = e; });
addEventListener('appinstalled', () => { $('#install').hidden = true; $('#install-hint').hidden = true; installEvt = null; track('install'); });
$('#install').onclick = async () => {
  const hint = $('#install-hint');
  if (installEvt) { installEvt.prompt(); await installEvt.userChoice.catch(() => {}); installEvt = null; return; }
  hint.textContent = /iphone|ipad|ipod/i.test(navigator.userAgent) ? ui.installIos : ui.installOther;
  hint.hidden = false;
};

// Menu (hamburger): language, sound, creator info.
function paintMute() { $('#mute img').src = `img/emoji/U+${isMuted() ? '1F507' : '1F50A'}.png`; $('#mute span').textContent = ui ? (isMuted() ? ui.soundOff : ui.soundOn) + (audioError() ? ` (${audioError()})` : '') : ''; }
function closeMenu() { $('#menu').hidden = $('#menu-back').hidden = true; $('#menu-btn').setAttribute('aria-expanded', 'false'); }
function toggleMenu() { paintMute(); const open = $('#menu').hidden; $('#menu').hidden = $('#menu-back').hidden = !open; $('#menu-btn').setAttribute('aria-expanded', String(open)); }

// Pixel grid of the card art: 72 by default (144x216, doubled pixels); test cards are natively 64x96 (retro 16 colours) or 96x144.
const gridOf = () => 64;   // all cards are natively 64x96 (retro 16 colours)
let cardAvail = { reveal: 255, read: 156 }, snapFn = (g, t) => t;
// Text always fits its box: we shrink the font until the longest word stops overflowing (lower limit 8 px).
function fitText(nm) {
  if (!nm) return;
  nm.style.fontSize = '';
  let size = parseFloat(getComputedStyle(nm).fontSize);
  while (nm.scrollWidth > nm.clientWidth + 0.5 && size > 8) { size -= 1; nm.style.fontSize = size + 'px'; }
}
const fitName = () => { fitText($('#card .nm')); fitText($('#rname')); };

function sizeCard() {
  if (!cur) return;
  const kind = screen === 's-read' ? 'read' : 'reveal';
  $('#card').style.setProperty('--cw', snapFn(gridOf(cur.card.id), cardAvail[kind]) + 'px');
  fitName();
}

// Pixel scale: all pixel graphics are enlarged by a whole number of DEVICE pixels (otherwise the pixels come out uneven).
function pixelScale() {
  const dpr = devicePixelRatio || 1, root = document.documentElement.style, v = $('#view');
  const pw = v.clientWidth, vh = v.clientHeight, n = Math.max(1, Math.round(dpr)), u = n / dpr;
  const snapDown = (grid, target) => grid * Math.max(1, Math.floor(target * dpr / grid + .25)) / dpr;   // size <= ~target, a multiple of the grid
  const snapUp = (grid, target) => grid * Math.max(1, Math.ceil(target * dpr / grid)) / dpr;           // rozmiar >= target (pokrycie)
  snapFn = snapDown; cardAvail = { reveal: Math.min(pw * .78, 340, (vh - 400) / 1.5) * .8625, read: Math.min(pw * .4, 170) };
  // Title: the Old English Gothic Pixel font has a 20-pixel-per-em grid, so size = 20 x (whole device pixels per font pixel)
  const fitTitle = (em, maxCss) => 20 * Math.max(1, Math.floor(maxCss * dpr / (em * 20))) / dpr + 'px';
  root.setProperty('--ft1', fitTitle(3.35, pw * .88));   // ekran startowy: "Spoooky" nad "Deck"
  root.setProperty('--ft2', fitTitle(5.6, pw * .84));    // ekran wyboru: jedna linia
  root.setProperty('--u', u + 'px');
  root.setProperty('--cw', snapDown(64, Math.min(pw * .78, 340, (vh - 400) / 1.5) * .8625) + 'px');
  const fwPx = snapDown(64, Math.min(pw * .5, 216)); root.setProperty('--fw', fwPx + 'px');
  root.setProperty('--fwt', snapDown(64, Math.min(fwPx * 1.4, pw * .66)) + 'px');   // chosen card larger by a whole scale
  root.setProperty('--aw', snapDown(64, Math.min(pw * .4, 170)) + 'px');
  root.setProperty('--iw', snapDown(108, Math.min(pw - 32 - 36 * u, (vh - 320) * 108 / 192)) + 'px');   // splash 108x192: fits together with the title and the button
  root.setProperty('--sw', Math.max(snapUp(72, pw), snapUp(128, vh) * 72 / 128) + 'px');
}
addEventListener('resize', () => { pixelScale(); sizeCard(); });

const VQ = new URL(import.meta.url).search;   // ?v=NNN from this module's URL: data gets the version too, so it does not stay cached after an update
const getJSON = u => fetch(u + VQ).then(r => r.json());

const SCENES = { 's-intro': 'intro', 's-form': 'pick', 's-pick': 'pick', 's-card': 'card', 's-read': 'read' };
let sceneTimer;
function setScene(id) {   // step background: smooth change (fade out, swap, fade in)
  const el = $('#scene'), k = SCENES[id]; clearTimeout(sceneTimer);
  if (k && el.dataset.scene === k && el.classList.contains('on')) return;   // same background (form and card pick): no flicker
  el.classList.remove('on');
  if (k) sceneTimer = setTimeout(() => { el.style.backgroundImage = `url(img/ui/bg-${k}.png)`; el.dataset.scene = k; el.classList.add('on'); }, 260);
}

function show(id) {
  if (appStale && (id === 's-intro' || id === 's-form')) return location.reload();   // a new version was waiting
  screen = id; setScene(id); if (id !== 's-pick') stopAmbient();
  document.querySelectorAll('.screen').forEach(s => s.hidden = s.id !== id);
  if (!reduced) { const sc = $('#' + id); sc.classList.remove('fadein'); void sc.offsetWidth; sc.classList.add('fadein'); }   // quick fade-in of the new screen
  $('#back').style.visibility = ['s-pick', 's-card', 's-read'].includes(id) ? 'visible' : 'hidden';
  closeMenu();
  $('#bar-title').textContent = '';   // the card name is on the plate, not in the header
  $('#view').scrollTop = 0; $('.bar').classList.remove('scrolled');
}

async function load() {
  [ui, grammar, zodiac, cards] = await Promise.all([getJSON(`data/ui.${lang}.json`), getJSON(`data/grammar.${lang}.json`), getJSON(`data/zodiac.${lang}.json`), getJSON('data/cards.json')]);
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-ui]').forEach(e => e.textContent = ui[e.dataset.ui]);
  document.querySelectorAll('.langs button').forEach(b => b.setAttribute('aria-pressed', b.dataset.lang === lang));
  paintMute();
  $('#f-zodiac').replaceChildren(...zodiac.map(z => new Option(z.name, z.id)));
  $('#f-industry').replaceChildren(...INDUSTRIES.map(i => new Option(ui['ind_' + i], i)));
  $('#f-stage').replaceChildren(...STAGES.map(s => new Option(ui['stg_' + s], s)));
  const saved = JSON.parse(store.get('sd_form') || '{}');
  $('#f-name').value = saved.name || '';
  $('#f-company').value = saved.company || '';
  if (saved.zodiac) $('#f-zodiac').value = saved.zodiac;
  $('#f-industry').value = INDUSTRIES.includes(saved.industry) ? saved.industry : 'inne';   // without saved data: neutral defaults
  $('#f-stage').value = STAGES.includes(saved.stage) ? saved.stage : 'rozwoj';
}

const em = cp => { const i = document.createElement('img'); i.className = 'emoji'; i.src = `img/emoji/U+${cp}.png`; i.alt = ''; return i; };
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };

function fillCard({ card, reversed }) {
  const c = $('#card');
  c.className = 'card' + (reversed ? ' rev' : '');
  const f = c.querySelector('.front');
  const sym = el('div', 'sym'); sym.append(em(SYM[card.suit || 'major']));
  f.style.backgroundImage = `url(img/cards/${card.id}.png)`;
  f.replaceChildren(sym, el('div', 'num', ROMAN[card.number] || String(card.number)), el('div', 'nm', card.name[lang]));
}

function reveal() {
  const form = { name: $('#f-name').value, zodiac: $('#f-zodiac').value, company: $('#f-company').value, industry: $('#f-industry').value, stage: $('#f-stage').value };
  store.set('sd_form', JSON.stringify(form));
  const hist = loadHistory();
  if (!seed) seed = newSeed(cards, hist);
  const { card, reversed } = preview ? { card: cards.find(c => c.id === preview.id), reversed: preview.rev } : draw(seed, cards);
  saveHistory([...hist, card.id]);
  track('draw', { card_id: card.id, reversed: reversed ? 1 : 0, industry: form.industry, stage: form.stage, language: lang });
  const z = zodiac.find(z => z.id === form.zodiac);
  const { parts, quote } = compose({ seed, card, reversed, name: form.name, zodiac: z, company: form.company, industry: form.industry, stage: form.stage, lang, grammar, ui });
  cur = { card, reversed, z, parts, quote };

  // Reset .fade elements without a transition BEFORE showing the screen (otherwise they faded out and in again on the next draw).
  const fades = document.querySelectorAll('#s-card .fade');
  fades.forEach(f => { f.style.transition = 'none'; f.classList.remove('in'); });
  setTheme(card.suit, reversed);
  show('s-card');
  $('#cardslot').append($('#card'));
  untilt(); untilt = tiltCard($('#cardslot'));
  fillCard(cur); sizeCard();
  $('#quote').textContent = lang === 'pl' ? `„${quote}”` : `“${quote}”`;
  const info = $('#info'); info.replaceChildren();
  for (const [ic, lb, vl] of [
    [SYM[card.suit || 'major'], ui.arcana, card.arcana === 'major' ? ui.major : ui.minor],
    [SIGN[z.id], ui.sign, z.name],
    [ELEM[z.element], ui.element, ui[z.element]],
    [reversed ? '1F53B' : '1F53A', ui.position, reversed ? ui.reversed : ui.upright]]) {
    info.append(el('div', '', '')); const d = info.lastChild;
    const icon = el('span', 'ic'); icon.append(em(ic));
    d.append(icon, el('span', 'lb', lb), el('span', 'vl', vl));
  }
  void document.body.offsetWidth;
  fades.forEach(f => f.style.transition = '');
  $('#offer').href = OFFER; $('#offer').onclick = () => track('offer_click', { card_id: card.id, language: lang });
  // Everything within 2 s: flip 0.6 s, then quote, info and button together (0.5-1.3 s). Space is reserved, nothing jumps.
  const t = reduced ? 0 : 1;
  sfx('pick');
  setTimeout(() => { $('#card').classList.add('flip'); sfx('flip'); }, 50 * t);
  setTimeout(() => { sfx(reversed ? 'hitRev' : 'hit'); revealFx(reversed, $('#card'), card.suit); }, 300 * t);
  setTimeout(() => fades.forEach(f => f.classList.add('in')), 500 * t);
}

function renderTab(name) {
  tab = name;
  document.querySelectorAll('.tabs button').forEach(b => b.setAttribute('aria-selected', b.dataset.tab === name));
  const box = $('#tabtext'); box.replaceChildren(); box.dataset.tab = name;
  const p = (t, cls) => box.append(el('p', cls, t));
  const side = cur.reversed ? cur.card.rev : cur.card.up;
  if (name === 'fortune') {
    cur.parts.forEach(x => p(x.text, x.id === 'puenta' ? 'lead' : undefined));
  } else if (name === 'card') {
    p(`${cur.card.name[lang]}, ${cur.reversed ? ui.reversed : ui.upright}`, 'lead');
    p(side.keywords[lang].join(', '));
    side.sentences[lang].forEach(s => p(s));
    p(cur.card.business[lang]);
  } else if (name === 'key') {
    const c = cur.card, major = c.arcana === 'major', SUIT_EL = { wands: 'fire', cups: 'water', swords: 'air', pentacles: 'earth' };
    // section headings use the same icons as the info row under the card (suit, sign, element, position)
    const lead = (icon, text) => { const e = el('p', 'lead'); e.append(em(icon), el('span', '', text)); box.append(e); };
    p(ui.keyHow);
    lead(SYM[c.suit || 'major'], `${ui.keyArcana}: ${major ? ui.major : ui.minor}`); p(major ? ui.keyMajor : ui.keyMinor);
    if (!major) p(ui['suit_' + c.suit]);
    lead(SIGN[cur.z.id], `${ui.keySign}: ${cur.z.name}`); p(ui.keySignText); p(`„${cur.parts[2].text}”`);
    lead(ELEM[cur.z.element], `${ui.keyElement}: ${ui[cur.z.element]}`); p(ui.keyElementText);
    p(major ? ui.keyElMajor : (SUIT_EL[c.suit] === cur.z.element ? ui.keyElMatch : ui.keyElDiff));
    lead(cur.reversed ? '1F53B' : '1F53A', `${ui.keyPos}: ${cur.reversed ? ui.reversed : ui.upright}`); p(cur.reversed ? ui.keyPosRev : ui.keyPosUp);
  }
  [...box.children].forEach((c, i) => { c.classList.add('stag'); c.style.animationDelay = Math.min(i, 12) * 95 + 'ms'; });   // paragraphs come in one by one
  box.style.animation = 'none'; void box.offsetWidth; box.style.animation = '';
}

function openRead() {
  show('s-read');
  $('#artslot').append($('#card')); sizeCard();
  $('#rname').textContent = cur.card.name[lang]; fitText($('#rname'));
  renderTab('fortune');
}

let pickTimers = [];   // shuffle timers; cleared on a new draw so old ones do not break the new animation
function pick() {
  pickTimers.forEach(clearTimeout); pickTimers = [];
  const later = (fn, ms) => pickTimers.push(setTimeout(fn, ms));
  show('s-pick'); startAmbient();
  $('#date').textContent = new Date().toLocaleDateString(lang, { weekday: 'long', day: 'numeric', month: 'long' });
  const fan = $('#fan'), N = 21, STEP = 9, mid = (N - 1) / 2;
  fan.replaceChildren(); fan.classList.remove('picked', 'drag', 'glide', 'shuffling'); $('#s-pick').classList.remove('picking');
  const els = Array.from({ length: N }, () => { const c = el('div', 'fcard'); c.setAttribute('aria-hidden', 'true'); fan.append(c); return c; });
  let off = 0, startX = 0, startOff = 0, moved = false, down = false, vel = 0, lastX = 0, lastT = 0, raf = 0, picking = false;
  // Depth: cards further from the centre are smaller and drop along an arc, while the middle one pops forward.
  const layout = () => els.forEach((c, i) => {
    const d = i - mid + off, a = Math.abs(d), top = a < 0.5;
    c.style.transform = `rotate(${d * STEP}deg) translateY(${(Math.min(a, 6) * Math.min(a, 6) * 1.2).toFixed(1)}px) scale(${(1 - Math.min(a, 8) * .018).toFixed(3)})${top ? ' translateY(calc(var(--fw) * .4425 - 24px)) scale(1.15)' : ''}`;
    c.classList.toggle('top', top);
    c.style.zIndex = N - Math.round(a);
    c.style.opacity = a > 4.6 ? '0' : '';   // far cards are hidden (their bottom edges created stripes in the background)
  });
  // Dealing: cards fly out of the stack in the middle one by one
  // Shuffling: a stack in the middle, two halves move alternately left and right (twice), then dealing into the fan
  const deal = () => { els.forEach((c, i) => { c.style.transitionDelay = (Math.abs(i - mid) * 40) + 'ms'; c.style.opacity = ''; }); layout(); sfx('flip'); later(() => els.forEach(c => c.style.transitionDelay = ''), 40 * mid + 700); };
  const stack = (dx, k) => els.forEach((c, i) => { c.style.transitionDelay = ''; c.style.transitionDuration = '.18s'; const side = (i % 2 ? 1 : -1) * k; c.style.transform = `translate(${side * dx}px, 0) rotate(${side * 3}deg) scale(.82)`; c.style.opacity = '1'; });
  els.forEach(c => { c.style.opacity = '0'; c.style.transform = 'translateY(40px) scale(.8)'; });
  if (reduced) deal(); else {
    fan.classList.add('shuffling');
    requestAnimationFrame(() => requestAnimationFrame(() => { stack(0, 0); sfx('flip');
      [[150, 1], [250, -1], [150, -1], [250, 1], [0, 0]].forEach(([t, k], n) => later(() => { stack(n === 4 ? 0 : 46, k); if (n < 4) sfx('tick'); }, 200 + n * 190));
      later(() => { els.forEach(c => c.style.transitionDuration = ''); fan.classList.remove('shuffling'); deal(); }, 1250); }));
  }
  let lastTop = 0;
  let lastSp = 0;
  const go = v => { const before = off; off = Math.max(-mid, Math.min(mid, v)); layout(); const t = Math.round(off); if (t !== lastTop) { lastTop = t; sfx('tick'); }
    const now = performance.now(); if (Math.abs(off - before) > .03 && now - lastSp > 140) { lastSp = now; sparkleCard(els.find(c => c.classList.contains('top')), 2); } };
  const ambientTimer = setInterval(() => { if (screen !== 's-pick') { clearInterval(ambientTimer); return; } sparkleCard(els.find(c => c.classList.contains('top')), 1); }, 1400);
  const glide = () => {   // inertia after release: the fan coasts and stops on the nearest card
    cancelAnimationFrame(raf);
    const step = () => {
      vel *= .93; const next = off + vel * 16;
      if (Math.abs(vel) < .0009 || next < -mid || next > mid) { go(Math.round(off)); fan.classList.remove('glide'); return; }
      go(next); raf = requestAnimationFrame(step);
    };
    fan.classList.add('glide'); raf = requestAnimationFrame(step);
  };
  // Card pick on pointerup (not click): after a drag the first tap opens the card at once.
  fan.onpointerdown = e => { if (picking) return; cancelAnimationFrame(raf); fan.classList.remove('glide'); fan.setPointerCapture(e.pointerId); down = true; moved = false; startX = lastX = e.clientX; startOff = off; vel = 0; lastT = performance.now(); fan.classList.add('drag'); };
  fan.onpointermove = e => {
    if (!down) return; const dx = e.clientX - startX; if (Math.abs(dx) > 8) moved = true;
    if (moved) { const now = performance.now(), dt = Math.max(1, now - lastT); vel = vel * .6 + (((e.clientX - lastX) / 40) / dt) * .4; lastX = e.clientX; lastT = now; go(startOff + dx / 40); }
  };
  const end = () => { if (!down) return; down = false; fan.classList.remove('drag'); if (Math.abs(vel) > .003) glide(); else go(Math.round(off)); };
  const choose = () => {   // the chosen card flies to the centre, the rest drop and fade, then the reveal
    if (picking) return; picking = true; sfx('pick'); fan.classList.add('picked'); $('#s-pick').classList.add('picking');   // title, date and captions fade out while the card flies up
    const t = els.find(c => c.classList.contains('top')) || els[mid];
    t.style.transform = 'translateY(calc(var(--fw) * -.3)) scale(1.35)'; t.style.transitionDuration = '.45s';
    later(reveal, reduced ? 0 : 460);
  };
  fan.onpointerup = () => { const tap = down && !moved; end(); if (tap) choose(); };
  fan.onpointercancel = end;
  fan.onkeydown = e => {
    if (e.key === 'ArrowLeft') go(Math.round(off) + 1); else if (e.key === 'ArrowRight') go(Math.round(off) - 1);
    else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(); }
  };
  fan.focus({ preventScroll: true });
}

const restart = () => { resetTheme(); seed = null; history.replaceState(null, '', location.pathname + `?lang=${lang}`); $('#share').textContent = ui.share; show('s-form'); };

// Fog transition: the screen is covered in fog, we switch screens at its peak, then the fog lifts.
function fogTo(fn) {
  if (reduced) return fn();
  const f = el('div', 'fog'); $('#phone').append(f);
  requestAnimationFrame(() => requestAnimationFrame(() => f.classList.add('in')));
  setTimeout(() => { fn(); f.classList.remove('in'); f.classList.add('out'); setTimeout(() => f.remove(), 520); }, 360);
}
$('#enter').onclick = () => fogTo(() => show('s-form'));
$('#form').onsubmit = e => {
  e.preventDefault();
  // both fields required (also not just spaces): browser message + highlight of the first empty one
  const empty = ['#f-name', '#f-company'].map($).find(i => !i.value.trim());
  if (empty) { empty.setCustomValidity(ui.required); empty.reportValidity(); empty.oninput = () => empty.setCustomValidity(''); return; }
  enableGyro(); pick();
};
$('#clear-form').onclick = () => {   // clears the fields and the saved data
  $('#form').reset(); store.set('sd_form', '{}');
  $('#f-industry').value = 'inne'; $('#f-stage').value = 'rozwoj'; $('#f-name').focus();
};
$('#more').onclick = openRead;
$('#again').onclick = restart;
$('#back').onclick = () => { if (screen === 's-pick') show('s-form'); else if (screen === 's-card') restart(); else { show('s-card'); $('#cardslot').append($('#card')); sizeCard(); } };
document.querySelectorAll('.tabs button').forEach(b => b.onclick = () => renderTab(b.dataset.tab));
$('#share').onclick = async () => {
  const url = `${location.origin}${location.pathname}?s=${seed}&lang=${lang}`;
  const text = ui.shareText.replace('{card}', cur.card.name[lang]);   // one inviting sentence with the name of the drawn card
  track('share', { method: 'link', card_id: cur.card.id });
  if (navigator.share) { try { await navigator.share({ title: ui.title, text, url }); } catch {} } else { await navigator.clipboard.writeText(`${text} ${url}`); $('#share').textContent = ui.copied; }
};
document.querySelectorAll('.langs button').forEach(b => b.onclick = async () => {
  if (b.dataset.lang === lang) return;
  lang = b.dataset.lang; track('language_change', { language: lang }); cur = null; const was = screen; await load(); paintConsent(); flickerTitle($('#s-intro h1')); show(was === 's-intro' ? 's-intro' : 's-form'); toggleMenu();
});

// Sound starts after the first gesture; the mute button shows the state.
for (const ev of ['pointerup', 'click', 'touchend', 'keydown']) document.addEventListener(ev, startAudio, { capture: true });
$('#share-img').onclick = () => { if (!cur) return; track('share', { method: 'image', card_id: cur.card.id }); shareImage({ ...cur, company: $('#f-company').value, lang, ui }); };
$('#menu-btn').onclick = toggleMenu;
// The music hint fades after the first gesture (it stays in the layout so nothing jumps under the finger; browsers do not allow earlier playback) or when sound is muted.
if (isMuted()) $('#music-hint').classList.add('gone');
else for (const ev of ['pointerup', 'click', 'touchend', 'keydown']) document.addEventListener(ev, () => $('#music-hint').classList.add('gone'), { once: true, capture: true }); $('#menu-back').onclick = closeMenu;
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
document.addEventListener('click', e => { if (e.target.closest('.cta, .mini, .tabs button') && !e.target.closest('#mute')) sfx('click'); });
$('#mute').onclick = () => { startAudio(); toggleMute(); paintMute(); const ic = $('#mute img'); ic.classList.remove('bump'); void ic.offsetWidth; ic.classList.add('bump'); if (!isMuted()) sfx('click'); };

pixelScale();
startBg(); cursorSparks();
await load();
flickerTitle($('#s-intro h1'));
show('s-intro');
// Card preview for checking the deck: ?card=ar00 (optionally &rev=1) shows the chosen card at once.
{
  const id = params.get('card');
  if (id && cards.some(c => c.id === id)) {
    preview = { id, rev: params.get('rev') === '1' };
    if (!$('#f-company').value) $('#f-company').value = 'Test'; if (!$('#f-name').value) $('#f-name').value = 'Anna';
    reveal();
  }
}

// The curtain fades out only when the fonts and the intro images are ready (min. 400 ms, max 4 s).
// Fonts are loaded with the Polish characters too (a separate latin-ext file), and emoji up front, so nothing flickers after the card is chosen.
const PL = 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ';
const emojiImgs = [...Object.values(SIGN), ...Object.values(ELEM), ...Object.values(SYM), '1F53A', '1F53B'].map(cp => { const i = new Image(); i.src = `img/emoji/U+${cp}.png`; return i; });
const ready = Promise.all([
  document.fonts.load('24px "Jacquard 12"', PL), document.fonts.load('18px "Geist Pixel"', PL),
  ...[...document.querySelectorAll('#s-intro img'), ...emojiImgs, ...['intro', 'pick', 'card', 'read'].map(k => { const i = new Image(); i.src = `img/ui/bg-${k}.png`; return i; })].map(i => i.decode().catch(() => {})),
]);
await Promise.race([Promise.all([ready, new Promise(r => setTimeout(r, 400))]), new Promise(r => setTimeout(r, 4000))]);
const loader = $('#loader');
loader.classList.add('hide');
setTimeout(() => loader.remove(), 700);

// PWA: a new service worker takes over the page at once. We reload immediately only on the intro screen and the form; during a draw
// or a reading we wait until the user is back on those screens (see show) so a reading is not lost. We look for updates on every return to the app and every 30 min.
if ('serviceWorker' in navigator) {
  const had = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.addEventListener('controllerchange', () => { if (!had) return; appStale = true; if (screen === 's-intro' || screen === 's-form') location.reload(); });
  navigator.serviceWorker.register('sw.js').then(reg => {
    const check = () => reg.update().catch(() => {});
    document.addEventListener('visibilitychange', () => { if (!document.hidden) check(); });
    setInterval(check, 30 * 60 * 1000);
  }).catch(() => {});
}

// Analytics consent: a banner on the first visit (only when a measurement ID is set) and a switch in the menu to change the choice.
function paintConsent() {
  const b = $('#consent-btn'); b.hidden = !gaEnabled(); b.textContent = gaConsent() === 'granted' ? ui.analyticsOn : ui.analyticsOff;
  $('#consent').hidden = !gaEnabled() || gaConsent() !== null;
}
const askConsent = v => { gaSetConsent(v); paintConsent(); if (v === 'granted') track('consent_granted'); };
$('#consent-yes').onclick = () => askConsent('granted');
$('#consent-no').onclick = () => askConsent('denied');
$('#consent-btn').onclick = () => askConsent(gaConsent() === 'granted' ? 'denied' : 'granted');
initAnalytics(); paintConsent();
