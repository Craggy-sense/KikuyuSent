# KikuyuSent: Kikuyu Sentence Sentiment

**Strathmore NLP Hub Datathon 2026 · Team 5 "Zeus" · Track B (sentiment) · Kikuyu (Gĩkũyũ), `ki-KE`**

KikuyuSent classifies a Kikuyu sentence as **positive**, **negative** or **neutral**. We built a new, human-written, independently reviewed dataset of 300 Kikuyu sentences, trained a transparent baseline, and demonstrate it in Streamlit.

## Results (dataset v1.1, held-out test, evaluated once)

| Model | Test accuracy | Test macro-F1 |
|---|---|---|
| Word + character TF-IDF + Logistic Regression | `[TO FILL]` | `[TO FILL]` |
| Always one label (reference floor) | 0.333 | 0.167 |

Per-label F1 · positive `[TO FILL]` · negative `[TO FILL]` · neutral `[TO FILL]`.
The model was chosen on dev only (`results/dev_model_comparison.csv`). The archived v1 result was accuracy 0.667 / macro-F1 0.664 (`results/v1/`). Both test runs are logged in `logs/test_runs.csv`.

## Dataset

| | positive | negative | neutral | total |
|---|---|---|---|---|
| train | 60 | 60 | 60 | 180 |
| dev | 20 | 20 | 20 | 60 |
| test | 20 | 20 | 20 | 60 |

- `data/kikuyu_dataset.csv`: starter-kit schema, **passes the official kit validator**.
- Every sentence was written by a person and independently reviewed by a second fluent speaker (`docs/SOURCE_LOG.md`).
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

## Repository map

| Path | What it is |
|---|---|
| `data/kikuyu_dataset.csv` | v1.1 dataset (used by everything) |
| `data/v1/` | Original v1 data, frozen |
| `data/provenance_map.csv` | Author, reviewer and method per record range |
| `review/v1.1_checks.csv` | Reviewer decisions on the 11 rows flagged after v1 |
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

`[TO FILL: link to 2–3 minute demo video]`. The app shows live predictions with label probabilities, the test scores against the always-one-label floor, and real test examples in two tabs: correct predictions and real failures.

## Team

Robi Memusi · Patriciah Mbua · Mariam Abdi, with an independent fluent Kikuyu reviewer (T05-E1). Roles are in `docs/CONTRIBUTIONS.md`, and AI assistance is described in `docs/AI_USE_STATEMENT.md`.

## Data use and ethics

Sentences are original contributions used with documented contributor consent; contributor identities and consent forms are kept privately. The model is an experimental prototype and must not be used for decisions about people.

Code builds on the Strathmore NLP Hub Datathon starter kit (`kit/`, see `kit/LICENSE_CODE.txt`).
