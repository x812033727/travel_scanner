# 查核報告 2（sothatswhy-p20-microwave-metal）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有寫 verify-1.md）
- 日期：2026-11-12
- 範圍：verify-1.md 之後，經 verify-1 修正與三輪盲評改寫的 23 句台詞（現行 `video.json` 的 p002、p024、p046、p061、p081、p082、p086、p088、p092、p093、p099、p100、p101、p104、p115、p116、p117、p127、p131、p149、p150、p156、p161），每句連前後一句讀；刪掉的句子有沒有讓別句失去前提；有沒有哪一句會被聽成「金屬放微波爐沒關係」或鼓勵小孩自己試；YouTube 說明欄、標籤、縮圖與參考資料是否還跟片子一致；字數與拉丁字母；`claims.md` 各列行號對不對得上。其餘台詞沒有重查，結論沿用 verify-1.md。
- 比對方法：把 verify-1 查的第一版（session 暫存的 `p20/v0.json`，173 句，p001–p173）跟現行版（165 句，p001–p165）逐句 diff（difflib 對台詞文字）。結果與任務單一致：
  - 新增 10 句：p081–p082（叉子四個尖頭，取代避雷針段）、p092–p093（細鐵絲對厚湯匙）、p099–p101（平的鋁箔）、p117（JennAir：金屬別碰別的金屬）、p149–p150（冒火花後怎麼處理）。
  - 改寫 13 句：舊 p002→p002、舊 p024→p024（加「陶瓷」）、舊 p050→p046、舊 p072→p061、舊 p102→p086（verify-1 F02）、舊 p104→p088、舊 p115→p104、舊 p126–p127→p115–p116、舊 p137→p127、舊 p141→p131、舊 p164→p156、舊 p169→p161。
  - 刪掉 18 句：舊 p041–p044（開門那一下、兩套連鎖開關、開著門還在運轉）、舊 p064–p070（厚食物外層先熱、熱的是食物不是爐子、比較省電）、舊 p074–p076（塑膠盒會融化、要用微波專用容器）、舊 p095–p098（避雷針與高壓電線，含 verify-1 F01 那一句）。173 − 18 + 10 = 165。
  - 另有一句不在任務清單但也跟 v0 不同：p140（舊 p150）「沒有金屬邊、也沒有金屬光澤的陶瓷碗，大多可以用。」就是 verify-1 F03 的建議句，照改了。
- verify-1 的四項必改都已處理：F01（避雷針）整段刪掉；F02 p086 改成「水不太會濺」，不再有「就好」；F03 p140 照建議句；F04 說明欄改成「鐵絲提把和金邊碗要不要拿開」。
- 來源：`claims.md` 只當線索，不採用它的引文。今天在新的空目錄重新 curl GET（全部 200），HTML 去掉 script／style 與標籤轉純文字後 grep 並讀上下文，PDF 用 `pdftotext -layout` 與 `-raw` 各轉一次對照：
  - 美國 FDA〈Microwave Ovens〉（200，52,965 bytes；頁尾 "Content current as of: 10/12/2023"）
  - Bloomfield《How Everything Works》question-759（200，63,984 bytes；1997-01-17）
  - Bloomfield question-1579（200，64,555 bytes；2009-03-31）
  - Bloomfield 身分：howeverythingworks.org/biography.html（200）"is Professor of Physics at the University of Virginia"
  - OpenStax《College Physics 2e》§18.7（200，382,733 bytes）
  - OpenStax《College Physics 2e》§19.2（200，403,396 bytes）
  - GE Appliances〈Spacemaker XL JVM1542 Owner's Manual〉（GE 的 products-salsify 網址，200，677,360 bytes）
  - Amana Product Help〈General Arcing and Sparking - Over-the-Range Microwave〉（200，1,436,664 bytes）
  - JennAir Product Help〈Can Metal or Aluminum Foil be Used in the Microwave〉（200，473,551 bytes）
- 結論統計（23 句）：**正確 22、需改 1、錯誤 0**。說明欄、標籤、縮圖、參考資料 4 項：**正確 4**。另有 7 處選修建議（不影響結論，見文末）。
- 字數：全部 165 句含標點計算，小問最長 15 字（p086）、所長最長 24 字（p061、p087、p140），沒有超過上限（小問 15、所長 25）。拉丁字母只有 p113 的「GE」，`build_scenes.py` 的 SAY 表把它念成「G E」（`say` 欄位有值，`say_for` = 9764f48174a7，跟原句 NFC 後的 sha256 前 12 碼相符）；其餘台詞沒有拉丁字母，也沒有阿拉伯數字。下文建議句也照同一算法。

## 一、需改的地方與理由

| 編號 | 行 | 現行台詞 | 結論 | 依據與理由 |
| --- | --- | --- | --- | --- |
| F01 | p150（所長） | 像拿掉鐵絲、把架子放正、把鋁箔貼緊。 | 需改（事實對，但對八歲的觀眾少了「請大人來」） | GE 說明書 Safety："If you see arcing, press the CLEAR/OFF pad and correct the problem."；Arcing is caused by 的三項各對到這三個動作（"twist-ties"、"The metal shelf not installed correctly so it touches the microwave wall"、"Foil not molded to food"），所以三個例子都有出處。問題在語境：這句回答小問 p149「怎麼處理？」，聽起來是她自己伸手進去拿。同一本說明書寫架子 "Use pot holders when handling the shelf—it may be hot."，片中 p067、p093 也才說細鐵絲「可能熱到燒起來」；說明書另寫 "If materials inside the oven should ignite, keep the oven door closed, turn the oven off … If the door is opened, the fire may spread."。冒過火花的金屬可能是燙的，而且片中沒有分「冒火花」和「燒起來」。跟 verify-1 F02 同類：事實對，可是小孩可能照著做錯 |

## 二、逐句核對

| 行 | 現行台詞 | 結論 | 來源 | 依據摘要與前後文 |
| --- | --- | --- | --- | --- |
| p002（小問） | 我拿去事務所的微波爐熱喔！ | 正確（故事） | — | 沒有事實主張。前句 p001「阿嬤做的滷肉飯！」，後句 p003「等一下，先別按」；「事務所的微波爐」讓 p006「這台微波爐」、p008「這台本來就附了一個金屬架」有明確指涉 |
| p024（所長） | 微波碰到玻璃、陶瓷、紙、塑膠，會穿過去； | 正確 | FDA | "Glass, paper, ceramic, or plastic containers are used in microwave cooking because microwaves pass through these materials."（開頭段的三個特性只列 glass, paper, plastic，陶瓷在 Cooking with Microwaves 這句）。前句 p023 磁控管送出微波，後句 p025「碰到食物，會被食物吸收」＝"they are absorbed by foods"。加「陶瓷」讓 p061 的回呼有前文 |
| p046（所長） | 就像我端著這個圓圓的水盤，左右晃一晃。 | 正確（比喻） | Bloomfield 759 | 比喻前句 p045「微波會推著它們來回跑」＝"a microwave pushes electrons back and forth through any metals it encounters"。「圓圓的」先把水盤的形狀講出來，p070「這個尖尖的水盤」、p086「圓圓的水盤」才有對照；圖 `chief-tray-up` 寫的是 "smooth round ends"，相符。比喻的限度見 claims C20 |
| p061（所長） | 還記得嗎？陶瓷會讓微波穿過去，碗自己不會被加熱。 | 正確 | FDA | "Although such containers cannot be heated by microwaves, they can become hot from the heat of the food cooking inside."「還記得嗎」回呼 p024（現在有「陶瓷」），不是重講。前句 p060「那碗會被微波加熱嗎？」，後句 p062「熱的飯會把碗燙熱」＝後半句原文。p139–p140 再補金邊碗的例外，不衝突（verify-1 S4 的「有些碗其實會熱」仍可留） |
| p081（小問） | 叉子有四個尖尖的頭耶！ | 正確（小孩的觀察） | — | 沒有事實主張（一般餐叉四齒；圖 `chief-prongs` 也是 "four slim prongs"）。前句 p080「課本也說，那是像閃電一樣的放電」，接得上：剛講完尖端放電，小孩聯想到開場 p011 的叉子 |
| p082（所長） | 對，每一個尖頭，都是電荷會擠過去的地方。 | 正確（教材＋專家，撰稿推論） | OpenStax §18.7；Bloomfield 759 | §18.7："Excess charges on a nonuniform conductor become concentrated at the sharpest points."（複數）、"An uncharged conductor in an originally uniform electric field is polarized, with the most concentrated charge at its most pointed end."；Bloomfield："a fork … may well begin to emit electrons into the air as those electrons pile up at one end"。沒有說「尖頭越多火花越大」，也沒有說每個尖頭一定冒火花。後句 p083「那湯匙呢？」→ p084–p085 回收 p011 的叉子與湯匙。取代避雷針段後，C12 的尖端原理直接回到片子的物件，沒有離題 |
| p086（小問） | 跟圓圓的水盤一樣，水不太會濺！ | 正確（比喻；verify-1 F02 已解決） | Bloomfield 759；OpenStax §18.7 | 前句 p085「通常不會冒火花；叉子就可能會」＝"Most spoons are smooth enough that no sparks will occur. But a fork … may well begin to emit electrons"。小孩只說水不太會濺（對應不太會冒火花），不再說「晃一晃就好」，不會被聽成「湯匙放進去沒事」。後句 p087「對。課本說，又平又圓的表面，電荷比較不會跑出去」＝§18.7 "the conductor should be very smooth and have as large a radius of curvature as possible"。15 字，剛好到上限 |
| p088（所長） | 還記得嗎？牆又大又平，只彈回微波，不冒火花。 | 正確 | Bloomfield 759 | "Like a spoon, the walls of the oven are good conductors of electricity and they have no sharp points. While electrons move back and forth in these walls, they simply reflect the microwaves without becoming very hot and without emitting any sparks."「還記得嗎」回呼 p028–p030「整台都是金屬……沒冒」；新加的「又大又平」＝no sharp points 的白話。前句 p087 平圓表面，後句 p089 小問轉到湯匙會不會熱，接得上 |
| p092（小問） | 那細細的鐵絲呢？ | 正確（提問） | — | 前句 p091「教授說，厚湯匙導電好，電跑過去，留下的熱很少」，小孩自然問細的；「細細的鐵絲」就是 p004 的提把 |
| p093（所長） | 還記得嗎？它太細，熱就留在裡面，才可能燒起來。 | 正確（簡化） | Bloomfield 759 | "Since most spoons are pretty thick, the modest currents flowing through them in the microwave will leave little energy inside them and they won't overheat. But a thin twist-tie or small bit of aluminum foil may well overheat and begin to burn."「熱就留在裡面」對照 p091 的「留下的熱很少」（leave little energy inside），「可能燒起來」＝may well … begin to burn，保留了「可能」。「還記得嗎」回呼 p067。twist-tie 套到便當盒提把的推論見 claims C11 與 verify-1 S2，沒有變。後句 p094 轉到鋁箔，接得上 |
| p099（小問） | 那平平的鋁箔就沒事？ | 正確（提問） | — | 前句 p098「皺一次，就多出很多小尖角」，小孩推到平的；問句本身不給答案，答案 p100–p101 沒有說「沒事」 |
| p100（所長） | 平的尖角少，可是一樣很薄，邊也可能尖尖的。 | 正確（支援頁＋撰稿推論） | JennAir；OpenStax §18.7 | JennAir："Thin, crumpled, or sharply edged metal can concentrate energy and spark (arc)."、不安全的情況 "Thin or wrinkled aluminum foil"——「薄」本身就列為風險，所以平的鋁箔不是沒事；「邊也可能尖尖的」＝sharply edged。「尖角少」是接 §18.7 尖端的推論，claims C14 已標。JennAir 另說即使允許時也要 "keep it flat and smooth"、"confirm your model's manual"，跟下一句一致 |
| p101（所長） | 所以平的也要照說明書用，等一下翻給你看。 | 正確 | JennAir；GE 說明書 | JennAir："Confirm your model permits limited foil use in the Use and Care Guide."；GE："Use foil only as directed in this manual."。「等一下翻給你看」在 p129「這本說明書說，只能照它寫的方法用」兌現（約 1 分 35 秒後）；盲評第三輪也把它記為已回收的鉤子。不是目錄句 |
| p104（所長） | 電就越容易跳過去。看這兩個水盤： | 正確 | OpenStax §19.2 | 前句 p103「兩塊金屬中間的縫越窄」；§19.2："it takes about 75 kV to make a spark jump across a 2.5 cm (1 in.) gap, or 150 kV for a 5 cm spark."——縫越寬要越大的電壓，反過來就是越窄越容易跳（verify-1 已核）。新加的「看這兩個水盤」讓 p105 小問的「兩個水盤靠很近」有人先端出來，不再突兀；圖 `tray-gap` 是兩個水盤端對端、中間一條細縫 |
| p115（所長） | 說明書還提醒：架子要放對位置，別碰到牆。 | 正確 | GE 說明書 | Shelf 頁："Make sure the shelf is positioned properly inside the microwave to prevent damage to the oven from arcing."；Arcing："The metal shelf not installed correctly so it touches the microwave wall."。前句 p114「它附的金屬架，是給大盤子、或兩層一起熱用的」，「還」接得上 |
| p116（所長） | 就是剛剛說的：金屬碰到牆，比較容易冒火花。 | 正確 | GE 說明書 | "Metal or foil touching the side of the oven."（列在 Arcing is caused by）。「剛剛說的」回呼 p107「所以金屬碰到牆、或靠得很近，也比較容易冒火花」，是點名回呼。舊句「不然可能冒火花」換成回呼，也把架子規則跟物理原理接起來 |
| p117（所長） | 剛剛那家家電公司也說，金屬別碰到別的金屬。 | 正確 | JennAir | "Do not allow contact with another metal object during cooking."「剛剛那家家電公司」指 p096「一家家電公司說」（JennAir），中間沒有出現別的公司（Amana 到 p121 才以「另一家廠商」登場），指涉清楚。後句 p118 小問「就像兩個水盤別靠太近！」：說明書講的是碰到，小孩用「靠太近」類比，接 p105–p107，可接受 |
| p127（所長） | 因為微波被彈開，飯會熱得不平均。 | 正確 | FDA | "Generally, metal pans or aluminum foil should also not be used in a microwave oven, as the microwaves are reflected off these materials causing the food to cook unevenly and possibly damaging the oven."拿掉「還可能弄壞爐子」：p109 已說「還可能弄壞微波爐」，不算刪掉主張。「飯」是故事裡的食物，＝food。前句 p126「一般不要放金屬鍋子或鋁箔」，後句 p128「那鋁箔一點都不能用？」 |
| p131（所長） | 鋁箔要貼緊食物；翹起來的邊，就像叉子的尖端。 | 正確（說明書＋撰稿類比） | GE 說明書；JennAir | GE Arcing："Foil not molded to food (upturned edges act like antennas)."「貼緊食物」＝molded to food。說明書的比喻是「天線」，片中換成「叉子的尖端」：翹起的邊是伸進空氣的薄尖邊，跟 JennAir "sharply edged metal" 與 p078–p082 的尖端同一個道理，是可接受的撰稿類比，claims C16 已標。p130–p132 都在「這本說明書說」之下，「就像叉子的尖端」聽起來像說明書的話，見選修 S2 |
| p149（小問） | 怎麼處理？ | 正確（提問） | — | 前句 p148「說明書說：先按停止，再把出問題的東西處理好」，問「處理」是什麼，很自然 |
| p150（所長） | 像拿掉鐵絲、把架子放正、把鋁箔貼緊。 | **需改**（見 F01） | GE 說明書 | 三個例子各有出處；缺「請大人來」。後句 p151「那家廠商也說，馬上停下來，通常不會弄壞爐子」＝Amana "If caught at once, arcing should not damage the oven." 不受影響 |
| p156（小問） | 剛剛那些尖尖的、皺皺的， | 正確（小孩的總結） | Bloomfield 759；JennAir；OpenStax §18.7、§19.2 | 後接 p157「還有靠得很近的金屬」、p158「電子擠在一起」、p159「就會跳出火花！」。尖尖的＝叉子尖端（Bloomfield fork、§18.7）；皺皺的＝crumpled（JennAir）；靠得很近＝§19.2 窄縫。「剛剛那些」把總結綁回片中講過的東西，不是新主張。p159 的「就會」verify-1 S5 已提過，沒有改，見選修 S6 |
| p161（所長） | 剛剛那又大又平的金屬牆，正好把微波關在爐子裡。 | 正確（意見，前句標「我覺得」） | Bloomfield 759；FDA | Bloomfield："It is this motion of electrons back and forth through the metal walls of the microwave oven that allow that metal to reflect the microwaves and keep them inside the oven."；FDA "The microwaves are reflected within the metal interior of the oven"。前句 p160「我覺得最妙的是：」，是所長的看法。門上的網子也一起把微波關住（p036、p051），這句只講牆，沒有說「只有牆」，可接受；見選修 S3 |

## 三、刪句與說明欄的檢查

### 刪掉的句子有沒有讓別句失去前提

| 刪掉的內容 | 會受影響的句子 | 結論 |
| --- | --- | --- |
| 舊 p041–p044 開門那一下、兩套連鎖開關、開著門還在運轉 | p038–p040 門壞掉、p041「金屬怎麼會把微波彈回來？」 | 沒問題。p039–p040 自己成立（FDA "Microwave energy will not leak from a microwave in good condition."、"Don't operate a microwave oven if the door does not close firmly or is bent"）。現行 p041 直接接 p040，話題從門回到金屬怎麼反射，靠小問的問句轉場，接得上。沒有別句提到開關 |
| 舊 p064–p070 外層先熱、熱的是食物不是爐子、比較省電 | p063「那這條鐵絲呢？」 | 沒問題。p063–p064「也會被推著晃嗎？」接 p055「就推著裡面的水，一直晃」，中間 p060–p062 是碗，前提都在。verify-1 S3 跟著消失 |
| 舊 p074–p076 塑膠盒會融化、用微波專用容器 | p134–p136 便當盒、p153「倒進這個白碗」 | 沒問題。p135–p136 只講拿掉鐵絲提把（GE "Remove wire twist-ties and metal handles from paper or plastic containers before placing them in the oven."）。p153 把飯倒進白碗是故事動作，沒有說是因為塑膠盒會融化，所以不缺理由；白碗由 p140 的條件涵蓋 |
| 舊 p095–p098 避雷針、高壓電線 | p080、p081–p082、p087 | 沒問題。p080「課本也說，那是像閃電一樣的放電」只講火花像閃電（§18.7 "discharge in the form of lightning sparks"），不需要避雷針。p087 的平滑表面自己引課本。verify-1 F01、S1 跟著消失 |

### 會不會被聽成「金屬放進微波爐沒關係」、會不會鼓勵小孩試

| 項目 | 結論 |
| --- | --- |
| 湯匙（p084–p091） | 只說「通常不會冒火花」「留下的熱很少」，p086 不再說「就好」；p108–p109「我拿叉子試試看！」「不行喔」緊接在火花段之後；p126 FDA「一般不要放金屬鍋子或鋁箔」是全片的通則。沒有一句說可以放湯匙，見選修 S7 |
| 平的鋁箔（p099–p101） | 答案是「一樣很薄、邊也可能尖」「也要照說明書用」，沒有說沒事 |
| 架子（p111–p122） | 都綁在「這台」「這本說明書」，p121–p122 馬上給反例（有些機型的架子微波時不能放） |
| 冒火花後的處理（p148–p150） | 需改，見 F01 |
| 說明欄 | 「請不要把金屬放進微波爐試火花；你家的微波爐怎麼用，請照那一台的說明書。」仍在 |

### YouTube 說明欄、標題、標籤、縮圖、參考資料

| 項目 | 結論 | 依據 |
| --- | --- | --- |
| 標題「微波爐遇到金屬，什麼時候會冒火花？｜原來如此事務所」 | 正確 | 同 verify-1 |
| 說明第 1 段（故事設定） | 正確 | 對應 p001–p012：鐵絲提把、先別按、金屬架、門上的網子、牆、「同樣是金屬」 |
| 說明第 2 段 | 正確，跟現行片子一致 | 水盤與電子（p045–p048）；牆只彈回去、細鐵絲／叉子尖端／皺鋁箔、推力強到空氣擋不住（p065–p098）；靠很近、碰到爐壁（p103–p107、p116）；水晃動摩擦生熱（p054–p058）；網子的洞（p036–p037）；說明書的架子、鋁箔、鐵絲提把與金邊碗「要不要拿開」（p113–p140，verify-1 F04 已照改）；另一家廠商的機型（p121–p122）；FDA 通則（p124–p126）。用 grep 查過，說明欄**沒有任何已刪掉的內容**：避雷、高壓、省電、融化、開關、連鎖、天線、外層都不在 |
| 說明第 3 段（AI 示意插圖、不要試火花） | 正確 | 「微波爐、叉子、鋁箔、碗和火花」都還在片中 |
| 標籤（微波爐、金屬、火花、鋁箔、電子、電荷、說明書、科普、原來如此事務所） | 正確 | 每一個都還在片中講到（電荷 p073–p076、p082、p087） |
| 縮圖「微波爐／冒火花？」「同樣是金屬，差在形狀」 | 正確 | 同 verify-1（S6 可留） |
| 參考資料（`sources` 8 筆） | 正確 | 8 筆片中都還用到：FDA（p017 起多處）、Bloomfield 759（p045、p067、p084–p093）、Bloomfield 1579（p034–p037、p050–p051）、§18.7（p073–p087）、§19.2（p103–p104）、GE（p113–p150）、Amana（p121–p122、p145、p151）、JennAir（p096–p100、p117）。verify-1 為避雷針另找的美國國家氣象局〈Lightning Rods〉〈Lightning Myths〉**沒有**加進 `sources`，現在也不需要了，不用加 |

## 四、claims.md 的同步

`claims.md` 在這一輪之前已由撰稿方改成現行編號（p001–p165）。逐條對過 C01–C21 的「可用說法」與注意欄的每個行號，全部對得上現行台詞。這次改動：

- 文首加一段「現行範圍 p001–p165（165 句）」，註明 verify-2 已逐條對過、未使用的說法照留原文。
- 整條或部分不再用到的標成「現行版未使用」：C09 整條（外層先熱、省電）；C06 的兩套連鎖開關與「開著門還在運轉」；C10 的塑膠盒會融化（補上 FDA 原句留作紀錄）；C12 的避雷針與高壓電線（並註明 NWS 兩頁也不再需要）。
- C18 的可用說法由 p123–p127 改成 p124–p127（p123 是小問的接話）。
- C16 注意欄在 p149–p150 那一段加上本報告 F01 的理由。
- C21 註明 p002 第二版的新說法。
- 原有的來源引文全部保留。

## 建議修改

必改：

- F01 p150（所長）：像拿掉鐵絲、把架子放正、把鋁箔貼緊。 → 請大人來：拿掉鐵絲、架子放正、鋁箔貼緊。（20 字）
  （三個例子不變，前後句 p149「怎麼處理？」、p151「那家廠商也說，馬上停下來，通常不會弄壞爐子。」都接得上；圖 `oven-fixed` 不用改。）

選修（不影響本輪結論）：

- S1 東西燒起來的情況：片中說細鐵絲「可能熱到燒起來」（p067、p093），但只教了冒火花怎麼辦。GE 說明書另寫 "If materials inside the oven should ignite, keep the oven door closed, turn the oven off … If the door is opened, the fire may spread."。要補的話可以在 p150 後面加一句所長的話，例如「要是燒起來了，門別打開，先按停止，叫大人。」（21 字）。會多一句、行號要重排，所以只列為選修。
- S2 p131 的類比歸屬：p129「這本說明書說」之下的 p131「就像叉子的尖端」聽起來像說明書的原話，其實說明書寫的是「像天線」。若想分清楚，可改「鋁箔要貼緊食物；翹起來的邊，我看就像叉子的尖端。」（24 字）。不改也不算錯，類比本身成立。
- S3 p161 只講牆：把微波關在爐子裡的，還有門上的金屬網（p036、p051）。可留，因為它標成「我覺得最妙的是」，而且沒說「只有牆」。若想包進網子：「剛剛那又大又平的金屬牆和網子，正好把微波關在裡面。」（25 字，剛好到上限）。
- S4 p116–p117 連兩句都以「剛剛」開頭（「就是剛剛說的」「剛剛那家家電公司」），聽起來重複。可把 p117 改成「那家家電公司也說，金屬別碰到別的金屬。」（19 字）；p096 之後到 p117 之間沒有別的公司，指涉仍清楚。
- S5 `loops`：p101「等一下翻給你看」是明確的前向鉤子（在 p129 兌現），但 `video.json` 的 `loops` 沒有它；其餘 25 組 setup／payoff 的行號都對得上現行台詞。建議在 `build_scenes.py` 補一組（p101→p129，「平的鋁箔要怎麼照說明書用」）。不在本次可改的範圍。
- S6 verify-1 S5 仍然開著：p159「就會跳出火花！」，來源都是 may／can。小孩的總結可以肯定一點；要一致可改「就可能跳出火花！」（8 字）。
- S7 圖與湯匙：圖 `food-uneven`（p127）畫的是一碗滷肉飯一半蓋著金屬鍋蓋，沒有畫微波爐，所以不是在示範金屬放進爐子，可留；若重畫，鍋蓋放在旁邊比較不會讓人誤會。另外 p091 之後沒有一句明說湯匙也不要放；p108–p109 與 p126 已經涵蓋，可留。`brief.md` 第 43、52、63、70、86、98 列還寫著避雷針、高壓電線、塑膠盒等已刪掉的段落，不在本次範圍，提醒一下，免得下一個代理照 brief 把它們加回來。
