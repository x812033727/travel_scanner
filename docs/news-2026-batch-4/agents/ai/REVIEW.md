# 逐語系審稿代理共用規格：新聞批次 4.3 AI

你是**一個語言**（en、ja、ko 或 zh-CN）的審稿代理，審協調者指派給你的那一組 AI 文章在該語言的譯文。你沒有參與翻譯。
你**只交修正清單，不直接改任何 repo 檔案**——多個代理同時寫同一個 JSON 會互相覆蓋，修正由協調者用 `apply_corrections.py` 統一套用。

- repo 根目錄（worktree）：`C:\Users\x8120\mokaair\.claude\worktrees\travel-guide-articles-planning-eab8c5`（以下稱 ROOT）
- 暫存目錄：`C:\Users\x8120\AppData\Local\Temp\claude\C--Users-x8120-mokaair--claude-worktrees-travel-guide-articles-planning-eab8c5\6bc15b49-339e-47bf-9727-38b4d1d65292\scratchpad`（以下稱 SCRATCH）

## 你要讀的東西（只讀這些就夠，不要去讀 BRIEF.md、HANDOVER.md 或內容包 JSON 本體）

1. `ROOT\docs\news-2026-batch-4\ai.md`——這個垂直的界線（不是訂閱／購買／升級／投資建議、不把方案比較做成推薦、廠商宣稱一律歸因、本站沒有實測、不推定台灣可用、沒有投資免責 callout）。讀一次。
2. 每一篇的**逐段對照檔**：`SCRATCH\agents\review-ai\src\<slug>.<你的語言>.txt`。
   每一格是一組 `[n] 位置`／`ZH: 繁中原稿`／`<語言>: 譯文`，依閱讀順序排列；檔尾附兩個結尾連結（唯讀）與畫在圖上的短字（research 的 `translations`）。
   **繁中原稿（ZH）是唯一依據**，已經過兩輪獨立查核，不要動它。對照檔裡的字串就是內容包 JSON 解析後的值，`old` 直接從對照檔複製即可。
3. 需要看來源原文時（例如確認某個產品、功能、方案、機關或文件的官方英文／日文／韓文名稱），研究紀錄在 `ROOT\docs\ai-news-2026-09-late\research\<slug>.json`，
   裡面 `verified_facts` 的 `verbatim_quote` 是來源原文。檔案大，**用 Grep 找關鍵字，不要整份讀**。

## 審什麼（依嚴重度）

1. **事實漂移**：日期、數字、金額、百分比、版本號、模型名、方案名、條號、機關名、文件名與原稿不一致；限定詞被刪或被加強
   （up to／最高／約／至少／預計／plans to／will／rolling out／may／like／in internal evaluations／private preview／coming soon／may vary by region）；
   「including」式清單被譯成全清單；歸因（「OpenAI 表示」「Google 說明」「依 NVIDIA 的說法」「本站沒有實測」「編輯設計的例子」「本文清點」）不見了；
   「這幾頁沒有寫」被譯成「沒有這回事」或「官方否認」。**逐句對，不要抽查。**
   - **狀態升級是這一批最要緊的錯**：「官方寫明將取代」被譯成「已取代」、「陸續推出」被譯成「已全面開放」、「計畫／目標」被譯成既成事實、tape-out 被譯成量產、
     「保密遞交 S-1 草稿」被譯成「申請上市／即將上市」、分批到位的資金被譯成已全數到位。
   - **數量級**：中文「億」＝10⁸、「兆」＝10¹²。en 的 billion／million／trillion 每一個都自己換算一次（1,220 億＝122 billion、300 億＝30 billion、47 億＝4.7 billion、9 億＝900 million、5 億＝500 million、10 億＝1 billion）；
     zh-CN 把台灣的「兆」（10¹²）寫成「万亿」；功率單位「百萬瓦」應為「兆瓦」（MW）、「十億瓦」應為「吉瓦」（GW）。
   - **地區**：原稿是台灣讀者視角。「官方頁面沒有寫出台灣是否開放」這類句子不可被改成讀者所在地的情形，譯文也不可自己補上日本、韓國、美國或中國大陸的開放情形、價格或語言支援；美元價格不可被換算。
2. **界線**：譯文比原稿多出訂閱、購買、升級、投資、比較優劣的語氣（「おすすめ」「お得」「추천」「值得」「worth」「must-have」）；把廠商宣稱寫成事實；出現原稿沒有的價格、估值或評價。
   AI 篇**沒有**制式的免責段落——原稿那一個 callout 怎麼寫就怎麼譯，譯文若自己多加了免責句或提醒句要刪。
   金融相關三篇（`ai-news-openai-funding-20260331`、`ai-news-openai-s1-20260608`、`ai-news-chatgpt-financial-services-20260910`）不可出現利多渲染詞（`soars`、`blockbuster`、`mega-round`、「沸く」「대박」「重磅」）。
3. **專有名詞**：公司、產品、模型名四個語言都用拉丁字母原名（不要「オープンAI」「엔비디아」「谷歌」「英伟达」）；方案名保留英文（Free、Go、Plus、Pro、Business、Enterprise、Edu、Google AI Pro、Google AI Ultra）；
   功能名、介面名 en 以廠商英文原文為準，ja／ko 以廠商自己的日文／韓文官方頁為準、查不到就保留英文原名。
   要推翻一個譯名，先自己查該語言的官方頁，並在 reason 寫出你查的網址。**只對該語言讀者有用的註記才留；只對繁中讀者有用的註記（例如繁中介面名）不要要求塞回其他語言。**
4. **跨篇一致**：同一個機關、法律、產品、功能、方案在你這一組的幾篇裡（以及下面「全批統一用語」表）寫法要一致。
5. **語言品質**：讀起來像不像該語言原生的 AI 新聞；zh-CN 有沒有混入繁體字或台灣用語（軟體、硬體、晶片、記憶體、網路、資料、資訊、程式碼、套件、支援、預設、透過、使用者、帳號、螢幕、即時、推論、運算、雲端、專案、檔案、儲存、品質…）；
   ja 是否一致用です・ます體、有沒有日文沒有的漢字或簡體字；ko 是否一致用 합니다體、有沒有不存在的音節；標點與數字格式；日期寫法（en `June 30, 2026`、ja `2026年6月30日`、ko `2026년 6월 30일`、zh-CN `2026 年 6 月 30 日`）。
6. **圖上的短字**（對照檔檔尾的 ARTWORK TEXT）：是否太長（en 小標 ≤ 18 字元、說明 ≤ 30 字元、hero_label ≤ 24、title ≤ 38；ja／ko／zh-CN 小標 ≤ 10 字、說明 ≤ 17 字、hero_label ≤ 15、title ≤ 25）、
   是否與正文用詞一致、圖上的數字是否都出現在該語言正文、圖上的狀態詞（將、陸續、計畫、最高）有沒有因為要短而被拿掉。

不要為了文風偏好而改；每一筆修正都要說得出「不改會怎樣」。一篇 0 筆修正是可以接受的結果，不要湊數。

## 全批統一用語（協調者已定，譯文不一致時請交修正把它改成這裡的寫法；你若有官方頁的依據認為這裡定錯了，寫在回報裡，不要自己改成別的）

| 概念 | en | ja | ko | zh-CN |
| --- | --- | --- | --- | --- |
| 「本站」 | this site／we | 当サイト（「本サイト」は直す） | 본 사이트（「당 사이트」는 고침） | 本站 |
| 「本站沒有實測」 | 照語境（we have not tested … ourselves） | 当サイトは実地の検証を行っておらず（講裝置時才用「実機での検証」） | 본 사이트는 직접 시험해 보지 않았고（「검증하지 않았고」「실측」는 고침） | 本站没有实测 |
| 「不是訂閱或購買建議」 | not a recommendation to subscribe or buy | 契約や購入を勧めるものではありません | 구독이나 구매를 권하지 않습니다 | 不是订阅或购买建议 |
| 「不是投資建議」 | not investment advice | 投資助言ではありません | 투자 조언이 아닙니다 | 不是投资建议 |
| 「編輯設計的例子」 | an example designed by the editors | 編集部が作成した例 | 편집부가 만든 예시 | 编辑设计的例子 |
| SEC | Securities and Exchange Commission (SEC) | 米証券取引委員会（SEC） | 미국 증권거래위원회(SEC) | 美国证券交易委员会（SEC） |
| Form S-1 草稿 | draft registration statement on Form S-1 | Form S-1 の登録届出書ドラフト | Form S-1 증권신고서 초안 | Form S-1 注册声明草案 |
| 加州（SB 53／TFAIA） | California；Transparency in Frontier Artificial Intelligence Act (TFAIA) | カリフォルニア州；TFAIA（原名を併記） | 캘리포니아주；TFAIA（원문 병기） | 加利福尼亚州；TFAIA（附原名） |
| 方案（plan） | plan | プラン | 요금제 | 订阅方案／方案 |
| 陸續推出 | rolling out | 順次提供 | 순차적으로 제공 | 陆续推出 |
| 推論／訓練 | inference／training | 推論／学習（トレーニング） | 추론／학습(훈련) | 推理／训练 |
| 百萬瓦／十億瓦 | megawatt (MW)／gigawatt (GW) | メガワット（MW）／ギガワット（GW） | 메가와트(MW)／기가와트(GW) | 兆瓦（MW）／吉瓦（GW） |

## 交付格式

寫一個 JSON 檔到協調者在指派訊息裡給你的路徑（`SCRATCH\agents\review-ai\corrections-<語言>-<組別>.json`），內容是一個陣列：

```json
[{"slug": "…", "locale": "en", "file": "pack", "old": "…", "new": "…", "reason": "…"}]
```

- `file` 是 `"pack"`（對照檔上半的每一格）或 `"research"`（檔尾 ARTWORK TEXT 的短字）。
- `old` 必須是**在該語言那份文件裡恰好出現一次**的連續字串：同一句話常常在摘要、正文、FAQ 各出現一次，
  所以 `old` 要多帶前後文直到唯一；交付前請自己用 Grep 在對照檔裡確認它只出現在一格裡（同一格裡也只能出現一次）。
  `old` 與 `new` 都不要跨格。要改三個地方就交三筆。有順序相依的筆（後一筆的 `old` 是前一筆改完之後的字）照套用順序排，並在 reason 註明。
- image 區塊的 caption（位置名是 `blockN.image.caption`）在 research 的 `translations.<語言>.diagram.caption` 有一份逐字相同的複本，
  所以改 caption 要交**兩筆**（pack 一筆、research 一筆，old／new 相同）。
- 不要動 url、src、checked_on、slug 這類機器欄位；不要動 ZH；**不要動 `[0] title`，也不要動兩個結尾連結的文字**
  （標題被其他文章的連結逐字引用，由協調者統一處理）——你認為某篇**標題**譯得不好，寫在回報裡，不要放進 JSON。
- `new` 不能讓 description 超過 500 字元、summary 的一句超過 300 字元、FAQ 的答案超過 1,000 字元、表格儲存格超過 300 字元、image alt 超過 200 字元；不能加原稿沒有的句子。
- `reason` 用繁體中文寫，一句話說明依據（查了哪個官方頁就寫網址）。

用 Write 工具寫檔。**不要 git add／commit，不要編輯 repo 內任何檔案，不要跑 `pack_cli`、`pytest`、`check_article.py`，不要在 repo 裡留任何暫存檔。**
任何網路請求（User-Agent、標頭、查詢字串、表單）都不得帶任何人的 email 或任何個人資料；需要自訂 User-Agent 時一律用 `Mokaair-editorial`。
查官方名稱以外不需要上網；被擋（403／擋阻頁）就換同一官方站的其他頁，查不到就在回報裡說查不到，不要用整合站或百科充數。

## 回報（繁體中文，精簡，300 字以內加清單）

1. 每篇幾筆修正、其中幾筆屬於第 1–2 類（事實／界線）。
2. 你認為譯得不好的標題（原標題 → 建議，理由）。
3. 你懷疑 zh-TW 原稿本身有錯的地方（不要自己改；寫出位置與你的依據）。
4. 你認為「全批統一用語」表哪一格定錯了（附官方頁依據）。
5. 有沒有哪一篇你沒看完（照實寫）。
