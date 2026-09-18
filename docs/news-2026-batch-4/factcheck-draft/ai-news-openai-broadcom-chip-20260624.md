# 獨立查核：ai-news-openai-broadcom-chip-20260624

查核代理：未參與撰稿。查核日 **2026-09-18**（與內容包的 `checked_on` 同一天，未更動）。
查核方式：`sources[]` 三條全部重抓並讀 body，內容包拆成 **106 條主張**逐條回原文核對，
**29 條 `verbatim_quote` 用程式做連續字串比對**。改了 **18 處**，另有 6 件留給站主。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實**，也沒有猜任何識別碼；
所有請求都沒有帶 email、姓名或任何個人資料。

## 重抓結果（三條 sources 今天全部讀到正文）

| source | UA | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- | --- |
| Broadcom 發表稿 | `Mokaair-editorial` → **失敗** | 000 | 0 | curl exit 28，逾時 60 秒 |
| Broadcom 發表稿 | curl 預設 UA | 200 | 70,913 | 是。五個條列、dateline、三段引言、三個小標、Cautionary Note 全在 |
| Broadcom 2025-10-13 稿 | curl 預設 UA | 200 | 71,384 | 是。10 gigawatts、term sheet、800 million、四段引言全在 |
| OpenAI 官方文章 | `Mokaair-editorial` | 200 | 403,575 | 是。Next.js RSC 串流，解出 8 段 chunk／230,738 字元，取得全文四個小標、五個條列、三段引言 |

兩個 Broadcom 位元組數與撰稿者、前兩輪代理記的完全相同（70,913／71,384）。
`investors.broadcom.com` 拒絕 `Mokaair-editorial` 這件事**已經第四次重現，四次四種 curl 結束碼**
（52／92／56／28）——失敗方式不穩定，但主機是穩定的：拿掉自訂 UA 每次都回 200。
**只有這個主機需要 fallback**，openai.com 用規定的 UA 直接就通。

**撰稿者升級 `sourcing_verdict` 為 `full` 的依據成立**：OpenAI 那篇今天確實讀到公告正文
（`<title>` 相符、四個小標齊全、三段引言齊全），不是 403 擋阻頁，也不是封存。

## 改掉的 18 處

**先回答撰稿者點名的三件事——三件全部站得住，只有歸屬要修。**

1. **『may be』對『we believe to be』：沒有讀反，沒有合併，中文沒有比原文強。**
   `what may be the fastest` 在 Broadcom 頁 1 次、OpenAI 頁 **0 次**；
   `what we believe to be the fastest` 在 OpenAI 頁 1 次、Broadcom 頁 **0 次**。兩句其餘部分逐字相同。
   **但限定語被刪了**：兩家原文都是 `the fastest ASIC development cycle ever achieved in
   **high-performance advanced semiconductors**`，文章寫成「史上最快的 ASIC 開發週期」。
   已補回「高效能先進半導體有史以來最快的」。並列不合併的作法維持。
2. **『如果 AI 能幫助工程師…』：兩邊原文都逐字存在，可以寫，但不是 OpenAI 獨有。**
   `If AI can help engineers design better chips faster, it can lower the cost of compute across the
   industry and help democratize access to advanced AI.` 在 Broadcom 新聞稿與 OpenAI 文章**各 1 次**，
   位置都在 `Nine-month tape-out` 那一節最後一段，**是新聞稿敘述、沒有具名到任何人**，
   所以文章不把它歸給個人是對的。條件句、講全產業、沒有數字、不是已實現語氣，也都保住了。
   只把「OpenAI 自己的文章裡也有一句」改成「兩篇官方文章都有一句」。
3. **多處「兩方官方文章都沒有…」：同義詞重掃後全部成立**（範圍限縮在本文引用的三頁、查核日 2026-09-18）。
   NVIDIA／nvidia **0**；AMD／TPU／Trainium／Blackwell／Rubin／Hopper／Instinct **0**；
   GPU 在兩篇正文 **0**、graphics processing **0**；nm／nanometer／process node／TSMC／foundry／fab／
   wafer／transistor／die size／package **0**；HBM／DRAM／SRAM／GB／TB／bandwidth **0**；
   percent **0**、% 在正文 **0**；50%／50 percent／cheaper than **0**；
   `10 gigawatts` 在兩篇 2026-06-24 頁面 **0**（gigawatt 只以 `gigawatt scale` 出現）；
   watt 只以 `performance per watt` 出現，沒有耗電瓦數；Taiwan／Asia **0**。
   原始 HTML 的命中（Broadcom 的 % 52 次與 cost 49 次、OpenAI 的 `50%` 與 `gpu`）
   **逐一確認都在 CSS 與 Next.js 資產字串裡**——`gpu` 是頁面變體清單裡的 `gpu-debug`，
   `50%` 是 `border-radius: 50%`。不在正文。
   只把否定句加上「正文」與查核日的範圍限縮（BRIEF 錯誤型態 6）。

**以下是撰稿者沒有點名、我自己查出來的。前四項是實質錯誤。**

4. **第一節第一段的 Broadcom／OpenAI 對比是虛構的。**
   原文：「Broadcom 形容它是『圍繞 OpenAI 對大型語言模型推論願景所打造的加速器』；**OpenAI 則說**
   這顆晶片『設計上保有彈性…』」。**兩句話都逐字出現在兩家公司的頁面上**——兩篇根本是同一份文稿，
   開頭整段一字不差。真正的差異只有五處：標題、條列第 3 點、`may be`／`we believe to be`、
   Kawwas 職稱、以及 OpenAI 頁多出三段內文與第四個小標。
   已改寫成「兩家公司發出的其實是同一份文稿」，並順手補回被丟掉的 `for the future of`
   （「推論**未來**願景」）與 `to work with all LLMs`（「能搭配**所有**大型語言模型」）。
5. **表格與正文把 Celestica 的工作寫給了 Broadcom。**
   兩篇文章結尾**唯一做分工的那一句**寫的是
   `combining OpenAI-designed accelerators with **Broadcom silicon implementation, networking, and
   connectivity technologies**; and **Celestica's board, rack and system expertise**`。
   原稿的表格給 Broadcom「晶片實作、**電路板與機櫃系統整合**、高效能網路」，正文也寫「機櫃系統整合」——
   電路板與機櫃是 **Celestica** 的，而且這和同一篇下一列自相矛盾。
   已改成 Broadcom =「矽晶實作、網路與連接技術」、Celestica =「電路板、機櫃與系統的專業能力」。
   前面那句 `with partners Broadcom and Celestica, helping industrialize the platform through chip
   implementation, board, rack system integration…` 是**把整串掛在兩家身上**，不能拿來分工。
6. **「這是兩篇官方文章裡唯一被點名的合作對象」不成立。**
   Celestica 也是被點名的 partner，而且同一篇第二節就在講它。
   已改成「微軟是兩篇官方文章裡唯一被點名的**資料中心**合作夥伴，其餘一律寫成『其他合作夥伴』」。
7. **FAQ 第 5 題「官方文章沒有提到任何一款產品會因此變快、變便宜」不成立。**
   OpenAI 的文章寫著 `Every improvement in cost, speed, and reliability **can show up as** a faster
   ChatGPT answer, a Codex task that can take more steps with less waiting, an API product that is
   cheaper to build, or more dependable access when demand is high.`
   已改成照原文寫出這句條件句，並說明它沒有日期、沒有百分比、沒有保證，也沒說是 Jalapeño 造成的。
   第五節第三段同步補上，避免那段的否定句被讀成「官方什麼都沒說」。
8. **文章自己打自己：正文寫「官方文章沒有講這代表『還不是出貨產品』」，
   summary 卻寫「還沒有對外出貨」、FAQ 第 1 題寫「不是已出貨的產品」。**
   `corrections-ai.md` must_fix #1 已經認定 `NOT SHIPPING PRODUCT` 是研究者的推論、頁面從來沒有這句。
   三處都改成「官方文章沒有寫出貨或上市的任何時間」，並刪掉正文那句談編輯流程的後設句。
9. **Brockman 引言把頁面上分開的兩段接成一句，還砍掉一半當完整引文。**
   頁面印的是 `"The world is moving to a compute-powered economy," said Greg Brockman, President and
   Co-Founder, OpenAI. "Jalapeño is part of our long-term…`。
   原稿用一對引號接起來、句號收在「更負擔得起」，把 `for people and businesses` 與最後一個子句吃掉了。
   已改成明講分成兩段、補回 `for people and businesses`、並用刪節號標出截斷。
   **研究紀錄那條 `verbatim_quote` 同樣不成立，已拆成兩條**（見下）。
10. **「這是 OpenAI 第一款自行設計…的晶片」放大了官方說法。**
    官方只說 `OpenAI's first Intelligence Processor`；研究紀錄的 `unverified_or_excluded` 自己就把
    無限定的「第一款客製晶片」列為排除項。已改成官方較窄的寫法。
11. **9 個月 tape-out 與「工程樣片在實驗室運作」被列在「可驗證的動作事實」那一欄**（第五節第一段與 callout）。
    實驗室內的狀態外部觀察不到，`must_fix` #1 已要求標成廠商宣稱。兩處都移到「外界無從查證」那一欄，
    第三節也補上「這個數字也是公司自己說的」。
12. **「Celestica 自己的官方新聞頁與新聞稿 RSS 目前都沒有出現…」不能寫。**
    那兩個網址**不在 `sources[]`**，而且是 2026-09-16 的快照、今天沒有重查，卻寫成「目前」（活資料當常數）。
    已改成限縮到本文引用的三篇文件：「這三篇文章沒有任何一句話出自 Celestica」。
13. **「Broadcom 自己把這段部署時程／這句話列為前瞻性陳述」**（summary 第三句、callout）。
    Cautionary Note 點名的是 `the deployment of gigawatt scale datacenters`，不是「2026 年底前開始部署」那一句。
    已改成「把部署十億瓦等級資料中心列為前瞻性陳述」。第四節第二段原本就寫對了，未動。
14. **「Tape-out 是晶片設計定案、送代工廠做光罩的階段」**——三篇來源都沒有提到任何代工廠或光罩，
    這是文章自己引進來源沒有的技術細節，而且同一篇正文才剛說「沒有寫哪一家代工廠生產」。
    已改成「設計定案、交付製造的階段」。
15. **「規劃到 2029 年底的合作」**（第四節第三段）——`end of 2029` 掛的是
    `Broadcom to deploy racks of AI accelerator and network systems targeted to start in the second
    half of 2026, to complete by end of 2029`，是**部署機櫃**的時程，不是合作本身的期限。已照原文改寫。
16. **「OpenAI 也提到公司當時已成長到『每週超過 8 億使用者』」**——那句在新聞稿裡是敘述句，
    沒有具名到 OpenAI 的任何人。已改成「那則公告也寫著」。歸屬與 2025-10-13 的日期都維持。
17. **第二節第三段句尾「不是本站查證到的財務數字」是殘句**（這篇沒有任何財務數字），已刪；
    同段「OpenAI 也提到」改成「兩篇官方文章也都寫著」（那句兩邊都有），
    並把括號裡的改寫引文換成原文的意思：「提供給使用者的同一批模型，正在幫助改善用來運行未來模型的基礎設施」。
18. **description**「說明這顆晶片目前只到工程樣片與實驗室測試」→「說明**依官方說法**…」；
    句尾「為何是兩件事」→「為何要分開看」。另把全篇「雙方官方文章」統一成「兩篇官方文章」。

## 研究紀錄改了 6 處

1. **`event_date_basis` 寫錯**：原記「OpenAI's own post … carries no independent dateline」。
   **它有。** 頁面印著 `<p class="text-meta text-primary-100">June 24, 2026</p>`，
   RSC payload 也帶 `"publicationDateText":"June 24, 2026"`。
   事件日 2026-06-24 現在是**兩家自己的頁面各有一個可見的一手日期**，不再只靠 Broadcom。
2. **Brockman 那條 `verbatim_quote` 拆成兩條**——它是 26 條裡**唯一**沒有通過連續字串比對的，
   原因是把被 `," said Greg Brockman…"` 隔開的兩段接起來，還把片段結尾的逗號悄悄改成句號。
3. **分工那條（Celestica）`is_vendor_claim` 由 `false` 翻成 `true`**，理由同 must_fix #1
   對「從零設計」那條的處理：誰做了哪一塊是關於功勞與流程的自述，外部無法觀察。
   同時把那條的 `fact` 改寫成**明確記下「只有結尾這句在做分工、前一句是兩家共用」**，
   免得下一個人重蹈第 5 點的覆轍。
4. **`corrections-ai.md` must_add 的「條列 vs 內文」那一條要修正**：
   那份修正清單是在 OpenAI 頁還讀不到時寫的，說效能寫法有 `better` vs `substantially better` 的落差。
   讀了兩邊之後，**這個落差只存在於 Broadcom 那一頁**：
   Broadcom 條列第 3 點 `Will deliver performance per watt **better** than…`，
   OpenAI 條列第 3 點 `Early testing shows that the first-generation accelerator will deliver
   performance per watt **substantially** better than…`，兩篇內文都是 `substantially better`。
   四個一手寫法裡有三個帶 `substantially`，文章用「顯著優於」是對的。已記進紀錄。
5. **新增一條 `TYPOGRAPHY` 事實**，記下兩頁「同文不同字」的三個陷阱：
   同一句 flexibility 裡 Broadcom 印 ASCII `OpenAI's`、OpenAI 印 `OpenAI’s`（U+2019）；
   模型名 Broadcom 印 `GPT-5.3-Codex-Spark`（ASCII 連字號）、OpenAI 印 `GPT‑5.3‑Codex‑Spark`
   （**U+2011 不斷行連字號**，正是 BRIEF 警告過的那個陷阱）；結尾那句 OpenAI 多一個序列逗號。
   **文章寫 ASCII 連字號，和它引用的 Broadcom 頁一致，沒問題。**
6. **`live_data_warnings` 更新**：Broadcom UA 拒絕第四次重現（四種結束碼），
   openai.com 由 403 轉 200 同日兩人獨立重現。

**另外 25 條 `verbatim_quote` 逐字成立**（只折疊空白，ñ／U+2019／U+2011 一個字元都沒放過），
`Tomahawk` 那條的「唯一」已限縮成「兩篇 2026-06-24 頁面裡唯一被點名的 Broadcom 產品系列」，
並補上來源自己的 `including`（不是全清單）。

## 查過而且正確的部分（沒有動）

- **三條 sources 今天全部讀到正文**，`checked_on` 2026-09-18 屬實；
  內容包三條、研究紀錄三條、正文第二段、表格 caption、圖解 caption **五處查核日一致**，
  沒有因為我今天重查而更動。
- **`sources[]` 已照 `source_list_fix` #1 拿掉 RSS feed 網址**，三條全是文章頁；
  106 條主張沒有任何一條需要 `sources[]` 以外的網址才站得住。
- **界線全數乾淨**：沒有購買建議、沒有推薦式比價、沒有任何價格或估值、沒有 AVGO 股價或營收、
  沒有上市預測或「利多」語氣、沒有「我們試用」這類實測語氣。
  **AI 篇只有一個 callout**（沒有多加投資免責段），`topics` 是 `ai／gadgets／ai-news`，不帶 `finance`。
  Broadcom 是上市公司這件事在文章裡完全沒有被寫成投資角度。
- **狀態詞正確**：deployment 一律寫成「規劃」「目標」「開始部署」，`designed for` 沒有被寫成承諾日；
  tape-out 沒有被寫成量產；工程樣片沒有被寫成上市；沒有把美國首發推定成台灣可用。
- **日期分得乾淨**：事件日 2026-06-24、更早的公告 2025-10-13、規劃部署 2026 年底、
  2025 那份的 2026 下半年與 2029 年底，五個日期沒有互相污染；
  「8 億週活躍使用者」每次出現都帶 2025-10-13。`news_date` 與 slug 尾碼一致。
- **沒有自己算出來的數字**：100 億瓦是 `10 gigawatts` 的換算並在括號附原文，
  9 個月、2026 年底、2029 年底全部照印；沒有任何加總、清點或推算出來的值。
- **圖解與 hero 未動**（`hero.alt` 依規格不查不改）。圖上三個數字（6/24、9 個月、2026 年底）
  與 summary 的每一個數字都能在正文找到；內容包 title 與研究紀錄 title 逐字相同，
  image caption 與研究紀錄 `diagram.caption` 逐字相同。
- 全文沒有簡體字，沒有列表、Markdown 或 emoji。

## 留給站主的 6 件事

1. **`check_article.py` 仍是 FAIL，只剩兩條允許保留的**：
   `zh-TW link text must be the title of ai-news-2026-january-september-index` 與
   `… of ai-news-chatgpt-storage-scale-20260911`。兩個結尾連結依規格未動，
   由協調者在索引與相關文章落地後原地更新。**這兩條失敗在查核前後完全相同**，不是本次編輯造成的。
2. **段落總字數 2,975／3,000，只剩 25 字。** 之後任何一句要加，都得從別處刪等量的字——
   但不可以刪但書或限定詞。翻譯階段照抄段落結構時也要留意這個餘裕。
3. **Broadcom 條列第 3 點少了內文的 `substantially`，OpenAI 條列第 3 點有。**
   文章統一用「顯著優於」（正確），但正文只註明了 `production`／`tape-out` 那一處落差，
   沒有註明效能這一處。`corrections-ai.md` must_add 要求「註明兩處不同」，
   我把它記進研究紀錄而沒有寫進正文——**字數已滿，是否補寫請站主決定**。
4. **OpenAI 文章還有四段沒進中文正文**（全端飛輪、democratizing AI、
   以及 `Making advanced AI more broadly available` 整節）。
   其中那句條件句本次已補進第五節與 FAQ 第 5 題，其餘三段是編輯取捨，字數上也放不下。
5. **Richard Ho 的引言怪處維持原樣**：他被介紹為 `who leads OpenAI's hardware program`，
   引言卻是 `using detailed insights from our close collaboration with OpenAI researchers`。
   今天確認**兩家頁面印的一模一樣**，不是 Broadcom 的轉寫瑕疵。文章沒有引用這段（字數）；
   日後要用必須照原樣引，不可以改歸給 Broadcom，也不可以偷偷修好。
6. **`investors.broadcom.com` 對 `Mokaair-editorial` 的拒絕已四次重現、四種 curl 結束碼。**
   若要把重抓自動化，這個主機必須單獨列成例外，否則會被誤判成來源已死。
   相對地 **openai.com 的擋阻狀態不穩定**（09-16 兩輪 403、09-18 兩人 200），下次要實測、不能沿用紀錄。

## 自檢最後輸出

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-chatgpt-storage-scale-20260911
```

## 結論

`needs_owner`：106 條主張逐條核對後，**沒有任何一條被來源推翻到骨幹論述**——
文章的主軸（同一份文稿、兩個標題、9 個月只到 tape-out、部署只是規劃、廠商宣稱與前瞻性陳述要分開）
全部站得住，撰稿者自己點名的三件事也全部通過。
改掉的 18 處集中在**歸屬（把共同文稿寫成對比）**、**角色分工（Celestica 的工作寫給 Broadcom）**、
**四個過寬的否定句**與**限定語遺漏**，都是句子層級的修正，不需要重寫。
唯一擋住 gate 的是兩個結尾連結的 title 尚未對齊，那由協調者處理、不在查核代理可動的兩個檔案裡。

## 第二輪

第二輪查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 未更動）。
範圍是覆核第一輪改動過的每一段與新寫進去的每一句，`sources[]` 三條全部自己重抓並讀 body，
**共核對 118 條主張**、**29 條 `verbatim_quote` 用程式做連續字串比對**。
內容包改 **11 處**、研究紀錄改 **6 處**（含新增 `factcheck.second_round`）。
**沒有使用 `sources[]` 以外的新網址替文章補事實**；所有請求都沒有帶 email、姓名或任何個人資料。

### 重抓結果（三條今天全部讀到正文）

| source | UA | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- | --- |
| Broadcom 發表稿 | `Mokaair-editorial` → **失敗** | 000 | 0 | curl exit 28，逾時 45 秒（**第五次重現**） |
| Broadcom 發表稿 | curl 預設 UA | 200 | 70,913 | 是。五個條列、dateline、三段引言、三個小標、Cautionary Note 全在 |
| Broadcom 2025-10-13 稿 | curl 預設 UA | 200 | 71,384 | 是。10 gigawatts、term sheet、second half of 2026、end of 2029、800 million 全在 |
| OpenAI 官方文章 | `Mokaair-editorial` | 200 | **403,533** | 是。自己 bracket-match 解出 RSC chunk（230,739 字元），四個小標、五個條列、三段引言、全部內文 |

兩個 Broadcom 位元組數與前四次逐位元組相同。OpenAI 那頁的 bytes 與第一輪差 42（403,575 → 403,533），
原因是頁尾「最新文章」卡片會換（今天抓到的是 09-17、09-09、09-08 三篇），**正文一字未變**。
`investors.broadcom.com` 拒絕 `Mokaair-editorial` 已第五次重現，這次又是 exit 28；只有這一台主機需要 fallback。

### 第 1 個點名疑點：兩邊文稿逐段對過一次

用 difflib（NFKC、折疊空白）把 **Broadcom 的 19 個區塊**對 **OpenAI 的 24 個區塊**跑完，結果如下。

**逐字相同的 11 個區塊**：條列 1、2、4、5；開頭 `today unveiled Jalapeño…` 那段
（Broadcom 只多一個 GLOBE NEWSWIRE dateline）；`While OpenAI is still measuring final performance…` 那段；
Richard Ho 引言；Hock Tan 引言；三個共同小標（`Designed to be the best inference platform for LLMs`、
`Nine-month tape-out, accelerated by OpenAI models`、`Building a multi-generation platform with partners`）；
`Jalapeño is a blank-slate design…` 那段；`The same models served to users…` 那段。

**措辭真的不同的 5 處**（全部很小）：

1. **條列第 3 點，差最多的一處**。Broadcom：`Will deliver performance per watt better than
   current state-of-the-art, based on early testing`；OpenAI：`Early testing shows that the
   first-generation accelerator will deliver performance per watt substantially better than
   current state-of-the-art`。
2. 交付那段：`Semiconductor Solutions President Charlie Kawwas`（Broadcom）對 `President Charlie Kawwas`（OpenAI）。
3. Brockman 的具名：`President and Co-Founder, OpenAI` 對 `President and Co-Founder of OpenAI`。
4. `what may be`（Broadcom，正文 1 次、OpenAI 正文 0 次）對 `what we believe to be`（OpenAI 正文 1 次、Broadcom 正文 0 次）。
   **第一輪的回報完全正確**，兩句其餘部分逐字相同。
5. 結尾分工句：OpenAI 少了 `and expanding` 前的逗號，多了 `board, rack, and system expertise` 的序列逗號。

**結構上的不同**：OpenAI 那頁另有**四段內文**（`That is the full-stack advantage…`、
`Jalapeño strengthens the flywheel…`、`The point of this work is simple…`、`Democratizing AI means…`）
與**第四個小標** `Making advanced AI more broadly available`；Broadcom 那頁則多了 dateline、
About／Press Contacts 與 Cautionary Note。（第一輪報告寫「多出三段」，實際是四段。）

所以「兩家公司發出的其實**是**同一份文稿」說得太滿，而且和第五節「**OpenAI 的文章**有一句條件句」
自相矛盾——那句 `can show up as` 正好就在 OpenAI 獨有的第四節裡。已改成「其實**大半**是同一份文稿」。
文章對差異的描述沒有比實際大，也沒有任何一句在替兩家公司解釋為什麼不同（第三節第三段只並列兩種保留字）。

### 內容包改掉的 11 處

1. **FAQ 第 4 題「一項規劃到 2029 年底、部署 100 億瓦客製化 AI 加速器的多年期合作」。**
   `end of 2029` 掛的是**機櫃部署**：`Broadcom to deploy racks of AI accelerator and network systems
   targeted to start in the second half of 2026, to complete by end of 2029`。
   第一輪在第四節第三段改對了，**FAQ 漏改**。已照原文改成「部署 100 億瓦客製化 AI 加速器的多年期合作，
   其中 Broadcom 部署機櫃的目標是 2026 年下半年開始、2029 年底前完成」。
2. **第四節第一段「Broadcom 與 OpenAI 都只用 gigawatt scale 描述部署規模，沒有寫出吉瓦數字」。**
   這句沒有限定是哪兩篇，卻被同一節第三段的「100 億瓦（10 gigawatts）」打臉——那個數字就在
   `sources[]` 的 2025-10-13 稿裡（`10 gigawatts` 該頁 2 次）。已改成「**兩篇官方文章**都只用…」。
3. **summary 第二句與 FAQ 第 1 題的「官方文章沒有寫出貨或上市的任何時間」。**
   2025-10-13 那份確實印了時程與規模（`10 gigawatts`、`second half of 2026`、`end of 2029`），
   主詞是機櫃部署、不是這顆晶片上市，但否定句仍不該涵蓋到它。兩處都改成「**兩篇 6 月 24 日的**官方文章…」。
4. **同一條否定句在正文沒有落腳點**（summary ⊆ 正文、FAQ ⊆ 正文）。
   第三節第二段「官方文章寫到這裡就停了，沒有再說這些樣片和出貨產品的關係」已擴寫成
   「**兩篇文章**寫到這裡就停了，沒有再說這些樣片和出貨產品的關係，**也沒有寫出貨或上市的時間**」。
5. **第二節第一段「（唯一被點名的產品是 Tomahawk 網路晶片）」是全稱說法。**
   Jalapeño 與 GPT-5.3-Codex-Spark 也是被點名的產品；而 2025-10-13 那份還點名了 Ethernet（5 次）與 PCIe。
   已改成「（**其中只點名** Tomahawk 網路晶片一項產品）」，範圍跟著它所屬的 2026-06-24 分工句走。
6. **表格 Broadcom 那列兩欄不同源。** 中文寫「矽晶實作、網路與**連接**技術」（來自結尾分工句），
   英文卻引 `silicon implementation and networking technologies`（來自 Tomahawk 那一句，沒有 connectivity）。
   已把英文換成分工句原文 `silicon implementation, networking, and connectivity technologies`，
   與 Celestica 那列同源。
7. **第一節第一段「其實是同一份文稿」→「其實大半是同一份文稿」**（理由見上一節）。
8. **第五節第三段「OpenAI 的文章只有一句沒有日期的條件句」。**
   同一節上一段才引了另一句沒有日期的條件句（`If AI can help engineers design better chips faster…`）。
   刪掉「只有」；後半「除此之外，沒有任何一句話說使用者會在哪一天感受到差異」保留，限定力不變。
9. **第五節第三段與 FAQ 第 5 題的「更便宜的 API 產品」。**
   原文是 `an API product that is **cheaper to build**`——便宜的是打造成本，不是售價。
   已改成「打造成本更低的 API 產品」，並在兩處補「等」：原文那一串有四項
   （另含 `more dependable access when demand is high`），文章只列了其中兩到三項。
   `can show up as`／「有可能呈現為」、無日期、無百分比、無保證**全部保留**，也沒有寫成「官方完全沒提」。
10. **「每週超過 8 億使用者」補回原文的 active**：`over 800 million weekly active users`
    →「超過 8 億**週活躍**使用者」。第四節第三段、第五節第一段、callout 三處一致，
    2025-10-13 的日期與「自報數字」屬性未動。
11. **第二段「以下每一項都是兩篇官方文章裡的說法」→「這三篇官方文章」**——
    這篇也用了 2025-10-13 那份（第四節第三段、summary 第四句、FAQ 第 4 題）。

### 研究紀錄改了 6 處

1. `IMPORTANT WORDING DIFFERENCE` 那條 `fact` 補上**完整的兩頁逐段比對結果**
   （11 個區塊逐字相同、5 處措辭不同、OpenAI 多四段內文與第四個小標），
   讓下一個人不必重跑，也不會把差異說大或說小。
2. Tomahawk 那條加上**範圍警告**：「唯一」只對 2026-06-24 那兩頁成立，
   2025-10-13 那份點名了 Ethernet／PCIe／optical connectivity。
3. `live_data_warnings` 的 Broadcom 條：四次 → **五次重現**（本次 exit 28、45 秒、0 bytes）。
4. `live_data_warnings` 的 openai.com 條：同日**三人**獨立重現 200，並記下 bytes 會在 403,533–403,585
   之間漂移是因為頁尾「最新文章」卡片會換、正文不變——避免下次有人拿 bytes 當成內容改過的證據。
5. `left_for_the_owner` 更新字數（2,975 → 2,984／3,000），並在 `substantially` 那條補上
   **文章引用的是兩頁逐字相同的內文句、不是 Broadcom 少了 `substantially` 的那條條列**；
   另新增一條 FAQ 第 6 題的 `⊆ 正文` 取捨（見下）。
6. `factcheck` 底下新增 `second_round`（日期、方法、118 條、29 條引文比對、11 處改動、結論）。

### 查過而且正確的部分（沒有動）

- **29 條 `verbatim_quote` 全部是所引頁面上的連續字串**（29/29，含 ñ、U+2019、U+2011 每一個字元），
  沒有任何一條帶 `...`／`…`／`|` 需要分段驗證。第一輪把 Brockman 拆成兩條的作法今天複驗成立。
- **分工一致性（第 2 個點名疑點）**：Broadcom＝矽晶實作／網路／連接、Celestica＝電路板／機櫃／系統，
  在正文、表格三列、圖解四格、image alt、summary、FAQ 六題、callout、description **全部一致**，
  沒有任何一處把電路板或機櫃寫給 Broadcom。全文「唯一」類全稱說法只剩兩處且都帶範圍：
  微軟那一處（實測 Microsoft 在兩篇 2026-06-24 頁各 1 次、2025-10-13 頁 0 次）與改過的 Tomahawk 那一處。
- **狀態詞與歸因（第 5 個點名疑點）**：tape-out 沒有被寫成量產（第三節第一段明說「不等於已經量產出貨」）、
  工程樣片沒有被寫成上市；9 個月與實驗室樣片**五處都帶歸因**（第三節第一段末、第三節第二段、
  summary 第二句、callout、第五節第一段的「外界無法查證」欄）。
  `high-performance advanced semiconductors` 的限定語完整保留為「高效能先進半導體有史以來最快的」。
- **效能措辭（第 6 個點名疑點）**：文章的「顯著優於現有最佳水準」取自**兩頁逐字相同的內文句**，
  不是 Broadcom 少了 `substantially` 的條列；歸屬在四處一致。
  實測 `substantially`：Broadcom 正文 1 次（內文）、OpenAI 正文 2 次（條列＋內文）。
- **否定句範圍全篇重掃**（三份正文的詞頻表）：GPU 0／0／0；NVIDIA、AMD、TPU、Trainium、Blackwell、
  Rubin、Hopper 三頁皆 0；TSMC、foundry、fab、wafer、transistor、nanometer、process node、mask、
  reticle 三頁皆 0；HBM、DRAM、SRAM、bandwidth 三頁皆 0；percent、`%`、`$`、price、`50` 三頁皆 0；
  `cheaper` 只在 OpenAI 的 `cheaper to build` 出現 1 次；Taiwan／Asia 三頁皆 0；
  `10 gigawatts` 在兩篇 2026-06-24 頁 0 次、2025-10-13 頁 2 次；watt 只以 `performance per watt` 出現。
- **前瞻性陳述**複驗：2026-06-24 的 Cautionary Note 原文點名 `delivering Jalapeño to OpenAI` 與
  `the deployment of gigawatt scale datacenters` **兩件事**，且寫 `include, but are not limited to`。
  文章用「列為前瞻性陳述**之一**」正確，summary 與 callout 沒有寫成「唯一」。
- **事件日**複驗：Broadcom JSON-LD `"datePublished": "2026-06-24T09:00:48-0400"`；
  OpenAI 頁面 meta 區印 `June 24, 2026`，RSC payload 也帶 `"publicationDateText":"June 24, 2026"`。
  第一輪對 `event_date_basis` 的更正屬實。
- **查核日五處一致**（內容包三條 source、研究紀錄三條、正文第二段、表格 caption、圖解 caption），
  沒有因為第二輪重查而更動。圖解四格、`hero_label`、`hero.alt` 未動。
- **界線（第 8 個點名疑點）全數乾淨**：沒有 AVGO 股價、營收、估值或利多語氣；
  沒有把這件事寫成與 Nvidia 的輸贏（FAQ 第 2 題直接寫「官方文章沒有回答這個問題」）；
  `topics` 是 `ai／gadgets／ai-news`，**不帶 `finance`**；**只有一個 callout**；
  沒有購買建議、推薦式比價、「我們試用」語氣，也沒有推定台灣可用。

### 留給站主的 3 件事（第一輪那 6 件仍然有效）

1. **段落總字數 2,975 → 2,984／3,000，只剩 16 字。**
   這 11 處改動**沒有刪掉任何但書或限定詞**；多出來的 9 字是第 4 點那個必要的正文落腳點
   （+13）扣掉第 2 點的縮寫（−12）與其他增減。之後要加句子，只能從**重複的敘述**騰字。
2. **FAQ 第 6 題引用了 blank-slate 那一句**（「不是從過去其他 AI 工作負載改造而來的通用型加速器」）。
   這句話一手來源逐字成立，但**它沒有出現在中文正文裡**，嚴格說不符合「FAQ 的答案 ⊆ 正文」。
   補進正文約需 30 字，字數只剩 16 字，所以沒有動——改寫、補進正文或刪掉，請站主決定。
3. **第一輪留下的第 3 件（Broadcom 條列少 `substantially` 要不要寫進正文）建議不必補。**
   文章引用的是兩頁逐字相同的內文句，沒有踩到那個落差；落差本身已完整記在研究紀錄裡。

### 自檢最後輸出

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-chatgpt-storage-scale-20260911
```

（與第一輪、與本次編輯前**完全相同**的兩條允許保留的 FAIL；兩個結尾連結依規格未動。）

### 第二輪結論

`needs_owner`：118 條主張複核後**沒有任何一條被來源推翻**，骨幹（同一份文稿的共同段落、兩個標題、
9 個月只到 tape-out、部署只是規劃、廠商宣稱與前瞻性陳述要分開）全部站得住，
第一輪自己點名的三件事今天也全部複驗通過。改掉的 11 處集中在
**否定句範圍**（三處會把 2025-10-13 那份的時程與規模掃進去）、
**一處漏改的時程主詞**（FAQ 第 4 題的 2029 年底）、**一處全稱說法**、**一處表格英文與中文不同源**，
以及**兩處把來源的 `cheaper to build` 與 `can show up as` 寫得比原文肯定的措辭**，
都是句子層級的修正。擋住 gate 的仍然只有兩個結尾連結的 title，由協調者處理。
