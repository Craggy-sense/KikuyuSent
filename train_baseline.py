
from pathlib import Path

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

DATA_PATH = Path("data/kikuyu_dataset.csv")
MODEL_PATH = Path("models/sentiment_model.joblib")

VALID_LABELS = {"positive", "negative", "neutral"}


def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, dtype=str).fillna("")

    required = {"text", "label", "review_status", "split"}
    missing = required - set(df.columns)

    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")

    df["label"] = df["label"].str.strip().str.lower()
    df["split"] = df["split"].str.strip().str.lower()
    df["text"] = df["text"].str.strip()

    eligible = df[
        (df["review_status"] ==
         "independently_reviewed_second_speaker_confirmed")
        & (df["text"] != "")
        & (df["label"].isin(VALID_LABELS))
    ]

    train = eligible[eligible["split"] == "train"].copy()

    if len(train) != 180:
        raise SystemExit(
            f"Expected 180 eligible training records; found {len(train)}."
        )

    if train["label"].nunique() != 3:
        raise SystemExit("Training data must contain all three labels.")

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 5),
            lowercase=True,
            sublinear_tf=True
        )),
        ("classifier", LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42
        ))
    ])

    model.fit(train["text"], train["label"])

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Training records used: {len(train)}")
    print("\nTraining label counts:")
    print(train["label"].value_counts().to_string())
    print(f"\nModel saved to: {MODEL_PATH}")
    print("Baseline training completed successfully.")


if __name__ == "__main__":
    main()

