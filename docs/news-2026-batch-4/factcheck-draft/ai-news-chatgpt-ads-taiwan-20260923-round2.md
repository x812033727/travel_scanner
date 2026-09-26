# 查核報告（第二輪）：ai-news-chatgpt-ads-taiwan-20260923

## 第二輪

- 查核者：獨立查核代理，第二輪（claude-opus-5-5）；沒有參與撰稿，也不是第一輪。
- 查核日：2026-09-26（台北）；重抓時間 2026-09-26T14:48–14:49Z。
- 規格：`<WORK>/FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/ai/SECOND-ROUND.md`（及它引用的 `agents/ai/FACTCHECK.md`）、DELTA-4-8（全）、DELTA-4-7 第 3、4、10、11、14、16 條；第一輪報告 `<WORK>/factcheck/ai-news-chatgpt-ads-taiwan-20260923-round1.md`。
- 報告放在 `<WORK>/factcheck/`（指派訊息的路徑）；SECOND-ROUND.md 說附在同一份報告後面，這裡照指派訊息另開一檔，標題仍寫「第二輪」。協調者要進 repo 時複製到 `docs/news-2026-batch-4/factcheck-draft/<slug>-round2.md`（DELTA-4-8 第 9 條）。

### 摘要

- 查了 48 條：第一輪改過或新寫的 15 句全部，加上第一輪其餘 97 條 CONFIRMED 中以固定種子（20260926）隨機抽的 33 條；另外 116 條全部回掃限定詞，研究紀錄 49 條 `verbatim_quote` 用程式對今天的正文做連續字串比對（49／49）。
- 結果：CONFIRMED 45、CHANGED 3（#3 description、#6 第一段、#68 第 15 段）、NOT FOUND 0。回掃另找到 1 條同型錯誤（summary 第 4 句），事實修改合計 4 處，都是「封閉清單被刪掉一項」：
  - 買廣告的三條管道掉了「技術夥伴」（description、第一段、summary 4）；
  - 未來計畫「new formats, optimization tools, and measurement solutions」掉了「優化工具」（第 15 段）。
- 第一輪的 15 處全部成立（#68 的「具體時程」成立，但同一句另有上面那個漏項）。
- 協調者五點裁定都已實作（下節）。內容包共 21 處文字替換；研究紀錄改 1 條 `verified_facts` 的 `fact` 文字，加 `factcheck.second_round`。
- 段落字數 2,907 → 2,811（≤3,000）。
- 自檢：`check_article.py` → `OK ai-news-chatgpt-ads-taiwan-20260923 zh-TW paragraphs 2811`（exit 0）。`pack_cli lint` 只有 `raw_internal_url`（warning）與兩條 `image_missing`（error，出圖前預期），exit 1 就是這兩條造成的。
- 來源與指示有一處衝突，以來源為準：裁定 4 的轉述寫「registers」，原文是「will advertise」（見「來源與指示的衝突」）。
- 結論：`ok`。

### 重抓結果

| # | URL | HTTP | 轉址 | bytes（落地檔） | body | 備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/ | 200 | 0 | 386,687 | 正文 | 頁首 September 23, 2026；`<article>` 抽出文字與第一輪逐字相同 |
| 2 | https://help.openai.com/en/articles/20001245-ads-manager-availability | 200 | 0 | 63,842 | 正文 | 自印 Updated: 18 hours ago；updatedAt 2026-09-25T21:12:52Z 不變；Taiwan｜Available |
| 3 | https://help.openai.com/en/articles/20001047-ads-in-chatgpt | 200 | 0 | 98,313 | 正文 | 自印 Updated: 5 hours ago；updatedAt 2026-09-26T10:04:51Z 不變 |
| 4 | https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/ | 403 → 200 | 0 | 9,967 → 401,787 | 擋阻頁 → 正文 | 第一次 403（間歇性，DELTA-4-7 第 11 條），隨即重試 200；只用重試那份。頁首 August 31, 2026 |
| — | https://openai.com/news/rss.xml | 200 | 0 | 750,532 | feed | 1,230 筆；本篇 pubDate Wed, 23 Sep 2026 02:00:00 GMT、8 月篇 Mon, 31 Aug 2026 04:00:00 GMT（日期依據，不在 sources[]） |

四頁與第一輪的差異只有說明中心的「Updated: N hours ago」一行（相對時間），條文沒有改。

### 協調者裁定（實作後再查）

1. **第二段改成直接對讀者說話。** 原本是查證敘述：「讀了 OpenAI 這篇公告，以及說明中心…兩頁查核當天讀到的版本…內容以查核當天讀到的版本為準」。改成：「無廣告方案的清單與開放自助投放的國家表都在 OpenAI 說明中心，頁面會更新，以下寫的是 2026 年 9 月 26 日的內容。本站沒有實測 ChatGPT 廣告，也不提供投放或訂閱建議。」
   - 「頁面會更新」有兩處依據：H2 “Availability may continue to evolve as testing expands.”，以及兩頁自印的更新時間。
   - 查核日仍在開頭兩段（checker 規則），檢查通過。
2. **欄名 “Self-service availability” 不進正文。** 第 12 段改成「國家表把台灣列為已開放自助投放（Available）」。“Available” 在括號裡留一次，讓讀者能對照官方頁；summary 4、FAQ 4 只寫「已開放」。
3. **重複的查核日說法只留一處。** 以下都拿掉了：
   - summary 2、4，第 6 段，FAQ 2、4，callout 的「查核日讀到的」；
   - 表格列的「（查核日版本）」，表格 caption 的「查核日…讀到的」；
   - 第 5、6、14、16 段的「以…查核到 2026-09-26 未見」；
   - callout 的「查核到 2026 年 9 月 26 日為止」。

   唯一的 as-of 句在第二段，點名兩個活頁面（方案清單、國家表）。否定句改成指名頁面的直述，例如「公告沒有說明…」「這兩頁都沒有寫…」「公告與說明中心都沒有寫…」，每一句今天都重驗過（見下表）。
4. **「不是使用者或行銷人員本人在哪裡」這個對照改成原文的規則。** 改了第 12 段、第 4 節標題、FAQ 4、callout 四處，統一寫成「刊登廣告並被收費的法律實體必須設在國家表列為開放的國家」，標題改成「自助投放看法律實體所在國家」。
   - 國家表頁今天全文沒有任何「不是看人在哪裡」的字句。
   - 研究紀錄 `verified_facts` 那一條的 `fact` 也帶著同一個推論，一併改掉，避免後面的輪次或翻譯把它改回去。
5. **「年化營收」與三種管道。**
   - 第 15 段加了定義：「年化營收（annualized revenue run rate，以當時的營收速度換算成一年的金額，不是一年實際收到的錢）」。FAQ 5 用短版。歸因仍是「OpenAI 在 2026 年 8 月底公布」。
   - 三種管道保留。description、第一段、summary 4 原本只列兩種，漏了「技術夥伴」，已補上。這是事實修改，見下文。

### 第一輪改過的 15 句（逐句回來源）

來源代號：A＝9/23 公告、H1＝〈Ads Manager Availability〉、H2＝〈Ads in ChatGPT〉、AUG＝8/31 公告。

| R1# | 位置 | 第一輪改成 | 判定 | 來源原文 |
| --- | --- | --- | --- | --- |
| 5 | p1 | 接下來可能陸續看到廣告，不是同一天全部開通 | CONFIRMED | H2 “Ads may appear for users on the Free and Go plans.”“We’re gradually rolling out ads to eligible users on the Free and Go plans in select regions.” |
| 16 | summary5 | 在 2026 年 8 月底公布、上線不到 200 天就達到的數字 | CONFIRMED | A “At the end of August, we announced that ChatGPT Ads had reached $1 billion in annualized revenue run rate in less than 200 days after launch.”；AUG 頁首 August 31, 2026 |
| 18 | p3 | 刪「公告寫，」→「這次是 ChatGPT 廣告擴及亞洲另外七個市場，台灣是其中之一」 | CONFIRMED | A 副標 “expands to seven additional markets across Asia”；本段歸因片語 2 個 |
| 25 | p5 | 以公告查核到…未見這項合作… | CONFIRMED（本輪依裁定 3 改寫為「公告沒有說明…」） | A 的 Shopee 引言只有 “we are pleased to extend this collaboration to Southeast Asia and Taiwan”，沒有投放內容、時程、條件 |
| 30 | p6 | 以這兩頁查核到…未見台灣使用者完成推出的時間表 | CONFIRMED（改寫為「這兩頁都沒有寫台灣使用者全面推出的時間表」） | A “will begin rolling out”；H2 “Availability will expand over time”；兩頁都沒有完成日期 |
| 34 | p8 | 說明中心也寫了廣告位置的限制： | CONFIRMED | H2 “Ads can appear below the end of a response.”“not eligible to appear near sensitive or regulated topics, including …” |
| 46 | p9 | 關掉某則廣告並提供回饋 | CONFIRMED | H2 “Dismiss ads and share feedback” |
| 51 | p11 | 廣告控制只提供給廣告已推出或即將推出地區的 Free 與 Go 使用者。 | CONFIRMED | H2 “Ad controls are available only to Free and Go users in regions where ads are available or will soon be available.”（連續字串） |
| 55 | h2[17] | 對台灣商家的影響：… | CONFIRMED（「影響」保留；後半依裁定 4 改） | A 行銷句 “brings that opportunity to more businesses” 不宜照搬 |
| 62 | p13 | 所在國家還沒開放前，先建立帳號也不會提前取得使用權限。 | CONFIRMED | H2 “Creating an account does not give you access before your country is supported.” |
| 63 | p14 | 以公告與說明中心查核到…未見台灣廣告主的價格… | CONFIRMED（改寫為「公告與說明中心都沒有寫…」） | 三頁詞界搜尋：price／pricing／currency／budget／minimum／billing 皆 0；“billed” 只在 H1 法律實體那句；A 的 “cost” 是 “low-cost access”；無台灣代理商 |
| 68 | p15 | 但沒有寫具體時程 | **CHANGED**（「具體時程」成立；同句掉了一項） | A “Over the next few months, we will continue to expand into new markets, build new formats, optimization tools, and measurement solutions.”：原句只寫「新廣告格式與量測工具」，漏「優化工具」且讀成完整清單 → 「新廣告格式、優化工具與成效量測方案」 |
| 73 | p16 | 以公告與說明中心查核到…未見台灣的個人化廣告設定狀態… | CONFIRMED（改寫為「公告與說明中心都沒有寫…」） | H2 “Personalized ads are not initially available in the European Economic Area (EEA) or Switzerland.”；H2 的 Taiwan 詞界 0 次；“regulat” 4 次都是 sensitive or regulated topics／verticals，不是主管機關 |
| 74 | p17 | 想確認最新規則… | CONFIRMED | H2 “If you’re eligible for the test, you’ll see clear in-product information.”：說明中心頁看不到個人帳號狀態 |
| 75 | p17 | 工具細節與計費方式，可以看下方連結的 5 月那篇整理。 | CONFIRMED | AUG “The introduction of Ads Manager in May”；第二個連結目標 zh-TW 標題「…5 月公告的工具、計費與鎖定機制」逐字相同，五語齊全 |

### 隨機抽查（第一輪其餘 CONFIRMED 97 條抽 33 條，`fc2_sample.py`，種子 20260926）

| R1# | 位置 | 判定 | 依據 |
| --- | --- | --- | --- |
| 2 | description 前半 | CONFIRMED | H2 “Ads may appear …”；A “Plus, Pro, and Enterprise subscriptions will remain ad-free.” |
| 3 | description 後半 | **CHANGED** | A “through the OpenAI Ads Solutions team, agency partners including …, and technology partners”：封閉三項清單，description 漏「技術夥伴」→ 補上（179 字） |
| 6 | p1 後半 | **CHANGED** | 同上，補「技術夥伴」 |
| 7 | p2 前半 | CONFIRMED（依裁定 1 改寫） | checked_on 2026-09-26 |
| 8 | p2 後半 | CONFIRMED（依裁定 1 改寫） | 本站自述；兩頁 Updated 行 |
| 11 | summary2 後半 | CONFIRMED（依裁定 3 去掉「查核日讀到的」） | H2 “Plus, Pro, Business, Enterprise, and Edu accounts will not have ads.”“under 18” |
| 17 | h2[3] | CONFIRMED | A “seven additional markets across Asia” |
| 19 | p3 | CONFIRMED | A “now available in over 60 countries” |
| 20 | p3 引文 | CONFIRMED | 連續字串；中譯忠實 |
| 24 | p5 | CONFIRMED | A Shopee 引言；職稱 “Executive Director, Brand and Growth Marketing, Shopee”，正文不寫姓名 |
| 28 | p6 | CONFIRMED（依裁定 3 改寫） | H2 同 11；「可能」＝may |
| 29 | p6 | CONFIRMED | H2 “I’m on a Go plan … If you’re on a paid plan …” |
| 31 | p7 | CONFIRMED | H2 “Ad testing started in the United States on February 9, 2026. We’re gradually rolling out …” |
| 35 | p8 | CONFIRMED | H2 “Temporary Chats will not show ads.”；including → 「這類」 |
| 36 | p8 | CONFIRMED | H2 “During this test, ads do not appear in the ChatGPT Atlas browser.” |
| 37 | table Free | CONFIRMED | eligible → 「限符合資格者」 |
| 38 | table Go | CONFIRMED | 同 29 |
| 39 | table Plus | CONFIRMED | A、H2 |
| 47 | p10 | CONFIRMED | H2 “won't use other chat threads, ads history or topics” |
| 49 | p10 引文 | CONFIRMED | “Ads-Free is a Free-plan option.” 連續字串；“(like Plus or Pro)” |
| 52 | p11 | CONFIRMED | H2 “retained for up to 30 days”（「最多」保留） |
| 53 | image.caption | CONFIRMED | 與研究紀錄 diagram.caption 逐字相同（checker 通過） |
| 57 | p12 | CONFIRMED | A “Self-service access through Ads Manager … is also available for eligible businesses.” |
| 64 | p14 | CONFIRMED | A “agency partners including dentsu …” |
| 66 | p15 | CONFIRMED | A “Tens of thousands of advertisers … with many reaching people across multiple countries.” |
| 70 | p16 | CONFIRMED | A “always clearly labeled and separate from ChatGPT’s answers” |
| 81 | faq2 | CONFIRMED | A |
| 82 | faq2 | CONFIRMED（依裁定 3 改寫） | H2 |
| 86 | faq3 | CONFIRMED | H2 “based on the context of your current chat thread” |
| 89 | faq4 | CONFIRMED | A 三項封閉清單 |
| 94 | faq5 | CONFIRMED（依裁定 5 加定義） | A “annualized revenue run rate”、“At the end of August” |
| 95 | faq5 | CONFIRMED | A 回顧句 |
| 100 | callout | CONFIRMED | A “will begin rolling out”；H2 “gradually … eligible … select regions” |

### 限定詞回掃（116 條全掃）

| 限定詞 | 原文 | 文章 | 結果 |
| --- | --- | --- | --- |
| may | Ads may appear；Ads-Free controls may only appear；you may not see these options；Ads can appear below | description、p1、p6、table、callout「可能」；p11 兩個「可能」；p8「可能出現」 | 保留 |
| gradually／begin rolling out | gradually rolling out；will begin rolling out | p1「陸續」、p3、p7、FAQ1、callout「逐步」 | 保留 |
| eligible | eligible users；eligible businesses；If you’re eligible for the test | p7、table、FAQ1；description、p1、p4、p12、summary4、FAQ4「符合資格」 | 保留（p1 使用者端沒寫「符合資格」，但對應的是 H2 首句 “Ads may appear for users on the Free and Go plans”，有「可能」，不改） |
| including | agency partners including；sensitive … topics, including … | p4「舉例包括…只是舉例」、p14；p8「這類」 | 保留 |
| up to | retained for up to 30 days | p11「最多」 | 保留 |
| select regions | in select regions | p7「特定地區」 | 保留 |
| during this test | During this test, ads do not appear in … Atlas | p8「測試期間」 | 保留 |
| where available | age prediction where available | p7「可用時的年齡預測」 | 保留 |
| over／more than／less than／tens of thousands | over 60；less than 200 days；Tens of thousands；many | 「超過」「不到」「數萬家」「許多」 | 保留 |
| 封閉清單 | Ads Solutions team, agency partners, and technology partners；new formats, optimization tools, and measurement solutions | description、p1、summary4 漏技術夥伴；p15 漏優化工具 | **已補** |

回掃沒有發現第一輪為了字數刪掉的但書（第一輪整體是加字，2,882 → 2,907）。

### 第二輪改動（內容包 21 處替換，研究紀錄 1 處）

事實修改（4 處）：

1. description：「透過 Ads Solutions 團隊、代理商，或符合資格的自助 Ads Manager」→「透過 Ads Solutions 團隊、代理商、技術夥伴，或符合資格的自助 Ads Manager」。來源：A “through the OpenAI Ads Solutions team, agency partners including …, and technology partners”。https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/
2. 第一段：「廣告解決方案團隊、代理商夥伴，或符合資格的自助 Ads Manager」→「廣告解決方案團隊、代理商夥伴、技術夥伴，或符合資格的自助 Ads Manager」。來源同上。
3. summary 4：同樣補「技術夥伴」；後半依裁定 2、3 改成「…說明中心的國家表把台灣列為已開放。」。來源：https://help.openai.com/en/articles/20001245-ads-manager-availability
4. 第 15 段：「推出新廣告格式與量測工具」→「推出新廣告格式、優化工具與成效量測方案」。來源：A “build new formats, optimization tools, and measurement solutions”。https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/

裁定實作（內容包其餘 17 處，研究紀錄 1 處）：

5. 第二段（裁定 1、3）：
   - 改前：這一篇的資料在 2026 年 9 月 26 日查核，讀了 OpenAI 這篇公告，以及說明中心〈Ads Manager Availability〉與〈Ads in ChatGPT〉兩頁查核當天讀到的版本；本站沒有實測 ChatGPT 廣告，也不提供投放或訂閱建議，這兩頁會持續更新，內容以查核當天讀到的版本為準。
   - 改後：無廣告方案的清單與開放自助投放的國家表都在 OpenAI 說明中心，頁面會更新，以下寫的是 2026 年 9 月 26 日的內容。本站沒有實測 ChatGPT 廣告，也不提供投放或訂閱建議。
   - 來源：https://help.openai.com/en/articles/20001047-ads-in-chatgpt
6. summary 2（裁定 3）：「；查核日讀到的說明中心頁面則多列出」→「；說明中心頁面則多列出」。
7. 第 5 段（裁定 3）：「；以公告查核到 2026-09-26 未見這項合作…」→「；公告沒有說明這項合作…」。
8. 第 6 段（裁定 3）：「查核日讀到的說明中心〈Ads in ChatGPT〉頁面列出更完整的清單」→「說明中心〈Ads in ChatGPT〉頁面列出更完整的清單」。
9. 第 6 段（裁定 3）：「；以這兩頁查核到 2026-09-26 未見台灣使用者完成推出的時間表。」→「；這兩頁都沒有寫台灣使用者全面推出的時間表。」
10. 表格列（裁定 3）：「說明中心（查核日版本）」→「說明中心」。
11. 表格 caption（裁定 3）：「以及查核日（2026 年 9 月 26 日）讀到的說明中心〈Ads in ChatGPT〉頁面」→「以及 2026 年 9 月 26 日的說明中心〈Ads in ChatGPT〉頁面」。
12. 第 4 節標題（裁定 4）：「對台灣商家的影響：自助資格看公司所在地，不是看人在哪裡」→「對台灣商家的影響：自助投放看法律實體所在國家」。
13. 第 12 段（裁定 2、3、4）：
    - 改前：說明中心〈Ads Manager Availability〉頁面解釋，自助資格看的是刊登廣告並被收費的法律實體所在國家，不是使用者或行銷人員本人在哪裡；查核日（2026-09-26）讀到的國家表裡，Taiwan 那一列的 Self-service availability 是 Available。
    - 改後：說明中心〈Ads Manager Availability〉頁面寫明，要使用自助 Ads Manager，刊登廣告並被收費的法律實體必須設在國家表列為開放的國家；國家表把台灣列為已開放自助投放（Available）。
    - 來源：H1 “Note: To use self-service Ads Manager, the legal entity that will advertise and be billed must be based in a country listed as available below.”；Taiwan｜Available。
14. 第 14 段（裁定 3）：「以公告與說明中心查核到 2026-09-26 未見台灣廣告主的價格、幣別、最低預算或計費方式，也未見列出…」→「公告與說明中心都沒有寫台灣廣告主的價格、幣別、最低預算或計費方式，也沒有列出…」。
15. 第 15 段（裁定 5）：「10 億美元的年化營收，是 OpenAI…」→「10 億美元的年化營收（annualized revenue run rate，以當時的營收速度換算成一年的金額，不是一年實際收到的錢），是 OpenAI…」。
16. 第 16 段（裁定 3）：「以公告與說明中心查核到 2026-09-26 未見台灣的個人化廣告設定狀態，也未見任何台灣主管機關、法規或個資法被提到。」→「公告與說明中心都沒有寫台灣的個人化廣告設定狀態，也沒有提到任何台灣主管機關、法規或個資法。」
17. FAQ 2（裁定 3）：「查核日讀到的說明中心頁面則列出」→「說明中心頁面則列出」。
18. FAQ 4（裁定 2、3、4）：
    - 改前：說明中心解釋，自助資格看的是刊登廣告並被收費的法律實體所在國家，查核日讀到的國家表裡 Taiwan 那一列標示 Available。
    - 改後：說明中心寫明，要自助投放，刊登廣告並被收費的法律實體必須設在國家表列為開放的國家，國家表把台灣列為已開放。
19. FAQ 5（裁定 5）：「（annualized revenue run rate）」→「（annualized revenue run rate，以當時的營收速度換算成一年的金額）」。
20. callout（裁定 3）：「查核日讀到的說明中心頁面另外列出」→「說明中心頁面另外列出」。
21. callout（裁定 3、4）：
    - 改前：企業能不能自助投放，看的是刊登並被收費的法律實體所在地，不是人在哪裡。查核到 2026 年 9 月 26 日為止，之後想確認最新狀態，請直接查 OpenAI 說明中心。
    - 改後：企業要自助投放，刊登廣告並被收費的法律實體必須設在國家表列為開放的國家。說明中心的清單會更新，最新狀態請直接查 OpenAI 說明中心。
22. 研究紀錄 `verified_facts`（法律實體那條）的 `fact`：
    - 改前：「…所在國家，不是使用者或行銷人員人在哪裡。」
    - 改後：「自助 Ads Manager 的資格：『刊登廣告並被收費的法律實體』必須設在國家表列為開放（available）的國家。頁面只寫這條規則，沒有寫『不是使用者或行銷人員本人在哪裡』這種對照，文章不寫這個對照（第二輪依協調者裁定刪除）。」
    - `verbatim_quote` 不變。

連帶檢查：
- summary ⊆ 正文：「技術夥伴」「已開放」都在正文。
- FAQ ⊆ 正文：FAQ 4 的規則句在第 12 段，FAQ 5 的定義在第 15 段。
- 圖解四格沒有數字；title、hero_label、diagram 不變，研究紀錄 `title`、`diagram.caption` 不變。
- description 179 字，句尾「（2026 年 9 月查證）。」。

### 本輪新寫的句子（自查）

- 第二段兩句：日期就是 checked_on；「頁面會更新」有 H2 “Availability may continue to evolve as testing expands.” 與兩頁的 Updated 行可依。
- 第 12 段、FAQ 4、callout 的規則句：H1 Note 原句的中譯。
- 否定句：
  - 第 5 段：A 沒有 Shopee 的投放內容、時程或條件。
  - 第 6 段：兩頁沒有完成日期。
  - 第 14 段：詞界搜尋三頁為 0。
  - 第 16 段：H2 只點名 EEA 與瑞士，沒有主管機關。
- 年化營收的定義：術語定義，不是 sources[] 的事實（見待決事項）。

### 讀者優先與界線

- 「本文」0 次；「查核日讀到的」「查核當天」「查核到」在正文、summary、表格、FAQ、callout 都是 0 次。圖片 caption 的「查核日 2026 年 9 月 26 日」是出處行，保留。
- 歸因片語：開場段 0 個。正文段最多 2 個（第 3、6、10、16 段各 2 個），第 16 段另有一個指名頁面的否定句，與第一輪的算法相同。
- 界線：沒有購買、投放或訂閱建議；「機會」語氣已由第一輪拿掉；廠商數字與原則句都有歸因；沒有 finance 主題，沒有免責 callout，只有一個一般 callout；沒有推定台灣使用者端已全面開通；使用者端推出與廣告主自助資格分開寫。
- 結尾連結：兩個 text 與目標內容包的 zh-TW title 逐字相同，兩個目標都有 zh-TW、en、ja、ko、zh-CN。

### 待決事項（給協調者）

1. 第 13 段「能不能用自助功能要看公司所在國家」對應 H1 “access depends on your country”。「公司」與同頁的法律實體規則一致，但不是字面；字面寫法是「要看所在國家」。沒有改。
2. 年化營收的定義（第 15 段、FAQ 5）是依裁定 5 加的術語解釋，sources[] 沒有一頁寫這個定義。
3. 否定句現在只指名頁面、不重複日期（裁定 3）。SECOND-ROUND.md 第 4 條原本要「頁面＋查核日」，現在由第二段唯一的 as-of 句替全文標日期。
4. 活頁面發布當天要重讀（DELTA-4-8 第 7 條）：14:48Z 時 Availability 的 updatedAt 仍是 2026-09-25T21:12:52Z（Taiwan｜Available），Ads in ChatGPT 仍是 2026-09-26T10:04:51Z。
5. 第一輪留下的風格項（“Ads Manager”“Ads-Free” 第一次出現沒有中文）不在本輪裁定內，沒有動。

### 來源與指示的衝突

- 裁定 4 把規則轉述成「the legal entity that registers and is billed」，H1 原文是 “the legal entity that will **advertise** and be billed”。以來源為準，文章寫「刊登廣告並被收費的法律實體」，沒有寫「註冊」。
- SECOND-ROUND.md 要報告附在同一檔、只准三個檔，FACTCHECK-48 與指派訊息要另開 `-round2.md`。依指派訊息。

### 自檢（原樣）

```
OK ai-news-chatgpt-ads-taiwan-20260923 zh-TW paragraphs 2811
exit=0
```

```
ai-news-chatgpt-ads-taiwan-20260923
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-chatgpt-ads-taiwan-20260923/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-chatgpt-ads-taiwan-20260923/diagram-1.svg
1 entries checked
exit=1
```

引文比對：`TOTAL 49 FAIL 0`（`_tools/<slug>/fc2_quotes_final.log`）。本輪的腳本與輸出都在 `<WORK>/_tools/ai-news-chatgpt-ads-taiwan-20260923/fc2_*`；改前的內容包與研究紀錄備份是同目錄的 `fc2_pack_before.json`、`fc2_record_before.json`。
