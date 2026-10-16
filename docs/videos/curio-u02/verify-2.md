# curio-u02 查核第二輪

- 查核 2026-10-10，Claude Fable 5.1（第二輪查核代理；不是撰稿的那一個，也不是第一輪查核的那一個）。
- 範圍照查核提示的最後一段：第一輪改過或拿掉的全部重查（verify-1.md 的 #9、#14、#19、#21、#49、#54、#57、#75、#77），加上第一輪確認列的隨機三分之一。抽樣用 `<home>\mokaair-work\videos\curio-u02\_tools\verify2\sample.py`，種子 `20261010`，從 73 列確認中抽 25 列（結果存 `sample.txt`）。另外自己把 `video.json` 重新抽成 381 條主張清單（`claims-list.txt`），對照時順手多看了一列（#70 地圖）。
- 方法：所有來源當天重開（curl，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.2 秒，`fetch.py`）。CIA 史三章 PDF（第 1、2、6 章，30 MB）重新下載到 `<home>\mokaair-work\videos\curio-u02\_tools\verify2\dl\a\`，pdftotext 抽字；文字層破損的頁（書頁 56 下半、58 地圖、72 下半）用 PyMuPDF 轉成圖逐字讀。CIA 閱覽室 curl 仍全部轉回首頁，改用內建瀏覽器開，開得了（見下）。網路搜尋用了 5 次中的 1 次（"BYE 2369-67"）。
- 改動原則：只改事實與連帶的地方；行 id 不變；沒加場景或句子；沒動旁白。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| EBB434 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/ | 200 |
| CH1 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%201.pdf （7.8 MB） | 200 |
| CH2 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf （12.2 MB，55 頁；書頁 56–58、69–70、72–73 逐字讀） | 200 |
| CH6 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%206.pdf （10.4 MB；書頁 278、288–290、297） | 200 |
| CIA-RR（curl） | https://www.cia.gov/readingroom/document/0001471747 、/document/0000190094 、/node/1819895 、/docs/DOC_0001471747.pdf | 200 但全部轉到閱覽室首頁 |
| CIA-RR（內建瀏覽器） | https://www.cia.gov/readingroom/document/0001471747 （文件頁開得了）；PDF 連結跳出存檔對話框，沒有下載；逐頁 GIF（Commons 標的 0001471747_0017.gif 那套）已 404 | 200／未下載／404 |
| CIA-RR-OSA（內建瀏覽器） | https://www.cia.gov/readingroom/search/site/%22OSA%20history%22 （22 筆）；https://www.cia.gov/readingroom/document/cia-rdp90b00184r000100010008-0 | 200 |
| CIA-1998 | https://www.cia.gov/resources/csi/books-monographs/the-cia-and-the-u-2-program-1954-1974/ | 200 |
| CIA-2015 | https://www.cia.gov/stories/story/area-51-and-the-accidental-test-flight/ | 200 |
| CIA-Molly | https://www.cia.gov/stories/story/ask-molly-what-really-went-on-at-area-51/ | 200 |
| CIA-Museum | https://www.cia.gov/legacy/museum/artifact/untouchable/ | 200 |
| FR95 | https://www.govinfo.gov/content/pkg/FR-1995-10-10/html/95-25244.htm | 200 |
| FR-API | https://www.federalregister.gov/api/v1/documents.json?conditions[term]="Groom Lake"（11 筆，9 筆是 1995–2003 的 Determination，之後無） | 200 |
| Clinton96 | https://clintonwhitehouse6.archives.gov/1996/01/1996-01-31-determination-exempting-usaf-from-conservation-laws.html | 200 |
| GAO | https://www.govinfo.gov/content/pkg/GAOREPORTS-NSIAD-95-187/html/GAOREPORTS-NSIAD-95-187.htm | 200 |
| NARA | https://www.archives.gov/research/military/air-force/ufos | 200 |
| EBB443 | https://nsarchive.gwu.edu/briefing-book/intelligence/2013-10-29/area-51-file-secret-aircraft-soviet-MiGs | 200 |
| ELR | https://www.elr.info/litigation/kasza-v-browner | 200 |
| FindLaw | https://caselaw.findlaw.com/court/us-9th-circuit/1054233.html | 200 |
| LVSun98 | https://lasvegassun.com/news/1998/jan/08/toxic-data-at-area-51-ruled-confidential/ | 200 |
| Reuters | https://www.csmonitor.com/USA/Latest-News-Wires/2013/0817/Area-51-is-real-say-CIA-documents | 200 |
| NPR-13、NPR-19a | npr.org 兩條 | 000（連線被拒）：NOT OPENED |
| NPR-19a-WB | https://web.archive.org/web/20250615143117/https://www.npr.org/2019/07/15/741938966/ | 200 |
| NPR-19b-WB | https://web.archive.org/web/20191231164552/https://www.npr.org/2019/09/20/762897934/storm-area-51-fails-to-materialize | 200 |
| AP | https://www.ktvu.com/news/about-75-people-gather-at-area-51-gate-1-person-arrested | 200 |
| CBS00 | https://www.cbsnews.com/news/satellite-image-of-area-51/ | 200 |
| TSR | https://thespacereview.com/article/4518/1 | 200 |
| Skeptic | https://www.skeptic.com/article/the-strange-case-of-bob-lazar/ | 200 |
| KNPR | https://knpr.org/knpr/2015-02/area-51-whistleblower-speaks-ufo-conference | 200 |
| KLAS-a、KLAS-b | 8newsnow 兩篇回顧（Wayback 20210117、20210507） | 200 |
| FAS | http://www.fas.org/irp/overhead/groom.htm （Wayback 20160902） | 200 |
| C-* | Commons API（六張圖的 extmetadata）＋ U-2 與 1967 年文件的整頁 | 200 |

## 主張表

判定：CONFIRMED 看到了／CHANGED 改了／NOT FOUND 沒看到／OUT OF SCOPE 不動。編號沿用 verify-1.md，方便對照。

### 第一輪改過或拿掉的（九列全部重查）

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 9 | 1967 年的一份「文件」早就印過這兩個字（第一輪由「備忘錄」改來） | youtube.description、release-memo-1967/k9az | CIA-RR（內建瀏覽器）：文件頁標題 "OXCART RECONNAISSANCE OF NORTH VIETNAM (W/ATTACHMENT)"，Document Type: FOIA，收在 "A-12 OXCART Reconnaissance Aircraft Documentation"，23 頁；照片那一頁頁首印 "II. OXCART RECONNAISSANCE OPERATIONS PLAN"、"BYE 2369-67 Page 15"、"deployed from Area 51 to Kadena"；PDF 本身要下載才看得到（存檔對話框，未下載），封面是不是備忘錄仍未親見 | 200 | CONFIRMED | — （「文件」維持；它是一份 23 頁、附件是作戰計畫的 FOIA 文件，這樣講沒錯） |
| 14 | `sources` 18 條的標題與網址 | sources[0..17] | 全部重開（表上）：17 條 200；npr.org 仍拒絕連線，`sources` 已是 Wayback 副本（200，內容同） | 見上 | CONFIRMED | — |
| 19 | 1967 年文件的卡片標題與圖片出處（第一輪改成「1967 年 5 月 15 日的 CIA 文件」） | assets[4]、release-memo-1967.title | C-1967（Date 1967-05-15、Author CIA (Richard Helms)、PD）；CIA-RR 文件頁 Publication Date 寫 **April 1, 1967**，和 Commons 的 5 月 15 日不一致 | 200 | CHANGED | 卡片標題「1967 年 5 月 15 日的 CIA 文件」→「1967 年的 CIA 文件：OXCART 偵察北越的計畫」（日期只留年份，補上閱覽室的文件名與頁面自己的標題）；assets.source →「Wikimedia Commons / CIA FOIA DOC_0001471747, 1967, PDF p.17, printed Page 15」（說明欄組合上限 5,000 位元組，寫長會爆） |
| 21 | 2013 年 CIA 才第一次「正式印出」Area 51 | hook/qfsw | Reuters："the 400-page CIA history contains the first deliberate official references to Area 51"；同篇 Richelson 說他記得至少兩份舊文件附帶提過 Area 51，他認為是無意的（incidental、inadvertent）；TSR 也說 2013 年新的是第一次承認「具體活動」（U-2 試飛） | 200 | CONFIRMED | — |
| 49 | 兩萬英尺的客機已入夜；再往上四萬英尺的 U-2（六萬英尺）還曬得到太陽 | 2xtp、bxrh、silver-steps-sighting | CH2 p.72 原頁（轉圖讀）："airliner flying at 20,000 feet … its horizon from an altitude of 60,000 feet was considerably more distant … appear to the airliner pilot, 40,000 feet below, to be fiery objects" | 200 | CONFIRMED | — |
| 54 | 調查員請華盛頓的計畫人員核對 U-2 飛行紀錄（第一輪拿掉「打電話」） | silver-phone-check/7ve6 | CH2 p.73："BLUE BOOK investigators regularly called on the Agency's Project Staff in Washington to check reported UFO sightings against U-2 flight logs"（called on＝請託，沒有電話） | 200 | CONFIRMED | — （插圖提示詞仍畫一支電話，見聽感） |
| 57 | 工人搭定期班機進出，週一從加州飛來，週五飛回 | secret-commute-plane/iqc3 | CH2 p.72 原頁："fly the essential personnel to the site on Monday morning and return them to Burbank on Friday evening … a regularly scheduled Military Air Transport Service (MATS) flight … began on 3 October 1955" | 200 | CONFIRMED | — |
| 75 | 新版還是有很多塗黑；內部的另一份歷史「還沒全部公開」 | release-still-redacted/qdua | EBB434 Pocock 評註（P11 footnote）：16 卷 OSA history 已申請，CIA 說 release "not pending"；CIA-RR 搜尋 "OSA history" 22 筆，多是 1968 年籌備寫史的備忘錄，標題就叫 OSA HISTORY 的只有一份 24 頁大綱（Declassified in Part，2012-09-19 釋出），不是 16 卷正史 | 200 | CONFIRMED | — |
| 77 | 他說念過的兩所學校都查無就學紀錄（第一輪拿掉「實驗室查不到人事資料」） | check-empty-drawers/4yy9 | Skeptic：MIT、Caltech "reported finding no record of him at either institution"；同篇反而寫 1982 年 Los Alamos Monitor 稱他為 Los Alamos Meson Physics Facility 的 physicist，所以拿掉實驗室那句是對的 | 200 | CONFIRMED | — |

### 第一輪確認列的隨機三分之一（種子 20261010，25 列）

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 1 | 「51 區」這個名字 CIA 等了 58 年才正式印在文件上（1955→2013） | youtube.title、release-big-58、rka8 | CH2 p.56（12 April 1955）；EBB434（approved 25 June 2013）；Reuters（first deliberate official references）；2013−1955＝58 | 200 | CONFIRMED | — |
| 6 | CIA 史家自己寫它占了那十幾年 UFO 通報的一半以上，沒附統計 | youtube.description、silver-quote-half、silver-historian/7awj | CH2 p.73 原句，腳註 50 只引 "OSA History, chap. 7, pp. 17-19"；CIA-Molly 照抄同句 | 200 | CONFIRMED | — |
| 13 | 縮圖「飛碟？是飛機」「外星與太空」「2013 年解密的檔案」 | thumbnail | EBB434（2013 年解密）；Reuters（CIA 發言人：U-2 與 A-12） | 200 | CONFIRMED | — |
| 16 | 美國空軍 U-2（TR-1）空對空照，1985 年，公有領域 | assets[1]、site-u2-photo.caption | C-U2 整頁檔案中繼資料：Ken Hackman, AAVS/DOOJ；1 March 1985；PD（API 的 date 欄仍只寫 between 1955 and 1998） | 200 | CONFIRMED | — |
| 24 | 內華達沙漠裡一片禁區，闖進去的人會被攔下來 | legend-sign-night/62gk | AP："lethal force could be used if people entered the Nevada Test and Training Range, and local and state officials said arrests would be made if people tried" | 200 | CONFIRMED | — |
| 26 | 四個固定細節：外星飛碟、羅斯威爾殘骸運到這裡、反向工程九艘飛碟、元素 115；全部是聲稱 | legend-list、d2rz、ynqm、6ztw、6t64 | Reuters（Roswell 殘骸運到這裡反向工程的 lore）；KLAS-a（nine flying saucers）；KNPR（nine saucers）；Skeptic（reverse-engineer、element 115、"remains unproven"） | 200 | CONFIRMED | — |
| 28 | 1994 年空軍再查，說最可能是機密氣球計畫的殘骸 | legend-balloon/n8pv | GAO："In the July 1994 Report of Air Force Research … the most likely source of the wreckage was from a balloon-launched classified government project" | 200 | CONFIRMED | — |
| 31 | 7 月中按參加超過 100 萬 | legend-storm-stats、hmvs | NPR-19a-WB："On Monday, the number of people who signed up for the tongue-in-cheek Facebook call to 'Storm Area 51' exceeded 1 million"（2019-07-15） | 200 | CONFIRMED | — |
| 34 | 這些說法沒有任何一份文件 | legend-no-paper/mvsb | Skeptic（central claim "remains unproven"）；Reuters（CIA 發言人：找不到外星人） | 200 | CONFIRMED | — |
| 35 | 直到 2013 年 CIA 自己的計畫史解密，約 400 頁，第一次正式印出 Area 51 | legend-big-2013、3vip | EBB434；Reuters（400-page、first deliberate official references） | 200 | CONFIRMED | — |
| 38 | 天上看像鋪過，踩下去陷到腳踝的土；真的降落飛機會翻過去，計畫的人全在上面 | csek、4ijy | CH2 p.56（原頁）："From the air the strip appeared to be paved … ankle-deep dust … the plane would probably have nosed over … killing or injuring all of the key figures in the U-2 project" | 200 | CONFIRMED | — |
| 42 | 七月跑道鋪好、基地可用、人陸續搬進去 | site-runway-july/5vb9 | CH2 p.57："project managers decided that a paved runway was needed … By July 1955 the base was ready, and Agency, Air Force, and Lockheed personnel began moving in" | 200 | CONFIRMED | — （「鋪好了」仍是推論，原文沒寫完工日） |
| 44 | 4/12 選址、8/1 滑行測試意外離地、8/4 第一次計畫內飛行、8/8「官方」首飛到 32,000 英尺 | site-steps-first-flights、mjcy、9x6y、fc3a、3xn7 | CH2 pp.56、69–70 逐句；CIA-2015 同（August 1、4、8） | 200 | CONFIRMED | — |
| 47 | U-2 設計高度 70,000+ 英尺（約 21 公里）；客機 10,000–20,000；軍機 B-47、B-57 在 40,000 以下 | silver-stats-altitude、7btc、hnbv | CH1（"70,000 feet or higher"、CL-282 "just over 70,000 feet"）；CH2 p.72 原頁 | 200 | CONFIRMED | — |
| 48 | 那時沒有人相信有人能飛到六萬英尺以上 | edmc | CH2 p.72 原頁："no one believed manned flight was possible above 60,000 feet" | 200 | CONFIRMED | — |
| 51 | 1952 年夏天的通報圖，那時 U-2 還沒出生；U-2 試飛後通報大幅增加 | silver-bluebook-chart、vjea、2kvi、caption | C-BB（June–September 1952、NARA、PD）；CH2 p.72（"tremendous increase"） | 200 | CONFIRMED | — |
| 52 | 藍皮書 1947–1969 共 12,618 件，701 件仍列未解，1969-12-17 宣布結束，結論沒有證據指向外星飛行器 | silver-bluebook-stats、e4ic、5v2r、4qzc | NARA 原句（12, 618／701／December 17, 1969／"no evidence indicating that sightings categorized as 'unidentified' are extraterrestrial vehicles"） | 200 | CONFIRMED | — |
| 56 | 政府承認有這個地方，只是不說名字 | secret-chapter/6udd | FR95（"operating location near Groom Lake, Nevada"）；LVSun98（政府稱 "the operating location near Groom Lake" 且否認它是 Area 51） | 200 | CONFIRMED | — |
| 59 | 1995 年起總統每年簽豁免令；公報上查得到的至少到 2003 年 | z7ew、tkbk、secret-every-year | FR95（PD 95-45，1995-09-29，one-year）；FR-API：1995、96、97、98、99、2000、01、02、03 共 9 件，之後無 | 200 | CONFIRMED | — |
| 60 | 背景是一場官司，前基地工人聲稱那裡露天燒有害廢棄物 | secret-widow-steps/zczm | LVSun98（five current and former workers 與兩位遺孀；"open 55-gallon drums and burned them"）；ELR | 200 | CONFIRMED | — |
| 66 | 1998 年版 vs 2013 年版：272 頁／約 400 頁、Area 51 全塗黑／印出、沒有地圖／第 58 頁整頁地圖、姓名塗黑／姓名代號經費恢復 | secret-compare-versions、amji、583d、release-pilot-glove/sdcw | CIA-1998（272 pages、1992）；EBB434（names of pilots、cryptonyms、funding、"map of the area"）；CH2 PDF 第 20 頁＝書頁 58 整頁地圖 | 200 | CONFIRMED | — |
| 71 | 一位英國史家說這些新內容他的書早就寫過 | release-bookshop/v2vq | EBB434 Pocock："nearly all of the newly-released information is already in my books" | 200 | CONFIRMED | — |
| 73 | A-12 1962 年在這裡首飛；三倍音速、九萬英尺 | release-a12-photo、wyp5、4ccd、caption | CH6 pp.288–289（25 April 非正式、26 April 官方 40 分鐘、30 April 官方首飛）；p.278 規格 Mach 3.2、84,500–97,600 英尺；p.297 驗收飛行達 90,000 英尺；CIA-Museum Mach 3.29 at 90,000 feet | 200 | CONFIRMED | — |
| 81 | 現在在裡面試什麼還是機密；官方只叫它訓練場的一部分 | check-training-range/ew6b | AP（Nevada Test and Training Range）；CIA-2015（NTTR at Groom Lake）；EBB443（"Both have been partly declassified"） | 200 | CONFIRMED | — |
| 83 | 不是突然承認，是有人問了八年 | check-big-answer/5j56 | EBB434（2005 FOIA request → approved 25 June 2013） | 200 | CONFIRMED | — |

### 順手多看的

| # | 主張 | 位置 | 來源 | HTTP | 判定 | 改前 → 改後 |
|---|---|---|---|---|---|---|
| 70 | 第 58 頁整頁地圖，右下角還標著拉斯維加斯 | release-map-page/e43u | CH2 PDF 第 20 頁原圖：Las Vegas 在圖的右側、下半（Indian Springs 旁），真正的右下角是 Arizona 與 San Diego | 200 | CONFIRMED | — （「右下角」偏鬆，「右下方」更準；只差一字、不是事實錯誤，沒動） |

合計：35 列（第一輪改過的 9＋抽樣 25＋多看 1）。CONFIRMED 34、CHANGED 1（#19，事實：1967 年文件的日期）、NOT FOUND 0、OUT OF SCOPE 0。

## 摘要

- 查了 35 列：第一輪改過或拿掉的 9 列全部重開一手來源，8 列維持、1 列再改（#19）；隨機抽的 25 列確認列全部維持（種子 20261010）；另多看 1 列維持。
- 事實修改 1 處：`release-memo-1967` 卡片標題「1967 年 5 月 15 日的 CIA 文件」→「1967 年的 CIA 文件：OXCART 偵察北越的計畫」，因為 CIA 閱覽室把這份文件的日期寫成 1967-04-01、Commons 寫 1967-05-15，兩邊不一致；`assets[4].source` 同步改成閱覽室的文件編號。旁白、說明欄本來就只說「1967 年」，沒動。
- BYE 2369-67 是什麼：CIA 閱覽室 curl 仍打不開，內建瀏覽器開得了。文件頁：標題 "OXCART RECONNAISSANCE OF NORTH VIETNAM (W/ATTACHMENT)"，Document Type: FOIA，收在 "A-12 OXCART Reconnaissance Aircraft Documentation"，23 頁，Publication Date: April 1, 1967；影片用的那一頁頁首印 "II. OXCART RECONNAISSANCE OPERATIONS PLAN"、"BYE 2369-67 Page 15"。PDF 本身點下去跳出存檔對話框（DOC_0001471747.pdf，2.44 MB），沒有下載；逐頁 GIF 已 404。所以封面是不是備忘錄仍未親見，旁白與說明欄維持「文件」，卡片標題用閱覽室的文件名說它是什麼。
- 會過期的事實：沒有近期會過期的。兩件仍懸：2003 年之後總統豁免令有沒有再簽（聯邦公報當天仍只到 2003-10-21）；16 卷 OSA 內部史公開到什麼程度（閱覽室只有一份 24 頁、部分塗黑的 OSA HISTORY 大綱，2012 年釋出）。說明欄「資料截至 2026-10-10」正確。
- 來源與企劃衝突：沒有。
- 意見：三句意見（`2nea`、`9v4v`、`ktc6`）都標成「我的看法」且與 `brief.md` 站主觀點一致。
- 聽感（只報告，沒動）：沒有超過 40 字的句子，沒有括號或網址，沒有「經查證」類字眼；Latin 詞 Area 51、CIA、U-2、A-12、S-4 都在發音字典；reveal 都在介紹句之後。`silver-phone-check` 的插圖提示詞仍畫一個軍官拿電話，旁白第一輪已改成「請華盛頓的計畫人員核對」，CIA 史沒寫電話，站主可考慮把提示詞的電話換成翻紀錄本。KLAS 自己的兩篇回顧把首播寫成 1989-05-13 與 05-15，影片只說「一九八九年」，不受影響。照我的粗算，12 句帶 `emotion` 的旁白在 21–23 單位（例如 `583d`、`rka8`、`5j56`），lint 沒報、都是撰稿原句、本輪沒碰。
- lint：`node tools/video/cli.mjs lint --slug curio-u02` 0 錯誤、1 警告（outro 一句，原本就有）；估 11.2 分鐘、126 句。改 assets.source 時說明欄組合一度到 5,010 位元組，縮短後回到上限內。
- 懷疑但沒動：#70「右下角標著拉斯維加斯」偏鬆（Las Vegas 在圖的右側下半，不是角落）；CIA 閱覽室那份文件的 Publication Date 常是「只知月份就填 1 日」的填法，4 月 1 日未必是真日期，但沒有第三個來源能裁定；Skeptic 2026 這篇對 Lazar 偏同情（說「純捏造」的講法站不住），影片只取它承認的「兩校無紀錄、核心主張未證實」；`photos/u2-nasa-1960.jpg` 仍未登記在 `assets`、也沒用到。
- 第三輪：不需要（本輪事實修改 1 處 ≤ 3）。沒有未解決的主張；BYE 2369-67 的文件類型未親見，但影片已用不依賴它的措辭。
