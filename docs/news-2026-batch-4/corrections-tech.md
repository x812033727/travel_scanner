# 科技（tech）垂直：批次 4 撰稿修正清單

這份檔案把 `docs/news-2026-batch-4/factcheck/tech-news-*.json` 的查核結果，逐篇整理成撰稿代理可以直接照著改的清單。
**對科技垂直的撰稿代理具有拘束力**：研究紀錄（`research/tech-news-*.json`）裡凡是本檔案列為 must_fix 的內容，一律不得照抄；
本檔案說「不要寫」的，就是不要寫。撰稿代理看不到原始來源，紀錄裡留下的錯誤會直接上線。

範圍：13 篇 `tech-news-*`。每篇四段：

- **must_fix** — 被推翻（refuted）或無法追溯（unsupported）的內容，格式是「紀錄寫 X；錯在 Y；改寫成 Z」。
- **must_add** — 查核者找到、但研究紀錄漏掉的實質事實，以及更好的一手來源（附它實際抓到的網址）。
- **live_data_warnings** — 會變動的快照數字（列表筆數、feed 項目數、「最後更新」字串、簽署單位數）。**凡是查核者或研究者自己數出來的數字都要當成可疑。**
- **source_list_fix** — `sources[]` 是否可以照這樣刊出（無法直接取用卻記了 `checked_on` 的網址、事實掛在不在 `sources[]` 的網址、超過 BRIEF 的 4 條上限）。

依 slug 排序。判斷基準是 `BRIEF.md` 與 `tech.md`：只用一手來源、`sources` 2–4 條、每個數字要指得到來源原文、廠商宣稱一律寫成「Apple 表示／NVIDIA 表示／數發部指出」、科技篇不寫購買建議、不加投資免責 callout。

---
## tech-news-apple-eu-business-terms-20260818

查核結果：needs_fixes，41 條確認、2 條推翻、3 條無法追溯。

### must_fix

1. 紀錄的 `sourcing_notes` 寫「Apple Newsroom Atom feed（`https://www.apple.com/newsroom/rss-feed.rss`）只有 20 筆 `<entry>`、最新 2026-09-16，8 月那篇不在窗內，所以改用文章頁的 JSON-LD 取日期」；**那是錯的**——查核者抓到的 20 筆窗口是 2026-08-11T13:59:21Z 到 2026-09-16T13:59:28Z，本篇**就在裡面**，entry 寫 `<updated>2026-08-18T15:59:46.948Z</updated>`、`<category term="UPDATE"/>`、網址完全一致。改寫成：Apple 官方 feed 給的日期是 2026-08-18，而文章頁 JSON-LD 的 `dateModified` 是 2026-08-27，兩者不一致，本文引用的是 2026-09-16 讀到的版本。
2. 紀錄 verified_fact 43 寫「Unlike the Japan/Brazil attachment, the EU attachment adds NO separate payment-processing fee on top of the 20%」；**對照錯行**——Attachment 12（日本、巴西）那筆額外的 "five percent (5%) fee for the App Store's payment processing and related commerce services" 掛在 Section 3.5(C)，也就是 Apple 自己的 in-app purchase（21%），不是掛在 Alternative Payment Processing（Section 3.5(B)，同樣 21%），根本沒有「加在 20% 之上」這個對照對象。而且這是研究者自己做的跨附件比較，不是任何一份文件說的話。**不要寫這個比較**；只能寫「歐盟 Attachment 14 的 Section 3.5 沒有另外的支付處理費」。
3. 紀錄 verified_fact 8（以及 `event_date_basis` 與一條 `unverified_or_excluded`）寫 Newsroom JSON-LD 的 `dateModified` 是 `2026-08-27T14:00:09Z`；**不可重現**——查核者七次抓取有六次拿到 `2026-08-27T13:59:42Z`，同一份文件裡 Organization logo 的 cache-buster 字串也寫 `Thursday, 27-Aug-2026 13:59:42 UTC`，Apple 至少供應兩種 edge 版本。日期 2026-08-27 是穩的，秒級時間戳不是。改寫成「該頁 JSON-LD 的 dateModified 為 2026-08-27」，**不要寫到秒**。
4. 紀錄 verified_fact 32 把「Apple 有稽核權；未付佣金可能導致抵扣其他市場應付款、下架 App、或退出 Apple Developer Program」掛在 `https://developer.apple.com/support/apps-in-the-eu/`；**掛錯頁**——該頁搜尋 audit／offset／removal 只找得到兩條 "Have completed a financial audit by a licensed accountant" 的資格條件。稽核權那句在另一頁 `https://developer.apple.com/support/payment-options-on-the-app-store-in-the-eu/`：「Please note that Apple has audit rights pursuant to the terms and conditions in the Apple Developer Program License Agreement... Failure to pay Apple's commission could result in the offset of proceeds owed to you in other markets, removal of your app from the App Store, or removal from the Apple Developer Program.」只有「每月於次月起 15 日內申報」那一句屬於 apps-in-the-eu。**拆成兩條事實、各自指對的網址。**
5. 紀錄 verified_fact 1 的 `verbatim_quote` 寫 `Changes for apps in the European Union / August 18, 2026`；**那個「 / 」是編輯自己加的**，標題與日期是頁面上兩個相鄰但獨立的元素。兩段字串都真的在頁上，事實成立，但**不要把這個組合字串當成原文引用**。
6. 「Apple 從頭到尾沒提到 DMA」這個說法**不可以寫成全稱命題**。Apple 的開發者公告與 Newsroom 稿確實 0 次提到 Digital Markets Act／DMA／gatekeeper／1925／antitrust／fine，但 Apple 自己的支援頁 `developer.apple.com/support/apps-in-the-eu/` 名列 Digital Markets Act 兩次（2024 年以來的背景、互通性請求程序）。正確寫法：**「Apple 對這次改版的公告沒有提到 DMA，只說是與歐盟執委會密切合作的結果。」** 仍然不可以寫 DMA「要求／迫使／導致」這次改版。

### must_add

- **Apple 兩頁對兒少保護的說法不一致，而且 Newsroom 那版比較寬鬆。** Newsroom 寫 "For users under 18 years old ... must include a parental gate" 與 "Apps in the Kids category ... will not include links to websites"；兩份支援頁寫的是：Kids 類 App「必須把使用替代支付處理的購買流程放在 parental gate 之後，且不得提供 App 外的網站購買」；「未滿 13 歲：替代支付購買須經 parental gate，且不允許 App 外購買提案」；「13 至 17 歲：App 內替代支付與 App 外購買提案兩者都須經 parental gate」。**只寫 Newsroom 的「未滿 18 歲」會低估未滿 13 歲那條規則。** 支援頁另有 Newsroom 省略的範例：「in some storefronts the protections apply to users under 16 (instead of under 13) and 16 to 17 (instead of 13 to 17)」；Apple 沒有說哪些 storefront 用哪個年齡。
- **費率表漏一行。** 10% 那一階不只涵蓋三個計畫的參與者，還涵蓋「首年之後的自動續訂訂閱」。`developer.apple.com/support/apps-in-the-eu/` 原文：「10% - Sales processed via alternative payment processing within the app from participants in the App Store Small Business Program, Mini Apps Partner Program, or Video Partner Program, and sales of auto-renewable subscriptions after their first year.」BRIEF 要求第 2 節結尾放表，這一行要進表。
- 兩頁對 15% 那一列的寫法不同：apps-in-the-eu 寫「15% - Out-of-app offers, excluding transactions from program participants or auto-renewable subscriptions after their first year」；payment-options 只寫「15% - Out-of-app offers.」**表格建在哪一頁就引哪一頁。**
- 資格條件也有分歧：Newsroom 寫「Are a government entity, educational institution, or nonprofit.」兩份支援頁寫「Are a government entity, educational institution, or nonprofit **approved for a fee waiver**.」
- **Core Technology Commission 的涵蓋範圍比紀錄的多。** apps-in-the-eu 列出 5% CTC 涵蓋的三類交易，包含「required to access or download alternative app marketplaces ... including paid subscriptions to access or download app content or catalogs of apps」，以及 link-out 後「made within 7 days of the link tap」的銷售。紀錄的 13、25 兩條只抄了 Newsroom 的一句版本。
- 兩條漏掉的一手事實：歐盟境內適用「Guideline 3.1.3(b) Multiplatform Services」的 App 必須提供 Apple In-App Purchase 和／或 App 內替代支付處理（payment-options 頁）；歐盟的 reader app 可以宣傳 App 外購買提案但不得放可點擊的連結（apps-in-the-eu 頁）。
- Dun & Bradstreet 那一條，Apple 的授權合約有量化門檻：合於 D&B「Global Business Ranking」的 "Low Risk" 或 "Below Average Risk" 級別。這個細節只在授權合約頁，不在公告裡。

### live_data_warnings

- `https://www.apple.com/newsroom/2026/08/apple-announces-changes-for-apps-in-the-european-union/` 是活頁面：JSON-LD `datePublished 2026-08-18`、`dateModified 2026-08-27`，而且同一天有兩個 CDN 版本（162,927 bytes / 162,779 bytes，時間戳差 27 秒）。**只寫日期、不寫秒，並註明是 2026-09-16 讀到的版本。**
- `https://developer.apple.com/support/terms/apple-developer-program-license-agreement/` 的 `Last-Modified` 是 **Thu, 10 Sep 2026 17:29:10 GMT**——具拘束力的條文在 8 月 18 日公告之後被改過。任何 Attachment 14 的引文都要寫「2026 年 9 月 16 日讀取」，不可寫成 8 月 18 日發布時的原文。
- 兩份支援頁的 `Last-Modified` 都是 Tue, 18 Aug 2026 22:12:10 GMT（查核當日）。
- feed 窗口全是滾動視窗，不能拿來證明「沒有」：Apple Developer RSS 142 筆、最新 2026-09-09；Apple Newsroom Atom 只有 20 筆；歐盟 DMA 新聞 feed `digital-markets-act.ec.europa.eu/node/2/rss_en` 30 筆、最新 2026-07-23；`ec.europa.eu/commission/presscorner/api/rss?language=en` 是 10 筆滾動視窗且 `size=`／`text=` 參數無效，**回溯不到 8 月，所以「執委會什麼都沒說」只能寫成「本文沒有取得執委會的一手說明」**。
- 頁面位元組數（111,532／162,927／142,113／141,539／842,456）是快照，不要寫進文章。

### source_list_fix

四條 sources 全部可達、都是 Apple 一手頁，沒有超過 4 條上限。要修的有兩點：

1. **三條事實（42、43、44）掛在 `https://developer.apple.com/support/terms/apple-developer-program-license-agreement/`，這條網址不在 `sources[]`。** 要嘛把它換進 sources（就得拿掉現有四條之一），要嘛不要寫 Attachment 14／Section 3.5／Section 4(E)／「全文 0 次出現 DMA」這些內容。
2. 前述 verified_fact 32 的稽核權半句要改掛 `payment-options-on-the-app-store-in-the-eu/`（已在 sources 內，不佔名額）。

---
## tech-news-apple-m6-m5-ultra-20260825

查核結果：needs_fixes，55 條確認、5 條推翻、7 條無法追溯。

### must_fix

1. 紀錄的 `event_date_basis` 寫「這些頁面沒有暴露 JSON-LD 的 datePublished／dateModified，Apple 自己顯示的日期是唯一官方日期訊號」；**直接被推翻**——六個頁面都內嵌 `application/ld+json`，`"datePublished": "2026-08-25Z"`、`"dateModified"` 落在 `2026-08-27T13:59:39Z` 到 `2026-08-27T14:09:07Z`。結論（事件日 2026-08-25）不變，但依據要改寫，而且 **2026-08-27 的 dateModified 必須記成活文件訊號**。
2. 紀錄在 `unverified_or_excluded` 寫「Newsroom 的 Atom feed 只有 20 筆、最舊到 2026 年 9 月，回溯不到 8 月」，並用它當作排除 M5 Pro／M5 Max 首發日的理由；**被推翻**——該 feed 20 筆的窗口最舊是 2026-08-11T13:59:21.581Z，而且**收錄了 8 月 25 日那三篇**。排除 M5 Pro／M5 Max 首發日的結論仍成立（窗口回溯不夠遠），但理由要重寫。
3. 紀錄 `sourcing_notes` 寫 Apple Newsroom archive 列表頁「curl 只拿到篩選器介面、零筆文章列」；**被推翻**——`https://www.apple.com/newsroom/archive/` 回 200、322,881 bytes，含 10 條文章連結（全是 2026-09）。實務結論（無法往回翻到 8 月）仍成立，但「零筆」是錯的。
4. 紀錄 `not_said` 寫「三篇稿都沒有出現 TSMC、台積電、foundry 等任何字眼」；**字面被推翻**——Mac Studio 稿出現兩次 "Foundry"，但那是 VFX 軟體商 Foundry（"Up to 15.4x faster CopyCat ML training performance in Foundry Nuke…"），不是半導體代工。TSMC／台積電／代工 確實六頁皆 0 次。編輯規則（不可補代工廠）不變，**但句子要縮小範圍**，否則讀者一查就以為我們寫錯。
5. 紀錄寫晶片稿 4.5 倍與 Mac Studio 稿 4.3 倍的差異「Apple 未說明兩者量測口徑差異」；**部分被推翻**——Apple 有揭露不同條件：晶片稿註腳 3 寫測試於 **2026 年 8 月**、預量產 Mac Studio M5 Ultra（36 核 CPU／80 核 GPU／**256GB**）對 M3 Ultra（32／80／256GB）對 M1 Ultra（20／64／64GB）；Mac Studio 稿註腳 1 寫測試於 **2026 年 7 月**，且該稿註腳 2 的基準是 512GB／8TB。改寫成「兩篇稿的測試月份與配置不同」，不要寫成無法解釋的矛盾。
6. 紀錄 verified_fact 44（Mac Studio）把「前一代 Mac Studio 搭載 M3 Ultra（32 核心 CPU、80 核心 GPU、512GB 統一記憶體、8TB SSD）、測試於 2026 年 7 月」當成 4.3 倍 AI／2 倍儲存／1.8 倍圖形／1.3 倍 CPU **四個數字共同的**依據；**錯**——頁面上標記是 "up to 4.3x faster AI performance,<sup>1</sup> up to 2x faster storage,<sup>2</sup> up to 1.8x faster graphics,<sup>1</sup> and up to 1.3x faster CPU speed,<sup>1</sup>"；註腳 1 只寫「Testing was conducted by Apple in July 2026.」，註腳 2 才是那組 512GB／8TB 配置。**那組配置只支撐「2 倍儲存」一項**，其餘三個倍數 Apple 沒有在這篇稿裡給對照配置。照抄會替 Apple 掛上它沒說的條件。
7. 紀錄 verified_fact 33（Mac mini）同樣把註腳對調了，而且 **Mac mini 稿的註腳編號與 Mac Studio 稿相反**：Mac mini 註腳 1 才是 M4 基準配置，註腳 2 是「Testing was conducted by Apple in July 2026.」，而本文是 "up to 4x faster AI performance,<sup>1</sup> 2x faster storage<sup>2</sup> and graphics,<sup>1</sup> and 40 percent faster CPU performance.<sup>1</sup>"。也就是 **Mac mini 的「2 倍儲存」只有日期註腳、沒有對照基準**。兩篇稿的註腳編號不可互套。
8. 紀錄 verified_fact 32 寫 Apple Intelligence「支援 16 種語言（含繁體中文）」；**「16」這個數字不在來源裡**——註腳 4 是逐一列名：English, Danish, Dutch, French, German, Italian, Norwegian, Portuguese, Spanish, Swedish, Turkish, Vietnamese, Chinese (simplified), Chinese (traditional), Japanese, Korean。數目是研究者自己數的（雖然數對了）。**改寫成「官方列出的語言中包含繁體中文」或照列清單，不要寫「16 種」。**
9. 紀錄 verified_fact 1 的 `verbatim_quote` 寫 `PRESS RELEASE / August 25, 2026`；**不是原文字串**，「 / 」是研究者加的。實質內容（PRESS RELEASE 標籤＋2026-08-25 日期，並在「Text of this article」區塊重複）已確認。
10. 紀錄 verified_fact 39 的 `verbatim_quote` 寫 `Up to 8.5x faster LLM prompt processing in LM Studio when compared to Mac mini with M2 Pro`；**漏字**——原文是 "Up to 8.5x faster LLM prompt processing **performance**<sup>5</sup> in LM Studio when compared to Mac mini with M2 Pro, and up to 4x faster than M4 Pro.<sup>2</sup>"。數字沒錯，但這是重打不是複製。**系統性問題：紀錄的 6、8、12、15、16、17、25 幾條英文引文把 Apple 的破折號「—」換成一般連字號「-」**，BRIEF 明文警告過這一點。**不要從 `verbatim_quote` 直接取字串。**
11. 紀錄 `not_said` 寫「Apple 沒有列出『全球最快的 CPU 核心／單執行緒效能』是和哪些競品、哪些基準測試比的。註腳只寫 shipping competitive systems and select industry-standard benchmarks」；**把兩個註腳混在一起了**——`<sup>1</sup>`（"Testing was conducted by Apple in August 2026 using shipping competitive systems and select industry-standard benchmarks"）掛在導言那句「…world's fastest CPU core … up to 170GB/s of unified memory bandwidth」；而「It delivers the world's fastest single-threaded performance and up to 1.2x faster multithreaded performance as compared to M5, and up to 2.4x faster than M1.」掛的是 `<sup>2</sup>`，**那個註腳只列 Apple 自己的三台 Mac，沒有任何競品**。結論（Apple 從未指名競品或基準測試）正確，註腳歸屬要改。
12. 紀錄 verified_fact 43（Mac mini 50% 再生材料）與 56（Mac Studio 35% 再生材料、供應鏈 40% 可再生能源）標成 `is_vendor_claim=false`；**錯**——這些是 Apple 自己的量測，各自帶方法學註腳（"Product recycled or renewable content is the mass of certified recycled material relative to the overall mass of the device…"）。依 BRIEF「廠商宣稱的能力、評測數字一律寫成『Apple 說明』」，**這兩條要寫成「Apple 說明」**。

### must_add

- **`overlaps_existing_article` 寫「站上目前沒有任何 tech-news-* 內容包…沒有既有科技文章可重複」，實質上是錯的。** `apps/api/app/guides/content/local-ai-on-mac-mini.json`（zh-TW 標題「Mac mini 當家用 AI 伺服器：統一記憶體、售價與區網設定」，sources checked_on 2026-09-14）已經出現 M6 12 次、M5 Pro 9 次、NT$29,900 兩次、NT$59,900 兩次、170GB 四次、307GB 四次——**正好就是 editorial_brief 想拿來當本文核心表格的那條統一記憶體階梯與台幣價格**。`local-llm-hardware-requirements.json` 與 `apple-intelligence-guide.json` 也有重疊。BRIEF「不要重寫既有文章講過的事」適用，**動筆前要重做重疊盤點**。
- **兩個 4.x 數字不只是數值不同，Apple 的標籤也不同。** 晶片稿：「up to 4.5x the peak GPU compute for AI compared to M3 Ultra」／繁中「AI 的 GPU 峰值運算能力最高可達 M3 Ultra 的 4.5 倍」；Mac Studio 稿：「up to 4.3x the peak AI compute performance of M3 Ultra」／繁中「AI 峰值運算效能最快可達 M3 Ultra 的 4.3 倍」。**一個是 GPU 峰值運算、一個是整機 AI 運算效能**——這比「數字打架」更站得住腳，也是比較好寫的角度。
- **漏掉一個 M5 Max 的官方標題數字**：Mac Studio 稿寫「M5 Max features phenomenal on-device AI compute with up to 3.9x faster AI performance than the prior generation」／繁中「M5 Max 具備出色的裝置端 AI 運算能力，AI 效能最快可達前一代的 3.9 倍」。紀錄只收了 M5 Max 的核心數、40 核 GPU、GPU 快 50%、614GB/s。
- **環保數字有不對稱，紀錄只抄了一半**：Mac mini 寫「Mac mini 在供應鏈製造過程中所使用的電力，均來自風能與太陽能等再生能源」（100%，再加上使用階段的抵換）；Mac Studio 寫「供應鏈使用 40% 可再生能源」。**只寫 40% 會讓讀者以為那是 Apple 的上限。**
- Mac Studio 稿有一句比規格列表更好用的「新在哪」：80 核 GPU「brings Neural Accelerators to the Ultra chip for the first time」，可以跟四晶粒「a first for Apple silicon」放在一起。
- **註腳編號隨語系與稿件而變**：紀錄已記到台灣版 Mac Studio 的環保註腳是 4／5、美國版是 5／6；**同樣的位移也發生在台灣版 Mac mini**（再生材料／包裝在台灣版是 5／6，美國版是 6／7），因為台灣版沒有 Siri AI 註腳。查核確認 Siri AI 出現次數：美版 Mac mini 12 次、美版 Mac Studio 12 次、台版兩篇皆 0 次、兩篇晶片稿皆 0 次。

### live_data_warnings

- 六個頁面全部帶 `dateModified` **2026-08-27**（13:59:39Z–14:09:07Z），也就是**現在讀到的都是 8 月 27 日修訂版**，不是 8 月 25 日發布時的原文。引用時要寫「2026-09-16 讀取」。
- Apple Newsroom Atom feed 是 **20 筆滾動視窗**（最新 2026-09-16、最舊 2026-08-11）。不能拿它證明「某事沒有發生」或「回溯不到」。
- `https://www.apple.com/newsroom/archive/` 只伺服當月的 10 條連結，同樣是快照。
- 頁面位元組數（201,731／195,266／225,209／212,252／235,077／231,931）是快照，不要寫進文章。
- 台灣售價 NT$29,900／NT$59,900／NT$84,900／NT$199,900 與教育價 NT$26,590／NT$56,390／NT$78,090／NT$185,390 是 **2026-09-16 查核日**的官方牌價，寫的時候要帶查核日（表格 caption 已規定要寫查核日）。

### source_list_fix

四條 sources 全部可達、無超量，但**結構有問題**：

- **60 條事實中有 9 條掛在兩個不在 `sources[]` 的美國版網址**（`.../apple-unveils-a-more-powerful-mac-mini-featuring-the-all-new-m6-and-m5-pro/` 與 `.../apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/`）。這 9 條涵蓋：**美金售價（US$899／US$1,699／US$2,499／US$5,499 與教育價）、「30 個國家和地區」、Apple Upgrade（Klarna）租賃、英文版 Srouji 引言、部分註腳條件、M6／M5 Pro／M5 Max 的應用測試數字**。
- 建議照研究紀錄自己的建議做：**只寫台幣、不寫美金與「30 個國家和地區」**，四條 sources 維持台灣版三篇＋美國版晶片稿。若非要寫美金或 30 個地區，必須把對應美國版網址換進 sources，且 4 條上限會逼你拿掉一條台灣版。
- 另注意：Apple 沒有 `/tw/` 版的開發者支援頁不是本篇問題，但 **本篇沒有任何 zh-TW 官方用語問題**——Apple 台灣版三篇全部提供官方譯名（超級核心／效能核心／節能核心／神經網路引擎／神經網路加速器／統一記憶體頻寬／四晶粒架構／動態快取／媒體引擎），不要自行翻譯。

---
## tech-news-apple-september-hardware-20260909

查核結果：needs_fixes，33 條確認、0 條推翻、5 條無法追溯。**注意：這一篇的查核涵蓋率最低。**

### must_fix

1. **研究紀錄有 91 條 verified_facts，但查核者只拿到並稽核了前 34 條**（交到查核者手上的輸出在「Apple Watch Series 12 台灣售價 NT$13,900 起；美國起價 399 美元。」處被截斷）。**第 35 條之後——Apple Watch Series 12、Ultra 4、AirPods 5 的全部事實——沒有經過獨立查核。** 撰稿代理必須把這一段當成未查核內容處理：能用查核者在 additional_findings 裡自行抓到的數字（見 must_add）交叉對上的才寫，對不上的不寫。
2. 紀錄 verified_fact 21 把「Pro Max 充滿電最長可用 30 小時」寫在「eSIM 專用機型」的限定語裡面；**美國版沒有把 30 小時綁在 eSIM 專用機型上**——美國版只把 36／45 小時的影片播放綁給 eSIM-only；30 小時在另一句、沒有限定語：「On iPhone 18 Pro Max, five minutes of wired charging provides around seven hours of video playback, and based on a new battery usage model that leverages real-world data, it provides up to 30 hours of usage on a full charge.」台灣版同一句寫 29 小時，所以美／台在這個數字上的差距也不是 eSIM 的兩小時造成的。**改寫成：30 小時（美國版）／29 小時（台灣版）是不帶 eSIM 限定語的「一般使用」數字。**
3. 紀錄 verified_fact 28 寫「iOS 27 於 2026 年 9 月 14 日以**免費軟體更新**形式推出」並掛台灣版網址；**台灣版寫的是「以免額外付費軟體更新的形式提供」**，「免費軟體更新」是美國版的 "free software update"。掛台灣版網址就要用台灣版的字：**「免額外付費軟體更新」**。
4. 紀錄 verified_fact 2 寫「當天沒有 Apple Watch SE 的新聞稿」；**這是從 20 筆滾動 feed 推出來的否定命題，而且寫法會誤導**——Apple Watch SE 3 就出現在同一批 9/9 稿件裡：watchOS 27 相容性清單（「Apple Watch Series 9 或後續錶款、Apple Watch SE 3，或 Apple Watch Ultra 2 或後續錶款」）與台灣版促銷註腳（「購買 Apple Watch Series 12、Apple Watch SE 3 或 Apple Watch Ultra 4…」）。`apple.com/tw/watchos/feature-availability` 也把 SE 3 與 Series 11／Ultra 3 歸為前一代。**若要寫，只能寫「9 月 9 日當天沒有單獨發布 SE 機型的新聞稿」，絕對不能寫成「沒有 Apple Watch SE」。**
5. **結構性問題：九條事實掛在不在 `sources[]` 的美國版 Newsroom 網址**（美金售價、美國版地區名單、mmWave、eSIM-only 續航與販售地區、iPhone Handoff、測試條件註腳）。`sources[]` 只有四條台灣版。依 BRIEF，這九條目前在內容包裡無法追溯。**其中測試條件註腳不必犧牲名額**——「測試由 Apple 於 2026 年 7 月…」／「…2026 年 8 月…」逐字就在台灣版頁面上，改掛台灣版網址即可。其餘要嘛不寫、要嘛換 source。
6. `sources` 裡的 `https://www.apple.com/tw/watchos/feature-availability/` 雖然回 200、內容也真，但**這條網址不是從四篇新聞稿任何一篇連出來的**（四篇台灣版唯一的 feature-availability 連結是 iPhone 頁上的 `apple.com/tw/ios/feature-availability`）。它看起來是從 iOS 那條路徑類推出來的。研究紀錄必須寫清楚它是怎麼找到的，不能留成一條像是自己拼出來的網址。
7. 地區名單的差異紀錄只寫了一半：**台灣版 iPhone 名單有「台灣」但沒有 Türkiye，美國版有 Türkiye 但沒有 Taiwan**；手錶也一樣，美國版 Series 12／Ultra 4 寫 "Australia, Canada, France, Germany, India, Japan, the UAE, the UK, the U.S., and more than 50 other countries"，台灣版寫「澳洲、加拿大、法國、德國、印度、日本、台灣、英國、美國等超過 50 個國家和地區」（有台灣、沒有阿拉伯聯合大公國）。**這是各語系的舉例名單，不是不同的地區集合。文章不可以把任何一版寫成完整名單。**
8. 四篇新聞稿正文都沒有介紹高血壓通知是什麼（美國版兩篇手錶稿 "hypertension" 出現 **0 次**，台灣版只在註腳出現「高血壓」）。**不可以描述這個功能怎麼運作、量什麼、準不準。**
9. 不可以叫讀者到 `support.apple.com/zh-tw/118210` 查高血壓通知——實測該網址回 200，但頁面標題是「可搭配 Apple Fitness+ 使用的裝置」，全頁沒有「高血壓」。**這是 Apple 自己註腳指錯頁，本文不可以轉述這個連結。**

### must_add

- **台灣版獨有的法規註腳，是整批最與台灣相關的一條，兩篇手錶稿一字不差**：「Apple Watch Series 12 或 Ultra 4 上的高血壓通知功能在台灣不會一開始就推出，因為該功能於這些型號的其他法規核准程序仍在進行中。預計將於明年推出。詳情請參閱功能供應狀態說明：support.apple.com/zh-tw/118210。」**Apple 沒有寫月份、沒有指名任何主管機關。**
- `apple.com/tw/watchos/feature-availability` 佐證但沒有加日期：「健康：高血壓通知」的地區清單有 183 筆，台灣寫成「台灣7」，註腳 7 是「『高血壓通知』功能可能不適用於你所在地區的 Apple Watch Series 12 或 Apple Watch Ultra 4，這些裝置尚待監管機構進行額外的審核。」**「預計將於明年推出」這句只存在於新聞稿註腳，要掛在新聞稿上。**
- **查核者自行抓頁確認的 Series 12 數字**（可用來交叉檢查未稽核的第 35 條之後）：NT$13,900 起／US$399；預訂即日起（9/9）、供貨 9 月 18 日；超過 50 個國家和地區；S11＋「健康感測系統」；全天候每五秒量一次心率；HRV 測量頻率最高可達以往的 24 倍；「準備指數」0 至 10 分、四種建議「恢復」「量力而為」「準備就緒」「全力以赴」；日常續航 24 小時、室外體能訓練 10 小時（較上一代 +25%）、充電 15 分鐘可增加最長 12 小時（較上一代 +50%）；鋁金屬錶款用超瓷晶盾 2、較 Ion-X 提升 60%；環境 40% 再生材料。**所有「最精準」字樣都是 Apple 宣稱，依據是 Apple 自己做的逾 1,000 人研究。**
- **Ultra 4**：NT$27,900 起／US$799；預訂即日起、供貨 9 月 18 日；超過 50 個國家和地區；連續追蹤室外體能訓練最長 45 小時；「運動手錶中最精準的裝置端 GPS」（Apple 宣稱）；原色與黑色鈦金屬。
- **AirPods 5**：NT$4,490 標準款／NT$5,190 搭配無線充電盒（更長續航、耳機柄音量控制）；US$129／US$149；供貨 9 月 18 日。**地區寫法兩版不同**：台灣版「包括台灣在內等超過 65 個國家與地區」，美國版 "the U.S. and more than 65 **other** countries and regions"。**不要合併這兩句。**
- **兩條有日期的未來承諾，紀錄漏了**：(a) SynthID——正文「影像後設資料和即將支援的 SynthID 標準，也能協助使用者辨識由 AI 生成或編輯的影像」，註腳「SynthID 將於今年稍晚透過軟體更新推出，並會視採用的編輯方式，套用於大多數經過編輯的影像」；紀錄的「Apple 參考影像」那條把 SynthID 整個漏掉。(b) 兩篇手錶稿：S11「也將支援於今年稍晚推出的全新功能，協助失聰或重聽使用者留意重要聲音」。
- 美國版 iPhone 註腳 159 比紀錄引用的那條 Apple Intelligence 註腳更廣：「Siri AI will not be available initially in the EU on iOS, iPadOS, and watchOS. Features that rely on Siri AI will also not be available in the EU on iOS, iPadOS, and watchOS.」紀錄引的那條只涵蓋 iOS。
- **美國限定、各有自己日期的商業項目，紀錄一條都沒有**：Apple Upgrade（Klarna 提供的租賃方案，限美國）iPhone 18 Pro 每月 $34.99 起、Series 12 每月 $11.99 起；新訂閱者與符合資格的回歸訂閱者可從 **9 月 17 日**起免費使用三個月 Apple One；AppleCare One 與 AppleCare One Family。**9 月 17 日是 9/9、9/12、9/14、9/18、9/25 之外的第六個日期。**
- 台灣版手錶稿獨有促銷：「購買 Apple Watch Series 12、Apple Watch SE 3 或 Apple Watch Ultra 4 的新訂閱者，可免費享有三個月的 Apple Fitness+ 和 Apple Music。優惠與服務適用狀況因區域而異。」
- iCloud+ 入門價依市場而異：台灣版「每月最低只需 NT$30」，美國版 "$0.99 (U.S.) per month"。要寫就用台灣版數字配台灣版來源。
- **日期衛生**：發表 2026-09-09（八個頁面與兩個 feed 一致）；iPhone 18 Pro 預購 2026-09-12——「台灣時間 9 月 12 日（星期六）晚上 8 點」與 "5 a.m. PT this Saturday, September 12" 是**同一個時刻的兩種寫法，不可寫成兩個事件**；手錶與 AirPods 預購 2026-09-09（即日起）；軟體 2026-09-14；首波供貨 2026-09-18；Apple One 優惠 2026-09-17；iPhone 18 Pro 第二波 2026-09-25（其他 20 個國家和地區）。`news_date` 與 slug 後綴都是 2026-09-09。

### live_data_warnings

- **台灣版 Apple Watch Ultra 4 是被改過的活頁面**：台灣 feed 的 `<updated>` 是 2026-09-11T21:53:40.438Z，頁面日期列仍寫 2026 年 9 月 9 日。查核者另發現該頁心率段落有明顯的編輯殘留：「帶來穿戴式裝置中最精準的心率感測功能透過針對超過千名多元參與者進行嚴謹的科學研究…」，註腳標記與句讀都掉了，與 Series 12 的平行句不同。**引用這一頁前必須重抓。**
- `apple.com/tw/watchos/feature-availability` 是**沒有日期的動態頁**，183 筆地區清單與註腳 7 都是 2026-09-16 讀到的狀態。**不可以寫成「9 月 9 日之後就是這樣」。**
- 兩個 Atom feed 都是 20 筆滾動視窗（美國版最新 2026-09-16、台灣版最新 2026-09-15）。**任何「當天沒有某篇稿」的判斷都受限於這個窗口。**
- 八個頁面的位元組數與 canonical 是快照，不進文章。
- Apple Watch Series 12／Ultra 4／AirPods 5 的台幣起價是查核日牌價，官方沒有完整價格表（GPS／行動網路、尺寸、材質、陶瓷與 Hermès 款的價格都沒公布）。

### source_list_fix

`sources[]` 是四條台灣版新聞稿，數量沒超過上限，但**這是本垂直結構問題最嚴重的一篇**：

- **20 條事實掛在 7 個不在 `sources[]` 的網址**：四篇美國版新聞稿（iPhone 7 條、Ultra 4 四條、AirPods 5 三條、Series 12 兩條）、美國與台灣兩個 Atom feed（各 1 條）、以及 `apple.com/tw/watchos/feature-availability`（2 條）。
- 4 條上限下不可能把它們都納入。**建議的取捨**：保留四篇台灣版；把測試條件註腳改掛台灣版（不佔名額）；**其餘美國版獨有內容（美金價、mmWave、eSIM-only 續航與地區、iPhone Handoff、Audio Intelligence／Live Rewind／Siri Recap、重新設計的「健康」App／Quest 檢驗）全部不寫**，因為那些本來就屬於同日另一篇 `Apple advances health and fitness capabilities using Apple Intelligence` 與既有的 `ai-news-siri-ai-ios-27-20260914`。
- 若要寫高血壓通知在台灣的狀態，`apple.com/tw/watchos/feature-availability` 只是佐證，**「預計明年推出」必須掛台灣版新聞稿**，不必為它換掉一條 source。
- `support.apple.com/zh-tw/118210` **不可進 sources、也不可寫進文章**（Apple 自己連錯頁）。

---
## tech-news-eu-cra-reporting-20260911

查核結果：needs_fixes，61 條中 57 條逐字確認、2 條推翻、4 條無法追溯。查核者評價這是本批次最扎實的一份紀錄，但四個缺口都會直接影響法規敘述。

### must_fix

1. 紀錄在 `unverified_or_excluded` 第 4 條寫「The CRA entered into force on 10 December 2024 ... 沒有任何官方頁寫出確切生效日，我不會刊出自己算出來的日期」；**被推翻**——執委會自己的「Cyber Resilience Act - Summary of the legal text」頁逐字寫著：「The CRA entered into force on 10 December 2024. It will be fully applicable as of 11 December 2027 with some provisions starting to apply earlier: Chapter IV on the notification of conformity assessment bodies will apply from 11 June 2026, whereas reporting obligations set out in Article 14 apply from 11 September 2026.」網址 `https://digital-strategy.ec.europa.eu/en/policies/cra-summary`（HTTP 200，123,150 bytes，Last update 3 December 2025），而且它就是已在 sources 內的 cra-reporting 頁上的 Quick Link。**刪掉這條排除，改寫成：執委會的法規摘要頁載明 CRA 於 2024 年 12 月 10 日生效。**
2. 紀錄 `sourcing_notes` 寫「`https://publications.europa.eu/resource/celex/32024R2847` 對 `Accept: text/html` 與 `Accept: application/pdf` 回 404、對 `Accept: application/xhtml+xml` 回 200」；**照這個配方重現不出來**——不帶 `Accept-Language` 時三種 Accept 全部回 HTTP 400（205 bytes 錯誤頁，測兩次皆同）。**必須加上 `Accept-Language: eng`** 才會出現紀錄描述的 404／404／200。研究紀錄必須把這個標頭寫進去，否則下一個查核者會判定這條來源已死。
3. 紀錄 verified_fact 54 裡「Section 9.1 of that guidance covers reporting obligations」與「The Commission also publishes 'FAQs on the CRA implementation', Section 5 of which covers reporting」兩句掛在 guidance 公告頁；**那一頁沒有這兩句**（該頁抽出的文字中 "9.1" 0 次、"Section 5" 0 次）。其餘（67 個實務案例、非拘束性、in force since December 2024、C(2026) 5252 Communication 加 Annex、2026-07-27 發布）確實在該頁且逐字無誤。這兩個節次編號在 **cra-reporting 頁**（「Section 9.1 of the Commission guidance on the CRA, as well as in Section 5 of the Commission's Frequently Asked Questions on the CRA implementation」）與 **ENISA FAQ 10**，兩者都已在 sources 內。**改掛正確網址。**
4. 紀錄 verified_facts 43 與 44（Commission Delegated Regulation (EU) 2026/881 of 11 December 2025，及其第 3 條的四項延後散布條件）內容全部正確——查核者抓 `https://publications.europa.eu/resource/celex/32026R0881`（200，29,368 bytes）確認了標題、2025-12-11、OJ L 2026/881 of 20.4.2026、ELI `http://data.europa.eu/eli/reg_del/2026/881/oj`、第二十日生效、第 3 條四項條件與第 4、5 條——**但這條網址不在四條 sources 內**。**「2025 年 12 月 11 日通過授權法案」這件事本身在 sources 內就有**（cra-reporting 頁寫 "on 11 December 2025, the Commission adopted a delegated act"；ENISA FAQ 21 寫 "The European Commission adopted a Delegated Act on 11 December 2025"）。**只有第 44 條那些第 3 條細節需要額外的 source 名額；不換就不要寫細節。**
5. 紀錄 verified_fact 21 寫「Counted on the page: 27 Member States, from Austria to Sweden.」；**「27」是研究者自己數的，ENISA 並沒有在那頁印出這個數字**（查核者獨立數過，確認是 27，「Last updated: 10 September 2026」也逐字無誤）。而且這條事實把研究者放在 `unverified_or_excluded` 的但書弄丟了。**寫法必須是「ENISA 的清單每個歐盟會員國各一筆聯絡窗口」，而且絕對不能寫成「每一件通報都會送達全部 27 個 CSIRT」**——第 16 條第 2 項只要求散布到製造商指明產品有供應的那些領域的 CSIRT。
6. **四條事實的 `verbatim_quote` 是 HTML 抽取殘留，不是頁面上的字**：facts 4、18、25、56 有標點前多空格（"11 December 2027 , with"、"Single Reporting Platform (SRP) . The"、"portal.cra-srp.enisa.europa.eu . From there"、"telecommunications . The streamlined"）；fact 0 把第 71 條第 2 項的兩個分項併成一句；fact 53 把標題寫成 "(EU) 2019/1020"，而它所引的 CELLAR 網址上的 OJ 正文寫的是 "(EU) **No** 2019/1020"（前者是出版局紀錄頁的寫法）。實質內容都確認無誤，**但不可以把 `verbatim_quote` 當字面引文照登**。
7. **法律適用日的但書被用得不一致，這是本篇最可能寫錯的地方。** 第 71 條第 2 項只把 **第 14 條與第四章（第 35–51 條）**提前；第 15、16、17、24、64、69 條**沒有**被提前，就文義而言自 2027 年 12 月 11 日起適用（查核者確認第 64 條在 OJ 正文屬第七章，不是第四章）。紀錄對第 13、24、64 條嚴格套用了這個但書，fact 1 也正確寫出第 14 條是唯一被提前的通報條文，**但 facts 16、17、22、39、41、42、46、47、48、50 卻把第 16 條、第 17 條與第 69 條第 3 項的義務寫成已在運作**。**文章不可以寫第 16 條或第 17 條自 2026 年 9 月 11 日起適用。**

### must_add

- **已在 sources 內、但沒被用到的更好引句**：ENISA FAQ 12 用 ENISA 自己的話說第 14 條義務「will apply from 11 September 2026 to all products with digital elements falling within the scope of the CRA, including products that were placed on the market before 11 December 2027.」研究紀錄把第 69 條第 3 項稱為「最強的讀者切入點」卻只引法規原文；FAQ 12 讓同一件事可以用已列來源的機關頁講。執委會摘要頁也有同樣的話：「Reporting obligations apply to all products with digital elements that have been made available on the Union market, including those already placed on the market before 11 December 2027.」
- **`sources[3]` 建議換掉**（見 source_list_fix）。可換的兩個都是一手：`https://digital-strategy.ec.europa.eu/en/policies/cra-summary`（執委會，HTTP 200，人看得懂，且自己就寫出第 71 條第 2 項三個日期、2024-12-10 生效、四個通報期限、以及 2027 年前既售產品那一點）；或 `https://op.europa.eu/en/publication-detail/-/publication/21b7d4eb-a6e2-11ef-85f0-01aa75ed71a1`（HTTP 200，標題正確，但只有中繼資料、沒有條文）。
- **換 cra-summary 的但書**：該頁自己聲明「This summary has been prepared by the Commission services and is not meant to systematically cover the full scope of the Regulation. This summary is not representative of the European Commission's official position.」而且最後更新是 2025 年 12 月 3 日（在平台上線之前），並寫著「It is also possible for any natural or legal person to notify vulnerabilities, cyber threats, incidents and near misses on a voluntary basis through the CRA Single Reporting Platform」——**這句已被 ENISA FAQ 27 就現行版本否定（"The platform has not yet implemented the voluntary reporting functionality provided for under Art. 15(1) and (2)"）。不可以用那句。**
- 未記錄的上線狀態限制，與紀錄已抓到的那幾條同類：ENISA FAQ 9 寫「No additional corporate entity authentication mechanism is currently used by the SRP.」同一條 FAQ 還寫：Secondary AR 只能看自己送出的通報，Primary AR 可以看該製造商全部的通報。
- 對消費者角度有用、紀錄沒收的：ENISA FAQ 11 說 SRP 在「遭實際利用的弱點」欄位包含 CVE ID 與 EUVD ID；FAQ 19 說 ENISA「discloses fixed vulnerabilities to the European Vulnerability Database (EUVD)」——這是第 17 條第 5 項在 sources 內的重述。**ENISA 全站的謹慎寫法是「manufacturers and, once applicable, open-source software stewards」，文章要照這個寫法。**

### live_data_warnings

- 三個官方頁都印著自己的「最後更新」，而且都是查核期間的日期：執委會 cra-reporting「Last update 11 September 2026」；ENISA SRP FAQ「Updated: 12 September 2026」、31 條編號 FAQ；ENISA CSIRT 清單「Last updated: 10 September 2026」、27 筆（**筆數是人工數的**）；ENISA 其他指引頁「Updated: 9 September 2026」或「Updated: 10 September 2026」，且 ENISA 自述這些材料「reflect ENISA's current best knowledge and may be subject to change」；cra-summary「Last update 3 December 2025」。
- **平台的「現況」全部是上線初期快照，隨時會改**：只有英文（FAQ 24）、沒有 API（FAQ 15）、沒有自願通報（FAQ 4／6／27）、72 小時計時器顯示 48 小時的已知瑕疵（FAQ 26）、遭實際利用弱點沒有最終報告計時器。**每一條都要寫「ENISA 表示，截至 2026 年 9 月 16 日查核時」。**
- 「SRP 上線以來收到幾件通報／幾家製造商註冊」**沒有任何官方數字，什麼都不要寫**。
- `https://portal.cra-srp.enisa.europa.eu` 只記「ENISA 公布這個位址、並說自 2026 年 9 月 11 日起可用」，本次沒有開啟，**不可描述介面**。

### source_list_fix

四條沒有超量，但**第 4 條實質上不可刊**：

- `https://publications.europa.eu/resource/celex/32024R2847` 對一般用戶端不會伺服 CRA 條文：不帶 `Accept-Language` 一律 HTTP 400；用瀏覽器式 Accept 會拿到 2,001,488 bytes 的 `application/rdf+xml` 中繼資料。**讀者點進去拿到的是一個 RDF 檔，不是法規。建議在內容包裡換成 cra-summary 或 op.europa.eu 紀錄頁**，並把 CELLAR 端點留在研究紀錄裡當作「實際讀取條文的網址」，同時寫明 `Accept-Language: eng` 的要求。
- EUR-Lex 系列網址（`eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R2847`、`eur-lex.europa.eu/eli/reg/2024/2847/oj`、`http://data.europa.eu/eli/reg/2024/2847/oj`）在本容器全部回 **HTTP 202、0 bytes**（AWS WAF）。**不可以記上 `checked_on` 當成來源。**
- 7 條事實掛在 4 個不在 `sources[]` 的網址：guidance 公告頁（3 條）、CELEX 32026R0881（2 條）、ENISA CSIRT 清單（1 條）、ENISA SRP 主題頁（1 條）。其中 guidance 頁那 3 條有一部分可改掛已列來源（見 must_fix 3）。
- 沒有任何一條事實來自媒體、整合站或搜尋摘要——16 個網址全在 europa.eu 網域。識別碼也沒有用猜的：CELEX 32024R2847 與 32026R0881 都是從執委會 cra-reporting 頁的 href 取得，cellar UUID 來自轉址鏈，18 個 ENISA FAQ 編號全部存在，C(2026) 5252 印在 guidance 頁的下載區。**唯一自行組出來的網址是 op.europa.eu 紀錄頁（用 cellar id 拼的）——它解析得到正確文件，但紀錄要註明它是拼出來的。**

---
## tech-news-iphone-duo-20260909

查核結果：needs_fixes，71 條確認、2 條推翻、7 條無法追溯。75 條 `verbatim_quote` 全部比對過，75／75 都能在所引頁面找到且數字單位一致。

### must_fix

1. 紀錄 `not_said` 寫「新聞稿沒有寫後鏡頭有幾顆，也沒有獨立的望遠鏡頭模組」；**被推翻**——已列為 source 的台灣技術規格頁把後鏡頭區塊標題寫成「**4800 萬像素雙融合相機系統**」，Apple 確實說了那是雙鏡頭系統。只有新聞稿沒寫。**這句要限縮成「新聞稿沒有寫」，或整句刪掉。**
2. 紀錄 `not_said` 寫「Apple 沒有提到 iPhone Duo 的 NCC 型式認證或任何台灣法規狀態」；**被推翻**——台灣技術規格頁上有「如需台灣 NCC 認證產品的進一步詳細資訊，請按這裡」。那是樣板文字、沒有 Duo 專屬的認證狀態，**但這個全稱句被自己引的來源否定，要改寫**。
3. 紀錄 verified_fact 20 末尾寫「內螢幕不是用 Ceramic Shield 2」；**沒有任何來源這樣說**——英文頁只說背板是 Ceramic Shield、Ceramic Shield 2 用在 "on the front"（圖說寫 "on the outer display"），台灣技術規格頁列「超瓷晶盾 2 面板／超瓷晶盾背板」，對內螢幕隻字未提。這是把「沒提到」推論成「沒有用」。**改寫成：「Apple 只說明超瓷晶盾 2 用於正面／外螢幕，內螢幕的保護方式另行說明。」**
4. 紀錄 verified_fact 57 把「Apple 的目標是 2030 年**整體營運**碳中和」與「**製程** 60% 採用可再生能源」掛在英文網址；**掛錯語系**——英文頁寫的是 "carbon neutral across its entire **footprint** by 2030" 與 "60 percent renewable energy ... across the **supply chain**"。「整體營運」「製程」是 Apple 台灣頁的措辭。**要嘛改掛台灣版網址，要嘛把字改成「整體碳足跡」「供應鏈」。**
5. 紀錄 verified_fact 45（有線約 20 分鐘、無線約 30 分鐘充到最多 50%）標成 `is_vendor_claim=false`；**錯**——這兩個數字帶的是和續航數字同一條「Apple 於 2026 年 7 月以預量產機型測試」的註腳，而續航那條（fact 42）已正確標成 vendor claim。**要寫成「Apple 表示」。**
6. 紀錄 verified_fact 25 的「零快門延遲」與低光源表現標成 `is_vendor_claim=false`；**錯**——"zero shutter lag" 與 "excels in low light" 是 Apple 的能力宣稱，不是公布的規格，本站也沒有實測。**寫成「Apple 表示」。**
7. 紀錄 verified_fact 32 寫 Split View「讓使用者**首次**能在 iPhone 上並排開啟兩個 app」標成 `is_vendor_claim=false`；**「首次」是 Apple 自己的說法**，要寫成「Apple 表示」。
8. 紀錄 verified_fact 47 寫「超過 500 家電信業者支援 eSIM」標成 `is_vendor_claim=false`；**那是廠商提供的數字**，事實文字裡雖然有「Apple 說明」但旗標矛盾。**寫成「Apple 說明」。**
9. 紀錄 facts 0、1、11、46 的 `verbatim_quote` 把頁面上分開的元素用 " / " 串成一條字串當原文引用；**那個字串在頁面上不存在**（其餘 71 條用 '…' 的寫法是對的）。**不要把這四條的引號字串帶進譯文或 QA 比對。**
10. **繁中版把 Apple 的 "up to" 對沖詞拿掉了，照抄會變成誇大**：台灣版「6 核心 CPU 比 A19 Pro 快了 20%」vs 英文 "up to 20 percent faster"；台灣版「其剛度比業界其他採用的材質高出 40%」vs 英文 "up to 40 percent higher stiffness"；更嚴重的是台灣版「7 核心 GPU 速度和能源效率都提升了 40%」把 40% 也掛到能源效率上，英文 "up to 40 percent faster and more power efficient" 的 40% **只掛在速度**。**三個數字都要照英文版的限定語寫。**
11. **繁中版把充電數字配錯了**：台灣版「搭配 MagSafe 或 Qi2 充電器，iPhone Duo 約 20 分鐘即可充至最多 50% 電量，或無線充電約 30 分鐘即可充至最多 50% 電量」，把 MagSafe／Qi2 掛在 20 分鐘那一邊。**英文版與台灣技術規格頁都是：20 分鐘＝有線，30 分鐘＝MagSafe／Qi2 無線。** 研究者採用了英文版（正確），但沒有把這個陷阱寫下來。

### must_add

- **Apple 兩個最核心的最高級說法完全沒有進 verified_facts，只殘存在 `not_said` 裡**：「Opened, it is the thinnest iPhone ever」與「iPhone Duo features the largest display ever on iPhone」（Ternus 另複述「the largest display ever on iPhone that still fits easily in your pocket」）。**這是新聞稿的主張核心，要以「Apple 表示」入稿。**
- 台灣技術規格頁註腳 13「須使用速度達 10Gb/s 的 USB 3 連接線」是 10Gb/s 那個數字的條件，而盒內線材只列「USB-C 充電連接線 (1 公尺)」。紀錄兩半都有，但沒把條件接起來。
- 台灣技術規格頁在螢幕區塊直接列「支援 Apple Pencil (USB-C)」且**沒有時間限定**，而新聞稿寫的是 "Later this year"。**要並記，免得讀者以為上市當天就能用。**
- 紀錄 verified_fact 24 把尺寸按頁面順序抄下來但**沒有標籤**。規格頁的標示是：展開 164.6 公釐＝**寬度**、117.8 公釐＝**高度**、厚 5.2 公釐；闔起 84.1 公釐寬、117.8 公釐高、厚 11.3 公釐；兩種狀態都是 254 公克。**editorial_brief 要做尺寸表，寬高互換是最容易犯的錯。**
- 英文註腳裡兩個「不是上市即有」的條件沒記：註腳 5 把新的「攝影風格」質感／顆粒控制限定在 "iPhone models that support the latest generation of Photographic Styles"；註腳 6 說 SynthID "will be available in a software update later this year"。
- 名單成員也不同，不只是數字不同：Brazil 出現在英／英國／澳／星版名單、不在台灣版名單；台灣版多了泰國與台灣。**這強化了「including … 只是舉例」的論點，要和 63／70 的差異寫在一起。**
- 英文註腳 3 說 Siri AI 初期在歐盟的 iOS、iPadOS、watchOS 都不提供；台灣版註腳只寫「在歐盟地區，Siri AI 推出初期不會於 iOS 上提供」。紀錄 fact 69 引英文網址所以本身沒錯，**但翻譯階段要注意台灣版範圍較窄**。
- **63 對 70 的矛盾是真的、而且是這篇獨有**：台灣版寫「超過 63 個國家和地區」，英／英國／日／澳／星版都寫 more than 70／「70以上」。對照組成立——同一天的 iPhone 18 Pro 英文版寫 "more than 65 countries and regions"、台灣版寫「65 個以上國家和地區」，**兩邊一致**，所以 63／70 不是 Apple 慣常的語系差異。**兩個數字要並列，不可擇一。**
- 紀錄把台灣商店價排除的**理由寫錯了**：NT$81,900 與 NT$118,900 確實出現在 `apple.com/tw/shop/buy-iphone/iphone-duo`（HTTP 200，查核者確認），而價格不是「能力宣稱」，所以 tech.md 的「產品行銷頁不能當能力宣稱的來源」表面上不適用。**不寫仍然正確，但正確理由是：原始 HTML 無法把容量與價格一一對應（查核者自己試也失敗）。** 只寫新聞稿的「NT$74,900 起」。

### live_data_warnings

- 四個來源頁的位元組數（341,693／298,161／251,311／330,229）只是快照；研究紀錄與查核抓到的英文版與台灣版各差 118 bytes，是頁面層級的動態標記，內容一致。**不要把位元組數寫進文章或當成頁面未變的證明。**
- Apple Newsroom Atom feed 是 20 筆滾動視窗（最新 2026-09-16），本篇 entry `<updated>` 2026-09-09T18:15:40.996Z。**窗口會滾掉。**
- `apple.com/tw/shop/buy-iphone/iphone-duo` 是 JavaScript 產生的商店頁，價格與容量對應隨時可能改，**不要引用**。
- 「超過 63 個／超過 70 個國家和地區」本身就是 Apple 兩個語系版本的當下狀態；10 月 30 日第二波的 28 個地區 Apple **從未公布名單**，任何推測都是捏造。

### source_list_fix

**這是本垂直結構最乾淨的兩篇之一：75 條事實全部掛在四條 sources 之內，沒有一條掛在表列之外的網址，也沒有超過上限。**

- 四條全是 apple.com 一手頁，全部 HTTP 200、真實內文。
- 第 4 條（新加坡版新聞稿）只用來佐證各語系名單差異，用途正當，但若版面吃緊可考慮換成台灣版技術規格頁以外的其他必要來源——目前沒有這個必要。
- 提醒：台灣版 AirPods／iPhone Duo 的 slug 與美國版不同，抄網址時不可套用美國 slug（查核者自己猜 `apple-introduces-...` 就得到 404）。本篇的四條網址都是從官方 feed 取得的，維持原樣。

---
## tech-news-nvidia-cuda-q-20260914

查核結果：needs_fixes，41 條確認、3 條推翻、5 條無法追溯。

### must_fix

1. 紀錄 F22 寫「The whole section sits under a docs navigation heading literally labelled "Preview"」並掛 `https://nvidia.github.io/cuda-quantum/latest/preview/logical/index.html`；**那一頁沒有這個標題**——該頁的 Sphinx 側欄標題只有 'Getting started'、'Use cases'、'Reference'、'CUDA-Q'。"Preview" 這個導覽標題在 `https://nvidia.github.io/cuda-quantum/latest/index.html`，而**那一頁不在 sources 裡**。F22 的其餘部分（該頁頂端的 'cudaq-logical is in preview. Its APIs, behavior, and documentation may change substantially in upcoming versions.' 警語）是對的、確認過。
2. 紀錄 F44 的 `verbatim_quote` 寫 'CUDA-Q also provides an open, extensible logical layer for fault-tolerant workloads, Quantum Error Correction (QEC) codes and QPU architecture co-design, currently in preview.'；**不是逐字**——線上頁面實際是 '...logical layer for fault-tolerant **fault-tolerant**\nworkloads, ...'，NVIDIA 的文件重複了一次 'fault-tolerant'。查核者比對的是原始 HTML，不是抽取後的文字，所以不是抽取造成的。**被默默修好的 `verbatim_quote` 正是翻譯會照抄的東西——不要用這條引文。**
3. 紀錄 F45 寫「…none is named for "logical", "ftqc" or "fault"」並掛 `https://raw.githubusercontent.com/NVIDIA/cuda-quantum/main/LICENSE`；**兩處都錯**——(a) 那條網址是 Apache 2.0 授權條文，完全沒有講分支，事實追溯不到所引頁面；(b) 字面主張為假，查核者自己跑 `git ls-remote --heads` 有 `refs/heads/debug_seg_fault` 與 `refs/heads/test_seg_fault`，兩個都含 'fault'。**實質內容（沒有 CUDA-Q Logical 專用分支，它在 main 的 `preview/logical/` 底下）正確，201 個 head 的數字也確認**，但這條的措辭與網址都要改。
4. 紀錄 F12 寫「the quick start adds a standalone route, `pip install cudaq-logical[cu13]`（或 CUDA 12 用 `[cu12]`），並警告裸裝的 `cudaq-logical` 不含必要相依」，掛在 logical index 頁；**那一頁只有** 'CUDA-Q Logical comes pre-installed with cudaq, so one command is enough: pip install cudaq'。`cu13`／`cu12`／`cudaq-logical[` 在該頁 0 次命中。那些文字全在 quickstart 頁，而 **quickstart 頁不在 sources 裡**。**F12 有一半追溯不到自己的網址。**
5. 紀錄 F30 寫「That is 150 physical qubits per logical qubit.」；**那是研究者自己算的（150,000 ÷ 1,000），新聞稿沒有這個數字**。NVIDIA 只寫 '1,000 logical qubits ... with just 150,000 physical qubits, roughly 10x fewer than Diraq's previous estimates'。依 BRIEF「每一個數字都要能指到來源原文」，**這個 150 不要寫**，真要寫必須標明是編輯自行換算。
6. 紀錄 F32 寫「The list of organisations NVIDIA says are ALREADY USING CUDA-Q Logical, **exactly six entries**」；**引文確認無誤，逗號的判斷也對**（原始 HTML 裡 'Quantum Motion' 自己是一個連到 quantummotion.com 的錨點，'QCDesign' 是純文字，所以是兩家），**但那句話開頭是 'is already being used by QPU makers and labs INCLUDING'**——明示不是窮舉。「exactly six」當「印出來的名字有六個」是對的，當「有六家在用」是錯的。**寫成「NVIDIA 列名的有六家，並以 including 表示不是完整名單」。**
7. 紀錄 F0 把 RSS 的 pubDate 'Mon, 14 Sep 2026 13:00:00 GMT' 與 modDate 'Mon, 14 Sep 2026 16:31:03 GMT' 掛在**文章頁**網址；兩個值都正確（查核者重抓 releases.xml 確認），**但文章頁上沒有這兩個字串**，一條事實掛一個網址的規則被破壞。另外 `event_date_basis` 寫「the release was revised about 3.5 hours after publication」是推論——**modDate 是 CMS 欄位，本身不能證明正文改過。**
8. **七條事實掛在不在 `sources[]` 的網址，卻沒有像 F40–F43 那樣標上「EXTRA URL, NOT IN sources」**：F10（raw README）、F11 與 F17（PyPI json）、F13（quickstart）、F39（sandialabs README）、F44 與 F45（cuda-quantum index／LICENSE）。每條網址本身都確實載有該事實，**問題是撰稿者掃過內容包時會以為它們可以掛在那四條 sources 下引用**，違反研究紀錄自己在 `sourcing_notes` 裡訂的規則。

### must_add

- **sources 2–4 應改用版本鎖定網址。** 目前三條都指 `/latest/`，是會移動的目標（文件自己寫 'You are browsing the documentation for latest version of CUDA-Q'），0.17.0 一出這些網址就會在描述另一個版本。查核者確認版本鎖定版今天位元組完全相同：`https://nvidia.github.io/cuda-quantum/0.16.0/preview/logical/index.html`（200，50,833 bytes）與 `https://nvidia.github.io/cuda-quantum/0.16.0/preview/logical/reference/capabilities.html`（200，37,029 bytes）。
- **第二處「摘要與內文不一致」，紀錄只抓到一處。** 研究者抓到 Fermilab 的 'architecture' vs 'algorithm'，但漏了 QUOPS 同樣的模式：News Summary 條列寫 'Developed by Sandia National Laboratories, QUOPS is now available in NVIDIA CUDA-Q'，內文只寫 'A QUOPS reference implementation is available in NVIDIA CUDA-Q.'。**用內文的寫法。**
- **漏掉一句有份量的引言**：Grassellino 被引的第一句紀錄沒收——'Fault-tolerant quantum computing is the path to unlocking new scientific discovery, but getting there will require researchers to codesign algorithm, error correction, architectures and hardware together.' 有了這句，「協同設計」這個前提就能掛在一位具名的 Fermilab 主管身上，而不是只掛在 NVIDIA 自己的框架（F5）上。已逐字確認在新聞稿頁上。
- **QUOPS 預印本裡一個關鍵區分被漏掉**：arXiv 摘要寫 Google／IBM／Quantinuum 那批量測是 'computing directly on physical qubits'；只有另外那組八個 [[7,1,3]] 的 Helios-1 實驗用到邏輯量子位元。紀錄收了「5 個數量級」與 Helios-1 那句，卻沒收這個區分，**文章可能因此讓讀者以為跨平台結果來自容錯機器**。來源 `https://arxiv.org/abs/2609.12146`（200，2026-09-10 投稿，Timothy Proctor 等共 30 位作者）。
- **NVIDIA 自己的前瞻性聲明被當樣板丟掉了。** 它確實是樣板，但開頭就是 'statements as to: expectations with respect to quantum computing'——**NVIDIA 自己把量子運算列為本稿中「非歷史事實」的第一項**。這是比文章自己寫的任何但書都更硬的一手保留條款。

### live_data_warnings

- **sources 2–4 的 `/latest/` 是活網址**，今天描述 CUDA-Q 0.16.0／CUDA-Q Logical 0.1.1，版本一升就變。文件頁的 'Preview release' 警語、'shipped／exercised／out of scope' 三分法、以及「哪些功能未經測試」的清單（dynamic codes、code switching、concatenation、meta-checks、P2 block requests）**全都是現行版本的狀態**，要寫「2026-09-16 查核時」。
- `https://nvidianews.nvidia.com/releases.xml` 是 20 筆滾動視窗；查核當天 lastBuildDate 已從研究紀錄的 15:02:09 GMT 移到 15:00:48 GMT，feed 已經滾過。**feed 的筆數與最新日期不可寫進文章。**
- PyPI 上傳時間（cudaq-logical 0.1.1 於 2026-09-12T09:46:22Z、cudaq 0.16.0 於 09:46:42Z）與「cudaq-logical 只發行過這一版、8 個 wheel」是查核日的狀態。
- GitHub 倉庫 201 個分支是查核日計數（且查核者實測 `github.com` HTML 在本容器回 403，只有 `raw.githubusercontent.com` 與 `git ls-remote` 可用）。
- IEEE Quantum Week 2026 主辦方寫的 'exceeded 2,222 participants' 是活動頁上的宣稱數字，且該頁不在 sources 裡。
- `https://developer.nvidia.com/blog/feed/` 是 100 筆 Atom；用它證明「NVIDIA 沒有配套技術部落格」只在查核日成立。同一 feed 裡唯一的量子項目 `NVIDIA Ising Enables Fully Automated Quantum Computer Calibration...` 的 `<published>` 是 2026-07-27T16:00:00Z，**`<updated>` 是 2026-08-20T18:15:35Z——不要從錯的元素重新推日期。**

### source_list_fix

四條沒有超量，但有兩類問題：

1. **11 條事實掛在 9 個不在 `sources[]` 的網址**：`pypi.org/pypi/cudaq-logical/json`（2）、`research.nvidia.com/publication/2026-09_cuda-q-logical-...`（2）、`raw.githubusercontent.com/NVIDIA/cuda-quantum/main/README.md`、`.../main/LICENSE`、`.../preview/logical/getting-started/quickstart.html`、`raw.githubusercontent.com/sandialabs/PRAQTICE/quops/quops/README.md`、`arxiv.org/abs/2609.12146`、`qce.quantum.ieee.org/2026/`、`nvidia.github.io/cuda-quantum/latest/index.html` 各 1。F40–F43 有標「EXTRA URL」，其餘七條沒標。**用到哪一條就要換 source，否則不寫。**
2. **建議把 sources 2 與 3 改成 0.16.0 版本鎖定網址**（見 must_add），避免內容包一過版就描述不存在的狀態。
3. 沒有任何一條來自媒體、整合站或搜尋摘要；識別碼也都是從新聞稿 HTML 的 href 抽出來的（GitHub、QUOPS repository、CUDA-Q Logical 論文、arXiv:2609.12146），不是猜的。研究者另外主動揭露了一條猜錯後丟棄的網址（正確路徑是 `getting-started/quickstart.html`，回 200），這個做法要保留。

---
## tech-news-nvidia-mediatek-20260831

查核結果：needs_fixes，45 條確認、2 條推翻、7 條無法追溯。

### must_fix

1. 紀錄 verified_fact 0 寫「The announcement is dated August 31, 2026 and datelined Santa Clara, California. NVIDIA's newsroom page prints the date 'August 31, 2026'」，掛在 NVIDIA newsroom 網址；**那一頁完全沒有發稿地**——82,927 bytes 的頁面裡 'Santa Clara' 出現 **0 次**，只印一行 'August 31, 2026'。'SANTA CLARA, Calif.—AUGUST 31, 2026—' 只在**聯發科的英文新聞室頁**上，而那一頁不在四條 sources 裡。**改寫：NVIDIA 頁只有日期沒有發稿地；發稿地是聯發科英文頁的寫法。**
2. 紀錄 verified_fact 31 把 feed 的 pubDate／modDate 掛在 `https://nvidianews.nvidia.com/releases.xml?page=3`；**這個網址指不到它宣稱的文件**——每次抓都拿到預設的 20 筆滾動視窗（68,371 bytes，最舊 2026-09-01），'MediaTek' 命中 0 次。**pubDate 'Mon, 31 Aug 2026 12:30:00 GMT' 與 modDate 'Mon, 31 Aug 2026 12:35:28 GMT' 兩個值是對的**，但只在 `?page=7`／`?page=10` 拿得到，而且 NVIDIA 的 CDN 對 page 參數的伺服並不一致。**這個指標不可重現，不能當成來源。**
3. **結構性阻斷：verified_facts 33、34、35、44（MOPS 2026-07-31 董事會決議與 MOPS 2026 年度公告清單）、31（NVIDIA feed），以及 facts 0 與 32 中屬於聯發科英文頁的那一半，全部掛在不在 `sources[]` 的網址。** `sources[]` 只有四條（NVIDIA newsroom、聯發科 zh-TW、MOPS 定價公告、聯發科 6 月 RTX Spark 稿）。**整組董事會決議與「9 月迄今沒有完成發行的公告」的材料，文章目前都不能引用。**
4. 紀錄把 verified_facts 4、10、16、18、19、22、23 標成 `is_vendor_claim=false`；**這些是 NVIDIA 與聯發科對一個還沒出貨的平台的自我描述**——'a prevalidated path'、'enabling their platforms to evolve alongside future NVIDIA architectures'、'customers can focus resources on the differentiated compute ... while relying on NVIDIA and MediaTek for ...'、'Customers can bring their XPU designs to MediaTek and tailor connectivity, memory, packaging, performance and power characteristics'。依 BRIEF 要寫成「NVIDIA 表示」「聯發科表示」。而且旗標與性質相同的 17／21／24（標成 true）自相矛盾。**照旗標寫會把廠商宣稱印成事實。**
5. 紀錄 verified_fact 2 的 `verbatim_quote` 用 ' | ' 把兩個副標串在一起；**那是新聞稿 `<subtitle>` 裡兩個獨立的 `<li>`，' | ' 是研究者自己加的，頁面上沒有。**
6. 紀錄 verified_fact 42 寫「The bonds are offered/listed through the Singapore Exchange Securities Trading Limited, and proceeds will fund procurement of raw materials in foreign currencies」；**所附的 `verbatim_quote` 只涵蓋募資用途那一半，完全沒有提到新加坡交易所**。SGX 那半查核者另外確認過（'Place of Offering and Trading: Singapore Exchange Securities Trading Limited'），**事實為真但如紀錄所寫無法追溯到自己的引文，要拆開或補引文。**
7. 紀錄 verified_fact 40（轉換期間）引文正確**但被截短，掉了兩個條件**：期間本身是暫定的（'the Bondholders may, **tentatively**, at any time starting from ...'），而且受定義的 'Closed Period' 排除。**照現狀寫會把暫定期間寫成固定期間。**
8. 紀錄 verified_fact 18 寫「The NVLink Fusion platform is said to bring together **three named technologies**」；**新聞稿寫的是 'brings together the critical technologies surrounding a custom XPU, **including**:'**——including 明示非窮舉。**改寫成「以 including 引出的三個具名例子」。**
9. 紀錄 verified_fact 30 的 `verbatim_quote` 是**空字串**。那是一條「不存在」的主張（聯發科 zh-TW 頁沒有前瞻性聲明），查核者自己驗過為真（該頁 '###' → 關於聯發科技 → 關於 NVIDIA → 頁尾），**但紀錄應該寫出查證方法，而不是留一個空引文。**

### must_add

- **2026-08-31 的 MOPS 定價公告把 NVIDIA 列為「Non-related party」，並把認購目的寫成「Long-term strategic collaboration」——50 條事實裡一條都沒有。** 這是這份法定公告自己對這樁交易的定性，也正是台灣角度所依附的法定細節。
- **紀錄 fact 43 把賣回權觸發條件簡化成「listed triggering circumstances」，公告其實逐條列了**：'(a) In the event that the Company's shares of common stock cease to be listed on the Taiwan Stock Exchange (the "TWSE") or trading of such shares is suspended for 30 or more consecutive business days ... (b) Upon the occurrence of a change of control of the Company'。
- 同一份 MOPS 清單上還有 2026/07/31 的另外兩筆：20:44:14「The Board of Directors has approved the issuance of unsecured straight corporate bonds」與 20:42:20「Announcement of the Company's medium- to long-term fund-raising plan」。**這兩筆是 fact 34 那個 US$5 億上限合併計算的另一半。**
- **editorial_brief 的核心角度要加條件。** 「within about five minutes of each other」只有拿 NVIDIA feed 的 pubDate 比才成立（20:30 台北 vs 20:25:52 的公告，相差 4 分 08 秒）。**聯發科自己的英文稿時間戳是 2026-08-30 21:40:00 GMT**（頁面的機器可讀值與聯發科新聞室 RSS 兩處都確認），也就是 8 月 31 日台北時間 **05:40**，比 MOPS 公告早約 14 小時 45 分。紀錄在 fact 32 裡記了這個時間戳，卻用另一個時間戳搭角度。**文章必須寫明先後順序是用哪一個時間戳算的。**
- **查核者三次獨立比對、全部一致的 MOPS 定價數字，可以放心使用**：'Issue Amount: US$3,900,000 thousand'；'NVIDIA Corporation has subscribed for 17,500 certificates, for a total amount of US$3,500,000 thousand.'；'The Conversion Price of the Bond is NT$4,513.75 per share, which has been determined at 115% of the closing price of NT$3,925 per share of the Company's Common Shares on the TWSE on August 31, 2026'；'Coupon Interest: 0% per annum'；發行價格為面額 100%；'Tentative Issue Date: 2026/09/08'；'Tentative Maturity Date: 2031/09/08, the 5th anniversary of the Issue Date.'；'Place of Offering and Trading: Singapore Exchange Securities Trading Limited'；'the maximum dilution of shareholding would be approximately 1.67%'；'Denomination: US$200 thousand or in any integral multiples of US$100 thousand in excess thereof'；轉換為 'newly-issued common shares of the Company'；以及 90%／ROC 稅法變動的提前贖回條款。
- 2026-07-31 董事會公告同樣確認：'Total amount issued:Up to US$4 billion'、'Issuance period:Tentatively five years'、'Coupon rate:Tentatively 0%'、'Issue price:Tentatively set at 100% of face value'、'Use of the funds raised by the offering and utilization plan:Procurement of raw materials in foreign currencies'、'The aggregate issuance amount of these first issuance of unsecured overseas convertible bonds and the straight corporate bonds resolved on the same date by the Board of Directors shall not exceed US$5 billion.'
- **不要把兩個英文頁的小差異寫成兩件事**：NVIDIA 印 'NVIDIA RTX Spark™ and DGX Spark™'、'enterprise-class workstations'、'the NVIDIA MGX™ rack-scale architecture'；聯發科英文頁印 'RTX Spark ™ and DGX Spark ™'、'enterprise class workstations'、'the MGX™ rack-scale architecture'。
- 字串細節：zh-TW 發稿行是「2026 年 8 月 31 日 美國聖塔克拉拉訊 —」，**「美國」前面有一個空格**，`event_date_basis` 引的時候把它漏掉了。

### live_data_warnings

- **MOPS 公告清單頁是活頁面。** 「2026-08-31 之後沒有任何公告確認債券發行完成」是 **2026-09-16 當天**的狀態；9 月的列是 09/02 17:23:36 法說會、09/03 18:38:39 RSA 資本額變更登記、09/10 16:56:15 八月營收、09/11 18:04:28 聯發科新加坡子公司。**2026/09/08 的發行日到查核日為止仍必須寫成「暫定」。**
- `https://nvidianews.nvidia.com/releases.xml` 是 20 筆滾動視窗，且 **CDN 對 `?page=` 參數的伺服不一致**（同一個 page=3 有時給 68,371 bytes 的預設窗、有時 page=7／page=10 才給到 8 月）。**不可把 feed 位置寫成穩定的來源。**
- 聯發科新聞室 RSS `https://www.mediatek.com/press-room/rss.xml` 只有 10 筆（最新 2026-09-15）。
- 兩個英文頁與 zh-TW 頁的位元組數（82,927／96,271／109,693／101,749）是快照。
- **NVIDIA 新聞室有軟性 404 陷阱**：`https://nvidianews.nvidia.com/news/nvidia-and-mediatek-deepen-long-standing-partnership`（少了後半段）回 **HTTP 200**、68,863 bytes，但 `<title>` 是 `News Archive | NVIDIA Newsroom`。**只看狀態碼會把一頁封存列表當成新聞稿。**

### source_list_fix

四條沒有超量，但第 3 條有可刊性問題，而且掛外事實比例偏高：

1. **`sources[2]` = `https://emops.twse.com.tw/server-java/t05st01_e?step=1&co_id=2454&spoke_date=20260831&spoke_time=202552&seq_no=3` 用 curl 會回 HTTP 200 加一個 800 bytes 的安全阻擋頁（"FOR SECURITY REASONS, THIS PAGE CAN NOT BE ACCESSED"）。** 研究者是用 WebFetch 讀到真正的公告（三次不同提示的結果一致）。**這條網址帶著 `checked_on` 刊出去，會讓讀者點到阻擋頁。** 研究紀錄必須寫明取得方式；若要保留為公開來源，需另尋 MOPS 的可直接開啟路徑。
2. **5 條事實掛在 3 個不在 `sources[]` 的網址**：MOPS 2026-07-31 董事會公告（2 條）、MOPS 2026 年度公告清單（2 條）、`nvidianews.nvidia.com/releases.xml?page=3`（1 條）。其中 releases.xml?page=3 **不可重現**，不能當來源。
3. 聯發科**英文**新聞室頁不在 sources 裡，但 facts 0 與 32 有一半靠它。要寫「SANTA CLARA, Calif.」發稿地或英文頁時間戳，就得換 source。
4. 沒有任何一條來自媒體、整合站或法律事務所部落格；四條全是一手。MOPS 的 `spoke_date`／`spoke_time`／`seq_no` 也不是猜的——查核者在清單頁上確認 2026/07/31 20:43:51 與 2026/08/31 20:25:52 兩列存在且主旨相符。

---
## tech-news-nvidia-vera-rubin-20260915

查核結果：needs_fixes，42 條確認、5 條推翻、6 條無法追溯。

### must_fix

1. 紀錄 F15 寫「**Rack-level** power claims NVIDIA made on the day: up to 40% more GPUs within the same site-power envelope and up to 35% higher token throughput」；**層級寫錯**——來源把這兩條放在**廠級（factory level）**：'At the factory level, NVIDIA DSX MaxLPS dynamically shifts power across racks as demand rises and falls. The payoff is significant: [40% / 35%]'。**下一句才是機櫃層級**：'Inside each rack, Intelligent Power Smoothing software and expanded energy buffering absorb short spikes'。**改寫成廠級。**
2. 紀錄 `sourcing_notes`（連同 `unverified_or_excluded` 與 `corrections_to_candidate_list`）寫「頁面的 LinkedIn 分享字串寫 'DSX Platform Advances'，`<title>`／h1 寫 'DSX Platform Advancements'」；**反了**——`<title>` 元素本身寫的是 'Advances'（Yoast SEO 標題），JSON-LD 的 WebPage `name` 也是；'Advancements' 才是 h1、og:title、JSON-LD headline 與新聞室 RSS `<title>` 的寫法（7 次對 2 次）。**而且根本沒有 LinkedIn 分享字串這回事。** 結論（用 'Advancements'）正確，但依據錯了，照它去找會找錯元素。
3. 紀錄 `not_said` 寫「'pricing' appears once each, and only in the phrase 'pricing signals'」；**對高峰會那篇成立、對同日的配套那篇不成立**——`from-megawatts-to-tokens` 裡唯一的 'pricing' 是 'pricing **events**'（DSX at a glance 側欄：'Receives grid signals (load-shedding, demand-response, pricing events)'）。更大的論點仍然成立：兩篇 'price' 皆 0 次。
4. 紀錄 `not_said` 寫「The only dated commitment **anywhere** is January's 'available from partners the second half of 2026', which has not been narrowed」；**「anywhere」被 NVIDIA 自己的材料推翻**——配套那篇的 'Numbers at a glance' 表寫 '3-5% end-to-end efficiency gain (projected) / 800V DC vs. 54V distribution; available with Vera Rubin NVL72 **2027**'，而且研究者自己在 F29 就記了這筆；Groq 3 LPX 開發者部落格寫 'in H2 2026'；NVLink 6 那篇寫 cuda-checkpoint GA 'expected by the end of the year'。**把這條限縮到「單位數／出貨量／地區數字」，不要講成所有日期。**
5. 紀錄 `not_said` 與 `must_not_write` 寫「NOTHING ABOUT TAIWAN ... 兩篇 9 月 15 日的公告裡 Taiwan 與 TSMC 都是零次出現」；**字串層面為真（各 0 次），但寫法會擋掉一個來源確實有寫的事實**——配套那篇寫 'Introduced at **GTC Taipei** in May, NVIDIA DSX is that answer for the AI factory'，那是唯一一句有來源的「DSX 在哪裡發表」，而且是一場在台灣辦的 NVIDIA 活動。**改寫成：沒有台灣部署、台灣夥伴或供應鏈說明，但 DSX 的發表場合是 GTC Taipei。**
6. 紀錄 F38 寫「The product is 'NVIDIA Groq 3 LPX' (the rack-scale accelerator) and the chip inside it is the 'NVIDIA Groq 3 LPU'」並掛 Groq 3 LPX 新聞稿；**'Groq 3 LPU' 這個字串在那篇新聞稿裡完全不存在**（'LPU' 只出現一次，在商標註記）。新聞稿把 Groq 3 LPX 稱為 'the **interactive AI inference** accelerator'，不是 'rack-scale accelerator'。**產品名這件事有一手來源，但在另一頁**：`blogs.nvidia.com/blog/vera-rubin-nvl72-efficiency-ai-agents/` 寫 'the full platform is a seven-chip architecture that also includes the NVIDIA Vera CPU, Groq 3 LPU, NVLink 6 Switch, BlueField-4 DPU, Spectrum-6 SPX and ConnectX-9 SuperNIC'。**改掛網址。**
7. 紀錄 F37（以及 F48 與 editorial_brief 的「第七顆 Groq 3 LPU 是 8 月 24 日 Hot Chips 宣布的」）寫「**THE SEVENTH CHIP** WAS ANNOUNCED ON 2026-08-24」；**所引的新聞稿只寫** 'Through extreme codesign across seven chips and five purpose-built racks, NVIDIA Vera Rubin is the most extensive AI factory platform.'——**它沒有列舉那七顆、沒有說 Groq 3 LPX／LPU 是「第七顆」、也沒有說那天宣布的就是第七顆。** 「一月六顆＋八月七顆＝新增的那顆是 LPU」是研究者的算術。要用「第七顆」這個框架，就必須引 `blogs.nvidia.com/blog/vera-rubin-nvl72-efficiency-ai-agents/`。
8. 紀錄 F42 寫「It also gives an approved Vera Rubin MaxP rack Thermal Design Power of 227 kW」並掛 `https://docs.nvidia.com/dsx/maxlps/overview`；**那個網址給 curl 的 HTML 裡沒有 '227'、沒有 'kW'、沒有 'Thermal Design Power'**（機櫃頁籤是前端渲染；檔案裡唯一的 '227' 是 SVG path 座標）。**數字是真的、也是一手，但在 `https://docs.nvidia.com/dsx/maxlps/overview.md`**：'Using an approved Vera Rubin 227 kW MaxP Thermal Design Power (TDP) as the fixed per-rack allocation basis...'。F42 其餘部分（固定 1 MW 下 MaxLPS 可放 400 顆 GPU、token 吞吐為 MaxP 的 1.35 倍、PUE 1.1、'Vera Rubin testing remains in progress'、NVOnline #1161311）在 HTML 裡確實有。**把 227 kW 拆到 `.md` 網址。**
9. 紀錄 F22 寫「NVIDIA states DSX was introduced at GTC Taipei in **May 2026**」；**頁面只寫 'Introduced at GTC Taipei in May'，沒有年份**（'May 2026' 在該頁 0 次命中）。推論幾乎一定對，但依不猜規則，**年份追溯不到這個網址，要刪掉或另尋來源**。
10. 紀錄 F34 寫「NVIDIA **also offers** HGX Rubin NVL8, a server board linking eight Rubin GPUs over NVLink for x86-based platforms」；**一月的新聞稿寫的是 'NVIDIA **will also offer** the NVIDIA HGX Rubin NVL8 platform'**。用現在式會把一月的前瞻敘述變成現在的供貨狀態，正是 BRIEF 警告的「宣布」與「上市」混淆。**2026-09-15 的材料沒有更新 NVL8 的供貨狀態。**
11. 紀錄 F03 寫「Amazon's Annapurna Labs is working with NVIDIA on NVHBM, **NVIDIA's** custom high-bandwidth memory technology」；**頁面寫的是 'the NVHBM custom high-bandwidth memory technology'，沒有講歸屬**，「NVIDIA 的」是研究者加的。NVIDIA 2026-08-26 的開發者部落格確實把 NVHBM 當成自家技術，但那條網址不是這條事實掛的網址，而且查核者確認**那篇部落格裡 'Annapurna' 與 'Amazon' 皆 0 次**，也撐不起合作那一半。

### must_add

- **NVIDIA 自己的配套文章對矽谷電力事件前後不一，紀錄把兩個數字都收了卻沒發現衝突。** 內文兩次都寫成 4 MW 降到 3 MW（'power dropping from four megawatts to three, automatically'；'power fell from four megawatts to three'），即 25%；但 'Numbers at a glance' 表把同一事件寫成 '**40%** | power demand reduction in under a minute | SVP automated response, Flexible Load Interconnect Program | Emerald AI / Future DSX Flex'。**F24 收了 4→3 MW、F29 收了 40%、editorial_brief 的圖解用 4 MW 降到 3 MW——同時用會自相矛盾。** 要嘛擇一並寫明出自該文哪一部分，要嘛寫明 NVIDIA 對同一事件有兩種描述。
- **F44 漏掉一個關鍵限定**：DSX MaxLPS 工程部落格的 125 kW→90 kW（GB200 NVL72）與 136 kW→101 kW（Vera Rubin NVL72）**不是同條件對比**——原文寫 'Vera Rubin NVL72 was tested with DeepSeek-R1, while GB200 NVL72 was tested with Kimi-K2.5'。39%／35% 的多放機櫃數與約 1.5 倍／1.3–1.4 倍的每瓦效能是建立在**不同模型**上的。
- **1.6 倍 MLPerf 那個數字漏了限定**：高峰會那篇無條件寫 'NVIDIA's MLPerf Inference v6.1 submissions delivered up to 1.6x higher performance than v6.0 through software optimizations alone'，但 MLPerf 專文把它綁在單一平台與單一模型：'In v6.1, GB300 NVL72 performance on Qwen3-VL improved up to 1.6x over v6.0 results.'**要用就用有限定的版本。**
- **F46 漏掉一句**：MLPerf 專文寫 'Nebius also submitted Vera Rubin NVL72 preview results and demonstrated excellent performance'——**NVIDIA 不是唯一提交 Vera Rubin 成績的一方**。同一篇也把 SemiAnalysis AgentX 的 30 倍描述成 'in preview testing'，比高峰會那篇的任何說法都保守，很適合放進「怎麼讀廠商數字」那一節。
- **15 倍那個數字的出處（F17）**：高峰會那篇寫 'roughly 15x the token volume of a simple chat request' 沒有註明來源，但 `blogs.nvidia.com/blog/vera-rubin-nvl72-efficiency-ai-agents/` 開頭寫 'According to **OpenRouter** data, agentic AI workloads consume 15x more tokens than a simple chat request.'**那是 NVIDIA 轉述的第三方資料，不是 NVIDIA 的量測，文章要寫明。**
- **F43 的 Lambda 案例研究要加註**：研究者正確依 tech.md 排除了 `nvidia.com/en-us/data-center/lpx/`（產品行銷頁），但 Lambda 案例研究就在同一個商業網站上。它的數字（GPT-OSS-120B 每節點 40 QPS、約 4.04M→約 5M tokens/sec、80% 政策下 10+10 節點時混合推論 +20%／混合訓練 +17%、'may be well positioned to deploy'）逐字都在，**但那是 NVIDIA 發布的、關於夥伴測試的材料，要寫成「NVIDIA 轉述 Lambda 的測試」，而且工程部落格有重複的數字時優先用工程部落格。**
- 結構提醒：**F41–F47 全部掛在不在四條 `sources[]` 內的網址**（developer.nvidia.com 三條、docs.nvidia.com、nvidia.com 案例研究、另外兩篇 blogs.nvidia.com）。研究者標了「swap-in」，研究紀錄這樣沒問題，**但內容包 4 條上限意味著：用了那些數字，`sources` 就要跟著換。**

### live_data_warnings

- **高峰會那篇是活文件，而且在查核期間又動過**：`article:published_time` 2026-09-15T16:55:40+00:00、`article:modified_time` **2026-09-16T14:57:15+00:00**（重抓時 134,585 bytes 未變）。新聞室 RSS 給的 modDate 是 Tue, 15 Sep 2026 16:57:47 GMT，**比頁面自己的 dateModified 落後一天**。引用要寫「2026-09-16 讀取」。
- `https://nvidianews.nvidia.com/releases.xml` 恰好 20 筆，channel lastBuildDate Wed, 16 Sep 2026 15:02:09 GMT，最新一筆 2026-09-16。**滾動視窗。**
- `blogs.nvidia.com/blog/vera-rubin-nvl72-mlperf-inference/` 的發布時間是 **2026-09-16T15:00:48Z——事件日的隔天**。`blogs.nvidia.com/blog/vera-rubin-nvl72-efficiency-ai-agents/` published 2026-08-24T15:00:19Z、modified 2026-09-15T23:52:27Z。`developer.nvidia.com` 的 DSX MaxLPS 那篇 published 2026-08-24T15:00:00Z、modified 2026-08-31T20:56:08Z。**每一篇都要各自標日期，不可混用。**
- **NVIDIA 自己說 Vera Rubin 的電力數字還沒測完**：DSX 文件寫 'Vera Rubin testing remains in progress'；DSX MaxLPS 工程部落格寫 Dynamic Power Software（DPS）與 DSX Exchange 'currently in Developer Preview'。**所有 Vera Rubin 的功耗數字都要寫成推估。**
- `docs.nvidia.com/dsx/maxlps/overview` 的機櫃頁籤是前端渲染，**curl 拿不到表格**；同一份內容的 `.md` 版本才有。頁面狀態隨時會變。

### source_list_fix

四條沒有超量、全部可達、全部是 nvidia.com 財產，但：

1. **7 條事實掛在 7 個不在 `sources[]` 的網址**（F41–F47）：`developer.nvidia.com` 的 Groq 3 LPX 篇、NVLink 6 篇、DSX MaxLPS 篇，`docs.nvidia.com/dsx/maxlps/overview`，`www.nvidia.com/en-us/case-studies/lambda/`，`blogs.nvidia.com/blog/vera-rubin-nvl72-mlperf-inference/`，`blogs.nvidia.com/blog/vera-rubin-nvl72-efficiency-ai-agents/`。**用哪一個數字就要把對應網址換進 sources。**
2. 另有兩條 must_fix 會再擠壓名額：「第七顆晶片」框架與 Groq 3 LPU 名稱都必須改掛 `vera-rubin-nvl72-efficiency-ai-agents`；227 kW 必須改掛 `docs.nvidia.com/dsx/maxlps/overview.md`。**四條上限下，這些不可能全部塞進去，要先決定文章要不要寫這些。**
3. F00 的全部內容（場地 Santa Clara Convention Center、日期、Ian Buck 職稱、'Coachella of infrastructure tech' 這個形容）**只有 NVIDIA 自己的部落格一個來源**。出席人數已正確標成廠商宣稱，**場地與形容詞同樣不可寫成已獨立確立的事實**。
4. 沒有媒體、整合站或搜尋摘要；MLCommons 提交編號 6.1-0106／6.1-0074／6.1-0073 與 'NVOnline #1161311' 都經查核者獨立確認存在，不是猜的。

---
## tech-news-pixel-drop-20260915

查核結果：needs_fixes，42 條確認、5 條推翻、4 條無法追溯。

### must_fix

1. 紀錄 `not_said[11]` 寫「blog.google 的相關報導欄顯示另有一篇 'September Android Drop'，Pixel Drop 那篇沒有提到它」；**被推翻**——查核者抓到的頁面裡 'Android Drop' 出現 **0 次**，相關報導欄只有四項：'You can officially buy the Pixel 11 phones and Pixel Watch 5.'、'Here's how to use sign-to-text translation on Pixel 11.'（Sharlene Yuan）、'Get closer to the game with Gemini and Pixel'（Eileen Mannion）、'Stay present while taking pictures with Magic Capture on Pixel 11.'；探測 2026 年 9 月 Android Drop 的網址回 404。**整句刪掉**，否則會誘導撰稿者去提一篇無法證明存在的文章。
2. 紀錄 verified_fact 1 寫「The browser-tab/**og** title is shorter: 'September Pixel Drop: VIP updates, Pixel Watch features.'」；**部分被推翻**——`og:title` 與 `twitter:title` **都是完整標題** 'September Pixel Drop: New Pixel VIP updates, Pixel Watch features, and more'，只有 `<title>` 元素是短版。**「og title」這個說法是錯的。**
3. 紀錄 verified_fact 36 寫 Offline Gemini「**Four** example actions are named」；**被推翻**——Google 只列三個（'setting up a timer, starting/stopping a workout, turning on do not disturb'），後面接的 'and other device actions' 是概括語，不是第四個具名動作。**改寫成三個具名例子加一個開放式結尾。**
4. 紀錄 verified_fact 26 寫註腳 5 是「Google 對 VIP 小工具與哈利波特兩列**唯一**的供應狀況但書」；**部分被推翻**——Disclaimer 2 也限制哈利波特那一列：'Harry Potter Audiobook Packs available until December 31, 2026.'。**這句只對 Pixel VIPs 那一列（與 Pause Point）成立。**
5. 紀錄 verified_fact 12 寫「so the **five** named features are explicitly not the complete list」；**數錯了**——'Here are just some of the features to look forward to' 底下的功能標題只有**四個**：'Pixel VIPs updates'、'Harry Potter Audiobook Packs'、'Scam Detection comes to your keyboard and expands to new regions'、'Pause Point expands to more Pixel devices'。五是供應狀況圖表的**列數**（Scam Detection 在圖表裡拆成兩列）。**寫「Google 列出五項功能」不符合 Google 的正文。**
6. 紀錄 verified_fact 40 寫手錶公告「以 'General bug fixes and improvements' 結束功能列表、**署名** 'Thanks, Google Pixel Watch Support Team'」；**署名在公告靠前的位置**（緊接在安全公告那一行之後），不是結尾；公告是以 'Previous Pixel Watch Updates' 結束。**現在的寫法暗示有一個結尾簽名，實際上沒有。**
7. 紀錄 verified_fact 41 寫該串列出「Google 在 **2026 年**的前幾次 Pixel Watch 更新」；**公告裡任何地方都沒有寫年份**——看得到的標籤只有 'June (Pixel Watch 2, 3, & 4)'、'March EMR (Pixel Watch 1)'、'March (Pixel Watch 2, 3, & 4)'。年份只存在於連結的 href（`.../google-pixel-watch-update-june-2026`、`.../google-pixel-watch-update-march-2026`、`.../pixel-watch-1-modem-software-update-march-2026`）。**事實保留，但年份要註明來自連結網址。**
8. 紀錄 verified_fact 20 寫該公告「links back to Google's own November 2025 Pixel Drop post **as its origin**」；**href 確認無誤，但 Google 從沒說這個功能源自那一篇**。'as its origin' 是推論。**改寫成「連到 Google 2025 年 11 月的 Pixel Drop 文章」。**
9. 紀錄 verified_fact 35 的 Proactive suggestions 引文在 'surfaces it directly on your wrist' 就停住、**沒有加刪節號**；原文還有 ', eliminating the need to dig through your phone'。語意不變，但 `verbatim_quote` 是翻譯會照抄的欄位。

### must_add

- **手錶公告的日期，是這份紀錄最大的漏網之魚，而且把一條排除項變成可用的發現。** 研究者解出手錶討論串的內部時間戳（貼文 2026-09-01T19:47:42Z、後續活動 2026-09-03T17:28:18Z）卻以「未公開的內部欄位」為由排除。查核者做了校準：討論串 442344064 'Google Pixel Watch Update - June 2026' = 2026-06-16、414486587 'Google Pixel Watch Update - March 2026' = 2026-03-03、417704094 'Pixel Watch 1 Modem Software Update - March 2026' = 2026-03-16，**其中兩筆與 Pixel Watch 安全公告自己標示的發布日完全吻合**（6 月公告 2026-06-16 發布、3 月公告 2026-03-03 發布）。也就是說 **Pixel Watch 5／Wear OS 7 那則公告比 Pixel Drop 部落格早約兩週**。研究者的實務指示（不要寫成「Pixel Watch 5 的 Wear OS 7 更新是 9 月 15 日宣布的」）正確，**應該從 `unverified_or_excluded` 提升到 `must_not_write`**。**但也不要把 2026-09-01 當事實印出來**——公告裡的版本號是 CP3A.260905.002，260905 這個戳記晚於 9 月 1 日，代表公告貼出後被編輯過。**只能寫「Google 在 Pixel Drop 文章之前就發布了手錶公告，而且那則公告沒有可見日期」。**
- **反方向的日期佐證**：同一個欄位在 Pixel Drop 手機討論串解出 2026-09-15T18:27:40Z，比部落格 JSON-LD 的 `datePublished` 18:00:00Z 晚 27 分鐘。**`event_date` 2026-09-15 與 slug 後綴現在是雙重確認。**
- **說明中心那一頁沒有任何日期**：`support.google.com/pixelphone/answer/16704479` 沒有可見的發布或更新日期、沒有 `dateModified`、沒有 JSON-LD，檔案裡唯一的 'Last updated' 字串是 JavaScript 樣板。**所以 11 個地區／8 種語言只能寫成「2026-09-16 讀取時的頁面狀態」，絕不能寫成「9 月 Drop 之後就是這樣」。這一點要補進 `not_said`。**
- **說明中心沒有寫機型條件**：該頁的 'Check feature eligibility' 一節**只列地區與語言**，沒有講任何 Pixel 機型要求，但論壇公告寫 'Pixel 6 and newer'、圖表也從 Pixel 6／6a 起跳。**Google 兩個頁面給的適用範圍不同，不可以把說明中心那份清單當成完整的適用條件。**
- **整段漏掉的內容：Circle to Search／Google Lens。** 所引說明中心頁有一整節 'Use Circle to Search & Google Lens to spot scam messages'，兩者各有操作步驟，並寫著 'Our systems will use AI and information from the web to assess whether the message is likely a scam.'**Google 沒有對這條路徑加上任何地區或語言限制。** 對台灣讀者而言這是該頁最有用的一件事，因為它是唯一不被 11 個地區清單擋住的防詐路徑。**但必須註明它是靠 AI 與網路資訊判讀的功能，與裝置端的 Scam Detection 不同，兩者不可混為一談。**
- **同一頁上有三種不同的「Scam Detection」**：通話層級（'On eligible Pixel phones, you can get real-time alerts if a call shows patterns commonly associated with scams'）與 Google Messages 垃圾訊息（'The Google Messages app automatically detects and moves suspected spam into a dedicated folder'），紀錄兩者都沒收。**本次 Drop 講的只有聊天通知與鍵盤兩種變體，文章不可以把三件事混在一起。**
- 論壇公告的兩個連結目標可以取代「讀出來的」推論：'Update to the latest Android version' → `support.google.com/pixelphone/answer/7680439`；'update your apps' → `support.google.com/googleplay/answer/113412`。**這用 Google 自己的 href 佐證了紀錄 verified_fact 11 的雙管道說法。**
- 手機討論串還有第二張紀錄沒提到的圖：`thread-466181739-10255076335878498553.png`（'Gstore_1156 x 650.5.png'，1,195,593 bytes，2312x1301）。**那是版頭美術圖，不是第二張資料表**，記下來免得後續代理誤認。

### live_data_warnings

- **裝置適用矩陣是從一張 PNG 數出來的。** 查核者用偵測格線、逐格數深色像素的方式獨立重數，結果與紀錄一致：**25 個裝置欄、5 個功能列**，五列裡第 1–24 格都有勾記（30–35 個深色像素），第 25 格 Pixel Tablet 為 0。圖表裡 '(AR, DE, ES, FR, DE, PT, and JA)' 重複的 'DE' 六倍放大後確認是 **Google 自己的瑕疵**。這是紀錄裡最容易出錯的部分，而它正確——**但它仍然是一張圖的快照，而且 Pixel Tablet 那一列是空白列，Google 從沒寫「Pixel Tablet 不支援」，只能寫「Google 的表格沒有為 Pixel Tablet 標記這五項功能」。**
- 說明中心 `answer/16704479` 的 **11 個地區／8 種語言是累計數字，而且該頁沒有任何日期**（見 must_add）。論壇公告的 9 個國家／6 種語言是這次新增。**兩組數字不可互換。**
- **截至 2026-09-16 沒有 2026 年 9 月的 Pixel Watch 安全公告**：`source.android.com/docs/security/bulletin/pixel-watch` 最新是 2026 年 8 月（2026-08-20 發布、修補等級 2026-08-05），頁尾寫 'Last updated 2026-08-20 UTC'。**這是查核日快照。**
- 兩個到期日是固定的但仍要標查核日：哈利波特有聲書包 **2026-12-31**、Audible 優惠 **2027-01-14**。
- `blog.google/intl/zh-tw/products-and-platforms/devices/pixel/september-2026-pixel-drop/` 回 **404**（而 `blog.google/intl/zh-tw/` 回 200），也就是 **Google 沒有出繁體中文版**。台灣讀者只有英文原文與 Google 自己標註「這個頁面可能含有使用 AI 技術翻譯的內容，也許會有錯誤」的機器輔助中文頁。
- 兩個支援討論串的內文**不在一般 HTML 裡**，藏在雙重轉義的 inline JSON 中，要反轉義 `\uXXXX`／`\xXX` 才讀得到。頁面位元組數（389,352／2,060,182／1,898,242／1,681,250）是快照。

### source_list_fix

**結構乾淨：50 條事實全部掛在四條 sources 之內，沒有掛外網址，沒有超量，四條全是 Google 自有財產。** 只有三點要記進研究紀錄：

1. 來源 2 與 3 的內文需要反轉義才讀得到（見上）；來源 1 可在 `blog.google/rss/` 裡以完整標題找到，**網址不是猜的**。
2. 來源 4 是經由 Google 自己的連結 `https://support.google.com/pixelphone?p=scam_detection` 轉到 `answer/16704479` 確認的，**answer id 不是猜的**——這一點要寫在紀錄裡。
3. 來源 4 **沒有任何日期**，引用時一律寫「2026-09-16 讀取的頁面狀態」。

---
## tech-news-taiwan-6g-spectrum-20260910

查核結果：needs_fixes，僅 22 條確認、4 條推翻、8 條無法追溯。**28 條事實裡有 12 條出問題，是本垂直比例最高的一篇，而且 `editorial_brief` 本身有三處要改。**

### must_fix

1. 紀錄 F12（及 F11）寫程式計畫頁 19090 的「副標寫『6G頻譜政策領航計畫』」，`verbatim_quote` 是 `6G 地空整合頻譜規劃計畫 ／ 6G頻譜政策領航計畫`；**被推翻**——「6G頻譜政策領航計畫」在 19090 只出現兩次，兩次都在 HTML 的 `<meta name="description">` 與 `<meta property="og:description">`，**可見頁面上沒有這行字**。母清單頁 `/digital-affairs/resource-management/programs/462` 把卡片顯示為「6G 地空整合頻譜規劃計畫」加日期 2026-03-05，沒有副標。**那個帶「／」的 `verbatim_quote` 在任何頁面上都不存在。**
2. 紀錄 F11 寫「研討會名稱『頻譜政策領航』就是從這個計畫來的」；**純屬推論**——新聞稿 20612 從未提到這個計畫，計畫頁 19090 從未提到這場研討會，兩者之間沒有任何連結，而「頻譜政策領航計畫」這個詞只存在於 meta 標籤。**不要寫這個因果。**
3. 紀錄 F14 寫 programs/19090 上那 9 份報告「封面與封底都印『本報告不必然代表數位發展部意見』」（同一說法也出現在 `unverified_or_excluded` 對 115年第七期月報與第二季季報的描述）；**被推翻**——查核者下載全部 9 份抽文字：7 份月報（115年第一～七期國際頻譜趨勢月報）各出現 2 次，正確；**但兩份季報都是 0 次**（115年第一季頻譜發展趨勢季報 = 0、115年第二季頻譜發展趨勢季報 = 0），而且兩份都沒有「不必然」「免責」「不代表」「僅供參考」任何字樣。**全稱句為假，對第二季季報的具體說法也是假的。**
4. 紀錄 `sourcing_notes` 用「數位通傳資源規劃專區三個子區（6GHz 最新 2023-08-25、衛星頻段最新 2025-02-13、無人載具）沒有更晚的公告」當作 114年2月供應計畫仍屬現行的間接證據；**被推翻**——無人載具子區最新一筆是 plan003/15424「公告修正案｜無人載具科技創新實驗條例」，建立日期 **2025-02-27**，晚於 2025-02-13。**結論仍成立**（查核者拉出 15424 的四份附件：車聯網 5850-5925MHz 實驗場域公告與無人載具條例頻率公告及其修正，都沒有修訂無線電頻率供應計畫），**但這個依據是錯的，不可重複使用。**
5. 紀錄 `not_said` 寫「新聞稿裡唯一的數字是 2030 和日期 10」；**被推翻**——五段本文裡有 10、2030、5（第5研究組）、6（6G）。**實質論點仍成立**（查核者獨立確認本文 0 次出現 決定／核定／公告／釋出／拍賣／MHz／GHz／頻段），但這句話寫成這樣讀者一查就能推翻。
6. 紀錄 F17 的結尾寫「前三組合計 280 MHz、2030 年到期，就是『4G屆期頻譜重耕』所指的頻段」，`editorial_brief` 更把「三組合計 280 MHz 的 4G 頻段執照期限到民國 119 年（2030 年）」當成全篇最有價值的角度；**這是研究者自己的推論，追溯不到任何來源**。表格每一格都對（703-748/758-803 = 90MHz；885-915/930-960 = 60MHz；1710-1775/1805-1870 = 130MHz；三組執照期限皆至 119 年；皆自 102 年 12 月起開放），**但供應計畫 PDF 全文 4G／5G／6G／IMT／重耕 各 0 次**，只寫「供行動寬頻業務使用」；計畫頁 19090 寫「4G屆期頻譜重耕釋出」卻沒有點名任何頻段。**把兩者接起來、稱它們為「4G 頻段」沒有來源；「280 MHz」也是研究者自己加的總和，官方文件沒有這個數字。這個角度要重寫或放棄。**
7. 紀錄 F11 寫 2025-09-17「數發部**辦過**次世代通信頻譜展望國際座談會」；**頁面 17422 寫的是「數位發展部林宜敬部長今（17）日出席」（出席），標題是「成功舉行」，全頁沒有說數發部是主辦。** 對照 20612 明寫「數位發展部今（10）日舉辦」。**兩場活動不可以用同一個動詞描述。**
8. 紀錄 F20 把英文句 'Study Group 5 is also responsible of the development of IMT and is currently working on IMT-2030 for the 6G' 掛在 ITU SG 5 網頁；**那句在 SG 5 頁面 HTML 裡 0 次命中，它在 R-GEN-SGB-2025-PDF-E.pdf 第 44 頁。** F20 自己的敘述也自相矛盾（「SG 5 頁寫 X … 等同的敘述在 ITU-R 手冊裡」）。SG 5 頁實際寫的是 'Terrestrial services / Systems and networks for fixed, mobile, radiodetermination, amateur and amateur-satellite services' 與 'Working Party 5D (WP 5D) - IMT Systems'。**要用那句就要改掛 PDF 網址。**
9. 紀錄 F25 把 E5RrlYLBIF6IfLS 稱為「數發部 115 年度（2026）施政計畫」，只對 116 年度那份堅持標「草案版」（F26）；**數發部自己的索引頁 `/information-service/govinfo/administrative-plans/1049` 把該連結標為「數位發展部115年度施政計畫（草案版）」**，和 116 年度那份一樣有草案標記，而 114／113／112 年度的條目沒有。**同一頁上兩份檔案卻用了兩套標準，兩份都要標草案版。**
10. `editorial_brief` 把 6425-7125 MHz 稱為全國可用的「**測試實驗頻率**」；**供應計畫的用語是「特定實驗頻率」**（第 3 頁定義，表頭也是「特定實驗頻率(MHz)」）。「測試實驗」是那一列「實驗目的」欄裡「…測試實驗網路之用」的片段，不是類別名稱。**`must_not_write` 也重複了同一個錯誤用語，兩處都要改。**
11. `editorial_brief` 第 (2) 節要求用供應計畫的「短期／中期／長期」解釋「已排程 vs 還在觀察」，並以「頻段／現況／執照到期年」表格作結；**這會逼撰稿者造一個文件裡沒有的欄位**。6425-7125 MHz 位於「(四)實驗網路」表，該表只有 特定實驗頻率／實驗目的／特定實驗場域／其他測試條件 四欄，**根本沒有優先順序欄**；而三組 119 年到期的頻段在「優先順序」欄全部標「-」，註 *2 說明已指配頻段在期限屆滿前不列優先順序。**文章的兩個主力頻段都沒有短／中／長標記。這一節要重新設計。**
12. `editorial_brief` 寫「**現行**『無線電頻率供應計畫』（114年2月修正）」；**同一份研究紀錄的 `sourcing_notes` 與 `unverified_or_excluded` 都說 law.moda.gov.tw 回 403、無法確認現行性，並指示撰稿者寫「114年2月修正版」而不是「現行版」。** `editorial_brief` 自打嘴巴，照抄就會違反紀錄本身的指示。

### must_add

- **供應計畫 PDF 全文 6G 與 IMT 各 0 次。** 這比紀錄寫的任何 `not_said` 都更有力：台灣唯一具法規效力的頻譜文件（研究者自己引了「本計畫屬實質法規命令性質…正式公告後對外將產生一定法律效果」）**完全沒有出現「6G」這個詞。**
- **研究者漏掉了唯一一條已經生效的地空共用規則——正好就是葉寧說還要建立的東西。** 供應計畫第 21–22 頁（衛星固定）：「申請使用27900-29500MHz頻段設置同步／非同步衛星固定通信者，應與既有行動寬頻業者完成協議，包含頻率發生干擾之處理程序，並經主管機關核配」，接著「本次開放頻段保留供未來行動通信使用。既有同步／非同步衛星固定通信設置者不得干擾行動通信且須忍受行動通信干擾之條件下使用」。第 18 頁有行動衛星的對應條文。**這比 6425-7125 MHz 更切題，而且是現行規定，不是研討會上的說法。**
- **真正能撐起「短／中／長」討論的列**：全份計畫裡唯二標「短」的是兩列衛星通信（1518-1559 等行動衛星；3610-4200 等衛星固定）；行動業務表裡唯一有優先順序的是 4700-4800／4900-5000 MHz，標「短/中」（現況「供公部門中繼微波系統使用」，未來規劃「與既有使用者進行協商，進行清移頻規劃」）。長期的例子是 632-652/678-698 MHz 與 2300-2390 MHz，兩者皆「視國際發展及國內使用需求再作評估規劃」。
- 其他可用但紀錄沒有的細節：衛星指配「使用期限最長為5年，屆期得依原核配內容申請核配」；註 *1 保留 1775-1785MHz 與 1870-1880MHz「作為政府重大施政計畫及其相關實驗網路之潛在使用頻率」。
- **R-GEN-SGB-2025 自己對 WRC-27 議題編號前後不一**：它把「WRC-27 agenda item 1.10 – Resolution 775 (WRC-23)」派給 WP 5C（71-76 GHz 與 81-86 GHz 的 pfd／e.i.r.p. 限制），又把「WRC-27 agenda item 1.10 – Resolution 256 (WRC-23)」派給 WP 5D（4 400-4 800 MHz、7 125-8 400 MHz、14.8-15.35 GHz 的 IMT 地面部分）。紀錄的 `must_not_write` 只記了後者。**同一份官方文件把同一個議題編號掛在兩個決議上，所以文章可以引頻段與 Resolution 256 (WRC-23)，但不要引議題編號。**
- **年對年的對照是有來源、可寫、而且比單純「官方沒說」更有資訊量的**：2025-09-17 的新聞稿 17422 明寫有「國內產官學研專家」參與，2026-09-10 的 20612 則完全沒有點名任何國內與會者。紀錄只寫了後半。
- **來源 3 應該改用或並用它的落地頁**：不透明的檔案端點 `www-api.moda.gov.tw/File/Get/...` 建議換成 `https://moda.gov.tw/digital-affairs/resource-management/resource-plan/plan002/15180`（公告修正案｜衛星頻段，建立與更新日期皆 2025-02-13）。那一頁列出三份 PDF（公告／無線電頻率供應計畫／無線電頻率供應計畫修正總說明及對照表），並說明修正緣由：「依據電信管理法第52條第4項」「為促進我國衛星服務與產業發展…修正『無線電頻率供應計畫』之規定」。
- F03 的小出入要修：人事頁寫的是「國立臺灣大學法律學系學士」與「國立臺灣大學法律學研究所碩士」（紀錄把兩者都縮短了）；「參事（2016-2022）」實際是**國家通訊傳播委員會參事**，而同一頁另外列了蒙藏委員會參事（2010）與司法院參事兼主任（2010-2013），壓縮後的列表很容易誤讀。**另外，新聞稿本身只寫「葉寧次長」，「常務次長」是人事頁的說法，不是新聞稿的。**
- F02 的 `verbatim_quote` 把三個獨立的 HTML div 用頁面上沒有的表意空格串在一起。**三個欄位值都對，但那不是字面引文，不可拿去做字串比對或翻譯。**

### live_data_warnings

- **計畫頁 `programs/19090` 的更新日期是 2026-09-15**（建立 2026-03-05），也就是**批次作業期間才動過**，而且掛著 9 份 File/Get 附件（月報與季報會持續增加）。**附件數與「最新一期是第幾期」都是快照。**
- 供應計畫 PDF（`Mrbx00R7mtGIJje`）內部 CreationDate D:20250206161539／ModDate D:20250206161547，重抓未變，**這一份本身不是活文件**；但 **`law.moda.gov.tw` 在本容器回 403 Cloudflare，無法確認它是否仍是現行版本。一律寫「114年2月修正版」，不可寫「現行版」。**
- moda 的英文新聞列表 `/en/press/press-releases/372` 是 15 筆、最新 2026-09-01，**且本篇沒有官方英文版**（`/en/press/press-releases/20612` 回 404）。這是滾動列表，不能拿來證明「沒有」。
- 施政計畫 PDF：116 年度（`CO53evdYhevAdZu`，11 頁）的 PDF 建立時間 2026-09-03；115 年度（`E5RrlYLBIF6IfLS`，12 頁）。**兩份都是草案版。**
- ITU 出版品 `R-GEN-SGB-2025-PDF-E.pdf` 是 2025 年版（CreationDate 2024-12-19、ModDate 2025-01-14），68 頁——**是一份有年份的年刊，人事與職稱會逐年變。**
- 查核者實測 `https://www.itu.int/online/mm/scripts/gensel90` 回 **HTTP 500**（ITU 'HTTP Shell Gateway Version 1.9' 錯誤頁），不是紀錄寫的「HTTP 200 F5 gateway page」。結論相同（拿不到名冊資料），但紀錄的狀態碼是錯的。
- 其他確認的封鎖：`law.moda.gov.tw` 403、`www.ofcom.org.uk` 403、`www.gsma.com` 403、`www.ncc.gov.tw` 403。**這些都不可記上 `checked_on`。**

### source_list_fix

四條沒有超量、全部可達，但問題不少：

1. **11 條事實（28 條中）掛在 9 個不在 `sources[]` 的網址**：`R-GEN-SGB-2025-PDF-E.pdf`（2）、`File/Get/.../b4RLKc8Mn5Y5Sj9`（11-5 書面報告，2）、葉寧人事頁、新聞稿 17422、`resource-plan/plan001/6369`、115 年度施政計畫 PDF、116 年度施政計畫 PDF、`ntia.gov` 人事頁、`nera.com` 專家頁各 1。**用到就要換 source。**
2. **`sources[3]`（ITU SG 5 頁）撐不起掛在它上面的 F20**（見 must_fix 8）。要嘛改掛 ITU PDF、要嘛改寫 F20。
3. **`sources[2]` 是不透明的檔案端點**，建議改用或並用落地頁 `plan002/15180`（見 must_add）。
4. `nera.com`（NERA 顧問公司的專家頁）用來確認 Hans-Martin Ihle 的職稱，嚴格說是當事人任職機構自己的頁面，**但它不在 tech.md 列舉的一手來源類型裡**。若要保留，研究紀錄要寫明理由；不然就不要寫他的職稱。
5. 沒有任何一條事實來自媒體、整合站或搜尋摘要，File/Get 的識別碼也都能從官方索引頁找到，不是猜的。**這部分是乾淨的。**

---
## tech-news-taiwan-matsu-cable-20260623

查核結果：needs_fixes，38 條確認、5 條推翻、9 條無法追溯。**43 條事實掛在約 17 個不同網址，而 `sources[]` 只有 4 條——這是本垂直結構最糟的一篇。**

### must_fix

1. 紀錄 `sourcing_notes` 寫 114年度海纜報告 PDF 下載得到卻讀不出來（「pypdf 也因 cryptography 的 _cffi_backend 匯入失敗而不可用，無法抽文字，報告數字一律改引 2026-04-07 新聞稿」）；**被推翻**——查核者抓同一個網址 `https://www-api.moda.gov.tw/File/Get/moda/zh-tw/kj9vSvBw5wUeqla`（200，40 頁），pypdf 正常匯入、抽出 24,883 個字元。**這份報告在本容器完全讀得出來，而且比新聞稿多得多的一手細節（見 must_add）。整個「報告數字拿不到」的前提是錯的。**
2. 紀錄 `not_said` 寫「新聞稿用的是『海纜七法』這個統稱，沒有逐一列出七部法律名稱與條號，不要自行補」；**對新聞稿 19392 成立，但當成資訊缺口是錯的**——官方報告（就掛在研究者已引用的 `/1805` 頁上）寫著「海纜七法」內容涵蓋電信、電業、天然氣、自來水、氣象、商港及船舶法；業經立法院於114年12月三讀通過，並於115/01/05經總統公布實施」，另有「電信管理法第72條、第72條之1修正案於112/06/28經總統公布實施」。**名稱、三讀時間與公布日期都有官方來源，「不要自行補」這條指示過度限制。**
3. 紀錄 `sourcing_notes` 寫「`https://www.cht.com.tw/zh-tw/home/cht/messages` 列表 200 但前端渲染…等於取不到清單」；**被推翻**——`cht.com.tw/robots.txt`（200）就指名 `https://www.cht.com.tw/home/eshop/sitemap/sitemap.xml`，該檔回 200、721,791 bytes、6,826 個 `<loc>`，其中含 386 個 2026 年訊息網址。**中華電信自己的公告清單拿得到。** 查核者藉此讀到 2026-03-07 TDM2、2026-03-31 與 2026-04-29 TM3（東引至北竿區段）、2026-05-25 TDM2 修復、2026-06-05 TM3-D（南竿-北竿區段）等公告。
4. 紀錄在 `sources` 註記裡寫 15082 提供「臺馬四號的補助計畫名稱（普及偏鄉寬頻接取環境計畫）」；**過度解讀，而且被另外兩份官方文本否定**——15082 是先寫 12.6 Gbps 微波擴容屬於普及偏鄉寬頻接取環境計畫，接著才寫「並補助中華電信建置臺馬4號海纜」，沒有重述計畫名稱；19976 寫臺馬四號是「透過**前瞻預算**」；114年度報告寫「本部自113年起藉由**前瞻計畫預算**補助海纜業者新建臺馬4號海纜」。**不可以把「普及偏鄉寬頻接取環境計畫」寫成臺馬四號的經費來源。**
5. 紀錄把 `programs/17418` 列在可換入的 2026 年政策材料裡；**該頁更新日期是 2025-10-02，不是 2026**。研究者對 `/6613` 標了正確日期（2026-02-13），對 17418 沒標。**任何「截至 2026 年」的敘述建立在它上面都會是錯的。**
6. 紀錄 verified_fact 1 的註解寫「官方寫的是『鄉間』微波通訊系統，指的是馬祖四鄉之間的微波，和台灣本島—馬祖之間的微波備援是不同的東西」；**那是研究者的解讀，不是來源說的**——19976 寫的是「馬祖東引、北竿、南竿與莒光鄉間微波通訊系統」與「每個鄉都至少有2組微波系統可**對外聯繫**」，「對外聯繫」並沒有把連線限制在鄉與鄉之間。數發部自己的 114年度報告把**臺馬間**微波（113/01/15 起 12.6 Gbps）描述成可完全備援臺馬間全部通訊。**官方文本從未區分這兩套系統，文章不可以斷言這個區分。**
7. 紀錄把「2026-04-29 全斷的推定原因是船難殘骸移動」標成 `is_vendor_claim=false`；**分類錯誤**——19582 明確歸屬給中華電信：「經該公司初步推估，故障原因疑似海象不佳，導致原擱淺船隻殘骸移動」。**這是電信業者的初步推估、由數發部轉述，必須寫成「中華電信初步推估」，絕不可寫成已確定的原因。**
8. 紀錄 15210 那條（2025-02-16 12:49 全斷於新北市外海；臺馬三號 1 月 15 日已全斷）配的 `verbatim_quote` 是芯線老化／113年10月3日、114年1月22日通報那段；**引文裡沒有它所宣稱的數字**。那些數字在同一頁的其他句子（「114年2月16日中午12時49分，位於我國新北市外海的臺馬二號海纜發生全斷障礙」；「臺馬三號海纜在1月15日已經發生全斷障礙」）。**事實可查，但紀錄的追溯鏈斷了，要重新配對引文。**
9. 紀錄 19392 那條「114 年 7 起障礙事件中有 3 起為船錨勾損（42.9%）」配的是 38.3% 四年平均那段引文；**兩個缺陷**：(a) 引文與事實不符，42.9% 出自「114年7起障礙事件中有3起『船錨勾損』，占比上升至42.9%，且有2起肇因為外籍『權宜輪』（FOC）非法下錨」；(b) **重大遺漏——那 7 起的範圍是「近岸（24海浬內）國內及國際海纜」**（報告表 7 確認）。**不加限定會讀成台灣 2025 年海纜障礙的總數，而同一則新聞稿自己就寫了年底地震另外損壞 24 浬外的 6 條國際海纜。**
10. 紀錄 `report/1805` 那條（建立日期 2026-04-07、更新日期 2026-09-02、中英文 PDF）配的引文是「其重要性如同我們的『數位生命線』」；**那句引文撐不起任何一項被宣稱的事實**。日期與兩個 PDF 連結都在頁上、也確認過，**但引文要換掉。**
11. 紀錄 `/1747` 國內海纜清單的 `verbatim_quote` 寫成 `1 臺金二號海纜 TK2 / 2 臺馬一號海纜 TM1-D / …`；**那些「 / 」是研究者拼的，頁面上沒有**。底層資料正確（TK2、TM1-D、TDM2、TM3、TP2、TP3、PK1、PK3、LLV1、LLU2；臺馬四號不在其中）。**要標成表格摘要，不是引文。**
12. 紀錄 19778 那條寫「地點距沙崙**約** 23.6 公里」；**來源這裡沒有「約」**——原文是「於距沙崙23.6公里處發生全斷障礙」（該則另一處 180 公里才用「約」）。另外**來源寫的是「沙崙」，不是「淡水沙崙」。**
13. 紀錄 19392 那條把「均經司法機關**判刑確定**」當背景重述；**數發部自己的 114年度報告把同兩案描述成一審判決**（臺南地院 114年6月 3年有期徒刑；福建連江地院 114/12/04 3個月得易科罰金），並寫「迄115年2月止已移送4案、2起遭判刑」，**沒有「確定」二字**。**要註明是數發部新聞稿的用語，不可斷言判決確定。**

### must_add

- **moda 新聞稿 16356（2025-06-03，部長就任週年，存在於 moda 自己的開放資料 CSV 裡）寫「補助臺馬4號海纜（預計115/6完工）與離島微波建置」——這是 2026 年 6 月完工目標的第二個官方出處**，同一則另寫「已在政府重要節點布建700個非同步衛星站點」。研究者漏了。
- 114年度報告寫「本部自113年起藉由前瞻計畫預算補助海纜業者新建臺馬4號海纜，114年補助其新建臺澎4號及澎金4號海纜，均預計於115年完工」——**臺馬四號是 2026 年到期的三條離島海纜之一，而且有官方的補助起始年（113年）與經費工具（前瞻計畫預算）。**
- 同一份報告把臺馬間微波容量的日期補上：「擴增臺馬間微波通訊頻寬於113/01/15已大幅擴容為12.6Gbps，可完全備援臺馬間全部通訊需求」。**15082 只有 12.6 Gbps 這個數字、沒有 2024-01-15 這個日期。**
- 同一份報告寫「112~113年，全國及離島地區設置770個非同步軌道衛星終端設備」，另一處寫「770個非同步衛星（OneWeb、SES）站點」。**現在官方衛星數字有三個：9 個（連江，15082）、700 個（16356）、770 個（報告）。三者範圍不同，不可混用，引用時要各自寫清楚範圍。**
- 同一份報告把兩件刑事案件寫全：TP3 斷纜案（114/02/25）多哥共和國籍貨船「宏泰58號」中國籍王姓船長，臺南地方法院 114年6月判 3 年有期徒刑（首例）；TDM2 斷纜案（114/10/07）中國籍漁船「閩連漁60138」吳姓船長，福建連江地方法院 114/12/04 判 3 個月得易科罰金；迄115年2月止已移送4案。**注意 TDM2 那案的日期 114/10/07 就是 2026-09-16 障礙表上仍未修復的那一筆。**
- **國際海纜 15 條 vs 16 條的差異有解釋，不要寫成官方不一致**：報告表 1 列 15 條國際海纜、註明「資料截至115年2月26日止」，且**不含**live 頁 `/1747` 上排第 16 的 TPU 臺美菲海纜。**那是有日期的快照 vs 活頁面的差別，可追溯到新增一條海纜。**
- **中華電信自己的公告（經官方 sitemap 取得）補了 moda 新聞稿沒有的細節**：2026-03-07 TDM2「訊務已於第一時間疏轉至台馬第三海纜」（改走 TM3，不是微波）；2026-05-25「已於05月25日完成**部分芯線**搶通並恢復雙海纜運作」——**是部分修復**，與 9/16 仍有兩筆 TDM2 障礙未結案一致，**所以 moda 標題的「海纜修復」不可以被改寫成完全修復**；2026-04-29 TM3 東引至北竿區段「訊務已於第一時間全數切換疏轉至微波電路」；2026-06-05 TM3-D 南竿-北竿區段。
- moda 開放資料 CSV（392 列、最新 2026-09-16）獨立支持研究者的關鍵否定結論：**2026-06-23 之後沒有任何 moda 新聞稿宣布臺馬四號完工或啟用**，2026 年的海纜新聞稿只有 19338、19392、19582、19778、19976。中華電信 2026-06-23 的訊息與本案無關（MOD 內容、CSR、一個獎項）。**2026-03-07 的 TDM2 斷纜從來沒有自己的 moda 新聞稿**，只在 5/26 那則與中華電信自己的公告裡出現。
- **`event_date` 2026-06-23 站得住腳**（新聞稿建立日期、行政院轉載頁的「日期：115-06-23」、CSV 的發布日期 2026-06-23T15:20:31 三者一致），**但新聞稿報導的視察是 2026 年 6 月 16 至 17 日進行的。文章開場句不可以把視察日期寫成 6/23。**
- **紀錄用 `not_said` 欄位，但 BRIEF 的研究紀錄 schema 要的是 `unverified_or_excluded`**；而且 `not_said` 清單交到查核者手上時在最後一項中途被截斷（「6/23 新聞稿裡『日前臺馬二號、三號海纜在東引地區同時...」），**那一項沒有被查核。**

### live_data_warnings

- **海纜障礙表 `https://moda.gov.tw/major-policies/subseacable/fault/1749` 在查核當天就動過**：頁面自標「日期：115/9/16」、建立日期 2025-12-09、**更新日期 2026-09-16**。**這是逐筆會增刪的登記表，任何從它數出來的筆數（未修復件數、各海纜的障礙筆數）都是當天快照，引用一定要寫查核日，而且最好不要在正文寫死筆數。**
- **國內海纜清單 `/subseacable/1747` 沒有任何頁面層級日期**——唯一的「更新日期」是網站頁尾由 JS 寫入的 `<span id="spanDateNow">`，也就是**你打開頁面的當天**。清單上 10 條國內海纜、16 條國際海纜都是活資料。**「臺馬四號不在清單上」只在 2026-09-16 成立。**
- 報告表 1 的 15 條國際海纜註明「資料截至115年2月26日止」——**有日期的快照，與活頁面的 16 條不是矛盾。**
- moda 開放資料 CSV `https://www-api.moda.gov.tw/OpenData/csv/9` 392 列、2022-08-26 到 2026-09-16，**是活檔案；用它證明「之後沒有新公告」只在查核日成立。**
- 中華電信 sitemap 6,826 個 `<loc>`、含 386 個 2026 年訊息網址——**活檔案。**
- 114年度報告 PDF（`kj9vSvBw5wUeqla`）ModDate D:20260326184906+08'00'，40 頁；`report/1805` 頁建立 2026-04-07、**更新 2026-09-02**。
- `www.ncc.gov.tw` 回 403 Cloudflare、`moda.gov.tw/robots.txt` 回 404；**但 `www.cht.com.tw/robots.txt` 回 200**（紀錄誤以為拿不到）。

### source_list_fix

四條沒有超量，全部可達、都是 moda 一手頁，但**結構性問題最嚴重**：

1. **43 條事實中有 21 條掛在 12 個不在 `sources[]` 的網址**：19392（6 條）、19582（4 條）、`/subseacable/1747`（2 條）、行政院轉載頁、19338、15210、`/subseacable/maintenance/1751`、`/subseacable/report/1805`、中華電信 TDM2 公告、中華電信 2026 財測、`/operations/312`、`/programs/6613` 各 1 條。
2. **幾乎所有量化材料都落在 `sources[]` 之外**：38.3%、42.9%、19 組衛星頻率、海纜七法、1500 人、有線電視無法走微波、16／10 條海纜、核定補助 1 案、NT$40.7 億。BRIEF 明文要求「每一個日期、價格、百分比…都要能指到一條 source 的原文」。**撰稿代理必須先挑一組四條 sources 真的涵蓋得到的事實來寫，不要依賴事後換 source 的清單。**
3. 中華電信 2026 財測那條（購置不動產、廠房及設備增加 40.7 億元至 319.1 億元，原因之一為 'the new construction of domestic and international submarine cable'）**沒有點名臺馬四號**，要寫成「中華電信表示」，**且不可寫成臺馬四號的造價**；該網址也不在 sources 裡。
4. 建議的取捨：把 19392（統計與法制）或 19582（東引全斷的實際影響）換進 sources，取代目前只用來當背景的某一條；**或者把文章範圍收到四條現有來源真的涵蓋的事實上。**

---
## tech-news-taiwan-sovereign-ai-corpus-20260915

查核結果：needs_fixes，35 條確認、3 條推翻、5 條無法追溯。**注意：交到查核者手上的紀錄在第 40 條（授權條款那條，「官方英文名為 Ta…」）處被截斷，第 41 至 60 條——包含整組即時語料庫統計與其餘授權條款事實——完全沒有經過查核。**

### must_fix

1. 紀錄 `sourcing_notes`(b) 寫「moda 自己的站內搜尋 API 對每個關鍵字、每個日期區間都回『查無任何資訊』，所以拿不到 moda 在 2025 年底的語料庫上線公告——上線這件事只靠 9/15 新聞稿自己那句『自去（114）年底上線』佐證」；**被推翻**——上線新聞稿存在、是一手、而且活著：`https://moda.gov.tw/press/press-releases/18314` HTTP 200，建立日期 2025-12-24／更新日期 2026-03-19，發布單位資料創新司，標題「『臺灣主權AI訓練語料庫』上線！ 數位發展部攜手200個機關打造本土語料資源」，內文「數位發展部今（24）日發布『臺灣主權AI訓練語料庫』」。英文版也活著：`/en/press/press-releases/18314`。**取得方式不需要用死掉的搜尋 API、也不用猜 id**：`moda.gov.tw/sitemap.xml`（HTTP 200）公布 392 條真實的中文新聞稿網址，用 2025-12-14 與 2026-01-03 兩筆的 id 夾出來只剩六頁要試，其中一頁就是 18314。**這篇研究紀錄漏掉了這個題目最重要的來源。**
2. 紀錄 `event_date_basis` 寫「附件簡報 PDF 封面標 2026.09.15，PDF CreationDate 是 D:20260915152311+08'00'；書單 PDF 的 CreationDate 相同」；**兩份 PDF 的 CreationDate 不同，而且引的那個時間戳屬於另一份**。書單 `MXH8xGP8UD6Awlf`：CreationDate D:20260915152311+08'00'、Author 王復中、Producer Microsoft Word LTSC。簡報 `7kSm8t10Nmtktpr`：CreationDate **D:20260915180859+08'00'**、Author SlideEgg、Producer Microsoft PowerPoint LTSC。**事件日 2026-09-15 仍然成立（頁面建立／更新日期與簡報封面），但依據要改寫。**
3. 紀錄 verified_fact 34 寫諮詢表單欄位是「聯絡人姓名、電話、電子郵件、語料範圍與想法，語料範圍選項為出版品、電子報、期刊、專題文章」；**三個標籤沒有一個是頁面上的字串**。查核者從 taic 自己的打包檔 `/_nuxt/DRODNAlq.js`（HTTP 200）讀出真正的字串是：**姓名 / 電話 / 電子郵件 / 資料類型（可複選） / 其他 / 請簡述您欲提供之語料內容 / 送出**。也就是「聯絡人姓名」應為「姓名」、「語料範圍」應為「資料類型（可複選）」、「語料範圍與想法」應為「請簡述您欲提供之語料內容」，而且**漏掉了第五個選項「其他」**。BRIEF 要求官方介面字串照抄不重打。
4. 紀錄 verified_fact 27 寫「**截至 2026 年 7 月 24 日**，語料庫自上線以來已累積『逾15億tokens』語料量」；**那一頁沒有為這個數字標任何截止時點**——原文是「自上線以來，已累積逾15億tokens語料量」，2026-07-24 只是發布日，而且英文版在 2026-07-30 被改過時仍寫 'more than 1.5 billion tokens'。研究者自己在 22 億那條的註記裡寫「這是官方唯一自己帶時間點的規模數字」，自相矛盾。**改寫成：7/24 新聞稿寫「自上線以來已累積逾15億tokens」，官方未給截止時點。**
5. 紀錄 verified_fact 35 末尾寫語料提供原則「文本日期標為 115.05.20，**也就是原則比記者會早約四個月訂定**」；**頁面只渲染 `<p class="content-date">115.05.20</p>`，從沒說那是訂定日**，而且語料提供原則第七點允許維運單位「滾動檢討修正本原則」，所以那也可能是修訂日。**保留「文本標示日期 115.05.20」，刪掉「訂定」這個推論。**
6. 紀錄 verified_fact 23 寫「**2026 年 7 月 24 日**，數發部發布…**正式上架**客家語言資源…」；**新聞稿寫的是「近日與客家委員會合作，正式上架」——是「近日」，不是 7/24。** 沒有任何官方材料給出客語語料的上架日期。**現在的寫法會誘導撰稿者把發布日當成上架日，正是 BRIEF 警告的混淆。**
7. 紀錄 verified_fact 15 寫「新聞發布頁附了兩份官方 PDF」，但 `verbatim_quote` 是**空字串**，依 BRIEF 無法追溯到文字。事實本身為真（查核者確認「相關檔案」列出「民間單位提供之語料書單 PDF」與「主權AI語料庫民間語料徵集記者會簡報 PDF」，兩個標籤與兩個檔案 token 完全對應）。**把標籤文字補成引文。**
8. 紀錄 verified_facts 2 與 24 把兩則新聞稿的官方標題掛在列表頁 `https://moda.gov.tw/press/press-releases/372`；**那個列表只顯示最新 15 筆，到刊出時它已經不會包含這兩個標題，引用會失效。** 兩個標題都在文章頁本身——查核者確認 `/20640` 與 `/20230` 的 `<title>` 與 `<h1>` 與紀錄的字串逐位元組相同，是純 ASCII 空格 U+0020，沒有不斷行空格或 U+2011。**改掛文章網址。**

### must_add

- **簡報第 3 頁「之前」那一欄是可以標日期的，紀錄 fact 18 寫「簡報沒有標明這兩個值各自對應哪一天」是錯失。** 2025-12-24 的上線新聞稿（`https://moda.gov.tw/press/press-releases/18314`）寫「目前已有超過200個政府機關投入，上架逾2,000筆資料集、超過6億tokens」——**正好就是簡報的 200／2000／6億**。只有「資料量(GB) 50」沒有可對應的日期錨點。
- **授權條款裡限縮「可退出」的那一條，紀錄完全沒有**：《臺灣主權AI訓練語料授權條款-第1版》二.2：「即使原語料資料後續停止提供使用，不影響已完成之訓練成果，包括但不限於所產出之模型、權重，以及程式碼、文件或其他型態之輸出。」另有二.1：「此項授權不得再授權與轉讓，有效期間得由授權人或其代表人指定為特定年份或永久。」**只轉述數發部的「可退出」而不寫這一條，會誤導讀者。** 來源 `https://taic.moda.gov.tw/api/v1/page-content.info?type=license`（200），渲染於 `https://taic.moda.gov.tw/content/license`。
- **語料提供原則第七點紀錄沒收**：「語料庫維運管理單位得視實際推動情形、技術發展及政策需要，滾動檢討修正本原則。」紀錄收了第 2 至 6 點，漏了第 1 點與第 7 點。**第七點正是研究者所標記的第四點（提供者受「第1版及其後續更新條款」拘束）的另一半。**
- **授權條款是與經濟部智慧財產局共同推出的**：18314 寫「數發部與經濟部智慧財產局合作，共同推出《臺灣主權AI訓練語料授權條款－第1版》」。**標題陷阱**：18314 用的是全形破折號「－第1版」，taic 自己的 title 欄位用的是 ASCII 連字號「-第1版」。
- **這份授權條款沒有單一的官方英文名，官方頁面上就有五種寫法**：'Taiwan Sovereign AI Training Corpus License - Version 1'（taic 的 title_en）、'Taiwan Sovereign AI Training Data License–Version 1.0'（條款內文，中英兩版皆同）、'Taiwan AI Training License-1.0' 與 'SAITD-Lic-Taiwan-1.0'（條款內文的縮寫）、'Taiwan Sovereign AI Training Corpus Licensing Terms - Version 1'（moda 英文版 18314）。**紀錄第 40 條（被截斷處）不論寫的是哪一個，都不可以寫成「官方英文名」。**
- 中英文條款內容有分歧，儘管六.1 宣告兩者皆為正式文本、具同等法律效力：英文版三.1 告訴被授權人縮寫可連結到 'ait-lic.moda.gov.tw'，中文版三.1 沒有點名網域。**那個網域在本容器無法解析（502 CONNECT tunnel failed），不要印出來。**
- 可用而未用的佐證：`taic /api/v1/logo.list?type=NGO`（200）恰好 5 筆、建檔時間都是 2026-09-15——巨思文化、印刻、秀威資訊、食力、讀墨，與五家簽署單位相符；`type=CENTRAL` 共 34、`type=LOCAL` 共 22。**注意 34+22=56 個有 logo 的單位不等於簡報的「政府機關參與 250」，兩者是不同的東西，不可畫等號。**
- **印刻文學在記者會簽署、也出現在簡報第 5 頁的民間單位面板，但它沒有出現在「民間單位提供之語料書單」PDF 裡。** 簽署與書目上架不是同一件事，值得寫一句。
- 同日的一手脈絡紀錄沒提：`https://moda.gov.tw/press/press-releases/18316`（200），2025-12-24，「立法院三讀通過《人工智慧基本法》 構築我國AI創新與安全治理基石」——**與語料庫上線同一天發布。**
- 簡報裡沒進事實的內容：第 3 頁底部橫幅「語料資源持續成長，支持更多 AI 應用與創新，打造臺灣主權 AI 的堅實基礎」與 14 個領域標籤（語言／歷史／民俗／生物／旅遊／醫療／地理／出版品／民間參與／交通／經濟／文化／藝術／法律）；第 7 頁「釋放資料價值，擴大臺灣文化觀點」與 經典資料活化／影響力擴散／臺灣觀點守護；第 8 頁結語「公私協力提供在地化高品質語料 共同支持我國主權AI發展」以及一個在投影片上看不見的連結 `https://youtu.be/lhLEBnsPcQw`；第 2 頁的兩行副標「確保AI時代符合國家安全與經濟安全，鞏固自由民主價值與文化詮釋權。」與「補足正體中文與臺灣在地語言資料缺口…」。**另外 fact 22 把第 2 頁的順序寫反了——投影片上「自主選擇」那一塊在前、「正體中文」那一塊在後。**
- `/contribute` 上的《臺灣主權AI訓練語料同意書》是一條連到 `https://s.moda.gov.tw/9DhGksapK8Cp`（moda 自己的短網址）的連結，紀錄沒記。同一頁的 `content_en` 欄位是未翻譯的中文。
- 申請須知及使用規範（`page-content.info?type=application_guidelines`，200；建立 2025-10-16、異動 2025-12-30）有未用的材料：申請資格、「原則於收受申請案後7個工作日內完成審查」、「帳號啟用後每3個月須重新進行憑證驗證」、曾提供語料者與數位產業署「數位產業跨域軟體基盤暨數位服務躍升計畫」算力平臺入選名單優先審查、以及「使用者同意語料庫得揭露其使用語料資料所產出或輸出之相關成果」。該頁另以明文列出 tsaitc@moda.gov.tw，**佐證了研究者對 Cloudflare 混淆信箱的解碼是對的。**

### live_data_warnings

- **這是本垂直「活登記表」風險最高的一篇，而且同一天的官方數字彼此不一致。** 2026-09-15 同日：新聞稿寫「約22億 Tokens **截至今年8月底**」，簡報卡片寫「21億」。taic 自己的公開端點 `/api/v1/no-auth/export/dataset/summary` 在 2026-09-16 回報 `estimated_tokens` **2,200,397,354**、`dataset_sum` **6,417**、`files` **50,769**、`size_formatted` **318.59 GB**——**資料集數與 GB 都遠高於簡報的 5000 與 200 GB**。moda 的「moda x AI」專區頁（頁面標示更新日期 2026/09/10）儀表板又寫 **2,161,123,541**。**四個數字、四個時點。簡報數字與即時 API 數字絕對不可以出現在同一句話裡；每一個數字都要標出處與時點。**
- **`estimated_tokens` 的欄位名就是 estimated（推估），不是實測計數**——引用時要照這個字寫。
- **合作夥伴數是活的**：CENTRAL 34、LOCAL 22、NGO 5（全部 2026-09-15 建檔）。**34+22=56 不是簡報的 250。不可把兩者相加、相減或等同。**
- taic 網站頁面標題仍是「臺灣主權 AI 訓練語料庫(Beta 版)」——**平台自稱仍在 Beta，這個狀態會變。**
- 上線新聞稿 18314 建立日期 2025-12-24、**更新日期 2026-03-19**，是被修訂過的文件；`/contribute` 頁內容建立 2026-08-27 16:35:15、**最後修改 2026-09-14 17:50:51（記者會前一天）**；授權條款與申請須知在 taic 的 CMS 紀錄都是 created 2025-10-16 08:47:48，**那是 CMS 紀錄時間，早於 2025-12-24 上線日，不可寫成上線日期。**
- `/partners` 頁回 200 但 SSR 的 body 裡沒有文章文字（查核者確認「自願參與」0 次命中）——**研究者的警告正確。**
- `taic.moda.gov.tw/api/v1/news.list` 研究者說「回 total 0」，查核者拿到的是 **404 HTML 頁**。
- `moda.gov.tw/press/press-releases/372` 是**只顯示最新 15 筆的滾動列表**（最新 2026-09-15）。`/en/press/press-releases/20640` 回 **404**（本篇沒有官方英文版；英文最新一筆是 2026-09-01）。
- 兩份 PDF 的 **HEAD 請求回 HTTP/2 404、GET 才會給 PDF**——研究紀錄要寫明用 GET。

### source_list_fix

四條沒有超量，但問題不少：

1. **60 條事實中有 21 條掛在 10 個不在 `sources[]` 的網址**：記者會簡報 PDF（5 條）、`taic.moda.gov.tw/content/application-guidelines`（4 條）、`taic.moda.gov.tw/content/about`（3 條）、新聞列表頁 `/372`（2 條）、書單 PDF（2 條）、moda 英文版 20230、`/api/v1/no-auth/export/dataset/summary`、`taic.moda.gov.tw/`、`/api/v1/logo.list?type=NGO`、`/major-policies/ai/1781` 各 1 條。**簡報與書單是本篇最實質的材料，卻都不在 sources 裡。**
2. **facts 2 與 24 掛的 `/372` 是滾動列表，到刊出時就指不到那兩個標題了**（見 must_fix 8）。改掛文章頁，不佔名額。
3. **最重要的一手來源根本不在紀錄裡**：2025-12-24 的上線新聞稿 `https://moda.gov.tw/press/press-releases/18314`。它同時提供了簡報「之前」那一欄的日期錨點與授權條款的共同推出機關。**強烈建議換進 sources。**
4. 沒有任何一條來自媒體、整合站或搜尋摘要——四條全是 moda.gov.tw／taic.moda.gov.tw。識別碼也沒有猜：20640／20230／372 都在 moda 自己的列表裡，兩個 PDF token 逐字出現在 20640 的 HTML href 且標籤與檔案相符，`_nuxt` 三個 js 檔都在 taic 自己的 script 清單裡。**這部分是乾淨的。**
5. **第 41 至 60 條沒有經過查核**（見開頭）。若文章要用到即時統計（50,769 檔／318.59 GB／6,417 資料集／2,200,397,354 tokens）、Beta 標示、合作夥伴數或 moda x AI 儀表板數字，**必須先送第二輪查核**。

---
## tech-news-windows-project-zenith-20260904

查核結果：needs_fixes，39 條確認、2 條推翻、4 條無法追溯。43 條 `verbatim_quote` 全部經機器比對（正規化破折號、彎引號與商標符號後）與來源相符。

### must_fix

1. 紀錄 F10（預載工具圖表第 3 欄）寫「Python 3.14+, uv, NVM, Node 24+, WSL 2+ Ubuntu, .NET 10 … **These six are the only entries in the whole chart that carry version markers**, apart from PowerShell 7 in column 2」；**被推翻**——查核者以 3756x2292 全解析度讀圖，那六項裡 **uv 與 NVM 完全沒有版本標記**，是裸名稱。全圖真正帶版本的只有五項：Python 3.14+、Node 24+、WSL 2+ Ubuntu、.NET 10（第 3 欄）與 PowerShell 7（第 2 欄）。**六個工具名本身是對的、已確認；錯的是「這六個都帶版本」那一句——照抄會讓撰稿者替 uv 與 NVM 編出版本號。**
2. 紀錄 `sourcing_notes`／`not_said` 寫「Acer, ASUS, Dell, HP, Lenovo, MSI, Intel, NVIDIA and Qualcomm are not mentioned in the Zenith post（grep：各 0 次命中）」；**Intel 那部分為假**——2026-09-04 頁面文字裡 'intel' 出現兩次，在 'shifting some of that **intel**ligence to the edge' 與 'Windows Developer Configurations to **Intel**ligent Terminal'。**實質論點仍成立**（以字界搜尋，Intel、HP、Lenovo、NVIDIA、Qualcomm 從未以公司名出現，AMD 是唯一具名的晶片夥伴），**但紀錄斷言了一個重現不出來的 grep 結果，而後續代理一定會重跑。**
3. 紀錄 F08 寫「The actual pre-installed tool names appear **ONLY** in a chart image embedded in the post（alt text 'Chart showing pre-installed tools', asset **Preinstalled-tools-2.png**）」；**兩個問題**：(a) `Preinstalled-tools-2.png` 這個檔名**在伺服的 HTML 裡完全不存在**，頁面上唯一出現的是 `Preinstalled-tools-2-1024x625.png`，而且沒有 srcset。裸檔名是把 WordPress 的尺寸後綴拿掉推出來的——**是衍生網址，不是從頁面上取得的**。它確實解析得到（200，580,648 bytes）、也是同一張圖，而且 F08–F10 掛的是文章網址不是圖片網址，所以沒有捏造，**但紀錄把衍生網址寫得像官方資產，正是 BRIEF 禁止的習慣**；要記下頁面上的網址並註明全尺寸版是自己去掉後綴取得的。(b) 「ONLY in a chart image」講過頭了——正文本身就寫了 Visual Studio Code 與 Windows Terminal。**只有完整的 18 項清單才是只存在於圖裡。**
4. 紀錄 F36 寫「**Micro Center is a United States retailer**; AMD names no other region or retailer in this blog」；後半確認無誤，**但「Micro Center 是美國零售商」這句話在 AMD 頁面上完全找不到**——查核者搜過全文。那是被塞進一條掛著 AMD 網址的事實裡的外部知識。幾乎一定為真，**但依一事一網址的規則它不能掛在那個網址上，否則文章會讓讀者以為 AMD 說了「限美國上市」。**
5. 紀錄 F43 寫「Both official Windows feeds are live and were used to confirm the date … windowsdeveloper feed 回 10 筆、最新 2026-09-14，並把 Zenith 那筆列為 'Fri, 04 Sep 2026 10:00:29 +0000'」；**內容正確（查核者完全重現），但這條事實掛的網址是文章頁，而文章頁一個字都沒有這些內容**，兩個 feed 網址也都不在 `sources` 裡。**這是全紀錄唯一一條無法對照自己所引網址查證的事實。要嘛改掛 feed 網址，要嘛移回 `sourcing_notes`（那裡本來就寫對了）並從 verified_facts 刪掉。**
6. 紀錄 F21 寫 2026-09-14 的 IFA 文章「repeats the same device-class figures but writes the bandwidth as '250gbps' rather than '250+ GB/s'」；**逐字確認無誤，但「重複同樣的數字」低估了差異，這個寫法不可以進文章**。IFA 那篇寫的是 '64GB+ unified memory and 250gbps memory bandwidth'：**它連加號也一起拿掉了，而且 250 gigabits per second 約等於 31 GB/s——那是另一個量，不是另一種寫法。** 只引 2026-09-04 的寫法（'250+ GB/s'）；若要提 IFA 版本，要寫成微軟自己寫得不一致，不可把兩者當成可互換。

### must_add

- **2026-09-04 那篇有一段實質內容整組漏掉：微軟明說 Zenith 機器之間的硬體會有差異。** 原文：'By working with our OEM partners, we give developers choice across devices and performance tiers while preserving the ready-to-code experience. The hardware may vary, but the developer promise is consistent - powerful for modern development, thoughtfully configured and ready for developers from the start.'**這是微軟對「Zenith 裝置之間什麼會變」唯一的說明，直接回應研究者正確標記為未解的「Zenith 到底是什麼」這個缺口。43 條事實裡一條都沒有。**
- **同一篇裡緊接在 30B+ 引句之前的那一句也漏了**：'Project Zenith devices come with a preconfigured Windows setup for development, and a set of tools curated for what developers reach first.'**這是微軟自己的一句話定義，也是最好翻譯的一句。**
- **Build 2026 那篇有一條路徑，正好回答研究者認為無解的讀者提問（「不買機器能不能用？」）**：除了 F26 記的 WinGet 路徑之外，微軟還宣布了 'Windows 365 with Developer configuration - Windows 365 comes pre-configured with the same Windows developer configuration, available in public preview.'**一條不需要任何硬體門檻的雲端 PC 路徑，截至 2026-06-02 處於公開預覽。紀錄完全沒有。**
- **F33（Surface RTX Spark Dev Box）漏了限定條件**：Build 2026 那篇註腳 [ii] 寫 'Microsoft Surface RTX Spark Dev Box and Surface Laptop Ultra are pre-release products. Products and features are subject to regulatory certification/approval; actual sale and delivery is contingent on compliance with applicable requirements.' F33 只記了「128 GB 統一記憶體」與「available later this year in the U.S. exclusively on Microsoft.com」。**要用 Dev Box 的供貨說法，這個但書就要跟著走。**
- **F22 講得太小了。** 研究者標出 AMD 那份清單寫 'GitHub Copilot CLI' 而圖表寫 'GitHub Copilot'，但更大的問題是：**微軟轉述的 AMD 開箱清單只有四項**（Visual Studio Code、WSL、GitHub Copilot CLI、PowerShell），微軟自己的圖表有 **18 項**；'WSL' 根本不是圖表上的條目（圖表寫的是 'WSL 2+ Ubuntu'）；AMD 的 'PowerShell' 沒有版本，圖表寫 'PowerShell 7'。**AMD 的四項清單與微軟的十八項圖表不可以當成同一件事。**
- **AMD 自己頁面內部的命名衝突，紀錄沒標**：規格表那一列寫 'Ryzen AI Max+ **PRO 495**'，註腳 GRHP-01 寫 'Ryzen AI Max+ **495 PRO**'。研究者在 F38、F39 各自引對了，卻沒記下這個衝突，**把兩者合併寫就會產生一個兩處都不存在的產品名。**
- **微軟「unmetered」這個詞的出處**：Build 2026 那篇有一節標題是 'Unmetered intelligence on Windows powered by on-device AI'，宣布裝置端小模型 'Aion 1.0 Instruct' 與 'Aion 1.0 Plan'，狀態是 'available in the coming months'。**這說明微軟自己的本機模型故事在 6 月時仍是未來式，正好強化研究者拒絕替 30B+ 那句掛上任何具名模型的判斷。**

### live_data_warnings

- 2026-09-04 的文章 `article:published_time` 與 `article:modified_time` 都是同日（modified 2026-09-04T13:17:30），**沒有事後修改**；但 **Build 2026 那篇自己的 `article:modified_time` 是 2026-06-05T14:18:38，也就是發布三天後被編輯過**，紀錄沒有記。引用 Build 那篇要寫「2026-09-16 讀取」。
- **Build 2026 裡所有 preview／GA 標籤都是 2026-06-02 當天的狀態，不是 2026-09-04 的狀態**（Coreutils for Windows 'now generally available'、WSL containers 'coming soon to public preview'、Windows Development Skills 'now generally available'、Intelligent Terminal 的狀態、Windows 365 developer configuration 'available in public preview'）。**Zenith 那篇沒有重述任何一個元件在 Zenith 上的預覽／正式狀態。這個警告必須寫進文章。**
- 三個 Windows 官方 feed 都是 **10 筆滾動視窗**（windowsdeveloper feed 最新 Mon 14 Sep 2026 17:00:49 +0000；blogs.windows.com/feed 最新 2026-09-14；devices feed 最新 2026-09-14）。**不可拿來證明「沒有更新」。**
- AMD 頁面有動態的相關文章欄，位元組數會漂移（研究紀錄 183,253、查核 183,411），**正文相同**。頁面 `og:updated_time` 2026-05-20T06:56:23-0500。
- AMD 的前瞻日期都是 2026 年 5 月 20 日當天的說法：預購 2026 年 6 月、次世代平台與 OEM 處理器 2026 年第三季、OEM 夥伴「starting this year」。**查核日重新確認 AMD 官網（`/en/newsroom/press-releases.html`、`ir.amd.com/news-events/press-releases`、`/en/blogs.html`）'Zenith' 均 0 次命中**，也就是**沒有任何可達的 AMD 一手頁載有 IFA 上那句 Zenith 表態**，研究者的排除正確。
- 預載工具圖表是從一張 PNG 讀出來的（頁面上是 `Preinstalled-tools-2-1024x625.png`，全尺寸 3756x2292）。**18 個工具名與 3 個欄位標題經查核者全解析度逐一重讀確認**，但它仍然是圖片快照，圖一換就過時。
- `https://blogs.windows.com/windowsdeveloper/wp-json/wp/v2/posts/57883` 回 **HTTP 401** `{"code":"rest_cannot_access"}`；**post id 57883 確實印在頁面 head 的 `<link rel="alternate" type="application/json">` 裡，不是猜的**，但這條網址取不到內容，不可記上 `checked_on`。
- `https://www.amd.com/en/blogs/advancing-ai-on-windows-with-microsoft.html`（從搜尋結果冒出來、研究者正確地沒有使用）回 **HTTP 404**。

### source_list_fix

**結構乾淨：43 條事實全部掛在四條 sources 之內，沒有掛外網址，沒有超量，四條全是一手（三個微軟部落格、一個 AMD 部落格）。** 三點要修：

1. **F43 的 feed 內容掛在文章網址**（見 must_fix 5）——改掛 feed 網址或移出 verified_facts。兩個 feed 網址目前都不在 `sources` 裡。
2. **F36 的「Micro Center 是美國零售商」不能掛在 AMD 網址上**（見 must_fix 4）——刪掉，或另尋來源。
3. F08 應記下頁面上的圖片網址 `Preinstalled-tools-2-1024x625.png`，並註明全尺寸版 `Preinstalled-tools-2.png` 是自行去掉尺寸後綴取得的（見 must_fix 3）。
4. `unverified_or_excluded` 正確隔離了 VideoCardz／Yahoo 的價格說法（查核者確認 AMD 頁面沒有價格、也沒有任何 '$'）與把 128 GB／200B 和 192 GB／300B 兩個產品混在一起的搜尋摘要。**這部分做得對，要保留。**

---
## 跨篇通則（13 篇裡重複出現的錯誤，寫成可以直接遵守的規則）

1. **不要從 `verbatim_quote` 直接取字串。** 13 篇裡有 9 篇的引文欄位靠不住：用「 / 」或「 | 」把頁面上兩個獨立元素串成一句（apple-eu-business-terms、apple-m6、iphone-duo 四條、nvidia-mediatek、taiwan-6g、taiwan-matsu）、把 Apple 的破折號「—」重打成「-」（apple-m6 七條）、漏掉單字（apple-m6 的 "performance"）、標點前留下 HTML 抽取的空格（eu-cra 四條）、悄悄修好來源自己的重複字（nvidia-cuda-q 的 'fault-tolerant fault-tolerant'）、或乾脆留空字串（nvidia-mediatek、sovereign-ai-corpus）。**引文一律回到來源頁重抄，或改寫成敘述而不是引用。**

2. **研究者自己算出來的數字不是事實。** 出現過的有：Apple Intelligence「16 種語言」（來源只列名）、「150 physical qubits per logical qubit」（150,000÷1,000）、三組 4G 頻段「合計 280 MHz」、CSIRT「27 個會員國」、「exactly six organisations」、Pixel Drop「五項功能」（實際四項）。**BRIEF 的規則是每個數字要指得到來源原文；自己加總、相除、清點出來的數字要嘛不寫，要嘛明寫是編輯換算。**

3. **「以 including／例如 引出的清單」不是完整清單。** NVIDIA 的 CUDA-Q Logical 使用者名單、NVLink Fusion 的三項技術、Apple 各語系的上市地區名單（台灣版有台灣沒有 Türkiye、美國版相反；iPhone Duo 台灣版 63 個對英文版 70 個）都是舉例。**不可以寫成「共 N 家／共 N 國」，也不可以拿某一語系的名單當全名單。**

4. **不要把「來源沒提到」寫成「來源說沒有」。** 被推翻的例子：iPhone Duo「內螢幕不是用超瓷晶盾 2」、iPhone Duo「沒有 NCC 相關敘述」、apple-september「當天沒有 Apple Watch SE」、pixel-drop「有一篇 September Android Drop」、windows-zenith 的 Intel grep、apple-m6 的 foundry grep、nvidia-vera-rubin 的 Taiwan／TSMC grep、nvidia-cuda-q 的分支命名。**否定命題要嘛限縮到「這一頁沒有寫」，要嘛不寫。**

5. **`is_vendor_claim` 旗標不可信，要自己判斷。** 被標成 false 卻其實是廠商量測或宣稱的有：Apple 的再生材料比例與可再生能源比例、iPhone Duo 的充電時間與「零快門延遲」與「首次」與「超過 500 家電信業者」、NVIDIA／聯發科對未出貨平台的能力描述、中華電信對斷纜原因的「初步推估」。**規則照 BRIEF：廠商或機關自己量的、自己說的，一律「Apple 表示／NVIDIA 表示／中華電信初步推估／ENISA 表示／數發部指出」。**

6. **同一家公司的不同語系版本會給出不同的數字與不同的對沖詞，不可混用也不可擇一。** iPhone Duo：台灣版把英文的 'up to' 拿掉（20%、40%），還把 40% 多掛給能源效率，並把 MagSafe／Qi2 配到 20 分鐘那一邊；iPhone 18 Pro：台灣版 34／43 小時對美國版 36／45 小時（且 eSIM-only 限定語只掛在後者）；Apple 兩篇同日稿對 M5 Ultra 給 4.5 倍與 4.3 倍且標籤不同（GPU 峰值運算 vs 整機 AI 運算效能）；微軟自己把 '250+ GB/s' 寫成 '250gbps'。**兩個版本都是官方，要並列並註明各自出處，不可以挑一個當唯一數字。**

7. **feed 與列表頁是滾動視窗，不能拿來證明「沒有」。** Apple Newsroom Atom 20 筆、Apple Developer RSS 142 筆、NVIDIA releases.xml 20 筆（且 `?page=` 參數伺服不一致）、Windows 三個 feed 各 10 筆、歐盟 presscorner 10 筆、moda 新聞列表 15 筆、聯發科 RSS 10 筆。本批次有三篇因此下了錯誤結論（apple-eu、apple-m6、sovereign-ai-corpus），**而其中兩篇要找的文章其實就在窗內或用 sitemap 一步就拿得到。拿不到就去找 sitemap、開放資料 CSV 或官方索引頁，不要用「feed 裡沒有」當結論。**

8. **HTTP 200 不代表拿到東西。** 本垂直實測到的陷阱：NVIDIA 新聞室的軟性 404（少半段網址回 200，標題是 `News Archive`）、MOPS 回 200 但 body 是 800 bytes 的安全阻擋頁、EUR-Lex 回 202 加 0 bytes、CELLAR 端點缺 `Accept-Language` 回 400、`docs.nvidia.com` 的表格是前端渲染 curl 看不到、`taic /partners` 的 SSR body 沒有正文、PDF 對 HEAD 回 404 但 GET 給檔案。**判斷「拿到了嗎」要看 body，而且研究紀錄要寫下完整的取得配方（含自訂標頭）。**

9. **`sources[]` 上限是 4 條，而 13 篇裡有 10 篇把事實掛在表外網址。** 最嚴重的是 taiwan-matsu-cable（43 條裡 21 條掛在 12 個表外網址）、sovereign-ai-corpus（60 條裡 21 條／10 個網址）、apple-september-hardware（91 條裡 20 條／7 個網址）、taiwan-6g-spectrum（28 條裡 11 條／9 個網址）。**動筆前先決定四條 sources，再把文章範圍收到那四條真的涵蓋的事實上；不要指望事後換 source。** 相對地 iphone-duo、pixel-drop、windows-project-zenith 三篇是 0 條掛外，可以當成範本。

10. **活文件要寫出「讀到的是哪一版」。** Apple 的六個 Newsroom 頁全部 dateModified 2026-08-27；歐盟與 ENISA 每頁都印自己的最後更新日；NVIDIA 高峰會那篇在查核期間又被改過（modified 2026-09-16）；Apple 開發者授權合約在公告後被改過（Last-Modified 2026-09-10）；台灣版 Apple Watch Ultra 4 在發布後被改過且留有編輯殘跡。**引用一律寫「2026 年 9 月 16 日查核」，而且不要寫到秒——Apple 同一天就有兩個 CDN 版本，秒級時間戳重現不了。**

11. **登記表、儀表板與 API 端點的數字會在查核當天移動，而且同一機關的不同來源會互相矛盾。** 最典型的是主權 AI 語料庫：同日新聞稿寫 22 億 tokens（截至 8 月底）、簡報寫 21 億、moda 儀表板寫 2,161,123,541、taic 端點寫 2,200,397,354，而資料集數 6,417 與 318.59 GB 遠高於簡報的 5000 與 200 GB；合作夥伴 34+22+5 也不等於簡報的「政府機關參與 250」。海纜障礙表的更新日期就是查核日。**每個計數都要標出處與時點，不同來源的計數不可以出現在同一句話裡、更不可以相加相減。**

12. **`/latest/` 這類不鎖版本的網址不要進 `sources`。** CUDA-Q 文件三條都指 `/latest/`，今天描述 0.16.0，0.17.0 一出就會描述別的東西；版本鎖定的 `/0.16.0/` 網址今天位元組完全相同。**能鎖版本就鎖版本，並在紀錄寫明讀的是哪一版。**

13. **不要把識別碼、網址或檔名推出來。** 本批次出現的：`Preinstalled-tools-2.png`（把 WordPress 尺寸後綴拿掉推出來的）、`op.europa.eu` 紀錄頁（用 cellar id 拼的）、`apple.com/tw/watchos/feature-availability`（從 iOS 那條路徑類推的）、`nvidianews.nvidia.com/releases.xml?page=3`（重現不了）。**這些即使解析得到也要在紀錄裡寫明「是推出來的」；BRIEF 說猜對也算捏造。**

14. **交給查核的研究紀錄被截斷，會留下整段沒人看過的內容。** `apple-september-hardware` 有 91 條事實但只有前 34 條經過查核；`sovereign-ai-corpus` 有 60 條但第 41 條之後未查核；`taiwan-matsu-cable` 的 `not_said` 最後一項在中途被截斷。**那些區段不是「通過查核」，是「沒被看過」。撰稿代理用到那裡的內容，要先送第二輪。**

15. **本垂直的兩條 tech.md 紅線在所有 13 篇一體適用**：不寫購買、升級或機型比較建議（官方定價可以寫，但要有來源與查核日，不做「現在買最划算」的結論）；**不加投資免責 callout**——科技篇不帶 `finance` 主題，`finance_no_disclaimer` 不適用。另外，站上尚無 tech 垂直的索引內容包（`apps/api/app/guides/content` 下只有 `ai-news-*` 與索引），BRIEF 要求的第一個 link 指不到目標，**撰稿代理不要自創索引 slug，留給索引階段統一處理。**
