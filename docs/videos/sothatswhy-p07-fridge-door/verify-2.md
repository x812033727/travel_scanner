# 查核報告 2（sothatswhy-p07-fridge-door）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有做查核第 1 輪）
- 日期：2026-11-06
- 範圍：`git diff HEAD~1 -- script.md`（commit 73c9aaa18「revision after fact-check round 1 and the blind panel」）改動或新增的部分。比對時把新舊 `video.json` 的台詞逐句對照（修改後台詞從 p001–p240 重新編號成 p001–p226），所以下表的行號都是**現在** `video.json` 的編號。沒改動的句子沿用 verify-1 的結論，不再重查。`script.md` 由 `build_scenes.py` 產生，重跑後與現有檔案一致（git 無變動），新舊句子都與 `video.json` 對得上。
- 方法：逐句讀新增與改寫的 18 句台詞、改過的 1 個 `shot` 提示詞，以及 `youtube`、`thumbnail`、`sources`（三者與上一版完全相同）。被刪掉的 16 句（冰箱背後留空隙與清灰塵、冷暖氣機冬天倒過來跑、冷只是熱比較少的回呼、電暖器一份電一份熱）不再需要查核，也確認留下的台詞與說明欄沒有再提到它們。來源都重新打開讀原文（curl 抓頁面轉成文字、Wikipedia 用 raw wikitext），不只沿用 verify-1 或 claims.md 的引文。
- 打不開的來源：沒有。
- 字數上限：小問 ≤15 字、所長 ≤25 字，數法照 `build_scenes.py` 的 `length()`（不算標點），用程式數過全部 226 句，沒有超過的。替換句與原句同長。
- 結論統計（新增或改寫的台詞 18 句）：OK 17、FIX 1、NOT FOUND 0。標題、說明、縮圖沒改動（沿用 verify-1 的 OK）。畫面提示詞 1 個改動：OK。
- verify-1 的 4 項台詞 FIX（F01–F04，共 5 句）都已改成來源支持的說法；F03 用「一個……鐵罐」而不是建議的「一顆」，意思相同（見第一節）。

## 一、第 1 輪 FIX 的落實情形

| 第 1 輪 | 現在的行 | 現在的句子 | 結論 | 依據 |
| --- | --- | --- | --- | --- |
| F01 | p196–p197（所長） | 一般的冷氣，用一份電，／大約能搬走好幾份的熱。 | OK | 與建議字句相同。HyperPhysics Heat Pump："they can use one unit of electric energy to transfer more than one unit of energy from a cold area to a hot area"；"A typical CP for a commercial heat pump is between 3 and 4"（制熱，含那份電）；Wikipedia COP "COP_heating = COP_cooling + 1"。換成搬走是 2–3 份，「好幾份」成立。p200–p201「要看冷氣和天氣」照留 |
| F02 | p198（小問） | 一份電搬好幾份？ | OK | 與建議字句相同，跟 F01 一致。畫面 kid-bargain、one-to-three 沒改，仍對得上（三是「好幾」之一） |
| F03 | p105–p106（所長） | 它跑進一個圓圓的鐵罐裡。／這個鐵罐叫做壓縮機。 | OK | 不再說壓縮機是馬達。Wikipedia Refrigerator："motor and compressor are integrated within a welded container, \"sealed unit\""，正是一個鐵罐；HyperPhysics "Then it is compressed and forced to condense in the hot area"。量詞從「一顆」改成「一個」，字數相同，畫面 compressor（"small round black metal compressor"）不必改 |
| F04 | p074（小問） | 有一股溫溫的風！ | OK | 與建議字句相同。HyperPhysics "warmer than the room temperature"；伊利諾大學 "it will usually be warm if the unit is running"。與所長 p076「摸起來是溫的」一致 |

## 二、逐項核對（新增與改寫的句子）

### 台詞

| 行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p129 | 先讓門關著，假設一組好算的數字 | OK | — | 把假設熱帳限定在門關著的情形，仍明說是假設；說明欄「為了好算的假設數字」也還對得上 |
| p137 | 那門關著，廚房會變熱嗎？ | OK | — | 問題；答案在 p138–p142 |
| p138 | 那兩顆熱，本來就是從牆和門邊，慢慢溜進冰箱的 | OK | Wikipedia Refrigerator；HyperPhysics Refrigerator、Thermal Conductivity | 冰箱是 "a thermally insulated compartment and a heat pump … that transfers heat from its inside to its external environment"；同頁說 "replacing deteriorated door seals with new ones … and replacing insulation" 能改善效率，即熱會從門封與隔熱層漏進去；HyperPhysics "The rate of heat transfer depends upon the temperature gradient and the thermal conductivity of the material"。門關著、溫度穩定時，冰箱搬出來的熱就等於漏進去的熱，所以在 p129 的「門關著」假設下，把兩顆熱說成從牆和門邊溜進來的是對的帳。附註：實際上放進去的溫食物、開門那幾秒也會帶熱進去，但台詞是在假設情境裡說，不必再補 |
| p139 | 現在被搬回廚房，還多帶了電變的那一顆 | OK | 伊利諾大學；Wikipedia COP | "more heat gets dumped outside the fridge than gets pumped out"；"when a fridge is running it is really warming up the room a little bit"；第一定律 Q_H + Q_C + W = 0。溜進去的兩顆被搬回來互相抵銷，淨多出的就是電變的那一顆，接 p140–p142「廚房也會熱一點點」 |
| p148 | 對，冰箱搬出來的那兩顆熱，又從門口跑回去 | OK | 伊利諾大學 | Follow-up："The refrigerator of course pumps heat around, from its inside to its coils, but … it still ends up dumping net energy into the room"。門開著時，背後吐出的熱進入廚房空氣，再從敞開的門口流回冰箱，跟 p145–p146、畫面 plan-loop 一致。p149「廚房的熱，一顆也沒有少」沒改 |
| p161 | 累的還有你家的電表 | OK | 伊利諾大學 | 接 p160「冰箱好累喔」的玩笑（所長的語氣標「笑」），意思是用電變多。依據同 p158–p159："The thermostat will kick in … This means the motor is running"。電表不會真的累，是擬人，不構成事實主張 |
| p162 | 電費也跟著一起變多 | OK | 伊利諾大學 | 壓縮機運轉更久＝用電更多，電費隨之增加，常識。原本的「吃的電越多，多變出來的熱也越多」刪掉了，不影響其餘的帳（p150–p151 已講每圈多一顆） |
| p165 | 很像。只是它繞了一大圈 | OK | Wikipedia Dehumidifier；伊利諾大學 | Dehumidifier："since all components … are in the same room … the electric power consumed … remains in the room as heat, so the room is actually heated, just as by an electric heater that draws the same amount of power"。開著門的冰箱冷熱兩頭都在廚房，帳相同，回答小問 p163–p164 說「很像」成立。「繞了一大圈」指 p145–p151 熱從門口進、背後出的循環；電暖器是直接把電變熱。原本「算起帳來」的限定拿掉了，但下一句馬上點出差別，不會被聽成兩者完全一樣 |
| p166 | 還順便讓冰箱裡的東西，一起變暖 | OK | 伊利諾大學 | "with the door open the temperature will start to rise inside the refrigerator"。這也正是它跟電暖器不同的地方（一開始有一部分熱拿去把冰箱裡變暖），「只是」接得正確 |
| p192 | 這次搬出去的熱，跑到圈外就回不來 | FIX（說得太絕對，且與片中自相矛盾） | EGEE 102；香港機電工程署；本片 p138、p207 | EGEE："It moves unwanted heat from where you don't want it (inside) to … (outside)"，支持熱被搬到圈外、不像開著門的冰箱那樣直接繞回來。但「回不來」太強：熱會從牆、窗再滲回房間，這正是 p206–p207「隔熱負責讓外面的熱，慢一點溜回來」與香港機電工程署 "Keep windows and doors closed … use curtains or blinds" 的理由；同一集 p138 也剛說過熱會從牆和門邊慢慢溜進冰箱。小朋友聽到 p192「回不來」、十五句後又聽到 p207「溜回來」，會覺得前後矛盾。要對照的是開著門的冰箱（p148「又從門口跑回去」），所以改成「不會直接繞回來」 |
| p193 | 圈裡的熱，才真的一顆一顆變少 | OK | EGEE 102 | "Only heat energy is moved or pumped by the air conditioner from a low temperature environment (inside the building) to a high temperature environment (outside the building)"。熱的那頭在圈外，圈裡淨減少，跟 p194–p195（電變的熱也大部分吐到圈外）一致。照 p192 改成「不會直接繞回來」後仍接得上 |
| p219 | 還記得冰箱和冷氣，是同一種機器嗎？ | OK | HyperPhysics Refrigerator | "The statements about refrigerators apply to air conditioners and heat pumps, which embody the same principles"。回呼的是 p172–p173 已講過的內容 |
| p222 | 還記得那三顆紅球嗎？你摸到的溫溫，就是它們 | OK | HyperPhysics Refrigerator；伊利諾大學 | 三顆＝搬出來的兩顆加電變的一顆（p133–p134），HyperPhysics "exhausting that heat to the room"、伊利諾大學 "more heat gets dumped outside the fridge than gets pumped out"。「三顆」是假設數字，這裡當回呼的代號用，意思是「搬出來的熱加上電」，與 verify-1 已 OK 的舊 p235–p236 相同 |

### 說明、縮圖與來源

`youtube`（標題、說明、標籤）、`thumbnail`、`sources` 與上一版逐字相同，沿用 verify-1 的 OK。說明欄「冷氣搬熱的倍數是教學資料裡的大約數字」在 F01 改成「好幾份」後仍成立；說明欄沒有提到刪掉的冷暖氣機制熱段落。本集沒有卡片。

## 三、畫面提示詞

改過 1 個，沒有畫出錯誤事實的：

- chief-out-of-circle（新）：所長在空中畫一個圈，再把手往圈外一揮，只有手勢，沒有事實內容；照 p192 改句後仍對得上。

刪掉的 9 個場景（kid-wall-q、chief-wall、kid-wall、kid-reverse-q、chief-reverse、kid-cold-heat、chief-cold-heat、chief-heater-vs、kid-heater-vs）隨台詞一起移除，不再需要查核。

## 非事實的備註（不影響查核結論，給 claims.md 的維護者參考）

- C10 的新主張「冰箱搬出的兩顆熱，本來就是從牆和門邊溜進去的」只引伊利諾大學與雪梨大學，兩者都沒寫熱從哪裡漏進去；本輪用 Wikipedia Refrigerator（"replacing deteriorated door seals … replacing insulation"）與 HyperPhysics Thermal Conductivity 核對，可補進 C10 的來源。兩筆都已在 `sources` 裡。
- C07／C08 寫的「家用冰箱是一個密封的鐵殼，馬達裝在裡面」可以補引 Wikipedia Refrigerator "motor and compressor are integrated within a welded container, \"sealed unit\""。
- C13 或 C14 若有寫到冷氣「搬出去的熱回不來」的可用說法，跟著 p192 一起改。

## 建議修改

- p192：這次搬出去的熱，跑到圈外就回不來， → 這次的熱吐到圈外，不會直接繞回來，（15 字，與原句同長）

## 來源

這一輪實際打開並讀到原文的頁面，都已在 `video.json` 的 `sources` 裡，本輪沒有新增。

```json
[
  {"title": "HyperPhysics (Georgia State University): Refrigerator", "url": "https://hyperphysics.gsu.edu/hbase/thermo/refrig.html", "checked_on": "2026-11-06"},
  {"title": "HyperPhysics (Georgia State University): Heat Pump, Air Conditioners and Heat Pumps, Coefficient of Performance", "url": "https://hyperphysics.gsu.edu/hbase/thermo/heatpump.html", "checked_on": "2026-11-06"},
  {"title": "University of Illinois Physics Van: Open Refrigerator", "url": "https://van.physics.illinois.edu/ask/listing/1790", "checked_on": "2026-11-06"},
  {"title": "Penn State EGEE 102: 10.4 How Air Conditioners Work", "url": "https://courses.ems.psu.edu/egee102/node/2426", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Refrigerator", "url": "https://en.wikipedia.org/wiki/Refrigerator", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Coefficient of performance", "url": "https://en.wikipedia.org/wiki/Coefficient_of_performance", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Dehumidifier", "url": "https://en.wikipedia.org/wiki/Dehumidifier", "checked_on": "2026-11-06"},
  {"title": "HyperPhysics (Georgia State University): Thermal Conductivity", "url": "https://hyperphysics.gsu.edu/hbase/thermo/thercond.html", "checked_on": "2026-11-06"},
  {"title": "Electrical and Mechanical Services Department, Hong Kong: Energy Saving Tips For Home, Air Conditioner", "url": "https://emsd.gov.hk/energyland/en/tips/home/air_conditioner.html", "checked_on": "2026-11-06"}
]
```

其餘來源（雪梨大學 Bar Fridge、Wikipedia Air conditioning）只支持沒改動的句子，沿用 verify-1 讀到的原文。
