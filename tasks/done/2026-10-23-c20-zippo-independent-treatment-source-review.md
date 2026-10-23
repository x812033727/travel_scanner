---
id: 2026-10-23-c20-zippo-independent-treatment-source-review
title: C20 Zippo independent Treatment source review
status: done
priority: P2
area: docs
owner: codex-c20-independent-review
claimed_at: 2026-10-23T03:54:58Z
created_at: 2026-10-23T03:54:44Z
completed_at: 2026-10-23T03:58:05Z
branch: codex/brand-story-zippo-c20-independent-review
depends_on: []
scope:
  - docs/videos/story-everyday-zippo-c20/reviews/independent-treatment-review.md
---

# C20 Zippo independent Treatment source review

## Why

C20 作者的六章 Treatment 與 M01–M13 來源矩陣需要不同代理對原件逐項覆核，並把結論綁到作者 PR #1708 的精確內容雜湊。保修的地區與商品界線、PDF 可讀性及運費說法尤其不能由宣傳推成全球條款。

## Definition of done

- [x] 獨立收據逐項列出 M01–M13 的 PASS／HOLD、可說界線、來源與作者檔案內容雜湊。
- [x] 不改作者的 Treatment／矩陣，另開以作者分支為 base 的草稿審查 PR，貼 `no-auto-merge`。

## Steps

- [x] 核對作者 commit、Git blob 內容 SHA-256 與工作樹檔案 SHA-256。
- [x] 查 task-board 路徑碰撞，於獨立工作樹建立並認領本票。
- [x] 逐項閱讀公司歷史、現行美國與英國維修頁及美國原始專利；無法直接讀取的官方 PDF 留精確 HOLD。
- [x] 寫入 `docs/videos/story-everyday-zippo-c20/reviews/independent-treatment-review.md`，提交並推送草稿 PR。

## How to verify

`python -c` 對 `git cat-file blob HEAD:<path>` 重算 SHA-256；`Get-FileHash` 核對工作樹；`npm run check:tasks`、`git diff --check`；`gh pr view` 核對 base、draft 與標籤。逐項原件 URL 與裁決寫在收據。

## Notes

作者 head 固定為 `b83a45fac8a97752aa3f96be46e64a4ba4968728`。Treatment 內容 SHA-256 `DDB768024F4560C00CEEF298C1D2EE48145683544DF0BECE4E88331885D2A2B6`，matrix `741689FC4BF7D2705546567DEE067AAA884C58CFF61E1ABC9D13C1BC8B3A78CB`；均由本代理重算。M11 的英國頁原文要求 insured **and** trackable，作者矩陣誤寫成「可追蹤**或**保價」。國際版說明書 PDF 於本輪網頁開啟超時、直接連線失敗，不能把搜尋索引片段當現行寄件費條款原件；審查收據對費用分配與 M11 文字列 HOLD。其餘公司歷史均標後來回顧，專利只證原申請構造；美國保修與英國內膽流程各限其所在頁面。沒有付費、匯入、上傳或發布。

作者修訂 head `936873bbb21808546f2dfdbdb17a5e363f263198` 後，獨立重新抓取與差分覆核：Treatment Git blob 內容 SHA-256 `3DF65F2FA5EC7B7FAF0F4C3A576C27E66C89EF3368DAAB9AC060E87EB52156E7`；matrix `6687CD9072DFCAFA533DB90F93565CEC802AC225DA147E0D7EFE8BABAD0FB08E`。M11 已改成英國「保價且可追蹤」，並明註 PDF 費用句不用；Treatment 第 5 章移除費用定論。此精確 head 的 Treatment 來源覆核為 PASS，仍非站主採用或製作授權。
