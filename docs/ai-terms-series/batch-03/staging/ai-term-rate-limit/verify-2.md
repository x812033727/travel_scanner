# 查核紀錄 verify-2：ai-term-rate-limit

查核日 2026-10-03。第二輪查核者，不是撰稿者，也不是第一輪查核者。依 `batch-03/VERIFY.md` 進行，讀了 `brief.md`、`../batch-02/brief.md`、`catalogue.json` 裡這個 slug 的指派，以及同目錄的 `verify-1.md`、`notes.md`、`research.json`。
原本的 16 筆 `sources` 全部用 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開，狀態碼都是 200。另外讀了 RFC 純文字版、Gemini troubleshooting 頁、Microsoft 英文版，並新增 Anthropic 繁中版 rate-limits 頁（200）。作者和第一輪的紀錄只拿來找條目，每條主張都回到原頁核對。

## 修改（原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

事實性修改：

1. 「Google 把每日配額用完單獨列一個代碼，建議等重設」→「Google 的 Interactions API 錯誤表把每日配額用完另列一個代碼，建議等重設」｜api-errors 頁開頭寫 "This page provides a reference for all Interactions API error codes"。用 generateContent 等其他方式呼叫的人不一定拿得到 quota_exceeded，原句把它寫成 Google 全面的做法。來源標題同步改成「Interactions API 錯誤代碼」｜https://ai.google.dev/gemini-api/docs/api-errors
2. 「AWS 觀察到定時工作常在每分鐘開頭或午夜過後幾秒一起啟動，建議排程也加抖動」→「AWS 提到，多台機器的定時工作可能在每分鐘頭幾秒或午夜剛過時撞在一起，建議也加抖動」｜原文的 "frequently" 修飾的是客戶端定期送請求，多台機器同時送出用的是 "can line up"。「常」比原文強｜https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
3. 表格「聊天方案上限｜等重設或換方案，與 API 分開」→「等重設、升級方案或加購用量，與 API 分開」｜說明中心原文是 "you'll need to wait for it to reset, upgrade your plan, or purchase usage credits"。原格漏了加購用量，「換方案」也包含降級，不精確｜https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work

措辭與來源修改（不計入 facts_changed）：

4. 「Google 繁中文件標題作「頻率限制」，內文與 Microsoft 繁中文件多作「速率限制」；這裡用後者」→「Anthropic 與 Microsoft 的繁中文件寫「速率限制」，Google 繁中頁標題作「頻率限制」、內文兩者混用；這裡用「速率限制」」｜Google 繁中頁頁首註明是 AI 翻譯，Microsoft 繁中頁也有明顯機器翻譯痕跡（TPM 譯作「每分鐘代幣數」）。這兩頁當譯名依據的證據力有限，所以加上 Anthropic 繁中頁：「速率限制」90 次、「頻率限制」0 次，沒有機器翻譯說明。原句沒有錯（Google 正文「速率限制」20 次、「頻率限制」11 次）。`sources` 新增這一頁，Google 繁中頁標題改成「AI 翻譯，譯名參考」｜https://platform.claude.com/docs/zh-TW/api/rate-limits ；https://ai.google.dev/gemini-api/docs/rate-limits?hl=zh-tw ；https://learn.microsoft.com/zh-tw/azure/foundry/openai/how-to/quota
5. 「Anthropic 用 token bucket 演算法⋯⋯（此處 token 指額度籌碼）⋯⋯所以這一分鐘還沒用完，下一秒仍可能被擋」→「Anthropic 用權杖桶（token bucket）演算法⋯⋯所以這一分鐘的額度還沒用完，短時間送太密仍可能被擋」｜「權杖桶」是 Anthropic 繁中文件的譯法，避開和模型 token 混淆的括號。末句改成貼近原文 "Short bursts of requests can exceed the limit"｜https://platform.claude.com/docs/en/api/rate-limits
6. 「要看錯誤內容的 error_code 才分得出來，自己另設的較低花費上限則回 400」→「自設的較低上限則回 400」｜精簡 429 這一段的三家細節。「才分得出來」也略強，因為沒有 retry-after 標頭本身就是線索。error_code 的細節留在 notes.md｜https://platform.claude.com/docs/en/api/rate-limits
7. 「在他的設定下（100 個客戶端同時更新同一筆資料），加抖動讓總呼叫數減少一半以上」→「他模擬 100 個客戶端搶著更新同一筆資料，加抖動後總呼叫數少了一半以上」｜精簡模擬設定的寫法，數字與條件不變（"In the case with 100 contending clients, we've reduced our call count by more than half"）｜https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
8. 「五層呼叫各自試 3 次，最底層的負載」→「五層服務呼叫各自試 3 次，最底層資料庫的負載」；「非冪等的請求」→「非冪等（重送可能多生效一次）的請求」｜把原文的資料庫寫出來，並替一般讀者解釋「非冪等」（RFC 9110 §9.2.2 的定義：多次相同請求的效果和一次不同）｜https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter ；https://www.rfc-editor.org/rfc/rfc9110
9. 其餘小改：「分成每分鐘輸入 token（ITPM）與每分鐘輸出 token（OTPM）」→「算成每分鐘輸入 token（ITPM）與輸出 token（OTPM）」；「把訂閱方案分成使用量上限與受上下文視窗限制的長度上限」→「把訂閱方案的上限分成使用量上限與長度上限（受上下文視窗限制）」；節流清單「OpenAI 以 max_tokens⋯⋯」補「輸出上限」三字說明 max_tokens｜措辭

pack.json 的結構沒有動：6 個 H2、恰好 1 個表、1 個 callout，5 個指派連結（含 `ai-terms-index`）都在。`diagram-1.svg` 與 `hero.svg` 沒改，圖上的文字和 `<desc>` 沒有碰到這輪改的主張。`_body_length` 從 2,665 變成 2,684（用 `app.guides.pack_ingest._body_length` 實算），在 1,800–3,000 內。dry-run 通過（exit 0），只剩不必處理的 `no_summary` 警告。`notes.md` 與 `research.json` 已同步（新增來源、Builders' Library 讀法、`running_text_characters` 2684）。

## 第一輪修改的逐條重查

- token bucket「不是每隔固定時間一次重設」：原文 "continuously replenished up to your maximum limit, rather than being reset at fixed intervals"，成立。
- Anthropic 方案等級的每月花費上限回 429、`rate_limit_error`、不附 retry-after、`error.details.error_code` 為 `enforced_spend_limit_reached`；自設上限回 400 `invalid_request_error`，Claude Code 工作區例外。rate-limits 頁與 errors 頁都這樣寫，成立。
- Google 依花費計算的速率限制：滾動時間窗計算，超過回 429 RESOURCE_EXHAUSTED，第一步是 "Wait and retry after a short period"，成立。表格「每月等計費週期內能花的金額」與 Anthropic 的 monthly spend cap、OpenAI 的 enforced monthly spend limit 一致。
- 「組織或專案」：OpenAI "defined at the organization level and at the project level"；Anthropic "Limits are set at the organization level"，另有工作區上限。成立。
- callout「一直重送並不會成功」：原文 "continuously resending a request won't work"，成立。
- 示例「重送時間會錯開，較少擠在同一秒」「多半代表」：沒有寫成保證，符合 AWS 原文 "spread the retries around in time"。
- 「能確認重送無害或原請求沒有生效」：RFC 9110 §9.2.2 "unless it has some means to know that the request semantics are actually idempotent ⋯ or some means to detect that the original request was never applied"，成立。

## 查過、沒問題的主要主張（抽查之外實際全數重看）

- RFC 6585（April 2012，Proposed Standard）第 4 節：429 是 "too many requests in a given amount of time"，SHOULD 說明原因、MAY 附 Retry-After，不定義怎麼辨識使用者、怎麼計數。
- RFC 9110 §10.2.3：Retry-After 是 HTTP-date 或 delay-seconds，範例 120 是 2 分鐘；搭配 503 時表示預計不可用多久。
- AWS Architecture Blog：Marc Brooker，04 MAR 2015；只有指數退避時 "there are still clusters of calls"；100 個客戶端競爭時 "reduced our call count by more than half"；模擬是 OCC。
- Builders' Library：五層、每層 3 次，"the load on the database will increase 243x"，建議 "retry at a single point in the stack"；建議替 "all timers, periodic jobs" 加 jitter。
- OpenAI rate-limits：RPM、RPD、TPM、TPD、IPM 任一先到即觸發；Retry-After "Treat this value as a minimum ⋯ add a small random delay"；SDK 自動重試 429 與 503，自管重試時 "disable SDK retries or account for them"；失敗請求計入每分鐘限制；slow_down 在 RPM、TPM 內也會發生、要逐步加量；計入 max_tokens 與估計 token 數的較大者；Batch API 不影響同步限制；回應標頭有 x-ratelimit-remaining-*。
- OpenAI error-codes：credit_balance_exhausted、organization_spend_limit_exceeded、project_spend_limit_exceeded、組織使用上限都是 429；"Retrying billing, spend, or quota errors won't restore API access"；error.type 仍可能是 insufficient_quota。
- Anthropic：兩類限制；RPM、ITPM、OTPM；超過回 429 附 retry-after；短區間執行（60 RPM 可能以每秒 1 次執行）；加速限制；大多數模型 cache_read_input_tokens 不計入 ITPM；max_tokens 不計入 OTPM；Message Batches 有獨立限制；回應標頭有剩餘量；Messages API 無狀態、每次送完整歷史；輸入超過上下文視窗回 400 "prompt is too long"。
- Google：RPM、TPM（input）、RPD；"applied per project, not per API key"；RPD 在太平洋時間午夜重設；Batch API 有獨立限制。Gemini 的 rate-limits 與 api-errors 兩頁用 quota 時都指每日上限（"RPD quotas"、"daily quota"），配額段「Google 指每日上限」成立。
- Microsoft Learn：配額依區域、模型、部署類型以 TPM 分給訂閱，部署分到的 TPM 直接對應它的 TPM 速率限制。
- Claude 說明中心：使用量上限與長度上限（上下文視窗）是兩種限制；付費訂閱 "doesn't include access to the Claude API or Console"。
- 示例流程 1、2、4、8、8 秒符合 Full Jitter 的 min(cap, base·2^attempt)，基準 1、上限 8，標了「示例（未實測）」。
- 系列規則：沒有型號、價格、截止日期、排行榜分數，也沒有任何服務、方案或等級的限制數字（RFC 範例 120、AWS 的 100 與 243 都是來源自己的範例設定）。沒有繞過限制的方法。topics 是 `["ai", "tutorial", "ai-terms"]`。「本文」「這篇」0 次。正文沒有查證過程。沒有用到推論或推理。沒有中國用語（信息、默認、優化、激活、用戶、視頻、質量、數據、網絡、軟件都是 0 次）。圖上的數字 429、2026 正文都有。

## 第一輪疑點的處理

- Google api-errors 頁只涵蓋 Interactions API：已處理，見修改 1。
- Builders' Library 的 JS 空殼：加 `-H 'Accept: text/html,application/xhtml+xml'` 連抓 6 次，3 次拿到 125,965 bytes 的完整伺服器渲染頁，內文據此核對。Wayback CDX 從這個環境連不上（連線被重設），沒能存快照。
- 「常」略強：已處理，見修改 2。
- 譯名證據：已加 Anthropic 繁中頁，見修改 4。國家教育研究院樂詞網用 curl 查詢時，連「machine learning」都回 0 筆，結果要靠 JavaScript 載入，仍然讀不到。Cloudflare 繁中學習中心回 403 驗證頁，沒有繞過。
- 聊天方案上限漏了加購用量：已處理，見修改 3。
- `_body_length` 超過撰稿目標：精簡後仍是 2,684，因為新增了 Interactions API 的範圍說明、加購用量與非冪等的解釋。在 3,000 上限內，沒有為了湊目標刪事實。

## 我懷疑但沒改的事

- 三個譯名來源都是廠商文件，其中兩個明顯是機器翻譯。Anthropic 繁中頁沒有機器翻譯說明，但也不確定是人工翻譯。國教院樂詞網用 curl 讀不到，「速率限制」是否為台灣通行譯名，仍然沒有中立的詞彙表佐證。
- Builders' Library 網址不帶 Accept 標頭時仍回 JS 空殼，帶了也只有約一半機率拿到全文，又沒有 Wayback 快照可以備援，之後的查核者可能重現困難。
- 節流清單「三家都有獨立於即時呼叫的限制」：OpenAI 的說法是 Batch API "without impacting your synchronous request rate limits"，另有佇列上限，和 Anthropic、Google 的「own rate limits」措辭不同。意思相近，沒有改。
- `_body_length` 2,684 仍高於撰稿目標 2,200–2,600。

facts_changed: 3
