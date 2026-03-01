import argparse
import pandas as pd
import matplotlib.pyplot as plt
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

    df["debutsemaine"] = pd.to_datetime(df["debutsemaine"], errors="coerce")
    df["mois"] = df["debutsemaine"].dt.month

    cols = ["visites_ordinateur", "visites_smartphone", "visites_tablette"]
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    monthly = df.groupby("mois", as_index=False)[cols].sum().sort_values("mois")

    plt.figure()
    for c in cols:
        plt.plot(monthly["mois"], monthly[c], label=c)
    plt.xlabel("Mois")
    plt.ylabel("Nombre de visites")
    plt.title(f"Evolution mensuelle des visites par appareil - UAI {args.uai} ({args.year})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"eb3_{args.uai}_{args.year}.png", dpi=150)
    print(f"Graph saved: eb3_{args.uai}_{args.year}.png")

if __name__ == "__main__":
    main()