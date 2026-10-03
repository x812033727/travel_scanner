---
id: 2026-09-27-fix-batch028-japanese-page-builder-diagram
title: Fix Batch028 Japanese page builder diagram card padding
status: done
priority: P1
area: web
owner: codex-p1-audit
claimed_at: 2026-09-29T02:11:25Z
created_at: 2026-09-27T17:26:02Z
completed_at: 2026-09-29T02:11:27Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/web/public/guides/wordpress-page-builder-choice/diagram-1-ja.svg
---

# Fix Batch028 Japanese page builder diagram card padding

## Why

After Batch028 published its five-language WordPress design guides, independent post-deploy visual QA measured `wordpress-page-builder-choice/diagram-1-ja.svg`. The third card's line `テンプレートの影響範囲` has only 8.80px of right padding at the native 1600×900 size, below the acceptance audit's 12px minimum. The text remains inside the border but looks crowded. The English repair and the 16 published article documents are separate work.

## Definition of done

- [x] The Japanese line keeps its exact wording and the diagram remains 1600×900.
- [x] Every card has at least 12px inner right margin with no text overlap, clipping or missing glyphs at native size and in desktop/mobile article renderings.
- [x] The diff changes only this SVG and this task record; no production write is made by this task.

## Steps

- [x] Claim the exact SVG scope in an isolated worktree based on deployed commit `853a3434dcc2eefe7f2b28f08e725f479b304090`.
- [x] Render local candidate and inspect all four cards and title/footer at native size.
- [x] Independently review the final rendered SVG and run the focused checks; prepare a reviewable PR.

## How to verify

Run a local Chromium SVG `getBBox()` audit against all card text and verify the minimum right margin is at least 12px. Render the full 1600×900 SVG and desktop/mobile article diagrams and inspect the original pixels. Parse SVG XML, compare its visible Japanese text inventory with the deployed version, and run `npm run check:tasks`. Do not treat the previously captured production FAIL as a local PASS.

## Notes

Read-only production card audit at 17:22 UTC: full 20-diagram receipt SHA `6121211a718e12e1203dc56df9cee7c698c806591ad484c1c540c9ecbc4c733f`; Japanese target text bbox right 1142.203px, card right 1151px, margin 8.797px. The 27px original has 52px vertical baseline separation to adjacent rows. Wrapping it into two 27px lines would overlap the next 32px line unless multiple rows are shifted. A 1px font reduction retains the original four-row alignment and wording; local geometry and visual review will determine whether it is sufficient.

Local candidate changes only that one font-size attribute, `27` to `26`. SHA256 `017b9865991f441d0d48986378bcc4ca613b3bdbf121bcb65afb0f84f3cb7091`. External evidence `<home>\.codex\article-localization-release\batch028-wordpress-design\diagram-fit-ja-review\validation.json` SHA256 `3fab14b437601b594b0893c8993ae5f2cbcf7cf5b40949da088655bbf6e882c6`: 4 cards, exact text, minimum right margin 19.765625px, no bbox overlap, native render and desktop/mobile page injection PASS. I viewed native 1600×900 and mobile third-card PNG; all text remains legible. `git diff --check` and `npm run check:tasks` pass (task checker reports pre-existing stale-claim warnings). This local simulation is not a production PASS.

Independent peer reviewed the exact content commit `59885765898ebf53ae7581d17690b84f575caf6a` and local render, PASS in external receipt `<home>\.codex\article-localization-release\batch028-wordpress-design\asset-hotfix-independent-review\jp-page-builder-local-review-20260927T173006Z.json` SHA256 `80c45340d9f4a4361c588094a8ef9d82d3bfbd2e8f456df19e69d1303b9ec9ed`. The old production visual FAIL remains historical; this peer review does not claim the fix is live.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-batch028-jp-diagram-fit；原分支：codex/batch028-jp-diagram-fit。

- PR #869 merged; batch028 release README records deployed SHA 017b9865991f441d0d48986378bcc4ca613b3bdbf121bcb65afb0f84f3cb7091 and margin 19.77px.
- Final independent acceptance SHA e4e4f872ae370a3bef8b1fc04f76eebbb3ea87b681e0997ae110c0a1111f3f26 includes both repaired diagrams.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。



`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
