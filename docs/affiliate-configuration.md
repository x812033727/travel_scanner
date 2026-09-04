# 聯盟行銷配置指南

本站的聯盟行銷子系統（`apps/api/app/affiliates/`）已完整實作：8 家平台註冊表、後台加密設定、
網域白名單防轉址、一次性 token clickout、append-only 點擊記錄。所有平台預設停用，
需要在後台填入憑證後才會出現在前台。

本文說明**先開哪一家、每個欄位填什麼、怎麼驗證**。

---

## 1. 結論：先用 Travelpayouts 單一主軸

| 判準 | 說明 |
|---|---|
| 審核成本 | 一個帳號涵蓋 100+ 品牌，其餘 7 家都要個別送審 |
| 追蹤能力 | Travelpayouts 是註冊表裡唯一具備 `link_api` capability 的平台（`registry.py:91`），走 Partner Links API 自動帶 `sub_id`；其他 7 家只能手寫 URL 範本 |
| 多語系涵蓋 | 同一帳號涵蓋 Booking、Agoda、Trip.com、Klook、GetYourGuide、Viator、Airalo，五個語系市場都有對應的強勢品牌 |
| 現金流 | 提領門檻 US$50，低於 KKday（銀行轉帳 US$200）與 Booking 直接方案（€100） |
| 對帳 | 單一後台結算，不必逐家平台對帳 |

**升級路徑已內建，現在不必決定。** `AffiliatePartner.priority` 數字小的排前面：

```
skyscanner / booking / kkday = 10
agoda / klook               = 20
trip_com                    = 30
travelpayouts               = 90   ← 最後
```

日後任一品牌的月成交量大到值得走直接方案時，只要在後台填該品牌的 CID/AID 與合作連結範本
並啟用，它就會自動排在 Travelpayouts 前面，Travelpayouts 退為長尾補位。**不需要改任何程式碼。**

---

## 2. 後台逐欄填寫表

路徑：`https://mokaair.com/zh-TW/admin/settings` →「分潤導流」分類 → `Travelpayouts Affiliate`

| 欄位（後台標籤） | 填什麼 |
|---|---|
| 啟用 | 勾選 |
| Partner Links API Base URL | `https://api.travelpayouts.com` — **不要改**。這個欄位被 `OFFICIAL_PROVIDER_HOSTS` 釘死（`config.py:59-74`），填別的網域會被拒絕 |
| Marker | Travelpayouts 的 affiliate marker，**純數字** |
| Project ID | Travelpayouts 專案 ID，即 API 的 `trs`，**純數字** |
| API Token | Travelpayouts API token（加密欄位，存進 `provider_configs.secret_config_encrypted`） |
| 允許跳轉網域 | `tp.st,travelpayouts.com,tp.media` |
| 安全備援合作連結 | 儀表板產生的短連結，例如 `https://<你的名稱>.tp.st/xxxxxxx`。只在 Partner Links API 失敗時使用 |
| 航班原始目標網址 | 例：`https://www.aviasales.com/search?destination={destination}&depart_date={departure_date}&return_date={return_date}` |
| 住宿原始目標網址 | 例：`https://www.booking.com/searchresults.html?ss={destination}&checkin={departure_date}&checkout={return_date}` |
| 活動原始目標網址 | 例：`https://www.getyourguide.com/s/?q={destination}` |
| 交通原始目標網址 | 例：`https://www.kiwitaxi.com/?destination={destination}` |
| eSIM 原始目標網址 | Airalo 在 Travelpayouts 上的方案網址。留空時自動沿用「活動原始目標網址」 |

> `Marker` 與 `Project ID` 在送出 API 前會被 `int()`（`affiliates/service.py:98-99`），
> 填入非數字會讓連結產生直接失敗。

四個目標網址不必全填 —— 只要其中一個有值，加上 token / marker / project ID，
就算「設定完成」（`registry.py:114-128`）。沒填的模組不會顯示 Travelpayouts 選項。

---

## 3. 五個踩雷點

### 3-1 `tp.media` 一定要加進允許跳轉網域

Travelpayouts 的短連結是 `*.tp.st`，長連結是 `tp.media/r?marker=...&trs=...`。
程式固定送 `shorten: true`（`affiliates/service.py:100`），所以 API 產出的連結一定是 `tp.st`；
但**從儀表板複製來當備援的 static link 常常是 `tp.media` 網域**。

`validate_target_url`（`affiliates/service.py:31-37`）會擋掉不在白名單的網域，
症狀是「設定看起來都對，但前台就是沒有出現連結」。預設值已含這三個網域，
若你手動改過這一欄，記得把 `tp.media` 加回去。

### 3-2 欄位格式驗證會擋

- 任何以 `_url` / `_url_template` 結尾的欄位**必須 HTTPS**
- 任何以 `_allowed_hosts` 結尾的欄位**必須是逗號分隔的純網域** —— 不可含協定、路徑、`*`、port、`@`

驗證邏輯在 `admin/service.py:938-959`，違反會回 422 並顯示中文錯誤。

### 3-3 目標網址必須是你已訂閱的品牌方案

Partner Links API 只接受你在 Travelpayouts 上**已加入該品牌方案**的網址。
沒訂閱就送出，API 會回錯，程式會**靜默 fallback 到備援連結**（`affiliates/service.py:158-163`）。
症狀是每個模組的連結都能點，但全部導到同一頁 —— 那就是備援連結。

### 3-4 範本變數只有五個

`{destination}` `{departure_date}` `{return_date}` `{sub_id}` `{module}`
（渲染邏輯在 `affiliates/service.py:40-51`），代入的值會被 percent-encode。
**沒有語系變數** —— 見下一節。

### 3-5 測試結果會被快取

連結產生成功後會寫進 Redis（`affiliate:travelpayouts:link:*`），
TTL 由 `affiliate_link_cache_ttl_seconds` 決定，預設 24 小時。
改完目標網址後如果「測試連線」結果沒變，通常是命中快取，不是設定沒生效。

---

## 4. 多語系落地頁怎麼處理

`_render` 不支援語系變數，同一組目標網址會服務 zh-TW / zh-CN / en / ja / ko 五個語系。

**做法：目標網址不要寫死 `locale=` 或 `language=` 參數。**
Booking、Agoda、GetYourGuide 等品牌會依瀏覽器的 `Accept-Language` 自動判斷語系，
留空反而能讓五個語系都拿到正確的落地頁；寫死任一語系則會把其他四個語系的使用者導到錯誤版本。

若日後需要站內語系精準對應，做法是讓 `AffiliateContext` 帶上 locale、
在 `_render` 增加 `{locale}` 變數，並由 `/affiliates/options` 傳入 —— 目前未實作。

---

## 5. 簡易模式 vs 完整模式

**簡易模式**：只填「安全備援合作連結」與「允許跳轉網域」。
系統一看到備援連結就判定設定完成（`registry.py:105-113`），五個模組共用同一條通用連結。
可以快速上線，但拿不到模組維度與 `sub_id` 維度的成效資料。

**完整模式**（建議）：token + marker + project ID + 各模組目標網址，
走 Partner Links API 產生帶 `sub_id` 的深層連結，備援連結只在 API 掛掉時頂上。

`sub_id` 由 `uuid5(NAMESPACE_URL, "travel-scanner:affiliate:{user_id}:{search_或_trip_id}:{partner}:{module}")`
產生（`affiliates/router.py:126-129`），對同一組條件穩定不變，且不含明碼個資。
在 Travelpayouts 後台可以用它區分成效來源。

---

## 6. 驗證清單

1. **後台測試連線**：儲存後按「測試連線」。這會真的呼叫 Partner Links API
   （`admin/service.py:1339-1357`，用「東京」+ 45/49 天後的日期、`sub_id="connection-test"`），
   成功顯示「Travelpayouts 合作連結驗證成功」。失敗訊息已自動遮罩金鑰。
2. **狀態 API**：`GET /api/v1/affiliates/status`，`travelpayouts` 應為
   `enabled: true, configured: true, available: true`。
3. **前台實測**：登入 → 執行一次搜尋 → 搜尋結果頁應出現「更多合作平台 / 整趟旅程合作平台」
   區塊與分潤揭露文字，點擊後 303 導向 `*.tp.st`。
4. **落庫確認**：`affiliate_clicks` 應新增一列，`partner='travelpayouts'`、
   `target_host` 為 tp.st 網域。該表有 append-only trigger，只能新增不能改刪。
5. **後台成效**：`/admin/analytics` 的「聯盟外連」為 `affiliate_clicks` 的權威計數。

純後台填值**不需要重新部署** —— `load_runtime_settings` 每次請求都重讀資料庫。

---

## 7. 何時加開直接方案

當某個品牌的月成交量穩定後，直接方案的抽成會優於透過 Travelpayouts 分潤。
2026 年行情供參（實際以各平台合約為準）：

| 平台 | 行情 | Cookie | 提領門檻 | 後台要填的識別碼欄位 |
|---|---|---|---|---|
| Klook | 基本 5%，月銷達標可加碼至 15% | 30 天 | PayPal US$50 / 銀行 US$500 | 僅需合作連結範本 |
| KKday | 階梯 2%–5.5% | — | 銀行轉帳 US$200 | `kkday_cid` → 自動注入為 `cid` |
| Agoda | 4%–7% | **僅 1 天** | — | `agoda_cid` → 自動注入為 `cid` |
| Trip.com | 飯店約 4.4%–5.9%，國際線機票約 3.5% | 30 天 | 依網路而定 | 僅需合作連結範本 |
| Booking.com | 其佣金的 25%–40%（約成交額 4%–8%） | 短 | €100 | `booking_affiliate_id` → 自動注入為 `aid` |

識別碼的自動注入邏輯在 `affiliates/service.py:167-172`：
`kkday` / `agoda` 注入 `cid`，`booking` 注入 `aid`，且採 `setdefault` —— 範本裡已有的參數不會被覆寫。

Skyscanner 與 Airalo 走 Impact 平台，只需填入 Impact 產生的文字連結。
Skyscanner 的合作申請清單見 [`skyscanner-partnership-application.md`](skyscanner-partnership-application.md)。

---

## 8. 已知落差與後續建議

1. **分潤揭露只有繁體中文。** `affiliates/router.py:40` 的 `DISCLOSURE` 與 `:161` 的 CTA 文案
   都是硬編碼中文，EN / JA / KO 使用者會看到中文揭露句。多語系並重的前提下，
   這是合規面應優先補上的一項（需搬進 next-intl 訊息檔）。
2. **聯盟選項目前只出現在搜尋頁，且需登入。** 掛載點在
   `search-experience.tsx:1175-1189`（整趟旅程）與 `:1225-1233`（單模組）。
   下列外連完全沒有包分潤，是目前最大的漏財點：
   - `hotel-offer-card.tsx:118` 的「前往供應商」
   - `airbnb-search-panel.tsx` 的硬編碼 Airbnb 連結
   - `flight-offer-card.tsx:157` 非 Skyscanner 供應商的 fallback
   - `hotspot-explorer.tsx` / `hotspot-restaurants-panel.tsx` / `food-merchant-card.tsx` 的官網與地圖連結
3. **航班 clickout 的網域驗證較寬鬆。** 見 [`security-audit-2026-09.md`](security-audit-2026-09.md)
   的 API-14（Low）：`search/router.py` 的 303 轉址只驗 HTTPS，沒有 affiliate 流程的網域白名單。
