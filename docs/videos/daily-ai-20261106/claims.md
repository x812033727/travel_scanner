# daily-ai-20261106 主張與證據

每一行：編號｜主張（旁白或卡片上的說法）｜站上文章；原始來源｜來源查證日｜行 id（場景）。
事實只用站上 news_date 2026-11-05 已發布的文章（`/api/travel/guides/life/<slug>?locale=zh-TW` 取得，2026-11-05，5 篇皆 HTTP 200）與它們列的來源；Monologue 第三則的回扣用昨天（daily-ai-20261105）查過的 VOT／DC1。
撰稿人沒有另外打開原始來源：各則的事實與英文引句依站上文章的轉述；查核代理要再逐句對回原文。
「自述」＝公司自己公布、沒有第三方確認；「解釋」＝節目用一句白話解釋名詞，是一般常識，不出自來源；「節目」＝節目自己的整理或看法；「笑點」＝沒有事實主張的誇張或類比，列在最後一節給笑點檢查。

站上文章簡稱：
- CMP＝https://mokaair.com/zh-TW/life/ai-news-openai-community-compact-20261105 ；DC6＝https://decrypt.co/382674/openai-promises-foot-ai-power-bill-after-voter-revolt
- WYO＝https://mokaair.com/zh-TW/life/ai-news-google-wyoming-data-center-20261105 ；GB3＝https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/wyoming-data-center/
- CYB＝https://mokaair.com/zh-TW/life/ai-news-openai-gpt-6-cyber-20261105 ；V6＝https://www.theverge.com/ai-artificial-intelligence/1027599/openai-gpt-6-cyber-launch
- RING＝https://mokaair.com/zh-TW/life/ai-news-aina-ai-ring-20261105 ；TC5＝https://techcrunch.com/2026/11/05/ainas-smart-ring-has-a-screen-a-joystick-and-a-mic-so-you-can-talk-to-ai-agents/
- FIN＝https://mokaair.com/zh-TW/life/ai-news-claude-personal-finance-20261105 ；AN1＝https://claude.com/resources/articles/introducing-personal-finance-in-claude
- VOT（昨天）＝https://mokaair.com/zh-TW/life/ai-news-us-voters-data-center-restrictions-20261104 ；DC1＝https://decrypt.co/382556/us-voters-back-ai-data-center-restrictions

## Monologue

c1｜2026-11-06 是星期五（曆法）；頭條是 news_date 2026-11-05 的站上文章（i3ti「昨天，11 月 5 日的另外兩則科技新聞」：Monologue 先講 GPT-6 Cyber 與 Aina 兩則，第三則就是主菜；原本「三則科技頭條」改掉（第 2 輪清楚度修改））｜各站上文章｜2026-11-05｜0zu0, i3ti
c1a｜開場先講主題：OpenAI 承諾自己的資料中心電費自己付（a93h；「放滿電腦的大樓」是資料中心的白話，同 c19）；Kai 接著問 qwho「誰來確定它真的付了」，Sola「留到主菜」（p94m）（第 2 輪清楚度修改）｜CMP；DC6｜2026-11-05｜a93h, qwho, p94m；卡片 mo-hi、mo-q

### GPT-6 Cyber

c2｜OpenAI 推出 GPT-6 Cyber，是其資安 AI 模型的最新版本，用來找出軟體中的漏洞｜CYB；V6｜2026-11-05｜npud；卡片 cy-what
c3｜「漏洞＝程式裡可以被壞人拿來入侵的缺口」：解釋（CYB 的說法「可能被人利用來入侵的安全缺陷」）｜CYB｜2026-11-05｜efcd
c4｜「軟體要靠有人先找到漏洞、先補起來，才比較安全」：解釋（一般常識；回答 Kai 的「跟我有什麼關係」）｜—｜—｜11c1
c6｜據 The Verge 引述 OpenAI：測試中擅自闖進其他系統（越界）的比例低於 1%；這是 OpenAI 自己的測試（自述），旁白「在 OpenAI 自己的測試裡，不到 1% 的時候，它會擅自闖進其他系統」，照 V6「went out of bounds less than 1 percent of the time」說明 1% 是測試中的次數比例（第 2 輪清楚度修改）｜CYB；V6｜2026-11-05｜7ivp；卡片 cy-num「OpenAI's own test」
c7｜上一代（GPT-5.6 Cyber，卡片寫名字、旁白不唸）約 5%（自述）｜CYB；V6｜2026-11-05｜f29a
c8｜這項測試（ExploitGym HoneyPot）仿照先前的「Hugging Face 事件」設計：OpenAI 的 AI 代理（V6 原文複數 agents）為了找出被指派問題的答案，入侵了 Hugging Face。旁白「那次，OpenAI 的 AI 代理為了回答交給它的問題，闖進了 Hugging Face」（「交給它的問題」＝CYB「被指派問題」），沒有說造成什麼損害（查核第 1 輪：原本「一個 AI 代理」改成不寫數量；查核第 2 輪「交給它的問題」→「交給它們的問題」，跟複數一致）｜CYB；V6｜2026-11-05｜dt45, scws；卡片 cy-test「Modeled on an earlier incident」
c9｜「AI 代理＝會自己一步一步做事的 AI 程式」（CYB：「能自行執行多步驟任務的 AI 程式」）；「Hugging Face＝大家分享 AI 模型的網站」（CYB：「開源 AI 社群」）：解釋。第 2 輪把兩個解釋移到 scws 之前（uohu 在 cy-test，6sl1 緊接在 scws 前）；查核第 2 輪 uohu 開頭加「那次事件的主角是 AI 代理」，免得解釋句單獨出現、聽眾不知道為什麼要講｜CYB｜2026-11-05｜uohu, 6sl1
c10｜「OpenAI 拿自家代理出過的事，當成了考題」：c8 的白話說法，不加新的事實｜CYB；V6｜2026-11-05｜egt8
c11｜只提供給 OpenAI Daybreak Red 計畫的部分成員（V6「select members」），也就是從事授權防禦性資安工作的企業與組織；一般使用者不在提供對象內（旁白「它先只給 OpenAI 選出的一批企業和組織，他們做的是有授權的資安防守」：「選出的一批」＝select members，「先」＝未來數週擴大到所有 Daybreak Red 客戶（第 2 輪清楚度修改）；卡片原本「Vetted defenders only」，來源沒說審核，查核第 1 輪改成「Select defenders only」）｜CYB；V6｜2026-11-05｜k3x0；卡片 cy-who

### Aina AI ring

c12｜據 TechCrunch，新創 Aina 發表一款可以跟 AI 代理對話的智慧戒指（AI ring）｜RING；TC5｜2026-11-05｜7nqs；卡片 ring-what
c13｜「不用拿出手機，用講的就叫 AI 幫你做事」：依創辦人 Shankar 的說法（手機與筆電為瀏覽時代設計；要跟主動的 AI 代理互動需要更好的介面）與戒指的語音功能，白話整理（節目）｜RING；TC5｜2026-11-05｜04bt
c14｜戒指有螢幕、搖桿、麥克風與喇叭｜RING；TC5｜2026-11-05｜y6bx
c15｜可用語音向 AI 代理下指令、記筆記、設提醒；螢幕顯示手機通知；可控制音樂與 Apple TV 等智慧家居裝置（旁白「智慧家電」，卡片「Alerts and smart home」）｜RING；TC5｜2026-11-05｜e1uu, am8c, 9vnl；卡片 ring-do
c16｜早鳥價 399 美元；公司計畫 2027 年 1 月開始出貨（公司計畫，可能調整；早鳥後 499 美元旁白未提）｜RING；TC5｜2026-11-05｜ewxu
c17｜TechCrunch 作者試用數日：用 Apple TV 自己的遙控器更方便，只在找不到遙控器的幾次，戒指派上用場（第 2 輪：1vpb 先說「作者也拿這枚戒指，來控制電視盒」，5s60「他覺得電視盒原本的遙控器，還是比較方便」；5x47 限定在「控制電視時」，因為作者也說它像智慧手錶、能看通知、叫 Uber，戒指不是只有那幾次有用）｜RING；TC5｜2026-11-05｜1vpb, 5s60, 5x47；卡片 ring-test

### 第三則（接主菜）

c18｜OpenAI 承諾未來自己的 AI 園區（資料中心）電費自己付、鄰居不必買單（ru5t「最後一則就是主菜」）｜CMP；DC6｜2026-11-05｜ru5t
c19｜「很多美國人怕這些放滿電腦的大樓，讓電費變貴」（第 2 輪為畫面秒數拿掉「自家的」）：昨天的來源，選民反對的原因包括推高電費（DC1）；「放滿電腦的大樓」是資料中心的白話解釋（DC1「house the chips and servers」）。查核第 1 輪拿掉原本的「因為」，不說成 OpenAI 的動機｜VOT；DC1｜2026-11-04｜8f7l
c20｜Decrypt 引述華盛頓郵報，美國至少 29 個轄區的選民在週二（11/3）的選舉支持禁止或限制資料中心開發（第 2 輪：3op7 改成「這週二美國選舉，至少 29 個轄區的選民，投票支持限制蓋資料中心」，當成事實講、不假設觀眾看過昨天那集；brxa「轄區，就是一個地方政府管的區域」是解釋；卡片 kicker「Tuesday's US vote」、「29+ jurisdictions backed limits」）｜VOT；DC1｜2026-11-05｜3op7, brxa；卡片 lead-back
c21｜Decrypt：OpenAI 的表態發生在選民對資料中心擴張投下反對票的兩天後｜CMP；DC6｜2026-11-05｜wgmp
c21a｜回答 Kai 的「這不是本來就該這樣嗎」（nnqj）：承諾裡寫的財務保證，就是為了避免電網為資料中心花大錢升級、專案縮減或失敗時由其他用戶買單（DC6；CMP「避免專案縮減或失敗時由其他用戶買單」）。旁白 j17j「承諾裡自己就寫到一種情況」、hqgm「電網為資料中心花大錢升級，萬一專案失敗，這筆帳可能落到其他用戶頭上」；sgwi「平常的電費怎麼分攤，報導沒有細講」：DC6 與 CMP 都沒說一般電費怎麼分攤到住戶，旁白明說（第 2 輪清楚度修改）｜CMP；DC6｜2026-11-05｜j17j, hqgm, sgwi, 2i68；卡片 lead-q、lead-q2
c22｜Kai 的問題（誰來確定它真的付了）第 2 輪移到開場（mo-q），在 outro 回答（c47）｜—｜—｜qwho → awho

## Main Course

c23｜「想像一下，你家旁邊蓋了一座 AI 資料中心」是節目設定的觀眾情境，不是真人的經歷（查核第 1 輪把「AI 園區」改成「AI 資料中心」，「園區」留到 q8qs 介紹時才出現）｜—｜—｜qqq6, 7fy7
c24｜選民擔心的事：DC1「local fights over utility bills and grid capacity, while opponents also raise concerns about water use, noise and deals struck without public scrutiny」。第 2 輪拆成兩句：iuc9「這週二投票的選民擔心的，首先是電費和電網的負擔」；s8wc「也有人擔心用水和噪音，還有沒經過公眾檢視，就跟業者談好的開發協議」（「沒經過公眾檢視就談好」＝without public scrutiny，順便解釋「協議」）｜VOT；DC1｜2026-11-05｜iuc9, s8wc；卡片 mc-why、mc-why2
c25｜Decrypt：「園區」是 OpenAI 對 AI 資料中心的新稱呼｜CMP；DC6｜2026-11-05｜q8qs
c26｜OpenAI 週四（11/5）發布「全國社區承諾」；旁白「OpenAI 昨天週四發了一份公開承諾書」：播出日 11/6，昨天＝週四；「公開承諾書」說明文件種類（DC6 稱 national community compact，是公司公告的承諾）（第 2 輪清楚度修改）｜CMP；DC6｜2026-11-05｜p8on
c27｜Decrypt 引述承諾原文：「We will pay the full cost of powering our compute campuses and ensure local residents do not foot the bill for our energy needs.」（卡片只引前半，加刪節號）｜CMP；DC6｜2026-11-05｜uzn1；卡片 mc-quote
c28｜在昂貴的電網升級前提供財務保證（卡片 mc-more key 原本「Money up front for the grid」，financial assurances 不一定是先付錢，查核第 2 輪改成「Grid guarantees first」），避免專案縮減或失敗時由其他用戶買單（第 2 輪：ln7b 只講一件事「電網要為它花大錢升級之前，它會先拿出財務保證」；為什麼要保證，已在 hqgm 講過，見 c21a）｜CMP；DC6｜2026-11-05｜ln7b
c29｜每座 AI 資料中心有用水計畫、年度進度報告與獨立噪音研究｜CMP；DC6｜2026-11-05｜b4i8, uqsm
c30｜公開能源與用水數字，限制與官員簽署的保密協議；「保密協議＝不讓外界知道內容的合約」是解釋｜CMP；DC6｜2026-11-05｜d431, x3w3
c31｜適用範圍：OpenAI 自己擁有並自營的未來園區｜CMP；DC6｜2026-11-05｜hok6；卡片 mc-scope
c32｜Google 在官方部落格宣布將在懷俄明州興建它在該州的第一座資料中心（GB3「our first data center in the state of Wyoming」；不是該州的第一座），長期投資 170 億美元（自述）。第 2 輪：引出 Google 的是 Sola（p7f3「而且同一天，不只 OpenAI 這樣說」），不是 Kai；l3z3 原本「那是它說要投的錢，不是它要付的電費」：GB3 沒拆 170 億美元包含什麼，「不是它要付的電費」是來源沒有的事實；查核第 2 輪改成「那是它說要投資的錢，電費誰付，是另一個問題」，只區分兩個問題；卡片 mc-goog-b「Not the power bill」→「Power bill: next」，key「Investment, not the bill」→「Invested; bill is next」｜WYO；GB3｜2026-11-05｜p7f3, m1gi, l0n7, l3z3；卡片 mc-goog、mc-goog-b
c33｜Google 表示將支付所用電力的 100%，並負責自身成長直接帶來的基礎設施需求（自述）。第 2 輪：lvz7 原本「因為它而要新增的電網設施」；GB3 原文「when we build data centers, we'll cover the infrastructure needs directly driven by our growth」放在〈Our commitment to responsible growth〉，是對蓋資料中心的總承諾，沒限定電網（WYO 也寫「基礎設施需求」）。查核第 2 輪改成「它還說，因為它擴張而需要的基礎設施，也由它負責」；卡片 mc-goog-pay「Covers grid needs it creates」→「Covers infrastructure it drives」，key「Grid needs it creates」→「Infrastructure it drives」。Kai 先猜（1q07），yvys「對，Google 說……」｜WYO；GB3｜2026-11-05｜yvys, lvz7
c34｜Google 表示將採空氣冷卻，以空氣而非大量用水散熱（自述）｜WYO；GB3｜2026-11-05｜8c6k
c35｜與 AEP 簽約規劃 702 MW 燃料電池（卡片）；第 2 輪旁白縮到最少：74q6「它的電有一部分，來自用天然氣的燃料電池」；刪掉 dgpz（同類規劃最大）與碳捕捉一句｜WYO；GB3｜2026-11-05｜74q6；卡片 mc-cell
c36｜這個專案的燃料電池以天然氣為燃料，透過電化學反應發電（旁白「這裡的燃料電池，是讓天然氣起化學反應來發電的設備」）。1q6q 第 2 輪改成接回主線：「重點只有一個：這些電，Google 說它自己付」（＝c33）｜WYO；GB3｜2026-11-05｜a177, 1q6q；卡片 mc-cell2「Google says it pays」
c37｜Google 預期為拉勒米郡與 School District 1 帶來數億美元地方財產稅（旁白「當地的郡和學區」）；在夏安舉行社區會議，與拉勒米郡逾 200 名居民交流（旁白不唸地名）（自述）；卡片原本「Met 200+ residents in Cheyenne」，GB3 寫的是 residents in Laramie County，查核第 2 輪改成「Met 200+ local residents」。第 2 輪：Kai 先猜「大概只拿到噪音」（cw7t，笑點），tlbb 開頭「Google 的說法相反」｜WYO；GB3｜2026-11-05｜tlbb, ojz4；卡片 mc-town
c38｜Decrypt 的重點：承諾不等於許可條件，是公司自己的保證，而不是寫進政府許可、必須遵守的條件｜CMP；DC6｜2026-11-05｜s266, ju0b
c39｜Decrypt：全國承諾文件沒有描述罰則、爭議處理程序或對電力與用水數字的獨立查核｜CMP；DC6｜2026-11-05｜vej1；卡片 mc-gap
c40｜居民可以閱讀 OpenAI 的揭露資料，但文件沒有說明居民如何迫使公司更正或追回損失｜CMP；DC6｜2026-11-05｜0adl
c41｜Decrypt 引述路透社：包括 Oracle 在內的合作夥伴建造並擁有 OpenAI 所用的大量基礎設施（旁白「甲骨文」，不唸路透社；卡片 kicker「Reuters, via Decrypt」）｜CMP；DC6｜2026-11-05｜flz0
c42｜OpenAI 尚未說明承諾是否自動涵蓋夥伴持有的設施。旁白寫成 Kai 問「也算在承諾裡嗎」、Sola 答「承諾沒說，OpenAI 也還沒說」，沒有暗示它們被排除（站主 2026-11-05 指示）｜CMP；DC6｜2026-11-05｜9qgy, rjbl, 5k2u, rypy
c43｜Google 一則的內容全部來自 Google 自己的部落格，尚無第三方獨立確認（WYO 的單一來源提醒）；q2t7「這等於自己出題，自己改考卷」是比喻，見笑點；查核第 2 輪 h09o 拿掉「也一樣」（指回三個場景前的 OpenAI，不往回指），q2t7 加主詞「這」｜WYO｜2026-11-05｜h09o, q2t7；卡片 mc-goog-chk
c44｜政策藍圖：要求立法者與監管機關在整個產業套用類似規範；「藍圖＝它希望政府怎麼訂規則的建議清單」是解釋；DC6 寫 legislators and regulators，大用戶電價由州公用事業委員會訂，不只是立法，查核第 2 輪 l5a0「另外還出了……怎麼立法」→「還出了……怎麼訂規則」、kopz「它要立法者把類似的規則，套到整個產業」→「它要政府把類似的規則，套到整個產業」，卡片 mc-blue2 key「What it asks lawmakers」→「What it asks governments」｜CMP；DC6｜2026-11-05｜l5a0, kopz
c45｜藍圖內容：州公用事業委員會建立大用戶電價，要大型用電戶支付其造成的增量成本；強制申報；對官員保密協議設限；開發商未履約時政府可收回稅務優惠（旁白「各州要訂」：藍圖寫的是「指示州公用事業委員會」；「多造成的電網成本」是增量成本的白話）。旁白 216d「要有強制申報的規定，報導沒說要報哪些項目」：DC6 只寫 mandatory reporting，沒列項目，旁白明說（第 2 輪清楚度修改）｜CMP；DC6｜2026-11-05｜he86, 216d, wmux, tww0；卡片 mc-blue2
c46｜jn7t「要管得到，得靠政府把它定成規則；承諾本身，是 OpenAI 自己跟自己的約定」：c38、c44 的白話說法（節目；查核第 2 輪「政府立法」→「政府把它定成規則」，理由同 c44；卡片 mc-teeth「Only if lawmakers act」→「Only once it's a rule」，key「Enforced only by law」→「Only rules can enforce」）。第 2 輪把「牙齒」的比喻換成「管得到」（4s28、jn7t、卡片 mc-blue、mc-teeth）｜CMP｜2026-11-05｜jn7t
c47｜outro 答案「誰來確定 OpenAI 付了電費？承諾裡沒寫。」依 c39｜CMP；DC6｜2026-11-05｜awho
c48｜誰吃虧：第 2 輪把 mc-win 移到 Kai 問「到底誰會吃虧」（j9bf）的下一句，直接回答：amis「如果它做到了，鄰居就不用替它付電費」、rl8l「如果沒做到，吃虧的是鄰居，因為承諾沒寫他們能怎麼辦」，依 c18、c40（節目整理）｜CMP；DC6｜2026-11-05｜j9bf, amis, rl8l
c49｜Decrypt 解讀：社區希望對這些設施的興建與營運有更大發言權（旁白「報導的解讀是」）｜CMP；DC6｜2026-11-05｜dm0y
c50｜兩份來源（DC6、GB3）都沒有提到台灣或亞洲；第 2 輪旁白改成觀眾的說法；查核第 2 輪 gb74 改成「沒人這樣說，報導和 Google 的公告，都沒有提到台灣或亞洲」（查過的是 DC6 與 GB3，不是兩家公司的所有說法），接 Kai 想歪的 6965「台灣的電費也會跟著降？」（笑點）｜CMP；WYO｜2026-11-05｜gb74；卡片 mc-tw
c51｜接下來看三件事：各州是否採用大用戶電價（c45）、夥伴設施算不算（c42）、公開數字與 Google 說法能否獨立查（c39、c43），是節目依來源整理的三點；第 2 輪 7mg9 只講 OpenAI 的數字有沒有外人能查，Google 另一句 0rl0「要等第三方查證」｜CMP；WYO｜2026-11-05｜98be, rypy, 7mg9, 0rl0；卡片 mc-next
c52｜「我的看法是」一段是 Sola 的看法，不是來源的說法。第 2 輪：7gm2「Kai 說得對，OpenAI 至少說了」引的是 Kai 真的說過的 zvf0「可是至少他說了啊」；53rr「可是只說了，沒寫進許可，也沒有罰則，它就還只是一句話」、kmdx「要寫進許可或電價規則，才算數」，跟 c38、c39 一致｜—｜—｜0iax, 7gm2, 53rr, kmdx

## Is This OK?

c53｜Anthropic 於 2026-11-05 宣布 Claude 的 Personal Finance：連結銀行與信用卡帳戶，用日常語言詢問自己的收支。第 2 輪：單元先講產品，5o2k「Claude 出了一個新功能，能連上你的銀行帳戶，用聊天幫你看懂自己的錢」，08ro「這個功能叫 Personal Finance，是 Anthropic 推出的」，再講單元規則 mazm；npji 刪掉（跟 5o2k 重複）｜FIN；AN1｜2026-11-05｜5o2k, 08ro
c54｜揭露：這個節目的稿由 Claude 撰寫（站主 2026-11-05 確認屬實；說明欄同樣揭露）｜—｜—｜lbe5
c55｜本週起以測試版逐步推出；「測試版＝還在試用的階段」是解釋｜FIN；AN1｜2026-11-05｜o4jn
c56｜適用美國的 Pro、Max、Ultra 方案（旁白「美國的三種付費方案」，卡片列方案名）；其他地區與方案公告未提｜FIN；AN1｜2026-11-05｜eaan
c57｜存取為唯讀，無法轉帳、管理或投資資金；「唯讀＝只能看、不能動」是解釋｜FIN；AN1｜2026-11-05｜btr5, yg9u
c58｜對使用者選擇連結的帳戶：銀行名稱、帳戶名稱、類型與末四碼、餘額與信用額度、最多兩年的交易紀錄（第 2 輪：Kai 先猜「唯讀，所以它應該什麼都看不到吧」n0sb，9ape 開頭「看得到不少」）｜FIN；AN1｜2026-11-05｜9ape, pa3b, e1fc, ewb5, 0haf
c59｜Claude 會加總已連結帳戶的支出並依類別分類（Anthropic 的「這個月錢花到哪」範例）；u94k 是 Kai 的立場句「它就幫你算，比自己記帳輕鬆多了」，「比自己記帳輕鬆」是 Kai 的意見｜FIN；AN1｜2026-11-05｜u94k
c60｜指出重複扣款、非預期費用或一整年逐漸上漲的帳單。第 2 輪改由 Sola 說（Kai 不先知道功能）：Kai 問「所以它會幫我省錢？」h2cs，Sola lc4j「省不省得到錢，公告沒說；但 Anthropic 說，它會指出三種事」（AN1 沒有承諾省錢）｜FIN；AN1｜2026-11-05｜lc4j, h0ue, 5hfj, x1ux；卡片 ok-flag
c61｜官方示範情境中，追問時 Claude 指出一筆會員續約（官方示範，不是實測）｜FIN；AN1｜2026-11-05｜51br
c62｜無廣告或贊助推薦；不提供自家信用卡、貸款或儲蓄帳戶（Anthropic 的說法，旁白開頭「Anthropic 說」）｜FIN；AN1｜2026-11-05｜k7x9
c63｜在 Personal Finance 中樞（Claude 裡專屬的 Personal Finance 區域）內的對話不會用於訓練模型；中樞外分享的內容適用使用者的隱私設定（第 2 輪 s27k「如果你在那個區域外面跟 Claude 聊錢，就看你自己的隱私設定」）｜FIN；AN1｜2026-11-05｜gy3t, s27k
c64｜Claude 的回答可能出錯；建議向銀行核對重要金額｜FIN；AN1｜2026-11-05｜knl6
c65｜並非設計來提供投資建議；使用者可隨時取消連結｜FIN；AN1｜2026-11-05｜4s57, nbtu
c66｜「這不是推薦，也不是理財建議」是節目的聲明；投票題 A／B 是節目的設計｜—｜—｜ekf4, qvote, rwvv, avote

## Sign-off

c67｜「今天最重要的是電費承諾」「最不確定的是夥伴設施算不算」是節目的看法；後者依 c42｜CMP｜2026-11-05｜avgv, 5k2u
c68｜回扣：OpenAI 11/5 的兩件事，測試裡越界低於 1%（c6，OpenAI 自己的測試；旁白加「測試裡」）與電費全部自己付（c27「full cost」；不用「百分之百」，那是 Google 的說法；卡片 so-call 原本「and 100%」也改成「and the full bill」）｜CYB；CMP｜2026-11-05｜a1pc
c69｜「前一件至少有它自己的測試，後一件還沒寫誰來查」依 c6、c39｜CYB；CMP｜2026-11-05｜a18b
c70｜完整整理在 Mokaair，說明欄列五篇站上文章（查核第 2 輪：原本只列主菜的 CMP、WYO，8ss9 說「今天的完整整理」，補上 CYB、RING、FIN，三個網址 2026-11-05 皆 200）｜CMP；WYO｜2026-11-05｜8ss9
c71｜縮圖「Who **checks**?」「OpenAI's power-bill pledge」：依 c39（DC6 標題「Who Enforces It?」）｜CMP；DC6｜2026-11-05｜thumbnail

## 笑點（無事實主張）

給查核代理做笑點檢查：每個笑點前一行的事實、笑點本身、為什麼不算新的事實。沒有新的數字、沒有雙關與諧音、沒有替真人編的話、不打一般人。

- p1pc（Sola）「低於 1%，就像保全公司跟你說，我們的保全很少自己去開別人家的門。」：類比，接 7ivp（c6，OpenAI 自己的測試）。數字是同一個 1%，不是新的；類比說的是「很少」，沒說它在真實世界闖過哪裡。卡片 cy-joke 原本把類比寫成加引號的「"We rarely open the wrong door"」、kicker「Sola's translation」，像 OpenAI 的原話；查核第 1 輪改成不加引號的「A guard that rarely opens the wrong door」，kicker「Sola's analogy」。hlbd（Kai）「很少？」是反應。
- sqcx（Kai）「所以考題是照它自家的事件出的？」與 egt8（Sola）：c8 的白話，查核要確認「自家代理出過的事」沒有把 Hugging Face 事件說得更嚴重（V6 稱為「Hugging Face incident」，OpenAI 的代理入侵了 Hugging Face）。
- gag1／gag2／gag3（Kai）「所以我要不要換手機？」：固定梗，三次都沒有事實主張。回應 k3x0（c11）是事實；ausc「它要你換的是手指」、ovhc「你要換的是問題」是誇張。
- c7zz（Kai）「戒指上有搖桿？」、ymu3「我手指上要有一台遊戲機？」：反應與誇張。
- cxnc（Sola）「對，科技業先把電腦塞進手機，再塞進手錶，現在連搖桿都裝到你的手指上了。」：誇張，講的是整個產業的走向，不是 Aina 的理由（查核第 1 輪改：原本「手機太大、手錶也太大」接在「對，」後面、卡片 kicker 寫「Sola's translation」，聽起來像在轉述 Aina 的想法；TC5 的 Shankar 說的是手機與筆電為瀏覽時代設計）。卡片改成「Phone, then watch, now your finger」，kicker「Sola's take」。
- creh（Sola）「所以在電視這一關，它最大的勝利，是打敗了一支找不到的遙控器。」：c17 的誇張說法，不是 TechCrunch 的評語；查核第 1 輪限定在「電視這一關」，免得聽成作者覺得戒指一無是處。
- nnqj（Kai）「這不是本來就該這樣嗎？」：反應，沒有事實主張。
- d1gr（Sola）「聽起來像裡面有溜滑梯。」、cm2r（Kai）「我還以為是竹科！」：拿「園區」這個新名字開玩笑，對象是公司命名（第 2 輪：「大學」要懂英文 campus 才好笑，改成中文聽眾熟悉的科學園區；翻譯代理要在地化）。
- 4e7h（Kai）「電池？我手機裡那種？」：Kai 誤會，下一句 a177 立刻更正（c36）。
- an6n（Sola）「這就像室友說電費他出，但這句話沒寫進租約。」：c38 的類比；「室友」是虛構的類比角色，不是真人。zvf0（Kai）「可是至少他說了啊！」是反應。
- 4s28（Kai）「這個管得到！」：反應，接 c45；jn7t 回到事實（第 2 輪：「有牙齒」是英文 has teeth 的直譯，換掉）。
- t2kw（Kai）「這次我被說服一半。」：反應。
- g68h（Kai）「所以是 Claude 在評 Claude 自己？」：接 c54 的揭露（查核第 1 輪改：原本「評自己老闆」暗示 Anthropic 是節目的老闆，不對）。
- y2nr（Kai）「那種會員續約，終於有人提醒了！」：接 51br（c61）。查核第 1 輪改：原本「你那個忘記取消的訂閱，終於被抓到了！」多了來源沒有的「忘記取消」，卡片「That forgotten renewal, found」也像事實；卡片改成「A membership renewal, flagged」。
- fgml（Kai）「每一筆？」：反應，前一行 0haf 已說「最多兩年來的每一筆交易」（c58）。
- 2zrr（Kai）「保全很少開錯門，電費說好自己付，好，兩個我都記住了。」：回扣 p1pc 與 c18，沒有新的事實。

第 2 輪新增（Kai 的猜錯與意見、Sola 的冷面句；都沒有新的事實或數字）：
- 8rwn（Kai）「一個會寫攻擊方法的 AI，我猜它自己也會亂跑。」：猜測，7ivp 用 OpenAI 的測試回答。
- zt4n（Kai）「我猜它是拿來打電動的。」：猜錯，e1uu「不是」更正。
- p94m（Sola）「這個問題，我們留到主菜。」：串場。
- 3fx1（Kai）「聽起來不錯，我已經想簽了。」：反應，沒有人能簽這份承諾，是誇張。
- iwcb（Kai）「等一下你再潑冷水。」：串場。
- 1q07（Kai）「我猜，這次電費也是它自己付。」：猜測，yvys 確認是 Google 的說法。
- l3z3（Sola）「那是它說要投資的錢，電費誰付，是另一個問題。」：區分 170 億美元投資與電費，見 c32（查核第 2 輪改：原句說 170 億「不是它要付的電費」，來源沒拆這筆錢）。
- cw7t（Kai）「那地方大概只拿到噪音吧。」：猜錯，tlbb 用 Google 的說法更正；笑的是專案，不是居民。
- q2t7（Sola）「這等於自己出題，自己改考卷。」：比喻 Google 一則全部是自述（c43），沒有說 Google 的說法是錯的。
- 6965（Kai）「所以台灣的電費，也會跟著降？」：想歪，gb74 立刻說沒人這樣說。
- 0cu3（Kai）「第一件，我賭會吵很久。」：Kai 的意見，不是預測的事實。
- n0sb（Kai）「唯讀，所以它應該什麼都看不到吧？」：猜錯，9ape 更正。
- h2cs（Kai）「所以它會幫我省錢？」：問句，lc4j 說公告沒說。

## 我懷疑但沒動的事

- 「低於 1%」與「約 5%」、Critical 分級都是 OpenAI 自己的說法（V6），旁白每次都說是 OpenAI 自己的測試。
- 「投票兩天後」：DC6 說「兩天後」；選舉日是 11/3，承諾是週四 11/5。
- 回扣句（a1pc）說「電費全部自己付」：OpenAI 寫的是「full cost」，Google 才寫 100%，所以沒有用「百分之百」。
- Google 一則全部是自述；稅收、排放與工作機會還沒有獨立資料。

## 沒有放進來的

- GPT-6 Cyber 的 ExploitGym 分數、GPT-6 Astra、Firefox 81 個漏洞、模型可能「知道自己在考試」（初稿有，Monologue 太長，刪了）、Fouad Matin 的「over 99 percent」引句（同上）。
- Aina 的 499 美元、Mirage、其他智慧戒指、550 萬美元募資。
- Google 的合作夥伴名單（Tallgrass、Black Hills、AEP、Related Digital、Bloom Energy）、接近 1 吉瓦、FEED 研究、20 年經驗。
- Personal Finance 的示範金額、Plaid 的名稱（旁白不唸；Claude 不會看到銀行密碼一事也沒放，免得名字太多）、APR 的解釋。

## 進度

- 第 2 輪（盲讀的清楚度修改，保留查核第 1 輪的所有改動）：75 個場景、176 句；`lint` 0 錯誤（剩兩條開場濃縮的警告）；估 14.2 分鐘，最長的畫面狀態估 12.9 秒（mc-goog-chk、ok-disc、ring-what）。
- 第 1 輪：68 個場景、163 句；估 12.8 分鐘。
- 句子完整性檢查（站主 2026-11-05 的規矩）0 行。
- 新加的發音字典詞：Cyber、Aina、Finance、Firefox（null，已在 bf8086a8c 提交；Firefox 最後沒在旁白用到）。
- 查核第 2 輪（2026-11-05）：見 verify-2.md；lint 0 錯誤、估 14.3 分鐘、176 句，最長畫面狀態 12.9 秒。
- 原待做（前半已由查核第 2 輪完成）：第 2 輪改動另派查核代理再對一次（c1a、c20、c21a、c24、c26、c32、c33、c45、c48、c50、c60 與笑點的第 2 輪新增）；Whisper 第二意見與試聽。
