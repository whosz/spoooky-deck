# Spoooky Deck: pikselowa wyrocznia tarota dla firm

Case study projektu zrealizowanego w dwa dni (23–24 października 2026) przez Claude (Anthropic) pod kierunkiem Mateusza Staniszewskiego (whosz.pl). Mateusz prowadził kierunek artystyczny i oceniał każdy etap, Claude pisał kod, treści i generował grafiki.

Działa na żywo: https://whosz.pl/tarot/ · Kod: https://github.com/whosz/spoooky-deck

## W skrócie

Użytkownik wpisuje imię, znak zodiaku i nazwę firmy, wybiera kartę z wachlarza 78 kart, a wróżba o przyszłości jego firmy zawsze kończy się wnioskiem, że firmie przyda się projektant. Na końcu jest link do oferty whosz.pl. To zabawny lead magnet dla właścicieli małych firm i startupów, czyli odbiorców oferty whosz.pl.

Efekt to aplikacja PWA (instalacja na telefonie, praca offline), po polsku i angielsku, napisana bez frameworka i bez procesu budowania: czyste pliki HTML, CSS i JavaScript wgrywane na zwykły serwer Apache.

## Cel i ograniczenia

- **Cel:** pamiętny, udostępnialny „haczyk”, który prowadzi do oferty. Ton: tajemniczy i lekko złowieszczy jak w grze, ale życzliwy na końcu.
- **Ograniczenia, które sam sobie narzuciliśmy:** statyczne pliki bez backendu, żadne dane osobowe nie opuszczają telefonu (link do udostępnienia zawiera tylko ziarno losowania, bez imienia i firmy), wszystko w jednym, spójnym stylu pikselowym.

## Jak powstało

| Etap | Co zrobiliśmy |
|---|---|
| Kontrakty | `BRIEF.md`, schematy JSON dla kart, gramatyki wróżb i znaków zodiaku, opis modułów. Dzięki nim zadania można było zlecać równolegle. |
| Silnik wróżb | Gramatyka Tracery z losowością zależną od ziarna (seedrandom). Karta, pozycja (prosta lub odwrócona), znak i usługa decydują o tekście. Test przechodzi 3744 kombinacji (78 kart × 2 pozycje × 12 znaków × 2 języki). |
| Treść | 78 kart po polsku i angielsku, 312 zdań znaczeń, 48 omenów znaków. Pisały je agenty (Haiku, potem Sonnet) według schematu, a skrypt walidował każdą partię. Redakcja przez skille humanizer. |
| Interfejs | Układ mobile first, na komputerze okno wielkości telefonu w ramie jak rama obrazu. Style: pikselowe ramki 9-slice, fonty, tła scen. |
| Talia | Najpierw własne ilustracje z kodu, potem 78 kart z modelu graficznego (Flux 2 Pro), sprowadzone skryptem do siatki 64×96 i 16 kolorów. |
| Animacje i dźwięk | Tasowanie, rozdanie, wachlarz z bezwładnością, iskry, połysk, pochylanie kursorem, żyroskopem i przeciąganiem, efekty ZzFX, muzyka z Suno AI. |
| PWA i wdrożenie | Manifest, service worker, ikony, `.htaccess`, obrazek wróżby do zapisania, grafika do udostępniania linku. Testy na produkcji po każdym etapie. |

## Najważniejsze decyzje

1. **Całkowita skala pikseli.** Piksele wyglądały nierówno, bo grafiki skalowałem o ułamki (np. 1,54×). Przeliczam więc rozmiary kart, teł i ramek na całkowitą liczbę pikseli urządzenia (na telefonie o dwukrotnym zagęszczeniu karta 64×96 wyświetla się dokładnie 10 pikseli urządzenia na piksel grafiki) i sprawdzam to pomiarem. Obrót karty rozmywa piksele, więc w spoczynku karta się nie obraca, a efekt 3D włącza się tylko podczas ruchu.
2. **Opis stylu słowami, nie obrazami.** Przy wyborze stylu dostaliśmy przykłady cudzych, płatnych talii. Cofnąłem generowanie z podaniem ich jako obrazu wzorcowego i zamiast tego opisałem styl słowami (paleta, kontury, gradienty, oświetlenie). Dzięki temu karty są własne.
3. **Ochrona prywatności z założenia.** Imię i firma trafiają na stronę jako zwykły tekst, a znaki sterujące gramatyki są z nich wycinane. Nic nie jest wysyłane na serwer.
4. **Serwer jako źródło prawdy, pamięć jako zapas.** Service worker najpierw pobiera świeże pliki, a z pamięci korzysta tylko offline. Wcześniejsza wersja z odwrotną kolejnością trzymała starą wersję aplikacji u użytkownika mimo wgranej nowej.
5. **Automatyzacja i testy.** Walidatory kart i gramatyki, test wszystkich kombinacji wróżb, skrypt generujący service workera, skrypty obróbki grafiki. Każdy wynik agentów był sprawdzany przez skrypt, zanim trafił do projektu.

## Problemy i jak je rozwiązaliśmy

- **Muzyka i autoodtwarzanie.** Przeglądarki blokują dźwięk bez dotknięcia ekranu, a Safari wymaga startu w momencie kliknięcia. Muzyka startuje więc przy pierwszym geście i ponawia próbę, a na ekranie startowym jest podpowiedź. Przy wyjściu z aplikacji muzyka się zatrzymuje, a po powrocie wraca.
- **„Żółte paski” w wachlarzu.** Przyczyną były obcinane cienie kart i dolne krawędzie dalekich kart, a nie jeden błąd. Ukryłem dalekie karty, wyłączyłem cienie na czas tasowania i zamieniłem poświatę na gradient.
- **Przyciski przesuwające się pod palcem.** Podpowiedź o muzyce znikała z układu po pierwszym dotknięciu i przesuwała przycisk, więc pierwsze dotknięcie nie trafiało. Znalazł to test dotykowy na emulowanym telefonie.
- **Tekst a gramatyka polska.** Imion i nazw firm nie da się bezpiecznie odmieniać, więc szablony używają ich w mianowniku i w cudzysłowie, a zdania o żywiołach też wymagały formy bez odmiany.

## Praca z AI

- **Podział ról:** główny model (Sonnet 5.5) prowadził projekt i kod, a pomocnicze agenty pisały treści (Haiku) i rysowały karty z kodu (Sonnet). Każdy agent dostawał krótki kontrakt i swój kawałek pracy, a jego wynik sprawdzał skrypt.
- **Generowanie grafik:** Flux 2 Pro przez API Replicate, sprowadzony skryptem do 16 kolorów. Wybór wariantów, kolorów i układu kierował Mateusz na zrzutach i próbkach. Łączny koszt generowania to kilka dolarów.
- **Moja rola w iteracjach:** kilkadziesiąt krótkich uwag Mateusza o układzie, rozmiarach i wyglądzie (np. „tło o 15% ciemniejsze”, „font o 2 px mniejszy”) wprowadzałem, mierzyłem w przeglądarce i wgrywałem na produkcję. Dokładne uwagi dawały szybkie, małe pętle.
- **Co poszło źle:** pierwsze ilustracje z kodu wyglądały dziecinnie („jak zrobiło je dziecko”), a pierwsze tła przeszkadzały w czytaniu tytułu. Zmiana kierunku na modele graficzne i prostszy, ciemny układ rozwiązała oba problemy.

## Wyniki

- 78 kart, 2 języki, 125 commitów w 2 dni.
- Około 730 linii własnego JavaScriptu (bez bibliotek) i 370 linii CSS, czyli aplikacja bez frameworka.
- Talia waży 316 KB, całość grafik i danych około 1 MB (bez muzyki 4,6 MB), 166 plików w pamięci podręcznej do pracy offline.
- Kilkanaście skryptów w `tools/` (walidacja, testy, test dymny, generowanie grafik, wdrożenie).

## Ograniczenia i dalsze kroki

- Aplikację testowałem w przeglądarce headless (na symulowanych telefonach, także najwęższym, 320 px) skryptem dymnym, który przechodzi cały przepływ w obu językach i sprawdza błędy, odpowiedzi serwera, formularz, zakładki, menu i obrazek wróżby (104 sprawdzenia). Na prawdziwym telefonie przepływ, instalację i udostępnianie potwierdził Mateusz.
- Muzyka wygenerowana w Suno oraz czcionki Cross Stitch i Olde Tome mają warunki użycia, które trzeba sprawdzić przy publikacji komercyjnej.
- Pomysły na później: żywioł jako osobny wątek wróżby (zrobione w prostej formie), historia wróżb na urządzeniu, audyt dostępności.
