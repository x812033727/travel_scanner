# 查核紀錄 1：ai-term-structured-outputs

查核者：獨立查核（非撰稿者）。查核日：2026-10-03。
讀取方式：所有來源以 `curl -sSL` 加 User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 今天重新打開，HTML 轉純文字後逐段比對；沒有沿用撰稿者的 notes。七個來源全部 HTTP 200：
`json-schema.org/specification`、`json-schema.org/draft/2020-12/json-schema-core`、`json-schema.org/draft/2020-12/json-schema-validation`、`rfc-editor.org/rfc/rfc8259`（轉址到 `/info/rfc8259/`）、`developers.openai.com/api/docs/guides/structured-outputs`（`platform.openai.com/docs/guides/structured-outputs` 今天確實轉址到這裡）、`platform.claude.com/docs/en/build-with-claude/structured-outputs`、`ai.google.dev/gemini-api/docs/structured-output`（頁尾 Last updated 2026-09-23 UTC）。

## 修改

- 第 1 段「它保證的是形狀：欄位名稱、型別與可選值落在……之內」→「它管的是形狀：……」｜Anthropic 文件寫的是「在大多數情況下」保證符合 schema，並明列 enum／const 的大小寫不保證，開頭不宜把可選值寫成無條件保證（與下面 enum 大小寫一條是同一處事實修改）｜https://platform.claude.com/docs/en/build-with-claude/structured-outputs（Invalid outputs → Enum value casing）
- 表格「schema 限制／仍然沒保證的」：「欄位值是否正確、拒答與截斷時的輸出」→ 加「；Anthropic 另說 enum 大小寫不保證」；限制清單 Anthropic 條加「enum 值的大小寫不保證與 schema 一致」｜Anthropic 原文：「Structured outputs don't guarantee the capitalization of string enum and const values」，且回應正常結束、沒有錯誤也沒有特殊 stop_reason。撰稿者讀到但沒寫進正文，而本文示例正好用了 enum，屬於第二層保證的例外｜https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- 「前兩層是供應商功能的範圍，各家仍寫了例外」→「……OpenAI 與 Anthropic 的文件仍寫了例外」｜Google 那一頁沒有列出格式保證的例外（全文搜尋 refus、truncat、incomplete、finish、blocked、safety、stop 皆無命中），只提醒要驗證值；「各家」把 Google 也算進去了｜https://ai.google.dev/gemini-api/docs/structured-output
- 「本文示例只用五個關鍵字。」→「本文示例主要用下面五個關鍵字，另有 items（陣列元素的規則）與 description（欄位說明）。」｜示例 schema 實際還用了 items（missing 陣列）與 description（三個欄位），原句與示例不符｜本文示例 schema；關鍵字定義見 https://json-schema.org/draft/2020-12/json-schema-core 10.3.1.2
- 「欄位全列進 required 並關閉 additionalProperties，符合 OpenAI 與 Anthropic 的要求」→「欄位全列進 required 是 OpenAI 的要求，關閉 additionalProperties 則是 OpenAI 與 Anthropic 都要求的」｜「所有欄位都要 required」只有 OpenAI 要求（All fields must be required）；Anthropic 允許選填欄位（Property ordering、Optional parameters 限制都以有選填欄位為前提），它要求的是 additionalProperties 為 false｜https://developers.openai.com/api/docs/guides/structured-outputs ；https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- 「狀態為 incomplete 且原因是 max_output_tokens，表示 JSON 被截斷」→「截斷在 Responses API 是狀態為 incomplete 且原因是 max_output_tokens，在 Chat Completions 是 finish_reason 為 length」｜OpenAI 指南兩種 API 都有範例；incomplete／max_output_tokens 只屬於 Responses API，Chat Completions 的範例檢查 `finish_reason == "length"`，原句沒標 API 會讓 Chat Completions 使用者找錯欄位｜https://developers.openai.com/api/docs/guides/structured-outputs（Step 3: Handle edge cases、JSON mode 的 Handling edge cases）
- OpenAI 條「數字上下限列為支援」→「數字上下限列為支援（微調模型除外）」｜OpenAI 原文：「For fine-tuned models, we additionally do not support … For numbers: minimum, maximum, multipleOf」；後段「minimum 這個關鍵字 OpenAI 與 Google 列為支援」因此成立但需要這個但書｜https://developers.openai.com/api/docs/guides/structured-outputs（Some type-specific keywords are not yet supported）
- 「工具呼叫和結構化輸出差在用途……結構化輸出管模型最後回答的格式。」→「工具呼叫和回答格式差在用途……回答格式管模型最後回答的形狀。不過 OpenAI 與 Anthropic 的『結構化輸出』也涵蓋工具參數：開啟 strict 後，工具參數同樣依 schema 限制。」｜OpenAI 原文「Structured Outputs is available in two forms … function calling … json_schema response format」；Anthropic 原文「Structured outputs provide two complementary features: JSON outputs … Strict tool use」。兩家的「結構化輸出」都包含工具參數，原句把結構化輸出與工具呼叫寫成互斥；Google 的對照表才是「Structured Outputs vs Function Calling」二分｜https://developers.openai.com/api/docs/guides/structured-outputs ；https://platform.claude.com/docs/en/build-with-claude/structured-outputs ；https://ai.google.dev/gemini-api/docs/structured-output
- （措辭，不計）「規範有兩個預設容易誤會」→「三個預設」｜後面列了 required、additionalProperties、format 三項｜https://json-schema.org/draft/2020-12/json-schema-validation 6.5.3、第 7 節
- （措辭，不計）「輸入與任務無關時……建議提示詞寫明無法擷取時回傳空值」→「輸入與 schema 完全無關時……建議提示詞寫明輸入不適用時回傳空參數或固定句子」｜貼近原文「if the input is completely unrelated to the schema」「return empty parameters, or a specific sentence」｜https://developers.openai.com/api/docs/guides/structured-outputs（Tips and best practices）
- （措辭，不計）diagram-1.svg 例三副標「三層都過，才適合寫入」→「三層都過；缺的日期轉人工追問」，`<desc>` 同步加「缺的日期再轉人工追問」｜正文寫「欄位為 null 或 missing 非空，就轉人工追問」，圖說日期為 null 的輸出可直接寫入，前後矛盾。已重新渲染 1600×900，無壓線、超框、疊字｜本文第「缺值、拒答與截斷怎麼接」節

## 查過、沒問題的主要主張

- JSON Schema 2020-12 是 Internet-Draft（draft-bhutton-json-schema-01，Intended Status: Informational，Expires 18 December 2022），不是 RFC；正文、來源標題都沒有把它寫成正式標準。json-schema.org/specification 今天仍寫「The current version is 2020-12!」。
- 摘要「a JSON-based format for describing the structure of JSON data」支持「用來定義 JSON 資料的結構」。type 可為字串或陣列（6.1.1）、enum（6.1.2）、required 省略等同空陣列（6.5.3）、additionalProperties 省略等同空 schema（10.3.2.3）、format 預設是註解且斷言須預設關閉、Format-Assertion 為選用（7.1、7.2.1）、不認得的關鍵字當註解（4.3.1「Unknown keywords SHOULD be treated as annotations」）。
- RFC 8259 是 STD 90、Internet Standard，定義 JSON 語法。
- OpenAI：結構化輸出確保遵守所給 JSON Schema、不漏必填鍵不編無效 enum；JSON 模式只保證有效可解析、少數邊緣情況要自行偵測、不保證任何 schema、對話內容必須要求 JSON（否則可能無止境輸出空白，context 沒有「JSON」字串時 API 報錯）；refusal 欄位與安全拒答；全欄位 required、以含 null 的聯集模擬選填、additionalProperties 必須 false、allOf／not／if 不支援、strict 下用不支援的 schema 會收到錯誤；function calling 與 response_format／text.format 的分工；「Structured Outputs can still contain mistakes」。
- Anthropic：今天確實有獨立的 Structured outputs 文件（output_config.format 的 JSON outputs 與 strict tool use 兩項功能）；靠 constrained decoding、把 schema 編譯成文法；不用時「Even with careful prompting」仍可能語法錯誤、缺必填、型別不一致；不支援遞迴 schema、minimum／maximum／multipleOf、minLength／maxLength，用到會回 400；additionalProperties 只能 false；拒答 stop_reason refusal、狀態碼 200、輸出可能不符 schema；max_tokens 時可能不完整；與 citations 不相容（400）；JSON 輸出管「what Claude says」、strict tool use 管「how Claude calls your functions」，可同請求合用。
- Google：可設定回應遵守 JSON Schema、只支援子集；支援的 type（含 null 以型別陣列表示）與 title、description、properties、required、additionalProperties、enum、format、minimum、maximum、items、prefixItems、minItems、maxItems；最佳實務「always validate values」「schema-compliant but semantically incorrect outputs」；限制「Very large or deeply nested schemas may be rejected」；Structured Outputs＝格式化最終回答、Function Calling＝對話中採取行動。該頁確實沒有提到拒答或截斷訊號，正文「這一頁沒有說明」寫法正確，沒有推成「Gemini 沒有這類訊號」。
- 示例 schema（三個 type 陣列含 null 的欄位、enum 字串陣列、全 required、additionalProperties false）對照三家今天的支援清單都沒有落在不支援項目；正文與兩個程式區塊標籤都標明虛構、示例、未實測、沒送進 API，預期輸出寫成「預期」而非觀察。
- 系列規矩：沒有模型型號、價格、截止日、排行榜分數（「Claude」只出現在轉述 Anthropic 文件的句子裡，是產品名不是型號）；全文沒有用到推論／推理；沒有「用了就不會錯」式保證；台灣用語；恰好一個三欄表、6 個 H2、1 個 callout；指派的五個站內連結都在且只連指派 slug；圖上唯一數字是製圖年份 2026，正文有「2026 年 10 月 3 日」。
- 來源標題與頁面 `<title>` 相符；checked_on 2026-10-03 是今天實際打開的日期。

## 我懷疑但沒改的事

- `research.json` 的 `running_text_characters` 仍寫 2578；修改後 `_body_length` 是 2809（仍在 1,800–3,000，但高於簡報 2,100–2,500 的目標）。本次查核只准寫 pack.json、diagram-1.svg、verify-1.md，research.json 留給協調者更新。
- OpenAI 另列 content_filter（Responses 的 incomplete_details.reason、Chat Completions 的 finish_reason）也會讓 JSON 中途停止；Anthropic 另列「與 message prefilling 不相容」、要求 schema 欄位寫推理過程可能觸發 reasoning_extraction 拒答。正文只寫拒答與截斷，不算錯，沒有加。
- Google 這一頁今天有遞迴結構的範例，也有「結構化輸出搭配工具」（標示 Preview）的段落；正文沒有說 Google 不支援，沒動。
- Anthropic 對 type 陣列（如 `["string","null"]`）與選填參數有每個請求的總數上限，抓到的 HTML 文字裡表格數值沒有出現，示例只有三個這類欄位應無問題，但沒有實測確認。
- 2020-12 Internet-Draft 本身已於 2022-12-18 過期，json-schema.org 仍稱它為現行版本；正文寫「是 Internet-Draft，不是 RFC」正確，沒有加過期的說明。
- dry-run 仍只有 `no_summary` 警告（沒有 summary 區塊），簡報沒要求，沒加。

facts_changed: 7
