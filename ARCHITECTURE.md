# ARCHITECTURE

Struktura katalogów jak w planie (`index.html`, `css/`, `js/`, `data/`, `img/`, `fonts/`, `audio/`, `sw.js`, `manifest.webmanifest`).

## Moduły (ES modules, brak globali poza `vendor/`)

| Plik | Eksport | Kontrakt |
| --- | --- | --- |
| `js/deck.js` | `newSeed()` | string base36 z `crypto.getRandomValues` |
| | `draw(seed, history)` | `{card, reversed}`; karta ≠ ostatnie z `history` (10), reversed ≈ 30% |
| | `loadHistory()` / `saveHistory(h)` | `localStorage`, try/catch |
| `js/oracle.js` | `compose({seed, card, reversed, name, zodiac, company, lang})` | `{parts:[{id, text}]}`, 5 części, ostatnia = puenta z usługą |
| `js/app.js` | — | ekrany 1-6, formularz, `?s=` i `?lang=`, przełącznik PL/EN |
| `js/fx.js` | `sparks(x,y)`, `shake()`, `bg(palette)` | respektuje reduced-motion |
| `js/audio.js` | `start()`, `sfx(name)`, `toggleMute()` | start po geście użytkownika |
| `js/share.js` | `shareLink(seed)`, `shareImage(result)` | link bez imienia i firmy |

## Dane (schematy w `schema/`)

- `data/cards.json` — 78 kart, schemat `schema/cards.schema.json`. Pola tekstowe to `{pl, en}`.
- `data/grammar.{pl,en}.json` — gramatyka Tracery. Wymagane symbole: `origin`, `wezwanie`, `znaczenie`, `omen`, `puenta`, `cta`.
- `data/zodiac.{pl,en}.json` — 12 znaków: `id`, `element`, `nom`, `gen`, `dat` (tylko PL), `omens[]`.

## Walidacja (skrypty w `tools/`)

- `tools/validate_cards.py` — JSON Schema dla `cards.json`.
- `tools/test_grammar.py` — symbole zdefiniowane, 100 losowych wróżb w PL i EN, każda ma puentę.
- `tools/check_png.py` — rozmiar 144×216 i liczba kolorów.

## Serwer

Apache, `whosz.pl/tarot/`. `sw.js` i `index.html` bez cache, reszta długo. `audio/*.mp3` poza precache.
