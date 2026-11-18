# TD 1 - models x questions (view of model-question-comparison-en.csv)

| Model | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | C15 | C16 | C17 | C18 | C19 | C20 | correct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A openai/gpt-oss-120b | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | 20/20 |
| B openai/gpt-oss-20b | OK | wrong | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | 19/20 |
| C cohere/north-mini-code:free | OK | SQL err | OK | OK | OK | OK | OK | wrong | wrong | wrong | wrong | OK | OK | OK | OK | OK | wrong | OK | OK | OK | 14/20 |
| D qwen/qwen3.8-27b | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | wrong | not run | wrong | not run | wrong | OK | 15/20 |
| E dots-studio/dots-3-note-preview:free | OK | OK | OK | OK | OK | OK | OK | OK | wrong | OK | OK | OK | OK | OK | wrong | wrong | wrong | wrong | SQL err | OK | 14/20 |

OK correct, wrong = value differs from the reference, SQL err = SQL could not run, not run = no answer (access failure or retry budget exhausted).
