import { draw, loadHistory, saveHistory, newSeed } from './deck.js';
import { compose } from './oracle.js';

const $ = s => document.querySelector(s);
const OFFER = 'https://whosz.pl/offer/?utm_source=tarot&utm_medium=app&utm_campaign=wrozba';
const ROMAN = ['0','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI'];
const SIGN = { aries:'♈', taurus:'♉', gemini:'♊', cancer:'♋', leo:'♌', virgo:'♍', libra:'♎', scorpio:'♏', sagittarius:'♐', capricorn:'♑', aquarius:'♒', pisces:'♓' };
const ELEM = { fire:'🔥', earth:'🌍', air:'💨', water:'💧' };
const SYM = { wands: '🔥', cups: '💧', swords: '⚔', pentacles: '✦', major: '☾' };
const params = new URLSearchParams(location.search);
const store = { get: k => { try { return localStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch {} } };
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

let lang = params.get('lang') || store.get('sd_lang') || (navigator.language.startsWith('pl') ? 'pl' : 'en');
if (!['pl', 'en'].includes(lang)) lang = 'pl';
let ui, grammar, zodiac, cards, seed = params.get('s');

const show = id => {
  document.querySelectorAll('.screen').forEach(s => s.hidden = s.id !== id);
  $('#back').style.visibility = id === 's-pick' || id === 's-read' ? 'visible' : 'hidden';
  $('#bar-title').textContent = '';
};
const getJSON = u => fetch(u).then(r => r.json());

async function load() {
  [ui, grammar, zodiac, cards] = await Promise.all([getJSON(`data/ui.${lang}.json`), getJSON(`data/grammar.${lang}.json`), getJSON(`data/zodiac.${lang}.json`), getJSON('data/cards.json')]);
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-ui]').forEach(e => e.textContent = ui[e.dataset.ui]);
  $('#lang').textContent = lang === 'pl' ? 'EN' : 'PL';
  $('#f-zodiac').replaceChildren(...zodiac.map(z => new Option(z.name, z.id)));
  const saved = JSON.parse(store.get('sd_form') || '{}');
  $('#f-name').value = saved.name || '';
  $('#f-company').value = saved.company || '';
  if (saved.zodiac) $('#f-zodiac').value = saved.zodiac;
}

function cardEl(c, reversed) {
  const el = $('#card');
  el.className = 'card' + (reversed ? ' rev' : '');
  const f = el.querySelector('.front');
  f.replaceChildren();
  for (const [cls, t] of [['num', c.arcana === 'major' ? ROMAN[c.number] : c.number], ['sym', SYM[c.suit || 'major']], ['nm', c.name[lang]]]) {
    const d = document.createElement('div'); d.className = cls; d.textContent = t; f.append(d);
  }
}

function reveal() {
  const form = { name: $('#f-name').value, zodiac: $('#f-zodiac').value, company: $('#f-company').value };
  store.set('sd_form', JSON.stringify(form));
  const hist = loadHistory();
  if (!seed) seed = newSeed(cards, hist);
  const { card, reversed } = draw(seed, cards);
  saveHistory([...hist, card.id]);
  const parts = compose({ seed, card, reversed, name: form.name, zodiac: zodiac.find(z => z.id === form.zodiac), company: form.company, lang, grammar, ui });
  show('s-read');
  const text = $('#text'), actions = $('#actions');
  text.classList.remove('in'); actions.classList.remove('in'); actions.hidden = true;
  text.textContent = parts.map(p => p.text).join(' ');
  cardEl(card, reversed);
  $('#bar-title').textContent = card.name[lang];
  const z = zodiac.find(z => z.id === form.zodiac);
  const info = $('#info'); info.classList.remove('in'); info.replaceChildren();
  for (const [ic, lb, vl] of [
    [SYM[card.suit || 'major'], ui.arcana, card.arcana === 'major' ? ui.major : ui.minor],
    [SIGN[z.id], ui.sign, z.name],
    [ELEM[z.element], ui.element, ui[z.element]],
    [reversed ? '▼' : '▲', ui.position, reversed ? ui.reversed : ui.upright]]) {
    const d = document.createElement('div');
    for (const [c, t] of [['ic', ic], ['lb', lb], ['vl', vl]]) { const e = document.createElement('span'); e.className = c; e.textContent = t; d.append(e); }
    info.append(d);
  }
  // Całość max 2 s: obrót 0,6 s, tekst 0,5-1,3 s, przyciski 1,3-1,9 s.
  const t = reduced ? 0 : 1;
  setTimeout(() => $('#card').classList.add('flip'), 50 * t);
  setTimeout(() => { text.classList.add('in'); info.classList.add('in'); }, 500 * t);
  setTimeout(() => { actions.hidden = false; requestAnimationFrame(() => actions.classList.add('in')); }, 1300 * t);
  $('#offer').href = OFFER;
  $('#share').onclick = async () => {
    const url = `${location.origin}${location.pathname}?s=${seed}&lang=${lang}`;
    if (navigator.share) { try { await navigator.share({ title: ui.title, url }); } catch {} } else { await navigator.clipboard.writeText(url); $('#share').textContent = ui.copied; }
  };
}

function pick() {
  show('s-pick');
  $('#date').textContent = new Date().toLocaleDateString(lang, { weekday: 'long', day: 'numeric', month: 'long' });
  const fan = $('#fan'), N = 13, STEP = 9, mid = (N - 1) / 2;
  fan.replaceChildren();
  const els = Array.from({ length: N }, () => { const c = document.createElement('div'); c.className = 'fcard'; c.setAttribute('aria-hidden', 'true'); fan.append(c); return c; });
  let off = 0, startX = 0, startOff = 0, moved = false, down = false;
  const layout = () => els.forEach((c, i) => {
    const d = i - mid + off, top = Math.abs(d) < 0.5;
    c.style.transform = `rotate(${d * STEP}deg)${top ? ' translateY(-24px)' : ''}`;
    c.classList.toggle('top', top);
    c.style.zIndex = N - Math.round(Math.abs(d));
  });
  const go = v => { off = Math.max(-mid, Math.min(mid, v)); layout(); };
  fan.onpointerdown = e => { down = true; moved = false; startX = e.clientX; startOff = off; fan.classList.add('drag'); };
  fan.onpointermove = e => { if (!down) return; const dx = e.clientX - startX; if (Math.abs(dx) > 6) moved = true; go(startOff + dx / 40); };
  const end = () => { if (!down) return; down = false; fan.classList.remove('drag'); go(Math.round(off)); };
  fan.onpointerup = fan.onpointercancel = fan.onpointerleave = end;
  fan.onclick = () => { if (!moved) reveal(); };
  fan.onkeydown = e => {
    if (e.key === 'ArrowLeft') go(Math.round(off) + 1); else if (e.key === 'ArrowRight') go(Math.round(off) - 1);
    else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); reveal(); }
  };
  layout(); fan.focus({ preventScroll: true });
}

$('#enter').onclick = () => show('s-form');
$('#form').onsubmit = e => { e.preventDefault(); pick(); };
const restart = () => { seed = null; history.replaceState(null, '', location.pathname + `?lang=${lang}`); $('#share').textContent = ui.share; show('s-form'); };
$('#again').onclick = $('#back').onclick = restart;
$('#lang').onclick = async () => { lang = lang === 'pl' ? 'en' : 'pl'; store.set('sd_lang', lang); await load(); };

await load();
show('s-intro');
