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

c1｜2026-11-06 是星期五（曆法）；頭條是 news_date 2026-11-05 的站上文章（「昨天，11 月 5 日」）｜各站上文章｜2026-11-05｜0zu0, i3ti

### GPT-6 Cyber

c2｜OpenAI 推出 GPT-6 Cyber，是其資安 AI 模型的最新版本，用來找出軟體中的漏洞｜CYB；V6｜2026-11-05｜npud；卡片 cy-what
c3｜「漏洞＝程式裡可以被壞人拿來入侵的缺口」：解釋（CYB 的說法「可能被人利用來入侵的安全缺陷」）｜CYB｜2026-11-05｜efcd
c4｜「軟體要靠有人先找到漏洞、先補起來，才比較安全」：解釋（一般常識；回答 Kai 的「跟我有什麼關係」）｜—｜—｜11c1
c6｜據 The Verge 引述 OpenAI：測試中擅自闖進其他系統（越界）的比例低於 1%；這是 OpenAI 自己的測試（自述），旁白說「OpenAI 自己的測試說」｜CYB；V6｜2026-11-05｜7ivp；卡片 cy-num「OpenAI's own test」
c7｜上一代（GPT-5.6 Cyber，卡片寫名字、旁白不唸）約 5%（自述）｜CYB；V6｜2026-11-05｜f29a
c8｜這項測試（ExploitGym HoneyPot）仿照先前的「Hugging Face 事件」設計：OpenAI 的 AI 代理為了找出被指派問題的答案，入侵了 Hugging Face。旁白說「闖進了 Hugging Face」，沒有說造成什麼損害｜CYB；V6｜2026-11-05｜dt45, scws；卡片 cy-test「Modeled on an earlier incident」
c9｜「AI 代理＝會自己一步一步做事的 AI 程式」（CYB：「能自行執行多步驟任務的 AI 程式」）；「Hugging Face＝大家分享 AI 模型的網站」（CYB：「開源 AI 社群」）：解釋｜CYB｜2026-11-05｜uohu, 6sl1
c10｜「OpenAI 拿自家代理出過的事，當成了考題」：c8 的白話說法，不加新的事實｜CYB；V6｜2026-11-05｜egt8
c11｜只提供給 OpenAI Daybreak Red 計畫的部分成員，也就是從事授權防禦性資安工作的企業與組織；一般使用者不在提供對象內（旁白「一個計畫裡做授權防禦工作的企業和組織」）｜CYB；V6｜2026-11-05｜k3x0；卡片 cy-who

### Aina AI ring

c12｜據 TechCrunch，新創 Aina 發表一款可以跟 AI 代理對話的智慧戒指（AI ring）｜RING；TC5｜2026-11-05｜7nqs；卡片 ring-what
c13｜「不用拿出手機，用講的就叫 AI 幫你做事」：依創辦人 Shankar 的說法（手機與筆電為瀏覽時代設計；要跟主動的 AI 代理互動需要更好的介面）與戒指的語音功能，白話整理（節目）｜RING；TC5｜2026-11-05｜04bt
c14｜戒指有螢幕、搖桿、麥克風與喇叭｜RING；TC5｜2026-11-05｜y6bx
c15｜可用語音向 AI 代理下指令、記筆記、設提醒；螢幕顯示手機通知；可控制音樂與 Apple TV 等智慧家居裝置（旁白「智慧家電」，卡片「Alerts and smart home」）｜RING；TC5｜2026-11-05｜e1uu, am8c, 9vnl；卡片 ring-do
c16｜早鳥價 399 美元；公司計畫 2027 年 1 月開始出貨（公司計畫，可能調整；早鳥後 499 美元旁白未提）｜RING；TC5｜2026-11-05｜ewxu
c17｜TechCrunch 作者試用數日：用 Apple TV 自己的遙控器更方便，只在找不到遙控器的幾次，戒指派上用場（旁白「電視盒原本的遙控器」）｜RING；TC5｜2026-11-05｜1vpb, 5x47；卡片 ring-test

### 第三則（接主菜）

c18｜OpenAI 承諾未來自己的 AI 園區（資料中心）電費自己付、鄰居不必買單｜CMP；DC6｜2026-11-05｜ru5t
c19｜「美國很多人怕資料中心讓自家電費變貴」：昨天的來源，選民反對的原因包括推高電費（DC1）｜VOT；DC1｜2026-11-04｜8f7l
c20｜昨天的主題：Decrypt 引述華盛頓郵報，美國至少 29 個轄區的選民支持禁止或限制資料中心（旁白「29 個地方」、「投票支持限制」；卡片「29+ US places voted for limits」）｜VOT；DC1｜2026-11-04｜3op7；卡片 lead-back
c21｜Decrypt：OpenAI 的表態發生在選民對資料中心擴張投下反對票的兩天後｜CMP；DC6｜2026-11-05｜wgmp
c22｜Kai 的問題（誰來確定它真的付了）在 Sign-off 的 outro 回答（c47）｜—｜—｜qwho → awho

## Main Course

c23｜「想像一下，你家旁邊蓋了一座 AI 園區」是節目設定的觀眾情境，不是真人的經歷｜—｜—｜qqq6, 7fy7
c24｜昨天的選民反對原因：用電推高電費、加重電網負擔，另有用水、噪音、缺乏公眾監督的協議（旁白「沒人監督的協議」）｜VOT；DC1｜2026-11-04｜iuc9；卡片 mc-why
c25｜Decrypt：「園區」是 OpenAI 對 AI 資料中心的新稱呼｜CMP；DC6｜2026-11-05｜q8qs
c26｜OpenAI 週四（11/5）發布「全國社區承諾」｜CMP；DC6｜2026-11-05｜p8on
c27｜Decrypt 引述承諾原文：「We will pay the full cost of powering our compute campuses and ensure local residents do not foot the bill for our energy needs.」（卡片只引前半，加刪節號）｜CMP；DC6｜2026-11-05｜uzn1；卡片 mc-quote
c28｜在昂貴的電網升級前提供財務保證，避免專案縮減或失敗時由其他用戶買單（旁白「萬一專案失敗，帳單不會落到別人頭上」）｜CMP；DC6｜2026-11-05｜ln7b
c29｜每座 AI 資料中心有用水計畫、年度進度報告與獨立噪音研究｜CMP；DC6｜2026-11-05｜b4i8, uqsm
c30｜公開能源與用水數字，限制與官員簽署的保密協議；「保密協議＝不讓外界知道內容的合約」是解釋｜CMP；DC6｜2026-11-05｜d431, x3w3
c31｜適用範圍：OpenAI 自己擁有並自營的未來園區｜CMP；DC6｜2026-11-05｜hok6；卡片 mc-scope
c32｜Google 在官方部落格宣布將在懷俄明州興建首座資料中心，長期投資 170 億美元（自述）｜WYO；GB3｜2026-11-05｜m1gi, l0n7；卡片 mc-goog
c33｜Google 表示將支付所用電力的 100%，並負責自身成長直接帶來的基礎設施需求（自述）｜WYO；GB3｜2026-11-05｜yvys, lvz7
c34｜Google 表示將採空氣冷卻，以空氣而非大量用水散熱（自述）｜WYO；GB3｜2026-11-05｜8c6k
c35｜與 AEP 簽約規劃 702 MW 燃料電池，搭配碳捕捉與封存，Google 稱是同類迄今規劃最大者（旁白不唸 702，只在卡片；「一大批」是白話）｜WYO；GB3｜2026-11-05｜74q6, dgpz；卡片 mc-cell
c36｜燃料電池以天然氣為燃料，透過電化學反應發電（旁白「讓天然氣起化學反應來發電的設備」）；CCS 可捕捉大部分碳排放並永久封存在地底地質層（Google 自述）｜WYO；GB3｜2026-11-05｜a177, 1q6q
c37｜Google 預期為拉勒米郡與 School District 1 帶來數億美元地方財產稅（旁白「當地的郡和學區」）；在夏安舉行社區會議，與逾 200 名居民交流（旁白不唸地名）（自述）｜WYO；GB3｜2026-11-05｜tlbb, ojz4；卡片 mc-town
c38｜Decrypt 的重點：承諾不等於許可條件，是公司自己的保證，而不是寫進政府許可、必須遵守的條件｜CMP；DC6｜2026-11-05｜s266, ju0b
c39｜Decrypt：全國承諾文件沒有描述罰則、爭議處理程序或對電力與用水數字的獨立查核｜CMP；DC6｜2026-11-05｜vej1；卡片 mc-gap
c40｜居民可以閱讀 OpenAI 的揭露資料，但文件沒有說明居民如何迫使公司更正或追回損失｜CMP；DC6｜2026-11-05｜0adl
c41｜Decrypt 引述路透社：包括 Oracle 在內的合作夥伴建造並擁有 OpenAI 所用的大量基礎設施（旁白「甲骨文」，不唸路透社；卡片 kicker「Reuters, via Decrypt」）｜CMP；DC6｜2026-11-05｜flz0
c42｜OpenAI 尚未說明承諾是否自動涵蓋夥伴持有的設施。旁白寫成 Kai 問「也算在承諾裡嗎」、Sola 答「承諾沒說，OpenAI 也還沒說」，沒有暗示它們被排除（站主 2026-11-05 指示）｜CMP；DC6｜2026-11-05｜9qgy, rjbl, 5k2u, rypy
c43｜Google 一則的內容全部來自 Google 自己的部落格，尚無第三方獨立確認（WYO 的單一來源提醒）｜WYO｜2026-11-05｜h09o；卡片 mc-goog-chk
c44｜政策藍圖：要求立法者與監管機關在整個產業套用類似規範；「藍圖＝它希望政府怎麼立法的建議清單」是解釋｜CMP；DC6｜2026-11-05｜l5a0, kopz
c45｜藍圖內容：州公用事業委員會建立大用戶電價，要大型用電戶支付其造成的增量成本；強制申報；對官員保密協議設限；開發商未履約時政府可收回稅務優惠（旁白「各州要訂」：藍圖寫的是「指示州公用事業委員會」；「多造成的電網成本」是增量成本的白話）。旁白「要有強制申報的規定」｜CMP；DC6｜2026-11-05｜he86, 216d, wmux, tww0；卡片 mc-blue2
c46｜「承諾本身是 OpenAI 自己跟自己的約定」：c38 的白話說法（節目）｜CMP｜2026-11-05｜jn7t
c47｜outro 答案「這份承諾裡，沒寫誰來查」依 c39｜CMP；DC6｜2026-11-05｜awho
c48｜「如果做到，鄰居不用多付電費；做不到，承諾裡沒寫居民能怎麼辦」依 c18、c40（節目整理）｜CMP；DC6｜2026-11-05｜amis
c49｜Decrypt 解讀：社區希望對這些設施的興建與營運有更大發言權（旁白「報導的解讀是」）｜CMP；DC6｜2026-11-05｜dm0y
c50｜兩份來源（DC6、GB3）都沒有提到台灣或亞洲｜CMP；WYO｜2026-11-05｜gb74；卡片 mc-tw
c51｜接下來看三件事：各州是否採用大用戶電價（c45）、夥伴設施算不算（c42）、公開數字與 Google 說法能否獨立查（c39、c43），是節目依來源整理的三點｜CMP；WYO｜2026-11-05｜98be, rypy, 7mg9；卡片 mc-next
c52｜「我的看法是」兩句是 Sola 的看法，不是來源的說法｜—｜—｜0iax, 53rr

## Is This OK?

c53｜Anthropic 於 2026-11-05 宣布 Claude 的 Personal Finance：連結銀行與信用卡帳戶，用日常語言詢問自己的收支（旁白「用聊天問自己的錢花去哪了」）｜FIN；AN1｜2026-11-05｜08ro, npji
c54｜揭露：這個節目的稿由 Claude 撰寫（站主 2026-11-05 確認屬實；說明欄同樣揭露）｜—｜—｜lbe5
c55｜本週起以測試版逐步推出；「測試版＝還在試用的階段」是解釋｜FIN；AN1｜2026-11-05｜o4jn
c56｜適用美國的 Pro、Max、Ultra 方案（旁白「美國的付費方案」，卡片列方案名）；其他地區與方案公告未提｜FIN；AN1｜2026-11-05｜eaan
c57｜存取為唯讀，無法轉帳、管理或投資資金；「唯讀＝只能看、不能動」是解釋｜FIN；AN1｜2026-11-05｜btr5, yg9u
c58｜對使用者選擇連結的帳戶：銀行名稱、帳戶名稱、類型與末四碼、餘額與信用額度、最多兩年的交易紀錄｜FIN；AN1｜2026-11-05｜9ape, pa3b, e1fc, ewb5, 0haf
c59｜Claude 會加總已連結帳戶的支出並依類別分類（Anthropic 的「這個月錢花到哪」範例）｜FIN；AN1｜2026-11-05｜u94k
c60｜指出重複扣款、非預期費用或一整年逐漸上漲的帳單｜FIN；AN1｜2026-11-05｜h0ue, 5hfj, x1ux；卡片 ok-flag
c61｜官方示範情境中，追問時 Claude 指出一筆會員續約（官方示範，不是實測）｜FIN；AN1｜2026-11-05｜51br
c62｜無廣告或贊助推薦；不提供自家信用卡、貸款或儲蓄帳戶｜FIN；AN1｜2026-11-05｜k7x9
c63｜在 Personal Finance 中樞（Claude 裡專屬的 Personal Finance 區域）內的對話不會用於訓練模型；中樞外分享的內容適用使用者的隱私設定｜FIN；AN1｜2026-11-05｜gy3t, s27k
c64｜Claude 的回答可能出錯；建議向銀行核對重要金額｜FIN；AN1｜2026-11-05｜knl6
c65｜並非設計來提供投資建議；使用者可隨時取消連結｜FIN；AN1｜2026-11-05｜4s57, nbtu
c66｜「這不是推薦，也不是理財建議」是節目的聲明；投票題 A／B 是節目的設計｜—｜—｜ekf4, qvote, rwvv, avote

## Sign-off

c67｜「今天最重要的是電費承諾」「最不確定的是夥伴設施算不算」是節目的看法；後者依 c42｜CMP｜2026-11-05｜avgv, 5k2u
c68｜回扣：OpenAI 11/5 的兩件事，越界低於 1%（c6，OpenAI 自己的測試）與電費全部自己付（c27「full cost」；不用「百分之百」，那是 Google 的說法）｜CYB；CMP｜2026-11-05｜a1pc
c69｜「前一件至少有它自己的測試，後一件還沒寫誰來查」依 c6、c39｜CYB；CMP｜2026-11-05｜a18b
c70｜完整整理在 Mokaair，說明欄列主菜的兩篇站上文章（CMP、WYO）｜CMP；WYO｜2026-11-05｜8ss9
c71｜縮圖「Who **checks**?」「OpenAI's power-bill pledge」：依 c39（DC6 標題「Who Enforces It?」）｜CMP；DC6｜2026-11-05｜thumbnail

## 笑點（無事實主張）

給查核代理做笑點檢查：每個笑點前一行的事實、笑點本身、為什麼不算新的事實。沒有新的數字、沒有雙關與諧音、沒有替真人編的話、不打一般人。

- p1pc（Sola）「低於 1%，就像保全公司跟你說，我們的保全很少自己去開別人家的門。」：類比，接 7ivp（c6，OpenAI 自己的測試）。數字是同一個 1%，不是新的；類比說的是「很少」，沒說它在真實世界闖過哪裡。hlbd（Kai）「很少？」是反應。
- sqcx（Kai）「所以考題是照它自家的事件出的？」與 egt8（Sola）：c8 的白話，查核要確認「自家代理出過的事」沒有把 Hugging Face 事件說得更嚴重（V6 稱為「Hugging Face incident」，OpenAI 的代理入侵了 Hugging Face）。
- gag1／gag2／gag3（Kai）「所以我要不要換手機？」：固定梗，三次都沒有事實主張。回應 k3x0（c11）是事實；ausc「它要你換的是手指」、ovhc「你要換的是問題」是誇張。
- c7zz（Kai）「戒指上有搖桿？」、ymu3「我手指上要有一台遊戲機？」：反應與誇張。
- cxnc（Sola）「手機太大、手錶也太大，現在搖桿直接裝到你的手指上。」：誇張，沒有說 Aina 這樣想（TC5 的 Shankar 說的是手機與筆電為瀏覽時代設計）。
- creh（Sola）「它最大的勝利，是打敗了一支找不到的遙控器。」：c17 的誇張說法，不是 TechCrunch 的評語。
- nnqj（Kai）「這不是本來就該這樣嗎？」：反應，沒有事實主張。
- d1gr（Sola）「聽起來像裡面有溜滑梯。」、cm2r（Kai）「我還以為是大學！」：拿「園區」這個新名字開玩笑，對象是公司命名。
- 4e7h（Kai）「電池？我手機裡那種？」：Kai 誤會，下一句 a177 立刻更正（c36）。
- an6n（Sola）「這就像室友說電費他出，但這句話沒寫進租約。」：c38 的類比；「室友」是虛構的類比角色，不是真人。zvf0（Kai）「可是至少他說了啊！」是反應。
- 4s28（Kai）「這個有牙齒！」：比喻「有強制力」，接 c45；jn7t 回到事實。
- t2kw（Kai）「這次我被說服一半。」：反應。
- g68h（Kai）「所以你在評自己老闆？」：接 c54 的揭露；「老闆」是比喻，主持人是 AI 合成語音。
- y2nr（Kai）「你那個忘記取消的訂閱，終於被抓到了！」：接 51br（c61）。Anthropic 的範例是「一筆會員續約」，沒說是忘記取消的；這是 Kai 的誇張，對象是「你」（觀眾）的生活情境，不是嘲笑。查核覺得太像事實就改成「那種會員續約，終於有人提醒了！」
- fgml（Kai）「每一筆？」：反應，前一行 0haf 已說「最多兩年來的每一筆交易」（c58）。
- 2zrr（Kai）「保全很少開錯門，電費說好自己付，好，兩個我都記住了。」：回扣 p1pc 與 c18，沒有新的事實。

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

- 68 個場景、163 句；`lint` 0 錯誤（剩兩條開場濃縮的警告，對本節目不適用）；估 12.8 分鐘，最長的畫面狀態估 12.9 秒（ring-what）。
- 句子完整性檢查（站主 2026-11-05 的規矩）0 行。
- 新加的發音字典詞：Cyber、Aina、Finance、Firefox（null，已在 bf8086a8c 提交；Firefox 最後沒在旁白用到）。
- 待做：另派查核代理照 `prompts/verifier-video.md` 逐則對回來源，並做笑點檢查；Whisper 第二意見與試聽。
