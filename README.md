# NextgenAI-DIA5-G1

Class: **DIA5**. Sub-group: **DIA5-G1**.

## Sub-group

G1, ESILV A4 DIA. Members: Ayoub LAMCHICHI, Maxence Tessier, Jérémie LEROY-DUBIEF, RASAKARAN Sharusan, Aurélien Guillout-Lacomblez, Aurelien Roche, hechmi Chemli.

## Pack and database

- Pack `2026-10-14-students-1`.
- `data/boutique.sqlite` SHA-256: `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`.

## Environment

Environment verified on Aurélien Guillout-Lacomblez's Windows machine on 25 October 2026: Python 3.13.9, `requests` 2.34.2, SQLite 3.51.0. These are the reproduction environment versions, not a claim that every operator used the same versions during the session.

Python 3.10 or later is required. Only `check_access.py` needs `requests`; the integrity check, replay and consolidation scripts use the standard library. Keys stay in `GROQ_API_KEY` and `OPENROUTER_API_KEY` environment variables. Offline replay needs no keys.

## Replay from a fresh clone

Windows PowerShell (direct interpreter use avoids activation-policy issues):

```powershell
git clone https://github.com/Ayaube/NextgenAI-DIA5-G1.git
cd NextgenAI-DIA5-G1
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install requests
.\.venv\Scripts\python.exe verify-data.py
.\.venv\Scripts\python.exe skeleton-multi-llm-en.py --replay traces-td1.jsonl --state traces-replay.jsonl --out traces-replay.csv
```

On Linux or macOS, use `python3 -m venv .venv`, then `.venv/bin/python` for the same install, verification and replay commands.

The integrity check must end with `"ok": true`. `.gitattributes` preserves LF line endings for the distributed data CSVs and `schema.sql`, including on Windows, so their SHA-256 hashes remain identical to the manifest.

Replay executes the stored SQL locally and writes separate files with `nature = replay`. It makes no model calls. Keep the original `traces-td1.csv` and JSONL as the evidence of the real batch. To rebuild the submitted summaries from the original per-operator files, run `python consolider_td1.py`; this overwrites the consolidated outputs.

## Completed work

TD 1: twenty checked references, 105 recorded attempts and 100 final cells, the comparison, its pivot and the five-model summary. Qwen C16 and C18 remain `not_executed` after two HTTP 429 responses each. The explanations and limitations are documented in the report. TD 2 voting is not implemented yet.

## AI assistance

Coding and analysis assistance used in this chat is disclosed in [ai-assistance.md](ai-assistance.md), with the relevant requests and the checks performed. The experiment's system message and user template are in [prompts-en.md](prompts-en.md).

## Session report

[reports/td1.md](reports/td1.md).
