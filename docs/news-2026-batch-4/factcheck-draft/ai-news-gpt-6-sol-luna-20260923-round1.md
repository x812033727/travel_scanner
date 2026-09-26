# 查核報告（第一輪）：ai-news-gpt-6-sol-luna-20260923

- 查核者：獨立查核代理（第一輪，opus），2026-09-26（台北）
- 規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/ai/FACTCHECK.md`、DELTA-4-8（全）、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF.md 十二條錯誤型態
- 改動的檔案：內容包 `apps/api/app/guides/content/ai-news-gpt-6-sol-luna-20260923.json`、研究紀錄 `docs/ai-news-2026-09-late/research/ai-news-gpt-6-sol-luna-20260923.json`（加 `factcheck`）
- 腳本：`_tools/ai-news-gpt-6-sol-luna-20260923/fc1_fetch.sh`、`fc1_text.py`、`fc1_quotes.py`、`fc1_apply.py`、`fc1_fix_method.py`；原始回應在 `_raw/ai-news-gpt-6-sol-luna-20260923/round1/`

## 摘要

- 主張 180 條：CONFIRMED 161、CHANGED 13、NOT FOUND 1（已刪）、OUT OF SCOPE 5。
- **事實修改 14 處**（13 CHANGED ＋ 1 NOT FOUND 刪除），另有 2 處非事實的格式修正（description 句尾、U+2011）。研究紀錄改 5 處並加 `factcheck`。
- 最重的五處：
  1. 「至少維持到 2026 年 11 月 21 日」被套到 Sol 與 Luna 兩個促銷價（summary 2、第二節 p4、FAQ 3）；價目表只寫 **GPT-5.6 Sol’s** promotional pricing。已限縮到 Sol，並寫明價目表沒寫 Luna 促銷價的期限。FAQ 6 的「可以。」一併刪除。
  2. 「價目表也顯示…90% 折扣」：價目表全頁沒有「90%」，這個數字出自公告。改成「公告寫」。
  3. HealthBench：Professional 與 Consensus「持平或進步」掉了 **length-adjusted**；Table 29 未調整分數 GPT-6 Sol 在 Professional 是 59.5，低於 GPT-5.6 Sol 的 64.1，限定詞不能省。
  4. 「公告與 changelog 都只點名 Enterprise 管理員」：公告全文沒有 admin（0 次），只有 changelog 寫。另補回 changelog 的限定詞「能不能用取決於推出進度與工作區設定」。
  5. 「公告的價格表把 Sol、Luna 的輸入與輸出都標示為 50% cheaper」：表上是每個型號一格 Price reduction，不是輸入、輸出各標一次。
- 協調者指定的重點：標題兩個子句都成立、沒有「只」；逐步推出有寫；台灣／地區寫「官方未說明」；每個「50%」都帶 GPT-5.6 促銷價基準；表格價格與今天的價目表、公告逐格相同；快取 90% 只講讀取、寫入較貴；Claude／Fable 比較都歸因 OpenAI，三個註腳都在（公開報告、Fable 5 代 5.1 在 FAQ 4、成本被低估）；剩下的評測數字逐字對上；「錯誤減半」限縮在使用者標記的對話；HealthBench 退步有寫；Preparedness High 標明是內部分級；安全內容是 Astra System Card 第 11 節附錄；日期行「台北時間 9 月 23 日凌晨（美國時間 9 月 22 日）」與 RSS pubDate 18:00Z 一致；全文沒有 Opus 5.5。
- 自檢：`check_article.py` → `OK ai-news-gpt-6-sol-luna-20260923 zh-TW paragraphs 2940`（exit 0）；`pack_cli lint` 只有 `image_missing` ×2 與 `raw_internal_url`（exit 1，皆為預期）。
- 結論：`needs_second_round`（事實改了 14 處，超過十處）。

## 重抓結果（2026-09-26，UTC）

UA：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL --max-time 30`，同主機間隔 ≥1 秒，請求沒有任何個人資料。

| 時間 | 網址 | HTTP | 落地 bytes | 正文？ |
| --- | --- | --- | --- | --- |
| 14:34:26Z | https://openai.com/index/introducing-gpt-6-sol-and-luna/ | 200，0 轉址 | 846,860（紀錄 846,857；可見文字與研究代理的抽取完全相同） | 是：價格表、AutomationBench 表、各節、Availability、註腳 |
| 14:34:27Z | https://learn.chatgpt.com/docs/changelog | 200，0 | 1,542,032（與紀錄相同） | 是：逐日條目，最新 2026-09-26；9/22 條目逐字在 |
| 14:34:29Z | https://developers.openai.com/api/docs/pricing | 200，0 | 552,704（相同） | 是：Flagship 表四個分頁與註記 |
| 14:34:30Z | https://deploymentsafety.openai.com/gpt-6-astra | 200，0 | 1,500,702（相同） | 是：變更紀錄、第 11 節附錄 |
| 14:34:35Z | https://openai.com/news/rss.xml（只用於日期） | 200 | 750,532 | 1,230 筆，最新 Fri, 25 Sep 2026 19:00:00 GMT |
| 14:34:37Z | https://openai.com/index/better-prompt-caching-for-gpt-6/（不在 sources） | 200 | 434,819 | 是（這次沒有 403） |
| 14:34:39Z | https://deploymentsafety.openai.com/（不在 sources） | 200 | 54,846 | Updates 最新一筆仍是 Sep 08, 2026 |
| 14:34:40Z | https://developers.openai.com/api/docs/models（不在 sources） | 200 | 369,017 | 是 |
| 14:41:24Z | https://openai.com/chatgpt/pricing/ → https://chatgpt.com/pricing/（不在 sources） | 200，2 轉址 | 993,948 | 是，只用來回答 Go 是否為付費方案（見待決 1） |

`verbatim_quote` 逐字比對（`fc1_quotes.py`，html.parser、去註解、html.unescape、只壓 ASCII 空白，NBSP／U+2011／U+2060 不動）：4/4 sources、48/48 verified_facts 都是連續子字串。修改後重跑仍為 0 BAD。

## 主張逐條

來源代號：A＝公告、C＝changelog 9/22 條目、P＝API 價目表、S＝GPT-6 Astra System Card、R＝OpenAI RSS（只作日期依據）。

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | GPT-6 Sol 與 Luna 推出 | CONFIRMED | A “expanding the GPT‑6 universe with GPT‑6 Sol and GPT‑6 Luna” |
| 2 | title | 免費與 Go 可在桌面 App 用 Luna（沒有「只」） | CONFIRMED | A “Free and Go users can access GPT‑6 Luna in the desktop app.”；C 同 |
| 3 | title | Chat 裡還沒有 | CONFIRMED | A “These models are not yet available in Chat.”；C “but not Chat” |
| 4 | description | 台北時間 2026-09-23 凌晨 | CONFIRMED | R pubDate Tue, 22 Sep 2026 18:00:00 GMT＝台北 02:00 |
| 5 | description | 付費方案可在 Work、Codex 使用 | CONFIRMED（標籤見待決 1） | A Availability |
| 6 | description | 免費與 Go 在桌面 App 用 Luna | CONFIRMED | A |
| 7 | description | Chat 裡還沒有 | CONFIRMED | A |
| 8 | description | API 比 GPT-5.6 促銷價便宜 50% | CONFIRMED | A “by 50% compared with their GPT‑5.6 promotional pricing” |
| 9 | description | OpenAI 自選的評測比較 | CONFIRMED | 紀錄 verified_facts #23；A |
| 10 | description | 句尾「（2026 年 9 月查核）」 | OUT OF SCOPE → 讀者優先規則改「查證」 | DELTA-4-7 第 14 條；FACTCHECK-48 |
| 11 | 第 1 段 | 台北 9/23 凌晨（美國 9/22） | CONFIRMED | R；A 頁面資料 publicationDateText “September 22” |
| 12 | 第 1 段 | 兩個新模型 | CONFIRMED | A |
| 13 | 第 1 段 | 訓練方法與 Astra 類似 | CONFIRMED | A “similar methods as GPT‑6 Astra” |
| 14 | 第 1 段 | 把 Astra 的部分進展帶到更快、更便宜的型號 | CONFIRMED | A “bringing the advances … to faster, more affordable models” |
| 15 | 第 1 段 | Astra 仍是目前最好的模型 | **CHANGED** → 「仍是 OpenAI 目前最好的模型」 | A “GPT‑6 Astra continues to be **our** best model across the board.” |
| 16 | 第 1 段 | 往下擴充、不是取代 Astra | CONFIRMED | 紀錄 fact #2；A |
| 17 | 第 2 段 | 2026-09-26 查核 | CONFIRMED | 紀錄 checked_on |
| 18 | 第 2 段 | 資料來自公告、changelog、價目表、System Card 附錄 | CONFIRMED | sources[] |
| 19 | 第 2 段 | 評測數字都是 OpenAI 公布 | CONFIRMED | A 註腳 |
| 20 | 第 2 段 | 網站沒實測、不是採購或投資建議 | OUT OF SCOPE | 編輯聲明 |
| 21 | summary 1 | 日期兩時區 | CONFIRMED | R、A |
| 22 | summary 1 | Plus、Pro、Business、Enterprise、Edu 當天起在 Work 與 Codex | CONFIRMED | A “starting today for all Plus, Pro, Business, Enterprise, and Edu users” |
| 23 | summary 1 | 免費與 Go 桌面 App 用 GPT-6 Luna | CONFIRMED | A |
| 24 | summary 1 | 目前都還沒有在 Chat | CONFIRMED（今天重抓仍是 not yet） | A、C |
| 25 | summary 2 | 基準是各自的 GPT-5.6 促銷價 | CONFIRMED | A |
| 26 | summary 2 | Sol 輸入 4 → 2 | CONFIRMED | A 表 “$4 → $2” |
| 27 | summary 2 | Sol 輸出 20 → 10 | CONFIRMED | A “$20 → $10” |
| 28 | summary 2 | Luna 輸入 0.20 → 0.10 | CONFIRMED | A |
| 29 | summary 2 | Luna 輸出 1.20 → 0.50 | CONFIRMED | A |
| 30 | summary 2 | OpenAI 都標 50% cheaper | CONFIRMED | A 兩列 Price reduction |
| 31 | summary 2 | 「這個促銷價」至少維持到 2026-11-21（指兩個） | **CHANGED** → 「GPT-5.6 Sol 的促銷價」 | P “GPT-5.6 Sol’s promotional pricing is available at least through November 21, 2026.”（全頁 promotional 只有這一句） |
| 32 | summary 3 | AutomationBench Sol（xhigh）33.2% | CONFIRMED | A 表 |
| 33 | summary 3 | Opus 5（max）26.9% | CONFIRMED | A 表 |
| 34 | summary 3 | 成本只有 Opus 5 的 9% | CONFIRMED | A “at just 9% of Opus 5’s cost per task” |
| 35 | summary 3 | OpenAI 自選、對手分數取自公開報告 | CONFIRMED | A 註腳 |
| 36 | summary 4 | Sol 事實錯誤約前代一半 | CONFIRMED | A |
| 37 | summary 4 | 只測使用者標記過的對話、不代表一般使用 | CONFIRMED | A “not representative of typical usage” |
| 38 | summary 4 | 資安與生物化學 High capability | CONFIRMED | S §11、§11.8 |
| 39 | summary 4 | OpenAI 內部框架的分級 | CONFIRMED | S “Under our Preparedness Framework” |
| 40 | summary 4 | 與 GPT-5.6 Sol／Luna 相同 | CONFIRMED | S §11.8 “These are the same capability determinations …” |
| 41 | summary 5 | 公告沒提台灣或地區的開放時程 | CONFIRMED | A（唯一的 Taiwan 在 Keep reading 卡片標題，與時程無關） |
| 42 | summary 5 | 看不到就稍後再試 | CONFIRMED | A |
| 43 | summary 5 | Enterprise 要管理員先啟用 | CONFIRMED | C |
| 44 | 一 p1 | 五個方案從公告當天起在 Work、Codex | CONFIRMED | A |
| 45 | 一 p2 | 引文 Free and Go …（U+2011 改 ASCII） | CONFIRMED | A |
| 46 | 一 p2 | 沒寫作業系統 | CONFIRMED | A、C 9/22 條目 macOS／Windows／iOS／Android 皆 0 次 |
| 47 | 一 p2 | 沒寫 Work 還是 Codex | CONFIRMED | A、C |
| 48 | 一 p2 | 沒寫網頁或手機版 | CONFIRMED | A（mobile 1 次在範例對話）、C 0 次 |
| 49 | 一 p2 | 兩頁都只提 Luna、沒提 Sol | CONFIRMED | A、C |
| 50 | 一 p3 | 引文 not yet available in Chat | CONFIRMED | A |
| 51 | 一 p3 | 當天逐步推出 | CONFIRMED | A “gradually throughout the day” |
| 52 | 一 p3 | 看不到請稍後再試 | CONFIRMED | A |
| 53 | 一 p3 | （掉了）能不能用取決於推出進度與工作區設定 | **CHANGED**：補「能不能用也取決於工作區設定：」 | C “Availability depends on rollout and workspace settings” |
| 54 | 一 p3 | Enterprise 由管理員啟用 | CONFIRMED | C |
| 55 | 一 p3 | 沒寫 Business、Edu 是否要管理員 | CONFIRMED | C |
| 56 | 一 p4 | 地區「官方未說明」 | CONFIRMED | A、C、P、S |
| 57 | 一 p4 | 四條來源都沒有提到台灣 | **CHANGED** → 「談 Sol 與 Luna 的開放範圍時都沒有提到台灣」 | A 頁尾 Keep reading 卡片〈ChatGPT Ads expands to Southeast Asia and Taiwan〉 |
| 58 | 一 p4 | 沒列國家或地區限制清單 | CONFIRMED | P 只有 EU data residency 的處理方式註記，不是開放名單 |
| 59 | 二 p1 | 引文 reducing … promotional pricing（U+2011 改 ASCII） | CONFIRMED | A |
| 60 | 二 p1 | 基準是促銷價、不是原價 | CONFIRMED | A “promotional pricing” |
| 61 | 二 p2 | 表把輸入與輸出都標 50% cheaper | **CHANGED** → 「在 Sol、Luna 兩列的降價欄都標示」 | A 表欄位 Model／Input／Output／Price reduction，每列一格 |
| 62 | 二 p2 | Luna 輸出 1.20 → 0.50 | CONFIRMED | A |
| 63 | 二 p3 | 「價目表也顯示」90% 折扣 | **CHANGED** → 「公告寫」 | A “discounts of 90% on cached input-token reads”；P 全頁「90%」0 次 |
| 64 | 二 p3 | 寫入快取比一般輸入貴 | CONFIRMED | P Cache writes 欄 |
| 65 | 二 p3 | Sol 寫入 2.50、輸入 2 | CONFIRMED | P |
| 66 | 二 p3 | 長脈絡另有較高價格 | CONFIRMED | P Long context 欄 |
| 67 | 二 p4 | GPT-5.6 Sol 促銷價至少到 2026-11-21 | CONFIRMED | P |
| 68 | 二 p4 | 「這次公告拿來比較的促銷價」（兩個）仍有效 | **CHANGED** → 限 Sol，並寫「GPT-5.6 Luna 的促銷價，價目表沒有寫維持到哪一天」 | P |
| 69 | 二 p4 | 兩個世代的價格同時存在 | CONFIRMED | P 可見文字 Cyber models 表 gpt-5.6-sol $4.00／$20.00；All models 資料另列 gpt-5.6-luna 0.2／1.2（見待決 2） |
| 70 | 表 | Sol 輸入 $2.00 | CONFIRMED | P Standard 短脈絡 |
| 71 | 表 | Luna 輸入 $0.10 | CONFIRMED | P |
| 72 | 表 | Sol 快取讀取 $0.20 | CONFIRMED | P |
| 73 | 表 | Luna 快取讀取 $0.01 | CONFIRMED | P |
| 74 | 表 | Sol 寫入快取 $2.50 | CONFIRMED | P |
| 75 | 表 | Luna 寫入快取 $0.125 | CONFIRMED | P |
| 76 | 表 | Sol 輸出 $10.00 | CONFIRMED | P |
| 77 | 表 | Luna 輸出 $0.50 | CONFIRMED | P |
| 78 | 表 | GPT-5.6 Sol 促銷價 $4／$20 | CONFIRMED | A 表；P |
| 79 | 表 | GPT-5.6 Luna 促銷價 $0.20／$1.20 | CONFIRMED | A 表；P All models 資料 |
| 80 | 表 caption | 「9 月 22 日公告」 | **CHANGED** → 「美國時間 9 月 22 日公告」 | R、DELTA-4-8 第 4 條（跨日文章兩個日期） |
| 81 | 表 caption | 短脈絡、Standard 分頁 | CONFIRMED | P |
| 82 | 表 caption | 每百萬 token 美元 | CONFIRMED | P “Prices per 1M tokens.” |
| 83 | 表 caption | 查核日 2026-09-26 | CONFIRMED | 紀錄 |
| 84 | 表 caption | 長脈絡另有較高價格 | CONFIRMED | P |
| 85 | 三 p1 | AutomationBench＝跨 App 商務流程測試 | CONFIRMED | A “a test of business workflows across apps” |
| 86 | 三 p1 | 自選 | CONFIRMED | 紀錄 |
| 87 | 三 p1 | Sol（xhigh）33.2% | CONFIRMED | A |
| 88 | 三 p1 | Opus 5（max）26.9% | CONFIRMED | A |
| 89 | 三 p1 | Opus 5 成本是 Sol 的 11.1 倍 | CONFIRMED | A “11.1x GPT‑6 Sol” |
| 90 | 三 p1 | Luna（high）比前代多 5.4 個百分點 | CONFIRMED | A |
| 91 | 三 p1 | 每項任務成本低 58% | CONFIRMED | A |
| 92 | 三 p1 | 對手分數取自公開報告 | CONFIRMED | A 註腳 |
| 93 | 三 p1 | Fable 5.1 成本被低估 | CONFIRMED | A “understates its actual cost” |
| 94 | 三 p1 | 約 40% 任務改用 Opus 5 備援 | CONFIRMED | A “~40% of tasks” |
| 95 | 三 p2 | Agents’ Last Exam Sol（max）56.4% | CONFIRMED | A |
| 96 | 三 p2 | 高於 Opus 5 的最高分 | CONFIRMED | A |
| 97 | 三 p2 | 成本低 60% | CONFIRMED | A |
| 98 | 三 p2 | DeepSWE v1.1 Sol（max）68.8% | CONFIRMED | A |
| 99 | 三 p2 | Fable 5 最高分 69.9%（xhigh） | CONFIRMED | A（比的是 Fable 5） |
| 100 | 三 p2 | 差 1.1 個百分點 | CONFIRMED | A “within 1.1 percentage points” |
| 101 | 三 p2 | 成本約低 80% | CONFIRMED | A |
| 102 | 三 p3 | 研究環境或 API、可能與正式版 ChatGPT 略有差異 | CONFIRMED | A 註腳 |
| 103 | 三 p3 | Astra 是電腦操作最好的模型（OpenAI 稱） | CONFIRMED | A “remains the world’s best model for computer use” |
| 104 | 三 p3 | Sol 與 Luna「只是」比前代更划算 | **CHANGED**：「只是」→「則是」 | A “offer more cost-efficient performance than their predecessors”（沒有 only） |
| 105 | 三 p3 | 不是取代 Astra | CONFIRMED | 紀錄 fact #2 |
| 106 | 圖 caption | 依美國時間 9/22 公告與 changelog | CONFIRMED | A、C |
| 107 | 圖 caption | 查核日 2026-09-26 | CONFIRMED | 紀錄 |
| 108 | diagram 1 | 付費方案：Work 與 Codex 可選用 | CONFIRMED（標籤見待決 1） | A |
| 109 | diagram 2 | 免費與 Go：桌面 App 可用 Luna | CONFIRMED | A |
| 110 | diagram 3 | Chat 模式：兩個新模型尚未提供 | CONFIRMED | A、C |
| 111 | diagram 4 | API：gpt-6-sol 與 gpt-6-luna | CONFIRMED | A |
| 112 | diagram title／hero_label | 在哪裡用得到／Astra 之下的兩個型號 | CONFIRMED | S “a highly capable, lower-cost alternative to Astra” |
| 113 | 四 p1 | 內部事實性評測用使用者標記過錯誤的真實對話 | CONFIRMED | A |
| 114 | 四 p1 | Sol 錯誤約前代一半 | CONFIRMED | A |
| 115 | 四 p1 | 接近 Astra 等級、成本低得多 | CONFIRMED | A |
| 116 | 四 p1 | 不代表一般使用 | CONFIRMED | A |
| 117 | 四 p1 | 一般使用錯誤更少見 | CONFIRMED | A |
| 118 | 四 p2 | Luna 事實性大幅進步 | CONFIRMED | A |
| 119 | 四 p2 | 較高推理設定下與 GPT-5.6 Sol 相當 | CONFIRMED | A |
| 120 | 四 p2 | 成本約百分之一 | CONFIRMED | A |
| 121 | 四 p3 | 安全資訊在 Astra System Card 附錄第 11 節 | CONFIRMED | S |
| 122 | 四 p3 | 2026-09-22 加入 | CONFIRMED | S 變更紀錄 |
| 123 | 四 p3 | 不是另一份獨立的 system card | CONFIRMED | A 的 system card 連結指向 gpt-6-astra；DSH 首頁今天最新仍是 Sep 08 |
| 124 | 四 p3 | 資安、生物化學 High capability | CONFIRMED | S |
| 125 | 四 p3 | 公司內部分級、不是外部評等 | CONFIRMED | S “our Preparedness Framework” |
| 126 | 四 p3 | 未達 AI 自我改進 High 門檻 | CONFIRMED | S |
| 127 | 四 p3 | 與 GPT-5.6 Sol／Luna 相同 | CONFIRMED | S §11.8 |
| 128 | 四 p3 | 沿用同一套防護措施 | CONFIRMED | S |
| 129 | 四 p4 | Professional 與 Consensus 持平或進步 | **CHANGED**：補「經長度調整的分數」 | S “maintain or improve **length-adjusted** performance”；Table 29 |
| 130 | 四 p4 | HealthBench 與 Hard 退步 | CONFIRMED | S |
| 131 | 四 p4 | 回答明顯變短 | CONFIRMED | S “substantially shorter final answers” |
| 132 | 四 p4 | Sol 約減少 45% | CONFIRMED | S |
| 133 | 四 p4 | Luna 約減少 35% | CONFIRMED | S |
| 134 | 五 p1 | 看模型選單；逐步推出、稍後再試 | CONFIRMED | A；C “Choose a model in the picker when available.” |
| 135 | 五 p2 | API 名稱 gpt-6-sol、gpt-6-luna | CONFIRMED | A |
| 136 | 五 p2 | CLI 用 /model | CONFIRMED | C |
| 137 | 五 p2 | codex --model gpt-6-sol／gpt-6-luna | CONFIRMED | C |
| 138 | 五 p2 | 計費以當天價目表為準 | OUT OF SCOPE | 建議語 |
| 139 | 五 p3 | Enterprise 先請管理員啟用 | CONFIRMED | C |
| 140 | 五 p3 | 「公告與 changelog 都只點名」Enterprise 管理員 | **CHANGED** → 「changelog 只點名」 | A 全文 admin 0 次 |
| 141 | 五 p3 | 沒寫 Business、Edu | CONFIRMED | C |
| 142 | 五 p3 | 「GPT-5.6 Sol 與 Luna 目前沒有下架的訊息」 | **CHANGED** → 「四條官方來源都沒有寫 GPT-5.6 Sol 與 Luna 要下架」 | A、C（只有 GPT-5.5 退役條目）、P、S |
| 143 | 五 p4 | 沒提台灣或地區的開放時程 | CONFIRMED | A |
| 144 | 五 p4 | 沒寫訂閱月費調整 | CONFIRMED | A、C（subscription 0 次；month 只在 “Earlier this month” 與 “past several months”） |
| 145 | 五 p4 | API 降價與月費是兩件事 | OUT OF SCOPE | 說明 |
| 146 | FAQ 1 | Free 與 Go 桌面 App 用 Luna | CONFIRMED | A |
| 147 | FAQ 1 | 沒寫 Sol 是否開放給免費或 Go | CONFIRMED | A、C |
| 148 | FAQ 1 | 沒寫 Windows 或 macOS | CONFIRMED | A、C |
| 149 | FAQ 1 | 沒寫 Work 還是 Codex | CONFIRMED | A、C |
| 150 | FAQ 1 | 沒寫網頁或手機版 | CONFIRMED | A、C |
| 151 | FAQ 2 | 還沒有 | CONFIRMED | A |
| 152 | FAQ 2 | 公告與 changelog 都這樣寫 | CONFIRMED | A、C |
| 153 | FAQ 2 | 兩邊都沒給時程 | CONFIRMED | A、C |
| 154 | FAQ 3 | 跟各自的 GPT-5.6 促銷價比 | CONFIRMED | A |
| 155 | FAQ 3 | 不是原價 | CONFIRMED | A |
| 156 | FAQ 3 | 「這個促銷價」至少到 11/21 | **CHANGED** → 「GPT-5.6 Sol 的促銷價」 | P |
| 157 | FAQ 3 | 新舊兩代價格同時存在 | CONFIRMED | P（同 #69） |
| 158 | FAQ 4 | 都是 OpenAI 自選評測 | CONFIRMED | A |
| 159 | FAQ 4 | 對手分數取自公開報告 | CONFIRMED | A |
| 160 | FAQ 4 | Fable 5.1 缺分數時用 Fable 5 | CONFIRMED | A “Scores for Claude Fable 5 were reported when scores for Claude Fable 5.1 were unavailable.” |
| 161 | FAQ 4 | Fable 5.1 成本被低估 | CONFIRMED | A |
| 162 | FAQ 5 | 官方未說明 | CONFIRMED | A、C、P、S |
| 163 | FAQ 5 | 公告、changelog、價目表沒提地區限制 | CONFIRMED | A、C、P |
| 164 | FAQ 6 | 「可以。」 | **NOT FOUND → 刪除** | P 只撐得住 GPT-5.6 Sol 在 API 的促銷價期限；Luna 與 ChatGPT 端四條來源都沒寫 |
| 165 | FAQ 6 | GPT-5.6 Sol 促銷價至少到 11/21 | CONFIRMED | P |
| 166 | FAQ 6 | 四條來源沒寫 GPT-5.6 下架或停用 | CONFIRMED | A、C、P、S |
| 167 | callout | 比較都是 OpenAI 自選、分數取自公開報告 | CONFIRMED | A |
| 168 | callout | 本站沒有實測 | OUT OF SCOPE | 編輯聲明 |
| 169 | callout | 50% 比的是 GPT-5.6 促銷價、不是原價 | CONFIRMED | A |
| 170 | callout | 逐步推出 | CONFIRMED | A |
| 171 | callout | Enterprise 要管理員先啟用 | CONFIRMED | C |
| 172 | callout | 沒提台灣或地區時程 | CONFIRMED | A |
| 173 | 連結 1 | 文字＝索引 zh-TW 標題、目標五語 | CONFIRMED | `ai-news-2026-january-september-index.json`（en、ja、ko、zh-CN、zh-TW） |
| 174 | 連結 2 | 文字＝Astra 篇 zh-TW 標題、目標五語 | CONFIRMED | `ai-news-gpt-6-astra-20260903.json`（五語），DELTA-4-8 第 5 條 |
| 175 | source 1 | 標題 | CONFIRMED | A |
| 176 | source 2 | changelog 2026-09-22 條目標題 | CONFIRMED | C “2026-09-22 GPT-6 Sol and Luna in Codex and ChatGPT Work” |
| 177 | source 3 | 標題 | CONFIRMED | P |
| 178 | source 4 | 第 11 節附錄、2026-09-22 加入 | CONFIRMED | S |
| 179 | sources | checked_on 全部 2026-09-26、與紀錄一致 | CONFIRMED | 撰稿與研究代理今天讀到，不因重查而改 |
| 180 | 全文 | 沒有提到 Claude Opus 5.5 | CONFIRMED | pack 內「5.5」0 次（DELTA-4-8 第 4 條） |

## 改掉的地方（原文 → 改成，依據）

1. summary 2：「價目表寫這個促銷價至少維持到 2026 年 11 月 21 日」→「價目表寫 GPT-5.6 Sol 的促銷價至少維持到 2026 年 11 月 21 日」。https://developers.openai.com/api/docs/pricing 原文 “GPT-5.6 Sol’s promotional pricing is available at least through November 21, 2026.”；全頁（含頁面資料）promotional 只有這一句。
2. FAQ 3：「OpenAI 的價目表寫這個促銷價至少維持到」→「OpenAI 的價目表寫 GPT-5.6 Sol 的促銷價至少維持到」。同上。
3. 第二節 p4：「這次公告拿來比較的促銷價現在仍然有效、不是舊價，兩個世代的價格現在同時存在。」→「也就是 Sol 這邊拿來比較的促銷價現在仍然有效、不是舊價，兩個世代的價格現在同時存在；GPT-5.6 Luna 的促銷價，價目表沒有寫維持到哪一天。」同上。
4. FAQ 6：刪「可以。」。同上；Luna 與 ChatGPT 端沒有來源。
5. 第二節 p3：「價目表也顯示，快取讀取的輸入 token 有 90% 折扣；寫入快取的價格比一般輸入高」→「公告寫快取讀取的輸入 token 有 90% 折扣；價目表另列寫入快取的價格，比一般輸入高」。https://openai.com/index/introducing-gpt-6-sol-and-luna/ “discounts of 90% on cached input-token reads”；價目表全頁「90%」0 次。
6. 第二節 p2：「公告的價格表把 Sol、Luna 的輸入與輸出都標示為「50% cheaper」」→「公告的價格表在 Sol、Luna 兩列的降價欄都標示「50% cheaper」」。公告表頭 Model／Input／Output／Price reduction，每列一格。
7. 第五節 p3：「公告與 changelog 都只點名 Enterprise 管理員」→「changelog 只點名 Enterprise 管理員」。公告全文 admin 0 次；https://learn.chatgpt.com/docs/changelog “Enterprise administrators must enable the new models.”
8. 第一節 p3：補限定詞「能不能用也取決於工作區設定：」。changelog “Availability depends on rollout and workspace settings”。
9. 第四節 p4：「HealthBench Professional 與 Consensus 上持平或進步」→「…上經長度調整的分數持平或進步」。https://deploymentsafety.openai.com/gpt-6-astra §11.4.1 “maintain or improve length-adjusted performance”；Table 29 未調整分數 GPT-6 Sol Professional 59.5 對 GPT-5.6 Sol 64.1。
10. 第 1 段：「GPT-6 Astra 仍是目前最好的模型」→「GPT-6 Astra 仍是 OpenAI 目前最好的模型」。公告 “our best model across the board”。
11. 第三節 p3：「Sol 與 Luna 只是比前代更划算」→「Sol 與 Luna 則是比前代更划算」。公告沒有 only。
12. 第一節 p4：「四條官方來源都沒有提到台灣」→「四條官方來源談 Sol 與 Luna 的開放範圍時都沒有提到台灣」。公告頁尾 Keep reading 卡片印著〈ChatGPT Ads expands to Southeast Asia and Taiwan〉。
13. 第五節 p3：「GPT-5.6 Sol 與 Luna 目前沒有下架的訊息。」→「四條官方來源都沒有寫 GPT-5.6 Sol 與 Luna 要下架。」否定句限縮到 sources[]（changelog 的退役條目只有 GPT-5.5，且註明不適用 API）。
14. 表格 caption：「OpenAI API 價目表與 9 月 22 日公告整理」→「OpenAI API 價目表與美國時間 9 月 22 日公告整理」。RSS pubDate 18:00Z；DELTA-4-8 第 4 條。

非事實的格式修正：description 句尾「（2026 年 9 月查核）」→「（2026 年 9 月查證）」（DELTA-4-7 第 14 條；repo 裡以這個句尾結束的 description 有 4 篇用「查證」、0 篇用「查核」）；兩段英文引文的 U+2011 改成 ASCII「-」（DELTA-4-7 第 11 條）。

研究紀錄同步修正（不然第二輪會把文章改回去）：verified_facts 的 11/21 那條加註「只講 GPT-5.6 Sol」；HealthBench 那條 fact 與對應的 must_not_write 補「經長度調整」；not_said 的台灣條限縮並註明 Keep reading 卡片；not_said 的 Luna 降幅條把「兩欄都標」改成「那一列的降價欄」。另加 `factcheck`（claims_checked 180、17 筆 changes、3 個 open_questions、2 條 coordinator_rulings）。`title` 沒改。

## 讀者優先檢查

- 「本文」0 次；「本站」出現在 FAQ 4 與 callout，可以。
- 開頭段只有一個歸因語（「官方表示」）；正文每段最多兩個，這次補的句子沒有讓任何一段超過兩個。
- description 只剩「（2026 年 9 月查證）」一個查證尾巴；title、description、summary 沒有選題計數。
- 未改、留給協調者：第二節 p2「照表印的數字寫，不自己計算或推論百分比，也不是說 OpenAI 標錯」是查證紀律寫進正文；第 2 段「資料來自…；評測數字都是 OpenAI 自己公布…也不是採購或投資建議」偏流程說明。兩者都不是事實錯誤。

## 待決（給協調者）

1. **「付費方案」標籤**：description、summary 1、第一節 p1、diagram 第一格（與 hero alt）把 Plus、Pro、Business、Enterprise、Edu 叫「付費方案」，並與「免費與 Go」對照，讀起來像 Go 不是付費方案。chatgpt.com/pricing（今天 200，不在 sources[]）把 Go 列成「/ month」的方案。分組照 OpenAI 原文是對的，只有標籤不精確；建議改成「Plus、Pro、Business、Enterprise、Edu 方案」或「Plus 等五個方案」。第一輪沒改，因為 description 已 191 字、改動牽涉圖檔。
2. **GPT-5.6 Luna 在價目表**：All models 表（頁面資料，點開才顯示）列了 gpt-5.6-luna 0.2／0.02／0.25／1.2 美元，撐得住「兩代價格同時存在」；但它不是靜態 HTML 的可見文字，沒有寫成 verified_facts。第二輪若要更嚴，可把 #69、#157 改成只講 Sol。
3. 發布當天重讀：價目表的促銷價註記與各欄價格、公告 Availability 段、changelog 9/22 條目、System Card 變更紀錄（live_data_warnings 已列）。
