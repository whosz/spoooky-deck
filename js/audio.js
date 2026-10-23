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
let muted = get(), music = null, started = false, lastErr = '';

export const isMuted = () => muted;
export const audioError = () => lastErr;   // do diagnozy w menu

// Wywoływane przy każdym geście: iOS/Safari wymaga play() wewnątrz click/touchend, więc ponawiamy, aż muzyka ruszy.
export function start() {
  try { zzfxX.resume(); } catch {}
  if (!started) {
    started = true; music = new Audio('audio/candlelit-tarot.mp3'); music.loop = true; music.volume = .45;
    music.addEventListener('error', () => { lastErr = 'media error ' + (music.error && music.error.code); });
    music.addEventListener('playing', () => { lastErr = ''; });
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
