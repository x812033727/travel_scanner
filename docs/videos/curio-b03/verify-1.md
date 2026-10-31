# curio-b03 查核第一輪

- 查核者：獨立查核代理（Claude Opus 5.5，沒有參與撰稿），2026-10-31。逐句讀 `video.json` 的旁白、卡片、`youtube.title`、`youtube.description`、`thumbnail.data` 與 121 張插圖提示詞；`claims.md` 只當待驗的主張。
- 重新開頁：BBC 2007 與 2013 新聞稿、BBC Trust 檢討報告 PDF 與兩個 Trust 頁、《衛報》2007／2009-04／2009-09／2011／2013 五篇、《愛爾蘭時報》2009、AP 2013、BusinessWorld 2015、NPR、Big Issue、India 書前頁 PDF、Lonely Planet 簡史與〈About〉、CS Monitor、Outlook Business、中央社、Taiwan News、弗萊堡大學、Red Ventures、NBC News、Forbes、Peninsula（AFP）、C21、Best in Travel 2027 頁，都用 curl 經代理讀到原文。tonywheeler.com.au 兩頁 curl 連線被重設、Taipei Times 回 403，三頁改用 WebFetch 讀（WebFetch 不肯轉錄 Space Captain 的歌詞，歌詞字面沿用研究表第 11 列）。
- 本輪自己加的列：#77–#85（附在表尾，標「查核代理補」）。#83 是推算，標 △。
- 旁白不用的列：#2、#3、#9、#15、#24、#30、#31、#36、#37、#42、#50、#51、#52、#57 前半（ITV／MySpace）、#61–#65、#68、#70、#74；#83 只供撰稿參考。
- 結果：旁白 142 行，OK 126、SOFTEN 14、FIX 2；卡片 10 張，FIX 1、SOFTEN 2；標題 SOFTEN；說明 FIX（跟著提示詞）；縮圖 OK。另有插圖規則違反（在世人物的替身），見〈插圖規則檢查〉。
- 這份檔案的〈逐項查核〉表照抄 `topic-checks/B03.md`，讓成片品管（`tools/video/qa/facts.mjs`）讀得到判定；兩份不一致時以 `topic-checks/B03.md` 為準。

## 稿子逐句核對

| 行 | 旁白或卡片（節錄） | 列 | 判定 | 說明 |
|---|---|---|---|---|
| t001 | 你可能翻過一套很厚的背包客旅遊書。 | #25 | OK | 對觀眾的開場，不帶數字 |
| t002 | 英國的 BBC 為了買下出它的公司，前後付了大約一億三千萬英鎊。 | #41 | OK | BBC 新聞稿「total consideration of £130.2m」（重讀 2026-10-31）；「前後」交代了是兩次 |
| t003 | 六年後賣掉，只拿回五千一百五十萬。 | #43 | OK | AU$75m（£51.5m），2007→2013 六年 |
| t004 | 一九七二年聖誕節隔天，一對年輕夫妻到了雪梨，身上只剩二十七分錢。 | #4 | OK | Wheeler〈About Tony〉「the day after Christmas 1972 … 27 cents」（WebFetch 重讀；curl 被重設） |
| t005 | 一年後，他們在廚房桌上，用釘書機釘出第一本旅遊書。 | #6 #10 | OK | 1973 年、廚房桌、釘書（India 書前頁 PDF 重讀） |
| t006 | 這樣一本書，值一億多英鎊？ | — | SOFTEN | 一億多英鎊買的是公司（含 500 多種書、網站、雜誌），不是「一本書」。改：「從這樣一本小書起家的公司，值一億多英鎊？」 |
| t007 | 買下四年後，生意遠不如預期，創辦人剩下的股份，BBC 用什麼價錢買？ | #39 #79 | OK | 「四年」是曆年 2007→2011；實際 2007-10 到 2011-02 約三年四個月（Marcus Arthur「three and a half years」，第 79 列）。可接受；要更準可改「買下三年多後」 |
| t008 | 而 BBC 自己的網站，後來跟它搶起了生意。 | #53 #84 | SOFTEN | 報告說 bbc.com 延誤後「decided to build its own travel vertical」、BBC 寧可自己做內容；「搶生意」是研究表的詮釋，報告沒這樣說。改：「而 BBC 自己的網站，後來沒用它，自己做起了旅遊版。」 |
| open-promise（卡） | {text: £130.2m, kicker: BBC 前後兩次付的錢（2007… | #41 #43 | OK | £130.2m、2007／2011、£51.5m 都對 |
| t009 | 兩次付錢、一次賣掉，這份檔案一筆一筆算給你看。 | #41 #43 | OK | 兩次付錢一次賣出 |
| t010 | BBC 花大錢買下背包客的聖經，為什麼六年後賠著賣掉？ | #14 #19 | OK | 「聖經」是外號（出版社自家文章也說 travel “bibles”） |
| t011 | 那一年稍早，這對姓惠勒的夫妻在倫敦買了一台破車， | #1 | SOFTEN | NPR 只說買了破車「drove from London」，沒說在倫敦買；Big Issue 說「left England … minivan bought for £50」。改：「那一年稍早，這對姓惠勒的夫妻買了一台破車，從倫敦出發，」 |
| t012 | 說要往東開，能開多遠就開多遠。 | #1 | OK | 「as far east as we could go」 |
| t013 | 阿富汗、印度、泰國，一路走到了澳洲。 | #1 | OK | NPR 原文順序 Afghanistan, India, Thailand |
| t014 | 到了雪梨，身邊的人一直問：你們去了哪裡？怎麼去的？ | #5 | OK | Big Issue「People kept asking us」 |
| t015 | 他們乾脆把答案寫成一本書。 | #5 | OK | 「So we made a book out of it」 |
| t016 | 一九七三年，就是開頭那張廚房桌子：兩個人一邊寫，一邊一本一本地釘。 | #6 #10 | OK | 1973 年（Wheeler「late 1973」、Big Issue「October 1973」） |
| t017 | 書名的意思是花小錢橫越亞洲，整本不到一百頁。 | #7 | OK | 94／96 頁之爭，「不到一百頁」兩說都對；書名 Across Asia on the Cheap |
| t018 | 你猜，這樣一本自己釘的小書，第一個禮拜賣了幾本？ | #8 | OK | 問句 |
| kitchen-1500（卡） | {text: 1,500 本, kicker: 第一本書，第一個禮拜, sub:… | #8 | OK | 書前頁的數字 |
| t019 | 一千五百本。 | #8 | OK | 書前頁「Within a week they'd sold 1500 copies」；AP 2013 同（重讀） |
| t020 | 我第一次讀到這個數字，還以為多打了一個零。 | — | OK | 旁白反應 |
| t021 | 書賣出去了，公司總得有個名字，從哪裡來？ | #10 | OK | 過場 |
| t022 | 名字來自一首歌，喬·庫克在一部巡迴演唱電影裡唱的〈太空船長〉。 | #11 #12 | OK | Space Captain，Matthew Moore 作，Joe Cocker 在《Mad Dogs & Englishmen》唱；旁白沒說是他寫的（WebFetch 重讀 2014-12-22 貼文） |
| t023 | 歌詞唱的是「可愛的星球」，丈夫一直唱成「寂寞的星球」。 | #11 | OK | lovely／lonely planet（研究表引句；WebFetch 不肯轉錄歌詞，但確認 Maureen 糾正一個字） |
| t024 | 妻子糾正他，他後來也承認：歌詞我老是記錯。 | #11 | OK | 「She was right, I always got the words wrong」 |
| t025 | 結果唱錯的那個留了下來：Lonely Planet，寂寞的星球。 | #11 | OK |  |
| t026 | 你唱錯歌詞，頂多被朋友笑一晚；他唱錯，唱出一塊招牌。 | — | OK | 玩笑 |
| t027 | 一九七五年，他們又出了一本，專寫東南亞。 | #13 | OK | △ 書目；只講年份與題材 |
| t028 | 背包客後來給它取了一個外號，叫什麼？ | #14 | OK | 問句 |
| t029 | 黃色聖經。 | #14 | OK | CSM 1992「Known as the "yellow bible" by travelers」（重讀） |
| t030 | 早在第三、四本書做尼泊爾的時候，他就想：只寫給背包客，不是太瘋狂了嗎… | #17 | OK | Big Issue「our third or fourth book … this is crazy」（重讀）；原文是「we thought」，旁白「他就想」可接受 |
| t031 | 所以從那一本開始，貴的地方也一起寫，一直到今天。 | #17 | OK | 「So that book covered the expensive places as well. And it's been that way ever since.」 |
| t032 | 一九八一年做印度，三個作者加起來在印度待了一年。 | #16 | OK | Outlook「In 1981, Wheeler and two other writers spent a year between them in India」（重讀） |
| t033 | 書寫到哪裡，人就跟到哪裡。 | #18 #19 | OK | 旁白的概括；#18 是創辦人自述（△） |
| t034 | 有記者問他：被你們寫紅的地方，後來擠爆了怎麼辦？ | #19 #81 | SOFTEN | AP 原問是「很多冷門地方被擠爆，有時 LP 的推薦也有份。這趟旅行有什麼不同？」，不是問「怎麼辦」。改：「有記者跟他說：很多冷門地方被擠爆，你們的推薦也有份。」 |
| t035 | 他說，你回到一個很愛、以前空空的地方，現在大家都知道了。 | #19 | OK | 「You go back to places you really loved … sort of empty, and now everybody knows them」 |
| t036 | 他舉峇里島當例子：現在人人都有一件「我去過峇里島」的T恤。 | #19 | OK | 「I've been to Bali」T-shirt |
| t037 | 但這還不是它影響力最怪的地方。 | — | OK | 升級句 |
| t038 | 它寫非洲的那一本，在馬拉威被禁。 | #20 | OK | 「Africa on the Cheap was banned in Malawi」（1980 年代） |
| t039 | 出版社自己寫過：美軍據說拿它一九九四年的中東指南來用。 | #20 | OK | 「allegedly」→「據說」，出版社自己寫的，歸屬清楚 |
| t040 | 一位前美國大使說：書很棒，但不該拿來當占領的依據。 | #20 | OK | Bodine 2007 年已是前大使；引句正確 |
| t041 | 一本旅遊書被拿去打仗，我讀到這裡是真的愣住了。 | — | OK | 旁白反應 |
| t042 | 它也寫到了你住的地方。你猜，第一本台灣指南是哪一年？ | #21 | OK | 問句 |
| taiwan-1987（卡） | {text: 1987, kicker: 第一本 Lonely Planet 台… | #21 | OK | Robert Storey 寫前四版 |
| t043 | 一九八七年。 | #21 | OK | Taipei Times 2017-01-05「Taiwan — a travel survival kit, published in 1987」（curl 403，WebFetch 重讀） |
| t044 | 到了二〇〇七年，它出了五百多種書，一年賣出六百五十多萬本。 | #22 | OK | 「over 500 titles … more than 6.5 million … sold annually」（重讀） |
| t045 | 這一年十月一日，有人上門來了。 | #27 | OK | 2007-10-01 新聞稿 |
| t046 | 上門的是 BBC 的商業部門，它買下了這家公司的四分之三。 | #27 | OK | 75% |
| deal-price（卡） | {text: £88.1m, kicker: 2007 年，買下 75%, su… | #28 #77 | FIX | sub「價錢在 2013 年的 BBC 新聞稿才寫出來」錯，《衛報》2011 已刊出 £88.1m。改 sub：「BBC 新聞稿（2013）所列價格」 |
| t047 | 價錢當時沒有公布。 | #28 | OK | 2007 新聞稿沒有價格（重讀全文確認） |
| t048 | 六年後，BBC 自己的新聞稿才寫出來：八千八百一十萬英鎊。 | #28 #77 | FIX | 「六年後…才寫出來」錯：《衛報》2011-02-18 已寫「In October 2007 … for £88.1m」（第 77 列）。改：「後來 BBC 的新聞稿寫明：八千八百一十萬英鎊。」 |
| t049 | 剩下的四分之一，留在惠勒夫婦手上。 | #27 | OK | 「will retain a 25% shareholding」 |
| t050 | 那 BBC 圖的是什麼？ | #29 | OK | 問句 |
| t051 | 商業部門的執行長說，這筆交易符合他們的策略： | #29 | OK | John Smith「This deal fits well with our strategy」 |
| t052 | 在網路上壯大自家的內容品牌，也擴大在澳洲和美國的生意。 | #29 | OK | 「grow our portfolio of content brands online … operations in Australia and America」 |
| t053 | 聽起來很合理，對吧？ | — | OK |  |
| t054 | 可是如果你是英國人，第一個反應大概是：那我繳的收視費呢？ | — | OK | 對觀眾的問句 |
| t055 | BBC 後來強調，買它沒有用到公共的錢。 | #76 | OK | △ AFP 轉述，旁白標「BBC 後來強調」（Peninsula 重讀：「Worldwide stressed that no taxpayers' money」） |
| t056 | 結果，消息一出來，《衛報》和《金融時報》同一天開罵。 | #32 | OK | Organ Grinder 2007-10-03「Today the Guardian and the Financial Times have both weighed in」 |
| t057 | 《衛報》的社論說，這是「笨手笨腳的商業化」。 | #32 | OK | 「blundering commercialism」 |
| t058 | 公平起見補一句：《衛報》在文章裡自己註明，它的母公司也是競爭對手。 | #32 | SOFTEN | 原文是「(including - full declaration- the Guardian)」：註明的是《衛報》自己是對手，不是「母公司」。改：「公平起見補一句：《衛報》在文中自己註明，它也是競爭對手。」 |
| t059 | 可是兩年後，開罵的換成了國會。 | #34 | OK | 2007→2009 |
| t060 | 二〇〇九年四月，下議院文化、媒體與體育委員會出了一份報告。 | #34 | OK | 《愛爾蘭時報》2009-04-08：Commons Culture, Media and Sport Select Committee（重讀） |
| t061 | 報告說，天平已經太偏向商業部門毫無限制的擴張。 | #34 | OK | 「the balance has been tipped too far in favour of Worldwide's unrestricted expansion」 |
| t062 | 更麻煩的是，帳也開始難看了。 | #38 | OK |  |
| loss-2009（卡） | {text: −£3.2m, kicker: 到 2009 年 3 月底的那一年… | #38 | OK |  |
| t063 | 到二〇〇九年三月底那一年，它虧了三百二十萬英鎊。 | #38 | OK | 「£3.2m loss in the year to the end of March 2009」（重讀） |
| committee-quote（卡） | {text: 最惡劣的例子, kicker: 下議院文化、媒體與體育委員會，20… | #35 | OK | 引句與轉引出處正確 |
| t064 | 九月，委員會又補了一份報告，用字更重： | #35 | OK | 2009-09 追加報告 |
| t065 | 商業部門跑進自己幾乎沒有本業的領域，買下它，是最惡劣的例子。 | #35 | SOFTEN | 原文是「areas where the BBC has no, or very limited, existing interests」——沒有本業的是 BBC，不是商業部門「自己」。改：「商業部門跑進 BBC 幾乎沒本業的領域，買下它是最惡劣的例子。」 |
| t066 | 報告還說，負責把關的信託會，看起來很傲慢。 | #35 | OK | 「apparent arrogance of the BBC Trust」→「看起來很傲慢」 |
| t067 | 說實話，被國會這樣點名，我大概會想找個洞鑽進去。 | — | OK | 旁白反應 |
| t068 | 同一個月，倫敦一家城市雜誌的創辦人乾脆說：憑什麼不能逼他們賣掉？ | #33 | OK | Tony Elliott（Time Out）2009-09：「Why shouldn't they be forced to sell it?」，同篇同月 |
| t069 | 如果你是 BBC 的主管，這時候你會怎麼做？賣掉，還是撐下去？ | — | OK | 問句 |
| t070 | 他們撐下去了。結果呢，生意好像真的轉過來了。 | #38 | OK | 「好像」有保留 |
| t071 | 二〇一一年二月，報紙寫它轉虧為盈，賺了一百九十萬英鎊。 | #38 | OK | 《衛報》2011-02-18「back into the black with profits of £1.9m」 |
| t072 | 同一個月，惠勒夫婦翻出了合約裡的一張牌。 | #39 | OK | 同篇報導賣權已行使；「翻出一張牌」是比喻，原文說是 2007 年就談好的條款 |
| t073 | 這張牌叫「賣權」：剩下的股份，他們有權要對方買下。 | #39 #40 | OK | put option 的白話 |
| t074 | 還記得開頭那個問題嗎？最後這四分之一，用什麼價錢買？ | #39 | OK | 回收開頭問題 |
| t075 | 照當年收購的價錢。 | #39 | OK | Trust 報告「the vendors received the original acquisition price」（PDF 重讀） |
| t076 | 最後這四分之一，BBC 付了四千兩百一十七萬英鎊。 | #39 | OK | £42.17m（BBC 2013 附註）；《衛報》A$67.2m（£42.1m）。注意第 83 列：「原價」是澳幣口徑，英鎊多付是因為澳幣升值 |
| t077 | 你想想看：四年來生意遠不如預期，最後這一塊，卻照四年前的價錢賣。 | #39 #79 | OK | 「四年」同 t007 的說明 |
| t078 | 換成你是賣的那一方，這大概是你簽過最划算的合約吧？ | — | OK | 問句 |
| put-quote（卡） | {text: 設計得很糟, kicker: BBC 信託會委託的檢討報告，201… | #39 #80 | SOFTEN | kicker「BBC 信託會委託的檢討報告」：Trust 是「asked the Executive to commission a review」，由 BBC 非執行董事 Brian McBride 主持。改 kicker：「BBC 信託會要求做的檢討報告，2013 年」 |
| t079 | 後來官方的檢討報告，寫得很直接：這個賣權，設計得很糟。 | #39 | OK | 「The put was badly structured」 |
| t080 | 兩次加起來，就是開頭那大約一億三千萬英鎊。 | #41 | OK | 88.1＋42.17＝130.27 |
| t081 | 惠勒夫婦也從此離開了自己一手做起來的公司。 | #75 | OK | Wheeler「In 2011 we completed the sale」「no longer have any formal role」 |
| t082 | 可是這家公司要在網路上賺錢，靠的不只是它自己。 | #53 | OK |  |
| t083 | 問題來了：它靠的是誰？ | — | OK | 問句 |
| t084 | 檢討報告說，它的網路生意，要接上 BBC 的國際網站，一起賣廣告。 | #53 | OK | 「dependent on connecting to bbc.com and monetising the content through advertising」 |
| t085 | 還記得開頭說的，那件跟它搶生意的事嗎？ | #53 | SOFTEN | 同 t008，「搶生意」是詮釋。改：「還記得開頭說的，BBC 自己的網站做了什麼嗎？」 |
| t086 | 結果，那個網站一延再延。 | #53 #84 | SOFTEN | 報告只說「bbc.com was delayed」「… which were delayed」，沒說一延再延。改：「結果，那個網站延誤了。」 |
| t087 | 然後呢？你猜它做了什麼？ | — | OK | 問句 |
| t088 | 它決定自己蓋一個旅遊頻道。 | #53 #84 | OK | 「decided to build its own travel vertical」；報告另一句也用「its own travel channel」。字面可以，但配圖 studio-globe／-2 畫成電視攝影棚，見規則檢查 |
| t089 | 花大錢買了一家旅遊公司，再自己做一個旅遊頻道，這不是很怪嗎？ | #53 | OK | 旁白反問 |
| t090 | 有點像你剛買了一台咖啡機，每天還是去樓下買咖啡。 | — | OK | 比喻 |
| t091 | 以美國為例，二〇一二年賣出的旅遊類書，比前一年少了百分之十九。 | #69 | OK | NBC 2013-03-20：Nielsen BookScan 美國「adult non-fiction/travel」2012 年比 2011 少 19%（重讀）；有標「以美國為例」 |
| t092 | 比二〇一〇年呢？ | #69 | OK |  |
| t093 | 少了百分之二十七。 | #69 | OK | 比 2010 少 27% |
| t094 | 檢討報告還寫了一句更讓人扼腕的話： | #54 | OK |  |
| t095 | 它反應太慢了，不然可能走上 TripAdvisor 的路， | #54 | OK | 「too slow in reacting … might have adopted the TripAdvisor model」 |
| t096 | 或者搭上後來那一波共享住宿的浪潮。 | #54 | OK | 「the subsequent social accommodation wave」 |
| t097 | 你上一次出國，是翻書找餐廳，還是打開手機看別人的評論？ | — | OK | 問句 |
| t098 | 報告說，買的時候 BBC 估它的獲利率有三成，太樂觀了。 | #55 | SOFTEN | 報告是「An EBITDA margin of 30% was highly optimistic」：是收購計畫的假設，而且是折舊攤銷與利息稅前的利潤率，不是一般說的獲利率。改：「報告說，收購計畫假設它的營業利潤率有三成，太樂觀了。」 |
| t099 | 買方被交易的氣勢沖昏了頭，書市會掉得多快，也沒算清楚。 | #55 | SOFTEN | 原文「seemed to get carried away with deal momentum」有「似乎」；「Not enough downside analysis」。改：「買方似乎被交易氣勢沖昏了頭，書市會掉多快，也沒細算。」 |
| t100 | 之後幾年回報業績，也一直報喜不報憂，明明早就看得出不對勁。 | #56 | SOFTEN | 原文「Throughout its ownership … a bias to positive in the reporting」：是偏向樂觀，不是只報好消息；時間是整段持有期間。改：「整段持有期間，業績回報都偏向樂觀，明明早有不對勁的跡象。」 |
| t101 | 到了二〇一三年三月，BBC 不撐了。 | #43 | OK |  |
| t102 | 三月十九日，BBC 宣布：整家公司賣掉，賣價七千五百萬澳幣。 | #43 | OK | 2013-03-19，AU$75m，100%（重讀） |
| t103 | 也就是開頭說的，大約五千一百五十萬英鎊。 | #43 | OK | £51.5m（含一年後付的 AU$15m） |
| t104 | 買家是一家總部在美國田納西州納許維爾的公司， | #44 | OK | NC2 Media「headquartered in Nashville Tennessee」 |
| t105 | 大股東是一位肯塔基出身、靠平價香菸起家的大地主。 | #44 #45 | OK | Forbes「a Kentucky native … fortune from discount cigarettes」「over 500,000 acres」（重讀） |
| t106 | 背包客的聖經，最後落到一位香菸富豪手上，你想得到嗎？ | #45 | OK | 反問 |
| t107 | 官方給的理由：它已經不符合把 BBC 自家品牌放在核心的計畫。 | #46 | OK | 「it no longer fits with our plans to put BBC brands at the heart of our business」 |
| t108 | 業績則被強勢的澳幣、出版業快速整併、全球經濟衰退一起拖累。 | #46 | OK | 「continued strength of the Australian dollar, the rapid consolidation of the publishing industry and a global recession」 |
| t109 | 那 BBC 到底賠了多少？ | — | OK | 問句 |
| t110 | 新聞標題幾乎都寫：將近八千萬英鎊。 | #47 #85 | SOFTEN | 「新聞標題幾乎都寫」是沒查過的概括；《衛報》標題是「at 'significant loss'」，£80m 在內文；法新社（Peninsula）標題才是「at £80m loss」。改：「當時法新社、《衛報》都寫：將近八千萬英鎊。」 |
| t111 | 算法很簡單：開頭那一億三千萬，減掉五千一百五十萬。 | #47 | OK | 130.2−51.5＝78.7 |
| t112 | 但這筆錢，不是賣掉那天才一口氣賠的。 | #48 | OK |  |
| loss-stats（卡） | {title: 那將近 8 千萬是怎麼來的, stats: [{value: £… | #41 #43 #48 | SOFTEN | 標籤「賣出那年帳面損失」：《衛報》說的是賣出時帳上損失約 £12m；C21 轉述 BBCW 2012/13 年報卻說該年度被「an £80m loss on the sale」拖累（#47 △），「那年」會跟年報口徑打架。改標籤：「賣出時帳面損失（《衛報》）」 |
| t113 | 《衛報》算過：六年來，BBC 已經在帳上把它減記了六千七百萬英鎊。 | #48 | SOFTEN | 減記是《衛報》報導的事實，不是《衛報》「算」出來的。改：「《衛報》寫道：六年來，BBC 已在帳上減記了六千七百萬英鎊。」 |
| t114 | 真正賣掉那天，帳面上的損失，只剩大約一千兩百萬。 | #48 | OK | 「making the loss on its books about £12m」，接在 t113 的《衛報》歸屬後 |
| t115 | 我讀到這裡才懂：它不是一次摔下來的，是六年慢慢滑下來的。 | — | OK | 旁白反應 |
| t116 | 可是，要是換個算法呢？ | — | OK | 問句 |
| t117 | 官方檢討報告說，持有這幾年，另外還投了大約兩千萬英鎊進去。 | #41 #49 | OK | Trust 報告「invested some £20m during its ownership」（PDF 重讀） |
| t118 | 照報告自己的數字推算，全部算進去，賠掉的接近一億英鎊。 | #49 | OK | 標了「照報告自己的數字推算」：132＋20−52＝100 |
| t119 | 那年十一月，信託會副主席說得更白：收購和經營它的過程中，犯了錯。 | #58 #80 | OK | Diane Coyle「Mistakes were made in the acquisition and handling」；報告 PDF 建檔 2013-11-06（第 80 列） |
| t120 | 那當年把公司賣給 BBC 的人，又是怎麼看這筆買賣？ | — | OK | 過場 |
| t121 | 那年九月，美聯社訪問了東尼·惠勒。 | #59 | OK | AP 2013-09-01 |
| ap-quote（卡） | {text: 最完美的時機, kicker: 東尼·惠勒，美聯社專訪，2013 … | #59 | OK |  |
| t122 | 他說：毫無疑問，我們賣在了最完美的時機。 | #59 | OK | 「There's no question we sold out at the perfect moment」 |
| t123 | 傷到公司的不只是經濟衰退，還有他們賣掉之後就起飛的澳幣。 | #59 | OK | 「It wasn't just the recession … we also sold out just as the Australian dollar took off」；「賣掉之後就起飛」與「just as」相當，接在 t122「他說」之後，歸屬清楚 |
| t124 | 這句話很誠實，也有一點殘忍。 | — | OK | 旁白評語 |
| t125 | 還記得那台從倫敦一路往東開的破車嗎？ | #1 | OK | 回扣 |
| t126 | 兩年後，在峇里島一場作家節上，據一家菲律賓媒體報導，他說得更白： | #60 #78 | FIX | BusinessWorld 那篇是路透社電稿（文末「— Reuters」，Wheeler「said in an interview」），不是菲律賓媒體自己的報導。改：「兩年後，在峇里島一場作家節上，他對路透社說得更白：」 |
| t127 | 這是一場徹底的災難。他們買下這台車，卻不加油、不踩油門。 | #60 | OK | 「It was a total disaster … should have put some fuel in the tank, and put it flat to the floor」 |
| t128 | 上了車只問：我們要幹嘛？那就慢慢開吧。 | #60 | OK | 「'what do we do?' Let's drive slowly」 |
| t129 | 那 BBC 賣掉之後呢？ | — | OK | 問句 |
| t130 | 二〇二〇年年底，它又被賣了一次，價錢沒有公開。 | #66 #67 | OK | Red Ventures 2020-12-01「for an undisclosed amount」（重讀） |
| t131 | 現在它的全職員工大約一百三十個；BBC 賣掉那年，是四百個。 | #26 #23 | OK | 「130 full-time staff」；2013「employs 400 people」 |
| t132 | 可是書還在出，翻成三十三種語言，一共印了超過一億五千萬本。 | #25 #26 #82 | SOFTEN | 〈About〉寫的是「content translated into 33 languages」；Red Ventures 2020 說指南書出 14 種語言。改：「書還在出，內容翻成三十三種語言，一共印了超過一億五千萬本。」 |
| t133 | 它也一直在替台灣打分數。你猜，高雄拿過第幾名？ | #71 | OK | 問句 |
| t134 | 二〇一八年，全球最值得去的城市，第五名。 | #71 | OK | 中央社「fifth best city in the world to visit in 2018」（重讀） |
| t135 | 二〇二二年，台北排第二。 | #72 | OK | Taiwan News「second only to Auckland」、弗萊堡大學（重讀） |
| t136 | 最新的二〇二七年推薦名單，台灣也在裡面，這次不排名次。 | #73 | OK | Best in Travel 2027 頁有「Taiwan — Best for night market grazing」，列表是 50 個地點、只有排序選項（重讀） |
| t137 | 給的理由是：最適合逛夜市，一路吃過去。 | #73 | OK |  |
| t138 | 下次你在夜市排隊，旁邊那個邊吃邊查手機的外國人，搞不好就是看它來的。 | — | OK | 玩笑 |
| t139 | 回到開頭的問題：BBC 為什麼賠著賣掉？ | — | OK | 問句 |
| close-outro（卡） | {title: £130.2m 買進，£51.5m 賣出, cta: 參考資料在… | #41 #43 | OK |  |
| t140 | 一億三千萬買、五千一百五十萬賣，官方檢討說：估太高、轉太慢，又碰上壞… | #41 #43 #55 #57 | OK | 「估太高」＝forecasts too aggressive／30% optimistic；「轉太慢」＝integration too slow／too slow in reacting；「壞時機」＝報告結論 A$ 升值、金融海嘯、書市結構壓力。都是報告原話的概括 |
| t141 | 你出國還會帶一本旅遊書嗎？還是全靠手機？留言告訴我。 | — | OK | CTA |
| t142 | 這個頻道只講紀錄裡有的，想一起翻檔案就訂閱。 | — | OK | CTA |
| 標題 | BBC 買下 Lonely Planet，為什麼六年賠掉近 8 千萬鎊？｜奇聞檔… | #47 #48 #85 | SOFTEN | 「近 8 千萬」有《衛報》「lost almost £80m」與法新社撐腰，「六年」也不是說一次認列，所以不算錯；但它把整集花一章去拆解的數字（帳面約 £12m、現金面推算近 £1 億）放成標題的事實，而且後綴前 31 字（不算空格）超過 30。建議：「BBC 前後付 1.3 億鎊，Lonely Planet 為何賠著賣？」（30 字，BBC 在前 3 字、「賠」、數字、問號；「前後付」交代兩次付款） |
| 說明 | 插圖由 AI 生成，畫中都是不指認的一般人物，在世人物不入畫。 | — | FIX | 現在的提示詞不成立：二十多張圖把惠勒夫婦（在世）畫成有臉、有髮型的年輕男女，另有幾位在世或 1956 年後過世的具名人物的替身（見下方規則檢查）。改完提示詞這句才成立；其他段落 OK（「三十四年後」＝1973→2007） |
| 縮圖 | BBC **賠著賣**／1.3 億鎊買，賣剩 5 千萬 | #41 #43 | OK | 「1.3 億鎊買」是兩次合計、沒寫年份，也沒說一次付清，成立。想更嚴可改 sub：「分兩次付 1.3 億，賣剩 5 千萬」（超過 12 字，現行可用）；shot open-stakes 是不指認的會計師 |

## 插圖規則檢查

規則（`tools/video/automation/explainer-series.mjs` MYSTERY lookRules；`curio-episode` 系列定案）：在世或 70 年內過世的人不畫成本人；故事需要他們入畫時，只能是**背影或遠處的小人**、只用一般角色與素色衣著描述，不寫名字、長相特徵、髮型、體型、制服或足以指認的職位；否則就不畫。提示詞裡沒有品牌、產品或真人姓名，地名（Taipei、London、India）可以。

**違反（要改提示詞，重畫）**

| 景 | 誰的替身 | 問題 |
|---|---|---|
| open-sydney、open-table、road-map、flat-ask-2、kitchen-type、name-correct | Maureen Wheeler（在世） | 正面中景／特寫、有表情，旁白同時在講她 |
| road-van、road-van-2、flat-ask、kitchen-staple、kitchen-shop、name-sing、name-sing-2、name-correct-2、name-sign、nepal-guesthouse、van-highway | Tony Wheeler（在世） | 同上，而且寫了「long hair」這種髮型特徵 |
| open-table-2、kerb-booklet、tshirt-stall、india-platform | 惠勒夫婦（邊界） | 「young woman's curious eyes」、1970 年代牛仔外套拿釘裝小書、t035 講 Wheeler 的話時配「older traveller … wistful smile」、印度三作者之一；建議一起改 |
| deal-ceo | John Smith（BBC Worldwide 執行長，在世） | 講他的話時配講台上的西裝男正面中景 |
| tent-soldier-2 | Barbara Bodine（在世） | 「woman diplomat at a microphone」＝職位指認 |
| rival-publisher | Tony Elliott（2020 年過世） | 「magazine publisher in his sixties」＝職位加年齡指認 |
| trust-lectern | Diane Coyle（在世） | 「the grey-haired woman board member」＝髮色加職位 |
| buyer-street、buyer-street-2 | Brad Kelley（在世） | 講他時配牛仔帽商人、牛仔帽地主的正面中景 |

改法：把人拿掉只留物件（壞車停在路邊、桌上的釘書機和一疊小冊、窗台上的收音機、空白木招牌、握手只拍手），或改成背影、遠處的兩個小人，刪掉「long hair」「grey-haired」「diplomat」「board member」「magazine publisher」「cowboy hat」這類指認詞。`backpack-hook`（t081 只畫掛鉤上的背包）就是合格的寫法。改完 `youtube.description` 那句「在世人物不入畫」才成立。

**不是違規但建議改**

- studio-globe、studio-globe-2：畫成電視攝影棚，但報告說的是 bbc.com 自建「travel vertical」（網站的旅遊專區），配圖會讓人以為是電視頻道。改成網站團隊在白板上排旅遊頁的格子。
- calendar-crossed：掛曆一般會畫出日期數字，加「blank calendar grid with no numbers」。
- deal-notary、put-lawyer-2：證書常被畫出字，加「blank certificate with no writing」。
- 邊界、可留：mp-report／-2、hearing-haughty、sale-podium、shutter-dusk 是不指認的一般角色（委員會、信託會、發言人、比喻），沒有對到單一在世人物的特徵。

## 逐項查核（抄自 `topic-checks/B03.md`，2026-10-31）

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 1 | 1972 年開車從倫敦出發往東走 | CONFIRMED | 「In 1972, Maureen and Tony Wheeler bought a beat-up car and drove from London "as far east as we could go." They wound up in Australia, by way of Afghanistan, India and Thailand.」 | NPR《How I Built This》節目頁（2017） | https://www.npr.org/2017/06/27/525917692/lonely-planet-maureen-tony-wheeler | ✅ |
| 2 | 出發時的錢與車 | CONFIRMED（金額）／DISPUTED（車價） | Big Issue（2023-10-28）：「left England with £400 between them, a second-hand minivan bought for £50」；Encyclopedia.com 版本是「bought an old van for one hundred and fifty dollars … then sold it for one hundred and fifty-five dollars」。**旁白只說「四百英鎊、一台二手小廂型車」，不講車價** | Big Issue；Encyclopedia.com | https://www.bigissue.com/life/lonely-planet-travel-book-50-years-history ；https://encyclopedia.com/arts/educational-magazines/wheeler-tony-1946 | △／⚠ |
| 3 | 車在阿富汗賣掉，1972 年 10 月走進巴基斯坦再到印度 | CONFIRMED（二手） | 「The couple sold the car in Afghanistan before walking across the border into Pakistan first and then to India, in October 1972.」 | Outlook Business 專訪 | https://www.outlookbusiness.com/cest-la-vie-6/pursuit-of-happiness-23/the-perpetual-wanderer-2462 | △ |
| 4 | 抵達雪梨時只剩 27 分錢 | CONFIRMED | Wheeler 自述：「When Maureen and I arrived in Sydney the day after Christmas 1972 … we had 27 cents left between us.」 | Tony Wheeler 個人網站〈About Tony〉 | https://tonywheeler.com.au/about-tony | ✅ |
| 5 | 為什麼寫書：一直有人問怎麼走 | CONFIRMED | 「People kept asking us: What did you do? Where did you go? How did you do it? So we made a book out of it, and away we went.」（Wheeler 受訪） | Big Issue（2023） | https://www.bigissue.com/life/lonely-planet-travel-book-50-years-history | ✅ |
| 6 | 廚房桌上寫、自己用釘書機釘 | CONFIRMED | 「broke but inspired – they sat at their kitchen table writing and stapling together their first travel guide, Across Asia on the Cheap.」 | Lonely Planet《India》第 18 版書前頁（出版社自述） | https://media.lonelyplanet.com/shop/pdfs/india-18-preview.pdf | ✅ |
| 7 | 第一本書幾頁 | DISPUTED（旁白說「不到一百頁」） | Lonely Planet 自家文章（2020-05-04）：「packed more than a dozen countries into just 94 pages」；Encyclopedia.com：「ninety-six pages long and hand-stapled together」 | Lonely Planet；Encyclopedia.com | https://www.lonelyplanet.com/articles/history-of-travel-guidebooks ；https://encyclopedia.com/arts/educational-magazines/wheeler-tony-1946 | ⚠ |
| 8 | 一週賣出 1,500 本 | CONFIRMED | 出版社書前頁：「Within a week they'd sold 1500 copies. Lonely Planet was born.」；AP 2013：「It sold 1,500 copies in a week」。Encyclopedia.com 說法是印 1,500 本、「In ten days, they sold out … eventually sold over 8,000 copies」 | Lonely Planet；AP（Spokesman-Review 轉載）；Encyclopedia.com | https://media.lonelyplanet.com/shop/pdfs/india-18-preview.pdf ；https://www.spokesman.com/stories/2013/sep/01/dark-adventures/ | ✅（一週 1,500）／△（之後 8,000 本） |
| 9 | 第一本書定價、怎麼賣 | CONFIRMED（二手） | 「walked to all the Sydney bookstores selling them for a dollar and eighty cents each」 | Encyclopedia.com | https://encyclopedia.com/arts/educational-magazines/wheeler-tony-1946 | △ |
| 10 | 公司成立年份與地點 | CHANGED | 官方：「In 1973, Tony and Maureen Wheeler … self-published their account as Across Asia on the Cheap」；Wheeler：「In late 1973 we started Lonely Planet Publications」；Big Issue：「In October 1973」。但 BBC 2007 新聞稿寫「founded the company in 1972」、《衛報》2013 寫「founded in a Melbourne kitchen in 1972」。**旁白用：1973 年、雪梨** | Lonely Planet〈About〉；Tony Wheeler 網站；BBC 新聞稿；《衛報》 | https://www.lonelyplanet.com/about ；https://tonywheeler.com.au/about-tony ；https://www.bbc.co.uk/pressoffice/bbcworldwide/worldwidestories/pressreleases/2007/10_october/lonely_planet.shtml | ✅ 1973／⚠ 他處 1972 |
| 11 | 店名來自唱錯的歌詞 | CONFIRMED | Wheeler 2014-12-22 自述：他哼的是「the Matthew Moore song 'Space Captain', sung by Joe Cocker in the classic rock and roll tour film Mad Dogs & Englishmen」，唱成「lonely planet」，Maureen 糾正「It's lovely planet」；Wheeler：「She was right, I always got the words wrong」 | Tony Wheeler 個人網站〈Joe Cocker〉 | https://tonywheeler.com.au/joe-cocker/ | ✅ |
| 12 | 「喬·庫克的歌」 | CHANGED | 作者是 Matthew Moore，Joe Cocker 是在巡演電影《Mad Dogs & Englishmen》裡演唱（Wheeler 原文）。**旁白說「喬·庫克在演唱會電影裡唱的一首歌」，不說是他寫的** | 同上 | https://tonywheeler.com.au/joe-cocker/ | ✅ |
| 13 | 《South-East Asia on a Shoestring》1975 年出版 | CONFIRMED（二手） | 書目：「South-East Asia on a Shoestring, Lonely Planet (Footscray, Victoria, Australia), 1975.」 | Encyclopedia.com；FineBooks | https://encyclopedia.com/arts/educational-magazines/wheeler-tony-1946 ；https://www.finebooksmagazine.com/fine-books-news/south-east-asia-shoestring | △ |
| 14 | 「黃色聖經」 | CONFIRMED | 1992 年：「Known as the "yellow bible" by travelers」，涵蓋緬甸、香港、印尼、澳門、馬來西亞、菲律賓、新加坡、巴紐、泰國、越南、寮國、柬埔寨，「The seventh edition is due out this month」 | Christian Science Monitor | https://www.csmonitor.com/1992/0207/07122.html | ✅ |
| 15 | 「黃色聖經是 Lonely Planet 第一本書」 | CHANGED | FineBooks 寫「Their first book, South East Asia on a Shoe String, was published in 1975」——錯，第一本是 1973 年《Across Asia on the Cheap》（第 10 列） | FineBooks（錯誤示例） | https://www.finebooksmagazine.com/fine-books-news/south-east-asia-shoestring | ✅ |
| 16 | 印度指南 1981 年、規模空前 | CONFIRMED | 「In 1981, Wheeler and two other writers spent a year between them in India, and co-authored the first Lonely Planet India edition. "It was bigger than anything we had done before," he recalls.」**印度版銷量查無一手數字，旁白不講** | Outlook Business | https://www.outlookbusiness.com/cest-la-vie-6/pursuit-of-happiness-23/the-perpetual-wanderer-2462 | ✅ 年份／UNVERIFIED 銷量 |
| 17 | 從背包客書轉向什麼人都寫 | CONFIRMED | Wheeler：做尼泊爾指南時（「our third or fourth book」）覺得只寫給背包客「that's crazy. So that book covered the expensive places as well. And it's been that way ever since.」 | Big Issue（2023） | https://www.bigissue.com/life/lonely-planet-travel-book-50-years-history | ✅ |
| 18 | 「被 Lonely Planet 寫進去的地方就爆紅」（例一） | CONFIRMED（創辦人自述） | 拉賈斯坦的齋沙默爾：「It wasn't on the international tourism radar till we featured it」 | Outlook Business | https://www.outlookbusiness.com/cest-la-vie-6/pursuit-of-happiness-23/the-perpetual-wanderer-2462 | △ |
| 19 | 「Lonely Planet 效應」（例二） | CONFIRMED | AP 問到 Lonely Planet 推薦讓地方被擠爆，Wheeler：「You go back to places you really loved … that were sort of empty, and now everybody knows them. I think of Bali: Now everybody's got an "I've been to Bali" T-shirt.」；Lonely Planet 自家文章提到小說《The Beach》與曼谷考山路的「banana pancake trail」 | AP（Spokesman-Review）；Lonely Planet | https://www.spokesman.com/stories/2013/sep/01/dark-adventures/ ；https://www.lonelyplanet.com/articles/history-of-travel-guidebooks | ✅ |
| 20 | 被一國禁、被一國軍隊拿去用 | CONFIRMED（出版社自述） | 「Africa on the Cheap was banned in Malawi」；美軍「allegedly used Lonely Planet's 1994 Middle East guide」，前美國大使 Bodine 2007：「It's a great guidebook, but it should not be the basis of an occupation.」 | Lonely Planet 自家文章 | https://www.lonelyplanet.com/articles/history-of-travel-guidebooks | ✅（出版社說法，美軍部分原文就用 allegedly） |
| 21 | 第一本台灣指南 | CONFIRMED | Robert Storey「author of the first four editions of the Lonely Planet Taiwan guide」；「their inaugural Taiwan guide, Taiwan — a travel survival kit, published in 1987」（David Frazier，2017-01-05） | Taipei Times | https://www.taipeitimes.com/News/feat/archives/2017/01/05/2003662528 | ✅ |
| 22 | 2007 年被收購時的規模 | CONFIRMED | 「Lonely Planet publishes over 500 titles and more than 6.5 million Lonely Planet books are sold annually」；辦公室在澳洲（總部）、英國、美國；網站「4.3 million unique visitors a month」 | BBC Worldwide 新聞稿（2007-10-01） | https://www.bbc.co.uk/pressoffice/bbcworldwide/worldwidestories/pressreleases/2007/10_october/lonely_planet.shtml | ✅ |
| 23 | 2013 年被賣掉時的規模 | CONFIRMED | 「printed approximately 120 million books in 11 different languages」；「more than 120million unique users visiting its website every year and more than 11million apps downloaded」；「employs 400 people, is headquartered in Melbourne Australia and has offices in London (at BBCW), Oakland California and Delhi, India」 | BBC Media Centre（2013-03-19） | https://www.bbc.co.uk/mediacentre/worldwide/190313lonelyplanet | ✅ |
| 24 | 「巔峰時在巴黎也有辦公室」 | CHANGED | 一手名單沒有巴黎：2007 年是澳、英、美；2013 年是墨爾本、倫敦、奧克蘭、德里；出版社書前頁另列「Franklin, London, Melbourne, Oakland, Dublin, Beijing and Delhi, with more than 600 staff and writers」。**旁白不提巴黎** | BBC 新聞稿；Lonely Planet 書前頁 | https://www.bbc.co.uk/mediacentre/worldwide/190313lonelyplanet ；https://media.lonelyplanet.com/shop/pdfs/india-18-preview.pdf | ✅ |
| 25 | 累計銷量 1.5 億本 | CONFIRMED | Red Ventures 2020：「Lonely Planet has produced over 150 million travel guidebooks」；Big Issue 2023：「sold over 150 million copies」（「印製」與「賣出」用詞不同，旁白說「超過一億五千萬本」） | Red Ventures 新聞稿；Big Issue | https://redventures.com/press/press-releases/red-ventures-acquires-lonely-planet ；https://www.bigissue.com/life/lonely-planet-travel-book-50-years-history | ✅ |
| 26 | 現在的人數 | CONFIRMED | 「a dedicated team of 130 full-time staff」、「1,100+ contributors」、「translated into 33 languages」（對照 2013 年 400 人） | Lonely Planet〈About〉 | https://www.lonelyplanet.com/about | ✅ |
| 27 | BBC Worldwide 2007-10-01 買下 75% | CONFIRMED | 「The privately owned business is being sold by Tony and Maureen Wheeler, who founded the company in 1972, and John Singleton who became a shareholder in 1999」；Wheeler 夫婦「will retain a 25% shareholding」 | BBC 新聞稿 | https://www.bbc.co.uk/pressoffice/bbcworldwide/worldwidestories/pressreleases/2007/10_october/lonely_planet.shtml | ✅ |
| 28 | 75% 的價格 | CONFIRMED | 2007 年新聞稿沒寫價格；BBC 2013 年新聞稿附註：「BBCW acquired 75% of Lonely Planet in 2007 for £88.1m」 | BBC Media Centre | https://www.bbc.co.uk/mediacentre/worldwide/190313lonelyplanet | ✅ |
| 29 | BBC 為什麼要買 | CONFIRMED | 執行長 John Smith：「This deal fits well with our strategy … to grow our portfolio of content brands online and to increase our operations in Australia and America.」 | BBC 新聞稿（2007） | https://www.bbc.co.uk/pressoffice/bbcworldwide/worldwidestories/pressreleases/2007/10_october/lonely_planet.shtml | ✅ |
| 30 | 創辦人當時怎麼說 | CONFIRMED | 「Joining BBC Worldwide allows us to secure the long-term future of our company within a globally recognised media group.」 | 同上 | 同上 | ✅ |
| 31 | BBC Trust 有條件核准 | CONFIRMED | Trust 7 月審查時開出四個條件（含再評估「four criteria」、實地查核、併購法務、公平交易），並要求證明此案能「leverage extra value from the BBC's intellectual property」；之後才「confirmed its approval」 | BBC Trust（2007-10-01 頁） | https://www.bbc.co.uk/bbctrust/our_work/commercial/lonely_planet.html | ✅ |
| 32 | 一宣布就被同業圍剿 | CONFIRMED | 「Today the Guardian and the Financial Times have both weighed in strongly against the acquisition」；《衛報》社論引句：「This week's deal represents a blundering commercialism」。**注意《衛報》母公司本身是競爭對手（文中自己 full declaration）** | 《衛報》Organ Grinder（2007-10-03） | https://www.theguardian.com/media/organgrinder/2007/oct/03/lonelyplanetisbbcworldwide | ✅ |
| 33 | Time Out 創辦人 Tony Elliott 要求 BBC 賣掉 | CONFIRMED | 2009 年：「Lonely Planet is losing money hand over fist. They are having to pump million into it. It is a complete sprawling mess」；「Why shouldn't they be forced to sell it?」 | 《衛報》（2009-09-23） | https://www.theguardian.com/media/2009/sep/23/mps-accuse-bbc-of-arrogance | ✅ |
| 34 | 「公共帳目委員會（PAC）批評」 | CHANGED | 批評的是下議院 **Culture, Media and Sport Select Committee**：2009-04 報告說「the balance has been tipped too far in favour of Worldwide's unrestricted expansion」 | 《愛爾蘭時報》（2009-04-08） | https://www.irishtimes.com/news/report-says-bbc-should-rein-in-commercial-arm-1.740195 | ✅ |
| 35 | 國會議員：「最惡劣的例子」 | CONFIRMED | 同委員會 2009-09 追加報告：「The purchase of Lonely Planet remains the most egregious example of the nature of BBC Worldwide's expansion into areas where the BBC has no, or very limited, existing interests.」並說 BBC Trust「apparent arrogance」 | 《衛報》（2009-09-23） | https://www.theguardian.com/media/2009/sep/23/mps-accuse-bbc-of-arrogance | ✅ |
| 36 | 競爭雜誌的抱怨 | CONFIRMED | Wanderlust 總編 Lyn Hughes：Lonely Planet 雜誌給廣告主「deals of just £500 for a full page」 | 《衛報》（2009-04-07） | https://www.theguardian.com/media/2009/apr/07/bbc-worldwide-channel-41 | ✅ |
| 37 | 同篇把收購金額寫成 £118m | DISPUTED | 《衛報》2009-04-07：「BBC Worldwide's £118m acquisition of the Lonely Planet travel guides company」，與 BBC 自己的 £88.1m（75%）不符，可能含債務或匯率口徑。**旁白只用 BBC 自己的數字** | 《衛報》；BBC | https://www.theguardian.com/media/2009/apr/07/bbc-worldwide-channel-41 ；https://www.bbc.co.uk/mediacentre/worldwide/190313lonelyplanet | ⚠ |
| 38 | 買下後第一年就虧 | CONFIRMED | 「poor trading conditions led the operation to report a £3.2m loss in the year to the end of March 2009」；之後轉盈「profits of £1.9m」；非紙本營收「from 9% in 2007 to 22%」；Trust 裁定往後不得再做類似收購，除非「exceptional circumstances」 | 《衛報》（2011-02-18） | https://www.theguardian.com/media/2011/feb/18/bbc-worldwide-lonely-planet-travel-guides | ✅ |
| 39 | 2011 年買下其餘 25%：用原價 | CONFIRMED（**強轉折**） | 價格：「A$67.2m (£42.1m)」，Wheeler 夫婦「exercised a put option」（《衛報》）；BBC 附註「£42.17m」。BBC Trust 檢討報告：「The put was badly structured: the vendors received the original acquisition price when they exercised the put, despite the significant under-performance of the business」 | 《衛報》；BBC；BBC Trust 檢討報告 PDF | https://www.theguardian.com/media/2011/feb/18/bbc-worldwide-lonely-planet-travel-guides ；https://downloads.bbc.co.uk/bbctrust/assets/files/pdf/our_work/lonely_planet/lonely_planet.pdf | ✅ |
| 40 | 賣權條款的白話 | CONFIRMED（二手） | 「the contract contained an agreement that said they could sell the remaining shares at the same price as they were worth at the time」 | SmartCompany（2011） | https://www.smartcompany.com.au/startupsmart/lonely-planet-founders-sell-remaining-stake-to-bbc/ | △（與第 39 列 Trust 一手一致） |
| 41 | BBC 總共付了多少 | CONFIRMED（兩種口徑） | BBC：「for a total consideration of £130.2m」；Trust 報告：「for a total of A$277m (£132m), invested some £20m during its ownership and sold it in 2013 for A$75m (£52m)」 | BBC Media Centre；BBC Trust PDF | https://www.bbc.co.uk/mediacentre/worldwide/190313lonelyplanet ；https://downloads.bbc.co.uk/bbctrust/assets/files/pdf/our_work/lonely_planet/lonely_planet.pdf | ✅ |
| 42 | 2011 年墨爾本裁員、網站搬去倫敦 | CONFIRMED | 「as many as 70 jobs will be lost as part of a restructure that will result in the publisher relocating a substantial part of its web operations to London」（只讀到導言） | Books+Publishing（2011-05-15） | https://www.booksandpublishing.com.au/articles/2011/05/15/19766/lonely-planet-to-cut-up-to-70-jobs-move-web-operations-to-uk/ | △ |
| 43 | 2013-03-19 賣給 NC2 Media | CONFIRMED | 「BBC Worldwide will receive AU$75m (£51.5m) for 100% of Lonely Planet with AU$60m (£41.2m) paid on completion and AU$15m (£10.3m) paid in one year's time.」 | BBC Media Centre | https://www.bbc.co.uk/mediacentre/worldwide/190313lonelyplanet | ✅ |
| 44 | 買家是誰 | CONFIRMED | NC2 Media「headquartered in Nashville Tennessee, and led by Daniel Houghton」；「primary shareholder is Brad Kelley, an American businessman and Forbes 400 member」 | 同上 | 同上 | ✅ |
| 45 | 「肯塔基億萬富翁」 | CHANGED（措辭） | Forbes：「a Kentucky native and a farmer's son, built a fortune from discount cigarettes」，Commonwealth Brands「sold it for $1 billion in 2001」，「over 500,000 acres」；居住地「Franklin, Tennessee」。**旁白說「肯塔基出身、靠平價香菸致富的地主富豪」** | Forbes 人物頁 | https://www.forbes.com/profile/brad-kelley/ | ✅ |
| 46 | BBC 給的賣出理由 | CONFIRMED | 「it no longer fits with our plans to put BBC brands at the heart of our business」；業績受「the continued strength of the Australian dollar, the rapid consolidation of the publishing industry and a global recession」影響 | BBC Media Centre | https://www.bbc.co.uk/mediacentre/worldwide/190313lonelyplanet | ✅ |
| 47 | 「賠了將近 £80m」 | CONFIRMED（算法說明） | £130.2m − £51.5m ≈ £78.7m；《衛報》「BBC Worldwide has lost almost £80m on its investment」；BBC Worldwide 2012/13 年度成績「dented by an £80m loss on the sale of Lonely Planet」（C21 轉述年報） | 《衛報》；C21 Media | https://www.theguardian.com/media/2013/mar/19/bbc-worldwide-criticised-lonely-planet-sale ；https://www.c21media.net/news/bbcww-profit-flat-sales-up/ | ✅ 算術／△ 年報 |
| 48 | 「BBC 一口氣認列 £80m 虧損」 | CHANGED（**強轉折**） | 「The corporation has already written down the value of Lonely Planet by £67m over the last six years to £63m, making the loss on its books about £12m.」**旁白：虧損是六年來一點一點減記的，賣出那天帳上只剩約 £12m** | 《衛報》（2013-03-19） | https://www.theguardian.com/media/2013/mar/19/bbc-worldwide-criticised-lonely-planet-sale | ✅ |
| 49 | 「其實賠了 £100m」 | DISPUTED | The Drum 標題「Damning report puts final BBC Lonely Planet losses at £100m」（頁面未能開啟）；用 Trust 自己的數字推算：£132m + 約 £20m 追加投資 − £52m ≈ £100m。**旁白可說「若把追加投資算進去，接近一億英鎊」，標「依官方報告推算」** | BBC Trust PDF（推算基礎） | https://downloads.bbc.co.uk/bbctrust/assets/files/pdf/our_work/lonely_planet/lonely_planet.pdf | ⚠ |
| 50 | 減記中的一筆 £33.8m | UNVERIFIED | 只看到 The Bookseller 標題「BBC wipes £33.8m off Lonely Planet value」，內文付費、年份未確認。**不用** | The Bookseller | https://www.thebookseller.com/news/bbc-wipes-338m-lonely-planet-value | ⚠ |
| 51 | 「BBC 2007 年花 £130m 買下」 | CHANGED | 好萊塢報導者：「BBC Worldwide bought Lonely Planet for $210 million (£130 million) in 2007」——錯，£130.2m 是 2007 與 2011 兩次合計（第 41 列） | The Hollywood Reporter（錯誤示例） | https://www.hollywoodreporter.com/news/bbc-worldwide-dealmaking-criticized-lonely-654173 | ✅ |
| 52 | 「創辦人 2007 年以 1.33 億美元賣掉」 | CHANGED | BusinessWorld 2015：「After selling the Lonely Planet enterprise for $133 million in 2007 to the BBC」——混用幣別且漏了 2011 年那筆。**不引用任何美元總價** | BusinessWorld（錯誤示例） | https://bworldonline.com/travel-tourism/2015/11/13/11726/lonely-planet-founder-reprises-original-trip-on-budget-air/ | ✅ |
| 53 | BBC 自己跟自己搶生意 | CONFIRMED（**強轉折**） | Trust 報告：Lonely Planet 上線要靠接上 bbc.com 賣廣告，「but bbc.com was delayed and then decided to build its own travel vertical」；BBC「preferring to create its own content (e.g. its own travel channel)」 | BBC Trust 檢討報告 PDF | https://downloads.bbc.co.uk/bbctrust/assets/files/pdf/our_work/lonely_planet/lonely_planet.pdf | ✅ |
| 54 | 本來可以變成 TripAdvisor | CONFIRMED（**強轉折**） | 「Lonely Planet/BBCW was too slow in reacting to fast-changing markets … with the result that Lonely Planet might have adopted the TripAdvisor model or successfully ridden the subsequent social accommodation wave.」 | 同上 | 同上 | ✅ |
| 55 | 估值太樂觀、書市下滑沒算進去 | CONFIRMED | 「An EBITDA margin of 30% was highly optimistic」；「BBCW seemed to get carried away with deal momentum」；「Not enough downside analysis was done of the potential impact of a faster decline in books」 | 同上 | 同上 | ✅ |
| 56 | 報喜不報憂、沒想到外界反彈 | CONFIRMED | 「Throughout its ownership of Lonely Planet there was a bias to positive in the reporting on performance, despite evident signs that all was not well.」；「the strength of the adverse public reaction to the acquisition seemed to take some parts of the BBC by surprise」 | 同上 | 同上 | ✅ |
| 57 | 報告自己拿 MySpace 來比 | CONFIRMED | 「ITV sold four years later at a loss of £150m, and that News Corp lost over $500m when it sold MySpace six years after acquiring it」；另列「significant and unforeseen appreciation of the A$, the Global Financial Crisis and structural pressures in the book retailing market」 | 同上 | 同上 | ✅ |
| 58 | Trust 的兩次表態 | CONFIRMED | 2013-03-19：「Although this did not prove to be a good commercial investment … Worldwide would not make this sort of acquisition again」；2013-11 副主席 Diane Coyle：「Mistakes were made in the acquisition and handling of Lonely Planet.」報告由非執行董事 Brian McBride 主持 | BBC Trust 聲明；BBC Trust 檢討頁 | https://www.bbc.co.uk/bbctrust/news/press_releases/2013/lonely_planet.html ；https://www.bbc.co.uk/bbctrust/our_work/commercial/lonely_planet_review.html | ✅ |
| 59 | Wheeler：「我們賣在最完美的時機」 | CONFIRMED（**強轉折**） | AP 2013：「There's no question we sold out at the perfect moment. It wasn't just the recession that hurt Lonely Planet – we also sold out just as the Australian dollar took off.」 | AP（Spokesman-Review 轉載，2013-09-01） | https://www.spokesman.com/stories/2013/sep/01/dark-adventures/ | ✅ |
| 60 | Wheeler 罵 BBC「一場災難」 | CONFIRMED（二手） | 2015 年 Ubud 作家節受訪：「It was a total disaster. They bought the Lonely Planet car. They should have put some fuel in the tank, and put it flat to the floor. Instead they got in the car, and said 'what do we do?' Let's drive slowly.'」 | BusinessWorld（2015-11-13） | https://bworldonline.com/travel-tourism/2015/11/13/11726/lonely-planet-founder-reprises-original-trip-on-budget-air/ | △ |
| 61 | Wheeler：BBC 沒看到非英語市場 | CONFIRMED | 「One of the things about LP that the BBC didn't really pick up on is that we look at it as an English-language brand, but it's very big in other languages … We're the biggest seller of guidebooks in the Italian language.」 | AP（2013） | https://www.spokesman.com/stories/2013/sep/01/dark-adventures/ | ✅ |
| 62 | 「Wheeler 後悔賣掉」 | UNVERIFIED | 沒有找到 Tony Wheeler 說「後悔賣掉」的一手話；他說的是「賣在最好時機」（第 59 列）與「BBC 搞砸」（第 60 列）。Maureen「no regrets」的 IOL 2012 專訪打不開。**旁白不說誰後悔** | — | — | ⚠ |
| 63 | NC2 接手四個月就裁員 | CONFIRMED（導言） | 「Four months after buying Lonely Planet from BBC Worldwide, new owner NC2 Media will announce staff reductions … expected to hit the Melbourne office the hardest」；「Australian media reported numbers up to 100」 | Skift（2013-07-17，兩篇） | https://skift.com/2013/07/17/lonely-planet-to-cut-staff-and-move-digital-offices-to-nashville/ ；https://skift.com/2013/07/17/statement-from-lonely-planet-regarding-staff-cuts-and-reorganization/ | △ |
| 64 | 2020 年疫情：墨爾本、倫敦幾乎全關，雜誌停刊 | CONFIRMED | 「essentially shuttering its Melbourne and London offices, due to the economic impact of Covid-19」（B+P 2020-04-09 導言）；公司聲明「Lonely Planet will continue to publish guidebooks and phrasebooks」，停掉雜誌、童書與主題書 | Books+Publishing；FMT 轉 The Bookseller | https://www.booksandpublishing.com.au/articles/2020/04/09/149112/redundancies-expected-as-lonely-planet-reduces-global-publishing-operations-melbourne-office-to-close-almost-entirely/ ；https://www.freemalaysiatoday.com/category/leisure/2020/04/15/lonely-planet-to-shut-magazine-non-destination-guidebooks | ✅ |
| 65 | 都柏林辦公室留下 | CONFIRMED（導言） | 「How Lonely Planet's intellectual property move saved its Dublin office from Covid-19 cull」；公司發言人：「The impact of Covid-19 on Lonely Planet has been both swift and severe」 | The Currency | https://thecurrency.news/articles/16151/guide-price-how-lonely-planets-intellectual-property-move-saved-its-dublin-office-from-covid-19-cull | △ |
| 66 | 2020 年 12 月賣給 Red Ventures | CONFIRMED | 「has acquired Lonely Planet … from NC2 Media for an undisclosed amount」；「Red Ventures aims to propel Lonely Planet into the digital era while remaining committed to publishing the guidebooks」；同一投資組合有 The Points Guy | Red Ventures 新聞稿；The Points Guy（2020-12-01） | https://redventures.com/press/press-releases/red-ventures-acquires-lonely-planet ；https://thepointsguy.com/news/tpgs-parent-company-buys-lonely-planet-in-major-expansion-of-travel-portfolio | ✅ |
| 67 | Red Ventures 付了多少 | UNVERIFIED | 官方「undisclosed」；Skift 估「$50 million range」只見於搜尋摘要，未開頁。**旁白不講金額** | Red Ventures | https://redventures.com/press/press-releases/red-ventures-acquires-lonely-planet | ⚠ |
| 68 | 2024 年退出中國 | CONFIRMED（二手） | 「宣布退出中國市場。Lonely Planet 於中國的辨公室已經關閉，停止在中國的出版業務」；中國期刊版「早在 2023 年正式停刊」 | unwire.hk（2024-06-27） | https://unwire.hk/2024/06/27/lonely-island-no-longer-in-the-chinese-market/hottopic/ | △ |
| 69 | 網路吃掉指南書：美國數字 | CONFIRMED | 「the nation's retailers sold 7.97 million books in the adult non-fiction/travel category last year, a 19-percent drop from 2011 and a 27-percent drop from 2010」（Nielsen BookScan，美國）；2008 年美國旅遊書市場「fell 16% … to $279 million」 | NBC News（2013-03-20）；Publishers Weekly（2009） | https://www.nbcnews.com/travel/travelkit/does-lonely-planets-sale-mark-death-print-travel-guides-1C8957602 ；https://publishersweekly.com/pw/print/20090316/14072-travel-book-market-tanked-in-2008.html | ✅（**是美國數字，不能說成英國**） |
| 70 | 英美指南書 2006–14 年跌約 45% | CONFIRMED（二手） | 「With sales of guidebooks peaking in the UK and the US in 2005, they fell by around 45% from 2006-14.」；2015 年英國「up 4.45%」（Nielsen BookScan Travel Publishing Year Book） | travelnews.ch（2016-03-22） | https://www.travelnews.ch/english-corner/2034-the-return-of-travel-guidebooks.html | △ |
| 71 | 高雄：2018 年全球最佳城市第 5 | CONFIRMED | 「Kaohsiung in southern Taiwan has been named as the fifth best city in the world to visit in 2018 by travel guide book publisher Lonely Planet」 | 中央社 Focus Taiwan（2017-10-25） | https://focustaiwan.tw/society/201710250005 | ✅ |
| 72 | 台北：2022 年最佳城市第 2 | CONFIRMED | 「Taipei came in second only to Auckland, New Zealand」；弗萊堡大學：「ranks Freiburg TOP3 … behind Auckland (NZ) and Taipei (TWN)」 | Taiwan News；弗萊堡大學 | https://www.taiwannews.com.tw/en/news/4343236 ；https://sfb1425.uni-freiburg.de/news/freiburg-ranked-top3-travel-2022 | ✅ |
| 73 | 台灣入選 Best in Travel 2027 | CONFIRMED（新） | 2027 年 50 個地點（不排名次）之一，標題「Taiwan — Best for night market grazing」，作者 Piera Chen | Lonely Planet Best in Travel 2027（canonical：https://www.lonelyplanet.com/best-in-travel） | https://www.lonelyplanet.com/articles/best-in-travel-cities-2023 | ✅（**不能說「第幾名」**） |
| 74 | 最新台灣指南 | CONFIRMED（零售頁） | Lonely Planet《Taiwan》第 12 版，2023-11-01 上架，456 頁 | Apple Books | https://books.apple.com/au/book/taiwan-12/id6473789206 | △ |
| 75 | Wheeler 夫婦現況 | CONFIRMED | 「In 2011 we completed the sale of Lonely Planet」；「Planet Wheeler, the foundation Maureen and I set up after we left Lonely Planet」；另有倫敦商學院 Wheeler Institute、墨爾本 Wheeler Centre；2023 年 Big Issue 稱 Tony「now 76」 | Tony Wheeler 網站；Big Issue | https://tonywheeler.com.au/about-tony ；https://www.bigissue.com/life/lonely-planet-travel-book-50-years-history | ✅ |
| 76 | 「用的是收視費」 | CHANGED | AFP：「Worldwide stressed that no taxpayers' money from the publicly-funded BBC had been used to buy Lonely Planet.」**旁白說「用的是商業部門的錢，不是收視費——但商業部門賺的錢本來要回饋 BBC」** | The Peninsula（AFP 稿，2013-03-19） | https://thepeninsulaqatar.com/article/19/03/2013/bbc-to-sell-lonely-planet-at-ps80m-loss | △ |
| 77 | 2007 年 75% 的價格在 2013 年之前就已公開（查核代理補） | CONFIRMED | 《衛報》2011-02-18：「In October 2007, the corporation acquired a 75% stake in Lonely Planet for £88.1m」。所以 t048「六年後…才寫出來」不成立 | 《衛報》 | https://www.theguardian.com/media/2011/feb/18/bbc-worldwide-lonely-planet-travel-guides | ✅ |
| 78 | 2015 年「一場徹底的災難」是路透社的訪問（查核代理補） | CONFIRMED | BusinessWorld 該篇：「Mr. Wheeler said in an interview on the sidelines of the Ubud Writers and Readers Festival」，文末署「— Reuters」 | BusinessWorld（轉載路透社） | https://bworldonline.com/travel-tourism/2015/11/13/11726/lonely-planet-founder-reprises-original-trip-on-budget-air/ | ✅ |
| 79 | 2007 到行使賣權約三年半（查核代理補） | CONFIRMED | Lonely Planet 董事長 Marcus Arthur：「The put option enabled us to benefit from the Wheelers' experience over the last three and a half years」；同篇說 Wheeler 夫婦「co-founded the Australian travel publisher in 1973」 | 《衛報》2011-02-18 | https://www.theguardian.com/media/2011/feb/18/bbc-worldwide-lonely-planet-travel-guides | ✅ |
| 80 | 檢討報告是誰做的、何時發表（查核代理補） | CONFIRMED | Trust 頁：「it asked the Executive to commission a review of lessons learnt」；PDF：「led by BBC Non-Executive Director Brian McBride and assisted by an external consultant」；PDF 建檔 2013-11-06（pdfinfo）；Coyle 署名「BBC Vice-Chairman」 | BBC Trust 檢討頁；BBC Trust PDF | https://www.bbc.co.uk/bbctrust/our_work/commercial/lonely_planet_review.html ；https://downloads.bbc.co.uk/bbctrust/assets/files/pdf/our_work/lonely_planet/lonely_planet.pdf | ✅ |
| 81 | AP 問 Wheeler 景點擠爆的原句（查核代理補） | CONFIRMED | 「AP: Many places that were once off the beaten path have become overrun, and sometimes Lonely Planet recommendations contributed to that. How was this trip different?」 | AP（Spokesman-Review 轉載，2013-09-01） | https://www.spokesman.com/stories/2013/sep/01/dark-adventures/ | ✅ |
| 82 | 「33 種語言」指的是內容（查核代理補） | CONFIRMED | 〈About〉：「content translated into 33 languages」；Red Ventures 2020：「guidebooks in 14 languages」 | Lonely Planet〈About〉；Red Ventures 新聞稿 | https://www.lonelyplanet.com/about ；https://redventures.com/press/press-releases/red-ventures-acquires-lonely-planet | ✅ |
| 83 | 「照原價」是澳幣口徑（查核代理補，推算） | 推算 | Trust：兩次合計 A$277m；2011 年那 25% 是 A$67.2m →2007 年 75% 約 A$209.8m，換算每 25% 約 A$69.9m，與 A$67.2m 相近；英鎊口徑 £88.1m÷3≈£29.4m，2011 年卻付 £42.17m，差額來自澳幣升值。**旁白沒用；要用須另找一手來源** | BBC Trust PDF；《衛報》2011；BBC 2013 | https://downloads.bbc.co.uk/bbctrust/assets/files/pdf/our_work/lonely_planet/lonely_planet.pdf | △ |
| 84 | bbc.com 延誤的原文（查核代理補） | CONFIRMED | 「It also relied on the BBC to re-launch bbc.com with Global News and US websites, which were delayed. These delays had a negative impact on Lonely Planet's ability to generate meaningful advertising revenue」；「bbc.com was delayed and then decided to build its own travel vertical」。報告沒有用「競爭」「搶」之類的字 | BBC Trust PDF | https://downloads.bbc.co.uk/bbctrust/assets/files/pdf/our_work/lonely_planet/lonely_planet.pdf | ✅ |
| 85 | 2013 年的新聞標題怎麼寫（查核代理補） | CONFIRMED | 《衛報》標題「BBC Worldwide criticised for sale of Lonely Planet at 'significant loss'」（£80m 在內文）；法新社稿（Peninsula）標題「BBC to sell Lonely Planet at £80m loss」，內文「a loss of almost £80 million」 | 《衛報》；The Peninsula（AFP） | https://www.theguardian.com/media/2013/mar/19/bbc-worldwide-criticised-lonely-planet-sale ；https://thepeninsulaqatar.com/article/19/03/2013/bbc-to-sell-lonely-planet-at-ps80m-loss | ✅ |

## 第二輪（盲評後改稿）逐句核對

- 查核者：同一個獨立查核代理，2026-10-31。比對 commit `38fa4b60`（盲評後重寫）與 `d3b828ca`（第一輪修稿）的 `video.json`：新增或改寫的旁白 26 行、改了的卡片 1 張、新提示詞 17 張；標題、說明、縮圖這次沒改。主對話點名的開場句與第一章標題雖然沒改，也一起列出。
- 重新開頁：BBC 2007 新聞稿、BBC Trust 2007-10-01 核准頁、BBC Trust 2013-03-19 聲明頁（頁面日期「19.03.2013」）、Trust 檢討報告 PDF、《衛報》2009-09-23 與 2011-02-18、AP 2013、Big Issue，都用 curl 經代理讀到原文。
- 結果：26 行裡 OK 23、SOFTEN 2、FIX 1；卡片 OK；提示詞 1 張違反人物規則（trust-lectern-2），2 張建議加「無字」。

| 行 | 旁白或卡片（節錄） | 列 | 判定 | 說明 |
|---|---|---|---|---|
| 章名 | 口袋裡二十七分錢，三十四年後賣給電視台 | #4 #27 | OK | 1972-12-26 只剩 27 分錢，到 2007-10-01 是 34 年又 9 個月，「三十四年後」成立；買的是 BBC 的商業部門，「電視台」可以接受 |
| t003 | 一九七二年聖誕節隔天，一對年輕夫妻到了雪梨，身上只剩二十七分錢。 | #4 | OK | 〈About Tony〉「the day after Christmas 1972 … 27 cents left between us」；Big Issue 稱兩人是「newlyweds」 |
| open-promise（卡） | sub：從一本廚房桌上釘的小書開始 | #6 | OK | 只把 sub 換掉，£130.2m 與 2007、2011 照舊正確 |
| t007 | 而 BBC 自家的網站，後來做了一個決定。 | #53 #84 | OK | 報告「bbc.com was delayed and then decided to build its own travel vertical」，主詞本來就是 bbc.com |
| t008 | 這份檔案，把這一億三千萬英鎊，一筆筆攤開給你看。 | #41 | OK | 承諾句 |
| t028 | 外號叫：黃色聖經。 | #14 | OK | CS Monitor 1992 |
| t031 | 你出國前翻的那幾本，便宜的、貴的都寫，就是從這裡來的。 | #17 | SOFTEN | Wheeler 只說 Lonely Planet 自己從尼泊爾那本起「covered the expensive places as well … ever since」；「你翻的那幾本」聽起來像所有旅遊書都從這裡來，超出這一列。改：「從那本起，它的書便宜的、貴的都寫，你翻的也是。」 |
| t035 | 他怎麼回？ | — | OK | 問句 |
| t038 | 我覺得這件T恤，比任何銷量數字都更能說明它有多紅。 | #19 | OK | 有標「我覺得」，是旁白的看法；AP 的問題本身就把擠爆跟 Lonely Planet 的推薦連在一起（#81） |
| t039 | 那本釘起來的小書，後來長成多大？ | — | OK | 問句 |
| t041 | 網站每個月，有四百三十萬個訪客。 | #22 | OK | BBC 2007 新聞稿「Lonely Planet's website receives 4.3 million unique visitors a month」（重讀），接在 t040 的二〇〇七年後面，年份對 |
| t053 | BBC 內部把關的信託會也沒有一口答應，開了四個條件， | #31 | OK | Trust 2007-10-01 頁：「It approved the proposed acquisition subject to four conditions being met」（重讀） |
| t054 | 還要證明這筆買賣，能讓 BBC 的節目和品牌更值錢。 | #31 | OK | 原文「leverage extra value from the BBC's intellectual property」，同頁另說要讓「BBC programmes in those genres associated with travel」的觀眾受益；「節目和品牌」是智慧財產的白話，可以接受 |
| t063 | 九月，委員會又補了一份報告，這次用了什麼字？ | #35 | OK | 2009 年 9 月 |
| t067 | 同一個月，倫敦一家城市雜誌的創辦人說，它賠錢賠得一塌糊塗， | #33 | OK | Elliott「Lonely Planet is losing money hand over fist」，《衛報》寫「Elliott claimed」；旁白有「創辦人說」，是對手的說法而且有歸屬。同篇同月（2009-09） |
| t068 | BBC 得一直往裡面砸幾百萬。憑什麼不能逼他們賣掉？ | #33 | OK | 「They are having to pump million into it」「Why shouldn't they be forced to sell it?」，仍在 t067 的「說」底下 |
| t072 | 紙本以外的收入，從百分之九拉到百分之二十二。 | #38 | SOFTEN | 原文是占比：「non-print revenues have grown from 9% in 2007 to 22% in the year to the end of March 2010」；少了「占比」會聽成收入金額成長。改：「紙本以外的收入占比，從百分之九拉到百分之二十二。」 |
| t089 | 報告的說法是：BBC 比較喜歡自己做內容。 | #53 | OK | 「which it was reluctant to do, preferring to create its own content (e.g. its own travel channel)」 |
| t090 | 報告說，這些延誤，讓它很難靠廣告賺到像樣的錢。 | #84 | OK | 「These delays had a negative impact on Lonely Planet's ability to generate meaningful advertising revenue」；「很難」略強於「negative impact」，仍在範圍內 |
| t103 | 報告也承認：當年外界反彈這麼大，似乎讓 BBC 有些部門很意外。 | #56 | OK | 「the strength of the adverse public reaction to the acquisition seemed to take some parts of the BBC by surprise」，連「似乎」也保留了 |
| t106 | 換成英鎊，大約五千一百五十萬。 | #43 | OK | £51.5m |
| t107 | 而且不是一次付清：六千萬澳幣先付，一千五百萬一年後再付。 | #43 | OK | 「AU$60m (£41.2m) paid on completion and AU$15m (£10.3m) paid in one year's time」 |
| t123 | 信託會在宣布當天也承認：這不是一筆好的商業投資。 | #58 | OK | Trust 聲明頁日期 19.03.2013，與 BBC 宣布出售同一天；「did not prove to be a good commercial investment」 |
| t127 | 還記得 BBC 怪的那個強勢澳幣嗎？他說，他們正好在澳幣起飛的時候賣掉。 | #46 #59 | OK | BBC 新聞稿確實把業績歸給「the continued strength of the Australian dollar」；Wheeler「we also sold out just as the Australian dollar took off」 |
| t129 | 他也說 BBC 沒看懂一件事：在義大利文的旅遊書裡，它賣得最多。 | #61 | OK | 原文是 BBC「didn't really pick up on」它在英語以外也很大，義大利文是他舉的證據：「We're the biggest seller of guidebooks in the Italian language」。濃縮過，但沒有說錯 |
| t130 | 兩個月後，BBC 這邊又開口了。信託會副主席說： | #58 #80 | OK | 接在 2013 年 9 月 AP 之後；檢討報告 PDF 建檔 2013-11-06，Trust 頁上是 Coyle 的話，九月到十一月剛好兩個月 |
| t131 | 收購和經營它的過程中，犯了錯。 | #58 | OK | 「Mistakes were made in the acquisition and handling of Lonely Planet」（文字沒改，但配圖換了，見下方） |
| t140 | 下次你在書店翻到它，可以想想它背後這本帳。 | — | OK | 收尾 |
| t142 | 紀錄給的答案不只一個；信託會自己的結論是：以後不會再做這種收購。 | #58 #80 | FIX | 照 #58 逐字看有三個問題。(1) 這是 Coyle 在 2013-03-19 賣出當天的聲明，不是什麼「結論」；檢討報告的 Conclusions 寫的是「another acquisition like this probably could not happen」，而且兩次都把原因歸給治理與策略改了。(2) 原文主詞是商業部門：「Worldwide would not make this sort of acquisition again」，不是信託會自己不做。(3) t141 剛問「BBC 為什麼賠著賣掉？」，這句回的是「以後不做」，不是為什麼，答案句裡沒有任何原因。改成兩句：「紀錄給的答案不只一個：估太高、轉太慢，又碰上壞時機。」（#55 #57 #84，同第一輪 t140）；要留信託會那句就另起一行：「信託會賣掉當天就說：商業部門不會再做這種收購。」 |

**新提示詞的人物規則**

| 景 | 判定 | 說明 |
|---|---|---|
| trust-lectern-2 | FIX（違規） | 「a woman economist in a dark jacket at a committee table speaking into a microphone … a steady frank look」，配的是 Diane Coyle（在世、經濟學家）說的話：用職業加性別指認、正面中景、有表情。第一輪的「grey-haired woman board member」只是換了一個指認詞。改成只有物件，例如「Close-up of a microphone and a glass of water on an empty committee table, a single blank sheet with no writing beside it, cool overcast light」，或把 t131 併進已經合格的 trust-lectern。改之前，說明裡「在世…人物不入畫」那句不成立 |
| trust-statement | 建議 | 「a single printed statement」很可能畫出可讀的字，加「blank sheet with no writing」 |
| tablet-cafe | 建議 | 平板上的「glowing map」可能畫出地名，加「with no labels」 |
| nepal-hotel-2、crowd-lane-2、souvenir-shop、grow-q、warehouse-2、trust-four、trust-tv、leaky-bucket、own-sketches、coin-jar、mail-flood、sale-piles、italy-bookshop、bookshop-today | OK | 都是不指認的一般人物或只有物件、手。crowd-lane-2 的記者沒有對到任何具名的人。第一輪點名的惠勒夫婦、John Smith、Elliott、Kelley 替身都已改成物件、手或不相干的路人；Bodine 那段已經刪掉 |

## 第三輪（盲評第 2 輪後）逐句核對

- 查核者：同一個獨立查核代理，2026-10-31。比對 commit `1a575573a`（盲評第 2 輪後改稿）與 `8867f2f89`（第二輪查核修正後）的 `video.json`：新增或改寫的旁白 18 行、新章名 1 個、新提示詞 9 張；卡片、標題、縮圖沒改，說明沒改（但內容因刪段而過時，見表尾）。
- 重新開頁：BBC 2013 新聞稿（網站與 app 數字）、BBC Trust 檢討報告 PDF、《衛報》2011-02-18、AP 2013、Books+Publishing 2011-05-15，都用 curl 經代理讀到原文。另補兩列：#86 advanced-television 2009-11-25（curl 讀到原文）；Press Gazette 與 Marketing Week 同主題的報導回 403，沒有採用。
- 結果：18 行裡 OK 15、SOFTEN 2、FIX 1（t063）；另有 t064 字沒改、但前後文變了要 FIX，說明也要 FIX；9 張新提示詞都合規。

| 行 | 旁白或卡片（節錄） | 列 | 判定 | 說明 |
|---|---|---|---|---|
| 章名 | 一台破車，一張廚房的桌子 | #1 #6 | OK | 換掉了歌名，事實沒變 |
| t006 | 創辦人手上最後那四分之一，BBC 後來用什麼價錢買？ | #27 #39 | OK | 預告句 |
| t008 | 這份檔案，把這筆錢六年的帳，一筆筆攤開給你看。 | #41 #43 | OK | 2007→2013 是六年 |
| t009 | 這一億三千萬英鎊，最後換回了什麼？ | #41 | OK | 問句 |
| t027 | 連惠勒自己都說：以前空空的地方，現在大家都知道了。 | #19 #81 | SOFTEN | AP 原文「You go back to places you really loved … sort of empty, and now everybody knows them」是回答記者「有時 LP 的推薦也有份」那一問；他沒有自己說是書造成的。「連…自己都說」放在 t026「書寫到哪裡，人就跟到哪裡」之後，就變成他承認了因果。改：「問到被推薦擠爆的地方，惠勒說：以前空空，現在大家都知道了。」 |
| t031 | 我覺得，廚房裡起家的小出版社長成這樣，難怪有人想買。 | — | OK | 有標「我覺得」，是旁白的看法，前面兩行的 500 多種書、650 萬本、430 萬訪客都已查過 |
| t063 | 信託會也定了規矩：除非情況特殊，以後不准再做這種收購。 | #38 #86 | FIX | 內容對（《衛報》2011：Trust ruling「must not undertake similar acquisitions in the future unless there are "exceptional circumstances"」），時間錯位。這條規矩是 **2009 年 11 月**定的（#86：信託會主席 Lyons 2009-11-25 公布 Worldwide 的新權限「An end to mergers and acquisitions unless there are exceptional circumstances」，並說不會再考慮 Lonely Planet 這種規模與性質的交易），稿子卻把它放在 2011 年 2 月轉盈與「同一個月」賣權之間，聽起來像 2011 年才定。改：「二〇〇九年底信託會就定了規矩：除非情況特殊，不准再這樣收購。」或把這行移到 t059／t060 之前 |
| t064（未改字，前後文變了） | 同一個月，惠勒夫婦翻出了合約裡的一張牌。 | #39 | FIX | t063 插進來以後，「同一個月」接的是信託會定規矩那一句，不再是 t061 的 2011 年 2 月。改：「二〇一一年二月，惠勒夫婦翻出了合約裡的一張牌。」（如果把 t063 移走，這行就可以不動） |
| t071 | 理由是：業績明顯不如預期，合約卻沒有因此打任何折扣。 | #39 | OK | 「the vendors received the original acquisition price when they exercised the put, despite the significant under-performance of the business」。「沒打折」是就原價（澳幣口徑）說的，見 #83 |
| t072 | 兩次加起來是多少？ | #41 | OK | 問句 |
| t073 | 就是開頭那大約一億三千萬英鎊。 | #41 | OK | 88.1＋42.17 |
| t074 | 同年五月，據澳洲出版業的媒體報導，墨爾本最多要裁掉七十個人， | #42 | OK | B+P 2011-05-15「Lonely Planet informed staff at its Melbourne office last week that as many as 70 jobs will be lost」；△ 已標出處（「據…媒體報導」）；「同年」接 t073 前的 2011 |
| t075 | 網站的工作，大半搬去倫敦。 | #42 | SOFTEN | 原文「relocating a substantial part of its web operations to London」：是「相當一部分」，不是「大半」。改：「網站業務有相當一部分，搬去倫敦。」（Trust 報告也提到「migrating the website to London」是收購兩年多後才做） |
| t099 | 那，全都怪 BBC 嗎？ | — | OK | 問句 |
| t100 | 報告也列了它控制不了的事：澳幣意外大漲、金融海嘯， | #57 | OK | 「factors beyond BBCW's control … the significant and unforeseen appreciation of the A$, the Global Financial Crisis」 |
| t101 | 還有書店通路的結構壓力。 | #57 | OK | 「structural pressures in the book retailing market」；同段報告接著說 BBCW 仍然「could have done a better job」，下一章已有交代 |
| t106 | 賣掉的時候，它的網站一年有一億兩千多萬人來看， | #23 | OK | BBC 2013「more than 120million unique users visiting its website every year」：單位是每年不重複使用者，「一年」「一億兩千多萬人」都對得上（重讀） |
| t107 | 手機 app 也被下載了超過一千一百萬次。 | #23 | OK | 「more than 11million apps downloaded」，是累計下載次數 |
| t115 | 算法很簡單：開頭那一億三千萬，減掉剛剛那筆賣價。 | #41 #43 | OK | 賣價 £51.5m 在 t104 剛講過 |
| t141 | 回到開頭的問題：這筆錢換回的不到一半，為什麼？ | #41 #43 | OK | 51.5÷130.2＝39.6%，不到一半；回扣 t009 |
| 說明 | 這一集照時間講：唱錯的歌怎麼變成 Lonely Planet；… | — | FIX | 歌名那段（〈太空船長〉、唱錯的歌詞）這一版已經刪掉，說明還在預告它。改成「一台破車、一張廚房桌子，怎麼變成 Lonely Planet」；其餘段落照舊成立 |

**新提示詞的人物規則**：tower-books、rubber-stamp、auditor-chart、office-box、office-box-2、gavel-file、rain-shop、app-grid、app-grid-2 都是不指認的一般人物或只有物件；有寫字可能的地方（表單、檔案、app 圖示）都已註明「no writing／no labels」。auditor-chart 的稽核員沒有對到具名的人（檢討報告的 Brian McBride 旁白沒提）。沒有違規。

**本輪補的列**（接在〈逐項查核〉表 #85 後面的編號）

| # | 主張 | 判定 | 原文引句或數字 | 來源 | 網址 | 信心 |
|---|---|---|---|---|---|---|
| 86 | 信託會「除非情況特殊，不准再收購」是哪一年定的（查核代理補） | CONFIRMED | 2009-11-25：「Sir Michael Lyons, the BBC Trust chairman, outlined a tighter remit for BBC Worldwide that will prevent the corporation's commercial arm making further acquisitions such as the Lonely Planet travel publisher deal」；新權限之一「An end to mergers and acquisitions unless there are exceptional circumstances」；「the Trust would not expect to consider a commercial deal of the scale and nature of the Lonely Planet acquisition in future」 | Advanced Television | https://www.advanced-television.com/2009/11/25/bbc-trust-no-more-deals-ae%E2%80%9C-except-virgin-media/ | △（業界媒體；與《衛報》2011 第 38 列一致） |
| 87 | 2011 年 5 月裁員、網站搬倫敦的原句（查核代理補） | CONFIRMED（導言） | 「Lonely Planet informed staff at its Melbourne office last week that as many as 70 jobs will be lost as part of a restructure that will result in the…」；標題「Lonely Planet to cut up to 70 jobs, move web operations to UK」；第 42 列另引「relocating a substantial part of its web operations to London」 | Books+Publishing（2011-05-15） | https://www.booksandpublishing.com.au/articles/2011/05/15/19766/lonely-planet-to-cut-up-to-70-jobs-move-web-operations-to-uk/ | △ |

## 第四輪（盲評第 3 輪後）逐句核對

- 查核者：同一個獨立查核代理，2026-10-31。比對 `video.json` 的 `1d5f0780c`（盲評第 3 輪後的檢查點；`56a90df3d` 沒有再動 video.json）與 `b15c7abc1`（第三輪查核修正後）：新增或改寫的旁白 10 行、新章名 1 個、新提示詞 3 張；卡片、標題、縮圖沒改，說明已照第三輪改好。
- 依據：第 79、80、84 列與 PDF 原文（本輪重讀）、《衛報》2011-02-18 與 2013-03-19（已存的原文）。
- 結果：10 行裡 OK 9、SOFTEN 1、FIX 0；章名 OK；3 張新提示詞合規。

| 行 | 旁白或卡片（節錄） | 列 | 判定 | 說明 |
|---|---|---|---|---|
| 章名 | 一九七三年，廚房桌上釘出第一本書 | #6 #10 | OK | 1973 年、廚房桌、釘書 |
| t024 | 你猜，那本釘起來的小書，後來長成多大？ | — | OK | 問句。附註：前一行 t023「書寫到哪裡，人就跟到哪裡。」原本後面有 Wheeler 的峇里島那段撐著，這一版拿掉了，現在只剩旁白自己的概括（#18 是創辦人自述的 △）；沒改字所以不判，想更穩可以標成惠勒的說法 |
| t068 | 當時公司董事長的說法是：這個賣權，讓公司三年半來都借重了惠勒夫婦的經驗。 | #79 | OK | Marcus Arthur（「chairman of Lonely Planet and managing director of BBC Worldwide's global brands division」）：「The put option enabled us to benefit from the Wheelers' experience over the last three and a half years」。有標是他的說法；他同時是 BBC Worldwide 的主管 |
| t076 | 那份檢討是信託會要 BBC 自己做的，由一位非執行董事主持，還找了外部顧問。 | #80 | OK | Trust 頁「it asked the Executive to commission a review」；PDF「led by BBC Non-Executive Director Brian McBride and assisted by an external consultant」 |
| t077 | 這份報告說，它的網路生意，要接上 BBC 的國際網站，一起賣廣告。 | #53 | OK | 「dependent on connecting to bbc.com and monetising the content through advertising」 |
| t082 | 這一延，它就很難靠廣告賺到像樣的錢。 | #84 | SOFTEN | 原文「These delays had a negative impact on Lonely Planet's ability to generate meaningful advertising revenue」。上一版有「報告說」，這一版拿掉了，變成旁白自己下的因果，「就很難」也比「negative impact」重。改：「報告說，這些延誤讓它更難靠廣告賺到像樣的錢。」 |
| t088 | 網路上它也動得太慢；報告說，它本來可能走上 TripAdvisor 的路， | #54 | OK | 「too slow in reacting to fast-changing markets … might have adopted the TripAdvisor model」；同一句裡有「報告說」 |
| t091 | 報告把問題追到買的那一天：收購計畫假設營業利潤率有三成。 | #55 | OK | 報告 Summary 的「Acquisition」一節：「An EBITDA margin of 30% was highly optimistic」；「營業利潤率」沿用第一輪的寫法 |
| t092 | 報告說這太樂觀；買方似乎被交易氣勢沖昏了頭，書市會掉多快，也沒細算。 | #55 | OK | 「highly optimistic」「seemed to get carried away with deal momentum」「Not enough downside analysis … faster decline in books」 |
| t111 | 帳上的價值，就從開頭那一億三千萬，一路減到六千三百萬。 | #48 | OK | £63m 有來源：《衛報》「written down the value of Lonely Planet by £67m over the last six years **to £63m**」。起點「一億三千萬」是 63＋67 隱含的數字（等於 £130.2m 的總價），《衛報》沒有直接寫；兩數相加正好吻合，可以不標推算 |
| t121 | 還記得報告怪的那個澳幣嗎？惠勒說，他們正好在澳幣起飛的時候賣掉。 | #57 #59 | OK | 檢討報告確實把「unforeseen appreciation of the A$」列為控制不了的因素（t094 剛講過）；AP「we also sold out just as the Australian dollar took off」 |

**新提示詞的人物規則**：put-handshake 只拍兩隻袖子和反扣的合約；review-binder 的「outside consultant」是報告裡沒具名的外部顧問，沒有可以指認的特徵，主持的 Brian McBride（在世）沒有入畫；ledger-book-2 是兩疊鈔票加會計的眼睛。都合規，沒有字或 logo。
