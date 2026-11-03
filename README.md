# KikuyuSent

**Team Zeus | Strathmore NLP Hub Datathon 2026**

A human-reviewed dataset and sentiment classifier for Kikuyu (Gĩkũyũ) text.

## Project status

Early prototype. The current baseline was trained on three temporary
examples and must not be treated as a validated sentiment classifier.

## Current components

- `validate.py` — basic dataset checks
- `train.py` — TF-IDF character n-gram and Logistic Regression baseline
- `predict.py` — command-line prediction
- `evaluate.py` — development-set evaluation
- `app.py` — Streamlit web demo

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas scikit-learn streamlit joblib

cd ~/KikuyuSent

cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.py[cod]
.DS_Store
.env
models/
results/
data/*.csv
