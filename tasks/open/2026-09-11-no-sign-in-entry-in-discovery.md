---
id: 2026-09-11-no-sign-in-entry-in-discovery
title: 登入入口只存在於我的頁底部且未登入者毫無說明
status: open
priority: P0
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:20:23Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/site-navigation.tsx
  - apps/web/components/mobile-nav.tsx
---

# 登入入口只存在於我的頁底部且未登入者毫無說明

## Why

線上 `GET /discovery/status` 回傳 `{"enabled": true}`。在這個模式下，桌面版與手機版的頁首都**沒有任何登入或登出按鈕**。

- `site-navigation.tsx:38`：`{!discovery.enabled && !discovery.loading && <><TextSizeSwitcher /><ThemeSwitcher /><HeaderAuth /></>}`。`HeaderAuth`（`header-auth.tsx:16,20`）是全站唯一的登入／登出鈕，`discovery.enabled` 為 true 時整組不渲染——連文字大小與主題切換也一起消失。
- `mobile-nav.tsx:65-69`：discovery 分支提前 return，只給語言切換、`/explore`、`/my` 三顆圖示，沒有選單鈕、沒有登入鈕。

結果：未登入訪客想登入，必須先點「我的」，在 `community/home.tsx:44` 的連結網格裡找到「登入」。兩跳，而且沒有任何視覺提示告訴他為什麼要先去「我的」。已登入者要登出同樣得先進 `/my`（`community/home.tsx:49`）。

對照 `lib/nav-links.ts:3-4` 自己寫的原則：*「One list for every navigation surface. The desktop header, the mobile menu sheet and the bottom tab bar must never disagree about what this site has.」* 登入狀態就是這個原則漏掉的一項。

順帶一提，`mobile-nav.tsx:109-113` 有兩段被 `discovery.enabled &&` 包住的程式碼，但 `:37` 的 `open` 條件要求 `!discovery.enabled`——這兩段永遠不會執行，是死碼。

## Definition of done

- [ ] 探索模式下，未登入訪客在桌面與手機的頁首都看得到登入入口。
- [ ] 已登入者在兩種尺寸都能一眼看到自己的登入狀態，並能登出。
- [ ] `mobile-nav.tsx:109-113` 的死碼移除或修正條件。

## Steps

- [ ] `site-navigation.tsx:38`：把 `HeaderAuth` 從 `!discovery.enabled` 的條件裡拿出來，讓它在兩種模式都渲染。順便決定 `TextSizeSwitcher` 與 `ThemeSwitcher` 是否也該保留（探索模式目前只能在 `/my` 調整）。
- [ ] `mobile-nav.tsx:65-69`：discovery 分支補上登入／帳號圖示，行為與 `:78` 的非 discovery 分支一致（未登入 → `/login`，已登入 → `/account`）。
- [ ] 移除 `:109-113` 的死碼。
- [ ] 加測試釘住：`discovery.enabled` 為 true 且未登入時，頁首必須有 `/login` 連結。

## How to verify

```bash
cd apps/web && npm run test:web -- site-navigation mobile-nav
cd apps/web && npx playwright test e2e/navigation.spec.ts
```

手動：登出後開 `https://mokaair.com/zh-TW`，桌面與手機寬度都應在頁首看到登入入口。

## Notes

- 這是**線上正在發生**的狀態，不是潛在問題：discovery 已開啟。
- `site-navigation.tsx:29-34` 還有另一條分支（`community.flags.enabled` 為 true 但 discovery 為 false）只渲染六個連結，會讓桌面版失去 `primaryNavLinks` 的所有項目，而手機選單（`mobile-nav.tsx:115-117`）有。那是同一類的漂移，但目前線上走不到（discovery 優先），所以沒有納入本任務——若之後關掉 discovery，要一併檢查。

## 瀏覽器實測補充（2026-09-11 第二輪）

用真實瀏覽器量測後，這張任務的**內容成立，但原標題「全站沒有登入入口」過強**——入口存在，只是埋得很深。實際情形：

- **頁首（手機與桌面）確實沒有任何登入／登出控制。** 手機頁首只有 Logo、語言、搜尋、人像四個元素；桌面是 Logo、探索、收藏、我的旅程、我的。**未登入與已登入的頁首完全相同**，所以已登入者也看不出自己登入了。
- 底部導覽列有四項（探索／收藏／我的旅程／我的），人像與「我的」都指向 `/my`。
- **`/my` 對未登入者只列出「我的收藏／我的旅行／發佈／公開個人頁／公開身分設定」等個人功能，沒有任何一句話說明需要先登入**，而「登入」是清單最後一項，在摺線下方。
- 更糟的是：「登入」在 7 條路由上被固定底部導覽列實體遮住（見 `2026-09-11-bottom-nav-covers-page-content`）。

所以完整修法是三件事：頁首補登入／帳號狀態、`/my` 未登入時給說明並把登入提前、底部列不要蓋住它。

