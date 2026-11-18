#!/usr/bin/env python3
"""TD 2, Pair C: exact TD 1 accuracy per question family and per model.

Reads the merged TD 1 traces and the question types, keeps the last attempt of
each cell (provider:model:question) and prints, for each family, the cells and
the correct / cases ratio of each model. No network call, standard library only.

Usage (from the repository root):
    python td2/C-routing/taux_par_famille.py
    python td2/C-routing/taux_par_famille.py --traces td1/traces-td1.csv --questions td1/questions-td1.json
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FAMILIES = {
    "period": "F1 period",
    "age on a reference date": "F2 completed age at a date",
    "age at the time of the order": "F2b age at the order",
    "product list": "F3 product list",
}


def find(name: str, explicit: Path | None) -> Path:
    candidates = [explicit] if explicit else [ROOT / name, ROOT / "td1" / name]
    for path in candidates:
        if path and path.exists():
            return path
    raise SystemExit(f"{name} not found (looked for {', '.join(str(c) for c in candidates)})")


def family_of(question_type: str) -> str:
    # A "+" combines filters: every combined type is reported in the combinations family.
    return FAMILIES.get(question_type, f"F4 combinations ({question_type})" if "+" in question_type else question_type)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--traces", type=Path, default=None)
    parser.add_argument("--questions", type=Path, default=None)
    args = parser.parse_args()

    traces_path = find("traces-td1.csv", args.traces)
    questions_path = find("questions-td1.json", args.questions)
    types = {q["id"]: q["type"] for q in json.loads(questions_path.read_text(encoding="utf-8"))["questions"]}

    last = {}
    with open(traces_path, newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):  # chronological: the last attempt of a cell wins
            if row["nature"] == "real":
                last[(row["case_id"], f"{row['provider']}:{row['model_requested']}")] = row

    models = sorted({model for _, model in last})
    by_family = defaultdict(list)
    for case_id, question_type in sorted(types.items()):
        by_family[family_of(question_type)].append(case_id)

    print(f"Source: {traces_path.name} (last real attempt per cell), {questions_path.name}\n")
    for family in sorted(by_family):
        cases = by_family[family]
        print(f"== {family}: {', '.join(cases)}")
        total_ok = total = 0
        for model in models:
            cells = [(c, last[(c, model)]["verdict"]) for c in cases if (c, model) in last]
            ok = sum(verdict == "correct" for _, verdict in cells)
            total_ok, total = total_ok + ok, total + len(cells)
            failures = ", ".join(f"{c} {verdict}" for c, verdict in cells if verdict != "correct")
            print(f"   {model:52} {ok}/{len(cells)}" + (f"   ({failures})" if failures else ""))
        print(f"   {'all five models':52} {total_ok}/{total}\n")


if __name__ == "__main__":
    main()
