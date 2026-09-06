---
id: 2026-09-06-social-login-launch-prep
title: 社群登入上線前置：正式主機收斂與 Apple 網域驗證檔
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-06T14:28:10Z
created_at: 2026-09-06T14:27:57Z
completed_at: 2026-09-06T14:31:31Z
branch: claude/google-apple-login-system-8a2465
depends_on: []
scope:
  - docs/social-login.md
  - apps/web/public/.well-known
---

# 社群登入上線前置：正式主機收斂與 Apple 網域驗證檔

## Why

Google / LINE / Apple 登入在 PR #85 就整套做完了，正式站也部署了，但三家憑證
從來沒填過：`/auth/oauth/providers` 目前回傳全 false，所以登入頁一顆社群按鈕
都沒有。要開通時會先撞到兩個 `docs/social-login.md` 沒寫到的坑：

1. 網站必須只在單一 origin 上應答。`redirect_uri` 只會來自單一的
   `NEXT_PUBLIC_SITE_URL`，而 BFF 寫的 flow cookie 沒有 `Domain` 屬性、是
   host-only，所以任何從非正式主機出發的登入都會在 callback 找不到 cookie，
   永遠卡在 `oauth_state_invalid`；在兩家主控台各填一組 callback URL 救不了。
   這項要求目前是滿足的（`www` 有路徑保留的 nginx 301），但文件完全沒寫，
   所以未來改動代理設定的人不會知道自己踩到了什麼。
2. Apple 要求網域驗證檔放在 `/.well-known/`，但 `apps/web/public/` 底下沒有這個
   目錄，文件也沒說要放哪。

## Definition of done

- [x] `docs/social-login.md` 寫清楚正式主機必須收斂成單一 origin，以及為什麼註冊
      兩組 callback URL 沒有用
- [x] `docs/social-login.md` 寫清楚 Apple 網域驗證檔的存放路徑與驗證指令
- [x] `docs/social-login.md` 寫清楚「測試連線」通過不等於憑證正確，以及停用的設定
      列會把環境變數的秘密一起蓋成 null

## Steps

- [x] 查證 www/apex 現況並確認 cookie 與 redirect_uri 的失敗鏈
- [x] 查證 `apps/web/public/` 沒有 `.well-known/`，並確認路由與打包不會擋這個路徑
- [x] 補上 `docs/social-login.md` 三個段落

這張任務的 repo 範圍到此結束。以下兩件事無法在 repo 內完成，由網站營運者依
`docs/social-login.md` 執行，不屬於本任務的 definition of done：

- 維持非正式主機 → 正式主機的 301（設定檔不在這個 repo 裡；目前已存在，
  改動邊緣代理後要用下面的指令重驗）
- 把 Apple 主控台產生的 `apple-developer-domain-association.txt` 放進
  `apps/web/public/.well-known/` 並部署（檔案內容由 Apple 產生，且綁定 Apple 團隊）

## How to verify

```bash
# 開通前的現況：三家都是 false
curl -s https://mokaair.com/api/travel/auth/oauth/providers

# 主機收斂：要驗 OAuth 路徑，不能只驗 /
curl -sSI https://www.mokaair.com/api/auth/oauth/google/start | grep -iE '^HTTP|^location'
# 期望：HTTP/1.1 301 ... 且 location: https://mokaair.com/api/auth/oauth/google/start

# Apple 檔案部署後應該取得檔案內容，再回 Apple 按 Verify
curl -s https://mokaair.com/.well-known/apple-developer-domain-association.txt
```

## Notes

查證過、可以省下重複追查的結論：

- **www 的 301 本來就存在**，路徑保留、涵蓋 `/api/*`（`nginx/1.28.3`）。規劃過程中
  一度誤判成「沒有 301」並當成阻斷性問題，原因是拿會把網頁轉成文字摘要的抓取工具
  去判斷轉址狀態。這種問題只能用 `curl` 看原始 header，而且要驗 OAuth 路徑而不是
  只驗 `/`，否則分不出「全站轉址」和「只轉根路徑」。

- **打包不會擋 `.well-known`。** `apps/web/next.config.ts` 用 `output: "standalone"`，
  standalone 不會自動帶 `public/`，但 `apps/web/Dockerfile` 有明確
  `COPY --from=builder /repo/apps/web/public ./apps/web/public`，Docker COPY 目錄會
  含隱藏檔；`.dockerignore` 也沒有排除 `.well-known` 或 `.txt`。
- **路由不會擋。** `apps/web/proxy.ts` 的 matcher `/((?!api|_next|_vercel|.*\..*).*)`
  排除含 `.` 的路徑，所以不會被加語系前綴。
- **連線測試很弱。** `admin/service.py:1586` 對 Google/LINE 只抓官方 OpenID
  metadata，完全不驗 client id/secret；只有 Apple 會真的用 `.p8` 簽一次 ES256，
  所以私鑰格式錯會當場失敗。
- **後台測試失敗不會讓按鈕消失。** `/auth/oauth/providers` 只看
  `provider_enabled()`（啟用 + 憑證齊全），跟 `last_test_status` 無關；
  `last_test_status == "failed"` 只影響後台卡片顯示。
- **停用的設定列會蓋掉環境變數。** `admin/service.py:513` 在 row 停用時把 secret
  欄位設成 None，連 `.env` 的值一起蓋掉；DB 密文本身保留，重新啟用就恢復。
- **LINE Login 和價格通知的 Messaging API 是兩個不同 channel**，設定也分開
  （`auth_line_*` vs `line_messaging_*`），憑證不能混用。
- 本專案沒有寄信也沒有忘記密碼流程，所以純社群帳號若之後停用該供應商會鎖死，
  回滾前要先確認。
- 完整開通手冊（三家主控台步驟、後台欄位對照、9 項驗收、錯誤碼對照表）在
  這次規劃的 plan 檔，內容已濃縮進 `docs/social-login.md`。
