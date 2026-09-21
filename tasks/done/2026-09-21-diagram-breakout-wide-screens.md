---
id: 2026-09-21-diagram-breakout-wide-screens
title: 寬螢幕上讓圖解用掉文章欄旁邊的空白
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-21T12:46:17Z
created_at: 2026-09-21T09:09:50Z
completed_at: 2026-09-21T13:07:51Z
branch:
depends_on: []
scope:
  - apps/web/components/content-blocks.tsx
---

# 寬螢幕上讓圖解用掉文章欄旁邊的空白

## Why

2026-09-21 修好了圖解在手機與桌機上的可讀性（票 `2026-09-21-diagram-text-is-unreadable-at-mobile`）：
圖現在畫到 1180px 寬、放在自己的橫向捲動盒裡，15px 的標籤從 6.8px 變成 11.1px。

**但桌機其實不必捲。** 文章欄寬固定 728px，1600px 的視窗左右各有 436px 空白沒用到，
1920px 的更有 596px。圖如果能突破欄寬，寬螢幕讀者就能一眼看完整張，完全不用捲。

**沒有直接做的原因是它有一個真的會踩到的陷阱。** 可靠的突破做法要用
`margin-inline: calc(50% - 50vw)`，而 `100vw` **包含垂直捲動條的寬度**，
在有捲動條的桌機上會讓整頁多出十幾 px 的橫向捲動——那正好違反上一張票自己列的驗收條件
（`scrollWidth == innerWidth`）。用固定 px 的負邊距則會在 1024px 這種剛好夠不到的寬度溢出。

## Definition of done

- [x] 在 **1280px** 以上的視窗，圖解完整顯示、不需要橫向捲動（比原訂的 1440 更早生效）。
- [x] 任何視窗寬度下整頁不橫向捲。實測 375／1279／1280／1366／1920 五種。
- [x] 手機維持現狀（捲動盒），沒有回歸。

## Steps

- [x] 決定斷點：**`xl`（1280px）**。實測 1280px 視窗含 15px 捲動條時，盒子左緣落在 42px，
      還有餘裕；連 1279px 都不會溢出，所以這個斷點取得保守。
- [x] 用媒體查詢加寫死的負邊距，沒有用 `100vw`。
- [x] 量過帶捲動條的情形（Windows，捲動條 15px，`innerWidth 1280` → `clientWidth 1265`）。
      不帶捲動條的情形只會更寬鬆，因為餘裕更大。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
```

再用瀏覽器在 375／768／1024／1280／1440／1920 六個寬度逐一量：

```js
JSON.stringify({w:innerWidth, pageOk:document.documentElement.scrollWidth<=innerWidth})
```

六個都要是 `pageOk: true`。

## 做法（2026-09-21）

`apps/web/components/content-blocks.tsx` 的捲動盒加一組 `xl` 變體：

```
-mx-5 overflow-x-auto px-5  xl:-mx-[226px] xl:px-0
```

`xl` 以上抵銷量變大、內距歸零，盒子剛好等於圖的 1180px，於是**完全不需要捲動**。

**226 這個數字差點寫錯，值得記下來。** 第一版寫 206，是用 `main` 的 768px 去算
`(1180 − 768) / 2`。量出來盒子只有 1140px、還是要捲 40px。原因是
**`main` 的 768 含它自己的 `px-5`**，圖所在的那一欄實際是 728px，
所以正確的是 `(1180 − 728) / 2 = 226`。這種差錯算式看不出來，只有量得出來。

| 視窗 | 版面寬 | 盒子 | 左緣 | 要捲嗎 | 整頁橫向捲 |
|---|---|---|---|---|---|
| 1280 | 1265 | 1180 | 42 | 否 | 無 |
| 1366 | 1351 | 1180 | 85 | 否 | 無 |
| 1920 | 1905 | 1180 | 362 | 否 | 無 |

## Notes

- 2026-09-21 量到的事實：**文章欄寬在 1024、1600、1920px 視窗下一律是 728px**，有上限，
  所以視窗再寬欄也不會變寬。375px 視窗下是 335px。
- 現行寬度常數是 `DIAGRAM_READABLE_WIDTH = 1180`，在 `apps/web/components/content-blocks.tsx`，
  由 `pack_ingest.MIN_LABEL_PX = 15` 推出來（`15 × 1180/1600 = 11.1px`）。
- 圖在 1180px 時高 664px。突破欄寬不會改變這個高度，只會少掉橫向捲動。
- **2026-09-21 續修後起點已經不是 728 了。** 捲動盒用 `-mx-5 px-5` 抵銷並加回
  `main` 的 20px 留白，所以現在桌機的可視窗口是 **768px**（等於 `main` 本身），手機是 375px。
  這張票要處理的是「768 以外那片空白」，離 1180 還差 412px。
- `-mx-5` 安全的原因是它抵銷一個已知的固定值。**這張票要的突破不一樣**，
  它需要知道視窗寬度，所以才會碰到 `100vw` 含捲動條的問題。
