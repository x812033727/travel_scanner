---
id: 2026-09-27-batch030-english-migration-diagram-fit
title: Fit Batch030 English migration diagram labels
status: done
priority: P1
area: web
owner: codex-p1-audit
claimed_at: 2026-09-29T02:11:03Z
created_at: 2026-09-27T23:35:04Z
completed_at: 2026-09-29T02:11:06Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/web/public/guides/wordpress-com-migration/diagram-1-en.svg
  - apps/web/public/guides/wordpress-domain-migration/diagram-1-en.svg
  - apps/web/public/guides/wordpress-host-migration/diagram-1-en.svg
  - apps/web/public/guides/wordpress-migration-aftercare/diagram-1-en.svg
---

# Fit Batch030 English migration diagram labels

## Why

Independent Batch030 post-publication QA measured card text against the right edge in all 20 diagram-1 language variants. Only the four English migration diagrams failed: some labels left less than 12 SVG units of space, and three crossed the card edge. The release hold remains in place pending this asset fix and new QA.

## Definition of done

- [x] All four English diagrams preserve their wording and fit every card with at least 16 SVG units of right margin at native 1600 × 900 size.
- [x] Full-size Chromium render shows no card text overlap or clipping.
- [x] Review, merge, deploy, and independently verify the corrected assets before clearing the production hold.

## Steps

- [x] Compare the independent Chromium getBBox report for all 20 language variants.
- [x] Reduce only the English card body labels from 32 to 28 SVG units; headings, other labels, and all other languages remain unchanged.
- [x] Render all four at native size and inspect the images.
- [x] Run targeted pack lint, task check, and diff check.

## How to verify

Run the four guide-pack lints from apps/api: `python -m app.guides.pack_cli lint --slug <slug>` for wordpress-com-migration, wordpress-domain-migration, wordpress-host-migration, and wordpress-migration-aftercare. Run `npm run check:tasks` and `git diff --check`. For the exact visual regression, use Chromium to open each local SVG at 1600 × 900, measure card text `getBBox()`, and require right margin ≥16 SVG units.

## Notes

- Independent pre-fix QA: `C:\Users\x8120\.codex\article-localization-release\batch030-independent-postpublish-qa-v2-20260928\svg-card-bounds.json` (20 variants; only 4 English files failed). Its minimum English margins included -6.33 (domain) and -9.88 (aftercare).
- Local post-fix Chromium report and full-size PNGs: `C:\Users\x8120\.codex\article-localization-release\batch030-svg-fit-qa-20260928\`. Minimum right margins by article: 38.88, 32.58, 37.08, and 29.48 SVG units. All four PASS the ≥16 condition and were visually inspected.
- Four pack lints passed with existing content warnings about summary blocks and English article length; no article content changed. `npm run check:tasks` passed (stale unrelated task warnings) and `git diff --check` passed.
- This PR only changes repository SVGs. It does not deploy assets, import articles, publish, or clear the production hold.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch030-svg-fit；原分支：codex/batch030-en-svg-fit。

- PR #874 merged 2026-09-28; docs/article-localization/releases/batch030/README.md records exact corrected asset deployment, eight English desktop/mobile checks, four full-size SVGs, min margins 29–39, independent PASS and hold clearance.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。



`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
