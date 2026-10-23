---
id: 2026-10-23-c20-zippo-blind-v2-reader1
title: C20 Zippo blind v2 reader1
status: in-progress
priority: P1
area: docs
owner: codex-c20-blind-v2-reader1
claimed_at: 2026-10-23T05:47:29Z
created_at: 2026-10-23T05:47:28Z
completed_at:
branch: codex/brand-story-zippo-c20-blind-v2-reader1
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/blind-v2-reader1.md
  - tasks/open/2026-10-23-c20-zippo-blind-v2-reader1.md
---

# C20 Zippo blind v2 reader1

## Why

C20 作者稿改過三個來源／配鏡爭點後，舊版盲讀不再適用。第一位讀者只看 68 行旁白投影，先獨立判斷故事是否能兌現開場，再留可核對的獨立收據。

## Definition of done

- [x] 在讀任何企劃、來源、審查或規範前，只讀固定 SHA-256 的旁白投影並鎖定 12 項 PASS／HOLD 判斷。
- [x] 收據逐項給旁白 ID／行號及具體理由，明說不涵蓋來源、配鏡與真實 TTS。
- [ ] 只提交本任務檔與 blind-v2-reader1.md，開對作者 head 的獨立 draft PR 並貼 no-auto-merge；讀回 PR head／base／標籤與 auto-merge 狀態。

## Steps

- [x] 核對輸入檔 68 行與 SHA-256 3E55ABA282998A8A18101D8047F313C88DAAA8CE7E6FD4E21BCF93B117C0C342。
- [x] 固定第一階段收據於獨立暫存檔，SHA-256 BAF9BFB32A80CD58C4C6B6976702972CD0C033F5B1B85E77FB788C9830CECA1E。
- [x] 讀 repo 規範，從作者 head 856b6b24564d7de3a4b1804ccf1f7fc6f10232f2 建極小稀疏、無初始 checkout 的獨立 worktree，claim 此窄 scope。
- [ ] 驗證收據、task 與 staged diff，commit／push，開 draft PR 並核對遠端狀態。

## How to verify

重算投影與第一階段收據 SHA-256；檢查本收據 12 列都含 PASS 或 HOLD 和 ID／行號。執行 node tools/tasks.mjs check、git diff --cached --check，確認 commit 只含本收據與本 task。用 gh pr view 讀回 isDraft=true、base 是 codex/brand-story-zippo-c20-script、base head 對應作者 commit、no-auto-merge 標籤、autoMergeRequest=null。

## Notes

2026-10-23：第一階段 3 PASS／9 HOLD。最需要作者處理的是 c200107 的「為何首款就承諾」在 c200608 沒有答案；戰時／日期碼／博物館與六億段落的因果推進也不足。這是旁白判斷，不能用於取代來源或配鏡查核；沒有改動作者腳本。
