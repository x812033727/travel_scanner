# curio-b02 查核第一輪

- 查核：獨立查核代理（Claude Opus 5.5，沒有參與撰稿），2026-10-31。逐句對照 `video.json` 的旁白、卡片、`youtube.title`、`youtube.description`、`thumbnail.data` 與 [`../history-curiosity/topic-checks/B02.md`](../history-curiosity/topic-checks/B02.md)；`claims.md` 只當待驗的對照，不當證據。
- 自己重開的來源（2026-10-31）：CPSC 1997／1999／2023／2026 四頁（curl 回 403，改用抓頁工具讀到）、CPSC 和解協議 PDF（下載逐字讀）、Tampa Bay Times 1997 檔案頁、JTC 轉載的日經亞洲 2024、日經亞洲 2020 與 2026、TechNews（MoneyDJ 轉 FT）、Ride Media、有報 S100XQSE（EDINET PDF）、FY2023／FY2024／FY2025 決算短信、Bicycle Retailer 2021／2022、road.cc、CSM 1982、Sheldon Brown、Encyclopedia.com 與 FundingUniverse 的 SRAM／Shimano 條、Paul Lange 新聞稿、the-shashi、NDL API、堺市頁、工商時報 2024-01-26、經濟部公司登記 API（含營業項目 API）。
- 讀不到：shimano.com（含台灣據點頁 stc_en 與 2012 fact sheet）一律 403，沒有繞過；FT、Straits Times 原報沒讀到（照 topic-check 的轉載）。
- 結果：旁白 172 行，OK 161、FIX 2、SOFTEN 9；說明欄 SOFTEN 一處。畫面：`sakai-founder` 與 `close-question` 等於畫島野庄三郎本人（1958 年歿，未滿 70 年），要改（見〈畫面規則〉）。
- 旁白不用的列：#3 的 12 坪與月租、#6、#8、#9、#15 的兩名員工、#17、#22、#26、#27、#31、#36 的各國廠名、#37、#38、#45 的金額、#51、#52、#54、#56、#58、#59、#60、#65、#69、#70、#72。
- 本輪自己補的列：#73–#81，附在表尾（標「查核代理 2026-10-31 補」）。
- 對 topic-check 的更正：#62 的「美聯社稿」在原頁找不到署名，應改為「Tampa Bay Times 檔案（未署名）」；#55 的「是銷售／服務據點，不是工廠」在登記上站不住（見 #74）。

## 稿子逐句核對

| 行 | 旁白或卡片（節錄） | 列 | 判定 | 說明 |
| --- | --- | --- | --- | --- |
| t001 | 你騎的公路車，變速器很可能出自同一家日本公司： | #53 | OK | 「很可能」對得上日經「estimated global share of 85%」（運動車零件）與 FT「高階零件 65%」兩個估計都過半；下一句立刻標出是日經的估計，沒說「全世界的腳踏車」 |
| t002 | 日經估計，運動車的零件，全球大約八成五是它的。 | #53 | OK | 重開 JTC 轉載的日經亞洲（2024-03-06 刊，2-16 專訪）：「mainly for sports bikes like road bikes and mountain bikes, with an estimated global share of 85%」；說成估計、限定運動車零件 |
| t003 | 可是它現在，一台完整的腳踏車都不賣。 | #11 #13 | OK | 有報三個事業：自転車部品／釣具／その他，無完成車；只說「現在」 |
| t004 | 一九二一年二月，大阪的堺， | #1 | OK | 有報沿革「1921年２月…堺市東湊町」，只到月 |
| t005 | 一個年輕人開了一間鐵工廠。 | #1 #3 | OK | the-shashi「26歳の島野庄三郎氏」 |
| t006 | 隔年，他做起了腳踏車後輪的小齒輪。 | #2 | OK | 有報「その翌年に自転車部品のフリーホイールの製造を開始」 |
| t007 | 一百多年後，它最大的客戶，卻不是車廠。 | #34 | OK | 有報「主な相手先別の販売実績」只列 PAUL LANGE & CO. OHG（11.6%），其他客戶都未達 10% |
| t008 | 它滿百歲那年，有車廠說零件要等四百天。 | #42 | OK | 說成「有車廠說」；TechNews 轉 FT「歐洲和美國業者說…長達400天」，Ride Media「Some companies are reporting delays of as much as 400 days」，都不是 Shimano 自己說的 |
| t009 | 二〇二六年，美國罰了它一千一百五十萬美元， | #67 #68 | SOFTEN | CPSC 標題是「Shimano Agrees to Pay」，是和解（2026-03-12 暫時接受，等公眾意見），Shimano 不承認；開場只有這一句、沒有否認。改「它同意付」。建議：「二〇二六年，它同意付給美國一千一百五十萬美元罰款，」 |
| t010 | 同一個罪名，二十七年前就罰過一次。 | #63 #67 | SOFTEN | 1999 年新聞稿標題是「Alleged Delay in Reporting」，兩次都是委員會的指控、Shimano 都否認；開場用「罪名」又沒有歸屬，像是定了罪。改成「指控」。建議：「同一種指控，二十七年前就罰過一次。」 |
| 卡片 open-promise | {"text": "105 年", "kicker": "1921 年 2 月，大阪府堺市", "sub": "一台車都不賣，憑什麼？"} | #1 | OK | 105 年、1921 年 2 月、大阪府堺市 |
| t011 | 這份檔案，我們把它一百零五年的帳翻給你看。 | #1 | OK | 1921→2026，105 年 |
| t012 | 不賣車的 Shimano，憑什麼讓別人的車替它賺錢？ | — | OK | 問句 |
| t013 | 那個年輕人叫島野庄三郎。 | #5 | OK | 名字可講；但配圖見下方「畫面規則」：這一句的配圖等於畫本人 |
| t014 | 他的鐵工廠，為什麼偏偏開在堺？ | #7 | OK | 問句 |
| t015 | 堺市政府說，大約一千六百年前，這裡蓋起了一大片古墳。 | #7 | OK | 重開堺市頁：「約1600年前に築かれた百舌鳥古墳群」，有說出是市政府 |
| t016 | 蓋古墳的打鐵功夫，後來拿去做鐵砲、做菜刀； | #7 | OK | 「古墳築造を支えた鉄加工技術は、鉄砲や包丁づくりへと発展」 |
| t017 | 到了明治時代，又拿去修國外進口的腳踏車。 | #7 | OK | 「明治時代には輸入自転車の修理にも活用されました」 |
| t018 | 從古墳一路接到腳踏車，我第一次讀到也愣了一下。 | — | OK | 旁白反應 |
| t019 | 換成你是他，在一條修了幾十年進口車的街上開店， | #7 | SOFTEN | 來源只說堺的鐵加工技術在明治時代用來修進口車；「一條…的街」「修了幾十年」都沒有出處（明治到 1912 年為止，「幾十年」要從 1900 年前算起，沒讀到）。建議：「換成你是他，在一座明治時代就在修進口車的城裡開店，」 |
| t020 | 你會做什麼？ | — | OK | 問句 |
| t021 | 他沒有去做整台車，做的就是開頭那個小齒輪：飛輪。 | #2 #4 #11 | SOFTEN | 來源只說隔年開始做飛輪；「他沒有去做整台車」是推論，而且 #11 已提醒 1951 年併過「島野自転車」、不能說它從沒做過車。拿掉前半句即可。建議：「他做的，就是開頭那個小齒輪：飛輪。」 |
| t022 | 你騎到一半停下腳，輪子還繼續轉，靠的就是它。 | #4 | OK | 飛輪的作用（PRESIDENT 廣告企劃，常識層級） |
| t023 | 一九五一年，它還併了一家叫島野腳踏車的公司。 | #10 #11 | OK | 有報「1951年２月 島野自転車株式会社(資本金2,300万円)を吸収合併」；同月改名島野工業。「島野腳踏車」是公司名的意譯，可接受（要更貼原名可說「島野自轉車」） |
| t024 | 那家公司做什麼？ | #11 | OK | 問句 |
| t025 | 紀錄沒寫。所以我只能跟你說：它現在不賣車。 | #11 | OK | 有報沒寫這家公司的業務；FundingUniverse 也只寫 1951 改名。只說「現在不賣車」，站得住 |
| t026 | 為什麼不賣？新加坡《海峽時報》引過島野家的人一句話： | #12 | OK | △ 有說出處；原報 Straits Times 2003-08-03 沒讀到，是 IDCH（FundingUniverse）轉引「remarked one of Shimano's sons to the Straits Times」 |
| t027 | 創辦人說過，絕對、絕對不要跟客戶競爭。 | #12 | OK | 「never ever compete with a customer」 |
| t028 | 可是不跟客戶搶，客戶又要去哪裡找？ | — | OK | 問句 |
| t029 | 在海外。一九六五年三月，它在紐約開了一家公司。 | #14 | OK | 有報 1965-03（FundingUniverse 寫 1965-01，以有報為準） |
| t030 | 兩年後，德國斯圖加特一家公司，當上它的德國總代理。 | #35 | OK | Paul Lange 新聞稿（2025-10-01）「Seit 1967 … der deutsche Generalvertreter für SHIMANO Komponenten」 |
| t031 | 先記住這家斯圖加特的公司。 | — | OK | 伏筆 |
| t032 | 一九七〇年，它又開始做一樣東西：釣魚用的捲線器。 | #28 | OK | 有報 1970-02「釣用リールの製造を開始」 |
| t033 | 你沒聽錯，釣魚。這個副業，後來會長到多大？ | — | OK | 問句 |
| t034 | 美國那幾年有多瘋？ | — | OK | 問句 |
| t035 | 一九七二年，美國人買的腳踏車，比汽車還多。 | #18 | OK | CSM 1982「in 1972, more bikes were bought than cars」（談美國市場） |
| t036 | 隔年，美國賣了一千五百二十萬台腳踏車，是那一波的最高點。 | #18 | OK | 「the 1973 high of 15.2 million bikes sold」 |
| t037 | 你想像得到，那兩年美國車行老闆的表情嗎？ | — | OK | 玩笑 |
| t038 | 一九七三年，它在新加坡開了第一座日本以外的組裝工廠； | #16 | OK | BRAIN「it was the company's first assembly plant outside of Japan」 |
| t039 | 一九七四年，又把銷售辦公室開到加州。 | #19 | OK | FundingUniverse「Opening a sales office in California in 1974」；沒說歐洲做不出來 |
| t040 | 一位美國老技師說，它最高階的那組零件， | #20 | OK | △ 有歸屬（Sheldon Brown） |
| t041 | 要到一九八四年才真正成功。那年發生了什麼？ | #20 | OK | 「not really successful until 1984」 |
| t042 | 它在最高階那一組上，放了一個新東西：段數定位。 | #21 | OK | 「In 1984, Shimano introduced Dura-Ace S.I.S.」；沒說「第一個」 |
| t043 | 以前換檔靠手感；段數定位，就是撥一格、換一檔。 | #21 | OK | 名詞解釋 |
| t044 | 你現在換檔撥一下就到位，用的就是這個想法。 | — | OK | 對觀眾 |
| t045 | 可是好零件不只一家會做，它到底多了什麼？ | — | OK | 問句 |
| t046 | 它多的，是怎麼賣。 | #23 | OK | 轉場 |
| t047 | 一本美國公司史辭典寫，它把撥桿和變速器配成一整組， | #23 | OK | △ 有歸屬：IDCH SRAM 條「sold its shifters and derailleurs to bike manufacturers as complete sets」 |
| t048 | 整組賣給車廠。 | #23 | OK | 同上 |
| t049 | 我的看法是，這一招比任何一個新零件都厲害。 | — | OK | 意見已標 |
| t050 | 整組賣，別人要怎麼插得進來？ | — | OK | 問句 |
| t051 | 一九八七年，芝加哥冒出一家新公司，做轉把式的變速器。 | #24 | OK | 「started in Chicago in 1987」 |
| t052 | 這家小公司在加州告 Shimano 違反反托拉斯法。 | #23 | OK | 「a California antitrust lawsuit by SRAM」 |
| t053 | 一九九一年，雙方庭外和解，條件沒有公開。 | #25 | OK | 「settled in 1991 for an estimated $3 million to $5 million」——只有估計，條件沒公開；沒講金額、沒說誰贏 |
| t054 | 之後，車廠可以混搭別家的零件了。 | #23 | OK | 「as complete sets until … settled in 1991」 |
| t055 | 六年後，美國消費品安全委員會發出一份公告， | #61 | OK | 1991→1997 |
| t056 | 主角，是一根曲柄。 | #61 | OK | — |
| t057 | 曲柄，就是你踩踏板時，連著踏板一起轉的那根金屬臂。 | — | OK | 名詞解釋 |
| t058 | 公告說，北美有超過一百萬根， | #61 | OK | CPSC 1997-07-01「more than 1 million cranks installed on bicycles in North America」 |
| t059 | 已經有六百三十多件斷掉的報告，二十二個人受傷。 | #61 | OK | 「more than 630 reports of cranks breaking in North America resulting in 22 injuries」 |
| t060 | 這些曲柄，裝在誰的車上？ | — | OK | 問句 |
| 卡片 crank-stats | {"title": "1997 年 7 月，美國的召回公告", "stats": [{"value": "100 萬+", "label": "北美的曲柄"}, {"value": "630+", "label": "斷裂報告"}, {"v | #61 | OK | 四個數字都對 CPSC 1997-07-01 |
| t061 | 兩百多款車，掛著至少四十九個品牌。 | #61 | OK | 「more than 200 models of bicycles … sold under at least 49 brand names」 |
| t062 | 美聯社的報導說，全世界要召回兩百五十萬台登山車。 | #62 #73 | FIX | 重開 Tampa Bay Times 檔案頁：沒有任何「Associated Press／AP」署名（credits 空白），「美聯社」沒有根據；而且 250 萬是「about 1-million bikes in North America」加「1.5-million bikes in Europe」，不是「全世界」。建議：「當時的報導說，北美加歐洲要召回兩百五十萬台登山車。」 |
| t063 | 名單上，有一個你一定認得的名字：捷安特。 | #62 | OK | 「at least 49 brand names, including … Giant …」 |
| t064 | 我覺得，一根零件出事，四十九個品牌就一起出事。 | — | OK | 意見已標 |
| t065 | 沒想到，事情還沒完。一九九九年七月，委員會宣布， | #63 | OK | CPSC 1999-07-07 |
| t066 | Shimano 的美國公司，同意付十五萬美元的民事罰款。 | #63 | OK | 「Shimano American Corp.」「$150,000 civil penalty」 |
| t067 | 還記得開頭那個罪名嗎？ | #63 | OK | 若 t010 改成「指控」，這裡也改「還記得開頭那個指控嗎？」保持一致 |
| t068 | 不是曲柄會斷，是報得太晚。 | #63 | OK | 描述的是指控內容（「Alleged Delay in Reporting」），下一句立刻標「委員會指控」 |
| t069 | 委員會指控，它早就知道有人受傷，卻沒有及時通報。 | #63 | OK | 新聞稿：CPSC also alleges Shimano knew of crank breakages causing 22 injuries before reporting |
| t070 | Shimano 否認曲柄有缺陷，也否認違反通報義務。 | #63 | OK | 「Shimano denies that the bicycle cranks were defective」「also denies that it violated the reporting requirements」 |
| t071 | 十五萬美元，我猜它不痛不癢； | — | OK | 意見已標 |
| t072 | 這個數字，留著跟另一張罰單比。 | — | OK | 伏筆 |
| t073 | 真正讓它坐上雲霄飛車的，是二〇二〇年。 | — | OK | 轉場 |
| t074 | 疫情一來，腳踏車的需求突然往上衝。 | #45 | OK | — |
| t075 | 那年八月，日經一篇評論的標題是： | #71 | OK | 2020-08-05，Makoto Kajiwara「Nikkei commentator」，確實是評論 |
| t076 | 這家做腳踏車零件的公司，市值超過了日產汽車。 | #71 | OK | 標題「How bicycle parts maker Shimano eclipsed Nissan in market cap」；只引標題，沒報市值 |
| t077 | 做齒輪的比做汽車的值錢，這個標題我看了兩遍。 | — | OK | 旁白反應 |
| t078 | 訂單多到什麼程度？ | — | OK | 問句 |
| 卡片 boom-400 | {"text": "400 天", "kicker": "歐美車廠對《金融時報》說", "sub": "高階零件，從下單到出貨"} | #42 | OK | 歸屬「歐美車廠對《金融時報》說」；FT 原文付費牆，讀的是 MoneyDJ 授權轉載 |
| t079 | 開頭那四百天，就是這時候：《金融時報》引述歐美車廠說， | #42 | OK | 歸屬給 FT 引述的歐美業者（TechNews 轉載 MoneyDJ 譯 FT 2021-05-31） |
| t080 | 高階零件從下單到出貨，要等這麼久。 | #42 | OK | 「高階零組件，下單到出貨的前置時間（lead time）長達400天」 |
| t081 | 報導也點名，台灣的巨大和美利達，都受到衝擊。 | #43 | OK | 「供應鏈吃緊衝擊數家大型自行車廠，如台灣巨大和美利達」 |
| t082 | 如果你那兩年想買新車卻被叫去排隊， | #42 #43 | OK | 假設句，說「一部分」 |
| t083 | 原因有一部分在這裡。 | #42 | OK | — |
| t084 | Shimano 自己怎麼說？ | — | OK | 問句 |
| t085 | 公關說，產能已經大幅擴充， | #44 | OK | Ride Media：Ben Hillsdon 是「Shimano's PR & Communication Specialist」，「We have massively upscaled our production capacity」 |
| t086 | 還請客戶，越早下單越好。 | #44 | OK | 「We are encouraging our customers to place orders as soon as possible」 |
| t087 | 二〇二一年它滿一百歲，營收多了四成四， | #41 | OK | BRAIN 2022-02-08「up 44.6% over 2020」 |
| t088 | 營業利益多了將近八成。 | #41 | OK | 「operating income was up 79.3%」 |
| t089 | 這波熱潮，最高衝到哪裡？ | — | OK | 問句 |
| 卡片 boom-peak | {"title": "疫情前後", "stats": [{"value": "3,632 億", "label": "2019 年營收（日圓）"}, {"value": "6,289 億", "label": "2022 年營收（日圓）"} | #39 #40 | OK | 3,632 億、6,289 億、26.9% |
| t090 | 二〇二二年，營收衝到六千兩百八十九億日圓； | #39 #40 | OK | FY2022 營收 628,909 百萬日圓 |
| t091 | 疫情前的二〇一九年，只有三千六百三十二億。 | #39 | OK | 「363.2 billion yen … in 2019」 |
| t092 | 每一百塊營收，有將近二十七塊是營業利益。 | #40 | OK | 169,158÷628,909＝26.9% |
| t093 | 你做生意做到這樣，大概也會覺得好日子不會結束吧？ | — | OK | 對觀眾 |
| t094 | 同年十月的財報，多了一句話： | #46 | OK | road.cc 2022-10-30 |
| t095 | 需求還算穩，但開始有降溫的跡象。 | #46 | OK | 「remained firm, although showing signs of cooling down」 |
| t096 | 降溫，很快變成了急凍。 | — | OK | 轉場 |
| t097 | 二〇二三年，營收少了快四分之一，營業利益直接砍半； | #47 | OK | FY2023 決算短信 −24.6%、營業利益 −50.5% |
| t098 | 腳踏車零件這一塊，掉了將近三成。 | #47 | OK | 「decreased 29.5%」 |
| t099 | 原因是什麼？ | — | OK | 問句 |
| t100 | 財報只給了一句：市場上的庫存，還是太多。 | #47 #77 | SOFTEN | 決算短信不只一句：自行車部門寫了熱潮降溫、歐洲以外通膨與景氣放緩、北美與亞洲零售疲弱，庫存高是其中一項。「只給了一句」不對。建議：「財報說的是：熱潮降溫，市場上的庫存還是太多。」 |
| t101 | 你可以想像：疫情時拚命訂的零件，裝成了車， | #47 #50 | OK | 對觀眾的畫面句 |
| t102 | 停在倉庫和車行裡，等不到人買。 | #47 | OK | — |
| t103 | 台灣呢？ | — | OK | 問句 |
| t104 | 工商時報引公會統計，那年整車出口少了六十三萬台， | #57 | OK | 工商時報 2024-01-26「2023年台灣整車出口量132.39萬台，較2022年足足少了63萬台」（文中「整車」指一般自行車，不含 E-Bike，用詞與原文一致） |
| t105 | 零件出口值縮水超過四成。 | #57 | OK | 「自行車零件出口值更是大幅萎縮逾4成」 |
| t106 | 二〇二四年，營收又少了一點。 | #48 | OK | FY2024 −4.9% |
| t107 | 問題來了：這場崩盤，它事前不知道嗎？ | — | OK | 問句 |
| 卡片 bust-quote | {"text": "早就料到", "kicker": "Shimano 會長對日經亞洲說（2024）", "sub": "We had anticipated that there would eventually be a slump"} | #49 #78 | OK | 「Shimano 會長對日經亞洲說（2024）」；英文原句逐字 |
| t108 | 它知道。那一年，會長島野容三對日經說： | #49 #78 | OK | JTC 轉載：「Chairman Yozo Shimano said in an interview on Feb. 16」（2024）；會長是在世人物，這段用卡片，沒畫他 |
| t109 | 我們早就料到，總有一天會崩。 | #49 | OK | 「We had anticipated that there would eventually be a slump」 |
| t110 | 那為什麼還一直擴產？ | — | OK | 問句 |
| t111 | 他說，高峰時只能先拚產量，其他計畫往後延。 | #49 | OK | 「we had to prioritize increasing production and postpone other projects」 |
| t112 | 還記得那句越早下單越好嗎？ | — | OK | 回呼 |
| t113 | 今年三月，日經寫得更直接： | #50 | OK | 日經亞洲 2026-03-01（Keisuke Takahashi） |
| t114 | Shimano 沒能勸住車廠，別在熱潮裡生產過頭。 | #50 | OK | 「unable to dissuade client bicycle makers from overproducing」 |
| t115 | 我的看法是，這是做零件最難的地方： | — | OK | 意見已標 |
| t116 | 車是客戶做的，要做多少，輪不到你說了算。 | — | OK | 意見 |
| t117 | 就在庫存賣不掉的那一年九月，一個老問題又回來了。 | #47 #64 | OK | 2023 年 9 月 |
| t118 | 九月二十一日，美國消費品安全委員會又發了召回公告。 | #64 | OK | CPSC 2023-09-21 |
| t119 | 又是曲柄。這次是十一速、用黏合做的中空曲柄。 | #64 | OK | 「11-Speed Bonded Hollowtech II Road Cranksets」 |
| t120 | 這次有多少？ | — | OK | 問句 |
| t121 | 美國六十八萬組，加拿大再八萬組。 | #64 | OK | 「About 680,000」「80,000 were sold in Canada」 |
| t122 | 委員會說，曲柄分離的通報有四千五百一十九件。 | #64 | OK | 公告寫「The firm has received 4,519 incidents of cranksets separating」——是公告裡的數字，「委員會說」可接受（要更精確可說「公告說」） |
| t123 | 如果你那幾年買過它比較貴的曲柄， | #64 | OK | 售價 $270–$1,500、售期 2012-01 至 2023-08 |
| t124 | 這份公告值得你回頭查一下。 | #64 | OK | 安全提醒 |
| t125 | 這一次，它付了多少代價？ | — | OK | 問句 |
| t126 | 光是免費檢查這一項，當年就認了一百七十六億日圓的損失。 | #66 | OK | FY2023 特別損失「Loss on free inspection 17,625」百萬日圓 |
| t127 | 開頭那張罰單，二〇二六年三月十六日來了： | #67 | OK | CPSC 2026-03-16 |
| t128 | Shimano 同意付一千一百五十萬美元的民事罰款。 | #67 | OK | 「agreed to pay an $11.5 million civil penalty」 |
| t129 | 罪名呢？ | #67 | OK | 若 t010 改「指控」，這裡可改「指控呢？」 |
| t130 | 跟一九九九年一模一樣：沒有立刻通報。 | #63 #67 | OK | 兩次都是 CPSA 15(b) 的通報義務；前一句問的是罪名（指控），t131 起標「委員會指控」 |
| t131 | 委員會指控，二〇一三到二〇二二年間， | #67 | OK | 新聞稿「resolves CPSC's charges」；協議第 8 段在「STAFF CHARGES」底下 |
| t132 | 它收到了好幾千件保固申訴， | #67 | OK | 「Between 2013 and 2022, Shimano received thousands of warranty claims」——申訴期間，沒跟銷售期間 2012–2023 混 |
| t133 | 還前前後後做了九次製造和設計上的修改。 | #67 | OK | 「nine overall manufacturing and design changes that resulted in over twenty-five individual changes」 |
| t134 | 九次。這是整份檔案裡，我最在意的一個數字。 | — | OK | 旁白反應 |
| t135 | 改了九次卻沒有先報告，這是委員會的說法。 | #67 #68 | OK | 歸屬給委員會 |
| t136 | 那 Shimano 怎麼說？ | — | OK | 問句 |
| t137 | 它在和解協議裡寫明，這不代表它承認指控。 | #68 | OK | 第 15 段「This Agreement does not constitute an admission by Shimano to the staff's charges」 |
| t138 | 協議也寫，檢查換新開始後，就沒有再收到受傷通報。 | #68 #76 | SOFTEN | 第 16 段在「RESPONSE OF SHIMANO」標題底下，是 Shimano 的陳述，不是雙方認定；「協議也寫」要改成「它在協議裡也說」。建議：「它在協議裡也說，檢查換新開始後，就沒有受傷通報了。」 |
| 卡片 recall-compare | {"title": "同一個罪名，兩張罰單", "left": {"heading": "1999 年", "points": ["15 萬美元", "曲柄斷裂、22 人受傷"]}, "right": {"heading": "2026 年 | #63 #67 #68 | OK | 「兩次都沒有承認」有協議第 15、17 段與 1999 新聞稿支持；右欄 4,519 件是 2023 召回公告的數字 |
| t139 | 前面那十五萬美元，這一次變成七十多倍。 | #63 #67 | OK | 1,150 萬÷15 萬≈76.7 |
| t140 | 同一個罪名，兩次，都沒有承認。 | #63 #67 #68 | OK | 有否認；若 t010 改「指控」，這裡也可改「同一種指控」 |
| t141 | 罰單來的隔天，它交出一份年度報告。 | #34 | OK | 有報【提出日】2026年３月17日 |
| t142 | 最大客戶那一欄，寫著一個德國名字。 | #34 | OK | — |
| t143 | 還記得那家斯圖加特的代理商嗎？ | #35 | OK | 回呼 |
| t144 | 它叫保羅朗格，從一九六七年代理到現在。 | #35 | OK | 新聞稿 2025-10-01 仍寫「Seit 1967」 |
| t145 | 去年，它一家就買了將近五百四十億日圓。 | #34 | OK | 53,991 百萬日圓 |
| 卡片 lange-card | {"text": "11.6%", "kicker": "2025 年，Shimano 最大的客戶", "sub": "保羅朗格（Paul Lange & Co.），斯圖加特的代理商"} | #34 #35 | OK | 11.6%、2025 年 |
| t146 | 百分之十一點六，是它最大的一個客戶。 | #34 | OK | 11.6% |
| t147 | 不是捷安特，不是哪一家車廠，是一家代理商。 | #34 #35 | OK | — |
| t148 | 這個答案，我一開始也沒猜到。 | — | OK | 旁白反應 |
| t149 | 為什麼是代理商？ | — | OK | 問句 |
| t150 | 它的生意是兩頭：一頭，車廠買它整組的零件裝車； | #23 | SOFTEN | 「整組賣給車廠」的出處（IDCH）只說到 1991 年和解為止，t054 也說之後車廠可以混搭；現在式的「車廠買它整組的零件」沒有出處。建議：「它的生意是兩頭：一頭，車廠買它的零件裝車；」 |
| t151 | 另一頭，代理商替它把零件賣進一個個國家。 | #35 | OK | 旁白的整理；有報也列 Shimano Europe、North America 等自己的銷售子公司，說「代理商」是其中一頭，可接受 |
| t152 | 台灣也是。二〇〇二年九月，它在台中設了台灣禧瑪諾， | #55 #74 | OK | 經濟部登記：統編 80248308，設立 0910909（2002-09-09），臺中市西區，代表人金澤毅史。股東登記沒列；與 Shimano 的關係靠名稱、日籍代表人與搜尋摘要裡的官網據點頁（shimano.com 對本環境 403，沒能直接讀） |
| t153 | 登記的是自行車和零件的批發，不是工廠。 | #55 #74 | FIX | 重查登記的完整營業項目：除了第一項 F114040 自行車及其零件批發業，還登記了 CD01050「自行車及其零件製造業」、零售、國際貿易、倉儲等。「登記的是…批發，不是工廠」與登記內容不符。建議：「登記的第一項營業，是自行車和零件的批發。」 |
| t154 | 它的工廠不在台灣；你在這裡碰到的，是賣的那一站。 | #36 #78 #79 | SOFTEN | 有報的主要設備與列名子公司、日經 2024 的「major factories」都沒有台灣，有報全文也查不到「台湾」；但有報只列 7 家子公司（另「その他42社」），生產寫「他」。能說的是「主要工廠／年報列的工廠沒有台灣」，不是斷言「工廠不在台灣」。建議：「年報列的主要工廠裡沒有台灣；你在這裡碰到的，是賣的那一站。」 |
| t155 | 去年，日本只占它營收的百分之九點一，其他九成在海外。 | #32 | OK | 42,341÷466,243＝9.1% |
| t156 | 還記得那個捲線器嗎？ | — | OK | 回呼 |
| t157 | 營收裡將近兩成四，是釣具。 | #30 | OK | 23.8% |
| t158 | 可是去年，中國的營收少了三分之一， | #33 | OK | 116,438→78,576（−32.5%） |
| t159 | 財報說，那裡的庫存還是很高。 | #33 | OK | 「market inventories remained at a high level」（中國市場） |
| t160 | 結果呢，歐洲反而多了將近三成。 | #33 | OK | 160,625→206,403（+28.5%） |
| t161 | 我覺得，這就是九成生意在海外的樣子：一邊跌，一邊漲。 | — | OK | 意見已標 |
| t162 | 前面那個最好的年頭，每一百塊賺將近二十七塊； | #40 | OK | 26.9% |
| t163 | 去年，只剩十一塊。 | #29 | OK | 11.1% |
| t164 | 回到開頭的問題：一台車都不賣，它憑什麼？ | — | OK | 問句 |
| t165 | 紀錄說得出來的是：它不跟客戶搶著賣車， | #12 | OK | △ 已在 t026 歸屬 |
| t166 | 賣的是一整組配好的零件， | #23 | SOFTEN | 同 t150：現在式「賣的是一整組配好的零件」超出 #23（到 1991 年為止），也跟 t054 打架。建議：「賣的是零件，早年還配成一整組賣給車廠，」 |
| t167 | 再交給替它把零件賣進各國的代理商。 | #34 #35 | OK | — |
| t168 | 疫情那場熱潮，讓它賺到最高點， | #39 #40 | OK | — |
| t169 | 也讓它跟著做太多車的客戶，一起摔了一跤。 | #47 #50 | OK | 日經「unable to dissuade client bicycle makers from overproducing」 |
| 卡片 close-outro | {"title": "2025 年營收 4,662 億日圓", "cta": "參考資料在說明欄"} | #29 | OK | 4,662 億日圓 |
| t170 | 二〇二五年，這門不賣車的生意，營收四千六百六十二億日圓。 | #29 | OK | 466,243 百萬日圓；含釣具，t157 已交代 |
| t171 | 你現在騎的那台車，變速器是哪一家的？留言告訴我。 | — | OK | 留言題 |
| t172 | 每一份檔案都附出處，想繼續一起翻，就訂閱。 | — | OK | 訂閱 |
| 標題 | Shimano 一台車都不賣，憑什麼年營收 4662 億日圓？｜奇聞檔案局 | #13 #29 #30 | OK | 數字是 2025 年全公司營收（含釣具 23.8%），標題沒說營收全來自腳踏車，片中 t157 有交代；「一台車都不賣」指現在，與 t025 一致 |
| 說明欄 | 一九二一年二月，大阪府堺市，一個年輕人開了一間鐵工廠，隔年開始做腳踏車後輪的飛輪。一百多年後，日經估計運動車零件全球約八成五出自這家公司；它卻一台完整的腳踏車都不賣。  這一集從堺… | #2 #13 #53 #63 #67 #68 | SOFTEN | 內容都對（日經估計、運動車零件、兩次都沒有承認），但整段沒提到營收裡近四分之一是釣具；配上標題的 4662 億，建議補一句「二〇二五年營收 4,662 億日圓，約四分之三是腳踏車零件、近四分之一是釣具。」。另：sources 裡「Tampa Bay Times 1997（美聯社）」的「美聯社」要拿掉（見 t062）；「畫中人物都是不指認的一般人物，不畫創辦人」要等下方畫面問題改完才成立 |
| 縮圖 | {"headline": "一台車\n**都不賣**", "tag": "品牌奇聞", "sub": "營收 4662 億日圓", "shot": "open-share"} | #13 #29 | OK | 底圖 open-share 是無名技師、無標記齒盤 |

## 畫面規則（提示詞逐張看過）

- 沒有品牌、產品或真人名字（查 Shimano、SRAM、Giant、Merida、Nissan、Dura-Ace、Hollowtech、logo、brand 都沒有）；零件都寫 plain／unmarked。
- **要改**：`sakai-founder`（t013「那個年輕人叫島野庄三郎」配「a young 1920s craftsman … in the doorway of a small wooden ironworks」）——旁白直接點名畫中人，等於畫本人；`close-question`（「the young 1920s craftsman … at his workshop doorway」）用定冠詞與 his workshop 把同一個人叫回來。建議：`sakai-founder` 改成「Medium shot of an elderly neighbourhood blacksmith in a leather apron at his open forge across a narrow 1920s street, pausing with his hammer raised to glance toward a newly opened workshop with a blank wooden sign, mild overcast morning light」；`close-question` 改成現代騎士「Medium shot of a young rider in a cycling cap at dusk outside a small bike shop holding a small plain gear in his open palm, looking thoughtful, soft lamp light」。
- **建議一起改**（同一個年輕匠人，旁白用「一個年輕人」「他」指創辦人，觀眾會把他認成本人）：`open-sakai`（t004–t005）、`open-gear`（t006）、`sakai-you`（t019「換成你是他」）、`sakai-freewheel`（t021）、`sakai-why`（t014「他的鐵工廠」）。做法：只畫手（hands only, face out of frame）或換成另一個不同年紀、不同裝束的無名人物（鄰居、學徒、送貨的孩子）。brief 允許「1920 年代堺的工坊匠人只當無名的年代人物」，但前提是不指認——跟著旁白一路出現就成了指認。
- `bust-why`（t111「他說，高峰時只能先拚產量」）畫的是「floor manager … waving workers on」，緊跟在會長的引言卡後面，容易被讀成會長本人；建議改成工人視角（「a line worker in a cap … glancing up at a speeding production line」）。
- 可能畫出可讀字的：`open-wait`、`crank-crime`（wall calendar，「pointing at one late date」）、`bust-freeze-b`（desk calendar）、`crank-small`（banknotes）、`crank-fine-b`（cheque）、`close-answer-b`（map-covered wall）、`recall-cost`（calculator）。建議都加 blank／unnumbered／unlabelled（例：「a blank wall calendar grid with no numbers」「plain unlabelled map」「plain paper money with no printing」）。評審的文字題會抓，但先寫進提示詞比較省重畫。

## 逐項查核（抄自 `topic-checks/B02.md`，2026-10-31）

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | 創業年月與地點 | CONFIRMED（只到月） | 有報沿革：「1921年２月 初代取締役社長島野庄三郎が大阪府堺市東湊町３丁において島野鉄工所を創立」。**查不到「哪一天」**，旁白只說「1921 年 2 月」 | シマノ有価証券報告書（2026-03-17 提出，第119期） | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 2 | 第一個產品是飛輪 | CHANGED | 同一句接著寫「その翌年に自転車部品のフリーホイールの製造を開始」——飛輪是 **1922 年**才開始做。**旁白改成「開業第二年開始做腳踏車的飛輪」** | 同上；EDINET DB 轉錄 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf ；https://edinetdb.jp/company/E02257/history | ✅ |
| 3 | 創業時的規模 | CONFIRMED（二手） | 「26歳の島野庄三郎氏が堺市東湊町の12坪を月5円で借り、旋盤1台の島野鉄工所を起こした」 | the-shashi（企業史整理站） | https://the-shashi.com/tse/7309/ceo/ | △ |
| 4 | 飛輪是什麼 | CONFIRMED | 「自転車の後輪に付く、ペダルを止めても車輪が回り続けるギヤ『フリーホイール』の生産に乗り出す」（PRESIDENT 2015-10-19 號，新加坡大使館贊助的廣告企劃） | PRESIDENT Online | https://president.jp/articles/-/16224 | △（廣告企劃） |
| 5 | 島野庄三郎的生卒年 | CONFIRMED | 國會圖書館典藏《島野庄三郎伝》（島野工業，1959 年出版）的主題標目「島野, 庄三郎, 1894-1958」；the-shashi：「庄三郎氏は1958年まで会社を率い」。**1958 年過世，至 2026 年只有 68 年，未滿 70 年，本系列不畫他本人**（也不畫島野家任何人） | 國立國會圖書館搜尋 API（書目記錄頁當天回 503，標目由 API 讀取）；the-shashi | https://ndlsearch.ndl.go.jp/api/opensearch?any=%E5%B3%B6%E9%87%8E%2C%20%E5%BA%84%E4%B8%89%E9%83%8E%2C%201894&cnt=5 ；https://ndlsearch.ndl.go.jp/books/R100000002-I000001070234 | ✅ |
| 6 | 創業者的背景 | CONFIRMED（二手） | 「Rather than follow his father into farming, Shozaburo had apprenticed at an iron works after high school.」 | FundingUniverse（International Directory of Company Histories 轉載） | https://www.fundinguniverse.com/company-histories/shimano-inc-history/ | △ |
| 7 | 堺：古墳→鐵砲、菜刀→修腳踏車 | CONFIRMED | 堺市政府：「堺の自転車産業のルーツは、約1600年前に築かれた百舌鳥古墳群にあります。古墳築造を支えた鉄加工技術は、鉄砲や包丁づくりへと発展し、明治時代には輸入自転車の修理にも活用されました。」 | 堺市「自転車のまち堺」頁 | https://www.city.sakai.lg.jp/kurashi/doro/jitensha/index.html | ✅ |
| 8 | 堺以刀與槍管聞名 | CONFIRMED（二手） | 「The town was a legendary blacksmithing center known for its swords and gun barrels.」 | FundingUniverse | https://www.fundinguniverse.com/company-histories/shimano-inc-history/ | △ |
| 9 | 堺有 Shimano 的自行車博物館 | CONFIRMED | 「日本唯一のシマノ自転車博物館やツアー・オブ・ジャパン堺ステージなど、自転車文化が地域に根付いています」 | 堺市 | https://www.city.sakai.lg.jp/kurashi/doro/jitensha/index.html | ✅ |
| 10 | 公司化與改名 | CONFIRMED | 1940-01「株式会社組織に改め、社名を株式会社島野鉄工所に変更」；1951-02「社名を島野工業株式会社に変更」；1991-03「社名を株式会社シマノに変更」 | 有報沿革 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 11 | 1951 年併了一家「島野自転車」 | CONFIRMED（存在）／用途 UNVERIFIED | 1951-02「島野自転車株式会社(資本金2,300万円)を吸収合併」。**這家公司做什麼查不到**，所以旁白不說「Shimano 從來沒做過一台車」，只說「現在不賣完成車」 | 有報沿革 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅／⚠ |
| 12 | 「絕不跟客戶競爭」 | CONFIRMED（二手轉引） | 「"Our founder said, 'never ever compete with a customer,'" remarked one of Shimano's sons to the Straits Times.」原報（Straits Times 2003-08-03）沒讀到，**旁白說「據新加坡《海峽時報》報導，島野家的人這樣說」** | FundingUniverse；Encyclopedia.com（同一份 IDCH 文本） | https://www.fundinguniverse.com/company-histories/shimano-inc-history/ ；https://www.encyclopedia.com/books/politics-and-business-magazines/shimano-inc | △ |
| 13 | 現在只做零件與釣具 | CONFIRMED | 有報：「自転車部品事業では、変速機等の駆動用部品、ブレーキ等の制動用部品、その他の自転車部品及び関連用品の製造・販売」；其他兩個事業是釣具與「ロウイング関連用品等」 | 有報「事業の内容」 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 14 | 進入美國 | CONFIRMED | 1965-03「米国、ニューヨーク市に現地法人Shimano American Corporationを設立」 | 有報沿革 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 15 | 進入歐洲 | CONFIRMED | 1972-08「西ドイツ、デュッセルドルフ市に現地法人Shimano(Europa)GmbHを設立」；FundingUniverse：成立時「with just two employees」 | 有報沿革；FundingUniverse | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf ；https://www.fundinguniverse.com/company-histories/shimano-inc-history/ | ✅ |
| 16 | 第一座海外工廠 | CONFIRMED | 1973-05 新加坡設 Shimano(Singapore)Pte.Ltd.；BRAIN：「Shimano first opened a Singapore facility in 1973; it was the company's first assembly plant outside of Japan.」 | 有報沿革；Bicycle Retailer | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf ；https://bicycleretailer.com/international/2021/07/11/report-shimano-invest-179-million-singapore-factory | ✅ |
| 17 | 上市 | CONFIRMED | 1972-11 大證二部上市；1973-10「大阪証券取引所、東京証券取引所の市場第1部に上場」 | 有報沿革 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 18 | 1970 年代美國腳踏車熱 | CONFIRMED | 1982 年報導：「in 1972, more bikes were bought than cars」；「the 1973 high of 15.2 million bikes sold」 | Christian Science Monitor 1982-07-21 | https://www.csmonitor.com/1982/0721/072106.html | ✅ |
| 19 | 歐洲廠產能跟不上、日本廠補位 | UNVERIFIED | 只有 Wikipedia 無註腳的段落：「When the 1970s United States bike boom exceeded the capacity of the European bicycle component manufacturers, Japanese manufacturers SunTour and Shimano rapidly stepped in」。**旁白不說「歐洲人做不出來」**，只說「1974 年在加州開了辦公室，正好接上美國的熱潮」（FundingUniverse：「Opening a sales office in California in 1974, the company was well placed to ride the booming bike market」） | Wikipedia（索引）；FundingUniverse | https://en.wikipedia.org/wiki/Shimano ；https://www.fundinguniverse.com/company-histories/shimano-inc-history/ | ⚠／△ |
| 20 | Dura-Ace 1973 年 | CONFIRMED（二手） | 「The Dura-Ace name goes back to at least 1973」；「Dura-Ace was always Shimano's attempt to make a top-of-the-line parts group, but it was not really successful until 1984.」 | Sheldon Brown | https://www.sheldonbrown.com/dura-ace.html | △ |
| 21 | SIS 段數定位變速 | CONFIRMED（年份用 1984） | 「In 1984, Shimano introduced Dura-Ace S.I.S. (Shimano Indexing System)」；時間表「1984 7400 … 6-speed S.I.S. shifting」。常見的「1985」是普及到中低階的年式，**旁白說「1984 年先放在最高階的 Dura-Ace」** | Sheldon Brown | https://www.sheldonbrown.com/dura-ace.html | △ |
| 22 | STI 煞變把 1990 年 | DISPUTED（旁白說「1990 年代初」） | Sheldon 時間表把 Dura-Ace 的 STI 記在「1991 7403 STI brake/shifters, Dual-pivot brakes」；1990 是常見說法但官方年表讀不到 | Sheldon Brown | https://www.sheldonbrown.com/dura-ace.html | ⚠ |
| 23 | 「整組賣」的做法 | CONFIRMED（二手） | 「Shimano sold its shifters and derailleurs to bike manufacturers as complete sets until a California antitrust lawsuit by SRAM, which was settled in 1991」 | Encyclopedia.com／FundingUniverse 的 SRAM 公司史（IDCH） | https://www.encyclopedia.com/books/politics-and-business-magazines/sram-corporation ；https://www.fundinguniverse.com/company-histories/sram-corporation-history/ | △ |
| 24 | SRAM 1987 年成立 | CONFIRMED（二手） | 「SRAM Corporation was started in Chicago in 1987 by Stanley R. Day」；起家產品是轉把式變速器 Grip Shift | FundingUniverse SRAM | https://www.fundinguniverse.com/company-histories/sram-corporation-history/ | △ |
| 25 | SRAM 告 Shimano 反托拉斯 | CONFIRMED（和解年）／金額 DISPUTED | 和解在 **1991 年**；金額只有「an estimated $3 million to $5 million」，其他整理寫「unspecified」。起訴年（常見寫 1990）只見 Wikipedia。**旁白不講金額，也不說「SRAM 贏了」**，只說「1991 年庭外和解，之後車廠可以混搭別家零件」 | Encyclopedia.com SRAM | https://www.encyclopedia.com/books/politics-and-business-magazines/sram-corporation | △／⚠ 金額 |
| 26 | 1990 年代初 Shimano 的市占 | CONFIRMED（二手估計） | 同一段：「The bike components business was then dominated by Japan's Shimano Inc., which had an 85 percent market share.」**是哪一塊市場、怎麼算的沒寫** | Encyclopedia.com SRAM | https://www.encyclopedia.com/books/politics-and-business-magazines/sram-corporation | △ |
| 27 | 2001 年 SRAM 在歐盟反傾銷 | CONFIRMED（二手） | 「In 2001, SRAM's German subsidiary filed an anti-dumping complaint with the European Union against rival Shimano.」 | FundingUniverse SRAM | https://www.fundinguniverse.com/company-histories/sram-corporation-history/ | △ |
| 28 | 釣具：1970 年開始 | CONFIRMED | 1970-02「釣用リールの製造を開始」；1971-01「島野足立株式会社を設立し、釣用竿の製造を開始」 | 有報沿革 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 29 | 最新年度營收與獲利（FY2025） | CONFIRMED | 營收 466,243 百萬日圓（+3.4%）；營業利益 51,677（−20.6%）；歸屬母公司淨利 33,991（−55.5%）；營業利益率「Operating income to net sales 11.1%」 | FY2025 決算短信（2026-02-10） | https://finance-frontend-pc-dist.west.edge.storage-yahoo.jp/disclosure/20260210/20260209552874.pdf | ✅ |
| 30 | 自行車零件 vs 釣具占比 | CONFIRMED（自算） | 自行車零件 354,972（+2.7%）、釣具 110,832（+5.6%）、其他 439。占比：354,972÷466,243＝**76.1%**；110,832÷466,243＝**23.8%** | 同上；有報「販売実績」同數 | https://finance-frontend-pc-dist.west.edge.storage-yahoo.jp/disclosure/20260210/20260209552874.pdf | ✅ |
| 31 | 自行車零件的利潤率 | CONFIRMED（自算） | 自行車部門營業利益 42,841 百萬日圓（−20.9%）→ 42,841÷354,972＝**12.1%**；釣具 8,865÷110,832＝8.0% | 同上 | 同上 | ✅ |
| 32 | 海外營收比例 | CONFIRMED（自算） | FY2025 依客戶所在地：日本 42,341、北美 48,423、歐洲 206,403、亞洲 145,686、其他 23,388。日本只占 42,341÷466,243＝**9.1%**，海外約 **91%** | 同上，地區別資訊 | 同上 | ✅ |
| 33 | 2025 年中國掉三分之一、歐洲大漲 | CONFIRMED（自算）—**故事轉折** | 中國：FY2024 116,438 → FY2025 78,576（**−32.5%**）；德國 48,360 → 67,403；歐洲合計 160,625 → 206,403（+28.5%）。決算短信：中國「demand for road bikes showed signs of easing … market inventories remained at a high level」 | 同上 | 同上 | ✅ |
| 34 | 最大客戶是德國代理商 | CONFIRMED—**故事轉折** | 有報「主な相手先別の販売実績」：「PAUL LANGE & CO. OHG … 53,991（百万円）11.6（％）」（上一年未達 10% 不揭露） | 有報 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 35 | Paul Lange 是誰 | CONFIRMED | 「Seit 1967 ist das im April 1949 gegründete Stuttgarter Unternehmen der deutsche Generalvertreter für SHIMANO Komponenten.」 | Paul Lange 官方新聞稿 | https://presse.paul-lange.de/pressreleases/paul-lange-und-co-strengthens-portfolio-with-acquisition-of-milremo-expert-in-custom-clothing-3404061 | ✅ |
| 36 | 生產地點 | CONFIRMED（越南 UNVERIFIED） | 有報主要設備：日本堺本社、下關工廠；Shimano(Singapore)、Shimano Components(Malaysia)（柔佛）、PT Shimano Batam（印尼）、Shimano(Kunshan)（中國昆山）、Shimano Czech Republic（卡爾維納）；特定子會社另有 Shimano(Philippines)、天津廠。**有報裡沒有越南生產據點，旁白不提越南** | 有報「設備の状況」「関係会社」 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 37 | 海外廠設立年 | CONFIRMED | 馬來西亞 1990-01；昆山 1992-10；天津 2003-04 | 有報沿革 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 38 | 員工數 | CONFIRMED | 2025-12-31 連結員工 10,242 人（另臨時 3,133）；其中自行車零件 6,633 人 | 有報「従業員の状況」 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 39 | 疫情前後營收 | CONFIRMED | 「Net sales and income reached record highs of 628.9 billion yen and 128.1 billion yen in 2022, a great leap from the 363.2 billion yen and 51.8 billion yen in 2019.」（628.9÷363.2＝1.73 倍） | 日經亞洲 2024-02 專訪，新加坡裕廊集團（JTC）轉載 | https://www.jtc.gov.sg/juronginnovationdistrict/story-articles/bicycle-parts-maker-shimano-seeks-growth-with-new-singapore-plant | ✅ |
| 40 | 2022 年的利潤率 | CONFIRMED | FY2022：營收 628,909、營業利益 169,158，營業利益率 **26.9%**（FY2025 只剩 11.1%） | FY2023 決算短信（附前期） | https://finance.stockweather.co.jp/contents/dispPDF.aspx?disclosure=20240207528856 | ✅ |
| 41 | 2021 年百年紀念年創紀錄 | CONFIRMED | 「Company-wide, Shimano's sales last year were up 44.6% over 2020, while operating income was up 79.3%.」自行車部門「net sales were up 49.0% to 443.7 billion yen」 | Bicycle Retailer 2022-02-08 | https://bicycleretailer.com/industry-news/2022/02/08/its-centennial-year-shimano-hits-record-revenues-and-earnings | ✅ |
| 42 | 交期 400 天 | CHANGED（是車廠說的） | FT 2021-05-31 經 MoneyDJ 轉述：「歐洲和美國業者說，Shimano生產的一系列高階零組件，下單到出貨的前置時間（lead time）長達400天」；Ride Media 2021-01：「Some companies are reporting delays of as much as 400 days for orders placed with Shimano.」**旁白說「有車廠說要等 400 天」，不說「Shimano 交期 400 天」** | TechNews（MoneyDJ 授權轉載 FT）；Ride Media | https://technews.tw/2021/06/01/bicycle-parts-shortage/ ；https://www.ridemedia.com.au/articles/shimano-update-part-1-we-have-massively-upscaled-our-production-capacity/ | △ |
| 43 | 小車廠被砍貨 | CONFIRMED（二手轉述） | 同一篇 FT 轉述：LeMond「上半年Shimano交貨減少80%等供給問題，迫使產品延後4個月問世」；並點名「台灣巨大和美利達」受衝擊 | TechNews | https://technews.tw/2021/06/01/bicycle-parts-shortage/ | △ |
| 44 | Shimano 自己怎麼說缺貨 | CONFIRMED | Shimano 公關 Ben Hillsdon：「We have massively upscaled our production capacity」；「In the last quarter of 2020, we achieved record outputs for the company」；「We are encouraging our customers to place orders as soon as possible」 | Ride Media 2021-01-21 | https://www.ridemedia.com.au/articles/shimano-update-part-1-we-have-massively-upscaled-our-production-capacity/ | ✅ |
| 45 | 為缺貨蓋新廠 | CONFIRMED | 「Shimano is investing about 20 billion yen ($179 million) to build a new plant in Singapore amid a surge in demand in the wake of the coronavirus pandemic, its newly appointed president, Taizo Shimano, has told Nikkei Asia.」（2021-07-11）；2024 年：「The plant went online in 2023 … Investing 25 billion yen」 | 日經亞洲；JTC 轉載 | https://asia.nikkei.com/business/companies/bicycle-parts-maker-shimano-invests-179m-to-build-singapore-plant ；https://www.jtc.gov.sg/juronginnovationdistrict/story-articles/bicycle-parts-maker-shimano-seeks-growth-with-new-singapore-plant | ✅ |
| 46 | 熱潮降溫的第一個訊號 | CONFIRMED | 2022 年前三季財報：需求「remained firm, although showing signs of cooling down」 | road.cc 2022-10-30 | https://road.cc/content/news/high-demand-bikes-cooling-down-says-shimano-296959 | ✅ |
| 47 | 2023 年庫存過剩、營收崩 | CONFIRMED | FY2023 營收 474,362（**−24.6%**）、營業利益 −50.5%；自行車零件「decreased 29.5% … to 364,679 million yen」；「market inventories generally remained high」 | FY2023 決算短信 | https://finance.stockweather.co.jp/contents/dispPDF.aspx?disclosure=20240207528856 | ✅ |
| 48 | 2024 年續跌 | CONFIRMED | FY2024 營收 450,993（−4.9%）；「retail sales of completed bicycles were weak and market inventories remained high」 | FY2024 決算短信 | https://contents.xj-storage.jp/xcontents/AS02673/b86e89fb/6eae/49e7/b21e/ca5e2f795c95/140120250207567352.pdf | ✅ |
| 49 | 會長：「早就料到會崩」 | CONFIRMED—**故事轉折** | 會長島野容三：「We had anticipated that there would eventually be a slump」；同一篇：高峰時「we had to prioritize increasing production and postpone other projects」 | 日經亞洲 2024，JTC 轉載 | https://www.jtc.gov.sg/juronginnovationdistrict/story-articles/bicycle-parts-maker-shimano-seeks-growth-with-new-singapore-plant | ✅ |
| 50 | 但勸不住客戶多做車 | CONFIRMED—**故事轉折** | 日經亞洲 2026-03-01：「The Japanese company was unable to dissuade client bicycle makers from overproducing during outdoor activity booms in the first half of the decade.」 | 日經亞洲 | https://asia.nikkei.com/business/companies/japan-s-shimano-struggles-with-excess-bicycle-stock-in-europe-and-china | ✅ |
| 51 | 2025 年淨利腰斬的原因 | CONFIRMED | 經常利益 47,029（−52.3%）；有報損益表：為替差損 19,626 百萬日圓（前一年是為替差益 12,227） | FY2025 決算短信；有報 | https://finance-frontend-pc-dist.west.edge.storage-yahoo.jp/disclosure/20260210/20260209552874.pdf ；https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 52 | 2026 年至今 | CONFIRMED | 2026 前九個月：全公司「sales were up 6.9% to ¥375 billion」；自行車零件「increased 4.6% to ¥278.4 billion」；北美完成車「remained weak」，部分因關稅推高售價 | Bicycle Retailer 2026-10-27 | https://bicycleretailer.com/international/2026/10/27/shimano-bike-division-sales-5-year-date | ✅ |
| 53 | 「全世界七、八成的腳踏車用 Shimano」 | CHANGED | 能找到的數字各說各的、**沒有一個是「全世界的腳踏車」**：日經 2024「mainly for sports bikes like road bikes and mountain bikes, with an estimated global share of 85%」；FT 2021「掌控高階自行車零組件65%市場」；IDCH 約 2004 年「an estimated 70 percent share of the world market for bike parts」；Shimano 自己的有報**沒有寫市占**（全文查「シェア」無結果）。**旁白說「運動車零件，外界估計大約八成以上用 Shimano」並標明是估計** | 日經（JTC 轉載）；TechNews；FundingUniverse；有報 | https://www.jtc.gov.sg/juronginnovationdistrict/story-articles/bicycle-parts-maker-shimano-seeks-growth-with-new-singapore-plant ；https://technews.tw/2021/06/01/bicycle-parts-shortage/ ；https://www.fundinguniverse.com/company-histories/shimano-inc-history/ | ⚠ |
| 54 | 「以金額計占全球零件 85%」 | UNVERIFIED | Wikipedia 引 Credit Suisse 2016-10-24 研究報告 p.16：「an estimated 85% of the global bicycle component market by value」；報告本身沒讀到 | Wikipedia（索引） | https://en.wikipedia.org/wiki/Shimano | ⚠ |
| 55 | 台灣禧瑪諾 | CONFIRMED | 公司登記：「台灣禧瑪諾股份有限公司」，統編 80248308，設立 2002-09-09（民國 91 年），臺中市西區，資本額 675 萬元；第一項營業項目「自行車及其零件批發業」。有報主要生產據點裡沒有台灣，**是銷售／服務據點，不是工廠** | 經濟部商業司公司登記開放資料 API | https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?$format=json&$filter=Company_Name%20like%20%E7%A6%A7%E7%91%AA%E8%AB%BE&$skip=0&$top=50 | ✅ |
| 56 | 禧瑪諾這個中文名 | CONFIRMED | 台灣登記名稱即「台灣禧瑪諾」（列 55）。名稱由來查不到，**旁白不解釋字義** | 同上 | 同上 | ✅ |
| 57 | 台灣自行車出口（疫情高峰） | CONFIRMED | 2022 年電動輔助車出口「103.61萬台的歷史新高峰」；2023 年一般整車出口「132.39萬台，較2022年足足少了63萬台」，零件出口值「大幅萎縮逾4成」 | 工商時報 2024-01-26（引公會草本統計） | https://www.ctee.com.tw/news/20240126700178-430503 | △ |
| 58 | 台灣自行車出口（2025） | CONFIRMED | 公會草本統計：整車出口值「7.43億美元，年減27.77％」；E-bike「6.68億美元，僅年減0.6％」；關鍵零組件「14.64億美元，年增4.6％」 | 工商時報 2026-01-20 | https://www.ctee.com.tw/news/20260120701898-430503 | △ |
| 59 | 台灣零件出口回升 | CONFIRMED | 公會理事長吳盈進：「自行車的零件出口，已連14個月正成長，今年度前二個月出口金額成長13.55%」 | 經濟日報 2026-03-30 | https://money.udn.com/money/story/5607/9412388 | △ |
| 60 | 傳動系統占一台車價值幾成 | UNVERIFIED | 查不到任何有出處的比例。**旁白不講百分比** | — | — | ⚠ |
| 61 | 1997 年曲柄召回 | CONFIRMED | CPSC 1997-07-01：北美「more than 1 million cranks」；「more than 630 reports of cranks breaking in North America resulting in 22 injuries」；裝在「more than 200 models of bicycles … sold under at least 49 brand names」 | 美國消費品安全委員會（CPSC） | https://www.cpsc.gov/Recalls/1997/CPSC-Shimano-Announce-Recall-of-Bicycle-Components | ✅ |
| 62 | 1997 年全球 250 萬台、捷安特也在內 | CONFIRMED | 美聯社稿：「recalling 2.5-million mountain bikes」；歐洲「1.5-million bikes」；品牌包括「Bianchi, Diamondback, GT, Giant, Huffy, Schwinn, Trek and Univega」 | Tampa Bay Times 1997-07-23 檔案 | https://www.tampabay.com/archive/1997/07/23/2-5-million-mountain-bikes-with-faulty-shimano-cranks/ | ✅ |
| 63 | 1999 年因「晚報」被罰 | CONFIRMED—**故事轉折** | CPSC 1999-07-07：Shimano American Corp. 同意付「a civil penalty of $150,000」；「CPSC alleges that Shimano knew of cranks breaking, resulting in 22 injuries, before it reported to CPSC」；Shimano 否認有缺陷、否認違反通報義務 | CPSC | https://www.cpsc.gov/Newsroom/News-Releases/1999/Shimano-to-Pay-150000-Civil-Penalty-for-Alleged-Delay-in-Reporting-Defect-with-Bicycle-Cranks | ✅ |
| 64 | 2023 年 Hollowtech II 召回 | CONFIRMED | 2023-09-21；美國「About 680,000 (In addition, 80,000 were sold in Canada)」；「The firm has received 4,519 incidents of cranksets separating」；產地「Japan」；售期 2012-01 至 2023-08，「for between $270 and $1,500」 | CPSC | https://www.cpsc.gov/Recalls/2023/Shimano-Recalls-Cranksets-for-Bicycles-Due-to-Crash-Hazard | ✅ |
| 65 | 全球 280 萬組 | CONFIRMED（二手） | 「more than 760,000 affected in North America and 2.8 million globally」；Shimano 自己的文件裡沒讀到這個數字 | BikeRadar 2023-09-21 | https://www.bikeradar.com/news/shimano-crankset-recall | △ |
| 66 | 召回花了多少 | CONFIRMED | FY2023 特別損失「Loss on free inspection 17,625」（百萬日圓）；註記：2019-06-30 以前生產的 11 速黏合曲柄「show bonding separation and delamination」 | FY2023 決算短信 | https://finance.stockweather.co.jp/contents/dispPDF.aspx?disclosure=20240207528856 | ✅ |
| 67 | 2026 年再因「晚報」被罰 1,150 萬美元 | CONFIRMED—**故事轉折** | CPSC 2026-03-16：「Shimano, Inc., of Japan, and Shimano North America Holding, Inc. … have agreed to pay an $11.5 million civil penalty」；「Between 2013 and 2022, Shimano received thousands of warranty claims」；「made nine overall manufacturing and design changes that resulted in over twenty-five individual changes」 | CPSC 新聞稿；Bicycle Retailer | https://www.cpsc.gov/Newsroom/News-Releases/2026/Shimano-Agrees-to-Pay-11-5-Million-Civil-Penalty-for-Failure-to-Immediately-Report-Bicycle-Cranksets-that-Posed-a-Crash-Hazard ；https://bicycleretailer.com/recalls/2026/03/16/shimano-agrees-115m-cpsc-penalty-crank-recall | ✅ |
| 68 | Shimano 不承認 | CONFIRMED | 和解協議第 15 段：「This Agreement does not constitute an admission by Shimano to the staff's charges」；第 16 段：檢查換新計畫開始後「there have been no reported injuries by consumers」。**旁白一定要說「CPSC 指控」「Shimano 沒有承認」**；協議是「provisionally accepted」 | CPSC 和解協議（Docket 26-C0002） | https://www.cpsc.gov/s3fs-public/Provisional-Acceptance-Shimano-Civil-Penalty-Settlement-Agreement-Dkt-26-C0002.pdf | ✅ |
| 69 | 美國集體訴訟和解 | CONFIRMED | 「A US court has granted final approval of the settlement in the class action case」（2026-02-05）；被告「Shimano, Specialized and Trek」 | BikeRadar | https://www.bikeradar.com/news/shimano-crankset-lawsuit-granted-final-court-approval | ✅ |
| 70 | 家族經營 | CONFIRMED（現任）／歷代 △ | 有報：代表取締役會長兼 CEO 島野容三（1948 年生）、代表取締役社長島野泰三（1966 年生，2021-03 就任）；the-shashi：「2021年就任の島野泰三氏まで6代すべてが島野家で、外部から社長を招いた例はない」 | 有報「役員の状況」；the-shashi | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf ；https://the-shashi.com/tse/7309/ceo/ | ✅／△ |
| 71 | 疫情時市值超越日產 | CONFIRMED（標題） | 日經亞洲評論標題「How bicycle parts maker Shimano eclipsed Nissan in market cap」（2020-08-05）；內文「the share price of Shimano … hit another all-time high this month」。**具體市值數字沒讀到，旁白不報數字** | 日經亞洲 | https://asia.nikkei.com/spotlight/comment/how-bicycle-parts-maker-shimano-eclipsed-nissan-in-market-cap | ✅ |
| 72 | 環法中立服務車換成 Shimano | CONFIRMED | 「blue Shimano cars replace the yellow ones」，Mavic 做了「almost four decades」 | Ride Media 2021-01-21 | https://www.ridemedia.com.au/articles/shimano-update-part-1-we-have-massively-upscaled-our-production-capacity/ | ✅ |
| 73 | 1997 年 250 萬台的出處與範圍（查核代理 2026-10-31 補） | CHANGED | 原頁導語「Makers of Shimano bicycle parts are recalling 2.5-million mountain bikes」；「The voluntary recall affects about 1-million bikes in North America … planned to recall 1.5-million bikes in Europe」。頁面 credits 空白，全文沒有 Associated Press／AP | Tampa Bay Times 檔案頁 | https://www.tampabay.com/archive/1997/07/23/2-5-million-mountain-bikes-with-faulty-shimano-cranks/ | ✅ 數字／⚠ 署名 |
| 74 | 台灣禧瑪諾的完整營業項目（查核代理 2026-10-31 補） | CHANGED | 共 36 項：F114040 自行車及其零件批發業、F214040 零售業、F401010 國際貿易業、**CD01050 自行車及其零件製造業**、G801010 倉儲業等；代表人金澤毅史；登記不列股東 | 經濟部公司登記（營業項目 API） | https://data.gcis.nat.gov.tw/od/data/api/236EE382-4942-41A9-BD03-CA0709025E7C?$format=json&$filter=Business_Accounting_NO%20eq%2080248308&$skip=0&$top=50 | ✅ |
| 75 | 2023 召回的受傷數（查核代理 2026-10-31 補，旁白不用） | CONFIRMED | 「The firm has received 4,519 incidents of cranksets separating, and six reported injuries」 | CPSC 2023 召回頁 | https://www.cpsc.gov/Recalls/2023/Shimano-Recalls-Cranksets-for-Bicycles-Due-to-Crash-Hazard | ✅ |
| 76 | 和解協議的結構（查核代理 2026-10-31 補） | CONFIRMED | 第 5–14 段標題「STAFF CHARGES」（第 8 段另有「dozens of reports of consumers globally sustaining personal injuries」）；第 15–17 段標題「RESPONSE OF SHIMANO」，第 16 段「there have been no reported injuries by consumers」是 Shimano 的陳述；「Provisionally accepted and Order issued on the 12th day of March, 2026」；新聞稿「resolves CPSC's charges」 | CPSC 和解協議 26-C0002；CPSC 2026 新聞稿 | https://www.cpsc.gov/s3fs-public/Provisional-Acceptance-Shimano-Civil-Penalty-Settlement-Agreement-Dkt-26-C0002.pdf | ✅ |
| 77 | FY2023 財報怎麼解釋衰退（查核代理 2026-10-31 補） | CONFIRMED | 「Although the booming popularity of bicycles cooled down … market inventories generally remained high」；歐洲以外「consumer demand waned on account of inflation and an economic slowdown」；北美「retail sales of completed bicycles remained weak」 | FY2023 決算短信 | https://finance.stockweather.co.jp/contents/dispPDF.aspx?disclosure=20240207528856 | ✅ |
| 78 | 日經 2024 的日期與工廠清單（查核代理 2026-10-31 補） | CONFIRMED | 「Chairman Yozo Shimano said in an interview on Feb. 16」；「first published by Nikkei Asia on March 6, 2024」；「Shimano has major factories in Japan, Singapore, Indonesia, Malaysia, the Philippines, China and the Czech Republic」 | JTC 轉載日經亞洲 | https://www.jtc.gov.sg/juronginnovationdistrict/story-articles/bicycle-parts-maker-shimano-seeks-growth-with-new-singapore-plant | ✅ |
| 79 | 有報有沒有台灣（查核代理 2026-10-31 補） | CONFIRMED（範圍有限） | 全文查「台湾」「Taiwan」無結果；関係会社只列 7 家、另「その他42社」（連結子会社 49 社）；自行車部品「当社及び連結子会社である…他が製造及び販売」 | 有報 | https://disclosure2dl.edinet-fsa.go.jp/searchdocument/pdf/S100XQSE.pdf | ✅ |
| 80 | 公關的職稱（查核代理 2026-10-31 補） | CONFIRMED | 「Ben Hillsdon, Shimano's PR & Communication Specialist」 | Ride Media 2021-01-21 | https://www.ridemedia.com.au/articles/shimano-update-part-1-we-have-massively-upscaled-our-production-capacity/ | ✅ |
| 81 | 日經 2026 與 2020 的署名（查核代理 2026-10-31 補） | CONFIRMED | 2026：KEISUKE TAKAHASHI，March 1, 2026；2020：MAKOTO KAJIWARA，「Nikkei commentator」，August 5, 2020，內文只說股價創新高、沒寫市值數字 | 日經亞洲 | https://asia.nikkei.com/business/companies/japan-s-shimano-struggles-with-excess-bicycle-stock-in-europe-and-china ；https://asia.nikkei.com/spotlight/comment/how-bicycle-parts-maker-shimano-eclipsed-nissan-in-market-cap | ✅ |
