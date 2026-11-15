# curio-w01-dolby-licensing 查核第二輪

- 查核日：2026-11-08
- 查核者：獨立查核代理（Claude Opus 5.5），沒有參與寫稿，也沒有做第一輪。
- 對象：目前的 `video.json`（`scenes[].lines` t001–t152 共 152 句旁白、`youtube.title`、`thumbnail`、`youtube.description`、`sources`）與全部 `scenes[].data.prompt`。`verify-1.md` 查的是改寫前的稿，這輪只拿它的來源清單與判定當線索，每句重新對原件。
- lint：`node tools/video/cli.mjs lint --slug curio-w01-dolby-licensing` → 0 errors, 0 warnings，估 13.6 分鐘、152 句。

## 結論

**有條件通過。** 錯誤 0、過強 1、NOT FOUND 0。

新寫的幾句都查得到：1949 年 16 歲的加州高中生、偶遇後進磁帶錄音機公司、週末和假日打工（OAC＋IEEE）；「第一筆生意賣的是自己造的機器」（OAC 寫迪卡是第一個客戶，年表寫 A301 是第一個產品，1966 年 4 月交第一批量產機，ETHW 寫公司自己造 A 型）；「年報到今天還寫著：得一直說服別人」（2025 財年 10-K 風險因素「We must continually convince mobile device OEMs」，2026 財年 10-K 要 2026-11-17 才出，所以「到今天」站得住）。

上架前要改的：

1. **t128** 拿 2023 財年當起點，配的卻是年報解釋 2025 比 2024 的理由；「兩點」也是四捨五入後的差（實算 20.4% → 21.5%，約 1.2 點）。
2. **t042**「亨利·克洛斯」是英文人名的中文音譯，不合系列規則（英文名照原文念，台灣沒有慣用的正式中文名）。這不是事實錯誤，但 QA 會擋。

其他列都是「可接受」，改不改由撰稿者決定。畫面規則通過：沒有一個提示詞畫出 Ray Dolby、Henry Kloss、庫柏力克或任何主管本人，也沒有畫代表他們的路人。

## 問題清單

| line id | 問題 | 現在的句子 | 建議改法 | 判定 |
|---|---|---|---|---|
| t128 | 年報 MD&A 說手機授權收入增加，是因為 GE Licensing 收購帶進影像專利收入，加上音訊專利最低量合約的入帳時間。這段解釋的是 2025 對 2024 財年（20% → 22%），旁白卻接在 2023 財年後面。2023 財年手機實算 20.36%，2025 財年 21.52%，差約 1.2 點，「兩點」是四捨五入後相減的結果 | 電視在往下掉；手機多出來的兩點，年報說來自收購和合約入帳的時間。 | 電視在往下掉；手機這一年回升，年報說是因為收購和合約入帳的時間。 | 過強 |
| t042 | 系列規則是英文名照原文念，只有台灣慣用的正式中文名例外。Henry Kloss 沒有通行的中文名。事實本身沒錯（OAC、年表、ETHW） | 這位廠商叫亨利·克洛斯，他催著要一套給一般家庭用的降噪。 | 這位廠商叫 Henry Kloss，他催著要一套給一般家庭用的降噪。 | 可接受（規則，要改） |
| t137 | t116 說九成三精確是九成二點五，這裡的百分之七其實是 7.495%（101,113／1,349,130）。兩句加起來是 99.5%，細心的觀眾會算。年報本身就列 7%，所以不算錯 | 授權費以外，還有百分之七是產品與服務，大約一億美元。這一億是什麼？ | 授權費以外，年報列百分之七是產品與服務，大約一億美元。這一億是什麼？ | 可接受 |
| t062–t064 | 日期對：申請 1969-10-20，核准 1971-12-28。新的發現是 Google Patents 顯示 US3631365 主張 1968-11-01 英國申請（GB3646669）的優先權，全文還引 Ser. No. 569,615 為前案，所以「阿富汗那封信變成這份專利」比 OAC 寫的更間接。旁白已標「典藏說明寫」，也加了「前面還有更早的申請」，可以不改 | 典藏說明寫，它變成了一份美國專利，／一九六九年申請，一九七一年底才核准。 | 維持；如果要更穩，t062 改成「典藏說明寫，它後來連到一份美國專利，」 | 可接受 |
| t075 | 沒有來源直接寫 1971 年還沒有這個名字。年表第一次出現「Dolby Stereo」是 1974 年 11 月，ETHW 寫 1975 年推出，所以推論合理，只是「根本」講得比來源滿 | 杜比立體聲這個名字，那時候根本還沒出現。 | 杜比立體聲這個名字，那時候都還沒推出。 | 可接受 |
| t006 | FCC ¶23 只寫 DTS 與杜比「sharply differ」，而且只在這個程序裡。「一直」沒有來源 | 一九九六年平安夜，美國要定數位電視的聲音，還有一家公司一直反對它。 | 一九九六年平安夜，美國要定數位電視的聲音，還有一家公司站出來反對它。 | 可接受 |
| t010 | IEEE（1988 專訪稿）寫 Poniatoff 請他「weekends and vacations」來工作，對得上；OAC 另外寫他之後「full-time when he could and part-time when in school」，做了八年。旁白講的是起頭，所以沒錯 | 一次偶遇，他進了一家做磁帶錄音機的公司，週末和假日去打工。 | 維持 | 可接受 |
| t026 | OAC 沒寫開車回英國是哪幾個月，只寫 1965 年、兩個月，又說 1965 年 5 月開公司。「同一年五月」暗示開車在五月以前，與來源不衝突，只是沒寫明 | 同一年五月，他在倫敦開了公司。 | 維持 | 可接受 |
| t035 | OAC 寫「After months of testing」。年表是 1965 年 11 月示範、1966 年 1 月訂貨，看起來只有兩個月左右。「好幾個月」照 OAC，可以不改。「迪卡」是常見譯名，要不要改念 Decca 交給念法審查 | 是迪卡唱片。測了好幾個月，訂下最早的九台，還要三個月獨家。 | 維持（或「測了幾個月」） | 可接受 |
| t019 | OAC 的原文是既有的 companders（壓縮擴展器），「市面上的設備」範圍比較大 | 市面上的設備他研究過，加進去的失真，比去掉的噪音還多。 | 市面上的降噪設備他研究過，加進去的失真，比去掉的噪音還多。 | 可接受 |
| t084、t087、t092 | 念法：`say` 寫成「A C 三」，數字用中文念。系列規則是英文名照原文念，念法交給念法審查，不是事實問題 | （`say`）…又叫 A C 三。 | 交念法審查決定念「A C three」或維持 | 可接受 |

## 逐句判定（t001–t152）

這裡寫「站得住」的列，對到的是〈開過的來源〉裡這輪親自開過的原件。沒列進問題清單的事實句都站得住。

| 行 | 主張 | 原件與數字 |
|---|---|---|
| t001–t003 | 每賣一台付一筆；13.49 億美元；九成三 | 10-K「typically enter into a per unit royalty arrangement」；R56 總營收 1,349,130、授權 1,248,017（千美元）。實算 92.505%，列 93.00% |
| t004、t036、t048、t141、t142 | 流傳的「不造硬體只賣專利」，以及半句對、半句錯 | 標成「你可能聽過」。ETHW「manufactured Dolby A units」；10-K 產品段落、「We do not manufacture these ICs」 |
| t005、t033、t040 | 第一筆生意賣的是自己造的機器 | OAC「Decca Records was Dolby's first customer」；年表 1966-01 訂九台 A301、1966-04「First production A301 units delivered」、A301 是「first product」；ETHW「The company manufactured Dolby A units」 |
| t006、t086–t094 | 平安夜、DTS 的主張、杜比的回應、三個理由 | FCC 96-493：Adopted December 24, 1996；¶23（exclude audio formats；not demonstrated superior；unnecessary cost and complexity）；¶51（did not go through the extensive testing … where the Dolby system prevailed；no independent testing；could delay；additional costs） |
| t007、t106、t130–t132 | 年報寫手機通常沒有標準撐腰，得一直說服，拿掉比較容易 | 10-K「usually are not mandated」「We must continually convince mobile device OEMs」「easier for mobile device OEMs to add or remove」；2026 財年財報 2026-11-17 才發布 |
| t009–t011、t018 | 1949、16 歲、加州高中生、偶遇、磁帶錄音機公司、從那時起想對付嘶聲 | OAC「In 1949, as a 16-year-old student at Sequoia High School in Redwood City … chance encounter … Ampex … the first U.S.-made professional audio tape recorder」「intrigued him since his time at Ampex」；IEEE「weekends and vacations」 |
| t013、t015–t017 | 錄影機電子部分、劍橋物理博士、1963 印度 UNESCO、嗜好錄現場音樂 | OAC：1952–57「mainly responsible … world's first practical video tape recorder」、1961 PhD in physics、1963 UNESCO technical adviser、錄 local musical performances |
| t020、t022 | 嘶聲只在小聲時聽得到，大聲的原樣放過 | OAC「only audible on quiet passages」「letting the loud sounds pass through undisturbed」 |
| t023–t025 | 1965、陸路兩個月、阿富汗、寄給加州專利律師 | OAC「two-month overland drive back to the UK … a stop in Afghanistan to write up his ideas and send them to Paul Flehr, his patent attorney in California」 |
| t027、t028 | 1988 專訪：成衣工廠一角、兩萬五千美元、四個員工 | IEEE「corner of a London dressmaking factory. He had $25,000 he had saved and borrowed, and four employees」（記者的敘述，旁白標「照他接受專訪的說法」）；年表「staff of four」 |
| t029–t032 | 黑白影像降噪、BBC 沒要、A 型金屬盒 | OAC「monochrome video noise reduction … BBC … converting to color」；ETHW「compact metal case. It was not a recording machine」 |
| t034 | 賣給英美錄音室 | ETHW「primarily to recording studios in England and the United States」；年表 1966-67 美國首批售出 |
| t037–t039 | 訊噪比伸展器、被叫成杜比、連他自己都意外、品牌也收錢 | IEEE「S/N (signal-to-noise) Stretchers … much to his surprise」；10-K「licensing technology, our brand, and patents」 |
| t041–t043、t047 | 1967 克洛斯催做家用版、B 型、賣設計、自己只造專業機 | OAC「at the urging of」；年表 1967-04「Negotiations begun on licensing」；ETHW「sold the plans for the technology」 |
| t049 | 我讀到的紀錄都沒寫為什麼 | OAC、IEEE、ETHW、年表都只寫做法，沒寫動機（只到讀過的範圍） |
| t051–t052 | KLH 1968 開盤機、獨家到 1970、一般家庭沒接受 | 年表 1968-06 KLH Model 40「exclusive until 1970」；ETHW「never enjoyed wide consumer acceptance」 |
| t055–t058 | 卡帶被看不起、加杜比追上黑膠 | ETHW「considered inferior to home reel-to-reel tape recorders and 8-track tapes」「rivaled LP records」（單一來源，t056 有標「工程史的紀錄寫」） |
| t059–t061 | 1970 年卡帶機、馬上紅、申請變多、九月第五家、隔年底三十家 | OAC「became popular immediately … multiplied」；年表 1970 夏首批卡帶機、1970-09「Fifth company, Revox」、1971「30 licensees by end of year」 |
| t067 | 工程師學會的雜誌：幾乎每家卡帶機廠商都授權 | IEEE 1988「Just about every manufacturer of audio cassette recorders licenses Dolby noise reduction technology」 |
| t071–t074 | 《發條橘子》、1971、只在混音與母帶、拷貝用傳統光學聲軌 | OAC；年表 1971-12「first film to use Dolby noise reduction on all pre-mixes and masters … conventional optical soundtrack」 |
| t077 | 第一部 1975，第一部帶環繞是 1976《星夢淚痕》 | 年表 1975-09「First feature film for general release with Dolby Stereo optical soundtrack, Lisztomania, completed」、1976 春 A Star Is Born；OAC 同 |
| t078–t080 | 先裝大戲院，《星際大戰》讓小戲院第一次裝立體聲 | Wikipedia Dolby Stereo「installed mainly in larger theaters already equipped with amplifiers and speakers … encouraged owners of smaller theaters to install stereo equipment for the first time」（單一來源）；年表 46 家戲院 |
| t081、t083、t084 | 加機器和新喇叭、不到十年六千家、1992、5+1、AC-3 | ETHW「a Dolby unit and new loudspeakers」；OAC「fewer than ten years, 6,000 cinemas」「five main audio channels … and one subwoofer channel」；年表 1992-06《蝙蝠俠大顯神威》、AC-3 |
| t096–t098 | 合理、非歧視；費率常得壓低、不一定能挑對象 | FCC ¶55「premised on reasonable and nondiscriminatory licensing of relevant patents」；10-K「must often limit the royalty rates … may be unable to limit to whom」 |
| t101–t105 | 只管美國地面數位電視；發射與接收；不管全世界、手機，也沒寫要付錢 | 47 CFR §73.682(d)(1)(i) ATSC A/52；§15.117(b)「capable of adequately receiving」；§15.117(i)(2) 明文排除不能收電視的手機；FCC 96-493 全文 royalt 0 處 |
| t107–t112 | 兩段授權、核可、象徵性初始費、OEM 授權後才能買晶片、約一千家 | 10-K「Licensing usually occurs in two stages」「once approved by Dolby」「nominal initial fee」「authorized to purchase chips」「approximately 1,000 consumer electronics manufacturers」 |
| t114–t116 | 沒公布單台授權費；九成三四捨五入、精確是九成二點五 | 10-K 搜 per unit／per device／cents，沒有任何金額；1,248,017／1,349,130 = 92.505% |
| t117–t118 | 2024 年十億、兩億、九千萬；越多越便宜；汽車 > 電視 > 手機 | 10-K「over one billion mobile devices, approximately 200 million TVs … approximately 90 million cars」「Higher volumes generally equate to lower prices」「ARPU for cars is higher than ARPU for TVs, which is higher than ARPU for mobile phones」 |
| t119–t121 | 專利池、不掛杜比品牌 | 10-K「patent licensing solutions are not Dolby-branded … patent pool」；AAC、HEVC |
| t122–t127 | 十二億多；電視與機上盒 34%；手機與平板 22%；2023 財年 38%、20% | R56／10-K：Broadcast 428,471（實算 34.33%）、Mobile 268,568（21.52%）；FY2023 451,719／1,197,930 = 37.71%、243,897 = 20.36% |
| t129 | 廣播標準的重要性下降 | 10-K「gradually diminishing over the recent years」 |
| t134–t135 | 先讓內容用它；2021 年 Apple Music 加入支援杜比全景聲的空間音訊 | 10-K（Atmos／Vision 內容是 OEM 授權的誘因；「Dolby Atmos is included in Apple Music」）；Apple Newsroom 2021-05-17「Spatial Audio with support for Dolby Atmos」，六月上線 |
| t137–t140 | 7%、約一億、戲院伺服器／處理器／擴大機／喇叭、主要靠代工 | R56 101,113；10-K「primarily for the cinema」、servers、audio processors；「rely primarily upon contract manufacturers」。另含 Dolby OptiView 的收入，所以旁白的「主要」是必要的 |
| t143–t148 | 不是憑一條法律或一張專利；我的解讀 | 標成「我的解讀」。法律只管美國地面電視（上列），手機沒有強制標準（10-K） |
| 其他 | t008、t012、t014、t021、t044–t046、t050、t053–t054、t057、t063、t065–t066、t068–t070、t076、t082、t085、t095、t099–t100、t113、t133、t136、t149–t152 | 問句、比喻、玩笑、承上啟下或標明「我覺得」，沒有要查的新事實 |

## 標題、縮圖、說明欄

- **標題**「杜比不造電視也不造手機，憑什麼 93% 的錢都是授權費？｜奇聞檔案局」：站得住。93.00% 是年報列的比例，「的錢」指營收，片中 t115–t116 講清楚了。
- **縮圖**「杜比／93% 授權／不造電視也不造手機」：可接受。「93% 授權」沒有分母，跟第一輪的意見相同，由站主決定。
- **說明欄**：每一句都對得上上表。「十六歲就在磁帶錄音機公司打工」對 OAC 與 IEEE；「1967 年家用版決定不自己造」對年表 1967-04 開始談授權與 ETHW；「1996 年平安夜 FCC 把 AC-3 寫進美國地面數位電視標準」對 FCC 96-493 與 §73.682；「2026 年 11 月 17 日才發布」對杜比 2026-10-12 新聞稿；「截至 2025 年 9 月 26 日」對 R56。「杜比進電影，第一部就是庫柏力克的片」被當成流傳的版本，其實字面是真的（OAC、年表），說明欄緊接著用「只在混音與母帶用降噪」補上限定，可以接受。`資料截至 2026-10-31` 不必改，因為來源在 11-08 重開後數字沒有變。

## 提示詞（畫面規則）

- 掃過 152 景全部 `data.prompt`：沒有人名、公司名、產品名或片名。正則抓到的「ray」都是 tray、a ray of light；「apple」是蘋果（reel-klh-q）。
- **Ray Dolby（2013 年過世）沒有入畫**：1949 年只畫課桌（origin-1949）；Ampex 只畫錄音機；開車只畫車的背面（origin-drive）；阿富汗只畫信封和筆（origin-afghan）；倫敦工廠一角畫一般的裁縫女工看著角落的工作檯（london-corner），不是他。賣設計那一景只畫兩隻手（reel-plans）。
- **Henry Kloss（2002 年過世）、庫柏力克（1999 年過世）、FCC 委員與杜比主管都沒有入畫**：reel-kloss 只畫喇叭與錄音機；film-master 是空的混音室；fcc-you 是「換成你」的觀眾；late-mobile 是不指認的業務員。
- 留意一景：london-name-b（t038「連他自己都意外」）畫「兩位 1960 年代錄音師指著盒子大笑」。他們代表的是旁白說的「大家」，不是他本人的替身，可以接受。若評審覺得像在畫他，改成只畫盒子和兩隻指著它的手。
- 不算事實問題、但給撰稿者參考：Ada 的 `characters[].appearance` 寫「short loose black bob…mustard-yellow knit cardigan」，提示詞卻寫「wavy black bob with a side fringe」，兩者不一致。另外，`curio-episode`「誰可以入畫」要求串場角色第一次入畫前，旁白先介紹她，但 Ada 第一次出現是 open-promise（t008），旁白沒有介紹。

## claims.md 覆蓋

- **ids 已經過期**：`claims.md` 有 135 列，ids 是舊稿的 t001–t140（跳過 t006、t086、t101、t102、t111）。現稿是 t001–t152，**沒有一列的 id 對得上同一句**。例如 claims 的 t003 是阿富汗那句，現稿 t003 是營收那句。
- **內容覆蓋**：用文字前綴粗比，現稿有 89 句的意思還找得到對應列。另外 63 句是改寫或新寫的，包括 t001–t011、t022–t026、t029–t037、t061–t062、t087–t089、t107、t111、t117–t118、t126–t131、t139、t143–t146。這些句子背後的事實都還在 W01 查核表的 #1–#65 裡（上表已逐句對過），但 `claims.md` 沒有把它們對到列號。新句「第一筆生意賣的是自己造的機器」可以對 #15 #16；1949 年那幾句可以對 #9 #11；t007 可以對 #52。
- 結論：要照現稿 t001–t152 整份重編，這輪不改。

## 查了哪些

- 152 句旁白逐句讀過，帶事實的每一句都回原件找原文，見〈逐句判定〉。
- 重算的數字：1,248,017／1,349,130 = 92.505%（93% 與「九成二點五」都對）；101,113／1,349,130 = 7.495%（年報列 7%，見 t137）；Broadcast 34.33%、Mobile 21.52%；2023 財年 Broadcast 37.71%、Mobile 20.36%；2024 財年 Mobile 19.95%；13.49 億、十二億多、約一億美元都對。
- 專利：US3631365 申請 1969-10-20、公告 1971-12-28，發明人 Ray M Dolby，主張 1968-11-01 英國優先權，全文引 Ser. No. 569,615；GB1120541 申請 1965-08-11、公開 1968-07-17。
- 財年：杜比 2026-10-12 新聞稿寫 2026 財年財報在 2026-11-17 發布。今天（11-08）還沒出，「二〇二五財年」「到今天還寫著」都站得住。若 11-17 之後才上架，依 `brief.md` 由站主決定要不要換數字。
- 這輪**沒開**，而且只用第一輪的判定的來源：Electronic Design、Brunswick Review、GoodWhale（t004 流傳說法的出處）、Screen Rant、Guinness、Stereo Review 1977、MediaTek、ATSC A/52 頁、Wikipedia 的 Dolby Laboratories 與 A Clockwork Orange 頁。現稿沒有一句只靠它們：t004、t071 都標成流傳的版本；AC-3 有年表與 FCC 支撐；庫柏力克導演《發條橘子》是常識。

## 開過的來源

全部在 2026-11-08 下載並全文搜尋，HTTP 200。

| 來源 | 網址 |
|---|---|
| Dolby 2025 財年 10-K 本文 | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/dlb-20250926.htm |
| 10-K R5（損益表） | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/R5.htm |
| 10-K R13（營收認列） | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/R13.htm |
| 10-K R56（營收拆分） | https://www.sec.gov/Archives/edgar/data/1308547/000130854725000007/R56.htm |
| 杜比 2026-10-12 新聞稿（Finviz 轉載） | https://finviz.com/news/401219/dolby-laboratories-announces-conference-call-and-webcast-for-q4-fiscal-2026-financial-results |
| 史丹佛 Ray Dolby papers 典藏說明（OAC） | https://oac.cdlib.org/findaid/ark:/13030/c8pv6t9k/ |
| IEEE Spectrum 2013 轉載 1988 年專訪稿 | https://spectrum.ieee.org/remembering-ray-dolby |
| ETHW：Dolby Laboratories | https://ethw.org/Dolby_Laboratories |
| 杜比 1998 年自編年表（Film-Tech 存檔） | https://www.film-tech.com/warehouse/manuals/dolbychronology.pdf |
| FCC 96-493 第四號報告與命令 | https://transition.fcc.gov/Bureaus/Mass_Media/Orders/1996/fcc96493.txt |
| 47 CFR §73.682（Cornell LII） | https://www.law.cornell.edu/cfr/text/47/73.682 |
| 47 CFR §15.117（Cornell LII） | https://www.law.cornell.edu/cfr/text/47/15.117 |
| Google Patents US3631365A | https://patents.google.com/patent/US3631365A/en |
| Google Patents GB1120541A | https://patents.google.com/patent/GB1120541A/en |
| Wikipedia：Dolby Stereo | https://en.wikipedia.org/wiki/Dolby_Stereo |
| Apple Newsroom 2021-05-17 | https://www.apple.com/newsroom/2021/05/apple-music-announces-spatial-audio-and-lossless-audio/ |
