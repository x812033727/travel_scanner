---
id: 2026-09-06-auth-dead-end
title: 沒有帳號的人走到底是死路：註冊已關閉，但每道牆只寫「前往登入」
status: in-progress
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T21:06:28Z
created_at: 2026-09-06T21:06:27Z
completed_at:
branch: claude/ux-auth-walls
depends_on: []
scope:
  - apps/web/components/auth-form.tsx
  - apps/web/components/auth-form.test.tsx
  - apps/web/app/[locale]/login/page.tsx
  - apps/web/messages/en/auth.json
  - apps/web/messages/ja/auth.json
  - apps/web/messages/ko/auth.json
  - apps/web/messages/zh-CN/auth.json
  - apps/web/messages/zh-TW/auth.json
---

# 沒有帳號的人走到底是死路：註冊已關閉，但每道牆只寫「前往登入」

## Why

線上 `/api/travel/auth/registration-status` 回的是 `{"registration_enabled": false}`。
可是每一道登入牆（`/trips`、`/alerts`、`/account`、景點卡上的鎖頭）都只寫
「登入後才能查看這裡的內容 ／ 前往登入」。第一次來的人照著按，走到 `/login`，
表單底下才用 14px 的灰字寫一句「目前暫停開放註冊」——他跑完整段路才知道自己根本
進不來。

第二件事在同一張表單上：密碼欄的 `minLength={10}` 是**登入與註冊共用**的。密碼比
十個字短的既有會員（規則上線前註冊的、或用 Google／LINE 綁定後設過短密碼的）按下
「登入」時，瀏覽器會擋下送出、只彈一個原生提示，在手機上很容易被當成「這顆按鈕壞了」。
那條規則屬於註冊，不屬於登入。

## Definition of done

- [x] 註冊關閉時，`/login` 在表單**上面**就說清楚「現在只開放給既有會員」，不是表單底下的灰字。
- [x] 登入表單不再套用註冊的密碼長度規則，也不再顯示「至少 10 個字元」。
- [x] 註冊表單維持原本的規則與提示。

## How to verify

```bash
cd apps/web && npx vitest run components/auth-form   # 4 passed
```

線上要重現原本的死路：`/zh-TW/trips` →「前往登入」→ `/zh-TW/login`，看表單底下那句灰字。

## Notes

註冊本身是不是要開放，是產品決定，不是這張任務要改的；這裡只讓畫面誠實地把狀態
講在讀者需要知道的時候。如果之後開放註冊，`/login` 會自動回到原本「還沒有帳號？免費註冊」
那句，不需要再改程式。
