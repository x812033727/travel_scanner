# 獨立查核：tech-news-nvidia-vera-rubin-20260915

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 維持 **2026-09-17**，那是撰稿者實際讀到來源的日子，六處一致，不因本輪重查而改）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；要引的英文字串一律用「去標籤但**不補空白**」的方式回原始 HTML 確認是可原樣搜尋到的連續字串
（NVIDIA 的頁面會把 `Silicon Valley Powe|r`、`HGX B20|0` 這種字切在兩個 span 裡，普通的抽文字會在字中間塞空白，拿去比對會誤判）。
另外重讀站上既有的 `ai-news-nvidia-rubin-20260105` 全文核對有無重寫或牴觸。**沒有使用任何 `sources[]` 以外的新網址替文章補事實。**

檢查的主張：約 **92** 條（正文 13 段、摘要 5 句、FAQ 6 題答句、1 個 callout、表格 12 格與 caption、圖解 caption 與四格、title、description）。
**改了 19 處**，其中約 15 處是事實層級；另有 5 件留給站主。

## 重抓結果（四條都還在、位元組數與研究紀錄逐條相同）

| source | HTTP | bytes | body 是正文嗎 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| blogs.nvidia.com `ai-infra-summit-vera-rubin-dsx-…` | 200 | 134,522 | 是 | `article:published_time` 2026-09-15T16:55:40+00:00、`modified_time` 2026-09-16T18:57:45+00:00；廠級 40%／35% 兩個項目符號；Lambda、SemiAnalysis、DSX Flex、Vera CPU 新創、NVLink 6 六個小節；`Wednesday, Sept. 16` 的 MLPerf 段 |
| blogs.nvidia.com `from-megawatts-to-tokens-…` | 200 | 126,175 | 是 | `published_time` 2026-09-15T16:55:59+00:00；黃仁勳引言；GTC Taipei 那句；Lambda 19／16 節點；`Based on NVIDIA’s projections` 那句；`DSX at a glance` 側欄；`Numbers at a glance` 五列 |
| nvidianews `rubin-platform-ai-supercomputer` | 200 | 93,790 | 是 | January 5, 2026；`CES—` 起頭；六顆晶片列名；10x／4x；`will be available from partners the second half of 2026`；`will also offer` HGX Rubin NVL8 |
| nvidianews `nvidia-groq-3-lpx-…` | 200 | 77,601 | 是 | August 24, 2026；`Hot Chips—` 起頭；`across seven chips and five purpose-built racks`；`Groq and LPU are used under license from Groq, Inc.` |

四個位元組數與研究紀錄寫的完全相同，沒有轉址殼、軟性 404 或擋阻頁。
`article:modified_time` 今天重抓仍是 **2026-09-16T18:57:45+00:00**，與 9 月 17 日那輪相同——這一點推翻了草稿 callout 的寫法，見下面第 19 點。

## 改掉的 19 處

**撰稿者點名要重查的三句，結論分別是：第 1 句正確但掉了一個條件、第 2 句正確、第 3 句歸屬要限縮。**

1. **廠級 40% 掉了『在同一場地電力額度內』**（第 3 節第 2 段）。原文是兩個獨立的項目符號，各自是連續字串：
   `Up to 40% more GPUs within the same site-power envelope` 與 `Up to 35% higher token throughput — no new power lines required`。
   草稿把 35% 的 `no new power lines required` 保留了，卻把 40% 的 `within the same site-power envelope` 拿掉。
   **廠級／機櫃級的區分本身是對的**（修正清單 must_fix 1 已套用），已補回條件，並把機櫃層級寫成
   「另有削峰軟體與擴充儲能吸收短暫尖峰，**官方在這一層沒有給百分比**」，把兩層的界線寫死。
2. **兩個 40% 讀起來像兩個數字，已合併成一個主張**（同段）。草稿先寫廠級「最高可多出 40% 的 GPU」，
   同段稍後又寫「Vera Rubin NVL72 那組最高多 40% GPU 容量的數字」——讀者會以為是兩筆。
   兩者其實是同一個宣稱：高峰會那篇的廠級段落本來就寫在 Vera Rubin NVL72 的脈絡裡。已改成
   「上面那個 40% 掛到 Vera Rubin NVL72 時……」。
3. **「NVIDIA 自己標成依投影」要限縮到配套那篇**（同段與 FAQ 第 2 題）。
   `Based on NVIDIA’s projections` 只在 `from-megawatts-to-tokens` 出現；
   **高峰會那篇寫同一件事時沒有這個前綴**（該字串在高峰會那篇 0 次命中），它寫的是
   `For next-generation NVIDIA Vera Rubin NVL72 AI factories, DSX MaxLPS can enable up to 40% more GPU capacity within the same megawatt budget in the right deployment environments.`
   已改成指名是配套那篇標的，並在 FAQ 補一句「同日的高峰會彙整文則只寫結果，沒有標上投影兩個字」。
4. **矽谷電力公司那句：4→3 MW 與 40% 的並列本身正確，不必改**。逐字複查：正文兩處都是 4→3 MW
   （`power dropping from four megawatts to three, automatically` 與 `power fell from four megawatts to three`），
   `Numbers at a glance` 表是 `40% | power demand reduction in under a minute | SVP automated response, Flexible Load Interconnect Program`。
   兩個數字各自的出處、條件與「官方沒有說明兩者關係」都寫對了，文章也沒有相加相減或替官方選一個。**這一處沒有動。**
5. **Lambda 的 24%／23% 與 Vera Rubin 的 40% 沒有被混成同一套硬體**——這一點草稿也做對了，
   但補了兩個限定：**（a）** `19 nodes at 85% power vs. 16 nodes at full power`，**85% 電力政策**是這兩個百分比的前提，
   正文那句沒寫、只有「數字一覽」表寫了，已補進文章；**（b）** 見第 6 點。
6. **「Lambda 總裁」→「Lambda 雲端服務總裁」**。Dave Ward 的職稱是 `president of cloud services at Lambda`，不是公司總裁。
7. **「唯一有實測支持的是 Lambda」→「這組電力數字裡有夥伴實測的是 Lambda」**。同一篇公告裡
   Vera CPU 的新創測試、SemiAnalysis AgentX 與 MLPerf 都是量測結果，「唯一」站不住（BRIEF 型態 6）。
8. **黃仁勳引言誤譯**（第 3 節第 1 段）。原文 `A one-gigawatt factory will never become a two-gigawatt factory`，
   草稿寫成「不會自己變成**兩座十億瓦**的機房」——把**一座二十億瓦**的機房寫成了兩座十億瓦。已改。
9. **講題寫錯**（第一段與摘要第 1 句）。草稿寫 Ian Buck「以 Vera Rubin 平台與 DSX 機房電力管理軟體為題演講」，
   來源寫的是 `spoke on AI factory efficiency`／`made AI factory efficiency the centerpiece of his infrastructure keynote`。
   已改成「以 AI 機房效率為題發表基礎設施主題演講」，並把場地與講題整句歸給 NVIDIA 官方部落格
   （聖塔克拉拉會議中心只有 NVIDIA 一個來源，修正清單 `source_list_fix` 3 點過名）。
10. **「Ian Buck 說明」是誤植歸屬**（第 1 節第 1 段）。`The metric for AI infrastructure is fast shifting…`
    那兩句**不在 Buck 的引號內**，是部落格本身（NVIDIA Writers）的敘述。已改成「NVIDIA 在這篇彙整文章裡表示」。
    description 的「NVIDIA……**把**衡量 AI 機房的指標**從尖峰效能換成**每百萬瓦的 token 產出」同步改成
    「並**表示**……**正從**尖峰效能**轉向**」——原文說的是指標正在移動，不是 NVIDIA 把它換掉。
11. **「當天新進展全是電力管理與生態系合作」不成立**（第 1 節第 2 段）。同一篇公告另有
    `Startups Celebrate Performance Results With NVIDIA Vera CPU`（多家新創的 Vera CPU 測試結果）與
    `NVIDIA NVLink 6 Keeps AI Factories Running at Massive Scale` 兩節。已改成「當天沒有新的晶片發表」並補上這兩節；FAQ 第 1 題同步。
12. **三項合作的歸屬全錯**（同段）。草稿寫「Annapurna Labs 表示」「d-Matrix 表示」「Pinterest 表示」，
    但唯一來源是 NVIDIA 自己的部落格，三家沒有發言。已全部改成「NVIDIA 表示」。
13. **d-Matrix 那句方向寫反且掉了限定**（同段）。原文 `d-Matrix is integrating with NVLink Fusion to combine NVIDIA Vera CPUs with d-Matrix Raptor XPUs to deliver ultra low-latency inference at scale`；
    草稿寫成「把 NVLink Fusion 整合進 Raptor XPU」，並掉了 `ultra` 與 `at scale`。
14. **Pinterest 那句換了主詞**（同段）。原文 `to bring conversational AI to visual discovery`，
    草稿寫成「強化視覺搜尋」——把對話式 AI 換成搜尋、把 visual discovery 換成視覺搜尋。
15. **megawatt 的出現次數刪掉**（第 2 節第 2 段）。「1 月零次、兩篇部落格十次與五次」是編輯自己數的
    （跨篇通則 2），而且**單複數要分開數**：配套那篇 `megawatts` 另有 5 次，只數單數會把它低估一半。
    已改成不寫次數，只寫「1 月的新聞稿整篇沒有用百萬瓦當衡量單位」——這一項複查成立（`megawatt` 與 `megawatts` 在 1 月稿皆 0 次）。
16. **`price` 的 grep 刪掉**（第 5 節第 1 段）。「兩篇公告也沒有出現 price（價格）一字」是子字串式的負面證據，
    而同兩篇各有一次 `pricing`（`pricing signals`／`pricing events`，講的是電網電價）。
    已改成「兩篇公告通篇沒有提到 Vera Rubin、Groq 3 LPX 或 DSX 任何一項的售價或授權費，只在描述電網訊號時出現過電價」。
17. **台灣那段改成規定的否定句型**（第 5 節第 2 段）。「兩詞皆零次出現」→「以 Taiwan 與 TSMC 查核到 2026 年 9 月 17 日都未見」，
    「唯一沾邊」→「與台灣有關的只有」。同時**刪掉指向 `nvidianews.nvidia.com/releases.xml` 的建議**——
    那個網址不在 `sources[]` 內，文章也沒有從它取任何事實，不該叫讀者去那裡；改成請讀者回到這兩篇部落格本身。
18. **「快 3.7 倍」→「吞吐量最高比 GB300 NVL72 高 3.7 倍」**（第 4 節第 2 段與表格第 4 列）。
    原文是 `up to 3.7x higher throughput`，是吞吐量不是速度。同段「官方完整說法只有一句」限縮成「兩篇 9 月 15 日部落格給的只有一句」。
19. **callout 的活文件敘述過頭**。草稿寫「本文查核當下（2026 年 9 月 17 日）**內文仍在變動**」，
    但證據只到「兩次查核之間被改過一次」：`article:modified_time` 是 2026-09-16T18:57:45+00:00，今天重抓沒再動。
    已改成「查核時（2026 年 9 月 17 日）讀到的版本標示最後修改於 9 月 16 日」。
    另外表格第 1 列「最高省 10 倍推論成本」補成「每 token 推論成本」（原文 `inference token cost`／`cost per token`）、第 3 列補上「官方稱」；
    摘要第 5 句「官方沒有公布……交付雲端或任何價格」改成「查核到的官方公告沒有公布……出貨數量、客戶名單或任何售價」；
    圖解第一格「晶片／Vera Rubin NVL72」改成「Vera Rubin 平台」（NVL72 是機櫃級系統不是晶片）、
    第三格「MaxLPS 動態調度，最高 40%」改成「同電力下多 40% GPU」，讓圖上的 40% 有受詞。

研究紀錄另改了 8 條：上述 1／6／12／13／14／15／18 對應的 `verified_facts`、
把廠級那條用刪節號串成的 `verbatim_quote` 換成真正的連續字串（跨篇通則 1）、
把 `verbatim_quote` 空字串那條標成「無逐字引文：這是編輯的清點結果」、
以及兩條 `not_said`（見下面「查過而且正確」最後一項）。

## 查過而且正確的部分（沒有動）

- **修正清單 must_fix 1／5／6／7／8／9／10／11 全部確認已套用或以不寫的方式避開**：40%／35% 寫成廠級、
  GTC Taipei 這個台灣關聯有寫出來**而且不帶年份**、沒有出現 `Groq 3 LPU`、沒有「第七顆晶片」框架、
  沒有 227 kW、沒有 HGX Rubin NVL8、NVHBM 沒有寫成「NVIDIA 的」技術。
- **`sources[]` 之外的事實沒有外溢**：`developer.nvidia.com` 三篇、`docs.nvidia.com`、
  `case-studies/lambda`、另兩篇 `blogs.nvidia.com` 上的數字（227 kW、125→90 kW、1.6x、Nebius、OpenRouter 15x、40 QPS）
  一句都沒有進文章，全部留在 `unverified_or_excluded`。
- **三組帶基準的數字都完整**：35x（對 GB200 NVL72、兩兆參數以上、長上下文）、
  2,529 output tokens/sec（100K 上下文、Qwen 3.8 27B）、30x（DeepSeek V4 Pro、對 GB300 NVL72、SemiAnalysis AgentX）。
  三者都歸因給 NVIDIA 或 NVIDIA 的轉述，沒有一處寫成本站驗證過。
- **預告與已上線分得清楚**：來源寫 Emerald AI `is planning to use` DSX Flex、
  `integrating into DSX Flex as the platform matures`、表格來源欄寫 `Future DSX Flex`；
  文章寫「還不是正式的 DSX Flex 安裝，只是證明概念可行」，一致。
- **日期沒有混用**：事件日 2026-09-15（兩篇 `published_time` 都是這一天）與 slug、`news_date` 一致；
  MLPerf 那段確實掛在頁內 `Wednesday, Sept. 16, 8:00 a.m. PT` 小標下，文章歸給 9 月 16 日正確；
  1 月 5 日（CES）與 8 月 24 日（Hot Chips）與新聞稿印的日期相符。
- **「9 月沒有更新 2026 下半年這個時程」成立**：兩篇 9 月 15 日部落格裡與年份有關的只有配套那篇
  800V DC 那列的 `2027`，而那是**電力架構**的時程、不是 Rubin 產品供貨時程，文章沒有引用，
  也沒有像修正清單 must_fix 4 警告的那樣寫成「唯一的日期承諾」。
- **與既有文章不衝突**：`ai-news-nvidia-rubin-20260105` 談 1 月 CES 與推論成本／終端定價的落差，
  本篇只用一句話帶過並明寫不重複；兩篇對「已全面生產、夥伴產品 2026 下半年提供」的寫法一致，沒有把一月的內容當成九月的新消息。
- **科技垂直界線**：全文沒有購買或升級建議、沒有推薦式比價、沒有機型比較結論、沒有攻擊細節；
  只有一個 `info` callout，**沒有**投資免責段落；廠商數字全部帶「NVIDIA 表示／NVIDIA 稱／官方稱」。
- **摘要與 FAQ 合規**：摘要 5 句的每個數字（40%、35%、24%、23%、3.7、35 倍、30 倍、2,529、4／3 百萬瓦、一分鐘、兩百）
  都在正文出現過；FAQ 答案是純文字、沒有網址；全文沒有簡體字、列表、Markdown 或 emoji。
- **兩條 `not_said` 已限縮**：原本寫「官方沒有在任何一處說 Lambda 已經把 DSX MaxLPS 用在正式營運環境」，
  但配套那篇明寫 `Results from cloud provider Lambda’s first validation in a deployment environment`——
  官方的說法是「在部署環境中的**首次驗證**」，同時**當事人**稱之為概念驗證，兩件事要並列；已改寫。
  文章正文本來就只寫了當事人那一半，沒有踩到，不必改文章。

## 留給站主的 5 件事

1. **`check_article.py` 仍是 FAIL，只剩一條**：`zh-TW link target tech-news-2026-index.json does not exist yet`。
   科技垂直的索引內容包還沒建立，不在查核代理可動的兩個檔案裡（跨篇通則 15 也說留給索引階段）。
   索引落地後，第一個 link 的 text（目前的佔位字串）要**逐字**換成索引自己的 zh-TW title，`check_article.py` 會比對。
   第二個 link（`tech-news-nvidia-cuda-q-20260914`）已經通過，沒有第二條 FAIL。
2. **撰稿者問的六條 `must_add`，本代理判定沒有一條屬於「不寫就會誤導」。**
   六條的正確一手出處都在四條 `sources[]` 之外，而草稿是**整條不寫**而不是寫一半，
   所以讀者不會拿到被削掉限定詞的版本（這正是 BRIEF 型態 3 想避免的相反情況）。
   最接近需要補的是 SemiAnalysis AgentX 的 30x：NVIDIA 自己 9 月 16 日的 MLPerf 專文把它描述成 `in preview testing`，
   比高峰會那篇保守。但文章已經寫明是 NVIDIA 轉述、本站未取得原始數據，缺這一句不會誤導。
   要補就必須換掉一條 `sources[]`（四條上限），那是編輯取捨，本代理不代決定。
3. **字數只剩 7 字**：zh-TW 段落 2,993／3,000。本輪為了補回「在同一場地電力額度內」與「85% 電力政策」兩個限定，
   已刪掉「本文只在這裡提一次」這句純編輯用語來換字數。之後若還要補任何限定詞，
   **必須從別處刪等量的字，不可以刪限定詞湊字數。**
4. **還有一層條件沒寫進去**：`Numbers at a glance` 把 Vera Rubin NVL72 那個 40% 的條件寫成
   `MaxLPS combined with data center power planning`，比正文多了「搭配機房電力規劃」這一層。
   文章目前只寫「在同一場地電力額度內」與「依投影、限於合適的部署環境」。要不要再補受第 3 點的字數限制。
5. **高峰會那篇是活文件，還會再長內容。** 今天（2026-09-18）重抓 `article:modified_time` 仍是
   2026-09-16T18:57:45+00:00，與 9 月 17 日那輪相同。出刊前建議再抓一次 meta；
   如果又往後移動，callout 裡「標示最後修改於 9 月 16 日」那一句要跟著改。

## 結論

`needs_second_round`。文章經約 92 條主張逐條核對後，事實面已可刊，19 處已改。
選第二輪不是因為還有已知的錯，而是照規格的門檻：**改了約 15 處事實，而且動到第 3 節
「廠級對機櫃級、實測對投影、Blackwell 對 Vera Rubin」這條骨幹論述**——那一段現在是全文最密的地方，
值得第二個人再讀一次那三句，尤其是兩個 40% 合併後的讀法。
另外唯一擋住 gate 的 FAIL 是科技索引內容包還不存在，不在查核代理可動的兩個檔案裡。

---

## 第二輪

第二位查核代理（未參與撰稿，也不是第一輪那位）。查核日 **2026-09-18**。
範圍不是整篇重做，而是：**（a）** 第一輪改動過的每一段與新寫進去的每一句，逐句回四條 `sources[]` 原文；
**（b）** 全文每一處功率單位重新換算；**（c）** 研究紀錄每一條 `verbatim_quote` 用程式做字串比對；
**（d）** 回掃第一輪有沒有為了字數刪掉但書；**（e）** `summary` ⊆ 正文、FAQ ⊆ 正文、否定句的範圍。
**重查了約 55 條主張，改了 18 處**（內容包 13 處、研究紀錄 5 處）。

### 重抓結果（四條今天再抓一次，全部與第一輪逐條相同）

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| blogs.nvidia.com `ai-infra-summit-vera-rubin-dsx-…` | 200 | 134,522 | 是 |
| blogs.nvidia.com `from-megawatts-to-tokens-…` | 200 | 126,175 | 是 |
| nvidianews `rubin-platform-ai-supercomputer` | 200 | 93,790 | 是 |
| nvidianews `nvidia-groq-3-lpx-…` | 200 | 77,601 | 是 |

`article:published_time` 2026-09-15T16:55:40+00:00、`article:modified_time` **2026-09-16T18:57:45+00:00**——
與第一輪讀到的完全相同，callout 那句「標示最後修改於 9 月 16 日」今天仍然成立。
配套那篇沒有 `article:modified_time` 欄位。

### 逐字引文全數比對（跨篇通則 11）

把研究紀錄 32 條 `verbatim_quote` 用程式對兩種抽文字結果（去標籤不補空白／去標籤補空白）做字串比對，
含彎引號、直引號、`&nbsp;`、破折號四種變體。**31 條通過，1 條不通過**：

> 矽谷電力公司 40% 那條寫成 `40% | power demand reduction in under a minute | SVP automated response, Flexible Load Interconnect Program`

那是把表格三個儲存格用 `|` 拼起來的，頁面上沒有這個連續字串。
已換成該列 Context 欄裡真正連續的 `power demand reduction in under a minute`，
並在 `fact` 欄寫清楚那是一列表格、`40%`／說明／來源分屬三個儲存格。改完 32 條全部通過。

### 改掉的 18 處

**最重的三處在最前面。**

1. **35% 掉了 `Up to`**（第 3 節第 2 段）。來源兩條項目符號**都**以 `Up to` 起頭：
   `Up to 40% more GPUs within the same site-power envelope` 與
   `Up to 35% higher token throughput — no new power lines required`。
   第一輪補回了 40% 的「在同一場地電力額度內」，卻沒發現自己改寫出來的句子把 35% 的「最高」吃掉了——
   「在同一場地電力額度內**最高**多出 40% 的 GPU，且不必新建輸電線路**就**多出 35% 的 token 吞吐量」，
   中文的「最高」不會跨過分句分配到第二個數字。已改成「就**最高**多出 35%」。
2. **40% 少了「搭配機房電力規劃」這一層**（第 3 節第 2 段與 FAQ 第 2 題）。第一輪把這一層留給站主決定；
   第二輪的判斷是**會讓那個 40% 變強，所以要補**：不寫這一層，讀者會以為 MaxLPS 這套軟體單獨就能多 40% 的 GPU。
   配套那篇「數字一覽」該列的 Context 欄原文是
   `Vera Rubin NVL72, MaxLPS combined with data center power planning, same power budget`。
   已補「同篇數字表還寫明要搭配機房電力規劃」，字數從別處刪重複敘述換來（見第 13 點）。
3. **把一張照片的說明當成正文**（第 3 節第 3 段與 FAQ 第 3 題）。草稿與第一輪都寫「**正文兩次**寫某個 8 月夜晚
   電力自動從 4 百萬瓦降到 3 百萬瓦」。`four megawatts to three` 在配套那篇確實出現兩次，但**只有一次是正文**：
   `That August evening, when SVP called, Conductor executed against a predefined workload hierarchy: lowest-priority jobs yielded, high-priority inference kept running, and power fell from four megawatts to three.`
   另一次在 `<figcaption class="wp-caption-text" id="caption-attachment-98197">` 裡，是**現在式的通則敘述**
   （`The Emerald AI team in San Francisco watches as …`），**沒有指名 8 月那一晚**。
   已改成「內文寫某個 8 月夜晚……，同頁一張照片說明也寫同樣兩個數字」。
   第一輪的報告把這一處列在「查過而且正確」（「正文兩處都是 4 MW→3 MW」），那是漏看了 `figcaption`。
4. **「把同一件事寫成一分鐘內降低 40%」→「同一場示範」**（第 3 節第 3 段、FAQ 第 3 題、摘要第 4 句）。
   表格那一列的 Context／Source 兩欄（`SVP automated response, Flexible Load Interconnect Program`、
   `Emerald AI / Future DSX Flex`）確實指同一個方案，但「同一件事」讀起來像官方自己說過兩者等價，官方沒有。
5. **黃仁勳引言後面的對比是編輯加的**（第 3 節第 1 段）。原句「一座十億瓦的機房永遠不會變成一座二十億瓦的機房，
   **機房擴張卡住的不是晶片**，是能不能拿到更多電力」——來源沒有把晶片拿來當對照組，
   只寫 `In the AI factory economy, power is the constraint.`，而且**那句與引言不在同一段**（中間隔了兩段）。
   已改成「；NVIDIA 在**同一篇裡**寫電力就是 AI 機房經濟裡的限制條件」。
   引言本身（`A one-gigawatt factory will never become a two-gigawatt factory`）第二輪逐字複查正確，不動。
6. **2,529 掉了主詞**（第 4 節第 1 段）。原文 `On a 100K-context Qwen 3.8 27B workload, **Groq 3 LPX** hit 2,529 output tokens per second per user.`；
   草稿寫「較具體的數字是 10 萬 token 上下文……每位使用者每秒測到 2,529 個輸出 token」，接在「合併平台 35 倍」那句後面，
   會被讀成合併平台的成績。已改成「較具體的是 **Groq 3 LPX 在** 10 萬 token 上下文……」。
7. **3.7 倍的中文寫法與同篇 35 倍、30 倍不一致**（第 4 節第 2 段與表格第 4 列）。
   三處英文都是 `up to N x higher … than Y`（`up to 3.7x higher throughput`、
   `up to 35X higher token throughput per megawatt than GB200 NVL72`、
   `up to 30x higher throughput per megawatt than NVIDIA GB300 NVL72`），
   但草稿把 35 倍寫成「最高**是**……**的** 35 倍」、3.7 寫成「最高**比**……**高** 3.7 倍」——後者在中文是 4.7 倍。
   第一輪改對了「快→吞吐量」，沒發現倍數句型自相矛盾。已統一成「吞吐量最高**是** GB300 NVL72 **的** 3.7 倍」。
8. **「當天沒有新的晶片發表」是範圍不明的否定句**（第 1 節第 2 段與摘要第 2 句）。
   NVIDIA 自己的部落格不是這場研討會的完整紀錄。已限縮成「**兩篇 9 月 15 日公告裡**沒有新的晶片發表」／
   「**兩篇 9 月 15 日公告裡**沒有新晶片」，與第 2 節與 FAQ 第 1 題本來就有的限縮寫法對齊。
9. **NVHBM 掉了 `custom`**（第 1 節第 2 段）。原文 `the NVHBM custom high-bandwidth memory technology`，
   已補成「NVHBM **客製**高頻寬記憶體技術」。
10. **FAQ 第 2 題「不是正式導入」是編輯的推論，而且與官方寫法相牴觸**。
    配套那篇明寫 `Results from cloud provider Lambda’s first validation in a deployment environment`——
    官方說的是「在部署環境中的首次驗證」。已刪掉「不是正式導入」，只留有出處的
    「Lambda **雲端服務總裁**自己把這稱為概念驗證」（職稱也順手與正文對齊）。
11. **FAQ 第 2 題「同日的高峰會彙整文則只寫結果」不準確**。高峰會那篇同樣帶著 `in the right deployment environments`，
    少的只有 `Based on NVIDIA’s projections` 這個標籤（該字串在高峰會那篇 0 次命中，第二輪複驗成立）。
    已改成「同一件事在同日的高峰會彙整文裡沒有標上投影兩個字」。
12. **FAQ 第 5 題「本文查核到的官方頁面完全沒有出現任何價格」範圍過大**，而且四篇來源**都**有 `pricing`：
    兩篇部落格各 1 次講的是電網電價，1 月與 8 月新聞稿頁尾各 2 次在
    `Features, pricing, availability and specifications are subject to change without notice.` 這句樣板裡。
    已改成與正文同一個寫法：「兩篇 9 月 15 日公告都沒有寫出 Vera Rubin、Groq 3 LPX 或 DSX 任何一項的售價或授權費」。
13. **騰字數的六處刪除，全部是重複敘述，沒有一處是限定詞或但書**：
    第 1 節「本文不替官方補充」（同句前半已寫官方只給一句話）、
    第 2 節結尾「下一節說明這套軟體實際在做什麼」（與下一個小標重複）、
    第 3 節「本文如實並列」（兩個數字就列在同一句裡）、
    第 4 節「也沒有另外查證」（與「本站未取得原始數據」重複）、
    第 5 節「9 月 15 日的材料同樣沒有把效率數字換算成價格或速度承諾」（同段開頭與結尾各講過一次）、
    第 5 節「本文每段都標明官方哪一天所說」（而且不是每段都標，是關於本文自己的不實描述）。
    段落字數 **2,993 → 2,985**，可用餘裕從 7 字變成 **15 字**。

研究紀錄另改了 5 條：上面第 3 點對應的 `verified_facts`（照片說明的更正）、
第 1／2 點對應的廠級那條（補「兩條項目符號都以 `Up to` 起頭」，並寫下這一節的開場句
`NVIDIA does this with a full-stack AI factory built on the Vera Rubin NVL72 …`，
證明廠級 40%／35% 本來就在 Vera Rubin NVL72 的脈絡裡）、
第 7 點對應的 MLPerf 那條（寫下三個倍數的中文句型規則）、
拼接引文那條，以及 `megawatt` 清點那條（見下一節）。

### 第一輪自己寫錯、第二輪抓到的一個數字

研究紀錄寫「配套那篇 `megawatt` 5 次、`megawatts` **另外 5 次**」。
第二輪重數：配套那篇 `megawatts` 是 **2 次**（都是 `from four megawatts to three`），
另加標題與頁首各一次大寫的 `Megawatts`（`From Megawatts to Tokens`）；`megawatt` 5 次成立。
高峰會那篇 `megawatt` 10 次、`megawatts` 0 次成立；1 月新聞稿兩者皆 0 次，兩輪一致。
**文章本身沒有引用任何出現次數**（第一輪已把次數刪掉），所以這個錯只存在於研究紀錄，已更正。
它同時說明了為什麼跨篇通則 2 要禁止把編輯自己的清點寫成事實：連查核代理都會數錯。

### 第一輪點名的三句，第二輪的結論

| 第一輪要覆核的 | 第二輪結論 |
| --- | --- |
| **廠級對機櫃級**（40%／35% 各屬哪一層、`within the same site-power envelope` 與 `combined with data center power planning` 兩層前提） | 分層**成立**。兩個數字都在 `At the factory level` 之後；機櫃層級那句（`Intelligent Power Smoothing` 與擴充儲能）官方確實沒給百分比。但 35% 少了 `Up to`（已補），`combined with data center power planning` 該補（已補）。 |
| **實測對投影**（哪一篇標了 `Based on NVIDIA’s projections`） | **成立但 FAQ 的說法要修**。該字串在配套那篇命中、在高峰會那篇 0 次；不過高峰會那篇不是「只寫結果」，它同樣寫了 `in the right deployment environments`，少的只是投影這個標籤。FAQ 已改。 |
| **Blackwell 對 Vera Rubin**（24%／23% 是哪一套硬體、`85% power` 前提） | **成立，不必改**。`Lambda’s results, released at the AI Infra Summit, are the first validation of DSX MaxLPS on NVIDIA HGX B200 GPU Servers.` 與正文相符；85% 只出現在「數字一覽」表兩個 Context 儲存格（`19 nodes at 85% power vs. 16 nodes at full power, same facility budget`、`19-node cluster at 85% power policy vs. 16-node full-power baseline`），第一輪補進正文的寫法與這兩格一致。 |

**兩個 40% 合併成一個主張也成立**：高峰會那篇的廠級項目符號寫在
`NVIDIA does this with a full-stack AI factory built on the Vera Rubin NVL72 — systems, networking, software and power management working as one.`
之後，本來就是 Vera Rubin NVL72 的脈絡，與 Lambda 那一節那句 Vera Rubin NVL72 的 40% 是同一個宣稱，
只是用詞不同（`more GPUs` 對 `more GPU capacity`、`site-power envelope` 對 `megawatt budget`）。
文章「上面那個 40% 掛到 Vera Rubin NVL72 時……」的寫法可以留。

### 第二輪查過而且正確的部分（沒有動）

- **功率單位全文重算，沒有一處錯**：megawatt＝百萬瓦（第 1／2／4／5 節的「每百萬瓦 token」、
  第 3 節「4 百萬瓦降到 3 百萬瓦」對 `from four megawatts to three`）、
  gigawatt＝十億瓦（`A one-gigawatt factory` → **一座**十億瓦、`a two-gigawatt factory` → **一座二十億瓦**）。
  description、摘要、表格、圖解、callout 一併重算，中文的「一座／兩座」與「百萬／十億」沒有再錯。
- **Ian Buck 的講題與引號範圍正確**：高峰會那篇 `Tuesday spoke on AI factory efficiency at the AI Infra Summit, the Santa Clara Convention Center event`、
  配套那篇 `made AI factory efficiency the centerpiece of his infrastructure keynote`，
  文章「以 AI 機房效率為題發表基礎設施主題演講」與兩篇都相符。
  頁面上**唯一**的 Buck 直接引語是 `Infrastructure that’s fungible…` 那一段，文章沒有引用、
  也沒有把任何話放進他的引號內；`The metric for AI infrastructure is fast shifting…` 兩句確實在引號之外，
  文章歸給「NVIDIA 在這篇彙整文章裡表示」正確。
- **三家夥伴改成「NVIDIA 表示」之後，三句的歸屬與內容逐句重核皆相符**：
  `Amazon’s Annapurna Labs is working with NVIDIA on the NVHBM custom high-bandwidth memory technology.`、
  `d-Matrix is integrating with NVLink Fusion to combine NVIDIA Vera CPUs with d-Matrix Raptor XPUs to deliver ultra low-latency inference at scale.`（超低、大規模都在）、
  `Pinterest is using the NVIDIA Blackwell platform and NVIDIA Dynamo inference software to bring conversational AI to visual discovery.`
  句首的「NVIDIA 表示」以分號串起三句，涵蓋範圍正確。
- **第一輪沒有為了字數刪掉任何但書**：把第一輪前後兩版逐句比對，刪掉的只有「本文只在這裡提一次」這句編輯用語；
  所有 `up to`、條件子句、歸因語都還在。唯一的例外就是上面第 1 點的 35%——那是第一輪自己改寫時漏掉的，不是為了字數刪的。
- **第 1 節第 2 段補的兩節確實存在**：`Startups Celebrate Performance Results With NVIDIA Vera CPU`
  （Perplexity、Daytona、ClickHouse、DeepInfra、Prime Intellect、Redpanda、Starburst、Kinetica）與
  `NVIDIA NVLink 6 Keeps AI Factories Running at Massive Scale`，文章寫「多家新創的 Vera CPU 測試結果與一段 NVLink 6 可靠度說明」相符。
- **`summary` ⊆ 正文、FAQ ⊆ 正文**：摘要五句的每一個數字（19、16、24%、23%、4、3、40%、2026）都在正文出現；
  FAQ 六題答案全部是純文字、沒有網址，改寫後仍然句句在正文找得到依據（第 10／11／12 點就是為了修掉三處超出正文的說法）。
- **與 `ai-news-nvidia-rubin-20260105` 沒有重寫也沒有牴觸**：本篇談推論成本與終端定價落差的那一句仍只是一句帶過並明寫不重複。
- **科技垂直界線複查**：沒有購買或升級建議、沒有推薦式比價、沒有機型比較結論、沒有攻擊細節、
  沒有投資免責 callout；廠商數字全部帶歸因。
- **`checked_on` 2026-09-17 六處一致**，沒有因為第二輪重查而改動。

### 留給站主的 5 件事（第二輪版）

1. **`check_article.py` 仍是同一條 FAIL**：`zh-TW link target tech-news-2026-index.json does not exist yet`。
   科技索引內容包還沒建立，不在查核代理可動的兩個檔案裡；索引落地後第一個 link 的 text 要逐字換成索引的 zh-TW title。
2. **字數 2,985／3,000，餘裕 15 字**（第一輪是 2,993／7 字）。第二輪補的兩個但書是靠刪六句重複敘述換來的。
3. **可補但沒補的一句**：配套那篇把 Lambda 的測試稱為
   `Results from cloud provider Lambda’s first validation in a deployment environment`，
   文章目前只寫當事人那一半（概念驗證）。兩種說法不牴觸，寫弱的那一半不會誤導，
   所以第二輪只把 FAQ 裡編輯自己加的「不是正式導入」刪掉，沒有花約 20 字把官方那一半也寫進正文。要不要並列是編輯取捨。
4. **高峰會那篇仍是活文件**。今天（2026-09-18）`article:modified_time` 仍是 2026-09-16T18:57:45+00:00。
   出刊前再抓一次；若晚於這個時間，callout 那句與第 5 節「最後更新時間在查核期間又往後移動過」要一起重寫。
5. **第一輪提的六條 `must_add` 與四條 `sources[]` 上限，第二輪沒有改變結論**：不補、不換源。

### 第二輪結論

`ok`。約 55 條主張重查完畢，18 處已改；沒有一處是會讓讀者誤解主要結論的錯，
第 3 節那條骨幹論述（廠級對機櫃級、實測對投影、Blackwell 對 Vera Rubin）逐句回原文後**成立**，
第二輪只補條件、沒有推翻任何一句。自檢只剩索引那一條規格允許的 FAIL。
