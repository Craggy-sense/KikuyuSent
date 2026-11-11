import os
import joblib
import pandas as pd

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

DATA_PATH = "data/kikuyu_dataset.csv"
MODEL_PATH = "models/sentiment_model.joblib"

REVIEW_STATUS = "independently_reviewed_second_speaker_confirmed"

df = pd.read_csv(DATA_PATH)

required_columns = ["text", "label", "review_status", "split"]
missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

train_df = df[
    (df["split"] == "train") &
    (df["review_status"] == REVIEW_STATUS)
].copy()

train_df = train_df.dropna(subset=["text", "label"])

if len(train_df) != 180:
    raise ValueError(
        f"Expected 180 reviewed training records, found {len(train_df)}"
    )

X_train = train_df["text"].astype(str)
y_train = train_df["label"].astype(str)

expected_labels = {"positive", "negative", "neutral"}

if set(y_train.unique()) != expected_labels:
    raise ValueError("Training data must contain all three sentiment labels.")

features = FeatureUnion([
    (
        "word_tfidf",
        TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "char_tfidf",
        TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5),
            sublinear_tf=True
        )
    )
])

model = Pipeline([
    ("features", features),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42
        )
    )
])

model.fit(X_train, y_train)

os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"Training records used: {len(train_df)}")
print("\nTraining label counts:")
print(y_train.value_counts())
print(f"\nModel saved to: {MODEL_PATH}")
print("Word + character TF-IDF training completed successfully.")
