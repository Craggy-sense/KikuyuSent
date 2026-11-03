import joblib
import sys

MODEL_PATH = "models/sentiment_model.joblib"

model = joblib.load(MODEL_PATH)

if len(sys.argv) > 1:
    text = " ".join(sys.argv[1:]).strip()
else:
    text = input("Enter Kikuyu text: ").strip()

if not text:
    raise SystemExit("Please enter some text.")

prediction = model.predict([text])[0]

print(f"\nText: {text}")
print(f"Predicted sentiment: {prediction}")
print("\nNote: This is an experimental prediction, not a verified result.")
