# KikuyuSent Dataset Card (v1.1)

## Summary

| | |
|---|---|
| Task | Three-class sentence-level sentiment: `positive` · `negative` · `neutral` |
| Language | Kikuyu (Gĩkũyũ), `ki-KE` · variety `[TO FILL]` |
| Size | 300 records: 100 per label |
| Splits | train 180 · dev 60 · test 60 (60/20/20 per label), group-safe |
| Source | Team-authored sentences, independently reviewed by a second fluent speaker (see `docs/SOURCE_LOG.md`) |
| Permission | Documented contributor consent (held privately) |
| File | `data/kikuyu_dataset.csv` (starter-kit schema; passes `kit/validate.py --track sentiment`) |
| Team | Team 5 "Zeus", Strathmore NLP Hub Datathon 2026 |

## Domain and labels

Short, everyday first-person or descriptive statements: feelings about events, people, services, products, food, travel and work, plus factual statements (times, places, quantities) for the neutral class.

| Label | Meaning | Example (Kikuyu → meaning) |
|---|---|---|
| positive | approval, happiness, gratitude, satisfaction | *Ndĩmũkenu mũno* → I am very happy |
| negative | dissatisfaction, anger, sadness, complaint | *Ndĩ mũrakaru mũno.* → I am very angry |
| neutral | factual or informational, no clear opinion | *Duka ĩrĩ hakuhĩ na benki.* → The shop is next to the bank |

**Deviation from the handbook's "one domain" advice:** the data covers general everyday statements rather than a single domain such as customer feedback. Models trained on it should be read as general-statement sentiment models, not domain-specific feedback models.

## Fields

The 15 starter-kit fields (`record_id`, `language`, `text`, `label`, `source_dataset`, `source_version`, `source_record_id`, `source_url`, `source_method`, `licence_or_permission`, `contributor_code`, `reviewer_code`, `review_status`, `group_id`, `split`), plus:

| Extra field | Meaning |
|---|---|
| `english_prompt` | English meaning or situation the sentence was written for (reference only, not a training feature) |
| `review_note` | Notes from review in v1 |
| `orthography` | How long vowels are marked: `tilde` (ĩ ũ), `acute` (í ú), `macron` (ī ū) or `plain` |
| `dataset_version` | `v1.1` |

## Characteristics

- Sentence length: 2–17 words (median 6).
- **Orthography varies,** as it does in real typing: 262 tilde, 17 acute, 14 macron, 7 plain. We kept the authors' spelling. A character-based model treats *ĩ*, *í*, *ī* and *i* as different characters, which may hurt rare spellings.
- Neutral sentences are mostly about times, places and objects, while positive and negative ones often contain feeling words (*-kenu* happy, *kĩeha* sadness, *-rakaru* angry). A model can partly learn these topic cues rather than sentiment.
- Record IDs contain the original intended label (`KIK-POS-…`). The model never sees IDs.

## Intended uses

Baseline research and teaching on Kikuyu sentiment; a seed for a larger, reviewed Kikuyu corpus.

## Not intended for

Judging real people or communities, moderation decisions, or any high-stakes automated decision. 300 sentences cannot represent all dialects, registers or speakers.

## Limitations and known issues

- Small size: 180 training sentences.
- `[TO FILL]` number of contributors and dialect coverage.
- The `english_prompt` is a guide, not an exact translation; a few English meanings were corrected in v1.1 (see `logs/v1.1_change_log.csv`).
- Sarcasm, mixed opinions and long multi-clause sentences are under-represented.

## Versions

| Version | Date | Notes |
|---|---|---|
| v1 | 11 Nov 2026 | First complete set; test evaluated once (accuracy 0.667, macro-F1 0.664), archived in `data/v1/`, `results/v1/` |
| v1.1 | 12 Nov 2026 | Starter-kit schema, provenance fields, reviewer-checked fixes, near-duplicate replaced, paraphrase pair kept in one split |
