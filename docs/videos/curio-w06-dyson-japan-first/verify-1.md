# curio-w06-dyson-japan-first 查核第一輪

- 查核者：獨立查核代理（Claude Opus 5.5，沒有參與寫稿），日期 2026-11-02。逐句讀 `video.json` 的旁白、字卡、標題、說明欄與縮圖字，對原始來源，撰稿者的 `claims.md` 只當線索。
- 用 curl 抓回原始 HTML 再搜全文、逐字對的：Fortune 2017；Gizmodo Japan 2014；Wikipedia Dyson (company)、James Dyson 的 wikitext；GetNavi 2023；BBC 2002 兩篇；Dyson 自家 *Invention: A Life* 第四至六章；《紐約客》2010；The Independent 2000；Encyclopedia.com Dyson Ltd.；日本維基シルバー精工。
- 用讀頁工具開、取回引句的：V&A；Science Museum；Design Museum；Forbes 2006；cash.ch；Encyclopedia.com Dyson, James；NZ Herald；Globe and Mail；Law Society Gazette；Google Patents US4373228A。讀頁工具是模型轉述，這幾份的短引句沒有逐字對過 HTML，但都與撰稿者的摘錄相符。
- 撰稿者沒開到、這輪新開的：BBC 1802155 與 2297227、《紐約客》、Independent（撰稿者記為打不開）；Dyson *Invention: A Life*、日本維基（撰稿者沒列）。
- 打不開：Fast Company 2007（403，Wayback 429）；Guardian 2002（404）；Earl & Wakeley 2005 書本（沒有線上全文）；Argus Press 1988（掃描版）；Dyson 區域站 aboutdyson（404／403，只見搜尋摘要）；收藏者論壇 manchestervacs、dysonmedic（403，只見搜尋摘要）。
- 列號與 `claims.md` 相同；#43 是這輪新增，#44–#47 只在這裡。

## 這輪改了什麼

| 行 | 問題 | 改法 |
|---|---|---|
| t044 | **錯**：「胡佛主管的一句話」。原文是戴森在隨機小冊子 *The Story of Dyson* 裡的轉述，「the inventor said」，沒有主管，也不是百科獨立記到的（#21） | 「他在自家小冊子裡寫，胡佛當年回他：袋子最好，袋子永遠最好」 |
| t008、`loops` | **錯**：「法院判的那筆賠償」。法院判侵權，但金額是定賠償額前和解（#42） | 「胡佛賠的那筆錢」 |
| t099、`fac-4m` 字卡 | 「胡佛賠了」沒錯但會接著上面聽成判決 | 「胡佛提出賠四百萬英鎊，他接受了」；字卡同 |
| t049 | **錯**：「他告回去了」暗示安麗先告；《紐約客》寫戴森提告、安麗反告（#22）。先後只有 NZ Herald 的安麗要錢訴訟可能較早，查不到日期 | 「他提告」 |
| t049、t047、t048 | **缺對方立場**：安麗否認有錯並反告；取消的理由是機器還不能賣；「更怪的是」把時間順序講成暗示（#22、#23） | 補「安麗否認有任何不對，還反告他」「對方後來說機器還不能賣」；「更怪的是」改成中性的「但這還不是結尾」 |
| t002、t094、說明欄 | 「當時將近兩千美元」當事實講。25 萬日圓用 1986 年平均匯率 168.5 約 1,480 美元，1987 年約 1,730 美元；《紐約客》寫 1,700。接近兩千要到約 125 日圓（#2、#44） | 標「他自己說」「他自己換算」，說明欄標明是他的換算；t002 為了開場長度把「那台吸塵器」縮成「它」 |
| t075、說明欄 | **錯**：「只查到維基和轉述」。維基的註腳就是 BBC 2002，BBC 兩點都寫；GetNavi 也記獎（#5） | 改成 BBC 與日本媒體都這樣寫，獎的原始紀錄沒找到 |
| t035、`uk-num` 字卡 | 來源比稿子更硬：戴森自家網站寫 550、生意不成功。「賣」與「造」差一字（#6、#7） | 主句換成他自己的網站 |
| t006 | 「同一個設計」：維基說 G-Force 是 Cyclon 的 reworked version，但第 7 章自己講機身、馬達全改，戴森也寫 1985 年在東京重畫吸頭（#43） | 「他設計的吸塵器」 |
| t033 | 「這家公司找了」：維基是被動句，沒寫誰找的（#6） | 「機器是義大利的家電廠造的」 |
| t055、`jp-none` 字卡、說明欄 | 原文「ステーショナリーに強い輸入業の会社」，不是「主要進口文具」（#25） | 「以文具進口見長」；後面口語的「賣文具的」保留，當旁白的玩笑 |
| t057 | 「全世界的家電廠都不要」過頭，舊句也不是來源的話（#18、#19） | 「那麼多家電廠」 |
| t064 | 原文是楽器、スタジオ機器，「音響」不精確（#29） | 「樂器和錄音室器材」，`say` 同步 |
| t068 | 「精密機械廠」「不是本來就做吸塵器的」來源沒寫；稿子自己的推論（#31） | 「另一家公司，它以編織機和打字機出名」（シルバー精工，日本維基） |
| t081 | 「最該替這個傳奇加油添醋的人，反而把它講小了」只看 Fortune；他自家網站寫 instant design classic（#43） | 「他自己的網站說它一上市就是設計經典，一談到生意，他反而把它講小了」 |
| t097 | 型號 Triple Vortex 是三重渦流，「三重氣旋」把爭點講死了（#41） | 「三重渦流機型」 |

`youtube.sources` 新增七筆。改了 18 行旁白，`script.md` 已重產。**盲評 `narrative` 要用這版做。**

## 撰稿者標的弱點

- **Kleeneze Rotork Cyclon：站得住，而且更強。** 戴森自家 *Invention: A Life* 第五章直接寫 1983、1984 年生產、Rotork 授權、只造 550 台、生意不成功。第 4 章與 t103 不用改結論。Zanussi 與郵購仍只有維基（引 Earl & Wakeley 2005，書沒開到）加收藏者貼文的搜尋摘要；t033、t034 的 Zanussi 部分已標「維基百科寫」，郵購那句接在同一段。
- **身分象徵與 1991 設計獎：** 比撰稿者記的強一點，BBC 2002 兩點都寫，GetNavi 記獎且寫「たちまち人気製品に」。但獎本身的主辦或得獎紀錄沒找到，BBC 也沒註出處。維基把它連到 iF Design Award，沒有來源支持，稿子沒用。
- **胡佛主管「袋子永遠最好」：** 歸屬是錯的，已改（上表）。沒有任何胡佛方紀錄。t100 回呼仍站得住，因為片中已講是他寫的。
- **日本細節：** 幾乎只有 Gizmodo 的山本秀夫訪談，已逐字對。有兩處佐證：戴森自己寫 1985 年在東京重畫吸頭；GetNavi 記 25 萬日圓與シルバー精工。沒有另一個來源佐證 100V、半年、一年半、沒有工程師。旁白 t052 標「當事人是這樣講的」，字卡標山本的說法。同一篇報導本文寫「デザイン誌に掲載された試作機」，訪談寫「本」，只差在載體，用了訪談。
- **安麗段落：** 沒有說抄襲。補上否認與反告後，雙方立場都有。「跟他的設計非常像」標維基；《紐約客》另寫 dual-cyclone，同方向。Argus Press 1988 原標題是 Claims Theft，稿子不用。t046「最難看的一段」是旁白對這段的評語，不指控，留著。
- **5,127 的 Fast Company 引文：** 仍打不開，維基轉引寫「about 5,127」。但稿子不靠它：Globe and Mail 署名戴森本人、Forbes、BBC、NZ Herald 都有 5,127。字卡「他自己講的原型數」站得住。
- **撰稿者的解讀：** t024（「這是我的猜測，他沒這樣解釋」）、t038（「我的讀法」）、t070（「我覺得」）、t085、t092（「這是我從這幾句話讀出來的」）、t104、t108 都有標明。t036「嚴格講已經不對了」與 t103 是結論，有 #6 撐。t092 另見下方。

## 逐項查核

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | V&A：G-Force，1986，戴森設計，APEX 製造，日本 | CONFIRMED | 「Designed by James Dyson」「Manufactured by APEX, Japan」；Given by Dyson；M.64-1993；Room 74 | V&A | https://collections.vam.ac.uk/item/O146046/ | ✅ |
| 2 | 25 萬日圓，將近兩千美元 | CHANGED | 「a quarter-million yen each, nearly $2,000 at the time」；《紐約客》seventeen hundred dollars；見 #44 | Fortune；New Yorker | https://fortune.com/2017/09/09/james-dyson-vacuum/ | ✅ 日圓／⚠ 美元 |
| 3 | 1986 發售，二十幾萬日圓 | CONFIRMED | 「1986年に最初の製品が発売」「当時の価格は驚きの20数万円」 | Gizmodo | https://www.gizmodo.jp/2014/10/dyson_g-force_vs_digital_slim.html | ✅ |
| 4 | 小眾、賣得不算成功、有點收入 | CONFIRMED | 「so we had some income coming in. However, Apex wasn't very successful with it. They sold the machine as a niche product」 | Fortune | https://fortune.com/2017/09/09/james-dyson-vacuum/ | ✅ |
| 5 | 1991 獎、身分象徵 | CHANGED | 「It won the 1991 International Design Fair prize in Japan and became a status symbol there」；GetNavi 同獎 | BBC；GetNavi | https://news.bbc.co.uk/2/hi/business/1802155.stm | △ 獎的原始紀錄未見 |
| 6 | Cyclon，Rotork 授權，550，不成功；Zanussi、郵購 | CHANGED | 「produced in 1983 and 1984 … Rotork, who had licensed my design … not a commercial success. Only 550 were made」；維基「Built by Italian appliance maker Zanussi」「Only about 500 units were sold in 1983」 | Dyson；維基 | https://www.dyson.com/james-dyson/invention-a-life/05 | ✅ 本人／△ Zanussi |
| 7 | 約 550、失敗 | CONFIRMED | 「Ein Flop: Nur rund 550 Stück」；「lizenzierte 1983/84」 | cash.ch | https://www.cash.ch/news/top-news/rotork-ein-kaum-bekanntes-detail-hinter-der-grossten-ubernahme-der-abb-firmengeschichte-967995 | ✅ |
| 8 | Rotork 是老東家 | CONFIRMED | 「begann seine Karriere 1970 bei Rotork」「1974 verliess」。旁白沒用「唯一」 | cash.ch | 同上 | ✅ |
| 9 | Hoover Junior，倒袋沒用，灰塞細網 | CONFIRMED | 「In the 1970s … Hoover Junior」「clogging the fine material mesh」。Fortune 版本是 1979 年沒備袋只好倒，年代相容；t013 末句是旁白的引申 | 維基 | https://en.wikipedia.org/wiki/Dyson_(company) | △ |
| 10 | 工業氣旋、紙板加膠帶 | CONFIRMED | 「giant cyclone」；「a cardboard model with sticky tape, connected it to his Hoover with its bag removed」 | 維基 | 同上 | △ |
| 11 | 美國專利、1979-04 英國優先權 | CONFIRMED | GB7913690，1979-04-19；1983-02-15 核准；「no dust bags are required」 | Google Patents | https://patents.google.com/patent/US4373228A/en | ✅ |
| 12 | 5,127 | CONFIRMED | 見上；Fast Company 未開到 | Globe；Forbes；BBC；NZ Herald | https://www.theglobeandmail.com/report-on-business/careers/leadership-lab/yes-its-ok-it-took-me-5127-attempts-to-make-a-bagless-vaccuum/article19992476/ | ✅ |
| 13 | Forbes 四年半 | CONFIRMED | 「After four and a half years and 5,127 prototypes」 | Forbes | https://www.forbes.com/2006/08/01/leadership-facetime-dyson-cx_hc_0801dyson.html | ✅ |
| 14 | 維基 1979–1984 | CONFIRMED | 「5,127 prototype designs between 1979 and 1984」 | 維基 | https://en.wikipedia.org/wiki/Dyson_(company) | ✅ |
| 15 | 2014 專欄十五年 | CONFIRMED | 「It took me 15 years and 5,127 attempts」，署名本人，2014-08-11。其他：BBC 五年、行銷百科 14 年、Independent 引他「20 years」 | Globe | 同 #12 | ✅ |
| 16 | 越欠越多、太太賣畫教課 | CONFIRMED | 「further and further into debt」「sold paintings and taught art classes, and we borrowed, and borrowed, and borrowed」 | Fortune | https://fortune.com/2017/09/09/james-dyson-vacuum/ | ✅ |
| 17 | 投資人出四成九 | CONFIRMED | 「Jeremy Fry provided 49% of the investment for cyclonic vacuum development, and the rest came from a loan」 | 維基 | https://en.wikipedia.org/wiki/Dyson_(company) | △ 單一 |
| 18 | 找授權、兩家美國廠牌、沒好理由 | CONFIRMED | 「Conair and Black & Decker—were quite keen」「for no good reason」；談判卡在對方專利律師 | Fortune | https://fortune.com/2017/09/09/james-dyson-vacuum/ | ✅ |
| 19 | 英美都難找授權 | CONFIRMED | 「struggled to find a licensee for his machine in the UK and America」 | 維基 | https://en.wikipedia.org/wiki/Dyson_(company) | ✅ |
| 20 | Forbes、Design Museum 講英國找不到支持 | CONFIRMED | 「launched it first in Japan」「wouldn't invest in a product that would disrupt the vacuum bag market」；「licensed his first design … in Japan」 | Forbes；Design Museum | https://designmuseum.org/adopt/move/dyson-g-force | ✅ |
| 21 | 「袋子永遠最好」 | CHANGED | 「Hoover wouldn't give it the time of day. They said: 'Bags are best. Bags will always be best.' Then they copied it," the inventor said in The Story of Dyson」 | Encyclopedia.com | https://www.encyclopedia.com/marketing/encyclopedias-almanacs-transcripts-and-maps/dyson-ltd | ✅ 引文／⚠ 戴森單方 |
| 22 | 安麗日期與提告 | CHANGED | 「In April 1984, Dyson claimed」「January 1985」「very similar」「Less than a month later」；「Amway denied any wrongdoing and countersued for damages」 | 維基；New Yorker | https://www.newyorker.com/magazine/2010/09/20/how-to-make-it | △ 日期只有維基（引 1988 報紙，未開） |
| 23 | 取消合約、要回錢 | CHANGED | 「cancel the agreement and instigate a lawsuit to get back the money」；「As Dyson recalls … backed away … claiming that the machine was not ready for sale」 | NZ Herald；New Yorker | https://nzherald.co.nz/business/james-dyson-on-how-trial-and-error-made-him-britains-wealthiest-inventor/Y2HK65HBGEL4XRIHJNSKI6ZD2U | △ 戴森單方 |
| 24 | 1991 和解、安麗照賣、共同被授權 | CONFIRMED | 「In 1991, Dyson and Amway Corp. settled … Amway continued to sell its product, and the two sides became joint licensees.」是 Fortune 編輯括號，不是戴森自述；《紐約客》只寫 dismissed the lawsuits | Fortune | https://fortune.com/2017/09/09/james-dyson-vacuum/ | ✅ |
| 25 | Apex 是文具進口商，沒工程師沒工廠 | CHANGED | 「本来ステーショナリーに強い輸入業の会社でエンジニアはいないし、工場もない」；本文另稱「美しいデザインのモノを各国から集めてくる商社」 | Gizmodo | https://www.gizmodo.jp/2014/10/dyson_g-force_vs_digital_slim.html | △ 單方 |
| 26 | 1984 書上的照片、一見鍾情 | CONFIRMED | 「1984年にアメリカで出版された「Product Design」という本に、ピンク色の掃除機の写真」「社長が一目惚れ」 | Gizmodo | 同上 | △ 單方 |
| 27 | 試作品、想進口、在日本造就讓權 | CONFIRMED | 「これはまだ試作品で完成していない」「日本で作ってくれるなら販売の権利を譲る」 | Gizmodo | 同上 | △ 單方 |
| 28 | 100V、機身全改、半年、一年半 | CONFIRMED | 「100Vのモーター」「筐体の設計をすべて見直す」「半年くらい」「その後1年半、不具合との戦い」 | Gizmodo | 同上 | △ 單方 |
| 29 | 山本 1985 進 Apex、防堵零件 | CHANGED（措辭） | 「ヤマハで楽器やスタジオ機器」；シュラウド「様々な穴のサイズ、形状を実験」 | Gizmodo | 同上 | △ 單方 |
| 30 | 科學博物館：戴森加 Apex 設計團隊 | CONFIRMED | 「designed by James Dyson and Apex Inc design team and manufactured by Apex Inc., Tokyo Japan, 1985-1990」 | Science Museum | https://collection.sciencemuseumgroup.org.uk/objects/co49526/g-force-cyclonic-vacuum-cleaner | ✅ |
| 31 | 製造者、1998 法人 | CHANGED | 「シルバー精工が製造を担当」「1998年にダイソンが日本法人を設立」；「シルバー編機で知られるが、タイプライターなど」。與 V&A、科學博物館的「Apex 製造」有出入 | GetNavi；日本維基 | https://getnavi.jp/homeappliances/877622 | △ |
| 32 | 1986 年 3 月投產 | CONFIRMED | 「in March 1986, a reworked version of the Cyclon, called G-Force」；旁白只講 1986 | 維基 | https://en.wikipedia.org/wiki/Dyson_(company) | ✅ |
| 33 | 第二代賣到 2011 | CONFIRMED | 「マーク2となって、2011年まで生産・発売」「90年代以降…シルバー精工」；シルバー精工 2011 下市、後破產，時間相容 | Gizmodo；日本維基 | https://www.gizmodo.jp/2014/10/dyson_g-force_vs_digital_slim.html | △ |
| 34 | 設計博物館：成功、資助 DC01 | CONFIRMED | 外型、顏色、氣旋「were a success」；銷售資助 1993 年 DC01 | Design Museum | https://designmuseum.org/adopt/move/dyson-g-force | ✅ |
| 35 | 小眾熱門貨 | CONFIRMED | 「emerged as a cult favorite, despite its rather high price tag」 | Encyclopedia.com | https://www.encyclopedia.com/books/culture-magazines/dyson-james | ✅ |
| 36 | 銷量與權利金查不到 | CONFIRMED（反面，只到讀過的範圍） | 日英再搜一輪也沒有；只有 2004 AFP 一個全 Dyson 機種的年銷量，無關。Apex、シルバー精工的文件沒找到 | 同列 | — | ⚠ |
| 37 | 維基：靠日本授權收入成立公司 | CONFIRMED | 「Using the income from the Japanese licence … in 1991 … Barleta Limited」；BBC 同方向；Companies House 成立日 1991-07-08（維基引） | 維基；BBC | https://en.wikipedia.org/wiki/Dyson_(company) | ✅ |
| 38 | 1993 前沒人借、銀行經理、100 萬美元 | CONFIRMED | 「None of the venture capitalists and banks would lend me money until 1993, when my bank manager, Mike Page, personally lobbied Lloyds」「$1 million」「for tooling」 | Fortune | https://fortune.com/2017/09/09/james-dyson-vacuum/ | ✅ 本人 |
| 39 | DA 001、Wrexham、1993-01、約 200 英鎊 | CONFIRMED | 「produced by American company Phillips Plastics in a facility in Wrexham, Wales, beginning in January 1993 and sold for about £200」 | 維基 | https://en.wikipedia.org/wiki/Dyson_(company) | △ 單一 |
| 40 | 兩年內最暢銷 | CONFIRMED | 「Within two years it was the best-selling vacuum in Britain」；「early 1995」 | Fortune；Encyclopedia.com | https://fortune.com/2017/09/09/james-dyson-vacuum/ | ✅ |
| 41 | 2000 高院認定侵權、胡佛的主張 | CHANGED（型號） | Deputy High Court Judge Michael Fysh QC；「the Hoover Triple Vortex」；「nothing that was not generally known within the industry」；「cyclonic technology was already developed in other fields」；胡佛 2001 上訴也輸 | Independent；Law Gazette；BBC | https://www.independent.co.uk/news/uk/home-news/james-dyson-spent-years-fighting-hoover-now-he-intends-to-clean-up-634348.html | ✅ |
| 42 | 2002 年 400 萬英鎊 | CHANGED | 「settled a dispute … by accepting a £4m ($6.3m) damages offer from its rival Hoover」 | BBC | https://news.bbc.co.uk/2/hi/business/2297227.stm | ✅ |
| 43 | 他自家網站的講法 | CONFIRMED（新增） | 「At work in Nishiazabu, Japan in 1985 redesigning the cleaner head」「Pale pink, it became an instant design classic」 | Dyson | https://www.dyson.com/james-dyson/invention-a-life/05 | ✅ 本人 |
| 44 | 1986 年匯率（新增） | CONFIRMED | 1985 平均 238.54，1986 平均 168.52，1987 平均 144.64（搜尋摘要，IMF 數字）；25 萬日圓約 1,050、1,480、1,730 美元 | Nautilus | https://nautilus.org/pegasus/u-s-japan-annual-average-exchange-rate/ | ✅ |
| 45 | 其他授權收入（新增，稿子沒用） | 註記 | 《紐約客》：加拿大 Iona 的 Drytech 版。「日本的錢」不是他唯一的授權收入，t092、t106 沒說唯一，站得住 | New Yorker | https://www.newyorker.com/magazine/2010/09/20/how-to-make-it | ✅ |
| 46 | 授權年份（新增，稿子沒用） | 註記 | Fortune 寫 1986 breakthrough，《紐約客》與維基寫 1985；山本 1985 年已在做。旁白沒講簽約年 | 同列 | — | ✅ |
| 47 | 銀行與開工的先後（新增） | 註記 | Fortune 只寫 1993 年借到；維基 1993-01 開工。t089、t093 都站得住，但實際先後沒有來源 | 同列 | — | △ |

## 其他判定

- **標題**「戴森先賣日本的粉紅吸塵器，25 萬日圓真的救了它嗎？」：問句，片中給答案，沒過頭。
- **縮圖**「戴森／日本救的」：單看像肯定句，靠畫面的困惑臉與片中講清楚；不算錯，由站主決定。
- **t001、t004、t031、t074** 都標成流傳或「你大概聽過」；「英國沒人要」有出處（Wikipedia James Dyson：「No manufacturer or distributor would handle his product in the UK」）。
- **t092「夠他活下去，不夠他開工廠」**：標成我的讀法。支持：Fortune 的 1993 借款。反面：BBC、GetNavi、維基都說日本收入是成立公司的本錢，所以 t106 用「讓他撐到銀行點頭」是合理折衷。金額查不到，這句驗不了到底。
- **t096「當年不要這個點子的人」**：胡佛拒絕是戴森與維基的講法，上下文已標。
- **提示詞**：`us-*`、`fac-*` 只畫不指認的一般人物，沒有公司名、人名、商標；`us-hoover` 畫主管搖頭，雖然引句不再歸給主管，但不矛盾（畫的是對方回絕）。
- **風險**：沒有暗示安麗或胡佛其他違法。胡佛侵權是法院認定；安麗只有戴森的主張與對方的否認。
- **`brief.md`** 還寫著舊措辭（「文具貿易商」「1983 約 500–550」），這輪沒動，交撰稿者同步。

## 仍只有單一或單方來源

100V、半年、一年半、沒有工程師、一見鍾情、試作品、讓出販售權（山本單方）；Zanussi、郵購（維基）；安麗 1984-04 與 1985-01 的日期、CMS-1000（維基，引 1988 報紙未開）；安麗的取消理由（戴森回憶）；「袋子永遠最好」（戴森單方）；1991 獎的原始紀錄（未見，只有 BBC、GetNavi）；49%、Wrexham（維基）；銀行經理與 100 萬美元（戴森自述）。日本銷量與權利金：查無。
