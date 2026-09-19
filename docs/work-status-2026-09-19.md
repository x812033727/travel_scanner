# 工作狀態盤點（2026-09-19）

> claude-opus-5 應站主要求整理。依據：main `161687ad` 的 `tasks/`、GitHub 上的 PR 狀態、正式站。
> 這是當天的快照；最新清單以 `npm run tasks -- list` 為準。

## 一、現況

- **正式站**：`a69763b5`（#553，「多模型 AI 工作流」13 篇已發布）已部署。之後的 #554 只改文件。
- **開著的 PR**：只有這一支。
- **未完成的票**：整理前 109 張，這次結案 4 張後剩 105 張。沒有 P0；P1 22 張、P2 53 張、P3 30 張。
- **認領卡住範圍**：整理前有 13 張被認領，其中 10 張認領超過 24 小時，而且有 10 張的主要程式或內容早已隨 PR 合併。
  它們的 scope 鎖住另外 23 張票，其中 8 張是 P1。
  整理後只剩 2 張有人認領，都在等外部金鑰（NAVER、TourAPI），不鎖任何票。

## 二、建議優先順序

依「有沒有期限、讀者看不看得到、花多少工夫」排序。

| 順位 | 票 | 為什麼現在做 | 效益 | 誰要動手 |
|---|---|---|---|---|
| 1 | `2026-09-12-denylist-tombstones-real-attractions` | 封鎖類型會把 4 個真景點永久判退。9/15 那一輪探索已經跑過，下一輪約在 9/22 | 防止永久的資料流失；程式小改 | 可直接做；部署要站主核准 |
| 2 | `2026-09-13-reject-public-guides-about-another-country` | 52 篇公開的介紹寫的是別的國家，例如河內玉山祠底下掛的是台灣玉山。根因 9/16 已修好，已公開的還在 | 修掉讀者看得到的錯誤；一次後台退件加全量掃描 | 要站主同意改正式資料 |
| 3 | `2026-09-15-publish-held-ai-coding-content` | 111 篇已合併沒上線；9/15 統計有 25 個站內連結點進去是「這篇文章目前看不到」 | 上線內容量最大的一筆，同時修好死連結 | 要站主決定發布；#525 改過其中兩篇，要先重跑 dry-run |
| 4 | `2026-09-14-article-image-retry` | 圖片被限流後一直破圖。程式已上線，只差主機 nginx 設定啟用 | 用最少的工夫修好讀者看得到的問題 | 要站主同意改主機設定 |
| 5 | `2026-09-08-prevent-google-coordinates-being-labelled-durable` | 核准店家時把 Google 的座標當永久資料存（有條款風險），每核准一筆就多一筆 | 止血；已存的舊資料另外處理 | 可直接做 |
| 6 | `2026-09-12-hk-openrice-public`、`2026-09-12-non-japan-reservation-sweep` | 資料已合併，正式站有沒有套用沒有紀錄 | 香港有平台按鈕的店家預計從 2 間變 16 間 | 先查正式站；套用要站主同意 |
| 7 | `2026-09-14-release-drivers-own-deploy-hold` | 一般部署和 Codex 的分段發布可能互撞，目前靠部署前的人工檢查擋著 | 根治部署時互撞的風險 | 可直接做 |
| 8 | `2026-09-16-launch-articles-batch-7` | 20 篇已上線，還剩日期類的後續票、既有文章的反向連結與上線後檢查 | 反向連結把既有流量導進新文章 | 可直接做 |

### 小而快、效益高的 P2

| 票 | 為什麼 | 大小 |
|---|---|---|
| `2026-09-14-food-links-city-param-ignored` | 每篇旅遊文章結尾的「XX 美食目錄」連結用 `?city=`，目錄只認 `destination_id`，讀者點進去看到的是所有城市 | 前端小改 |
| `2026-09-14-refresh-kansai-lite-and-expressway-passes` | 三篇文章寫的票券版本 9/30 到期，十月起就成了過期資訊 | 文章小改；官網公布新版後回填，十月前至少要加註 |
| `2026-09-13-ci-duplicate-runs-amplify-flakes` | 每次推送 CI 都跑兩遍，舊的也不會取消，拖慢每一支 PR，也放大不穩定的測試 | 設定小改 |
| `2026-09-11-flight-status-checked-at-utc` | 航班動態的「查詢時間」把 UTC 當成當地時間顯示 | 前端小改 |
| `2026-09-12-tables-coffee-closed` | 已經停業的店還公開在大阪美食清單 | 一筆資料；改正式資料要站主同意 |
| `2026-09-12-re-add-the-seoul-national-folk` | 首爾的國立民俗博物館被誤判退件，成了墓碑 | 一筆資料；改正式資料要站主同意 |

其他大型功能（社群、情境旅遊服務、飯店平台、網美店家、Gemini／Codex 深入教學）多半在等下一節的人工條件，不建議先開工。

## 三、等站主決定或動手的事

- 發布那 111 篇（第 3 項）。
- 同意在正式站：退件 52 篇（第 2 項）、套用訂位資料（第 6 項）、改主機 nginx（第 4 項）。
- NAVER 金鑰：沒有它，韓國景點與店家不能發布（`2026-09-06-naver-maps-key`）。
- 網站體驗設定的人工驗收（`2026-09-09-site-experience-settings`）。
- 教學實測需要的帳號、裝置與費用上限：
  - Claude 教學：claude-lab 的 `ANTHROPIC_API_KEY`、測試用 MCP OAuth 服務、實體手機（`2026-09-14-claude-tutorial-ci-validation`、`2026-09-14-claude-advanced-live-validation`）。
  - Gemini 深入系列：Google 測試帳號與費用上限、Android／iPhone 實機（`2026-09-14-gemini-advanced-*`）。
- 上架門檻：
  - Travelpayouts：品牌與目的地的實際核對（`2026-09-08-travelpayouts-live-destination-activation`）。
  - 情境旅遊服務：六城市的真實庫存與追蹤驗證（`2026-09-07-contextual-travel-services`）。
  - 社群：公開政策與聯絡資訊（`2026-09-07-mokaair-community-foundation`）。

## 四、這次整理做了什麼

經站主在 2026-09-19 同意。每張票都補上依據與剩下的工作，標題是「標記完成（由站主授權，非原持有者）」或「釋出認領（由站主授權）」。

**結案 4 張**（以合併紀錄為證）

- `2026-09-12-shared-trip-partner-cta`、`2026-09-12-trip-partner-cta`、`2026-09-12-trip-partner-offer-availability`：清單全部打勾，PR #436 於 9/12 合併。
- `2026-09-14-new-trip-auth-draft-ci`：PR #468 於 9/14 合併，四項必要檢查全綠；兩個沒勾的 CI 項目由合併紀錄證明。

**釋出 7 張認領**（改回待認領，要做的人重新 claim）

| 票 | 原持有者 | 為什麼釋出 | 剩下什麼 |
|---|---|---|---|
| `2026-09-09-site-experience-settings` | codex-site-experience | #380 已合併；卡在受阻狀態 10 天，鎖住 17 張票 | 回歸測試，以及站主的人工驗收 |
| `2026-09-11-deny-school-hospital-tram-stop-ward` | claude-opus-5 | #403 已合併；和第 1 項同一個 scope | 9/15 那輪探索之後的查核 |
| `2026-09-12-food-merchant-enrichment` | claude-fable-5-1 | #432 已合併；鎖住 8 張票 | E：研究批次 30 家試點與報告 |
| `2026-09-12-hk-openrice-public` | claude-opus-5 | #414 已合併 | 正式站套用與數字核對 |
| `2026-09-12-non-japan-reservation-sweep` | claude-opus-5 | #440 已合併 | 正式站試跑、套用 |
| `2026-09-13-life-ai-batch-11` | claude-fable-5-1 | 認領後沒有進度，也沒有分支 | 整批 20 篇 |
| `2026-09-16-launch-articles-batch-7` | claude-opus-5 | #543 已合併，20 篇都在 sitemap | 後續票、反向連結、上線後檢查 |

**補註 3 張**：第 1、4、5 項各加一段 2026-09-19 的查證，分別是期限與下一輪探索的時間、nginx 還差哪一步、Google 座標的問題在 main 上仍然存在。

**沒動的**：四張 Codex／Gemini 的票清單已經全勾，但沒有結案：`2026-09-14-codex-depth-plan-alignment`、`2026-09-14-gemini-advanced-platform`、`2026-09-14-gemini-advanced-visible-projection`、`2026-09-14-gemini-advanced-visible-ui`。
它們沒有人認領，也不鎖任何票，收尾交給 Codex 的發布流程決定。

## 五、全部未完成的工作（本 PR 合併後，105 張）

「清單」是完成條件與步驟裡的打勾數。「已合併的 PR」是票上 `branch` 對應的 PR 已經合併，表示做了一部分，不表示完成。

### API 與資料（api）：33 張

| 優先 | 狀態 | 清單 | 已合併的 PR | 票 | 標題 |
|---|---|---|---|---|---|
| P1 | 待認領 | 7/8 | #336 | `2026-09-07-contextual-travel-services` | Contextual travel services and affiliate catalog |
| P1 | 待認領 | 8/11 | — | `2026-09-07-hotel-platform-options-and-quote-readiness` | Hotel platform options and quote readiness |
| P1 | 待認領 | 19/20 | #361 | `2026-09-07-merchant-style-discovery` | 網美與文青店家風格篩選、審核及首批來源資料 |
| P1 | 待認領 | 7/9 | #343 | `2026-09-07-mokaair-community-foundation` | Mokaair community foundation and account safety |
| P1 | 待認領 | 0/6 | — | `2026-09-08-prevent-google-coordinates-being-labelled-durable` | Prevent Google coordinates being labelled durable by merchant review |
| P1 | 待認領 | 8/10 | #403 | `2026-09-11-deny-school-hospital-tram-stop-ward` | Deny school, hospital, tram stop, ward and military base types in hotspot discovery |
| P1 | 待認領 | 0/4 | — | `2026-09-12-denylist-tombstones-real-attractions` | Military base, primary school and hospital deny types will tombstone real attractions on 2026-09-15 |
| P1 | 待認領 | 8/10 | #432 | `2026-09-12-food-merchant-enrichment` | 反向用美食定位平台補齊待審店家資料（Gemini 補齊模式與瀏覽器批次匯入） |
| P2 | 待認領 | 0/5 | — | `2026-09-07-enrich-new-shopping-place-ids` | 30 筆新購物店家還沒 place enrichment，所以加不進行程 |
| P2 | 待認領 | 0/6 | — | `2026-09-07-jsonb-3-42` | 防 jsonb 運算子的測試只守住 3 張表，實際有 42 張 |
| P2 | 待認領 | 0/4 | — | `2026-09-10-daily-route-force-refresh` | Preserve force refresh in daily route background jobs |
| P2 | 待認領 | 0/6 | — | `2026-09-12-attribute-affiliate-clicks-to-the-guide` | Attribute affiliate clicks to the guide article that placed them |
| P2 | 待認領 | 0/4 | — | `2026-09-12-discovery-only-sees-100-articles-per-centre` | Wikimedia discovery can only ever see the 100 nearest articles within 10 km of each city centre |
| P2 | 待認領 | 3/6 | #414 | `2026-09-12-hk-openrice-public` | 香港 OpenRice 店家頁改為公開（僅電話訂位也顯示） |
| P2 | 待認領 | 4/6 | #440 | `2026-09-12-non-japan-reservation-sweep` | 台灣、新加坡、泰國、越南的訂位連結再掃一輪 |
| P2 | 待認領 | 0/4 | — | `2026-09-12-test-warning-codes-allowlist-misses-its` | test_warning_codes allowlist misses its own files on Windows path separators |
| P2 | 待認領 | 0/7 | — | `2026-09-14-diagram-descriptions-are-unreadable` | 498 SVG diagrams hide their fares and times from every crawler |
| P2 | 待認領 | 0/7 | — | `2026-09-14-mypy-does-not-check-tests` | mypy does not check tests, so a signature change breaks integration tests silently |
| P2 | 待認領 | 0/5 | — | `2026-09-14-planner-budget-admin-card` | Planner budget cannot be lowered without a restart |
| P2 | 待認領 | 0/6 | — | `2026-09-14-preview-never-charged` | Itinerary preview is limited but never charged |
| P2 | 待認領 | 0/8 | — | `2026-09-14-redis-py-8-migration` | Migrate the API from redis-py 6 to redis-py 8 |
| P2 | 待認領 | 0/4 | — | `2026-09-16-guides-aliases-seed-crashes-in-the` | guides-aliases-seed crashes in the production image |
| P2 | 待認領 | 0/7 | — | `2026-09-16-pack-cli-ingest-805` | pack_cli ingest 不認子主題，805 篇已上線的內容包重跑會被擋 |
| P2 | 待認領 | 0/7 | — | `2026-09-17-commons-non-ascii-filename-ingest` | 非 ASCII 檔名的 Commons 圖片 ingest 不進來：UnicodeEncodeError |
| P3 | 待認領 | 0/5 | — | `2026-09-06-area-circles-electronics-districts` | 區域目錄缺龍山電子商街與光華商圈兩個圈 |
| P3 | 待認領 | 0/6 | — | `2026-09-06-oka-amerikamura-wrong-qid` | 沖繩美國村的 Wikidata QID 指到大阪，座標也是 |
| P3 | 待認領 | 0/5 | — | `2026-09-06-shopping-seeds-second-batch` | 第二批購物店家：十五個沒有公開座標來源的候選 |
| P3 | 待認領 | 0/7 | — | `2026-09-07-add-a-meal-to-a-day` | 行程裡新增一餐：四個 trip-selections 端點接受 mode: replace_meal\|append |
| P3 | 待認領 | 0/3 | — | `2026-09-07-fixed-email-in-integration-tests` | 整合測試用固定 email，同一個資料庫跑第二次就 UniqueViolation |
| P3 | 待認領 | 0/3 | — | `2026-09-09-backup-catalog-free-disk-fixture` | Isolate backup catalog test from host free disk capacity |
| P3 | 待認領 | 0/5 | — | `2026-09-12-api-windows-agents-md` | 三個 API 測試在 Windows 開發機上必紅，AGENTS.md 叫大家推送前跑的就是這套 |
| P3 | 待認領 | 0/5 | — | `2026-09-14-answer-first-howto-descriptions` | AIO: 68 how-to descriptions enumerate topics instead of answering |
| P3 | 待認領 | 0/10 | — | `2026-09-14-life-finance-series-hub` | 財經教學中心：系列目錄與 hub |

### 前端（web）：23 張

| 優先 | 狀態 | 清單 | 已合併的 PR | 票 | 標題 |
|---|---|---|---|---|---|
| P1 | 待認領 | 1/7 | #340 | `2026-09-07-mokaair-community-web` | Mokaair community responsive web and five-language experience |
| P1 | 待認領 | 8/10 | #380 | `2026-09-09-site-experience-settings` | Mokaair site experience palettes and managed information pages |
| P1 | 待認領 | 5/6 | #470 | `2026-09-14-article-image-retry` | Article images recover from rate limits |
| P1 | 待認領 | 11/11 | #520 | `2026-09-14-gemini-advanced-platform` | Gemini 深入系列：可見篇章與發布批次支援 |
| P1 | 待認領 | 6/6 | #520 | `2026-09-14-gemini-advanced-visible-projection` | Gemini 深入系列：伺服器可見清單與投影驗證 |
| P1 | 待認領 | 8/8 | #520 | `2026-09-14-gemini-advanced-visible-ui` | Gemini 深入目錄：接收可見清單的介面與瀏覽器驗證 |
| P2 | 待認領 | 0/4 | — | `2026-09-10-locale-login-return-path` | Normalize locale-prefixed login return paths |
| P2 | 待認領 | 0/5 | — | `2026-09-11-flight-status-checked-at-utc` | 航班動態的查詢時間把 UTC 當成地方時顯示 |
| P2 | 待認領 | 0/3 | — | `2026-09-11-offline-day-view-needs-an-app` | 當日檢視要真的離線可用，需要預先快取 app shell |
| P2 | 待認領 | 0/5 | — | `2026-09-14-food-links-city-param-ignored` | Food directory links use ?city= but the directory only reads destination_id |
| P2 | 待認領 | 0/7 | — | `2026-09-14-foods-establishment-graph` | AIO: /foods states its merchants and their verification as FoodEstablishment |
| P3 | 受阻 | 0/7 | — | `2026-09-13-google-ads-conversion-measurement` | 付費 Google Ads 導流的轉換量測 |
| P3 | 受阻 | 0/5 | — | `2026-09-14-eslint-10-upgrade` | Upgrade ESLint to 10 once eslint-config-next supports it |
| P3 | 受阻 | 0/6 | — | `2026-09-14-typescript-7-upgrade` | Upgrade TypeScript to 7 once typescript-eslint supports it |
| P3 | 待認領 | 0/6 | — | `2026-09-06-ask-origin-airport-at-trip-creation` | 建立旅程時就問出發機場，不要等到查機票才問 |
| P3 | 待認領 | 0/5 | — | `2026-09-06-full-trip-search` | 彈性日期區塊的價格標籤寫死 full_trip_search |
| P3 | 待認領 | 0/2 | — | `2026-09-11-admin-shell-modal-layer` | admin-shell 命令面板改用 modal-sheet 的分層堆疊 |
| P3 | 待認領 | 0/6 | — | `2026-09-11-discovery-card-language-badge` | 推薦流卡片標示內容語言（語言方向 1） |
| P3 | 待認領 | 0/4 | — | `2026-09-11-fare-lab-warnings-and-copy` | 航班票價實驗室三個畫面的多語系與警告代碼 |
| P3 | 待認領 | 0/8 | — | `2026-09-13-adsense-ads-txt-drift` | Serve ads.txt from the configured publisher id instead of a build-time file |
| P3 | 待認領 | 0/3 | — | `2026-09-13-display-card-promises-language` | 外觀與語言卡片其實沒有語言選項 |
| P3 | 待認領 | 0/6 | — | `2026-09-14-airline-comparison-browser-timeout` | Investigate intermittent airline comparison browser timeout |
| P3 | 待認領 | 0/7 | — | `2026-09-14-sitemap-lists-pet-friendly-places` | Sitemap lists the pet-friendly place pages, not just the directory |

### 維運與正式站資料（ops）：16 張

| 優先 | 狀態 | 清單 | 已合併的 PR | 票 | 標題 |
|---|---|---|---|---|---|
| P1 | 待認領 | 7/7 | — | `2026-09-08-continue-evidence-backed-remaining-hotspot-candidate` | Continue evidence-backed remaining hotspot candidate review |
| P1 | 待認領 | 0/8 | — | `2026-09-08-travelpayouts-live-destination-activation` | Complete live Travelpayouts brand and destination offer verification |
| P1 | 待認領 | 0/8 | — | `2026-09-12-nginx-deploy-checks-false-pass` | ops/nginx 的上機指引有三處會假通過 |
| P1 | 待認領 | 0/6 | — | `2026-09-13-reject-public-guides-about-another-country` | 五十二篇已公開的景點介紹講的是別的國家，逐筆退掉 |
| P1 | 待認領 | 0/9 | — | `2026-09-14-release-drivers-own-deploy-hold` | Codex 發布工具自己建立與移除部署暫停檔 |
| P2 | 受阻（claude-fable-5-1） | 0/7 | #201 | `2026-09-06-naver-maps-key` | 沒有 NAVER 金鑰，韓國景點與店家無法發布 |
| P2 | 受阻 | 0/8 | — | `2026-09-13-prod-compose-network-segmentation` | Production compose has no network segmentation or read-only root |
| P2 | 待認領 | 1/5 | — | `2026-09-09-verify-reported-hotels-booking-links` | Verify the two reported hotels exact Booking links |
| P2 | 待認領 | 0/6 | — | `2026-09-11-seoul-day2-live-requery` | Re-query the live Seoul Day 2 route after the #387 release |
| P2 | 待認領 | 0/5 | — | `2026-09-12-naver-booking-ids` | 找出韓國店家的 Naver 예약 商家編號 |
| P2 | 待認領 | 0/6 | — | `2026-09-12-re-add-the-seoul-national-folk` | Re-add the Seoul National Folk Museum after its Wikidata QID was tombstoned |
| P2 | 待認領 | 0/5 | — | `2026-09-12-tables-coffee-closed` | TABLES Coffee Bakery & Diner 已停業，仍公開在大阪美食清單 |
| P2 | 待認領 | 0/10 | — | `2026-09-13-adsense-auto-ads-overlay-setup` | AdSense 後台開啟錨定／插頁／Multiplex，修正封鎖清單，兩週後比較收益 |
| P2 | 待認領 | 0/6 | — | `2026-09-13-ci-duplicate-runs-amplify-flakes` | CI runs every branch push twice and never cancels superseded runs |
| P3 | 受阻（claude-opus-5） | 8/16 | #243 | `2026-09-06-korea-tourism-tourapi-spike` | TourAPI（韓國觀光公社）可行性驗證：先確認拿得到金鑰、連得上、資料量夠不夠 |
| P3 | 待認領 | 0/4 | — | `2026-09-13-search-text` | 部署後清掉三筆搬過家的景點殘留的舊城市 search_text |

### 內容與文件（docs）：30 張

| 優先 | 狀態 | 清單 | 已合併的 PR | 票 | 標題 |
|---|---|---|---|---|---|
| P1 | 待認領 | 12/23 | #520 | `2026-09-14-gemini-advanced-md` | Gemini 深入教學 69–74：MD 與 CLI 設定實驗 |
| P1 | 待認領 | 47/73 | #520 | `2026-09-14-gemini-advanced-work` | Gemini 深入教學 51–56：日常與工作流程 |
| P1 | 待認領 | 0/10 | — | `2026-09-15-publish-held-ai-coding-content` | 批次 04 與 Claude Code 兩系列要一起發：線上 25 個連結指向它們 |
| P2 | 受阻 | 18/21 | #525 | `2026-09-14-codex-depth-content` | Codex deep content and isolated learning components |
| P2 | 受阻 | 10/14 | #525 | `2026-09-14-codex-learning-series` | Codex learning hub - 60 in-depth multilingual tutorials |
| P2 | 受阻 | 0/6 | — | `2026-09-16-unpublished-content-packs-hub-descriptions-and` | "Unpublished content packs: hub descriptions and lesson ordinals in body text" |
| P2 | 待認領 | 0/7 | — | `2026-09-13-life-ai-batch-11` | 生活分享 AI 系列批次 11：生活應用、3C 與旅途中的 AI（20 篇） |
| P2 | 待認領 | 16/20 | #501 | `2026-09-14-claude-advanced-live-validation` | Claude Code 進階：補齊真實環境驗證 |
| P2 | 待認領 | 10/10 | #525 | `2026-09-14-codex-depth-plan-alignment` | Align Codex deep tutorials with Claude Code plan |
| P2 | 待認領 | 8/16 | #520 | `2026-09-14-gemini-advanced-api` | Gemini 深入教學 81–86：API 工程與完整專案 |
| P2 | 待認領 | 13/30 | #520 | `2026-09-14-gemini-advanced-automation` | Gemini 深入教學 75–80：CLI 擴充與自動化專案 |
| P2 | 待認領 | 9/16 | — | `2026-09-14-gemini-advanced-creative` | Gemini 深入教學 63–68：圖片、影片與資料作品 |
| P2 | 待認領 | 11/30 | #520 | `2026-09-14-gemini-advanced-release` | Gemini 深入系列：36 篇整套驗收與目錄開放 |
| P2 | 待認領 | 35/47 | #520 | `2026-09-14-gemini-advanced-research` | Gemini 深入教學 57–62：NotebookLM 與研究方法 |
| P2 | 待認領 | 0/9 | — | `2026-09-14-life-ai-batch-12-suffix-keywords` | 生活分享 AI 系列批次 12：字尾關鍵字補位（11 篇） |
| P2 | 待認領 | 0/11 | — | `2026-09-14-life-finance-batch-04` | 生活分享財經系列批次 04：稅務與政府制度（20 篇） |
| P2 | 待認領 | 0/11 | — | `2026-09-14-life-finance-batch-05` | 生活分享財經系列批次 05：投資入門：觀念與台股（20 篇） |
| P2 | 待認領 | 0/11 | — | `2026-09-14-life-finance-batch-06` | 生活分享財經系列批次 06：海外投資、數位資產與退休（20 篇） |
| P2 | 待認領 | 0/6 | — | `2026-09-14-refresh-kansai-lite-and-expressway-passes` | 十月起 KANSAI RAILWAY PASS LITE 與 TEP、KEP 高速周遊券的新版本要回填三篇文章 |
| P2 | 待認領 | 0/5 | — | `2026-09-15-ai-suffix-keywords-batch-08-backfill` | 批次 08 落地後補 14 篇字尾關鍵字（生圖、去背、簡報、影片、配音、作曲、3D、Canva、字幕、版權） |
| P2 | 待認領 | 7/12 | #543 | `2026-09-16-launch-articles-batch-7` | 撰寫並上線第七批旅遊文章：二十篇 zh-TW 攻略與情報 |
| P2 | 待認領 | 0/7 | — | `2026-09-16-model-table-quarterly-recheck` | 模型總表定期重查：價格與上下文每季對一次官網 |
| P2 | 待認領 | 0/3 | — | `2026-09-16-news-batch-4-4-the-8` | News batch 4.4: the 8/1 onward secondary news for the three verticals |
| P3 | 待認領 | 0/43 | — | `2026-09-14-batch-6-guides-dated-maintenance` | "Batch 6 guides: dated edits after launch (removals, re-checks, expiring notices)" |
| P3 | 待認領 | 0/5 | — | `2026-09-14-kanazawa-21-museum-closure-2027-05` | 2027-05-06 起金澤篇的 21 世紀美術館改寫成休館中，2028 年 3 月重開後改回 |
| P3 | 待認領 | 0/5 | #531 | `2026-09-15-content-summary-howto-and-life` | 編輯為攻略與生活文章加入重點摘要（summary）與真實 FAQ |
| P3 | 待認領 | 0/4 | — | `2026-09-16-existing-guides-season-sources` | 既有文章依第七批規劃修正：沒有出處的季節月份與霧霾說法 |
| P3 | 待認領 | 0/5 | — | `2026-09-16-retitled-guides-stale-link-text` | 17 篇文章仍以四篇改過的舊標題當連結文字 |
| P3 | 待認領 | 0/3 | — | `2026-09-16-travel-guides-doc-article-ending` | Article anatomy in docs/travel-guides.md still ends with the other-language list |
| P3 | 待認領 | 0/5 | — | `2026-09-19-ollama-getting-started-tool-choice-recheck` | ollama-getting-started says tool_choice is unsupported but the Ollama OpenAI-compatibility page now lists it |

### 工具（tools）：3 張

| 優先 | 狀態 | 清單 | 已合併的 PR | 票 | 標題 |
|---|---|---|---|---|---|
| P2 | 待認領 | 7/8 | #501 | `2026-09-14-claude-tutorial-ci-validation` | Claude tutorial GitHub Actions validation workflow |
| P2 | 待認領 | 0/4 | — | `2026-09-14-investigate-windows-task-archive-leftover-open` | Investigate Windows task archive leftover open file |
| P2 | 待認領 | 0/7 | — | `2026-09-14-tasks-done-retains-open-copy` | tasks done 後仍保留 open 副本：調查 Windows 封存行為 |
