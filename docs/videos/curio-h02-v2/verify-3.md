# curio-h02-v2 查核第三輪：開場預告改寫（2026-10-13）

## 範圍

- 只查 `git diff HEAD -- docs/videos/curio-h02-v2/`：`video.json` 第一章改成「一個場景＋轉一句＋四個預告＋問題」，
  正文六句改寫（`ro223`、`ro402`、`ro409`、`ro516`、`ro602`、`ro613`），`loops`、`claims.md` 場景欄、
  `NOTES.md`〈開場預告 2026-10-13〉。`youtube`、`thumbnail`、`sources` 沒有動。
- 判準：新句或改過的句子裡每一個事實（誰、什麼、哪裡、何時、數字、名字、「當時說是金的」這類限定）
  都要已經由查過的正文句、`claims.md` 或 verify-1／verify-2 標為找到的來源支持；「開頭那…」要指得到開場真的講過的東西。
- 外部查證只做一次：重開勞森原文（https://www.gutenberg.org/cache/epub/1838/pg1838.txt ，200），
  User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。二〇二六年六月四日那則宣布的日期
  verify-1、verify-2 都從頁面 metadata 確認過（`article:published_time` 2026-06-04T18:48Z），這一輪沒有重開。

## 逐句

| id | 句子 | 依據 | 結果 |
|---|---|---|---|
| `ro102` | 一個畫地圖的人，回到羅阿諾克島。 | c1（一五九〇年八月十八日懷特一行上岸）、c8；verify-1 #15「artist John White」、1585 年的地圖 | OK |
| `ro103` | 三年前，他把人留在這裡。 | 舊 `ro103` 的事實（verify-1 #15，1587-08-27→1590-08-18）；「他」＝上一句畫地圖的人 | OK |
| `ro104` | 靠岸之前，他們吹了號，沒有人回應。 | c3（吹號、唱歌、無人回應、天亮才上岸）；只是把舊 `ro104`＋`ro105` 合併、拿掉唱歌 | OK |
| `ro109` | 柵欄的木樁上，刻著一個字。 | c4（入口的木樁、高大的柵欄「high palisado」）；`the-word` 卡片原本就寫「柵欄的木樁上」 | OK |
| `ro112` | 他後來寫，看到這個字反而很高興。 | c5，單一目擊來源的「他後來寫」歸屬保留 | OK |
| `ro114` | 但這還不是最怪的。 | 轉場，不含事實 | OK |
| `ro115` | 一七〇九年，哈特拉斯人跟一個旅行的人說起祖先。 | c26、`ro402`、`ro403` | **問題**，見下 |
| `ro116` | 二〇一七年，一只當時說是金的戒指，送去化驗。 | c34（二〇一七年驗出全是黃銅）、`ro502`「當時說是金的」、`ro516`；限定詞保留 | OK |
| `ro117` | 二〇一二年，他那張地圖上的補丁底下，有什麼？ | c40（懷特地圖上的補丁、二〇一二年在大英博物館） | **問題**，見下 |
| `ro118` | 二〇二六年六月，一個基金會宣布了一件事。 | c42（First Colony Foundation 2026-06-04 在自己的網頁宣布）；月份與「基金會」都對；不講宣布內容，所以不必帶 `ro613`／`ro614` 的保留 | OK |
| `ro113` | 那個字，到底把他留下的人帶去了哪裡？ | 問句；前提「刻的是搬去的地名」是 c15 的約定。「他留下的人」呼應 `ro103`「他把人留在這裡」，讀得出是畫地圖的人 | OK |
| `ro223` | 木樁上那個字的上面，沒有十字。 | c4（「without any crosse or signe of distresse」）；舊 `ro111` 挪過來 | OK |
| `ro402` | 一七〇九年，開頭那個旅行的人把它寫了下來。 | c26（一七〇九年出版）；開場 `ro115` 確實講了「一個旅行的人」（照下面的建議改了也還在） | OK |
| `ro409` | 懷特那天還看到，一棵樹上刻著三個大寫字母。 | c4；Hakluyt：同一天上岸後「upon a tree… C R O」；仍是「一棵樹上」，不說樹皮；「還」不暗示先後 | OK |
| `ro516` | 二〇一七年，開頭那只戒指送去化驗。 | c34；開場 `ro116` 講了戒指 | OK |
| `ro602` | 地圖上貼著的，就是開頭那塊補丁。 | c40；開場 `ro117` 講了補丁 | OK |
| `ro613` | 開頭那則宣布，沒有附新的發掘報告。 | c42；開場 `ro118` 講了宣布 | OK |

### 問題一：`ro115` 把「說」的年份寫成一七〇九年

一七〇九年是勞森那本書在倫敦出版的年份（Gutenberg 檔內「This book was originally published in London in 1709」），
不是哈特拉斯人跟他說話的年份。原文是「A farther Confirmation of this we have from the Hatteras Indians… These tell us,
that several of their Ancestors were white People」，整段沒有日期；勞森的旅程從「December the 28th, 1700」開始，
書是事後寫成的。正文 `ro402` 說的是一七〇九年「寫了下來」，c26 也是「一七〇九年勞森記下」，都把年份掛在寫的那一端；
預告把它挪到「說起祖先」上，是紀錄沒有給的年份。

建議改成（仍停在結果之前，不講祖先是誰，`ro402` 的「開頭那個旅行的人」照樣指得到）：

> 一七〇九年，一個旅行的人寫下了哈特拉斯人說起的祖先。

### 問題二：`ro117` 的「他」會指到旅行的人

`ro117` 前面最近的單數人物是 `ro115` 的「一個旅行的人」（`ro116` 沒有人），所以「他那張地圖」最自然的讀法是旅行的人的地圖，
不是 `ro102` 那個畫地圖的人。勞森的書本身也附了一張卡羅來納地圖，這個誤讀不是空想。要指的是懷特的地圖（c40、`ro601`）。

建議改成：

> 二〇一二年，畫地圖的人那張地圖上，補丁底下有什麼？

## 拿掉的開場句子（`ro105`–`ro108`、`ro111`）

- `ro105`（沒有人回應）併進 `ro104`，沒有丟。
- `ro106`（聚落裡只剩他們留下的東西，c2）旁白不再唸。還依賴它的只有 `ro213`「他踏上空島的那一天」的「空島」，
  而 `ro104`（沒有人回應）加上 c2 本身仍支持它，不算懸空。但 `claims.md` c2 的場景欄現在只寫 `trumpet-ashore`，
  那一句並沒有講 c2 的內容；建議 c2 場景欄改成 `trumpet-ashore, third-birthday`，並註明「旁白不再唸殘留物，`ro213` 的『空島』靠它」。
- `ro107`（樹上三個大寫字母）挪到 `ro409`；`ro410`「可是傳到後來，變成樹上刻著一個字」仍接得上。
- `ro108`（木樁被剝了皮）旁白不再唸；沒有任何剩下的句子依賴「剝了皮」。說明欄第一段與 `five-feet` 的畫面仍有，c4 支持。
- `ro111`（沒有十字）挪到 `ro223`；`ro224`「沒有十字就是平安」接得上。
- 標題「CROATOAN 到底是什麼意思？」：`ro110` 仍唸出這個字，不依賴拿掉的句子。縮圖「他反而高興」：`ro112` 仍在。
  說明欄第一段（小船、唱歌、剝了皮、離地五英尺、沒有十字）都是 c1／c3／c4 支持的事實，本來就不是逐字照旁白，可以留著。

## 範圍外但會壞的東西（不是事實問題）

- `shorts.json`（未追蹤檔）是照舊開場做的：short-1 用了已刪掉的場景 `boat-lowered`、`no-answer`、`no-cross`，
  旁白引的是舊 `ro102`、`ro105`、`ro109`、`ro111`、`ro112`、`ro113`；short-2 引舊 `ro516`「二〇一七年，那只戒指送去化驗。」
  如果短片是從正片剪的，這幾段已經找不到。需要照新版重做或把那些場景另外保留。
- `claims.md` c5 的場景欄仍列 `the-question`，但 `ro113` 已不再問「為什麼高興」；改掛 c15（約好刻地名）比較準。
- `voice.performance` 還寫「像跟著小船靠上那座島」與「『還記得』開頭的句子」，開場已不唸小船，「還記得」只剩兩句；不影響事實。

## 結論

17 句新句或改過的句子：15 句 OK，2 句要改（`ro115` 年份、`ro117` 代名詞），改完不需要第四輪。
沒有發現誇大、被當成事實的轉述或掉了的保留：「當時說是金的」「他後來寫」都留著，`ro118` 沒講宣布內容所以不必帶保留。

## 第二輪修改查核 2026-10-13

### 範圍與做法

- 查 `NOTES.md`〈盲評修正 2026-10-13〉與〈盲評修正第二輪 2026-10-13〉列的改句，加上 `git diff HEAD -- video.json`
  的第 5、6 章場景重排、兩個章名、`loops`。只看旁白與章名的事實；`prompt`、`camera`、`emotion` 不在範圍內。
- 依據：`claims.md` c13、c26、c32、c34、c36–c42，verify-1 #41、#91、#103–#107、#112–#121，verify-2 第 4 節與 #7、#20。
- 這一輪重開三個網址（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，三個不同主機）：
  Coastal Review 2020（200）、National Geographic 2015（200）、First Colony Foundation 2026 宣布頁（200）。

### 逐句

| id | 現在的句子 | 依據 | 結果 |
|---|---|---|---|
| `ro115` | 一七〇九年，一個旅行的人寫下了哈特拉斯人說起的祖先。 | 照本檔問題一的建議逐字改了；年份掛在「寫下」（c26） | OK |
| `ro117` | 二〇一二年，畫地圖的人那張地圖上，補丁底下有什麼？ | 照本檔問題二的建議逐字改了；指懷特的地圖（c40） | OK |
| `ro116` | 二〇一七年，哈特拉斯島挖到的一只戒指，被送去化驗。 | NG 2015「In 1998, archaeologists from East Carolina University found a ten-carat gold signet ring here」（here＝哈特拉斯島的 Cape Creek，同頁圖說「excavated from the Cape Creek site on Hatteras Island」）；SM17（2017-04-07）「recently subjected the ring to a lab test」。拿掉「當時說是金的」沒有丟掉保留——預告不再說金，`ro502` 第一次講時帶著限定 | OK（「二〇一七年」是報導年份，與 verify-2〈建議〉3 同一個已知的殘留，`ro516` 也一樣） |
| `ro214` | 沒想到四天後，全體殖民者找上他。 | c13；Hakluyt「the 22 of August, the whole company…came to the Gouernour」（8/18＋4，verify-1 #41）。「沒想到」不帶事實 | OK |
| `ro524` | 而另一支團隊，是從一張地圖開始的。 | 回到 verify-1 #112 查過的原句；NG 2015「a 1585 watercolor map drawn by White prompted the First Colony Foundation to turn its attention to the mainland」 | OK |
| `ro601` | 二〇一二年，有人在大英博物館攤開懷特那張地圖。 | 回到原句；FCF「in 2012, we asked a First Colony board member to determine if the British Museum knew…」，NG「made headlines in 2012」 | OK |
| `ro513` | 二〇一五年春天，哈特拉斯島那邊挖到一截鐵劍柄。 | NG 2015（今天重開）「Part of an iron rapier handle was unearthed in the spring of 2015 at the Cape Creek site on Hatteras Island」；同頁「Mark Horton…who heads the excavation on Hatteras」。是哈特拉斯島那支（Croatoan Archaeological Society／Horton），不是內陸 | OK |
| `ro514` | 二〇二五年初，哈特拉斯島又挖到成桶的鍛鐵碎屑。 | WHRO（2025-01-20）「Archaeologists recently found "buckets" of hammer scale on Hatteras Island」（c38、verify-1 #105、verify-2 #7）。地點對；「年初」是 verify-1 給的寫法，殘留同 verify-2〈建議〉3。「又」接 `ro501`／`ro513` 的哈特拉斯島，讀得通 | OK |
| `ro608` | 二〇二〇年，內陸那支團隊自己的考古學家說過一句話。 | Coastal Review 2020-10-16（今天重開）：說話的是「principal investigator and Foundation Research Vice President Nicholas Luccketti」，談的是 First Colony Foundation 在伯蒂郡的 Site Y（「the 2019-2020 archaeological survey…known as Site Y」）。是內陸那支 | OK |
| `ro611` | 沒想到二〇二六年六月，內陸那支團隊的基金會改口了。 | FCF 宣布頁（今天重開；`article:published_time` 2026-06-04，verify-1／2 已確認）：作者是「the First Colony Foundation」，也就是 Site X／Site Y 的發掘者，`ro608` 那位考古學家所屬的基金會。「改口」公平：2020 年 Luccketti 說 Site Y「is not the major relocation site…but again, a satellite site」，報導也寫兩處都只是「a small group of Roanoke colonists for a short period」；2026 年同一個基金會寫「This is not another hoax or false claim」「Site X and Site Y were part of a larger, dispersed settlement of farms along the Chowan River, where 117 immigrants established their New World home」——從「小群人的衛星點」改成「全部一百一十七人的家找到了」。`ro612`–`ro614` 照舊標明是基金會自己網頁上的宣稱、沒有報告、沒有第三方評估 | OK |

### 新的年份順序

| 年份 | 句子 | 依據 | 結果 |
|---|---|---|---|
| 1998 | `ro501`–`ro502` 戒指；`ro503`–`ro508` 年輪 | c34（NG：1998 ECU 在 Cape Creek）；c32（Science 1998 的樹輪研究，「同一年」對） | OK |
| 2009 | `ro511`–`ro512` 考古團體、英國大學 | c36（NG「founded the Croatoan Archaeological Society…in 2009 and have sponsored Horton's annual digs ever since」） | OK |
| 2012 | `ro601`–`ro606` 補丁、堡壘記號、五十英里、伯蒂郡 | c40 | OK |
| 2015 | `ro513` 劍柄 | c37 | OK |
| 2017 | `ro516`–`ro522` 化驗與定年 | c34、c35、c39（`ro518`–`ro522` 本身不帶年份，是對同一遺址的說明） | OK |
| 2020 | `ro608`–`ro610` | c42；Coastal Review 2020-10-16、SM20 2020-11-09（「同一年」對） | OK |
| 2025 | `ro514`–`ro515`、`ro523` | c38 | OK |
| 2026 | `ro611`–`ro614` | c42 | OK |

**一處不是錯、但與「照年份」的說法擦邊：`ro607`**「這裡開了兩個工地，挖到歐洲人用的器物。」現在排在 2012 之後、
2015 之前，聽起來兩個工地都是二〇一五年以前就挖出東西了。今天重開的來源：Site X 在 NG 2015（2015-08）已經在挖
（「found on a recent weekend excavation at what the First Colony Foundation calls Site X」），但 Site Y 是
「the 2019-2020 archaeological survey」（Coastal Review 2020），FCF 2026 也寫 Site Y 是後來「Upstream, our continued
search located the larger Site Y」。句子沒有寫年份，所以不算事實錯誤；如果要讓它和年份順序一致，建議改成：

> 後來這裡陸續開了兩個工地，挖到歐洲人用的器物。

（`ro608`–`ro609` 的「其中一個工地」照樣接得上；`two-sites` 卡不必動。）

### 章名與 loops

- 第 5 章「一只戒指出土，地圖補丁底下有一個堡壘」：戒指 1998 出土（c34）、補丁底下的堡壘記號（c40）；章名不再用「島上」，
  verify-2〈還要改的地方〉4 那個「島」指兩座島的問題也一併消失。OK。
- 第 6 章「戒指驗出是黃銅，基金會卻宣布找到了」：c34「It's all brass」、c42 基金會自己宣布。OK。
- `loops`：`ro115`→`ro403`、`ro116`→`ro517`、`ro117`→`ro603`、`ro118`→`ro612`，setup 都在 payoff 之前，`what` 欄與句子一致。OK。

### 範圍外（不是旁白的事實問題）

- `NOTES.md` 第 19 行附近的章節表還是舊章名（第 6 章「地圖的補丁底下，有一個堡壘的記號」）與舊的時間碼。
- `ro214` 的「四天後」是從 `ro211` 的一五八七年八月十八日算，中間隔了 `ro212`–`ro213` 講一五九〇年的同一天；
  `ro215` 馬上講「要他回英格蘭」，讀得出是一五八七年。這是原句就有的，verify-1／2 都判 CONFIRMED，這一輪沒改它的事實。

### 結論

這一輪改過或挪動的旁白 10 句全部 OK（`ro115`、`ro117`、`ro116`、`ro214`、`ro524`、`ro601`、`ro513`、`ro514`、`ro608`、`ro611`），
年份順序八個年份都對，兩個章名與 loops OK。唯一建議（非必改）是 `ro607` 加「後來…陸續」，讓 2019–2020 才挖的
Site Y 不被讀成 2015 年以前。沒有需要第四輪的事實錯誤。
