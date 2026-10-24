# Spoooky Deck

![Spoooky Deck: rewers karty, tytuł i hasło](img/og.png)

Mroczna wyrocznia tarota dla firm. Wpisujesz imię, znak zodiaku i firmę, wybierasz kartę z wachlarza 78 kart, a wróżba zawsze kończy się wnioskiem, że firmie przyda się projektant. Na końcu jest link do oferty [whosz.pl](https://whosz.pl/offer/).

Działa na żywo: https://whosz.pl/tarot/

**Status:** projekt zamknięty na tym etapie (24.10.2026). Aplikacja jest kompletna i wdrożona; opis procesu: [docs/case-study.md](docs/case-study.md).

## Co to jest

- Czyste pliki statyczne (HTML, CSS, ES modules), bez backendu i bez procesu budowania.
- PWA: instalacja na ekranie głównym, praca offline (service worker, sieć najpierw).
- Dwa języki od razu: polski i angielski.
- 78 kart (22 Wielkie i 56 Małych Arkanów) w pikselowym stylu retro 16 kolorów, siatka 64×96, skalowana o całkowitą liczbę pikseli urządzenia.
- Wróżby składa gramatyka [Tracery](https://github.com/galaxykate/tracery) z losowością [seedrandom](https://github.com/davidbau/seedrandom). Karta, pozycja (prosta lub odwrócona), znak zodiaku i usługa decydują o treści, a puenta zawsze wskazuje projektanta. Małe arkana dostają dodatkowe zdanie o zgodności żywiołu znaku z kolorem karty.
- Ekran wróżby ma trzy zakładki: **Wróżba**, **Karta** (znaczenie i słowa kluczowe) oraz **Klucz** (objaśnienie, jak arkana, znak, żywioł i pozycja wpływają na wróżbę).
- Menu (hamburger): język, dźwięk, instalacja aplikacji, informacje o twórcy i licencje.
- Wachlarz kart z tasowaniem, bezwładnością i wyborem palcem lub myszą, odkrycie karty z iskrami, złoty połysk, pochylanie za kursorem, żyroskopem i przeciąganiem.
- Dźwięk: muzyka w pętli (zatrzymywana, gdy aplikacja jest w tle, i zapisywana do pracy offline) oraz efekty generowane w przeglądarce ([ZzFX](https://github.com/KilledByAPixel/ZzFX)).
- Udostępnianie: link z ziarnem losowania (bez imienia i firmy) z jednym zdaniem zachęcającym i nazwą karty oraz obrazek z wróżbą do zapisania lub udostępnienia. Link ma podgląd w komunikatorach (Open Graph).
- Prywatność: imię i firma zostają na urządzeniu. Nic nie jest wysyłane na serwer ani zapisywane w linku.

## Struktura

```
index.html, manifest.webmanifest, sw.js (generowany), favicon.ico, .htaccess
css/      style, cards, theme, fonts
js/       app, deck, oracle, fx, audio, share (+ vendor: tracery, seedrandom, zzfx)
data/     cards.json, grammar.{pl,en}.json, zodiac.{pl,en}.json, ui.{pl,en}.json
img/      cards/ (78 PNG), ui/, emoji/, icons/, og.png
fonts/    woff2/ttf (OFL); Olde Tome tylko na serwerze (patrz niżej)
audio/    spoooky-theme-mm.mp3
schema/   schematy JSON kart, gramatyki i zodiaku
tools/    generatory, walidatory i skrypty (deploy, service worker, grafika)
```

## Uruchomienie lokalnie

```bash
python3 -m http.server 8123
# http://localhost:8123/
```

Podgląd konkretnej karty: `?card=ar13` (Wielkie Arkana `ar00`–`ar21`; małe `wa`, `cu`, `sw`, `pe` + `01`–`14`), odwrócona: `&rev=1`. Język: `?lang=en`.

## Testy i narzędzia

```bash
node tools/test_oracle.mjs         # wszystkie kombinacje karta x pozycja x znak x język
python3 tools/validate_cards.py    # schemat i zakazane znaki w cards.json
python3 tools/build_sw.py          # generuje sw.js (lista plików + wersja z hasha)
node tools/smoke.cjs [adres]       # test dymny: cały przepływ w PL i EN, telefon 390 i 320 px (wymaga Playwrighta)
```

Talia powstała w modelu graficznym (Replicate, Flux 2 Pro) i została przetworzona skryptami z `tools/ai/` (zmniejszenie do 64×96, paleta 16 kolorów). Surowe obrazy nie są w repozytorium.

## Wdrożenie

`tools/deploy.sh` wgrywa pliki na serwer przez SFTP. Dane dostępowe są w lokalnym pliku poza repozytorium. Serwer Apache, katalog `whosz.pl/tarot/`, ścieżki względne. `.htaccess` ustawia typy MIME i nagłówki cache.

## Autorzy i licencje

Autor: Mateusz Staniszewski, [whosz.pl](https://whosz.pl), 2026. Szczegóły licencji zależności, fontów i emoji: [licenses.txt](licenses.txt). Warunki użycia komercyjnego i lista kroków na później: [docs/licensing.md](docs/licensing.md). Licencje komercyjne (m.in. czcionki, plan Suno) świadomie odłożono do czasu, gdy projekt zyska zasięg.

- Muzyka `audio/spoooky-theme-mm.mp3` została wygenerowana modelem MiniMax Music 2.6 (Replicate). Warunki użycia komercyjnego wyników są mniej jednoznaczne niż w ACE-Step (MIT), patrz docs/licensing.md. Skrypty: `tools/ai/music2.py` (MiniMax), `tools/ai/music.py` (ACE-Step).
- Czcionka tytułu: Old English Gothic Pixel (OFL, dołączona w `fonts/`). Czcionka Olde Tome (nagłówki) nie jest dołączona do repozytorium, bez niej nagłówki używają fontu zastępczego.
- Pikselowe emoji: SerenityOS (BSD-2). Teksty wróżb sprawdzano skillami humanizer (`.claude/skills/`).
