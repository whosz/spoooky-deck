# BRIEF: Spooooky Deck

Mroczna pikselowa wyrocznia tarota dla firm. Wejście: imię (≤30 znaków), znak zodiaku (12), firma (≤60). Losowanie 1 z 78 kart, prosta lub odwrócona (~30%). Wróżba o firmie zawsze kończy się wnioskiem: potrzebny projektant. Na końcu link do https://whosz.pl/offer/ (UTM) i kolejne losowanie.

Zasady:
- Czyste pliki statyczne, ES modules, bez backendu i buildu. Ścieżki względne (działa w `whosz.pl/tarot/`).
- PL i EN od razu. Teksty w `data/*.{pl,en}.json`, nigdy w kodzie.
- Dane użytkownika tylko jako `textContent`, nic nie wychodzi na serwer ani do linku. Link ma tylko ziarno `?s=`.
- Styl: Dead Cells (granat, złoto, świece), animacje jak Balatro (sprężyste, błysk). Paleta w `STYLE.md`.
- Szanuj `prefers-reduced-motion`. Kontrast tekstu ≥ 4,5:1. Przyciski ≥ 44 px.
- Teksty użytkowe sprawdzają skille: `humanizer-pl` dla polskich, `humanizer` dla angielskich (`.claude/skills/`). Bielik/Ollama pomijamy.
- Muzyka: `audio/Candlelit Tarot.mp3`, start po pierwszym kliknięciu, przycisk wyciszenia.
