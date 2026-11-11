from pathlib import Path

import joblib
import streamlit as st

MODEL_PATH = Path("models/sentiment_model.joblib")

st.set_page_config(
    page_title="KikuyuSent | Team Zeus",
    page_icon="💬",
    layout="centered"
)

st.title("💬 KikuyuSent")
st.subheader("Kikuyu Language Sentiment Analyser")

st.write(
    "Enter a sentence in Kikuyu (Gĩkũyũ) to analyse "
    "whether its expressed sentiment is positive, negative or neutral."
)

st.info(
    "Experimental research prototype trained on 180 independently "
    "reviewed Kikuyu records. Held-out test accuracy: 66.67%; "
    "macro-F1: 0.6639 (60 test records)."
)

st.warning(
    "Predictions are machine-generated and may be incorrect. "
    "They should not be treated as verified interpretations "
    "of Kikuyu language or meaning."
)

if not MODEL_PATH.exists():
    st.error(
        "Trained model not found. Run `python train.py` "
        "from the project directory first."
    )
    st.stop()


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


try:
    model = load_model()
except Exception as error:
    st.error(f"Could not load the trained model: {error}")
    st.stop()


st.markdown("### Analyse a sentence")

user_text = st.text_area(
    "Kikuyu text",
    placeholder="Andika gĩkũyũ haha...",
    height=150,
    help="Enter the Kikuyu sentence you want to analyse."
)

analyse = st.button(
    "Analyse sentiment",
    type="primary",
    use_container_width=True
)

if analyse:
    if not user_text.strip():
        st.warning("Please enter a Kikuyu sentence first.")
    else:
        try:
            prediction = model.predict([user_text.strip()])[0]

            labels = {
                "positive": ("😊", "Positive"),
                "negative": ("😟", "Negative"),
                "neutral": ("😐", "Neutral")
            }

            icon, sentiment = labels.get(
                prediction,
                ("💬", str(prediction).title())
            )

            st.markdown("### Analysis result")

            if prediction == "positive":
                st.success(f"{icon} {sentiment} sentiment")
            elif prediction == "negative":
                st.error(f"{icon} {sentiment} sentiment")
            else:
                st.info(f"{icon} {sentiment} sentiment")

            st.caption(
                "This result is a model prediction, not a "
                "human-verified interpretation."
            )

        except Exception as error:
            st.error(f"Prediction failed: {error}")


st.divider()

st.markdown("### About KikuyuSent")

st.write(
    "KikuyuSent is a Team Zeus project developed for the "
    "Strathmore NLP Hub Datathon 2026, Track B: Sentiment Analysis."
)

st.write(
    "The system uses word-level and character-level TF-IDF "
    "features with Logistic Regression to classify Kikuyu text."
)

st.caption(
    "Team Zeus | Strathmore NLP Hub Datathon 2026"
)
