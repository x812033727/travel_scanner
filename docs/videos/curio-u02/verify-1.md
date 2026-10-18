# curio-u02 查核第一輪

- 查核 2026-10-10，Claude Fable 5.1（查核代理，不是撰稿的那一個）。
- 方法：先把 `video.json` 的每句旁白、每張卡片、縮圖、標題、說明欄、標籤、`sources[]`、`assets[]` 抽成 271 條清單（`<home>\mokaair-work\videos\curio-u02\_tools\verify1\claims-list.txt`），再把 `research.md` 與 `claims.md` 列的每個網址當天用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.2 秒）重開，去掉註解後讀全文。CIA 史三章 PDF（第 1、2、6 章，30 MB）下載到 `<home>\mokaair-work\videos\curio-u02\_tools\verify1\dl\a\`，用 pdftotext 抽字；文字層壞掉的頁（p.58 地圖、p.72）用 PyMuPDF 轉成圖看原頁。網路搜尋用了 5 次中的 4 次（Kasza 案指控、OSA 內部史、Lazar 1989 年訪談日期、Los Alamos 紀錄）。
- 這是歷史題：「官方頁」指一手或權威來源。最重的是國家安全檔案館 EBB 434 的 CIA 史 2013 年解密版（Pedlow & Welzenbach，每頁印 Approved for Release: 2013/06/25）、聯邦公報、國家檔案館、GAO、EBB 443、CIA 官網；其次路透社（CSMonitor 轉載）、AP（KTVU 轉載）、NPR（Wayback）、Las Vegas Sun 1998、KLAS 的回顧、The Space Review、Skeptic、KNPR。Wikipedia 沒有用。
- 改動原則照查核提示：只改事實與連帶的地方，不動風格、順序、節奏；每句旁白維持 24 單位以內（帶 `emotion` 的 20 以內）；行 id 不變；沒有加場景或句子。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| EBB434 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/ （導言、Pocock 評註） | 200 |
| CH1 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%201.pdf （7.8 MB，有文字層） | 200 |
| CH2 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf （12.2 MB，54 頁；書頁 56–58、69–70、72–73 看過原頁） | 200 |
| CH6 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%206.pdf （10.4 MB；書頁 274、288–289） | 200 |
| CIA-RR | https://www.cia.gov/readingroom/node/1819895 、/document/0000190094 、/document/0001471747 、/node/1990206 | 200 但全部轉到閱覽室首頁：NOT OPENED |
| CIA-1998 | https://www.cia.gov/resources/csi/books-monographs/the-cia-and-the-u-2-program-1954-1974/ | 200 |
| CIA-2015 | https://www.cia.gov/stories/story/area-51-and-the-accidental-test-flight/ | 200 |
| CIA-Molly | https://www.cia.gov/stories/story/ask-molly-what-really-went-on-at-area-51/ | 200 |
| CIA-Museum | https://www.cia.gov/legacy/museum/artifact/untouchable/ | 200 |
| FR95 | https://www.govinfo.gov/content/pkg/FR-1995-10-10/html/95-25244.htm | 200 |
| FR-API | https://www.federalregister.gov/api/v1/documents.json?conditions[term]="Groom Lake"（11 筆，其中 9 筆是歷年 Determination） | 200 |
| Clinton96 | https://clintonwhitehouse6.archives.gov/1996/01/1996-01-31-determination-exempting-usaf-from-conservation-laws.html | 200 |
| GAO | https://www.govinfo.gov/content/pkg/GAOREPORTS-NSIAD-95-187/html/GAOREPORTS-NSIAD-95-187.htm | 200 |
| NARA | https://www.archives.gov/research/military/air-force/ufos | 200 |
| EBB443 | https://nsarchive.gwu.edu/briefing-book/intelligence/2013-10-29/area-51-file-secret-aircraft-soviet-MiGs | 200 |
| ELR | http://www.elr.info/litigation/kasza-v-browner （轉 https） | 200 |
| FindLaw | https://caselaw.findlaw.com/court/us-9th-circuit/1054233.html （DR v. Whitman 2003，含 Kasza 1998 的重述） | 200 |
| LVSun98 | https://lasvegassun.com/news/1998/jan/08/toxic-data-at-area-51-ruled-confidential/ | 200 |
| OpenJurist | https://openjurist.org/133/f3d/1159 （判決全文） | 403：NOT OPENED |
| Reuters | https://www.csmonitor.com/USA/Latest-News-Wires/2013/0817/Area-51-is-real-say-CIA-documents | 200 |
| NPR-13 | https://www.npr.org/sections/thetwo-way/2013/08/16/212549163/ | 000（連線被拒）；Wayback 20250919 副本 200 |
| NPR-19a | https://www.npr.org/2019/07/15/741938966/ | 000；Wayback 20250615 副本 200（`sources` 已換成這個） |
| NPR-19b | https://www.npr.org/2019/09/20/762897934/storm-area-51-fails-to-materialize | 000；Wayback 20191231 副本 200 |
| AP | https://www.ktvu.com/news/about-75-people-gather-at-area-51-gate-1-person-arrested | 200 |
| CBS00 | https://www.cbsnews.com/news/satellite-image-of-area-51/ | 200 |
| TSR | https://thespacereview.com/article/4518/1 | 200 |
| Skeptic | https://www.skeptic.com/article/the-strange-case-of-bob-lazar/ （2026-04-23） | 200 |
| KNPR | https://knpr.org/knpr/2015-02/area-51-whistleblower-speaks-ufo-conference （轉到 2015-02-12 網址） | 200 |
| KLAS-a | 8newsnow「I-Team: 25 years later」（Wayback 20210117） | 200 |
| KLAS-b | 8newsnow「I-Team: Man who detailed UFO secrets…」（Wayback 20210507） | 200 |
| FAS | http://www.fas.org/irp/overhead/groom.htm （Wayback 20160902，USGS 航照頁） | 200 |
| C-Roswell | https://commons.wikimedia.org/wiki/File:RoswellDailyRecordJuly8,1947.jpg （API） | 200 |
| C-U2 | https://commons.wikimedia.org/wiki/File:Usaf.u2.750pix.jpg （API 與整頁） | 200 |
| C-BB | https://commons.wikimedia.org/wiki/File:Appendix_I_to_Project_Blue_Book_Status_Report_Number_8_-_NARA_-_595542.jpg | 200 |
| C-USGS | https://commons.wikimedia.org/wiki/File:Area_51_28_August_1968_2.jpg | 200 |
| C-1967 | https://commons.wikimedia.org/wiki/File:CIA_BYE2369-67_page17.gif | 200 |
| C-A12 | https://commons.wikimedia.org/wiki/File:A12-flying.jpg | 200 |
| af.mil | https://www.af.mil/News/Photos/igphoto/2000544086/ （U-2 照片原頁） | Wayback 副本 200，但沒有日期與作者欄 |

## 主張表

判定：CONFIRMED 看到了／CHANGED 改了／NOT FOUND 沒看到，拿掉或換掉／OUT OF SCOPE 風格、問句、系列安排，不動。位置是行 id 或 `scene.data` 路徑；同一個事實出現在幾個地方就併成一列。

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 1 | 「51 區」這個名字 CIA 等了 58 年才正式印在文件上（1955→2013） | youtube.title、release-big-58、rka8 | Reuters（"first deliberate official references to Area 51"）、CH2 p.56（1955-04-12）、EBB434（2013） | 200 | CONFIRMED | — （「正式」＝刻意的官方承認；1967 年那一頁是附帶提及，見 #59） |
| 2 | 一個 1955 年就有的地方，CIA 正式文件到 2013 年才第一次印出「Area 51」和地圖位置；那 400 頁講的是一架飛機 | youtube.description | Reuters（400-page）、EBB434（map of the area）、Pocock 評註 P58 | 200 | CONFIRMED | — |
| 3 | 1947 羅斯威爾、1989 遮著臉的電視訪談、2019「衝進 51 區」 | youtube.description | GAO、KLAS-a（face was hidden）、AP | 200 | CONFIRMED | — |
| 4 | 1955-04-12 選址；只是地圖編號的 Area 51 | youtube.description、hook.data、site-small-plane/zybc、site-big-area51/d4kt、check-stats-answer | CH2 p.56（"On 12 April 1955"、"known by its map designation as Area 51"） | 200 | CONFIRMED | — |
| 5 | 七萬英尺的 U-2 在客機飛行員眼裡像火球 | youtube.description、silver-pilot-face/wrj7 | CH2 p.72（"fiery objects"） | 200 | CONFIRMED | — |
| 6 | CIA 史家自己寫它占了那十幾年 UFO 通報的一半以上（沒有附統計） | youtube.description、silver-quote-half、silver-historian/7awj | CH2 p.73 原句；腳註 50 只引 OSA History chap. 7；CIA-Molly 照抄 | 200 | CONFIRMED | — |
| 7 | 1995 年起的總統豁免令寫「Groom Lake 附近的空軍作業地點」 | youtube.description、secret-quote-groom、nhjp、4pj9、z7ew | FR95（原句、42 U.S.C. 6961(a)、one-year） | 200 | CONFIRMED | — |
| 8 | 2005 年申請等了八年，2013 年版印出名字和第 58 頁的地圖 | youtube.description、release-request-2005/7cqn、vr9v、release-map-page/e43u、check-big-answer | EBB434（2005 FOIA、approved 25 June 2013）、CH2 PDF 第 20 頁＝書頁 58 整頁地圖 | 200 | CONFIRMED | — |
| 9 | 1967 年的一份「備忘錄」早就印過這兩個字 | youtube.description、release-memo-1967/k9az | C-1967（頁面印 "deployed from Area 51 to Kadena"；Commons 只稱 FOIA document）；CIA-RR 打不開，文件類型未能確認 | 200／NOT OPENED | CHANGED | 備忘錄 → 文件（說明欄、k9az、卡片標題） |
| 10 | 結尾用三個問題檢查「S-4 有九艘飛碟」 | youtube.description、check-chapter | KNPR（"nine saucers located in a hangar"）、KLAS-a | 200 | CONFIRMED | — |
| 11 | 資料截至 2026-10-10；只講文件裡有的；在世人物只引述他說過的話 | youtube.description | 當天 | — | CONFIRMED | — |
| 12 | 標籤 | youtube.tags | — | — | OUT OF SCOPE | — |
| 13 | 縮圖「飛碟？是飛機」「外星與太空」「2013 年解密的檔案」 | thumbnail | EBB434 | 200 | CONFIRMED | — |
| 14 | `sources` 18 條的標題與網址 | sources[0..17] | 全部重開（表上） | 見上 | CHANGED | NPR 2019-07-15 的網址換成 Wayback 20250615 副本（npr.org 連線被拒，Wayback 開得了且內容相同） |
| 15 | 羅斯威爾日報 1947-07-08 頭版，公有領域（未續約） | assets[0]、legend-roswell-front-page | C-Roswell（PD-US-not renewed；date 1947-07-08；報頭印 TUESDAY, JULY 8, 1947、標題 RAAF Captures Flying Saucer On Ranch in Roswell Region） | 200 | CONFIRMED | — （Commons 英文描述誤寫 July 9，報頭本身是 July 8） |
| 16 | 美國空軍 U-2（TR-1）空對空照，1985 年，公有領域 | assets[1]、site-u2-photo.caption | C-U2 整頁的檔案中繼資料：Author Ken Hackman, AAVS/DOOJ；1 March 1985；PD-USGov-Military-Air Force（API 的 date 欄只寫 between 1955 and 1998） | 200 | CONFIRMED | — （`assets.source` 原本就寫 1985，沒改） |
| 17 | 藍皮書狀態報告第 8 號附件 I（NARA 595542），公有領域 | assets[2]、silver-bluebook-chart | C-BB（NARA RG 341；1952-12-31；PD-USGov；圖上 "NO. OF REPORTS PER DAY"、JUNE THROUGH SEPTEMBER 1952） | 200 | CONFIRMED | — |
| 18 | USGS 1968-08-28 航照，公有領域 | assets[3]、secret-usgs-photo.title | C-USGS（PD-USGov-USGS，來源 FAS）；FAS 頁六處寫 "28 August 1968 - USGS Aerial imagery" | 200 | CONFIRMED | — |
| 19 | CIA FOIA BYE 2369-67「第 17 頁」（1967-05-15），公有領域 | assets[4]、release-memo-1967.title | C-1967（PD-USGov-CIA；1967-05-15；檔名 page17 是 FOIA 檔的頁序，頁面上印的是 "BYE 2369-67 Page 15"） | 200 | CHANGED | 卡片標題「1967 年 5 月的 CIA 備忘錄，第 17 頁」→「1967 年 5 月 15 日的 CIA 文件」；assets.source 註明 PDF p.17、印 Page 15 |
| 20 | 美國空軍 A-12 空對空照，1960 年代，公有領域 | assets[5]、release-a12-photo | C-A12（U.S. Air Force、DVIC DF-SC-82-10542、1960s、PD-USGov-DoD） | 200 | CONFIRMED | — |
| 21 | 2013 年 CIA 第一次把 Area 51 印在正式文件上 | hook/qfsw | Reuters（first deliberate official references）；C-1967 是 CIA 正式文件、早就印了這兩個字，本片自己在 #59 也這樣講 | 200 | CHANGED | 「CIA 第一次把 Area 51 印在正式文件上」→「CIA 才第一次正式印出 Area 51」 |
| 22 | 「1955 年就有的地方，名字 2013 年才正式印出來」「CIA 自己的計畫史，約 400 頁」 | hook.data | CH2 p.56；Reuters 400 頁、CIA 閱覽室 406（未開）、新聞 407 | 200 | CONFIRMED | — |
| 23 | 你以為藏的是飛碟和外星人，其實藏的是一架飛機 | ctmu、ae9v | Reuters（CIA 發言人：U-2 與 A-12 測試場） | 200 | CONFIRMED | — |
| 24 | 內華達沙漠裡一片禁區，闖進去的人會被攔下來 | legend-sign-night/62gk | AP（arrests would be made if people tried；lethal force 警告） | 200 | CONFIRMED | — |
| 25 | 1989 年拉斯維加斯電視台播了一段訪談；一個男人遮著臉說他在那裡幫忙研究九艘飛碟 | n2e6、wbu6 | KLAS-a（1989-05-15 直播、face was hidden、pseudonym Dennis、nine flying saucers）、KNPR | 200 | CONFIRMED | — |
| 26 | 四個固定細節：外星飛碟、羅斯威爾殘骸運到這裡、反向工程九艘飛碟、元素 115；全部是聲稱 | legend-list、d2rz、ynqm、6ztw、6t64 | Reuters（Roswell 殘骸運去反向工程的 lore）、Skeptic（reverse-engineer、element 115）、KNPR | 200 | CONFIRMED | — |
| 27 | 1947-07-08 羅斯威爾陸軍機場說撿到飛碟，隔天改口是追蹤雷達用的氣象氣球 | legend-roswell-front-page/fhdd、tqzr、caption | GAO（"flying disc"／"radar-tracking (weather) balloon"） | 200 | CONFIRMED | — |
| 28 | 1994 年空軍再查，說最可能是機密氣球計畫的殘骸 | legend-balloon/n8pv | GAO（July 1994 Report of Air Force Research…"balloon-launched classified government project"） | 200 | CONFIRMED | — |
| 29 | 羅斯威爾在新墨西哥；殘骸運去內華達的紀錄一份都沒有 | legend-ranch/prxk | GAO（New Mexico）；沒有任何開到的官方文件提到運往內華達 | 200 | CONFIRMED | — （「沒有紀錄」是對缺席的陳述，照系列守則標為傳說） |
| 30 | 2019 年臉書玩笑活動約大家衝進 51 區 | legend-storm-road/3ify | NPR-19a（tongue-in-cheek Facebook call）、AP（internet hoaxster） | 200 | CONFIRMED | — |
| 31 | 7 月中按參加超過 100 萬 | legend-storm-stats、hmvs | NPR-19a（Monday 2019-07-15 exceeded 1 million） | 200 | CONFIRMED | — |
| 32 | 9 月 20 日清晨到大門口的「數十人」：AP 約 75、NPR 約 40 | legend-storm-stats、74zr | AP（About 75 people arrived early Friday）、NPR-19b（about 40 people gathered at the gates） | 200 | CONFIRMED | — |
| 33 | 前一晚附近小鎮的派對約 1,500 人，郡警估計 | legend-storm-stats、yrfh | AP（Sheriff Kerry Lee estimated late Thursday about 1,500 at the festival sites） | 200 | CONFIRMED | — |
| 34 | 這些說法沒有任何一份文件 | legend-no-paper/mvsb | Skeptic（remains unproven）、Reuters（CIA 史無外星人） | 200 | CONFIRMED | — |
| 35 | 直到 2013 年 CIA 自己的計畫史解密，約 400 頁，第一次正式印出 Area 51 | legend-big-2013、3vip | EBB434、Reuters | 200 | CONFIRMED | — |
| 36 | 1955 年美國要一架飛得很高的飛機；設計目標七萬英尺以上 | imdu、site-u2-photo/fss6、caption | CH1（1953 年需求書 "70,000 feet or higher"；CL-282 "just over 70,000 feet"） | 200 | CONFIRMED | — |
| 37 | 四月十二日負責人坐小飛機飛過內華達找地方；鹽湖旁一條像跑道的直線 | zybc、er8k | CH2 p.56（Bissell、Ritland、Johnson，LeVier 駕 Beechcraft；airstrip by a salt flat known as Groom Lake） | 200 | CONFIRMED | — |
| 38 | 天上看像鋪過，踩下去陷到腳踝的土；真的降落飛機會翻過去，計畫的人全在上面 | csek、4ijy | CH2 p.56（ankle-deep dust；nosed over…killing or injuring all of the key figures） | 200 | CONFIRMED | — |
| 39 | 回到華盛頓才發現那片地不在原子能委員會試驗場裡；請委員會劃進來，艾森豪批准 | kvtk、hq9j、site-big-area51.sub | CH2 p.56（文字層破損，Reuters 與 CIA-2015 逐句引同段）、EBB443 導言 | 200 | CONFIRMED | — |
| 40 | 今天地圖上是試驗場東北角一小塊長方形 | site-big-area51.sub | CH2 p.57（small rectangular area adjoining the northeast corner） | 200 | CONFIRMED | — |
| 41 | 三個名字：Area 51（地圖編號，1955）、天堂牧場（強森取的，1955）、夢境（無線電呼號，60 年代末） | site-names-table、p7zb、ngai、ez3c | CH2 p.57（Paradise Ranch→the Ranch）、CIA-2015（Dreamland＝1960 年代末起的呼號，據 TD Barnes） | 200 | CONFIRMED | — |
| 42 | 七月跑道鋪好、基地可用、人陸續搬進去 | site-runway-july/5vb9 | CH2 p.57（"By July 1955 the base was ready, and…personnel began moving in"；鋪跑道是"decided…was needed"） | 200 | CONFIRMED | — （「鋪好了」是合理推論，見聽感） |
| 43 | 要在這裡試飛的飛機叫 U-2 | cc7z | CH2 | 200 | CONFIRMED | — |
| 44 | 時間軸 4/12 選址、8/1 滑行測試意外離地、8/4 第一次計畫內飛行、8/8「官方」首飛到 32,000 英尺 | site-steps-first-flights、mjcy、9x6y、fc3a、3xn7 | CH2 pp.69–70 逐句；CIA-2015 同 | 200 | CONFIRMED | — |
| 45 | 試飛員事後說他根本沒打算飛，人就在空中了 | site-test-pilot/dmpa | CH2 p.69（"I had no intentions whatsoever of flying"） | 200 | CONFIRMED | — |
| 46 | 設計的人答應過八個月內飛起來，他做到了 | site-engineer-deadline/eb8q | CH2 p.70（"Kelly Johnson had met his eight-month deadline"） | 200 | CONFIRMED | — |
| 47 | U-2 設計高度 70,000+ 英尺（約 21 公里）；1950 年代中客機 10,000–20,000；軍機 B-47、B-57 在 40,000 以下 | silver-stats-altitude、7btc、hnbv | CH1；CH2 p.72 | 200 | CONFIRMED | — （21.3 公里是換算） |
| 48 | 那時沒有人相信有人能飛到六萬英尺以上 | edmc | CH2 p.72 原頁（"no one believed manned flight was possible above 60,000 feet"） | 200 | CONFIRMED | — |
| 49 | 傍晚往西飛的客機天已經黑了；U-2 在上面四萬英尺還曬得到太陽 | 2xtp、bxrh、silver-steps-sighting | CH2 p.72（airliner 20,000、U-2 60,000、"40,000 feet below"） | 200 | CHANGED | 「上面四萬英尺的 U-2」→「再往上四萬英尺的 U-2」（原句可聽成 U-2 飛四萬英尺） |
| 50 | 飛行員通報塔台，有人寫信給空軍；信寄到代頓的調查單位；藍皮書計畫 | wmx4、silver-steps、ydx7 | CH2 p.73（Wright Air Development Command in Dayton；Operation BLUE BOOK；Wright-Patterson） | 200 | CONFIRMED | — （CIA 史寫 Operation，正式名 Project，卡片用「藍皮書」不涉） |
| 51 | 1952 年夏天的通報圖，那時 U-2 還沒出生；U-2 試飛後通報大幅增加 | silver-bluebook-chart、vjea、2kvi、caption | C-BB（1952 年 6–9 月每日通報數）；CH2 p.72（"tremendous increase"） | 200 | CONFIRMED | — |
| 52 | 藍皮書 1947–1969 共 12,618 件，701 件仍列未解，1969-12-17 宣布結束，結論沒有證據指向外星飛行器 | silver-bluebook-stats、e4ic、5v2r、4qzc | NARA 原句 | 200 | CONFIRMED | — |
| 53 | 引言 "U-2 and later OXCART flights accounted for more than one-half of all UFO reports during the late 1950s and most of the 1960s." p.73 | silver-quote-half、5civ | CH2 p.73 逐字 | 200 | CONFIRMED | — |
| 54 | 調查員打電話去華盛頓核對 U-2 飛行紀錄 | silver-phone-check/7ve6 | CH2 p.73（"regularly called on the Agency's Project Staff in Washington to check…against U-2 flight logs"＝請託核對，沒有電話） | 200 | CHANGED | 「調查員打電話去華盛頓」→「調查員請華盛頓的計畫人員」 |
| 55 | 大部分通報就這樣消掉，但不能告訴寫信的人為什麼；回覆是「自然現象」 | w94n、9tra、silver-steps | CH2 p.73（eliminate the majority…could not reveal to the letter writers the true cause；linking them to natural phenomena） | 200 | CONFIRMED | — （「回覆四個字」是推論，見聽感） |
| 56 | 政府承認有這個地方，只是不說名字 | secret-chapter/6udd | FR95（Groom Lake 這個地名寫出來了，沒有 Area 51）、Clinton96 | 200 | CONFIRMED | — |
| 57 | 工人不住在那裡，從加州搭定期班機進出 | secret-commute-plane/iqc3 | CH2 p.72（essential personnel 週一早上飛進、週五晚上飛回 Burbank；MATS 定期班機 1955-10-03 開航） | 200 | CHANGED | 「工人不住在那裡，從加州搭定期班機進出」→「工人搭定期班機進出，週一從加州飛來，週五飛回」 |
| 58 | 1955 年 11 月一架班機失事，14 人罹難 | secret-crash-wreath/f9zc | CH2 p.72（17 November、all 14 persons、greatest single loss）；CIA-2015 | 200 | CONFIRMED | — |
| 59 | 1995 年起總統每年簽豁免令；公報上查得到的至少到 2003 年 | z7ew、tkbk、secret-every-year | FR95；FR-API 列 1995、96、97、98、99、2000、01、02、03 共 9 件，之後無；EBB443 Doc 9（Bush 2003-09-16） | 200 | CONFIRMED | — |
| 60 | 背景是一場官司，前基地工人聲稱那裡露天燒有害廢棄物 | secret-widow-steps/zczm | LVSun98（five current and former workers 與兩位遺孀；open 55-gallon drums and burned them）、ELR | 200 | CONFIRMED | — |
| 61 | 1998 年法院駁回，理由是這件事本身就是國家機密；馬賽克理論 | secret-gavel/2if2、secret-mosaic/km7k | ELR（9th Cir. 1998-01-08；"the very subject matter of the action is a state secret"；mosaic theory）、FindLaw 重述 | 200 | CONFIRMED | — |
| 62 | 同一年 CIA 出了這本史書的第一版，272 頁；提到 Area 51 的字句全部塗黑；原版 1992 年寫成 | secret-1998-book/fnxk、secret-big-272、3ink | CIA-1998（1998、272 pages、partially redacted version of the classified original published in 1992）、EBB434（Area 51 references newly declassified）、Pocock | 200 | CONFIRMED | — |
| 63 | 1968 年的政府航照一直放在公開的檔案庫裡；跑道和機棚清清楚楚 | secret-usgs-photo、gkzc、64nc | TSR（USGS 1959、1968 航照 "available in public archives"）、FAS 頁、照片本身 | 200 | CONFIRMED | — |
| 64 | 1974 年太空站太空人違反指示拍了它；備忘錄寫那趟任務只有這個地方被交代不准拍 | secret-skylab/6cpb、secret-memo-analyst/i4if | TSR（CIA 1974-04-19 memo："There were specific instructions not to do this"、"the only location which had such an instruction"） | 200 | CONFIRMED | — （單一來源，但引 CIA 備忘錄原句） |
| 65 | 2000 年俄國衛星照片被放上網，兩公尺解析度 | secret-satellite-2000/7ac8 | CBS00（2000-04-17；Russian spy satellite 1998；2-meter resolution；Terraserver） | 200 | CONFIRMED | — |
| 66 | 1998 年版 vs 2013 年版：272 頁／約 400 頁、Area 51 全塗黑／印出、沒有地圖／第 58 頁整頁地圖、姓名塗黑／姓名代號經費恢復 | secret-compare-versions、amji、583d、release-pilot-glove/sdcw | CIA-1998、EBB434（names of pilots、cryptonyms、funding、map）、Pocock P58 | 200 | CONFIRMED | — |
| 67 | 2013-06-25 CIA 核准公開；8 月 15 日國家安全檔案館放上網，媒體都報了 | release-approved/e6xb、release-published/e5rz、check-stats-answer | EBB434（Posted August 15, 2013；approved for release 25 June 2013；In The News 列 16 家） | 200 | CONFIRMED | — |
| 68 | 標題都說 CIA 終於承認 51 區存在，這樣講不太準 | release-memo-1967/hjrh | EBB434 In The News 標題（"It's real!"、"CIA Admits"）；TSR 同一批評 | 200 | CONFIRMED | — |
| 69 | 路透社：第一次刻意的、官方的提及；申請人說第一次有高層決定承認名字和位置 | release-quote-reuters、wi7t、wsg8 | Reuters 逐字（兩句） | 200 | CONFIRMED | — |
| 70 | 第 58 頁整頁地圖，右下角標拉斯維加斯 | release-map-page/e43u | CH2 PDF 第 20 頁原圖（Las Vegas、Indian Springs 在內華達南端右下） | 200 | CONFIRMED | — |
| 71 | 一位英國史家說這些新內容他的書早就寫過 | release-bookshop/v2vq | EBB434 Pocock："nearly all of the newly-released information is already in my books" | 200 | CONFIRMED | — |
| 72 | CIA 發言人說讀者找不到任何關於外星人的字 | release-spokesman-page/p3ma | Reuters（Edward Price 原句） | 200 | CONFIRMED | — |
| 73 | A-12 1962 年在這裡首飛；三倍音速、九萬英尺 | release-a12-photo、wyp5、4ccd、caption | CH6 pp.288–289（4/25 非正式、4/26、4/30 官方）、Mach 3.2／90,000；CIA-Museum Mach 3.29 | 200 | CONFIRMED | — |
| 74 | 之後是弄到手的蘇聯米格機，和 77 年的隱形驗證機 | release-mig/fn2f、check-compare | EBB443（HAVE DOUGHNUT MiG-21 1968、HAVE DRILL/FERRY MiG-17 1969 at Area 51；HAVE BLUE first flight April 1977） | 200 | CONFIRMED | — （EBB443 沒明寫 HAVE BLUE 在 51 區首飛，旁白也沒說地點） |
| 75 | 新版還是有很多塗黑；內部的另一份歷史到今天沒公開 | release-still-redacted/qdua | Pocock（16 卷 OSA history 已申請、CIA 說 release not pending，2013）；CIA 閱覽室後來有部分塗黑的 OSA 歷史文件（搜尋可見，閱覽室當天打不開） | 200／NOT OPENED | CHANGED | 「到今天沒公開」→「還沒全部公開」 |
| 76 | 三個問題：最早出處 1989 年電視訪談；他自己說的，先化名遮臉、同年稍後具名；沒有任何文件、2013 年解密後仍沒有外星人 | check-steps-three、xtkt、c8jp、6jcd | KLAS-b（1989-05-15、"Dennis"、"another seven months before the world learned the guy's real name"）、KLAS-a、Reuters | 200 | CONFIRMED | — |
| 77 | 他說念過的兩所學校查無紀錄；實驗室也查不到人事資料 | check-empty-drawers/4yy9 | Skeptic（MIT、Caltech "no record of him at either institution"）；Los Alamos 人事紀錄一句在開到的來源裡找不到一手出處（Skeptic 反寫 1982 年當地報紙稱他 physicist；其餘只有維基） | 200 | CHANGED | 「他說念過的兩所學校查無紀錄，實驗室也查不到人事資料」→「他說念過的兩所學校，都查無他的就學紀錄」 |
| 78 | 25 年後他說真希望當年沒接受那次訪談 | check-regret/ggmd | KNPR 2015-02-12（25-year anniversary interview："wished he had never done the interview"）、KLAS-a 同 | 200 | CONFIRMED | — |
| 79 | 大家以為的 vs 文件裡的（U-2 1955、A-12 1962、米格機與隱形驗證機、2013 年約 400 頁） | check-compare-believed-record、ydye、v24x | 同 #4、#73、#74、#2 | 200 | CONFIRMED | — |
| 80 | 我的看法：政府藏的多半是自己的飛機；故事的數量不是證據；不笑相信的人、不替政府背書 | check-own-plane/2nea、9v4v、ktc6 | brief.md 站主觀點 | — | OUT OF SCOPE | — （標成意見，與站主觀點一致） |
| 81 | 現在在裡面試什麼還是機密；官方只叫它訓練場的一部分 | check-training-range/ew6b | AP（Nevada Test and Training Range）、CIA-2015（NTTR at Groom Lake）、EBB443（partly declassified） | 200 | CONFIRMED | — |
| 82 | 三個年份卡 1955／2005／2013 | check-stats-answer、s22u、n5uk、75dq | 同 #4、#8、#67 | 200 | CONFIRMED | — |
| 83 | 不是突然承認，是有人問了八年 | check-big-answer/5j56 | EBB434（2005→2013） | 200 | CONFIRMED | — |
| 84 | 留言題、下一份檔案麥田圈、訂閱 | 28pp、outro | brief.md | — | OUT OF SCOPE | — |
| 85 | 章名七條 | *.chapter | 同各章 | — | CONFIRMED | — |

合計：85 列（涵蓋清單 271 條）。CONFIRMED 73、CHANGED 9（其中事實 8：#9、#19、#21、#49、#54、#57、#75、#77；#14 是來源網址維護）、NOT FOUND 0（找不到的都併進 CHANGED 處理）、OUT OF SCOPE 3。

## 摘要

- 查了 85 列（271 條抽出的主張）：確認 73、改了 9（事實 8＋來源網址 1）、沒找到而拿掉的細節 2（Los Alamos 人事紀錄、第 17 頁，併在改了裡）、不在範圍 3。
- 事實修改 8 處：`qfsw`（開場「印在正式文件上」→「正式印出」）、`iqc3`（工人週一來週五回，不是「不住在那裡」）、`7ve6`（「打電話」→「請華盛頓的計畫人員」）、`qdua`（OSA 內部史「到今天沒公開」→「還沒全部公開」）、`4yy9`（拿掉實驗室人事紀錄）、1967 年文件的頁碼（印 Page 15，不是第 17 頁）、1967 年文件的類型（備忘錄→文件，三處）、`bxrh`（「上面四萬英尺」→「再往上四萬英尺」）。
- 會過期的事實：沒有近期會過期的；兩件懸而未決——2003 年之後總統豁免令有沒有再簽（聯邦公報到 2003-10-21 為止，EBB 443 的最後一件是 2003-09-16）、OSA 內部史公開到什麼程度（CIA 閱覽室當天打不開）。說明欄「資料截至 2026-10-10」正確。
- 來源與企劃衝突：沒有。企劃的「不講 F-117 首飛地點」「A-12 首飛只說 1962 年 4 月」「到場人數給範圍」都照辦了。
- 意見：三句意見（`2nea`、`9v4v`、`ktc6`）都標成「我的看法」且與 `brief.md` 站主觀點一致，沒有不符。
- 聽感（只報告）：沒有超過 40 字的句子，沒有括號或網址，沒有「經查證」類字眼；Latin 詞 Area 51、CIA、U-2、A-12、S-4 都在發音字典；reveal 都在介紹句之後。`9tra`「回覆是自然現象四個字」與 `5vb9`「跑道鋪好了」是合理推論，原文分別只寫「linking them to natural phenomena／could not reveal the true cause」與「decided that a paved runway was needed…By July 1955 the base was ready」；lint 的 outro 警告（只有一句）是撰稿照 H01 經驗刻意留的。
- lint：`node tools/video/cli.mjs lint --slug curio-u02` 0 錯誤、1 警告（outro，原本就有）；估 11.2 分鐘、126 句。改句後 `youtube.description` 組合曾到 5,075 位元組，把 Wayback 網址縮成不帶 slug 的短形（curl 驗證會轉到同一份快照）後回到上限內。
- 懷疑但沒動：標題與 `hook.data`「正式印在文件上／正式印出來」與 1967 年那一頁的張力，靠「正式」兩字撐著，站主可考慮改成「正式承認」；BYE 2369-67 很可能真是給 303 委員會的備忘錄，但閱覽室打不開，先用「文件」；Skeptic 2026 這篇對 Lazar 偏同情，本片只取它承認的「兩校無紀錄、核心主張未證實」兩點；KNPR 稱 Lazar 為「在該基地工作的物理學家」是 KNPR 的措辭，本片沒有重複；Commons 的羅斯威爾檔案英文描述寫 July 9，報頭本身印 July 8；說明欄「那 400 頁」用路透社的數字，CIA 閱覽室版 406 頁、新聞另有 407；`photos/u2-nasa-1960.jpg` 下載了但沒登記在 `assets`、也沒用到。
- 第二輪：需要（事實修改 8 處 > 3）。第二輪請重查 #9、#19、#21、#49、#54、#57、#75、#77 這八處，加上確認列的隨機三分之一；CIA 閱覽室若換個時段或換 User-Agent 開得了，優先補 DOC_0001471747 的文件類型與 OSA 歷史的釋出狀態。
