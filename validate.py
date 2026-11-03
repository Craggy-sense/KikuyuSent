import sys
import pandas as pd

VALID_LABELS = {"positive", "negative", "neutral"}
VALID_SPLITS = {"train", "dev", "test"}
REQUIRED_COLUMNS = {
    "record_id", "text", "label", "source_type",
    "consent", "review_status", "split"
}

def validate_dataset(path):
    df = pd.read_csv(path, dtype=str).fillna("")
    errors = []

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        print("Missing columns:", ", ".join(sorted(missing_columns)))
        return 1

    for col in ["record_id", "text", "label", "consent",
                "review_status", "split"]:
        blank = df[col].str.strip().eq("")
        if blank.any():
            errors.append(f"{col}: {int(blank.sum())} blank value(s)")

    if df["record_id"].duplicated().any():
        errors.append("Duplicate record_id values found")

    if df["text"].str.strip().duplicated().any():
        errors.append("Duplicate text values found; review possible duplicates")

    invalid_labels = set(df["label"].str.strip().str.lower()) - VALID_LABELS
    if invalid_labels:
        errors.append(f"Invalid labels: {sorted(invalid_labels)}")

    invalid_splits = set(df["split"].str.strip().str.lower()) - VALID_SPLITS
    if invalid_splits:
        errors.append(f"Invalid splits: {sorted(invalid_splits)}")

    if (df["consent"].str.strip().str.lower() != "yes").any():
        errors.append("Some records lack confirmed consent")

    if (df["review_status"].str.strip().str.lower() != "accepted").any():
        errors.append("Some records have not been accepted by reviewers")

    print(f"\nFile: {path}")
    print(f"Total records: {len(df)}")
    print("\nLabel counts:")
    print(df["label"].value_counts().to_string())
    print("\nSplit counts:")
    print(df["split"].value_counts().to_string())

    if errors:
        print("\nVALIDATION ISSUES:")
        for error in errors:
            print(f"- {error}")
        print("\nPlease review these issues before training.")
        return 1

    print("\nBasic validation passed.")
    print("This does not replace human translation, consent, or quality review.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate.py data/contribution.csv")
        sys.exit(2)
    sys.exit(validate_dataset(sys.argv[1]))
