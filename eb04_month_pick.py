import argparse
import pandas as pd
from api_client import fetch_records

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--uai", required=True)
    parser.add_argument("--year", type=int, required=True)
    args = parser.parse_args()

    select = "debutsemaine,uai,visites_ordinateur,visites_smartphone,visites_tablette"
    where = (
        f"uai = '{args.uai}' "
        f"AND debutsemaine >= '{args.year}-01-01' "
        f"AND debutsemaine < '{args.year+1}-01-01'"
    )

    df = fetch_records(select, where, limit=100)

    if df.empty:
        print("Aucune donnée trouvée.")
        return

    # Convertir date + créer mois
    df["debutsemaine"] = pd.to_datetime(df["debutsemaine"], errors="coerce")
    df["mois"] = df["debutsemaine"].dt.month

    # Nettoyage numeric
    cols = ["visites_ordinateur", "visites_smartphone", "visites_tablette"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    # Agrégation mensuelle
    monthly = df.groupby("mois", as_index=False)[cols].sum()
    monthly["total_visites"] = monthly[cols].sum(axis=1)

    # Trouver le mois de pic
    peak = monthly.loc[monthly["total_visites"].idxmax()].copy()

    # Appareil dominant sur ce mois
    device_cols = {
        "ordinateur": peak["visites_ordinateur"],
        "smartphone": peak["visites_smartphone"],
        "tablette": peak["visites_tablette"],
    }
    appareil_dominant = max(device_cols, key=device_cols.get)
    visites_appareil_dominant = device_cols[appareil_dominant]

    print("Mois de pic (UAI, année):", args.uai, args.year)
    print("mois:", int(peak["mois"]))
    print("total_visites:", int(peak["total_visites"]))
    print("appareil_dominant:", appareil_dominant)
    print("visites_appareil_dominant:", int(visites_appareil_dominant))

if __name__ == "__main__":
    main()