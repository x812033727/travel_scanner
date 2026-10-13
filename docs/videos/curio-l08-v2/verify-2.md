# curio-l08-v2 查核第二輪

- 查核 2026-10-13，Claude Opus 5（第二輪查核代理）。**我不是這一版的撰稿人，也不是第一輪的查核人。**
  我沒有讀過第一輪的工作過程，只讀它留下的 `verify-1.md`、現在的 `video.json`／`claims.md`／`brief.md`／
  `NOTES.md`、第一版的 `../curio-l08/video.json`，以及來源本身。第一輪和撰稿人在我這裡都是**待驗的主張**。
- 為什麼有第二輪：系列規則是一輪改動超過三個事實就換人再查。第一輪要求改 16 條（重 5、中 6、輕 5），
  另加 `claims.md` 兩筆記帳，都已經套用。第一輪自己的結語說有五個地方從此必須互相對得上：`cl7y`、
  `cl7z`、`two-accounts` 卡、`loops[3]` 與標題的問句。
- 方法：
  1. 先把現在的 `video.json` 抽成場景逐句清單（125 個場景、144 句旁白、`say` 零個、七個章名、
     19 筆 `sources`、`assets` 空、標題／說明欄／十個標籤／縮圖四欄／`loops` 四條）。
  2. **自己重寫一份抓取腳本**重開 20 個網址（見下表），沒有沿用上一次留在暫存區的檔案——啟動說明說
     暫存區可能有別人中斷的半成品，我把它們當未驗證的東西，整批重抓、重轉文字、重讀。
     User-Agent 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔
     1.3 秒，兩個 PDF（S6、S15）用 `pdftotext -layout` 轉文字後讀全文。
  3. 第一輪 16 條改動逐條回到來源重判，不看第一輪的理由，只看來源句子與現在的字。
  4. 章名七個全查（第一輪沒有抽章名，這是它留下的洞）。
  5. 從第一輪的 29 列 CONFIRMED 裡抽 13 列重驗（45%，超過三分之一的要求）。
  6. 把第一版和這一版逐句對一遍，回答第一輪交代的問題：**限定語還有沒有第六處被弄掉**。
  7. 機械檢查：單位數、同一個數字有沒有說兩次、四條 `loops` 的 payoff 有沒有給新事實、
     七章的第一句有沒有接上一句。
- **沒有用網路搜尋（0 次）。沒有跑 git。沒有跑任何影片階段（單位數是我自己算的，沒有叫 lint）。
  沒有花任何錢。只寫了這一個檔案與我自己暫存區裡的東西。**

## 當天開過的網址

二十個，我自己重開一次，全部 200。（`sources` 裡的 `checked_on` 是撰稿方的 2026-10-10，我沒有動它；
下面是我在 2026-10-13 重開的結果。）

| 代號 | 網址 | HTTP |
|---|---|---|
| S1 | https://www2.nau.edu/~gaud/bio372/class/readings/circ.htm | 200 |
| S2 | https://web.archive.org/web/20180613234536/https://www.nytimes.com/1991/09/10/world/2-jovial-con-men-demystify-those-crop-circles-in-britain.html | 200 |
| S4 | https://physicsworld.com/a/coming-soon-to-a-field-near-you/ | 200 |
| S5 | https://web.archive.org/web/20251111084343/https://www.britannica.com/biography/Doug-Bower | 200 |
| S6 | https://circlemakers.org/028_FT371.pdf （pdftotext，訃聞兩頁全讀） | 200 |
| S7 | https://improbable.com/ig/winners/ | 200 |
| S8 | https://ufologie.patrickgross.org/press/independent4nov2000.htm | 200 |
| S9 | https://www.fwi.co.uk/news/crop-circle-maker-fined | 200 |
| S9b | https://web.archive.org/web/20140515090322/http://www.thisiswiltshire.co.uk/archive/2000/11/07/7393897.Man_fined___100_for_making_crop_circle/ | 200 |
| S10 | https://www.fwi.co.uk/news/crime/farmers-tell-fw-of-stress-and-anguish-over-unwanted-crop-circle | 200 |
| S11 | https://www.fwi.co.uk/arable/hidden-truths-of-crop-circles | 200 |
| S12 | https://www.theguardian.com/environment/2022/sep/24/invasion-of-the-barley-snatchers-crop-circles-cost-farmers-thousands-in-lost-revenue | 200 |
| S13 | https://circlemakers.org/cereal_entrepreneurs.html | 200 |
| S14 | https://circlemakers.org/la.html （第一頁） | 200 |
| S14b | https://circlemakers.org/la2.html （第二頁，Dickinson 那段原話在這裡） | 200 |
| S15 | https://www.cicap.org/crops/en/jse_pr_en.pdf （pdftotext） | 200 |
| S16 | https://ufology.patrickgross.org/htm/cropbower01.htm | 200 |
| S17 | https://hoaxes.org/weblog/comments/september_9 | 200 |
| S18 | https://www.womensweekly.com.au/news/crop-circles-australia-tully/ | 200 |
| S19 | https://circlemakers.org/new_documents.html | 200 |

`sources` 裡仍然沒有 S14b（`la2.html`）。`claims.md` 的 c28 已經照第一輪第 18 條補上它了（我確認了），
但 `video.json` 的 `sources[]` 只有 19 筆、只列 `la.html`。這一點見文末「仍然要改的」第 3 條。

## 第一輪 16 條改動：逐條重判

全部 16 條都已經套用，字句與第一輪開的處方一字不差（我逐條比對了行 id 與文字），單位數也和第一輪
預估的完全一致。**15 條我判「現在這樣站得住」，1 條（第 1 條裡的 `cl7y`）判「還要再改一個詞」。**

| # | 輕重 | 位置 | 現在的字 | 來源句子 | 重判 |
|---|---|---|---|---|---|
| 1a | 重 | `cl7zb` | 做了十幾年之後，紀錄沒有把這一點講定。(17) | 三個起算：S1「for the past 13 years」（S1 自己從 1978 起算）／S13「spent 14 years」／S6「his idea in 1976」＋S19「June 1976」＝15 年。S4 另有「a 15-year duel」。四個讀法都落在「十幾年」裡 | **CONFIRMED**。而且它不再把任何一家的說法當成全片的答案 |
| 1b | 重 | `cl7y` | 為什麼開口，時代雜誌寫是為了那筆經費。(17) | S1：「It was only **after** circle enthusiasts began seeking government funding **that** the two jovial con men decided to admit to the hoax.」 | **CHANGED（還要改）**。S1 寫的是「在那之後才決定承認」——一個觸發，不是一個目的。中文的「為了 X」最自然的讀法是「為了得到 X」，聽起來會變成兩個人開口是想要那筆錢，剛好和紀錄相反；而且前一章剛講完「愛好者向政府要經費」，這個誤讀是活的。改法見文末第 1 條 |
| 1c | 重 | `loops[3].what` | 那筆研究經費在兩種紀錄裡的位置 | 同上 | **CONFIRMED**。不再預設因果 |
| 2 | 重 | `outro.data.lines[0]` | 一塊木板，兩個人，十幾年 | 同 1a | **CONFIRMED**。與 `cl7zb` 一致。`how-many-stats` 卡仍保留「持續 13 年」，但它標在 TIME 那一欄底下（`{"label":"TIME","note":"1991 年；持續 13 年"}`），有出處，不衝突 |
| 3 | 重 | `cl1f`＋`nine-metres` 卡 `sub`＋說明欄第一段 | 照圈內人的記述，那是拴畫框店後門的鐵棒。(18)／圈內人的記述：一根鐵棒，一個晚上／提著一根鐵棒走進麥田（圈內人的記述） | S19（單源，圈內人自己的網站）：「Using a heavy iron bar - normally employed to secure the rear doors of Doug's picture-framing gallery - they swirled a simple circle, about 30 feet across」。我另外確認：**S6 那篇訃聞（同一位作者 Rob Irving）寫第一個圓時完全沒有提工具**，只有「laid down a simple circle, 30ft (9m) across」 | **CONFIRMED**。三個地方都標了出處。`cl1e`「道格手上提著一根鐵棒。」仍是無主的，但下一句隔四秒就把出處補上，聽得過去 |
| 4 | 重 | `cl3b` | 一位氣象學者提出一個天氣的解釋。(15) | S4「Terence Meaden, then a **meteorologist** and physicist」；S1 他的團隊主張那個天氣現象是「**often** responsible」。我把 S1、S4 兩篇都重讀一遍，**沒有一句寫他說過「那不是人做的」**；S4 反而寫他後來「conceded that these straight-line designs … were man-made」 | **CONFIRMED**。而且它不再和同一章的 `cl3m` 自打嘴巴 |
| 5 | 重 | `cl4h` | 然後記者去通知一個人。(10) | S1：記者 Graham Brough「had **alerted** Delgado to the latest apparition」並在田裡「**introduced** him to」兩人。怎麼通知的，S1 沒寫 | **CONFIRMED**。而且順序對：S1 的 Delgado 是被通知來看「the latest apparition」，圈是先做好的 |
| 6 | 中 | `cl6i` | 複雜的圖形，最多有兩千個獨立的形狀。(16) | S4 兩處：「featuring **up to** 2000 individual shapes」「which can feature **up to** 2000 individual shapes」 | **CONFIRMED**。和 `cl3t` 處理 S1「as many as」的方式（也是「最多」）一致 |
| 7 | 中 | `cl7l` | 夏天八成五到九成的生意，都跟麥田圈有關。(18) | S13：「**Around 85 to 90 per cent** of our custom during the summer months is connected to crop circles」 | **CONFIRMED**。下緣回到八成五。原文的「Around」還是沒有，但「八成五到九成」本身是個區間，而且 `cl7k` 已經把它標成「一位遊客中心的職員說」，不要求再改 |
| 8 | 中 | `cl5r` | 圖形是前一晚做的，三個人，約兩小時四十五分。(19) | S14b（第二頁）：「It was made the previous night, by three people, in **about** two and three-quarters hours, starting around 2:45 am」 | **CONFIRMED**。「約」回來了，換算（2¾ 小時＝兩小時四十五分）也對 |
| 9 | 中 | `cl2g` | 報紙把它叫做飛碟巢。(9) | S6：「Doug told Dave about the mysterious '**saucer nests**' he'd **read about in a newspaper**」；S16：「I saw an article in the Australian newspaper one day, about some circles in some reed and grass in Tully」；S18：「The so-called 'flying saucer nest' … was so peculiar it became national news」 | **CONFIRMED**。S18 單獨看只寫「所謂的」、沒寫是誰取的（第一輪否掉「當地人」是對的），但 S6 明確把這個詞放在報紙上，所以「報紙把它叫做」有來源。比第一版的「大家叫它」準 |
| 10 | 中 | 章名 1 | 星期五那一杯之後，他們提著鐵棒進麥田 | S19「One Friday night in June 1976」；S16「we used to go out on Friday evenings for a pint of beer」「it was Fridays' nights that we were doing the circles」；S6「They used to meet for a beer every Friday evening」；S4「As Bower and Chorley strolled home from the pub through the English countryside, they created their first imitation nest」 | **CONFIRMED**。「打烊」確實沒有來源，拿掉是對的；而且新章名不再和 `cl1a`「星期五傍晚」打架，S4 那句「從酒館走回家的路上做了第一個」正好支持「那一杯之後」 |
| 11 | 中 | `cl3j` | 兩個人想證明，這些圓跟天氣無關。(14) | S4：「the pair increased the number of circles in their formations, **hoping to demonstrate** that they were not weather-related」 | **CONFIRMED**。回到第一版的「想證明」 |
| 12 | 輕 | `cl4j` | 他盯著那片倒下的麥子。(10) | S1：「Delgado was **gazing** at a large area where the crops had been mysteriously flattened」 | **CONFIRMED**。沒有時間長度了 |
| 13 | 輕 | `cl4k` | 他站在田裡說，沒有人類做得出這個。(15) | S1：「marveled retired engineer Pat Delgado last week, **as he stood in a wheat field** near Sevenoaks. 'No human could have done this.'」 | **CONFIRMED**。「站起來」的多餘動作沒了，而且前一句已改成「盯著」，兩句不再重複「站」 |
| 14 | 輕 | `cl2d` | 他曾經移民澳洲，住了好幾年才回英國。(16) | S6：1976 年時「**18 years earlier**」他和妻子 Ilene 搭 £10 assisted passage 去澳洲（即約 1958 年；他 1924-06-25 生，當時 34 歲，1948 年結婚已十年），「returned to Hampshire in 1968」；S16：「it was **eight and a half years**」 | **CONFIRMED**。「年輕時」拿掉是對的（34 歲、已婚十年）。兩源的居留長度（8.5 年 vs 約 10 年）與回國年份（1966 vs 1968）不一致，旁白不給數字正好避開 |
| 15 | 輕 | `cl7c` | 二〇一七年，約六十公尺寬的圈壓掉兩英畝小麥。(20) | S10：「The crop circle is **about** 60m wide and covers **about** two acres of quality milling wheat」；同頁日期 16 August 2017 | **CONFIRMED**（達到第一輪開的「至少補一個」）。原文第二個「about」還是沒有，可選的收緊見文末第 2 條 |
| 16 | 輕 | `forty-five-minutes` 卡 `text` | 約 45 分鐘 | S14：「flew over the field at about 5:30 pm that day and again **about** 45 minutes later」 | **CONFIRMED**。卡片上的大字有「約」了。但**旁白 `cl5n`「四十五分鐘後再飛過，圖形就在那裡了。」還是沒有「約」**——卡片不會被唸出來，聽的人拿到的是精確數字。這是第一版就有的寫法（v1 `dmiu` 同字），不是這一版新長出來的，所以我不要求改，記在文末第 2 條 |

### 第一輪的兩筆 `claims.md` 記帳

| # | 內容 | 重判 |
|---|---|---|
| 18 | c28 補上 `la2.html` | **已套用**。c28 現在兩個網址都列，並寫明「Dickinson 那一段原話在同一篇訪問的第二頁」。我照 c28 現在的網址去查，兩頁都開得到，那句話確實在第二頁。另外 c26 的場景欄也補進了 `harder-and-paid`（第一輪順手提的） |
| 19 | c6 的「約 30 呎」 | **已套用，而且兩邊都對了**。見下面第 5 項 |

## 第 2 項：片尾只用耳朵聽，兩種說法都掛了名字嗎

只聽聲音（含配音版，卡片不會被唸出來），片尾的順序是：

| 行 | 聽到的字 | 出處有沒有唸出來 |
|---|---|---|
| `cl7x` | 還記得那筆研究經費嗎？ | — （回扣第 3 章） |
| `cl7y` | 為什麼開口，**時代雜誌寫**是為了那筆經費。 | ✅ 時代雜誌 |
| `cl7z` | **一篇訃聞寫**，公開是戴夫的主意。 | ✅ 訃聞 |
| `cl7zb` | 做了十幾年之後，**紀錄沒有把這一點講定**。 | ✅ 明說未結 |

**兩種說法都在聲音裡掛了名字，而且片尾明說紀錄沒有把這一點講定。**第一輪指出的那個毛病
（「時代雜誌那一種從頭到尾沒有被標出來，最後一句聽起來就是結論」）在聲音軌上已經不存在了。
配音版同樣成立：兩個出處（「時代雜誌」「一篇訃聞」）都是旁白字串，不靠卡片。

啟動說明要我特別判這兩句「是不是照原文寫的」：

- **「一篇訃聞寫，公開是戴夫的主意。」照原文，判 CONFIRMED。**
  S6（Fortean Times 371 訃聞）：「Doug regretted admitting having made crop circles. Not making them,
  but telling people about it. **This was not his choice but Dave's**, and Doug recognised the power of
  mystery…」。「This」指的正是「telling people about it」＝公開；「不是他的選擇，是戴夫的」＝
  「是戴夫的主意」。來源類型（訃聞）也對。
- **「時代雜誌寫是為了那筆經費。」不是照原文，判 CHANGED。**
  S1 的原句是「It was only **after** circle enthusiasts began seeking government funding **that** the two
  jovial con men decided to admit to the hoax.」——那筆經費是**觸發**（愛好者開口要錢之後，他們才決定
  承認），不是**目的**。中文「為了 X」最自然的讀法是「為了得到 X」，聽起來會變成兩個人開口是想要
  那筆錢；更麻煩的是這一句前面幾章剛講過「愛好者甚至開始向政府要研究經費」，所以聽眾手上正好有
  一個現成的誤解材料。
  有意思的是，**`two-accounts` 卡的左欄反而寫對了**：「愛好者開始向政府要研究經費」／
  「之後兩個人才決定承認」——那就是 S1 的句構。看得到卡片的人不會誤解，只聽聲音的人會。
  這正是第一輪自己定義的那個毛病（聲音軌比卡片少一層），只是這次出在它開的處方上。
  而且**第一版自己寫對過**：`../curio-l08/video.json` 的 `dj8u`
  是「時代雜誌寫，是因為愛好者開始向政府要經費。」（19 單位），用的是「因為」。
  第一輪的括號備案「時代雜誌寫，是那筆經費讓他們決定承認。」(17) 也是對的——它開的主方案偏偏是
  「為了」那一版。改法見文末第 1 條。

### 五個地方還對得上嗎

| 地方 | 現在 | 對得上？ |
|---|---|---|
| `cl7y` | 時代雜誌那一種，掛名 | ✅（措辭要改一個詞） |
| `cl7z` | 訃聞那一種，掛名 | ✅ |
| `two-accounts` 卡 | 左＝時代雜誌 1991、右＝訃聞 2018、verdict「紀錄沒有把這一點講定」、source 兩筆 | ✅ 與兩句旁白一一對應 |
| `loops[3].what` | 那筆研究經費在兩種紀錄裡的位置 | ✅ 不再預設因果；payoff `cl7x` 之後確實給出兩種紀錄 |
| 標題問句 | 為什麼 1991 年兩個英國老先生，承認麥田圈是他們做的？ | ✅ 全片給的答案是「紀錄有兩種說法，沒有講定」，兩種候選答案都講了。問句沒有被騙式使用 |

一個輕微的觀察（不要求改）：`two-accounts` 卡的 verdict 字串「紀錄沒有把這一點講定」與下一個場景
`cl7zb` 的後半字字相同。對只聽聲音的人這是第一次聽到（卡片不唸），這正是這樣寫的理由；對看畫面的人
則是前一幕剛讀過、下一幕立刻聽到一模一樣的話。我判這是值得付的代價——要讓「未結」進到聲音軌，
就得說這句話——不建議動。

## 第 3 項：七個章名（第一輪沒有抽，這裡補上）

章名會進 YouTube 的章節列表，觀眾會讀到，所以當公開的字查。七個我都對了章內容與來源。

| # | 場景 | 章名 | 涵蓋場景 | 來源 | 判定 |
|---|---|---|---|---|---|
| 1 | `friday-evening` | 星期五那一杯之後，他們提著鐵棒進麥田 | 0–11 | 星期五＋那一杯：S6「a beer every Friday evening」、S16「Friday evenings for a pint of beer」、S19「One Friday night in June 1976」；那一杯之後進田：S4「As Bower and Chorley strolled home from the pub … they created their first imitation nest」；鐵棒：S19（單源）；麥田：S19「snuck out into a Hampshire wheat field」 | **CONFIRMED**。章內容（酒館→翻過柵門→鐵棒→壓圓→九公尺→回家→三年沒人注意）完全對上。與 `cl1a`「星期五傍晚」也一致 |
| 2 | `back-again` | 那個東西，又回來了 | 12–30 | S6：「'**The Return of the Thing**', ran the headline.」（1980 年 Westbury 那篇報導的標題） | **CONFIRMED**。這是引語當標題，章末的 `the-thing-returns` 卡（kicker「一九八〇年，一家報紙的標題」、sub「一篇訃聞的轉述」）與 `cl2v`「那篇報導的標題，後來被一篇訃聞轉述。」把出處講清楚了——而且「被訃聞轉述」這個說法精確：1980 年的標題正是透過 2018 年的訃聞才傳到我們手上 |
| 3 | `researchers-arrive` | 氣象學家說，那是帶電的旋風 | 31–50 | 氣象學家：S4「Terence Meaden, then a **meteorologist** and physicist」；帶電的旋風：S1「when whirling columns of air pick up **electrically charged** matter, flatten the crops below」＋S4「an electromagneto-hydrodynamic '**plasma vortex**'」 | **CONFIRMED**。章名有掛「氣象學家說」，是他提的假說，不是全片的斷言；章內容（研究者進場→天氣解釋→電漿渦旋→專書→加圓→直線→他承認→物理學家）對上 |
| 4 | `they-decide-to-talk` | 專家看完那個圓，說人類做不出來 | 51–70 | S1「'No human could have done this.'」「Delgado was gazing at a large area…」「as he stood in a wheat field」；S2 稱他「a **self-styled expert** on the crop circle phenomena」「the author and expert」 | **CONFIRMED**。「專家」用 S2 的字；話是引語且掛了「專家說」。章內容（九月決定說出來→肯特郡→當面做一個圈→專家來→那句話→兩人就在他後面→小報頭條→漢普郡再做一次→改口）對上 |
| 5 | `already-others` | 那年夏天，田裡已經有別人 | 71–90 | S6：「By **summer 1991**, others had joined in … way beyond Doug and Dave's capabilities」；S13：Dickinson 的第一個圈「was the **summer of 1991**, just months before … came out」 | **CONFIRMED**。「那年」接的是第 4 章的 1991 年九月，時序對。章內容（別人已經在做→第二波→搞笑諾貝爾→巨石陣旁的四十五分鐘→194 個圓）對上 |
| 6 | `harder-and-paid` | 有人開始付錢，請人去壓麥田圈 | 91–105 | S13：Circlemakers 公開接案，「clients including Weetabix, O2, Big Brother, Mitsubishi, and Thompson Holidays」、「the paper **paid the farmer £6,000**」；S4：BBC 拍 100 圓圖形 | **CONFIRMED**，與章的第一句 `cl6a` 同義。小觀察：這一章的後半（麥稈節、電磁輻射、批評者）章名沒有涵蓋到，但章名是標題不是目錄，不算錯 |
| 7 | `fined-one-hundred` | 每一個圈底下，都是別人的收成 | 106–124 | S10（警方）：「The damage caused means a loss in revenue to the farmer and landowner」、「covers about two acres of quality milling wheat」；S12：「Farmers lost £30,000 in income」；S13：委託案是**付錢給農夫**（「paid the farmer £6,000」、「a farmer paid £500 apiece for two fields」），作物仍然是農夫的 | **CONFIRMED**。我特別查了「每一個」這個全稱說法站不站得住：就算是付了錢的商業委託，被壓掉的也還是農夫的作物，所以「底下是別人的收成」在來源裡沒有例外（來源裡沒有任何一個圈是做在自己田裡的）。章內容（罰金→刑事毀損→不是邀請→觀光的另一面→那筆帳→損失→兩位老先生的下場→片尾）對上 |

**七個章名全部 CONFIRMED。**第一輪把章名 1 從「酒吧打烊」改成「星期五那一杯之後」是對的：
「打烊」在二十個來源裡一個字都沒有，而且和 `cl1a`「星期五傍晚」互相矛盾。

唯一值得記下的：章名 1 的「鐵棒」只有 S19 一個來源（圈內人自己的網站），而章名是全片唯一沒辦法
掛出處的字串。旁白（`cl1f`）、卡片（`nine-metres` 的 sub）與說明欄三處都標了「圈內人的記述」，
縮圖用的是來自 S1 的「一塊木板」而不是鐵棒，所以我判這樣的分配可以接受，不要求改章名。

## 第 4 項：第一輪 29 列 CONFIRMED 的抽樣

抽 13 列（45%，要求是三分之一＝10）。**挑的理由**：我不隨機抽，專挑風險高的——
(a) 會上卡片的數字（觀眾讀得到，錯了最難救）、(b) 單一來源的數字、(c) 需要換算或對日期的、
(d) 引語、(e) 片尾那段改寫倚賴的事實。全部回到來源重讀，沒有一列靠第一輪的轉述。

| 第一輪列 | 挑它的理由 | 位置 | 來源句子 | 重判 |
|---|---|---|---|---|
| c1 | 單源年齡＋上卡片 | `cl4e`、`their-ages` 卡 | S1「two land-scape painters, **David Chorley, 62**, and **Douglas Bower, 67**」；S6「opened a gallery and picture-framing studio」 | **CONFIRMED**。而且人沒有對調（道格 67、戴夫 62），卡片 sub 標「時代雜誌 1991 年的報導」，Chorley 的年齡確實只有 S1 一源 |
| c4 | 整段「十幾年」推論的地基 | `cl1a`、`cl2a2`、`cl1i`、`nine-metres` 卡 | S6「his idea in **1976**」「a simple circle, **30ft (9m)** across」；S19「One Friday night in **June 1976**」「**about** 30 feet across」；S1「conceived their hoax in **1978**」；S5「since the **late 1970s**」 | **CONFIRMED**。兩個年份都講了（`cl2a2`），卡片的「大約 9 公尺」和 S19 的「about 30 feet」對得上 |
| c9 | 日期＋引語，兩者都上卡片 | `cl4d`、`cl4q`、`conned-the-world` 卡 | S17「**September 9, 1991**: … the British tabloid **Today** announced」；S2「According to Today, which broke the story with the headline '**Men Who Conned the World**'」 | **CONFIRMED**。卡片 sub 寫「紐約時報 1991-09-10 的轉述」，而標題確實是透過紐時轉述的 |
| c15 | 單源大數字，上大字卡 | `cl3h`、`fifty-thousand` 卡 | S1「has co-authored a book called Circular Evidence with another believer, Colin Andrews. It has sold **more than 50,000 copies**」 | **CONFIRMED**。「五萬多本」對應「more than 50,000」 |
| c18 | 三個數字擠在一張卡上，最容易互撞 | `cl3r`–`cl3t`、`how-many-stats` 卡 | S5「more than **200** crop circles since the late 1970s」；S4「confessed to making **250** formations」；S1「as many as **25 to 30** new circles each growing season」 | **CONFIRMED**。三個數字各自掛到大英百科／Physics World／TIME，旁白不給單一答案。S4 的 250 是「formations（圖形）」不是圓，卡片把它和大英百科的「圓」並排在「做了幾個」底下——`claims.md` c18 已經寫明這個設計，我同意保留 |
| c21 | 時序風險（來源寫「同一天」） | `cl4r`–`cl4t` | S2「**Late today**, the two men demonstrated their craft before reporters in a field in Hampshire」「Colin Andrews … 'There is nothing here to impress us at all except **two very fit 60-year-olds**'」 | **CONFIRMED**。旁白說「之後」而不是「同一天」，比來源保守；引語照原文 |
| c23 | 引語＋年份，上大字卡 | `cl5f`、`cl5g`、`award-reason` 卡 | S7「**The 1992 Ig Nobel Prize Winners** … PHYSICS: David Chorley and Doug Bower, lions of low-energy physics, for their circular contributions to field theory based on the **geometrical destruction of English crops**」 | **CONFIRMED**。1991＋1＝1992，「隔年」對；理由照原文譯 |
| c26 | 全片唯一的除法換算 | `cl6d`、`cl6e`、`the-fee` 卡 | S13「the paper paid the farmer **£6,000** for the equivalent of **around £100** worth of crops」 | **CONFIRMED**。6,000÷100＝60，旁白保留「大概」。卡片兩個原始數字都在，source 標「製作者自述」。順帶確認：S13 另有一筆「£30,000 in four weeks」的觀光傳聞，全片**沒有**用它，所以 `cl7h` 的三萬英鎊（衛報的損失）不會和它撞 |
| c29 | 數字＋日期要對月 | `cl5v`、`one-nine-four` 卡 | S4「One evening in **July 1996** … That same evening, **194** 'crop circles' … appeared in a nearby field at Windmill Hill」；S14「less than a month later, on **July 29** … totalling **194** individual circles」 | **CONFIRMED**。兩源都落在 1996 年七月，「同一個月」沒有超出來源 |
| c32 | 全片的知識論底線 | `cl6o`、`cl6p` | S4「neither Levengood nor Haselhoff's work has ever been **reconfirmed or disproved** by subsequent studies」 | **CONFIRMED**。「沒有被證實，也沒有被推翻」照原文。`cl6o`「最老實」是評語 |
| c35 | 三個數字一張卡 | `cl7g`–`cl7i`、`the-losses` 卡 | S12「More than **40 football pitches**' worth of arable land has been affected by crop circles **in England since 2018** … Farmers lost **£30,000** in income between **2018 and 2022** as a result of **92** crop circles」 | **CONFIRMED**。卡片標題寫明「英格蘭」與「衛報的估算」。足球場那個數字原文是「since 2018」無下限，但該文發表於 2022-09-24，等於 2018–2022，放在同一張卡上不算超出 |
| c38 | 片尾那段改寫倚賴它 | `cl7r`–`cl7t` | S6「born Horton Heath, Hampshire, 25 June 1924; **died West End, Hampshire, 21 July 2018, aged 94**」「Doug regretted admitting having made crop circles. Not making them, but **telling people about it**」；S19「Doug, who **died in 2018 aged 94**」 | **CONFIRMED**（兩源）。戴夫的卒年照舊不講，對 |
| M9 | 19 筆來源可不可達 | `sources[]` | 我自己重抓一次 | **CONFIRMED**，19 個網址加 S14b 共 20 個全部 200。S8、S11 仍然沒有任何一句靠它們（我讀了兩篇：S8 的 NFU 原話、S11 的 £5 誠實箱，旁白都沒有用；`cl7e` 的水桶來自 S10 的 Klindt 一家，沒有和 S11 的誠實箱混起來） |

**13 列全部維持 CONFIRMED，沒有一列翻盤。**

## 第 5 項：c6 的「約 30 呎」，兩邊都對了嗎

是的，兩邊都對：

- **來源**：S18 的原文是「tall reeds were now woven into a **30-foot diameter** circle」——沒有「約」。
  （同頁另一處：「where the reeds had been **flattened** and woven to become the saucer nest」。）
- **旁白 `cl2f`**：「潟湖的蘆葦，被壓成一個三十呎的圓。」——照原文的硬數字，**沒有被改錯方向**。
- **`claims.md` c6**：現在寫「S18：香蕉農、潟湖蘆葦『woven into a 30-foot diameter circle』，
  **原文沒有「約」**，旁白 `cl2f` 說「三十呎」」——記帳改對了，第一輪擔心的事（下一輪照清單把旁白
  改鬆）不會發生。

順帶確認另一個 30 呎不要混淆：S19 講 1976 年第一個圓時寫的是「**about** 30 feet across」（有「約」），
而 `nine-metres` 卡寫「大約 9 公尺」、`cl1i` 寫「直徑大約九公尺」——這一個有「約」是對的。
**兩個三十呎，一個有「約」一個沒有，現在各自跟著自己的來源，沒有交叉污染。**

## 第 6 項：套用之後有沒有弄壞第一輪已經通過的東西

| 檢查 | 結果 |
|---|---|
| 四條 `loops` 的 payoff 有沒有給聽眾手上還沒有的事實 | **四條都有。** [0] `cl1e`→`cl2i`：payoff 下一句 `cl2j` 給「鐵棒換成一塊木板」，新的。[1] `cl1g`→`cl2b`：下一句起給澳洲報紙與飛碟巢，新的。[2] `cl2q`→`cl7a`：下面給 2017 年的圈、水桶、衛報的損失，新的。[3] `cl3v`→`cl7x`：下面給**訃聞那一種說法**（公開是戴夫的主意）與「紀錄沒有講定」，都是新的——改完之後這一條**仍然**在付帳，付的是「紀錄是分裂的」這個事實，不是重複觀眾已有的答案 |
| 同一個數字有沒有被說兩次 | **沒有。**我掃了全部 144 句的 30 個數字樣式，每一個都只出現一次。唯一的疑似命中是字串「九十四」在 `cl5v`（一百九十四**個圓**）與 `cl7s`（九十**四歲**）各一次——是 194 和 94 兩個不同的數字共用字串，單位也不同，不是重複。「十幾年」旁白說一次（`cl7zb`）、`outro` 卡寫一次（同時出現、互相強化），「一百英鎊」旁白只在 2000 年的罰金出現一次（作物的約 £100 只在卡片上），都照 `claims.md` c26 的設計 |
| 七章的第一句有沒有接上一句 | **七句都接得上，而且沒有一句被這 16 條改動碰到**（改的是 `cl7zb`／`cl7y`／`cl1e-f`／`cl3b`／`cl4h`／`cl4j`／`cl4k`／`cl2d`／`cl6i`／`cl5r`／`cl3j`／`cl2g`／`cl7l`／`cl7c` 與章名 1、兩張卡、說明欄；章首句是 `cl1a`／`cl2a`／`cl3a`／`cl4a`／`cl5b`／`cl6a`／`cl7o`，一句都沒動）。逐條：第 2 章 `cl2a`「他們沒有停」接第 1 章「沒有人注意到」的後果；第 3 章 `cl3a`「報導一登出來，開始有人認真研究」直接接 `cl2w` 的 1980 年標題；第 4 章 `cl4a`「那年九月，兩個人決定說出來」接 `cl3u`「愛好者甚至開始向政府要研究經費」——這正是 S1 的時序，而且只給時序、不宣稱因果；第 5 章 `cl5b`「田裡已經不只他們兩個」回答 `cl4x`「他們把那塊木板帶去加拿大了嗎？」；第 6 章 `cl6a` 接 `cl5v` 的 194 個圓；第 7 章 `cl7o` 接 `cl6q`「有一件事一直沒有人算」（唯一的清算就是那張一百英鎊的罰單） |
| 章名 1 改了，還配得上 `cl1a` 嗎 | **配得上。**舊章名「酒吧打烊」和 `cl1a`「星期五傍晚」互相矛盾，新章名「星期五那一杯之後」不矛盾 |
| 單位數 | 144 句，最長 22（`cl2a2`，未改動），合計 2,106 單位（改動淨增 20）。**16 條改動的單位數與第一輪預估的一字不差**，全部在這一集自己的 22 上限內，離 lint 的 40 很遠 |
| 其他位置 | `assets` 是空陣列（全片插圖都是 AI 生成，說明欄第四段已聲明），所以沒有照片說明要查。`characters` 空、`look` 用 `cute-mystery` 預設、`say` 零個（旁白沒有拉丁字母）。`NOTES.md` 的改動表（第 146–149 行）與 `video.json` 現在的字一致，第一輪指出的那個結構說明（「`outro` 第一句第一次說出答案」）也已經改寫成「`outro` 第一句說紀錄拒絕了什麼」，文件沒有留下矛盾 |

### 第一輪交代的功課：限定語還有沒有第六處

第一輪說這一版把第一版的限定語弄掉了五處（鐵棒的出處、想證明、最多的、約 2 小時 45 分、十幾年），
要我逐句對一遍確認沒有第六處。我把第一版 114 個場景／134 句全部抽出來和這一版對過。
**答案：有，兩處**——一處是第一版就寫對、這一版新長出來的，一處是第一輪自己的處方帶進來的。

1. **`cl1k`／說明欄的「整整三年」**（第一輪列為第 17 條「記下來，不要求改」）。
   第一版 `35mn` 寫的是「可是**頭三年**，根本沒有人注意到他們的圈。」，這一版改成
   「之後**整整**三年，沒有人注意到那些圓。」。S1 的原文是「this and other forays during the next
   three years went unnoticed」——按 S1 自己的起算（1978＋3＝1981）確實剛好三年，所以我同意
   第一輪判 CONFIRMED；但「整整」是這一版新加的強調，而這一集自己在 `cl2a2` 告訴觀眾起算年份有兩說
   （1976 起算到 `cl2u` 的「一九八〇年前後」是四年）。同一個毛病第一輪在片尾的「十三年」上判了「重」，
   這裡建議用同樣的尺。改法見文末第 2 條。
2. **`cl7y` 的「為了」**（見第 2 項）。第一版 `dj8u` 寫的是「時代雜誌寫，是**因為**愛好者開始向政府要
   經費。」——用「因為」，而且把觸發寫出來。這一版現在的「是**為了**那筆經費」比第一版和來源都鬆。
   這是第一輪的處方帶進來的，不是撰稿人的錯。

除此之外，第一版所有帶限定語或出處的句子（「大約九公尺」「照道格本人的說法」「仍可能是大氣現象」
「每一季最多」「大概只值」「大約是一分鐘」「流傳的說法是」「所以有人說」「超過四十個足球場」
「圈內人想像他會說」）在這一版都還在，而且第一版的 `ijkv`（把觀察和推測併成一句）這一版拆成
`cl6k`／`cl6l` 兩句，比第一版更乾淨。**第一版的 45 分鐘卡其實也寫「45 分鐘」沒有「約」，
這一版的卡片比第一版更準。**

## 仍然要改的

### 1.（必改，一個詞）`cl7y`：把「為了」換成因果

- **現在**：`cl7y`「為什麼開口，時代雜誌寫是為了那筆經費。」(17)
- **問題**：S1 寫的是觸發（「It was only **after** circle enthusiasts began seeking government funding
  **that** the two … decided to admit」），不是目的。中文的「為了 X」最自然的讀法是「為了得到 X」，
  只聽聲音的人（含配音版）會聽成兩個人開口是想要那筆錢；而且前面幾章剛鋪了「愛好者向政府要經費」，
  誤讀的材料就在手上。看得到 `two-accounts` 卡的人不會誤解（左欄寫的是「愛好者開始向政府要研究
  經費／之後兩個人才決定承認」，正是 S1 的句構），聲音軌比卡片少一層——這正是第一輪要修的那個毛病。
- **應該改成**（任一，都在上限內、都保留 `cl7x` 的回扣）：
  - 最小改動，長度完全不變：**「為什麼開口，時代雜誌寫是因為那筆經費。」(17)**
  - 把觸發講出來、完全沒有歧義：「為什麼開口，時代雜誌寫是因為有人要經費。」(18)
  - 第一輪自己的括號備案，也是對的：「時代雜誌寫，是那筆經費讓他們決定承認。」(17)
    （這一版會少掉「為什麼開口」這個框，`cl7z` 的「公開是…」還撐得住，但兩句是不是同一個問題的
    兩個答案就要靠聽眾自己接。）
- 我的建議是第一個：一個詞、長度不變、不動節奏，`cl7z`／卡片／`loops[3]`／標題都不用跟著動。

### 2.（可選，輕）三處概數可以更貼原文

這三處都不是這一版新長出來的毛病（前兩處第一版就這樣，第三處是 S1 自己的算法），所以我不把它們
列為必改；要收緊的話一次收完比較省事。

| 位置 | 現在 | 原文 | 建議 |
|---|---|---|---|
| `cl1k` | 之後整整三年，沒有人注意到那些圓。(15) | S1「during the next three years went unnoticed」（第一版寫「頭三年」） | 「之後三年，沒有人注意到那些圓。」(13)；說明欄第一段「之後整整三年，沒有人注意到。」同樣拿掉「整整」 |
| `cl5n` | 四十五分鐘後再飛過，圖形就在那裡了。(16) | S14「again **about** 45 minutes later」（卡片已經改成「約 45 分鐘」，旁白還沒有） | 「約四十五分鐘後再飛過，圖形就在那裡了。」(17) |
| `cl7c` | 二〇一七年，約六十公尺寬的圈壓掉兩英畝小麥。(20) | S10 兩個數字前面都有「about」 | 「二〇一七年，約六十公尺寬的圈壓掉約兩英畝小麥。」(21) |

### 3.（可選，記帳）`sources[]` 少 S14b

`claims.md` 的 c28 已經照第一輪第 18 條補上 `https://circlemakers.org/la2.html`，但 `video.json` 的
`sources[]` 還是 19 筆、只列 `la.html`。`cl5r`／`cl5s`／`cl5t` 三句旁白依據的 Dickinson 原話在第二頁，
說明欄的參考資料會帶一個查不到那句話的網址。建議把 S14b 加進 `sources[]`（我實測 200），
或把 S14 那一筆的 `title` 註明「分兩頁」。同一時間可以決定要不要拿掉 S8、S11——這一版沒有任何一句
靠它們（第一輪已經提過，我重讀兩篇後確認）。

## 懷疑但沒有要求改的

- `cl1e`「道格手上提著一根鐵棒。」仍是無主句，出處在下一句 `cl1f`。鐵棒只有 S19 一源（圈內人網站），
  而 S6 同一位作者寫第一個圓時沒有提工具。四秒後補出處我判可以接受，而且卡片、說明欄都標了，
  縮圖用的是有 S1 撐著的「一塊木板」。章名無法掛出處，見第 3 項末段。
- `cl7l`「夏天八成五到九成」沒有把 S13 的「Around」譯出來。區間本身帶概數意味，`cl7k` 也標了說話人，
  不要求改。
- `cl5p`「兩邊的說法，都出自同一篇訪問。」嚴格說，醫生那一面是 Lindemann 在文章裡**轉述**的既有報導
  （「it was reported that a doctor…」），不是在那次訪問裡說的；Dickinson 那一面才是訪問內容。
  兩面確實都只透過這一篇文章到我們手上，`cl5k` 也已經把醫生那一面標成「流傳的版本」，所以我判
  站得住；真要精確可以寫「都出自同一篇報導」。
- `cl5t`「他沒有說自己就是做的人。」在巨石陣那個圖形上完全正確（S14「They were made by people.
  Definitely.」「Do you know who?」「Yes.」）。但 S14b 同一篇裡他說「I myself made several dozen of
  them」——他承認做過好幾十個大圖形。前後三句都在講巨石陣那一個，聽起來不會誤會，但剪接時若把
  `the-makers-version` 到 `never-claimed-it` 拆開，這一句要重看。
- `cl2j`「鐵棒換成一塊木板」：沒有一條來源明寫「換」。另外 S2 與 S17 都寫「**two** wooden boards」，
  S1 寫「a 4-ft. long wooden plank」，S13 的 Bower 自己說「planks and bits of rope」。旁白跟著 S1 的
  一塊木板（縮圖、`cl4x`、`cl7q` 都倚賴「那塊木板」這個單數意象）。一對二，但 S1 是最詳細的操作
  描述，保留；記在這裡供下一輪。
- `cl6m`「統計和取樣都有問題」：S15 列的四項裡最接近「取樣」的是「the arbitrary discarding of
  unwanted results」（任意丟掉不想要的結果）。對應得鬆但讀得通（第一版同字），不要求改。
- `cl3s`「他們承認做了兩百五十個」：S4 的 250 是 formations（圖形）不是圓，卡片把它和大英百科的
  「兩百多個圓」並排。`claims.md` c18 已經寫明，保留。
- S4 另有一句「two unassuming men in their sixties declared that they had been creating crop circles for
  **more than 25 years**」——同一段前面又寫他們是「mid-1970s」開始的，自相矛盾，顯然是 S4 的筆誤。
  不採，也不影響「十幾年」（S1 的 13、S13 的 14、S6／S19 的 15、S4 自己的「15-year duel」四個讀法
  都落在十幾年裡）。
- `cl6o`「一位物理學者的結論最老實」是評語，`claims.md` 的〈不是來源主張的句子〉沒有收它
  （c32 的場景欄收了這個場景）。可以考慮和 `my-own-view` 一樣標成意見。
- `two-accounts` 卡的 verdict 與 `cl7zb` 後半字字相同（見第 2 項末段）。為了讓「未結」進到聲音軌，
  這個回音是值得付的代價，不建議動。
- 會過期的事實：沒有。我看到的頁面日期：Physics World 2011-08-04、Fortean Times 371（印刷日
  30/08/2018）、Independent 2004-07-06、TIME 1991-09-23（頁尾自述 pg 59）、紐約時報 1991-09-10、
  衛報 2022-09-24、FW 2017-08-16、FW 2000-11-07、This Is Wiltshire 2000-11-07、CICAP 2005-06-21、
  AWW（網路版）、Britannica 存檔 2025-11-11、Circlemakers 站上最新一則 NEWS UPDATE 16-12-2025。

## 摘要與結論

- **第一輪的 16 條改動全部套用，字句與處方一字不差，單位數也完全吻合。重判結果：15 條站得住
  （CONFIRMED），1 條還要改一個詞（`cl7y` 的「為了」→「因為」）。**另加的兩筆 `claims.md` 記帳
  （c28 補第二頁網址、c6 拿掉「約」）都套用了，而且 c6 的旁白與清單現在兩邊都對。
- **七個章名全部 CONFIRMED**，包括這一輪改掉的章名 1（「酒吧打烊」→「星期五那一杯之後」，
  「打烊」在二十個來源裡一個字都沒有，改對了）。
- **抽驗 13 列 CONFIRMED（45%），13 列全部維持，沒有一列翻盤。**挑的是上卡片的數字、單源數字、
  要換算或對日期的、引語，以及片尾改寫倚賴的事實。
- **片尾只用耳朵聽：兩種說法都掛了名字，片尾也明說紀錄沒有把這一點講定。**「一篇訃聞寫，公開是
  戴夫的主意」照 S6 原文（「This was not his choice but Dave's」），CONFIRMED；
  「時代雜誌寫是為了那筆經費」不照 S1 原文（S1 是「只有在…之後才決定承認」，是觸發不是目的），
  要改。第一版自己用的是「因為」，第一輪的括號備案也是對的。
- **第一輪指定的五個對齊點（`cl7y`、`cl7z`、`two-accounts` 卡、`loops[3]`、標題問句）現在互相對得上。**
- **套用改動沒有弄壞任何第一輪通過的東西**：四條 loops 都還在用新事實付帳（含改完的第 3 條）、
  沒有任何數字被說兩次、七章的第一句都還接得上（章首句一句都沒被動到）、最長句仍是 22 單位。
- **第一輪交代的「有沒有第六處掉了限定語」：有兩處**——`cl1k` 的「整整三年」（第一版寫「頭三年」，
  這一版新加的強調，第一輪已列為第 17 條記錄）與 `cl7y` 的「為了」（第一輪處方帶進來的）。
- 程序：沒有用網路搜尋（0 次）；沒有跑 git；沒有跑任何影片階段；沒有花錢；沒有動
  `video.json`／`claims.md`／`brief.md`／`NOTES.md`，只寫了這一個檔案。

**結論：改掉 `cl7y` 一個詞（「為了」→「因為」）之後，這一集可以進畫面與配音。**
除此之外沒有任何事實錯誤，沒有未標出處的流傳說法，沒有宣稱定論。第 2、3 條是可選的收緊
（三處概數、`sources[]` 補 S14b），不影響開拍；要做的話建議和 `cl7y` 一起做完，省一次往返。

**第三輪：不需要。**這一輪只要求改一條，遠低於「超過三條就再查一輪」的門檻。`cl7y` 改完以後，
套用的人請順手確認 `cl7z`（13）、`two-accounts` 卡與 `loops[3].what` 都不用跟著動——用上面第一個
建議的寫法，這三個地方確實都不用動。
