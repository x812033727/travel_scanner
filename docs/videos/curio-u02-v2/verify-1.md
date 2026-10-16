# curio-u02-v2 查核第一輪

- 查核 2026-10-13，Claude Opus 5（查核代理，不是撰稿的那一個，也不是第一版兩輪查核的那幾個）。
- 這是第二版：事實應該全部沿用第一版兩輪查核後的版本，只有講法重寫。所以這一輪的重點是
  「同一個事實換個說法之後，有沒有比來源強」。
- 方法：先把 `video.json` 的每句旁白（145 句，沒有任何一句有 `say`／`say_for`）、每張卡片的
  `data` 欄、章名、縮圖、標題、說明欄、標籤抽成 231 條清單
  （`<scratch>\verify-u02\claims-list.txt`），對到這一版 `claims.md` 的 30 條主張；再把
  `claims.md` 與第一版 `research.md` 列的每個網址當天用 curl 重開
  （User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機用
  `--rate 40/m`＝每 1.5 秒一次，超過提示要求的 1.2 秒）。CIA 史三章 PDF（第 1、2、6 章，30 MB）
  下載後用 pdftotext 抽字；文字層破損的書頁 56、72 和整頁地圖的書頁 58 用 PyMuPDF 轉成圖逐字讀
  （`<scratch>\verify-u02\img\`）。**網路搜尋用了 0 次**（來源都已經有名有網址）。
- 「官方頁」指一手或權威來源。最重的是國家安全檔案館 EBB 434 的 CIA 史 2013 年解密版
  （每頁印 Approved for Release: 2013/06/25）、聯邦公報與其 API、國家檔案館、GAO、
  柯林頓白宮存檔、EBB 443、CIA 官網；其次路透社（CSMonitor 轉載）、AP（KTVU 轉載）、
  Las Vegas Sun 1998、The Space Review、Skeptic、KNPR、KLAS 的兩篇回顧（Wayback）。
  Wikipedia 沒有用。
- 我沒有改 `video.json`、`claims.md`、`brief.md`、`NOTES.md` 的任何一個字；要改的都寫在最後一節，
  附行 id、現在的句子、建議的句子與單位數（用 `tools/video/core/timeline.mjs` 的 `spokenUnits`
  量過，全部在 24 單位以內）。沒有跑 git，沒有跑任何影片階段。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| EBB434 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/ （導言、Pocock 評註） | 200 |
| CH1 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%201.pdf （7.8 MB） | 200 |
| CH2 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf （12.2 MB；書頁 56、58、72 轉圖逐字讀） | 200 |
| CH6 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%206.pdf （10.4 MB；書頁 288–289、297） | 200 |
| CIA-1998 | https://www.cia.gov/resources/csi/books-monographs/the-cia-and-the-u-2-program-1954-1974/ | 200 |
| CIA-2015 | https://www.cia.gov/stories/story/area-51-and-the-accidental-test-flight/ | 200 |
| CIA-Molly | https://www.cia.gov/stories/story/ask-molly-what-really-went-on-at-area-51/ | 200 |
| CIA-Museum | https://www.cia.gov/legacy/museum/artifact/untouchable/ | 200 |
| CIA-RR | https://www.cia.gov/readingroom/node/1819895 | 200 但轉到閱覽室首頁：NOT OPENED |
| Reuters | https://www.csmonitor.com/USA/Latest-News-Wires/2013/0817/Area-51-is-real-say-CIA-documents | 200 |
| FR95 | https://www.govinfo.gov/content/pkg/FR-1995-10-10/html/95-25244.htm | 200 |
| FR-API | https://www.federalregister.gov/api/v1/documents.json?conditions[term]="Groom Lake"（11 筆，其中 9 筆是 1995–2003 歷年的 Determination） | 200 |
| Clinton96 | https://clintonwhitehouse6.archives.gov/1996/01/1996-01-31-determination-exempting-usaf-from-conservation-laws.html | 200 |
| GAO | https://www.govinfo.gov/content/pkg/GAOREPORTS-NSIAD-95-187/html/GAOREPORTS-NSIAD-95-187.htm | 200 |
| NARA | https://www.archives.gov/research/military/air-force/ufos | 200 |
| EBB443 | https://nsarchive.gwu.edu/briefing-book/intelligence/2013-10-29/area-51-file-secret-aircraft-soviet-MiGs | 200 |
| ELR | https://www.elr.info/litigation/kasza-v-browner | 200 |
| LVSun98 | https://lasvegassun.com/news/1998/jan/08/toxic-data-at-area-51-ruled-confidential/ | 200 |
| CBS00 | https://www.cbsnews.com/news/satellite-image-of-area-51/ | 200 |
| TSR | https://thespacereview.com/article/4518/1 | 200 |
| Skeptic | https://www.skeptic.com/article/the-strange-case-of-bob-lazar/ | 200 |
| KNPR | https://knpr.org/knpr/2015-02/area-51-whistleblower-speaks-ufo-conference （轉到 2015-02-12 網址） | 200 |
| KLAS-a | https://web.archive.org/web/20210507140618/https://www.8newsnow.com/news/local-news/i-team-man-who-detailed-ufo-secrets-decades-ago-helped-launch-area-51-stampede/ | 200 |
| KLAS-b | https://web.archive.org/web/20210117151518/https://www.8newsnow.com/news/i-team-25-years-later-man-who-exposed-area-51/ | 200 |
| AP | https://www.ktvu.com/news/about-75-people-gather-at-area-51-gate-1-person-arrested | 200 |
| C-USGS | https://commons.wikimedia.org/wiki/File:Area_51_28_August_1968_2.jpg | 200 |
| C-1967 | https://commons.wikimedia.org/wiki/File:CIA_BYE2369-67_page17.gif | 200 |
| C-BB | https://commons.wikimedia.org/wiki/File:Appendix_I_to_Project_Blue_Book_Status_Report_Number_8_-_NARA_-_595542.jpg | 200 |
| NPR-13 | https://www.npr.org/sections/thetwo-way/2013/08/16/212549163/ （`claims.md` c3 的第二個網址；不在 `sources[]` 裡） | 000 連線逾時：NOT OPENED |

KLAS-a／KLAS-b 是第一版 `claims.md` c6 列、這一版 c6 漏掉的兩個網址；因為第 5 章有四句只有它們撐得住，所以我自己開了（見第 77、78、81 列與改動要求 S）。

## 主張表

判定：CONFIRMED 看到了／CHANGED 要改／NOT FOUND 沒看到／OUT OF SCOPE 風格、問句、回呼、系列安排。
位置是行 id 或 `scene.data` 路徑；同一個事實出現在幾個地方就併成一列。

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 現在 → 建議 |
|---|---|---|---|---|---|---|
| 1 | 「51 區」這個名字 CIA 等了 58 年才正式印在文件上（1955→2013） | youtube.title | Reuters（"the first deliberate official references to Area 51"）、CH2 p.56（12 April 1955）、EBB434（approved 25 June 2013） | 200 | CONFIRMED | —（靠「正式」＝刻意的官方承認撐著，與第一版兩輪的判法一致） |
| 2 | 1955-04-12 **下午**，四個人坐小飛機飛過內華達 | youtube.description 第 1 段 | CH2 p.56 原頁只寫 "On 12 April 1955"；CIA-2015 也只有日期；CH2 與 CIA-2015 全文沒有 afternoon | 200 | CHANGED | 「四月十二日下午」→「四月十二日」 |
| 3 | 這個編號，CIA 自己的正式文件等了五十八年才印出來 | youtube.description 第 1 段 | Reuters（first **deliberate** official references）；C-1967 本身就是 CIA 正式文件、1967 年就印著 "deployed from Area 51 to Kadena"；本片第 4 章自己也這樣講 | 200 | CHANGED | 「等了五十八年才印出來」→「等了五十八年才刻意印出來」（第一版查核第一輪為同一句改過一次，見 curio-u02/verify-1.md #21） |
| 4 | 說明欄第 2 段的清單：三次首飛、七萬英尺的機翼、1967 年的文件、1968 年的航照、1989 年的訪談、1995 年起的命令、八年的申請、第 58 頁的地圖 | youtube.description | 見第 30、40、63、66、72、91、106、113 列 | 200 | CONFIRMED | — |
| 5 | 流傳版標出處與年份、在世人物只講他說過的話、沒有定論就說沒有定論 | youtube.description 第 3 段 | 編輯守則 | — | OUT OF SCOPE | — |
| 6 | 插圖由 AI 生成、畫中的人是虛構卡通角色、不寫名字、在世或近代人物不入畫 | youtube.description 第 4 段 | 125 個 `prompt` 逐一看過：沒有任何人名，電視訪談那張是 "face in deep shadow"，簽署那張只有一隻手 | — | CONFIRMED | — |
| 7 | 資料截至 2026-10-10 | youtube.description 第 5 段 | `sources[]` 16 條的 `checked_on` 都是 2026-10-10；我今天（10-13）重開，內容沒有變 | 200 | CONFIRMED | —（要不要改成 10-13 由撰稿方決定，不是錯） |
| 8 | 標籤十個 | youtube.tags | — | — | OUT OF SCOPE | — |
| 9 | 縮圖「飛碟？是飛機」「外星與太空」「2013 年解密的檔案」 | thumbnail | Reuters（CIA 發言人：在那裡試 U-2 與 A-12，沒有外星人）、EBB434 | 200 | CONFIRMED | — |
| 10 | 第 1 章章名「他們差一點降落在那片鹽湖上」 | basin-from-above.chapter | CH2 p.56 原頁："After debating about landing on the old airstrip, LeVier set the plane down on the lakebed, and all four walked over to examine the strip."——鹽湖床他們**降落了**；差一點降落的是那條舊跑道 | 200 | CHANGED | 「他們差一點降落在那片鹽湖上」→「他們差一點降落在那條舊跑道上」 |
| 11 | 一九五五年四月十二日，內華達上空 | u101 | CH2 p.56 | 200 | CONFIRMED | — |
| 12 | 小飛機上坐著四個人 | u102 | CH2 p.56（Bissell、Ritland、Johnson、LeVier；"all four walked over"） | 200 | CONFIRMED | — |
| 13 | 他們在找一個地方，試飛一架飛機 | u103 | CH2 p.56（"to search for a site where the aircraft could be tested safely and secretly"） | 200 | CONFIRMED | — |
| 14 | 底下是一片白色的乾鹽湖 | u104 | CH2 p.56（"a salt flat known as Groom Lake"）、CIA-2015（dry lakebed） | 200 | CONFIRMED | — |
| 15 | 這塊荒地的地圖編號是 Area 51 | map-number.data、u105 | CH2 p.56（"this strip of wasteland, known by its map designation as Area 51"）、CIA-2015（"The strip of wasteland was known **at the time** by its map designation: Area 51"）——所以在選址這一段就講這個編號不算提前 | 200 | CONFIRMED | — |
| 16 | 旁邊有一條直線，像一條跑道 | u106 | CH2 p.56（"what appeared to be an airstrip"） | 200 | CONFIRMED | — |
| 17 | 那不是柏油，是鬆掉的土 | u107 | CH2 p.56（"From the air the strip appeared to be paved… compacted earth that had turned into ankle-deep dust"） | 200 | CONFIRMED | — |
| 18 | 要是降落，飛機會往前翻 | u108 | CH2 p.56（"If LeVier had attempted to land on **the airstrip**, the plane would probably have nosed over"）——原文限定在那條跑道，配上第 10 列的章名會被聽成鹽湖 | 200 | CHANGED | 「要是降落，飛機會往前翻。」→「要是降落在那條線上，飛機會往前翻。」（15 單位） |
| 19 | 機上的人幾乎是整個計畫的核心 | u109 | CH2 p.56（"killing or injuring all of the key figures in the U-2 project"） | 200 | CONFIRMED | — |
| 20 | 回到華盛頓才發現，它不屬於試驗場 | u110 | CH2 p.56（"Upon returning to Washington, Bissell discovered that Groom Lake was not part of the AEC proving ground"） | 200 | CONFIRMED | — |
| 21 | 他們請原子能委員會把它劃進來 | u111 | CH2 p.56（"asked the Atomic Energy Commission to add the Groom Lake area to its real estate holdings"；Strauss readily agreed） | 200 | CONFIRMED | — |
| 22 | 艾森豪總統批准了 | u112 | CH2 p.56（"President Eisenhower also approved the addition"） | 200 | CONFIRMED | — |
| 23 | 一個地圖編號，為什麼等了五十八年才印出來？ | u113 | 同第 3 列 | 200 | CHANGED（建議） | 「才印出來？」→「才正式印出來？」（21 單位） |
| 24 | 第 2 章章名「八月一日，它自己飄了起來」 | runway-ready.chapter | CH2 p.69（1 August 滑行測試中離地） | 200 | CONFIRMED | — |
| 25 | 跑道在七月鋪好，人開始搬進去 | u201 | CH2 p.57（"project managers decided that a paved runway was needed… By July 1955 the base was ready, and Agency, Air Force, and Lockheed personnel began moving in"） | 200 | CONFIRMED | —（「鋪好」仍是推論，原文沒寫完工日；第一版兩輪也這樣留著） |
| 26 | 工程師取名天堂牧場，後來簡稱牧場 | u202、u203、u204 | CH2 p.57、CIA-2015（"called it 'Paradise Ranch,' which was soon shortened to just 'the Ranch'"） | 200 | CONFIRMED | — |
| 27 | 三個名字：51 區（地圖編號）、天堂牧場（招工人用）、夢境（無線電呼號） | names-table.rows、u206 | CH2 p.57；CIA-2015（Dreamland 是 1960 年代末起的呼號，據 TD Barnes） | 200 | CONFIRMED | — |
| 28 | 表格出處「CIA 計畫史 p.57」 | names-table.data.source | 「夢境」不在 CIA 史 p.57，只在 CIA-2015；第一版卡片寫的是「CIA 史 p.56–57；CIA 2015 年文章」 | 200 | CHANGED | 「CIA 計畫史 p.57」→「CIA 計畫史 p.57；CIA 2015 年文章」 |
| 29 | 一九六〇年代末，無線電裡叫它夢境 | u206 | CIA-2015（"a radio call sign for the base, introduced in the late 1960s"） | 200 | CONFIRMED | — |
| 30 | 三次「首飛」：8/1 滑行測試中自己離地、8/4 第一次計畫內飛行、8/8 長官在場的官方首飛 | first-flights.data、u207、u208、u209、u210、u211 | CH2 pp.69–70 逐句（LeVier："I had no intentions whatsoever of flying"；"the first planned flight on 4 August 1955"；"scheduled the 'official' first flight for 8 August 1955. This time outsiders were present"） | 200 | CONFIRMED | — |
| 31 | 它爬到三萬兩千英尺 | u212 | CH2 p.70（"The U-2 flew to 32,000 feet"） | 200 | CONFIRMED | — |
| 32 | 工程師答應過八個月內飛起來，他做到了 | u213、u214 | CH2 p.70（"Kelly Johnson had met his eight-month deadline"） | 200 | CONFIRMED | — |
| 33 | 十月三日起，加州飛來的班機固定開航 | u215 | CH2 p.72（"a regularly scheduled Military Air Transport Service (MATS) flight using a USAF C-54 aircraft began on 3 October 1955"；從 Burbank 飛） | 200 | CONFIRMED | — |
| 34 | 關鍵的人星期一飛進來，星期五飛回去 | u216 | CH2 p.72（"fly the essential personnel to the site on Monday morning and return them to Burbank on Friday evening"） | 200 | CONFIRMED | — |
| 35 | 開航不到七週 | u216b | CH2 p.72（"Less than seven weeks after it started"） | 200 | CONFIRMED | — |
| 36 | 十一月十七日一架飛往基地的班機失事，機上十四個人全部罹難 | u217、u218 | CH2 p.72（"crashed on 17 November, killing all 14 persons aboard"）、CIA-2015 | 200 | CONFIRMED | — |
| 37 | 那是整個計畫死最多的一次 | u219 | CH2 p.72（"the greatest single loss of life in the entire U-2 program"） | 200 | CONFIRMED | — |
| 38 | 一架飛機要飛多高，才值得這樣藏？ | u220 | — | — | OUT OF SCOPE | — |
| 39 | 第 3 章章名「傍晚的客機上，有人看到一團火」 | seventy-thousand.chapter | CH2 p.72（"most prevalent in the early evening hours"、"to be fiery objects"） | 200 | CONFIRMED | — |
| 40 | 七萬英尺；空軍一九五三年要的就是這個高度 | u301、u302 | CH1（"By March 1953… The requirement stated that such an aircraft must have an optimum subsonic cruise speed at altitudes of 70,000 feet or higher"） | 200 | CONFIRMED | —（旁白講約數，照本片自己的規矩） |
| 41 | 卡片「70,000 英尺／這架飛機的設計高度」 | altitude-stats.stats[0] | CH1（CL-282 "maximum altitude would be just over 70,000 feet"）；第一版卡片寫「70,000+ 英尺」。卡片放精確數字是本片的規矩，這裡掉了「以上」 | 200 | CHANGED | 「70,000 英尺」→「70,000 英尺以上」 |
| 42 | 這架飛機叫 U-2，機翼又細又長 | u303 | CH1（high-aspect-ratio sailplane wing）、CH2 | 200 | CONFIRMED | — |
| 43 | 當時的客機飛一萬到兩萬英尺 | u304、altitude-stats.stats[1] | CH2 p.72 原頁（"most commercial airliners flew at altitudes between 10,000 and 20,000 feet"） | 200 | CONFIRMED | — |
| 44 | 軍用的轟炸機飛得更低 | u305 | CH2 p.72 原頁："military aircraft like the B-47s and B-57s operated at altitudes **below 40,000 feet**"——比客機的一萬到兩萬**高**，不是更低；而且和同一張卡片的 stats[2] 自相矛盾 | 200 | CHANGED | 「軍用的轟炸機飛得更低。」→「當時的軍機，四萬英尺以下。」（11 單位） |
| 45 | 卡片「40,000 英尺以下／當時的軍機」 | altitude-stats.stats[2] | CH2 p.72 原頁 | 200 | CONFIRMED | — |
| 46 | 卡片出處「CIA 計畫史 1954–1974」 | altitude-stats.data.source | 高度三欄分別出自 CH1 與 CH2 p.72，都是同一本 | 200 | CONFIRMED | — |
| 47 | 沒有人相信有人能飛到六萬英尺以上 | u306 | CH2 p.72 原頁（"At this time, no one believed manned flight was possible above 60,000 feet"） | 200 | CONFIRMED | — |
| 48 | 然後它就開始那樣飛；塔台收到的奇怪通報變多了 | u307、u308 | CH2 p.72（"once U-2s started flying at altitudes above 60,000 feet, air-traffic controllers began receiving increasing numbers of UFO reports"） | 200 | CONFIRMED | — |
| 49 | 一架往西飛的客機，天已經黑了；在客機那個高度太陽已經下去 | u309、u310 | CH2 p.72（"from pilots of airliners flying from east to west. When the sun dropped below the horizon of an airliner flying at 20,000 feet, the plane was in darkness"） | 200 | CONFIRMED | — |
| 50 | 再往上四萬英尺，機翼還曬得到太陽 | u311 | CH2 p.72（"its horizon from an altitude of 60,000 feet was considerably more distant… its silver wings would catch and reflect the rays of the sun"；"40,000 feet below"） | 200 | CONFIRMED | —（第一版查核第一輪改成「再往上」，這一版沿用對了） |
| 51 | 在客機飛行員眼裡，那是一團火 | u312 | CH2 p.72（"appear to the airliner pilot, 40,000 feet below, to be fiery objects"） | 200 | CONFIRMED | — |
| 52 | 一次目擊怎麼被消掉：寫信到代頓→請華盛頓的計畫人員核對飛行紀錄→對外說自然現象 | sighting-steps.data、u313、u314、u315 | CH2 p.73（"wrote letters to the Air Force unit at Wright Air Development Command in Dayton"；"BLUE BOOK investigators regularly **called on** the Agency's Project Staff in Washington to check reported UFO sightings against U-2 flight logs"；"linking them to natural phenomena"） | 200 | CONFIRMED | —（第一版查核第一輪拿掉的「打電話」沒有跑回來） |
| 53 | 大部分通報就這樣消掉，但不能說原因 | u316 | CH2 p.73（"eliminate the majority of the UFO reports, although they could not reveal to the letter writers the true cause"） | 200 | CONFIRMED | — |
| 54 | 還記得他們要藏的那架飛機嗎？ | u317 | — | — | OUT OF SCOPE | — |
| 55 | CIA 自己的計畫史裡有一句話：那十幾年的飛碟通報一半以上是它們；這句是史家寫的，沒有附任何統計 | u318、u319、u320 | CH2 p.73 原句（"U-2 and later OXCART flights accounted for more than one-half of all UFO reports during the late 1950s and most of the 1960s."）；腳註只引 OSA History chap. 7, pp. 17-19，沒有統計；CIA-Molly 照抄同句 | 200 | CONFIRMED | — |
| 56 | 一九五二年夏天就有過一波，比它早三年 | u321 | C-BB（Blue Book Status Report No. 8 附件：1952 年 6–9 月每日通報數）；1952→1955 | 200 | CONFIRMED | — |
| 57 | 藍皮書：一萬兩千多件、七百零一件未解、一九六九年底結案；卡片 12,618／701／1969 年 | bluebook-stats.data、u322、u323、u324 | NARA 原句（"a total of 12, 618 sightings… Of these 701 remain 'Unidentified.'"；"On December 17, 1969, the Secretary of the Air Force announced the termination"） | 200 | CONFIRMED | — |
| 58 | 結論裡有一句：沒有證據指向外星飛行器 | u325 | NARA 原句有限定語："no evidence indicating that sightings **categorized as 'unidentified'** are extraterrestrial vehicles"；旁白把限定語省掉了（第一版同樣的句子，兩輪都沒動） | 200 | CONFIRMED | —（見改動要求 R：要補限定語得多四個單位，不是必改） |
| 59 | 可是那片沙漠上飛的，已經不是它了 | u326 | — | — | OUT OF SCOPE | — |
| 60 | 第 4 章章名「一九六七年，這兩個字已經印過了」 | new-plane-1962.chapter | C-1967、Reuters | 200 | CONFIRMED | — |
| 61 | 一九六二年四月，一架新的飛機在這裡首飛 | u401 | CH6 pp.288–289（25 April 非正式短跳、26 April 官方 40 分鐘首飛、30 April「官方」首飛）；CH6 p.?（testing site at Area 51） | 200 | CONFIRMED | —（三個日期都在四月，旁白只說四月，對） |
| 62 | 它叫 A-12，設計速度三倍音速、設計高度九萬英尺，比前面那架更高更快 | u402、u403 | CH6（Mach 3.2；驗收飛行達 90,000 英尺）、CIA-Museum | 200 | CONFIRMED | — |
| 63 | 一九六七年，CIA 的一份文件提到這個地方，上面印的就是那兩個字 | u404、name-1967.data、u406 | C-1967 整頁（"Three OXCART aircraft and the necessary task force personnel will be deployed from **Area 51** to Kadena."；PD-USGov-CIA） | 200 | CONFIRMED | —（Commons 寫 1967-05-15、閱覽室寫 1967-04-01，旁白與卡片只寫年份，對） |
| 64 | 後來提出申請的人說那是無意的；不是刻意承認，只是附帶提到 | u407、u408 | Reuters（"Richelson said he could recall at least two previous government documents in which an **incidental** reference to Area 51 appeared, but he assumed those were **inadvertent**"） | 200 | CONFIRMED | — |
| 65 | 更怪的是，隔年政府自己拍了它 | u409 | C-USGS（1968-08-28）；1967→1968 | 200 | CONFIRMED | — |
| 66 | 一張一九六八年的政府航照，一直放在公開的檔案庫裡；從空中看那條跑道一清二楚 | u410、u411、u412 | C-USGS（USGS 航照，PD）、TSR（"at least two US Geological Survey aerial photographs of Groom taken in 1959 and 1968 had been available in public archives"） | 200 | CONFIRMED | — |
| 67 | 一九五九年那一批，也在同一個地方 | u411b | TSR 原文是 "at least two… aerial photographs"（兩張，不是兩批） | 200 | CHANGED（建議） | 「一九五九年那一批」→「一九五九年那一張」（15 單位） |
| 68 | 一九七四年太空站的太空人也拍了它；那趟任務只有這一個地方被交代不准拍 | u413、u414 | TSR（1974-04-19 CIA 備忘錄："There were specific instructions not to do this"、Groom "was the only location which had such an instruction"） | 200 | CONFIRMED | —（見「懷疑但沒要求改」：拍照本身的年份來源沒有寫死，任務是 1973-11 到 1974-02） |
| 69 | 事後的備忘錄只寫了一句 | u415 | TSR 引的同一份備忘錄不只一句：還寫了跨部會審查、DoD 與 NASA／國務院的不同立場、三項先例，另有 Colby 的附註 | 200 | CHANGED | 「事後的備忘錄只寫了一句。」→「事後的備忘錄裡有一句。」（10 單位） |
| 70 | 有明確的指示，不要這樣做 | u416 | TSR 原句 | 200 | CONFIRMED | — |
| 71 | 同一個時期，這裡還研究別人的飛機：弄到手的蘇聯米格機 | u417、u418 | EBB443（HAVE DOUGHNUT：以色列取得的 MiG-21，1968 年在 Area 51；HAVE DRILL／HAVE FERRY：MiG-17，1969 年在 Groom Lake） | 200 | CONFIRMED | — |
| 72 | 一九七七年，隱形驗證機第一次飛 | u419 | EBB443（HAVE BLUE "with a first flight in April 1977"；原文沒寫首飛地點，旁白也沒說） | 200 | CONFIRMED | — |
| 73 | 地點從來不是祕密；名字才是 | u420、u421 | TSR（引 Merlin「Area 51 was Never Classified」；1959／1968 航照在公開檔案庫）但同一段也寫 "The US government has at times acknowledged and at other times refused to acknowledge its existence"；research.md §0 寫的是「政府多次以 Groom Lake 附近的作業地點稱呼它」 | 200 | CHANGED（建議） | 「地點從來不是祕密。」→「地點早就不是祕密。」（8 單位，長度不變） |
| 74 | 第 5 章章名「一九八九年，電視上有人說那裡有九艘飛碟」 | twelve-years-later.chapter | KLAS-b、KNPR | 200 | CONFIRMED | —（章名自己標了「有人說」，好） |
| 75 | 十二年後，有人在電視上講這個地方 | u501 | 1977（第 72 列）→1989 | 200 | CONFIRMED | — |
| 76 | 一九八九年，拉斯維加斯的一家電視台播了訪談 | u502 | KLAS-a（"On May 15, 1989, KLAS-TV aired a live interview"）、Skeptic（"In 1989, Bob Lazar told Las Vegas reporter George Knapp…"） | 200 | CONFIRMED | — |
| 77 | 受訪的人遮著臉，用的是化名 | u503 | KLAS-b："In the interview, Lazar's face was hidden and he used a pseudonym, Dennis"；**c6 現在列的兩個網址（Skeptic、KNPR）都沒有這件事** | 200 | CONFIRMED | —（事實對；要補來源，見改動要求 S） |
| 78 | 他說他在這個地方南邊的 S-4 工作 | u504 | KLAS-b："a location called S-4 **south of Groom Lake**"；Skeptic 只寫 "near Area 51" | 200 | CONFIRMED | —（同上，要補來源） |
| 79 | 一個機棚裡停著九艘飛碟；卡片「9 艘／他說的／一個機棚裡的飛碟」 | nine-saucers.data、u505 | KNPR（"nine saucers located in a hangar"）、KLAS-b（"inside were nine flying saucers"） | 200 | CONFIRMED | —（歸屬只靠卡片的 kicker 與 u504、u508 撐著，見改動要求 Q） |
| 80 | 動力是一種叫元素一一五的東西 | u506 | Skeptic（element 115）、KNPR | 200 | CONFIRMED | —（同上） |
| 81 | 同一年稍後，他的本名公開了 | u507 | KLAS-a："It would be another seven months before the world learned the guy's real name was Bob Lazar"（1989-05-15＋7 個月，仍在 1989 年）；research.md §1.2 寫 11 月的系列 | 200 | CONFIRMED | —（同上，要補來源） |
| 82 | 這些話，一份文件都沒有 | u508 | Skeptic（核心主張 "remains unproven"）、Reuters（CIA 史裡沒有外星人） | 200 | CONFIRMED | — |
| 83 | 他說念過的兩所學校，都查不到他的紀錄 | u509 | Skeptic（"Skeptics, including ufologist Stanton Friedman, reported finding no record of him at either institution"） | 200 | CONFIRMED | —（第一版拿掉的「實驗室人事紀錄」沒有跑回來） |
| 84 | 沒想到，另一個更早的故事被接了上來 | u510 | — | — | OUT OF SCOPE | — |
| 85 | 一九四七年七月羅斯威爾陸軍機場發新聞稿說撿到飛碟，隔天改口是追蹤雷達的氣象氣球 | u511、u512、u513 | GAO 原句（"On July 8, 1947, the Roswell Army Air Field (RAAF) public information office… reported the crash and recovery of a 'flying disc.'"；"The following day… a crashed radar-tracking (weather) balloon"） | 200 | CONFIRMED | — |
| 86 | 一九九四年空軍再查了一次；最可能的來源是一個機密氣球計畫的殘骸 | u514、u515 | GAO（"In the July 1994 Report of Air Force Research… the most likely source of the wreckage was from a balloon-launched classified government project"）、NARA（1994-09-08 Widnall 聲明） | 200 | CONFIRMED | — |
| 87 | 羅斯威爾在新墨西哥；這塊地在內華達，中間隔著一千公里 | u516、u517 | GAO（New Mexico）、CH2（Nevada）；research.md 查核註寫「約 1,000 公里」。我自己算大圓距離：羅斯威爾到 Groom Lake 約 1,110 公里 | 200 | CHANGED（建議） | 「中間隔著一千公里。」→「中間隔著一千多公里。」（16 單位） |
| 88 | 殘骸運過去的紀錄，一份也沒有 | u518 | GAO 與 CH2 都沒有任何運送紀錄；是對缺席的陳述，照系列守則處理 | 200 | CONFIRMED | — |
| 89 | 這兩個故事從此黏在一起／那政府自己是怎麼稱呼這個地方的？ | u519、u520 | — | — | OUT OF SCOPE | — |
| 90 | 第 6 章章名「總統每年簽一次，卻從來不寫名字」 | september-1995.chapter | FR95、FR-API（九份都寫 "operating location near Groom Lake, Nevada"，沒有 Area 51） | 200 | CONFIRMED | — |
| 91 | 一九九五年九月總統簽了一份命令；稱呼是空軍在格魯姆湖附近的作業地點；豁免有害廢棄物的資訊揭露；理由是公開會洩露機密 | u601、u602、u603、u604 | FR95 原文（Presidential Determination No. 95-45 of September 29, 1995；"the United States Air Force's operating location near Groom Lake, Nevada"；"respecting control and abatement of solid waste or hazardous waste disposal that would require the disclosure of classified information"；42 U.S.C. 6961(a)） | 200 | CONFIRMED | — |
| 92 | 這份命令年年簽，公報上一共九份 | u607 | FR-API：1995-10-10、1996-10-08、1997-10-08、1998-10-23、1999-10-26、2000-10-05、2001-10-04、2002-12-24、2003-10-21，共 9 件，之後無 | 200 | CONFIRMED | — |
| 93 | 一九九六年，總統給國會的信把它連到一場官司 | u608 | Clinton96 原文（1996-01-31 發布、信日期 1996-01-30："to eliminate any potential uncertainty arising from a decision in pending litigation, Kasza v. Browner"） | 200 | CONFIRMED | —（但 `claims.md` 說這一版沒用這封信，見改動要求 T） |
| 94 | 五個前基地工人和兩位遺孀，告了空軍和環保署 | u609 | LVSun98 原文："Lawyers for **five current and former workers** at the base, and the widows of two workers…"；ELR（兩件 RCRA 公民訴訟，被告是空軍與 EPA） | 200 | CHANGED | 「五個前基地工人和兩位遺孀」→「五個基地工人和兩位遺孀」（19 單位） |
| 95 | 他們聲稱，基地把有害化學品放在桶裡燒 | u610 | LVSun98（"The lawsuits said employees at the base routinely put hazardous chemicals in open 55-gallon drums and burned them."） | 200 | CONFIRMED | —（「聲稱」標得對） |
| 96 | 空軍部長援用了國家機密特權 | u611 | ELR（"the Air Force's invocation of the state secrets privilege"）、LVSun98（Air Force Secretary Sheila Widnall 的未分類陳述） | 200 | CONFIRMED | — |
| 97 | 一九九八年一月，法院駁回 | u612 | ELR（9th Cir. Jan 8, 1998，"affirms the district court dismissal"）、LVSun98（"ordering dismissal of the case"） | 200 | CONFIRMED | —（嚴格說是「維持原駁回」，口語從寬，第一版同） |
| 98 | 理由是：這件事本身就是國家機密 | u613 | ELR（"because the very subject matter of the action is a state secret"） | 200 | CONFIRMED | — |
| 99 | 法院用的說法叫馬賽克理論；一片一片沒事，拼起來就洩密 | u614、u615 | ELR（"the Air Force properly employed the mosaic theory of classification"）、LVSun98（Rymer："seemingly innocuous information"／"mosaic"） | 200 | CONFIRMED | — |
| 100 | 連那裡有沒有有害廢棄物，都算機密 | u616 | LVSun98："are not entitled to learn **whether hazardous substances exist there** or how they are handled… or even the name of the base" | 200 | CONFIRMED | — |
| 101 | 同一年 CIA 出了這本史書的第一版；卡片「一九九八年的第一版」 | u617、redacted-272.data.kicker | CIA-1998："(This book is a partially redacted version of the classified original, which was **published in 1992**.)"；EBB434 也寫 1998 年出的是塗黑版。1998 年是第一個**公開**的版本，不是第一版 | 200 | CHANGED（建議） | 「這本史書的第一版」→「第一個公開的版本」；卡片 kicker 同（第一版腳本也是這樣寫的，不是這一版新造的） |
| 102 | 兩百七十二頁，只要講到這裡的句子就塗掉 | redacted-272.data、u618 | CIA-1998（"Download PDF of complete book (272 pages)"）、EBB434（2013 年新解密的就是 Area 51 的名稱、地圖、人名等） | 200 | CONFIRMED | — |
| 103 | 先記住這些塗黑的句子，等一下會回來 | u619 | — | — | OUT OF SCOPE | — |
| 104 | 兩年後俄國衛星的照片上了網；黑白的，解析度兩公尺 | u620、u621 | CBS00（2000-04-17："A U.S. company, Terraserver.com, took the photos using a Russian spy satellite in 1998"；"The panchromatic, or black-and-white, images have a 2-meter resolution"） | 200 | CONFIRMED | — |
| 105 | 那份命令，查得到的最後一份是二〇〇三年 | u621b | FR-API（最後一件 2003-10-21，之後無） | 200 | CONFIRMED | — |
| 106 | 二〇〇五年一位研究者送出申請：同一本書，塗黑少一點；然後他等 | u622、u623、u624 | EBB434（"What the CIA released in response to a 2005 Freedom of Information Act request is a substantially less redacted version…"；"FOIA request for a review of the redactions by the National Security Archive in 2005"） | 200 | CONFIRMED | — |
| 107 | 第 7 章章名「第五十八頁，是一整頁地圖」 | approved-june.chapter | CH2 PDF 第 20 頁＝書頁 58，整頁地圖（轉圖看過） | 200 | CONFIRMED | — |
| 108 | 二〇一三年六月二十五日，CIA 核准公開 | u701 | EBB434（"Document review completed and approved for release 25 June 2013"）；CH2 每頁印 Approved for Release: 2013/06/25 | 200 | CONFIRMED | — |
| 109 | 從申請到核准，整整八年 | u702 | EBB434 只寫「2005 年的申請」，沒有月份；2005-01 到 2013-06-25 之間，實際是 7 年半到 8 年半 | 200 | CHANGED（建議） | 「整整八年。」→「八年。」（8 單位） |
| 110 | 八月十五日，檔案館把它放上網 | u703 | EBB434（"Posted August 15, 2013"） | 200 | CONFIRMED | — |
| 111 | 兩版對照卡：272 頁／名字全部塗黑／沒有地圖；約 400 頁／名字印出來／第 58 頁一整頁地圖／飛行員姓名與代號 | two-editions.data | CIA-1998（272 頁）、EBB434（"names of pilots, codenames and cryptonyms, locations, funding"；"Numerous references to Area 51 and Groom Lake, with a map of the area"）、Reuters（400-page） | 200 | CONFIRMED | — |
| 112 | 舊版連地圖那一頁都沒有；新版四百多頁，名字就印在裡面 | u705、u706 | 同上；CIA 閱覽室版 406 頁、新聞另寫 407，旁白說「四百多頁」 | 200 | CONFIRMED | — |
| 113 | 第五十八頁，整頁都是地圖 | u707 | CH2 PDF 第 20 頁原圖（標題就是 Area 51，含 Groom Lake 插圖） | 200 | CONFIRMED | — |
| 114 | 右下角標著拉斯維加斯 | u707b | CH2 書頁 58 原圖：Las Vegas 在圖的右側、中間偏下（約右 73%、下 59%），右下角是 San Diego 與 Arizona | 200 | CONFIRMED | —（「右下角」偏鬆；第一版第二輪同樣判斷、同樣沒動） |
| 115 | 飛行員的姓名、代號和經費，都回來了 | u708 | EBB434（names of pilots、codenames and cryptonyms、funding） | 200 | CONFIRMED | — |
| 116 | 媒體的標題說 CIA 終於承認它存在，不太準 | u709 | EBB434 的 In The News 標題（"It's real!"、"CIA Admits to Secret Area 51"…）、TSR 同一批評 | 200 | CONFIRMED | — |
| 117 | 這樣的舊文件，他記得至少有兩份 | u710、u711 | Reuters（"at least two previous government documents"） | 200 | CONFIRMED | —（原文是「政府文件」，旁白說「這樣的舊文件」，上一句指的是 CIA 文件；差別很小，沒要求改） |
| 118 | 路透社的用詞是：第一次刻意的官方提及 | u712 | Reuters 逐字 | 200 | CONFIRMED | — |
| 119 | 還記得那些被塗黑的句子嗎？ | u713 | — | — | OUT OF SCOPE | — |
| 120 | 新版還是有很多，另一份內部的歷史也還沒公開 | u714 | EBB434：Pocock 評註列了幾十處 "still redacted"（新版還是有很多，對）；16 卷 OSA 內部史 "release was not pending"，但 CIA 閱覽室 2012-09-19 已釋出一份 24 頁、部分塗黑的 OSA HISTORY 大綱——**第一版查核第一輪就是為了這一點把「沒公開」改成「還沒全部公開」**（curio-u02/verify-1.md #75、verify-2.md #75），這一版把「全部」弄丟了 | 200 | CHANGED | 「也還沒公開。」→「也還沒全部公開。」（22 單位） |
| 121 | 還記得電視上那九艘飛碟嗎？ | u715 | — | — | OUT OF SCOPE | — |
| 122 | CIA 發言人說，讀者找不到任何外星人的字 | u716 | Reuters（Edward Price："What readers won't find are any references to aliens or other conspiracy theories…"） | 200 | CONFIRMED | — |
| 123 | 今天官方的說法，是訓練場的一部分 | u718 | AP（"the Nevada Test and Training Range"）、CIA-2015（"the commonly preferred official name for the facility today is the Nevada Test and Training Range at Groom Lake"） | 200 | CONFIRMED | — |
| 124 | 現在在試什麼，仍然是機密 | u719 | 沒有官方說法；EBB443（1977 年後的隱形機與 MiG 計畫只部分解密）；影片只說「仍是機密」 | 200 | CONFIRMED | — |
| 125 | 卡片「未結／這份檔案／名字印出來了，用途還沒有」與 u722 | unsettled.data、u722 | 同第 120、124 列 | 200 | CONFIRMED | —（沒有宣稱定論） |
| 126 | 片尾卡「一個地圖編號，等了五十八年」 | outro.data.lines[0] | 1955（CH2 p.56）→2013（EBB434） | 200 | CONFIRMED | — |
| 127 | 那個編號現在印在公開的地圖上，一小塊長方形 | u723 | CH2 pp.56–57 原頁："The outlines of Area 51 are shown on current unclassified maps as a small rectangular area adjoining the northeast corner of the much larger Nevada Test Site." | 200 | CONFIRMED | —（但這一版 `claims.md` 的 c11 把這一句刪掉了，見改動要求 V） |
| 128 | 留言題與訂閱句 | u724、u725 | — | — | OUT OF SCOPE | — |
| 129 | `sources[]` 16 條的標題、網址與 checked_on | sources[0..15] | 全部重開：16 條都 200（表上） | 200 | CONFIRMED | — |
| 130 | `loops` 三組設定與回呼、`voice`、`look`、`target_minutes` | loops、voice、look | — | — | OUT OF SCOPE | — |

合計 130 列（涵蓋抽出的 231 條）：CONFIRMED 102、CHANGED 16（必改 10、建議 6）、NOT FOUND 0、OUT OF SCOPE 12。

## 改動要求

每一條都附行 id、現在的句子、建議的句子。我沒有動 `video.json`、`claims.md`、`brief.md`、`NOTES.md`。

### 必改（事實或出處錯了）

- **A. `basin-from-above` 的 `chapter`**
  現在：`他們差一點降落在那片鹽湖上`
  改成：`他們差一點降落在那條舊跑道上`
  為什麼：CIA 史 p.56 原頁寫得很清楚——"After debating about landing on the old airstrip, LeVier set the plane
  down on the lakebed, and all four walked over to examine the strip."。鹽湖床他們**降落了**；差一點降落的是那條舊跑道。
  現在的章名把來源講反了。

- **B. `u108`**（與 A 連動）
  現在：`要是降落，飛機會往前翻。`（10 單位）
  改成：`要是降落在那條線上，飛機會往前翻。`（15 單位）
  為什麼：原文是 "If LeVier had attempted to land on **the airstrip**…"。章名改了以後，這句也要指明是那條線，
  否則仍然可以聽成「降落在鹽湖上會翻」。

- **C. `u305`**
  現在：`軍用的轟炸機飛得更低。`（10 單位）
  改成：`當時的軍機，四萬英尺以下。`（11 單位）
  為什麼：CIA 史 p.72 原句是 "military aircraft like the B-47s and B-57s operated at altitudes below 40,000 feet"——
  比前一句講的客機（一萬到兩萬英尺）**高**。現在這句不只和來源相反，還和同一張卡片的
  `altitude-stats.stats[2]`（40,000 英尺以下／當時的軍機）自相矛盾。

- **D. `u714`**
  現在：`新版還是有很多，另一份內部的歷史也還沒公開。`（20 單位）
  改成：`新版還是有很多，另一份內部的歷史也還沒全部公開。`（22 單位）
  為什麼：第一版查核第一輪就是為了這一點改過（`qdua`：「到今天沒公開」→「還沒全部公開」），第二輪再確認：
  CIA 閱覽室 2012-09-19 釋出過一份 24 頁、部分塗黑的 OSA HISTORY 大綱，Pocock 說沒釋出的是 16 卷正史。
  這一版掉了「全部」，等於把查核過的修正退回去。這一版 `claims.md` c34 自己也還寫著「還沒全部公開」。

- **E. `u609`**
  現在：`五個前基地工人和兩位遺孀，告了空軍和環保署。`（20 單位）
  改成：`五個基地工人和兩位遺孀，告了空軍和環保署。`（19 單位）
  為什麼：Las Vegas Sun 1998-01-08 原文是 "five **current and former** workers at the base"。
  這一版 `claims.md` c23 自己引的也是這一句。寫成「前基地工人」把現職的那幾位變成離職的。

- **F. `youtube.description` 第 1 段**
  現在：`一九五五年四月十二日下午，四個人坐在一架小飛機上飛過內華達`
  改成：`一九五五年四月十二日，四個人坐在一架小飛機上飛過內華達`
  為什麼：CIA 史 p.56 與 CIA 2015 年的文章都只寫日期，全文沒有 afternoon；旁白 `u101` 也只說日期。
  「下午」沒有任何來源，`claims.md` 裡也沒有這一條。

- **G. `youtube.description` 第 1 段**
  現在：`這個編號，CIA 自己的正式文件等了五十八年才印出來。`
  改成：`這個編號，CIA 自己的正式文件等了五十八年才刻意印出來。`（或「…才正式承認。」）
  為什麼：本片第 4 章自己就說 1967 年一份 CIA 正式文件已經印過這兩個字（C-1967 原件：
  "deployed from Area 51 to Kadena"）。路透社的用詞是 first **deliberate** official references。
  第一版查核第一輪正是為了同一個矛盾，把開場的「第一次把 Area 51 印在正式文件上」改成
  「才第一次正式印出 Area 51」（curio-u02/verify-1.md #21）；說明欄這一句是那個被否決的講法又回來了。
  標題「等了 58 年才正式印在文件上」有「正式」兩個字撐著，照第一版的判法留著。

- **H. `altitude-stats.stats[0].value`**
  現在：`70,000 英尺`
  改成：`70,000 英尺以上`
  為什麼：CIA 史第 1 章：空軍 1953 年的需求是 "70,000 feet or higher"，CL-282 的最大高度是
  "just over 70,000 feet"。第一版卡片寫「70,000+ 英尺」。本片自己的規矩是「旁白講約數，卡片放精確數字」，
  所以旁白 `u301`／`u302` 可以不動，卡片要把「以上」補回來。

- **I. `names-table.data.source`**
  現在：`CIA 計畫史 p.57`
  改成：`CIA 計畫史 p.57；CIA 2015 年文章`
  為什麼：表上的「夢境」＝Dreamland 是 CIA 2015 年那篇文章講的呼號（"a radio call sign for the base,
  introduced in the late 1960s"），不在計畫史 p.57。第一版卡片的出處就是兩個。

- **J. `u415`**
  現在：`事後的備忘錄只寫了一句。`（11 單位）
  改成：`事後的備忘錄裡有一句。`（10 單位）
  為什麼：The Space Review 引的 1974-04-19 備忘錄不只一句——還寫了跨部會審查的僵局、DoD 與 NASA／
  國務院各自的立場、三項先例，外加 Colby 自己的附註。「只寫了一句」把備忘錄的篇幅說死了。

### 建議（比來源稍強或稍鬆，不是硬錯）

- **K. `u113`**：`一個地圖編號，為什麼等了五十八年才印出來？` → `…才正式印出來？`（21 單位）。理由同 G。
- **L. `u702`**：`從申請到核准，整整八年。` → `從申請到核准，八年。`（8 單位）。EBB 434 只寫 2005 年提出申請，
  沒有月份，「整整」是多出來的精確度。
- **M. `u617` 與 `redacted-272.data.kicker`**：「這本史書的第一版」「一九九八年的第一版」→「第一個公開的版本」
  「一九九八年的公開版」。CIA 自己寫 1998 年版是 "a partially redacted version of the classified original,
  which was published in 1992"。（第一版腳本也是這樣寫的，不是這一版新造的錯。）
- **N. `u420`**：`地點從來不是祕密。` → `地點早就不是祕密。`（8 單位，長度不變）。TSR 同一段寫
  "The US government has at times acknowledged and at other times refused to acknowledge its existence"，
  「從來」比來源絕對。
- **O. `u517`**：`中間隔著一千公里。` → `中間隔著一千多公里。`（16 單位）。我算的大圓距離是約 1,110 公里。
- **P. `u411b`**：`一九五九年那一批` → `一九五九年那一張`。TSR 原文是 "at least two… aerial photographs"。
- **Q. `u505`／`u506`**：這兩句是旁白裡唯二把「他的聲稱」講成直述句的地方（`一個機棚裡停著九艘飛碟。`
  `動力是一種叫元素一一五的東西。`），歸屬只靠上一句 `u504` 的「他說」、卡片 kicker「他說的」和後面的
  `u508` 撐著。若長度允許，`u506` 補成 `他說動力是一種元素一一五。` 會穩一點；`u505` 旁邊就是
  kicker「他說的」，可以不動。
- **R. `u325`**：`結論裡有一句：沒有證據指向外星飛行器。` 原句有限定語——"no evidence indicating that sightings
  **categorized as 'unidentified'** are extraterrestrial vehicles"。要補得多四個單位（例如
  `結論裡有一句：未解的那些，沒有證據指向外星飛行器。`）。第一版同一句，兩輪都沒動，所以只記在這裡。

### `claims.md` 要補的（文件，不是旁白）

- **S. c6 的網址**：現在只有 Skeptic 與 KNPR，但「遮著臉」（`u503`）、「化名」（`u503`）、
  「這個地方南邊的 S-4」（`u504`）、「同一年稍後本名公開」（`u507`）四件事這兩個來源都沒有寫。
  第一版 c6 列的兩篇 KLAS 回顧（8newsnow，Wayback 20210507／20210117）才是出處，我今天重開過，200，
  內容對得上（"Lazar's face was hidden and he used a pseudonym, Dennis"、"a location called S-4 south of
  Groom Lake"、"another seven months before the world learned the guy's real name"）。請把這兩個網址補回 c6。
- **T. 「第一版有、這一版沒有講的主張」那一節**寫「c22 的柯林頓 1996-01-31 致國會信…長度取捨」，
  但 `u608`（`behind-it-a-lawsuit`）講的就是這封信，c22 的場景清單裡也有這個場景。這一條要拿掉。
- **U. c2 的括號**寫「片尾『等的是一個決定』就是這一句」，但 `video.json` 裡已經沒有這一句
  （同一份 claims 的下一節也說第三輪盲評後拿掉了）。括號要更新，否則 c2 的場景 `reuters-wording` 對不上。
- **V. c11 的條文**把第一版「它在今天的非機密地圖上是內華達試驗場東北角一小塊長方形」那一句刪掉了，
  但片尾 `u723` 還在講它。CIA 史 pp.56–57 原文支持（"shown on current unclassified maps as a small
  rectangular area adjoining the northeast corner"），請把這一句補回 c11，否則 `u723` 在表上沒有依據。
- **W. c3 的第二個網址**（npr.org）今天 curl 連線逾時（000），和第一版兩輪一樣。這一句（CIA 發言人）
  路透社那一邊是逐字的，`sources[]` 也沒有列 NPR，所以不影響影片；記在這裡供下一輪參考。

## 摘要

- 抽出 231 條主張，併成 130 列：**CONFIRMED 102、CHANGED 16（必改 10、建議 6）、NOT FOUND 0、OUT OF SCOPE 12**。
  另有兩條建議（Q、R）寫在改動要求裡，表上判 CONFIRMED。
  網路搜尋 0 次。
- 必改 10 處，涵蓋 9 個事實與出處：第 1 章章名與 `u108`（他們降落在鹽湖上，差一點降落的是舊跑道，來源被講反了）、
  `u305`（當時的軍機飛在四萬英尺以下，比客機高，不是更低）、`u714`（掉了「全部」，推翻第一版查核過的修正）、
  `u609`（current and former workers 變成「前工人」）、說明欄的「下午」（沒有來源）與
  「等了五十八年才印出來」（第一版為同一個矛盾改過一次）、卡片的「70,000 英尺」掉了「以上」、
  `names-table` 的出處漏了 CIA 2015 年文章、`u415`（備忘錄不只一句）。
- 這些錯全部出在「重講」的接縫上：章名是新寫的、`u305` 是把卡片的數字口語化時翻向、`u714` 是把長句縮短時
  掉了兩個字、`u609` 是把第一版沒有數字的句子補上人數時連帶改了身分、說明欄第 1 段是整段重寫的。
  第一版兩輪查核改過的八處裡，`7ve6`（請華盛頓的人核對）、`bxrh`（再往上四萬英尺）、`4yy9`（只講兩所學校）、
  1967 年文件只寫年份、`iqc3`（週一進週五回）都正確沿用了；只有 `qdua`（還沒全部公開）與開場那句
  「正式印出」退回去了。
- 會過期的事實：沒有新的。兩件仍懸，和第一版一樣——2003 年之後總統豁免令有沒有再簽
  （聯邦公報 API 今天仍只到 2003-10-21）、16 卷 OSA 內部史公開到什麼程度。
  說明欄「資料截至 2026-10-10」仍然成立（我今天重開，內容沒有變）。
- 意見與定論：全片沒有一句宣稱定論；`u719`「現在在試什麼，仍然是機密」與 `u722`「蓋的是未結」都誠實。
  傳說段（第 5 章）標了年份與「他說」，只有 `u505`／`u506` 的歸屬靠鄰句與卡片撐著（建議 Q）。
- 聽感（只報告，沒動）：145 句沒有一句超過 24 單位的目標，沒有括號、沒有網址、沒有「經查證」類字眼；
  沒有任何一句用 `say`／`say_for`，所以改上面的句子不會動到發音表。插圖 `prompt` 逐一看過，沒有人名、
  沒有求相似的在世人物，和說明欄第 4 段的聲明一致。
- 懷疑但沒要求改：`u707b`「右下角標著拉斯維加斯」——書頁 58 的原圖上 Las Vegas 在右側中間偏下，
  右下角是 San Diego 與 Arizona（第一版第二輪同樣判斷、同樣沒動）；`u413` 的「一九七四年」——
  The Space Review 只有 1974-04-19 的備忘錄與「recent Skylab mission」，Skylab 4 的任務是
  1973-11 到 1974-02，拍照那一刻的年份來源沒有寫死；`u201`「跑道在七月鋪好」仍是推論
  （原文只說 By July 1955 the base was ready）；`u612`「法院駁回」嚴格說是「維持原駁回」；
  `u711`「這樣的舊文件」對應路透社的 "government documents"；`u618`「只要講到這裡的句子就塗掉」
  是 EBB 434 的對照結論，不是逐句數過的。
- **第二輪：需要**（必改 10 處 > 3）。第二輪請換人，重查上面 A–J 十處與建議 K–R，再隨機抽三分之一的
  CONFIRMED；另外請核對 S–W 五項 `claims.md` 的補正有沒有做。
