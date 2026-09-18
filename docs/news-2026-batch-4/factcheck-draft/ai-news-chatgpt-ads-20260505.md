# 獨立查核：ai-news-chatgpt-ads-20260505

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 本來就是 2026-09-18，且四處一致，未改）。
查核方式：`sources[]` 全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；三份開發者文件的 HTML
去標籤後用 Python 做**連續字串**比對；RSS 以 ElementTree 解析、逐項核對 `pubDate` 與 `description`。
另外**重試了撰稿者宣告為「被存取阻擋」的四個網址**——那是本輪最大的發現，見下一節。
沒有猜任何網址或識別碼；所有請求的 User-Agent 都是 `Mokaair-editorial`，沒有帶入任何個人資料。

檢查的主張：**138 條**（正文 14 段、摘要 4 句、FAQ 5 題的問與答、callout、表格 12 格與 caption、
圖解 caption 與四格、`hero_label`、title、description，以及研究紀錄的 35 條 `verified_facts`、
7 條 `not_said`、8 條 `unverified_or_excluded` 與 `event_date_basis`）。
**改了 24 處**，其中一處是骨幹前提，另有 5 件留給站主。

## 重抓結果

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| **（新）**`openai.com/index/new-ways-to-buy-chatgpt-ads/` | 200 | 376,485 | **是**。去標籤後 7,200 字，含「OpenAI May 5, 2026」、Product／ChatGPT 標記、四個小節與全部內文 |
| `developers.openai.com/ads/api-overview` | 200 | 378,465 | 是。四層架構表、Rate limits、完整 Changelog |
| `developers.openai.com/ads/bidding-and-budgets` | 200 | 406,052 | 是。目標／計費對照表、Maximize Results、Campaign Budgets、Account Budgets |
| `developers.openai.com/ads/campaign-targeting` | 200 | 424,107 | 是。Inclusion & Exclusion、Geographic、Platform、Custom Audiences、Context Hints |
| **（移出）**`openai.com/news/rss.xml` | 200 | 736,773 | 是。四則項目逐字重抓確認，但不再列入 `sources[]` |

不帶尾斜線的公告網址 308 轉到帶斜線的那一個；`sources[]` 記的是最後落地的網址。
公告頁連抓三次是 376,489／376,525／376,481 bytes，內容一致——**位元組數是活值，不可當版本識別**。

## 最重要的一處：`openai.com/index/*` 並沒有被擋

研究紀錄與文章共有**五處**寫著「公告原文網頁在本站的查核環境會被系統擋下、讀不到正文，
所以凡是引用公告內容的地方，都只能引用新聞摘要那一句描述」，`sourcing_verdict` 也因此降為 `partial`。

**這句不成立。** 2026-09-18 以同一條 `curl -sL -A "Mokaair-editorial"` 指令重試，公告頁回 **HTTP 200**
與完整正文；同一產品線另外三則（`testing-ads-in-chatgpt` 423,935 bytes、
`chatgpt-ads-expands-across-europe` 394,806 bytes、`our-approach-to-advertising-and-expanding-access`
388,430 bytes）同樣都回 200 與真實正文。這是 BRIEF 錯誤型態 5「放棄的路徑被寫成環境限制」，
而且它的代價很大：整篇文章的核心事件只靠 RSS 的一句 156 字元描述撐著，
而那一頁本身有 OpenAI 對這次更新的完整說明（試行階段、分批開放、CPM→CPC、量測、隱私原則）。

依規格「除非你判定 `sources[]` 本身該換」，已把 `sources[0]` 從 feed 換成公告原文頁
（BRIEF：「`sources` 放的是文章頁的網址，不是 feed 的網址」），並以公告正文重寫第一節。
`sourcing_verdict` 由 `partial` 升為 `full`。

同理，`ads.openai.com`（200／191,408 bytes）與文件連出去的地點代碼目錄
`ads.openai.com/assets/openai-geotargets.csv`（200／44,595,955 bytes、615,788 列）也都讀得到。
**但後者不能回答台灣的問題**——見下面「查過而且正確的部分」第 2 點。

## 改掉的 24 處

1. **`sources[0]`：`openai.com/news/rss.xml` → `https://openai.com/index/new-ways-to-buy-chatgpt-ads/`**（理由如上）。
2–6. **刪掉全文五處「讀不到公告正文、只能引用新聞摘要」的敘述**（第二段、第一節第一段、
   第五節第二段、callout、FAQ 第 5 題），改以公告正文重寫。
7. **第一節兩段整段重寫。** 原本第二段是 1/16、8/11、8/18 三則 feed 摘要；`sources` 上限 4 條
   （`check_article.py` 硬性驗 `2 <= len(sources) <= 4`）已被公告頁與三份開發者文件用滿，
   那三則沒有名額，一併移出（**這是留給站主的第 1 件事**）。改寫後的兩段全部出自公告原文：
   一開始只和一小群廣告主合作、透過夥伴擴大、5/5 推出測試版自助工具、
   「逐步開放給更多企業」、第一階段只有 CPM、這次加 CPC、只依點擊結果付費、
   會繼續同時支援 CPM 與 CPC、Conversions API 與像素量測、廣告主只拿到彙整過的資料。
8. **「最低出價與最低預算依帳戶幣別而定……低於門檻會回錯誤訊息」把兩句不同的話併成一句。**
   原文是 `Daily minimums depend on the account currency. Requests below the applicable minimum
   return an error with the required amount.`（**每日預算**）與
   `Bid limits and permitted monetary precision depend on the account currency **and campaign
   objective**.`（**出價**，而且多一個條件）。已拆開兩句並補回「與活動目標」。
9. **「文件的原句是這些條件同時都要滿足」刪除。** `bidding-and-budgets` 的原句是
   `Delivery also depends on the campaign schedule, resource statuses, reviews, targeting, and
   available inventory.`——「還取決於」，沒有「同時都要滿足」的意思；那個語意來自 `api-overview`
   談啟用的 `Activation enables delivery when the remaining requirements are satisfied.`，
   文章別處已經用過。已改成「文件寫的是除了預算與出價之外，還取決於……」。
10. **平台分組補上「廣義」。** 原文是 `Use these **broad** platform groups:`，
    而同一站的更新紀錄 2026-09-10 已在 `web` 之下加了 `desktop_web`／`ios_web`／`android_web`。
    少了這個限定語，第四節的「三組」與第五節的「再細分成三種」會互相打架。已補，並加上
    文件寫明的「建立活動時沒設定平台鎖定則預設全部平台」。
11. **「排除優先」的範圍收回受眾。** 原文限定在
    `when someone belongs to both an included **audience** and an excluded **audience**`，
    前一版寫成泛指的「納入與排除名單」，緊接在地區那句之後，會被讀成地區清單也適用。
12. **2,500 的「各自」拿掉，並補回但書。** 原文是
    `You can include up to 2,500 IDs in geographic inclusion and exclusion lists. **Account
    availability and campaign mode can impose additional restrictions.**` ——沒有「各自」這個分法，
    而且後面那句但書整句被漏掉。
13. **「地區與平台鎖定」補回受眾。** 原文是
    `Geographic, platform, **and audience** settings work together`。
14. **四層設定被漏掉的項目補齊。** `api-overview` 的表格裡，廣告活動層還有
    `audience inclusion and exclusion, conversion events`，廣告組層還有 `product set`；
    另外 `New resources are created paused` 適用於三層，前一版的表格只寫廣告活動「預設為暫停」，
    第三欄已改成三層都預設暫停、廣告另加「素材送審」。
15. **「文件裡出現的金額都標明是示範用途」限縮到出價與預算頁。** 原文
    `**Budget and bid** examples use illustrative USD amounts.` 只涵蓋那一頁的預算與出價範例，
    不是「文件裡出現的金額」這個全稱。正文與 FAQ 第 2 題同步改。
16. **補上開放限制：`Spend-limit windows are available only to some accounts.`**
    文章原本把帳戶花費上限寫成人人都有。BRIEF 要求分批開放與限制要分開寫。
17. **更新紀錄 9/9 那筆補上限定語。** 原文是
    `Added daily account spending limits for ad accounts **on postpaid invoice billing**.`
18. **context hints 的「自由文字」改成原文說法。** 原文寫的是描述
    `relevant products, use cases, or needs that the creative and landing page may not fully cover`，
    並另有一句 `Hints are not exact-match keywords.`——「自由文字」是推論，已改；
    「範例」改寫成「表格裡的範例」，因為 `These examples` 指的是那張寫法對照表。
19. **受眾識別碼補上「官方支援的」**（原文 `their **supported** SHA-256 variants`）；
    **「500,000,000 bytes（約 500 MB）」的編輯換算拿掉**，只留原文印的位元組數。
20. **FAQ 第 4 題（台灣）的理由換掉。** 原本寫「那份清單所在的網址在本站的查核環境讀不到」——
    該網址實測可讀（44.5 MB 的地點代碼目錄）。已改成「本文查核的四條來源都沒有列出可投放地區清單」，
    並補上帳戶可用範圍與活動模式的額外限制。**結論（不回答台灣）沒有變，變的是理由。**
21. **description 與 callout 重寫**，不再說依據是「官方新聞摘要」。
22. **研究紀錄兩條 `verbatim_quote` 不是逐字。** 第 17 條
    `Added granular web platform targeting with desktop_web , ios_web , and android_web …`
    的空格是去標籤工具在 `<code>` 前後插出來的；第 19 條 `Campaign objective (\`bidding_type\`)`
    的反引號只存在於 `.md` 版，不在被引用的 HTML 網址上。兩條都已換成頁面上搜尋得到的連續字串。
    **重寫後 35 條引文全部通過連續字串比對。**
23. **`event_date_basis` 不再拿佔位時刻換算台北時間。** feed 給 5/5 的 `pubDate` 是
    `Tue, 05 May 2026 00:00:00 GMT`，而同一份 feed 裡有數百筆同樣是 `00:00:00 GMT`——
    BRIEF 第 14 條說那是佔位值、**日期可用時刻不可用**。原紀錄對 1/16 那則套了這條規則、
    對 5/5 卻換算成「台北 08:00」，自相矛盾。現在事件日改以公告頁自己印的 `OpenAI May 5, 2026` 為準
    （更強的證據），不做時刻換算；HTML 裡也沒有 `datePublished` 之類的結構化時間欄位。
24. **`sourcing_verdict` `partial` → `full`**，`sourcing_notes` 重寫並寫明來源清單為何重建。

## 查過而且正確的部分（沒有動）

1. **「轉換目標仍按有效點擊計費」——撰稿者點名要重查的反直覺結論，沒有讀反。**
   `bidding-and-budgets` 三處互相印證：目標對照表的 `conversions` 列 billing event 是 `click`
   （兩列都是）；內文 `Conversion campaigns optimize for the selected action and bill for valid
   clicks.`；Maximize Results 一節 `Both strategies use billing_event_type: "click".`。
   設定表另寫明 Billing event 決定的是 `Whether you pay for impressions or clicks`。
   文章的「把目標設成轉換，改變的是出價要最佳化的方向，付費依據仍然是點擊」成立。
2. **全文刻意不回答「台灣能不能投／看得到廣告」是正確的，而且是必要的。**
   四條來源逐詞查核到 2026-09-18，`Taiwan`／`TW`／國家清單在三份開發者文件與公告頁都未見；
   `campaign-targeting` 只有一句 `use supported advertising locations` 與一個指向
   `ads.openai.com` 目錄的連結。**那份目錄本輪確實下載得到**（615,788 列，其中 391 列國碼是 `TW`，
   含一列 Target Type 為 `Country` 的台灣），**但它回答不了這個問題**——同一頁自己寫著
   `A code’s ISO validity does not mean it is available for advertising in your account`，
   目錄列的是可填的地點代碼，不是可投放地區清單。所以即使讀得到也不能寫，
   而且 `campaign-targeting` 頁上**沒有**任何地區清單，不存在「照來源寫」的選項。
3. **25,000 沒有「少了但書」的問題——因為它一次都沒出現。**
   逐字掃過正文、摘要、FAQ、表格與圖解，`25,000` 出現 0 次。值得記下的是：這個數字其實就在
   `sources[]` 內的 `campaign-targeting`（同一頁兩次，寫成**硬性要求**
   `Inclusion and bid multipliers require at least 25,000 matched users`），
   而未列入 `sources` 的 `custom-audiences` 把它寫成 `public planning threshold` 加隱私邊界但書。
   兩個官方頁強度不一致，依 BRIEF 第 8 條不可以挑一個當唯一說法——**維持不寫是對的**。
4. **三則公告的日期與時區**（雖然 8/11、8/18 兩則本輪已移出文章）：
   5/5 `Tue, 05 May 2026 00:00:00 GMT`（佔位時刻）、8/11 `10:00:00 GMT`（台北同日 18:00，不跨日）、
   8/18 `22:00:00 GMT`（台北 **2026-08-19 清晨 6 點**）。前一版正文寫「8 月 19 日清晨」並註明換算依據，
   **處理正確、前後一致**，沒有任何一處寫成「8 月 18 日」。換算結果已移進研究紀錄的
   `unverified_or_excluded`，站主若要補回那一段可以直接取用。
5. 四則 RSS 項目的 `title`／`pubDate`／`category`／`link`／`guid`（`isPermaLink=true`）逐字重抓確認，
   與研究紀錄相符；`slug` 尾碼、`news_date`、`event_date` 三處都是 2026-05-05。
6. 四層架構、`chat_card`、640 × 640、預覽不等於上線資格、帳戶 `active` 仍可能有未結案審核、
   micros 換算、Maximize Results 的每日預算與省略出價金額、`fixed_bid` 可用每日或總預算、
   活動預算與帳戶花費上限各自獨立、iPhone 瀏覽器算 web 版位、500,000,000 bytes、
   context hints 不保證觸發——全部逐字回原文確認無誤。
7. 更新紀錄的日期範圍 2026-06-03 至 2026-09-10、以及「再往前只有一則未標日期的 v1」逐條核對無誤。
8. **界線**：全文沒有投放建議、沒有效益判斷、沒有推薦式比價、沒有「值得投／該試試／比較划算」這類結論
   （逐詞掃過，0 次）。廠商宣稱一律寫成「公告說」「OpenAI 表示」「文件寫明」，
   沒有任何一句寫成本站觀察到的行為。分批開放／限制四處都寫出來了：測試版、逐步開放給更多企業、
   花費上限期間只給部分帳戶、每日花費上限限後付發票制帳戶。
   非窮舉清單也標明了：公告的代理商與技術夥伴那兩句用 `including`／`such as`，
   文章明寫「不是完整名單」，不列名單、不寫家數。
   AI 篇只有一個 callout，**沒有**投資免責段落。
9. **活資料沒有入稿**：RSS 的 `<item>` 總數（本輪抓到 1,207，與紀錄的 1,194／1,195／1,196 都不同）、
   `lastBuildDate`、sitemap 的 `lastmod`、頁面 bytes 數、地點代碼目錄的列數——一條都沒有寫進文章，
   只記在研究紀錄的 `live_data_warnings`。
10. 摘要四句的每個數字都在正文出現；FAQ 五題的答案都是純文字、沒有網址；
    圖解四格與 `hero_label` 沒有任何數字；研究紀錄的 `title` 與內容包 zh-TW title 相同、
    `diagram.caption` 與 image caption 相同；兩個 JSON 都是 LF、2 格縮排、不跳脫非 ASCII、檔尾一個換行。

## 留給站主的 5 件事

1. **指派訊息要求本篇「含 8/11、8/18 兩則更新」，本輪把那一段移除了。** 原因是來源名額：
   `check_article.py` 硬性驗 `2 <= len(sources) <= 4`，四個名額已用在公告原文頁與三份撐起四個小節的
   開發者文件上，而那兩則各需要自己的網址。三個可選方案：(a) 維持現狀，本文只講 5/5 與機制；
   (b) 換掉一份開發者文件、放進 8/18 那則，代價是砍掉對應的小節；(c) 另開一篇以 8/11 或 8/18 為事件日的新聞。
   兩則的公告頁 2026-09-18 都可讀。**若寫回 8/18，繁中正文必須寫「8 月 19 日清晨（台北時間）」或註明 GMT。**
2. **`openai.com/index/*` 全站 403 這個前提要全批次複查。** BRIEF 與 `corrections-ai.md` 都把它當既定事實，
   AI 垂直另有三篇（`chatgpt-financial-services`、`chatgpt-storage-scale`、`openai-funding`）據此把
   `sources[0]` 指向 403 頁、正文改用 `web.archive.org` 封存。本輪實測該前提在 2026-09-18 不成立，
   建議協調者讓那三篇也重試一次自己的公告頁。
3. **zh-TW 段落字數是 2,993／3,000，幾乎沒有餘裕。** 要再補任何一句
   （例如 oCPC 的 403 例外、25,000 門檻與隱私區間機制）都得先換掉 `sources` 名額，
   而且要從別處刪等量的字——但不可以刪但書或限定詞來湊字數。
4. **`check_article.py` 仍是兩條 FAIL，都在規格允許的清單內、且查核前後完全相同**：
   AI 索引內容包尚未建立，兩個結尾連結的 `text` 都還是佔位字串，要等索引與相關文章由協調者處理。
   查核代理沒有動那兩個 link。
5. **翻譯階段注意**：`sources[0]` 的標題含英文原標題〈New ways to buy ChatGPT ads〉，
   各語系翻譯時 `url` 與 `checked_on` 不可變；正文裡「廣義平台分組」「有效點擊」「逐步開放」
   這三個限定語在每個語系都必須留著。

## 結論

`needs_second_round`：推翻的是骨幹前提（五處宣稱公告正文讀不到），`sources[0]` 已換成公告原文頁、
第一節整段重寫、另有 8 處事實修正與 3 段刪除，改動幅度超過一輪查核的安全範圍。
文章本身現在每一句都指得到四條 `sources` 之一，35 條引文全部通過連續字串比對，自檢回到查核前的兩條允許 FAIL。
第二輪請逐句重查第一節兩段與第三、四節被改寫的句子。

---

## 第二輪

第二輪代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 四處一致，未改）。
四條 `sources` 當天自己重抓：`curl -sL -A "Mokaair-editorial"`，去標籤後用 Python 對
**37 條 `verbatim_quote` 與另外 63 條正文主張**（合計 **100 條**）做連續字串比對。
所有請求都沒有帶入任何 email 或個人資料，也沒有猜任何網址。**改了 12 處。**

### 重抓結果（2026-09-18，第二輪自己抓）

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `openai.com/index/new-ways-to-buy-chatgpt-ads/` | 200 | 376,525 | 是。去標籤 6,960 字，含日期、四個小標與全部內文 |
| `developers.openai.com/ads/api-overview` | 200 | 378,465 | 是。四層表、Rate limits、**帶日期的 Changelog** |
| `developers.openai.com/ads/bidding-and-budgets` | 200 | 406,052 | 是。目標／計費表、Maximize Results、Campaign／Account Budgets |
| `developers.openai.com/ads/campaign-targeting` | 200 | 424,107 | 是。Inclusion & Exclusion、Geographic、Platform、Audiences、Context Hints |

第一輪「`openai.com/index/*` 並沒有被擋」的核心發現**成立**，公告頁第二輪一樣回 200 與完整正文
（bytes 與第一輪差 40，再次證明位元組數是活值）。`sources[0]` 的更換、第一節以公告正文重寫、
`sourcing_verdict` 升為 `full`——三件事逐句覆核後都站得住。

### 改掉的 12 處

1. **`verified_facts[0]` 的引文「OpenAI May 5, 2026」不是連續字串。** 頁面實際印出來的日期字串是
   `May 5, 2026`（`<p class="text-meta">`，RSC 酬載欄位 `publicationDateText`），「OpenAI」是相鄰的
   作者元素；兩者只有在**去標籤之後**才會黏成 `OpenAIMay 5, 2026`。引文已改成 `May 5, 2026`，
   `event_date_basis` 也改寫並說明黏字的成因。**事件日 2026-05-05 本身不受影響**，仍由公告頁自己印的日期撐住。
2. **第四節把 9/10 的網頁細分掛錯頁。** 原文是「不是全部可填的值——**同一份文件**的更新紀錄顯示，
   9 月 10 日又把網頁再細分成……」，而那一段從頭到尾講的是 `campaign-targeting`。
   實測：**帶日期的更新紀錄只長在 `api-overview` 這一頁**；`campaign-targeting` 與
   `bidding-and-budgets` 上出現的 `Changelog` 字樣是整站側邊導覽的連結（與 `Deprecations`、
   `Supported countries` 並列），不是那兩頁自己的更新紀錄。而且 `campaign-targeting` 全頁
   **沒有出現** `desktop_web`／`ios_web`／`android_web`，只列三個廣義分組。已改成「**文件總覽頁**的更新紀錄顯示」。
3. **「接下來要建 ChatGPT 廣告平台」→「正在打造」。** 第四節小標是 `Building the ChatGPT ad platform`
   （進行式），該節第一句是 `We’re still early in building advertising in ChatGPT`——OpenAI 說的是
   已經在做、還很早期，後面才接「隨時間繼續演進」的計畫。前一版把進行式寫成未來式。
4. **「文件寫的是除了預算與出價之外，還取決於……」→「除了預算與**帳戶花費上限**之外」。**
   原文 `Delivery also depends on the campaign schedule, resource statuses, reviews, targeting, and
   available inventory.` 的 `also`，接的是它前面那兩句
   （`Campaign budgets and ad account spend limits apply independently. Raising a campaign budget does
   not override an exhausted account spend limit.`），**那一段沒有提到出價**。同一句的
   「各層資源的狀態」也收回原文的 `resource statuses`＝「資源狀態」。
5. **FAQ 第 2 題「低於門檻會收到錯誤訊息並被告知差多少」→「並被告知需要的金額」。**
   原文是 `Requests below the applicable minimum return an error with **the required amount**`——
   回的是「需要的金額」，不是差額。而且正文第三節寫的是「告知需要多少」，**FAQ 與正文互相矛盾**。
6. **「出價與預算頁裡的美元金額**都**寫明是示範用途」是全稱，收回原句範圍。**
   原文 `**Budget and bid examples** use illustrative USD amounts.` 只講預算與出價的範例。
   正文與 FAQ 第 2 題都改成「出價與預算頁的**預算與出價範例**寫明是示範用途」。
   （第一輪已把「文件裡出現的金額」收到「出價與預算頁」，第二輪再收到原句真正的範圍。）
7. **摘要第 1 句與 FAQ 第 5 題的「不會把對話或個人資料交給廣告主」在正文找不到對應句。**
   正文第一節第二段只有量測那一節的「彙整過的成效資料、看不到個別對話」，沒有「個人資料」。
   這句的原文出處是**公告開頭的總述段**（`without sharing conversations or personal details with
   advertisers`），不在量測那一節。已在第一節第二段補上並歸因給公告，`summary` ⊆ 正文、FAQ ⊆ 正文恢復成立；
   研究紀錄也為它建了一條自己的 `verified_fact`。
8. **新增 `verified_fact`：`We’re still early in building advertising in ChatGPT`**，撐住第 3 點的改寫，
   並寫明不可以再寫成未來式。
9. **`illustrative` 那條 `verified_fact` 的 `fact` 文字**同樣帶著「頁面上的美元金額都」這個全稱，已收回並加註不可寫成全稱。
10. **更新紀錄那條 `verified_fact` 補上第 2 點的事實**：帶日期的 Changelog 只在 `api-overview`，
    另兩頁的 `Changelog` 是側邊導覽。
11. **門檻那條 `verified_fact` 補上翻譯提醒**：`the required amount` 是「需要的金額」，各語系不可寫成差額。
12. **為了騰字數，刪掉第二段裡「，不是一次全面上線」**——它是同一句內對「逐步開放給更多企業」的重複敘述，
    **限定語本身沒有刪**（全文仍有六處寫出逐步開放）。另把第五節第二段「要提醒的是，本文**所有**……
    OpenAI **自己的**公告與**自己的**文件」的重複字樣精簡（同段內容 callout 已完整寫過一次）。

### 指派訊息點名的六個疑點，逐條結果

1. **第一節重寫的兩段逐句回公告原文頁**：公告頁今天讀得到，兩段每一句都對得上——
   `We initially worked directly with a small group of advertisers…`、
   `Today, we’re beginning to roll out a beta self-serve Ads Manager…`、
   `Businesses can register as advertisers, add payment information, set budgets, bids and pacing…`、
   `We’re gradually opening Ads Manager to more businesses…`、`including` 與 `such as` 兩份夥伴名單、
   `In the first phase of the pilot…on a CPM…basis`、`Advertisers are only charged based on a click outcome.`、
   `We’ll continue to support CPM and CPC buying`、`We recently launched Conversions API and pixel-based
   measurement`、`Advertisers receive aggregated performance insights…without access to individual
   conversations.` 全部逐字命中。只有第 3 點（小標的時態）與第 7 點（個人資料）兩處要改。
   **全文逐詞掃過「摘要」「RSS」「feed」「讀不到」「擋」，各 0 次**——舊說法沒有殘留。
   事件日以公告頁自己印的 `May 5, 2026` 為準，沒有做時刻換算。
2. **8/11、8/18 兩則更新的殘留**：正文、摘要、FAQ、表格、圖解 `nodes`、`image alt`、`description`
   逐詞掃「8 月」「八月」「歐洲」「Europe」「2026 年 8」「1 月 16」「31」——除了 `ISO 3166-1` 裡的
   `31` 之外**全部 0 次**，沒有任何一句在講那兩則的內容或日期。
   文章裡剩下的後續日期只有兩個：更新紀錄區間「2026 年 6 月 3 日到 9 月 10 日」與第四節的「9 月 10 日」，
   **兩者都由 `sources[1]`（`api-overview`）的 Changelog 撐住**（`September 10th, 2026`、`June 3rd, 2026`
   逐字命中；第五節列的其餘項目 `September 9th`／`August 25th`／`June 3rd` 也都在同一份 Changelog）。
   第 2 點修掉的正是這裡唯一一處指錯頁的掛法。
3. **出價與預算**：兩句確實是分開的，正文與 FAQ 都已拆開——
   `Daily minimums depend on the account currency. Requests below the applicable minimum return an error
   with the required amount.`（**每日預算**，在 Campaign Budgets 的 Understand micros 之下）與
   `Bid limits and permitted monetary precision depend on the account currency **and campaign objective**.`
   （**出價**，在 Fixed Bids 的 Understand bid amounts 之下）。只有 FAQ 的「差多少」要改（第 5 點）。
   **轉換目標按有效點擊計費，本輪找到四處互證**（第一輪報告寫三處）：目標對照表 `conversions` 兩列的
   billing event 都是 `click`；`Conversion campaigns optimize for the selected action and bill for valid
   clicks.`；`Use billing_event_type: "click" for both Maximize Results strategies.`；
   `Both strategies use billing_event_type: "click".` 第一輪引的後面這一句**確實存在**（在 Maximize Results 一節），
   沒有引錯。`Delivery also depends on…` 沒有「同時都要滿足」的意思——正文第一輪已改對，第二輪只修了 `also` 的對象（第 4 點）。
4. **平台分組與鎖定**：`Use these **broad** platform groups:` 逐字命中，正文寫「三個『廣義平台分組』」
   並明講「不是全部可填的值」；`At creation, omitting platform targeting defaults to all platforms.` ✓。
   「排除優先」原文限定在 `an included **audience** and an excluded **audience**`，正文也只寫受眾，
   而且排在地區那一句**之前**，不會被讀成地區清單適用 ✓。
   2,500 那句的但書 `Account availability and campaign mode can impose additional restrictions.` 在正文與
   FAQ 第 4 題都在，也沒有「各自」的分法 ✓。
   `Geographic, platform, **and audience** settings work together` 三項——正文、FAQ 第 3 題一致，
   表格與圖解 `nodes` 不觸及這三項、沒有矛盾 ✓。
   （小節標題「鎖定條件：地區、平台與 Context Hints」沿用文件自己的頁面副標框架
   `Configure geographic, platform, and audience targeting and context hints`，**未改**；正文緊接著就寫明
   hints「不能取代地區、平台或受眾的明確鎖定」，不會被讀成 hints 是第三種鎖定。）
5. **地區**：`campaign-targeting` 全頁**沒有可投放地區清單**，只有
   `A code’s ISO validity does not mean it is available for advertising in your account; use supported
   advertising locations.` 與一個連出去的目錄連結。正文與 FAQ 第 4 題都只寫「本文查核的四條來源都沒有列出
   可以投放廣告的地區清單」——**既沒有推定台灣可投放或台灣使用者會看到廣告，也沒有寫成台灣不能投放** ✓。
   全文搜尋 `ads.openai.com`：**0 次**，第一輪下載過的地點代碼目錄一次都沒有被當成依據 ✓。
   另外實測：公告頁正文（`Taiwan`／`Europe`／`US`／`country`／`region`／`market` 各 0 次，只有
   `global brands` 這個形容規模的用法）確實沒有提到任何地區，FAQ 第 4 題「公告本身……沒有提到任何地區」成立。
6. **分批開放的四個狀態**：測試版（第二段、第一節、摘要、FAQ 1、callout、description）、
   逐步開放給更多企業（同上再加 FAQ 4）、`Spend-limit windows are available only to some accounts.`
   （第三節末）、`Added daily account spending limits for ad accounts **on postpaid invoice billing**.`
   （第五節）——四處逐一比對，用語一致、沒有互相打架。
   要注意兩個詞在來源裡本來就不同：受限的是**花費上限「期間」**（spend-limit window），
   不是帳戶花費上限本身；正文寫的是「花費上限**期間**」，表格沿用 `api-overview` 四層表的
   `spend limits` 不帶但書，**這不是漏但書，是兩件事** ✓。
7. **界線**：逐詞掃「投資」0 次、「值得」0 次、「划算」0 次、「應該」0 次；「建議」2 次都在否定句
   （「不提供任何採購建議」）。沒有投放教學、沒有行銷建議、沒有對使用者好壞的評價；
   廠商宣稱一律「公告說」「OpenAI 表示」「文件寫明」；`topics` 是 `ai`／`software`／`ai-news`，
   **不帶 `finance`**；`callout` 恰好一個，沒有免責段落 ✓。

### 覆核過、沒有動的部分

- **37 條 `verbatim_quote` 全部通過連續字串比對**（含 U+2019 彎引號、`×` 乘號與 `desktop_web, ios_web, and
  android_web` 這種第一輪修過的去標籤空格問題）。**沒有任何一條引文含 `...`／`…`／`|`**（逐條掃過，0 條），
  所以不存在省略號拼接的問題；三條跨句的長引文（目標對照表、活動預算與投放條件、受眾識別碼與檔案大小）
  逐片段檢查後**都是同一張表或同一段裡前後相連的文字**，不是把不同段落拼在一起。
- 四層架構四列、`chat_card`、640 × 640、`Creating an ad submits its creative for review.`、
  `A preview shows appearance; it does not confirm serving eligibility.`、
  `An account marked active may still have an outstanding review.`、
  「廣告活動／廣告組／廣告各自呼叫啟用」（`api-overview` 第 6 步確實是三個 `activate` 呼叫）、
  micros 換算、`fixed_bid` 可用每日或總預算、Maximize Results 只能用每日預算且不填出價金額、
  活動預算與帳戶花費上限各自獨立、`iPhone` 瀏覽器算 web 版位、`500,000,000 bytes`、
  `their supported SHA-256 variants`、context hints 三句——逐字回原文確認無誤。
- `25,000` 在正文、摘要、FAQ、表格、圖解裡仍然是 0 次；兩份官方頁強度不一致、承載但書的那頁沒有名額，
  **維持不寫是對的**（第一輪的判斷本輪覆核成立）。
- `checked_on` 2026-09-18 四處一致，**沒有因為第二輪重查而改**。
- 兩個結尾連結（索引與相關文章）**沒有動**。

### 留給站主的事（第一輪五件仍然有效，第二輪補兩件）

1. 第一輪的五件（8/11 與 8/18 的來源名額、`openai.com/index/*` 403 前提要全批次複查、字數餘裕、
   兩條允許 FAIL、翻譯注意事項）**全部維持**。其中第 3 件的數字更新為：zh-TW 段落字數現在是
   **2,996／3,000**，餘裕 4 個字。
2. **翻譯階段新增三個不可丟的限定語**：`the required amount`＝「需要的金額」（不是差額）、
   `Budget and bid examples`＝「預算與出價**範例**」（不是「頁面上的金額」）、
   第四節的更新紀錄要說是**總覽頁**的（不是鎖定設定頁的）。三件都已寫進研究紀錄對應的 `verified_facts`。
3. **第一輪報告裡一個字面小錯，本輪沒有回頭改報告正文**：上面「重抓結果」表寫公告頁「去標籤後 7,200 字」，
   第二輪自己的去標籤工具數到 6,960 字——這是工具差異，不是內容差異，兩輪讀到的正文相同。
   同理表中的 bytes 每次抓都會差幾十，`live_data_warnings` 已經記過這一點。

### 第二輪結論

`ok`。第一輪的 `needs_second_round` 到此解除：骨幹（公告原文頁可讀、`sources[0]` 換頁、第一節重寫）
逐句覆核後成立，另修 **12 處**，其中 5 處是事實或歸因錯誤（引文不連續、更新紀錄掛錯頁、進行式寫成未來式、
`also` 的對象、FAQ 的「差多少」），2 處是全稱收回與 `summary` ⊆ 正文，其餘是研究紀錄的補強與騰字數。
自檢輸出（原樣）：

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-chatgpt-financial-services-20260910
```

兩條都在規格允許的清單內（索引內容包尚未建立、兩個結尾連結的 `text` 仍是佔位字串，由協調者處理），
且查核前後完全相同。
