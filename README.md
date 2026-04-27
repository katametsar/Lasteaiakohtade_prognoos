# Projekti teema  
Rakvere valla sündivuse ja rände trendide analüüs lasteaia kohtade vajaduse hindamiseks

---

# Uurimisküsimus  
Kuidas on muutunud Rakvere valla sündivus ja ränne ning mida see tähendab lasteaia kohtade vajaduse jaoks lähiaastatel?

---

# Projekti eesmärk  
Projekti eesmärk on ehitada lihtne, kuid realistlik andmetöötluse pipeline, mis:
- kogub rahvastikuandmed
- puhastab ja transformeerib need
- salvestab andmebaasi
- visualiseerib tulemused interaktiivses tööriistas

---

# Andmeallikad  

- Statistikaamet (Statistics Estonia)
  - sündide arv
  - rahvaarv
  - ränne (sisse/välja)
- (valikuline) hinnangulised lasteaia kohtade andmed

---

# Arhitektuur  
Statistikaameti andmed -> Python (ETL) -> transformatsioonid -> PostgreSQL -> Superset (Docker) -> visualiseerimine


---

# ETL pipeline  

## 1. Extract  
Andmed loetakse Statistikaameti allikatest (CSV / API).

## 2. Transform  
Andmetega tehakse järgmised sammud:

- arvutatakse sündide trendid ajas  
- arvutatakse rändesaldo (sisse − välja)  
- hinnatakse lasteaiaealiste laste arv  

 **Oluline loogika:**
lasteaia_vajadus=sündide arv 3-6 aastat tagasi


## 3. Load  
Andmed laetakse PostgreSQL andmebaasi tabelitesse:

- `population`
- `births`
- `kinder`

---

# 🗄️ Andmemudel  

## Raw / lähteandmed
- population  
- births  

## Tuletatud andmed
- kinder (lasteaia vajaduse hinnang)

---

# 📈 Visualiseerimine (Superset)

Supersetis võimalik luua vaated:

- sündivus ajas (line chart)  
- ränne ajas (bar chart)  
- lasteaia kohtade vajadus ajas (line chart)  
- kombineeritud vaated  

---

# Kuidas projekti käivitada  

## 0. Eeldused  
- Python 3  
- Docker + Docker Compose  
---

## 1. Paigalda Python sõltuvused  
```bash
pip3 install -r requirements.txt
```
## 2. ETL andmete genereerimine  
```bash
python3 Lasteaiakohad.py
```
## 3. Andmete laadimine PostgreSQL-i
```bash
python3 etl/load_to_postgres.py
```
## 4. Käivita andmebaas ja superset
```bash
docker compose up -d
```
## 5. Ava superset 
http://localhost:8088

username: admin
password: admin

## 6.Andmebaasi ühendus (Superset)
Supersetis uue andmebaasi lisamisel kasuta:
**Connection URI:**
postgresql://postgres:postgres@postgres:5432/lasteaiakohad
Selgitus:
- `postgres` – kasutajanimi  
- `postgres` – parool  
- `postgres` – host (Docker service nimi!)  
- `5432` – port konteineri sees  
- `lasteaiakohad` – andmebaasi nimi  
NB! Ära kasuta siin `localhost`, sest Superset jookseb Dockeris.

---

# Piirangud  

- Lasteaia vajaduse hinnang on lihtsustatud (ei arvesta kõiki tegureid)  
- Ei erista era- ja munitsipaallasteaedu  
- Rände mõju võib avalduda ajas nihkega  
- Vanuserühmad on ligikaudsed  
- Prognoos põhineb ajaloolisel trendil, mitte masinõppel

# Kasutatud tehnoloogiad  

- **Python**
  - pandas  
  - numpy  
  - sqlalchemy  

- **Andmebaas**
  - PostgreSQL  

- **Visualiseerimine**
  - Apache Superset  

- **Orkestreerimine**
  - Docker  
  - Docker Compose  
