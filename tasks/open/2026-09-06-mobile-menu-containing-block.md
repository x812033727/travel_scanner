---
id: 2026-09-06-mobile-menu-containing-block
title: 手機主選單被標題列的 backdrop-filter 關在 68px 裡
status: review
priority: P0
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T14:10:00Z
created_at: 2026-09-06T14:09:00Z
completed_at:
branch: claude/ui-ux-simplification-72afb9
depends_on: []
scope:
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
---

# 手機主選單被標題列的 backdrop-filter 關在 68px 裡

## Why

線上 mokaair.com，手機 390×844 點右上角的 ☰：整個選單只露出最底下一列
（「方案」或「價格通知」，看語系），黏在畫面最上緣，其他全部在畫面外。等於
手機使用者沒有主選單——航班動態、航空票價、方案這三個頁面在手機上本來就只有
這個入口。

原因是 `position: fixed` 的包含塊。`.site-header` 有
`backdrop-filter: blur(20px) saturate(1.2)`，任何有 backdrop-filter 的祖先都會
變成後代 fixed 元素的包含塊，而 `MobileNav` 的遮罩與 sheet 就長在 header 裡面。
量出來的結果：

```
overlay  top=0  bottom=68   (應該是 0..844)
dialog   top=-236 bottom=68 (應該貼齊畫面底部)
header   top=0  bottom=69
```

## Definition of done

- [x] 手機點 ☰ 會從畫面底部升起完整的 sheet，遮罩蓋滿整個畫面。
- [x] 有一個測試會在 sheet 又被關回 header 裡時失敗。

## Steps

- [x] 用 `createPortal` 把遮罩與 sheet 掛到 `document.body`。
- [x] 量測 overlay／dialog 的 bounding box 確認貼齊 viewport。

## Notes

- `open` 一開始是 false，sheet 只在使用者點擊之後才渲染，所以 `createPortal`
  不會在 SSR 執行，不需要 mounted 旗標。
- 這類 bug 只有量幾何才看得出來：DOM 在、`toBeVisible()` 也過，是位置錯。
  scratchpad 的 `menu_geom.mjs` 會把 overlay／dialog／header 的 box 與造成包含塊的
  祖先一起印出來，之後檢查其他 fixed 覆蓋層可以照抄。
- 同一個站上其他 `fixed inset-0` 的覆蓋層（景點詳情、附近用餐、後台側邊欄）都不在
  header 底下，量過沒有這個問題。
