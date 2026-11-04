# daily-ai-20261104 主張與證據

每一行：編號｜主張（旁白或卡片上的說法）｜站上文章；原始來源｜來源查證日｜場景 id。
事實只用站上 news_date 2026-11-03 已發布的文章（`/api/travel/guides/life/<slug>?locale=zh-TW` 取得，2026-11-03，17 篇皆 HTTP 200）與它們列的來源；
撰稿人 2026-11-03 另外打開 TechCrunch 的 Anthropic 原文（核對營收是「季度」而非年化、虧損沒有金額、Brandom 的引句）與 Google 部落格（核對沒有列出機型與地區、Be Scam Ready 已在台灣）。
The Verge 的頁面撰稿環境打不開，The Verge 各則的事實與英文引句依站上文章的轉述（站上文章引用了原文英文句）；查核代理要再逐句對回原文。
「自述」＝公司自己公布、沒有第三方確認；「換算」＝節目依來源數字自己算的；「建議」＝節目的建議，不是來源的說法。

站上文章簡稱：
- ANT＝https://mokaair.com/zh-TW/life/ai-news-anthropic-compute-costs-20261103 ；TC1＝https://techcrunch.com/2026/11/03/anthropic-is-still-grappling-with-the-economics-of-compute/
- AMD＝https://mokaair.com/zh-TW/life/tech-news-amd-q3-2026-results-20261103 ；AMDPR＝https://ir.amd.com/news-events/press-releases/detail/1303/amd-reports-third-quarter-2026-financial-results
- FAL＝https://mokaair.com/zh-TW/life/ai-news-fal-valuation-20261103 ；TC2＝https://techcrunch.com/2026/11/03/ai-inference-startup-fal-doubles-its-valuation-to-16b-as-demand-surges/
- JET＝https://mokaair.com/zh-TW/life/ai-news-data-center-jet-engine-power-20261103 ；TC3＝https://techcrunch.com/2026/11/03/data-centers-are-turning-to-old-jet-engines-as-the-wait-for-power-grows/
- CAMP＝https://mokaair.com/zh-TW/life/ai-news-openai-compute-campuses-20261103 ；V1＝https://www.theverge.com/ai-artificial-intelligence/1025242/openai-quietly-renames-data-centers-as-compute-campuses
- SRCH＝https://mokaair.com/zh-TW/life/ai-news-chatgpt-search-share-20261103 ；V2＝https://www.theverge.com/ai-artificial-intelligence/1025482/openai-says-chatgpt-is-catching-up-to-google-in-search
- SCAM＝https://mokaair.com/zh-TW/life/tech-news-google-apac-scams-20261103 ；GB＝https://blog.google/company-news/inside-google/around-the-globe/google-asia/fight-against-apac-scams/
- APPL＝https://mokaair.com/zh-TW/life/ai-news-apple-18-plus-ai-companions-20261103 ；TC4＝https://techcrunch.com/2026/11/03/apple-restricts-dating-apps-and-ai-companions-to-users-18-and-up/
- FP＝https://mokaair.com/zh-TW/life/ai-news-anthropic-flashprove-20261103 ；AR＝https://www.anthropic.com/research/provable-inference ；TC5＝https://techcrunch.com/2026/11/03/anthropic-is-working-on-a-system-to-prove-ai-models-identity/
- WM＝https://mokaair.com/zh-TW/life/ai-news-claude-text-watermark-20261103 ；RN＝https://platform.claude.com/docs/en/release-notes/overview#november-3-2026
- GIT＝https://mokaair.com/zh-TW/life/crypto-news-gitbook-ai-agent-breach-20261103 ；DC1＝https://decrypt.co/382465/crypto-docs-gitbook-ai-agent-security-breach
- NFX＝https://mokaair.com/zh-TW/life/ai-news-netflix-ai-discover-20261103 ；V3＝https://www.theverge.com/streaming/1025029/netflix-ai-discover-recommendations
- BNB＝https://mokaair.com/zh-TW/life/crypto-news-binance-hack-north-korea-denial-20261103 ；DC2＝https://decrypt.co/382394/north-korea-denies-6-3b-binance-hack-calls-fbi-finding-a-political-provocation
- OKX＝https://mokaair.com/zh-TW/life/crypto-news-okx-ice-tokenized-stock-objections-20261103 ；DC3＝https://decrypt.co/382458/elon-musk-tesla-spacex-block-okx-ice-tokenized-stock
- FSC＝https://mokaair.com/zh-TW/life/crypto-news-taiwan-stablecoin-rules-20261103 ；FSCPR＝https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0,2&mcustomize=news_view.jsp&dataserno=202611030002&dtable=News
- STM＝https://mokaair.com/zh-TW/life/tech-news-steam-review-delays-20261103 ；V4＝https://www.theverge.com/games/1025596/valve-steam-indie-games-missing-launch-dates

## Intro

c1｜2026-11-04 是星期三（曆法）｜—｜—｜intro
c2｜今天的主題：Anthropic 上市前更新的文件（S-1）與算力帳單；營收成長、營運虧損擴大（問題，答案在 c20–c24、片尾）｜ANT；TC1｜2026-11-03｜intro-kai, intro-q

## Headlines

c3｜快訊是 news_date 2026-11-03 的站上文章（「昨天，11 月 3 日的科技新聞」）；其中幾件事發生在週一 11/2，旁白照實說「這週一」｜各站上文章｜2026-11-03｜hl-open
c4｜據 The Verge（單一報導），OpenAI 週一記者會稱 ChatGPT 搜尋查詢量相當於 Google 的 20%（五分之一）；公司自述｜SRCH；V2｜2026-11-03｜hl-search
c5｜「搜尋」定義：使用者查詢觸發網路搜尋；不含解釋名詞或簡單操作說明；Fry 未說明 Google 數字來源｜SRCH；V2｜2026-11-03｜hl-search-def
c6｜Nadella 在 2023 年 Google 反壟斷審判中說，Bing 嘗試十多年後市占約 3%（The Verge 的對照）｜SRCH；V2｜2026-11-03｜hl-search-bing
c7｜OpenAI 上個月宣布 ChatGPT 廣告將呈現贊助產品與服務的圖片｜SRCH；V2｜2026-11-03｜hl-search-ads
c8｜「分清楚哪段是回答、哪段是廣告」是節目建議（旁白與卡片 kicker 已標「我們的建議」「Our advice」）（依站上文章「閱讀 AI 回應時，可留意哪些內容屬於廣告」）｜SRCH｜2026-11-03｜hl-search-tw
c9｜Google 11/3 宣布擴大亞太反詐騙；Android 今年推出偽冒來電偵測，辨識 AI 驅動的電話冒充｜SCAM；GB｜2026-11-03｜hl-scam, hl-scam-what
c10｜Pixel 內建詐騙偵測可對多款常見通訊 App 的潛在詐騙發出警示；今年稍後與夥伴帶給更多 Android 用戶（自述）｜SCAM；GB（"We are partnering to bring this to additional Android users later this year."）｜2026-11-03｜hl-scam-what, hl-scam-more
c11｜Google.org 提供 600 萬美元給 The Asia Foundation 與 Tech for Good Institute，做防詐教育與資助｜SCAM；GB｜2026-11-03｜hl-scam-what
c12｜Google 這篇沒有列出功能涵蓋的國家、地區或機型｜GB（撰稿人 2026-11-03 開原文核對）｜2026-11-03｜hl-scam-tw, tt-settings
c13｜據 TechCrunch，蘋果週一通知開發者：提供約會或浪漫關係功能的 App 須採 18+ 分級｜APPL；TC4｜2026-11-03｜hl-apple
c14｜TechCrunch：多數主流約會服務本來就限成人，更值得留意的是 AI 伴侶 App（Character.AI、Replika 等，常以較年輕族群為目標）｜APPL；TC4｜2026-11-03｜hl-apple-why
c15｜11 月 16 日起開發者須加入新的內容描述；熱門 AI 伴侶 App 截至去年夏天全球下載 2.2 億次｜APPL；TC4｜2026-11-03｜hl-apple-date
c16｜報導未說明蘋果如何執行；「家長控制還是自己設」是節目建議（旁白標「我們建議」）（依站上文章「仍需搭配家長控制」）｜APPL；TC4｜2026-11-03｜hl-apple-tw, tt-parents
c17｜Anthropic 說使用者無法確認回應是否來自宣稱的模型：路由服務可能為省成本換模型、攻擊者可能竄改 token 串流；FlashProve 為開源原型，以零知識密碼學證明回應來自承諾的模型，權重不公開｜FP；AR；TC5｜2026-11-03｜hl-prove, hl-prove-why
c18｜Llama 4 Maverick 上，單張 H100 每秒約證明 110 token；每個 1,024 token 請求的證明約 19 MB；TechCrunch：目前沒有在 Anthropic 或其他實驗室部署的計畫｜FP；AR；TC5｜2026-11-03｜hl-prove-cost
c19｜Claude Platform 發行說明（11/3）：Mythos 5、Opus 4.7、Sonnet 4.6 生成的文字帶 Anthropic 文字浮水印，只限所列平台；Sonnet 4.6 在 temperature、top_p、top_k 設為非預設值時可能不帶；所以沒有浮水印不代表不是 AI 寫的｜WM；RN｜2026-11-03｜hl-mark, hl-mark-limit
c20｜GitBook 揭露 11/2 歐洲中部時間晚上 7 點（週一晚上）遭使用 AI 代理的有針對性攻擊，攻擊者取得部分基礎設施憑證｜GIT；DC1｜2026-11-03｜hl-gitbook
c21｜AI 代理與聊天機器人的差別：能執行一連串動作、操作軟體、在有限的人為監督下完成任務（Decrypt 的說明）｜GIT；DC1｜2026-11-03｜hl-gitbook-ai
c22｜可能外洩：API 權杖、整合密鑰、使用者向 GitBook AI 助理提交的問題；GitBook 已讓客戶 API 權杖失效並要求更換權杖與密鑰；沒有證據顯示託管內容遭修改｜GIT；DC1｜2026-11-03｜hl-gitbook-what, hl-gitbook-do
c23｜GitBook 尚未說明攻擊如何進行、涉及哪些 AI 系統、憑證怎麼被取得｜GIT；DC1｜2026-11-03｜hl-gitbook-unknown
c24｜Netflix 電視 App 新增實驗性 AI Discover 分頁，第一項實驗是主題式推薦（Something Light、Family Movie Night、Quick Watches）；可告知不喜歡，App 會記住；美國逐步開放，英文、支援的電視；未說明何時擴及其他地區｜NFX；V3｜2026-11-03｜hl-netflix, hl-netflix-how, hl-netflix-tw
c25｜Signal Number：運算成本占 Anthropic 營收 58%；「每 100 美元營收有 58 美元用在運算」是換算｜ANT；TC1｜2026-11-03｜hl-number, hl-number-what, sd-share

## Signal of the Day

c26｜「想像你是一個盯著新股的分析師」是情境；Anthropic 週一（11/2）提交新文件，更新前一週公布的 S-1｜ANT；TC1｜2026-11-03｜sd-scene, sd-back
c27｜S-1 是公司準備 IPO 時提交、含財務數據的文件｜ANT｜2026-11-03｜sd-s1
c28｜先前財務揭露只到 6 月 30 日，新數據多一季到 9 月 30 日；TechCrunch：越接近 IPO，公司終於披露更多運算經濟學｜ANT；TC1｜2026-11-03｜sd-why-now, sd-econ
c29｜運算＝訓練與執行 AI 模型所需的算力｜ANT｜2026-11-03｜sd-compute
c30｜季度營收 170 億美元，前一季 115 億美元（TC1 原文為季度營收，非年化）；「快五成」為換算（約 48%）｜ANT；TC1｜2026-11-03｜sd-revenue
c31｜營運虧損同時擴大，主因之一是運算成本上升（TC1「thanks in large part to」；卡片 kicker 查核第 2 輪由「The main reason」改「In large part」）；TechCrunch 沒寫虧損金額｜ANT；TC1｜2026-11-03｜sd-loss, sd-loss-why
c32｜運算占營收比重：前一季 48%，新一季 58%；「十個百分點」為換算｜ANT；TC1｜2026-11-03｜sd-share
c33｜本季運算帳單 100 億美元，其中 50 億美元為短期承諾，成本明顯高於多年期承諾的同等運算｜ANT；TC1｜2026-11-03｜sd-bill, sd-short
c34｜TechCrunch 解讀：需求成長太快，必須倉促取得算力而付出較高價格｜ANT；TC1｜2026-11-03｜sd-rush
c35｜每 1 美元運算對應營收：自 2025 年初上升，峰值略高於 2 倍，回落至 1.72 倍（旁白不說峰值在哪一季，TC1 沒寫）｜ANT；TC1｜2026-11-03｜sd-ratio
c36｜Anthropic 每月付 SpaceX 12.5 億美元運算費；與 Nscale、Akamai、Volta 有數十億美元合約；TechCrunch 稱之為 neocloud（非超大規模雲端），合約較彈性、費率較高｜ANT；TC1｜2026-11-03｜sd-spacex, sd-neo
c37｜Anthropic Direct 建立自有運算基礎；TechCrunch 認為跟不上需求成長｜ANT；TC1｜2026-11-03｜sd-direct
c38｜AMD 11/3 公布第三季：資料中心營收 85 億美元、年增 97%（「將近一倍」）；遊戲營收年減 40%｜AMD；AMDPR｜2026-11-03｜sd-chips, sd-amd
c39｜AMD 稱 Anthropic、Meta、微軟、OpenAI 與 Oracle 雲端基礎設施在首批 Helios 機櫃上執行工作負載；未公布金額；公司自述｜AMD；AMDPR｜2026-11-03｜sd-helios, sd-helios-n
c40｜Fal 託管並運行 AI 影像、圖像與音訊模型；最新一輪募 13 億美元；估值（Bloomberg，經 TechCrunch）為 4 月的兩倍｜FAL；TC2｜2026-11-03｜sd-fal
c41｜據知情人士，推論公司因購買或租用運算資源成本高，毛利仍薄｜FAL；TC2｜2026-11-03｜sd-fal-margin
c42｜TechCrunch 轉述紐約時報：部分 AI 資料中心等不到電網與新渦輪機，改用退役飛機引擎改裝、燒天然氣的機組發電｜JET；TC3｜2026-11-03｜sd-power
c43｜IEA：北維吉尼亞 100 兆瓦接上電網約七年；Rystad 的 Martinsen：噴射引擎機組可在 24 個月內讓資料中心運轉；效率較低、污染較多（NYT）｜JET；TC3｜2026-11-03｜sd-jet
c44｜上個月微軟退出 Nscale 在英國 Loughton 資料中心的主要客戶角色，因當地電力公司要到 2030 年代初至中期才能供應足夠電力｜JET；TC3｜2026-11-03｜sd-nscale, sd-nscale-why
c45｜錢的流向整理（晶片接單、雲端越急越貴、電是最慢一環）、「Anthropic 自己最吃虧」是節目依 c33–c44 的歸納｜ANT；AMD；JET｜2026-11-03｜sd-flow, sd-squeezed, sd-wrap
c46｜文章沒說 AI 訂閱會不會漲價；「每問一句都是帳單的一小格」是節目的說法，依 ANT「AI 服務背後的成本與算力供應是影響營運的重要因素」｜ANT｜2026-11-03｜sd-you
c47｜今天的來源都沒有提到台灣廠商；AMD 風險因素列出出口管制、關稅、記憶體供應、依賴第三方製造，未點名製造商｜AMD；AMDPR；ANT；FAL；JET｜2026-11-03｜sd-taiwan, sd-risk, sd-asia
c48｜公司預期運算與基礎設施支出絕對金額增加、仍為最大營運支出；TechCrunch 認為更像短暫波動；債券市場緊張或地方反對加劇可能讓資料中心建設放緩｜ANT；TC1｜2026-11-03｜sd-next
c49｜TechCrunch：營收每季成長近 50%，投資人就不太擔心運算成本｜ANT；TC1｜2026-11-03｜sd-calm
c50｜報導沒有 IPO 日期，只說 Anthropic 逐步接近 IPO｜TC1｜2026-11-03｜sd-ipo

## What People Are Saying

c51｜Russell Brandom（TC1 作者）："At a moment when the company could win over IPO investors by showing margins improving, they're getting worse."（卡片取後半）｜TC1｜2026-11-03｜wp-tc
c52｜Rystad Energy 分析師 Audun Martinsen 對紐約時報："It's all about getting power as fast as possible"｜JET；TC3｜2026-11-03｜wp-rystad
c53｜The Verge：OpenAI 週一 Grid Protectors Program 公告以「compute campus」為主要用語、「data center」只出現兩次；OpenAI 未回應置評｜CAMP；V1｜2026-11-03｜wp-rename, wp-conner
c54｜NAACP 環境與氣候正義中心的 Abre' Conner：改名 "does not fix the problem"｜CAMP；V1｜2026-11-03｜wp-conner
c55｜ChatGPT 消費者產品負責人 Adam Fry："most people do not seem to mind ads in the product"｜SRCH；V2｜2026-11-03｜wp-fry

## Money Signal

c56｜據 Decrypt 引述韓聯社，北韓否認涉及幣安遭駭；金與正稱美方認定是「嚴重的政治挑釁」｜BNB；DC2｜2026-11-03｜ms-open, ms-kim
c57｜FBI 週六（上週六，10/31）表示北韓駭客組織 TraderTraitor 要為盜取幣安超過 60 億美元負責；Decrypt 先前報導 64.3 億美元中約 28.5 億美元已被凍結或查扣（查核第 2 輪：出自 Decrypt 11/2 週一的 https://decrypt.co/382355/north-korea-laundering-binance-hack-loot-new-wallet-every-25-seconds ，引 Elliptic，DC2 連到這篇並重述）｜BNB；DC2；DC4｜2026-11-03｜ms-fbi
c58｜幣安稱已補足約 95% 被盜資產；持有前 10 大代幣的用戶可透過 10 月 31 日備付快照的零知識證明驗證餘額是否有足額資產支撐｜BNB；DC2｜2026-11-03｜ms-users, ms-proof
c59｜零知識證明：在不公開細節的情況下證明某件事為真（BNB 的名詞解釋；FlashProve 也是零知識，c17）｜BNB；FP｜2026-11-03｜ms-zk
c60｜「看交易所有沒有給你自己能檢查的證明」是節目建議（旁白與卡片 kicker 已標「我們的建議」「Our advice」）（依 BNB「值得留意的是交易所是否公開可驗證的備付證明」）｜BNB｜2026-11-03｜ms-lesson
c61｜OKXICE TSV 是 ICE 與 OKX 美國控股公司各半的合資；11/2 通知新增 Amazon、Tesla、SpaceX、Netflix、Lam Research、SoFi，異議公司總數 56 家｜OKX；DC3｜2026-11-03｜ms-okx, ms-who
c62｜代幣化股票：把股票以區塊鏈上的代幣呈現、在區塊鏈平台交易｜OKX｜2026-11-03｜ms-token
c63｜SEC 9 月的創新豁免：平台須先通知公司；公司 30 天內書面異議，平台不能提供由無關第三方代幣化的該股票（旁白「別人代做的代幣版」；發行公司自己代幣化的仍可上）；只適用該平台；平台仍在計畫階段｜OKX；DC3｜2026-11-03｜ms-rule, ms-okx-you
c64｜金管會 11/3：研訂「穩定幣發行許可及管理辦法」草案等，近日內預告｜FSC；FSCPR｜2026-11-03｜ms-tw
c65｜申請對象：銀行、金融控股公司或銀行轉投資之股份有限公司（FSCPR 第 (2) 款是一項：金控或銀行轉投資的公司，不是金控本身；旁白「金控或銀行轉投資的公司」，查核第 2 輪改）及金管會公告的其他機構；非銀行發行人最低實收資本額新臺幣 3 億元｜FSC；FSCPR｜2026-11-03｜ms-tw-who
c66｜可發行與新臺幣或單一外國貨幣一比一連結的穩定幣；準備資產按公允價值不低於流通在外總餘額；確認認購人與贖回人身分；定期委託會計師查核｜FSC；FSCPR｜2026-11-03｜ms-tw-def, ms-tw-what
c67｜公告翌日起 40 日內陳述意見；配合虛擬資產服務法施行日期生效（施行日期由行政院另定）｜FSC；FSCPR｜2026-11-03｜ms-tw-when, ms-tw-you

## Try This

c68｜Try This 三步（掛掉回撥、Android 設定搜尋「詐騙」、家長自己設家長控制）是節目建議，不是 Google 或蘋果的指示｜—（建議）｜—｜tt-open, tt-call, tt-settings, tt-parents
c69｜Be Scam Ready 是模擬常見詐騙的教育遊戲，已在新加坡、泰國與台灣提供，將擴展至印尼、日本、馬來西亞、菲律賓、越南｜SCAM；GB｜2026-11-03｜tt-game

## Noise of the Day

c70｜據 The Verge，多名獨立開發者稱 Steam 審核等待過久、部分遊戲錯過發售日｜STM；V4｜2026-11-03｜nd-open
c71｜Valve：商店頁面審核通常 3–5 個工作天；Food Devils 10/12 提交、原定 11/3 搶先體驗上市仍在等待；Wheel Make It 延後近兩週；「三個禮拜」為換算（10/12 至 11/3）｜STM；V4｜2026-11-03｜nd-wait
c72｜開發者推測是 AI slop 塞爆審核；Valve 在 The Verge 刊出後發文承認送審量大增、審核落後，現在最多要 12 個工作天（V4「Update, November 3rd: Added new post from Valve」；查核第 1 輪改，原稿「未立即回覆」已過時）；V4 的轉述沒有把延誤歸因於 AI｜STM；V4｜2026-11-03｜nd-why, nd-valve
c73｜10 月 Steam Next Fest 7,240 款、比 6 月多 65.2%（How to Market a Game，經 The Verge）；一名 Reddit 使用者發現 Valve 2024 年起要求標示後發售的遊戲有 49.9% 帶 AI 揭露｜STM；V4｜2026-11-03｜nd-numbers

## Sola's Take、片尾

c74｜「今天最重要的是 Anthropic 的文件」「帳單怎麼付會影響 AI 服務的樣子」「我不確定是否只是波動」是節目的看法；依 c30–c49；報導沒說廣告與算力成本有關｜—｜—｜tk-main, tk-why, tk-unsure
c75｜每則的完整整理在 Mokaair 文章，連結在說明欄（說明欄列 16 篇站上文章）｜各站上文章｜2026-11-03｜tk-site
c76｜片尾答案：錢大多付給了算力，而且是急著買的（c32、c33）｜ANT；TC1｜2026-11-03｜outro

## 我懷疑但沒動的事

- Anthropic 的季度營收 170 億美元聽起來很大，撰稿人開 TC1 原文確認寫的是 "revenue reached $17 billion, up from $11.5 billion in the previous quarter"，是季度數字；查核代理可再對 S-1 本身。
- 「峰值略高於兩倍」：站上文章寫「上一季峰值」，TC1 只說 peaked at just over 2x 再回落；旁白不說是哪一季，站上文章的「上一季」可能要修。
- Fal「估值是四月的兩倍」出自 Bloomberg 經 TechCrunch 轉述，旁白已說「據 Bloomberg」。
- The Verge 四篇（V1–V4）在撰稿環境打不開，引句照站上文章所列的英文原文；查核代理要逐句對回。
- 「FBI 上週六」：BNB 寫「FBI 週六表示」，Decrypt 文章 11/3（週二）發布，推定是 10/31。
- Nadella 那句：旁白說「微軟執行長 2023 年在法庭上說」，依 SRCH 的「微軟執行長 Nadella 在 2023 年的 Google 反壟斷審判中說」。

## 沒有放進來的

- CrowdStrike 與 Fiddler（ai-news-crowdstrike-ai-kill-switch-fiddler-20261103）：題材與 GitBook 重疊，沒選。
- 台灣或亞洲供應鏈與 Anthropic 算力的直接關聯：今天的來源都沒有，旁白明說不猜。
- Anthropic 營運虧損的金額：TC1 沒寫，旁白只說「擴大」。

## 進度

- 110 個場景、268 句；`lint` 0 錯誤（剩下的警告是開場濃縮兩條與 Headlines 開頭的固定句，對本節目不適用）。
- 待做：另派查核代理照 `prompts/verifier-video.md` 逐則對回來源；Whisper 第二意見與試聽（新加的發音字典詞）；配樂已綁 `techsignal-bed.mp3`。
