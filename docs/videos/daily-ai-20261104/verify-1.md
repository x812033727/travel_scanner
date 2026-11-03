# daily-ai-20261104 查核第 1 輪

查核日 2026-11-03。查核代理不是撰稿人。每一條旁白（`text`，Sola 與 Kai 兩位都查；本片沒有 `say`）、每張卡片的 `data`（含 `source`、`note`、`keys`）、縮圖、`youtube.title`、`description`、`tags` 都抽出來逐條對照：
站上 16 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，1.2 秒一篇，全部 HTTP 200、`status: published`、news_date 2026-11-03）與 `video.json` `sources` 的 17 個原始來源，2026-11-03 全部用 `Mokaair-editorial/1.0` UA 以 curl 重新打開。
**The Verge 四篇這次都打得開（HTTP 200）**，所以 V1–V4 的事實與英文引句是對原文逐句核對的，不是只對站上文章的轉述。

## 來源代號

站上文章（全部 200，published，news_date 2026-11-03）：

| 代號 | slug |
| --- | --- |
| ANT | ai-news-anthropic-compute-costs-20261103 |
| SRCH | ai-news-chatgpt-search-share-20261103 |
| SCAM | tech-news-google-apac-scams-20261103 |
| APPL | ai-news-apple-18-plus-ai-companions-20261103 |
| FP | ai-news-anthropic-flashprove-20261103 |
| WM | ai-news-claude-text-watermark-20261103 |
| GIT | crypto-news-gitbook-ai-agent-breach-20261103 |
| NFX | ai-news-netflix-ai-discover-20261103 |
| AMD | tech-news-amd-q3-2026-results-20261103 |
| FAL | ai-news-fal-valuation-20261103 |
| JET | ai-news-data-center-jet-engine-power-20261103 |
| CAMP | ai-news-openai-compute-campuses-20261103 |
| BNB | crypto-news-binance-hack-north-korea-denial-20261103 |
| OKX | crypto-news-okx-ice-tokenized-stock-objections-20261103 |
| FSC | crypto-news-taiwan-stablecoin-rules-20261103 |
| STM | tech-news-steam-review-delays-20261103 |

原始來源（2026-11-03 重開，全部 HTTP 200，沒有轉址）：

| 代號 | URL（頁面上的日期） |
| --- | --- |
| TC1 | https://techcrunch.com/2026/11/03/anthropic-is-still-grappling-with-the-economics-of-compute/ （Russell Brandom，9:07 AM PST, November 3, 2026） |
| AMDPR | https://ir.amd.com/news-events/press-releases/detail/1303/amd-reports-third-quarter-2026-financial-results （November 03, 2026 4:15 pm EST） |
| TC2 | https://techcrunch.com/2026/11/03/ai-inference-startup-fal-doubles-its-valuation-to-16b-as-demand-surges/ （11:34 AM PST, November 3, 2026） |
| TC3 | https://techcrunch.com/2026/11/03/data-centers-are-turning-to-old-jet-engines-as-the-wait-for-power-grows/ （2:19 PM PST, November 3, 2026） |
| V1 | https://www.theverge.com/ai-artificial-intelligence/1025242/openai-quietly-renames-data-centers-as-compute-campuses （2026-11-03T15:00Z） |
| V2 | https://www.theverge.com/ai-artificial-intelligence/1025482/openai-says-chatgpt-is-catching-up-to-google-in-search （2026-11-03T18:30Z） |
| GB | https://blog.google/company-news/inside-google/around-the-globe/google-asia/fight-against-apac-scams/ （2026-11-03） |
| TC4 | https://techcrunch.com/2026/11/03/apple-restricts-dating-apps-and-ai-companions-to-users-18-and-up/ （2026-11-03T15:38Z） |
| AR | https://www.anthropic.com/research/provable-inference （datePublished 2026-11-02；TC5 稱 blog post published Tuesday） |
| TC5 | https://techcrunch.com/2026/11/03/anthropic-is-working-on-a-system-to-prove-ai-models-identity/ （2026-11-03T22:41Z） |
| RN | https://platform.claude.com/docs/en/release-notes/overview （November 3, 2026 條目） |
| DC1 | https://decrypt.co/382465/crypto-docs-gitbook-ai-agent-security-breach （2026-11-03T19:46） |
| V3 | https://www.theverge.com/streaming/1025029/netflix-ai-discover-recommendations （2026-11-03T18:00Z） |
| DC2 | https://decrypt.co/382394/north-korea-denies-6-3b-binance-hack-calls-fbi-finding-a-political-provocation （2026-11-03T10:18） |
| DC3 | https://decrypt.co/382458/elon-musk-tesla-spacex-block-okx-ice-tokenized-stock （2026-11-03T17:46） |
| FSCPR | https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0,2&mcustomize=news_view.jsp&dataserno=202611030002&dtable=News （更新日期 2026-11-03） |
| V4 | https://www.theverge.com/games/1025596/valve-steam-indie-games-missing-launch-dates （2026-11-03T18:14Z；**「Update, November 3rd: Added new post from Valve」**，updatedAt 21:56Z） |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 今天是 11 月 4 日星期三 | 5yxg；intro | 曆法 | — | CONFIRMED（2026-11-03 是星期二） | |
| 2 | 主題：Anthropic 上市前更新的文件、算力帳單；營收一直漲、虧損卻變大 | ao43、qmon；intro-kai、intro-q | TC1 | 200 | CONFIRMED（「revenue reached $17 billion, up from $11.5 billion」「the operating loss grew at the same time」） | |
| 3 | 先看昨天 11 月 3 日的科技新聞 | g9s8；hl-open | 站上 16 篇 | 200 | CONFIRMED（news_date 皆 2026-11-03） | |
| 4 | OpenAI 這週一（記者會）說 ChatGPT 搜尋量已是 Google 的五分之一 | iz00；hl-search | V2、SRCH | 200 | CHANGED（數字對：「now equals 20 percent of the volume run through Google」，Fry 週一 press event。但只有 The Verge 一家報導，旁白沒有「據」，其他單一報導的各則都有） | 「好。這週一，OpenAI 在記者會上說，…」→「好。據 The Verge，OpenAI 這週一說，ChatGPT 的搜尋量，已經是 Google 的五分之一。」 |
| 5 | 觸發網路搜尋才算；解釋名詞、簡單操作說明不算；OpenAI 沒說 Google 數字從哪來 | rzxg、cqwh、g62g；hl-search-def | V2 | 200 | CONFIRMED（「as opposed to tasks like defining a term or a simple how-to explanation. (Fry did not specify the source of the Google search volume number.)」） | |
| 6 | 微軟執行長 2023 年在法庭上說，Bing 試了十多年，市占約 3% | srca；hl-search-bing | V2 | 200 | CONFIRMED（Nadella, Google's 2023 antitrust trial, 「about 3 percent … after trying for more than a decade」） | |
| 7 | OpenAI 上個月說 ChatGPT 廣告要放贊助產品圖片 | we58；hl-search-ads | V2 | 200 | CONFIRMED（「OpenAI announced last month … images of sponsored products and services」） | |
| 8 | 看清楚哪段是回答、哪段是廣告 | ahuo；hl-search-tw | SRCH | 200 | CHANGED（標示：這是節目建議，原稿沒有標，卡片 kicker「For you」） | ahuo「對台灣的你來說：…」→「我們的建議：…」；kicker「For you」→「Our advice」 |
| 9 | Google 11/3 公布亞太反詐騙；Android 偽冒來電偵測，認出 AI 假冒來電 | 2tqk、a9go；hl-scam、hl-scam-what | GB | 200 | CONFIRMED（「This year, Android launched Fake Call Detection, a feature designed to spot AI-driven phone call impersonation」） | |
| 10 | Pixel 內建詐騙偵測對常見通訊 App 的可疑內容警示；今年稍後跟夥伴帶給更多 Android | j1c6、b0xe；hl-scam-more | GB | 200 | CONFIRMED（「We are partnering to bring this to additional Android users later this year」） | |
| 11 | Google 慈善部門拿出 600 萬美元做亞太防詐教育 | 3myb；hl-scam-what | GB | 200 | CONFIRMED（Google.org $6 million to The Asia Foundation and Tech for Good Institute；內容含培訓、原型與政策，「防詐教育」是概括） | |
| 12 | 哪些機型、地區沒有列出 | wul6、pvi0；hl-scam-tw、tt-settings | GB | 200 | CONFIRMED（全文只說 APAC，沒有國家、機型清單） | |
| 13 | 據 TechCrunch，蘋果週一通知開發者：約會或浪漫關係功能 App 一律 18+ | z2ua；hl-apple | TC4 | 200 | CONFIRMED（「announcement to developers on Monday」「all apps offering dating or romantic relationship features to carry an 18+ rating」） | |
| 14 | TechCrunch：真正受影響的是 AI 伴侶 App；常鎖定年輕族群 | 90kq、ycjs；hl-apple-why | TC4 | 200 | CHANGED（TC4 是「It's perhaps more interesting how this rule could impact AI companion apps」，不是說「真正受影響的」） | 90kq「…真正受影響的，是 AI 伴侶 App。」→「…更值得注意的，是 AI 伴侶 App。」 |
| 15 | 11 月 16 日起補新內容描述；AI 伴侶 App 到去年夏天全球下載 2.2 億次 | 0klx、4foc；hl-apple-date | TC4 | 200 | CONFIRMED（「Starting November 16」；「As of last summer … 220 million times globally」） | |
| 16 | 報導沒說蘋果怎麼執行；家長控制自己設 | zt5n；hl-apple-tw | TC4 | 200 | CHANGED（事實對；後半是節目建議，原稿沒有標） | 「…報導沒說蘋果怎麼執行，家長控制，還是要自己設。」→「…報導沒說蘋果怎麼執行；我們建議，家長控制還是自己設。」 |
| 17 | Anthropic 說，中間服務可能為省錢偷換模型，或有人竄改輸出 | nnfb；hl-prove-why | AR | 200 | CONFIRMED（「secretly substituted in by a routing service for cost reasons, or even by an attacker who has tampered with the token stream」） | |
| 18 | 開源原型 FlashProve，密碼學證明回答來自那個模型，不公開權重 | 9aan；hl-prove-why | AR、TC5 | 200 | CONFIRMED（「an open-source performant prototype」「the proof reveals nothing about the model's weights」） | |
| 19 | 一張 GPU 每秒約證明 110 token；1,024 token 請求的證明約 19 MB；目前沒有任何實驗室要部署 | lux8、t9dy、prva；hl-prove-cost | AR、TC5 | 200 | CONFIRMED（AR：Llama 4 Maverick、single H100、110 tokens per second、18.78 MB；TC5：「no plans to deploy it at Anthropic or any other lab」） | |
| 20 | Anthropic 昨天說 Claude 三個模型的文字帶浮水印；只限列出的平台；Sonnet 4.6 改生成設定時可能不帶 | mktx、m7jx、zmrr；hl-mark、hl-mark-limit | RN | 200 | CONFIRMED（November 3, 2026：Mythos 5、Opus 4.7、Sonnet 4.6；temperature、top_p、top_k 非預設值「might not carry it」） | |
| 21 | 很多加密專案放文件的 GitBook 說，週一晚上有人用 AI 代理攻擊，拿到部分系統的憑證 | 52k2、e7fb；hl-gitbook | DC1 | 200 | CONFIRMED（「7 p.m. Central European Time on November 2」＝週一；「some of its infrastructure credentials」） | |
| 22 | AI 代理會一步步操作軟體、人盯得較少 | 1klv；hl-gitbook-ai | DC1 | 200 | CONFIRMED（「carry out sequences of actions, interact with software, and perform tasks with limited human supervision」） | |
| 23 | 可能外洩：API 權杖、串接密鑰、問 AI 助理的問題；已讓客戶 API 權杖失效、要客戶換；沒有證據內容被改 | d67c、etvc、5g0v、pngi、14fs；hl-gitbook-what、hl-gitbook-do | DC1 | 200 | CONFIRMED | |
| 24 | 怎麼做到、哪些 AI 系統、憑證怎麼被拿走都沒說明 | 54rb；hl-gitbook-unknown | DC1 | 200 | CONFIRMED | |
| 25 | Netflix 電視版 AI Discover 分頁，主題推薦（輕鬆、家庭電影夜、很快看完）；可說不喜歡、App 會記住；美國、英文、支援的電視逐步開放；擴大時間沒說 | ypdj、h2mc、jv1a、jfmp、ix3p；hl-netflix* | V3 | 200 | CONFIRMED | |
| 26 | 訊號數字 58%：每 100 美元營收有 58 美元付算力 | os5p、4fv9；hl-number、hl-number-what；縮圖 | TC1 | 200 | CONFIRMED（「compute took up 58% of the company's revenue」；換算） | |
| 27 | 這週一 Anthropic 遞新文件更新 S-1；前一週才交；舊版到 6 月底，新版到 9 月 30 日 | n1w1、026w；sd-scene、sd-why-now | TC1 | 200 | CONFIRMED（「In a new filing on Monday … an update to the S-1 released last week … through June 30 … to September 30」） | |
| 28 | TechCrunch：越接近上市，終於多透露營收有多少被算力吃掉 | xpmb；sd-econ | TC1 | 200 | CONFIRMED | |
| 29 | 營收前一季 115 億、這一季 170 億美元；「快五成」 | aqr1、t181、gnzv；sd-revenue | TC1 | 200 | CONFIRMED（季度數字；17÷11.5＝1.478，+47.8%） | |
| 30 | 營運虧損同時擴大；TechCrunch 沒寫金額，主因之一是算力成本上升 | 6y9t、c6qv；sd-loss、sd-loss-why | TC1 | 200 | CONFIRMED（「thanks in large part to growing compute costs」；沒有虧損金額） | |
| 31 | 前一季 48%、這一季 58%；跳了十個百分點 | 7nny、y11g；sd-share | TC1 | 200 | CONFIRMED | |
| 32 | 這一季算力帳單 100 億美元，其中一半是短期合約，比多年合約貴得多 | tt6k、bmua、eu8k；sd-bill、sd-short | TC1 | 200 | CONFIRMED（「$10 billion for the quarter」「$5.0 billion of compute under short-term commitments, which currently costs significantly more than comparable compute procured under our multi-year commitments」） | |
| 33 | TechCrunch 解讀：需求太快、趕著找算力、付較高價 | bs8p；sd-rush | TC1 | 200 | CONFIRMED | |
| 34 | 每一美元算力帶回的營收：2025 年初起上升，高峰略高於兩倍，現在 1.72 倍 | pcca、mex6；sd-ratio | TC1 | 200 | CONFIRMED（旁白沒說高峰在哪一季，見「懷疑但沒改」） | |
| 35 | 每月付 SpaceX 12.5 億美元；與 Nscale、Akamai、Volta 簽數十億美元合約；neocloud，較彈性、費率較高 | kv8c、bthn、a2ft、xa1v；sd-spacex、sd-neo | TC1 | 200 | CONFIRMED | |
| 36 | Anthropic Direct 建自己的算力；TechCrunch 認為跟不上需求 | qojx、d0x8；sd-direct | TC1 | 200 | CONFIRMED | |
| 37 | AMD 昨天公布第三季；資料中心營收 85 億美元、比去年多將近一倍（+97%）；遊戲少四成 | bpnk、bh69、ybob、y4j8；sd-chips、sd-amd | AMDPR | 200 | CONFIRMED（「Data Center segment revenue was a record $8.5 billion, up 97% year-over-year」；「Gaming business revenue was $773 million, down 40%」） | |
| 38 | AMD 說 Anthropic、Meta、微軟、OpenAI、甲骨文雲端在第一批 Helios 機櫃上跑工作；金額沒公布、公司自述 | lvm1、71n3；sd-helios、sd-helios-n | AMDPR | 200 | CONFIRMED（「are running models and workloads on the first AMD Helios rackscale solutions」；沒有金額） | |
| 39 | Fal 做影像、聲音模型託管，募 13 億美元；據 Bloomberg，估值是四月的兩倍 | irzo；sd-fal | TC2 | 200 | CONFIRMED（$1.3B；$16B，「double its $8 billion valuation in April, Bloomberg reported」） | |
| 40 | TechCrunch 引知情人士：買或租算力太貴，這類公司毛利還是很薄 | 993g；sd-fal-margin | TC2 | 200 | CONFIRMED（「gross margins remain thin because of the high cost of buying or leasing compute, according to several people familiar」；說的是 Baseten、Fireworks AI、Modal 等推論公司，旁白用「這類公司」成立） | |
| 41 | TechCrunch 轉述紐約時報：資料中心等不到電網，改用退役飛機噴射引擎發電 | 7yb2；sd-power | TC3 | 200 | CONFIRMED（「pulled from retired aircraft and rebuilt to burn natural gas」「the New York Times reported Tuesday」） | |
| 42 | 北維吉尼亞 100 兆瓦接電網約七年（IEA）；分析師說 24 個月能運轉；效率低、污染多 | zujv、egf8；sd-jet | TC3 | 200 | CONFIRMED | |
| 43 | 上個月微軟退出 Nscale 英國資料中心主要客戶位置；當地電力公司說 2030 年代初到中期才有足夠電 | 41ju、vhse；sd-nscale* | TC3 | 200 | CONFIRMED（Loughton, England；「early to mid-2030s」） | |
| 44 | 錢的流向、「Anthropic 自己最吃虧」 | x6k8、0xed、5d9c、mnya；sd-flow、sd-squeezed | TC1、AMDPR、TC3 | 200 | CONFIRMED（節目依各來源的歸納；見「懷疑但沒改」） | |
| 45 | 文章沒說會不會漲價；每問一句是帳單一小格 | c83x、jie6；sd-you | ANT | 200 | CONFIRMED（比喻） | |
| 46 | 今天這幾篇都沒提到台灣廠商；AMD 風險說明列出口管制、關稅、記憶體供應、依賴第三方製造；沒點名 | twna、2oz0、e0hq、vqdu、d3b7；sd-taiwan、sd-risk、sd-asia | AMDPR、TC1–TC3、ANT、AMD、FAL、JET | 200 | CONFIRMED（四則原文與站上文章都沒有 Taiwan／TSMC／台灣；AMDPR forward-looking statements 有「export regulations」「import tariffs」「memory supply」「third party manufacturers」，沒有點名） | |
| 47 | 支出金額還會增加、仍是最大營運支出；TechCrunch 認為比較像短暫波動；債市緊張或地方反對可能讓建設放慢 | z6e4、f2xh、8qns；sd-next | TC1 | 200 | CONFIRMED（filing 引句；「more of a blip than a long-term problem」；「if bond markets get skittish or local opposition gets more intense」） | |
| 48 | 營收每季成長將近五成，投資人不太擔心 | 9reg；sd-calm | TC1 | 200 | CONFIRMED | |
| 49 | 報導沒給上市日期，只說越來越近 | zcc6；sd-ipo | TC1 | 200 | CONFIRMED（「as Anthropic inches towards it IPO」） | |
| 50 | 四句都是原始報導裡的原話 | u63w；wp-open | TC1、TC3、V1、V2 | 200 | CONFIRMED | |
| 51 | Brandom：正好可以用毛利改善說服上市投資人時，毛利卻變差 | u7lu、368b；wp-tc | TC1 | 200 | CONFIRMED（引句逐字；Brandom 是本文作者，TechCrunch AI Editor） | |
| 52 | Rystad Energy 分析師對紐約時報：盡可能快拿到電 | gcwr；wp-rystad | TC3 | 200 | CONFIRMED（Audun Martinsen；引句逐字） | |
| 53 | The Verge：OpenAI 在新公告裡把資料中心改叫運算園區；OpenAI 沒回應置評 | dnrp、xft7；wp-rename | V1 | 200 | CONFIRMED（Grid Protectors Program 公告；「OpenAI did not respond to The Verge's request for comment」） | |
| 54 | NAACP 的 Abre' Conner：改名解決不了問題 | darw；wp-conner | V1 | 200 | CONFIRMED（「Changing the name does not fix the problem」，director of the NAACP's Center for Environmental and Climate Justice） | |
| 55 | ChatGPT 消費者產品負責人 Adam Fry：大多數人似乎不介意廣告 | 9fxy；wp-fry | V2 | 200 | CONFIRMED（「most people do not seem to mind ads in the product」逐字） | |
| 56 | 據 Decrypt 引述韓聯社，北韓否認；金與正：嚴重的政治挑釁 | ihg8、wllv；ms-open、ms-kim | DC2 | 200 | CONFIRMED（「grave political provocation," Yonhap reported on Tuesday」；她也暗示美方，卡片「blames the US」成立） | |
| 57 | FBI 上週六說 TraderTraitor 偷走幣安超過 60 億美元；約 28.5 億已凍結或查扣 | hxx2、oclb；ms-fbi | DC2 | 200 | CONFIRMED（「The FBI said on Saturday … more than $6 billion」；「About $2.85 billion of the $6.43 billion stolen has been frozen or seized」；DC2 11/3 週二，週六＝10/31） | |
| 58 | 幣安說已補足約九成五；前十大代幣持有人可用 10/31 備付快照的零知識證明查餘額 | 7wne、7nw3、x68d；ms-users、ms-proof | DC2 | 200 | CONFIRMED | |
| 59 | 零知識證明：證明一件事是真的但不公開細節；跟 FlashProve 同一類 | xzi2；ms-zk | AR、BNB | 200 | CONFIRMED（AR：zkSNARK，zero-knowledge） | |
| 60 | 交易所出事時看有沒有能自己檢查的證明 | plgd；ms-lesson | BNB | 200 | CHANGED（標示：節目建議，原稿沒有標；kicker「For your money」） | 「交易所出事的時候，值得看的，是…」→「我們的建議：交易所出事的時候，看它…」；kicker →「Our advice」 |
| 61 | OKX 與紐約證交所母公司 ICE 合資的代幣化股票平台，反對名單增加到 56 家；新加入 Tesla、SpaceX、Amazon、Netflix 等六家 | 4eoy、r5as；ms-okx、ms-who | DC3 | 200 | CONFIRMED（Nov. 2 notice；Amazon、Tesla、SpaceX、Netflix、Lam Research、SoFi；「50-50 joint venture between NYSE owner Intercontinental Exchange and OKX's U.S. holding company」） | |
| 62 | 代幣化股票：股票做成區塊鏈代幣、在區塊鏈平台交易 | jntm；ms-token | OKX、DC3 | 200 | CONFIRMED | |
| 63 | SEC 九月創新豁免：先通知公司；30 天內書面反對，平台就不能上架；只限這個平台 | 9uwp、fehm、rtwy；ms-rule | DC3 | 200 | CHANGED（擋的只是「unaffiliated third party」代幣化的版本，發行公司自己代幣化的仍可上；原句說成整支股票不能上架） | fehm「…平台就不能上架。」→「…平台就不能上架別人代做的代幣版。」 |
| 64 | 平台還在計畫階段 | z8ye；ms-okx-you | DC3 | 200 | CONFIRMED（「planned OKX-ICE tokenized stock venue」） | |
| 65 | 金管會近日內預告穩定幣發行許可辦法草案 | fp84；ms-tw | FSCPR | 200 | CONFIRMED（「將依行政程序法規定，於近日內預告」） | |
| 66 | 申請對象：銀行、金控、銀行轉投資的公司、金管會公告的其他機構；非銀行實收資本至少 3 億 | lgku、cg1t；ms-tw-who | FSCPR | 200 | CONFIRMED | |
| 67 | 跟新台幣或單一外國貨幣一比一；準備資產不少於流通總額；確認認購和贖回人；定期會計師查核 | edyq、lk0k、bgww；ms-tw-what | FSCPR | 200 | CONFIRMED（「按公允價值衡量之總價值不低於該穩定幣流通在外之總餘額」） | |
| 68 | 公告隔天起 40 天內提意見；生效配合虛擬資產服務法施行日期，行政院還沒定 | 28m1；ms-tw-when | FSCPR | 200 | CONFIRMED（「施行日期將由行政院另定」） | |
| 69 | 這段不談價格；全片沒有價格、報酬、漲跌或買賣 | 251t；ms-tw-you；全片 | — | — | CONFIRMED | |
| 70 | Try This：節目建議不是 Google 的指示；掛掉用自己存的號碼回撥；設定搜尋「詐騙」；家長控制 | 1a87、scma、gfdq、9hi7、khjh；tt-* | — | — | CONFIRMED（每張卡片 kicker 標 our advice；不跟來源衝突） | |
| 71 | Google 說 Be Scam Ready 模擬常見詐騙、台灣已經有了 | 9qnc；tt-game | GB | 200 | CONFIRMED（「already available in Singapore, Thailand, and Taiwan」） | |
| 72 | 據 The Verge，獨立開發者說 Steam 審核等太久、錯過發售日 | zokc；nd-open | V4 | 200 | CONFIRMED | |
| 73 | Valve 說明通常 3–5 個工作天；Food Devils 10/12 送審、原定昨天上市還在等；另一款延後快兩週；等三個禮拜 | d4n5、9sru、rzbd、5l7t；nd-wait | V4 | 200 | CONFIRMED（「typically takes 3-5 business days」；early access today＝11/3；Wheel Make It「by nearly two weeks」；10/12→11/3＝22 天） | |
| 74 | 開發者猜是 AI 粗製遊戲塞爆審核 | 05ct；nd-why | V4 | 200 | CONFIRMED（Kamon 與 2 Left Thumbs「suspect」） | |
| 75 | Next Fest 7,240 款、比六月多六成五；網友算出 49.9% 標了 AI | 5y7k、nxdo；nd-numbers | V4 | 200 | CONFIRMED（How to Market a Game；「A Reddit user also found」） | |
| 76 | Valve 沒有立即回覆 The Verge | 4nba；nd-valve | V4 | 200 | CHANGED（**過時**：V4 11/3 更新後寫 Valve 發文承認送審量大增、「running a little behind right now」、審核「up to 12 business days」、延誤多半是「having to re-review games」；V4 現在已沒有「didn't immediately respond」。The Verge 的轉述沒有把原因歸給 AI） | 4nba →「Valve 後來發文承認審核落後，最多要十二個工作天。怪 AI，仍是開發者的猜測。」；卡片 text「No comment / so far」→「Running behind / up to 12 business days」，key「Valve: no reply yet」→「Valve: up to 12 days now」 |
| 77 | 我的看法：今天最重要的是 Anthropic 的文件；帳單影響 AI 服務；我不確定是不是波動 | 7qsr、d9ls、so1l、kzi0、z02r；tk-* | brief.md | — | OUT OF SCOPE（觀點，見摘要） | |
| 78 | 完整整理在 Mokaair 文章，連結在說明欄 | k0ch；tk-site；說明欄 | 站上 16 篇 | 200 | CONFIRMED（說明欄 16 個網址都是 200、published） | |
| 79 | 片尾：錢大多付給了算力，而且是急著買的 | qans；outro | TC1 | 200 | CONFIRMED（58%、$5B/$10B 短期合約） | |
| 80 | 縮圖「Compute 58%」「Anthropic's revenue, per TechCrunch」；標題「Anthropic's compute bill, explained」 | thumbnail、youtube.title | TC1 | 200 | CONFIRMED | |
| 81 | 說明欄（AI 合成語音、Try This 為節目建議、不談價格與投資）；tags | youtube.description、tags | — | — | CONFIRMED／OUT OF SCOPE | |
| 82 | 串場與 Kai 的反應句（8vau、srcq、2p4c、f46p、kcmm、61em、mpeg、531m、39tw、6kp4、svzk、hhp6、2jfc、tfql、fe8z、4pwl、npwp 等） | 各處 | — | — | OUT OF SCOPE（不含新事實；沒有編主持人的私人經驗） | |

## 摘要

- 查了 82 條（同一事實在多處出現時合為一條）：CONFIRMED 73（#81 的 tags 部分是 OUT OF SCOPE）、CHANGED 7、NOT FOUND 0、OUT OF SCOPE 2。事實改動 4 處：(1) Valve 已回應，「沒有立即回覆」過時（4nba、nd-valve 卡片）；(2) ChatGPT 五分之一加「據 The Verge」（iz00）；(3) TechCrunch 對 AI 伴侶 App 的說法是「更值得注意」不是「真正受影響」（90kq）；(4) OKX-ICE 異議只擋第三方代做的代幣版（fehm）。標示改動 3 處（不是事實錯誤，是節目建議沒有標）：ahuo＋hl-search-tw kicker、zt5n、plgd＋ms-lesson kicker。
- 重點數字全部對到原文：Anthropic 季營收 170 億（前一季 115 億，確為季度、非年化）、運算占比 48%→58%、帳單 100 億其中 50 億短期、1.72 倍、SpaceX 每月 12.5 億；ChatGPT 搜尋量＝Google 的 20%（OpenAI 自述、Google 數字無來源）；AMD 資料中心 85 億、+97%、遊戲 −40%；Fal 募 13 億、估值 160 億是四月 80 億的兩倍（據 Bloomberg，旁白只說「兩倍」）；幣安 FBI 說「超過 60 億」（Decrypt 標題 63 億、內文 64.3 億，旁白用 FBI 的說法）、凍結或查扣約 28.5 億、補足約 95%；OKX-ICE 56 家（11/2 通知，新增 6 家）；金管會 3 億、一比一、40 日。
- 「據報導」：單一媒體的各則都有掛名（據 The Verge／TechCrunch／Decrypt／Bloomberg、TechCrunch 轉述紐約時報）；本輪補上 ChatGPT 搜尋那一句。公司自述都有標：OpenAI（2p4c「它自己說的」）、AMD（71n3）、Google（hl-scam-tw 卡片、9qnc）、Anthropic（nnfb、hl-prove-cost 標題 by Anthropic's numbers）、GitBook（14fs「它說」）、幣安（7wne「它說」）。
- 節目建議：Try This 四張卡片都標 our advice、1a87 開頭明說不是 Google 的指示；本輪把散在 Headlines 與 Money Signal 的三句建議也標上「我們的建議」。
- 加密貨幣：全片沒有價格、報酬、漲跌或買賣；ms-lesson 只談可檢查的證明，ms-tw-you 明說不談價格。
- 唸出來的日期：11/2 週一（S-1 更新、OpenAI 記者會、蘋果通知、GitBook 晚上 7 點 CET、OKX 通知）、10/31 週六（FBI、幣安快照）、11/3（Google、AMD、Claude 發行說明、金管會、Food Devils 原定上市）、11/16（蘋果）、10/12（Food Devils 送審）都與原文相符。
- `sources` 17 個網址 2026-11-03 全部 HTTP 200，`checked_on` 維持 2026-11-03。
- 會過期的事實：Anthropic S-1 可能再更新、上市日期未公布（TC1 2026-11-03）；Steam 審核時間（Valve 新貼文「up to 12 business days」，V4 2026-11-03 更新）；幣安補足比例約 95% 與凍結 28.5 億、幣安說週三（11/4）再做更大的快照（DC2 2026-11-03）；OKX-ICE 名單 56 家（11/2 通知，名單一週內從 38→50→56）；金管會草案預告日與 40 日意見期（FSCPR 2026-11-03，「近日內預告」）；Pixel 詐騙偵測擴大（「later this year」）；蘋果 11/16 起的內容描述；Netflix AI Discover 美國逐步推出。
- 觀點：7qsr、d9ls、so1l、kzi0、z02r 以「我的看法是」「我只覺得」「老實說，我不確定」標明，與 brief.md〈站主觀點〉一致（S-1 最重要、不說 Anthropic 會出問題、不猜漲價、TechCrunch 認為是波動但我不確定）。沒有不一致。
- 聽眾檢查（只報告）：超過 40 字的句子 29 句，最長 lvm1 61、iz00 56（本輪加「據 The Verge」後拿掉「在記者會上」以免更長）、srca 56、z2ua 53、mktx 53、9aan 50、xpmb 50；本輪改的 4nba 41。沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後。本輪新加進旁白的拉丁詞只有 The Verge（原稿已多處在唸），lint 沒有新增字典警告。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261104` → `daily-ai-20261104: 0 errors, 3 warnings`（開場濃縮兩條與 Headlines 開頭是標籤，撰稿時就有，本節目格式沒有開場濃縮；估計 21.4 分鐘，268 句）。新卡片 key「Valve: up to 12 days now」24 字元。
- 懷疑但沒改：
  - **站上文章 STM 需要修正**：仍寫「Valve 未立即回覆置評請求」，V4 已在 11/3 更新加上 Valve 的貼文（不在本輪可改的範圍）。brief.md 的 Noise 理由也還寫「Valve 沒立即回覆」。
  - sd-ratio「高峰略高於兩倍」：TC1 原文是「peaking at just over 2x this past quarter, then falling back down to 1.72x」，「this past quarter」可以讀成高峰就在最近這一季（又在同一季回落？），語意不清；旁白不說是哪一季，沒改。站上文章 ANT 寫「上一季峰值」，是否要修請站主看 S-1 原圖。
  - oclb「Decrypt 先前報導」：DC2 把 28.5 億放在「Decrypt reported on Monday」之後的下一句，看起來是本篇自己的數字；說「先前報導」不算錯但不確定，沒改。
  - sd-loss-why 卡片 kicker「The main reason」：TC1 是「thanks in large part to」，旁白說「主因之一」比較準；卡片偏強但不算錯，沒改。
  - mnya「急著買的那一方，也就是 Anthropic 自己，最吃虧」是節目的歸納（claims c45 有標），旁白沒有用「我覺得」，但跟 TC1「margins got worse because of deals like these」一致，沒改。
  - hl-apple 卡片「AI companion apps: rated 18+」：規則是對有約會或浪漫關係功能的 App；不是所有 AI 伴侶 App。TC4 標題也是這樣寫，旁白 z2ua 講得精確，沒改。
  - hl-prove kicker「Anthropic · Nov 2–3」：AR 的 datePublished 是 11/2，TC5 說 Tuesday（11/3）發布；寫成區間成立，沒改。
  - 3myb「做亞太的防詐教育」：Google.org 的 600 萬還包含孵化 AI 防禦原型與給政策制定者的資料，「教育」是概括，沒改。
- 需要第二輪：**是**。本輪改了 4 個事實（超過 3 個），要由另一個代理寫 `verify-2.md`。第二輪完成前，這份稿子不能稱為已查核。
