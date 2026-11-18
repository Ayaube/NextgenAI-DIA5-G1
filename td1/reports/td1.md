# TD 1 report — NextgenAI-DIA5-G1

Session of 21 October 2026. Pack `2026-10-14-students-1`. Database `data/boutique.sqlite`, SHA-256 `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`.

This batch contains only real calls (`nature = real` on all 105 rows of [traces-td1.csv](../traces-td1.csv)). There is no replayed row and no simulated row. The two cells with no SQL are access failures, not synthetic examples.

## What was completed

1. Twenty reference queries in [reference-td1.csv](../reference-td1.csv), each written in `Requetes_TD1/Cxx.sql` and checked by another member. Values come from SQLite run read-only, not from a model.
2. Five model lots, one request at a time, temperature 0, on 21 October 2026 between 13:30 and 14:07 UTC. Raw files kept per operator, then merged.
3. [model-question-comparison-en.csv](../model-question-comparison-en.csv): 100 final cells. [comparison-pivot.md](../comparison-pivot.md) is only a view of that file.
4. [five-model-summary-en.csv](../five-model-summary-en.csv): index and prices taken from the kit portfolio of 28 September 2026 when the model is listed there.
5. The prompt actually sent is copied in [prompts-en.md](../prompts-en.md). It is the skeleton's `build_prompt()`, unchanged. Each question has one `prompt_sha256` across every model and every attempt.

`consolider_td1.py` rebuilds the merged traces, the 100-row comparison and the summary from the per-lot files. Verdicts are taken from the traces. Explanations are taken from the operators' comparison files.

## Scores

| Lot | Model | Final cells | Correct |
|---|---|---:|---:|
| A | `openai/gpt-oss-120b` (Groq) | 20 | 20 |
| B | `openai/gpt-oss-20b` (Groq) | 20 | 19 |
| C | `cohere/north-mini-code:free` (OpenRouter) | 20 | 14 |
| D | `qwen/qwen3.8-27b` (Groq) | 20 | 15 |
| E | `dots-studio/dots-3-note-preview:free` (OpenRouter) | 20 | 14 |

100 final cells: 82 correct, 14 incorrect, 2 invalid SQL, 2 not executed. The trace file has 105 rows because Qwen recorded 5 retries. Every first attempt is present. A retry is a second row of the same cell, not a new question.

By family, from [five-model-summary-en.csv](../five-model-summary-en.csv):

- Period (C01, C04, C05, C06, C07, C20): 6/6 on all five models, including the empty period C06, whose reference is 0.
- Product list (C03, C12, C13, C14): 4/4 on all five models, including the empty period with a product filter in C14.
- Age (C02, C08, C09, C10, C11): 5/5 for A and D, 4/5 for B and E, 0/5 for C.
- Combined (C15–C19): 5/5 for A and B, 4/5 for C, 0/5 for E. D has 0 correct, 3 incorrect and 2 not executed.

## Failures and causes

Causes below are the `explanation` of the final row in [model-question-comparison-en.csv](../model-question-comparison-en.csv), read against the SQL stored in the trace.

**Convention, completed age.** This is the only convention the models missed. The period bounds (`date >= start AND date < end`) and the product filter were applied correctly everywhere, including when the true total is 0.

- B, C02 (0 instead of 590320). The birth window is shifted by 25 years: `birth_date > 2025-09-25 AND <= 2026-09-25` instead of `> 2000-09-25 AND <= 2001-09-25`.
- C, C08 and C09 (both 0). The age predicate does not select customers of completed age 25. C11 is the same failure mode: the two date bounds contradict each other, so the sum is 0 instead of 446690. C10 casts `YYYY-MM-DD` to an integer and therefore drops the month and day (548920 instead of 558980). C17 subtracts a `MMYYYY` concatenation (105840 instead of 258180).
- D, C15 (0 instead of 168680). The predicate compares a month-day with itself in both directions (`<= '09-25'` and `> '09-25'`), which is always false. C17 is an off-by-one on the birthday: it drops the customer born on 2001-09-25 and keeps the one born on 2000-09-25 (248490 instead of 258180). C19 compares a year string with the full date `2026-09-25`, so the upper bound never applies (83580 instead of 1990).
- E, C09, C15, C16, C17 and C18. The SQL keeps `year difference = 25` and then requires the birthday to have passed. Customers born in 2000 whose anniversary is after the reference day have a year difference of 26 and a completed age of 25; they are excluded. C09 also uses a birth window that runs up to 2026.

**Invalid SQL.** The sandbox rejected the statement. The HTTP call had succeeded.

- C, C02: `syntax_error` near `AS`, an alias placed inside an arithmetic expression.
- E, C19: `near ")": syntax error`. `CAST(substr('2026-09-25', 1, 4)` has no `AS INTEGER`. The same statement also approximates a year as 365 days.

**Access refused, not a wrong answer.** D, C16 and C18. Both attempts returned HTTP 429, Groq Free output-tokens-per-minute limit (1000) on `qwen/qwen3.8-27b`. No SQL and no value. The retry budget is one extra attempt, so the cell stays `not_executed`. The same 429 hit the first attempt of C17, C19 and C20; the retry of those three cells did return SQL, and that SQL is what the comparison judges. Detail is on the 429 rows of [traces-D.csv](../traces-D.csv).

Completed age is the difference between the reference year and the birth year, minus one year if the birthday has not yet occurred on the reference date. For age at order time, the reference date is the date of that order. The observed age errors show why checking the month and day is necessary. Combining age with a period or a product list is where D and E fail questions while passing other cases in isolation. This single batch does not establish a general success rate.

## Portfolio reading

In this batch, `gpt-oss-120b` answered all twenty questions correctly. Its kit index is 11.6 (28 September 2026). The documented paid route of the same model is OpenRouter pay-per-token, 0.15 USD per million input tokens and 0.60 output. The calls used Groq Free. Native cost measurements are absent on all 65 Groq rows and remain empty; a free access route alone does not establish a measured zero. OpenRouter filled `cost_native` on all 40 of its rows.

`gpt-oss-20b` (index 9) misses only C02. The kit portfolio has no paid route for this exact model id. `qwen/qwen3.8-27b` (index 33.7) matches the 120b model on period, age and product, then fails the combined block, and the free tier did not finish two of those cells. Cohere North and Dots are absent from the portfolio file, so their index and paid price are N/A. Both are usable for period and product questions and unreliable for completed age.

`model_returned` differs from `model_requested` only on the seven Qwen 429 rows, where the returned name is empty. No provider substituted another model.

## Limitations

- One run per cell. A wrong value is the value of that call.
- Groq does not report a native cost. Prices in the summary are the kit's paid-route documentation, not the invoice of this batch.
- C16 and C18 of Qwen are unmeasured. Counting them as model errors would mix an access failure with a bad convention.
- Cohere and Dots have no public index in the supplied portfolio, so the sheet cannot rank them on that axis.
- The skeleton was not modified. TD 2 voting is not implemented yet.

## Contributions

Names as written in `Requetes_TD1/` and on the commits that added each lot.

| Member | References | Model lot |
|---|---|---|
| Aurelien Roche | C01, C02, C03, written. Checked C04, C05, C06. | A, `gpt-oss-120b`: [trace_A.csv](../trace_A.csv), [comparison_A.csv](../comparison_A.csv) |
| hechmi Chemli | C04, C05, C06, written. Checked C07, C08, C09. | C, Cohere: [traces-C.csv](../traces-C.csv), [comparison-C.csv](../comparison-C.csv) |
| Ayoub LAMCHICHI | C07, C08, C09, written. Checked C10, C11, C12. | D, Qwen: [traces-D.csv](../traces-D.csv), [comparison-D.csv](../comparison-D.csv). Merged the five lots (`consolider_td1.py`) and wrote [prompts-en.md](../prompts-en.md). |
| RASAKARAN Sharusan | C10, C11, C12, written. Checked C13, C14, C15. | |
| Jérémie LEROY-DUBIEF | C13, C14, C15, written. Checked C01, C02, C03. Maintained `reference-td1.csv`. | E, Dots: [traces-E.csv](../traces-E.csv), [comparison-E.csv](../comparison-E.csv) |
| Aurélien Guillout-Lacomblez | C16, C17, C18, written. Checked C19, C20. | B, `gpt-oss-20b`: [traces-B.csv](../traces-B.csv), [comparaison B.csv](../comparaison%20B.csv). Git author `Aurélien`, distinct from Aurélien Roche's commits of lot A. |
| Maxence Tessier | C19, C20, written. Checked C16, C17, C18. | |

## Next steps

TD 2 reads these traces and adds the vote in `skeleton-multi-llm-en.py` (`atelier-vote.py` is the workshop version). No new network batch unless the instructor assigns one. Replayed rows, if a pilot trace is used later, stay `nature = replay` and out of the real counts.

## AI assistance and verification

Aurélien Guillout-Lacomblez used Codex to help draft C16–C18, populate the model B comparison from its saved traces, understand the protocol, and review the hand-in. On 25 October, Codex also helped correct the README, this report and Git line-ending settings. The relevant user requests and the scope of assistance are retained in [ai-assistance.md](../ai-assistance.md).

The C16–C18 amounts were obtained by executing the SQL on the supplied read-only database and checked independently by a calculation on the supplied CSVs. Model B's comparison was checked against `traces-B.csv`, including the incorrect C02 birth-date filter. The final review executed the twenty reference queries, rechecked returned SQL and prompt fingerprints, and compared the merged CSV/JSONL with the saved attempts. The reference amounts and recorded model outputs were not invented by the assistant. The group remains responsible for explaining the queries, checks and conclusions.
