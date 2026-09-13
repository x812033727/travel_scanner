# Google AdSense 可行性評估

2026-09-13。問題是「文章分享加入 Google 廣告的可能性」。本文以 **AdSense**（在自己的頁面放 Google
展示廣告賺錢）為主，另附一節 **付費 Google Ads 導流**。這是評估，不是實作；後續工作在
`tasks/open/` 的五張票，見第八節。

政策內容以 2026-09-13 讀到的 Google 說明頁為準，Google 會改政策，動手前要重讀第十節的來源。
站上數據是當天對正式站 `https://mokaair.com` 發 GET 查證的結果。

## 一、結論

**可以做，但現在不建議申請或上線。**

建議順序：

1. 先把法律頁發布（任務 `2026-09-06-legal-content-from-owner`）。
2. 站主決定第六節的 D1–D5，尤其是隱私立場（D1）與 CSP 取捨（D5）。
3. 到後台 `/zh-TW/admin/analytics` 看文章頁的實際瀏覽量；月瀏覽量到 1 萬左右再申請。
4. 上線時只在文章頁放 1–2 個手動版位，並量測分潤點擊率有沒有掉。

理由一句話：以目前的內容量與流量，廣告收入每月大概是零到幾百台幣（第五節），
換來的是改寫隱私政策、放寬 CSP、跟分潤搶點擊、版面與效能風險，外加一條新的測試與維運負擔。

## 二、「文章分享」在站上是哪些頁

| 頁面 | 路由 | 正式站現況 | 適不適合放廣告 |
| --- | --- | --- | --- |
| 旅遊情報攻略 | `/{locale}/guides/{intel,howto}/{slug}` | 30 篇，**全部只有 zh-TW**；repo 內容包 30 個，28 個含 offer 區塊 | **適合**：伺服器渲染、可索引、有實質內容 |
| 生活分享 | `/{locale}/life/{slug}` | 0 篇 | 要等有文章 |
| 文章 hub（非 zh-TW） | `/{en,ja,ko,zh-CN}/guides`、`/guides/{kind}`、`/life` | 顯示「Nothing is published here yet.」，沒有 robots meta，canonical 指向自己，而且在 sitemap 裡 | **不行**：屬於「無內容畫面」 |
| 行程分享頁 | `/{locale}/share/{token}` | noindex、robots 擋 `/*/share/`、client 空殼 | **不建議**：見 4.6 |
| 社群 | `/{locale}/community/...` | 總開關關閉、全部 noindex | **不行** |

兩個文章區共用 `components/guides/article-page.tsx` → `components/guides/article.tsx`。

## 三、AdSense 的門檻與本站現況

| 項目 | 政策要求 | 本站現況 |
| --- | --- | --- |
| 資格 | 年滿 18、擁有網站並能改 HTML、內容原創且有價值 | 符合；內容風險見本節末 |
| 驗證網站 | 三擇一：AdSense 程式碼、`ads.txt` 片段、meta tag | `https://mokaair.com/ads.txt` 回 **404** |
| 隱私權政策 | 必須揭露「Google 等第三方供應商使用 cookie，依使用者先前造訪投放廣告」，並提供退出管道（廣告設定或 aboutads.info） | 正式站 `/zh-TW/privacy` 仍顯示「**內容準備中**」；五語系草稿**完全沒提廣告**（`docs/privacy-data-map.md:291-293`） |
| 歐洲同意 | EEA／英國（2024-01-16 起）與瑞士（2024-07-31 起）投放**個人化廣告**要用 Google 認證、整合 IAB TCF 的 CMP；Google 自家「隱私權與訊息」就是認證 CMP | 沒有任何 CMP 或同意 UI |
| 無內容畫面 | 不能在無內容或低價值內容、施工中、純導覽用途的畫面放廣告；**不能在未經人工審核或編修的自動產生內容放廣告** | 非 zh-TW 的 hub 是空頁；分享頁是 AI／使用者產生的行程 |
| 標示 | 只能標「廣告」（Advertisements）或「贊助連結」（Sponsored links），不能用「推薦網站」之類的字眼 | 站上沒有這個標籤 key |
| 放置 | 不能放在導覽、下載、播放等互動元素旁邊，不能讓旁邊的內容排得像廣告 | 文章裡的分潤按鈕就是互動元素 |
| 無效點擊 | 不能自己點，也不能請人點（包括「支持我們」這類字眼） | — |
| AdSense 爬蟲 | `Mediapartners-Google` **忽略** robots.txt 的 `*` 群組 | 不必改 `app/robots.ts`；另外 `app/robots.test.ts:66` 要求 `*` 以外的群組都是 `disallow: "/"`，加 allow 群組會失敗 |

**內容審核風險。** 這 30 篇是撰稿代理寫的，雖然每個數字都查過來源，但 AdSense 對「自動產生內容」的限制看的是
有沒有人工審核或編修。新站也常被判「低價值內容」而退件。申請前，站主要真的審閱過文章，
about／contact 頁也要上線（兩者都在同一個法律頁任務裡）。

## 四、跟本站現有設計的衝突

### 4.1 隱私立場

站上的設計刻意不做廣告追蹤：

- GA4 的 Consent Mode 四項（`analytics_storage`、`ad_storage`、`ad_user_data`、`ad_personalization`）**永遠是 denied**，
  整個 repo 沒有 `gtag("consent","update")`（`components/analytics-provider.tsx:59`，`docs/privacy-data-map.md:117-120`）。
- 瀏覽器送出 DNT 或 GPC 時，GA4、Travelpayouts Drive、Stay22 一律不載入（`components/analytics-provider.tsx:32-34`、
  `components/travelpayouts-drive.tsx:17-24`、`lib/stay22-script.ts:33-35`）。
- `next.config.ts:14` 的 `Permissions-Policy` 關掉 `browsing-topics`。
- 分潤 `sub_id` 只能是粗粒度的目錄標籤（`apps/api/app/affiliates/sub_id.py`）。
- 第三方腳本的前例是 Stay22：放在**另一個 root document**，裡面沒有 session、Email 或私人行程，
  理由是「移除 React `<Script>` 收不回已經執行的第三方 observer、timer」（`docs/stay22-module-switch.md:41-62`）。

AdSense 的衝突點：

- **非個人化廣告仍然會用 cookie**：Google 的說法是非個人化廣告不拿 cookie 做鎖定，
  但仍用來做頻率上限與彙總報表。所以不管選哪種廣告，隱私政策都一定要改。
- 文章頁跟帳號、行程共用同一個 root layout。讀者看完文章後用 client-side 導覽進私人頁面時，
  已經執行的廣告腳本還留在同一個 document 裡。要比照 Stay22 的前例處理：
  私人頁面的連結用整頁導覽，或者把有廣告的文章頁搬到獨立的 route group。
- `docs/travel-guides.md:98-100` 寫「文章永遠不會讓讀者的瀏覽器向第三方抓圖」，放了廣告就不成立，文件要跟著改。

### 4.2 CSP

- Google 的 AdSense CSP 說明**只支援 nonce 式的嚴格 CSP**，建議
  `script-src 'nonce-{random}' 'unsafe-inline' 'unsafe-eval' 'strict-dynamic' https: http:`。
  官方不支援網域白名單，因為廣告程式碼用的網域會變；還說「更嚴格的政策可能在沒有通知的情況下壞掉」。
- 本站的嚴格 CSP 在 `apps/web/lib/csp.ts:51-81`，由 `apps/web/proxy.ts` 逐請求產生：
  - 目前只是 **Report-Only**，強制的只有 `next.config.ts` 的 baseline（`frame-ancestors`／`object-src`／`base-uri`／`form-action`）。
  - `docs/security-audit-2026-09.md:210` 計畫把它改成強制。
  - `lib/csp.test.ts:46` 斷言 production **不含 `'unsafe-eval'`**。
  - `lib/csp.test.ts:9` 把 `frame-src` 寫死成精確字串；`connect-src` 也是白名單。
- 所以一旦 CSP 轉成強制，AdSense 需要 `'unsafe-eval'`，`frame-src`／`connect-src` 也要放寬到 `https:`，
  否則「可能沒有通知就壞掉」。可行做法是只對有廣告的文章路由產生放寬版 CSP，其他頁維持嚴格。
  這是資安取捨，要站主決定（D5）。

### 4.3 分潤

- 30 篇裡 28 篇有 offer 區塊（Klook 直簽、Stay22 住宿按鈕），另外文末還有自動合作區塊。
- AdSense 會在同一頁出現 Klook、KKday、Agoda、Booking、Trip.com 這類旅遊廣告主，把本來會走分潤的點擊帶走。
  比例感：一筆 NT$8,000 的訂房，分潤 4% 約 NT$320；以第五節的 RPM 換算，這相當於 5 千到 3 萬次瀏覽的廣告收入。
- 對策：
  - 在 AdSense「封鎖控制項」封鎖跟分潤夥伴重疊的廣告主網址（D4）。
  - 版位不要貼著 offer 區塊。這既是政策（互動元素旁），也是生意。
  - 上線前後比較文章頁的分潤點擊率。這需要任務 `2026-09-12-attribute-affiliate-clicks-to-the-guide` 先把點擊記到文章。

### 4.4 測試

- 8 支 e2e 規格斷言「零外部請求」：`site-experience`、`stay22-script`、`stay22-allez`、`discovery-card-details`、
  `admin-operations`、`korea-dual-maps`、`planner-route-tones`、`food-map-reservations`；
  `travel-services` 另外攔截 `https://tp.st/**`。其中 `stay22-script` 用 `https://mokaair.com` 當 origin 跑：
  載入器如果靠執行期的 `location.origin` 判斷是不是正式站，在這支規格裡會真的發出請求而失敗。
- 離線 fixture `tools/e2e-runtime-api.mjs:216` 回傳固定的 analytics config，未知端點一律 404。
  如果瀏覽器在這些規格走過的頁面去打新的設定端點，404 會讓 `admin-operations`（計算本站 4xx 回應）
  與 `korea-dual-maps`（計算 console 錯誤）失敗。
- 結論：廣告設定預設關閉、只在文章頁載入，fixture 要回「關閉」。

### 4.5 版面與效能

- 文章頁是單欄 `max-w-3xl`，hero 圖是 LCP，已預留寬高（`article.tsx:116-137`）。
- 手機版有 `sticky top-0 z-40` 的 header（`components/site-header.tsx:8`）和 z-index 60 的固定底部導覽
  （`app/globals.css:606`），會跟 AdSense 的錨定廣告、插頁廣告撞在一起 → 自動廣告要關掉這兩種（D3）。
- 站上沒有 web-vitals 回報、Lighthouse CI 或 CLS 測試（Lighthouse 是還沒做的 `2026-09-10-seo-lighthouse-workflow`）。
  CLS 要用 Playwright 在頂層頁量，而且要先跑一個故意位移的對照頁；內建瀏覽器 pane 永遠量到 0。

### 4.6 不該放廣告的頁

- **行程分享頁**：網址本身就是秘密 token（`/share/{token}`），同頁的第三方腳本讀得到它；
  頁面是 noindex（`app/[locale]/share/[token]/page.tsx:10`），伺服器只送空殼，內容是 AI 或使用者產生的行程。
  既有隱私風險，也碰到「自動產生內容」的政策。
- **社群**：總開關關閉，全部 noindex。
- **非 zh-TW 的文章 hub**：空頁。另外，這些頁可索引又在 sitemap 裡，本身也是 SEO 問題（已開票，見第八節）。
- **中國大陸的訪客**：Google 網域被封鎖，zh-CN 讀者若在中國大陸，本來就看不到廣告。

## 五、收益估算

公式：**月收入 ≈ 文章頁月瀏覽量 × RPM ÷ 1,000**。

台灣展示廣告的 RPM 約 **NT$10–60**（台灣部落客公開的收入整理，非官方數字，依主題差很多）。

| 文章頁月瀏覽量 | 每月估計收入 |
| --- | --- |
| 3,000 | NT$30–180 |
| 10,000 | NT$100–600 |
| 50,000 | NT$500–3,000 |
| 300,000 | NT$3,000–18,000 |

- 付款門檻 **US$100**（約 NT$3,000），累積到才會匯款。
- 只放非個人化廣告時 RPM 會更低；沒有認證 CMP 時，EEA／英國／瑞士的訪客只會收到非個人化或限制型廣告。
- 目前 30 篇只有 zh-TW，en／ja／ko 的高 RPM 市場沒有文章可放。

## 六、站主要決定的事

| # | 決定 | 建議 | 替代方案與代價 |
| --- | --- | --- | --- |
| D1 | 隱私立場 | 全站只放**非個人化廣告**；DNT／GPC 時完全不載入；**不裝 CMP**（EEA／英國／瑞士只會收到非個人化或限制型廣告） | 個人化廣告＋Google「隱私權與訊息」CMP：RPM 較高，但要加同意 UI、改更多政策文字，也違背現在「consent 永遠 denied」的設計 |
| D2 | 申請時機 | 法律頁已發布，而且文章頁月瀏覽量 ≥ 1 萬 | 現在就申請：可能因「低價值內容」或缺隱私政策被退件 |
| D3 | 版位 | 手動 in-article 1–2 個：不放第一屏、不貼著 offer 區塊；自動廣告關閉錨定與插頁 | 全開自動廣告：省工，但版面與分潤風險最大 |
| D4 | 廣告主封鎖 | 封鎖跟分潤夥伴重疊的旅遊廣告主（Klook、KKday、Agoda、Booking、Trip.com、Expedia 等） | 不封鎖：廣告收入稍高，分潤點擊可能下降 |
| D5 | CSP | 只有有廣告的文章路由用 AdSense 版 CSP，其他頁維持嚴格 | 全站放寬：最簡單，但整站失去 `'unsafe-eval'` 限制 |

## 七、站主的操作步驟（不用寫程式的部分）

1. 用 Google 帳號申請 AdSense，網站填 `mokaair.com`，取得發布商 ID `ca-pub-` 加 16 位數字。
2. 用 `ads.txt` 片段驗證。檔案要部署到 `apps/web/public/ads.txt`，內容一行
   `google.com, pub-<16 位數字>, DIRECT, f08c47fec0942fa0`；`proxy.ts:28` 的 matcher 會跳過含點的路徑，所以不會被語系導向。
   這一行可以先單獨出一個小 PR，不必等版位那張票。**審核期間不需要在頁面放廣告程式碼。**
3. 送審前確認隱私權政策（含第四節的廣告揭露）、about、contact 已發布。
4. 審核通過後，在「隱私權與訊息」設定非個人化廣告（依 D1），在「封鎖控制項」封鎖 D4 的廣告主，
   在自動廣告關閉錨定與插頁（依 D3），再建立 1–2 個廣告單元並取得 slot ID。
5. 付款設定：在 AdSense 填美國稅務資料（非美國個人通常是 W-8BEN）；
   收入到 US$10 時 Google 會用國際平信寄 6 位數 PIN 碼到付款地址（通常要 3 週），4 個月內要輸入完成。
6. 上線後兩週，比較文章頁分潤點擊率與 CLS，再決定要不要保留。

## 八、實作概要與後續票

| 票 | 狀態 | 內容 |
| --- | --- | --- |
| `adsense-privacy-policy-section` | blocked（等 D1、法律頁任務） | 五語系同結構的廣告揭露區塊；正式站已初始化後改草稿無效，要在後台逐語系改版發布 |
| `adsense-admin-config` | blocked（等 D1–D3） | 後台設定（開關、`ca-pub` 驗證、slot ID、非個人化）與匿名公開設定端點，預設關 |
| `adsense-article-slot` | open，依賴上面兩張與分潤點擊歸因任務 | 文章頁版位、載入器、文章路由 CSP、`ads.txt`、e2e fixture、CLS 量測 |
| `guides-empty-locale-hubs-indexable` | open | 這次順帶發現：非 zh-TW 的空 hub 可索引又在 sitemap 裡 |
| `google-ads-conversion-measurement` | blocked（等站主決定要投放） | 付費導流需要的轉換量測 |

實作時要沿用的前例：

- 匿名公開設定端點比照 `GET /travel-services/stay22-script-config`：匿名、`no-store`、尊重 DNT／GPC、
  只回有效狀態與驗證過的 ID，web 端在伺服器讀（`lib/stay22-script.server.ts`）。
  `GET /runtime/public-config` 需要登入，文章讀者拿不到。
- 伺服器端決定要不要輸出版位：讀設定，加上請求的 `Sec-GPC`／`DNT` 標頭；
  關閉時連預留空間都不輸出，開啟時預留高度，避免 CLS。
- 標籤文字放 `apps/web/messages/*/common.json` 的 `guides.*`（`tools/check-i18n.mjs` 會擋元件裡新加的中文）。

## 九、附錄：付費 Google Ads 導流

**結論：現在不划算，補齊量測前不建議投。**

- **單位經濟**：台灣搜尋廣告常見 CPC 約 NT$20–250（代理商公開行情，旅遊長尾詞可能較低）。
  付費訪客要讀文章、點分潤按鈕、再到夥伴站成交，才有分潤。
  例：分潤點擊率 5%、成交率 3%、每筆分潤 NT$150 → 每位訪客約 NT$0.23，遠低於一次點擊的成本。
- **夥伴條款**：
  - Klook：禁止競價 Klook 品牌字與其變體（例如 klook discount、klook japan），不能把付費廣告當轉址用，
    廣告裡也不能放 Klook 的網址或商標。
  - Travelpayouts：多數方案不允許付費搜尋；允許的也只能導到自己的網站（不能自動轉址），
    廣告文字不能出現品牌名，要加品牌否定關鍵字。各方案規則在該方案頁的「Allowed brand promotion methods and channels」。
  - Booking.com：禁止品牌字競價。Stay22 的合作條款沒有提到付費搜尋，但 Booking 本身的規則仍適用。
- **Google Ads 到達頁政策**：不能是「只為了把人送去別處」的頁面，也不能是「主要為了顯示廣告」的頁面。
  文章頁有原創內容所以可以；但如果同時上 AdSense 又買流量，要注意這條與無效流量風險。
- **量測缺口**：
  - web 只接受 `G-` 開頭的 GA4 ID（`analytics-provider.tsx:165`、`apps/api/app/admin/service.py:1264`），
    沒有 Google Ads 轉換標記。
  - GA4 的 `page_location` 只保留路徑（`analytics-provider.tsx:62`、`:117`），網址上的 `gclid` 會被丟掉，
    所以把 GA4 連到 Google Ads 也歸因不到廣告點擊。
  - Consent Mode 在所有地區都是 denied，Google 那邊只收得到 cookieless 訊號，轉換大多靠模型推估。
  - `affiliate_clicks`（`apps/api/app/models.py:282`）沒有 campaign 欄位，站內算不出某個廣告活動帶來多少分潤點擊。
    第一方分析有記 `utm_source`／`utm_medium`／`utm_campaign`，但沒有跟分潤點擊串起來。
- **市場**：韓國以 Naver 為主、中國大陸封鎖 Google，五個語系裡只有 zh-TW、ja、en 適合用 Google Ads。

## 十、來源

AdSense：

- [AdSense 資格條件](https://support.google.com/adsense/answer/9724)
- [AdSense 計畫政策](https://support.google.com/adsense/answer/48182)
- [無內容畫面上的 Google 廣告](https://support.google.com/publisherpolicies/answer/11112688?hl=en)
- [廣告放置政策](https://support.google.com/adsense/answer/1346295?hl=en)
- [隱私權政策必要內容](https://support.google.com/adsense/answer/1348695?hl=en)
- [EEA／英國／瑞士的同意管理要求](https://support.google.com/adsense/answer/13554116?hl=en)
- [個人化與非個人化廣告](https://support.google.com/adsense/answer/9007336?hl=en)
- [廣告程式碼搭配 CSP](https://support.google.com/adsense/answer/16283098?hl=en)
- [將網站連結到 AdSense（驗證方式）](https://support.google.com/adsense/answer/7584263?hl=en)
- [付款門檻](https://support.google.com/adsense/answer/1709871?hl=en)
- [美國稅務資料常見問題](https://support.google.com/adsense/answer/10735961?hl=en)
- [地址驗證（PIN）說明](https://support.google.com/adsense/answer/157667?hl=en)
- [Google 特殊用途檢索器（Mediapartners-Google）](https://developers.google.com/search/docs/crawling-indexing/google-special-case-crawlers)
- [台灣 AdSense 收入與 RPM 整理（非官方）](https://deanlife.blog/google-adsense-guide/)

付費 Google Ads：

- [Google Ads：濫用廣告聯播網／目的地要求](https://support.google.com/adspolicy/answer/6368661?hl=en)
- [Consent Mode 在 EEA 的更新](https://support.google.com/tagmanager/answer/13695607?hl=en)
- [Travelpayouts：用付費搜尋廣告推廣品牌](https://support.travelpayouts.com/hc/en-us/articles/115004350388-Promoting-brands-through-paid-search-ads)
- [Klook 聯盟計畫的 PPC 限制（第三方整理）](https://ecomobi.com/klook-affiliate-program-review/)
- [Stay22 合作夥伴條款](https://www.stay22.com/terms)
- [台灣關鍵字廣告 CPC 行情（代理商整理）](https://kaisheng.tw/ads/google-ads-keyword-cost/)
