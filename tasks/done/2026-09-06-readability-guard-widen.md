---
id: 2026-09-06-readability-guard-widen
title: e2e 只守住預設字級的六個頁面，守不住大字模式與 320px
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T19:35:05Z
created_at: 2026-09-06T19:35:04Z
completed_at: 2026-09-06T20:11:50Z
branch: claude/ux-guards
depends_on: []
scope:
  - apps/web/e2e/readability.spec.ts
  - .github/workflows/ci.yml
---

# e2e 只守住預設字級的六個頁面，守不住大字模式與 320px

## Why

`e2e/readability.spec.ts` 是 2026-09-06 那輪加的，只做兩件事：預設字級下六個頁面沒有
小於 13px 的字、沒有自己有底色卻低於 4.5:1 的元件。可是這一輪修掉的問題有一半它抓不到：

- 大字模式（root 20px）會把每一個 rem 放大，寫死寬度的版面只有在那時候才會露餡。
- 手機主選單被標題列的 `backdrop-filter` 關在 68px 裡——DOM 在、`toBeVisible()` 也過，
  錯的是位置。
- 選單關掉之後焦點掉回 `<body>`。

這三個都復發得了，而且復發時不會有任何測試變紅。

## Definition of done

- [x] 大字模式 × 320px × 五個頁面：`data-text-size` 在第一次繪製前就是 `largest`、
      root 字級 20px、文件不會橫向捲、沒有元素超出畫面（橫向捲軸內的子元素除外）。
- [x] 手機選單：遮罩貼滿整個畫面、sheet 貼齊底部、掛在 `document.body` 上。
- [x] 選單關閉後焦點回到開啟它的按鈕。
- [x] 這些都跟著既有的 readability spec 一起在 CI 跑。

## How to verify

```bash
cd apps/web && npx playwright test e2e/readability.spec.ts   # 28 passed（兩個 project）
```

## Notes

判斷「超出畫面」時要往上走一遍祖先，只要有任何一層是 `overflow-x: auto/scroll` 就跳過——
橫向膠囊列的子元素本來就會比畫面寬，那不是 bug。之前手寫的稽核腳本沒做這件事，報表裡
一半是這種誤判。
