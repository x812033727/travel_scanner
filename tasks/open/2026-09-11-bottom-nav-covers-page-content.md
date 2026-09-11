---
id: 2026-09-11-bottom-nav-covers-page-content
title: 登入頁的送出鈕在手機上要捲一下才看得到
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T13:05:03Z
completed_at:
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/app/globals.css
  - apps/web/components/app-bottom-nav.tsx
  - apps/web/app/[locale]/login/page.tsx
---

# 登入頁的送出鈕在手機上要捲一下才看得到

## 更正在先：原始版本嚴重高估

這張任務原本標為 **P0**，主張「有底部固定列的 79 個手機頁面裡 56 個（71%）有可互動元素被蓋住，包括 `/login` 的送出鈕」。

**那是量測方法的缺陷。** 原本的判定是「**捲動位置 0 時**元素矩形與導覽列相交」，但那些元素捲一下就到得了。實測十條路由、捲到底之後再量：

```
路由        捲動前被蓋  捲到底後仍被蓋
/login          2             0
/about          3             0
/privacy        3             0
/terms          3             0
/contact        3             0
/hotspots       4             0
/foods          3             0
/               0             0
/explore        0             0
/my             1             0
```

**沒有任何一個頁面有元素是碰不到的。** `.public-app-shell` 的 `padding-bottom: calc(5rem + env(safe-area-inset-bottom))`（80px）對上導覽列的 69px 高加 10px 離底（合計 79px），保留是夠的。

## 真正剩下的問題

`/login` 在 390×844 的手機上，送出鈕落在首屏之外，要捲一下才看得到。原因是表單上方堆了較多內容：`<main className="… py-14">` 的上下內距、歡迎語、標題，以及「現在只開放給既有會員」那張說明卡。

這是第一印象的問題，不是無法使用——一個想登入的人第一眼看不到登入按鈕。值得改，但不急。

## Definition of done

- [ ] `/login` 在 390×844 下，送出鈕不需捲動就看得見。
- [ ] 桌面版不受影響。

## Steps

- [ ] 收斂 `/login` 首屏的垂直用量：`py-14` 在手機上可以小一點，或讓「只開放既有會員」的說明卡更精簡。
- [ ] 只動這一頁，不要改 `.public-app-shell` 的保留量——那個目前是對的，動了會影響全站。

## How to verify

```bash
cd apps/web && npx playwright test --project="Pixel 7"
```

斷言：390×844 視窗開啟 `/zh-TW/login`，不捲動時送出鈕的矩形完全在視窗內。

## Notes

- `apps/web/app/[locale]/login/page.tsx` 目前也在 `2026-09-10-seo-index-directives` 的 scope 裡（`claude-opus-5-seo`，review 中），所以這張任務暫時 claim 不動。等那張結束再認領。
- 教訓記在這裡：凡是牽涉固定定位元素的遮擋判定，都必須在**捲到底**的狀態下再量一次，否則會把「首屏之外」誤報成「無法觸及」。
