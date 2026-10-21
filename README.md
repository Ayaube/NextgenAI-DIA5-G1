# NextgenAI-DIA5-G1

Next-Generation AI (Trustworthy generative AI), ESILV A4 DIA, sub-group G1. Shared repository for TD 1 to TD 3.

## Members

| Name |
|---|
| Ayoub LAMCHICHI |
| Maxence Tessier |
| Jérémie LEROY-DUBIEF |
| RASAKARAN Sharusan |
| Aurélien Guillout-Lacomblez |
| Aurelien Roche |
| hechmi Chemli |

Who wrote and who checked each reference query: columns `written_by` and `checked_by` of `reference-td1.csv`. Contributions per session: `reports/td1.md`.

## Kit and data

- Kit `2026-10-14-students-1` at the repository root. `modeles-autorises.json` of the 2026-10-18 pack differs only by its status text: same five models, same parameters.
- Database `data/boutique.sqlite`, never modified: SHA-256 `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`, seed 20260925, as in `data/manifest.json`.
- Configuration read by the code: `modeles-autorises.json` (models, providers, parameters). No replacement model was used.

## Environment

Python 3.12.3 (3.10 or later required), `requests` 2.34.2 in a virtual environment, SQLite 3.45.1. API keys only in the environment variables `GROQ_API_KEY` and `OPENROUTER_API_KEY`, never in the repository.

## Replay from a fresh clone

```bash
git clone https://github.com/Ayaube/NextgenAI-DIA5-G1.git && cd NextgenAI-DIA5-G1
python3 -m venv .venv && . .venv/bin/activate && pip install requests
python verify-data.py                                   # database integrity, expects "ok": true
python check_access.py --no-network                     # local checks, no call
for c in Requetes_TD1/C*.sql; do sqlite3 -readonly data/boutique.sqlite < "$c"; done   # the 20 references
python skeleton-multi-llm-en.py --replay traces-td1.jsonl  # re-executes the stored SQL offline, no key
python skeleton-multi-llm-en.py --rates --state traces-td1.jsonl
python consolider_td1.py                                # rebuilds the hand-in files from the raw traces
```

A real batch (network, keys, quota) was run once per model; do not rerun it to reproduce results:

```bash
python skeleton-multi-llm-en.py --run --models groq:qwen/qwen3.8-27b --state state-D.jsonl --out traces-D.csv
```

## TD 1 files

| File | Content |
|---|---|
| `reference-td1.csv` | C01 to C20: query, value, author, checker. One query per question in `Requetes_TD1/` |
| `trace_A.csv`, `traces-B.csv` ... `traces-E.csv`, `state_A.jsonl`, `state-B.jsonl` ... `state-E.jsonl` | Raw attempts of each operator's lot (A GPT-OSS 120B, B GPT-OSS 20B, C Cohere North Mini Code, D Qwen 3.8 27B, E Dots 3 Note) |
| `traces-td1.csv`, `traces-td1.jsonl` | All 105 attempts of the five lots, including HTTP 429 errors and retries |
| `model-question-comparison-en.csv` | 100 final rows, one per model and question, with explanation and trace pointer |
| `comparison-pivot.md` | Models x questions view of that CSV |
| `five-model-summary-en.csv` | Five models: public index, prices, access, results by question family |
| `prompts-en.md` | System message and user template as used, fingerprint per question |
| `reports/td1.md` | Session report |

## Status

TD 1: twenty references written and independently checked by another member, five lots and both summaries done. Open: `reports/td1.md`.
