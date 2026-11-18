## Step 3 — Routing rule (period and age at the order)

Written by RASAKARAN Sharusan. Families covered: period (C01, C04, C05, C06, C07, C20) and age at the order (C10). The rule is in [routing-rule-td2.md](../routing-rule-td2.md).

### What was done

1. The rule was written from the TD 1 results ([comparison-pivot.md](../comparison-pivot.md)) before looking at the simulator outcomes.
2. The kit simulator was run unchanged: [routage-avant.jsonl](../routage-avant.jsonl).
3. [atelier-routage.py](../atelier-routage.py) was adapted: `RESOURCES` now holds the five TD 1 models plus the paid OpenRouter route of gpt-oss-120b, a `RULE` table gives the order, evidence and checks per family and use, and `choose` applies it. The seven kit scenarios are kept by name and re-expressed with the two families; two scenarios were added (Groq unavailable for a period question, customer figure).
4. The adapted simulator was run: [routage-apres.jsonl](../routage-apres.jsonl).

Reproduce from the repository root:

```bash
python atelier-routage.py > routage-apres.jsonl
python atelier-routage.py --scenario deferrable
```

### Observed facts

- Period: all five models 6/6, including the one-day periods C05 and C07 and the empty period C06 (reference 0).
- C10: four models return 558 980 (reference), cohere returns 548 920. Its SQL casts `strftime('%Y-%m-%d', birth_date)` to INTEGER, which keeps only the year in SQLite: the age is a year difference that ignores the birthday.
- Qwen received an HTTP 429 on C20 and succeeded on the second attempt ([traces-td1.csv](../traces-td1.csv)).

### Before and after

| Scenario | Before (kit rule, fictitious resources) | After (DIA5-G1 rule) |
|---|---|---|
| simple | run small-free | period, dashboard: run gpt-oss-20b (Groq) |
| complex | run senior-subscription | age at order, dashboard: run gpt-oss-120b (Groq) |
| deferrable | defer senior-subscription, 60 min | Groq exhausted: defer gpt-oss-120b, 60 min |
| urgent | run senior-api, 0.30 USD | Groq exhausted, 5 min: run paid gpt-oss-120b on OpenRouter, 0.000285 USD |
| budget exhausted | abstain | abstain (cohere and dots not eligible on age) |
| high impact | run senior-subscription, human review | payout: run gpt-oss-120b, reference query and human review |
| unknown capability | abstain (difficulty 4) | abstain (family `combined` not covered by this part of the rule) |
| preferred provider unavailable | not in kit | period, Groq exhausted: run cohere on OpenRouter |
| customer figure | not in kit | period: run gpt-oss-20b, 2-of-3 quorum gpt-oss-20b, cohere, dots |

Main differences: eligibility is decided per family from TD 1 cells instead of a single capability level; the check depends on the use (dashboard, customer, payout) instead of a single high-impact flag; the fallback changes provider first, because three of the five models depend on Groq; every reason cites the TD 1 cells.

### Hypotheses and limits

- Age at the order rests on one question (C10). The rule borrows the four age-on-a-date questions because they share the completed-age convention; this is an assumption.
- One run at temperature 0 on twenty questions: a routing hypothesis for this batch, not an error rate or a ranking.
- Availability and reset times in the simulator are scenario assumptions, not measurements. The paid cost is an estimate with a fixed token envelope.
- The fixed workshop panel (gpt-oss-120b, cohere, qwen) is in practice a 2-of-2 on age, since cohere is wrong on all age questions. A panel for customer figures on age should replace cohere (here by dots).

### Next steps

- Merge with the rules of the other families (age on a date, product list, combinations).
- In TD 3, measure the real cost of the quorum and of the paid fallback on the combined questions, where no free model other than the gpt-oss pair is reliable.
