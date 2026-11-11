# KikuyuSent Dataset Card

## Dataset Overview

KikuyuSent is a sentiment-analysis dataset developed by Team Zeus for the Strathmore NLP Hub Datathon 2026, Track B.

The dataset contains 300 original Kikuyu (Gĩkũyũ) text examples labelled according to sentiment.

## Intended Task

Three-class sentiment classification:

- Positive
- Negative
- Neutral

## Dataset Composition

| Sentiment | Records |
|---|---:|
| Positive | 100 |
| Negative | 100 |
| Neutral | 100 |
| Total | 300 |

## Data Collection

The dataset was collected using a combination of methods. The precise breakdown of collection methods and sources should be maintained in the source log.

The examples are original contributions and are not simply unchanged starter-kit examples.

## Review and Quality Assurance

All 300 records were independently reviewed by a second Kikuyu speaker.

The review status recorded in the dataset is:

`independently_reviewed_second_speaker_confirmed`

## Dataset Splits

| Split | Records |
|---|---:|
| Train | 180 |
| Development | 60 |
| Test | 60 |
| Total | 300 |

Each split contains 20 examples from each sentiment class.

## Fields

| Field | Description |
|---|---|
| record_id | Unique record identifier |
| text | Original Kikuyu text |
| label | Sentiment label |
| english_prompt | English meaning or corresponding prompt |
| review_status | Review status |
| reviewer_code | Reviewer identifier, where recorded |
| review_note | Review notes, where recorded |
| split | Train, development or test partition |

## Intended Uses

- Kikuyu sentiment-analysis research.
- Baseline natural-language-processing experiments.
- Educational demonstrations.
- Further development of low-resource language technology.

## Limitations

- The dataset contains only 300 examples.
- It may not represent all Kikuyu dialects, speakers, writing styles or contexts.
- Sentiment can depend on cultural and conversational context.
- Model predictions should not be treated as definitive interpretations.

## Ethics and Data Use

Dataset sharing must follow the permissions and conditions under which the examples were collected.

Private contributor information and identifying details should not be published.

## Version

Initial datathon dataset: 300 records.
