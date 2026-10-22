---
id: 2026-10-22-independently-recheck-c07-final-narrative-source
title: Independently recheck C07 final narrative source delta
status: done
priority: P1
area: docs
owner: codex-c07-v12-source
claimed_at: 2026-10-22T14:54:02Z
created_at: 2026-10-22T14:53:55Z
completed_at: 2026-10-22T14:55:14Z
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v12.md
---

# Independently recheck C07 final narrative source delta

## Why

盲讀指出 C07 第三章及第六章轉場斷裂；作者修訂後，原 v11 來源 PASS 僅屬舊 SHA。需由不同審查者直接讀來源，重核改過的句與畫面。

## Definition of done

- [x] 留下綁定新 SHA 的逐句／逐鏡來源差異覆核及後續關卡。

## Steps

- [x] 對照前後稿，直接查 B3、B2、A1，核 c070307–310、c070606–608 及對應畫面。
- [x] 重算 73 個 ID 同序、鏡型與來源適用範圍；明示兩位新盲讀及時長仍待完成。

## How to verify

`Get-FileHash` 三檔；`git show HEAD --` 對照改句；PowerShell 正則比對 script／visual 的 73 個唯一 ID 同序；來源網址列於收據。

## Notes

收據：`docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review-v12.md`。新稿 73／73 的來源界線 PASS；「這條街」是否讓盲讀者誤會荷蘭鞋帶與英國花卉客製同地，是敘事盲讀的明示觀察點。沒有付費。
