# 查核報告（第一輪）：ai-news-chatgpt-ads-taiwan-20260923

- 查核者：獨立查核代理，第一輪（claude-opus-5-5）；沒有參與撰稿。
- 查核日：2026-09-26（台北）；重抓時間 2026-09-26T14:32–14:33Z。
- 規格：`<WORK>/FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/ai/FACTCHECK.md`、DELTA-4-8（全）、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF 十二條錯誤型態。
- 本報告放在 `<WORK>/factcheck/`（FACTCHECK-48 的路徑）；DELTA-4-8 第 9 條要求進 repo 的 `docs/news-2026-batch-4/factcheck-draft/<slug>-round1.md`，由協調者複製（查核者只准改內容包與研究紀錄）。

## 摘要

- 主張：116 條；CONFIRMED 103（其中 6 條內容正確但改了措辭：4 條否定句補上出處、1 條廠商規則補歸因、1 條歸因片語超量）、CHANGED 7、NOT FOUND（已改寫）2、OUT OF SCOPE 4（FAQ 問句）。
- 事實修改 8 處（#5、#16、#46、#51、#62、#68、#74、#75），界線修改 1 處（#55），措辭修改 6 處（#18、#25、#30、#34、#63、#73）；內容包共 15 處文字替換，研究紀錄只加 `factcheck` 物件（紀錄本身沒有發現與來源不符的地方，`verified_facts` 49 條引文今天逐字比對 49／49 通過）。
- 骨幹論述沒有動：逐步推出、兩份無廣告清單各自歸因、關個人化不等於沒廣告、自助資格看法律實體所在地、10 億美元是 8 月底的舊數字。
- 自檢：`check_article.py` → `OK ai-news-chatgpt-ads-taiwan-20260923 zh-TW paragraphs 2907`（exit 0；改前 2882）；`pack_cli lint` 只有 `raw_internal_url`（warning）與兩條 `image_missing`（error，出圖前預期），與撰稿者的 lint 輸出相同。

## 協調者指定的六點

1. **逐步推出**：公告 “Starting today, ChatGPT Ads will begin rolling out across … Taiwan.”，說明中心 “We’re gradually rolling out ads to eligible users on the Free and Go plans in select regions.”——標題「開始在台灣逐步推出」成立。第一段原本寫 Free／Go 使用者「會陸續…看到廣告」，掉了 may，已改成「可能陸續看到廣告，不是同一天全部開通」（#5）。
2. **無廣告方案**：公告只列 Plus、Pro、Enterprise；〈Ads in ChatGPT〉英文版今天列 Plus、Pro、Business、Enterprise、Edu（updatedAt 2026-09-26T10:04:51Z＝台北 18:04），正文、表格、FAQ、callout 都分別歸因。Go 是付費方案而仍可能看到廣告（Help 以 “If you’re on a paid plan” 回答 Go 的提問）。Ads-Free 是 Free 方案選項，英文 “Ads-Free is a Free-plan option.”；zh-Hant 版今天仍把 “Tap Change plan to go ad-free.” 誤譯成「輕觸變更方案以享受 Go 無廣告體驗」，文章沒有採用。
3. **自助資格**：“the legal entity that will advertise and be billed must be based in a country listed as available below”；今天國家表 Taiwan｜Available（updatedAt 2026-09-25T21:12:52Z＝台北 9/26 05:12）。文章把使用者端推出與廣告主端資格分開寫。另修掉一句把「建立帳號不會提前取得權限」套到台灣商家身上的錯置（#62），台灣列是 Available。
4. **OpenAI 自報數字與原則**：60 國、數萬家廣告主、10 億美元年化營收都歸因給 OpenAI；10 億美元寫明是 8 月底公布、不是新數字、不是「年營收／已賺進」。摘要第 5 句原本寫成「上線不到 200 天時公布」，原文是「不到 200 天達到、8 月底公布」，已改（#16）。「對話不給廣告主、不賣資料、不影響回答」寫成 OpenAI 的宣示，並寫明本站無法查證。
5. **引文**：兩句英文引文逐字（程式比對連續字串通過）。改寫成間接引述的句子逐一比對：Shopee 引言（#24）、廣告原則（#69–71、#97）、關個人化後仍依目前對話顯示廣告（#47、#86）、Go 使用 Ads-Free 的兩條路（#49），都忠實。撰稿者沒有留下「哪兩句被改寫」的紀錄，以上是正文所有間接引述。
6. **台灣先前被排除**：全文沒有這種句子，只寫台灣是公告說的 “seven additional markets” 之一，sources[] 撐得住。沒有改。

## 重抓結果

| # | URL | HTTP | 轉址 | bytes（落地檔） | body | 備註 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/ | 200 | 0 | 386,726 | 正文 | 頁首 September 23, 2026；今天沒有 403 |
| 2 | https://help.openai.com/en/articles/20001245-ads-manager-availability | 200 | 0 | 63,895 | 正文 | 自印 Updated: 17 hours ago；Taiwan｜Available |
| 3 | https://help.openai.com/en/articles/20001047-ads-in-chatgpt | 200 | 0 | 98,313 | 正文 | 自印 Updated: 4 hours ago |
| 4 | https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/ | 200 | 0 | 401,787 | 正文 | 頁首 August 31, 2026 |
| — | https://openai.com/news/rss.xml | 200 | 0 | 750,532 | feed | 1,230 筆、最新 2026-09-25T19:00Z；本篇 pubDate 02:00:00 GMT（日期依據，不在 sources[]） |
| — | help.openai.com zh-hant 兩頁 | 200 | 0 | 99,737／65,179 | 正文 | 兩語比對；國家表 zh-Hant 自印機器翻譯 |

四頁抽出的文字與研究代理 13:45–13:51Z 那份逐字相同（bytes 差異只在頁面動態 token）。

## 改掉的 15 處（原文 → 改成，來源原文，理由）

1. #5 第一段：「接下來會陸續、不是同一天全部看到廣告」→「接下來可能陸續看到廣告，不是同一天全部開通」。H2 “Ads may appear for users on the Free and Go plans.”“gradually rolling out ads to eligible users … in select regions”。掉了 may／eligible。https://help.openai.com/en/articles/20001047-ads-in-chatgpt
2. #16 摘要第 5 句：「在 2026 年 8 月底、上線不到 200 天時公布的數字」→「在 2026 年 8 月底公布、上線不到 200 天就達到的數字」。A “At the end of August, we announced that ChatGPT Ads had reached $1 billion in annualized revenue run rate in less than 200 days after launch.” https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/
3. #18 第 3 段：刪「公告寫，」。三個歸因片語 → 兩個（協調者核准）。同上 URL。
4. #25 第 5 段：「以查核到 2026-09-26 未見這項合作」→「以公告查核到 2026-09-26 未見這項合作」。否定句補出處。同上 URL。
5. #30 第 6 段：「以查核到 2026-09-26 未見台灣使用者完成推出的時間表」→「以這兩頁查核到…」。https://help.openai.com/en/articles/20001047-ads-in-chatgpt
6. #34 第 8 段：「廣告出現的位置也有限制：」→「說明中心也寫了廣告位置的限制：」。敏感話題規則是 OpenAI 對自家流程的說法，整段原本沒有歸因。同上 URL。
7. #46 第 9 段：「關掉某則廣告並回饋原因」→「關掉某則廣告並提供回饋」。H2 “Dismiss ads and share feedback”。同上 URL。
8. #51 第 11 段：「台灣使用者要等廣告推送到自己帳號，才會看到對應控制項。」→「廣告控制只提供給廣告已推出或即將推出地區的 Free 與 Go 使用者。」來源沒有前者，原文是 “Ad controls are available only to Free and Go users in regions where ads are available or will soon be available.” 同上 URL。
9. #55 第 4 節標題：「對台灣商家的機會」→「對台灣商家的影響」。照搬 OpenAI 行銷句 “brings that opportunity to more businesses”，AI 垂直不寫推薦語氣。https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/
10. #62 第 13 段：「台灣商家先建立帳號，也不會因此提前取得使用權限。」→「所在國家還沒開放前，先建立帳號也不會提前取得使用權限。」H2 “Creating an account does not give you access before your country is supported.”；台灣列是 Available。https://help.openai.com/en/articles/20001047-ads-in-chatgpt
11. #63 第 14 段：「以查核到 2026-09-26 未見台灣廣告主」→「以公告與說明中心查核到 2026-09-26 未見台灣廣告主」。https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/
12. #68 第 15 段：「但沒有寫時程」→「但沒有寫具體時程」。A “Over the next few months, we will continue to expand …”。同上 URL。
13. #73 第 16 段：「以查核到 2026-09-26 未見台灣的個人化廣告設定狀態」→「以公告與說明中心查核到…」。H2 只點名 EEA 與瑞士。https://help.openai.com/en/articles/20001047-ads-in-chatgpt
14. #74 第 17 段：「想確認自己帳號目前是什麼狀態」→「想確認最新規則」。H2 “If you’re eligible for the test, you’ll see clear in-product information.” 說明中心看不到個人帳號狀態。同上 URL。
15. #75 第 17 段：「完整的操作流程與計費方式，可以看 OpenAI 當時的公告。」→「工具細節與計費方式，可以看下方連結的 5 月那篇整理。」sources[] 只撐 “The introduction of Ads Manager in May”。https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/

改動連帶檢查：摘要數字都在正文；description、title、表格、圖、callout 不受影響；研究紀錄 `title`、`diagram.caption` 不變；段落 2,882 → 2,907 字。

## 界線檢查（AI 垂直）

- 購買建議、推薦式比價：沒有（「機會」標題已改）。ads.openai.com 的抵用金優惠沒有寫（紀錄排除）。
- 沒歸因的廠商宣稱：原則句、數字、敏感話題規則都已歸因；第 8 段補上歸因。
- 預告／分批開放狀態：標題、第一段、第 3 段、FAQ 1、callout 都寫「開始逐步推出」；Ads-Free 的 “may only appear in regions where ads are being tested” 保留在第 11 段。
- 沒有免責 callout、沒有 finance 主題。

## 讀者優先檢查

- 「本文」0 次；「這一篇」1 次（第二段）。
- 歸因片語：開場段 1 個；改後每個正文段 ≤2 個（第 3 段原本 3 個，已改）。
- description 174 字，句尾「（2026 年 9 月查證）。」；title、description、summary 沒有選題數。
- 未改、留給協調者看的風格事項：第二段「讀了 OpenAI 這篇公告，以及說明中心…兩頁查核當天讀到的版本」是查證敘述（同批已發布篇也有同樣寫法）；「查核日讀到的」在正文、表格、FAQ、callout 出現多次；欄名 “Self-service availability” 進了正文（撰稿規格說官方頁欄名不進正文）；“Ads Manager”“Ads-Free” 第一次出現沒有中文。

## 待決事項（給協調者）

1. 「年化營收」：紀錄 `must_not_write` 允許「年化營收」、禁止「年營收／已賺進」，FAQ 5 另附英文原詞，保留。若協調者連「營收」二字都不要，字面譯法是「年化營收運行率」（摘要 5、第 15 段、FAQ 5 與其問句）。
2. 「不是使用者或行銷人員本人在哪裡」（第 12 段、第 4 節標題、callout）：是由法律實體標準推出的對照，國家表頁沒有逐字寫這個否定。因為紀錄 `verified_facts` 有、指派訊息也是同一讀法，保留。
3. 「三種管道」：數的是公告裡的封閉三項清單（自助是下一句的第四條路），保留。
4. 活文件：兩個說明中心頁面發布當天要重讀（DELTA-4-8 第 7 條）；Business／Edu 與 Taiwan＝Available 都是 2026-09-26 的快照。

## 來源與指示的衝突

- 沒有。協調者列的六點都與今天讀到的來源一致。

## 完整主張表

來源代號：A＝9/23 公告、H1＝Help〈Ads Manager Availability〉、H2＝Help〈Ads in ChatGPT〉、AUG＝8/31 公告、FEED＝openai.com/news/rss.xml（不在 sources[]，只當日期依據）、PACK＝目標內容包、REC＝研究紀錄。主張文字是**改前**的草稿。

| # | 位置 | 主張（改前） | 判定 | 來源 | 依據／處理 |
| --- | --- | --- | --- | --- | --- |
| 1 | title | ChatGPT 廣告開始在台灣逐步推出：哪些方案會看到、能怎麼控制、商家怎麼買 | CONFIRMED | A, H2 | “will begin rolling out”；Help “We’re gradually rolling out ads to eligible users … in select regions”。標題「開始在台灣逐步推出」成立。 |
| 2 | description | OpenAI 於 2026 年 9 月 23 日宣布 ChatGPT 廣告開始在台灣逐步推出，Free 與 Go 方案的使用者可能陸續看到廣告，Plus、Pro 等無廣告方案不受影響； | CONFIRMED | A, H2 | “Ads may appear for users on the Free and Go plans”；公告 “Plus, Pro, and Enterprise subscriptions will remain ad-free”。 |
| 3 | description | 台灣企業也可以透過 Ads Solutions 團隊、代理商，或符合資格的自助 Ads Manager 在 ChatGPT 上投放廣告（2026 年 9 月查證）。 | CONFIRMED | A | “through the OpenAI Ads Solutions team, agency partners … Self-service access through Ads Manager … eligible businesses”。句尾只有「（2026 年 9 月查證）」。 |
| 4 | p1 | OpenAI 在 2026 年 9 月 23 日宣布，ChatGPT 廣告從當天起在台灣開始逐步推出，同時擴及印尼、馬來西亞、菲律賓、新加坡、泰國與越南。 | CONFIRMED | A, FEED | 頁首 “September 23, 2026”；feed pubDate Wed, 23 Sep 2026 02:00:00 GMT＝台北 10:00，同日。 |
| 5 | p1 | 對台灣讀者而言：使用 Free 或 Go 方案的人，接下來會陸續、不是同一天全部看到廣告； | CHANGED | H2 | 掉了 may：Help “Ads may appear …”“gradually rolling out ads to eligible users”。「會…看到廣告」→「可能陸續看到廣告，不是同一天全部開通」。 |
| 6 | p1 | 台灣企業與代理商現在則可以透過 OpenAI 的廣告解決方案團隊、代理商夥伴，或符合資格的自助 Ads Manager，在 ChatGPT 上刊登廣告。 | CONFIRMED | A, H1 | 公告三管道＋自助；國家表 Taiwan＝Available（今天 14:32Z）。 |
| 7 | p2 | 這一篇的資料在 2026 年 9 月 26 日查核，讀了 OpenAI 這篇公告，以及說明中心〈Ads Manager Availability〉與〈Ads in ChatGPT〉兩頁查核當天讀到的版本； | CONFIRMED | REC | checked_on 2026-09-26 與研究紀錄、四條 source 一致。讀者優先註記：「讀了…兩頁查核當天讀到的版本」是查證敘述（同批已發布篇也這樣寫，未改）。 |
| 8 | p2 | 本站沒有實測 ChatGPT 廣告，也不提供投放或訂閱建議，這兩頁會持續更新，內容以查核當天讀到的版本為準。 | CONFIRMED | H1, H2 | 本站自述；兩頁皆活文件（updatedAt 9/25 21:12Z、9/26 10:04Z）。 |
| 9 | summary1 | OpenAI 在 2026 年 9 月 23 日宣布，ChatGPT 廣告開始在台灣逐步推出，同時擴及印尼、馬來西亞、菲律賓、新加坡、泰國與越南，官方表示現在已在超過 60 個國家提供。 | CONFIRMED | A | 副標 “now available in more than 60 countries”，歸因「官方表示」。 |
| 10 | summary2 | 公告寫，廣告只會顯示給 Free 與 Go 方案的使用者，Plus、Pro 與 Enterprise 訂閱維持無廣告； | CONFIRMED | A | “ads will be shown only to users on the Free and Go plans. Plus, Pro, and Enterprise subscriptions will remain ad-free.” |
| 11 | summary2 | 查核日讀到的說明中心頁面則多列出 Business 與 Edu 兩種無廣告方案，被判定為未滿 18 歲的帳號也不會看到廣告。 | CONFIRMED | H2 | “Plus, Pro, Business, Enterprise, and Edu accounts will not have ads.”“We do not show ads to accounts identified as belonging to users under 18”。 |
| 12 | summary3 | 使用者可以在設定裡關閉廣告個人化，但說明中心寫明，關掉之後仍會依目前對話的脈絡顯示廣告； | CONFIRMED | H2 | “you will still see ads based on the context of your current chat thread”。 |
| 13 | summary3 | 想要真正沒有廣告，Free 方案可以改用 Ads-Free 體驗，但訊息數等使用上限會降低。 | CONFIRMED | H2 | “switch to an Ads-Free experience … lower usage limits … fewer messages”。 |
| 14 | summary4 | 台灣企業可以透過 OpenAI 的 Ads Solutions 團隊、代理商夥伴，或符合資格的自助 Ads Manager 投放廣告； | CONFIRMED | A | 同 3。 |
| 15 | summary4 | 自助資格看的是刊登並被收費的法律實體所在國家，查核日讀到的國家表把 Taiwan 列為 Available。 | CONFIRMED | H1 | “the legal entity that will advertise and be billed must be based in a country listed as available”；Taiwan｜Available。 |
| 16 | summary5 | 10 億美元的年化營收，是 OpenAI 在 2026 年 8 月底、上線不到 200 天時公布的數字，9 月 23 日的公告只是回顧，不是這次的新數字。 | CHANGED | A, AUG | 原文 “had reached $1 billion … in less than 200 days after launch”＋“At the end of August, we announced”：不到 200 天是「達到」，不是「公布時」。改成與正文第 15 段同句。 |
| 17 | h2[3] | 發生了什麼：台灣是這次亞洲擴張新增的七個市場之一 | CONFIRMED | A | “expands to seven additional markets across Asia”。 |
| 18 | p3 | 公告寫，這次是 ChatGPT 廣告擴及亞洲另外七個市場，台灣是其中之一； | CONFIRMED | A | 內容正確；本段三個歸因片語，刪掉「公告寫，」（協調者核准的讀者優先修改）。 |
| 19 | p3 | OpenAI 表示現在已在超過 60 個國家提供。 | CONFIRMED | A | “now available in over 60 countries”，已歸因。 |
| 20 | p3 | 公告原文寫「Starting today, ChatGPT Ads will begin rolling out across Indonesia, Malaysia, the Philippines, Singapore, Thailand, Vietnam, and Taiwan.」（從今天開始，廣告將開始在印尼、馬來西亞、菲律賓、新加坡、泰國、越南與台灣逐步推出），是逐步推出，不是當天全面開通。 | CONFIRMED | A | 引文逐字（程式比對連續字串通過）；中譯忠實，「逐步推出」＝rolling out。 |
| 21 | p4 | OpenAI 表示，這次擴張接在亞太先前在澳洲、紐西蘭、日本、南韓與印度推出之後。 | CONFIRMED | A | “follows Asia Pacific launches in Australia, New Zealand, Japan, South Korea and India”。 |
| 22 | p4 | 廣告主可透過三種管道購買：Ads Solutions 團隊、代理商夥伴（公告舉例包括 dentsu、Havas Media、Omnicom Media、Publicis Groupe 與 WPP，只是舉例），以及技術夥伴； | CONFIRMED | A | 三項是封閉清單（through A, B, and C）；代理商名單以 including 起頭並註明舉例。「三種」是數封閉清單，見待決事項。 |
| 23 | p4 | 符合資格的企業也能用 Ads Manager 自助購買。 | CONFIRMED | A | “Self-service access through Ads Manager … is also available for eligible businesses.” |
| 24 | p5 | Shopee 品牌與成長行銷執行董事在公告裡表示，繼巴西推出 ChatGPT Ads 之後，把與 OpenAI 的合作延伸到東南亞與台灣； | CONFIRMED | A | Shopee 引言改寫成間接引述：“Following the launch of ChatGPT Ads in Brazil, we are pleased to extend this collaboration to Southeast Asia and Taiwan” ——忠實；只寫職稱、不寫姓名。 |
| 25 | p5 | 以查核到 2026-09-26 未見這項合作實際會投放什麼廣告、何時開始，或合作的條件。 | CONFIRMED | A | 否定句沒有指出頁面：補成「以公告查核到…未見」；公告只有引言，無投放內容、時程、條件。 |
| 26 | h2[7] | 對台灣使用者的影響：誰會看到廣告、誰不會 | CONFIRMED | A, H2 | — |
| 27 | p6 | 公告寫，和既有市場一樣，廣告只會顯示給 Free 與 Go 方案的使用者，Plus、Pro 與 Enterprise 訂閱維持無廣告。 | CONFIRMED | A | “As in our existing markets …”。 |
| 28 | p6 | 查核日讀到的說明中心〈Ads in ChatGPT〉頁面列出更完整的清單：Free 與 Go 方案的使用者「可能」看到廣告，Plus、Pro、Business、Enterprise 與 Edu 帳號不會有廣告，比公告多列了 Business 與 Edu。 | CONFIRMED | H2 | 英文版清單＋“may”，查核日版本（updatedAt 2026-09-26T10:04:51Z）。與公告各自歸因。 |
| 29 | p6 | Go 雖是付費方案，仍在可能出現廣告的名單上； | CONFIRMED | H2 | “I’m on a Go plan—can I use Ads-Free? … If you’re on a paid plan …”：Go 是付費方案且在可能出現廣告名單。 |
| 30 | p6 | 以查核到 2026-09-26 未見台灣使用者完成推出的時間表。 | CONFIRMED | A, H2 | 否定句沒有指出頁面：補成「以這兩頁查核到…未見」；兩頁都沒有完成日期（“Availability will expand over time”）。 |
| 31 | p7 | 說明中心寫，廣告測試從 2026 年 2 月 9 日在美國開始，OpenAI 正對特定地區、符合資格的 Free 與 Go 使用者逐步推出； | CONFIRMED | H2 | “Ad testing started in the United States on February 9, 2026. We’re gradually rolling out ads to eligible users on the Free and Go plans in select regions.” |
| 32 | p7 | 符合測試資格會在 ChatGPT 產品裡看到明確說明。 | CONFIRMED | H2 | “If you’re eligible for the test, you’ll see clear in-product information.” |
| 33 | p7 | 被判定為未滿 18 歲的帳號不會看到廣告，依據是帳號層級的年齡資訊與可用時的年齡預測。 | CONFIRMED | H2 | “based on account-level age information and age prediction where available”。 |
| 34 | p8 | 廣告出現的位置也有限制：可能出現在回答結尾下方，清楚標示為贊助（sponsored），並與回答在視覺上分開； | CONFIRMED | H2 | “Ads can appear below the end of a response … clearly labeled as sponsored and visually separated”。整段原本沒有歸因，而敏感話題規則是 OpenAI 對自家流程的說法（紀錄 is_vendor_claim=true）：句首改「說明中心也寫了廣告位置的限制」。 |
| 35 | p8 | 暫時對話（Temporary Chats）不會顯示廣告，也不會出現在個人健康、心理健康或政治這類敏感或受規範話題旁； | CONFIRMED | H2 | “Temporary Chats will not show ads.”“not eligible to appear near sensitive or regulated topics, including personal health, mental health, or politics”——「這類」保留了 including。 |
| 36 | p8 | 測試期間，ChatGPT Atlas 瀏覽器裡也不會出現廣告。 | CONFIRMED | H2 | “During this test, ads do not appear in the ChatGPT Atlas browser.” |
| 37 | table.r1 | Free ｜ 可能出現，逐步推出、限符合資格者 ｜ 公告、說明中心 | CONFIRMED | A, H2 | — |
| 38 | table.r2 | Go ｜ 可能出現（付費方案仍在此清單） ｜ 公告、說明中心 | CONFIRMED | A, H2 | — |
| 39 | table.r3 | Plus ｜ 無廣告 ｜ 公告、說明中心 | CONFIRMED | A, H2 | — |
| 40 | table.r4 | Pro ｜ 無廣告 ｜ 公告、說明中心 | CONFIRMED | A, H2 | — |
| 41 | table.r5 | Enterprise ｜ 無廣告 ｜ 公告、說明中心 | CONFIRMED | A, H2 | — |
| 42 | table.r6 | Business、Edu ｜ 無廣告 ｜ 說明中心（查核日版本） | CONFIRMED | H2 | 公告沒有列 Business、Edu（頁尾導覽的 ChatGPT Business 不是方案清單）。 |
| 43 | table.caption | 整理自 OpenAI 2026 年 9 月 23 日公告，以及查核日（2026 年 9 月 26 日）讀到的說明中心〈Ads in ChatGPT〉頁面； | CONFIRMED | A, H2 | caption ≤200 字。 |
| 44 | table.caption | Business 與 Edu 是說明中心版本才列出的無廣告方案。 | CONFIRMED | H2 | — |
| 45 | h2[12] | 使用者能怎麼控制：關掉個人化不等於沒有廣告 | CONFIRMED | H2 | “Turning personalization off can make ads less tailored, but it doesn’t remove ads.” |
| 46 | p9 | 說明中心寫，廣告控制在「設定」裡（英文版寫 Settings > Ad Controls，同頁另一處寫 Settings → Ads controls，字樣可能因平台而異），可以關閉廣告個人化、關掉某則廣告並回饋原因、查看為什麼出現某則廣告，以及清除用來投放廣告的資料。 | CHANGED | H2 | 原文 “Dismiss ads and share feedback”，沒有說回饋「原因」：「回饋原因」→「提供回饋」。 |
| 47 | p10 | 但關掉個人化不等於沒有廣告：說明中心明寫，關掉後仍會依對話脈絡看到廣告，只是不再用其他對話、廣告紀錄或主題挑選。 | CONFIRMED | H2 | “won't use other chat threads, ads history or topics”。 |
| 48 | p10 | 想真正沒有廣告，Free 方案可改用 Ads-Free 體驗，代價是使用上限較低、可用功能較少，例如訊息數變少、不能用圖片生成或深度研究。 | CONFIRMED | H2 | “fewer messages and no access to some tools like image generation or deep research”。 |
| 49 | p10 | 說明中心寫「Ads-Free is a Free-plan option.」（Ads-Free 是 Free 方案才有的選項），Go 要用它得先切回 Free，或升級到本身無廣告的方案，例如 Plus 或 Pro。 | CONFIRMED | H2 | 引文逐字；Go 的兩條路 “switch back to Free … or upgrade to a plan that’s already ad-free (like Plus or Pro)”。zh-Hant 版「享受 Go 無廣告體驗」的誤譯沒有被採用。 |
| 50 | p11 | 說明中心也提醒，廣告與 Ads-Free 控制項「可能」只出現在正在測試廣告的地區，不符合資格的使用者可能看不到這些選項； | CONFIRMED | H2 | “Ads (and Ads-Free controls) may only appear in regions where ads are being tested. If you’re not eligible for the ads test, you may not see these options.” |
| 51 | p11 | 台灣使用者要等廣告推送到自己帳號，才會看到對應控制項。 | NOT FOUND | H2 | 來源沒有「台灣使用者要等廣告推送到自己帳號才會看到控制項」；原文反而是 “Ad controls are available only to Free and Go users in regions where ads are available or will soon be available.” 改寫成這句。 |
| 52 | p11 | 刪除廣告資料後，最多再保留 30 天才會從伺服器移除。 | CONFIRMED | H2 | “retained for up to 30 days before being removed from our servers”（保留「最多」）。 |
| 53 | image.caption | 整理自 OpenAI 2026 年 9 月 23 日公告與說明中心兩頁，查核日 2026 年 9 月 26 日。 | CONFIRMED | A, H1, H2 | 與研究紀錄 diagram.caption 逐字相同。 |
| 54 | image.alt | 四格圖解：ChatGPT 廣告到台灣的四件事，分別是誰會看到、誰沒有廣告、怎麼控制與商家怎麼買 | CONFIRMED | REC | 描述四格圖解，與 diagram.nodes 一致。 |
| 55 | h2[17] | 對台灣商家的機會：自助資格看公司所在地，不是看人在哪裡 | CHANGED | A | AI 垂直界線（推薦／宣傳語氣）：「機會」是照搬 OpenAI 行銷句 “brings that opportunity to more businesses”，改「影響」，與第 2 節標題對稱。 |
| 56 | p12 | 公告寫，廣告主可透過三條管道投放：Ads Solutions 團隊、代理商夥伴，以及技術夥伴； | CONFIRMED | A | 同 22。 |
| 57 | p12 | 自助購買則透過 Ads Manager，開放給符合資格的企業。 | CONFIRMED | A | 同 23。 |
| 58 | p12 | 說明中心〈Ads Manager Availability〉頁面解釋，自助資格看的是刊登廣告並被收費的法律實體所在國家，不是使用者或行銷人員本人在哪裡； | CONFIRMED | H1 | 法律實體標準照原文；「不是使用者或行銷人員本人在哪裡」是由此推出的對照，頁面沒有逐字寫（見待決事項）。 |
| 59 | p12 | 查核日（2026-09-26）讀到的國家表裡，Taiwan 那一列的 Self-service availability 是 Available。 | CONFIRMED | H1 | 今天國家表 Taiwan｜Available。讀者優先註記：欄名 Self-service availability 進了正文（未改）。 |
| 60 | p13 | 說明中心也提醒，建立帳號和取得自助資格是兩回事：能不能用自助功能要看公司所在國家； | CONFIRMED | H1 | “Account creation and self-service availability are separate: access depends on your country.” |
| 61 | p13 | 標示 Coming Soon 或沒有列在表上，代表自助還沒開放，仍可先到 ads.openai.com 註冊，開放時會收到通知。 | CONFIRMED | H1 | “If your country is marked Coming Soon or isn’t listed … You can still sign up for an account at ads.openai.com and we'll notify you”。 |
| 62 | p13 | 台灣商家先建立帳號，也不會因此提前取得使用權限。 | CHANGED | H2, H1 | 原文 “Creating an account does not give you access before your country is supported.” 是一般規則；台灣列是 Available，不能寫成台灣商家的限制。改「所在國家還沒開放前，先建立帳號也不會提前取得使用權限」。 |
| 63 | p14 | 以查核到 2026-09-26 未見台灣廣告主的價格、幣別、最低預算或計費方式，也未見列出台灣本地的代理商或技術夥伴名字； | CONFIRMED | A, H1, H2 | 否定句沒有指出頁面：補成「以公告與說明中心查核到…未見」；三頁詞界比對無 price／currency／budget／minimum，也無台灣代理商。 |
| 64 | p14 | 代理商名單是「包括」（including）起頭的舉例，不是完整名單。 | CONFIRMED | A | “agency partners including dentsu …”。 |
| 65 | h2[21] | 數字與界限：哪些是官方自報的、哪些沒有說 | CONFIRMED | — | — |
| 66 | p15 | OpenAI 在公告裡提到的幾個數字都是公司自己公布的自報數字：現在有數萬家廣告主在 ChatGPT 投放廣告，許多同時觸及多個國家的使用者； | CONFIRMED | A | “Tens of thousands of advertisers … with many reaching people across multiple countries”，已歸因為自報。 |
| 67 | p15 | 10 億美元的年化營收，是 OpenAI 在 2026 年 8 月底公布、上線不到 200 天就達到的數字，9 月 23 日的公告只是回顧，不是新數字。 | CONFIRMED | A, AUG | “At the end of August, we announced …”；8/31 頁首 August 31, 2026。「年化營收」照紀錄允許的譯法，並寫明不是新數字。 |
| 68 | p15 | OpenAI 也表示，接下來幾個月會持續擴展新市場、推出新廣告格式與量測工具，但沒有寫時程。 | CHANGED | A | 原文有時間框架 “Over the next few months”（同句已寫「接下來幾個月」），「沒有寫時程」自相矛盾：改「沒有寫具體時程」。 |
| 69 | p16 | 公告裡也做了幾項宣示：對話不會提供給廣告主，也不會出售使用者資料； | CONFIRMED | A | “we keep conversations private from advertisers and never sell customer data”，已歸因為宣示。 |
| 70 | p16 | 廣告一律清楚標示，並與 ChatGPT 的回答分開； | CONFIRMED | A | “always clearly labeled and separate from ChatGPT’s answers”。 |
| 71 | p16 | 廣告不會影響 ChatGPT 給出的答案。 | CONFIRMED | A | “advertising does not influence the answers ChatGPT provides”。 |
| 72 | p16 | 這些都是 OpenAI 自己的說法，本站沒有能力查證； | CONFIRMED | — | 本站自述；歸因完整。 |
| 73 | p16 | 以查核到 2026-09-26 未見台灣的個人化廣告設定狀態，也未見任何台灣主管機關、法規或個資法被提到。 | CONFIRMED | H2, A | 否定句沒有指出頁面：補成「以公告與說明中心查核到…未見」；Help 只點名 EEA 與瑞士（“Personalized ads are not initially available in the EEA or Switzerland”），Taiwan 0 次；無主管機關或法規。 |
| 74 | p17 | 想確認自己帳號目前是什麼狀態，或商家想確認能不能自助投放，可以直接查說明中心的〈Ads in ChatGPT〉與〈Ads Manager Availability〉兩個頁面。 | CHANGED | H2 | 說明中心頁面看不到讀者自己帳號的狀態；Help “you’ll see clear in-product information”。「想確認自己帳號目前是什麼狀態」→「想確認最新規則」。 |
| 75 | p17 | Ads Manager 本身是 2026 年 5 月推出的自助購買工具，完整的操作流程與計費方式，可以看 OpenAI 當時的公告。 | NOT FOUND | AUG | 前半成立（“The introduction of Ads Manager in May”＋公告 “Self-service access through Ads Manager”）；後半「完整的操作流程與計費方式，可以看 OpenAI 當時的公告」sources[] 撐不住（已發布的 5 月篇計費取自開發者文件）。改指向第二個結尾連結。 |
| 76 | faq1.q | 台灣的 ChatGPT 使用者現在就會看到廣告嗎？ | OUT OF SCOPE | — | 問句。 |
| 77 | faq1.a | 不一定。 | CONFIRMED | H2 | — |
| 78 | faq1.a | OpenAI 公告寫的是「開始逐步推出」，說明中心也寫廣告是逐步推送給符合資格的 Free 與 Go 使用者，不是所有帳號在同一天都會看到； | CONFIRMED | A, H2 | 「開始逐步推出」是 begin rolling out 的中譯；Help “gradually rolling out … to eligible users”。 |
| 79 | faq1.a | 如果帳號符合測試資格，會在 ChatGPT 產品裡看到明確的說明。 | CONFIRMED | H2 | 同 32。 |
| 80 | faq2.q | 哪些方案完全沒有廣告？ | OUT OF SCOPE | — | 問句。 |
| 81 | faq2.a | 公告裡點名的無廣告方案是 Plus、Pro 與 Enterprise； | CONFIRMED | A | — |
| 82 | faq2.a | 查核日讀到的說明中心頁面則列出更完整的清單，寫 Plus、Pro、Business、Enterprise 與 Edu 帳號不會有廣告。 | CONFIRMED | H2 | — |
| 83 | faq2.a | 要注意 Go 雖然是付費方案，但仍在可能出現廣告的名單上。 | CONFIRMED | H2 | 同 29。 |
| 84 | faq3.q | 關掉廣告個人化，是不是就不會再看到廣告？ | OUT OF SCOPE | — | 問句。 |
| 85 | faq3.a | 不是。 | CONFIRMED | H2 | “Is turning off ad personalization the same as going Ads-Free? No.” |
| 86 | faq3.a | 說明中心明寫，關掉個人化之後仍會依照目前這段對話的脈絡顯示廣告，只是不再用其他對話、廣告紀錄或主題來挑選； | CONFIRMED | H2 | 同 12、47（間接引述忠實）。 |
| 87 | faq3.a | 想要真正沒有廣告，Free 方案可以改用 Ads-Free 體驗，但會有訊息數變少等使用限制。 | CONFIRMED | H2 | 同 13。 |
| 88 | faq4.q | 台灣企業要怎麼在 ChatGPT 上投放廣告？ | OUT OF SCOPE | — | 問句。 |
| 89 | faq4.a | 公告寫的管道有三種：OpenAI 的 Ads Solutions 團隊、代理商夥伴，以及技術夥伴； | CONFIRMED | A | 同 22。 |
| 90 | faq4.a | 符合資格的企業也可以使用自助的 Ads Manager。 | CONFIRMED | A | 同 23。 |
| 91 | faq4.a | 說明中心解釋，自助資格看的是刊登廣告並被收費的法律實體所在國家，查核日讀到的國家表裡 Taiwan 那一列標示 Available。 | CONFIRMED | H1 | 同 15。 |
| 92 | faq5.q | 10 億美元年化營收是這次公告的新數字嗎？ | CONFIRMED | A | 問句內含主張，同 94。 |
| 93 | faq5.a | 不是。 | CONFIRMED | A | — |
| 94 | faq5.a | 這是 OpenAI 在 2026 年 8 月底公布的數字，說 ChatGPT 廣告上線不到 200 天就達到 10 億美元的年化營收（annualized revenue run rate）； | CONFIRMED | A, AUG | “annualized revenue run rate”；8 月底公布。 |
| 95 | faq5.a | 9 月 23 日這篇公告只是回顧提到這個數字，不是這次新公布的成績。 | CONFIRMED | A | “At the end of August, we announced …”（回顧）。 |
| 96 | faq6.q | OpenAI 說對話不會給廣告主、也不會影響回答，是查證過的事實嗎？ | CONFIRMED | A | 問句內含主張，已歸因 OpenAI。 |
| 97 | faq6.a | 不是查證過的事實，是 OpenAI 自己在公告裡的宣示：官方表示不會把使用者對話提供給廣告主、也不會出售資料，廣告一律清楚標示並與回答分開，且不影響 ChatGPT 給出的答案； | CONFIRMED | A | 原則句改寫成間接引述：忠實（conversations private、never sell customer data、clearly labeled and separate、does not influence）。 |
| 98 | faq6.a | 本站沒有能力查證這些說法。 | CONFIRMED | — | 本站自述。 |
| 99 | callout.title | 三件事：逐步推出、方案清單看出處、控制項不是消除廣告 | CONFIRMED | A, H2 | — |
| 100 | callout.text | ChatGPT 廣告在台灣是「開始逐步推出」，不是 9 月 23 日當天所有帳號都看得到； | CONFIRMED | A, H2 | — |
| 101 | callout.text | 無廣告方案公告只列 Plus、Pro、Enterprise，查核日讀到的說明中心頁面另外列出 Business 與 Edu，兩份清單要分開看，Go 是付費方案但仍可能出現廣告。 | CONFIRMED | A, H2 | 兩份清單分開歸因；Go 付費仍可能有廣告。 |
| 102 | callout.text | 使用者可以在設定裡調整廣告個人化，但關掉之後仍會依對話脈絡顯示廣告； | CONFIRMED | H2 | — |
| 103 | callout.text | 企業能不能自助投放，看的是刊登並被收費的法律實體所在地，不是人在哪裡。 | CONFIRMED | H1 | 同 58。 |
| 104 | callout.text | 查核到 2026 年 9 月 26 日為止，之後想確認最新狀態，請直接查 OpenAI 說明中心。 | CONFIRMED | H1, H2 | — |
| 105 | link | 2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用 -> https://mokaair.com/zh-TW/life/ai-news-2026-january-september-index | CONFIRMED | PACK | 與 ai-news-2026-january-september-index 的 zh-TW title 逐字相同；目標五語齊全。 |
| 106 | link | ChatGPT 廣告開放自助購買：OpenAI 5 月公告的工具、計費與鎖定機制 -> https://mokaair.com/zh-TW/life/ai-news-chatgpt-ads-20260505 | CONFIRMED | PACK | 與 ai-news-chatgpt-ads-20260505 的 zh-TW title 逐字相同；目標五語齊全。 |
| 107 | hero_label | 廣告在台灣逐步推出 | CONFIRMED | A | — |
| 108 | diagram.title | ChatGPT 廣告到台灣的四件事 | CONFIRMED | — | — |
| 109 | diagram.node1 | 誰會看到 / Free、Go 方案逐步推出 | CONFIRMED | A, H2 | — |
| 110 | diagram.node2 | 誰沒有廣告 / Plus、Pro 等方案 | CONFIRMED | A, H2 | 「等」保留清單不完整。 |
| 111 | diagram.node3 | 怎麼控制 / 關個人化不等於沒廣告 | CONFIRMED | H2 | — |
| 112 | diagram.node4 | 商家怎麼買 / 自助看法律實體所在地 | CONFIRMED | H1 | — |
| 113 | source | ChatGPT Ads expands to Southeast Asia and Taiwan https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/ 2026-09-26 | CONFIRMED | A | 今天 200、0 次轉址、386,726 bytes、<article> 全文。 |
| 114 | source | Ads Manager Availability（OpenAI Help Center） https://help.openai.com/en/articles/20001245-ads-manager-availability 2026-09-26 | CONFIRMED | H1 | 今天 200、0 次轉址、63,895 bytes、全文；updatedAt 2026-09-25T21:12:52Z。 |
| 115 | source | Ads in ChatGPT（OpenAI Help Center） https://help.openai.com/en/articles/20001047-ads-in-chatgpt 2026-09-26 | CONFIRMED | H2 | 今天 200、0 次轉址、98,313 bytes、全文；updatedAt 2026-09-26T10:04:51Z。 |
| 116 | source | A milestone in expanding access to AI https://openai.com/index/expanding-access-to-ai-with-chatgpt-ads/ 2026-09-26 | CONFIRMED | AUG | 今天 200、0 次轉址、401,787 bytes、全文；頁首 August 31, 2026。 |
