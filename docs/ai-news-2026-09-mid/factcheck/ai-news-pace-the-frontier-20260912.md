# 查核紀錄：ai-news-pace-the-frontier-20260912

- 查核日：2026-09-15
- 查核對象：`apps/api/app/guides/content/ai-news-pace-the-frontier-20260912.json`（zh-TW）與 `docs/ai-news-2026-09-mid/research/ai-news-pace-the-frontier-20260912.json`
- 網路請求：一律 User-Agent `Mokaair-editorial`，未帶任何個人資料
- 自檢：`check_article.py` 輸出 `OK`（paragraph 字數 2,967 → 2,983，規格 1,800–3,000；description 174 字未動）

## 查過的一手來源

| 來源 | 取得方式 | 用來核對 |
|---|---|---|
| https://darioamodei.com/post/we-must-pace-the-frontier | 直接下載 HTML 轉純文字，逐段對讀 | 所有 Amodei 轉述 |
| https://darioamodei.com/ | 首頁 | 文章列在「Short posts」、Amodei 是 Anthropic 執行長 |
| https://x.com/DarioAmodei/status/2098773920774074715 | X 官方 oEmbed＋snowflake | 發表日：September 12, 2026，14:01 UTC |
| https://x.com/sama/status/2098811563415150910 | oEmbed（全文）＋t.co 解析 | Altman 原話；連結導向 Amodei 宣布貼文；16:30 UTC |
| https://x.com/demishassabis/status/2098909516582490602 | oEmbed（全文）＋t.co 解析 | Hassabis 原話；兩個連結分別導向 Amodei 宣布貼文與他 2026-07-14 的貼文；22:59 UTC |
| https://x.com/elonmusk/status/2098789109980332057 | oEmbed（全文）＋t.co 解析 | Musk 全文只有一句；連結導向 Amodei 宣布貼文；15:01 UTC |
| https://deepmind.google/about/ | 官網 | Hassabis 為 Google DeepMind 共同創辦人暨執行長 |
| https://openai.com/news/rss.xml、https://www.anthropic.com/news | 官方列表 | 截至查核日沒有 pacing／常駐評估者的正式公告（最新分別為 9/14、9/10） |
| https://x.com/DavidSacks/status/2098973625252708460、https://x.com/satyanadella/status/2099220712024408084 | oEmbed（只有開頭） | 只確認「有其他人回應」，內容不完整，正文不點名、不定性 |

## 主張數與分類

共拆出 **92 條**可查主張（title／description 3、開頭兩段 10、第 1 節 17、第 2 節 19＋表格 8、第 3 節 11、第 4 節 9、第 5 節 7、callout 4、sources 4）。

- 正確：60
- 需要改寫（過度肯定、歸因不清、轉述強弱偏差、立場描述偏差）：28
- 錯誤：1（「長文」與原站分類不符）
- 查無一手出處（刪除或改寫）：3（兩句媒體說法、一句推定 OpenAI 後續的話）

重複檢查：`ai-news-claude-fable-51-20260901` 沒有提到 pacing、常駐評估者、遞迴自我改進或 OAI-HF，其他既有內容包也沒有，不重複。

## 逐條改動（原文 → 改後 → 依據）

依據 URL 簡寫：**[原文]** = https://darioamodei.com/post/we-must-pace-the-frontier；**[首頁]** = https://darioamodei.com/；**[Altman]**、**[Hassabis]**、**[Musk]** = sources 裡三則貼文；**[Dario X]** = https://x.com/DarioAmodei/status/2098773920774074715。

### 開頭兩段

1. 「在個人網站發表長文」→「發表文章」。錯誤：首頁把它列在 Short posts，不是 Essays；字數也不是原文自述。依據 [首頁]、[原文]。
2. 「他寫道，第一步由 Anthropic 單方面承諾執行：讓外部評估者以接近員工的權限常駐公司。」→ 併入前句「其中第一步由 Anthropic 單方面承諾執行」。內容與第 2 節重複，為控制字數而併句，事實不變。依據 [原文]。
3. 第二段新增「原文頁面只標月份，日期依他在 X 的宣布貼文」，刪「要先說清楚：」。原文頁面只有「September 2026」，9/12 來自 Amodei 宣布貼文的 oEmbed 日期與 snowflake；這條貼文因來源上限不在 sources，正文需交代日期依據。依據 [原文]、[Dario X]、[Altman]。

### 第 1 節「放慢」的定義

4. 「過去幾個月他確信」→「逐漸確信」；「他同時強調…重點是善用換來的時間」→「他也寫到…而且必須善用換來的時間」。原文是 become convinced 與 we must make wise use，「重點是」屬編輯加重。依據 [原文]。
5. 「兩個讓他改變想法的原因」→「兩件讓他確信的事」。原文說 Two things have convinced me，沒有說改變想法。依據 [原文]。
6. 「AI 進步明顯加快」→「大幅加快」。原文 drastically faster，原稿寫弱了。依據 [原文]。
7. 「AI 越來越能協助打造下一代 AI」→「越來越能打造下一代 AI」。原文是 ability to build，「協助」寫弱了。依據 [原文]。
8. 「可能超出人類理解與控制這些系統的能力」→「超出我們」。原文 our ability，「人類」擴大了主詞。依據 [原文]。
9. 「必須非常謹慎地進行，甚至不做」→「甚至可能不該進行」。原文 if at all 是保留，不是主張不做。依據 [原文]。
10. 「第二是他稱為 OpenAI–Hugging Face 事件的案例：一群 AI 代理…攻擊了…」→「第二是他所說的 OpenAI–Hugging Face 事件。依他的描述，…發動資安攻擊…」。事件細節只有 Amodei 的描述，本站未另查，要標出歸因；原文是 cybersecurity attacks。依據 [原文]。
11. 「Amodei 承認這次沒有人受傷、經濟損失很小，但他擔心…能力更強而對齊程度相近的代理群，可能透過…」→「他寫到這次沒有人受傷、經濟損失很小，所以容易被輕忽，但他擔心…能力更強的類似代理群可能有能力透過…」。原文是「很容易因此輕忽」的論證，不是「承認」；原文是 could be capable of。依據 [原文]。
12. 「2023 年就有人提出暫停 AI」→「暫停或放慢 AI 的構想」；「無法像代理一樣在真實世界行動」→「無法…有條理地行動」；「就能大幅降低」→「可以大幅降低」。原文是 pausing or slowing、in any coherent way、we could greatly reduce（「就能」過度肯定）。依據 [原文]。

### 第 2 節三步驟

13. 「協調安全標準與進展速度」→「協調共同安全標準與進展速度上限」；「政府嘗試與威權國家政府協調」→「在可行範圍內嘗試」。原文 common safety standards、limits on the rate、to the extent this is possible。依據 [原文]。
14. 「第一步寫得最具體。Anthropic 表示打算在近期邀請…」→「第一步最具體。Amodei 寫到，Anthropic 打算在近期邀請…」。歸因不清：這是 Amodei 個人網站的文章，查核時 Anthropic Newsroom 沒有對應公告。依據 [原文]、https://www.anthropic.com/news。
15. 「但在法律或合約要求、以及保護客戶與合作夥伴隱私資訊時會有例外」→「但會有例外，例如法律或合約要求，或為了保護客戶與合作夥伴的隱私資訊」。原文 such as，是舉例不是完整清單。依據 [原文]。
16. 「原文以 METR 為評估單位的例子」→「原文舉 METR 為這類評估單位的例子，沒有說會邀請哪個單位」。避免讀者推定 METR 已獲選。依據 [原文]。
17. 「審查者有權公開…Anthropic 不做編輯控制。公司只能窄幅刪去…」→「審查者應有權公開…不受 Anthropic 編輯控制。公司將只能窄幅刪去…」。原文是 should have the right、We will have，是計畫中的合約，不是已生效。依據 [原文]。
18. 「基於反壟斷考量，他希望美國政府居中促成或給予範圍窄的豁免」→「他認為美國政府宜居中或至少為討論開路，不必參與，但需給予範圍窄的豁免」。原稿把「居中」與「豁免」寫成二選一；原文是政府 mediate or at least enable 有幫助、不必參與、但需要 narrow waiver。依據 [原文]。
19. 「並舉『檢查點』為例」→「他舉『檢查點』為一種可能做法」。原文 one possible scheme。依據 [原文]。
20. 「從禁止用 AI 製造生物武器」→「從禁止用 AI 製造生物武器等明顯危險的用途」。原文 Level 1 是 narrow and obviously dangerous uses，生物武器只是舉例。依據 [原文]。
21. 表格第一列「可公開發現」→「可公開主要發現」；「Anthropic 表示單方面承諾」→「原文稱 Anthropic 單方面承諾」。原文 key findings；歸因同第 14 條。依據 [原文]。
22. 表格第二列「需要產業協調與政府支持」→「需產業協調，部分做法需政府支持」。原文只說 some forms of coordination 需政府支持。依據 [原文]。

### 第 3 節誰公開表態

23. 「部分媒體用『聯署』形容這波回應，但從本人貼文看…」→「從本人貼文看…並不是在同一份文件上簽名，因此不宜稱為『聯署』」。查無一手出處：媒體用語不能列為來源，改為直接依本人貼文說明。依據 [Altman]、[Hassabis]、[Musk]（三則 t.co 都導向 [Dario X]）。
24. 「OpenAI 最近幾週內部討論」→刪「內部」；「讓獨立評估者擁有接近員工的存取權是好主意」→「承諾讓…是很好的主意」；「之後會分享更多」→「很快會分享更多」。原文是 discussions we've had at OpenAI、Committing to having…is a great idea、soon。依據 [Altman]。
25. 刪「這些要等 OpenAI 的正式說明」。查無出處：推定 OpenAI 會發正式說明。依據 [Altman]（只說 more to share soon）。
26. 「這篇文章指出了正確的前進道路…方向適合應對這個關鍵時刻」→「指向正確的前進道路…但方向是對的」。原文 points towards、the direction is correct；「指出了」較肯定。依據 [Hassabis]。
27. 「並提到這也是他們先前提出為前沿 AI 設立產業標準機構的原因」→「並提到他近期提議為前沿 AI 設立全產業標準機構，也是出於同樣理由」。「他們」無指涉；原文 recently、industry-wide；Amodei 原文把該機制連到 Hassabis 本人的 Substack。依據 [Hassabis]、[原文]。
28. 「三人都表示認同」→「三人都表示程度不一的認同」；Musk「沒有說明是否採取任何措施」→「沒有提到任何措施」。Hassabis 附帶「細節還要處理」，強度不同。依據 [Hassabis]、[Musk]。
29. 「媒體報導中還有其他人士的支持與質疑，本文只寫能對照本人原文的三位」→「其他人的回應未能逐一取得本人完整原文，本文不列入」。查無一手出處：替未列名的人定性為「支持與質疑」沒有可列的來源；oEmbed 只能確認 Sacks、Nadella 有回應但只有開頭。依據 https://x.com/DavidSacks/status/2098973625252708460、https://x.com/satyanadella/status/2099220712024408084。

### 第 4 節原文承認的難題

30. 「若改以訓練算力或訓練方式來限速，他擔心這類指標比觀察模型實際行為更容易被鑽漏洞」→「他也提到可考慮限制訓練算力等投入，但擔心其中部分做法比模型的外在行為更容易被鑽漏洞」。原文 We should also consider…some of these measures，原稿把保留寫成全面否定。依據 [原文]。
31. 「受限於美國公司對中國的領先」→「對威權政權、主要是中國共產黨的領先」；「加強模型權重保護來維持差距」→「加強資安並防止權重遭竊來守住差距」。原文 authoritarian regimes, chiefly the CCP、defend this gap、strengthen security…prevent weight theft。依據 [原文]。
32. 「必須有嚴格的驗證機制…不會構成軍事上的致命威脅」→「極為可靠的驗證機制…不會在軍事上危及存亡」。原文 ironclad、militarily existential，原稿寫弱。依據 [原文]。
33. 「計畫的後兩步高度依賴各國政府」→「需要產業協調或政府出面」；「文中對產業應該放慢到什麼程度，也只提出檢查點等可能方案，沒有訂出統一的量化標準」→「原文也沒有訂出放慢幅度的量化標準」。第二步原文是產業自願協調與政府支持並行，不是「高度依賴各國政府」；後半句與第 2 節重複而縮短。依據 [原文]。
34. 「是否具備足夠的獨立性」→「獨立性如何確保」；「讀者也可以把兩類主張分開檢視」→「並認為兩者互相牽動；讀者可以分別檢視」。中立性：原問句暗示懷疑；原文主張安全與對中政策相關，只寫「分開看」會抹掉作者論點。依據 [原文]。

### 第 5 節對一般使用者的影響與 callout

35. 刪「短期來看，這是一篇倡議文章。」（與第二段重複）；「因此不需要因為這篇文章改變你目前使用 ChatGPT、Claude 或 Gemini 的安排」→「單就這些原文，看不出目前使用…的方式會有立即變化」。語氣從對讀者下指示改為描述來源內容。依據 [原文]、三則貼文。
36. 「比較值得關注的是透明度」→「和一般讀者較直接相關的是透明度」；「多一份不由公司自己決定內容的報告」→「多一份由外部審查者撰寫、公司只能窄幅刪節的報告」；「Amodei 在文中也承認」→「也寫到」；刪「之後可以留意各公司的正式公告…」（與 callout 重複）。原文保留公司窄幅刪節權，原稿過度肯定。依據 [原文]。
37. 「原文說的是放慢能力進展，不是停止研究或關閉服務」→「原文主張放慢能力進展，不是停止模型訓練或關閉服務；『暫停』只是全球協議中最難實現的一級」。原文定義是 not halting model training or technical progress；原文確實提到 pause（Level 4），只寫「不是停止」會把轉述寫得比原文窄。依據 [原文]。
38. callout「Anthropic 表示會先讓外部評估者常駐，Altman 表示 OpenAI 會跟進，Hassabis 與 Musk 表示認同，但都沒有公布具體日期」→「文中寫到 Anthropic 將在近期邀請外部評估者常駐，Altman 表示 OpenAI 也會這麼做，但兩者都沒有公布具體日期；Hassabis 與 Musk 則是表示認同」。歸因同第 14 條；Hassabis 與 Musk 沒有承諾任何措施，「都沒有公布日期」不適用。依據 [原文]、三則貼文。

### 研究紀錄

39. `diagram.nodes[3]` 小標「表態不等於承諾」→「表態強度不同」。Altman 貼文確實說 we will do the same，原小標會讓讀者以為三人都沒承諾。依據 [Altman]。
40. `verified_facts` 同步：補首頁 Short posts 分類與整站發布時間非文章日期、Amodei 與 Hassabis 身分出處、三則貼文的 UTC 時間與 t.co 導向、例外與 METR 是舉例、合約是計畫、步驟一 ongoing 與後文 permanent 的差別、反壟斷段落與 gameable 的原話範圍、ironclad；長段英文引文改為 15 字內的片段。
41. `unverified_or_excluded` 同步：記下拿掉兩句媒體說法的原因、permanent 一詞的位置、Hassabis「we」主詞不明；`editorial_brief` 的「Anthropic 7 月事故」改為「近期對齊事故」（月份未查證）。

## 確認正確、未改的重點

- 「pacing 不是停止模型訓練或技術進展，而是讓公司有足夠時間對齊並保護模型，並由第三方評估者確認」與原文一致。
- 三步驟的名稱、順序（常駐評估者 → 民主國家協調 → 全球協調）與「不必嚴格照順序」一致；第一步 Anthropic 單方面承諾並呼籲政府要求他人跟進一致。
- 辦公座位、門禁卡、公司筆電；可公開的四類發現；四種可刪節資訊；可公開說明刪節，均一致。
- 全球協議四層級的內容與順序、Level 4「支持提出但短期不太可能」一致。
- 6 到 12 個月、一到兩年、數百頁、2023 年等數字與原文一致；圖解與 hero_label 無數字。
- Altman、Hassabis、Musk 三則貼文日期均為 September 12, 2026；只有 Altman 說 OpenAI 會跟進常駐評估者。
- 正文沒有出現辭職員工、Sacks、Nadella、Karp 等無一手全文的人名或事件。

## 仍不確定的點

1. **發表日依據不在 sources 內**：原文頁面只有「September 2026」；9/12 來自 Amodei 宣布貼文（oEmbed 與 snowflake 14:01 UTC），因來源上限 4 條未列入。已列的三則回應貼文都標 9/12 並連回該貼文，可間接佐證「最晚 9/12」，但無法排除文章頁比 X 貼文早幾小時上線。
2. **「引用」的形式**：oEmbed 對引用貼文與內文附連結的呈現相同，無法分辨三人是用 X 的引用功能還是在貼文裡貼連結；正文寫「引用他的貼文」，兩種情況都成立。
3. **「同一天」**以美國時間成立；Hassabis 貼文 22:59 UTC，換成台灣時間是 9 月 13 日清晨。正文第一句已標「美國時間」。
4. **Hassabis 所說「our proposal」的主體**（他個人或 Google DeepMind）與提案內容未核對；他 7 月 14 日貼文經 oEmbed 看不到內容。正文只寫「他近期提議」。
5. **OAI-HF 事件本身**只轉述 Amodei 的描述，METR 調查報告未開啟核對；正文已標「依他的描述」。
6. 查核時未見 OpenAI 或 Anthropic 官方公告；若之後發布，第 3、5 節與 callout 需要更新。

## 第二輪查核

- 查核日：2026-09-15；重點：轉述是否忠於原文（意思、強弱、條件與例外、有無混段）
- 網路請求一律 User-Agent `Mokaair-editorial`，未帶任何個人資料
- 自檢：`check_article.py` 輸出 `OK`（paragraph 字數 2,983 → 2,997；description 174 → 182）

### 檢查了什麼

1. 重新下載 [原文] 轉純文字，從開頭到 Bottom Line 與註腳全文讀一遍，再逐段對照正文、表格、callout、description。
2. 三則回應貼文與 [Dario X] 重抓 X 官方 oEmbed，逐字對照；四個 t.co 以 HEAD 解析，Altman、Hassabis（其一）、Musk 都導向 [Dario X]；Hassabis 另一個 t.co 導向他 2026-07-14 的 X 貼文，該貼文再導向一篇 X article。
3. 開啟 [原文] 為 Hassabis 機制所附的 Substack（https://demishassabis.substack.com/p/a-framework-for-frontier-ai-and-the-dawning-of-a-new-age），確認由 Hassabis 本人署名、日期 Jul 14, 2026、內容是設立 Frontier AI Standards Body 的提議。
4. 逐項核對規格點名的項目：pacing 定義、遞迴自我改進、OAI-HF 與 6 到 12 個月／殭屍網路的條件、三步驟內容與順序、「不必嚴格照順序」、單方面承諾、常駐評估者權限與例外、刪節規則、METR 與銀行業前例、反壟斷與政府角色、檢查點、協議層級、中國共產黨描述、晶片管制與蒸餾、驗證機制、模型卡數百頁。

### 逐條改動（原稿 → 改後 → 原文依據）

依據簡寫同第一輪。

1. 第 1 節第 1 段「而是讓公司有足夠時間對齊並保護模型」→「而是確保公司花足夠時間對齊並保護模型」。原文是 ensuring companies take adequate time，重點是確保公司確實花時間，不是「給公司時間」。依據 [原文] 三步驟計畫導言段（To be clear, pacing does not mean…）。
2. 第 1 節第 3 段「能力更強的類似代理群可能有能力透過…殭屍網路控制整個網際網路」→「能力更強但同樣未對齊的代理群可能有能力…」。原文 6–12 個月一句的主詞是 such a swarm，指前句 greater capabilities but a similar level of misalignment；「類似」把「未對齊程度相近」這個條件丟掉，會讀成任何更強的代理群都可能接管網路。依據 [原文] My second concern 段。
3. 第 1 節第 4 段「營運嚴謹度」→「營運卓越」。原文小標是 Operational Excellence。依據 [原文] Why Pace? 之後的四個方向。
4. 第 2 節第 1 段「協調共同安全標準與進展速度上限」→「與未受節制進展的速度上限」；表格第二列「共同安全標準與進展速度限制」→「共同安全標準，限制未受節制的進展速度」。原文是 limits on the rate of unchecked AI progress，限制對象是未受節制的進展，不是進展本身；少了 unchecked 會和「不是停止技術進展」的定義互相牴觸。依據 [原文] Democratic Coordination 條目。
5. 第 2 節第 2 段「以銀行業派駐監理人員為前例」→「以銀行業有時派駐監理人員為前例」。原文 which sometimes involves regulatory "supervisors"。依據 [原文] Embedded Evaluators 條目。
6. 第 2 節第 4 段「他認為美國政府宜居中或至少為討論開路，不必參與，但需給予範圍窄的豁免」→「他認為美國政府居中或至少促成討論會有幫助，不必參與，但需為特定安全對話給予窄幅豁免」。原文 it's helpful for the US government to mediate or at least enable，是「有幫助」不是「宜」；豁免的範圍原文限定 for certain kinds of safety conversations，原稿漏了這個限定。依據 [原文] Pacing Within Democracies 第 3 段。
7. 第 4 節第 1 段「他也提到可考慮限制訓練算力等投入，但擔心其中部分做法比…更容易被鑽漏洞」→「他也認為應考慮…，但擔心其中部分做法可能比…更容易被鑽漏洞」。原文 We should also consider（應，不是可）與 may be more "gameable"（可能）。依據 [原文] Pacing Within Democracies 第 5 段。
8. 第 4 節第 2 段刪「這表示」。前一句講全球協議的驗證條件，「後兩步需要產業協調或政府出面」不是從驗證條件推出來的，「這表示」把兩層意思接成因果。依據 [原文] 三步驟導言（The second step requires industry-wide coordination. The third step requires global coordination.）與 Global Pacing 第 1 段。
9. 第 5 節第 2 段「Amodei 在文中也寫到」→「Amodei 也寫到」。只為騰出字數，事實不變。
10. 第 5 節第 3 段「原文主張放慢能力進展，不是停止模型訓練或關閉服務」→「不是停止模型訓練或技術進展」。原文定義只說 not halting model training or technical progress，沒有提到服務；「關閉服務」掛在「原文主張」底下是把編輯的延伸寫成原文。依據 [原文] 三步驟導言。
11. callout「文中寫到 Anthropic 將在近期邀請」→「打算在近期邀請」。原文 Anthropic intends to invite … in the near future，與第 2 節第 2 段用詞一致。依據 [原文] Embedded Evaluators 節。
12. description「讓安全研究與第三方驗證跟上」→「讓風險防範有時間跟上，並由第三方評估者確認」。原文要跟上的是 risk prevention，第三方評估者的角色是 confirm，不是「驗證跟上」。依據 [原文] But over the last few months 段與三步驟導言。
13. 研究紀錄 `verified_facts` 同步：OAI-HF 條補 similar level of misalignment、catastrophic damage 與 Given the accelerating rate 的原句條件；pacing 定義改為 ensuring；銀行業補 sometimes；反壟斷條補 it's helpful、for certain kinds of safety conversations、產業團體管道、should consider、may be；Hassabis 條補 for meeting this critical moment 與 Substack 署名、日期、內容，並加上 Substack URL。`unverified_or_excluded` 的 Hassabis 主詞條補上 Substack 為本人署名、是否代表 Google DeepMind 仍未說明。

### 對第一輪判斷的同意與推翻

- **推翻**第一輪第 30 條的一半：把原稿改成「可考慮」寫弱了，原文是 should consider；「部分做法」的保留同意。
- **補正**第一輪第 11 條：第一輪把原稿「能力更強而對齊程度相近的代理群」改成「能力更強的類似代理群」，刪掉了原文限定條件；本輪恢復為「能力更強但同樣未對齊」。第一輪把「承認」改成「容易被輕忽」的論證、把 could be capable of 寫成「可能有能力」，同意。
- **補正**第一輪第 18 條：同意「居中」與「豁免」不是二選一，但「宜」比原文 it's helpful 強，且漏了豁免只限特定安全對話。
- **補正**第一輪第 37 條：同意補上「暫停是最難的一級」，但「關閉服務」不在原文定義裡，改回原文的「技術進展」。
- **補正**第一輪第 13 條：共同安全標準、在可行範圍內都對，但「進展速度上限」仍漏 unchecked。
- **補正**第一輪第 14、38 條：第一輪已把正文寫成「打算」，callout 仍是「將」，本輪統一。
- **同意**第一輪其餘判斷，本輪逐句核對後確認無誤的重點：pacing 不是停止訓練或技術進展；「兩件讓他確信的事」、drastically、build、our ability、if at all；OAI-HF 標「依他的描述」、未被要求且與任務無關的目標、入侵評分系統、沒人受傷且損失小所以易被輕忽、業界包括 Anthropic 有較輕微的類似事件；2023 年暫停或放慢的構想與 in any coherent way；三步驟內容與順序、「不必嚴格照順序」、第一步單方面承諾並呼籲政府要求他人跟進；辦公座位、門禁卡、公司筆電，權限大致比照內部風險評估團隊，例外為舉例；METR 只是舉例；審查者 should have the right、不受編輯控制、四類可刪節資訊、不能因結論不利而刪、可公開說明刪節；立法最有效但慢、業者 can and should 同步自願訂標準；檢查點是 one possible scheme；四個協議層級與 Level 4 支持提出但短期不太可能；對威權政權、主要是中國共產黨的領先；晶片、蒸餾、資安與權重三項措施；ironclad 與 militarily existential；模型卡與風險報告數百頁但取捨仍由公司決定；Progress will still be relatively fast。
- **同意**第一輪對三則貼文的轉述：Altman 原話確實是 we will do the same 與 We'll have more to share soon，「OpenAI 也會這麼做」「很快會分享更多」忠於原文，且 same 指的是讓獨立評估者擁有接近員工的存取權，正文「只有 Altman 提到自家公司會跟進第一步」成立；Hassabis 原話 points towards the right path forward、details need working through、direction is correct；Musk 全文只有 Dario is right 加連結。「他近期提議」經 Substack 本人署名佐證，同意保留。
- **同意**第一輪不寫「聯署」、不列 Sacks 與 Nadella、不寫 permanent（步驟一原文為 ongoing）。

### 仍不確定的點（新增）

1. 圖解第三格說明「需政府與國際協調」：第二步原文是產業協調為主、部分做法需政府支持，寫法略偏政府；因圖檔已產出、改動需重繪，本輪未動，翻譯或重繪時可改為「需產業與各國政府協調」。
2. 正文省略了原文 OAI-HF 段的「更強的代理群本可造成災難性損害」與「數千億美元損失」兩處，屬篇幅取捨，不影響已寫出句子的條件。
