// Google Analytics 4 behind a consent banner (Consent Mode v2, default: denied).
// Without a measurement ID, or without the user's consent, nothing is loaded and nothing is sent.
// Events never contain the name or the company: only the card, position, industry, stage and language.
const GA_ID = 'G-751JS5MMX0';   // measurement ID, e.g. 'G-XXXXXXXXXX'; empty = analytics fully disabled
const id = () => (window.SD_GA_ID !== undefined ? window.SD_GA_ID : GA_ID);   // window.SD_GA_ID overrides the ID in tests (an empty string disables analytics)
const KEY = 'sd_consent';
const store = { get: () => { try { return localStorage.getItem(KEY); } catch { return null; } }, set: v => { try { localStorage.setItem(KEY, v); } catch {} } };
let loaded = false;

export const enabled = () => !!id();
export const consent = () => store.get();   // 'granted' | 'denied' | null (not asked yet)

function load() {
  if (loaded || !enabled()) return;
  loaded = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied' });
  gtag('js', new Date());
  gtag('consent', 'update', { analytics_storage: 'granted' });
  gtag('config', id(), { allow_google_signals: false, allow_ad_personalization_signals: false });
  const s = document.createElement('script'); s.async = true; s.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(id())}`;
  document.head.append(s);
}

function dropCookies() {   // withdrawing consent removes the Google cookies of this site
  window['ga-disable-' + id()] = true;
  for (const c of document.cookie.split(';')) { const n = c.split('=')[0].trim(); if (/^_ga/.test(n)) document.cookie = `${n}=; Max-Age=0; path=/`; }
}

export function setConsent(v) {
  store.set(v);
  if (v === 'granted') { window['ga-disable-' + id()] = false; load(); } else if (loaded) { dropCookies(); }
}

export function initAnalytics() { if (enabled() && consent() === 'granted') load(); }

export function track(name, params = {}) { if (enabled() && consent() === 'granted' && window.gtag) window.gtag('event', name, params); }
