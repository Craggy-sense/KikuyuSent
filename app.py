import streamlit as st
import joblib
from pathlib import Path

MODEL_PATH = Path("models/sentiment_model.joblib")

st.set_page_config(
    page_title="KikuyuSent | Team Zeus",
    page_icon="💬",
    layout="centered"
)

st.title("KikuyuSent")
st.subheader("Kikuyu Text Sentiment Classifier")
st.write(
    "Enter a Kikuyu sentence to see the baseline model's "
    "predicted sentiment."
)

st.warning(
    "Experimental prototype: this model was trained on only three "
    "temporary examples. Its predictions are not reliable research results."
)

if not MODEL_PATH.exists():
    st.error("Model not found. Run `python train.py` first.")
    st.stop()

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

text = st.text_area(
    "Kikuyu text",
    placeholder="Andika gĩkũyũ haha...",
    height=130
)

if st.button("Analyse sentiment", type="primary"):
    if not text.strip():
        st.warning("Please enter a sentence first.")
    else:
        prediction = model.predict([text.strip()])[0]

        labels = {
            "positive": "😊 Positive",
            "negative": "😟 Negative",
            "neutral": "😐 Neutral"
        }

        st.markdown("### Prediction")
        st.success(labels.get(prediction, prediction))
        st.caption(
            "This is a model prediction, not a human-verified interpretation."
        )

st.divider()
st.caption("Team Zeus | Strathmore NLP Hub Datathon 2026")
