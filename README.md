[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/jsTzsySB)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=15150395)

Aplikacja Bankowa

Aplikacja służy do tworzenia kont bankowych, zarządzania nimi. Funkcje:
- Rejestracja i logowanie się użytkowników,
- Tworzenie kont bankowych (wybór banku w którym ma być utworzone konto, tytuł konta i opis, automatyczne generowanie numeu konta)
- Wpłaty oraz wypłaty z wybranych przez użytkownika kont, wyświetlanie historii wpłat i wypłat
- Przelewy między kontami
- Historia przelewów wychodzących i przychodzących

Aplikacja obsługuje błedy takie jak 404 i 403

Zaimplementowaliśmy mechanizm przelewów, gdzie przelewy między kontami w tym samym banku przechodzą natychmiastowo, jednak jeśli przelew wysyłany jest między kontami z różnyc banków dzieje się to w sesjach - raz na 15 minut w godzinach 10-23. Przy wysłaniu przelewu pieniądze są od razu 'zamrażane' na koncie wysyłającego i czekają na przelew, gdy przychodzi sesja przelewów pieniądze są wysyłane i trafiają na konto, do którego ten przelew był wysłany. Jest to zrealizowane dzięki bibliotece apscheduler.

Aplikacja została zrealizowana w języku python oraz frontend w HTML i CSS.

Korzystanie z aplikacji:
Aby kożystać  z aplikacji trzeba utworzyć tam konto, przy starcie zostaje automatycznie utworzone konto:
email: user@example.com
hasło: userpassword
Tworzone są 3 banki w których można stworzyć swój rachunek bankowy (Bank A, Bank B i Bank C)

Wszystkie transakcje są rejestrowane w bazie danych i mają swoje uuid.
