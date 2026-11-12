# KikuyuSent: Kikuyu Sentence Sentiment

**Strathmore NLP Hub Datathon 2026 · Team 5 "Zeus" · Track B (sentiment) · Kikuyu (Gĩkũyũ), `ki-KE`**

KikuyuSent classifies a Kikuyu sentence as **positive**, **negative** or **neutral**. We built a new, human-written, independently reviewed dataset of 300 Kikuyu sentences, trained a transparent baseline, and demonstrate it in Streamlit.

## Results (dataset v1.1, held-out test, evaluated once)

| Model | Test accuracy | Test macro-F1 |
|---|---|---|
| **Word + character TF-IDF + Logistic Regression** | **0.667** (40/60) | **0.664** |
| Always one label (reference floor) | 0.333 | 0.167 |

Per-label F1: positive 0.65 · negative 0.54 · neutral 0.80. The model was chosen on dev only (dev macro-F1 0.643; `results/dev_model_comparison.csv`).
v1.1 only cleaned whitespace and added provenance fields. The retrained model predicts identically to v1 on all 300 sentences, so the v1 and v1.1 test runs match. Both are logged in `logs/test_runs.csv`.
**Improved model v2 (Kikuyu-aware).** On **60 fresh sentences** written and reviewed on 12 Nov (`KIK-301…360`), scored once: improved setup **70.0% accuracy / 0.699 macro-F1** vs official 66.7% / 0.671 (`docs/QUALITY_REPORT.md` §9). The demo app runs a single model, v2: this setup retrained on all 360 sentences.
Post-freeze experiment (cross-validation only, test untouched): Kikuyu-aware preprocessing using fluent-speaker spelling and negator lists raises CV macro-F1 from 0.655 to 0.699 (`docs/QUALITY_REPORT.md` §8).
Error analysis (5 real failures: intensifier shortcut, negation, near-identical frames, unseen sentiment words) is in `docs/QUALITY_REPORT.md`.

## Dataset

| | positive | negative | neutral | total |
|---|---|---|---|---|
| train | 60 | 60 | 60 | 180 |
| dev | 20 | 20 | 20 | 60 |
| test | 20 | 20 | 20 | 60 |

- `data/kikuyu_dataset.csv`: starter-kit schema, **passes the official kit validator**.
- Every sentence was produced by a person (written by the team, collected from conversations, or contributed by invited speakers) from team-written English prompts, then cross-reviewed by someone other than its contributor (`docs/SOURCE_LOG.md`).
- Changes from v1 to v1.1 are listed row by row in `logs/v1.1_change_log.csv`. The original v1 file is unchanged in `data/v1/`.

## Run it

Python 3.10–3.13.

```bash
git clone https://github.com/Craggy-sense/KikuyuSent.git && cd KikuyuSent
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python validate.py                       # official kit validator + team checks
python experiments/compare_on_dev.py     # model comparison on dev (never test)
python train.py                          # trains SELECTED_MODEL from pipeline.py
python evaluate.py dev
python evaluate.py test --final          # test is guarded and every run is logged
python -m streamlit run app.py           # demo
python predict.py "Ndĩmũkenu mũno"       # one-off prediction
```

To rebuild the dataset from v1 plus the reviewer decisions: `python tools/prepare_dataset.py`.

Improved model v2 (already run; the held-out step refuses to run twice):
```bash
python tools/prepare_supplementary.py          # 60 supplementary sentences -> kit schema
python experiments/train_experimental.py       # setup E on train+dev (240)
python experiments/evaluate_heldout.py --final # one-time fresh evaluation (official vs improved)
python experiments/train_final_v2.py           # setup E on all 360 -> models/kikuyusent_v2.joblib
```

## Repository map

| Path | What it is |
|---|---|
| `data/kikuyu_dataset.csv` | v1.1 dataset (used by everything) |
| `data/v1/` | Original v1 data, frozen |
| `data/supplementary/` | 60 supplementary sentences (KIK-301…360), the fresh held-out set, then used to train v2 |
| `data/provenance_map.csv` | Author, reviewer and method per record range |
| `review/v1.1_checks.csv` | Fluent-speaker decisions on the 11 rows flagged after v1 (all kept) |
| `logs/v1.1_change_log.csv` · `logs/test_runs.csv` | Every data change · every test evaluation |
| `pipeline.py` | Shared data loading, model definitions, `SELECTED_MODEL` |
| `validate.py` · `kit/` | Team validator wrapping the official starter-kit validator |
| `experiments/compare_on_dev.py` | Dev-only model comparison |
| `train.py` · `evaluate.py` · `predict.py` · `app.py` | Train · evaluate · CLI · Streamlit demo |
| `models/` | `sentiment_model.joblib` + `model_info.json` (data and model hashes); `models/v1/` archived |
| `results/` | Metrics JSON, per-label reports, confusion matrices, predictions; `results/v1/` archived |
| `docs/` | Dataset card, source log, annotation guide, quality report, contributions, AI use |
| `tools/` | Dataset preparation and submission packaging |

## Demo

The 2–3 minute demo video is submitted with the entry through the NLP Hub channel. The app shows live predictions with label probabilities, the test scores against the always-one-label floor, and real test examples in two tabs: correct predictions and real failures.

## Team

Robi Memusi · Patriciah Mbua · Mariam Abdi, with Kikuyu-speaking contributors and outside reviewers. Roles are in `docs/CONTRIBUTIONS.md`, and AI assistance is described in `docs/AI_USE_STATEMENT.md`.

## Reuse, licences and data release

- **Reused:** starter kit v2 code (`kit/`, licence in `kit/LICENSE_CODE.txt`); our scripts adapt its structure. No external dataset was used; all 360 sentences are new contributions.
- **Team code:** shared for datathon assessment under the starter kit's terms.
- **Data release:** contributors agreed to use for the submission and assessment. Wider public release is a pending decision with the NLP Hub.

## Data use and ethics

Sentences are original contributions used with documented contributor consent; contributor identities and consent forms are kept privately. The model is an experimental prototype and must not be used for decisions about people.

Code builds on the Strathmore NLP Hub Datathon starter kit (`kit/`, see `kit/LICENSE_CODE.txt`).
