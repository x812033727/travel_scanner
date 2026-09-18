# 獨立查核：ai-news-chatgpt-sponsored-agents-20260916

查核代理：未參與撰稿。查核日 **2026-09-18**（與撰稿者記的 `checked_on` 同一天，因此
內容包三處、研究紀錄、第二段與表格 caption 的 `2026-09-18` **全部不動**）。
查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
逐頁去標記後做可見文字比對，每一條 `verbatim_quote` 都用程式做連續字串搜尋，
否定句一律用詞界比對重測。**沒有使用任何 `sources[]` 以外的新網址**，沒有用封存站，
也沒有猜任何識別碼；任何請求的 UA、標頭、查詢字串都沒有 email 或個人資料。

檢查的主張：約 **95** 條（正文 18 段的每一句、摘要 4 句、FAQ 6 題的答句、callout、
表格 24 格與 caption、圖解 caption 與四格節點、`hero_label`、title、description、兩個連結文字）。
**改了 22 處（歸為 14 組）**，另修研究紀錄本身 2 處，5 件留給站主。

批次 4.5 差異已套用：沒有 `corrections-ai.md` 段落，`corrections_applied` 維持 `[]`；
第一個連結文字與 DELTA-4-5 第 3 節的索引現行標題逐字相同，索引標題不改，
第二個連結指向既有已發布的 `ai-news-chatgpt-ads-20260505`，文字與該內容包 zh-TW `title` 逐字相同。
因此自檢**沒有留下任何 FAIL**，連規格允許的那兩條都沒有出現。

## 重抓結果（三條 sources 今天都拿到正文）

| source | HTTP | bytes | 最終落地 URL | body 是不是正文 |
| --- | --- | --- | --- | --- |
| `openai.com/index/reimagining-advertising-with-ai/` | 200 | 380,351 | 同 URL，無轉址 | 是：全文含 dateline「OpenAI September 16, 2026」、四個小節與全部引文 |
| `openai.com/index/testing-ads-in-chatgpt/` | 200 | 423,892 | 同 URL，無轉址 | 是：四段疊加更新＋2026-02-09 原始貼文全文 |
| `ads.openai.com/` | 200 | 201,646 | 同 URL，無轉址 | 是：三張信任卡、四個品牌、Newegg 引言、業務表單 |

BRIEF 記的 `openai.com/index/*` 403 今天沒有重現，撰稿者的觀察成立；bytes 與撰稿者記的
380,345／423,891／201,647 有 1–6 byte 漂移，屬已知漂移，**不可拿位元組數當版本識別**。
三頁的 `Taiwan`／`Taipei`／`台灣` 皆 **0 次**，`Agents API` **0 次**。

## 撰稿者點名要重查的三件事

**(a)「9 月 23 日起」的年份 —— 推算站得住，措辭我再收緊了一次。**
原句今天仍是 `The app will be available internationally in markets where ChatGPT Ads are available starting September 23.`，
確實**沒有印年份**。公告 dateline 是 2026-09-16，該日期在其後第七天，2026 是唯一合理讀法。
依 BRIEF 型態 9「要嘛照來源寫、要嘛明寫是編輯換算」，草稿原本寫「本文依…推算為」已屬誠實，
我把它改成明講**這是編輯的判讀而不是官方寫出來的**。**但表格那一格原本印「國際 9 月 23 日起」完全沒有年份**，
違反研究紀錄自己的 `must_not_write`，已補成「國際 2026 年 9 月 23 日起」。

**(b) 持續更新頁今天的狀態 —— 最新更新仍是 8/11，但草稿漏了一整段更新。**
頁面 dateline 今天讀到的是「OpenAI **August 11, 2026**」（dateline 跟著最新更新跑，不是原始貼文日），
其下依序疊著 **8/11 → 5/7 → 3/26 → Originally published on February 9, 2026**，共四段。
草稿把 3/26 寫成「再往前一次更新」，**中間的 5/7 整段被跳過**——那一段寫的是
`we plan to expand the ads pilot ... in the United Kingdom, Mexico, Brazil, Japan, and South Korea`，
是「計畫」，正好是 8/11 後來宣告已開放的那五個市場。已補進正文並標明是計畫。

**(c) 方案規則逐字核對 —— 兩個限定詞被刪掉了。**
原句是 `The test will be for logged-in adult users on the Free and Go subscription tiers. Plus, Pro, Business, Enterprise, and Education tiers will not have ads.`
草稿的正文有「登入的成年使用者」，但 **description、摘要第三句、FAQ 第三題三處都把它刪掉**，
寫成「廣告只出現在 Free 與 Go 方案」。而且這句話位在該頁 **2026-02-09 原始貼文**裡、主詞是 `The test`，
不是一條平台常規。同一頁還寫著 `If you prefer not to see ads, you can upgrade to our Plus or Pro plans,
or opt out of ads in the Free tier in exchange for fewer daily free messages.`——
**免費方案使用者可以關掉廣告**，所以「Free 就會看到廣告」本來就不是全貌。三處都已補回。

## 改掉的 22 處（依嚴重度）

1. **FAQ「台灣看得到這些廣告嗎？」把九個市場寫成一份現行清單**（最嚴重）。
   原文：「這份清單截至 2026 年 9 月 18 日寫的是美國，以及英國、墨西哥、巴西、日本、南韓、加拿大、澳洲、紐西蘭。」
   頁面沒有任何一份九市場清單：只有 8/11 更新用 `has now launched` 點名英、墨、巴、日、韓五個；
   加、澳、紐**只出現在 3/26 更新的未來式**，而且用的字是 `pilots`，查到今天沒有任何後續更新回報結果。
   這同時是 BRIEF 型態 3（放大範圍）與型態 11（預告寫成已上市），而且**和文章自己的正文互相矛盾**。
   已改寫成兩組分開、各帶更新日期。
2. **正文第 3 節把 3/26 稱作「再往前一次更新」**——中間還有 5/7。已補上並標為「計畫」。
3. **方案規則的兩個限定詞**（description、摘要第三句、FAQ 第三題共三處）。已補「登入的成年使用者」，
   標明出自該頁 2/9 原始貼文且講的是這次測試，並把兩條不看廣告的路（升級 Plus/Pro、
   或留在免費方案用每日訊息則數換取關掉廣告）寫進正文與 FAQ。
4. **「廣告主看得到多少內容，三個頁面也都沒有說明」是假的否定句**。同一份說明頁寫著
   `Advertisers do not have access to your chats, chat history, memories, or personal details.
   Advertisers only receive aggregate information about how their ads perform such as number of views or clicks.`
   已把這段寫進正文，並把真正的缺口說清楚：那段話是針對廣告整體寫的，沒有特別提到贊助對話。
5. **「廣告主要怎麼申請加入…都沒有交代」範圍過寬**——`ads.openai.com` 有 Sign up／Start now 與業務表單。
   已收斂成「怎麼加入**這項測試**」。
6. **第 4 節「不是廣告主自己確認過的原文」把「來源沒說」寫成「來源說沒有」**。官方只對 Ads Manager 的
   **創意建議**寫了廣告主可審閱（`they can review and edit suggestions`），對文字客製化什麼都沒寫。
   已改成「廣告主能不能事先看到或審核這些改寫與翻譯，公告沒有寫」。
7. **FAQ 第四題張冠李戴**：問的是「點開贊助對話之後，看到的文字…」，答的卻是 AI 文字客製化，
   而那項功能改的是 `headlines and descriptions`（廣告本身），不是代理人的回話。
   問句已改成「廣告上的文字…」，並把「代理人講的話怎麼產生的，公告沒交代」另外寫成一句。
8. **「原文用的動詞是『testing』，不是『launching』」不成立**：同一頁就有
   `We're also launching the ability to opt into AI-powered text customization.` 與 `Together, these launches reflect...`。
   已收斂成「官方描述**這件事**用的動詞是 testing」。
9. **「同一句話也寫明」歸錯句子**：美國／特定廣告主的限制在該節**最後一句**，不是定義那一句。已改。
10. **兩個沒有來源的「第一次」**：「第一次讓廣告在 ChatGPT 裡變成可以打開來對話的東西」官方完全沒這樣說，已刪；
    「OpenAI 並第一次把廣告接上 HubSpot 與 Shopify」官方的說法窄得多（`our first CRM partner` /
    `our first ecommerce partner`），已改成歸因給官方的分類第一。
11. **ChatGPT Work 與 Ads Manager 外掛被併成一句**（第一段與第 1 節第三段兩處）。官方的
    建立／修改／分析那一句寫的是 `directly in ChatGPT with the Ads Manager plugin`；
    ChatGPT Work 只出現在開頭摘要那一句，而且只講 `create ads`。兩句已分開照官方寫法寫。
12. **表格三項修正**：Shopify 那格補上年份；「AI 創意與文字客製化」原本把條件不同的兩項
    （廣告主可審閱 vs 廣告主選擇開啟）併成一列，已拆成兩列（共 6 列，仍在 3–6 內）；
    三格「已上線」高於官方的 `rolling out`，改成「官方寫正在推出」，HubSpot／Shopify 兩列
    依 `Starting today`／`Also available today` 改成「公告當天起」。
13. **「要自己審核修改過才能決定」把 can 寫成 must**。原文是 `they can review and edit suggestions
    before choosing whether to add them`。已改回「可以先審閱、修改，再決定」。
14. **callout 帶了投資免責**（「也不是投資建議」）。`ai.md` 把這種措辭保留給金融服務那一篇、
    其餘 AI 篇不得自行加投資免責，已刪。同一段還把市場清單掛在廣告主介紹頁（清單在測試說明頁上），
    已改正並補上「那是一頁會持續疊加更新的頁面」。
15. **零碎修正**：「沒有出現『台灣』兩個字」（三頁是英文頁）→「沒有提到台灣」；
    「把四項改動和兩個整合放在一起看」重複計算（整合本來就是四項裡的第四項）；
    「品牌贊助的代理人」→「企業贊助」（`business-sponsored`）；Shopify「加裝」→「使用」；
    第 1 節標題「廣告可以對話了」→「可以打開來對話的廣告」，避免標題暗示測試已對讀者開放；
    第 2 節標題的「四項改動」隨表格一起改為「這次的改動」；
    FAQ 第五題補上說明頁自己那句「廣告不會影響 ChatGPT 給你的答案」。

## 研究紀錄本身的兩處修正

- **`verified_facts` 有一條 `verbatim_quote` 是拼接的**（BRIEF 型態 1）：
  `Clearly labeled Ads are clearly identified in the experience. Separate from answers ...`
  把 `ads.openai.com` 上**三張各自獨立的卡片**（各一個 h3 加一行）串成一句。
  已拆成三條、每條的引文都是單一 `<p>` 裡原樣搜尋得到的連續字串。
- **`unverified_or_excluded` 寫「Agents API 或 Apps SDK 在三頁都沒出現」**——`Agents API` 確實 0 次，
  但 `Apps SDK` 在兩個 `openai.com/index` 頁**各出現 1 次**（站台頁尾導覽，不是正文）。
  已改寫成精確的敘述；文章的 FAQ 只宣稱沒提到 Agents API，那句成立。

另外補進研究紀錄的新事實六條（5/7 更新、免費方案關廣告、廣告主看得到什麼、
`rolling out` 的狀態字、ChatGPT Work 那一句、first CRM／ecommerce partner 的正確範圍），
並在 `live_data_warnings` 記下這一頁的 dateline 會跟著最新更新跑、以及方案規則出自 2/9 原始貼文。

## 查過而且正確的部分（沒有動）

- **27 條 `verbatim_quote` 今天全部在頁面上重新找到**（含我新增的六條）。只有一條
  （`Throughout this work, our ads principles remain unchanged...`）在原始 HTML 裡被
  `ads principles` 上的 `<a>` 切開，但它是單一可見句子，Ctrl-F 搜尋得到，保留。
- **事件日與三處一致**：公告 dateline「OpenAI September 16, 2026」、slug 尾碼、`news_date`、
  正文第一句全部是 2026-09-16；台北時間換算不改變日期。
- **Sponsored Agents 三個限制**（測試、特定廣告主、美國）與**兩條分離**
  （與 ChatGPT 自己的答案分開、與原本對話分開）逐字對得上。
- **台灣的寫法正確**：三頁 0 次命中、沒有排除清單，文章寫的是「不在官方列出的開放市場裡」
  並明說這不等於官方說不會開放——`must_not_write` 那一條守住了。
- **Go 方案沒有定義**：詞界比對只有三個 `Go`，兩個是方案名、一個是 `ads.openai.com` 的動詞
  （`Go beyond keywords`），文章「頁面沒有另外說明 Go 是什麼樣的方案」成立。
- **四個品牌處理正確**：列為被點名的參與者，並寫明該頁在「Results from early advertisers」標題下
  沒有給任何一個品牌的數字。
- **3 月那句成效說法已歸因**給 OpenAI，並寫明沒有測量方法、樣本數與期間。
- **界線**：沒有購買或升級建議、沒有推薦式比價、沒有未歸因的廠商宣稱、
  沒有把預告／測試／分批開放寫成已上市、沒有實測語氣、沒有多出來的免責 callout、
  沒有把 Sponsored Agents 連到 Agents API、沒有重寫 5 月那篇的四層架構與出價機制。
- **圖解**：四格節點與 `hero_label` 沒有任何數字，caption 與內容包一致，沒有商標或介面。

## 留給站主的事

1. **`testing-ads-in-chatgpt` 是活頁，整個市場那一節都壓在它身上。** 發布當天要再讀一次：
   只要 8/11 上面多出一段新更新，正文的更新堆疊、FAQ 第二題與「2026 年 8 月 11 日」要一起改。
2. **台灣今天確實不在清單上，但這是最可能在發布前就過期的一件事。**
3. **zh-TW 段落字數 2,979／上限 3,000。** 後面任何一句加字都要有等量刪減，
   而依 BRIEF 刪的不可以是但書或限定詞。
4. **表格現在 6 列**（仍在 3–6 內），但 Shopify 的「美國；國際 2026 年 9 月 23 日起」是全表最長的一格，
   手機上請實際看一眼。
5. **「9 月 23 日」的年份是編輯判讀**，正文已明寫。若站主希望完全不印推得出來的年份，
   可以把表格那一格改成「美國（國際待開放）」、只在正文交代——這是取捨，不是錯誤。

## 結論

`needs_owner`。事實層面已經修好並通過自檢，但市場清單與台灣是否被列入都掛在一頁會變的官方頁上，
發布當天必須再讀一次那一頁再決定是否調整第 3 節與 FAQ 第二題。

自檢輸出：

```
OK ai-news-chatgpt-sponsored-agents-20260916 zh-TW paragraphs 2979
```

## 第二輪

第二輪查核代理：沒有參與撰稿，也沒有參與第一輪。查核日 **2026-09-18**（重抓落在撰稿者與第一輪
記的同一天，因此 `checked_on` 與內容包、研究紀錄、第二段、表格 caption 的四處 **全部不動**）。
範圍依 `agents/ai/SECOND-ROUND.md`：第一輪**改動過的每一段**與**新寫進去的每一句**逐句回來源，
不是整篇重做。共覆核 **約 80 條**主張，**再改 3 處**，另修研究紀錄 2 處。
任何請求的 UA、標頭、查詢字串、表單都沒有 email 或個人資料；沒有使用 `sources[]` 以外的網址，沒有封存站。

### 重抓結果（三條今天再次都拿到正文）

| source | HTTP | bytes | 最終落地 URL | body 是不是正文 |
| --- | --- | --- | --- | --- |
| `openai.com/index/reimagining-advertising-with-ai/` | 200 | 380,349 | 同 URL，無轉址 | 是：dateline「OpenAI September 16, 2026」、四個小節與全部引文 |
| `openai.com/index/testing-ads-in-chatgpt/` | 200 | 423,900 | 同 URL，無轉址 | 是：四段疊加更新＋2026-02-09 原始貼文全文 |
| `ads.openai.com/` | 200 | 201,377 | 同 URL，無轉址 | 是：三張信任卡、四個品牌、Newegg 引言、業務表單 |

bytes 與第一輪記的 380,351／423,892／201,646 又各漂移了數百位元組（`ads.openai.com` 最多，−269），
再次印證第一輪的結論：**位元組數不能當版本識別**。三頁 `Taiwan`／`Taipei`／`台灣` 仍是 0 次。

### 引文的連續字串比對（程式跑，27 條全過）

把三頁去標記後取可見文字，對 `verified_facts` 的 **27 條 `verbatim_quote` 逐條做連續子字串搜尋**
（彎引號兩邊都正規化再比一次）：**27 條全部在可見文字裡命中**，沒有一條只在原始 HTML 裡才找得到，
也沒有任何一條含 `...`、`…` 或 `|`。第一輪把 `ads.openai.com` 三張卡片拆成三條獨立引文的修正**站得住**。

### 再改的 3 處

1. **`description` 仍把方案規則寫成平台常規**（最重）。
   原文：「…查核這項功能只在美國與特定廣告主之間測試、**廣告只對 Free 與 Go 方案的登入成年使用者顯示**，且…」
   → 改成「…、**廣告測試只對 Free 與 Go 方案的登入成年使用者顯示**，且…」。
   來源原文是 `The test will be for logged-in adult users on the Free and Go subscription tiers.`——
   **主詞是 `The test`**，而且整句位在該頁 2026-02-09 的原始貼文裡。
   第一輪把「登入的成年使用者」補回了三處，但**只有正文與 FAQ 第三題標了「這次測試」**，
   description 與摘要留成了無條件的敘述。description 改後 **199／上限 200**。
2. **摘要第三句同一個缺口**。「官方說明頁**寫的是**：…」→「官方說明頁**針對這次廣告測試**寫的是：…」。
   這樣摘要才真的 ⊆ 正文那句「講的是這次測試的範圍」。
3. **表格 Shopify 的「地區」格把條件寫掉了**。原文「美國；**國際** 2026 年 9 月 23 日起」
   → 改成「美國；**支援廣告的市場** 2026 年 9 月 23 日起」。
   來源是 `The app will be available internationally **in markets where ChatGPT Ads are available** starting September 23.`
   光寫「國際」等於把它讀成全球同步，這既違反研究紀錄自己的 `must_not_write`，
   對本文的台灣讀者更是**反向誤導**——台灣正好不是「已支援廣告的市場」，
   而正文兩段前才剛寫明這一點。改後用的是正文自己的措辭，年份依 `must_not_write` 保留。

三處都落在 description、摘要與表格，**都不計入段落字數**，所以段落維持 **2,979／3,000**，
沒有為了騰字刪掉任何但書、限定詞或歸因，也不需要刪。

### 指派訊息點名的七件事，逐條結果

- **(a) 市場清單三處一致**：正文第 3 節與 FAQ 第二題都把「8/11 已開放的五個」與「3/26 未來式 `pilots` 的三個」
  分開並各帶更新日期；表格根本沒有市場清單，不存在第三份說法。兩處都沒有把台灣寫成「確定不在」，
  寫的都是「截至查核日不在官方列出的清單上」，並保留官方「會繼續擴大」那句。**通過。**
- **(b) 更新堆疊順序**：今天重讀，dateline 是 `OpenAI August 11, 2026`，其下正好四塊，
  8/11（`has now launched` 五個市場）→ 5/7（`we plan to expand the ads pilot` 同樣五個）
  → 3/26（`we'll begin expanding beyond the U.S., starting with pilots in Canada, Australia, and New Zealand`）
  → `Originally published on February 9, 2026`（美國開始測試）。
  正文每個日期配的內容**逐段核對，沒有錯位**，5/7 與 3/26 都標了是計畫。**通過。**
- **(c) 方案規則三處措辭**：正文與 FAQ 第三題已標明是測試階段的規則，**description 與摘要沒有**——
  就是上面改掉的第 1、2 處。**原本不通過，已修。**
- **(d) 9/23 的年份**：來源句今天仍然沒有印年份。正文明寫「這是編輯的判讀而不是官方寫出來的」，
  並保留「支援 ChatGPT 廣告的市場」這個條件。表格那格原本的問題不是年份而是「國際」，已改。
  **全篇沒有把它寫成官方日期**（唯一殘留：表格印了推得出來的年份、caption 又寫「整理自…公告」，
  但 `must_not_write` 要求印日期就要印年份，正文的說明優先，維持原樣）。
- **(e) 廣告主看得到多少內容**：改寫後那句逐字對上 `testing-ads` 的
  `Advertisers do not have access to your chats, chat history, memories, or personal details.
  Advertisers only receive aggregate information about how their ads perform such as number of views or clicks.`
  另外把 `ads.openai.com` 三張信任卡**一張一張**對過：`Clearly labeled`／`Separate from answers`／`Choice and control`
  三句都逐字對得上，正文第 2 節與 FAQ 第五題也都寫明那是整個廣告系統的原則、不是 Sponsored Agents 的承諾。**通過。**
- **(f) 字數**：段落 2,979 未動，三處修改都不計入；沒有刪但書。**通過。**
- **(g) callout 沒有別篇的制式句**：整份 zh-TW 文件掃過
  「投資／免責／理財／財務／不構成／僅供參考／值得／划算／推薦／實測／保證／唯一／首次／從未」——**全部 0 次**。
  唯一的「第一」是已歸因的「官方稱這兩家是自己的第一個 CRM 夥伴與電商夥伴」。**通過。**

### 第二個結尾連結

`ai-news-chatgpt-ads-20260505` 的內容包存在，zh-TW `title` 是
「ChatGPT 廣告開放自助購買：OpenAI 5 月公告的工具、計費與鎖定機制」，與本文連結文字**逐字相同**。
那一篇全文讀過：它寫的是 5 月的自助購買、四層帳戶架構、CPM／CPC 計費、出價策略與地區／平台／context hints 鎖定。
本文第 1 節末與 callout 都只**指過去**、沒有重寫，兩篇**沒有矛盾**；
台灣這件事兩篇也都拒絕斷言（那篇是「來源沒有列出可投放地區清單」，本文是「不在已開放市場清單上」），角度不同但不打架。

### 查過而且正確、沒有動的部分

- **`Sponsored Agents are now being tested with select advertisers in the United States.` 確實是
  「Being part of the AI conversation」那一節的最後一句**——第一輪的第 9 處修正經得起覆核。
- **ChatGPT Work 與 Ads Manager 外掛兩句仍然分開**：`create ads ... in ChatGPT Work` 對開頭摘要，
  `create, update, and analyze campaigns directly in ChatGPT with the Ads Manager plugin` 對內文，沒有再被併回去。
- **`can review and edit` 仍寫成「可以」不是「必須」**；`opt into`／「選擇加入」仍在。
- **否定句全部重測**：`Agents API` 0 次（FAQ 第六題成立）、`Apps SDK` 只在兩頁站台頁尾各 1 次、
  `Go` 全詞比對整整 3 次（兩個方案名、一個 `Go beyond keywords` 的動詞，與研究紀錄記的一致）、
  `train`／`retain`／`retention` 0 次（「會不會拿去訓練、保留多久沒說明」成立）、
  `price`／`pricing`／`CPC`／`CPM`／`$` 0 次（「價格完全沒有出現」成立）。
- **界線**：沒有購買、升級或投放建議，沒有推薦式比價，沒有未歸因的廠商宣稱，
  沒有把測試／計畫／分批開放寫成已上市，沒有實測語氣，一個 callout、沒有 `finance` 主題、沒有投資免責。

### 留給站主的事（第一輪四條仍然成立，另補三條）

1. 第一輪的第 1、2 條**原封不動最重要**：`testing-ads-in-chatgpt` 是活頁，發布當天要再讀一次；
   只要 8/11 上面多一段更新，正文第 3 節、FAQ 第二題與「2026 年 8 月 11 日」要一起改。台灣這件事最可能先過期。
2. 第一輪第 3 條的字數提醒仍然有效（2,979／3,000），第 4 條的手機視覺提醒現在更要看一眼：
   Shopify 的地區格從「美國；國際 2026 年 9 月 23 日起」變長成「美國；支援廣告的市場 2026 年 9 月 23 日起」。
   表格本身沒有單格長度規則（自檢只管欄數與列數），但它仍是全表最長的一格。
3. **圖解第三格把方案規則壓成「免費與 Go 才會看到」**，沒有「登入的成年使用者」也沒有測試框架，
   因為節點說明上限 15 個字。正文、FAQ、description 與摘要都帶了完整規則，所以這是壓縮不是錯，
   但那是全篇唯一裸寫這條規則的地方——若站主想改，得同時改研究紀錄的 `diagram.nodes` 與內容包的圖說 alt。
4. **表格三格都寫「官方寫正在推出」**。前兩項確實是官方的 `rolling out`，
   但「AI 文字客製化」那一項官方自己的動詞是 `launching`（`We're also launching the ability to opt into...`）。
   「推出」兩個英文動詞都蓋得住，而且方向是**低報不是高報**，所以沒有改；
   只是別把 `rolling out` 當成官方對那一列用的字（已寫進研究紀錄該條 `fact`）。
5. **表格 caption 寫「整理自…公告與廣告測試說明頁」，但六列其實全部來自 9/16 公告**。
   無害，而且那串 caption 和圖解共用（圖解確實兩頁都用到），要改就得連研究紀錄的 `diagram.caption` 一起改，
   否則自檢的 caption 比對會紅。判斷是不值得動。

### 結論

`needs_owner`。第二輪再修的三處都不是骨幹（description／摘要的測試範圍、表格一格的地區條件），
事實層面現在站得住、自檢乾淨；但**市場清單與台灣是否被列入仍然壓在一頁會變的官方頁上**，
發布當天必須重讀 `testing-ads-in-chatgpt` 再決定第 3 節與 FAQ 第二題要不要動。

自檢輸出（第二輪改完後，原樣）：

```
OK ai-news-chatgpt-sponsored-agents-20260916 zh-TW paragraphs 2979
```
