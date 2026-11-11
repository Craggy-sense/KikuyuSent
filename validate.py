
import sys
import pandas as pd

VALID_LABELS = {"positive", "negative", "neutral"}
VALID_SPLITS = {"train", "dev", "test"}

REQUIRED_COLUMNS = {
    "record_id",
    "text",
    "label",
    "english_prompt",
    "review_status",
    "split"
}

EXPECTED_COUNTS = {
    "train": 180,
    "dev": 60,
    "test": 60
}

CONFIRMED_REVIEW_STATUS = (
    "independently_reviewed_second_speaker_confirmed"
)


def validate_dataset(path):
    df = pd.read_csv(path, dtype=str).fillna("")
    errors = []

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        print("Missing columns:", ", ".join(sorted(missing)))
        return 1

    for col in ["record_id", "text", "label", "review_status", "split"]:
        blank = df[col].str.strip().eq("")
        if blank.any():
            errors.append(f"{col}: {int(blank.sum())} blank values")

    if df["record_id"].duplicated().any():
        errors.append("Duplicate record IDs found")

    if df["text"].str.strip().duplicated().any():
        errors.append("Duplicate Kikuyu texts found")

    labels = df["label"].str.strip().str.lower()
    splits = df["split"].str.strip().str.lower()

    if not set(labels).issubset(VALID_LABELS):
        errors.append("Invalid sentiment labels found")

    if not set(splits).issubset(VALID_SPLITS):
        errors.append("Invalid split names found")

    if not (df["review_status"].str.strip() ==
            CONFIRMED_REVIEW_STATUS).all():
        errors.append("Some records lack confirmed second-speaker review")

    if len(df) != 300:
        errors.append(f"Expected 300 records; found {len(df)}")

    if set(labels) != VALID_LABELS:
        errors.append("Dataset must contain all three sentiment classes")

    print(f"\nDataset: {path}")
    print(f"Total records: {len(df)}")

    print("\nSentiment counts:")
    print(labels.value_counts().to_string())

    print("\nSplit counts:")
    print(splits.value_counts().to_string())

    print("\nSentiment distribution by split:")
    print(pd.crosstab(splits, labels).to_string())

    for split, expected in EXPECTED_COUNTS.items():
        actual = int((splits == split).sum())
        if actual != expected:
            errors.append(
                f"{split}: expected {expected}, found {actual}"
            )

    if errors:
        print("\nVALIDATION ISSUES:")
        for error in errors:
            print("-", error)
        return 1

    print("\nBasic dataset validation passed.")
    print("Second-speaker review status confirmed for all records.")
    print("Consent and source provenance should be documented separately.")

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate.py data/kikuyu_dataset.csv")
        sys.exit(2)

    sys.exit(validate_dataset(sys.argv[1]))
