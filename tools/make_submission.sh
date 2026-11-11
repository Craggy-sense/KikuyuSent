#!/usr/bin/env bash
# Tag the current commit as submission-v1, build a ZIP of exactly that commit, and write a manifest.
# Usage (from repo root, after committing everything): bash tools/make_submission.sh
set -euo pipefail
if [ -n "$(git status --porcelain)" ]; then echo "Commit or stash your changes first."; exit 1; fi
grep -rqn "TO FILL" docs README.md && { echo "There are still [TO FILL] items in docs/ or README.md:"; grep -rn "TO FILL" docs README.md; exit 1; }
SHA=$(git rev-parse HEAD)
git tag -f submission-v1 "$SHA" >/dev/null
mkdir -p submission
git archive --format=zip --prefix=KikuyuSent/ -o submission/KikuyuSent-submission-v1.zip "$SHA"
{
  echo "Team: 5 (Zeus) - Strathmore NLP Hub Datathon 2026 - Track B (sentiment) - Kikuyu"
  echo "Repository: https://github.com/Craggy-sense/KikuyuSent"
  echo "Tag: submission-v1"
  echo "Commit SHA: $SHA"
  echo "Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "ZIP sha256: $(sha256sum submission/KikuyuSent-submission-v1.zip | cut -d' ' -f1)"
  echo "Dataset sha256: $(sha256sum data/kikuyu_dataset.csv | cut -d' ' -f1)"
  echo "Model sha256: $(sha256sum models/sentiment_model.joblib | cut -d' ' -f1)"
  echo; echo "Files:"; git ls-tree -r --name-only "$SHA"
} > submission/MANIFEST.txt
echo "Tagged submission-v1 at $SHA"
echo "Built submission/KikuyuSent-submission-v1.zip and submission/MANIFEST.txt"
echo "Now run: git push origin submission-v1"
