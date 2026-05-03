from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine, text

OUTPUT_DIR = Path("Outputs")

DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5433/lasteaiakohad"
)

TABLES = {
    "rakvere_rahvastiku_prognoos_2026_2035.csv": "population_forecast",
    "rakvere_synnid_2026_2035.csv": "birth_forecast",
    "rakvere_lasteaiavajadus_2026_2030.csv": "kinder_need",
    "rakvere_kokkuvottev_tabel.csv": "summary",
    "rakvere_aastate_vordlus_tabel.csv": "yearly_kinder_compare",
    "rakvere_rahvaarvu_vordlus_tabel.csv": "population_compare",
    "rakvere_rande_saldo_2015_2024.csv": "migration_history",
    "rakvere_synnid_surmad_2018_2024.csv": "birth_death_history",
    "rakvere_rahvastikupuramiid_andmed.csv": "population_pyramid",
}


def main() -> None:
    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(
            "Outputs kausta ei leitud. Käivita enne: python Lasteaiakohad.py"
        )

    engine = create_engine(DB_URL)

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))

    loaded = []
    for filename, table_name in TABLES.items():
        path = OUTPUT_DIR / filename
        if not path.exists():
            print(f"JÄTAN VAHELE: {path} puudub")
            continue

        df = pd.read_csv(path, encoding="utf-8-sig")
        df.columns = [
            str(c).strip().lower().replace(" ", "_").replace("-", "_")
            for c in df.columns
        ]
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        loaded.append((table_name, len(df)))
        print(f"Laaditud tabel: {table_name} ({len(df)} rida)")

    if not loaded:
        raise RuntimeError("Ühtegi CSV-faili ei laaditud. Kontrolli Outputs kausta sisu.")

    print("\nValmis. PostgreSQL tabelid:")
    for table_name, n_rows in loaded:
        print(f"- {table_name}: {n_rows} rida")


if __name__ == "__main__":
    main()
