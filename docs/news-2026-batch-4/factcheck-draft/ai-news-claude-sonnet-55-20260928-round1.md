# 查核報告（第一輪）：ai-news-claude-sonnet-55-20260928

- 查核者：獨立查核代理（第一輪，opus），2026-09-30（台北）
- 規格：`agents/ai/FACTCHECK.md`（Windows 路徑與「允許留下的 FAIL」不適用）、`DELTA-4-10.md`（全）、`DELTA-4-9.md`、`DELTA-4-7.md` 第 11–14 條、`BRIEF.md` 最後一節錯誤型態、HANDOVER §3
- 改動的檔案：內容包 `apps/api/app/guides/content/ai-news-claude-sonnet-55-20260928.json`、研究紀錄 `docs/ai-news-2026-09-late/research/ai-news-claude-sonnet-55-20260928.json`（`title` 與 `diagram.nodes` 第三格同步，另加 `factcheck`）
- 暫存與原始回應：`/root/news49/s55/agents/fc1/`（`src1.bin`–`src4.bin`、正規化 `norm.py`、PDF 抽字 `sc.txt`／`sc.norm.txt`、改稿腳本 `edit_pack.py`／`edit_research.py`、`check0.log`（改前）、`check.log`（改後））

## 摘要

- 主張約 110 條：CONFIRMED 88、CHANGED 18、刪除 4（編輯清點、推論句、帶暗示的否定句、未解釋的 partial 標記）。
- **內容包改了 21 處**（事實或範圍 13 處、讀者優先與措辭 8 處），表格重做。研究紀錄改 2 處（title、diagram 節點）並加上 `factcheck`。
- 最重的五處：
  1. **標題「三家雲端」是編輯清點**：公告寫 `all platforms, including Amazon Web Services, Google Cloud, and Microsoft Azure`（including 不是全清單），模型頁列五個平台，沒有任何一頁印「三家」。標題改成「API、雲端平台與 Claude.ai 都能用」；圖解第三格「API 與三家雲端」是同一個清點，也改成「API 與雲端平台」（圖由 `build_assets.py` 從研究紀錄 `diagram.nodes` 繪製）。
  2. **「第一個是 9 月 22 日的 Opus 5.5」沒有來源**：四條 `sources[]` 查 `September 22`／`Sep 22` 都是 0 次，公告只寫 `the second model in the Claude 5.5 family`。改成「同家族還有 Opus 5.5」。
  3. **表格的 Opus 5.5 欄**（DELTA-4-10 第 3 條）：刪掉。表格改成三欄「項目（每百萬 tokens）｜Sonnet 5.5 牌價｜列在哪裡」、六列，把原本在正文的模型頁明細（5 分鐘與 1 小時快取寫入、Batch 五折）移進表格；caption 改寫，保留查核日。正文刪掉「下表的 Opus 5.5 欄是公告同一張價格表印的」。
  4. **「快取寫入與 Batch 是否相同，這幾頁沒有寫」**：這句暗示價格可能不同，刪掉；只留公告原文撐得住的「公告明寫與 Sonnet 5 相同的是輸入、輸出與快取讀取三項」。
  5. **推論句「Sonnet 5 目前也還會用到」**：刪掉，改成歸因句「公告另寫，較高風險的資安任務會退回 Sonnet 5 處理（見最後一節）」，對應原文 `higher-risk cybersecurity tasks will visibly fall back to Sonnet 5`。
- 限定詞補回四處：產品頁 30% 的 `estimated … for typical workloads billed by token`、FrontierCode 註腳的 `in two cases Cognition examined`、GDPval 註腳的 `could degrade`、提示注入的 `particularly in coding environments and browser use`。
- 自檢：`OK ai-news-claude-sonnet-55-20260928 zh-TW paragraphs 2857`（exit 0，零 FAIL；改前 2877）。
- 結論：`needs_second_round`（事實改動超過十處；DELTA-4-10 第 6 條本來就要求第二輪）。

## 重抓結果（2026-09-30，UTC）

UA：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL --compressed --max-time 90`，同一主機間隔 1.2 秒，請求沒有任何人的姓名、email 或個資。

| 時間 | 網址 | HTTP | 落地 bytes | 正文？ |
| --- | --- | --- | --- | --- |
| 11:44Z | https://www.anthropic.com/claude-sonnet-5-5 | 200，0 次轉址 | 430,222（與研究代理的落地檔逐位元組相同） | 是：日期、導言、五點改進、評測表與四個註腳、成本對分數圖說、價格表、Safety、Getting started |
| 11:45Z | https://platform.claude.com/docs/en/models/sonnet-5-5/overview | 200，0 | 429,111（研究代理 429,120；差在 nonce 與 chunk 名，可見文字逐字相同） | 是：規格卡、五項破壞性變更、比較表、Model IDs、Pricing、Capabilities、Availability |
| 11:45Z | https://www.anthropic.com/claude-sonnet-5-5-system-card | 200，2 次轉址 → `www-cdn.anthropic.com/870c8f52…/Claude%20Sonnet%205.5%20System%20Card.pdf` | 13,101,289（相同） | 是：148 頁（pypdf 計數，讀到的值），封面 `September 28, 2026`，摘要、§1.5 Safeguards、§2 RSP evaluations、§3.3 |
| 11:45Z | https://www.anthropic.com/claude/sonnet | 200，0 | 405,412（相同） | 是：Announcements、Availability and pricing。頁首仍是「Claude Sonnet 4.6 Hybrid reasoning model…」，FAQ 仍停在 Sonnet 5（活頁面部分落後） |

沒有 403、逾時或軟性 404。

`verbatim_quote` 逐字比對：HTML 刪註解與 script／style／noscript／svg／template 後，做 A（行內標籤→無、其他→空格）、B（全部→空格）、C（全部→無）三種正規化加解碼後 RAW；PDF 用空白收斂版。**44/44 通過**，所有 `url` 都在 `sources[]`。另外以詞首查 System Card 的 `ASL`：今天的抽字只命中 `ASLR` 1 次（研究紀錄記 2 次，是抽字差異），沒有 `ASL-n` 分級字樣。

## 主張逐條

來源代號：A＝公告頁、M＝模型頁、S＝System Card、P＝Sonnet 產品頁。

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | Sonnet 5.5 推出 | CONFIRMED | A 標題與日期 |
| 2 | title | 牌價與 Sonnet 5 相同 | CONFIRMED | A `priced the same as Sonnet 5 at $2 … $10 … $0.20` |
| 3 | title | 「API、三家雲端與 Claude.ai 都能用」 | **CHANGED** →「API、雲端平台與 Claude.ai」 | A 用 including 舉三例；M 列五平台；沒有頁面印「三家」（HANDOVER §3） |
| 4 | description | 2026-09-28 推出 | CONFIRMED | A、M `Released September 28, 2026`、S 封面、P `Sep 28, 2026` |
| 5 | description | 牌價同 Sonnet 5，輸入 2、輸出 10 | CONFIRMED | A |
| 6 | description | Claude.ai、API 與多個雲端平台可用 | CONFIRMED | P `Anyone can chat…`；M Platforms |
| 7 | description | 較高風險的資安請求退回 Sonnet 5 | CONFIRMED | A Safeguards；S §3.3 `falls back to Claude Sonnet 5 for requests that are blocked by our cyber classifier system` |
| 8 | 第 1 段 | Claude 5.5 家族第二個模型 | CONFIRMED | A 導言 |
| 9 | 第 1 段 | 「第一個是 9 月 22 日的 Opus 5.5」 | **CHANGED** →「同家族還有 Opus 5.5」 | 四條來源 `September 22`／`Sep 22` 皆 0 次 |
| 10 | 第 1 段 | 牌價 2／10，與 Sonnet 5 相同 | CONFIRMED | A |
| 11 | 第 1 段 | 「每個任務最多便宜 30%」是測試量到的每任務成本，不是牌價調降 | **CHANGED**（措辭）→ 每個任務的成本比前一代「最多少 30%」，是 Anthropic 在自己測試裡量到的結果 | A `In our testing, it costs up to 30% less per task than its predecessor.` |
| 12 | 第 2 段 | 2026-09-30 查核、依據四頁 | CONFIRMED（「讀的是」→「依據」） | `sources[]` 四條 `checked_on` 一致 |
| 13 | 第 2 段 | 任何人都能在 Claude.ai 使用 | CONFIRMED | P |
| 14 | 第 2 段 | 開發者用 claude-sonnet-5-5 | CONFIRMED | A、M、P |
| 15 | 第 2 段 | 這幾頁沒有提到台灣，也沒有列地區限制 | **CHANGED** →「也沒有列出開放或限制的地區」 | 詞界查 Taiwan：A、M、P、S 皆 0；原句可被讀成台灣可用 |
| 16 | 第 2 段 | 評測與安全分級是 Anthropic 自己公布，沒有實測 | CONFIRMED | 編輯聲明 |
| 17 | 第 2 段 | 「也不建議換模型或訂閱」 | **CHANGED** →「也不提供換模型或訂閱的建議」 | 原句可讀成勸讀者不要換，是反向的建議 |
| 18 | summary 1 | 9/28、第二個、API 名稱 | CONFIRMED | A、M |
| 19 | summary 1 | 這幾頁沒有寫 Sonnet 5 何時停用 | CONFIRMED | A、P 的 retire／deprecat／replac 皆 0；M 的 2 次 retire 是 Sonnet 5.5 自己的 Retirement 與導覽列；S 的 deprecat 3 次在模型福祉章節 |
| 20 | summary 2 | 輸入 2、輸出 10、快取讀取 0.20 同 Sonnet 5 | CONFIRMED | A |
| 21 | summary 2 | 通常需要少得多的 tokens，是 Anthropic 的說法 | CONFIRMED | A `typically needs far fewer tokens to do the same work` |
| 22 | summary 3 | 網頁、iOS、Android；方案未逐一列出 | CONFIRMED | P |
| 23 | summary 3 | 模型頁五平台 | CONFIRMED | M Platforms |
| 24 | summary 4 | Terminal-Bench 70.6%／10.3%，不代表讀者任務 | CONFIRMED | A 評測表與導言 |
| 25 | summary 4 | Opus 5.5 在複雜開放式工作仍明顯較強 | CONFIRMED | A `Opus 5.5 remains clearly stronger at complex, open-ended work requiring sustained judgment` |
| 26 | summary 5 | 沒有跨過新的 RSP 門檻，Anthropic 自己的判定 | CONFIRMED | S 摘要 |
| 27 | summary 5 | 較高風險的資安請求退回 Sonnet 5 | **CHANGED**（加歸因）→「公告說較高風險的資安任務會退回」 | A |
| 28 | 第 1 節第 1 段 | 較快、成本較低的搭配；Opus 5.5 給需要審慎判斷的複雜工作 | CONFIRMED | A |
| 29 | 同上 | 範圍明確的日常任務、修 bug、文件／簡報／試算表 | CONFIRMED | A |
| 30 | 同上 | 「明確升級」、輸出快 30% 以上，Anthropic 自述 | CONFIRMED | A `clear upgrade`、`generates outputs 30%+ faster` |
| 31 | 第 1 節第 2 段 | 三頁沒有寫 Sonnet 5 何時停用 | CONFIRMED | 同 #19 |
| 32 | 同上 | Sonnet 5.5 退役日不早於 2027-09-28，是承諾 | CONFIRMED | M `Retirement Not sooner than September 28, 2027`；M 的 Model deprecations 連結說明是 `retirement commitments` |
| 33 | 同上 | 「Sonnet 5 目前也還會用到」 | **刪除**，改為歸因句 | 推論句；原文只說 `will visibly fall back to Sonnet 5` |
| 34 | 第 1 節第 3 段 | 五項破壞性變更影響原本在 Sonnet 5 跑的程式 | CONFIRMED | M `Five breaking changes affect code already running on Claude Sonnet 5` |
| 35 | 同上 | 關思考的要改用 between_tools | CONFIRMED | A Getting started；M 第一項 |
| 36 | 第 2 節第 1 段 | 模型頁牌價明細 | 移入表格 | M Pricing |
| 37 | 同上 | 公告明寫相同的是三項 | CONFIRMED | A |
| 38 | 同上 | 「快取寫入與 Batch 是否相同，這幾頁沒有寫」 | **刪除** | 句子本身屬實（A、M、P、S 都沒寫），但會讓讀者以為可能不同；協調者點名第 4 項 |
| 39 | 第 2 節第 2 段 | 公告：測試中每任務最多少 30% | CONFIRMED | A |
| 40 | 同上 | 產品頁是「一般工作負載的估計」 | **CHANGED** → 補「對以 token 計費的一般工作負載，估計執行成本比 Sonnet 5 最多少 30%」 | P `up to an estimated 30% less to run than Sonnet 5 for typical workloads billed by token` |
| 41 | 同上 | 兩處都是「最多」，牌價沒有降 | CONFIRMED | A、P |
| 42 | 同上 | 「實際省多少，看自己的任務」 | **CHANGED** →「實際成本要看」 | 原句預設一定會省 |
| 43 | 第 2 節第 3 段 | 快取最多省 90%、批次省 50% | CONFIRMED | P |
| 44 | 同上 | US-only inference 輸入與輸出 1.1 倍 | **CHANGED**（補條件）→ 需要在美國境內執行的工作負載可選 | P `For workloads that need to run in the US, …` |
| 45 | 同上 | 「下表的 Opus 5.5 欄是公告同一張價格表印的」 | **刪除** | 表格已刪 Opus 5.5 欄 |
| 46–51 | 表格 | 輸入 $2、輸出 $10、快取讀取 $0.20（A、M）；5 分鐘快取寫入 $2.50（M；A 價格表寫 `Cache writes $2.50`）；1 小時快取寫入 $4（M）；Batch API 輸入與輸出五折（M） | **CHANGED**（重做表格；每格已回原文核對） | A 價格表、M Pricing |
| 52 | 表格 caption | 原「Anthropic 公告價格表…Sonnet 5 的輸入、輸出、快取讀取與 Sonnet 5.5 相同」 | **CHANGED** → 標明依公告價格表與模型頁、公告寫明相同的三項 | A、M |
| 53 | 第 3 節第 1 段 | 任何人都能在 Claude.ai 用，網頁、iOS、Android | CONFIRMED | P |
| 54 | 同上 | 沒有逐一列出方案、用量上限、是否為預設模型；官方未說明、不能推論成某方案不能用 | CONFIRMED | P、A；照 DELTA-4-10 第 3 條 |
| 55 | 第 3 節第 2 段 | 公告「所有平台」，舉例 AWS、Google Cloud、Microsoft Azure | CONFIRMED | A `now available on all platforms, including …`（Azure 照公告） |
| 56 | 同上 | 模型頁五平台（Microsoft Foundry） | CONFIRMED | M（Foundry 照模型頁；兩者沒有混用） |
| 57 | 同上 | Bedrock 的 ID 是 anthropic.claude-sonnet-5-5，其餘是 claude-sonnet-5-5 | CONFIRMED | M Model IDs |
| 58 | 第 3 節第 3 段 | 1M、128K、可靠知識截止 2026 年 6 月 | CONFIRMED | M |
| 59 | 同上 | 「這些頁面沒有寫 Sonnet 5 的規格，所以不比較」 | **CHANGED** →「這些頁面沒有 Sonnet 5 的規格可對照」 | 「所以不比較」是撰稿流程；M 比較表沒有 Sonnet 5 |
| 60 | 同上 | Claude Code 與 Claude 應用預設 Medium、Claude Platform 預設 High | CONFIRMED | A |
| 61 | 圖解 caption | 四項主題、依四頁整理、查核日 | CONFIRMED | 與研究紀錄 `diagram.caption` 相同 |
| 62 | 圖解第 1 格 | 牌價不變，與 Sonnet 5 相同 | CONFIRMED | A |
| 63 | 圖解第 2 格 | 網頁、iOS、Android | CONFIRMED | P |
| 64 | 圖解第 3 格 | 「API 與三家雲端」 | **CHANGED** →「API 與雲端平台」 | 同 #3 |
| 65 | 圖解第 4 格 | 未跨新 RSP 門檻 | CONFIRMED | S |
| 66 | hero_label | 同價新一版 Sonnet | CONFIRMED | A |
| 67 | 第 4 節第 1 段 | 公告評測表、Anthropic 公布、不代表讀者任務 | CONFIRMED | A |
| 68 | 同上 | Terminal-Bench 4.0（代理式寫程式）70.6／10.3／66.4，註腳 Opus 取 Xhigh 最高分 | CONFIRMED | A 表與註 1 |
| 69 | 同上 | CursorBench 4.0 55.5／34.1／57.8 | CONFIRMED | A |
| 70 | 同上 | OSWorld 2.1 80.1／57.0／81.8 | CONFIRMED | A |
| 71 | 同上 | 「表上三格都帶 partial 標記」 | **刪除** | A 沒有解釋 partial；協調者點名第 5 項 |
| 72 | 第 4 節第 2 段 | FrontierCode Max 46.2、Xhigh 52.1、Sonnet 5 42.4、Opus 5.5 54.4 | CONFIRMED | A |
| 73 | 同上 | 註腳：Max 較常跑程式審查技能，「有兩個任務逾時或改到範圍外」 | **CHANGED** →「在 Cognition 檢視的兩個案例裡導致逾時或改到任務範圍外」 | A 註 2 `in two cases Cognition examined` |
| 74 | 同上 | GDPval-AA 是分數制：1844／1449／1846 | CONFIRMED | A |
| 75 | 同上 | 註腳：Artificial Analysis 在上市前部署上跑，「有影響結構化輸出的 bug」 | **CHANGED** →「有一個可能影響結構化輸出回應的 bug，現已修正」 | A 註 3 `a bug that could degrade responses to requests that use structured outputs … That bug has since been fixed.` |
| 76 | 第 4 節第 3 段 | Anthropic 的但書 | CONFIRMED | A |
| 77 | 第 4 節全節 | 沒有 GPT／OpenAI 比較 | CONFIRMED | 內容包 grep GPT、OpenAI 皆 0 |
| 78 | 第 5 節第 1 段 | RSP 評估：整體能力低於 Opus 5.5，沒有跨過任何新的 RSP 門檻 | CONFIRMED | S 摘要 `broadly less capable than Opus 5.5 across domains and does not cross any new RSP thresholds` |
| 79 | 同上 | Opus 5.5 未跨 CB-2 與 Autonomy-2 的判定同樣適用 | CONFIRMED | S §2.1 |
| 80 | 同上 | 當作已達 CB-1 與 Autonomy-1，套用 RSP 對應緩解 | CONFIRMED | S §2.1 `We do treat Sonnet 5.5 as meeting our CB-1 and Autonomy-1 thresholds and apply the corresponding mitigations from our RSP.` |
| 81 | 同上 | 沒有寫成 ASL | CONFIRMED | 內容包與 S 都沒有 ASL-n |
| 82 | 第 5 節第 2 段 | 失準風險低 | CONFIRMED | S 摘要 |
| 83 | 同上 | 對提示注入最穩健的 Sonnet 級模型 | **CHANGED**（補限定）→（特別是寫程式與瀏覽器使用） | S 摘要 `particularly in coding environments and browser use` |
| 84 | 同上 | 電腦操作環境的有害任務拒絕率與 Opus 5.5 相當、比部分較早模型退步 | CONFIRMED | S 摘要 |
| 85 | 第 5 節第 3 段 | 資安能力比 Sonnet 5 大幅提升，比照 Opus 5.5 部署類似防護 | CONFIRMED | A `a large improvement over Sonnet 5’s, so we’re deploying it with safeguards similar to those on Opus 5.5` |
| 86 | 同上 | 第一個帶資安防護與備援上線的 Sonnet | CONFIRMED | A |
| 87 | 同上 | 一般找 bug、修 bug 不受影響；高風險資安任務看得到地退回 Sonnet 5 | CONFIRMED | A |
| 88 | 同上 | 退回適用第一方產品與 API 選擇啟用的開發者，「其他平台可能不同」 | **CHANGED** →「透過其他平台與供應商使用時可能不同」 | S §1.5 `via other platforms and providers may experience different behavior` |
| 89 | 同上 | 沒有攻擊細節 | CONFIRMED | 全文沒有漏洞、利用手法或 CVE |
| 90 | FAQ 1 | 牌價相同的三項 | CONFIRMED | A |
| 91 | FAQ 1 | 「最多便宜 30%」是「測試或估計的每任務成本」 | **CHANGED** →「測試的每任務成本或對一般工作負載的估計」 | A 是每任務；P 是 typical workloads，不是每任務 |
| 92 | FAQ 2 | 任何人、網頁／iOS／Android；方案與上限官方未說明 | CONFIRMED | P |
| 93 | FAQ 2 | 登入後看能選哪些模型 | CONFIRMED（操作提示，不是購買建議） | — |
| 94 | FAQ 3 | 截至 9/30 三頁沒寫 Sonnet 5 何時停用；Sonnet 5.5 不早於 2027-09-28 | CONFIRMED | 同 #19、#32 |
| 95 | FAQ 4 | 比照 Opus 5.5 的類似防護、高風險退回、一般修 bug 不受影響 | CONFIRMED | A |
| 96 | FAQ 4 | 退回的適用範圍 | **CHANGED**（同 #88） | S §1.5 |
| 97 | FAQ 5 | RSP 是 Anthropic 自己的框架；CB-1／Autonomy-1、未跨 CB-2／Autonomy-2；不是外部評等 | CONFIRMED | S |
| 98 | FAQ 6 | Haiku 5.5「未來幾週」加入，沒有日期 | CONFIRMED | A `will join the Claude 5.5 family in the coming weeks` |
| 99 | FAQ 6 | 四頁都沒有 Haiku 5.5 的上市資訊 | CONFIRMED | `Haiku 5.5`：A 1 次（就是這句）、M／P／S 0 次 |
| 100 | callout | 截至 9/30、頁面可能更新；沒有實測、不是換模型或訂閱的建議 | CONFIRMED | 編輯聲明 |
| 101–110 | sources／checked_on／結尾連結／related | 四條 `checked_on` 2026-09-30 一致；兩個結尾連結與 `related` 照 DELTA-4-10 第 4 條 | CONFIRMED | 自檢通過；沒有改動 |

## 改掉的地方（原文 → 改成，依據）

1. **title**：「…API、三家雲端與 Claude.ai 都能用」→「…API、雲端平台與 Claude.ai 都能用」。「三家」是編輯清點（HANDOVER §3）。研究紀錄 `title` 同步。
2. **第 1 段**：「第一個是 9 月 22 日的 Opus 5.5」→「同家族還有 Opus 5.5」。`sources[]` 沒有這個日期。
3. **第 1 段**：「公告的『每個任務最多便宜 30%』，是 Anthropic 在自己測試裡量到的每任務成本」→「公告說每個任務的成本比前一代『最多少 30%』，那是 Anthropic 在自己測試裡量到的結果」。改成貼近原文 `up to 30% less per task than its predecessor` 的說法，保留「最多」。
4. **第 2 段**：「沒有列地區限制」→「沒有列出開放或限制的地區」；「也不建議換模型或訂閱」→「也不提供換模型或訂閱的建議」；「讀的是」→「依據」。
5. **summary 第 5 點**：加上「公告說」，「請求」改成原文的「任務」。
6. **第 1 節第 2 段**：刪「Sonnet 5 目前也還會用到：較高風險的資安請求會退回它處理（第 5 節）」，改為「公告另寫，較高風險的資安任務會退回 Sonnet 5 處理（見最後一節）」。
7. **第 2 節第 1 段**：牌價明細移進表格；刪「快取寫入與 Batch 是否相同，這幾頁沒有寫」。
8. **第 2 節第 2 段**：產品頁 30% 補上「對以 token 計費的一般工作負載，估計執行成本比 Sonnet 5 最多少 30%」；「實際省多少」→「實際成本要看」。
9. **第 2 節第 3 段**：US-only inference 補上「需要在美國境內執行的工作負載」；刪 Opus 5.5 欄那句。
10. **表格**：刪 Opus 5.5 欄；改成三欄六列（見上表 #46–51）。
11. **表格 caption**：→「Claude Sonnet 5.5 牌價，美元／每百萬 tokens，依 Anthropic 公告價格表與模型頁，查核日 2026 年 9 月 30 日；公告寫明與 Sonnet 5 相同的是輸入、輸出、快取讀取三項。」
12. **第 3 節第 3 段**：「所以不比較」→「沒有 Sonnet 5 的規格可對照」。
13. **第 4 節第 1 段**：刪「表上三格都帶 partial 標記」。
14. **第 4 節第 2 段**：FrontierCode 註腳補回 Cognition 檢視的兩個案例。
15. **第 4 節第 2 段**：GDPval 註腳「有影響」→「可能影響」，補「現已修正」。
16. **第 5 節第 2 段**：提示注入補「特別是寫程式與瀏覽器使用」。
17. **第 5 節第 3 段**：「其他平台可能不同」→「透過其他平台與供應商使用時可能不同」。
18. **FAQ 4**：同上。
19. **FAQ 1**：「測試或估計的每任務成本」→「測試的每任務成本或對一般工作負載的估計」。
20. **研究紀錄 `diagram.nodes[2]`**：「API 與三家雲端」→「API 與雲端平台」。
21. **研究紀錄**：加 `factcheck` 欄位。

## 協調者點名的九項

1. 「三家雲端」：title 與圖解第三格都改掉。正文、summary、FAQ、description 查過沒有「三家」或其他來源沒印的清點。description 的「多個雲端平台」不是數字，保留。
2. 表格 Opus 5.5 欄：刪掉；三欄六列；caption 已改。
3. 30%：每一處都有「最多」且歸因給 Anthropic（第 1 段、第 2 節第 2 段、FAQ 1）；「30% 以上」照 `30%+ faster`；summary、title、description 與圖上都沒有 30%。牌價相同的三項照原文。
4. 快取寫入與 Batch：那句刪掉，只留公告寫明的三項。
5. partial：刪掉。評測在第 4 節開頭就歸因並寫明不代表讀者任務，summary 4 也寫了；全文沒有 OpenAI 或 GPT。
6. Azure／Foundry：第 3 節第 2 段「公告…Microsoft Azure」「模型頁…Microsoft Foundry」各自對應各自的來源；summary 3 只寫模型頁的清單。沒有混用。
7. 安全分級：照 S 原文（沒有跨過新的 RSP 門檻；當作已達 CB-1／Autonomy-1；Opus 5.5 未跨 CB-2／Autonomy-2 的判定同樣適用）；沒有 ASL；資安退回照 A 與 S；沒有攻擊細節。
8. 「Sonnet 5 目前也還會用到」：刪掉，改成歸因句。
9. 沒有購買建議，沒有「該不該換」（第 2 段的反向建議句也改了），沒有推定台灣可用（地區那句改成中性說法）。

## 界線檢查

- 購買建議、推薦式比價：無。價格表只有 Sonnet 5.5 一欄，沒有跨模型或跨廠商比價。
- 廠商宣稱：速度、30%、token 用量、評測、失準風險、提示注入都已歸因給 Anthropic，並保留 up to／30%+／particularly 等限定詞。
- 狀態：Haiku 5.5 寫「未來幾週」、沒有日期；方案層級寫「官方未說明」。台灣沒有寫成可用，也沒有寫成不可用。
- 「本文」：0 次。免責 callout：沒有；只有一個 info callout。
- 與 GPT-6.1 Sol 那篇：沒有互相比較。

## 留給站主的事

1. 產品頁（P）是活頁面，頁首仍是 Sonnet 4.6 的介紹，FAQ 仍停在 Sonnet 5；文章只引用 Availability and pricing 一節。發布當天要重讀。
2. Sonnet 5 的退役承諾（deprecations 頁：`Not sooner than June 30, 2027`），以及「快取寫入、Batch 也同價」（What's new 頁、docs 定價頁），都不在 `sources[]`，所以文章不寫。要寫就需要換來源（上限 4 條）。
3. System Card 自己前後不一致，研究紀錄已記錄，這一輪也不裁定：摘要寫 `three-stage cyber safeguards … as they are to Opus 5.5`，§1.5 寫 `similar blocking classifiers to those on Opus 5`；生物防護則是公告寫「同 Sonnet 5」、S 寫「同 Opus 5」。文章不提生物防護，資安照公告寫。
4. 版本說明 RSS 9/28 那則沒有列 Amazon Bedrock，模型頁有列。發布當天重讀模型頁的 Platforms。
5. 圖解 SVG 還沒產生（`apps/web/public/guides/ai-news-claude-sonnet-55-20260928/` 不存在）。協調者跑 `--assets` 時，圖上會用改過的節點文字。

## 結論

`needs_second_round`：事實與範圍改了 13 處（超過十處），表格重做，而且 DELTA-4-10 第 6 條本來就要求第二輪。第二輪請逐句回原文，特別看這一輪新寫的句子：第 1 段 30% 那句、第 2 節第 1 段、新表格的第三欄與 caption、第 1 節第 2 段的歸因句，以及第 4 節兩個註腳的改寫。
