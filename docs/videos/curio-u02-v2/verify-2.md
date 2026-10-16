# curio-u02-v2 查核第二輪

- 查核 2026-10-13，Claude Opus 5（第二輪查核代理）。**我不是撰稿的那一個，也不是第一輪
  [`verify-1.md`](verify-1.md) 的那一個**，第一版 `curio-u02` 兩輪查核也不是我做的。
  第一輪改了 10 處必改（超過 3 個事實），依系列規矩換人做第二輪。
- 這一輪的立場：**第一輪與撰稿都當成待驗的主張**。第一輪說對的我自己去原文看過才算數；
  撰稿偏離第一輪建議的兩處（`u305`、說明欄第 1 段）我只看來源，不看兩邊各自的說法。
- 方法：
  1. 自己從 `video.json` 抽出 125 個場景、145 句旁白（沒有任何一句有 `say`／`say_for`）、
     12 張卡片的 `data`、7 個 `chapter`、縮圖、標題、說明欄、標籤、`loops`、`sources[]`
     （`<scratch>\verify2-u02\lines2.txt`），不用第一輪或上一次未完成嘗試留下的任何檔案。
  2. 每個網址當天用 `curl` 重開，User-Agent `Mokaair-editorial/1.0 (https://mokaair.com;
     support@mokaair.com)`，同一主機間隔 1.4 秒（提示要求 1.2 秒以上）。所有請求都沒有帶個人信箱。
  3. CIA 計畫史第 1、2、6 章 PDF（7.8／12.2／10.4 MB）重新下載、`pdftotext -layout` 抽字；
     書頁 56、72、73 的文字層確實破損，書頁 58 是整頁地圖沒有可用文字層，這四頁用 PyMuPDF
     轉圖逐字讀（`<scratch>\verify2-u02\pg\`）。
  4. **第一輪沒開的一份：1998 年塗黑版的 272 頁 PDF 本體**（`CIA-and-U2-Program.pdf`，10.0 MB）。
     它整份沒有文字層，所以用 PyMuPDF 轉圖，對 1998 年版與 2013 年版的同一書頁逐頁比對。
     這是為了回答第一輪留下的第六個疑點（「只要講到就塗掉」）。
  5. 羅斯威爾到格魯姆湖的距離自己用大圓公式算（1,109 公里）。
  - **網路搜尋 0 次**（來源都已經有名有網址）。沒有跑 git，沒有跑任何影片階段，沒有花任何提供者的錢。
- 我沒有改 `video.json`、`claims.md`、`brief.md`、`NOTES.md` 的任何一個字。要改的都寫在
  〈這一輪自己找到的問題〉，附行 id、現在的句子、建議的句子與單位數
  （用 `tools/video/core/timeline.mjs` 的 `spokenUnits` 量過）。

## 當天開過的網址

| 縮寫 | 網址 | HTTP |
|---|---|---|
| EBB434 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/ | 200 |
| CH1 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%201.pdf （7,830,580 bytes） | 200 |
| CH2 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf （12,223,825 bytes；書頁 56、58、72、73 轉圖讀） | 200 |
| CH6 | https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%206.pdf （10,369,049 bytes） | 200 |
| CIA-1998 | https://www.cia.gov/resources/csi/books-monographs/the-cia-and-the-u-2-program-1954-1974/ | 200 |
| **CIA-1998-PDF** | https://www.cia.gov/resources/csi/static/CIA-and-U2-Program.pdf （10,001,947 bytes、272 頁、**無文字層**；第一輪沒開過這一份） | 200 |
| CIA-2015 | https://www.cia.gov/stories/story/area-51-and-the-accidental-test-flight/ | 200 |
| CIA-Molly | https://www.cia.gov/stories/story/ask-molly-what-really-went-on-at-area-51/ | 200 |
| CIA-Museum | https://www.cia.gov/legacy/museum/artifact/untouchable/ | 200 |
| CIA-RR | https://www.cia.gov/readingroom/node/1819895 | 200 但轉到閱覽室首頁：**NOT OPENED**（與第一輪同） |
| Reuters | https://www.csmonitor.com/USA/Latest-News-Wires/2013/0817/Area-51-is-real-say-CIA-documents | 200 |
| FR95 | https://www.govinfo.gov/content/pkg/FR-1995-10-10/html/95-25244.htm | 200 |
| FR-API | https://www.federalregister.gov/api/v1/documents.json?conditions[term]="Groom Lake"（11 筆，其中 9 筆是 1995–2003 的 Determination） | 200 |
| Clinton96 | https://clintonwhitehouse6.archives.gov/1996/01/1996-01-31-determination-exempting-usaf-from-conservation-laws.html | 200 |
| GAO | https://www.govinfo.gov/content/pkg/GAOREPORTS-NSIAD-95-187/html/GAOREPORTS-NSIAD-95-187.htm | 200 |
| NARA | https://www.archives.gov/research/military/air-force/ufos | 200 |
| EBB443 | https://nsarchive.gwu.edu/briefing-book/intelligence/2013-10-29/area-51-file-secret-aircraft-soviet-MiGs | 200 |
| ELR | https://www.elr.info/litigation/kasza-v-browner | 200 |
| LVSun98 | https://lasvegassun.com/news/1998/jan/08/toxic-data-at-area-51-ruled-confidential/ | 200 |
| CBS00 | https://www.cbsnews.com/news/satellite-image-of-area-51/ | 200 |
| TSR | https://thespacereview.com/article/4518/1 | 200 |
| Skeptic | https://www.skeptic.com/article/the-strange-case-of-bob-lazar/ | 200 |
| KNPR | https://knpr.org/knpr/2015-02/area-51-whistleblower-speaks-ufo-conference | 200 |
| KLAS-a | https://web.archive.org/web/20210507140618/https://www.8newsnow.com/news/local-news/i-team-man-who-detailed-ufo-secrets-decades-ago-helped-launch-area-51-stampede/ | 200 |
| KLAS-b | https://web.archive.org/web/20210117151518/https://www.8newsnow.com/news/i-team-25-years-later-man-who-exposed-area-51/ | 200 |
| AP | https://www.ktvu.com/news/about-75-people-gather-at-area-51-gate-1-person-arrested | 200 |
| C-USGS | https://commons.wikimedia.org/wiki/File:Area_51_28_August_1968_2.jpg | 200 |
| C-USGS-img | https://upload.wikimedia.org/wikipedia/commons/d/df/Area_51_28_August_1968_2.jpg （166,642 bytes，我自己看過原圖） | 200 |
| C-1967 | https://commons.wikimedia.org/wiki/File:CIA_BYE2369-67_page17.gif | 200 |
| C-BB | https://commons.wikimedia.org/wiki/File:Appendix_I_to_Project_Blue_Book_Status_Report_Number_8_-_NARA_-_595542.jpg | 200 |
| NPR-13 | https://www.npr.org/sections/thetwo-way/2013/08/16/212549163/ （`claims.md` c3 的第二個網址，不在 `sources[]`） | **000 連線逾時：NOT OPENED**（與第一版兩輪、第一輪同） |

`sources[]` 的 16 條今天全部 200，內容與 `checked_on` 2026-10-10 記的一致。

## 第一輪十八處改動，逐條重判

全部 18 處都已經套進 `video.json`。下面一條一條對原文重判。

| 代號 | 位置 | 現在的樣子 | 我自己看到的來源句 | 判定 |
|---|---|---|---|---|
| **A** | `basin-from-above.chapter` | 他們差一點降落在那條舊跑道上 | CH2 書頁 56（轉圖逐字讀）："After debating about landing on the old airstrip, LeVier set the plane down on the lakebed, and all four walked over to examine the strip." | **成立**。鹽湖床是他們實際降落的地方，差一點降落的是那條舊跑道；第一輪把方向判對了 |
| **B** | `u108` | 要是降落在那條線上，飛機會往前翻。（15 單位） | 同頁："If LeVier had attempted to land on **the airstrip**, the plane would probably have nosed over when the wheels sank into the loose soil" | **成立**。原文的風險限定在那條跑道；「那條線」回指 `u106`「旁邊有一條直線」，章名與句子現在一致 |
| **C** | `u305` | 軍用的轟炸機高一點，四萬英尺以下。（15 單位） | CH2 書頁 72（轉圖逐字讀）："most commercial airliners flew at altitudes between 10,000 and 20,000 feet and military aircraft like the B-47s and B-57s operated at altitudes **below 40,000 feet**" | **成立**（撰稿偏離第一輪建議，判給撰稿）。B-47 與 B-57 都是轟炸機，寫「軍用的轟炸機」比第一輪的「當時的軍機」更貼原文點的機型；「高一點」符合原文一萬～兩萬 → 四萬以下 → 六萬以上這道梯子。**但這一句帶出兩個新問題，見下方問題 2 與問題 3** |
| **D** | `u714` | 新版還是有很多，另一份內部的歷史也還沒全部公開。（22 單位） | EBB434 Pocock 評註逐頁寫了幾十處 "still redacted"；同頁："This is a reference to the 16-volume OSA history which has also been FOIA'd… The CIA historian told me last year that its release was **not pending**, due to 'multiple equities'" | **成立**。「還沒全部公開」是比「還沒公開」弱的講法，16 卷正史沒釋出時它必然為真，閱覽室今天開不了也不影響 |
| **E** | `u609` | 五個基地工人和兩位遺孀，告了空軍和環保署。（19 單位） | LVSun98："Lawyers for **five current and former workers** at the base, and the widows of two workers…"；ELR："two RCRA citizen suits against the U.S. Air Force and the U.S. Environmental Protection Agency (EPA)" | **成立**。有現職的，所以不能寫「前基地工人」 |
| **F** | `youtube.description` 第 1 段 | 一九五五年四月十二日，四個人坐在一架小飛機上飛過內華達 | CH2 書頁 56 只寫 "On 12 April 1955"；CIA-2015 連日期都沒有，全文都沒有 afternoon | **成立**。「下午」沒有來源，拿掉是對的 |
| **G** | `youtube.description` 第 1 段 | 這個編號，CIA 等了五十八年才**刻意**印在正式文件上。 | Reuters："the 400-page CIA history contains **the first deliberate official references to Area 51**"；同篇 Richelson："at least two previous government documents in which an **incidental** reference to Area 51 appeared, but he assumed those were **inadvertent**" | **成立，而且比第一輪建議的講法好**（撰稿偏離，判給撰稿）。第一輪建議「CIA 自己的正式文件等了五十八年才刻意印出來」會讓人以為 CIA 的正式文件從來沒印過；現在的寫法把「刻意」掛在動作上，正好是路透社的 deliberate，也和第 4 章「一九六七年，這兩個字已經印過了」、說明欄第 2 段「順手印過」互相撐得住。1955→2013 ＝ 58 年也對 |
| **H** | `altitude-stats.stats[0].value` | 70,000 英尺以上 | CH1 書頁 8："The requirement stated that such an aircraft must have an optimum subsonic cruise speed at altitudes of **70,000 feet or higher**"；CH1 書頁 11："The CL-282's maximum altitude would be **just over 70,000 feet**" | **成立**。卡片標籤寫「這架飛機的設計高度」，對應的是 CL-282 的 "just over 70,000 feet"，「以上」補回來是對的 |
| **I** | `names-table.data.source` | CIA 計畫史 p.57；CIA 2015 年文章 | CH2 書頁 57 全文只有 Paradise Ranch、the Ranch、Watertown Strip，**沒有 Dreamland**；CIA-2015："Dreamland was a radio call sign for the base, introduced in the late 1960s" | **成立**。第三列的出處本來就在另一篇 |
| **J** | `u415` | 事後的備忘錄裡有一句。（10 單位） | TSR 引同一份 1974-04-19 備忘錄，除了 "There were specific instructions not to do this" 還有 "This photo has been going through an interagency reviewing process…There is no agreement. DoD elements (USAF, NRO, JCS, ISA) all believe it should be withheld…NASA, and to a large degree State, has taken the position that it should be released"，另有 "some complicated precedents" 三項與 Colby 的附註 | **成立**。備忘錄不只一句，「裡有一句」是對的 |
| **K** | `u113` | 一個地圖編號，為什麼等了五十八年才**正式**印出來？（21 單位） | 同 G | **成立但最弱的一環**（見下方問題 4）。「正式」要靠第 4 章與 `u712` 回頭解釋才站得住；影片自己有解，所以不是硬錯 |
| **L** | `u702` | 從申請到核准，八年。（8 單位） | EBB434："FOIA request for a review of the redactions by the National Security Archive **in 2005**. Document review completed and approved for release 25 June 2013." 沒有寫申請的月份 | **成立**。「整整」是多出來的精確度，拿掉對 |
| **M** | `u617` / `redacted-272.data.kicker` | 更離奇的是，同一年 CIA 出了這本史書的第一個公開版本。（24 單位）／一九九八年的公開版 | CIA-1998："(This book is a partially redacted version of the classified original, which was **published in 1992**.)"；EBB434："the study was published in classified channels in 1992. Subsequently, a heavily redacted version of the U-2 portion was published, **in 1998**" | **成立**。1998 年是第一個公開的版本，不是第一版。`u617` 正好 24 單位，壓在上限 |
| **N** | `u420` | 地點早就不是祕密。（8 單位） | TSR："The US government has **at times** acknowledged and at other times refused to acknowledge its existence"；同段引 Merlin 的〈Area 51 was Never Classified〉、"The existence of an airstrip at Groom was revealed when it was first constructed" | **成立**。「從來」比來源絕對，「早就」剛好 |
| **O** | `u517` | 這塊地在內華達，中間隔著一千多公里。（16 單位） | GAO（Roswell, New Mexico）、CH2（Nevada）；我自己算大圓距離：羅斯威爾市→格魯姆湖 **1,109 公里**，羅斯威爾陸軍機場→格魯姆湖 1,113 公里 | **成立**。「一千公里」會低估，「一千多公里」對 |
| **P** | `u411b` | 一九五九年那一張，也在同一個地方。（15 單位） | TSR："at least **two** US Geological Survey aerial **photographs** of Groom taken in 1959 and 1968 had been available in public archives" | **成立**。是兩張照片，不是兩批 |
| **Q** | `u506` | 他說動力是一種叫元素一一五的東西。（16 單位） | Skeptic 把 element 115 整段當成 Lazar 的聲稱（"his specific claims about a stable isotope or gravity propulsion"）；KNPR 同 | **成立**。歸屬補上「他說」之後，不再只靠鄰句。`u505` 旁邊有卡片 kicker「他說的」，依第一輪的判法留著，我同意 |
| **R** | `u325` | 結論裡有一句：未解的那些，沒有證據指向外星飛行器。（22 單位） | NARA 原句："there has been no evidence indicating that sightings **categorized as 'unidentified'** are extraterrestrial vehicles" | **成立**。限定語補回來了，而且沒有超過 24 單位 |

**18 處全部成立：16 處照第一輪的建議改、判定無誤；2 處撰稿偏離建議（C、G），依來源判，兩處都站得住，G 還比第一輪的建議準。**

`claims.md` 的 S–W 五項我也對過，全部做了，而且我自己驗過底：
S（c6 補回兩個 KLAS Wayback 網址）——今天重開 200，四件事都在原文裡；
T（拿掉「柯林頓致國會信沒講」那一條）——`u608` 講的就是這封信，Clinton96 原文 1996-01-30；
U（c2 的括號改成第三輪盲評後拿掉片尾那句）——`video.json` 裡確實沒有那一句了；
V（c11 補回「非機密地圖上一小塊長方形」）——CH2 書頁 56–57 轉圖讀到原句，`u723` 有依據了；
W（c3 的 npr.org）——我今天也是 000 逾時，`sources[]` 沒列 NPR，不影響影片。

## 七個章名，逐個判

第一輪只查了第 1 章的章名。`chapter` 會進 YouTube 的章節清單，觀眾讀得到，所以七個我全查。

| # | 章名 | 來源 | 章內的句子對不對得上 | 判定 |
|---|---|---|---|---|
| 1 | 他們差一點降落在那條舊跑道上 | CH2 p.56："After debating about landing on the old airstrip, LeVier set the plane down on the lakebed"；"more than a decade of disuse"（所以是「舊」） | `u106` 那條直線像跑道 → `u107` 不是柏油是鬆土 → `u108` 要是降落在那條線上會往前翻。章名與三句同指一物 | **成立** |
| 2 | 八月一日，它自己飄了起來 | CIA-2015："On August 1, 1955, during a high-speed-taxi test…Tony LeVier, **inadvertently became airborne**"；CH2 p.69 LeVier 原話 "I became aware of being airborne…I had no intentions whatsoever of flying" | `u207` 八月一日高速滑行測試 → `u208` 飛機自己離地 → `u209` 試飛員說他根本沒打算飛 | **成立**。章首 `u201` 講七月，章名講八月一日，是章名先許一個承諾、`u207`–`u209` 兌現，不是不符 |
| 3 | 傍晚的客機上，有人看到一團火 | CH2 p.72："Such reports were most prevalent in the **early evening hours** from pilots of airliners flying from east to west"；"its silver wings would catch and reflect the rays of the sun and appear to the airliner pilot, 40,000 feet below, to be **fiery objects**" | `u309` 往西飛的客機天已黑 → `u311` 機翼還曬得到太陽 → `u312` 在客機飛行員眼裡那是一團火 | **成立**。「傍晚」＝early evening，「客機上」＝airline pilots，都在原句裡 |
| 4 | 一九六七年，這兩個字已經印過了 | C-1967 原件（BYE 2369-67，1967-05-15，CIA，PD-USGov-CIA）："Three OXCART aircraft and the necessary task force personnel will be deployed from **Area 51** to Kadena." | `u404` 一九六七年 CIA 的一份文件提到這個地方 → `u406` 上面印的就是那兩個字 | **成立**。章首講 1962 年的 A-12、章名講 1967 年，章名挑的是這一章最重的那一拍，不是章首那一拍——以 YouTube 章節清單來說這樣寫是對的，觀眾讀到的是一句完整、準確的事實 |
| 5 | 一九八九年，電視上有人說那裡有九艘飛碟 | KLAS-a："On May 15, 1989, KLAS-TV aired a live interview"；KLAS-b："inside were **nine flying saucers**"；KNPR："nine saucers located in a hangar" | `u502` 一九八九年拉斯維加斯一家電視台播了訪談 → `u505` 一個機棚裡停著九艘飛碟 | **成立，而且寫法對**。章名自己標了「有人說」，傳說段的歸屬在觀眾只讀章節清單時也不會掉 |
| 6 | 總統每年簽一次，卻從來不寫名字 | FR95 原文："the United States Air Force's **operating location near Groom Lake, Nevada**"，全篇沒有 Area 51；FR-API 九件（1995-10-10、1996-10-08、1997-10-08、1998-10-23、1999-10-26、2000-10-05、2001-10-04、2002-12-24、2003-10-21）標題一律同一個稱呼 | `u601` 一九九五年九月總統簽了一份命令 → `u602` 稱呼是空軍在格魯姆湖附近的作業地點 → `u607` 年年簽、公報上一共九份 | **成立**。「每年」沒有寫到哪一年為止，但同一章的 `u607`（九份）與 `u621b`（最後一份是二〇〇三年）把它框住了 |
| 7 | 第五十八頁，是一整頁地圖 | CH2 PDF 第 20 頁＝書頁 58，我自己轉圖看過：整頁一張地圖，標題就是 "Area 51"，含 Groom Lake／AEC Nevada Test Site 插圖；EBB434 Pocock 評註 "P58 This is a whole-page map of CA and NV to show where the test site was" | `u707` 第五十八頁，整頁都是地圖 | **成立** |

七個章名全部對得上來源，也對得上各自章內的句子；沒有一個是功能式章名（背景、結論、最站得住的解釋），都寫「這一章發生了什麼」。

## 第一輪留下的六個疑點，逐個回答

### 1.「右下角標著拉斯維加斯」（`u707b`）——**不精確，建議改，不擋**

我自己把 CH2 PDF 第 20 頁（書頁 58）以 200 dpi 轉圖量過：Las Vegas 的點與標籤在**整頁的右 72%、下 59%**，
換算到地圖外框之內是**右 81%、下 62%**。地圖真正的右下角是 Arizona，再往下是 San Diego 與墨西哥那一塊。
所以拉斯維加斯在**右半邊、中線略下**，落在右下象限裡，但不在角上。

這一版沒有照片卡（`claims.md` 自己說的），觀眾看不到這張地圖，所以不會當場對不起來；
第一版第二輪與第一輪也都是同樣的量測、同樣選擇不動。我同意不擋，但這是三輪都記下同一件事了，
要收就一次收乾淨：`右下角標著拉斯維加斯。`（10 單位）→ `右邊偏下標著拉斯維加斯。`（11 單位）。

### 2.「一九七四年」（`u413`）——**不成立，要改**

TSR 全文沒有一句把拍照那一刻定在 1974 年。它給的是：
- "The third and last Skylab crew had **launched into space on November 16, 1973**…Their mission lasted **84 days**."（＝1973-11-16 到 1974-02-08，跨年）
- "On **April 19, 1974**, someone in the CIA sent the Director of Central Intelligence, William Colby, a memorandum"
- 備忘錄原句只說 "the **recent** Skylab mission inadvertently photographed"
- 圖說："Its existence created a stir within the US Intelligence Community **in 1974**."

有來源的 1974 是**備忘錄與那場風波**，不是**拍照**。84 天裡有 45 天在 1973 年、39 天在 1974 年，
拍照落在哪一年來源沒有寫死。這和第一輪判成必改的說明欄「下午」是同一類：**旁白自己加上了來源沒有的時間**。
依同一把尺，這一句要改。詳細改法見下方〈問題 1〉。

### 3.「跑道在七月鋪好」（`u201`）——**仍是推論，可以留，但要知道留的是什麼**

CH2 書頁 57 原文："Although the dry lakebed could have served as a landing strip, project managers decided that
a **paved runway was needed** so that testing could also take place during the times when rainwater runoff from
nearby mountains filled the lake…**By July 1955 the base was ready**, and Agency, Air Force, and Lockheed
personnel began moving in." EBB443 的敘述一樣：決定要鋪跑道、By July 1955 基地可用。
**兩個來源都沒有寫跑道的完工日**。我把 CH2 整章搜過（`runway`／`paved`／`July 1955`），也沒有第二處給日期。

「基地可用」裡合不合理地含著那條跑道？合理——跑道正是那段工程的理由。但嚴格說，
「跑道在七月鋪好」是從「七月基地可用」推出來的。第一版兩輪與第一輪都選擇留著，我也留著，
因為它推得不遠、而且句子的功能是交代時間，不是交代跑道。**記在這裡，不要求改。**
（附帶一提：1998 年塗黑版裡 "By July 1955 the base was ready" 這一句整句被塗掉，所以這個事實只有 2013 年版有。）

### 4.「法院駁回」（`u612`）——**成立**

ELR："(9th Cir. **Jan 8, 1998**)…because the very subject matter of the action is a state secret, the court
**affirms the district court dismissal** of the action."；LVSun98 同日："Rymer's opinion denying disclosure and
**ordering dismissal of the case**"。

嚴格講第九巡迴做的是「維持地院的駁回」，但影片引的來源之一（Las Vegas Sun）自己就寫 ordering dismissal，
旁白也沒有說是哪一級法院第一次駁回。口語上「一九九八年一月，法院駁回」沒有讓觀眾得到錯的印象。**成立，不改。**

### 5.「這樣的舊文件」（`u711`）——**成立（寬，但歸屬正確）**

Reuters 原句："Richelson said he could recall at least two previous **government documents** in which an
incidental reference to Area 51 appeared, but he assumed those were inadvertent because they were devoid of
any other details or context."

來源寫的是「政府文件」，旁白上一句 `u710` 指的是 1967 年那一份 CIA 文件。CIA 文件本來就是政府文件，
所以「這樣的舊文件」沒有說錯；而且句子有「**他記得**」，歸屬掛在 Richelson 身上，正是原文的結構。
Richelson 記得的那兩份是不是包含 1967 那一份，來源沒說，旁白也沒有宣稱。**成立，不改。**

### 6.「只要講到這裡的句子就塗掉」（`u618`）——**成立，而且現在有直接證據**

第一輪說這是 EBB 434 的對照結論，不是逐句數過的。我把 1998 年版的 272 頁 PDF 抓下來
（無文字層，轉圖），找出它的頁碼位移（PDF 頁＝書頁＋12），把同一本書的同三頁拿來並排：

- **書頁 56**（1998 年版）：凡是指出地點的字全部在黑條底下——"the top officials of the Development Projects
  Staff flew to ███ search for a site"、"flew ███ with Kelly Johnson"、"They spotted what appeared to be an
  airstrip ███"、"LeVier set the plane down ███ and all four walked over to examine the strip"、
  "Bissell and his colleagues all agreed that ███ would make an ideal site"、
  "Upon returning to Washington, Bissell discovered that ███（以下整段到頁底全黑）"。
  **沒有指出地點的句子完整留著**：「If LeVier had attempted to land on the airstrip, the plane would probably
  have nosed over…」一字未塗。
- **書頁 57**（1998 年版）：整個上半頁（Area 51 的外框、Paradise Ranch、the Ranch、Watertown Strip、
  By July 1955 the base was ready）全黑，只留下沒有地名的那幾句。
- **書頁 58**（1998 年版）：**整頁全黑**，一張地圖都看不到。

另外 EBB434 的 Pocock 評註自己寫："I have described most of the now-lifted redactions below, but have not
commented below on those that were **already obvious from the context, such as 'Area 51'**."——他連註都懶得一個個下，
因為這個詞的塗黑到處都是。全份 272 頁 PDF 抽不出任何文字（是掃描件），所以沒辦法給一個「幾句」的數字，
但「只要講到這裡的句子就塗掉」這個敘述，逐頁比對下來是準的。**成立。**

順帶因此確認了兩件第一輪判 CONFIRMED 的事：
`u705`「舊版連地圖那一頁都沒有」——那一頁在，但整頁塗黑，**效果上成立**（要更精確可以寫「那一頁整頁塗黑」）；
`two-editions` 卡片左欄「名字全部塗黑」「沒有地圖」——書頁 57、58 親眼看到，成立。

## CONFIRMED 抽樣：42／102

**怎麼選的（不是亂數，是挑最會出錯的地方）**：
(a) 凡是帶數字、日期或數量、觀眾回頭查得到的，全抽——第一輪十個必改裡有七個都出在這一類；
(b) 凡是緊鄰那 18 處改動的「接縫」——第一輪自己說錯都出在重講的接縫上，改完的接縫最值得再看一次；
(c) 凡是只有單一來源撐著的；
(d) 凡是第一輪判 CONFIRMED 但後面加了但書的。
四條規則取聯集，得 42 列，佔 102 列的 41%，超過三分之一的要求。

| 第一輪 # | 主張 | 位置 | 我重查到的原句 | 判定 |
|---|---|---|---|---|
| 1 | 標題「CIA 等了 58 年才正式印在文件上」 | youtube.title | Reuters "first deliberate official references"；1955（CH2 p.56）→2013（EBB434） | CONFIRMED（但「正式」是全片最弱的一環，見問題 4） |
| 7 | 資料截至 2026-10-10 | description 第 5 段 | `sources[]` 16 條今天（10-13）全部 200，內容未變 | CONFIRMED |
| 9 | 縮圖「飛碟？是飛機」 | thumbnail | Reuters 發言人 Price："CIA tests its U-2 and A-12 reconnaissance aircraft at the site…What readers won't find are any references to aliens" | CONFIRMED |
| 6 | 插圖是 AI、虛構卡通角色、不寫名字、在世人物不入畫 | description 第 4 段 | 我自己把 113 個 `prompt` 逐一搜過（21 個人名、resembl／likeness／real person 等字）：**0 命中**；`face-hidden` 是 "face in deep shadow"、`a-hand-signs` 只有一隻手 | CONFIRMED（第一輪寫「125 個 prompt」是把卡片場景也算進去了，實際帶 prompt 的是 113 個） |
| 11 | 一九五五年四月十二日 | u101 | CH2 p.56："On 12 April 1955 Richard Bissell and Col. Osmund Ritland…" | CONFIRMED |
| 12 | 小飛機上坐著四個人 | u102 | 同頁：Bissell、Ritland、Kelly Johnson、"piloted by Lockheed's chief test pilot, Tony LeVier"；"**all four** walked over" | CONFIRMED |
| 15 | 這塊荒地的地圖編號是 Area 51 | map-number、u105 | CH2 p.56（轉圖）："this strip of wasteland, **known by its map designation as Area 51**"；CIA-2015 "known at the time by its map designation: Area 51" | CONFIRMED |
| 19 | 機上的人幾乎是整個計畫的核心 | u109 | CH2 p.56："killing or injuring **all of the key figures in the U-2 project**" | CONFIRMED |
| 20–22 | 回華盛頓才發現不屬於試驗場／請 AEC 劃進來／艾森豪批准 | u110、u111、u112 | CH2 p.56（轉圖）："Upon returning to Washington, Bissell discovered that Groom Lake was not part of the AEC proving ground…asked the Atomic Energy Commission to add the Groom Lake area to its real estate holdings in Nevada. AEC Chairman Adm. Lewis Strauss readily agreed, and **President Eisenhower also approved** the addition" | CONFIRMED |
| 25 | 跑道在七月鋪好，人開始搬進去 | u201 | CH2 p.57："By July 1955 the base was ready, and Agency, Air Force, and Lockheed personnel began moving in." | CONFIRMED（跑道完工日仍是推論，見疑點 3） |
| 26 | 工程師取名天堂牧場，後來簡稱牧場 | u202–u204 | CH2 p.57："Kelly Johnson called it the Paradise Ranch, which was soon shortened to the Ranch"；CIA-2015 同 | CONFIRMED |
| 29 | 一九六〇年代末，無線電裡叫它夢境 | u206 | CIA-2015："Dreamland was a radio call sign for the base, **introduced in the late 1960s**" | CONFIRMED |
| 30 | 三次「首飛」8/1、8/4、8/8 | first-flights、u207–u211 | CH2 p.69："followed on 1 August…'I had no intentions whatsoever of flying'"；"the **first planned flight on 4 August 1955**"；p.70："scheduled the 'official' first flight for **8 August 1955**. This time **outsiders were present**" | CONFIRMED |
| 31 | 它爬到三萬兩千英尺 | u212 | CH2 p.70："The U-2 flew to **32,000 feet** and performed very well." | CONFIRMED |
| 32 | 八個月內飛起來，他做到了 | u213、u214 | CH2 p.70："Kelly Johnson had met his **eight-month deadline**." | CONFIRMED |
| 33–35 | 十月三日開航／週一進週五回／不到七週 | u215、u216、u216b | CH2 p.72："fly the essential personnel to the site on **Monday morning** and return them to Burbank on **Friday evening**…a regularly scheduled Military Air Transport Service (MATS) flight using a USAF C-54 aircraft began on **3 October 1955**…**Less than seven weeks** after it started" | CONFIRMED |
| 36–37 | 十一月十七日失事、十四人全罹難、死最多的一次 | u217–u219 | CH2 p.72："a MATS aircraft bound for Area 51 crashed on **17 November**, killing **all 14 persons** aboard…This crash represented the **greatest single loss of life in the entire U-2 program**" | CONFIRMED |
| 40 | 七萬英尺；空軍一九五三年要的就是這個高度 | u301、u302 | CH1 p.8："**By March 1953**, Seaberg had expanded his ideas…The requirement stated that such an aircraft must have an optimum subsonic cruise speed at altitudes of **70,000 feet or higher**" | CONFIRMED |
| 42 | 機翼又細又長 | u303 | CH1 p.25："a sailplane wing (in technical terms a **high-aspect-ratio, low-induced-drag wing**)" | CONFIRMED |
| 43 | 當時的客機飛一萬到兩萬英尺 | u304、stats[1] | CH2 p.72（轉圖）："most commercial airliners flew at altitudes **between 10,000 and 20,000 feet**" | CONFIRMED |
| 45 | 卡片「40,000 英尺以下／當時的軍機」 | stats[2] | 同頁："military aircraft like the B-47s and B-57s operated at altitudes **below 40,000 feet**" | CONFIRMED（但出現的時機不對，見問題 2） |
| 47 | 沒有人相信有人能飛到六萬英尺以上 | u306 | CH2 p.72（轉圖）："**At this time, no one believed manned flight was possible above 60,000 feet**, so no one expected to see an object so high in the sky." | CONFIRMED |
| 49–51 | 往西飛的客機天已黑／再往上四萬英尺／那是一團火 | u309–u312 | CH2 p.72（轉圖）："When the sun dropped below the horizon of an airliner flying at 20,000 feet, the plane was in darkness…its silver wings would catch and reflect the rays of the sun and appear to the airliner pilot, **40,000 feet below**, to be fiery objects" | CONFIRMED |
| 52 | 寫信到代頓→請華盛頓核對→對外說自然現象 | sighting-steps、u313–u315 | CH2 p.73："wrote letters to the Air Force unit at **Wright Air Development Command in Dayton**…investigators then attempted to explain such sightings by linking them to **natural phenomena**. BLUE BOOK investigators regularly **called on the Agency's Project Staff in Washington** to check reported UFO sightings against U-2 flight logs" | CONFIRMED |
| 55 | 計畫史裡有一句話：一半以上是它們；史家寫的，沒有統計 | u318–u320 | CH2 p.73（轉圖）逐字："U-2 and later OXCART flights accounted for **more than one-half of all UFO reports** during the late 1950s and most of the 1960s."；p.73 頁底只印一條註："Information supplied by James Cunningham to Donald E. Welzenbach (U)"（"OSA History, chap. 7, pp. 17-19" 那條在 p.72 頁底）。兩條都不是統計 | CONFIRMED（第一輪把腳註指到 OSA History，位置記反了；不影響 `u320` 的「沒有附任何統計」） |
| 57 | 12,618／701／1969 年底 | bluebook-stats、u322–u324 | NARA："a total of 12, 618 sightings were reported…Of these **701** remain 'Unidentified.'"；"On **December 17, 1969**, the Secretary of the Air Force announced the termination" | CONFIRMED |
| 61 | 一九六二年四月，新飛機在這裡首飛 | u401 | CH6 p.288："On **25 April 1962**, test pilot Louis Schalk took 'article 121' for an unofficial, unannounced flight…on the next day, **26 April**, Schalk made the official 40-minute maiden flight"；p.289："the OXCART's official first flight took place on **30 April 1962**"；CIA-2015："The first flight test of the CIA's A-12 OXCART took place **at the Groom Lake facility** on April 25, 1962" | CONFIRMED（三個日期都在四月；地點有 CIA-2015 撐著） |
| 62 | A-12，三倍音速、設計高度九萬英尺 | u402、u403 | CH6 p.278："the OXCART aircraft was to achieve a speed of **Mach 3.2**"；CIA-Museum "three times the speed of sound"；CH6 p.273 設計對照表 Lockheed A-12 的三段高度：**84,500 ft／91,000 ft／97,600 ft**；p.262 "cruise at Mach 3.0 at altitudes **above 90,000 feet**" | CONFIRMED（九萬英尺落在設計巡航帶的正中間，不是只有事後達到的紀錄） |
| 63 | 一九六七年 CIA 文件印著那兩個字 | u404、name-1967、u406 | C-1967 原件全文："Three OXCART aircraft and the necessary task force personnel will be deployed from **Area 51** to Kadena."；Commons 標 1967-05-15、CIA、PD-USGov-CIA | CONFIRMED（旁白只寫年份，避開了 Commons 與閱覽室日期不一致的問題） |
| 64 | 申請的人說那是無意的、只是附帶提到 | u407、u408 | Reuters："…an **incidental** reference to Area 51 appeared, but he assumed those were **inadvertent** because they were devoid of any other details or context" | CONFIRMED |
| 65–66 | 隔年政府自己拍了它／一直在公開檔案庫／跑道一清二楚 | u409–u412 | C-USGS（1968-08-28，PD-USGS）；TSR："at least two US Geological Survey aerial photographs of Groom taken in 1959 and 1968 had been **available in public archives**"；我自己下載原圖看過：主跑道、機棚、營區一目了然 | CONFIRMED |
| 68 | 一九七四年太空人拍了它／只有這一個地方不准拍 | u413、u414 | TSR："Groom '**was the only location which had such an instruction**.'" | **後半 CONFIRMED，前半（一九七四年）NOT FOUND**，見疑點 2 與問題 1 |
| 70 | 有明確的指示，不要這樣做 | u416 | TSR 引備忘錄："**There were specific instructions not to do this**" | CONFIRMED |
| 71 | 同一個時期還研究弄到手的蘇聯米格機 | u417、u418 | EBB443："a 300-page Defense Intelligence Agency report on the exploitation of the **MiG-21**, a project titled **HAVE DOUGHNUT**…two **MiG-17s**, efforts named **HAVE DRILL and HAVE FERRY**"；"Soviet MiGs were evaluated and flown at Area 51 starting in the late 1960s"（TSR） | CONFIRMED |
| 72 | 一九七七年隱形驗證機第一次飛 | u419 | EBB443："Designated HAVE BLUE, it resulted in two experimental aircraft, with a **first flight in April 1977**"（原文沒寫首飛地點，旁白也沒說） | CONFIRMED |
| 75 | 十二年後 | u501 | 1977（EBB443）→1989（KLAS-a） | CONFIRMED |
| 77–78 | 遮著臉、用化名／這個地方南邊的 S-4 | u503、u504 | KLAS-b："In the interview, **Lazar's face was hidden and he used a pseudonym, Dennis**…a location called **S-4 south of Groom Lake**" | CONFIRMED（出處已依 S 補回 c6） |
| 79–80 | 一個機棚裡九艘飛碟／元素一一五 | nine-saucers、u505、u506 | KNPR："**nine saucers located in a hangar**"；KLAS-b："inside were nine flying saucers"；Skeptic 的 element 115 段 | CONFIRMED |
| 81 | 同一年稍後本名公開 | u507 | KLAS-a："It would be **another seven months** before the world learned the guy's real name was Bob Lazar"（1989-05-15＋7 個月＝1989 年 12 月中，仍在同一年） | CONFIRMED |
| 82–83 | 這些話一份文件都沒有／兩所學校查不到紀錄 | u508、u509 | Skeptic："Lazar's central claim…**remains unproven**"；"He has claimed to have earned two master's degrees, one in physics from **MIT** and the other in engineering from **Caltech**. Skeptics, including ufologist Stanton Friedman, reported **finding no record of him at either institution**" | CONFIRMED |
| 85–86 | 1947-07-08 新聞稿說飛碟、隔天改口氣象氣球／1994 年空軍再查 | u511–u515 | GAO 逐字："On **July 8, 1947**, the Roswell Army Air Field (RAAF) public information office…reported the crash and recovery of a '**flying disc**.' **The following day**…a crashed **radar-tracking (weather) balloon**"；"In the **July 1994** Report of Air Force Research…the **most likely source of the wreckage was from a balloon-launched classified government project**" | CONFIRMED |
| 88 | 殘骸運過去的紀錄，一份也沒有 | u518 | GAO："We conducted an **extensive search** for government records related to the crash near Roswell…Our search…yielded **two records** originating in 1947"；GAO 全文 0 次出現 Nevada／Area 51／Groom，CH2 全文 0 次出現 Roswell | CONFIRMED（對缺席的陳述，兩邊都查過了） |
| 91–92 | 1995-09 命令／稱呼／豁免內容／公報九份 | u601–u604、u607 | FR95 逐字："Presidential Determination No. 95-45 of **September 29, 1995**…the **United States Air Force's operating location near Groom Lake, Nevada**…any Federal, State, interstate or local provision respecting control and abatement of **solid waste or hazardous waste disposal that would require the disclosure of classified information**"；FR-API 九件 | CONFIRMED |
| 93 | 1996 年總統給國會的信把它連到一場官司 | u608 | Clinton96（信日期 1996-01-30，1996-01-31 發布）："to eliminate any potential uncertainty arising from a decision in **pending litigation, Kasza v. Browner**" | CONFIRMED |
| 95–100 | 桶裡燒／國家機密特權／馬賽克理論／連有沒有廢棄物都算機密 | u610、u611、u614–u616 | LVSun98："employees at the base routinely put hazardous chemicals in **open 55-gallon drums and burned them**"；"an unclassified filing by Air Force Secretary **Sheila Widnall**"；"the disclosure of even '**seemingly innocuous information**' can be barred if it is part of a '**mosaic**'"；"are not entitled to learn **whether hazardous substances exist there** or how they are handled…or even the name of the base"；ELR："the Air Force properly employed the **mosaic theory** of classification" | CONFIRMED |
| 102 | 兩百七十二頁／只要講到就塗掉 | redacted-272、u618 | CIA-1998："Download PDF of complete book (**272 pages**)"；1998 年版 PDF 本體 272 頁；逐頁比對見疑點 6 | CONFIRMED |
| 104–105 | 兩年後俄國衛星、黑白兩公尺／最後一份是二〇〇三年 | u620、u621、u621b | CBS00（2000-04-17）："took the photos using a **Russian spy satellite in 1998**…The **panchromatic, or black-and-white**, images have a **2-meter resolution**"；FR-API 最後一件 **2003-10-21**，之後無 | CONFIRMED |
| 106、108、110 | 2005 年的申請／2013-06-25 核准／8 月 15 日上網 | u622–u624、u701、u703 | EBB434："What the CIA released in response to a **2005** Freedom of Information Act request is a **substantially less redacted version**…Document review completed and **approved for release 25 June 2013**"；"**Posted – August 15, 2013**"；CH2 每頁印 "Approved for Release: 2013/06/25" | CONFIRMED |
| 112 | 舊版連地圖那一頁都沒有／新版四百多頁 | u705、u706 | 1998 年版書頁 58 **整頁全黑**（我親眼比對）；Reuters "the **400-page** CIA history"（406／407 的精確頁數只在 CIA 閱覽室，今天打不開，旁白說「四百多頁」在三個數字之間都成立） | CONFIRMED |
| 115–118 | 姓名代號經費都回來了／媒體標題不太準／至少兩份／路透社的用詞 | u708–u712 | EBB434："names of pilots, codenames and cryptonyms, locations, funding and cover arrangements"；EBB434 的 In The News 標題（"CIA lifts the lid on Area 51 for the first time EVER"、"Area 51 Finally Acknowledged By US Government"）＋TSR "despite all the other times it had already done so"；Reuters 前引 | CONFIRMED |
| 122–124 | 發言人說找不到外星人／今天是訓練場／現在在試什麼仍是機密 | u716、u718、u719 | Reuters（Edward Price 逐字）；CIA-2015："the commonly preferred official name for the facility today is the **Nevada Test and Training Range at Groom Lake**"；AP："the **Nevada Test and Training Range**"，空軍回應沒有說用途 | CONFIRMED |
| 127 | 那個編號現在印在公開的地圖上，一小塊長方形 | u723 | CH2 pp.56–57（轉圖）："The outlines of Area 51 are **shown on current unclassified maps as a small rectangular area** adjoining the northeast corner of the much larger Nevada Test Site." | CONFIRMED |
| 129 | `sources[]` 16 條 | sources[0..15] | 16 條今天全部重開，**16／16 都是 200** | CONFIRMED |

**抽樣結果：42 列裡 41 列 CONFIRMED，1 列（#68 的前半、`u413` 的「一九七四年」）判 NOT FOUND。**
沒有發現第一輪判錯的 CONFIRMED，只有一處腳註位置記反（#55），不影響影片。

## 這一輪自己找到的問題

### 必改

**問題 1. `u413` 的「一九七四年」沒有來源**（事實）

現在：`一九七四年，太空站的太空人也拍了它。`（16 單位）
建議：`後來，太空站的太空人也拍了它。`（13 單位），並把年份移到有來源的那一句——
`u415` 從 `事後的備忘錄裡有一句。`（10 單位）改成 `一九七四年的備忘錄裡有一句。`（13 單位）。

為什麼：見疑點 2。TSR 把 1974 掛在**備忘錄（1974-04-19）與那場風波**上，拍照那一刻落在
Skylab 4 跨年的 84 天任務（1973-11-16 起）裡，來源沒有寫死。這麼改之後，
這一段三句（`u413` 拍了它 →`u414` 只有這裡不准拍 →`u415` 一九七四年的備忘錄裡有一句 →`u416` 原句）
每一個時間點都踩在來源上，而且全段只多出 0 單位（13＋13 ＝ 16＋10）。
`claims.md` c28 的條文也要跟著把「1974 年 Skylab 4 太空人…拍到」改成「1974-04-19 備忘錄記下 Skylab 4 拍到」。

**問題 2. `altitude-stats` 的三個數字比旁白早一步出現**（卡片，不是事實）

這張卡的三句都帶 `reveal: 1`，`timeline.mjs` 把第一句的 reveal 併進開場狀態
（`current.start_frame === frame → current.reveal = reveal`），`templates.mjs` 的
`visibility()` 再算 `shown = count − totalReveals + reveal`。所以實際是：

| 說到這一句 | 螢幕上新出現的 | 對不對得上 |
|---|---|---|
| `u304` 當時的客機，飛一萬到兩萬英尺。 | stats[0]「70,000 英尺以上／這架飛機的設計高度」 | ✗ 聽到客機、看到七萬 |
| `u305` 軍用的轟炸機高一點，四萬英尺以下。 | stats[1]「10,000–20,000 英尺／當時的客機」 | ✗ 聽到軍機、看到客機 |
| `u306` 沒有人相信，有人能飛到六萬英尺以上。 | stats[2]「40,000 英尺以下／當時的軍機」 | ✗ 聽到六萬、看到四萬 |

整張卡慢一拍（或說快一拍）。我把這一版所有多段揭示的卡片都算過，**只有這一張錯位**：
`first-flights`、`sighting-steps`、`bluebook-stats`、`two-editions` 四張，第 N 句對第 N 個元素，全部對齊。

第一輪的改動 C 讓這件事變嚴重：`u305` 現在講出「四萬英尺以下」，而螢幕上那一格要到下一句才出現。

建議（純粹是 `data` 重排，不動任何事實、不動任何句子）：把 `altitude-stats.stats` 的順序改成

```
[ {10,000–20,000 英尺 / 當時的客機},
  {40,000 英尺以下   / 當時的軍機},
  {70,000 英尺以上   / 這架飛機的設計高度} ]
```

這樣 `u304`→客機、`u305`→軍機、`u306`→七萬英尺以上，三句三格全部對齊；
卡片標題「一九五〇年代中期，誰飛在哪裡」本來就是一道由低到高的梯子，改完更順，
而且 `u306`「沒有人相信有人能飛到六萬英尺以上」落在「70,000 英尺以上」那一格上，正好是這一章的轉折。

**不要用「拿掉 `u306` 的 reveal」這個做法**：那會讓 `u305`＋`u306` 合成一個狀態（15＋14 ＝ 29 單位，
約 9 秒），超過 `cadence.mjs` 的 `MAX_PICTURE_SECONDS = 8`，最終關卡會擋。

### 建議（不擋）

**問題 3. 「四萬英尺」六句之內講了兩次，意思不同**

`u305` `軍用的轟炸機高一點，四萬英尺以下。`（軍機的天花板）
`u311` `再往上四萬英尺，機翼還曬得到太陽。`（U-2 比客機高出來的差距）

兩句都有來源、都沒錯，但中間只隔五句，同一個數字講的是兩件事；
`u311` 的那個「四萬」是和 `u304` 的客機高度比出來的，聽眾很可能接到 `u305` 的軍機上。
`lint` 的門檻是同一個數字出現在三句以上才警告，所以這不是規則違反，是聽感風險，
而且是改動 C 帶進來的（改之前 `u305` 是「軍用的轟炸機飛得更低」，沒有數字）。

如果採了問題 2 的重排，`u305` 說話時那一格就在螢幕上，數字由卡片扛，旁白可以讓出來：
`軍用的轟炸機，只高一點點。`（11 單位）——仍然修正了第一輪抓到的方向錯誤（比客機高，不是更低），
也不再和 `u311` 撞號。要保留 `u305` 現在的講法也行，那就把 `u311` 改成 `再往上一大截，機翼還曬得到太陽。`
兩個擇一即可，我不堅持哪一個。

**問題 4. 標題與 `u113` 的「正式」比說明欄的「刻意」弱**

說明欄現在寫「才**刻意**印在正式文件上」，正是路透社的 deliberate；
標題與 `u113` 寫的是「才**正式**印出來」。但第 4 章的章名就叫「一九六七年，這兩個字已經印過了」，
而 1967 那一份本來就是 CIA 的正式文件。這個張力影片自己有收（`u407`／`u408` 說那是無意的、
`u712` 給出路透社的用詞），所以當作有意的懸念讀得通，第一版兩輪與第一輪也都這樣放行。

我同意不擋，但要記一筆：**這是全片唯一一處要靠後面四章才解得開的措辭**。
站主若要一次收乾淨，`u113` 改成 `一個地圖編號，為什麼等了五十八年才刻意印出來？`（21 單位，長度不變）
就和說明欄同一把尺了；標題同理。

**問題 5. 「右下角標著拉斯維加斯」**（`u707b`）：見疑點 1，建議 `右邊偏下標著拉斯維加斯。`（11 單位）。

## 第一輪過了的地方，我再確認一次沒有被改壞

- **三個 `loops` 都兌現，而且兌現的是觀眾還沒有的東西**（`script-writing.md`：點名不等於回收）：
  `u103`→`u317`，後面接 `u318`–`u320`（CIA 計畫史「一半以上」那一句＋沒有統計）——新事實；
  `u508`→`u715`，後面接 `u716`（CIA 發言人 Edward Price 的原話）——新事實；
  `u619`→`u713`，後面接 `u714`（新版仍有大量塗黑、16 卷 OSA 內部史還沒全部公開）——新事實。
  三組都不是把埋設句再念一次。
- **每一章的第一句都接得上**：`u201`（接下來發生了什麼）、`u301`（直接回答 `u220`「要飛多高」）、
  `u401`（回答 `u326`「飛的已經不是它了」）、`u501`（接 `u419` 的 1977 數十二年）、
  `u601`（回答 `u520`「政府怎麼稱呼」）、`u701`（兌現 `u624`「然後他等」）。
  沒有一句是標籤句（「先講…」「回到…」「接下來」「第 N 頁」）。
- **數字**：145 句裡唯一重複的數量詞是「四萬英尺」兩次（問題 3），沒有任何數字出現在三句以上。
- **長度**：145 句全部在 24 單位以內（最長 `u617` 24、`u325` 22、`u714` 22——正好是第一輪改長的三句，
  都還壓在線內），合計 1,991 單位。沒有括號、沒有網址、沒有「經查證」類字眼，
  沒有任何一句帶 `say`／`say_for`，所以上面的建議改法都不會動到發音表。
- **沒有宣稱定論**：`u719`「現在在試什麼，仍然是機密」、`u722`／`unsettled` 卡「未結」都誠實；
  第 5 章傳說段的歸屬在章名、`u502`–`u507`、卡片 kicker 與 `u508` 四個地方都有。

## 懷疑但沒要求改

- **「還記得…」在第 7 章擠成一串**：全片四句（`u317`、`u710`、`u713`、`u715`），沒有超過五句的上限，
  每一個掛鉤也都隔了好幾分鐘，所以規則上過關。但 `u710`、`u713`、`u715` 擠在最後八句裡、
  各自只隔一兩句，正是 `script-writing.md` 記下 H01 盲評讀者說「聽得出來是公式」的那個形狀。
  這不是查核問題，也不是這 18 處改動造成的（第一輪判 OUT OF SCOPE），記給撰稿與盲評關卡參考。
- **`u705`「舊版連地圖那一頁都沒有」**：那一頁在，是整頁塗黑。效果上成立，要更精確可寫「整頁塗黑」。
- **第一輪 #55 的腳註位置**：「OSA History, chap. 7, pp. 17-19」印在書頁 72 頁底，書頁 73 頁底只有
  "Information supplied by James Cunningham to Donald E. Welzenbach (U)"。兩條都不是統計，`u320` 不受影響。
- **`u706`「四百多頁」**：路透社寫 400-page，406／407 這兩個精確數字只在 CIA 閱覽室與新聞上，
  閱覽室今天（和第一輪一樣）轉到首頁打不開。三個數字之間「四百多頁」都成立，保留。
- **會過期的事實**：和第一輪一樣兩件仍懸——2003 年之後總統豁免令有沒有再簽
  （聯邦公報 API 今天仍只到 2003-10-21）、16 卷 OSA 內部史公開到什麼程度。
  說明欄「資料截至 2026-10-10」今天重開全部沒有變，仍然成立。

## 結論

**還不能進畫面與旁白；兩處改完就可以。**

必改兩處：
1. `u413` 的「一九七四年」（事實：來源只把 1974 給了備忘錄，沒給拍照），連帶 `u415` 與 `claims.md` c28；
2. `altitude-stats.stats` 的三格順序（卡片與旁白差一拍，三句三格全部對不上）。

建議三處（`u305`／`u311` 的「四萬英尺」二選一、`u113` 與標題的「正式」→「刻意」、`u707b` 的「右下角」），
由撰稿與站主決定，不擋。

第一輪的 18 處改動**全部成立**，其中撰稿自己改寫的兩處（`u305`、說明欄第 1 段）依來源判也都站得住，
說明欄那一處還比第一輪的建議準；`claims.md` 的 S–W 五項都做了，我也各自驗過底。
七個章名全部對得上來源與章內的句子。102 條 CONFIRMED 抽查 42 條（41%），41 條維持 CONFIRMED，
1 條（`u413` 的年份）翻成 NOT FOUND。第一輪留下的六個疑點，四個判成立、一個要改（1974）、
一個建議收乾淨（右下角）。

**第三輪：不需要**——這一輪只動 1 個事實與 1 項卡片設定，沒有超過 3 個。
改完之後請撰稿跑一次 `lint`（我依啟動說明沒有跑任何影片階段）：`altitude-stats` 只是重排三格的順序，
揭示數仍是 3／3、狀態仍是三個，秒數不會變；`u413`／`u415` 的長度一增一減，整支片的估計時長也不會變。
