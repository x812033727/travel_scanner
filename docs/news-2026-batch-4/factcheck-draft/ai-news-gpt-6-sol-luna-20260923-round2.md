# 查核報告（第二輪）：ai-news-gpt-6-sol-luna-20260923

- 查核者：獨立查核代理（第二輪，opus；沒有參與撰稿，也沒有參與第一輪），2026-09-26（台北）
- 規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/ai/SECOND-ROUND.md`（加上它指向的 `agents/ai/FACTCHECK.md`）、DELTA-4-8（全）、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF.md 十二條錯誤型態；第一輪報告 `factcheck/ai-news-gpt-6-sol-luna-20260923-round1.md`
- 改動的檔案：內容包 `apps/api/app/guides/content/ai-news-gpt-6-sol-luna-20260923.json`、研究紀錄 `docs/ai-news-2026-09-late/research/ai-news-gpt-6-sol-luna-20260923.json`（加 `factcheck.second_round`）
- 腳本：`_tools/ai-news-gpt-6-sol-luna-20260923/fc2_fetch.sh`、`fc2_text.py`、`fc2_around.py`、`fc2_keywords.py`、`fc2_quotes.py`、`fc2_apply.py`（資料 `fc2_second_round.json`）；原始回應與 `fetch-log.tsv` 在 `_raw/ai-news-gpt-6-sol-luna-20260923/round2/`

## 摘要（可直接貼）

- 查了 97 條：第一輪改動或新寫的 20 條、第一輪已確認的 161 條裡以 `random.seed(20260926)` 抽出的 54 條、協調者三條裁定、20 條但書／否定句／歸因／summary 與 FAQ 回掃。結果 CONFIRMED 80、CHANGED 15、NOT FOUND 1（刪）、OPEN 1。
- 事實修改 10 處，另依裁定改 11 處；研究紀錄改 7 處並加 `factcheck.second_round`。zh-TW 段落 2,940 → 2,900，description 191 → 198。
- 最重的三處：
  1. **OpenAI 自己的方案頁與標題矛盾**（沒改，留給站主）：chatgpt.com/pricing（今天 14:54Z，200，不在 sources[]）的比較表把 GPT-6 Luna、GPT-6 Sol 在 Free、Go 兩欄都標「No」，Free／Go 的桌面 Work／Codex 仍掛在 GPT-5.6 Terra；公告與 changelog（今天重抓，文字未變）寫 Free 與 Go 可在桌面 App 用 GPT-6 Luna。
  2. **「官方沒有寫 Business 或 Edu 是否也要管理員操作」被推翻**：changelog 9/22 條目自己連到的〈Workspace model availability〉頁寫 “In Enterprise and Edu, an administrator must enable Luna first.” 第一節 p3 與第五節 p3（第一輪改過的句子）兩處否定句刪掉，只留 Enterprise。
  3. **範圍不明的否定句與 summary／FAQ 不在正文**：FAQ 1「官方沒有寫 Sol 是不是也開放給免費或 Go」被方案頁推翻，限縮到公告與 changelog；summary 3 的「9%」正文沒有，改用正文的「11.1 倍」；FAQ 4 的 Fable 5 代替規則補進第三節 p3。
- 其他：HealthBench 的 45%／35% 只是 HealthBench 的數字（Hard 是「類似」），已限縮；第四節 p2 的廠商宣稱移到「OpenAI 表示」之後；「更划算」改回原文的「成本效益比前代更好」；callout 與 FAQ 6 的否定句對齊正文範圍。
- 協調者裁定：1）「付費方案」全部改成方案名（description、summary 1、第一節 p1、圖 alt、node 1、caption 加定義、hero alt）；2）「兩代價格同時存在」限縮到 GPT-5.6 Sol 與 GPT-6 Sol（第二節 p4、FAQ 3）；3）第二段與第二節 p2 的查證紀律改成直接對讀者說的句子。
- 第一輪 14 處事實修改全部成立；它新寫的「changelog 只點名 Enterprise 管理員」字面成立、但會誤導，已刪；它補的「能不能用也取決於工作區設定」保留，冒號改分號（原文是兩個分開的敘述）。
- verbatim_quote：4/4 sources、48/48 verified_facts 在今天的正文是連續子字串；沒有含 `...`、`…`、`|` 的引文。
- 自檢：`check_article.py` → `OK ai-news-gpt-6-sol-luna-20260923 zh-TW paragraphs 2900`（exit 0）；`pack_cli lint` 只有 `image_missing` ×2 與 `raw_internal_url`（exit 1，皆為預期）。
- 結論：`needs_owner`（第 1 點要站主決定是否換來源補一句，發布當天三頁都要重讀）。

## 重抓結果（2026-09-26，UTC）

UA：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL --max-time 30`，同主機間隔 ≥1 秒，請求沒有任何個人資料。

| 時間 | 網址 | HTTP | 落地 bytes | 正文？ |
| --- | --- | --- | --- | --- |
| 14:53:55Z | https://openai.com/index/introducing-gpt-6-sol-and-luna/ | 200，0 轉址 | 846,851（第一輪 846,860、紀錄 846,857；可見文字與第一輪逐字相同） | 是 |
| 14:54:01Z | https://learn.chatgpt.com/docs/changelog | 200，0 | 1,542,032（與紀錄相同） | 是，9/22 條目逐字在 |
| 14:54:07Z | https://developers.openai.com/api/docs/pricing | 200，0 | 552,704（相同） | 是 |
| 14:54:19Z | https://deploymentsafety.openai.com/gpt-6-astra | 200，0 | 1,500,702（相同） | 是，第 11 節附錄 |
| 14:54:28Z | https://openai.com/news/rss.xml（只作日期依據） | 200 | 750,532 | 1,230 筆，最新 Fri, 25 Sep 2026 19:00:00 GMT；本篇 pubDate Tue, 22 Sep 2026 18:00:00 GMT |
| 14:54:31Z | https://chatgpt.com/pricing/（不在 sources，只用來反駁） | 200，0 | 1,079,963 | 是：方案卡、比較表、FAQ |
| 14:57:42Z | https://learn.chatgpt.com/codex/enterprise/workspace-model-availability（changelog 9/22 條目的連結，去掉錨點；不在 sources） | 200，1 轉址到 /docs/enterprise/workspace-model-availability | 352,212 | 是 |
| 15:03:38Z | https://deploymentsafety.openai.com/（不在 sources） | 200，0 | 54,846 | Updates 最新一筆仍是 Sep 08, 2026 |

四條來源的可見文字（`fc2_text.py`：html.parser、去註解、html.unescape）與第一輪的抽取逐字相同。

## 主張逐條

來源代號：A＝公告、C＝changelog 9/22 條目、P＝API 價目表、S＝GPT-6 Astra System Card、R＝RSS、W＝Workspace model availability（不在 sources）、G＝chatgpt.com/pricing（不在 sources）。

### A. 第一輪改動或新寫的句子（20）

| # | 位置 | 第一輪的結果 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| A1 | summary 2 | 「GPT-5.6 Sol 的促銷價」至少到 11/21 | CONFIRMED | P “GPT-5.6 Sol’s promotional pricing is available at least through November 21, 2026.”；raw HTML 的 promotional 2 次都是這一句（一次在頁面資料） |
| A2 | FAQ 3 | 同上 | CONFIRMED（句尾「新舊兩代」依裁定 2 改，見 C2） | P |
| A3 | 第二節 p4 | 「Sol 這邊拿來比較的促銷價現在仍然有效」「GPT-5.6 Luna 的促銷價，價目表沒有寫維持到哪一天」 | CONFIRMED（「兩個世代」依裁定 2 改） | P；全頁沒有 Luna 的促銷期限 |
| A4 | FAQ 6 | 刪「可以。」 | CONFIRMED（刪得對；剩下的句子範圍見 D16） | P 只撐 API 端 GPT-5.6 Sol |
| A5 | 第二節 p3 | 「公告寫」90% 折扣；價目表另列寫入快取 | CONFIRMED | A “discounts of 90% on cached input-token reads”；P「90%」0 次；P Cache writes 欄 |
| A6 | 第二節 p2 | 「在 Sol、Luna 兩列的降價欄都標示」 | CONFIRMED（後半依裁定 3 改寫，見 C3） | A 表頭 Model／Input／Output／Price reduction |
| A7 | 第五節 p3 | 「changelog 只點名 Enterprise 管理員，沒有寫 Business 或 Edu 是否也要先操作」 | **CHANGED（刪）** | 字面對 C 成立，但 C 同一條目的「Workspace model availability for administrator controls」連到 W，W 寫 “In Enterprise and Edu, an administrator must enable Luna first.”；留著會讓 Edu 讀者以為不用管理員 |
| A8 | 第一節 p3 | 補「能不能用也取決於工作區設定：」 | **CHANGED**：冒號改分號；其後原有的「官方沒有寫 Business 或 Edu 是否也要管理員操作」刪除（見 B55） | C “Availability depends on rollout and workspace settings; Enterprise administrators must enable the new models.”；W |
| A9 | 第四節 p4 | 「經長度調整的分數」持平或進步 | CONFIRMED（同段 45%／35% 的範圍見 D10） | S §11.4.1；Table 29 未調整分數 GPT-6 Sol Professional 59.5 對 GPT-5.6 Sol 64.1 |
| A10 | 第 1 段 | 「GPT-6 Astra 仍是 OpenAI 目前最好的模型」 | CONFIRMED | A “GPT‑6 Astra continues to be our best model across the board.”（OpenAI 對自家產品線的定位，在同段唯一的歸因「官方表示」之後） |
| A11 | 第三節 p3 | 「只是」→「則是比前代更划算」 | **CHANGED**：「更划算」→「成本效益比前代更好」 | A “offer more cost-efficient performance than their predecessors”；FACTCHECK.md 第 9 點把「比較划算」列為購買語氣 |
| A12 | 第一節 p4 | 「談 Sol 與 Luna 的開放範圍時都沒有提到台灣」 | CONFIRMED | 詞界比對 Taiwan：A 1（Keep reading 卡片）、C 0、P 0、S 0 |
| A13 | 第五節 p3 | 「四條官方來源都沒有寫 GPT-5.6 Sol 與 Luna 要下架」 | CONFIRMED | C 的 retire／deprecat 只有 GPT-5.5、5.4、5.3 與程式項目（“Remove the ultrafast service tier from gpt-5.6-sol” 是服務層級，不是下架）；P、S 沒有 5.6 的下架 |
| A14 | 表 caption | 「美國時間 9 月 22 日公告」 | CONFIRMED | R 18:00Z＝美國各時區仍是 9/22 |
| A15 | description | 句尾「（2026 年 9 月查證）」 | CONFIRMED | DELTA-4-7 第 14 條 |
| A16 | 兩段英文引文 | U+2011 改 ASCII | CONFIRMED | 內容包 U+2011、U+2060、NBSP 皆 0 次（DELTA-4-7 第 11 條） |
| A17 | 紀錄 | verified_facts 11/21 那條只講 GPT-5.6 Sol | CONFIRMED | P |
| A18 | 紀錄 | HealthBench fact 與 must_not_write 補「經長度調整」 | CONFIRMED | S Table 29 |
| A19 | 紀錄 | not_said 台灣條與 Keep reading 卡片 | CONFIRMED | A |
| A20 | 紀錄 | not_said Luna 降價欄「每個型號一格」 | CONFIRMED | A |

### B. 第一輪已確認的主張，隨機抽三分之一（54 條，編號沿用第一輪）

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 4 | description | 台北 9/23 凌晨 | CONFIRMED | R pubDate Tue, 22 Sep 2026 18:00:00 GMT＝台北 02:00 |
| 5 | description | 五個方案可在 Work、Codex 使用 | CONFIRMED（標籤依裁定 1 改） | A |
| 7 | description | Chat 裡還沒有 | CONFIRMED | A “These models are not yet available in Chat.” |
| 11 | 第 1 段 | 台北 9/23 凌晨（美國 9/22） | CONFIRMED | R |
| 13 | 第 1 段 | 訓練方法與 Astra 類似 | CONFIRMED | A “similar methods as GPT‑6 Astra” |
| 16 | 第 1 段 | 往下擴充、不是取代 Astra | CONFIRMED | A “expanding the GPT‑6 universe”；S “a highly capable, lower-cost alternative to Astra” |
| 22 | summary 1 | 五個方案當天起在 Work、Codex | CONFIRMED | A “starting today for all Plus, Pro, Business, Enterprise, and Edu users” |
| 23 | summary 1 | 免費與 Go 桌面 App 用 GPT-6 Luna | CONFIRMED（對 A、C）；G 相反，見待決 1 | A；C “Free and Go users can access Luna in the desktop app.” |
| 24 | summary 1 | 目前都還沒有在 Chat | CONFIRMED | A；C “but not Chat” |
| 26 | summary 2 | Sol 輸入 4 → 2 | CONFIRMED | A 表 |
| 34 | summary 3 | 成本只有 Opus 5 的 9% | **CHANGED**：來源有（A “at just 9% of Opus 5’s cost per task”），但正文沒有；summary 改用正文的「Opus 5 每項任務的成本是 Sol 的 11.1 倍」 | A 表 “11.1x GPT‑6 Sol”；SECOND-ROUND 第 4 項 summary ⊆ 正文 |
| 36 | summary 4 | 錯誤約前代一半 | CONFIRMED | A “about half as many mistakes” |
| 37 | summary 4 | 只測使用者標記的對話、不代表一般使用 | CONFIRMED | A |
| 46 | 一 p2 | 沒寫作業系統 | CONFIRMED | macOS、Windows：A 0、C 9/22 條目 0 |
| 52 | 一 p3 | 看不到請稍後再試 | CONFIRMED | A |
| 54 | 一 p3 | Enterprise 由管理員啟用 | CONFIRMED | C；W “off by default in Enterprise workspaces at launch” |
| 55 | 一 p3 | 官方沒有寫 Business 或 Edu 是否要管理員 | **NOT FOUND（被推翻）→ 刪** | W “In Enterprise and Edu, an administrator must enable Luna first.” |
| 58 | 一 p4 | 沒列國家或地區限制清單 | CONFIRMED（在句子自己的範圍內） | P 的 EU data residency 註記是處理方式、導覽列的 Supported countries 是連結文字，都不是 Sol／Luna 的開放名單 |
| 59 | 二 p1 | 引文 reducing … promotional pricing | CONFIRMED | A（U+2011 已改 ASCII） |
| 66 | 二 p3 | 長脈絡另有較高價格 | CONFIRMED | P Sol 4.00／0.40／5.00／15.00、Luna 0.20／0.02／0.25／0.75 |
| 67 | 二 p4 | GPT-5.6 Sol 促銷價至少到 11/21 | CONFIRMED | P |
| 71 | 表 | Luna 輸入 $0.10 | CONFIRMED | P |
| 73 | 表 | Luna 快取讀取 $0.01 | CONFIRMED | P |
| 74 | 表 | Sol 寫入快取 $2.50 | CONFIRMED | P |
| 81 | 表 caption | 短脈絡、Standard | CONFIRMED | P |
| 82 | 表 caption | 每百萬 token 美元 | CONFIRMED | P “Prices per 1M tokens.” |
| 90 | 三 p1 | Luna（high）多 5.4 個百分點 | CONFIRMED | A |
| 93 | 三 p1 | Fable 5.1 成本被低估 | CONFIRMED | A “understates its actual cost” |
| 97 | 三 p2 | 成本低 60% | CONFIRMED | A “at 60% lower cost per task”（原文沒有 approximately，正文也沒有「約」） |
| 98 | 三 p2 | DeepSWE Sol（max）68.8% | CONFIRMED | A |
| 99 | 三 p2 | Fable 5 最高分 69.9%（xhigh） | CONFIRMED | A |
| 102 | 三 p3 | 研究環境或 API、可能與正式版略有差異 | CONFIRMED | A 註腳 |
| 106 | 圖 caption | 依美國時間 9/22 公告與 changelog | CONFIRMED | A、C |
| 107 | 圖 caption | 查核日 2026-09-26 | CONFIRMED | 紀錄 |
| 110 | node 3 | Chat 模式尚未提供 | CONFIRMED | A、C |
| 113 | 四 p1 | 內部評測用使用者標記過錯誤的真實對話 | CONFIRMED | A |
| 115 | 四 p1 | 接近 Astra 等級、成本低得多 | CONFIRMED | A |
| 116 | 四 p1 | 不代表一般使用 | CONFIRMED | A |
| 120 | 四 p2 | 成本約百分之一 | CONFIRMED | A “about a hundredth its cost” |
| 123 | 四 p3 | 不是另一份獨立的 system card | CONFIRMED | A 的「system card」連結指向 deploymentsafety.openai.com/gpt-6-astra；DSH 首頁 15:03Z 最新仍是 Sep 08 |
| 127 | 四 p3 | 與 GPT-5.6 Sol／Luna 相同 | CONFIRMED | S §11.8 “These are the same capability determinations we made for GPT-5.6 Sol and GPT-5.6 Luna.” |
| 128 | 四 p3 | 沿用同一套防護 | CONFIRMED | S §11、§11.8 |
| 134 | 五 p1 | 看模型選單；逐步推出 | CONFIRMED | A；C “Choose a model in the picker when available.” |
| 137 | 五 p2 | codex --model gpt-6-sol／gpt-6-luna | CONFIRMED | C |
| 141 | 五 p3 | 沒寫 Business、Edu（第一輪改成 changelog） | **CHANGED（刪）** | 同 A7 |
| 146 | FAQ 1 | Free 與 Go 桌面 App 用 Luna | CONFIRMED（G 相反，見待決 1） | A、C |
| 150 | FAQ 1 | 沒寫網頁或手機版 | CONFIRMED（對 A、C）；同句「官方沒有寫 Sol…」見 D11 | A、C |
| 151 | FAQ 2 | 還沒有 | CONFIRMED | A、C |
| 154 | FAQ 3 | 跟各自的 GPT-5.6 促銷價比 | CONFIRMED | A |
| 157 | FAQ 3 | 新舊兩代價格同時存在 | **CHANGED**（裁定 2） | P 可見文字只有 gpt-5.6-sol（Cyber models 表 $4.00／$20.00） |
| 160 | FAQ 4 | Fable 5.1 缺分數用 Fable 5 | CONFIRMED（正文原本沒有，見 D15） | A “Scores for Claude Fable 5 were reported when scores for Claude Fable 5.1 were unavailable.” |
| 163 | FAQ 5 | 公告、changelog、價目表沒提地區限制 | CONFIRMED | P 的 EU data residency 限制是處理方式的選項，不是地區開放限制 |
| 170 | callout | 逐步推出 | CONFIRMED | A |
| 179 | sources | checked_on 全部 2026-09-26 | CONFIRMED | 內容包、紀錄一致 |

### C. 協調者裁定（3）

| # | 裁定 | 做了什麼 | 依據 |
| --- | --- | --- | --- |
| C1 | Go 是付費方案，不再用「付費方案」對照「免費與 Go」 | description、summary 1、第一節 p1 寫方案名；圖 alt、record node 1 改「Plus、Pro 等方案」（8.4／9 單位），caption（內容包與紀錄同步、仍相等）加「（「Plus、Pro 等方案」指 Plus、Pro、Business、Enterprise、Edu）」；hero alt 改方案名。沒有用「Plus 以上」：沒有來源支持這個分組 | G FAQ “Paid plans (Go, Plus, Business, and Enterprise) are priced per user per month.”；A 的方案清單 |
| C2 | 「兩代價格同時存在」只講 GPT-5.6 Sol | 第二節 p4、FAQ 3 改「GPT-5.6 Sol 與 GPT-6 Sol 兩個世代的價格現在同時存在」 | P 可見文字：Cyber models 表 gpt-5.6-sol、Flagship 表 gpt-6-sol |
| C3 | 查證紀律改成直接說話 | 第二段刪「資料來自…」改「價格與開放範圍以當天 OpenAI 頁面寫的為準」；第二節 p2 刪「照表印的數字寫，不自己計算或推論百分比，也不是說 OpenAI 標錯」，改「其中 Luna 的輸出價，表上印的是從 1.20 美元降到 0.50 美元」 | DELTA-4-7 第 14 條 |

### D. 回掃：但書、否定句、歸因、summary 與 FAQ（20）

| # | 項目 | 判定 | 依據 |
| --- | --- | --- | --- |
| D1 | description 的 50% 帶促銷價基準 | CONFIRMED | A |
| D2 | summary 2 的 50% 帶基準 | CONFIRMED | A |
| D3 | 第二節標題與 p1 帶基準 | CONFIRMED | A |
| D4 | FAQ 3、callout 帶基準 | CONFIRMED | A |
| D5 | gradually：summary 5、一 p3、五 p1、callout | CONFIRMED | A “gradually throughout the day”；C “rolling out” |
| D6 | depends on workspace settings：一 p3 | CONFIRMED | C |
| D7 | length-adjusted：四 p4 | CONFIRMED | S |
| D8 | up to：四條來源的相關句子沒有 up to；配套文的「up to 90%」不是來源，正文照主文並寫「公告寫」 | CONFIRMED | A |
| D9 | 約／~：約一半、約 40%、約低 80%、約百分之一、約 45%／35% 都帶「約」 | CONFIRMED | A、S |
| D10 | 四 p4「平均回答長度 Sol 約減少 45%、Luna 約減少 35%」接在 HealthBench 與 Hard 之後 | **CHANGED**：限縮為 HealthBench 的數字，Hard「也有類似的減少」 | S “On HealthBench, mean answer lengths decrease by approximately 45% for Sol and 35% for Luna, with similar reductions on HealthBench Hard.” |
| D11 | FAQ 1「官方沒有寫 Sol 是不是也開放給免費或 Go 帳號」 | **CHANGED**：改「公告與 changelog 都只提到 Luna、沒有提到 Sol」（與一 p2 同範圍） | G 比較表 GPT-6 Sol：Free No、Go No |
| D12 | callout「官方也沒有提到台灣或其他地區的時程」 | **CHANGED**：「官方公告也沒有提到」（與 summary 5、五 p4 同範圍） | SECOND-ROUND 第 4 項 |
| D13 | 四 p2「GPT-6 Luna 在事實性上也大幅進步」在歸因之前 | **CHANGED**：「OpenAI 表示 GPT-6 Luna 在事實性上也大幅進步：」 | A “GPT‑6 Luna also improves substantially”；BRIEF 第 10 條 |
| D14 | summary 1、2、4、5 ⊆ 正文 | CONFIRMED | 各節 |
| D15 | FAQ 4 的 Fable 5 代替規則 ⊆ 正文 | **CHANGED**：三 p3 加「Claude Fable 5.1 沒有分數時則改報 Fable 5 的分數」（在同段「OpenAI 寫明」之下，該段歸因仍是兩個） | A 註腳 |
| D16 | FAQ 6「GPT-5.6 系列要下架或停用」比正文寬 | **CHANGED**：「GPT-5.6 Sol 與 Luna 要下架或停用」 | 五 p3 |
| D17 | FAQ 2「changelog 也寫還沒有在 Chat」 | CONFIRMED（核心句在一 p3；changelog 那句屬實） | C “but not Chat” |
| D18 | 標題與 summary 1：免費與 Go 可在桌面 App 用 Luna | **OPEN**（未改，照兩條 sources） | A、C 對 G 比較表的「No」，見待決 1 |
| D19 | 界線：topics 無 finance、只有一個 callout、無訂閱／購買／升級建議、無推定台灣可用、Opus 5.5 0 次、「本文」0 次 | CONFIRMED | 內容包 |
| D20 | 兩個結尾連結文字與目標 | CONFIRMED | `check_article.py` OK |

合計 97：CONFIRMED 80、CHANGED 15、NOT FOUND 1、OPEN 1。

## 改掉的地方（原文 → 改成，依據）

事實修改（10 處）：

1. 第一節 p3：「能不能用也取決於工作區設定：Enterprise 方案要先由管理員啟用，官方沒有寫 Business 或 Edu 是否也要管理員操作。」→「能不能用也取決於工作區設定；Enterprise 方案要先由管理員啟用。」https://learn.chatgpt.com/docs/enterprise/workspace-model-availability（changelog 9/22 條目的連結）“In Enterprise and Edu, an administrator must enable Luna first.”
2. 第五節 p3：「要先請管理員啟用新模型；changelog 只點名 Enterprise 管理員，沒有寫 Business 或 Edu 是否也要先操作。」→「要先請管理員啟用新模型。」同上。
3. FAQ 1：「官方沒有寫 Sol 是不是也開放給免費或 Go 帳號」→「公告與 changelog 都只提到 Luna、沒有提到 Sol」。https://chatgpt.com/pricing/ 比較表 GPT-6 Sol：Free No、Go No。
4. callout：「官方也沒有提到台灣或其他地區的時程」→「官方公告也沒有提到台灣或其他地區的時程」。https://openai.com/index/introducing-gpt-6-sol-and-luna/
5. summary 3：「每項任務成本只有 Opus 5 的 9%」→「Opus 5 每項任務的成本是 Sol 的 11.1 倍」。同上（表 “Claude Opus 5 (max) 26.9% 11.1x GPT‑6 Sol”；正文第三節 p1 用的是 11.1 倍）。
6. 第三節 p3：「可能與正式版 ChatGPT 略有差異；」→「可能與正式版 ChatGPT 略有差異，Claude Fable 5.1 沒有分數時則改報 Fable 5 的分數；」。同上註腳。
7. 第三節 p3：「Sol 與 Luna 則是比前代更划算」→「Sol 與 Luna 則是成本效益比前代更好」。同上 “more cost-efficient performance than their predecessors”。
8. 第四節 p2：「GPT-6 Luna 在事實性上也大幅進步：OpenAI 表示在較高的推理設定下，」→「OpenAI 表示 GPT-6 Luna 在事實性上也大幅進步：在較高的推理設定下，」。同上 “GPT‑6 Luna also improves substantially”。
9. 第四節 p4：「退步、回答明顯變短：平均回答長度 Sol 約減少 45%、Luna 約減少 35%。」→「退步、回答明顯變短：HealthBench 的平均回答長度 Sol 約減少 45%、Luna 約減少 35%，HealthBench Hard 也有類似的減少。」https://deploymentsafety.openai.com/gpt-6-astra §11.4.1。
10. FAQ 6：「都沒有寫 GPT-5.6 系列要下架或停用。」→「都沒有寫 GPT-5.6 Sol 與 Luna 要下架或停用。」https://learn.chatgpt.com/docs/changelog（FAQ ⊆ 正文）。

依裁定（11 處）：

- 裁定 1：description「推出 GPT-6 Sol 與 GPT-6 Luna：付費方案可在 ChatGPT Work、Codex 使用，免費與 Go 使用者能在桌面 App 用 Luna，…，文中整理開放範圍、價格基準與 OpenAI 自選的評測比較」→「推出 GPT-6 Sol 與 Luna：Plus、Pro、Business、Enterprise、Edu 可在 ChatGPT Work、Codex 使用，免費與 Go 能在桌面 App 用 Luna，…，並列出 OpenAI 自選的評測」（198 字；騰字只刪重複的敘述與內容清單，基準、「Chat 裡還沒有」、查證尾巴都在）；summary 1「付費方案（Plus、Pro、Business、Enterprise、Edu）」→「Plus、Pro、Business、Enterprise、Edu 方案」；第一節 p1「這些付費方案，」→「方案」；圖 alt「在付費方案、免費與 Go、Chat 與 API」→「在 Plus、Pro 等方案，以及免費與 Go、Chat、API」；紀錄 node 1「付費方案」→「Plus、Pro 等方案」；caption（內容包＝紀錄）加「（「Plus、Pro 等方案」指 Plus、Pro、Business、Enterprise、Edu）」；hero alt「多種付費方案與工具」→「Plus、Pro、Business、Enterprise、Edu 方案與工具」。
- 裁定 2：第二節 p4「兩個世代的價格現在同時存在」、FAQ 3「新舊兩個世代的價格現在同時存在」→「GPT-5.6 Sol 與 GPT-6 Sol 兩個世代的價格現在同時存在」。https://developers.openai.com/api/docs/pricing
- 裁定 3：第二段「這篇的內容在 2026 年 9 月 26 日查核，資料來自 OpenAI 官方公告、changelog、API 價目表與 System Card 附錄；」→「這一篇的資料在 2026 年 9 月 26 日查核，價格與開放範圍以當天 OpenAI 頁面寫的為準；」；第二節 p2「Luna 輸出印的是從 1.20 美元降到 0.50 美元，照表印的數字寫，不自己計算或推論百分比，也不是說 OpenAI 標錯。」→「其中 Luna 的輸出價，表上印的是從 1.20 美元降到 0.50 美元。」

研究紀錄（7 處＋`factcheck.second_round`）：node 1 與 `diagram.caption`（同上）；verified_facts 電腦操作那條的「更划算」改「成本效益比前代更好」並註明原文；not_said「管理員啟用」與對應的 must_not_write 補 W 的 Edu 句，禁止寫回「官方沒有寫 Business 或 Edu」；unverified_or_excluded 加 G（比較表的 No、Go 是付費方案）與 W 兩條；live_data_warnings 加方案頁與公告矛盾、發布當天三頁重讀。`title` 沒改。editorial_brief 仍寫「付費方案（…）」與「兩代價格現在並存」，那是撰稿指示，當作歷史沒改。

## 待決（給協調者／站主）

1. **方案頁與公告矛盾**：G 比較表 GPT-6 Luna、GPT-6 Sol 在 Free、Go 都是「No」，GPT-5.6 Terra 在 Free、Go 是「Limited access in Work and Codex on desktop」；A、C 寫 Free 與 Go 可在桌面 App 用 GPT-6 Luna。多半是方案頁還沒更新，但兩頁都是 OpenAI 官方。正文照 sources 寫並在第一節 p2 引原文歸因；要在正文交代這個矛盾，得換掉一條 source（四條都在用）。發布當天重讀 G、A 的 Availability 段、C 的 9/22 條目。
2. **Edu 管理員**：W 寫 Enterprise 與 Edu 的 Luna 要管理員先啟用（在 GPT-5.4 退役一節）。第二輪選擇刪否定句、不寫 Edu；若要寫 Edu，同樣要換 source。
3. 圖 node 1「Plus、Pro 等方案」靠 caption 定義；畫圖時若能放下完整五個方案名，caption 的括號可以拿掉（內容包與紀錄要一起改）。
4. hero alt 依裁定 1 的「anywhere else」改了；agents/ai/FACTCHECK.md 原本把 hero alt 留給協調者，畫完照實際畫面重寫即可。

## 讀者優先檢查

- 「本文」0 次；「本站」在 FAQ 4 與 callout。
- 開頭段只有一個歸因語（「官方表示」）；正文每段最多兩個（第三節 p1、p3 各兩個，這次加的句子沒有新增歸因語）。
- 兩句查證紀律（第二段、第二節 p2）已改成直接說話；description 只剩「（2026 年 9 月查證）」；title、description、summary 沒有選題計數。
- 「官方」開頭的否定句都收到了具體頁面（第一節 p4 與 FAQ 5 的「官方未說明」後面緊接著四條／三頁的範圍）。

## 自檢

- `PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py ai-news-gpt-6-sol-luna-20260923` → `OK ai-news-gpt-6-sol-luna-20260923 zh-TW paragraphs 2900`，exit 0（`_tools/…/fc2_check_article.log`）
- `./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life --slug ai-news-gpt-6-sol-luna-20260923` → `raw_internal_url`（warning）、`image_missing` hero.jpg、diagram-1.svg，exit 1，皆為預期（`fc2_pack_lint.log`）
- `fc2_quotes.py`（改完重跑）：TOTAL BAD 0、SPLICED QUOTES 0

## 結論

`needs_owner`：文章在四條 sources 的範圍內成立，第一輪的 14 處修改都站得住；但 OpenAI 的方案頁今天與標題的核心主張（免費與 Go 可用 GPT-6 Luna）相反，要站主決定是否換來源交代，並在發布當天重讀。
