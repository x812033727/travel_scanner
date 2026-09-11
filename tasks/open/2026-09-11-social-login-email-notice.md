---
id: 2026-09-11-social-login-email-notice
title: 社群登入按鈕下方說明會取得 Email 與用途（LINE Email 權限申請要附這個畫面）
status: in-progress
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T17:17:17Z
created_at: 2026-09-11T17:17:15Z
completed_at:
branch: claude/social-login-email-notice
depends_on: []
scope:
  - apps/web/components/social-login-buttons.tsx
  - apps/web/components/social-login-buttons.test.tsx
  - apps/web/messages/en/auth.json
  - apps/web/messages/ja/auth.json
  - apps/web/messages/ko/auth.json
  - apps/web/messages/zh-CN/auth.json
  - apps/web/messages/zh-TW/auth.json
---

# 社群登入按鈕下方說明會取得 Email 與用途（LINE Email 權限申請要附這個畫面）

## Why

LINE Developers 申請「Email address permission」時要勾一句聲明（My app only collects a user's
email address after asking for their consent and explaining the purpose of collecting…），並上傳
「告訴使用者會取得 Email 以及用途」的畫面截圖。mokaair 的登入／註冊頁原本只有「使用 LINE
繼續」按鈕，沒有任何一句說明，所以那句聲明並不成立。

LINE 登入的程式要 `openid email`；用 LINE 建新帳號時如果沒有 Email，API 會回
`oauth_email_required`。所以 Email 權限是 LINE 開放新會員的前提，而這個畫面是申請的前提。

## Definition of done

- [x] 登入與註冊頁的社群登入按鈕下方有一句說明：用這些帳號繼續時，會取得該帳號的 Email，
      用來建立並辨識 Mokaair 帳號。五個語系都有。
- [x] 沒有任何社群登入可用時，這句話跟按鈕一起不出現。
- [x] 不寫政策性的承諾（例如「不會用於其他用途」）：那要等
      `2026-09-06-legal-content-from-owner` 由站主決定。

## Steps

- [x] `auth.json` 五個語系加 `socialEmailNotice`。
- [x] `social-login-buttons.tsx` 把它放在按鈕與「或使用 Email」分隔線之間。
- [x] 新增 `social-login-buttons.test.tsx`。

## How to verify

```bash
npm run check:i18n && npm run test:web -- components/social-login-buttons
```

部署後開 `https://mokaair.com/zh-TW/login`，社群登入按鈕下方應該出現那句說明。

## Notes

- 文字刻意不寫「只取得 Email」：程式實際會收到 Email 和該服務的帳號識別碼（`sub`），寫「只」
  就不精確。
- 截圖由站主上傳：瀏覽器工具沒辦法代傳檔案，勾選那兩句聲明也應該由站主本人做。
- 查核 LINE 規則時確認過的事（2026-09-12）：官方文件沒寫 Email 權限的審核時間，唯一的第一手
  紀錄（2018）是按下 Apply 立刻變 Applied；「一到兩個工作天」查不到出處。頻道在 Developing 時
  只有 Admin／Tester 能登入，發布後無法改回。
- LINE Login 頻道 `mokaair`（Channel ID 2011565306，provider `mokaair`／2005531077）已於
  2026-09-12 由站主同意後發布為 Published。價格通知用的 Messaging API 頻道不在這個 provider 底下，
  但通知綁定走 Messaging API 的 account link（`apps/api/app/line/router.py`），不依賴登入的 `sub`，
  所以兩者不同 provider 不影響現有功能。
