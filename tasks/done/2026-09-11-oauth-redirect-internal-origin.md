---
id: 2026-09-11-oauth-redirect-internal-origin
title: OAuth 回跳導向容器內部位址 0.0.0.0:3000，Google 登入最後必定落在錯誤頁
status: done
priority: P0
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T16:27:35Z
created_at: 2026-09-11T16:27:16Z
completed_at: 2026-09-11T16:37:36Z
branch: claude/google-oauth-setup-bd4f94
depends_on: []
scope:
  - apps/web/app/api/auth/oauth
---

# OAuth 回跳導向容器內部位址 0.0.0.0:3000，Google 登入最後必定落在錯誤頁

## Why

BFF 的 OAuth 路由用 `request.nextUrl.origin`／`request.url` 組回跳網址。Next.js standalone
在容器裡綁 `0.0.0.0:3000`，經過反向代理後這個 origin 就是 `https://0.0.0.0:3000`，所以
callback 的成功與失敗回跳、start 的失敗回跳，全都把瀏覽器送到 `https://0.0.0.0:3000/...`，
Chrome 顯示 `ERR_ADDRESS_INVALID`。

2026-09-12 使用者第一次實測 Google 登入就撞到（當時是 `oauth_error=oauth_account_exists`）。
成功登入時 `travel_access` 其實已經設在 mokaair.com，只是畫面停在錯誤頁，看起來像登入失敗。
測試沒抓到，是因為既有測試的請求網址都寫成 `https://mokaair.com/...`。

不用登入就能重現：

```bash
curl -sS -o /dev/null -D - "https://mokaair.com/api/auth/oauth/google/callback?state=bogus&code=bogus" | grep -i '^location'
# 修好前：location: https://0.0.0.0:3000/zh-TW/login?oauth_error=oauth_state_invalid&next=%2F
```

## Definition of done

- [x] callback 的成功、失敗回跳，以及 start 的失敗回跳，都落在 `NEXT_PUBLIC_SITE_URL`
      （正式站就是 `https://mokaair.com`），不再看請求自己的 origin。
- [x] 單元測試用 `https://0.0.0.0:3000` 當請求位址，證明回跳不會帶出內部位址。

## Steps

- [x] `_shared.ts` 新增 `siteRedirectUrl()`，以 `@/lib/seo` 的 `siteUrl` 為基底；
      `errorRedirect` 與成功回跳改用它。
- [x] `[provider]/start/route.ts` 兩個錯誤回跳改用它。
- [x] 補測試：`_shared.test.ts` 的成功／失敗回跳、新的 `[provider]/start/route.test.ts`。

## How to verify

```bash
npm run test:web -- app/api/auth/oauth
```

部署後（同一個 session 在合併後部署並回報於 PR）：

```bash
curl -sS -o /dev/null -D - "https://mokaair.com/api/auth/oauth/google/callback?state=bogus&code=bogus" | grep -i '^location'
# 期望：location: https://mokaair.com/zh-TW/login?oauth_error=oauth_state_invalid&next=%2F
```

再實際走一次 Google 登入，應該回到網站而不是 `ERR_ADDRESS_INVALID`。

## Notes

- 用 `siteUrl` 而不是從 `X-Forwarded-Host` 推 origin：API 的 `redirect_uri` 本來就只取
  `NEXT_PUBLIC_SITE_URL`，flow cookie 又是 host-only，單一 origin 是既有的硬需求（見
  `docs/social-login.md`）。從標頭推 origin 反而會讓回跳跟著偽造的 Host 走。
- 同一天 Google Cloud Console 的設定也修好了（專案 `server-241609`，專案編號 854167334118）：
  用戶端「Mokaair」的重新導向 URI 原本只有 `https://mokaair.com/`，Google 對正式 callback
  一律回 `redirect_uri_mismatch`，已改成正式 callback；同意畫面名稱從「Translate」改成
  「Mokaair」，補上首頁與隱私權網址，並從「測試」發布為「實際運作中」。
- 品牌還沒驗證，所以同意畫面暫時不會顯示 Mokaair 的名稱。送品牌驗證要等
  `2026-09-06-legal-content-from-owner` 把真的隱私權政策寫出來——現在 `/privacy` 還是待補頁，
  卻已經掛在 Google 同意畫面上。
- `oauth_account_exists` 是設計：同一個信箱已經有密碼帳號時不會自動合併，要先用密碼登入，
  再到帳號頁綁定 Google。
