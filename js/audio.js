// Dźwięk: muzyka z pliku (pętla) po pierwszym geście użytkownika + efekty ZzFX (generowane, bez plików).
// Wyciszenie jest zapamiętywane w localStorage.
const PRESETS = {  // parametry zzfx(volume, randomness, frequency, attack, sustain, release, shape, shapeCurve, slide, deltaSlide, pitchJump, pitchJumpTime, repeatTime, noise, modulation, bitCrush, delay, sustainVolume, decay, tremolo)
  click: [[.5, , 900, .01, .01, .03, 1, 1.5, , , , , , , , , , .8, .02]],
  tick: [[.25, , 1600, , .005, .01, 1, , , , , , , , , , , .6, .01]],
  pick: [[.6, , 180, .02, .08, .2, 4, 2, -8, , , , , .6, , , , .8, .1]],
  flip: [[.5, , 320, .01, .05, .12, 4, 1.5, 12, , , , , .3, , , , .7, .05]],
  hit: [[.9, , 90, .01, .1, .35, 2, 2, , , , , , .2, , .1, , .8, .15], [.35, , 1046, .02, .12, .5, 1, 1.2, , , , , , , , , .08, .7, .1]],
  hitRev: [[1, , 55, .02, .25, .6, 2, 3, -3, , , , , .3, , .2, , .9, .3], [.4, , 196, .02, .2, .6, 3, 1.5, -1, , , , , , , , .12, .7, .2]],
};
const get = () => { try { return localStorage.getItem('sd_mute') === '1'; } catch { return false; } };
const MUSIC = 'audio/spoooky-theme-mm.mp3';
let muted = get(), music = null, started = false, lastErr = '', cachedTried = false;

// Muzyka offline: po kilku sekundach grania zapisujemy plik w osobnej pamięci (sd-audio, nie jest czyszczona przy aktualizacjach).
// Gdy sieci brak i odtwarzacz zgłasza błąd, gramy z zapisanej kopii.
async function cacheMusic() {
  try {
    if (!('caches' in window) || (navigator.connection && navigator.connection.saveData)) return;
    const c = await caches.open('sd-audio'); await Promise.all(['audio/candlelit-tarot.mp3', 'audio/spoooky-theme.mp3'].map(u => c.delete(u)));   // sprzątanie po poprzednim utworze
    if (await c.match(MUSIC)) return;
    const r = await fetch(MUSIC); if (r.ok) await c.put(MUSIC, r);
  } catch {}
}
async function playFromCache() {
  try {
    const c = await caches.open('sd-audio'), r = await c.match(MUSIC); if (!r) return false;
    music.src = URL.createObjectURL(await r.blob()); await music.play(); return true;
  } catch { return false; }
}

export const isMuted = () => muted;
export const audioError = () => lastErr;   // do diagnozy w menu

// Wywoływane przy każdym geście: iOS/Safari wymaga play() wewnątrz click/touchend, więc ponawiamy, aż muzyka ruszy.
export function start() {
  try { zzfxX.resume(); } catch {}
  if (!started) {
    started = true; music = new Audio(MUSIC); music.loop = true; music.volume = .45;
    music.addEventListener('error', async () => { if (!muted && !navigator.onLine && await playFromCache()) { lastErr = ''; return; } lastErr = 'media error ' + (music.error && music.error.code); });
    music.addEventListener('playing', () => { lastErr = ''; if (!cachedTried) { cachedTried = true; setTimeout(cacheMusic, 8000); } });
  }
  if (!muted && music.paused) music.play().catch(e => { if (e.name !== 'NotAllowedError') lastErr = e.name; });
}

export function toggleMute() {
  muted = !muted;
  try { localStorage.setItem('sd_mute', muted ? '1' : '0'); } catch {}
  if (music) muted ? music.pause() : music.play().catch(() => {});
  return muted;
}

export function sfx(name) {
  if (muted || !started || typeof zzfx !== 'function') return;
  for (const p of PRESETS[name] || []) zzfx(...p);
}

// Muzyka i dźwięk milkną, gdy aplikacja znika z ekranu (przełączenie na inną aplikację, blokada ekranu, inna karta),
// i wracają, gdy użytkownik wraca (o ile dźwięk nie jest wyciszony).
let resumeMusic = false;
function onHidden() {
  if (music && !music.paused) { resumeMusic = true; music.pause(); }
  try { zzfxX.suspend(); } catch {}
}
function onVisible() {
  try { zzfxX.resume(); } catch {}
  if (resumeMusic && !muted && music) music.play().catch(() => {});
  resumeMusic = false;
}
document.addEventListener('visibilitychange', () => (document.hidden ? onHidden() : onVisible()));
addEventListener('pagehide', onHidden);
addEventListener('pageshow', e => { if (e.persisted && !document.hidden) onVisible(); });
