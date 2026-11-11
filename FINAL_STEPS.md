# Final steps before submission (Thu 12 Nov, deadline 11:00 p.m.)

Work top to bottom. Internal target: **submitted by 8:00 p.m.**

## 1. Reviewer session (Robi + reviewer, ~45 min)

Open `review/v1.1_checks.csv` in Google Sheets, or in Excel saved as **CSV UTF-8**. For each of the 11 rows, fill in:

| Column | What to write |
|---|---|
| `decision` | `keep` · `fix_label` · `fix_text` · `fix_english` · `replace_text` |
| `new_label` | Only for `fix_label` (or a new label for `replace_text`) |
| `new_text` | Only for `fix_text` / `replace_text` |
| `new_english` | A corrected English meaning, whenever the current one is wrong |
| `decided_by` | e.g. `T05-A+T05-E1` |
| `note` | One line on why |

- **KIK-POS-022 must be `replace_text`:** Robi writes a **new, different positive sentence** in her own words, and the reviewer checks it.
- **KIK-POS-130** needs its English meaning (`fix_english`).
- **KIK-NEG-230:** choose `Duka` or `Nduka` and remove the bracket (`fix_text`).
- **For the rest,** the reviewer reads the Kikuyu and decides. `keep` is fine if it is correct; just put the reason in `note`.

## 2. Confirm provenance (5 min)

Edit `data/provenance_map.csv`. Set the correct `contributor_code`, `reviewer_code`, `source_method` (`original_human` = written by people in their own words; `human_localised` = people translated given prompts into Kikuyu) and dates. Then set `confirmed=yes`.

## 3. Final run (~5 min)

```bash
python tools/prepare_dataset.py        # must end with "READY"
python validate.py                     # must say "Validation passed" with no notes
python experiments/compare_on_dev.py   # dev only; if a different model wins, change SELECTED_MODEL in pipeline.py
python train.py
python evaluate.py dev
python evaluate.py test --final        # ONCE. It is logged in logs/test_runs.csv
python -m streamlit run app.py         # check it opens
```

## 4. Fill in the docs (~30 min)

Replace every `[TO FILL]` in `docs/` and `README.md`. Use these files:

| Doc | Source of the numbers |
|---|---|
| Results tables | `results/test_metrics.json`, `results/dev_model_comparison.csv` |
| Error analysis | Pick 5 rows from `results/test_predictions.csv` where `correct` is False. Robi writes the "why". |
| Change summary | `logs/v1.1_change_log.csv` |

```bash
grep -rn "TO FILL" docs README.md     # should print nothing when done
```

## 5. Demo video (2–3 min)

Screen-record `streamlit run app.py`:
1. One sentence of what the project is.
2. Type 3 sentences that are predicted correctly.
3. Open the **Real failures** tab, show 2, and say why they fail.
4. Close on the test score vs the always-one-label score.

Save it as `demo.mp4` **outside** the repo, or upload it and paste the link in the README.

## 6. Freeze and submit

```bash
git add -A && git commit -m "Final v1.1 submission"
git push
bash tools/make_submission.sh          # tags submission-v1, prints the SHA, builds the ZIP + manifest
git push origin submission-v1
```

Submit through the official NLP Hub channel: the repo link, the full commit SHA, the ZIP, and the demo video.
**Make sure the organisers can open the repo.** It is private, so add them as collaborators or make it public if the rules allow.
