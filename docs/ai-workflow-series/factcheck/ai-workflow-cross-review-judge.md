# 獨立查核：ai-workflow-cross-review-judge

查核代理：未參與撰稿。查核日 **2026-09-19**（`date -u +%F` 取一次）。
文章的 `checked_on` 本來就是 **2026-09-18**、八條 source 與研究紀錄一致，
而且今天重抓後**沒有任何一個數字或原句因為頁面改版而變動**，所以依 FACTCHECK 第 1 節
「不要因為你今天重查就改它」，`checked_on` 一律**維持 2026-09-18 不動**。
只有研究紀錄 `code_samples` 裡多數決那塊的 `compiled_on` 改成 2026-09-19，
因為那塊程式是今天被本代理改掉並重新編譯的。

查核方式：`sources[]` 八條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body
（GitHub 的三個檔走 `raw.githubusercontent.com`），逐句把 title、description、正文、
摘要、FAQ、callout、表格每一格與 caption、圖解 caption 與節點對回原文；
研究紀錄的 `verbatim_quote` 用程式做**連續字串**比對，而且**同時比對原始 HTML 與去標籤後的正文**；
三塊 `code` 重新抽出到暫存目錄編譯，純 Python 那塊實際執行並補跑邊界案例；
模型 id 另外到三家官方模型頁確認仍在。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料**，
也**沒有使用 `sources[]` 以外的網址替文章補任何事實**（讀模型頁只為了反駁與確認 id，未寫進文章）。

檢查的主張：**約 110 條**（正文 44 個句／子句、摘要 5 句、FAQ 5 題答句、callout 2 句、
表格 12 格、表格與圖解 caption 各 1、圖解 4 組節點、`hero_label`、title、description，
外加三塊程式共約 46 個識別字），另有研究紀錄原本 26 條引文。
**改了 10 處（內容包 8 處、研究紀錄 2 組）**，另有 4 件留給站主。

## 重抓結果：八條 sources 今天都讀到正文，不是擋阻頁

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `platform.openai.com/docs/guides/evals` | 200 | 729,709 | **是**。去標籤後 47,947 字元；「Working with evals」全文、三步驟清單、Python／JS／Ruby／REST 範例與 `OpenAI is deprecating the Evals platform.` 的完整公告段都在 |
| `platform.openai.com/docs/guides/evaluation-best-practices` | 200 | 410,401 | **是**。31,747 字元；`Create and combine different types of evaluators` 整節在，含 Metric-based／Human／LLM-as-a-judge 三塊的 Examples／Challenges／Recommendations |
| `raw.githubusercontent.com/openai/openai-python/main/README.md` | 200 | 41,584 | **是**。純 Markdown，Responses 快速上手、Chat Completions 對照、`## Timeouts` 整節都在 |
| `platform.claude.com/docs/en/test-and-evaluate/develop-tests` | 200 | 1,934,869 | **是**。26,208 字元；`Grade your evaluations`、`Tips for LLM-based grading` 三條與兩段 Python 範例都在 |
| `platform.claude.com/docs/en/api/sdks/python` | 200 | 754,022 | **是**。24,834 字元；Usage 範例、`Timeouts` 整節、各家 Provider 對照表都在 |
| `ai.google.dev/gemini-api/docs/structured-output` | 200 | 330,008 | **是**。45,143 字元；Recipe Extractor 等四組 Python／JS／Java／REST 範例、`Best practices`、`Limitations` 都在，頁尾寫 `Last updated 2026-09-17 UTC` |
| `raw.githubusercontent.com/googleapis/python-genai/main/google/genai/types.py` | 200 | 882,336 | **是**。純 Python 原始碼，`class HttpOptions(_common.BaseModel)` 整段可讀 |
| `raw.githubusercontent.com/googleapis/python-genai/main/README.md` | 200 | 54,529 | **是**。純 Markdown，`API Selection`、Proxy、Custom base url 等 `http_options` 段落都在 |

另外為了核 id 讀了三頁官方模型頁（**不是** `sources[]`，只用於反駁，沒有寫進文章）：
`platform.openai.com/docs/models`（200、382,226 bytes，`gpt-5.6-luna` 4 次、`gpt-6-astra` 5 次）、
`platform.claude.com/docs/en/about-claude/models/overview`（200、367,902 bytes，`claude-haiku-4-5-20251001` 5 次）、
`ai.google.dev/gemini-api/docs/models`（200、149,775 bytes，`gemini-3.8-flash` 6 次）。
四個 id 都還在、都已在 `models-seen.json` 裡，**`models-seen.json` 不需要新增任何條目**。

## 程式範例重驗

三塊都用 `apps/api/.venv/bin/python3 -m py_compile` 重編譯。第三塊是純 Python，
在暫存目錄**實際執行**並補跑邊界案例；第一、二塊需要金鑰與網路，**沒有執行**。

| # | label | 語言 | 行數 | 編譯 | 比對過的簽名／參數／端點 | 文件 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 兩個模型各答一次（需要 openai、anthropic 套件） | python | 41 | **ok** | `from openai import OpenAI`、`OpenAI(timeout=20.0)`、`client.responses.create(model=, input=[{"role": "developer"…}])`、`response.output_text`、`OPENAI_API_KEY`；`from anthropic import Anthropic`、`Anthropic(timeout=20.0)`、`client.messages.create(model=, max_tokens=, messages=)`、`next(block.text for block in message.content if block.type == "text")`、`ANTHROPIC_API_KEY`；id `gpt-5.6-luna`、`claude-haiku-4-5-20251001` | openai-python README `## Timeouts` 與快速上手；evals 指南的 Python 範例；Claude Python SDK 頁 Usage 與 Timeouts；develop-tests 的評分範例 |
| 2 | 第三個模型依 rubric 評分並輸出 JSON（需要 google-genai、pydantic 套件） | python | 48 | **ok** | `from google import genai`、`from google.genai import types`、`genai.Client(http_options=types.HttpOptions(timeout=20000))`、`client.interactions.create(model=, input=, response_format={…})`、`"type": "text"`、`"mime_type": "application/json"`、`"schema"`、`Verdict.model_json_schema()`、`interaction.output_text`、`model_validate_json`、`GOOGLE_API_KEY`；id `gemini-3.8-flash` | 結構化輸出頁的 Recipe Extractor Python 範例（逐字同形）；google-genai README 的 `http_options` 與 `GEMINI_API_KEY`／`GOOGLE_API_KEY` 段；types.py 的 `class HttpOptions` |
| 3 | 多數決函式（純 Python，離線可跑） | python | 25 → **31** | **ok**（改寫後重編譯＋實跑） | `collections.Counter`、`Counter.most_common()`、`ValueError` | docs.python.org `collections` |

第 2 塊的「協調者特別交辦」結論：**Gemini 那塊不用改參數名**。
今天（2026-09-19）`ai.google.dev/gemini-api/docs/structured-output` 的 Python 示範就是
`interaction = client.interactions.create(model="gemini-3.8-flash", input=prompt,
response_format={"type": "text", "mime_type": "application/json", "schema": Recipe.model_json_schema()})`，
後面接 `Recipe.model_validate_json(interaction.output_text)`；
同頁 REST 範例打的端點是 `https://generativelanguage.googleapis.com/v1beta/interactions`。
草稿寫的 `response_format`／`mime_type`／`schema` 與方法名**逐字相符**，
頁面上**沒有** `response_mime_type`、`response_schema`、`GenerateContentConfig` 或 `generate_content`
（那些只出現在 google-genai 的 README，屬於另一組 API，本文沒有用）。

第 3 塊實跑的結果（改寫前 → 改寫後）：

| 輸入 | 改寫前回傳 | 改寫後回傳 | 正文怎麼說 |
| --- | --- | --- | --- |
| `["A","A","B"]` | `"A"` | `"A"` | 示意：A ✔ |
| `["A","B","tie"]` | `None` | `None` | 示意：None ✔ |
| `["A","A","B","B","tie"]`（quorum 0.6） | `None` | `None` | 示意：None ✔ |
| `["A","A","B","B"]` | **`"A"`** | `None` | 「沒有任何一方過半時回傳沒有結論」✘ → ✔ |
| `["A","B"]` | **`"A"`** | `None` | 同上 ✘ → ✔ |
| `["A","A","B","C"]`（最高票剛好一半） | **`"A"`** | `None` | 同上 ✘ → ✔ |

## 改掉的 10 處

### 協調者點名的六項

1. **（最重的一處）多數決範例在平手時會硬選一邊，與摘要、正文、FAQ、圖解四處矛盾。**
   協調者要求「實際跑一次確認平手怎麼處理」——跑出來就是錯的。
   原程式 `winner, top = counts.most_common(1)[0]` 加 `if top / len(votes) < quorum`，
   `Counter.most_common(1)` 在票數並列時**按插入順序**回傳第一個，而 `< 0.5` 讓「剛好一半」通過。
   實測 `majority_vote(["A","A","B","B"])` 回 `"A"`、`majority_vote(["A","B"])` 回 `"A"`。
   但摘要第 5 句寫「沒有任何一方**過半**時回傳沒有結論」、docstring 寫同一句、
   FAQ 第 4 題寫「**不會硬選一個**……用偶數個評審時，平手交給人工的機率會比較高」、
   圖解節點寫「多數決／**過半**才採用」。
   已改成先擋並列最高票、門檻改成必須**超過** `quorum`：
   `ranked = Counter(votes).most_common()` → `if len(ranked) > 1 and ranked[1][1] == top: return None`
   → `if top / len(votes) <= quorum: return None`，並加一組 `even_split = ["A","A","B","B"]` 的示例。
   正文投票那段、摘要第 5 句、FAQ 第 4 題同步補上「或是有兩個結論並列最高票」。
   研究紀錄 `code_samples` 的 `lines` 25 → 31、`compiled_on` → 2026-09-19。

2. **「交換順序再評一次」的歸屬與否定範圍（協調者第 2 點）。** 原文寫
   「本站另外建議一個**沒有寫在官方文件裡**、但邏輯上通用的做法」。
   兩個問題：(a) 「沒有寫在官方文件裡」是**無範圍的否定**；
   (b) 這個檢查**站內已經寫過**——`ai-term-llm-as-a-judge` 的原句是
   「位置偏差是指候選順序可能影響評審偏好。**可以把相同候選交換前後位置再評一次**，
   檢視是否出現無法由內容解釋的變化。」寫成「本站另外建議」等於把既有文章的東西當新的講。
   今天用詞界比對過：`swap`／`reverse the order`／`counterbalance`／`both orders`
   在 s1、s2、s4、s5、s6、s8 六頁**各 0 次**（s2 只有一個 `randomized`，
   出現在 **Human evals** 的 `create a randomized, blinded test`，講的是人工評分，不是評審模型）。
   已改成範圍句並點名既有文章：「本文查證當天讀的 OpenAI、Anthropic、Google 三份文件都沒有寫，
   它是本站在『以語言模型擔任評審（LLM-as-a-Judge）是什麼』就提過的檢查」。
   結論也從「代表這組結果本身就**不可信**」降回「就**不能單獨採信**這一組評分」——
   既有文章說的是「檢視是否出現無法由內容解釋的變化」，且明寫
   「這些檢查是設計建議，不代表任何特定模型必然有相同程度的偏差」，原文的斷語比它強。

3. **callout 沒有把「本站做法」與「官方說法」分開（協調者第 2 點）。**
   原 callout 第一句掛 OpenAI 的名，第二句「上線前至少把每組答案交換順序各評一次」緊接著出現，
   讀起來像同一份文件的建議。已在中間插入
   「交換順序再評一次**是本站的建議，不是官方文件寫的做法**：」，並同樣把「不可信」降為「不能單獨採信」。

4. **Gemini 結構化輸出被寫成保證（協調者第 4 點）。** 原文：
   「用 response_format **強制**模型做結構化輸出，回傳的內容**一定要符合**這個 Schema，
   不需要另外寫程式從一段文字裡把 JSON 挖出來。」
   但同一頁自己的 Best practices 與 Limitations 寫：
   `Validation: While output is syntactically correct JSON, always validate values in your application.`、
   `Error handling: Implement robust error handling for schema-compliant but semantically incorrect outputs.`、
   `Schema subset: Not all JSON Schema features are supported.`
   ——只保證**語法**正確，值要自己驗，還有「符合 Schema 但語意不對」的輸出要處理。
   已改成「用 response_format **指定輸出格式**，官方範例把回傳的 `interaction.output_text`
   交給 Pydantic 驗證」，並補一句把三個限制照文件寫出來。
   研究紀錄補三條 `verified_facts` 掛這三句原句。

5. **「OpenAI Evals 平台 2026-11-30 停止服務」（協調者第 5 點）：正文沒有寫，不必刪，但研究紀錄的敘述補精確。**
   正文、摘要、FAQ、callout、表格逐一搜過，**沒有**這個日期，也沒有 Evals 平台的任何句子。
   研究紀錄 `unverified_or_excluded` 有一條當作排除理由，原本只寫「將於 2026 年 11 月 30 日停止服務」。
   今天頁面的原句是
   `Evals will become read-only for existing users on October 31, 2026, and the platform is scheduled to shut down on November 30, 2026.`
   ——**是 scheduled（預定），而且還有一個 10/31 轉唯讀的日期**。已照原句補上「預定」與唯讀日，
   並註明這兩個日期只記在研究紀錄、沒有寫進正文。

6. **「自我偏好查無官方說法」是無範圍否定（協調者第 5、6 點）。** FAQ 第 3 題原文
   「同一顆模型評自己家答案的情況**目前沒有查到可歸因的官方說法**，這篇沒有寫」。
   `self-preference`／`self preference`／`self-enhancement` 在六頁**各 0 次**，事實成立，
   但寫法超出「這幾頁沒有寫」的範圍，而且站內 `ai-term-llm-as-a-judge` 引 Zheng 等人的研究**就提過自我偏好**，
   寫成全稱會跟既有文章打架。已改成
   「模型偏好自己家輸出的『自我偏好』現象，**本文查證當天讀的這三份官方文件都沒有提到**，所以正文沒有寫」。
   同一題順手把「不同廠商」這一層的歸屬講清楚（協調者第 6 點）：
   官方**有**的說法是 Anthropic 評分範例註解裡的
   `Generally best practice to use a different model to evaluate than the model used to generate the evaluated output`
   ——講的是「不同**模型**」；「不同**廠商**」是本文自己的做法，已在答句裡分開寫並各自歸屬。

### 其餘（都在「安靜強化來源」與「限定詞被刪」兩類）

7. **緩解建議掉了「要先跟人工標註一致」這個條件。** 原文
   「也建議先用能力最好的模型當評審，**再視情況換成比較快或比較便宜的模型**」。
   文件的兩句分別是 `Use the most capable model to grade if you can.` 與
   `Once the LLM judge reaches a point where it’s faster, cheaper, and consistently agrees with human annotations, scale up`
   ——**擴大使用的前提是「跟人工標註持續一致」**，不是「視情況」。已照原句改寫。
   同段開頭「文件給的**緩解方式**包括」也改成「文件在**同一段列的建議**包括」：
   文件的結構是 `Challenges :` 之後接 `Recommendations :`，它沒有說這些是用來緩解那兩個偏誤的。

8. **掛在 Anthropic 名下的對照例是草稿自己造的。** 原文
   「例如直接寫『回答一定要在第一句提到指定的名稱……』，**而不是寫『回答要夠專業』這種沒有明確通過條件的敘述**」。
   前半確實是文件的例子（`The answer should always mention 'Acme Inc.' in the first sentence.
   If it does not, the answer is automatically graded as 'incorrect.'`），
   後半那個加了引號的反例**頁面上沒有**。已換成文件真的有的兩句：
   `Purely qualitative evaluations are hard to assess quickly and at scale.`（移到下一段）與
   `might require several rubrics for holistic evaluation.`
   下一段也補上「Anthropic 寫」「文件寫」的歸因，免得跟後面 OpenAI 那段混在一起。

9. **冗長偏誤多了一個文件沒有的說法，而且與既有文章重疊。** 原文
   「冗長偏誤是指評審傾向偏好比較長的回答，**即使長的那份沒有講出更多重點**」。
   文件括號裡只有 `(preferring longer responses)`，沒有「沒有講出更多重點」這個判斷。
   已改成貼著原句的寫法，並在段末補一句
   「這兩個詞站內『以語言模型擔任評審（LLM-as-a-Judge）是什麼』已經解釋過，
   這裡只補上官方文件的出處，以及換成多個評審之後要怎麼處理」——同時處理「不得整段重講」。

10. **「程式本身能編譯、能執行」與同句的「站方沒有拿真實金鑰實際呼叫」互相打架。**
    第一、二塊要金鑰與網路才跑得動，本代理也沒有跑。已改成「程式本身**只通過編譯**」。

### 研究紀錄另外兩組改動

- **一條 `verbatim_quote` 在頁面上搜尋不到。** Google 那條原本寫 `client.interactions.create`，
  但抓下來的 330,008 bytes 原始 HTML 與去標籤後的正文**都找不到這個連續字串**——
  語法高亮把 `client`、`.`、`interactions` 拆進不同的 `<span>`，去標籤後變成
  `client . interactions . create`。已換成同頁 REST 範例裡貨真價實的連續字串
  `https://generativelanguage.googleapis.com/v1beta/interactions`，
  另補 `"mime_type": "application/json"` 與 `model_json_schema` 兩條撐參數名。
- **補 11 條 `verified_facts`**（Anthropic 5、OpenAI 2、Google 4），把新寫進正文的每一句都掛上原句。
  改完全部 **38 條** `verbatim_quote` 重跑連續字串比對：**0 條 miss**。

## 查過而且正確的部分（沒有動）

- **「官方文件目前舉的例子是 gpt-6-astra」（協調者第 1 點）成立。** 今天
  `evaluation-best-practices` 上的原句仍是
  `Start with gpt-6-astra when you need a strong LLM judge, then validate agreement against your human labels before optimizing for cost or latency.`
  ，id 與句子都沒變；正文那句連「確認評分結果跟人工標註一致之後」這個條件都寫了。
  因為沒有任何數字或原句改變，**這條 source 的 `checked_on` 維持 2026-09-18**，其餘七條同步不動。
- **位置偏誤與冗長偏誤的歸因成立。** 原句
  `Challenges : Position bias (response order), verbosity bias (preferring longer responses)`
  今天仍在，摘要第 3 句、description、正文、callout 四處的歸因都寫了「OpenAI 的官方文件」。
- **成本表格與正文自洽（協調者第 3 點）。** 三列算式逐格驗算：
  `n + m` 在 n=2、m=1 是 **3**；`n + m` 在 n=2、m=3 是 **5**；`n + 2m` 在 n=2、m=3 是 **8**。
  正文那段把 2、3、5、6、8 每一個數字都算給讀者看，摘要第 4 句的 5 與圖解節點的 2、3 也都在正文裡。
  caption 已寫「公式為**本站整理，非官方公布數字**（2026 年 9 月）」，查證年月在。
  這三列**沒有任何一格宣稱是官方數字**。
- **`HttpOptions.timeout` 的單位。** types.py 裡 `timeout: Optional[int] = Field(default=None,
  description="""Timeout for the request in milliseconds.""")`，掛在 `class HttpOptions` 底下，
  所以程式裡的 `timeout=20000` 是 20 秒，與其他兩家的 `timeout=20.0`（秒）不同單位但各自正確。
- **限定詞沒有漏。** 結構化輸出頁唯一標 `Preview` 的是
  `Structured outputs with tools`（`This feature is available only to Gemini 3 series models.`），
  本文範例沒有用工具，不缺這個狀態；其餘六頁沒有 beta／preview／限方案的限定詞需要帶。
- **界線。** 全篇只有 **1 個** callout、沒有免責段落、沒有訂閱或購買建議、
  沒有推薦式比價、沒有未經實測的排名或快慢比較、沒有寫「台灣可用」；
  廠商宣稱全部有歸因（「OpenAI 的官方文件」「Anthropic 的官方文件」「Google 建議」）。
- **與必連三篇的分工。** `ai-term-evals` 與 `ai-term-llm-as-a-judge` 各只用一句帶過並留給結尾連結；
  `gemini-cli-subagent-review-workflow` 那句「遇到兩邊建議衝突時只會保留衝突紀錄，不會自動幫忙選邊」
  對得上該篇原文「如果同一組證據得到相反建議，程式保留在 conflicts，**不自動採多數決**」——
  **沒有矛盾**，因為本篇在同一節就把程式碼審查明確劃出去了。
  第二個結尾 link 的 text「以語言模型擔任評審（LLM-as-a-Judge）是什麼」與
  第一個的「多模型 AI 工作流教學：從拆任務到串接不同模型」逐字比對過，**完全相同**。
- **模型 id 全部仍在（協調者第 6 點）**，且都已在 `models-seen.json`：
  `gpt-5.6-luna`、`claude-haiku-4-5-20251001`、`gemini-3.8-flash`、`gpt-6-astra`。
  **`models-seen.json` 沒有新增任何條目。**
- **金鑰與安全。** 三塊程式都只從環境變數讀（`OPENAI_API_KEY`／`ANTHROPIC_API_KEY`／`GOOGLE_API_KEY`），
  沒有字面金鑰、沒有 `<YOUR_KEY>`、沒有 `eval`、沒有刪檔命令，三個會連網的客戶端都帶了 `timeout`。

## 留給站主的事

1. **用語不一致（跨篇）。** 本篇寫「位置**偏誤**」「冗長**偏誤**」，
   站內 `ai-term-llm-as-a-judge` 寫「位置**偏差**」「冗長**偏差**」。
   BRIEF 的系列統一用語表沒有收這兩個詞，改哪一邊都會動到另一篇，本代理**沒有自行統一**。
2. **摘要與 description 的「倍增」偏強。** `n + m` 是線性相加（m 從 1 加到 3，呼叫次數 3 → 5，
   是 1.67 倍不是兩倍），只有加上交換順序那一列才真的把評分次數乘二。
   算式與每一個數字都對，是用字的取捨，是否改成「一路往上加」請站主決定。
3. **第二塊 code 無法獨立執行。** 它沿用第一塊的 `QUESTION`、`answer_a`、`answer_b`，
   單獨跑會 `NameError`。正文與程式註解都寫明了，且 BRIEF 允許「能單獨**看懂**」，
   本代理沒有改；若要改成可獨立執行需要加假資料，會多約 6 行。
4. **結尾兩個純 `link` 區塊等協調者跑 `pack_cli relink`**（自檢那個 `raw_internal_url` WARN 就是這個，
   是預期的）。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-cross-review-judge paragraphs 2772 code_blocks 3 sources 8
```

正文 2,772 字（改前 2,558），在 1,800–3,000 內；三塊 code；八條 sources。
唯一的 FAIL 沒有出現，WARN 是協調者 relink 前的預期狀態。
另外程式驗過：兩個 JSON 檔都是 LF、2 格縮排、不跳脫中文、檔尾一個換行，
且以 `json.dumps(indent=2, ensure_ascii=False)` 逐字節還原；
內容包與研究紀錄的 `title`、`sources`（順序與內容）、`diagram.caption`、
`code_samples` 的 `label` 與 `lines` 全部一致。

## 結論

**ok。**

改的 10 處裡只有第 1 處動到可執行的行為（多數決的平手處理），
而那一處是把程式改成**符合原本就寫在摘要、正文、FAQ 與圖解上的敘述**，
骨幹論述（rubric 怎麼寫、兩答一評、多評審投票、位置／冗長偏誤、n+2m 的算式）沒有改，
三個程式範例都沒有整塊換掉，事實改動不到十處，所以不需要第二輪。
需要協調者接手的只有 `pack_cli relink`，以及上面第 1、2 點兩個跨篇用字的決定。
