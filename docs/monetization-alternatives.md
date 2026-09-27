# AdSense 以外的收入方案

2026-09-24。AdSense 在 2026-09-23 以「缺乏價值的內容」退件後，站主要一份 AdSense 以外的規劃，
四個方向都要評估：其他廣告聯播網、擴大分潤、直接贊助（自售版位）、自有產品與讀者支持。
這是評估，不是實作；後續工作在 `tasks/open/` 的六張票，見第八節。

外部方案的條款以 2026-09-24 讀到的官方頁為準，第九節列出來源。只在第三方網站找到的數字標「（第三方）」，
找不到的標「未查證」。各方案會改條款，加入前要重讀。

## 一、結論

**現在就能做、又不必在站上放第三方腳本的，是分潤與讀者支持。其他展示廣告聯播網以現在的流量幾乎都進不去，
進得去的也多半要審內容品質。**

建議順序：

1. **先補量測**：目前量不出每篇文章的瀏覽量（第六節），任何方案都比較不了。一張 P1 票，改兩個檔案。
2. **旅遊分潤補齊，不用寫程式**：
   - 程式的品牌表裡已經有 Tiqets、Airalo、Kiwitaxi、KKday、Welcome Pickups 等品牌。
     它們在 Travelpayouts 專案 570089 裡都是 Available，現在就能產生連結。
   - 缺的是既有的 P1 票 `2026-09-08-travelpayouts-live-destination-activation`：在後台建品牌列與目的地優惠，並完成驗證。
   - GetYourGuide、Viator 在該專案裡還在「Unlock more」，要等 Travelpayouts 的專案審核（4.1）。
3. **主機商分潤**：站上有 11 份架站教學，對應 8 個主機與網域品牌，其中 10 份有五語系，但沒有一篇放了合作連結。
   讀「在 X 架 WordPress」的人正準備買 X，購買意圖是全站最高的（4.2）。
4. **讀者支持連結**：文章文末放一行 Buy Me a Coffee 連結，收入很少，但幾乎沒有成本（4.4）。
5. **AdSense 複審照 `2026-09-23-reposition-the-site-as-a-travel` 的建議**：
   - 審核期間暫停批次發布。
   - 關於頁補上誰在寫、怎麼使用 AI、怎麼查證。
   - 收錄 4–8 週後再送審。
   這不是替代方案，但只要還想用 AdSense 或任何展示廣告，就得做。
6. **有條件才做**：
   - 自售贊助版位：有廣告主主動來問，或月瀏覽到 3 萬左右（4.3）。
   - 使用次數方案開賣：要先解決金流與發票（4.5）。
   - EthicalAds：開發者向文章月瀏覽到 5 萬（4.6）。
   - Journey by Mediavine：每 30 天有 1,000 個來自美、加、英、澳的 session（4.6）。
7. **不建議**：
   - Ezoic、Raptive、Monumetric、Setupad、Publisher Collective、Taboola、Outbrain、Media.net、ClickForce（4.6）。
   - 日本與韓國的在地聯播網與聯盟（4.7）。

理由一句話：月瀏覽不到 3,000 時，展示廣告就算通過審核，每月也只有 NT$30–180。
成交一筆主機方案或兩三筆訂房的分潤就超過這個數字，而且分潤連結不必在站上放第三方腳本，
也不用動隱私政策、同意框或 CSP（第五節）。

## 二、現況

### 2.1 退件與已做的處理

- **退件**：2026-09-23，原因是「缺乏價值的內容」。技術面沒問題：ads.txt、robots、sitemap、關於／聯絡／隱私頁都正常回應。
- **已做的處理**：PR #702 把全站的站名、描述與首頁改成「旅行與生活的實用指南」，首頁也直接連到文章。
- **站主 2026-09-23 的決定**：生活類主題全部保留、繼續收錄，不用 noindex 藏起來。本文件不重開這個決定。

### 2.2 流量

- 站主估計文章頁每月瀏覽不到 3,000。
- Search Console 的資料從 2026-09-14 才開始，repo 裡沒有任何實測的瀏覽量或國家分布。

### 2.3 內容組成

以 repo 的 `apps/api/app/guides/content/*.json` 計算，2026-09-24：

| 類別 | 份數 | 比例 | 五語系都有 |
| --- | ---: | ---: | ---: |
| 旅遊（攻略、情報、韓國美食特輯） | 174 | 15.6% | 53 |
| AI（教學、名詞、Claude Code／Codex／Gemini 系列、AI 新聞） | 607 | 54.3% | 119 |
| 架站、WordPress、SEO、行銷 | 202 | 18.1% | 20 |
| 科技新聞、軟體、3C | 49 | 4.4% | 31 |
| 理財（含幣圈） | 85 | 7.6% | 16 |
| **合計** | **1,117** | | **239** |

- 878 份只有 zh-TW。
- 2026-09-23 的 sitemap 列了 2,016 個「文章 × 語系」網址（`docs/article-localization/releases/batch024/README.md`）。

### 2.4 現有收入管道

| 管道 | 狀態 |
| --- | --- |
| Travelpayouts（專案 570089） | 已啟用。住宿品牌仍鎖著；33 個目的地的優惠還在等驗證（P1 票） |
| Klook 直簽（AID 134379） | 上線中，文章、城市、行程頁都有按鈕 |
| Stay22 | 上線中，涵蓋 Booking、Agoda、Expedia 的住宿按鈕 |
| 文章合作連結（`partner_link`，PR #450） | Hostinger、博客來已登錄，**1,117 份內容包裡 0 份使用** |
| AdSense | 退件；程式就緒、預設關閉 |
| Skyscanner | 只有申請清單，未申請 |
| 樂天（日本飯店） | 一般連結，沒有分潤 |
| 使用次數方案（NT$199／499／1,299） | 資料表與帳本都在，`purchasable=False`，沒有金流 |

## 三、「低價值內容」退件對其他方案的意義

- **展示廣告聯播網多半不是 Google 的替代品。**
  - 它們賣的廣告需求通常包含 Google Ad Exchange，Google 的發布商政策照樣適用。
  - 經由 MCM 合作夥伴接 Google Ad Manager 也一樣（見來源）。
  - 另外，Mediavine、Raptive 這類都是先人工審網站、再決定收不收。
  - 所以同一批內容換一家送審，不太可能得到不同的結果。
- **分潤、讀者支持、自售贊助都不經過 Google 審核**，這次退件不影響它們。
  但聯盟方案也會看網站，例如 Booking.com 經由 Travelpayouts 審核時要求原創的旅遊內容與兩個月的網站歷史。
  所以內容品質的處理還是有用。
- **`2026-09-23-reposition-the-site-as-a-travel` 的觀察**：
  - 2026-09-14 到 09-22 這九天上了 940 篇，這是最強的低價值訊號，改程式無法抹掉。
  - 要等收錄時間拉長。回填發布日期被否決了：Google 以第一次檢索的日期為準，回填只會像是在操弄。

## 四、各方案評估

共通的程式限制（任何方案都要遵守，出處見 `docs/adsense-feasibility.md` 第四節與 `docs/privacy-data-map.md`）：

- 瀏覽器送出 DNT 或 GPC 時，完全不載入任何第三方腳本。
- Consent Mode 永遠是 denied，全站沒有自己的同意框。
- 腳本 CSP 是強制的，只有 `app/(ads-public)` 裡已發布的文章路由在廣告開啟時才放寬。
- `/share/{token}`、行程、帳號頁永遠不放第三方廣告。
- 一般連結不能帶追蹤參數（存檔時回 `422 content_link_affiliate`），分潤只能走 clickout 或 `partner_link`。

### 4.1 旅遊分潤（最貼近網站本業）

站上的品牌表 `BRANDS`（`apps/api/app/travel_services/registry.py:30`）只接受 Travelpayouts 與 Klook 直簽兩個通路。
所以「經 Travelpayouts」的品牌不用寫程式，另外直簽的品牌則要新增通路。
下表的「570089 狀態」是 2026-09-07 在 Travelpayouts 後台的唯讀查核（`docs/travel-services.md`）。

| 方案 | 570089 狀態 | 台灣個人／出款 | 佣金／cookie | 本站要做什麼 |
| --- | --- | --- | --- | --- |
| Tiqets、Kiwitaxi、Welcome Pickups、GetTransfer、WeGoTrip | **Available** | 同 Travelpayouts | 見各方案頁 | 已在 `BRANDS`；完成 P1 票的品牌列與目的地優惠 |
| Airalo（eSIM） | **Available** | 同 Travelpayouts | Travelpayouts 12%（直簽 Impact 10%）；30 天 | 同上 |
| KKday | **Available**（經 Travelpayouts） | 同 Travelpayouts；直簽 KKpartners 為銀行匯款、US$200 門檻（第三方） | 直簽 2–5.5% 階梯、30 天（第三方）；經 Travelpayouts 的費率未查證 | 先走 Travelpayouts；直簽要在後台填 `kkday_cid`（`apps/api/app/affiliates/registry.py`，登入後的搜尋流程用） |
| GetYourGuide | Unlock more（要專案審核） | 直簽：PayPal 無門檻、銀行 €50；活動結束後才付 | 8% 起；30 天（Awin）、31 天（Travelpayouts）（第三方） | 等解鎖；直簽要新增通路 |
| Viator | Unlock more | 直簽：官方寫「沒有流量或追蹤者門檻」；PayPal 每週無門檻、銀行每月 US$50 | 8%；30 天 | 同上 |
| Trip.com | 無，填完資料就能產生連結 | **US$200 門檻**、美元或港幣匯款、40–60 天 | 飯店 5–7%、活動 1.5–4%；網頁 cookie 30 天 | 已有 `trip_com`；門檻高，排後面 |
| DiscoverCars（租車） | 無 | 銀行或 PayPal，US$200 | 利潤的 70%；**沒有 VAT 或 EIN 時降到 58%**；cookie 365 天 | 站上沒有租車模組，要寫程式；先不做 |
| SafetyWing（旅平險） | 無 | PayPal、銀行、Wise，US$10（第三方） | 保費約 10%，364 天 | 沒有保險模組；先不做 |
| Agoda 直簽 | 未查證 | US$200（第三方） | 4–7%，cookie 1 天（第三方） | 已經經由 Stay22 涵蓋，不必另簽 |
| 樂天 Travel | 經 Rakuten Advertising；台灣能否加入未查證 | 未查證 | 5%（入住完成）、30 天 | 先不做 |

建議：先把 Available 的那幾列接起來（前三列）。GetYourGuide、Viator 等 Travelpayouts 解鎖，
不要為了它們新增直簽通路。Trip.com 等流量上來再做。

### 4.2 主機商與軟體分潤（放進既有的架站與 AI 教學）

站上對應的文章（`apps/api/app/guides/content/`）：

- Bluehost 兩篇、Cloudways 兩篇（其中 SSL 那篇只有 zh-TW），
  FastComet、HostGator、hosting.com、Hostinger、Namecheap、SiteGround 各一篇，
  外加 `managed-hosting-comparison`。
- 另有 46 篇 WordPress 教學與 9 篇網域教學。

**主機商方案**（2026-09-24 查證；Hostinger 為 2026-09-13）：

| 品牌 | 聯盟網路 | 佣金 | cookie | 台灣個人出款 | 對本站要注意的 | 連結網域 |
| --- | --- | --- | --- | --- | --- | --- |
| **SiteGround** | 自營 | 每月 1–5 筆每筆 US$50，筆數越多越高 | 60 天 | PayPal 每週、**無門檻** | 禁品牌字競價；未經核准不得用折扣碼或回饋 | `siteground.com/go/…`，會轉到 `world.`、`us.` 等子網域 |
| **Namecheap** | Impact 或 CJ | 主機與 SSL 35%、網域 20%（只算新客首單） | 30 天 | Impact：銀行或 PayPal，**US$10 起** | 禁品牌字競價；只能用聯盟給的折扣碼 | `namecheap.pxf.io`（Impact）、`www.anrdoezrs.net`（CJ） |
| **hosting.com**（原 A2 Hosting） | FirstPromoter | 首張帳單 50%，**上限 US$400** | 未查證（A2 時期 90 天，第三方） | PayPal 或電匯，US$100 起；**未滿 US$100 的餘額 18 個月後作廢** | 禁競價 hosting.com、A2 hosting | `hosting.com/?fpr=…`（第三方） |
| Hostinger | 自營 | 首購最高 40%，單筆上限 US$300 | 30 天 | （2026-09-13 查證） | **顧客推薦計畫（`REFERRALCODE`）不准放網站**，已寫進 `forbidden_params` | `hostinger.com`（已登錄） |
| FastComet | 自營 | 共享主機每筆 US$50 起，依月筆數分級 | 條款寫「至少 10 天」 | 只有 PayPal、無門檻；W-8BEN 要親筆簽名 | 網址、標題、meta 不能出現 coupon／discount／promo | 經 `affiliate.fastcomet.com` 轉址 |
| Bluehost | Impact | 每筆 US$65 起（限 12 或 36 個月方案） | 30 天 | Impact：PayPal 或銀行；門檻 US$100（第三方） | **成交只在第一筆那個月結束後 90 天內累計**，單筆 US$65 過不了門檻就作廢；揭露要在每頁、不用捲動就看得到 | `bluehost.sjv.io`（第三方） |
| HostGator | Impact | US$65 起 | 未查證（60 天，第三方） | PayPal 或銀行，US$100 | 同 Bluehost 的 90 天累計規則 | `partners.hostgator.com/c/…`（第三方） |
| Cloudways | 自營（條款連到 DigitalOcean） | 每筆 US$50 起，或 US$30＋終身 7% | 90 天 | **US$250 才能以 PayPal 提款** | 客戶付滿兩期帳單才算成交；「Cloudways」要設為否定關鍵字 | `cloudways.com/…?id=…` |

- 七家都不禁止非英文內容，也都不限美國居民領款。
- Impact 支援以新台幣電匯；Bluehost、HostGator、FastComet 要填 W-8BEN。
- 連結網域一律以後台實際產生的為準：Impact 的後台可能給出不同網域。

**建議第一批**：

- SiteGround：單筆就有 US$50，PayPal 無門檻。
- Namecheap：US$10 就能提款；網域是每篇架站教學都會用到的東西。
- hosting.com：費率最高，但要先在後台確認 cookie 天數，也要記得 18 個月作廢的規則。
- Hostinger 已經登錄，站主只要提供聯盟連結即可。

Bluehost、HostGator、Cloudways 在低流量時很可能累積不到提款門檻，等流量上來再加。

**AI 與軟體方案**（2026-09-13 評估 PR #450 時查證；加入前重查）：

- 可用：
  - n8n Cloud：12 個月 30%，禁止一切付費廣告。站上有 `n8n-ai-automation-guide`。
  - Make：12 個月 35%。
  - ElevenLabs：12 個月 22%。站上有 `ai-voice-cloning-elevenlabs`。
  - Gamma（PartnerStack）、Raycast 30%、DigitalOcean（Awin）。
  - Udemy（Impact 10%、cookie 7 天）、Coursera 15–45%。
- 沒有方案或已關閉：Notion、Canva（受邀制）、Zapier、Cursor、Perplexity、Obsidian、OpenRouter。
- **Claude／Anthropic 沒有現金分潤。**

**本站要做什麼**：

- 每個方案在 `CONTENT_PARTNERS`（`apps/api/app/affiliates/content_links.py:51`）加一筆，再加測試。
  `hosts` 一定要用站主後台實際產生的連結來確認：聯盟網路常有獨立的追蹤網域，不能用猜的。
- 在文章裡放 `partner_link` 區塊，每篇最多三個。五個語系都要放，照 skill `content-pipeline` 走審稿與部署後匯入。
- 前端已經會加「合作」徽章與 `rel="sponsored"`，點擊也會記進 `affiliate_clicks`（`sub_id` 以 `cnt_` 開頭、帶文章 slug）。
- 不必載入第三方腳本，也不必改 CSP。

### 4.3 自售贊助版位

- **隱私面最合適**：卡片由站上自己的資料庫渲染，沒有第三方腳本，不必改同意框或 CSP。
- **現在沒有需求**：以不到 3,000 的月瀏覽，廣告主付的錢抵不過開發成本。
- **現有的表不能直接用**：
  - `TravelServiceBrand` 的 CHECK 只允許 `travelpayouts`、`klook_direct`（`apps/api/app/models.py:386`）。
  - 優惠要通過分潤憑證與連結驗證才算就緒。
  - 揭露文字是分潤用語，不是「廣告」。
- **要新增的欄位**：廣告主與素材、「廣告」標示、起訖日、語系與頁面鎖定，以及曝光計數（站上目前完全不記曝光）。
- **業配文**也屬於這一類。依公平會的薦證廣告規範，文章本身要揭露。
  日文標「広告」、韓文標「광고」，連結要加 `rel="sponsored"`。

建議：先不做。票 `2026-09-24-first-party-sponsor-placements-design`（blocked）寫了觸發條件與設計要點。

### 4.4 讀者支持

| 平台 | 手續費 | 台灣出款 |
| --- | --- | --- |
| Buy Me a Coffee | 5%＋Stripe 手續費 | **可以**：經 Stripe Express 付到台灣（說明頁 2026-08-24 更新）；只有 Stripe，沒有 PayPal |
| Ko-fi | 單次贊助 0%（要手動關掉預設的 5%）；其他 5% | 只能用 PayPal：Stripe 不在台灣開帳戶 |
| Portaly | 基本方案 12%、進階方案 6%（年繳 NT$219／月），另加金流費 | **台灣銀行帳戶**，NT$150 起提（第三方） |
| Patreon | 新創作者 10%（第三方），另加金流與 2.5% 換匯 | PayPal 1% 手續費（上限 US$20）、US$10 起；也有 Payoneer；清單沒有明列台灣 |

- 建議用 Buy Me a Coffee 一個就好：五個語系的讀者都付得了錢。想用台灣本地付款方式時才考慮 Portaly。
- 放法：文章文末一行普通連結，不用對方的 widget 腳本。
- 文案不能暗示「點廣告或合作連結支持我們」，這條 AdSense 政策在複審時仍然適用。

### 4.5 自有產品

- **使用次數方案**：
  - 四個方案都已經 seed 在 `apps/api/app/usage/service.py:51-112`。
  - 定價頁的購買按鈕是停用的「購買即將開放」（`apps/web/app/[locale]/pricing/page.tsx:57`）。
  - `grant_package`（`usage/service.py:360`）以 `external_reference` 保證冪等，可以直接接付款回呼。
  - 缺的是金流：Stripe 不在台灣開帳戶。綠界、藍新、TapPay 這類本地金流能不能讓沒有營業登記的個人使用、
    開立發票的義務為何，**本次未查證**，要站主與會計師確認。
  - 此外，只有回訪的規劃器使用者才會買，目前也量不到回訪。建議：先不做。
- **電子報**：站上沒有電子報或 Email 訂閱。LINE 官方帳號只做一對一推播（綁定與到價通知），沒有群發。
  beehiiv 的廣告聯播網要付費方案，而且要 Stripe Express（台灣未查證）；付費訂閱要完整的 Stripe 帳戶，台灣大概不行。
  建議：等有穩定讀者再說。

### 4.6 其他展示廣告聯播網

| 聯播網 | 門檻（2026-09-24） | 腳本與同意框 | 對本站 |
| --- | --- | --- | --- |
| Ezoic | **2026-02-19 起要每月 25 萬使用者**（之前已加入的站不受影響）；另有每月收 20 個小站的 Incubator | 重：header bidding＋CMP | 進不去 |
| Journey by Mediavine | 每 30 天 1,000 個 session，**只算美、加、英、澳** | 重：Grow 外掛＋廣告包裝腳本 | 條件式：英文文章的英語系流量到了再看 |
| Mediavine | 一年 US$5,000 廣告收入 | 重 | 進不去 |
| Raptive | 月瀏覽 2.5 萬（2025-10-16 調降）；10 萬以下要一半流量來自英語系國家；網域要滿 6 個月 | 重 | 進不去 |
| Monumetric | Propel 方案 1–8 萬瀏覽，開通費 US$99；要一半英語系流量、WordPress 或 Blogger（第三方） | 重 | 不符 |
| Media.net | 沒公布門檻；只收英文內容、英語系流量（第三方） | 中 | 不符：主力是 zh-TW |
| Setupad | 代管約 10 萬月訪客（第三方）；自助方案門檻未查證 | 重 | 進不去 |
| Publisher Collective（原 Snigel） | 月瀏覽 300 萬 | 重 | 進不去 |
| Taboola、Outbrain（現 Teads） | Taboola 無官方數字，評論說 50–100 萬（第三方）；Outbrain 由業務審 | 重：外掛＋追蹤 | 進不去；與隱私立場衝突 |
| Google Ad Manager（經 MCM） | 看合作夥伴 | Google 標籤＋Prebid、要 CMP | 仍是 Google 政策 |
| Amazon Publisher Services | 受邀制；而且要先有 Google Ad Manager | 伺服器端 header bidding | 進不去 |
| **EthicalAds** | 月瀏覽 5 萬以上、以開發者為主的網站，人工審核 | **輕**：一支腳本、不追蹤、依內容投放；頁面上只能有它一個廣告 | **唯一符合本站隱私規則的**；等開發者向文章（Claude Code、Codex、Gemini 系列）流量到了再申請 |
| Carbon Ads | 受邀制；英文開發者或設計師受眾；**全站只能有它一家廣告** | 輕 | 暫不 |
| ClickForce 域動（台灣） | 未公布 | 中到重：自家標籤加 Google、Criteo 等競價 | 條款不明，暫不 |

就算日後要換一家，程式的代價也是中等：

- **可以沿用**：`app/(ads-public)` 的獨立 document、`adsenseRequestGate`、已發布文章檢查、
  版位演算法 `adsensePlacements`、預留高度的版位框，以及文章路由上已經放寬到 `https:` 的 CSP。
- **Google 專用、要重寫**：載入器 `components/ads/adsense-loader.tsx`、`<ins class="adsbygoogle">`、
  ID 驗證、`anchor-ad-offset.tsx`、`/ads.txt` 的內容。
- **要跟著改**：五語系隱私政策（`apps/api/app/site_pages/drafts/*.json`）、EEA 的 CMP，
  以及 e2e fixture（新的設定端點要回「關閉」，否則 `admin-operations` 與 `korea-dual-maps` 會紅）。

### 4.7 日本與韓國的在地方案

| 方案 | 擋住的條件 |
| --- | --- |
| A8.net | 海外居民要有**日本銀行帳戶與日本聯絡地址**，而且網站要是日文 |
| ValueCommerce、もしもアフィリエイト、i-mobile | 要日本銀行帳戶 |
| 忍者AdMax | 付到日本銀行或 PeX（日本點數）；海外居民未查證 |
| 楽天アフィリエイト | 以楽天 Cash 支付，**每月超過 ¥3,000 的部分作廢**，除非有日本的楽天銀行或楽天卡；楽天銀行無法從海外開戶（第三方） |
| Kakao AdFit | 韓國身分驗證，只付到帳戶本人名下，₩50,000 起 |
| Coupang Partners | 要韓國手機號碼（第三方） |
| LinkPrice | 出款要韓國手機身分驗證 |

結論：ja 與 ko 頁面改用全球性的方案（4.1 的 Travelpayouts 品牌、Klook、KKday）。
另外，2026-09-22 韓國國家人權委員會認定某聯盟公司全面拒絕外國人屬於歧視，
但它建議的改法仍然以韓國外國人登錄號與韓國銀行帳戶為前提，對本站沒有幫助。

### 4.8 台灣聯盟網（給 zh-TW 讀者）

| 方案 | 門檻 | 資格／出款 | 形式 |
| --- | --- | --- | --- |
| 聯盟網 Affiliates.One | 無 | 可；NT$1,000 起、匯費 NT$30、單次超過 NT$2 萬要扣繳（第三方） | 純連結；KKday 3.5%（直簽 KKpartners 較高） |
| 通路王 iChannels | 要有網站或社群帳號 | **限 18 歲以上的中華民國國民**；NT$500 起，每月 5–15 日付款（第三方） | 純連結；CPS 或 CPL |
| 蝦皮分潤計畫 | 無，但要審核 | 可；NT$500 起（第三方） | 純連結；站外推廣最高 10%，歸因 7 天（第三方） |

- 適合 zh-TW 的 3C、軟體、書籍類文章。
- 這些聯盟網的連結會先經過它們自己的轉址網域，所以只能放在 `partner_link`，
  而 `CONTENT_PARTNERS` 要登錄它們的轉址網域。
- 排在主機商分潤之後。

## 五、收益比例感

以下數字都是假設，用來比大小，不是預測。站上目前沒有任何轉換資料。

| 來源 | 假設 | 一次或一個月 |
| --- | --- | --- |
| 展示廣告（假設通過審核） | 月瀏覽 3,000 × RPM NT$10–60（`docs/adsense-feasibility.md` 第五節） | **NT$30–180／月** |
| 訂房 | NT$8,000 × 4% | 約 NT$320／筆 |
| 一日遊 | NT$2,000 × 8%（GetYourGuide、Viator 解鎖後的費率） | 約 NT$160／筆 |
| eSIM | NT$500 × 12%（Airalo 經 Travelpayouts） | 約 NT$60／筆 |
| 主機方案 | SiteGround 每筆 US$50；hosting.com 首張帳單 50%、上限 US$400；Namecheap 網域 20%（見 4.2） | 主機一筆約 NT$1,500 起；單買網域只有幾十元 |
| 讀者支持 | 一杯咖啡約 US$3–5，扣手續費 | 零星 |

一個月只要成交一筆主機方案，或兩三筆訂房，就超過展示廣告整個月的收入。
而分潤的量只跟「讀者有沒有要買」有關，不像展示廣告那樣和瀏覽量成正比。所以在低流量階段，分潤的效益比較高。

## 六、量測缺口

1. **每篇文章的瀏覽量量不到。**
   - `apps/api/app/analytics/service.py:80`（`_UUID_OR_TOKEN`）與 `apps/web/components/analytics-provider.tsx:45`（`sanitizedPath`）
     會把 20 字元以上的路徑段改成 `:id`，用意是擋掉分享 token 與 UUID。
   - 但 1,117 份文章裡約 998 份的 slug 也有那麼長，瀏覽量全部併成 `/life/:id` 或 `/guides/howto/:id`。
   - 票：`2026-09-24-article-page-views-keep-the-article`（P1）。
2. **分潤點擊已能歸到文章**（PR #565 合併），但還沒用正式站的真實點擊驗收。
   票 `2026-09-12-attribute-affiliate-clicks-to-the-guide` 仍是 blocked。
3. **沒有曝光紀錄。** 只有自售贊助需要，現在不必做。
4. **分潤收入不會回傳到站上**，只存在各夥伴的後台。
   - 建議站主每月初記一次：各夥伴的訂單數與佣金，對照後台 `/admin/analytics` 的分潤點擊報表（依 partner、placement、文章）。
   - 有了第 1 項之後，就能算出每篇文章的「點擊率」與「每千次瀏覽的分潤」。

## 七、站主要決定的事與申請清單

### 7.1 決定

| # | 決定 | 建議 | 替代方案與代價 |
| --- | --- | --- | --- |
| D1 | 加入哪些方案 | 第一批：Travelpayouts 裡已是 Available 的品牌（Tiqets、Airalo、Kiwitaxi、KKday 等）；主機商 SiteGround、Namecheap、hosting.com，加上已登錄的 Hostinger（4.2）。第二批：GetYourGuide、Viator（等 Travelpayouts 解鎖）、Trip.com、通路王、蝦皮、AI 工具方案 | 一次全加：管理成本高，多數方案在低流量下不會有成交 |
| D2 | 架站文章放合作連結的原則 | 只放文章教的那一家；每個語系一個 `partner_link`，放在讀者要註冊的那一步；比較文要嘛每家都放、要嘛都不放；文章的評價與建議不因分潤改寫 | 每篇放滿三個：點擊可能多一點，但讀起來像業配，也是 AdSense 複審的扣分項 |
| D3 | 讀者支持平台 | Buy Me a Coffee，一個就好 | Portaly：台灣讀者付款方便，但海外讀者不便；兩個都放：選擇太多反而沒人點 |
| D4 | 使用次數方案要不要開賣 | 先不要；等規劃器有回訪使用者，而且發票問題問過會計師 | 現在開賣：要接金流、改法律頁，可能沒人買 |
| D5 | 自售贊助 | 不主動招商；有廣告主來問時才做設計票 | 現在就做：開發成本大於可能的收入 |

跟這些決定並行、不必再決定的：審核期間暫停批次發布，是 `2026-09-23-reposition-the-site-as-a-travel` 已經給的建議。

### 7.2 站主的申請清單（不用寫程式）

1. **Travelpayouts**（專案 570089，mokaair.com）：
   - 確認 Tiqets、Airalo、Kiwitaxi、KKday 仍是 Available。
   - 接著讓既有的 P1 票 `2026-09-08-travelpayouts-live-destination-activation` 在後台建品牌列與目的地優惠，並完成驗證。
   - 順便看 GetYourGuide、Viator 解鎖了沒有。
2. **KKpartners**（可以晚點再做）：KKday 直簽的費率可能比經 Travelpayouts 高。拿到 CID 後填進後台的 `kkday_cid`。
3. **主機商聯盟**：依 4.2 的建議加入，並把 mokaair.com 登記成推廣網站。
   - 把後台產生的一條實際連結交給票 `2026-09-24-hosting-affiliate-links-in-the-hosting`。
   - 不要用顧客推薦計畫的連結（例如 Hostinger 的 `REFERRALCODE`），條款禁止放在網站上。
4. **Buy Me a Coffee**：開帳戶、設定 Stripe Express 出款，把頁面網址交給票 `2026-09-24-reader-support-link-at-the-end`。
5. **每月初**：照第六節第 4 點記一次各夥伴的訂單與佣金。

稅務：多數國外方案要填美國稅表（非美國個人通常是 W-8BEN），模型不能代填。

## 八、後續票

| 票 | 狀態 | 內容 |
| --- | --- | --- |
| `2026-09-24-article-page-views-keep-the-article` | open P1 | 公開文章的瀏覽量保留 slug，分享 token 等照舊折成 `:id` |
| `2026-09-24-hosting-affiliate-links-in-the-hosting` | blocked P2（等 D1、D2 與站主加入方案） | `CONTENT_PARTNERS` 登錄主機商方案，11 份架站教學放 `partner_link` |
| `2026-09-24-travelpayouts-drive-loads-on-share-token` | open P2 | 順帶發現：Travelpayouts Drive 在 `/share/{token}` 也會載入，第三方腳本讀得到秘密網址 |
| `2026-09-24-reader-support-link-at-the-end` | blocked P3（等 D3） | 文章文末的讀者支持連結 |
| `2026-09-24-first-party-sponsor-placements-design` | blocked P3（等 D5） | 自售贊助的設計文件；觸發條件：有廣告主來問或月瀏覽約 3 萬 |
| `2026-09-24-take-payment-for-the-usage-packs` | blocked P3（等 D4） | 使用次數方案接金流 |

相關的既有票：

- `2026-09-08-travelpayouts-live-destination-activation`（P1）：旅遊品牌與目的地優惠的驗證。
- `2026-09-12-attribute-affiliate-clicks-to-the-guide`（blocked）：文章歸因的正式站驗收。
- `2026-09-23-third-party-scripts-on-privileged-routes`（P2）：同一支 Drive 腳本在後台與帳號頁的問題，建議與分享頁那張一起做。
- `2026-09-13-adsense-auto-ads-overlay-setup`：要等 AdSense 重新通過審核才有意義。

## 九、來源

2026-09-24 讀取。

展示與原生廣告：

- [Ezoic 加入條件](https://support.ezoic.com/)（Getting Started: Ezoic's Requirements）、[Ezoic Incubator](https://www.ezoic.com/incubator)
- [Mediavine 與 Journey 加入條件](https://www.mediavine.com/mediavine-requirements/)
- [Raptive 門檻調整公告（2025-10-16）](https://raptive.com/blog/)
- [Monumetric Propel](https://www.monumetric.com/propel-payment/)
- [Setupad FAQ](https://setupad.com/faq/)
- [Publisher Collective FAQ](https://publisher-collective.com/faq/)
- [Outbrain 流量門檻說明](https://www.outbrain.com/help/publishers/outbrains-minimum-traffic-requirement/)
- [Google Ad Manager MCM](https://support.google.com/admanager/answer/11130475)
- [Amazon Publisher Services UAM](https://aps.amazon.com/aps/solutions/unified-ad-marketplace/)
- [EthicalAds 發布商](https://www.ethicalads.io/publishers/)、[EthicalAds 發布商政策](https://www.ethicalads.io/publisher-policy/)
- [Carbon Ads FAQ](https://www.carbonads.net/faq)
- [BuySellAds 發布商](https://www.buysellads.com/publishers)
- [ClickForce](https://www.clickforce.com.tw/)
- [AdSense 在 EEA／英國／瑞士的同意管理要求](https://support.google.com/adsense/answer/13554116)

旅遊分潤：

- [GetYourGuide 合作夥伴說明](https://partner.getyourguide.support/)
- [Viator 合作夥伴資源](https://partnerresources.viator.com/)
- [Trip.com 聯盟方案問答](https://www.trip.com/ask/questions/trip.com-affliate-program.html)
- [DiscoverCars 聯盟條件](https://www.discovercars.com/affiliate-conditions)
- [Holafly 聯盟方案](https://esim.holafly.com/affiliate-program/)
- [SafetyWing Ambassador](https://hello.safetywing.com/ambassador-page)
- [樂天 Travel 聯盟](https://travel.rakuten.co.jp/en/en_affiliate.html)
- [KKpartners](https://kkpartners.kkday.com/)（頁面由腳本產生，數字取自第三方整理）

台灣、日本、韓國：

- [通路王會員資格](https://www.ichannels.com.tw/main-member.php)
- [蝦皮分潤計畫說明](https://help.shopee.tw/)（文章 145785）
- [A8.net FAQ](https://support.a8.net/)、[ValueCommerce FAQ](https://www.valuecommerce.ne.jp/)、[もしもアフィリエイト](https://af.moshimo.com/)
- [楽天アフィリエイト FAQ](https://affiliate.faq.rakuten.net/)（000009938）
- [忍者AdMax](https://admax.shinobi.jp/)、[i-mobile 說明](https://www.i-mobile.co.jp/help_partner_sp.html)
- [Kakao AdFit 使用說明](https://adfit.kakao.com/web/html/use_kakao.html)、[LinkPrice](https://www.linkprice.com/)

讀者支持：

- [Buy Me a Coffee 出款國家](https://help.buymeacoffee.com/)（文章 6258038，2026-08-24 更新）
- [Ko-fi 手續費說明](https://help.ko-fi.com/)
- [Patreon 美國以外創作者的出款](https://support.patreon.com/)
- [Portaly 訂閱平台比較（2026-02-26）](https://portaly.cc/blog/subscription-platform)
- [beehiiv Ad Network FAQ](https://www.beehiiv.com/support)
- [Stripe 支援的國家](https://stripe.com/global)

主機商：

- [SiteGround 聯盟](https://www.siteground.com/affiliates)、[SiteGround 佣金說明（2025-08-07）](https://www.siteground.com/kb/affiliate_program_earnings/)
- [Namecheap 聯盟](https://www.namecheap.com/affiliates/)、[Namecheap 聯盟協議](https://www.namecheap.com/legal/affiliate-program/affiliate-agreement/)
- [hosting.com 聯盟](https://hosting.com/about/affiliate-program/)、[hosting.com 聯盟政策（2026-08-28）](https://terms.hosting.com/affiliate-policy)
- [FastComet 聯盟](https://www.fastcomet.com/affiliate)、[FastComet 聯盟條款（2025-10-28）](https://www.fastcomet.com/terms/affiliate)
- [Bluehost 聯盟](https://www.bluehost.com/affiliates)、[Newfold 聯盟協議](https://legal.newfold.com/NewfoldAffiliateAgreement.pdf)
- [HostGator 聯盟](https://www.hostgator.com/affiliates)、[HostGator 聯盟 FAQ](https://www.hostgator.com/help/article/affiliates-faq)
- [Cloudways 聯盟](https://www.cloudways.com/en/web-hosting-affiliate-program.php)、[DigitalOcean 聯盟協議](https://www.digitalocean.com/legal/affiliate-program-agreement)
- [Impact 支援的出款幣別](https://help.impact.com/)

AI 與軟體方案、Hostinger：2026-09-13 評估 PR #450 時查證，當時沒有留下網址；加入前請重讀各方案的官方條款。
