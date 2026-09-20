---
id: 2026-09-20-article-localization-ai-credit-fields
title: Translate descriptive AI hero image credits safely
status: done
priority: P2
area: tools
owner: codex-credit-localization-tool
claimed_at: 2026-09-20T08:30:04Z
created_at: 2026-09-20T08:29:59Z
completed_at: 2026-09-20T12:33:00Z
branch: codex/article-localization-credit-fields
depends_on: []
scope:
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
  - tools/article-localization/README.md
---

# Translate descriptive AI hero image credits safely

## Why

The localization pipeline treated every image credit as immutable. Its AI-made
hero credit uses Chinese text to describe the illustration and disclose that it
is not a photograph, so that text remained Chinese on other-language pages.
Photographer attribution and legal license names must remain unchanged.

## Definition of done

- [x] The known Mokaair AI hero disclosure is translated with its attribution
  preserved; photograph credits and legal license identities remain immutable.
- [x] Field validation rejects a missing Mokaair prefix, omitted AI disclosure,
  copied source disclosure, and translation jobs changing only credit text.
- [x] Focused tests, format/lint, and task validation pass.
- [x] Parent review and PR/release decision.

## Steps

- [x] Add an exact AI hero credit allowlist and validate attribution/disclosure.
- [x] Document staging and migration implications.
- [x] Parent review completed; PR #589 merged and included in production deployment bf820a62.

## How to verify

`apps/api/.venv/Scripts/python.exe tools/article-localization/test_pipeline.py`
(using the existing API venv in the article-localization-tools worktree),
`ruff check tools/article-localization/pipeline.py tools/article-localization/test_pipeline.py`,
`ruff format --check tools/article-localization/pipeline.py tools/article-localization/test_pipeline.py`,
`git diff --check`, and `npm run check:tasks`.

## Notes

The repository currently has 34 AI hero credits with the exact descriptive pair
`Mokaair · AI 生成示意圖` / `AI 生成，非實拍`; copyright/CC and photo credits are separate.
The allowlist intentionally does not rewrite existing staged jobs. Matching new
jobs gain two fields and a new job hash, so prepare them under a new work root.

Parent confirmed PR #589 was merged, and its tooling was deployed with bf820a62
and verified on the production service. The task is closed before claiming the
subsequent same-file URL localization work.
