---
id: 2026-09-21-diagram-breakout-wide-screens
title: 寬螢幕上讓圖解用掉文章欄旁邊的空白
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-21T09:09:50Z
completed_at:
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

- [ ] 在 1440px 以上的視窗，圖解完整顯示、不需要橫向捲動。
- [ ] 任何視窗寬度下 `document.documentElement.scrollWidth == innerWidth`，整頁不橫向捲。
- [ ] 手機維持現狀（捲動盒），沒有回歸。

## Steps

- [ ] 決定斷點。`xl`（1280px）時欄外單邊剩 276px，扣掉頁面 padding 還要留餘裕；
      1440px 起比較安全（單邊 356px）。
- [ ] 用媒體查詢加寫死的負邊距，**不要用 `100vw`**。
- [ ] 帶捲動條與不帶捲動條的瀏覽器都要量（Windows Chrome 會佔寬度，macOS 預設不會）。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
```

再用瀏覽器在 375／768／1024／1280／1440／1920 六個寬度逐一量：

```js
JSON.stringify({w:innerWidth, pageOk:document.documentElement.scrollWidth<=innerWidth})
```

六個都要是 `pageOk: true`。

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
