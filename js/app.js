import { draw, loadHistory, saveHistory, newSeed } from './deck.js';
import { compose } from './oracle.js';

const $ = s => document.querySelector(s);
const OFFER = 'https://whosz.pl/offer/?utm_source=tarot&utm_medium=app&utm_campaign=wrozba';
const ROMAN = ['0','I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI'];
const SYM = { wands: '🔥', cups: '💧', swords: '⚔', pentacles: '✦', major: '☾' };
const params = new URLSearchParams(location.search);
const store = { get: k => { try { return localStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch {} } };
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

let lang = params.get('lang') || store.get('sd_lang') || (navigator.language.startsWith('pl') ? 'pl' : 'en');
if (!['pl', 'en'].includes(lang)) lang = 'pl';
let ui, grammar, zodiac, cards, seed = params.get('s');

const show = id => { document.querySelectorAll('.screen').forEach(s => s.hidden = s.id !== id); };
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
  // Całość max 3 s: obrót 0,8 s, tekst 0,9-2,1 s, przyciski 2,2-2,8 s.
  const t = reduced ? 0 : 1;
  setTimeout(() => $('#card').classList.add('flip'), 50 * t);
  setTimeout(() => text.classList.add('in'), 900 * t);
  setTimeout(() => { actions.hidden = false; requestAnimationFrame(() => actions.classList.add('in')); }, 2200 * t);
  $('#offer').href = OFFER;
  $('#share').onclick = async () => {
    const url = `${location.origin}${location.pathname}?s=${seed}&lang=${lang}`;
    if (navigator.share) { try { await navigator.share({ title: ui.title, url }); } catch {} } else { await navigator.clipboard.writeText(url); $('#share').textContent = ui.copied; }
  };
}

function pick() {
  show('s-pick');
  const fan = $('#fan'); fan.replaceChildren();
  for (let i = 0; i < 5; i++) {
    const c = document.createElement('div'); c.className = 'card'; c.tabIndex = 0; c.role = 'button';
    c.innerHTML = '<div class="face back"></div>';
    c.onclick = reveal; c.onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') reveal(); };
    fan.append(c);
  }
}

$('#enter').onclick = () => show('s-form');
$('#form').onsubmit = e => { e.preventDefault(); pick(); };
$('#again').onclick = () => { seed = null; history.replaceState(null, '', location.pathname + `?lang=${lang}`); $('#share').textContent = ui.share; show('s-form'); };
$('#lang').onclick = async () => { lang = lang === 'pl' ? 'en' : 'pl'; store.set('sd_lang', lang); await load(); };

await load();
