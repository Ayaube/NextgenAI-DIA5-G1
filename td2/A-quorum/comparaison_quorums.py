"""Pair A: compare fixed 2/3 and 3/5 quorums using stored TD1 traces only."""
import csv
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
HERE = Path(__file__).resolve().parent
MODELS = {
    "A": ("groq", "openai/gpt-oss-120b"),
    "B": ("groq", "openai/gpt-oss-20b"),
    "C": ("openrouter", "cohere/north-mini-code:free"),
    "D": ("groq", "qwen/qwen3.8-27b"),
    "E": ("openrouter", "dots-studio/dots-3-note-preview:free"),
}
PANEL_3 = [MODELS[label] for label in "ACD"]
PANEL_5 = list(MODELS.values())
SOURCES = [ROOT / "trace_A.csv", ROOT / "traces-B.csv", ROOT / "traces-C.csv",
           ROOT / "traces-D.csv", HERE / "traces-E.csv"]
GITHUB_COMMIT = "af26f14022229f3bbfc2c095e9976b426c9fc0d9"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_vote():
    spec = importlib.util.spec_from_file_location("pair_a_skeleton", ROOT / "skeleton-multi-llm-en.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return lambda proposals, k: module.Orchestrateur.vote_k_sur_n(None, proposals, k)


def proposals_for(latest, case, panel):
    """Convert stored verdicts to execution status; never pass a reference."""
    proposals = []
    for provider, model in panel:
        key = (provider, model, case)
        if key not in latest:
            # Missing trace is a data gap, not evidence of a provider failure.
            raise ValueError(f"Missing TD1 trace: {provider}:{model}:{case}")
        row = latest[key]
        executed = row["verdict"] in {"correct", "incorrect"} and row["value"] not in {None, ""}
        proposals.append(SimpleNamespace(provider=provider, model_requested=model,
                                         value=int(row["value"]) if executed else None,
                                         verdict="executed" if executed else "error"))
    return proposals


def comparison(vote, latest, case, reference):
    # Both votes are made before consulting the reference for scoring.
    three = vote(proposals_for(latest, case, PANEL_3), 2)
    five = vote(proposals_for(latest, case, PANEL_5), 3)
    output = {"case_id": case, "reference": reference}
    for suffix, result, k in [("2of3", three, 2), ("3of5", five, 3)]:
        output.update({f"decision_{suffix}": "consensus" if result["consensus"] else "abstention",
                       f"value_{suffix}": result["value"] if result["consensus"] else "",
                       f"votes_{suffix}": result["votes"],
                       f"margin_{suffix}": result["votes"] - k,
                       f"matches_reference_{suffix}": result["value"] == reference if result["consensus"] else "",
                       f"models_{suffix}": " | ".join(result["models"])})
    output["decision_changed"] = (three["consensus"], three["value"]) != (five["consensus"], five["value"])
    return output


def cell(row):
    value = row["value"] if row["value"] not in {None, ""} else "—"
    text = f"{value} ({row['verdict']})"
    if row.get("http_status") and row["http_status"] != "200":
        text += f" ; HTTP {row['http_status']}"
    return text


def result_text(row, suffix):
    decision = row[f"decision_{suffix}"]
    if decision == "abstention":
        return "abstention / —"
    return f"consensus / {row[f'value_{suffix}']}"


def main():
    questions = json.loads((ROOT / "questions-td1.json").read_text(encoding="utf-8"))["questions"]
    cases = [q["id"] for q in questions]
    if cases != [f"C{i:02}" for i in range(1, 21)]:
        raise ValueError("Expected the twenty TD1 questions C01 to C20")
    refs = {r["case_id"]: int(r["revenue_cents"]) for r in read_csv(ROOT / "reference-td1.csv")}
    records, sources, owners = [], [], {}
    for path in SOURCES:
        rows = read_csv(path)
        rel = path.relative_to(ROOT).as_posix()
        sources.append({"file": rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "rows": len(rows)})
        for index, row in enumerate(rows, 1):
            key = (row["provider"], row["model_requested"], row["case_id"])
            if key[:2] not in PANEL_5 or row["case_id"] not in cases or row["nature"] != "real":
                raise ValueError(f"Unexpected model, case or nature in {rel}, record {index}")
            if key in owners and owners[key] != rel:
                raise ValueError(f"Overlapping experiment exports for {key}")
            owners[key] = rel
            if int(row["reference"]) != refs[row["case_id"]]:
                raise ValueError(f"Conflicting reference for {key}")
            records.append((row, rel, index))
    # Stable sorting preserves CSV attempt order when timestamps are equal.
    records.sort(key=lambda item: datetime.fromisoformat(item[0]["date_utc"]))
    for case in cases:
        hashes = {r["prompt_sha256"] for r, _, _ in records if r["case_id"] == case}
        if len(hashes) != 1:
            raise ValueError(f"Incompatible prompts for {case}")
    latest, selected = {}, {}
    for row, path, index in records:
        key = (row["provider"], row["model_requested"], row["case_id"])
        latest[key] = row
        selected[key] = {"source": path, "csv_record": index, "date_utc": row["date_utc"],
                         "value": row["value"], "verdict": row["verdict"], "http_status": row.get("http_status", ""),
                         "error": row.get("error", "")}
    vote = load_vote()
    results = []
    for case in cases:
        row = comparison(vote, latest, case, refs[case])
        b, e = latest[(*MODELS["B"], case)], latest[(*MODELS["E"], case)]
        note = "Décision changée" if row["decision_changed"] else "Même décision"
        note += f" ; B={cell(b)} ; E={cell(e)}. Max voix {row['votes_2of3']}→{row['votes_3of5']}, seuil 2→3, marge {row['margin_2of3']:+d}→{row['margin_3of5']:+d}."
        row["comment"] = note
        results.append(row)
    write_csv(HERE / "comparaison-quorums.csv", results)
    write_csv(HERE / "traces-td1-merged.csv", [r for r, _, _ in records])
    provenance = {"github_commit_for_E": GITHUB_COMMIT,
                  "github_source_E": f"https://github.com/Ayaube/NextgenAI-DIA5-G1/blob/{GITHUB_COMMIT}/traces-E.csv",
                  "sources": sources, "method": "last attempt per provider/model/case after stable UTC sort; no new API call",
                  "selected_cells": {f"{label}:{case}": selected[(*key, case)] for label, key in MODELS.items() for case in cases}}
    (HERE / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run = subprocess.run([sys.executable, str(ROOT / "atelier-vote.py")], cwd=ROOT,
                         capture_output=True, text=True, encoding="utf-8", check=True)
    (HERE / "vote-synthetic.jsonl").write_text(run.stdout, encoding="utf-8")
    synthetic = [json.loads(line) for line in run.stdout.splitlines()]
    synthetic_table = "| Exemple | Propositions | Décision | Valeur | Voix | Référence | Accord |\n|---|---|---|---:|---:|---:|---|\n"
    values = ["100, 100, 120", "100, 110, 120", "100, indisponible, indisponible", "0, 0, 100"]
    for example, proposals in zip(synthetic, values):
        d = example["decision"]
        synthetic_table += f"| {example['example']} | {proposals} | {'consensus' if d['consensus'] else 'abstention'} | {d['value'] if d['consensus'] else '—'} | {d['votes']} | {example['reference']} | {('oui' if example['matches_reference'] else 'non') if d['consensus'] else 'sans réponse'} |\n"
    table = "| Cas | Référence | 2/3 : décision / valeur | Voix | Accord | 3/5 : décision / valeur | Voix | Accord |\n|---|---:|---|---:|---|---|---:|---|\n"
    comments = "| Cas | Effet de l'ajout de B et E (valeurs en centimes, verdicts des traces) |\n|---|---|\n"
    details = "| Cas | A : GPT-OSS-120B | B : GPT-OSS-20B | C : North | D : Qwen | E : Dots |\n|---|---|---|---|---|---|\n"
    for row in results:
        case = row["case_id"]
        agree3 = "oui" if row["matches_reference_2of3"] is True else "non" if row["matches_reference_2of3"] is False else "sans réponse"
        agree5 = "oui" if row["matches_reference_3of5"] is True else "non" if row["matches_reference_3of5"] is False else "sans réponse"
        table += f"| {case} | {row['reference']} | {result_text(row, '2of3')} | {row['votes_2of3']}/3 | {agree3} | {result_text(row, '3of5')} | {row['votes_3of5']}/5 | {agree5} |\n"
        comments += f"| {case} | {row['comment']} |\n"
        details += "| " + case + " | " + " | ".join(cell(latest[(*key, case)]) for key in MODELS.values()) + " |\n"
    changes = [r["case_id"] for r in results if r["decision_changed"]]
    summary = {suffix: {"correct_consensus": sum(r[f"matches_reference_{suffix}"] is True for r in results),
                        "wrong_consensus": sum(r[f"matches_reference_{suffix}"] is False for r in results),
                        "abstentions": sum(r[f"decision_{suffix}"] == "abstention" for r in results)} for suffix in ("2of3", "3of5")}
    report = f"""# TD2 — Pair A : vote et comparaison des quorums

Consigne finale `2026-11-18-students-5`, 18 novembre 2026. Contribution **Pair A / étape 1 uniquement**, à intégrer au rapport collectif après la revue croisée.

## 1. Méthode `vote_k_sur_n`

Implémentation dans [skeleton-multi-llm-en.py](skeleton-multi-llm-en.py), méthode `Orchestrateur.vote_k_sur_n`. Le reste du squelette TD1 est conservé.

`n` compte tous les membres, y compris les erreurs et indisponibilités. Le code refuse un seuil non entier ou hors de `n // 2 < k <= n`, ainsi qu'un doublon `(provider, model_requested)`. Il compte les valeurs entières des propositions `executed` uniquement. Dès qu'une valeur atteint k voix, il renvoie cette valeur et les modèles qui la soutiennent. Sinon il s'abstient, conserve le plus grand nombre de voix observé et renvoie `value=None`, `models=[]`. La valeur 0 est un vote valide.

La référence n'entre jamais dans le vote : `correct` et `incorrect` deviennent tous deux `executed`. Les erreurs (`sql_invalid`, `not_executed`, etc.) deviennent `error` et ne votent pas, même si une valeur résiduelle était présente. Comparaison à la référence seulement après les deux décisions. Une trace absente fait échouer le script : elle n'est pas inventée ni assimilée à une panne du fournisseur.

## 2. Quatre exemples synthétiques exécutés

Commande : `python atelier-vote.py`. Sortie brute : [vote-synthetic.jsonl](vote-synthetic.jsonl). Ces exemples ne sont pas des résultats réels sur la boutique.

{synthetic_table}
Le cas « wrong consensus » montre pourquoi l'accord n'est pas une preuve de justesse. L'analyse SQL détaillée relève de Pair B.

## 3. Données et sélection des tentatives

- A : Groq / `openai/gpt-oss-120b`, [trace_A.csv](trace_A.csv).
- B : Groq / `openai/gpt-oss-20b`, [traces-B.csv](traces-B.csv).
- C : OpenRouter / `cohere/north-mini-code:free`, [traces-C.csv](traces-C.csv).
- D : Groq / `qwen/qwen3.8-27b`, [traces-D.csv](traces-D.csv).
- E : OpenRouter / `dots-studio/dots-3-note-preview:free`, [copie locale traces-E.csv](traces-E.csv), récupérée dans [le commit GitHub source](https://github.com/Ayaube/NextgenAI-DIA5-G1/blob/{GITHUB_COMMIT}/traces-E.csv).

105 lignes originales, dont 25 pour D, réduites à **100 cellules : 5 modèles × 20 questions** en gardant la dernière tentative par fournisseur/modèle/question. Tri chronologique stable : à date identique, l'ordre du CSV départage les tentatives. Aucun retour à une ancienne tentative réussie après un échec. Les exports A/B/C/D de GitHub sont identiques aux fichiers locaux ; les 20 références numériques et les hashes de prompts concordent pour les cinq modèles.

Le panel 2/3 est **A+C+D** ; le quorum 3/5 est **A+B+C+D+E**. B et A partagent la famille GPT-OSS : cinq modèles ne signifient pas cinq sources d'erreur indépendantes. Aucun nouvel appel API, aucune modification des prompts, aucune réouverture du TD1.

Référence : [reference-td1.csv](reference-td1.csv). [Traces fusionnées](traces-td1-merged.csv). [Provenance des 100 cellules](provenance.json) : fichier, numéro d'enregistrement CSV (hors en-tête, pas numéro de ligne physique), date, valeur, verdict, statut HTTP et erreur.

## 4. Comparaison commentée des vingt questions

Montants en centimes HT. « Voix » est le maximum obtenu par une valeur, même en cas d'abstention. « Accord » ne note que les consensus ; une abstention n'est pas une réponse numérique fausse.

{table}
**Bilan :** 2/3 = {summary['2of3']['correct_consensus']} consensus corrects, {summary['2of3']['wrong_consensus']} faux consensus, {summary['2of3']['abstentions']} abstention(s). 3/5 = {summary['3of5']['correct_consensus']} consensus corrects, {summary['3of5']['wrong_consensus']} faux consensus, {summary['3of5']['abstentions']} abstention(s). Changements de décision/valeur : {', '.join(changes) if changes else 'aucun'}.

### Explication de toutes les différences de voix et de marge

La marge vaut **nombre maximum de voix − k** : négative, aucun consensus ; nulle, seuil atteint exactement. L'ajout de B et E peut augmenter les voix sans améliorer cette marge puisque le seuil passe aussi de 2 à 3. Les valeurs et verdicts des deux modèles ajoutés sont cités pour chaque question ci-dessous ; ceux du panel initial figurent dans la section suivante.

{comments}
**C02 :** A et D votent 590 320 ; C est `sql_invalid`. Le 2/3 atteint exactement son seuil. B vote 0 (`incorrect`) tandis que E vote 590 320 (`correct`) : le 3/5 atteint aussi exactement son seuil, avec trois voix. L'erreur SQL de C ne réduit ni n=3 ni n=5.

**C17 :** A=258 180 (`correct`), C=105 840 (`incorrect`), D=248 490 (`incorrect`) : une voix maximum, donc abstention 2/3. B ajoute 258 180 (`correct`), E ajoute 152 730 (`incorrect`) : deux voix maximum, insuffisantes pour k=3. La référence vaut 258 180 mais le vote n'a pas le droit de la choisir grâce à cette connaissance.

**C16 et C18 :** la dernière tentative D est `not_executed` et ne vote pas. A et C suffisent au 2/3 ; B les rejoint au 3/5, tandis que E propose une autre valeur incorrecte. **C19 :** E est `sql_invalid` et D propose 83 580 (`incorrect`) ; A, B et C soutiennent 1 990, d'où le consensus 3/5. Ces verdicts proviennent des traces ; aucune panne HTTP 429 n'est supposée sans trace correspondante.

### Valeurs et verdicts exacts des 100 cellules retenues

{details}
## 5. Reproduction, tests et contribution

Depuis td2/A-quorum, avec Python standard, sans clé API :

```powershell
..\\..\\.venv\\Scripts\\python.exe atelier-vote.py
..\\..\\.venv\\Scripts\\python.exe comparaison_quorums.py
..\\..\\.venv\\Scripts\\python.exe test_vote.py
..\\..\\.venv\\Scripts\\python.exe atelier-vote.py --traces traces-td1-merged.csv --case C02
```

Le script produit ce rapport, le [CSV comparatif](comparaison-quorums.csv), les traces fusionnées, leur provenance et les quatre exemples. Les tests vérifient notamment les seuils, doublons, indisponibilités, zéros, votes incorrects et les 2/3 et 3/5 sur toutes les combinaisons de quatre valeurs possibles. Sortie : [tests.txt](tests.txt).

Contribution préparée avec assistance de Codex : implémentation, exécution hors ligne, comparaison et explications. Membres de Pair A : **à compléter**. À relire et expliquer à Pair B/C lors de la revue croisée. Le rapport collectif intégrera leurs travaux séparément ; ils ne sont pas réalisés dans cette contribution. Aucun commit, push ou dépôt Moodle effectué.
"""
    (ROOT / "rapport-A.md").write_text(report, encoding="utf-8")
    print(json.dumps({"cells": len(latest), "source_rows": len(records), "results": summary, "changed_decisions": changes}, ensure_ascii=False))


if __name__ == "__main__":
    main()
