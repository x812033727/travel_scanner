# 獨立查核：ai-news-astra-for-law-20260917

查核代理：未參與撰稿。查核日 **2026-09-18**（與草稿的 `checked_on` 同一天，未更動）。
查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，用 Python 剝掉
`<script>`／`<style>` 後去標籤、**不補空白**，再逐條比對 `verbatim_quote` 是不是可以連續搜尋到的字串。
**沒有使用 `sources[]` 以外的任何網址替文章補事實**；請求的 UA、標頭與查詢字串都沒有放入任何 email 或個人資料。

檢查的主張：約 **146** 條（title、description、正文 16 段、摘要 4 句、表格 6 列 24 格與 caption、
圖解 caption 與四格、FAQ 6 題答句、callout、兩條 link）。**改了 28 處**，另有 4 件留給站主。

## 重抓結果（三條都讀到正文）

| source | HTTP | bytes | body 是正文？ | 驗到的東西 |
| --- | --- | --- | --- | --- |
| `openai.com/index/astra-for-law/` | 200 | 516,164 | 是（去標籤後 20,135 字） | 日期列、定位句、索引句、評測三句、可用性句、模型代號、兩項資料條款、Latham 與 Wachtell 兩段、外掛 26／9／47、ChatGPT for Word、結尾接洽句 |
| `openai.com/index/cooley-gopublic/` | 200 | 382,574 | 是（7,415 字） | 同日日期列、「an international law firm」、GO Public built on ChatGPT Work、2025 年 180 件／515 億美元 |
| `openai.com/business/plugins/?tab=plugins-legal` | 200 | 2,025,068 | 是（5,900 字） | 篩選列含 Legal、外掛的一般說明句 |

位元組數與撰稿者記錄的 516,162／382,570／2,025,061 相差 2～4 bytes，屬於已知漂移，內容相同；
**不可拿位元組數當版本識別**。前期研究紀錄擔心的 `openai.com/index/*` 403 今天沒有重現。
32 條 `verbatim_quote` 全部通過連續字串比對（含 U+2011 的 GPT‑6 Astra 與評測句的 en dash）。

## 改掉的 28 處（最重的先列）

1. **治理合作對象寫錯人：Wachtell → Latham & Watkins**（第 4 節第 2 段）。
   原文是 “We are also working with **Latham & Watkins**, a leader in AI governance, to design for
   information permissions, ethical walls, client instructions, and firm oversight.”
   草稿把這四個治理項目掛到了 Wachtell, Lipton, Rosen & Katz 身上——那是公告**最後一節另一段**、
   另一家事務所的另一件事（用字是 explore 探索，不是 design for）。兩段相隔數百字，
   頁面上 Latham 出現 3 次、Wachtell 2 次。已改成 Latham 做治理設計、Wachtell 是一起探索，兩件事分開寫。
   **這一條是前期研究紀錄寫對、撰稿階段寫錯的**，`verbatim_quote` 也補成完整句子。
2. **檢索 54% 掉了兩個條件**（第 3 節第 2 段、摘要第二句）。原文是
   “**On the audited set of target passages**, it retrieved up to 54% more relevant passages
   **from the correct court opinions**, when comparing the systems at the same reasoning effort.”
   草稿三個條件只留了「相同推理量」。已補回「經稽核的目標段落集合」與「來自正確法院意見書」。
3. **「申請管道公告全部沒有寫」被來源自己推翻**（第 4 節第 1 段）。公告結尾寫著
   “To explore early access to Astra for Law, build it into your product, or develop tools around
   your firm’s expertise, **contact OpenAI**.” 這是一條寫明的接洽管道。
   連帶地，**全篇 13 處「受邀」改成「選定」**：公告用的是 selected law firms 與 eligible law firms，
   整頁 `invite`／`invited` **出現 0 次**，「受邀才能用」是草稿加上去的機制推論。
   兩者合在一起會讓台灣讀者以為連問都不能問。已改成沒有寫的是合資格標準、規模與名額，
   並把那條管道寫進正文與摘要。（`hero.alt` 依規格不動，留給協調者。）
4. **「OpenAI 表示這不是新模型」是官方沒說過的話**（description、摘要第一句、第一段、第 1 節、FAQ 1）。
   公告全文 `new model` 與 `train` **各 0 次**；OpenAI 只寫了正面的定位句
   “Our most powerful model, configured into a new AI foundation for law.”
   「不是新模型」是本文的閱讀，不是官方的陳述。五處一律改成官方自己的說法，
   並補上它在模型選單裡有自己的名字「GPT‑6 Astra Law」、API 代號 `gpt-6-astra-law`，讓讀者自己判斷。
5. **「公告列出的每一類都加上 U.S.」不成立**（第 2 節第 1 段、FAQ 2）。原文只印一次
   “search **U.S.** case law, statutes, regulations, court rules, and administrative decisions”，
   以 U.S. 起頭涵蓋整串清單；全篇 `U.S.` 共 3 次（索引清單、99.9% 判例、200 題）。
   **這一條前期研究紀錄就寫錯（“Every item … is prefixed 'U.S.'”），草稿照抄。**

其餘 23 處（同樣逐條回原文）：

6. 54.0% 的主詞改成「在 54.0% 的題目通過評測的**整體正確性檢查**」，不再寫成「整體正確率是 54.0%」；
   38.7% 的比較對象與「40% 的相對進步」原本正確，未動。
7. 47 項自訂技能改掛在 9 個社群外掛上（原句 “9 community plugins … **with 47 custom skills**”），
   不是 26＋9 共帶來 47；正文與表格兩處。
8. 「頁面引用的律師與事務所評語**都是**早期測試、這個階段」收窄成公告裡直接評論 Astra for Law 的
   **兩段**引言（頁面自己標 1 of 2），並照原文寫出「preview early versions」「at this early stage」
   「In our early testing」；同頁 Latham、Cooley、Thomson Reuters、Ropes & Gray、Wachtell 的引言
   講的是合作與策略，不是早期測試。
9. Cooley 由「美國律師事務所」改為「國際律師事務所」（原文 “Cooley is an **international** law firm”）；
   「2025 年全球處理 180 件交易」改為「為全球 180 件交易**提供顧問**」（advised on）。
10. 外掛目錄的「**八個**類別」拿掉：個數是數出來的、頁面沒有印，而且那是沒有日期的活頁面。
    改成標明 2026-09-18 讀取時點、只列部分類別並加「等」。
11. 「**三個**百分比都只在官方自訂的測試條件下成立」改成「這**四個**百分比」——文章實際引用了四個。
12. 兩處 `sources[]` 外的事實改寫成站內互引：GPT‑6 Astra 的「2026 年 9 月 3 日發布」與金融機構版
    「用同一個模型打造」都不在三條來源裡，改成公告自己的形容（最新、最強大）與本站既有文章的事件日。
13. 「分析結果可以追回原始的判例或條文，讓**使用者**自己核對」改成官方原句的說法（研究基礎更紮實、
    附上「**律師**可以自己查看的可靠出處」），並刪掉把 Ropes & Gray 自家系統的
    “trace findings back to the source” 混進來的成分。
14. 「等於點名自己和既有法律資料庫供應商是互補，不是競爭」這個推論，改成引官方自己那句
    「在 OpenAI 上建置應該是從生態系得到更多，而不是取代它」。
15. 「公告裡**唯一**跟一般讀者直接有關的事」的「唯一」拿掉；「公告**全文**沒有提到一般 ChatGPT 個人帳號」
    改為「公告**內文**」，把頁尾全站導覽排除在否定句的範圍外。
16.–28. 表格三列（模型、Trusted Access 兩格、外掛與社群技能）、第 4 節標題、摘要三句、
    FAQ 1／2／3／6、callout、圖解 alt 隨上述各條連動改寫；另有 6 處純為字數精簡的刪冗。

**字數**：補回條件之後 zh-TW 段落一度到 3,071 字（上限 3,000），
改以刪除與第一段重複的敘述與冗詞回到 **2,970** 字，
**沒有為了湊字數刪掉任何但書、限定詞或條件**。

## 查過而且正確的部分（沒有動）

- **本篇最容易寫錯的兩件事，草稿都寫對了**：Cooley 的 GO Public 建立在 **ChatGPT Work** 之上（客戶案例頁原文），
  而公告介紹三家事務所客製應用程式那一段官方用的字眼是「**調整 ChatGPT Enterprise**」，不是 Astra for Law；
  2025 年的 180 件／515 億美元也沒有和任何 AI 成果建立因果關係，並明寫那是事務所整體業務規模。
- **地域沒有混寫**：索引是美國、可申請地區官方未說明，兩者在正文、表格、FAQ 三處都分開寫，
  沒有推定台灣可用，也沒有反過來推定只限美國事務所。`region`／`country`／`Taiwan` 在公告內文各 0 次。
- **索引本身**：美國判例、法規、法院規則與行政決定，超過 2.3 億筆網址、每日新增，
  Free Law Project／CourtListener 與「超過 99.9% 已公布的美國判決先例」，全部與原文相符且歸因給官方。
- **兩項資料條款**（API 端零資料保留、ChatGPT Enterprise 用量預設不納入人工審閱）都寫明限於合資格事務所，沒有外溢。
- **界線**：沒有購買建議、沒有推薦式比價、沒有與 Harvey／Legora／Thomson Reuters 的競品比較、
  沒有法律意見、沒有「我們試用」；效能與評測數字一律帶「官方表示」。
  AI 篇只有**一個** callout、沒有投資免責段落，也沒有掛 `finance` 主題。
- **未定狀態都在**：先給選定事務所、API「即將開放」沒有時間表、治理設計還不是公開標準、
  ChatGPT for Word 只寫全面開放而沒有方案／地區／語言（`language` 在公告內文 0 次）。
- **日期分開寫**：事件日 2026-09-17 與 slug 尾碼、`news_date`、正文第一段一致；
  Cooley 的 2025 年數字、ChatGPT for Word 的同日開放與事件日三者沒有混用。
  `checked_on` 2026-09-18 在內容包三條 source、研究紀錄、第二段、表格與圖解 caption 一致，**未更動**。
- 與既有 `ai-news-chatgpt-financial-services-20260910` 沒有矛盾、沒有重寫它的題目；
  第二條 link 的 text 與該內容包 zh-TW title 逐字相同。
- 摘要四句的每個數字都在正文出現；FAQ 六題答案都是純文字、沒有連結；圖解四格沒有數字；全文沒有簡體字；
  內容包 9 處 `GPT‑6` 全是 U+2011，沒有混入 ASCII 連字號。

## 留給站主的 4 件事

1. **第 4 節的治理段現在同時出現 Latham & Watkins 與 Wachtell 兩家事務所**，比原稿長。
   若覺得一般讀者不需要兩家，刪掉 Wachtell 那半句即可——但 **Latham 那半句不能再換回 Wachtell**。
2. **公告另有一個沒有寫進文章的數字**：最高推理量下、以判例為主的題目，找到的參考判例多 **24%**
   （已補進研究紀錄）。目前段落 2,970／3,000 字，要補得從別處刪等量的字，是編輯取捨。
3. **外掛目錄是沒有日期的活頁面**，出刊當天若要保留那句類別敘述，需要再讀一次確認篩選列沒有變。
4. **`hero.alt` 仍寫「受邀事務所」**，依規格查核代理不動；協調者依實際主圖改寫 alt 時，
   請一併改成「選定的事務所」，以免與正文不一致。

## 自檢

```
OK ai-news-astra-for-law-20260917 zh-TW paragraphs 2970
```

沒有任何 FAIL（索引與相關文章兩條 link 的目標都已存在，text 也與目標 title 逐字相同）。

## 結論

`needs_second_round`：文章經約 146 條主張逐條核對後，28 處已改，事實層級的修正超過十處，
而且動到骨幹敘述（治理合作對象換人、可用性從「受邀才能用」改成「選定＋公告留有接洽管道」、
「不是新模型」從官方陳述改為官方沒有這樣說）。
第二輪請逐句回來源查**本輪新寫進去的每一句**，特別是第 1 節的模型代號那句、
第 3 節第 2 段的兩個新條件、第 4 節第 1 段的接洽管道句與第 2 段的 Latham／Wachtell 兩段。

---

## 第二輪

第二輪查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 未更動）。
`sources[]` 三條自行以 `curl -sL -A "Mokaair-editorial"` 重抓，請求的 UA、標頭與查詢字串都沒有放入任何
email 或個人資料；**沒有使用 `sources[]` 以外的任何網址替文章補事實**。
覆核範圍是第一輪改動過的 28 處段落、第一輪新寫進去的每一句，以及 32 條逐字引文的程式比對，
**約 60 條**主張。**又改了 12 處**（內容包 9 處、研究紀錄 3 類）。

### 重抓結果（三條仍是自己讀到的正文）

| source | HTTP | bytes | 與第一輪差 | body 是正文？ |
| --- | --- | --- | --- | --- |
| `openai.com/index/astra-for-law/` | 200 | 516,160 | −4 | 是（去標籤後 20,025 字） |
| `openai.com/index/cooley-gopublic/` | 200 | 382,573 | −1 | 是（7,310 字） |
| `openai.com/business/plugins/?tab=plugins-legal` | 200 | 2,025,111 | +43 | 是（5,793 字） |

位元組數三輪都在漂移（撰稿者→第一輪→第二輪），內容相同；**不可拿位元組數當版本識別**。
`openai.com/index/*` 的 403 第二次也沒有重現。外掛目錄今天的篩選列與第一輪記錄**逐字相同**
（All、Small Business、Productivity、Engineering & IT、Data & Research、Legal、Design & Creative、
Finance、Sales & Commerce），正文那句「2026-09-18 讀取時…等」仍然成立。

### 逐字引文

32 條 `verbatim_quote` 用「剝掉 `<script>`／`<style>` → 去標籤 → **不補空白**」的正文做連續字串比對，
**32 條全部 `count >= 1`**；沒有任何一條含 `...`、`…` 或 `|`，因此沒有拼接引文要逐片段拆。
唯一 `count = 2` 的是 Harvey 那句（第 25 條），比對頁面發現是輪播元件把兩段引言各渲染兩次，
不是引文被拼在一起。第二輪另外新增 2 條，共 **34 條，全部通過**。

### 指派訊息點名的八件事

| 疑點 | 結果 |
| --- | --- |
| (a) Latham 治理／Wachtell 探索是否分開 | **通過**。Latham 在 Legal-grade trust and controls 一節拿四項治理設計（`design for`），Wachtell 在最後一節 Build with us、用字是 `explore`；`Latham` 3 次、`Wachtell` 2 次，正文、表格、FAQ 沒有再混 |
| (b) 檢索 54% 的三個條件 | **通過**。`On the audited set of target passages`、`from the correct court opinions`、`at the same reasoning effort` 加上 `up to`，四者在第 3 節第 2 段與摘要第二句都在 |
| (c) 「受邀」→「選定」 | **通過**。內容包 `受邀` 只剩 **1 處**，就是 `hero.alt`（依規格不動，見下方留給站主）；title、description、summary、表格、FAQ、callout、圖解 alt、第 4 節標題全部是選定／合資格。`invite`／`invited`／`invitation` 全頁各 **0 次**，`selected` 3 次、`eligible` 2 次。**但研究紀錄有 4 處殘留，已改**（見下） |
| (d) 「不是新模型」五處＋模型選單名／API 代號 | **通過**。`new model` 0 次、`train` 0 次；五處都是官方定位句。10 處 `GPT‑6` 全是 U+2011，`gpt-6-astra-law` 2 處全是 ASCII 連字號。FAQ 1 的時態已修（見改動 4） |
| (e) `U.S.` 只印 3 次、起頭涵蓋整串 | **通過**。全頁 `U.S.` 3 次（索引清單、99.9% 判例、200 題），索引清單只在句首印一次。研究紀錄 `verified_facts` **沒有**殘留舊的「每一類都加 U.S.」寫法 |
| (f) 地域三處分開寫、不推定台灣 | **通過**。`region`／`country`／`Taiwan` 各 0 次；正文第 2 節、表格 Trusted Access 列、FAQ 第 3 題三處都把「索引範圍」與「申請資格」分開，沒有任一方向的推論 |
| (g) 分批開放／即將開放／未定狀態詞 | **不通過，已改 4 處**。原文是 `will be initially offered`／`will be coming soon`，公告當天尚未開通；草稿的「先開放給」讀起來像已上線（見改動 3） |
| (h) 2,961／3,000 字、加字須等量刪減 | **通過**。淨變化 −4 字（刪 18、加 14），**沒有刪掉任何但書、限定詞或條件**；本輪新增的兩處反而都是補限定 |

### 又改掉的 12 處

內容包 9 處：

1. **把不屬於官方的對比從「官方的說法」裡拿掉**（第 2 節第 3 段）。原句是
   「官方的說法是研究基礎更紮實，會附上『律師可以自己查看的可靠出處』，**而不是只給流暢卻可能編造依據的答案**」。
   公告原文只寫到 “The result is a stronger research foundation … with reliable authorities the lawyer can
   examine for herself.”，**完全沒有提編造引註**。這是第一輪新寫進去、歸因過頭的半句，已刪；
   同一段下一句本來就把這層意思寫成本文自己的觀察，讀者拿到的訊息沒有少。已另立 `verified_fact` 存原句。
2. **「律師引言」→「外部引言」**（第 3 節第 3 段）。那兩段引言之一的 Niko Grupen 是
   **AI 公司 Harvey 的 Head of Applied Research，不是律師**（另一位 John Savva 才是 Sullivan & Cromwell 合夥人）。
3. **可用性補成未來式，4 處**（description、摘要第三句、表格 Trusted Access 列、第 4 節第 1 段）。
   原文 “Astra for Law **will be** initially offered to selected law firms … and **will be coming soon** to the API.”
   ——公告當天還沒開通，「先開放給選定的事務所」讀起來像已經上線。已一律改為「將先開放給…」。
4. **FAQ 1「在模型選單裡有自己的名字」→「會顯示成」**，對齊原文 “It **will appear** in the model picker as”。
5. **「付費」是推論**（第 2 節第 2 段）。原文是 “complements the **licensed content and specialist products**
   firms rely on”，沒有寫付費。改成「補充事務所既有的授權內容與專門產品」。
6. **否定句限縮回公告**（第 4 節第 2 段）。「兩者都還不是公開的標準」改成
   「公告把兩者都寫成進行中的合作，還不是公開的標準」——Latham 是 `to design for`、Wachtell 是 `to explore`，
   都是進行式，這樣才是「這一頁怎麼寫」而不是對世界的斷言。
7. **摘要第三句的「只有一條管道」**改成「公告寫明可以與 OpenAI 聯絡，但…」。頁首另有
   `Contact Legal sales` 入口，摘要裡不設範圍的「只留下…這一條」不成立；
   正文「公告**結尾**只留一句」有限定在結尾，正確，未動。
8.–9. 上述 3 與 7 連帶的 description 與表格格內文字。

研究紀錄 3 類（第一輪只改了內容包、沒有回頭改自己的紀錄）：

10. **`受邀` 殘留 4 處**：`verified_facts` 的使用資格那條、`not_said` 第 1 條、
    `unverified_or_excluded` 第 5 條、`must_not_write` 第 2 條。第一輪報告寫「全篇 13 處已改」，
    指的只是內容包。已全部改成選定／可申請，並在該條 fact 補上詞頻與未來式的提醒。
11. **`must_not_write` 第 11 條仍寫「頁面上所有引言都是受訪者自己的早期測試印象」**——
    第一輪已在正文推翻這個全稱（改動 8），卻沒有回頭改這條**拘束句**，等於留著一個會讓
    後續譯稿或改寫再犯一次的陷阱。已改寫成兩段引言的實況，並註明其中一位不是律師。
12. **「外掛目錄有八個產業類別」殘留 2 處**（`unverified_or_excluded` 第 6 條、`must_not_write` 第 8 條）。
    第一輪把這個數出來的數字從正文拿掉了，兩條理由句卻還留著；已改成不帶個數的寫法。
    另新增 2 條 `verified_fact`：第 2 節第 3 段依據的官方原句（第一輪寫了句子沒留引文），
    以及公告開頭「法律事務所**與法律科技公司**」＋點名 Harvey／Legora 等 API 客戶那句。

### 覆核無誤、沒有再動的部分

- 第一輪五項骨幹修正（Latham／Wachtell、54% 三條件、受邀→選定、「不是新模型」、U.S. 只印一次）**全部複核成立**。
- **狀態詞逐一對來源**：26 個夥伴外掛與 ChatGPT for Word 是 `today`（已開放）、
  Trusted Access 與 API 是 `will`／`coming soon`（未開放、無時間表）、治理設計與 Wachtell 合作是進行式；
  本輪把前後不一致的四處補成未來式後全部對齊。
- **界線**：沒有購買建議、沒有推薦式比價、沒有投資免責 callout（全篇只有一個 `info` callout）、
  沒有 `finance` 主題、沒有法律意見、沒有「我們試用」，效能與評測數字一律歸因。
  值得記一筆的是公告頁尾附了一段與 **Claude Fable 5.1** 的同題輸出比較（官方自評對手引到已被上級法院推翻的判決），
  文章**完全沒有引用**，符合不做競品比較的界線。
- **第二個結尾連結**：`ai-news-chatgpt-financial-services-20260910` 的既有內容包今天打開核對，
  zh-TW title 與 link text **逐字相同**，事件日 2026-09-10 與正文「一週前」相符；
  `ai-news-gpt-6-astra-20260903` 也存在、`news_date` 是 2026-09-03，第 1 節第 3 段的事件日互引成立。
  兩篇都沒有被本文改寫，也沒有矛盾。第一個連結的文字與 DELTA-4-5 指定的索引標題逐字相同。
- 摘要四句的數字都仍在正文出現；FAQ 六題答案都是純文字；圖解四格沒有數字；沒有簡體字；
  `checked_on` 2026-09-18 在內容包三條 source、研究紀錄、正文第二段、表格與圖解 caption 一致，未更動。
- 價格、可申請地區、API 時間表、個人帳號四個否定句今天再驗一次：
  `price`／`pricing`／`cost`、`region`／`country`／`Taiwan`、`language`、`personal account` 在公告內文**各 0 次**。

### 留給站主的事

1. **`hero.alt` 仍寫「受邀事務所」**，第二輪同樣依規格不動。這是內容包**最後一處**與正文不一致的用詞，
   協調者重畫主圖改寫 alt 時**務必**一併改成「選定的事務所」。
2. 第一輪留下的三件事（Latham/Wachtell 兩家是否都保留、要不要補 24% 那個數字、出刊當天要不要重讀外掛目錄）
   第二輪沒有替站主決定，維持原狀。目前 **2,961／3,000** 字，補 24% 那句約需 30 字，空檔剛好夠，仍是編輯取捨。
3. 文章沒有寫出公告點名的 API 客戶（Harvey、Legora）與「法律科技公司」這一類對象，是字數取捨；
   已寫進研究紀錄並標明——日後若擴寫，**不可**反過來寫成只有法律事務所能用。

### 自檢

```
OK ai-news-astra-for-law-20260917 zh-TW paragraphs 2961
```

沒有任何 FAIL（依 DELTA-4-5 第 3、4 條，索引標題不改、第二個連結指向既有文章，
所以第一輪規格裡允許的那兩條 FAIL 本來就不該出現，實際也沒有出現）。

### 結論

`ok`。第二輪覆核約 60 條、又改 12 處，**沒有再發現骨幹層級的錯誤**；
本輪的 12 處都是歸因邊界（官方說的 vs 本文的讀法）、時態（未來式被寫成已上線）、
與第一輪只改內容包沒回頭改研究紀錄的殘留。三個檔以外沒有動任何 repo 檔案。
