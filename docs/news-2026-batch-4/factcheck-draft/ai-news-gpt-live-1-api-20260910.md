# 獨立查核：ai-news-gpt-live-1-api-20260910

查核日 2026-09-18。查核者沒有參與撰稿。

把正文 16 段、summary 4 句、FAQ 6 題答句、callout、表格 15 格與 caption、圖解 caption 與
四個節點、title、description 拆成 **96 條主張**逐條回一手原文比對，**改了 15 處**
（其中 4 處動到骨幹論述）。29 條 `verbatim_quote` 以程式做連續字串比對，全部命中。

## 重抓結果（四條 sources 都讀到正文，位元組與撰稿者記錄一致）

`curl -sL -A "Mokaair-editorial"`，HTML 與 `.md` 兩版各抓一次。

| source | HTTP | bytes（.md） | 驗到的東西 |
| --- | --- | --- | --- |
| developers.openai.com/api/docs/changelog | 200 | 69,420 | `September, 2026` → `Sep 10` 的 `Feature · Model: gpt-live-1 · API: v1/live/sessions`（中點是 U+00B7）；`is now generally available in the API`；`$0.05 per minute, billed per second`；Responses／client 委派那句。回溯到 `October, 2023` |
| developers.openai.com/api/docs/models/gpt-live-1 | 200 | 2,713 | 模態四行與 `Jul 31, 2025 knowledge cutoff`；Pricing 與 `Session duration is not rounded up…`；18 列 Endpoints 表（只有 Live 是 Supported，末列 `Completions (legacy)`）；`Unsupported usage tiers: Free.`；Tier 1–5 的 25／50／200／300／500 |
| developers.openai.com/api/docs/guides/voice-sip | 200 | 22,381 | 第 1–103 行為 GPT-Live 半頁（第 109 行起換成 Realtime，本次引文全部只取前半）：兩種連線方式表、300–699、486、`decision_already_made`、refer／hangup 的 `200 OK`、`sip_headers` untrusted、第 85 行的 inbound／outbound 那句、**第 43 行的 `deprecated live.call.incoming`** |
| developers.openai.com/api/docs/guides/live-conversations | 200 | 33,781 | Configuration fields 表、12 列語音表（Language 欄 10 English／2 Portuguese）、`Regional influence…not a guarantee of accent fidelity`、128,000 與 90%、8,192 tokens 與 `when available`、store／30 天／ZDR、stereo WAV、五個 `reason`、**Deliver a disclosure 段**、**第 257 行的 `Use the language specified by your application`** |

反證用、未寫入文章：`openai.com/news/rss.xml`（200、736,773 bytes、1,207 筆；第一輪記 1,195，已再次證明是活資料）。
`openai.com/index/introducing-gpt-live` 與 `…-1-in-the-api` 仍 403。

## 改掉的 15 處

**1（骨幹）. 「同一套技術先前已經用在 ChatGPT 的語音對話裡」整個框架 → 刪除。**
出現在第一段、第一節標題（「和 7 月有什麼不同」）、第一節第一段、FAQ 第一題、description 五處。
四條 sources **沒有任何一句**把 GPT-Live 連到 ChatGPT：`ChatGPT` 以詞界比對只在 changelog 出現
（21 次、18 行），全部是 `chat-latest` 快照、`gpt-image`／`chatgpt-image` 模型與 Secure MCP Tunnel；
而回溯到 2023-10 的整份 changelog 裡，`gpt-live` 只出現在 2026-09-10 那條與兩條 `gpt-live-transcribe`，
**2026 年 7 月完全沒有 GPT-Live 條目**。今天另抓官方 RSS 確認〈Introducing GPT-Live〉的 pubDate 是
`Wed, 08 Jul 2026 00:00:00 GMT`，但 feed 只給標題與日期、標題本身沒有 ChatGPT 字樣，文章頁 403 ——
**連 feed 也撐不起「那次是在 ChatGPT 端」**。`sources[]` 上限 4 條且四條全部吃重，無法再加，故整段改寫。

**2（骨幹）. 「是同一套技術第一次以 API 的形式開放給開發者」→ 被 sources 自己推翻。**
changelog 只寫 `is now generally available in the API`——GA 是**狀態**，不是首度供應；
而 voice-sip 第 43 行寫 `Existing integrations may still receive the deprecated `live.call.incoming` event`。
既有整合＋已淘汰的事件名稱，代表 9/10 之前就有整合在跑。改成照抄 GA 的說法，並把這句反證寫進正文與 FAQ。

**3（骨幹）. summary 與第四節「選定聲音與語言後，通話中途都不能更換」→ 語言那一半是杜撰。**
來源只在 Configuration fields 表對 `Model` 與 `Voice` 寫 `Start a new session to change it.`，
**對語言一個字都沒有**。反方向還有反證：同頁第 257 行 `Use the language specified by your application
until the caller speaks`，而 `instructions` 正是可以用 `session.instructions.append` 中途追加的欄位。
已刪去語言那一半，並把「語言由應用程式指定」補進正文與 FAQ。

**4（骨幹）. 「這個電話功能目前只能接聽…不是 GPT-Live 1 直接支援」→ 限縮成來源的範圍。**
原文（第 85 行）是 `This flow accepts inbound calls. Creating an outbound SIP call through
`POST /v1/live/sessions` is not supported; use the relevant partner integration for **provider-owned
outbound calling**.`。「This flow」指的是 Direct SIP 這一段流程，不是整個產品；而且原文把外撥講成
「業者自己掌握」，不是「做不到」。summary、FAQ 第四題、圖解節點（「只能接聽／電話 API 不支援外撥」
→「接聽為主／外撥須走合作夥伴」）與 caption（「電話只接不撥」→「電話接聽為主」）一併改。

**5. 「GPT-Live 1 用一個 API 動作決定接聽或拒接」→ 主詞錯了。**
來源：`Your backend still owns the incoming-call decision`、`Apply your application's authorization and
routing rules.` 決定的是開發者的應用程式，不是模型。已改。

**6. 「通話中可以用另一個動作把電話轉接出去，或直接掛斷…兩者成功時」→ 自相矛盾。**
`refer` 與 `hangup` 是兩個獨立端點，`Both return 200 OK`。「另一個動作」改成「另有兩個動作」。

**7. 被刪掉的限定詞，四處補回。**
`up to 8,192 tokens of conversation history, containing recent messages and, **when available**, a
summary of older messages` 的 `when available`（草稿寫成「加上舊訊息的摘要」）；
Direct SIP 責任清單漏掉的 `session configuration`；伺服器橋接漏掉的 `event translation, playback,
and call lifecycle`；store 漏掉的 `a data policy that permits persistence`。

**8. 「應用程式只需要處理…」的「只」刪除**——來源是中性的 `Your application handles …`，
草稿加了一個最小化的限定詞。

**9. 「電話業者直接把通話音訊送給 OpenAI」→「交換」。** 原文是 `exchanges call audio with OpenAI`，雙向。

**10. 「SIP 標頭只能當成參考資料」→「不可信的來電方資訊」。**
原文 `Treat data.sip_headers as **untrusted** caller metadata, not authorization.`「參考資料」把 untrusted 弄丟了。

**11. 「知識截止日是 2025 年 7 月 31 日，也就是說那之後才發生的事，它不會知道」→ 刪去絕對推論。**
來源只印 `Jul 31, 2025 knowledge cutoff`；而且這句與本文自己寫的「委派給後端查資料」互相矛盾。
改成「模型本身訓練資料的時間點」。

**12. 「這代表它是一條獨立的產品線，不能直接套用其他端點的呼叫方式」→ 換成來源自己的話。**
voice-sip 第 5 行印著 `Each API has its own authentication, session creation, and event contract.`
推論改成引用。

**13. 「官方定義了五種結束原因」→「官方文件列出的結束原因包含」。** 清點的數字來源沒印。
同段 `expired` 的中譯「通話達到時長上限」改成「工作階段達到時長上限」（原文是 `The session`）。

**14. 否定句一律限縮到「本文查核的四份官方文件」。**
支援語言、可使用的地區、國家清單、更早的預覽時程四處。查法已寫進研究紀錄的 `not_said`：
`Taiwan` 四頁詞界比對各 0 次；`country` 只有 1 次、在 voice-sip 後半 Realtime 段的
`an unsupported country code` 錯誤訊息裡；`countries` 0 次。
另外 callout 的「沒有規定業者必須告知你正在跟 AI 對話」補上文件自己的 **Deliver a disclosure** 段落
（示範請模型唸出 `This call may be recorded for quality and training purposes`，但那是開發者的選擇，
而且同段寫著 `This requests the wording; it does not guarantee exact delivery.`）。

**15. 其餘小處。** 速率限制刪掉來源沒印的「而不是每分鐘呼叫次數」對比；表格「唯一端點」→「唯一支援端點」；
第二節標題「還沒有免費層級」→「不支援免費層級」（`Unsupported usage tiers: Free.` 沒有「還沒」的意思）；
語音舉例的「偏英式腔的 vesper」改用文件自己的 `Language`／`Regional influence` 欄位措辭
（文件下一句就說 regional influence 不保證腔調擬真，草稿卻先把它寫成腔調）；
錄音「使用者的聲音與 AI 的聲音」改回 `input audio`／`output audio`；
補上 `Omitted or null delegation selects client mode`。

## 撰稿者點名要重查的三句

1. **「官方文件沒有列出支援的口說語言」** —— 事實成立，但範圍要改，已改（見第 14 處）。
   四頁裡唯一的語言資訊是 12 列語音表的 `Language` 欄（10 English、2 Portuguese），
   那是**每個具名語音的欄位值**，不是模型支援語言的清單；預設語音 `marin` 根本不在表內。
   而且文件反過來要開發者「用應用程式指定的語言」並拿自己支援的語言去測試 ——
   **草稿把「文件沒列清單」寫得像「模型只會兩種語言」**，已補上這個反向證據。

2. **「三分鐘通話約 0.15 美元」** —— **留下，算術與歸屬都站得住，但補了查核日綁定。**
   單價出自模型頁 `## Pricing` 的 `Voice sessions cost $0.05 per minute, billed per second.`
   （changelog 同日條目重複印一次，兩處一致）。這是**每分鐘工作階段**計費，不是 token 計費，
   所以不需要「輸入／輸出音訊各多少」的假設；假設只有「語音部分講滿三分鐘」一個。
   0.05×3＝0.15，正確。草稿已標明是編輯換算，本次在正文與 FAQ 兩處各補上「依查核日 2026-09-18 的費率」。
   價格頁是活文件這件事，已寫進 `live_data_warnings` 與 `factcheck.left_for_the_owner`。

3. **「只能接聽、不能透過此 API 主動撥出」** —— **比來源強，已限縮**（見第 4 處）。

## 六條 must_add 的判斷：沒有一條到「不寫就會誤導」

| must_add | 判斷 |
| --- | --- |
| **定價頁「資料落地端點加收 10%」** | **不寫不會誤導。** 文章從頭到尾沒有提資料落地或區域處理端點，也明講後端模型與工具另計、總價要看後端做了多少事，沒有把 0.05 美元說成全額。四條 sources 裡唯一的 `data residency` 在 voice-sip **後半的 Realtime 段**，不能拿來撐 GPT-Live。要納入就得把 pricing 頁收進 `sources[]` |
| guides/audio 的 `start with GPT-Live` 定位 | 不寫不會誤導：文章沒有做任何模型間的定位比較 |
| 合作夥伴表的外撥措辭（Twilio／Telnyx） | 已用 voice-sip 自己的 `provider-owned outbound calling` 達成同樣效果，見第 4 處 |
| live-prompting 的 `small context window` 調和 | 本篇沒有引 live-prompting，矛盾不存在 |
| 7/8 RSS pubDate 錨點 | 見第 1 處：feed 撐不起「在 ChatGPT 端」這句 |
| feed 佔位時間（338 筆 `00:00:00 GMT`） | 文章沒有用到任何時刻，不適用 |

## 查過而且正確的部分（沒有動）

- 事件日 2026-09-10 與 `news_date`、slug 尾碼三者一致；`checked_on` 2026-09-18 在四處一致，未更動。
- 每分鐘 0.05 美元、按秒計費、不進位到整分鐘、後端另計：模型頁與 changelog 兩處印法一致。
- 模態、`Jul 31, 2025` 截止日、端點表（只有 Live 是 Supported、末列官方列名 `Completions (legacy)`）、
  `Unsupported usage tiers: Free.`、Tier 1–5 的 25／50／200／300／500，逐格相符。
- SIP 細節全中：300–699 與 486、第一個決定生效、refer／hangup 的 `200 OK` 空內容、四家合作夥伴原句。
- 聲音與工作階段：`marin` 預設、12 列語音表、accent fidelity 但書、換聲音要開新工作階段、
  128,000 與 90%、8,192 tokens、store 預設 false 且須為專案啟用、30 天到期、ZDR 下 store 視為 false、
  stereo WAV、usage 是快照不可相加、五個 `reason` 的字面意義。
- **29 條 `verbatim_quote` 全部是今天頁面上的連續字串**，URL 全在 `sources[]` 內，
  voice-sip 的引文全部落在 GPT-Live 半頁（第 1–103 行）。這一包的引文欄位是乾淨的。
- 界線：沒有購買建議、沒有推薦式比價、沒有投資免責 callout（AI 篇本來就不該有）、callout 恰好一個；
  廠商宣稱（`Our premier model…`、full-duplex 定義）都有歸屬並註明本站沒有實測。
- 圖上四個數字（1、12、30、0.05）都出現在正文；summary 的數字都出現在正文。

## 留給站主的 4 件事

1. **7 月 ChatGPT 端的對照框架被整段刪掉。** 要救回來只有兩條路：把 `openai.com/news/rss.xml`
   加成第五條 source（會破 BRIEF 的 4 條上限，而且 feed 只給標題與日期、標題沒有 ChatGPT 字樣），
   或改走站內既有的 `ai-news-gpt-live-voice-20260708`。本篇第二個結尾連結目前指向
   `ai-news-gemini-38-live-20260915`（`check_article.py` 的 `RELATED` 寫死），是否改指 7/8 那篇，
   由站主與協調者決定——**查核者沒有動兩個結尾連結**。
2. **10% 資料落地加價仍不寫**，理由見上表。要納入必須把 pricing 頁收進 `sources[]`。
3. **四頁都是沒有版本號、沒有日期的活文件。** 所有數字都綁 2026-09-18；發稿若隔了幾天，
   值得再抓一次模型頁與 changelog（型號、上下文長度、價格、可用端點都可能變）。
4. 其餘四條 must_add 未採用，逐條理由見上表與研究紀錄的 `unverified_or_excluded`。

## 自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-gemini-38-live-20260915
```

只剩規格允許的兩條（索引與相關文章的連結文字，由協調者事後處理）。
段落字數 2,986（限 1,800–3,000），未靠刪限定詞湊字數。

## 結論

`needs_second_round`。改了 15 處，其中 4 處動到骨幹論述：整個「7 月 ChatGPT」對照框架被刪除、
「第一次開放」被來源推翻、「語言不能中途更換」是杜撰、「只能接不能撥」的範圍被限縮。
第二輪只需要逐句回來源查**本輪新寫進去的每一句**（第一段末句、第一節第一段、第一節標題、
FAQ 第一題、第四節第二段新增的語言那一句、callout 的告知語那一段），其餘 96 條主張已逐條驗過。

---

# 第二輪

查核日 2026-09-18。第二輪查核者沒有參與撰稿，也沒有參與第一輪。

覆核了第一輪改動過的每一段、第一輪新寫進去的每一句，以及指派訊息點名的五個疑點，
共 **78 條主張**，**改了 13 處**。沒有一處推翻第一輪的骨幹修正——第一輪那四處全部站得住；
本輪抓到的是那四處修正留下的**殘留與新生的過度**。

## 重抓結果（四條 sources 全部自己重抓，位元組與第一輪一致）

`curl -sL -A "Mokaair-editorial"`，`.md` 與 HTML 兩版各抓一次。

| source | .md HTTP／bytes | HTML HTTP／bytes | 是否正文 |
| --- | --- | --- | --- |
| developers.openai.com/api/docs/changelog | 200／69,420 | 200／511,612 | 是（Sep 15、Sep 10×3、Sep 8… 回溯到 October, 2023） |
| developers.openai.com/api/docs/models/gpt-live-1 | 200／2,713 | 200／406,952 | 是（88 行全文） |
| developers.openai.com/api/docs/guides/voice-sip | 200／22,381 | 200／509,941 | 是（GPT-Live 半頁 = 第 1–103 行，第 97 行 `Next steps with GPT-Live`；第 109 行起才是 Realtime） |
| developers.openai.com/api/docs/guides/live-conversations | 200／33,781 | 200／538,712 | 是（548 行，20 個標題） |

`verbatim_quote` 連續字串比對：原有 29 條 **29/29 命中**，加上本輪補寫的 17 條，共 **46/46 命中**，
URL 全在 `sources[]` 內。沒有任何一條引文含 `...`／`…` 的拼接；唯一帶 `|` 的三條是本輪新增的
**文件表格列**（Vesper／Gleam／Bossa+Tempo），那些 `|` 是 Markdown 表格自己的分隔線，
每一條都是單一連續字串（Bossa 與 Tempo 在原檔是相鄰的第 41–42 行），不是把不同段落拼在一起。

## 改掉的 13 處

**1（骨幹殘留）. 第一段末句「變成開發者可以買來裝進…的零件」→「是開發者…」。**
「變成」把 9-10 寫成狀態的轉變，正是第一輪刪掉的「第一次開放」框架的殘留，
而且與本文自己第一節寫的「可見這之前就有整合在跑」互相矛盾。指派訊息點名要查的第一段末句，
其餘成分逐一回得到來源：「會邊聽邊說」= 模型頁 `It can listen and speak at the same time`；
「買」= 模型頁 `## Pricing` 的每分鐘費率；「電話系統」= voice-sip 的兩種連線方式；
「App 或產品」= 四頁通篇的 `Your application`。

**2（骨幹殘留）. GA 的譯法全文統一成「正式提供」。**
第一段「正式在 API 開放（generally available）」→「已在 API 正式提供（generally available）」；
第一節標題「正式開放」→「正式提供（GA）」；summary 第一句與 description 的「正式推出」同步。
`is now generally available in the API` 是供應狀態，正文裡不再留「開放」「推出」這種帶事件感的動詞。

**3. 第一節第一段首句「GPT-Live 是 OpenAI 的全雙工語音技術」→「官方模型頁把 GPT-Live 1 定義成一個全雙工語音模型」。**
四頁沒有一句把 GPT-Live 稱為「技術」；模型頁第 9 行寫的是
`GPT-Live 1 is a full-duplex voice model for real-time conversations.`
原句還把主詞從有來源的 GPT-Live 1 放大成沒有來源的 GPT-Live。

**4. 第一節第一段「那是一個狀態，不是「第一次出現」」→ 限縮成否定句。**
改成「那句話講的是供應狀態，本文查核的四份文件沒有寫這是第一次出現」。
原句是查核者對 GA 這個詞本身下的斷言；反證仍在（voice-sip 第 43 行
`Existing integrations may still receive the deprecated \`live.call.incoming\` event, which has no \`data.type\`.`）。
FAQ 第一題同步，並把「沒有寫出更早的預覽時程，也沒有寫分批開放的安排」的主詞明寫成「這四份文件」。

**5. 第一節第二段「API 版本的模型代號是 gpt-live-1」→「模型頁列出的模型代號是…」。**
「API 版本的」暗示同型號另有非 API 版本，這四頁沒有寫；模型頁第 7 行印的是 `Model ID: \`gpt-live-1\``。

**6. 第三節第二段「用一個 API 動作決定接聽或拒接」→「分別用一個 API 動作接聽或拒接」。**
accept 與 reject 是兩個各自獨立的端點（`POST /v1/live/sessions/{session_id}/accept` 與 `.../reject`）。
第一輪已為 `refer`／`hangup` 做過同樣的修正（第 6 處），這裡漏掉。

**7（限定詞）. 第四節第二段與 FAQ 第二題：「要開發者「用應用程式指定的語言」」→ 補回「在來電者開口前」。**
原文（live-conversations 第 257 行）是
`Use the language specified by your application until the caller speaks; don't infer it from a name, phone number, or location.`
第一輪新寫這句時把 `until the caller speaks` 刪掉了，**寫得比來源強，也讓它看起來像一條沒有時限的通則**。
這是指派點名的第一輪新句裡唯一一處實質錯誤。同段另一半「拿自己支援的語言去測試」
對得上第 261 行 `Test your greeting with the languages and interruptions your application supports.`

**8. 第四節標題「文件沒有列出支援語言」→「這四份文件沒有列出支援語言」。** 標題裡的否定句原本沒有範圍。

**9. 第五節第三段與 FAQ 第六題的「官方文件沒有…」→「這四份文件沒有…」。** 同一個理由。

**10. callout 的告知語示範補齊並限縮。**
「本通話可能被錄音」→「本通話可能為了品質與訓練目的而錄音」：文件第 274 行示範的整句是
`This call may be recorded for quality and training purposes.`，只譯前半會把用途略掉。
同段「沒有規定業者一定要告訴你正在跟 AI 對話」的主詞明寫成「這四份文件」。
其餘成分無誤：「把它當成開發者的選擇」對得上 `Use \`session.instructions.append\` to request…`，
「不保證逐字唸出」對得上第 301 行 `This requests the wording; it does not guarantee exact delivery.`

**11. description「文件為何不支援用這個端點外撥」→「文件說這個端點不支援外撥」。**
「為何」等於承諾一個理由，但文件只寫 `is not supported` 並要開發者改走合作夥伴整合，沒有給理由。

**12. 第二段「本文只談 API 開發者端的這次開放」→「這次更新」。** 同第 2 處。

**13（騰字數）. 第五節第二段末句刪去「不是每一句都會被完整記住」。**
那是同一句「有可能被摘要或省略」（第 319 行 `Older conversation details may be summarized or omitted.`）
的重複敘述。補回第 7 處的限定詞之後段落字數衝到 3,005，**刪的是重複敘述，不是但書或限定詞**：
2,986 → 3,005 → 2,992。

## 指派點名的五個疑點，逐條結論

**疑點 1：第一輪新寫的五句，逐句回四條來源。**
第一段末句（第 1 處，改「變成」）、第一節標題（第 2 處）、第一節第一段（第 3、4 處）、
FAQ 第一題（第 4 處同步）、第四節語言那一句（**第 7 處，唯一的實質錯誤**）、
callout 告知語那一段（第 10 處）。每一句的每一個成分都已標到來源的行號，見上。

**疑點 2：兩種被推翻的說法沒有殘留。**
title、description、summary、正文、FAQ、圖解 nodes 與 caption 全文比對：沒有「先前已用在 ChatGPT」
「和 7 月有什麼不同」「第一次以 API 開放」或任何等價說法。「第一次」只出現在 FAQ 第一題的**提問**
與正文的**反駁**裡。`ChatGPT` 在四頁的詞界比對重驗：只在 changelog 出現 21 次，逐一看過全部是
`chat-latest` 快照、`gpt-image`／`chatgpt-image` 與 Secure MCP Tunnel，無一與 GPT-Live 有關；
`gpt-live` 在整份 changelog 只出現在 2026-09-10 那條與兩條 `gpt-live-transcribe`。
`rollout`／`staged`／`phased`／`waitlist`／`early access` 四頁各 0 次。
GA 的譯法已統一成「正式提供（GA）」（第 2 處）。
**第二段的「不談 ChatGPT 使用者端的方案與設定」保留**：那是界線聲明，不是把 GPT-Live 連到 ChatGPT
的事實主張；站上既有的 `ai-news-gpt-live-voice-20260708` 自己就寫著「開發者端和 ChatGPT 裡的推出是兩件事」。
**標題未改**，理由見「留給站主」。
另讀 `ai-news-gpt-live-voice-20260708` 內容包全文逐段比對：本篇不碰 7 月發布、方案用量與錄音訓練開關，
不寫 mini 版，因此不重寫也不矛盾；該篇最後一段記的 9-10 事實（在 API 正式開放、每分鐘 0.05 美元、
按秒計費、後端另計）與本篇一字不差地相容。兩個結尾連結未動。

**疑點 3：「只能接聽」限縮後的一致性。** 五處互相一致，也都沒有比原文強：
正文第三節第三段、summary 第三句、FAQ 第四題、圖解節點「接聽為主／外撥須走合作夥伴」、
caption「電話接聽為主」。原文（第 85 行）限縮在 Direct SIP 這段流程（`This flow`），
不支援的是**透過 `POST /v1/live/sessions` 建立**外撥 SIP 通話，外撥則是 `provider-owned`、要走
partner integration——第一輪的限縮正確，本輪未動。

**疑點 4：「三分鐘約 0.15 美元」四項要求全部滿足，未改。**
單價 `Voice sessions cost $0.05 per minute, billed per second.` 在模型頁 `## Pricing`（第 23 行）
與 changelog（第 39 行）兩處字面一致；那是**每分鐘工作階段**計費、不是 token 計費，
所以 0.05×3=0.15 只需要「語音講滿三分鐘」一個假設，算術正確。
正文與 FAQ 兩處都寫明「這是本文的換算，不是官方數字」**並綁查核日 2026-09-18**，
也都寫明後端模型與工具另計、實際總價要看後端做了多少事、這四份文件沒有整通電話的總價範例。

**疑點 5：活文件全部綁查核日。** 四頁都沒有版本號也沒有日期。型號、每分鐘 0.05 美元、
端點表、併發上限 25／50／200／300／500、12 個具名語音、128,000 與 8,192 tokens、90%、
30 天、300–699 與 486，都在正文、表格 caption、圖解 caption 或 FAQ 裡綁著 2026-09-18；
`checked_on` 在內容包四條 source、研究紀錄、第二段、表格 caption 四處一致，**未更動**。

## 查過而且正確、沒有動的部分

- 第一輪那 **4 處骨幹修正全部站得住**，本輪沒有推翻任何一處。
- 研究紀錄補寫了 **17 條 `verified_facts`**：第一輪在報告裡引用、但沒有留進研究紀錄的載重引文
  （`Each API has its own…`、`Existing integrations may still receive the deprecated…`、
  `Your backend still owns the incoming-call decision…`、`Apply your application's authorization…`、
  `Omitted or \`null\` delegation selects client mode.`、`You cannot change the delegation mode after startup.`、
  語音表的引言與 Vesper／Gleam／Bossa+Tempo 三組列、`Use the language specified by your application until the caller speaks`、
  `Test your greeting with the languages…`、告知語示範與它的但書、`up to 8,192 tokens…when available…`、
  `Older conversation details may be summarized or omitted.`、
  `Downloads and forks require…a data policy that permits persistence.`）。全部通過連續字串比對。
- 否定句重驗：`Taiwan`／`Chinese`／`Mandarin`／`countries` 四頁各 0 次；`country` 只在 voice-sip
  第 193 行出現 1 次，而那一行在 **Realtime 半頁**（`an unsupported country code` 的錯誤訊息）；
  工作階段時長上限的數字四頁皆無（唯一的 `duration limit` 是第 538 行沒有數字的 `expired` 說明）。
- 界線：`topics` 是 `ai`／`software`／`ai-news`，不帶 `finance`；只有一個 `info` callout、
  沒有投資免責段落；沒有購買建議、沒有推薦式比價、沒有「值得升級」式結論；
  廠商宣稱（`Our premier model…`、full-duplex 定義）都有歸屬並註明本站沒有實測；
  沒有推定台灣可用（FAQ 第三題明講請以自己帳號畫面為準）。
- `summary` ⊆ 正文、圖解四個節點的數字（12、30、0.05，加上型號裡的 1）都出現在正文。

## 留給站主的 3 件事

1. **標題「GPT-Live 1 開放 API：…」未改。** 判斷是它沒有宣稱首度：句中沒有「第一次」「首度」，
   「開放」對應的是 `generally available` 這個供應狀態，而站上既有、已查核過的
   `ai-news-gpt-live-voice-20260708` 也用同一句「GPT-Live 1 在 API 正式開放」記這一天；
   正文第一節緊接著就寫明那句話講的是供應狀態、這四份文件沒有寫這是第一次出現。
   若仍想換掉標題的動詞（例如「GPT-Live 1 進 API」），要同步改內容包 `title`、研究紀錄 `title`，
   以及協調者做的索引與相關文章連結文字。
2. **FAQ 第一題末句「這四份文件也沒有寫出更早的預覽時程，或分批開放的安排」是正文沒有的一句。**
   事實本身已驗證、範圍也已限縮，因此保留；若要嚴格執行「FAQ ⊆ 正文」，刪掉這一句即可，不影響其餘內容。
3. **第一輪留下的四件事全部維持原判**（7 月 ChatGPT 框架不救回、10% 資料落地加價不寫、
   四頁是活文件、其餘 must_add 不採用）。本輪另外確認：站內 `ai-news-gpt-live-voice-20260708`
   已經替讀者接上 7 月那一段，所以本篇不寫也不會留下缺口。第二個結尾連結仍指向
   `ai-news-gemini-38-live-20260915`，依指派未動。

## 自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
 - zh-TW link text must be the title of ai-news-gemini-38-live-20260915
```

只剩規格允許的兩條。段落字數 **2,992**（限 1,800–3,000），description 188（限 120–200）。
補限定詞導致超標時，刪的是重複敘述，沒有動任何但書或限定詞。

## 第二輪結論

`ok`。
