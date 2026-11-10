# daily-ai-20261110 查核第 1 輪

查核日 2026-11-10（台北時間）。查核代理不是撰稿人。每一條旁白（`text`，Sola 與 Kai 兩位都查；本片沒有 `say`）、每張卡片的 `data`（含 `kicker`、`source`、`key`、`keys`）、章節名、縮圖、`youtube.title`、`description`、`tags` 都抽出來逐條對照（清單在工作區 `_tools/dump.txt`）。
來源：站上 4 篇文章（`/api/travel/guides/life/<slug>?locale=zh-TW`，間隔 1.2 秒，全部 HTTP 200、`status: published`，news_date 2026-11-09，與 claims.md 相同），加上 `video.json` `sources` 的 4 個原始來源，用 `Mokaair-editorial/1.0` UA 以 curl 重開（去掉 `<!-- -->` 後讀全文，全部 200、沒有轉址）。web search 0 次。
另有〈笑點檢查〉與〈清楚度檢查〉兩節。

## 來源代號

站上文章（全部 200，published，news_date 2026-11-09）：

| 代號 | slug |
| --- | --- |
| TRUMP | ai-news-trump-60-minutes-ai-20261109 |
| APPLE | ai-news-apple-intelligence-usage-packs-20261109 |
| JET | ai-news-used-jet-engine-turbines-20261109 |
| NYSE | crypto-news-nyse-avalanche-settlement-20261109 |

原始來源（全部 HTTP 200，沒有轉址）：

| 代號 | URL（頁面上的日期） |
| --- | --- |
| TV | https://www.theverge.com/ai-artificial-intelligence/1029802/trump-60-minutes-ai （Stevie Bonifield，datePublished 2026-11-09T15:50Z） |
| AV | https://www.theverge.com/tech/1030084/apple-intelligence-usage-packs-ai-features-creator-studio-logic-pro （Andrew Liszewski，datePublished 2026-11-09T19:09Z） |
| DJ | https://decrypt.co/382890/ai-data-centers-used-jet-engines-power-turbines （Jose Antonio Lanz，Nov 9, 2026） |
| DN | https://decrypt.co/382833/nyse-avalanche-settle-tokenized-stock-platform （Decrypt Staff，Nov 9, 2026） |

## 主張表

| # | 主張 | 位置 | URL | HTTP | 判定 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 今天 11 月 10 日星期二；昨天 11 月 9 日的新聞 | d001、q003；intro、mo-day | 曆法；站上 4 篇 | 200 | CONFIRMED（2026-11-10 是星期二；四篇 news_date 都是 11-09，四個原始來源都是 11/9 發布） | |
| 2 | 主菜一句：川普在《60 分鐘》談 AI 安全，說政府警告過一位 AI 公司老闆「準備坐牢」；卡片 Trump on AI safety: a jail warning；標題、縮圖 | hk01；mo-topic、youtube.title、thumbnail | TV | 200 | CONFIRMED（副標「Trump claims the DOJ told a top AI executive, 'get ready to go to jail.'」；內文「We called them very strongly and said, 'Get ready to go to jail…'」；以「說」標成他的說法） | |
| 3 | Kai 的問題（如果……政府就打電話叫老闆準備坐牢） | q001；mo-q | — | — | OUT OF SCOPE（假設句，outro 回答） | |
| 4 | 據 The Verge，Apple 在做音樂的軟體 Logic Pro 裡開始賣 AI 功能的額外用量；卡片 Logic Pro sells more AI usage | a001；ap-what | AV | 200 | CONFIRMED（「has updated Logic Pro with an option to "Buy More Usage"」；副標「Logic Pro is Apple's first app to charge for extended usage」） | |
| 5 | Apple 有些 AI 功能有用量上限，用完要付錢才能繼續用 | a002；ap-first | AV、APPLE | 200 | **CHANGED（措辭）**（AV 只說用量包「will allow users to continue accessing certain Apple Intelligence features that have usage limits」，沒說付錢是唯一的路；APPLE 寫「可能要額外付費」） | →「這代表 Apple 有些 AI 功能有用量上限，用完了，可以付錢加買來繼續用。」 |
| 6 | Apple 叫它 Intelligence Usage Pack，一次買斷，49.99 美元；卡片 $49.99 One-time purchase | a005；ap-price | AV | 200 | **CHANGED**（「These Intelligence Usage Packs, as Apple calls them」「one-time purchase price of $49.99」都對；但「買斷」在中文是永久擁有，跟下一句「12 個月後過期」打架） | 「一次買斷」→「單次購買」；卡片沒動 |
| 7 | 沒用完的額度每月滾存，購買 12 個月後過期；卡片 12 mo、unused use rolls over | a006；ap-price | AV | 200 | CONFIRMED（「any unused additional usage will roll over from month to month, but will expire 12 months after it was purchased」） | |
| 8 | 有上限是因為有些功能交給 OpenAI 或 Google Gemini 的雲端模型；雲端模型的解釋 | a007、a008；ap-why | AV、APPLE | 200 | CONFIRMED（「rely on cloud-based AI models from OpenAI or Google Gemini」；解釋照 APPLE） | |
| 9 | 只限購買的 Apple 帳號，不支援家人共享 | a009；ap-family | AV | 200 | CONFIRMED（「can only be used by the Apple Account that purchased them (Family Sharing isn't supported)」） | |
| 10 | Apple 說 Logic Pro 的上限受跟助理對話的複雜度影響 | a011；ap-complex | AV | 200 | CONFIRMED（「impacted by the complexity of conversations you have with the assistant」） | |
| 11 | Kai：還算老實，總比用完就直接鎖住好 | a004 | — | — | OUT OF SCOPE（意見） | |
| 12 | 據 Decrypt，蓋 AI 資料中心的公司在找二手發電渦輪機，連退役噴射引擎都找；卡片 used jet engines | j001；je-what | DJ | 200 | CONFIRMED（「AI data-center developers are hunting for used gas turbines and retired jet engines」） | |
| 13 | 原因：資料中心要電，新的發電設備要等太久 | j002；je-term | DJ | 200 | CONFIRMED（「ordering brand-new power equipment could leave their servers waiting for electricity until the next decade」） | |
| 14 | 燃氣渦輪機＝燒天然氣、帶動發電機發電 | j003；je-term | DJ | 200 | CONFIRMED（「burning natural gas to spin equipment connected to a generator」） | |
| 15 | Decrypt 引述一家能源顧問公司：美國新燃氣渦輪機平均要等六年交貨；卡片 6 yrs per Wood Mackenzie | j006；je-wait | DJ | 200 | CONFIRMED（「New gas turbines now take an average of six years to deliver in the United States, according to energy consultancy Wood Mackenzie」） | |
| 16 | 一條路是拿飛機噴射引擎的技術改成發電機；卡片 Jet-engine tech, on land | j009；je-aero | DJ | 200 | CONFIRMED（「an aeroderivative turbine, a power generator built using technology adapted from aircraft jet engines」） | |
| 17 | 二手比較便宜、可能比較快；但數量有限、維護、污染許可 | j011、j012；je-used | DJ | 200 | CONFIRMED（In brief「Used turbines are cheaper and potentially faster to obtain, but limited supply, maintenance issues and pollution permits remain obstacles」） | |
| 18 | 業界一家公司的執行長跟路透社說二手市場非常非常熱門；卡片引句、kicker EthosEnergy's CEO, to Reuters | j013；je-hot | DJ | 200 | CONFIRMED（「"That secondary market is very, very hot right now," EthosEnergy CEO Ana Amicarella told Reuters」；引句逐字） | |
| 19 | 第三則：據 The Verge，川普在美國電視專訪裡談到 AI 安全；卡片 risk 'can be managed' | t001；tr-lead | TV | 200 | CONFIRMED（標題「Trump's 60 Minutes interview touched on AI safety」；專訪播出日報導沒寫，旁白沒說） | |
| 20 | 想像一家大型 AI 公司的老闆接到政府的電話；內容是川普自己在節目上說的 | m001、m002；mc-scene | TV | 200 | CONFIRMED（節目設定的情境，下一句就標明出處；「大型」對「One of the big ones」） | |
| 21 | 有人被舉報用 AI 做壞事，他們很強硬地打電話過去；卡片 'Something bad with AI' | m003；mc-call | TV | 200 | CONFIRMED（「somebody was reported to us to be doing something bad with AI. We called them very strongly」） | |
| 22 | 引句：準備坐牢、晚安吻；卡片 mc-quote1 原文 | m004；mc-quote1 | TV | 200 | **CHANGED（引句）**（卡片原文逐字對。旁白中譯「準備去坐牢吧，今晚記得親一下你太太，說晚安」放在「」裡，但加了「今晚」「記得」「說晚安」，「Please」變成「記得」；任務要求引號裡照原話） | →「他說他們跟對方講：『準備去坐牢吧。請給你太太一個晚安吻。』」 |
| 23 | 節目問他，AI 主管們警告自家模型不安全 | m007；mc-ask | TV | 200 | **CHANGED（措辭）**（「Asked about AI executives' warnings about their models' safety」是「對模型安全的警告」，旁白「警告自家模型不安全」替主管們下了結論；撰稿人懷疑的一條） | →「節目問他，AI 公司的主管們對自家模型安全提出警告，他怎麼看。」 |
| 24 | AI 安全的解釋（被拿去做壞事，或出錯傷到人的風險） | m008；mc-term | — | — | CONFIRMED（解釋；一般定義，沒有超出來源，也沒有替川普下定義） | |
| 25 | 他回答：風險遠沒有他們說的那麼真實，可以管理，而且已經在管理；卡片引後半 | m009；mc-risk | TV | 200 | CONFIRMED（「the risk is not nearly as real as it– as they talk, and I think the risk can be managed, and it's managed」；卡片逐字，前面有 …） | |
| 26 | 他說在管的是美國司法部；司法部的解釋 | m010、m011；mc-doj | TV | 200 | CONFIRMED（「He claimed the DOJ is managing that risk」：這是 The Verge 對他的話的描述，他的引句裡只說「we」；旁白「他說」與卡片「he says」可接受，見〈懷疑但沒改〉） | |
| 27 | 不肯說名字和公司，只說是一家 AI 公司的負責人，「大公司之一」；卡片 One of the big ones. | m014、m015；mc-who | TV | 200 | CONFIRMED（「refused to name the person or company … the leader of an AI company, "One of the big ones."」） | |
| 28 | 被威脅要逮捕以後，「這個人完全改變了做法」；卡片 …this person totally changed everything. | m016；mc-changed | TV | 200 | **CHANGED（引句）**（「after the threat of arrest, "this person totally changed everything."」；「做法」是加上去的，放在引號裡） | 「完全改變了做法」→「完全改變了一切」 |
| 29 | 改了什麼，他沒說，報導也沒寫 | m018 | TV | 200 | CONFIRMED（TV 全文沒有） | |
| 30 | 都只是川普的說法，經 The Verge 轉述；沒有第二個來源，沒有司法部或那家公司的回應；卡片 mc-check | m019、m020、m062；mc-check、mc-unsure | TV、TRUMP | 200 | CONFIRMED（TV 全文只有這一段專訪，沒有任何回應；TRUMP callout 與 FAQ 同） | |
| 31 | 兩人的立場、規則的三件事 | m021–m029；mc-sides、mc-rules | — | — | OUT OF SCOPE（意見與節目整理，c31） | |
| 32 | 他說不介意設護欄，但不想讓美國遠遠落到第二名；卡片引句；m030「跟你很像」 | m030、m031；mc-rails | TV | 200 | CONFIRMED（「I don't mind guardrails, but I don't want to put us in a deep second position.」逐字；m030 是節目對照） | |
| 33 | 護欄的解釋；Kai「連他都說，不能因為規則跑輸」 | m032、m033；mc-rails2 | TRUMP | 200 | CONFIRMED（解釋照 TRUMP；m033 是 Kai 對 #32 的轉述，意思沒有超出原句） | |
| 34 | 他說「絕對願意」跟民主黨合作談 AI 安全；要設什麼護欄、什麼時候設報導沒提；卡片 'Absolutely would' | m034、m035、s002；mc-dems | TV | 200 | CONFIRMED（「Ross Douthat went on to ask if Trump would work with Democrats on AI safety, and Trump said he "absolutely would"」；全文沒有護欄內容或時程） | |
| 35 | 他說習近平全力投入他所謂的 SI，超級智慧；名字比較好，因為不是「人工」的；卡片引句 | m038、m039；mc-si | TV | 200 | CONFIRMED（「China's Xi is "…all in to SI, as I call it, because it really is super intelligence. It's a much better name, I think, because it's not artificial."」）；**CHANGED（語氣）**：m038 開頭「更怪的是」是節目替他的話下評語，任務要求中立 | 「更怪的是，他說」→「但這還不是全部，他還說」（保留 lint 要的鉤子） |
| 36 | 亞洲：報導只有中國，中國沒有護欄，只有習近平說了算 | m043；mc-asia | TV | 200 | **CHANGED（引述）**（撰稿人懷疑的一條。原話「China has no guardrails, by the way. […] They have the guardrails that whatever President Xi says goes.」是兩段：先說沒有護欄，再說他們的護欄就是習近平說了算。「只有習近平說了算」把第二段的「護欄」框架拿掉了。「說了算」本身是「whatever … says goes」的準確譯法） | →「報導只提到中國：川普說中國沒有護欄，他們的護欄就是習近平說了算。」 |
| 37 | 台灣報導完全沒提；卡片 Taiwan: not mentioned | m044；mc-asia | TV | 200 | CONFIRMED | |
| 38 | 報導沒有罰款、預算、具體法案或時間表 | m048、m049、m050；mc-money | TV | 200 | CONFIRMED（TV 全文沒有） | |
| 39 | 接下來看三件事 | m057–m061；mc-next | — | — | OUT OF SCOPE（節目整理，三件都對得上 #30、#34、#25） | |
| 40 | 看法與結尾 | m053–m056、m063–m066；mc-lose、mc-small、mc-kai-last、mc-view、mc-view2 | brief.md | — | OUT OF SCOPE（意見；Sola 的看法以「我的看法是」標明，與〈站主觀點〉一致） | |
| 41 | 據 Decrypt，NYSE 的新交易平台要用 Avalanche 區塊鏈來記帳；卡片 fm-intro「NYSE picks Avalanche」 | f002；fm-intro | DN | 200 | **CHANGED**（撰稿人懷疑的一條。DN 的標題與導言確實寫「NYSE Taps Avalanche」「The New York Stock Exchange is turning to Avalanche … of its forthcoming tokenized securities platform」，但宣布的是 Ava Labs（「Ava Labs, the company behind Avalanche, said Monday」），NYSE 沒有自己的公告，平台是「NYSE-affiliated」、還在規劃（待核准），用 Avalanche 的是平台背後的清算公司。卡片沒有掛名，把 Ava Labs 的說法寫成 NYSE 的決定。旁白「紐約證券交易所，也就是 NYSE 的新交易平台」也會聽成「NYSE＝新交易平台」） | 卡片 →「Avalanche for an / **NYSE-linked venue**」，key →「Avalanche for NYSE venue」；f002 →「據 Decrypt，紐約證券交易所 NYSE 規劃中的新平台，要用一條叫 Avalanche 的區塊鏈來記帳。」（「its forthcoming」） |
| 42 | 重要是區塊鏈放進股票買賣最後完成的那一層，Decrypt 叫它管線；卡片 The plumbing | f003；fm-why | DN | 200 | CONFIRMED（「puts a blockchain underneath the clearing and settlement layer, the plumbing that finalizes trades」） | |
| 43 | 成交、清算、結算三步；網購類比 | f005–f009；fm-steps、fm-shop | NYSE | 200 | CONFIRMED（解釋照 NYSE callout；網購是類比） | |
| 44 | Avalanche 背後的公司說，它會是這個平台清算公司的核心帳本；卡片 kicker Ava Labs says | f011；fm-ledger | DN | 200 | CONFIRMED（「"core ledger technology" for the clearing firm」；旁白「核心帳本」少了「技術」，意思沒變） | |
| 45 | 帳本、區塊鏈、代幣化的解釋 | f013、f041、f014；fm-terms | DN、NYSE | 200 | CONFIRMED（代幣化照 DN「issuing traditional assets as blockchain-based tokens」；區塊鏈是一般解釋） | |
| 46 | 平台要交易的是代幣化證券 | f016；fm-same | DN | 200 | CONFIRMED（「tokenized securities platform」） | |
| 47 | 設計目標全天候交易、清算和結算，要先等監管核准；卡片 24/7 pending approval | f017；fm-247 | DN | 200 | CONFIRMED（「designed to allow 24/7 trading, clearing and settlement … subject to regulatory approval」；上線時間沒寫，f019 沒有新日期） | |
| 48 | NYSE 數位發行主管：替每項工作挑合適的技術；支援好幾條區塊鏈上市的股票，帳本要快、可靠、能控管誰參與；卡片 Dennis Lee | f020–f023；fm-quote、fm-needs | DN | 200 | CONFIRMED（「Dennis Lee, the NYSE's head of digital issuance … "picking the right technology for each job" … fast, reliable and able to control who participates」；引句逐字） | |
| 49 | Decrypt 說這是華爾街最老牌的機構把核心設施搬上公有區塊鏈的跡象 | f026；fm-sign | DN | 200 | CONFIRMED（「one of the clearest signs yet that Wall Street's oldest institutions are moving core market infrastructure onto public blockchains」） | |
| 50 | 這筆合作誰付誰多少錢，報導沒寫 | f027；fm-pipes | DN | 200 | CONFIRMED（DN 沒有任何金額） | |
| 51 | 母公司 ICE 跟 OKX 另外在規劃一個代幣化股票平台；卡片 OKX-ICE venue: planned | f029；fm-catch | DN | 200 | CONFIRMED／**CHANGED（措辭）**（「ICE and crypto exchange OKX are planning a 24/7 tokenized stock venue」「the NYSE's parent Intercontinental Exchange」；「母公司 ICE」沒說是誰的母公司） | →「第一，NYSE 的母公司 ICE 跟加密貨幣交易所 OKX，另外在規劃一個代幣化股票平台。」 |
| 52 | 美股七巨頭，就是七家最大的科技公司，包括 Apple 和 Meta，全都選擇不讓股票在那裡被代幣化；卡片 Big Tech opted out there | f036；fm-catch | DN | 200 | **CHANGED（解釋）**（「Every Magnificent Seven stock, including Apple and Meta, opted out」對；但 Magnificent Seven 是市場慣稱，不是市值前七大，「七家最大的」是新的事實主張） | →「美股七巨頭，是七家大型科技公司的統稱，包括 Apple 和 Meta，都選擇不讓股票在那裡代幣化。」 |
| 53 | 「67 家公司」沒有念 | — | DN、NYSE | 200 | CONFIRMED（撰稿人懷疑的一條。DN「with 67 companies in all joining them」可讀成「連七巨頭在內一共 67 家」或「另有 67 家」，NYSE 站上文章寫成「另有 67 家公司也選擇退出」。來源本身含糊，不念比念錯好；不念也不會讓聽眾以為只有七巨頭退出，因為旁白沒說「只有」） | |
| 54 | 國際貨幣基金的研究：代幣化股票的需求是真的，但不平均；卡片 Per an IMF study | f030；fm-imf | DN | 200 | CONFIRMED（「Research shows the appetite for tokenized stocks is real but uneven. An IMF study found tokenized stocks show genuine demand」；嚴格說「不平均」是 Decrypt 的概括，IMF 研究說的是「genuine demand yet remain volatile and illiquid」，見〈懷疑但沒改〉） | |
| 55 | Decrypt 的提醒：管線蓋好可能比需求跟上還快 | f032；fm-early | DN | 200 | CONFIRMED（「the infrastructure may be arriving faster than the markets to fill it」） | |
| 56 | 不是投資建議，也不推薦任何代幣或平台 | f035；fm-note、description | — | — | CONFIRMED（節目聲明） | |
| 57 | Sign-off：最重要、最不確定、節目的建議 | s001–s003；so-take、so-tip | AV | 200 | CONFIRMED（s003 標明是「節目的建議」，依據 #7、#9） | |
| 58 | Mokaair 網站的完整整理；說明欄四個網址 | s006；so-site、description | 站上 4 篇 | 200 | CONFIRMED（四個網址都 200、published） | |
| 59 | 說明欄：AI 合成語音、AI 配樂、內容依官方來源與媒體報導整理；司法部警告是他本人的說法，沒有第二個來源，也沒有司法部或當事公司的回應；Follow the Money 不構成投資建議 | youtube.description | TV、DN | 200 | CONFIRMED | |
| 60 | tags、標題「Tech Signal 11/10｜Trump on AI safety and a jail warning」、縮圖「Jail threat?」「Trump on AI safety, 60 Minutes」 | youtube.title、tags、thumbnail | TV | 200 | CONFIRMED（「a jail warning」與「Jail threat?」都是他自述的警告；問號保留不確定） | |
| 61 | 章節名四個 | intro、mc-scene、fm-intro、so-take | — | — | CONFIRMED（「股票的帳本搬上區塊鏈」：平台還在規劃、待核准，章節名用的是方向，不是已上線；見〈懷疑但沒改〉） | |
| 62 | outro：答案、留言題、訂閱 | o001–o003；outro | — | — | OUT OF SCOPE（意見；三句） | |

## 笑點檢查

逐句看 claims.md〈笑點〉列的每一句，加上卡片上接梗的字。六條標準：暗示來源沒有的事實、新的數字、替真人編話、打一般人、黨派立場而不是笑政策本身、雙關或諧音。

| # | 笑點 | 位置 | 判定 | 理由 | 修改前 → 修改後 |
| --- | --- | --- | --- | --- | --- |
| 1 | 「一家人什麼都能分，就這包 AI 不能分？」 | a010 | **留** | 接 #9；笑的是 Apple 的規則。 | |
| 2 | 「打個比方，就像計程車跳表，聊得越複雜，跳得越快。」（撰稿人不確定的 a012） | a012 | **改** | 計程車跳表是邊坐邊收錢，聽的人會以為 Apple 按對話計費。實際是買一包固定額度，聊得越複雜用得越快、越早用完（#6、#10）。換成同樣是生活例子、又有「上限＋可以加買」結構的手機流量。 | →「打個比方，就像手機流量，聊得越複雜，掉得越快。」 |
| 3 | 「原來跟 AI 講話，要講簡單一點才省錢！」 | a013；ap-joke | **留** | Kai 的推論，從「越複雜、用越多」推到少買用量包，方向對；明顯是誇張。 | |
| 4 | 「所以我要不要換手機？」×2；「不用，這次要你掏錢的不是手機，是 AI 的額度」「不用，今天連資料中心都在找二手的」 | a015、a016、j015、j016 | **留** | 固定梗；a016 的「掏錢」是自願加買，接 #5 改過的說法，不衝突。 | |
| 5 | 「打個比方，就像小一的時候下訂，小六畢業才送到。」 | j007；je-joke、s004 | **留** | 小學六年對六年，沒有新數字；卡片英文「grade one … graduation」沒寫年數。 | |
| 6 | 「等到交貨，資料中心裡的晶片都要過時了吧！」（撰稿人不確定的 j008） | j008 | **留** | 「吧」是猜測，誇張的反應，沒有數字，不會被當成報導內容；AI 晶片換代快是一般常識，笑的是交貨時間，不是任何人。 | |
| 7 | 「好，叫人準備坐牢算保護還是嚇人，現在可以吵了。」 | t002 | **留** | 串場。 | |
| 8 | 「連晚安吻都幫人家安排好了？」 | m005 | **留** | 接 #22 的原話，笑的是有權力的人說的話；m004 改成直譯「請給你太太一個晚安吻」以後，這句接得更直接。 | |
| 9 | 「所以風險沒那麼真實，可是已經真實到，要打電話叫人準備坐牢。」「所以風險到底是有，還是沒有？」 | m012、m013；mc-joke1 | **留旁白，改卡片** | 兩半都是他自己的話（#25、#21–#22），笑的是說法前後對不上，不說他說謊。卡片「real enough for jail」單獨看會讀成有人坐牢。 | 卡片 →「Not that real, / **yet a jail warning**」 |
| 10 | 「有用？我看是把人嚇到不敢動吧。」 | m017 | **留** | Kai 的意見，m018 立刻說改了什麼沒人知道。 | |
| 11 | 「打個比方，就像考試範圍還沒公布，老師已經先打電話說你會被當。」「這種課，我一定第一個退選！」（撰稿人不確定的 m036） | m036、m037；mc-joke2 | **留** | 兩邊的事實都在來源裡：護欄內容與時程沒說（#34），警告電話是他說的（#21–#22）。笑的是「規則還沒寫、警告先到」的順序，沒提政黨、沒評價川普本人或支持者；前一句剛講他「絕對願意」跟民主黨合作，這個梗也不是在替哪一黨說話。類比沒有說那位老闆沒做錯事，所以不暗示來源沒有的事實。 | |
| 12 | 「身為一個 AI 主持人，我得承認，我就是人工的。」「我也是，至少我們的名字很誠實。」（撰稿人不確定的 m040／m041） | m040、m041；mc-joke3 | **留，m041 措辭改** | 笑點打在主持人自己身上（說明欄揭露兩位是 AI 合成語音），沒有笑川普的用詞；「人工」是 artificial 的字面意思，不是諧音，八語的 AI 全名都有「人工／artificial」，翻得過去。但「我們的名字」會聽成 Sola、Kai 這兩個名字，梗就斷了。 | m041 →「我也是，至少 AI 這個名字，用在我們身上很誠實。」 |
| 13 | 「所以這場 AI 安全的談話，到目前為止唯一的成本，是一通電話。」「而且那通電話，還沒人證實有打過。」（撰稿人不確定的 m051） | m051、m052；mc-cost | **改** | 「唯一的成本」把「報導沒寫」說成「沒有」，是來源沒有的事實；卡片「The policy's cost」把一段專訪說成政策。m052「還沒人證實有打過」漏了川普本人就是說有打的人。沒有新數字、不是雙關。 | m051 →「所以照報導，這場談話到目前為止唯一的成本，是一通電話。」；m052 →「而且那通電話，除了他自己，沒人證實過。」；卡片 →「Cost in the report: / **one phone call**」 |
| 14 | 「第一件，我賭會有很多公關在開會。」 | m059 | **留** | 猜想，不指任何公司。 | |
| 15 | 「連預算都沒有？」 | m068 | **留** | 反應。 | |
| 16 | 「所以 Avalanche，是在幫股票送包裹？」 | f010 | **留** | 想歪，f011 立刻更正。 | |
| 17 | 「交易終於不用下班了！」「監管機關還沒點頭之前，它連第一天上班都還沒排。」 | f018、f019；fm-kai | **留** | 接 #47，擬人，沒有新日期。 | |
| 18 | 「那錢流去哪？」「所以今天跟的不是錢，是錢走的管線。」 | f024、f025；fm-pipes | **留** | 接 #50、#42。 | |
| 19 | 「Apple 今天出場兩次，一次在賣 AI 加量包，一次在拒絕被代幣化。」（撰稿人不確定的 f031） | f031；fm-apple | **改** | 兩件事都是本集講過的事實（#4、#52），但 DN 沒寫七巨頭退出 OKX-ICE 平台的日期，不是 11/9 的新聞；「今天」會聽成同一天發生，卡片「twice today」英文更明顯。「拒絕」對「opted out」可以接受。 | f031「今天」→「這一集」；卡片「Apple, twice today:」→「Apple, on air twice:」 |
| 20 | 「打個比方，就像捷運站先蓋好了，乘客還在路上。」「我還是覺得先蓋好比較好。」 | f033、f034；fm-early、fm-kai2 | **留** | 類比接 #55；Kai 的意見，不是投資看法。 | |
| 21 | 「今天最有耐心的，是在等新渦輪機的資料中心，小一下訂，小六才到貨。」 | s004；so-call | **留** | 回扣 #5。 | |
| 22 | 「等它到貨，我的老問題，應該已經問了好幾百次。」 | s005 | **改** | 「好幾百次」是一個新的數量，而且算不對（平日一集、六年是上千集）。 | →「等它到貨，我的老問題，大家應該都會背了。」 |
| 23 | 卡片 Kai: dumb it down?、Proudly artificial、Rules TBA, warnings sent | ap-joke、mc-joke3、mc-joke2 | **留** | 都有 kicker 標明是誰的反應或類比。 | |

笑點總計：23 項，留 17 項，改 6 項（a012、mc-joke1 卡片、m041 措辭、m051／m052 與卡片、f031 與卡片、s005），刪 0 項。全片沒有雙關或諧音；改完沒有新的數字、沒有替真人編的引句（m004、m016 兩處引號裡的中譯改成直譯）、沒有打一般人的笑點；Main Course 的笑點都打在說法與政策順序上，不打政黨或支持者。

## 清楚度檢查

照 daily-brief.md §一之〇。

- 句子完整性檢查（任務給的 node 指令，含 key 長度與 keys 數量）：修改前 0 行，修改後 0 行。`big`、`quote`、`outro` 都沒有 `reveal`；所有 `key`／`keys` ≤24 字（新的 fm-intro key「Avalanche for NYSE venue」正好 24）；改過的 big 卡每行 ≤22 字。
- 每則前兩句：
  - Apple：a001 說發生了什麼，a002 說為什麼跟你有關（有上限、用完可以加買）。符合。
  - 噴射引擎：j001 發生什麼，j002 原因。符合。
  - 川普：t001／hk01 先說發生什麼，q001 帶出跟一般人的關係；主菜 m001–m004 從場景講起。符合。
  - NYSE：f002 原本「紐約證券交易所，也就是 NYSE 的新交易平台」會聽成「NYSE 就是新交易平台」，改成「紐約證券交易所 NYSE 規劃中的新平台」；f003 說為什麼重要。
- 生字第一次出現就解釋：雲端模型、燃氣渦輪機、AI 安全、司法部、護欄、清算、結算、帳本、區塊鏈、代幣化、美股七巨頭都有解釋。「航空衍生渦輪機」旁白沒用，改說「拿噴射引擎技術改成發電機」。「SI」m038 當場說「超級智慧」。
- 不往回指：f029「母公司 ICE」沒說是誰的母公司，補成「NYSE 的母公司 ICE」；m041「我們的名字」改成「AI 這個名字」。s002 重說「他說要跟民主黨談的護欄」，沒有寫「剛剛那個」。
- 出處短講：每則一次（據 The Verge、據 Decrypt）；Decrypt 在 NYSE 段多次出現，是為了把評論（管線、跡象、提醒）標成 Decrypt 的看法，不是轉引鏈。
- 一句一件事：沒有一句同時塞兩個數字和兩個名字。

畫面狀態：改完後用 lint 的估計時間軸（`tools/video/core/timeline.mjs` 的 `estimateTimeline` 加 `cadence.mjs` 的 `slideStates`）重算。第一版改動讓 mc-asia 14.8、fm-intro 14.1、ap-complex 13.3、mc-cost 13.3 秒超過，已縮短 m043、f002、a012、m051、m052；改完全片最長 12.9 秒（mc-asia，與原稿相同），其次 12.8（ap-first、tr-lead）、12.7（mc-changed）；outro 12.3 秒（沒動，三句）。拿掉 m038 的「更怪的是」後 lint 報 05:36–07:07 沒有鉤子，換成中性的「但這還不是全部」，警告消失。

## 摘要

- 查了 62 條（同一事實在多處出現時合為一條）加 23 項笑點：CONFIRMED 46、CHANGED 10（#5、#6、#22、#23、#28、#35、#36、#41、#51、#52，含措辭、引句與卡片）、NOT FOUND 0、OUT OF SCOPE 6（#3、#11、#31、#39、#40、#62）。笑點表裡另有一處帶事實的改動（#13，m051／m052 與卡片），合計事實改動 11 處。
- 事實改動 11 處：(1) a002 用完「要付錢才能繼續用」→「可以付錢加買來繼續用」；(2) a005「一次買斷」→「單次購買」（12 個月過期）；(3) m004 引號裡的中譯照原話直譯；(4) m007「警告自家模型不安全」→「對自家模型安全提出警告」；(5) m016 引號裡「改變了做法」→「改變了一切」；(6) m038「更怪的是」→「但這還不是全部」（語氣中立）；(7) m043 習近平那句照原話分兩段；(8) fm-intro 卡片「NYSE picks Avalanche」→「Avalanche for an NYSE-linked venue」，f002 補「規劃中」並修好斷句；(9) f029 補「NYSE 的」母公司；(10) f036 七巨頭「七家最大的」→「七家大型科技公司的統稱」；(11) 笑點裡帶事實的兩處：m051／m052「照報導」「除了他自己」與 mc-cost、mc-joke1 兩張卡片。
- 撰稿人的三個疑問：fm-intro 改（#41，Ava Labs 宣布、平台是 NYSE 關聯、還在規劃）；「只有習近平說了算」改（#36，「說了算」本身準確，但要保留他說那就是中國的護欄）；「67 家公司」維持不念（#53，來源含糊、站上文章的讀法不一定對）。另外的 m007 也改了（#23）。
- 笑點：改 6 項，刪 0 項。撰稿人的疑問：a012 改（跳表→手機流量）；m040 留、m041 措辭改；m036 留（笑政策順序，不是黨派）；f031 改（今天→這一集）；m051 改（照報導、不說成沒有）；j008 留。另改 s005（拿掉「好幾百次」）與 mc-joke1 卡片。
- 川普的引述：每一句都標成「他說」「他回答」「川普自己的說法」；卡片引句（mc-quote1、mc-risk、mc-who、mc-changed、mc-rails、mc-si）逐字對過 TV；旁白引號裡的中譯（m004、m016）改成直譯；說明欄與 m019／m020／m062 都說明沒有第二個來源與回應。節目沒有說電話是真的或假的。
- 唸出來的日期：11 月 10 日星期二、11 月 9 日（四則的報導日）。旁白沒有說專訪的播出日、Apple 用量包的上市日或 NYSE 平台的上線日，都對。
- `sources` 4 個網址 2026-11-10 重開全部 HTTP 200，內容與撰稿人 2026-11-09 引的相同；`checked_on` 維持 2026-11-09（沒有數字改動）。
- 會過期的事實：Apple 用量包目前只有 Logic Pro、預計本月加到其他 App（AV 2026-11-09，旁白沒念後半）；NYSE／Avalanche 平台待監管核准、上線時間未定（DN 2026-11-09）；六年交貨是 Wood Mackenzie 的平均（DJ 2026-11-09）；川普那通電話是否有人證實（TV 2026-11-09）。
- 觀點：m065、m066 以「我的看法是」標明，s001、s002 以「說一句真心話」「我最不確定的」標明，m062 以「我不知道」標明，s003 以「節目的建議」標明，與 brief.md〈站主觀點〉一致。沒有不一致。
- 聽眾檢查（只報告）：lint 改完沒有再報超過 40 字的句子（f002、f036 第一版改動曾到 41、42，已縮短）。沒有「經查證」「根據官方文件」「本影片」、括號或網址；揭曉都在介紹句之後。本輪沒有新增字典外的拉丁詞（NYSE、Avalanche、AI、Apple、Meta、ICE、OKX 都是原稿就有的）。
- lint：`node tools/video/cli.mjs lint --slug daily-ai-20261110` → `daily-ai-20261110: 0 errors, 1 warnings`（開場章節長度：本節目沒有開場濃縮，照 daily-brief.md 不理）；估 13.7 分鐘，151 句。
- 懷疑但沒改：
  - m010「他說，在管的是美國司法部」：川普的引句只說「we」，「DOJ」是 The Verge 的描述（「He claimed the DOJ is managing that risk」「Trump claims the DOJ told」）。旁白「他說」照 The Verge 的寫法，沒改；第 2 輪可以考慮改成「據 The Verge，他的意思是……」。
  - f030「需求是真的，但不平均」：「uneven」是 Decrypt 的概括，IMF 研究本身說的是需求真實但波動大、流動性不足（後半撰稿人刻意不念，因為太接近價格）。卡片 kicker「Per an IMF study」可能讓人以為「uneven」是 IMF 的用字，沒改。
  - 章節名「股票的帳本搬上區塊鏈」：平台待核准、還沒上線；章節名講的是方向，f017、f019 有說要等核准，沒改。
  - 站上 NYSE 文章把「with 67 companies in all joining them」寫成「另有 67 家公司也選擇退出」，原文可能是一共 67 家；不影響本片（沒念），但站上文章可能要另外看。
  - mc-quote1 的 kicker「Trump on 60 Minutes」與 key「Trump: 'go to jail'」：引句是他轉述「我們」對那位老闆說的話，卡片沒寫「他轉述」；字面上是他在節目上說的話，沒改。
- 需要第二輪：**是**。本輪改了 11 個事實（超過 3 個）。所有主張都已判定，沒有懸而未決的。
