import requests
import pandas as pd

BASE_URL = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-dnma-par-uai-appareils/records"

def fetch_records(select: str, where: str, limit: int = 100) -> pd.DataFrame:
    offset = 0
    all_rows = []

    while True:
        params = {"select": select, "where": where, "limit": limit, "offset": offset}
        r = requests.get(BASE_URL, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        rows = data.get("results", [])

        if not rows:              # plus rien à récupérer
            break

        all_rows.extend(rows)     # on ajoute la page à la liste
        offset += len(rows)       # on avance

        if len(rows) < limit:     # dernière page
            break

    return pd.DataFrame(all_rows)
