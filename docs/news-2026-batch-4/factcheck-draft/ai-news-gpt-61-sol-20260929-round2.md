# 查核報告（第二輪）：ai-news-gpt-61-sol-20260929

## 第二輪

- 查核者：獨立查核代理（第二輪，opus），2026-09-30；沒有參與研究、撰稿與第一輪。
- 規格：`agents/ai/SECOND-ROUND.md`、`agents/ai/FACTCHECK.md`（Windows 路徑與「允許的 FAIL」不適用）、`DELTA-4-9.md`、`DELTA-4-7.md` 第 11–14 條、`BRIEF.md` 十二種錯誤型態、`ai.md`。
- 改動的檔案：內容包、研究紀錄（加 `factcheck.second_round`）、本報告。第一輪報告未改。
- 暫存：`/root/news49/agents/fc2/`（`s1–s4.html`、抽字 `s1–s4.txt`、`ext.py`、逐字比對 `q.py`、`fetch.log`、`check.log`）。

### 摘要

- 覆核 74 條主張（第一輪改過的段落、第一輪新寫的句子、summary、FAQ、圖解、協調者點名的五項），`verbatim_quote` 45 條。
- 改 9 處。最重的三處：
  1. **第一段第一輪新補的方案句掉了 Enterprise／Edu 的管理員條件**：「首發給 Plus、Pro、Business、Enterprise、Edu 在 Codex 與 ChatGPT Work 使用」→「首發推出範圍包括 …（Enterprise 與 Edu 要管理員啟用）」。來源 L：“For Enterprise and Edu, the plan keeps GPT-6.1 Sol off by default until an administrator enables it.”
  2. **Coding Deception 的但書被收窄**：「刻意挑來誘發不誠實行為的，比例不代表正式環境的實際情況」→「刻意挑來誘發可能的不誠實行為，觀察到的比例預期不會等於正式環境的實際比例」。S 7.4.1：“deliberately selected to elicit **potentially** dishonest behavior and the observed rates are **not expected to match** the true rate of misbehavior in production.”
  3. **第二段第一輪新寫的範圍句不對**：「評測只寫 system card 的安全與對齊評測」，但正文用了 HealthBench（S 第 5 節 Health）與幻覺（第 6 節 Hallucinations），兩者都不在 Alignment。改成「評測只引 system card 增補」。
- 自檢：`OK ai-news-gpt-61-sol-20260929 zh-TW paragraphs 2992`（exit 0，零 FAIL）。
- 結論：`ok`。

### 重抓結果（2026-09-30，UTC）

UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，`curl -sSL --compressed --max-time 90`，間隔 1.5 秒；請求沒有任何人的姓名、email 或個資。

| 時間 | 網址 | HTTP | 落地 bytes | 正文？ |
| --- | --- | --- | --- | --- |
| 10:46:14Z | https://developers.openai.com/api/docs/models/gpt-6.1-sol | 200，0 轉址 | 447,982 | 是：定位句、資料落地、規格卡、Text tokens 價格與計價規則、Snapshots |
| 10:46:17Z | https://developers.openai.com/api/docs/pricing | 200，0 | 575,660 | 是：Flagship 表五個分頁；`tier:standard` props 第四列 gpt-6-sol 2／0.2／2.5／10 |
| 10:46:18Z | https://learn.chatgpt.com/docs/models | 200，0 | 584,535 | 是：Recommended models、三張模型卡、〈GPT-6.1 Sol〉推出範圍段 |
| 10:46:20Z | https://deploymentsafety.openai.com/gpt-6-1-sol | 200，0 | 543,894 | 是：Published September 29, 2026、第 1–10 節 |

四條的落地 bytes 與研究代理、第一輪完全相同。

### `verbatim_quote` 逐字比對

`q.py`：html.parser 抽字（去 script／style／noscript／svg／template）、`html.unescape`、所有空白壓成一格，對可見文字做連續子字串比對；不中再對去標籤後的全文、再對解碼後的原始 HTML。45/45 通過，所有 `url` 都在 `sources[]`。44 條在可見文字成立；第 16 條（`[0,"gpt-6-sol"],[0,2],[0,0.2],[0,2.5],[0,10]`）只在解碼後的 HTML 成立，位於 `tier:[0,"standard"]` 的 `TextTokenPricingTables` props，與第一輪結論相同。沒有任何一條含 `...`、`…` 或 `|`。第 7、9、14、15、28 條是相鄰頁面元素以空白接起來的字串，在來源裡順序相同、中間沒有其他文字。

### 改掉的地方（原文 → 改成，依據）

1. **第一段**（第一輪新補）：「首發給 Plus、Pro、Business、Enterprise、Edu 在 Codex 與 ChatGPT Work 使用」→「首發推出範圍包括 Plus、Pro、Business、Enterprise、Edu 的 Codex 與 ChatGPT Work（Enterprise 與 Edu 要管理員啟用）」。第一段是讀者判斷「跟我有沒有關係」的地方，Enterprise／Edu 使用者照原句會以為開箱即用。
2. **「首發範圍是」→「首發範圍包括」**（第一段、summary 2、§3 p2、FAQ 3）：L 原文 “The GPT-6.1 Sol launch rollout **includes** Plus, Pro, Business, Enterprise, and Edu”。BRIEF 第 3 條：includes 起頭的名單不寫成全清單。FAQ 3 同時補「其中 Enterprise 與 Edu 要管理員啟用」（正文已有）。
3. **第一段**：「但沒有寫 GPT-6 Sol 何時停用」→「但這幾份文件沒有寫 …」。否定句限縮到文件範圍。四份文件以詞界比對 retire／deprecat：S 0 次；M、P 只有導覽列 Deprecations 與 fine-tuning 段；L 只涉及 GPT-5.5、GPT-5.3-Codex-Spark、gpt-5.4、gpt-5.2。
4. **第二段**（第一輪新寫）：「評測只寫 system card 的安全與對齊評測」→「評測只引 system card 增補」。見摘要第 3 點。
5. **第二段**：刪「價格與開放範圍以當天頁面為準」。同義敘述另見 callout（「都是截至 2026 年 9 月 30 日的頁面內容，之後可能改動」）與 §5 p3（「都是首發當下的描述，之後可能改」），為了讓補回的但書不超過 3,000 字而刪；查核日本身保留。
6. **§2 p1**：「由編輯以牌價換算，輸入 2.00 美元對 10.00 美元、輸出 10.00 美元對 50.00 美元，GPT-6.1 Sol 各是 Astra 的五分之一」→「由編輯以牌價換算，GPT-6.1 Sol 的輸入與輸出牌價各是 Astra 的五分之一」。四個數字在前一句已列出，屬重複；「以牌價換算」「輸入與輸出」的限定都保留。
7. **§4 p3**：「並因此套用與 GPT-6 Astra 相同的防護措施」→「並依上述分級套用 …」。原句的「因此」只接在資安 Critical 後面；S 第 9 節是 “Based on this assessment, we applied the same safeguards stack”，this assessment 指三個領域的判定（同節另寫 “consistent with our decision to adopt the same Preparedness determinations for both models”）。
8. **§4 p3**：「資安用途和 Astra 一樣透過 Daybreak 分階段開放，Daybreak 的開放細節要看 GPT-6 Astra system card」→「和 Astra 一樣，GPT-6.1 Sol 的資安存取透過 Daybreak 採分階段做法，細節要看 GPT-6 Astra system card」。S 9.2.1.3（Trusted Access for Cyber）：“Like Astra, we are taking a phased approach for GPT-6.1 Sol through Daybreak”；「分階段開放」讀起來像已經在開放，來源寫的是做法。
9. **§4 p4**、**FAQ 2**：Coding Deception 但書（見摘要第 2 點）；FAQ 2 的否定句原本只列三份文件、日期放在第二句，改成「截至 2026 年 9 月 30 日，… 模型頁、價目表、Models 頁與 system card 增補都沒有寫 …」，單獨被引用時也有日期與完整範圍。

### 第一輪新寫或改過的句子，查過而且正確

- 第一段「說明文件稱 GPT-6 Sol 為『前一個 Sol 模型』」：L “To see how its API specifications differ from the previous Sol model, compare GPT-6.1 Sol and GPT-6 Sol.”
- 第一段 system card 引句：S “GPT-6.1 is the latest model family in the GPT-6 series.”
- summary 3、§2 p3、FAQ 5：272K 只掛 GPT-6.1 Sol（M “Prompts with more than 272K input tokens are priced at 2x input and cache rates and 1.5x output for the full request.”）。價目表也印了 Astra 的長脈絡價格（20／2／25／75），但沒有印門檻，正文沒有替 Astra 寫門檻；表格 caption「價目表另列較高的長脈絡價格」沒有數字，成立。
- §2 p3「未快取輸入價的 1.25 倍」「5%」「Fast 2 倍」「Batch 與 Flex 便宜 50%」「有提供地區處理的地方加收 10%」：M 逐字。
- §3 p2「Business 是否也要管理員啟用，文件沒有寫」：L 只點名 Enterprise 與 Edu，Business 在推出名單內；沒有推論。
- §3 p3「Ultrafast 支援『之後才會有』，沒有日期」：L “Ultrafast support for GPT-6.1 Sol is coming later.”，同段沒有日期；沒有寫成已上線。API 價目表的 Ultrafast 分頁只有 gpt-6-astra 一列，與此不衝突。
- §3 p4、FAQ 7 台灣否定句：已限縮到這幾份文件與 2026-09-30；Taiwan 詞界比對四份皆 0 次。
- §4 p1：頁題與「Published September 29, 2026」逐字。
- §4 p2、summary 4、FAQ 6：S 第 9 節 “Critical capability in Cybersecurity, High capability in the Biological and Chemical domain, and below the High threshold in AI Self-Improvement”；「視為」對應 treating。
- §4 p3 SAG 句：S 9.2 “informed our Safety Advisory Group’s recommendation and OpenAI leadership’s determination that these safeguards are sufficient for GPT-6.1 Sol’s public launch.”
- §4 p4：評測環境註腳、幻覺 “similarly low”（6.1 Sol 對 6 Sol，Cases Flagged by Users）、HealthBench “on par with GPT-6 Astra”、1.50%／0.51%／1.30% 與比較對象逐字。
- 表格 12 格、FAQ 1、FAQ 5 的數字：P 可見文字與 props。

### summary、FAQ、圖

- summary 四句的內容與數字都在正文；FAQ 七題的答案都在正文（FAQ 3 新補的管理員條件在第一段與 §3 p2）。
- `diagram` nodes 只有「6.1」這個數字（在正文）；`hero_label`「新一版的 Sol」在第一段。title、image caption 未改，研究紀錄不用同步。

### 協調者點名

- (a) 五分之一：全文一次，在 §2 p1，「由編輯以牌價換算」，只限輸入與輸出；title、description、summary、FAQ、圖都沒有。
- (b) 272K：只限 GPT-6.1 Sol（見上）。
- (c) Enterprise／Edu 管理員啟用、Business「文件沒有寫」：逐字對 L，成立；第一段補回漏掉的條件。
- (d) Preparedness 三項：照 S 第 9 節，成立；防護措施的依據改成「依上述分級」。
- (e) 「Ultrafast 之後才有」有來源（L），沒有寫成已上線；「Daybreak 分階段」有來源（S 9.2.1.3），改寫成「採分階段做法」，不寫成已開放。

### 回掃但書

第一輪為字數刪掉的都是重複敘述（§1 p2 的前一個 Sol 模型、§3 p1「寫得很明確」等），沒有刪 up to、may、可能或歸因。這一輪找到的兩個但書問題（Coding Deception 的 potentially／not expected to match、Enterprise／Edu 管理員條件）不是第一輪刪掉的，是原稿就漏了（前者）與第一輪新句漏了（後者），都已補回。補回後的字數靠刪第 5、6 點的重複敘述騰出，最後 2,992。

### 界線

沒有購買建議與「該不該換」；沒有推定台灣可用；沒有能力評測分數；沒有 44.8%／16.1%；沒有攻擊細節（Critical 定義的引句沒進正文）；一個 callout、無 `finance`；「本文」「官方」各 0 次。

### 留給站主的事

1. 圖解第一格「Plus 等方案／Codex、Work 可選」沒有 Enterprise／Edu 要管理員啟用的條件，caption 也沒有。重畫圖不在這一輪的檔案範圍；要補的話，caption 與研究紀錄 `diagram.caption` 要一起改。
2. 第一輪留下的四項照舊（RSS 若換進 `sources[]` 可改成歸因給 OpenAI；L 的 GPT-5.5 段仍建議 GPT-6 Sol；All models 按鈕名是介面；公告頁 403）。

### 結論

`ok`。改 9 處，骨幹論述不變；自檢零 FAIL。
