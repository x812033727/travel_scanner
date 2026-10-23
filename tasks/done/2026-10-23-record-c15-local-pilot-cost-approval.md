---
id: 2026-10-23-record-c15-local-pilot-cost-approval
title: Record C15 local pilot cost approval
status: done
priority: P2
area: docs
owner: codex-c15-paid-pilot-receipt
claimed_at: 2026-10-23T05:33:04Z
created_at: 2026-10-23T05:32:52Z
completed_at: 2026-10-23T05:36:33Z
branch: codex/brand-story-frixion-c15-script
depends_on: []
scope:
  - docs/videos/story-everyday-frixion-c15/reviews/owner-paid-pilot-approval.md
  - docs/videos/story-everyday-frixion-c15/production-quote.md
---

# Record C15 local pilot cost approval

## Why

站主在 2026-10-23 以原文「核准 C15 本機試片，US$25 上限」回答同一份報價。必須把新費用決定與先前已核的劇本／分鏡位元組綁定，並把報價狀態由「待站主核准」改成「上限已核准、路由與語音價格仍阻斷首筆付費」。本票不製作媒體。

## Definition of done

- [x] 獨立站主本機試片費用核准收據，綁定 PR #1701 回答前 head、報價 Git blob SHA-256 與四份原稿 SHA-256。
- [x] 報價明確寫上 US$25 整片上限已核准，同時保留可歸屬預算路由、語音價格及實測 480 秒／70% 畫面停線。
- [x] 不動原四份稿件，不發起付費呼叫、匯入、上傳或發布。

## Steps

- [x] 核對 C15 同一草稿 PR 與原稿雜湊。
- [x] 寫入收據並窄修報價狀態。
- [x] 更新並驗證原 PR #1701 的說明、draft 與 `no-auto-merge`。

## How to verify

對 `4a528e3d11b5afc49b75bd62344f6b5153fb9825` 的 quote 與四份原稿執行 Git blob SHA-256；`git diff --check`；`npm run check:tasks`；`gh pr view 1701 --json headRefOid,isDraft,labels,autoMergeRequest`。核對本次 commit 只含本票、收據與報價狀態修訂。

## Notes

前輪在原作者工作樹的已結案票有一份未追蹤 `tasks/open/2026-10-23-record-c15-frixion-script-approval-and.md` 重複檔，精確路徑刪除被工具回覆 `blocked by policy`。本票在以 `4a528e3d` 建立的獨立、非完整 sparse checkout 透過正常 CLI 認領；沒有觸碰或繞道刪除被擋的舊檔。`npm run check:tasks` 在本票結案前通過 2,078 筆；`tasks done` 寫入本份 done 檔後，同樣留下新的未追蹤 open 副本並以 exit 1 停止，故只提交 done 檔，提交後以 CI 核對。上限核准不代表語音路由、定價或帳本歸屬已驗證，仍不能發起首筆付費呼叫。
