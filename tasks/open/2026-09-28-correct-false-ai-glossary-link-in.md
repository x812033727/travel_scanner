---
id: 2026-09-28-correct-false-ai-glossary-link-in
title: Correct false AI glossary link in image SEO source
status: in-progress
priority: P2
area: docs
owner: codex-batch041-source-fix
claimed_at: 2026-09-28T13:47:32Z
created_at: 2026-09-28T13:47:14Z
completed_at:
branch: codex/article-localization-041-seo-links
depends_on: []
scope:
  - apps/api/app/guides/content/image-seo-workflow.json
---

# Correct false AI glossary link in image SEO source

## Why

Block 16 of the zh-TW image SEO guide discusses checking whether a theme's
image crop keeps a subject's roots, hands, or necessary labels visible. Its
ordinary word `標記` linked to the unrelated AI token glossary article. That
would send readers away from the image guidance and be copied into the four
missing language documents unless corrected first.

## Definition of done

- [x] The misleading article link becomes plain text with the same visible word.
- [x] Every other source field, block, source citation and image reference is unchanged.
- [ ] Pack lint, content-link tests, task checks and PR CI pass (local checks passed; CI pending).
- [ ] The source correction is reviewed and merged before Batch041 translations use it.

## Steps

- [x] Checked the link against the surrounding crop and file-size paragraph.
- [x] Changed only block 16's inline object from `article` to `text`.
- [x] Compared full parsed JSON against the pinned original with that one expected change.
- [ ] Record checks and open a focused PR.

## How to verify

From `apps/api`: `uv run python -m app.guides.pack_cli lint --slug image-seo-workflow`
and `uv run pytest tests/test_guides_content_links.py`. From repository root:
`npm run check:tasks` and `git diff --check`.

## Notes

Original pack at `origin/main` commit `b48c8b1bfa7215356839a49d087f01f502e3d710`
has SHA-256 `ecab2da5004ad12b46093e53c93baa36e88a2963c97c3246545ab9e64bad9367`;
the one-inline correction yields SHA-256
`b10f6e1f633cff9a13ef0470af157fdd4d0b5616b560141c6e17819fda7c0357`.
The full parsed JSON comparison returned `only_expected_change True`.

Local checks: pack lint passed with only the pre-existing `no_summary` warning;
`tests/test_guides_content_links.py` passed 3 tests; `git diff --check` passed.
Task check passed after the source change; it is rerun after this task-note update.

The current official [Google image SEO guide](https://developers.google.com/search/docs/appearance/google-images?hl=zh-tw)
and [W3C alt-text decision tree](https://www.w3.org/WAI/tutorials/images/decision-tree/)
remain available; this edit does not change any SEO claim or source citation.
Four-lock read-only Batch041 baseline receipt:
`C:\Users\x8120\.codex\article-localization-release\batch041-seo-readonly-inventory-20260928\receipt-20260928T134834Z.json`
(SHA-256 `01da33a9f151c5472997a449408593b2b8f4e789dcef06b7f0f9084f1760bb99`).
It confirms this article is active/published v2, zh-TW draft/published v4
matches the pre-correction main document, and all four target locales are
absent. The changed zh-TW source will therefore need a guarded live revision
before target-language publication; its published v4 is not the corrected
source. This PR does not import, deploy, revise, or publish anything.
