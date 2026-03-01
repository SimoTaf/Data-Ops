import argparse
import pandas as pd
from api_client import fetch_records

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--uai", required=True)
    parser.add_argument("--granularity", required=True, choices=["Annee", "Mois"])
    args = parser.parse_args()

    select = "debutsemaine,uai,visites_ordinateur,visites_smartphone,visites_tablette"
    where = f"uai = '{args.uai}'"

    df = fetch_records(select, where, limit=100)

    if df.empty:
        print("Aucune donnée trouvée pour cette UAI.")
        return

    df["debutsemaine"] = pd.to_datetime(df["debutsemaine"], errors="coerce")
    df["annee"] = df["debutsemaine"].dt.year
    df["mois"] = df["debutsemaine"].dt.month

    cols = ["visites_ordinateur", "visites_smartphone", "visites_tablette"]
    df["nb_visites"] = df[cols].sum(axis=1)

    if args.granularity == "Annee":
        out = df.groupby("annee", as_index=False)["nb_visites"].sum().sort_values("annee")
    else:
        out = df.groupby(["annee", "mois"], as_index=False)["nb_visites"].sum().sort_values(["annee", "mois"])

    print(out.to_string(index=False))

if __name__ == "__main__":
    main()