# KikuyuSent Quality Report (v1.1)

## 1. Data checks

| Check | Result |
|---|---|
| Official starter-kit validator (`python kit/validate.py --track sentiment --data data/kikuyu_dataset.csv`) | **PASS**: 300 records |
| Team validator (`python validate.py`): exact 100/100/100 balance, accent-insensitive near-duplicates kept in one group, provenance confirmed | **PASS** |
| Records per label / split | 100 per label; 60 / 20 / 20 per label |
| Exact duplicates (after normalisation) | 0 |
| Accent-insensitive near-duplicates | 1 pair (`KIK-PILOT-013` / `KIK-POS-022`, both train, shared group). Kept by team decision and documented. |
| Same prompt across splits | 1 pair (`KIK-PILOT-017` train / `KIK-NEG-026` dev, different Kikuyu wording). Test unaffected. |
| Private information (emails, phone numbers) | None found |
| Whitespace problems | 10 rows cleaned. The model trained on cleaned text predicts **identically** to the v1 model on all 300 rows. |

## 2. Review process

1. **Collection review.** Every row was reviewed by someone other than its contributor: team members cross-reviewed rows they had not produced, and outside fluent Kikuyu speakers also reviewed. Reviewers are recorded as a pool (`T05-XREV`), not per row.
2. **v1.1 re-check.** An automated comparison of each Kikuyu sentence with its English prompt flagged 11 rows: possible meaning or label mismatches, a near-duplicate, a bracketed alternative spelling and a missing English prompt. Robi (T05-A, fluent) re-checked all 11 and confirmed every sentence and label as correct, so none was changed (`review/v1.1_checks.csv`). The automated flags came from a non-speaker comparing against the English, and the fluent speaker's judgement prevails.

## 3. Model selection (dev only)

All models were trained on the 180 train sentences and compared on the 60 dev sentences (`results/dev_model_comparison.csv`). Test was not used for any choice.

| Model | Dev accuracy | Dev macro-F1 |
|---|---|---|
| Character 2–5-gram TF-IDF + Logistic Regression | 0.600 | 0.606 |
| **Word 1–2-gram + character 2–5-gram TF-IDF + Logistic Regression (selected)** | **0.633** | **0.643** |
| Word + character TF-IDF + Linear SVM | 0.617 | 0.621 |
| Always one label (reference floor) | 0.333 | 0.167 |

## 4. Test results

| Metric | v1.1 test (final) | Always one label |
|---|---|---|
| Accuracy | **0.667** (40/60) | 0.333 |
| Macro-F1 | **0.664** | 0.167 |
| F1 positive | 0.65 (precision 0.61, recall 0.70) | — |
| F1 negative | 0.54 (precision 0.59, recall 0.50) | — |
| F1 neutral | 0.80 (precision 0.80, recall 0.80) | — |

Confusion matrix (rows = actual, columns = predicted):

| | → positive | → negative | → neutral |
|---|---|---|---|
| **positive** | 14 | 5 | 1 |
| **negative** | 7 | 10 | 3 |
| **neutral** | 2 | 2 | 16 |

**Test usage, stated openly:** the test split was evaluated once on v1 (11 Nov). After the v1.1 cleanup (whitespace only, no label, text or split change), the model was retrained and test was evaluated once more. Predictions and scores were identical (0.667 / 0.664). No choice was made using test results. Both runs are in `logs/test_runs.csv`.

**Reading the numbers:** the model is twice as accurate as guessing one label. Neutral is easiest. Negative is hardest: 7 of the 20 negative sentences were called positive. With only 60 test sentences, the accuracy has an uncertainty of roughly ±12 percentage points.

## 5. Error analysis: 5 real test errors

Each explanation uses the model's own feature weights (which words pushed it towards the wrong label) and how often those words appear with each label in the 180 training sentences. Meanings come from the dataset's English prompts.

| # | Record | Kikuyu text | Meaning | Human | Model | Why it failed |
|---|---|---|---|---|---|---|
| 1 | `KIK-NEU-024` | Mwana akomete mũno | The child is sleeping deeply | neutral | **positive** (p = 0.73) | **Intensifier shortcut.** *mũno* ("very/deeply") is in 30 positive, 10 negative and 0 neutral training sentences, so the model treats it as a positive signal even in a plain factual statement. |
| 2 | `KIK-PILOT-007` | Nĩ ndĩ na kĩeha nĩ ũndũ wa huduma ĩyo itarĩ njega. | I am disappointed because the service was poor | negative | **positive** (0.47 vs 0.39) | **Negation.** *njega* ("good") pushes towards positive, but the sentence says *itarĩ njega* ("was **not** good"). Word and character n-grams can't tell that the negator flips *njega*. *kĩeha* ("sadness") appears in only 2 training sentences. |
| 3 | `KIK-POS-205` | Indo iria ciatũmirwo ciakinyire irĩ ndungĩra. | The delivery arrived in good condition | positive | **negative** (p = 0.64) | **Near-identical training sentence with the opposite label.** Train has `KIK-NEG-083` *Indo iria ciatũmirwo ciakinyire irĩ na thũkũmo* ("…arrived damaged"). Five of six words are shared, so the shared frame outweighs the one word that carries the sentiment (*ndungĩra*). |
| 4 | `KIK-NEG-062` | Rũgendo rũu rwarĩ rũrũra na rwa kũnoga mũno. | The journey was stressful and exhausting | negative | **positive** (p = 0.63) | **Template and intensifier overlap.** *rũu*, *rwarĩ* and *rwa* appear only in positive training sentences (e.g. `KIK-POS-076` *Rũgendo rũu rwarĩ rwa gĩkeno mũno* "The journey was enjoyable"), and *mũno* adds positive weight. The negative words (*rũrũra*, *kũnoga*) are unseen in training. |
| 5 | `KIK-NEG-278` | Kĩndũ kĩu gĩgĩthũka thuutha wa mũthenya ũmwe. | The product broke after one day | negative | **neutral** (p = 0.53) | **Topic shortcut.** *mũthenya* ("day") appears in 7 training sentences, all neutral (times and dates), so time words pull towards neutral. The verb carrying the complaint, *gĩgĩthũka* ("it broke"), never appears in training. |

**Patterns:**
- The model learns **surface cues**: the intensifier *mũno* → positive, time words → neutral, and shared sentence frames. It does not learn sentiment itself.
- It **cannot handle negation** (*-ti-*, *ta-*, *nd-*).
- **Unseen sentiment words** (most verbs and adjectives appear only once) leave function words to decide.

**Fixes for the next version:** more sentences per sentiment word; contrastive pairs placed together in one split; sentences with negation for every label; *mũno* in neutral sentences; more contributors.

## 6. Limitations

- 180 training sentences is very small, and 60 test sentences give wide uncertainty.
- TF-IDF ignores word order and the scope of negation.
- Mixed orthography splits character features across spellings.
- Author and reviewer were recorded per pool, not per row.

## 7. Conclusion

The v1.1 dataset passes the official starter-kit validator, has complete provenance fields and a row-by-row change log. Every test evaluation is logged. The baseline doubles the always-one-label accuracy (0.667 vs 0.333; macro-F1 0.664 vs 0.167). Its errors come from surface cues and negation, which points directly at what data to collect next.
