# Pair B - etape 1 : chercher dans traces-td1.csv les valeurs fausses partagees
# Usage : python3 td2_pairB/01_valeurs_fausses_partagees.py
import csv
from collections import defaultdict

lignes = list(csv.DictReader(open("traces-td1.csv", encoding="utf-8")))
print("nombre de lignes dans le fichier :", len(lignes))

# Il y a plus de 100 lignes car un HTTP 429 a ete reessaye (colonne attempts).
# On garde la DERNIERE tentative de chaque (modele, question) = 100 cellules.
cellules = {}
for l in lignes:
    cellules[(l["model_requested"], l["case_id"])] = l
print("cellules (modele x question) :", len(cellules))

# Repartition des verdicts
verdicts = defaultdict(int)
for l in cellules.values():
    verdicts[l["verdict"]] += 1
print("verdicts :", dict(verdicts))

# Pour chaque question, on regroupe les modeles qui ont rendu la meme valeur FAUSSE
# (verdict incorrect avec une vraie valeur ; sql_invalid / not_executed n'ont pas de valeur)
fausses = defaultdict(list)
for (modele, case), l in cellules.items():
    if l["verdict"] == "incorrect" and l["value"] != "":
        fausses[(case, l["value"])].append(modele)

print()
print("Valeurs fausses rendues, question par question :")
for (case, valeur), modeles in sorted(fausses.items()):
    print(" ", case, "valeur", valeur, "->", modeles)

print()
partagees = [(c, v, m) for (c, v), m in fausses.items() if len(m) >= 2]
if partagees:
    print("VALEURS FAUSSES PARTAGEES :", partagees)
else:
    print("Aucune valeur fausse partagee entre 2 modeles dans nos 100 cellules.")
    print("=> on utilise le cas historique DEMO-SQL-C11 (voir 03_c11_demo.py)")
