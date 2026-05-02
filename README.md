# Rakvere valla sündivuse ja rände trendide analüüs lasteaia kohtade vajaduse hindamiseks

## Uurimisküsimus
Kuidas on muutunud Rakvere valla sündivus ja ränne ning mida see tähendab lasteaia kohtade vajaduse jaoks lähiaastatel?

## Projekti eesmärk
Projekti eesmärk on luua ETL-pipeline, mis loeb Statistikaameti API-st rahvastiku-, sündide-, surmade- ja rändeandmeid, puhastab ja teisendab need analüüsitavaks kujuks, salvestab tulemused PostgreSQL andmebaasi ning võimaldab tulemusi visualiseerida Apache Supersetis.

## Andmeallikad
Statistikaameti API tabelid:
- RV0240 – rahvastik soo, vanuse ja elukoha järgi
- RV112U – elussündinud soo ja haldusüksuse järgi
- RV49U – surnud soo ja haldusüksuse järgi
- RV172 – sündimuse vanuskordajad
- RVR02 – rände saldo haldusüksuse järgi
- RVR03 – rände saldo vanuserühma järgi

## Arhitektuur
Statistikaameti API → Python ETL → CSV väljundfailid → PostgreSQL → Apache Superset → visualiseeringud

## Projekti struktuur
```text
.
├── Lasteaiakohad.py              # Extract + Transform + CSV väljundid ja pildid
├── etl/
│   └── load_to_postgres.py       # Load: CSV failid PostgreSQL-i
├── docker/
│   └── superset/
│       └── Dockerfile            # Superset + PostgreSQL driver
├── docker-compose.yml            # PostgreSQL ja Superset
├── requirements.txt              # Python sõltuvused
└── README.md
```

## Käivitamine

### 1. Paigalda Python sõltuvused
```bash
pip install -r requirements.txt
```

### 2. Käivita PostgreSQL ja Superset
```bash
docker compose up -d
```

### 3. Genereeri ETL väljundfailid
```bash
python Lasteaiakohad.py
```

Skript loob `Outputs` kausta CSV-failid ja PNG-graafikud.

### 4. Laadi CSV-failid PostgreSQL-i
```bash
python etl/load_to_postgres.py
```

### 5. Ava Superset
Brauseris: http://localhost:8088

Kasutaja: `admin`  
Parool: `admin`

### 6. Lisa Supersetis PostgreSQL ühendus
Supersetis kasuta ühenduse stringi:
```text
postgresql://postgres:postgres@postgres:5432/lasteaiakohad
```

NB! Superseti sees on PostgreSQL host `postgres`, mitte `localhost`, sest mõlemad teenused töötavad Docker Compose võrgus. Kui ühendud oma arvutist otse PostgreSQL-i, kasuta porti `5433`.

## PostgreSQL tabelid
Laadimisskript loob järgmised tabelid:
- `population_forecast`
- `birth_forecast`
- `kinder_need`
- `summary`
- `yearly_kinder_compare`
- `population_compare`
- `migration_history`
- `birth_death_history`

## Soovituslikud Superseti visualiseeringud
- Sündide ja surmade ajalooline trend 2018–2024
- Rändesaldo 2015–2024
- Rahvaarvu prognoos 2026–2035 stsenaariumite kaupa
- Lasteaiakohtade vajadus 2026–2030 koos olemasoleva kohtade arvuga
- Kokkuvõttev tabel, kas olemasolevatest kohtadest piisab

## Piirangud
- Prognoos põhineb eeldustel ja ajaloolistel trendidel.
- Rände vanuseline jaotus on lihtsustatud.
- Ei eristata era- ja munitsipaallasteaedu.
- Lasteaiaealiste laste osalemismäärad põhinevad eeldustel.

## Kasutatud tehnoloogiad
Python, pandas, numpy, requests, matplotlib, SQLAlchemy, PostgreSQL, Docker Compose, Apache Superset.
