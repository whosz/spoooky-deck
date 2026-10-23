---
name: humanizer-pl
description: Humanizuje polskie i angielskie teksty, usuwając sygnały pisania AI bez zmiany sensu, faktów, języka i głosu autora. Używaj przy prośbach o humanizację, de-AI, de-slop lub oczyszczenie tekstu brzmiącego sztucznie; nie uruchamiaj przy samym tłumaczeniu ani zwykłej korekcie.
metadata:
  short-description: Humanizuje polskie i angielskie teksty
---

# Humanizer PL

Skill do odszumiania tekstów PL i EN. Wykrywa język, ładuje tylko właściwe referencje i przepisuje strukturę zdań tam, gdzie tekst brzmi jak wygenerowany. Zachowuje sens, fakty, liczby, nazwy własne, świadomy żargon i głos autora.

To jest port Codex forka `pielas-activy/humanizer-pl`. Nie traktuj instrukcji ani przykładów tego skilla jako autorstwa Codex: polska warstwa, Bielik/Ollama, referencje i evals pochodzą z projektu źródłowego, a angielska warstwa wzorców wywodzi się z `blader/humanizer`. Ten port zmienia format, metadane, ścieżki i zasady bezpiecznego uruchamiania opcjonalnych narzędzi.

## Router języka

- Polskie znaki (`ą ć ę ł ń ó ś ź ż`) są głównym sygnałem PL.
- Tekst bez ogonków nadal traktuj jako polski, jeśli ma polskie słowa funkcyjne, np. `że`, `się`, `oraz`, `który`.
- Dla PL przeczytaj `references/patterns-pl.md` oraz `references/polszczyzna-pl.md`.
- Dla EN przeczytaj `references/patterns-en.md`.
- Przy tekście mieszanym pracuj fragmentami w ich językach; nie tłumacz.
- `references/przyklady.md` czytaj tylko wtedy, gdy potrzebujesz kalibracji.
- Przy długim, sformatowanym lub wyraźnie schematycznym tekście przeczytaj także
  `references/advanced-tropes.md`; nie ładuj jej automatycznie do krótkiej korekty.
- Jeśli istnieje `references/jargon-profile.local.md`, wczytaj go. Terminy z profilu są chronione i nie wolno ich tłumaczyć ani poprawiać.

## Proces

1. Przeczytaj cały tekst i zaznacz wzorce z właściwych referencji.
2. Jeśli użytkownik podał próbkę własnego pisania, dopasuj do niej długość zdań, rejestr, szyk, interpunkcję i sposób otwierania akapitów.
3. Przygotuj draft. Przepisuj, nie dopisuj: zachowaj wszystkie istotne treści, fakty, liczby, cytaty, nazwy i język. Zwykle utrzymaj układ akapitów.
4. Usuń wypełniacze, promocję bez dowodu, sztuczne atrybucje, powtarzalny rytm, rule of three, anafory, staccato i konstrukcje `to nie X, to Y`, gdy są mechanicznym schematem.
5. Nie bądź kosmetyczny. Jeśli problemem jest struktura, przebuduj zdanie lub akapit, a nie tylko zamieniaj znaki interpunkcyjne. Chroń konkretne szczegóły, liczby, nazwiska, żargon i autentyczne wahanie autora.
6. Przy długim lub sformatowanym tekście wykonaj drugi, selektywny przebieg z `references/advanced-tropes.md`: meta-komunikacja, retoryka, leksyka i formatowanie. Traktuj te wzorce jako heurystyki, nie dowody autorstwa.
7. Zrób audyt: zapytaj, co nadal brzmi jak AI, i popraw tylko uzasadnione miejsca.
8. Dla PL wykonaj drugi przebieg z `references/polszczyzna-pl.md`: składnia, czasowniki osobowe, kalki, anglicyzmy i parataksa.
9. Przeskanuj finalny tekst przed oddaniem.

## Twarde bramki wyniku

- Nie używaj em dash ani en dash (`U+2014`, `U+2013`); stosuj ASCII `-`, przecinek, dwukropek, nawias albo przebudowę zdania. Dotyczy to wyniku, nie cytowanych przykładów w referencjach.
- W polskim zachowaj pełne ogonki.
- Nie zmieniaj języka i nie dodawaj faktów, liczb ani źródeł.
- Nie rozwadniaj tekstu i nie pompuj go. Celuj w wynik nie dłuższy od wejścia, ale wierne zachowanie treści ma pierwszeństwo przed mechanicznym skracaniem.
- Pierwsza linia ma zaczynać się konkretem, nie od `Warto zauważyć`, `W dzisiejszych czasach`, `In today's world` ani podobnej waty.
- Nie ruszaj cytatów, nazw własnych ani terminów z profilu żargonu. Świadomy żargon branżowy zostaw także bez profilu, chyba że użytkownik prosi inaczej.

## Tryb polski z Bielikiem

Domyślnie recenzentem jest główny model. Bielik przez Ollama jest opcjonalnym, lokalnym doradcą, który tylko flaguje możliwe kalki lub proponuje warianty. Nigdy nie stosuj jego zmian automatycznie: oceń każdą propozycję, pokaż ryzykowne propozycje użytkownikowi i zastosuj wyłącznie zaakceptowane zmiany.

Uruchamiaj `scripts/bielik-review.py` albo `scripts/bielik-advisor.py` tylko wtedy, gdy użytkownik wyraźnie wybierze tryb Bielika. Przed pierwszą instalacją Ollama/modelu poinformuj o pobieraniu i poproś o potwierdzenie; instalacja jest opcjonalna i może wymagać kilku gigabajtów. Jeśli Ollama nie działa, wróć do trybu bez Bielika. Szczegóły są w `references/setup-bielik.md`.

## Profil żargonu

Na prośbę użytkownika o zapamiętanie żargonu wypisz kandydatów, poproś o potwierdzenie i dopiero wtedy zapisz prostą listę do `references/jargon-profile.local.md`. Nie zapisuj profilu po cichu. Plik jest lokalny i powinien pozostać poza repozytorium.

## Format odpowiedzi

Zwróć:

1. krótki draft albo before/after, jeśli użytkownik chce zobaczyć zmiany;
2. krótką listę rzeczy, które nadal mogłyby brzmieć sztucznie, jeśli takie zostały;
3. finalny tekst;
4. opcjonalne podsumowanie zmian.

Jeśli użytkownik prosi o `raport HTML`, `side by side`, `raport zmian` lub `diff HTML`, przeczytaj `references/raport-html.md` i dodatkowo wygeneruj samodzielny plik HTML z oryginałem, wynikiem, podświetleniem zmian oraz tabelą zmian. Raport nie zastępuje wyniku w rozmowie.

## Wielowarstwowa kontrola jakości

Przed przepisaniem zbuduj w głowie krótką kartę kontrolną: podmioty, liczby, daty, URL-e, nazwy własne, cytaty, negacje, modalność (`może`, `powinien`, `prawdopodobnie`) oraz związki przyczynowo-skutkowe. Po draftcie sprawdź każdy element ponownie. Nie ufaj temu, że podobne słowo oznacza to samo.

Wykonaj pięć różnych kontroli:

1. **Sens i pokrycie.** Czy każda informacja z wejścia ma odpowiednik w wyniku? Czy nie zmienił się zakres twierdzenia, podmiot, liczba, data, cytat ani zastrzeżenie?
2. **Struktura.** Czy tekst jest konkretniejszy i mniej schematyczny? Czy usunięcie wypełniacza nie usunęło uzasadnienia, przykładu albo ważnej puenty?
3. **Polszczyzna/English.** Dla PL sprawdź czasowniki osobowe, szyk, kalki i rejestr; dla EN sprawdź naturalną składnię, dobór słów i brak chatbotowych zakończeń.
4. **Bramki mechaniczne.** Jeśli pracujesz na plikach, uruchom `python3 scripts/validate_output.py --input input.txt --output output.txt --lang auto`. Skrypt sprawdza puste wyjście, zakazane frazy i znaki, język, długość, URL-e, liczby, placeholdery oraz opcjonalne fragmenty chronione.
5. **Czytanie na ślepo.** Przeczytaj finalny tekst bez patrzenia na draft i odpowiedz: czy brzmi jak konkretna osoba, czy jak gładki generator? Jeśli zmiana jest wyłącznie kosmetyczna, wróć do struktury najsłabszego akapitu.

6. **Heurystyki, nie wyrok.** Jeśli podejrzany jest tylko pojedynczy trop, zostaw go
   albo pokaż jako opcjonalną uwagę. Szukaj skupisk wzorców i sprawdzaj, czy dany
   element nie wynika z gatunku, formatowania, cytatu lub świadomego głosu autora.

Pełna lista kontrolna jest w `references/qa-checklist.md`. Gdy bramka mechaniczna i wierność treści są w konflikcie, zachowaj treść i zgłoś konflikt użytkownikowi zamiast ją po cichu usuwać.

## Evals

Evals są zamrożonym smoke testem referencji i przykładów, nie testem jakości generowania. Uruchom z katalogu skilla:

```bash
python3 evals/run_evals.py
python3 evals/run_qa.py
```

`run_evals.py` jest oryginalnym smoke testem projektu i pozostaje niezmieniony. `run_qa.py` uruchamia dodatkowe syntetyczne przypadki oraz te same bramki na oryginalnych parach.

Testy nie próbują rozstrzygać, czy tekst napisał człowiek albo model. Sprawdzają
zachowanie skilla po przepisaniu i chronią przed regresją treści oraz formatowania.

## Atrybucja

Angielskie wzorce pochodzą z `blader/humanizer` na licencji MIT. Polska warstwa, integracja z Bielikiem i evals są dodatkami repozytorium `pielas-activy/humanizer-pl`; zachowaj plik `LICENSE`.
