# daily-ai-20261106 查核第 1 輪

查核日 2026-11-05。查核代理不是撰稿人。每一條旁白（`text`，Sola 與 Kai 兩位都查；本片沒有 `say`）、每張卡片的 `data`（含 `kicker`、`source`、`key`、`keys`）、縮圖、`youtube.title`、`description`、`tags` 都抽出來逐條對照（清單在工作區 `_tools/dump.txt`）。
來源：站上 5 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，1.2 秒一篇，全部 HTTP 200、`status: published`、news_date 2026-11-05），加上 `video.json` `sources` 的 6 個原始來源，2026-11-05 全部用 `Mokaair-editorial/1.0` UA 以 curl 重新打開，去掉 `<!-- -->` 後讀全文。web search 0 次。
撰稿人只用了站上文章的轉述；這一輪每個數字、引句都對回原文。這是脫口秀版的第一次查核，另有一節〈笑點檢查〉與一節〈清楚度檢查〉（站主 2026-11-06 的「每句話都要有頭有尾」）。

## 來源代號

站上文章（全部 200，published，news_date 2026-11-05）：

| 代號 | slug |
| --- | --- |
| CMP | ai-news-openai-community-compact-20261105 |
| WYO | ai-news-google-wyoming-data-center-20261105 |
| CYB | ai-news-openai-gpt-6-cyber-20261105 |
| RING | ai-news-aina-ai-ring-20261105 |
| FIN | ai-news-claude-personal-finance-20261105 |

原始來源（2026-11-05 重開，全部 HTTP 200，沒有轉址）：

| 代號 | URL（頁面上的日期） |
| --- | --- |
| DC6 | https://decrypt.co/382674/openai-promises-foot-ai-power-bill-after-voter-revolt （2026-11-05T21:36） |
| GB3 | https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/wyoming-data-center/ （2026-11-05） |
| V6 | https://www.theverge.com/ai-artificial-intelligence/1027599/openai-gpt-6-cyber-launch （Emma Roth，2026-11-05T17:00Z） |
| TC5 | https://techcrunch.com/2026/11/05/ainas-smart-ring-has-a-screen-a-joystick-and-a-mic-so-you-can-talk-to-ai-agents/ （6:42 AM PST, November 5, 2026） |
| AN1 | https://claude.com/resources/articles/introducing-personal-finance-in-claude （2026-11-05） |
| DC1 | https://decrypt.co/382556/us-voters-back-ai-data-center-restrictions （2026-11-04T18:46；昨天查過，本輪重開；`checked_on` 改成 2026-11-05） |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 今天是 11 月 6 日星期五；昨天 11 月 5 日的頭條 | 0zu0、i3ti；intro、mo-hi | 曆法；站上 5 篇 | 200 | CONFIRMED（2026-11-06 是星期五；news_date 皆 2026-11-05） | |
| 2 | OpenAI 推出新 AI GPT-6 Cyber，專門找軟體漏洞 | npud；cy-what | V6 | 200 | CONFIRMED（「the latest version of its cybersecurity AI model, which it says is better at finding vulnerabilities」） | |
| 3 | 漏洞＝可被壞人拿來入侵的缺口；軟體要先找到漏洞補起來才安全 | efcd、11c1；cy-why | CYB | 200 | CONFIRMED（解釋，一般常識） | |
| 4 | 據 The Verge，OpenAI 自己的測試：擅自闖進其他系統低於 1%；上一代約 5% | 7ivp、f29a；cy-num | V6 | 200 | CONFIRMED（「during testing, GPT-6 Cyber went out of bounds less than 1 percent of the time, down from around 5 percent with GPT-5.6 Cyber」；「OpenAI says」，旁白與卡片都標 OpenAI 自己的測試） | |
| 5 | 測試照之前一次真實事件設計；OpenAI 的 AI 代理為了找答案闖進 Hugging Face | dt45、scws；cy-test | V6 | 200 | CHANGED（原文「OpenAI's AI agents breached the open-source AI community」，複數） | 「OpenAI 的一個 AI 代理」→「OpenAI 的 AI 代理」 |
| 6 | AI 代理＝自己一步步做事的 AI 程式；Hugging Face＝分享 AI 模型的網站 | uohu、6sl1；cy-terms | CYB、V6 | 200 | CONFIRMED（解釋；V6「open-source AI community」） | |
| 7 | OpenAI 拿自家代理出過的事當考題 | sqcx、egt8；cy-test2 | V6 | 200 | CONFIRMED（見笑點檢查 #2） | |
| 8 | 不給一般人，只給一個計畫裡做授權防禦工作的企業和組織 | k3x0；cy-who | V6 | 200 | CHANGED（卡片）（原文「rolling out to select members of OpenAI's Daybreak Red program … for "authorized defensive cybersecurity work"」；旁白對，卡片的「Vetted」原文沒有） | 卡片「Vetted defenders only」→「Select defenders only」（text 與 key） |
| 9 | 據 TechCrunch，新創 Aina 做了能跟 AI 說話的戒指；不用拿手機，用講的叫 AI 做事 | 7nqs、04bt；ring-what | TC5 | 200 | CONFIRMED（「a smart ring … so that you can talk to your agents and take notes」；04bt 是 Shankar 說法的白話） | |
| 10 | 螢幕、搖桿、麥克風、喇叭 | y6bx；ring-parts | TC5 | 200 | CONFIRMED | |
| 11 | 指揮 AI 代理；語音記筆記、設提醒；看手機通知、控制智慧家電 | e1uu、am8c、9vnl；ring-do | TC5 | 200 | CONFIRMED（「send a prompt to agents, set reminders」「notifications from your phone」「smart home devices like Apple TV」） | |
| 12 | 早鳥價 399 美元，公司計畫 2027 年 1 月出貨 | ewxu；ring-do | TC5 | 200 | CONFIRMED（「early-bird pricing of $399 … plans to start shipping the device in January 2027」） | |
| 13 | 作者試了幾天，電視盒原本的遙控器比較方便；只有找不到遙控器的那幾次戒指才派上用場 | 1vpb、5x47；ring-test | TC5 | 200 | CHANGED（原文「It's easier to use Apple TV's remote itself, but the Aina ring proved useful the couple times I couldn't find the remote」，只講電視；作者同時說它像智慧手錶，能回通知、看會議、叫 Uber。「只有……才派上用場」沒有限定，聽起來像戒指整體只在那幾次有用） | 「只有遙控器找不到的那幾次，這枚戒指才派上用場。」→「控制電視時，只有遙控器找不到的那幾次，戒指才派上用場。」 |
| 14 | OpenAI 說以後自己的 AI 資料中心電費自己付 | ru5t；lead-pledge | DC6 | 200 | CONFIRMED（「neighbors of its future AI campuses won't foot the bill」；只涵蓋自有自營，hok6 有講） | 卡片 text 原本加引號「"We'll pay our own power bill"」，像 OpenAI 原話（原文是「We will pay the full cost of powering our compute campuses」）→「Pledge: paying its own power bill」；key「OpenAI: we pay the bill」→「OpenAI pledges to pay」（引號與出處，不是事實改動） |
| 15 | 美國很多人怕資料中心讓電費變貴 | 8f7l；lead-pledge | DC1 | 200 | CHANGED（措辭）（DC1 有「local fights over utility bills」；原句「因為……」接在 OpenAI 承諾後面，讀成 OpenAI 的動機，來源沒有這樣說） | 「因為美國很多人怕資料中心讓自家的電費變貴。」→「很多美國人怕這些放滿電腦的大樓，讓自家的電費變貴。」（也順便解釋資料中心，見清楚度檢查） |
| 16 | 昨天講到：美國至少 29 個地方選民投票支持限制資料中心 | 3op7；lead-back | DC1 | 200 | CONFIRMED（「Voters in at least 29 U.S. jurisdictions backed bans or restrictions」） | |
| 17 | 投票兩天後 OpenAI 做了這個承諾 | wgmp；lead-back | DC6 | 200 | CONFIRMED（「two days after voters dealt data center expansion a blow at the polls」） | |
| 18 | 卡片「"We'll pay." Who checks?」 | lead-q | DC6 | 200 | CHANGED（卡片）（加引號的「We'll pay.」不是原話） | →「It says it pays. / Who checks?」 |
| 19 | 想像你家旁邊蓋了一座 AI 園區 | qqq6；mc-scene | — | — | OUT OF SCOPE（節目情境）；用詞改了，見清楚度檢查 | |
| 20 | 昨天的選民反對，就是因為電費、電網、用水、噪音、沒人監督的協議 | iuc9；mc-why | DC1 | 200 | CHANGED（措辭）（DC1：「local fights over utility bills and grid capacity, while opponents also raise concerns about water use, noise and deals struck without public scrutiny」，是擔心的事，不是唯一原因；「沒人監督」比「沒有公眾監督」強） | →「對，昨天的選民擔心的，是電費、電網、用水、噪音，還有缺少公眾監督的協議。」 |
| 21 | OpenAI 把資料中心叫做園區 | q8qs；mc-name | DC6 | 200 | CONFIRMED（「campuses (a fancy rebranding for the term AI data centers)」） | |
| 22 | OpenAI 週四發布「全國社區承諾」；據 Decrypt 付園區供電全部成本、不讓居民買單 | p8on、uzn1；mc-quote | DC6 | 200 | CONFIRMED（逐字引句在卡片，前半加刪節號；11/5 是週四） | |
| 23 | 電網升級前財務保證；用水計畫、獨立噪音研究；年度進度報告；公開用電用水數字；限制與官員簽保密協議 | ln7b、b4i8、uqsm、d431、x3w3；mc-more | DC6 | 200 | CONFIRMED（「financial assurances before costly grid upgrades, so other customers aren't left paying if projects shrink or fail」「water plan, annual progress reports and independent noise studies」「public energy and water figures and limits on secrecy agreements with officials」） | |
| 24 | 範圍：OpenAI 自己擁有、自己營運的未來園區 | hok6；mc-scope | DC6 | 200 | CONFIRMED（「covers future campuses … OpenAI both owns and operates」） | |
| 25 | 說要自己付的不只 OpenAI 一家；Google 同一天宣布在懷俄明州蓋當地第一座資料中心；長期投資 170 億美元 | p7f3、m1gi、l0n7、s83t；mc-goog | GB3 | 200 | CHANGED（原文「our first data center in the state of Wyoming」＝Google 在該州的第一座，「當地第一座」可聽成懷俄明州第一座資料中心） | 「蓋當地第一座資料中心」→「蓋它在那裡的第一座資料中心」 |
| 26 | Google 說付自己用電的百分之百；負責成長直接帶來的基礎建設；散熱用空氣不用大量的水 | yvys、lvz7、8c6k；mc-goog-pay | GB3 | 200 | CONFIRMED（「We will pay for 100% of the power we use … cover the infrastructure needs directly driven by our growth」「air-cooled to minimize strain on local water resources」） | |
| 27 | 電有一部分來自一大批燃料電池；Google 說同類規劃最大；卡片 702 MW | 74q6、dgpz；mc-cell | GB3 | 200 | CONFIRMED（「702 MW fuel cell development with carbon capture and storage (CCS) — the largest planned development of its kind to date」；另有燃氣發電機，所以「一部分」對） | |
| 28 | 燃料電池是讓天然氣起化學反應發電的設備；碳排放大部分抓起來封進地底 | a177、1q6q；mc-cell2 | GB3 | 200 | CHANGED（措辭）（原文「Fuel cells efficiently convert fuel, in this case natural gas」：燃料電池不一定用天然氣；1q6q 是 Google 的說法，原句沒掛名） | a177「燃料電池是……」→「這裡的燃料電池，是……」；1q6q 開頭加「Google 說，」 |
| 29 | Google 預期替當地的郡和學區帶來數億美元財產稅；開社區會議，跟兩百多位居民交流 | tlbb、ojz4；mc-town | GB3 | 200 | CONFIRMED（「hundreds of millions of dollars in local property taxes for Laramie County and School District 1」「met with more than 200 residents in Laramie County」，會議在夏安） | |
| 30 | 承諾是公司自己的保證，沒寫進政府許可，不是一定要遵守的條件 | s266、ju0b；mc-sola | DC6 | 200 | CONFIRMED（小標「A pledge is not a permit condition」） | |
| 31 | 承諾沒寫罰則、爭議處理、誰來獨立查電力和用水數字 | vej1；mc-gap | DC6 | 200 | CONFIRMED（「does not describe penalties for noncompliance, a dispute process or independent verification of electricity and water figures」） | |
| 32 | 居民看得到資料，但沒說怎麼逼它更正或拿回損失 | 0adl；mc-resid | DC6 | 200 | CONFIRMED（「how they could compel corrections or recover losses」） | |
| 33 | OpenAI 用的很多設施是甲骨文這些夥伴蓋的、擁有的；承諾沒說、OpenAI 也沒說會不會自動涵蓋 | flz0、9qgy、rjbl；mc-partner* | DC6 | 200 | CONFIRMED（「Partners including Oracle build and own much of the infrastructure reserved for OpenAI, Reuters reported. The company has not said its national compact automatically covers those」；路透社只在卡片 kicker） | |
| 34 | Google 的內容全部來自它自己的部落格，沒有第三方查證 | h09o；mc-goog-chk | GB3、WYO | 200 | CONFIRMED（全部第一人稱公司說法） | |
| 35 | 政策藍圖＝希望政府怎麼立法的建議；要立法者把類似規則套到整個產業 | l5a0、kopz；mc-blue | DC6 | 200 | CONFIRMED（「A separate policy blueprint asks legislators and regulators to apply similar requirements across the industry」） | |
| 36 | 藍圖四點：各州訂大用戶電價（大戶付自己多造成的電網成本）、強制申報、保密協議設限、開發商沒做到可收回稅務優惠 | he86、216d、wmux、tww0；mc-blue2 | DC6 | 200 | CONFIRMED（「direct state public utility commissions to create large-load tariffs that require large electricity consumers to pay the incremental costs they create」「mandatory reporting, narrow limits on officials' NDAs and provisions letting governments reclaim tax breaks when developers miss agreed commitments」） | |
| 37 | 牙齒要政府去裝，承諾是自己跟自己的約定 | jn7t；mc-teeth | DC6 | 200 | CONFIRMED（c38 的白話；小標「The policy blueprint urges enforceable rules, but the company's own national compact specifies no penalties」） | |
| 38 | 做到鄰居不用多付；做不到承諾沒寫居民能怎麼辦 | amis；mc-win | DC6 | 200 | CONFIRMED（節目整理，依 #14、#32） | |
| 39 | 報導的解讀：社區想對興建和營運有更大發言權 | dm0y；mc-say | DC6 | 200 | CONFIRMED（「send a message … that communities want a bigger say in how these facilities are built」） | |
| 40 | 兩份來源都沒提到台灣或亞洲 | gb74；mc-tw | DC6、GB3 | 200 | CONFIRMED（全文沒有；GB3 只有語言選單的「台灣 (中文)」） | |
| 41 | 接下來看三件事 | kmxd、98be、rypy、7mg9；mc-next | DC6、GB3 | 200 | CONFIRMED（節目依來源整理） | |
| 42 | 我的看法：對的方向；沒罰則沒人查只是一句話，寫進許可或電價規則才算數 | 0iax、53rr；mc-view* | brief.md | — | OUT OF SCOPE（觀點，見摘要） | |
| 43 | Anthropic 推出 Claude 新功能 Personal Finance；把銀行帳戶連上，用聊天問錢花去哪 | 08ro、npji；ok-what | AN1 | 200 | CONFIRMED（「securely connect your bank and card accounts and ask in your own words」） | |
| 44 | 讓一家 AI 公司看你的帳戶資料 | 12g5；ok-why | AN1 | 200 | CONFIRMED（辯論的框架；Claude 看得到所連帳戶的資料，見 #48） | |
| 45 | 揭露：這個節目的稿是 Claude 寫的 | lbe5；ok-disc；description | — | — | CONFIRMED（站主 2026-11-05 確認；說明欄同樣揭露） | |
| 46 | 本週開始以測試版推出；只有美國的付費方案；其他地區公告沒提 | o4jn、eaan；ok-who | AN1 | 200 | CHANGED（原文「on the Pro, Max, and Ultra plans in the US」，只列三種方案；「美國的付費方案」把 Team、Enterprise 等方案也包進去，公告沒說） | eaan「只有美國的付費方案用得到，其他地區公告沒提。」→「目前只開放美國的三種付費方案，其他地區和方案，公告沒提。」；卡片 key「US paid plans only」→「Three US paid plans」 |
| 47 | 唯讀，不能轉帳、不能投資 | btr5；ok-who | AN1 | 200 | CONFIRMED（「can't move, manage, or invest your money」） | |
| 48 | 選的帳戶：銀行與帳戶名稱、類型與末四碼、餘額與信用額度、最多兩年交易紀錄 | 9ape、pa3b、e1fc、ewb5、0haf；ok-see | AN1 | 200 | CONFIRMED（逐項對到；0haf「每一筆」＝最多兩年的交易） | |
| 49 | 好幾個銀行 App 變成一個對話；問這個月錢花去哪，幫你分類加總 | tp8n、u94k；ok-kai | AN1 | 200 | CONFIRMED（「no longer means opening every banking app」「adds up your spending across the accounts you connected and sorts it by category」） | |
| 50 | 抓重複扣款、沒想到的手續費、一整年慢慢變貴的帳單 | h0ue、5hfj、x1ux；ok-flag | AN1 | 200 | CONFIRMED（「charges that hit twice, unexpected fees, or a bill that's crept up all year」；卡片 title「per Anthropic」） | |
| 51 | 官方示範裡指出一筆會員續約 | 51br；ok-renew | AN1 | 200 | CONFIRMED（「points to a membership renewal」）；卡片改了，見笑點檢查 #1 | |
| 52 | 沒有廣告和贊助推薦；不賣自己的信用卡或貸款 | k7x9；ok-noads | AN1 | 200 | CHANGED（措辭）（是 Anthropic 的說法，旁白原本沒掛名；原文「doesn't offer credit cards, loans, or savings accounts of its own」） | →「Anthropic 說，這裡沒有廣告和贊助推薦，也不提供自家的信用卡或貸款。」 |
| 53 | 理財區域內的對話不拿去訓練；區域外看隱私設定；回答可能出錯，要跟銀行核對 | gy3t、s27k、knl6；ok-fine | AN1 | 200 | CONFIRMED | |
| 54 | 不是設計來給投資建議；隨時可以取消連結 | 4s57、nbtu；ok-advice | AN1 | 200 | CONFIRMED（「isn't designed to give investment advice」「You can unlink an account anytime」） | |
| 55 | 這不是推薦也不是理財建議；投票 A／B | qvote、rwvv、avote；ok-vote | — | — | OUT OF SCOPE（節目聲明與設計） | |
| 56 | 真心話：最重要是電費承諾；最不確定是夥伴設施算不算，OpenAI 還沒說 | avgv、5k2u；so-take | DC6、brief.md | 200 | CONFIRMED（後半依 #33）／OUT OF SCOPE（觀點） | |
| 57 | OpenAI 昨天說兩件事：擅自闖進別的系統低於 1%、電費全部自己付；卡片「Under 1%, and 100%」 | a1pc；so-call | V6、DC6 | 200 | CHANGED（「低於 1%」是測試結果，回扣句把「測試」拿掉，聽起來像真實世界的紀錄；卡片「100%」是 Google 的說法，OpenAI 寫的是「full cost」，claims.md c68 自己也說旁白不用百分之百） | a1pc「一件是擅自闖進……」→「一件是測試裡擅自闖進……」；卡片「Under 1%, **and 100%**」→「Under 1%, **and the full bill**」，key「Under 1% vs 100%」→「Under 1% vs full bill」 |
| 58 | 前一件至少有它自己的測試，後一件還沒寫誰來查 | a18b；so-call2 | V6、DC6 | 200 | CONFIRMED | |
| 59 | 完整整理在 Mokaair，連結在說明欄 | 8ss9；so-site；description | CMP、WYO | 200 | CONFIRMED（兩個網址 200、published） | |
| 60 | 答案：承諾裡沒寫誰來查 | awho；outro | DC6 | 200 | CONFIRMED；句子改了，見清楚度檢查 | |
| 61 | 標題「OpenAI's power-bill promise」；縮圖「Who checks?」「OpenAI's power-bill pledge」；說明欄揭露；tags | youtube.*、thumbnail | DC6 | 200 | CONFIRMED（DC6 標題「Who Enforces It?」）／OUT OF SCOPE | |
| 62 | 串場與 Kai 的反應句（r6rt、8rwn、hlbd、oqkf、c7zz、zt4n、3fx1、iwcb、qq8a、s83t、1q07、cw7t、ve8l、jqsj、qmis、zvf0、9qgy、j9bf、kbgm、6965、0cu3、t2kw、5o2k、mazm、8w9h、ekf4、lsd0、n0sb、fgml、kb70、k4ii 等） | 各處 | — | — | OUT OF SCOPE（不含新事實；沒有編主持人的私人經驗） | |

## 笑點檢查

逐句看 claims.md〈笑點〉列的每一句，加上卡片上接梗的字。五條標準：暗示錯誤或來源沒有的事實、新的數字、替真人編話、打一般人、雙關或諧音。

| # | 笑點 | 位置 | 判定 | 理由 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- |
| 1 | 「你那個忘記取消的訂閱，終於被抓到了！」（撰稿人不確定的第 1 個） | y2nr；卡片 ok-renew | **改** | AN1 只說 Claude「points to a membership renewal」，沒說是忘記取消的訂閱。這句接在事實句 51br 後面，又配上卡片「That forgotten renewal, found」，聽起來像示範的內容，是來源沒有的事實。「你那個」也是在笑觀眾。 | 旁白照 claims.md 的建議改成「那種會員續約，終於有人提醒了！」；卡片「That forgotten / **renewal, found**」→「A membership renewal, / **flagged**」，key「Forgotten renewals, found」→「A renewal, flagged」 |
| 2 | 「對，OpenAI 拿自家代理出過的事，當成了考題。」（不確定的第 2 個） | egt8、sqcx；cy-test2 | **留** | V6：「ExploitGym HoneyPot, is modeled after the Hugging Face Incident, in which OpenAI's AI agents breached the open-source AI community」。「出過的事」是中性說法，比原文的「breached」還輕，也沒說造成損害，沒有誇大。同一輪把 scws 的「一個 AI 代理」改成跟原文一樣不寫數量（主張表 #5）。 | |
| 3 | 「低於 1%，就像保全公司跟你說，我們的保全很少自己去開別人家的門。」（不確定的第 3 個） | p1pc；卡片 cy-joke；回扣 2zrr | **留旁白，改卡片** | 前一句 7ivp 已經說「OpenAI 自己的測試說」，類比的主詞也是「保全公司跟你說」，聽眾知道這是公司的自我報告，不是真實世界的闖入紀錄；「很少」對的是 1%，沒有新數字。問題在別的地方：(a) 卡片把類比加上引號寫成「"We rarely open the wrong door"」、kicker「Sola's translation」，英文觀眾會看成 OpenAI 的原話；(b) 片尾回扣 a1pc 把「測試」拿掉了，聽起來像真的闖進了別人的系統（主張表 #57）。 | 卡片 →「A guard that rarely / **opens the wrong door**」，kicker「Sola's analogy」；a1pc 加「測試裡」 |
| 4 | 「對，手機太大、手錶也太大，現在搖桿直接裝到你的手指上。」（不確定的第 4 個） | cxnc；卡片 ring-joke | **改** | 不夠清楚是 Sola 的誇張：句子以「對，」接在 Kai 問的「戒指上有搖桿？」後面，前半是「因為 A、B，所以 C」的句型，聽起來像在說 Aina 做這枚戒指的理由；卡片 kicker「Sola's translation」更像在翻譯 Aina 的說法。TC5 的 Shankar 講的是手機與筆電為「瀏覽時代」設計，不是太大，「手錶太大」來源完全沒有。 | →「對，科技業先把電腦塞進手機，再塞進手錶，現在連搖桿都裝到你的手指上了。」（講產業走向，不說成誰的理由，沒有新數字）；卡片「Phones too big? / **Joystick on a finger**」→「Phone, then watch, / **now your finger**」，kicker「Sola's take」 |
| 5 | 「所以它最大的勝利，是打敗了一支找不到的遙控器。」 | creh；ring-joke2 | **改** | 誇張，對象是產品，可以留；但它跟 5x47 一起讓人以為 TechCrunch 覺得戒指只在找不到遙控器時有用。作者其實也寫了看通知、看會議、叫 Uber（主張表 #13）。限定在電視就沒有錯誤的暗示。 | →「所以在電視這一關，它最大的勝利，是打敗了一支找不到的遙控器。」；卡片「It beat」→「TV round: it beat」 |
| 6 | 「所以你在評自己老闆？」 | g68h；ok-disc | **改** | 暗示 Anthropic 是這個節目的老闆。揭露的事實只是「節目稿由 Claude 撰寫」，節目是 Mokaair 的，這是來源沒有的事實。 | →「所以是 Claude 在評 Claude 自己？」 |
| 7 | 「這就像室友說電費他出，但這句話沒寫進租約。」／「可是至少他說了啊！」 | an6n、zvf0；mc-lease | **留** | 類比 DC6「A pledge is not a permit condition」；室友是虛構角色，打的是公司的承諾。卡片引號裡的「I'll pay」是室友說的，kicker 一併改成「Sola's analogy」，跟 cy-joke 一致。 | kicker「Sola's translation」→「Sola's analogy」 |
| 8 | 「聽起來像裡面有溜滑梯。」／「我還以為是大學！」 | d1gr、cm2r；mc-name | **留** | 笑的是公司把資料中心改名叫「園區」（DC6 自己也說「a fancy rebranding」）。「園區」與溜滑梯、大學是聯想，不是諧音。 | |
| 9 | 「這個有牙齒！」／「那些牙齒要政府去裝」 | 4s28、jn7t；mc-teeth | **留** | 比喻有強制力，接 DC6 小標「urges enforceable rules」。不是雙關。翻譯代理要知道「有牙齒」是英文 has teeth 的直譯，中文聽眾第一次聽可能要想一下；jn7t 馬上講白，見「懷疑但沒改」。 | |
| 10 | 「所以我要不要換手機？」×3；「不用，它要你換的是手指」；「你要換的不是手機，是問題」 | gag1、gag2、gag3、ausc、ovhc | **留** | 固定梗，三次都沒有事實主張；回答都是明顯的誇張。 | |
| 11 | 「戒指上有搖桿？」「我手指上要有一台遊戲機？」 | c7zz、ymu3 | **留** | 反應，沒有事實。 | |
| 12 | 「等等，這不是本來就該這樣嗎？」 | nnqj | **留** | 反應，笑的是承諾本身。 | |
| 13 | 「電池？我手機裡那種？」 | 4e7h | **留** | Kai 誤會，a177 立刻更正。 | |
| 14 | 「保全很少開錯門，電費說好自己付，好，兩個我都記住了。」 | 2zrr；so-call2 | **留** | 回扣 p1pc 與 ru5t，沒有新事實；前一句 a18b 已經說「前一件至少有它自己的測試」。 | |
| 15 | 「每一筆？」「170 億美元！」 | fgml、s83t | **留** | 反應，數字都是前一句的。 | |
| 16 | 縮圖「Who **checks**?」 | thumbnail | **留** | DC6 標題「Who Enforces It?」。 | |

笑點總計：16 項，留 10 項，改 6 項（#1、#3 卡片、#4、#5、#6、#7 kicker），刪 0 項。全片沒有雙關或諧音、沒有新的數字、沒有替真人編的引句；修完後沒有打一般人的笑點（#1 原本笑「你」忘記取消訂閱）。

## 清楚度檢查

照 daily-brief.md §一之〇。

- 句子完整性檢查（brief 給的 node 指令）：修改前 0 行，修改後 0 行。每一行都以 。？！ 結尾；Kai 的短反應（「很少？」「每一筆？」「170 億美元！」）回應的事實句都是完整的一句。
- 每則前兩句：
  - GPT-6 Cyber：npud 說發生了什麼，efcd 解釋漏洞，r6rt／11c1 接著說跟你有什麼關係（第 3、4 句）。可以接受：「跟我有什麼關係」由 Kai 明白問出來，在 15 秒內回答。沒改。
  - Aina：7nqs、04bt 符合。
  - 第三則／主菜：ru5t 說發生了什麼；8f7l 原本「因為……」讀成 OpenAI 的動機，改成直接講跟一般人的關係，並在同一句解釋資料中心（見下）。
  - Google：m1gi、l0n7 符合（為什麼重要由 p7f3「不只 OpenAI 一家」先講）。
  - Personal Finance：08ro、npji、12g5 符合。
- 生字第一次出現就解釋：
  - **資料中心**：整集沒有解釋（昨天那集有，但今天的聽眾不一定聽過）。8f7l 改成「很多美國人怕這些放滿電腦的大樓，讓自家的電費變貴。」（依 DC1「These facilities house the chips and servers」）。
  - **AI 園區**：qqq6 在 mc-name 的 q8qs 解釋「園區」之前就用了「AI 園區」。qqq6 改成「AI 資料中心」，卡片「next to a campus」→「next to a data center」；「園區」第一次出現就在 q8qs 的解釋句裡。
  - **燃料電池**：a177 加「這裡的」，不把天然氣說成所有燃料電池的定義。
  - 漏洞、AI 代理、Hugging Face、保密協議、政策藍圖、大用戶電價、測試版、唯讀、理財區域都在第一次出現時解釋；AI 代理與 Hugging Face 的解釋在用到它們的下一句（cy-terms），沒有搬動場景。
- 不往回指：outro 的 awho 原本「答案是，這份承諾裡，沒寫誰來查。」離問題 qwho（Monologue）隔了十分鐘，聽眾不知道是哪個問題的答案。改成「誰來確定 OpenAI 付了電費？承諾裡沒寫。」先把問題重講一次。
- 出處短講：每則一次（據 The Verge、據 TechCrunch、據 Decrypt；Google 與 Anthropic 是官方來源）。路透社只在卡片 kicker。1q6q 與 k7x9 加了「Google 說」「Anthropic 說」，因為那是公司自述，不算出處鏈。
- 一句一件事：沒有一句同時塞兩個數字和兩個名字；a1pc 有兩件事，是回扣句的設計。

畫面狀態：改完後用 lint 的估計時間軸（`tools/video/core/cadence.mjs` 的 `slideStates`）重算，最長 12.9 秒（ring-what、ok-disc），全部 ≤13 秒。第一版的改動讓 outro 14.7 秒、ring-test 14.3 秒、lead-pledge 14.3 秒超過，已縮短 awho、5x47、8f7l。

## 摘要

- 查了 62 條（同一事實在多處出現時合為一條）加 16 項笑點：CONFIRMED 47、CHANGED 11、NOT FOUND 0、OUT OF SCOPE 4（#19、#42、#55、#62；#56、#61 部分）。
- 事實改動 6 處：(1) Hugging Face 事件是 OpenAI 的「AI 代理」（複數），不是「一個」（scws）；(2) Google 是在懷俄明州蓋「它在那裡的」第一座，不是當地第一座（m1gi）；(3) 戒指只在控制電視時輸給遙控器，不是只有那幾次有用（5x47）；(4) Personal Finance 只開放美國三種方案，不是所有付費方案（eaan，卡片 key）；(5) 片尾「低於 1%」補回「測試裡」（a1pc）；(6) 片尾卡片「100%」是 Google 的說法，OpenAI 寫的是 full cost（so-call）。
- 措辭／出處改動：iuc9（選民擔心的事，不是唯一原因；「缺少公眾監督」）、8f7l（拿掉讀成 OpenAI 動機的「因為」）、a177（這裡的燃料電池）、1q6q 加「Google 說」、k7x9 加「Anthropic 說」；卡片 cy-who「Vetted」→「Select」；lead-pledge、lead-q、cy-joke 拿掉像原話的引號。
- 笑點：改 6 項，刪 0 項（見〈笑點檢查〉）。撰稿人的四個疑問：#1 改（忘記取消是新事實）、#2 留（沒有誇大）、#3 旁白留、卡片與片尾回扣改、#4 改（聽起來像 Aina 的理由）。另外改了「評自己老闆」（暗示 Anthropic 是節目的老闆）與「最大的勝利」（限定在電視）。
- 「據報導」：單一媒體的各則都有掛名（據 The Verge／TechCrunch／Decrypt）；公司自述都有標：OpenAI 的 1% 與 5%（「OpenAI 自己的測試」）、Google（「Google 說」「它說」、h09o 明說全部來自它自己的部落格）、Anthropic（ok-flag「per Anthropic」、k7x9 本輪補「Anthropic 說」）、Aina 的出貨（「公司計畫」）。
- 理財：Is This OK? 開頭揭露節目稿由 Claude 撰寫，ekf4、qvote 說不推薦、不是理財建議；沒有價格、報酬或買賣建議。示範金額沒有用。
- 唸出來的日期：11/5 週四（OpenAI 承諾、Google、GPT-6 Cyber、Aina、Anthropic，原文皆 2026-11-05）、「投票兩天後」（DC6）、2027 年 1 月（Aina 出貨），都與原文相符。
- `sources` 6 個網址 2026-11-05 全部 HTTP 200，`checked_on` 全部 2026-11-05（DC1 原本 2026-11-04）。
- 會過期的事實：GPT-6 Cyber 未來數週擴大到所有 Daybreak Red 客戶（V6 2026-11-05）；Aina 2027 年 1 月出貨、早鳥價（TC5 2026-11-05）；Personal Finance 測試版的地區與方案（AN1 2026-11-05）；OpenAI 承諾是否涵蓋夥伴設施（DC6 2026-11-05）；Google 懷俄明州的財產稅與排放（GB3 2026-11-05，未經第三方查證）。
- 觀點：0iax、53rr 以「我的看法是」標明，avgv、5k2u 以「說一句真心話」「我最不確定的」標明，與 brief.md〈站主觀點〉一致（自己付電費是對的方向、沒罰則沒人查只是一句話、寫進許可或電價規則才算數、不確定夥伴設施算不算）。沒有不一致。
- 聽眾檢查（只報告）：超過 40 字的句子 3 句：a1pc 44（本輪加了「測試裡」）、npud 42、08ro 42。沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後。本輪沒有新增字典外的拉丁詞（eaan 刻意不唸 Pro、Max、Ultra）。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261106` → `daily-ai-20261106: 0 errors, 2 warnings`（開場濃縮兩條，本節目格式沒有開場濃縮；估 13.1 分鐘，163 句）。
- 懷疑但沒改：
  - **站上文章 WYO** 寫「在懷俄明州興建當地首座資料中心」，跟 GB3「our first data center in the state of Wyoming」意思不完全一樣（可讀成該州第一座）。不在本輪可改的範圍。
  - k3x0「它不給一般人」：V6 只說推給 Daybreak Red 的部分成員，沒明說一般人不能用；推論合理，站上文章 CYB 也這樣寫，沒改。
  - 9vnl「智慧家電」：TC5 的例子是 Apple TV（smart home devices），叫家電稍寬，沒改。
  - 4s28「這個有牙齒！」：英文 has teeth 的直譯，中文不常這樣說；jn7t 馬上講白，卡片也寫 Teeth，留給站主試聽時判斷。
  - rjbl「承諾沒說」：承諾本身限定「自己擁有並自營」，嚴格說它是有寫範圍的；照站主 2026-11-05 指示不暗示夥伴設施被排除，沒改。
  - x3w3 的保密協議解釋「不讓外界知道內容的合約」：NDA 是約定不對外透露的合約，白話夠用，沒改。
  - GPT-6 Cyber 一則的「跟你有什麼關係」在第 3、4 句才講（見清楚度檢查）。
- 需要第二輪：**是**。本輪改了 6 個事實（超過 3 個）。所有主張都已判定，沒有懸而未決的。
