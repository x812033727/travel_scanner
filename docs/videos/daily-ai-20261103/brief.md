# Tech Signal 11/3：政府網站憑證，星期五前要換新

企劃日期 2026-11-03。每日 Podcast《Tech Signal｜科技訊號》，照 `.agents/skills/youtube-video/references/daily-brief.md`：
`format: "slides"`、`category: "ai-news"`、`theme: "paper"`，slug `daily-ai-20261103`（播出 2026-11-03 星期二，新聞日 2026-11-02），
雙主持（Sola 講新聞、Kai 替觀眾問與翻白話），台灣國語旁白、字卡全英文，目標 20–25 分鐘。
這一集在工作階段裡手做。每則的事實只用站上 news_date 2026-11-02 已發布的文章與它列的來源（2026-11-03 重新打開，皆 HTTP 200），
沒有用到網路補充的新聞；站上文章網址放說明欄，卡片 `source` 寫原始來源。

## 選題

排序依：影響多少台灣觀眾 → 有沒有日期與今天能做的事 → 錢與帳戶安全 → 其他。同一件事的兩篇（Anthropic 訊息串、Mercado Bitcoin）各合成一則。

| 段落 | 新聞（來源：站上文章） | 排在這裡的理由 |
| --- | --- | --- |
| Signal of the Day | TWCA 網站憑證序號亂數只有 24 位元、未達 64 位元以上的國際標準；數發部請 962 個機關、9,772 張憑證 11/6 前更新（站上：https://mokaair.com/zh-TW/life/tech-news-twca-certificate-20261102 ；數位發展部新聞稿） | 理由見下一節 |
| Headlines 1 | OpenAI 將合併 ChatGPT 桌面版的 Chat 與 Work 分頁，ChatGPT 與 Codex 共用額度（站上：https://mokaair.com/zh-TW/life/ai-news-chatgpt-merge-chat-work-tabs-20261102 ；TechCrunch） | 台灣最多人用的 AI 服務；額度共用直接影響重度使用者；單一媒體報導，照實說「據報導」 |
| Headlines 2 | 紐約時報等媒體告 Brave：爬取內容供 AI 使用、讓使用者繞過付費牆（站上：https://mokaair.com/zh-TW/life/ai-news-nyt-sues-brave-ai-scraping-20261102 ；The Verge） | 瀏覽器與 AI 內容的爭議，點名 Anthropic、Perplexity 等 AI 公司；但都是指控、沒有裁決、觀眾沒有要做的事，所以排第二 |
| Headlines 3 | Google DeepMind 的世界模型 Genie 4，研究預覽、只給受信任測試者（站上：https://mokaair.com/zh-TW/life/ai-news-genie-4-research-preview-20261102 ；DeepMind、Google 十月整理） | 好懂、好想像，但台灣一般人現在用不到；10/27 發表、11/2 Google 彙整再提，旁白照實說日期 |
| Headlines 4 | Anthropic Messages API 訊息串（message threads）公開測試版（合併兩篇：https://mokaair.com/zh-TW/life/ai-news-claude-message-threads-20261102 、https://mokaair.com/zh-TW/life/ai-news-message-threads-20261102 ；claude.com、Claude Platform 發布說明） | 只影響開發者；要講清楚「省的是等待時間、不是 token」 |
| Headlines 5 | Google Cloud 的 google-cloud-developer 外掛上架 Antigravity Marketplace（站上：https://mokaair.com/zh-TW/life/ai-news-google-cloud-antigravity-plugin-20261102 ；Google Cloud 部落格） | 開發者向；「啟用收費服務前先問你」對用 AI 代理的人有用，但全是 Google 自述，排在快訊最後 |
| Signal Number | OpenAI 在喬治亞州試辦 Grid Protectors Program，極端天氣最多釋出 1,000 百萬瓦（站上：https://mokaair.com/zh-TW/life/ai-news-openai-grid-protectors-program-20261102 ；The Verge） | 今天最好記的數字（約 70 萬戶的冷氣），當 Headlines 的收尾與 Shorts 素材；台灣沒有直接影響，所以不排成一則快訊 |
| What People Are Saying | Brave 訴狀、紐約時報發言人、Perplexity 首席傳播長；OpenAI 對發電廠的說法與「compute campuses」（同上兩則的來源） | 只引用站上文章列的 The Verge 原文；Brave 一案三方說法正好對照，OpenAI 那句接 Signal Number |
| Money Signal | 巴西 Mercado Bitcoin 資安事件、暫停存提款（合併兩篇：https://mokaair.com/zh-TW/life/crypto-news-mercado-bitcoin-halts-withdrawals-20261102 、https://mokaair.com/zh-TW/life/crypto-news-mercado-bitcoin-hack-freeze-20261102 ；Decrypt、Chainalysis）；Squarespace 裁員約 19%（https://mokaair.com/zh-TW/life/tech-news-squarespace-layoffs-20261102 ；TechCrunch、The Verge）；Trajectory 募得 4,500 萬美元（https://mokaair.com/zh-TW/life/ai-news-trajectory-series-a-20261102 ；TechCrunch） | 交易所出事是「帳戶安全」最值得講的錢的訊號；裁員是工作；Trajectory 是錢流進來的一邊。只講誰說了什麼數字，不談價格、漲跌、買賣 |
| Try This | 看到政府網站跳安全性警示時怎麼做；自家網站用 TWCA 憑證時怎麼做（數發部新聞稿＋節目建議） | 主題那則真的有觀眾能做的事，而且有日期 |
| Noise of the Day | Proton 執行長「loser thinking」風波（站上：https://mokaair.com/zh-TW/life/tech-news-proton-ai-backlash-20261102 ；Decrypt） | 主打隱私的公司說資安測試是失敗者思維，輕鬆、有反差；照 Decrypt 提醒，用戶反應是情緒、不是查證過的退訂數，不嘲笑人 |

## 為什麼是這一則當 Signal of the Day

- 跟台灣的關係不用湊：962 個政府機關、9,772 張網站憑證，數發部自己發的新聞稿。
- 有日期：11 月 6 日（這個星期五）前要更新，否則民眾瀏覽時「可能」看到安全性警示；11/2 晚間只換好 926 張，不到一成。
- 有觀眾今天能做的事（Try This），也有能講透的背景：憑證是什麼、序號裡的亂數為什麼看長度不夠、128 位元只有 24 位元是亂數。
- 有人、有場景：TWCA 系統把新憑證寄給各機關承辦人，故事從那封信講起。
- 誰承擔：機關資訊人員要在幾天內裝好；TWCA 面對第三方檢測、依約罰款與求償；數發部同時是採購方與督促者。
- 接下來要看什麼很清楚：11/6 能否換完、檢測結果、罰款與求償。
- 亞洲其他地方：來源只講台灣，節目明說不猜。

## 觀眾

每天通勤或午休聽 20 分鐘科技新聞的台灣上班族、學生與工程師：天天用政府網站報名、查資料、繳費，用 ChatGPT、Claude、Brave；
有些人管公司網站，或用 AI 代理寫程式。他們要知道「這對我改變了什麼、這星期要不要做什麼」。

## 觀眾看完能做到的事

- 11 月 6 日之後，打開政府網站跳出安全性警示時，知道先停下來、不在跳過警告的頁面輸入密碼或身分證字號、確認網址、晚點再試或打機關電話（節目建議；警示的可能性依數發部新聞稿）。
- 管公司網站的人，會去看憑證是誰發的；是 TWCA 的，就在 11 月 6 日前確認換成新憑證（數發部新聞稿呼籲其他 TWCA 憑證使用者更新）。
- 分得出「憑證不合標準」和「網站被入侵」：數發部說目前沒有造成具體資安危害。
- 重度使用 ChatGPT 與 Codex 的人，知道兩邊之後共用一個額度池（據 TechCrunch）。
- 聽到交易所「凍結被盜資金」時，知道凍結不等於還給原主（Decrypt）。

## 站主觀點

套用立場：2、4、5
（站主還沒在設定分頁存「頻道立場」，條號依 `docs/videos/HANDS-OFF.md` §頻道立場的草稿；這段是提案，給站主在大綱關卡看。）
今天最重要的是 TWCA 的憑證：它有日期、就在台灣、觀眾這星期就可能碰到。我不把它講成「政府網站被駭」——數發部說目前沒有具體資安危害——
但也不輕輕帶過：11/2 晚間只換好不到一成，11/6 能不能全部換完，我老實說不確定。安全靠的是技術上的標準（亂數夠不夠），
不是看起來夠長的序號。其他快訊照實標出「據報導」「公司自己說」「原告的指控」；錢的段落只講帳戶安全與工作，不談價格。

## 不選

- Anthropic 調整 Claude Code 提示詞、避免重製特定遊戲（協調者指示略過；觀眾影響小）。
- Apple 2026 財年第四季財報（純財報數字，跟觀眾的使用沒有直接關係）。
- AWS SageMaker 知識蒸餾示範、Cloudflare DNS 建置改造（企業工程細節，離一般觀眾太遠）。
- Strive 增持比特幣、OKX 與 ICE 代幣化股票遭拒名單（持幣與交易平台的新聞，容易滑向價格與投資話題）。

## 會過期的事實

- TWCA 憑證的更新進度（926／9,772 是 11/2 晚間的數字）、11/6 期限是否延長、第三方檢測結果與罰款金額。
- Brave 訴訟的進度與 Brave 的回應（The Verge 11/2 更新過一次提告方的寫法）。
- Mercado Bitcoin 何時恢復存提款、被盜與凍結金額（各方說法不一，交易所未確認）。
- ChatGPT 合併分頁的開放範圍、Genie 4 的開放對象、訊息串的測試版狀態。
- OpenAI Grid Protectors Program 的協議內容與成效。

## 不做的事

- 不說 TWCA 或政府網站「被駭」；不猜哪些機關在名單上（新聞稿沒有名單）；不猜亞洲其他地方。
- 不解釋國際標準為什麼要求 64 位元以上的亂數（來源沒有說明理由），只講要求是什麼、TWCA 實際是多少；「一千六百多萬種」「一兆倍以上」「不到一成」「一天兩千兩百張」是依新聞稿數字自己算的，卡片標明。
- 不談任何價格、估值走勢、漲跌、買賣時機，不推薦任何交易所、代幣或服務。
- 不把指控（Brave）、公司自述（Google、Anthropic、OpenAI、Trajectory）、單一媒體報導（ChatGPT、Proton）講成已證實。
- 不編主持人的私人經驗；Try This 標明是節目的建議，不是數發部的指示。
- 片尾不提下一集。

## 大綱

### 選項 A：最多人用的先講

一行說明：照使用人數排，ChatGPT 分頁合併當 Cold Open，TWCA 憑證排在快訊之後當主題，Money Signal 與 Try This 照段落表。
開場鉤子：11 月 2 日，據 TechCrunch 報導，OpenAI 寄信通知使用者，ChatGPT 桌面版的兩個分頁要合併，額度也要跟 Codex 共用。

排序理由：ChatGPT 是台灣最多人用的 AI 服務，開場最好懂。缺點：開場是單一媒體轉述的郵件內容，沒有日期壓力，
觀眾聽完也沒有一定要做的事；真正有期限、就在台灣的那則要等到第七分鐘才出現。

### 選項 B：有期限、就在台灣的先講（推薦）

一行說明：Cold Open 就從 TWCA 憑證通報講起，停在「過了 11 月 6 日會怎樣」；快訊照影響排，主題段從承辦人收到新憑證的那封信講起，Try This 接主題。
開場鉤子：10 月 30 日，國際社群 Bugzilla 上一則通報，點名台灣網路認證公司發給九百六十二個政府機關的網站憑證。

排序理由：開場是官方新聞稿的事實，有日期、有數字、直接關係台灣觀眾，停在影響之前讓整集有一個要回答的問題（星期五之後打開這些網站會怎樣）；
片尾第一句回答它。快訊從最多人用的 ChatGPT 排到只影響開發者的兩則，用 OpenAI 的 1,000 百萬瓦收尾當 Signal Number。

選定：選項 B（理由：唯一有日期、有觀眾能做的事、又完全在台灣的一則放在開場，符合 daily-brief「Cold Open 用主題那則最意外的一句」；
選項 A 的開場是沒有期限的單一媒體報導，主題要等太久）。
