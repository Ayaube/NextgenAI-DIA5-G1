"""Consolidates the TD 1 lots into the hand-in files. Rerun after each new lot.

Reads the raw traces of each lot (one row per attempt, written by skeleton-multi-llm-en.py)
and the per-lot comparison files written by the operators, then writes:
  - traces-td1.csv                    all attempts of all lots, one header
  - model-question-comparison-en.csv  one final row per model/question (last attempt wins)
  - comparison-pivot.md               models x questions view of that CSV, for the plenary
  - five-model-summary-en.csv         the five models: portfolio index/prices, access, results by family

Values and verdicts always come from the traces; only the explanations come from the
operators' comparison files. A lot whose trace file is absent is reported as missing.
"""
import csv
import json
import os
from collections import OrderedDict

# Lot -> (raw trace file, state file, operator's comparison file). Names as pushed by each operator.
LOTS = OrderedDict([
    ("A", ("trace_A.csv", "state_A.jsonl", "comparison_A.csv")),
    ("B", ("traces-B.csv", "state-B.jsonl", "comparaison B.csv")),
    ("C", ("traces-C.csv", "state-C.jsonl", "comparison-C.csv")),
    ("D", ("traces-D.csv", "state-D.jsonl", "comparison-D.csv")),
    ("E", ("traces-E.csv", "state-E.jsonl", "comparison-E.csv")),
])
# Required models of modeles-autorises.json, in lot order.
MODELS = OrderedDict([
    ("A", ("groq", "openai/gpt-oss-120b")),
    ("B", ("groq", "openai/gpt-oss-20b")),
    ("C", ("openrouter", "cohere/north-mini-code:free")),
    ("D", ("groq", "qwen/qwen3.8-27b")),
    ("E", ("openrouter", "dots-studio/dots-3-note-preview:free")),
])
COMPARISON_HEADER = ["case_id", "model_id", "trace_file", "cell_id", "nature", "status",
                     "value_cents", "reference_cents", "explanation"]
PORTFOLIO = "portefeuille-modeles-2026-09-28.csv"
PORTFOLIO_DATE = "2026-09-28"


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


questions = json.load(open("questions-td1.json", encoding="utf-8"))["questions"]
CASES = [q["id"] for q in questions]
TYPES = {q["id"]: q["type"] for q in questions}

# 1. traces-td1.csv: every attempt of every lot present.
all_rows, header, present = [], None, OrderedDict()
for lot, (trace_file, _, _) in LOTS.items():
    if not os.path.exists(trace_file):
        continue
    rows = read_csv(trace_file)
    header = header or list(rows[0].keys())
    if list(rows[0].keys()) != header:
        raise SystemExit(f"{trace_file}: columns differ from the other trace files")
    all_rows += rows
    present[lot] = rows
write_csv("traces-td1.csv", header, [[r[k] for k in header] for r in all_rows])

# 2. model-question-comparison-en.csv: last attempt per cell, operator's explanation if any.
explanations = {}
for lot, (_, _, comparison_file) in LOTS.items():
    if os.path.exists(comparison_file):
        for r in read_csv(comparison_file):
            if r.get("explanation", "").strip():
                explanations[r["cell_id"]] = r["explanation"].strip()

final = OrderedDict()  # lot -> case -> last trace row
for lot, rows in present.items():
    last = {}
    for r in rows:  # rows are written in attempt order
        last[r["case_id"]] = r
    final[lot] = last

comparison = []
for lot, last in final.items():
    trace_file = LOTS[lot][0]
    for case in CASES:
        r = last.get(case)
        if r is None:
            provider, model = MODELS[lot]
            comparison.append([case, f"{provider}:{model}", trace_file, f"{provider}:{model}:{case}", "real",
                               "not_executed", "", "", "No attempt recorded in the trace file."])
            continue
        explanation = explanations.get(r["cell_id"])
        if not explanation:
            if r["verdict"] == "correct":
                explanation = f"Value equals the reference. Last attempt {r['attempts']}."
            else:
                explanation = (f"TO EXPLAIN from the SQL in the trace ({r['verdict_detail'] or r['error']}). "
                               f"Last attempt {r['attempts']}.")
        comparison.append([case, f"{r['provider']}:{r['model_requested']}", trace_file, r["cell_id"], r["nature"],
                           r["verdict"], r["value"], r["reference"], explanation])
write_csv("model-question-comparison-en.csv", COMPARISON_HEADER, comparison)

# 3. comparison-pivot.md: the matrix is a view of the long CSV, not a second entry.
SHORT = {"correct": "OK", "incorrect": "wrong", "sql_invalid": "SQL err", "sql_rejected": "rejected",
         "access_error": "access", "not_executed": "not run"}
lines = ["# TD 1 - models x questions (view of model-question-comparison-en.csv)", "",
         "| Model | " + " | ".join(CASES) + " | correct |",
         "|---|" + "---|" * (len(CASES) + 1)]
for lot, last in final.items():
    cells = [SHORT.get(last[c]["verdict"], last[c]["verdict"]) if c in last else "-" for c in CASES]
    ok = sum(1 for c in CASES if c in last and last[c]["verdict"] == "correct")
    lines.append(f"| {lot} {MODELS[lot][1]} | " + " | ".join(cells) + f" | {ok}/20 |")
missing = [lot for lot in LOTS if lot not in final]
if missing:
    lines += ["", f"Lots not yet available: {', '.join(missing)}."]
lines += ["", "OK correct, wrong = value differs from the reference, SQL err = SQL could not run, "
              "not run = no answer (access failure or retry budget exhausted)."]
open("comparison-pivot.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")

# 4. five-model-summary-en.csv
portfolio = {(r["identifiant_gate"], r["gate"]): r for r in read_csv(PORTFOLIO)}
FAMILIES = OrderedDict([
    ("period_results", lambda t: t == "period"),
    ("age_results", lambda t: t.startswith("age") and "+" not in t),
    ("product_results", lambda t: t == "product list"),
    ("combined_results", lambda t: "+" in t),
])
ACCESS = {
    "groq": "Groq Free plan, operator's personal account, no payment method; temperature 0, capped output, 45 s timeout",
    "openrouter": "OpenRouter :free route, operator's personal account, provider.max_price = 0, no credits bought; "
                  "temperature 0, capped output, 45 s timeout",
}


def family_result(last, predicate):
    cases = [c for c in CASES if predicate(TYPES[c])]
    done = [c for c in cases if c in last]
    ok = [c for c in done if last[c]["verdict"] == "correct"]
    access = [c for c in done if last[c]["verdict"] in ("not_executed", "access_error")]
    evaluated = [c for c in done if c not in access]
    wrong = [f"{c} {last[c]['verdict']}" for c in evaluated if c not in ok]
    text = f"{len(ok)}/{len(evaluated)} correct ({','.join(cases)})"
    if wrong:
        text += "; " + ", ".join(wrong)
    text += f"; access failures/not run: {len(access)}" + (f" ({','.join(access)})" if access else "")
    return text


summary_header = read_csv("five-model-summary-en.csv")[0].keys() if read_csv("five-model-summary-en.csv") else None
summary_header = list(summary_header)
summary = []
for lot, (provider, model) in MODELS.items():
    free_route = portfolio.get((model, provider))
    paid = next((r for (m, g), r in portfolio.items() if m == model and r["acces"] == "payant"), None)
    index = (free_route or paid or {}).get("score_public", "")
    row = {"provider": provider, "model_id": model}
    if index:
        row.update(public_index=index, index_date=PORTFOLIO_DATE, index_source=f"{PORTFOLIO} (kit)")
    else:
        row.update(public_index="N/A", index_date="",
                   index_source=f"N/A: model absent from {PORTFOLIO} or index not recorded there")
    if paid:
        row.update(paid_route_same_model=f"{paid['cle']} (pay-per-token)",
                   input_usd_per_million=paid["prix_entree_usd_m"], output_usd_per_million=paid["prix_sortie_usd_m"],
                   price_date=PORTFOLIO_DATE, price_source=f"{PORTFOLIO} (kit)")
    else:
        row.update(paid_route_same_model="N/A: no paid route of this exact model documented in the kit portfolio",
                   input_usd_per_million="N/A", output_usd_per_million="N/A", price_date="", price_source="")
    row["access_used"] = ACCESS[provider]
    trace_file, state_file, _ = LOTS[lot]
    limits = ["One real run of 20 questions at temperature 0: a routing hypothesis for this batch, not a general ranking."]
    if lot == "C":
        limits.append("The kit template listed inclusionai/ling-3.0-flash-sante:free on this row; replaced by the model "
                      "actually called, cohere/north-mini-code:free, as selected in modeles-autorises.json (14/10/2026).")
    if lot in final:
        last = final[lot]
        for column, predicate in FAMILIES.items():
            row[column] = family_result(last, predicate)
        retries = sum(1 for r in present[lot] if r["attempts"] == "2")
        http429 = sorted({r["case_id"] for r in present[lot] if r["http_status"] == "429"})
        if http429:
            limits.append(f"HTTP 429 rate limit on {','.join(http429)}; {retries} retried attempt(s) recorded.")
        row["trace_files"] = f"{trace_file}; {state_file}; traces-td1.csv"
    else:
        for column in FAMILIES:
            row[column] = "not run yet"
        row["trace_files"] = ""
    row["limits"] = " ".join(limits)
    summary.append([row.get(k, "") for k in summary_header])
write_csv("five-model-summary-en.csv", summary_header, summary)

print(f"traces-td1.csv: {len(all_rows)} attempts from lots {', '.join(present)}")
print(f"model-question-comparison-en.csv: {len(comparison)} rows")
todo = [f"{row[1]} {row[0]}" for row in comparison if row[8].startswith("TO EXPLAIN")]
print("explanations still to write:", ", ".join(todo) or "none")
print("lots missing:", ", ".join(missing) or "none")
