# 查核紀錄 verify-1：ai-term-rate-limit

查核日 2026-10-03。查核者不是撰稿者。依 `batch-03/VERIFY.md` 進行，並讀了 `brief.md`、`../batch-02/brief.md` 與它指定的兩份文件，以及 `catalogue.json` 裡這個 slug 的指派。
16 筆 `sources` 全部用 `curl -sSL`、User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 重新打開，狀態碼都是 200。另外讀了 RFC 純文字版、Gemini troubleshooting 頁和 Microsoft 英文版對照。作者的 notes.md 與 research.json 只拿來找條目，每條主張都回到原頁核對。

## 修改（原句（節錄）→ 改成 ｜ 理由 ｜ 依據網址）

事實性修改：

1. 「持續補回到上限，不是整點一次歸零」→「持續補回到上限，不是每隔固定時間一次重設」｜文件寫的是 "rather than being reset at fixed intervals"。原句的主詞是額度，「歸零」會讓人以為額度被清空，意思剛好相反；「整點」也不是文件說的固定間隔｜https://platform.claude.com/docs/en/api/rate-limits
2. 「Anthropic 每月花費上限用完時回 429 但不附 retry-after，要看錯誤內容的 error_code 才分得出來」→「Anthropic 方案等級的每月花費上限用完時回 429 但不附 retry-after，要看錯誤內容的 error_code 才分得出來，自己另設的較低花費上限則回 400」｜回 429 而且沒有 retry-after 的只有方案等級（usage tier）的每月上限。使用者在 Console 自己設的組織或工作區花費上限用完時回 400 invalid_request_error（Claude Code 工作區例外）｜https://platform.claude.com/docs/en/api/rate-limits ；https://platform.claude.com/docs/en/api/errors
3. 「Google 把每日配額用完單獨列一個代碼，建議等重設。」→ 句尾補「依花費計算的速率限制則是短時間窗，建議稍等再試」；表格「花費上限｜一段期間內能花的金額」→「每月等計費週期內能花的金額」｜Gemini API 另有依花費計算的速率限制（spend-based rate limits），用滾動時間窗計算，超過時回 429 RESOURCE_EXHAUSTED，官方第一步建議是 "Wait and retry after a short period"。原本的表格和 callout 寫「一段期間內能花的金額 → 不重試」，會讓讀者把它當成不可重試的花費上限。正文沒有寫時間窗長度與金額，符合指派｜https://ai.google.dev/gemini-api/docs/rate-limits
4. 節流清單「因為額度算在專案上」→「因為額度算在組織或專案上」｜Anthropic 的限制定在組織層級，可以再設工作區上限，沒有「專案」；OpenAI 定在組織與專案。原句也和同篇第二節的說法不一致｜https://platform.claude.com/docs/en/api/rate-limits ；https://developers.openai.com/api/docs/guides/rate-limits

措辭修改（不計入 facts_changed）：

5. callout「一直重送只會更久」→「一直重送並不會成功」｜改回 OpenAI 原文 "continuously resending a request won't work" 的意思｜https://developers.openai.com/api/docs/guides/rate-limits
6. 示例「預期結果：多個工作不會同一秒一起重送。若 5 次都失敗，代表平均速度本身超標」→「預期結果：多個工作的重送時間會錯開，較少擠在同一秒。若 5 次都失敗，多半代表平均速度本身超標」｜隨機抖動不保證錯開，系列規則不寫保證｜https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
7. 「非冪等的請求除非能確認原請求沒有生效」→「非冪等的請求除非能確認重送無害或原請求沒有生效」｜RFC 9110 §9.2.2 另一個例外是確知請求語意本身冪等｜https://www.rfc-editor.org/rfc/rfc9110

pack.json 的結構沒有動：6 個 H2、恰好 1 個表、1 個 callout，5 個指派連結都在，`diagram-1.svg` 與 `hero.svg` 沒改（重新渲染檢查過，沒有疊字或超框）。`_body_length` 從 2,594 變成 2,665。dry-run 通過，只剩不必處理的 `no_summary` 警告。

## 查過、沒問題的主要主張

- RFC 6585（April 2012）第 4 節：429 的定義是 "too many requests in a given amount of time"，回應 SHOULD 說明原因、MAY 附 Retry-After，規範也不定義怎麼辨識使用者、怎麼計數。rfc-editor 資訊頁沒有 Obsoleted by。
- RFC 9110 §10.2.3：Retry-After 可以是 HTTP-date 或 delay-seconds，範例 120 就是 2 分鐘，也可以搭配 503 使用（§15.6.4）。§9.2.2 規定非冪等請求不應自動重試。
- AWS Architecture Blog 是 Marc Brooker 在 2015 年 3 月 4 日發表的。模擬設定是 OCC，很多客戶端同時更新同一列資料。只有指數退避時重試仍然成群，加上 jitter 後，在 100 個客戶端競爭的設定下呼叫數減少一半以上。
- Builders' Library：五層呼叫、每層 3 次，資料庫負載放大 243 倍，建議只在一處重試；每分鐘開頭或午夜過後幾秒的定時工作會撞在一起，建議替定期工作加 jitter。
- OpenAI：RPM、RPD、TPM、TPD 任一項先到就觸發；限制定在組織與專案；Retry-After 當作最少等待時間，再加小的隨機延遲；SDK 會自動重試，應用自己重試時要關掉或算進上限；失敗的請求也計入每分鐘限制；slow_down 在 RPM、TPM 內也可能發生，要逐步加量；計入的是 max_tokens 與估計 token 數兩者較大者；Batch API 不影響同步限制。error-codes 頁：預付額度、組織或專案花費上限、組織使用上限都回 429，重試不會恢復，error.type 仍可能是 insufficient_quota。
- Anthropic：限制分花費上限與速率限制兩類；RPM、ITPM、OTPM；token bucket；每分鐘上限可能在更短區間執行；加速限制（acceleration limits）；大多數模型的 cache_read_input_tokens 不計入 ITPM；max_tokens 不計入 OTPM；Message Batches 有獨立限制；回應標頭有剩餘量。Messages API 是無狀態的，每次送完整歷史。輸入超過上下文視窗時回 400。
- Google：RPM、TPM（標為 input）、RPD；限制套在專案上，不是 API 金鑰；RPD 在太平洋時間午夜重設；Batch API 有獨立限制。api-errors 頁的 429 分 rate_limit_exceeded、quota_exceeded、too_many_requests 三種。
- Microsoft Learn（繁中與英文版）：Azure OpenAI 的配額依區域、模型、部署類型以 TPM 分給訂閱，再分配到各部署，部署分到的 TPM 就是它的速率限制。
- 譯名：Google 繁中頁的標題是「頻率限制」，內文「速率限制」20 次、「頻率限制」11 次；Microsoft 繁中頁「速率限制」38 次、「頻率限制」1 次。
- Claude 說明中心：使用量上限與長度上限（上下文視窗）是兩回事；付費訂閱不含 API 與 Console。
- 示例流程的 1、2、4、8、8 秒符合 Full Jitter 公式 min(cap, base·2^attempt)，基準 1、上限 8；示例標了「示例（未實測）」。
- 系列規則：沒有型號、價格、截止日期、排行榜分數，也沒有任何服務、方案或等級的限制數字。圖上的數字 429、2026 正文都有。沒有繞過限制的方法。topics 含 `ai-terms`。「本文」「這篇」0 次。正文沒有查證過程。沒有中國用語（信息、默認、優化、激活、用戶等都是 0 次），也沒有用到推論或推理。

## 我懷疑但沒改的事

- Google 的 api-errors 頁自稱是 Interactions API 的錯誤代碼表，troubleshooting 頁則把它當成完整參考。用 generateContent 的呼叫端看到的 429 可能只有 RESOURCE_EXHAUSTED，沒有 quota_exceeded 這個代碼。正文「Google 把每日配額用完單獨列一個代碼」照官方頁寫，沒有改。
- Builders' Library 的 builder.aws.com 網址用 curl 抓時多半只回 3,849 bytes 的 JS 空殼（狀態碼 200）。完整頁只在一次轉址時拿到並據此核對，之後可能需要改用 Wayback 快照佐證。
- 「AWS 觀察到定時工作常在每分鐘開頭或午夜過後幾秒一起啟動」：原文的「frequently」講的是客戶端定時送請求，多台機器撞在同一刻用的是「can line up」，原句的「常」略強。
- Google 繁中頁是機器翻譯（頁首有說明），拿它的用字當台灣譯名依據，證據力有限。國教院雙語詞彙網用 curl 讀不到搜尋結果，Google 機器學習詞彙表沒有這個詞條。
- 表格「聊天方案上限」的處理寫「等重設或換方案」，Claude 說明中心還列了加購用量（usage credits）。這一格不算錯，所以沒改。
- `_body_length` 2,665 超過撰稿目標 2,600，但在 3,000 上限內，沒有為了湊目標刪事實。

facts_changed: 4
