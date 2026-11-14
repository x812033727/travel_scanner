# 查核報告 2（sothatswhy-p04-microgravity-flame）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有寫 verify-1.md）
- 日期：2026-11-12
- 範圍：verify-1.md 之後，經 verify-1 修正與四輪盲評改寫的 18 句台詞（現行 `video.json` 的 p011、p012、p025、p034、p042、p055、p063、p074、p102、p104、p118、p122、p126、p133、p145、p148、p150、p157），每句連前後一句讀；刪掉的句子有沒有讓別句失去前提；YouTube 說明欄與縮圖是否還跟片子一致；`claims.md` 各列行號對不對得上。其餘台詞沒有重查，結論沿用 verify-1.md。
- 比對方法：把 verify-1 查的第一版（session 暫存的 `p04/v1.json`，181 句，p001–p181）跟現行版（164 句，p001–p164）逐句 diff。結果與任務單一致：
  - 新增 3 句：p011、p012（片頭兩個鉤子）、p148（所長把「零重力」交回給小問判斷）。
  - 改寫 15 句：舊 p024→p025、舊 p033→p034、舊 p041→p042、舊 p054→p055、舊 p062→p063、舊 p075→p074、舊 p105→p102、舊 p107–p108→p104、舊 p122→p118（verify-1 F02）、舊 p127→p122、舊 p133→p126（F03）、舊 p140→p133（S1）、舊 p155–p156→p145、舊 p167→p150、舊 p174→p157。
  - 刪掉 20 句：舊 p023（「這是美國太空總署給老師的手冊裡，一個活動」）、p068–p069（十六次日出）、p076–p077（拋物線飛機）、p126、p128–p129（九十五公升、一公釐半到五公釐、三百多次）、p143（一團霧）、p144–p145（冷焰的產物與更省油的車，含 verify-1 F04 那一句），以及舊 p155–p163 九句裡除了濃縮成 p145 的部分以外的 8 句（同一種燃料兩成一到兩成五、氧氣減少、氦氣）。舊 p041（F01）整句換掉，不再有字數問題。
  - 編號：舊 p011 之後全部位移，位移量不固定（+2 到 −18）。`claims.md` 原本用的是舊編號，已同步（見第四節）。
- 來源：`claims.md` 只當線索，不採用它的引文。今天重新 curl GET（全部 200），HTML 取 `<main>` 去標籤轉純文字後 grep 並讀上下文，PDF 用 pdftotext：
  - NASA STEM〈What Is Microgravity? (Grades 5-8)〉（200，293,256 bytes；頁首 "Feb 15, 2012"）
  - NASA Glenn〈What is Microgravity?〉（200，267,665 bytes；頁首 "Feb 13, 2009"）
  - NASA〈Space Station Facts and Figures〉（200，313,866 bytes）
  - NASA〈Studying Combustion and Fire Safety〉（200，304,383 bytes）
  - NASA〈Candle Flame – 1g vs Microgravity〉（200，270,371 bytes）
  - NASA Glenn〈Zero Gravity Research Facility〉（200，311,417 bytes）
  - NASA 教師手冊 EG-1997-08-110-HQ（ERIC ED463964 PDF，200，5,173,725 bytes）：〈Falling Water〉、〈Can Throw〉、Student Reader 1–2、〈Combustion Science〉的擴散段
  - FLEX 論文 Nayagam 等（2014）NTRS 20140006750：條目頁（200，101,136 bytes）與原 PDF（200，324,885 bytes，`pdftotext -layout`）：§2、§3.1
  - Ross、Dietrich、Tien〈Candle Flames in Microgravity: USML-1 Results – 1 Year Later〉NTRS 20030075810 PDF（200，1,430,189 bytes）：摘要、Results
- 結論統計（18 句）：**正確 18、需改 0、錯誤 0**。另有 4 處選修建議（不影響結論，見文末）。
- verify-1 的四項必改都已處理：F02（p118）、F03（p126）照建議句改；F01、F04 所在的句子在盲評中整句換掉或刪掉。選修 S1（「幾乎看不見」）p133 與說明欄都已照改；S2（手冊用汽水罐）p074 改成不提容器，已解決。
- 字數：全部 164 句含標點計算，小問最長 14 字、所長最長 25 字（p011、p108、p109、p140 剛好 25），沒有超過上限；所有台詞不含拉丁字母。下文建議句也照同一算法。

## 一、需改的地方與理由

無。18 句都有來源支持，前後文也接得上。

## 二、逐句核對

| 行 | 現行台詞 | 結論 | 來源 | 依據摘要與前後文 |
| --- | --- | --- | --- | --- |
| p011（所長） | 等一下你會看到，一根點著的蠟燭，掉進一口很深的井。 | 正確（預告，簡化） | 教師手冊 Student Reader；NASA Glenn；Glenn ZGRF 頁 | 手冊："a combustion experiment conducted at the NASA Lewis Research Center 132 Meter Drop Tower … recorded during a 5-second drop tower test. An electrically heated wire was used to ignite the candle and then withdrawn 1 second into the drop"。蠟燭是落下時點著的，「點著的蠟燭」成立。Glenn："a large shaft some 500 feet deep that allows test packages to free fall in a vacuum for just over 5 seconds"，這口「井」跟手冊的 132 公尺落塔是同一座設施（verify-1 第三節已核）。實際上蠟燭裝在密封的實驗艙裡掉，「蠟燭掉進井」是預告用的簡化，p080–p083 才細講，跟 verify-1 已接受的 p082 同一層次。前文 p010「其實一直在往下掉」，後文 p012 第二個鉤子，接得上；預告在 p080–p083 兌現 |
| p012（所長） | 還有一團火熄了以後，儀器卻量到一件怪事。 | 正確（預告） | FLEX 論文 §3.1 | "Both the color camera and the UV-camera are not sensitive enough to register any flame images during this period. Both the broadband and narrowband radiometers, however, register continued radiative heat loss from the droplet indicating active chemical heat release."「儀器」＝輻射計，「怪事」＝看得見的火熄了還在放熱。在 p124–p127 兌現（「那團火忽然熄了」「量熱的儀器，還量得到那一滴在放出熱」），用字前後一致 |
| p025（所長） | 沒有不見喔。重力還在，杯子和水一起往下掉。 | 正確 | 教師手冊〈Falling Water〉、〈Can Throw〉 | "Since they are both accelerated downward by gravity an equal amount, the cup and water fall together."〈Can Throw〉"when the can is tossed, gravity's effects on the can and its contents are greatly reduced"——是「效應」變小，不是重力不見，正好推翻 p023–p024 的錯猜「重力就不見了？」。p026「掉得一樣快，就不會從小洞擠出去」接著補理由 |
| p034（所長） | 還記得我說太空人一直在掉嗎？整座太空站都在掉。 | 正確 | NASA Glenn；NASA STEM | Glenn："they're all falling together: the apple, the astronaut and the station"；STEM："The spacecraft, its crew and any objects aboard are all falling toward but around Earth."「還記得我說」回呼 p010。拿掉了舊句的「連裡面的人和東西」，但下一句 p035–p036 馬上說「太空人放開一顆蘋果，蘋果也在掉」「人、蘋果、太空站掉得一樣快」，沒有缺 |
| p042（小問） | 體重計也跟著一起掉了！ | 正確（小孩的推論） | NASA Glenn；NASA STEM | Glenn："Objects in a state of free fall or orbit are said to be weightless. The object's mass is the same, but it would register "0" on a scale."；STEM："all falling together"。體重計跟人一起自由落下，人不壓在秤上，所以顯示零，這是正確的物理解釋。前文 p040–p041 剛說顯示零、身體沒變少；後文 p043「對。遊樂園的自由落體也一樣」接得上 |
| p055（所長） | 很久以前，研究重力的科學家牛頓，就想過這件事： | 正確 | NASA Glenn | "The nature of gravity was first described by Sir Isaac Newton, more than 300 years ago."；"Newton developed a thought experiment to demonstrate this concept. Imagine placing a cannon at the top of a very tall mountain."「這件事」指 p054「拋得超級超級快呢？」，牛頓的大砲正是問越來越快會怎樣，對得上。「很久以前」不給年份 |
| p063（所長） | 太空站，就是那顆繞著地球掉的砲彈。 | 正確（比喻） | NASA Glenn；NASA STEM | Glenn："If fired with the proper speed, the cannonball would achieve a state of continuous free-fall around Earth, which we call orbit. The same principle applies to the space shuttle or space station."；STEM："the spacecraft keeps falling toward the ground but never hits it. As a result, they fall around the planet."「就是那顆砲彈」是比喻（同一個原理），不是說太空站是被大砲射上去的；前面 p056–p062 一直在講想像的大砲，小孩聽得出是比喻 |
| p074（所長） | 美國太空總署給老師的手冊說，往上飛那段水也不漏。 | 正確 | 教師手冊〈Can Throw〉 | "The water remains in the can through the entire fall including the upward portion."手冊是 NASA 出版（EG-1997-08-110-HQ），「美國太空總署給老師的手冊」正確。手冊用汽水罐，這句沒提容器，verify-1 S2 已解決。前文 p073「還記得拋出去的杯子嗎？」接小問 p072「在地上也能飄起來嗎？」：往上飛時也在自由落下，回答成立；後文 p075–p076 雲霄飛車、彈簧床（Glenn "brief periods of weightlessness"）。舊 p023 的手冊介紹刪了以後，這句成為片中第一次提到這本手冊，後面 p111「那本手冊說」、p140「那本老師手冊也說」都在它之後，指涉清楚 |
| p102（所長） | 沒有對流往上拉，氧氣只能從四面八方慢慢靠過來。 | 正確 | 教師手冊〈Combustion Science〉、Student Reader | "In the absence of buoyancy-driven convection, as in microgravity, the supply of oxygen and fuel vapor to the flame is controlled by the much slower process of molecular diffusion. Where there is no "up" or "down," the flame tends toward sphericity."；Student Reader "Instead, oxygen works it way slowly to the flame by the process of diffusion."「只能」對應 controlled by diffusion；有風吹的情況由 p104「沒被吹著」排除。舊句的「火就圓了」拿掉了，由 p103 小問「跟我在影片裡看到的一樣！」和 p086 的問題（「為什麼一掉就變圓？」）補上，意思還在，見選修 S2 |
| p104（所長） | 對。在太空站上，沒被吹著的小火也會這樣。 | 正確（簡化） | 〈Studying Combustion〉 | "In microgravity, this flow doesn't occur and on the space station, low-momentum flames tend to be rounded or even spherical."「沒被吹著的小火」＝low-momentum；「這樣」指前兩句的圓火。原文是 tend to（傾向），舊句的「常常」被拿掉，說法稍滿，但下文 p109「不是每一團太空裡的火都長這樣」、p111–p112「只看得到球的一部分」已把範圍收回，不會教錯；見選修 S1 |
| p118（所長） | 大多一分鐘就熄了，可能是裝它的盒子裡氧氣快沒了。 | 正確 | Ross 等 USML-1；教師手冊 Student Reader | Ross："Extinction occurred between 40 and 60 seconds for all flames except one. One flame had a lifetime of 105 seconds"；"oxygen depletion in the candlebox and the overall glovebox volume, combined with ongoing heat losses … led to extinction"；摘要 "it is concluded that a candle can burn indefinitely in a large enough ambient of air in microgravity"。「大多」照顧到 105 秒那一次，「可能」對應原文的推論語氣。手冊 "burned from 45 seconds to about 1 minute"。就是 verify-1 F02 的建議句。前文 p117「一九九二年，在太空中做過的蠟燭實驗」，後文 p119–p120 小問「火熄了，就是不燒了吧？」，接得上 |
| p122（所長） | 他們讓一小滴燃料自己飄著，用燒熱的電線點火。 | 正確 | FLEX 論文 §2 | "The MDCA used an opposed-needle deployment technique to freely deploy droplets of chosen size in microgravity."；"Ignition of the free droplet was accomplished using two symmetrically positioned hot-wire igniters."「他們」接 p121「太空站上有一組實驗」。燃燒室容積、液滴大小範圍、三百多次都刪了，後文 p123「一滴大約四公釐」自己交代大小，不依賴刪掉的句子 |
| p126（所長） | 相機拍不到火了。可是量熱的儀器， | 正確 | FLEX 論文 §2、§3.1 | "Both the color camera and the UV-camera are not sensitive enough to register any flame images during this period."液滴相機仍在量大小（§2 "a black-and-white, back-lit droplet image capture camera"），所以 p128「那一滴還在變小」不衝突。就是 verify-1 F03 的建議句 |
| p133（所長） | 幾乎看不見，卻還在燒。 | 正確 | FLEX 論文 §3.1、摘要；〈Studying Combustion〉 | 相機拍不到火焰影像（同上）；"continued "burning" under certain conditions after extinction of the visible flame"；摘要 "continue to burn quasi-steadily … in a low-temperature regime"。「幾乎」把絕對的「看不見」收回，就是 verify-1 S1 的建議；說明欄也同步寫「幾乎看不見的『冷焰』」 |
| p145（所長） | 像是氧氣多一點，液滴燒到很小時，會自己爆開。 | 正確 | FLEX 論文 §3.1（R374） | "a 3.79 mm n-decane droplet burning at a slightly increased oxygen concentration of 25% … The visible flame diameter initially increases with time and then it decreases until the droplet micro-explodes 26 seconds after ignition."；"Visible flame extinction in this case occurs at much smaller droplet size with a micro-explosion."；"precludes the radiative extinction observed before"。「氧氣多一點」＝21% 加到 25%（"slightly increased"），「燒到很小時」＝much smaller droplet size，「自己爆開」＝micro-explodes。比較的對象是 p123–p135 那一滴（R377，同為正癸烷、0.5 大氣壓），結局確實從冷焰變成爆開。前文 p144「換掉周圍的氣體」實際是改變氧氣比例，「像是」帶出一個例子，可接受的簡化 |
| p148（所長） | 對。那還記得零重力嗎？你自己判斷呢？ | 正確 | — | 沒有事實主張。「對」回應 p146–p147 小問的整理（「還要看旁邊是什麼氣體」，由 p144–p145 一個例子支持，沒說成通則）；「你自己判斷」兌現 p048「對不對，等一下你自己判斷」 |
| p150（小問） | 還記得那九成嗎？重力一直在！ | 正確 | NASA STEM | "At that altitude, Earth's gravity is about 90 percent of what it is on the planet's surface."；"a small amount of gravity can be found everywhere in space"。回呼 p029「還有地面的九成左右」。後文 p151「美國太空總署也說，叫零重力會讓人誤會」＝STEM "Microgravity is sometimes called "zero gravity," but this is misleading." |
| p157（小問） | 就像井裡那根蠟燭， | 正確（小孩的總結） | 教師手冊 Student Reader；〈Studying Combustion〉 | 前句 p156「火和旁邊的空氣，一起在掉」、後句 p158「火就不會被拉成尖尖的！」。手冊："Instead of the typical teardrop shape seen on Earth, the microgravity flame becomes spherical. On Earth, the flame is drawn into a tip by the rising hot gases. However, convection currents are greatly reduced in microgravity."井裡的蠟燭裝在有空氣的密封艙裡跟著一起掉，「火和旁邊的空氣一起在掉」正好成立。回收 p011 的鉤子與 p080–p083。舊句「熱空氣不往上跑」拿掉，但 p101「熱空氣也不再往上跑」已講過 |

## 三、刪句與說明欄的檢查

### 刪掉的句子有沒有讓別句失去前提

| 刪掉的內容 | 會受影響的句子 | 結論 |
| --- | --- | --- |
| 舊 p023「這是美國太空總署給老師的手冊裡，一個活動」 | p074、p111「那本手冊」、p140「那本老師手冊」 | 沒問題。p074 現在第一次介紹「美國太空總署給老師的手冊」，p111、p140 都在它之後 |
| 舊 p068–p069 十六次日出 | p068「大約九十分鐘，就繞地球一圈」 | 沒問題。p068 自己成立（Space Station Facts "orbiting Earth about every 90 minutes"）。插圖 `sunrise-curve` 還是地球邊上的日出，畫面跟話不衝突，只是少了呼應，可留 |
| 舊 p076–p077 拋物線飛機 | p073–p077、片尾留言題 p162 | 沒問題。地上也能飄的例子剩杯子往上那段、雲霄飛車、彈簧床（Glenn），p162「你在哪裡覺得自己飄了一下？」仍由 p075–p077 鋪好。說明欄沒有提飛機 |
| 舊 p126、p128–p129 燃燒室、液滴大小範圍、三百多次 | p122–p123 | 沒問題。p123 自己說「一滴大約四公釐」 |
| 舊 p143 一團霧 | — | 沒有別句提到 |
| 舊 p144–p145 冷焰的產物、更省油的車 | — | 沒有別句提到；說明欄沒有提車子 |
| 舊 p155–p163 同一種燃料的數字、氧氣減少、氦氣 | p144–p147 | 沒問題。p144「換掉周圍的氣體，結局就變了」由 p145 一個例子支持；p146–p147 小問的整理沒有說成規律。沒有任何句子再提氦氣或「另一種燃料」 |
| 舊 p107「美國太空總署說」 | p104 | 沒問題。p104 不再掛名，內容仍由〈Studying Combustion〉支持 |
| 舊 p167「只是一起在掉」、舊 p174「熱空氣不往上跑」 | p150、p157 | 沒問題，見第二節 |

### YouTube 說明欄、標題、縮圖

| 項目 | 結論 | 依據 |
| --- | --- | --- |
| 標題「太空人一直在掉，火焰為什麼也變了？｜原來如此事務所」 | 正確 | 同 verify-1 |
| 說明第 1 段（故事設定） | 正確 | 對應 p001–p013 |
| 說明第 2 段 | 正確，跟現行片子一致 | 杯子拿著會漏、拋出去不漏（p016–p026）；九成左右（p029）；一起在掉（p034–p036）；往旁邊跑得很快、繞著地球掉（p051–p064）；冷空氣被拉到火底下、對流停了「就可能變圓」（p089–p102）；液滴實驗、「幾乎看不見的『冷焰』」（p121–p133，跟 p133 用字一致）；「換掉周圍的氣體，結局也跟著變」（p144–p145）；微重力不是零重力（p149–p151）。**沒有提到任何已刪掉的內容**（日出、飛機、一團霧、車子、燃燒室、三百多次、氦氣、氧氣減少都沒有出現）。沒有提到井裡的蠟燭與 1992 年的蠟燭，只是沒寫進摘要，不是不一致 |
| 說明第 3 段（AI 示意插圖、「請不要自己在家做燃燒的實驗」） | 正確 | 「杯子、蠟燭、井、太空站與液滴」都還在片中 |
| 縮圖「太空的火／變圓了？」「不是沒有重力，是一直在掉」 | 正確 | 同 verify-1 |
| 參考資料（`sources` 7 筆） | 正確 | 片中仍用到全部 7 筆：[3] 只剩一秒八公里與九十分鐘，FLEX 論文只剩 R377 與 R374。Ross 等 USML-1 是 p118 的依據，但不在 `sources` 裡，見選修 S3 |

## 四、claims.md 的同步

`claims.md` 用的是第一版的編號（p001–p181），已逐列改成現行編號（p001–p164），引文全部保留。改動：

- 文首的行號說明改成 p001–p164（盲評第四輪後），並換算文首提到的 p087–p088、p148–p149、p150–p151。
- C01–C25 的「可用說法」與注意欄行號全部換成現行編號。
- 整條沒用到的標成「現行版未使用」：C21（冷焰的產物與更省油的車）、C24（氦氣）。
- 部分沒用到的在該列註明：C10 的十六次日出日落、C11 的拋物線飛機、C19 的九十五公升、液滴大小範圍與三百多次、C20 的一團霧、C23 的「同一種燃料」數字與氧氣減少；C03 的舊 p023 手冊介紹句改成註明現在由 p074 介紹手冊。
- 補上新句的對應：p011（C12）、p012（C20）、p042（C04、C05）、p055（C09）、p063（C08）、p104 不再掛名也拿掉「常常」（C16）、p145（C23）、p148–p150（C02、C07）、p157（C12、C25）。

## 建議修改

必改：無。

選修（不影響本輪結論）：

- S1 p104（所長）：原文是 "tend to be rounded or even spherical"，舊句有「常常」，現行「也會這樣」說得稍滿。下文已收回範圍，可留；若要貼原文：對。在太空站上，沒被吹著的小火也常這樣。（20 字）
- S2 p102（所長）：「火就圓了」拿掉後，「為什麼一掉就變圓」（p086）的答案要靠小孩自己從「四面八方」聯想到圓，再由 p103「跟我在影片裡看到的一樣！」接住。事實沒錯，是敘事選擇；若盲評有人聽不出答案，可改：沒有對流，氧氣只能從四面八方慢慢靠過來，火就圓了。（25 字）
- S3 `sources`：p118 的「可能是裝它的盒子裡氧氣快沒了」出自 Ross、Dietrich、Tien〈Candle Flames in Microgravity: USML-1 Results – 1 Year Later〉（NTRS 20030075810），說明欄的參考資料沒有它。建議補一筆（https://ntrs.nasa.gov/citations/20030075810）。不在本次可改的範圍，只提出來。
- S4 `brief.md` 第 21、37、42、50、61、63、68、71、87 列還寫著日出、拋物線飛機、一團霧、車子、九十五公升、三百多次、氦氣等已刪的內容，行號也是第一版。不在本次範圍，只提一下，免得下一個代理照 brief 把刪掉的段落加回來。
