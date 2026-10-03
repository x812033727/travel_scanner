# 查證與編輯紀錄：ai-term-rate-limit

格式：主張｜來源網址｜查證日｜讀取方式。所有頁面以 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 取得，狀態碼皆 200；HTML 轉純文字後閱讀。

## 規範（RFC）

429 定義為一段時間內送出太多請求；回應 SHOULD 說明原因、MAY 附 Retry-After｜https://www.rfc-editor.org/rfc/rfc6585｜2026-10-03｜curl rfc6585.txt 第 4 節
RFC 6585 發布於 2012 年（April 2012）｜https://www.rfc-editor.org/rfc/rfc6585｜2026-10-03｜curl rfc6585.txt 檔頭
規範不定義伺服器怎麼辨識使用者、怎麼計數｜https://www.rfc-editor.org/rfc/rfc6585｜2026-10-03｜curl rfc6585.txt 第 4 節
Retry-After 值可為 HTTP 日期或秒數；範例 120 即 2 分鐘｜https://www.rfc-editor.org/rfc/rfc9110｜2026-10-03｜curl rfc9110.txt 第 10.2.3 節
Retry-After 可搭配 503 使用，表示預計不可用多久｜https://www.rfc-editor.org/rfc/rfc9110｜2026-10-03｜curl rfc9110.txt 第 10.2.3、15.6.4 節
非冪等請求除非能確認語意冪等或原請求未生效，否則不應自動重試｜https://www.rfc-editor.org/rfc/rfc9110｜2026-10-03｜curl rfc9110.txt 第 9.2.2 節

## 退避與抖動（AWS）

Marc Brooker，2015 年 3 月 4 日；只有指數退避時重試仍成群出現，加抖動後接近固定速率｜https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/｜2026-10-03｜curl HTML；公式是圖片，下載 figure-3/6/10/11 PNG 直接看
模擬設定為樂觀並行控制（多個客戶端同時更新同一列資料）；100 個客戶端競爭時加抖動讓呼叫數減少一半以上｜https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/｜2026-10-03｜同上
Full Jitter：sleep = random_between(0, min(cap, base * 2 ** attempt))｜https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/｜2026-10-03｜figure-6 PNG
五層呼叫、每層各自 3 次嘗試，最底層負載放大 243 倍；建議只在一處重試｜https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter｜2026-10-03｜curl；原網址 aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ 轉址到此
定時工作常在每分鐘開頭或午夜過後幾秒一起送出；建議替計時器與定期工作加抖動｜同上｜2026-10-03｜同上

## OpenAI

單位 RPM、RPD、TPM、TPD、IPM；任一項先到即觸發｜https://developers.openai.com/api/docs/guides/rate-limits｜2026-10-03｜curl（platform.openai.com 同路徑轉址至 developers.openai.com）
限制定在組織與專案層級，不是使用者層級｜同上｜2026-10-03｜同上
Retry-After 當成最少等待時間，再加小的隨機延遲｜同上｜2026-10-03｜同上
官方 SDK 會自動重試部分 429 與 503；自己管理重試時要關掉 SDK 重試或算進上限｜同上｜2026-10-03｜同上
失敗的請求也計入每分鐘限制｜同上｜2026-10-03｜同上
slow_down：流量增加太快，即使在 RPM、TPM 內也可能發生；要逐步加量｜同上｜2026-10-03｜同上
計入限制的是 max_tokens 與依字元數估計的 token 數兩者較大者；建議 max_tokens 接近預期回覆長度｜同上｜2026-10-03｜同上（Reduce the max_tokens 一節）
Batch API 不影響同步請求的速率限制，另有佇列限制｜同上｜2026-10-03｜同上
429 也用於預付額度用完、組織／專案花費上限、組織使用上限；重試帳務、花費、配額類錯誤不會恢復存取｜https://developers.openai.com/api/docs/guides/error-codes｜2026-10-03｜curl
帳務類錯誤的 error.type 仍可能是 insufficient_quota｜同上｜2026-10-03｜同上
觸發原因包括頻繁或同時送請求的迴圈腳本、與其他使用者或應用共用金鑰｜同上｜2026-10-03｜同上

## Anthropic

兩類限制：花費上限（每月最多花多少）與速率限制（一段時間內最多幾個請求）｜https://platform.claude.com/docs/en/api/rate-limits｜2026-10-03｜curl（docs.anthropic.com 轉址至 platform.claude.com）
限制設在組織層級，可再設工作區上限｜同上｜2026-10-03｜同上
Messages API 以 RPM、ITPM、OTPM 計；超過回 429 並附 retry-after｜同上｜2026-10-03｜同上
token bucket 演算法：持續補回到上限，不在固定間隔重設｜同上｜2026-10-03｜同上
每分鐘上限可能在更短區間執行，短時間爆量會觸發｜同上｜2026-10-03｜同上（正文未寫文件中的示例數字）
大多數模型 cache_read_input_tokens 不計入 ITPM｜同上｜2026-10-03｜同上
max_tokens 不計入 OTPM｜同上｜2026-10-03｜同上
每月花費上限用完回 429、type 為 rate_limit_error、不附 retry-after；以 error.details.error_code（enforced_spend_limit_reached）分辨｜同上｜2026-10-03｜同上
Message Batches API 有獨立的速率限制｜同上｜2026-10-03｜同上
加速限制（acceleration limits）：用量急升可能回 429，要逐步加量｜https://platform.claude.com/docs/en/api/errors｜2026-10-03｜curl；rate-limits 頁亦有
Messages API 無狀態，每次送完整對話歷史｜https://platform.claude.com/docs/en/build-with-claude/working-with-messages｜2026-10-03｜curl
輸入本身超過上下文視窗回 400 invalid_request_error（prompt is too long）｜https://platform.claude.com/docs/en/build-with-claude/context-windows｜2026-10-03｜curl

## Google

單位 RPM、TPM（標為 input）、RPD；限制套在專案而非 API 金鑰；RPD 配額在太平洋時間午夜重設｜https://ai.google.dev/gemini-api/docs/rate-limits｜2026-10-03｜curl
另有以花費計算的速率限制，超過回 429 RESOURCE_EXHAUSTED｜同上｜2026-10-03｜同上（正文未寫時間窗與金額）
Batch API 有獨立於非批次呼叫的限制｜同上｜2026-10-03｜同上
繁中頁標題為「頻率限制」，內文混用「速率限制」（約 20 次）與「頻率限制」（約 11 次）｜https://ai.google.dev/gemini-api/docs/rate-limits?hl=zh-tw｜2026-10-03｜curl 後計次
429 分三個代碼：rate_limit_exceeded、too_many_requests 建議指數退避重試；quota_exceeded（每日配額）建議等重設或申請提高｜https://ai.google.dev/gemini-api/docs/api-errors｜2026-10-03｜curl

## Microsoft

Azure OpenAI 的配額：依區域、模型、部署類型以 TPM 分配給訂閱，各部署再分配；部署分到的 TPM 就是它的速率限制｜https://learn.microsoft.com/zh-tw/azure/foundry/openai/how-to/quota｜2026-10-03｜curl 繁中版，並對照英文版 /en-us/ 同頁
繁中文件用「速率限制」（約 38 次，「頻率限制」1 次）｜同上｜2026-10-03｜curl 後計次

## Claude 說明中心（聊天產品）

訂閱方案有兩種上限：使用量上限（一段時間內能用多少）與長度上限（上下文視窗）｜https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work｜2026-10-03｜curl
付費訂閱不包含 Claude API 與 Console，兩者分開｜https://support.claude.com/en/articles/9876003-i-have-a-paid-claude-subscription-pro-max-team-or-enterprise-plans-why-do-i-have-to-pay-separately-to-use-the-claude-api-and-console｜2026-10-03｜curl

## 編輯備註

- 依指派不寫任何服務、方案或等級的限制數字，也不寫官方 SDK 的預設重試次數。正文的 120、20、1、2、4、8、5、2 分鐘都是 RFC 範例或標明「示例（未實測）」的參數；100 與 243 是 AWS 文章自己的模擬與舉例設定。
- 譯名：Google 繁中標題用「頻率限制」，內文與 Microsoft 繁中多用「速率限制」；本系列採「速率限制」，第一段說明。
- 「token bucket」保留英文，括號說明此處 token 是額度籌碼，避免和模型 token 混淆。
- 未寫繞過限制的方法；正文明說同專案多開金鑰額度不會變多。批次 API、提示詞快取、調整 max_tokens 都是官方文件自己建議的做法。
- 曾考慮引用 IETF 草案 draft-ietf-httpapi-ratelimit-headers（2026-05-23 版仍為 Internet-Draft），為控制字數刪去。
- 示例流程是說明用的設計，沒有實際呼叫任何 API。SVG 為手繪向量圖，2026 為製圖年份。
