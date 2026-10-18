# curio-h01-v2 查核第二輪

- 查核 2026-10-13，Claude Opus 5（第二輪查核代理）。**我不是撰稿的那一個，也不是第一輪查核的那一個**，
  也不是第一版兩輪查核的任何一個。`video.json`、`claims.md`、`brief.md`、`NOTES.md` 我一個字都沒有動；
  下面每一條要改的都寫成「行 id ＋現在的字＋應該變成的字」，交給別人去改。
- 為什麼有第二輪：第一輪（[`verify-1.md`](verify-1.md)）要求 19 處改動、涵蓋 16 條主張列，遠超過 3 條的門檻。
  19 處與 4 處文件連帶都已經改進稿子（`NOTES.md`〈第四輪〉），第一輪自己也指定第二輪至少重查 R1–R12
  與三分之一的 CONFIRMED。
- 方法：
  1. 把 `video.json` 重新抽成 140 句旁白、7 個章名、7 張卡片的欄位、標題、說明欄、縮圖、`loops`、
     `sources`（抽取腳本 `extract.mjs`，輸出 `script.txt`、`script-prompts.txt`）。`say`／`say_for` 全稿 0 個，
     `assets[]` 與 `characters[]` 是空的。
  2. **`sources[]` 的 20 筆加上三個對照頁，當天全部用 curl 自己重開一次**（User-Agent
     `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.6 秒，
     去掉標籤與註解後讀全文）。第一輪與前一次中斷的嘗試留在暫存區的下載檔我一律不用，全部重抓重讀。
  3. 重點回到一手文件：**Austin 勘驗報告全文（1872-12-23）逐段讀過 65 段**、**Patron 化驗報告全文（1873-01-30）**、
     **Gibraltar Chronicle 1872-12-13／1873-01-31／03-04／03-15 全文**、**maryceleste.net/facts 的 16 條更正**、
     **THP 引的 Solly-Flood 1873-01-22 信原文**、**Wikisource 的道爾 1884 全文（含逐字搜尋飯菜）**、
     **Commons 的 1873 紐約時報剪報全文**。
  4. 聽眾檢查不跑影片階段：我照 `tools/video/core/narrative.mjs` 與 `core/timeline.mjs` 的算法
     自己寫了一支 `listener.mjs`（單位數、數字重複、「還記得」間隔、章首標籤句、`loops`），只讀程式不執行工具。
- 判定沿用四個：**CONFIRMED** 看到了／**CHANGED** 要改／**NOT FOUND** 沒看到，拿掉或換掉／**OUT OF SCOPE** 不動。
- 程序：**沒有跑 git、沒有跑任何影片階段（含 `lint` 與 `narrative`）、沒有花任何提供者的錢、沒有用網路搜尋（0 次）**；
  curl 的 User-Agent 用的是 `support@mokaair.com`，沒有放任何個人信箱。輔助檔在
  `<scratch>\verify2-h01\r2\`（`fetch.sh`、`totext.mjs`、`extract.mjs`、`listener.mjs`、`statuses.txt`、`raw/`、`txt/`）。

## 當天（2026-10-13）我自己開過的網址

`sources[]` 的 20 筆全部在內，**23 個網址全部 200**。

| 縮寫 | 網址 | HTTP |
|---|---|---|
| MCN/facts | https://www.maryceleste.net/facts.htm | 200 |
| MCN/survey | https://www.maryceleste.net/survey.htm （Austin 勘驗報告全文，65 段） | 200 |
| MCN/news | https://www.maryceleste.net/news.htm （Chronicle 1872-12-13、1873-01-31、03-04、03-15） | 200 |
| MCN/doctor | https://www.maryceleste.net/doctor.htm （Patron 化驗報告全文） | 200 |
| MCN/briggs | https://www.maryceleste.net/briggs.htm | 200 |
| MCN/barrel | https://www.maryceleste.net/barrel.htm | 200（**有內文**，見摘要的更正） |
| MCN/spencer | https://www.maryceleste.net/spencer.htm | 200 |
| MCN/about | https://www.maryceleste.net/about.htm | 200 |
| MCN/genoa | https://www.maryceleste.net/genoa.htm （再確認卸貨日期） | 200，只有熱那亞港通史，**沒有卸貨日期** |
| AH | https://www.americanheritage.com/mystery-mary-celeste | 200 |
| SM | https://www.smithsonianmag.com/history/abandoned-ship-the-mary-celeste-174488104/ | 200 |
| SM-ARC | https://web.archive.org/web/20260920054456/…smithsonianmag… （`sources[0]`） | 200 |
| EB | https://www.britannica.com/topic/Mary-Celeste | 200 |
| EB-ARC | https://web.archive.org/web/20260819222317/…britannica… （`sources[1]`） | 200 |
| THP | https://thehistorypress.co.uk/article/the-ongoing-mystery-of-the-mary-celeste/ | 200 |
| HH | https://www.historyhit.com/ghost-ship-what-happened-to-the-mary-celeste/ | 200 |
| FV | https://fishermensvoice.com/archives/201711TheMysteriousCaseOfTheMaryCeleste.html | 200 |
| NEHS | https://newenglandhistoricalsociety.com/mysterious-disappearance-mary-celeste/ | 200 |
| SL | https://www.slate.com/articles/life/culturebox/2011/12/the_mary_celeste_the_unluckiest_ship_to_ever_sail_the_seven_seas_.html | 200 |
| SK | https://skeptoid.com/episodes/289 | 200 |
| WS | https://en.wikisource.org/wiki/J._Habakuk_Jephson%27s_Statement | 200 |
| ACD | https://www.arthur-conan-doyle.com/wiki/Mary_Celeste | 200 |
| C-NYT | https://commons.wikimedia.org/wiki/File:Mary_Celeste_NYTimes_1873February26.png | 200 |

快照對照：EB-ARC 與現在的 EB 逐字比對，只差一行 Guardian 書評連結，我查的每一個字串
（「3 feet (1 meter)」「November 7, 1872」「Richard W. Haines」「10 people」「May 18, 1861」「one-sixth」）一字不差；
SM-ARC 與 SM 同。**兩個快照撐得起 `sources[0]`／`[1]` 的主張。**

## 一、二十三處已改動的重新判定

19 處要求改動（R1–R19）＋ 4 處文件連帶（K1–K4）。每一條我都回到來源自己讀過，不看第一輪的理由。

| # | 行 id／欄位 | 現在的字 | 來源句 | 判定 |
|---|---|---|---|---|
| R1 | `youtube.description` | 「…一八八四年一篇小說怎麼把『小艇都在』寫進大家的記憶、那頓熱飯菜又是從哪裡長出來的…」 | WS 全文：Gazette 段落有「The boats were intact and slung upon the davits」；**全篇沒有任何艙桌上的飯菜**——breakfast 只出現在敘事者自己 10-18 的日記（「At breakfast this morning…」）。AH：「Other romancers added… a partly consumed breakfast on the cabin table, including cups of tea that were still lukewarm」**沒有年份** | **CONFIRMED**（改對了。這是第一版兩輪都改過、重講時又回來的那一條，現在說明欄與 `mc5g` 不再互相矛盾） |
| R2 | `added-later/mc5h` | 「是別人轉述的時候，才加上去的。」 | 同 R1：沒有任何開得了的來源給熱飯菜的年份 | **CONFIRMED**（「後來」拿掉了；全稿唯一談先後的是 `mc5k`「都沒有標那是哪一年加的」，與來源一致） |
| R3 | `youtube.description` | 「直布羅陀的檢察總長怎麼把它當成一樁謀殺案」 | MCN/about 直接寫：「It also suggests that the Court in Gibraltar believed foul play had taken place. **Mr Frederick Solly Flood, clearly believed that, but the court did not.**」；EB「British authorities investigated, but found no evidence of foul play」；SM「After more than three months, the court found no evidence of foul play」；AH「The queen's proctor… promptly convinced himself」 | **CONFIRMED**（改對了，而且 MCN/about 幾乎是逐句駁掉原來的寫法） |
| R4 | `sea-tore-wood/mc4d` | 「一個多月後，一艘美國軍艦的艦長說，那是海水撕裂的木頭。」 | Patron 報告署「Gibraltar, 30th January 1873」；Shufeldt 的報告見 Chronicle **1873-03-04**「it amounts merely to splinters in the bending of the planks, which were afterwards forced off by the action of the sea」。01-30 → 03-04 ＝ 33 天 | **CONFIRMED**（「三個月後」是算錯的，「一個多月後」對。另外 Chronicle 同一篇最後一句還寫「the opinion of Captain Shufeldt… is in direct contradiction to that expressed by the surveyors here」——旁白把它講成「艦長說」而不是定論，正確） |
| R5 | `chronometer-off/mc6q` | 「天文鐘有誤差，船長的位置比他以為的偏西一百二十哩。」 | SM：「Their conclusion: **Briggs was actually 120 miles west of where he thought he was**, probably because of an inaccurate chronometer. By the captain's calculations, he should have sighted land three days earlier than he did.」 | **CONFIRMED**（方向正確：實際位置偏西，所以陸地比他算的晚出現） |
| R6 | `kill-captain/mc2i` | 「喝醉之後殺了船長，再上別的船逃走。」 | THP 引 1873-01-22 信原文：「…murdered the Master whose name was Briggs and wife and Child and the Chief Mate… and that they did sometime between the 25th November and the 5th December **escape on board some vessel** bound for some north or South American port or the West Indies」 | **CONFIRMED**（信的原文就是「搭上別的船」。AH 的摘要寫「escaped in the boat」，兩個來源不同，旁白跟一手文件是對的；旁白只說殺了船長、沒有講妻女，比來源保守，符合內容守則） |
| R7 | `cargo-stats/mc2p` | 「那不是拿來喝的，而且只有一桶被打開過。」 | NEHS「denatured alcohol, which is **undrinkable** but commonly used for fuel and other industrial purposes」；MCN/about「the alcohol carried was of a strength and type that would **not be palatable to drink**」；Chronicle 1873-01-31 第 1 點「all of which were well stowed and in good order and condition, **except one which had been started**」 | **CONFIRMED**（「喝下去會死人」確實沒有來源；現在的講法連 SK／MCN/about 那一派也不反對） |
| R8 | `galley-stove/mc3f` | 「奇怪的是，大副上船那天，廚房的爐灶被撞離了原位。」 | MCN/facts 第 4 條「The galley stove was knocked out of place… The water in the galley was a foot or two deep.」出處欄寫 **Testimony before Vice-Admiralty Court, Gibraltar, 1872**；Austin 第 21 段反過來寫「The stove and cooking utensils were **in good order** and exhibited no appearance of having suffered from exposure to water」 | **CONFIRMED**（事實與歸屬都對；撰稿換了寫法，見第二節） |
| R9 | `binnacle-knocked/mc3g` | 「那天的羅經櫃也歪了，羅盤的玻璃罩破了。」 | NEHS、FV 講的都是 12-04 發現時（FV「binnacle broken with the glass shattered」）；Austin 第 52 段把兩片裂掉的玻璃歸給燈的熱度，第 54 段「**The binnacle itself did not appear to have sustained any damage**」 | **CONFIRMED** |
| R10 | `still-aboard-stats.data.source` | 「Dei Gratia 號船員在直布羅陀的證詞，1872–73」 | AH（登船者所見）「**The ship's stores contained provisions for six months** and ample drinking water」；SM「There was a six-month supply of food and water」；**Austin 全文沒有任何「六個月」**，第 59 段只寫「barrels of stores and other provisions in good order」 | **CONFIRMED**（出處掛對了。Dei Gratia 的人從 1872-12-18 作證到 1873-03-04 德沃第三次受訊，「1872–73」也對） |
| R11 | `nine-empty.data.sub` | 「其他的沒有漏」 | SM「nine of the 1,701 barrels in the hold were empty」；MCN/barrel「the cargo was found to contain nine empty barrels」；MCN/about「**This level of shrinkage was considered normal**, and differences in the wood used to make the barrels could account for leaks」 | **NOT FOUND → 還要改（F1）**。沒有一個來源說其餘 1,692 桶「沒有漏」；MCN/about 反而說這種漏損量是**正常的**。第一輪給了兩個寫法，撰稿選了沒有來源的那一個 |
| R12 | `outro/mc7x` | 「十個人離開的理由，紀錄最後留下的是那九個空桶。」 | `script-writing.md` §結尾：蓋「未結」的那一集「第一句就講紀錄確定了什麼、或紀錄拒絕了什麼」，並把「目前只有…說得通」記成反例 | **CONFIRMED**（撰稿沒照第一輪的字，但照得更對，見第二節） |
| R13 | `opening-swell/mc1a` | 「一八七二年十二月四日下午，大西洋上。」 | MCN/facts 第 6 條「found on 4 December between 1:00 and 2:00 P.M.」；第 15 條發現位置 38°20'N **17°15'W** | **CONFIRMED**（海況的斷言拿掉了；撰稿兩個建議都沒照抄，理由成立，見第二節） |
| R14 | `miscalculation/mc6p` | 「二零零七年，有一份研究從同一個念頭往下查。」 | SM：MacGregor「began by asking what didn't happen」，起點是 Solly-Flood 的日誌抄本；Chronicle 03-04 Shufeldt「she may have strained in a gale and for the time **leaked so much as to seriously alarm the master**」 | **CONFIRMED**（沒有來源把 MacGregor 接到 Shufeldt 那句話上，現在的句子也沒有這樣說；「同一個念頭」＝船看起來在進水、船長被嚇到，兩邊確實是同一個念頭） |
| R15 | `sea-monster/mc5m` | 「還有人說是海怪，說是巨大的章魚。」 | AH 把 giant octopus 列在道爾之後的「Authors variously conjectured」；MCN/about 寫「**A popular theory at the time** was that a giant squid, octopus, kraken…」 | **CONFIRMED**（兩個來源的年代相反，拿掉先後是唯一站得住的寫法；`mc5q`「法庭的檔案裡…一個字都沒有」照樣成立） |
| R16 | `lookout-glass/mc1b` | 「一艘英國帆船的船長舉起望遠鏡。」 | AH「her master, David Reed Morehouse, sighted a sailing ship on his port bow, to windward. **Through a glass he perceived**…」；THP 引莫爾豪斯的庭上證詞「**through his telescope** from a distance he 'saw the marks or spalls on the bows'」 | **CONFIRMED**（兩個互相獨立的來源都把望遠鏡放在船長手上；「瞭望手」沒有來源。插圖要跟著改，見第六節） |
| R17 | `family-gangplank/mc2m` | 「十一月七日，他帶著太太莎拉和兩歲的女兒蘇菲亞離開紐約。」 | EB「On November 7, 1872, the Mary Celeste **set sail** from New York City」；HH 同；SK「They left port from Staten Island, New York in November of 1872」；MCN/briggs「On October 31, 1870, Their daughter Sophia M. was born」（1872-11-07 剛滿兩歲） | **CONFIRMED**（啟航日不是上船日；單位數 26→25） |
| R18 | `covered-150/mc5u` | 「一個真實的船名，被一篇小說蓋了一百多年。」 | ACD「In january 1884, Arthur Conan Doyle published anonymously…」；1884 到 2026 ＝ 142 年 | **CONFIRMED** |
| R19 | `captain-notices/mc7g` | 「最站得住的版本是：船長發現艙裡有水，或者聞到味道。」 | SK「there seems little reason to speculate beyond **what's best supported by the evidence**: powerful and dangerous fumes from the alcohol-soaked red oak barrels」；EB「**A more likely scenario** is that Captain Briggs erroneously believed his ship was taking on too much water」 | **CONFIRMED**（標記放在假說開始的地方，而且「最站得住」有來源。但 `NOTES.md` 說它連 `mc6u` 也蓋住了——**這一句不成立**，`mc6u` 在第 112 句、`mc7g` 在第 121 句，標記在後面蓋不到前面；`mc6u` 本身另有來源，見第八節） |
| K1 | `claims.md` c45 | 「天文鐘誤差讓 Briggs 的**實際位置比他以為的偏西 120 哩**（smithsonianmag：actually 120 miles west of where he thought he was，所以他以為早三天就該看到陸地）」 | 同 R5 | **CONFIRMED**（連來源原文一起寫進去了） |
| K2 | `claims.md`〈算出來的數字〉 | 「`sea-tore-wood` 的『一個多月後』（1873-01-30 到 1873-03-04，相隔一個月又四天）」、「`covered-150`…（1884 到今天；主詞是那篇小說）」 | 同 R4、R18 | **CONFIRMED**（兩個算術都改正了） |
| K3 | `claims.md` 最後一節 | 不再引「還記得那九個空桶嗎？」那一句 | `grep` 全檔：那句話只剩在 `NOTES.md` 第 56 行的改動紀錄表裡，而且當場註明「第四輪的查核又把它改掉了」 | **CONFIRMED**（文件不再落後於稿子；紀錄表保留舊字是對的） |
| K4 | `brief.md` 第 48 行 | 「熱飯菜與溫著的茶是別人轉述時加的」 | 同 R2 | **CONFIRMED**（「後來」拿掉了） |

**二十三處的結果：CONFIRMED 22、NOT FOUND 1（R11 改成的字本身沒有來源）。**

## 二、五處偏離第一輪建議的判定

我只看來源與規則，不看兩邊的理由。

| 行 id | 第一輪建議 | 撰稿寫的 | 判定 |
|---|---|---|---|
| `mc1a` | 「大西洋的正中間。」／「亞速群島東邊的大西洋上。」 | 「一八七二年十二月四日下午，大西洋上。」 | **撰稿對。** MCN/facts 第 15 條：發現位置 38°20'N **17°15'W**；AH「at a point about midway between the Azores and Portugal」。那一帶的大西洋從葡萄牙（約 9.5°W）到美洲東岸（約 75°W），正中間在 40°W 附近——17°W 在**東邊五分之一**，叫「正中間」不準。第二個寫法（亞速群島東邊）有來源，但會把 `mc5o`「可是她是在葡萄牙外海被發現的」的位置先講掉，而那句話是第 5 章拆百慕達三角的關鍵一擊。現在的寫法只留日期與海域，兩個都查得到 |
| `mc3f` | 「上船那天的證詞說，廚房的爐灶被撞離了原位。」 | 「奇怪的是，大副上船那天，廚房的爐灶被撞離了原位。」 | **撰稿對，而且兩個理由都查得到。**（一）我讀了 `core/narrative.mjs`：`escalation` 的樣式表裡就有「**奇怪的是**」，而第 3 章這一段從 `mc2r`「但這還不是最奇怪的地方」到 `mc3u`「那段空白裡…」之間隔了 21 句，拿掉它就只剩一個超過 `HOOK_GAP_SECONDS`（90 秒）的空檔，`hookCadenceProblems` 會報警——撰稿說的「02:21 到 04:03」正是這一段（我沒有跑 `lint`，但空檔是數得出來的）。（二）`script-writing.md` 第 28 條要旁白不要用「文件寫／證詞說」開頭，全稿已經有五句在旁白裡點名紀錄或報告（`mc3d`、`mc3v`、`mc5i`、`mc5k`、`mc6n`），再加一句「證詞說」正好往反方向走。「大副上船那天」把日子與觀察者都講清楚了，歸屬一樣穩 |
| `mc3h` | （第一輪沒有要求） | 「勘驗官還看到，船頭兩側有像刀砍出來的痕跡。」 | **撰稿對，而且這一句是必要的。**刀痕確實是 Austin 自己的發現：Austin 第 2、3 段「On approaching the Vessel I found on the bow… apparently done by a sharp cutting instrument」。更關鍵的是 THP 的這一段：「**None of the Dei Gratia crew** who first or even subsequently went on board the Mary Celeste found anything damaged around her bows that might arouse suspicions of 'injury' inflicted there」——莫爾豪斯只在遠處用望遠鏡看到 marks or spalls。所以前兩句改成「那天」之後，如果這一句不把視角交回勘驗官，刀痕就會被時間標記一路蓋成「登船那天的證詞」，而那剛好是來源明文否認的事。這個自己加的標記擋掉了一個新的錯誤歸屬 |
| `mc7g` | 「最站得住的版本是：船長發現艙裡有水，或者聞到味道。」 | 一字不差照做 | **CONFIRMED，不算偏離**（我逐字比對過，和第一輪給的字完全相同；唯一偏離的是 `NOTES.md` 對它的說明——它蓋不到前面的 `mc6u`，見 R19 與第八節） |
| `mc7x` | 「十個人離開的理由，目前最說得通的是那九個空桶。」 | 「十個人離開的理由，紀錄最後留下的是那九個空桶。」 | **撰稿對，比第一輪的建議更對。**`script-writing.md` §結尾那一條就是為這一集寫的：「檔案蓋『未結』的那一集**沒有這個數字**…那第一句就講紀錄確定了什麼、或紀錄拒絕了什麼」，並且把「瑪麗賽勒斯特號寫成『目前只有…說得通』」列為反例。第一輪的「目前最說得通的是」還是在替一個未結的案子排名次，而且會和 `mc7g` 的「最站得住的版本」在同一支片裡講兩次最高級。現在的寫法只講紀錄留下了什麼——九個空桶確實是這個問題上紀錄最後交出來的東西（MCN/about、MCN/barrel、SM 都寫卸貨時才發現），而且它仍然點名那九桶、和 `mc7v`「還是沒有定論」、`mc6v`「這兩條路，都還有破洞」一致 |

**五處的結果：四處偏離全部成立（其中 `mc3h` 擋掉了一個新錯誤），`mc7g` 其實沒有偏離。**

## 三、第 3 章的歸屬：以聽眾的耳朵讀一次

勘驗報告寫爐灶與炊具「in good order」（第 21 段）、羅經櫃本身「did not appear to have sustained any damage」（第 54 段），
而這一章把兩件事都放在勘驗官那一段裡，只加了一個兩個字的時間標記。我把第 31–39 句連著讀：

| 句 | 行 id | 說的是誰看到的 | 標記 |
|---|---|---|---|
| 031 | `mc3a` 十二月二十三日，法庭派的勘驗官上了船。 | 勘驗官 | 明寫日期 |
| 032–035 | `mc3b`–`mc3e` 潛水夫、船殼、天氣、油瓶 | 勘驗官（Austin 第 63、4、30 段） | 承接 |
| 036 | `mc3f` 奇怪的是，**大副上船那天**，廚房的爐灶被撞離了原位。 | 登船那天（MCN/facts 第 4 條） | **換日子＋換觀察者** |
| 037 | `mc3g` **那天的**羅經櫃也歪了，羅盤的玻璃罩破了。 | 同上（NEHS、FV） | 「那天」指前一句 |
| 038 | `mc3h` **勘驗官還看到**，船頭兩側有像刀砍出來的痕跡。 | 勘驗官（Austin 第 2、3 段） | **交回勘驗官** |

**判定：歸屬站得住，標記沒有超過它能承擔的工作。**三個理由：

1. 「大副上船那天」不是一個模糊的時間副詞，它同時換了**日子**和**觀察者**，而「大副爬上甲板」這一幕
   第 1 章整整講了十二句（`mc1e`「大副德沃划小艇過去，爬上甲板」），聽眾手上有這個座標。
2. 「那天」只跨一句，指的是上一句剛說完的那一天，中間沒有別的日子插進來；這是一跳的指代，不是三跳。
3. 下一句立刻把名字叫回來（「勘驗官還看到」），所以這一段是 A–A–B 而不是 A–B–A–B：每一次換人都有標記，
   沒有一句是靠聽眾自己猜的。

另外兩件事讓它更穩：**插圖剛好站在同一邊**——`galley-stove` 的 prompt 是「a sailor's boot beside the gap」、
`binnacle-knocked` 是「a sailor's hand steadying it」，而 `surveyor-list`／`hull-sound`／`no-rough-weather`／`bow-cuts`
畫的都是 surveyor（`bow-cuts` 還明寫 bowler hat）。畫面沒有把水手的發現畫成勘驗官的。
再者 THP 自己就提醒這件事該怎麼講：「It is important to note that it was carried out **two and a half weeks after**
the Dei Gratia had found her derelict, after she had been made shipshape for her run to Gibraltar…
The Mary Celeste's condition at the time of the survey was therefore in many ways **very different from how she was found**」。

唯一可以挑的是 `mc3h` 的「還」要跨過兩句回去接 `mc3e`，讀起來多轉一個彎；但主詞是點名的「勘驗官」，不會誤會。
**不要求改。**（`mc3f` 的「奇怪的是」讓第 3 章出現兩句講述者在場的句子——另一句是標成意見的 `mc3p`「我的看法是」。
`script-writing.md` 第 114 行寫「每章最多一句自己的反應」。若站主要收到一句，動的應該是 `mc3p` 而不是 `mc3f`，
因為 `mc3f` 是這一段唯一撐著鉤子節奏的句子。這是風格裁量，不是事實問題。）

## 四、七個章名的判定

第一輪沒有查章名（M14 只寫「都只用章內已查過的事實」）。章名會進 YouTube 的章節清單，觀眾**讀得到**，
而且是脫離上下文單獨讀的，所以我照兩個標準看：對不對得上章內容與來源，以及單獨讀的時候立不立得住。

| # | 章名 | 章內容 | 來源 | 判定 |
|---|---|---|---|---|
| 1 | 爬上一艘沒有人的船 | 第 1 章就是登船（`mc1e`–`mc1l`） | AH「Rowing up to the silent ship… Deveau and Wright clambered onto her deck. The investigators soon confirmed that **there was not a soul on board**」 | **CONFIRMED** |
| 2 | 他把這艘空船開進直布羅陀 | 德沃決定自己開船、留兩個水手、12-13 靠港 | MCN/facts 第 8 條把「towed」列為誤傳：「The Mary Celeste was **sailed all the way** from the place where she was picked up… to Gibraltar by **Mate Deveau** and Seamen Lund and Anderson」；AH 同 | **CONFIRMED（事實）／建議改字（S1）**：章名裡的「他」在章節清單上沒有前文可以指。改成「**大副把這艘空船開進直布羅陀**」仍是同一個事件，而且 MCN/facts 用的就是「Mate Deveau」 |
| 3 | 少了找路的工具，留下了半年的糧食 | 第 3 章的清單 | AH 一段全中：「The captain's chronometer and sextant, the navigation book, and the ship's register were missing… The ship's stores contained provisions for six months and ample drinking water」；SM「a six-month supply of food and water」 | **CONFIRMED**（兩半都有來源，而且章名沒有宣稱是誰看到的，不受第三節的歸屬問題影響） |
| 4 | 化驗說不是血 | 第 4 章從化驗結論開始 | Patron 報告「there is **no blood** either in the stains observed on the deck of the Mary Celeste or on those found on the blade of the sword」 | **CONFIRMED**（`script-writing.md` 第 94 行拿這一句當好章名的範例） |
| 5 | 一八八四年，有人把她寫成小說 | 第 5 章從雜誌登小說開始 | ACD「**In january 1884**, Arthur Conan Doyle published anonymously in The Cornhill Magazine a short story」 | **CONFIRMED**（旁白全稿不唸道爾的名字，章名用「有人」與它一致） |
| 6 | 說法一個一個掉下來 | `mc6a`–`mc6w`：船主自燃（被擋）、海盜（被擋）、詐保（被擋）、海震與水龍捲（被擋）、Shufeldt「理由不充分」＋2007 年的誤判進水（**沒有被擋，被帶進第 7 章**） | — | **CHANGED → 還要改（F4）**。三個問題：(a) 寫的是這一章的**功能**（把說法一個一個淘汰），正是 `script-writing.md` 第 94 行禁止的那一類，和第一版的「七種解釋，三個問題淘汰」同一個毛病；(b) 這一章最後三分之一是**唯一沒有掉下來**的那一條（`brief.md` 第 138 行自己寫「剩酒精蒸氣與誤判進水」），章節清單上的讀者跳進來會對不上；(c) 和旁白 `mc4e`「謀殺的說法，一條一條掉了下來」幾乎同一句話。這一集其他六個章名都是「章內第一個事件」的寫法（第 4、5、7 章都幾乎就是該章第一句），照同一個模子應該是「**船主說是酒精自己起了火**」（AH：「did spontaneous combustion occur, blowing off the fore hatch cover, as the Celeste's then principal owner, **Captain J. H. Winchester**, afterward maintained?」）。想讓清單上掛這一章最強的新事實，「**天文鐘差了一百二十哩**」也有來源（SM） |
| 7 | 熱那亞的碼頭上，九桶是空的 | 第 7 章從卸貨開始 | MCN/about「when the cargo was finally unloaded in **Genoa** nine barrels were found to be empty」；MCN/barrel 同；SM「nine of the 1,701 barrels in the hold were empty」 | **CONFIRMED**（SK 寫直布羅陀是少數說法，多數寫熱那亞，照多數） |

**七個章名的結果：CONFIRMED 5、要改 1（第 6 章）、建議改字 1（第 2 章）。**

## 五、第一輪 50 條 CONFIRMED 的抽樣（22 條，44%）

**怎麼挑的**：不抽籤。這一版的風險不是均勻散開的，所以我照四個會出錯的地方挑，門檻 17 條，實際 22 條：

- **A 組（8 條）最後那個解釋踩在上面的**——這幾條若有一條錯，第 7 章整段倒：c4、c23、c24、c40、c42、c44、c48、c50。
- **B 組（7 條）緊貼著被改過的句子**——改一句可能把旁邊那句的歸屬或時間推歪：c1、c19、c21、c25、c31、c32、c37。
- **C 組（4 條）單一來源**——沒有第二個來源可以互相擋：c33、c35、c36、c52。
- **D 組（3 條）觀眾讀得到的欄位**——卡片與參考資料：M9、M11、M15。

| # | 主張 | 位置 | 來源句 | 判定 |
|---|---|---|---|---|
| c4 | 艙底約 3.5 英尺（一公尺多）的水，船仍可航行 | `open-hatch/mc1g` | SM「Three and a half feet of water was sloshing in the ship's bottom」；EB「more than 3 feet (1 meter) of water in the hold—an amount that would not have caused panic—the vessel was **seaworthy**」 | CONFIRMED |
| c23 | 前艙口開著，主艙口蓋好 | `open-hatch/mc1g`、`main-hatch-closed/mc6c` | AH「Both her **fore and lazaretto hatches were uncovered**」；SK「the forehatch… and the lazarette hatch had both been **removed and were stowed**」；FV「The main hatch was tightly covered, but the fore and lazarette hatches were open, **with their covers nearby, on the deck**」；SM「the boarding party found the main hatch secured」 | CONFIRMED（事實）；但這兩個事實在第 6 章被接成一個不成立的反駁，見 F2 |
| c24 | 測深桿留在甲板上；兩具幫浦之一被拆開 | `sounding-rod/mc1i`、`mc6r`、`pump-apart/mc6s` | Austin 第 49–50 段「I found one of the pumps in good order the valve of the other had been removed for the purpose of passing a sounding-apparatus into the well. The sounding apparatus… was lying near」；SM「one of its two pumps had been disassembled」；EB「the sounding rod… was discovered on deck」 | CONFIRMED（一手文件逐字對上） |
| c40 | 約三吋周長的主升降索斷裂、拖在船外 | `trailing-rope/mc1k`、`mc7i`–`mc7k` | MCN/about「the main halyard, a stout rope three inches in circumference, was found **broken and hanging over the side**」（並引 Anderson 的交互詰問「there were ropes hanging over the side」）；SK「the main peak halyard, the stoutest line on the ship… found cleated off and **trailing in the water behind the ship**」 | CONFIRMED（「船尾」有 SK）；**但 Austin 反對**，見第八節 |
| c42 | 海底地震（David Williams）與水龍捲：船與貨無損，純假設 | `quake-waterspout/mc6k`、`no-damage/mc6l`／`mc6m` | SK「**Since then**, even more suggestions have come from the fringe… like waterspouts and rogue waves. One in particular, David Williams, proposes that a 'seaquake'… but as **no damage was noted** on the Mary Celeste, his seems an arbitrary explanation」；Chronicle 1873-01-31 第 1–3 點 | CONFIRMED（「後來的研究者」成立） |
| c44 | 反證：主艙口蓋好、沒人聞到氣味；沒有爆炸或火燒痕跡 | `mc6c`、`no-smell/mc6d`、`no-burn-marks/mc6e` | SM「the boarding party found the main hatch secured and **did not report smelling any fumes**」；SK「no one in Morehouse's party reported smelling anything」；Austin 第 61 段「did not discover the slightest trace of there having been any explosion or any fire」 | CONFIRMED（三個事實都對）；`mc6c` 的**接法**要改，見 F2 |
| c48 | 九個空桶是紅橡木，其餘白橡木；紅橡木孔隙大易滲漏 | `red-oak/mc7e`、`porous-oak/mc7f` | SM「the empty nine had been recorded as being made of **red oak, not white oak like the others**. Red oak is known to be a more porous wood and therefore more likely to leak」；MCN/barrel 轉引 SK 的 cooper 說明 | CONFIRMED |
| c50 | 2007 年用氣象資料回推，結論「基本上是自己走的」 | `drift-study/mc7n`／`mc7o`、`sailed-herself/mc7p` | SM「data that MacGregor found in the **International Comprehensive Ocean-Atmosphere Data Set (ICOADS)**… '**We found out it basically just sailed itself**,' Richardson says」 | CONFIRMED |
| c1 | 被發現時船仍在航行、部分帆張著 | `mc1a`、`crooked-sails/mc1c`、`still-sailing/mc1h`、`sails-away/mc7l` | MCN/facts 第 5 條（把「all sails were set」列為誤傳；只有 lower topsail、jib、fore-topmast staysail 張著）；AH「beating northwest under very short canvas」；FV「her sails were set in an odd manner」 | CONFIRMED（`mc1c`「帆是歪的，走得晃晃悠悠」與 FV 的 erratically／odd manner 對得上） |
| c19 | 12-04 下午被發現（日誌記 5 日）；距最後一筆九天 | `mc1a`、`nine-days-blank/mc3t`、`four-or-five/mc3v` | MCN/facts 第 6 條「found on **4 December between 1:00 and 2:00 P.M.**… the entry on the Dei Gratia's log was therefore dated 5, December, **sea-time**」並把 5 日列為誤傳；AH「Early in the afternoon of December 4」；EB、SM、Chronicle 用 5 日 | CONFIRMED（兩個日期旁白都講；11-25 → 12-04 ＝ 9 天，算術對） |
| c21 | 德沃與兩人登船；之後帶兩名水手把船開到直布羅陀 | `row-across/mc1e`、`decide-sail/mc2a`、`three-men/mc2c` | AH「sent first mate Oliver Deveau, with second mate John Wright and a seaman」「**Mate Deveau proposed** that he sail the derelict to Gibraltar, and Morehouse… detailed two seamen to go with the mate」；MCN/facts 第 8 條（Lund、Anderson） | CONFIRMED（登船的三個人與開船的三個人是不同組合，稿子沒有混在一起；「他決定」略強於 AH 的 proposed，但下一句就把莫爾豪斯帶出來，保留） |
| c25 | 1,701 桶無人動過，只有一桶被打開 | `cargo-stats` 卡、`casks-counted/mc7d` | Chronicle 1873-01-31：「the Queen's Proctor… ordered a special survey of the vessel in the first instance **on the 23d December** last by Mr. Austin… The result of this, and a subsequent survey was… 1. As regards the cargo… **except one which had been started**」；AH「**A survey of the 1,701 barrels** of alcohol… showed that none had been tampered with」 | CONFIRMED（卡片出處成立；精確度註記見第八節） |
| c31 | 12-23 勘驗：船殼無損、沒遇過特別惡劣天氣、縫紉機油瓶直立 | `mc3a`–`mc3e` | Austin 第 4 段「The whole of the Hull--Masts Yards and other Spars were in their proper places and in **good condition** and exhibited no appearances whatever… any seriously heavy weather」；第 30 段「a small **phial of oil for a sewing machine in its proper perpendicular position** a reel of cotton… and a thimble」（在大副艙的小架上）；第 63 段潛水夫 Ricardo Portunato | CONFIRMED（`mc3e`「大副艙的小架上」與一手文件完全一致；THP 另證這幾樣東西「only emerged in Austin's survey」，所以放在這一章是對的） |
| c32 | 船艏兩側「刀痕」；劍「像被血抹過又擦掉」 | `bow-cuts/mc3h`、`sword-smear/mc3x`、`send-to-test/mc3y` | Austin 第 2 段「apparently done by a **sharp cutting instrument**」；第 44 段「on drawing out the blade it appeared to me as if it had been **smeared with blood and afterwards wiped**」 | CONFIRMED（兩句都保留了「像」） |
| c37 | 1873-03 判 £1,700；估值 $42,643，約五分之一 | `award-stats` 卡、`mc4i`／`mc4j` | Chronicle 1873-03-15：「**In the Vice Admiralty Court yesterday** the Hon. the Chief Justice gave judgment… awarded the sum of £1,700… valued at $5,700, and her cargo at $36,943, total $42,643, so that the award may be set down as **one fifth**」 | CONFIRMED（金額與五分之一都對）；**但 `mc4i` 的「隔年三月」錯，見 F3** |
| c33 | 化驗（Dr. J. Patron，1873-01-30）證明不是血 | `not-blood/mc4a`、`doctor-signed/mc4b` | MCN/doctor 全文：「**Gibraltar, 30th January 1873**」…「there is no blood either in the stains observed on the deck of the Mary Celeste or on those found on the blade of the sword」，署名「(Sig'd) J. PATRON / M.D.」 | CONFIRMED（旁白說的是「日期是」，而文件上署的正是這個日期——報告內文提到 1 月 31 日才取件，站上也註了這個矛盾，所以「日期是」比「做化驗的那天」準確） |
| c35 | 紐約時報 1873-02-26 轉載波士頓郵報的標題 | `news-crossed/mc4g`、`headline-murdered/mc4h` | C-NYT 全文「**A Brig's Officers Believed to Have Been Murdered at Sea.** From the Boston Post. Feb. 24.」 | CONFIRMED（旁白只用標題；內文的 236 噸、11-17 出港、towed into Gibraltar 都與他源不合，一句都沒有引） |
| c36 | 德沃從熱那亞被召回，1873-03-04 第三次受訊 | `deveau-recalled/mc4f` | THP「**Oliver Deveau himself was later recalled from Genoa to be cross-examined for a third time in the court, on 4 March 1873**」（單一來源，THP 另寫 Dei Gratia 12-23 由德沃指揮駛往熱那亞、01-16 抵達，時間上成立） | CONFIRMED（仍是單一來源，照第一輪註明） |
| c52 | 1885-07 波士頓審判，陪審團 7:5 僵局 | `hoax-jury/mc7u` | SL「**The July 1885 trial** of Capt. Parker…」「the jury returned with a shocker: They'd **deadlocked, 7-5**, with the majority in favor of conviction」 | CONFIRMED（單一來源；旁白沒有講哪一邊多數，比來源保守） |
| M9 | `cargo-stats`：1,701 桶工業用酒精／1 桶被打開過／出處「直布羅陀勘驗報告 1872-12-23」 | `cargo-stats.data` | SM「1,701 barrels of **industrial** alcohol」；NEHS「denatured alcohol, which is undrinkable but commonly used for fuel and other **industrial** purposes」；MCN/facts 第 10 條「1,701 barrels of alcohol shipped by Meissner, Ackerman & Co.」；出處同 c25 | CONFIRMED（「工業用」有兩個來源；SK 與 MCN/about 反對，見第八節） |
| M11 | `award-stats`：1,700 英鎊／42,643 美元／出處「直布羅陀副海事法院 1873-03」 | `award-stats.data` | 同 c37 | CONFIRMED（卡片的「1873-03」沒有「隔年」的問題，錯只在旁白） |
| M15 | `sources[]` 20 筆、`checked_on` 2026-10-10 | `sources` | 20 筆我當天全部重開，**全部 200**；`sources[0]`／`[1]` 的快照與原站逐字相符 | CONFIRMED（兩個註記見第八節） |

**抽樣結果：22 條全部 CONFIRMED**（其中 c23／c44 牽出 F2、c37 牽出 F3——兩個都不是這幾條主張本身錯，
而是稿子把對的事實接成了不對的句子）。

## 六、插圖問題：`lookout-glass` 畫的是誰

`NOTES.md` 已經把這一處列成「畫面與旁白對不上，但不能改」（插圖畫好、付過錢）。要我判的是**哪一邊有來源**：

- **望遠鏡在船長手上，有兩個互相獨立的來源。** AH：「her **master, David Reed Morehouse**, sighted a sailing ship
  on his port bow, to windward. **Through a glass he perceived** that she was another brigantine…」；
  THP 引他在法庭上的證詞：「Capt. Morehouse testified that, on the day the Dei Gratia encountered the derelict,
  **through his telescope** from a distance he 'saw the marks or spalls on the bows of the Mary Celeste'」。
- **「瞭望手」一個來源都沒有。** 泛指「船員發現」的有三個（SM「crew members spotted」、NEHS「the crew of a Canadian
  vessel… sighted」、HH「spotted by the crew of British ship Dei Gratia」），FV 寫的是**舵手**（「the helmsman spied a vessel
  about 6 miles off」）。**沒有任何一個來源把望遠鏡交給瞭望手或舵手。**

**判定：旁白 `mc1b`「一艘英國帆船的船長舉起望遠鏡」是有來源的那一邊，不要改回去；要改的是畫。**
（順帶一提「英國帆船」也站得住：Chronicle 1873-01-31 自己寫「the Master and crew of the **British ship** Dei Gratia」，
HH 同；AH 寫 Nova Scotian、ACD 寫 Canadian，1872 年的新斯科舍兩者都對。）

重畫那一張的票照第一版第二輪的做法寫，只換主體與地點、不動景別、單一主體與光線：

- 現在：`Medium shot of a lookout on a wooden foredeck in grey daylight, a bearded sailor in a thick knitted cap
  raising a brass telescope to one eye, rigging behind him, light from an overcast sky on the left`
- 應該變成：`Medium shot of a ship's master on a wooden quarterdeck in grey daylight, a bearded captain in a peaked
  cap and dark coat raising a brass telescope to one eye, rigging behind him, light from an overcast sky on the left`

這樣也和同一章後面 `dei-gratia` 的 prompt（`a sea captain in a peaked cap on a sunlit quarterdeck`）連得起來，
而且仍然是卡通化、不寫名字、不追求相似。

## 七、還要改的（4 處＋2 處建議）

每一條只動事實與接法，不動順序、節奏、場景數與行 id；括號裡是 `spokenUnits`（現在→改後），算法照 `core/timeline.mjs`。

| # | 行 id／欄位 | 現在的字 | 應該變成 | 為什麼 |
|---|---|---|---|---|
| **F1** | `nine-empty.data.sub` | 「其他的沒有漏」 | 「**只有這九桶是空的**」 | 沒有來源說其餘 1,692 桶沒有漏。SM／MCN/barrel 只說「nine of the 1,701 barrels… were empty」；MCN/about 反過來寫這個漏損量「**This level of shrinkage was considered normal**, and differences in the wood used to make the barrels could account for leaks」——卡片上寫「其他的沒有漏」等於把來源說正常的事講成全有全無。第一輪給的第二個寫法（「1,701 桶裡只有這 9 桶是空的」）才有來源，建議用它的短版。這是第一輪自己的建議沒有來源，不是撰稿加的 |
| **F2** | `main-hatch-closed/mc6c` | 「可是主艙口是蓋好的。」（9） | 「**可是那塊艙蓋是取下來放好的。**」（14）<br>或刪掉這一句，讓 `mc6d`「上船的人，也沒有報告聞到什麼味道」直接接 `mc6b` | **事實是真的，反駁對不上。**前一句 `mc6b` 講的是船主主張自燃「把**前艙蓋**掀了開來」（AH：「blowing off the **fore hatch** cover, as the Celeste's then principal owner, Captain J. H. Winchester, afterward maintained」），而「主艙口是蓋好的」反駁的是 SM 版本的說法（「alcohol vapors… blew off the **main** hatch」）。更糟的是第 1 章的 `mc1g` 已經告訴聽眾「**前艙口開著**」——聽眾手上的事實正好支持船主，而旁白卻用另一個艙口來否認他。真正擋得住「被掀開」的證據是艙蓋的狀態：SK「the forehatch… and the lazarette hatch had both been **removed and were stowed**」、FV「the fore and lazarette hatches were open, **with their covers nearby, on the deck**」——取下來放好的蓋子不是被炸開的蓋子。後面 `mc6e`（Austin 第 61 段「no explosion or any fire」）才是致命那一刀，所以刪掉也不傷這一段 |
| **F3** | `award-stats`／`mc4i` | 「隔年三月，法庭判了救難金，一千七百英鎊。」（17） | 「**那年三月**，法庭判了救難金，一千七百英鎊。」（17） | **判決是 1873 年**（Chronicle 1873-03-15：「In the Vice Admiralty Court **yesterday**…」，即 1873-03-14），而這一句前面兩句已經把聽眾放在 1873 年了：`mc4b` 明說「一八七三年一月三十日」，`mc4d` 再加「一個多月後」（＝1873 年 3 月初）。接著說「隔年三月」，聽到的是 **1874 年 3 月**，差了一年。（`mc5a`「十二年後的一八八四年」沒有這個問題，因為同一句就把年份說出來、聽眾自己會校正；`mc4i` 沒有年份可以校正。）這一句第一版也是這樣寫（`ycs4`），但第一版那一章沒有先講出 1873，第二版把年份提前講了，這個相對詞就壞了——是重講的連帶，不是舊錯 |
| **F4** | `scenes[].chapter` 第 6 章 | 「說法一個一個掉下來」 | 「**船主說是酒精自己起了火**」<br>或「**天文鐘差了一百二十哩**」 | 見第四節：寫的是章的功能（`script-writing.md` 第 94 行禁止）、和旁白 `mc4e` 幾乎同一句、而且這一章最後三分之一（Shufeldt 那句「理由不充分」＋2007 年的誤判進水）**沒有掉下來**，是被帶進第 7 章的那一條，章節清單的讀者跳進來會對不上。兩個替代寫法都是章內的事件、都有來源（AH／SM），也和其他六章「章名＝章內第一個事件」的寫法一致 |
| S1 | `scenes[].chapter` 第 2 章 | 「他把這艘空船開進直布羅陀」 | 「**大副**把這艘空船開進直布羅陀」 | 事實沒問題（MCN/facts 第 8 條就是「Mate Deveau」），但章名在 YouTube 的清單上是單獨讀的，「他」沒有前文可以指。建議，不是必要 |
| S2 | `youtube.description` 第二段開頭 | 「這一集照事情被查出來的順序講完這份檔案：…」 | 「這一集**從大副爬上甲板那一刻開始**，講完這份檔案：…」 | 第一輪把這一句列為 NOT FOUND，撰稿以「那是對結構的說法、不是歷史主張」保留。我同意它不是歷史主張，但它是觀眾**對著影片就能驗**的一句話，而且對不上：熱那亞卸貨是 1873 年的事（AH「It was not until February, 1873, that the court released the Celeste to proceed to Genoa」），排在第 5 章的 1884 年與第 6 章的 2007 年之後。拿掉「順序」兩個字就不必解釋了。建議，不是必要 |

## 八、懷疑但不要求改

- **升降索：Austin 的報告反對它斷過。** 第 5 段「The peak halyards and throat halyards appeared to be the same with wh.
  she had been rigged… **None of them had been recently spliced** and they were all in good working condition.
  If the peak halyards had been carried away during her last voyage they must have been subsequently spliced
  wh. was not the case」，第 6、7 段還從 gaff 與 main boom 的完好推同一個結論。稿子把斷繩放在**登船那天**
  （`mc1k`，來源是 MCN/about 轉的 Anderson 證詞與 SK），第 7 章用它的那幾句又整段掛在 `mc7g`「最站得住的版本是」底下，
  所以旁白沒有說錯；但這是全片最後那個解釋踩著的那條繩子，而一手勘驗報告明文不同意。
  **值得站主知道**，不必改字；真要補，`mc7d` 那種「兩邊量的不是同一件事」的句法可以再用一次。
- **「工業用酒精」有兩派。** 支持：SM「industrial alcohol」、NEHS「undrinkable but commonly used for fuel and other
  industrial purposes」。反對：SK「1,701 wooden barrels of **pure grain alcohol, intended to fortify cheap Italian wines**」、
  MCN/about「The cargo was Spirit, today called **ethanol** shipped for the purpose of fortifying wine. Some books say it was
  'denatured alcohol' **this is clearly nonsense**… denaturing… started in the United States 1906」。
  旁白講的「那不是拿來喝的」兩派都同意，`mc2o` 與卡片的「工業用」只有一派。
  不要求改（有兩個來源），但若站主想完全避開爭議，`mc2o` 改成「那一千七百零一桶裝的是酒精」也不影響任何後續。
- **`mc6u`「以為船要沉了，是一個船長會做的判斷」**：`NOTES.md` 說它被 `mc7g` 的標記蓋住了——**時間上不可能**
  （`mc6u` 第 112 句、`mc7g` 第 121 句）。不過這一句本身有來源：SK「Briggs' action, though ultimately disastrous,
  was **more than reasonable** at the time」、MCN/about「A theory at the time of the inquiry was that the Captain and crew
  may have abandoned ship because they thought she was about to sink」。所以不是沒有根據的判斷句，不要求改；
  若站主要照 `script-writing.md` 第 114 行只留一句講述者在場，再標成意見就好。
- **`cargo-stats` 的出處精確度**：Austin 的報告全文**沒有一段寫到那 1,701 桶貨**（第 59 段寫的是後艙的補給桶）。
  1,701 這個數字出自船運與保險紀錄（MCN/facts 第 10 條），「一桶被打開過」出自 Chronicle 轉的
  「a special survey… in the first instance on the 23d December… **and a subsequent survey**」。
  卡片寫「直布羅陀勘驗報告 1872-12-23」仍站得住（AH 就稱那次是「A survey of the 1,701 barrels」，勘驗也是從 12-23 開始），
  但嚴格說是「勘驗結果」而不是「Austin 的那份報告」。R10 既然把另一張卡的出處拆開了，這張要一起精確化也可以，
  不是錯。
- **`mc5n`「再後來，還有人把她算進百慕達三角」**：沒有來源給百慕達三角這個說法的年份；FV 把它寫成
  「**modern-day** cases of alien abduction and Bermuda Triangle losses」，而 MCN/about 說海怪是「at the time」的說法，
  所以「再後來」在方向上成立。保留，但這是全稿唯一一個沒有來源直接標年代的先後詞。
- **`mc5a`「十二年後的一八八四年」**：1872 到 1884 是 12 個年份，`claims.md` 也照實寫了算法；但從 1872-12 的發現
  到 1884-01 的刊登其實是 11 年多（AH 自己寫「**Eleven years later**」）。因為同一句就說出 1884，聽眾不會被誤導，
  所以不要求改（和 F3 的差別就在有沒有絕對年份可以校正）。
- **`mc3k`「航海手冊和船籍文件，也一起被帶走了」**：來源寫的是 missing／were missing（AH），「被帶走」是推論；
  但下一句 `mc3q`「帶走的是找路的工具」第一版就 CONFIRMED 過，同一個框架，保留。
- **`mc6l`「連貨都是完好的」**：Chronicle 第 1 點是「all… in good order and condition, **except one which had been started**」。
  那一桶的例外聽眾在 `mc2p` 已經聽過，`mc7d` 又把兩次清點的差別講清楚了，保留。
- **第一輪的一個記述要更正**：`verify-1.md` 的網址表寫 `maryceleste.net/barrel.htm`「內容是框架頁，文字在 about.htm」。
  我今天抓到的 barrel.htm **有內文**：「The cargo consisted of 1,701 barrels of alcohol shipped by Meissner, Ackerman & Co.
  of New York. There were no other goods loaded on board. When the ship was unloaded, the cargo was found to contain
  nine empty barrels.」＋紅橡木那一整段。所以 `sources[7]` 是一筆有效來源（它支撐 c47、c48），不是空頁。
- **`sources[0]`／`[1]` 的快照日期（2026-09-20、2026-08-19）早於 `checked_on` 的 2026-10-10**：第一輪列在要求之外，我同意
  不影響任何判定（兩邊今天都 200、逐字相符）。要嚴謹就把這兩筆換回原站網址（今天也開得了），或把 `checked_on` 標成快照日。
- **會過期的事實：沒有。** 看到的頁面日期：Britannica 標「Last updated Sep. 18, 2026」、SM 2007-11、AH 1981-02／03、
  THP 2023-01-05、SK 2011-12-20、SL 2011-12、ACD 2021-10-31、NEHS「updated in 2026」、MCN 各頁無日期。

## 九、改完有沒有把第一輪過的東西弄壞（聽眾檢查）

照 `core/narrative.mjs`／`core/timeline.mjs` 的算法自己跑（`listener.mjs`，沒有執行任何影片階段）：

- **`loops` 五組都還兌現，而且回收時帶的是聽眾還沒有的東西**（規則第 106 行）：
  `mc1i`→`mc6r`（隔 100 句，下一句給「兩具幫浦被拆開了一具」）、`mc1k`→`mc7i`（隔 112 句，下一句給「小艇被綁在繩子後面」）、
  `mc2l`→`mc6i`（隔 76 句，下一句給「船沉了，賠的是他自己」）、`mc3t`→`mc7n`（隔 78 句，下一句給氣象資料回推）、
  `mc4m`→`mc5g`（隔 8 句，給「連這篇小說裡都沒有」）。最後那一組雖然只隔 8 句，但它**不是**「還記得」句式，
  正是規則第 103 行要求的做法（近的東西直接接著講下去）。埋設沒有一個落在片尾，有兩個埋在第 1 章的開場濃縮。
- **沒有數字被講到第三句**：跳過回呼句之後，出現在兩句的只有「一千七百零一桶」（`mc2o`、`mc7b`），
  工具的門檻是三句以上才警告；而 `mc7b` 是規則允許的點名回呼，下一句 `mc7d`「勘驗官在直布羅陀數的是有沒有人動過，
  不是桶裡還剩多少」當場說明為什麼要數第二次。「十二月」「十一月」各出現兩句，但指的是不同日子（12-04／12-23、11-07／11-25），
  不是同一個事實講兩次。
- **「還記得」三句（上限五句），沒有連著**：`mc6i`（第 100 句）、`mc7i`（123）、`mc7n`（128），每一句的前一句都不是「還記得」。
- **七章的第一句都還是接住上一章的事或答案，沒有一句是標籤句**（我用 `LABEL_OPENERS` 的十個樣式比對，0 命中）：
  第 2 章接第 1 章的問句、第 3 章接「但這還不是最奇怪的地方」、第 4 章回答「送去化驗」、第 5 章回答「那頓飯菜是誰加上去的」、
  第 6 章回答「當年的人自己怎麼解釋」、第 7 章接「還有一個數字沒有人提過」。**R8／R9／R13 改的三句都不是章首，鏈子沒有斷。**
- **單位數**：140 句共 2,215 單位，最長 25 單位三句（`mc2m`、`mc3p`、`mc7d`），其餘 ≤24；上限沒有被改動推破
  （`mc2m` 從 26 降到 25）。F1–F4 的改法：F1 的卡片欄位不是旁白，F2 9→14，F3 17→17，F4 是章名，都不碰上限。
- **片尾**：三句，沒有講下一支／下一集／下一份檔案（符合 10-13 的新規則），只求訂閱一次，沒有連續三個請求。
- **內容守則**：傳說都標成加上去的、而且現在都不講先後；沒有定論說了沒有定論（`mc7v`、`unsettled` 卡）；
  沒有編造布里格斯一家的對話或心理（第 7 章整段掛在 `mc7g` 的標記底下）；沒有血腥（Solly-Flood 的信裡連妻女都被殺，
  旁白只說殺了船長）；沒有「經查證」「根據官方文件」「本影片」；旁白沒有括號或網址；唯一的拉丁字 Dei Gratia 在
  第一版就進了 `lexicon.json`。

## 摘要

- **二十三處已改動：CONFIRMED 22、NOT FOUND 1。**唯一沒改對的是 **R11**（`nine-empty.data.sub` 的「其他的沒有漏」）——
  而且錯的是第一輪給的那個寫法，不是撰稿加的。第一輪指定重查的 R1–R12 全部重讀一手文件，
  兩個真正的錯（天文鐘 120 哩的方向、熱飯菜算回 1884 小說）都改對了，`claims.md` c45 也跟著對了。
- **五處偏離：四處成立，第五處其實沒有偏離。**`mc1a`（17°W 不是「正中間」，而第二個寫法會先講掉 `mc5o`）、
  `mc3f`（「奇怪的是」是 `narrative.mjs` 數得到的升級句，那一段隔了 21 句沒有別的鉤子）、
  `mc7x`（`script-writing.md` §結尾明文要求「未結」的片尾不下結論，比第一輪的建議更對）都站得住；
  **`mc3h` 那個自己加的標記擋掉了一個新的錯誤歸屬**——THP 寫得很清楚：Dei Gratia 的人沒有一個在船艏看到值得起疑的傷，
  刀痕是 Austin 的用語，前兩句改成「那天」之後若不把視角交回勘驗官，就會變成把刀痕算進登船那天的證詞。
  `mc7g` 和第一輪給的字一模一樣。
- **第 3 章的歸屬站得住，標記沒有超載**：換日子的那一句同時換了日子與觀察者、「那天」只跨一句、下一句立刻點名勘驗官，
  是 A–A–B 而不是 A–B–A–B；插圖也剛好把水手與勘驗官分開畫。
- **七個章名：CONFIRMED 5、要改 1、建議改字 1。**第 6 章「說法一個一個掉下來」寫的是章的功能、和 `mc4e` 幾乎同一句，
  而且這一章最後三分之一那條說法沒有掉下來。
- **抽樣 22 條（第一輪 50 條 CONFIRMED 的 44%，門檻 17），全部 CONFIRMED。**挑法不抽籤：最後那個解釋踩著的 8 條、
  緊貼被改句子的 7 條、單一來源的 4 條、觀眾讀得到的欄位 3 條。其中兩條牽出了稿子的接法問題（F2、F3），
  主張本身沒有一條錯。
- **插圖問題有答案：旁白對、畫要改。**望遠鏡在船長手上有兩個獨立來源（AH 的「Through a glass he perceived」、
  THP 引莫爾豪斯的庭上證詞「through his telescope」），「瞭望手」一個來源都沒有。
  第六節給了只換主體與地點的重畫 prompt。
- **還要改 4 處**：F1 `nine-empty.data.sub`「其他的沒有漏」→「只有這九桶是空的」；
  F2 `mc6c` 用錯艙口反駁船主的自燃說（而第 1 章已經說前艙口開著）；
  F3 `mc4i`「隔年三月」把 1873 年 3 月的判決講成 1874 年；F4 第 6 章章名。
  另有兩處建議（第 2 章章名的「他」、說明欄的「順序」）。四處都只改一個欄位或一句話，不需要新的查核。
- **第三輪：不需要。**這一輪要改的是 **3 個事實／歸屬＋1 個章名**，沒有超過三個事實的門檻（F1 卡片、F2 接法、F3 日期），
  而且三個都在這一份裡寫明了該變成什麼字與來源句。
- **結論：F1–F4 改完之前還不能進畫面與配音；改完就可以。**另外 `NOTES.md` 自己註明
  **〈說故事關卡〉的十題在這一輪動了十六句旁白之後還沒有重跑**（十題全過的紀錄是第二稿那一次）。
  那不是事實問題，我也沒有跑；但它是交片前的關卡，請在 F1–F4 改完之後讓一個沒看過稿子的讀者答一次。
