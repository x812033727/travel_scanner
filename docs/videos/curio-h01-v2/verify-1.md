# curio-h01-v2 查核第一輪

- 查核 2026-10-13，Claude Opus 5（查核代理）。**我不是撰稿的那一個**，也不是第一版兩輪查核的任何一個；
  這一版的 `video.json`、`claims.md`、`brief.md`、`NOTES.md` 我一個字都沒有動，下面每一條要改的
  都寫成「行 id ＋現在的字＋應該變成的字」，交給別人去改。
- 方法：先把 `video.json` 抽成 **270 條**清單（140 句旁白、28 個卡片欄位、7 個章名、1 個標題、
  1 個說明欄、10 個標籤、5 個縮圖欄位、15 個 `youtube` 設定／`loops` 欄位、60 個 `sources` 欄位；
  `say`／`say_for` 全稿 0 個，`assets[]` 與 `characters[]` 是空的，所以沒有照片主張要查），
  存在 `<scratch>\verify-h01\claims-list.txt`，抽取腳本 `extract.mjs`、場景對主張的比對腳本 `map.mjs`
  都在同一個目錄。然後把這一版 `claims.md` 的 c1–c52 逐條對到場景 id（`map.mjs`），再把
  **第一版 `claims.md`／`research.md`／`verify-1.md`／`verify-2.md` 列的每一個網址**當天用 curl 重開
  （User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.3 秒，
  去掉標籤與註解後讀全文）。**沒有用網路搜尋（0 次）**：來源都已經在檔案裡指名了。
- 這一版是重講，不是重查，所以重點放在「同一個事實換了字之後有沒有變強」。為此我把
  第一版 `video.json` 的對應句子全部調出來並排讀（`legend-writer/k2wi`、`court-letter/pdk7`、
  `find-stats`、`theories-table`、`answer-nine-casks`、`find-lookout/ympw`、`outro` 等），
  凡是字不一樣的、`claims.md` 標過爭議的、以及**每一個數字與日期**，都回到一手或最權威的那一頁重讀：
  maryceleste.net 轉錄的 **Austin 勘驗報告全文（1872-12-23）**、**Dr. Patron 化驗報告全文（1873-01-30）**、
  **Gibraltar Chronicle 1872-12-13／1873-01-31／03-04／03-15**、**maryceleste.net/facts 的逐條更正**、
  The History Press 引的 **Solly-Flood 1873-01-22 信原文**、Wikisource 的**道爾 1884 全文**、
  Commons 的 **1873 紐約時報剪報全文**；其次 Smithsonian Magazine 2007、Britannica、American Heritage 1981。
  Skeptoid、History Hit、Fishermen's Voice、NEHS、Slate 只能佐證。Wikipedia 沒有用。
- 判定沿用第一版的四個：**CONFIRMED** 看到了／**CHANGED** 要改／**NOT FOUND** 沒看到，拿掉或換掉／
  **OUT OF SCOPE** 風格、問句、系列安排與標成意見的句子，不動。每一條要改的都附了
  `spokenUnits`（`tools/video/core/timeline.mjs` 的算法，CJK 一字一單位），全部在 24 單位以內。
- 程序：沒有跑任何 git，沒有跑任何影片階段（`lint` 也沒跑，啟動說明不准），沒有花任何提供者的錢。

## 當天（2026-10-13）開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| SM07 | https://www.smithsonianmag.com/history/abandoned-ship-the-mary-celeste-174488104/ | 200 |
| SM07-ARC | https://web.archive.org/web/20260920054456/https://www.smithsonianmag.com/history/abandoned-ship-the-mary-celeste-174488104/ （`sources[0]` 用的快照） | 200 |
| EB | https://www.britannica.com/topic/Mary-Celeste | 200 |
| EB-ARC | https://web.archive.org/web/20260819222317/https://www.britannica.com/topic/Mary-Celeste （`sources[1]` 用的快照） | 200 |
| AH | https://www.americanheritage.com/mystery-mary-celeste | 200 |
| MCN/facts | https://www.maryceleste.net/facts.htm | 200 |
| MCN/news | https://www.maryceleste.net/news.htm （Gibraltar Chronicle 1872-12-13、1873-01-31、03-04、03-15） | 200 |
| MCN/survey | https://www.maryceleste.net/survey.htm （Austin 勘驗報告全文） | 200 |
| MCN/doctor | https://www.maryceleste.net/doctor.htm （Patron 化驗報告全文） | 200 |
| MCN/about | https://www.maryceleste.net/about.htm | 200 |
| MCN/briggs | https://www.maryceleste.net/briggs.htm | 200 |
| MCN/barrel | https://www.maryceleste.net/barrel.htm | 200（內容是框架頁，文字在 about.htm） |
| MCN/spencer | https://www.maryceleste.net/spencer.htm | 200 |
| MCN/genoa | https://www.maryceleste.net/genoa.htm （想查熱那亞卸貨的日期） | 200，但只回導覽文字，**沒有可用內文** |
| THP | https://thehistorypress.co.uk/article/the-ongoing-mystery-of-the-mary-celeste/ | 200 |
| HH | https://www.historyhit.com/ghost-ship-what-happened-to-the-mary-celeste/ | 200 |
| FV | https://fishermensvoice.com/archives/201711TheMysteriousCaseOfTheMaryCeleste.html | 200 |
| NEHS | https://newenglandhistoricalsociety.com/mysterious-disappearance-mary-celeste/ | 200 |
| SL | https://www.slate.com/articles/life/culturebox/2011/12/the_mary_celeste_the_unluckiest_ship_to_ever_sail_the_seven_seas_.html | 200 |
| SK | https://skeptoid.com/episodes/289 | 200 |
| WS | https://en.wikisource.org/wiki/J._Habakuk_Jephson%27s_Statement | 200 |
| ACD | https://www.arthur-conan-doyle.com/wiki/Mary_Celeste | 200 |
| C-NYT | https://commons.wikimedia.org/wiki/File:Mary_Celeste_NYTimes_1873February26.png | 200 |

`sources[0]`、`sources[1]` 用的是 web.archive.org 的快照，`claims.md` 引的是原站網址；兩邊我都開了，
快照在我查的每一個字串上（「3 feet (1 meter)」「November 7, 1872」「Richard W. Haines」「10 people」
「chronometer」）與現在的頁面一字不差，**快照支持得起那些主張**（註記見摘要）。

## 主張表（c1–c52）

| # | 主張 | 位置（行 id／欄位） | 來源 | HTTP | 判定 | 要改的 |
|---|---|---|---|---|---|---|
| c1 | 被發現時船仍在航行、部分帆張著 | opening-swell/mc1a、crooked-sails/mc1c、still-sailing/mc1h、sails-away/mc7l | MCN/facts 第 5 條（只有 lower topsail、jib、fore-topmast staysail 張著，前帆與上前中帆被吹走；「all sails set」列為誤傳）、AH「beating northwest under very short canvas」 | 200 | CONFIRMED | — |
| c2 | 船上十個人，一個都不在 | ten-aboard 卡＋mc1d、the-question/mc1l、outro | EB「the 10 people aboard」、SM07 | 200 | CONFIRMED | — |
| c3 | 「小艇都在」出自道爾 1884；熱飯菜不在道爾全文裡，是別的轉述加的；**先後沒有來源，所以旁白不講先後** | hot-meal-legend/mc4m、who-added/mc4n、remember-meal/mc5g、added-later/**mc5h**、warm-tea/mc5j、no-year-marked/mc5k、**youtube.description** | WS 全文：Gazette 段落有「The boats were intact and slung upon the davits」，全篇沒有任何艙桌上的飯菜（breakfast 只出現在敘事者自己的航海日記）；AH「Other romancers added… a partly consumed breakfast on the cabin table, including cups of tea that were still lukewarm」**沒有年份**；MCN/facts 第 3 條只寫 erroneously reported | 200 | **CHANGED ×2** | R1（說明欄把熱飯菜算成 1884 小說寫的）、R2（mc5h 的「後來」） |
| c4 | 艙底約 3.5 英尺（一公尺多）的水，船仍可航行 | open-hatch/mc1g | AH、SM07「Three and a half feet」、EB「more than 3 feet (1 meter)… seaworthy」 | 200 | CONFIRMED | — |
| c5 | 艙內濕透、廚房爐灶被撞離原位、桌上沒有任何吃喝 | galley-stove/**mc3f**、nothing-on-table/mc5i | MCN/facts 第 4 條「The galley stove was knocked out of place. …The water in the galley was a foot or two deep.」，**出處欄寫的是 Testimony before Vice-Admiralty Court, Gibraltar, 1872（上船那天的證詞）**；Austin 1872-12-23 報告第 21 段反而寫「The stove and cooking utensils were in good order and exhibited no appearance of having suffered from exposure to water」 | 200 | **CHANGED**（事實成立，出處被挪位） | R8 |
| c6 | 1861 年新斯科舍 Spencer's Island 建造，原名 Amazon，05-18 下水 | not-her-name/mc5r、amazon-launch/mc5s | EB「built in 1861 at Spencer's Island, Nova Scotia… launched on May 18, 1861… named the Amazon」 | 200 | CONFIRMED | — |
| c7 | 1868 年售予美國人後改名（下水後七年） | renamed-1868/mc5t | EB「The following year the Amazon was sold to American Richard W. Haines, who renamed it the Mary Celeste」（前句是 1867-10 的 Cow Bay 擱淺） | 200 | CONFIRMED | — |
| c8 | 道爾 1884-01 在 Cornhill 匿名發表，拼成 Marie，寫小艇都在、船被拖進港；讀者當成真的 | magazine-office/mc5a、anonymous-author/mc5b、misspelled-name/mc5c、boats-on-davits/mc5d、not-in-records/mc5e、taken-as-real/mc5f | ACD「In january 1884… published anonymously in The Cornhill Magazine… he spelled the vessel's name as Marie Celeste… the readers thought it was a report of a real event」；WS 第一段「having in tow the derelict brigantine Marie Celeste」 | 200 | CONFIRMED | — |
| c9 | 柯南道爾是福爾摩斯的作者 | anonymous-author/mc5b | ACD（含 Holmes 專節） | 200 | CONFIRMED | — |
| c10 | 海怪、巨大章魚、百慕達三角是後人加的，法庭紀錄裡沒有 | sea-monster/**mc5m**、bermuda-triangle/mc5n、monster-triangle/mc5q | 「紀錄裡沒有」：Austin 全文與 Chronicle 都沒有；百慕達：FV「nowhere near the Bermuda Triangle」、MCN/about「far, far away」。但**章魚的年代有衝突**：AH 把 giant octopus 列在 Doyle 之後的「Authors variously conjectured」，MCN/about 卻寫「**A popular theory at the time** was that a giant squid, octopus, kraken…」 | 200 | **CHANGED**（次要） | R15 |
| c11 | 位置在亞速與葡萄牙之間；離百慕達數千公里 | off-portugal/mc5o、thousands-km/mc5p | AH「midway between the Azores and Portugal」、HH「near to the Azores… off the coast of Portugal」、MCN/facts 第 15 條 38°20'N 17°15'W（到百慕達約 4,300 公里是算出來的） | 200 | CONFIRMED | — |
| c12 | 1872-11-07 自紐約啟航，目的地熱那亞 | family-gangplank/**mc2m**、seven-crew/mc2n | EB「On November 7, 1872, the Mary Celeste **set sail** from New York City」、HH「set sail from New York on 7 November 1872」、SM07；MCN/facts 第 14 條另記 Maritime Register 的「sailed 4 November」（少數） | 200 | **CHANGED**（次要：啟航日被寫成上船日） | R17 |
| c13 | 貨是 1,701 桶工業用酒精（**不能喝**） | cargo-stats 卡＋mc2o／**mc2p**、still-sailing/mc1h、remember-casks/mc7b | SM07「1,701 barrels of industrial alcohol」、NEHS「denatured alcohol, which is **undrinkable**」、FV「**toxic**, denatured alcohol」、ACD denatured；反方：SK「1,701 wooden barrels of **pure grain alcohol**, intended to fortify cheap Italian wines」、MCN/about「the alcohol carried was of a strength and type that would **not be palatable** to drink… 'denatured alcohol' this is clearly nonsense」 | 200 | **CHANGED**（「會死人」沒有來源，而且兩個來源說它可以喝） | R7 |
| c14 | Briggs 37 歲、麻州 Marion 人、在海上十幾年 | briggs-portrait/mc2j、bought-share/mc2k | NEHS「Captain Briggs, then 37… after more than 10 years sailing」、SM07「hometown of Marion, Massachusetts」、C-NYT「of Marion, Mass.」 | 200 | CONFIRMED | — |
| c15 | 不喝酒；買了這艘船的股份（比例不講） | teetotal/mc2q、bought-share/mc2k、remember-share/mc6i、he-pays/mc6j | FV「eschewed all forms of alcoholic drink」、NEHS「not fond of drinking」、MCN/briggs「1872, Capt. Briggs bought an interest in the Brig Mary Celeste」、SK「one-third owner」 | 200 | CONFIRMED | — |
| c16 | 妻 Sarah、兩歲女兒 Sophia 同行 | family-gangplank/mc2m | MCN/briggs「On October 31, 1870, Their daughter Sophia M. was born」、SM07、EB「his wife, and their two-year-old daughter」 | 200 | CONFIRMED | — |
| c17 | 船員 7 人，全船 10 人 | seven-crew/mc2n | SK「plus seven sailors」、NEHS「handpicked his crew of seven」、SM07、EB（10 人） | 200 | CONFIRMED | — |
| c18 | 石板最後一筆 11-25 早上，聖瑪麗亞島外約 11 公里 | last-slate/mc3r、santa-maria/mc3s | AH「at 8 A.M., November 25, as six miles northeast of Santa Maria」、MCN/facts 第 15 條「Eastern point of St. Mary's bore 6 miles SSW」、EB「6 nautical miles (11 km)」（時刻與方位兩說，旁白只講「早上」與距離） | 200 | CONFIRMED | — |
| c19 | 12-04 下午被發現（日誌記 5 日）；距最後一筆九天 | opening-swell/mc1a、nine-days-blank/mc3t、four-or-five/mc3v | **MCN/facts 第 6 條**：「The vessel was found on **4 December between 1:00 and 2:00 P.M.**… the entry on the Dei Gratia's log was therefore dated 5, December, sea-time」，並把「found on 5 December」列為誤傳；EB、SM07 用 5 日。兩個日期旁白都講（mc3v） | 200 | CONFIRMED | — |
| c20 | Dei Gratia 是英屬（新斯科舍）雙桅帆船，船長 Morehouse | lookout-glass/**mc1b**、dei-gratia/mc2b | AH「the Nova Scotian brigantine Dei Gratia… her master, David Reed Morehouse, sighted a sailing ship… **Through a glass** he perceived」、HH「British ship Dei Gratia」；FV 寫「the **helmsman** spied a vessel」 | 200 | **CHANGED**（次要：沒有來源有「瞭望手」） | R16 |
| c21 | 大副 Deveau 與兩人登船；之後帶兩名水手把船開到直布羅陀 | row-across/mc1e、decide-sail/mc2a、three-men/mc2c | AH「sent first mate Oliver Deveau, with second mate John Wright and a seaman」「Morehouse… detailed two seamen to go with the mate」、MCN/facts 第 8 條（Lund、Anderson） | 200 | CONFIRMED（mc2a 的「他決定」見摘要） | — |
| c22 | 甲板無人；只剩少數帆張著 | crooked-sails/mc1c、empty-wheel/mc1f | MCN/facts 第 5 條、AH「unable to make out any people」 | 200 | CONFIRMED | — |
| c23 | 前艙口開著，主艙口蓋好 | open-hatch/mc1g、main-hatch-closed/mc6c | SK「the forehatch… and the lazarette hatch had both been removed and were stowed」、AH、SM07「the boarding party found the main hatch secured」、FV | 200 | CONFIRMED | — |
| c24 | 測深桿留在甲板上；兩具幫浦之一被拆開 | sounding-rod/mc1i、remember-rod/mc6r、pump-apart/mc6s | SM07「one of its two pumps had been disassembled」、Austin 第 49–50 段（拆了一具幫浦的閥好把測深器放進井裡，測深器就在旁邊）、EB | 200 | CONFIRMED | — |
| c25 | 1,701 桶無人動過，只有一桶被打開 | cargo-stats 卡（含出處「直布羅陀勘驗報告 1872-12-23」）、casks-counted/mc7d | Chronicle 1873-01-31 轉的勘驗結果第 1 點：「barrels marked as containing alcohol, all of which were well stowed and in good order and condition, **except one which had been started**」；AH「**A survey of the 1,701 barrels** of alcohol… showed that none had been tampered with」 | 200 | CONFIRMED（卡片出處成立：1,701 與「一桶被動過」都掛在那次勘驗上） | — |
| c26 | 不見的：天文鐘、六分儀、航海手冊、船籍證；還在的：日誌、床下鞘內的劍、衣物、小孩衣物與玩具、六個月糧水 | surveyor-list/mc3a、sextant-missing/mc3i、find-position/mc3j、papers-gone/mc3k、more-remained/mc3l、clothes-toys/mc3m、**still-aboard-stats 卡**＋mc3n、took-navigation/mc3q、sword-under-bunk/mc3w、holes-remain/mc7q、why-take-tools/mc7r | AH 一段全中：「The captain's chronometer and sextant, the navigation book, and the ship's register were missing, but the log book lay on the desk in the mate's cabin… dresses… 'articles of child's wearing apparel; also child's toys.'… Under the bed Deveau found a sheathed sword」「**The ship's stores contained provisions for six months** and ample drinking water」；SM07「a six-month supply of food and water」。**Austin 的報告裡沒有任何「六個月」的數量**（第 59 段只寫「barrels of stores and other provisions in good order」） | 200 | **CHANGED**（卡片出處掛錯人） | R10 |
| c27 | 羅經櫃被撞、羅盤玻璃破 | binnacle-knocked/**mc3g**、orderly-leaving/mc3p | NEHS「The ship's binnacle… suffered damage – its glass cover broken」、FV「binnacle broken with the glass shattered」（兩者講的都是 12-04 發現時）；Austin 第 52 段「Both these panes of glass were cracked perpendicularly and **apparently from the heat of the lamp only**」、第 54 段「**The binnacle itself did not appear to have sustained any damage**」 | 200 | **CHANGED**（事實成立，出處被挪位） | R9 |
| c28 | Dei Gratia 12-12 抵港，Mary Celeste 翌晨 | gibraltar-rock/mc2d | AH「The Dei Gratia reached Gibraltar on the evening of December 12, and the Mary Celeste the following morning」、Chronicle 1872-12-13、THP「held up at Gibraltar for eleven days, since 12 December」 | 200 | CONFIRMED | — |
| c29 | 副海事法院 12-18 開庭；檢察總長 Solly-Flood 懷疑有罪案 | salvage-money/mc2e、court-opens/mc2f、doesnt-believe/mc2g | AH「On December 18 the vice-admiralty court met at Gibraltar to consider Captain Morehouse's claim for a salvage award. The queen's proctor… promptly convinced himself」、SM07、Austin 第 1 段「H. M's Advocate General… Proctor for the Queen」 | 200 | CONFIRMED（「五天後」＝12-13→12-18） | — |
| c30 | Solly-Flood 的推論：船員偷喝酒精、酒後殺了船長（1873-01-22 信） | drunk-theory/mc2h、kill-captain/**mc2i** | THP 引信原文：「the Crew got at the alcohol and in the fury of drunkenness murdered the Master… and the Chief Mate – that they then damaged the bows… and that they did sometime between the 25th November and the 5th December **escape on board some vessel** bound for some north or South American port or the West Indies」。**信裡逃走的方式是「搭上別的船」，不是划走小艇**（AH 的摘要寫「escaped in the boat」，但 c30 只引 THP） | 200 | **CHANGED** | R6 |
| c31 | 12-23 勘驗：船殼無損、沒遇過特別惡劣天氣、縫紉機油瓶直立 | surveyor-list/mc3a、surveyor-diver/mc3b、hull-sound/mc3c、no-rough-weather/mc3d、oil-bottle/mc3e | Chronicle 1873-01-31 第 3 點「she could not have encountered any seriously heavy weather. **The whole of the hull, masts, and yards were in good condition**」；Austin 第 4 段同；第 30 段「on a little bracket in which I found a small phial of oil for a sewing machine in its proper perpendicular position, a reel of cotton… and a thimble」；潛水夫 Ricardo Portunato 見 Chronicle | 200 | CONFIRMED（「桅杆也好好的」有來源） | — |
| c32 | 船艏兩側「刀痕」；劍「像被血抹過又擦掉」 | bow-cuts/mc3h、sword-smear/mc3x、send-to-test/mc3y | THP 引 Austin：「apparently done by a sharp cutting instrument」、「it appeared to me as if it had been smeared with blood and afterwards wiped」（兩句都是 Austin 的用語，旁白用「像」保留了） | 200 | CONFIRMED | — |
| c33 | 化驗（Dr. J. Patron，1873-01-30，簽 M.D.）證明不是血 | not-blood/mc4a、doctor-signed/mc4b | MCN/doctor 全文：「Gibraltar, 30th January 1873」…「there is no blood either in the stains observed on the deck…」，署名「(Sig'd) J. PATRON / M.D.」 | 200 | CONFIRMED | — |
| c34 | 美艦 Plymouth 艦長 Shufeldt 1873-03-04：船被「無充分理由」棄置；艏痕是海水撕裂的 | what-about-bow/mc4c、sea-tore-wood/**mc4d**、without-cause/mc6n／mc6o | Chronicle **1873-03-04**：「Captain Shufeldt, with everyone who has examined the ship, is of opinion that she was abandoned by the master and crew **without sufficient reason**, probably in a moment of panic」「it amounts merely to splinters in the bending of the planks, which were afterwards **forced off by the action of the sea**」 | 200 | **CHANGED**（事實對，間隔算錯） | R4 |
| c35 | 紐約時報 1873-02-26 轉載波士頓郵報的標題 | news-crossed/mc4g、headline-murdered/mc4h | C-NYT 全文「A Brig's Officers Believed to Have Been Murdered at Sea. From the Boston Post. Feb. 24.」 | 200 | CONFIRMED（旁白只用標題，內文的 11-17、236 噸沒有引） | — |
| c36 | Deveau 從熱那亞被召回，1873-03-04 第三次受訊 | deveau-recalled/mc4f | THP「Oliver Deveau himself was later recalled from Genoa to be cross-examined for a third time in the court, on 4 March 1873」（單一來源） | 200 | CONFIRMED | — |
| c37 | 1873-03 判 £1,700；估值 $5,700＋$36,943＝$42,643，約五分之一 | award-stats 卡＋mc4i／mc4j | Chronicle 1873-03-15：「the sum of £1,700」「The Mary Celeste was valued at $5,700, and her cargo at $36,943, total $42,643, so that the award may be set down as **one fifth**」；SM07 另說投保值 $46,000 的六分之一（旁白已有「大約」） | 200 | CONFIRMED | — |
| c38 | 法院批評 Morehouse 讓 Deveau 把 Dei Gratia 開去熱那亞 | morehouse-blamed/mc4k | Chronicle 1873-03-15「express the disapprobation of the Court as to the conduct of the…」 | 200 | CONFIRMED | — |
| c39 | 唯一的小艇不見；一側欄杆放下，像正常放艇 | empty-davits/mc1j、rail-lowered/mc3o | MCN/facts 第 2 條「no boat was found on board」、SK「the railings on one side of the ship had been lowered indicating that the yawl had been launched normally」 | 200 | CONFIRMED | — |
| c40 | 約三吋周長的主升降索斷裂、拖在船外 | trailing-rope/mc1k、remember-rope/mc7i、towed-behind/mc7j、rope-parts/mc7k | MCN/about「the main halyard, a stout rope three inches in circumference, was found broken and hanging over the side」、SK「the main peak halyard, the stoutest line on the ship… found cleated off and **trailing in the water behind the ship**」 | 200 | CONFIRMED（「船尾」有 SK 的 behind the ship） | — |
| c41 | 沒有暴力痕跡；海盜說出自當年的報紙；詐保當年就有人猜；Briggs 自己持股 | pirates-mutiny/mc6f、nothing-taken/mc6g、insurance-claim/mc6h、remember-share/mc6i、he-pays/mc6j | C-NYT「was **seized by pirates**」（Boston Post 1873-02-24）、Chronicle 03-04「no evidence of violence about the decks or in the cabins」、SK「Early theories quickly focused on… insurance fraud」、HH「immediately theorised」 | 200 | CONFIRMED | — |
| c42 | 海底地震（David Williams）與水龍捲：船與貨無損，純假設 | quake-waterspout/mc6k、no-damage/mc6l／mc6m | SK「**Since then**, even more suggestions have come from the fringe… like waterspouts and rogue waves. One in particular, David Williams, proposes that a 'seaquake'… as no damage was noted on the Mary Celeste, his seems an arbitrary explanation」（「後來的研究者」成立）；Chronicle 第 1–3 點 | 200 | CONFIRMED | — |
| c43 | 酒精蒸氣說：船主主張自燃掀開前艙蓋；船長怕出事全員上小艇、用升降索拖著，繩索斷裂 | owner-said-so/mc6a、vapour-theory/mc6b、**captain-notices/mc7g**、all-aboard/mc7h、towed-behind/mc7j、rope-parts/mc7k、boat-left/mc7m、sails-away/mc7l | AH「Or did **spontaneous combustion** occur, **blowing off the fore hatch cover**, as the Celeste's then principal owner, **Captain J. H. Winchester**, afterward maintained?」；SK 第 163 段把上小艇、用最粗的繩子綁住、繩斷、追不上船整段寫成推測 | 200 | **CHANGED**（內容成立，但第 7 章把假說當敘事講，少了「這是目前最站得住的版本」那個標記） | R19 |
| c44 | 反證：主艙口蓋好、沒人聞到氣味；沒有爆炸或火燒痕跡 | main-hatch-closed/mc6c、no-smell/mc6d、no-burn-marks/mc6e | SM07「the boarding party found the main hatch secured and did not report smelling any fumes」；THP 引 Austin 報告結尾「did not discover the slightest trace of there having been any explosion or any fire」 | 200 | CONFIRMED | — |
| c45 | 誤判進水說（MacGregor 2007）：天文鐘誤差 120 哩；煤灰可能堵住幫浦；骨幹 1873 年 Shufeldt 就提過 | without-cause/mc6o、**miscalculation/mc6p**、**chronometer-off/mc6q**、remember-rod/mc6r、pump-apart/mc6s、coal-dust/mc6t、captains-judgement/mc6u | SM07：「Their conclusion: **Briggs was actually 120 miles west of where he thought he was**, probably because of an inaccurate chronometer. By the captain's calculations, he should have sighted land three days earlier than he did.」「Coal dust and construction debris could have fouled the ship's pumps」；MacGregor 的起點是 Solly-Flood 的抄本與「先問什麼沒有發生」，**沒有一個來源說她是從 Shufeldt 那句話往下推的** | 200 | **CHANGED ×2** | R5（方向反了）、R14（因果連結無來源） |
| c46 | 仍解釋不了：小艇從未被找到、為什麼不直接靠岸 | both-have-holes/mc6v、holes-remain/mc7q、why-take-tools/mc7r、never-found/mc7s | Chronicle 1873-01-31「not a word has been heard, nor a trace discovered」、SM07、EB | 200 | CONFIRMED | — |
| c47 | 熱那亞卸貨時 1,701 桶中 9 桶是空的 | genoa-hook/mc6w、genoa-unload/mc7a、remember-casks/mc7b、**nine-empty 卡**＋mc7c | MCN/about「when the cargo was finally unloaded in Genoa nine barrels were found to be empty. **This level of shrinkage was considered normal**」、SM07「nine of the 1,701 barrels in the hold were empty」、SK「nine of the barrels of alcohol were empty: undamaged, yet empty」 | 200 | **CHANGED**（卡片多了一句沒有來源的「其他的都是滿的」，而且跟 c25 的「一桶被打開過」打架） | R11 |
| c48 | 九個空桶是紅橡木，其餘白橡木；紅橡木孔隙大易滲漏 | red-oak/mc7e、porous-oak/mc7f | SM07「recorded as being made of red oak, not white oak like the others. Red oak is known to be a more porous wood」、MCN/about 轉引 SK 的 cooper 說明 | 200 | CONFIRMED | — |
| c49 | 最被接受的是自願棄船（誤判進水或怕蒸氣）、小艇失事，沒有定論 | holes-remain/mc7q、no-verdict/mc7v、unsettled 卡＋mc7w、**outro/mc7x** | SK 第 163 段、EB「A more likely scenario」；本稿自己在 mc6v 說「這兩條路，都還有破洞」；MCN/about 還說九個空桶的漏損量「considered normal」 | 200 | **CHANGED**（片尾第一句把兩條路收成一條，講成「只有九個空桶說得通」） | R12 |
| c50 | 2007 年紀錄片用氣象資料回推，結論「基本上是自己走的」 | drift-study/mc7n／mc7o、sailed-herself/mc7p | SM07「data that MacGregor found in the International Comprehensive Ocean-Atmosphere Data Set (ICOADS)… 'We found out it basically just sailed itself,' Richardson says」 | 200 | CONFIRMED | — |
| c51 | 1885-01 Parker 為詐保駛上海地 Rochelois 礁；船沒沉、騙局被拆穿 | reef-1885/mc7t | SL「she wrecked off Haiti in January 1885, slamming squarely into Rochelois Reef… The ship didn't sink」「a 282-ton, fully-rigged insurance scam」、FV、EB | 200 | CONFIRMED | — |
| c52 | 1885-07 波士頓審判，陪審團 7:5 僵局 | hoax-jury/mc7u | SL「The July 1885 trial of Capt. Parker」「the jury returned with a shocker: They'd deadlocked, 7-5」 | 200 | CONFIRMED | — |

## 標題、說明欄、標籤、縮圖、卡片、sources

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 要改的 |
|---|---|---|---|---|---|---|
| M1 | 「1872 年那艘沒有人的船，十個人去了哪裡？」 | youtube.title | 見 c2 | 200 | CONFIRMED | — |
| M2 | 說明欄第一段：12-04 下午、亞速與葡萄牙之間、帆張著、貨一桶都沒少、食物和水還夠半年、十個人一個都不在 | youtube.description | 見 c1、c11、c19、c25、c26 | 200 | CONFIRMED（「帆張著」照第一版的講法，見摘要） | — |
| M3 | 「直布羅陀副海事法院怎麼把它當成一樁謀殺案」 | youtube.description | 推謀殺的是檢察總長兼 Queen's Proctor（AH「The queen's proctor… promptly convinced himself」、THP 的 1873-01-22 信）；法院本身判了救難金並批評 Morehouse，EB 還寫「British authorities investigated… found no evidence of foul play」 | 200 | **CHANGED**（把一個人的推論說成法院的立場） | R3 |
| M4 | 「一八八四年一篇小說怎麼把熱飯菜和『小艇都在』寫進大家的記憶」 | youtube.description | 見 c3：熱飯菜不在道爾全文裡。本集自己的 mc5g 就說「連這篇小說裡都沒有」 | 200 | **CHANGED**（與本集旁白互相矛盾，也是第一版兩輪都改過的那一條） | R1 |
| M5 | 「照事情被查出來的順序講完這份檔案」 | youtube.description | 熱那亞卸貨發現九個空桶是 1873 年的事，排在 1884 年的小說與 2007 年的研究之後；想確認卸貨日期而開的 MCN/genoa 只有導覽文字 | 200 | NOT FOUND（順序的說法查不到支撐，見摘要；不是硬改） | — |
| M6 | 「資料截至 2026-10-10」 | youtube.description | `sources[].checked_on` 全部 2026-10-10；我在 2026-10-13 重開，全部 200 | 200 | CONFIRMED | — |
| M7 | 十個標籤 | youtube.tags | — | — | OUT OF SCOPE | — |
| M8 | 「船在走／人沒了」「歷史懸案」「一八七二年的檔案」 | thumbnail.data | 見 c1、c2、c19 | 200 | CONFIRMED | — |
| M9 | `cargo-stats`：1,701 桶工業用酒精／1 桶被打開過／出處「直布羅陀勘驗報告 1872-12-23」 | cargo-stats.data | 見 c13、c25 | 200 | CONFIRMED | — |
| M10 | `still-aboard-stats`：半年／留下的糧食與飲水／出處「直布羅陀勘驗報告 1872-12-23」 | still-aboard-stats.data.source | 見 c26：六個月出自 Dei Gratia 船員的證詞（AH、SM07），Austin 報告沒有這個數量 | 200 | **CHANGED** | R10 |
| M11 | `award-stats`：1,700 英鎊／42,643 美元／出處「直布羅陀副海事法院 1873-03」 | award-stats.data | 見 c37 | 200 | CONFIRMED | — |
| M12 | `nine-empty`：9 桶是空的／熱那亞卸貨／**其他的都是滿的** | nine-empty.data.sub | 見 c47：來源只說九桶是空的；「其他的都是滿的」沒有來源，而且 c25 的那一桶是「started」（被動過，就不是滿的） | 200 | **CHANGED** | R11 |
| M13 | `ten-aboard`、`unsettled`、`outro` 三張卡的字 | 各 data | 見 c2、c49 | 200 | CONFIRMED | — |
| M14 | 七個章名 | scenes[].chapter | 都只用章內已查過的事實 | 200 | CONFIRMED | — |
| M15 | `sources[]` 20 筆、`checked_on` 2026-10-10 | sources | 全部 2026-10-13 重開 200；`sources[0]`／`[1]` 是 web.archive 快照，內容與原站一致 | 200 | CONFIRMED（註記見摘要） | — |
| M16 | `loops[]` 五組 setup／payoff | loops | 十個 id（mc1i/mc6r、mc1k/mc7i、mc2l/mc6i、mc3t/mc7n、mc4m/mc5g）在稿子裡都存在 | — | OUT OF SCOPE | — |

## 沒有主張可對的句子

`map.mjs` 把 131 個場景逐一對過 `claims.md`：**只有一個場景完全沒有主張可對**，另外幾句是
`claims.md` 自己列在「不是來源主張的句子」那一節的。

| # | 句子 | 位置 | 判定 | 說明 |
|---|---|---|---|---|
| A1 | 「大西洋上風浪不小」 | opening-swell/**mc1a** | **NOT FOUND** | c1 與 c19 都沒有講當天的海況。開得到的來源裡：SM07 把大浪放在**最後一筆日誌的前一晚**（11-24／25，「rough seas and winds of more than 35 knots」）；EB、HH 說的是**啟航後兩週**「harsh weather」；MCN/facts 第 6 條只寫發現時間。**12-04 下午的海況沒有任何來源**，而同一稿的 mc3d 還要講勘驗官說「她沒有遇上特別惡劣的天氣」（Chronicle 第 3 點、Austin 第 4 段）。要改：R13 |
| A2 | 「一個真實的船名，被一篇小說蓋了一百五十年」 | covered-150/**mc5u** | **CHANGED** | 整個場景在 `claims.md` 沒有對應的編號（`map.mjs` 唯一的漏網），只在「算出來的數字」那一節被當成 1872 到今天的算術。但這句話的主詞是**那篇小說**（1884），到 2026 是 142 年。要改：R18 |
| A3 | 「救難金不是誰撿到就歸誰，要法庭判。」 | salvage-money/mc2e | CONFIRMED | AH：Morehouse 的 salvage claim 由副海事法院審（c29 的同一段） |
| A4 | 「他看著德沃，覺得這個故事不對。」 | doesnt-believe/mc2g | OUT OF SCOPE | 鏡頭調度；懷疑本身是 c29（AH「promptly convinced himself」）。沒有編造對話或心理活動 |
| A5 | 「以為船要沉了，是一個船長會做的判斷。」 | captains-judgement/mc6u | OUT OF SCOPE（但見摘要） | 這是判斷句，卻沒有像 mc3p、mc4l 一樣標成「我的看法是」 |
| A6 | 「勘驗官在直布羅陀數的是有沒有人動過，不是桶裡還剩多少。」 | casks-counted/mc7d | CONFIRMED | Chronicle 第 1 點記的正是「well stowed and in good order and condition, except one which had been started」——記的是有沒有被動過。這一句是**減弱**而不是加強，沒問題 |
| A7 | 「這兩件事都不在法庭紀錄裡。」 | not-in-records/mc5e | CONFIRMED | 比來源還保守：小艇都在、被拖進港不只是「不在紀錄裡」，是被紀錄否定（MCN/facts 第 2、19 條） |
| A8 | 「這個頻道只講紀錄裡有的，想一起開檔案就訂閱。」 | outro/mc7z | OUT OF SCOPE | CTA |
| A9 | 升級句、鉤子問句、兩句「我的看法是」 | mc2r、mc4e、mc5l、mc2l、mc3u、mc5v、mc4n、mc1l、mc7y、mc3p、mc4l | OUT OF SCOPE | 與 `claims.md`「不是來源主張的句子」一節一致 |

## 要求的改動

每一條都只動事實與連帶的字，不動順序、節奏、章名、場景數，行 id 不變；括號裡是改後的
`spokenUnits`（現在的值→改後的值）。**我沒有改任何檔案**。

| # | 行 id／欄位 | 現在的字 | 應該變成 | 為什麼 |
|---|---|---|---|---|
| **R1** | `youtube.description` 第二段 | 「…以及一八八四年一篇小說怎麼把熱飯菜和『小艇都在』寫進大家的記憶…」 | 「…以及一八八四年一篇小說怎麼把『小艇都在』寫進大家的記憶，還有熱飯菜是從哪裡長出來的…」 | 熱飯菜不在道爾全文裡（WS 全文；AH「Other romancers added」）。這正是第一版查核第一輪與第二輪各改過一次的那一條，重講時又回來了，而且和本集 mc5g「連這篇小說裡都沒有」當場矛盾 |
| **R2** | `added-later/mc5h` | 「是後來別人轉述的時候，才加上去的。」 | 「是別人轉述的時候，才加上去的。」（15→13） | 「後來」是先後的斷言。`claims.md` c3 自己寫「熱飯菜比道爾早還是晚…來源都沒有標年份，**所以旁白不講先後**」；第一版第二輪就是為了這個把卡片的「後來的轉述」改成「其他轉述」。AH 的「Other romancers added」沒有年份，唯一有年份的線索（1883-06）第一版也開不到 |
| **R3** | `youtube.description` 第二段 | 「直布羅陀副海事法院怎麼把它當成一樁謀殺案」 | 「直布羅陀的檢察總長怎麼把它當成一樁謀殺案」 | 推謀殺的是檢察總長兼 Queen's Proctor Solly-Flood（AH、THP 的信）；法院判了救難金、還批評 Morehouse，EB 寫當局「found no evidence of foul play」。把一個人的推論說成法院的立場是失去歸屬 |
| **R4** | `sea-tore-wood/mc4d` | 「三個月後，一艘美國軍艦的艦長說，那是海水撕裂的木頭。」 | 「一個多月後，一艘美國軍艦的艦長說，那是海水撕裂的木頭。」（23→24） | 前一句 mc4b 的日期是 1873-01-30（Patron 報告），Shufeldt 的報告見 Chronicle **1873-03-04**，相隔一個月又四天。`claims.md` 的「算出來的數字」那一節把它寫成「（1873-01-30 到 1873-03-04）＝三個月後」，算術本身就錯了（從發現那天 12-04 算才是三個月，但旁白的前句不是那個日期） |
| **R5** | `chronometer-off/mc6q` | 「天文鐘有誤差，讓船長以為自己在一百二十哩以西。」 | 「天文鐘有誤差，船長的位置比他以為的偏西一百二十哩。」（21→23）<br>或「天文鐘有誤差，船長以為自己比實際位置偏東一百二十哩。」（24） | **方向反了。** SM07：「Briggs was actually **120 miles west of where he thought he was**」——實際位置在西，他以為自己偏東，所以「he should have sighted land three days earlier than he did」。現在的講法把它說成他以為自己偏西，正好相反。**`claims.md` 的 c45 也寫反了**（「以為自己在實際位置以西 120 哩」），請連帶修正 |
| **R6** | `kill-captain/mc2i` | 「喝醉之後殺了船長，再划小艇逃走。」 | 「喝醉之後殺了船長，再上別的船逃走。」（14→15） | c30 只引 THP，而 THP 引的 1873-01-22 信原文寫的是「**escape on board some vessel** bound for some north or South American port or the West Indies」。AH 的摘要寫「escaped in the boat」，但那不是 c30 的來源；要用 AH 的版本就得把 AH 加進 c30 |
| **R7** | `cargo-stats/mc2p` | 「喝下去會死人，而且只有一桶被打開過。」 | 「那不是拿來喝的，而且只有一桶被打開過。」（16→17） | c13 寫的是「不能喝」，第一版的 55b2 也是「工業用的，不能喝」。來源最強的講法是 NEHS「undrinkable」、FV「toxic」；**沒有一個來源說喝了會死**，而且 SK（「pure grain alcohol, intended to fortify cheap Italian wines」）與 MCN/about（「not be palatable to drink」、denatured 是 1906 年以後才有的做法）都說它是可以喝的酒精。把爭議點講成致命是這一版新加的強度 |
| **R8** | `galley-stove/mc3f` | 「奇怪的是，廚房的爐灶被撞離了原位。」 | 「上船那天的證詞說，廚房的爐灶被撞離了原位。」（15→19） | 事實成立，但這一版把它排進第 3 章「十二月二十三日勘驗官上船」那一段，前後都是 Austin 的發現（mc3d「勘驗官還記了一筆」、mc3e 油瓶），聽起來就是勘驗官看到的。MCN/facts 第 4 條的出處欄寫的是「Testimony before Vice-Admiralty Court, Gibraltar, 1872」，而 **Austin 第 21 段**反過來寫爐灶與炊具「in good order and exhibited no appearance of having suffered from exposure to water」（第一版第二輪已註明兩者差了兩週半）。加一個時間標記就解決，mc3p 的意見句照樣成立 |
| **R9** | `binnacle-knocked/mc3g` | 「羅經櫃也歪了，羅盤的玻璃罩破了。」 | 「那天的羅經櫃也歪了，羅盤的玻璃罩破了。」（14→17） | 同 R8。c27 的兩個來源（NEHS、FV）講的都是 12-04 發現時的狀態；**Austin 第 54 段**寫「The binnacle itself did not appear to have sustained any damage」，第 52 段還把裂掉的玻璃歸給燈的熱度。放在勘驗那一段會變成勘驗官說了他沒說的話 |
| **R10** | `still-aboard-stats.data.source` | 「直布羅陀勘驗報告 1872-12-23」 | 「Dei Gratia 號船員在直布羅陀的證詞，1872–73」（第一版同一張卡的出處） | 「六個月的糧食與飲水」出自上船的人（AH「The ship's stores contained provisions for six months and ample drinking water」、SM07「a six-month supply」）。**Austin 的報告全文沒有任何「六個月」**，第 59 段只寫「barrels of stores and other provisions in good order」。同一張卡的 1,701／一桶（`cargo-stats`）掛在勘驗報告上是對的（AH 稱那次是「A survey of the 1,701 barrels」），但糧水不是 |
| **R11** | `nine-empty.data.sub` | 「其他的都是滿的」 | 「其他的沒有漏」（或「1,701 桶裡只有這 9 桶是空的」） | 來源只說九桶是空的（MCN/about、SM07、SK），沒有說其餘 1,692 桶都是滿的；而且本集自己的 c25 說有一桶被「started」（動過），那一桶就不是滿的。另外 MCN/about 還補了一句「This level of shrinkage was considered normal」，卡片不該把它講成反常的全有全無 |
| **R12** | `outro/mc7x` | 「十個人離開的理由，目前只有那九個空桶說得通。」 | 「十個人離開的理由，目前最說得通的是那九個空桶。」（20→21） | c49 列的是**兩條**路（誤判進水或怕蒸氣），本集自己在 mc6v 說「這兩條路，都還有破洞」、在 mc7q 說「這個解釋還是擋不住」。「只有…說得通」把一個未結的案子收成唯一解，也把第 6 章整段（2007 年的誤判進水）作廢。順帶一提：`claims.md` 最後一節寫「現在第一句是點名的回呼『還記得那九個空桶嗎？』」——那句話不在 `video.json` 裡（`grep` 0 筆），文件落後於稿子，請一起更新 |
| **R13** | `opening-swell/mc1a` | 「一八七二年十二月四日下午，大西洋上風浪不小。」 | 「一八七二年十二月四日下午，大西洋的正中間。」（20→19）<br>或「一八七二年十二月四日下午，亞速群島東邊的大西洋上。」（23，位置有 AH、MCN/facts 第 15 條） | 當天的海況沒有來源（見 A1），而本集 mc3d 要講勘驗官認定「她沒有遇上特別惡劣的天氣」。日期本身不用改：MCN/facts 第 6 條明寫 12-04 下午 1–2 時，並把 5 日列為誤傳，mc3v 也把兩個日期都講了。（同場景的 `prompt` 寫了 long swells，`prompt` 是畫面不是主張，留給撰稿方決定） |
| **R14** | `miscalculation/mc6p` | 「二零零七年，有一份研究從這句話往下算。」 | 「二零零七年，有一份研究從同一個念頭往下查。」（17→19） | c45 說的是「這個骨幹 Shufeldt 就提過」，不是 2007 年那份研究**從 Shufeldt 的那句話**出發。SM07 寫 MacGregor 的起點是「asking what didn't happen」與 Solly-Flood 的日誌抄本，沒有一個字把她接到 Shufeldt 的報告上。兩個事實不要併成一個因果 |
| **R15** | `sea-monster/mc5m` | 「後來的人又加了海怪，加了巨大的章魚。」 | 「還有人說是海怪，說是巨大的章魚。」（16→14） | 年代有衝突：AH 把 giant octopus 放在道爾之後的作者群，**MCN/about 卻寫「A popular theory at the time was that a giant squid, octopus, kraken…」**（當年就有）。第一版第二輪把這一點記成未決、留給撰稿方。拿掉先後，「紀錄裡一個字都沒有」（mc5q）照樣站得住；百慕達那一句（mc5n）不用動 |
| **R16** | `lookout-glass/mc1b` | 「一艘英國帆船的瞭望手舉起望遠鏡。」 | 「一艘英國帆船的船長舉起望遠鏡。」（15→14） | AH：「her master, David Reed Morehouse, sighted a sailing ship on his port bow… **Through a glass** he perceived…」；FV 寫的是 helmsman。**沒有來源有「瞭望手」**。改成船長既有來源，也替 mc2b 的莫爾豪斯鋪了路 |
| **R17** | `family-gangplank/mc2m` | 「十一月七日，他從紐約帶著太太莎拉和兩歲的女兒蘇菲亞上船。」 | 「十一月七日，他帶著太太莎拉和兩歲的女兒蘇菲亞離開紐約。」（26→25） | 11-07 是**啟航**日（EB「set sail from New York City」、HH「set sail from New York on 7 November」），不是上船日；MCN/facts 第 14 條還記了 Maritime Register 的 11-04。c12 寫的也是「自紐約啟航」。順帶把全稿最長的一句（26 單位）壓回 25 |
| **R18** | `covered-150/mc5u` | 「一個真實的船名，被一篇小說蓋了一百五十年。」 | 「一個真實的船名，被一篇小說蓋了一百多年。」（19→18） | 這句話的主詞是 1884 年那篇小說，到 2026 是 142 年。「一百五十年」是第一版從 1872 年算出來的數字（第一版那句是「酒館裡講了一百五十年」），換了主詞之後沒有跟著換 |
| **R19** | `captain-notices/mc7g` | 「船長發現艙裡有水，或者聞到不對的味道。」 | 「最站得住的版本是：船長發現艙裡有水，或者聞到味道。」（17→22） | 第 7 章的 mc7g–mc7m 用敘事過去式把 c43 的假說整段講完（發現有水→叫全員上小艇→綁繩子→繩斷→船走掉），中間沒有任何「這是推測」的標記；第一版是用 `qa9h`「所以目前最站得住的版本是：…」掛在前面的。mc7q 的「這個解釋」要兩分鐘後才出現，`unsettled`／mc7v 的「沒有定論」更晚。這一條的輕重由撰稿方判斷，但依「沒有定論就說沒有定論」，標記應該在假說開始的地方 |

### 不在 `video.json`、但應該跟著修的檔案（我沒有動）

| 檔案 | 位置 | 問題 |
|---|---|---|
| `claims.md` | c45 | 「天文鐘誤差讓 Briggs 以為自己在**實際位置以西** 120 哩」——方向與 SM07 相反，見 R5。這一條是從第一版繼承的，第一版的旁白（`avqr`「船長以為自己在別的地方」）沒有講方向，所以錯誤沒有露出來；這一版把方向寫進旁白才顯形 |
| `claims.md` | 「算出來的數字」一節 | 「`sea-tore-wood` 的『三個月後』（1873-01-30 到 1873-03-04）」——這兩個日期差一個月又四天，見 R4 |
| `claims.md` | 最後一節 | 寫「現在第一句是點名的回呼『還記得那九個空桶嗎？』」，但 `video.json` 的 mc7x 是「十個人離開的理由，目前只有那九個空桶說得通。」；`NOTES.md` 第三輪的對照表才是現狀。見 R12 |
| `brief.md` | 第 48 行 | 「熱飯菜與溫著的茶是**後來**別人轉述時加的」——同 R2 的先後問題（第一版第二輪也留下同樣的 `brief` 衝突給站主） |

## 摘要

- **抽出 270 條**（140 句旁白、28 個卡片欄位、7 個章名、標題 1、說明欄 1、標籤 10、縮圖 5、
  `youtube`／`loops` 15、`sources` 60；`say`／`say_for` 0，`assets[]` 空）。
  合併成 **52 條主張列（c1–c52）＋16 條標題／說明欄／卡片／sources 列（M1–M16）＋9 條沒有主張可對的（A1–A9）**，
  共 **77 列**。
- 判定：**CONFIRMED 50、CHANGED 19 列、NOT FOUND 2、OUT OF SCOPE 6**（合計 77）。
  CHANGED 的列：c3（兩處）、c5、c10、c12、c13、c20、c26、c27、c30、c34、c43、c45（兩處）、c47、c49、
  M3、M4（＝c3 的同一處）、M10（＝c26）、M12（＝c47）、A2；NOT FOUND：A1 的海況、M5 的「查出來的順序」。
  去掉互相指向的重複之後，**要求的改動共 19 處（R1–R19）**：15 處在旁白、2 處在說明欄、2 處在卡片。
- **每一個場景都對得到 `claims.md` 的某一條**，只有 `covered-150` 例外（A2）；`claims.md` 提到的場景 id
  也沒有一個在 `video.json` 裡找不到。沒有「完全沒有主張撐著」的事實句，只有一句算術（A2）與一句
  海況（A1）在表外。
- **最重的四條**：R1（說明欄把熱飯菜算回 1884 小說，第一版兩輪都改掉的錯又回來，且與本集 mc5g 矛盾）、
  R5（天文鐘 120 哩的方向反了，連 `claims.md` c45 一起）、R8／R9（爐灶與羅經櫃搬進勘驗那一章，
  變成勘驗官說了他報告裡反過來寫的話）、R12（片尾把未結的案子收成「只有九個空桶說得通」）。
- **數字與日期全部重算過**：1,701／1 桶／9 桶／3.5 英尺＝一公尺多／6 哩＝11 公里／£1,700／
  $5,700＋$36,943＝$42,643＝五分之一／7:5／37 歲／十個人／七個船員／1861-05-18／1868／1872-11-07／
  11-25／12-04（日誌 5 日）／12-12／12-13／12-18／12-23／1873-01-22／1873-01-30／1873-03-04／
  1873-03／1885-01／1885-07 全部對得上來源。**錯的只有三個算出來的數字**：R4（三個月→一個多月）、
  R18（一百五十年→一百多年）、R5（120 哩的方向）。其他算術（五天後、九天、十二年後、七年後）都對。
- 會過期的事實：沒有。看到的頁面日期：Britannica 標「Last updated Sep. 18, 2026」、SM07 2007-11、
  AH 1981-02／03、THP 2023-01-05、SK 2011-12-20、SL 2011-12、ACD 2021-10-31、NEHS「updated in 2026」。
- `sources[0]`／`sources[1]` 改用了 web.archive 快照（2026-09-20、2026-08-19），`claims.md` 引的是原站。
  兩邊今天都 200、內容一致，所以不影響判定；但快照日期**早於** `checked_on` 的 2026-10-10，
  而第一版讀到的 Britannica 標的是 2026-09-18 更新——要嚴謹就把 `checked_on` 改成快照日，
  或把 `sources` 換回原站網址（原站今天也開得了）。這一條我沒有列進要求的改動。
- 懷疑但沒有要求改的：
  - `mc2a`「大副德沃沒有等人來救，他決定自己把船開走」：AH 寫的是 Deveau **提議**、Morehouse 同意
    （「Mate Deveau proposed that he sail the derelict to Gibraltar, and Morehouse… detailed two seamen」）。
    「他決定」略強，但下一句就把莫爾豪斯帶出來，聽得懂是誰拍板，保留。
  - `mc6u`「以為船要沉了，是一個船長會做的判斷」：是判斷句，卻沒有像 mc3p、mc4l 一樣標成
    「我的看法是」。若 R19 採用，這句會被前面的標記蓋住；若不採用，建議標成意見。
  - `mc7b`「這時候才真的被數過」：直布羅陀也數過（c25），但下一句 mc7d 就把兩個數字的差別講清楚了，
    `NOTES.md` 也說那一句是為它寫的，保留。
  - 說明欄「帆張著」沒有寫「部分」：只有三面帆張著（MCN/facts 第 5 條把「all sails set」列為誤傳），
    但第一版的說明欄是同樣的寫法且兩輪都 CONFIRMED，照舊。
  - `mc3k`「航海手冊和船籍文件，也一起被帶走了」：來源寫的是 missing／not found（AH、Chronicle），
    「被帶走」是推論；但 mc3q「帶走的是找路的工具」第一版就 CONFIRMED 過，同一個框架，保留。
  - `mc6p`「一份研究」：c50 說的是 2007 年 Smithsonian Channel 的紀錄片（Anne MacGregor）。
    她確實做了研究（ICOADS、Richardson 的漂流計算），叫「研究」說得通，但全稿沒有一處說它是紀錄片。
  - `mc3f`／`mc3g` 的事實本身（爐灶、羅經櫃）第一版兩輪都 CONFIRMED 過，這一輪改的只有歸屬。
  - `mc2n`「他雇的船員」：NEHS「handpicked his crew of seven」，成立。
  - 熱那亞卸貨的日期：MCN/genoa 開得了（200）但沒有可用內文，所以 M5 的「照事情被查出來的順序」
    查不到支撐；這是對本集結構的說法，不是歷史事實，留給撰稿方決定。
  - SK 說九個空桶是在直布羅陀發現的（少數），MCN/about 與 SM07 寫熱那亞或不寫地點，照舊寫熱那亞。
- 內容守則：傳說都標明是加上去的（但先後要照 R2、R15 拿掉）；沒有編造布里格斯一家的對話或心理
  （mc7g–mc7m 是 c43 的假說敘述，需要 R19 的標記）；沒有血腥；沒有「經查證」「根據官方文件」「本影片」；
  旁白沒有括號或網址；唯一的拉丁字 Dei Gratia 在第一版就進了 `lexicon.json`。
  片尾沒有講下一支（第一版的「下一份檔案：51 區」已經拿掉），符合 10-13 的新規則。
- 聽眾檢查：140 句最長 26 單位（`mc2m`，R17 改後 25），25 單位兩句（`mc3p`、`mc7d`），
  其餘都在 24 以內；沒有超過 `SENTENCE_WARN`（40）的句子。要求改動的 15 句旁白改後全部 ≤24 單位。
  卡片上的數字（1,701、42,643、1,700、9、10、半年）旁白都用國字唸過，不需要補 `say`／`say_for`。
- 程序註記：**沒有跑 git、沒有跑任何影片階段（含 `lint`）、沒有花錢、沒有用網路搜尋（0 次）**；
  curl 的 User-Agent 用的是 `support@mokaair.com`，沒有放任何個人信箱。
  輔助檔在 `<scratch>\verify-h01\`（`extract.mjs`、`map.mjs`、`fetch.sh`、`totext.mjs`、
  `claims-list.txt`、`status.txt`、`dl/`、`txt/`）。
- **第二輪：需要。** 這一輪要改 19 處、涵蓋 16 條主張列，遠超過 3 條。第二輪請換人，至少重查
  R1–R12（尤其 R5 的方向與 R4 的間隔——兩者都要回 SM07 與 Chronicle 1873-03-04 原文），
  再從 54 條 CONFIRMED 裡隨機抽三分之一。另外請一併處理 `claims.md` c45 寫反的方向、
  「算出來的數字」那一節的錯誤算術、最後一節與 `video.json` 不符的片尾描述，以及 `brief.md` 第 48 行。
