from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)

DATA_PATH = Path("data/kikuyu_dataset.csv")
MODEL_PATH = Path("models/sentiment_model_svm.joblib")
OUTPUT_PATH = Path("results/dev_predictions_svm.csv")

LABELS = ["positive", "negative", "neutral"]
REVIEW_STATUS = "independently_reviewed_second_speaker_confirmed"

df = pd.read_csv(DATA_PATH, dtype=str).fillna("")

dev = df[
    (df["split"].str.strip().str.lower() == "dev")
    & (df["review_status"].str.strip() == REVIEW_STATUS)
    & (df["text"].str.strip() != "")
    & (df["label"].str.strip().str.lower().isin(LABELS))
].copy()

if len(dev) != 60:
    raise SystemExit(f"Expected 60 dev records; found {len(dev)}")

model = joblib.load(MODEL_PATH)

y_true = dev["label"].str.strip().str.lower()
predictions = model.predict(dev["text"])

print("\nModel: Linear SVM")
print(f"Evaluation split: dev")
print(f"Records evaluated: {len(dev)}")
print(f"Accuracy: {accuracy_score(y_true, predictions):.4f}")
print(
    "Macro-F1: "
    f"{f1_score(y_true, predictions, labels=LABELS, average='macro', zero_division=0):.4f}"
)

print("\nClassification report:")
print(classification_report(
    y_true, predictions, labels=LABELS, zero_division=0
))

print("Confusion matrix:")
print(confusion_matrix(y_true, predictions, labels=LABELS))

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

output = dev[["record_id", "text", "label"]].copy()
output["prediction"] = predictions
output.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"\nPredictions saved to {OUTPUT_PATH}")
