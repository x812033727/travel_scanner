# daily-ai-20261110 主張與證據

每一行：編號｜主張（旁白或卡片上的說法）｜站上文章；原始來源｜來源查證日｜行 id（場景）。
事實只用站上 news_date 2026-11-09 已發布的文章（`/api/travel/guides/life/<slug>?locale=zh-TW` 取得，2026-11-09，4 篇皆 HTTP 200、`status: published`）與它們列的來源。
撰稿人 2026-11-09 也打開了 TV、AV、DJ、DN 四個原始來源（HTTP 200），只拿來核對文章的轉述。
「自述」＝公司或當事人自己說、沒有第三方確認；「解釋」＝節目用一句白話解釋名詞，是一般常識，不出自來源；「節目」＝節目自己的整理、看法或建議；「笑點」＝沒有事實主張的誇張或類比，列在最後一節給笑點檢查。

站上文章簡稱：
- TRUMP＝https://mokaair.com/zh-TW/life/ai-news-trump-60-minutes-ai-20261109 ；TV＝https://www.theverge.com/ai-artificial-intelligence/1029802/trump-60-minutes-ai （datePublished 2026-11-09T15:50Z）
- APPLE＝https://mokaair.com/zh-TW/life/ai-news-apple-intelligence-usage-packs-20261109 ；AV＝https://www.theverge.com/tech/1030084/apple-intelligence-usage-packs-ai-features-creator-studio-logic-pro （datePublished 2026-11-09T19:09Z）
- JET＝https://mokaair.com/zh-TW/life/ai-news-used-jet-engine-turbines-20261109 ；DJ＝https://decrypt.co/382890/ai-data-centers-used-jet-engines-power-turbines （Nov 9, 2026）
- NYSE＝https://mokaair.com/zh-TW/life/crypto-news-nyse-avalanche-settlement-20261109 ；DN＝https://decrypt.co/382833/nyse-avalanche-settle-tokenized-stock-platform （Nov 9, 2026）

## Monologue

c1｜2026-11-10 是星期二（曆法）；q003「昨天，11 月 9 日的另外兩則新聞」：四篇的 news_date 都是 2026-11-09｜各站上文章｜2026-11-09｜d001, q003
c2｜開場一句主菜：川普在《60 分鐘》談 AI 安全，說政府警告過一位 AI 公司老闆「準備坐牢」。TV「Trump claims the DOJ told a top AI executive, 'get ready to go to jail.'」與內文「We called them very strongly and said, 'Get ready to go to jail…'」；「一位 AI 公司老闆」＝「the leader of an AI company」。旁白掛「說」，是他的說法（見 c20）｜TRUMP；TV｜2026-11-09｜hk01；卡片 mo-topic
c3｜Kai 的問題（政府打電話叫老闆準備坐牢，是保護我們還是嚇跑創新）是假設句（「如果」），在 outro 回答（c47）｜—｜—｜q001 → o001

### Apple

c4｜據 The Verge，Apple 更新 Logic Pro，加入「Buy More Usage」選項，單次購買 49.99 美元（查核第 1 輪：原「一次買斷」聽起來像永久擁有，可是用量包 12 個月過期，改「單次購買」）（AV「has updated Logic Pro with an option to "Buy More Usage" for a one-time purchase price of $49.99」）；「做音樂的軟體」＝APPLE「音樂製作軟體 Logic Pro」｜APPLE；AV｜2026-11-09｜a001, a005；卡片 ap-what、ap-price
c5｜Apple 有些 AI 功能有用量上限，用完了可以付錢加買來繼續用（查核第 1 輪：原「要付錢才能繼續用」比來源強，來源只說用量包「allow users to continue accessing」，站上文章也寫「可能」）（AV「continue accessing certain Apple Intelligence features that have usage limits」；APPLE「依賴雲端模型的功能，在用完額度後可能要額外付費才能繼續使用」）｜APPLE；AV｜2026-11-09｜a002；卡片 ap-first
c6｜Apple 把它叫 Intelligence Usage Pack（AV「These Intelligence Usage Packs, as Apple calls them」）｜APPLE；AV｜2026-11-09｜a005；卡片 ap-price title
c7｜沒用完的額度按月滾存，購買 12 個月後到期（AV「any unused additional usage will roll over from month to month, but will expire 12 months after it was purchased」，引 Apple 官網）｜APPLE；AV｜2026-11-09｜a006；卡片 ap-price
c8｜有上限是因為這些功能依賴 OpenAI 或 Google Gemini 的雲端模型（AV「have usage limits because they rely on cloud-based AI models from OpenAI or Google Gemini」）；「雲端模型＝在遠端伺服器上跑的 AI」照 APPLE 的解釋｜APPLE；AV｜2026-11-09｜a007, a008；卡片 ap-why
c9｜用量包只限購買的 Apple 帳號，不支援家人共享（AV「can only be used by the Apple Account that purchased them (Family Sharing isn't supported)」）｜APPLE；AV｜2026-11-09｜a009；卡片 ap-family
c10｜Logic Pro 的上限受與助理對話的複雜度影響（AV 引 Apple「impacted by the complexity of conversations you have with the assistant」）｜APPLE；AV｜2026-11-09｜a011；卡片 ap-complex
c11｜Kai a004「我覺得這樣還算老實，總比用完就直接鎖住好」：意見；「用完就鎖住」對的是「有上限」（c5），不是說 Apple 以前會鎖住｜節目｜—｜a004

### 噴射引擎

c12｜據 Decrypt，AI 資料中心開發商在找二手燃氣渦輪機與退役噴射引擎（DJ「AI data-center developers are hunting for used gas turbines and retired jet engines」）；「蓋 AI 資料中心的公司」＝developers｜JET；DJ｜2026-11-09｜j001；卡片 je-what
c13｜原因：訂新的發電設備，伺服器可能要等電到下個十年（DJ「ordering brand-new power equipment could leave their servers waiting for electricity until the next decade」；旁白「新的發電設備要等太久」）｜JET；DJ｜2026-11-09｜j002；卡片 je-term 第一項
c14｜燃氣渦輪機＝燒天然氣、帶動發電機發電（DJ「burning natural gas to spin equipment connected to a generator」）｜JET；DJ｜2026-11-09｜j003；卡片 je-term 第二項
c15｜Decrypt 引述能源顧問公司 Wood Mackenzie：美國新燃氣渦輪機平均要六年交貨（DJ「New gas turbines now take an average of six years to deliver in the United States, according to energy consultancy Wood Mackenzie」）；旁白不唸公司名，卡片 note「per Wood Mackenzie」｜JET；DJ｜2026-11-09｜j006；卡片 je-wait
c16｜一條路是航空衍生渦輪機：用飛機噴射引擎技術做的發電機（DJ「an aeroderivative turbine, a power generator built using technology adapted from aircraft jet engines」）；旁白不說「航空衍生」這個詞｜JET；DJ｜2026-11-09｜j009；卡片 je-aero
c17｜二手渦輪機比較便宜、也可能比較快拿到；但供應有限、維護問題與污染許可是障礙（DJ In brief「Used turbines are cheaper and potentially faster to obtain, but limited supply, maintenance issues and pollution permits remain obstacles」）。價格數字不唸｜JET；DJ｜2026-11-09｜j011, j012；卡片 je-used
c18｜EthosEnergy 執行長 Ana Amicarella 跟路透社說「That secondary market is very, very hot right now」（DJ 引）；旁白「業界一家公司的執行長」，不唸名字；卡片 kicker「EthosEnergy's CEO, to Reuters」，source「Quoted by Decrypt」｜JET；DJ｜2026-11-09｜j013；卡片 je-hot
c19｜Kai j010「我覺得這招很聰明，總比乾等好」：意見｜節目｜—｜j010

### 第三則（接主菜）

c20｜據 The Verge，川普在美國電視專訪《60 分鐘》談到 AI 安全（TV 標題「Trump's 60 Minutes interview touched on AI safety」）。報導日 2026-11-09；專訪播出日報導沒寫，旁白不說｜TRUMP；TV｜2026-11-09｜t001；卡片 tr-lead

## Main Course

c21｜「想像一下，一家大型 AI 公司的老闆接到一通政府打來的電話」：節目設定的情境；「這通電話的內容，是川普自己在節目上說的」（c23）｜TRUMP；TV｜2026-11-09｜m001, m002；卡片 mc-scene
c22｜川普說，有人被舉報用 AI 做壞事，他們很強硬地打電話過去（TV「We had a situation where somebody was reported to us to be doing something bad with AI. We called them very strongly」）。卡片 mc-call 引原話片段「'Something bad / with AI'」｜TRUMP；TV｜2026-11-09｜m003；卡片 mc-call
c23｜他說他們對對方說「Get ready to go to jail. Please give your wife a kiss good night.」（旁白中譯「準備去坐牢吧。請給你太太一個晚安吻。」；查核第 1 輪：原譯「今晚記得……說晚安」加了「今晚」「記得」「說晚安」，放在引號裡要照原話，改成逐句直譯；卡片 mc-quote1 用原文）｜TRUMP；TV｜2026-11-09｜m004；卡片 mc-quote1
c24｜節目問他 AI 主管們對自家模型安全的警告（TV「Asked about AI executives' warnings about their models' safety on 60 Minutes」）；旁白「主管們對自家模型安全提出警告」（查核第 1 輪：原「警告自家模型不安全」把「warnings about their models' safety」說成定論，改回來源的說法）｜TRUMP；TV｜2026-11-09｜m007；卡片 mc-ask
c25｜「AI 安全＝AI 被拿去做壞事，或出錯傷到人的風險」：解釋（TRUMP 的「護欄」解釋是安全規範，AI 安全本身來源沒定義；查核要確認不超出）｜—｜—｜m008；卡片 mc-term
c26｜他回答「I think that the risk is not nearly as real as it– as they talk, and I think the risk can be managed, and it's managed.」（旁白「風險遠沒有他們說的那麼真實，風險可以管理，而且已經在管理了」；卡片 mc-risk 引後半）｜TRUMP；TV｜2026-11-09｜m009；卡片 mc-risk
c27｜他說是司法部在管這個風險（TV「He claimed the DOJ is managing that risk」）；「司法部＝負責起訴聯邦犯罪的政府部門」：解釋｜TRUMP；TV｜2026-11-09｜m010, m011；卡片 mc-doj（查核第 2 輪：川普的引句只說「we」，沒唸出司法部；「DOJ」是 The Verge 的轉述「He claimed the DOJ is managing that risk」。m010 改成「據 The Verge 的報導，他的意思是，現在管這個風險的是美國司法部。」卡片 mc-doj「The Justice Dept., / per The Verge's report」，key「DOJ, per The Verge」）
c28｜他不肯說出對象或公司，只說是一家 AI 公司的負責人，「One of the big ones」（TV「Trump refused to name the person or company…but said it was the leader of an AI company, "One of the big ones."」）｜TRUMP；TV｜2026-11-09｜m014, m015；卡片 mc-who
c29｜他說被威脅逮捕後「this person totally changed everything」（旁白「這個人完全改變了一切」；查核第 1 輪：原「改變了做法」照 TRUMP 的中譯，但放在引號裡，「做法」是加的，改成直譯「everything」）；改了什麼，他沒說，報導也沒寫（TV 確實沒有）｜TRUMP；TV｜2026-11-09｜m016, m018；卡片 mc-changed
c30｜這些只是川普的說法，經 The Verge 轉述；報導沒有第二個來源，也沒有司法部或當事公司的回應（TRUMP callout「本文僅依據 The Verge 的報導……為川普的自述，報導中沒有第二個來源，也沒有司法部的回應」；TV 內文也沒有任何回應）。「那家公司的回應」：TV 沒有，TRUMP FAQ「報導中沒有司法部或當事公司的回應」｜TRUMP；TV｜2026-11-09｜m019, m020, m062；卡片 mc-check、mc-unsure
c31｜兩人的立場是意見：Kai「站產業這邊」「坐牢的威脅會嚇跑想做 AI 的人」；Sola「總要有人能讓 AI 公司負責」「威脅不是規則」；mc-rules 規則寫清楚的三件事（什麼算做錯、誰來查、怎麼申訴）是節目的整理，不出自來源｜節目｜—｜m021–m029；卡片 mc-sides、mc-rules
c32｜他說「I don't mind guardrails, but I don't want to put us in a deep second position.」（旁白「不介意設護欄，但不想讓美國遠遠落到第二名」）；「護欄＝替 AI 發展設下的安全規範和限制」照 TRUMP 的解釋。m030「跟你很像」：Kai 的「寫完別人早就跑到前面」與「不想落到第二」都講速度，是節目的對照｜TRUMP；TV｜2026-11-09｜m030, m031, m032；卡片 mc-rails、mc-rails2
c33｜他說「absolutely would」與民主黨合作談 AI 安全（TV「60 Minutes's Ross Douthat went on to ask if Trump would work with Democrats on AI safety, and Trump said he "absolutely would"」）；要設什麼護欄、什麼時候設，報導沒提（TRUMP 表格「未提到具體法案或時程」「未說明護欄的內容」）｜TRUMP；TV｜2026-11-09｜m034, m035, s002；卡片 mc-dems
c34｜他說習近平「all in to SI, as I call it, because it really is super intelligence. It's a much better name, I think, because it's not artificial.」（旁白「全力投入他所謂的 SI，超級智慧」「這個名字比較好，因為它不是人工的」；TV「Eventually he said」，旁白不說「節目最後」；查核第 1 輪：m038 開頭「更怪的是」是節目替他的話下評語，改成中性的「但這還不是全部，他還說」）｜TRUMP；TV｜2026-11-09｜m038, m039；卡片 mc-si
c35｜亞洲：報導只提中國；他說「China has no guardrails, by the way. […] They have the guardrails that whatever President Xi says goes.」（旁白「川普說中國沒有護欄，他們的護欄就是習近平說了算」；查核第 1 輪：原「只有習近平說了算」漏掉他把習近平的話說成中國的「護欄」，改成照原句的兩段）；台灣報導完全沒提｜TRUMP；TV｜2026-11-09｜m043, m044；卡片 mc-asia
c36｜錢：報導沒有罰款、預算、具體法案或時間表（TV 全文沒有；TRUMP「未附具體措施」「未提到具體法案或時程」）｜TRUMP；TV｜2026-11-09｜m048, m049, m050；卡片 mc-money
c37｜誰贏誰輸是兩人的意見：Kai「做 AI 的人」「小公司」；Sola「看不到改了什麼的一般人」（依 c29）；m056「規則要寫得連小公司都看得懂」是 Sola 的意見｜節目｜—｜m053–m056；卡片 mc-lose、mc-small
c38｜接下來看三件事是節目的整理：電話有沒有人證實（c30）、護欄會不會寫成規則（c33）、「已經在管理」是怎麼管（c26）｜節目｜—｜m057–m061；卡片 mc-next
c39｜結尾：Kai 不改立場（m063、m064 是意見）；Sola「我的看法是」（m065、m066 是看法）。m062「我不知道」：c30｜節目｜—｜m062–m066

## Follow the Money

c40｜據 Decrypt，Ava Labs 週一說，Avalanche 會是 NYSE 關聯數位交易平台背後清算公司的「core ledger technology」（DN「Ava Labs, the company behind Avalanche, said Monday that the blockchain will serve as the "core ledger technology" for the clearing firm behind an NYSE-affiliated digital trading venue」；DN 標題「NYSE Taps Avalanche」）。f002「紐約證券交易所 NYSE 規劃中的新平台，要用一條叫 Avalanche 的區塊鏈來記帳」（DN 導言「The New York Stock Exchange is turning to Avalanche to power the behind-the-scenes plumbing of its forthcoming tokenized securities platform」）：平台是「NYSE-affiliated」、用它的是平台背後的清算公司，f011 補「Avalanche 背後的公司說，它會是這個平台清算公司的核心帳本」。查核第 1 輪：原 f002「紐約證券交易所，也就是 NYSE 的新交易平台」聽起來像「NYSE＝新交易平台」，也沒說平台還在規劃；卡片 fm-intro 原「NYSE picks Avalanche」把 Ava Labs 的宣布寫成 NYSE 的決定（NYSE 沒有自己的公告，只有 Dennis Lee 的談話），改成「Avalanche for an / NYSE-linked venue」，key「Avalanche for NYSE venue」｜NYSE；DN｜2026-11-09｜f002, f011；卡片 fm-intro、fm-ledger
c41｜重要在於區塊鏈被放在清算與結算這一層、讓交易最終完成的「管線」，不只是把單一基金或股票做成代幣（DN「puts a blockchain underneath the clearing and settlement layer, the plumbing that finalizes trades, rather than just wrapping a single fund or stock in a token」）｜NYSE；DN｜2026-11-09｜f003, f025；卡片 fm-why、fm-pipes
c42｜成交、清算、結算三步：清算＝確認雙方該交付什麼；結算＝實際完成股票與款項交換（NYSE callout「清算與結算：買賣成交後，確認雙方該交付什麼，並實際完成股票與款項交換的步驟」）。網購的對照是節目的類比｜NYSE｜2026-11-09｜f005–f009；卡片 fm-steps、fm-shop
c43｜帳本＝記錄每筆交易、誰擁有什麼的總紀錄（NYSE）；代幣化＝把股票、基金等傳統資產發行成區塊鏈上的代幣（DN「Tokenization, the practice of issuing traditional assets as blockchain-based tokens」；NYSE）；「區塊鏈＝很多台電腦一起保管、寫上去就很難改的帳本」：解釋，不出自來源｜NYSE；DN｜2026-11-09｜f013, f041, f014；卡片 fm-terms
c44｜平台交易的是代幣化證券（DN「tokenized securities platform」）；f016「可以這樣想」回應 Kai 的白話（股票換一種方式記在區塊鏈上），是解釋｜NYSE；DN｜2026-11-09｜f015, f016
c45｜設計目標：全天候交易、清算與結算，須待監管核准（DN「designed to allow 24/7 trading, clearing and settlement of tokenized securities, subject to regulatory approval」）；上線時間報導沒說（NYSE FAQ「報導中未說明上線時間」）｜NYSE；DN｜2026-11-09｜f017, f019；卡片 fm-247
c46｜NYSE 數位發行主管 Dennis Lee：交易所是「picking the right technology for each job」，平台會支援在多種區塊鏈上市的股票，但記錄與結算交易的帳本要快、可靠、能控管誰可以參與（DN）。旁白不唸名字；卡片 source 寫名字｜NYSE；DN｜2026-11-09｜f020, f021, f022, f023；卡片 fm-quote、fm-needs
c47｜Decrypt 說這是華爾街最老牌的機構把核心市場基礎設施搬上公有區塊鏈的跡象（DN「one of the clearest signs yet that Wall Street's oldest institutions are moving core market infrastructure onto public blockchains」）；旁白「核心設施」｜NYSE；DN｜2026-11-09｜f026；卡片 fm-sign
c48｜這筆合作的金額報導沒寫（DN、NYSE 都沒有任何金額）｜NYSE；DN｜2026-11-09｜f027
c49｜ICE 與 OKX 計劃設立代幣化股票平台；七巨頭（包括 Apple 與 Meta）全都選擇不讓股票在該平台代幣化（DN「ICE and crypto exchange OKX are planning a 24/7 tokenized stock venue under an SEC exemption」「Every Magnificent Seven stock, including Apple and Meta, opted out of having its shares tokenized on the venue」）。「美股七巨頭＝七家大型科技公司的統稱」：解釋（Magnificent Seven 是市場慣稱；查核第 1 輪：原「七家最大的科技公司」說成市值排名，慣稱不等於前七大，改「統稱」）。f029「NYSE 的母公司 ICE」：DN「the NYSE's parent Intercontinental Exchange」（查核第 1 輪補「NYSE 的」，原「母公司 ICE」沒說是誰的母公司）。DN 的「with 67 companies in all joining them」不念：可讀成「連同七巨頭共 67 家」或「另有 67 家」，站上文章寫成後者，來源沒說清楚｜NYSE；DN｜2026-11-09｜f029, f036；卡片 fm-catch
c50｜IMF 研究：代幣化股票有真實需求，但不平均（DN「Research shows the appetite for tokenized stocks is real but uneven. An IMF study found tokenized stocks show genuine demand…」）。波動與流動性那半句不唸（太接近價格）｜NYSE；DN｜2026-11-09｜f030；卡片 fm-imf
c51｜Decrypt 的提醒：基礎設施到位可能比市場需求跟上還快（DN「the infrastructure may be arriving faster than the markets to fill it」）｜NYSE；DN｜2026-11-09｜f032；卡片 fm-early
c52｜「不是投資建議，也不推薦任何代幣或平台」：節目聲明（NYSE 文末同樣聲明）｜節目｜—｜f035；卡片 fm-note
c53｜Kai 的意見：f018「交易終於不用下班了」、f040「比又多一個新產品實在」、f034「先蓋好比較好」；都不談價格、報酬或買賣｜節目｜—｜f018, f040, f034

## Sign-off

c54｜s001「今天最重要的，是川普談 AI 安全的那段話」、s002「最不確定的是護欄會長什麼樣子，報導完全沒說」（c33）：節目的看法｜節目｜—｜s001, s002；卡片 so-take
c55｜s003「節目的建議是，買任何 AI 加量包之前，先看能不能跟家人共用，還有多久會過期」：節目的建議，不是事實主張；依據是 c7、c9（Logic Pro 的用量包不支援家人共享、12 個月到期）｜節目；AV｜—｜s003；卡片 so-tip
c56｜s004 回扣 j007（c15 的六年）｜—｜—｜s004
c57｜s006 Mokaair 網站的完整整理：四篇站上文章，說明欄列網址｜—｜—｜s006
c58｜outro：o001「保護人又不嚇跑人的，是規則」是節目的答案（意見），回答 q001；o002 留言題｜節目｜—｜o001, o002

## 盲聽修改第 2 輪（第一次聽的讀者 6/10；保留查核第 1 輪的全部改動）

直接改 `video.json`，沒有重跑 build.mjs。下面是改過、新增的事實句與它們的依據；拿掉的句子列在最後。本輪改過的事實句（c59–c74）要再交查核代理對一次。

c59｜hk01／hk02 拆成兩句：「川普上了美國電視新聞節目《60 分鐘》，談 AI 安全。」「他說，政府警告過一位 AI 公司老闆『準備坐牢』。」＝c2、c20；「美國電視新聞節目」是對《60 分鐘》的解釋｜TRUMP；TV｜2026-11-09｜hk01, hk02
c60｜a011「用量上限會受你跟 Logic Pro 內建 AI 助理對話的複雜度影響」＝c10；「內建 AI 助理」：AV「It has a built-in AI assistant」，APPLE「Logic Pro 內建 AI 助理」｜APPLE；AV｜2026-11-09｜a011
c61｜m003「川普說，有人向政府舉報某人用 AI 做壞事，政府那邊就很強硬地打電話給對方」；m004「他說，政府跟對方講：……」。原話只說「reported to us」「We called them」，「us／we」讀成政府，依據是 TV 對同一段話的描述「He claimed the DOJ is managing that risk」「Trump claims the DOJ told a top AI executive」；旁白說「政府」不說「司法部」，不替他指定是哪個單位打的。查核可決定要不要改成「他說『我們』」｜TRUMP；TV｜2026-11-09｜m003, m004（查核第 2 輪：留「政府」。TV 自己把這段的「we」寫成 DOJ（「Trump claims the DOJ told…」「He claimed the DOJ is managing that risk, saying, 'We…'」），「政府」比 DOJ 寬，又掛在「川普說」底下，沒有超出來源；hk02、m001、q001 也都說「政府」，全片一致。是哪個單位，交給 m010 用「據 The Verge」標明。卡片 mc-quote1 kicker 改「Trump, retelling the call」、key 改「Retold: 'go to jail'」，讓人看出是他轉述的話，不是他對誰說的）
c62｜m009「風險遠沒有那些 AI 主管說的那麼真實」：「as they talk」的 they＝前一句的「AI executives」（TV「Asked about AI executives' warnings…」）｜TRUMP；TV｜2026-11-09｜m009
c63｜m043「台灣，報導完全沒提到；亞洲只提到中國。」m069「那是川普自己的說法：他說中國沒有護欄，他們的護欄就是習近平說了算。」＝c35，照查核第 1 輪的譯法，只把「是他的說法」講在前面｜TRUMP；TV｜2026-11-09｜m043, m069；卡片 mc-asia
c64｜f002「紐交所的母公司 ICE 在規劃新平台，要交易記在區塊鏈上的股票」：DN「The platform, which the NYSE's parent Intercontinental Exchange previously said it was developing, is designed to allow 24/7 trading … of tokenized securities」；「記在區塊鏈上的股票」是代幣化證券的白話（c43）。卡片 fm-intro「NYSE's parent plans / on-chain shares」，key「On-chain stock venue」（不再寫 NYSE 選了 Avalanche）｜NYSE；DN｜2026-11-09｜f002；卡片 fm-intro
c65｜f042「Avalanche 這條區塊鏈的開發公司說，這個平台的帳，會記在 Avalanche 上」＝c40（Ava Labs 說 Avalanche 是清算公司的 core ledger technology）；f011「替買賣雙方對帳、交割的清算公司，會拿 Avalanche 當核心帳本」＝c40；「清算公司＝替買賣雙方對帳、交割的公司」：解釋｜NYSE；DN｜2026-11-09｜f042, f011；卡片 fm-books、fm-ledger
c66｜f043「一筆股票買賣成交以後，還要確定錢和股票真的換手，這一步叫清算和結算」：NYSE callout「買賣成交後，確認雙方該交付什麼，並實際完成股票與款項交換的步驟」；f003「區塊鏈這次被放進的就是這一步，Decrypt 叫它市場的管線」＝c41｜NYSE；DN｜2026-11-09｜f043, f003；卡片 fm-plain、fm-why
c67｜f041 改由 Kai 說區塊鏈的解釋（內容不變，解釋）；f015 Kai「股票還是那張股票，只是記帳的地方換了」、f016 Sola「差不多」＝c44｜—｜—｜f041, f015, f016
c68｜f049「他說，平台會支援在好幾條區塊鏈上市的股票」、f021「記錄和結算交易的那本帳，他說有條件」＝c46（f021 拆成兩句）；f039 Kai「我覺得這很務實……」：意見｜NYSE；DN｜2026-11-09｜f049, f021, f039
c69｜f026「這是華爾街老牌機構把核心設施，搬上公有區塊鏈的跡象」＝c47；f047「公有，就是誰都看得到帳上的紀錄，不像銀行的帳只放在自己家裡」：解釋，不出自來源（DN 只寫「public blockchains」）。注意 c46 Lee 說帳本要「能控管誰可以參與」，f047 講的是看得到紀錄，不是誰都能參與；查核要確認兩句聽起來不矛盾｜DN｜2026-11-09｜f026, f047；卡片 fm-public（查核第 2 輪：改。原句「誰都看得到帳上的紀錄」加上卡片「Anyone can see it」，聽起來像這個平台的交易紀錄人人可見，DN 沒有這樣說；Lee 又說這本帳要「able to control who participates」，兩句一起聽會打架；「銀行的帳只放在自己家裡」也是來源沒有的對照。f047 →「公有區塊鏈一般誰都看得到紀錄，但 NYSE 主管說，這本帳仍要控管誰能參與。」卡片 fm-public 左「Public blockchain：Usually open to view」，右「This platform's ledger：Controls who joins」，key「Public, but gated entry」）
c70｜f040 Kai「放進交易的底層，比只把一檔股票包成代幣實在」：意見；比較的兩邊照 DN「puts a blockchain underneath the clearing and settlement layer … rather than just wrapping a single fund or stock in a token」｜DN｜—｜f040；卡片 fm-kai3
c71｜f029「ICE 還跟加密貨幣交易所 OKX，在規劃另一個代幣化股票平台」＝c49（ICE 在 f002 已介紹）；f036「美股七巨頭，是包括 Apple 和 Meta 在內的七家大型科技股統稱」（查核第 1 輪「統稱」的說法）；f048「這七家全都選擇，不讓自己的股票在 ICE 和 OKX 的平台上代幣化」＝DN「Every Magnificent Seven stock … opted out of having its shares tokenized on the venue」，把「那裡」改成平台名｜NYSE；DN｜2026-11-09｜f029, f036, f048；卡片 fm-catch
c72｜f030「代幣化股票確實有人要，但還不容易順利買賣」：DN「An IMF study found tokenized stocks show genuine demand yet remain volatile and illiquid」，取 genuine demand 與 illiquid；「不易順利買賣」是 NYSE 文章對流動性不足的解釋。volatile（價格波動）仍不唸。卡片 fm-imf「Real demand, / hard to trade」，kicker「Per an IMF study」現在對得上 IMF 的用字｜NYSE；DN｜2026-11-09｜f030；卡片 fm-imf（查核第 2 輪：CONFIRMED。「確實有人要」＝genuine demand，「還不容易順利買賣」＝illiquid，兩者都是 DN 轉述的 IMF 研究結論，kicker「Per an IMF study」歸屬正確；「real but uneven」是 Decrypt 自己的概括，旁白與卡片都已不用）
c73｜j010 Kai「飛機退役的引擎，換個地方繼續上班」：擬人；事實是 DJ「seeking older machines and retired aircraft engines that can be rebuilt for stationary power production」（j001 已說在找退役噴射引擎）｜JET；DJ｜2026-11-09｜j010
c74｜outro：o001「我說靠規則，Kai 說先讓產業跑，出事再依法罰」：兩位主持人的立場（m063、m066），不是事實主張；o002「你站哪一邊？留言告訴我們。」；卡片 outro「Rules first, or speed?」｜節目｜—｜o001, o002

意見句（沒有事實主張）：a004「我可以接受，至少還能自己決定要不要加買」（接 c5）；m005「這種事不是應該走正式程序嗎？一通電話就算數？」；m013「最可怕的是不知道風險算大還是算小」；m032 Kai 說護欄的解釋（照 TRUMP）並說「我同意要有，只是不要多到跑不動」；m037；m047「罰則寫清楚最重要，罰多少都比一通電話好猜」；m052「公司連下一通會打給誰都不知道」；m056 Sola「規則寫太複雜，最先撐不住的確實是小公司」；f004；f010；f045；f046；f034。

拿掉的句子：a013（ap-joke 場景）、j013（je-hot 場景，c18 不再出現在旁白）、m006、m067、m042、m044、m068、m059、m038–m041（mc-si、mc-joke3 兩個場景，c34 不再出現；這也拿掉了查核第 1 輪改過的 m038「但這還不是全部」與 m041 措辭）、f024、f037。卡片 mc-rails2 改成 Kai 的護欄立場，mc-joke2、mc-cost 改字（見笑點）。

## 笑點（無事實主張）

給查核代理做笑點檢查：每個笑點前一行的事實、笑點本身、為什麼不算新的事實。沒有新的數字、沒有雙關與諧音、沒有替真人編的話、不打一般人。

- a010（Kai）「一家人什麼都能分，就這包 AI 不能分？」：誇張的反應，接 a009（c9）。笑的是 Apple 的規則，不是家人。
- a012（Sola）「打個比方，就像手機流量，聊得越複雜，掉得越快。」：類比，接 a011（c10）；「打個比方」標明。查核第 1 輪：原「計程車跳表，跳得越快」是邊用邊付錢，聽起來像 Apple 按對話計費；實際是一包固定額度、用得快就早用完，手機流量（有上限、可以加買）對得上。
- a013（Kai）「原來跟 AI 講話，要講簡單一點才省錢！」：誇張的推論，接 c10；「省錢」是玩笑，Apple 沒有這樣說。
- a015（Kai）「我有一個每集都要問的老問題：所以我要不要換手機？」：固定梗（11/6 起），這一句先交代它是每集都問的老問題；a016（Sola）「不用，這次要你掏錢的不是手機，是 AI 的額度。」接 c4、c5。
- j007（Sola）「打個比方，就像小一的時候下訂，小六畢業才送到。」：類比，接 j006（c15 的六年）；台灣小學六年，沒有新數字；s004 回扣。
- j008（Kai）「等到交貨，資料中心裡的晶片都要過時了吧！」：誇張，「吧」是猜測，不是事實主張。
- j015（Kai）「老問題又來了，所以我要不要換手機？」；j016（Sola）「不用，今天連資料中心都在找二手的。」：固定梗第二次，接 c12。
- t002（Kai）「好，叫人準備坐牢算保護還是嚇人，現在可以吵了。」：串場，把開場的問題重說一次。
- m005（Kai）「連晚安吻都幫人家安排好了？」：反應，接 m004（c23 的原話「Please give your wife a kiss good night」）；笑的是有權力的人說的話，不改原話。
- m012（Sola）「所以風險沒那麼真實，可是已經真實到，要打電話叫人準備坐牢。」：把 c26 與 c22、c23 兩句他自己的話放在一起，笑政策說法前後對不上；不說他說謊，不評他的政治立場。卡片 mc-joke1 原「real enough for jail」讀成有人坐牢，查核第 1 輪改「yet a jail warning」。m013（Kai）「所以風險到底是有，還是沒有？我聽到頭都暈了。」：反應。
- m017（Kai）「有用？我看是把人嚇到不敢動吧。」：Kai 的意見（他的立場），接 c29；不是在說那位負責人做了什麼。m018（Sola）「改了什麼，他沒說，報導也沒寫。」：事實（c29）。
- m036（Sola）「打個比方，就像考試範圍還沒公布，老師已經先打電話說你會被當。」：類比，接 m034、m035（c33 護欄沒說內容）與 c22、c23（警告電話）；笑的是政策順序，不是任何人的政治立場。m037（Kai）「這種課，我一定第一個退選！」：誇張，假設語氣。
- m040（Sola）「身為一個 AI 主持人，我得承認，我就是人工的。」；m041（Kai）「我也是，至少 AI 這個名字，用在我們身上很誠實。」（查核第 1 輪：原「我們的名字」會聽成 Sola、Kai 這兩個名字，改說清楚是「AI」這個名字）：接 m039（c34）；笑點打在主持人自己身上（兩位主持人是 AI，說明欄已揭露），不笑川普的用詞。
- m051（Sola）「所以照報導，這場談話到目前為止唯一的成本，是一通電話。」：誇張，接 c36（沒有罰款、預算、法案）；「成本」是比喻，沒有金額。m052（Kai）「而且那通電話，除了他自己，沒人證實過。」：事實（c30），補刀。查核第 1 輪：報導沒寫不等於沒有，m051 補「照報導」；原 m052「還沒人證實有打過」漏了川普本人就是說有打的人，補「除了他自己」；卡片原「The policy's cost」把一段談話說成政策，改「Cost in the report: / one phone call」。
- m059（Kai）「第一件，我賭會有很多公關在開會。」：猜想，沒有事實主張，不指任何一家公司。
- m068（Kai）「連預算都沒有？」：反應，接 m049（c36）。
- f010（Kai）「所以 Avalanche，是在幫股票送包裹？」：想歪，接 f009 的網購類比；f011 用來源更正（c40）。
- f018（Kai）「我覺得這很酷，交易終於不用下班了！」：擬人，接 f017（c45 的全天候）；f019（Sola）「監管機關還沒點頭之前，它連第一天上班都還沒排。」：接 c45（待核准、沒說上線時間），擬人，沒有新日期。
- f024（Kai）「那錢流去哪？」；f025（Sola）「所以今天跟的不是錢，是錢走的管線。」：接 f027（c48）與 c41（Decrypt 的「plumbing」）。
- f031（Kai）「Apple 這一集出場兩次，一次在賣 AI 加量包，一次在拒絕被代幣化。」：callback，兩件事都是本集照來源講過的事實（c4、c49）。查核第 1 輪：原「今天」會聽成兩件事同一天發生（DN 沒寫 OKX-ICE 退出的日期，不是 11/9 的新聞），旁白改「這一集」，卡片「twice today」改「on air twice」。
- f033（Sola）「打個比方，就像捷運站先蓋好了，乘客還在路上。」：類比，接 f032（c51）。f034（Kai）「我還是覺得先蓋好比較好，總比人到了沒車坐好。」：Kai 的意見，接同一個類比；不是投資看法。
- s004（Sola）「今天最有耐心的，是在等新渦輪機的資料中心，小一下訂，小六才到貨。」：回扣 j007。s005（Kai）「等它到貨，我的老問題，大家應該都會背了。」：誇張，沒有新的事實。查核第 1 輪：原「好幾百次」是一個新的數量（平日一集、六年其實上千集），改成不帶數字的說法。

盲聽修改第 2 輪（笑點改打政策與做法，不打人；兩位主持人互相吐槽）：
- m005（Kai）改「等一下，這種事不是應該走正式程序嗎？一通電話就算數？」：原本「連晚安吻都幫人家安排好了？」笑的是他的用字；改成 Kai 替產業質疑做法，接 c22、c23。
- m012（Sola）改「同一段話裡，風險沒那麼真實，處理方法卻是坐牢警告。」（查核第 2 輪 →「同一段話裡，風險沒那麼真實，他舉的例子卻是坐牢警告。」：一通電話是他舉的一個例子，「處理方法」會聽成整套政策就是坐牢警告）：笑的是說法與做法對不上，不說「他」；事實照 c26、c23。m013（Kai）改「對做 AI 的公司來說，最可怕的是不知道風險算大還是算小。」：Kai 的立場（可預期性），不是反應。
- m033（Sola，對 Kai）「你要的護欄，最好都裝在別人的車道上。」：接 m032 Kai「要有，只是不要多到跑不動」，吐槽 Kai，沒有事實主張。原本 Kai「你看，連他都說……」把 Kai 跟川普綁在一起，拿掉。
- m036（Sola）改「打個比方，就像考試範圍還沒公布，被當的通知已經先寄出來了。」：拿掉「老師打電話」（太像在指某個人），只留順序的對比：規則（c33 沒說內容）還沒有、警告（c23）已經來了。m037（Kai）改「對想創業的人來說，這種課根本不敢選。」：Kai 的立場。卡片「Fail notice: sent」。
- m051（Sola）改「所以照報導，這套管法目前沒有一條寫下來的規則，只有一通電話。」（查核第 2 輪 →「所以照報導，這套管法只講到一通電話，沒提到寫下來的規則。」：「沒有一條寫下來的規則」把報導沒寫說成沒有，而且坐牢警告本身就要靠寫下來的刑法；卡片 key「Written rules: not yet」→「Written rules: not cited」）：依 c36（報導沒有罰款、預算、法案）；「照報導」照查核第 1 輪保留。m052（Kai）改「而且公司連下一通會打給誰都不知道，這最嚇人。」：Kai 的立場，不再說「沒人證實」（c30 已在 m019、m020 講）。卡片「Written rules: / none reported」。
- SI 那段（m038–m041）整段拿掉：本來笑點打在主持人身上，但緊貼著他的用字，讀者聽成在笑他。
- f016（Sola，對 Kai）「差不多，Kai 今天難得一次講對。」；f050（Sola，對 Kai）「難得，你這次沒有先問要不要換手機。」：回扣固定梗。f046（Kai 回嘴）「那我先幫它準備工作服。」：接 f019 的擬人。
- j010（Kai）「飛機退役的引擎，換個地方繼續上班。」：擬人，見 c73。

## 我懷疑但沒動的事

- f002：DN 標題是「NYSE Taps Avalanche」，宣布的卻是 Ava Labs（「Ava Labs … said Monday」），內文沒有 NYSE 自己的公告，只有 Dennis Lee 的談話。撰稿時把原本的「NYSE 選了一條叫 Avalanche 的區塊鏈」改成「NYSE 的新交易平台，要用一條叫 Avalanche 的區塊鏈來記帳」，f011 再說是 Avalanche 背後的公司說的；卡片 fm-intro「NYSE picks / Avalanche」照 DN 標題留著，查核可決定要不要改。
- m007「AI 公司的主管們警告自家模型不安全」：TV 是「warnings about their models' safety」，沒說是哪些主管、警告了什麼；旁白不加細節。
- m043「中國沒有護欄，只有習近平說了算」：原話是「China has no guardrails … They have the guardrails that whatever President Xi says goes」，旁白把後半壓成「只有習近平說了算」，意思一樣，但不是逐字。
- 美股七巨頭的白話「七家最大的科技公司」：Magnificent Seven 是市場慣稱，DN 只說包括 Apple 和 Meta，沒列全部；旁白只舉這兩家。
- 「67 家公司」：DN「with 67 companies in all joining them」，NYSE 文章寫成「另有 67 家公司也選擇退出」；兩種讀法算法不同，不念。

## 沒有放進來的

- Trump：訪問者 Ross Douthat 的名字；他先前說「artificial intelligence」是他視為敵人的人用的詞；「With me, it's pretty strong, but it's not quite that strong.」；「We're leading number one.」
- Apple：9to5Mac 先發現、9 月初的支援文章、Logic Pro 助理能做的事（開始新歌、設定人聲音軌）、購買位置（Intelligence Features > Show Usage）、預期加入的其他 App（Pixelmator Pro、Final Cut Pro、Motion、Pages、Keynote、Numbers；第 1 稿念過，為了長度刪掉）。
- 噴射引擎：100 吉瓦對 60–70 吉瓦、Siemens Energy、GE Vernova、三菱重工、國際能源署的 485 與 950 太瓦時、Crusoe 的 13 台與 650 兆瓦、每兆瓦價格、29 兆瓦 1,250 萬美元、環保署的空氣污染標準、OpenAI 的電費承諾、Cleanview 的 90 與 2 吉瓦、Wärtsilä 的 3 吉瓦、交貨討論集中在 2030 與 2031 年、接公共電網也要好幾年（第 1 稿念過，為了長度刪掉）。
- NYSE：Emin Gün Sirer 的「24/7 atomic settlement」與可預期的成本、Blockchain.com 合作、SEC 豁免、摩根士丹利、IMF 研究的波動與流動性不足。

## 進度

- 第 1 稿（2026-11-09）：76 個場景、151 句（Kai 42 句）；`lint` 0 錯誤、1 條警告（開場章節長度：本節目沒有開場濃縮，照 daily-brief.md 不理）；估 13.7 分鐘，最長畫面狀態 12.9 秒（mc-asia），其次 12.8 秒（tr-lead）、12.7 秒（mc-changed）。
- 句子完整性檢查 0 行；`key`／`keys` 全部 ≤24 字、`keys` 數量與畫面狀態一致；`big`、`quote`、`outro` 沒有 `reveal`；`big` 卡每行 ≤22 字。
- 卡片組合：big 49、quote 8、bullets 7、compare 4、stats 3、steps 2、title 1、outro 1；lint 沒有再報跟 daily-ai-20261106 的投影片順序相似（11/9 是 86%）。
- 新加的發音字典詞（null）：Avalanche、Follow、Logic、Money、NYSE、Pack、SI、Usage。
- 待做：另派查核代理照 `prompts/verifier-video.md` 逐句對回原始來源並做笑點檢查；盲讀；Whisper 第二意見與試聽。
- 盲聽修改第 2 輪（2026-11-10，保留查核第 1 輪的全部改動，直接改 `video.json`）：75 個場景、147 句（Kai 36 句）；`lint` 0 錯誤、1 條警告（開場章節長度，同前）；估 14.0 分鐘，最長畫面狀態 12.8 秒（ap-complex、tr-lead），outro 12.0 秒；三個檢查都是 0 行，`big` 卡每行 ≤22 字。卡片：big 50、quote 6、bullets 7、compare 5、stats 3、steps 2、title 1、outro 1，lint 沒報投影片順序相似。字典拿掉 SI（旁白不再念）。本輪改過的事實句 c59–c74 要再交查核代理對一次。
- 查核第 2 輪（2026-11-10，另一個代理，只查盲聽第 2 輪改過的部分，見 verify-2.md）：改 5 處事實（m010 與 mc-doj、mc-quote1 卡片、f047 與 fm-public、m051 與 mc-cost key、m012；c61 的「政府」查過留著），笑點改 2 句（m012、m051）。`lint` 0 錯誤、1 條警告（同前）；估 14.1 分鐘，147 句；最長畫面狀態 12.8 秒（ap-complex、tr-lead、mc-joke1），outro 12.0 秒；句子完整性檢查 0 行。
