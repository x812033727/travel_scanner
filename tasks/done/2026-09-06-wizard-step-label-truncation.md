---
id: 2026-09-06-wizard-step-label-truncation
title: 首頁精靈步驟標籤在英文 390px 會截字
status: done
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T07:55:01Z
created_at: 2026-09-06T00:54:03Z
completed_at: 2026-09-06T09:04:12Z
branch: claude/p3-polish
depends_on: []
scope:
  - apps/web/components/search-workbench.tsx
---

# 首頁精靈步驟標籤在英文 390px 會截字

## Why

步驟指示器是 `grid grid-cols-5 gap-1`，每顆藥丸 `px-1 text-xs`。390px 手機扣掉卡片
padding 後，每格約 66px 可用寬度。繁中的「目的地」放得下，英文的 `Destination`、
`Preferences` 與韓文的 `목적지`／`선호도` 放不下，正式站實測顯示成 `Destina…`／`Travelle…`。

2026-09-06 把這排從不可點的 `<li>` 改成真按鈕（已完成步驟可回頭），所以現在它是
**可操作元件**，標籤看不完整比純裝飾時更礙事。

## Definition of done

- [x] 390px 下五個語系的步驟標籤都完整可讀（不截字、不重疊）。
- [x] 已完成步驟仍可點回去、目前步驟仍帶 `aria-current="step"`、未來步驟仍 disabled。
- [x] 每顆仍 ≥ 44px 高。

## Steps

- [x] 三個方向擇一：
  - [x] 手機改成橫向可捲的一列（沿用 `globals.css` 既有的 `.app-chip-row`，
        它有 `scroll-snap` 與隱藏捲軸）；
  - [ ] 或手機只顯示序號 + 目前步驟名（「2 / 5 · Destination」），其餘用圓點；
  - [ ] 或縮短英韓的字串本身（`messages/*/search.json` 的 `workbench.steps.*`）。
        注意這樣要改的是文案不是版面，scope 要加 messages 檔案。
- [x] 三種都要保留「已完成可點回去」這個行為。

## How to verify

Playwright 390×844，`locale: "en"`，開 `/en`，對五顆藥丸各取
`scrollWidth > clientWidth` 應為 false；再跑一次 `ja`／`ko`。

```bash
cd apps/web && npx vitest run components/search-workbench.test.tsx
```

## Notes

**這個檔案 2026-09-06 大改過**（PR #160），接手前先讀：

- 整張精靈的字串搬到 `messages/*/search.json` 的 `workbench` 物件（77 鍵，五語系）。
  之前是寫死繁中 + 靠 `LegacyUiLocalizer` 的 54 筆字典補，補不到，
  所以英日韓看到的是「標題外文、欄位繁中」。
- 步驟藥丸從 `<li>` 改成 `<button>`：`index <= step` 可點，`aria-current="step"`，
  未來步驟 `disabled`，每顆 `min-h-11`。
- 切換步驟會把焦點移到該段的 `<h3>`（`tabIndex={-1}` + `focus()`），
  因為原本按下一步後再按 Tab 會直接跳出表單，第 2–5 步用鍵盤根本填不到。
  `scrollIntoView` 有 `?.` 保護 —— jsdom 沒有這個方法，拿掉會讓測試炸。
- 日期與天數的跨欄位驗證改成離開第 1 步時就跑（原本要走完五步、按送出才報，
  而且訊息用的詞和欄位標籤對不起來）。

改版面時不要把上面任何一項弄回去。

2026-09-06 claude-fable-5-1：選第一個方向。`<ol>` 在 `max-sm` 改成 flex 橫向捲動列（`snap-x`、隱藏捲軸、`-mx-1 px-1`、
`[contain:inline-size]`），`sm:` 以上維持 `grid-cols-5`；`<li>` `flex-none snap-start`，按鈕 `whitespace-nowrap px-3`。
沒直接套 `.app-chip-row`，因為它會把 chip 的圓角底色一起帶進來，步驟藥丸有自己的樣式。`contain: inline-size` 不能省：
沒有它，五顆 flex-none 會把 `<form>` 撐到 497px，整頁在 390px 手機變成 537px 寬、可以左右捲。
Playwright 390×844 en／ja／ko／zh-TW／zh-CN：五顆都不截字（`scrollWidth <= clientWidth`）、高 44、頁面寬 390 不橫捲，
`<ol>` 本身可捲到第五顆。`aria-current`／disabled／可點回去／焦點移到 `<h3>` 沒動。
