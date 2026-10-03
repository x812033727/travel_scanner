# 查證與編輯紀錄：ai-term-structured-outputs

格式：主張｜來源網址｜查證日｜讀取方式。查證日一律 2026-10-03（實際打開頁面的日期）。
讀取方式：`curl -sSL` 加 User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，狀態碼 200，HTML 轉純文字後閱讀；沒有用 Wayback。

## OpenAI（https://developers.openai.com/api/docs/guides/structured-outputs）

結構化輸出確保輸出遵守所提供的 JSON Schema，不會漏掉必填鍵或編出無效的列舉值｜https://developers.openai.com/api/docs/guides/structured-outputs｜2026-10-03｜curl -sSL；原網址 platform.openai.com/docs/guides/structured-outputs 轉址到此
JSON 模式保證輸出是有效 JSON（少數邊緣情況要自行偵測），不保證符合任何特定 schema｜同上，「JSON mode」一節｜2026-10-03｜同上
使用 JSON 模式時對話內容必須明確要求輸出 JSON，否則可能無止境產生空白，且上下文沒有「JSON」字串時 API 會報錯（二審為可讀性刪出正文）｜同上，「JSON mode」Important notes｜2026-10-03｜同上
拒答時回應帶 refusal 欄位，不一定符合 schema；正文只寫「OpenAI 與 Anthropic 都會在回應裡標出」拒答與截斷，不列欄位名｜同上，「Refusals with Structured Outputs」｜2026-10-03｜同上
截斷：Responses API 的 status 為 incomplete 且 incomplete_details.reason 為 max_output_tokens；Chat Completions 的 finish_reason 為 length（欄位名二審後不寫進正文）｜同上，「Step 3: Handle edge cases」與 JSON mode「Handling edge cases」範例程式｜2026-10-03｜同上
輸入與 schema 完全無關時，模型仍會嘗試符合 schema，可能產生幻覺；建議提示詞說明輸入不適用時回傳空參數（empty parameters）或固定句子｜同上，「Tips and best practices」｜2026-10-03｜同上
支援的是 JSON Schema 子集：所有欄位必須 required，選填用含 null 的聯集型別模擬；物件必須 additionalProperties 為 false；pattern、format、數字上下限（minimum、maximum 等）列為支援，但微調模型不支援（二審後正文不再寫 OpenAI 的數字上下限）；allOf、not、if 等組合關鍵字不支援；strict 下用到不支援的 schema 會收到錯誤｜同上，「Supported schemas」｜2026-10-03｜同上
結構化輸出有兩種形式：function calling（strict: true 時工具參數依 schema）與 json_schema response format；連接工具與功能用 function calling，結構化回答使用者用 response_format／text.format｜同上，「When to use Structured Outputs via function calling vs via response_format」｜2026-10-03｜同上

## Anthropic（https://platform.claude.com/docs/en/build-with-claude/structured-outputs）

做法是把 JSON schema 編譯成文法來約束輸出（constrained decoding / constrained sampling）｜https://platform.claude.com/docs/en/build-with-claude/structured-outputs｜2026-10-03｜curl -sSL
未使用結構化輸出時，即使小心撰寫提示詞，仍可能遇到 JSON 語法錯誤、缺必填欄位、資料型別不一致｜同上，「Why use structured outputs」｜2026-10-03｜同上
不支援遞迴 schema，也不支援 minimum、maximum、minLength、maxLength 等限制；用到不支援功能會回 400 錯誤（正文只寫「不支援」，未寫 400）｜同上，「JSON Schema limitations」｜2026-10-03｜同上
物件的 additionalProperties 必須設為 false；required 可以只列部分欄位（「Property ordering」以有選填欄位為例），所以「全欄位 required」只歸給 OpenAI｜同上，「Supported features」「Property ordering」｜2026-10-03｜同上
拒答時 stop_reason 為 refusal、狀態碼 200、輸出可能不符 schema；達 max_tokens 時輸出可能不完整｜同上，「Invalid outputs」｜2026-10-03｜同上
SDK 輔助函式會拿掉 API 不支援的限制、有驗證功能的版本在本地依原始 schema 驗證（這一條今天讀到、最後沒寫進正文）｜同上，「How SDK transformation works」｜2026-10-03｜同上
啟用 citations 時不能同時使用 output_config.format（回 400）；也與 message prefilling 不相容（兩條都是今天讀到、二審後不寫進正文）｜同上，「Feature compatibility」｜2026-10-03｜同上
結構化輸出包含 JSON outputs 與 strict tool use 兩項功能：JSON 輸出管 Claude 說什麼，strict tool use 讓工具名稱與參數依 schema；兩者可同請求合用（合用一句二審後刪出正文）｜同上，開頭與「Using both features together」｜2026-10-03｜同上
string enum 與 const 值的大小寫不保證與 schema 一致，回應正常結束、沒有特殊 stop_reason（寫在正文表格）｜同上，「Invalid outputs」→「Enum value casing」｜2026-10-03｜同上
未寫進正文但讀到：schema 複雜度上限（含 type 陣列的參數有每請求總數上限，示例只有三個）、文法快取 24 小時、要求 schema 欄位寫推理過程可能觸發 reasoning_extraction 拒答、支援模型清單（依指示不列模型型號）｜同上｜2026-10-03｜同上

## Google Gemini API（https://ai.google.dev/gemini-api/docs/structured-output）

可設定模型產生符合所提供 JSON Schema 的回應；支援的是 JSON Schema 規範的子集｜https://ai.google.dev/gemini-api/docs/structured-output｜2026-10-03｜curl -sSL（頁尾標示 Last updated 2026-09-23 UTC）
文件列出的關鍵字：type（string、number、integer、boolean、object、array、null）、title、description、properties、required、additionalProperties、enum、format、minimum、maximum、items、prefixItems、minItems、maxItems｜同上，「JSON schema support」｜2026-10-03｜同上
最佳實務：輸出語法正確，但一律在應用程式端驗證值；要處理符合 schema 卻語意不正確的輸出｜同上，「Best practices」｜2026-10-03｜同上
限制：只支援子集；過大或巢狀過深的 schema 可能被拒絕｜同上，「Limitations」｜2026-10-03｜同上
這一頁沒有說明拒答或截斷的訊號（頁面文字搜尋 refus、truncat、incomplete、finish、blocked 皆無命中；正文只寫「這一頁沒寫」，沒有說 Gemini 沒有這類訊號）｜同上｜2026-10-03｜同上，全文搜尋
結構化輸出管最終回答格式，函式呼叫管對話中的動作｜同上，「Structured outputs versus function calling」表｜2026-10-03｜同上

## JSON Schema 與 JSON

JSON Schema 是用來定義 JSON 資料結構的 JSON 媒體類型｜https://json-schema.org/draft/2020-12/json-schema-core｜2026-10-03｜curl -sSL，第 1 節 Introduction
2020-12 版規範以 Internet-Draft 形式發布（draft-bhutton-json-schema-01，Intended Status: Informational，文件首部寫 Expires 18 December 2022），不是 RFC；正文寫「以 Internet-Draft 形式發布」，不寫到期｜https://json-schema.org/draft/2020-12/json-schema-core｜2026-10-03｜同上，文件首部
json-schema.org 標示現行版本是 2020-12｜https://json-schema.org/specification｜2026-10-03｜curl -sSL，頁面寫「The current version is 2020-12!」
type 可為字串或陣列；enum 限定值取自清單｜https://json-schema.org/draft/2020-12/json-schema-validation｜2026-10-03｜curl -sSL，6.1.1、6.1.2
required 省略時行為等同空陣列｜https://json-schema.org/draft/2020-12/json-schema-validation｜2026-10-03｜curl -sSL，6.5.3
additionalProperties 省略時斷言行為等同空 schema（額外屬性通過）｜https://json-schema.org/draft/2020-12/json-schema-core｜2026-10-03｜curl -sSL，10.3.2.3
format 預設只當註解收集，作為斷言是選用｜https://json-schema.org/draft/2020-12/json-schema-validation｜2026-10-03｜curl -sSL，第 7 節
不認得的關鍵字只會被當成註解｜https://json-schema.org/draft/2020-12/json-schema-core｜2026-10-03｜curl -sSL，第 3 節 Overview
RFC 8259（STD 90）定義 JSON 文字的語法｜https://www.rfc-editor.org/rfc/rfc8259｜2026-10-03｜curl -sSL，轉址到 rfc-editor.org/info/rfc8259/

## 示例與編輯判斷（不是來源主張）

報名信、王小美、人數 6、schema 與預期輸出都是原創虛構示例，沒有呼叫任何 API，正文與程式區塊標籤都寫明「示例／未實測」。
「三層」（合法 JSON、符合 schema、內容正確）是本文為了教學設計的分層，不是任何一家文件的用語；正文沒有把它歸給任何供應商。
示例 schema 只用 type（含 null 聯集）、properties、required、enum、additionalProperties、items、description，對照上面三份文件沒有落在任何一家列出的不支援項目；沒有實際送進 API。
圖解沒有數字，唯一的數字是頁尾製圖年份 2026，正文有「2026 年 10 月 3 日」。
未寫模型名、價格、截止日、排行榜分數。

## 與簡報指令的出入（給協調者）

1. 簡報的 SVG 渲染指令用 `chromium-1194/chrome-linux/chrome`，這個完整版 Chromium 在 `--headless --window-size=1600,900` 下只截到約 812 px 高，畫面底部被截掉、整片變白。改用 `chromium_headless_shell-1194/chrome-linux/headless_shell`（`pack_ingest.chromium_binary()` 預設會優先選它）渲染出完整 1600x900，兩張圖都是用這個檢查的。
2. 簡報說字數「不含連結文字」，但 `_body_length` 會把 `rich_paragraph` 裡 `article` inline 的文字也算進去。`research.json` 的 `running_text_characters` 採 `_body_length` 的值：初稿 2578，一審後 2809，二審為可讀性刪減後 2543；扣掉連結文字是 2454。
3. 目錄把 JSON Schema 稱為「規範原文」；實際上 2020-12 版是 Internet-Draft，不是 RFC，正文已照此寫。
4. 簡報要求寫各家「拒答訊號」：OpenAI 與 Anthropic 有，Google 這一頁沒寫，正文如實寫「這一頁沒寫拒答或截斷的訊號」。
5. dry-run 只有一個警告 `no_summary`（沒有 summary 區塊），簡報沒有要求，留給後續 `pack_cli summarize` 批次處理。

## 查核輪次

一審（verify-1.md）改了 7 處事實；二審（verify-2.md）今天重開七個來源（全部 HTTP 200）確認那 7 處，另抽查三分之一的其餘主張，並為可讀性刪去各家欄位名與次要限制，沒有改事實。
