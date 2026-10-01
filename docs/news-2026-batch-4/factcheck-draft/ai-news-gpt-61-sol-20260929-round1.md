# 查核報告（第一輪）：ai-news-gpt-61-sol-20260929

- 查核者：獨立查核代理（第一輪，opus），2026-09-30（台北）
- 規格：`agents/ai/FACTCHECK.md`（Windows 路徑不適用）、`DELTA-4-9.md`（全）、`DELTA-4-7.md` 第 11–14 條、`BRIEF.md` 十二種錯誤型態、`ai.md`
- 改動的檔案：內容包 `apps/api/app/guides/content/ai-news-gpt-61-sol-20260929.json`、研究紀錄 `docs/ai-news-2026-09-late/research/ai-news-gpt-61-sol-20260929.json`（改兩處、加 `factcheck`）
- 暫存與原始回應：`/root/news49/agents/fc1/`（`s1.bin`–`s5.bin`、`fetch.log`、抽字 `ext.py`、逐字比對 `q.py`、`check.log`）

## 摘要

- 主張 131 條：CONFIRMED 112、CHANGED 12、刪除 3（查證流水帳或來源撐不住的否定句）、OUT OF SCOPE 4（編輯聲明）。
- **事實修改 10 處**，另有 6 處讀者優先的改寫（刪查證流水帳、限定詞補回原文用語）與 1 處開頭段補寫。研究紀錄改 2 處（「五分之一」算術）並加 `factcheck`。
- 最重的五處：
  1. **272K 的加價門檻被套到 Astra**（summary 3、表格 caption、FAQ 5）：272K 只印在 GPT-6.1 Sol 的模型頁；價目表只分 Short／Long context 兩欄，沒有印 Astra 的門檻。改成限定 GPT-6.1 Sol，表格與 FAQ 改寫「價目表另列較高的長脈絡價格」。
  2. **「這是編輯換算，不是 OpenAI 印出的倍數」是錯的**：OpenAI 的 RSS 就印了 “one-fifth of Astra’s standard API input and output token prices”。RSS 不在 `sources[]`，所以改成「由編輯以牌價換算」，全文只出現這一次，只限輸入與輸出。
  3. **第二段「OpenAI 的公告頁這次讀不到」**（協調者裁定）：刪掉，改成讀者要的範圍說明——根據 API 模型頁、價目表、ChatGPT 與 Codex 說明文件的 Models 頁與 system card 增補整理，評測只寫 system card 的安全與對齊評測；不提 403。
  4. **「不是另一份獨立的 system card」刪除**：PDF 自己的標題是「GPT-6.1 Sol System Card」、首頁印「Addendum: GPT-6.1 Sol System Card」；網頁頁題是 Addendum，這句否定是推論，來源沒寫。
  5. **台灣否定句**：「以 Taiwan 一詞在這四頁搜尋…未見」是查法不是內容；改成「截至 2026 年 9 月 30 日，這幾份文件都沒有寫，也沒有針對 GPT-6.1 Sol 列出國家或地區限制」。FAQ 7「答案只能是官方頁沒有寫」範圍比讀到的大，改成列出四份文件。
- 研究紀錄 `unverified_or_excluded` 第 2 條與 `must_not_write` 第 3 條：「寫入快取 2.50 對 12.50 不是五分之一」是算術錯誤（2.50×5＝12.50）。已改正；結論不變（OpenAI 那句只講 input and output，所以仍只寫兩欄）。快取輸入 0.10 對 1.00 是十分之一。
- 自檢：`OK ai-news-gpt-61-sol-20260929 zh-TW paragraphs 2998`（exit 0，零 FAIL）。
- 結論：`ok`（事實改 10 處，未超過十處；骨幹論述不變）。第二輪照 DELTA-4-9 第 8 條照常進行，請特別看第一段新補的句子。

## 重抓結果（2026-09-30，UTC）

UA：`Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL --compressed --max-time 90`，同主機間隔 ≥1.2 秒，請求沒有任何人的姓名、email 或個資。

| 時間 | 網址 | HTTP | 落地 bytes | 正文？ |
| --- | --- | --- | --- | --- |
| 10:37:39Z | https://developers.openai.com/api/docs/models/gpt-6.1-sol | 200，0 轉址 | 447,982（與研究代理落地檔相同） | 是：定位句、推理強度、資料落地、規格卡、Text tokens 價格與計價規則、Snapshots |
| 10:37:41Z | https://developers.openai.com/api/docs/pricing | 200，0 | 575,660（相同） | 是：Flagship 表五個分頁，可見三列 gpt-6-astra／gpt-6.1-sol／gpt-6-luna；`tier:standard` 元件 props 含 gpt-6-sol |
| 10:37:43Z | https://learn.chatgpt.com/docs/models | 200，0 | 584,535（相同） | 是：Recommended models、三張模型卡、〈GPT-6.1 Sol〉推出範圍段、GPT-5.5 退役段 |
| 10:37:44Z | https://deploymentsafety.openai.com/gpt-6-1-sol | 200，0 | 543,894（相同） | 是：Published September 29, 2026、第 1–10 節 |
| 10:37:47Z | …/gpt-6-1-sol/gpt-6-1-sol.pdf（不在 sources，交叉核對） | 200 | 8,020,508 | 48 頁（pypdf），首頁「Addendum: GPT-6.1 Sol System Card 2026-09-29」 |
| 10:38Z | https://openai.com/index/introducing-gpt-6-1-sol（不在 sources） | 403 | 5,141 | 否：Cloudflare 挑戰頁，未使用 |

`verbatim_quote` 逐字比對（`q.py`：html.parser、去 script／style／noscript／svg／template 與註解、html.unescape、只壓 ASCII 空白，NBSP／U+2011／U+2019 不動；A 區塊標籤→空格、B 全部→空格、C 全部→無，外加解碼後 RAW）：45/45 通過，所有 `url` 都在 `sources[]`。第 16 條（gpt-6-sol 價格）只在 RAW 成立：位於 `component-export="TextTokenPricingTables"`、`props={"tier":[0,"standard"],"collapsedLatestRowCount":[0,3],…}` 的 rows 第四列，`[0,"gpt-6-sol"],[0,2],[0,0.2],[0,2.5],[0,10]`；同一份 rows 第一列 gpt-6-astra 是 10／1／12.5／50，與可見的短脈絡欄一致，所以這四個數字是 Standard 短脈絡。

## 主張逐條

來源代號：M＝API 模型頁、P＝價目表、L＝learn.chatgpt.com Models、S＝system card 增補。

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | GPT-6.1 Sol 推出 | CONFIRMED | S “Today, we’re introducing GPT-6.1 Sol.” |
| 2 | title | 新一版 Sol | CONFIRMED | L “the previous Sol model” |
| 3 | title | 上 API、Codex、ChatGPT Work；Chat 裡沒有 | CONFIRMED | M Snapshots；L “available in Work and Codex. They aren’t available in Chat.” |
| 4 | description | 2026-09-29 推出 | CONFIRMED | S “Published September 29, 2026” |
| 5 | description | API 名稱 gpt-6.1-sol | CONFIRMED | M “Use gpt-6.1-sol to select this model.” |
| 6 | description | 五方案 Codex 與 Work「首發可用」 | **CHANGED** →「在首發推出範圍內」 | L “launch rollout includes …”＋“Availability depends on the rollout” |
| 7 | description | Enterprise、Edu 要管理員啟用 | CONFIRMED | L |
| 8 | description | Free、Go 首發不含 | CONFIRMED | L “not included at launch” |
| 9 | description | Chat 裡沒有 | CONFIRMED | L |
| 10 | 第 1 段 | 9/29 推出、API 名稱 | CONFIRMED | S、M |
| 11 | 第 1 段 | 說明文件稱 GPT-6 Sol 為前一個 Sol 模型 | CONFIRMED | L |
| 12 | 第 1 段（新補） | 沒有寫 GPT-6 Sol 何時停用 | CONFIRMED | M、P、L、S 的 retire／deprecat 只出現在 GPT-5.5、Codex-Spark 與導覽列 |
| 13 | 第 1 段 | 「GPT-6.1 是 GPT-6 系列最新的模型家族」 | CONFIRMED | S 第 1 節 |
| 14 | 第 1 段（新補） | 五方案在 Codex 與 Work，Free/Go 首發不含 | CONFIRMED | L |
| 15 | 第 1 段 | Chat 裡沒有 | CONFIRMED | L |
| 16 | 第 1 段 | 台灣帳號能不能用，文件沒有寫 | CONFIRMED | Taiwan 詞界比對 M、P、L、S、PDF 皆 0 |
| 17 | 第 2 段 | 「OpenAI 的公告頁這次讀不到，所以公告裡的評測分數一律不寫」 | **刪除**（協調者裁定）→ 改寫資料範圍 | DELTA-4-7 第 14 條 |
| 18 | 第 2 段 | 資料來自四份文件 | CONFIRMED | `sources[]` |
| 19 | 第 2 段 | 2026-09-30 查核 | CONFIRMED | 四條 `checked_on`、callout、表格 caption 一致 |
| 20 | 第 2 段 | 評測只寫 system card 的安全與對齊評測 | CONFIRMED | 正文只有 S 第 6、7、5 節的數字與結論 |
| 21 | 第 2 段 | 網站沒實測、不提供購買或換模型建議 | OUT OF SCOPE | 編輯聲明 |
| 22–25 | summary 1 | 日期、API 名稱、前一個 Sol 模型、沒寫停用 | CONFIRMED | S、M、L |
| 26–32 | summary 2 | 五方案、Codex 桌面 App 與 CLI、Work 網頁與行動版、Enterprise/Edu 預設關閉要管理員、Free/Go 首發不含、Chat 沒有 | CONFIRMED | L “in Codex in the desktop app and CLI, and ChatGPT Work on the web and mobile.” |
| 33–38 | summary 3 | 6.1 Sol 2.00／0.10／10.00，Astra 10.00／50.00 | CONFIRMED | P 可見文字；M |
| 39 | summary 3 | 「輸入超過 272K tokens 的請求另計較高價格」（接在 Astra 之後） | **CHANGED** → 限定 GPT-6.1 Sol | 272K 只在 M；P 沒有印 Astra 的門檻 |
| 40 | summary 4 | 資安 Critical、生化 High，「列為」 | **CHANGED** →「視為」 | S “we are treating GPT-6.1 Sol as Critical …” |
| 41 | summary 4 | OpenAI 自己的分級、沒實測 | CONFIRMED／OUT OF SCOPE | S “Under our Preparedness Framework” |
| 42 | §1 p1 | 較低成本、複雜程式、電腦操作、專業工作，接近 Astra（OpenAI 自述） | CONFIRMED | M “delivers near-Astra performance at a lower cost for complex coding, computer use, and professional work” |
| 43 | §1 p1 | 沒有給百分比或分數差 | CONFIRMED | M、L、S 皆只有 near-Astra／comparable |
| 44 | §1 p1 | 建議拿自己的任務和 Astra 比 | CONFIRMED | M “Compare it with Astra on your tasks to assess the tradeoff between quality and cost.” |
| 45 | §1 p2 | 請讀者比較兩者 API 規格差異 | CONFIRMED | L |
| 46 | §1 p2 | 說明文件把 GPT-6 Sol 與 6.1 Sol 並列 Work 與 Codex 可用 | CONFIRMED | L |
| 47 | §1 p2 | 價目表截至查核日仍列 GPT-6 Sol | CONFIRMED | P props |
| 48–52 | §1 p3 | 1,050,000、128,000、2026-04-30、輸入文字與圖片、輸出文字 | CONFIRMED | M 規格卡、“Input Text, Image Output Text” |
| 53–60 | §2 p1 | 6.1 Sol 2.00／0.10／2.50／10.00；Astra 10.00／1.00／12.50／50.00 | CONFIRMED | P 可見文字 |
| 61 | §2 p1 | 「以牌價換算（這是編輯換算，不是 OpenAI 印出的倍數）」 | **CHANGED** →「由編輯以牌價換算」 | OpenAI RSS description 印了 one-fifth；括號內後半句是錯的 |
| 62 | §2 p1 | 輸入、輸出各是 Astra 的五分之一 | CONFIRMED（算術） | 2÷10、10÷50 |
| 63–66 | §2 p2 | GPT-6 Sol 2.00／0.20／2.50／10.00 | CONFIRMED | P props（tier standard） |
| 67 | §2 p2 | 只有快取輸入不同 | CONFIRMED | 同上 |
| 68 | §2 p2 | 「價目表預設只顯示三列，GPT-6 Sol 要展開才看得到；它的長脈絡價格這次沒讀到，不寫。」 | **刪除**（查證細節） | 改成「同一張價目表的 All models 清單裡」，保留讀者點得到的按鈕名 |
| 69 | §2 p3 | 「計價規則寫在模型頁」 | **CHANGED** →「GPT-6.1 Sol 的模型頁寫明」 | 規則印在 6.1 Sol 頁 |
| 70 | §2 p3 | 快取輸入 5% | CONFIRMED | M |
| 71 | §2 p3 | 寫入快取「1.25 倍」 | **CHANGED** →「未快取輸入價的 1.25 倍」 | M “1.25x the uncached input token rate” |
| 72 | §2 p3 | 2.50 比一般輸入貴 | CONFIRMED（算術） | 2.50＞2.00 |
| 73–74 | §2 p3 | 超過 272K：輸入與快取 ×2、輸出 ×1.5、整筆請求 | CONFIRMED | M “for the full request”；P 長脈絡 4.00／0.20／5.00／15.00 吻合 |
| 75–77 | §2 p3 | Fast 2 倍、Batch／Flex 便宜 50%、地區處理 +10% where available | CONFIRMED | M |
| 78 | §2 p4 | 牌價不是訂閱價；這幾頁沒有月費或用量上限 | CONFIRMED | L 只有 “See pricing for plan access and usage” 的連結 |
| 79–82 | table | 12 格 | CONFIRMED | P（可見文字與 props） |
| 83 | table caption | 「GPT-6 Sol 一欄取自價目表展開後的完整清單」 | **CHANGED** →「GPT-6 Sol 列在價目表的 All models 清單」 | 讀者優先 |
| 84 | table caption | 「輸入超過 272K tokens 的請求另計較高價格」（三欄共用） | **CHANGED** →「價目表另列較高的長脈絡價格」 | 見 #39 |
| 85 | §3 p1 | 三個模型在 Work 與 Codex、不在 Chat，原文照引（U+2019） | CONFIRMED | L |
| 86 | §3 p1 | 沒寫 Chat 會不會加入 | CONFIRMED | L 無 yet、無時程 |
| 87–89 | §3 p2 | 五方案、Codex 桌面 App 與 CLI、Work 網頁與行動版 | CONFIRMED | L |
| 90 | §3 p2 | Enterprise、Edu 預設關閉、要管理員啟用 | CONFIRMED | L |
| 91 | §3 p2 | 「文件只點名這兩種方案，Business 怎麼處理這一頁沒有寫」 | **CHANGED** →「Business 是否也要管理員啟用，文件沒有寫」 | L 只點名 Enterprise 與 Edu；Business 在推出名單內 |
| 92 | §3 p2 | Free、Go 不在首發範圍、沒寫之後 | CONFIRMED | L |
| 93–94 | §3 p3 | Standard、Fast 首發；Ultrafast coming later、無日期 | CONFIRMED | L |
| 95 | §3 p3 | 推出期間 GPT-5.6 三型仍可用 | CONFIRMED | L |
| 96 | §3 p3 | 取決於推出進度、登入方式、用戶端 | CONFIRMED | L |
| 97 | §3 p3 | 選新模型不改權限、不取得使用權 | CONFIRMED | L |
| 98 | §3 p4 | 「以 Taiwan 一詞在這四頁搜尋…未見，這幾頁也沒有列出國家或地區限制」 | **CHANGED**（限縮、刪查法） | 導覽列有 “Supported countries” 連結，所以改成「沒有針對 GPT-6.1 Sol 列出」 |
| 99–100 | image caption | 四個開放範圍、查核日；與 `diagram.caption` 相同 | CONFIRMED | L、M |
| 101–104 | diagram nodes | Plus 等方案／Free 與 Go／Chat 模式／API | CONFIRMED | L、M |
| 105–106 | §4 p1 | Deployment Safety Hub、頁題、增補、9/29 | CONFIRMED | S |
| 107 | §4 p1 | 「不是另一份獨立的 system card」 | **刪除** | PDF 標題「GPT-6.1 Sol System Card」；否定句來源沒寫 |
| 108–110 | §4 p2 | 資安 Critical、生化 High、AI 自我改進低於 High | CONFIRMED | S 第 9 節逐字 |
| 111 | §4 p2 | 內部分級、不是外部評等 | CONFIRMED | “our Preparedness Framework” |
| 112 | §4 p2 | 「這一篇也不寫攻擊細節」 | **刪除**（編輯流程） | DELTA-4-7 第 14 條 |
| 113 | §4 p3 | 與 Astra 處理相同、套用相同防護 | CONFIRMED | S “As we did for GPT-6 Astra …”、“applied the same safeguards stack” |
| 114 | §4 p3 | Daybreak 分階段；「這一頁沒有細寫申請與對象」 | **CHANGED** →「Daybreak 的開放細節要看 GPT-6 Astra system card」 | S “For more details on Daybreak access, please see … the GPT-6 Astra card.” |
| 115 | §4 p3 | SAG 建議與領導層判斷，歸因 OpenAI | CONFIRMED | S 9.2 |
| 116 | §4 p4 | 研究環境或 API、可能與正式版 ChatGPT 略有不同 | CONFIRMED | S 註腳 1 |
| 117 | §4 p4 | 使用者標記案例上幻覺率 similarly low（6.1 對 6 Sol） | CONFIRMED | S 6.1 |
| 118 | §4 p4 | HealthBench 與 Astra 相當 | CONFIRMED | S “on par with GPT-6 Astra” |
| 119 | §4 p4 | 「程式工作的不實陳述評測」1.50／0.51／1.30 | **CHANGED**（補評測名） | S 7.4.1 Coding Deception（7.4 Avoiding Deceptive Interactions with Users）；三個數字與比較對象逐字相符 |
| 120 | §4 p4 | 刻意挑來誘發不誠實、不代表正式環境 | CONFIRMED | S 同段 |
| 121 | §5 p1 | 看 Codex／Work 模型選單；Enterprise／Edu 找管理員 | CONFIRMED | L |
| 122–123 | §5 p2 | 美國與歐盟資料落地；歐盟不能 Fast | CONFIRMED | M |
| 124 | §5 p3 | 「之後會改」 | **CHANGED** →「之後可能改」 | 預測，來源沒寫 |
| 125 | FAQ 1 | 前一個 Sol、只差快取輸入 | CONFIRMED | L、P |
| 126 | FAQ 2 | 「這幾頁」沒寫停用 | **CHANGED**（列出頁名） | FAQ 單獨被引用時要自足 |
| 127 | FAQ 3、4 | Free/Go 首發不含；Chat 沒有、沒時程 | CONFIRMED | L |
| 128 | FAQ 5 | 272K 接在 Astra 價格之後 | **CHANGED** →「價目表另列較高的長脈絡價格（GPT-6.1 Sol 適用於輸入超過 272K tokens 的請求）」 | 見 #39 |
| 129 | FAQ 6 | 內部分級、同一套防護 | CONFIRMED | S |
| 130 | FAQ 7 | 「答案只能是官方頁沒有寫」 | **CHANGED** → 限縮到四份文件與查核日 | BRIEF 第 2 條 |
| 131 | callout | 截至 9/30、可能改動；沒有實測、不是建議 | CONFIRMED／OUT OF SCOPE | — |

## 改掉的地方（原文 → 改成，依據）

1. **summary 3、表格 caption、FAQ 5**：「輸入超過 272K tokens 的請求另計較高價格」→ summary 限定「GPT-6.1 Sol 輸入超過 272K…」；caption「價目表另列較高的長脈絡價格」；FAQ「價目表另列較高的長脈絡價格（GPT-6.1 Sol 適用於輸入超過 272K tokens 的請求）」。M 印 “Prompts with more than 272K input tokens are priced at 2x input and cache rates and 1.5x output for the full request.”；P 的 Flagship 表只有 Short context／Long context 欄名，沒有印 gpt-6-astra 的門檻。原句接在 Astra 價格之後，讀起來 Astra 也是 272K，來源撐不住。
2. **§2 p1**：「以牌價換算（這是編輯換算，不是 OpenAI 印出的倍數）」→「由編輯以牌價換算」。OpenAI 的 RSS 印了 “one-fifth of Astra’s standard API input and output token prices”，括號後半句與事實相反；RSS 不在 `sources[]`，所以維持編輯換算，全文「五分之一」只出現這一次，只限輸入與輸出。
3. **第 2 段**：刪「OpenAI 的公告頁這次讀不到，所以公告裡的評測分數一律不寫」，改寫資料範圍（協調者裁定；DELTA-4-7 第 14 條）。
4. **§4 p1**：刪「不是另一份獨立的 system card」。PDF `/Title` 是 “GPT-6.1 Sol System Card”，首頁 “Addendum: GPT-6.1 Sol System Card”。
5. **§3 p4、FAQ 7**：台灣否定句限縮到這幾份文件與 2026-09-30，刪查法；「沒有列出國家或地區限制」加「針對 GPT-6.1 Sol」，因為 M、P、L 導覽列都有 Supported countries 連結。
6. **§4 p3**：「（這一頁沒有細寫申請與對象）」→「Daybreak 的開放細節要看 GPT-6 Astra system card」。S：“For more details on Daybreak access, please see the Trusted Access for Cyber section in the GPT-6 Astra card.”
7. **description**：「首發可用」→「在首發推出範圍內」。L 的用詞是 rollout，同頁另寫 “Availability depends on the rollout”。
8. **§5 p3**：「之後會改」→「之後可能改」。
9. **§3 p2**：「文件只點名這兩種方案，Business 怎麼處理這一頁沒有寫」→「Business 是否也要管理員啟用，文件沒有寫」。Business 在推出名單裡，只是沒有「管理員啟用」這個條件。
10. **§2 p3**：「計價規則寫在模型頁：…寫入快取是 1.25 倍」→「GPT-6.1 Sol 的模型頁寫明計價規則：…寫入快取是未快取輸入價的 1.25 倍」。

讀者優先與用語（不算事實修改）：§2 p2 刪「價目表預設只顯示三列…長脈絡價格這次沒讀到，不寫」，改「同一張價目表的 All models 清單裡」；§4 p2 刪「這一篇也不寫攻擊細節」；§4 p4 補評測名 Coding Deception；summary 4「列為」→「視為」；FAQ 2 的「這幾頁」列出頁名；第 1 段補「但沒有寫 GPT-6 Sol 何時停用」與首發方案（DELTA-4-9 第 4 條：開頭段交代舊版怎麼處理；DELTA-4-7 第 14 條：第一段講讀者能不能用）。字數因此到 3,085，刪掉的都是重複敘述（§1 p2 重複的「前一個 Sol 模型」與停用句、§3 p1「寫得很明確」、§4 p2 重複的「OpenAI 對自家模型」、§4 p3 重複的「對 GPT-6.1 Sol」、第 2 段與 §2 p1 的標價說明合併），沒有刪任何但書、限定詞或歸因；最後 2,998。

## 協調者點名的八項

1. 價目表 12 格全對。GPT-6 Sol 2／0.2／2.5／10 在 `tier: standard` 的元件 props，第一列 Astra 與可見短脈絡欄相同，確認是 Standard 短脈絡。「預設只顯示三列、要展開」屬查證細節，已刪，只保留讀者點得到的「All models」。
2. 「五分之一」全文一次，寫「由編輯以牌價換算」，只限輸入與輸出，不在標題、description、summary、圖。研究紀錄算術已改。
3. 1.50%／0.51%／1.30%：S 7.4.1 Coding Deception，比較對象 GPT-6 Astra 與 GPT-6 Sol 逐字相符，但書同段。原文同段另有「GPT-5.6 Sol 在最高推理強度下約 7 倍」，正文未寫，不影響。
4. 方案可用性逐字對 L：Plus、Pro、Business、Enterprise、Edu；Codex 桌面 App 與 CLI、Work 網頁與行動版；只有 Enterprise 與 Edu 寫預設關閉要管理員啟用；Business 沒有這個條件，正文寫「文件沒有寫」，沒有推論。
5. 台灣否定句已限縮並刪查法。
6. 第二段已依裁定改寫，不提 403。
7. Preparedness 三項照 S 第 9 節；Critical 定義的攻擊描述句（研究紀錄 #37）沒有進正文；ExploitBench 等資安分數沒寫。
8. 沒有購買建議、沒有「該不該換」、沒有推定台灣可用；正文數字除評測外都在 M、P、L、S；沒有 44.8%／16.1%。

## 界線檢查

- 購買建議／推薦式比價：無。L 的「Consider GPT-6.1 Sol … when cost matters」沒有寫進正文。
- 沒歸因的廠商宣稱：near-Astra、幻覺、HealthBench、SAG 判斷都有「OpenAI 表示／自述」。
- 預告／分批：Ultrafast「之後才會有」、rollout、Daybreak 分階段、Enterprise／Edu 預設關閉都有寫。
- 「本文」0 次；「官方」0 次；「403」0 次。

## 留給站主的事

1. 若協調者把 RSS 換進 `sources[]`，五分之一可以改成「OpenAI 表示輸入與輸出牌價是 Astra 的五分之一」並歸因。
2. L 的 GPT-5.5 退役段仍建議 Plus–Edu「choose GPT-6 Sol (gpt-6-sol) when available」，與同頁推薦 GPT-6.1 Sol 不一致；沒寫進正文。
3. 價目表「All models」按鈕名與收合狀態是介面，發布當天和其他活頁面一起重讀（`live_data_warnings`）。
4. 公告頁 2026-09-30T10:38Z 仍 403（5,141 bytes 挑戰頁）；文章沒有任何句子靠它。

## 結論

`ok`。事實修改 10 處，骨幹論述（新一版 Sol、牌價、推出範圍、Preparedness 分級）不變；自檢零 FAIL。
