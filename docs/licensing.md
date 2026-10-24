# Licencje i warunki użycia: Spoooky Deck

Stan na 24 października 2026. Ten dokument opisuje, na jakich warunkach można używać każdego elementu aplikacji, zwłaszcza przy użyciu komercyjnym. Aplikacja jest lead magnetem dla whosz.pl, więc przy publikacji na stronie firmowej warto traktować ją jako użycie komercyjne.

To nie jest porada prawna. Informacje o Suno, Olde Tome i Flux pochodzą ze stron producentów i źródeł wtórnych (lista na końcu). Warunki zmieniają się, więc przed publikacją sprawdź je jeszcze raz.

## Podsumowanie

| Element | Skąd | Użycie komercyjne | Co trzeba zrobić |
|---|---|---|---|
| Czcionka **Old English Gothic Pixel** (tytuł) | FontSpace / FontStruct | Tak (SIL OFL 1.1). | Zachować tekst licencji (jest w `fonts/` i `licenses.txt`). Czcionka zastąpiła Cross Stitch. |
| Czcionka **Olde Tome** (nagłówki, przyciski) | LadyLiefy (itch.io) | **Prawdopodobnie tak.** Strona autorki łączy znacznik CC0 z prośbą o dobrowolną opłatę przy użyciu komercyjnym. | Potwierdzić z autorką i najlepiej zapłacić dowolną kwotę. |
| **Muzyka** (`spoooky-theme-mm.mp3`) | MiniMax Music 2.6 (Replicate), wersja instrumentalna | **Niepotwierdzone.** Sprawdzone 24.10.2026: „Music Creation Terms of Use” (minimax.io/audio/doc/terms-of-service-music.html) nie mówią nic o własności ani użyciu komercyjnym wyników, nie wspominają o API i wymagają oznaczania treści jako wygenerowanych przez AI. Ogólny regulamin daje MiniMax szeroką licencję na treści użytkownika. Źródła wtórne twierdzą, że warunki Open Platform zostawiają prawa klientowi, ale nie znalazłem tego w dokumencie pierwotnym. | Przeczytać regulamin MiniMax lub poprosić o potwierdzenie na piśmie. Bezpieczna alternatywa: poprzedni utwór ACE-Step 1.5 (MIT), jest w historii git (`audio/spoooky-theme.mp3`). |
| **Karty, tła, rewers, splash** | Flux 2 Pro przez Replicate | **Prawdopodobnie tak.** Źródła wtórne i regulamin Replicate (przekazuje użytkownikowi prawa do wyników, także do użycia komercyjnego) to potwierdzają, ale strona pomocy BFL zwróciła 404, więc nie mam cytatu z warunków BFL. Model jest przeznaczony do zastosowań komercyjnych, ale nie znalazłem w źródłach tekstu warunków dla wyników. | Przeczytać warunki API Black Forest Labs i regulamin Replicate. |
| Czcionki **Geist Pixel**, **Jacquard 12** | Google Fonts | Tak (SIL Open Font License). | Zachować informację o licencji (jest w `licenses.txt`). |
| Pikselowe emoji | SerenityOS | Tak (BSD 2-Clause). | Zachować tekst licencji (jest w `img/emoji/LICENSE` i `licenses.txt`). |
| Biblioteki: Tracery, seedrandom, ZzFX | GitHub | Tak (Apache-2.0, MIT, MIT). | Zachować noty licencyjne (są w `licenses.txt`). |
| Kod aplikacji, teksty wróżb, skrypty | Autor | Własne. | Zdecydować o licencji repozytorium (patrz niżej). |

## Szczegóły

**Cross Stitch.** Czcionka została wycofana (tylko użytek osobisty), zastąpiona Old English Gothic Pixel na licencji OFL.

**Olde Tome.** Autorka pozwala używać i modyfikować font za darmo w pracach osobistych. Przy użyciu komercyjnym prosi o dobrowolną opłatę („pay what you can”), a jednocześnie oznacza zasób licencją CC0, która sama w sobie nie wymaga zapłaty. Sprzeczność wynika z jej opisu, więc bezpiecznie jest zapytać autorkę o potwierdzenie na piśmie. Atrybucja nie jest wymagana. Plik fontu nie jest w repozytorium.

**Muzyka.** Pierwotny utwór pochodził z darmowego planu Suno (tylko użycie niekomercyjne), więc został zastąpiony utworem z ACE-Step 1.5 (MIT, komercyjne użycie dopuszczone), a następnie, na prośbę autora (bliższe brzmienie do Suno), utworem z MiniMax Music 2.6. Jego warunki komercyjne są mniej jednoznaczne, więc przed szerszą promocją trzeba je potwierdzić.

**Grafiki (Flux 2 Pro).** Obrazy powstały z opisów słownych, bez obrazów referencyjnych cudzych prac. Model Flux 2 Pro jest dostępny wyłącznie przez API i opisywany jako komercyjny, ale w sprawdzonych źródłach nie znalazłem cytatu z warunków dotyczących wyników. Sprawdź w pierwszej kolejności warunki API Black Forest Labs, a potem regulamin Replicate. Należy też pamiętać, że według amerykańskiego urzędu praw autorskich dzieła wygenerowane w całości przez AI, bez istotnego wkładu twórczego człowieka, nie podlegają rejestracji. Wkład kierunku artystycznego (dobór wariantów, kolorów, układu, obróbka skryptami) może mieć znaczenie, ale nie jest to gwarancja.

**Repozytorium bez licencji.** Publiczne repozytorium na GitHubie bez pliku `LICENSE` oznacza, że wszystkie prawa pozostają przy autorze, a inni mogą je tylko oglądać i forkować w ramach regulaminu GitHuba. Jeśli chcesz, żeby kod można było wykorzystywać, dodaj licencję (np. MIT dla kodu, a dla grafik, tekstów i muzyki zastrzeż prawa). Nie dodawałem żadnej, bo to Twoja decyzja.

## Lista kroków przed publikacją komercyjną

1. **Cross Stitch:** zrobione (zamieniona na Old English Gothic Pixel, OFL).
2. **Muzyka:** utwór MiniMax Music 2.6, potwierdzić warunki komercyjne (albo wrócić do ACE-Step, MIT).
3. **Grafiki:** przeczytaj warunki wyników w API Black Forest Labs i w regulaminie Replicate, zapisz wynik w tym dokumencie.
4. **Olde Tome:** napisz do autorki i zapłać dowolną kwotę (lub potwierdź CC0 na piśmie).
5. **Repozytorium:** wybierz licencję lub zostaw wszystkie prawa zastrzeżone.

## Źródła

- Suno, oficjalna pomoc o prawach do utworów: https://help.suno.com/en/articles/2416769
- Suno, zmiany regulaminu: https://about.suno.com/blog/suno-updates-tos
- Przewodnik o prawach do wyników Suno: https://terms.law/ai-output-rights/suno/
- Olde Tome (itch.io): https://ladyliefy.itch.io/olde-tome
- Cross Stitch (dafont): https://www.dafont.com/cross-stitch-2.font
- FLUX.2 pro w Replicate (opis modelu): https://replicate.com/black-forest-labs/flux-2-pro
