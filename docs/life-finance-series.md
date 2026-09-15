# 生活分享：財經文章與教學系列（120 篇總表）

這份文件是「生活分享」（`kind: "life"`，`/{locale}/life/{slug}`）財經系列的**編輯總表**：每一篇的
slug、標題、主題、配圖方式與易變性在這裡定死，批次任務票的 `scope` 才能精確到檔案。
內容包格式、圖片與文字規則在 [`docs/travel-guides.md`](travel-guides.md)（「Editorial rules」一節）；
撰稿代理拿到的指令在 [`docs/life-finance-series-brief.md`](life-finance-series-brief.md)。

這是生活分享專區的第二個垂直領域，第一個是 [`docs/life-ai-series.md`](life-ai-series.md) 的 AI 工具系列。
產製流程、批次票的形狀與踩過的坑照抄那一份，**但財經多了一層法遵限制**（第「不能寫的東西」節），
AI 系列沒有這個問題，不要把兩邊的規則混著用。

## 目的與讀者

站主要用一批與旅遊無關、可索引的自有文章換曝光，文末再把讀者導向旅遊情報攻略與目的地頁
（`docs/travel-guides.md`「What this is」）。讀者是台灣的一般上班族與小家庭：有薪水、有勞健保、
會報稅、有幾張信用卡，想知道錢該怎麼分配、制度怎麼運作、工具怎麼選；**不是**想被告知該買什麼。

這個系列對本站的額外價值在於銜接：換匯、海外刷卡手續費、旅平險、班機延誤不便險、海外購物關稅、
入境免稅額度這些題目，讀者本來就是在規劃出國時搜尋的。這些篇散在批次 02／03／04，
每一篇都要連回站內既有的旅遊攻略——**只能連下面「可連的旅遊攻略」那張表列出的網址**。

## 政策

- **語系：只寫 zh-TW。** 五語系共用一份 1,000 列的 sitemap（`SITEMAP_LIMIT`／`SITEMAP_GUIDE_ENTRY_LIMIT`），
  一個已發布的翻譯佔一列。今天文章約佔 478 列，靜態頁另有 ≤385 個 URL，
  `pack_ingest.SITEMAP_WARN_ROWS` 是 800。120 篇單語系加進去約 598 列，仍在警戒線內；
  要翻其他語系得等 sitemap 拆分（`docs/travel-guides.md`「Still open」）。
- **主題：** 用 `finance` 加上 life 既有詞彙（`ai`、`tutorial`、`software`、`gadgets`、`productivity`、
  `daily`、`misc`）。實務上是 `finance` 再加一個：操作教學型加 `tutorial`，工具比較型加 `software`，
  生活情境型加 `daily`。`destination_id` 一律 `null`。
- **合作連結：一律不放，總表的「合作」欄全部留空。** `app/affiliates/content_links.py` 的
  `ContentCategory` 只有 `hosting`／`books`／`courses`／`software`，`CONTENT_PARTNERS` 今天只有
  Hostinger 與博客來，**沒有任何金融類夥伴**。要放金融聯盟連結必須先登記夥伴與類別，
  那是另一張票；在那之前，任何帶追蹤參數的網址放進 `link` 區塊、`sources` 或圖片 credit
  都會被 `422 content_link_affiliate` 擋下來，這是對的，不要繞過。
- **配圖：以自繪插圖為主。** hero 必須是點陣圖（`HERO_SRC_PATTERN`），所以自繪 hero 由
  `pack_cli ingest` 把 `hero.svg` 渲染成 1600×900 的 `hero.jpg`；有實物可拍（錢包、提款機、
  報稅用的紙本、保單文件夾）時才用 Wikimedia Commons 的 CC0／PD／CC BY／CC BY-SA 照片。
  **銀行、券商、保險公司、交易所、支付 App 的 logo、字標、圖示與介面截圖一律不用**——
  商標不是我們的，而且畫面一改就過時。總表「圖」欄：插＝自繪 hero 插圖，照＝Commons 照片；
  每篇另有至少一張自繪 SVG 圖解。
- **事實：** 費率、級距、額度、手續費、稅率、申報時程都在撰稿當天查主管機關或業者官網
  （財政部稅務入口網、各地區國稅局、勞動部勞保局、衛福部健保署、金管會、中央銀行、
  臺灣證券交易所、證券櫃檯買賣中心、聯徵中心、各銀行與保險公司官網），`sources` 每筆記
  `checked_on`，查不到的寫「以主管機關公告為準」。稅率與級距逐年公告，所以「易變」欄打勾的
  篇數比 AI 系列多很多——那一欄打勾的，每年報稅季前要回查一次。

## 不能寫的東西（這個系列獨有）

財經是 Google 的 YMYL 類別，`docs/adsense-feasibility.md` 已經指出代理撰寫的內容本身就有
AdSense「自動產生內容」的政策風險。這個系列又包含投資入門：台灣《證券投資信託及顧問法》
限制未取得許可者為報酬提供證券投資分析與建議。**整個系列是教育性的，不是投顧。**

逐字照抄到 [`docs/life-finance-series-brief.md`](life-finance-series-brief.md)，撰稿代理動筆前會先讀到：

1. **不推薦個別商品。** 不推個股、個別基金、個別 ETF、個別保單、個別交易所、個別銀行方案。
   要舉例就講**類型與成本結構**（「市值型 ETF 的選股邏輯」可以，「某某 ETF 值得買」不行；
   「數位帳戶的優利活存通常有額度上限」可以，「某某銀行最划算」不行）。
2. **不給買賣建議。** 不寫進場時機、目標價、預期報酬率、績效預測、回測結果、「現在適合買」。
3. **不用絕對化措辭。** 沒有「保證」「穩賺」「零風險」「必賺」「無腦存」「躺著賺」。
   報酬與風險同時出現，成本與限制寫在好處旁邊，不要分段藏。
4. **每篇最後固定一個免責 `callout`。** 措辭模板在 brief 裡，不要自己重寫。
   這是額外的，不取代原本那個「最有價值的提醒」callout——所以財經文章會有兩個 callout。
5. **行情數字不寫進正文。** 股價、匯率、幣價、殖利率、基金淨值查證日一過就是錯的。
   制度、費率結構、計算方式、申請流程可以寫，並註明查證日。

**機器只擋得住一半。** `pack_cli lint` 會檢查「有沒有免責 callout」（error）與「正文有沒有出現
絕對化措辭」（warning，因為 `investment-scam-red-flags` 這種講詐騙話術的篇本來就要引用那些詞）。
「有沒有變相推薦個股」「風險講得夠不夠」機器讀不出來，留在批次票的 Definition of done，
由認領批次的人逐篇看。**lint 綠不等於法遵過了。**

## 可連的旅遊攻略（銜接篇只能連這張表）

**站上有 91 篇旅遊攻略，但只有 85 篇有 zh-TW。** 針對境外旅客寫的 `taiwan-*` 那幾篇
（`taiwan-payment-easycard-cash-cards`、`taiwan-tax-refund-shopping-2026`、`taiwan-esim-sim-wifi` …）
只有 `en`／`ja`／`ko`／`zh-CN`，**從 zh-TW 的財經文連過去會把讀者送到一個沒有他語言版本的網址**。
AI 系列的經驗記錄裡記過同一種錯（批次 03 連了 13 篇不存在的文章）。

網址形狀是 `https://mokaair.com/zh-TW/guides/<kind>/<slug>`，**`kind` 是網址的一部分**
（`howto` 或 `intel`，弄錯就是 404），所以下表直接給完整網址，指派照抄，不要自己組。

| 用在哪 | 網址 |
| --- | --- |
| 換匯、海外提款 | `https://mokaair.com/zh-TW/guides/howto/korea-money-exchange-wowpass-guide` |
| 退稅、免稅新制 | `https://mokaair.com/zh-TW/guides/intel/japan-tax-free-refund-2026` |
| 退稅實務、購物 | `https://mokaair.com/zh-TW/guides/howto/korea-olive-young-tax-refund-shopping` |
| 購物省錢 | `https://mokaair.com/zh-TW/guides/howto/japan-drugstore-shopping-list` |
| 交通 IC 卡、儲值 | `https://mokaair.com/zh-TW/guides/howto/japan-ic-card-suica-icoca-guide` |
| 交通卡、電子票證 | `https://mokaair.com/zh-TW/guides/howto/seoul-subway-t-money-guide` |
| 交通票券比價 | `https://mokaair.com/zh-TW/guides/howto/tokyo-transit-passes` |
| 交通票券比價 | `https://mokaair.com/zh-TW/guides/howto/kansai-rail-passes-guide` |
| 車票預訂、早鳥 | `https://mokaair.com/zh-TW/guides/howto/japan-shinkansen-ticket-guide` |
| 租車保險、押金 | `https://mokaair.com/zh-TW/guides/howto/japan-car-rental-expressway-guide` |
| 租車保險、押金 | `https://mokaair.com/zh-TW/guides/howto/jeju-car-rental-guide` |
| 入境規定、海關申報 | `https://mokaair.com/zh-TW/guides/intel/japan-entry-2026-visit-japan-web` |
| 入境規定 | `https://mokaair.com/zh-TW/guides/intel/thailand-entry-2026-tdac` |
| 訂房方案、取消條件 | `https://mokaair.com/zh-TW/guides/howto/japan-hotel-room-plan-guide` |
| 住宿預算、宿泊稅 | `https://mokaair.com/zh-TW/guides/howto/tokyo-where-to-stay` |
| 住宿預算 | `https://mokaair.com/zh-TW/guides/howto/seoul-where-to-stay` |
| 住宿預算 | `https://mokaair.com/zh-TW/guides/howto/osaka-kyoto-where-to-stay` |

批次票的指派只從這張表挑，挑幾個就寫幾個進指派；撰稿代理不准連指派沒給的網址。
站內連到其他財經文用 `https://mokaair.com/zh-TW/life/<slug>`，那些都是 zh-TW，沒有這個問題。

## 狀態怎麼看

總表不記錄「寫了沒」。`apps/api/app/guides/content/<slug>.json` 存在就是寫了；

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life \
  --catalogue ../../docs/life-finance-series.md
```

會列出總表有、內容包沒有的 slug（還沒寫）與內容包有、總表沒有的 slug（該補進總表）。
注意這個指令會把 AI 系列的內容包一起列成「總表沒有」——兩個系列共用 `--kind life`，
看的時候只認財經那些 slug。批次完成後不必回頭改這份檔案。

## 批次與任務票

每批 20 篇一張任務票，scope 是該批 20 個內容包檔案加 20 個圖片目錄（`tools/tasks.mjs` 的 scope
比對是「相同或前綴」，兄弟檔案不互卡，所以六批可以同時進行）。**scope 絕對不要寫成
`apps/api/app/guides/content`**，那會鎖死整個專區，連 AI 系列的批次都動不了。

批次 01 是試點，02 起依賴 01：試點學到的先寫回 brief 的「經驗記錄」。批次 06 另外依賴 05，
因為海外投資要連回台股那批建立的基礎觀念。

| 票 | 做什麼 | 依賴 |
| --- | --- | --- |
| `2026-09-14-life-finance-series-catalogue` | 這份總表與撰稿指令 | — |
| `2026-09-14-life-finance-topic` | `taxonomy.py` 加 `finance` ＋ migration 0075 | — |
| `2026-09-14-life-finance-lint-rules` | 免責與措辭的 lint 規則 | — |
| `2026-09-14-life-finance-batch-01` | 理財基礎與記帳（試點） | 上面三張 |
| `2026-09-14-life-finance-batch-02` | 銀行、支付與信用 | 上面三張 ＋ 批次 01 |
| `2026-09-14-life-finance-batch-03` | 保險與風險 | 上面三張 ＋ 批次 01 |
| `2026-09-14-life-finance-batch-04` | 稅務與政府制度 | 上面三張 ＋ 批次 01 |
| `2026-09-14-life-finance-batch-05` | 投資入門：觀念與台股 | 上面三張 ＋ 批次 01 |
| `2026-09-14-life-finance-batch-06` | 海外投資、數位資產與退休 | 上面三張 ＋ 批次 01、05 |
| `2026-09-14-life-finance-series-hub` | 教學中心（延後，見最後一節） | 六個批次 |

前三張票的 scope 互不重疊，**可以同時進行**。批次 02–06 之間也不互相依賴，五批可以同時開工。

**`life-finance-topic` 沒完成，一篇都寫不進來**：`pack_ingest._known_topics` 讀的是
`LIFE_SEED_TOPICS`，在 `finance` 進到那個常數之前，每一篇都會被 `topic_unknown` 擋下。

**`life-finance-lint-rules` 現在還不能認領**：`apps/api/app/guides/pack_ingest.py` 在
`2026-09-14-claude-code-tutorial-center`（`status: review`）的 scope 裡，`review` 會佔住 scope。
等它合併或認領過期。這不擋批次票——lint 規則是多一層保險，不是 ingest 的前提。

## 產製流程（每批）

1. 認領任務票（`npm run tasks -- claim <id> --owner <你的名字>`）。
2. 從總表抄出該批的指派，一篇一個撰稿代理、每波最多七個（AI 系列的經驗：兩篇一個代理
   會在半小時左右撞到額度）。代理照 `docs/life-finance-series-brief.md` 產出工作區。
3. 每篇落地就 `cd apps/api && uv run python -m app.guides.pack_cli ingest --from <workdir> --slug <slug>`；
   被拒的退回修。
4. `pack_cli lint --kind life --render-dir /tmp/renders` 之後**逐張看圖**——代理看不到自己畫的版面，
   標籤壓線、文字溢出、標籤互相疊在一起都能通過機械檢查。
5. **逐篇讀一次，確認沒有變相推薦個別商品、風險寫得夠。** 這一步沒有工具可代勞。
6. 跑測試、更新任務票、commit。

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## 總表

欄位：`圖` 插＝自繪 hero 插圖、照＝Commons 照片；`易變` 打勾的篇每年報稅季前回查一次。
「合作」欄整個系列都是空的（見「政策」）。

### 批次 01｜理財基礎與記帳（地基，之後每批都連回這 20 篇）

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 1 | `personal-finance-first-steps` | 個人理財第一步：先看懂收支，再談存錢與投資 | finance, tutorial | 插 |  |  |
| 2 | `finance-glossary-50-terms` | 財經名詞速查：50 個理財與投資常見詞彙一次搞懂 | finance, misc | 插 |  |  |
| 3 | `expense-tracking-getting-started` | 記帳新手入門：記什麼、記多久、怎麼不半途而廢 | finance, tutorial | 插 |  |  |
| 4 | `expense-tracking-app-choose` | 記帳 App 怎麼選：自動同步、手動輸入與隱私的取捨 | finance, software | 插 |  | ✓ |
| 5 | `household-budget-methods` | 預算怎麼抓：50/30/20、信封法與零基預算的差別 | finance, tutorial | 插 |  |  |
| 6 | `bank-account-separation-system` | 帳戶分離法：用三到四個帳戶把錢分開管 | finance, tutorial | 插 |  |  |
| 7 | `emergency-fund-how-much` | 緊急預備金要存多少：怎麼算、放哪裡、什麼時候可以動 | finance, tutorial | 插 |  |  |
| 8 | `fixed-cost-subscription-audit` | 固定支出健檢：訂閱、電信與保費一年能省下多少 | finance, daily | 插 |  |  |
| 9 | `payslip-explained-taiwan` | 看懂薪資單：勞保、健保、勞退提繳與實領差在哪 | finance, tutorial | 插 |  | ✓ |
| 10 | `labor-pension-self-contribution` | 勞退自提 6%：怎麼提、省多少稅、什麼時候不適合 | finance, tutorial | 插 |  | ✓ |
| 11 | `labor-insurance-vs-pension` | 勞保與勞退不是同一件事：老年給付各自怎麼領 | finance | 插 |  | ✓ |
| 12 | `einvoice-carrier-taiwan` | 電子發票載具設定教學：手機條碼、歸戶與自動對獎 | finance, tutorial | 插 |  | ✓ |
| 13 | `personal-balance-sheet` | 寫一張個人資產負債表：把自己的淨值算出來 | finance, tutorial | 插 |  |  |
| 14 | `monthly-money-review` | 每月收支回顧：30 分鐘看完一個月的錢去哪了 | finance, productivity | 插 |  |  |
| 15 | `savings-goal-planning` | 存錢目標怎麼設：把「想買」換算成每月要存的金額 | finance, tutorial | 插 |  |  |
| 16 | `spending-triggers-and-habits` | 錢為什麼會不見：找出自己的消費觸發點 | finance, daily | 插 |  |  |
| 17 | `couple-money-management` | 兩個人的錢怎麼管：共同帳戶、分攤比例與定期對帳 | finance, daily | 插 |  |  |
| 18 | `kids-allowance-money-education` | 零用錢怎麼給：把金錢觀教給孩子的實際做法 | finance, daily | 插 |  |  |
| 19 | `bank-fee-audit` | 銀行手續費健檢：跨行、匯款與帳管費怎麼省 | finance | 插 |  | ✓ |
| 20 | `financial-document-organization` | 財務文件整理：保單、對帳單與稅單放哪裡才找得到 | finance, productivity | 插 |  |  |

`finance-glossary-50-terms` 是總索引篇，`display_order: 10`，其他篇 `100`。
**批次 01 全部用自繪插圖**：試點確認財經沒有安全的攝影主體（卡片、提款機、招牌都帶商標），
自繪也省掉 Commons 的授權與網路風險。原本標「照」的第 16、17、18 篇已改為「插」。
第 20 篇連回既有的 `digital-receipt-archive`（收據與保固資料夾）。

### 批次 02｜銀行、支付與信用

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 1 | `digital-bank-account-taiwan` | 數位帳戶是什麼：開戶流程、優利活存與使用限制 | finance, software | 插 |  | ✓ |
| 2 | `high-interest-savings-taiwan` | 高利活存怎麼看：利率級距、額度上限與實際拿到的利息 | finance | 插 |  | ✓ |
| 3 | `mobile-payment-taiwan-guide` | 台灣行動支付總整理：綁定方式、回饋與適用場景 | finance, software | 插 |  | ✓ |
| 4 | `credit-card-cashback-basics` | 信用卡回饋入門：現金回饋、紅利與哩程的差別 | finance, tutorial | 插 |  | ✓ |
| 5 | `credit-card-choose-by-spending` | 依消費習慣選信用卡：先算出自己的支出結構 | finance, tutorial | 插 |  |  |
| 6 | `credit-card-revolving-interest` | 循環利息與最低應繳：只繳最低到底會付多少 | finance | 插 |  | ✓ |
| 7 | `installment-zero-interest-cost` | 分期零利率的真實成本：手續費、定價與現金折扣 | finance | 插 |  |  |
| 8 | `credit-score-jcic-taiwan` | 聯徵信用報告怎麼查：信用評分是怎麼算出來的 | finance, tutorial | 插 |  | ✓ |
| 9 | `build-credit-from-zero` | 信用小白怎麼建立信用：第一張卡與往來紀錄 | finance, tutorial | 插 |  |  |
| 10 | `bank-transfer-fees-taiwan` | 轉帳與跨行手續費：什麼情況免費、什麼情況要錢 | finance | 插 |  | ✓ |
| 11 | `foreign-currency-account-taiwan` | 外幣帳戶開戶與用途：換匯、存款與領現金 | finance, tutorial | 插 |  | ✓ |
| 12 | `online-forex-exchange-taiwan` | 線上結匯教學：銀行 App 換匯、匯率價差與機場提領 | finance, tutorial | 插 |  | ✓ |
| 13 | `overseas-card-fees-dcc` | 海外刷卡手續費與 DCC：選當地幣別還是台幣 | finance, tutorial | 插 |  | ✓ |
| 14 | `overseas-atm-withdrawal` | 海外 ATM 提款：跨國提款卡、手續費與安全 | finance, tutorial | 插 |  | ✓ |
| 15 | `online-banking-security` | 網銀與帳戶安全：裝置綁定、OTP 與常見詐騙手法 | finance, tutorial | 插 |  |  |
| 16 | `warning-account-prevention` | 警示帳戶是怎麼來的：避免帳戶被凍結的實際做法 | finance | 插 |  |  |
| 17 | `debit-vs-credit-card` | 金融卡與信用卡差在哪：扣款時點、爭議款與額度 | finance, tutorial | 插 |  |  |
| 18 | `credit-card-dispute-chargeback` | 刷卡爭議款怎麼申請：時限、證明文件與流程 | finance, tutorial | 插 |  |  |
| 19 | `epayment-vs-ewallet-taiwan` | 電子支付與電子票證：法規分類與實際差別 | finance | 插 |  | ✓ |
| 20 | `bank-account-opening-guide` | 第一次開戶要帶什麼：臨櫃、線上與未成年開戶 | finance, tutorial | 插 |  | ✓ |

第 11–14 篇是旅遊銜接篇，連回「可連的旅遊攻略」表裡的換錢與 IC 卡那幾篇。

### 批次 03｜保險與風險

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 1 | `insurance-basics-taiwan` | 保險基本觀念：保險買的是什麼、應該先保什麼 | finance, tutorial | 插 |  |  |
| 2 | `insurance-policy-checkup` | 保單健檢怎麼做：把手上的保單列成一張表 | finance, tutorial | 插 |  |  |
| 3 | `term-vs-whole-life-insurance` | 定期險與終身險：保費結構與各自的適用情境 | finance | 插 |  |  |
| 4 | `medical-insurance-reimbursement` | 實支實付醫療險：收據正副本、限額與常見誤解 | finance, tutorial | 插 |  |  |
| 5 | `hospital-daily-benefit` | 住院日額怎麼看：給付條件與健保病房差額 | finance | 插 |  |  |
| 6 | `accident-insurance-basics` | 意外險：「意外」的定義比你想的窄 | finance | 插 |  |  |
| 7 | `cancer-insurance-basics` | 癌症險與重大傷病：一次金與療程給付的差別 | finance | 插 |  |  |
| 8 | `disability-income-insurance` | 失能扶助險：收入中斷時的保障怎麼看 | finance | 插 |  |  |
| 9 | `long-term-care-insurance` | 長照險怎麼理解：給付門檻與其他替代方案 | finance | 插 |  |  |
| 10 | `travel-insurance-basics` | 旅平險要保什麼：醫療、意外與海外急難救助 | finance, tutorial | 插 |  | ✓ |
| 11 | `flight-delay-baggage-insurance` | 不便險：班機延誤與行李延誤怎麼賠、證明怎麼留 | finance, tutorial | 插 |  | ✓ |
| 12 | `credit-card-travel-insurance` | 刷卡附贈的旅遊保險：保了什麼、沒保什麼 | finance | 插 |  | ✓ |
| 13 | `overseas-medical-claim` | 海外就醫與健保核退：要帶回來的文件與申請時限 | finance, tutorial | 插 |  | ✓ |
| 14 | `compulsory-auto-insurance` | 汽機車強制險與任意險：理賠範圍差在哪 | finance | 插 |  | ✓ |
| 15 | `home-fire-insurance` | 住宅火險與地震險：房貸綁的那張保單保了什麼 | finance | 插 |  |  |
| 16 | `insurance-policyholder-beneficiary` | 要保人、被保險人、受益人：填錯會怎麼樣 | finance, tutorial | 插 |  |  |
| 17 | `insurance-claim-process` | 理賠申請流程：文件、時限與被拒賠的常見原因 | finance, tutorial | 插 |  |  |
| 18 | `insurance-surrender-lapse` | 解約、停效與復效：繳不出保費時有哪些選項 | finance | 插 |  |  |
| 19 | `online-insurance-purchase` | 網路投保：能買什麼、和臨櫃差在哪 | finance, software | 插 |  | ✓ |
| 20 | `insurance-sales-questions` | 聽業務員說明時該問的問題：把話術換回條款 | finance | 照 |  |  |

第 10–13 篇是旅遊銜接篇。保險文尤其要守「不推薦個別保單」：講的是險種與條款結構。

### 批次 04｜稅務與政府制度

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 1 | `income-tax-filing-taiwan` | 綜所稅申報全流程：時程、申報方式與查詢碼 | finance, tutorial | 插 |  | ✓ |
| 2 | `tax-filing-app-guide` | 報稅 App 與線上申報教學：認證、下載所得與繳稅 | finance, tutorial | 插 |  | ✓ |
| 3 | `standard-vs-itemized-deduction` | 標準扣除額與列舉扣除額：哪一種對自己划算 | finance, tutorial | 插 |  | ✓ |
| 4 | `tax-dependents-taiwan` | 扶養親屬怎麼報：資格、文件與常見爭議 | finance | 插 |  | ✓ |
| 5 | `medical-expense-deduction` | 醫藥及生育費列舉：哪些收據可以用 | finance | 插 |  | ✓ |
| 6 | `donation-deduction-taiwan` | 捐贈列舉扣除：限額與收據要求 | finance | 插 |  | ✓ |
| 7 | `mortgage-interest-deduction` | 房貸利息扣除額：條件、上限與自用住宅認定 | finance | 插 |  | ✓ |
| 8 | `rent-expense-deduction` | 租金支出扣除：房東不配合時可以怎麼處理 | finance | 插 |  | ✓ |
| 9 | `dividend-income-tax-options` | 股利所得二擇一：合併課稅與分開計稅怎麼算 | finance, tutorial | 插 |  | ✓ |
| 10 | `overseas-income-minimum-tax` | 海外所得與最低稅負制：什麼時候需要申報 | finance | 插 |  | ✓ |
| 11 | `second-generation-nhi-supplement` | 二代健保補充保費：哪些收入會被扣、怎麼算 | finance | 插 |  | ✓ |
| 12 | `tax-refund-schedule-taiwan` | 退稅什麼時候入帳：批次時程與退稅方式 | finance | 插 |  | ✓ |
| 13 | `gift-tax-taiwan` | 贈與稅：免稅額、婚嫁贈與與父母幫忙買房 | finance | 插 |  | ✓ |
| 14 | `estate-tax-basics-taiwan` | 遺產稅入門：課稅範圍、扣除額與申報時限 | finance | 插 |  | ✓ |
| 15 | `house-land-transaction-tax` | 房地合一稅：持有期間與稅率級距怎麼對應 | finance | 插 |  | ✓ |
| 16 | `property-holding-tax` | 房屋稅與地價稅：自用稅率與繳納時程 | finance | 插 |  | ✓ |
| 17 | `overseas-shopping-customs-duty` | 海外購物關稅：郵包、快遞與自用免稅額怎麼算 | finance, tutorial | 插 |  | ✓ |
| 18 | `inbound-duty-free-allowance` | 入境台灣免稅額度：菸酒、行李與應申報物品 | finance, tutorial | 插 |  | ✓ |
| 19 | `side-income-tax-taiwan` | 兼職與接案的稅：扣繳、執行業務所得與費用率 | finance | 插 |  | ✓ |
| 20 | `government-subsidy-lookup` | 政府補助怎麼查：查詢入口、資格與常見申請 | finance, tutorial | 插 |  | ✓ |

**整批幾乎全是易變。** 級距與額度每年公告，寫作當天查財政部稅務入口網與各地區國稅局，
查不到的寫「以主管機關公告為準」。第 17、18 篇是旅遊銜接篇，連回「可連的旅遊攻略」表裡的
免稅與購物那幾篇。

### 批次 05｜投資入門：觀念與台股

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 1 | `before-you-invest-checklist` | 投資前先做完的四件事：緊急金、負債、保險與目標 | finance, tutorial | 插 |  |  |
| 2 | `compound-interest-explained` | 複利到底怎麼運作：用實際數字看時間的作用 | finance, tutorial | 插 |  |  |
| 3 | `risk-and-return-basics` | 風險與報酬：為什麼高報酬一定伴隨高風險 | finance, tutorial | 插 |  |  |
| 4 | `asset-allocation-basics` | 資產配置入門：股債現金的比例怎麼決定 | finance, tutorial | 插 |  |  |
| 5 | `what-is-a-stock` | 股票是什麼：股東權益、股價與公司價值的關係 | finance, tutorial | 插 |  |  |
| 6 | `what-is-an-etf` | ETF 是什麼：追蹤指數、內扣費用與折溢價 | finance, tutorial | 插 |  |  |
| 7 | `index-investing-explained` | 指數化投資是什麼：為什麼「不選股」也是一種策略 | finance, tutorial | 插 |  |  |
| 8 | `taiwan-brokerage-account-opening` | 台股開戶教學：證券戶、交割戶與電子下單 | finance, tutorial | 插 |  | ✓ |
| 9 | `taiwan-stock-order-types` | 台股下單方式：限價市價、ROD／IOC／FOK 與各盤別 | finance, tutorial | 插 |  |  |
| 10 | `odd-lot-trading-taiwan` | 零股怎麼買：盤中零股與定期定額的差別 | finance, tutorial | 插 |  | ✓ |
| 11 | `taiwan-trading-costs` | 台股交易成本：手續費、證交稅與折讓怎麼算 | finance | 插 |  | ✓ |
| 12 | `ex-dividend-taiwan` | 除權息是什麼：填權息、扣抵與要不要參與 | finance, tutorial | 插 |  |  |
| 13 | `dollar-cost-averaging` | 定期定額：適合什麼情況、什麼時候該檢討 | finance, tutorial | 插 |  |  |
| 14 | `portfolio-rebalancing` | 再平衡怎麼做：頻率、門檻與需要付出的成本 | finance, tutorial | 插 |  |  |
| 15 | `market-cap-vs-dividend-etf` | 市值型與高股息 ETF 的制度差異：選股邏輯與配息來源 | finance | 插 |  |  |
| 16 | `etf-expense-ratio-tracking-error` | 看 ETF 的內扣費用與追蹤誤差：公開說明書怎麼讀 | finance, tutorial | 插 |  |  |
| 17 | `mutual-fund-vs-etf` | 基金與 ETF 差在哪：申購方式、費用與交易時點 | finance | 插 |  |  |
| 18 | `investment-scam-red-flags` | 投資詐騙辨識：代操、假平台與「保證獲利」的共同特徵 | finance | 插 |  | ✓ |
| 19 | `financial-statement-basics` | 看懂財報三表：資產負債表、損益表與現金流量表 | finance, tutorial | 插 |  |  |
| 20 | `investment-information-sources` | 投資資訊怎麼查證：公開資訊觀測站與官方揭露管道 | finance, tutorial | 插 |  | ✓ |

第 15 篇只比較**制度差異**（選股邏輯、配息來源、除息機制），不比績效、不點名商品。
第 18 篇會引用「保證獲利」這類詞作為詐騙特徵，`banned_phrase` 的 lint warning 在這篇是預期的，
審稿時確認它是在指認話術而不是在使用話術。

### 批次 06｜海外投資、數位資產與退休

| # | slug | 標題 | topics | 圖 | 合作 | 易變 |
|---|---|---|---|---|---|---|
| 1 | `sub-brokerage-vs-foreign-broker` | 複委託與海外券商：成本結構與遺產處理的差別 | finance | 插 |  | ✓ |
| 2 | `w8ben-dividend-withholding` | W-8BEN 與股息扣繳：30% 是怎麼來的、怎麼填 | finance, tutorial | 插 |  | ✓ |
| 3 | `international-wire-transfer-cost` | 國際匯款成本：電匯費、中轉行與匯率價差 | finance, tutorial | 插 |  | ✓ |
| 4 | `us-stock-market-basics` | 美股市場基礎：交易時段、漲跌幅機制與報價單位 | finance, tutorial | 插 |  |  |
| 5 | `bond-basics` | 債券入門：票面利率、殖利率與價格為何反向 | finance, tutorial | 插 |  |  |
| 6 | `money-market-and-time-deposit` | 貨幣市場工具與定存：短期資金可以放哪裡 | finance | 插 |  | ✓ |
| 7 | `reits-basics` | REITs 是什麼：參與不動產的方式與風險 | finance | 插 |  |  |
| 8 | `gold-investment-channels` | 黃金的參與方式：實體、存摺與基金的差別 | finance | 插 |  |  |
| 9 | `forex-basics-for-individuals` | 外匯基礎：匯率怎麼看、個人換匯與投機的差別 | finance | 插 |  |  |
| 10 | `margin-and-leverage-risk` | 融資與槓桿的風險：維持率、追繳與強制平倉 | finance | 插 |  |  |
| 11 | `futures-options-risk-overview` | 期貨與選擇權：先理解風險再談工具 | finance | 插 |  |  |
| 12 | `what-is-cryptocurrency` | 加密貨幣是什麼：區塊鏈、代幣與價格從哪裡來 | finance, tutorial | 插 |  |  |
| 13 | `bitcoin-basics` | 比特幣入門：供給上限、挖礦與常見誤解 | finance, tutorial | 插 |  |  |
| 14 | `stablecoin-explained` | 穩定幣是什麼：錨定機制與脫鉤風險 | finance | 插 |  |  |
| 15 | `crypto-exchange-vs-wallet` | 交易所與自管錢包：私鑰、助記詞與保管責任 | finance, tutorial | 插 |  |  |
| 16 | `taiwan-vasp-regulation` | 台灣虛擬資產業者法遵現況：洗錢防制登記與投資人保護 | finance | 插 |  | ✓ |
| 17 | `crypto-tax-taiwan` | 加密貨幣的稅：交易所得、境內外與申報實務 | finance | 插 |  | ✓ |
| 18 | `behavioral-biases-investing` | 投資裡的行為偏誤：損失趨避、定錨與從眾 | finance, tutorial | 插 |  |  |
| 19 | `retirement-planning-calculation` | 退休金試算：勞保、勞退與自己要補的缺口 | finance, tutorial | 插 |  | ✓ |
| 20 | `fire-movement-realistic` | FIRE 提早退休：4% 法則的前提與台灣的差異 | finance | 插 |  |  |

加密貨幣那幾篇（12–17）風險最高，寫的是**運作機制與法遵現況**，不是參與建議；
第 16、17 篇的法規狀態變動快，每次回查都要重讀金管會與國稅局的公告。

## 教學中心（hub）：待批次 01–06 完成後再做

站主要的是「文章**與教學**」。站上已有兩套 hub 機制：

- **API 端**：`apps/api/app/guides/series_data/<slug>.json` ＋ `app/guides/series.py`，
  公開路由 `GET /guides/series/{series_slug}`（Claude Code 教學中心，60 課、10 群組、5 條學習路線）。
- **Web 端**：`apps/web/lib/guide-series.json` ＋ `apps/web/lib/gemini-series.ts`，
  前端自帶搜尋（Gemini 系列，50 篇）。

**現在不做**，因為 catalogue 的 validator 要求編號從 1 連續、每個 `prerequisites`／`related`
都要指到系列內存在的條目，而系列路由要求 hub 文章本身已發布——文章還沒寫，catalogue 沒東西可指。
**另外 `apps/api/tests/test_guide_series.py` 的 `(catalogue,) = catalogues()` 是解構成「剛好一個」
catalogue，在 `series_data/` 放第二個檔案會直接弄壞那個測試**，那是要一起改的真改動，
不該夾在內容票裡。

預定做法，等 01–06 落地後另開一張票：

- hub slug `personal-finance-tutorials`，走 API 端機制（財經要的是學習路線與先修順序，
  不是 Gemini 那種純搜尋）。
- 進 catalogue 的是**操作型**那些：記帳 App、開戶、載具設定、報稅 App、下單、零股、
  網路投保、W-8BEN、聯徵查詢——大約 30–40 篇，不是全部 120 篇。
- 群組按批次切，學習路線至少三條：「剛開始工作」「準備報稅」「第一次投資」。
- 那張票必須同時修 `test_guide_series.py`，讓它不再假設只有一個 catalogue。

## 經驗記錄

批次 01 是試點。02–06 開工前先讀這一節，細節在
[`tasks/done/2026-09-14-life-finance-batch-01.md`](../tasks/done/2026-09-14-life-finance-batch-01.md) 的 Outcome。

- **hero 不要畫成由低到高的長條**——渲染出來就是績效成長圖，是 brief 第 2 節自己禁止的
  視覺語言。順序題材用等大方塊排成一列。
- **字數會貼著上限寫。** 批次 01 每一篇都落在 2,900–3,031。brief 已加 10.6 節，
  批次 02 起瞄準 2,200–2,600 字，留審稿補字的餘裕。
- **政府網站 403 的兩種合格處理**：限定官方網域的 WebSearch 取回原句逐字比對；
  或放棄該來源改引其他官方單位。兩種都要在 `notes.md` 寫明讀取方式與快照日期。
  **不要引用自己沒讀到的網址。**
- **會過期的費率，用當期官方金額表反推驗證**，比引用舊公告可靠得多。
- **代理還在跑的時候就可以送修正回去**，而且要給可執行的判準，不要只說「再查一次」。
- **全部自繪插圖是對的決定**：20 篇沒有一篇需要照片，也沒有任何授權或商標問題。
- 一篇一個代理，每篇約 19–33 分鐘。

批次 02 補充（額度中斷那一次）：

- **額度是整個 session 累積的，不是看同時開幾個代理。** 批次 01 的 18 個並行代理沒事，
  於是這裡本來寫著「不必限制每波幾個」——這個推論是錯的。批次 01 用掉的量加上批次 02
  前半段，才在第二批中途觸頂，一次砍掉 10 個還在跑的代理。
  `docs/life-ai-series.md` 的「每波最多七個」結論是對的，只是理由不是並行數。
  **一個 session 連續派兩批 20 篇會觸頂，第二批要分波，或換一個 session。**
- **被額度砍掉的代理救不回來，但它的工作區還在。** 代理一旦以 429 結束就不可續跑
  （`SendMessage` 會回 no agent reachable），不過它寫到磁碟的 `pack.json`、SVG 都還在。
  正確的復原方式是**派新代理接手那個工作區**，明講現有哪幾個檔案、缺哪幾個，
  並要求它自己重新查證一次再寫 `notes.md`——查證紀錄不能從別人的草稿推回來。
  那 10 篇的 `pack.json` 其實都已經寫完（2,615–2,957 字），缺的多半只是 SVG 與 `notes.md`。
- **dry-run 不會把 PNG 留在工作區。** 代理要看自己畫的圖，得自己渲染：
  `from app.guides.pack_ingest import render_svg` 然後對 `hero.svg`／`diagram-1.svg` 各跑一次。
  指派時要把這段指令直接給它，否則「用眼睛看過」那一步會被跳掉。
- **前後遮蔽是機械檢查抓不到的第二種版面錯。** `installment-zero-interest-cost` 的天平，
  左盤吊牌蓋住了吊桿、右盤沒有，左盤看起來是浮空的。對稱結構要確認兩邊被前景蓋掉的
  程度一樣。這和「標籤壓線」是同一類問題：只有真的把圖打開看才會發現。
- **圖上想寫數字又不想觸發比對，就寫中文數字。** 數字比對只認阿拉伯數字，
  「一萬美元」不會被檢查，「10,000 美元」會。
- **WebFetch 對 PDF 會給出「看起來像引文、但和內文對不上」的東西。** `overseas-atm-withdrawal`
  查銀行局的兩份 PDF 時，WebFetch 一份讀不出、一份回了與實際內容不符的引文；代理自己寫
  FlateDecode＋ToUnicode 抽字之後，發現原稿引的那句實際上是**「於國內使用金融卡所領取之外幣」**，
  兩份全文裡「國外」出現 0 次——整段海外折算依據的主張是錯的。`online-banking-security`
  也是為了讀銀行公會的 PDF 自寫 ObjStm 解析器。**要引 PDF 裡的句子，就把 PDF 抓下來自己抽字**，
  不要相信摘要。這和批次 01 那次「二十七萬元被譯成 2.7 million」是同一類問題：
  工具轉述會出錯，原文不會。
