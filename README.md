# NextgenAI-DIA5-G1

## Sub-group

G1, ESILV A4 DIA. Members: Ayoub LAMCHICHI, Maxence Tessier, Jérémie LEROY-DUBIEF, RASAKARAN Sharusan, Aurélien Guillout-Lacomblez, Aurelien Roche, hechmi Chemli.

## Pack and database

- Pack `2026-10-14-students-1`.
- `data/boutique.sqlite` SHA-256: `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`.

## Environment

Python 3.12.3, `requests` 2.34.2, SQLite 3.45.1. Keys in `GROQ_API_KEY` and `OPENROUTER_API_KEY` only.

## Replay from a fresh clone

```bash
git clone https://github.com/Ayaube/NextgenAI-DIA5-G1.git && cd NextgenAI-DIA5-G1
python3 -m venv .venv && . .venv/bin/activate && pip install requests
python verify-data.py
python skeleton-multi-llm-en.py --replay traces-td1.jsonl
python consolider_td1.py
```

## Completed work

TD 1: twenty checked references, five model lots, comparison and five-model summary.

## Session report

[reports/td1.md](reports/td1.md).
