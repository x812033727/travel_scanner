# Tech Signal 11/5：資料中心上了選票

企劃日期 2026-11-04。每日 Podcast《Tech Signal｜科技訊號》，照 `.agents/skills/youtube-video/references/daily-brief.md`：
`format: "slides"`、`category: "ai-news"`、`theme: "paper"`，slug `daily-ai-20261105`（播出 2026-11-05 星期四，新聞日 2026-11-04），
雙主持（Sola 講新聞、Kai 替觀眾問與翻白話），台灣國語旁白、字卡全英文，目標 20–25 分鐘，沒有開場濃縮（影片從片頭動畫接 Intro）。
這一集在工作階段裡手做。每則的事實只用站上 news_date 2026-11-04 已發布的文章與它列的來源（2026-11-04 以
`/api/travel/guides/life/<slug>?locale=zh-TW` 取得，15 篇皆 HTTP 200），沒有用到網路補充的新聞；說明欄只放主題的兩篇站上文章（YouTube 說明欄 5,000 位元組、八種語言），卡片 `source` 寫原始來源。
選題依編輯指示（國際新聞為主；今天沒有台灣新聞）。

## 選題

排序依：影響多少台灣觀眾 → 今天能不能做什麼、有沒有日期 → 錢與帳戶安全 → 其他。同一件事的兩篇（The Verge 與 Decrypt 的期中選舉資料中心報導）合成主題。

| 段落 | 新聞（來源：站上文章；原始來源） | 排在這裡的理由 |
| --- | --- | --- |
| Signal of the Day | 美國期中選舉：至少 29 個轄區的選民支持禁止或限制資料中心（https://mokaair.com/zh-TW/life/ai-news-us-voters-data-center-restrictions-20261104 ；Decrypt 引述華盛頓郵報、Ballotpedia）＋資料中心成為選民反彈焦點、45 項地方公投 33 項傾向限制、各州當選人立場（https://mokaair.com/zh-TW/life/ai-news-data-center-midterms-20261104 ；The Verge 引述 NBC News、Redbud Consulting）。錢的流向接：高通把成長押在資料中心（https://mokaair.com/zh-TW/life/ai-news-qualcomm-data-center-20261104 ；The Verge）；亞洲的線接：AI 資料中心搶購記憶體造成短缺（https://mokaair.com/zh-TW/life/ai-news-altman-ram-comments-20261104 ；The Verge） | 理由見下一節 |
| Headlines 1 | ChatGPT 可做 GIF 動圖，隨新的圖像模型 Images 2.6 推出（https://mokaair.com/zh-TW/life/ai-news-chatgpt-animated-gifs-images-26-20261104 ；The Verge） | 台灣最多人用的 AI 服務，開放給所有使用者，好懂、輕鬆，放第一則接住聽眾；限制報導沒說，要講清楚 |
| Headlines 2 | Apple 在 watchOS 27.3 測試版測 Siri Recaps 等四項音訊 AI 功能，引發隱私疑慮（https://mokaair.com/zh-TW/life/ai-news-apple-siri-recaps-watch-beta-20261104 ；TechCrunch） | 用 iPhone、Apple Watch 的人多，又是隱私題，接 Try This 第一件事；目前只在開發者測試版，排第二不排第一 |
| Headlines 3 | Meta 收購 AI 寫程式新創 Conductor，雲端服務 11/20 關閉後開始刪資料（https://mokaair.com/zh-TW/life/ai-news-meta-acquires-conductor-20261104 ；TechCrunch） | 有一個使用者必須知道的日期（11/20），接 Try This 第二件事；直接影響的是開發者，一般人較遠 |
| Headlines 4 | Google 告訴學校關其他 AI 功能會失去搜尋，DuckDuckGo 向學校招手（https://mokaair.com/zh-TW/life/ai-news-duckduckgo-schools-google-ai-policy-20261104 ；TechCrunch、Google 部落格） | 家長與老師關心；只有 TechCrunch 一家報導、雙方各說各話，地區報導沒說，排中後 |
| Headlines 5 | 據 TechCrunch 報導，OpenAI 全球事務長 Chris Lehane 把 AI 比作新政、已在設法影響 2028 年大選（https://mokaair.com/zh-TW/life/ai-news-openai-2028-election-20261104 ；TechCrunch） | 一家媒體的報導加評論，旁白與卡片標「據報導」，不當主題；它談資料中心暫停，正好把快訊交給主題段 |
| Signal Number | 4：Uber 第三季由第三方 AI 代理叫的車只有 4 趟（https://mokaair.com/zh-TW/life/ai-news-uber-ai-agents-rides-20261104 ；The Verge） | 今天最驚人的小數字，好記、適合 Shorts；同時把「AI 代理」交給 What People Are Saying 與 Money Signal 的 OCC |
| What People Are Saying | 貝萊德執行長 Larry Fink（暫停令會導致衰退，經 Decrypt）、AI Now 的 Kate Brennan（評 Lehane 文章，經 TechCrunch）、Uber 執行長 Dara Khosrowshahi（非常早期，經 The Verge） | 三句都是站上文章列的原始來源裡的原文：業界對限制的警告、批評者對 OpenAI 的看法、平台對 AI 代理的看法 |
| Money Signal | OCC 首份銀行業 AI 框架，能自主付款的代理列最高風險（https://mokaair.com/zh-TW/life/ai-news-occ-bank-ai-framework-20261104 ；Decrypt）；摩根士丹利透過 DTCC 新服務代幣化美股與公債（https://mokaair.com/zh-TW/life/crypto-news-morgan-stanley-dtcc-tokenization-20261104 ；Decrypt）；Circle 獲利季裁員約 5%（https://mokaair.com/zh-TW/life/crypto-news-circle-workforce-cut-20261104 ；Decrypt）；Coinbase 稱 99% 以上資產在冷儲存、未受幣安駭客事件影響（https://mokaair.com/zh-TW/life/crypto-news-coinbase-cold-storage-binance-hack-20261104 ；Decrypt） | OCC 是「帳戶安全與 AI 代理」，排第一；代幣化是規則與誰能用；Circle 是工作；Coinbase 是帳戶安全的補充，標明是自述。只講規則、工作與安全，不談價格、漲跌、買賣 |
| Try This | 會錄音的 AI 功能先搞清楚何時在聽、私下談話關掉；用 Conductor 雲端的人 11/20 前存檔；讓 AI 工具碰帳戶前先看上限與撤銷權限（TechCrunch、Decrypt＋節目建議） | 三件都接今天的新聞，旁白與卡片標「我們的建議」「our advice」 |
| Noise of the Day | Sam Altman 選舉夜在 X 上替自己的記憶體言論辯護（https://mokaair.com/zh-TW/life/ai-news-altman-ram-comments-20261104 ；The Verge） | 輕鬆、有點荒謬，又跟主題同一晚、同一個資料中心；不嘲笑人，最後點出背後的短缺是真的 |

## 為什麼是這一則當 Signal of the Day

- 國際上影響最大、背景最值得講：AI 的實體基礎建設第一次在美國大選裡成了選民直接投票的題目（Decrypt 引述華盛頓郵報：至少 29 個轄區；The Verge：45 項地方公投 33 項傾向限制、NBC 選舉日調查 76% 反對社區設資料中心）。
- 有一個要回答的問題：一棟放電腦的房子，為什麼要用投票擋？答案在來源裡（電費、電網、用水、噪音、缺乏公眾監督）。
- 有場景：威斯康辛州 Janesville 的選民週二拿到選票，上面問前通用汽車廠址的大型開發要不要先再投一次（Decrypt）。
- 錢的流向有同一天的佐證，不用推論：當選人提的條件（開發商自付能源用水、停掉稅收優惠、禁用保密協議）、AI 公司的遊說與公關、高通把成長押在資料中心；投票會不會影響高通，報導沒說，旁白明說不推論。
- 台灣與亞洲：今天的來源都沒有提到台灣，旁白明說；看得到的一條線是 AI 資料中心搶購記憶體造成短缺（The Verge，英特爾與 SK 海力士的預測），美國少蓋會不會改變供應，來源沒說，不猜。
- 接下來看什麼很清楚：哪些投票有約束力、新州長會不會立法暫停、電費用水與稅收優惠誰付、2028 年大選（TechCrunch）。

## 觀眾

每天通勤或午休聽 20 分鐘科技新聞的台灣上班族、學生與工程師：天天用 ChatGPT、Google 搜尋，用 iPhone、Apple Watch 或 Android，
家裡有學生；有些人寫程式、用 AI 代理工具，有些人用網銀或交易所。他們要知道「這對我改變了什麼、今天要不要做什麼」。

## 觀眾看完能做到的事

- 說得出美國選民為什麼擋資料中心：用電推高電費、電網負擔、用水、噪音、協議缺乏公眾監督（Decrypt），以及「部分只是諮詢性投票」（Decrypt）、「很難歸因於單一議題」（The Verge）。
- 知道 AI 的需求會一路影響到自己買電腦的記憶體（The Verge），但不把它講成選舉的結果。
- 用會錄音、會摘要的 AI 功能時，先搞清楚它何時在聽；談私事時關掉（節目建議；功能與作者的做法依 TechCrunch）。
- 用 Conductor 雲端的人，11/20 前把要留的東西存下來（節目建議；日期依 TechCrunch 轉述創辦人）。
- 讓 AI 工具碰帳戶前，先看能不能設上限、隨時收回權限（節目建議；思路依 OCC 框架，經 Decrypt）。
- 分得清「公司自述」：Coinbase 的安全說法、高通的預測、Google 與 DuckDuckGo 的說法都不是外部驗證。

## 站主觀點

套用立場：2、4、5
（站主還沒在設定分頁存「頻道立場」，條號依 `docs/videos/HANDS-OFF.md` §頻道立場的草稿；這段是提案，給站主在大綱關卡看。）
今天最重要的是美國期中選舉裡的資料中心：AI 不只是 App，它有房子、要用電，住在旁邊的人開始用選票說話。
我不說資料中心會蓋不成，也不說選舉是因為資料中心而輸贏；很多投票只是表態，The Verge 也說很難歸因，我老實說不確定會不會真的放慢。
台灣的角度不硬湊：來源沒有提到台灣就說沒有；只講來源寫到的記憶體短缺。OpenAI 的 2028 年報導標「據報導」；錢的段落只講規則、工作與帳戶安全，不談價格。

## 不選

- Nexus Mods 要求模組作者揭露 AI（ai-news-nexus-mods-ai-disclosure-20261104）：可當 Noise，但 Altman 那則跟主題同一晚、同一個資料中心，選了它。
- 高通 2026 年總營收「104 億美元」與 2027 年的季度預測：站上文章寫的總營收數字跟高通的規模對不上（可能是單季），不用；只留手機銷量、2029 年目標與三成占比。
- Uber「3.2 億筆」總量：站上文章沒寫是哪段期間，不用，只用 4 趟與萬聖節週約 500 筆，並說期間不同。
- Circle 的營收、EBITDA、USDC 流通量與市占：跟一般人的工作與帳戶無關的財報數字。
- Lehane 把支持暫停比作 2002 年授權伊拉克戰爭的投票、SB 1047 的歷史：細節多、要很多背景，留在文章裡。
- 任何代幣價格、交易所資產規模的漲跌與買賣時機。

## 會過期的事實

- 各地公投的計票（Redbud「截至週三早上」33 項）、29 個轄區的數字（華盛頓郵報，經 Decrypt）。
- 各州當選人的資料中心立場與後續立法。
- Siri Recaps 等功能仍在開發者測試版，正式版行為與隱私設計可能不同。
- Conductor 雲端關閉與刪資料的時程、明年初之後的產品。
- Google 學校 AI 設定的預設值與 DuckDuckGo 的說法。
- OCC 框架會隨技術更新；DTCC 服務 2027 年加入更多區塊鏈。
- 記憶體短缺的時程預測（英特爾、SK 海力士）。

## 不做的事

- 不說資料中心「被禁了」；講清楚部分是諮詢性投票、效力不一。
- 不說選舉結果由資料中心決定；不替高通推論選舉會影響它。
- 不把台灣或亞洲供應鏈硬接進主題；SK 海力士只當成 The Verge 引述的記憶體廠預測。
- 不把公司自述（OpenAI 每週圖像量、Google、DuckDuckGo、高通預測、Coinbase 安全措施）講成已證實；OpenAI 2028 年一則標「據報導」。
- 不編主持人的私人經驗；Siri Recaps 的試用是 TechCrunch 作者的經驗，旁白照實說。Try This 標明是節目建議。
- 片尾不提下一集。

## 大綱

### 選項 A：從 ChatGPT 動圖講起

一行說明：Intro 由 Kai 問「打一句話就有 GIF，那它的限制是什麼」，快訊照使用人數排，Signal of the Day 仍是期中選舉的資料中心，但從投票數字講起。
開場鉤子：ChatGPT 現在打一句話就能做出 GIF 動圖，可是長度、檔案大小，報導一個字都沒寫。

排序理由：GIF 最輕鬆、最多人會用。缺點：Intro 的問題在快訊第一則就答完（「報導沒說」），撐不起整集；
主題段從數字講起，沒有場景，五拍會變成條列講義。

### 選項 B：資料中心上了選票（推薦）

一行說明：Intro 由 Kai 問「一棟放電腦的房子，美國人為什麼要用投票擋它」，停在答案之前；快訊照對台灣聽眾的影響排、以 OpenAI 談 2028 年把話題交給主題，用 Uber 的 4 趟收尾當 Signal Number；主題段從 Janesville 一張選票講起，順著電費、當選人的條件、高通與記憶體講到接下來看什麼。
開場鉤子：今天的主題，是美國期中選舉裡，一個意外的大題目：AI 資料中心。

排序理由：國際上影響最大、兩家媒體各有數字，又能把同一天的高通、OpenAI 2028 年、Altman 的記憶體、OCC 的 AI 代理串成一條線；
問題在片尾第一句回答。今天沒有台灣新聞，台灣的角度留在主題第 ④ 拍與每則的影響句。

選定：選項 B（理由：有一個貫穿全集、片尾才回答的問題，主題有場景、撐得起五拍；選項 A 的問題在第一則就答完）。
