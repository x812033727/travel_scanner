---
id: 2026-09-20-fix-localization-svg-container-detection
title: Fix localization SVG container detection
status: done
priority: P2
area: tools
owner: codex-article-localization
claimed_at: 2026-09-20T03:32:21Z
created_at: 2026-09-20T03:32:14Z
completed_at: 2026-09-20T03:49:41Z
branch: codex/article-localization-render-containers
depends_on: []
scope:
  - tools/article-localization/render.mjs
  - tools/article-localization/render-layout.mjs
  - tools/article-localization/render-layout.test.mjs
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
---

# Fix localization SVG container detection

## Why

The SVG layout check selected the smallest rectangle crossing a source label's
centre, even when that decorative rectangle did not contain the source label.
Translated CJK subtitle text was therefore reported outside its container despite
remaining inside the actual coloured header band.

## Definition of done

- [x] Container selection only considers shapes that fully contain the source text.
- [x] A regression test covers the overlapping decorative strip used by the
  convenience-store guide.
- [x] A localized SVG description replaces the source-language image
  description in its referencing document block.
- [x] The real staged zh-TW guide renders with no false overflow issue.

## Steps

- [x] Extract the geometry helpers into a directly testable module.
- [x] Update the renderer to use the corrected helper.
- [x] Keep document image descriptions aligned with the localized SVG `<desc>`.
- [x] Run focused, tooling and task validation.

## How to verify

`node --test tools/article-localization/render-layout.test.mjs`

`npm run test:tools && npm run check:tasks`

## Notes

The source English subtitle at y=186 has a measured box from y=167 to y=191.
The old code selected a decorative rectangle from y=176 to y=200 because its
centre crossed that strip. The rectangle never contained the original label.

The six-article zh-TW batch was rematerialized after the fix. All six 1600x900
SVG previews passed the automated bounds and overlap checks; the convenience
store diagram is the regression case.

Validation: 26 Python pipeline tests, 17 renderer/integrity tests, and all 76
tool tests passed (75 run, one existing environment skip). Ruff check/format,
task validation, and diff whitespace checks passed.

Review hardening records each SVG slot's actual element tag. Duplicate numeric
tokens may collapse only in bilingual `<title>` or root-level `<desc>` metadata;
visible `<text>` nodes retain exact multiset checks. Nested or multiple `<desc>`
elements fail closed before a document image description can be updated.

Jobs prepared before this change do not contain `svg_tag`; if they need another
materialization, prepare them again so the explicit metadata binding is present.
Already assembled and hash-reviewed bundles do not need rematerialization.
