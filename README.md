### Zadanie Semantive REST API - Dockerized

![Architektura](diagram1.jpg?raw=true "Architektura")

- 4 endpointy API: ¿¹danie tekstu z zadanego URL, ¿¹danie zdjêæ, pobranie zasobów i sprawdzenie statusu zadania
- Zarz¹dzanie workerami przez Celery - dowolna skalowalnoœæ
- Broker redis
- Scraping stron z wykorzystaniem Selenium + headless Chrome-Webdriver oraz requests

Instalacja krok po kroku
-------------
1. Pobraæ repozytorium
2. Zbudowaæ kontener dockera przez docker-compose
`docker-compose build`
3. Uruchomiæ przez
`docker-compose up`
W terminalu powinny wyœwietliæ siê komunikaty brokera, Celery i flaskowej aplikacji.

Przyk³ad komunikacji z API
-------------
`curl -X 'POST' <docker-machine ip>:5000/textFromWebsite/<websiteUrl>`

`curl -X 'POST' <docker-machine ip>:5000/imagesFromWebsite/<websiteUrl>`

`curl -J -L <docker-machine ip>:5000/downloadResources/<websiteURL> -o <websiteURL>.zip`

`curl <docker-machine ip>:5000/status/<taskId>`


- Dwa pierwsze endpointy s³u¿¹ do scrapowania tekstu i obrazów z zadanego URL do lokalnego katalogu w którym uruchomiona jest aplikacja
Oba zwracaj¹ przy przyjêciu ¿¹dania id zadania, co pozwala na œledzenie jego statusu
- /downloadResources/ spakuje i wyœle zasoby w ZIP, jeœli s¹ one na serwerze
- /status/ pozwala œledziæ status wykonywanego zadania


Do wykonania (TODO)
-------------
0. !! Nie dzia³a pobieranie zasobów !!
1. Dodaæ testy
2. Wyabstrahowaæ metodê pobierania zasobów z URL, by mo¿na by³o zmieniæ sposób scrapowania i rozszerzyæ jego funkcjonalnoœæ (np. zmieniæ silnik na inny ni¿ Selenium czy dodaæ rotuj¹ce proxy/user-Agenta)
3. Dodaæ mo¿liwoœæ konfiguracji limitera

Przyk³adowy komunikat po uruchomienie kontenera
-------------
![Docker-screen](1.jpg?raw=true "Docker-screen")
