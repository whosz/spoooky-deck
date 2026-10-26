# Licences and terms of use: Spoooky Deck

Status as of 24 October 2026. This document describes the terms under which each element of the app can be used, especially for commercial use. The app is a lead magnet for whosz.pl, so when it is published on a business site it should be treated as commercial use.

This is not legal advice. The information about Suno, Olde Tome and Flux comes from the vendors' pages and secondary sources (listed at the end). Terms change, so check them again before publishing.

## Summary

| Element | Source | Commercial use | What to do |
|---|---|---|---|
| Font **Old English Gothic Pixel** (title) | FontSpace / FontStruct | Yes (SIL OFL 1.1). | Keep the licence text (it is in `fonts/` and `licenses.txt`). It replaced Cross Stitch. |
| Font **Olde Tome** (headings, buttons) | LadyLiefy (itch.io) | **Probably yes.** The author's page combines a CC0 tag with a request for a voluntary payment for commercial use. | Confirm with the author and preferably pay any amount. |
| **Music** (`spoooky-theme-mm.mp3`) | MiniMax Music 2.6 (Replicate), instrumental | **Unconfirmed.** Checked on 24 Oct 2026: the "Music Creation Terms of Use" (minimax.io/audio/doc/terms-of-service-music.html) say nothing about ownership or commercial use of the output, do not mention the API, and require AI-generated content to be labelled. The general terms give MiniMax a broad licence to user content. The labelling requirement is met by the AI notice in the README; the app menu only links to that section. This does not settle the rights to the output. Secondary sources claim that the Open Platform terms leave the rights with the customer, but I did not find this in a primary document. | Read the MiniMax terms or ask for written confirmation. A safe alternative: the previous ACE-Step 1.5 track (MIT), which is in the git history (`audio/spoooky-theme.mp3`). |
| **Cards, backgrounds, card back, splash** | Flux 2 Pro via Replicate | **Probably yes.** Secondary sources and the Replicate terms (which pass the rights in the outputs to the user, including for commercial use) confirm it, but the BFL help page returned 404, so I have no quotation from the BFL terms. The model is meant for commercial use, but I did not find the wording on outputs in the sources. | Read the Black Forest Labs API terms and the Replicate terms. |
| Fonts **Geist Pixel**, **Jacquard 12** | Google Fonts | Yes (SIL Open Font License). | Keep the licence notice (it is in `licenses.txt`). |
| Pixel emoji | SerenityOS | Yes (BSD 2-Clause). | Keep the licence text (it is in `img/emoji/LICENSE` and `licenses.txt`). |
| Card list and traditional meanings | [NTielman/Tarot-Reader](https://github.com/NTielman/Tarot-Reader) and [ekelen/tarot-api](https://github.com/ekelen/tarot-api) (idea and dataset structure), A. E. Waite, *The Pictorial Key to the Tarot* (1910) | Yes. No code or text was copied from the two repositories (neither has a licence file); the meanings are our own wording based on Waite's public-domain text. | Keep the acknowledgement (it is in `licenses.txt` and the README). |
| Libraries: Tracery, seedrandom, ZzFX | GitHub | Yes (Apache-2.0, MIT, MIT). | Keep the licence notices (they are in `licenses.txt`). |
| App code, reading texts, scripts | Author | Own. | Decide on a repository licence (see below). |

## Details

**Cross Stitch.** The font was dropped (personal use only) and replaced by Old English Gothic Pixel under the OFL.

**Olde Tome.** The author allows using and modifying the font for free in personal work. For commercial use she asks for a voluntary payment ("pay what you can") while also tagging the asset CC0, which by itself does not require payment. The contradiction comes from her description, so it is safest to ask the author for written confirmation. Attribution is not required. The font file is not in the repository.

**Music.** The original track came from Suno's free plan (non-commercial use only), so it was replaced by a track from ACE-Step 1.5 (MIT, commercial use allowed) and then, at the author's request (a sound closer to Suno), by a track from MiniMax Music 2.6. Its commercial terms are less clear, so they need to be confirmed before wider promotion.

**Artwork (Flux 2 Pro).** The images were made from text descriptions, with no reference images of other people's work. Flux 2 Pro is available only through an API and is described as commercial, but in the sources I checked there is no quotation of the terms on outputs. Check the Black Forest Labs API terms first, then the Replicate terms. Also note that, according to the US Copyright Office, works generated entirely by AI without meaningful human creative input cannot be registered. The art direction (choice of variants, colours, layout, script processing) may count, but there is no guarantee.

**Tarot sources.** The idea of a tarot reader on a 78-card dataset, and the structure of the data (card ids such as `ar01`, major and minor arcana, suits), come from NTielman/Tarot-Reader and its data source ekelen/tarot-api. Neither has a licence file (checked on 26 Oct 2026), which under copyright law means all rights are reserved, so we copied none of their code, text or images: `data/cards.json` is our own wording and the card images are our own. The traditional meanings go back to A. E. Waite's *The Pictorial Key to the Tarot* (1910), which is in the public domain because Waite died in 1942. Giving credit is good practice even where it is not required.

**A repository without a licence.** A public GitHub repository without a `LICENSE` file means all rights stay with the author, and others may only view and fork it under GitHub's terms. If you want the code to be reusable, add a licence (for example MIT for the code, and reserve the rights to the graphics, texts and music). None was added, because that is the author's decision.

## Checklist before commercial publication

1. **Cross Stitch:** done (replaced by Old English Gothic Pixel, OFL).
2. **Music:** the MiniMax Music 2.6 track; confirm the commercial terms (or go back to ACE-Step, MIT).
3. **Artwork:** read the output terms in the Black Forest Labs API terms and in the Replicate terms, and record the result in this document.
4. **Olde Tome:** write to the author and pay any amount (or get the CC0 status confirmed in writing).
5. **Repository:** choose a licence or leave all rights reserved.

## Sources

- Suno, official help on song rights: https://help.suno.com/en/articles/2416769
- Suno, terms of service changes: https://about.suno.com/blog/suno-updates-tos
- Guide to rights in Suno outputs: https://terms.law/ai-output-rights/suno/
- Olde Tome (itch.io): https://ladyliefy.itch.io/olde-tome
- Cross Stitch (dafont): https://www.dafont.com/cross-stitch-2.font
- FLUX.2 pro on Replicate (model description): https://replicate.com/black-forest-labs/flux-2-pro
- NTielman/Tarot-Reader: https://github.com/NTielman/Tarot-Reader
- ekelen/tarot-api: https://github.com/ekelen/tarot-api
