# 查核報告 1（sothatswhy-p06-bubble-film）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-10
- 方法：逐句讀 `video.json` 的 206 句台詞（p001–p206），加上 YouTube 標題、說明與縮圖文字（headline「方框吹出／圓泡泡？」、sub「顏色藏在哪一層」）。對照 `claims.md` 的 C01–C25，但不採用它的引文，每個來源都重新打開讀原文（curl 抓 HTML 轉純文字後逐段讀）：
  - Exploratorium（Ron Hipschman）泡泡系列 annex 站五頁：The Shape of Bubbles、Sticky Water、When Bubble Meets Bubble、Bubble Colors、Soap（最後一頁是撰稿沒列的，用來確認「肥皂其實降低表面張力」不跟片中打架）。
  - Exploratorium Science Explorer〈See Colors in Bubbles〉（bub_dome）。
  - Virginia Tech／JMU Bubble Physics 兩頁：Properties of Bubbles、Introduction and Basic Information（Young-Laplace、Plateau Laws）。
  - Wolfram MathWorld〈Double Bubble〉。
  - HyperPhysics〈Soap Film Interference〉與〈Interference in Thin Films〉（相位翻轉），都用 http 打開。
  - University of Colorado Boulder Physics Labs〈Interference in a Soap Film〉（頁面很短，只有 Purpose 一段與圖說）。
  - 補充的較好來源：OpenStax *University Physics Volume 3* §3.4 Interference in Thin Films（泡泡破前變黑、反射相位翻轉、顏色隨角度變）；OpenStax *College Physics 2e* §11.8 Surface Tension（泡泡內壓 P = 4γ/r，越小壓力越大）；Arscott (2013) "Wetting of soap bubbles on hydrophilic, hydrophobic and superhydrophobic surfaces", *Applied Physics Letters* 102, 254103（arXiv:1303.6414 摘要，親水表面上泡泡接觸角 90°＝半球）。
  - Wikipedia Soap film、Soap bubble（raw wikitext，只用來找二級文獻：黑膜厚度引 Pugh (2016) *Bubble and Foam Chemistry*, Cambridge；接觸角引 Teixeira & Teixeira 2009、Arscott 2013；結論不只靠它）。
- 打不開／沒讀到原文的：IUPAC Gold Book「black film」「Newton black film」條（新站被 Cloudflare 擋、舊站 TLS 握手失敗）；Pugh (2016) 原書（未取得，只經 Wikipedia 轉引，只當輔助）；Teixeira & Teixeira (2009) 全文（未讀，只用 Arscott 摘要）。`claims.md` 說讀不到的 exploratorium.edu 主站 Snacks 頁與 AMS 文章，本次也沒有依賴。
- 結論統計（台詞 206 句）：正確 205、需改 1、錯誤 0。另外標題、說明、縮圖 3 項：正確 3、需改 0。另有 4 處選修建議（不影響結論，見文末）。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| F01 | p121（所長） | 對。裡面那道，要多穿過一次皮， | 需改（簡化不精確，數錯一次） | Exploratorium〈Bubble Colors〉："light reflects off both the front (outside) and rear (inside) surfaces of the bubble, but the ray of light that reflects off the inside surface travels a longer distance than the ray which reflects from the outside surface." 裡面那道光是從外面進到皮裡、在內側那面彈回、再從外面出來，**沒有穿過**整層皮；它在皮裡走的是一個來回，也就是多走約兩倍膜厚（`claims.md` C15 的注意自己也寫「來回各走一次」）。「多穿過一次」字面上是「多穿透一次」，小朋友會想成光穿到泡泡裡面去、而且只多一層厚。改成「來回」既對，又讓 p173「斜斜地」的畫面接得上（斜著走一個來回，路線跟著改）。p122「走的路，比外面那道長一點點」照留 | 對。裡面那道，要在皮裡走一個來回，（17 字） |

## 二、逐段核對（正確的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p005 | 方框吹出圓泡泡；顏色一直轉；頭頂變黑就破 | 正確 | Exploratorium Bubble Colors；bub_dome | 小問的觀察；變黑後破："The black film which then appears at the top of the bubble is a harbinger of an upcoming disaster."、"When the soap film looks black, it's just about to pop." |
| p006–p016 | 兩件怪事（形狀、顏色）；預告小泡泡推大泡泡、頂上變黑；答案在那層皮 | 正確 | 同下各段 | 預告句，各在 p080、p155 回收 |
| p017–p021 | 沾泡泡水，框裡有一片薄皮 | 正確 | Exploratorium Shape of Bubbles | "leaving a flat circle of soap in the bubble wand" |
| p022–p023 | 框上那片皮是平的；一吹被撐大，包住一團空氣 | 正確（附註） | 同上 | "A bubble, like a balloon, is a very thin skin surrounding a volume of air." 附註：來源寫圓框；方框是平面框，張在平面框上的最小面積膜就是平面，可留 |
| p024–p026 | 很多水加一點肥皂；肥皂在兩面、水在中間，像三明治 | 正確 | bub_dome | "A bubble film is a sort of sandwich: a layer of soap molecules, a filling of water molecules, and then another layer of soap molecules."；配方 "1 gallon water / 2/3 cup dishwashing soap" |
| p027–p030 | 我的猜法：皮一直想縮小 | 正確 | — | 標成猜法，下面驗證 |
| p031–p033 | 氣球皮被撐開，一放手就把空氣擠出來 | 正確 | Exploratorium Shape of Bubbles | "If you let the mouthpiece of the balloon go free, the rubber skin squeezes the air out of the balloon and it deflates as it flies around the room." 比喻是來源自己用的 |
| p034–p040 | 吹到一半停下，泡泡慢慢縮回，框裡又變回平的皮 | 正確 | 同上 | "The same thing happens if you start blowing a bubble and then stop. … like a balloon it pushes the air out of the bubble, leaving a flat circle of soap in the bubble wand." |
| p041–p042 | 一直往內拉、想縮小的力氣叫表面張力 | 正確（附註，簡化） | Exploratorium Sticky Water；VT Properties；OpenStax CP 11.8 | "the surface molecules tend to be pulled back into the liquid"、"This "stretchy skin" effect is called surface tension."；VT "The driving force behind this shape is the surface tension … attempting to minimize the surface area"。附註：嚴格說是單位長度的力；Exploratorium Soap 頁說肥皂其實把表面張力降到水的約三分之一，片中沒說肥皂增加拉力，不打架 |
| p043–p045 | 離開框後空氣被關住；皮想用最少面積包住 | 正確 | Exploratorium Shape of Bubbles；VT Properties | "tries to shrink the bubble into a shape with the smallest possible surface area for the volume of air it contains"；VT "only a fixed volume" |
| p046–p049 | 方盒子包一樣多空氣，皮大約比圓球多兩成 | 正確（附註） | Exploratorium Shape of Bubbles | 表：同 1 立方英寸，Cube "6 square inches"、Sphere "4.84 square inches"；6÷4.84≈1.24，精確值 (36π)^(1/3)=4.836，多 24%。「大約兩成」是向下取整，有「大約」可留；若要更準可說「兩成多」（見選修 S1） |
| p050 | 所有形狀裡用皮最少的是圓球 | 正確 | 同上；VT Properties | "That shape happens to be a sphere."；"the shape with the minimum surface area is a sphere"。來源表也列四面體到二十面體都比球多 |
| p051–p053 | 才多兩成也要省；能縮就縮 | 正確 | — | 口語收尾 |
| p054–p057 | 不管框什麼形狀，飛出去的泡泡都被拉成圓的（C06） | 正確（附註，推論成立） | VT Properties；Exploratorium Shape of Bubbles | VT："For an enclosed surface with no boundary conditions, only a fixed volume, the shape with the minimum surface area is a sphere." 離開框後框的形狀不再是邊界，條件正好是這一句，推論直接。附註：剛脫離框的一瞬間、或很大的泡泡被風吹時會晃動變形，但很快回到球形；片中說「會被拉成圓的」是講停下來後的樣子，可留 |
| p058–p059 | 氣球皮只是比喻：放完氣皮會鬆，泡泡皮再小都一直在拉 | 正確 | Exploratorium Shape of Bubbles | "Unlike a sheet of rubber that when unstretched loses all tension, a bubble always has its "stretch" no matter how small the surface becomes." 比喻的限度交代得對 |
| p060–p063 | 只說飄在空中、單獨一顆；停在濕盤子上是半顆圓頂（C08） | 正確（附註） | Arscott 2013（APL 摘要）；bub_dome；Wikipedia Soap bubble | Arscott："A hydrophilic surface results in a bubble contact angle of 90 deg"——泡泡皮跟濕表面垂直相交，正好是半球；bub_dome 在沾濕的蓋子上 "blow one big bubble to make a bubble dome"。附註：同一篇說親水表面上 "the bubble angle diminishes with bubble radius"，小泡泡會比半顆再扁一點點；「半顆圓頂」對兒童恰當。撰稿引的 VT「Dry Surface Bubble」講的是浮在液面、底部泡在液體裡的泡泡，不是盤子，本次改以 Arscott 為主要依據 |
| p064–p068 | 兩顆黏在一起是考試；吹兩顆一樣大的碰一下；猜一碰就破 | 正確 | — | 問題與錯猜 |
| p069–p070 | 常常不會破，黏成一對；中間一片共用的平牆（C09） | 正確 | Exploratorium Bubble Meets Bubble；MathWorld | "two bubbles will merge to share a common wall. If the bubbles are the same size …, this wall will be flat."；MathWorld "two equal partial spheres sharing a boundary of a flat disk"。「常常不會破」比來源保守，恰當 |
| p071–p074 | 只碰一點（錯猜）；各包各的皮多，合用一片牆比較省 | 正確 | 同上 | "Since bubbles always try to minimize surface area two bubbles will merge to share a common wall."；MathWorld "using a total surface area that is less than any other boundary"（Hass et al. 1995 證明） |
| p075–p076 | 兩邊一樣大，誰也推不動誰，牆就平平的 | 正確（推論成立） | VT Basic；OpenStax CP 11.8；MathWorld | Δp = 4γ/r：半徑一樣、壓力一樣，兩邊沒有壓力差；MathWorld 分隔面曲率 = 兩泡曲率之差，相等時為零（平面）。撰稿推論與公式一致 |
| p077–p080 | 大的壓扁小的（錯猜）；牆往大泡泡那邊凸 | 正確 | Exploratorium Bubble Meets Bubble；MathWorld | "the smaller bubble, which always has a higher internal pressure, will bulge into the larger bubble."；MathWorld 不等大時分隔面是球面的一部分 |
| p081–p084 | 同一瓶泡泡水皮拉的力氣都差不多；小泡泡彎得厲害，皮往內擠得緊，空氣壓得緊 | 正確（附註，簡化） | VT Basic；OpenStax CP 11.8 | VT："Δp = 4γ/r"（γ 表面張力、r 曲率半徑）；OpenStax "The inward surface tension force causes bubbles to be approximately spherical and raises the pressure of the gas trapped inside"、"the pressure inside a bubble is greatest when the bubble is the smallest." 「皮拉的力氣都差不多」＝同一種液體 γ 相同，是正確的前提；「彎得比較厲害」＝r 小。附註：嚴格說兩顆泡泡的皮可能因膜厚、老化有小差異，「差不多」恰當 |
| p085–p089 | 研究泡泡的人說小泡泡裡壓力比較大，所以它往大的推 | 正確 | Exploratorium Bubble Meets Bubble；OpenStax CP 11.8 | 同上；回收 p013 預告 |
| p090–p092 | 三顆擠在一起，三片牆在中間碰，角度大約 120° | 正確 | Exploratorium Bubble Meets Bubble；VT Properties；VT Basic | "All three bubbles meet at the center at an angle of 120 degrees."；"These films contact symmetrically with one another at 120 degrees."；Plateau Rule 1 "the films can intersect only three at a time, and must do so at 120 degrees." Wikipedia Soap bubble："Since the surface tension is the same in each of the three surfaces, the three angles between them must be equal to 120°."——正是 p082「皮拉的力氣都差不多」的理由，兩段前後一致 |
| p093–p097 | 圓蛋糕切一樣大的三塊，尖角就那麼大 | 正確 | — | 360°÷3 = 120°，比喻 |
| p098–p099 | 一串泡泡，牆交叉的地方是不是都剛好三片 | 正確（附註） | Exploratorium Bubble Meets Bubble；VT Basic | "all of the vertices where three bubble walls meet (and there are always three,) form 120 degree angles"（兩片玻璃中間的泡泡）；VT Rule 1。附註：立體的泡泡堆裡，牆沿著「線」三片三片相交；但在某些「點」上會有四條這種線交在一起（VT Rule 2："no more than 4 Plateau borders to meet at a junction … at most 6 surfaces"）。小朋友一般看的是線，觀察題可留；要更嚴謹見選修 S3 |
| p100–p105 | 泡泡水沒有顏色，倒在手上是透明的 | 正確 | bub_dome | 顏色來自干涉，不是色素 |
| p106–p110 | 皮拉太緊才變彩色（錯猜）；拉力管形狀，顏色找光（C13） | 正確 | Exploratorium Bubble Colors；bub_dome；VT Properties | 兩個 Exploratorium 頁都把顏色歸給 interference；VT："The inconsistencies on the surface move due to the surface tension, causing a change in the local thickness of the bubble and thus the color yielded by the thin-film light interference."——表面張力只會透過改變厚度**間接**影響顏色，顏色本身是光的干涉。片中說拉力「管的是形狀」、顏色另找光，沒說拉力跟顏色完全無關，也沒有在 p151 把打轉歸給拉力，不打架。「很多人會這樣猜」是開場語，不當主張 |
| p111–p115 | 白光是很多顏色混在一起；拿掉一種剩下的帶顏色；拿掉藍偏黃 | 正確 | Exploratorium Bubble Colors；bub_dome | "White light is made up of all colors, all wavelengths. If one of these colors is subtracted from white light (by interference, for instance) we see the complementary color. For example, if blue light is subtracted from white light, we see yellow." |
| p116–p120 | 皮有外面和裡面兩個面，都把一點光彈回眼睛；一顆泡泡兩道光 | 正確 | Exploratorium Bubble Colors；CU Boulder；OpenStax UP3 §3.4 | "light reflects off both the front (outside) and rear (inside) surfaces"；CU "reflections from the front and back surfaces"。「一點光」恰當（每面只反射一小部分） |
| p121 | 要多穿過一次皮 | 見 F01 | — | — |
| p122 | 走的路比外面那道長一點點 | 正確 | Exploratorium Bubble Colors | "travels a longer distance than the ray which reflects from the outside surface" |
| p123–p130 | 池塘同時丟兩顆小石頭；高碰高更高、高碰低抵掉、水面平；公園看過有的地方特別平 | 正確（附註） | bub_dome；Exploratorium Bubble Colors | "If both waves push up on the water, the water moves twice as high … If one wave pushes up and the other pushes down, the two pushes cancel each other and the water doesn't move at all."；"crest-to-crest … crest-to-trough"。「同時丟」是必要條件，寫對了。附註：小問「公園看過」是她自己的經驗，不當主張；池塘兩圈水波碰在一起的抵消區不一定好找，但不會誤導 |
| p131–p133 | 光也可以想成一種波；兩道光一碰，有的顏色加強、有的抵掉 | 正確 | bub_dome | "Light waves, like water waves, can interfere with each other."、"Some waves add together, making certain frequencies or colors of light brighter. Other waves cancel each other, removing a frequency or color from the mixture." |
| p134–p136 | 我的猜法：看皮多厚；厚薄一變多走的路跟著變，抵掉的顏色換一種 | 正確 | Exploratorium Bubble Colors；bub_dome | "Given a certain thickness of the bubble wall, a certain wavelength will be cancelled and its complementary color will be seen."；"that depends on the distance between the layers or the thickness of the soap film"。標成猜法，後面兩個檢驗回收 |
| p137 | 紅色被抵掉，剩下偏藍綠 | 正確 | Exploratorium Bubble Colors | "When red is cancelled, it leaves a blue-green reflection." |
| p138–p143 | 留在框上、頭不動盯著看；顏色變成一條一條橫的 | 正確 | Exploratorium Bubble Colors | "If you let a bubble hang from a bubble wand for awhile, the interference colors begin forming horizontal stripes" |
| p144–p145 | 泡泡水被地球往下拉、慢慢往下流；底下厚、頂上越來越薄，顏色排成條 | 正確 | Exploratorium Bubble Colors；CU Boulder | "because the bubble film is thicker at the bottom than at the top, forming a wedge shape. As the bubble drains, the wedge of bubble solution gets thinner and thinner."；CU "patterns that shift as the film thins under gravity" |
| p146–p148 | 顏色一直往下跑；時間一過皮變薄，顏色一條條往下換；第一個檢驗 | 正確 | 同上 | 頂薄底厚的楔形整體變薄時，同一厚度的位置往下移，色帶就往下走，推論成立；CU 的示範就是色帶隨時間移動 |
| p149–p152 | 風一吹泡泡水在皮裡流來流去，厚薄換位置，顏色打轉 | 正確（附註） | bub_dome | "By causing the liquid bubble film to flow and change in thickness, a puff of wind makes the bubble colors swirl and change." 附註：VT 說表面張力差、蒸發也會推動膜面；片中只講風，避開跟 p109 打架，可接受 |
| p153–p157 | 頂上薄到一個程度，兩道光不管什麼顏色都剛好抵掉；沒有光彈回來，看起來就黑（C20） | 正確（附註，簡化可接受） | Exploratorium Bubble Colors；bub_dome；OpenStax UP3 §3.4；HyperPhysics | 現象：Exploratorium "Eventually the bubble becomes so thin that cancellation occurs for all wavelengths and the bubble appears black against a black background."；bub_dome "looks black because all the reflecting wavelengths of light cancel."；OpenStax "if you observe a soap bubble carefully, you will note it gets dark at the point where it breaks." 原因：Exploratorium、HyperPhysics（"a 180 degree phase change upon reflection from the film surface, but no phase change for the reflection from the back surface"）與 OpenStax 都用外表面反射時「翻面」解釋。判斷：片中只講結果、不講原因，**沒有說錯話**，也沒有把變黑歸給「多走的路剛好差半個波」，所以不算誤導，可留。但要知道它留了一個洞：照 p121–p136 的模型推，皮薄到幾乎沒有厚度時兩道光走的路一樣長，應該「高碰高」變亮，OpenStax 正好把這當成問題提出（"why should they interfere destructively and not constructively? The answer is that a phase change can occur upon reflection"）。若想補一句不加負擔的提示，見選修 S2。「沒有光彈回」：實際上黑膜仍有極微弱的反射，兒童說法可接受；p201 也交代了要深色背景 |
| p158–p160 | 變黑就是快破；我已經薄到快撐不住了 | 正確（附註） | Exploratorium Bubble Colors；bub_dome | "you know the bubble is only about one millionth of an inch thick and will soon pop"；"When the soap film looks black, it's just about to pop." 附註見 p163 |
| p161–p162 | 有一間科學博物館說，這時頂上的皮大約只有一毫米的四萬分之一（C21） | 正確（附註） | Exploratorium Bubble Colors；bub_dome；Wikipedia Soap film（引 Pugh 2016） | Exploratorium 原文 "about one millionth of an inch"；1 英寸 = 25.4 mm，百萬分之一英寸 = 25.4 nm ≈ 1/39,400 mm，「大約四萬分之一」換算正確，而且明說是博物館的說法。附註：bub_dome 另一處寫 "only a few millionths of an inch"；Wikipedia 引 Pugh：黑點 "significantly thinner (< 100 nm)"，"Common black films, around 50 nm"、"Newton black films, around 4 nm"。實際黑膜從幾奈米到幾十奈米都有，25 nm 落在範圍內；片中用「大約」並掛名來源，數量級正確，可留 |
| p163 | 不是一黑就馬上破，常常還會撐一下下 | 正確 | Exploratorium Bubble Colors；Wikipedia Soap film（引 Pugh 2016） | Exploratorium "only a few moments remain until. . .POP!"；Pugh 轉引 "despite its extreme thinness, the final black film can be quite stable and can survive for many minutes." 黑膜有時能撐得比「一下下」更久，片中用「常常」「一下下」是保守說法，沒有說錯，也正好把 p160「快撐不住」拉回來 |
| p164–p170 | 歪頭顏色也變；是不是皮剛好在那一下變薄？沒那麼巧 | 正確 | — | 觀察與推理 |
| p171–p174 | 厚薄沒變，變的是光進來、彈到眼睛的方向；斜著穿過時多走的路跟直直穿過不一樣長（C22） | 正確（附註） | HyperPhysics Soap Film；OpenStax UP3 §3.4 | HyperPhysics："The color seen depends also upon the angle of view."，計算器由入射角經 Snell 定律求膜內角，再求最大反射波長；OpenStax："paint jobs that use thin-film interference to produce colors that change with angle. This expensive option is based on variation of thin-film path length differences with angle." 「不一樣長」正確，而且刻意不說變長：光程差 2nd·cosβ 斜著看反而變短，小朋友直覺會猜變長，不說方向是對的選擇。附註：p173「穿過皮」與 F01 同一種字面問題，但這裡講的是斜著進出的路線，不涉及次數，可留；若 F01 改成「來回」，可順手改成「光斜斜地在皮裡走來回」（選修，不必） |
| p175–p177 | 又是多走的路；第二個檢驗：方向 | 正確 | 同上 | — |
| p178–p181 | 頭不動、顏色慢慢往下流是皮在變薄；泡泡不動、一歪頭顏色就跳是方向在變（C23） | 正確（附註，推論成立） | Exploratorium Bubble Colors；HyperPhysics；OpenStax | 兩個原因各有來源（排液變薄；角度改變光程差），控制一個變因看另一個，方法正確。附註：實際上兩者常同時發生；「歪頭」時眼睛的位置只移動幾公分，泡泡正對你的那一塊顏色變化不大，靠邊、斜著看的部分變化才明顯，「顏色就跳」略誇張但方向正確。另一個更好分的線索是「頭擺回來，顏色也回來」（角度變化可以來回，變薄不會回頭），不必加 |
| p182–p188 | 光看顏色量不準皮多厚；變薄時同一種顏色會出現好幾次，分不出是哪一次；顏色只能當線索，不能當尺 | 正確（附註） | HyperPhysics Soap Film；Exploratorium Bubble Colors；bub_dome | HyperPhysics："you can get an approximate wavelength from a diagram of spectral colors, but there is no simple way to determine what order of reflection you are seeing."、"you see red at three different angles, showing that three orders of reflection have been spanned." 與 Exploratorium 不打架：Exploratorium 開頭說顏色是 "an extremely accurate tool for measuring the thickness of the soap film"，bub_dome 也說 "Each color corresponds to a certain thickness"——那是實驗室裡知道光源、角度，又能從色序數出第幾輪時的用法。片中每一句都加了「光看顏色」，而且 p171–p174 剛講過角度也會改變顏色，所以「只看一張照片的顏色量不準」是對的，說明欄也寫「光看照片上的顏色」。這句不否認顏色跟厚度有關（p182 先說了「顏色跟厚薄有關」），措辭恰當 |
| p189–p196 | 形狀跟顏色是兩件事；小問總結 | 正確 | 同前 | 與已核說法一致 |
| p197–p199 | 所長意見：你看到的顏色就是這層皮正在一點一點變薄的樣子 | 正確（意見已標明） | Exploratorium Bubble Colors；CU Boulder | 有「我覺得」。附註：顏色也受角度影響（p171–p177），但頭不動時顏色變化確實反映變薄，作為意見可留 |
| p200–p202 | 留在框上，背後找深色的牆，看變黑前最後一個顏色 | 正確 | bub_dome；Exploratorium Bubble Colors | "Interference colors on a bubble look brightest when there's white light shining on the bubble and a black background behind it."、"What colors do you see right before the bubble pops?"；"appears black against a black background" |
| p203–p206 | 片尾、留言題、訂閱 | 正確 | — | — |
| YouTube 標題 | 泡泡用方框吹也是圓的，顏色又從哪來？ | 正確 | 同 p054、p131 | — |
| YouTube 說明 | 氣球皮比喻；兩顆一樣大是平牆、一大一小小的往大的推；外面裡面各彈回一道、像池塘水波；時間與眼睛；AI 插圖示意、數字大約、光看照片顏色量不準 | 正確 | 同前 | 與片中核過的說法一致；限度都有交代 |
| 縮圖 | 方框吹出／圓泡泡？／顏色藏在哪一層 | 正確（附註） | — | 「哪一層」對應片中 p016「答案就藏在泡泡外面那一層薄薄的皮裡」，是預告句，不是說皮裡有顏料；片中 p100–p110 明說泡泡水透明、顏色要找光，可留 |

## 三、撰稿者標出的疑點

| 項目 | 結論 |
| --- | --- |
| 1. C06 任何形狀的框，自由後都是圓的 | 正確。VT："For an enclosed surface with no boundary conditions, only a fixed volume, the shape with the minimum surface area is a sphere." 離框後正好是這個條件。剛脫離或被風吹時會晃，但不影響結論 |
| 2. C08 濕盤子上是半顆圓頂 | 正確。改以 Arscott 2013（APL）為依據：親水表面接觸角 90°，就是半球；小泡泡會略扁。VT 的 Dry Surface Bubble 講的是浮在液面的泡泡，不適合當這句的來源 |
| 3. C09「常常不會破」「誰也推不動誰」；小的凸進大的 | 都正確。「常常」比來源保守；等大時 Δp 相同、分隔面曲率 = 兩曲率之差 = 0（MathWorld），「推不動」是 Laplace 壓力的正確兒童說法；小泡泡壓力大（Exploratorium、OpenStax P = 4γ/r） |
| 4. C10「皮拉的力氣都差不多」；三顆 120° | 正確。同一種液體表面張力相同，正是三片牆角度相等（120°）的理由（Wikipedia Soap bubble、VT Plateau Rule 1）。p098 的「三片」對線成立，點上可到六片，選修 S3 |
| 5. C20 不講翻面的變黑 | 可接受，不算誤導：只講結果、沒給錯的原因。但照片中「多走的路」模型推，極薄時應變亮，OpenStax 正把這當問題；可用選修 S2 補一句「比光的波還薄很多」，仍不必講翻面 |
| 6. C21 四萬分之一毫米、「常常還會撐一下下」 | 正確。換算對（25.4 nm），掛名博物館；實際黑膜約 4–50 nm（Pugh 轉引），落在範圍內。黑膜有時能撐好幾分鐘，「常常撐一下下」保守、正確 |
| 7. C22 角度、「不一樣長」 | 正確。HyperPhysics 與 OpenStax 都說顏色隨角度變、因為路程差隨角度變；不說變長變短是對的（光程差斜著反而變短） |
| 8. C23 分辨變薄與角度 | 正確（推論成立）。控制變因的方法對；兩者實際上會同時發生，片中說的是一次只動一個 |
| 9. 顏色不能當尺 vs Exploratorium「很準的量具」 | 不矛盾。片中每句都限定「光看顏色」，HyperPhysics 明說分不出第幾輪；Exploratorium 的「準」是在知道階數與條件的實驗室裡 |
| 10. 表面張力不是顏色的原因；氣球皮比喻與限度；池塘水波 | 都正確。VT 說表面張力只透過改變厚度間接影響顏色；氣球比喻與限度逐字對上 Exploratorium；池塘比喻對上 bub_dome 的水波說法，「同時丟兩顆」寫對了 |
| 其他：方盒子多兩成 | 正確（向下取整，24%），選修 S1 |
| 其他：p121「多穿過一次皮」 | 需改（F01） |

## 建議修改

必改（F01）：

- p121：對。裡面那道，要多穿過一次皮， → 對。裡面那道，要在皮裡走一個來回，（17 字；p122 照留。若插圖 `chief-longer` 畫成光穿透到泡泡內側，一起改成在膜裡折返）

選修（不影響本輪結論）：

- S1 p049：大約比圓球多了兩成。 → 比圓球多了兩成多。（Exploratorium 表 6 ÷ 4.84 ≈ 1.24；p051 小問「才多兩成」可照留）
- S2 p155：頂上的皮薄到一個程度，兩道光不管是什麼顏色， → 頂上的皮比光的波還薄很多，兩道光不管是什麼顏色，（22 字；說出真正的條件「遠比波長薄」，仍不講翻面，p156 照留）
- S3 p098：下次你吹出一串泡泡，看看牆交叉的地方， → 下次你吹出一串泡泡，看看牆跟牆碰在一起的那條線，（22 字；立體泡泡堆裡「點」上可有六片牆，「線」上一定是三片）
- S4（給 `claims.md` 的維護者）C08 改引 Arscott 2013（親水表面接觸角 90°），VT「Dry Surface Bubble」講的是浮在液面的泡泡；C21 補記實際黑膜厚度約 4–50 nm（Pugh 2016，經 Wikipedia 轉引）與黑膜可撐好幾分鐘；C20 補記 OpenStax 指出的「模型推會變亮」問題；C10 補 OpenStax CP 11.8 的 P = 4γ/r。

## 來源

只列查核者這次實際打開並讀到原文的頁面。

```json
[
  {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: The Shape of Bubbles", "url": "https://annex.exploratorium.edu/ronh/bubbles/shape_of_bubbles.html", "checked_on": "2026-11-10"},
  {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: Sticky Water", "url": "https://annex.exploratorium.edu/ronh/bubbles/sticky_water.html", "checked_on": "2026-11-10"},
  {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: When Bubble Meets Bubble", "url": "https://annex.exploratorium.edu/ronh/bubbles/bubble_meets_bubble.html", "checked_on": "2026-11-10"},
  {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: Bubble Colors", "url": "https://annex.exploratorium.edu/ronh/bubbles/bubble_colors.html", "checked_on": "2026-11-10"},
  {"title": "Exploratorium (Ron Hipschman), Soap Bubbles: Soap", "url": "https://annex.exploratorium.edu/ronh/bubbles/soap.html", "checked_on": "2026-11-10"},
  {"title": "Exploratorium Science Explorer, See Colors in Bubbles", "url": "https://annex.exploratorium.edu/science-explorer/bub_dome.html", "checked_on": "2026-11-10"},
  {"title": "Virginia Tech / JMU Bubble Physics, Properties of Bubbles", "url": "https://www1.phys.vt.edu/bubble/properties-of-bubbles.html", "checked_on": "2026-11-10"},
  {"title": "Virginia Tech / JMU Bubble Physics, Introduction and Basic Information", "url": "https://www1.phys.vt.edu/bubble/basic-information.html", "checked_on": "2026-11-10"},
  {"title": "Wolfram MathWorld, Double Bubble", "url": "https://mathworld.wolfram.com/DoubleBubble.html", "checked_on": "2026-11-10"},
  {"title": "HyperPhysics (R. Nave), Soap Film Interference（http）", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/soapfilm.html", "checked_on": "2026-11-10"},
  {"title": "HyperPhysics (R. Nave), Interference in Thin Films / Reflection Phase Change（http）", "url": "http://hyperphysics.phy-astr.gsu.edu/hbase/phyopt/interf.html", "checked_on": "2026-11-10"},
  {"title": "University of Colorado Boulder Physics Labs, Interference in a Soap Film (DCS 6D30.20)", "url": "https://physicslabs.colorado.edu/demos/optics/interference/thin-films/interference-in-a-soap-film/", "checked_on": "2026-11-10"},
  {"title": "OpenStax, University Physics Volume 3, 3.4 Interference in Thin Films", "url": "https://openstax.org/books/university-physics-volume-3/pages/3-4-interference-in-thin-films", "checked_on": "2026-11-10"},
  {"title": "OpenStax, College Physics 2e, 11.8 Cohesion and Adhesion in Liquids: Surface Tension and Capillary Action", "url": "https://openstax.org/books/college-physics-2e/pages/11-8-cohesion-and-adhesion-in-liquids-surface-tension-and-capillary-action", "checked_on": "2026-11-10"},
  {"title": "Arscott (2013), Wetting of soap bubbles on hydrophilic, hydrophobic and superhydrophobic surfaces, Applied Physics Letters 102, 254103（arXiv 摘要）", "url": "https://arxiv.org/abs/1303.6414", "checked_on": "2026-11-10"},
  {"title": "Wikipedia: Soap film（raw wikitext；黑膜厚度引 Pugh 2016）", "url": "https://en.wikipedia.org/wiki/Soap_film", "checked_on": "2026-11-10"},
  {"title": "Wikipedia: Soap bubble（raw wikitext；Plateau 定律、接觸角）", "url": "https://en.wikipedia.org/wiki/Soap_bubble", "checked_on": "2026-11-10"}
]
```
