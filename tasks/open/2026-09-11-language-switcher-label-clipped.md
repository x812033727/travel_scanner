---
id: 2026-09-11-language-switcher-label-clipped
title: 語言切換器的標籤在幾乎每一頁都被截斷
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T13:05:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/language-switcher.tsx
  - apps/web/app/globals.css
---

# 語言切換器的標籤在幾乎每一頁都被截斷

## Why

實測 162 個頁面的文字截斷（元素 `scrollWidth > clientWidth` 且 overflow 非 visible），共 293 處、24 種。**單一最高頻的就是語言切換器的標籤**：

| 被截斷的文字 | 次數 |
| --- | --- |
| 「語言」 | **122** |
| 「Language」 | 20 |
| 「言語」 | 20 |
| 「外觀主題」 | 12 |
| 「目的地」／「Destination」 | 16 / 4 |

合計 162 次，等於**幾乎每一個頁面、每一個語系都會發生**。手機與桌面都一樣（390 與 1440 的截斷數幾乎相同：19 vs 21），所以不是 RWD 斷點問題，是元件本身的寬度約束。

其餘被截斷的還有「推薦原因:」（24 次）、「Why this appears:」（8）、「おすすめの理由:」（8）、「下一站，從這裡發現」（12）、「搜尋旅行靈感」（12）。

## Definition of done

- [ ] 「語言」及其各語系翻譯在所有頁面都完整顯示。
- [ ] 「外觀主題」「推薦原因:」等其餘 24 種截斷也處理掉，或確認是刻意的單行省略。

## Steps

- [ ] 先分辨哪些是 bug、哪些是刻意的 `truncate`。刻意截斷應該要有 `title` 屬性讓滑鼠停留看得到全文，而且不該發生在只有 2–4 個字的標籤上。
- [ ] 「語言」只有兩個字卻被截斷，八成是容器寬度寫死或 `flex` 子項沒有 `min-width: 0`——那是最常見的成因。
- [ ] 各語系的字串長度不同（Language 比「語言」長很多），修正時要用最長的語系驗證。

## How to verify

掃描腳本的判定：可見、無子元素、`scrollWidth > clientWidth + 2`、且 `overflow !== 'visible'`。修好後這三項條件不應同時成立。

```bash
cd apps/web && npx playwright test --project="Pixel 7"
```

## Notes

- 深色模式與特大字下的截斷數與標準模式完全相同（19/21），代表這與主題、字級都無關，是純結構問題。
