# ai-news-meta-one-subscription-20260915 查核報告（第一輪）

- 查核者：獨立查核代理（第一輪），未參與撰稿
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/ai-news-meta-one-subscription-20260915.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-meta-one-subscription-20260915.json`
- 主張數 91：CONFIRMED 72／CHANGED 18／NOT FOUND 1（已改寫）／OUT OF SCOPE 0
- 事實類更動 11 處，DELTA-4-7 第 14 條讀者優先更動 7 處

## 1. `sources[]` 今天重抓的結果

同一主機間隔 ≥1 秒，UA 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`；
請求的 UA、標頭、查詢字串都沒有帶入任何姓名或 email。

| # | 網址 | HTTP | bytes | 轉址 | body 是否為正文 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://about.fb.com/news/2026/09/introducing-meta-one-subscription-service-more-features-ai/` | 200 | 713,186 | 0 | 是。`entry-content` 抽出 6,044 字元、`highlights-container`（Takeaways）387 字元，JSON-LD `wordCount` 991 |
| 2 | `https://about.fb.com/news/` | 200 | 307,920 | 0 | 是。這一則的卡片同時印 `published 2026-09-15T08:00:59-07:00` 與 `updated 2026-09-16T13:22:09-07:00` |
| 3 | `https://about.fb.com/news/2026/09/presentation-de-...-se-demarquer/` | 200 | 855,949 | 0 | 是。正文抽出 8,672 字元，含歐元定價 |

三條的 bytes 與研究紀錄記的完全相同，頁面文字沒有在這兩天內變動。
另以程式逐條比對研究紀錄的 `verified_facts` 32 條與 `sources[]` 3 條 `verbatim_quote`（彎引號、NBSP
正規化後做連續字串比對）：**35 條全部在今天抓下的頁面裡找得到，0 條落空**，`sourcing_verdict: full` 成立。
內容包裡印出的 4 段英文引文也逐字比對通過。

`https://www.meta.com/meta-one-plans/` 依規格**不是來源**：內容包全篇 0 次提及、`sources[]` 沒有列，
與研究紀錄 `unverified_or_excluded` 1、`must_not_write` 6 一致。本輪沒有重抓它，也沒有用它撐任何句子。

## 2. 主張表

驗證欄：C＝CONFIRMED、X＝CHANGED、N＝NOT FOUND。來源縮寫：EN＝主來源、NR＝新聞總覽頁、FR＝法文版。

| # | 欄位 | 主張 | 來源怎麼寫 | 判 |
| --- | --- | --- | --- | --- |
| 1 | title | Meta One 訂閱服務上線 | EN「Today, we're introducing Meta One」 | C |
| 2 | title | 官方說核心**功能**維持免費 | EN 寫的是 core **experience** | **X** |
| 3 | title | 台灣價格沒有寫 | EN 全文 `Taiwan` 0 次 | C |
| 4 | description | 2026-09-15 Meta 宣布推出 Meta One | JSON-LD `datePublished 2026-09-15T15:00:59+00:00` | C |
| 5 | description | 三個 Plus 方案併入同一品牌 | EN「Earlier this year, we launched Meta One single product plans」 | C |
| 6 | description | 新增個人與商家方案 | EN Core／Premium、Essential／Advanced／Expert／Max | C |
| 7 | description | 核心體驗維持免費 | EN「has always been free, and that's not changing」 | C |
| 8 | description | 付費解鎖更多 AI 生成用量 | EN「expanded AI usage」 | C |
| 9 | description | 價格與供應因地區而異 | EN「may vary by region, by app, and by account」 | C |
| 10 | description | 公告全文未提及台灣 | 同 3 | C |
| 11 | description | 句尾「（2026 年 9 月查證）」、無查證流水帳 | DELTA-4-7 第 14 條 | C |
| 12 | 第一段 | 事件日 2026 年 9 月 15 日（＝slug 尾碼＝`news_date`） | 同 4 | C |
| 13 | 第一段 | 在官方新聞室宣布 | about.fb.com＝Meta Newsroom | C |
| 14 | 第一段 | 併入 IG Plus／FB Plus／WA Plus 三個方案 | EN 同 5 | C |
| 15 | 第一段 | 兩種個人組合＋四種創作者及商家方案 | EN 方案清單 | C |
| 16 | 第一段 | 發布日落在上一輪整理區間外，這一輪補上 | DELTA-4-7 第 1 條、研究紀錄 `sourcing_notes` | C |
| 17 | 第二段 | 查核日 2026 年 9 月 23 日 | 與三條 `checked_on` 一致；本輪重抓同日 | C |
| 18 | 第二段 | 「讀的是公告英文版、法文版與 Meta 新聞室總覽頁」 | 屬實，但是查證流水帳 | **X** |
| 19 | 第二段 | 本站沒有實測、不提供訂閱或購買建議 | `ai.md` 界線 | C |
| 20 | 第二段 | 公告 9 月 16 日又被改過一次，沒有編輯說明 | `dateModified 2026-09-16T20:22:09+00:00`；全頁無編者註 | C |
| 21 | summary 1 | 2026-09-15 宣布、三個舊方案併入 | 同 4、5 | C |
| 22 | summary 1 | 新增兩種個人組合與四種創作者及商家方案 | 同 15 | C |
| 23 | summary 1 | 官方表示 FB／IG／WA 與 Meta AI 的核心體驗一直是免費的 | EN 寫 our apps；NR 摘要自己寫 on Facebook, Instagram, WhatsApp, and Meta AI | C（見待決 1） |
| 24 | summary 2 | 訂閱解鎖更多 AI 生成用量與表達功能 | EN「more self-expression features and AI usage」 | C |
| 25 | summary 2 | 單一產品 2.99 起、個人組合 7.99 起、創作者商家 14.99 起 | EN「start at just $2.99 … $7.99 … $14.99」 | C |
| 26 | summary 2 | 公告只印美元符號，沒有幣別代碼 | EN 全文 `USD` 0 次 | C |
| 27 | summary 3 | 方案現已在全球提供 | EN「now available globally」 | C |
| 28 | summary 3 | 價格、權益與供應可能因地區、App 與帳號而異 | EN 同 9 | C |
| 29 | summary 3 | 摘要欄位另外寫逐步推出 | Takeaways「rolling out gradually」 | C |
| 30 | summary 3 | 全文沒有台灣，也沒有售價或開放時間 | 同 3 | C |
| 31 | summary 4 | 累計超過 50 項功能上線、1,500 萬份訂閱與試用 | Takeaways 逐字 | C |
| 32 | summary 4 | 官方未拆分期間與付費比例 | EN 未寫 | C |
| 33 | summary 4 | 9/16 改過、無編輯說明 | 同 20 | C |
| 34 | §1 p1 | 「官方把這句話放在公告**最前面**」 | 被引句在 `entry-content` 第二段；最前面的是 Takeaways | **X** |
| 35 | §1 p1 | 引文 The core experience … that's not changing. | 逐字比對通過 | C |
| 36 | §1 p1 | 「這句話講的是既有事實，**不是對未來的新承諾**」 | Takeaways 第三條正是未來式「will stay free」 | **X** |
| 37 | §1 p2 | 訂閱解鎖更專門的功能與更多 AI 用量，超出免費體驗所能提供的範圍 | EN「Subscriptions unlock more specialized capabilities…」 | C |
| 38 | §1 p2 | 更多 Meta AI 媒體生成：建立與編輯圖片、Muse 模型生成影片 | EN「creating and editing images and generating videos powered by Muse models」 | C |
| 39 | §1 p2 | Instagram 內建 AI 工具（Restyle）的「使用次數」 | EN 只寫 more **use**，沒有量化成次數 | **X** |
| 40 | §1 p3 | Meta One 不是從零開始，三個方案今年稍早就已推出 | EN 同 5 | C |
| 41 | §1 p3 | 官方對舊方案只給形容詞：留存表現強勁，沒有數字 | EN「These plans are seeing strong retention」 | C |
| 42 | §2 p1 | WhatsApp Plus 每月 2.99 美元 | EN「WhatsApp Plus ($2.99/mo)」 | C |
| 43 | §2 p1 | Instagram Plus 與 Facebook Plus 各 3.99 美元 | EN 兩行各 ($3.99/mo) | C |
| 44 | §2 p1 | Core 每月 7.99 美元 | EN「Core ($7.99/mo)」 | C |
| 45 | §2 p1 | Premium 19.99 美元 | EN「Premium ($19.99/mo)」 | C |
| 46 | §2 p1 | Premium＝Core 全部＋最多的 Meta AI 創作空間與「跨 App **額度**」 | EN「the most room to create content with Meta AI and across our family of apps」 | **X** |
| 47 | §2 p2 | 創作者與商家方案分四階，價格標 starting at | EN 四階皆 starting at | C |
| 48 | §2 p2 | Essential 自 14.99 起，賣點是建立形象、贏得新受眾信任 | EN「Establish yourself and build confidence with new audiences」 | C |
| 49 | §2 p2 | 防冒名保護與驗證徽章須先通過驗證才會啟用 | EN「(pending successful verification)」 | C |
| 50 | §2 p2 | Advanced 自 49.99 起，官方形容為投資專業級工具 | EN「Invest in professional-grade tools」 | C |
| 51 | §2 p2 | Expert 自 149 起、Max 自 499 起，形容為擴大規模並最佳化 | EN「Scale and optimize」 | C |
| 52 | §2 p2 | 「公告**沒有列出功能清單**」 | EN 其實寫了 highest levels of feature access 與 Business Agent capacity | **X** |
| 53 | §2 p3 | 訂閱後可取得更多 Meta Business Agent 額度，不分日夜回覆顧客 | EN「respond to customers day and night with more access to Meta Business Agent」 | C |
| 54 | §2 p3 | 「站上小商家指南已寫過 Business Agent 開始使用免費、之後要訂閱」 | 出自 2026-08-19 另一則公告，不在 `sources[]` | **N** |
| 55 | §2 p3 | 商家在台灣怎麼申請、是否支援中文，公告沒有寫 | EN 未寫（限縮在這一頁） | C |
| 56 | 表格 | 單一產品列「2.99 **起**」「3.99 **起**」 | EN 印的是固定月費 ($2.99/mo)、($3.99/mo) | **X** |
| 57 | 表格 | 個人組合列「7.99 **起**」「19.99 **起**」 | EN 印的是 ($7.99/mo)、($19.99/mo) | **X** |
| 58 | 表格 | 創作者與商家列 14.99 起／49.99 起／149 起／499 起 | EN 四階皆 starting at | C |
| 59 | 表格 | 涵蓋範圍三列與方案名稱 | EN 三個小標 | C |
| 60 | 表格 | caption：金額為官方所印的美元數字（未附幣別代碼）、查核日 | EN 同 26 | C（已補寫哪四階才是 starting at） |
| 61 | §3 p1 | 引自「How to Get Started」一段 | EN 小標存在 | C |
| 62 | §3 p1 | 引文 Meta One plans are now available globally… | 逐字比對通過 | C |
| 63 | §3 p1 | 中譯：現已全球提供、三個起始價 | 與原文相符 | C |
| 64 | §3 p2 | 引文 Plans, benefits, pricing, and availability may vary… | 逐字比對通過 | C |
| 65 | §3 p2 | 摘要欄位的措辭是逐步推出 | Takeaways 同 29 | C |
| 66 | §3 p2 | 「這一篇把兩句並排寫出，不只取其一」 | 編務說明入正文 | **X** |
| 67 | §3 p3 | 公告全文沒有出現 Taiwan，也沒有列出任何國家或地區名單 | EN `Taiwan` 0 次、無地區清單 | C |
| 68 | §3 p3 | 「否定句只能限縮到……不能反過來說台灣訂不到」 | 查核規則入正文 | **X** |
| 69 | §3 p3 | 公告只印 $ 符號、沒有標示幣別 | 同 26 | C |
| 70 | §3 p3 | 法文版 Core 6.99 歐元／英文版 7.99 美元 | FR「Core (6,99 €/mois)」 | C |
| 71 | §3 p3 | 法文版 Premium 20.99 歐元／英文版 19.99 美元 | FR「Premium (20,99 €/mois)」 | C |
| 72 | §3 p3 | 兩組數字高低順序翻轉，代表各市場自己定價 | 6,99<7.99 但 20,99>19.99 | C |
| 73 | §3 p3 | 「這一篇因此不替台灣讀者換算或推估新台幣價格」 | 編務說明入正文 | **X** |
| 74 | 圖說 | 核心體驗官方說維持免費、付費層分三類、因地區 App 帳號而異、查核日 | 同 7、9；與研究紀錄 `diagram.caption` 逐字一致 | C |
| 75 | §4 p1 | 規模數字寫在正文前方獨立的摘要欄位，不在正文段落裡 | HTML 裡 `highlights-container` 在 `entry-content` 之前 | C |
| 76 | §4 p1 | 引文 Meta One plans are rolling out gradually… | 逐字比對通過 | C |
| 77 | §4 p1 | 訂閱與試用合計、沒有拆分比例、沒有起算期間、不能當付費人數 | EN 未寫 | C |
| 78 | §4 p2 | 早期測試中超過一半的訂閱者同時使用 AI 與表達功能 | EN「In early testing, more than half of subscribers engaged with both…」 | C |
| 79 | §4 p2 | Restyle 與語音效果「**是最常被提到的**訂閱原因」 | EN「**among** the top reasons people subscribed」 | **X** |
| 80 | §4 p2 | 原文沒有寫樣本數、測試期間或地區範圍 | EN 未寫 | C |
| 81 | §4 p2 | 「這一篇保留這些限定，不替官方補數字」 | 編務說明入正文 | **X** |
| 82 | §4 p3 | WhatsApp Plus 即將測試備份儲存與 Focus Schedules | EN「will soon test」 | C |
| 83 | §4 p3 | Edits Plus 與即將推出的 Edits 助理還沒開放 | EN「soon we'll bring…the upcoming Edits assistant」 | C |
| 84 | §4 p3 | 功能未來會擴展到 Edits 與 AI 眼鏡 | EN「will expand to Edits, AI glasses」 | C |
| 85 | §4 p3 | 「這一篇一律照 will、soon、upcoming 寫成即將」 | 編務說明入正文 | **X** |
| 86 | §5 p1 | 把三個獨立訂閱收整成三層結構的品牌 | EN 三個小標分組 | C |
| 87 | §5 p1 | 「AI 生成用量、客服代理額度這些**原本免費試用**的功能往上移到付費層」 | EN 沒有寫這些原本是免費試用 | **X** |
| 88 | §5 p1 | 「沒有主動訂閱，公告的說法是**現有功能不會因此消失**」 | EN 寫的是核心體驗免費＋「Meta AI will still be free for everyday use」 | **X** |
| 89 | §5 p2 | 「Muse 模型本身的能力，留給**第二個連結那篇**處理」 | 編務用語 | **X** |
| 90 | §5 p3 | 「想知道能訂閱到哪些方案與**價格**，直接從 **App 內**的訂閱流程查看」 | EN「To see the specific **features** available to your account, start the subscription process」 | **X** |
| 91 | §5 p3 | 既有 Plus 訂閱者怎麼被轉換、要不要重訂，公告沒有說明 | EN 未寫 | C |
| 92 | FAQ1 | 核心體驗一直是免費的，訂閱買到的是額外用量與工具 | 同 7、37 | C |
| 93 | FAQ2 | 公告全文沒有台灣、沒有地區名單 | 同 67 | C |
| 94 | FAQ2 | 「但**同一段**也寫明……」 | may vary 在正文倒數第二段，不與 now available globally 同段 | **X** |
| 95 | FAQ2 | 「要知道能訂閱到什麼方案與**價格**，官方建議從訂閱流程查看」 | 同 90 | **X** |
| 96 | FAQ3 | 1,500 萬是訂閱與試用合計、原文逐字、不能當付費人數 | Takeaways 逐字 | C |
| 97 | FAQ4 | 「起」代表分類裡最低的起始價、四階都標 starting at | EN 同 47 | C |
| 98 | FAQ4 | 「實際金額會依**選擇的功能與規模**而不同」 | EN 沒有寫原因；唯一寫的是 may vary by region, by app, and by account | **X** |
| 99 | FAQ4 | 公告沒有列出更高階的完整定價區間 | EN 未寫 | C |
| 100 | FAQ5 | 9/16 確實改過、無編輯說明與修訂紀錄、事件日仍照 9/15 | 同 20；DELTA-4-7 第 10 條 | C |
| 101 | FAQ6 | 更多 Meta AI 媒體生成、Muse 影片、Instagram 工具「使用次數」 | 同 39 | **X** |
| 102 | FAQ6 | 公告沒有列出各方案的張數、支數或分鐘數上限 | EN 未寫 | C |
| 103 | callout | 只有一個 callout、不帶 finance 主題、無投資免責段落 | `ai.md`；pack `topics` 為 ai／software／ai-news | C |
| 104 | callout | 不建議訂閱哪一個方案、不比較其他服務 | `ai.md` 界線 | C |
| 105 | 結尾連結 1 | text＝「2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用」 | 索引 pack 的 zh-TW title 逐字相同 | C |
| 106 | 結尾連結 2 | text＝「Meta Muse Spark 登場：社群裡的 AI 助手如何改變搜尋與提問？」 | 目標 pack 的 zh-TW title 逐字相同 | C |
| 107 | sources | 三條的 `checked_on` 均為 2026-09-23，與正文、caption、圖說一致 | 本輪重抓同日 | C |

（表列 107 行，其中 16 行是同一主張的分項；合併後可查證主張 91 條。）

## 3. 改掉的 18 處

事實類 11 處（1–11），讀者優先 7 處（12–18）。

1. **標題** `核心功能維持免費` → `核心體驗維持免費`。公告寫的是 core **experience**，而這一篇的主旨正是
   「功能」被移進付費層；`description`、正文與研究紀錄 `diagram.nodes` 本來就寫「核心體驗」，只有標題是例外。
   研究紀錄的 `title` 已同步。（EN）
2. **§1 p1** `官方把這句話放在公告最前面` → `公告正文把這句話放在前段`，並補上
   `頁首的摘要欄位則寫成未來式的 will stay free（會維持免費）。前一句講的是過去到現在，後一句才指向之後。`，
   刪掉 `這句話講的是既有事實，不是對未來的新承諾`。被引的那一句在 `entry-content` 第二段；真正放在最前面的是
   `highlights-container` 的 Takeaways，而它的第三條正是未來式的
   `The core experience across our apps and Meta AI will stay free.`（研究紀錄 `verified_facts` 5、
   指派表也點名這一句）。草稿整篇沒有提到它，於是把官方的一句未來式說法寫成了「不是對未來的新承諾」。（EN）
3. **§2 p1** `再加上最多的 Meta AI 創作空間與跨 App 額度` → `再加上在 Meta AI 與旗下 App 家族裡最多的創作空間`。
   原文 `Everything in Core, with the most room to create content with Meta AI and across our family of apps.`
   沒有任何「額度」。（EN）
4. **§2 p2** `兩階官方形容為擴大規模並最佳化，公告沒有列出功能清單` →
   `兩階寫的是擴大規模並最佳化，內容是最高等級的功能存取與 Meta Business Agent 容量，給大規模經營的團隊`。
   公告其實寫了 `These plans include our highest levels of feature access and Meta Business Agent capacity
   for teams managing at scale.`，原句的否定超出了「這一頁沒有寫」的範圍。（EN）
5. **§2 p3**（NOT FOUND）刪掉 `站上既有的小商家 AI 指南已寫過 Business Agent 開始使用免費、之後想用更多要訂閱
   Meta One`，整段改成 `……讓客服代理不分日夜回覆顧客，Advanced 以上再加上更多回覆則數。這次公告把這項額度列在
   收費的商家方案裡；商家在台灣怎麼申請、是否支援中文，公告沒有寫。`。那句事實出自 2026-08-19 的 Meta for
   Business 公告，不在 `sources[]`，研究紀錄 `unverified_or_excluded` 6 與 `must_not_write` 14 明文排除；
   改寫後改用公告自己寫的 `even more Meta Business Agent responses`（Advanced）。（EN）
6. **表格**`2.99 起（WhatsApp Plus）、3.99 起（…）` → `2.99（WhatsApp Plus）、3.99（…）`，
   `7.99 起（Core）、19.99 起（Premium）` → `7.99（Core）、19.99（Premium）`。公告對這五個方案印的是
   `($2.99/mo)`、`($3.99/mo)`、`($7.99/mo)`、`($19.99/mo)` 的固定月費，只有 Essential／Advanced／Expert／Max
   四階寫 `starting at`。原表格與同一篇的 §2 p1 正文和 FAQ4 互相矛盾。caption 同步補上
   `創作者與商家四階原文標的是 starting at，所以寫「起」，其餘是公告直接標示的月費`。（EN）
7. **§4 p2** `是最常被提到的訂閱原因` → `名列最主要的訂閱原因`。原文
   `among the top reasons people subscribed`，草稿刪掉 `among`、變成最高級。（EN）
8. **§5 p1** `把更多 AI 生成用量、商家客服代理額度這些原本免費試用的功能，往上移到付費層` →
   `並把更多 AI 生成用量與商家客服代理額度放進付費層`。公告沒有說這些功能原本是免費試用
   （Business Agent 的免費期出自不在 `sources[]` 的另一則公告）。（EN）
9. **§5 p1** `公告的說法是現有功能不會因此消失` →
   `公告的說法是核心體驗維持免費，Meta AI 的日常使用也仍然免費`。官方真正寫的是
   `Meta AI will still be free for everyday use`（`verified_facts` 20）。（EN）
10. **§5 p3／FAQ2** `想知道自己的帳號能訂閱到哪些方案與價格，直接從 App 內的訂閱流程查看` →
    `想知道自己的帳號有哪些方案與功能可用，公告寫的做法是走一次訂閱流程去看`；FAQ2 同步改成
    `要知道自己的帳號有哪些功能可用，官方寫的做法是開始訂閱流程來查看`。原文
    `To see the specific features available to your account, start the subscription process.` 寫的是
    **功能**、不是價格，也沒有說在 App 內。FAQ2 的 `但同一段也寫明` 一併改成 `但同一頁也寫明`——
    `may vary` 那一句在正文倒數第二段，不與 `now available globally` 同段。（EN）
11. **FAQ4** 刪掉 `實際金額會依選擇的功能與規模而不同`，改成
    `單一產品與個人組合方案則是直接標一個月費。公告本身沒有列出更高階的完整定價區間，只寫方案、權益、價格與
    供應可能因地區、App 與帳號而異。`。公告沒有寫金額為何不同，唯一給的理由是
    `may vary by region, by app, and by account`。（EN）
12. **§1 p2／FAQ6** `Instagram 內建 AI 工具（例如 Restyle）的使用次數` → `……的使用`。
    原文是 `more use of in-app AI tools`，沒有量化成次數。（EN）
13. **第二段** 刪 `讀的是公告英文版、法文版與 Meta 新聞室總覽頁；`（DELTA-4-7 第 14 條：查證流水帳不寫進正文）。
14. **§3 p2** `摘要欄位的措辭是逐步推出，跟正文現已全球提供不是同一句話，這一篇把兩句並排寫出，不只取其一。` →
    `頁首摘要欄位的措辭又是逐步推出，跟正文的現已全球提供不是同一句話。`（事實不變，刪編務說明）。
15. **§3 p3** `否定句只能限縮到這一則公告沒有寫台灣，不能反過來說台灣訂不到。` →
    `這只代表這一則公告沒有寫台灣，不等於台灣訂不到。`（把查核規則改成對讀者說的話）。
16. **§3 p3** `這一篇因此不替台灣讀者換算或推估新台幣價格。` →
    `把美元數字換算成新台幣不會是台灣的售價。`（同上，依據仍是英法兩版價格不成換算關係）。
17. **§4 p2／§4 p3** 刪 `這一篇保留這些限定，不替官方補數字。` 與
    `這一篇一律照 will、soon、upcoming 寫成即將，不當成已上線的功能。`（DELTA-4-7 第 14 條；
    預告的三項事實原句未動）。順帶解掉 §4 p2 的「一段兩次歸因」。
18. **§5 p2** `Muse 模型本身的能力，留給第二個連結那篇處理。` → `Muse 模型本身的能力，站上另一篇也寫過。`
    （「第二個連結」是編務用語，讀者看不懂）。

## 4. 查過而且正確的部分

- **事件日與日期一致性**：JSON-LD `datePublished 2026-09-15T15:00:59+00:00`（台北 9/15 23:00）、
  `dateModified 2026-09-16T20:22:09+00:00`；新聞總覽頁的卡片同時印 published `2026-09-15` 與
  updated `2026-09-16`。slug 尾碼 `20260915`＝`news_date 2026-09-15`＝正文第一段「2026 年 9 月 15 日」。
  法文版 `datePublished`／`dateModified` 都在 9/15，而它的摘要已帶 1,500 萬那一條——所以那個數字不是 9/16
  才有的，草稿也沒有寫成「9/16 更新後新增了……」，符合 `must_not_write` 7。
- **1,500 萬的處理**：摘要、正文、FAQ3 三處都寫成「訂閱與試用合計、官方到查核日為止的累計說法」，
  沒有一處寫成付費人數、會員數或訂閱者數。
- **台灣**：全文 `Taiwan` 0 次；文章的否定句都限縮在「這一則公告沒有寫台灣」，沒有推定台灣訂得到或訂不到。
- **歐元與美元**：文章明寫兩組價格不是換算關係，並用 Core（6,99 € < $7.99）與 Premium（20,99 € > $19.99）
  高低翻轉當證據；全篇沒有台幣換算、沒有匯率。
- **預告與已上線**：WhatsApp Plus 的備份與 Focus Schedules（will soon test）、Edits Plus 與 Edits 助理
  （soon we'll bring／upcoming）、Edits 與 AI 眼鏡（will expand）四項都寫成即將，沒有寫成已上線。
- **「首次／唯一」**：全篇 0 次；§1 p3 明寫三個 Plus 方案今年稍早就已推出。
- **`ai.md` 界線**：沒有購買、升級或退訂建議，沒有與 ChatGPT／Gemini 或任何服務比價；「投資」只出現在
  `Invest in professional-grade tools` 的譯文裡；只有一個 callout、不帶 finance 主題、沒有投資免責段落。
- **廠商宣稱的歸因**：留存表現強勁、超過一半的訂閱者、50 項功能與 1,500 萬、方案效益描述都掛著
  「Meta 表示／官方寫」；`meta.com` 方案頁 0 次提及。
- **兩個結尾連結**：text 與目標 pack 的 zh-TW title 逐字相同（已用程式比對），本輪未動。
- **`checked_on`**：三條 source、研究紀錄、正文第二段、表格 caption、圖說六處都是 2026-09-23，本輪重抓同日，未改。
- **研究紀錄本身**：32 條 `verified_facts` 的 `url` 全在 `sources[]` 內，35 條 `verbatim_quote` 今天全部可在
  頁面裡找到連續字串，沒有一條落空。

## 5. 留給協調者／站主的事

1. **summary 第一條把 `the core experience across our apps` 寫成「Facebook、Instagram、WhatsApp 與 Meta AI」**。
   本輪沒有改：新聞總覽頁對這一則的摘要自己就寫
   `a new subscription service on Facebook, Instagram, WhatsApp, and Meta AI`（`sources[2]` 的
   `verbatim_quote`），公告正文也寫 `launching with more than 50 features on Instagram, Facebook,
   WhatsApp, and Meta AI`。但 `our apps` 的範圍比這四個大（同一頁就提到 Messenger 與 Edits）。
   要更保險就收斂成「旗下 App 與 Meta AI」——請第二輪或站主決定。
2. **表格標頭寫「官方標價（每月，美元）」，而公告只印 `$`、沒有幣別代碼。** caption 已註明，正文與 summary
   也都寫「公告只印美元符號，沒有幣別代碼」，本輪維持；若認為標頭不該直接寫「美元」，可改成
   「官方標價（每月，公告只印 $）」。
3. **字數只剩 98 字的空間**（2,902／3,000，五節各三段）。第二輪若要再補句子，得同時刪字，且不得刪但書或限定詞。
4. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug，本輪照 DELTA-4-7 第 15 條沒有跑 `--assets`。
   圖上的四格沿用研究紀錄 `diagram.nodes`（核心體驗／單一產品方案／個人組合方案／創作者與商家），
   圖說與 `diagram.caption` 目前逐字一致，改任一邊都要同步。

## 6. 自檢輸出（原樣）

```
OK ai-news-meta-one-subscription-20260915 zh-TW paragraphs 2902
check_article exit=0
```

```
ai-news-meta-one-subscription-20260915
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-meta-one-subscription-20260915/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-meta-one-subscription-20260915/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

兩個 log 檔：`_out/fc1_check_ai-news-meta-one-subscription-20260915.log`、
`_out/fc1_lint_ai-news-meta-one-subscription-20260915.log`。lint 只剩規格允許的
`image_missing`（圖還沒畫）與 `raw_internal_url`（還沒 relink）。

## 7. 結論

`needs_second_round`——依 DELTA-4-7 第 12 條，第一輪一律要有第二輪；本輪另有 11 處事實更動，
其中 §1 p1（補上 Takeaways 的未來式那一句）、§2 p3（刪掉引用 `sources[]` 以外那篇公告的事實）、
表格的「起」與 §5 p1 的免費界線四處動到論述，**第二輪務必逐句回一手來源重查這四處與所有新寫進去的句子**。
