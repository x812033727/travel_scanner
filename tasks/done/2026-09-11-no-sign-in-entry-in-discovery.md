---
id: 2026-09-11-no-sign-in-entry-in-discovery
title: 探索模式開啟時全站沒有登入入口
status: done
priority: P0
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T08:19:37Z
created_at: 2026-09-11T03:20:23Z
completed_at: 2026-09-11T09:16:26Z
branch: claude/google-apple-line-login-0fmfi5
depends_on: []
scope:
  - apps/web/components/site-navigation.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/site-navigation.test.tsx
  - apps/web/components/mobile-nav.test.tsx
---

# 探索模式開啟時全站沒有登入入口

## Why

線上 `GET /discovery/status` 回傳 `{"enabled": true}`。在這個模式下，桌面版與手機版的頁首都**沒有任何登入或登出按鈕**。

- `site-navigation.tsx:38`：`{!discovery.enabled && !discovery.loading && <><TextSizeSwitcher /><ThemeSwitcher /><HeaderAuth /></>}`。`HeaderAuth`（`header-auth.tsx:16,20`）是全站唯一的登入／登出鈕，`discovery.enabled` 為 true 時整組不渲染——連文字大小與主題切換也一起消失。
- `mobile-nav.tsx:65-69`：discovery 分支提前 return，只給語言切換、`/explore`、`/my` 三顆圖示，沒有選單鈕、沒有登入鈕。

結果：未登入訪客想登入，必須先點「我的」，在 `community/home.tsx:44` 的連結網格裡找到「登入」。兩跳，而且沒有任何視覺提示告訴他為什麼要先去「我的」。已登入者要登出同樣得先進 `/my`（`community/home.tsx:49`）。

對照 `lib/nav-links.ts:3-4` 自己寫的原則：*「One list for every navigation surface. The desktop header, the mobile menu sheet and the bottom tab bar must never disagree about what this site has.」* 登入狀態就是這個原則漏掉的一項。

順帶一提，`mobile-nav.tsx:109-113` 有兩段被 `discovery.enabled &&` 包住的程式碼，但 `:37` 的 `open` 條件要求 `!discovery.enabled`——這兩段永遠不會執行，是死碼。

## Definition of done

- [x] 探索模式下，未登入訪客在桌面與手機的頁首都看得到登入入口。
- [x] 已登入者在兩種尺寸都能一眼看到自己的登入狀態，並能登出。
- [x] `mobile-nav.tsx:109-113` 的死碼移除或修正條件。

## Steps

- [x] `site-navigation.tsx:38`：把 `HeaderAuth` 從 `!discovery.enabled` 的條件裡拿出來，讓它在兩種模式都渲染。`TextSizeSwitcher` 與 `ThemeSwitcher` 一併保留——它們消失的原因與 `HeaderAuth` 相同，而探索模式目前只能在 `/my` 調整字級與主題。現在的條件只剩 `!discovery.loading`。
- [x] `mobile-nav.tsx:65-69`：discovery 分支補上登入／帳號圖示，行為與非 discovery 分支一致（未登入 → `/login` + `LogIn`，已登入 → `/account` + `CircleUserRound`）。
- [x] 移除 `:109-113` 的死碼，連帶移除因此變成未使用的 `discoveryCopy` 與 `getDiscoveryCopy` import。
- [x] 加測試釘住：`site-navigation.test.tsx` 與 `mobile-nav.test.tsx` 各補案例，已確認在修好前會失敗、修好後會通過。

## How to verify

```bash
cd apps/web && npm run test:web -- site-navigation mobile-nav
cd apps/web && npx playwright test e2e/navigation.spec.ts
```

手動：登出後開 `https://mokaair.com/zh-TW`，桌面與手機寬度都應在頁首看到登入入口。

## Notes

- 這是**線上正在發生**的狀態，不是潛在問題：discovery 已開啟。本次直接確認過
  `GET https://mokaair.com/api/travel/discovery/status` 回傳 `{"enabled":true}`。

### 寫測試時踩到的坑（留給下一個人）

`useDiscoveryStatus`（`lib/discovery.ts`）把 `status`、`checkedAt`、`request` 放在
**模組層級**當單例快取，30 秒內不會重新問。同一個測試檔裡先跑過的案例會把答案留給
後面的案例，所以 `site-navigation.test.tsx` 新增的案例一開始「不改程式也會過」——
它讀到的是前一個案例快取的 `enabled:false`。

處理方式：那個案例放在 describe 的**最後**，並用
`vi.spyOn(Date, "now").mockImplementation(() => realNow() + 60_000)` 把快取推成過期，
逼它重新抓一次。回傳的 `enabled:true` 會留在快取裡，所以它不能放在別的案例前面。
`mobile-nav.test.tsx` 沒有這個問題，因為它整個檔案 `vi.mock("@/lib/discovery")`。

（`discovery-navigation.test.tsx` 其實是更自然的落點，它已經 mock 好 discovery，
但目前被 `2026-09-09-frontend-flow-discovery-web`（review）佔住 scope，沒有動。）

### 一併看到、但沒有動的事

- `mobile-nav.tsx` 選單內 `{... !discovery.enabled ? [["/my","my"]] : []}` 也是永遠成立
  的條件：整個選單只在 `!discovery.enabled` 時才打得開。留著沒有壞處，但下一個改這
  個檔案的人可以順手拿掉。
- `site-navigation.tsx:29-34` 的 `community.flags.enabled && !discovery.enabled` 分支
  只渲染六個連結，會讓桌面版失去 `primaryNavLinks`。目前線上走不到（discovery 優先），
  原任務已記錄，本次維持原狀。
- `site-navigation.tsx:29-34` 還有另一條分支（`community.flags.enabled` 為 true 但 discovery 為 false）只渲染六個連結，會讓桌面版失去 `primaryNavLinks` 的所有項目，而手機選單（`mobile-nav.tsx:115-117`）有。那是同一類的漂移，但目前線上走不到（discovery 優先），所以沒有納入本任務——若之後關掉 discovery，要一併檢查。
