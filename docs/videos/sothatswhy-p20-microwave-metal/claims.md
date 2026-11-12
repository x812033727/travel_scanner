# 主張與來源（sothatswhy-p20-microwave-metal）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說（行號）、來源原文與注意事項，並標出它是
**官方說明**、**教材**、**專家問答**、**廠商說明書**、**廠商支援頁**、**撰稿推論**、**常識**，還是**比喻／示意**。撰稿只用「可用說法」裡的數字與說法；逐行查核等另一個代理寫 `verify-1.md`。

**行號**以現行 `video.json` 為準（p001–p173，第一版）；`script.md` 是它的可讀版。

## 先看這裡：找不到來源、因此沒講或小心講的事

- **USDA FSIS〈Cooking with Microwave Ovens〉讀不到**：2026-11-12 curl（一般 User-Agent）與 WebFetch 都回 403，跟 2026-09-29 舊查核（`so-thats-why/week7/S13.md`）一樣。搜尋摘要提到「皺的鋁箔會冒火花」「鋁箔不超過食物四分之一」，但沒有讀到原頁，**片中一句都不用 FSIS**。鋁箔的規則只用一本具名的說明書（GE JVM1542，C16），而且明說「這是這一台的規則；你家那台，要看你家的說明書」（p143）；通用的建議只用 FDA 的「一般不要放金屬鍋子或鋁箔」（p136）。
- **企劃點名的兩個缺口**：(1) 尖端與窄縫為什麼集中電場、跳火花——用 OpenStax《College Physics 2e》18.7 與 19.2（大學物理教材，講的是靜電導體）；套到微波爐裡，靠 Bloomfield（維吉尼亞大學物理學教授）講的「微波推著電子在金屬裡來回跑、電子在尖端擠起來、跳進空氣」。教材本身沒有講微波爐，這個連結是**撰稿推論加專家問答**，見 C11–C13。(2) 具名說明書——GE Appliances〈Spacemaker XL Microwave Oven JVM1542 Owner's Manual〉（49-40264），檔案在 GE 自己的 `products-salsify.geappliances.com`。
- **金邊碗為什麼會冒火花**：沒有找到機制來源（GE 與 Amana 只列在會冒火花的東西裡）。片中只說「說明書把金邊的碗，也列在會冒火花的東西裡」（p149），**不解釋原因**。
- **皺鋁箔為什麼會冒火花**：JennAir 支援頁說「Thin, crumpled, or sharply edged metal can concentrate energy and spark」（C14）；「皺一次，就多出很多小尖角」（p112）是撰稿用 C11 的尖端原理接上去的**撰稿推論**。
- **含礦物質的蔬菜也會冒火花**（Amana 有提）：機制沒有來源，片中不提。
- **2.45 GHz、水的共振頻率、發明故事、漏能數字**：舊查核有來源，但本集不講（第二章只講到「推著晃、摩擦生熱」，見 brief.md「長度判斷」）。
- **不做的事**：不示範、不鼓勵放金屬試火花（p119–p120 所長明說不行，說明欄也寫）；不說「金屬其實都可以放」；湯匙只說「通常不會冒火花」（Bloomfield 原話的範圍），不說可以放；不給和 FDA 或說明書相反的通用操作建議。

## 當天重讀的來源（2026-11-12，curl GET；HTML 去標籤轉純文字後逐段讀；PDF 用 `pdftotext`）

- [1] 美國 FDA〈Microwave Ovens〉（Content current as of 10/12/2023）：200（52,965 bytes），讀全文（開頭三段、What is Microwave Radiation、Cooking with Microwaves、Microwave Oven Safety Standard、Checking Ovens、Tips on Safe Microwave Oven Operation）。
- [2] Louis A. Bloomfield（University of Virginia 物理學教授）《How Everything Works》〈Why do metal objects spark/arc in the microwave? Why don't the metal walls of the microwave spark?〉（1997-01-17）：200（63,984 bytes），讀全文。
- [3] Bloomfield〈If a microwave oven door reflects microwaves, why doesn't everything?〉（2009-03-31）：200（64,555 bytes），讀全文。
- [4] OpenStax《College Physics 2e》18.7〈Conductors and Electric Fields in Static Equilibrium〉：200（382,733 bytes），讀全節（含 Electric Fields on Uneven Surfaces、Applications of Conductors 與圖 18.32–18.33 圖說）。
- [5] OpenStax《College Physics 2e》19.2〈Electric Potential in a Uniform Electric Field〉：200（403,396 bytes），讀 Example 19.4 與它後面的 Discussion。
- [6] GE Appliances〈Spacemaker XL Microwave Oven JVM1542 Owner's Manual〉（49-40264，Printed in Korea）：200（677,360 bytes），讀 Safety Instructions（Arcing、Microwave-safe cookware、Foil）、Features、Shelf、Microwave terms、Troubleshooting。
- [7] Amana Product Help〈General Arcing and Sparking - Over-the-Range Microwave〉：200（1,436,662 bytes），讀 Possible Solutions 全部。Amana 是 Whirlpool 集團的品牌。
- [8] JennAir Product Help〈Can Metal or Aluminum Foil be Used in the Microwave〉：200（473,549 bytes），讀全文。JennAir 也是 Whirlpool 集團的品牌。
- 讀不到：USDA FSIS〈Cooking with Microwave Ovens〉（403）；Whirlpool〈General Arcing and Sparking - Built-In Microwave〉（404）。舊查核 `week7/S13.md` 與素材池 LEG-S13 只當線索；上面每一筆都是今天重開。

---

## C01 微波爐裡面是金屬，微波碰到會彈回來；在裡面來回跑，最後被食物吸收【官方說明】

- **可用說法**：p017–p018、p026–p027（p007–p008 的鐵架、p028–p030 推翻小問 p013–p014 的錯猜）
- **來源**：[1]
- **原文**：「they are reflected by metal; they pass through glass, paper, plastic, and similar materials; and they are absorbed by foods.」「The microwaves are reflected within the metal interior of the oven where they are absorbed by food.」「The microwaves reflect off the metal interior of the oven」
- **注意**：p030「所以不是金屬越多，火花就越大」是從「整台都是金屬卻沒冒火花」推出來的**撰稿推論**，C10 再由 Bloomfield「the walls of the oven … without emitting any sparks」支持。

## C02 微波是看不見的波，跟收音機用的電波很像；碰到玻璃、紙、塑膠會穿過去，碰到食物會被吸收【官方說明】

- **可用說法**：p019–p020、p024–p025
- **來源**：[1]
- **原文**：「Microwave ovens heat food using microwaves, a form of electromagnetic radiation similar to radio waves.」三個特性同 C01。
- **注意**：「收音機用的電波」＝ radio waves 的白話；FDA 另說「A radio detects a different portion of the spectrum」。

## C03 爐子裡有一個零件叫磁控管，專門做出微波【官方說明】

- **可用說法**：p021–p023
- **來源**：[1]
- **原文**：「A device called a magnetron inside the oven produces microwaves.」「Microwaves are produced inside the oven by an electron tube called a magnetron.」
- **注意**：「送進放食物的地方」是口語補充（FDA 只說在爐內產生、在金屬內壁反射）；圖 `oven-back` 是示意，不是實際結構。

## C04 門上的網子是金屬；微波的一個波大約十二公分長，網子的洞小很多，微波鑽不過去；洞又讓你看得到裡面【專家問答＋廠商說明書】

- **可用說法**：p009–p010（埋）、p031–p037
- **來源**：[3]、[6]
- **原文**：[3]「That mesh that you see in the door isn't plastic, it's metal. … even though the mesh has holes in it to allow you to observe the food, it acts as a perfect mirror for the microwaves. Basically, the holes are so much smaller than the 12.2-cm wavelength of the 2.45-GHz microwave that the microwave cannot propagate through the holes.」[6] Features：「Window with Metal Shield. Screen allows cooking to be viewed while keeping microwaves confined in the oven.」
- **注意**：12.2 公分說成「大約十二公分」。片中不說 2.45 GHz，也不講可見光的波長（[3] 沒寫），只說洞讓你看得到食物。

## C05 有洞的網子也能把微波彈回去：洞小到擋不住電流，網子就跟一整片金屬一樣【專家問答】

- **可用說法**：p053–p055
- **來源**：[3]
- **原文**：「Electric currents flow through the metal mesh as the microwave hits it and those currents re-radiate the microwave in the reflected direction. Since the holes aren't big enough to disrupt that current flow, the mesh reflects the microwaves as effectively as a solid metal surface would.」
- **注意**：「擋不住電子跑」＝ holes aren't big enough to disrupt that current flow（電流＝電子在跑，接 C09 的白話）。

## C06 門和門框好好的，微波不會漏出來；門關不緊、彎掉就別用；每台都有兩套連鎖開關，門一開就停；開著門還在運轉就立刻停用【官方說明】

- **可用說法**：p038–p044
- **來源**：[1]
- **原文**：「Microwave energy will not leak from a microwave in good condition. A damaged microwave oven may present a risk of microwave energy leaks. Contact your microwave's manufacturer for assistance if your microwave oven has damage to its door hinges, latches, or seals」「Don't operate a microwave oven if the door does not close firmly or is bent, warped, or otherwise damaged.」「The standard also requires all ovens to have two independent interlock systems that stop the production of microwaves the moment the latch is released or the door is opened.」「Stop using a microwave oven if it continues to operate with the door open.」
- **注意**：「門和門框好好的」＝ in good condition／hinges, latches, seals 沒壞的白話。「每台都要有」是美國聯邦標準（21 CFR 1030.10）的要求，片中說「美國食藥署說」，不說台灣的規定。「兩套各自的開關」＝ two independent interlock systems。

## C07 微波推著飯裡的水晃，互相摩擦生熱；水分多的食物（新鮮蔬菜）熱得比較快【官方說明＋簡化】

- **可用說法**：p056–p063
- **來源**：[1]
- **原文**：「The microwaves … cause the water molecules in food to vibrate. This vibration results in friction between molecules, which produces heat that cooks the food.」「That's why foods that are high in water content, like fresh vegetables, can be cooked more quickly than other foods.」
- **注意**：「推著晃」＝ vibrate 的白話；物理上較精確是極性分子跟著電場轉動（舊查核也這樣註），片中不講共振、不講頻率。

## C08 水分子是「水最小最小的一顆」【常識／簡化】

- **可用說法**：p062
- **來源**：常識（FDA [1] 用 water molecules 一詞）
- **注意**：給八歲小孩的**簡化**；不說原子、不說形狀。查核代理請看「最小最小的一顆」是否可接受（水分子是保有水的性質的最小單位）。

## C09 厚的食物外層先被微波加熱，裡面靠外層的熱傳進去；微波的能量熱的是食物、不是整個爐子，所以可能比較省電【官方說明】

- **可用說法**：p064–p070
- **來源**：[1]
- **原文**：「Although heat is produced directly in the food, microwave ovens do not cook food from the "inside out." When thick foods are cooked, the outer layers are heated and cooked primarily by microwaves while the inside is cooked mainly by the conduction of heat from the hot outer layers.」「Microwave cooking can be more energy efficient than conventional cooking because foods cook faster and the energy heats only the food, not the whole oven compartment.」
- **注意**：p067「難怪中間常常冷冷的」是小孩的生活經驗，不是主張。p070「可能比較省電」照 FDA 的 can be more energy efficient（比較對象是一般烹調），保留「可能」。

## C10 玻璃、陶瓷碗微波穿過去，碗本身不會被加熱，但會被熱飯燙熱；有些塑膠盒會被熱飯燙到融化；要用做給微波爐用的容器【官方說明】

- **可用說法**：p071–p076
- **來源**：[1]，交叉 [6]
- **原文**：[1]「Glass, paper, ceramic, or plastic containers are used in microwave cooking because microwaves pass through these materials. Although such containers cannot be heated by microwaves, they can become hot from the heat of the food cooking inside. Some plastic containers should not be used in a microwave oven because they can be melted by the heat of the food inside.」「Use microwave safe cookware specially manufactured for use in the microwave oven.」[6]「Some cookware is labeled "suitable for microwaving."」

## C11 微波推著金屬裡的電子來回跑，牆因此把微波彈回去；細鐵絲可能熱到燒起來；電子在尖端擠成一堆；厚湯匙導電好、留下的熱很少；湯匙通常不冒火花、叉子可能會；牆沒有尖端，只反射不冒火花【專家問答】

- **可用說法**：p045–p052、p077–p082、p099–p107
- **來源**：[2]
- **原文**：「Since an electric field exerts forces on charged particles, a microwave pushes electrons back and forth through any metals it encounters. It is this motion of electrons back and forth through the metal walls of the microwave oven that allow that metal to reflect the microwaves and keep them inside the oven.」「To keep the spoon from overheating, it must be a good conductor of electricity. Since most spoons are pretty thick, the modest currents flowing through them in the microwave will leave little energy inside them and they won't overheat. But a thin twist-tie or small bit of aluminum foil may well overheat and begin to burn.」「Electrons are more likely to leave the end of a metal surface at a sharp point, so avoiding points is important. Most spoons are smooth enough that no sparks will occur. But a fork, a sharp piece of foil, or a twist-tie may well begin to emit electrons into the air as those electrons pile up at one end of the wire while the microwave oven is on.」「Like a spoon, the walls of the oven are good conductors of electricity and they have no sharp points. While electrons move back and forth in these walls, they simply reflect the microwaves without becoming very hot and without emitting any sparks.」
- **注意**：片中第一次說「一位物理學教授說」（p034，C04 的同一位），之後簡稱「物理學教授」「教授」。p046–p048 的「電子」白話（很小、帶電、在金屬裡能到處跑）是**常識／簡化**。原文是 twist-tie（束線鐵絲），片中套到便當盒的鐵絲提把（同樣是細鐵絲、有兩個尖頭），是**撰稿推論**；GE 說明書（C16）也把 wire twist-ties 和 metal handles 一起列出。「湯匙夠厚、頭又圓圓的，通常不會冒火花」＝ most spoons are smooth enough / pretty thick；「叉子就可能會」＝ may well。

## C12 金屬上越尖的地方電荷擠得越多、周圍的推力越強；強到空氣擋不住，就從尖端跳進空氣，變成像閃電一樣的小火花；又平又圓的表面電荷比較不會跑出去；避雷針做尖、高壓電線做平滑【教材＋簡化】

- **可用說法**：p083–p098、p103–p104
- **來源**：[4]，微波爐的部分接 [2]
- **原文**：[4]「Excess charges on a nonuniform conductor become concentrated at the sharpest points. Additionally, excess charge may move on or off the conductor at the sharpest points.」「An uncharged conductor in an originally uniform electric field is polarized, with the most concentrated charge at its most pointed end.」「On a very sharply curved surface, such as shown in Figure 18.32, the charges are so concentrated at the point that the resulting electric field can be great enough to remove them from the surface.」「If the electric field is sufficiently large, the insulating properties of the surrounding material break down and it becomes conducting. For air this occurs at around 3×10^6 N/C. Air ionizes ions and electrons recombine, and we get discharge in the form of lightning sparks and corona discharge.」「Lightning rods work best when they are most pointed. … The induced charge is bled away continually by a lightning rod, preventing the more dramatic lightning strike.」「the conductor should be very smooth and have as large a radius of curvature as possible. … Smooth surfaces are used on high-voltage transmission lines, for example, to avoid leakage of charge into the air.」
- **注意**：「推力」＝電場的**簡化**（電場就是電荷在那裡受到的推拉）；片中不說「電場」這個詞，也不念 3×10⁶ N/C。教材講的是**靜電**（電荷靜止的導體）；微波爐裡電荷來回跑，套用是 Bloomfield [2] 的說法（電子在尖端擠起來、跳進空氣），兩者合起來才是片中的說法。「電荷是那些帶著電的東西，像剛剛的電子」（p090）是簡化（教材的 excess charge 也可以是正電荷）。避雷針「讓電從尖端慢慢流走，比較不會打下大閃電」照教材的 bled away continually / preventing the more dramatic lightning strike，片中說「比較不會」。p104「微波爐的牆又大又平」接 [2] 的 no sharp points。

## C13 兩塊金屬中間的縫越窄，電就越容易跳過去；金屬碰到牆、或靠得很近，也比較容易冒火花【教材＋廠商說明書＋撰稿推論】

- **可用說法**：p113–p118、p126–p128
- **來源**：[5]、[6]、[8]
- **原文**：[5]「it takes about 75 kV to make a spark jump across a 2.5 cm (1 in.) gap, or 150 kV for a 5 cm spark. … A smaller voltage will cause a spark if there are points on the surface, since points create greater fields than smooth surfaces.」[6] Arcing is caused by：「The metal shelf not installed correctly so it touches the microwave wall.」「Metal or foil touching the side of the oven.」[8]「Do not allow aluminum foil or metal to touch the inside cavity walls, ceiling, or floor. Do not allow contact with another metal object during cooking.」
- **注意**：[5] 的意思是「縫越寬，要越大的推力才跳得過去」，片中反過來說「縫越窄，越容易跳」，不念千伏。「碰到牆」有 [6] 的原句；「靠得很近也比較容易冒火花」是把 [5] 的原理套到微波爐的**撰稿推論**，說明書只寫 touch／contact。查核代理請看這句是否要改成「碰到牆、或碰到別的金屬」。

## C14 鋁箔是包東西用的薄金屬片；薄的、皺的、邊很尖的金屬會把能量集中起來冒火花【廠商支援頁＋常識】

- **可用說法**：p108–p112
- **來源**：[8]，交叉 [2]
- **原文**：[8]「Microwaves heat food by exciting water molecules. Metal reflects this energy rather than absorbing it. Thin, crumpled, or sharply edged metal can concentrate energy and spark (arc).」「Thin or wrinkled aluminum foil, or foil touching the cavity walls, floor, or door」「Forks, skewers, or scrunched foil balls with pointed ends」[2]「a sharp piece of foil」
- **注意**：片中說「一家家電公司說」（JennAir，不念名字）。p112「皺一次，就多出很多小尖角」是**撰稿推論**（接 C12 的尖端）。p109 鋁箔的定義是常識。

## C15 金屬架：GE JVM1542 附的架子給大盤子或兩層一起熱；要放對位置、不能碰到牆，不然可能冒火花【廠商說明書】

- **可用說法**：p007–p008（埋）、p121–p128
- **來源**：[6]
- **原文**：Features：「Shelf. Lets you microwave large dishes or several foods at once.」〈Shelf〉「Use the shelf for dishes that are too large to fit on the turntable.」「Make sure the shelf is positioned properly inside the microwave to prevent damage to the oven from arcing.」「Only use the shelf when reheating on more than one level.」Arcing：「The metal shelf not installed correctly so it touches the microwave wall.」
- **注意**：說明書有兩種說法（Features 的 large dishes／several foods，Shelf 頁的 only when reheating on more than one level），片中合成「給大盤子、或兩層一起熱用的」。事務所那台是故事設定，片中說「像這本，是GE一款微波爐的說明書」（p124），**不說事務所的爐子就是 GE**。p122–p123「做這種爐子的公司，把架子設計好，也把用法寫在說明書裡」是撰稿的口語轉場。

## C16 GE JVM1542 說明書：鋁箔只照它寫的方法用、小條遮蓋雞翅尖這類薄的地方、貼緊食物（翹邊像天線）、離爐壁至少 1 英寸；鐵絲和金屬提把要先拿掉；金邊碗會冒火花；沒有金屬邊或光澤的瓷器大多可用；回收紙巾可能有金屬碎片；冒火花先按停止再處理【廠商說明書】

- **可用說法**：p138–p153、p157–p158
- **來源**：[6]
- **原文**：「Use foil only as directed in this manual. … When using foil in the microwave oven, keep the foil at least 1″ away from the sides of the oven.」「When microwaving, you use small strips of foil to shield thin parts, such as the tips of wings and legs on poultry, which would cook before larger parts.」Arcing is caused by：「Foil not molded to food (upturned edges act like antennas).」「Metal, such as twist-ties, poultry pins, or goldrimmed dishes, in the microwave.」「Recycled paper towels containing small metal pieces being used in the microwave.」「Remove wire twist-ties and metal handles from paper or plastic containers before placing them in the oven.」「Most glass casseroles, cooking dishes, measuring cups, custard cups, pottery or china dinnerware which does not have metallic trim or glaze with a metallic sheen can be used.」「If you see arcing, press the CLEAR/OFF pad and correct the problem.」
- **注意**：1 英寸換算「大約兩公分半」（2.54 cm）。「容易過熟」＝ would cook before larger parts。p143 緊接「這是這一台的規則；你家那台，要看你家的說明書」，不把它說成通則。說明書允許 3/4 英寸以下的鋁盒餐，片中**不講**（容易被聽成「金屬都可以」）。CLEAR/OFF 說成「停止」。說明書寫 paper or plastic containers，片中說「紙盒、塑膠盒」。p161 所長把飯倒進白瓷碗、鐵絲盒放旁邊，是照這幾條做的故事動作，不是新主張。

## C17 另一家廠商：有些機型附的架子只能用在烤箱功能，微波時放進去可能冒火花；牆上卡的髒東西可能冒火花；馬上停下來通常不會弄壞爐子【廠商支援頁】

- **可用說法**：p129–p133、p154–p155、p159
- **來源**：[7]
- **原文**：「Metal oven-proof bakeware should only be used during Oven functions such as air fry, toast, bake, convect bake, roast, broil, and dehydrate cycles (on some models). Using the provided accessory racks with microwave function can cause arcing or sparking.」「Soil build-up on cavity walls, microwave cover, cooking rack supports, and the area where the door touches the frame can cause arcing.」「Prolonged arcing can damage the oven. If caught at once, arcing should not damage the oven.」
- **注意**：片中說「另一家廠商」「剛剛那家廠商」「那家廠商」（Amana，不念名字）。這頁是 Amana 有烤箱功能的上掛式微波爐（over-the-range）；「有些機型」照 on some models。「通常不會」＝ should not。

## C18 每台微波爐的說明會寫可以用哪些容器；一般不要放金屬鍋子或鋁箔，因為微波被彈開，食物熱得不平均、還可能弄壞爐子【官方說明】

- **可用說法**：p133–p137
- **來源**：[1]
- **原文**：「Generally, metal pans or aluminum foil should also not be used in a microwave oven, as the microwaves are reflected off these materials causing the food to cook unevenly and possibly damaging the oven. The instructions that come with each microwave oven indicate the kinds of containers to use.」「Follow the manufacturer's instruction manual for recommended operating procedures and safety precautions for your oven model.」
- **注意**：這是全片的通用建議；說明書的鋁箔用法（C16）一定接在這句之後。p120「火花會燒焦東西，還可能弄壞微波爐」：弄壞爐子有 [1] possibly damaging the oven、[7] Prolonged arcing can damage the oven；「燒焦東西」接 [2] 的 overheat and begin to burn，是撰稿的口語合併。

## C19 清潔：用水和溫和的清潔劑常常擦乾淨【官方說明】

- **可用說法**：p156
- **來源**：[1]
- **原文**：「Regularly clean the oven cavity, the outer edge of the cavity, and the door with water and a mild detergent. A special microwave oven cleaner is not necessary. Be sure to not use scouring pads, steel wool, or other abrasives.」
- **注意**：片中沒有提鋼絲絨（原因 FDA 沒寫）。

## C20 水盤比喻【比喻／示意】

- **可用說法**：p049–p052、p061、p084–p086、p102、p116–p117、p128
- **注意**：水盤只說明三件事：(1) 被左右推，裡面的東西就來回跑（C11 的電子被微波推著跑）；(2) 往窄的尖角擠，就堆高、濺出去（C11–C12 的電荷擠在尖端、跳進空氣）；(3) 兩個水盤靠很近，水就濺過去（C13 的窄縫）。
  **限度**：水是有重量的液體、靠人手晃，電子是被微波的電場推；水濺出去不等於空氣變成導體；水盤不說明細鐵絲為什麼會熱。片中第二章所長回答「像水盤那樣晃？」時先說「有點像」（p062），不說一樣。插圖的水盤、火花都是示意。

## C21 故事設定與片尾【故事】

- p001–p006、p161、p170 的滷肉飯、阿嬤、便當盒、鐵架、白碗是故事設定，不是主張。p163–p167 小問的答案是 C11–C13 的白話；p168–p169 所長的看法標成「我覺得」，依據 C01、C04–C05、C11。p171 留言題。

---

## 來源

1. U.S. Food and Drug Administration, Microwave Ovens (content current as of 2023-10-12). https://www.fda.gov/radiation-emitting-products/resources-you-radiation-emitting-products/microwave-ovens
2. Louis A. Bloomfield, How Everything Works, "Why do metal objects spark/arc in the microwave? Why don't the metal walls of the microwave spark?" (1997-01-17). https://howeverythingworks.org/1997/01/17/question-759/
3. Louis A. Bloomfield, How Everything Works, "If a microwave oven door reflects microwaves, why doesn't everything?" (2009-03-31). https://howeverythingworks.org/2009/03/31/question-1579/
4. OpenStax, College Physics 2e, 18.7 Conductors and Electric Fields in Static Equilibrium. https://openstax.org/books/college-physics-2e/pages/18-7-conductors-and-electric-fields-in-static-equilibrium
5. OpenStax, College Physics 2e, 19.2 Electric Potential in a Uniform Electric Field. https://openstax.org/books/college-physics-2e/pages/19-2-electric-potential-in-a-uniform-electric-field
6. GE Appliances, Spacemaker XL Microwave Oven JVM1542 Owner's Manual (49-40264). https://products-salsify.geappliances.com/image/upload/s--BEQq86so--/3842e17e8541177381e364fb66ab5c46460333f5.pdf
7. Amana Product Help, General Arcing and Sparking - Over-the-Range Microwave. https://producthelp.amana.com/Cooking/Microwaves/Over-the-Range_Microwave/General_Arcing_and_Sparking/General_Arcing_and_Sparking_-_Over-the-Range_Microwave
8. JennAir Product Help, Can Metal or Aluminum Foil be Used in the Microwave. https://producthelp.jennair.com/Cooking/Microwaves/Product_Info_new/Product_Information/Can_Metal_or_Aluminum_Foil_be_Used_in_the_Microwave
