# KikuyuSent Dataset Quality Report

## 1. Dataset Summary

The KikuyuSent dataset contains 300 Kikuyu text examples for three-class sentiment classification.

| Sentiment | Records |
|---|---:|
| Positive | 100 |
| Negative | 100 |
| Neutral | 100 |
| Total | 300 |

## 2. Dataset Distribution

| Split | Records |
|---|---:|
| Training | 180 |
| Development | 60 |
| Test | 60 |
| Total | 300 |

Each split contains 20 records from each sentiment class.

## 3. Validation Checks

The dataset validation script checks:

- Required columns are present.
- Labels belong to the supported sentiment classes.
- Dataset splits are valid.
- Required fields are not blank.
- Record identifiers are unique.
- Kikuyu text records are not duplicated.
- Expected dataset size and class distribution are maintained.
- Review status is recorded for all 300 examples.

The validation script previously completed successfully.

## 4. Independent Review

All 300 records have the review status:

`independently_reviewed_second_speaker_confirmed`

The team confirmed that the second Kikuyu speaker independently reviewed the records.

Five representative model errors from the held-out test set were also individually checked with a Kikuyu reviewer. The reviewer confirmed that the original sentences and labels were correct. These examples were retained.

## 5. Model Evaluation

The selected word-and-character TF-IDF Logistic Regression model achieved:

| Metric | Test result |
|---|---:|
| Accuracy | 66.67% |
| Macro F1-score | 0.6639 |
| Correct predictions | 40 out of 60 |

### Class-level F1 scores

| Class | F1-score |
|---|---:|
| Positive | 0.65 |
| Negative | 0.54 |
| Neutral | 0.80 |

## 6. Error Analysis

The selected model made 20 incorrect predictions out of 60 test examples.

Five representative errors were independently reviewed by a Kikuyu speaker. The reviewer confirmed that the original labels and sentences were correct.

The errors included:

- Negative sentences classified as positive.
- Positive sentences classified as negative.
- Neutral sentences classified as positive or negative.

These results suggest that the model still struggles with sentiment polarity and contextual interpretation.

The original reviewed labels were retained.

## 7. Limitations

- The dataset is relatively small.
- Sentiment can depend on context and cultural meaning.
- TF-IDF features do not fully capture linguistic context.
- Positive and negative sentiment remain more difficult to distinguish than neutral sentiment.

## 8. Conclusion

The dataset passed the implemented structural and distribution validation checks. Independent second-speaker review was recorded for all 300 examples.

The selected baseline provides a reproducible starting point, but further data collection and model improvements are necessary.
