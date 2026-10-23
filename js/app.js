import { draw, loadHistory, saveHistory, newSeed } from './deck.js';
import { compose } from './oracle.js';
import { startBg, revealFx, tiltCard, enableGyro } from './fx.js';
import { shareImage } from './share.js';
import { start as startAudio, sfx, toggleMute, isMuted, audioError } from './audio.js';

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

// Start zawsze po polsku (angielski tylko przez przełącznik lub ?lang=en z linku).
let lang = params.get('lang') || 'pl';
if (!['pl', 'en'].includes(lang)) lang = 'pl';
let untilt = () => {}, preview = null;
let ui, grammar, zodiac, cards, seed = params.get('s'), cur, screen = 's-intro', tab = 'fortune';

// Menu (hamburger): język, dźwięk, informacje o twórcy.
function paintMute() { $('#mute img').src = `img/emoji/U+${isMuted() ? '1F507' : '1F50A'}.png`; $('#mute span').textContent = ui ? (isMuted() ? ui.soundOff : ui.soundOn) + (audioError() ? ` (${audioError()})` : '') : ''; }
function closeMenu() { $('#menu').hidden = $('#menu-back').hidden = true; $('#menu-btn').setAttribute('aria-expanded', 'false'); }
function toggleMenu() { paintMute(); const open = $('#menu').hidden; $('#menu').hidden = $('#menu-back').hidden = !open; $('#menu-btn').setAttribute('aria-expanded', String(open)); }

const getJSON = u => fetch(u).then(r => r.json());

function show(id) {
  screen = id;
  document.querySelectorAll('.screen').forEach(s => s.hidden = s.id !== id);
  $('#back').style.visibility = ['s-pick', 's-card', 's-read'].includes(id) ? 'visible' : 'hidden';
  closeMenu();
  $('#bar-title').textContent = id === 's-card' && cur ? cur.card.name[lang] : '';
  $('#view').scrollTop = 0;
}

async function load() {
  [ui, grammar, zodiac, cards] = await Promise.all([getJSON(`data/ui.${lang}.json`), getJSON(`data/grammar.${lang}.json`), getJSON(`data/zodiac.${lang}.json`), getJSON('data/cards.json')]);
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-ui]').forEach(e => e.textContent = ui[e.dataset.ui]);
  document.querySelectorAll('.langs button').forEach(b => b.setAttribute('aria-pressed', b.dataset.lang === lang));
  paintMute();
  $('#f-zodiac').replaceChildren(...zodiac.map(z => new Option(z.name, z.id)));
  const saved = JSON.parse(store.get('sd_form') || '{}');
  $('#f-name').value = saved.name || '';
  $('#f-company').value = saved.company || '';
  if (saved.zodiac) $('#f-zodiac').value = saved.zodiac;
}

const em = cp => { const i = document.createElement('img'); i.className = 'emoji'; i.src = `img/emoji/U+${cp}.png`; i.alt = ''; return i; };
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };

function fillCard({ card, reversed }) {
  const c = $('#card');
  c.className = 'card' + (reversed ? ' rev' : '');
  const f = c.querySelector('.front');
  const sym = el('div', 'sym'); sym.append(em(SYM[card.suit || 'major']));
  f.style.backgroundImage = `url(img/cards/${card.id}.png)`;
  f.replaceChildren(el('div', 'num', card.arcana === 'major' ? ROMAN[card.number] : card.number), sym, el('div', 'nm', card.name[lang]));
}

function reveal() {
  const form = { name: $('#f-name').value, zodiac: $('#f-zodiac').value, company: $('#f-company').value };
  store.set('sd_form', JSON.stringify(form));
  const hist = loadHistory();
  if (!seed) seed = newSeed(cards, hist);
  const { card, reversed } = preview ? { card: cards.find(c => c.id === preview.id), reversed: preview.rev } : draw(seed, cards);
  saveHistory([...hist, card.id]);
  const z = zodiac.find(z => z.id === form.zodiac);
  const { parts, quote } = compose({ seed, card, reversed, name: form.name, zodiac: z, company: form.company, lang, grammar, ui });
  cur = { card, reversed, z, parts, quote };

  // Elementy .fade zerujemy bez przejścia PRZED pokazaniem ekranu (inaczej przy kolejnym losowaniu gasły i zapalały się ponownie).
  const fades = document.querySelectorAll('#s-card .fade');
  fades.forEach(f => { f.style.transition = 'none'; f.classList.remove('in'); });
  show('s-card');
  $('#cardslot').append($('#card'));
  untilt(); untilt = tiltCard($('#cardslot'));
  fillCard(cur);
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
  $('#offer').href = OFFER;
  // Całość max 2 s: obrót 0,6 s, potem cytat, info i przycisk razem (0,5-1,3 s). Miejsce zarezerwowane, nic nie skacze.
  const t = reduced ? 0 : 1;
  sfx('pick');
  setTimeout(() => { $('#card').classList.add('flip'); sfx('flip'); }, 50 * t);
  setTimeout(() => { sfx(reversed ? 'hitRev' : 'hit'); revealFx(reversed, $('#card')); }, 300 * t);
  setTimeout(() => fades.forEach(f => f.classList.add('in')), 500 * t);
}

function renderTab(name) {
  tab = name;
  document.querySelectorAll('.tabs button').forEach(b => b.setAttribute('aria-selected', b.dataset.tab === name));
  const box = $('#tabtext'); box.replaceChildren();
  const p = (t, cls) => box.append(el('p', cls, t));
  const side = cur.reversed ? cur.card.rev : cur.card.up;
  if (name === 'fortune') {
    const [w, zn, om, pu, cta] = cur.parts.map(x => x.text);
    p(w); p(zn); p(om); p(pu, 'lead'); p(cta);
  } else if (name === 'card') {
    p(`${cur.card.name[lang]}, ${cur.reversed ? ui.reversed : ui.upright}`, 'lead');
    p(side.keywords[lang].join(', '));
    side.sentences[lang].forEach(s => p(s));
    p(cur.card.business[lang]);
  } else {
    p(`${cur.z.name}, ${ui[cur.z.element]}`, 'lead');
    p(cur.parts[2].text);
  }
  box.style.animation = 'none'; void box.offsetWidth; box.style.animation = '';
}

function openRead() {
  show('s-read');
  $('#artslot').append($('#card'));
  $('#rname').textContent = cur.card.name[lang];
  renderTab('fortune');
}

function pick() {
  show('s-pick');
  $('#date').textContent = new Date().toLocaleDateString(lang, { weekday: 'long', day: 'numeric', month: 'long' });
  const fan = $('#fan'), N = 21, STEP = 9, mid = (N - 1) / 2;
  fan.replaceChildren();
  const els = Array.from({ length: N }, () => { const c = el('div', 'fcard'); c.setAttribute('aria-hidden', 'true'); fan.append(c); return c; });
  let off = 0, startX = 0, startOff = 0, moved = false, down = false;
  const layout = () => els.forEach((c, i) => {
    const d = i - mid + off, top = Math.abs(d) < 0.5;
    c.style.transform = `rotate(${d * STEP}deg)${top ? ' translateY(calc(var(--fw) * .4425 - 24px)) scale(1.15)' : ''}`;
    c.classList.toggle('top', top);
    c.style.zIndex = N - Math.round(Math.abs(d));
  });
  let lastTop = 0;
  const go = v => { off = Math.max(-mid, Math.min(mid, v)); layout(); const t = Math.round(off); if (t !== lastTop) { lastTop = t; sfx('tick'); } };
  // Wybór karty na pointerup (nie na click): po przeciągnięciu pierwszy tap od razu otwiera kartę.
  fan.onpointerdown = e => { fan.setPointerCapture(e.pointerId); down = true; moved = false; startX = e.clientX; startOff = off; fan.classList.add('drag'); };
  fan.onpointermove = e => { if (!down) return; const dx = e.clientX - startX; if (Math.abs(dx) > 8) moved = true; if (moved) go(startOff + dx / 40); };
  const end = () => { if (!down) return; down = false; fan.classList.remove('drag'); go(Math.round(off)); };
  fan.onpointerup = () => { const tap = down && !moved; end(); if (tap) reveal(); };
  fan.onpointercancel = end;
  fan.onkeydown = e => {
    if (e.key === 'ArrowLeft') go(Math.round(off) + 1); else if (e.key === 'ArrowRight') go(Math.round(off) - 1);
    else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); reveal(); }
  };
  layout(); fan.focus({ preventScroll: true });
}

const restart = () => { seed = null; history.replaceState(null, '', location.pathname + `?lang=${lang}`); $('#share').textContent = ui.share; show('s-form'); };

$('#enter').onclick = () => show('s-form');
$('#form').onsubmit = e => { e.preventDefault(); enableGyro(); pick(); };
$('#more').onclick = openRead;
$('#again').onclick = restart;
$('#back').onclick = () => { if (screen === 's-pick') show('s-form'); else if (screen === 's-card') restart(); else { show('s-card'); $('#cardslot').append($('#card')); } };
document.querySelectorAll('.tabs button').forEach(b => b.onclick = () => renderTab(b.dataset.tab));
$('#share').onclick = async () => {
  const url = `${location.origin}${location.pathname}?s=${seed}&lang=${lang}`;
  if (navigator.share) { try { await navigator.share({ title: ui.title, url }); } catch {} } else { await navigator.clipboard.writeText(url); $('#share').textContent = ui.copied; }
};
document.querySelectorAll('.langs button').forEach(b => b.onclick = async () => {
  if (b.dataset.lang === lang) return;
  lang = b.dataset.lang; cur = null; const was = screen; await load(); show(was === 's-intro' ? 's-intro' : 's-form'); toggleMenu();
});

// Dźwięk startuje po pierwszym geście; przycisk wyciszenia pokazuje stan.
for (const ev of ['pointerup', 'click', 'touchend', 'keydown']) document.addEventListener(ev, startAudio, { capture: true });
$('#share-img').onclick = () => cur && shareImage({ ...cur, company: $('#f-company').value, lang, ui });
$('#menu-btn').onclick = toggleMenu;
// Podpowiedź o muzyce gaśnie po pierwszym geście (zostaje w układzie, żeby nic nie przeskoczyło pod palcem) (przeglądarki nie pozwalają grać wcześniej) albo gdy dźwięk jest wyciszony.
if (isMuted()) $('#music-hint').classList.add('gone');
else for (const ev of ['pointerup', 'click', 'touchend', 'keydown']) document.addEventListener(ev, () => $('#music-hint').classList.add('gone'), { once: true, capture: true }); $('#menu-back').onclick = closeMenu;
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
document.addEventListener('click', e => { if (e.target.closest('.cta, .mini, .tabs button') && !e.target.closest('#mute')) sfx('click'); });
$('#mute').onclick = () => { startAudio(); toggleMute(); paintMute(); };

startBg();
await load();
show('s-intro');
// Podgląd karty do kontroli talii: ?card=ar00 (opcjonalnie &rev=1) od razu pokazuje wybraną kartę.
{
  const id = params.get('card');
  if (id && cards.some(c => c.id === id)) {
    preview = { id, rev: params.get('rev') === '1' };
    if (!$('#f-company').value) $('#f-company').value = 'Test'; if (!$('#f-name').value) $('#f-name').value = 'Anna';
    reveal();
  }
}

// Zasłona znika przez fade dopiero, gdy fonty i obrazki ekranu startowego są gotowe (min. 400 ms, max 4 s).
// Fonty ładujemy też z polskimi znakami (osobny plik latin-ext), a emoji z góry, żeby nic nie migało po wyborze karty.
const PL = 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ';
const emojiImgs = [...Object.values(SIGN), ...Object.values(ELEM), ...Object.values(SYM), '1F53A', '1F53B'].map(cp => { const i = new Image(); i.src = `img/emoji/U+${cp}.png`; return i; });
const ready = Promise.all([
  document.fonts.load('24px "Jacquard 12"', PL), document.fonts.load('18px "Geist Pixel"', PL),
  ...[...document.querySelectorAll('#s-intro img'), ...emojiImgs].map(i => i.decode().catch(() => {})),
]);
await Promise.race([Promise.all([ready, new Promise(r => setTimeout(r, 400))]), new Promise(r => setTimeout(r, 4000))]);
const loader = $('#loader');
loader.classList.add('hide');
setTimeout(() => loader.remove(), 700);

// PWA: service worker przejmuje stronę od razu po aktualizacji; jednorazowo przeładowujemy, żeby załadować nowe pliki.
if ('serviceWorker' in navigator) {
  const had = !!navigator.serviceWorker.controller; let reloaded = false;
  navigator.serviceWorker.addEventListener('controllerchange', () => { if (had && !reloaded) { reloaded = true; location.reload(); } });
  navigator.serviceWorker.register('sw.js').catch(() => {});
}
