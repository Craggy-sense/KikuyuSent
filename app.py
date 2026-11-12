"""KikuyuSent demo. Run: python -m streamlit run app.py"""
import json
import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))  # the experimental model uses experiments/kikuyu_text.py
MODEL_PATH = ROOT / 'models' / 'sentiment_model.joblib'
EXP_PATH = ROOT / 'models' / 'kikuyusent_v2.joblib'
HELDOUT = ROOT / 'results' / 'heldout' / 'heldout_metrics.json'
METRICS = ROOT / 'results' / 'test_metrics.json'
PREDICTIONS = ROOT / 'results' / 'test_predictions.csv'
# The 5 real test errors analysed in docs/QUALITY_REPORT.md
WHY = {
    'KIK-NEU-024': 'Intensifier shortcut: "mũno" (very) appears only in positive/negative training sentences, mostly positive.',
    'KIK-PILOT-007': 'Negation: "itarĩ njega" means "not good", but the model only sees "njega" (good).',
    'KIK-POS-205': 'A training sentence shares 5 of these 6 words but means "arrived damaged" (negative).',
    'KIK-NEG-062': 'Same frame as a positive training sentence ("Rũgendo rũu rwarĩ … mũno"); the negative words are unseen.',
    'KIK-NEG-278': 'Topic shortcut: "mũthenya" (day) appears only in neutral training sentences; "broke" is unseen.',
}
STYLE = {'positive': ('😊', 'Positive', st.success), 'negative': ('😟', 'Negative', st.error),
         'neutral': ('😐', 'Neutral', st.info)}

st.set_page_config(page_title='KikuyuSent | Team Zeus', page_icon='💬', layout='centered')
st.title('💬 KikuyuSent')
st.caption('**Team 5 (Zeus)** · Working language: **Kikuyu (Gĩkũyũ)** · Track B: sentiment · Status: **prototype**')
st.subheader('Kikuyu (Gĩkũyũ) sentence sentiment: positive, negative or neutral')

if not MODEL_PATH.exists():
    st.error('Trained model not found. Run `python train.py` first.')
    st.stop()


@st.cache_resource
def load_model(path):
    return joblib.load(path)


OFFICIAL = 'Official model (submitted)'
EXPERIMENTAL = 'Improved model v2 (Kikuyu-aware)'
choice = OFFICIAL
if EXP_PATH.exists():
    choice = st.sidebar.radio('Model', [EXPERIMENTAL, OFFICIAL])
    if HELDOUT.exists():
        h = json.loads(HELDOUT.read_text(encoding='utf-8'))
        st.sidebar.markdown('**Fresh held-out test** (60 new sentences, scored once)')
        st.sidebar.table(pd.DataFrame({
            'accuracy': [f"{h['experimental']['accuracy']:.1%}", f"{h['official']['accuracy']:.1%}"],
            'macro-F1': [f"{h['experimental']['macro_f1']:.3f}", f"{h['official']['macro_f1']:.3f}"]},
            index=['Improved setup', 'Official']))
    st.sidebar.caption('**Improved v2:** fluent-speaker vowel/spelling standardisation + negation marking '
                       '(e.g. *itarĩ njega* = "not good"). Its setup was trained on 240 sentences and scored once on '
                       '60 fresh ones; the demo model is then retrained on all 360.')
    st.sidebar.caption('**Official:** the submitted model (180 training sentences), test 66.7% / macro-F1 0.664.')
model = load_model(EXP_PATH if choice == EXPERIMENTAL else MODEL_PATH)

if METRICS.exists():
    m = json.loads(METRICS.read_text(encoding='utf-8'))
    c1, c2, c3 = st.columns(3)
    c1.metric('Official test accuracy', f"{m['accuracy']:.1%}")
    c2.metric('Official test macro-F1', f"{m['macro_f1']:.3f}")
    c3.metric('Always-one-label macro-F1', f"{m['majority_baseline']['macro_f1']:.3f}")
    st.caption(f"{m['correct']} of {m['records']} held-out test sentences correct · model: {m['model']}")
st.warning('Experimental prototype trained on human-produced, cross-reviewed Kikuyu sentences. '
           'Predictions can be wrong and are not verified interpretations of Kikuyu.')


SUMMARY = {'positive': 'The writer sounds pleased or approving.',
           'negative': 'The writer sounds unhappy, critical or upset.',
           'neutral': 'The sentence states a fact without a clear opinion.'}


def show(pred, conf=None):
    icon, name, box = STYLE.get(pred, ('💬', str(pred).title(), st.info))
    extra = f' (model score {conf:.0%}, uncalibrated)' if conf is not None else ''
    box(f'{icon} **{name}**{extra}  \n{SUMMARY.get(pred, "")}')


st.markdown('### Try a sentence')
text = st.text_area('Kikuyu text', placeholder='Andika Gĩkũyũ haha…', height=110)
if st.button('Analyse sentiment', type='primary', use_container_width=True):
    if not text.strip():
        st.warning('Please enter a Kikuyu sentence first.')
    else:
        pred = model.predict([text.strip()])[0]
        proba = model.predict_proba([text.strip()])[0] if hasattr(model, 'predict_proba') else None
        show(pred, None if proba is None else float(max(proba)))
        st.caption(f'Model: {choice}. Sentiment of the sentence only: not emotion detection or a measure of '
                   "anyone's mental state. The model always picks one of the three labels, even for text it "
                   'cannot handle (e.g. English or very long sentences).')
        if proba is not None:
            st.caption('Model scores per label (uncalibrated: not true probabilities)')
            st.bar_chart(pd.Series(proba, index=model.classes_, name='uncalibrated score'))

with st.expander('📊 Dataset contribution and evaluation summary'):
    st.markdown(
        '- **360 new Kikuyu sentences** produced by people (written by the team, collected from conversations, '
        'or contributed by invited speakers) and cross-reviewed by someone other than the contributor.\n'
        '- **Main set (300):** 100 positive · 100 negative · 100 neutral; train 180 / dev 60 / test 60. '
        'Passes the official starter-kit validator.\n'
        '- **Supplementary set (60):** 20 per label, approved by two speakers. Used once as a fresh '
        'held-out test, then to train model v2.\n'
        '- **Official model:** test accuracy 66.7%, macro-F1 0.664 (always-one-label: 0.167).\n'
        '- **Improved setup:** 70.0% / 0.699 on the 60 fresh sentences vs 66.7% / 0.671 for the official model.\n'
        '- Full details: `docs/QUALITY_REPORT.md`, `results/`, `docs/DATASET_CARD.md`.')

if PREDICTIONS.exists():
    p = pd.read_csv(PREDICTIONS, dtype=str, keep_default_na=False)
    p['correct'] = p.label == p.prediction
    st.divider()
    st.markdown('### Held-out test examples')
    st.caption('Official model on real sentences from the test split, never seen in training. '
               'Shows what works and what does not.')
    ok = pd.concat([p[p.correct & (p.label == l)].head(1) for l in ['positive', 'negative', 'neutral']])
    bad = p[p.record_id.isin(WHY)].set_index('record_id').loc[list(WHY)].reset_index()
    tab1, tab2, tab3 = st.tabs(['✅ Correct predictions', '❌ Real failures', '🚫 Unsupported input'])
    with tab3:
        st.markdown('The model only knows Kikuyu sentences like those in its training data. '
                    'It still forces one of the three labels for anything else:')
        for ex in ['The weather is nice today.', '12345', 'Habari yako?']:
            st.write(f'`{ex}` → model says **{model.predict([ex])[0]}** (meaningless: unsupported input)')
    for tab, rows in ((tab1, ok), (tab2, bad)):
        with tab:
            for _, r in rows.iterrows():
                st.markdown(f"**{r.text}**  \n_{r.english_prompt}_")
                st.write(f'Human label: `{r.label}` · Model: `{r.prediction}`')
                if r.record_id in WHY:
                    st.caption('Why: ' + WHY[r.record_id])
                st.divider()

st.caption('Team Zeus · Strathmore NLP Hub Datathon 2026 · Track B: Sentiment')
