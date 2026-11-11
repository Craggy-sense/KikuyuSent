# KikuyuSent Annotation Guide

## Purpose

This guide describes the sentiment labels used in the KikuyuSent dataset.

## Sentiment Labels

### Positive

Use `positive` when the text expresses a favourable, happy, approving, grateful or otherwise positive sentiment.

### Negative

Use `negative` when the text expresses dissatisfaction, anger, sadness, disappointment, criticism or another unfavourable sentiment.

### Neutral

Use `neutral` when the text is primarily factual, descriptive or informational and does not clearly express positive or negative sentiment.

## Annotation Principles

1. Interpret the Kikuyu sentence in its linguistic and cultural context.
2. Do not assign sentiment based only on individual words.
3. Consider the overall meaning of the sentence.
4. Do not assume that every statement about an event expresses an emotion.
5. Preserve the original Kikuyu text.
6. Do not change an independently reviewed label without a documented review.

## Independent Review

The dataset records that all 300 examples were independently reviewed by a second Kikuyu speaker.

The review status used is:

`independently_reviewed_second_speaker_confirmed`

## Dataset Structure

Each record contains:

- record_id
- text
- label
- english_prompt
- review_status
- reviewer_code
- review_note
- split

## Quality Considerations

Kikuyu expressions may have meanings that are not directly captured by literal English translations. Reviewers should consider the intended meaning rather than relying exclusively on the English prompt.

Ambiguous examples should be flagged for further human review rather than assigned a label without justification.
