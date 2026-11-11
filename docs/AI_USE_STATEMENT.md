# AI Use Statement

| Tool | Used for | Not used for |
|---|---|---|
| ChatGPT | Early Python scripts and debugging, first drafts of documentation and README. `[TO FILL: and/or drafting the English situation list in english_prompt? State yes or no.]` | Writing, translating or labelling Kikuyu sentences |
| Claude (Anthropic) | Project planning and workflow; repository review; v1.1 restructuring (starter-kit schema, `tools/prepare_dataset.py`, validator wrapper, dev-only model comparison, logged test evaluation, demo examples tab); documentation templates | Writing, translating or labelling Kikuyu sentences; reviewer decisions |

## What humans did

- Wrote every Kikuyu sentence: `[TO FILL: who]`.
- Assigned every label, and reviewed every sentence independently (T05-E1).
- Made all v1.1 decisions in `review/v1.1_checks.csv` (fluent speakers only).
- Wrote the error-analysis explanations in `docs/QUALITY_REPORT.md` §5.
- Checked and ran all AI-assisted code. Every reported number comes from an actual run (`results/*.json`, `logs/test_runs.csv`).

## Flags raised by AI review

During the v1.1 review, the assistant flagged possible label/meaning mismatches. Because it is not a fluent Kikuyu speaker, it did not change any text or label. Each flag was decided by the human reviewer.
