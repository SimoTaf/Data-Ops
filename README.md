# Test Pratique DataOps – DNMA (EFFIOS)

Ce dépôt répond au test pratique DataOps à partir du dataset **fr-en-dnma-par-uai-appareils** (DNMA).  
La partie pratique utilise l'API publique (Explore v2.1) afin d'éviter la manipulation locale de fichiers volumineux.  
La pagination est gérée via `limit` / `offset`.

---

## Installation

```bash
python3 -m venv .data
source .data/bin/activate
pip install -r requirements.txt
```

---

## Exercices

### EB1 – Top 3 semaines (2025) pour l'UAI `0010024W`

```bash
python3 eb01_top3.py
```

---

### EB2 – Agrégation par granularité

```bash
python3 eb02_aggregate.py --uai 0010024W --granularity Annee
python3 eb02_aggregate.py --uai 0010024W --granularity Mois
```

---

### EB3 – Graphique mensuel des visites par appareil (ordinateur / smartphone / tablette)

```bash
python3 eb03_plot.py --uai 0010024W --year 2025
```

> Le script génère : `eb3_0010024W_2025.png`

---

### EB4 – Mois de pic + appareil dominant

```bash
python3 eb04_month_pick.py --uai 0010024W --year 2025
```

---

## API

**Endpoint :**

```
https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-dnma-par-uai-appareils/records
```

**Champs utilisés :**

| Champ | Description |
|---|---|
| `debutsemaine` | Date de début de semaine |
| `uai` | Identifiant de l'établissement |
| `visites_ordinateur` | Nombre de visites depuis un ordinateur |
| `visites_smartphone` | Nombre de visites depuis un smartphone |
| `visites_tablette` | Nombre de visites depuis une tablette |

---

## Commit final

```bash
git add .
git commit -m "feat: DNMA API solution for EB1-EB4"
git status
```