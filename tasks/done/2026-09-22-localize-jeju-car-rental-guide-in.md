---
id: 2026-09-22-localize-jeju-car-rental-guide-in
title: Localize Jeju car rental guide in five languages
status: done
priority: P1
area: docs
owner: codex-p1-audit
claimed_at: 2026-09-29T02:10:28Z
created_at: 2026-09-22T00:46:00Z
completed_at: 2026-09-29T02:10:32Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/guides/content/jeju-car-rental-guide.json
  - apps/web/public/guides/jeju-car-rental-guide
---

# Localize Jeju car rental guide in five languages

## Why

The public Jeju car-rental guide has only a published `zh-TW` document. Complete
`en`, `ja`, `ko`, and `zh-CN` documents and language-specific text diagrams are
needed without losing the published source, photos, credits, or factual limits.

## Definition of done

- [x] The Jeju pack has all five full locale documents, including image text,
      source titles, tables, link labels, descriptions and credits.
- [x] The corrected `zh-TW` source and four translations have independent,
      hash-bound review and desktop/mobile diagram inspection.
- [x] A Jeju-only PR is open with passing scoped checks and no Nami/Seoul files.

## Steps

- [x] Pin live `zh-TW` v6, reconcile repo differences, and independently review
      the exact source corrections.
- [x] Translate four complete documents and four SVGs and verify all hashes.
- [x] Run scoped lint, pipeline tests, pack tests, task checks, and render checks.
- [x] Open the Jeju-only PR; keep publication behind a later release gate.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug jeju-car-rental-guide`
from `apps/api`, `uv run python ../../tools/article-localization/test_pipeline.py`,
`uv run pytest tests/test_guides_pack_ingest.py tests/test_guides_content_pack.py -q -k 'not packaged_content_validates and not packaged_life_content_passes_lint'`,
`node --test tools/article-localization/artifact-integrity.test.mjs`, and
`npm run check:tasks`. Recheck the candidate's eight PNG hashes and independent
review receipt before publication; read-only live version/visibility verification
and import dry-run are later release gates.

## Notes

- Base `origin/main` at split: `f36acbb57568b79bd0bf37002ff12a56fe2d89d1`.
  Jeju pack/assets had no changes from the original source baseline
  `2c3deadd2efa8ea0890d5c6650fc1aef28cf0394`.
- Live source at `2026-09-22T07:21:20.716347+08:00`: article v2, active and
  published `zh-TW` v6, SHA-256
  `2610fc945b0e6cb47ff4939c26a324737e5ed2b186b3b57ad458984f71d5ab31`.
  Recheck before import; this PR does not publish content.
- Source correction review receipt SHA-256
  `773608f2f5a3f0d83151a3223db8eb657a76dadcebf55f38bcc3f059544265af`.
  Corrected `zh-TW` SVG SHA-256
  `baf9e3a32cc75e52a243392320b516fdd5872ed1da4c8653c24e9d53386340a7`.
- Frozen five-language pack SHA-256
  `49a57dd942994cd5bd8ecf473ecbddece0713cdf3052e8cb2ce854c92e2f639a`;
  candidate packet SHA-256
  `fc51f6213f8fe9d1650d3412aa8669289c380d5911e6cec1248fad505b7b8163`;
  independent content review receipt SHA-256
  `51cf40b0f345948706ca91e7f2ae597f7c6cc8d43176782885d2babad241d7f7`
  (`approved_exact_frozen_jeju_v3_candidate`, zero blockers).
- Scoped pack lint passed with only existing `no_summary` guidance and English
  length guidance; full translation was retained. Pipeline: 32 passed;
  artifact-integrity: 14 passed; API pack tests: 38 passed, 5 skipped,
  2 unrelated repository-wide asset tests deselected for sparse checkout;
  task check passed with unrelated stale/overlap warnings. Four 1600x900
  desktop and four 780x440 mobile diagram PNGs retained their bound hashes;
  independent reviewer also inspected 390px horizontal-scroll segments.
- The original three-article task's local scope was narrowed to Nami and Seoul.
  Their candidate files remain on HOLD in the separate author worktree and are
  excluded from this PR. Do not merge, deploy, import or publish this PR before
  the earlier batch release gate and a fresh live version/visibility check.
- PR: https://github.com/x812033727/travel_scanner/pull/643. Keep this task in
  `review` until the PR is merged; `done` is reserved for the merge.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch011-jeju-author；原分支：codex/article-localization-batch-011-jeju。

- PR #643 merged 2026-09-22.
- Main five locales; docs/article-localization/releases/2026-09-22 records five drafts/five publications, five HTML and ten browser cases with independent LF SVG review.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。



`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
