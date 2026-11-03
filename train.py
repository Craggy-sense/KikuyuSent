from pathlib import Path
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

DATA_PATH = Path("data/contribution.csv")
MODEL_PATH = Path("models/sentiment_model.joblib")

def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, dtype=str).fillna("")

    required = {"text", "label", "consent", "review_status", "split"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")

    # Train only on accepted, consent-confirmed training records.
    df["label"] = df["label"].str.strip().str.lower()
    df["split"] = df["split"].str.strip().str.lower()

    train = df[
        (df["split"] == "train")
        & (df["consent"].str.strip().str.lower() == "yes")
        & (df["review_status"].str.strip().str.lower() == "accepted")
        & (df["text"].str.strip() != "")
        & (df["label"].isin(["positive", "negative", "neutral"]))
    ].copy()

    if train.empty:
        raise SystemExit("No eligible training records found.")

    if train["label"].nunique() < 2:
        raise SystemExit(
            "Need at least two sentiment classes to train. "
            "Add more reviewed training records."
        )

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
    print("Training label counts:")
    print(train["label"].value_counts().to_string())
    print(f"\nModel saved to: {MODEL_PATH}")
    print("This is a baseline model, not evidence of good performance.")

if __name__ == "__main__":
    main()
