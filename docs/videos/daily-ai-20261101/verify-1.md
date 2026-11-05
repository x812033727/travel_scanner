# daily-ai-20261101 查核第 1 輪

查核日 2026-11-02。查核代理不是撰稿人。每一條旁白（`text`，本片沒有 `say`）、每張卡片的 `data`（含 `source` 欄）、縮圖、`youtube.title`、`description`、`tags` 都抽出來逐條對照：
站上 7 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，全部 HTTP 200、`status: published`）與 `video.json` `sources` 列的 7 個官方頁或報導，2026-11-02 全部重新打開；另外打開 Google Cloud 支出上限的說明文件（O1d），因為部落格沒有寫適用對象與適用服務。

## 來源代號

站上文章（全部 200）：

| 代號 | slug | news_date |
| --- | --- | --- |
| S1 | tech-news-google-cloud-spend-caps-20261030 | 2026-10-30 |
| S2 | ai-news-openai-funding-target-20261031 | 2026-10-31 |
| S3 | ai-news-xai-naacp-lawsuit-20261031 | 2026-10-31 |
| S4 | tech-news-project-suncatcher-satellite-response-20261030 | 2026-10-30 |
| S5 | ai-news-doordash-agent-orders-20261030 | 2026-10-30 |
| S6 | ai-news-gpt-rosalind-6-system-card-20261030 | 2026-10-30 |
| S7 | ai-news-pope-leo-lethal-autonomous-weapons-20261030 | 2026-10-30 |

官方頁與報導（2026-11-02 重開，全部 HTTP 200，沒有轉址、沒有頁面拒絕容器）：

| 代號 | URL |
| --- | --- |
| O1 | https://cloud.google.com/blog/topics/cost-management/google-cloud-spend-caps-now-generally-available/ （October 30, 2026） |
| O1d | https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps （Last updated 2026-10-26 UTC；本輪新加進 `sources`） |
| O2 | https://techcrunch.com/2026/10/31/openai-reportedly-lowers-funding-target-for-new-round/ （9:12 AM PDT · October 31, 2026） |
| O3 | https://techcrunch.com/2026/10/31/judge-allows-naacp-lawsuit-over-xai-data-center-pollution-to-move-forward/ （2:17 PM PDT · October 31, 2026） |
| O4 | https://blog.google/innovation-and-ai/models-and-research/google-research/project-suncatcher-satellite-response/ （Oct 30, 2026） |
| O5 | https://techcrunch.com/2026/10/30/doordash-said-its-only-received-several-hundred-orders-from-ai-agents/ （6:54 AM PDT · October 30, 2026） |
| O6 | https://deploymentsafety.openai.com/gpt-rosalind-6 （Published October 30, 2026） |
| O7 | https://www.theverge.com/ai-artificial-intelligence/1023188/pope-leo-disarm-ai （Oct 30, 2026, 2:58 PM UTC） |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 月 30 日 Google Cloud 宣布支出上限正式推出 | ru7q；open.data.subtitle | O1、S1 | 200 | CONFIRMED（O1 October 30, 2026：「Today, we're announcing that spend caps on Google Cloud Budgets are generally available」；S1 news_date 10-30） | |
| 2 | 預算用完，雲端用量就自動暫停 | xatk；open.data.key | O1、O1d | 200 | CONFIRMED（開場簡化，例外在 g-except 揭曉；只適用符合資格的服務，見「懷疑但沒改」） | |
| 3 | 「有一種用量」碰到上限也不會停 | 9cf8；loops[0].what；youtube.title | O1、O1d | 200 | CHANGED（O1 只舉 Provisioned Throughput，但 O1d：「Spend caps don't pause any on-going, fixed usage associated with persistent resources (such as compute and storage services), which remain active and continue to accrue charges」；不會停的不只一種） | 9cf8「可是有一種用量，碰到上限也不會停。」→「可是有些用量，碰到上限也不會停。」；loops[0].what「…的那一種用量」→「…的用量」；標題「但有一種不會停」→「但有些不會停」 |
| 4 | 同一個週末，多家媒體報導 OpenAI 下調新一輪募資目標 | iknv；open-oa | O2、S2 | 200 | CONFIRMED（「according to multiple news reports」；O2 10-31 週六） | |
| 5 | open-oa kicker「10 月 31 日 · 據報導」、sub「TechCrunch 引述多家媒體；OpenAI 未證實」 | open-oa.data | O2 | 200 | CONFIRMED | |
| 6 | Google 送上太空的 AI 晶片傳回第一個回答，是一首詩 | yk7k、ppmg；open-sat | O4、S4 | 200 | CONFIRMED（first-ever AI response … haiku） | |
| 7 | 週末版，補上週五和週六的新聞 | j8kb | S1–S7 | 200 | CONFIRMED（2026-10-30 是週五、10-31 是週六；七篇 news_date 五篇 10-30、兩篇 10-31） | |
| 8 | 煞車裝在 Google Cloud 的預算工具裡，支出上限從預覽版轉成正式版 | rpf4；g-open.sub | O1 | 200 | CONFIRMED（「since the initial preview」「generally available」） | |
| 9 | 超過預算會暫停用量，不會刪掉資源 | 3gjh；g-open.text | O1、O1d | 200 | CONFIRMED（「without risking resource deletion」） | |
| 10 | g-open kicker「10 月 30 日 · Google Cloud」 | g-open.data.kicker | O1 | 200 | CONFIRMED | |
| 11 | 正式版多了三件事 | 4uc7；g-three.title | O1 | 200 | CONFIRMED（three major updates） | |
| 12 | 可以用 API 設上限，開新的測試專案時直接套上 | 5vxr；g-three.steps[0] | O1 | 200 | CONFIRMED（spend caps API … whenever a developer spins up a new sandbox project） | |
| 13 | AI 服務的上限用估算的即時成本，用量發生後幾分鐘內觸發 | nqd4；g-three.steps[1] | O1 | 200 | CONFIRMED（「trigger within minutes of usage using estimated, live costs」） | |
| 14 | 被擋下的服務下個月初自動恢復，不用再手動解除 | hew4；g-three.steps[2] | O1、O1d | 200 | CONFIRMED（automated monthly resets；手動覆寫仍在，卡片沒說沒有） | |
| 15 | g-three 卡片來源「Google Cloud 部落格 2026-10-30」 | g-three.data.source | O1 | 200 | CONFIRMED | |
| 16 | 開場說有一種用量不會停，就在這裡 | n8n7；g-except.keys[0] | O1d | 200 | CHANGED（依 #3） | 「開場說有一種用量不會停」→「開場說有些用量不會停」；keys[0]「有一種用量不會停」→「有些用量不會停」 |
| 17 | 隨用隨付與承諾使用折扣涵蓋的請求碰到上限會暫停 | n5u4；g-except.left | O1、O1d | 200 | CONFIRMED（「halt pay-as-you-go and CUD-covered requests」） | |
| 18 | 用預留容量跑的 Provisioned Throughput 不會被暫停 | mu9u；g-except.right | O1、O1d | 200 | CHANGED（PT 本身對，但卡片與旁白把它當成唯一的例外；O1d 另有常駐資源的固定用量不暫停、照常計費） | mu9u「但用預留容量跑的 Provisioned Throughput，不會被暫停，會照常執行。」→「但預留容量的 Provisioned Throughput 照常執行，常駐的運算和儲存也照樣計費。」；right.points[1]「預留容量照常執行」→「常駐的運算與儲存資源」；keys[2]「預留容量：照常執行」→「預留容量、常駐資源：照常」；source「Google Cloud 部落格 2026-10-30」→「Google Cloud 部落格 2026-10-30、支出上限說明文件」 |
| 19 | 對在台灣用 Google Cloud 跑 AI 的你，今天就能做 | ryzv；g-do.title、keys[0] | O1、O1d | 200 | CHANGED（O1、O1d 都沒有地區限制，也沒有提到台灣，GA 且「Get started today」，所以「今天就能做」成立；但 O1d：「Spend cap budgets are limited to first-party Google Cloud customers. Reseller accounts are out of scope.」在台灣透過經銷商開帳戶的人做不到） | ryzv「…這是今天就能做的事。」→「…只要帳戶不是透過經銷商開的，今天就能做。」；g-do.source →「Google Cloud 部落格 2026-10-30｜經銷商帳戶不適用（說明文件）」 |
| 20 | 到計費控制台的預算頁面設第一個支出上限；卡片「Budgets and Alerts」 | 7nwk；g-do.steps[0] | O1 | 200 | CONFIRMED（「navigate to the Budgets and Alerts page in your Google Cloud Billing Console, to set your first spend cap」；頁面名稱是原文，不是編的選單路徑） | |
| 21 | Google 建議先從測試專案開始，設嚴格、金額低的上限 | fayx；g-do.steps[1] | O1 | 200 | CONFIRMED（Target non-production environments first … strict, low-dollar spend caps） | |
| 22 | 用到一定比例時，預設通知計費管理員和專案擁有者；卡片 50%、80%、100% | wrj5；g-do.steps[2] | O1、O1d | 200 | CONFIRMED | |
| 23 | 先確認這兩個角色上有對的人 | ez5s | O1 | 200 | CONFIRMED（Make sure the right folks are set up in these roles） | |
| 24 | 你的帳單有了煞車，AI 公司的錢也有人踩煞車 | wtmi | — | — | OUT OF SCOPE（串場） | |
| 25 | 10 月 31 日，TechCrunch 引述金融時報報導 | repi；o-open.source | O2、S2 | 200 | CONFIRMED（TechCrunch October 31；FT 是「reported Friday」即 10-30，日期掛在 TechCrunch 上，正確） | |
| 26 | 募資目標從原本傳的數字降到 200 億美元；卡片先前 300 億美元 | qm94；o-open.rows[0] | O2 | 200 | CONFIRMED（$30 billion → $20 billion） | |
| 27 | 華爾街日報後續報導：已籌到 110 億美元；卡片先前「未提及」 | dt7g；o-open.rows[1] | O2 | 200 | CONFIRMED | |
| 28 | 領投的是一群阿聯投資人 | 82ee；o-open.rows[2] | O2 | 200 | CHANGED（事實對，但這是《金融時報》說的；82ee 緊接在「華爾街日報的後續報導說」之後，聽起來像 WSJ 說的） | 「領投的會是一群阿拉伯聯合大公國的投資人。」→「金融時報則說，領投的會是一群阿拉伯聯合大公國的投資人。」 |
| 29 | 部分大型投資人反應冷淡；卡片引句與「引述《華爾街日報》」 | ynw6；o-tepid | O2 | 200 | CHANGED（引句逐字相符，出自 WSJ；82ee 改後「同一篇報導」會指到 FT） | 「同一篇報導也說，…」→「華爾街日報也說，…」 |
| 30 | TechCrunch 認為部分原因是時機不好：華爾街對 AI 基礎建設大筆支出越來越謹慎 | n94a、3m7v；o-why | O2 | 200 | CONFIRMED（「could be blamed, in part, on bad timing … wary of heavy AI infrastructure spending」，已標 TechCrunch 認為） | |
| 31 | 這些都是媒體報導，不是 OpenAI 的正式公告；TechCrunch 已去問、報導裡沒有回應 | 6ib9、htgq；o-you | O2、S2 | 200 | CONFIRMED（「TechCrunch has reached out to OpenAI for comment」） | |
| 32 | 報導沒有說這會影響 ChatGPT 的產品或服務 | 8c2e；o-you.sub | O2、S2 | 200 | CONFIRMED（O2 全文沒有談產品；S2：「報導沒有說明這會如何影響 OpenAI 的產品或服務」） | |
| 33 | 要看 OpenAI 自己怎麼說、最後實際募到多少 | b9ni | S2 | 200 | OUT OF SCOPE（頻道建議，與 S2 一致） | |
| 34 | 華爾街擔心花太多錢；地面上資料中心的鄰居也有意見 | rkut | O2、O3 | 200 | CONFIRMED（串場，依 #30 與 O3 的反彈） | |
| 35 | 10 月 31 日，TechCrunch 報導，聯邦法官駁回 xAI 撤銷訴訟的聲請 | 2hw3；x-open | O3、S3 | 200 | CONFIRMED（日期掛在 TechCrunch 上；S3 news_date 10-31） | |
| 36 | x-open kicker「10 月 31 日 · 美國聯邦法院」 | x-open.data.kicker | O3 | 200 | CONFIRMED（日期是報導日，O3 沒寫裁定日；見「懷疑但沒改」） | |
| 37 | 告它的是 NAACP，美國全國有色人種協進會 | zdhc | O3、S3 | 200 | CONFIRMED（由南方環境法律中心代表提告，旁白沒說錯） | |
| 38 | 指控 xAI 沒取得空氣許可，就在孟菲斯附近的 Colossus 運轉供電用的燃氣渦輪機 | m5dk、rpfx；x-open.sub | O3 | 200 | CONFIRMED（「outside Memphis」，已標指控） | |
| 39 | xAI：渦輪機是移動式、不需許可，原告沒資格告 | 74pv；x-dispute.left | O3 | 200 | CONFIRMED | |
| 40 | 法官：不屬於移動污染源，原告有資格提告 | 32c6；x-dispute.right | O3 | 200 | CONFIRMED（Judge Debra M. Brown：statutory standing under the Clean Air Act；not 'mobile sources' under Mississippi's SIP） | |
| 41 | 只代表可以繼續審，不是判 xAI 違法；違規仍是原告指控 | 3wrt、vq47；x-not | O3、S3 | 200 | CONFIRMED（「the plaintiffs' claims will proceed」；S3「這不是最終判決」） | |
| 42 | 原告指控至少 35 台渦輪機未取得許可 | x-not.sub | O3 | 200 | CONFIRMED（「at least 35 combustion turbines」） | |
| 43 | TechCrunch 形容美國輿論似乎已急轉、反對資料中心 | hqkk；x-bg.keys[0] | O3 | 200 | CONFIRMED（「seems to have turned sharply」，「似乎」保留） | |
| 44 | 紐約最近通過暫停新建資料中心；其他州與地方考慮跟進 | 4ah8、mkn6；x-bg.items | O3 | 200 | CONFIRMED（moratorium） | |
| 45 | Amazon、微軟承諾跟政府機關往來時不再用保密協議 | 3h4i；x-bg.items[2] | O3 | 200 | CONFIRMED | |
| 46 | 台灣沒有要你動手的地方 | aiae | — | — | OUT OF SCOPE（頻道判斷） | |
| 47 | TechCrunch 說這波反彈可能成為美國即將到來的期中選舉的重要因素；後續審理時程未公布 | 4g52；x-watch | O3、S3 | 200 | CONFIRMED（「could be a significant factor in the imminent U.S. midterm elections」；S3「報導沒有提供後續時程」） | |
| 48 | 地上的資料中心有人反對；Google 研究把 AI 運算搬到太空 | mbh9；s-open.keys[0] | O4 | 200 | CONFIRMED（「explore powering AI compute in space」） | |
| 49 | 10 月 30 日 Google 宣布收到 Suncatcher 原型衛星的第一個回應 | 9a8s | O4、S4 | 200 | CONFIRMED（Oct 30, 2026） | |
| 50 | 衛星一個月前才發射；卡片 10/1 | c563；s-open.stats[0] | O4 | 200 | CONFIRMED（「On October 1, we launched」，相對 10-30 約一個月） | |
| 51 | TPU 跑 Gemma 4 開放模型 | 2z8e；s-open.stats[1] | O4 | 200 | CONFIRMED（onboard Gemma 4 open model） | |
| 52 | 地面站把題目傳上去，要它寫一首關於身在太空的俳句 | m9gk | O4 | 200 | CONFIRMED | |
| 53 | 經過挪威斯瓦巴時傳回，證明測試成功 | asia、wr7z | O4 | 200 | CONFIRMED（「As the satellite passed by Svalbard, Norway, the downlinked poem confirmed success」） | |
| 54 | 俳句三行原文；第一句「下方是一顆藍色的彈珠」 | kbib；s-poem.quote | O4 | 200 | CONFIRMED（逐字相符，句尾 emoji 省略；中譯是頻道譯的） | |
| 55 | Google 說這是資料中心等級的 TPU 在軌道上的第一次；只有 Google 自己說 | xgeq、mppu；s-claim | O4、S4 | 200 | CONFIRMED（「first-ever AI response from a data center class TPU in orbit」，已標自述） | |
| 56 | 接下來測耐熱、抗輻射；2027 年兩顆衛星互連 | enr4、yrr8、9dz8；s-next | O4 | 200 | CONFIRMED（thermal stress and radiation exposure；twin interconnected satellites in 2027） | |
| 57 | 早期技術驗證，沒有可以用的服務；公告沒有提到成本、規模、商業服務時間表 | ns9z、4dzi；s-you | O4、S4 | 200 | CONFIRMED（O4 全文沒有成本、規模、時程） | |
| 58 | 卡片來源「Google 部落格 2026-10-30」（s-open、s-poem、s-next） | s-*.data.source | O4 | 200 | CONFIRMED | |
| 59 | AI 在太空寫詩；地上替你點餐的 AI 代理呢 | rrmh | — | — | OUT OF SCOPE（串場） | |
| 60 | 10 月 30 日，DoorDash 在財報電話會議上被分析師問到 AI 代理下單 | 5qw9、znn9；d-open.source | O5、S5 | 200 | CHANGED（S5 news_date 10-30 是 TechCrunch 的報導日，O5 發於 10-30 6:54 AM PDT，沒寫電話會議日期；原句說電話會議在 10-30，來源不能證實） | 5qw9「10 月 30 日，美國外送平台 DoorDash 在財報電話會議上，」→「10 月 30 日，TechCrunch 報導，美國外送平台 DoorDash 在財報電話會議上，」 |
| 61 | 執行長回答：其他公司做的 AI 代理總共大概只帶來幾百筆訂單；卡片引句 | yah9、qkvz；d-open.quote | O5 | 200 | CONFIRMED（「we're seeing maybe several hundred orders in total from some of these third-party agents」逐字） | |
| 62 | DoorDash 平均每天完成 300 萬筆外送（2025 年報告） | xanw；d-scale.stats[1] | O5 | 200 | CONFIRMED | |
| 63 | 用戶主要還是用 DoorDash 自己的 App 下單 | e47s | O5 | 200 | CONFIRMED（predominantly placing orders through DoorDash's app） | |
| 64 | 不要逆勢，也不要有幻想 | d52x；d-ceo | O5 | 200 | CONFIRMED（「never want to fight gravity … don't want to be delusional」，意譯） | |
| 65 | 想了解 AI 代理怎麼被使用，未來可能在代理裡放廣告 | 972k；d-ceo.sub | O5 | 200 | CONFIRMED | |
| 66 | 自家代理：聊天機器人 6 月、命令列 7 月、文字下單 9 月，今年陸續推出 | 84ih；d-own.rows | O5 | 200 | CONFIRMED（O5 連到 techcrunch.com/2026/06/11、2026/07/16、2026/09/30，年份是 2026） | |
| 67 | Amazon 一直在封鎖個人代理；Walmart 敞開大門搶生意 | 8kh5、nek4；d-door | O5 | 200 | CONFIRMED（「laid out a red carpet … to snag some business from its competitors」） | |
| 68 | 至少在這家外送平台，用的人還非常少 | hr7t、5nbf；d-you | O5、S5 | 200 | CONFIRMED（依 #61、#62） | |
| 69 | AI 代理沒什麼人用；另一種 AI 是刻意不讓一般人用 | befq | O6 | 200 | CONFIRMED（only made available via trusted access） | |
| 70 | 10 月 30 日 OpenAI 公布 GPT-Rosalind-6 系統卡補充文件 | 5ijc；r-open | O6、S6 | 200 | CONFIRMED（Published October 30, 2026） | |
| 71 | 給生物學、藥物研發用的模型 | 7c8s | O6 | 200 | CONFIRMED（biology, drug discovery, and translational medicine） | |
| 72 | 只開放給審核過的科學家、研究機構、企業和政府夥伴 | nxwy；r-open.text | O6 | 200 | CONFIRMED | |
| 73 | 跟旗艦推理模型 GPT-6 Astra 用同一組權重 | txcc；r-same.left | O6 | 200 | CONFIRMED（「uses the same weights as GPT-6 Astra, our flagship reasoning model」） | |
| 74 | 可能被濫用的生物問題拒答較少；仍拒絕生物武器化；只透過受信任存取 | aw47、sm2h；r-same.right | O6 | 200 | CONFIRMED（fewer refusals on dual-use biological queries） | |
| 75 | 生物與化學列為高能力，低於關鍵；網路安全沿用 Astra 評估列為關鍵 | gpc9、gt9b；r-risk | O6 | 200 | CONFIRMED（High … below the threshold for Critical；Critical in Cybersecurity，已標 OpenAI 自己的分級） | |
| 76 | 不是每一項安全測試都比母模型好；警告後繞過限制的比率比 Astra 高；21.7% 對 18.9% | rc22、9yyg；r-not | O6 | 200 | CONFIRMED（Respecting Warnings 21.7% vs 18.9%，越低越好；Agent Replay 27.1% vs 26.7% 也較差） | |
| 77 | 申請要通過使命、用途和治理的審核 | wtbk；r-you.steps[0] | O6 | 200 | CONFIRMED（legitimate mission, credible use case, governance, ability to safely control access） | |
| 78 | 只讓有正當需要的人用，權限最小 | a2qf；r-you.steps[1] | O6 | 200 | CONFIRMED（authorized users with a legitimate need … least-privilege） | |
| 79 | 輸出先經合格的人審查，才能用在實驗或重大決策 | 2u6m；r-you.steps[2] | O6 | 200 | CONFIRMED（qualified human review before model outputs inform experiments, publications, or consequential decisions） | |
| 80 | 台灣的機構能不能申請，補充文件沒有寫 | vqed | O6、S6 | 200 | CONFIRMED（O6 全文沒有國家或地區） | |
| 81 | Rosalind 卡片來源「OpenAI 系統卡補充文件 2026-10-30」等 | r-*.data.source | O6 | 200 | CONFIRMED | |
| 82 | Rosalind 輸出要先經人審查；教宗要更大範圍的人類把關 | 3gj2 | O6、O7 | 200 | CONFIRMED（串場） | |
| 83 | 10 月 30 日 The Verge 報導，教宗良十四世在週五的演說中說 AI 應被解除武裝，機器是工具不是人 | k9r3、3kcs；p-open | O7、S7 | 200 | CONFIRMED（Oct 30, 2026；「In Friday's Papal Address」「disarmed」「Machines are tools, not persons」） | |
| 84 | 呼籲聯合國會員國下個月在日內瓦開會時採取具體步驟，禁止致命自主武器 | 59yh、8mnv；p-ask.items[0..1] | O7 | 200 | CONFIRMED（致命自主武器的解釋出自 S7） | |
| 85 | 影響人命、自由和使用武力的決定，必須受到人類有效的監督 | xjg9；p-ask.items[2] | O7 | 200 | CONFIRMED | |
| 86 | 2024 年前任教宗方濟各也呼籲禁止自主武器；卡片引句譯文 | 5ra9；p-bg | O7 | 200 | CONFIRMED（「No machine should ever choose to take the life of a human being」） | |
| 87 | 一項呼籲，報導沒有提到有約束力的決定；日內瓦議程與結果未說明 | umgf、eur4；p-watch | O7、S7 | 200 | CONFIRMED | |
| 88 | 我的看法、我不確定的、留言題 | v-main、v-unsure、closing | brief.md | — | OUT OF SCOPE（觀點，見下） | |
| 89 | 縮圖「帳單**自動煞車**」「OpenAI 傳降募資目標、太空 TPU 寫詩」 | thumbnail.data | O1、O2、O4 | 200 | CONFIRMED（「傳」標明是傳聞或報導） | |
| 90 | 標題「雲端 AI 帳單能設上限了，但有一種不會停｜AI 科技快報 週末版」 | youtube.title | O1d | 200 | CHANGED（依 #3） | 「但有一種不會停」→「但有些不會停」 |
| 91 | 說明欄：補上 10 月 30 日與 31 日七則；OpenAI 是 TechCrunch 轉述 FT、WSJ，OpenAI 未證實；Google「第一次」與 OpenAI 評測分級是自述；xAI 只是可以續審 | youtube.description | O2、O3、O4、O6 | 200 | CONFIRMED | |
| 92 | 說明欄 7 個 Mokaair 網址 | youtube.description | S1–S7 | 200 | CONFIRMED（七篇都 published，API 200） | |
| 93 | tags | youtube.tags | — | — | OUT OF SCOPE | |

## OpenAI 募資那則：留或拿掉

**判定：留。** daily-brief 第一節第 4 條「不選：沒有官方來源的傳聞」針對的是來路不明、沒有具名來源的說法。這一則是 TechCrunch 具名轉述《金融時報》與《華爾街日報》兩家主要財經媒體的原創報導，有具體數字與出處，站上文章 S2 已發布並標「OpenAI 尚未證實」。影片把它當報導講，而不是當事實：章首卡 kicker「據報導」、sub「OpenAI 未證實」；旁白 repi、dt7g、82ee、ynw6 每個數字都掛在 TechCrunch、金融時報、華爾街日報名下（82ee、ynw6 本輪修正了 FT、WSJ 張冠李戴）；o-you 整張卡講「是媒體報導、OpenAI 還沒回應」，也講了「報導沒說會影響 ChatGPT」；v-unsure 再說一次「還只是報導」；說明欄、縮圖的「傳」也都標明。它排在第二、不當開場，開場那句也不唸數字。在這些標示下，觀眾不會把它當成 OpenAI 的公告，所以留。規則字面上的「沒有官方來源」確實沒有滿足，這是編輯判斷，交站主在大綱關卡定；站主要拿掉時，撰稿人在 claims.md 已列好替換的文章。

## 摘要

- 查了 93 條：CONFIRMED 79、CHANGED 8（列）、NOT FOUND 0、OUT OF SCOPE 6。事實改動 5 處：(1) Google Cloud「有一種用量不會停」改「有些」並補上常駐資源（9cf8、n8n7、mu9u、g-except 卡、loops、標題）；(2) 「今天就能做」加上經銷商帳戶不適用（ryzv、g-do.source）；(3) 阿聯領投改掛《金融時報》（82ee）；(4) 「同一篇報導」改「華爾街日報也說」（ynw6，隨 (3)）；(5) DoorDash 的 10 月 30 日改掛在 TechCrunch 報導上（5qw9）。
- 「今天就能做」：支持，有條件。O1 是 10-30 的全球 GA、寫「Get started today」，O1 與 O1d 都沒有地區限制；O1d 寫明只限直接向 Google 買的客戶（經銷商帳戶不適用），且只適用 Gemini API、Gemini Enterprise Agent Platform（前 Vertex AI）、Cloud Run、Cloud Run functions，一個預算管一個專案的一項服務。旁白已補經銷商的條件；適用服務清單沒有上卡（見「懷疑但沒改」）。
- 唸出來的日期：ru7q、9a8s、5ijc、k9r3 的 10 月 30 日與 repi、2hw3 的 10 月 31 日都等於站上文章的 news_date，也等於官方頁或報導的發布日；5qw9 的 10 月 30 日是報導日不是電話會議日，已改成掛在 TechCrunch 上。repi 的 FT 原報導是週五（10-30），旁白日期掛在 TechCrunch 上，正確。
- `sources` 7 個網址 2026-11-02 全部 HTTP 200；新增 O1d（說明文件，Last updated 2026-10-26），`checked_on` 全部 2026-11-02。
- 會過期的事實：OpenAI 募資目標、已籌金額、領投方（O2，2026-10-31，OpenAI 回應或交割後會變）；Google Cloud 支出上限的適用服務與經銷商限制（O1d，Last updated 2026-10-26）；xAI 案進度（O3，2026-10-31，無時程）；Suncatcher 的測試與 2027 里程碑（O4，2026-10-30）；日內瓦會議（O7，「next month」，2026 年 11 月）。
- 觀點：v-main、v-unsure 以「我的看法是」「我不確定的是」標成觀點，與 brief.md〈站主觀點〉（提案）一致；kx9f「唯一一則讓你今天就能設防線」在加了經銷商條件後仍成立。沒有不一致。
- 聽眾檢查（只報告）：超過 40 字的句子 11 句（全形與拉丁字母逐字計）：rpf4 43、mu9u 49、ryzv 47、2hw3 48、4g52 44、9a8s 54、5qw9 49、84ih 41、5ijc 44、txcc 41、gpc9 42；mu9u、ryzv、5qw9 是本輪改的。沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後。撰稿人新增的字典詞（Provisioned、Throughput、Colossus、Suncatcher、Gemma、DoorDash、Rosalind 等）仍未試聽。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261101` → `daily-ai-20261101: 0 errors, 2 warnings`（「10」7 句、「30」5 句，是每則第一句報日期的結果；估計 10.5 分鐘，108 句）。
- 懷疑但沒改：
  - xatk「預算用完，雲端用量就自動暫停」與 3gjh：上限只對 O1d 列的四項服務有效、一次一個專案一項服務；開場是簡化，mu9u 已說有些用量不停，所以沒改。若站主要更精確，可在 g-do 卡加一行「適用 Gemini API、Vertex AI、Cloud Run」。
  - O1d：「the enforcement of spend caps isn't instant and any cost overages are billed as normal」，觸發後已進行中的請求照收費。影片沒說「一毛都不會多收」，沒改。
  - x-open kicker「10 月 31 日 · 美國聯邦法院」：10-31 是 TechCrunch 報導日，O3 沒寫裁定日；旁白 2hw3 已掛在 TechCrunch 上，卡片沒改，可改成「10 月 31 日 · TechCrunch」。
  - o-tepid 的引句是 TechCrunch 轉述 WSJ 的英文句子，不是 WSJ 原文；卡片來源寫「TechCrunch｜引述《華爾街日報》」，正確，沒改。
  - 3kcs 把「解除武裝」與「機器是工具，不是人」連成一句；O7 兩句都出自同一場演說，沒改。
  - daily-brief「沒有官方來源的傳聞」這條規則對「具名媒體報導、公司未回應」沒有明說；建議站主在 daily-brief.md 補一句，免得主機工人下次判法不同。
- 需要第二輪：**是**。本輪改了 5 個事實（超過 3 個），要由另一個代理寫 `verify-2.md`。第二輪完成前，這份稿子不能稱為已查核。
