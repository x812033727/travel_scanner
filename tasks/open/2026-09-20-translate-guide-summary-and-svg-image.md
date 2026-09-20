---
id: 2026-09-20-translate-guide-summary-and-svg-image
title: Translate guide summary and SVG image descriptions in article localization jobs
status: in-progress
priority: P1
area: tools
owner: codex-batch007-summary-tool
claimed_at: 2026-09-20T13:17:13Z
created_at: 2026-09-20T13:16:40Z
completed_at:
branch: codex/batch007-summary-description
depends_on:
  - 2026-09-20-article-localization-verified-site-links
scope:
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
  - tools/article-localization/README.md
---

# Translate guide summary and SVG image descriptions in article localization jobs

## Why

Four published Tokyo guides begin with a `summary.items` block. The localization
pipeline rejects that valid GuideDocument block during preparation. Each also has
a long image description duplicated in its SVG `<desc>`; the pipeline currently
omits the document field and silently replaces it from the translated SVG.

## Definition of done

- [x] Full translation jobs expose every summary item (300-character limit) and
  each nonempty image description (4,000-character limit) for review.
- [x] A translated image description and the corresponding SVG `<desc>` agree;
  a mismatch stops materialization before any artifacts are written.
- [x] Existing image-only jobs still derive descriptions from SVG `<desc>`;
  unsupported blocks, immutable credits, URLs and source dates stay guarded.
- [ ] Focused tests, format/lint and task checks pass; PR contains tooling only.

## Steps

- [x] Confirm #596 merged and close its task before claiming this scope.
- [x] Add narrow field extraction and preflight consistency guard.
- [x] Test full and image-only paths, document validation, and refusal cases.
- [ ] Open a separate tooling PR; do not import or publish article content.

## How to verify

Run `apps/api/.venv/Scripts/python.exe tools/article-localization/test_pipeline.py`,
`ruff check` and `ruff format --check` on pipeline and test files, `git diff
--check`, and `npm run check:tasks`. Read-only extraction against the four
Tokyo source documents must include summary and long-description pointers.

## Notes

The four source summaries have 3, 3, 4, and 5 items respectively; each long
description equals the corresponding SVG root `<desc>` in its zh-TW source.
SummaryBlock requires 2–5 items, each at most 300 characters, before the first
heading. ImageBlock.description allows up to 4,000 characters. The new guard
applies only when a full job has a translated document-description field;
image-only jobs have only SVG fields and retain their existing backfill.
The four repository zh-TW source packs yield summary counts 3/3/4/5 and one
4,000-character-limited image-description pointer each with the updated
extractor. The paired source SVG `<desc>` values match those descriptions.
The 32 Python pipeline tests pass, including a two-SVG mismatch that leaves no
output artifacts. Ruff check/format, the 14 artifact-integrity tests, and task
validation pass. The broad `npm run test:tools` cannot start its unrelated
Playwright crawler test in this fresh worktree because `@playwright/test` is
not installed here; CI installs dependencies and will run the full suite.
