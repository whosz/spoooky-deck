# Spoooky Deck: a pixel-art tarot oracle for companies

A case study of a project built in two days (23-24 October 2026) by Claude (Anthropic) under the direction of Mateusz Staniszewski (whosz.pl), then refined over the following days. Mateusz led the art direction and judged every stage; Claude wrote the code and the copy and generated the artwork.

Live: https://whosz.pl/tarot/ · Code: https://github.com/whosz/spoooky-deck

## In short

The user enters a name, a zodiac sign, a company and its industry and stage, picks a card from a fan of 78, and gets a reading about the company's future. The reading always ends with the conclusion that the company needs a designer, followed by a link to the whosz.pl offer. It is a playful lead magnet for owners of small businesses and start-ups, who are the audience of the whosz.pl offer.

The result is a PWA (installable on a phone, works offline) in Polish and English, written without a framework or a build step: plain HTML, CSS and JavaScript files uploaded to an ordinary Apache server.

## Goal and constraints

- **Goal:** a memorable, shareable hook that leads to the offer. The tone is mysterious and a little ominous like in a game, but kind at the end.
- **Constraints we set ourselves:** static files with no backend; no personal data leaves the phone (the share link carries only the draw seed, never a name or a company); everything in one consistent pixel style.

## How it was built

| Stage | What we did |
|---|---|
| Contracts | `BRIEF.md`, JSON schemas for the cards, the reading grammar and the zodiac signs, and a description of the modules. They made it possible to hand out tasks in parallel. |
| Reading engine | A Tracery grammar with seed-dependent randomness (seedrandom). The card, position (upright or reversed), sign, industry, stage and service decide the text. A test runs 7488 combinations (78 cards × 2 positions × 12 signs, with every industry and stage, in 2 languages). |
| Content | 78 cards in Polish and English, 312 meaning sentences, 48 sign omens, and 60 sentences about industries and company stages. Written by agents (Haiku, then Sonnet) against a schema, with a script validating each batch. Edited with the humanizer skills. |
| Interface | Mobile first; on a desktop the app is a phone-sized window in a picture frame. Pixel 9-slice frames, fonts, scene backgrounds. |
| Deck | First hand-drawn illustrations from code, then 78 cards from an image model (Flux 2 Pro), reduced by script to a 64×96 grid and 16 colours. |
| Animation and sound | Shuffling, dealing, a fan with inertia, sparks, shine, tilt following the cursor, gyroscope or drag, ZzFX effects, and a music loop generated with an AI model. |
| PWA and release | Manifest, service worker, icons, `.htaccess`, a shareable reading image and a link-preview image. Tests on production after every stage. |

## Key decisions

1. **Whole-pixel scaling.** Pixels looked uneven because the artwork was scaled by fractions (e.g. 1.54×). Card, background and frame sizes are now computed as a whole number of device pixels (on a 2× phone a 64×96 card is drawn at exactly 10 device pixels per art pixel), and verified by measurement. Rotating a card blurs the pixels, so a resting card does not rotate and the 3D effect switches on only while it moves.
2. **A style described in words, not images.** When choosing a style we were given examples from other people's paid decks. I reverted the generation that used them as reference images and described the style in words instead (palette, outlines, gradients, lighting), so the cards are original.
3. **Privacy by design.** The name and the company are inserted as plain text, with the grammar's control characters stripped. Nothing is sent to a server.
4. **The server is the source of truth, the cache is a fallback.** The service worker fetches fresh files first and uses the cache only offline. An earlier version with the opposite order kept serving an old version to users after a new one was deployed. Later, modules and data also got a version in their URL (`?v=N`), so a reload never mixes old and new files.
5. **Automation and tests.** Validators for cards and grammar, a test of all reading combinations, a browser smoke test with regression checks, an update test, a service worker generator and image-processing scripts. Every agent result was checked by a script before it entered the project.

## Problems and how we solved them

- **Music and autoplay.** Browsers block sound until the screen is touched, and Safari requires playback to start inside the click. The music therefore starts on the first gesture and retries, and the intro screen shows a hint. It pauses when the user leaves the app and resumes on return.
- **"Yellow stripes" in the fan.** The cause was clipped card shadows and the bottom edges of distant cards, not one bug. I hid distant cards, turned shadows off while shuffling and replaced the glow with a gradient.
- **Buttons shifting under the finger.** The music hint left the layout after the first tap and moved the button, so the first tap missed. A touch test on an emulated phone found it.
- **Polish grammar.** Names and company names cannot be inflected safely, so templates use them in the nominative and inside quotation marks, and the element sentences also needed forms without inflection.
- **Stale versions after an update.** Users reported an old look staying behind. Reproducing an upgrade from a real earlier version showed that a reload loaded a new `app.js` together with an old cached module and hung. Versioned module URLs, periodic update checks and a deferred reload (never in the middle of a draw) fixed it, and a test now covers it.
- **Animations stopping after a quick swipe.** Tapping a card during the fan's inertia left a CSS class that disabled all transitions. A user's screen recording led to the cause, and a regression test now guards it.

## Working with AI

- **Division of roles:** the main model (Sonnet 5.5) ran the project and the code, while helper agents wrote the content (Haiku) and drew cards from code (Sonnet). Each agent received a short contract and its own piece of work, and a script checked the result.
- **Image generation:** Flux 2 Pro through the Replicate API, reduced by script to 16 colours. Mateusz steered the choice of variants, colours and layout with screenshots and samples. Generation cost a few dollars in total. The music was generated with AI models too (ACE-Step first, then MiniMax Music).
- **My role in the iterations:** dozens of short notes from Mateusz about layout, sizes and looks (e.g. "background 15% darker", "font 2 px smaller") were applied, measured in a browser and deployed to production. Precise notes made for fast, small loops. For changes that alter the look, I showed a sample first.
- **What went wrong:** the first illustrations drawn from code looked childish ("as if a child made them") and the first backgrounds got in the way of reading the title. Switching to image models and a simpler, darker layout fixed both.

## Results

- 78 cards, 2 languages, about 190 commits.
- About 850 lines of our own JavaScript (without libraries) and about 450 lines of CSS, so an app without a framework.
- The deck weighs 316 KB; all graphics and data come to about 1 MB (without the music), and about 160 files are cached for offline use.
- A dozen scripts in `tools/` (validation, tests, a smoke test, an update test, image generation, deployment).

## Limitations and next steps

- The app was tested in a headless browser (on simulated phones, including the narrowest, 320 px) by a smoke script that walks the whole flow in both languages and checks errors, server responses, the form, tabs, the menu and the reading image (127 checks, including regressions). Mateusz confirmed the flow, installation and sharing on a real phone.
- Licence details are in `docs/licensing.md`.
- Ideas for later: a history of readings on the device, an accessibility audit.
