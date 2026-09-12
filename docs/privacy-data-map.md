# 個資盤點：這套程式實際蒐集什麼、送給誰、留多久

## 這份文件要解決什麼

`/privacy`、`/terms`、`/about`、`/contact` 四頁的草稿都寫好了，但發布被
`pending_requirements()`（`apps/api/app/site_pages/service.py:61-70`）擋著，因為
`operator`、`location`、`contact`、`retention`、`legal` 五個欄位與 `effective_date` 是空的。
其中 `retention` 有一半不是法律判斷，是「這套程式實際上做了什麼」——那個答案散在 repo 裡。

這份文件把它整理出來，每一條都標到檔案與行號。它有兩個用途：

1. 讓擁有者回答 `retention` 時是在**確認事實**，不是在猜。
2. 功能改了以後，拿它對照隱私權政策哪一段需要跟著改。

**這份文件不是隱私權政策，也不是法律意見。** 它只陳述程式的行為。

## 這份清單有多可信

初稿由兩次自動盤點產出，但**寫進法律文件之前每一條都得自己驗**，所以下面這幾條是
逐一讀過程式碼確認的，不是照抄：

| 主張 | 核對結果 |
| --- | --- |
| Travelpayouts 收到 `uuid5(...user.id...)` 當 `sub_id` | ✅ 成立，而且**範圍比初稿更廣**（見第七節） |
| Travelpayouts Drive 沒有 env flag，只看 production hostname | ✅ 成立 |
| `AI_PLANNER_ENABLED` 預設 true，`notes` 原文送給 AI 廠商 | ✅ 成立 |
| `users` 列留著、`usage_*` 三張表 `erase_account()` 完全沒碰 | ✅ 成立 |
| `/places/photo` 302 導向 Google，瀏覽器直接抓 | ✅ 成立 |
| 稽核紀錄去識別化「是部分的」 | ❌ **核對後撤回**（見第六節） |

最後一列是重點：初稿說稽核紀錄只做了部分去識別化、政策應該加但書。掃過全部 95 個
寫入點之後那不成立。**如果照抄，這份隱私權政策會對讀者少承諾一件它其實有做到的事。**
反方向的錯誤（多承諾沒做到的事）更糟，但兩種都是錯的。

---

## 一、帳號與登入

`users` 表（`apps/api/app/models.py:45-69`）只有：email、密碼雜湊（OAuth 帳號為 null）、
啟用狀態、`auth_version`、偏好語系與幣別、email 驗證時間、`deleted_at`、`last_login_at`、
停權三欄。**沒有姓名、電話、地址、生日，也沒有 IP 欄位。** 註冊只收 email 與密碼
（`apps/api/app/auth/schemas.py:26-29`）。密碼用 pwdlib 的 `recommended()`，預設 Argon2
（`auth/service.py:10,21`）。

第三方登入（`user_auth_identities`，`models.py:107-126`）限定 google／line／apple，
要求的 scope 只有 `openid email`／`email`（`auth/oauth.py:148,161,169`），**沒有要 profile
或頭像**。首次建立帳號只複製 email 與語系（`oauth.py:436-455`）。Apple 的 refresh token
會加密保存，用途僅限向 Apple 反向撤銷。

登入狀態是 JWT，不是資料表（`auth/service.py:131-158`）。60 分鐘、用掉一半時滑動續期、
**絕對上限 30 天**（`config.py:120,123`）。登出後 `jti` 進 Redis 黑名單直到過期
（`service.py:235-257`）。

密碼重設與刪除帳號的連結只存 SHA-256 摘要，30 分鐘失效（`community/accounts.py:69-86`），
而且 token 放在 URL 的 fragment——程式註解說明了原因：「Fragments are not sent in HTTP
requests, access logs or Referer headers.」（`accounts.py:88-89`）

---

## 二、Cookie 與瀏覽器儲存

### Cookie

| 名稱 | httpOnly | 期限 | 用途 |
| --- | --- | --- | --- |
| `travel_access` | 是 | 1 小時（BFF 最長 30 天） | 登入 JWT |
| `admin_step_up` | 是，`sameSite=strict` | 5 分鐘 | 管理員破壞性操作前的再驗證 |
| `travel_locale` | **否** | **1 年** | 介面語言 |
| `travel_oauth_{google,line,apple}` | 是 | ≤30 分鐘 | OAuth CSRF／PKCE 狀態，回跳後刪除 |
| `travel_oauth_registered` | **否**（刻意讓 JS 讀） | 5 分鐘 | 一次性訊號，讀完立刻刪 |

正式環境強制 `COOKIE_SECURE=true`（`config.py:584-585`）。**站方自己不設任何第三方 cookie**；
GA4 啟用時 Google 會設自己的 `_ga*`。

### localStorage（留在裝置上，直到使用者清除）

主題／配色／字級（`lib/theme.ts:1-2`、`lib/text-size.ts:1`）、餐廳篩選偏好、後台介面狀態。
**還有使用者自己打的行程內容**：`trip-planner-draft:<tripId>`（`components/trip-editor.tsx:424,592`）
存未存檔的行程編輯，存檔或捨棄時才刪除。

### sessionStorage（關掉分頁就消失）

`travel_analytics_session`（一個 `crypto.randomUUID()`）、
`mokaair-new-trip-draft:<accountId>`、`mokaair-pending-plan:<accountId>`。
後兩者同樣含使用者打的內容。

> **共用裝置要注意**：上面三個「草稿」鍵在使用者存檔或捨棄之前會一直留在瀏覽器裡。
> 現行隱私權草稿沒有提到這件事。

---

## 三、使用分析

**預設全關**：`analytics_enabled=False`、`ga4_enabled=False`（`config.py:139-140`）。

**DNT／GPC 一律尊重**，而且兩端都擋：瀏覽器端連 gtag.js 都不載入
（`components/analytics-provider.tsx:32-34,169`）；伺服器端收到 `DNT: 1` 或 `Sec-GPC: 1`
直接回 `accepted=0`（`analytics/service.py:190-197`）。連伺服器自己產生的事件也照擋，
註解寫得很清楚：「a visitor who asked not to be measured did not mean 'except when the
measuring happens server-side'.」（`analytics/context.py:39-41`）

**一筆事件實際存了什麼**（`models.py:511-542`）：事件名、正規化路徑、語系、`session_hash`、
`visitor_day_hash`、國碼、裝置／瀏覽器／OS 分類、來源分類與主機、UTM、是否登入（**布林值**）、
是否機器人。**沒有 `user_id` 欄位，也沒有原始 IP 或原始 User-Agent。**

- 路徑會正規化：UUID 與長 token 換成 `:id`，而且 `/admin`、`/api`、`/health`、`/ready`
  底下的事件**整筆丟掉**（`service.py:83-98`）。
- `session_hash` 與 `visitor_day_hash` 是用 `APP_SECRET_KEY` 當金鑰的 **HMAC-SHA256**
  （`service.py:100-101,216-217`），不是單純雜湊。原始 IP 只當 HMAC 輸入，**從不儲存**，
  而且 `visitor_day_hash` 按台北日期輪替。
  *附帶影響*：換掉 `APP_SECRET_KEY` 會讓這兩個雜湊斷開連續性，而同一把金鑰也在簽 session JWT。
- 事件屬性只收 bool、int，與符合 `[a-z][a-z0-9_]{0,31}` 的字串，最多 6 個 key
  （`service.py:277-296`）。註解值得直接引用：「a truncated identifier is still an
  identifier, and a UUID is only 'a short string' until you notice it names someone.」
- 國碼只在 `analytics_trust_country_header` 開啟時才有，而它**預設是關的**（`config.py:142`）。

**GA4 的同意狀態永遠是拒絕。** `analytics-provider.tsx:56-64` 把
`analytics_storage`／`ad_storage`／`ad_user_data`／`ad_personalization` 全設為 denied、
開啟 `ads_data_redaction`、關閉 `allow_google_signals`。**整個 repo 沒有任何一處呼叫
`gtag("consent","update")`**——所以站上沒有同意橫幅，政策也不該先描述一個不存在的橫幅。

---

## 四、使用者產生的內容

**行程預設是私人的。** `trip_plans` 與其子表存名稱、日期、備註、花費、座標（6 位小數）。
分享連結只存 token 的 SHA-256（`models.py:1997-2006`），而且公開出去的欄位是
**加法白名單**（`trips/router.py:913-954`）：每一項備註、整個 `data`、報價快照、
`offer_id`、供應商來源都**不會**進分享頁。註解：「Anything the owner typed for themselves
(notes), paid (price_snapshot, offer_id) … stays out.」

**社群是選擇加入的，而且身分獨立。** `community_profiles` 沒有 email 欄位，公開投影只回
handle／暱稱／簡介／語言／目的地／頭像（`community/policy.py:114-123`）。上傳的圖片會
**重新點陣化以剝除 EXIF／XMP／ICC**（`community/media.py:71-72`），原圖進隔離區。
私訊、檢舉、通知各有自己的表；檢舉證據限於「回報者自己選取的訊息」（`models.py:281`）。

---

## 五、保存期限：程式真正支持的只有這些

| 項目 | 期限 | 出處 |
| --- | --- | --- |
| analytics 原始事件 | **90 天**（可設 30–365） | `config.py:145` → `analytics/jobs.py:60-67` |
| analytics 每日彙總 | **25 個月**（可設 13–60） | `config.py:146` |
| 登入 session | 60 分鐘滑動、**絕對上限 30 天** | `config.py:120,123` |
| 密碼重設／刪除帳號連結 | 30 分鐘 | `community/accounts.py:69-86` |
| OAuth flow state | 10 分鐘 | `config.py:153` |
| 管理員 step-up 再驗證 | 5 分鐘 | `auth/service.py:33` |
| 航班動態快取 | 到期時順手刪 | `flights/router.py:53-57` |
| 供應商原始回應、路線預覽 | Redis，10–15 分鐘 | `providers/*.py`、README:561 |
| `travel_locale` cookie | 1 年 | — |

**其餘全部沒有排程清理**：`search_requests`、`provider_responses`、`trip_plans`、
`admin_audit_logs`、`usage_ledger`、`affiliate_clicks`、`community_*`——都保留到帳號清除為止，
而稽核與帳本連帳號清除都不刪（見下一節）。

> 這一行就是擁有者要決定的地方：要不要為這些資料訂一個期限，還是照現況寫「保留到你刪除帳號」。

---

## 六、刪除帳號實際上做了什麼

**兩階段。** 使用者按下確認後（`community/accounts.py:219-250`，需要一封 30 分鐘有效的信）：
立刻停用帳號、`auth_version+1` 讓所有 session 失效、隱藏公開內容、**撤銷所有行程分享連結**，
然後把清除工作丟給背景 worker。

`erase_account()`（`community/jobs.py:173-443`）會刪除或清空四十幾類資料：探索偏好、
S3 上的圖片（含隔離區原圖）、社群個人檔案、貼文與留言內容、收藏、追蹤與封鎖、寵物回報、
五張收藏表、通知、行程子表、`search_requests` 的 `request_json`／`result_json`、
`provider_responses` 的 `payload`、航班查詢、報價、價格通知、LINE 連結。

**但有東西刻意留下來，政策必須講清楚**（`jobs.py:206` 的註解：「Retain FK identities for
ledger and already-delivered conversations; erase PII.」）：

- **`users` 那一列不會被刪掉。** email 改寫成 `<uuid>@deleted.invalid`，密碼雜湊、
  驗證時間、最後登入時間清空（`jobs.py:208-214`，已核對）。
- **`usage_accounts`／`usage_ledger`／`usage_reservations` 完全沒被碰。**
  `erase_account()` 裡沒有任何一處引用這三張表（已核對）。它們仍帶著 `user_id` 與
  自由文字的 `summary`。
- **已送達的私訊本文留在對方的對話裡。**
- **`admin_audit_logs` 的去識別化靠兩個 UPDATE**（`jobs.py:238-247`）：一個打
  `target == "user:<id>"`，一個打 `actor_user_id == 使用者`，兩者都把 `metadata_json`
  清成 `{}`。**已逐一核對全站 95 個 `AdminAuditLog(...)` 寫入點**：每一個把 email 或
  使用者識別碼寫進 `metadata_json` 的（`admin/users.py` 十餘處、`cli.py:139,188`）都用
  `target=f"user:{user.id}"`，所以都會被清掉。**目前沒有漏網的列。**
  → 但這是靠慣例而非機制維持的：沒有任何東西擋得住未來新增一個把 email 寫在別的
  `target` 底下的稽核列，那樣就會靜默地逃過清除。這是**該補一個測試**的地方，
  不是政策要加的但書。
- **`affiliate_clicks` 是 PostgreSQL trigger 強制的 append-only**
  （`migrations/versions/0068_admin_operations_center.py:313`），唯一允許的變更是
  `SECURITY DEFINER` 的匿名化函式。清除時走那個函式，把 `user_id` 等改成 NULL。

**程式從來沒有執行過 `DELETE FROM users`。** 清除是就地覆寫，不是刪列——政策要描述的是
「抹除」，不是「刪除資料列」。

管理員發動的清除另有 24 小時緩衝（`models.py:2296-2329`、`jobs.py:443-560`），
而且受環境保護的管理員與最後一位 owner 不能被清除。

---

## 七、第三方

### 會在瀏覽器上跑的

| 對象 | 拿到什麼 | 開關 |
| --- | --- | --- |
| **Google Analytics 4** | IP、UA、正規化後的路徑、語系、對應後的事件名 | `GA4_ENABLED=false`；DNT／GPC 完全不載入 |
| **Travelpayouts Drive** | 在站方 origin 上執行的第三方腳本：頁面網址、referrer、IP／UA | **沒有 env flag**，只看 `NEXT_PUBLIC_SITE_URL` 是不是 mokaair.com（`lib/travelpayouts-drive.ts:3-6`，已核對）；DNT／GPC 會擋 |
| **Stay22 LetMeAllez SDK** | 同樣在站方 origin 上執行。文件自己寫明：「DOM/document separation, **not a separate cookie or security origin**」 | 預設關閉，且限定 `/(stay22-public)/` 路由群組 |
| **Stay22 地圖 iframe** | 白名單參數：座標（5 位小數）、日期、人數、樣式 | **點擊才載入**，`referrerPolicy="no-referrer"` |
| **Google Maps JS／NAVER Maps JS** | IP／UA、金鑰、行程座標與路線 | 使用者展開路線抽屜才載入；Google 版預設關閉 |
| **YouTube（nocookie）** | 載入時的 IP／UA | **點擊才載入** |
| **Google 圖片 CDN** | `/places/photo` 回 302 導到 Google 自架的圖片網址，所以**瀏覽器直接去抓**，Google 拿到訪客 IP／UA（`places/router.py:152-168`，已核對；該端點需登入） | 有 `GOOGLE_MAPS_API_KEY` 就會發生 |

**沒有第三方字型或 JS CDN**（`font-src 'self' data:`）。

### 伺服器端會送出去的

- **AI 規劃**（OpenAI／Anthropic／MiniMax／Gemini，`AI_PLANNER_ENABLED` **預設 true**，
  `config.py:174`，已核對）：收到目的地、日期、人數、偏好，**以及使用者自己打的 `notes`
  與行程項目的 `title`／`location_name`**（`ai/itinerary.py:281-282`）。排除清單只排掉
  各語系顯示名稱，**不排使用者文字**。其中 **MiniMax（`api.minimaxi.com`）在跨境傳輸上
  最敏感**，`location` 選了哪個司法管轄區會直接影響這一條。
- **社群翻譯**：整篇貼文或留言內容（最多 6 萬字）送給 Gemini（`community/translation.py:30-54`）。
- **Google Places**：使用者輸入的搜尋與自動完成文字**原文送出**（`places/google.py:128,225,302`）。
- **Google Routes／Weather、MET Norway、NAVER、ODsay 等**：座標與時間。MET Norway 送 4 位
  小數，Google Weather 送 6 位。
- **航班與住宿供應商**（Amadeus／Skyscanner／Duffel／Booking）：機場代碼、日期、人數。
  Booking Demand API 另外送**精確座標（6 位小數）與實際的兒童年齡**
  （`providers/booking.py:288-320`）。預設 `TRAVEL_PROVIDER_MODE=mock`，也就是預設完全不呼叫。
- **LINE 推播**：`line_user_id`，訊息內容含航空公司或飯店名稱、起訖地、價格與目標價
  （`alerts/monitor.py:321-394`）。預設關閉。
- **SMTP**：收件者 email 與一次性連結。**S3／MinIO**：社群圖片，物件鍵含使用者 id。

### 一個要特別決定的問題：交給聯盟網路的每使用者識別碼

`affiliates/router.py:376-379`（已核對）：

```python
sub_id = uuid5(
    NAMESPACE_URL,
    f"travel-scanner:affiliate:{user.id}:{source}:{partner.code}:{module}",
).hex
if partner.code == "klook":
    sub_id = f"aff_{module}_{active_locale()}"
```

這是一個**穩定的、綁定使用者的假名識別碼**，交給聯盟網路做跨站歸因。Travelpayouts 透過
Links API 收到它（`service.py:163`）；其他夥伴則是在管理後台設定的網址樣板裡若出現
`{sub_id}` 就會被代入（`service.py:55`）。

**Klook 是唯一有防護的**（`service.py:231-234`：「never expose a member/trip-derived ID」）。
KKday、Agoda、Trip.com、Airalo、Booking、Skyscanner 都沒有同樣的處理。

→ 這件事有兩個選項：在政策裡揭露它，或是把 Klook 那條防護套用到所有夥伴。**這是產品決定，
不只是文件問題。**

### 一個寫政策時不能講錯的前提

**嚴格版 CSP 目前是 Report-Only**（`proxy.ts:17,23`），強制的只有 baseline
（`frame-ancestors`／`object-src`／`base-uri`／`form-action`）。那份白名單表達的是意圖，
**不是技術保證**，政策不要寫成「我們在技術上阻止了 X」。

另外 `scripts.stay22.com` 刻意不在 `script-src` 裡，它是靠 `'strict-dynamic'` 執行的
（`lib/csp.test.ts:10` 還斷言 stay22 只出現在 `frame-src`）——只看白名單的人會漏掉
站上權限最高的那個第三方腳本。

---

## 八、現有草稿與程式不符的地方

`apps/api/app/site_pages/drafts/*.json` 的 `privacy` 條目（五語系各 13 個區塊）整體是準確的，
它刻意只描述機制、把承諾推給 `requirements`。但有四處需要修：

1. **「帳號刪除確認後……背景程序再清理相關個人資料與媒體」講得太輕。** 見第六節：
   `users` 那一列留著、`usage_*` 三張表完全沒動。這是一整類留存資料，要講出來。
2. ~~稽核紀錄的去識別化是部分的~~ — **核對後撤回**。全部 95 個寫入點都用
   `target=f"user:{user.id}"`，清除時會被涵蓋。內文不需要為此加但書；要補的是一個
   防止未來回歸的測試。
3. **沒提到未存檔的草稿會留在瀏覽器**（第二節）。共用裝置上這是實際風險。
4. **「雜湊識別」其實是 HMAC**（第三節）。可以寫得更準確也更有利。

以及一個缺口：**全文沒有任何一句提到廣告。** 要放 Google AdSense 的話，AdSense 計畫政策
要求揭露第三方（含 Google）使用 cookie 投放廣告，這裡得新增一個區塊；同時第三節提到的
「同意永遠是拒絕」現況也要一併交代。

---

## 九、只有擁有者能回答的五件事

這五個欄位會**原文公開在頁面上**（`components/site-page-content.tsx:14` 把它們渲染成 `<dl>`），
而且**每個語系各有一份**（5 欄 × 5 語系 = 25 格），沒有任何檢查會提醒哪個語系漏填。

| 欄位 | 後台標籤 | 需要什麼 |
| --- | --- | --- |
| `operator` | 營運者 | 對外的法律主體名稱（公司或個人） |
| `location` | 營運所在地 | 決定適用哪一國法規，也決定上面跨境傳輸那幾條怎麼寫 |
| `contact` | 聯絡我們 | 一個真的收得到信的地址或表單 |
| `retention` | 資料保留與刪除 | 事實在第五、六節；**期限是承諾**，要人決定 |
| `legal` | 適用法律及爭議處理 | 純法律決定 |
| — | 生效日期 | 必填，且不能是未來日期（`service.py:66-69`） |

**注意**：改 `drafts/*.json` 只對**還沒初始化**的環境生效。`initialize_pages()`
（`service.py:201-230`）用 `on_conflict_do_nothing`，註解寫明「No draft, published pointer
or history that already exists is overwritten.」已經初始化的環境要在
**後台 → 網站資訊** 逐語系編輯並發布。
