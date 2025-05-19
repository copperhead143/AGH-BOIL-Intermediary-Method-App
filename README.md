#  Product Backlog

## Epiki wraz z kryteriami akceptacji

### EPIK 1: Wprowadzenie działającego backendu:

- opracowanie modelu przechowywania danych w bazie => M (could have), WS

_Kryterium: Model danych zawiera wszystkie niezbędne encje i relacje wymagane przez logikę biznesową._
- połączenie modelu z bazą danych => S (could have), WS

_Kryterium: Aplikacja poprawnie łączy się z bazą i umożliwia podstawowe operacje._
- prasowanie danych dla aplikacji => L (could have), WS


  _Kryterium: Surowe dane wejściowe są przetwarzane do ustandaryzowanej formy wymaganej przez model._
- model wpisywania danych przez użytkownika => M (must have), SS

_Kryterium: Użytkownik może dodać dane przez interfejs._
- implementacja obliczania maksymalnych ilości zakupu u i-tego dostawcy i maksymalnych ilości do dostarczenia do j-tego odbiorcy => L (must have), SS

_Kryterium: System poprawnie oblicza ograniczenia na podstawie danych wejściowych._
- obliczenie kosztu zakupu od dostawcy i ceny sprzedaży dla odbiorcy => L (must have), SS

_Kryterium: Aplikacja zwraca prawidłowe wartości kosztów i przychodów zgodnie z formułami._
- pokazanie kolejnych kroków obliczeniowych programu => L (could have), WS

_Kryterium: Użytkownik widzi czytelnie opisany każdy etap obliczeń._
- obliczanie dochodów jednostkowych => S (must have), SS

_Kryterium: System prawidłowo oblicza różnicę między ceną sprzedaży a kosztem zakupu._

---
### EPIK 2: Stworzenie frontendu oraz połączenie go z backendem

- stworzenie części wizualnej programu => M (must have), ŁW

_Kryterium: Interfejs użytkownika zawiera wszystkie wymagane widoki i elementy._
- połączenie jej z backendem => S (must have), ŁW

_Kryterium: Dane przesyłane z i do backendu są poprawnie obsługiwane w interfejsie._
- usprawnienie interakcyjności oraz czytelności => S (should have), SS

_Kryterium: Użytkownik intuicyjnie porusza się po aplikacji i może łatwo odczytać dane._

- odpowiednie wyświetlanie macierzy wynikowej  => S (should have), ŁW

_Kryterium: Macierz wynikowa jest przedstawiona w czytelnej, tabelarycznej formie na froncie._

---
### POMYSŁY I USPRAWNIENIA:
- Zapisywanie i wczytywanie projektów
- Dodanie innych problemów niż 2x3

---
### HARMONOGRAM POSZCZEGÓLNYCH ZADAŃ:
**Sprint 1:** Wprowadzenie danych

**Sprint 2:** Obliczenia związane z zagadnieniem

**Sprint 3:** Upiększenie programu

---
### PODZIAŁ OBOWIĄZKÓW
**Szymon Sikora** - backend

**Wojciech Starzyk** - baza danych

**Łucja Wuls** - frontend




