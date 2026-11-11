# KikuyuSent Source Log

One source contributes records: **team-authored Kikuyu sentences** (`source_dataset = team_authored`, version `v1`). No external dataset, web text, social-media post or starter-kit practice row is included.

## Source summary

| Field | Value |
|---|---|
| Source dataset | `team_authored` |
| Source version | `v1` (collected 3–10 Nov 2026); cleaned into dataset **v1.1** on 12 Nov 2026 |
| Source URL | `not_applicable`: sentences were written for this project and were never published elsewhere |
| Source record ID | Same as `record_id` (`KIK-PILOT-001` … `KIK-NEU-300`) |
| Licence / permission | `documented_contributor_permission`: signed contributor consent, held privately by Team 5 (not in this repository) |
| Language | Kikuyu (Gĩkũyũ), `ki-KE` · variety: `[TO FILL: e.g. Kiambu / Murang'a / Nyeri]` |
| Records | 300 (100 positive, 100 negative, 100 neutral) |

## How the records were produced

| Record IDs | Count | Written by | Reviewed by | Method | Dates |
|---|---|---|---|---|---|
| `KIK-PILOT-001` – `KIK-PILOT-021` | 21 (7 per label) | `[TO FILL: T05-A]` | `[TO FILL: T05-E1]` | `[TO FILL]` | `[TO FILL]` |
| `KIK-POS-*`, `KIK-NEG-*`, `KIK-NEU-*` (`022`–`300`) | 279 (93 per label) | `[TO FILL]` | `[TO FILL]` | `[TO FILL]` | `[TO FILL]` |

**Method, in plain words:** `[TO FILL: describe exactly what happened. Example: "An English list of everyday sentiment situations was drafted (with ChatGPT / by the team). For each situation, Robi (T05-A) wrote a Kikuyu sentence in her own words; no machine translation was used. The english_prompt column keeps the English situation for reference." Be precise: this is the most important paragraph for provenance.]`

Machine translation (Google Translate, ChatGPT, etc.) was `[TO FILL: not]` used to produce Kikuyu text.

## Contributor codes

| Code | Role | Identity |
|---|---|---|
| T05-A | `[TO FILL]` | Robi Memusi (Team 5) |
| T05-E1 | Independent fluent Kikuyu reviewer (external) | Name and signed consent held privately |
| `[add others if any]` | | |

## Permission

Every contributor signed a consent statement covering: original authorship (no copying, AI generation or machine translation of Kikuyu), use in the Team 5 datathon submission and assessment, and consideration for a combined NLP Hub corpus with credit. Signed copies are stored privately by `[TO FILL: team member]` and can be shown to organisers on request.

## Changes after collection (v1 → v1.1)

All changes are listed row by row in `logs/v1.1_change_log.csv`. In summary:
- whitespace/tab/line-break cleanup in 10 rows (this changes no prediction of the v1 model);
- reviewer decisions on 11 flagged rows (`review/v1.1_checks.csv`), including replacing the near-duplicate `KIK-POS-022`;
- `KIK-NEG-026` moved dev → train to sit with its paraphrase `KIK-PILOT-017` (shared `group_id`). `KIK-NEG-110` moved train → dev to keep 20 negatives in dev.

The original v1 file is kept unchanged in `data/v1/kikuyu_dataset_v1.csv`.
