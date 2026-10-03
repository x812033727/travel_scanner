# 查核紀錄 2：ai-term-structured-outputs

查核者：第二輪獨立查核（不是撰稿者，也不是一審查核者）。查核日：2026-10-03。
讀取方式：七個來源今天以 `curl -sSL` 加 User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開，HTML 轉純文字後逐段比對，沒有沿用一審或撰稿者的摘錄。全部 HTTP 200：
`developers.openai.com/api/docs/guides/structured-outputs`（`platform.openai.com/docs/guides/structured-outputs` 仍轉址到這裡）、`platform.claude.com/docs/en/build-with-claude/structured-outputs`、`ai.google.dev/gemini-api/docs/structured-output`（頁尾 Last updated 2026-09-23 UTC）、`json-schema.org/specification`、`json-schema.org/draft/2020-12/json-schema-core`、`json-schema.org/draft/2020-12/json-schema-validation`、`rfc-editor.org/rfc/rfc8259`（轉址到 `/info/rfc8259/`）。

## 一審 7 處事實修改的複查（全部成立）

1. 開頭「它保證的是形狀」改成「它管的是形狀」：成立。Anthropic「Invalid outputs」寫「guarantee schema compliance in most cases」，並另列 enum／const 大小寫不保證。｜https://platform.claude.com/docs/en/build-with-claude/structured-outputs
2. 表格加「Anthropic 另說 enum 大小寫不保證」：成立。原文「Structured outputs don't guarantee the capitalization of string enum and const values」，回應正常結束、沒有錯誤也沒有特殊 stop_reason。這是第二層保證的例外，二審保留在表格，從限制清單刪掉重複的一句。｜同上
3. 「OpenAI 與 Anthropic 的文件仍寫了例外」（不寫「各家」）：成立。Google 頁面全文搜尋 refus、truncat、finish、incomplete、max_output、max_tokens、blocked、stop 都沒有命中（只有側欄導覽的 Safety 字樣）。｜https://ai.google.dev/gemini-api/docs/structured-output
4. 「另有 items 與 description」：成立，示例 schema 確實用到；items 定義見 Core 10.3.1.2，description 見 Google 支援清單。｜https://json-schema.org/draft/2020-12/json-schema-core
5. 「全列 required 是 OpenAI 的要求，關閉 additionalProperties 則是 OpenAI 與 Anthropic 都要求的」：成立。OpenAI「All fields must be required」「additionalProperties: false must always be set in objects」；Anthropic「required and additionalProperties (must be set to false for objects)」，且「Property ordering」以只列部分 required 的 schema 為例。｜https://developers.openai.com/api/docs/guides/structured-outputs ；https://platform.claude.com/docs/en/build-with-claude/structured-outputs
6. 截斷訊號分兩種 API：成立。今天頁面兩種範例都有：Responses 是 `response.status == "incomplete"` 且 `incomplete_details.reason == "max_output_tokens"`，Chat Completions 是 `finish_reason == "length"`。二審為可讀性把欄位名整句刪出正文（見下），不是推翻這一處。｜https://developers.openai.com/api/docs/guides/structured-outputs
7. 「數字上下限列為支援（微調模型除外）」：成立。原文「For fine-tuned models, we additionally do not support … For numbers: minimum, maximum, multipleOf」。二審刪掉 OpenAI 的數字上下限整段，連帶把下一段改成不提 OpenAI，避免留下少了但書的「OpenAI 支援 minimum」。｜同上
8. 「OpenAI 與 Anthropic 的『結構化輸出』也涵蓋工具參數」：成立。OpenAI「Structured Outputs is available in two forms … When using function calling / When using a json_schema response format」；Anthropic「JSON outputs (output_config.format) … Strict tool use (strict: true): Guarantee schema validation on tool names and inputs」。｜同上兩頁

（一審的 facts_changed 是 7，列了 8 條事實修改，第 1、2 條算同一處。三處措辭修改也看過，與原文相符。）

## 修改（全部是可讀性刪減或措辭，不計事實）

- （刪減）第一節「第二種是 JSON 模式……但不保證符合任何特定 schema，且對話內容必須要求輸出 JSON」→ 刪掉「且對話內容必須要求輸出 JSON」｜OpenAI 的使用細節，不影響讀者理解三種做法的差別；保證範圍沒變｜https://developers.openai.com/api/docs/guides/structured-outputs（JSON mode → Important notes）
- （措辭）「2020-12 版是 Internet-Draft，不是 RFC，json-schema.org 今天仍標示它為現行版本」→「json-schema.org 標示的現行版本 2020-12 以 Internet-Draft 形式發布，不是 RFC」｜一審留下的疑問：這份草案首部寫 Expires 18 December 2022。改成「以⋯⋯形式發布」不暗示它仍是有效草案，也就不必再加到期說明｜https://json-schema.org/draft/2020-12/json-schema-core ；https://json-schema.org/specification
- （措辭）「欄位全列進 required 是 OpenAI 的要求，關閉 additionalProperties 則是 OpenAI 與 Anthropic 都要求的」→「欄位全列進 required（OpenAI 的要求），並關閉 additionalProperties（OpenAI 與 Anthropic 都要求）」｜縮短，歸屬不變｜同一審第 5 條
- （措辭）「建議提示詞寫明輸入不適用時回傳空參數或固定句子」→「建議提示詞寫明這時回傳空參數或固定句子」｜縮短，前半句已說明「輸入與 schema 完全無關時」｜https://developers.openai.com/api/docs/guides/structured-outputs（Tips and best practices）
- （刪減）「結束訊號：OpenAI 的回應可能帶 refusal 內容……截斷在 Responses API 是狀態為 incomplete 且原因是 max_output_tokens，在 Chat Completions 是 finish_reason 為 length。Anthropic 對應的是 stop_reason 為 refusal 或 max_tokens，拒答時仍回 200 狀態碼。這兩種都不該直接解析。」→「停止原因：模型可能因安全理由拒答，或寫到長度上限被截斷。OpenAI 與 Anthropic 都會在回應裡標出這類情況，Anthropic 拒答時還照樣回 200 成功狀態碼，所以不能只看請求有沒有成功。帶著這類訊號的輸出不該直接解析。」｜五個欄位名是開發細節，一般讀者要懂的是「先看停止原因、拒答不是錯誤碼」；欄位名留在實作篇 ai-workflow-structured-handoff 與 notes.md。「可能因⋯⋯或⋯⋯」與「這類訊號」不是窮舉，所以不必另提 OpenAI 的 content_filter｜https://developers.openai.com/api/docs/guides/structured-outputs（Refusals with Structured Outputs、Step 3: Handle edge cases）；https://platform.claude.com/docs/en/build-with-claude/structured-outputs（Invalid outputs）
- （措辭）「先看結束訊號」→「先看停止原因」（該節導言與清單首項）｜與 diagram-1.svg 底部「先看停止原因」及圖片 alt 用同一個詞｜本文圖解
- （刪減）限制清單 OpenAI 條刪「數字上下限列為支援（微調模型除外）」；Anthropic 條刪「enum 值的大小寫不保證與 schema 一致」（表格已有）與「啟用引用（citations）功能時不能同時用 JSON 輸出」，加「這類數值與長度限制」說明那四個關鍵字是什麼；Google 條刪關鍵字清單「enum、format、minimum、maximum、items 等」，「這一頁沒有說明拒答或截斷的訊號」縮成「這一頁沒寫拒答或截斷的訊號」｜各家細節與概念無關；保留讀者需要的三點：都只支援子集、各家不同、Google 該頁沒寫拒答訊號（目錄 must_cover 要求寫拒答訊號）｜三家頁面「Supported schemas」「JSON Schema limitations」「Feature compatibility」「JSON schema support」
- （措辭）「minimum 這個關鍵字，OpenAI 與 Google 列為支援，Anthropic 不支援」→「同一個 minimum（數值下限），Google 列為支援，Anthropic 的 API 不支援」｜OpenAI 條刪掉後，若照舊寫「OpenAI 列為支援」會少了微調模型的但書，所以不提 OpenAI；加「的 API」與限制清單一致（Anthropic 的 SDK 輔助函式會把這類限制移進欄位說明並在本地驗證）｜https://platform.claude.com/docs/en/build-with-claude/structured-outputs（How SDK transformation works、Not supported）；https://ai.google.dev/gemini-api/docs/structured-output
- （刪減）分工段刪「Anthropic 的文件說兩者可同請求合用：strict tool use 管 Claude 怎麼呼叫函式，JSON 輸出管 Claude 說什麼。」，前句改成「OpenAI 與 Anthropic 的『結構化輸出』兩邊都涵蓋：開啟 strict 後，工具參數同樣依 schema 限制」｜同一段已說明工具呼叫與回答格式的分工，這句是重複的 Anthropic 細節｜https://platform.claude.com/docs/en/build-with-claude/structured-outputs（開頭兩項功能）

正文 `_body_length`：2809 → 2543（扣掉連結文字 2454）。結構不變：6 個 H2、恰好 1 個三欄表、1 個 callout、指派的五個站內連結都在且只連指派 slug。核心兩點都保留：三層保證（第 5 段與圖解）、格式合法不等於內容正確（開頭、示例日期段、callout）。diagram-1.svg 沒改。

## 查過、沒問題的主要主張

隨機抽樣：把一審沒改的其餘主張列成 27 條，以固定種子 `2026-10-03 ai-term-structured-outputs verify-2` 抽 9 條（三分之一），結果如下，全部對到今天的原文：

- 表格列一（只靠提示詞可能語法錯誤、缺必填、型別不一致）：Anthropic「Even with careful prompting, you may encounter: Parsing errors from invalid JSON syntax / Missing required fields / Inconsistent data types」。
- 表格列二（JSON 模式少數邊緣情況要自行偵測）：OpenAI「ensured to be valid JSON, except for in some edge cases that you should detect and handle appropriately」。
- required 省略等於沒有必填、additionalProperties 省略時額外欄位通過：Validation 6.5.3「Omitting this keyword has the same behavior as an empty array」；Core 10.3.2.3「Omitting this keyword has the same assertion behavior as an empty schema」。
- format 預設只是註解：Validation 7.2.1，format 收集為 annotation，當成斷言的驗證「MUST be disabled by default」。正文「驗證程式不一定檢查」比原文寬鬆，但沒有錯。
- OpenAI 與 Anthropic 都在回應標出拒答與截斷：OpenAI 的 refusal 欄位與 incomplete／length；Anthropic 的 stop_reason refusal／max_tokens，拒答「You'll receive a 200 status code」。
- 三家都只支援子集：OpenAI「supports a subset of the JSON Schema language」、Google「supports a subset of the JSON Schema specification」、Anthropic「standard JSON Schema with some limitations」。
- 規範讓不認得的關鍵字通過：Core 4.3.1「Unknown keywords SHOULD be treated as annotations」。
- minimum：Google 支援清單有「minimum: The minimum inclusive value」；Anthropic「Not supported: Numerical constraints (such as minimum, maximum, multipleOf)」。
- 三家都把工具呼叫與回答格式分開：OpenAI「function calling vs response_format」、Anthropic「JSON outputs control Claude's response format (what Claude says) / Strict tool use validates tool parameters (how Claude calls your functions)」、Google「Structured outputs versus function calling」表。

抽樣以外順手對過、也成立的：JSON 模式「only that it is valid and parses without errors」支持「保證輸出可解析」；Anthropic「constrained decoding」與「compiling your JSON schemas into a grammar」；OpenAI「all fields must be required」與「emulate an optional parameter by using a union type with null」（範例就是 `["string", "null"]`）、「Composition: allOf, not, … if, then, else」不支援、strict 下用不支援的 schema「you will receive an error」；Anthropic 不支援遞迴 schema、minLength、maxLength，用到回 400；Google「Very large or deeply nested schemas may be rejected」「always validate values」「schema-compliant but semantically incorrect outputs」，type 陣列含 null 的寫法；OpenAI「Structured Outputs can still contain mistakes」與「completely unrelated to the schema … return empty parameters, or a specific sentence」；Core 摘要「a JSON-based format for describing the structure of JSON data」，首部 Internet-Draft、draft-bhutton-json-schema-01、Informational；json-schema.org「The current version is 2020-12!」；RFC 8259 是 STD 90、Internet Standard。

示例 schema 對三家今天的清單：三個 type 陣列含 null（Anthropic 每請求聯集型別參數上限 16，今天表格數值有出現）、0 個選填參數、items 內字串 enum、additionalProperties false，都沒有落在不支援項目。

系列規矩：沒有型號、價格、截止日、排行榜分數（OpenAI 與 Anthropic 頁面今天都有型號，正文沒有抄）；沒有用到推論／推理；沒有「用了就不會錯」式保證；示例與預期輸出都標明虛構、未實測；台灣用語。diagram-1.svg 渲染到 `/tmp/ai-term-structured-outputs-d1.png`，1600×900，三個箭頭分別落在第一層、第二層、第三層，沒有壓線、超框、疊字；圖上唯一數字是製圖年份 2026，正文有「2026 年 10 月 3 日」。

dry-run：`exit 0`，「dry run: nothing written」，只有 `no_summary` 警告。

`notes.md` 與 `research.json` 已同步：`running_text_characters` 改成 2543；各來源的 claims 改成正文現在實際用到的主張（加 OpenAI 兩種形式、Anthropic 的 additionalProperties 與 enum 大小寫，刪 citations、合用、OpenAI 數字上下限）；notes.md 標出哪些今天讀到但二審刪出正文。

## 我懷疑但沒改的事

- 一審留下的三個疑問都決定不加：OpenAI 的 content_filter 停止，正文改寫後「可能因安全理由拒答，或寫到長度上限被截斷」與「這類訊號」不是窮舉，不寫也不失準；Anthropic 與 message prefilling 不相容、schema 欄位要求寫推理過程可能觸發 reasoning_extraction 拒答，示例沒有用到預填也沒有推理欄位，正文也沒宣稱相容；2020-12 草案已過期，正文改成「以 Internet-Draft 形式發布」，不暗示它仍有效，json-schema.org 今天仍稱它為現行版本。
- 「拒答是輸出離開了 schema」比兩家原文的「may not match your schema」「does not necessarily follow the schema」肯定一點；這句講的是處理路徑要分開，沒改。
- H2「三家文件今天列出的限制」的「今天」，上線後讀起來會模糊；段落第一句寫了 2026 年 10 月 3 日，標題沒動。
- Google 頁面有「Structured outputs with tools」（標示 Preview）與遞迴結構範例；正文沒寫 Google 不支援這兩項，沒動。
- dry-run 仍有 `no_summary` 警告，簡報沒要求 summary 區塊。

facts_changed: 0
