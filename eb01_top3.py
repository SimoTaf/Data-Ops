import pandas as pd
from api_client import fetch_records

uai = "0010024W"

select = "debutsemaine,uai,visites_ordinateur,visites_smartphone,visites_tablette"
where = f"uai = '{uai}' AND debutsemaine >= '2025-01-01' AND debutsemaine < '2026-01-01'"

df = fetch_records(select, where, limit=100)

df["debutsemaine"] = pd.to_datetime(df["debutsemaine"], errors="coerce")
df["semaine"] = df["debutsemaine"].dt.isocalendar().week

cols = ["visites_ordinateur", "visites_smartphone", "visites_tablette"]
df["nb_visites"] = df[cols].sum(axis=1)

top3 = (
    df.groupby("semaine", as_index=False)["nb_visites"].sum()
      .sort_values("nb_visites", ascending=False)
      .head(3)
)

print("\nTop 3 semaines 2025 (Semaine | Nb Visites)")
print(top3.to_string(index=False))