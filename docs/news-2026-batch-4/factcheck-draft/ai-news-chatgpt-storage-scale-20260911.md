# 獨立查核：ai-news-chatgpt-storage-scale-20260911

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 本來就是 2026-09-18、
六處一致，且確實是撰稿者與本代理都讀到來源的那一天，**不改**）。
查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
逐句把正文、摘要、FAQ、callout、表格每一格、caption、title、description 對回原文；
否定結論一律用**詞界**比對；研究紀錄 27 條 `verbatim_quote` 用程式做連續字串比對。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。

檢查的主張：**87 條**（正文 45 句／子句、摘要 4 句、FAQ 5 題答句、callout 3 項、
表格 21 格、表格與圖解 caption 各 1、圖解 4 組節點、`hero_label`、title、description），
外加研究紀錄 27 條引文。**改了 20 條（24 個編輯點）**，另有 4 件留給站主。

## 重抓結果：三條 sources 今天都讀到正文，不是擋阻頁

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `openai.com/index/scaling-storage-one-billion-users-part-one/` | 200 | 550,689 | **是**。`<title>` 為「Rapidly scaling online storage to serve over 1 billion ChatGPT users \| OpenAI」，十節全文、Figure 01–05、byline、三個統計方塊、頁尾「Keep reading」都在；`Request Access`／`Access Denied`／`http-equiv="refresh"` 各 **0** 次 |
| `openai.com/news/rss.xml` | 200 | 736,773 | **是**。本篇 `<item>` 的 `pubDate` 為 `Fri, 11 Sep 2026 10:00:00 GMT`、`category` 為 `Engineering`、`<link>` 不帶尾斜線 |
| `openai.com/sitemap.xml/engineering/` | 200 | 192,116 | **是**。22 個 `<url>`：20 篇文章 ＋ `/news/` 與 `/news/engineering/` 兩個清單頁；查無 `part-two` 的 `<loc>` |

**協調者交辦的重抓確認**：文章頁今天（2026-09-18）確實讀得到**正文**。
撰稿者同日記的是 550,655 bytes，本代理量到 550,689——頁面帶隨機產生的元素 id，
逐次有幾十位元組的漂移，**不可拿位元組數當版本識別**，內容逐句相同。
`10:00:00 GMT` 換算台北時間是同日 18:00，**不跨日**，`news_date` 2026-09-11 成立。

**關於 `<lastmod>` 的推論**：本代理今天讀到的值與撰稿者相同（`2026-09-17T21:51:03.895Z`），
所以「兩次查核之間變了兩次」是撰稿者跨日的觀察，本輪無法自己重現。
**但同一件事今天有更硬的證據、而且全在 `sources[]` 裡**：這份地圖給
`jalapeno-first-results`、`continuous-voice-interaction-with-gpt-live`、
`gpt-5-6-frontier-intelligence-efficiency` 的 `lastmod` 是 2026-09-17 與 2026-09-15，
而文章頁自己的「Keep reading」區塊把這三篇印成 **Aug 25 2026、Aug 3 2026、Jul 29 2026**。
同一批來源裡就互相推翻，`lastmod` 不是發布日也不是更新日。
草稿原本沒把這個推論寫進正文，卻在 FAQ 第 5 題寫成「每篇文章都附有各自的更新時間」——
那句已改掉；正文第 5 節新加的一句**明寫是本文的觀察**（見下面第 17、18 條）。

## 改掉的 20 條

### 協調者點名的三段

1. **連線池那段的名詞張冠李戴（最重的一處）。**
   原文：「`Further investigation found that Python's aiohttp TCPConnector defaults to LIFO
   connection reuse…` **`In this case, it created a metastable failure for us.`**」，
   前一句還寫「`This was a class of failures some of our teammates were well-acquainted with
   from prior work: metastable failure.`」
   而 `known as a “thundering herd”` 出現在**另一個小節**
   （`Avoiding flooding downstream resources`）：
   「`One side effect of tuning for low asyncio delay and having so many Python processes is
   that it becomes very easy to overwhelm downstream dependencies with the vast number of
   connections (known as a “thundering herd”).`」
   草稿把 LIFO 連線池的回饋循環稱為「OpenAI 稱之為一種『驚群效應』」，
   **是把兩個不同小節、不同現象的歸屬接在一起**（跨篇通則第 12 條）。
   已改成「OpenAI 稱這是一種『亞穩態故障』（metastable failure）」，
   並在研究紀錄拆成兩條事實、各自掛自己的原句，另加一條 `must_not_write` 擋住翻譯階段再犯。
2. **同一段的因果被改寫過。** 原文是
   「`During a burst of requests, requests to slower overloaded servers returned connections to
   the pool later and were therefore selected more frequently by subsequent requests, gradually
   concentrating more traffic on the pods already struggling.`」
   草稿寫成「這個機制會讓愈來愈多流量集中到原本已經吃緊的**處理程序**上，形成惡性循環」——
   機制（較慢的伺服器**比較晚把連線還回池子**、因此更常被選中）整個不見了，
   而且原文那一句寫的是 **pods**，不是 processes。已照原文改寫，
   並補上 metastable failure 的具體現象（`despite stopping the client that was overloading part
   of our service, a subset of processes remained degraded well past the bursty traffic`、
   `receiving increasingly more requests until we restarted them`）。
3. **`steady state` 被刪掉。** 原文 `even reduced our steady state request variance as well`，
   草稿只寫「連請求量波動也跟著變小」。已補回「連**穩態下**的請求量落差也跟著變小」。
4. **Statsig 那段把 `all` 寫成「幾乎所有」，又漏掉「某個瞬間」。** 原文是
   「`this meant that every minute each pod would have some moment where all of its workers
   stalled processing in-flight requests…`」
   草稿寫「變成每分鐘**幾乎所有處理程序**都會停下手上的請求」。
   已改成「每分鐘**每個 Pod 都會有某個瞬間**，所有工作處理程序同時停下手上的請求」。
   （研究紀錄第 12 條原本也是「幾乎所有處理程序」，同步改，並把 `verbatim_quote`
   從 `up to 8 Python processes per pod` 換成這一句完整的原句。）
5. **A/B 測試被寫成 OpenAI 在做的事。** 原文是
   `Statsig (a tool that manages feature flags, and can be used to run A/B tests and more)`。
   草稿寫「Habitat 用 Statsig 這套工具管理功能開關**與 A/B 測試**」，
   把「這個工具**可以**用來做」寫成「他們用它做」。已改成「Statsig 這套功能開關工具」。
6. **同一段另外三個限定詞。** `By default`（草稿寫「原本設定成」→改「預設」）、
   `every production rule across every service`（草稿寫「所有服務的規則」，漏掉
   **正式環境**與「每個服務的**每一條**」→已補）、
   `add some jitter to background tasks **like these**`（草稿寫「背景工作」→改「**這類**背景工作」）。
7. **`main challenge` 被升級成「最大的挑戰」。** 原文
   `We've found the main challenge in running a Python service at this scale is in managing
   these tail latencies.`。已改成「主要挑戰」，同段的
   `When the average user request results in hundreds of database calls` 也改回條件句式。

### 「超過 10 億」到底是哪一種：標題、摘要、正文、FAQ 一致化

8. **OpenAI 自己在同一個頁面上有四種寫法，草稿只採了一種、還自己加了推論。**
   今天抓下的 HTML 逐一確認：
   - 可見標題、`og:title`、`twitter:title`：`over 1 billion ChatGPT users`
   - 文末 part II 那一句：`to serve over 1 billion ChatGPT users`
   - **正文的規模句**：`supporting products used by over 1 billion people each week`
     （主詞是 **products**，單位是**每週的人數**，不是 ChatGPT 帳號）
   - `meta description`／`og:description`／`twitter:description`：
     `serving 1 billion ChatGPT users and 22M requests per second`
   - `og:image:alt`／`twitter:image:alt`：`nearly 1 billion ChatGPT users`
   草稿的 FAQ 第 2 題把正文那句解釋成「指的是 OpenAI **全部產品加總**、以週為單位的使用人數」——
   `全部` 與 `加總` **原文都沒有**，而且「加總」在語意上還會變成重複計算。
   FAQ 第 2 題已整題重寫成把四種寫法並列、說明 OpenAI 沒有交代彼此關係、也沒有說哪些產品計入。
9. **FAQ 第 2 題的問句引用了一個不存在的標題。** 原問句是
   「**文章標題寫「超過 10 億使用者」**，這是什麼意思？」，但本文標題從來沒有這句話。
   已改成「「超過 10 億」到底是哪一種使用者？」。
10. **title 掉了 `over`。** 原標題「支撐**每週十億使用者**背後的規模與極限」，
    原文是 `over 1 billion people each week`——掉了「超過」就比來源強，`people` 也不是「使用者」。
    已改成「**每週逾十億人使用**背後的規模與極限」，研究紀錄的 `title` 同步改。
11. **表格四格掉了限定詞。** 原文都是 `more than`／`70M+`／`500 PB+`，
    儲存格卻寫成「7000 萬/秒」「2000 萬/秒」「500 PB+」「10 倍」。
    已改成「逾 7000 萬/秒」「逾 2000 萬/秒」「逾 500 PB」「逾 10 倍」。
    摘要第 2 句的「這套系統過去 3 年」也改成「過去 3 年**他們**」（原文主詞是 `we`，不是 Habitat）。

### 其餘（都在「安靜強化來源」與「全稱」兩類）

12. **兩處「唯一」不成立，而且草稿自己就有反例。**
    第 4 節寫「文中**唯一**出現的地區相關字串，是示意圖上代表資料庫節點的範例標籤」，
    FAQ 第 3 題寫「文章裡**唯一**看得到的地區相關文字……」。
    但文末職缺連結的網址就是
    `openai.com/careers/software-engineer-habitat-(online-data)-seattle/`，
    草稿自己在第 1 節寫了「**西雅圖的**工程職缺連結」——同一篇文章自相矛盾。
    （另：頁尾語系切換器上還印著 `United States`。）
    兩處「唯一」都已拿掉，改成「比較接近地區資訊的，是示意圖上那三個資料庫代號，
    以及職缺連結網址裡的城市名」。
13. **`us0`／`us1`／`eu0` 被讀成「美國兩區、歐洲一區」。** 那是本文的推論，原文沒有寫，
    而且研究紀錄自己的 `unverified_or_excluded` 第 4 條明寫「不把示意標籤當地區清單使用」——
    正文卻用了。同句還寫「並**註明**那是示意用的標籤」，OpenAI 沒有註明；
    圖上自陳為簡化的是那張圖（`Simplified Habitat request flow`）。
    已改成「只在一張自陳為『簡化』的示意圖上，出現 us0、us1、eu0 三個範例資料庫代號」。
14. **跨地區 Cosmos DB 遷移被寫成已完成。** 原文是
    `we wanted to reduce the blast radius of any single region outage for our most critical data
    sets by migrating them to a set of regionally distributed Azure Cosmos DB accounts`，
    而那段故事的結尾是**旗標還沒啟用就出了事故**。
    草稿寫「OpenAI **提到把**部分關鍵資料**放進**跨地區分散的 Azure Cosmos DB 帳戶」。
    已改成「只描述過一次**想**把最關鍵的資料集移到……的**經過**」。
15. **「誤回滾」是草稿加的判斷。** 原文是
    `only for one of the teams to roll back their service for unrelated reasons to a previously
    buggy client, causing the outage we had worked so hard to avoid`——是**不相干的原因**，
    不是失誤。已照原文改寫，同段「幾次**自己造成的**事故」也改成「幾次自家系統出過的狀況」。
16. **否定句補上查法。** 「文章通篇沒有提到『耐用性』『備份』或『資料復原』」
    改成「本文以英文原詞逐字比對，文章沒有出現 durability、backup、replica 這幾個字」。
    （查核結果見下一節。另把全篇「耐用性」統一成研究紀錄用的「耐久性」。）
17. **FAQ 第 5 題把 sitemap 的時間戳說成「更新時間」。** 已刪掉，改成明寫
    「網站地圖上標的時間是網站端的時間戳，不能當成文章的發布日或更新日」。
18. **第 5 節對 feed 行為的推定。** 「兩者都會在有新文章發布時更新」是對 OpenAI 系統的推定，
    已改寫成本文實際做了什麼；並依協調者指示，把「那是網站端時間戳」這個推論
    **明寫成「這是本文的觀察」**。
19. **「反覆強調」與漏掉的三種對象。** 原文
    `Habitat plays a critical role in protecting user data and preventing unauthorized access
    from external, internal, and agent actors` 只出現一次，不是「反覆強調」；
    已改成「只說」，並補上 `external, internal, and agent actors`。
20. **五個小修**：`If those requests are slow` 是複數，「一次查詢變慢」改「這些查詢一慢」；
    統計方塊上印的只有 `1B+ / people each week`，草稿寫「每週超過 10 億人**使用旗下產品**」，
    已把那四個字拿掉（旗下產品那句留在正文規模句，那裡原文才有）；
    `If you want to work on OLTP systems… check out this open role` 是條件句，
    「邀請讀者加入團隊」改成「歡迎有興趣的人自己去看」；
    `95% of our production requests` 的「正式流量」改「正式環境請求」，
    並補上 `Our data shows` 的歸屬（「OpenAI 說自家數據顯示」）；
    第 2 段「文中的情境舉例都會另外標明是編輯設計的例子」——**這篇根本沒有情境舉例**，
    改成「本文沒有使用虛構的生活情境」。

## 查過而且正確的部分（沒有動）

- **事件日**：頁面標題上方印 `September 11, 2026`，RSS `pubDate` 是
  `Fri, 11 Sep 2026 10:00:00 GMT`（台北時間同日 18:00，不跨日）。
  slug 尾碼、`news_date`、正文第一段三處一致。
- **規模數字逐句吻合，而且每一處都寫成 OpenAI 的說法**：
  `more than 70 million requests every second`、`over 1 billion people each week`、
  `almost 40 geographic regions`、`more than 500 petabytes`、
  `more than 10x year-over-year for the last three years`、
  Python 尖峰 `more than 20 million requests every second`、
  `6x more CPU efficient`／`15x more memory efficient`／`95% of our production requests`、
  `In Q2 2026, with just 2 engineers, Codex, and GPT‑5.5`、
  `deprecating Python entirely in the coming weeks`。
- **`22M` 那一格成立**：渲染後正文 `22M` **0 次**、`22 million` **0 次**；
  原始 HTML 的 7 次全部落在 `meta description`／`og:description`／`twitter:description`／
  RSC payload／一段 SVG path／一個元素 id。RSS 摘要確實寫著 `22M requests per second`。
- **耐久性與 SLA 的負面結論成立**：以**詞界**比對，`durability`、`durable`、`backup`、
  `replica`、`replication`、`SLA`、`uptime`、`restore`、`disaster recovery`、`retention`
  在整份 HTML 皆為 **0 次**。
  （撰稿者提到的「`SLA` 子字串 27 次假陽性」屬實，來自 CSS 類名如 `translate-y`；詞界比對後 0 次。）
- **兩個後續承諾確實是兩件事**：part II（`In a future post, we'll go into detail about how we
  made multi-tenancy reliability at scale…`）與 Rust 心得
  （`We plan to share more learnings in a future blog.`），兩者都沒有日期。
  今天的 Engineering 網站地圖沒有 part-two 的 `<loc>`、RSS 沒有對應 `<item>`；
  文章寫成「以官方網站地圖與新聞 feed 查核到 2026 年 9 月 18 日未見」，不是「官方確認沒有」。
- **27 條 `verbatim_quote` 全部通過連續字串比對**（修掉兩條之後，見下）。
  其中兩條本輪修正：
  第 3 條 `70M+ requests per second 1B+ people each week 500 PB+ data` 是**拼裝品**
  ——那是六個各自獨立的 `<div>`（`text-h2` 放數字、`text-p2` 放說明），
  連起來的字串在頁面上搜尋不到，已改成可原樣搜尋到的 `500 PB+`，其餘標成讀到的值；
  第 9 條的 `we'll` 用的是 ASCII 直撇，原文是 **U+2019**（同一頁的 `we've` 反而是直撇，
  OpenAI 自己混用），已照原文改。
  第 17 條的 `GPT‑5.5` 確認是 **U+2011**，原樣保留無誤。
- **界線檢查全部通過**：全文沒有購買、升級或訂閱建議，沒有推薦式比價，沒有任何價格；
  廠商宣稱全部有歸屬；沒有把預告寫成已上市（part II 與停用 Python 都寫明沒有日期）；
  只有一個 `callout`、**沒有**投資免責段落；`topics` 沒有掛 `finance`。
- **`checked_on` 2026-09-18** 在內容包三條 source、研究紀錄、正文第二段、
  表格 caption、圖解 caption 六處一致，未更動。

## 留給站主的事

1. **`openai.com/index/*` 的可讀性是浮動的。** 2026-09-16 兩位代理拿到 403 邊緣攔截頁，
   2026-09-18 撰稿者與本代理都拿到 HTTP 200 的正文全文。
   日後重查若又被擋，**不代表本文引用的內容有問題**，也不要再以「讀不到」為由
   改掉已經查證過的句子；要重驗請先確認拿到的是正文。
2. **「亞穩態故障（metastable failure）」這個名詞要不要留。**
   正文現在是名詞＋白話解釋。若覺得對一般讀者太技術，可以只留白話、拿掉括號裡的英文；
   **但不可以換回「驚群效應」**，那是原文另一節的名詞。翻譯階段同理，
   研究紀錄的 `must_not_write` 已加上這一條。
3. **title 仍帶「十億」這個數字。** 本文的處理是照正文那一句寫、並在 FAQ 把 OpenAI 自己的
   四種寫法並列。若站主希望標題完全避開這個數字，需要重擬 title，
   並連動已指向本篇的 `ai-news-openai-broadcom-chip-20260624` 的連結文字。
4. **兩個 FAIL 是協調者的事**：索引內容包 `ai-news-2026-january-september-index` 的標題尚未更新，
   以及第二個連結指向的 `ai-news-openai-broadcom-chip-20260624` 標題比對。
   依規格，本代理沒有動那兩個結尾連結。

## 自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-openai-broadcom-chip-20260624
```

只剩規格允許的兩個 FAIL。段落字數 **2,973**（1,800–3,000），title 39 字，description 175 字。

## 結論

`needs_second_round`。改了 20 條、24 個編輯點，其中一處動到骨幹敘述
（第 3 節的連線池案例被冠上原文另一節的名詞），另有 title 與 FAQ 第 2 題整題重寫。
文章本身現在可刊，但依規格，改到骨幹論述就該再走一輪：
第二輪只需要逐句回來源查**本輪新寫進去的每一句**（第 3 節第 2、3 段、第 4 節第 1、2 段、
第 5 節第 3 段、FAQ 第 2、3、5 題、title、表格四格）。

---

## 第二輪

第二輪查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 六處仍一致，**不改**）。
範圍是第一輪改動過的每一段與新寫進去的每一句，不重做全篇。
三條 sources 全部自己重抓（`curl -sL -A "Mokaair-editorial"`），
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**。
檢查 **63 條**主張（第一輪新寫的段落逐句、四種「10 億」寫法的每一處落點、表格四格、
27 條引文、否定結論重驗、界線重掃），**改了 14 處**。

### 重抓結果

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `openai.com/index/scaling-storage-one-billion-users-part-one/` | 200 | 550,676 | **是**。`<title>` 為「Rapidly scaling online storage to serve over 1 billion ChatGPT users \| OpenAI」；`Request Access`／`Access Denied`／`http-equiv="refresh"` 各 **0** 次 |
| `openai.com/news/rss.xml` | 200 | 736,773 | **是**。本篇 `<item>` 的 `pubDate` 仍為 `Fri, 11 Sep 2026 10:00:00 GMT`、`category` 為 `Engineering` |
| `openai.com/sitemap.xml/engineering/` | 200 | 192,116 | **是**。22 個 `<url>`（20 篇文章＋2 個清單頁）；`part-two` 字串 **0** 次 |

位元組數三次分別是撰稿者 550,655、第一輪 550,689、本輪 550,676。頁面帶隨機產生的元素 id，
**位元組數不可當版本識別**；內容逐句相同。

### 改掉的 14 處

**最重的三處**

1. **研究紀錄第 10 條事實的引文掛錯來源。** `verbatim_quote` 是
   `In a future post, we’ll go into detail about how we made multi-tenancy reliability at scale…`，
   出自**文章頁**，`url` 卻填成 Engineering 網站地圖——那句話在網站地圖裡搜尋不到。
   第一輪報告寫「27 條全部通過連續字串比對」，是因為它**跨來源**搜尋；
   本輪把每條引文綁回**它自己的 `url`** 再比對，27 條裡就這一條落空。
   已把 `url` 改回文章頁，並在事實文字裡分開標明「網站地圖與 feed 沒有第二篇」的證據
   各自在 `sources[2]` 與 `sources[1]`。改完重跑，27 條全數通過。
2. **三處全稱否定與文章自己的敘述互相矛盾。** 第 4 節第 2 段、FAQ 第 3 題、摘要第 4 句
   都寫「沒有列出任何國家或城市名稱」，但**同一句**（第 4 節）緊接著就說
   「以及職缺連結網址裡的城市名」。第一輪拿掉了兩處「唯一」，卻沒有拿掉這個同樣不成立的全稱否定。
   查證：職缺連結 href 是 `careers/software-engineer-habitat-(online-data)-seattle/`（網址裡有城市名，
   渲染後可見文字則沒有，`Seattle` 在可見正文 **0** 次），頁尾語系切換器另外印著 `United States`。
   三處都限縮成「**沒有把任何國家或城市寫成資料存放地點**」；FAQ 第 3 題殘留的
   「只有示意圖上的範例代號」也改成與正文一致的兩處並列。
   研究紀錄 `not_said` 第 3 條有同樣的毛病（「唯一的地區相關字串」），一併更正。
3. **研究紀錄 `must_not_write` 自己留著第一輪刪掉的那個推論。** 第 2 條寫著
   正文那句「**是全部產品加總、以週為單位的人數**」——「全部」與「加總」原文都沒有，
   正是第一輪從 FAQ 第 2 題刪掉的東西。這條是給翻譯階段看的指令，留著等於叫各語系照抄回去。
   已改寫成四種官方寫法並列，並明寫「各語系不可互換、不可挑數字最大或語氣最確定的那一種」。

**其餘十一處**

4. 第 4 節第 2 段「登入、查看 Codex 設定、開新對話**都需要**查資料」漏掉原文的 `may require`
   （第 1 節保留了「可能」，第 4 節掉了）→ 改「都**可能**需要查資料」。
5. 第 3 節第 3 段「**那些**處理程序仍然持續惡化」漏掉 `a subset of processes`
   → 改「仍有**一部分**處理程序持續惡化」。
6. 第 3 節第 2 段「OpenAI 說修法很單純」掉了條件
   `The fix was straightforward **once CPU profiling helped us root cause the issue**`
   → 改「一旦用 CPU 剖析定位到根因，修法就很單純」。
7. 第 4 節第 1 段「反而引發**他們**原本想避免的事故」的「他們」會被讀成回滾的那個團隊，
   原文是 `the outage **we** had worked so hard to avoid`（作者團隊）→ 拿掉「他們」。
8. 第 5 節第 3 段把 `<lastmod>` **斷定**成「網站端的時間戳」——那是推論不是觀察。
   縮到只寫本文真正看到的事（標的時間和頁面印出的發布日期對不起來），並標明
   「這是本文**查核當天**的觀察」。
9. FAQ 第 5 題把同一件事寫成不帶限定的通則（「是網站端的時間戳，不能當成…」），
   改成與正文一致的觀察式寫法。（協調者點名的第 4 項：正文與 FAQ 現在都是「本文的觀察」。）
10. 第 1 節第 3 段「網址**指向西雅圖的職缺**」是對讀不到的職缺頁下判斷（該頁本輪仍回存取限制頁）
    → 改「網址裡帶著西雅圖的地名」，與第 4 節寫法一致。
11. 摘要第 3 句「多租戶**穩定性**」與原文 `multi-tenancy reliability`、正文第 1 節的
    「多租戶**可靠性**」不一致 → 統一成「可靠性」。
12. 研究紀錄 `not_said` 第 2 條「幾次**自己造成的**事故」——第一輪在正文改掉了
    （原文是 `for unrelated reasons`），沒同步回研究紀錄 → 已更正。
13. 研究紀錄 `not_said` 第 4 條「**反覆強調**這裡是保護使用者資料」——`protecting user data`
    在正文只出現 **1** 次 → 改「只說過一次」，並補上 `external, internal, and agent actors`。
14. **騰字**：刪掉第 2 節第 3 段末尾「這種自陳的成長數字沒有第三方查核或稽核，本文只能引用
    OpenAI 自己的說法」。同一個但書在 callout（明白點名「成長倍數」）、第 4 節第 3 段、
    第 5 節第 2 段各出現一次——刪的是**重複敘述**，不是但書本身。段落字數 2,973 → **2,956**。
    另加兩條 `must_not_write`（地區全稱否定、`<lastmod>` 的觀察限定）擋住翻譯階段再犯。

### 協調者點名的四項：查證結果

1. **第一輪新寫的每一句都回貼原文比對過**，除上面第 4–11 點外沒有再發現走樣的句子。
2. **兩個官方名詞沒有再互換。** 本輪重數：`metastable failure` 在連線池那一節出現 **2** 次
   （`This was a class of failures … : metastable failure` 與 `In this case, it created a metastable
   failure for us`）；`thundering herd` 只出現 **1** 次、在另一節 `Avoiding flooding downstream
   resources`。正文只用「亞穩態故障」，**沒有出現「驚群效應」**。
   因果也照原文：`requests to slower overloaded servers returned connections to the pool later and
   were therefore selected more frequently by subsequent requests, gradually concentrating more
   traffic on the pods already struggling` → 正文逐項對得上，**沒有替官方補原文沒有的解釋**。
3. **四種「10 億」寫法，每一處落點都對得上其中一種、都不比它強。** 今天的 HTML 逐一確認：
   `<title>`／`og:title`／`twitter:title`＋文末 part II 句＝`over 1 billion ChatGPT users`；
   正文規模句＝`supporting products used by over 1 billion people each week`；
   `meta description`／`og:description`／`twitter:description`＝`1 billion ChatGPT users and 22M
   requests per second`；`og:image:alt`／`twitter:image:alt`＝`nearly 1 billion ChatGPT users`。
   落點：title「每週逾十億人使用」→ 正文句；摘要第 1 句與第 2 節第 1 段「支撐旗下產品每週被超過
   10 億人使用」→ 正文句；第 1 節第 2 段「每週超過 10 億人」→ 統計方塊 `1B+ / people each week`；
   description 不提這個數字；FAQ 第 2 題四種並列，引述逐字無誤。**沒有一處比它的來源強。**
   `22M requests per second` 入文兩處（第 2 節第 2 段、表格那一格）**都帶了出處**
   （官方 RSS feed 與網頁中繼資料）。重驗：渲染後正文 `22M` **0** 次、`22 million` **0** 次；
   原始 HTML 9 次全落在三個 meta、RSC payload、一段 SVG path 座標與一個隨機元素 id
   （第一輪記 7 次，差額來自頁面隨機 id，**結論不變**）。
4. **`<lastmod>` 那個觀察本輪自己重現得到，而且正文寫成「本文的觀察」。**
   這篇文章的 `<lastmod>` 是 `2026-09-17T21:51:03.895Z`，頁面印的發布日是 `September 11, 2026`；
   同一份地圖給 `jalapeno-first-results`（09-17T01:12:55）、
   `continuous-voice-interaction-with-gpt-live`（09-17T11:33:44）、
   `gpt-5-6-frontier-intelligence-efficiency`（09-17T11:33:45）的值，
   對上文章頁「Keep reading」印的 `Aug 25, 2026`／`Aug 3, 2026`／`Jul 29, 2026`——**四組全部對不起來**。
   （第一輪讀到的是 09-17 與 09-15 兩批，今天三篇同為 09-17，結論不變。）
   正文與 FAQ 現在都標明是本文查核當天的觀察，**沒有寫成 OpenAI 的說明**。
   `us0`／`us1`／`eu0` 全篇**沒有任何地區推論**（正文、FAQ 第 3 題、研究紀錄一致）。

### 查過而且正確、沒有動的部分

- **耐久性與 SLA 的否定結論重驗成立**：`durability`、`durable`、`backup(s)`、`replica(s)`、
  `replication`、`SLA`、`uptime`、`restore`、`disaster recovery`、`retention`、`redundancy`、
  `failover` 在整份 HTML 的**詞界**命中數全為 **0**；渲染後正文只有一個百分比 `95%`，
  因此「沒有任何可用性數字」成立。
- **表格四格的限定詞與出處欄**都對得上 `more than 70 million requests every second`／
  `more than 20 million requests every second`／`more than 500 petabytes`（方塊 `500 PB+`）／
  `more than 10x year-over-year for the last three years`；「近 40 個」對 `almost 40 geographic regions`。
- **事件日**：RSS `pubDate` 仍是 `Fri, 11 Sep 2026 10:00:00 GMT`（台北時間同日 18:00，不跨日），
  頁面標題上方印 `September 11, 2026`，與 slug 尾碼、`news_date` 一致。
  網站地圖與 RSS 全文搜尋 `part-two` 皆 **0** 次。
- **界線重掃全部通過**：`topics` 沒有 `finance`；只有**一個** `info` callout、**沒有**投資免責段落；
  沒有訂閱、購買、升級或投資建議，沒有價格與推薦式比價；廠商宣稱全部帶歸屬；
  預告（part II、Rust 心得、停用 Python）都寫成沒有日期；沒有推定台灣可用。
- **摘要每一句仍 ⊆ 正文**，FAQ 答案與正文不衝突，圖解四格的數字（7000 萬、40）都在正文出現。
- **`checked_on` 2026-09-18** 六處仍一致，未更動。

### 留給站主的事

1. **第一輪留的四項全部仍然成立，本輪沒有推翻任何一項**（`openai.com/index/*` 可讀性浮動、
   「亞穩態故障」名詞去留、title 要不要避開「十億」、兩個 FAIL 由協調者處理）。
2. **職缺頁本輪重抓仍是存取限制頁。** 文章現在只說「網址裡帶著西雅圖的地名」，
   沒有斷言職缺在西雅圖；日後該頁若可讀且站主想寫明，要重新查證後才改。
3. **「沒有把任何國家或城市寫成資料存放地點」是本輪替三處全稱否定做的限縮寫法。**
   翻譯各語系時要照這個限縮翻，**不可以回到「沒有列出任何國家或城市名稱」**——
   `must_not_write` 已加上這一條。

### 自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-openai-broadcom-chip-20260624
```

只剩規格允許的兩個 FAIL。段落字數 **2,956**（1,800–3,000），title 39 字，description 175 字。

### 結論

`ok`。第二輪改了 14 處，其中 3 處是第一輪留下的自相矛盾或引文掛錯來源，其餘為限定詞與歸屬的回補。
**沒有動到骨幹敘述**——第一輪那處骨幹更正（連線池案例的官方名詞與因果）本輪逐字重驗，成立且未再更動。
不需要第三輪。
