# curio-h01-v2 查核第三輪（開場預告）

- 查核 2026-10-13，Claude Opus 5.5（獨立查核代理，不是改寫開場的那一個）。`video.json` 一個字都沒動。
- 範圍：只查 `git diff HEAD -- video.json` 裡新增或改過的旁白（第 1 章與五句正文），以及第 1 章拿掉的句子
  有沒有讓別的句子、標題、說明欄、縮圖失去依據。對照 `claims.md`、`verify-1.md`、`verify-2.md`、
  `NOTES.md`〈開場預告 2026-10-13〉。另外自己重開 Austin 勘驗報告（maryceleste.net/survey.htm，第 37–44 段：
  劍在船長艙）與 Britannica（測深桿）。

## 改過或新增的句子

| id | 句子 | 結果 |
| --- | --- | --- |
| `mc1m` | 大副德沃划小艇過去，甲板上、舵邊都沒有人。 | OK（舊 `mc1e`＋`mc1f`，事實不變） |
| `mc1n` | 唯一的小艇不見了，船尾拖著一條斷掉的粗繩。 | OK（c39、c40） |
| `mc1o` | 而這，只是第一天。 | OK（不是事實主張） |
| `mc1p` | 船長床底下放著一把劍，後來被送去化驗。 | OK（c26 床下鞘內的劍；Austin 第 37、44 段：在船長艙；c33 化驗） |
| `mc1q` | 一八八四年，一篇沒有署名的小說寫了她，作者是誰？ | OK（c8 1884 年 1 月 Cornhill 匿名） |
| `mc1r` | 熱那亞的碼頭上，她載的酒精被一桶一桶數過。 | OK（c47 熱那亞卸貨；c13 貨是酒精） |
| `mc1s` | 一八八五年，一個新船長故意把她開上礁石。 | OK（c51 原文就是「為詐保故意駛上」；Parker 是 Briggs 之後的船長） |
| `mc3w` | 還有開頭說的那把劍，收在鞘裡，放在床底下。 | OK（開頭 `mc1p` 確實講了劍） |
| `mc5b` | 那個沒署名的作者，後來寫出了福爾摩斯。 | OK（c8、c9） |
| `mc6r` | 大副上船那天，甲板上還躺著一根量水深的桿子。 | **小問題**，見 P1 |
| `mc7b` | 開頭那次點數就在這時候：一千七百零一桶酒精。 | OK（開頭 `mc1r` 講了熱那亞那次點數；c47） |
| `mc7t` | 一八八五年那塊礁石，是新船長為了詐領保險開上去的。 | OK（c51） |

**P1 `mc6r`**：c24 與兩輪查核的來源（Austin 第 49–50 段是 12-23 的勘驗；Britannica 只寫「discovered on deck」）
都沒有把桿子釘在「大副上船那天」。舊句只是「甲板上那根量水深的桿子」，日子是新加的。建議改成只用已查核的
Austin 原文（測深器就放在被拆開的幫浦旁邊）：

> 甲板上的幫浦旁邊，躺著一根量水深的桿子。

## 拿掉開場句的連帶影響

**P2 `mc1d`（沒改的句子，代詞指錯船）**：舊開場的順序是 `mc1b` 英國船長舉起望遠鏡 → `mc1c`「遠處那艘船的帆是歪的」
→ `mc1d`「她叫瑪麗賽勒斯特號」。`mc1c` 拿掉之後，`mc1d` 的「她」緊接在「一艘英國帆船」後面，聽起來像
英國船就叫瑪麗賽勒斯特號（其實英國船是 Dei Gratia，瑪麗賽勒斯特號是美國船）。建議：

> 望遠鏡裡那艘船叫瑪麗賽勒斯特號，船上有十個人。

其他拿掉的事（歪帆、前艙口與一公尺多的積水、「貨一桶都沒少」、測深桿首次出場、空吊架）沒有被任何留下的句子
當成「已經講過」：`mc7i` 的粗繩指向 `mc1n`、`mc6i`／`mc7n`／`mc5g` 指向正文；`mc6c` 的艙蓋、`mc7g` 的「艙裡有水」
本來就自己成立。標題、縮圖（「船在走／人沒了」→ `mc1l`、`mc1m`）不受影響；說明欄的「帆張著」「貨一桶都沒少」
仍有 `mc7l`、`mc6l`、`mc2p` 撐著。`shorts.json` 用到的場景都還在。

## 結論

12 句改過或新增的旁白：11 句 OK，1 句小問題（P1）；拿掉開場句造成 1 個代詞問題（P2）。沒有新的人名、數字或年份，
「故意」「唯一」都有 claims 原文。P1、P2 改完即可，不需要第四輪。i18n 三份仍待重譯（NOTES 已記）。

## 盲評修改查核 2026-10-13

- 查核 2026-10-13，Claude Opus 5.5（獨立查核代理，沒有寫過也沒有改過這份稿子）。`video.json` 一個字都沒動。
- 範圍：`NOTES.md`〈盲評修正 2026-10-13〉與〈盲評修正第二輪 2026-10-13〉列的每一句，加上 `git diff HEAD -- video.json`
  裡搬了位置的句子（`never-found`、`reef-1885`、`hoax-jury` 移進第 7 章，`miscalculation`…`both-have-holes` 成為第 8 章）。
- 當天重開的來源（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 ≥1.2 秒）：
  Austin 勘驗報告（maryceleste.net/survey.htm）、maryceleste.net/facts.htm、smithsonianmag（SM07）、americanheritage（AH）、
  skeptoid #289（SK）、Britannica（EB）。全部 200。

### 逐句

| id | 句子 | 結果 |
| --- | --- | --- |
| `mc1d` | 望遠鏡裡那艘船叫瑪麗賽勒斯特號，船上有十個人。 | OK（上一節 P2 的字一字不差） |
| `mc1q` | 到了一八八四年，一篇沒署名的小說寫了她，作者是誰？ | OK（c8） |
| `mc1r` | 更怪的是，熱那亞的碼頭上，她的酒精被一桶一桶數過。 | OK（c47、c13；「更怪的是」是修辭，不是事實） |
| `mc1s` | 然後是一八八五年，一個新船長故意把她開上礁石。 | **小問題 Q5**（順序） |
| `mc3f` | 奇怪的是，空船上廚房的爐灶被撞離了原位。 | **小問題 Q3**（歸屬） |
| `mc3g` | 羅經櫃也歪了，羅盤的玻璃罩破了。 | OK（c27；NEHS、FV 講的是發現時，現在排在德沃三人開船的時候，時間對） |
| `mc2c`→`mc3f`→`mc2d` | 爐灶、羅經櫃插在「三個人把空船往東開」與「英國船先進了直布羅陀」之間 | OK（facts.htm 第 4 條出處欄是 Testimony before Vice-Admiralty Court，講的是上船時的狀態，與開船同幾天） |
| `mc3z` | 勘驗官卻寫爐灶和羅經櫃都好好的，玻璃是燈烤裂的。 | OK（Austin 第 21 段 stove「in good order」、第 54 段 binnacle「did not appear to have sustained any damage」、第 52 段兩片玻璃「cracked… apparently from the heat of the lamp only」；原文有 apparently，但句子掛在「勘驗官寫」下面，是他的判讀，可以） |
| `mc6s` | 兩具幫浦拆了一具，好把量水深的桿子放進艙底。 | OK。**目的是紀錄原文，不是推論**：Austin 第 49 段「one of the pumps in good order the valve of the other had been removed **for the purpose of passing a sounding-apparatus into the well**」。嚴格說拆的是那一具的閥（SM07、EB 都寫 disassembled，所以「拆了一具」成立）；「艙底」＝幫浦井，可以。句子沒有說是誰拆的，這點也對（SM07 第 5 段說登船隊 12-04 就看到了，Austin 沒寫是誰） |
| `mc6r` | 那根桿子，就躺在幫浦旁邊。 | OK（Austin 第 50 段「The sounding apparatus… was lying near」，第 49 段開頭「Returning to the deck」；上一節 P1 已解決）。**插圖不符**（不是旁白）：`remember-rod` 的 prompt 還是「a long wooden rod standing in the corner of a cabin」，新句說它在甲板上、幫浦旁邊，Austin 寫的是一根繫在繩上的金屬栓。建議 prompt 改成甲板上幫浦井旁、平躺的一根繫繩測深桿 |
| `mc3h` | 怪就怪在船頭：勘驗官看到兩側有像刀砍出來的痕跡。 | OK（c32；「怪就怪在」是鉤子） |
| `mc3v` | 日誌把發現她那天記成五日：海上的一天，從中午換日。 | 事實 OK（facts.htm 第 6 條：found on 4 December between 1:00 and 2:00 P.M.，「the date, at sea, changed daily at the noon hour, the entry on **the Dei Gratia's log** was therefore dated 5, December, sea-time」）；**小問題 Q4**（哪一本日誌） |
| `mc3w` | 還有開頭說的那把劍，收在鞘裡，放在床底下。 | OK（上一節已查，字沒變） |
| `mc5b` | 那個沒署名的作者，後來寫出了福爾摩斯。 | OK（c8、c9） |
| `mc5r` | 查她的來歷，才知道她本來也不叫這個名字。 | OK（c6、c7） |
| `mc6t` | 前一趟載的是煤，煤灰可能塞住了那兩具幫浦。 | OK（SM07「on its previous voyage… had carried coal… Coal dust and construction debris could have fouled the ship's pumps」，複數；有「可能」） |
| `mc6p` | 二零零七年，有一份研究去查船長為什麼以為船在進水。 | **問題 Q1** |
| `mc6q`／`mc6u`／`mc6v` | （搬到第 8 章，字沒變） | OK（SM07；「這兩條路」的前文是 `mc7g`「艙裡有水，或者聞到味道」，跨了礁石兩句，仍接得上） |
| `mc7b` | 開頭那次點數就在這時候：一千七百零一桶酒精。 | OK（上一節已查） |
| `mc7s` | 小艇和上面的人，從來沒有被找到。 | OK（c46） |
| `mc7t` | 一八八五年那塊礁石，是新船長為了詐領保險開上去的。 | OK（c51） |
| `mc7u` | 船沒有沉，騙局被拆穿，陪審團七比五僵住了。 | OK（c51、c52；搬位置，字沒變） |
| `mc7r` | 六分儀和天文鐘，不是暫時下船的人會先帶走的東西。 | **問題 Q2** |

### 問題與替換

**Q1 `mc6p`（預設了一件來源沒說的事）**：「去查船長為什麼以為船在進水」把「船長以為船在進水」當成已知、當成研究的題目。
SM07 寫的研究題目是「Did Briggs, then, have a rational reason to abandon ship?」；結論也不是他「以為進水」，而是幫浦壞了，
「Briggs would not have known how much seawater was in his ship's hull」「having no way of determining whether his ship would sink」。
「erroneously believed his ship was taking on too much water」是 EB 寫的「A more likely scenario」，是假說，不是那份研究查的前提。替換：

> 二零零七年，有一份研究去查，船長叫大家離船，是不是有他的道理。

（下一句 `mc6q` 天文鐘、`mc6t` 幫浦、`mc6u`「以為船要沉了，是一個船長會做的判斷」都接得上。）

**Q2 `mc7r`（旁白自己的推理，沒有標記，而且和來源反方向）**：「不是暫時下船的人會先帶走的東西」不是任何來源的說法
（c46 列的破洞是「小艇從未被找到」「為什麼不直接靠岸」，不是儀器）。來源反而把帶走儀器寫進最被接受的那個解釋裡：
AH 轉述 Cobb 的假說「Gathering up chronometer, sextant, and ship's papers, Captain Briggs ordered everyone into the boat」；
SK「The captain had the sense to collect his sextant and marine chronometer, necessary for navigating」，並說
「No strong evidence suggests an answer to the question of whether they intended to completely abandon the ship, or to simply
sit at a safe distance」。舊句（「要暫時下船的人，不會先把找路的工具帶下去」）同樣的毛病，前兩輪把它掛在 c26／c46 下放過了，
這一輪改了字才重查到。前一句 `mc7q`（沒改）「這個解釋還是擋不住」也跟著講過頭。替換（兩句一起）：

> `mc7q` 清單上少掉的那幾樣東西，這個解釋只答得了一半。
> `mc7r` 帶走六分儀和天文鐘是謹慎，可是他們打算離開多久，沒有證據說得準。

若只能動 `mc7r` 一句，至少標成意見：「我的看法是，只想暫時避一下的人，不太會先帶走六分儀和天文鐘。」——但這仍和 SK 的判斷相反，不建議。

**Q3 `mc3f`（小，歸屬）**：事實有來源（證詞），排在第 2 章也對時間。可是現在它是旁白自己的口吻，十幾句後 `mc3z` 用「勘驗官**卻**寫…」
反駁，聽起來是旁白和勘驗官打架、沒有人收尾。`mc3z` 的「卻」已經承認了兩份紀錄不一致，這是對的；來源沒有解釋為什麼不一致
（中間隔了十八天和一趟航程，但沒有來源說有人把爐灶擺回去），所以不要補理由，只要把第一句掛回看到的人：

> 奇怪的是，他們發現廚房的爐灶被撞離了原位。

（「他們」＝前一句 `mc2c` 的三個人；`mc3g` 跟著它，不用改。）順帶：`mc3p`「我的看法是，除了爐灶和羅經櫃…」現在排在 `mc3z` 後面，
是意見句、證詞撐得住，不算錯，但撰稿可以考慮讀起來會不會像旁白沒聽進勘驗官的話。

**Q4 `mc3v`（小，哪一本日誌）**：這一章前面講過的「日誌」是瑪麗賽勒斯特號自己攤在桌上的那本（`mc3l`），facts.htm 講的是
Dei Gratia 號的日誌。替換：

> 發現她的那艘船，日誌記的是五日：海上的一天，從中午換日。

**Q5 `mc1s`（小，順序）**：開場三個預告是「到了一八八四年」→「更怪的是，熱那亞」（沒有年份）→「然後是一八八五年」。
「到了」和「然後」讓三件事聽起來照時間排，熱那亞卸貨（1873）就被放到 1884 和 1885 之間。替換（拿掉「然後」的時間意味）：

> 還有一八八五年，一個新船長故意把她開上礁石。

（或把 `tease-casks` 移到 `tease-novel` 前面，三件事就真的照時間排。）

### 搬位置後的日期與順序

第 6 章停在 1873-03-04 艦長的報告 → 第 7 章熱那亞卸貨（1873）→ 小艇沒找到 → 1885-01 礁石、1885-07 審判 → 第 8 章 2007 年研究。
現在照時間走，沒有一句的日期或「後來／這時候」講錯；`mc7o`「同一份研究」的前文 `mc6p` 在同一章；loops 八條仍先埋後收
（`mc1s`→`mc7t` 在 `mc7t` 搬動後仍在後面）。第 8 章章名「二零零七年，一份研究重算了她的位置」有 SM07（reconsidered those positions… 120 miles west）。

### 結論

24 句（含搬位置沒改字的 4 句）：19 句 OK；2 個實質問題（Q1 `mc6p` 把假說當前提、Q2 `mc7r` 是沒標記的推理且與 AH／SK 相反，連帶 `mc7q`），
3 個小問題（Q3 `mc3f` 歸屬、Q4 `mc3v` 哪本日誌、Q5 `mc1s` 預告順序），另有 1 張插圖 prompt（`remember-rod`）與新句不符。
`mc6s` 的「好把…放進艙底」是 Austin 第 49 段原文的目的，不是推論，不用改。Q1、Q2 改完即可，不需要再一輪；Q3–Q5 改不改由撰稿判斷。

## 第三輪修改查核 2026-10-13

- 查核 2026-10-13，Claude Opus 5.5（獨立查核代理，沒有寫過也沒有改過這份稿子）。`video.json` 一個字都沒動。
- 範圍：`NOTES.md`〈盲評修正第三輪 2026-10-13〉列的句子、搬了位置的句子，以及新的章序（1872 發現 → 直布羅陀勘驗 →
  1873 審理 → 1873 當年的說法 → 熱那亞 → 1884 小說 → 1885 礁石與陪審團 → 後來的傳說與海震／水龍捲 → 2007 研究）。
  上兩節已查過、字沒變的句子不重查。
- 當天重開的來源（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 ≥1.2 秒）：
  Austin 勘驗報告（survey.htm）、maryceleste.net/news.htm、maryceleste.net/about.htm、SM07、EB、AH、SK。全部 200。

### 逐句

| id | 句子 | 結果 |
| --- | --- | --- |
| `mc3za` | 爐灶歪了沒有，證詞和勘驗對不上，紀錄沒有答案。 | OK（c5 證詞 vs Austin 第 21 段 stove「in good order」；兩份隔了 12-04 到 12-23，沒有來源說明誰對、也沒有來源說有人擺回去，「紀錄沒有答案」不多不少） |
| `mc5w` | 小說登出來的隔年，她自己也出了事。 | OK（c8 1884 年 1 月 → c51 1885-01-03：曆年上就是隔年；實際相隔約一年，兩種讀法都成立） |
| `mc6x` | 誰也解釋不了，船長為什麼不直接把船開去靠岸。 | **問題 T1**（講過頭） |
| `mc6y` | 一百多年後，還有人想把這件事算清楚。 | OK（1872 → 2007 相隔 135 年；SM07「More than a century after her crew went missing」、「reconsidered those positions」，「算」貼切） |
| `mc6v` | 進水和酒精味，這兩條路都還有破洞。 | OK（c49「因為誤判進水或怕酒精蒸氣」；「酒精味」對應 `mc7g` 的「聞到味道」，酒精味這條的破洞 c44 沒有人聞到氣味） |
| `mc2m` | 船上本來還有他的太太莎拉，和兩歲的女兒蘇菲亞。 | OK（c14、c16：Sophia 1870-10-31 生，1872-11 兩歲；加上 `mc2n` 七個船員＝十人） |
| `mc1s` | 然後是一八八五年，一個新船長把她開上了礁石。 | OK（c51；預告現在照 1873 → 1884 → 1885 排，「然後」名副其實，Q5 已解決） |
| `mc5u`（搬到 `mc5f` 後） | 一個真實的船名，被一篇小說蓋了一百多年。 | OK（主詞是小說拼錯的船名，1884 到今天，與 claims「算出來的數字」一致） |
| `mc5l`（字沒變，位置變了） | 更離奇的還在後面。 | **小問題 T2**（新章序讓它變成時間主張） |
| 插圖 `remember-rod` | （prompt） | **是，相符**：Austin 第 49 段「Returning to the deck… the valve of the other had been removed for the purpose of passing a sounding-apparatus into the well」、第 50 段「a metal bolt attached to a line was lying near」——甲板、幫浦旁、繫繩的金屬栓、平放，prompt 都對上 |

### 問題與替換

**T1 `mc6x`（「誰也解釋不了」比來源強，而且緊接在一個答案後面）**：c46 的「為什麼不直接靠岸」在第一版 `research.md` 7.2
就標成「仍是推論」，是從 SM07「within sight of… Santa Maria」推出來的，SM07 和 EB 都沒有一句說「沒有人能解釋」。
反過來，SM07 的研究正好給了一個答案：幫浦壞了，「Briggs would not have known how much seawater was in his ship's hull」、
「having finally and belatedly sighted land and having no way of determining whether his ship would sink—might well have issued
an order to abandon ship」，而且他前一天「changed course and headed north of Santa Maria Island, perhaps seeking haven」。
`mc6u` 剛講完「以為船要沉了，是一個船長會做的判斷」，下一句接「誰也解釋不了」就跟它打架。能站住的是：紀錄裡沒有船長自己的理由
（日誌 1885 年已失，只剩抄本）。替換：

> 只是看得到陸地了，船長為什麼不直接把船開過去，紀錄沒有寫。

（「看得到陸地」＝SM07 的 within sight of / sighted land；仍是 c46 那個破洞，loop 與 `mc7q`／`mc7r`／`mc7s` 不受影響。）

**T2 `mc5l`（小，章序把升級句變成時間主張）**：它原本是升級句，不算主張。現在它緊接在 1885 年陪審團僵局後面、這一章又照年份走，
「還在後面」聽起來是海怪、章魚的說法出現在 1885 年以後。c10 本來就記了兩說：AH 放在道爾之後，about.htm 寫
「A popular theory **at the time** was that a giant squid, octopus, kraken…」，所以 `sea-monster` 的旁白刻意不講先後
（`NOTES.md` 章表把它寫成「後來的傳說」也偏了一邊）。替換（拿掉時間意味，`mc5m` 不用改；`mc5n`「再後來」只說百慕達三角比海怪晚，兩說下都成立）：

> 流傳的說法裡，還有更離奇的。

### 新章序的日期與「後來／這時候／那年」

- 第 2–4 章：12-13 靠港 → 12-18 開庭（「五天後」）→ 12-23 勘驗 → 1873-01-30 化驗 → 03-04 艦長報告（「一個多月後」）→
  「那年三月」判救助金：都對。
- 第 5 章（當年的說法）：船主自燃、海盜（1873-02 報紙）、詐保（「當年就有人猜」）、艦長「理由不充分」（03-04）都屬 1873；
  海震／水龍捲移走是對的：SK「Since then, even more suggestions have come from the fringe… like waterspouts and rogue waves.
  One in particular, David Williams, proposes that a "seaquake"…」——晚於當年的說法；news.htm 1873 年的報導沒有提到這兩說。
- 第 6 章：熱那亞卸貨（1873）。`mc7g` 起的「最站得住的版本」是今天的評價，沒有日期字眼；`mc4m`「全世界後來記住的」不和小說比先後，與 c3 一致。
- 第 7 章：`mc5a`「十二年後的一八八四年」有明確年份，從 1872 算成立（上一章停在 1873，但年份講出來了，不會誤會）；
  `mc5w`、`mc7t`、`mc7u` 1885 正確；`mc6k`「後來的研究者」排在 2007 之前：沒有來源給 Williams 的年份，句子也沒說比 2007 早，
  `mc6y` 的「還有人」不構成先後主張，可以。
- 第 8 章：`mc6y` → `mc6p` 2007 → 片尾，順。
- 圖（不是旁白，不算問題）：`year-after-novel` 借用 `sails-away` 的圖（小艇上的人看著帆船遠去，是 1872 年棄船那一幕），
  配的是 1885 年的句子；撰稿可以考慮換成同一章已畫好的圖，避免觀眾以為又回到 1872。

### 結論

這一輪 9 句旁白（含搬位置的 `mc5u` 與位置改變的 `mc5l`）：7 句 OK；1 個實質問題（T1 `mc6x`「誰也解釋不了」比 c46 強，
且與前一句 SM07 的答案打架），1 個小問題（T2 `mc5l` 被新章序變成時間主張）。`remember-rod` 的新 prompt 與 Austin 第 49–50 段相符。
章序沒有一句「後來／這時候／那年」講錯，海震與水龍捲排在當年說法之後有 SK 撐著。T1 改完即可，不需要再一輪；T2 改不改由撰稿判斷。
