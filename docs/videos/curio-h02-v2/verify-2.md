# curio-h02-v2 查核第二輪

- 查核 2026-10-13，Claude Opus 5（第二輪的獨立查核代理）。**我不是寫這份腳本的那一個，也不是
  查核第一輪的那一個**：`video.json`、`claims.md`、`brief.md`、`NOTES.md`、`verify-1.md` 五份都不是
  我寫的，這一輪我一個字都沒有改它們。我寫的只有這一份 `verify-2.md`。
- 為什麼有第二輪：這一集在本倉庫沒有第一版，腳本是直接照
  [`../history-curiosity/topic-checks/H02.md`](../history-curiosity/topic-checks/H02.md)
  （2026-10-10 查核＋同日獨立覆核，ADOPT_WITH_CHANGES）寫成的，
  [`verify-1.md`](verify-1.md) 要了二十二條改動（十七條內容、五條出處），全部已經套進檔案裡，
  而它自己要求「第二輪請換人，重查這二十二條，再抽三分之一的 CONFIRMED」。
- 方法：
  1. 先把 `video.json` 重讀一遍，用腳本把 123 個場景、131 句旁白、9 張卡片的每個 `data` 欄位、
     七個章名、標題、五段說明欄、十個標籤、縮圖、`sources[]`（20 筆）與 `loops[]`（4 組）抽出來，
     確認全檔**沒有任何 `say`／`say_for`**（所以沒有第二種唸法要查）。最長的一句是 `ro311`，
     23 個字（不含標點）。
  2. 查核一要的二十二條，逐條去比**現在檔案裡的字**，再去比來源原句——不看查核一的判斷，
     自己重讀來源那一段。十七條內容改動用 `grep` 確認舊的字串一個都沒有留在 `video.json` 裡
     （樹皮、出不了港、開不出去、每年上演、歷史書、離開的三個、殖民者在島上的三年、二〇二五年一月、
     一件都還連不上、在島上首演、像他們一樣、年輪窄、上岸以後：全部 0 筆）。
  3. 二十六個網址當天用 `curl` 重開（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com;
     support@mokaair.com)`，同一主機間隔 1.2 秒以上；兩本 Gutenberg 讀全文檔，兩個 PDF 用
     `pdftotext` 抽文字，HTML 自己寫腳本去標籤後讀全文）。原始檔與腳本在
     `<scratch>\verify2-h02\`（`raw/` 底下是當天抓的原頁）。上一次嘗試留下的檔案我沒有沿用，
     全部重抓、重判。
  4. 一五八七年那張名單的 119 個名字**我自己重數一次**（結果見〈CONFIRMED 抽樣〉第 34 列）。
  5. 網路搜尋用了 2 次、`WebFetch` 1 次，都只為了那兩件會過期的事實（見該節）。
- 這是歷史題，「官方頁」指一手或權威來源。最重的是 Gutenberg 的 Hakluyt 卷 13 所收懷特 1587、
  1590 兩篇記述（唯一的目擊紀錄）與 Lawson 1709，以及國家人文中心那份**現代拼字版**的 1590 記述
  ——這一輪我特意用它去對 Hakluyt 的古拼字，兩邊逐字一致，所以「樹／木樁」那一段不是我讀錯古字。
  其次是美國國家公園管理局三頁、Encyclopedia Virginia、Britannica 兩頁、NCpedia 三頁；
  報導層是 Smithsonian 2017／2020、National Geographic 2015、WHRO 2025、Coastal Review 2020、
  NCLR 書評；基金會自己的網頁只當「他們自己說」用。science.org 的全文頁我沒有開（H02.md 記它對
  機器回 403、沒有可用存檔），摘要走 NCBI，跟 H02.md 與查核一同一條路。
- `assets[]` 是空的、沒有照片卡，所以沒有圖片授權要查；H02.md 的六張公有領域圖與站主要決定的三件
  這一版都沒有入稿。
- 我沒有跑 git、沒有跑任何影片階段、沒有跑 `lint`、沒有花任何提供者的錢。

## 當天開過的網址（2026-10-13）

| 縮寫 | 網址 | HTTP |
|---|---|---|
| HAK-txt | https://www.gutenberg.org/cache/epub/25645/pg25645.txt （實際比對引句用的全文檔；檔頭標 Volume 13、Richard Hakluyt） | 200 |
| HAK | https://www.gutenberg.org/ebooks/25645 （`sources[]` 第 1 筆） | **504、504、504，第四次 200** |
| HAK-files | https://www.gutenberg.org/files/25645/ | 200 |
| LAW-txt | https://www.gutenberg.org/cache/epub/1838/pg1838.txt （檔內「This book was originally published in London in 1709」） | 200 |
| LAW | https://www.gutenberg.org/ebooks/1838 | 200 |
| NHC | https://nationalhumanitiescenter.org/pds/amerbegin/exploration/text6/white.pdf （現代拼字版，`pdftotext` 抽文字） | 200 |
| NPS87 | https://www.nps.gov/fora/learn/historyculture/1587-the-lost-colony.htm （Last updated: September 20, 2026） | 200 |
| NPS90 | https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm （Last updated: August 14, 2026） | 200 |
| NPSth | https://www.nps.gov/fora/learn/historyculture/major-theories-of-the-lost-colony.htm （**Last updated: July 11, 2025**，與查核一同一個日期） | 200 |
| EV | https://encyclopediavirginia.org/entries/roanoke-colonies-the/ | 200 |
| EBp | https://www.britannica.com/place/Lost-Colony （我抓到的 HTML 裡沒有更新日期的字串，只有「most recently revised and updated by」沒有日期） | 200 |
| EBs | https://www.britannica.com/story/the-lost-colony-of-roanoke （查核一要補進 `sources[]` 的那一條，已經補了） | 200 |
| NCp | https://www.ncpedia.org/lost-colony | 200 |
| NCpC | https://www.ncpedia.org/croatoan-indians | 200 |
| NCpD | https://www.ncpedia.org/dare-stones | 200 |
| SM17 | https://www.smithsonianmag.com/history/mystery-roanoke-endures-yet-another-cruel-twist-180962837/ （April 7, 2017） | 200 |
| SM20 | https://www.smithsonianmag.com/smart-news/new-evidence-roanoke-colonys-disappearance-180976248/ （November 9, 2020） | 200 |
| NG | https://www.nationalgeographic.com/culture/article/150807-lost-colony-roanoke-hatteras-outer-banks-archaeology | 200 |
| WHRO | https://www.whro.org/arts-culture/2025-01-20/new-artifacts-on-hatteras-point-to-the-real-fate-of-the-lost-colony （Published January 20, 2025 at 3:40 AM EST） | 200 |
| FCF | https://www.firstcolonyfoundation.org/news/lost-colony-is-found/ （`article:published_time` 2026-06-04T18:48:06Z、`dateModified` 2026-06-04T18:52:03Z） | 200 |
| FCF2 | https://www.firstcolonyfoundation.org/news/scientific-tests-confirm-archaeology-discovery/ （銅耳飾；新聞索引把它列為 August 21, 2024） | 200 |
| FCF-news | https://www.firstcolonyfoundation.org/news/ （這一輪多開的：確認基金會在那則宣布之後沒有再發任何東西） | 200 |
| FCF-dig | https://www.firstcolonyfoundation.org/archaeology/dig-reports/ （這一輪多開的：基金會自己的「發掘報告」頁） | 200 |
| CR20 | https://coastalreview.org/2020/10/lost-colony-moved-inland-archaeologists/ | 200 |
| NCLR | https://nclr.ecu.edu/wp-content/pv-uploads/sites/460/Haspel-EwenShields-review.pdf （`pdftotext` 抽文字，含圖說） | 200 |
| SCI | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9554842&rettype=abstract&retmode=text | 200 |
| EBSCO | https://www.ebsco.com/articles/history/88670256-…/excavating-the-lost-colony-mystery-…-review （為了那兩件會過期的事實查的，見該節） | **403** |

沒有開：https://www.science.org/doi/10.1126/science.280.5363.564 （H02.md 記 403、無可用存檔，摘要讀
SCI 那一列）。Commons 沒有開（`assets[]` 空）。

**關於那三個 504**：`sources[]` 第 1 筆（Gutenberg 的書目頁）連吃三次 504 Gateway Time-out，
第四次就 200；同一主機的 `/ebooks/1838`、`/files/25645/` 與兩個全文檔全程 200，所以那是暫時性的。
說明欄的參考資料會把這個網址給觀眾看，上架前順手再開一次就好，**不需要改檔**。

## 查核一的二十二條改動，逐條重判

「現在的字」是我今天從 `video.json`／`claims.md` 讀出來的原字。判定只有兩種：**支持**（這句話照現在
的寫法指得到來源原句）、**不支持**（指不到，要再改一次）。

### 旁白、卡片、章名、說明欄（十七條）

| # | 位置 | 現在的字 | 來源原句 | 判定 |
|---|---|---|---|---|
| 1 | `ro104`＋說明欄 ¶1 | 靠岸之前，他們吹號，唱英格蘭的歌。 | HAK-txt：「we let fall our Grapnel neere the shore and sounded with a trumpet a Call, and afterwardes many familiar English tunes and Songs, and called to them friendly; but we had no answere, **we therefore landed at day-breake**」；NHC 現代拼字版同句「…we therefore landed at day-break」 | **支持**（次序對了：號聲與歌在小船上，沒有回應才上岸） |
| 2 | `ro107` | 一棵樹上，刻著三個大寫字母。 | HAK-txt：「vpon a tree, in the very browe thereof were curiously carued these faire Romane letters C R O」（**沒有**樹皮）；NHC：「upon a tree, in the very brow thereof were curiously carved these fair Roman letters C R O」；NPS90：「White found "CRO" carved into a tree」；EBp：「the letters CRO on a tree」 | **支持** |
| 3 | `ro409`、`loops[1].what` | 還記得樹上那三個大寫字母嗎？／樹上那三個字母後來變成什麼 | 同上；`loops[1].what` 也已經跟著改掉 | **支持** |
| 4 | `ro301` | 可是那幾年，英格蘭正在打仗。 | EV：「Queen Elizabeth **had been** fighting the Spanish on the seas and in the Netherlands」；NPSth 另有更直接的一句：「**In the summer of 1587, Spain and England were in the midst of war.**」（懷特是 1587 年 8 月走的） | **支持**（NPSth 那一句比查核一引的 EV 更硬，建議 `claims.md` c16 補掛） |
| 5 | `ro404` | 還會像英格蘭人一樣，對著一本書說話。 | LAW-txt：「These tell us, that several of their Ancestors were white People, and could talk in a Book, **as we do**」——「we」是勞森那邊的英格蘭人 | **支持** |
| 6 | `ro413` | 一八三〇年代，一本書和一篇雜誌文章這樣寫它。 | SM20：「the image of Roanoke as a "Lost Colony" only got its start in the 1830s, when **a book and a magazine article** cast the settlement as a "romantic mystery"」 | **支持** |
| 7 | `ro514` | 二〇二五年初，又挖到成桶的鍛鐵碎屑。 | WHRO（Published January 20, 2025）：「Archaeologists **recently** found "buckets" of hammer scale on Hatteras Island」 | **支持**（比「一月」穩；殘留的一點見〈建議〉3） |
| 8 | `ro615` | 那兩個工地的器物，沒有一件能確定屬於他們。 | NPSth：「Even the artifacts found there have **not been definitively linked** to the Lost Colony.」同段還寫發掘者「believe may have belonged to the colonists」 | **支持** |
| 9 | `ro504` | 那份研究從年輪的**寬窄**，看出雨水多少。 | SCI 摘要全文只有：「**Tree-ring data from Virginia** indicate that the Lost Colony of Roanoke Island disappeared during the most extreme drought in 800 years (1587-1589)…These extraordinary droughts can now be implicated…」——**沒有一個字寫年輪怎麼讀，沒有「寬窄」** | **不支持**（見〈還要改的地方〉2；`claims.md` c20 自己也記了這一點） |
| 10 | `ro416` | 一九三七年，一齣戶外劇開始上演。 | NCLR：「The year 1937, the time of the **premiere** of Paul Green's outdoor drama The Lost Colony」 | **支持**（地點的事見〈建議〉5） |
| 11 | `count-stats`.stats[0].note | 其中三個沒有留下 | 三個人裡的 George How 是**留在島上被殺**的，不是沒有留下：HAK-txt「The eight and twentieth, George Howie, one of our twelue Assistants was…」（1587-07-28）、NPS87「Native people ambushed and killed a colonist name George Howe」；而 119－3＝116 沒有來源寫，EV 兩處都寫懷特走時「leaving behind **117** settlers」「the **117** colonists he left at Roanoke Island」 | **不支持**（見〈還要改的地方〉3） |
| 12 | `drought-stats`.stats[0].label | 論文算出的乾旱年份 | SCI 摘要：「the most extreme drought in 800 years **(1587-1589)**」——那是論文算出來的乾旱年份，不是任何人在島上的三年 | **支持** |
| 13 | `added-later`.rows[3][2] | 首演 | NCLR 只寫 premiere；我把 NCLR 全文重搜一次，沒有 annual／every summer／every year | **支持** |
| 14 | `added-later`.rows[1][1] | 一本書和一篇文章 | 同第 6 條（SM20） | **支持** |
| 15 | `war-at-home`.chapter（第 3 章章名） | 無敵艦隊那一年，他的補給送不到島上 | EV：「**Despite a prohibition on all English ships leaving port**, Raleigh managed to arrange for a two-ship relief mission that **sailed on April 22, 1588**…But **a fight at sea with the French left the ships limping back to England**」；EV 年表另寫那兩艘是 the Brave 與 the Roe、從 Bideford 出發；NCp：「White was able to get away to sea that year in two small vessels with 15 new settlers, but these ships were beset by calamities…and **returned home**」；補給到 1590 年還是沒送到：NPS90、HAK-txt | **支持**（船確實開出了港，章名現在說的是「送不到島上」） |
| 16 | 說明欄 ¶2 | 無敵艦隊那一年補給為什麼送不到 | 同上 | **支持** |
| 17 | 說明欄 ¶1 | 一棵樹上刻著三個大寫字母 | 同第 2 條 | **支持** |

### 出處（五條，不影響旁白）

| # | 位置 | 現在的狀態 | 我重查的結果 | 判定 |
|---|---|---|---|---|
| 18 | `sources[]` | 二十筆，第 8 筆就是 Britannica 故事頁（EBs），`checked_on` 2026-10-10 | EBs 今天 200，而且 c28 引的那一句確實在那一頁上：「The word CROATOAN and the letters CRO, **carved into trees** within the colony's borders」 | **支持** |
| 19 | `claims.md` c40 | 改掛 NPSth＋NG＋SM17＋FCF＋SM20 | 「2012＋大英博物館」三條都在：NG「part of the British Museum's permanent collection, the document **made headlines in 2012**」、SM17「The digs by the First Colony Foundation were sparked by the **2012** discovery of a patch concealing the image of a fort on a map painted by John White」、FCF「**in 2012**, we asked a First Colony board member to determine if the **British Museum** knew what lay underneath two small paper patches」。我也驗了反面：SM20 全文搜不到「2012」，NPSth 沒有任何年份 | **支持** |
| 20 | `claims.md` c42 | `ro610` 改掛 SM20，CR20 留給 `ro608`／`ro609` | SM20：「"**I am skeptical**," Charles Ewen, an archaeologist at East Carolina University…tells National Geographic」（SM20 是 2020-11-09，與 CR20 同年，所以 `ro610` 的「同一年」對）；CR20 全文搜「skeptic」0 筆，而「We all agree that is not the major relocation site of the Lost Colony」確實在 CR20（Luccketti 談 Site Y） | **支持** |
| 21 | `claims.md` c30、`added-later`.source | 補掛 NCLR；卡片出處現在是「NCpedia、NCLR、Smithsonian 2026-10-10」 | 1937 年首演只在 NCLR；NCp 提 Paul Green 只在一張照片的圖說裡（「Roanoke colonists leave Fort Raleigh at the climax of Paul Green's dramatic recreation…」），沒有年份；NCpD 沒有提那齣戲 | **支持** |
| 22 | `claims.md` 編號 | 原本跳掉的 c20 補成樹輪研究做法那一列，排在 c32 後面 | 我用腳本數過：c1–c45 共 45 列，**沒有缺號、沒有重號** | **支持** |

**計數：二十二條裡二十條支持（其中第 7 條帶一個殘留的但書），兩條不支持**——第 9 條（`ro504`
的「寬窄」）與第 11 條（人數卡的註「其中三個沒有留下」）。兩條都要再改一次，寫在
〈還要改的地方〉。

### 啟動說明要我讀兩次的三件事

**（一）樹皮。** 兩個獨立的轉錄本逐字一致，分得乾乾淨淨：

- 樹：「as we entered vp the sandy banke **vpon a tree, in the very browe thereof** were curiously
  carued these faire Romane letters **C R O**」（HAK-txt）／「upon a tree, in the very brow thereof
  were curiously carved these fair Roman letters C R O」（NHC）。**整句沒有 bark。**
- 木樁：「one of the chiefe **trees or postes at the right side of the entrance had the barke taken
  off**, and **5 foote from the ground** in fayre Capitall letters was grauen **CROATOAN without any
  crosse or signe of distresse**」（HAK-txt）／NHC 同句「…had the bark taken off, and 5 feet from the
  ground in fair capital letters was graven CROATOAN without any cross or sign of distress」。

所以：樹上三個字母（`ro107`）✓、木樁整個字（`ro108`–`ro110`）✓、離地五英尺（`ro109`、
`the-word`.sub）✓、字上沒有十字（`ro111`）✓，剝皮只屬於木樁（`ro108`）✓。
轉述層也支持這個分法：NPS90「White found "CRO" carved into a tree and "CROATOAN" carved into a
palisade」、EBp「the word CROATOAN carved on a post of the palisade erected by the settlers and the
letters CRO on a tree」、NCpC「the word "CROATOAN," carved in a post, was found by John White in
1590」。**查核一這一條改得對，現在的字站得住。**
（「大寫」：樹那一句原文是 faire **Romane** letters、木樁那一句才是 fayre **Capitall** letters；
但原文把樹上那三個字寫成 C R O、NPS90 與 EBp 也寫成 CRO，所以「三個大寫字母」留著沒問題。）

**（二）補給。** EV 同一段把兩件事都寫清楚了：女王禁止所有英格蘭船出港（「Despite a prohibition on
all English ships leaving port」），**但那兩艘船還是在 1588-04-22 開出去了**（the Brave 與 the Roe，
從 Bideford），是「a fight at sea with the French left the ships limping back to England」；
NCp 用另一個說法寫同一件事（「these ships were beset by calamities…and returned home」）。
所以舊章名「出不了港」是錯的，現在的「送不到島上」對；而且旁白 `ro303`（女王下令船留在本土）與
`ro304`（四月出發、交戰後折返）並排放在一起也不矛盾——NPS90 的原句是「Queen Elizabeth I ordered
all English vessels to **remain nearby** in defense of the homeland」，EV 的「prohibition」與那兩艘
船的例外是同一段話。**改得對。**

**（三）乾旱卡。** SCI 摘要只說「the Lost Colony of Roanoke Island **disappeared during** the most
extreme drought in 800 years (1587-1589)」，一個字都沒有說那批人在島上待了那三年；NPSth 寫的是
「a major drought struck the Outer Banks in 1587 and lasted for three years」，講的是乾旱，不是人。
而 NPS87 同時寫懷特走前「the remaining colonists split into two groups. One group would stay on
Roanoke Island through the winter. Another would go inland」——他們幾時離開羅阿諾克正是全集說沒有
定論的事。所以舊標籤「殖民者在島上的三年」是把一個沒有來源的事寫在畫面上，現在的
「論文算出的乾旱年份」對。**改得對。**

## H02.md 拒絕的四件事，我自己再答一次

**1. 不給單一人數——仍然被拒絕，守住了。**
我用 `grep` 把 `video.json` 整檔搜過：`115`／`117`／`118`／一百一十五／一百一十七／一百一十八
**都是 0 筆**，「一百多」只出現一次（`ro207`）。卡片 `count-stats` 把兩件事並列：
「119／名單上的名字」與「100–150／各家來源的說法」，旁白 `ro208`「名單上的名字」、
`ro209`「各家來源寫的」用詞也沒有把名單當人數。各家來源我今天逐頁重讀：EBp「approximately **100**
settlers」、SM17「**115** men, women, and children」、EV「**117** settlers」、NPS87「consisting of
**118** men, women, and children」、NPSth「an additional **117** people」、NCp「approximately **150**
men, women, and boys」、WHRO「**More than 100** colonists」——100 到 150 這個範圍對。
**但那張卡的註「其中三個沒有留下」我判不支持**（見〈還要改的地方〉3）：這一件被拒絕的事守住了，
守它的那一行註腳自己沒有來源。

**2. 不說「樹上刻著 CROATOAN」——仍然被拒絕，守住了，而且比第一輪更乾淨。**
樹（三個字母）與木樁（整個字、離地五英尺、沒有十字）在 `ro107`–`ro111` 分開講、`the-word` 卡的
kicker 直接寫「柵欄的木樁上」；第 4 章 `ro410` 把「樹上刻著一個字」標成後來的講法，`ro411` 說誰
最先這樣講查不到。來源原句見上一節（一）。流傳版那一邊也有三個來源在：EBs「carved into **trees**」、
NCp「cut into a **tree or post** of a palisade」、WHRO 引發掘方自己轉述「they left behind this
cryptic message **on a tree**, 'Croatoan'」。全檔「樹皮」0 筆。
插圖也沒有把分別糊掉：`three-notches`／`remember-three-letters` 畫的是樹皮上三道新削的刻痕，
`stripped-post`／`five-feet` 畫的是一整根**剝得精光**的木樁——辨識特徵還在畫面上，而且刻字要削開
樹皮才看得到，所以圖沒有宣稱任何錯的事。

**3. 與克羅托安人同住只是「最受歡迎的說法之一」——仍然被拒絕，守住了。**
NPSth 原句：「The third theory involving the colonists leaving Roanoke Island is, **perhaps, one of
the most popular and compelling**」；`ro704` 說「只是最受歡迎的說法之一」，比來源更保守。
全檔「主流」「證實」「謎團已解」各 0 筆。而且這句之前先放了 `ro701`「沒有」、`ro702`–`ro703`
國家公園管理局 2025 年那句（原句「no human remains, graves, buildings, or village sites have been
definitively linked to the Lost Colony」），之後接 `ro705` 兩位專書作者的「不知道」與片尾卡的「未結」。
**但第 7 章的章名把「能確定」漏掉了**（見〈還要改的地方〉1）——那是查核一第 8 條剛修好的同一個毛病，
只是它漏掉了章名。

**4. 二〇二六年內陸的「找到了」只能當基金會自己的宣稱——仍然被拒絕，守住了。**
我今天自己把 FCF 那一頁從頭讀到尾：標題「The Lost Colony is Found! How We Did It.」、
第一句「This is not another hoax or false claim.」、結論「Site X and Site Y were part of a larger,
dispersed settlement of farms along the Chowan River, where **117 immigrants established their New
World home**」；`article:published_time` 是 2026-06-04T18:48Z。**那一頁沒有附任何發掘報告**
（全頁沒有 PDF 連結，「report」只出現在導覽列與一句引述裡）。我另外開了基金會自己的
「Archaeological Dig Reports」頁：上面只有 Fort Raleigh 外堡那幾份，**沒有 Site X／Site Y 的報告**
——而 CR20 在 2020 年還寫「Reports on the Site X and Site Y work will be completed in coming months
and posted on the foundation's website」。基金會的新聞索引顯示那則宣布是**最新的一則**，
上一則是 2024-10-17。
腳本把這些都標明了：`ro611`「同一個基金會改口了」、`ro612`「他們在**自己的網頁**上宣布」、
`found-it` 卡的 sub「基金會自己的網頁」、`ro613`「那則宣布沒有附新的發掘報告」、
`ro614`「到今天也沒看到第三方的評估」；而且 2020 年那兩句（CR20 的「is not the major relocation
site」與 SM20 的「I am skeptical」）放在前面、沒有被寫成對 2026 年宣告的回應。
**時間順序沒有被弄反，守住了。**（我今天重搜的結果見〈兩件會過期的事實〉。）

## 七個章名，逐個判

章名會進 YouTube 的章節列，觀眾是**在列表裡一條一條讀**的——所以我也用「單獨讀會不會讀錯」這把尺
量了一次。查核一只動過第 3 章，其餘六個沒有抽。

| # | 場景 | 章名 | 這一章實際講什麼 | 來源 | 判定 |
|---|---|---|---|---|---|
| 1 | `daybreak-outer-banks` | 他們吹了號，島上沒有人回應 | 天亮上岸、吹號、沒有回應、剩下的東西、樹上三個字母、木樁上的字、沒有十字、他反而很高興 | HAK-txt「sounded with a trumpet a Call…but we had no answere」；NPS90「no signs of life」 | **過**（而且改成「靠岸之前」以後，章名沒有說他們在岸上吹號，仍然對得上） |
| 2 | `his-own-sign` | 他們簽了一張紙，請總督回英格蘭 | 約定、1587 年的島上、外孫女出生、全體請求、聯名證明、他上船、約定的十字 | HAK-txt 的證明全文：「we all of one minde and consent, haue most earnestly intreated…Iohn White, Gouernour of the planters in Virginia, **to passe into England**」、署「the 25 of August 1587」「vnder all their handes and seales」 | **過** |
| 3 | `war-at-home` | 無敵艦隊那一年，他的補給送不到島上 | 打仗、無敵艦隊、禁止出港、四月的船折返、補給沒送到、他回來卻過不去、五十英里的矛盾 | 見上面第 15 條 | **過**（查核一改對了） |
| 4 | `island-people-say` | 一七〇九年，有人說祖先是白人 | 勞森 1709、白人祖先、二手的屠殺說、樹與木樁被記反、名字、戶外劇、刻字石 | LAW-txt「These tell us, that several of their Ancestors were white People」；檔內「originally published in London in 1709」 | **過**（「有人說」沒有說錯，但單獨讀有點含混，見〈建議〉6） |
| 5 | `dig-1998` | 島上的土裡，挖出一只戒指 | 1998 年的戒指、樹輪與乾旱、回去挖、鐵劍柄、鍛鐵碎屑、2017 年驗出黃銅、年代的但書 | NG「In 1998, archaeologists from East Carolina University found a ten-carat gold signet ring here」（here＝**哈特拉斯島**的 Cape Creek） | **要改**（戒指是在南邊那座島挖到的，不是羅阿諾克；而第 3 章章名裡的「島上」指的正是羅阿諾克——同一列章節名裡「島」指了兩座島，見〈還要改的地方〉4） |
| 6 | `british-museum-map` | 地圖的補丁底下，有一個堡壘的記號 | 2012 年的補丁、伯蒂郡、兩個工地、2020 年自己人的保留、2026 年的宣稱 | NPSth「On a map created by John White, there is **a patch covering a fort-like symbol**」 | **過** |
| 7 | `no-such-thing` | 沒有遺骸，也沒有能確定的房子 | 「沒有」、NPS 2025 年的說明、最受歡迎的說法之一、兩位學者的「不知道」、我的看法 | NPSth「no human remains, graves, buildings, or village sites have been **definitively linked** to the Lost Colony」 | **要改**（「能確定」只管到房子，沒有管到遺骸；旁白 `ro703` 已經是對的寫法，章名反而留著查核一第 8 條剛修掉的那個毛病，見〈還要改的地方〉1） |

## CONFIRMED 抽樣：四十四列（查核一 CONFIRMED 103 列的 43%）

**怎麼挑的**（不是隨機，是挑最會出事的）：(A) 這一集立論所在的樹／木樁那一段全抽；
(B) 觀眾查得到、查核一只掛一個來源的年份與數字；(C) 帶引述的句子（引錯一個字就變另一件事）；
(D) 只有單一來源或「沒有」型的主張；(E) 畫面上的卡片字（觀眾讀得到，改起來最貴）。
另外三列（#103、#109、#117）查核一判 CONFIRMED 但在文末留了〈建議〉，我一併重查，所以實際查了 47 列。

| 查核一 # | 位置 | 我今天看到的來源原句 | 判定 |
|---|---|---|---|
| 13 | `ro101` 一五九〇年八月十八日，天剛亮 | NPS90「**Landing on August 18, 1590**」；HAK-txt「we therefore landed at day-breake」 | CONFIRMED |
| 17 | `ro105` 沒有人回應 | HAK-txt「but we had no answere」 | CONFIRMED |
| 18 | `ro106` 聚落裡只剩下他們留下的東西 | NPS90「found remnants of the colonists but no signs of life」；HAK-txt（鐵條、兩塊鉛、四門小砲、被挖開的箱子） | CONFIRMED |
| 20 | `ro108` 柵欄入口有一根木樁被剝了皮 | HAK-txt／NHC「one of the chiefe trees or postes at the right side of the entrance had the barke taken off」 | CONFIRMED |
| 21 | `ro109` 離地五英尺，刻著一整個字 | 「5 foote from the ground in fayre Capitall letters was grauen CROATOAN」 | CONFIRMED |
| 22 | `the-word` 卡（CROATOAN／柵欄的木樁上／離地五英尺） | 同上；EBp「carved on a post of the palisade」；NCpC「carved in a post」 | CONFIRMED |
| 23 | `ro110` 那個字是克羅托安 | 同上 | CONFIRMED |
| 24 | `ro111` 字的上面，沒有十字 | 「grauen CROATOAN **without any crosse or signe of distresse**」 | CONFIRMED |
| 25 | `ro112` 他後來寫下，看到這個字，他反而很高興 | HAK-txt「but although it much grieued me to see such spoyle of my goods, yet on the other side **I greatly ioyed** that I had safely found a certaine token of their safe being at Croatoan」 | CONFIRMED |
| 29 | `ro203` 一五八七年七月二十二日，他們在外灘靠岸 | HAK-txt「**The two and twentieth of Iuly** wee arriued safe at Hatorask」 | CONFIRMED |
| 30 | `ro204` 本來要去的，是北邊的乞沙比克灣 | HAK-txt「the **Bay of Chesepiok** where we intended to make our seate and forte」；NPS87「intended to make a new colony in the Chesapeake Bay」 | CONFIRMED |
| 34 | `ro208`／`count-stats` 名單上的名字一共一百一十九個 | **我自己重數**：HAK-txt「The names of all the men, women and children, which safely arriued in Virginia, and remained to inhabite there. 1587.」底下，男 **91**、Women **17**、Boyes and children **9**、Children borne in Virginia **2**＝**119**（另有 Manteo、Towaye 兩個名字列在「Sauages that were in England and returned home」那一節，不算在這 119 裡）。唯一要留意的是男丁名單裡「Henry Rufoote」那一行少了句點，在這份快取文字檔裡它自己佔一行，所以不會被數成一個名字 | CONFIRMED（與查核一、H02.md 同為 119） |
| 41 | `ro214` 四天後，全體殖民者找上他 | HAK-txt「The next day, **the 22 of August**, the whole company both of the Assistants and planters came to the Gouernour」（8/18＋4） | CONFIRMED |
| 42 | `ro215` 他們要他回英格蘭，親自把補給帶回來 | 「with one voice requested him to returne **himselfe** into England, for the better and sooner obtaining of supplies」 | CONFIRMED |
| 44 | `ro217` 八月二十五日，他們立下一張聯名的證明 | 證明全文署「the 25 of August 1587」，前文「vnder all their handes and seales」 | CONFIRMED |
| 45 | `ro218` 兩天後的早上，他上了船 | 「departed from Roanoak **the seuen and twentieth of August in the morning** and the same day about midnight, came aboord the Flieboat」 | CONFIRMED（措辭的事見〈建議〉2） |
| 46 | `ro219` 那時候外孫女出生才九天 | 8/18→8/27 | CONFIRMED |
| 47 | `ro220`–`ro222` 約好的記號／刻地名／加十字 | 「a secret token agreed vpon betweene them and me at my last departure from them」「they should not faile to write or carue on the trees or posts of the dores the name of the place where they should be seated」「they should carue ouer the letters or name, a Crosse + in this forme」 | CONFIRMED |
| 48 | `ro223`／`ro224` 沒有十字就是平安 | 「but we found no such signe of distresse」＋「a certaine token of their safe being at Croatoan」；EV 的轉述「To White's relief, no such cross could be found」 | CONFIRMED |
| 51 | `ro302` 一五八八年，西班牙的無敵艦隊來了 | NPS90「The Spanish Armada…was preparing to attack England directly」；NCp「The Spanish Armada of 1588」 | CONFIRMED |
| 53 | `ro304` 那年四月出發的補給船，跟法國人交戰後折返 | EV「a two-ship relief mission that sailed on **April 22, 1588**…a fight at sea with the French left the ships limping back to England」 | CONFIRMED |
| 54 | `ro305`／`delay-stats` 卡（1587 他離開、1590 他回來） | HAK-txt（1587-08-27 離開）＋NPS90（1590-08-18 上岸） | CONFIRMED |
| 57 | `ro310` 懷特自己寫，那是他們的朋友 | HAK-txt「the Sauages of the Iland **our friends**」 | CONFIRMED |
| 63 | `ro317` 八月二十八日，一場風暴把船吹向亞速群島 | HAK-txt「**On the 28.** the winde changed…wee were driuen to change our first determination for Trynidad, and stoode for the Ilands of **Açores**」 | CONFIRMED |
| 65 | `ro320` 那次道別之後，沒有紀錄說英格蘭人再見過他們 | NCp「His departure marked **the last known contact** between the English and their colony in America」 | CONFIRMED |
| 67 | `ro322` 他寫過，他們準備搬到內陸五十英里 | 1590 篇「for at my comming alway they were prepared to **remoue from Roanoak 50 miles into the maine**」；1587 篇「they intended to remoue 50 miles further vp into the maine presently」 | CONFIRMED |
| 71 | `ro403` 哈特拉斯人跟他說，祖先裡有幾個是白人 | LAW-txt「several of their Ancestors were white People」 | CONFIRMED |
| 73 | `ro405` 這是很久以後的轉述，而且只有這一份 | 1709－1587＝一百二十二年；勞森之外我沒有找到第二份一手轉述（H02.md 也沒有） | CONFIRMED（「沒有」型，以今天查到的為限） |
| 74 | `ro406`／`ro407` 內陸的大酋長下令殺了他們／寫下的人是聽別人說的 | EV「the Virginia colony's secretary, William Strachey, suggested that the paramount chief Powhatan had ordered them killed」；NCLR「Strachey presents second-hand information, that is, his manuscript fits our definition of a secondary source」（50） | CONFIRMED |
| 78 | `ro411` 誰最先這樣講，今天查不到 | H02.md 查不到，我這一輪也沒找到（EBs、NCp、WHRO 三個流傳版都沒有講來歷） | CONFIRMED（「沒有」型） |
| 82 | `lost-colony-name` 卡（失落的殖民地／這個名字／一八三〇年代才出現） | SM20「only got its start in the 1830s」；NCLR 的 1837 也落在這十年 | CONFIRMED |
| 87 | `ro417` 同一年，第一塊刻字石出現了 | NCpD「**The first stone was found in the summer of 1937**」「discovered over a period from 1937 to 1940」 | CONFIRMED |
| 88 | `ro418` 到一九四〇年，一共出現四十幾塊 | NCpD「a series of **forty-eight** rocks」；NCLR「the first of **forty-seven** stones」——旁白說「四十幾塊」，兩說都容得下 | CONFIRMED |
| 91 | `ro501` 一九九八年，一所大學在那座島上挖開一塊沙地 | NG「**In 1998**, archaeologists from **East Carolina University** found a ten-carat gold signet ring here」（Cape Creek, Hatteras Island） | CONFIRMED |
| 93 | `ro503` 同一年，另一邊有人在數樹的年輪 | SCI「Science. **1998** Apr 24;280(5363):564-7」、作者署「**Tree-Ring Laboratory**, Department of Geography, University of Arkansas」、摘要「**Tree-ring data** from Virginia」 | CONFIRMED（這一句只說研究用的是年輪，沒有說年輪怎麼讀——`ro504` 的問題就在這一步，見第 9 條） |
| 96 | `drought-stats` 卡 stat 2（800 年／樹輪裡最旱的一次）與出處 | SCI「the most extreme drought in **800 years**」；NPSth 的乾旱那一段 | CONFIRMED |
| 104 | `ro513` 二〇一五年春天，他們挖到一截鐵劍柄 | NG「Part of an **iron rapier handle** was unearthed in the **spring of 2015** at the Cape Creek site on Hatteras Island」 | CONFIRMED |
| 106 | `ro515` 這一條目前只有發掘方受訪的說法 | WHRO 全篇只有 Scott Dawson（該團體 president）的話；我這一輪也沒有找到發表的報告 | CONFIRMED |
| 107 | `ro516`／`ro517`／`brass` 卡（二〇一七年送驗／全部都是黃銅） | SM17（2017-04-07）「A team led by archaeologist Charles Ewen **recently** subjected the ring to a lab test at East Carolina University…"**It's all brass**," he said. "There's no gold at all."」 | CONFIRMED（「recently」的事見〈建議〉3） |
| 123 | `ro613`／`ro614` 沒有附報告／沒看到第三方評估 | 見〈H02.md 拒絕的四件事〉第 4 點與〈兩件會過期的事實〉第 1 點 | CONFIRMED（2026-10-13 重查） |
| 126 | `ro702` 美國國家公園管理局二〇二五年更新了說明 | NPSth 頁尾今天仍標「**Last updated: July 11, 2025**」 | CONFIRMED |
| 129 | `ro705` 寫過一整本書的兩位學者說，他們的答案是不知道 | NCLR「the authors ask that readers not "ask us where we think the Lost Colony went. **Both of us will say, 'I don't know.' And mean it**" (174)」 | CONFIRMED |
| 131 | `outro` 卡（未結／一個字指出了去處，沒有指出下落） | EBp「**The mystery of the Lost Colony has never been solved.**」；去處有線索（HAK-txt「which letters presently we knew to signifie the place, where I should find the planters seated」）、下落沒有定論（NPSth 兩句） | CONFIRMED |
| 37 | `count-stats`.source（Hakluyt、NPS、Britannica 2026-10-10） | 三者今天都在用：Hakluyt 的 119、NPS87／NPSth 的 118／117、EBp 的「approximately 100」 | CONFIRMED |
| 103 | `ro512` 後來一所英國的大學也加進來 | NG「Mark Horton, an archaeologist at **Britain's Bristol University**, who heads the excavation on Hatteras」、同頁「founded the Croatoan Archaeological Society…**in 2009** and have sponsored Horton's annual digs **ever since**」；SM17 另寫「University of Bristol」 | CONFIRMED（查核一的〈建議〉5：來源的順序本來就是「2009 年成立團體→此後贊助霍頓的年度發掘」，「後來」讀得通，**不必改**） |
| 109 | `ro520` 島上多數歐洲器物，都混在十七世紀中期的東西裡 | NG「Like most of the European finds **at Cape Creek**, however, the artifact was mixed in with objects that date to the mid-17th century」——講的是**一個遺址**，不是整座島 | **要改**（見〈還要改的地方〉5） |
| 117 | `ro606` 位置是今天的伯蒂郡 | NPSth 寫「**near** present-day Bertie County」，但 FCF 自己寫「Underneath a patch at the west end of the Albemarle Sound, **in today's rural Bertie County**, was the symbol of a Renaissance-style fort」，CR20 也把 Site Y 寫在「land belonging to Bertie County」 | CONFIRMED（查核一的〈建議〉10 可以結案：FCF 與 CR20 支持「是伯蒂郡」，**不必改**） |

抽樣結果：**44 列裡 43 列 CONFIRMED、1 列要改**（#109）；另外兩列查核一留的建議（#103、#117）
我重查之後認為不必改，理由寫在表內。

## 兩件會過期的事實，今天重查

**1.（`ro614`）二〇二六年六月那則「找到了」還是沒有第三方的評估——重查之後仍然成立。**
今天做了三件事：(a) 重開 FCF 那一頁：`article:published_time` 2026-06-04T18:48Z、頁上沒有附報告；
(b) 重開基金會的新聞索引與自己的「Archaeological Dig Reports」頁：那則宣布是最新的一則、
上一則是 2024-10-17，發掘報告頁上**沒有** Site X／Site Y 的報告（只有 Fort Raleigh 外堡那幾份）；
(c) 兩次網路搜尋，都沒有找到任何針對 2026-06-04 那則宣告的同行或媒體評估，搜到的都是
2015–2020 年的舊報導（National Geographic 2020、Smithsonian 2020、Coastal Review 2020 的那幾句存疑，
全部早於宣告）。
**唯一的新東西**：搜尋帶出一筆第三方的學術書評——Hélène Ducros 在《Southeastern Geographer》
2025 年 65 卷 1 期 119 頁評 Klingelhofer 編、UNC Press 2023 年的《Excavating the Lost Colony
Mystery》（那本書的作者群就是基金會自己的人：Klingelhofer、Luccketti、Evans、Straube）。
它的全文我開不到（EBSCO 的記錄頁回 403，期刊要訂閱），而且它評的是**基金會自己 2023 年的書**，
不是 2026 年那則宣告。所以 `ro613`／`ro614` 照現在的寫法（主語是前一句的「那則宣布」）**不必改**；
要更不可能被誤讀，可以把 `ro614` 寫成「那則宣布到今天也沒看到第三方的評估。」（見〈建議〉4）。
**上架前還是要再搜一次**：這是一句「沒有」的主張。

**2.（`ro702`、`claims.md` c43）國家公園管理局那一頁的更新日期——沒有變。**
NPSth 今天 200，頁尾仍是「Last updated: **July 11, 2025**」，而且 `ro703`、`ro704`、`ro615`
依賴的三句原句我都在今天的頁面上逐字比對過：
「no human remains, graves, buildings, or village sites have been definitively linked to the Lost
Colony」「perhaps, one of the most popular and compelling」「Even the artifacts found there have not
been definitively linked to the Lost Colony」。另外兩頁今天標的是 2026-09-20（NPS87）與
2026-08-14（NPS90），沒有任何一句綁在它們的更新日上。

## 套改之後有沒有弄壞別的東西

- **四個 loop 都還在，而且回收的都是觀眾還沒有的事實。**
  `ro111`→`ro223`（新的是「照約定，沒有十字就是平安」）、`ro107`→`ro409`（新的是「傳到後來變成樹上
  刻著一個字」）、`ro101`→`ro212`（新的是三歲生日）、`ro323`→`ro604`（新的是補丁底下那個記號就在
  那個距離上）。第 2 組最該擔心——「樹皮」改成「樹上」之後，埋與回收的用字還是一字對一字
  （`ro107`「一棵樹上，刻著三個大寫字母」→`ro409`「還記得樹上那三個大寫字母嗎？」），
  `loops[1].what` 也跟著改了，對比仍然成立（三個字母 vs 一整個字、樹 vs 木樁，而「木樁上那個字」
  在第 2 章 `ro223` 又出現過一次，觀眾手上有這張牌）。
- **沒有哪個事實變成講兩次。** 會重複的四個數字（八月十八日、五十英里、沒有十字、三個字母）
  每一次再出現都掛在「還記得…」上。查核一第 8 條之後 `ro615`、`ro616`、`ro703` 連著三句都帶
  「確定」兩個字，但三句的範圍是一層層放大的（那兩個工地的器物→任何東西→遺骸、墳、房子），
  講的不是同一件事；那是用字的回音，不是事實重複。
- **每一章的第一句還是接得上前一章。** 1→2：`ro113` 問「為什麼讓他高興」→`ro201`「他高興，是因為…」；
  2→3：`ro225`「他以為自己很快就會回來」→`ro301`「**可是**那幾年，英格蘭正在打仗」（第 4 條改完
  連接詞還在，接點沒斷）；3→4：`ro324`「木樁上刻的，不是內陸的方向」→`ro401`「南邊那座島上的人，
  後來講過一件事」；4→5：`ro421`「那座島上的土裡，有別的東西」→`ro501`「一九九八年…挖開一塊沙地」；
  5→6：`ro524`「另一支團隊，是從一張地圖開始的」→`ro601`「二〇一二年…攤開懷特那張地圖」；
  6→7：`ro616` 問句→`ro701`「沒有」。
- **片尾只說紀錄裡有的。** `outro` 卡「未結」對得上 EBp「never been solved」；
  「一個字指出了去處，沒有指出下落」兩半都有來源（去處＝懷特自己的記述；下落＝NPS 的兩句）。
  `ro706` 標成「我的看法是」、`ro707` 是留言題、`ro708` 沒有預告下一支。第 7 章短（NOTES 說 39 秒），
  H02.md 裡確實沒有別的、沒講過的事實可以補，補一句重述正是盲評三輪都判掉的事——**我同意選短**。
- **一處畫面被改出來的矛盾（還沒有花錢，現在改不用錢）。** `trumpet-ashore` 的 `prompt` 畫的是
  「one man in a buff coat blowing a long brass trumpet」站在沙地上，而 `ro104` 現在說「靠岸之前」。
  `NOTES.md` 說改 `prompt`「要重畫、要花錢」，但 `brief.md` 與 `NOTES.md` 自己都寫這一集
  「只到腳本：沒有生圖、沒有配音、沒有花錢」——**還沒有畫，現在改 prompt 不花任何錢**。
  見〈還要改的地方〉6。

## 還要改的地方（我沒有動任何檔案）

1. **`no-such-thing` 的 `chapter`（第 7 章章名）**
   現在：`沒有遺骸，也沒有能確定的房子`
   改成：`遺骸和房子，沒有一樣能確定是他們的`（或照 `ro703` 的寫法：`沒有遺骸、沒有房子能確定屬於他們`）
   為什麼：NPSth 的原句是「no human remains, graves, buildings, or village sites have been
   **definitively linked** to the Lost Colony」——「能確定」要管到遺骸，現在只管到房子。
   這正是查核一第 8 條在 `ro615` 修掉的毛病，章名沒有被抽到，所以留在畫面上了。
   旁白 `ro703` 本身是對的，不用動。

2. **`ro504`**
   現在：`那份研究從年輪的寬窄，看出雨水多少。`
   改成：`那份研究從年輪，看出雨水多少。`
   為什麼：SCI 摘要從頭到尾只有「Tree-ring data from Virginia indicate…」，沒有寫年輪怎麼讀，
   「寬窄」指不到來源。`claims.md` c20 自己就記了這一點並寫出同一個改法，照它改即可
   （c20 的但書也可以一併刪掉）。`how-rings-work` 那張圖（木芯上有寬窄的紋）不用改——
   木芯本來就有寬窄的紋，圖沒有宣稱雨水怎麼讀出來。

3. **`count-stats`.stats[0].note**
   現在：`其中三個沒有留下`
   改成（兩個都可以，選一個）：`名單第一個是總督自己` ／ `其中兩個回了英格蘭`
   為什麼：三個人裡的 George How 是**留在島上被殺**的（HAK-txt「The eight and twentieth, George
   Howie, one of our twelue Assistants was…」＝1587-07-28；NPS87「Native people ambushed and killed
   a colonist name George Howe」），說他「沒有留下」讀起來是離開，而且 119－3＝116 沒有任何來源
   寫得出來：EV 兩處都寫懷特走時「leaving behind **117** settlers」「the **117** colonists he left at
   Roanoke Island」（＝119－2），NPSth 也寫「an additional 117 people」。
   後一個選項對得上 EV 的 117（走的兩個是懷特與領航員——HAK-txt 寫 Ferdinando
   「who was appointed to returne for England」，NCp 寫「their pilot, Simon Fernándes」）；
   前一個選項完全不必算數，最安全。**死因照 H02.md 一樣不提。**

4. **`dig-1998` 的 `chapter`（第 5 章章名）**
   現在：`島上的土裡，挖出一只戒指`
   改成：`哈特拉斯島的土裡，挖出一只戒指`（或 `南邊那座島的土裡，挖出一只戒指`）
   為什麼：戒指是在**哈特拉斯島**的 Cape Creek 挖到的（NG「In 1998, archaeologists from East
   Carolina University found a ten-carat gold signet ring **here**」，here 指該篇全文的哈特拉斯島
   遺址），不是羅阿諾克。可是第 3 章章名「他的補給送不到**島上**」裡的「島」指的是羅阿諾克，
   章節列裡一前一後讀下來，「島上的土裡挖出一只戒指」最容易被讀成羅阿諾克——那會變成一個
   來源不支持的事實，而且是觀眾在點章節時第一眼看到的字。旁白 `ro308` 本來就唸過「哈特拉斯島」，
   字典問題不存在。

5. **`ro520`**
   現在：`島上多數歐洲器物，都混在十七世紀中期的東西裡。`
   改成：`那個遺址的歐洲器物，多數混在十七世紀中期的東西裡。`（23 字，與現在全片最長句同長）
   為什麼：NG 的原句是「Like most of the European finds **at Cape Creek**, however, the artifact was
   mixed in with objects that date to the mid-17th century」——講的是一個遺址。查核一把它放在
   〈建議〉，但同一把尺（指不到來源就不算）已經用在 `ro504` 與 `ro615` 上，應該一致。
   前面 `ro501`、`ro510`、`ro513`、`ro514` 講的都是同一個遺址，「那個遺址」接得上。

6. **`trumpet-ashore` 的 `prompt`（畫面，趁還沒生圖改）**
   現在：`Wide shot of a sandy clearing in early morning, one man in a buff coat blowing a long brass
   trumpet towards a row of pines, dune grass around his boots, light from a low sun behind the trees`
   建議改成：人在小船上吹號、對著還暗的岸，岸上遠處一簇火光（HAK-txt：「we let fall our Grapnel
   neere the shore and sounded with a trumpet a Call」，而且他們就是朝著林子裡那堆火划過去的）。
   為什麼：`ro104` 現在說「靠岸之前」，這張圖畫的是人已經站在岸上吹號——查核一第 1 條修掉的錯，
   會在畫面上再出現一次。`NOTES.md` 把這件事列成「要花重畫的錢」，但同一份檔與 `brief.md` 都寫
   這一集「沒有生圖、沒有花錢」：**現在改 prompt 是零成本**，生圖之後才是錢。
   另外兩張（`three-notches`、`remember-three-letters`）我判**不用改**：刻字本來就要削開樹皮才看得到，
   而剝得精光的那一根在 `stripped-post`／`five-feet` 兩張上，分別還在畫面上。

## 建議（指得出來源，但我不要求改）

1. **`ro102`「一艘英格蘭船在羅阿諾克島外放下小船。」**——HAK-txt 的小船是從 Hatorask 放的
   （「we put off from Hatorask, being the number of 19 persons in both boates」），而且是前一天入夜
   前後放的、在黑暗裡划過頭了四分之一哩，天亮才上岸；EV 還寫 1590 年「four ships finally sailed
   for Roanoke」。「一艘英格蘭船在外灘放下小船。」會更準。查核一也提過同一條。
2. **`ro218`「兩天後的早上，他上了船。」**——他 27 日早上離開羅阿諾克，當天「about midnight, came
   aboord the Flieboat」。要準就寫「兩天後的早上，他離開了羅阿諾克。」
3. **`ro514`／`ro516` 的年份都是報導的年份。** WHRO（2025-01-20）寫「recently found」，
   SM17（2017-04-07）寫「recently subjected the ring to a lab test」——兩句的時間都只能推到
   「報導前不久」。`ro514` 已經從「一月」退到「年初」，`ro516`／`brass` 卡的「二〇一七年」同理
   還有一點空間（真要收緊就寫「那幾年」或把句子掛在報導上），但 `ro515` 緊接著就說「目前只有
   發掘方受訪的說法」，`ro502` 也先說「當時說是金的」，我認為可以留。
4. **`ro614`「到今天也沒看到第三方的評估。」**——主語靠前一句的「那則宣布」帶著走，讀得通；
   要完全不可能被誤讀（基金會自己 2023 年那本書有人評過，見〈兩件會過期的事實〉），
   可以寫成「那則宣布到今天也沒看到第三方的評估。」
5. **`ro416` 的地點。** NCLR 的圖說寫「Scene from Paul Green's historical drama The Lost Colony
   **performed in Manteo, NC, 1937-38**」——要把地點寫回去，這是唯一找得到的一條；但「Manteo 在
   羅阿諾克島上」那一步得自己接（NPS 的 Fort Raleigh 通訊地址在 Manteo），所以我**不建議**，
   現在的「開始上演」最乾淨。
6. **第 4 章章名「一七〇九年，有人說祖先是白人」**——是哈特拉斯人自己說祖先裡有白人。
   「一七〇九年，島上的人說祖先有白人」會更清楚，不是事實問題。
7. **`added-later` 表格 1937 那一列的「加了什麼：首演」**——事實對（NCLR 的 premiere），
   但放在「加了什麼」那一欄讀起來怪（加了「首演」？）。寫成「一齣戲」或「戶外劇首演」會順一點，
   這是文字不是事實。
8. **`ro201`「那個字是他自己留下的約定。」**——原文是「agreed vpon **betweene them and me**」，
   雙方約的；`ro220`「他跟他們約好一個記號」已經補回來，所以不要求改。
9. **`brass` 卡的 kicker「那只金戒指」**——卡面上「金」沒有引號，單看像在斷定；`ro502`「當時說是
   金的」救回來了。要更穩可以寫「那只『金』戒指」。
10. **`claims.md` c16 可以補掛 NPSth。** 「那幾年英格蘭正在打仗」最直接的來源其實是 NPSth 的
    「In the summer of 1587, Spain and England were in the midst of war.」，比 EV 的「had been
    fighting」更硬，而 NPSth 本來就在 `sources[]` 裡。

## 其他

- **只靠一個來源的事**（旁白都已標明說話的人）：約好的記號與十字、他看到字很高興（只有懷特 1593 年
  寄出的記述）；1709 年的轉述（只有勞森，`ro405` 明說）；哈特拉斯島的鍛鐵碎屑（只有發掘方受訪，
  `ro515` 明說）；2026 年的「找到了」（只有基金會自己的網頁，`ro612`–`ro614` 明說）；
  1587–1589 的大旱（一篇 1998 年的論文，`ro507`、`ro508` 都加了但書）。這一輪沒有發現新的單一來源。
- **來源彼此不一致、腳本照 H02.md 處理的地方**：補丁底下畫的是什麼（NPS 說堡壘狀符號、NG 說
  四角星、SM20 說兩座隱形墨水的堡壘——旁白只說堡壘形狀的記號）；刻字石 47 或 48 塊（旁白說
  「四十幾塊」）；人數 100–150（並列在卡片上）。三處都守住了。
- **聽眾檢查**：131 句，最長 23 字（`ro311`）；沒有「經查證」「根據官方文件」「本影片」；
  旁白沒有唸出任何拉丁字（Site X／Y、Cape Creek、Bristol、East Carolina、First Colony Foundation
  都改成中文說法）；沒有括號、沒有網址；全檔沒有 `say`／`say_for`。
- **內容守則**：流傳的版本都標成後來加的；沒有宣稱定論；George Howe 被殺、1590 年翻船淹死七人
  （HAK-txt 寫「There were 11 in all and 7 of the chiefest were drowned」）、前一批駐軍的骸骨、
  1586 年酋長被砍頭，全片都沒有提，插圖也沒有畫；Virginia Dare 的名字沒有出現，血統的說法沒有碰；
  勞森那一段帶種族貶義的下一句（「how apt Humane Nature is to degenerate」）沒有引。
- **我沒有跑的事**：git、任何影片階段、`lint`、任何要付錢的提供者。`lint` 的結果照 `NOTES.md`
  是 0 錯誤 0 警告（寫稿方跑的），我沒有重跑；上面建議的六條改動都只動字，不會動鏡頭數或長度。

## 結論

**這一集還不能進圖與配音，但離得很近：上面〈還要改的地方〉六條改完就可以。**

- 查核一的二十二條，**二十條成立**（十五條內容、五條出處），**兩條要再改一次**：
  `ro504` 的「寬窄」（來源沒有）、人數卡的註「其中三個沒有留下」（沒有來源，而且 George How 是
  留在島上被殺的）。
- H02.md 拒絕的四件事**全部仍然被拒絕**：沒有單一人數、樹與木樁分得清楚（這一條我用古拼字與現代
  拼字兩個轉錄本逐字對過）、與克羅托安人同住只說「最受歡迎的說法之一」、2026 年的「找到了」只標成
  基金會自己網頁上的宣稱（今天重查：沒有報告、沒有第三方評估）。
- **查核一沒有抽的七個章名，我抽了，兩個要改**：第 7 章把 NPS 的「能確定」漏掉（跟查核一第 8 條
  同一個毛病），第 5 章的「島上」在章節列裡會被讀成羅阿諾克（戒指在哈特拉斯島）。
- CONFIRMED 抽樣 44 列（43%），43 列成立，1 列要改（`ro520` 的「島上」應為「那個遺址」）；
  119 這個數字我自己重數一次，得到 119（男 91、女 17、男孩 9、當地出生 2）。
- 兩件會過期的事實今天都重查了：2026 年那則宣告仍然沒有第三方評估（找到的唯一新東西是第三方評
  基金會自己 2023 年那本書，與宣告無關）；NPS 那一頁仍標 Last updated: July 11, 2025。
- 套改沒有弄壞結構：四個 loop 都還回收得到新東西，沒有事實講兩次，六個章節接點都接得上，
  片尾只說紀錄裡有的。唯一被改出來的矛盾在 `trumpet-ashore` 那張圖的 `prompt` 上，
  **而這一集還沒有生圖，現在改不用錢**。
- **第三輪：不需要**（這一輪要改的六條裡，五條是一句話或一個標籤的用字、一條是還沒花錢的
  prompt，都指得到具體原句）。改完請寫稿方在 `NOTES.md` 記一行，`claims.md` 的 c20、c9、c39、c43
  跟著更新出處與但書即可；上架前再搜一次 `ro614` 那句「沒有」。
