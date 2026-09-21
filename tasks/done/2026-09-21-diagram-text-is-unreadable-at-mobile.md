---
id: 2026-09-21-diagram-text-is-unreadable-at-mobile
title: Diagram text is unreadable at mobile width
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-21T08:49:00Z
created_at: 2026-09-21T01:04:29Z
completed_at: 2026-09-21T09:09:48Z
branch:
depends_on: []
scope:
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/guides/guide-image.tsx
---

# Diagram text is unreadable at mobile width

## Why

Editorial diagrams are authored on a 1600x900 canvas and rendered inside the article
column. At a 375px viewport that column is 335px wide, so the whole SVG is scaled to
21% and every label shrinks with it. Measured on the live English
`singapore-gardens-indoor-outdoor` guide on 2026-09-21, all 19 text elements land
between 4.8 and 8.8 CSS pixels, against 16px body text in the same article:

| Authored size | Rendered at 375px | Count | Example label |
|---|---|---|---|
| 42 | 8.8 px | 1 | Step order · A practical sequence |
| 34 | 7.1 px | 4 | 01 |
| 33 | 6.9 px | 3 | Choose your focus |
| 29 | 6.1 px | 1 | Check maintenance |
| 26 | 5.4 px | 5 | Indoor vs. outdoor |
| 25 | 5.2 px | 1 | Choose what suits you… |
| 23 | 4.8 px | 4 | Pick one priority |

The diagram is decorative on a phone: the reader can see the shape of the four steps
but cannot read them.

This is not one article's problem. The same 1600x900 convention is used across the
localized guide batches, and two independent reviews already recorded it per article:
batch-006 asked for KL English SVG legibility, and
`2026-09-20-localize-four-tokyo-first-trip-guides` notes that "at 390px the whole
1600px diagram is scaled down; small lettering needs explicit mobile-readability
review". Both notes sit inside article-scoped localization tasks owned by other
sessions, so nothing tracks the shared rendering problem that causes them.

It is not an accessibility failure today. Every diagram carries alt text, the figure
has a "Read the full description" disclosure that repeats the content as prose, and
the page allows pinch zoom (`width=device-width, initial-scale=1`, with no
`user-scalable=no` and no `maximum-scale`). The gap is that a phone reader cannot use
the diagram as a diagram without leaving the reading flow.

## 2026-09-21：這不是手機獨有的問題，原本的前提寫窄了

在正式站逐一量過，**文章欄寬在任何視窗下都是 728px**（375px 視窗下是 335px，
1024、1600、1920px 視窗下一律 728px，欄寬有上限）。所以同一個 15px 標籤：

| 視窗 | 欄寬 | 圖的縮放 | 15px 標籤變成 |
|---|---|---|---|
| 375px（手機） | 335px | 0.21 | **3.1px** |
| 1024px 以上（桌機） | 728px | 0.455 | **6.8px** |

也就是說**桌機也讀不到**，只是沒那麼糟。原本的完成定義寫「桌機維持不變」，
是在以為桌機沒事的前提下寫的；那個前提不成立，所以這一條刻意不遵守，理由記在下面。

同時量了這次重繪的 22 張韓國圖共 513 個標籤：**89% 在手機上低於 6px、98% 低於 9px**，
範圍 3.1–12.1px。重繪前是 532 個標籤、同樣 89%、同樣範圍，所以**重繪既沒有改善也沒有惡化**，
它是 `pack_ingest.MIN_LABEL_PX = 15` 搭配 1600px 畫布的結構性後果。

## Definition of done

- [x] At a 375px viewport a reader can read every label in an article diagram.
      量到 15px 的下限標籤變成 11.1px，17px 變成 12.5px，21px 變成 15.5px。
- [~] ~~Desktop rendering is unchanged.~~ **刻意違反。** 桌機同樣是 6.8px，
      用斷點只修手機會把筆電讀者留在原地。桌機現在一樣是 1180px 的圖加一條橫向捲軸
      （捲 1.6 個螢幕寬；手機是 3.5 個）。
- [x] The document still has `scrollWidth == innerWidth` at 375px; no horizontal page scroll.
      375、1600 兩種視窗都實測過，頁面本身沒有橫向捲動。
- [x] Alt text and the full-description disclosure are untouched; this does not replace them.

## Steps

- [x] Choose an approach. **選了 `overflow-x-auto`**，也就是文章表格既有的那套：不需要 JS、
  沒有焦點管理、桌機手機一體適用。另一個選項（點開全幅檢視）最後還是得把圖畫到 1180px
  才讀得到，讀者一樣要捲，卻多一個彈層要維護。
  Tapping the figure to open the SVG at full size, or giving it
  the `overflow-x-auto` treatment the article tables already use with a minimum width,
  both fit the declared scope. Emitting a separate mobile SVG variant with larger type
  does not: that lives in the localization render pipeline and needs the scope widened
  to `tools/article-localization` and the asset directories, which other localization
  tasks currently hold.
- [x] ~~Implement it in `guide-image.tsx`~~ → **改在 `content-blocks.tsx`**，測試在
  `content-blocks.test.tsx`（三個案例：圖解進捲動盒、照片不進、不放大小於 1180 的圖）。
  `guide-image.tsx` 是封面與 hero 共用的重試 `<img>`，只多開放一個 `style` 屬性。
- [x] Check one diagram in each of the five locales. 用 `taiwan-convenience-store-guide`
  在正式站量了 en／ja／ko／zh-CN，加上 `seoul-seolleongtang-food-guide` 的 zh-TW：
  五個都是 1180×664、盒子可捲、頁面沒有橫向捲動。
  **這條原本的顧慮對這個做法不成立**：SVG 的文字是畫好的，等比例放大不會重排，
  所以英文能放下的版面，日文韓文也一樣放得下——會溢出的是重排型的做法。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
```

Then on a deployed build, at a 375x812 viewport, on
`/en/guides/howto/singapore-gardens-indoor-outdoor`:

- `document.documentElement.scrollWidth` equals `window.innerWidth` (375).
- No element inside `main` has a bounding rect extending past the viewport.
- Every `<text>` in the diagram resolves to at least 11 CSS pixels, or is reachable at
  that size through whatever affordance the fix adds.

## Notes

- Measured live on 2026-09-21 with the in-app browser at 375x812. The article page
  itself was clean: no viewport widening, zero overflowing elements, hero and diagram
  both at 335px, largest font 30px on the H1. The only defect was diagram type size.
- A first screenshot showed the diagram area blank. That was `loading="lazy"` not yet
  painted, not a missing asset. All five locale SVGs return 200 with valid markup, and
  the English one reports `naturalWidth` 1600 once loaded. Scroll it into view and wait
  before judging a diagram screenshot.
- The SVG carries its own opaque background (`<rect width="1600" height="900"
  fill="#f4f0e5">`) and fixed hex fills, with no `prefers-color-scheme`, `currentColor`
  or CSS variables. It therefore renders as a light card on the dark theme, which is
  legible but means a future dark-mode diagram treatment has no hook to work with.
- Separate small inconsistency found while measuring, not covered by this task: the
  English SVG's internal `<title>` still reads `Singapore’s` with a typographic
  apostrophe, which PR #605 replaced everywhere else in that article. It is not
  rendered, because the SVG is loaded through `<img>`, but it is inconsistent and tools
  that parse the SVG will read the old character.

## 做法與取捨（2026-09-21）

改在 `content-blocks.tsx` 的 image block，不是原本寫的 `guide-image.tsx`——後者是所有圖
共用的重試 `<img>`，封面與 hero 也在用，動它會波及不該動的地方。

圖解（`.svg`）現在包在自己的 `overflow-x-auto` 盒子裡，寬度 `min(內容包寫的寬度, 1180)`。
1180 的由來：`pack_ingest.MIN_LABEL_PX` 是 15，`15 × 1180/1600 = 11.1px`，
低於 11px 左右中文與韓文的字就糊掉。照片（`.webp` 等）維持貼齊欄寬，因為它的細節不在小字裡。

**三個實作上的坑**

1. **`max-width` 必須寫成行內樣式，不能只給 `max-w-none` 類別。** Tailwind 的 preflight 有
   `img { max-width: 100% }`，會把 1180px 直接吃掉；而只有這一個分支用得到的工具類別，
   隨時可能沒被掃進輸出的樣式表。第一次實測就是這樣失敗的：寬度設了，量出來還是 335px。
2. **盒子要 `tabIndex={0}`。** 裡面沒有可聚焦的元素，而只有 Firefox 會自動讓捲動容器可聚焦，
   鍵盤使用者否則捲不動它。
3. **盒子刻意不給 `aria-label`。** 圖片自己有 alt，替盒子命名會讓螢幕閱讀器把同一句唸兩次。

**代價，明講**：圖變成 1180×664，手機上大約佔掉八成螢幕高度（原本 189px）。
這是可讀的必然代價——要讓 15px 的字到 11px，圖就得有 1180px 寬，高度跟著等比例長。
橫向要滑 3.5 個螢幕寬（桌機 1.6 個）。捲動條本身就是「可以滑」的提示。

**沒有做的**：桌機視窗其實左右各有 800px 以上的空白，讓圖突破欄寬會更好。
但可靠的做法要用 `100vw`，那會把捲動條寬度算進去而撐出整頁的橫向捲動，
正好違反這張票自己的第三條。要做就得另外用媒體查詢寫死斷點，值得另開一張票再評估。
