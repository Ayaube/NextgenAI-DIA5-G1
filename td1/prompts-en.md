# Prompts used in TD 1

The prompt is the one of the kit's `skeleton-multi-llm-en.py` (pack 2026-10-14-students-1), **unchanged**, identical for the five models.
The skeleton builds it in `build_prompt()`: `{schema}` is the content of `schema.sql`, `{question}` the English question of `questions-td1.json`.
The fingerprint written in every trace line is `sha256(system + "\n" + user)`.

## System message

```text
You write SQLite queries for a small e-commerce database. Reply with exactly one SQLite SELECT statement and nothing else: no explanation, no comments, no markdown other than an optional ```sql fence.
```

## User template

```text
Schema (SQLite):
{schema}

Conventions (binding):
- product.price is the unit price in euro cents, excluding VAT (an integer). Revenue excluding VAT is SUM(quantity_product * price), an integer number of cents.
- orders holds order lines: one row per (order_id, product_id). All lines of an order share the same customer_id and the same date.
- orders.date and customers.insert_date are UTC timestamps stored as text 'YYYY-MM-DD HH:MM:SS'. customers.birth_date is a date stored as text 'YYYY-MM-DD'. Compare them as text or with SQLite date functions.
- A period "from S to E" is closed on the left and open on the right: date >= S AND date < E.
- A customer's age on a day D is the number of completed years: someone born on B is N years old on D when the N-th anniversary of B is on or before D and the (N+1)-th anniversary is after D. "Exactly 25 years old" means completed age 25 on that day, computed from month and day, never from the year difference alone.
- Unless the question says "at the time of the order", ages are computed on the reference date given in the question.
- The query must return exactly one row and one column named revenue_cents. When no order line matches, return 0 (use COALESCE), not NULL.
- Use only the tables above. One SELECT statement, nothing else.

Question: {question}
```

## Fingerprint per question

One fingerprint per question across all lots and attempts (checked on `traces-td1.csv`): the same prompt was sent to every model, so a gap between models comes from the model, not from the wording.

| Question | prompt_sha256 | Models |
|---|---|---|
| C01 | `d25f63730bdd4980e31c3e5a449f59f3410bcee3a2cfc132d8f38efab03b1bdd` | 5 |
| C02 | `42b91ea47ed6f10aa79e4579ad12fb7a5191e12b1a3fb82b79d253b9d9ae8a62` | 5 |
| C03 | `5d8e7c01aa0646ca4a352456f4abb4665fc48e546a82767d6827a905d70d21be` | 5 |
| C04 | `c2a73db35adea5cd8622a7c03a9ba03687f12bfcd2e4b40893c93685f34016f4` | 5 |
| C05 | `b96a003b2b5ae4511254b974c61e08af86ceed7421a162c48b1590f9e646b70c` | 5 |
| C06 | `e10af71902d58af793255a62dee11db30da6f4df4588be141bb0a82b03923258` | 5 |
| C07 | `7fef6bd6a1dac0bfc655deb9e35dc04f960b8b8a276b49f6a727a88e1c67c2aa` | 5 |
| C08 | `d875514cab7aae73cb92d4378c96e2e5291e14746c05baf6fa28d1449c19e99c` | 5 |
| C09 | `8a183ea0b704135aacad9681a454de5f091062bf148a3b9e43cbdec6c7cc8c19` | 5 |
| C10 | `bf06c7f2b73ebaad7deca36db05e5d26b7de0e2e97fbf7f829b3471f2b256aca` | 5 |
| C11 | `2f368d80930bd7ca3aef95d2966b5d542f1703819851b2503f1837b628fafd88` | 5 |
| C12 | `428f3d31cb2a9021446721741fd70f330bb83ca218791305e04bf6732a36bc74` | 5 |
| C13 | `8df2423fb78cd6ef6bf4157943bec37c0f05ff124ae276122f3e53ac78f6a88a` | 5 |
| C14 | `a0715dbffe3d8f9c9245ace5031860493ab079cd524a1403b9a1a5cce391e167` | 5 |
| C15 | `524c019f96e7672f941e11be69dc0f2575dfc5c95719259d6d6f013cada492ad` | 5 |
| C16 | `ebc89bbcb01e5890298132161b6ed675899a8d158b7a56619aa3636504d6bca7` | 5 |
| C17 | `a99fd1bb3b8d470a035c26906d2c14623694590b52ad8bd3d7d392ca305f4d75` | 5 |
| C18 | `2df965d9a03714e645bf78bd50249f8585da3f3d832d14605e72c7777836b985` | 5 |
| C19 | `e5396619f946e273f11d2baf48666f84d8a817fde9f7189579c96ce2c2a14119` | 5 |
| C20 | `3ff11fcc9b7dce0bdf408c10ec54d9f7d7944f363aa6f85a9c6d4d6df145a0ef` | 5 |

No variant of the prompt was used.
