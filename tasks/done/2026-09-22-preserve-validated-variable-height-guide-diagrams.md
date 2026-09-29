---
id: 2026-09-22-preserve-validated-variable-height-guide-diagrams
title: Preserve validated variable-height guide diagrams
status: done
priority: P1
area: api
owner: codex-p1-audit
claimed_at: 2026-09-29T02:10:48Z
created_at: 2026-09-22T08:36:53Z
completed_at: 2026-09-29T02:10:50Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_guides_pack_ingest.py
  - docs/travel-guides.md
---

# Preserve validated variable-height guide diagrams

## Why

Translated guide diagrams sometimes need a taller canvas to keep all source text readable at
15 px or larger. The GuideDocument schema already supports image sides up to 4000 px, but the
content-pack linter required every SVG to use `0 0 1600 900`, while ingest also overwrote every
SVG reference with 1600x900 metadata. A reviewed tall diagram therefore failed lint or received
incorrect layout metadata.

## Definition of done

- [x] Inline SVG diagrams accept a validated 1600 px width and positive integral height up to
  4000 px, with an origin-zero viewBox and matching root dimensions.
- [x] Ingest derives the validated dimensions for every reference, including a second locale
  that shares a staged SVG; hero rendering remains fixed at 1600x900.
- [x] Repository lint compares every ImageBlock reference with the exact SVG dimensions even
  when the asset-level checks were already de-duplicated.
- [x] Existing SVG security, accessibility, external-reference, number and 15 px label checks
  remain active, and the existing fixed 1600x900 packs continue to pass.
- [x] Focused regression tests and documentation cover the new contract.

## Steps

- [x] Add the contextual body-diagram dimension parser without changing default `check_svg()`.
- [x] Derive dimensions on both first-stage and staged-file reuse ingest paths.
- [x] Add per-reference metadata comparison to `lint_all()`.
- [x] Add success, invalid-dimension, shared-reference, mismatch, security, dry-run and fixed-hero
  regressions.
- [x] Update the guide authoring documentation.

## How to verify

```bash
cd apps/api
python -m pytest tests/test_guides_pack_ingest.py -q
python -m pytest tests/test_guides_content_pack.py -q
python -m ruff check app/guides/pack_ingest.py tests/test_guides_pack_ingest.py
python -m mypy app/guides/pack_ingest.py
cd ../..
npm run check:tasks
git diff --check
```

## Notes

- Body SVGs use the schema's existing `MAX_IMAGE_SIDE=4000`; there is no database, schema,
  publisher or front-end change.
- Variable-height diagrams must explicitly declare root `width` and `height`. Existing reviewed
  1600x900 SVGs that omit both optional root attributes remain valid; requiring them retroactively
  would reject 36 shipped life guides without improving their already pinned metadata.
- Dimension tokens are checked against the ASCII SVG number grammar before exact decimal
  comparison. Python-only underscores and Unicode digits are rejected; valid decimal and exponent
  forms remain accepted.
- Default `check_svg()` remains the fixed 1600x900 contract used by `hero.svg`; only body diagram
  staging and lint opt into the contextual dimensions.
- A complete repository audit covered 1,089 packs, 1,889 body-SVG references and 1,589 distinct
  assets (48 legacy fixed diagrams omitted root dimensions). Every reference matched its asset,
  and no existing asset failed the new dimensional or lexical checks.
- A scoped lint over the pending Batch007 integration confirms all 16 tall localized assets now
  pass dimensions. Remaining errors are separate content/source gates: the inherited transit
  zh-TW SVG has 13/14 px labels, and each localized transit diagram draws `330` while its document
  does not carry that number. This task does not waive or repair those findings.
- The two pre-existing merged-task handoff edits in this worktree were left untouched.
- Independent code review PASS is recorded at
  `batch007-resumption-20260922/diagram-dimensions-tool-review-v2/root-independent-code-review.json`
  (SHA-256 `4a02f67a8431ca660f494c265a2afc05d5f1fb3945b475e0bb17242f4c461d91`).
  It rechecked every frozen file and added nine boundary cases, including percentages,
  non-finite numbers, the 4000/4001 limit, the default fixed-height rejection and a real reviewed
  variable-height guide SVG.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-diagram-dimensions；原分支：codex/guide-diagram-dimensions。

- PR #658 merged 2026-09-22.
- main pack_ingest.py has _body_svg_dimensions, staging/reuse dimensions, per-reference svg_dimensions_mismatch checks; all original DoD checked.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。



`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
