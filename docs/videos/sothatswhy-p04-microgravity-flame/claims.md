# 主張與來源（sothatswhy-p04-microgravity-flame）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說、來源原文與注意事項，並標出它是
**官方說明**、**教材**、**研究報告**、**撰稿推論**、**常識**，還是**比喻／示意**。撰稿只能用「可用說法」裡的數字與說法；逐行查核等另一個代理寫 `verify-1.md`。

**行號**以現行 `video.json` 為準（p001–p153，verify-1 修正與四輪盲評之後的版本；2026-11-12 由 verify-2 從第一版的 p001–p181 換算；2026-11-13 照新頻道規則刪減小問台詞後重新換算，原 p001–p164）；`script.md` 是它的可讀版。**2026-11-14**：C26 在 p108 之後插入 10 句（p109–p118），C01–C25 裡寫的 p109 以後的行號，在現行 `video.json` 裡都要加 10（例如章尾鉤子原 p109–p110 現為 p119–p120）；p108 以前不變。第一版有、現行版刪掉的說法，在各列標成「現行版未使用」，引文照留。

2026-11-12 撰稿時當天重讀每一個來源（引文是原句；方括號數字對應文末〈來源〉）：
- [1] NASA〈What Is Microgravity? (Grades 5-8)〉（2012-02-15）、[2] NASA Glenn〈What is Microgravity?〉（2009-02-13）、[3]〈Space Station Facts and Figures〉、[5]〈Studying Combustion and Fire Safety〉（2023-12-26）、[6]〈Candle Flame – 1g vs Microgravity〉（2020-04-30）：curl GET 200（293,255／267,665／313,866／304,383／270,371 bytes），取 `<main>` 轉純文字，逐段讀。
- [4] NASA《Microgravity: A Teacher's Guide with Activities in Science, Mathematics, and Technology》（EG-1997-08-110-HQ，1997-08；ERIC ED463964 掃描版 PDF）：curl GET 200（5,173,725 bytes），pdftotext 後讀〈Combustion Science〉、〈Falling Water〉、〈Can Throw〉、〈Candle Flame in Microgravity〉與兩頁 Student Reader。掃描有 OCR 錯字，引文照可辨認的原句。
- [7] Nayagam、Dietrich、Hicks、Williams（2014）NTRS 20140006750：條目頁 200（101,136 bytes）與原 PDF 200（324,885 bytes，`pdftotext -layout`），讀摘要、1 Introduction、2 Experiments、3 Results 首段、3.1、3.2、3.3 開頭與圖 1–3 圖說。
- 素材池 P52-008～010、LEG-S80、LEG-S48 與 `season2/S48.md` 只當線索；這裡每一條都重開來源。P52-008 綁的 NASA 教育頁是 2012 年版，高度「200 到 250 英里」偏舊，**片中不說高度**，只說「在太空站那個高度」與「九成左右」（企劃：用 NASA 原句、不自算）。

**本集刻意不做的事**（企劃的刪減條件）：不講月球自轉、潮汐、太空生活清單；不說所有微重力火焰都是同一個形狀或顏色（藍色圓球只綁 [6] 那一根蠟燭，C17 另說只看得到球的一部分）；
不念冷焰的化學名（一氧化碳、甲醛、負溫度係數、正癸烷、正辛烷），也不念燃燒速率常數；不把冷焰推到太空站防火；不教任何點火或丟蠟燭的實驗（p076–p077 明說不行）；插圖一律是示意，說明欄寫明不是實驗照片或實際器材。

**還缺的來源（企劃點名的）**：「為什麼冷焰只在微重力下看得到」沒有找到說明**原因**的來源。找到的是 NASA [5] 的一句**現象**：「Cool flames produced on Earth quickly flicker out. Since they burn longer in microgravity, scientists have the opportunity to study them.」片中只照這句說（p128–p129），**不說「只有」微重力看得到，也不解釋為什麼燒得比較久**；另外加 [4] 的一般說法（對流會蓋住一些現象、微重力比較安靜好分析，p130–p131），不把它說成冷焰的原因。

## C01 太空人會飄，看起來沒有重量；這叫微重力，「微」是很小【教材】

- **可用說法**：p001、p039–p040
- **來源**：[1]
- **原文**：「Microgravity is the condition in which people or objects appear to be weightless. … "Micro-" means "very small," so microgravity refers to the condition where gravity seems to be very small. In microgravity, astronauts can float in their spacecraft」
- **注意**：p039「好像沒有重量的樣子」＝ appear to be weightless；p040 只解釋字面。

## C02 太空站那個高度，地球的重力還有地面的九成左右；梯子比喻 100 → 90【教材＋官方說明交叉】

- **可用說法**：p024–p027（p006、p020 的錯猜由這裡推翻）；p140 小問回呼「重力一直在！」（2026-11-13 從「還記得那九成嗎？重力一直在！」縮短）
- **來源**：[1]，交叉核對 [2]
- **原文**：[1]「The International Space Station orbits Earth at an altitude between 200 and 250 miles. At that altitude, Earth's gravity is about 90 percent of what it is on the planet's surface. In other words, if a person who weighed 100 pounds on Earth's surface could climb a ladder all the way to the space station, that person would weigh 90 pounds at the top of the ladder.」[2]「Earth's gravitational field at about 250 miles above the surface is 88.8 percent of its strength at the surface.」
- **注意**：原文是磅；片中拿掉單位，只說「體重是一百……還有九十左右」，比例照原文。高度不說（2012 年的數字）。沒有自行用平方反比核算。

## C03 一拋出去，破洞杯子不漏水；杯子和水被重力拉得一樣，一起往下掉【教材】

- **可用說法**：p014–p022、p046、p066–p067、p091、p149
- **來源**：[4]〈Can Throw〉、〈Falling Water〉
- **原文**：〈Can Throw〉（拿汽水罐，底部用釘子戳一個小洞）「When the can is stationary, water easily pours out of the small hole and falls to the catch basin. However, when the can is tossed, gravity's effects on the can and its contents are greatly reduced. The water remains in the can through the entire fall including the upward portion. This is the same effect that occurs on aircraft flying in parabolic arcs.」〈Falling Water〉「the cup and water both fall at the same time. Since they are both accelerated downward by gravity an equal amount, the cup and water fall together.」
- **注意**：手冊用汽水罐，片中換成底部有小洞的塑膠杯（同一個做法，杯子比較好畫）；第一版的介紹句「這是美國太空總署給老師的手冊裡，一個活動」已刪（現行版未使用）；現在由 p067「美國太空總署給老師的手冊說，往上飛那段水也不漏」第一次提到手冊，且不提容器。p021「沒有不見喔。重力還在，杯子和水一起往下掉」推翻 p019–p020 的錯猜。p022「就不會從小洞擠出去」是撰稿的口語解釋（水和杯子之間沒有相對的推擠），手冊只寫結果。片中所長示範、沒有叫小朋友去拋（片尾小問說要拋給媽媽看，只是水，不危險）。

## C04 太空站和裡面的人、東西一起在掉；放開蘋果，蘋果也在掉，只是掉得一樣快，看起來像飄著【官方說明＋教材】

- **可用說法**：p008、p029–p031（p029「還記得我說太空人一直在掉嗎？整座太空站都在掉」回呼 p008）；p036 小問「體重計也在掉！」也靠這條（秤跟人一起掉）
- **來源**：[2]、[1]
- **原文**：[2]「If an astronaut on the space station drops an apple, it falls too. It just doesn't look like it's falling. That's because they're all falling together: the apple, the astronaut and the station. … Because they're all falling at the same rate, objects inside of the station appear to float」[1]「The answer is because they are in free fall. … The spacecraft, its crew and any objects aboard are all falling toward but around Earth. Since they are all falling together, the crew and objects appear to float when compared with the spacecraft.」

## C05 一直在掉的時候，體重計顯示零；身體（質量）沒變【官方說明】

- **可用說法**：p034–p036
- **來源**：[2]
- **原文**：「Objects in a state of free fall or orbit are said to be weightless. The object's mass is the same, but it would register "0" on a scale.」
- **注意**：p035「身體一點都沒變少」＝ mass is the same 的口語。p036 小問「體重計也在掉！」是小孩的推論：秤和人一起自由落下（C04 的 all falling together），所以顯示零；物理正確，不是新數字。（第一版的「梯子頂端還有九十，掉起來就變零！」已換掉。）

## C06 遊樂園的自由落體：下墜時放開東西，它飄在你面前【教材】

- **可用說法**：p037–p038
- **來源**：[1]
- **原文**：「Some amusement parks have free-fall rides, in which a cabin is dropped along a tall tower. If a person let go of an object at the beginning of the fall, the person and the object would fall at the same acceleration. Because of that, the object would appear to float in front of the person.」

## C07 叫「零重力」會讓人誤會【教材＋官方說明】

- **可用說法**：p041–p042（埋）、p138–p141（回收；p138 所長「那還記得零重力嗎？你自己判斷呢？」兌現 p042，p140「重力一直在！」回呼九成）
- **來源**：[1]、[2]
- **原文**：[1]「Microgravity is sometimes called "zero gravity," but this is misleading.」[2]「objects inside of the station appear to float in a state we call "zero gravity" (0g), or more accurately microgravity」
- **注意**：[2] 括號裡的 1×10⁻⁶ g 不念（企劃：不說任何軌道的固定重力值）。

## C08 太空站不只往下掉，還往旁邊跑得非常快；落下的彎跟地球的彎一樣，所以一直掉卻碰不到地；這叫軌道【教材＋官方說明】

- **可用說法**：p045、p047、p053–p058（p057「太空站，就是那顆繞著地球掉的砲彈」是比喻，對應 [2] 的「The same principle applies to the space shuttle or space station.」）
- **來源**：[1]、[2]
- **原文**：[1]「Gravity pulls on the space station, too. As a result, it is constantly falling toward Earth's surface. It also is moving at a very fast speed … It moves at a speed that matches the way Earth's surface curves. … An orbiting spacecraft moves at the right speed so the curve of its fall matches the curve of Earth. Because of this, the spacecraft keeps falling toward the ground but never hits it.」[2]「If fired with the proper speed, the cannonball would achieve a state of continuous free-fall around Earth, which we call orbit.」
- **注意**：p047「不管拋多快，杯子都是一邊往前、一邊往下掉」是撰稿的口語橋接，意思同 [1] 的 baseball 段（「gravity will cause it to curve down」）。

## C09 牛頓的大砲：山頂的大砲，射得越快飛得越遠；快到剛好就一直繞著地球掉【官方說明】

- **可用說法**：p049–p052
- **來源**：[2]
- **原文**：「Newton developed a thought experiment to demonstrate this concept. Imagine placing a cannon at the top of a very tall mountain. Once fired, a cannonball falls to Earth. The greater the speed, the farther it will travel before landing. If fired with the proper speed, the cannonball would achieve a state of continuous free-fall around Earth, which we call orbit.」
- **注意**：p049「很久以前」不給年份；[2] 前一段說牛頓描述重力是 300 多年前，不念。p049「研究重力的科學家牛頓」對應 [2]「The nature of gravity was first described by Sir Isaac Newton」。

## C10 一秒大約八公里；大約九十分鐘一圈；一天十六次日出日落；裡面的東西跟著一樣快【官方說明＋換算】

- **可用說法**：p060、p061、p062–p063（「一天十六次日出日落」現行版未使用，第一版的 p068–p069 已刪）
- **來源**：[3]、[2]
- **原文**：[3]「An international crew of seven people live and work while traveling at a speed of five miles per second, orbiting Earth about every 90 minutes.」「In 24 hours, the space station makes 16 orbits of Earth, traveling through 16 sunrises and sunsets.」[2]「While objects inside them appear to be floating and motionless, they are actually traveling at the same orbital speed as their spacecraft: 17,500 miles per hour (28,000 km per hour)!」
- **注意**：一秒八公里是**換算**（5 英里 ≈ 8.05 公里；[2] 的每小時 28,000 公里 ÷ 3600 ≈ 7.8 公里，兩者都在「大約八公里」）。p063「不會被甩在後面」是撰稿推論，意思同 [2] 的 same orbital speed。

## C11 在地上也能飄：飛機照拋出去的弧線飛，一次二十幾秒；雲霄飛車的小山丘、跳彈簧床也有一小下【教材＋官方說明】

- **可用說法**：p066–p069（拋物線飛機「一次二十幾秒」現行版未使用，第一版的 p076–p077 已刪；現行版只留杯子往上那段、雲霄飛車與彈簧床）
- **來源**：[4]〈Can Throw〉（見 C03）、[1]、[2]
- **原文**：[1]「NASA uses airplanes to create microgravity for short periods of time. The airplane does this by flying in up-and-down parabolas. At the top of the parabola, people and objects inside the airplane are in free fall for about 20-30 seconds at a time.」[2]「aircraft flying in parabolic arcs to create microgravity for tests and simulations that last 20-25 seconds」「Most roller coasters have a set of parabolic (rolling) hills that also create brief periods of weightlessness. For less adventurous people, a car ride on the rolling hills of a country road or jumping on a trampoline also create brief experiences of weightlessness.」
- **注意**：兩頁的秒數不同（20–30、20–25），第一版片中說「二十幾秒」兩者都對（現行版已不說飛機）。片尾留言題（p151「你在哪裡覺得自己飄了一下？」）由這段鋪好。

## C12 美國太空總署有一口很深的井，東西可以在裡面掉五秒多；把點著的蠟燭放進去掉，火很快就變圓【官方說明＋教材】

- **可用說法**：p072–p075；片頭鉤子 p009「一根點著的蠟燭，掉進一口很深的井」（收尾小問原本的「就像井裡那根蠟燭」2026-11-13 已刪）
- **來源**：[2]、[4] Student Reader
- **原文**：[2]「NASA Glenn has the Zero Gravity Research Facility. It is a large shaft some 500 feet deep that allows test packages to free fall in a vacuum for just over 5 seconds.」[4]「The sequence of pictures … illustrates a combustion experiment conducted at the NASA Lewis Research Center 132 Meter Drop Tower. These pictures of a candle flame were recorded during a 5-second drop tower test. An electrically heated wire was used to ignite the candle … the flame stabilizes quickly, and its shape appears to be constant throughout the remainder of the drop. Instead of the typical teardrop shape seen on Earth, the microgravity flame becomes spherical.」
- **注意**：NASA Lewis 就是現在的 Glenn；[4] 的 132 公尺落塔和 [2] 的 500 英尺深井是同一個設施的兩種說法（深井裡可自由落下的長度），**這是撰稿的對照，查核代理請確認**；片中不念公尺或英尺，只說「很深的井」與「五秒多」。p075「圓圓的一團」照 [4] 的 spherical，C17 再補「不是完整的球」。[2] 原文的井在真空中落下，片中不提真空（跟火焰無關，會讓人以為火在真空裡燒）。

## C13 火很危險，這要在專門的地方做【安全提醒】

- **可用說法**：p076–p077
- **注意**：[4] 的〈Candle Flame in Microgravity〉是課堂活動（戴護目鏡、老師帶），片中不教做法，只說不要自己在家做；說明欄也寫。

## C14 重力沒有把火往上拉；火把空氣燒熱，同樣一團熱空氣比冷空氣輕；重力把較重的冷空氣拉到火底下，熱空氣被推上去，火被拉成尖尖的【官方說明＋教材】

- **可用說法**：p080–p084
- **來源**：[5]、[4]
- **原文**：[5]「on Earth, hot gases from a flame rise and gravity pulls cooler, denser air to the bottom of a flame, creating the classic shape and flickering effect.」[4]「combustion generally produces hot gas …, which is less dense than the cooler gases around it. In Earth's gravity, the hot gas is pushed up by the denser surrounding gases.」「The familiar shape of a candle flame on Earth is caused by buoyancy-driven convection.」
- **注意**：「輕」是密度的口語，所以 p082 寫「同樣一團空氣」；不說熱空氣沒有重量（S48 的限制）。p080 小問的錯猜「重力把火往上拉」由 p081 直接推翻。

## C15 熱的往上、冷的補進來的流動叫對流；冷空氣從底下補進來帶來新鮮的氧氣【教材】

- **可用說法**：p087–p090
- **來源**：[4]
- **原文**：「heated water rises to the top due to buoyancy. A circulation pattern is produced … This is an example of buoyancy driven (or gravity driven) convection. … This is the same density driven convection process to which we refer when we state matter-of-factly that "hot air rises."」Student Reader：「convection currents are greatly reduced in microgravity. Fresh oxygen is not being delivered to the candle by these currents.」
- **注意**：p090「空氣裡，幫東西燒起來的那一種氣體」是**常識**的口語定義，不是來源原句。

## C16 一起往下掉時，冷空氣不再往下擠，熱空氣也不往上跑；沒有對流往上拉，氧氣從四面八方慢慢來，火就圓了；太空站上對流不會發生，沒被吹著的小火常常變圓甚至像球【撰稿推論＋官方說明＋教材】

- **可用說法**：p091–p094
- **來源**：[5]、[4]、[6]
- **原文**：[5]「In microgravity, this flow doesn't occur and on the space station, low-momentum flames tend to be rounded or even spherical.」[4]「In microgravity, a candle flame assumes a spherical shape as fresh oxidizer reaches it by diffusion processes.」「In the absence of buoyancy-driven convection, as in microgravity, the supply of oxygen and fuel vapor to the flame is controlled by the much slower process of molecular diffusion. Where there is no "up" or "down," the flame tends toward sphericity.」[4] 詞彙表：「Buoyancy-Driven Convection — Convection created by the difference in density between two or more fluids in a gravitational field.」
- **注意**：p091–p092 把杯子（C03）套到空氣上，是**撰稿推論**：來源分別說「一起掉時重力的效應大幅變小」（C03）與「微重力中這股流動不發生」（[5]），沒有一句話把兩者連起來。比喻的限度：杯子講的是水和杯子之間不再有推擠；空氣講的是冷熱空氣之間不再有「重的往下擠」。兩者都是「大家掉得一樣快、輕重不再造成推擠」，這一點對應正確；杯子不能說明擴散與燃燒。
  p093 現在是「沒有對流往上拉，氧氣只能從四面八方慢慢靠過來」，不再自己說「火就圓了」，直接由 p094 接上（原本接話的小問「跟我在影片裡看到的一樣！」2026-11-13 已刪，p094 句首的「對。」一併拿掉）。p094「在太空站上，沒被吹著的小火也會這樣。」：「沒被吹著的小火」是 low-momentum 的口語（S48：「氣流等帶來的推動比較弱」），**簡化**；第一版的「美國太空總署說」「常常」「甚至像一顆球」已拿掉，「也會這樣」比 tend to 稍滿，由 p109、p111–p112 收回範圍（verify-2 選修 S1）。不說太空裡完全沒有氣流。

## C17 一根蠟燭的比較：地上對流把煙灰帶到火尖所以黃；微重力裡那根蠟燭的火圓、沒有煙灰、藍；不是每一團都這樣；實際常只看得到球的一部分【官方說明＋教材】

- **可用說法**：p096–p102
- **來源**：[6]、[4]
- **原文**：[6]「On Earth, gravity-driven buoyant convection causes a candle flame to be teardrop-shaped and carries soot to the flame's tip, which makes it yellow. In microgravity, where convective flows are absent, the flame is spherical, soot-free and blue.」[4]「Heat lost to the top of the candle causes the base of the flame to be quenched, and only a portion of the sphere is seen. The diminished supply of oxygen and fuel causes the flame temperature to be lowered to the point that little or no soot forms.」
- **注意**：顏色只綁 [6] 那一張比較（p098「那根蠟燭」、p099 明說不是每一團都這樣），符合企劃「不能說所有微重力火焰都呈同一形狀或顏色」。p102 照 [4]。

## C18 氧氣來得慢、火燒得沒那麼旺、溫度降；1992 年太空中的蠟燭燒 45 秒到 1 分鐘左右就熄【教材】

- **可用說法**：p105–p108
- **來源**：[4] Student Reader
- **原文**：「Soon, the flame temperature begins to drop because the combustion is less vigorous. The lower temperature slows down the melting and vaporization of the candle wax. Candles onboard the first United States Microgravity Laboratory, launched in June 1992, burned from 45 seconds to about 1 minute before being extinguished because of the dropping temperature and reduction of wax vapor.」
- **注意**：片中不念 USML-1 的名字，也不說太空梭（[4] 這句沒寫載具）。
- **verify-1 F02 修正（2026-11-12）**：原研究 Ross, Dietrich & Tien, "Candle Flames in Microgravity: USML-1 Results – 1 Year Later"（NTRS 20030075810）寫 "Extinction occurred between 40 and 60 seconds for all flames except one"，並把熄滅歸因於小型密閉手套箱與蠟燭盒裡的氧氣耗盡，結論是 "a candle can burn indefinitely in a large enough ambient of air in microgravity"。所以 p108（第一版 p122）改成「大多一分鐘就熄了，可能是裝它的盒子裡氧氣快沒了。」，不把一分鐘說成太空蠟燭的自然上限。

## C19 太空站上的一組實驗：九十五公升左右的燃燒室、液滴自己飄著、熱電線點火、一公釐半到五公釐、三百多次【研究報告】

- **可用說法**：p111–p112（自己飄的一小滴、熱電線點火）。九十五公升的燃燒室、一公釐半到五公釐、三百多次現行版未使用（第一版的 p126、p128–p129 已刪）
- **來源**：[7] §2、§3；[5]
- **原文**：[7]「The cylindrical combustion chamber in the CIR has a free-volume of approximately 95 liters with the MDCA insert installed. The MDCA used an opposed-needle deployment technique to freely deploy droplets of chosen size in microgravity. … Ignition of the free droplet was accomplished using two symmetrically positioned hot-wire igniters.」「Over three hundred droplet combustion tests were completed as part of the FLEX experiments using three different normal alkane fuels and two different alcohol fuels … The droplet initial diameters in these tests varied from approximately 1.5 mm to 5 mm」[5]「FLEX … led to the discovery of a type of cool flame, where the fuel continued "burning" under certain conditions after extinction of the visible flame.」
- **注意**：p111「發現不一定」綁 [5] 的 under certain conditions。不念 FLEX、CIR、MDCA 的名字。（第一版的「三百多次」包含酒精燃料，當時只說「點過三百多次」；現行版已刪。）

## C20 一滴約四公釐的燃料，先燒出看得見的火，約十五秒熄；相機拍不到，量熱的儀器還量到放熱；液滴繼續變小但慢一點；叫冷焰；溫度較低、看不見卻還在燒；最後在某個大小突然停、剩下的只是蒸發；前後常冒出一團霧【研究報告】

- **可用說法**：p113–p125；片頭鉤子 p010「還有一團火熄了以後，儀器卻量到一件怪事」。「前後常冒出一團霧」現行版未使用（第一版的 p143 已刪）
- **來源**：[7] §3.1（R377）、摘要、§1；[5]
- **原文**：[7]「Figure 1a (R377) corresponds to a n-decane droplet with an initial diameter of 4.03 mm burning in 21% oxygen and 79% nitrogen mixture at 0.5 atm pressure. … the diameter of the diffusion flame Df surrounding the droplet increases with time before extinguishing abruptly at around 14.6 seconds.」「The second-stage combustion termed "cool flame" zone starts immediately following hot-flame extinction. As in the hot-flame region the square of the droplet diameter decreases linearly with time in the cool-flame region, but at a slightly slower rate. Both the color camera and the UV-camera are not sensitive enough to register any flame images during this period. Both the broadband and narrowband radiometers, however, register continued radiative heat loss from the droplet indicating active chemical heat release.」「Following cool flame extinction the droplet simply evaporates in the hot environment」摘要：「large n-alkane droplets can continue to burn quasi-steadily following radiative extinction in a low-temperature regime」「A vapor-cloud formed in most cases slightly prior to or following the "cool flame" extinction.」§1「the "cool flame" combustion of the droplet abruptly ends at a finite droplet diameter leaving the unburned droplet to vaporize in the hot ambient.」
- **注意**：「量熱的儀器」＝輻射計（radiometer，量從液滴放出的輻射），**簡化**；「放出熱」照 radiative heat loss … indicating active chemical heat release。p116「相機拍不到火了」（verify-1 F03）、p123「幾乎看不見」（verify-1 S1）是指相機拍不到可見的火焰影像（[5] 的 visible flame 熄了）。p122「比一般的火溫度低」照 low-temperature regime，不給溫度。p118「變小」：原文是直徑平方隨時間直線變小、速率稍慢；不念 0.41、0.33。這是一次試次（R377），p113 說「有一次」。

## C21 冷焰燒出來的東西跟一般的火不一樣；弄懂它也許能做出更省油、汙染更少的車子【官方說明】

- **可用說法**：現行版未使用（第一版的 p144–p145 已在盲評中刪掉）
- **來源**：[5]
- **原文**：「Typical flames produce carbon dioxide and water, but cool flames produce carbon monoxide and formaldehyde. Learning more about the behavior of these chemically different flames could lead to the development of more-efficient, less-polluting vehicles.」
- **注意**：「也許」照 could；不念一氧化碳、甲醛。

## C22 在地上做出的冷焰很快就熄；在微重力裡燒得比較久，科學家才有機會研究；對流會蓋住一些現象，拿掉後比較安靜、好分析【官方說明＋教材】

- **可用說法**：p126–p131
- **來源**：[5]、[4]
- **原文**：[5]「Cool flames produced on Earth quickly flicker out. Since they burn longer in microgravity, scientists have the opportunity to study them.」[4]「One advantage is that the "quieter" and more symmetric microgravity environment makes the experiments easier to model (describe mathematically), thus providing a better arena for testing theories. In addition, eliminating buoyancy-induced flows allows scientists to study phenomena that are obscured by the effects of gravity」
- **注意**：見文首「還缺的來源」。p127 小問問「才看得清楚？」，答案只說到 [5] 的現象，不說「只有」微重力看得到、不解釋燒得久的原因；p130–p131 是 [4] 對所有微重力燃燒研究的一般說法（1997 年，早於冷焰的發現），**不說成冷焰的原因**。「更容易看懂」＝ easier to model 的口語。

## C23 換掉周圍的氣體結局就變：同一種燃料氧從 21% 加到 25%，火更靠近液滴更熱、燒到很小時液滴爆開；減到 17%、14%，熱焰和冷焰都更早熄【研究報告】

- **可用說法**：p134–p135（現行版只留氧氣加多、燒到很小時爆開：p135「像是氧氣多一點，液滴燒到很小時，會自己爆開。」；「同一種燃料、兩成一到兩成五」的數字與氧氣減到 17%、14% 現行版未使用，第一版的 p155、p157–p158 已刪）
- **來源**：[7] §3.1（R374、R379、R383）
- **原文**：「Figure 1b (R374) shows the combustion characteristics for a 3.79 mm n-decane droplet burning at a slightly increased oxygen concentration of 25% … at 0.5 atm pressure. The visible flame diameter initially increases with time and then it decreases until the droplet micro-explodes 26 seconds after ignition. Clearly, the increased ambient oxygen concentration moves the flame closer to the droplet surface … and thus precludes the radiative extinction observed before. Visible flame extinction in this case occurs at much smaller droplet size with a micro-explosion.」「the radiative heat loss from the flame is higher than the previous case due to the increased flame temperature resulting from higher oxygen concentration.」「In general it can be summarized based on the results presented in Fig. 1 that reducing the ambient oxygen concentration leads to earlier hot and cool flame extinctions.」（R379 17%、R383 14%）
- **注意**：這幾次都是正癸烷、0.5 大氣壓，跟 C20 的 R377 同一種燃料（第一版 p155 說「同一種燃料」，現行版已刪）；各次液滴大小不同（3.14–4.03 mm），不說是同一顆。「氧氣多一點」＝ 21% 加到 25%（slightly increased）。p134「同一組實驗」＝同一系列試驗；「換掉周圍的氣體」實際是改變氧氣比例，由 p135 的「像是」帶出這一個例子。

## C24 另一種燃料把氮氣換成氦氣（就是讓氣球飄起來的氣體）；氦氣很會把熱帶走；換到七成五，火點著不到一秒就熄、冷焰也很快結束【研究報告＋常識】

- **可用說法**：現行版未使用（第一版的 p159–p163 已刪）。原本接在後面的小問整理 p136–p137「所以火的樣子，還要看旁邊是什麼氣體！」仍保留，現在只由 C23 的一個例子支持
- **來源**：[7] §3.2（R707）
- **原文**：「In these tests the helium dilution is gradually increased at expense of nitrogen while the oxygen mole fraction is held constant at 0.21.」「When helium dilution was increased to 75% by volume in test R707 … The hot flame that formed during the ignition dies within a fraction of a second and the cool flame burning commences immediately which also ends quickly leaving the droplet to evaporate. The high thermal conductivity of helium leads to large heat loss from the flame zone」
- **注意**（本句前半的行號是第一版，那些句子現行版都已刪）：這是正辛烷、一大氣壓，跟 C23 不同燃料，第一版 p159 說「另一種燃料」（P52-010 覆核的提醒）。「讓氣球飄起來的那種氣體」是**常識**；第一版 p161 小問的錯猜「會讓火飄起來」由 p162 推翻。「很會把熱帶走」＝ high thermal conductivity。小問的結論原本是兩組結果的合理整理；現行版 p136–p137 只由 C23 的一個例子支持，仍不是通用規律。

## C25 片頭與收尾的比喻、看法與留言題【比喻／示意／撰稿】

- p001–p005：小問看到的影片是故事設定，不是指某一支真實影片；她說的「圓圓的、像一顆球」「藍色的」（p095）由 C16、C17 回答，並在 p099 加限定。
- p009–p010：片頭的兩個鉤子，分別在 p072–p075（C12）與 p114–p117（C20）兌現。
- p086「很像，都是比較重的往下擠」、p091–p092、p146–p147、p149：杯子比喻與小問的總結，限度見 C16；收尾原本回收 p009（C12）的「就像井裡那根蠟燭」2026-11-13 已刪。p148–p149 標成所長的看法（「我覺得最妙的是」）。
- 所有插圖（杯子、梯子、大砲、井、太空站、蠟燭、液滴）是 AI 生成的示意，不是實驗照片或實際器材；說明欄寫明。

## C26 太空站失火怎麼滅：要看火的樣子和燒的東西；地上好用的方法到太空可能沒用、甚至讓火更糟；比較大的火在離開太空站、沒有人的貨運太空船上燒；把氣壓調低火蔓延得比較慢；研究用來挑選太空船材料，也讓地上的防火更安全；研究滅火藥劑的實驗發現了冷焰【官方說明＋撰稿推論】

- **可用說法**：p109–p118（2026-11-14 補：小問刪減後量到的正文 451.2 秒低於 480 秒，站主選擇補真內容；接在 C18 的 1992 年蠟燭之後、章尾鉤子 p119–p120 之前）
- **來源**：[5]（2026-11-14 重開：curl GET 200，304,073 bytes，取 `<main>` 轉純文字重讀全文）
- **原文**：
  - 開頭段「Combustion investigations contribute to the safety of crew members, equipment, and spacecraft by guiding selection of spacecraft cabin materials, improving understanding of fire growth, and identifying optimal fire suppression techniques. This research also contributes to fire safety on Earth」
  - BASS 段「Putting out fires in space must consider flame geometry, characteristics of the materials, and methods used to extinguish it, because methods used on the ground could be ineffective or even make the flame worse.」
  - Saffire 段「Saffire is a series of experiments conducted aboard uncrewed Cygnus cargo spacecraft after they depart the station, which makes it possible to test larger fires without putting crew members at risk. Results on flame spread in microgravity can be used to establish the rate of heat release in a spacecraft and show that reducing pressure slows down that spread.」
  - FLEX 段「FLEX, which analyzed the effectiveness of fire suppressants, led to the discovery of a type of cool flame, where the fuel continued "burning" under certain conditions after extinction of the visible flame.」
- **注意**：
  - p110「要看火的樣子和燒的東西」＝ flame geometry、characteristics of the materials（原文還有 methods，由 p111 接上）；p111–p112「可能沒用，甚至讓火更糟」照原文的 could，不說「一定」。
  - p112「所以比較大的火，他們不在太空站上燒」是**撰稿推論**：原文只說 Saffire 在離站後的無人貨運船上做，因而能燒比較大的火、不讓太空人冒險；太空站上仍做小型燃燒實驗（CIR），所以只說「比較大的火」。p113「上面沒有人了」＝ uncrewed、after they depart the station；p114 ＝ test larger fires without putting crew members at risk。片中不念 Saffire、Cygnus 名稱。
  - p115「把艙裡的空氣變稀一點」＝ reducing pressure（給小孩的說法：氣壓低就是同樣大的地方空氣比較少）；「火就蔓延得比較慢」＝ slows down that spread。不給數字。
  - p116–p117「幫忙挑選太空船裡用的材料，也讓地上的防火更安全」＝ guiding selection of spacecraft cabin materials、contributes to fire safety on Earth；不說「挑出不會燒的材料」。
  - p118「有一組研究滅火藥劑的實驗，還發現了一件怪事」＝ FLEX analyzed the effectiveness of fire suppressants, led to the discovery of a type of cool flame；「怪事」由下一章 C19–C20 的冷焰兌現（同一個 FLEX 系列，[7] 的液滴實驗）。不說「意外」。
  - 插圖 cargo-ship（一艘小貨運太空船獨自飄在地球上空）與 cloth-flame（金屬艙裡一條布上爬著一道小火）是示意，不是 Cygnus 或 Saffire 的實際外觀與器材。

## 來源

1. NASA STEM Team〈What Is Microgravity? (Grades 5-8)〉（2012-02-15；Is There Gravity in Space?、Why Do Objects Float in Orbit?、How Can Spacecraft Fall Around Earth?、Can Microgravity Be Found on Earth?），https://www.nasa.gov/learning-resources/for-kids-and-students/what-is-microgravity-grades-5-8/
2. NASA Glenn Research Center〈What is Microgravity?〉（2009-02-13；全文），https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/
3. NASA〈Space Station Facts and Figures〉（International Space Station Facts 段），https://www.nasa.gov/international-space-station/space-station-facts-and-figures/
4. M. J. B. Rogers、G. L. Vogt、M. J. Wargo, *Microgravity: A Teacher's Guide with Activities in Science, Mathematics, and Technology*, NASA EG-1997-08-110-HQ（1997-08；ERIC ED463964），https://files.eric.ed.gov/fulltext/ED463964.pdf
5. NASA Space Station Research Integration Office〈Studying Combustion and Fire Safety〉（2023-12-26；開頭兩段與 CIR／FLEX 段；2026-11-14 為 C26 重讀全文，另用 BASS 與 Saffire 段），https://www.nasa.gov/missions/station/iss-research/studying-combustion-and-fire-safety/
6. NASA〈Candle Flame – 1g vs Microgravity〉（2020-04-30），https://www.nasa.gov/image-article/candle-flame-1g-vs-microgravity/
7. V. Nayagam、D. Dietrich、M. C. Hicks、F. A. Williams, *Cool-flame Extinction During N-Alkane Droplet Combustion in Microgravity*, 2014 Spring Technical Meeting of the Central States Section of the Combustion Institute（NASA NTRS 20140006750），https://ntrs.nasa.gov/citations/20140006750 （原 PDF：https://ntrs.nasa.gov/api/citations/20140006750/downloads/20140006750.pdf）

素材池裡另有 S48 綁的 Ross 等 1994 年 USML-1 原研究（NTRS 20030075810），這次沒有重讀、片中也沒有直接用；1992 年蠟燭的秒數與「只看得到球的一部分」都改用 [4]。
