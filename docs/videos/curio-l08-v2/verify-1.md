# curio-l08-v2 查核第一輪

- 查核 2026-10-13，Claude Opus 5（獨立查核代理）。**我不是這一版的撰稿人**，也不是第一版的撰稿人或
  協調者；這份檔案只讀 `video.json`、`claims.md`、`brief.md`、`NOTES.md` 與來源，沒有動其中任何一個。
  要改的句子寫在文末，由別人套用。
- 方法：先把 `video.json` 的每句旁白（144 句，`say` 一個都沒有）、每張卡片的每個文字欄位、七個章名、
  標題、說明欄、十個標籤、縮圖四欄、`loops` 四條與 `sources` 十九筆抽成 273 條清單
  （`<scratch>/verify-l08/claims-list.txt`，另有 `scene-dump.txt`、`meta-dump.txt`、與第一版逐句對照的
  `v1-dump.txt`）。再把 `claims.md` 列的每一個網址當天用 curl 重開（User-Agent
  `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 1.6 秒），去掉標籤後
  讀全文；兩個 PDF 用 pdftotext 轉文字。**沒有用網路搜尋（0 次）**，來源都已經指名。
- 這一版宣稱「事實全部沿用第一版，只有講法換了」，所以查核的重點放在**講法換了的地方**：把 v2 的
  144 句逐句對到第一版的 114 個場景，凡措辭與第一版不同、或第一版有而這一版沒有的限定語，一律回到
  原始來源重讀。這抓到的八成問題都在這一類。
- 來源代號 S1–S19 同 `../curio-l08/research.md`。最重的是 S1（TIME 1991-09-23 全文轉載）、S2（紐約時報
  1991-09-10 存檔）、S6（Fortean Times 371 訃聞 PDF）、S4（Physics World 2011）、S14（1996-10-27 訪問，
  分兩頁）、S19（圈內人自述）；S16（Bower 訪問逐字稿）與 S13（Independent 2004）是次級來源，單獨不定案。
  S3（Smithsonian）第一版因為 403 就沒有放進 `sources`，這一版照舊，我也沒有把它當依據。
- 判定「這一版的旁白說得比來源多嗎」時，我只看來源寫了什麼，不看第一版通過了兩輪查核；凡第一版就有
  的問題我會註明「第一版就這樣」，但不因此改判。

## 當天開過的網址

二十個，全部 200。

| 代號 | 網址 | HTTP |
|---|---|---|
| S1 | https://www2.nau.edu/~gaud/bio372/class/readings/circ.htm | 200 |
| S2 | https://web.archive.org/web/20180613234536/https://www.nytimes.com/1991/09/10/world/2-jovial-con-men-demystify-those-crop-circles-in-britain.html | 200 |
| S4 | https://physicsworld.com/a/coming-soon-to-a-field-near-you/ | 200 |
| S5 | https://web.archive.org/web/20251111084343/https://www.britannica.com/biography/Doug-Bower | 200 |
| S6 | https://circlemakers.org/028_FT371.pdf | 200 |
| S7 | https://improbable.com/ig/winners/ | 200 |
| S8 | https://ufologie.patrickgross.org/press/independent4nov2000.htm | 200 |
| S9 | https://www.fwi.co.uk/news/crop-circle-maker-fined | 200 |
| S9b | https://web.archive.org/web/20140515090322/http://www.thisiswiltshire.co.uk/archive/2000/11/07/7393897.Man_fined___100_for_making_crop_circle/ | 200 |
| S10 | https://www.fwi.co.uk/news/crime/farmers-tell-fw-of-stress-and-anguish-over-unwanted-crop-circle | 200 |
| S11 | https://www.fwi.co.uk/arable/hidden-truths-of-crop-circles | 200 |
| S12 | https://www.theguardian.com/environment/2022/sep/24/invasion-of-the-barley-snatchers-crop-circles-cost-farmers-thousands-in-lost-revenue | 200 |
| S13 | https://circlemakers.org/cereal_entrepreneurs.html | 200 |
| S14 | https://circlemakers.org/la.html | 200 |
| S14b | https://circlemakers.org/la2.html （c28 引的那句在第二頁，`claims.md` 只列了第一頁） | 200 |
| S15 | https://www.cicap.org/crops/en/jse_pr_en.pdf | 200 |
| S16 | https://ufology.patrickgross.org/htm/cropbower01.htm | 200 |
| S17 | https://hoaxes.org/weblog/comments/september_9 | 200 |
| S18 | https://www.womensweekly.com.au/news/crop-circles-australia-tully/ | 200 |
| S19 | https://circlemakers.org/new_documents.html | 200 |

## 主張表

判定：CONFIRMED 看到了／CHANGED 要改（改法在文末，我沒有動檔案）／NOT FOUND 沒看到／
OUT OF SCOPE 風格、問句、系列安排，不判。

| # | 主張 | 位置 | 來源原文 | HTTP | 判定 |
|---|---|---|---|---|---|
| c1 | 兩個風景畫家，1991 年 67 歲與 62 歲，畫框店 | cl1c、cl4e、their-ages 卡 | S1「two land-scape painters, David Chorley, 62, and Douglas Bower, 67」；S6「opened a gallery and picture-framing studio」。卡片標「時代雜誌 1991 年的報導」，Chorley 的年齡只有這一源，標得對 | 200 | CONFIRMED |
| c3 | 兩人每週五晚上喝一杯 | cl1b、章名 1 | S6「They used to meet for a beer every Friday evening」；S16「we used to go out on Friday evenings for a pint of beer」。**沒有一條寫到打烊或「最後一杯」** | 200 | CHANGED（章名 1） |
| c4 | 起始年份 1976／1978 分歧；第一個圓直徑約九公尺 | cl1a、cl1i、cl2a2、nine-metres 卡 | S6「his idea in 1976」「a simple circle, 30ft (9m) across」；S19「One Friday night in June 1976」「about 30 feet across」；S1「conceived their hoax in 1978」。旁白說「七〇年代後半」又在 cl2a2 把兩個年份都講出來，卡片保留「大約」 | 200 | CONFIRMED |
| c5 | 道格移民澳洲，住了好幾年才回英國；飛碟巢是從報紙上讀到的 | cl2c、cl2d | S6：1976 年時「18 years earlier」設籍澳洲（即約 1958 年，當時 34 歲，已婚十年，與妻同行），1968 年回漢普郡；S16「eight and a half years」「I saw an article in the Australian newspaper one day」。**沒有一條支持「年輕時」** | 200 | CHANGED（cl2d） |
| c6 | 1966 年昆士蘭香蕉農看到飛碟升空、蘆葦被壓成三十呎的圓、叫飛碟巢 | cl2e、cl2f、cl2g、cl1g、cl2b、cl3a2 | S18「banana farmer George Pedley」「It then shot off above the treetops」「tall reeds were now woven into a 30-foot diameter circle」「The so-called "flying saucer nest" – a term predating crop circle terminology – was so peculiar it became national news」；S6「Doug told Dave about the mysterious 'saucer nests' he'd read about in a newspaper」「make it look as if a flying saucer has landed」；S1「Saucer enthusiasts argued that the cropland patterns marked the landing spots of UFOS」。**三十呎是 S18 的原數（`claims.md` 寫「約 30 呎」反而比來源鬆），但「當地人把它叫做」沒有來源** | 200 | CHANGED（cl2g） |
| c7 | 做了十三年 | cl7zb、outro 卡 | S1 兩處寫「during the past 13 years」「for the past 13 years」，而 S1 的起算是 1978；S13 裡 Lundberg 寫「spent 14 years」；S6／S19 的 1976 起算是 15 年。**三個數字，旁白給了一個** | 200 | CHANGED（cl7zb、outro 卡） |
| c8 | 頭三年沒人注意；一九八〇年前後第一篇報導，標題「那個東西又回來了」 | cl1k、cl2u、cl2v、cl2w、the-thing-returns 卡 | S1「this and other forays during the next three years went unnoticed. But one of their circles was spotted in 1981」；S6「until in 1980, in a field near Westbury, someone noticed and their circle made the newspapers … "The Return of the Thing", ran the headline」。卡片的 1980 標明出自訃聞，旁白說「前後」 | 200 | CONFIRMED |
| c9 | 1991-09-09 英國小報，標題「騙了全世界的人」 | cl4d、cl4q、conned-the-world 卡 | S17「September 9, 1991: … the British tabloid Today announced」；S2「According to Today, which broke the story with the headline "Men Who Conned the World"」 | 200 | CONFIRMED |
| c10 | 最早用的是一根拴畫框店後門的鐵棒 | cl1e、cl1f、nine-metres 卡、說明欄第一段 | S19（**圈內人自述，單源**）「Using a heavy iron bar - normally employed to secure the rear doors of Doug's picture-framing gallery - they swirled a simple circle, about 30 feet across」。S6 這篇訃聞（同一作者 Rob Irving）講第一個圓時完全沒有提鐵棒。**第一版的旁白寫「照圈內人的記述，他們最早用的是一根鐵棒」，這一版把限定語拿掉了** | 200 | CHANGED（cl1e／cl1f 一處、說明欄） |
| c11 | 木板一公尺多長、繩子、帽簷上的鐵絲圈、膝蓋高度 | cl2j、cl2k–cl2n、cl2o、how-to-press-a-ring 卡 | S1「a 4-ft. long wooden plank, a ball of string and a baseball cap with wire threaded through the visor as a sighting device」「At the center … Bower held one end of the string. The other end was attached to the plank, held horizontally at knee level by Chorley」。卡片的「約 1.2 公尺」是 4 呎換算，來源欄標「兩人自己的說法」，S1 裡確有 Chorley 的解釋句 | 200 | CONFIRMED |
| c12 | 太太先發現里程不對、剪報簿、帶她去看一次才信 | cl2r、cl2s、cl2t | S16「this car needs servicing quite a lot … with the enormous amount of miles you're doing」「I had no alternative but to handle the huge album with all the Press cuttings … you take me out one night … Which we did, and then, it was true」。旁白標「照道格自己的說法」，沒有說「懷疑外遇」 | 200 | CONFIRMED |
| c13 | 肯特郡：記者帶他們去、當面做一個圈、研究者說人類做不出來、兩句對話 | cl4f、cl4g、cl4h、cl4i、cl4j、cl4k、cl4l、cl4m、cl4n、no-human 卡 | S1「Graham Brough, a reporter from the London tabloid Today who had **alerted** Delgado to the latest apparition, **introduced** him to two land-scape painters」「They had created the Sevenoaks circle while Brough looked on」「Delgado was **gazing** at a large area」「marveled … **as he stood in a wheat field**」「No human could have done this.」「I'm afraid we've been having you on.」「We have all been conned」；S17「To prove their claim, the pair created a crop circle in the presence of a Today journalist」。**「打了一通電話」「看了很久」「站起來說」三個動作都不在任何來源裡** | 200 | CHANGED（cl4h、cl4j、cl4k） |
| c14 | 氣象學者的假說：旋轉氣柱帶著帶電物質把作物壓平，叫電漿渦旋 | cl3b、cl3c、cl3d、cl3e、章名 3 | S1「Meaden says, when whirling columns of air pick up electrically charged matter, flatten the crops below」，而且 S1 寫他的團隊主張那個天氣現象是「**often** responsible」；S4「Terence Meaden, then a **meteorologist** and physicist」「an electromagneto-hydrodynamic "plasma vortex"」。「氣象學者」這個身分 S4 支持。**但沒有一條寫他說過「那不是人做的」，S4 還明寫他後來承認帶直線的是人做的** | 200 | CHANGED（cl3b） |
| c15 | 一位退休工程師和夥伴的專書賣了五萬多本 | cl3f、cl3g、cl3h、cl4i、fifty-thousand 卡 | S1「retired engineer Pat Delgado」「has co-authored a book called Circular Evidence with another believer, Colin Andrews. It has sold more than 50,000 copies」 | 200 | CONFIRMED |
| c16 | 兩人為了證明跟天氣無關而加圓、後來出現直線、氣象學者承認那些是人做的、但強調單純的圓還是可能來自大氣 | cl3j、cl3k、cl3l、cl3m、cl3n | S4「the pair increased the number of circles in their formations, **hoping to demonstrate** that they were not weather-related」「even Meaden conceded that these straight-line designs … were man-made, although he stressed that simple circles could still be a consequence of atmospheric phenomena」。**「決定證明」比「hoping to demonstrate」強；第一版寫的是「想證明」** | 200 | CHANGED（cl3j） |
| c17 | 1991 年一位物理學家說，麥田圈要嘛是惡作劇要嘛是空氣渦旋 | cl3o、cl3p | S4「When a spate of circles appeared … in 1991, Hawking told a local newspaper that "crop circles are either hoaxes or formed by vortex movement of air"」。旁白不說名字，照規則 | 200 | CONFIRMED |
| c18 | 數量三說並列：兩百多、兩百五十、每季最多二三十個 | cl3r、cl3s、cl3t、how-many-stats 卡 | S5「more than 200 crop circles since the late 1970s」；S4「confessed to making 250 formations」；S1「as many as 25 to 30 new circles each growing season」。卡片逐一標是誰的數字，旁白不給單一數字 | 200 | CONFIRMED |
| c19 | 「人類做不出來」這個流傳的說法 | cl4k、cl5o | S2「the genuine article, of the sort no human could have made」；S1 Delgado 原話 | 200 | CONFIRMED |
| c20 | **為什麼公開，紀錄有兩種說法** | cl3u、cl3v、cl4a、cl7x、cl7y、cl7z、cl7zb、two-accounts 卡、loops[3] | S1「It was only after circle enthusiasts began seeking government funding that the two jovial con men decided to admit to the hoax」；S6「Doug regretted admitting having made crop circles. Not making them, but telling people about it. **This was not his choice but Dave's**」。`claims.md` 自己寫「旁白兩種都講，各標是誰寫的」，卡片的 verdict 也寫「紀錄沒有把這一點講定」。**但旁白只講了訃聞那一種（cl7z）；時代雜誌那一種從頭到尾沒有被標出來，最後一句 cl7zb 直接把它當成答案講掉** | 200 | CHANGED（cl7zb，連帶 cl7y、loops[3].what） |
| c21 | 之後在漢普郡對記者再做一次；另一位研究者說除了兩個身體很好的六十歲老人沒什麼了不起 | cl4r、cl4s、cl4t | S2「**Late today**, the two men demonstrated their craft before reporters in a field in Hampshire」「Colin Andrews, who is an associate of Mr. Delgado … "There is nothing here to impress us at all except two very fit 60-year-olds"」。旁白說「之後」，沒有說同一天 | 200 | CONFIRMED |
| c22 | 第一個研究者後來改口；加拿大也有圈 | cl4u、cl4v、cl4w、cl4x | S1「The two gents may have hoaxed some of the circles … but the phenomenon is still there」；S2「At first … he confessed that he and a lot of others had obviously been duped … But later he argued that the men's claims appeared suspect」「Yesterday there were circle discovered on a prairie in Canada … Have these guys been out there with their board?」 | 200 | CONFIRMED |
| c23 | 1992 年搞笑諾貝爾物理獎，理由是用幾何破壞英國作物 | cl5f、cl5g、award-reason 卡 | S7「**The 1992 Ig Nobel Prize Winners** → PHYSICS: David Chorley and Doug Bower, lions of low-energy physics, for their circular contributions to field theory based on the geometrical destruction of English crops」 | 200 | CONFIRMED |
| c24 | 1991 年夏天田裡已經有別人，圖形超出他們的能力；一個後來的製作者第一個圈做在那個夏天 | cl5b、cl5c、cl5d | S6「By summer 1991, others had joined in … way beyond Doug and Dave's capabilities」；S13「Rod Dickinson clearly remembers the night he made his first crop circle. It was the summer of 1991, just months before … Doug Bower and Dave Chorley, came out」；S1「apparently inspired copycats」 | 200 | CONFIRMED |
| c25 | 他們留下的圖形帶出第二波創作者 | cl5e | S4「the pictographs they created inspired a second wave of crop artists」 | 200 | CONFIRMED |
| c26 | 藝術團體接商業委託；客戶有麥片品牌、電信公司、電視節目；一家報社付農夫六千英鎊，作物約值它的六十分之一 | cl6b、cl6c、cl6d、cl6e、the-fee 卡 | S13「clients including Weetabix, O2, Big Brother, Mitsubishi, and Thompson Holidays」「the paper paid the farmer £6,000 for the equivalent of **around** £100 worth of crops」。6,000÷100＝60，旁白保留「大概」，「一百英鎊」整支片子只出現在罰金那裡一次 | 200 | CONFIRMED |
| c27 | 1998 年電視台拍一百個圓的圖形、一分鐘一個；最複雜的有兩千個獨立形狀 | cl6f、cl6g、cl6h、cl6i、one-a-minute 卡 | S4「it allowed BBC filmmakers to document its construction of a 100-circle roulette pattern in 1998, team members were observed … at the remarkable rate of one every minute」「featuring **up to** 2000 individual shapes」。**「up to」的限定沒了；第一版寫的是「最多的有兩千個」** | 200 | CHANGED（cl6i） |
| c28 | 1996 年七月巨石陣旁的圖形：醫生的說法與製作者的說法出自同一篇沒有錄音的訪問 | cl5j、cl5k、cl5l、cl5m、cl5n、cl5o、cl5q、cl5r、cl5s、cl5t、cl5p、cl5u、forty-five-minutes 卡 | S14「On July 7, 1996, in a field just south of Stonehenge」「it was reported that a doctor in a private plane flew over the field at **about** 5:30 pm that day and again **about** 45 minutes later」「The interview wasn't taped」；S14b（第二頁）「It was made the previous night, by three people, in **about** two and three-quarters hours, starting around 2:45 am … When that doctor flew over, he just didn't see it the first time」，他只說「They were made by people」與知道是誰，沒說自己做的。**第一版的 steps 卡寫「約 2 小時 45 分」，這一版把「約」弄掉了**；圓圈數照舊不講 | 200 | CHANGED（cl5r；forty-five-minutes 卡建議） |
| c29 | 同一個月另一個圖形有一百九十四個圓 | cl5v、one-nine-four 卡 | S4「That same evening, 194 "crop circles" … appeared in a nearby field at Windmill Hill」（S4 全段講的是 1996 年七月）；S14「less than a month later, on **July 29** … totalling 194 individual circles」。兩源都在 1996 年七月 | 200 | CONFIRMED |
| c30 | 有研究者說圈裡麥稈的節被拉長，推測是電磁輻射加熱 | cl6k、cl6l | S4「Levengood … proposed that the elongated pulvini were a result of superheating from electromagnetic radiation」。旁白說「有研究者說」「他推測」，把觀察與推測分開（第一版是合成一句的） | 200 | CONFIRMED |
| c31 | 批評者指出統計與取樣有問題；被壓倒的麥子本來就會長得不一樣 | cl6m、cl6n | S15「the misrepresentation of the experimental protocols, the misleading application of statistical procedures, the arbitrary discarding of unwanted results」「nothing but a mere difference in the stem elongation between the flattened plants … as one should expect when whatever kind of mechanical force flattens the plants」 | 200 | CONFIRMED |
| c32 | 這些研究沒有被證實也沒有被推翻 | cl6o、cl6p | S4「neither Levengood nor Haselhoff's work has ever been reconfirmed or disproved by subsequent studies」。cl6o 的「最老實」是評語，當意見 | 200 | CONFIRMED |
| c33 | 2017 年六十公尺寬的圈壓掉兩英畝小麥；農夫放水桶請人捐錢 | cl7c、cl7e | S10「The crop circle is **about** 60m wide and covers **about** two acres of quality milling wheat」「the Klindts have put a bucket in the field, asking for donations to help offset some of the crop loss」。**兩個「about」都沒了（第一版也沒有）** | 200 | CHANGED（cl7c，輕） |
| c34 | 那是別人的田；威爾特郡警方說這是刑事毀損 | cl2p、cl7n、cl7q | S10「Rural crime officer Marc Jackson of Wiltshire Police … reiterated that creating a crop circle is criminal damage and an offence」 | 200 | CONFIRMED |
| c35 | 衛報估算：2018–2022 年英格蘭 92 個圈、三萬英鎊、四十多個足球場 | cl7g、cl7h、cl7i、the-losses 卡 | S12「More than 40 football pitches' worth of arable land has been affected by crop circles **in England since 2018**, according to an analysis carried out by the Guardian. Farmers lost £30,000 in income between 2018 and 2022 as a result of 92 crop circles」。卡片標題寫明英格蘭與衛報的估算，旁白說「衛報算過」 | 200 | CONFIRMED |
| c36 | 2004 年遊客中心職員說夏天八到九成的生意跟麥田圈有關 | cl7j、cl7k、cl7l | S13「**Around 85 to 90 per cent** of our custom during the summer months is connected to crop circles," says Jo Smith, an information assistant at Avebury Tourist Centre」。**來源是八成五到九成，旁白說八到九成（第一版也是）**；四週三萬英鎊那個傳聞照舊不用，地名照舊不說 | 200 | CHANGED（cl7l） |
| c37 | 2000 年有人認罪，被罰一百英鎊 | cl7o、cl7o2 | S9「Williams, 29 … was fined 100 and ordered to pay 40 costs by Devizes magistrates after pleading guilty to causing criminal damage」；S9b（帶英鎊符號）「A man was fined £100 after admitting damaging farmland」「also ordered to pay £40 costs by Devizes magistrates」。旁白不說名字、不說「唯一被定罪」（兩源寫的是 first，不是 only），照規則 | 200 | CONFIRMED |
| c38 | 道格活到 2018 年九十四歲；晚年後悔的是告訴了大家 | cl7r、cl7s、cl7t | S6「died West End, Hampshire, 21 July 2018, aged 94」「Doug regretted admitting having made crop circles. Not making them, but telling people about it」。戴夫的卒年照舊不講，對 | 200 | CONFIRMED |
| c39 | 圈內人想像他會說「那只是壓平的麥子」 | cl7u | S19「I'm sure his mischievous spirit will be looking down, chuckling to himself and whispering to the audience "It's only flattened corn."」。旁白標「想像」，corn 譯成麥子 | 200 | CONFIRMED |
| M1 | 標題：為什麼 1991 年兩個英國老先生承認麥田圈是他們做的 | youtube.title | 是問句，與 c9／c13 相符；**但全片對這個問句的答案就是 cl7zb，見 c20** | — | CONFIRMED（連帶 c20） |
| M2 | 說明欄第一段：星期五晚上、喝完最後一杯、拴畫框店後門的鐵棒、約九公尺、之後整整三年 | youtube.description | 見 c3、c4、c10。**鐵棒的來源限定在這裡也沒有** | 200 | CHANGED（說明欄） |
| M3 | 說明欄第二段的十一個事件（飛碟巢、鐵棒換木板、一九八〇年前後、電漿渦旋、五萬多本、直線、九月肯特郡、第二波與委託、四十五分鐘的兩面說法、損失、觀光、刑事毀損） | youtube.description | 逐條對上 c5–c36；「一九九一年九月肯特郡」由 S2「a pattern found over the weekend in a Kent wheat field」（1991-09-10 見報）與 S1「last week」佐證 | 200 | CONFIRMED |
| M4 | 說明欄第三段：流傳的版本標明是誰在哪一年說的、來源矛盾就說矛盾、沒有定論就說沒有定論 | youtube.description | 這是向觀眾做的承諾。**cl7zb 違反它的第三句** | — | CHANGED（連帶 c20） |
| M5 | 標籤十個、縮圖四欄（「一塊木板」「一九九一年的自白」） | youtube.tags、thumbnail | 木板出自 S1，1991 年自白出自 S2／S17；`thumbnail.data.shot` 指到存在的場景 | 200 | OUT OF SCOPE（標籤）／CONFIRMED（縮圖） |
| M6 | 章名 2–7 | scenes[].chapter | 章名 2 是 S6 的標題轉述、3 是 c14、4 是 c13、5 是 c24、6 是 c26、7 是第一版的旁白句 | 200 | CONFIRMED |
| M7 | 章名 1「酒吧打烊，他們提著一根鐵棒進麥田」 | scenes[0].chapter | 星期五那一晚、鐵棒、麥田都有來源（S19「One Friday night in June 1976」、S16「it was Fridays' nights that we were doing the circles」）；**「打烊」沒有** | 200 | CHANGED（章名 1） |
| M8 | `loops` 四條 | loops[] | 四條的 setup／payoff 行 id 都存在；[0]–[2] 沒問題。**[3].what「那筆研究經費跟他們開口有什麼關係」預設了因果，而紀錄沒有把這一點講定** | — | CHANGED（loops[3].what） |
| M9 | `sources` 十九筆、checked_on 2026-10-10 | sources[] | 十九個網址當天我全部重開，都是 200。**S8（Independent 2000-11-04）與 S11（FW 2010）在這一版沒有任何一句靠它們**（NFU 的原話與 2010 年的誠實箱都拿掉了）；S3（Smithsonian）在 c4／c25／c38 的文字裡被引用，但網址不在 `sources`，也不在那幾條的網址欄——沿用第一版的決定 | 200 | CONFIRMED（兩筆冗餘，見「懷疑但沒改」） |
| M10 | 十三個不帶事實的場景 | walk-home、the-question、back-again、settle-it-later、researchers-arrive、problem-comes、no-longer-theirs、not-the-strangest、harder-and-paid、nobody-counted、remember-the-bill、my-own-view、archived | 全部在 `claims.md`〈不是來源主張的句子〉裡列到；`my-own-view` 兩句標成站主意見。125 個場景沒有一個落在清單外 | — | OUT OF SCOPE |

## 要改的地方

十六條要改的（重 5、中 6、輕 5），加一條判了 CONFIRMED 但值得記的（第 17），再加給 `claims.md` 的
兩筆（第 18、19）。每一條都給行 id、現在的字、應該的字；我沒有動 `video.json`、`claims.md`、
`brief.md`、`NOTES.md`。括號裡是改後的旁白單位數（這一集最長的句子是 22 單位，全部在上限內）。

### 重（這一版新出現的，會讓觀眾拿到紀錄沒有給的答案）

1. **`cl7zb`（`outro` 第一句）——把沒有定論的事講成定論，而且丟掉出處。**
   現在：「做了十三年之後，是那筆研究經費讓他們開了口。」
   問題：這句之前十幾秒，`two-accounts` 卡的 verdict 才剛寫「紀錄沒有把這一點講定」；`claims.md` c20
   也寫「旁白兩種都講，各標是誰寫的」。這一句把 S1 的說法（愛好者要經費）當成全片的答案，沒有標是
   時代雜誌寫的，而 S6 那篇訃聞寫的是「This was not his choice but Dave's」。只聽聲音的人（含配音版，
   卡片不會被唸出來）聽到的順序是：「紀錄留下兩種說法」→「一篇訃聞寫，公開是戴夫的主意」→
   「是那筆研究經費讓他們開了口」——時代雜誌那一種從來沒有被標出來，最後一句聽起來就是結論。
   `NOTES.md` 寫得很清楚這是刻意的結構（「`outro` 第一句第一次說出答案」），所以要改的是這個結構的
   最後一步，不是順便的一句話。
   應該改成：「做了十幾年之後，紀錄沒有把這一點講定。」（17）
   連帶：`cl7y`「為什麼開口，紀錄留下兩種說法。」→「為什麼開口，時代雜誌寫是為了那筆經費。」（17）
   ——這樣左欄（時代雜誌）揭曉時旁白有把它標出來，`cl7z`（訃聞那一種）不用動，兩種說法在聲音裡都
   成立；`loops[3].what`「那筆研究經費跟他們開口有什麼關係」→「那筆研究經費在兩種紀錄裡的位置」。
   （如果一定要在片尾說出時代雜誌那個理由，最少要寫成「時代雜誌寫，是那筆經費讓他們決定承認。」(17)，
   不能是無主的「是那筆研究經費讓他們開了口」。）

2. **`outro` 的 `data.lines[0]`——把 13 到 15 年收斂成一個數字。**
   現在：「一塊木板，兩個人，十三年」
   問題：13 年是 S1 的數字，而 S1 的起算是 1978；S13 裡 Lundberg 寫 14 年，S6／S19 的 1976 起算是 15 年。
   這一集自己在 `cl2a2` 告訴觀眾起始年份有兩說，片尾卻給一個只在其中一說下成立的數字。第一版寫的是
   「十幾年」。
   應該改成：「一塊木板，兩個人，十幾年」（10）。`cl7zb` 照第 1 條改成「十幾年」後兩邊一致。
   （要留 13 這個數字也可以，但得標出處，例如卡片上寫「時代雜誌算十三年」。）

3. **`cl1e`／`cl1f`——鐵棒的出處限定不見了。**
   現在：`cl1e`「道格手上提著一根鐵棒。」`cl1f`「那根鐵棒，平常拴著他畫框店的後門。」
   問題：鐵棒只有 S19 一源，而 S19 是圈內人自己的網站文字；同一位作者寫的那篇訃聞（S6）講第一個圓
   時根本沒提鐵棒。第一版的旁白是「照圈內人的記述，他們最早用的是一根鐵棒」，這一版把「照圈內人的
   記述」拿掉了，於是一個單方面的說法變成紀錄。這根鐵棒是第 1 章的章名、`nine-metres` 卡的副題、
   說明欄第一段和一整個 loop 的 setup，份量不輕。
   應該改成（兩句改一句就夠）：`cl1f`「照圈內人的記述，那是拴畫框店後門的鐵棒。」（18）
   連帶：`nine-metres` 卡的 `sub`「一根鐵棒，一個晚上」→「圈內人的記述：一根鐵棒，一個晚上」；
   說明欄第一段「提著一根拴畫框店後門的鐵棒走進麥田」→「提著一根鐵棒走進麥田（圈內人的記述）」。

4. **`cl3b`——把氣象學者沒說過的話放進他嘴裡。**
   現在：「一位氣象學者說，那不是人做的。」
   問題：沒有一條來源寫他說過這句。S1 寫他的團隊主張那個天氣現象是「often responsible」（常常是，
   不是全部）；S4 寫他後來「conceded that these straight-line designs … were man-made」。這一集自己在
   `cl3m`／`cl3n` 講了他承認直線是人做的——前後矛盾的是旁白，不是來源。
   應該改成：「一位氣象學者提出一個天氣的解釋。」（15）

5. **`cl4h`——憑空多了一通電話。**
   現在：「然後記者打了一通電話。」
   問題：S1 寫的是記者「had alerted Delgado to the latest apparition」並在田裡「introduced him to」兩人，
   沒有寫怎麼通知的。第一版寫的是「記者請來那位寫專書的研究者，看這個圈」。
   應該改成：「然後記者去通知一個人。」（10）

### 中

6. **`cl6i`——「up to 2000」的限定沒了。**
   現在：「最複雜的圖形，有兩千個獨立的形狀。」S4 的原文是「featuring **up to** 2000 individual shapes」，
   第一版寫的是「最多的有兩千個獨立的形狀」。這一集對 S1 的「as many as」就是用「最多」處理的（c18），
   同樣的字要同樣處理。
   應該改成：「複雜的圖形，最多有兩千個獨立的形狀。」（16）

7. **`cl7l`——範圍的下緣從八成五掉到八成。**
   現在：「夏天八到九成的生意，都跟麥田圈有關。」S13 原文是「Around 85 to 90 per cent」。第一版也是
   八到九成，兩輪查核沒有抓到；這是單源的數字，照原文講比較安全。
   應該改成：「夏天八成五到九成的生意，都跟麥田圈有關。」（18）

8. **`cl5r`——「約兩小時四十五分」的「約」沒了。**
   現在：「圖形是前一晚做的，三個人，花了兩小時四十五分。」S14b 原文是「in **about** two and
   three-quarters hours」。第一版的 steps 卡寫的是「約 2 小時 45 分」，這一版拿掉那張卡，「約」也跟著
   不見了，於是一個單方面說法裡的概數變成精確時間。
   應該改成：「圖形是前一晚做的，三個人，約兩小時四十五分。」（19）

9. **`cl2g`——飛碟巢是誰取的名字。**
   現在：「當地人把它叫做飛碟巢。」S18 只寫「The so-called "flying saucer nest" … became national news」，
   沒有寫是當地人取的；S6 寫道格是「read about in a newspaper」。第一版寫的是「大家叫它飛碟巢」。
   應該改成：「報紙把它叫做飛碟巢。」（9）

10. **章名 1——「打烊」沒有來源。**
    現在：「酒吧打烊，他們提著一根鐵棒進麥田」
    星期五那一晚有來源（S19「One Friday night in June 1976」、S16「it was Fridays' nights that we were
    doing the circles」、S6 的每週五一杯），但沒有一條寫到打烊；而且 `cl1a` 說的是「星期五傍晚」，
    跟「打烊」自己也打架。章名會進 YouTube 的章節列表，算公開的字。
    應該改成：「星期五那一杯之後，他們提著鐵棒進麥田」（17）
    （`cl1b`「兩個朋友在小酒館喝完最後一杯。」我判 CONFIRMED：S16 寫他們星期五出門「for a pint of
    beer」，「最後一杯」是戲劇化但不改變事實。若要一併收緊，可以寫「兩個朋友在小酒館喝了一杯。」）

11. **`cl3j`——「hoping to demonstrate」變成「決定證明」。**
    現在：「兩個人決定證明，這些圓跟天氣無關。」第一版寫的是「想證明」。
    應該改成：「兩個人想證明，這些圓跟天氣無關。」（14）

### 輕

12. **`cl4j`「他在田裡看了很久。」**——S1 只寫「Delgado was gazing at a large area」，沒有寫看了多久。
    建議：「他盯著那片倒下的麥子。」（10）

13. **`cl4k`「他站起來說，沒有人類做得出這個。」**——S1 寫的是「marveled … as he **stood** in a wheat
    field」，他本來就站著，「站起來」是多出來的動作。建議：「他站在田裡說，沒有人類做得出這個。」（15）
    （如果 12 照上面改成「盯著」，這裡就不會和前一句重複「站」。）

14. **`cl2d`「他年輕時移民澳洲」**——S6 推算是 1958 年前後，他 34 歲、結婚十年、與妻同行。第一版寫的是
    「道格曾經移民澳洲」。建議：「他曾經移民澳洲，住了好幾年才回英國。」（16）

15. **`cl7c`「二〇一七年，六十公尺寬的圈壓掉兩英畝小麥。」**——S10 原文兩個數字前面都有「about」
    （第一版也沒有）。建議至少補一個：「二〇一七年，約六十公尺寬的圈壓掉兩英畝小麥。」（19）

16. **`forty-five-minutes` 卡的 `text`「45 分鐘」**——S14 原文是「about 45 minutes later」。卡片的 kicker
    「他說再飛過的時候」與 sub「1996 年 10 月一篇訪問的轉述」已經把它標成單方面的說法，所以我沒有把它
    算進「重」；但畫面上的大字是概數，寫「約 45 分鐘」更準。

17. **（記下來，不要求改）說明欄與 `cl1k` 的「整整三年」**——S1 是「during the next three years went unnoticed」，
    「整整」是這一版加的（第一版旁白寫「頭三年」）。`cl1k` 同一個字。這一句我判 CONFIRMED（S1 自己的
    算法就是 1978＋3＝1981），只是記下來：如果要跟「一九八〇年前後第一篇報導」併著看，兩個數字來自
    兩個不同起算的來源，說「之後三年」比「整整三年」安全。

### 給 `claims.md` 的兩筆（不是旁白，但會影響下一輪）

18. **c28 的網址少一頁**：旁白 `cl5r`／`cl5s`／`cl5t` 依據的那段 Dickinson 原話在
    https://circlemakers.org/la2.html （第二頁），c28 只列了 `la.html`。`research.md` 的 S16 兩頁都列了。
    照 c28 現在的網址去查，查不到那句話。
19. **c6 的「約 30 呎」比來源鬆**：S18 的原文是「woven into a **30-foot diameter** circle」，沒有「約」。
    旁白 `cl2f`「三十呎」是對的，反而是清單上的「約」要拿掉，否則下一輪會照清單把旁白改錯方向。
    （另外 `harder-and-paid` 這個場景只有前半句被〈不是來源主張的句子〉收走，後半句「然後有人開始付錢」
    靠的是 c26，建議把這個場景 id 加進 c26 的場景欄。）

## 摘要

- 抽出 273 條主張（144 句旁白、0 個 `say`、卡片與章名與縮圖與說明欄與標籤與 `loops` 與 `sources`），
  併成 48 列判定（38 條主張列 c1、c3–c39，加十列 M1–M10 收主張列以外的位置）：
  **CONFIRMED 29、CHANGED 17、NOT FOUND 0、OUT OF SCOPE 1，另一列（M5）標籤不判、縮圖確認**。
- 125 個場景全部對得上：112 個在 `claims.md` 的主張列裡，13 個在〈不是來源主張的句子〉裡，**沒有一句
  宣稱事實而找不到主張列**。這一點這一版做得比第一版乾淨。
- 十七列 CHANGED 裡，**十五列是這一版重講時新長出來的**（cl7zb／cl7y／outro 卡、cl1e-f、cl3b、cl4h、
  cl4j、cl4k、cl2d、cl6i、cl5r、cl3j、cl2g、章名 1、說明欄兩列、loops[3]），只有兩列是第一版就有的
  （cl7l 的八到九成、cl7c 的兩個 about）。「事實一條都沒改」這個說法在**數字**上成立（沒有一個數字
  被改掉），在**限定語**上不成立：第一版寫過的「照圈內人的記述」「想證明」「最多的」
  「約 2 小時 45 分」「十幾年」，這一版有五處把限定語弄掉了。
- **最重的一條只有一句話**：`outro` 第一句。這一版刻意把「他們為什麼開口」留到片尾當揭曉
  （`NOTES.md` 寫明是結構上的決定），而紀錄給的是兩種互不相讓的說法，片尾需要的是一個答案——
  結構要的東西比來源能給的多，差額就寫成了那一句。標題問的問題、`loops[3]`、`remember-this`／
  `remember-the-funding` 整條線都掛在它上面，所以改法要連著 `cl7y` 和 `loops[3].what` 一起看。
- 會過期的事實：沒有。看到的頁面日期：Physics World 2011-08-04、Fortean Times 371（2018-08）、
  Independent 2004-07-06、TIME 1991-09-23、紐約時報 1991-09-10、衛報 2022-09-24、FW 2017-08-16、
  CICAP 2005、AWW（網路版 2025）、Britannica 存檔 2025-11-11。
- 內容守則：流傳的版本都標成流傳的（`cl3a2`、`cl5k`、`cl5o`、`cl7u`）；沒有編造兩人的對話或心理；
  三處明說那是別人的田（`cl2p`、`cl7n`、`cl7q`）；不說名字、不說「唯一被定罪」、不說店名與地名，
  都守住了；旁白沒有拉丁字母（所以 `say` 一個都不需要）。
- 聽眾檢查：144 句最長 22 單位（`cl2a2`），沒有超過 40 單位的句子（lint 的上限），合計 2,086 單位；
  我提的改法最長 19 單位，都在這一集自己的上限內。
- 沒有用網路搜尋（0 次）。沒有跑 git，沒有跑任何影片階段，沒有花錢。

## 懷疑但沒改的

- `cl2j`「鐵棒換成一塊木板」：沒有一條來源明寫「換」，是 S19（最早用鐵棒）加 S1（後來的做法用木板）
  推出來的。c10 的「最早用的是一根鐵棒」本身就含這個意思，保留。
- `cl6m`「統計和取樣都有問題」：S15 列的是「misrepresentation of the experimental protocols」「misleading
  application of statistical procedures」「arbitrary discarding of unwanted results」「weakness of the
  proposed physical models」。「取樣」對應得鬆（第一版同字），寫「統計和做法」更貼，沒有到要改。
- `cl3s`「他們承認做了兩百五十個」：S4 的原文是 250 個 formations（圖形），不是 250 個圓；卡片把它和
  大英百科的「兩百多個圓」並排在「做了幾個」底下。c18 是這樣設計的，保留。
- `cl6o`「一位物理學者的結論最老實」：是評語。`claims.md` 的〈不是來源主張的句子〉沒有點到這一句
  （c32 的場景欄收了這個場景），下一輪可以考慮把它和 `my-own-view` 一樣標成意見。
- `cl7t`「他晚年說，後悔的是告訴了大家」：S6 把後悔寫成事實陳述，沒有寫是什麼時候說的（同頁另一段
  引的是 2005 年的訪問，那年他 81 歲）。第一版同字，保留。
- `sources` 裡的 S8（Independent 2000-11-04）與 S11（FW 2010-06-01）：這一版沒有任何一句靠它們
  （NFU 的原話與 2010 年的誠實箱都照 `claims.md` 的取捨拿掉了）。多列不算錯，但說明欄的參考資料會
  帶兩筆沒有用到的來源，撰稿方可以決定要不要留。
- S3（Smithsonian）：c4／c25／c38 的文字引了它，網址不在 `sources`，也不在那幾條的網址欄。這是第一版
  的決定（Node 的連結檢查會被 403 擋掉），我沒有把它當依據：那三條靠 S6／S19／S4 也站得住。
- `cl5l`「傍晚五點半」：S14 是「about 5:30 pm」，第一版同字，而且前一句 `cl5k` 已經標成「流傳的版本」，
  保留。
- `one-nine-four` 卡標「同一個月的另一個圖形」：S14 給的日期是 7 月 29 日，S4 寫「That same evening」
  指的是它自己敘述的那一晚。兩源都落在 1996 年七月，卡片說「同一個月」沒有超出來源。
- `cl6f`「電視台來拍他們做圈」的「他們」：指前一個場景的藝術團體（S4 的 Circlemakers），不是兩位
  老先生。聽起來不會誤會，但剪接時若把 `the-fee` 與 `television-comes` 分開，這個代名詞要重看。

## 第二輪

**需要。** 這一輪要求改 16 條，其中 5 條是「重」，超過三條。第二輪請換一個代理，重查上面十七列
CHANGED（特別是 `outro` 那一句改完以後，`cl7y`／`cl7z`／`two-accounts` 卡／`loops[3]`／標題問句五個
地方是不是還互相對得上），再隨機抽三分之一的 CONFIRMED。另外建議第二輪專門看一件事：這一版把第一版
的限定語弄掉了五處，請把 `../curio-l08/video.json` 和這一版逐句對一遍，確認沒有第六處。
