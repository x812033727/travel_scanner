# curio-h01 查核第一輪

- 查核 2026-10-10，Claude Fable 5.1（查核代理，不是撰稿的那一個）。
- 方法：先把 `video.json` 的每句旁白、每張卡片、縮圖、標題、說明欄、標籤、`assets[]` 抽成 263 條清單（`<home>\mokaair-work\videos\curio-h01\_tools\verify1\claims-list.txt`），再把 `research.md` 與 `claims.md` 列的每個網址當天用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.2 秒）重開，去掉註解後讀全文。沒有用網路搜尋（0／5 次）。
- 這是歷史題：「官方頁」指一手或權威的歷史來源。最重的是 maryceleste.net 轉錄的 Gibraltar Chronicle 1872–73（含 Austin 勘驗摘要、Shufeldt 報告、判決）、The History Press 引的 Austin 報告原文與 Solly-Flood 1873-01-22 信、Wikisource 的道爾 1884 全文、Commons 的 1873 紐約時報剪報全文；其次 Smithsonian Magazine 2007、Britannica、American Heritage 1981（引 Bryan 與 Fay 1942）。Skeptoid、History Hit、Fishermen's Voice、NEHS、Slate 只用來佐證，單獨不能定案。Wikipedia 沒有用。
- 改動原則照查核提示：只改事實與連帶的地方，不動風格、順序、節奏；每句旁白維持 24 單位以內；行 id 不變；沒有加場景或句子。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| SM07 | https://www.smithsonianmag.com/history/abandoned-ship-the-mary-celeste-174488104/ | 200 |
| EB | https://www.britannica.com/topic/Mary-Celeste （頁面標 Last updated Sep. 18, 2026；這天 curl 開得了） | 200 |
| AH | https://www.americanheritage.com/mystery-mary-celeste | 200 |
| MCN/facts | https://www.maryceleste.net/facts.htm | 200 |
| MCN/news | https://www.maryceleste.net/news.htm （Gibraltar Chronicle 1872-12-13、1873-01-31、03-04、03-15） | 200 |
| MCN/spencer | https://www.maryceleste.net/spencer.htm | 200 |
| MCN/briggs | https://www.maryceleste.net/briggs.htm | 200 |
| MCN/barrel | https://www.maryceleste.net/barrel.htm | 200 |
| MCN/about | https://www.maryceleste.net/about.htm | 200 |
| THP | https://thehistorypress.co.uk/article/the-ongoing-mystery-of-the-mary-celeste/ | 200 |
| HH | https://www.historyhit.com/ghost-ship-what-happened-to-the-mary-celeste/ | 200 |
| FV | https://fishermensvoice.com/archives/201711TheMysteriousCaseOfTheMaryCeleste.html | 200 |
| NEHS | https://newenglandhistoricalsociety.com/mysterious-disappearance-mary-celeste/ | 200 |
| SL | https://www.slate.com/articles/life/culturebox/2011/12/the_mary_celeste_the_unluckiest_ship_to_ever_sail_the_seven_seas_.html | 200 |
| SK | https://skeptoid.com/episodes/289 | 200 |
| WS | https://en.wikisource.org/wiki/J._Habakuk_Jephson%27s_Statement | 200 |
| ACD | https://www.arthur-conan-doyle.com/wiki/Mary_Celeste | 200 |
| C-Amazon | https://commons.wikimedia.org/wiki/File:Mary_Celeste_as_Amazon_in_1861.jpg | 200 |
| C-Engraving | https://commons.wikimedia.org/wiki/File:Mary_Celeste_engraving.jpg | 200 |
| C-Briggs | https://commons.wikimedia.org/wiki/File:Benjamin_Briggs_captain_of_Mary_Celeste.jpg | 200 |
| C-Sarah | https://commons.wikimedia.org/wiki/File:Sarah_Briggs_wife_of_Benjamin.JPG | 200 |
| C-Sophia | https://commons.wikimedia.org/wiki/File:Sophia_Briggs_daughter_of_Benjamin.JPG | 200 |
| C-NYT | https://commons.wikimedia.org/wiki/File:Mary_Celeste_NYTimes_1873February26.png | 200 |
| EB-Bermuda | https://www.britannica.com/place/Bermuda-Triangle （查百慕達的聯想，全文沒有提這艘船） | 200 |

## 主張表

判定：CONFIRMED 看到了／CHANGED 改了／NOT FOUND 沒看到，拿掉或換掉／OUT OF SCOPE 風格、問句、系列安排，不動。

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 1 | 1872 年一艘完好的船上十個人全部消失 | youtube.title、thumbnail | EB、SM07、MCN/news（Austin：hull 無任何損傷） | 200 | CONFIRMED | — |
| 2 | 帆還張著、貨一桶都沒少、十個人不見 | youtube.description | AH（jib、staysail 張著）、MCN/news（1,701 桶「well stowed… except one which had been started」） | 200 | CONFIRMED | — |
| 3 | 1,701 桶酒精、六個月糧食、不見的小艇與航海儀器 | youtube.description | AH、SM07 | 200 | CONFIRMED | — |
| 4 | 直布羅陀副海事法院的三個月 | youtube.description | SM07「more than three months」；12-18 開庭→03-14 判決 | 200 | CONFIRMED | — |
| 5 | 檢察總長的謀殺推論、劍上「像血」、化驗結果 | youtube.description | THP（Austin 原文、Solly-Flood 信）、AH、MCN/news | 200 | CONFIRMED | — |
| 6 | 只有估值五分之一的救難金 | youtube.description | MCN/news（1873-03-15：「one fifth of the total value」$42,643）；SM07 說投保值 $46,000 的六分之一 | 200 | CHANGED | 只有估值五分之一 → 只有大約估值五分之一 |
| 7 | 把七種解釋過一遍 | youtube.description、kp6j、theories-table | 各來源合計至少八種說法 | 200 | CONFIRMED | — |
| 8 | 資料截至 2026-10-10 | youtube.description | 當天 | — | CONFIRMED | — |
| 9 | 標籤（船名、幽靈船、直布羅陀、柯南道爾…） | youtube.tags | — | — | CONFIRMED | — |
| 10 | 「十個人 全不見」「1872 年的檔案」 | thumbnail | EB、SM07 | 200 | CONFIRMED | — |
| 11 | 1861 年 Amazon 進馬賽港的畫，作者未確認，公有領域 | assets[0]、legend-amazon-painting | C-Amazon：「Brigantine Amazon entering Marseilles in November 1861」、Artist「Unconfirmed, possibly Honore Pellegrin」、PD | 200 | CONFIRMED | — |
| 12 | 1870–1890 年版畫，出自《300 Years of British Gibraltar》，繪者不明 | assets[1]、theories-engraving | C-Engraving：「between 1870 and 1890」、「No illustrator given」、PD | 200 | CONFIRMED | — |
| 13 | Briggs 船長肖像，公有領域 | assets[2]、find-briggs-portrait | C-Briggs：PD-old-100，無作者資訊 | 200 | CONFIRMED | — |
| 14 | Sarah Briggs 肖像，公有領域 | assets[3]、find-sarah-portrait | C-Sarah：PD-old-100 | 200 | CONFIRMED | — |
| 15 | Sophia Briggs 肖像（1872 年前），公有領域 | assets[4]、find-sophia-portrait | C-Sophia：「before 1872」、Unknown author、PD-old-100 | 200 | CONFIRMED | — |
| 16 | 紐約時報 1873-02-26 轉載波士頓郵報，公有領域 | assets[5]、court-nytimes | C-NYT：NYT 1873-02-26 p.2「citing the Boston Post of February 24, 1873」、PD-US | 200 | CONFIRMED | — |
| 17 | 一八七二年船還在走，十個人全不見 | hook/mwbb、hook.data | AH（「beating northwest under very short canvas」）、EB | 200 | CONFIRMED | — |
| 18 | 1872 年 12 月，大西洋 | hook.data.subtitle | AH、MCN/facts | 200 | CONFIRMED | — |
| 19 | 流傳版：桌上有熱飯菜、小艇都在 | hook-hot-meal/pyny、legend-listener/xfca、legend-list | MCN/facts 2–3（列為 erroneously reported）、AH | 200 | CONFIRMED（當傳說講） | — |
| 20 | 紀錄裡沒有這些，艙裡是一公尺的水 | hook-flooded-cabin/ftqe | MCN/facts 3；AH、SM07 3.5 呎；EB「more than 3 feet (1 meter)」 | 200 | CONFIRMED | — |
| 21 | 收尾問句 | hook-empty-vessel/hjvp | — | — | OUT OF SCOPE | — |
| 22 | 酒館裡講了一百五十年 | legend-chapter/r8im | 1872→2026 | — | CONFIRMED | — |
| 23 | 流傳版：帆還張著、一點傷都沒有 | legend-tavern/b7js | MCN/facts 5（all sails set 是誤傳）；Austin 無損 | 200 | CONFIRMED（當傳說講） | — |
| 24 | 流傳版四個細節＋出處「道爾 1884 年的小說，與後來的轉述」 | legend-list.data | WS、AH | 200 | CONFIRMED | — |
| 25 | 1861 年進馬賽港的畫像，船名還是 Amazon | legend-amazon-painting.data、yekh | C-Amazon、MCN/spencer（1861 年 11 月在馬賽入畫） | 200 | CONFIRMED | — |
| 26 | 加拿大新斯科舍下水，七年後改名 | legend-amazon-painting/c6gg | EB（1861 Spencer's Island、1861-05-18 下水、翌年即 1868 售 Haines 改名）；MCN/facts（美籍登記 1868-12-31） | 200 | CONFIRMED | — |
| 27 | 熱飯菜這個細節是 1884 年小說加進去的 | legend-writer/k2wi | WS 全文：只有「The boats were intact and slung upon the davits」與縫紉機上的絲線軸，沒有任何飯菜；AH：「Other romancers added… a partly consumed breakfast on the cabin table, including cups of tea that were still lukewarm」；SK 說道爾加了 meals——與原文不符，不採 | 200 | CHANGED | 熱飯菜這個細節，是一八八四年一篇小說加進去的。 → 小艇都在，是一八八四年一篇小說加的，熱飯菜更晚才有。 |
| 28 | 第一段原文 "the derelict brigantine Marie Celeste" | legend-doyle-quote.data | WS 第一段 | 200 | CONFIRMED | — |
| 29 | Cornhill Magazine，1884 年 1 月，匿名發表 | legend-doyle-quote.data.source、dqmb | WS 出版註、ACD「published anonymously」、AH（1892 年才公開作者）；SK 說筆名 W. Small，少數，不採 | 200 | CONFIRMED | — |
| 30 | 柯南道爾是福爾摩斯的作者 | dqmb | SK、ACD | 200 | CONFIRMED | — |
| 31 | 小說裡連船名都拼錯 | 6xr9 | WS、ACD、MCN/facts 1 | 200 | CONFIRMED | — |
| 32 | 這篇小說被很多人當成真的，推論從此開始 | legend-newsboy/q4ch | ACD「the readers thought it was a report of a real event」、SM07「set off waves of theorizing」 | 200 | CONFIRMED | — |
| 33 | 後來的人加了海怪、巨大章魚、百慕達三角 | legend-sea-monster/uepv | SM07（sea monsters）、AH（giant octopus）、MCN/about（squid, octopus, kraken）；百慕達的聯想：FV「nowhere near the Bermuda Triangle」、MCN/about「far, far away」 | 200 | CONFIRMED | — |
| 34 | 在葡萄牙外海被發現，離百慕達幾千公里 | legend-chart/j54f | AH（Azores 與 Portugal 中間）、HH（off the coast of Portugal）、MCN/facts 38°20'N 17°15'W；到百慕達約 4,300 公里是我算的 | 200 | CONFIRMED | — |
| 35 | 收尾問句 | legend-question/6mht | — | — | OUT OF SCOPE | — |
| 36 | 第 3 章卡片「1872 年 12 月 4 日」 | find-chapter.data.subtitle | 見 #50 | 200 | CHANGED | 1872 年 12 月 4 日 → 1872 年 12 月 4 日（船上日誌記 5 日） |
| 37 | 1872-11-07 從紐約出港往熱那亞 | find-new-york-pier/hnsv | EB、SM07、AH、HH、ACD 都寫 11-07；NEHS 11-05、MCN/facts 週報「sailed 4 November」為少數；Briggs 11-03（週日）家書說「shall leave on Tuesday」，與 5 日清關、7 日出港相容 | 200 | CONFIRMED | — |
| 38 | 1,701 桶酒精，工業用，不能喝 | find-hold-casks/55b2 | SM07「industrial alcohol」、NEHS 與 FV「denatured… undrinkable／toxic」、ACD「denatured」；SK 說是強化葡萄酒用的穀物酒精——一對四，不採，記在下方 | 200 | CONFIRMED | — |
| 39 | Briggs 37 歲、麻州 Marion 人 | find-briggs-portrait.data.caption、5imz | NEHS（37）、SM07 與 C-NYT 剪報（Marion, Mass.）；NEHS 寫 Wareham，少數 | 200 | CONFIRMED | — |
| 40 | 在海上跑了十幾年 | 5imz | NEHS「after more than 10 years sailing」 | 200 | CONFIRMED | — |
| 41 | 滴酒不沾、這艘船有他的股份 | 7pij | FV「eschewed all forms of alcoholic drink」、NEHS；MCN/briggs「bought an interest」、EB、SK（1/3）、NEHS（2/5，比例不講） | 200 | CONFIRMED | — |
| 42 | 太太莎拉、兩歲女兒蘇菲亞同行 | find-family-gangplank/w4r2 | SM07、EB、MCN/briggs | 200 | CONFIRMED | — |
| 43 | Sarah E. Briggs，1862 年結婚，到這年十年 | find-sarah-portrait.data、8trw | MCN/briggs「In 1862, Benjamin S. Briggs married Sarah E. Cobb」 | 200 | CONFIRMED | — |
| 44 | 七歲兒子亞瑟留在家上學 | find-son-at-school/u2sf | SM07、MCN/briggs | 200 | CONFIRMED | — |
| 45 | Sophia Matilda Briggs，1870-10-31 生，上船時剛滿兩歲 | find-sophia-portrait.data、66tg | MCN/briggs、SM07 | 200 | CONFIRMED | — |
| 46 | 七個船員，全船十個人 | find-crew-rope/6mmb | SM07、NEHS、SK、ACD（crew of seven）、EB（10 人）；HH 寫 eight crew、AH「eight men」把船長算進去——10 人一致，7 名船員是 10 減船長夫婦與女兒 | 200 | CONFIRMED | — |
| 47 | 11 月 25 日早上石板最後一筆 | find-slate/w9v8 | MCN/news 與 AH 8 a.m.；SM07 5 a.m.；旁白只講「早上」 | 200 | CONFIRMED | — |
| 48 | 聖瑪麗亞島外海十一公里左右 | find-island/avgx | MCN/news「eastern point… bore S.S.W., 6 miles」、AH「six miles northeast」、EB「6 nautical miles (11 km)」；方位兩說，旁白只講距離 | 200 | CONFIRMED | — |
| 49 | 之後九天沒有任何紀錄 | find-empty-ocean/ejmr | 11-25→12-04 九天；EB、SM07 用船上日誌的 12-05 算 ten days；#50 之後兩個日期都講了 | 200 | CONFIRMED | — |
| 50 | 十二月四日下午另一艘英國船看到她 | find-lookout/ympw | MCN/facts 6（12-04 下午 1–2 時，Dei Gratia 日誌海日記 12-05）；AH、HH、FV、NEHS、ACD 寫 4 日；EB、SM07、Gibraltar Chronicle 寫 5 日——依啟動說明，兩個都講 | 200 | CHANGED | 十二月四日下午，另一艘英國船看到遠處一艘船怪怪的。 → 十二月四日下午，日誌記五日，另一艘英國船看到她怪怪的。（24 單位） |
| 51 | 位置在亞速群島和葡萄牙之間 | find-position-chart/787f | AH、MCN/facts、EB（離亞速 400 浬） | 200 | CONFIRMED | — |
| 52 | Dei Gratia、船長莫爾豪斯、晚八天離開紐約 | find-morehouse/nt2k | AH（David Reed Morehouse、Nova Scotian brigantine）、SM07「left New York City eight days before him」、FV「Eight days later」 | 200 | CONFIRMED | — |
| 53 | 大副德沃帶兩個人划小艇過去，爬上船 | find-boarding/mtua | AH（Deveau、Wright 與一名水手；Deveau 與 Wright 登船） | 200 | CONFIRMED | — |
| 54 | 甲板無人、前帆被吹走、一面帆鬆脫 | find-empty-deck/t6ni | AH、MCN/facts 5 | 200 | CONFIRMED | — |
| 55 | 前艙口開著、艙底一公尺多的水 | find-open-hatch/njvf | AH（fore 與 lazaretto 艙口開、3.5 呎）、FV | 200 | CONFIRMED | — |
| 56 | 甲板上的測深桿、兩具幫浦一具拆開 | find-sounding-rod/mgrf | EB、SM07、HH | 200 | CONFIRMED | — |
| 57 | 3.5 英尺、約 1 公尺、船還能航行 | find-stats、nvhj | AH、SM07、EB（seaworthy）、MCN/news（「staunch and sea worthy」） | 200 | CONFIRMED | — |
| 58 | 1,701 桶，只有 1 桶被打開過 | find-stats、rtpc、2rum | MCN/news 1873-01-31「except one which had been started」、AH | 200 | CONFIRMED | — |
| 59 | 6 個月糧食和水 | find-stats、as24、kua2 | AH、SM07、HH | 200 | CONFIRMED | — |
| 60 | 0 人；卡片出處 Dei Gratia 證詞 1872–73 | find-stats、29ax | AH、MCN/facts | 200 | CONFIRMED | — |
| 61 | 艙裡全濕、爐子撞歪、桌上沒有吃的 | find-galley/6y3w | MCN/facts 3–4（水一兩呎深、爐子 knocked out of place、桌上 nothing to eat or drink） | 200 | CONFIRMED | — |
| 62 | 羅經櫃被撞歪、羅盤玻璃罩破 | find-binnacle/kjde | NEHS、FV | 200 | CONFIRMED | — |
| 63 | 日誌在桌上、船長的劍在、衣服掛著 | find-logbook/qwpv | AH（log book 在大副艙的桌上、slate 在主艙桌上；劍在床下鞘內；衣物掛鉤上） | 200 | CONFIRMED | — |
| 64 | 紀錄版四點（桌上沒有、唯一小艇不見、前帆吹走 3.5 呎水、儀器文件不見） | find-compare-legend-record.data.right | MCN/facts、AH | 200 | CONFIRMED | — |
| 65 | 對照卡出處「左：道爾 1884」 | find-compare-legend-record.data.source | 見 #27 | 200 | CHANGED | 左：道爾 1884；右：… → 左：道爾 1884 與後來的轉述；右：… |
| 66 | 收尾問句 | find-question/46w5 | — | — | OUT OF SCOPE | — |
| 67 | 德沃帶兩個水手把船開到直布羅陀領救難金 | court-chapter/mnce | MCN/facts 8（Lund、Anderson）、AH | 200 | CONFIRMED | — |
| 68 | 12 月 13 日早上跟在英國船後進港 | court-harbour/h8g9 | AH（Dei Gratia 12-12 晚、Mary Celeste 翌晨）、MCN/news 1872-12-13「arrived in The Bay this morning」 | 200 | CONFIRMED | — |
| 69 | 檢察總長索利弗拉德 | court-prosecutor/u7aq | SM07、HH、FV（Attorney General）、AH（queen's proctor） | 200 | CONFIRMED | — |
| 70 | 12 月 18 日開庭，懷疑謀殺 | court-bench/8vum | AH | 200 | CONFIRMED | — |
| 71 | 推論：船員偷喝酒精、酒後殺了船長和大副 | court-letter/pdk7 | THP 引 1873-01-22 信原文（信裡還有妻與女兒，旁白依內容守則省略） | 200 | CONFIRMED | — |
| 72 | 12 月 23 日驗船，潛水夫看船底 | court-diver/2ifb | MCN/news、THP（Austin、Portunato） | 200 | CONFIRMED | — |
| 73 | 船殼無傷、縫紉機油瓶直立 | court-oil-bottle/zz49 | MCN/news（Chronicle）、THP（Austin 報告：在大副艙的小架上；THP 提醒這是船到直布羅陀兩週半後看到的）——旁白說的是驗船結果，沒改 | 200 | CONFIRMED | — |
| 74 | 船頭像刀痕、劍上像沾過血 | court-sword/3sp6 | THP 引 Austin：「smeared with blood and afterwards wiped」、「sharp cutting instrument」 | 200 | CONFIRMED | — |
| 75 | 最早出處：1872 年 12 月直布羅陀的驗船報告 | court-three-questions.data.steps[0]、2ndb | THP、MCN/news（1872-12-23）；AH 說德沃 12-04 已看到劍上「faint discolorations」，但「血」的說法是 Austin 寫的 | 200 | CONFIRMED | — |
| 76 | 誰說的：檢察總長，在爭救難金的法庭上 | steps[1]、ecs7 | AH、SM07 | 200 | CONFIRMED | — |
| 77 | 化驗結果不是血；一位醫生化驗 | steps[2]、k3aq、court-chemist/rby8 | AH（chemical tests）、MCN/news 1873-03-04（「an analysis made by Dr. Patron, of this City」）、THP、NEHS；Dr. 是否醫師，來源只給頭銜，沒改 | 200 | CONFIRMED | — |
| 78 | 美國軍艦艦長說船頭痕跡是海水撕裂的木頭 | court-bow-wood/c8ms | MCN/news 1873-03-04（Shufeldt、USS Plymouth：「splinters… forced off by the action of the sea」），單一來源但是當年報紙的轉錄 | 200 | CONFIRMED | — |
| 79 | 桶查過、一桶打開、沒有喝醉鬧事的痕跡 | court-casks-checked/2rum | MCN/news、THP 引 Austin「found no wine or beer or spirits on board」 | 200 | CONFIRMED | — |
| 80 | 紐約時報 1873-02-26 轉載波士頓郵報，標題「船上的幹部，據信在海上遇害」 | court-nytimes.data、bu9q、kiap | C-NYT 全文：「A Brig's Officers Believed to Have Been Murdered at Sea. From the Boston Post. Feb. 24.」；旁白沒有引內文（內文的 17 日、236 噸與他源不合） | 200 | CONFIRMED | — |
| 81 | 德沃從熱那亞被叫回，第三次作證 | court-deveau-recalled/9i5z | THP「recalled from Genoa… cross-examined for a third time… 4 March 1873」，單一來源 | 200 | CONFIRMED | — |
| 82 | 隔年三月判救難金一千七百英鎊 | court-award/ycs4 | MCN/news 1873-03-15（「yesterday」判 £1,700）、AH（In March）；FV 寫 4-08，少數 | 200 | CONFIRMED | — |
| 83 | 大約只有船加貨估值的五分之一 | court-one-fifth/zkud | MCN/news（$5,700＋$36,943＝$42,643，「one fifth」）、FV（1/5）；SM07 投保值 $46,000 的 1/6——旁白已有「大約」 | 200 | CONFIRMED | — |
| 84 | 法庭怪莫爾豪斯讓德沃把船開去熱那亞 | court-morehouse-blamed/a52w | MCN/news（「disapprobation… allowing the first mate… to do away with the vessel」）、THP、FV | 200 | CONFIRMED | — |
| 85 | 收尾問句 | court-question/jds4 | — | — | OUT OF SCOPE | — |
| 86 | 唯一的小艇不見，一邊欄杆放下，像正常放艇 | list-davits/t3k4 | SK、AH（one boat was gone）、MCN/facts 2 | 200 | CONFIRMED | — |
| 87 | 船尾拖著一條斷掉的粗繩 | list-broken-halyard/npmj | MCN/about（main halyard 周長三吋，broken and hanging over the side）、SK（trailing in the water）；兩個都是二手 | 200 | CONFIRMED | — |
| 88 | 六分儀和天文鐘不見 | list-sextant/xakr | AH、SK、FV | 200 | CONFIRMED | — |
| 89 | 航海手冊和船籍文件不在 | list-empty-case/guwn | AH；MCN/news「No bills of lading nor manifest were found」 | 200 | CONFIRMED | — |
| 90 | 還在的：船長的劍、衣服、縫紉機、小孩的衣服 | list-child-dress/cw9n | AH 列的是 clothing、dresses、「articles of child's wearing apparel; also child's toys」、melodeon；今天開的來源沒有一個把縫紉機列為船上還在的東西（Chronicle 只提縫紉機用的油瓶、頂針、棉線軸；道爾小說裡才有縫紉機） | 200 | NOT FOUND → 換成有來源的玩具 | 船長的劍、衣服、縫紉機，小孩的衣服都在 → 船長的劍、衣服、玩具，小孩的衣服都在 |
| 91 | 六個月食物和水、1,701 桶貨都在 | list-stores/kua2 | AH、SM07 | 200 | CONFIRMED | — |
| 92 | 對照卡「衣服、小孩衣物、縫紉機」 | list-compare.data.right.points[3] | 見 #90 | 200 | NOT FOUND → 換 | 衣服、小孩衣物、縫紉機 → 衣服、小孩衣物、玩具 |
| 93 | 對照卡其餘項目與結語 | list-compare.data | AH、SM07 | 200 | CONFIRMED | — |
| 94 | 「我的看法是，匆忙但有秩序地離開」 | list-captain-door/dxy5 | 標成意見；與 brief 大綱第 4 章一致 | — | OUT OF SCOPE（意見） | — |
| 95 | 帶走找路的工具，留下吃穿和貨 | list-forecastle/xmte | AH、SK | 200 | CONFIRMED | — |
| 96 | 老船長帶著太太和兩歲女兒 | list-question/npuj | SM07、MCN/briggs | 200 | CONFIRMED | — |
| 97 | 至少七種說法 | theories-chapter/kp6j | SM07、AH、SK、EB 合計至少八種 | 200 | CONFIRMED | — |
| 98 | 海怪、百慕達出處是小說與轉述，紀錄裡一個字都沒有 | gb9h、7tyn、theories-table row 1 | MCN/news（Austin 與 Chronicle）、SM07、AH、MCN/about | 200 | CONFIRMED | — |
| 99 | 海盜、叛變：貨與個人物品都在，沒有打鬥痕跡 | theories-pirate-sail/zemg、table row 2 col 3 | EB、MCN/news（Shufeldt「no evidence of violence」） | 200 | CONFIRMED | — |
| 100 | 海盜、叛變是「1872 年的檢察總長」提的 | theories-table row 2 col 2 | 叛變殺人：Solly-Flood（AH 12-18、THP 信）；海盜：波士頓郵報 1873-02-24（C-NYT「seized by pirates」）、SK「some believed piracy」——檢察總長沒有提海盜 | 200 | CHANGED | 1872 年的檢察總長 → 當年的檢察總長與報紙 |
| 101 | 保險詐騙：船長持股、划不來 | theories-insurance/7vne、table row 3 col 3 | SK、NEHS、MCN/briggs、EB | 200 | CONFIRMED | — |
| 102 | 保險詐騙是「後來的猜測」 | theories-table row 3 col 2 | SK「Early theories quickly focused on… insurance fraud」、HH「Insurance fraud and foul play were immediately theorised」 | 200 | CHANGED | 後來的猜測 → 當年就有的猜測 |
| 103 | 海底地震、水龍捲：船和貨無傷 | theories-waterspout/6jaz、table row 4 | SK（David Williams 的 seaquake）、MCN/news（勘驗） | 200 | CONFIRMED | — |
| 104 | 酒精蒸氣說的內容 | theories-match/cr29、table row 5 col 1 | AH（Cobb）、SK | 200 | CONFIRMED | — |
| 105 | 酒精蒸氣說「1920 年代起」 | theories-table row 5 col 2 | AH：當年 Morehouse 相信氣體「rumble menacingly」、船主 J. H. Winchester 主張自燃掀開前艙蓋；Cobb 是後來寫成完整版本；今天開的來源沒有一個給 1920 年代這個年份 | 200 | CHANGED | 1920 年代起 → 當年的船主，後來的研究者 |
| 106 | 主艙口蓋好、沒人聞到氣味 | theories-main-hatch/bcxz、table row 5 col 3 | SM07、FV（main hatch tightly covered） | 200 | CONFIRMED | — |
| 107 | 天文鐘不準、船長以為在別處 | theories-chronometer-box/avqr | SM07（120 哩） | 200 | CONFIRMED | — |
| 108 | 幫浦被前一趟的煤灰塞住 | theories-pump-coal/ujze | SM07 | 200 | CONFIRMED | — |
| 109 | 誤判進水是「2007 年的紀錄片調查」提的 | theories-table row 6 col 2 | MCN/news 1873-03-04：Shufeldt「leaked so much as to seriously alarm the master」已是同一個骨幹；MacGregor 2007 補了天文鐘與煤灰 | 200 | CHANGED | 2007 年的紀錄片調查 → 1873 年的美艦艦長，2007 年的紀錄片 |
| 110 | 誤判進水解釋不了：小艇沒被找到、為何不直接靠岸 | table row 6 col 3、tycg | SM07（當時看得到陸地）、EB（小艇出事）、MCN/news（not a trace） | 200 | CONFIRMED | — |
| 111 | 表格出處：勘驗報告 1872-12-23 | theories-table.data.source | MCN/news、THP | 200 | CONFIRMED | — |
| 112 | 1870 到 1890 年之間的版畫，繪者不明 | theories-engraving.data | C-Engraving | 200 | CONFIRMED | — |
| 113 | 剩下最站得住的是最後兩個／哪一個更站得住 | 2w53、pdv5 | 敘事判斷 | — | OUT OF SCOPE | — |
| 114 | 線索在熱那亞卸貨時出現 | answer-chapter/s6yd、answer-nine-casks.data.kicker | MCN/about「unloaded in Genoa」、SM07（沒寫地點）；SK 寫 Gibraltar——少數，且 research.md §8.3 允許寫熱那亞 | 200 | CONFIRMED | — |
| 115 | 1,701 桶裡九桶是空的 | 3wc8、answer-nine-casks.data | SM07、SK、MCN/about、MCN/barrel | 200 | CONFIRMED | — |
| 116 | 九桶是紅橡木，其餘白橡木 | yft6、answer-nine-casks.data.sub | SM07、SK、MCN/barrel | 200 | CONFIRMED | — |
| 117 | 紅橡木孔隙大、會滲漏 | answer-seeping-cask/f78g | SM07、SK | 200 | CONFIRMED | — |
| 118 | 目前最站得住：船長察覺不對勁、怕出事 | answer-captain-alert/qa9h | EB（「A more likely scenario」）、SK、AH；標成「目前最站得住的版本」 | 200 | CONFIRMED | — |
| 119 | 全員上小艇，用繩子拖在船後等 | answer-towed-boat/kzyk | AH（Cobb 假說）、SK | 200 | CONFIRMED | — |
| 120 | 繩子斷了 | answer-rope-parts/2gch | AH「the straining line parted」、SK | 200 | CONFIRMED | — |
| 121 | 帆還張著船繼續走，小艇越離越遠 | answer-sailing-away/9wsg | AH、SK | 200 | CONFIRMED | — |
| 122 | 2007 年用氣象資料回推：那九天她是自己走的 | answer-drift-study/nhz6 | SM07（ICOADS；「it basically just sailed itself」；SM07 以 12-05 算 ten days） | 200 | CONFIRMED | — |
| 123 | 暫時下船為何帶走六分儀和文件 | answer-empty-satchel/bwmh | AH、SK | 200 | CONFIRMED | — |
| 124 | 小艇和十個人從來沒有被找到 | answer-never-found/4f9b | MCN/news 1873-01-31「not a word has been heard, nor a trace discovered」、SK | 200 | CONFIRMED | — |
| 125 | 1885 年新船長為詐保把她開上海地的礁石 | answer-reef-1885/6azw | EB、FV（1885-01-03 Rochelois Bank）、SL | 200 | CONFIRMED | — |
| 126 | 船沒沉、騙局拆穿、陪審團七比五、三個月後過世 | answer-boston-jury/u2ek | EB（failed to sink）、SL（1885 年 7 月審判、deadlocked 7-5、「three months after his trial」） | 200 | CONFIRMED | — |
| 127 | 「不是消失，是離開之後回不去」「未結」「還解釋不了小艇和儀器」 | answer-big.data、nrsd | 敘事收攏，標成未結；與 brief 的「觀眾看完能做到的事 3」一致 | — | CONFIRMED（沒有宣稱定論） | — |
| 128 | 10 個人、1 艘小艇、9 個空桶；沒有定論 | outro.data、mnjn | 見 #46、#86、#115 | 200 | CONFIRMED | — |
| 129 | 下一份檔案：51 區 | outro、txtu | 系列安排 | — | OUT OF SCOPE | — |
| 130 | sources[] 18 筆 checked_on 2026-10-10 | sources | 全部當天開過，200 | 200 | CONFIRMED | — |

## 摘要

- 查了 130 條（合併重複出現的同一主張；原始抽取 263 條）：CONFIRMED 112、CHANGED 9（對應 8 個事實）、NOT FOUND 2（縫紉機，旁白與卡片各一，換成有來源的玩具）、OUT OF SCOPE 7。
- 改的 8 個事實：(1) 發現日期——旁白 ympw 與第 3 章卡片加上「日誌記五日」；(2) 熱飯菜不是道爾 1884 加的，是更後來的轉述——k2wi 改寫、對照卡出處補「與後來的轉述」、claims c3／c8 改；(3) 表格「海盜、叛變」的提出者——檢察總長只提叛變殺人，海盜是 1873 年的報紙；(4) 表格「保險詐騙」——當年就有，不是後來；(5) 表格「酒精蒸氣」——當年的船主與莫爾豪斯就說過，不是 1920 年代起；(6) 表格「誤判進水」——1873 年 Shufeldt 已提，2007 年補證據；(7) 縫紉機→玩具（cw9n、list-compare）；(8) 說明欄「估值五分之一」加「大約」。沒有數字在卡片上改動，所以沒有 `say`／`say_for` 要補。
- 會過期的事實：沒有。看到的頁面日期：Britannica「Last updated Sep. 18, 2026」、Smithsonian 2007 年 11 月、The History Press 2023-01-05、American Heritage 1981 年 2／3 月、Skeptoid 2011-12-20、Slate 2011-12。
- 意見：dxy5「我的看法是，這張清單像是匆忙，但有秩序地離開」與 qa9h「目前最站得住的版本」都標成意見或主流說法，與 brief 的站主觀點（只講紀錄裡有的、傳說標明、沒有定論就說沒有定論）一致；沒有不符。
- 聽眾檢查：118 句都在 24 單位以內（最長 24：ympw、原稿已有的幾句）；沒有超過 40 字的句子；沒有「經查證」「根據官方文件」「本影片」；旁白裡唯一的拉丁字 Dei Gratia 在 lexicon.json 裡（德伊 格拉提亞，站主要試聽）；旁白沒有括號或網址；每個 reveal 都在介紹該項的句子上，沒有提前。
- 內容守則：傳說都標成後來加的；沒有宣稱定論；沒有編造布里格斯一家的對話或心理（qa9h 的「察覺不對勁」是假說的敘述，標在「目前最站得住的版本」底下）；沒有血腥。
- 照片：六張的說明與出處都對得上 Commons 頁；1873 年剪報只用了標題，標題與 Commons 全文一致，內文沒有引。
- Lint：`node tools/video/cli.mjs lint --slug curio-h01` 改後 0 錯誤、1 個原本就有的警告（outro 三句共用一個畫面 14.4 秒）。估計 11.0 分鐘、118 句、2,302 單位。
- 懷疑但沒改的：
  - 55b2「工業用的，不能喝」：SM07、NEHS、FV、ACD 說 industrial／denatured，Skeptoid 說是強化葡萄酒用的穀物酒精；一對四，保留，但第二輪可再看。
  - 6mmb「七個船員」：History Hit 寫 eight crew；10 人一致，7 是減出來的，保留。
  - hnsv「十一月七日」：NEHS 11-05、maryceleste.net 週報 11-04（疑為清關日），五個來源寫 11-07，保留。
  - rby8「一位醫生化驗」：來源只給「Dr. Patron」的頭銜，是否醫師沒看到，保留。
  - 熱那亞卸貨發現九個空桶：Skeptoid 寫 Gibraltar，其餘寫熱那亞或不寫地點，保留熱那亞。
  - zz49 縫紉機油瓶：Austin 原文是在大副艙的小架上、船到港兩週半後看到的；旁白只說驗船結果，沒改；插圖 prompt（court-oil-bottle）畫在縫紉機上，是 Chronicle 的版本。
  - list-child-dress 的插圖 prompt 畫了縫紉機；旁白已改成玩具，prompt 是畫面不是主張，留給撰稿方決定要不要改。
  - legend-doyle-quote：Skeptoid 說筆名 W. Small，ACD、AH、maryceleste.net 都說匿名，採匿名。
  - 第 2 章的 b7js「帆還張著」當傳說講；實際發現時確有兩三面帆張著（AH），傳說版是「全部帆都張著」，旁白的講法兩邊都讀得通。
  - j54f「葡萄牙外海」：位置離葡萄牙本土約 1,000 公里，離亞速（葡屬）740 公里；AH 說在兩者中間，HH 說 off the coast of Portugal，保留。
- 程序註記：中途誤跑了一次唯讀的 `git diff --stat`（只看 video.json 有沒有被追蹤），沒有任何 git 寫入；啟動說明要求不跑 git，記在這裡。
- **第二輪：需要**（這一輪改了 8 個事實，超過 3 個）。第二輪請換人，重查上面 9 條 CHANGED 與 2 條 NOT FOUND，再隨機抽三分之一的 CONFIRMED。
