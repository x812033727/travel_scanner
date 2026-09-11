# 開通 Google 與 LINE 登入（站長操作手冊）

程式碼已經寫好而且上線了。這份文件是**申請憑證並打開開關**的逐步流程。
設計決策與安全行為寫在英文版的 [`social-login.md`](social-login.md)，讀者是開發者；
這份的讀者是要去 Google 與 LINE 後台按按鈕的人。

現在的狀態可以直接問線上站台：

```bash
curl -s https://mokaair.com/api/travel/auth/oauth/providers
# 目前：{"providers":{"google":false,"line":false,"apple":false}}
```

三個都是 `false`，代表三家都還沒填憑證。登入頁因此一顆第三方按鈕都不會顯示——
這不是壞掉，是 `provider_enabled()`（`apps/api/app/auth/oauth.py:60`）要求
**「已啟用」而且「憑證齊全」**才算數。

Apple 需要付費的 Apple Developer Program（US$99／年），程式碼同樣已經支援，
本文最後一節說明要準備什麼，但不影響先把 Google 與 LINE 開起來。

---

## 一、開始之前要先知道的三條規則

這三條會**實際擋住使用者**，不是注意事項。先看懂再決定怎麼對外公告。

### 1. 第一次用第三方建立帳號，一定要拿得到「已驗證的 Email」

`apps/api/app/auth/oauth.py:435` 直接擋下沒有已驗證 Email 的首次註冊，
回 `oauth_email_required`。

對 Google 沒問題（`email_verified` 一定會給）。
對 LINE 則代表：**Email 權限沒過審之前，LINE 只能綁定既有帳號，不能註冊新帳號。**
使用者會一路點到最後才看到錯誤。所以 LINE 的 Email 權限沒過，就先別打開 LINE 開關。

### 2. 同一個 Email 不會自動合併帳號

已經用密碼註冊 `you@gmail.com` 的人，直接按「使用 Google 繼續」，
會拿到 `oauth_account_exists`（`oauth.py:437`），畫面上寫
「此 Email 已有會員，請先用原方式登入後再到帳號頁綁定」。

這是刻意的安全設計——自動合併等於讓任何能在供應商端控制該 Email 的人接管帳號。
但真實使用者會覺得「我明明就是用這個 Gmail 註冊的」。正確的路徑是：

1. 用原本的 Email + 密碼登入
2. 進「帳號」頁
3. 按「連結 Google」

綁定之後，下次就可以直接用 Google 一鍵登入。

### 3. 管理員信箱不能用第三方登入建立帳號

列在 `ADMIN_EMAILS`、`DEPLOY_ADMIN_EMAILS`、`DATABASE_ADMIN_EMAILS` 的地址
會被 `admin_email_reserved` 擋下（`oauth.py:447`），避免有人搶先用第三方登入
把管理員信箱註冊走。這些帳號要用 CLI 建立：

```bash
cd apps/api && uv run python -m app.cli create-admin --email you@example.com
```

---

## 二、Google（免費，大約 15 分鐘）

### 在 Google Cloud Console

1. 開 <https://console.cloud.google.com/> → 建立或選一個專案。
2. 左側「API 和服務」→「OAuth 同意畫面」：
   - User Type 選 **External**（外部）
   - 應用程式名稱填 `Mokaair`
   - 使用者支援電子郵件、開發人員聯絡資訊填你的信箱
   - 「已授權的網域」加 `mokaair.com`
3. 「API 和服務」→「憑證」→「建立憑證」→ **OAuth 用戶端 ID**：
   - 應用程式類型選 **網頁應用程式**
   - 「已授權的重新導向 URI」**逐字**填入：

     ```text
     https://mokaair.com/api/auth/oauth/google/callback
     ```

     本機也要測的話，再加一筆：

     ```text
     http://localhost:3000/api/auth/oauth/google/callback
     ```

4. 建立後會拿到 **用戶端 ID** 與 **用戶端密鑰**，兩個都留著。

### 不需要送審

Mokaair 只要 `openid email` 兩個 scope（`oauth.py:151`），屬於 Google 的
非敏感範圍，**不必經過驗證流程**。同意畫面在「測試」狀態時只有你加進測試使用者
清單的帳號能登入，要對所有人開放就按「發布應用程式」。

> 逐字是逐字：`https://` 不能寫成 `http://`、有沒有 `www` 算兩個不同的網址、
> 結尾不能多一個斜線。不一致 Google 會直接擋在自己的錯誤頁，連 Mokaair 都進不來。

---

## 三、LINE（免費，但 Email 權限要送審）

### 在 LINE Developers Console

1. 開 <https://developers.line.biz/console/> → 建立一個 Provider（如果還沒有）。
2. 在該 Provider 下建立 channel，類型選 **LINE Login**（不是 Messaging API）。
3. channel 的「App types」要勾到 **Web app**。
4. 「LINE Login」分頁 →「Callback URL」**逐字**填：

   ```text
   https://mokaair.com/api/auth/oauth/line/callback
   ```

   本機測試再加一行 `http://localhost:3000/api/auth/oauth/line/callback`
   （LINE 的 Callback URL 欄位可以一行一個）。

5. 「OpenID Connect」區塊 → **Email address permission** → 按 **Apply**。
   要上傳一張說明用途的截圖（通常放登入畫面即可），審核大約一到兩個工作天。
6. 「Basic settings」拿 **Channel ID** 與 **Channel secret**。

> ### 不要跟價格通知的 LINE channel 搞混
>
> 這個專案另外有一個 LINE **Messaging API** channel，用來推播降價通知
> （見 [`line-price-alerts.md`](line-price-alerts.md)）。那是不同的 channel，
> 憑證不能互換。登入用的一定要是 **LINE Login** 類型。

### Email 權限沒過就先別開

如前面第一條規則：沒有 Email 權限，LINE 拿不到 `email` claim，
新使用者會走完整個授權流程才看到「首次建立帳號需要已驗證的 Email」。
等審核通過再打開 LINE 的啟用開關。

---

## 四、填進 Mokaair 後台

1. 用管理員帳號登入，開 <https://mokaair.com/zh-TW/admin/settings>。
2. 找到 **「Google 登入」** 卡片：
   - `auth_google_client_id` ← Google 的用戶端 ID
   - `auth_google_client_secret` ← 用戶端密鑰
   - 打開「啟用」
   - 儲存
3. **「LINE 登入」** 卡片同樣填 `auth_line_channel_id` 與 `auth_line_channel_secret`，
   打開啟用，儲存。
4. 兩張卡片都按一次「測試連線」。

### 「測試連線」通過不代表憑證是對的

`apps/api/app/admin/service.py:1722-1737`：Google 與 LINE 的測試只去抓供應商的
**公開 OpenID metadata**（Google 的 JWKS、LINE 的 `.well-known/openid-configuration`）。
那是公開網址，**client id 填錯、secret 填錯，測試一樣會過**。

它只證明一件事：伺服器連得到供應商。
唯一能證明憑證正確的，是**真的走完一次登入**。

（Apple 的測試比較有用，它會實際簽一份 ES256 client secret，所以 `.p8` 壞掉會被抓到。）

### 環境變數是備援，不是主要途徑

後台存的值優先。也可以改用環境變數（`.env`）：

```text
AUTH_GOOGLE_ENABLED=true
AUTH_GOOGLE_CLIENT_ID=
AUTH_GOOGLE_CLIENT_SECRET=
AUTH_LINE_ENABLED=true
AUTH_LINE_CHANNEL_ID=
AUTH_LINE_CHANNEL_SECRET=
```

但**兩邊混用會出事**，原因見下一節第一條。建議只用後台。

---

## 五、驗收

```bash
curl -s https://mokaair.com/api/travel/auth/oauth/providers
# 期望：{"providers":{"google":true,"line":true,"apple":false}}
```

然後開**無痕視窗**（避免既有 cookie 干擾）：

1. 開 <https://mokaair.com/zh-TW/login>，應該看到「使用 Google 繼續」與
   「使用 LINE 繼續」兩顆按鈕，下面一條「或使用 Email」分隔線。
2. 各走完一次完整登入，確認回到站上而且是已登入狀態。
3. 再去「帳號」頁，確認已連結的方式列出來，而且可以解除連結
   （最後一個可用的登入方式不會讓你解除——這是刻意的）。

---

## 六、「我明明設定了，卻還是 false」排查清單

依照實際踩到的機率排序。

### 1. 後台有一列存著、但開關是關的 ← 最常見

`apps/api/app/admin/service.py:539-543`：

```python
if definition.enabled_field:
    updates[definition.enabled_field] = row.enabled
if not row.enabled and row.provider not in ALWAYS_ENABLED_PROVIDERS:
    updates.update({field: None for field in definition.secret_fields})
    continue
```

資料庫那一列的 `enabled` 會**覆蓋環境變數，而且是雙向的**。更麻煩的是：
只要那列是關的，它會把該供應商的**所有 secret 欄位設成 `None`**——
連你在 `.env` 裡填好的也一起清掉。

所以「`.env` 設了 `AUTH_GOOGLE_ENABLED=true`，但後台留著一列關掉的 google_login」
的結果就是 `false`，而且看起來像環境變數壞了。

**解法**：後台把那列打開再存一次。加密過的 secret 還在資料庫裡，開回來就會回來。

### 2. 後台存進了空字串

同一段的 `:536-538`：只要 key 出現在 `row.config` 裡就會覆蓋環境變數。
存成空字串會讓 `provider_enabled()` 判成 falsy，結果一樣是 `false`。

### 3. `SETTINGS_ENCRYPTION_KEY` 換過

舊的密文解不開，等同沒填。這個值在正式環境要固定，換掉會讓所有已存的加密設定失效。

### 4. 改的是 `.env` 但沒重啟 API

後台設定是每個 request 重讀資料庫（`load_runtime_settings`），改完立刻生效。
但環境變數要重啟 API 容器才會重讀。

### 5. `redirect_uri` 不符

callback 網址由 `NEXT_PUBLIC_SITE_URL` 產生（`oauth.py:88`）：

```python
return f"{settings.next_public_site_url.rstrip('/')}/api/auth/oauth/{provider}/callback"
```

供應商後台填的必須**逐字相同**。不一致的話 Google／LINE 會在自己的頁面就擋下來，
錯誤訊息通常是 `redirect_uri_mismatch`。

### 6. 一直出現 `oauth_state_invalid`

代表站台同時在兩個網域上應答。`/api/auth/oauth/{provider}/start` 寫的流程 cookie
是 **host-only**（沒有 `Domain` 屬性，見 `start/route.ts:52-69`）。
在 `www.mokaair.com` 開始的登入，cookie 留在 `www`，
但 `redirect_uri` 永遠指向 `NEXT_PUBLIC_SITE_URL`，供應商把瀏覽器送回 `mokaair.com`，
callback 就找不到 cookie。每一次都失敗，重試也沒用。

在供應商後台把兩個網域都註冊**不能解決**，因為 API 只會產生一種 `redirect_uri`。
所有會應答的網域都必須轉址到正式的那一個。

檢查的時候**要測 OAuth 路徑，不能只測 `/`**——只蓋到根目錄的轉址仍然會壞掉，
而測 `/` 看不出差別：

```bash
curl -sSI https://www.mokaair.com/api/auth/oauth/google/start | grep -iE '^HTTP|^location'
# 期望：HTTP/1.1 301 ...
#       location: https://mokaair.com/api/auth/oauth/google/start
```

### 7. 使用者說「它叫我先用原方式登入」

那不是故障，是第一節第 2 條的 `oauth_account_exists`。

---

## 七、之後要開 Apple 的話

需要：

- **Apple Developer Program** 會籍（US$99／年）
- 一組 **Services ID**、**Team ID**、**Key ID**，以及 Sign in with Apple 的 `.p8` 私鑰
- 網域驗證：Apple 會發一個 `apple-developer-domain-association.txt`，
  必須放在 `apps/web/public/.well-known/`，讓它能從
  `https://mokaair.com/.well-known/apple-developer-domain-association.txt` 讀到
  （這個檔案本來就是要公開的，不是機密）

程式碼已經完整支援，包含 Apple 的 `form_post` 回應模式、ES256 client secret、
以及解除連結時呼叫 Apple 的 token 撤銷端點。
細節見 [`social-login.md`](social-login.md) 的 Apple 段落。
