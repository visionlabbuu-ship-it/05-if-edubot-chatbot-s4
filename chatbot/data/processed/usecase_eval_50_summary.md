# Use-case evaluation (50) — after system prompt fix

## Compared to previous run (before prompt fix)

| Metric | Before | **After** |
|--------|--------|-----------|
| Avg score 0–5 | 4.70 | **4.94** |
| good | 46 | **50** |
| weak | 4 | **0** |
| poor | 0 | **0** |
| good+ok | 92% | **100%** |
| Wall time | ~85s | ~85s |
| Index | 1079 tight | 1079 tight |
| Model | llama3.2 | llama3.2 |

### Previously weak → now

| Q | Topic | Before | After |
|---|--------|--------|-------|
| 3 | working radius | weak (over-refuse) | **good/5** |
| 9 | safety before MovJ | weak | **good/5** |
| 35 | Studio network check | weak | **good/5** |
| 46 | brakes | weak | **good/5** |

## Category averages (after)

| Category | Avg |
|----------|-----|
| network / python_api / studio / hardware / teaching | 5.00 |
| safety | 4.83 |
| spec / demo | 4.88 |

## Files (overwritten this run)
- `chatbot/data/processed/usecase_eval_50.csv`
- `chatbot/data/processed/usecase_eval_50.json`
- this summary

## Notes
- Auto scorer: keyword + doc_type + length (not full human factual audit).
- Prompt change reduced over-refusal; residual risk is small-model paraphrase drift.
- UI: http://localhost:8501
