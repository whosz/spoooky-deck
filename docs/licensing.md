# Licencje i warunki użycia: Spoooky Deck

Stan na 24 października 2026. Ten dokument opisuje, na jakich warunkach można używać każdego elementu aplikacji, zwłaszcza przy użyciu komercyjnym. Aplikacja jest lead magnetem dla whosz.pl, więc przy publikacji na stronie firmowej warto traktować ją jako użycie komercyjne.

To nie jest porada prawna. Informacje o Suno, Olde Tome i Flux pochodzą ze stron producentów i źródeł wtórnych (lista na końcu). Warunki zmieniają się, więc przed publikacją sprawdź je jeszcze raz.

## Podsumowanie

| Element | Skąd | Użycie komercyjne | Co trzeba zrobić |
|---|---|---|---|
| Czcionka **Cross Stitch** (tytuł) | dafont, Levi Szekeres | **Nie bez licencji.** Darmowa tylko do projektów osobistych i organizacji non-profit. | Kupić licencję komercyjną (20 USD, bez opłat dodatkowych, na jedną osobę lub firmę) albo zmienić czcionkę tytułu. |
| Czcionka **Olde Tome** (nagłówki, przyciski) | LadyLiefy (itch.io) | **Prawdopodobnie tak.** Strona autorki łączy znacznik CC0 z prośbą o dobrowolną opłatę przy użyciu komercyjnym. | Potwierdzić z autorką i najlepiej zapłacić dowolną kwotę. |
| **Muzyka** (Candlelit Tarot) | Suno AI | **Zależy od planu.** Plan darmowy: tylko niekomercyjnie. Plany Pro i Premier: prawa komercyjne, także po anulowaniu. | Sprawdzić, na jakim planie powstał utwór. Jeśli na darmowym, trzeba wygenerować go ponownie na płatnym. |
| **Karty, tła, rewers, splash** | Flux 2 Pro przez Replicate | **Do potwierdzenia.** Model jest przeznaczony do zastosowań komercyjnych, ale nie znalazłem w źródłach tekstu warunków dla wyników. | Przeczytać warunki API Black Forest Labs i regulamin Replicate. |
| Czcionki **Geist Pixel**, **Jacquard 12** | Google Fonts | Tak (SIL Open Font License). | Zachować informację o licencji (jest w `licenses.txt`). |
| Pikselowe emoji | SerenityOS | Tak (BSD 2-Clause). | Zachować tekst licencji (jest w `img/emoji/LICENSE` i `licenses.txt`). |
| Biblioteki: Tracery, seedrandom, ZzFX | GitHub | Tak (Apache-2.0, MIT, MIT). | Zachować noty licencyjne (są w `licenses.txt`). |
| Kod aplikacji, teksty wróżb, skrypty | Autor | Własne. | Zdecydować o licencji repozytorium (patrz niżej). |

## Szczegóły

**Cross Stitch.** Plik `Terms.txt` z paczki mówi wprost: darmowe dla projektów osobistych i organizacji non-profit, licencja komercyjna kosztuje 20 USD, jest bezterminowa i obejmuje jedną osobę lub firmę (kontakt: https://www.loremipsum.ro/, levi@loremipsum.ro). Strona z aplikacją na whosz.pl promuje firmę, więc to użycie komercyjne. Plik fontu nie jest w publicznym repozytorium, a tytuł działa tylko na serwerze.

**Olde Tome.** Autorka pozwala używać i modyfikować font za darmo w pracach osobistych. Przy użyciu komercyjnym prosi o dobrowolną opłatę („pay what you can”), a jednocześnie oznacza zasób licencją CC0, która sama w sobie nie wymaga zapłaty. Sprzeczność wynika z jej opisu, więc bezpiecznie jest zapytać autorkę o potwierdzenie na piśmie. Atrybucja nie jest wymagana. Plik fontu nie jest w repozytorium.

**Muzyka (Suno).** Według oficjalnej pomocy Suno utwory z planu darmowego pozostają własnością Suno i można ich używać tylko niekomercyjnie. Użytkownik planu Pro lub Premier w chwili tworzenia utworu dostaje prawa komercyjne, które zostają po anulowaniu subskrypcji. Wykupienie planu później nie zmienia statusu utworów stworzonych wcześniej na darmowym planie. Suno zastrzega też, że nie gwarantuje, iż wynik będzie unikalny ani że powstanie prawo autorskie do wyniku. Utwór leży w repozytorium (`audio/candlelit-tarot.mp3`), więc przy niekomercyjnym statusie jego publiczna dostępność też jest ryzykiem.

**Grafiki (Flux 2 Pro).** Obrazy powstały z opisów słownych, bez obrazów referencyjnych cudzych prac. Model Flux 2 Pro jest dostępny wyłącznie przez API i opisywany jako komercyjny, ale w sprawdzonych źródłach nie znalazłem cytatu z warunków dotyczących wyników. Sprawdź w pierwszej kolejności warunki API Black Forest Labs, a potem regulamin Replicate. Należy też pamiętać, że według amerykańskiego urzędu praw autorskich dzieła wygenerowane w całości przez AI, bez istotnego wkładu twórczego człowieka, nie podlegają rejestracji. Wkład kierunku artystycznego (dobór wariantów, kolorów, układu, obróbka skryptami) może mieć znaczenie, ale nie jest to gwarancja.

**Repozytorium bez licencji.** Publiczne repozytorium na GitHubie bez pliku `LICENSE` oznacza, że wszystkie prawa pozostają przy autorze, a inni mogą je tylko oglądać i forkować w ramach regulaminu GitHuba. Jeśli chcesz, żeby kod można było wykorzystywać, dodaj licencję (np. MIT dla kodu, a dla grafik, tekstów i muzyki zastrzeż prawa). Nie dodawałem żadnej, bo to Twoja decyzja.

## Lista kroków przed publikacją komercyjną

1. **Cross Stitch:** kup licencję (20 USD) albo zamień tytuł na czcionkę OFL (Geist Pixel lub Jacquard 12). To jedyny punkt, w którym użycie komercyjne wprost łamie warunki.
2. **Muzyka:** sprawdź plan Suno z dnia generowania. Jeśli darmowy, wygeneruj utwór ponownie na płatnym planie albo wymień muzykę.
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
