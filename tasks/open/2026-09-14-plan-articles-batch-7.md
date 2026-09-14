---
id: 2026-09-14-plan-articles-batch-7
title: 規劃第七批旅遊文章：喀比優先，再補仙台、大邱、清萊、大叻、順化、全州
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-14T13:37:34Z
completed_at:
branch:
depends_on: []
scope:
  - docs/travel-guides-batch-7
---

# 規劃第七批旅遊文章：喀比優先，再補仙台、大邱、清萊、大叻、順化、全州

## Why

第六批（2026-09-14）之後，目的地目錄裡 primary 城市喀比（krabi）仍是 0 篇；仙台、大邱、清萊、大叻、順化、全州也沒有文章。第六批規劃時已列了候補與被淘汰的題目。

## Definition of done

- [ ] 照第六批的做法（`docs/travel-guides-batch-6/README.md` 的流程：候選、評分、逐篇讀官方頁、規格、三輪一致性）在 `docs/travel-guides-batch-7/` 產出 README 與每篇規格。
- [ ] 喀比第一（例如 krabi-ao-nang-railay-4-islands）；規格要求它和 `phuket-airport-transport-where-to-stay` 互連。

## Steps

- [ ] 候補：ha-long-bay-cruise-from-hanoi（河內篇 Day 3 會連過去）、澳門一日遊（香港入境篇與行程篇留了位置）、2027 年農曆新年跨亞洲（與 2027 連假篇重疊，要分工）。
- [ ] 藏王與銀山溫泉冬季文等 11 月各度假村公布日期再排。
- [ ] 香港迪士尼 vs 海洋公園、首爾漢江巴士、韓國高速巴士、順化在第六批被淘汰，原因是核心數字在官方頁讀不到；再選前先確認官方頁狀況。

## How to verify

`npm run check:tasks` 通過；README 表格的 slug、kind、destination、topics、display order 與規格一致。

## Notes

- 第六批的教訓寫在 `2026-09-14-launch-articles-batch-6-twenty-more` 的 Notes（Commons API 429 的替代路徑、hero 壓縮、圖解數字規則、規格錯誤的更正）。
