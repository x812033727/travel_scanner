# 獨立查核：ai-news-nvidia-hugging-face-20260903

查核代理：未參與撰稿。查核日 **2026-09-18**（與草稿的 `checked_on` 同一天，未更動）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，PDF 以系統 python
的 pypdf 6.16.2 抽 5 頁。NVIDIA 公告用 `<p>`／`<li>`／`<h*>` 逐塊抽出並記下**每一塊在原始碼的位元組位置**，
用位置重建原文順序；研究紀錄 30 條 `verbatim_quote` 以 NFKC 加引號／連字號／空白正規化做連續字串比對。
**沒有使用任何 `sources[]` 以外的網址替文章補事實**，也沒有猜任何網址。

檢查的主張：**約 118 條**（正文 17 段、summary 4 句、表格 5 列 15 格與 caption、圖解 caption 與 alt、
FAQ 7 題的答句、callout、title、description、研究紀錄 `diagram` 四格與 `hero_label`），
外加研究紀錄 30 條逐字引文。**內容包改了 19 處、研究紀錄改了 6 處**，另有 12 處純為字數的敘述精簡
（沒有刪掉任何但書或限定詞），3 件留給站主。

## 重抓結果（四條 sources 都還在、位元組數與紀錄完全相同）

| source | HTTP | bytes | body 是正文？ | 驗到的東西 |
| --- | --- | --- | --- | --- |
| blogs.nvidia.com 收購公告 | 200 | 109,596 | 是，`<article>` 16,886 bytes 完整 | 交易金額；四項承諾；平台五個數字；三個貢獻數字的真實版面與順序；`article:published_time` 2026-09-03T11:56:49+00:00、`article:modified_time` 2026-09-03T20:54:05+00:00；byline `September 3, 2026 by Jensen Huang`；內文唯一超連結 `open model` |
| huggingface.co 2026-07-16 揭露 | 200 | 575,348 | 是，`datePublished` 2026-07-16 | 事件範圍那兩段 |
| huggingface.co 2026-07-27 技術文 | 200 | 725,774 | 是，`datePublished` 2026-07-27 | TL;DR；五個資料集的影響範圍句；Claude Opus／Fable 拒絕分析那一段；`wrongly` 仍在 |
| images.nvidia.com 公開信 PDF | 200 | 801,845 | 是，5 頁，第 4、5 頁空白 | `July 24, 2026` ×1；`Huang`／`Jensen` 各 **0** 次；無作者署名；風險與「禁止不是正確回應」那段 |

活資料另外重抓一次（**不進 `sources[]`**，只用來重驗正文那句已寫明查法的否定句）：
`huggingface.co/blog` 200／296,864、`/blog/community` 200／136,143、`/clem/activity/posts` 200／546,059，
三頁對 `acqui` 不分大小寫**今天皆 0 命中**。後兩頁比上一輪少 105／190 bytes——頁面漂移，
**位元組數不可當版本識別**。

## 改掉的 19 處（最重的排前面）

1. **「兩段話」「下一段」把公告的版面說錯，而那一段的論點就是順序**（第 3 節第 2 段）。
   `NVIDIA is the largest contributor…` 與 `NVIDIA has released more than 500 models…`
   **不是兩個段落，是同一個 `<ul>` 裡連續的兩條 `<li>`**（原始碼 59199、59323，之間還有第三條
   `We build our own models, libraries and tools in the open…`）；而草稿當成「另外一段」的
   第三人稱「hundreds」那一句，其實是**排在它們之前的一個 `<p>`**（58845）。
   草稿寫「同一份公告因此前後出現 500 個以上、250 個以上與數百個」，把真實先後倒過來了。
   已改成「先是一段第三人稱寫成的文字…緊接著才用條列，第一條…第二條才給出具體數字…」，
   結尾也改成「因此出現數百個、500 個以上與 250 個以上三種說法」。
2. **「黃仁勳接著把這件事接到一項政策主張」順序相反**（第 3 節第 3 段）。
   `Open models let startups, businesses, universities and public institutions…` 在原始碼 58367，
   **早於**三個貢獻數字（58845／59199／59323），也早於「AI advances faster when people can build together.」。
   已改成「在這些貢獻數字之前，黃仁勳已經先把開放模型接到一項政策主張」。
3. **一個指向不存在文章的交叉引用**（第 5 節第 3 段）。草稿寫
   「完整經過本站另一篇文章已從 Anthropic 執行長 Amodei 的角度整理過，這裡不重複」。
   站上沒有這篇：`content/` 目錄搜 `security-incident-july-2026`／`agent-intrusion-technical-timeline`／
   `ExploitGym` 只命中本篇自己，`ai-news-*amodei*` 無檔案，唯一沾邊的
   `ai-news-anthropic-threat-report-20260910` 全文 `Amodei`／`Hugging Face`／`鑑識` 各 0 次。
   **整句刪掉**（文章結尾第二個連結本來就指向 Astral 那篇，不是它）。
4. **「商用前沿模型的安全防護擋下了鑑識分析需要的大量攻擊指令」不是來源說的事**
   （第 5 節第 3 段與 FAQ 第 6 題，兩處）。原文是
   `The models we reached for first, Claude Opus and Fable, refused a large part of that work:
   their safety guardrails treated reverse-engineering an exploit the same as launching one.`
   ——被拒絕的是**鑑識工作本身**，不是「攻擊指令」；而且原文**具名兩個模型**，不是泛指商用前沿模型。
   已照原文改寫成「最先動用的 Claude Opus 與 Fable 兩個模型因為安全防護把逆向分析漏洞視同發動攻擊，
   拒絕了鑑識工作的很大一部分」（FAQ 因篇幅寫成「最先動用的兩個模型」）。
5. **FAQ 第 1 題以「沒有。」斷定交易狀態**。四條來源只撐得起
   「公告寫的是 `has agreed to acquire`，整頁 `completed`／`definitive agreement`／`closing` 各 0 次」，
   **撐不起查核日當天這筆交易是否已完成**。已改寫成照原文的說法，並明寫
   「本文四條來源裡沒有任何一條說明這筆交易後來是否完成」。這是併購題目最容易寫過頭的一句。
6. **資安那一段少了影響範圍**（第 5 節第 3 段，`must_add`）。只寫「入侵了部分正式環境基礎設施」、
   不寫官方講的範圍，對讀者是誤導。已補上 2026-07-27 技術文的原句改寫：
   「唯一被讀取的客戶內容是五個資料集，其他面向使用者的模型、資料集、Spaces 與套件都未受影響」。
   **沒有**補進任何攻擊手法、入侵向量名稱、逐日次數或階段表（`tech.md` 的界線）。
7. **FAQ 第 6 題把公告的論點掛到那封 PDF 上**：「呼應黃仁勳信裡開放權重能強化資安的論點」。
   `strengthen cybersecurity` 出現在**公告段落**（58367）；把主張歸給那封信等於認定黃仁勳是信的作者，
   正是 `must_not_write` 第 11 條禁止的。已改成「黃仁勳在公告裡『開放模型能強化資安』的說法」。
8. **時刻的出處沒有交代，而修改時間是活資料**（第 1 節第 1 段）。11:56 與 20:54 **只存在於 HTML 中繼資料**，
   頁面上看得到的只有 `September 3, 2026`。已寫出 `article:published_time` 與 `article:modified_time`
   兩個欄位名、註明查核日重讀仍是同樣的值，並補上「後者是頁面當下狀態，不是事件日」。
   兩個台北時間換算重算無誤：11:56:49 UTC → 9/3 19:56、20:54:05 UTC → **9/4 04:54（跨零時）**。
9. **公開信的否定句沒有寫查法**（第 5 節第 2 段）。已改成
   「以查核日抽取的這份 PDF 全文搜尋，找不到 Huang 或 Jensen，文件也沒有列出任何作者署名」，
   把否定限縮到**本文引用的這一份檔案與這一次的查法**。
10. **「創辦團隊」「共同創辦人 clem」「創辦人」沒有來源**（第 1 節、第 4 節、summary、FAQ 2、callout 共 5 處）。
    四條 `sources[]` 沒有任何一條寫 Clem／Julien／Thomas 的職稱，公告連姓氏都沒有
    （`Delangue`／`Chaumond`／`Wolf` 在整頁各 0 次，`founder`／`co-founder` 在 `<article>` 內 0 次）。
    已改成「公告只用這三個名字，沒有寫出姓氏，也沒有寫出他們在公司的職稱」與「站上 clem 帳號的動態頁」。
11. **summary 第 4 句比正文的查核範圍大**：「Hugging Face 自己還沒有針對這筆收購發表任何聲明」。
    已加上查了哪三頁與「未見」的句型；正文、summary、FAQ、callout 現在**四處一致**寫同樣三個頁面
    （正文原本只寫兩頁、研究紀錄寫三頁）。
12. **「20 萬以上的合作公司」把使用者寫成合作夥伴**（FAQ 5、圖解第四格、圖解 alt、研究紀錄 `diagram`）。
    原文是 `More than 200,000 companies **use** the platform`。已改成「使用平台的公司」／「使用企業」。
13. **「公告裡最具體的是四項承諾」的「四」是本文的歸納**，公告沒有編號。
    已改成「公告裡最具體的說法，本文整理成四項承諾」。
14. **兩個負面句範圍過寬**：「公告沒有寫出任何季度或年度」→「沒有**為這筆交易**寫出任何季度或年度」
    （同一頁的 GTC 推廣區塊印著 `October 20-22`）；「公告**全文**只在開放模型這個詞上放了一個連結」
    →「公告**內文**」（`<article>` 內另有 byline、分享與推廣連結）。
15. **FAQ 第 7 題有一句沒有來源的斷言**：「Hugging Face 是一個網站與服務，台灣的使用者原本就可以直接使用」。
    已刪掉，改成照原文寫「公告沒有提到任何國家或市場…全文只用到全球、世界各地這類泛稱」
    （`American`／`U.S.`／`United States`／`Taiwan`／`China`／`Europe`／`market` 在內文皆 0 次）。

研究紀錄另外改了 6 處：`verified_facts` 第 4 條把「200 萬以上（原文 more than 200,000）」這個自相矛盾的
中文敘述改回 **20 萬**並加註不可寫成「合作公司」；第 8、9、10、12 條補上真實的版面型態（`<ul>`／`<li>`）
與原始碼位置；`sourcing_notes` 的 `Huang`／`Jensen` 次數由 18／14 更正為今天的 **11／9** 並標明那是活值、
差額全在會換內容的「相關文章」區塊，**而且其中兩處落在 `<article>` 之內**（文章自己的 byline 與作者連結），
不是紀錄寫的「只在導覽列」；`diagram` 第四格改為「使用企業」。
新增 `factcheck` 欄位記錄方法、19 條 `edits_to_the_pack`、12 條 `checked_and_correct` 與 4 條 `left_for_the_owner`。

## 查過而且正確的部分（沒有動）

- **30 條 `verbatim_quote` 逐條做連續字串比對，26 條原樣命中。** 第 17 條（公開信定義句）唯一的差異是
  pypdf 抽出來的 `Open  weight`（雙空白）與 `modify ,`（逗號前空白），是**抽取器的字距假影、不是文件的字**，
  紀錄的寫法比抽取結果更貼近原件，維持不動。
- **`must_fix` 3 的順序顛倒沒有重演，但同樣的型態還在四條上**：第 11、20、23、26 條用刪節號接起原文
  兩段不相鄰的文字。逐段驗過——四條的兩個片段都各自逐字命中，**先後順序也與原文一致**
  （35891→38695、3263→3540、5870→6428、35609→35865）。見「留給站主」第 2 點。
- **`must_fix` 1／2／4／6／7／9／10 都確認已照改**：全文沒有任何簽署數、沒有寫 Anthropic 拒簽；
  meta description 記成完整兩句；`wrongly` 保留；黃仁勳與那封信拆成兩條、不合併；
  標題／日期不再用 `/` 拼接；4.5 天與 2.5 天兩個數字都記；GLM-5.2 兩個型號記成不矛盾。
- **監理與時程的否定句今天重驗仍成立**：`regulatory`／`antitrust`／`approval`／`closing`／`subject to`／
  `customary`／`forward-looking`／`signator` 在整頁 HTML 皆 **0** 次；`billion` 0 次
  （所以「全文沒有另外換算成約 129 億美元」成立）；`brand` 在 `<article>` 內僅 **1** 次
  （所以「與品牌有關的說法只有一句」成立）。
- **平台五個數字逐字無誤**（18M／3M／500,000／1M／200,000），文章與圖解都寫成 NVIDIA 自陳、未附截止日期。
  圖解四格與 `hero_label` 的每個數字都在正文出現；summary 四句的每個數字都在正文出現。
- **四項承諾逐句對照原文無誤**，包含
  `NVIDIA compute will not be required to build on or deploy through Hugging Face.`
- **「執行長」有依據**：頁面 JSON-LD 的作者簡介印著 `president, chief executive officer`，在 `sources[0]` 之內。
- **`must_not_write` 十三條逐條比對，文章都沒有踩到**：沒有監理審查預測、沒有完成日期、沒有交易結構、
  沒有把承諾或引言歸給 Hugging Face 一方、沒有 8-K、沒有 OpenAI 2026-08-26 那篇的內容、
  沒有把收購說成資安事件造成的。
- **界線**：全文沒有購買建議、沒有推薦式比價、沒有估值判斷、沒有股價或上市語氣；
  廠商宣稱一律帶「NVIDIA 表示／Hugging Face 表示」。**只有一個 callout**，沒有另加投資免責 callout，
  該 callout 內已寫明本文不是投資建議。資安部分沒有任何攻擊手法、入侵指標、逐日次數或階段表。
- **格式**：段落 2,990／3,000 字，五節各 3 段，`summary` 在第一個 heading 之前，FAQ 7 題、答案無連結，
  全文無簡體字、無列點、無 Markdown、無 emoji，`checked_on` 2026-09-18 在四條 source、研究紀錄、
  第二段、表格 caption 與圖解 caption **六處一致**（本輪未更動）。

## 留給站主的 3 件事

1. **`topics` 是 `["ai", "ai-news"]`，缺 `BRIEF.md` 要求的橫向主題**
   （同垂直的 `ai-news-anthropic-threat-report-20260910` 用 `["ai", "software", "ai-news"]`）。
   `check_article.py` 不擋，所以查核代理沒有自行挑一個填——請協調者決定。
2. **`verified_facts` 第 11、20、23、26 條的 `verbatim_quote` 仍是刪節號接起來的兩段。**
   兩個片段各自逐字、順序也對（見上），所以不是 `must_fix` 3 那種錯；但依 `BRIEF.md`
   「`verbatim_quote` 只能是原樣搜尋得到的連續字串」，它們應該拆成兩條或改標成敘述。
   查核代理沒有動，以免改變研究紀錄的形狀。
3. **第二個結尾連結目前指向 Astral 那篇。** 第 5 節現在只用官方說法交代 7 月資安事件，
   不再宣稱站上另有一篇 Amodei 角度的文章；若之後補寫那一篇，這個連結可以換過去。
   兩個結尾連結依規格未動。

另外記錄一個**判斷**：修正清單 `must_add` 提到的 `data.sec.gov` 8-K 與攻擊階段表，
**不寫不會誤導**。事件日已由公告自己的 `article:published_time` 認定，8-K 只會再確認同一天
（`acceptanceDateTime` 晚約 7 分鐘，同一天）；階段表是攻擊手法的細部拆解，正是 `tech.md`
要求不寫的那一類。維持撰稿者的決定，不加來源、不擴編。

## 自檢輸出（原樣）

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-openai-astral-20260319
```

兩條都在規格允許留下的清單內（索引與相關文章由協調者事後處理），
而且**與查核前的輸出完全相同**，不是本次編輯造成的。

## 結論

`needs_second_round`：文章經約 118 條主張逐條核對後可刊，19 處已改；
但改動超過十處事實，而且第 3 節的順序論述與第 5 節的資安段落是**重寫**的，
依規格應由另一位查核者對這一輪新寫進去的每一句再走一次來源。

---

## 第二輪

查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 未更動）。
範圍是第一輪改動過的每一段與新寫進去的每一句，加上研究紀錄**全部** `verbatim_quote` 的連續字串比對與界線再掃——
不是整篇重做。查了**第一輪新寫或改寫的約 55 條主張**外加 **31 條逐字引文**；
**內容包改了 9 處、研究紀錄改了 6 類（含引文拆併，31 條 → 34 條）**。

### 來源重抓（四條都還在，body 都是正文）

| source | HTTP | bytes | body 是正文？ | 與第一輪的差異 |
| --- | --- | --- | --- | --- |
| blogs.nvidia.com 收購公告 | 200 | 109,600 | 是，`<article>` 16,886 chars | 比第一輪多 4 bytes，差額全在 `<article>` 之外的相關文章區塊 |
| huggingface.co 2026-07-16 揭露 | 200 | 575,348 | 是，`datePublished` 2026-07-16 | 相同 |
| huggingface.co 2026-07-27 技術文 | 200 | 725,774 | 是，`datePublished` 2026-07-27 | 相同 |
| images.nvidia.com 公開信 PDF | 200 | 801,845 | 是，5 頁，第 4、5 頁只有空白字元 | 相同；`Huang`／`Jensen` 各 0 次、`July 24, 2026` ×1 |

活資料三頁另外重抓（不進 `sources[]`）：`/blog` 200、`/blog/community` 200、`/clem/activity/posts` 200，
對 `acqui` 不分大小寫**今天三頁皆 0 命中**，正文那句否定句成立。

### 指派訊息點名的五個疑點

**1. 第 3 節的順序論述——先後與主詞都對，但論點比來源強。**
直接讀原始 HTML 58340–59620 重建版面：`<p>`58369（政策主張）→ `<p>`58789（`AI advances faster…`）
→ `<p>`58847（第三人稱 `hundreds`）→ `<ul>`，其中 `<li>`59201（最大貢獻者，用 `our`）、
`<li>`59325（500+／250+）、`<li>`59424（`We build our own models…`）。
**第一輪的兩處順序更正完全成立**：政策主張確實早於三個貢獻數字；`hundreds` 確實是段落不是 `<li>`；
兩個貢獻數字確實是同一個 `<ul>` 裡連續的前兩條、後面還有第三條。主詞也對（`hundreds` 那段是 `NVIDIA…it`，
第一條帶 `our` 所以文章寫「自稱」）。
**但論點本身站不住，已改**：(a)「順序值得注意」是文章自己的評價，改成「是這樣排的」，只並列官方怎麼寫；
(b) 結尾「同一份公告因此出現數百個、500 個以上與 250 個以上**三種說法**」會暗示公告自相矛盾，
而原文的 `hundreds of open models and datasets` 是**模型與資料集合計的概括說法**、500+ 與 250+ 是**拆開的明細**，
兩者並不衝突。改成「概括的數百個與拆開的 500 個以上、250 個以上並存」。
同段第 3 段結尾「這段是公告裡把收購和開放權重立場連在一起**最直接的部分**」也刪了：
58369 那一段通篇只談開放模型的作用，**整段沒有出現 Hugging Face，也沒有出現這筆收購**，
撐不起「把收購和開放權重連在一起」，更撐不起「最直接」這個比較級。改成可查證的
「這一段沒有提到 Hugging Face，也沒有提到這筆收購」。

**2. 第 5 節資安段落——官方影響範圍被截掉了後半句，已補回。**
原文是 `No other customer-facing models, datasets, Spaces, or packages were affected,
and the only customer records read were operational metadata tied to search queries against the dataset server.`
第一輪只寫到前半，**讀起來比官方自己說的範圍更小**，是被吃掉的但書。
已補上「被讀取的客戶紀錄只有資料集伺服器查詢的維運中繼資料」。
另外把「改用開放權重模型**完成鑑識**」改成「把整條鑑識流程改走自行架設的開放權重模型」——
原文只寫 `rerouted the entire pipeline through it`、`on our own infrastructure`
與 `decipher **most** of the agent payloads`，`most` 不等於「完成」。
出處也修了：「部分的正式環境基礎設施」這個限定只出現在 2026-07-16 的揭露
（`part of our production infrastructure`），技術文寫的是 `internal infrastructure`
與 `against our production infrastructure`、沒有 `part of`，所以改成「2026 年 7 月的**兩篇**說明」，
範圍句另標「其中的技術文章」。
「兩個具名的商用模型拒絕了鑑識工作的很大一部分」這句**照原文、歸因 Hugging Face、沒有評語**，維持不動；
FAQ 第 6 題原本寫成「最先動用的兩個模型」，已補回原文具名的 Claude Opus 與 Fable，並刪掉「剛好」這個評語副詞。
**全段仍沒有任何攻擊手法、入侵向量名稱、逐日行動數、階段表或入侵指標**（來源那幾段寫出的
`chunk+XOR+compress`、兩個注入向量、五天逐日表，一個字都沒有進文章）。

**3. 四條刪節號引文——全部換成連續字串，31 條 → 34 條。**
先在**未正規化的原始 HTML** 上定位（四組片段在各自來源都只出現一次，位置唯一），確認先後與原文一致，再處理：

| 原第幾條 | 兩個片段的位置 | 處理 |
| --- | --- | --- |
| Clem 三人名 | s1 56944 → 60772（相隔約 3.8 KB） | 拆成兩條 |
| 2026-07-16 影響範圍 | s2 66698 → 66975（中間隔一句） | **補回中間那句**成單一連續引文 |
| ExploitGym 評測／作弊動機 | s3 81126 → 81684（中間隔一句） | 拆成兩條 |
| Claude Opus 與 Fable／GLM-5.2 | s3 141886 → 142419（中間隔一張圖說） | 拆成兩條 |

2026-07-16 那條特別值得記：**刪節號略過的那一句，正是這條事實自己依據的句子**
（「當時仍在確認是否影響合作夥伴或客戶資料」＝`We are still completing our assessment…`），
所以不是拆條而是補回。拆開後每一條都重新對照來源，撐的仍是同一件事。
同一條順手修掉一個抄錄錯誤：`( nvidia/GLM-5.2-NVFP4 )` 括號內的空格原件沒有——
原始碼是 `(<a href="/nvidia/GLM-5.2-NVFP4">nvidia/GLM-5.2-NVFP4</a>)`，空格是把標籤換成空白造成的抽取假影。
另附更正：第一輪報告把這四條編號成第 11、20、23、26 條，實際是第 **12、21、24、27** 條（整體少一），
「公開信定義句」也是第 18 條而非第 17 條。

**4. 交易狀態——全文仍只寫 `has agreed to acquire` 撐得住的說法。**
`completed`／`definitive agreement`／`closing`／`subject to`／`regulatory`／`antitrust`／`approval`／
`customary`／`forward-looking`／`signator`／`billion`／`quarter` 今天在**整頁 HTML 皆 0 次**。
FAQ 第 1 題刪掉「用的是**協議階段**的說法」這個本文自己的定性，改成照字面寫
「NVIDIA 在 2026 年 9 月 3 日寫的是**它**已同意收購 Hugging Face」——
主詞只留 NVIDIA，不寫成「雙方達成協議」，避開 `must_not_write` 第 4 條（不得把任何事歸給 Hugging Face 一方）；
「截至查核日」補成完整日期。答句現在先給讀者一個明確的界線（公告只說到已同意），
再明寫「四條來源裡沒有任何一條說明這筆交易後來是否完成」，**不推測是否已完成**。
全文無估值判斷、無股價、無上市或投資語氣（`估值` 僅一次，出現在「公告未說明先前的估值與營收」這個否定句裡）。

**5. `topics` 維持 `["ai", "ai-news"]`，此項結案。**
今天清點 `content/` 下 52 篇 `ai-news-*`：38 篇 `["ai","software","ai-news"]`、
**8 篇（含本篇）`["ai","ai-news"]`**、3 篇 gadgets、2 篇 productivity、1 篇 daily。
這是一則公司併購新聞，沒有合適的第二個橫向主題，依指派維持不動；
第一輪把它掛成待站主決定的事項，第二輪已在研究紀錄裡結案。

### 內容包改掉的 9 處

1. 第 3 節第 2 段：「順序值得注意」→「是這樣排的」（論點降回敘述）。
2. 第 3 節第 2 段結尾：「出現…三種說法」→「概括的數百個與拆開的 500 個以上、250 個以上並存」。
3. 第 3 節第 3 段結尾：刪掉「最直接的部分」，改成「這一段沒有提到 Hugging Face，也沒有提到這筆收購」。
4. 第 5 節第 3 段：補上官方影響範圍的後半句（維運中繼資料）。
5. 第 5 節第 3 段：「完成鑑識」→「把整條鑑識流程改走自行架設的開放權重模型」。
6. 第 5 節第 3 段：資安事件出處由「技術文章」改成「2026 年 7 月的兩篇說明」，範圍句另標「其中的技術文章」。
7. 第 5 節第 3 段：刪掉重複的「NVIDIA 公告並未提到這起事件」（同段開頭已寫過）。
8. 第 2 節第 3 段：刪掉重複的「文章開頭寫明這是黃仁勳個人具名發表」（第 1 節第 2 段已寫過）。
9. FAQ 第 1 題與第 6 題改寫（見上）。

第 7、8 兩處是**刪重複敘述**，為的是騰出字數放第 4 處補回的官方範圍句；
**沒有為了字數刪掉任何但書、限定詞或歸因**。段落總字數 2,990 → **2,987**（上限 3,000）。

### 研究紀錄改掉的 6 類

1. `sourcing_notes` 的 `Taiwan` grep 結果是錯的：整頁 HTML 今天有 **2 次**，兩次都在 JSON-LD 的作者簡介
   （黃仁勳的榮譽博士學位；同一段也是 `founder` 一字整頁唯一的出處），`<article>` 內文 0 次。
   原紀錄寫成「整頁 0 次」，否定句只能限定在**公告內文**。
2. 四條刪節號引文改成連續字串（見上），`verified_facts` 31 → 34 條。
3. GLM-5.2 引文的括號空格更正。
4. 五個資料集那條補上原文同句後半的維運中繼資料。
5. 活資料那條刪掉三個位元組數：同一天內就量到 `/blog/community` 136,143 與 `/clem/activity/posts`
   546,059、546,165 等不同值，**位元組數不是版本識別**；同時刪掉沒有來源的「共同創辦人 clem」。
6. `factcheck` 底下新增 `second_round`（方法、9 條 `edits_to_the_pack`、6 條 `edits_to_the_record`、
   12 條 `checked_and_correct`、1 條 `left_for_the_owner`），並把第一輪 `left_for_the_owner` 的第 1、2 項結案。

### 查過而且正確、沒有動的部分

- **第一輪最重的兩處順序更正經原始 HTML 重驗完全成立**（見疑點 1）。
- 時間戳記今天重讀仍是 `article:published_time` 2026-09-03T11:56:49+00:00 與
  `article:modified_time` 2026-09-03T20:54:05+00:00；台北時間 9/3 19:56 與 **9/4 04:54**（跨零時）換算無誤；
  頁面上看得到的日期仍只有 `September 3, 2026`。
- 公開信 PDF 定義句那條引文以**忽略空白**的比對確認與 PDF 文字層一致，差異只是 pypdf 的字距假影
  （同頁另有 `st ud y`、`modify ,` 這類明顯假影），**維持第一輪不動的判斷**。
- 職稱：`Delangue`／`Chaumond`／`Wolf`／`co-founder` 整頁 0 次；`president, chief executive officer`
  只在 JSON-LD 作者簡介裡，是「執行長」一詞的依據。文章四處都已不寫三人職稱。
- 平台五個數字（18M／3M／500,000／1M／200,000）與「使用平台的公司」逐字無誤；
  `summary` 四句、圖解四格與 `hero_label` 的每個數字都仍在正文出現。
- 唯一內文超連結仍只有掛在 `open model` 一詞上的名詞解釋頁（57075，落在 56944 那段之內）。
- 界線：沒有購買建議、推薦式比價、估值判斷、股價或投資語氣；廠商宣稱一律帶「NVIDIA 表示／Hugging Face 表示」；
  **只有一個 callout**、不帶 `finance` 主題、沒有投資免責 callout；沒有推定台灣可用；
  沒有重寫或牴觸站上既有 AI 文章（第一輪刪掉的那個指向不存在文章的交叉引用確認已不在文中）。
- 格式：五節各 3 段、FAQ 7 題且答案無連結、無簡體字、無列點、無 Markdown、無 emoji；
  `checked_on` 2026-09-18 六處一致，本輪未更動。

### 留給站主的事

只剩**兩個結尾連結**：依規格未動，索引與相關文章的標題由協調者事後處理；
第二個連結目前指向 OpenAI 併購 Astral 那篇。第一輪列的另外兩項（`topics`、刪節號引文）本輪已結案。

### 自檢輸出（原樣）

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-openai-astral-20260319
```

兩條都在規格允許留下的清單內，**與第一輪、與本輪編輯前的輸出完全相同**，不是本次編輯造成的。

### 結論

`ok`。第一輪那 19 處的方向都對，兩處最重的順序更正經原始 HTML 重驗成立；
本輪改的 9 處是**論點強度**（順序論述、「三種說法」、「最直接」）、
**被截掉的官方影響範圍**與**被吃掉的 `most`**，不是事實錯誤，
四條刪節號引文也已全部換成連續字串。文章可刊，只等協調者處理兩個結尾連結。
