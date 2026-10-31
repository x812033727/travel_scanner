# S37 獨立查核（第二版旁白）

查核日：2026-10-31。查核者不是撰稿者；只讀，沒有改 `video.json`。本集資料夾原本沒有 `verify-1.md`，舊稿從分支 `origin/codex/curio-s34-endurance-20261019` 取出比對；檔名照交辦用 `verify-2`。

## 結論：有條件通過

主幹守得住：`舅舅`、`外甥` 是對的（拉丁 avunculus、英譯 your brother、LRB、USNA 全都一致），舊稿的「叔父」確實是錯的；信中沒有龐貝這個地名、死因標成猜測、火光掛在安慰話底下、不講月日，這些界線也都沒破。

但有 **2 個錯誤、4 個過強、11 個措辭與文件問題**。第 1–6 列修完才能進 `tts`；第 7–17 列建議一併處理。片尾 pn128 講「這個頻道只講紀錄裡找得到的」，所以第 3 列（片尾答案）尤其不能留。

這次通讀兩封信的拉丁文，發現撰稿時只對了幾個字的代價：英譯 Melmoth 有好幾處比拉丁文多加東西，旁白跟著加了（第 5、7、8、10、12 列）。

## 查了哪些

- `video.json` 全部 128 句旁白、3 張字卡、片尾卡、8 個章名、標題、縮圖 `headline`/`tag`/`sub`、`youtube.description`，逐句對 `research.md` 與原文。
- 與舊稿比對：舊稿 91 句，新稿 128 句，只有 2 句和舊稿相近（相似度 0.75 以上），所以整集當新句查。新稿 `video.json` 與 `script.md` 無「叔父」「侄」殘留。
- 開原文核對的列：`L65a`、`L65b`、`L65c`、`L66a`、`L66b`、`L66c`、`L66d`、`EDIT`、`N1`–`N9`，共 17 列。
- `claims.md`：腳本比對，112 列的旁白節錄與 `video.json` 全部一致；表內 112 列加表頭豁免 16 句，正好 128 句，沒有漏句；豁免的句子確實不帶新事實。原文欄英文引句切成 138 段，132 段逐字在固定版內，其餘 6 段的原因見下方（3 段來自 USNA、維基、LRB，都已在該來源找到；`pn027` 只差註腳記號 `[94]`；`pn125` 同屬 LRB；`pn054` 見第 17 列）。
- 查核表「不入旁白」與界線：「唯一留存的目擊記述」沒有用到；「幸運眷顧勇者」掛「大意是」；月日沒進旁白；畫面提示詞沒有小普林尼登船、沒有可辨遺體、沒有龐貝街景。

撰稿者自己標為「最可能被挑」的三句都**通過**：

- pn010「應該算」：已標推斷，引文撐得住。
- pn056「塔西佗果然追問了」：比撰稿者以為的更穩。拉丁第二封信開頭就是「Ais te … cupere cognoscere」（你說你想知道），不只是英譯的 it seems。可以把這幾個字補進 `N9`。
- pn123「只提到兩個僕人」：拉丁「alios in fugam vertunt」「servolis duobus」，相符。

## 開了哪些來源

| 來源 | 怎麼開 | 用途 |
| --- | --- | --- |
| [GITenberg 固定英譯 2811.txt](https://github.com/GITenberg/Letters-of-Pliny_2811/blob/959ded9fab0f9d54768d2dbfad860b79c864c4c8/2811.txt#L3500-L3732) | raw.githubusercontent.com 下載，SHA-256 `9f5fd6bc…` 與 `research.md` 相符 | 兩封信全文通讀；L3500–3732 搜 `pompei` 零筆 |
| [The Latin Library 第六卷](https://www.thelatinlibrary.com/pliny.ep6.html) | 下載，通讀 6.16、6.20；全卷搜 `pompei` 零筆 | 對英譯；`N1`、`N2`、`N3`、`N8` |
| [USNA Nimitz Library](https://usna.edu/Library/sca/blog/posts/vesuvius_i.php) | 下載 | `N2`、`N4`、`N5` 引文都在 |
| [LRB, Thomas Jones](https://www.lrb.co.uk/the-paper/v42/n18/thomas-jones/sheets-of-fire-and-leaping-flames) | 下載 | `N1`、`N2`、`N6`、`N7` 引文都在 |
| [維基：79 年爆發](https://en.wikipedia.org/wiki/Eruption_of_Mount_Vesuvius_in_79_AD) | 下載 | `N4`、`N7`；月日爭議確實存在 |
| [維基：Pliny the Elder](https://en.wikipedia.org/wiki/Pliny_the_Elder)、[Pliny the Younger](https://en.wikipedia.org/wiki/Pliny_the_Younger) | 下載 | 妹妹 Plinia；年齡「17 or 18」 |
| [維基：Stabiae](https://en.wikipedia.org/wiki/Stabiae)、[CyArk：Ancient Stabiae](https://cyark.org/projects/ancient-stabiae/in-depth) | 下載、WebFetch（查核表沒有，我另外找的） | 斯塔比亞與龐貝的距離 |

## 問題

| # | 行 id | 旁白原文 | 問題 | 依據 | 建議改法 | 嚴重度 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | pn058 | 舅舅那晚也是洗澡吃飯，可是他睡得又短又不安穩。 | 「他」緊接「舅舅」，聽起來是舅舅睡不好。這跟 pn036 和原文相反：舅舅睡得很熟，睡不好的是外甥。 | 英譯 L3580「fall into a sound sleep」對 L3636–3637「a short and uneasy sleep」；拉丁「verissimo quidem somno」對「somnus inquietus et brevis」 | 「舅舅那晚也是洗澡吃飯。不一樣的是，舅舅睡得很熟，外甥睡得又短又不安穩。」 | 錯誤 |
| 2 | pn125（`N6`、`sources` 的 LRB 標題） | 舅舅倒下的斯塔比亞，在龐貝南邊四英里 | LRB 一篇書評確實這樣寫，但其他來源是約 4–4.5 公里，也就是不到三英里；方位也是西南。四英里約 6.4 公里，多了四成。數字只靠單一來源，沒有對過第二個。 | 維基 Stabiae「approximately 4.5 km (2.79 miles) southwest of Pompeii」；CyArk「only 4 km from Pompeii」 | 「舅舅倒下的斯塔比亞，離龐貝只有幾公里；外甥人在海灣對岸。」`N6` 與 `sources` 同步改，並補這兩個來源 | 錯誤 |
| 3 | pn126、片尾卡 `pl099.sub` | 船上那些，他說是事後很快聽來的。／船上的事：他說是事後很快聽來的 | 這是全集的答案句，卻多掛了一個「他說」。他只說「要不是親眼看見，就是事後立刻聽到」，**沒有**指明哪段屬於哪一種。把船上歸給「聽來的」是推論，推論本身合理（他不在船上），但不是他說的。`research.md` 的〈日期與見證位置〉也是編者的分層，不是信的話。 | 英譯 L3615–3618；拉丁「omnia me quibus interfueram quaeque statim … audieram」 | 「船上那些他不在場，只能算他說的另一種：事後很快聽來的。」片尾卡：「船上的事：他不在場，只能是事後聽來的」 | 過強 |
| 4 | pn001、pn002、pn014，連帶 pn065、pn127、首章名、`description` 首句 | 你說不了，我還有東西要抄。／這句話留了一千九百多年 | 留下來的回答不是這句。拉丁是「respondi studere me malle」（我回答寧願讀書），英譯是「had rather go on with my work」。「要寫的東西」是作者另外補的一句旁白（forte ipse quod scriberem dederat），不是回答的內容。「抄」也只來自英譯 write out，拉丁只是 scriberem（寫），`L65a` 列自己寫的是「寫作」。把合併改寫的話說成「這句話留了一千九百多年」就太強了。 | 英譯 L3539–3541；拉丁 6.16.7；`L65a` | 全部改「功課」：pn001「我還有功課要做」；pn014「開頭那句話就是這時候回的，他說寧願留下來讀書；手上剛好還有舅舅交代要寫的東西。」pn065、pn127、章名、`description` 同步。若要留「抄」：pn002 改「這個回答留了一千九百多年」，`description` 界線段註明「抄」是英譯 write out 的譯法 | 過強 |
| 5 | pn019 | 要救的不只瑞克蒂娜，還有沿岸一連串的城鎮。 | 拉丁是 multis（很多人），緊接著的理由是這段海岸人煙稠密。「towns」是 Melmoth 加的，`L65b` 列自己寫「救沿岸居民」，LRB 也寫 many other people。`claims.md` 標了「未裁決」，這裡裁決。 | 拉丁 6.16.9「non Rectinae modo sed multis — erat enim frequens amoenitas orae」；LRB「many other people in need of rescuing」 | 「要救的不只瑞克蒂娜，還有這片人煙稠密的海岸上很多人。」 | 過強 |
| 6 | `card-two.sub`、`youtube.description` 界線段 | 對照拉丁文本／逐句依 William Melmoth 英譯……再對照 The Latin Library 的拉丁文本 | `research.md` 和 `NOTES.md` 都明寫拉丁文本「只對了這幾個字」，觀眾會讀成每句都對過。第 4、5、7、8、10、12 列就是逐句對照會抓到、而當時沒抓到的地方。 | `research.md` 追加段首句；`NOTES.md` | 照實寫：字卡「Melmoth 英譯」；說明「逐句依英譯，舅舅、年齡、舵手那句、龐貝地名另對拉丁文本；不是手稿校勘」。若第 4、5、7、8、10、12 列都照改，本次查核已通讀拉丁文，原句可保留 | 過強 |
| 7 | pn035、`description` | 只是村民丟下的村莊在燒。 | 拉丁是農民慌亂中留下的火（ignes relictos）和無人的 villas（農舍、宅院），不是村莊。「villages」是英譯。 | 拉丁 6.16.13「agrestium trepidatione ignes relictos desertasque villas」 | 「只是農民慌忙丟下的爐火和空屋在燒。」`description` 改「火光是空屋在燒」 | 措辭 |
| 8 | pn006、pn046、pn083 | 海邊有人替舅舅鋪了一塊帆布 | 「sail cloth」是英譯；拉丁是 linteum（亞麻布），abiectum 是「丟在地上的」。而且這是貫穿全集的鉤子。 | 拉丁 6.16.18「super abiectum linteum recubans」 | 三句改「一塊布」，意思不變。提示詞的 sail cloth 可不動 | 措辭 |
| 9 | pn025 | 舵手勸他掉頭。舅舅停下來，想了一下。 | 順序反了。原文是他先停下來考慮要不要回頭，舵手才勸。 | 拉丁 6.16.11「Cunctatus paulum an retro flecteret, mox gubernatori … monenti」；英譯 L3560–3561 | 「舅舅停下來，想了一下要不要回頭。舵手勸他掉頭。」懸念不變 | 措辭 |
| 10 | pn024 | 海水又突然退開，船有擱淺的危險 | 拉丁只說 vadum subitum（突然變淺），「海退」是英譯的解釋；`L65b` 也跟著寫「退海」。 | 拉丁 6.16.11 | 「海水又突然變淺，船有擱淺的危險」 | 措辭 |
| 11 | pn027 | 這位朋友住在斯塔比亞 | 原文只說他當時在那裡。 | 英譯「was then at Stabiae」；拉丁「Stabiis erat」 | 「這位朋友當時在斯塔比亞」 | 措辭 |
| 12 | pn077 | 幾隻海裡的動物，就這樣被留在岸上。 | 拉丁是 multa（很多），英譯 several，「幾隻」比兩者都少。 | 拉丁 6.20.9「multaque animalia maris」 | 「不少海裡的動物」 | 措辭 |
| 13 | pn059 | 前幾天地面就一直在抖 | 原文是好多天。 | 英譯「for many days before」；拉丁「per multos dies」 | 「之前好多天，地面就一直在抖」 | 措辭 |
| 14 | pn064 | 只說那年才十八歲上下。 | 「十八歲上下」當描述可以接受（英譯 18、拉丁第十八個年頭、LRB 與 USNA 17、維基 17 or 18），但「只說」把含糊算到他頭上。他給的是一個明確的序數。 | 拉丁 6.20.5「agebam enim duodevicensimum annum」 | 「只提了自己那年的年紀，算起來十七、八歲。」`description` 同步 | 措辭 |
| 15 | pn102 | 這就是傳說中那個沒有盡頭的最後黑夜。 | 這句單獨成景、單獨配音，只靠上一句句尾的逗號接「認定」。`L66c` 的界線是「世界終結是恐懼，不是災情事實」。 | 拉丁「interpretabantur」；`L66c` | 「以為這就是傳說中那個沒有盡頭的最後黑夜。」 | 措辭 |
| 16 | `description` 首段 | 那艘船開往維蘇威火山 | 問他的是一艘輕船（liburnica），開去的是改派的軍艦（quadriremes）。pn002、pn019 分得清楚，說明欄併成同一艘。 | 拉丁 6.16.7、6.16.9 | 「舅舅後來帶軍艦開往維蘇威火山」 | 措辭 |
| 17 | 文件：`research.md` N9、`claims.md` pn054、`sources` | who were at Misenum-- | 固定版 L3613 實印「Miscnum」（掃描錯字），引文無聲改過，應註明。`sources` 的 Pliny the Elder 維基沒有對應的查核列；`N6` 見第 2 列。`brief.md` 仍有 18 處「叔父」（舊的企劃，觀眾看不到）。 | 固定版 L3613 | 註明錯字；`N5` 補維基；`brief.md` 加一行更正 | 措辭 |

## 看過、沒有列成問題的

- **pn002** 一千九百多年：信約寫於爆發後 25 年左右（維基 some 25 years after），相減仍在一千九百多年內。
- **pn006、pn007** 第二天、同一天：兩封信對得起來（舅舅那邊「It was now day everywhere else」，母子那邊「it was now morning」），是推算但穩。
- **pn119** 「消息什麼時候到、誰帶來的，兩封信都沒寫」：通讀拉丁與英譯確認如此。
- **pn121** 「只多交代了一件事」：拉丁就是「Unum adiciam」，比英譯更貼。
- **pn124** 沒有龐貝兩個字：自己重新搜尋，兩個文本都零筆。
- **pn043**「全部的防護」（拉丁只說這是防護）、**pn063**「拿起」（拉丁 posco，叫人拿來）、**pn093**「像雲」（拉丁「torrentis modo」，像洪流）：都依英譯且不改變事實，只記錄，不要求改。
- **標題、縮圖**：「79 年龐貝被埋，少年沒上船，憑什麼寫出船上的事？」沒有比紀錄強；pn122、pn123 給了誠實的答案（他說事後立刻聽到，誰說的沒寫）。開場 pn004、pn005、pn006、pn007、pn008、pn009 都在正片兌現。
- **pn048**「就這樣死了」：照信寫。Suetonius 有別的說法，本集說明只照兩封信，不算問題；若將來要講「他怎麼死的」才需要提。此項未開原文，僅憑記憶，不當依據。
