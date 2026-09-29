---
id: 2026-09-28-localize-pestle-and-swot-tows-guides
title: Localize PESTLE and SWOT/TOWS guides in five languages (Batch039 Pair B)
status: done
priority: P1
area: docs
owner: codex-p1-audit
claimed_at: 2026-09-29T02:12:23Z
created_at: 2026-09-28T12:22:56Z
completed_at: 2026-09-29T02:12:25Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/guides/content/pestle-business-scan.json
  - apps/api/app/guides/content/swot-tows-action-plan.json
  - apps/web/public/guides/pestle-business-scan
  - apps/web/public/guides/swot-tows-action-plan
  - docs/article-localization/batch039-pair-b-evidence.md
  - tasks/open/2026-09-28-localize-pestle-and-swot-tows-guides.md
---

# Localize PESTLE and SWOT/TOWS guides in five languages (Batch039 Pair B)

## Why

Both published zh-TW strategy guides have complete 33-block source articles but no
zh-CN, English, Japanese or Korean documents. Their hero and diagram artwork has
Chinese text. Batch039 Pair B adds full reviewable translations and locale artwork
without altering the published originals.

## Definition of done

- [x] Both packs contain complete zh-CN, en, ja and ko title, description, body, table, alt, caption and source-title translations.
- [x] Each target locale has a translated hero SVG/JPG and diagram SVG with browser-checked text fit.
- [x] Pinned source facts, qualifiers, URLs/dates, exact ArticleInline targets, and zh-TW/root metadata survive structural and hash audit.
- [x] A scoped evidence record and draft PR are ready for editorial review; live release remains a separate gate.

## Steps

- [x] Confirm #914 merged, reuse its clean worktree, branch from current main, verify freeze and task scopes, and claim this task.
- [x] Translate and review all four target documents for both articles.
- [x] Render and inspect localized SVGs and hero JPGs across all target locales.
- [x] Run scoped lint, API/web tests, task check, browser layout QA and final content/asset hash audit.
- [x] Open draft PR only after content QA and record any external CI blocker.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --kind life --slug pestle-business-scan --slug swot-tows-action-plan`, focused guide content/link/ingest API tests, targeted article/image web tests and typecheck, `npm run check:tasks`, final content/asset hash audit, and browser previews recorded in `docs/article-localization/batch039-pair-b-evidence.md`.

## Notes

- #914 is merged and the reused worktree was clean. Branch base `origin/main` was `c54594e488f48e3655566cc8a86d45e9dc2e004e` before drafting.
- Pinned candidate inventory SHA-256 `3ce92eeeb90f1793988308dacf1d93729b5a0ee61d8e0e98a9a769e68c7d666f`; guarded four-lock read-only receipt `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-readonly-inventory-20260928/receipt-20260928T115126Z.json` SHA-256 `e156935e618b5233d63a5c8981db2dda0837f9cfceefded365fdd75d9485024f`. Both source packs and six original assets still match inventory on current main; receipt captured published zh-TW v4 with no target locales at 2026-09-28T11:51:28Z.
- The earlier two Alembic migration heads were joined by main PR #918. This branch merged `origin/main` `ebde813d6a7fa9cdd8282bfa2400d002c0a6add8`; `uv run alembic heads` reports one head, `0111_video_story_series`. PR CI remains an independent check.
- Final audit: 26 content/asset files, zero issues; 16 final SVG browser cases and 16 desktop/mobile article preview cases, zero issues. API guide tests: 67 passed, 5 skipped; pack lint, web typecheck, task check, and diff check pass. Local Windows Vitest stopped at thread-worker startup for all three targeted guide suites and did not execute assertions; PR CI must validate them. Details and hashes: `docs/article-localization/batch039-pair-b-evidence.md`.
- Draft PR [#928](https://github.com/x812033727/travel_scanner/pull/928) was opened with `isDraft: true` and no auto-merge request. CI is pending; no import, deployment, or publication occurred.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch039-pair-b；原分支：codex/article-localization-039-strategy-b。

- PR #928 merged 2026-09-28; both main packs have five locales, scope evidence doc present.
- DoD covers draft content/24 assets/structural audit/editorial review; live release explicitly separate.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

Live release remains separate and is not claimed.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
