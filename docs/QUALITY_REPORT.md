# KikuyuSent Quality Report (v1.1)

## 1. Data checks

| Check | Result |
|---|---|
| Official starter-kit validator (`python kit/validate.py --track sentiment --data data/kikuyu_dataset.csv`) | **PASS** |
| Team validator (`python validate.py`): balance, accent-insensitive near-duplicates, provenance confirmed | `[TO FILL: PASS]` |
| Records per label / split | 100 per label · 60/20/20 per label |
| Exact duplicates (after normalisation) | 0 |
| Accent-insensitive near-duplicates | v1 had 1 pair (`KIK-PILOT-013` / `KIK-POS-022`); fixed in v1.1 by replacing `KIK-POS-022` |
| Paraphrases across splits | v1 had 1 pair across train/dev (`KIK-PILOT-017` / `KIK-NEG-026`); fixed in v1.1 with a shared `group_id` in train |
| Private information (emails, phone numbers) | none found |
| Whitespace problems | 10 rows cleaned (tabs, line breaks, double spaces); no effect on v1 model predictions |

## 2. Review process

- Every record was reviewed by a fluent Kikuyu speaker who did not write it (`review_status = independently_reviewed`, `reviewer_code` ≠ `contributor_code`).
- `[TO FILL: Did the reviewer see the author's label? How were disagreements resolved? How many disagreements were there in the first pass, if recorded?]`
- **Second check (v1.1):** a structural and English-meaning comparison flagged 11 rows for re-review: possible label/meaning mismatches, a near-duplicate, a missing English meaning and a bracketed alternative spelling. The reviewer's decisions are in `review/v1.1_checks.csv`:

| Decision | Rows |
|---|---|
| kept as is | `[TO FILL]` |
| label changed | `[TO FILL]` |
| text corrected | `[TO FILL]` |
| English meaning corrected | `[TO FILL]` |
| sentence replaced (near-duplicate) | `KIK-POS-022` |

## 3. Model selection (dev only)

All models are trained on the 180 train sentences and compared on the 60 dev sentences (`results/dev_model_comparison.csv`). Test was not used for any choice.

| Model | Dev accuracy | Dev macro-F1 |
|---|---|---|
| Character TF-IDF + Logistic Regression | `[TO FILL]` | `[TO FILL]` |
| **Word + character TF-IDF + Logistic Regression (selected)** | `[TO FILL]` | `[TO FILL]` |
| Word + character TF-IDF + Linear SVM | `[TO FILL]` | `[TO FILL]` |
| Always one label (reference) | 0.333 | 0.167 |

## 4. Test results (v1.1, evaluated once)

| Metric | v1.1 test (final) | v1 test (archived) | Always-one-label |
|---|---|---|---|
| Accuracy | `[TO FILL]` | 0.667 (40/60) | 0.333 |
| Macro-F1 | `[TO FILL]` | 0.664 | 0.167 |
| F1 positive | `[TO FILL]` | 0.65 | — |
| F1 negative | `[TO FILL]` | 0.54 | — |
| F1 neutral | `[TO FILL]` | 0.80 | — |

**Test usage, stated openly:** the test split was evaluated once on v1 (11 Nov). After the documented cleanup (§1–2), the model was retrained on v1.1 and the test split was evaluated once more. No model, feature or threshold choice was made using test results. Both runs are recorded in `logs/test_runs.csv`.

Confusion matrix (v1.1 test, rows = actual, columns = predicted): `[TO FILL from results/test_confusion_matrix.csv]`

## 5. Error analysis (5 real test errors)

Explanations written by Robi (fluent speaker), from `results/test_predictions.csv`:

| # | Record | Kikuyu text | Meaning | Human label | Model | Why the model probably failed |
|---|---|---|---|---|---|---|
| 1 | `[TO FILL]` | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

Patterns to look for when writing the "why":
- **Negation:** *ti / nd- / -ti-* flips the meaning, but bag-of-words features don't model it.
- **Shared words:** the same word appears in positive and negative contexts.
- **Spelling variants:** acute/macron spellings are rare in training.
- **Neutral vs feeling words:** a factual sentence with an emotional-looking word.

## 6. Limitations

- 180 training sentences is very small; scores on 60 test sentences have wide uncertainty (±~12 percentage points).
- TF-IDF features ignore word order and negation scope.
- Mixed orthography splits character features across spellings.
- One main author (`[TO FILL]`): style diversity is limited.

## 7. Conclusion

The v1.1 dataset passes the official starter-kit validator, has complete per-record provenance fields and a documented change history. The baseline clearly beats the always-one-label floor but struggles with `[TO FILL: e.g. negative vs positive confusion]`. Next steps: more authors and dialects, more negation examples, and a consistent orthography experiment on dev.
