# 獨立查核：ai-workflow-structured-handoff

查核代理：未參與撰稿。查核日 **2026-09-19**。
文章的 `checked_on` 本來就是 **2026-09-18**、六條 source 與研究紀錄七處一致，
本輪重抓沒有因為頁面改了數字而更動任何數字（改掉的都是撰稿者的讀法），
依規格 **不改** `checked_on`；只有被我改過的第二個 code 區塊 `compiled_on` 改成今天。

查核方式：`sources[]` 六條全部以 `curl -sL -A "Mokaair-editorial"` 今天重抓並讀 body，
逐條把 title、description、正文每一句與子句、summary、表格每一格、兩個 caption、
圖解節點、callout、FAQ 每一題答句、兩個 `code` 區塊的每一個識別字對回原文。
研究紀錄的 `verbatim_quote` 用正規化後的**連續字串**比對（程式跑，不靠肉眼）。
**任何請求的 UA、標頭、查詢字串與表單都沒有放入 email 或任何個人資料。**
`sources[]` 以外只讀了兩個 Google 頁面**用來反證**（見下），沒有拿它們替文章補任何事實。

檢查的主張：**204 條**（正文 44 句／子句、摘要 6 句、表格 15 格、表格與圖解 caption 各 1、
圖解 5 組節點、FAQ 6 題答句、callout 3 項、步驟列 4 項、title／description／hero_label 各 1，
外加兩個程式區塊去重後的 **116 個識別字**），加上研究紀錄的引文。
**改了 14 條（19 個編輯點）**，研究紀錄的 `verified_facts` 從 21 條補到 32 條，
另有 4 件留給站主。

## 重抓結果：六條 sources 今天都讀到正文

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| `platform.openai.com/docs/guides/structured-outputs` | 200 | 3,253,904 | **是**。`<h1>` 為 `Structured model outputs`，`Supported models`／`Supported schemas`／`How to use Structured Outputs with response_format`／`… with text.format`／`JSON mode` 各節俱全；`response_format` 127 次、`json_schema` 207 次、`additionalProperties` 435 次 |
| `platform.claude.com/docs/en/build-with-claude/structured-outputs` | 200 | 1,629,202 | **是**。`Migrating from beta?` 提示框、`JSON outputs`／`Strict tool use`／`JSON Schema limitations`／`Schema complexity limits`／頁尾 `Compatibility` 表都在 |
| `ai.google.dev/gemini-api/docs/structured-output` | 200 | 330,012 | **是**。Recipe／Classification 等五組範例（Python／JavaScript／Java／REST）與 `Structured outputs with tools` 都在 |
| `python-jsonschema.readthedocs.io/` | 200 | 35,895 | **是**。標題 `jsonschema 4.26.0 documentation`，Features／Installation／Extras 俱全 |
| `python-jsonschema.readthedocs.io/en/stable/validate/` | 200 | 113,244 | **是**。The Basics／The Validator Protocol／Type Checking／Versioned Validators／Validating Formats 俱全 |
| `python-jsonschema.readthedocs.io/en/stable/errors/` | 200 | 82,169 | **是**。`ValidationError.message` 等屬性清單俱全 |

研究紀錄原有 **21 條 `verbatim_quote` 全部通過**連續字串比對（0 條落空），
補進去的 11 條也各自逐字驗過。

## 程式範例重驗

| # | label | 語言 | 行數 | `python3 -m py_compile` | 比對過的簽名／端點／標頭 |
| --- | --- | --- | --- | --- | --- |
| 1 | `schema_and_upstream.py（需要標準庫 urllib）` | python | 49（未改） | **通過** | 端點 `https://api.openai.com/v1/chat/completions`、標頭 `Authorization: Bearer $OPENAI_API_KEY` 與 `Content-Type: application/json`、`response_format: {type: json_schema, json_schema: {name, schema, strict}}`、回應路徑 `choices[0].message.content`、`required` 列滿、`additionalProperties: false`、`format: "date"`、`["string","null"]` 可選欄位寫法 — 全部在 <https://platform.openai.com/docs/guides/structured-outputs> 上逐字找得到；`urllib.request.Request`／`urlopen(..., timeout=30)` 為標準庫 |
| 2 | `validate_and_handoff.py（需要 jsonschema）` | python | 45 → **47**（本輪改） | **通過** | `Draft202012Validator(schema)` 建構子、`iter_errors(instance)`、`sorted(..., key=str)`（與官方範例同一種寫法）、`error.message`、`jsonschema.exceptions.ValidationError`／`SchemaError` — 對 <https://python-jsonschema.readthedocs.io/en/stable/validate/> 與 <https://python-jsonschema.readthedocs.io/en/stable/errors/>；模型 id 對 `models-seen.json` 與 OpenAI 頁 |

venv 與系統 python 都沒有 `jsonschema` 套件（指派已說明），
所以驗證行為只做 `py_compile` 加上對官方文件比對函式簽名，**沒有實際執行驗證迴圈**。
金鑰只從 `os.environ["OPENAI_API_KEY"]` 讀、沒有字面金鑰或 `<YOUR_KEY>`、
沒有 `eval` 或刪檔命令、網路呼叫都帶 `timeout=30`、範例沒有捏造輸出——這幾項本來就合格。

## 改掉的 14 條

### 協調者點名的五件事

1. **Anthropic 的支援模型清單被改寫成 API id（最重的一處）。**
   原文頁尾的 `Compatibility` 表寫的是
   「`Supported models Fable 5 and 5.1 Mythos 5, 5.1, and Preview Opus 4.5, 4.6, 4.7, 4.8, and 5 Sonnet 4.5, 4.6, and 5 Haiku 4.5`」——
   **列的是系列名，不是 API id**。以字串比對，整頁
   `claude-sonnet-5` **0 次**、`claude-haiku-4-5-20251001` **0 次**，
   只有範例裡的 `model = "claude-opus-5"` 出現 **8 次**。
   草稿卻寫「Anthropic 文件列出的名單包含 claude-sonnet-5、claude-opus-5 與
   claude-haiku-4-5-20251001 這幾個目前看得到的版本」——三個 id 有兩個是從別的頁面（模型總覽）
   搬來的，而且整整漏掉 Fable 與 Mythos 兩個系列。
   正文已改成照原文列系列名並註明「列的是系列名而不是 API id」，
   表格「支援模型」欄同步改；研究紀錄那條事實的 `fact` 也改寫，
   另加一條 `must_not_write` 擋住翻譯階段再犯。
2. **Anthropic 的 beta 遷移敘述漏掉原文自己的但書。**
   原文：「`The output_format parameter has moved to output_config.format , and beta headers are
   no longer required. The API continues to accept the old beta header
   ( structured-outputs-2025-11-13 ) and the output_format request field for a transition period,
   but the Python SDK (v1.0 and later) does not accept output_format={...} on
   client.beta.messages.create() or count_tokens() and raises a TypeError`」。
   草稿只寫到「API 暫時還接受舊寫法過渡」就停了，**`but` 以後整段不見**。
   已補上「Python SDK 1.0 之後在 `client.beta.messages.create()` 與 `count_tokens()` 上
   不接受舊的 `output_format` 寫法，會丟 `TypeError`」。
   另外，表格「現況」欄原本寫「**已從 beta 轉為正式功能**」——頁面沒有 GA／generally available
   這種字眼，那是從「不需要 beta 標頭」推出來的，已改成文件真正寫的
   「output_format 已移到 output_config.format、beta 標頭不再必要；舊標頭與舊欄位過渡期仍接受」。
3. **Google 的端點與欄位：草稿是對的，不用改參數。**
   今天的頁面確認：`client . interactions . create (` 就是頁面示範的呼叫方式，
   `response_format` 的三個鍵是
   「`To generate a JSON object, configure response_format with an object (or an array containing
   an object) of type text and set its mime_type to application/json`」，
   REST 範例五處都是
   「`curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions"`」
   配 `x-goog-api-key` 標頭。
   **這一頁 `generateContent` 0 次、`response_schema` 0 次、`responseSchema` 0 次、
   `response_json_schema` 0 次、`response_mime_type` 0 次**——沒有第二種寫法可以並列，
   所以不需要標「主推／舊法」。
   為了反證這不是孤例，另外讀了兩個**不在 `sources[]`、也沒有寫進文章**的頁面：
   `ai.google.dev/gemini-api/docs/text-generation`（HTTP 200，`v1beta/interactions` 12 次、
   `generateContent` **0 次**）與 `ai.google.dev/gemini-api/docs/text`（**HTTP 404**，該路徑已不存在）。
   改掉的是**寫法的範圍**：草稿的「目前的 Gemini API 文件是以 Interactions API 為準」是全站級斷言，
   已改成可查證的「這一頁目前示範的呼叫方式只有 Interactions API 一種」；
   「REST 端點目前仍然掛在 v1beta 這個路徑下」也寫清楚成「v1beta 路徑底下的 `/interactions`」。
   表格「支援模型」欄的「gemini-3.8-flash 等 Gemini 系列」改成「頁面範例用 gemini-3.8-flash」
   （搭配工具那個 Preview 範例用的是另一個 Gemini 3 預覽版 id，不在白名單，依研究紀錄不點名）。
4. **OpenAI 的 5000／10 這組上限逐字正確，不用改。**
   原文：「`A schema may have up to 5000 object properties total, with up to 10 levels of nesting.`」
   與研究紀錄第 6 條一字不差。這組數字**沒有寫進文章**（研究紀錄 `unverified_or_excluded`
   已說明只留給讀者自己查），所以正文不必動。
   同頁另外兩組上限（`1000 enum values`、`15,000 characters`、`120,000 characters`）也一併核對過，
   確認撰稿者引的那一組沒有張冠李戴。
5. **`gpt-4o`：正文屬歸因引述，保留；程式用的本來就是現行 id。**
   兩個 code 區塊用的是 `gpt-6-astra`（在白名單，而且該頁自己寫
   「`For new projects, start with gpt-6-astra`」），**沒有**在程式裡用 `gpt-4o`，協調者擔心的情況不存在。
   正文那句是歸因引述，但原文是
   「`Structured Outputs is available in our latest large language models , starting with GPT-4o.`」——
   草稿寫成「這項功能**從 GPT-4o 開始支援**」、表格寫成「**GPT-4o 以後的模型**」，
   兩處都把「我們較新的大型語言模型」這個限定拿掉、變成一條時間線上的全稱。
   已改成「從 GPT-4o 起的**較新模型**支援，**沒有逐一列出型號**」，表格同步。
   `models-seen.json` 的 `gpt-4o` 條目依規格不刪；我今天也重新確認它的 `verbatim`
   在該頁上逐字找得到。

### 協調者點名的第 6 件：端點、標頭、欄位逐一比對

6. **兩個 code 區塊的每一個對外識別字都找得到出處，沒有改任何參數名。**
   逐一命中的有：端點 `https://api.openai.com/v1/chat/completions`；
   `-H "Authorization: Bearer $OPENAI_API_KEY"`；`"Content-Type: application/json"`；
   請求欄位 `model`／`messages`（`role`、`content`）／
   `response_format.type = "json_schema"` 與 `json_schema.{name, schema, strict}`；
   回應路徑 `choices[0].message.content`；
   schema 這邊 `All fields must be required`、
   `additionalProperties: false must always be set in objects`、
   字串 `format` 清單含 `date`
   （`Predefined formats for strings. Currently supported: date-time time date duration email
   hostname ipv4 ipv6 uuid`）、
   以及 `new_date` 用的 `["string","null"]` 寫法
   （`it is possible to emulate an optional parameter by using a union type with null`）。
   `jsonschema` 這邊 `Draft202012Validator`、`iter_errors`、`ValidationError`、`SchemaError`、
   `error.message` 全部對到官方文件，連 `sorted(..., key=str)` 都和官方範例同款。
   **沒有找不到出處的參數，因此沒有刪改任何一個。**
7. **但程式和本篇主旨打架的地方改了一處：下游呼叫傳的是 `UPSTREAM_MODEL`。**
   `forward_to_downstream()` 的 docstring 寫「下游模型只讀 validated 這個字典」，
   實際卻把 `UPSTREAM_MODEL` 傳進 `call_model`——在一篇講「交接給下游模型」的文章裡，
   這會讓讀者以為兩端是同一個角色。
   已新增 `DOWNSTREAM_MODEL` 常數（值一樣是 `gpt-6-astra`）與一行說明
   「這個範例上下游都接 OpenAI；換成別家只要改 call_model 裡的端點與標頭」，
   下游呼叫改用它。**沒有**換成別的 id：結構化輸出頁只寫「從 GPT-4o 起的較新模型」、
   沒有逐一列型號，我不在沒有頁面依據的情況下宣稱 `gpt-5.6-terra` 或 `gpt-5.6-luna` 支援這個功能。
   區塊從 45 行變成 47 行，重新 `py_compile` 通過，研究紀錄 `code_samples` 的 `lines`
   與 `compiled_on` 同步。

### 站內分工：一個被發明出來的 CLI 旗標

8. **草稿說 `claude-code-structured-cli-pipeline`「把 `--json-schema` 接到自己寫的驗證與重試邏輯」，
   那一篇根本沒有這個旗標。**
   打開該內容包字串比對：`--json-schema` **0 次**、`json-schema` **0 次**、
   `--output-format` **0 次**、`jsonschema` **0 次**。
   它實際的做法是 `automation/schema.json` 描述欄位，加上 `automation/result.mjs`
   自己解析 `structured_output` 這層外殼（`structured_output` 出現 6 次）。
   「重試邏輯」也不成立——那一篇自己寫「本篇只摘要假資料，因此**重試比較單純**」，
   並把重跑與去重整個推給 `claude-code-scheduled-workflow-reliability`。
   這是**必連不可重寫的三篇之一**，寫錯就等於和它矛盾。
   已改成「把 `claude -p` 輸出的 JSON 接進自己寫的驗證邏輯，再決定要不要往下一步送」，
   並加一條 `must_not_write`。
   （另外兩篇的一句話帶過都查過沒問題：`gemini-api-files-structured-output` 確實用
   `interactions` ＋ `response_format` 這同一套 Google 功能處理 PDF，
   而且確實強調「JSON 合法」與「內容真的來自檔案」是兩件事；
   `ai-term-tool-calling` 的定位也沒有被重講。三篇的 zh-TW title 都逐字抄對。）

### 其餘（都在「安靜強化來源」與「限定詞被刪」兩類）

9. **「理論上不是保證」後面舉的例子，來源頁沒有寫。**
   草稿寫「網路逾時、模型中斷、或者剛好卡在某些例外狀況」。
   OpenAI 自己在 `Step 3: Handle edge cases` 列的是另外兩種：
   「`This can happen in the case of a refusal, if the model refuses to answer for safety reasons,
   or if for example you reach a max tokens limit and the response is incomplete.`」，
   而且拒答那條還補了
   「`Since a refusal does not necessarily follow the schema you have supplied in response_format ,
   the API response will include a new field called refusal`」。
   已照原文改寫成這兩種，並明寫是 OpenAI 文件列的。
10. **表格 OpenAI「現況」欄的「正式功能」是推論。**
    以字串比對，該頁 `preview`／`Preview` **各 0 次**、`generally available` **0 次**；
    `beta` 只有 2 次、兩次都在 `client.beta.chat.completions.stream(` 這個串流 helper 上，
    `Beta` 1 次是側邊導覽的 `GitLab (Beta)`——**沒有一次**與結構化輸出的狀態有關。「沒有標 beta」不等於文件說了「正式」，
    已改成可查證的「頁面沒有標 beta 或預覽」。
11. **「比較新的 Responses API」——來源頁沒有說哪個比較新。**
    該頁把 Chat Completions 與 Responses 並列成兩個模式切換，
    只寫「`Both Structured Outputs and JSON mode are supported in the Responses API,
    Chat Completions API, Assistants API, Fine-tuning API and Batch API.`」，
    沒有任何一句說 Chat Completions 比較舊。正文與表格都拿掉了「比較新的」。
12. **jsonschema 那句把「多半會偏好」寫成「官方文件建議」，還漏掉前提。**
    原文：「`If you know you have a valid schema already, especially if you intend to validate
    multiple instances with the same schema, you likely would prefer using the`
    jsonschema.protocols.Validator.validate `method directly on a specific validator`」。
    草稿只留「同一份 schema 如果要重複驗證很多筆資料，官方文件**建議**改用……」，
    **「已經確定 schema 本身合法」這個前提整個不見**。已照原文補回並改掉語氣。
13. **範例 schema 裡的 `format: "date"` 其實不會被驗——這件事漏寫了。**
    同一頁的 `Validating Formats` 寫
    「`By default, as per the specification, no validation is enforced. Optionally however,
    validation can be enabled by hooking a format-checking object into a Validator`」。
    文章附的 schema 有 `"format": "date"`，讀者很容易以為 `iter_errors()` 會擋掉亂寫的日期。
    已在該段補一句：format 關鍵字預設不做驗證，要把 `format_checker` 掛到驗證器上才生效，
    所以 `new_date` 標了 `format` 也不會真的被驗。
14. **兩處語氣過強。** FAQ 第 1 題「才能確保下游**一定**拿得到固定形狀的資料」——
    同一頁明寫拒答與截斷仍可能不照 schema，已改成「才能在資料送進下游之前先確認它的形狀」；
    導言「多模型工作流**最常**卡住的地方」是沒有來源也沒有實測的頻率宣稱，
    改成「很容易卡住的地方」。

## 查過而且正確的部分（沒有動）

- **OpenAI 的欄位位置全部吻合**：Chat Completions 的
  `response_format: { "type": "json_schema", "json_schema": { "name": …, "schema": …, "strict": true } }`、
  Responses API 的 `text: { format: { type: "json_schema", "strict": true, "schema": … } }`、
  以及 Python SDK 的 `client.responses.parse(model=…, input=…, text_format=CalendarEvent)`
  可以直接吃 Pydantic 類別——草稿這三點逐字對得上。
- **Anthropic 的欄位與 `strict` 的分工吻合**：
  `JSON outputs ( output_config.format )` 與 `Strict tool use ( strict: true )` 是頁面自己的分法，
  範例裡 `strict: True` 確實掛在 `tools` 的工具定義上，
  和「整段回覆是不是合法 JSON」是兩件事——草稿說「容易搞混」並沒有說錯。
- **Google 的 Preview 限定沒有被刪**：
  「`Preview: This feature is available only to Gemini 3 series models.`」
  這句只掛在 `Structured outputs with tools` 那一節，草稿寫的「搭配內建工具時」範圍正確，
  沒有把整個結構化輸出說成 Preview；內建工具清單（Google 搜尋、URL Context、程式碼執行、
  File Search、Function Calling）也對得上。
- **jsonschema 的行為描述吻合**：`validate()` 會先驗 schema 再比 instance
  （`validate() will first verify that the provided schema is itself valid`）、
  兩種例外的類別名、`iter_errors` 的
  `Lazily yield each of the validation errors in the given instance.`、
  `message` 的 `A human readable message explaining the error.`、
  首頁的 `Full support for Draft 2020-12 …` 與 `pip install jsonschema`，全部逐字命中。
- **模型 id 全部合規**：正文與程式出現的 `gpt-6-astra`、`claude-opus-5`、`gemini-3.8-flash`
  都在 `models-seen.json`，而且都能在對應來源頁上找到；
  自檢沒有對任何 id 發出 `models-seen.json has not recorded` 的警告。
- **界線檢查全部通過**：沒有購買、訂閱或投資建議；沒有推薦式比價；
  沒有速度或品質的排名（本站沒有實測，文章也沒有寫）；
  廠商宣稱都有「OpenAI 的文件寫」「Anthropic 的文件寫」「Google 的文件也提醒」這類歸因；
  beta／Preview／過渡期／`up to` 這些限定詞在修完之後都在；
  **只有一個 `callout`、沒有免責段落**；沒有寫「台灣可用」。
- **結構與連動**：兩個結尾 `link` 的 `text` 與 `url` 未更動，第二個逐字等於
  `gemini-api-files-structured-output` 的 zh-TW title；正文中間沒有多餘的 `link` 區塊；
  研究紀錄的 `title`、`sources`（順序與內容）、`diagram.caption` 與內容包一致；
  圖解五組節點沒有任何數字，不會與正文脫節。
- **`checked_on` 2026-09-18** 在內容包六條 source 與研究紀錄七處一致，未更動。

## 留給站主的事

1. **FAQ 第 3 題點名的《成本、品質、延遲：多模型流程怎麼取捨》還沒有內容包。**
   `ai-workflow-cost-quality-latency` 不在 `apps/api/app/guides/content/`。
   但這個標題和 `ai-workflow-basics`、`ai-workflow-split-tasks-across-models`、
   `ai-workflow-unified-api-layer`、`ai-workflow-model-routing-cascade`、
   `ai-workflow-cross-review-judge` 五篇用的完全一致
   （其中 `model-routing-cascade` 還把它寫成 `link` 區塊的 text），
   所以本代理**沒有動它**——那一篇定稿時若改標題，這六處要一起改。
2. **Anthropic 的相容性表沒有 API id 可寫。** Fable 與 Mythos 兩個系列在那一頁上
   完全沒有對應的 `claude-*` id，所以表格只能照抄系列名。
   若站主希望這一欄只列 API id，得另外把模型總覽頁加進 `sources[]`，那是換來源、不是改字。
3. **程式範例上下游都是 `gpt-6-astra`。** 讓下游改用便宜模型（例如 `gpt-5.6-luna`）
   在編輯上更能呼應「級聯」那一篇，但結構化輸出頁沒有逐一列型號，
   要換 id 就得先在模型頁上查到「支援結構化輸出」的字樣，那會動到 `sources[]`。
4. **兩個結尾連結仍是純 URL**（自檢的 `raw_internal_url` WARN）。
   依指派這是協調者 `pack_cli relink` 的工作，本代理沒有碰。

## `models-seen.json`

**沒有新增**。文章與程式用到的三個 id（`gpt-6-astra`、`claude-opus-5`、`gemini-3.8-flash`）
都已經在清單裡；我今天在三個來源頁上分別重新看到它們，但既有條目依規格不改。
撰稿者加的 `gpt-4o` 條目也重新驗過：它的 `verbatim`
（`Structured Outputs is available in our latest large language models , starting with GPT-4o`）
今天在該頁上仍逐字找得到，依「只增不刪」保留。

## 自檢

```
WARN - lint raw_internal_url: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
OK ai-workflow-structured-handoff paragraphs 2895 code_blocks 2 sources 6
```

## 結論

`needs_second_round`。骨幹論述（交接契約＝JSON Schema、驗證、重試、下游只吃驗證過欄位）
與兩個程式範例的架構都站得住，端點、標頭與參數名逐一查完**沒有一個是編出來的**；
但事實面改動超過十處，其中兩處是硬錯誤——
Anthropic 的支援模型清單被改寫成該頁上不存在的 API id，
以及必連文章 `claude-code-structured-cli-pipeline` 被安上不存在的 `--json-schema` 旗標。
建議第二輪特別重看 Anthropic 那一段（系列名 vs API id 的寫法讀起來仍偏技術），
以及新加的 `format` 但書是否和 callout 重複到需要合併。
