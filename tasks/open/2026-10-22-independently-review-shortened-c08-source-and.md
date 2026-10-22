---
id: 2026-10-22-independently-review-shortened-c08-source-and
title: Independently review shortened C08 source and visual delta
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-22T12:33:30Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-shortened.md
---

# Independently review shortened C08 source and visual delta

## Why

C08 縮成 79 句後，先前的來源 PASS 都綁定舊稿，不能證明本版旁白與畫面仍可被直接來源支持。需要一名未參與改稿的審查者留下精確稿件 SHA、逐句問題與視覺邊界，供作者修稿後重審。

## Definition of done

- [x] 對本版 C08 留下綁定 PR head、`script.md` 與 `visual-plan.md` SHA-256 的獨立來源判定。
- [x] 精確指出需要改稿的句號，並把時長估算風險與來源判定分開。

## Steps

- [x] 對照 MoMA、GK 與龜甲萬可直接讀取的資料，核對瓶嘴、年份、商標和數字歸屬。
- [x] 核對旁白／逐鏡 ID、shot/card 比例與視覺提示詞邊界，寫下查核收據。
- [x] 標記 `c080405` HOLD，交作者修訂並等待新雜湊的獨立重審。

## How to verify

查核收據：`docs/videos/story-everyday-kikkoman-c08/reviews/line-source-review-20261022-shortened.md`。其 PR head 與兩檔 SHA 應等於 `git rev-parse HEAD` 和 `Get-FileHash -Algorithm SHA256`；`npm run check:tasks` 與 `git diff --check` 檢查此新增任務及文件。

## Notes

本輪判定 HOLD `c080405`：「卡住設計的，是收手那一刻」把 MoMA 說的防滴與控流雙重難題縮成單一時刻；其他差異未見來源 HOLD。第 2–6 章按 C05 實測語速推算約 408 秒，低於 480 秒門檻，但 C08 尚未付費配音實測。修稿需再查核，不能沿用本版收據放行。
