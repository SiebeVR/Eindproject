# Eindproject API-Development
> Eindproject voor het vak API-Development
> gemaakt door Siebe Van Rompay R0804405

## Inhoud

* [Project Thema](#project-thema)
* [Methods](#Methods)
* [Database](#Database)
* [Authentication](#Authentication)
* [Hashing](#Hashing)
* [Screenshots](#Screenshots)
* [Links](#Links)


## Project Thema

- Het thema van dit project is wielrennen.
- Het wielrenseizoen is afgelopen dus nu zijn alle punten van de renners bekend.


## Methods

- GET /riders => Lijst van alle riders met info
- GET /leaderboard => Leaderboard van de renners (Hoogste punten eerst)
- GET /rider/{riderid} => Opvragen van specifieke rider door middel van zijn ID
- GET /ploegen => Lijst van alle ploegen
- GET /users => Lijst van alle users (Authenticatie vereist)
- POST /adduser/ => Maakt nieuwe gebruiker aan
- POST /token => Vraagt token aan voor user (Login vereist)
- POST /addrider/ => Maakt nieuwe rider aan (Authenticatie vereist)
- POST /addploeg/ => Maakt nieuwe ploeg aan (Authenticatie vereist)
- PUT /updaterider/{id} => Verandert een bestaande rider aan de hand van ID(Authenticatie vereist)
- DELETE /deleterider/{id} => Verwijdert een rider aan de hand van ID (Authenticatie vereist)

## Database

De database heeft 3 tabellen:
- Users
  - id
  - username
  - password
- Riders
  - id
  - naam
  - land
  - leeftijd
  - ploeg
  - punten
- Ploegen
  - naam
  - land



## Authentication

De authenticatie wordt gedaan met OAuth 2.0.
Wanneer een gebruiker zich wil authenticeren moet hij eerst een user account aanmaken en vervolgens een token aanvragen.
Alle POST/PUT/DELETE methods en ook de GET methods voor alle users en je eigen user vereisen authenticatie.

## Hashing

Als een user een account aanmaakt wordt zijn opgegeven wachtwoord gehasht in de database.

## Screenshots

# GET /riders
![image](https://user-images.githubusercontent.com/55507726/210878399-a38e7831-1c14-4f7f-b6c7-ed926329a06f.png)
# GET /leaderboard
![image](https://user-images.githubusercontent.com/55507726/210878338-11ef2576-aaee-4bbc-9c2d-9d7be974248d.png)
# GET /rider/{riderid}
![image](https://user-images.githubusercontent.com/55507726/210878441-f1fabce9-1372-4802-b9dd-958f5bdae42e.png)
# GET /ploegen
![image](https://user-images.githubusercontent.com/55507726/210878585-f58970d8-927d-4e35-adda-ad38f18e81c5.png)
# GET /users
![image](https://user-images.githubusercontent.com/55507726/210878754-aee79f76-62c3-48a2-a1f7-3e51b849d9ef.png)
# POST /adduser/
![image](https://user-images.githubusercontent.com/55507726/210875845-c1e2674f-0e91-4f3f-b817-9581941a15a7.png)
# POST /token
![image](https://user-images.githubusercontent.com/55507726/210875947-b00d5274-92bc-49d8-834f-f638b3be6348.png)
# POST /addrider/
![image](https://user-images.githubusercontent.com/55507726/210877558-9a4da7cf-d693-44b0-8223-53b53c900556.png)
# POST /addploeg/
![image](https://user-images.githubusercontent.com/55507726/210877290-ba2b5780-5177-469b-98e6-b210be4dc857.png)
# PUT /updaterider/{id}
![image](https://user-images.githubusercontent.com/55507726/210877815-ac587955-48ce-48ff-8453-55d28b1aa4a9.png)
# DELETE /deleterider/{id}
![image](https://user-images.githubusercontent.com/55507726/210878963-50d88639-635e-4d4d-a068-e0b3f1a1633a.png)
# Database
![image](https://user-images.githubusercontent.com/55507726/210879338-301d5519-404a-4223-a143-573a80a8192a.png)
![image](https://user-images.githubusercontent.com/55507726/210880318-5246a588-38bd-4a2d-8ae2-be561313e89d.png)
![image](https://user-images.githubusercontent.com/55507726/210880395-f851d477-8636-4f31-b133-630bb8bd8ec9.png)
![image](https://user-images.githubusercontent.com/55507726/210880426-1e5c5fc3-b7a8-4faa-a146-f55e578c831b.png)
# Authenticatie
![image](https://user-images.githubusercontent.com/55507726/210875586-9228916b-e316-4fa3-98ea-a0a26a1ef14b.png)
![image](https://user-images.githubusercontent.com/55507726/210876145-71c28de2-0aa0-4914-9072-b2e84aef51d8.png)
# Hashing
![image](https://user-images.githubusercontent.com/55507726/210875464-b9c6d3de-768d-49a3-9c36-174f97fd13ff.png)
# OpenAPI
![image](https://user-images.githubusercontent.com/55507726/210894064-461e72d9-f8b5-4ec4-a021-7ab4b8e11f3f.png)




## Links

- Link naar hosted API: https://main-service-siebevr.cloud.okteto.net/
- Link naar Front-end repository: https://github.com/SiebeVR/Eindproject_frontend
- Link naar hosted Front-end: https://siebevr.github.io/Eindproject_frontend/
- Link naar OpenAPI docs: https://main-service-siebevr.cloud.okteto.net/docs
