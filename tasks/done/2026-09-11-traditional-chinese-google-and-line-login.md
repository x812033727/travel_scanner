---
id: 2026-09-11-traditional-chinese-google-and-line-login
title: Traditional Chinese Google and LINE login setup guide
status: done
priority: P1
area: docs
owner: claude-opus-5
claimed_at: 2026-09-11T08:53:51Z
created_at: 2026-09-11T08:53:48Z
completed_at: 2026-09-11T09:16:26Z
branch: claude/google-apple-line-login-0fmfi5
depends_on: []
scope:
  - docs/social-login-setup.zh-TW.md
  - docs/social-login.md
---

# Traditional Chinese Google and LINE login setup guide

## Why

Google / LINE / Apple 登入的程式碼在 `apps/api/app/auth/oauth.py`、
`apps/web/app/api/auth/oauth/`、`apps/web/components/social-login-buttons.tsx`
已經完整實作並上線，但線上三家都沒有憑證：

```bash
curl -s https://mokaair.com/api/travel/auth/oauth/providers
# {"providers":{"google":false,"line":false,"apple":false}}
```

`provider_enabled()`（`oauth.py:60`）要求「已啟用且憑證齊全」，
`social-login-buttons.tsx:47` 只渲染回傳 true 的供應商，所以登入頁一顆按鈕都沒有。

缺的是**設定**，而設定要站長本人拿他的 Google / LINE 開發者帳號去申請。
既有的 `docs/social-login.md` 是英文、寫給開發者看設計決策的參考文件，
不是拿著照做的操作手冊。

## Definition of done

- [x] 站長可以照著一份中文文件，從零申請到 Google 與 LINE 憑證並成功開通。
- [x] 文件講清楚三條會實際擋住使用者的規則（首次註冊需已驗證 Email、
      同 Email 不自動合併、管理員信箱保留）。
- [x] 文件包含「設定了卻還是 false」的排查清單，涵蓋實際會踩到的陷阱。
- [x] 英文版有一行指向中文手冊，兩份文件的分工說清楚。

## Steps

- [x] 新增 `docs/social-login-setup.zh-TW.md`。
- [x] `docs/social-login.md` 頂端加交叉連結。
- [ ] （交接）`README.md:340-343` 那段補一句指向中文手冊。

## How to verify

```bash
npm run check:tasks
```

文件本身沒有程式碼可跑。內容的正確性是逐條對著原始碼查證的，對應位置寫在文件裡：
`oauth.py:60`（啟用判斷）、`:88`（callback 由 `NEXT_PUBLIC_SITE_URL` 產生）、
`:151`（scope 只有 `openid email`）、`:435`（首次註冊需已驗證 Email）、
`:437`（同 Email 不合併）、`:447`（管理員信箱保留）、
`admin/service.py:539-543`（關掉的那列會清空 secret）、
`admin/service.py:1722-1737`（測試連線只碰公開 metadata）、
`start/route.ts:52-69`（流程 cookie 是 host-only）。

## Notes

### README.md 沒有動，是故意的

`README.md` 同時被 `2026-09-10-seo-audit-followups` 與 `2026-09-11-pr388-seo-review`
兩個 `review` 狀態的任務佔住 scope（`tools/tasks.mjs:32` 的 `HOLDS_SCOPE`）。
把它放進這個任務的 scope 會讓 claim 被拒絕，所以留給那兩個任務合併後再補一句。

### 文件裡最值得記住的一條

`apply_runtime_overrides`（`admin/service.py:539-543`）裡，資料庫那一列的 `enabled`
會**雙向覆蓋**環境變數，而且只要那列是關的，它會把該供應商所有 secret 欄位設成
`None`——包含 `.env` 裡填好的值。「在 .env 設好了卻還是 false」最常見的原因就是
後台留著一列關掉的 row。這一條沒寫在任何地方會讓人找很久。

### 測試連線的實際效力

Google 與 LINE 的「測試連線」只抓供應商的公開 OpenID metadata，
**client id / secret 填錯一樣會過**。只有 Apple 會真的簽一份 ES256 client secret，
所以只有 Apple 的測試抓得到憑證問題。文件裡有寫清楚，避免站長以為綠燈就是好了。
