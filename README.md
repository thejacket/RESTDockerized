### Zadanie Semantive REST API - Dockerized

![Architektura](diagram1.jpg?raw=true "Architektura")

- 4 endpointy API: ��danie tekstu z zadanego URL, ��danie zdj��, pobranie zasob�w i sprawdzenie statusu zadania
- Zarz�dzanie workerami przez Celery - dowolna skalowalno��
- Broker redis
- Scraping stron z wykorzystaniem Selenium + headless Chrome-Webdriver oraz requests

Instalacja krok po kroku
-------------
1. Pobra� repozytorium
2. Zbudowa� kontener dockera przez docker-compose
`docker-compose build`
3. Uruchomi� przez
`docker-compose up`
W terminalu powinny wy�wietli� si� komunikaty brokera, Celery i flaskowej aplikacji.

Przyk�ad komunikacji z API
-------------
`curl -X 'POST' <docker-machine ip>:5000/textFromWebsite/<websiteUrl>`

`curl -X 'POST' <docker-machine ip>:5000/imagesFromWebsite/<websiteUrl>`

`curl -J -L <docker-machine ip>:5000/downloadResources/<websiteURL> -o <websiteURL>.zip`

`curl <docker-machine ip>:5000/status/<taskId>`


- Dwa pierwsze endpointy s�u�� do scrapowania tekstu i obraz�w z zadanego URL do lokalnego katalogu w kt�rym uruchomiona jest aplikacja
Oba zwracaj� przy przyj�ciu ��dania id zadania, co pozwala na �ledzenie jego statusu
- /downloadResources/ spakuje i wy�le zasoby w ZIP, je�li s� one na serwerze
- /status/ pozwala �ledzi� status wykonywanego zadania


Do wykonania (TODO)
-------------
0. !! Nie dzia�a pobieranie zasob�w !!
1. Doda� testy
2. Wyabstrahowa� metod� pobierania zasob�w z URL, by mo�na by�o zmieni� spos�b scrapowania i rozszerzy� jego funkcjonalno�� (np. zmieni� silnik na inny ni� Selenium czy doda� rotuj�ce proxy/user-Agenta)
3. Doda� mo�liwo�� konfiguracji limitera

Przyk�adowy komunikat po uruchomienie kontenera
-------------
![Docker-screen](1.jpg?raw=true "Docker-screen")
