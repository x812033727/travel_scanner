---
id: 2026-09-27-fix-batch028-english-page-builder-diagram
title: Fix Batch028 English page builder diagram overflow
status: done
priority: P1
area: web
owner: codex-p1-audit
claimed_at: 2026-09-29T02:11:19Z
created_at: 2026-09-27T14:55:30Z
completed_at: 2026-09-29T02:11:25Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/web/public/guides/wordpress-page-builder-choice/diagram-1-en.svg
---

# Fix Batch028 English page builder diagram overflow

## Why

The already-published English page-builder guide shows four lines spilling past the right edge of their diagram cards on the live desktop page. The four phrases are “Which pages are special?”, “Mobile and interaction”, “Dynamic data source”, and “Features and licenses”. The existing SVG-wide bounds check missed card-relative overflow. Correct only this English SVG; the guarded Batch028 production hold stays in place until the asset is separately reviewed, deployed, and the full published-site QA is repeated.

## Definition of done

- [x] All four English phrases remain complete and legible inside their own cards at original SVG size and on live-equivalent desktop and horizontally scrolled mobile renders; the other guides and language images remain byte unchanged.
- [x] A narrow PR passes relevant validation and preserves the original failure screenshots/hash for the protected asset-only release.

## Steps

- [x] Confirm production failure, source SVG hash, and exact card-relative bounds; claim this one-file task after closing the merged content task.
- [x] Wrap the four phrases with natural line breaks and adequate vertical spacing in the existing SVG.
- [x] Render and inspect original 1600×900 SVG, desktop page, and mobile right-scroll positions; run focused checks, review diff, and open a narrow PR without deploying across the hold.

## How to verify

Use Chromium/Playwright on the SVG and live-equivalent guide page at 1280×900 and 390×844. Read each text element's rendered `getBBox()` and compare it with its card's inner rectangle; inspect original-size PNG plus desktop and horizontally scrolled mobile screenshots. Run `npm run check:tasks`, relevant web lint and guide pack lint if affected, and inspect `git diff --check`/exact changed paths. The release owner must independently approve a guarded asset-only deployment; repository merge alone does not alter the live SVG.

## Notes

Original SVG SHA256 `39594b83a61e794ca16d02e2a44e0f8499e0f7f875baa28a962b12340256bc2e`. Independent production QA measured card overflows of +6, +9, +6, and +13 px respectively; the other 19 Batch028 diagrams did not show card overflow. Original failed desktop/mobile captures and raw HTML/assets are retained under `C:\Users\x8120\.codex\article-localization-release\batch028-wordpress-design\peer-review-agent\acceptance-v3`. PR #852 had already merged and its content task was closed; this is a separate post-publication correction. No production asset, database, or hold write is part of this task.

Local repair SHA256 `df4bee3246105b41378d09ef44e9c069f1a354b8c496b16f2c9d64833b6d4dc9`. Playwright original-size, desktop and four mobile scroll positions, plus card-relative `getBBox()` all passed; smallest card right margin is 15.42 px. Sealed local receipt SHA256 `4ffd35f1f4503f4c31a326e514b02a9ca36d896dd75f7167fa47327252ea3067` in `C:\Users\x8120\.codex\article-localization-release\batch028-wordpress-design\diagram-fit-review\sealed-local-visual-review.json`. Independent review `REVIEW_PASS.json` SHA256 `a370067266fd80d1ac4c760186911cde1eaff09b8e6efc558fbf1c7e45ec8696` confirms the original-size pixel hash, complete labels and responsive renders. Original live FAIL receipt and screenshots remain unchanged; guarded deployment and new full QA remain separate release work.

Focused `wordpress-page-builder-choice` pack lint, `check:i18n`, `check:tasks`, web typecheck and web lint passed. The pack lint reported existing non-blocking summary/text-length warnings without an error. PR and CI remain to be checked separately.

Draft PR #863 opened at reviewed head `ffbd74b6f5f3a047f248c827f5aa57005ec987e7`; `isDraft=true` and `autoMergeRequest=null` were verified immediately after creation. CI was still running. Independent peer local asset review SHA256 `0bc6fb69bc86526b814b6edd4e190d9573dc62a08538a0c096d1f85192ee5ac1` confirmed the four labels and desktop/mobile renders. The production hold remains active.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch028-diagram-fit；原分支：codex/batch028-diagram-fit。

- PR #863 merged; batch028 release README records deployed SHA df4bee3246105b41378d09ef44e9c069f1a354b8c496b16f2c9d64833b6d4dc9 and minimum margin 15.42px.
- Final release QA included repaired English/Japanese diagrams, 40 page cases/20 mobile-right cases, all 20 card bounds pass, hold cleared.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。



`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
