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

DATA_PATH = Path("data/contribution.csv")
MODEL_PATH = Path("models/sentiment_model.joblib")
RESULTS_DIR = Path("results")

def main():
    df = pd.read_csv(DATA_PATH, dtype=str).fillna("")

    required = {"text", "label", "consent", "review_status", "split"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")

    for col in ["label", "split", "consent", "review_status"]:
        df[col] = df[col].str.strip().str.lower()

    dev = df[
        (df["split"] == "dev")
        & (df["consent"] == "yes")
        & (df["review_status"] == "accepted")
        & (df["text"].str.strip() != "")
        & (df["label"].isin(["positive", "negative", "neutral"]))
    ].copy()

    if dev.empty:
        raise SystemExit(
            "No eligible development records found. "
            "Add independently reviewed records with split=dev. "
            "Do not copy training examples into dev."
        )

    model = joblib.load(MODEL_PATH)
    predictions = model.predict(dev["text"])

    accuracy = accuracy_score(dev["label"], predictions)
    macro_f1 = f1_score(
        dev["label"], predictions,
        labels=["positive", "negative", "neutral"],
        average="macro",
        zero_division=0
    )

    print(f"Development records evaluated: {len(dev)}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Macro-F1: {macro_f1:.3f}")
    print("\nPer-class report:")
    print(classification_report(
        dev["label"], predictions,
        labels=["positive", "negative", "neutral"],
        zero_division=0
    ))
    print("Confusion matrix (rows=actual, columns=predicted):")
    print(confusion_matrix(
        dev["label"], predictions,
        labels=["positive", "negative", "neutral"]
    ))

    RESULTS_DIR.mkdir(exist_ok=True)
    output = dev[["text", "label"]].copy()
    output["prediction"] = predictions
    output.to_csv(RESULTS_DIR / "dev_predictions.csv", index=False)
    print("\nPredictions saved to results/dev_predictions.csv")

if __name__ == "__main__":
    main()
