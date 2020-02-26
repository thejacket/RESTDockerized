### Zadanie Semantive REST API - Dockerized

![Architektura](diagram1.jpg?raw=true "Architektura")

- 4 endpointy API: żądanie tekstu z zadanego URL, żądanie zdjęć, pobranie zasobów i sprawdzenie statusu zadania
- Zarządzanie workerami przez Celery - dowolna skalowalność
- Broker redis
- Scraping stron z wykorzystaniem Selenium + headless Chrome-Webdriver oraz requests

Instalacja krok po kroku
-------------
1. Pobrać repozytorium
2. Zbudować kontener dockera przez docker-compose
`docker-compose build`
3. Uruchomić kontener przez
`docker-compose up`
W terminalu powinny wyświetlić się komunikaty brokera, Celery, monitora Celery-flower i flaskowej aplikacji.

Przykład komunikacji z API
-------------
`curl -X 'POST' <docker-machine ip>:5000/textFromWebsite/<websiteUrl>`

`curl -X 'POST' <docker-machine ip>:5000/imagesFromWebsite/<websiteUrl>`

`curl -J -L <docker-machine ip>:5000/downloadResources/<websiteURL> -o <websiteURL>.zip`

`curl <docker-machine ip>:5000/status/<taskId>`


- Dwa pierwsze endpointy służą do scrapowania tekstu i obrazów z zadanego URL do lokalnego katalogu w którym uruchomiona jest aplikacja
Oba zwracają przy przyjęciu żądania id zadania, co pozwala na śledzenie jego statusu
- /downloadResources/ spakuje i wyśle zasoby w ZIP, jeśli są one na serwerze
- /status/ pozwala śledzić status wykonywanego zadania


Do wykonania (TODO)
-------------
0. !! Nie działa pobieranie zasobów !!
1. Dodać testy
2. Wyabstrahować metodę pobierania zasobów z URL, by można było zmienić sposób scrapowania i rozszerzyć jego funkcjonalność (np. zmienić silnik na inny niż Selenium czy dodać rotujące proxy/user-Agenta)
3. Dodać możliwość konfiguracji limitera

Przykładowy komunikat po uruchomienie kontenera
-------------
![Docker-screen](1.jpg?raw=true "Docker-screen")
