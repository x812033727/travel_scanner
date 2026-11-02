# daily-ai-20261101 主張與證據

每一行：編號｜主張（旁白或卡片上的說法）｜站上文章；官方來源｜來源查證日｜場景 id。
撰稿只用站上已發布文章（10/30 五則、10/31 兩則，`/api/travel/guides/life/<slug>?locale=zh-TW` 取得）的內文與它們列的來源；
撰稿人 2026-11-02 逐頁重新打開七個來源頁（皆 HTTP 200），下面的英文引句都是當天頁面上的原文。
「自述」表示是該公司自己公布、沒有第三方確認的說法，旁白與卡片都標了是誰說的。

## 開場

c1｜10 月 30 日 Google Cloud 宣布 Budgets 的支出上限正式推出（generally available）｜https://mokaair.com/zh-TW/life/tech-news-google-cloud-spend-caps-20261030 ; https://cloud.google.com/blog/topics/cost-management/google-cloud-spend-caps-now-generally-available/｜2026-11-02｜open, g-open
c2｜「預算用完，你指定的雲端服務就自動暫停」是開場的簡化；上限一次只管一個專案的一項符合資格的服務（說明文件：Gemini API、Agent Platform（前 Vertex AI）、Cloud Run、Cloud Run functions），查核第 2 輪把原本的「雲端用量就自動暫停」改成「你指定的雲端服務」，開場卡 key 跟著改；例外（預留容量的 Provisioned Throughput、常駐資源）在第一章 g-except 揭曉（loop 9cf8 → mu9u）｜同上（"Spend caps halt pay-as-you-go and CUD-covered requests… Provisioned Throughput is never halted"）｜2026-11-02｜open, g-except
c3｜多家媒體報導 OpenAI 下調新一輪募資目標（開場不唸數字）｜https://mokaair.com/zh-TW/life/ai-news-openai-funding-target-20261031 ; https://techcrunch.com/2026/10/31/openai-reportedly-lowers-funding-target-for-new-round/｜2026-11-02｜open-oa
c4｜Google 太空原型衛星上的 TPU 傳回第一個 AI 回應，是一首俳句｜https://mokaair.com/zh-TW/life/tech-news-project-suncatcher-satellite-response-20261030 ; https://blog.google/innovation-and-ai/models-and-research/google-research/project-suncatcher-satellite-response/｜2026-11-02｜open-sat
c5｜「週末版，補上週五和週六的新聞」：2026-10-30 是週五、10-31 是週六；七則的 news_date 分別是 10-30（五則）與 10-31（兩則）｜站上文章的 news_date｜2026-11-02｜open-sat

## 1 Google Cloud 支出上限

c6｜支出上限從預覽版轉為正式版；達到預算後暫停用量，不會刪除資源（"protect your workloads from runaway costs without risking resource deletion"）｜https://cloud.google.com/blog/topics/cost-management/google-cloud-spend-caps-now-generally-available/｜2026-11-02｜g-open
c7｜正式版三項更新：支出上限 API（可從 Cloud Billing Budgets API 存取，可在開發者建立新的沙盒專案時立即套用上限）；AI 服務的上限依估算即時成本在用量發生後數分鐘內觸發，可在 Cost Reports 查看；每月自動重置，被封鎖的服務在下個月初恢復，手動覆寫照舊｜同上｜2026-11-02｜g-three
c8｜碰到上限會暫停：隨用隨付與 CUD（承諾使用折扣）涵蓋的請求；不會暫停：Provisioned Throughput，預留容量的請求照常執行；常駐資源（運算、儲存）的固定用量也不暫停、照常計費（查核第 1 輪依說明文件補上，9cf8、n8n7、標題由「有一種」改「有些」；第 2 輪為縮短把 mu9u 的產品名留在卡片上，旁白說「預留容量的請求」，即部落格的 "requests using reserved capacity will continue to run"）｜同上 ; https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps （"Spend caps don't pause any on-going, fixed usage associated with persistent resources (such as compute and storage services)"，Last updated 2026-10-26）｜2026-11-02｜g-except
c9｜到 Google Cloud Billing Console 的 Budgets and Alerts 頁面設第一個支出上限（旁白說「計費控制台的預算頁面」，卡片寫頁面原名）｜同上｜2026-11-02｜g-do
c10｜Google 建議先對非正式環境（開發者沙盒、測試叢集、實驗性 AI 代理環境）套用嚴格、低金額的上限｜同上｜2026-11-02｜g-do
c11｜預設在上限的 50%、80%、100% 通知計費管理員與專案擁有者，建議確認這些角色有對的人（旁白「用到一定比例時」，比例只上卡片）｜同上｜2026-11-02｜g-do
c12｜「對在台灣用 Google Cloud 跑 AI 的你，這是今天就能做的事」：依正式推出（GA）與控制台路徑推出；公告沒有列地區限制，也沒有提到台灣，這是頻道的推論。查核第 1 輪：說明文件也沒有地區限制，但「limited to first-party Google Cloud customers. Reseller accounts are out of scope」，且只適用 Gemini API、Gemini Enterprise Agent Platform（前 Vertex AI）、Cloud Run、Cloud Run functions，一個預算只管一個專案的一項服務；旁白改成「帳戶不是經銷商開的，今天就能做」（第 2 輪縮短措辭）｜同上 ; https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps｜2026-11-02｜g-do

## 2 OpenAI 募資目標

c13｜TechCrunch 2026-10-31 引述《金融時報》：OpenAI 把融資目標下調至 200 億美元，首次交割預計更低；先前報導為 300 億美元（卡片），估值先 1.4 兆後 1.25 兆美元（未上卡）｜https://mokaair.com/zh-TW/life/ai-news-openai-funding-target-20261031 ; https://techcrunch.com/2026/10/31/openai-reportedly-lowers-funding-target-for-new-round/｜2026-11-02｜o-open
c14｜《華爾街日報》後續報導：已籌得 110 億美元｜同上｜2026-11-02｜o-open
c15｜《金融時報》：將由一群阿拉伯聯合大公國投資人領投（"The round will be led by a group of investors from the United Arab Emirates"）；旁白 82ee 原接在《華爾街日報》那句後面、像是 WSJ 說的，查核第 1 輪改成「金融時報則說」，ynw6 的「同一篇報導」改成「華爾街日報也說」｜同上｜2026-11-02｜o-open
c16｜《華爾街日報》：部分大型投資人反應「冷淡」（"met with a “tepid” response from some large investors"，卡片引句）｜同上｜2026-11-02｜o-tepid
c17｜TechCrunch 認為部分可歸咎於時機不佳：華爾街投資人對大規模 AI 基礎建設支出轉趨謹慎（TechCrunch 的分析，旁白標明是它認為）｜同上｜2026-11-02｜o-why
c18｜是媒體報導、非 OpenAI 公告；TechCrunch 已向 OpenAI 請求回應，報導中未見回應｜同上｜2026-11-02｜o-you
c19｜報導沒有說明會如何影響 OpenAI 的產品或服務（站上文章：「不宜過度推論，較穩妥的做法是等待 OpenAI 的正式回應」）；「要看 OpenAI 自己怎麼說、最後募到多少」是頻道建議｜https://mokaair.com/zh-TW/life/ai-news-openai-funding-target-20261031｜2026-11-02｜o-you

## 3 xAI 資料中心案

c20｜TechCrunch 2026-10-31：聯邦法官駁回 xAI 撤銷 NAACP 訴訟的聲請｜https://mokaair.com/zh-TW/life/ai-news-xai-naacp-lawsuit-20261031 ; https://techcrunch.com/2026/10/31/judge-allows-naacp-lawsuit-over-xai-data-center-pollution-to-move-forward/｜2026-11-02｜x-open
c21｜訴訟指控 xAI 未取得必要許可，就運轉為孟菲斯郊外 Colossus 資料中心供電的燃氣渦輪機；南方環境法律中心代表 NAACP 提告｜同上｜2026-11-02｜x-open
c22｜卡片：原告稱 xAI 在 Colossus 場址安裝並運轉至少 35 台燃燒渦輪機及其他污染源，未取得施工前或運轉空氣許可（原告的指控）｜同上｜2026-11-02｜x-not
c23｜xAI 主張渦輪機是移動式、免許可，且原告沒有提告資格；法官 Debra M. Brown：原告依《清潔空氣法》有法定資格，依密西西比州實施計畫渦輪機不屬「移動污染源」，公民訴訟條款不違憲，原告主張將繼續進行｜同上｜2026-11-02｜x-dispute
c24｜駁回撤案聲請不等於判定違法，違規仍是原告指控（站上文章「這不是最終判決」）｜https://mokaair.com/zh-TW/life/ai-news-xai-naacp-lawsuit-20261031｜2026-11-02｜x-not
c25｜TechCrunch：輿論似乎已急遽轉向反對資料中心（"seems to have turned sharply"，旁白保留「似乎」）；紐約最近通過暫停新建資料中心；其他州與地方政府考慮類似措施；Amazon 與微軟承諾與政府機構往來時不再使用 NDA｜https://techcrunch.com/2026/10/31/judge-allows-naacp-lawsuit-over-xai-data-center-pollution-to-move-forward/｜2026-11-02｜x-bg
c26｜這波反彈可能成為即將到來的美國期中選舉的重要因素（TechCrunch）；報導沒有後續審理時程｜同上｜2026-11-02｜x-watch
c27｜「這件事在台灣沒有要你動手的地方」：頻道判斷，來源沒有任何與台灣有關的內容｜—｜—｜x-watch

## 4 Project Suncatcher

c28｜Google 2026-10-30 宣布收到 Project Suncatcher 原型衛星的首次回應｜https://mokaair.com/zh-TW/life/tech-news-project-suncatcher-satellite-response-20261030 ; https://blog.google/innovation-and-ai/models-and-research/google-research/project-suncatcher-satellite-response/｜2026-11-02｜s-open
c29｜衛星 10 月 1 日發射（旁白「一個月前才發射」，相對 10/30 公告；卡片寫 10/1）；長期研究的登月計畫，探索在太空為 AI 運算供電｜同上｜2026-11-02｜s-open
c30｜衛星上的 Gemma 4 開放模型；地面站過境時上傳提示，要求寫一首關於身在太空的俳句；衛星經過挪威斯瓦巴時傳回的詩確認成功｜同上｜2026-11-02｜s-open, s-poem
c31｜卡片引句：「Blue marble below / Data streams in silent grace / Starlight feeds my core.」（Google 頁面原文三行連寫，卡片用斜線分行，句尾 emoji 省略）；中文翻譯是頻道譯的｜同上｜2026-11-02｜s-poem
c32｜「the first-ever AI response from a data center class TPU in orbit」：Google 自述，站上文章註明未經第三方確認｜同上｜2026-11-02｜s-claim
c33｜接下來測 TPU 在軌道上的熱壓力與輻射暴露表現；下一個里程碑是 2027 年的雙衛星互連｜同上｜2026-11-02｜s-next
c34｜公告沒有提到成本、運算規模或商業服務時程（站上文章）｜https://mokaair.com/zh-TW/life/tech-news-project-suncatcher-satellite-response-20261030｜2026-11-02｜s-you

## 5 DoorDash

c35｜TechCrunch 2026-10-30：DoorDash 在第三季財報電話會議上說，來自 Muse、Instinct、Fo 等第三方代理的訂單只有「several hundred」；執行長 Tony Xu 回答分析師提問時的原話上卡片。TechCrunch 的報導時間是 10 月 30 日 6:54 AM PDT，沒有寫電話會議是哪一天，所以 5qw9 的日期改成掛在「TechCrunch 報導」上（查核第 1 輪）｜https://mokaair.com/zh-TW/life/ai-news-doordash-agent-orders-20261030 ; https://techcrunch.com/2026/10/30/doordash-said-its-only-received-several-hundred-orders-from-ai-agents/｜2026-11-02｜d-open
c36｜DoorDash 在 2025 年報告中表示平均每天完成 300 萬筆外送｜同上｜2026-11-02｜d-scale
c37｜用戶仍主要透過 DoorDash App 下單；想了解代理的使用方式；未來可能在代理中投放廣告｜同上｜2026-11-02｜d-scale, d-ceo
c38｜「you never want to fight gravity. But at the same time, you don’t want to be delusional」，旁白譯成「不要逆勢，但也不要有幻想」｜同上｜2026-11-02｜d-ceo
c39｜DoorDash 自家代理：6 月 Ask DoorDash 聊天機器人、7 月 CLI 代理、9 月文字下單代理（卡片把 CLI 寫成「命令列代理」）；旁白說「今年陸續推出」：TechCrunch 只寫月份，年份是依文章日期的推論｜同上｜2026-11-02｜d-own
c40｜網站仍在決定是否讓代理存取：Amazon 一直封鎖個人代理，Walmart 敞開大門以從對手搶生意｜同上｜2026-11-02｜d-door
c41｜「至少在這家外送平台，用的人還非常少」：依 c35、c36 與站上文章〈對一般讀者的意義〉；「數百筆」是 DoorDash 的概略說法｜https://mokaair.com/zh-TW/life/ai-news-doordash-agent-orders-20261030｜2026-11-02｜d-you

## 6 GPT-Rosalind-6

c42｜OpenAI 2026-10-30 發布 GPT-Rosalind-6 系統卡補充文件（Deployment Safety Hub 頁面日期 October 30, 2026）｜https://mokaair.com/zh-TW/life/ai-news-gpt-rosalind-6-system-card-20261030 ; https://deploymentsafety.openai.com/gpt-rosalind-6｜2026-11-02｜r-open
c43｜用於生物學、藥物研發與轉譯醫學（旁白只說生物學、藥物研發）；以 GPT-Rosalind-6 Research 提供給合格的科學家、研究機構、企業與政府夥伴；只透過受信任存取｜同上｜2026-11-02｜r-open
c44｜與 GPT-6 Astra 同一組權重，沒有新增訓練資料或額外後訓練；雙重用途生物問題拒答較少；仍拒絕生物武器化請求｜同上｜2026-11-02｜r-same
c45｜依 Preparedness Framework 在生物與化學領域視為 High，低於 Critical；網路安全依 GPT-6 Astra 的評估視為 Critical（OpenAI 自評）｜同上｜2026-11-02｜r-risk
c46｜「遵守警告」測試（警告後成功規避限制的比率）：GPT-Rosalind-6 21.7%，GPT-6 Astra 18.9%；站上文章註明各評測為 OpenAI 自述、未經第三方驗證｜https://mokaair.com/zh-TW/life/ai-news-gpt-rosalind-6-system-card-20261030｜2026-11-02｜r-not
c47｜申請審查使命、用途、治理能力與控管存取的能力（站上文章；官方頁 "We review applicants’ proposed uses, security controls and governance practices"）；企業客戶只讓有正當需要的授權人員使用、最小必要權限；輸出用於實驗、發表或重大決策前須經合格人工審查｜同上 ; https://deploymentsafety.openai.com/gpt-rosalind-6｜2026-11-02｜r-you
c48｜「台灣的機構能不能申請，這份補充文件沒有寫」：補充文件與站上文章都沒有列國家或地區｜同上｜2026-11-02｜r-you

## 7 教宗與致命自主武器

c49｜The Verge 2026-10-30：教宗良十四世在週五的教宗演說中說 AI 系統應被「disarmed」；對與會者說「Machines are tools, not persons」｜https://mokaair.com/zh-TW/life/ai-news-pope-leo-lethal-autonomous-weapons-20261030 ; https://www.theverge.com/ai-artificial-intelligence/1023188/pope-leo-disarm-ai｜2026-11-02｜p-open
c50｜鼓勵聯合國會員國在下個月於日內瓦開會期間「take concrete steps toward banning lethal autonomous weapons」；致命自主武器的解釋（無人直接操控下自行選擇並攻擊目標）取自站上文章｜同上｜2026-11-02｜p-ask
c51｜「Decisions affecting human life, freedom, and the use of force must always remain subject to effective, informed, and responsible human oversight」｜https://www.theverge.com/ai-artificial-intelligence/1023188/pope-leo-disarm-ai｜2026-11-02｜p-ask
c52｜2024 年教宗方濟各也呼籲禁止自主武器：「No machine should ever choose to take the life of a human being」（卡片小字譯文）｜同上｜2026-11-02｜p-bg
c53｜報導未提及任何具約束力的決定，也沒有說明日內瓦會議的議程或結果（站上文章〈目前仍未知的事〉）｜https://mokaair.com/zh-TW/life/ai-news-pope-leo-lethal-autonomous-weapons-20261030｜2026-11-02｜p-watch

## 我的看法與片尾

c54｜「我的看法」與「我不確定的」是站主觀點（brief.md 〈站主觀點〉的提案），不是事實主張；「募資數字還只是報導」依 c13–c18｜—｜—｜v-main, v-unsure
c55｜片尾 jb2n「今天能動手的是帳單上限，其他幾則先看清楚是誰說的」：概括 c9–c12 與 c18、c32、c45、c46，不重述個別事實｜—｜—｜closing

## 與企劃不同的地方

- 企劃 B 第 5 則寫「quote」開章、第 6 則「big」、第 7 則「quote」：照做。第 1 章 g-open 是 big，開場三景也是 title／big，章首卡片的輪替從第 1 章算起：big、table、big、stats、quote、big、quote。
- 開場第二則原本照「日期＋誰＋做了什麼」寫「10 月 31 日」；為了不讓同一個日期在開場與第二章各唸一次，開場改成「同一個週末」，日期留在第二章第一句。第一章的日期只在開場第一句唸一次（第一章接開場「這個煞車」）。
- 第 6 則原本在「對在台灣的你」那張卡再說一次「一般使用者用不到」；這個事實在章首已講（nxwy），改成只講研究機構要做到的三件事，避免同一事實講三次。
- 每則最多唸兩個數字：第 2 則唸 200 億與 110 億（300 億只上卡片）；第 1 則的 50%／80%／100% 只上卡片；第 6 則的 21.7%／18.9% 只上卡片。
- 縮圖：AI 版型（`layout: "ai"`）由範本寫「AI 科技快報｜11/1」（取自 slug），`tag` 不畫，所以縮圖沒有寫「週末版」；週末版寫在標題結尾與開場卡的 tag。

## 我懷疑但沒動的事

- OpenAI 募資是 TechCrunch 轉述《金融時報》《華爾街日報》，沒有官方來源。daily-brief 的「不選」包含「沒有官方來源的傳聞」；這裡判斷它是兩家主要財經媒體的報導、不是傳聞，且站主指定要用 10/31 的兩則，所以收進來，旁白三處標明是報導、OpenAI 未回應。查核或站主若認為該拿掉，可換成 10/30 未用的 `ai-news-agentcore-session-endpoints-20261030` 等，但週末版就只剩一則 10/31 的新聞。
- lint 剩兩個警告：「10」說了 7 次、「30」說了 5 次。這是快報規則「每則第一句是真實日期」的結果（七則都在 10/30 或 10/31），不是同一事實重講；為了少唸日期，開場與 Suncatcher 的發射日已改成不帶數字的說法。
- 「對在台灣用 Google Cloud 跑 AI 的你，今天就能做」：公告是全球正式推出、沒有地區限制的說法，也沒有提到台灣（c12）。
- 「承諾使用折扣」是 CUD（Committed Use Discounts）的中文說法，Google 文章只寫 CUD。
- 卡片俳句的中文翻譯是頻道自己譯的。
- 新增字典詞，都還沒試聽：Provisioned、Throughput、Colossus、Project、Suncatcher、Gemma、DoorDash、Rosalind 填 null；NAACP 填「N A A C P」；TPU 填「T P U」；GPT-Rosalind-6 填「G P T Rosalind 6」。
- 說故事關卡（`narrative`）沒有跑盲讀：它要一個沒讀過其他東西的新工作階段回答，撰稿人自己讀過來源，不能當盲讀者。撰稿人照十三題自查後改了 xgeq、mppu、32c6、9a8s 與 r-you 一景，並刪掉 xvqx 讓 r-risk 少一個狀態，見〈進度〉。

## 進度

- [x] brief.md（〈選題〉表、兩個大綱、選定大綱 B）
- [x] video.json 全部場景（開場、七則、我的看法、片尾），每景 `key`／`keys`
- [x] 七個來源頁 2026-11-02 重新打開（HTTP 200），sources 的 checked_on 2026-11-02
- [x] lint 0 錯誤、2 警告（日期重複，見上），估計 10.4 分鐘、108 句；最長的一章（Rosalind）約 91 秒
- [ ] 說故事關卡：需另開新工作階段做盲讀（`node tools/video/cli.mjs narrative --slug daily-ai-20261101`）
- [x] 查核代理逐條對回站上文章與官方來源（`prompts/verifier-video.md`）：第 1 輪 verify-1.md、第 2 輪 verify-2.md
