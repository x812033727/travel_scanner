# 查核報告 1（sothatswhy-p04-microgravity-flame）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-12
- 方法：逐句讀 `video.json` 的 181 句台詞（p001–p181），加上 YouTube 標題、說明、標籤與縮圖文字（headline「太空的火／變圓了？」、sub「不是沒有重力，是一直在掉」）。`claims.md` 的 C01–C25 只當線索，不採用它的引文；每個來源當天重新打開（curl GET，HTML 取 `<main>` 去標籤轉純文字後 grep 並讀上下文；PDF 用 pdftotext）：
  - NASA STEM〈What Is Microgravity? (Grades 5-8)〉（200，293,256 bytes；頁首 "Feb 15, 2012"），讀全文：定義、"zero gravity … misleading"、200–250 英里與 90 percent、梯子 100／90 磅、free fall、遊樂園自由落體、棒球與 "falling toward but around Earth"、飛機 20-30 秒、雲霄飛車、落塔。
  - NASA Glenn〈What is Microgravity?〉（200，267,665 bytes；頁首 "Feb 13, 2009"），讀全文：88.8 percent、蘋果、牛頓大砲、17,500 mph（28,000 km/h）、"register "0" on a scale"、拋物線飛機 20-25 秒、Zero Gravity Research Facility "500 feet deep … just over 5 seconds"、雲霄飛車與彈簧床。
  - NASA〈Space Station Facts and Figures〉（200，313,866 bytes），讀 International Space Station Facts 段：five miles per second、about every 90 minutes、16 sunrises and sunsets。
  - NASA〈Studying Combustion and Fire Safety〉（200，304,383 bytes；頁首 "Dec 26, 2023"），讀開頭兩段與 CIR／FLEX 段。
  - NASA〈Candle Flame – 1g vs Microgravity〉（200，270,371 bytes；頁首 "Apr 30, 2020"），全文兩句。
  - NASA《Microgravity: A Teacher's Guide with Activities in Science, Mathematics, and Technology》EG-1997-08-110-HQ（ERIC ED463964 PDF，200，5,173,725 bytes，pdftotext），讀〈Drop Facilities〉、〈Combustion Science〉、〈Falling Water〉、〈Can Throw〉、〈Candle Flame in Microgravity〉活動說明（含 Activity Management 與 Extensions）、Student Reader 1–2（落塔、蠟燭、1992 年）。掃描 OCR 有錯字，引文照可辨認的原句。
  - Nayagam、Dietrich、Hicks、Williams（2014）NTRS 20140006750：條目頁（200，101,144 bytes）與原 PDF（200，324,885 bytes，`pdftotext -layout`），讀摘要、§1、§2、§3 首段、§3.1、§3.2、§3.3、§3.4 討論段與圖 1、圖 2 圖說。
  - **另找的一手來源**（C12 與 1992 年蠟燭需要）：
    - NASA Glenn〈Zero Gravity Research Facility〉https://www.nasa.gov/glenn/zero-gravity-research-facility/（200，311,417 bytes）與 Glenn 設施總覽 https://www1.grc.nasa.gov/facilities/zero-gravity/（200，415,289 bytes），讀 Facility Overview 與 Operational Parameters。
    - H. D. Ross、D. L. Dietrich、J. S. Tien〈Candle Flames in Microgravity: USML-1 Results – 1 Year Later〉（Joint L+1 Science Review for USML-1 and USMP-1, 1993-09；NTRS 20030075810 PDF，200，1,430,189 bytes，pdftotext），讀摘要、VI. Results、glovebox 內火焰壽命估算與熄滅機制段。這就是 claims.md 末尾說「這次沒有重讀」的那篇原研究。
- 打不開／沒讀到原文的：本集引用的 7 個來源都打得開（全部 200）。另試了兩個可能談冷焰可見度的 NASA 舊網址（science.nasa.gov〈Strange Flames on the ISS〉、nasa.gov 冷焰新聞稿），都是 404，沒有找到替代網址，所以 p140「看不見」只能用 FLEX 論文的相機敘述核對（見 S1）。
- 結論統計（台詞 181 句）：**正確 177、需改 4、錯誤 0**。另外標題、說明、標籤、縮圖 4 項：正確 4。另有 5 處選修建議（不影響結論，見文末）。
- 需改的 4 句裡，**內容會讓小孩記錯的只有 1 句**：p122（F02）。1992 年的蠟燭在太空裡只燒一分鐘左右，原研究把原因歸給密封小盒子裡的氧氣用完，並推論空氣夠多時蠟燭可以一直燒；片中接在「氧氣來得慢、溫度降下來」後面，小孩會記成「太空裡的蠟燭本來就只能燒一分鐘」。p133（F03）是說法和下一句互相打架；p041、p144（F01、F04）內容正確，只是字數超過上限。
- 字數：下表建議句含標點計算，小問 ≤15、所長 ≤25；建議句不含拉丁字母。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| F01 | p041（小問） | 梯子頂端還有九十，掉起來就變零！ | 需改（字數 16，超過小問的 15 字上限；內容正確） | 內容對：梯子頂端 90 出自 NASA STEM "that person would weigh 90 pounds at the top of the ladder"；掉落時體重計顯示零出自 NASA Glenn "it would register "0" on a scale"。只要縮短 | 梯子頂端九十，一掉就變零！（13 字） |
| F02 | p122（所長） | 蠟燭燒了四十五秒到一分鐘左右，就熄了。 | 需改（數字有據，但少了原因，接在 p119–p120 後面會讓小孩記成太空裡的蠟燭本來就只能燒一分鐘） | 秒數出自教師手冊 Student Reader："Candles onboard the first United States Microgravity Laboratory, launched in June 1992, burned from 45 seconds to about 1 minute before being extinguished because of the dropping temperature and reduction of wax vapor." 但這次實驗的原研究（Ross、Dietrich、Tien，USML-1 Results）寫的是："Extinction occurred between 40 and 60 seconds for all flames except one. One flame had a lifetime of 105 seconds"；火是在 glovebox 裡的小 candlebox 中燒的，"ambient oxygen depletion owed to the small glovebox volume and the candlebox complicates the test"、"This estimate supports the notion that flame extinction was caused by oxygen depletion"；摘要的結論是 "it is concluded that a candle can burn indefinitely in a large enough ambient of air in microgravity"（作者也註明這是推論，不是實驗證明）。片中 p118 問「會一直燒下去嗎？」，p119–p120 答「氧氣來得慢、溫度降下來」，p121–p122 再給一分鐘就熄的例子，聽起來一分鐘是太空蠟燭的天生上限，正好跟原研究的結論方向相反。p119 的「不一定」可以保留，把 p122 改成說出盒子的限制，「可能」對應原文的 supports the notion。「大多」照顧到 105 秒那一次 | 大多一分鐘就熄了，可能是裝它的盒子裡氧氣快沒了。（23 字；p121 照留） |
| F03 | p133（所長） | 相機什麼都拍不到了。可是量熱的儀器， | 需改（「什麼都拍不到」字面上不對，也跟下兩句打架：拍不到東西，怎麼知道液滴還在變小） | FLEX 論文 §3.1 說的是火焰影像拍不到："Both the color camera and the UV-camera are not sensitive enough to register any flame images during this period." 同一套儀器另有一台背光的液滴相機（§2 "a black-and-white, back-lit droplet image capture camera"），冷焰期間液滴大小就是靠它量的："the square of the droplet diameter decreases linearly with time in the cool-flame region, but at a slightly slower rate"。p135 的「那一滴還在變小」正是這台相機拍到的。改成「拍不到火」就一致 | 相機拍不到火了。可是量熱的儀器，（16 字） |
| F04 | p144（所長） | 美國太空總署說，冷焰燒出來的東西，跟一般的火不一樣； | 需改（字數 26，超過所長的 25 字上限；內容正確） | 〈Studying Combustion and Fire Safety〉："Typical flames produce carbon dioxide and water, but cool flames produce carbon monoxide and formaldehyde." 內容對，只要縮短 | 美國太空總署說，冷焰燒出來的東西跟一般的火不同；（24 字） |

## 二、逐段核對（正確的句子與依據）

### 開場：影片裡，火圓圓的（p001–p012）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p004 | 學校看影片：太空人飄來飄去，旁邊一團小火圓圓的像一顆球 | 正確 | NASA STEM；〈Studying Combustion〉 | 故事設定。"In microgravity, astronauts can float in their spacecraft"；"low-momentum flames tend to be rounded or even spherical"。「像一顆球」是小孩看到的樣子，p114–p116 補上「只看得到球的一部分」 |
| p005–p006 | 跟家裡蠟燭不一樣；蠟燭的火尖尖的 | 正確 | 〈Candle Flame〉 | "On Earth … a candle flame to be teardrop-shaped" |
| p007–p008 | 一定是太空沒有重力，東西才會飄，火才會變圓 | 正確（錯猜） | NASA STEM | 錯猜，p027–p028 以 "Some people think that there is no gravity in space. In fact, a small amount of gravity can be found everywhere in space" 與 90 percent 推翻 |
| p009–p010 | 很多人這樣猜；太空人其實一直在往下掉 | 正確 | NASA Glenn；NASA STEM | Glenn "Many people mistakenly think that gravity does not exist in space"；STEM "The answer is because they are in free fall" |
| p011 | 人一直在掉，火為什麼也跟著變了 | 正確 | — | 問句 |
| p012 | 他們明明是飄著的 | 正確 | — | 小孩的疑問，p013 回答 |

### 破洞的杯子一拋，水不漏了（p013–p049）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p013 | 飄著跟往下掉可以同時發生 | 正確 | NASA Glenn | "It just doesn't look like it's falling … Because they're all falling at the same rate, objects inside of the station appear to float" |
| p014–p016 | 底下有小洞的杯子，裝滿水拿著，水從洞裡流出來 | 正確 | 教師手冊〈Can Throw〉 | "When the can is stationary, water easily pours out of the small hole"。手冊用汽水罐，片中換成杯子（見 S2） |
| p017–p020 | 輕輕拋進大水盆，杯子在空中時小洞不漏水 | 正確 | 〈Can Throw〉 | "Toss the can through the air to the basin"；"The water remains in the can through the entire fall including the upward portion." 手冊另提醒 "being careful not to rotate the can in flight"，示範由所長做 |
| p021–p022 | 一拋出去重力就不見了嗎 | 正確（錯猜） | — | p024 推翻 |
| p023 | 這是美國太空總署給老師的手冊裡的一個活動 | 正確 | 教師手冊 | NASA EG-1997-08-110-HQ 的〈Can Throw〉活動；容器不同見 S2 |
| p024–p025 | 重力還在，杯子和水被拉得一樣，一起往下掉；掉得一樣快，水不會從洞擠出去 | 正確（簡化） | 〈Falling Water〉 | "Since they are both accelerated downward by gravity an equal amount, the cup and water fall together." 「拉得一樣」是加速度一樣的口語，不教錯 |
| p026–p028 | 太空站也是這樣；在太空站那個高度，重力還有地面的九成左右 | 正確 | NASA STEM；NASA Glenn | STEM "At that altitude, Earth's gravity is about 90 percent of what it is on the planet's surface"；Glenn "Earth's gravitational field at about 250 miles above the surface is 88.8 percent"。另以平方反比自行核算（地球半徑 6,371 公里、目前軌道約 420 公里）約 0.88，「九成左右」成立；片中不說高度，避開 2012 年頁面的舊高度 |
| p029–p030 | 梯子通到那裡，地上一百，頂端九十左右 | 正確 | NASA STEM | "if a person who weighed 100 pounds on Earth's surface could climb a ladder all the way to the space station, that person would weigh 90 pounds at the top of the ladder"。拿掉磅，比例照原文 |
| p031–p032 | 那太空人還很重，怎麼會飄 | 正確 | NASA STEM | 原文同一問："If 90 percent of Earth's gravity reaches the space station, then why do astronauts float there?" |
| p033–p035 | 整座太空站連人和東西都在掉；放開蘋果，蘋果也在掉，只是掉得一樣快，看起來像飄著 | 正確 | NASA Glenn；NASA STEM | Glenn "If an astronaut on the space station drops an apple, it falls too … they're all falling together: the apple, the astronaut and the station"；STEM "Since they are all falling together, the crew and objects appear to float" |
| p036 | 跟杯子和水一樣 | 正確 | — | 小孩的對照，對應 p024 |
| p037–p040 | 體重計會顯示零；身體一點都沒變少，只是量不出重量 | 正確 | NASA Glenn | "The object's mass is the same, but it would register "0" on a scale." |
| p041 | 梯子頂端還有九十，掉起來就變零 | 需改（F01，字數） | NASA STEM；NASA Glenn | 內容正確，字數 16 |
| p042–p043 | 遊樂園的自由落體，往下衝時放開東西，它飄在你面前 | 正確 | NASA STEM | "If a person let go of an object at the beginning of the fall, the person and the object would fall at the same acceleration … the object would appear to float in front of the person." |
| p044–p045 | 好像沒有重量的樣子叫微重力；微就是很小 | 正確 | NASA STEM | "Microgravity is the condition in which people or objects appear to be weightless … "Micro-" means "very small"" |
| p046–p047 | 可以叫零重力嗎；很多人這樣叫，等一下自己判斷 | 正確 | NASA STEM；NASA Glenn | STEM "Microgravity is sometimes called "zero gravity," but this is misleading"；Glenn "a state we call "zero gravity" (0g), or more accurately microgravity" |
| p048–p049 | 一直往下掉，怎麼沒撞到地球 | 正確 | — | 問句 |

### 杯子拋得越快，落得越遠（p050–p082）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p050 | 不只往下掉，還往旁邊跑得非常快 | 正確 | NASA STEM | "it is constantly falling toward Earth's surface. It also is moving at a very fast speed" |
| p051–p052 | 拋得越用力落得越遠；不管多快都是一邊往前一邊往下掉 | 正確 | NASA STEM | "If a person throws a baseball, gravity will cause it to curve down" |
| p053 | 拋得超級快呢 | 正確 | — | 問句 |
| p054–p057 | 牛頓想過：高山上的大砲，越快飛越遠；快到剛好就一直繞著地球掉 | 正確 | NASA Glenn | "Imagine placing a cannon at the top of a very tall mountain … The greater the speed, the farther it will travel before landing. If fired with the proper speed, the cannonball would achieve a state of continuous free-fall around Earth, which we call orbit." 「很久以前」不給年份 |
| p058–p061 | 地球是圓的；砲彈往下彎，地面也往下彎；兩個彎一樣，就永遠碰不到地 | 正確 | NASA STEM | "An orbiting spacecraft moves at the right speed so the curve of its fall matches the curve of Earth. Because of this, the spacecraft keeps falling toward the ground but never hits it." |
| p062–p063 | 太空站就是這樣，一直在掉卻掉不下去；這叫軌道 | 正確 | NASA Glenn；NASA STEM | "which we call orbit"；"As a result, they fall around the planet."（推進修正見 S5，選修） |
| p064–p066 | 一秒大約八公里 | 正確（換算） | Space Station Facts；NASA STEM；NASA Glenn | Facts "traveling at a speed of five miles per second"（約 8.05 公里）；STEM／Glenn "17,500 miles per hour (28,000 km per hour)"（約 7.8 公里／秒）。兩種都落在「大約八公里」 |
| p067–p069 | 大約九十分鐘一圈；一天看到十六次日出日落 | 正確 | Space Station Facts | "orbiting Earth about every 90 minutes"；"In 24 hours, the space station makes 16 orbits of Earth, traveling through 16 sunrises and sunsets." |
| p070–p071 | 裡面的人和東西也跑一樣快，所以不會被甩在後面 | 正確（撰稿推論） | NASA Glenn | "they are actually traveling at the same orbital speed as their spacecraft" |
| p072–p075 | 地上也能飄；手冊說杯子往上飛那一段水也不漏 | 正確（附註） | 〈Can Throw〉 | "including the upward portion"。手冊寫的是汽水罐，見 S2 |
| p076–p077 | 飛機照一樣的弧線一上一下飛，裡面的人飄起來，一次二十幾秒 | 正確 | 〈Can Throw〉；NASA STEM；NASA Glenn | "This is the same effect that occurs on aircraft flying in parabolic arcs"；STEM "about 20-30 seconds at a time"；Glenn "20-25 seconds"。「二十幾秒」兩者都對 |
| p078–p080 | 雲霄飛車衝過小山丘、跳彈簧床，也有一小下飄起來 | 正確 | NASA Glenn | "Most roller coasters have a set of parabolic (rolling) hills that also create brief periods of weightlessness … jumping on a trampoline also create brief experiences of weightlessness." |
| p081–p082 | 火在掉的時候也會變嗎 | 正確 | — | 問句 |

### 把蠟燭丟進很深的井（p083–p124）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p083–p084 | 美國太空總署讓火一起掉過；有一口很深的井，東西在裡面掉五秒多 | 正確 | NASA Glenn；Glenn ZGRF 頁；教師手冊 | Glenn "a large shaft some 500 feet deep that allows test packages to free fall in a vacuum for just over 5 seconds"；ZGRF 頁 "Microgravity Duration 5.18 seconds"、"Free Fall Distance 432 feet (132 m)"；手冊 "One provides a 132 meter drop into a hole in the ground similar to a mine shaft … for 5.2 seconds"。同一設施，見第三節 C12 |
| p085–p086 | 點著的蠟燭跟著一起往下掉，火很快就不尖了，變成圓圓的一團 | 正確 | 教師手冊 Student Reader | "a combustion experiment conducted at the NASA Lewis Research Center 132 Meter Drop Tower … recorded during a 5-second drop tower test … the flame stabilizes quickly … Instead of the typical teardrop shape seen on Earth, the microgravity flame becomes spherical." 原文是落下前後用電熱線點火、落下 1 秒時抽走，「點著的蠟燭放進去」是簡化，不影響結論 |
| p087–p088 | 小問要在家丟蠟燭；不行，火很危險，要在專門的地方做 | 正確（安全提醒） | 教師手冊〈Candle Flame in Microgravity〉 | 手冊的課堂版是老師帶、"be sure everyone working with the activity wears eye protection"、裝在塑膠罐裡丟；片中一律不教，說明欄也寫「請不要自己在家做燃燒的實驗」。方向正確（見 S3） |
| p089–p091 | 為什麼一掉就變圓；平常為什麼尖；是重力把火往上拉嗎 | 正確（錯猜） | — | 錯猜由 p092 推翻 |
| p092–p093 | 重力沒有把火往上拉；火把空氣燒熱，同樣一團空氣熱的比冷的輕 | 正確 | 教師手冊〈Combustion Science〉 | "combustion generally produces hot gas … which is less dense than the cooler gases around it." 「同樣一團」把「輕」限定成密度，沒說熱空氣沒重量 |
| p094–p095 | 重力把較重的冷空氣拉到火底下，熱空氣被推上去，火被拉成尖尖的 | 正確 | 〈Studying Combustion〉；教師手冊 | "gravity pulls cooler, denser air to the bottom of a flame, creating the classic shape"；"In Earth's gravity, the hot gas is pushed up by the denser surrounding gases"；"On Earth, the flame is drawn into a tip by the rising hot gases." |
| p096–p098 | 就像杯子裡的水往下從小洞擠出去？很像，都是比較重的往下擠 | 正確（比喻，附限度） | 教師手冊 | 兩件事背後是同一個機制：有重力又有東西撐著時，重的流體往下壓（水從洞流出、冷空氣擠到火底下）；大家一起自由落下時這股壓差消失（〈Can Throw〉"gravity's effects on the can and its contents are greatly reduced"；詞彙表 "Buoyancy-Driven Convection — Convection created by the difference in density between two or more fluids in a gravitational field"）。限度見第三節 C16 |
| p099 | 熱的往上、冷的補進來的流動叫對流 | 正確（簡化） | 教師手冊 | "This is an example of buoyancy driven (or gravity driven) convection"。片中講的是浮力對流，風扇吹的強制對流不提，p108 用「沒被吹著」補上 |
| p100 | 冷空氣從底下補進來帶來新鮮的氧氣 | 正確 | 教師手冊 Student Reader | "Fresh oxygen is not being delivered to the candle by these currents"（反面說法） |
| p101–p102 | 氧氣是空氣裡幫東西燒起來的那種氣體 | 正確（常識） | — | 給小孩的定義，不教錯 |
| p103–p104 | 掉的時候大家掉得一樣快，冷空氣不再往下擠，熱空氣也不再往上跑 | 正確（撰稿推論） | 〈Studying Combustion〉；〈Can Throw〉 | "In microgravity, this flow doesn't occur"；與杯子的機制相同，推論成立 |
| p105–p106 | 沒有對流往上拉，氧氣從四面八方慢慢來，火就圓了 | 正確 | 教師手冊 | "In the absence of buoyancy-driven convection … the supply of oxygen and fuel vapor to the flame is controlled by the much slower process of molecular diffusion. Where there is no "up" or "down," the flame tends toward sphericity." |
| p107–p108 | 太空站上對流不會發生，沒被吹著的小火常常變圓甚至像球 | 正確（簡化） | 〈Studying Combustion〉 | "In microgravity, this flow doesn't occur and on the space station, low-momentum flames tend to be rounded or even spherical." 「對流」沿用 p099 的浮力對流定義；「常常」＝tend to；「沒被吹著」＝low-momentum 的口語 |
| p109–p111 | 火是藍色的；他們比過一根蠟燭，地上對流把煙灰帶到火尖，所以黃 | 正確 | 〈Candle Flame〉 | "gravity-driven buoyant convection … carries soot to the flame's tip, which makes it yellow" |
| p112–p113 | 微重力裡那根蠟燭的火圓、沒煙灰、藍；這是那一根，不是每團太空裡的火都這樣 | 正確 | 〈Candle Flame〉 | "In microgravity, where convective flows are absent, the flame is spherical, soot-free and blue." 顏色只綁這一組比較，p113 明說範圍；USML-1 原研究也記錄點火後最初 8–10 秒有黃色煙灰，之後才變藍（"After 8-10 seconds, the yellow, presumably from soot, disappeared, and the flame became blue and hemispherical"），與 p113 的保留一致 |
| p114–p116 | 一整顆圓球嗎？不一定；手冊說蠟燭頂端把熱吸走，火的底部熄掉一塊，只看得到球的一部分 | 正確 | 教師手冊；Ross 等 | "Heat lost to the top of the candle causes the base of the flame to be quenched, and only a portion of the sphere is seen."；USML-1 "becomes and remains hemispherical and blue" |
| p117–p120 | 會一直燒下去嗎？不一定；氧氣來得慢，火燒得沒那麼旺，溫度慢慢降 | 正確 | 教師手冊 Student Reader | "Instead, oxygen works it way slowly to the flame by the process of diffusion. Soon, the flame temperature begins to drop because the combustion is less vigorous." 「不一定」與原研究「空氣夠多可以一直燒」相容 |
| p121 | 一九九二年在太空中做過的蠟燭實驗 | 正確 | 教師手冊；Ross 等 | "the first United States Microgravity Laboratory, launched in June 1992"；Ross 等 "determined in the glovebox facility aboard the First United States Microgravity Laboratory" |
| p122 | 燒了四十五秒到一分鐘左右就熄了 | 需改（F02） | 教師手冊；Ross 等 | 秒數有據，但缺了「盒子裡氧氣用完」的條件，會被聽成太空蠟燭的天生上限 |
| p123–p124 | 火熄了就是不燒了吧 | 正確 | — | 問句，p125 起回答 |

### 火熄了，那一滴還在變小（p125–p170）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p125 | 太空站上有一組實驗，發現不一定 | 正確 | 〈Studying Combustion〉；FLEX 論文 | "FLEX … led to the discovery of a type of cool flame, where the fuel continued "burning" under certain conditions after extinction of the visible flame." |
| p126–p127 | 約九十五公升的燃燒室，一小滴燃料自己飄著，用燒熱的電線點火 | 正確 | FLEX 論文 §2 | "free-volume of approximately 95 liters"；"freely deploy droplets of chosen size in microgravity"；"two symmetrically positioned hot-wire igniters"。原文也可用纖維繫住液滴，片中只講自由飄的，與本段引用的試次相符 |
| p128–p129 | 一公釐半到五公釐；點過三百多次 | 正確 | FLEX 論文 §3 | "Over three hundred droplet combustion tests were completed"；"varied from approximately 1.5 mm to 5 mm" |
| p130–p131 | 有一次，約四公釐的燃料先燒出看得見的火，約十五秒忽然熄了 | 正確 | FLEX 論文 §3.1（R377） | "initial diameter of 4.03 mm"；"extinguishing abruptly at around 14.6 seconds" |
| p132 | 熄了還有什麼好看的 | 正確 | — | 問句 |
| p133 | 相機什麼都拍不到了 | 需改（F03） | FLEX 論文 §2、§3.1 | 拍不到的是火焰影像，液滴相機仍在量大小 |
| p134 | 量熱的儀器還量得到那一滴在放出熱 | 正確（簡化） | FLEX 論文 §3.1 | "Both the broadband and narrowband radiometers, however, register continued radiative heat loss from the droplet indicating active chemical heat release." 輻射計說成「量熱的儀器」是合理簡化 |
| p135–p136 | 那一滴還在變小，只是慢一點；叫做冷焰 | 正確 | FLEX 論文 §3.1 | "The second-stage combustion termed "cool flame" … the square of the droplet diameter decreases linearly with time in the cool-flame region, but at a slightly slower rate." |
| p137–p140 | 冷的火摸起來冰嗎？不是，只是比一般的火溫度低，看不見卻還在燒 | 正確（簡化） | FLEX 論文摘要；〈Studying Combustion〉 | "continue to burn quasi-steadily following radiative extinction in a low-temperature regime"；"after extinction of the visible flame"。「看不見」見 S1 |
| p141–p142 | 縮到某個大小時冷焰突然停了，剩下的只是慢慢蒸發 | 正確 | FLEX 論文 §1、§3.1 | "the "cool flame" combustion of the droplet abruptly ends at a finite droplet diameter leaving the unburned droplet to vaporize in the hot ambient"；"Following cool flame extinction the droplet simply evaporates" |
| p143 | 冷焰熄掉前後，旁邊常常冒出一團霧 | 正確 | FLEX 論文摘要、§1 | "A vapor-cloud formed in most cases slightly prior to or following the "cool flame" extinction"；§1 "as the partially oxidized fuel and other products condensed" |
| p144 | 冷焰燒出來的東西跟一般的火不一樣 | 需改（F04，字數） | 〈Studying Combustion〉 | 內容正確，字數 26 |
| p145 | 弄懂它也許能做出更省油、汙染更少的車子 | 正確 | 〈Studying Combustion〉 | "could lead to the development of more-efficient, less-polluting vehicles"。「也許」＝could |
| p146–p147 | 為什麼要跑到太空才看得清楚 | 正確 | — | 小孩的問句；答案沒有接受「只有太空才有」的前提 |
| p148–p149 | 美國太空總署說，地上做出的冷焰很快就熄；在微重力裡燒得比較久，科學家才有機會研究 | 正確 | 〈Studying Combustion〉 | "Cool flames produced on Earth quickly flicker out. Since they burn longer in microgravity, scientists have the opportunity to study them." 逐句對應；p148 明說地上也做得出冷焰，沒說只在太空存在；沒解釋為什麼燒得比較久 |
| p150–p151 | 手冊也說，地上的對流會把火的一些事蓋住；拿掉對流，火比較安靜，更容易看懂 | 正確 | 教師手冊〈Combustion Science〉 | "eliminating buoyancy-induced flows allows scientists to study phenomena that are obscured by the effects of gravity"；"the "quieter" and more symmetric microgravity environment makes the experiments easier to model"。用「也說」「火的一些事」接，是對所有微重力燃燒的一般說法，沒有說成冷焰燒得久的原因 |
| p152–p154 | 太空裡的火都會這樣嗎？不是，同一組實驗換掉周圍氣體，結局就變 | 正確 | FLEX 論文 §3.1、§3.2 | 同一系列 FLEX 試次，各換氧氣濃度與稀釋氣體 |
| p155–p156 | 同一種燃料，氧從兩成一加到兩成五，火更靠近液滴也更熱，燒到很小時液滴爆開 | 正確 | FLEX 論文 §3.1（R374） | "a 3.79 mm n-decane droplet burning at a slightly increased oxygen concentration of 25%"；"the increased ambient oxygen concentration moves the flame closer to the droplet surface"；"increased flame temperature resulting from higher oxygen concentration"；"until the droplet micro-explodes 26 seconds after ignition"。R377 與 R374 都是正癸烷、0.5 大氣壓，「同一種燃料」成立 |
| p157–p158 | 減到一成七、一成四，看得見的火和冷焰都更早熄 | 正確 | FLEX 論文 §3.1（R379、R383） | "In general it can be summarized based on the results presented in Fig. 1 that reducing the ambient oxygen concentration leads to earlier hot and cool flame extinctions." |
| p159–p160 | 另一種燃料，把氮氣換成氦氣；就是讓氣球飄起來的氣體 | 正確 | FLEX 論文 §3.2；常識 | "four different n-octane droplets burning in oxygen/helium/nitrogen mixtures at one atmospheric pressure … the helium dilution is gradually increased at expense of nitrogen while the oxygen mole fraction is held constant at 0.21"。正辛烷、一大氣壓，與 p155 不同燃料，「另一種燃料」正確 |
| p161–p163 | 氦氣會讓火飄起來嗎？不會，氦氣很會把熱帶走；換到七成五，火點著不到一秒就熄，冷焰也很快結束 | 正確 | FLEX 論文 §3.2（R707） | "When helium dilution was increased to 75% by volume in test R707 … The hot flame that formed during the ignition dies within a fraction of a second and the cool flame burning commences immediately which also ends quickly"；"The high thermal conductivity of helium leads to large heat loss from the flame zone"。R707 液滴較小（2.49 mm），片中沒說是同一顆，沒有誤導 |
| p164–p165 | 火會變成什麼樣子，還要看旁邊是什麼氣體 | 正確 | FLEX 論文 | 兩組結果的合理整理，沒有說成通用定律 |
| p166–p168 | 不能叫零重力；重力還在，只是一起在掉；美國太空總署也說叫零重力會讓人誤會 | 正確 | NASA STEM | "Microgravity is sometimes called "zero gravity," but this is misleading."；"a small amount of gravity can be found everywhere in space"。p168 把小孩的「不能」收成「會讓人誤會」，照原文 |
| p169–p170 | 太空人一直在掉，火為什麼也變了 | 正確 | — | 問句，回收 p011 |

### 回到那段影片，小問想通了（p171–p181）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p171 | 杯子、蠟燭你都看過了 | 正確 | — | 橋接 |
| p172–p175 | 火和旁邊的空氣一起在掉，熱空氣不往上跑，火就不會被拉成尖尖的 | 正確 | 〈Studying Combustion〉；教師手冊 | "In microgravity, this flow doesn't occur"；"On Earth, the flame is drawn into a tip by the rising hot gases"。小孩的總結沒有說火一定變成藍色圓球 |
| p176–p177 | 我覺得最妙的是：讓杯子不漏水的那件事，也讓火變了樣子 | 正確（看法） | 〈Can Throw〉；教師手冊詞彙表 | 標成所長的看法；物理上兩者都是自由落下時重力造成的壓差消失，說法成立 |
| p178 | 我要拋破洞杯子給媽媽看 | 正確 | — | 只是水，不危險 |
| p179–p181 | 留言題、訂閱 | 正確 | — | p179 由 p078–p080 鋪好 |

### YouTube 標題、說明、標籤、縮圖

| 項目 | 結論 | 依據 |
| --- | --- | --- |
| 標題「太空人一直在掉，火焰為什麼也變了？｜原來如此事務所」 | 正確 | 問句；"they are in free fall" |
| 說明 | 正確 | 杯子（〈Can Throw〉）、九成左右（NASA STEM、Glenn）、一起在掉與繞著地球掉（STEM、Glenn）、冷空氣被拉到火底下與對流停了「就可能變圓」（〈Studying Combustion〉，「可能」保住範圍）、冷焰與換氣體結局變（FLEX）、微重力不是零重力（STEM）、AI 示意插圖聲明、「請不要自己在家做燃燒的實驗」、資料截至日。「看不見的『冷焰』」見 S1 |
| 標籤 | 正確 | 與內容相符 |
| 縮圖「太空的火／變圓了？」「不是沒有重力，是一直在掉」 | 正確 | 問句；sub 對應 NASA STEM 的 90 percent 與 free fall，沒有暗示所有太空的火都一樣 |

## 三、撰稿者標出的疑點

| 項目 | 結論 |
| --- | --- |
| C12 手冊的「132 Meter Drop Tower」與 Glenn 的「500 英尺深井」是不是同一個設施 | **是同一個**。Glenn〈Zero Gravity Research Facility〉頁："Microgravity Duration 5.18 seconds"、"Free Fall Distance 432 feet (132 m)"、"The free fall is conducted inside of a 467-foot- (142-meter-) long steel vacuum chamber … resides inside of a 28.5-foot- (8.7-meter-) diameter concrete lined shaft, which extends 510 feet (155 meters) below ground level"，而且 "The facility is one of two drop towers located at NASA's Glenn Research Center"（另一座是 2.2 秒落塔）。手冊 Student Reader："the 145 meter drop tower at the NASA Lewis Research Center … packages fall 132 meters"；〈Drop Facilities〉："One provides a 132 meter drop into a hole in the ground similar to a mine shaft … for 5.2 seconds. A tower at Lewis allows for 2.2 second drops down a 24 meter structure." Lewis 在 1999 年改名 Glenn；兩座設施中只有這一座是 132 公尺、5 秒多，所以手冊的蠟燭試驗（"a 5-second drop tower test"）就在這口深井裡做的。「500 英尺」是 Glenn 頁的概數（井深 510 英尺），「132 公尺」是自由落下的距離。片中只說「很深的井」「五秒多」，兩種數字都不念，正確。注意：這座設施落下時艙內抽成真空，蠟燭一定是裝在密封的實驗艙裡，插圖不要畫成蠟燭裸露在井裡掉（見 S4） |
| C10 一秒八公里由「five miles per second」換算 | 正確。5 英里 ≈ 8.05 公里；STEM／Glenn 的 17,500 mph ≈ 7.82 公里／秒、28,000 km/h ≈ 7.78 公里／秒。「大約八公里」對兩種寫法都成立。p065 把換算後的數字掛在「美國太空總署說」底下，可以接受（只換單位） |
| C22 冷焰：不能說為什麼燒得久、不能說只在太空存在 | 守住了。p148–p149 逐句照 NASA 原文，p148 明說「在地上做出的冷焰」，等於承認地上也有；沒有一句解釋燒得久的原因。p150–p151 用「那本老師手冊也說」接，主詞是「火的一些事」，是一般說法，不是冷焰的原因。p146–p147 小孩的問句帶有「要到太空才看得清楚」的前提，答案用 NASA 原句回應，沒有放大成「只有太空看得到」。FLEX 論文 §1 另寫過去的冷焰研究用 "stirred reactors, flow reactors, shock tubes, and rapid compression machines"（地上的預混氣體），也佐證冷焰不是太空才有 |
| 九成重力 | 正確。兩個 NASA 頁面（90 percent、88.8 percent）加上自行平方反比核算約 0.88。片中不給高度，避開舊數字 |
| 1992 年蠟燭燒的秒數 | 秒數有據，但需改 p122（F02）。手冊 45 秒到約 1 分鐘；原研究 "Extinction occurred between 40 and 60 seconds for all flames except one. One flame had a lifetime of 105 seconds"，並把熄滅歸給密封小空間的氧氣用完，推論 "a candle can burn indefinitely in a large enough ambient of air in microgravity"。片中不提這個條件，小孩會把一分鐘記成太空蠟燭的上限。另：原研究寫的是 "About ten single-candle flame tests"，手冊沒寫次數，片中也沒說次數，不受影響 |
| 藍色圓火是「那一根蠟燭」還是典型 | 守住了。p110「他們比過一根蠟燭」、p112「那根蠟燭」、p113「不是每一團太空裡的火都長這樣」，p116 再補「只看得到球的一部分」。開場平板上的藍色圓火是小孩看到的畫面，後面有交代。原研究也記錄前 8–10 秒有黃色煙灰，片中不說「一點著就藍」，沒有衝突 |
| 氧氣組與氦氣組是不同燃料 | 正確。氧氣組 R377／R374／R379／R383 都是正癸烷、0.5 大氣壓（p155「同一種燃料」）；氦氣組 R298／R694／R698／R707 是正辛烷、一大氣壓（p159「另一種燃料」）。液滴大小各次不同，片中沒說是同一顆 |
| 「不要在家丟蠟燭」的安全句 | 正確，方向對。手冊其實有課堂版的「丟蠟燭」活動（生日蠟燭裝在約 2 公升的塑膠罐裡丟，"be sure everyone working with the activity wears eye protection"，由老師帶），所以「要在專門的地方做」略嚴，但對孩子是正確的保守說法；片中與說明欄都沒教做法 |
| C16 破洞杯子比喻的限度 | 比喻在物理上比撰稿者擔心的更站得住：水從洞流出、冷空氣擠到火底下，背後都是重力在「有東西撐著」時造成的壓力差；一起自由落下時兩者同時消失（手冊對杯子 "gravity's effects on the can and its contents are greatly reduced"、對火 "In the absence of buoyancy-driven convection"）。p098「都是比較重的往下擠」就是這一點。限度：杯子不能說明火為什麼變圓（那是擴散從四面八方送氧，p105 另講）、為什麼變藍、為什麼會熄；片中沒有拿杯子去解釋這些，所以不教錯。小孩可能記成「火像水一樣會漏」，但 p103–p105 把杯子只用在「大家掉得一樣快，就不再擠」，風險低 |

## 建議修改

必改：

- F01 p041（小問）：梯子頂端還有九十，掉起來就變零！ → 梯子頂端九十，一掉就變零！（13 字）
- F02 p122（所長）：蠟燭燒了四十五秒到一分鐘左右，就熄了。 → 大多一分鐘就熄了，可能是裝它的盒子裡氧氣快沒了。（23 字）
- F03 p133（所長）：相機什麼都拍不到了。可是量熱的儀器， → 相機拍不到火了。可是量熱的儀器，（16 字）
- F04 p144（所長）：美國太空總署說，冷焰燒出來的東西，跟一般的火不一樣； → 美國太空總署說，冷焰燒出來的東西跟一般的火不同；（24 字）

改 F02 時請一起改 `claims.md` 的 C18（補上 Ross 等的 40–60 秒、105 秒與氧氣用完的原因）與 `script.md` 的同一行；本次查核依指示只寫 verify-1.md。

選修（不影響本輪結論）：

- S1 p140 與說明欄的「看不見」：FLEX 論文的根據是 "Both the color camera and the UV-camera are not sensitive enough to register any flame images"，也就是那兩台相機拍不到；〈Studying Combustion〉說的是 "after extinction of the visible flame"。冷焰在地上的暗室裡一般描述為很淡的光，本次沒找到能打開的 NASA 頁面確認肉眼可見度（兩個舊網址 404），所以不列需改。想更保守可改成：p140「幾乎看不見，卻還在燒。」（11 字）；說明欄「還有幾乎看不見的『冷焰』繼續燒」。
- S2 p014–p025、p075 的杯子：手冊〈Can Throw〉用的是底部戳洞的汽水罐（"Punch a small hole with a nail near the bottom of an empty soft drink can"）。p023 說「手冊裡，一個活動」沒問題；p075「那本手冊說，杯子往上飛的那一段」把杯子掛在手冊名下，若要精確可改成「那本手冊說，往上飛的那一段，水也不漏。」（19 字）。物理完全相同，可留。
- S3 p088：可留。若想不顯得「只有實驗室能做」，也可保持現句；不建議改成「大人帶著就可以」，因為本集企劃決定一律不教燃燒實驗。
- S4 deep-shaft 插圖：Glenn 這口井落下時抽成真空（"reduce the pressure in the chamber to a pressure of 0.05 torr"），蠟燭必定裝在密封、有空氣的實驗艙裡。插圖請把蠟燭畫在透明的密封箱或艙裡，不要畫成蠟燭裸露掉進井裡，避免小孩以為火能在真空裡燒。
- S5 p061–p062「永遠碰不到地」「一直掉不下去」：照 NASA STEM "never hits it" 與牛頓的理想化實驗，可留。實際上太空站受到很稀薄的空氣拖慢，需要不時推一下才能維持高度；本集不必講，只提醒之後若有小孩留言問可以這樣回答。
