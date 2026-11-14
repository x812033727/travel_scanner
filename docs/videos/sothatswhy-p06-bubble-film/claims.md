# 主張與來源（sothatswhy-p06-bubble-film）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說（附行號，第一版 2026-11-10）、來源原文與注意事項。
撰稿只能用「可用說法」裡的數字與說法；等另一個代理逐行查核（`verify-1.md`）。
2026-11-10 撰稿時用 curl 讀過每一個來源的原文（HTML 轉成純文字後摘句），引文是原句。方括號數字對應文末〈來源〉。

**讀不到的**：exploratorium.edu 主站的 Snacks 頁（soap-film-painting、soap-bubble-optics）與 AMS 的 Morgan 文章、Feature Column 回 403，沒有用；
同一位作者（Ron Hipschman）的泡泡系列放在 Exploratorium 的 annex 站，讀得到，用它 [1]–[4]。Virginia Tech 的 plateau-laws 頁 404，Plateau 定律改引同站的 basic-information [7]。
HyperPhysics 只有 http 能開（https 憑證不符），`build_scenes.py` 的 `sources` 寫 https 網址以過 `lint`，查核時請用 http 開。

## C01 框上一片平平的皮，一吹就撐大，包住一團空氣

- **可用說法**：小問「框裡就有一片薄薄的皮！」（p021；p020「沾一下泡泡水，」2026-11-13 刪）所長「對，框上那片皮是平平的。你一吹，它就被撐大，包住一團空氣。」（p022–p023）
- **來源**：[1]
- **可信度／注意**：高。Exploratorium [1]：「A bubble, like a balloon, is a very thin skin surrounding a volume of air.」「…it pushes the air out of the bubble, leaving a flat circle of soap in the bubble wand.」
  來源說的是圓框留下「flat circle」；方框上那片皮是平的，是同一件事套到方框（日常可見），**撰稿推論**。

## C02 皮是很多水加一點肥皂；肥皂在兩面、水在中間，像三明治

- **可用說法**：「就是你這瓶泡泡水：很多水，加上一點肥皂。肥皂夾在兩面，水夾在中間，像一片很薄的三明治。」（p025–p026）
- **來源**：[5]
- **可信度／注意**：高。Exploratorium Science Explorer [5]：「A bubble film is a sort of sandwich: a layer of soap molecules, a filling of water molecules, and then another layer of soap molecules.」泡泡水配方「1 gallon water, 2/3 cup dishwashing soap」，所以說「很多水，加上一點肥皂」。
  **簡化**：市售泡泡水常另加甘油等；片中只說小問那瓶的主要成分。

## C03 吹到一半停下來，泡泡會縮回框裡，變回一片平的皮（氣球皮比喻）

- **可用說法**：所長「我的猜法是：這層皮，一直想把自己縮小。」（p029，標成猜法）「你吹過氣球吧？吹大的氣球皮，是被撐開的。一放手，皮就把空氣擠出來。」（p031–p032）「那我們來試：泡泡吹到一半，你停下來不吹，你猜會怎樣？」（p034–p035）「你試試看。泡泡會慢慢縮回去，最後在框裡，又變回一片平平的皮。」（p037–p038）
- **來源**：[1]
- **可信度／注意**：高。Exploratorium [1]：「If you let the mouthpiece of the balloon go free, the rubber skin squeezes the air out of the balloon and it deflates as it flies around the room. The same thing happens if you start blowing a bubble and then stop. The liquid skin of the bubble is stretchy, somewhat like a piece of thin rubber, and like a balloon it pushes the air out of the bubble, leaving a flat circle of soap in the bubble wand.」
  比喻（氣球皮）就是這個來源自己用的比喻。

## C04 一直往內拉、想縮小的力氣叫表面張力

- **可用說法**：「對，這種一直往內拉、想縮小的力氣，科學家叫它表面張力。」（p041–p042）
- **來源**：[2]、[1]、[6]
- **可信度／注意**：高。Exploratorium [2]：「…the surface molecules tend to be pulled back into the liquid.」「This "stretchy skin" effect is called surface tension.」Virginia Tech [6]：「The driving force behind this shape is the surface tension of the bubble interface. This is attempting to minimize the surface area of the bubble.」
  **簡化**：表面張力是單位長度的力（或單位面積的能量），片中說成「往內拉、想縮小的力氣」。

## C05 空氣一樣多，皮想用最少的面積包住；方盒子大約比圓球多兩成的皮；所有形狀裡圓球用的皮最少

- **可用說法**：「泡泡一離開框，那團空氣就被關在裡面了。空氣一樣多，皮卻想用最少的面積把它包住。」（p044–p045）「不划算。包一樣多的空氣，方盒子要的皮，大約比圓球多了兩成。」（p048–p049）「所有形狀裡，用的皮最少的，就是圓球。」（p050）「對泡泡皮來說，能縮就縮，多一點都不肯。」（p053，口語收尾）
- **來源**：[1]、[6]
- **可信度／注意**：高。Exploratorium [1]：「If you blow a bubble and close the opening by flipping the wand over, the tension in the bubble skin tries to shrink the bubble into a shape with the smallest possible surface area for the volume of air it contains. That shape happens to be a sphere.」表：同 1 立方英寸，Cube「6 square inches」、Sphere「4.84 square inches」；6 ÷ 4.84 ≈ 1.24，片中說「大約多兩成」。Virginia Tech [6]：「For an enclosed surface with no boundary conditions, only a fixed volume, the shape with the minimum surface area is a sphere.」

## C06 不管框是什麼形狀，飛出去的泡泡都會被拉成圓的

- **可用說法**：「所以不管框是什麼形狀，飛出去的泡泡，都會被拉成圓的。」（p054–p055）小問「所以我的方框，怎麼吹都是圓的！」（p056–p057）
- **來源**：[1]、[6]（C05 的推論）
- **可信度／注意**：高（推論直接）。離開框後沒有邊界，只剩固定的空氣量（[6] 的條件），最省面積是球（[1]）。框的形狀只決定框上那片皮，**撰稿推論**；圖 `many-wands` 畫方、三角、星形框各飄起一顆圓泡泡，是示意。

## C07 比喻的限制：氣球放完氣皮會鬆，泡泡皮不管縮得多小都一直在拉

- **可用說法**：「先說清楚，氣球皮只是比喻。氣球放完氣，皮會鬆掉；泡泡皮不管縮得多小，都一直在拉。」（p058–p059）
- **來源**：[1]
- **可信度／注意**：高。Exploratorium [1]：「Unlike a sheet of rubber that when unstretched loses all tension, a bubble always has its "stretch" no matter how small the surface becomes.」

## C08 邊界：說的是飄在空中、只有一顆的泡泡；停在濕盤子上是半顆圓頂

- **可用說法**：小問「那泡泡，永遠都是圓的嗎？」所長「不一定。我說的是飄在空中、只有一顆的泡泡。停在濕濕的盤子上，就會變成半顆圓頂。」（p060–p063）
- **來源**：[6]、[5]、[3]
- **可信度／注意**：高。Virginia Tech [6]（Shapes of Bubbles）：停在液面的泡泡「The top is a spherical cap」，底部被壓扁；Exploratorium Science Explorer [5] 的活動：在沾濕的蓋子上「blow one big bubble to make a bubble dome」。兩顆以上黏在一起時不圓，見 C09–C11。舊題查核 `topic-checks/s3-S64-S75.md` 也把標題限定成「飄在空中」。

## C09 兩顆一樣大的泡泡碰在一起，常常會黏成一對，合用一片平的牆，比各包各的省皮

- **可用說法**：「這就是剛剛那個猜法的考試。你從同一瓶，吹兩顆一樣大的泡泡，讓它們碰一下。」（p066–p067）「常常不會破，它們會黏成一對。中間多了一片兩顆一起用的牆，而且是平的。」（p069–p070）「那樣各包各的，皮用得比較多。還是想省皮：兩顆合用一片牆，比較省。」（p073–p074）「兩邊一樣大，誰也推不動誰，牆就平平的。」（p076）
- **來源**：[3]、[8]
- **可信度／注意**：高。Exploratorium [3]：「Since bubbles always try to minimize surface area two bubbles will merge to share a common wall. If the bubbles are the same size as the bubbles to the left, this wall will be flat.」MathWorld [8]：「two equal partial spheres sharing a boundary of a flat disk separate two volumes of air using a total surface area that is less than any other boundary」（Hass et al. 1995 證明）。
  「常常不會破」是保守說法：來源說會合併共用一面牆，沒說一定不破（乾的手、灰塵都可能讓它破）。「誰也推不動誰」是由 C10 的壓力說法推得（兩邊一樣大、壓力一樣），**撰稿推論**。

## C10 一大一小：牆往大泡泡那邊凸；小泡泡裡面壓力比較大

- **可用說法**：「你看，中間那片牆，是往大泡泡那邊凸過去的。」（p080，回收 p013 的預告）「你可以這樣想：同一瓶泡泡水，皮拉的力氣都差不多。可是小泡泡彎得比較厲害，皮往內擠得比較緊，裡面的空氣，就被壓得比較緊。」（p082–p084）「對。研究泡泡的人說，小泡泡裡面的壓力比較大，所以是它往大的那邊推。」（p087–p088）
- **來源**：[3]、[7]、[8]
- **可信度／注意**：高。Exploratorium [3]：「If the bubbles are different sized, the smaller bubble, which always has a higher internal pressure, will bulge into the larger bubble.」Virginia Tech [7]：薄膜的 Young-Laplace 式「Δp = 4γ/r」（γ 表面張力、r 曲率半徑），r 越小壓差越大。MathWorld [8]：分隔面是球面的一部分，「the curvature of the partition is simply the difference of the curvatures of the two bubbles」。
  **簡化**：「皮拉的力氣都差不多」＝同一種泡泡水表面張力相同；「彎得比較厲害」＝曲率半徑小。

## C11 三顆擠在一起：三片牆在中間碰在一起，角度大約一百二十度（圓蛋糕切成一樣大的三塊）

- **可用說法**：「三片牆會在中間碰在一起，碰的角度都差不多一樣，大約一百二十度。」（p091–p092）「像把一個圓蛋糕，切成一樣大的三塊，每一塊尖尖的那個角，就差不多那麼大。」（p094–p095）
- **來源**：[3]、[6]、[7]
- **可信度／注意**：高。Exploratorium [3]：「All three bubbles meet at the center at an angle of 120 degrees.」「…the 120 degree rule always holds, even with complex bubble collections like a foam.」Virginia Tech [6]：「These films contact symmetrically with one another at 120 degrees.」[7] Plateau 第一條：「In a dry foam, the films can intersect only three at a time, and must do so at 120 degrees.」圓 360 度切三等份＝120 度。

## C12 給你的觀察：一串泡泡的牆交叉處，是不是都剛好三片

- **可用說法**：「下次你吹出一串泡泡，看看牆交叉的地方，是不是都剛好三片？」（p098–p099）
- **來源**：[3]、[7]
- **可信度／注意**：高。Exploratorium [3]：「all of the vertices where three bubble walls meet (and there are always three,) form 120 degree angles」（在兩片玻璃中間吹的泡泡）。[7]：乾泡沫的牆三片三片相交。片中只出觀察題、不給答案；濕的泡沫或剛吹出來還在動的泡泡可能看不清楚。

## C13 顏色不是表面張力直接造成的

- **可用說法**：小問「是皮拉得太緊，才變彩色的？」所長「很多人會這樣猜。可是這股往內拉的力氣，管的是形狀，顏色要找另一個角色：光。」（p107–p110）
- **來源**：[4]、[6]
- **可信度／注意**：高。Exploratorium [4] 與 [5] 都把泡泡的顏色歸給干涉（interference colors）。Virginia Tech [6] 說表面張力的差異會讓膜面流動、改變局部厚度，「thus the color yielded by the thin-film light interference」——表面張力只**間接**透過厚度影響顏色。EPISODES.md 的無聊風險也點名「不把表面張力說成彩色的直接原因」。
  **簡化**：「拉力管形狀」是一句話的分工；第四章顏色打轉只說風讓泡泡水流動（C19），沒有說拉力造成顏色，避免前後矛盾。

## C14 白光是很多顏色混在一起；拿掉一種剩下的就帶顏色（拿掉藍偏黃；紅被抵掉偏藍綠）

- **可用說法**：「白光其實是很多種顏色混在一起。要是從裡面拿掉一種，剩下的，就會帶著顏色。」（p112–p113）「比方說，從白光裡拿掉藍色，剩下的看起來就偏黃。」（p115）「比方說，紅色被抵掉，剩下的就偏藍綠。」（p137）
- **來源**：[4]、[5]
- **可信度／注意**：高。Exploratorium [4]：「White light is made up of all colors, all wavelengths. If one of these colors is subtracted from white light (by interference, for instance) we see the complementary color. For example, if blue light is subtracted from white light, we see yellow.」「When red is cancelled, it leaves a blue-green reflection.」[5]：「When white light reflects from a soap film, some of the colors get brighter, and others disappear.」

## C15 皮的外面和裡面兩個面都會反射；裡面那道走的路比較長

- **可用說法**：「這層皮有外面和裡面兩個面。光照過來，兩個面都會把一點光，彈回你的眼睛。」（p117–p118）「對。裡面那道，要多穿過一次皮，走的路，比外面那道長一點點。」（p121–p122）
- **來源**：[4]、[10]
- **可信度／注意**：高。Exploratorium [4]：「light reflects off both the front (outside) and rear (inside) surfaces of the bubble, but the ray of light that reflects off the inside surface travels a longer distance than the ray which reflects from the outside surface.」CU Boulder [10]：「constructive and destructive interference between reflections from the front and back surfaces」。
  **簡化**：「多穿過一次皮」＝裡面那道在膜裡來回各走一次（多走約兩倍膜厚）。

## C16 兩圈水波：高碰高變更高、高碰低互相抵掉；光也可以想成一種波，兩道光一碰有的顏色加強、有的被抵掉

- **可用說法**：「我們用水波來想。你往池塘裡，同時丟兩顆小石頭。兩圈水波碰在一起：高的碰到高的，就變得更高；高的碰到低的，就互相抵掉，水面平平的。」（p125–p127）「對，那就是兩圈水波，互相抵掉的地方。」（p130）「光也可以想成一種波。兩道光一碰，有的顏色被加強，有的顏色被抵掉。」（p131–p132）
- **來源**：[5]、[4]
- **可信度／注意**：高。Exploratorium Science Explorer [5]：「If both waves push up on the water, the water moves twice as high … This is called constructive interference. If one wave pushes up and the other pushes down, the two pushes cancel each other and the water doesn't move at all.」「Light waves, like water waves, can interfere with each other.」「Some waves add together, making certain frequencies or colors of light brighter. Other waves cancel each other, removing a frequency or color from the mixture.」[4]：crest-to-crest、crest-to-trough。
  池塘兩顆石頭是比喻；小問「有的地方特別平」是她自己的觀察。

## C17 所長的猜法：被抵掉哪一種顏色，要看皮有多厚

- **可用說法**：「我的猜法是：要看這層皮有多厚。厚薄一變，裡面那道光多走的路就跟著變，被抵掉的顏色就換一種，你看到的顏色也跟著換。」（p134–p136，標成猜法，第四章檢驗）
- **來源**：[4]、[5]
- **可信度／注意**：高（來源直接這樣說；片中刻意標成猜法，留給第四章兩個檢驗）。Exploratorium [4]：「Given a certain thickness of the bubble wall, a certain wavelength will be cancelled and its complementary color will be seen.」[5]：「The interference colors depend on how far the light waves have to travel before they meet up again--and that depends on the distance between the layers or the thickness of the soap film.」

## C18 泡泡留在框上：泡泡水被往下拉，底下厚、頂上薄，顏色排成橫條，越變越薄、顏色往下換

- **可用說法**：「拿你那一瓶來試。把泡泡吹在框上，先別讓它飛走，頭不要動，盯著它看。」（p140–p141）小問「顏色變成一條一條的，橫橫的！」「對。泡泡水會被地球往下拉，慢慢往下流，底下比較厚，頂上越來越薄，顏色就排成一條一條。」（p142–p145）「時間一過，皮一直變薄，顏色就一條一條往下換。這是第一個檢驗：厚薄變，顏色就變。」（p147–p148）
- **來源**：[4]、[10]
- **可信度／注意**：高。Exploratorium [4]：「If you let a bubble hang from a bubble wand for awhile, the interference colors begin forming horizontal stripes - because the bubble film is thicker at the bottom than at the top, forming a wedge shape. As the bubble drains, the wedge of bubble solution gets thinner and thinner.」CU Boulder [10]：「wavelength-dependent patterns that shift as the film thins under gravity」。
  「顏色一條一條往下換」是把「越變越薄、色帶跟著移動」說成小孩看得到的樣子；來源的示範影像就是色帶隨時間移動。

## C19 顏色會打轉：風一吹，泡泡水在皮裡流來流去，厚薄換位置

- **可用說法**：「風一吹，泡泡水就在皮裡流來流去，厚的薄的換了位置，顏色就跟著打轉。」（p151–p152，回收 p003）
- **來源**：[5]、[6]
- **可信度／注意**：高。Exploratorium Science Explorer [5]：「By causing the liquid bubble film to flow and change in thickness, a puff of wind makes the bubble colors swirl and change.」Virginia Tech [6] 另說表面張力的差異也會推動膜面、改變局部厚度；片中只講風（避開 C13 的矛盾），蒸發等其他原因不講。

## C20 頂上變黑：薄到兩道光不管什麼顏色都剛好抵掉，沒有光彈回來

- **可用說法**：「頂上的皮薄到一個程度，兩道光不管是什麼顏色，都剛好互相抵掉。沒有光彈回你的眼睛，看起來就黑了。」（p155–p157，回收 p014 的預告）
- **來源**：[4]、[5]
- **可信度／注意**：高（現象）；**簡化**（原因）。Exploratorium [4]：「Eventually the bubble becomes so thin that cancellation occurs for all wavelengths and the bubble appears black against a black background.」[5]：「The very thinnest film … looks black because all the reflecting wavelengths of light cancel.」
  [4] 解釋全部抵掉是因為外表面反射時波會「上下翻轉」、內表面不會；片中不講翻轉，只說「薄到一個程度就剛好抵掉」。「看起來就黑了」在深色背景前最明顯（[4] 的「against a black background」），收尾 p201 請觀眾找深色的牆。

## C21 變黑通常就快破了；那時頂上大約一毫米的四萬分之一；不是一黑就馬上破

- **可用說法**：「它在說：我已經薄到快撐不住了。」（p160）「有一間科學博物館說，這時候頂上的皮，大約只有一毫米的四萬分之一。」（p161–p162）「不過不是一黑就馬上破，常常還會撐一下下。」（p163）
- **來源**：[4]、[5]
- **可信度／注意**：高（數量級）。Exploratorium [4]：「When you see this happening at the top of a soap bubble you know the bubble is only about one millionth of an inch thick and will soon pop.」「The black film which then appears at the top of the bubble is a harbinger of an upcoming disaster. The bubble is now so thin only a few moments remain until. . .POP!」[5]：「Right before it pops, the skin of a soap bubble is only one-millionth of an inch thick!」「When the soap film looks black, it's just about to pop.」
  換算：1 英寸 = 25.4 毫米，百萬分之一英寸 = 0.0000254 毫米 ≈ 一毫米的 39,000 分之一，片中說「大約四萬分之一」。[5] 另一處寫「only a few millionths of an inch」，所以只當數量級。
  「不是一黑就馬上破」：`refresh-20261101/new-topics.json` 的 S81 限制寫「不能把黑色區域說成必定立即破裂」；[4] 的「only a few moments remain」支持「還會撐一下下」。**撰稿推論**：黑膜能撐多久沒有來源給數字，片中不給。

## C22 歪頭顏色也變：厚薄沒變，變的是光進來和彈回眼睛的方向；斜著穿過時多走的路不一樣長

- **可用說法**：小問「我一歪頭，顏色也變了耶！」（p165–p167）「對，沒有那麼巧。皮的厚薄沒變，變的是光進來、彈到你眼睛的方向。」（p171–p172）「光斜斜地穿過皮，裡面那道光多走的路，就跟直直穿過的時候不一樣長。」（p173–p174）
- **來源**：[9]
- **可信度／注意**：高（現象）；**簡化**（原因）。HyperPhysics [9]：「The color seen depends also upon the angle of view.」計算器以入射角 α 經 Snell 定律求膜內角 β，再求最大反射的波長；角度一變，最大反射波長就變。
  「多走的路不一樣長」是給兒童的說法：嚴格說是光程差（2nd·cosβ）隨角度改變；斜著看時光程差其實變**短**，片中只說「不一樣長」，不說變長或變短。「歪頭那一下皮沒有變薄」是**撰稿推論**（排液是慢的，C18），由同一顆泡泡的兩種觀察對照。

## C23 怎麼分：頭不動、顏色還在往下流是皮在變薄；泡泡不動、一歪頭顏色就跳是方向在變

- **可用說法**：「頭不動，顏色還在慢慢往下流，是皮在變薄；泡泡不動，你一歪頭顏色就跳，是方向在變。」（p180–p181）
- **來源**：C18、C22 的組合
- **可信度／注意**：**撰稿推論**，是 EPISODES.md 要的「用同一顆泡泡的觀測序列區分膜厚變化與觀看條件」。實際上兩者會同時發生（泡泡也會被風吹動），片中說的是讓一個條件不動、看另一個。

## C24 顏色跟厚薄有關，可是光看顏色量不準皮多厚：同一種顏色會在不同厚度出現好幾次

- **可用說法**：「還有一件事要老實說：顏色跟厚薄有關，可是光看顏色，沒辦法準準地量出皮有多厚。」（p182–p183）「因為皮越變越薄的時候，同一種顏色會出現好幾次，光看顏色，分不出是哪一次。」（p185–p186）「對，所以顏色只能當線索，不能當尺。」（p188）
- **來源**：[9]、[4]
- **可信度／注意**：高。HyperPhysics [9]：「If you see a visible color reflected from a soap film, you can get an approximate wavelength from a diagram of spectral colors, but there is no simple way to determine what order of reflection you are seeing.」「Note that you see red at three different angles, showing that three orders of reflection have been spanned.」Exploratorium [4] 的色序（藍綠 → 藍 → 洋紅 → 黃 → 黑）也只是一輪。
  注意：[4] 開頭說顏色是「an extremely accurate tool for measuring the thickness of the soap film」——那是實驗室知道階數、光源與角度時；EPISODES.md 要求不把拍攝顏色當精確量測，片中照 [9] 說。

## C25 收尾：小問的答案、所長的意見、給你的觀察

- **可用說法**：小問「皮一直想縮小，所以泡泡是圓的；皮多厚、從哪邊看，決定光留下什麼顏色！」（p193–p196）所長「說得好，是你自己連起來的。我覺得最好玩的是：你看到的顏色，其實就是這層皮，正在一點一點變薄的樣子。」（p197–p199，意見標成意見）「好啊。這次把泡泡留在框上，背後找一面深色的牆，看看頂上變黑之前，最後一個顏色是什麼。」（p201–p202）留言題（p204）。
- **來源**：C03–C24 的總結；[4]（深色背景）、[5]（觀察題）
- **可信度／注意**：Exploratorium [5]：「Interference colors on a bubble look brightest when there's white light shining on the bubble and a black background behind it.」「What colors do you see right before the bubble pops?」片中不給答案。

## C26 肥皂不是讓皮拉更緊，反而讓表面張力變小；清水拉太用力又乾得快；肥皂讓皮慢一點乾；封在罐子裡的泡泡撐了三個月

2026-11-14 補長度（站主：補一小段真內容，不灌水）加的一段，放在第一章 p042「科學家叫它表面張力。」之後、p043「那它為什麼要縮成圓的？」之前；三個新鏡頭 `soap-drop`、`straw-water`、`bubble-jar` 都是物件特寫。
新台詞用 `build_scenes.py` 的 `add()` 取新編號 p187–p191，原有的 p001–p186 一個都沒動（i18n 照編號對，新五句要補翻譯）。2026-11-14 用 curl 重讀 [11]、[12] 全文（HTML 轉純文字後摘句）。

- **可用說法**：小問「肥皂是讓皮拉更緊嗎？」（p187，說出常見的錯誤直覺）所長「剛好相反：肥皂讓表面張力，只剩清水的三分之一左右。」（p188）「清水拉得太用力，又乾得快，一下就破。」（p189）「肥皂有點像一層蓋子，讓皮裡的水慢一點乾掉。」（p190）「有人把泡泡封進罐子，不讓它乾，撐了三個月！」（p191）
- **來源**：[11]、[12]
- **可信度／注意**：高（博物館教材）。
  - p187–p188，Exploratorium [11]：「There is a common misconception that water does not have the necessary surface tension to maintain a bubble and that soap increases it, but in fact soap decreases the pull of surface tension - typically to about a third that of plain water.」「三分之一左右」照來源的 typically／about。
  - p189，[11]：「The surface tension in plain water is just too strong for bubbles to last for any length of time. One other problem with pure water bubbles is evaporation: the surface quickly becomes thin, causing them to pop.」
  - p190，[11]：「Because the greasy end of the soap molecule sticks out from the surface of the bubble, the soap film is somewhat protected from evaporation (grease doesn't evaporate) which prolongs the life of the bubble substantially.」「一層蓋子」是**比喻**，來源說 somewhat protected，所以寫「有點像」「慢一點乾」，不說不會乾。
  - p191，[11]：「I've blown soap bubbles on a watchglass glued to the bottom of a jar with a large mouth. Once I've sealed the jar the environment will support the bubble for quite a long time. My longest lasting bubble survived for three months!」[12]：「You must have a good seal or the liquid will escape slowly and the bubble will pop from evaporation.」「My longest lasting bubble survived for 3 months! This bubble never popped.」
    「有人」＝作者 Ron Hipschman 本人；兩頁對另一位 Eiffel Plasterer 的紀錄一頁寫 341 天、一頁寫 342 天，互相不一致，**不用**。罐子裡另加了甘油的長壽配方（[12]），片中不提配方，只說封起來不讓它乾。
  - 圖：`soap-drop` 一碗清水滴進一滴洗碗精、`straw-water` 吸管尖一顆小泡泡破掉、`bubble-jar` 玻璃罐裡小玻璃碟上的一顆泡泡。沒有手、沒有字、沒有並排對照。

## 不講、找不到來源的

- 洗碗油、彩虹大全、蜂巢：依 EPISODES.md 刪減條件不講；Exploratorium [3] 提到蜂巢，片中不用。
- 雙泡泡猜想 2002 年的數學證明（Hutchings、Morgan、Ritoré、Ros）：舊題查核有來源，可是不推進「同一層皮」這一題，不講。
- 為什麼純水吹不出泡泡、肥皂其實把表面張力降到約三分之一（Exploratorium soap 頁）：有來源，但會讓「表面張力」變成兩件事，第一版不講。
- 黑膜到破裂的確切秒數、市售泡泡水的配方：沒有來源給數字，片中不給。
- 光的相位翻轉、光程差公式、階數：只在 C20、C22、C24 的注意裡交代，片中用兒童說法。

## 來源

1. Exploratorium (Ron Hipschman, 1995), Soap Bubbles: The Shape of Bubbles. https://annex.exploratorium.edu/ronh/bubbles/shape_of_bubbles.html（2026-11-10 curl 讀全文）
2. Exploratorium (Ron Hipschman, 1995), Soap Bubbles: Sticky Water. https://annex.exploratorium.edu/ronh/bubbles/sticky_water.html（2026-11-10 curl 讀全文）
3. Exploratorium (Ron Hipschman, 1995), Soap Bubbles: When Bubble Meets Bubble. https://annex.exploratorium.edu/ronh/bubbles/bubble_meets_bubble.html（2026-11-10 curl 讀全文）
4. Exploratorium (Ron Hipschman, 1995), Soap Bubbles: Bubble Colors. https://annex.exploratorium.edu/ronh/bubbles/bubble_colors.html（2026-11-10 curl 讀全文）
5. Exploratorium Science Explorer (1998), See Colors in Bubbles. https://annex.exploratorium.edu/science-explorer/bub_dome.html（2026-11-10 curl 讀全文；`new-topics.json` S81 的來源之一）
6. Virginia Tech / James Madison University, Bubble Physics: Properties of Bubbles. https://www1.phys.vt.edu/bubble/properties-of-bubbles.html（2026-11-10 curl 讀全文；舊題查核 `topic-checks/s3-S64-S75.md` 用過）
7. Virginia Tech / James Madison University, Bubble Physics: Introduction and Basic Information（Young-Laplace、Plateau Laws）. https://www1.phys.vt.edu/bubble/basic-information.html（2026-11-10 curl 讀全文）
8. Wolfram MathWorld, Double Bubble. https://mathworld.wolfram.com/DoubleBubble.html（2026-11-10 curl 讀全文）
9. HyperPhysics (R. Nave, Georgia State University), Soap Film Interference. http://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/soapfilm.html（2026-11-10 用 http 讀全文；https 憑證不符）
10. University of Colorado Boulder, Physics Undergraduate Labs, Interference in a Soap Film（DCS 6D30.20）. https://physicslabs.colorado.edu/demos/optics/interference/thin-films/interference-in-a-soap-film/（2026-11-10 curl 讀全文；`new-topics.json` S81 的來源之一）
11. Exploratorium (Ron Hipschman), Soap Bubbles: Soap. https://annex.exploratorium.edu/ronh/bubbles/soap.html（2026-11-14 curl 讀全文）
12. Exploratorium (Ron Hipschman), Soap Bubbles: Bubble Formulae. https://annex.exploratorium.edu/ronh/bubbles/formulae.html（2026-11-14 curl 讀全文）
