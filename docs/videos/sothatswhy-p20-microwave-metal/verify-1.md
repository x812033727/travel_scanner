# 查核報告 1（sothatswhy-p20-microwave-metal）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-12
- 方法：逐句讀 `video.json` 的 173 句台詞（p001–p173），加上 YouTube 標題、說明、標籤與縮圖文字（headline「微波爐／冒火花？」、sub「同樣是金屬，差在形狀」）。`claims.md` 的 C01–C21 只當線索，不採用它的引文；每個來源當天重新打開（curl GET，HTML 去掉 script／style 與標籤轉純文字後 grep 並讀上下文；PDF 用 `pdftotext -layout` 與 `-raw` 各轉一次對照）：
  - 美國 FDA〈Microwave Ovens〉（200，52,965 bytes；頁尾 "Content current as of: 10/12/2023"），讀全文：開頭三段、What is Microwave Radiation、Cooking with Microwaves、Microwave Oven Safety Standard、Checking Ovens、Tips on Safe Microwave Oven Operation。
  - Bloomfield《How Everything Works》question-759〈Why do metal objects spark/arc in the microwave? …〉（200，63,984 bytes；1997-01-17），讀全文。
  - Bloomfield question-1579〈If a microwave oven door reflects microwaves …〉（200，64,555 bytes；2009-03-31），讀全文。
  - Bloomfield 身分：howeverythingworks.org/biography.html（200）"Louis A. Bloomfield is Professor of Physics at the University of Virginia"。
  - OpenStax《College Physics 2e》§18.7（200，382,733 bytes），讀全節（Electric Fields on Uneven Surfaces、Applications of Conductors、圖 18.31–18.33 圖說）。
  - OpenStax《College Physics 2e》§19.2（200，403,396 bytes），讀 Example 19.4 與它後面的 Discussion。
  - GE Appliances〈Spacemaker XL JVM1542 Owner's Manual〉（GE 自己的 products-salsify 網址，200，677,360 bytes，10 頁 PDF），讀 Safety Instructions（To reduce the risk of fire、Arcing、Microwave-safe cookware、Foil）、Features of the Oven、Other features your model may have／Shelf、Microwave terms。
  - Amana Product Help〈General Arcing and Sparking - Over-the-Range Microwave〉（200，1,436,664 bytes），讀 Possible Solutions 全部。
  - JennAir Product Help〈Can Metal or Aluminum Foil be Used in the Microwave〉（200，473,551 bytes），讀全文。
  - **另找的一手來源**（p097 需要）：美國國家氣象局（NWS）〈Lightning Rods〉https://www.weather.gov/safety/lightning-rods（200，24,890 bytes），讀正文兩段；〈Lightning Myths〉https://www.weather.gov/safety/lightning-myths（200），讀金屬與尖形那一條。
- 打不開／沒讀到原文的：USDA FSIS〈Cooking with Microwave Ovens〉今天 curl 仍是 403（510 bytes），片中也沒用它，不影響結論。UVA 物理系個人頁（physics.virginia.edu 連線被重設；phys.virginia.edu 舊頁寫 "No information about this person is available"），所以「物理學教授」改用 Bloomfield 自己網站的簡介核對。NWS 另外兩個可能談避雷系統的網址（lightning-structures、lightning-protection-systems）都是 404。
- 結論統計（台詞 173 句）：**正確 170、需改 2、錯誤 1**。另外標題、說明、標籤、縮圖 4 項：**正確 3、需改 1（說明欄）**。另有 6 處選修建議（不影響結論，見文末）。
- 錯的 1 句是 **p097（F01）**：「避雷針讓電從尖端慢慢流走，比較不會打下大閃電」。課本確實這樣寫，但美國國家氣象局明說避雷系統 "do not prevent lightning from striking the structure"，而是把打下來的閃電接住、導到地下。小孩會記成「裝了避雷針，閃電就比較不會打下來」，跟現行的防雷說法相反。
- 需改的 2 句：**p102（F02）** 小問說湯匙「晃一晃就好」，所長接「對」，聽起來像「湯匙放進微波爐沒關係」，跟 FDA 與 Amana 的通用建議衝突；**p150（F03）** 把說明書的 "metallic trim" 縮成「金邊」，銀邊的碗會被小孩當成可以用。
- 安全面：全片沒有一句鼓勵小孩自己試（p119–p120 所長明說「不行喔」，說明欄也寫「請不要把金屬放進微波爐試火花」）；鋁箔規則都掛在 GE 那一台名下並緊接 p143「你家那台，要看你家的說明書」；通用建議只用 FDA 的「一般不要放金屬鍋子或鋁箔」。除 F02 外，沒有找到會被聽成「金屬放微波爐沒關係」的句子。
- 字數：下表建議句含標點計算，小問 ≤15、所長 ≤25；建議句不含拉丁字母。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| F01 | p097（所長） | 讓電從尖端慢慢流走，比較不會打下大閃電。 | **錯誤**（課本原文有，但和美國國家氣象局的說明相反，小孩會學到錯的事） | 課本 §18.7："Lightning rods work best when they are most pointed. … The induced charge is bled away continually by a lightning rod, preventing the more dramatic lightning strike." 同一節圖 18.33 圖說較保守："A lightning rod is pointed to facilitate the transfer of charge."　NWS〈Lightning Rods〉："Note that lightning protection systems do not prevent lightning from striking the structure, but rather intercept a lightning strike, provide a conductive path for the harmful electrical discharge to follow … and disperse the energy safely into the ground (grounding network)." 課本那句是「尖端放電可以消掉雷擊」的舊說法；片中照念，等於告訴小孩避雷針讓閃電「比較不會打下來」。保留課本跟氣象局都同意的部分（尖端讓電容易走），再補上閃電打中後順著它進地下。p096「課本說，避雷針就故意做得尖尖的」照留；建議句前半是課本圖說，後半是 NWS，主詞仍可接在「課本說」後面，因為兩者不衝突。插圖 `rod-roof` 沒有畫閃電被擋開，可以照用 | 讓電容易從尖端走；閃電打中它，也會順著它進地下。（24 字） |
| F02 | p102（小問） | 跟大水盤一樣，晃一晃就好！ | 需改（物理比喻對，但「就好」加上 p103 所長的「對」，會被聽成「湯匙放進微波爐沒事」） | Bloomfield 只說會不會冒火花："Most spoons are smooth enough that no sparks will occur." 他講的是在咖啡裡留一支湯匙的情況，不是建議放金屬。廠商與 FDA 的通用說法是不要放金屬：Amana "Metal cookware and bakeware … should not be used in the microwave oven. If used, they could cause sparking or arcing"；FDA "Generally, metal pans or aluminum foil should also not be used in a microwave oven"。p101「通常不會冒火花」已經守住 Bloomfield 的範圍，問題只在小問那句的「就好」是一句評價。改成只描述水盤的樣子，所長的「對」就只是在確認比喻 | 跟大水盤一樣，水比較不會濺！（14 字） |
| F03 | p150（所長） | 沒有金邊、也沒有金屬光澤的陶瓷碗，大多可以用。 | 需改（把說明書的條件縮窄了，銀邊、白金邊的碗也會被當成可以用） | GE JVM1542："Most glass casseroles, cooking dishes, measuring cups, custard cups, pottery or china dinnerware which does not have metallic trim or glaze with a metallic sheen can be used." 原文是 metallic trim（任何金屬的邊），不只是金色。Amana 也寫 "objects with gold or silver trim or a metallic glaze should not be used"。p149 講「金邊的碗」照留（原文 "gold-rimmed dishes"），p150 這句是在說「哪些可以用」，條件要照原文寫全 | 沒有金屬邊、也沒有金屬光澤的陶瓷碗，大多可以用。（24 字） |
| F04 | YouTube 說明欄 | ……鋁箔可以怎麼用、鐵絲提把和金邊碗為什麼要拿開，都照那一台的規則；…… | 需改（片中沒有解釋金邊碗為什麼會冒火花，說明欄寫「為什麼」是說了片中沒給的東西） | 片中 p149 只說「說明書把金邊的碗，也列在會冒火花的東西裡」，`claims.md` 也承認「金邊碗為什麼會冒火花：沒有找到機制來源」。GE 原文只把 "gold-rimmed dishes" 列在 "Arcing is caused by" 之下，沒有說原因 | ……鋁箔可以怎麼用、鐵絲提把和金邊碗要不要拿開，都照那一台的規則；…… |

## 二、逐段核對（正確的句子與依據）

### 開場：便當盒上的鐵絲（p001–p016）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p004 | 阿嬤的滷肉飯、便當盒上一條細鐵絲提把，所長叫小問先別按 | 正確（故事） | GE | 故事設定；先停下來的動作合乎 GE "Remove wire twist-ties and metal handles from paper or plastic containers before placing them in the oven" |
| p005–p006 | 鐵絲放進去「有時候會出問題」 | 正確 | Bloomfield 759；GE | "a thin twist-tie … may well overheat and begin to burn"；GE 把 twist-ties 列在 arcing 原因裡。「有時候」不誇大 |
| p007–p008 | 這台本來就附一個金屬架 | 正確（故事） | GE Features | "Shelf. Lets you microwave large dishes or several foods at once." 事務所那台是故事設定 |
| p009–p012 | 門上一格一格的網子是什麼做的；同樣是金屬，為什麼有的冒火花有的不會 | 正確 | — | 問句與鉤子 |
| p013–p014 | 金屬越多，火花越大 | 正確（錯猜） | — | 小孩的錯猜，p028–p030 推翻 |
| p015–p016 | 裡面的牆亮亮的，是金屬做的嗎 | 正確 | FDA | "the metal interior of the oven" |

### 微波是什麼，牆和門做什麼（p017–p044）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p017–p018 | 美國食藥署說，微波爐裡面是金屬，微波碰到會彈回來 | 正確 | FDA | "they are reflected by metal"；"The microwaves reflect off the metal interior of the oven" |
| p019–p020 | 微波是看不見的波，跟收音機用的電波很像 | 正確 | FDA | "a form of electromagnetic radiation similar to radio waves"；"The human eye can only detect a small portion … A radio detects a different portion of the spectrum" |
| p021–p023 | 爐子裡有一個零件叫磁控管，專門做出微波，送進放食物的地方 | 正確（簡化） | FDA | "A device called a magnetron inside the oven produces microwaves"；"Microwaves are produced inside the oven by an electron tube called a magnetron." 「送進放食物的地方」是口語 |
| p024–p025 | 碰到玻璃、紙、塑膠穿過去；碰到食物被吸收 | 正確 | FDA | "they pass through glass, paper, plastic, and similar materials; and they are absorbed by foods" |
| p026–p027 | 牆讓微波在裡面來回跑，最後被食物吸收 | 正確 | FDA | "The microwaves are reflected within the metal interior of the oven where they are absorbed by food." |
| p028–p030 | 整台都是金屬卻沒冒火花，所以不是金屬越多火花越大 | 正確（撰稿推論，有據） | FDA；Bloomfield 759 | "the walls of the oven … simply reflect the microwaves without becoming very hot and without emitting any sparks" |
| p031–p033 | 門上網子也是金屬；有洞，微波不會跑出來嗎 | 正確 | Bloomfield 1579；GE Features | "That mesh that you see in the door isn't plastic, it's metal."；GE "Window with Metal Shield. Screen allows cooking to be viewed while keeping microwaves confined in the oven." |
| p034–p035 | 一位物理學教授說，微波的一個波大約十二公分長 | 正確 | Bloomfield 1579；Bloomfield 簡介 | "the 12.2-cm wavelength of the 2.45-GHz microwave"；"Professor of Physics at the University of Virginia" |
| p036–p037 | 網子的洞比它小很多，微波鑽不過去；洞又讓你看得到食物 | 正確 | Bloomfield 1579 | "the holes are so much smaller than the 12.2-cm wavelength … that the microwave cannot propagate through the holes"；"the mesh has holes in it to allow you to observe the food" |
| p038–p040 | 美國食藥署說，門和門框好好的，微波不會漏；門關不緊、彎掉就別用 | 正確 | FDA | "Microwave energy will not leak from a microwave in good condition … door hinges, latches, or seals"；"Don't operate a microwave oven if the door does not close firmly or is bent, warped, or otherwise damaged." |
| p041–p043 | 食藥署說，每台都要有兩套各自的開關，門一開就馬上停止做出微波 | 正確 | FDA | "The standard also requires all ovens to have two independent interlock systems that stop the production of microwaves the moment the latch is released or the door is opened." 這是美國聯邦標準 21 CFR 1030.10；片中掛在「食藥署說」底下，沒有說成台灣規定 |
| p044 | 開著門還在運轉，就立刻別用 | 正確 | FDA | "Stop using a microwave oven if it continues to operate with the door open."；"the FDA recommends immediately discontinuing use of the oven" |

### 電子與水盤：牆和網子怎麼彈微波（p045–p055）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p045–p048 | 金屬裡有很多會跑的小東西叫電子；很小、帶電、在金屬裡能到處跑 | 正確（簡化） | Bloomfield 759 | "a microwave pushes electrons back and forth through any metals it encounters"。「在金屬裡能到處跑」是自由電子的白話，給八歲可以 |
| p049–p052 | 物理學教授說，微波推著電子來回跑；像晃水盤；電子在牆裡這樣來回跑，微波就被彈回去 | 正確（比喻有界線） | Bloomfield 759 | "It is this motion of electrons back and forth through the metal walls of the microwave oven that allow that metal to reflect the microwaves and keep them inside the oven." 水盤只示意「被推著來回跑」，見文末 C20 |
| p053–p055 | 教授說，洞小到擋不住電子跑，網子就跟一整片金屬一樣把微波彈回去 | 正確 | Bloomfield 1579 | "Electric currents flow through the metal mesh … Since the holes aren't big enough to disrupt that current flow, the mesh reflects the microwaves as effectively as a solid metal surface would." |

### 微波怎麼把飯變熱、碗與塑膠盒（p056–p076）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p056–p060 | 靠飯裡的水；微波推著水一直晃；食藥署說，水被推著晃、互相摩擦生熱 | 正確（簡化） | FDA | "cause the water molecules in food to vibrate. This vibration results in friction between molecules, which produces heat that cooks the food." |
| p061–p062 | 像水盤那樣晃？有點像；晃的是水分子，水最小最小的一顆 | 正確（簡化） | FDA | FDA 用 water molecules。「有點像」守住比喻的界線；「最小最小的一顆」對八歲可接受（保有水性質的最小單位） |
| p063 | 水分多的食物，像新鮮蔬菜，熱得比較快 | 正確 | FDA | "That's why foods that are high in water content, like fresh vegetables, can be cooked more quickly than other foods." |
| p064–p066 | 不是從中間先熱；食藥署說，厚的食物外層先被微波加熱，裡面靠外面的熱慢慢傳進去 | 正確（簡化） | FDA | "microwave ovens do not cook food from the "inside out." When thick foods are cooked, the outer layers are heated and cooked primarily by microwaves while the inside is cooked mainly by the conduction of heat from the hot outer layers."（「先」見選修 S3） |
| p067–p068 | 難怪中間常冷冷的；整個爐子也會變熱嗎 | 正確 | — | 小孩的生活經驗與問句 |
| p069–p070 | 食藥署說，能量熱的是食物不是整個爐子；所以可能比較省電 | 正確 | FDA | "Microwave cooking can be more energy efficient than conventional cooking because foods cook faster and the energy heats only the food, not the whole oven compartment." 保留「可能」 |
| p071–p073 | 玻璃、陶瓷碗微波穿過去，碗本身不會被加熱；熱飯會把碗燙熱 | 正確 | FDA | "Although such containers cannot be heated by microwaves, they can become hot from the heat of the food cooking inside."（GE 另有「碗變熱就別用」的測試，見選修 S4） |
| p074–p076 | 食藥署說，有些塑膠盒會被熱飯燙到融化；要用做給微波爐用的容器 | 正確 | FDA | "Some plastic containers should not be used in a microwave oven because they can be melted by the heat of the food inside."；"Use microwave safe cookware specially manufactured for use in the microwave oven." |

### 鐵絲、尖端與火花（p077–p101、p103–p120）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p077–p080 | 鐵絲裡的電子也會被推著來回跑；鐵絲很細，又有尖尖的兩頭 | 正確 | Bloomfield 759 | "pushes electrons back and forth through any metals it encounters" |
| p081 | 物理學教授說，細的鐵絲可能熱到燒起來 | 正確（套用） | Bloomfield 759；GE | "a thin twist-tie or small bit of aluminum foil may well overheat and begin to burn"。原文是 twist-tie，片中套到便當盒提把；GE 把 "wire twist-ties and metal handles" 一起列在 "To reduce the risk of fire in the oven cavity" 底下，方向一致，且有「可能」 |
| p082 | 電子容易在尖尖的那頭擠成一堆 | 正確 | Bloomfield 759 | "Electrons are more likely to leave the end of a metal surface at a sharp point"；"those electrons pile up at one end of the wire" |
| p083–p086 | 尖尖的水盤一晃，水擠到尖角、濺出去 | 正確（比喻） | — | 示意，見文末 C20 |
| p087–p088 | 大學的物理課本說，金屬上越尖的地方電荷擠得越多，周圍推力越強 | 正確（簡化） | OpenStax §18.7 | "Excess charges on a nonuniform conductor become concentrated at the sharpest points."；"The electric field is very strong at the point"。「推力」＝電場的白話（C12） |
| p089–p090 | 電荷就是那些帶著電的東西，像剛剛的電子 | 正確（簡化） | — | 教材的 excess charge 也可以是正電荷；對八歲可以 |
| p091–p092 | 推力強到空氣也擋不住，電從尖端跳進空氣，變成一道小火花 | 正確（靜電原理套到微波爐，有專家問答支持） | OpenStax §18.7；Bloomfield 759 | "the charges are so concentrated at the point that the resulting electric field can be great enough to remove them from the surface"；"If the electric field is sufficiently large, the insulating properties of the surrounding material break down … we get discharge in the form of lightning sparks"；Bloomfield "a fork … may well begin to emit electrons into the air as those electrons pile up at one end"。撰稿標的推論（C12）成立：教材講靜電，Bloomfield 把同一件事放進微波爐，片中沒有說得比兩者合起來更多 |
| p093–p094 | 像很小的閃電；課本也說那是像閃電一樣的放電 | 正確 | OpenStax §18.7 | "discharge in the form of lightning sparks and corona discharge" |
| p095–p096 | 尖尖的有好處嗎；課本說避雷針故意做得尖尖的 | 正確 | OpenStax §18.7 | "Lightning rods work best when they are most pointed"；圖說 "A lightning rod is pointed to facilitate the transfer of charge" |
| p097 | 讓電從尖端慢慢流走，比較不會打下大閃電 | **錯誤（F01）** | OpenStax；NWS | 見表一 |
| p098 | 高壓電線做得很平滑，免得電漏到空氣裡 | 正確 | OpenStax §18.7 | "Smooth surfaces are used on high-voltage transmission lines, for example, to avoid leakage of charge into the air." |
| p099–p101 | 物理學教授說，湯匙夠厚、頭又圓圓的，通常不會冒火花；叉子就可能會 | 正確 | Bloomfield 759 | "Most spoons are smooth enough that no sparks will occur. But a fork … may well begin to emit electrons into the air"。「夠厚」原文用在不會過熱，片中合在一起說，p107 再把厚度單獨講清楚，可接受；「通常」「可能」守住範圍 |
| p102 | 跟大水盤一樣，晃一晃就好 | 需改（F02） | Bloomfield；Amana；FDA | 見表一 |
| p103–p104 | 課本說，又平又圓的表面電荷比較不會跑出去；微波爐的牆又大又平，只彈回微波、不冒火花 | 正確 | OpenStax §18.7；Bloomfield 759 | "the conductor should be very smooth and have as large a radius of curvature as possible"；"the walls of the oven are good conductors of electricity and they have no sharp points … without emitting any sparks"（牆上卡髒東西的例外在 p155 補上） |
| p105–p107 | 湯匙裡也有電子在跑，不會熱嗎；教授說厚湯匙導電好，電跑過去留下的熱很少 | 正確 | Bloomfield 759 | "To keep the spoon from overheating, it must be a good conductor of electricity. Since most spoons are pretty thick, the modest currents flowing through them in the microwave will leave little energy inside them" |
| p108–p111 | 鋁箔是包東西用的薄金屬片；一家家電公司說，薄的、皺的、邊很尖的金屬會把能量集中起來冒火花 | 正確 | JennAir | "Thin, crumpled, or sharply edged metal can concentrate energy and spark (arc)." 不念廠商名 |
| p112 | 皺一次，就多出很多小尖角 | 正確（撰稿推論，有據） | JennAir；Bloomfield 759 | 撰稿標為推論（C14）。JennAir 同頁把 "Thin or wrinkled aluminum foil" 與 "scrunched foil balls with pointed ends" 列為風險，Bloomfield 寫 "a sharp piece of foil"；皺褶產生尖角、尖角集中電荷，跟 p087–p092 一致。小孩聽到的是「皺的比較危險」，方向與廠商相同 |
| p113–p115 | 課本說，兩塊金屬中間的縫越窄，電就越容易跳過去 | 正確（換句話說） | OpenStax §19.2 | "it takes about 75 kV to make a spark jump across a 2.5 cm (1 in.) gap, or 150 kV for a 5 cm spark"。縫寬一倍、要的電壓也一倍，反過來就是縫越窄越容易跳；同一段也寫 "A smaller voltage will cause a spark if there are points on the surface"。撰稿標的推論（C13）成立 |
| p116–p117 | 兩個水盤靠很近，水就濺過去 | 正確（比喻） | — | 示意 |
| p118 | 金屬碰到牆、或靠得很近，也比較容易冒火花 | 正確 | GE；JennAir；OpenStax §19.2 | GE "The metal shelf not installed correctly so it touches the microwave wall"、"Metal or foil touching the side of the oven"、"keep the foil at least 1″ away from the sides of the oven"；JennAir "keep at least one inch of clearance from cavity walls and the door"、"Do not allow contact with another metal object during cooking"。`claims.md` 擔心「靠得很近」沒有廠商根據；GE 與 JennAir 都要求離爐壁一英寸，等於把「靠很近」也當成風險，不必改 |
| p119–p120 | 我拿叉子試試看；不行喔，火花會燒焦東西，還可能弄壞微波爐 | 正確（安全句） | JennAir；FDA；Amana | JennAir "Arcing can scorch the cavity, damage interior coatings"；FDA "possibly damaging the oven"；Amana "Prolonged arcing can damage the oven"。明確拒絕小孩試 |

### 說明書與廠商的規則（p121–p159）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p121–p123 | 鐵架怎麼可以；做爐子的公司把架子設計好，用法寫在說明書裡 | 正確（口語轉場） | GE；FDA | GE 的 Shelf 專頁就是用法；FDA "Follow the manufacturer's instruction manual for recommended operating procedures" |
| p124–p125 | GE 一款微波爐的說明書；它附的金屬架是給大盤子、或兩層一起熱用的 | 正確 | GE | Features "Shelf. Lets you microwave large dishes or several foods at once."；Shelf 頁 "Use the shelf for dishes that are too large to fit on the turntable. Only use the shelf when reheating on more than one level." 說明書另註 "features and appearance may vary from your model"，片中說「它附的」以 Features 頁為準，可以 |
| p126–p128 | 架子要放對位置、不能碰到牆，不然可能冒火花；像兩個水盤別靠太近 | 正確 | GE | "Make sure the shelf is positioned properly inside the microwave to prevent damage to the oven from arcing."；"The metal shelf not installed correctly so it touches the microwave wall." |
| p129–p132 | 每台的架子都能微波嗎；另一家廠商說，有些機型附的架子只能用在烤箱功能，微波時放進去可能冒火花 | 正確 | Amana | "Metal oven-proof bakeware should only be used during Oven functions such as air fry, toast, bake … (on some models). Using the provided accessory racks with microwave function can cause arcing or sparking." |
| p133–p135 | 要看是哪一台；食藥署也說，每台微波爐的說明會寫可以用哪些容器 | 正確 | FDA | "The instructions that come with each microwave oven indicate the kinds of containers to use." |
| p136–p137 | 一般不要放金屬鍋子或鋁箔；微波被彈開，飯熱得不平均，還可能弄壞爐子 | 正確 | FDA | "Generally, metal pans or aluminum foil should also not be used in a microwave oven, as the microwaves are reflected off these materials causing the food to cook unevenly and possibly damaging the oven." |
| p138–p140 | 這本說明書說只能照它寫的方法用：小小一條，蓋住雞翅尖那種很薄、容易過熟的地方 | 正確（比原文保守） | GE | "Use foil only as directed in this manual."；Microwave terms／Shielding "you use small strips of foil to shield thin parts, such as the tips of wings and legs on poultry, which would cook before larger parts." 說明書另允許 3/4 英寸以下的鋁盒餐，片中刻意不講，只會讓規則更嚴，不會害人 |
| p141 | 鋁箔要貼緊食物，翹起來的邊就像一根天線 | 正確 | GE | "Foil not molded to food (upturned edges act like antennas)." |
| p142 | 離爐子的牆至少一英寸，大約兩公分半 | 正確 | GE | "keep the foil at least 1″ away from the sides of the oven"；1 英寸＝2.54 公分 |
| p143 | 這是這一台的規則；你家那台要看你家的說明書 | 正確（安全框） | FDA | "Follow the manufacturer's instruction manual … for your oven model." |
| p144–p146 | 說明書寫著：紙盒、塑膠盒上的鐵絲和金屬提把，放進去之前要先拿掉 | 正確 | GE | "Remove wire twist-ties and metal handles from paper or plastic containers before placing them in the oven." |
| p147–p149 | 阿嬤家的碗有一圈金邊；說明書把金邊的碗也列在會冒火花的東西裡 | 正確 | GE | Arcing is caused by "Metal, such as twist-ties, poultry pins, or gold-rimmed dishes, in the microwave." 不解釋原因，正確 |
| p150 | 沒有金邊、也沒有金屬光澤的陶瓷碗，大多可以用 | 需改（F03） | GE；Amana | 見表一 |
| p151–p153 | 還有看不出來的金屬嗎；說明書說，回收紙做的紙巾可能藏著小金屬碎片，也會冒火花 | 正確 | GE | "Recycled paper towels containing small metal pieces being used in the microwave."；"Recycled paper towels, napkins and waxed paper can contain metal flecks which may cause arcing or ignite." |
| p154–p155 | 剛剛那家廠商也說，牆上卡的髒東西可能冒火花 | 正確 | Amana | "Soil build-up on cavity walls, microwave cover, cooking rack supports, and the area where the door touches the frame can cause arcing." |
| p156 | 食藥署建議，用水和溫和的清潔劑常常擦乾淨 | 正確 | FDA | "Regularly clean the oven cavity, the outer edge of the cavity, and the door with water and a mild detergent." |
| p157–p158 | 真的冒火花了呢；說明書說先按停止，再把出問題的東西處理好 | 正確 | GE | "If you see arcing, press the CLEAR/OFF pad and correct the problem." |
| p159 | 那家廠商也說，馬上停下來，通常不會弄壞爐子 | 正確 | Amana | "Prolonged arcing can damage the oven. If caught at once, arcing should not damage the oven." |

### 收尾（p160–p173）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p160–p161 | 滷肉飯倒進白碗、鐵絲盒放旁邊，就可以熱了 | 正確（故事動作） | GE | 照 "Remove wire twist-ties and metal handles" 與 "china dinnerware which does not have metallic trim" 做；插圖 `rice-pour` 是素白碗，一致 |
| p162–p167 | 什麼時候會冒火花；尖尖的、皺皺的、靠得很近的金屬，電子擠在一起就會跳出火花 | 正確（小孩的總結） | Bloomfield 759；OpenStax；JennAir | 對應 p082、p087–p092、p110–p118。「就會」比來源的 may／can 肯定（見選修 S5） |
| p168–p169 | 我覺得最妙的是：把微波關在爐子裡的，正是又大又平的金屬 | 正確（標成意見） | FDA；Bloomfield 759、1579 | 牆與網子都把微波反射回去，且 "no sharp points" |
| p170 | 我要叫阿嬤先拔掉鐵絲 | 正確 | GE | 同 p145–p146 |
| p171–p173 | 你家的微波爐有沒有附架子？留言；訂閱 | 正確 | — | 只是請小孩看一看、留言，不是實驗 |

### 標題、說明、標籤、縮圖

| 項目 | 結論 | 依據 |
| --- | --- | --- |
| 標題「微波爐遇到金屬，什麼時候會冒火花？｜原來如此事務所」 | 正確 | 問句，片中有回答 |
| 說明欄 | 需改一處（F04）；其餘正確 | 電子被推著跑、尖端與皺鋁箔、縫與碰壁、水晃動摩擦生熱、網洞比波長小、GE 架子與鋁箔、Amana 烤箱架、FDA 一般不放金屬與看說明書，逐句對得上上面的來源；「請不要把金屬放進微波爐試火花」「AI 生成的示意插圖，不是實驗的照片」都對 |
| 標籤 | 正確 | 都是主題詞 |
| 縮圖「微波爐／冒火花？」「同樣是金屬，差在形狀」 | 正確（簡化） | 片子的主線就是尖端、皺褶、邊緣對比又大又平的牆與圓頭湯匙（形狀）；碰壁、窄縫、回收紙巾等不在「形狀」裡，但縮圖是鉤子，不是規則（見選修 S6） |

### 水盤比喻（C20）的限度

水盤只出現在三個地方，各自只示意一件事，而且所長在 p062 先說「有點像」：(1) 被左右推，裡面的東西來回跑（p049–p052，對應 Bloomfield 的 "pushes electrons back and forth"）；(2) 尖角的水盤把水擠到尖角、濺出去（p084–p086，對應電荷擠在尖端、跳進空氣）；(3) 兩個水盤靠近，水濺過去（p116–p117、p128，對應窄縫）。不會誤導的理由：片中沒有用水盤解釋細鐵絲為什麼會熱（p081 另外引教授）、沒有說火花就是電子「潑出去」本身（p091–p092 用課本說「空氣也擋不住」），也沒有拿水盤去推「大的平的金屬就可以放」。唯一的風險是 p102 小問用大水盤得出「晃一晃就好」，已列為 F02。同一個水盤先比電子、後比水分子（p061），所長用「有點像」區隔，可留。

## 建議修改

必改：

- F01 p097（所長）：讓電從尖端慢慢流走，比較不會打下大閃電。 → 讓電容易從尖端走；閃電打中它，也會順著它進地下。（24 字）
- F02 p102（小問）：跟大水盤一樣，晃一晃就好！ → 跟大水盤一樣，水比較不會濺！（14 字）
- F03 p150（所長）：沒有金邊、也沒有金屬光澤的陶瓷碗，大多可以用。 → 沒有金屬邊、也沒有金屬光澤的陶瓷碗，大多可以用。（24 字）
- F04 說明欄：「鐵絲提把和金邊碗為什麼要拿開」 → 「鐵絲提把和金邊碗要不要拿開」

改 F01 時請一起改 `claims.md` 的 C12（補上 NWS〈Lightning Rods〉"do not prevent lightning from striking the structure, but rather intercept a lightning strike" 與網址，並把 p097 的說法改成課本圖說 "pointed to facilitate the transfer of charge"），以及 `script.md` 與 `build_scenes.py` 的同一行；F03 請一起改 C16 的「金邊碗」為「金屬邊（metallic trim）」。本次查核依指示只寫 verify-1.md。

選修（不影響本輪結論）：

- S1 p096 的「課本說」：F01 改完後，p097 後半其實是氣象局的說法。若想主詞完全乾淨，可把 p096 改成「有。避雷針就故意做得尖尖的，」（14 字），尖端那一點已經在 p087 歸給課本。
- S2 p081「細的鐵絲，可能熱到燒起來」：Bloomfield 說的 twist-tie 是包了紙或塑膠的細鐵絲，「燒起來」主要是外皮與旁邊的紙盒；便當盒提把通常比 twist-tie 粗。片中有「可能」，又有 GE 把提把列在防火段落，可留。若想更準，可改成「物理學教授說，細的鐵絲，可能熱到把旁邊燒焦；」（22 字）。
- S3 p065「外面那層先被微波加熱」：FDA 原文是 "primarily by microwaves"（主要靠微波），不是時間上的「先」。對小孩「外面先熱、裡面後熱」的結果沒有錯，可留；要更貼原文可改「厚的食物，外面那層主要靠微波加熱，」並保留「不是。食藥署說，」（整句 25 字）。
- S4 p072「碗本身不會被加熱」：照 FDA 原文 "cannot be heated by microwaves"，可留。GE 說明書另給一個測試（"If the dish heats, it should not be used for microwaving"），表示有些碗其實會被加熱；本集不必講，若之後有留言問可以這樣回答。
- S5 p167「就會跳出火花！」：來源都是 may／can。小孩的總結可以肯定一點；若要一致，可改「就可能跳出火花！」（8 字）。
- S6 縮圖 sub「同樣是金屬，差在形狀」：可留。若想把碰壁與窄縫也包進去，可改「同樣是金屬，差在形狀和距離」，但字數變長，縮圖可讀性要另外看。
