# curio-s25-v2 查核第二輪（2026-11 重做稿）

- **查核日期**：2026-11-13。查核者沒有參與撰稿。
- **範圍**：`video.json` 的 `scenes[].lines[].text`，共 120 句（t001–t120）、120 景（`say` 只管讀音，沒有查），加上 `youtube.title`、`youtube.description` 裡的事實。章名（`chapter`）有事實的也順手看了。
  另外查了 `curio-redo-handoff/drafts/curio-s25-v2/changes.md`：〈【待查】清單〉寫「無」；〈原稿沒有、這一輪新寫進旁白的事實句〉列了 9 句（t003、t008、t010、t012、t013、t021、t025、t026、t043）；
  第 10 點〈合併或改寫（意思不變）〉列了 5 處（t089、t060、t105、t112–t113、t120）；第 5、7、8 點也有改寫（t023–t024、t116、t117–t118 等）。這些逐條判定如下。
  （`video.json` 和草稿資料夾那份台詞一字不差，差在其他欄位。）
- **方法**：逐句看人名、年份、數字、引號裡的話、誰說的、事件順序，以及「第一個」「親口」「沒有一個」「只有」「到今天」「可以結案」這類強詞。對照的是 `claims.md`、`verify-1.md`（第一版查核加獨立覆核，44 列）、`brief.md`、`NOTES.md`。
  注意：`claims.md` 的行號還是舊的 nw001–nw623，這次的 t001–t120 是照句子內容對回去的。這次沒有只照抄前一份：`video.json` 的 `sources` 列的固定文本，抓得到的都**重新抓下來逐字核對**：
  - STUK-NP＝Newton Project `OTHE00001`（normalized，Stukeley 1752 回憶錄全文）：f. 10r–11r（1721 年）、f. 14r–15r（1726-04-15、喝茶、蘋果段）、族譜（born 25 dec. … 1642-3）、f. 77r（20 march 1726-7）、書名頁與序。全文檢索「apple」6 次，全部在 f. 15r 同一段，沒有「head」跟蘋果連在一起
  - NATP00385＝牛頓 MS Add. 3968 f. 85r（diplomatic）：1665 級數、切線、流數；「the next year in Ianuary had the Theory of colours」；「And the same year I began to think of gravity extending to ye orb of the Moon」；行間「All this was in the two plague years of 1665 & 1666」。整頁「apple」0 次
  - COND＝Newton Project `THEM00167`（Keynes 130.04，diplomatic）、`THEM00145`（129.01）、`THEM00146`（129.02）
  - PEMB＝archive.org `viewofsirisaacne00pemb` 全文 OCR：序「As he sat alone in a garden … why not as high as the moon, said he to himself」；「apple」只出現在訂戶名單的「Appleby」
  - VOLT-1727＝archive.org `bim_eighteenth-century_an-essay-upon-the-civil-_voltaire_1727` OCR；VOLT-ELEM 1741＝`bim_eighteenth-century_elements-de-la-philosop_voltaire_1741` OCR；VOLT-LET＝Gutenberg 2445 前言
  - PHIL1739＝`philosophicaldis00londiala` OCR（書名頁 MDCCXXXIX，約 1.9 萬字，「Newton」0 次）；PHIL1740＝`bim_eighteenth-century_a-philosophical-disserta_philalethes_1740` OCR（約 2.9 萬字，p. 76 那段在）
  - EULER＝`lettresuneprinc02eulegoog`（1768 本 OCR）；EULER 1795＝`letterseulertoa00eulegoog`（英譯 OCR，含 Hunter 前言的「F. E.」說明）
  - FONB＝`englandunderseve01fonbuoft` OCR（〈Signs of the Times in 1829〉pp. 223–224）
  - BREW1831＝`b33028035_0001` OCR（p. 148 正文、p. 344 兩條註）；BREW1855＝Newton Project `OTHE00097`（ch. II 正文與註 [18]）
  - HAYCOCK＝Newton Project `OTHE00017`；KEES＝York 的 Keesing PDF（pdftotext）；YORK＝York〈Newton's apple tree〉頁；NT＝National Trust 兩頁
  - 沒有重開、**沿用 verify-1** 的：STUK-MS 手稿掃描（1936 年贈皇家學會的題字）、PHIL1740 書名頁年份（OCR 沒抓到，verify-1 看過頁影像）、EULER 1768 書名頁年份與「comme la lune ne lui tomba point sur la tête」（OCR 字形壞了，抓不到）、
    1795 英譯本的出版年、VOLT-1727 書名頁（OCR 壞了）、伏爾泰 1738 年三本（只開了 1741 本）、WP 的二手資料（外甥女管家、康杜特在造幣廠當副手）、「第一部大部頭的牛頓傳」（verify-1 第 40 列備註，沒有原文引句）。
- **結論摘要**：主幹沒有問題。斯塔克利手稿（1726-04-15、肯辛頓、單獨吃飯、飯後蘋果樹下喝茶、「same situation」、坐著沉思、垂直落地、地球的中心、拉力跟物質多少成比例、蘋果也拉地球、只說 formerly、全稿只這一段）、
  牛頓筆記（1666、月亮、兩個瘟疫年、沒有蘋果）、康杜特三份草稿（1665／1666、沉思／看見蘋果掉下）、伏爾泰 1727 的散步與 1741 年才補的外甥女、彭伯頓 1728（花園、月亮、沒有蘋果）、
  小冊子（1739 年沒有、第二版 p. 76 的「fell on his Head」「according to Pemberton」「整個果園」）、歐拉（躺著、蘋果掉在頭上、月亮沒掉下來、「我們說不定還不懂」、1795 英譯照寫、F. E. 的註是巴黎版編者的）、
  1829 年的玩笑、Brewster 1831／1855、Turnor 1806、Keesing 的推論與 Whiteside、Haycock、York 與 NT 的現況，都逐字對得上。verify-1 的但書（目前找得到最早、說是根據彭伯頓、1741 不說 1738、牛頓晚年不用 c. 1714、
  不給樹倒的年份、不說牛頓指認那棵樹、不說「從來沒寫過」）全部守住了。**要改 4 句**：
  - stuk-intro（t021）「**說出**這件事的人，是一位醫生，叫斯塔克利」：說的人是牛頓，斯塔克利是聽的、記的人；「要等到牛頓八十三歲」也只能說是目前找得到最早、有日期的一次。
  - stuk-notyet（t024）「因為那一年，他還沒聽過蘋果的故事」：Keesing 原文是「may not have been aware」（**可能**），還自己承認這個解釋有點牽強（「ingenuity」）。旁白要保留「可能」，並掛在學者身上。
  - diary-who（t030）「這本日記，是一位研究牛頓蘋果樹的學者**翻出來的**」：Keesing 只是在論文裡**引**了日記，沒有任何來源說是他發現的。
  - schoolboy-branch（t108）「老師還帶著**全班同學**，去鋸了幾段樹枝」：1912 年那封信寫的是「Mr Pearson and **several of the boys**」，鋸樹枝的是老師本人。這是這次重抓 KEES 才抓到的，verify-1 第 30 列備註寫「老師帶學生去鋸了幾段樹枝」，沒有「全班」。
- changes.md：【待查】**確實是 0 條**，新稿沒有用到查核表以外的事實。但「新寫進旁白」的 9 句裡，t021 **要改**（見上），t003 **通過但記一筆**，其他 7 句（t008、t010、t012、t013、t025、t026、t043）**通過**。
  「意思不變」的 5 處：t089、t105、t112–t113、t120 **通過**；t060「牛頓自己，兩年都認」**記一筆**。另外第 5 點把 nw606 搬到 t024 時，連帶把 verify-1 沒加的「可能」也漏了，**要改**（見上）。
- `youtube.description`：**要改一處，建議改一處**。「他一七五二年寫成的回憶錄手稿」的「他」最近的先行詞是牛頓，聽起來像牛頓寫的回憶錄（牛頓 1727 年就過世了），要改成「斯塔克利」；
  「牛頓親口說的是『一顆蘋果掉了下來』」的引號會被當成牛頓的原話，其實那是斯塔克利 1752 年的轉述，建議拿掉引號。
- `youtube.title`「1726 年他親口說的，只有掉下來」：**通過（記一筆）**。誰記下的：斯塔克利（醫生，那天在場）。哪一年說的：1726 年 4 月 15 日（4 月已經過了舊曆新年 3 月 25 日，新舊曆都是 1726；KEES 寫「15 April 1725/6」是 Keesing 自己寫錯）。
  哪一年寫成：斯塔克利 1752 年完成的回憶錄手稿（STUK-NP 書名頁「William Stukeley 1752」）。哪一年出版：1936 年（HAYCOCK「published in 1936」）。而且斯塔克利當天的日記有這頓飯、沒有蘋果（KEES 轉引）。
  「親口」照字面成立：斯塔克利寫的是「he told me」，是當面聽到的，不是轉了好幾手；可是我們手上的字是 26 年後寫下的轉述（verify-1 第 3 列「最接近牛頓親口說的版本，但仍是斯塔克利的轉述」）。標題要短，可以照用，條件是說明欄把「斯塔克利一七五二年記下、一九三六年才出版」寫清楚（照上面改了以後就有）。

## 判定表

| 景 id（句 id） | 句子（原文） | 判定 | 依據 | 建議改法 |
| --- | --- | --- | --- | --- |
| stuk-intro（t021，changes 新句） | 要等到牛頓八十三歲。說出這件事的人，是一位醫生，叫斯塔克利。 | 要改 | 接的是 t020「那這顆蘋果，最早是從誰的嘴裡，說出來的？」。STUK-NP f. 15r（重抓）：「amidst other discourse, **he told me**, he was just in the same situation, as when formerly, the notion of gravitation came into his mind」。說的人是牛頓，斯塔克利是聽到並寫下來的人。「要等到牛頓八十三歲」暗示在那之前沒人說過；我們只知道這是目前找得到、有日期的最早一次（康杜特 c. 1727–28、伏爾泰 1727、外甥女告訴伏爾泰的時間不詳，verify-1 #9、#12、#13）。算術 1642-12-25 到 1726-04-15＝83 歲對 | 目前找得到最早的一次，是牛頓八十三歲那年，講給一位醫生聽的。這位醫生，叫斯塔克利。 |
| stuk-notyet（t024，changes #5） | 先別急著下結論：因為那一年，他還沒聽過蘋果的故事。 | 要改 | KEES p. 386（重抓）：「Stukeley **may not have been aware** of the story till five years after this visit which could explain the omission. I must admit to a certain amount of `ingenuity' in this explanation」。原文是「可能」，作者自己還說有點牽強。verify-1 #39 備註也寫了「KEES 自己也承認這個解釋有點『ingenuity』」。站主規則：原文的「可能」要保留 | 先別急著下結論：研究這棵樹的學者猜，可能是那一年，他還沒聽過蘋果的故事。 |
| diary-who（t030） | 這本日記，是一位研究牛頓蘋果樹的學者翻出來的。那蘋果去了哪裡？ | 要改 | KEES（重抓）：「Yet another version was given by William Stukeley who visited Sir Isaac Newton on 15 April 1725/6, as his diary records: Ap.15. I din'd with him at his Lodgings alone, at Orbels buildings Kensington」；「Although the account of the incident of the apple does not appear in Stukeley's diary」。Keesing 是**引用**日記，沒有說是他找到的；verify-1 #44 也只寫「KEES 轉引」「日記原件 UNOPENED」。「翻出來」多了一件來源沒有的事 | 這段日記，是一位研究牛頓蘋果樹的學者，在論文裡引出來的。那蘋果去了哪裡？ |
| schoolboy-branch（t108） | 老師還帶著全班同學，去鋸了幾段樹枝。 | 要改 | KEES p. 381–382 轉引 Walker 1912-01-12 的信（重抓）：「The school master, Mr Pearson **and several of the boys** at once set off for Woolsthorpe … he obtained a saw from somewhere and **sawed a good many logs of wood from the branches**. My father got one of these pieces」。是幾個學生，不是全班；鋸的是老師；鋸下的是「好幾段」。verify-1 #30 備註「老師帶學生去鋸了幾段樹枝」沒有「全班」，「全班」是 NOTES 第二版加長時寫進來的 | 老師帶著幾個學生趕了過去，還從樹枝上鋸下好幾段木頭。 |
| open-you（t001） | 你一定聽過：蘋果砸到牛頓的頭，他想到了萬有引力。 | 通過 | 用「你一定聽過」框住，講的是流傳的版本（verify-1 #27：COLE 1824「an apple fell on his head」、FONB 1829） | — |
| open-books（t002） | 這一下，從童書一路砸到課本，你小時候大概也是這樣聽來的。 | 通過 | verify-1 #27 備註「20 世紀以後的童書、教材幾乎都寫打到頭（FTS 大量命中），但沒有逐本看」；有「大概」 | — |
| open-but（t003，changes 新句） | 可是你想不到：聽過牛頓親口講這件事的人，沒有一個寫蘋果打到他的頭。 | 通過（記一筆） | verify-1 #24 CONFIRMED：斯塔克利「occasion'd by the fall of an apple」、康杜特「made an apple fall from the tree to the ground」「observing an apple fall from a tree」（都重抓）。限制：#24 也把伏爾泰和格林算進去，但伏爾泰是聽外甥女說的、格林是聽福克斯說的，不是「聽過牛頓親口講」；直接聽過的只有斯塔克利（還有康杜特、彭伯頓）。這句只說「沒有一個寫打到頭」，對這幾個人都成立；「沒有一個」指的是留下紀錄的人。要更穩可以加「留下紀錄的」 | （可選）可是你想不到：聽過牛頓親口講、又留下紀錄的人，沒有一個寫蘋果打到他的頭。 |
| open-moon（t004） | 更怪的是，牛頓自己的筆記，講到重力，寫的是月亮。 | 通過 | NATP00385 f. 85r（重抓）「And the same year I began to think of gravity extending to ye orb of the Moon」；整頁沒有 apple | — |
| open-pamphlet（t005） | 而打到頭的版本，目前找得到最早的，是一本連作者都不知道是誰的小冊子。 | 通過 | PHIL1740 p. 76（重抓）「an Apple which fell on his Head」；「目前找得到最早」照 verify-1 #25 覆核；作者不知道照 #25 備註（署名 Philalethes） | — |
| open-promise（t006） | 今天我們就來聊聊：那顆蘋果，到底有沒有打到牛頓的頭？ | 通過 | 承諾句，沒有事實 | — |
| origin-ada（t007） | ……要回答這一題，得先回到牛頓二十出頭的時候。 | 通過 | 1665 年夏天 22 歲（族譜 born 25 dec. 1642，重抓）；verify-1 #21 | — |
| origin-born（t008，changes 新句） | 牛頓一六四二年聖誕節出生，老家在英格蘭林肯郡的鄉下。 | 通過 | STUK-NP 族譜（重抓）：「Isaac Newton only child of Isaac & Hannah born 25 dec. baptizd at Colsterworth 1 jan. 1642-3」；同段「an estate at Wulsthorp in Colsterworth parish in that county」（that county＝前文的 Lincolnshire）；f. 10r「Wulsthorp, which parishes to Colsterworth, 6 mile on this side Grantham」。舊曆日期，#21 備註說新舊曆不用提 | — |
| origin-cambridge（t010，changes 新句） | 長大後，他到劍橋念書。一六六五年，一場瘟疫，讓劍橋停了課。 | 通過 | BREW1855 ch. II（重抓）「before the 8th of August 1665, when the College was "dismissed" on account of the Plague」；NT〈History〉（重抓）「At University, Newton made two extended trips back to Woolsthorpe Manor between the summer of 1665 and spring of 1667. This was to escape the Great Plague」 | — |
| origin-home（t011） | 牛頓只好回到鄉下老家。那時候，他二十三、四歲。 | 通過（記一筆） | 「二十三、四歲」是 verify-1 #21 建議的說法（「1665 年聖誕節滿 23、1666 年聖誕節滿 24」）。嚴格講，1665 年夏天剛回去時他 22 歲，一直待到 1667 年 4 月（24 歲）。t007 已經說「二十出頭」，不改也可以 | （可選）牛頓只好回到鄉下老家。那時候，他才二十出頭。 |
| origin-two-years（t012，changes 新句） | 前後算起來，他在鄉下待了將近兩年；中間劍橋只短暫開過幾個月。 | 通過 | NT（重抓）「between the summer of 1665 and spring of 1667」；verify-1 #19 KEES「The university opened for a few months between March and June 1666, but otherwise Newton was away until April 1667」（KEES 那句這次沒在 PDF 抽字裡重找，沿用） | — |
| origin-garden（t013，changes 新句） | 老家的花園裡，有一棵蘋果樹。這棵樹先記著，後面會再回來。 | 通過 | KEES（重抓）「the apple tree was the only one in his garden」；「By the year 1806 … the tree would have been about 150 years old」（也就是牛頓年輕時已經在） | — |
| origin-what、origin-list、origin-colours（t014–t016） | 多年以後，牛頓自己在一份筆記裡，寫下了那兩年。……一件一件列出自己年輕時做出來的東西：從數學裡的級數、切線，一路寫到光的顏色。 | 通過 | NATP00385（重抓）「In the beginning of the year 1665 I found the Method of approximating series … The same year in May I found the method of Tangents … & the next year in Ianuary had the Theory of colours」；「牛頓晚年」照 #15 覆核，不用 c. 1714 | — |
| origin-moon（t017） | 寫到一六六六年，他說：那一年，我開始想，重力能不能一路延伸到月亮。 | 通過 | 同上「And the same year I began to think of gravity extending to ye orb of the Moon」；「the same year」＝1666（#41） | — |
| origin-plague-years（t018） | 他又在行間補了一句：這些，都在那兩個瘟疫年裡。 | 通過 | NATP00385 行間（重抓）「\All this was in the two plague years of 1665 & 1666/」 | — |
| origin-noapple（t019） | 整份筆記，有月亮，沒有蘋果。到今天，還找不到牛頓親筆寫的蘋果。 | 通過 | NATP00385 整頁 apple 0 次（重抓）；#16「目前找不到牛頓親筆寫的蘋果」，不說「從來沒寫過」 | — |
| stuk-1721、stuk-notree（t022–t023） | 其實早在一七二一年，斯塔克利就去過牛頓鄉下的出生地。／可是他的紀錄裡，為什麼一個字都沒提到那棵蘋果樹？ | 通過 | STUK-NP f. 10r（重抓）「returning home on 13 october I visited Wulsthorp … I had the curiosity to visit the place where Sir Isaac was born」；全稿 apple 只在 f. 15r。KEES「The tree does not appear in Stukeley's drawing either」 | — |
| tea-garden（t025，changes 新句） | 五年後，一七二六年四月十五日，倫敦。斯塔克利去拜訪八十三歲的牛頓。 | 通過 | STUK-NP f. 14r（重抓）「on 15 April 1726 I paid a visit to Sir Isaac, at his lodgings in Orbels buildings, Kensington: din'd with him, & spent the whole day with him, alone」。1721→1726 五年。肯辛頓當時在倫敦城外，說明欄寫「倫敦肯辛頓」，可以 | — |
| tea-under（t026，changes 新句） | 天氣暖，飯後兩個人走進花園，在蘋果樹下喝茶，就他們兩個。 | 通過 | STUK-NP f. 15r（重抓）「after dinner, the weather being warm, we went into the garden, & drank thea under the shade of some appletrees, only he, & myself」 | — |
| same-situation（t027） | 牛頓說：當年想到重力，就是這樣的情境，一顆蘋果掉了下來。 | 通過 | 同上「he told me, he was just in the same situation, as when formerly, the notion of gravitation came into his mind … occasion'd by the fall of an apple」。「牛頓說」是斯塔克利寫的間接引述，沒有加引號，可以 | — |
| diary、diary-page（t028–t029） | 奇怪的是，斯塔克利那天的日記，記了這次拜訪，卻沒有蘋果。／日記那天寫的是：四月十五日，跟他單獨在肯辛頓的住處吃飯。 | 通過（二手） | KEES（重抓）「Ap.15. I din'd with him at his Lodgings alone, at Orbels buildings Kensington」「the account of the incident of the apple does not appear in Stukeley's diary」。日記原件沒開（#44） | — |
| manuscript（t031） | 蘋果在他一七五二年完成的回憶錄手稿裡；手稿今天收在英國皇家學會。 | 通過 | STUK-NP 書名頁（重抓）「MEMOIRS OF SIR ISAAC NEWTON'S life. William Stukeley 1752.」；目錄頁「Source: MS/142, Royal Society Library, London, UK」 | — |
| sat-thinking、why-perp、why-down（t032–t034） | ……那一次，他正坐著沉思。／他心裡想：為什麼蘋果總是垂直落到地上？／為什麼不往旁邊、不往上，偏偏總是掉向地球的中心？ | 通過 | STUK-NP f. 15r（重抓）「"why should that apple always descend perpendicularly to the ground," thought he to him self: occasion'd by the fall of an apple, as he sat in a comtemplative mood: "why should it not go sideways, or upwards? but constantly to the earths centre?"」 | — |
| earth-pulls、apple-pulls（t035–t036） | 他的答案是：地球在拉它。物質裡，一定有一種拉力，／而且拉力跟物質的多少成比例。所以，蘋果也在拉地球。 | 通過 | 同上「assuredly, the reason is, that the earth draws it. there must be a drawing power in matter … if matter thus draws matter; it must be in proportion of its quantity. therefore the apple draws the earth, as well as the earth draws the apple."」 | — |
| hearsay（t037） | 這是今天找得到、最接近牛頓親口說法的紀錄；不過，它仍是斯塔克利的轉述。 | 通過 | verify-1 #3 備註原話；不說「最早的紀錄」 | — |
| three-missing、no-head（t039–t040） | 手稿裡，三樣都沒有：沒有地點，沒有年份，只說「從前」；／也沒有一個字，說蘋果打到了他的頭。整份手稿，蘋果只出現在這一段。 | 通過 | STUK-NP「as when formerly」；全文檢索 apple 6 次，全部在 f. 15r 同一段約 800 字內（重抓） | — |
| you-rewind（t041） | 你可以回頭聽一次牛頓那句話：他說的是「掉了下來」。 | 通過（記一筆） | 「掉了下來」加了引號、說是牛頓的話，其實是斯塔克利的「occasion'd by the fall of an apple」。跟 t037 剛說完「仍是斯塔克利的轉述」連在一起聽，不會誤會；changes.md 也列它是可刪的景 | （可選）你可以回頭聽一次那句話：手稿寫的是「掉了下來」。 |
| years、years-184（t042–t043，t043 為 changes 新句） | 手稿一七五二年寫成，一九三六年才印成書；同一年，才送進皇家學會。／中間隔了一百八十四年。這段時間，蘋果的故事，早就在別人筆下傳開了。 | 通過 | HAYCOCK（重抓）「An edition of the Royal Society version of the biography was published in 1936」「it was almost two centuries before Stukeley's account was published」；送進皇家學會照 verify-1 #7（STUK-MS 題字，沿用，未重開）。1936−1752＝184。「早就傳開」：伏爾泰 1727、小冊子 1740、歐拉 1760/1768 都早於 1936（下面都重抓） | — |
| london-book、voltaire（t045–t046） | 不只。一七二七年三月，牛頓過世；同一年，倫敦就出了一本英文書，／寫到這顆蘋果。作者是法國作家伏爾泰，牛頓過世的時候，他人就在英國。 | 通過 | STUK-NP f. 77r（重抓）「he dy'd … the 20 march 1726-7」；VOLT-LET 前言（重抓）「He was here when Sir Isaac Newton died」；書名頁年份與倫敦沿用 verify-1 #12（OCR 壞了）。沒說「第一本印出來的」 | — |
| voltaire-quote、walking（t047–t048） | 他寫：牛頓在花園裡散步，看見一顆蘋果從樹上掉下來，／就有了重力學說的第一個念頭。這一次，他是在散步，不是坐著。 | 通過 | VOLT-1727（重抓）「Sir Isaak Newton walking in his Gardens had the first Thought of his System of Gravitation, upon seeing an Apple falling from a Tree」 | — |
| new-edition、niece-quote（t050–t051） | 十幾年後，一七四一年，他在另一本書的新版裡，才補上一句：／「這是他的外甥女告訴我的。」這位外甥女，替牛頓管過家。 | 通過 | VOLT-ELEM 1741（重抓 OCR）「Un jour en l'année 1666. Neuton retiré à la Campagne & voyant tomber des fruits d'un arbre, à ce que m'a conté sa nièce (Madame Conduit)」；1738 年本沒有，沿用 #43。1727→1741 是 14 年。「管過家」是 WP 二手（#13），沿用 | — |
| niece-scene（t052） | 那一段說：有一天，牛頓在鄉下，看見果子從樹上掉下來，就想得出神： | 通過（記一筆） | 同上「retiré à la Campagne & voyant tomber des fruits d'un arbre … se laissa aller à une méditation profonde」，年份不念，對。句尾是冒號，原稿冒號後面接的是 nw209（「是什麼，讓所有東西都朝著地球中心落下？」），重做時刪掉了，現在冒號後面什麼都沒有（文字問題，不是事實問題） | 那一段說：有一天，牛頓在鄉下，看見果子從樹上掉下來，就想得出神。 |
| niece-fruits（t053） | 你注意，她說的是「果子」，連蘋果都沒指名。 | 通過（記一筆） | 原文是 fruits（#13）。嚴格講「果子」是伏爾泰的用字，外甥女原話是什麼我們不知道；這句跟原片 nw210 一樣，verify-1 時通過 | （可選）你注意，這裡寫的是「果子」，連蘋果都沒指名。 |
| conduitt-mint、conduitt-drafts（t055–t056） | 外甥女的丈夫康杜特，是牛頓在造幣廠的副手。／牛頓過世以後，他著手替牛頓寫傳記，留下了好幾份草稿。 | 通過 | #9 備註（造幣廠副手，沿用）；COND 三份草稿（重抓） | — |
| musing-garden、garden-apple（t057–t058） | 有一份寫他在花園裡沉思，想到讓蘋果落地的那股力；／另一份寫他看見一顆蘋果，從樹上掉下來。…… | 通過 | THEM00167（重抓）「whilst he was musing in a garden it came into his thought that the same power of gravity (wch brought \made/ an apple \fall/ from the tree to the ground)」；THEM00145「by observing an apple fall from a tree」；THEM00146「from seeing an apple fall from a tree」 | — |
| year-card（t059） | 同一個人的稿子，有的寫一六六五年，有的寫一六六六年。 | 通過 | THEM00167「In the year 1666 {sic}」；THEM00145、00146「in the year 1665」（重抓） | — |
| both-years（t060，changes #10） | 還記得筆記行間那句嗎？「都在那兩個瘟疫年裡。」牛頓自己，兩年都認。 | 通過（記一筆） | 引的那句對（NATP00385 行間）。但「牛頓自己，兩年都認」接在「康杜特的年份對不上」後面，聽起來像牛頓替蘋果那一年給了答案。其實牛頓的筆記沒有蘋果，而且把重力想到月亮明寫在「the same year」＝1666（t017 自己就這樣講）；「兩個瘟疫年」是總括整張清單（1665 的級數、切線也在內）。claims 說這是白話、verify-1 時通過，所以不列「要改」；要更準可以改 | （可選）還記得筆記行間那句嗎？「都在那兩個瘟疫年裡。」牛頓自己，也是把兩年放在一起講。 |
| no-head-yet（t061） | 不管哪一年，這些人寫的，都沒有說它打到頭。 | 通過 | #24；上面三份草稿重抓都沒有 head | — |
| postures（t062） | 你有沒有發現？每傳一手，牛頓就換一個姿勢：坐著、散步。等一下，還有第三種。 | 通過（記一筆） | 坐著（STUK-NP「as he sat」）、散步（VOLT-1727「walking」）、躺著（EULER「couché」）都對。可是「每傳一手就換一個」不成立：康杜特只寫「musing」（沒寫姿勢），彭伯頓 1728「sat alone in a garden」、小冊子「as he sat under the Tree」又都是坐著。這是旁白的修辭，不算錯；要更準可以改 | （可選）你有沒有發現？傳著傳著，牛頓的姿勢也變了：坐著、散步。等一下，還有第三種。 |
| pemberton、pemberton-talk（t063–t064） | 還有一個人，替牛頓編過《原理》的第三版：彭伯頓。／他親自跟牛頓談過，這個理論是怎麼來的。…… | 通過 | PEMB 序（重抓）「upon my taking care of the late edition of Sir Isaac Newton's Principia」（「the late edition」即 1726 年第三版，「第三版」照 S25.md 來源表，沿用）；BREW1855 註 [18]（重抓）「Neither Pemberton nor Whiston, who received from Newton himself the History of his first Ideas of Gravity, records the story of the falling apple」 | — |
| pemb-garden、pemb-moon、pemb-none（t065–t067） | 一七二八年……序裡寫，牛頓一個人坐在花園裡，／想著重力：為什麼不能高到月亮那裡？他對自己說。／有花園，有月亮，就是沒有蘋果。…… | 通過 | PEMB 序（重抓 OCR）「As he sat alone in a garden, he fell into a speculation on the power of gravity … why not as high as the moon, said he to himself」；全書 apple 只有訂戶名「Appleby」。1728 年照 #18（書名頁 OCR 沒抓到年份，沿用） | — |
| pamphlet、first-ed（t069–t070） | ……它的第一版，一七三九年在倫敦出版，／從頭到尾，沒提過牛頓；作者是誰，到今天也不知道。 | 通過 | PHIL1739（重抓）「LONDON: Printed for T. COOPER at the Globe in Pater-Noster Row. MDCCXXXIX.」；全文 Newton、gravit、Orchard 都是 0 次。作者照 #25 | — |
| second-ed、head-quote（t071–t072） | 結果呢？一七四〇年前後印的第二版，多出了一段：／牛頓的引力學說，是他坐在樹下時，一顆蘋果掉到他頭上，給他的提示。 | 通過 | PHIL1740 p. 76（重抓 OCR）「And Sir Isaac Newton's famous Attraction and Gravitation, according to Pemberton, was suggested to him by an Apple which fell on his Head as he sat under the Tree」；「一七四〇年前後」照 #25 覆核（書名頁 MDCCXL…，沿用） | — |
| mathematician、orchard-fruit（t073–t074） | 作者還補一句：可是，他得是個數學家才行；／不然，整個果園的果子都砸在他身上，他也只會覺得，又重又硬。 | 通過 | 同上「but he must have been a Mathematician, to make the noble Use he did of it, otherwise all the Fruit in the Orchard might have struck him, without any other Advertisement than that of their Weight and Hardness」 | — |
| you-laugh（t075） | 這一句我是真的笑出來。你注意，蘋果在這裡，終於碰到頭了。 | 通過 | 旁白自己的反應；後半句同 t072 | — |
| according-to、pemb-callback（t076–t077） | ……書上寫：根據彭伯頓。／還記得剛剛彭伯頓那本書嗎？有花園，有月亮，就是沒有蘋果。 | 通過 | 「according to Pemberton」；「說是根據」不說「假託」（#25 覆核） | — |
| euler-writes（t079） | 還有一封信。一七六〇年九月，數學家歐拉寫信給一位德國公主，也講到了牛頓。 | 通過 | EULER 1768（重抓）書名「LETTRES A UNE PRINCESSE D'ALLEMAGNE」；1795 英譯信末「September, 1760」（重抓）；法文信末日期 OCR 壞了，沿用 #26「le 3 Septembre 1760」 | — |
| euler-lying、euler-quote（t080–t081） | 信裡說：這位英國的大哲學家、大數學家，有一天躺在花園裡的一棵蘋果樹下，／一顆蘋果，掉在他的頭上。…… | 通過 | EULER 1768（重抓 OCR）「Ce grand Philosophe & Mathématicien Anglois, se trouvant un jour couché dans un jardin, sous un pommier, une pomme lui tomba sur la tête」 | — |
| lying-this-time（t082） | 就是這個：躺著。坐著、散步、躺著，三種姿勢都齊了。 | 通過 | 同上「couché」 | — |
| moon-not-fall、moon-motion（t083–t084） | 歐拉接著寫：可是月亮，並沒有掉到他頭上；／於是他想到，讓月亮不掉下來的，可能是它的運動。 | 通過（沿用 verify-1） | #26 覆核 p. 209「comme la lune ne lui tomba point sur la tête, il comprit que le mouvement en pourroit être la cause」；這次 OCR 那一頁字形壞了，沒找到，未重開頁影像。「可能」保留了 pourroit | — |
| ignorance（t085） | 他還寫：要是蘋果沒有剛好掉在他頭上，我們說不定到現在還不懂。 | 通過 | EULER 1768 p. 212（重抓 OCR）「Si Newton ne s'étoit pas couché dans un jardin sous un pommier, & que par hazard une pomme ne lui fût pas tombée sur la tête, peut être nous nous trouverions dans la même ignorance」；「說不定」對 peut être | — |
| how-far、printed（t086–t087） | ……這些信一七六八年印成了書；／一七九五年的英譯本，也照樣寫蘋果掉在他頭上。 | 通過 | EULER 1795（重抓 OCR）「happening one day to be lying under an apple-tree, an apple fell upon his head」；1768、1795 兩個出版年照 #26（書名頁 OCR 沒抓到，沿用） | — |
| editor-note（t089，changes #10） | 巴黎版的編者加了一條註：比起蘋果，牛頓說自己「靠一直想」才想通，更像真的。 | 通過 | EULER 1795（重抓）註：「Newton was asked one day, How he had discovered the system of the universe? By continually thinking upon it, replied he. This anecdote has a greater air of probability than the story of the apple. — F. E.」；Hunter 前言（重抓）「The translated notes of the Paris Edition, I have … marked with the characters F. E.」。拿掉「十八世紀末」不影響事實 | — |
| nineteenth（t090） | 懷疑歸懷疑，到了十九世紀，打到頭已經是常見的講法。 | 通過（沿用 verify-1） | #27 COLE 1824、FONB 1829、1833、1836、1837 的 FTS 命中；不說「十九世紀才加的」 | — |
| critic-writes、eat-apple（t091–t092） | 一八二九年，有個時評家拿它開玩笑：／換個人，蘋果掉到頭上，大概會先把它吃掉，哪會想什麼重力。 | 通過（記一筆） | FONB pp. 223–224（重抓）「Had Newton been a man after the Reviewer's heart, when the apple fell on his head he would have asked, not "How is it?" but "What is it?" … and would probably have eat it, instead of digesting the doctrine of gravitation.」；目錄「Signs of the Times in 1829」。他挖苦的其實是那位評論者（換成評論者喜歡的那種人，牛頓就會把蘋果吃掉），「換個人」是簡化，claims 已註明，可以照用 | — |
| you-textbook（t093） | 你小時候課本裡的那顆蘋果，大概也是這個版本。 | 通過 | 有「大概」；#27 備註 | — |
| brewster-doubt（t094） | 故事還沒結束。偏偏就在這時候，有一個人，不敢寫這顆蘋果。 | 通過（記一筆） | BREW1831 p. 344 註（重抓）「I did not feel myself at liberty to use it」。不過同一頁正文其實提到了蘋果：「The celebrated apple tree, the fall of one of the apples of which **is said to** have turned the attention of Newton to the subject of gravity, was destroyed by wind about four years ago」；他是不把這件事寫進敘事（p. 148 正文只寫「sitting alone in the garden at Woolsthorpe」）。「不敢寫」比原文滿一點，章名「一部不敢寫蘋果的大傳記」同樣 | （可選）……有一個人，不敢把這顆蘋果寫進正文。 |
| brewster-1831（t095） | 一八三一年，第一部大部頭的牛頓傳出版了。 | 通過（記一筆） | 1831 年對（BREW1831 書名頁，重抓）。「第一部大部頭」只有 verify-1 #40 的備註（「第一部大型牛頓傳刻意把蘋果拿掉」），沒有原文引句撐，屬於強詞。說明欄也有同一句 | （可選）一八三一年，一部大部頭的牛頓傳出版了。 |
| brewster-note（t096） | 作者在註裡說：這個蘋果的故事，他找不到任何出處，不敢用。 | 通過 | BREW1831 p. 344 註（重抓）「The anecdote of the falling apple is mentioned neither by Dr Stukely nor by Mr Conduit, and, as I have not been able to find any authority for it whatever, I did not feel myself at liberty to use it.」 | — |
| brewster-later（t097） | 二十多年後，他改口，把蘋果放了回去；理由是：牛頓的外甥女跟伏爾泰講過。 | 通過（記一筆） | BREW1855 ch. II 正文（重抓）「it was therefore in the autumn of that year … that the apple is said to have fallen from the tree at Woolsthorpe」；註 [18]「It was mentioned, however, to Voltaire by Catherine Barton, Newton's niece, and to Mr. Green by Martin Folkes」。1831→1855＝24 年。原文的理由有兩個（外甥女→伏爾泰、福克斯→格林），旁白只講一個；NOTES 說不帶出福克斯是刻意的。不算錯 | — |
| tree-question、tree-when（t098–t099） | 紙上的蘋果傳開了，地上也有一棵樹。還記得牛頓老家花園裡那棵蘋果樹嗎？／它最早，是在什麼時候，被人當成了「那一棵」？ | 通過 | 回收 t013；問句 | — |
| visitors-1806、strangers（t100–t101） | 目前找得到最早的紀錄，是一八〇六年的一本地方志：那棵蘋果樹還在，／會帶外地人去看。這時，牛頓已經過世將近八十年了。 | 通過（二手） | KEES p. 381（重抓）「appears in the book Collections for the History of the Town and Soak of Grantham, by Edmund Turnor FRS (1754–1829) published in 1806. A footnote on page 160 states that: The apple tree is now remaining and is showed to strangers. This is 80 years after Newton's death.」。原書沒開，不加引號（#28）。1727→1806＝79 年 | — |
| sixty-years（t102） | 比印出打到頭的小冊子，又晚了六十多年。那這棵樹，是牛頓自己指認的嗎？ | 通過 | 算術：1740 前後→1806＝66 年 | — |
| only-tree、only-tree-b（t103–t104） | 沒有證據。研究這棵樹的學者認為，它會被選中，／只是因為牛頓家的花園裡，只有這一棵蘋果樹。 | 通過 | KEES（重抓）「There is no evidence to suggest that Newton identified a particular apple tree … The reason for this appears simply to have been that the apple tree was the only one in his garden」；掛在「學者認為」 | — |
| stuk-callback（t105，changes #10） | 還記得斯塔克利一七二一年的紀錄嗎？也沒提到這棵樹。那它後來怎麼了？ | 通過 | STUK-NP f. 10r–11r（重抓）沒有 apple；KEES「The tree does not appear in Stukeley's drawing either」 | — |
| letter-1912、storm-night（t106–t107） | 研究這棵樹的那位學者，引過一封一九一二年的信。／寫信的人說：他父親小時候，有一夜颳大風，第二天就聽說，牛頓的蘋果樹倒了。 | 通過（二手） | KEES（重抓）「from a Mr Walker, dated 12 January 1912」；「My father Richard Walker, was born … in 1807. He went to school, when he was 10 or 12 years of age … there was a very severe storm of wind one night, and that in the morning news came that Sir Isaac Newton's apple tree had blown down at Woolsthorpe」。不給年份（#30 DISPUTED） | — |
| re-rooted（t109） | 沒想到，倒下的樹幹又長出了根；今天，它還在莊園裡開花、結果。 | 通過 | YORK（重抓）「Some branches were removed but a large portion of the tree was left and re-rooted. Surprisingly, this tree is still growing at Woolsthorpe Manor today」；NT（重抓）「it continues to grow and bear blossom and fruit」 | — |
| you-visit（t110） | 你要是去看，會看到一棵從倒下的樹幹長起來的老樹，四周圍著矮欄杆。 | 通過 | NT（重抓）「A low barrier has been installed around it to protect the roots」；「從倒下的樹幹長起來」照 YORK；「同一棵」是學者推論（#31），這句沒說 | — |
| two-folders（t113，changes #10） | 紀錄沒辦法結案，學者自己也分兩邊：有人把它降成一則沒有佐證的軼事； | 通過 | KEES（重抓）「Whiteside [10] claims that as Newton's original calculation from 1665/6 has not come to light the account which Newton gave `must be demoted to mere unsupported anecdote'」；不點名（#23） | — |
| soul-risk（t114） | 研究那棵樹的學者則說，牛頓不至於為了這麼小的事，拿自己的靈魂去冒險。 | 通過（記一筆） | KEES（重抓）「it seems unlikely to me that a man who was acknowledged to be the greatest mathematician and scientist of his age, and who stood in the deepest awe of the judgement of God would put his immortal soul in jeopardy by fabricating such an unnecessary falsehood」。原文冒的險是「捏造一個沒必要的謊」，旁白的「為了這麼小的事」把「捏造」吞掉了，聽的人要自己補；而且原文是「it seems unlikely to me」（他個人的看法），旁白有「學者則說」框住，可以 | （可選）研究那棵樹的學者則認為，牛頓不至於為了編一個沒必要的謊，拿自己的靈魂去冒險。 |
| legend-self（t115） | 也有歷史學家認為，講起六十年前的事，晚年的牛頓可能在替自己塑造傳奇。 | 通過 | HAYCOCK（重抓）「Newton -- an old and famous man by that stage -- may well have been indulging in some self-fashioning of his own myth」；1666→1726＝60 年；「可能」對 may well；不掛 Westfall | — |
| answer（t116，changes #8） | 結果，打到頭這一題反而可以結案：蘋果有紀錄，打到頭，是後來加的。 | 通過（記一筆） | 支撐的是 #3、#24、#25、#42：聽過的人沒有一個寫打到頭，目前找得到最早的打到頭是 1740 年前後的第二版，1739 年第一版沒有。「是後來加的」是根據目前找得到的紀錄下的結論，片子前面一再說「目前找得到最早」（t005、t068），整體不會誤導；「反而」是 changes #8 為了承接加的，沒有改事實 | — |
| close-you（t117，changes #7） | 下次再聽到蘋果砸頭，你可以想起樹下那杯茶：牛頓說的，只是掉了下來。 | 通過（記一筆） | 同標題：「牛頓說的」是斯塔克利 1752 年記下的轉述（#3）。片尾收束，前面已講清楚，可以照用 | — |
| close-line（t118，changes #7） | 故事每傳一手，就多一點細節；越生動的那一下，越要問：這是誰加的？ | 通過（記一筆） | changes.md 說這句是價值觀、不帶新事實，但它說成了普遍事實，沒有標成意見。而且片子自己就有反例：外甥女那一版只剩「果子」、彭伯頓沒有蘋果，細節是變少的。站主規則：意見要標成意見 | （可選）我自己的心得是：故事每傳一手，常常就多一點細節；越生動的那一下，越要問：這是誰加的？ |
| youtube.title | 牛頓被蘋果砸到頭？1726 年他親口說的，只有掉下來｜奇聞檔案局 | 通過（記一筆） | 見開頭結論摘要：說的人牛頓，聽的人與記下的人斯塔克利，1726-04-15 說，1752 年寫成，1936 年出版，當天日記沒有蘋果。「親口」照「he told me」成立，「只有掉下來」照 f. 15r 成立（沒有 head） | 可以照用（條件：說明欄照下一列改） |
| youtube.description | 「……牛頓親口說的是「一顆蘋果掉了下來」；他一七五二年寫成的回憶錄手稿（一九三六年才出版）沒有地點、沒有年份，也沒有打到頭。」 | 要改 | 「他」最近的先行詞是牛頓，讀起來像牛頓 1752 年寫了回憶錄（牛頓死於 1727 年，STUK-NP f. 77r）。寫的人是斯塔克利（STUK-NP 書名頁「William Stukeley 1752」）。另外引號裡的「一顆蘋果掉了下來」不是牛頓的原話，是斯塔克利的轉述（「occasion'd by the fall of an apple」），建議拿掉引號 | ……牛頓說，他當年想到重力，就是因為一顆蘋果掉了下來；斯塔克利一七五二年寫成的回憶錄手稿（一九三六年才出版）沒有地點、沒有年份，也沒有打到頭。 |
| youtube.description（其餘） | （全文） | 通過（記一筆） | 逐句對過：1726-04-15、肯辛頓、八十三歲（#1、#21）；伏爾泰 1727、康杜特的年份 1665／1666（重抓）；牛頓晚年筆記 1666 與月亮、沒有蘋果（NATP00385 重抓）；小冊子 1740 前後第二版、1739 第一版沒有、說是根據彭伯頓、彭伯頓 1728 只有花園和月亮（重抓）；歐拉 1760；Brewster 1831 找不到出處；1806 年帶外地人去看（KEES）；大約兩百年前被風吹倒、樹幹重新生根、今天開花結果（YORK、NT）；界線段（外甥女 1741、目前找得到最早、日記與 1912 的信是轉引、不給年份、沒有證據是牛頓指認）都對。插圖那句跟提示詞一致。記一筆：「一八三一年第一部大部頭的牛頓傳」同 t095；「這個畫面講了快三百年」從 1740 前後算是 286 年，可以 | 只改上一列那一句 |

**其餘全部通過**（逐句看過，都是問句、轉場、點名的回呼、「你」的旁白、Ada 的自我介紹或畫面說明，沒有暗含新事實）：t009、t020、t038、t044、t049、t054、t068、t078、t088、t099、t111、t112、t119、t120。

## changes.md 逐條

- **【待查】清單「無」**：同意。新稿每一句都能對回 verify-1 的列或備註，沒有用到查核表以外的事實。
- **新寫進旁白的 9 句**：t003 通過（記一筆，「沒有一個」指留下紀錄的人）；t008、t010、t012、t013、t025、t026、t043 通過；**t021 要改**（「說出這件事的人」是牛頓不是斯塔克利；「要等到」要改成「目前找得到最早」）。
- **第 10 點〈合併或改寫（意思不變）〉**：
  - nw510＋nw511 → t089：通過，拿掉「十八世紀末」不影響事實（F. E.＝巴黎版編者，重抓 Hunter 前言）。
  - nw315＋nw314＋nw319 → t060：通過（記一筆），「兩年都認」容易被聽成牛頓替蘋果給了年份，見判定表。
  - nw605＋nw606 → t105：通過。
  - nw612 → t112＋t113：通過。
  - nw616 → t120：通過。
- **第 5 點（斯塔克利 1721 年移到步 4）**：t022–t023 通過；**t024 要改**：原 nw606 跟 verify-1 #39 備註一樣沒有「可能」，但 KEES 原文是「may not have been aware」，這次重抓才對到，旁白要補回。
- **第 7 點（t117、t118 新的收尾）**：t117 通過（記一筆）；t118 記一筆，要標成意見。
- **第 8 點（鉤子改寫）**：stuk-notree（t023）、who-told（t049）、stuk-callback（t105）、outro-q（t119）、answer（t116「結果，……反而」）、re-rooted（t109「沒想到」）、open-half（t112）都只動了語序或承接字，事實沒變，通過。
- **第 9 點（刪掉的原句）**：逐條看過，刪掉的都不是保留「可能」「據說」的地方，沒有把但書刪掉。nw209 刪掉後 t052 句尾的冒號懸空（文字問題，見判定表）。
- **「要站主決定的事」第 1 點（人名念法）**：不屬於查核，略。

## 畫面與規則（只影響畫面，記一筆）

- 在世或 1956 年後過世的人：提示詞裡**沒有**任何真人。歷史人物都用物件代表（三角帽＝牛頓、醫生提包＝斯塔克利、羽毛筆＝伏爾泰、鑰匙＝外甥女、厚書＝彭伯頓與 Brewster），動作景只畫手。研究者 Keesing（在不在世查不到）、Whiteside、Haycock 都沒有入畫，diary-who 是 Ada 拿日記。
- 一般人物景（沙發上的「你」7 景、strangers 從背後畫的兩位旅人、schoolboy-branch 的小男孩、you-visit 從背後畫的訪客）都是無名的一般人，沒有對應到真人。
- schoolboy-branch 畫的是男孩扛著一段樹枝：信裡是老師鋸下好幾段木頭、寫信人的父親拿到其中一段，「扛樹枝」可以；如果 t108 照改成「幾個學生」，畫面不用動。
- you-visit 畫「small red fruit」：NT 說那棵樹的果子是「green with a red flush」（verify-1 #35），想對齊可以改成「small green apples with a red blush」。其他景的「yellow-red apple」只是象徵，不用動。
- Ada 的 `characters[0].appearance`（short loose black bob）跟提示詞（wavy black bob with a side fringe）不一致，changes.md 第 6 點已經提了，跟事實無關。
- 章名順手看了：「兩份草稿，兩個年份，一本沒有蘋果的書」，康杜特的草稿其實是三份（兩份寫 1665、一份寫 1666），旁白自己說「好幾份」。不算錯（說的是兩種寫法），要更準可以改成「三份草稿，兩個年份……」。「一八〇六年，那棵樹被指了出來」是「目前找得到最早」的簡寫（KEES 也推論十八世紀後期就已經被當成那一棵），章名可以照用。

## 要改的句子清單

- stuk-intro（t021）｜要等到牛頓八十三歲。說出這件事的人，是一位醫生，叫斯塔克利。｜目前找得到最早的一次，是牛頓八十三歲那年，講給一位醫生聽的。這位醫生，叫斯塔克利。
- stuk-notyet（t024）｜先別急著下結論：因為那一年，他還沒聽過蘋果的故事。｜先別急著下結論：研究這棵樹的學者猜，可能是那一年，他還沒聽過蘋果的故事。
- diary-who（t030）｜這本日記，是一位研究牛頓蘋果樹的學者翻出來的。那蘋果去了哪裡？｜這段日記，是一位研究牛頓蘋果樹的學者，在論文裡引出來的。那蘋果去了哪裡？
- schoolboy-branch（t108）｜老師還帶著全班同學，去鋸了幾段樹枝。｜老師帶著幾個學生趕了過去，還從樹枝上鋸下好幾段木頭。
- `youtube.description`｜牛頓親口說的是「一顆蘋果掉了下來」；他一七五二年寫成的回憶錄手稿……｜牛頓說，他當年想到重力，就是因為一顆蘋果掉了下來；斯塔克利一七五二年寫成的回憶錄手稿……

旁白以外的事（本輪沒有改）：

- `claims.md` 的行號還是舊的 nw001–nw623，跟這次的 t001–t120 對不上。如果 `tools/video/qa/facts.mjs` 照 id 對，要重排；t024（nw606）、t030（nw115 前後）、t108（nw622）的依據也要照上面更新，並在 nw622 那列拿掉「全班」。
- `NOTES.md` 第二版加長那一條寫「1912 年那封信裡一夜大風與全班去鋸樹枝 #30」，「全班」也要改。
- `verify-1.md` 第 39 列備註「1721 年他還沒聽過蘋果故事（1726 年才聽到）」少了 KEES 的「may」，下一次重抄 verify 表時可以補上。
- `loops` 裡如果有把 t021、t024、t030 當 setup 或 payoff 的，文字要跟著改句。

## 開場補一句的建議

lint 說開場章（t001–t006）約 37 秒，系列規定 40–90 秒。下面兩句都只用 claims.md／verify-1.md 已經查證的事實，加一句大約多 7–9 秒，就會超過 40 秒。兩句都放在 t005（小冊子）之後、t006（承諾句）之前，都會在正文裡回收，可以登記成新的 loop。

1. **建議先加這句**（放在 t005 後面）：
   > 還有，那份最接近牛頓親口說法的紀錄，寫好以後，整整一百八十四年，都沒有印出來。

   依據：verify-1 第 3 列備註（「最接近牛頓親口說的版本，但仍是斯塔克利的轉述」）、第 6 列（書名頁「Wm Stukeley 1752」）、第 7 列（HAYCOCK「published in 1936」，這次重抓過）；1936−1752＝184。原片 nw002 就用過這個數字（claims.md nw002、nw119）。
   回收在 t042–t043（「手稿一七五二年寫成，一九三六年才印成書……中間隔了一百八十四年」），t037 也會先接到「最接近牛頓親口說法」。這句不講是誰寫的、寫了什麼，鉤子留到第 2 章才揭曉。
   畫面可以沿用 years-184 的寫法（積灰的素灰盒裡一疊闔上的手稿，不畫數字），換一個光線就不會跟 t043 重複。

2. **想再長一點可以接這句**（接在上一句後面）：
   > 就連牛頓老家那棵「蘋果樹」，也要等到他過世將近八十年，才第一次被寫進書裡。

   依據：verify-1 第 28 列（Turnor 1806 年地方志 p. 160 註，KEES、YORK 轉引；KEES 原文「This is 80 years after Newton's death」，這次重抓過）、第 34 列（牛頓死於 1727 年）。回收在 t100–t101。
   注意「第一次被寫進書裡」是強詞，照第 28 列只能說「目前找得到最早」；若要完全照規矩，改成：「就連牛頓老家那棵『蘋果樹』，目前找得到最早的紀錄，也是他過世將近八十年以後。」（較長，約 9 秒）。
   這句會提前用掉 t013「這棵樹先記著」的懸念，所以排第二順位。
