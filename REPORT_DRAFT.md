# Projekti raport
## Projekti eesmärk

Projekti eesmärk oli luua korratav andmetöötluse ja visualiseerimise töövoog, mis võimaldab hinnata Rakvere valla sündivuse, rände ja rahvastikumuutuste võimalikku mõju lasteaiakohtade vajadusele lähiaastatel. Projekti keskmes oli tervikliku ETL-pipeline loomine, mis loeb andmed automaatselt Statistikaameti API-st, töötleb need analüüsitavaks kujuks, salvestab PostgreSQL andmebaasi ning võimaldab tulemusi visualiseerida Apache Supersetis. Projekti uurimisküsimus keskendub sellele, kuidas sündivuse ja rände muutused võivad mõjutada lasteaiakohtade vajadust tulevikus.

---

## Andmeallikas

Andmeallikana kasutati Statistikaameti API-t. Kasutatud tabelid sisaldasid rahvastikuandmeid soo, vanuse ja elukoha järgi, sündide ja surmade arvu, sündimuse vanuskordajaid ning rändesaldot. API kasutamine võimaldas luua korratava töövoo, kus sama pipeline’i saab uuemate andmete avaldamisel uuesti käivitada ilma käsitsi andmeid kogumata.

---

## ETL protsess

ETL-protsess jagunes extract-, transform- ja load-etappideks. Töövoog oli üles ehitatud nii, et andmete allalaadimine, teisendamine ja andmebaasi laadimine olid eraldi sammudena kontrollitavad.

### Extract

Extract-etapis tehti Pythoni abil päringud Statistikaameti API-sse ning vajalikud andmed (rahvastik, sünnid, surmad, sündimuse vanuskordaja ja rändesaldo) laeti töötluskeskkonda. Päringud piirati Rakvere valla andmetega ning API vastused teisendati pandas DataFrame objektideks. Edasiseks töötluseks kasutati ka metaandmeid, mis aitasid leida õiged muutujate ja väärtuste koodid.

### Transform

Transform-etapis puhastati Pythoni ETL-skriptis API-st saadud tabelid, korrastati veerunimed ning viidi erineva struktuuriga andmed ühtsesse aastate ja vanuserühmade põhisesse formaati. Seejärel ühendati eri andmetabelid ning arvutati aegread, rändesaldo, loomulik iive ja rahvastikuprognoos. Väljundina salvestati CSV-tabelid ja graafikud kausta `Outputs/`.

Prognoosis kasutati erinevaid sündivuse ja rände stsenaariume, vältimaks tulemuste sõltumist ühest eeldusest. Rahvastikuprognoosis arvestati vanuserühmade liikumist järgmisesse aastasse, sündide ja surmade mõju ning võimalikku rändesaldot.

Lasteaiakohtade vajaduse prognoosimiseks hinnati 1–6-aastaste laste arvu ja rakendati vanusepõhiseid lasteaias osalemise määrasid. Selle põhjal arvutati, kas olemasolevatest lasteaiakohtadest piisab või võib tulevikus tekkida vajadus kohtade arvu muuta. Transform-etapi lõpus salvestati prognoosid, koondtabelid ja visualiseerimiseks vajalikud andmed CSV-failidena.

### Load

Load-etapis laaditi genereeritud CSV-failid PostgreSQL andmebaasi skriptiga `load_to_postgres.py`, mis luges väljundfailid, puhastas vajadusel veerunimed, lõi andmebaasitabelid ja kirjutas andmed PostgreSQL-i. Iga CSV-fail vastas kindlale andmebaasitabelile. Andmete laadimisel kasutati SQLAlchemy teeki ja pandas `to_sql()` funktsiooni.

Projektis loodud ETL-pipeline automatiseerib andmetöötluse Statistikaameti API-st andmete lugemisest kuni PostgreSQL andmebaasini. PostgreSQL toimib keskse andmelaona, mille andmeid kasutatakse hiljem Apache Superseti visualiseeringutes.

---

## Visualiseerimine

Visualiseerimiseks kasutati Apache Superseti, mis ühendati PostgreSQL andmebaasiga. See võimaldas visualiseeringud siduda otse andmebaasitabelitega, mistõttu sai ETL-töövoo tulemusena loodud andmeid dashboardil kasutada ilma graafikuid käsitsi ümber koostamata.

Dashboard sisaldas:

- rahvaarvu prognoosi,
- sündide ja surmade trende,
- rändesaldot,
- rahvastikupüramiidi,
- lasteaiakohtade vajaduse prognoosi.

Visualiseeringute eesmärk oli muuta tulemused lihtsamini tõlgendatavaks ning võimaldada stsenaariumite võrdlemist.

Analüüsi tulemused näitasid, et enamikus stsenaariumites rahvaarv väheneb ning loomulik iive püsib negatiivne. Prognoosi põhjal väheneb järk-järgult ka lasteaiakohtade vajadus. Oluline tulemus oli, et aastaks 2029 võrdsustub hinnanguline laste arv olemasolevate lasteaiakohtade arvuga ning järgnevatel aastatel võib vajadus olemasolevate kohtade arvust väiksemaks muutuda.

Projektis kasutati versioonihalduseks Git-repositooriumi, kus paiknesid kood, konfiguratsioonifailid ja dokumentatsioon. Töökeskkonna loomiseks kasutati Docker Compose’i, mille abil käivitati PostgreSQL ja Superset ühtses lokaalses keskkonnas. README-fail kirjeldas projekti arhitektuuri, andmeallikaid ning süsteemi käivitamise samme. Projekti oli võimalik käivitada nii VS Code devcontaineris kui ka otse host-arvutis terminalist.

---

## Väljakutsed

Peamisteks väljakutseteks osutusid API tabelite erinevad struktuurid, vanuserühmade teisendamine ning arenduskeskkondade erinev käitumine macOS- ja Windows-süsteemides. Projekti käivitamist mõjutasid ka Pythoni versioonide erinevus: uuema Pythoni versiooniga töötas pipeline mõnes keskkonnas probleemideta, kuid teistes tekkisid sõltuvuste ja lokaalse seadistusega seotud käivitusprobleemid. Selle riski vähendamiseks kasutati `requirements.txt` faili ning README-s kirjeldati täpsemalt projekti käivitamise samme.

Mõnes Windowsi keskkonnas ei olnud Docker devcontaineri sees otse kättesaadav, mistõttu tuli Docker Compose käske käivitada host-süsteemi terminalist. Probleemi leevendamiseks muudeti andmebaasi ühendus paindlikumaks keskkonnamuutuja `DB_URL` abil. Superseti ja PostgreSQL ühendamisel tekkis probleem, kuna Superseti konteineris puudus PostgreSQL draiver `psycopg2`, mis lahendati Dockerfile’i täiendamisega.

Suure hulga järjestikuste päringute tõttu katkestas Statistikaamet API vahel ajutiselt ühenduse. Selle vähendamiseks lisati päringute vahele lühikesed viivitused, mis muutsid andmete laadimise stabiilsemaks ja vähendasid API ülekoormamise riski.

Koostöö käigus tekkis GitHubis harude ühendamisel konflikt, sest eri rühmaliikmed olid muutnud samu faile. Konflikti lahendamiseks tuli võrrelda erinevaid lahendusi, otsustada, millised muudatused alles jätta ja ühendada töö toimivaks tervikuks. See andis praktilise kogemuse pull requestide, harude ühendamise ja versioonihalduse töövoo mõistmiseks.

Nendest probleemidest õppisime, et ETL-töövoo loomisel ei piisa ainult andmete töötlemise loogika kirjutamisest. Sama oluline on tagada, et töövoog käivituks erinevates arenduskeskkondades, vajalikud sõltuvused oleksid kirjeldatud ning andmebaasi ja visualiseerimisvahendi ühendused oleksid paindlikult seadistatavad.

---

## Teostajad

- Liis Lille
- Kata Maria Metsar
- Miina Voltri
- Jaak Ilves
