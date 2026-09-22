---
id: 2026-09-21-validate-equivalent-singapore-guide-numbers-and
title: Validate equivalent Singapore guide numbers and food-directory links
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-21T23:03:29Z
completed_at:
branch: codex/batch010-pipeline-validator
depends_on: []
scope:
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
---

# Validate equivalent Singapore guide numbers and food-directory links

## Why

The batch010 Singapore translation jobs currently produce 112 numeric/token
warnings from the stock localization validator, and its verified-route filter
rejects the public `/foods?city=singapore` directory. These must be resolved
without weakening fare/date safeguards or approving a content defect.

## Definition of done

- [ ] All numeric differences are independently reviewed and any genuine
  source-to-target omission is corrected in the content candidate first.
- [ ] Only proven numeric/unit equivalences or exact reviewed exceptions pass;
  changed fares, dates and route links still fail.
- [ ] The exact public Singapore food directory query is localized in all five
  languages; unknown queries and unpublished guide links remain blocked.
- [ ] Focused validator/link tests, lint and task checks pass in a complete
  checkout; tooling PR is reviewed separately from content.

## Steps

- [x] Classify all 112 warnings against pinned source and candidate hashes.
- [x] Return content gaps for independent editorial review before tooling work.
- [ ] Recheck revised candidate and implement narrow validator/link rules.
- [ ] Test and open an independent tooling PR.

## How to verify

`apps/api/.venv/Scripts/python.exe tools/article-localization/test_pipeline.py`,
Ruff check/format on the changed Python files, `git diff --check`,
`npm run check:tasks`, and a fresh eight-job materialization preflight.

## Notes

The immutable candidate is commit `e0392c90966af673fba7cabd63b75a33a3c29d86`.
Classification and exact source/target snippets are in
`C:\Users\x8120\.codex\article-localization-release\batch010-work\numeric-112-classification-review.json`
(SHA-256 `7839067cbe4e9e1527af96c2b1b695af6a31a588ebb949c3c814c1fe13f2caaf`).
The hash-bound return request is `content-gap-review-request.json` in the same
directory (SHA-256 `834ad328a5e9ed61ac48cde33f9a92abe580a7d93b46141eaf63370096c3ae0f`).
It records two clear English SVG subtitle omissions and four condensed-duration
fields requiring editorial judgment. No pack, SVG or tooling code was changed;
do not waive these warnings. The new task is released while independent content
review and revision proceed. The old PR #600 task was archived as already merged.
