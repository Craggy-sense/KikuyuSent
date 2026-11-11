# KikuyuSent – Kikuyu Language Sentiment Analysis

**Strathmore NLP Hub Datathon 2026 | Team Zeus | Track B**

KikuyuSent is a sentiment analysis project focused on classifying written Kikuyu (Gĩkũyũ) text into three sentiment categories:

- Positive
- Negative
- Neutral

The project aims to contribute to the development of language technology for underrepresented African languages.

## 1. Project Overview

KikuyuSent uses a machine-learning baseline to predict the sentiment expressed in a Kikuyu sentence.

The project includes:
- An independently collected and reviewed Kikuyu dataset.
- Dataset validation.
- TF-IDF feature extraction.
- Logistic Regression classification.
- Model evaluation.
- A Streamlit demonstration interface.

## 2. Dataset

The dataset contains 300 original Kikuyu examples.

| Category | Records |
|---|---:|
| Positive | 100 |
| Negative | 100 |
| Neutral | 100 |
| **Total** | **300** |

### Dataset split

| Split | Records |
|---|---:|
| Training | 180 |
| Development | 60 |
| Testing | 60 |
| **Total** | **300** |

Each sentiment category is balanced across the three splits.

The examples were independently reviewed by a second Kikuyu speaker.

The dataset uses the following fields:

- `record_id`: Unique record identifier.
- `text`: Original Kikuyu sentence.
- `label`: Sentiment classification.
- `english_prompt`: English meaning or corresponding prompt.
- `review_status`: Review status.
- `reviewer_code`: Reviewer identifier.
- `review_note`: Review notes.
- `split`: Dataset partition.

Refer to the documentation folder for the dataset card, annotation guide, source log and quality report.

## 3. Project Structure

```text
KikuyuSent/
│
├── app.py
├── validate.py
├── train.py
├── train_baseline.py
├── train_word_char.py
├── train_svm.py
├── evaluate.py
├── evaluate_svm.py
├── predict.py
├── requirements.txt
├── README.md
│
├── data/
│   └── kikuyu_dataset.csv
│
├── docs/
│   ├── DATASET_CARD.md
│   ├── ANNOTATION_GUIDE.md
│   ├── SOURCE_LOG.md
│   ├── QUALITY_REPORT.md
│   └── AI_USE_STATEMENT.md
│
├── models/
│   └── sentiment_model.joblib
│
└── results/
    └── test_predictions.csv
```

Some files may be added or updated as the project develops.

## 4. Technology Stack

- Python
- Pandas
- Scikit-learn
- TF-IDF
- Logistic Regression
- Linear SVM (experimental)
- Joblib
- Streamlit

## 5. Installation

Clone the repository:

```bash
git clone https://github.com/Craggy-sense/KikuyuSent.git
cd KikuyuSent
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 6. Running the Project

### Validate the dataset

```bash
python validate.py
```

### Train the selected Logistic Regression model

```bash
python train.py
```

### Evaluate on the development split

```bash
python evaluate.py dev
```

### Evaluate on the held-out test split

```bash
python evaluate.py test
```

### Launch the Streamlit application

```bash
streamlit run app.py
```

The application will provide an interface for entering Kikuyu sentences and viewing predicted sentiment.

## 7. Baseline Model Results

The selected word-and-character TF-IDF Logistic Regression model achieved the following results on the held-out test set:

| Metric | Result |
|---|---:|
| Accuracy | 66.67% |
| Macro F1-score | 0.6639 |
| Correct predictions | 40/60 |

### Class-level F1 scores

| Sentiment | F1-score |
|---|---:|
| Positive | 0.65 |
| Negative | 0.54 |
| Neutral | 0.80 |

The model is experimental. Its predictions are not always reliable, particularly where sentiment depends on context, expressions or linguistic nuance.

The test set has already been evaluated and should not be used for further model tuning.

## 8. Team Contributions

Team Zeus is developing KikuyuSent as part of the Strathmore NLP Hub Datathon 2026.

Contributions include:
- Kikuyu data collection and review.
- Dataset preparation and validation.
- Model development and evaluation.
- Application development.
- Documentation and reproducibility.

## 9. Reproducibility

Please use the documented dataset split and scripts when reproducing the reported results.

Do not modify independently reviewed labels or use the held-out test set for model tuning.

## 10. Data Use and Ethics

Use the dataset only in accordance with its documented permission and contribution conditions.

Do not publish private contributor information or identifying details.

Any new examples should have a documented source and appropriate permission before being added.

## 11. Current Status

KikuyuSent has a validated 300-record dataset, a trained baseline model, development and test evaluation scripts, and a Streamlit prototype.

Documentation, final repository organisation and demonstration preparation are ongoing.
