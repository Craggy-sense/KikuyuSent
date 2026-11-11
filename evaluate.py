from pathlib import Path
import sys
import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)

DATA_PATH = Path("data/kikuyu_dataset.csv")
MODEL_PATH = Path("models/sentiment_model.joblib")
RESULTS_DIR = Path("results")

LABELS = ["positive", "negative", "neutral"]
REVIEW_STATUS = "independently_reviewed_second_speaker_confirmed"


def main():
    split = sys.argv[1].lower() if len(sys.argv) > 1 else "dev"

    if split not in {"dev", "test"}:
        raise SystemExit("Usage: python evaluate.py [dev|test]")

    if not MODEL_PATH.exists():
        raise SystemExit("Model not found. Run python train.py first.")

    df = pd.read_csv(DATA_PATH, dtype=str).fillna("")

    eligible = df[
        (df["split"].str.strip().str.lower() == split)
        & (df["review_status"].str.strip() == REVIEW_STATUS)
        & (df["text"].str.strip() != "")
        & (df["label"].str.strip().str.lower().isin(LABELS))
    ].copy()

    if len(eligible) != 60:
        raise SystemExit(
            f"Expected 60 eligible {split} records; found {len(eligible)}."
        )

    if split == "test":
        test_counts = eligible["label"].str.strip().str.lower().value_counts()
        for label in LABELS:
            if test_counts.get(label, 0) != 20:
                raise SystemExit(
                    f"Expected 20 {label} test records; "
                    f"found {test_counts.get(label, 0)}."
                )

    model = joblib.load(MODEL_PATH)
    y_true = eligible["label"].str.strip().str.lower()
    predictions = model.predict(eligible["text"])

    accuracy = accuracy_score(y_true, predictions)
    macro_f1 = f1_score(
        y_true, predictions, labels=LABELS,
        average="macro", zero_division=0
    )

    print(f"\nEvaluation split: {split}")
    print(f"Records evaluated: {len(eligible)}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro-F1: {macro_f1:.4f}")

    print("\nClassification report:")
    print(classification_report(
        y_true, predictions, labels=LABELS, zero_division=0
    ))

    print("Confusion matrix (rows=actual, columns=predicted):")
    print(confusion_matrix(y_true, predictions, labels=LABELS))

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output = eligible[["record_id", "text", "label"]].copy()
    output["prediction"] = predictions
    output.to_csv(
        RESULTS_DIR / f"{split}_predictions.csv",
        index=False, encoding="utf-8-sig"
    )

    print(f"\nPredictions saved to results/{split}_predictions.csv")


if __name__ == "__main__":
    main()
