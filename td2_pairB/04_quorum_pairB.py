# Pair B - comptage des votes (version simple, faite pour verifier la methode vote_k_sur_n de Pair A)
# Usage (depuis la racine du repo) : python3 td2_pairB/04_quorum_pairB.py
import csv
from collections import Counter

PANEL_3 = ["openai/gpt-oss-120b", "cohere/north-mini-code:free", "qwen/qwen3.8-27b"]
PANEL_5 = PANEL_3 + ["openai/gpt-oss-20b", "dots-studio/dots-3-note-preview:free"]

def vote(propositions, k):
    # propositions : liste de (modele, valeur) ; valeur = None si erreur / indisponible
    # l'indisponible reste dans n mais ne vote pas
    n = len(propositions)
    if not (n // 2 < k <= n):
        raise ValueError("k doit etre une majorite stricte de n")
    noms = [m for m, v in propositions]
    if len(set(noms)) != len(noms):
        raise ValueError("deux propositions du meme modele")
    compteur = Counter([v for m, v in propositions if v is not None])
    if len(compteur) == 0:
        return {"consensus": False, "value": None, "votes": 0, "models": []}
    valeur, nb = compteur.most_common(1)[0]
    if nb >= k:
        return {"consensus": True, "value": valeur, "votes": nb,
                "models": [m for m, v in propositions if v == valeur]}
    return {"consensus": False, "value": None, "votes": nb, "models": []}

# ---- on lit les traces : derniere tentative de chaque (modele, question) ----
cellules = {}
for l in csv.DictReader(open("traces-td1.csv", encoding="utf-8")):
    cellules[(l["model_requested"], l["case_id"])] = l

def propositions(case, modeles):
    res = []
    for m in modeles:
        l = cellules[(m, case)]
        if l["verdict"] in ("correct", "incorrect") and l["value"] != "":
            res.append((m, int(l["value"])))
        else:
            res.append((m, None))   # sql_invalid ou not_executed : reste dans n
    return res

ref = {}
for r in csv.DictReader(open("reference-td1.csv", encoding="utf-8")):
    ref[r["case_id"]] = int(r["revenue_cents"])

# ---- 1. C11 sur NOS traces reelles ----
print("=== C11, traces reelles de traces-td1.csv ===")
for m, v in propositions("C11", PANEL_5):
    print("  ", m, "->", v)
print("reference :", ref["C11"])
print("2-sur-3 :", vote(propositions("C11", PANEL_3), 2))
print("3-sur-5 :", vote(propositions("C11", PANEL_5), 3))

# ---- 2. C11 historique (septembre 2026) : M1 et M2 rendent 0 ----
# SCENARIO REJOUE : on remplace les 2 propositions de 20b et north par les valeurs historiques (0 et 0)
# et on garde nos valeurs reelles pour les 3 autres modeles (120B, Qwen, Dots).
print()
print("=== C11 historique (rejoue) : 20b=0 et north=0 ===")
hist = {
    "openai/gpt-oss-120b": 446690,
    "cohere/north-mini-code:free": 0,
    "qwen/qwen3.8-27b": 446690,
    "openai/gpt-oss-20b": 0,
    "dots-studio/dots-3-note-preview:free": 446690,
}
p5 = [(m, hist[m]) for m in PANEL_5]
p3_fixe = [(m, hist[m]) for m in PANEL_3]
p3_faible = [(m, hist[m]) for m in ["openai/gpt-oss-20b", "cohere/north-mini-code:free", "openai/gpt-oss-120b"]]
print("panel fixe 2-sur-3 (120B, north, qwen)  :", vote(p3_fixe, 2))
print("panel 2-sur-3 (20b, north, 120B)        :", vote(p3_faible, 2))
print("quorum 3-sur-5 (les 5 modeles)          :", vote(p5, 3))

# contre-exemple : si un 3e modele avait le meme bug, le 3-sur-5 serait trompe aussi
p5_pire = [(m, (0 if m == "qwen/qwen3.8-27b" else hist[m])) for m in PANEL_5]
print("3-sur-5 si qwen faisait aussi 0 (hypothese) :", vote(p5_pire, 3))

# ---- 3. DEMO-VOTE (jouet) ----
print()
print("=== DEMO-VOTE : propositions [0, 0, 100], reference 100 ===")
jouet = [("modele_1", 0), ("modele_2", 0), ("modele_3", 100)]
print("2-sur-3 :", vote(jouet, 2))

# ---- 4. Dans les 20 questions, est-ce qu'une valeur FAUSSE atteint le quorum ? ----
print()
print("=== Une valeur fausse gagne-t-elle quelque part (traces reelles) ? ===")
for nom, panel, k in [("2-sur-3", PANEL_3, 2), ("3-sur-5", PANEL_5, 3)]:
    faux_gagnants = []
    abstentions = []
    for i in range(1, 21):
        case = "C%02d" % i
        r = vote(propositions(case, panel), k)
        if r["consensus"] and r["value"] != ref[case]:
            faux_gagnants.append(case)
        if not r["consensus"]:
            abstentions.append(case)
    print(nom, ": wrong consensus =", faux_gagnants, "| abstentions =", abstentions)
