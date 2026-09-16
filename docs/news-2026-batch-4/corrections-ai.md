# 批次 4 AI 垂直：撰稿前必須套用的修正清單

這份檔案是 `docs/news-2026-batch-4/research/ai-news-*.json`（研究紀錄）與
`docs/news-2026-batch-4/factcheck/ai-news-*.json`（獨立查核）逐篇比對後的結果，
**對 AI 垂直的撰稿代理具有拘束力**。12 篇的查核結論全部是 `needs_fixes`，
研究紀錄裡留著的錯誤如果照抄就會上線；撰稿代理不能重讀來源，錯誤不會有第二次攔截。

使用方式：開稿前先讀本篇對應的 slug 段落，再讀研究紀錄。
`must_fix` 的每一條都是「紀錄寫了 X／X 錯在哪／改寫成 Z」，照著改；
寫「不要寫這一句」「整條刪掉」的就整句刪掉，不要改寫成比較婉轉的版本。

四個全域提醒：

- 本檔引用事實時一律寫 **`verified_facts` 陣列的 1-based 位置**（第 1 條＝陣列第一個元素）。
  查核檔本身的編號不一致，**不要拿查核檔的 `F##` / `verified_facts[n]` 直接對位**。
  對照表（查核檔的寫法 → 研究紀錄的 1-based 位置）：
  0-based（查核檔的 n ＝ 紀錄第 n+1 條）：`chatgpt-ads`、`chatgpt-storage-scale`、
  `frontier-governance`、`gpt-55-instant`、`gpt-live-1-api`、`nvidia-hugging-face`、
  `openai-broadcom-chip`、`openai-funding`。
  1-based（查核檔的 n ＝ 紀錄第 n 條）：`chatgpt-financial-services`、`gemini-38-live`、
  `openai-astral`、`openai-s1`。
- 所有查核與研究的 `checked_on` 都是 **2026-09-16**，正文第二段的查核日一律寫 2026 年 9 月 16 日。
- `sources[]` 上限 4 條、下限 2 條，只放一手來源（`BRIEF.md`）。
  **文章裡的每一個事實都必須指得到 `sources[]` 裡的某一條 url**；
  指到 `sources[]` 以外的網址等於沒有來源，那句話就不能寫。
  本檔每篇的 `source_list_fix` 已經把「哪幾條事實掛在 sources 以外的網址」逐條列出。
- **AI 篇不帶 `finance` 主題、不加投資免責 callout**（`ai.md`）。這條沒有例外，
  包括 `ai-news-chatgpt-financial-services-20260910`——詳見該篇 `must_fix` 第 1 條。

---
## ai-news-chatgpt-ads-20260505

OpenAI 2026-05-05 的〈New ways to buy ChatGPT ads〉。研究紀錄 41 條事實、4 條 sources，
查核確認 34 條。公告原文頁 403，全篇只能靠官方 RSS 的一句描述＋developers.openai.com 的廣告文件。

### must_fix

1. 紀錄第 1 條寫「feed 於 2026-09-16 取得時有 **1,194 筆 item**，最新一筆 pubDate 為
   Wed, 16 Sep 2026 13:00:00 GMT，所以是活的」。**這兩個數字都已被推翻。**
   查核者同一天再抓：724,913 bytes、**1,195 筆 `<item>`**、lastBuildDate
   `Wed, 16 Sep 2026 15:30:49 GMT`、最新一筆是〈Helping older adults use AI in everyday life〉、
   pubDate `Wed, 16 Sep 2026 16:00:00 GMT`。**筆數與最新時間都不准寫進文章與研究紀錄。**
   第 1 條其餘部分逐字確認無誤，可以寫：標題 `New ways to buy ChatGPT ads`、
   pubDate `Tue, 05 May 2026 00:00:00 GMT`、category `Product`、
   link 與 guid（isPermaLink=true）都是 `https://openai.com/index/new-ways-to-buy-chatgpt-ads`。
2. `overlaps_existing_article` 結尾寫「An article pinned to 2026-05-05 is the **fourth** event
   in a six-event line」。**算錯了。** 研究紀錄自己列的六則依序是
   2026-01-16、2026-05-05、2026-08-11、2026-08-18、2026-08-31、2026-09-16，
   5/5 是**第二則**，不是第四則；把 2026-01-18 的 business-model 那篇也算進去才變第三則。
   **改寫成**：「5/5 是這條廣告產品線六則官方公告裡的第二則。」
   （這句是「文章有多過時」的整個論證基礎，錯了會整段推論錯。）
3. `corrections_to_candidate_list` 第 3 條寫「On 2026-09-16 the feed's newest item is
   *Reimagining advertising with AI*, pubDate Wed, 16 Sep 2026 13:00:00 GMT」。**不正確。**
   查核者抓到時最新一筆是〈Helping older adults use AI in everyday life〉（16:00:00 GMT），
   〈Reimagining advertising with AI〉是第二新。**改寫成**：「2026-09-16 當天 OpenAI 至少
   發了兩則（13:00 與 16:00 GMT），所以 `candidates-tech-and-ai.md` 第 82 行的
   『查否：OpenAI 在 9/15–9/16 沒有發布消息』已經過期；9/15 仍然沒有項目。」
4. 紀錄第 40 條寫 OpenAPI 規格「confirms the enumerations rather than leaving them to prose」
   （只是替文字敘述背書）。**不成立。** 規格不只背書，還多出文件沒寫的東西：
   `components/schemas/CreateCampaignBody` 同時帶 `bidding_type`
   （enum impressions/clicks/conversions）**與另一個 `objective` 屬性**
   （`CampaignObjectiveParam`，enum `['reach','clicks','conversions']`），
   其中 `reach` 不出現在任何一張文件表格裡。
   **改寫成**：「規格裡的列舉值與文字敘述一致，但規格另有一個文件從未說明的 `objective` 欄位，
   其中 `reach` 這個值在官方文件裡找不到對應說明，本文不描述它。」
   第 40 條其餘子項全部確認：openapi 3.1.0、info.version 2.3.0、64 個 path、
   servers[0].url `https://api.ads.openai.com/v1`、billing_event_type impression/click、
   BiddingStrategyTypeParam fixed_bid/maximize_clicks/maximize_conversions、
   `automated_bid` 只出現在 `BiddingStrategyTypeBody`（回應 schema）。
5. 紀錄第 16 條寫「There are **exactly three** campaign objectives」。
   對照那一頁確實只有三個（五列表格與欄名 `Campaign objective (bidding_type)` 都逐字確認），
   但一旦把規格裡的 `objective`／`reach` 算進來，「恰好三個」就是不安全的斷言。
   **改寫成**：「bidding-and-budgets 那張出價與預算表列出三種 campaign objective」，
   把「恰好／exactly」拿掉，並把範圍限定在那張表。
6. 紀錄第 9 條寫「The self-serve product is called Ads Manager」並把 url 掛在
   `https://developers.openai.com/ads/api-overview`。**那一頁從未出現 self-serve 這個詞。**
   該頁逐字只有：`You will need an [ad account](https://ads.openai.com/) and an Advertiser API key.
   You can create your Advertiser API key within the [Settings page](https://ads.openai.com/settings)
   in Ads Manager`。「self-serve」來自 RSS 描述（`a beta self-serve Ads Manager`）與
   bulk-api 的額度表（`Self-serve campaigns per ad account`），兩者都不是被引用的那個網址。
   **拆成兩條事實**：Ads Manager 的位置與 API key 產生方式掛 api-overview；
   「自助（self-serve）」這個字掛 RSS 描述，並寫成「OpenAI 在公告描述裡用的字是 self-serve」。
7. 紀錄第 30 條把 25,000 名比對到的使用者寫成「a documented floor（官方寫明的下限）」。
   **必須補上同一批文件的但書**，那段文字研究者自己也抓過：
   `For inclusion and bid adjustments, use 25,000 matched users as the public planning threshold.
   Privacy safeguards can affect the exact boundary, and uploading 25,000 identifiers doesn't
   guarantee enough matched users.`
   **改寫成**：「官方把 25,000 寫成公開的規劃門檻，並說明隱私保護機制會影響實際邊界，
   上傳 25,000 筆識別碼也不保證比對得到足夠人數。」不可寫成硬性下限。
8. 紀錄第 37 條把成效指標列成完整清單（impressions、clicks、spend、ctr、cpc、cpm、
   conversions、cpa、post_click_cvr、order_created_attributed_sales、order_created_roas）。
   **十一個都正確，但不是全部**：同一頁還記載 `view_through_conversions` 與
   `product.carousel_product_card_impressions` / `product.carousel_product_card_clicks`。
   **改寫成**：「官方文件列出的指標包括……」，不要寫成窮舉。
9. 紀錄第 41 條的 `verbatim_quote` 是
   `<loc>…new-ways-to-buy-chatgpt-ads/</loc><lastmod>2026-05-22T19:11:20.545Z</lastmod>`。
   **數值全對**（查核者重抓 sitemap，四個 lastmod 逐毫秒吻合），
   **但這不是逐字原文**：sitemap 在 `</loc>` 與 `<lastmod>` 之間有換行與縮排，
   這串是重排過的拼接。**改寫成**：標成「讀到的值」，不要標成引文。
10. 紀錄第 35 條把 view-through 回報寫成「就是有這個功能」。
    measurement-pixel 那一頁對它下了兩層條件：`when available for your account`，
    以及 `Whether view-through reporting is available does not depend on your configured click window.`
    **改寫成**：「官方說明這項回報是否可用要看帳戶，而且與設定的點擊歸因視窗無關。」
    第 35 條其餘逐字正確，包括
    `CPA, post-click CVR, bidding, billing, and conversion optimization also remain click-through-based.`
11. 紀錄第 18 條（`OpenAI adjusts bids to seek more clicks from your budget`）與
    第 32 條（`OpenAI charges you only when a valid click occurs`）都標成 `is_vendor_claim=false`。
    兩句確實是官方文件逐字，可以寫，**但一律寫成「官方文件寫明」**，
    不可寫成本站或任何人觀察到的行為。

### must_add

- **UTC 與台北時間的跨日問題，研究紀錄完全沒處理。**
  〈ChatGPT Ads expands across Europe〉的 pubDate 是 `Tue, 18 Aug 2026 22:00:00 GMT`，
  換算台北時間是 **2026-08-19 清晨 6 點**；zh-TW 文章寫「8 月 18 日」就是日期混淆。
  5/5 那則是 00:00:00 GMT（台北 5/5 08:00），所以 event_date、slug 與 news_date 用 2026-05-05 安全；
  8/11（10:00 GMT）與 8/31（04:00 GMT）也安全。
- **一個研究者已經抓過卻沒記的開放條件**（conversion-optimized-campaigns）：
  `The ad account supports conversion bidding. If campaign creation returns 403 with
  Conversion bidding is not enabled, contact your OpenAI partner representative.`
  也就是 oCPC 不是每個廣告帳戶都自動開通。BRIEF 要求分批開放／限制分開寫，這正是一條。
- **直接回答「廣告主到底看得到我什麼」的一手機制**（custom-audiences），
  目前只躺在 `unverified_or_excluded` 的理由欄裡、沒進 `verified_facts`：
  比對人數是以隱私保護的**區間**回傳——`under_25k`、`25k_100k`、`100k_500k`、`500k_1m`，
  超過 5,000,000 再更寬——而且官方寫 `Don't use a count range to decide targeting eligibility.`
  這是可查核的機制，不是廠商宣稱，代表廣告主拿不到逐人的數字。
- **來自 sources 內（campaign-targeting）卻沒記下的具體數字**：
  地區包含／排除清單上限 2,500 個 ID；
  `Audience uploads support email, phone, their supported SHA-256 variants, and GAID identifiers`；
  名單檔案 `must be no larger than 500,000,000 bytes`；平台分組就是
  `ios_app` / `android_app` / `web` 三種。識別碼那一句是「廣告主到底上傳了我的什麼」最直接的答案。
- **來自 sources 內（api-overview）的一句**，可以把第 13 條的審核論點講得更準：
  `An account marked active may still have an outstanding review.`
- **規格裡有、文件沒有的欄位，明列出來避免有人自行腦補**：
  `CreateCampaignBody` 另外帶 `business_agent_id` 與 `landing_page_configuration`，
  兩者在文件與 `llms-full.txt` 裡都找不到任何說明。`business_agent_id` 看起來和 9/16 的
  Sponsored Agents 有關，**但沒有任何一手文字，一個字都不能寫**。
- **重疊警告經查核者獨立確認，不可放寬**：`apps/api/app/guides/content/chatgpt-ads-status.json`
  確實存在——slug `chatgpt-ads-status`、kind `life`、topics `['tutorial','ai-chat']`、
  display_order 100、只有 zh-TW、33 個 block、
  title「ChatGPT 廣告怎麼查：開放地區、官方規則與品牌準備」、五條 sources 的 checked_on 都是
  2026-09-14，其中一條就是 `https://openai.com/index/new-ways-to-buy-chatgpt-ads/`，
  另有兩條是 403 的 help.openai.com 文章。它**沒有** `news_date`，也沒有頂層 `checked_on`。
- 紀錄第 29 條那個「全稱」主張經查核者實測為真：`conversation` 這個字在 355,929 bytes 的
  `llms-full.txt` 裡**只出現一次**，就在
  `These examples illustrate writing style, not a guarantee that a particular conversation will trigger an ad.`
- 候選清單的行號經查核者逐一核對無誤：第 133 行是 2026-05-05 那列、
  第 376／377 行是 8/11 與 8/18 兩列、第 82 行是「查否：OpenAI 在 9/15–9/16 沒有發布消息」。

### live_data_warnings

- **RSS 的 item 筆數與最新一筆時間**：紀錄寫 1,194／13:00 GMT，查核者數小時後是 1,195／16:00 GMT，
  lastBuildDate 也變了。**永遠不要把 feed 筆數或最新項目寫進文章。**
- **sitemap 的 lastmod 全部是活值**：`testing-ads-in-chatgpt` 2026-09-15T11:52:14.524Z、
  `chatgpt-ads-expands-across-europe` 2026-09-16T12:50:39.497Z、
  `expanding-access-to-ai-with-chatgpt-ads` 2026-09-16T12:50:35.814Z、
  `new-ways-to-buy-chatgpt-ads` 2026-05-22T19:11:20.545Z，
  外加研究者沒列的 `reimagining-advertising-with-ai` 2026-09-16T13:03:27.128Z。
  可以拿來說明「官方頁在發布後被改過」，但不要把時間戳當成內容更新日。
- **各種檔案大小與筆數都是快照**：`openai.com/sitemap.xml/product/` 186 個 `<url>`、
  `sitemap-0.xml` 1,315 個 `<loc>`、`/ads/` 底下 31 頁、38 份子 sitemap、
  feed body 724,913 vs 725,972 bytes。一律不入稿。
- **developers.openai.com 的廣告文件全部沒有發布日與版本號**，是會被改的活頁面；
  文中必須寫明「本文於 2026 年 9 月 16 日讀到的版本」，而且**不可拿來描述 2026-05-05 當天的產品**
  （changelog 最早的有日期條目是 2026-06-03）。`openapi.json` 的 `info.version 2.3.0` 與
  64 個 path 同理，會變。
- 8/31 那則的「$1 billion in annualized revenue run rate」是特定時點的公司自報數字，
  只能寫成「OpenAI 在 8 月 31 日的公告描述中表示」，且不屬於 5/5 這篇的事件。

### source_list_fix

**需要重建。** 目前 4 條已到上限且全部可達（HTTP 200、真實內容），但問題有三個：

1. **11 條事實掛在 sources 以外的網址**：第 31 條（custom-audiences）、32（conversion-optimized-campaigns）、
   33（conversion-tracking）、34 與 35（measurement-pixel）、36（supported-events）、37（reporting）、
   38（api-reference/ads）、39（bulk-api）、40（openapi.json）、41（sitemap.xml/product/）。
   研究紀錄自己用 `[NOT IN sources]` 標了，但**沒有改 sources**。
   要用哪一條就把它換進四條裡；沒換進去的那些事實不能寫。
2. 第 9 條的「self-serve」實際上出自 RSS 與 bulk-api，不是被引用的 api-overview（見 must_fix 6）。
3. `sources[0]` 是 feed 網址（`openai.com/news/rss.xml`），與 BRIEF「sources 放的是文章頁的網址，
   不是 feed 的網址」抵觸。本篇的文章頁 403、確實讀不到，這是編輯要明白裁量的例外，
   不可讓後續查核者「修正」成那個 403 網址。
   另注意 OpenAI 自家 sitemap 給的正規網址帶尾斜線
   （`https://developers.openai.com/ads/api-overview/` 等）；兩種寫法都回 200、不轉址，
   但帶斜線那個才是 canonical。

---
## ai-news-chatgpt-financial-services-20260910

OpenAI 2026-09-10 的〈Introducing ChatGPT for Financial Services〉。研究紀錄 34 條事實，查核確認 30 條。
**本篇的查核檔用 1-based 編號，與研究紀錄位置一致。**

### must_fix

1. **最嚴重的一條：`editorial_brief`、`must_not_write` 第 15／16 條與
   `corrections_to_candidate_list` 第 2 條建議 topics 用 `["ai","finance","ai-news"]`
   並強制加五語投資免責 callout，還說這是派工單的硬性要求。這與 `ai.md` 直接牴觸，而且 `ai.md` 贏。**
   `ai.md` 逐字點名這個 slug，判的是相反方向：B8 **不掛 finance、用一般 callout**，
   理由原文是「掛上 finance 會讓一篇 AI 新聞出現在理財專區，那是分類錯誤，而且會連帶觸發
   `finance_no_disclaimer`（error 級）去要求一段它不需要的投資免責」。
   研究紀錄引用的 `pack_ingest.py` 事實本身都對（`FINANCE_TOPICS = {finance, investing, crypto}` 在第 117 行、
   `FINANCE_DISCLAIMER_MARKERS` 在第 97 行、`finance_no_disclaimer` 在第 363 行），
   但那是**不要掛 finance 的理由**，不是要掛的理由。
   **照 `ai.md` 做**：topics 用 `["ai", <橫向主題>, "ai-news"]`、不掛 finance、
   **不要投資免責 callout**，改用一般 callout 明講：本文寫的是一個給金融機構的工具、
   本站沒有試用、也不是投資建議。`must_not_write` 第 15、16 兩條整條作廢。
2. 紀錄的 `event_date_basis` 與 `unverified_or_excluded` 第 13 條說
   「sitemap lastmod `2026-09-11T23:41:13.520Z` 是網站建置時間戳、大量頁面同時變動，不能當更新日」。
   **這個理由不成立。** 查核者逐封存比對：`20260910185345` 版 Crunchbase 出現 0 次、Quartr 6 次；
   `20260911101011` 版 Crunchbase 19 次、Quartr 0 次（加入 Crunchbase、刪掉錯誤率圖）；
   `20260911215402` 版再加上 Fiscal.ai 9 次。**兩次改動都發生在 2026-09-11**，23:41:13Z 就在同一天。
   而且 product 分區 186 個 url 裡只有 22 個帶 09-11 的 lastmod（09-15 有 61 個、09-16 有 27 個），
   根本不是整批重建。**改寫成**：內容確實在 2026-09-11 被改過兩次，lastmod 與之相符。
3. 紀錄第 24 條與 `unverified_or_excluded` 第 8 條寫「頁面的行動按鈕連到
   `/business/contact-sales-financial-services/` 與 `/contact-sales/`」。**後者是錯的。**
   文章的兩個 CTA 都指向 `/business/contact-sales-financial-services/`：
   hero 按鈕標籤 `Contact financial services sales`
   （data-analytics `finserv-blog-cta-contact-financial-services-sales`）與
   prefooter 按鈕 `Contact sales`（`finserv-blog-prefooter-cta-contact-sales`）。
   頁面上唯一那個 `openai.com/contact-sales/` 是**全站頁尾導覽連結**
   （`footer-nav-for-business-contact-sales`，在 For Business 欄），每一頁都有，不是文章的 CTA。
   另外，供應狀況段落裡的 `contact us` 在兩個封存版裡都是**純文字、沒有超連結**。
   **改寫成**：只寫一個 CTA 網址，並刪掉「contact us 是連結」的暗示。
4. 紀錄第 27 條寫「這一頁是活文件：2026-09-10 上線版與 2026-09-14 版**至少有三處**改動，
   撰稿必須寫明依據的是 2026 年 9 月 14 日的版本」。**日期錯、數量也低估。**
   改動發生在 **2026-09-11**、分兩次；頁面自 2026-09-11 21:54 UTC 起到最新封存
   2026-09-14 01:29 UTC 之間都沒再動。實際至少**七處**：內文資料商清單加入 Crunchbase；
   「Premium financial data」段的資料商清單加入 Crunchbase；新增 Crunchbase 引言與 Jager McConnell；
   新增 Fiscal.ai 引言與 Braden Dennis；MCP 段刪掉 `like S&P Global and FactSet`；
   connector 生態清單加入 FactSet；刪掉「Error rate」圖（Quartr 5.09%→1.99%、
   S&P Global 6.84%→2.66%、FactSet 9.59%→6.45%、Daloopa 7.53%→2.57%）與其圖說。
   **正文要寫的說法是「2026 年 9 月 11 日起的版本」，不是「9 月 14 日的版本」。**
5. 紀錄第 28 條把 Free 0 美元／Go 8 美元／Plus 20 美元／Pro 100 美元起／
   Business 每人 20 美元（2 人以上、年繳，月繳 25 美元）／Enterprise & Edu 洽詢
   寫成「ChatGPT 的方案定價」。**每個數字都印得沒錯、「整份沒提 Financial Services」也對
   （`financial` 0 命中），但框架錯了**：那一頁把這些全部框成 **Codex 方案**——
   切換器 id 是 `codex-pricing-plans`，副標是
   `Explore Codex capabilities on quick coding tasks`、`Use Codex for lightweight coding tasks`、
   `Power a few focused coding sessions each week`、`Bring Codex into your startup or growing business`、
   `Unlock Codex for your entire organization`；而且還漏掉第七張卡
   `API Key`（無價格，`Pay for Codex usage based on API pricing`）。
   照現在的寫法，撰稿者會把 8／20／100 美元丟進一篇講企業產品的文章裡。
   **把這條收窄成**：「OpenAI 自家的 ChatGPT 產品文件定價頁上，沒有 ChatGPT for Financial Services 的任何價格。」
6. 紀錄第 1 條的 `verbatim_quote`
   `OpenAISeptember 10, 2026 / Product / Introducing ChatGPT for Financial Services`
   **是拼出來的字串，不是頁面上的字串**。實際標記是 `<p>September 10, 2026</p><a>Product</a>` 加一個 `<h1>`；
   頁面上**沒有 OpenAI 這個作者署名**（唯一的 `OpenAI</span>` 是導覽列 logo），也沒有 ` / ` 分隔。
   事實本身成立（publicationDateText `September 10, 2026`、分類連結 `Product`、h1 是那個標題），
   **只把 `verbatim_quote` 換成單一存在的字串，或標成「讀到的值」**。
   同型問題：第 28 條的引文是跨約六行、用刪節號接起來的拼裝；
   第 26、27、33、34 條的 `verbatim_quote` 是**空的**；
   第 3 條的 og:url 主張只有內嵌的 Next.js RSC payload 支撐——封存 HTML 裡看得見的
   `<meta property="og:url">` 已被 Wayback 改寫成 web.archive.org 位址。

### must_add

- 文章自己的一句定位（hero 副標），紀錄完全沒有：`Frontier intelligence, built for financial services.`
- **對台灣一般讀者最可用的一段能力描述**，34 條事實裡沒有：
  `It can navigate and understand figures, tables, and the supporting notes in financial documents.
  It can take inputs, run financial analysis, and draw conclusions. And it can take all of this work
  and accurately synthesize it into documents, spreadsheets, and slides.`
- 官方唯一承認「目前涵蓋範圍不是最終版」的一段：
  `Our partners are central to this work and as we expand coverage, we will continue to deepen our
  models' understanding of these datasets. We will post train our models to find, interpret, and use
  this data like we know the best analysts can.`
- **互動圖表功能整個漏掉**：`We've built fundamental capabilities into the product so that it can
  research across multiple sources, trace figures across different periods, and interpret annotations
  in public data. Once that analysis is complete, teams can build interactive charts and visualizations.`
  圖說是 `Compare company performance in interactive charts, with the underlying data and sources
  available for review.`
- **整個「Expanding what the industry can achieve」段落漏掉**，那是 OpenAI 自己承認一個產品蓋不了整個產業
  （`we recognize that it will require a range of solutions`），並說機構與開發者可以用 API 自建應用。
  這是重要的框架資訊。
- 官方自己對資料故事的三段式總結：`ChatGPT for Financial Services brings together the financial data
  teams need, with the depth of detail expected. We've included premium financial data, streamlined
  existing provider connections, and improved MCP performance.`
- 現行版 MCP 那一句從來沒被記成事實、只出現在差異比對裡：
  `It can be challenging to effectively use MCP connectors for data providers. We have focused on making
  some of the most used MCPs in financial services optimized for immediate use in the product, so teams
  can spend less time troubleshooting requests and more time on analysis.`
  另漏兩段圖說：`ChatGPT for Financial Services brings together built-in data, connected sources, and
  financial analysis workflows.`、`Publish firm templates to the teams who use them.`
  以及 prefooter 區塊 `Bring ChatGPT for Financial Services to your firm` /
  `Equip your teams with GPT-6 Astra, included financial data, and new tools for research,
  financial modeling, and client materials.`
- **更好的一手管道（研究者用不到、查核者用到了）**：
  `https://web.archive.org/web/timemap/link/<url>` 在本容器回 200，可列出全部 8 個封存
  （20260910175211、20260910185332、20260910185345、20260911101011、20260911163047、
  20260911215402、20260912024658、20260914012930），最新就是 20260914012930。
  研究者回報 CDX API「Temporarily Offline」而改用時間戳轉址，其實 timemap 可用，
  而且正是靠它才把改動釘在 2026-09-11。
- **經查核者攻擊後仍站得住的部分，撰稿可以放心用**：三張評測圖的數字全對——
  OfficeQA Pro：GPT-6 Astra 69.9／GPT-5.6 Sol 60.2／Claude Fable 5.1 62.4（Y 軸 `Correctness`）；
  BoxBench：0.77／0.74／0.72（Y 軸 `Weighted rubric accuracy`）；
  簡報圖標題 `["Slides Head to Head (Internal)","Versus Opus 5"]`、Y 軸 `Win Rate (Human Eval)`、
  GPT-5.5 0.216／GPT-5.6 Sol 0.306／GPT-6 Astra 0.556，而圖說寫「only 21.6% for GPT-5.6 Sol」。
  **圖說與圖表資料的矛盾是真的、兩個版本都有，只寫 55.6% 的決定是對的。**
  三段圖說逐字無誤，三條都正確標成 `is_vendor_claim`。
  第 2、4–23、25、26、29–33 條全部逐字正確；第 26 條六位具名主管全部核對過
  （Jager McConnell／Crunchbase CEO、Thomas Li／Daloopa CEO、Tom Van Buskirk／PitchBook EVP of
  Technology and Engineering、Braden Dennis／Fiscal.ai CEO、Sally Moore／S&P Global
  Chief Client Officer and Co-Head of Market Intelligence, Kensho Data & Platforms、
  Emily Prince／LSEG Group Head of Enterprise AI）。16 條 `not_said` 全部攻不破。
  `corrections_to_candidate_list` 第 1、3、4 條也都查證屬實。

### live_data_warnings

- **官方公告頁是活文件**：2026-09-11 當天被改了兩次，2026-09-16 的線上版本容器讀不到。
  正文必須寫明依據的是**「2026 年 9 月 11 日起的版本」**與查核日 2026-09-16。
- **已被官方撤下的數字絕對不可用**：connector 錯誤率 Quartr 5.09%→1.99%、
  S&P Global 6.84%→2.66%、FactSet 9.59%→6.45%、Daloopa 7.53%→2.57%（`must_not_write` 第 6 條正確，維持）。
- **sitemap lastmod 是活值**：`/policies/financial-services-terms/` 2026-09-16T09:39:18.917Z、
  `/business/contact-sales-financial-services/` 2026-09-15T15:57:50.711Z、
  公告頁本身 2026-09-11T23:41:13.520Z。可以用來佐證「頁面被改過」，但不要當內容更新日印出來。
- **feed 與 sitemap 的筆數都會動**：研究紀錄寫 1,194 筆 item，查核者數到 1,195；
  product 分區 186 個 url、lastmod 日期分布（09-15 61 筆、09-16 27 筆、09-11 22 筆）同理。不入稿。
- 「connector 生態超過 50+ 個」是官方在活文件上的自報數字，只能寫「OpenAI 表示」，
  而且要照官方那個重複的寫法引述（`over 50+ connectors`）。
- `learn.chatgpt.com` 的定價頁與 `llms.txt`（323 行）都是活文件；
  「整站沒有這個產品的說明頁」這個負面結論只在 2026-09-16 成立，要寫成「查核當天未見」。

### source_list_fix

**不能照現況出刊，需要編輯裁量。**

1. `sources[0]` = `https://openai.com/index/introducing-chatgpt-financial-services/`
   帶著 `checked_on: 2026-09-16`，但那一頁在本容器回 **HTTP 403**（9,857 bytes 的 Cloudflare 挑戰頁），
   **沒有任何人在 2026-09-16 讀過它**。整篇的實質內容都是從 `web.archive.org` 的封存讀來的
   （第 1、3–26 條掛 20260914012930 的封存、第 27 條掛 20260910175211 的封存），
   而 web.archive.org 不在 `sources[]` 裡。
   BRIEF 對 403 的規定是「換同一官方站的其他頁、官方 RSS……查到的事實如果只存在於被擋的頁面後面，那就不寫」，
   **封存路線不是規格授權的做法**。編輯必須二選一：
   明白裁量接受封存路線（並在正文自己說明依據的是官方頁的封存版本），或把 B8 當成被擋、不寫。
2. 另外三條 sources（learn.chatgpt.com 的 pricing / ChatGPT Work overview / Plugin controls）
   **完全沒有提到 ChatGPT for Financial Services**（`financial` 在 pricing.md 與 323 行的 llms.txt 裡
   都是 0 命中），只能支撐背景與「官方沒說」的負面結論。
   所以這一包實質上只有**一條**能支撐主題的來源，低於 BRIEF 的「至少 2 條一手來源」。
3. 事實掛在 sources 以外網址的還有：第 2 條（`openai.com/news/rss.xml`）、
   第 28–32 條（`.md` 版網址，與 sources 的 HTML 網址不同字串）、
   第 33 條（`learn.chatgpt.com/llms.txt`）、
   第 34 條（`openai.com/sitemap.xml`——而且如下）。
4. 第 34 條寫「官方 sitemap 列有 `/policies/financial-services-terms/` 與
   `/business/contact-sales-financial-services/`」並掛在 `https://openai.com/sitemap.xml`。
   **主張為真但網址錯**：`openai.com/sitemap.xml` 只有 3,414 bytes、是子 sitemap 的索引，
   裡面沒有這兩個路徑；它們在 `https://openai.com/sitemap.xml/page/`（3,234,989 bytes）。
   要用就改掛正確網址。
5. 研究紀錄的 `must_not_write` 第 12 條（sources 不得放 web.archive.org 網址）與第 1 條的作法相衝：
   若編輯裁量接受封存，正文與 sources 的處理方式必須一致，不能一邊引封存一邊宣稱讀的是官方頁。

### 額外：規格合規

- `hero_label`「AI 進投行，先看得懂來源」是 **13 個字**，超過 BRIEF 的「繁中 ≤ 12 字」。要改短。
- `title` 還是占位字串「（撰稿時填入 zh-TW title，≤ 60 字）」，`diagram.caption` 也是占位字串，兩者都是必填。
- `diagram` 節點「四家資料商直接可用」把家數寫死成四家，但官方原文是 `providers like …`（非窮舉），
  而且同一頁把 Fiscal.ai 以資料夥伴身分放了 CEO 引言與 logo。
  研究紀錄自己的 `unverified_or_excluded` 第 4 條與 `must_not_write` 第 9 條已經點出這個張力，
  **圖解與它們互相矛盾，要改掉圖上的家數**。

---
## ai-news-chatgpt-storage-scale-20260911

OpenAI 2026-09-11 的工程部落格〈Rapidly scaling online storage to serve over 1 billion ChatGPT users〉。
研究紀錄 37 條事實，查核確認 33 條。**查核檔用 0-based 編號**（`verified_facts[3]` ＝紀錄第 4 條）。

### must_fix

1. 紀錄 `unverified_or_excluded` 第 6 條寫「x.com 的伺服器端輸出沒有 tweet 的 `created_at`，
   唯一的時間戳是附圖的 uploadDate 2026-09-11T20:00:41.000Z，所以只記到『2026-09-11』」。
   **錯了，而且是把手上已有的資料讀漏了。** 該頁的 payload 對整串每一則都給了 `created_at_ms`：
   **1789156841000、1789156844000、1789156847000**（另有一則後續回覆 1789157484000），
   換算就是 **2026-09-11T20:00:41Z、20:00:44Z、20:00:47Z**。
   **改寫成**：記下這三個時間，並說明推文在 feed 的 10:00 GMT 之後約 10 小時，
   因此**推文時間不是事件時間**。
2. 紀錄第 4 條寫「feed 帶 1,194 筆 item、channel lastBuildDate 為
   `Wed, 16 Sep 2026 14:30:47 GMT`，所以是活的」。**兩個數字兩小時後就變了**：
   查核者數到 **1,196 筆**、lastBuildDate `Wed, 16 Sep 2026 16:30:51 GMT`。
   這是活文件的診斷值、不是事實，**不准入稿也不該寫成紀錄裡的事實**。
   第 4 條其餘部分逐字確認：pubDate `Fri, 11 Sep 2026 10:00:00 GMT`、category `Engineering`、標題與 link。
3. `sources[0]` = `https://openai.com/index/scaling-storage-one-billion-users-part-one/`
   帶著 `checked_on: 2026-09-16`，但查核者在每一種寫法下都拿到 **HTTP 403**
   （9,869 bytes，帶 `<meta http-equiv="refresh" content="360">` 的 OpenAI 邊緣挑戰頁）。
   **沒有人在 2026-09-16 讀過它**，而實際證據在不在 `sources[]` 裡的 `web.archive.org`。
   把一個抓不到的頁面列成第一條來源，等於偽造證據鏈（詳見 `source_list_fix`）。
4. `sourcing_notes` 寫 `openai.com/sitemap.xml/engineering/`「listing the 22 engineering posts」。
   **是 22 個 `<url>`，但其中兩個是列表頁**（`https://openai.com/news/` 與
   `https://openai.com/news/engineering/`），**實際是 20 篇文章**。
   紀錄第 15 條寫的是「lists 22 URLs」、那個說法正確；
   **錯的是 `sourcing_notes`，而撰稿者最容易掃到的就是 notes**。改掉 notes。
5. 紀錄第 30 條在引號內寫 `'Each client team is responsible for scaling their own Rockset instance.'`
   **句子被截斷、還自己補了句號**。原文是
   `Each client team is responsible for scaling their own Rockset instance for their complex querying needs.`
   （`verbatim_quote` 欄位是完整的，錯在撰稿者會照抄的敘述文字。）
6. 紀錄第 26 條把 `There are no unbounded queries that can overload Habitat.` 當成完整句引用。
   **原文沒有句點、後面還有一半**：
   `There are no unbounded queries that can overload Habitat and complex joins and graph traversals
   require product teams to do some of the heavy-lifting which helps overall optimize for more efficient designs.`
   中間插一個句號，會把一個有但書的子句變成對 OpenAI 系統的絕對斷言。**照原文寫完整句。**
7. 紀錄第 33 條把 Figure 01 的 Habitat 功能拆成**八項**、結尾是
   `…rate limiting (request shaping), routing, and schema lookup (data residency)`。
   標記其實是嚴格的 label|sublabel 序列：Caching|Caches、ACL policies|Authorization、
   Placement & data residency|Data residency、Encryption|Data security、Isolation|Multi-tenancy、
   Rate limiting|Request shaping、Routing|`Schema lookup · Data residency`。
   一致地讀就是**七項**，`Schema lookup · Data residency` 是 Routing 的副標，
   不是一個 routing 沒副標、schema lookup 獨立成項的八項清單。
   **改寫成七項**，或明說這是一種讀法而非官方分類。
8. 紀錄第 15 條說 sitemap 的 lastmod 是「OpenAI 在 2026-09-11 發布日之後
   **唯一**公布的時間戳」。**「唯一」無法成立**：頁面本身線上讀不到，而 OpenAI 在多個表面發布
   （@OpenAIDevs 那串帶 2026-09-11T20:00:41Z，頁面自己的「Keep reading」區塊也印了其他文章的日期）。
   lastmod 值 `2026-09-12T02:19:32.976Z` 本身確認無誤，**把「唯一」拿掉**。
9. 紀錄第 13 條（`In a future post, we'll go into detail about…`）標成 `is_vendor_claim=false`。
   那是 OpenAI 對未來出版的承諾，**是廠商說法**，應標 `true`，逼撰稿寫成「OpenAI 表示」——
   紀錄自己的 `must_not_write` 第 9 條已經預設了這件事。

### must_add

- **第二個被承諾的後續文章，紀錄完全沒記**：Rust 段落之後緊接著寫
  `We plan to share more learnings in a future blog.`
  這是關於 **Rust 遷移** 的後續，與「part II」（講儲存層）是兩件事。
  `not_said` 第 10 條只寫了 part two 沒有日期，**沒有涵蓋這一條**。兩者都沒有日期。
- **唯一把「by the middle of 2025」與「In Q2 2026」串起來的時間長度**：
  `Deferring a Python rewrite for a year allowed us to focus on more urgent and impactful challenges
  during our hypergrowth.` 要做時間線的小節會需要它。
- **X 那串的真實時間戳**（見 must_fix 1）：2026-09-11T20:00:41Z / 20:00:44Z / 20:00:47Z。
- **紀錄第 22 條漏掉了官方點名的成因**：
  `Asyncio helps Python execute I/O-bound workloads concurrently, but does not help work around the
  Python GIL and provide CPU parallelism.` GIL 是整個 asyncio 抖動段落的機制，漏掉它這條就只剩現象。
- **應該補進 `not_said`**：Figure 03 的座標軸標的是
  `Illustrative time 0.0 / 40 illustrative units`，圖說也自陳是示意。
  也就是**官方完全沒有公布任何實測延遲圖**；全頁僅有的延遲數字是抖動範圍
  `hundreds of milliseconds ... in some edge cases several seconds`，
  以及沒有數字的 `significantly lower average and tail latencies`。
- **支撐研究者日期判斷的一段內部證據**：頁面自己的「Keep reading」區塊把另外三篇工程文章
  標為 Aug 25 2026、Aug 3 2026、Jul 29 2026，而 engineering sitemap 給那三個網址的 lastmod
  卻是 2026-09-15 與 2026-09-16。**同一批來源裡就證明了 sitemap lastmod 是建置時間戳、不是發布日**，
  日後有人質疑為何不用 2026-09-12 當事件日時可以拿出來。
- **三條外連經查核者確認為真實 href，不必再爭**：
  `https://engineering.fb.com/2014/11/14/production-engineering/solving-the-mystery-of-link-imbalance-a-metastable-failure-state-at-scale/`（metastable failure，紀錄第 24 條）、
  `https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf`（TAO，第 26 條）、
  `https://openai.com/careers/software-engineer-habitat-(online-data)-seattle/`（徵才頁，第 35 條；
  該頁本身在本容器 403，**可以描述其存在，但不可列為 source**）。
- **查核者自己數過、可以放心寫的負面結論**：`22M` 在正文出現 **0 次**（只在 meta 與 JSON 裡有 9 次原始 HTML 命中），
  `22 million` 0 次；`durability`、`backup`、`replica`、`SLA`、`uptime`、`restore`、`disaster recovery`
  各 0 次；`Nanobase` 只在圖裡出現 1 次。
  Rust 那句裡的 `GPT‑5.5` 確認是 **U+2011**（0x2011），與頁尾導覽列 `GPT-5.5` 的一般連字號不同——
  **那句必須整段複製，不能自己重打**。
  另外 OpenAI 頁面自己的 `og:image:alt` 與 `twitter:image:alt` 都寫 `nearly 1 billion`、
  而 `og:title` 寫 `over 1 billion`，所以第 37 條的矛盾在文章頁上就成立，不只在 X 的卡片上。

### live_data_warnings

- **feed 筆數與 lastBuildDate**：紀錄 1,194／14:30:47 GMT，兩小時後 1,196／16:30:51 GMT。不入稿。
- **engineering sitemap 的 22 個 `<url>`（其中 20 篇文章）與各篇 lastmod** 都是活值；
  `2026-09-12T02:19:32.976Z` 只是查核當下的值，且它是建置時間戳，不是發布日或更新日。
- **「part two 尚未發布」是查核當天的狀態**：靠的是 sitemap 沒有 part-two 條目、feed 沒有對應 item，
  兩者都會變。寫成「截至 2026 年 9 月 16 日尚未發布」，不可寫成「官方確認沒有」。
- **封存本身也是快照**：`web/20260914185323` 是查核當天 Archive 持有的最新一份
  （`/web/20260916235959/…` 會 302 回它），552,850 bytes。這個「最新」會變。
- 所有 `70M+ requests per second`、`1B+ people each week`、`500 PB+ data`、
  `almost 40 geographic regions`、`10x year-over-year`、`6x/15x/95%`、`Q2 2026 / 2 engineers`
  都是 OpenAI 自陳、沒有方法學、沒有第三方驗證的營運數字，一律寫「OpenAI 在工程部落格表示」。
- feed 的 `<link>` 是**不帶尾斜線**的 `https://openai.com/index/scaling-storage-one-billion-users-part-one`，
  `sources[0]` 帶尾斜線。兩者都 403，不影響內容，但內容包若要寫 canonical 網址應與 feed 一致。

### source_list_fix

**不能照現況出刊。**

1. `sources[0]` 是 403、從未讀到的頁面，卻帶著 `checked_on: 2026-09-16`（見 must_fix 3）。
2. **37 條事實裡有 31 條只掛 `web.archive.org`**（第 1、2、3、6–13、16–35 條），
   而該網址不在 `sources[]`。查核者獨立確認本容器沒有任何一手路徑可讀到正文
   （語系路徑、無尾斜線、`/news/engineering/`、它的 `rss.xml`、`.json` 路徑、徵才網址全部 403；
   只有 `robots.txt`、`sitemap.xml`、`sitemap.xml/<section>/`、`news/rss.xml` 通得過，
   而 feed 完全沒有 `content:encoded`）。所以缺口是真的，不是研究失誤。
   **編輯必須二選一**：(a) 裁定官方頁的逐字封存可採，並把 `web.archive.org` 那條網址
   連同它自己的 `checked_on` 加進 `sources[]`；或 (b) 退回研究者自己寫的殘量——
   只剩 RSS ＋ sitemap ＋ @OpenAIDevs 撐得住的部分（Habitat 的名字與角色、`10x year over year`、
   Rust 改寫前 Python 尖峰 `more than 20 million requests per second`、
   asyncio 與連線池的框架、發布日、part two 尚未發布）。
   **`sourcing_verdict: "full"` 兩種情況下都不成立，要改。**
   （封存本身查核者驗過是忠實的：552,850 bytes、og/twitter meta 相符、
   23 條取自封存的逐字引文全部逐字元吻合。）
3. `sources[3]` = `https://x.com/OpenAIDevs/status/2098502006935814272` 是 OpenAI 官方開發者帳號的原文，
   查核者確認 200 且伺服器端渲染、三則貼文逐字可見。留不留由編輯判斷，但**要意識到它是社群平台網址**，
   不是廠商官網頁面。

---
## ai-news-frontier-governance-20260528

OpenAI 2026-05-28 公布的 22 頁 Frontier Governance Framework（FGF）。
研究紀錄 58 條事實，查核確認 48 條。**查核檔的「FACT n」是 0-based**（FACT 35 ＝紀錄第 36 條）。

### must_fix

1. 紀錄第 36 條把 SB 53 第 22757.11(c) 條的「catastrophic risk」定義寫成
   「a frontier developer's development, storage, use or deployment of **a foundation model**」。
   **法條寫的是 `frontier model`，不是 `foundation model`。** 原文逐字：
   `a foreseeable and material risk that a frontier developer's development, storage, use, or
   deployment of a frontier model will materially contribute to the death of, or serious injury to,
   more than 50 people or more than one billion dollars ($1,000,000,000) in damage to, or loss of,
   property arising from a single incident`。
   同一條裡 `foundation model`（22757.11(f)）與 `frontier model`（22757.11(i)）是兩個分開的定義用語：
   frontier model 是訓練算力超過 10^26 次運算的 foundation model。
   **寫成 foundation model 會把法定門檻擴大到所有模型，等於寫錯了「誰被管到」。**
2. 紀錄第 12 條結尾寫「>50 fatalities 與 $1 billion **是整份文件裡僅有的兩個數量**」，
   對應的 `not_said` 第 4 條還寫「除了 50 人、10 億美元、六個月、12 個月、30 天以外，裡面沒有數字」。
   **兩句都被推翻。** 查核者自己抽文字，FGF 22 頁裡還有：
   CBRN Tier 2 的基準年 `relative to unlimited access to baseline of tools available in **2021**`（第 10 頁）、
   `we plan to release a more capable model in less than a month`（第 18 頁）、
   `ISO 42001`（第 4 頁）、`ISO 27001, 27017, 27018, and 27701` 與 `SOC 2 Type II`（第 16 頁）、
   `Regulation (EU) 2024/1689`（第 3 頁）、`27/7/365 incident response capabilities`（第 17 頁）、
   `Appendix 2.2 of the Code of Practice`（第 18 頁）、`Appendix B of the PF`（第 20 頁）。
   定義本身的引文正確，**錯的是那句全稱**，而且它很危險：`not_said` 那個版本會讓撰稿者以為
   **2021 這個基準年不存在**。兩處都要刪掉全稱說法。
3. 紀錄第 51 條寫「Measure 7.6 requires signatories to provide the AI Office with an updated
   Model Report at least every six months」，`verbatim_quote` 是
   `Signatories will provide the AI Office with an updated Model Report at least every six months.`
   **那是句中片段，把管住它的條件切掉了。** Measure 7.6 實際是：
   `Further, if the model is amongst their respective most capable models available on the market,
   Signatories will provide the AI Office with an updated Model Report at least every six months.`
   照現在的寫法會變成「簽署方的每一個模型都要每半年報一次」，而準則只針對**其市場上最強的模型**，
   後面還緊接著三個排除條款。**改寫成加上「若該模型屬於簽署方在市場上最強的模型」這個條件。**
4. 紀錄第 27 條把 OpenAI 的 Model Report 更新頻率寫成單一規則（「最強的前沿模型每六個月決定是否更新」）
   加三個例外。六個月那句引得對，**但界定整節範圍的前一句被省略了**。FGF 第 18 頁開頭是：
   `For models in scope of this Framework that are subject to the EU AI Act, if we have reasonable
   grounds to believe that the basis for considering the model's systemic risks acceptable has been
   materially undermined, we will update our Model Report as appropriate after completing a systemic
   risk assessment.`
   **這套更新機制是寫成歐盟 AI 法的義務，不是 OpenAI 的全球作法。** 要把這個範圍寫出來。
5. 紀錄第 13 條寫 FGF 的風險評估「incorporates feedback from academic researchers, independent domain
   experts, industry bodies such as the Frontier Model Forum, and the U.S. government, the European
   Commission and other government agencies」。引的字在第 5 頁，**但限定詞被拿掉了**。完整句是
   `This process draws on our own internal research and signals, and, **where appropriate**, incorporates
   feedback from…`。`where appropriate` 把承諾變成裁量，而研究紀錄自己的第 28 條
   （`We may solicit...`）靠的正是這個區別。**把「必要時」補回去。**
6. 紀錄第 18 條把網路攻擊風險分級形容成「three tiers, **described not numerically scored**」。
   **那是研究者的詮釋，而且文件對自己的說法幾乎相反**：
   `we have established a tier system that seeks to quantify model capabilities against cybersecurity
   threats and incorporates risk estimates and other suitable metrics. We use these measurable thresholds
   for decision-making`（第 9 頁）。
   **可查核的說法是**：FGF 沒有公布任何分級的數字、分數或切分點——不是「文件說這些分級不量化」。
7. 紀錄第 32 條寫「California SB 53 (Wiener) became **Chapter 138 of the Statutes of 2025**」，
   url 掛 leginfo 的法案條文頁。**那一頁只印了 `CHAPTER 138`，沒有 `of the Statutes of 2025`。**
   主張為真（查核者在另一個官方頁證實：BPC 第 25.1 章的法典頁印
   `Chapter 25.1 added by Stats. 2025, Ch. 138, Sec. 2.`），**但照現在的網址追不到**。
   改掛法典頁，或把那半句拿掉。
8. 紀錄第 38 條結尾寫 SB 53 第 22757.12(b) 條「is the statutory source of the 30-day changelog
   commitment in OpenAI's FGF」。條文與 30 天都確認無誤，**但這個因果是推論**：
   FGF 沒有引用任何條號，法條也從未提到 OpenAI；兩者也不是乾淨對應——
   法條要求在重大修改後 30 天內公布修改後的框架**與理由**，FGF 承諾的是
   `changes and justifications for material updates documented in a changelog and published within
   30 days of the update`。**改寫成「法條裡有同樣的 30 天期限」，不要寫成 FGF 的條文出處。**
9. 紀錄第 53 條說 Preparedness Framework v2「remains the version the FGF refers to as of 2026-09-16」。
   **FGF 從未指名 PF 的版本、沒給日期、也沒連 PDF**，只寫 `our existing Preparedness Framework (PF)`
   與 `Appendix B of the PF`。blob 的 last-modified 只能證明**那一個檔案**沒有被原地覆寫，
   不能證明別的網址沒有 v3。
   **更好的佐證（研究者沒用）**：`openai.com/news/rss.xml` 有一則〈Our updated Preparedness Framework〉，
   pubDate `Tue, 15 Apr 2025`，而 1,195 筆裡之後沒有任何 Preparedness Framework 的項目。
10. 紀錄第 8 條寫 FGF「is designed to meet the baseline legal requirements of **two regimes at once**」。
    文件寫的是 `Our FGF is designed to meet the baseline legal requirements of **various** frontier AI
    laws, **including**:` 然後列出兩個。`including` 是開放式的，**FGF 沒有說只有兩部法**。
    兩個項目的引文本身逐字正確。**改寫成「包括以下兩部」。**
11. 紀錄的 `unverified_or_excluded` 第 2 條把「TFAIA／SB 53 於 2026 年 1 月 1 日生效」排除掉，
    理由是沒有官方頁寫生效日，並指示撰稿「寫『法條沒有印出一般生效日』或乾脆不寫日期」。
    **這是錯的，而且壓掉了一個查得到的一手事實。** 研究者停在法案條文頁、沒有打開法典頁。
    `https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=BPC&division=8.&title=&part=&chapter=25.1.&article=`
    回 HTTP 200，在 22757.10 到 22757.16 這七條的每一條底下都印著
    `(Added by Stats. 2025, Ch. 138, Sec. 2.   (SB 53)   **Effective January 1, 2026.**)`。
    **改寫成**：TFAIA 自 2026 年 1 月 1 日生效，OpenAI 在其生效約五個月後（2026-05-28）公布 FGF；
    這也正是 FGF 那句沒有定義的 `the Effective Dates of the TFAIA and the EU Code of Practice`
    在加州這一側所指的日子。
12. `sourcing_notes` 與 `corrections_to_candidate_list` 裡的 feed 數字——
    「1,194 筆 `<item>`」「lastBuildDate Wed, 16 Sep 2026 14:30:47 GMT」「408 筆 2026 年」
    「最新一筆是 Reimagining advertising with AI」——**同一天稍晚就全部過期**：
    查核者在 16:03 UTC 數到 1,195 筆、lastBuildDate `15:30:49 GMT`、409 筆 2026 年、
    最新一筆是〈Helping older adults use AI in everyday life〉（16:00Z）。**一個都不要寫進文章。**
13. **事件日的追溯性有缺口**：`event_date` 2026-05-28 只靠 `openai.com/news/rss.xml` 的 pubDate，
    而那個網址**不在 `sources[]` 裡**。PDF 本身沒有日期（`not_said` 第 1 條已正確指出）、
    blob 標頭是 2026-05-27、sitemap 是 2026-06-04。也就是**沒有任何一條列出的來源支撐頭條日期**，
    違反 BRIEF「每一個日期都要能指到一條 source 的原文」。
    feed 項目本身是真的（查核者重抓，逐字為
    `<title><![CDATA[OpenAI's Frontier Governance Framework]]></title> ... <category><![CDATA[Safety]]></category> <pubDate>Thu, 28 May 2026 00:00:00 GMT</pubDate>`），
    **所以正確的修法是把 feed（或那個 canonical 的 /index/ 頁）放進 sources，不是改日期。**

### must_add

- **TFAIA 的生效日 2026 年 1 月 1 日**（見 must_fix 11）。除了日期本身，法典頁還有一件事值得記：
  七條沒有任何一條標 `Amended by`，代表研究者讀的那份條文到 2026-09-16 仍是現行法——
  法案條文頁只是 2025-09-29 的快照，**證明不了現行法**。這一頁應該取代或加入 `sources[]`。
- **FGF 的風險分級文字大量沿用 Preparedness Framework，這與研究紀錄「兩份文件不同」的框架相反。**
  查核者逐字比對兩份 PDF：FGF 的 CBRN Tier 2
  （`The model can provide meaningful counterfactual assistance (relative to unlimited access to
  baseline of tools available in 2021) to novice actors (anyone with a basic relevant technical
  background) that enables them to create known biological or chemical threats`）
  與 PF 的 Biological and Chemical [High] 門檻**逐字相同**，只差 `novice` 外面的引號；
  FGF CBRN Tier 3 與 PF 的 [Critical] 門檻逐字相同；
  FGF Cyber Tier 3 與 PF Cybersecurity [Critical] 只差 `OR the model can devise` vs `OR model can devise`、
  `high-level` vs `high level`；FGF Cyber Tier 2 是 PF 的 [High] 門檻前面加
  `provides substantial capability uplift to small organizations by`。
  FGF 關於優先做生物評測的敘述也幾乎照抄 PF 的註 5。
  這是兩份一手文件的可觀察文字事實，不是對意圖的推測，也不牴觸研究者「兩份文件都沒說對應關係」
  的正確警告（`unverified_or_excluded` 第 7 條維持）。
  **編輯上的意義**：FGF 真正新的是 Tier 1（比 PF 的 High 更低的一級）與法遵框架，不是最上面兩級門檻。
- **紀錄第 54 條漏掉的中間一句，會讓整篇的核心對比失衡。** PF 的註腳不只寫「數千人／數千億美元」：
  `By "severe harm" in this document, we mean the death or grave injury of thousands of people or
  hundreds of billions of dollars of economic damage. **Our safety stack addresses a broad spectrum of
  risks, including many with harms below this severity.** In choosing to set a high bar here, we aim to
  ensure that the most severe risks receive attention commensurate with their magnitude.`
  研究紀錄記了第一句與第三句、漏了第二句——正是阻止讀者以為「OpenAI 不管數千人以下的風險」那一句。
- **SB 53 第 22757.11(c)(2) 條有三項排除，完全沒記**，而文章第二節正建立在那個定義上：
  (A) 模型輸出的資訊若 `otherwise publicly accessible in a substantially similar form from a source
  other than a foundation model`；(B) `Lawful activity of the federal government`；
  (C) 前沿模型與其他軟體合併造成的損害，`if the frontier model did not materially contribute to the harm`。
- **SB 53 第 22757.16 條**：`The loss of value of equity does not count as damage to or loss of property
  for the purposes of this chapter.` 這一條直接界定了文章會引用的那個 10 億美元。
- **SB 53 第 22757.13(h)-(j) 是聯邦等效的安全港**：加州緊急事務辦公室可以用規則指定某些聯邦法規或指引，
  其事故通報標準 `substantially equivalent to, or stricter than` 州規；
  聲明要以該方式遵循的開發者即 `deemed in compliance with this section`，
  而未達該聯邦標準 `shall constitute a violation of this chapter`。
  再加上第 5(d) 條（與聯邦政府契約嚴重衝突時不適用）與第 5(e) 條（聯邦法先占時不適用），
  這些**實質限縮了紀錄第 45 條「加州法讓 OpenAI 自己寫的話變成可罰」的框架**。
- **SB 53 第 22757.14(d) 條**：`Beginning January 1, 2027, and annually thereafter, the Attorney General
  shall produce a report with anonymized and aggregated information about reports from covered employees.`
  紀錄第 43 條記了 OES 的事故報告、第 44 條記了科技署的檢討，**漏了這第三份年度報告**。
- **歐盟安全與資安章 Measure 10.2 的排除條款沒記**：
  `For Frameworks, such publication is not necessary if all of the Signatory's models are similarly safe
  or safer models pursuant to Appendix 2.2. For Model Reports, such publication is not necessary if the
  model is a similarly safe or safer model pursuant to Appendix 2.2.`
  這正是整條為什麼是有條件的（`If and insofar as necessary`），也解釋了 FGF 為何在自己的六個月例外清單裡
  交叉引用 `Appendix 2.2 of the Code of Practice`。
- **值得補進 `not_said` 的一項觀察**：歐盟章 Measure 1.1 要求框架必須針對每一種有分級的系統性風險，
  載明 `estimates of timelines when Signatories reasonably foresee that they will have a model that
  exceeds the highest systemic risk tier already reached by any of their existing models`，
  並附理由、假設與不確定性。**OpenAI 公布的 FGF 沒有任何這種時程估計，也沒說任何模型目前落在哪一級。**
  這不等於不遵循（Measure 10.2 只要求公布「經刪節的摘要版」），
  但「公開文件不會告訴你 OpenAI 認為自己的模型在哪一級」是可查核的缺口，比研究者那條籠統的 `not_said` 更利。
- **`27/7/365` 確認真的印在 FGF 第 17 頁**（查核者重抽）。研究者的處理——記進
  `unverified_or_excluded`、不引用、也不自行改成 24/7——是對的，**維持不動**。
- **識別碼來源經查核者驗過，不必再懷疑**：歐盟文件編號 118119 不是猜的，
  解析 GPAI 政策頁的錨點，它精確對應連結文字 `Safety and Security chapter (PDF)`
  （同組還有 118120 Transparency、118115 Copyright、118118 Model Documentation Form、
  118312 Signatory Form、124170 Vademecum）；leginfo 的 `bill_id 202520260SB53` 解析到正確文件
  並由法典頁佐證；cdn.openai.com 的 PDF UUID 無法用樣式猜出、且回傳真實的 22 頁文件。

### live_data_warnings

- **OpenAI feed 的所有計數**（1,194／1,195 筆、408／409 筆 2026 年、lastBuildDate、最新項目標題）——
  同一天就漂移。**永遠不寫。**
- **`openai.com/sitemap.xml/safety/` 的 165 個 `<loc>` 與 FGF 頁的 lastmod `2026-06-04T08:13:28.790Z`
  （68 個 hreflang 替代）** 都是活值。可以說「頁面在發布後被動過」，
  但**不能說內容被改寫**——那一頁在本容器 403，改了什麼沒人看過（`not_said` 第 14 條維持）。
- **PDF blob 標頭是活值**：FGF `Wed, 27 May 2026 16:04:12 GMT`、6,136,955 bytes、md5
  `efeae18be97ece7b1a71e7afcf2019d6`；PF v2 `Mon, 09 Jun 2025 21:27:02 GMT`、170,399 bytes。
  可以拿來說「這個檔案自那時起沒被覆寫」，**不能拿來說「沒有更新版存在」**（見 must_fix 9）。
- **歐盟簽署方名單是會長的清單**：紀錄第 49 條列了 OpenAI 與另外 20 個名字，
  而該頁自己就寫 `Some signatories may not appear immediately`。
  **不要寫簽署方總數**，也不要把「某家不在名單上」寫成拒簽。
- **各頁的「Last update」字串是活的**：GPAI 政策頁 `31 July 2026`、
  執委會新聞稿 `Publication 31 July 2026`、法案頁 `Version: 09/29/25 - Chaptered`。
  引用時要寫成查核當天讀到的狀態。
- FGF PDF 本身**沒有版本號、沒有日期、沒有 changelog**，
  所以「這是發布當時的版本」只能靠 blob 時間戳推斷，寫的時候要留餘地。

### source_list_fix

4 條，在上限內，四條全部可達且是宣稱的那份文件（查核者逐一驗過 PDF 頁數、md5、
法案頁的 `CHAPTER 138`、GPAI 頁標題）。**但有兩個問題必須處理：**

1. **事件日沒有來源撐**：`event_date` 2026-05-28 只由 `openai.com/news/rss.xml` 支撐，
   而它不在 `sources[]`（見 must_fix 13）。**要把 feed 或 canonical 文章頁放進 sources。**
2. **58 條事實裡有 7 條掛在 sources 以外的網址**：
   第 1、2、58 條 → `https://openai.com/news/rss.xml`；
   第 3 條 → `https://openai.com/sitemap.xml/safety/`；
   第 50、51 條 → `https://ec.europa.eu/newsroom/dae/redirection/document/118119`（歐盟安全與資安章 PDF）；
   第 52 條 → 執委會 2026-08-02 執法新聞稿。
   第 50、51 條是歐盟那一側的核心條文（Commitment 1、Measure 7.6、10.1、10.2），
   **要用就得把那份 PDF 換進四條裡**。
3. **建議加入的官方頁**：加州法典頁
   `https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=BPC&division=8.&title=&part=&chapter=25.1.&article=`
   （HTTP 200），它同時給了生效日與「這仍是現行法」的證據，比法案條文頁強。
4. 沒有任何事實追到新聞媒體、整合站、律師事務所部落格或搜尋摘要；
   媒體線索（enterprisedna.co、startuphub.ai、ciodive.com、techtimes.com 等）都正確隔離在
   `unverified_or_excluded` 裡，維持。
5. **注意分工**：紀錄第 52 條（執委會 2026-08-02 開始執法）就是既有文章
   `ai-news-eu-transparency-20260802` 的同一則新聞稿。
   **最多用一句話當日期脈絡**，超過就是重寫既有文章，`ai.md` 禁止。

---
## ai-news-gemini-38-live-20260915

Google 2026-09-15 發表 Gemini 3.8 Live 與 3.8 Live Extended Thinking。
研究紀錄 48 條事實，查核確認 47 條。**本篇查核檔用 1-based 編號，與研究紀錄位置一致。**
四條 sources 全部可達、都是宣稱的那份文件，這是本垂直來源狀況最乾淨的一篇。

### must_fix

1. `editorial_brief` 與 `corrections_to_candidate_list` 第 4 條寫「兩篇貼文互相連結（the two posts
   cross-link each other）」，用來支撐「合併成一篇」的決定。**只有單向。**
   開發者那篇第一句把 `new Gemini Live models` 連到模型那篇；**模型那篇沒有任何連到開發者那篇的連結**
   （查核者搜該篇 HTML 找不到開發者那篇的 slug，並列舉了模型那篇內文所有 href，
   只有 `ai.google.dev/gemini-api/docs/live-api`、`cloud.google.com/gemini-enterprise-cx`、
   model card、`deepmind.google/models/synthid/` 與六個夥伴文件站）。
   **一篇文章的決定仍然成立，但理由要改成「兩篇的 RSS pubDate 完全相同」**
   （查核者確認都是 `Tue, 15 Sep 2026 17:00:00 +0000`），不是互相連結。
2. `not_said` 第 12 條寫「Live API 的 thinking 指南把從 `gemini-3.1-flash-live-preview`
   升級描述成**選用的**遷移（optional migration）」。**那一頁從來沒說 optional。**
   它的小節標題是 `Migration and integration paths` → `Upgrading from Gemini 3.1 Flash Live`，
   並給出具體升級步驟；全頁搜 `optional` 與 `deprecat` 只命中側邊欄的導覽項目 `Deprecations`。
   底層論點（定價頁、Live API 頁與 thinking 指南都沒有 `gemini-3.1-flash-live-preview` 的汰換公告）
   是對的，**「選用」這個形容是編出來的，刪掉**。
3. `must_not_write` 第 6 條寫「不要說 Gemini 3.8 Live 在 Gemini app 裡。Google 的發表文把
   3.8 Live 放在 Search Live、Extended Thinking 放在 Gemini Live」。
   **這條指示叫撰稿者壓掉一個一手陳述。** Google 自己從發表文連出去的 DeepMind model card 寫：
   `Gemini 3.8 Live is distributed in the following channels: Gemini API, Gemini App, Google AI Studio,
   Google Cloud / Vertex AI, Google Search Live.`
   發表文自己的內文也寫兩個模型讓使用者對 Gemini 說話
   `across the Gemini app, Google Workspace, and Search` 更流暢（研究紀錄第 21 條就是這句）。
   這條指示還與研究紀錄自己的 `unverified_or_excluded` 第 3 條衝突——那一條正確地寫
   `Flag the discrepancy rather than resolving it`。
   **改寫成**：照部落格的消費者分工寫（3.8 Live ＝ Search Live、Extended Thinking ＝ Gemini Live），
   **同時寫明 Google 的 model card 列出更廣的通路，包含 Gemini app 與 Vertex AI**，兩邊不一致就直說。
4. 紀錄第 8 條寫 Google 把兩個模型定位為 `our most advanced live dialogue models yet`，
   並註明出處是「meta description **與標題下的引言（standfirst）**」，引文結尾是
   `built for natural conversation.`。**那整句只存在於 `<meta name=description>` 與 `og:description`。**
   頁面上看得見的引言是
   `...are our most advanced live dialogue models yet. Major upgrades in intelligence and parallel
   reasoning make them more intuitive to collaborate with and use to execute complex tasks using your voice.`
   `built for natural conversation` 在正文裡完全不存在。
   **改寫成**：只寫 meta description，並把引言那句另外引述。
5. `event_date_basis` 把「Gemini API 定價頁頁尾的 `Last updated 2026-09-15 UTC`」列為第四個佐證。
   **那是全站文件的建置戳，不是事件日。** 查核者在
   `ai.google.dev/gemini-api/docs/live-api` 上找到一模一樣的字串，而那一頁從頭到尾沒提 `gemini-3.8-live`。
   **把第四個佐證刪掉**；前三個（兩篇的 `article:published_time`、兩篇相同的 RSS pubDate、
   model card 的 `Published 15 September 2026`）已經足夠。
6. `corrections_to_candidate_list` 第 3 條把「Google 自己的 Live API 總覽文件**仍然寫**
   `Converse in 70 supported languages`」當成對 97 這個數字的反證。
   **兩個觀察都屬實（查核者重現：那句在、`97` 不在），但推論不成立**：
   那一頁是平台層的功能清單，從未點名 `gemini-3.8-live` 或任何模型，而且它自己的頁尾也寫
   `Last updated 2026-09-15 UTC`。
   **改寫成**：三個數字來自 Google 的三個頁面（發表文 97、開發者文 97+、
   查核當天 Live API 總覽頁 70），並列陳述；**不可讓文章暗示 Google 的文件否定了 97**。

### must_add

- **一份被漏掉的一手評測文件，而且它替所有評測數字加上限定條件。**
  model card 的 Evaluation 區把「Evals & Methodology for 3.8 Live Extended Thinking」連到
  `https://deepmind.google/models/evals-methodology/gemini-3-8-live`，轉址（HTTP 200）到
  `https://storage.googleapis.com/deepmind-media/gemini/gemini_3-8_live_model_evaluation.pdf`，
  是一份 5 頁的 Google DeepMind PDF，標題〈Gemini 3.8 Audio (Live, Live Extended Thinking) Model evaluation〉。
  研究者從未抓過。裡面寫明：
  `All Gemini scores are pass@1 except where otherwise noted`；
  `ServiceNow's EVA-Bench results were run by ServiceNow with the Gemini Enterprise Agent Platform
  (thinking minimal and high)`；
  `Artificial Analysis (run by AA) and tau-Bench results were run with the Gemini API for the model-ids
  gemini-3.8-live-preview and gemini-3.8-live-extended-thinking with thinking high and default sampling settings`；
  結果 `as of September 2026`。
- **同一份 PDF 用的模型代號是 `gemini-3.8-live-preview`，與定價頁印的 `gemini-3.8-live` 不同。**
  Google 自己的兩份文件對同一個模型用了兩個代號。
  **文章若要印代號，用定價頁那個**，而且不可把評測分數寫成是在正式版模型上量到的，除非附上這個但書。
- **PDF 裡的分數圖是圖片**：82.6、68.6%、35.1%、97.7% 在 PDF 裡抽不出文字。
  這四個數字只追得到部落格，**所以 `must_not_write` 第 3 條的「Google 表示」不是文體偏好，是必要條件**。
- **Google 自己對 Sierra 那個基準用了兩種名字**：部落格原始標記是
  `68.6% on <i>tau</i>-Voice and 35.1% on Sierra's <i>tau</i>-Voice-banking benchmark`，
  評測 PDF 叫它 `Sierra tau-cubed-Bench (tau-cubed-Banking)`。
  **逐字引部落格的寫法，不要合併、不要自己「訂正」。**
- **兩段圖說帶著 Google 的官方介面名稱，而 `verified_facts` 裡完全沒有**，
  可用性表格應該照它們寫：
  `Try Gemini 3.8 Live Extended Thinking in Google Workspace with Docs Live, Gmail Live, and Keep Live.`
  與 `Get step-by-step, real-time troubleshooting help powered by Gemini 3.8 Live - right inside Search Live.`
  這是 Google 唯一點名 Docs Live／Gmail Live／Keep Live 的地方，也獨立佐證了兩個模型的分工。
- **一個較鬆的第三種表面說法，紀錄沒有**：小節標題
  `Across Google Workspace and Search, our Live models deliver more intuitive, collaborative experiences
  - especially when tackling your most complex tasks`。
- **model card 把 `Google Cloud / Vertex AI` 列為兩個模型的通路，而部落格的可用性清單完全沒提 Vertex AI。**
  這被記在第 22 條裡，**卻從建議的 4×5 可用性表與 2×2 圖解裡掉了**——圖解的企業節點只寫
  「Gemini Enterprise 私人預覽」。**企業面的完整圖像是 Gemini Enterprise 私人預覽＋Vertex AI。**
- **Gemini 3.5 Transcribe 的日期有更好的一手來源**，紀錄只停在「released last month」：
  model card 的 Related stories 連到 Google 自己的發表文
  `https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/`，
  `article:published_time` 是 **2026-08-26**、`<title>` 是〈Introducing Gemini 3.5 Transcribe〉。
- **Live API thinking 指南記載了「背景執行工具」這個頭條主張背後的機制，也記載了兩個模型的硬分界**
  （研究紀錄為了 4 條上限把它排除，可以接受，但這是整篇立論的實質）：
  `thinking_level` 不支援 `gemini-3.8-live`；`gemini-3.8-live-extended-thinking` 接受
  low／medium／high，**不支援 MINIMAL**；Extended Thinking
  `Requires asynchronous (NON_BLOCKING) tool declarations`，
  呼叫端要追 `interaction_status` 而不是 `turnComplete`。
- **「官方未說明開放地區」經查核者獨立證實，必須寫進文章。**
  查核者對三個 Google 頁面全文掃 `region`、`country`、`market`、`United States`、`worldwide`、
  `globally`、`available`，命中的只有 blog.google 版面的 `Global network`、`Global (English)`、
  影片圖說裡的 `marketing toolkits`、開發者功能條列的 `Reach global audiences`，
  以及只點產品、不點地點的可用性陳述。**沒有任何地區、國家、市場或上線順序的陳述。**
- **額外的一手交叉確認**：Google Workspace Updates 的 Atom feed（HTTP 200、25 筆、最新 2026-09-16）
  在 2026-09-15 的條目是 Meet 會議室代碼、Gemini 連接器、Gmail 搜尋 AI 總覽與雲端硬碟分享，
  **沒有任何 Docs Live／Gmail Live／Keep Live 或 3.8 Live Extended Thinking**。
  這是佐證「沒有公布地區與資格範圍」，不是反證。
- **經查核者獨立確認、撰稿可以放心用的部分**：所有價格、128K／64K token 數字、
  2025 年 1 月知識截止日、免費層「Used to improve our products」Yes/No 的分野、
  以及「每月 5,000 次免費搜尋、之後每 1,000 次 14 美元」的 grounding 條件，全部逐字重現。
  兩個模型代號 `gemini-3.8-live` 與 `gemini-3.8-live-extended-thinking` 逐字印在定價頁上、不是猜的；
  model card 網址由模型那篇連出、定價網址由 Live API 文件連出，都不是猜的；
  兩個部落格網址零轉址解析到紀錄的位址。
  倉庫面的主張也都對：`ai-news-siri-ai-ios-27-20260914` 的 display_order 是 148；
  索引的 zh-TW title 仍是「2026 年 AI 新聞總整理：1 月 1 日至 9 月 14 日的重點與生活應用」；
  `ai-news-gemini-live-20260826` 確實引用
  `blog.google/innovation-and-ai/products/gemini-app/productivity-features-gemini-live/`；
  `ai-news-gemini-38-flash-20260902` 存在，適合當第二個 link。

### live_data_warnings

- **定價頁是活文件**：頁尾 `Last updated 2026-09-15 UTC` 是全站建置戳，同一個字串也出現在
  Live API 總覽頁上。每一個價格都是 2026-09-16 讀到的版本，正文要寫明查核日。
  model card 自己也寫 `Model cards may be updated from time to time`。
- **`blog.google/rss/` 只有 20 筆、最新一筆 2026-09-16 16:00 UTC**——是活性診斷值，不入稿。
- **所有排行榜名次都是快照**：`#1 overall spot on Artificial Analysis' Speech to Speech Quality Index (82.6)`、
  `second place in the Speech Agent Arena`、`68.6%`／`35.1%`／`97.7%`。
  排行榜持續變動，研究紀錄 `unverified_or_excluded` 第 9 條已正確標明，**一律寫成
  「Google 在 2026 年 9 月 15 日的公告中表示」**。
- **「97 種語言」本身是會變的平台數字**，而且 Google 自家三個頁面給了三個值（97／97+／70）。
  照 must_fix 6 並列陳述，不要挑一個寫死。
- **`rolling out starting today` 是開始、不是完成**；企業端是私人預覽。
  任何「已經開放」的寫法都要避開，`not_said` 第 5 條維持。
- Frontier Safety 的結論是從 Gemini 3.7 Flash 推論過來的，不是對這兩個模型做的評估
  （`unverified_or_excluded` 第 5 條正確），**不可寫成「通過」**。

### source_list_fix

**`sources[]` 本身可以出刊。** 4 條、全部 HTTP 200、零轉址、內容為真，
而且 **48 條事實全部追得到這四條之一**——本垂直唯一做到這件事的兩篇之一。
`sources[].checked_on` 都是正確的 2026-09-16。沒有任何事實追到新聞媒體、整合站或搜尋摘要。

唯一要注意的：若撰稿要用上面 `must_add` 裡的評測 PDF、Live API thinking 指南、
或 Gemini 3.5 Transcribe 的發表文，**那些網址都不在四條裡**，用了就得換掉其中一條。

### 額外：規格合規

- **研究紀錄缺少四個 BRIEF 規定的頂層欄位**：`checked_on`、`title`、`hero_label`、`diagram`。
  `hero_label` 與 `diagram` 目前只以散文建議的形式躺在 `editorial_brief` 裡。撰稿代理要補齊。
- `editorial_brief` 建議的 `hero_label`「語音模型升級，開放條件分開看」是 **14 個字**，
  超過 BRIEF 的「繁中 ≤ 12 字」。要改短。
- 小瑕疵（不是錯誤）：紀錄第 44 條把夥伴列成
  `Agora, Fishjam, LangChain, LiveKit, Pipecat, Vercel and Vision Agents`，
  頁面印的順序是 `Agora, Fishjam, LiveKit, LangChain, Pipecat, Vercel, and Vision Agents`——
  集合相同、順序不同，附的 `verbatim_quote` 正確。
  紀錄第 4 條沒提開發者那篇的 `<title>`（`New Gemini Audio models for developers`）與 `og:title` 不同，
  而模型那篇有記同類差異。
  紀錄第 29 條標 `is_vendor_claim=false`：數字是事實沒錯，但同一句裡的
  `Competitively priced` 與 `industry-leading performance` 是廠商修辭，紀錄裡沒有記下來。

---
## ai-news-gpt-55-instant-20260505

OpenAI 2026-05-05 的 GPT-5.5 Instant 與其系統卡。研究紀錄 40 條事實，查核確認 40 條的內容、
**一條事實都沒被推翻**。查核者的原話是：逐格重抓、每個數字、單位、日期與逐字引文都吻合，
包括刻意保留的官方錯字 `CA/DNS Hijakcing`（紀錄第 24 條）。
剩下的問題是**來源結構與遺漏**，不是捏造。**查核檔用 0-based 編號**（`#12` ＝紀錄第 13 條）。

### must_fix

1. `not_said` 第 3 條寫「官方**從未列出**支援語言，也沒有分語言的評測數字，繁體中文表現無任何官方資料」。
   **「從未列出」是錯的。** 系統卡的註 1 明確指向一份官方語言清單：
   `A list of the languages that ChatGPT currently supports can be found here.`
   連到 `https://help.openai.com/en/articles/8357869-how-to-change-your-language-setting-in-chatgpt`。
   查核者抓了那個連結：**HTTP 403**。
   **改寫成**：系統卡連到一份官方語言清單，該頁在本容器讀不到；系統卡本身沒有任何分語言的評測數字。
   （撰稿照抄「官方從未列出」會誤述來源。）
2. `unverified_or_excluded` 第 3 條排除「2026-06-09 起個人化改進開放給 Go 與免費版」的理由寫
   「官方 feed 中 2026-06-09 沒有對應項目（6 月只有 6/4 的 Dreaming 與 6/18 的 health intelligence）」。
   **這個理由是假的。** 2026 年 6 月的 feed 大約有 55 則，光 2026-06-09 就有三則：
   〈How engineers at Nextdoor use Codex to build without limits〉、
   〈What Codex unlocks for Notion〉、〈Industrial policy for the Intelligence Age〉。
   **結論（6 月沒有任何一則公告個人化開放）仍然成立，但這個理由不可再用**，
   改寫成「6 月的項目逐一看過，沒有任何一則公告個人化功能的開放對象」。
3. 紀錄第 13、26、27 條把圖檔網址
   （`.../assets/images/factuality.png`、`capture_the_flag.png`、`cve_bench.png`）
   當成事實的追溯 url，而那些網址不在 `sources[]` 裡，事實因此追不到列出的來源。
   **數字本身完全正確**——查核者自己開了三張圖、逐一讀標籤：
   Figure 2 為 25.3／17.9、7.4／4.4、61.3／46.1、25.2／15.8、36.4／19.9、10.1／4.8；
   Figure 7（pass@12）88.23／96.3／94.11；Figure 8（pass@1）86.27／93.1／90.2。
   **修法是機械性的**：把這三條的 url 改成 `https://deploymentsafety.openai.com/gpt-5-5-instant/introduction`。
   紀錄自己的 `must_not_write` 第 2 條已經這樣要求，只是 `verified_facts` 沒照做。
   **另外要知道**：這些百分比在 PDF 裡也是圖片，**PDF 的文字層抽不到**，
   所以紀錄第 32 條那句「PDF 表格數字與 HTML 版逐格核對一致」只對**表格**成立、對**圖**不成立，
   要把範圍寫清楚。
4. `sources[1]` 是 `https://openai.com/news/rss.xml`，而整包**唯一一句產品面陳述**
   （紀錄第 2 條的
   `GPT-5.5 Instant updates ChatGPT's default model with smarter, more accurate answers,
   reduced hallucinations, and improved personalization controls.`）就掛在它上面。
   BRIEF 明文：「feed 給的是日期與標題，不是內容……sources 放的是文章頁的網址，不是 feed 的網址。」
   內容本身是真的（查核者逐位元比對過，含 U+2019 撇號），feed 也確實是 OpenAI 一手，
   **但這是規格違反，而且能滿足規格的那個文章頁 403**。
   更要緊的是：**`default` 這個字在整份系統卡裡出現 0 次**（查核者 grep 過），
   所以本篇整個「預設模型」的框架只存在於這句 feed 描述裡。
   **編輯必須有意識地二選一**：明白裁量給這條例外，或放棄 feed、連帶放棄「預設模型」這個說法。
   紀錄第 11 條 `not_said` 已經正確記下這件事，撰稿不可忽略。

### must_add

- **基礎模型的但書，這是重大遺漏。** 系統卡第 3.1 節寫：
  `Our evals are run on the base model, without system-level safeguards, to ensure the model's
  underlying behavior meets our safety bar.`
  也就是撰稿要印的每一個 Table 1 數字——包括頭條的退步 gore 0.867→0.703 與
  sexual 0.857→0.806——**都是沒有系統層防護的裸模型分數**，不是使用者在 ChatGPT 裡遇到的。
  少了這句，文章會朝著 `editorial_brief` 自己要避免的方向誇大退步。
- **基準漂移的但書，同樣重大。** 第 2 節寫：
  `Note that comparison values from previously-launched models are from the latest versions of those
  models, so may vary slightly from values published at launch for those models`，第 3.1 節重複一次。
  意思是文章要印的每一個 GPT-5.3 Instant 數字（0.867、0.995、25.3%、49.6……）
  **都是重新量過的值，不是當初 GPT-5.3 Instant 系統卡上公布的數字**。任何「從 X 變成 Y」的句子都需要這個框架。
- **第二段「不代表日常出錯率」的聲明。** 研究者只記了幻覺那一段的（紀錄第 12 條）。
  第 3.1 節自己另有一段：
  `These evaluations were deliberately created to be difficult. They were built around cases in which
  our existing models were not yet giving ideal responses ... Error rates are not representative of
  average production traffic.`
  建議的 table 取自第 6 節、安全退步取自第 3.1 節，**兩段聲明都要有**。
- **分類改名，這關係到中文怎麼翻。** 第 3.1 節的註記：
  `to deduplicate overlaps between our previous "hate" and "harassment" categories, we are merging
  "harassment" and "hate" into a single evaluation. Additionally, we have renamed our previous
  "violence" category to "gore" in order to more clearly distinguish it from requests related to
  illicit violent behavior; this is a naming change, not a change in the underlying evaluation.`
  另有註腳把 gore 定義為 `graphic or gratuitously gory content ... does not include violent roleplay,
  violent ideation, or facilitation of violent activity`。
  **本篇的頭條退步就是 gore 那一列，所以必須把官方的定義寫出來**，否則中文讀者會把「血腥」讀成「暴力」。
- **生物能力的評測結果，對「更強」的框架是反向證據，平衡的稿子需要它**：
  多模態病毒學除錯（350 題 SecureBio 保留題）：`All models exceed the median domain expert baseline of 22.1%.`；
  ProtocolQA Open-Ended（108 題改寫成開放式、19 位博士基準）：
  `All models underperform the consensus expert baseline (54%).`；
  默會知識：`GPT-5.5 Instant just outperforms the consensus expert baseline of 80% when including
  refusals and safe completions, and underperforms 80% when excluding them.`；
  TroubleshootingBench（52 個實驗流程、12 位博士專家）：
  `GPT-5.5 Instant performs below the comparison models, and below the expert baseline of 36.4%.`
- **403 牆外極少數的消費者面陳述之一**，第 3.3 節結尾：
  `We've strengthened ChatGPT's ability to recognize subtle warning signs across long, high-stakes
  conversations and trained the model to respond safely in acute situations, including self-harm.`
- **「後來被取代」有更好的第二佐證，而且已經在 sources 裡**：
  API changelog 的 2026-08-06 條目寫
  `Updated the chat-latest snapshot, which points to the latest model available in ChatGPT for Plus and
  Pro users. We recommend leveraging GPT-5.6 Sol for production API usage.`
  `chat-latest` 的描述正是在那一天停止寫「latest Instant model」——這是 API 這一側對交接的一手佐證，
  獨立於 8 月那份系統卡。
- **chat-latest 的完整沿革，查核者全部確認**，正好支撐紀錄堅持的「這是會移動的指標」：
  2/24 釋出 `gpt-5.3-chat-latest`；3/16 更新；5/5 釋出 `chat-latest`；5/28 再次釋出；
  6/24 更新；8/6 改指向 Plus/Pro 的模型。紀錄第 35 條寫的「6 月 24 日」正確。
  另注意 5/28 那條寫 `the latest improvements`、5/5 那條寫 `our latest improvements`——
  研究者寫的「幾乎相同」是準確的，不是含混。
- **Figure 1（越獄）查核者看過了**：折線圖，Y 軸標 0–100% 並有誤差線，但沒有逐點數值標籤。
  GPT-5.5-Instant（紅）在**每一個攻擊預算下都低於** GPT-5.3-Instant（綠），
  並在多數預算下**高於** GPT-5.1-Instant 與 GPT-5.2-Instant。
  拒絕從圖上讀數字是對的；若撰稿想把退步放在整條 Instant 線上而不是只對前一代，這個細節可用。
- **被排除的 52.5% 算術經查核者驗算**：(10.1−4.8)/10.1 = 52.48%。
  研究者拒絕把它歸給 OpenAI 是對的（那句話不在任何可達的一手頁面上），
  **維持「寫 10.1% 降到 4.8%」的指示**。
- **候選清單的核對結果確認**：`candidates-tech-and-ai.md` 第 132 行確實寫
  `| 2026-05-05 | GPT-5.5 Instant: smarter, clearer, and more personalized | 站上只有 4/23 的 GPT-5.5，這是不同型號 |`，
  而系統卡確實寫了 `there is not a model named GPT-5.4 Instant` 與
  `we refer to GPT-5.5 as GPT-5.5 Thinking to avoid confusion with the instant model`。
  同日 10:00 GMT 還有第三則 OpenAI 項目〈Unlocking large scale AI training networks with MRC〉
  （category Engineering），與本題無關。

### live_data_warnings

- **feed 筆數與最新項目時間**：紀錄寫 1,194 筆、最新 2026-09-16 13:00 GMT；
  查核者看到 1,195 筆、最新 16:00 GMT。同一天漂移。不入稿。
- **sitemap lastmod 是活值**：公告頁 `2026-09-15T11:52:22.071Z`（同時列在 `/product/` 與 `/release/`）、
  系統卡頁 `2026-05-22T19:27:50.474Z`（列在 `/safety/` 與 `/publication/`），四個查核者都重新確認。
  68 個 hreflang 替代（含 zh-Hant、ja-JP、ko-KR）也確認。
  可以用來說「發布後被改過」，**不可當內容更新日**。
- **`chat-latest` 模型頁上的一切都是「查核當天那個指標所指的模型」**：
  400,000 上下文、128,000 最大輸出、2025-08-31 知識截止、每百萬 token 5.00／0.50／30.00 美元，
  而且該頁當天建議的正式用途模型已經換成 GPT-6 Astra。
  紀錄第 36 條與 `must_not_write` 第 3 條已經正確警告，**這條絕對不能鬆**。
- **系統卡是會被事後修訂的活文件**：紀錄第 38 條記下 8/6 那份系統卡帶有 2026-08-19 的 Change log
  （把 GPT-5.5 在 hard-negative protein binding prediction 的 pass@4 從 0.4% 更正為 1.48%）。
  GPT-5.5 Instant 那份目前沒有 Change log 區塊——**這是查核當天的狀態**。
- Deployment Safety Hub 首頁列出的 slug 清單（`chatgpt-images-2-5`、`gpt-6-astra`、
  `gpt-5-6-august-update`、`gpt-5-6`、`gpt-5-6-preview`、`gpt-live`、`gpt-rosalind-5-5`、
  `gpt-5-5-instant`）會隨新模型增加，不要寫死。
- PDF 21 頁、1,566,379 bytes、封面日期 2026-05-04、Producer `pdfTeX-1.40.27`、
  CreationDate/ModDate `D:20251217192705Z`——查核者逐一確認（`/Count = 21`）。
  **那個 metadata 時間戳是產製流程留下的，不可引用**（紀錄 `unverified_or_excluded` 第 7 條正確）。

### source_list_fix

4 條，在上限內，**全部可達、內容為真**（查核者逐一驗過：系統卡 HTML 347,613 bytes、
changelog 507,528 bytes、8 月系統卡 401,144 bytes、PDF 1,566,379 bytes、
以及八張評測 PNG 全部 200）。但有兩件事要處理：

1. **6 條事實掛在 sources 以外的網址**：
   第 13 條 → `.../assets/images/factuality.png`；
   第 26 條 → `.../capture_the_flag.png`；第 27 條 → `.../cve_bench.png`（三條改掛系統卡頁，見 must_fix 3）；
   第 32 條 → `.../gpt-5-5-instant.pdf`；
   第 36 條 → `https://developers.openai.com/api/docs/models/chat-latest`；
   第 39 條 → `https://openai.com/sitemap.xml/release/`。
   後三條要用就得換進四條裡，否則不寫。
2. **`sources[1]` 是 feed 網址**，與 BRIEF 抵觸，而且整包唯一的產品面陳述掛在它上面（見 must_fix 4）。
3. `must_not_write` 第 1 條（不可把 403 的 `openai.com/index/gpt-5-5-instant` 列進 sources）
   **完全正確，維持**。查核者重新確認那兩個網址在加不加尾斜線、換 `/zh-Hant/`、`/ja-JP/` 下全部 403。
   另確認 `https://developers.openai.com/api/docs/models/gpt-5.5-instant` 回 **404**——
   `must_not_write` 說「API 上沒有這個模型代號」是對的。

---
## ai-news-gpt-live-1-api-20260910

OpenAI 2026-09-10 在 API 正式開放 GPT-Live 1。研究紀錄 67 條事實，查核確認 65 條。
**查核檔用 0-based 編號**（`Fact 6` ＝紀錄第 7 條）。
四條 sources 全部可達、都是真實文件，但**來源清單本身不能出刊**，見 `source_list_fix`。

### must_fix

1. 紀錄第 7 條結尾寫「API 的模型清單頁 Realtime 分類下**只有 GPT-Live 1，沒有 mini 版**」。
   **前半是錯的。** `https://developers.openai.com/api/docs/models` 有一個
   `id="realtime"`、標題 `Realtime` / `Models for realtime speech and translation` 的區塊，
   底下列了**七個**模型：`gpt-live-1`、`gpt-realtime-2.1`、`gpt-realtime-2.1-mini`、
   `gpt-realtime-2`、`gpt-realtime-translate`、`gpt-realtime-1.5`、`gpt-realtime-mini`——
   **其中兩個就是 mini 版**。同一頁的 `.md` 版是沒有分類的平鋪字母清單，所以這個說法也不可能來自 .md。
   而且它與研究紀錄自己的第 67 條（Realtime 仍在更新）互相矛盾。
   **改寫成**：「API 模型清單沒有 `gpt-live-1-mini`。清單頁的 Realtime 區塊除了 GPT-Live 1，
   還列了 `gpt-realtime-2.1`、`gpt-realtime-2.1-mini`、`gpt-realtime-2`、`gpt-realtime-translate`、
   `gpt-realtime-1.5`、`gpt-realtime-mini`。」
   連帶：`not_said` 第 5 條「API 的模型清單裡沒有 `gpt-live-1-mini`」本身是對的，維持；
   `must_not_write` 第 9 條「不要寫 API 上有 `gpt-live-1-mini`。**API 模型清單只有 `gpt-live-1`**」
   的後半句同樣要改掉。
2. 紀錄第 17 條列出定價頁 Standard 表的三列（`gpt-5.6-terra` 2.00／12.00 美元、
   `gpt-5.6-luna` 0.20／1.20 美元、`gpt-6-astra` 10.00／50.00 美元），並說
   「這是 GPT-Live **後端可選模型**的價格」。**三個價格都對，歸屬是推論。**
   GPT-Live 的文件從未公布 Responses 委派支援哪些後端模型；
   `guides/live-delegation` 只點名 GPT-5.6 Terra（`Start with`）與 GPT-5.6 Luna
   （`for cost-sensitive workloads`）；`guides/live` 只寫 `use a supported Responses model`。
   `gpt-6-astra` 在所有語音指南裡總共只出現一次，在 `guides/voice-agents` 第 67 行，
   而且是在**串接式（chained）語音流程**的 Agents SDK 範例裡，不是 GPT-Live 的委派範例。
   **改寫成**：只寫官方點名的 Terra 與 Luna 兩個後端建議，
   **不可把 `gpt-6-astra` 的價格寫成 GPT-Live 的後端價格**。
3. 紀錄第 45 條的 `verbatim_quote`
   `Custom voices are limited to eligible customers. Contact our sales team to learn more.`
   **在被引用的 `.md` 頁面上並不是連續字串**——那份 .md 漏出了原始 JSX：
   `{"Custom voices are limited to eligible customers. Contact our "} [{"sales team"}] {" to learn more..."}`。
   查核者抓了渲染後的 HTML，那句**確實逐字存在**，所以事實成立、可以用；
   **但要引 HTML 版的渲染結果，不要引這份重組字串**。
4. 紀錄第 12 條的 Endpoints 表把最後一列寫成「Completions」。
   **官方印的列名是 `Completions (legacy)`，路由 `v1/completions`。** 照原樣抄。
   同型小錯：`sources[0].title` 記成「API Changelog」，該頁自己的 H1 是 `Changelog`。

### must_add

- **一個比研究者用的框架更強的一手定位陳述，研究者從未抓過那一頁**：
  `https://developers.openai.com/api/docs/guides/audio`（HTTP 200；.md 200、4,927 bytes）
  是 OpenAI 自己的音訊與語音路由頁，現在寫著
  `For a new conversational voice application, start with GPT-Live`，
  並把 Realtime 留給 `when you need its session and tool model`。
  這比從 changelog 推論 GPT-Live 的地位強得多。
- **一個定價陷阱，而且是雙面的**：`pricing.md` 有一句
  `Regional processing (data residency) endpoints are charged a 10% uplift for models released on or
  after March 5, 2026, that are eligible for data residency.`
  GPT-Live 1 符合資料落地資格（美國＋EEA／瑞士）而且在那個日期之後推出。
  **但這句只出現在 Standard 與 Batch 的 token 表底下，沒有在「GPT-Live sessions」那一區重複。**
  所以**文章不可以寫每分鐘 0.05 美元要加 10%**；正確寫法是記成
  **「官方沒有對每分鐘費率說明是否適用這個 10% 加價」**。
- **本篇要與既有的 7/8 那篇擺在一起，需要的一手錨點**：同一份官方 RSS 另有
  〈Introducing GPT-Live〉，pubDate `Wed, 08 Jul 2026 00:00:00 GMT`（link `/index/introducing-gpt-live`），
  以及〈How we built a realtime system for responsive voice AI in six months〉，
  `Mon, 03 Aug 2026`（link `/index/continuous-voice-interaction-with-gpt-live`，同樣 403）。
  7/8 那個 pubDate 就是「ChatGPT 端兩個月前先推出」這個框架的一手依據。
  兩篇文章頁都 403，**只有 feed 的中繼資料可用**。
- **紀錄第 41 條（只能接、不能撥）的具體對照**，夥伴表自己的文字：
  Twilio ＝ `Connect incoming and outgoing phone calls to GPT-Live with Twilio Agent Connect`，
  Telnyx ＝ `Build outbound calling experiences with GPT-Live and the Telnyx Voice API`。
  這就是「外撥必須走合作夥伴整合」在實務上長什麼樣。
- **撰稿陷阱（不是研究失誤），一定要在文章裡調和**：
  `guides/live-prompting` 寫 `The live model has a small context window`（紀錄第 62 條），
  `guides/live-conversations` 寫 `The default context window holds 128,000 tokens`（紀錄第 28 條）。
  兩句都引得對，但放進同一篇文章而不解釋，讀起來就是自相矛盾。
  **調和的數字紀錄裡都有**：`instructions` 上限 16,384 tokens、
  啟動歷史上限 128 則訊息／8,192 tokens，而那 128,000 的工作階段視窗會被**不出現在逐字稿裡的音訊 token**吃掉。
- 查核者確認的一項事實：**1,195 筆 pubDate 裡有 338 筆是 `00:00:00 GMT`**，
  所以那個時間是佔位值——**日期 2026-09-10 可用，時間不可用**。

### live_data_warnings

- **feed 的大小與筆數**：`sourcing_notes` 記 725,972 bytes／1,194 筆，
  查核者抓到 726,611 bytes／1,195 筆（當天 16:00 GMT 又加了一則）。
  目標項目逐位元相同。**不要把 feed 筆數寫進文章。**
- **developers.openai.com 的每一頁都沒有版本號、沒有日期**，是會被改的活頁面。
  「在網址後面加 `.md` 取得 Markdown」是頁面自己寫明的
  （`Markdown versions of documentation pages are available by appending .md to the page URL`），
  所以那不是猜測。**本紀錄的每一個數字都是「2026-09-16 讀到的版本」，正文要寫明。**
- **會隨文件改版而變的具體數字**，引用時都要綁查核日：每分鐘 0.05 美元、
  Tier 1–5 的併發上限 25／50／200／300／500、12 個具名語音、預設語音 `marin`、
  128,000 token 視窗與 90% 門檻、instructions 16,384 tokens、啟動歷史 128 則／8,192 tokens、
  單一事件 content 上限 500 tokens、錄音 30 天到期、每組織 20 個自訂語音、
  音訊樣本 30 秒以內、單次上傳 10 MiB、同意語句 16 種語言、
  WebRTC 先計 15 秒、以及 90 秒＝0.075 美元＋後端 0.02 美元＝0.095 美元這個**官方自陳為示意的試算**。
- **`gpt-live-transcribe` 每分鐘 0.017 美元等轉錄模型價格是另一組模型的價格**
  （紀錄第 16 條、`must_not_write` 第 8 條），不可混用。
- **汰換頁是活文件**：`gpt-realtime` 等舊快照在 2027-01-20 移除、
  `whisper-1` 與 `gpt-4o-transcribe` 等在 2027-02-26 移除——這些是查核當天公布的計畫日期。

### source_list_fix

**以現況交付即不合格。**

1. **67 條事實裡約 33 條掛在 12 個不在 `sources[]` 的網址上**，而且撰稿最想用的頭條數字全部落在那一群裡：
   - `guides/live-conversations` → 第 23、24、25、26、27、28、29、30、31、32、33、34、65 條
     （12 個具名語音與預設 `marin`、128,000 token 視窗與 90% 門檻、錄音 30 天、結束原因）
   - `guides/live` → 第 18、19、20、21 條
   - `pricing` → 第 15、16、17 條
   - `guides/your-data` → 第 53、54、55 條（美國＋歐洲資料落地、ZDR 資格、沒有公開刪除端點）
   - `guides/voice-latency-cost` → 第 56、57、58 條（計費時間定義、WebRTC 15 秒、0.095 美元試算）
   - `guides/live-delegation` → 第 59、60、61 條
   - `guides/live-prompting` → 第 62、63、64 條
   - `openai.com/news/rss.xml` → 第 1、2 條
   - `guides/voice-agents` → 第 22 條；`guides/voice-websockets` → 第 43 條；
     `guides/live-partner-integrations` → 第 44 條；`guides/live-migration` → 第 66 條；
     `deprecations` → 第 67 條
   BRIEF 要求每一個日期、價格、百分比、方案名、地區、語言、模型名都要指到文章 sources 的原文，
   **所以這一包照現狀寫不出來**。研究者在 `sourcing_notes` 裡點出了這件事，卻沒有改 `sources[]`。
   **依文章實際要寫的內容重建 sources（上限仍是 4）**；
   `guides/live-conversations` 與 `guides/your-data` 幾乎一定要頂掉現有的兩條。
2. `sources[0].title` 要改成頁面自己的 H1 `Changelog`。
3. 沒有任何事實追到新聞媒體、整合站或搜尋摘要；模型代號 `gpt-live-1`、端點 `v1/live/sessions`、
   所有事件名與路徑都逐字印在查核者抓過的頁面上，**沒有猜測的識別碼**。
   `platform.openai.com/docs/models` → 301 → `developers.openai.com/api/docs/models` 的轉址鏈也重新確認。
4. `must_not_write` 第 11 條（不要把 403 的 `openai.com/index/...` 當 source）**正確，維持**；
   查核者重新確認 `https://openai.com/index/introducing-gpt-live-1-in-the-api`、
   `https://openai.com/index/continuous-voice-interaction-with-gpt-live`、`https://openai.com/api/`、
   `https://help.openai.com/en/articles` 全部 403。
5. **`not_said` 經查核者逐條驗過，全部成立**：他對所有 GPT-Live 指南加模型頁 grep 了
   語言清單、資格門檻、浮水印／SynthID、SLA 與時長上限——
   沒有任何口說語言清單；GPT-Live 本身沒有等候名單或資格閘門（閘門只存在於 SIP 啟用、
   工作階段儲存與自訂語音）；沒有浮水印、沒有 AI 揭露義務（文件只示範如何「要求」說出揭露，
   並警告不保證逐字）；沒有 SLA；`session.closed` 的 `expired` 背後沒有任何時長數字。
   `must_not_write` 整份健全，**唯一要加的就是上面那個 10% 資料落地加價的陷阱**。
6. 事件日 2026-09-10 成立：RSS pubDate 與 changelog 的 `Sep 10` 標題一致，
   GA 寫成一個狀態、沒有另外的開放日或分批時程，紀錄裡沒有任何日期混淆。
   廠商宣稱標記正確：第 2、8、9 條是僅有的三條 `is_vendor_claim=true`，
   剛好就是那三句形容詞式的官方說法（`stronger instruction following`、
   `full-duplex voice model ... delegate reasoning`、
   `Our premier model ... smooth interruption handling`），沒有把廠商宣稱記成獨立事實。

### 額外：規格合規

研究紀錄缺少四個 BRIEF 規定的頂層欄位：`checked_on`、`title`、`hero_label`、`diagram`。撰稿代理要補齊。

---
## ai-news-nvidia-hugging-face-20260903

NVIDIA 2026-09-03 宣布收購 Hugging Face。研究紀錄 32 條事實，查核確認 25 條。
**查核檔用 0-based 編號**（`verified_facts[15]` ＝紀錄第 16 條）。
四條 sources 全部可達、都是真實文件，**所有 25 條逐字引文在正規化後逐位元吻合**。

### must_fix

1. 紀錄第 16 條寫「2026-09-16 取得的那份公開信版本，簽署名單印有 **235 個**名字」。
   **235 對那份 PDF 而言是正確的（查核者重數：235 個項目、234 個項目符號分隔），
   但它是個過期快照，不可當成這封信的簽署數。**
   同一封信由另一個簽署方一手代管：
   `https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/`（HTTP 200、
   datePublished 2026-07-24T09:48:44+00:00、dateModified 2026-08-11T00:22:42+00:00），
   標題、July 24 2026 的日期與正文全部相同，**但列了 273 個組織**——
   是 NVIDIA 那 235 個的嚴格超集合，多出 38 個（Docker、Dropbox、Asana、Spotify、Snyk、
   SambaNova、Hewlett Packard Enterprise 等），**沒有任何一個出現在 NVIDIA 版卻不在微軟版**；
   而且微軟那一頁自己寫著
   `More than 270 companies and organizations have signed the "Open Weights and American AI Leadership"
   open letter as of August 3, 2026.`
   **NVIDIA 的 PDF 完全沒有截止日期。**
   同一條還有兩個用字問題：PDF 裡 `signator` / `signatories` 出現 **0 次**，
   也從未替那份清單下標題或圖說，所以「the signatory list」是研究者自己的標籤、不是文件的；
   而且那些是**組織名稱**，不是「names（人名）」。
   **改寫成**：完全不要寫簽署數；若一定要提，寫「微軟代管的同一封信在 2026 年 8 月 3 日時表示
   超過 270 個組織簽署」，並註明那是信件自己的截止日。
   另外注意：`wordpress.org/news/2026/08/open-weight/`（一手、HTTP 200）連的是**微軟那一頁**，
   不是 NVIDIA 的 PDF。
2. 紀錄第 3 條寫「同一句話就是該頁的 meta description」。**不是。**
   meta description（與 og:description）是**兩句**：
   `NVIDIA has agreed to acquire Hugging Face. Together, we will scale Hugging Face's platform,
   strengthen its infrastructure and expand access to AI for developers and institutions worldwide.`
   被引用的那句只是後半。**改寫成**：那句是 meta description 的後半句。
3. 紀錄第 8 條的 `verbatim_quote`
   `NVIDIA has released more than 500 models on Hugging Face and more than 250 open datasets. ...
   NVIDIA is the largest contributor of open models and data to Hugging Face, and our contributions
   continue to grow.`
   **兩句在原文裡的順序是相反的**：先是
   `NVIDIA is the largest contributor of open models and data to Hugging Face, and our contributions
   continue to grow.`，**下一段**才是
   `NVIDIA has released more than 500 models on Hugging Face and more than 250 open datasets.`
   用刪節號把順序顛倒的引文不是逐字引文，而且這裡顛倒的是「哪一句在替哪一句背書」。
   研究者的散文摘要順序是對的，**錯在 JSON 紀錄——而那才是撰稿實際會用的東西**。
4. 紀錄第 29 條寫「dataset config renderer **不再處理** HDF5 外部參照」。
   原文是 `nor **wrongly** processes HDF5 external references`
   （`huggingface.co/blog/agent-intrusion-technical-timeline` 的 "What we changed"）。
   **漏掉 wrongly 就把一個修 bug 寫成移除功能。Hugging Face 沒有說它停止處理 HDF5 外部參照。**
5. 同樣是紀錄第 29 條：「內部 service-connector 憑證**收窄到每個叢集一份**」。
   原文是：`the internal service-connector should not have returned a full cluster catalog to a single
   ephemeral client. This was a subtle configuration flaw in our cluster access system. We patched it,
   and each cluster is now fully isolated.`
   **原文沒有任何關於「每個叢集一份憑證」的陳述。**
   同一條還悄悄漏掉同標題下的兩項：`We switched to workload identity when it was not yet implemented`，
   以及 Better detection 底下的
   `tighter enforcement of network origins, plus tooling that flags tokens used from unexpected origins`。
   **第 29 條完全沒有 `verbatim_quote`，是整份紀錄唯一的長段落無引文改寫——整條要照原文重寫。**
6. 紀錄第 15 條寫「Huang 提到的那封公開信就是〈Open Weights and American AI Leadership〉」，
   並標成 `is_vendor_claim: false`。**兩個部分都是推論。**
   NVIDIA 那篇裡
   `Recently, I coauthored an open letter on the importance of open weights to the AI economy`
   這句是**純文字、沒有超連結**（查核者列舉了 `<article>` 內所有 `<a>`，內文唯一的連結是
   `open model` → `https://www.nvidia.com/en-us/glossary/open-models/`）；
   而那封信 5 頁裡 `Huang` 與 `Jensen` 各出現 **0 次**，整份文件沒有署名任何作者。
   **改寫成**：只能寫「Huang 表示他共同署名了一封關於開放權重的公開信」，
   以及另外分開寫「NVIDIA 網站上代管了一封同名的公開信」。**不可標 `is_vendor_claim: false`。**
   （網址本身不是猜的——它由限定 nvidia.com 網域的搜尋回傳，所以沒有觸犯猜網址那條；
   但研究紀錄沒有寫下它是怎麼找到的，應該補。）
7. 紀錄第 15 條的 `verbatim_quote` `Open Weights and American AI Leadership / July 24, 2026`
   **是研究者自己插入 ` / ` 拼出來的**。PDF 裡標題分兩行、日期在空行之後，那些字元並不相鄰。
   它能通過正規化比對只是因為分隔符被正規化掉了。**`verbatim_quote` 不可含自創標點。**
8. 紀錄第 14 條寫「NVIDIA 沒有另外發一頁新聞室稿」。
   **據查核者所能確認是真的，但那是從 20 筆 feed 視窗推論出來的，紀錄卻寫成事實。**
   查核者用研究者沒用的路徑佐證：`https://nvidianews.nvidia.com/news?q=Hugging%20Face`（HTTP 200）
   只回傳 `https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/` 與一則無關的 LeRobot 貼文，
   沒有 `nvidianews.nvidia.com/news/...` 的新聞稿。**要把查法寫進去，不要只寫結論。**
9. 紀錄第 25 條寫「2026-07-09 02:28 UTC 到 2026-07-13 14:14 UTC——**約 4.5 天的行動**」。
   時間窗與 `4.5-day campaign` 都在原文裡，**但同一篇的 TL;DR 寫
   `Over roughly two and a half days inside our infrastructure`**。
   4.5 天是**整個窗**，含發生在 OpenAI 與第三方基礎設施上的 Stage 1；
   **在 Hugging Face 裡面的只有約 2.5 天**。
   只記 4.5 天會讓文章寫成「攻擊者在 Hugging Face 裡待了 4.5 天」，原文沒有這樣說。**兩個數字都要記。**
10. 紀錄第 23 條與第 28 條讀起來像是 2026-07-16 與 2026-07-27 兩篇對鑑識所用的模型說法不同
    （`zai-org/GLM-5.2` vs `nvidia/GLM-5.2-NVFP4`）。**2026-07-27 那篇兩個都寫了**：
    TL;DR 是 `Using open-weights models, in particular zai-org/GLM-5.2`，
    分析段是 `We stood up the quantized version of ZAI's GLM-5.2 by Nvidia ( nvidia/GLM-5.2-NVFP4 )
    on our own infrastructure`。
    **兩篇之間沒有矛盾，文章不可寫成有矛盾。**

### must_add

- **一個被漏掉、而且更好的一手來源**：`https://data.sec.gov/submissions/CIK0001045810.json`
  在本容器回 HTTP 200（159,883 bytes）。它是 SEC 自己的 submissions API，
  比 `efts.sec.gov/LATEST/search-index` 乾淨得多，能確認紀錄第 31 條的每一項
  （accession 0001045810-26-000078、form 8-K、items 8.01、filingDate 2026-09-03、
  reportDate 2026-09-02、primaryDocument `nvda-20260902.htm`、fileNumber 000-23985），
  **而且多給一個研究者沒有的事實**：`acceptanceDateTime 2026-09-03T12:03:56.000Z`——
  比部落格的 `article:published_time`（11:56:49+00:00）晚約 7 分鐘、
  比新聞室 RSS 的 pubDate（11:59:49 GMT）晚 4 分鐘。
  **部落格在先、8-K 在後，同一天。** 這強化了 slug 維持 20260903 的決定，應該記下來。
- **NVIDIA 那篇裡被漏掉的一整段，而且它給了第三個數字**：
  `NVIDIA has been committed to open weight models for years, demonstrated by multiyear investments and
  major contributions to open source platforms, including Hugging Face. NVIDIA has said that open
  models, data and tools broaden access to AI, and it has contributed hundreds of open models and
  datasets to Hugging Face as part of that effort.`
  除了 500+／250+ 之外多出一個「hundreds」，而且這段在一篇第一人稱的文章裡用**第三人稱**寫——
  有理由把它當成公司樣板文字，而不是 Huang 的話。
- **NVIDIA 的政策論證整段被漏掉，而那正是把這樁交易接到開放權重框架的環節**：
  `Open models let startups, businesses, universities and public institutions build on advanced
  capabilities without training every model from scratch. They enable organizations to match the right
  model to the right job. That is how AI can advance safely, strengthen cybersecurity and sovereignty,
  accelerate innovation, and reach factories, hospitals, farms, classrooms and Main Street businesses
  around the world.` 後面接獨立一行 `AI advances faster when people can build together.`
- **收購文內文唯一的超連結**是 `open model` 指向
  `https://www.nvidia.com/en-us/glossary/open-models/`（HTTP 200、437,021 bytes）。
  那是 NVIDIA 自己的定義頁，也是這篇文章唯一以連結背書的定義——
  比那份沒有連結的 PDF 更適合當「開放權重」那一個子句的依據。
- **一手歸因被漏掉**：2026-07-27 技術文的 TL;DR 寫
  `an autonomous AI agent driven by a combination of OpenAI models ran an end-to-end intrusion against
  our platform`。
  這是 Hugging Face 自己具名說出攻擊由誰的模型驅動。
  研究者把這個問題丟進 `unverified_or_excluded`（第 10 條），
  **它應該進 `verified_facts` 並標 `is_vendor_claim: true`。**
- **Hugging Face 自承的失誤被漏掉**：同一篇寫自家偵測堆疊
  `failed to correctly raise the alert's criticality and trigger the on-call team, costing precious
  time in the response`。只寫好看的那一半就是照抄公關稿。
- **三段替具名第三方澄清的文字，文章絕不可寫歪**：
  `the ExploitGym maintainers and their infrastructure had no involvement in the deployment or
  operation of that evaluation environment`；被濫用的框架是
  `an instance labeled "CyberGym", deployed by an unknown third party, exposing an arbitrary-code
  endpoint that upstream CyberGym does not provide`；第三方沙箱供應商具名為 Modal，
  而且 `Modal's infrastructure was not compromised in any way.`
- **署名被漏掉**：2026-07-27 技術文由四位具名 Hugging Face 工程師署名——
  Hugo Larcher（hlarcher）、Adrien Carreira（XciD）、raphael g（raphael-gl）、
  Christophe Rannou（chris-rannou）；2026-07-16 的揭露則署名 `system`。
  兩篇的頁面日期 July 27, 2026 與 July 16, 2026 都在頁上確認。
- **初始入侵途徑在技術文裡有精確名稱**：一個回傳本機檔案內容的 HDF5 external raw storage
  資料集讀取，以及一個執行任意程式碼的 Jinja2 template injection，兩者都打同一個
  config-driven data loader、在正式環境的 Kubernetes pod 上。
  2026-07-16 的揭露寫得比較鬆（`a remote-code dataset loader and a template-injection in a dataset
  configuration`）。**中文要照較晚、較精確的那個寫法。**
- **另一組數字被漏掉**：除了逐日次數（07-09 3,779；07-10 1,135；07-11 7,677；07-12 3,892；
  07-13 1,130——五個全部逐字確認）之外，文章還有一張階段表：
  recon 6,191；rce 2,911；dropper 6,972；exfil 56；c2 114；evasion 6；k8s 87；
  supply-chain 69；tailscale 115。**用一張，不要混用。**
- 技術文自己引用 OpenAI 那一頁的網址是
  `https://openai.com/index/hugging-face-model-evaluation-security-incident/`（帶尾斜線）——
  這是一手的 Hugging Face 頁面替那個網址背書。查核者重測：加不加尾斜線都 403，
  `https://openai.com/index/hugging-face-incident-and-the-road-ahead` 同樣 403。**研究者的封鎖結論成立。**
- 公開信 PDF 是 5 頁，**但第 4、5 頁是空白**；信的內容是 3 頁，項目清單在第 3 頁末。
  「5 頁」技術上為真、實務上會誤導。
- **研究者最強的那個負面結論經查核者用另一條路徑重驗，成立**：
  `huggingface.co/clem/activity/posts`（HTTP 200）顯示 clem 最近兩則 HF 貼文的 publishedAt 是
  2025-08-07T16:50:56Z 與 2025-06-19T17:46:44Z，**沒有 2026 年的貼文**；
  該頁上看得到的 2026-09-03 時間戳是 2025-08-07 那則底下留言串的 `updatedAt`，不是新貼文。
  `huggingface.co/api/posts?author=clem` 回的是 SPA 殼、`huggingface.co/posts/clem` 回 401，
  **那兩條不能當檢查**；活動頁才可以。
  `acquir` 在 `huggingface.co/blog`、`/blog/community`、`/clem`、`/clem/activity/posts`、
  `/clem/activity/community` 上都是 0 次命中；`https://huggingface.co/blog/huggingface` 回 404。

### live_data_warnings

- **公開信的簽署數是典型的活數字**：NVIDIA 版 235、微軟版 273、信件自陳「超過 270（截至 2026-08-03）」。
  **不要印任何簽署數**，也不要因為某家不在名單上就寫成「拒簽」
  （`must_not_write` 第 12 條已正確處理 Anthropic，維持）。
  PDF 的 CreationDate `D:20260730024102Z` / ModDate `D:20260729234720-03'00'` 與
  sha256 `12a888ac...` 都是快照值。
- **平台規模數字全部是 NVIDIA 自陳、沒有截止日、沒有方法學、沒有第三方統計**：
  1,800 萬以上開發者、300 萬以上模型、50 萬資料集、100 萬應用、20 萬以上公司，
  以及 NVIDIA 自己的 500+ 模型／250+ 開放資料集與「最大貢獻者」。
  `not_said` 第 10 條正確，**不可自行補上一個原文沒有的截止日**。
- **各種 feed 的筆數與最新日期都是活值**：`nvidianews.nvidia.com/releases.xml` 20 筆、
  最新 Wed 16 Sep 2026 15:00:48 GMT；`huggingface.co/blog/feed.xml` 862 筆、
  最新 Tue 15 Sep 2026 16:00:44 GMT；`openai.com/news/rss.xml` 紀錄 1,195 筆、查核者 1,196 筆（當日漂移）。
  **「Hugging Face 沒有發任何收購公告」這個負面結論是 2026-09-16 當天的狀態**，
  要寫成「截至 2026 年 9 月 16 日未見」。
- NVIDIA 部落格頁的 `article:modified_time` 是 `2026-09-03T20:54:05+00:00`
  （比 published 晚），是活值，不要當事件日。

### source_list_fix

4 條，在上限內，**四條全部 HTTP 200 且是真實內容**（查核者逐一驗過大小與標題）。
但有兩個結構問題：

1. **4 條事實掛在 sources 以外的網址，而且那四個都是 feed 或搜尋 API**，
   依紀錄自己的 `must_not_write` 第 10 條，它們不得進 `sources[]`：
   第 14 條 → `https://nvidianews.nvidia.com/releases.xml`；
   第 30 條 → `https://openai.com/news/rss.xml`；
   第 31 條 → `https://efts.sec.gov/LATEST/search-index?q=%22Hugging+Face%22&forms=8-K`；
   第 32 條 → `https://huggingface.co/blog/feed.xml`。
   **也就是說，從這四條寫出來的任何一句話在成稿裡都沒有可追溯的網址**：
   8-K 的存在、OpenAI 那兩篇的標題、Hugging Face 沒有公告——
   每一句都需要一個文章頁來源，或在正文裡明白寫出「依官方 feed」。
   `data.sec.gov` 那條（見 must_add）是 8-K 那一項可用的替代文章頁。
2. 第 15 條那個 PDF 網址沒有記下取得方式（見 must_fix 6）；
   研究紀錄應該補一句它是由限定網域的搜尋取得，不是拼出來的。
3. **沒有任何一條事實追到新聞媒體、整合站、律師事務所部落格或搜尋摘要**；
   `unverified_or_excluded` 把 Yahoo／Bloomberg 的現金加股權拆分、
   「definitive agreement」標題、CNBC 的時間點與 `discuss.huggingface.co` 的論壇風向
   全部正確隔離。這一軸乾淨。

---
## ai-news-openai-astral-20260319

Astral（uv／Ruff／ty 的開發商）2026-03-19 宣布將加入 OpenAI 的 Codex 團隊。
研究紀錄 38 條事實，查核確認 36 條。**本篇查核檔用 1-based 編號，與研究紀錄位置一致。**

### must_fix

1. 紀錄第 35 條（來源 `https://astral.sh/pyx`）寫「該頁沒有給日期、沒有給理由，
   **也沒有提到 OpenAI**」。**最後一個子句被推翻。**
   查核者抓了那一頁（HTTP 200、38,110 bytes），裡面 `OpenAI` 出現 **2 次**：
   Astral 在全站頁首掛了一條公告列，內容是
   `<span>Astral to join OpenAI as part of the Codex team<!-- --> →</span>`，外面包著連結。
   同一條公告列也在 `https://astral.sh/`（200、144,076 bytes）上。
   第 35 條其餘部分逐字確認：`pyx is no longer accepting new signups.`、
   `A Python-native package registry from the creators of uv.`、
   客戶 Ramp／Intercom／fal，以及確實沒有日期、沒有理由。
   **改寫成**：刪掉「沒有提到 OpenAI」，改寫成「pyx 頁面上仍掛著全站的收購公告列」。
2. 紀錄第 37 條寫「OpenAI 的 Codex 開發者文件首頁（2026-09-16 取得）裡
   `astral`、`ruff`、`uv` 各出現 0 次；收購六個月後，OpenAI 的公開 Codex 文件沒有露出 Astral 的工具」，
   url 掛 `https://developers.openai.com/codex/`。**照這個網址無法成立。**
   那個網址不提供任何頁面：`curl -A Mokaair-editorial` 回 **HTTP 308** 轉到 `/codex`，
   再 **308** 轉到 `https://learn.chatgpt.com/docs`——**不同主機**。
   最後拿到的 200 是 ChatGPT Learn 文件的外殼，抽出來的可見文字（12,413 字元）是導覽索引，
   **而且裡面連 `python` 也是 0 次**——足以證明那幾個 0 是導覽殼的產物，不是關於 Codex 文件的證據。
   **正確的替代來源存在**：`https://learn.chatgpt.com/docs/llms-full.txt`
   （200、1,809,784 bytes，開頭是
   `# Codex — full documentation / > Single-file Markdown export of ChatGPT docs for Codex across the
   CLI, IDE, cloud, and SDK.`）對 astral／ruff／uv 全部 0 次命中，
   `https://learn.chatgpt.com/docs/llms.txt`（200、26,062 bytes）同樣 0 次。
   **改掛那個網址，而且即使如此這仍是很弱的負面證據**——
   只能寫「OpenAI 的 Codex 文件未提到」，**絕不可寫成對 OpenAI 意圖的陳述**。
3. 紀錄第 19 條寫「2026-09-16 查核時，官方 uv 文件**仍然**寫 `uv is backed by Astral, the creators of
   Ruff.`」，用來支撐「六個月後還是 Astral」。**這個「仍然」站不住**：
   `https://docs.astral.sh/uv/` 的頁尾 git 修訂資訊寫 `title="March 13, 2026 14:17:06 UTC"`，
   也就是那一頁**從公告前六天起就沒有再改過**，證明不了任何收購之後的決定。
   查核者另外確認：`https://docs.astral.sh/ty/` 確實帶 September 15, 2026 的修訂日（紀錄第 21 條正確）；
   `https://docs.astral.sh/ruff/` **完全沒有修訂日**，這一點研究者沒寫。
   **改寫成**：三頁的文字都還寫 backed by Astral，但只有 ty 那一頁有近期的修訂日，
   uv 那一頁的最後修訂是 2026-03-13（早於公告），ruff 那一頁沒有修訂日。
4. 紀錄第 34 條引用 uv audit 比 pip-audit 快 4 到 10 倍。
   **Astral 自己的註腳限定了這個數字，紀錄沒記**：
   `Comparisons between uv audit and pip-audit are slightly apples-to-oranges, since the representative
   uses of the two are often different. The short version: uv audit is significantly faster than most
   equivalent pip-audit invocations, but using pip-audit with a fully-primed cache can be roughly as
   fast as uv audit.`
   **要用 4x–10x 就必須帶上這個但書。**

### must_add

- **六個月後狀態的更強、更安全的證據，比第 37 條那個壞掉的主張好用得多**：
  `https://astral.sh/about`（200、79,571 bytes，2026-09-16 查核）仍把 Charlie Marsh 署名為
  `Founder, Astral`，仍寫著 `We're growing the team / Not rapidly, but deliberately`、
  `We're a small, distributed team of software engineers`，以及
  `We build in the open. Our tools are open source and permissively licensed.`
  **整頁沒有任何關於 OpenAI 所有權的陳述。**（該頁的使命段只列 Ruff 與 uv，沒有 ty。）
- **六個月後 Astral 自己仍在用全站公告列推這樁交易**：
  `Astral to join OpenAI as part of the Codex team →`（見 must_fix 1）。這是可用的事實。
- **經查核者逐一重抓、可以放心寫的部分**（提高撰稿信心）：
  Ruff v0.16.0 那篇（frontmatter 2026-07-23、作者 Brent Westbrook）逐字寫
  `Ruff now enables 413 rules by default, up from 59 in previous versions. Since Ruff's default rule
  set was last modified in v0.1.0, the number of rules in Ruff has grown from 708 to 968`，
  並精確列出那 18 條被移除的規則 E401、E402、E701、E702、E703、E711、E712、E713、E714、
  E721、E731、E741、E742、E743、F403、F405、F406、F722。
  PyPI JSON：uv 0.12.15 上傳 2026-09-15T12:07:02Z、`license_expression "MIT OR Apache-2.0"`；
  ruff 0.16.7 上傳 2026-09-10T18:03:30Z、`"MIT"`；ty 0.0.81 上傳 2026-09-15T02:04:51Z、
  `license_expression` 為 null。
  2023 年那篇（frontmatter 2023-04-18）寫
  `We've raised $4m in seed funding led by Accel, with participation from Caffeinated Capital,
  Guillermo Rauch (Vercel), Solomon Hykes (Docker), David Cramer (Sentry), and others.`
  公告裡所有外連都與紀錄相符，含 `OpenAI's own announcement` →
  `https://openai.com/index/openai-to-acquire-astral/` 與 Codex → `https://chatgpt.com/codex`。
- **一個可以寫、但不可寫成官方規則的觀察**：OpenAI 的 feed 區分
  「OpenAI to acquire X」（Astral 2026-03-19、Ona 2026-06-11、Promptfoo 2026-03-09、Neptune 2025-12-03）
  與「OpenAI acquires X」（TBPN 2026-04-02、Rockset 2024-06-21、Global Illumination 2023-08-16）。
  Astral 的標題用的是**未完成式**，支持研究者「已達成協議、尚未完成」的讀法。
  **這是一個模式，不是 OpenAI 說過的規則，不可寫成官方說法。**
- **路徑建構的說明應補進研究紀錄**：第 26–29 條用的
  `raw.githubusercontent.com/astral-sh/<repo>/main/<file>` 路徑是照慣例組出來的、不是從任何讀過的頁面連出來的。
  查核者五個全抓過、全部 200 且內容完全吻合
  （uv `LICENSE-MIT` 為 `Copyright (c) 2025 Astral Software Inc.`、uv `LICENSE-APACHE` 為 Apache 2.0、
  ruff `LICENSE` 為 `Copyright (c) 2022 Charles Marsh`、ty `LICENSE` 為
  `Copyright (c) 2025 Astral Software Inc.`），**所以沒有捏造，但紀錄應該寫明這些路徑是組出來的。**
- **紀錄第 29 條的範圍要限縮**：`https://raw.githubusercontent.com/astral-sh/uv/main/CHANGELOG.md`
  （50,166 bytes）**只完整保留 0.12 系列**——16 個標題從 0.12.0 到 0.12.15、
  `Released on 2026-07-28` 到 `Released on 2026-09-15`（0.12.14 與 0.12.15 同為 2026-09-15），
  0.11.x 以前只是指標。
  所以它佐證的是 **2026-07-28 起**的連續發版，**不是 2026-03-19 到 2026-09-15 整個區間**。
  16 這個數字與兩個日期本身精確無誤。
- **ARK 的處理維持**：查核者在 ark-funds.com 上找到的唯一一手頁面講的是
  ARK Venture Fund（ARKVX），一檔持有未上市公司的封閉式間隔基金，**不是 ETF**。
  那是線索、不是確認。研究者的排除是對的；若要提 ARK，**只能停在「OpenAI 表示」的層次、不寫任何代號**。

### live_data_warnings

- **OpenAI feed 的筆數**：紀錄第 4 與第 38 條都寫「1,194 筆」，查核者當天抓到 **1,195 筆**
  （726,611 bytes、最新 pubDate 2026-09-16 16:00:00 UTC、最舊 2015-12-11）。
  實質結論不變（全 feed 只有一則命中 `astral`，就是 2026-03-19 那則，
  標題 `OpenAI to acquire Astral`、描述
  `Accelerates Codex growth to power the next generation of Python developer tools`、
  category `Company`、link `https://openai.com/index/openai-to-acquire-astral`），
  **但這個滾動的數字不可入稿**。
- **Astral 的 blog feed 39 筆、最新 2026-09-04**（23,318 bytes）同理，是活性診斷值。
- **PyPI 的版本號與上傳時間都是活值**：uv 0.12.15、ruff 0.16.7、ty 0.0.81 以及三個上傳時間戳
  都是 2026-09-16 讀到的狀態；`ty is still on a 0.0.x version number` 這個觀察同樣會過期。
- **`openai.com/sitemap.xml/company/` 的 261 個 `<url>` 與該頁的
  `<lastmod>2026-08-31T19:59:25.765Z</lastmod>`（65 個 hreflang 替代，含 zh-Hant、zh-Hans-CN、
  ja-JP、ko-KR）** 經查核者重抓確認，`roughly sixty` 的說法合理。
  研究者拒絕把那個 lastmod 當成交易日期是**正確的**，維持。
- **文件頁的修訂日是活值**：ty 頁的 September 15, 2026、uv 頁的 March 13, 2026 14:17:06 UTC。
- **`pyx is no longer accepting new signups.` 是查核當天的頁面狀態，沒有日期也沒有理由**；
  `must_not_write` 第 3 條（不可把它跟收購接上因果、也不可幫它推一個時間點）**維持**。
- **「交易是否已完成」是持續變動的狀態**：沒有任何可達的一手頁面說它完成了，
  也沒有 feed 後續項目。`not_said` 第 2 條的寫法（官方公告的是「已達成協議」、
  並未說明何時完成）**維持**。

### source_list_fix

4 條，在上限內。四條全部可達、內容為真（`astral.sh/blog/openai` 200／52,443 bytes；
`openai.com/news/rss.xml` 200；`docs.astral.sh/uv/` 200；`pypi.org/project/uv/` 200，顯示 uv 0.12.15）。
但問題不少：

1. **一個被引用的網址根本不落地**：第 37 條掛的 `https://developers.openai.com/codex/`
   是 308→308 轉到另一個主機（見 must_fix 2）。**這是本篇唯一一個「記了卻沒抓到」的網址，必須換掉。**
2. **38 條事實裡有 18 個不在 sources 的網址**，共支撐 21 條事實：
   `astral.sh/blog/rss.xml`（第 7、30 條）、
   `astral.sh/blog/announcing-astral-the-company-behind-ruff`（第 16、17 條）、
   `astral.sh/blog/python-packaging-council`（第 31、32 條）、
   `openai.com/sitemap.xml/company/`（第 6 條）、`docs.astral.sh/ruff/`（第 20 條）、
   `docs.astral.sh/ty/`（第 21 條）、`pypi.org/pypi/uv/json`（第 23 條）、
   `pypi.org/pypi/ruff/json`（第 24 條）、`pypi.org/pypi/ty/json`（第 25 條）、
   `raw.githubusercontent.com/...`（第 26、27、28、29 條）、
   `astral.sh/blog/ruff-v0.16.0`（第 33 條）、`astral.sh/blog/uv-audit`（第 34 條）、
   `astral.sh/pyx`（第 35 條）、`docs.pyx.dev/`（第 36 條）、
   `developers.openai.com/codex/`（第 37 條）。
   **要用哪一條就得換進四條裡。**
   研究紀錄自己在 `sourcing_notes` 提供了替代方案（`astral.sh/pyx` 或
   `astral.sh/blog/python-packaging-council` 可頂掉 `pypi.org/project/uv/`），那是合理的做法。
3. **`sources[1]` 是 feed 網址**，與 BRIEF 抵觸。
   查核者獨立重現了那個封鎖：`https://openai.com/index/openai-to-acquire-astral` 403（9,791 bytes）、
   帶尾斜線 403、`/ja-JP/` 403、`/zh-Hant/` 403、`.md` 變體 403、`https://openai.com/` 本身也 403。
   **這個 feed 確實是唯一可達的 OpenAI 自撰文字**，研究者明白記錄了這個例外，處理方式是對的；
   `must_not_write` 第 12 條（不要把 403 的網址寫進 sources）**維持**。
4. **沒有任何一條事實追到新聞媒體、整合站、律師事務所部落格或搜尋摘要**；
   `pypi.org` 是 PSF 的官方索引，對套件中繼資料而言是一手。這一軸乾淨。
   事件日 2026-03-19 由兩條獨立的一手管道支撐（Astral 的 MDX frontmatter `"date":"2026-03-19"`
   加上渲染出的 `March 19, 2026`；OpenAI feed 的 pubDate `Thu, 19 Mar 2026 00:00:00 GMT`——
   2026-03-19 確實是星期四），沒有日期混淆。

### 額外：規格合規

研究紀錄缺少三個 BRIEF 規定的頂層欄位：`title`、`hero_label`、`diagram`。撰稿代理要補齊。

---
## ai-news-openai-broadcom-chip-20260624

OpenAI 與 Broadcom 2026-06-24 共同發表 Jalapeño 推論晶片。研究紀錄 33 條事實，查核確認 33 條的內容，
**沒有任何一條被推翻**。問題集中在**廠商宣稱的標記**、**引文完整性**與**來源結構**。
**查核檔用 0-based 編號**（`VF6` ＝紀錄第 7 條）。

### must_fix

1. **五條事實的 `is_vendor_claim` 標錯，全部要改成 `true`，並在正文寫成「Broadcom 與 OpenAI 表示」。**
   - 紀錄第 7 條：`OpenAI designed the chip from scratch around its deep understanding of LLM
     fundamentals ... with partners Broadcom and Celestica`。引文逐字正確，
     但「從零設計、基於自己對 LLM 本質的深刻理解」是關於功勞與流程的自述，外部無法驗證。
   - 紀錄第 11 條：`As of the announcement the chip exists as engineering samples, **NOT SHIPPING
     PRODUCT**`。**兩個缺陷**：(a)「不是出貨產品」那句**頁面上從來沒有**，是研究者的推論；
     原文只有 `Engineering samples of the Jalapeño chip are running ML workloads in the lab at
     production target frequency and power, including GPT-5.3-Codex-Spark.`；
     (b) 實驗室內的狀態由廠商回報、外部觀察不到，本來就是廠商宣稱。
     **把「NOT SHIPPING PRODUCT」刪掉，只寫官方那句。**
   - 紀錄第 20 條：`designed for initial deployment by the end of 2026, and expanding in the years ahead`。
     **同一份新聞稿的 Cautionary Note 把 `the deployment of gigawatt scale datacenters`
     列為前瞻性陳述，並說 `undue reliance should not be placed on such statements`。**
     發行人自己正式免責的句子不能記成非廠商事實。
   - 紀錄第 21 條：`To be deployed at gigawatt scale with data center partners, over multiple
     generations`。理由同上，也在那份前瞻性陳述的涵蓋範圍內。
   - 紀錄第 30 條：`OpenAI has grown to over 800 million weekly active users`。
     **這一條標錯得最明顯**——新聞稿裡未經查核的自報使用者數，時點是 2025-10-13。
     **必須寫成「OpenAI 表示」並附上 2025-10-13 這個日期**，不可寫成裸事實。
   同型但程度較輕、也要改成廠商宣稱的：紀錄第 17 條的「九個月」本身、
   第 27 條的 `targeted to start in the second half of 2026, to complete by end of 2029`、
   第 13 條的 `A detailed technical report on performance will be presented in the coming months`
   （那是對未來出版的承諾，不是已觀察到的事實）。
   （第 17 條抓到的「條列 vs 內文」差異本身是真實的文字事實，那部分維持。）
2. 紀錄第 6 條的 `verbatim_quote` 把開頭五個條列用 ` / ` 串成一串。
   **五段條列文字全部確認存在、順序正確、就是五段**，
   **但那串字串在頁面上並不存在**——` / ` 是研究者插進去的。
   **拆成五段引文，或標成重組字串。**

### must_add

- **新聞稿裡其實有成本語言，而 `must_not_write` 第 1 條會讓撰稿者以為沒有。**
  內文逐字寫著：
  `If AI can help engineers design better chips faster, it can lower the cost of compute across the
  industry and help democratize access to advanced AI.`
  它是**條件句（if）**、講的是**全產業**、**沒有數字**、**沒有點名任何晶片**。
  **記成廠商宣稱**，並把 `must_not_write` 第 1 條改寫成：
  只禁止沒有出處的「便宜 50%」與任何數字化的價格比較，不是禁止提到官方這句條件式的成本說法。
- **一句應該進 `verified_facts` 卻只躺在 `not_said` 第 9 條裡的原文**：
  `Jalapeño is designed with flexibility to work with all LLMs guided by OpenAI's insights into the
  inference needs of current and future AI models across the industry.`
  這是最容易被誤讀成「這顆晶片會賣給別人」的一句，**應該正式記成事實並標
  `is_vendor_claim: true`，同時保留現有的但書（官方從未說要銷售）**。
- **第二處「條列 vs 內文」不一致，研究者沒抓到**：研究者抓到了
  `design to production`（條列）vs `design to manufacturing tape-out`（內文），
  **但效能那一處是同一個問題**——條列第 3 點寫每瓦效能
  `better than current state-of-the-art`，內文寫
  `**substantially** better than current state-of-the-art`。
  **用內文的寫法，並註明兩處不同。**
- **新聞稿自己的三個小節標題都沒有記下來**：
  `Designed to be the best inference platform for LLMs`、
  `Nine-month tape-out, accelerated by OpenAI models`、
  `Building a multi-generation platform with partners`。
  中間那個是 Broadcom 自己的標題，**獨立佐證了官方框架講的是 tape-out 而不是量產**，
  正好直接支撐 `must_not_write` 第 4 條。
- **一個絕不可「順手修掉」的來源怪處**：Richard Ho 被介紹為
  `who leads OpenAI's hardware program`，但他被引用的話卻是
  `using detailed insights from our close collaboration with OpenAI researchers`，
  讀起來像是 OpenAI 以外的人在說話。**頁面就是這樣印的。照原樣引用，
  不要改歸給 Broadcom，也不要偷偷修好。**
- **兩份新聞稿的職稱會漂移，不可混用**：Charlie Kawwas 在 2026-06-24 是
  `Semiconductor Solutions President`，在 2025-10-13 是
  `Charlie Kawwas, Ph.D., President of the Semiconductor Solutions Group for Broadcom Inc.`；
  Sam Altman 在 2026 年 6 月是 `OpenAI CEO Sam Altman`，在 2025 年 10 月是
  `Sam Altman, co-founder and CEO of OpenAI`。
- **2025-10-13 那份還有一段 Sam Altman 的引言沒記**
  （`Partnering with Broadcom is a critical step in building the infrastructure needed to unlock AI's
  potential…`），以及副標
  `Multi-year partnership enables OpenAI and Broadcom to deliver accelerator and network systems for
  next-generation AI clusters`。研究者記了 Kawwas 卻沒記 Altman。屬背景資訊。
- **Celestica 完全沒有旁證**：`corporate.celestica.com/news`（HTTP 200）與
  `corporate.celestica.com/rss/news-releases.xml`（HTTP 200）**完全沒有提到 Jalapeno、OpenAI 或 Broadcom**。
  **Celestica 的角色完全建立在 Broadcom 的說法上，要這樣寫。**
- **日期處理健全，但有一個值得保留的細節**：OpenAI 的 feed 發布時間是
  24 Jun 2026 06:00 GMT，而 Broadcom 的 IR 頁戳的是 `2026-06-24T09:00:48-0400`（＝13:00 GMT），
  相差七小時、同一個日曆日；換算台北時間是 2026-06-24 的 14:00 與 21:00，
  **所以 zh-TW 內容包用 `news_date: 2026-06-24` 是安全的**。
  公告、發布、`initial deployment by the end of 2026`，以及 2025-10-13 的
  `H2 2026 到 end of 2029` 視窗都被正確分開，**沒有任何日期混淆**。

### live_data_warnings

- **OpenAI feed 的筆數是活值**：`sourcing_notes` 記 725,972 bytes／1,194 筆，
  查核者抓到 726,611 bytes／1,195 筆。不入稿。
- **Broadcom 的 IR RSS 只保留最新 10 筆**（查核者抓到的區間是 2026-08-06 到 2026-09-02），
  **回不到 6 月**。它不能當成任何較早日期「有沒有新聞」的依據。
- **`https://investors.broadcom.com/news-releases`（列表頁）回 404**，
  新聞稿只能用 `news-release-details` 的 slug 直接取得——這個結構會變。
- **所有「未來」的數字都是前瞻性陳述**：`initial deployment by the end of 2026`、
  `gigawatt scale`、`beginning in 2026`、以及 2025-10-13 那份的
  `10 gigawatts`、`second half of 2026`、`end of 2029`。
  Broadcom 自己在 Cautionary Note 裡說 `undue reliance should not be placed on such statements`，
  **這一點紀錄 `must_not_write` 第 15 條要求寫進正文，維持**。
- **`over 800 million weekly active users` 是 2025-10-13 的時點數字**，2026-06-24 那份完全沒有使用者數。
  引用一定要附日期（紀錄第 30 條與 `editorial_brief` 都正確要求，維持）。
- **`what may be the fastest ASIC development cycle ever achieved` 的 `may be` 是官方的保留**，
  `must_not_write` 第 11 條正確，維持。

### source_list_fix

3 條（在 2–4 的範圍內），**33 條事實全部追得到這三條之一**——
本垂直唯二做到這件事的另一篇。但仍有兩件事：

1. **`sources[2]` 是 feed 網址**（`https://openai.com/news/rss.xml`），
   承載紀錄第 4、31、32、33 條。BRIEF 明文
   「feed 給的是日期與標題，不是內容……sources 放的是文章頁的網址，不是 feed 的網址」。
   **兩份 Broadcom 的 IR 頁已經滿足「至少 2 條一手來源」**，
   建議把 feed 那一條從 `sources[]` 拿掉，那四條事實留在研究紀錄裡並標明是 feed 的中繼資料。
   這是規格違反，不是捏造。
2. **`sourcing_verdict: "full"` 誇大了。** 就 2026-06-24 這個事件而言，
   **只有一個可讀的一手文章頁（Broadcom 的）**；OpenAI 自己那篇 403，
   能拿到的 OpenAI 自撰文字只有 26 個字的 feed 描述。
   **要嘛加註「OpenAI 那一側從未讀到」，要嘛降級。**
3. **存取怪癖，整批都會踩到，必須記住**：`investors.broadcom.com` 與
   `corporate.celestica.com`（同一個 IR 平台）**拒絕 BRIEF 規定的 User-Agent `Mokaair-editorial`**——
   curl 以結束碼 92（HTTP/2 stream INTERNAL_ERROR、零位元組）失敗，
   改用 curl 預設 UA 才回 HTTP 200。（研究者記的是結束碼 52「Empty reply from server」，
   查核者看到的是 92，兩者都是失敗。）
   **後續重驗這兩個來源的人若不知道這件事，會誤判成來源已死。**
   `www.broadcom.com/company/news/product-releases/64506` 回 200 但是 JS 外殼：
   `<title>` 是正確標題，正文裡 `Jalape`、`Celestica`、`Tomahawk`、`GLOBE NEWSWIRE`、
   `tape-out`、`Brockman`、`Hock Tan` 全部 0 次命中。
4. **沒有猜測的識別碼**：node id 64506 印在頁面自己的 `href="/node/64506/pdf"` 上；
   三個 `openai.com/index` 的 slug 全部來自官方 feed 的 `<link>`；
   Q3 那個網址是 Broadcom 自家 IR RSS 的 `<link>`。
   沒有任何事實追到新聞媒體、整合站、律師事務所部落格或搜尋摘要；
   TechCrunch／Bloomberg／Seeking Alpha 與「比 Nvidia GPU 便宜 50%」都正確隔離在
   `unverified_or_excluded` 裡，理由也對。
5. Broadcom 的 Q3 FY2026 財報稿（datePublished `2026-09-02T16:15:47-0400`）查核者抓過並確認：
   **`Jalape` 0 次、`OpenAI` 0 次**——`unverified_or_excluded` 第 5 條的排除成立，維持。
6. **倉庫面的主張全部經查核者驗證**：`apps/api/app/guides/content` 剛好 970 個內容包、
   40 個 `ai-news-*`、**0 個 `tech-news-*`**；對所有內容包 grep `broadcom|jalape` 零命中；
   `ai-news-siri-ai-ios-27-20260914` 的 display_order 是 148；
   `ai-news-2026-january-september-index` 的 display_order 是 141、
   zh-TW title 是「2026 年 AI 新聞總整理：1 月 1 日至 9 月 14 日的重點與生活應用」、
   **沒有頂層 `news_date`**；`candidates-tech-and-ai.md` 第 136 與 314 行確實重複列了同一個事件。
   **「寫在 AI 垂直、劃掉 tech 那一列」的決定與整份 `corrections_to_candidate_list` 都成立。**

### 額外：規格合規

研究紀錄缺少三個 BRIEF 規定的頂層欄位：`title`、`hero_label`、`diagram`。撰稿代理要補齊。

---
## ai-news-openai-funding-20260331

OpenAI 2026-03-31 宣布完成 1,220 億美元募資。研究紀錄 29 條事實，查核確認 25 條。
查核者的評語是「這是我查過最乾淨的一份研究紀錄」——沒有捏造的網址、沒有猜測的識別碼、
沒有用媒體頂替一手來源、沒有日期混淆、每一個廠商指標都已經標成 `is_vendor_claim: true`。
需要處理的是**兩處用字、一個數錯的段落數、一份要重建的 sources，以及一個要由人決定的封存依賴**。
**查核檔用 0-based 編號**（`verified_facts[20]` ＝紀錄第 21 條）。

### must_fix

1. 紀錄第 21 條寫「官方頁的正文在 2026-04-05 與 2026-09-15 兩個封存版之間沒有變動：
   **26 個 body paragraph**、逐字相同」。**實質正確，段數錯了。**
   查核者自己跑 `<p>` 層級的差異比對：文章文字確實相同，只有導覽版面與三張
   「Keep reading」卡片不同（4 月版是 Apr 2／Mar 24／Mar 19 2026，9 月版是 Sep 9／Sep 8／Sep 8 2026）。
   但 9 月那份有 **28 個 `<p>`**，其中 1 個是導覽 class 的片段、3 個是 Keep-reading 卡片，
   **剩下 24 個才是文章段落**（而且這 24 個已經含了四個小節標題
   `Deep conviction across global capital`、`Leadership across consumer and enterprise`、
   `Compute is a strategic advantage`、`Building an AI superapp`）。
   **怎麼讀都得不到 26。改寫成 24，或乾脆不寫段數。**
2. 紀錄第 8 條結尾寫「It also claims it is growing revenue four times faster than **Alphabet and Meta** did.」
   **原文是**：
   `At this stage, we are growing revenue four times faster than the companies who defined the Internet
   and mobile eras, **including** Alphabet and Meta.`
   Alphabet 與 Meta 是一個更大比較集合裡**舉的例子**，不是對標基準。
   照現在的寫法會把 OpenAI 的說法窄化成一對一比較，**而 OpenAI 沒有那樣說**；
   而且研究者自己附的 `verbatim_quote` 根本沒有涵蓋那一句（引文在它之前就結束了）。
   **改寫成照原文的「包括 Alphabet 與 Meta 在內的、定義了網際網路與行動時代的公司」。**
3. 紀錄第 10 條寫「OpenAI **列出**其他參與機構為 Altimeter、Appaloosa LP、ARK Invest……」
   （19 個名字）。**19 個名字逐一核對全對，但「列出為」不成立**：
   原文是 `There was also significant participation from a diverse set of global institutions
   **including** …`。`including` 明示這不是窮舉。
   **改寫成「包括……在內」**。另外這一條的 `verbatim_quote` 是空的——
   偏偏這是最需要引文的一條，要補上。
4. 紀錄第 13 條寫循環信貸額度「supported by a syndicate of JPMorgan Chase, Citi, Goldman Sachs,
   Morgan Stanley, Wells Fargo, Mizuho, Royal Bank of Canada, SMBC, UBS, HSBC and Santander」。
   **原文是 `The facility is supported by a global syndicate **including** JPMorgan Chase, …`**，
   同樣是非窮舉；而且研究者的引文用 `...` 把那個字省掉了，**讓這個缺漏看不出來**。
   11 個名字、約 47 億美元與 `remains undrawn at close` 都確認無誤。**把「including」的意思寫回去。**
5. **`sourcing_verdict: "full"` 站不住，需要人來裁決。**
   查核者獨立在兩條不同的出口路徑上重新確認 `openai.com/index/*` 都是 403，
   也確認封存是真的（封存頁的 `og:description` 與查核者直接從 openai.com 抓到的 RSS **逐位元相同**；
   byline 與 feed 的 pubDate 相符；自己做的四月對九月比對顯示沒有改寫）。**沒有任何東西是捏造的。**
   但 BRIEF 明文：「查到的事實如果只存在於被擋的頁面後面，那就不寫。」
   **每一個面向讀者的正文數字**——9 億週活躍使用者、5,000 萬訂閱者、每月 20 億美元營收、
   47 億美元循環額度、來自個人投資人的逾 30 億美元、superapp、8,520 億美元投後估值——
   **在這份紀錄裡都只存在於 `web.archive.org`**。
   這需要編輯簽核，不是研究者自評。（研究者自己在 notes 裡提供了降級路徑，這一點值得肯定。）

### must_add

- **價值最高、而且部分解決了封存問題的一項**：SoftBank 2026-02-27 的新聞稿寫明這一輪的
  **投前估值是 7,300 億美元**。**730 + 122 = 852。**
  也就是說 OpenAI 的 8,520 億美元投後估值由**第二個、完全沒有被擋的一手來源**佐證，
  而 1,220 億美元本身就在 OpenAI 自己的 RSS 描述裡（查核者直接從 openai.com 抓到）。
  **兩個頭條數字因此完全不依賴 Wayback。** 研究者讀過那一頁卻沒注意到。
- **直接關係到 IPO 那一段，也被漏掉**：SoftBank 2026-02-27 寫明取得的證券是
  `Preferred Shares (automatically convertible into common shares of OpenAI upon an IPO or related
  listing transaction)`。
  研究紀錄的 `not_said` 第 9 條說「OpenAI 從未提到 IPO」——**對 OpenAI 那篇而言是真的，
  但一手的上市掛鉤確實存在於 SoftBank 的申報裡。**
- **SoftBank 2026-02-27 其他被漏掉的內容**：SBG 自 2024 年 9 月起已透過 SoftBank Vision Fund 2
  累計投資 346 億美元（34.6 + 30.0 = 64.6，與紀錄裡的累計數字吻合）；
  SBG 董事會決議日 2026-02-20（日本時間）；價金初期以過渡貸款支應；
  LTV 政策平時低於 25%、緊急時 35%；OpenAI Group PBC 成立於 2018 年 11 月、
  2025 年 10 月改組為 PBC、Sam Altman 為執行長、位於舊金山；採 FVTPL 公允價值會計；
  另有孫正義與 Sam Altman 的引言。
- **交割可因上市而提前的註腳，2026-02-27 那份就有**
  （`*4 Closing dates may be subject to acceleration in the event of a public listing of OpenAI shares`），
  不是只有研究者放的 2026-07-01 那份才有。
- **SoftBank 2026-03-27 被漏掉的內容**：過渡融資的貸與人是 JPMorgan Chase、Goldman Sachs、
  Mizuho Bank、Sumitomo Mitsui Banking Corporation 與 MUFG Bank；到期日 2027-03-25；
  擔保品 None；分階段償還。
  **其中四家銀行同時出現在 OpenAI 自己的循環額度銀行團裡**——這是一個真正有意思的一手重疊。
- **Amazon 2026-02-27 被漏掉的四項，全部有日期、可查核**：
  OpenAI 與 Amazon 將開發客製化模型以支援 Amazon 面向顧客的應用；
  Trainium 承諾涵蓋 Trainium3 與 Trainium4；
  Trainium4 `expected to begin delivery in 2027`；
  Stateful Runtime Environment 在該日時 `expected to launch in the next few months`。
- **OpenAI 自己那篇裡被漏掉的一段，講這筆錢已經做出了什麼**：
  `We recently launched GPT-5.4, our most capable model yet, with meaningful gains in intelligence and
  workflow performance. We expanded Codex into a flagship coding agent. We pushed forward on memory,
  search, personalization, and multimodal interaction. We also expanded into areas like health,
  scientific discovery, and commerce.`
  另外 Nvidia 那一段漏掉了 `and with this round we are deepening that partnership as we scale`。
- **一個 BRIEF 特別警告過、研究者沒標的字元陷阱**：該頁兩處的 `GPT‑5.4` 用的是
  **U+2011 不斷行連字號**。用 ASCII 連字號去 grep 封存檔會是零命中。
- **NVIDIA 的排除經查核者重新確認**：`nvidianews.nvidia.com/releases.xml` 現在只有 4 筆、
  最舊回到 2026-09-01（研究者當時看到的是 2026-08-31，視窗又往前滾了），
  限定網域搜尋 nvidianews／blogs.nvidia／investor.nvidia 只找到 2025 年 9 月的 10 GW 合作案。
  **不可寫任何 NVIDIA 的金額。**
- **「第三批尚未發生」成立**：查核者抓了 SoftBank 的新聞稿列表（HTTP 200），
  它跑到 2026-09-09，**2026-07-01 之後沒有第三批、也沒有提前交割的公告**。
- **ARK 的處理維持**：查核者在 ark-funds.com 上找到的唯一一手頁面是
  ARK Venture Fund（ARKVX），一檔持有未上市公司的封閉式間隔基金，**不是 ETF**。
  那是線索不是確認；若要提 ARK，**停在「OpenAI 表示」、不寫任何代號**。

### live_data_warnings

- **feed 的筆數與月分計數**：`sourcing_notes` 寫「1,194 筆」「9 月……現在是 34 則」，
  查核者數到 **1,195 筆、9 月 35 則**，而且最新一筆已經變成
  〈Helping older adults use AI in everyday life〉（Wed, 16 Sep 2026 16:00:00 GMT），
  不是〈Reimagining advertising with AI〉（13:00 GMT）。
  對文章無害，**但 `corrections_to_candidate_list` 第 2、3 條寫下的數字任何人一重跑就是錯的**。不入稿。
- **`openai.com/sitemap.xml/company/` 的 261 個 `<url>` 與該頁的
  `<lastmod>2026-08-13T23:42:20.362Z</lastmod>`** 都是活值。
  研究者判定那是網站樣板重建、不是內容改寫——**這個判斷經查核者的段落比對支持，維持**，
  但時間戳本身不要當成更新日印出來。
- **Wayback 封存本身是快照**：`20260915092422`（385,815 bytes）與
  `20260405075032`（321,567 bytes）都是查核當天 Archive 持有的版本。
- **所有 OpenAI 自報指標都是時點值，一律寫「OpenAI 表示」**：
  9 億以上週活躍使用者、5,000 萬以上訂閱者、每月 20 億美元營收、
  每分鐘逾 150 億 token、Codex 逾 200 萬週活躍使用者（三個月成長 5 倍、月增逾 70%）、
  6 倍／4 倍的 App 比較、「搜尋用量一年內將近三倍」、
  「廣告試辦不到六週達到逾 1 億美元 ARR」、「企業佔營收逾 40%」。
  `must_not_write` 第 9 條已經正確列出這一串，**維持**。
- **「1,220 億美元」是承諾資本（committed capital），不是到帳金額**；
  SoftBank 自己的申報顯示分三批 100 億美元（2026-04-01、2026-07-01、計畫中的 2026-10-01），
  Amazon 自己的稿把 500 億拆成現在 150 億、之後 350 億
  `when certain conditions are met`（且不說明條件）。
  **這是整篇最有價值的識讀點，而且完全是一手的。**
- **第三批與 Amazon 第二批的狀態會變**：`not_said` 第 16 條正確寫明，
  沒有任何一手來源確認 Amazon 的 350 億在 2026-09-16 時是否已支付。

### source_list_fix

**需要重建，而且需要一個人的裁決。**

1. **`sources[0]` = `https://openai.com/index/accelerating-the-next-phase-ai/` 帶著
   `checked_on: 2026-09-16`，但它在本容器回 HTTP 403**（9,812 bytes 的 Cloudflare 阻擋頁），
   用 WebFetch 走第二條出口也是 403；`.../index.txt`、`/news/`、`/llms.txt`
   與官方 zh-Hant 版 `/zh-Hant/index/accelerating-the-next-phase-ai/` 同樣 403，
   `cdn.openai.com/index/accelerating-the-next-phase-ai.html` 回 404。
   **沒有人在 2026-09-16 讀過它。**
2. **29 條事實裡有 25 條掛在 `sources[]` 以外的網址**：
   第 4–20 條 → `web.archive.org/web/20260915092422/...`；第 21 條 → `.../20260405075032/...`；
   第 1、2、22、29 條 → `https://openai.com/news/rss.xml`；
   第 3 條 → `https://openai.com/sitemap.xml/company/`；
   第 24 條 → `https://group.softbank/en/news/press/20260327`（過渡融資）；
   第 26 條 → `https://group.softbank/en/news/press/20260701`（第二批）。
   **後兩條特別要注意**：文章若要寫過渡融資或 7 月那一批，**sources 必須重建**——
   最可能的做法是**把 2026-04-01 那份換成 2026-02-27 那份**，因為 2026-02-27 那份已經含了整張分批表
   （而且還多給了投前估值 7,300 億美元、優先股轉換條款與累計投資額）。
3. **Wayback 依賴要編輯簽核**（見 must_fix 5）。
   研究紀錄的 `note_on_fact_urls` 說內容包的 sources 要寫 canonical 網址、不寫封存網址——
   **那個 canonical 網址是真的（由 OpenAI 自家 sitemap 的 `<loc>` 與 RSS 的 guid 兩處確認），
   但沒有人讀過它。** 兩種處理方式擇一，不能一邊引封存一邊宣稱讀的是官方頁。
4. **四條 sources 的網址本身全部有一手憑證**，這一點查核者特別確認：
   帶尾斜線的 canonical 由 OpenAI 自家 sitemap 的 `<loc>` 背書、
   不帶斜線的形式由 RSS 的 guid 背書、四個 SoftBank 路徑由
   `group.softbank/en/news/press` 列表頁上的真實 href 背書、
   Amazon 那個網址由它自己的 `rel=canonical` 背書。**沒有猜測的識別碼。**
5. **沒有任何一條事實追到新聞媒體、整合站、律師事務所部落格或搜尋摘要。**
   Bloomberg 的 NVIDIA 300 億美元、Amazon 350 億的條件（IPO 或 AGI）、
   「史上最大募資」、TechCrunch 的「retail investors」用字，全部正確隔離在
   `unverified_or_excluded` 裡，理由也對。

### 額外：規格合規

研究紀錄缺少三個 BRIEF 規定的頂層欄位：`title`、`hero_label`、`diagram`。撰稿代理要補齊。

---
## ai-news-openai-s1-20260608

OpenAI 2026-06-08 確認向 SEC 保密遞交 S-1 草稿。研究紀錄 30 條事實，查核確認 25 條。
**本篇查核檔用 1-based 編號，與研究紀錄位置一致。**
`sourcing_verdict` 已經誠實寫成 `partial`，`not_said`（12 條）與 `unverified_or_excluded`（10 條）
經查核者逐條攻擊後找不到實質缺口。

### must_fix

1. 紀錄第 11 條寫「這 46 筆分屬 **30 個**申報人」。**是 41 個，不是 30。**
   `efts.sec.gov` 的 `entity_filter` 聚合**最多只回 30 個 bucket**，
   研究者把一個被截斷的聚合當成完整名單。把 46 筆命中的 `display_names` 全部展開會得到 41 個申報人
   （2024-03-22 有一筆是兩個共同申報人：MAV OpenAI Fund I 與 QP-MAV OpenAI Fund I）。
   聚合裡看不到的申報人包括 OpenAI Startup Fund II, L.P.、SPV I、SPV V、SPV VI、
   OurCrowd (Investment in G-new OpenAI) L.P.、OpenAI Tender Fund I Sep 2025、
   OpenAI-01 a Series of OpenAI Opp Fund LLC、OpenAI-s a Series of GatePass Ventures I LLC、
   Starbridge OpenAI 1 Jul 2025、VM OpenAI 1 a Series of PCXS LLC。
   **第 11 條其餘部分（全部是第三方創投基金或 SPV、名單裡沒有 OpenAI 公司本身）查核者驗過，成立。**
2. 紀錄第 30 條寫 SEC 新聞稿 RSS 的 25 筆「只涵蓋 **2026-09-03 至 2026-09-16**」。
   **實際是 2026-07-08 到 2026-09-16——超過兩個月，不是兩週。**
   最舊一筆是 `Wed, 08 Jul 2026 13:54:26 -0400`〈SEC to Host Virtual Roundtable on Modernizing IPOs
   and Expanding Access to Public Markets〉。
   研究者的結論（視窗不含 6 月，所以證明不了 6 月沒有新聞稿）**仍然成立，
   但這個區間寫錯了，不可照抄進文章**。查核者另外確認那份 feed 的內容裡
   沒有 `OpenAI`、也沒有 `draft registration`。
3. `editorial_brief` 把紀錄第 10 條轉述成「這 46 筆**全部是 Form D**」。
   **46 筆裡有 40 筆 `file_type` 是 D、6 筆是 D/A（Form D 的修正）。**
   `form_filter` 聚合是按母表單分組的，所以它才顯示 `D: 46`。
   **第 10 條對那個聚合本身的描述是準確的，錯的是 `editorial_brief` 的轉述。**
   **正確寫法**：「46 筆全部是 Form D 或其修正（40 筆 Form D、6 筆 Form D/A）。」
4. 紀錄第 4 條寫 2026-09-16 取得 feed 時有 **1,194 筆 `<item>`**。
   查核者在同日 16:12 UTC 數到 **1,195 筆**。這是活 feed 的當日漂移、不是抄錯，
   **但正是 BRIEF 禁止呈現給讀者的那種只增不減的數字。**
   **不准入稿**，研究紀錄本身也應改寫成「逾 1,100 筆、最新一筆的 pubDate 等於查核日」。
   第 4 條的另外兩個判準（最新一筆 2026-09-16、feed 是活的）查核者確認無誤。
5. 紀錄第 15 條的後半（Cerebras Systems Inc. 2026-05-04 的 S-1/A、file number **333-295145**）
   掛在 `https://efts.sec.gov/LATEST/search-index?q=%22OpenAI%22&forms=DRS`。
   **那個查詢限定 `forms=DRS`，回應裡只有 DRS 與 DRS/A 的申報，而且完全沒有 file-number 欄位。**
   這條事實照被引用的那個網址追不到，依 BRIEF 就是沒有來源。
   （事實本身為真，查核者在 `https://data.sec.gov/submissions/CIK0002021728.json`（HTTP 200）上獨立驗過。）
   **第 15 條的前半（Cerebras Systems Inc.、CIK 0002021728、2026-03-31 的 DRS/A、
   出現在那個查詢裡）確認成立。** 後半要換來源或刪掉。
6. 紀錄第 18 條把 Pub. L. 112-106 稱為「JOBS Act」、Pub. L. 114-94 稱為「FAST Act」，
   並掛在 govinfo 的 §77f 頁。
   **那一頁完全沒有 `JOBS`、`FAST`、`Jumpstart` 或 `Fixing America` 這些字串**（查核者全文搜過）。
   它只給了 `Pub. L. 112-106, title I, §106(a), Apr. 5, 2012, 126 Stat. 312` 與
   `Pub. L. 114-94, div. G, title LXXI, §§71001, 71002, Dec. 4, 2015`，
   以及把 `21 days` 換成 `15 days` 的修正註記——這些查核者逐字確認無誤。
   **那兩個簡稱要改掛 91 FR 30086**，該文件確實寫明 Public Law 112-106 是 JOBS Act、
   Public Law 114-94 是 Fixing America's Surface Transportation（"FAST"）Act。
7. **三個識別碼沒有記下取得方式**：govinfo 的 USCODE 網址、
   `uscode.house.gov` 的 granuleid 網址、以及《聯邦公報》文件編號 2026-10222。
   三個都是可以照樣式拼出來的識別碼，而研究紀錄沒說是哪一次官方檢索產生的。
   查核者三個都抓過、都解析到宣稱的文件（§77f、§77f prelim、91 FR 30086），
   **所以不是捏造**——但 BRIEF 的規則是「猜對也一樣算猜」，**研究紀錄要補上取得方式**。
   （對照之下，研究者確實寫了 `openai.com/sitemap.xml/company/` 與《聯邦公報》`raw_text_url`
   的來源，查核者也驗過兩者：前者列在 `https://openai.com/sitemap.xml` 的 sitemapindex 裡，
   後者是 API 回傳的 `raw_text_url` 欄位。）

### must_add

- **一條更好的一手路徑，研究者漏了**：同一份《聯邦公報》文件在 GPO 自己的網站上可讀——
  `https://www.govinfo.gov/content/pkg/FR-2026-05-21/pdf/2026-10222.pdf`（HTTP 200），
  而且它是 FR API 回傳的 `pdf_url`、不是拼出來的；
  相對地 `federalregister.gov` 的人看的 HTML 頁會 302 導到 `unblock.federalregister.gov`。
  **建議把 govinfo 這個網址放進 `sources[]`，取代或並列現在的 raw text 網址。**
- **研究紀錄漏掉的一個日期區別**：該提案規則由委員會於 **2026-05-19** 通過
  （`By the Commission. Dated: May 19, 2026. Vanessa A. Countryman, Secretary.`），
  於 **2026-05-21** 刊登於《聯邦公報》。
  **文章不可寫成「SEC 在 5 月 21 日提出」。**
- **Cerebras 這個對照組的正確來源與更完整的軌跡**：
  `https://data.sec.gov/submissions/CIK0002021728.json`（HTTP 200）顯示
  DRS 2025-12-22、DRS/A 2026-03-31（兩筆都在 file number **377-08857** 底下），
  接著 S-1 2026-04-17、S-1/A 2026-05-04、S-1/A 2026-05-11、
  8-A12B 2026-05-11（001-43284）、424B4 2026-05-14（S-1 系列都在 **333-295145** 底下）；
  tickers `['CBRS']`、exchanges `['Nasdaq']`。
  **保密期間的 377- 字頭在公開申報後變成 333- 字頭**——
  這比「別家公司的 DRS 查得到」更能說明保密轉公開這個過程，正是本篇最有價值的一段。
- **一個要寫進研究紀錄、供後續批次參考的方法論陷阱**：
  `efts.sec.gov` 的 `entity_filter` **最多回 30 個 bucket**；
  這次查詢的 `sic_filter` 是空陣列；`form_filter` 按母表單分組，所以 D/A 會被併進 D。
  **任何「有幾個申報人」或「全部都是某某表單」的結論，都必須展開命中逐筆計算，不可從聚合上讀。**
- **15 U.S.C. §77f(e)(1) 有一句研究者沒記、文章可以用的**：
  一個發行人在保密遞交登記說明書時是新興成長公司、之後喪失資格的，
  就本項而言仍繼續被視為 EGC，直到其首次公開發行完成或喪失資格屆滿一年之較早者為止。
  **這支持文章「不替 OpenAI 歸類」的立場**——EGC 身分是以遞件當下判斷的。
- **研究者實際抓過的那份 SEC 新聞稿 feed 裡，有一則同期、切題卻沒被記下的官方項目**：
  2026-07-08〈SEC to Host Virtual Roundtable on Modernizing IPOs and Expanding Access to Public Markets〉。
  它與 OpenAI 無關，**但若文章要提到 SEC 在 2026 年對 IPO 流程的動作，這是那份 feed 裡唯一的一手線索。**
- **查核者用更寬的關鍵字重跑了「沒有後續」這個檢查，結論更強**：
  用 S-1、SEC、prospectus、road show、public markets、restructur、PBC、Foundation、
  valuation、investor、equity、capital 掃過 feed 裡每一則 2026 年的項目，
  **2026-06-08 那一則是唯一命中 S-1 的**，之後也沒有任何關於這次遞件、上市或公開申報的 OpenAI 公告。
  **紀錄第 5 條的結論在更嚴的測試下成立。**
- **一個可以放心打字的細節**：那則 OpenAI 項目的標題與描述**全部是純 ASCII**（查核者逐字元檢查），
  沒有 U+2011 或不斷行空格的陷阱，
  所以 `Confidential submission of draft S-1 to the SEC` 可以直接打出來。

### live_data_warnings

- **OpenAI feed 的筆數**：紀錄 1,194 筆、查核者 1,195 筆，同日漂移。不入稿。
  `corrections_to_candidate_list` 第 3 條自己就正確地寫了「這類數字不該固定寫在文件裡」，**照做**。
- **EDGAR 的每一個計數都是活值**：`entityName=OpenAI` 的 46 筆申報（`hits.total.value = 46`）、
  41 個申報人、40 筆 D／6 筆 D/A、限定 2026-06-01 至 2026-09-16 的 2 筆、
  `q="OpenAI"&forms=DRS` 的 121 筆。**每一個都會隨新申報增加**，
  引用時必須綁上「2026 年 9 月 16 日查詢時」。
- **`https://www.sec.gov/news/pressreleases.rss` 只保留 25 筆**（查核當天涵蓋 2026-07-08 到 2026-09-16），
  這個視窗會往前滾（紀錄第 30 條的區間本身也寫錯，見 must_fix 2）。
  **它不能拿來證明任何較早日期沒有新聞稿**，紀錄自己已正確警告，維持。
- **`openai.com/sitemap.xml/company/` 的 261 個 `<url>`、34 個不同 lastmod 日期
  （2026-08-31 有 26 筆、2026-08-25 有 50 筆、2026-09-16 有 33 筆）與該頁的
  `<lastmod>2026-08-31T19:59:25.610Z</lastmod>`** 全部是活值。
  紀錄第 9 條與 `unverified_or_excluded` 第 4 條用它們來證明「不能推論成內容被改寫」——
  **推論正確，但這些計數本身不要印出來。**
- **`ecfr.gov` 的 versioner API 有日期上限**（不能超過該 title 的最新發行日，查核當天是 2026-09-14），
  而且**不送壓縮的 Accept-Encoding 會回 406**（查核者確認：加 `--compressed` 回 200，不加回 406）。
  17 CFR 239.11 的條文本身是現行版的快照。
- 《聯邦公報》全文檢索「2026-01-01 以後、含 OpenAI」的結果是 2 筆（`count=2`，查核者確認），
  這也是會變的查詢結果。

### source_list_fix

4 條，在上限內，**四條全部可達且是宣稱的那份文件**（查核者逐一驗過：
RSS 726,611 bytes、頻道標題 `OpenAI News`；EDGAR FTS 回應 32,681 bytes、
`hits.total.value = 46`；govinfo §77f 頁 24,007 bytes、標題 `Sec. 77f - Registration of securities`；
《聯邦公報》raw text 657,682 bytes、91 FR 30086 全文）。但有三件事：

1. **30 條事實裡有 12 條掛在 `sources[]` 以外的網址**：
   第 8、9 條 → `openai.com/sitemap.xml/company/`；
   第 12 條 → `efts...&forms=DRS`；第 13 條 → `efts...&dateRange=custom&startdt=2026-06-01&enddt=2026-09-16`；
   第 14 條 → `data.sec.gov/submissions/CIK0001877240.json`；
   第 15 條 → `efts...q=%22OpenAI%22&forms=DRS`；
   第 20 條 → `uscode.house.gov/view.xhtml?req=granuleid:...`；
   第 21 條 → `federalregister.gov/api/v1/documents/2026-10222.json`；
   第 28 條 → `ecfr.gov/api/versioner/...`；
   第 29 條 → `federalregister.gov/api/v1/documents.json?...`；
   第 30 條 → `sec.gov/news/pressreleases.rss`。
   **每一條要用就得換進四條裡**，尤其第 28 條（Form S-1 的法規定義，17 CFR 239.11）
   是文章第二層論述的骨幹。
2. **`sources[0]` 是 feed 網址、`sources[1]` 是搜尋 API 網址**，兩者都與 BRIEF
   「sources 放的是文章頁的網址，不是 feed 的網址」抵觸。
   查核者確認這個 feed **是被迫的、不是偷懶**：文章頁與它的 zh-Hant、ja-JP 變體
   全部回 HTTP 403（Cloudflare 挑戰頁、`cf-mitigated: challenge`），
   **規格要求的那個作法在這一篇根本做不到**。研究者把衝突標出來交編輯裁量，是正確處理。
   同樣 403 而被正確排除的還有兩份 Corp Fin 官方說明頁
   （`voluntary-submission-draft-registration-statements-faqs` 與
   `draft-registration-statement-processing-procedures-expanded`）。
3. **建議加入的官方頁**：`https://www.govinfo.gov/content/pkg/FR-2026-05-21/pdf/2026-10222.pdf`
   （GPO 自家版本，見 must_add）與
   `https://data.sec.gov/submissions/CIK0002021728.json`（Cerebras 對照組的正確來源）。
4. **沒有任何一條事實追到新聞媒體、整合站、律師事務所部落格或搜尋摘要**；
   全部落在 openai.com、efts.sec.gov、data.sec.gov、govinfo.gov、uscode.house.gov、
   federalregister.gov、ecfr.gov 或 sec.gov 的官方管道上。
   廠商宣稱標記正確（第 3 條標了 `is_vendor_claim`）；
   第 6、7 條標成廠商宣稱其實是對 feed 的客觀觀察，**過於保守但無害**。

### 額外：規格合規

研究紀錄缺少四個 BRIEF 規定的頂層欄位：`checked_on`、`title`、`hero_label`、`diagram`。撰稿代理要補齊。

---
## 跨篇：這個垂直重複出現的錯誤，寫稿時逐條自檢

以下每一條都在 AI 垂直的多篇裡出現過，寫成可以直接照做的規則：

1. **不要把任何 feed、sitemap、搜尋 API 或註冊表的筆數寫進文章或研究紀錄。**
   12 篇裡有 9 篇把 `openai.com/news/rss.xml` 的 item 數當事實記下來，
   而且 9 篇記的數字彼此不同（1,193／1,194／1,195／1,196），全都在 **2026-09-16 同一天內**漂移。
   同類的還有 sitemap 的 `<url>` 數、EDGAR 命中數、簽署方人數、Astral blog feed 的 39 筆。
   要證明「這個 feed 是活的」就寫「最新一筆的 pubDate 等於查核日」，不要寫筆數。
2. **不要把「最新一筆是什麼」寫成事實。** 三篇各自把 OpenAI feed 當天的最新項目寫成
   〈Reimagining advertising with AI〉，而查核者抓到的是〈Helping older adults use AI in everyday life〉。
   三小時之差就換人。
3. **`sitemap` 的 `<lastmod>` 不是發布日、不是更新日、也不是事件日。**
   五篇踩到。判斷它是不是真的內容更動，要靠**逐版比對**（B8 就是這樣證明改動在 2026-09-11），
   不要靠「同日有幾筆」這種統計直覺——B8 那個直覺剛好是反的。
   同理，PDF 的 `CreationDate`／`ModDate`、blob 的 `Last-Modified`、
   文件站頁尾的 `Last updated` 都是產製或建置時間戳。
4. **`sources[]` 幾乎每一篇都不合格：事實掛在清單以外的網址。**
   12 篇裡有 10 篇有這個問題，最嚴重的 `gpt-live-1-api` 有 33 條事實掛在 12 個未列網址上，
   `openai-astral` 有 21 條掛在 18 個未列網址上。
   `[NOT IN sources]` 這種標註**不能取代改 `sources[]`**。
   開稿前先決定文章要寫哪些事實，再**倒過來**組四條來源；沒進四條的事實就不寫。
5. **`openai.com/index/*` 全站 403，不可以把沒讀到的網址列進 `sources[]` 還附 `checked_on`。**
   三篇（`chatgpt-financial-services`、`chatgpt-storage-scale`、`openai-funding`）
   的 `sources[0]` 就是這種寫法。這會讓整條證據鏈失真。
   **同一個決定要一次做完**：要嘛編輯明白裁量接受 `web.archive.org` 的逐字封存
   （並把封存網址連同自己的 `checked_on` 放進 `sources[]`、在正文說明依據），
   要嘛把只存在於被擋頁面後的事實整批不寫、把 `sourcing_verdict` 降級。
   **不能一邊引封存、一邊宣稱讀的是官方頁。**
6. **`sourcing_verdict: "full"` 在本垂直被系統性高估。**
   `chatgpt-financial-services`、`chatgpt-storage-scale`、`openai-funding`
   的正文全部來自封存；`openai-broadcom-chip` 只有一個可讀的一手文章頁。
   判 `full` 之前先問：**主題的核心陳述有沒有一條是我自己在官方網址上讀到的？**
7. **`verbatim_quote` 不可以是拼裝品。** 六篇踩到，型態有四種：
   用 ` / ` 串條列（broadcom 第 6 條、nvidia-hugging-face 第 15 條）、
   用刪節號把不相鄰甚至**順序相反**的兩句接起來（nvidia-hugging-face 第 8 條）、
   把換行縮排壓掉重排（chatgpt-ads 第 41 條）、
   以及從 `.md` 版抓到漏出 JSX 的字串（gpt-live-1-api 第 45 條）。
   **引文欄位必須是可以原樣搜尋得到的字串**；做不到就標成「讀到的值」，不要標成引文。
8. **不可以把句子截短、補句號，或刪掉限定詞。** 這是本垂直最常見的實質錯誤：
   `frontier-governance` 第 13 條刪掉 `where appropriate`、第 51 條刪掉
   `if the model is amongst their respective most capable models`；
   `chatgpt-storage-scale` 第 26 條在句中插句號、第 30 條截斷引號內的句子；
   `nvidia-hugging-face` 第 29 條刪掉 `wrongly`、第 10 條把 `including` 當成窮舉；
   `openai-funding` 第 10、13 條把 `including` 當成窮舉；
   `chatgpt-ads` 第 37 條把非窮舉的指標清單寫成完整清單。
   **刪一個限定詞就是改變主張。看到 `including`、`where appropriate`、`may`、`if`、
   `substantially`、`wrongly` 一律原樣保留。**
9. **不可以把「全稱」寫成事實。** `frontier-governance` 第 12 條的「整份文件只有這兩個數量」
   被一口氣舉了八個反例，而且對應的 `not_said` 更糟——它會讓撰稿者相信 2021 這個基準年不存在。
   `chatgpt-ads` 第 16 條的「恰好三個」、`gpt-live-1-api` 第 7 條的「Realtime 分類下只有一個」同型。
   **「只有」「恰好」「從未」「全部」出現時，先反問是不是只查了一個聚合或一個頁面。**
   （`openai-s1` 第 11 條就是把 EDGAR 只回 30 個 bucket 的**截斷聚合**當成完整名單。）
10. **負面結論要寫清楚查法與範圍，不可寫成「官方確認沒有」。**
    「Hugging Face 沒有公告」「part two 尚未發布」「6 月沒有個人化公告」「SEC 沒有新聞稿」
    都是從某個視窗推論的。**寫成「以某某清單查核到 2026-09-16 未見」**，
    並把視窗本身寫對——`openai-s1` 第 30 條與 `gpt-55-instant` 的 6 月理由都是視窗描述錯誤。
11. **廠商宣稱的標記系統性偏鬆。** `openai-broadcom-chip` 有五條該標 `true` 的標成 `false`
    （含「800 million weekly active users」這種未經查核的自報使用者數，
    以及發行人自己在前瞻性陳述裡免責的部署時程）；
    `chatgpt-storage-scale` 第 13 條把「我們未來會再發一篇」標成非廠商宣稱；
    `chatgpt-ads` 第 18、32 條把 OpenAI 描述自家行為的句子標成非廠商宣稱。
    **判準**：外部無法觀察、由公司自報、關於未來、或關於自己的功勞與流程——一律是廠商宣稱。
12. **不可以把兩個東西的歸屬接在一起。**
    `chatgpt-ads` 第 9 條把 RSS 的「self-serve」掛到沒有那個字的文件頁；
    `gpt-live-1-api` 第 17 條把 `gpt-6-astra` 的價格說成 GPT-Live 的後端價格；
    `frontier-governance` 第 38 條把加州法條寫成 FGF 那句話的出處；
    `nvidia-hugging-face` 第 15 條把一封沒有署名的信認定成 Huang 共同署名的那一封。
    **一句話要掛在真的印著它的那一頁上；掛不上就拆成兩條事實。**
13. **廠商自己的文件會用兩個名字指同一件事，不要合併也不要「訂正」。**
    Gemini 的評測 PDF 用 `gemini-3.8-live-preview`、定價頁用 `gemini-3.8-live`；
    Sierra 那個基準在部落格是 `tau-Voice-banking`、在 PDF 是 `tau-cubed-Bench`；
    Broadcom 的 Richard Ho 被介紹成 OpenAI 的人卻說「我們與 OpenAI 研究員密切合作」；
    OpenAI 與 Broadcom 對同一則公告用了兩個不同的標題。**照原樣寫，並指出不一致。**
14. **UTC 與台北時間的跨日要算。** 只有 `chatgpt-ads`（由查核者補上）與
    `openai-broadcom-chip`、`openai-s1` 處理了這件事。
    `ChatGPT Ads expands across Europe` 的 22:00 GMT 在台北已經是隔天早上——
    **每一個要寫進 zh-TW 正文的日期都要換算一次**。
    另注意 OpenAI feed 有 338 筆 pubDate 是 `00:00:00 GMT`，那是佔位值，**日期可用、時刻不可用**。
15. **非 ASCII 字元必須整段複製，不可以重打。**
    `GPT‑5.5`、`GPT‑5.4`、`GPT‑Live‑1` 用的是 U+2011 不斷行連字號；
    Apple Developer 的 `Sign\xa0in\xa0with\xa0Apple` 用不斷行空格；
    `chatgpt-ads` 第 25 條的 `A code's ISO validity…` 用 U+2019。
    用 ASCII 去 grep 會查無此項，而 `check_article.py` 要求 link 的 `text` 等於目標 title。
16. **研究紀錄的 schema 幾乎全垂直不合格。**
    12 篇裡有 **10 篇缺 `title`、`hero_label`、`diagram`**，**5 篇缺 `checked_on`**；
    有寫的那兩篇，`title` 還是占位字串，`chatgpt-financial-services` 的 `hero_label`
    是 13 字（BRIEF 上限 12 字），`gemini-38-live` 的建議是 14 字。
    **撰稿代理必須自己補齊這四個欄位，且 `hero_label` 要數過字數。**
    另外 BRIEF 要求「圖上任何數字都必須出現在文章正文」——
    `chatgpt-financial-services` 的圖解節點「四家資料商直接可用」把非窮舉的清單寫死成四家，
    與同一份紀錄的 `unverified_or_excluded` 第 4 條互相矛盾。
17. **`ai.md` 的垂直規則高於研究紀錄的建議。**
    `chatgpt-financial-services` 的研究紀錄花了整段論證要掛 `finance` 並加投資免責，
    `ai.md` 逐字點名該 slug 判了相反。**AI 篇一律不掛 finance、不加投資免責、只放一般 callout。**
    研究紀錄與規格衝突時，以規格為準，並把衝突記進 `tasks/`，不要自己改規則。
18. **同一批裡的兩篇不要互相重寫。** 本垂直有三組需要明確分工：
    `chatgpt-ads` 與站上既有的 `chatgpt-ads-status`（後者已涵蓋開放地區、方案、標示與量測）；
    `gpt-live-1-api` 與既有的 `ai-news-gpt-live-voice-20260708`（後者最後一節**已經寫過**
    「9 月 10 日 GPT-Live 1 在 API 開放、每分鐘 0.05 美元」）；
    `frontier-governance` 與既有的 `ai-news-eu-transparency-20260802`（同一則執委會新聞稿，
    最多一句話的日期脈絡）。**動筆前讀目標內容包本身，不要只看標題。**
