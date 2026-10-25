# Brief: Spoooky Deck

A dark pixel-art tarot oracle for companies. Input: a name (≤30 characters), a zodiac sign (12), a company (≤60) and its industry and stage. The user draws one of 78 cards, upright or reversed (~30%). The reading about the company always ends with the conclusion that a designer is needed, followed by a link to https://whosz.pl/offer/ and another draw.

Rules:
- Plain static files, ES modules, no backend and no build step. Relative paths (works at `whosz.pl/tarot/`).
- Polish and English from day one. Texts live in `data/*.{pl,en}.json`, never in the code.
- User input is only ever inserted as `textContent`. Nothing leaves the device and nothing but the seed (`?s=`) goes into the share link.
- Style: Dead Cells (navy, gold, candles), Balatro-like animation (springy, shiny). The palette is in `STYLE.md`.
- Respect `prefers-reduced-motion`. Text contrast ≥ 4.5:1. Buttons ≥ 44 px.
- Texts are checked with the `humanizer-pl` skill for Polish and `humanizer` for English (`.claude/skills/`).
- Music: an AI-generated loop (`audio/spoooky-theme-mm.mp3`), started after the first gesture, with a mute button.
