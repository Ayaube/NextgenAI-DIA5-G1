# TD 2 - Step 3 (Pair C): the routing rule

Goal: assign each question family to **the cheapest model that remains up to it**, with a level of checking set by **what an error costs**, and a course of action when the first model is unavailable. The rule is locked to the exact TD 1 rates below, then exercised on `atelier-routage.py`.

Source data: `traces-td1.csv` (merged TD 1 traces, last **real** attempt per cell) and `questions-td1.json` (question types). No new network call.

## Files

| File | Content |
|---|---|
| `taux_par_famille.py` | Recomputes the table below from the traces: `python td2/C-routing/taux_par_famille.py` (from the repository root) |
| `simulateur-avant.txt` | Output of the supplied `atelier-routage.py`, seven scenarios, **before** adaptation (`nature = simulation`) |
| `simulateur-apres.txt` | *To do*: output after adapting `RESOURCES` and `choose` |
| `review-1.md`, `review-2.md` | Cross-review by the other pairs |

## 1. Exact TD 1 rates per family

Correct / cases per model. Failures are listed with their verdict.

| Family | Cells | gpt-oss-120b | gpt-oss-20b | qwen3.8-27b | north-mini-code | dots-3-note | All |
|---|---|---|---|---|---|---|---|
| F1 period | C01, C04, C05, C06, C07, C20 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | **30/30** |
| F2 completed age at a date | C02, C08, C09, C11 | 4/4 | 3/4 (C02 incorrect) | 4/4 | **0/4** (C02 sql_invalid; C08, C09, C11 incorrect) | 3/4 (C09 incorrect) | **14/20** |
| F2b age at the order | C10 | 1/1 | 1/1 | 1/1 | 0/1 (C10 incorrect) | 1/1 | **4/5** |
| F3 product list | C03, C12, C13, C14 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | **20/20** |
| F4 period + age at a date | C15 | 1/1 | 1/1 | 0/1 (incorrect) | 1/1 | 0/1 (incorrect) | 3/5 |
| F4 age at a date + product | C16 | 1/1 | 1/1 | 0/1 (**not_executed**, HTTP 429) | 1/1 | 0/1 (incorrect) | 3/5 |
| F4 period + age at a date + product | C17, C19 | 2/2 | 2/2 | 0/2 (C17, C19 incorrect) | 1/2 (C17 incorrect) | 0/2 (C17 incorrect, C19 sql_invalid) | 5/10 |
| F4 period + age at the order | C18 | 1/1 | 1/1 | 0/1 (**not_executed**, HTTP 429) | 1/1 | 0/1 (incorrect) | 3/5 |

Reading notes:
- Qwen's C16 and C18 are **access failures** (HTTP 429, output-token rate limit on Groq, 2026-10-21 13:33 UTC, two attempts each), **not wrong answers**. Qwen is therefore *not measured* on these two cells; it is not proven wrong there.
- Only **gpt-oss-120b** and **gpt-oss-20b** are correct on every combined cell (C15 to C19).
- Twenty questions support a **batch-specific hypothesis**, not a general error rate, a permanent ranking or a quorum error guarantee. One or four cells per family is a small sample.

## 2. Prices (portfolio `portefeuille-modeles-2026-09-28.csv`, read on 2026-09-28)

| Model | Group | Public index | Route used in TD 1 | Paid route of the same model (input / output USD per M tokens) |
|---|---|---|---|---|
| openai/gpt-oss-120b | G5 (Groq Free) / G4 (OpenRouter paid) | 11.6 | Groq Free, 0 | OpenRouter, 0.15 / 0.60 |
| openai/gpt-oss-20b | G5 | 9 | Groq Free, 0 | N/A: none documented in the portfolio |
| qwen/qwen3.8-27b | G5 | 33.7 | Groq Free, 0 | N/A: none documented in the portfolio |
| cohere/north-mini-code:free | - | N/A | OpenRouter `:free`, 0 | N/A: absent from the portfolio |
| dots-studio/dots-3-note-preview:free | - | N/A | OpenRouter `:free`, 0 | N/A: absent from the portfolio |

All five cost 0 on the free routes used. What differs is the **quota** (Groq Free limits per minute and per day; OpenRouter `:free` limits) and the fallback price if a paid route is needed.

## 3. The rule (one page)

> *To complete and validate in the sub-group.* Constraint from the assignment: `none` (a single free model, no check) is admissible **only** for a low-stakes internal dashboard **and** on a family where that model scored **100 %** in TD 1. As soon as the model made one error on the family, or the figure is shown to a customer or governs a payout, the rule requires a **quorum** or a **deterministic check**.

| Family | Cells cited | Models at 100 % in TD 1 | First model called | Check: internal dashboard | Check: figure shown to the customer | Check: amount paid out | If the first model is unavailable |
|---|---|---|---|---|---|---|---|
| F1 period | C01, C04, C05, C06, C07, C20 | all five | | | | | |
| F2 completed age at a date | C02, C08, C09, C11 | 120b, qwen | | | | | |
| F2b age at the order | C10 | 120b, 20b, qwen, dots | | | | | |
| F3 product list | C03, C12, C13, C14 | all five | | | | | |
| F4 combinations | C15 to C19 | 120b, 20b | | | | | |

For "if unavailable", use the order of lecture 2: capacity already paid for (subscription) → free model up to the request → **wait for the refill if the request can wait** → paid route within the budget → **abstention** or a person.

## 4. Simulator

- **Before adaptation:** `simulateur-avant.txt`. The supplied fictitious resources are `small-free` (level 1), `senior-subscription` (level 3, `cash 0`, `allocation 0.04`) and `senior-api` (level 3, `cash 0.30`). Decisions: simple → `small-free`; complex → `senior-subscription`; deferrable → `defer` 60 min; urgent → `senior-api`; budget exhausted → `abstain`; high impact → subscription + "source verification and human review"; unknown capability (level 4) → `abstain`.
- **After adaptation:** *to do.* Replace `RESOURCES` with the portfolio models, an eligibility level per family derived from the table in section 1, and their price. Cite the justifying TD 1 cells in the `reason` string of every decision. Then save the output to `simulateur-apres.txt`.

## 5. Priority order in `choose`

*To write.* The question: why does an immediately available subscription (`cash == 0`, `allocation > 0`) come **before** deferring to wait for an exhausted free resource (`cash == 0`, `allocation == 0`) whose refill falls before `deadline_minutes`? Under what operational condition should this priority be reversed?
