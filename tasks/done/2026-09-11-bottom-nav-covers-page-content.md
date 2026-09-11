---
id: 2026-09-11-bottom-nav-covers-page-content
title: 登入頁的送出鈕在手機上要捲一下才看得到
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T18:56:47Z
created_at: 2026-09-11T13:05:03Z
completed_at: 2026-09-11T19:02:07Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/app/globals.css
  - apps/web/components/app-bottom-nav.tsx
  - apps/web/app/[locale]/login/page.tsx
  - apps/web/e2e/readability.spec.ts
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

- [x] `/login` 在 390×844 下，送出鈕不需捲動就看得見。
- [x] 桌面版不受影響。

## Steps

- [x] 收斂 `/login` 首屏的垂直用量：`py-14` 在手機上可以小一點，或讓「只開放既有會員」的說明卡更精簡。
- [x] 只動這一頁，不要改 `.public-app-shell` 的保留量——那個目前是對的，動了會影響全站。

## How to verify

```bash
cd apps/web && npx playwright test --project="Pixel 7"
```

斷言：390×844 視窗開啟 `/zh-TW/login`，不捲動時送出鈕的矩形完全在視窗內。

## Notes

- `apps/web/app/[locale]/login/page.tsx` 目前也在 `2026-09-10-seo-index-directives` 的 scope 裡（`claude-opus-5-seo`，review 中），所以這張任務暫時 claim 不動。等那張結束再認領。
- 教訓記在這裡：凡是牽涉固定定位元素的遮擋判定，都必須在**捲到底**的狀態下再量一次，否則會把「首屏之外」誤報成「無法觸及」。

## 完成紀錄（claude-opus-5, 2026-09-11）

### 先量，結果比任務寫的更細

390×844、扣掉底部導覽的 79px，有效首屏是 765px。送出鈕的下緣：

| 字級 | 修之前 | 修之後 |
| --- | --- | --- |
| standard | 727 | 543 |
| large | **885** | 678 |
| largest | **1030** | 753 |

所以「送出鈕在首屏之外」在**標準字級下其實不成立**（727 < 765，只差 38px），成立的是**放大與最大字級**——而那正是會去調字級的人，也是最不會去找一顆看不到的按鈕的人。任務原本沒有區分字級，這一點值得寫下來。

### 改了什麼

主要不是擠空間，是**改順序**：表單移到「只開放既有會員」那張說明卡**前面**。會走到這頁的人是來登入的，解釋為什麼暫停註冊可以放在按鈕後面。另外手機的 `py-14` → `py-8 md:py-14`、卡片 `p-8` → `p-6 md:p-8`。

沒有動 `.public-app-shell` 的 `padding-bottom`，照任務 Steps 的指示——那個保留量是對的。

### 驗證

`e2e/readability.spec.ts`（CI 有跑）加三個案例，三種字級各一個，斷言送出鈕下緣不超過「視窗高度減 80px」。把版面還原成原本的順序與內距之後，`largest` 那條變紅：

```
Error: sign in sits 791px down, past the 759px fold
```

（Playwright 的 mobile 專案是 Pixel 7、412×915，比 390×844 寬鬆，所以只有 largest 會紅；390×844 下 large 也會。）

寫測試時踩到一個東西值得記：`button[type=submit]` 選不到這顆按鈕——DOM 屬性 `type` 預設是 `"submit"`，但 HTML 上沒有那個 attribute，CSS 選擇器比對的是 attribute。改用 role + 名稱。
