# Dodatkowe wzorce AI: tropy, struktura i kontrola kontekstu

Ta referencja jest kuratorskim dodatkiem do `patterns-en.md`, `patterns-pl.md` i
`polszczyzna-pl.md`. Została opracowana na podstawie katalogu
[tropes.md](https://tropes.fyi/tropes-md) oraz przewodnika Wikipedii
[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
Nie kopiuje tych materiałów w całości. Porządkuje wzorce, które są szczególnie
przydatne przy dłuższych tekstach, README, raportach i tekstach z formatowaniem.

## Jak z tego korzystać

To są heurystyki redakcyjne, nie detektor autorstwa. Jeden sygnał niczego nie
dowodzi, a człowiek może używać każdego z tych wzorców celowo. Szukaj klastrów:
powtarzalnego rytmu, meta-komentarzy, ogólników, sztucznej symetrii i braku
konkretu. Usuwaj tylko to, co osłabia tekst lub nie należy do głosu autora.

Przed zmianą zadaj trzy pytania:

1. Czy ten fragment przekazuje informację, czy tylko zapowiada, porządkuje albo
   podsumowuje to, co właśnie zostało powiedziane?
2. Czy forma wynika z gatunku i intencji autora, czy została dodana jako
   automatyczna dekoracja?
3. Czy po skróceniu lub przepisaniu zostają fakty, zastrzeżenia, źródła i
   właściwy poziom pewności?

## Tropy komunikacyjne i meta

- **Preambuła przed odpowiedzią.** Zamiast wejść w temat, tekst mówi, co za
  chwilę zrobi: „najpierw omówmy”, „poniżej przedstawiam”, „przyjrzyjmy się”.
  Skróć zapowiedź albo zacznij od pierwszego konkretu.
- **Wyciek procesu rozumowania.** W gotowym tekście zostają ślady pracy
  asystenta: plan, samokorekta, komentarz o analizowaniu lub deklaracja kolejnego
  kroku. Usuń je, chyba że użytkownik tworzy jawny dziennik procesu.
- **Komunikat usługowy.** „Mam nadzieję, że to pomoże”, „daj znać, jeśli...” i
  podobne zakończenia należą do rozmowy z użytkownikiem, nie do artykułu, maila
  ani raportu, chyba że autor świadomie używa takiego tonu.
- **Zastrzeżenie o wiedzy modelu.** Informacje o dacie odcięcia, braku dostępu
  albo „jako model językowy” są właściwe w odpowiedzi technicznej, ale zwykle
  nie powinny trafić do przepisywanego tekstu.
- **Fałszywa skromność.** Formuły typu „nie twierdzę, że mam rację, ale...” lub
  „to tylko moja opinia” mogą sztucznie osłabiać prostą tezę. Zachowaj realne
  zastrzeżenie, usuń samą asekurację.

## Tropy retoryczne

- **Sztuczna symetria.** Schemat „nie X, nie Y, tylko Z” jest skuteczny raz,
  ale powtarzany brzmi jak szablon. Przepisz go na normalne zdanie, jeśli
  kontrast nie jest istotny.
- **Kompulsywna trójka i anafora.** Trzy równoległe elementy albo kilka zdań
  zaczynających się tak samo nie zawsze są problemem. Zostaw je, gdy budują
  rytm; rozbij, gdy tylko udają kompletność.
- **Inflacja stawki.** Lokalna obserwacja staje się „punktem zwrotnym”, a
  pojedyncza zmiana „przełomem dla całej branży”. Przywróć skalę wynikającą z
  faktów.
- **Wymuszona metafora i slogan.** „To nie tylko..., lecz także...” albo
  efektowna puenta bez nowej informacji może być ozdobnikiem. Zostaw metaforę,
  jeśli jest częścią głosu autora i coś dopowiada.
- **Zapętlona konkluzja.** Wstęp, środek i zakończenie powtarzają tę samą tezę
  innymi słowami. Zachowaj najmocniejszą wersję, a pozostałe skróć.
- **Jednozdaniowa puenta na siłę.** Krótki, cytowalny slogan po rzeczowym
  akapicie często nie wnosi treści. Usuń go albo połącz z poprzednim zdaniem.
- **Dramatyczny zwrot.** Zapowiedzi w rodzaju „i tu jest sedno” mają sens w
  mowie, ale w raporcie zwykle można przejść od razu do sedna.

## Tropy leksykalne i składniowe

- **Wymyślona etykieta.** Tekst tworzy nazwę dla zwykłej obserwacji, np.
  „paradoks X” lub „efekt Y”, choć źródło takiej nazwy nie podaje. Nie twórz
  terminów dla efektu stylistycznego. Jeśli termin jest źródłowy, zachowaj go.
- **Synonimiczny slalom.** To samo pojęcie zmienia nazwę w każdym zdaniu tylko
  po to, by uniknąć powtórzenia. W tekście fachowym konsekwencja jest ważniejsza
  niż urozmaicenie.
- **Magiczne przysłówki.** Słowa typu „po cichu”, „subtelnie”, „głęboko” albo
  „znacząco” sugerują efekt bez pokazania, co faktycznie się wydarzyło. Zamień
  je na konkret albo usuń.
- **Unik prostych czasowników.** Konstrukcje „stanowi”, „pełni funkcję” i
  „służy jako” nie są automatycznie lepsze od „jest”, „ma” lub zwykłego
  czasownika. Przywróć prostą składnię, jeśli nie ma powodu do formalnego
  rejestru.
- **Ogólny autorytet.** „Eksperci twierdzą”, „badania pokazują” i „wiele osób
  uważa” wymagają konkretnego źródła albo ostrożniejszego sformułowania.
- **Ogólnik promocyjny.** „Wyjątkowy”, „innowacyjny”, „tętniący życiem” i
  podobne słowa powinny wynikać z danych lub zostać zastąpione opisem.

## Tropy strukturalne i formatowanie

- **Nagłówki jako dekoracja.** Nagłówki w stylu „Co? Dlaczego? Jak?” albo
  tytuły pisane Title Case mogą wyglądać jak szablon. Nie zmieniaj ich, jeśli
  narzuca je konwencja produktu, ale nie dodawaj ich automatycznie.
- **Pogrubiony początek każdego punktu.** Lista, w której każdy punkt ma
  pogrubioną etykietę i dwukropek, często rozdrabnia tekst. Zostaw listę, gdy
  poprawia skanowanie; usuń powtarzalne etykiety, gdy nie niosą informacji.
- **Nadmierna enumeracja.** Każdy akapit ma numer, podpunkty i podsumowanie,
  choć materiał nie wymaga procedury. Zachowaj tylko hierarchię potrzebną
  czytelnikowi.
- **Zduplikowana treść.** Wstęp streszcza całość, każdy nagłówek streszcza
  sekcję, a konkluzja streszcza ponownie. Zostaw jeden poziom streszczenia.
- **Poszarpane akapity.** Krótkie, podobnej długości akapity mogą być wygodne
  na ekranie, ale seria fragmentów po jednym zdaniu często zdradza automatyczny
  podział. Scal je, gdy należą do jednej myśli.
- **Osierocony nagłówek lub lista.** Nagłówek bez treści, sama lista pod
  nagłówkiem albo samotny blok cytatu wymaga scalenia lub usunięcia, nie
  kosmetycznego formatowania.
- **Dekoracyjne Unicode i uszkodzony Markdown.** Emoji, ozdobniki, nietypowe
  cudzysłowy, nierówne poziomy nagłówków i niedomknięte bloki kodu sprawdzaj
  jako całość. Pojedynczy znak nie jest dowodem problemu.

## Źródła, markup i wiarygodność

W tekście z bibliografią lub Markdownem kontroluj nie tylko styl. Sprawdź, czy
nie pojawiły się pozorne źródła, uszkodzone linki, błędne identyfikatory,
artefakty cytowań, nieużywane etykiety referencji albo komentarze techniczne.
Nie naprawiaj źródła przez zgadywanie. Zachowaj istniejący URL i oznacz brak
pewności użytkownikowi.

## Kalibracja z quizu

Strona [AI or not quiz](https://en.wikipedia.org/wiki/Wikipedia:AI_or_not_quiz)
jest inspiracją do testu ślepego, a nie testem prawdy o autorstwie. Jeśli tworzysz
własne przypadki:

1. mieszaj teksty ludzkie, AI i celowo nietypowe;
2. zapisuj nie tylko werdykt, ale też pewność i konkretny powód;
3. licz osobno fałszywe alarmy i przeoczenia;
4. po ujawnieniu odpowiedzi sprawdzaj, który sygnał zawiódł;
5. nie używaj wyniku jako podstawy do oskarżenia autora ani do usuwania
   charakterystycznego głosu.

## Przebieg dla długiego lub sformatowanego tekstu

1. Najpierw wykonaj zwykły przebieg z referencjami językowymi.
2. Potem uruchom tylko odpowiednie sekcje tej referencji: meta, retorykę,
   słownictwo albo strukturę.
3. Następnie zrób audyt faktów i źródeł.
4. Na końcu przeczytaj tekst bez porównywania z oryginałem i sprawdź, czy nie
   usunąłeś intencjonalnego rytmu, humoru, ostrożności albo formatowania gatunku.
