from pathlib import Path

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

DATA_PATH = Path("data/kikuyu_dataset.csv")
MODEL_PATH = Path("models/sentiment_model_svm.joblib")

REVIEW_STATUS = "independently_reviewed_second_speaker_confirmed"
LABELS = {"positive", "negative", "neutral"}

df = pd.read_csv(DATA_PATH, dtype=str).fillna("")

required = {"text", "label", "review_status", "split"}
missing = required - set(df.columns)

if missing:
    raise SystemExit(f"Missing columns: {sorted(missing)}")

train = df[
    (df["split"].str.strip().str.lower() == "train")
    & (df["review_status"].str.strip() == REVIEW_STATUS)
    & (df["text"].str.strip() != "")
    & (df["label"].str.strip().str.lower().isin(LABELS))
].copy()

if len(train) != 180:
    raise SystemExit(f"Expected 180 training records, found {len(train)}")

X = train["text"].str.strip()
y = train["label"].str.strip().str.lower()

features = FeatureUnion([
    (
        "word",
        TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "character",
        TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5),
            sublinear_tf=True
        )
    )
])

model = Pipeline([
    ("features", features),
    ("classifier", LinearSVC(
        class_weight="balanced",
        random_state=42
    ))
])

model.fit(X, y)

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"Training records used: {len(train)}")
print("\nTraining label counts:")
print(y.value_counts())
print(f"\nSVM model saved to: {MODEL_PATH}")
print("Linear SVM training completed successfully.")
