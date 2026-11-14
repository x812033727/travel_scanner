# 查核報告 1（sothatswhy-p01-wireless-energy）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-12
- 方法：逐句讀 `video.json` 的 175 句台詞（p001–p175），加上 YouTube 標題、說明、標籤與縮圖文字（headline「卡片不燙／鍋子卻熱？」、sub「電怎麼隔空跑過去」）。`claims.md` 的 C01–C29 只當線索，不採用它的引文；每個來源當天重新打開（curl GET，HTML 去掉 script／style 與標籤轉純文字後 grep 並讀上下文；PDF 用 `pdftotext -layout`）：
  - [1] OpenStax《College Physics 2e》23.4〈Eddy Currents and Magnetic Damping〉（200，374,219 bytes），讀全文：金屬板進出磁場、"no eddy current if the field is uniform"、絕緣體 "extremely small"、回收場 "works for all metals"、最後一段電磁爐。
  - [2] OpenStax 23.2〈Faraday's Law of Induction: Lenz's Law〉（200，391,492 bytes），讀 Faraday's and Lenz's Law 兩段。
  - [3] OpenStax 20.2〈Ohm's Law: Resistance and Simple Circuits〉（200，376,439 bytes），讀電阻定義段。
  - [4] HyperPhysics〈Faraday's Law〉（http 200，5,344 bytes）與〈Electric Power〉（http 200，5,911 bytes），只當交叉核對（沒有可用的 https，`video.json` 未列，跟 claims.md 一致）。
  - [5] NFC Forum〈NFC Technology〉（200，47,823 bytes），讀 Technical Overview、Designed for Flexibility、Designed for Contactless、Operating Modes。
  - [6] NXP MIFARE Classic EV1 1K 規格書 MF1S50YYX_V1 Rev. 3.2（PDF，200，472,343 bytes），讀 §1、§2 Features、§8.1 Block description、§11 Load Modulation Strength Option、Limiting values。
  - [7] NXP MIFARE DESFire EV3 short data sheet Rev. 3.1（PDF，200，435,243 bytes），讀 §2.1.1、交易計時器段、§7.2。
  - [8] Wireless Power Consortium〈Principle of Inductive Power〉（200，65,284）、〈Coupling Factor〉（200，68,247）、〈How Qi Works〉（200，66,010），讀正文。
  - [9] TI BQ51013B 規格書 SLUSB62D（PDF，200，5,005,156 bytes），讀 §1 Features、§2 Applications、§3 Description、§8.3.15 同步整流、§8.3.16 Foreign Object Detection。
  - [10] TI 應用報告 SLOA192B（PDF，200，949,118 bytes），讀 §1 與 target 模式的 load modulate 段。
  - [11] Apple 支援 108377（200，163,085 bytes），讀全文。
  - [12] DOE〈Making the Switch to Induction Stoves or Cooktops〉（200，124,386 bytes），讀全文。
  - [13] ENERGY STAR〈Electric Cooking Products〉（200，53,127 bytes），讀 Consider the benefits of induction、Additional product features、維護段。
  - [14] Iowa State University Extension AnswerLine 標籤頁（200，89,461 bytes），讀 Geiger〈Induction Cooking – What You Need to Know〉與 Steed〈Portable Induction Burners〉全文。頁面另顯示更新日（2025-12-02、2026-05-04），`<time class="published">` 仍是 2022-06-07 與 2019-09-30，跟 `video.json` 的標題一致。
  - [15] UC Cooperative Extension〈Safety Note #14〉（PDF，200，116,492 bytes），讀全文含 NOTE。
  - **另找的一手來源**（C08 負載調變與「卡片收到的電很少」需要）：
    - [16] Microchip〈microID 13.56 MHz RFID System Design Guide〉DS21299E（https://ww1.microchip.com/downloads/en/DeviceDoc/21299E.pdf，PDF，200，2,903,872 bytes），讀 AN680 的 Definitions 與 Backscatter Modulation 段，以及被動標籤的功率段。
    - [17] Microchip AN710〈Antenna Circuit Design for RFID Applications〉（https://ww1.microchip.com/downloads/en/AppNotes/00710c.pdf，PDF，200，1,040,450 bytes），讀 Introduction。
- 打不開／沒讀到原文的：本集引用的 16 個來源都打得開（全部 200）。另試 ST 的天線設計應用說明（AN2972），連線中斷（curl 92），沒用。ISO/IEC 14443 要付費，跟撰稿一樣沒讀；所以閘門實際用的晶片與讀卡距離仍查不到，片中也沒有說。
- 結論統計（台詞 175 句）：**正確 173、需改 2、錯誤 0**。另外標題、說明、標籤、縮圖 4 項：正確 4。另有 6 處選修建議（不影響結論，見文末）。
- 需改的 2 句都是**小孩會記錯方向**的地方，不是數字錯：p125（F01）把「卡片為什麼不燙」答成能量的去向，會讓小孩記成「拿去做事的電就不會變熱」，跟 p085（手機的線圈和整流器會變熱）和物理都相反，真正的差別是卡片收到的電非常少；p157（F02）說「金屬待在磁場裡，也會繞起電流」，字面上是不變的磁場也行，正好是 p047–p048 要教的反面。
- 撰稿要我特別看的幾點，結論如下（細節在第二節）：
  - 負載調變「一下多拿一點、一下少拿一點」（p052–p053）：**正確（簡化）**。另找的 Microchip 原文 "The incoming RF carrier signal to the tag is loaded and unloaded"，就是「多拿、少拿」。
  - 「離開磁場就沒電可用」（p056）：**正確**。被動卡沒有電池，DESFire 規格書要特別防範攻擊者 "keeping the card powered after it left the legitimate reader device"。
  - 「剩下的，多半變成熱，散到廚房裡」（p122）：**正確（推論）**，物理上其餘能量最後幾乎都成了熱，「多半」只會更保守。
  - 十公分（p142–p143）：**正確**，片中說「一款做車票用的卡片晶片」，沒有說成「這類感應卡」，也照規格書加了限制。p035 的「這類感應卡」只用在 13.56 MHz，那是 NFC Forum 也寫的基礎頻率，說得通。
  - 鍋子材質（p110–p116）、爐面受熱（p104–p106）：**正確**，有原文。
  - 卡片會不會熱：片中沒有說「卡片完全不熱」，p124 是小孩的問題；但 p125 的答法要改（F01）。
  - 水盆比喻：方向對（手一停、水一靜、水車就停，p046–p048），全片沒有「穩定的磁場能推出電」的說法，只有 p157 的字面例外（F02）。
  - 安全：p079–p082 卡片不放充電板、p160–p161 硬幣鋁箔卡片都不放、p117–p118 磁鐵要等鍋子冷了拿下爐子、p106 剛放過鍋子的地方別摸；說明欄也寫。沒有任何一句建議把卡片、硬幣或金屬放上充電板或爐子。
- 字數：下表建議句含標點計算，小問 ≤15、所長 ≤25；建議句不含拉丁字母。現行 175 句沒有超過上限的。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 | 建議改法 |
| --- | --- | --- | --- | --- | --- |
| F01 | p125（所長） | 卡片的電，被細線送進晶片，拿去回答閘門。 | 需改（說法本身沒錯，但當作 p124「為什麼卡片不會燙？」的答案，會讓小孩記成「拿去做事的電不會變熱」） | 電的能量用掉以後會轉成熱等形式：HyperPhysics〈Electric Power〉"the rate at which energy is converted from the electrical energy of the moving charges to some other form, e.g., heat"；片中 p085 自己也說「線圈和整流器在整理電的時候，有一點會變成熱」。卡片不燙的主因是收到的電非常少：Microchip DS21299E "Because the passive tag is remotely powered by the reader's RF signal, it deals with very small power (~ µw)"；NXP MF1S50 的上限 "total power dissipation per package … 120 mW"。片中 p049 已經說「卡片收到這一點電」，把「一點點」帶進答案就跟 p126（電磁爐專門把能量灌進鍋底）形成「很少 vs 很多、拿去回答 vs 變成熱」的對比，也不用說出沒有來源的數字 | 卡片只收到一點點電，送進晶片拿去回答閘門。（21 字；p126 照留） |
| F02 | p157（所長） | 可能會。金屬待在磁場裡，也會繞起電流。 | 需改（「待在磁場裡」聽起來是不變的磁場也會推出電流，跟 p047–p048 相反；小孩家裡冰箱磁鐵吸著鐵片，會以為那也在繞電流） | OpenStax 23.4 "When the metal plate is completely inside the field, there is no eddy current if the field is uniform, since the flux remains constant in this region."；HyperPhysics "Any change in the magnetic environment of a coil of wire will cause a voltage (emf) to be "induced""。硬幣會熱的依據照舊：OpenStax "eddy currents … occur only in conductors"、"This works for all metals, not just ferromagnetic ones"；TI BQ51013B §8.3.16 "to limit the temperature rise of Foreign Objects"。改成「一直變的磁場」，跟 p032、p062、p088、p165 用同一個詞 | 可能會。金屬在一直變的磁場裡，也會繞起電流。（22 字） |

## 二、逐段核對（正確的句子與依據）

### 一路沒插線，鍋子先滾了（p001–p021）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p002 | 搭捷運來；卡片在閘門上一貼就嗶一聲 | 正確 | — | 故事設定 |
| p003–p008 | 麵快煮好；手機放充電板，沒插線也在充；鍋子也滾了 | 正確 | [8] Principle | 故事設定。"An alternating current in the transmitter coil generates a magnetic field which induces a voltage in the receiver coil. This voltage can be used to power a mobile device or charge a battery." |
| p009 | 碰了一下鍋子旁邊的玻璃，不燙 | 正確（見選修 S1） | [14] | "Only the pan, and what's directly under it, on an induction range gets hot. The surface around it stays cool." 限制在 p105–p106 補上 |
| p010 | 你先別碰，等一下告訴你為什麼 | 正確 | [14] | 安全叮嚀；"one can never assume that it will be cool to the touch" |
| p011–p013 | 三樣都沒插線，電怎麼跑過去；只有鍋子變熱 | 正確 | — | 問句 |
| p014 | 三樣東西都是隔空收到能量 | 正確 | [8]；[1] | [8] 上引；[1] "The magnetic field is varied rapidly producing eddy currents in the base of the pot, causing the pot and its contents to increase in temperature." |
| p015–p016 | 能量是讓燈亮、東西動、變熱的那份本事 | 正確（簡化） | [4] Electric Power | 給八歲小孩的白話，不是定義；方向跟 "converted … to some other form, e.g., heat, mechanical energy" 一致 |
| p017 | 收到以後做的事完全不一樣 | 正確 | [8]；[1] | power a device / charge a battery / pot increases in temperature |
| p018–p020 | 預告：手機挪一點、玻璃鍋、卡片要多近 | 正確 | — | 預告，回收在 p129–p137、p107–p109、p141–p143 |
| p021 | 小問猜：電是飛過去的 | 正確（錯猜） | — | p022、p048 推翻 |

### 卡片貼上閘門那一下（p022–p059）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p022 | 不是像球那樣飛過去 | 正確 | [2]；[4] | 感應是變化的磁通在線圈裡產生電動勢，沒有電荷飛過去 |
| p023–p024 | 卡片裡有電池嗎；小問猜一定有 | 正確（錯猜） | — | p025 推翻 |
| p025 | 一家做感應卡晶片的廠商說，它不需要電池 | 正確 | [7] §7.2 | "connected to a coil consisting of a few turns embedded in a standard ISO/IEC smart card. A battery is not needed." |
| p026 | 卡片裡藏著一圈一圈的細線，接著一顆小晶片 | 正確 | [6] §8.1 | "Energy and data are transferred via an antenna consisting of a coil with a small number of turns which is directly connected to the MF1S50yyX/V1." |
| p027–p028 | 晶片是會記東西、照規則回話的電子零件 | 正確（白話） | [6] §8.1 | "consists of a 1 kB EEPROM, RF interface and Digital Control Unit" |
| p029–p030 | 電從閘門來；閘門讀卡處也有一圈線 | 正確 | [5]；[7] | [5] "one side can also transmit power over the connection allowing for battery-less operating modes"；[7] "positioned in the proximity of the PCD antenna"。另見 [17] "Since the energizing and communication between the reader and tag is accomplished through antenna coils" |
| p031–p032 | 線裡的電一下往這邊、一下往那邊；旁邊就有一直在變的磁場 | 正確 | [8] Principle | "An alternating current in the transmitter coil generates a magnetic field" |
| p033–p034 | 磁場是磁鐵旁邊看不見、能吸住鐵的範圍 | 正確（簡化） | — | 給小孩的畫面；p031–p032 已說明這裡的磁場是線圈的電造出來的 |
| p035 | 這類感應卡用的磁場，一秒來回變一千三百多萬次 | 正確 | [6]；[5] | [6] "Operating frequency of 13.56 MHz"；[5] "base frequency of 13.56 MHz"。13.56 MHz＝每秒 1,356 萬個週期，一個週期即一次來回 |
| p036–p037 | 好快；跟卡片有什麼關係 | 正確 | — | 反應與問句 |
| p038–p039 | 一直在變的磁場穿過卡片細線，推著線裡的電跑起來 | 正確 | [2]；[4] | [2] "the emf induced by a change in magnetic flux"；[4] "Any change in the magnetic environment of a coil of wire will cause a voltage (emf) to be "induced" in the coil." |
| p040–p045 | 洗手台的水盆與小水車：手晃、水晃、水車轉；手＝閘門線圈，晃的水＝變的磁場，水車＝卡片細線 | 正確（比喻） | — | 比喻；限度見 claims.md C24 與選修 S5。方向對：轉動來自「晃」，不是來自水本身 |
| p046–p048 | 手不晃、水靜，水車停；磁場要一直變才推得動電 | 正確 | [1]；[2] | [1] "there is no eddy current if the field is uniform, since the flux remains constant"；[2] emf ∝ ΔΦ。p048 也回收 p021 |
| p049 | 卡片收到這一點電，晶片就醒過來 | 正確 | [6] §8.1；[16] | [6] RF interface 含 "Rectifier"、"Power-On Reset (POR)"，"After Power-On Reset (POR) the card answers to a request"；[16] 被動標籤 "very small power (~ µw)"，支持「這一點」 |
| p050 | 跟閘門交換資料，閘門才嗶一聲讓你過 | 正確 | [6] | "Contactless transmission of data and energy supply"；嗶一聲是故事情境 |
| p051 | 卡片沒電池怎麼回話 | 正確 | — | 問句 |
| p052–p053 | 不用自己發訊號，讓閘門的磁場被它一下多拿一點、一下少拿一點 | 正確（簡化） | [10]；[16]；[6] §11 | [10] "the target … load modulates the initiator's RF field in passive mode"、"the target load modulates the initiator RF field instead of modulating its own field"；[16] "This terminology refers to the communication method used by a passive RFID tag to send data to the reader using the reader's own carrier signal. The incoming RF carrier signal to the tag is loaded and unloaded"；"loaded and unloaded" 就是多拿、少拿，簡化不教錯 |
| p054 | 閘門感覺到這些變化，就讀懂卡片的回答 | 正確 | [16] | "By monitoring the changes in the reader antenna voltage (due to the tag's modulation data), the data in the tag can be reconstructed."；"as the secondary winding (tag coil) is momentarily shunted, the primary winding (reader coil) experiences a momentary voltage change" |
| p055–p056 | 卡片沒有電池，離開那個磁場就沒電可用 | 正確（推論，依規格書） | [7]；[17] | [7] "A battery is not needed"；交易計時器防的是攻擊者 "keeping the card powered after it left the legitimate reader device"，表示正常情況離開就斷電；[17] 被動標籤 "has no external power source such as a battery" |
| p057 | 它不存電，收到的電當下就用掉 | 正確（簡化） | [7]；[17] | [17] "This induced AC voltage is rectified to provide a voltage source for the device"。晶片裡的記憶資料不靠電保存，見選修 S2 |
| p058–p059 | 手機呢，也是收到就用掉嗎 | 正確 | — | 問句 |

### 把媽媽的手機放上充電板（p060–p086）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p060 | 不只用掉，手機還會把電存起來 | 正確 | [8] How Qi Works | "This voltage can be used to power a mobile device or charge a battery." |
| p061 | 充電板裡有一圈線，手機背面也有一圈 | 正確 | [8] How Qi Works | "You need two coils, a transmitter coil and a receiver coil." |
| p062–p064 | 充電板的磁場也一直在變，推著手機那圈線的電；跟小水車一樣 | 正確 | [8] | "An alternating current in the transmitter coil generates a magnetic field which induces a voltage in the receiver coil." |
| p065 | 推出來的電一下往這邊、一下往那邊 | 正確 | [9] | "The BQ51013B devices provide the receiver (RX) AC-to-DC power conversion" |
| p066–p067 | 那樣不能充電嗎；電池要往同一邊走的電 | 正確（常識） | [9] | 電池用直流充電；[9] 方塊圖 "AC to DC … Rectification" |
| p068–p069 | 手機裡有整流器，把來回跑的電整理成往同一邊 | 正確 | [9] | "Full synchronous rectifier"；§8.3.15 "integrated, self-driven synchronous rectifier that enables high-efficiency AC to DC"；[9] Applications "Cell phones and smart phones" |
| p070–p071 | 剛剛那家廠商說，卡片的晶片裡也有整流器 | 正確 | [6] §8.1 | RF interface "– Rectifier"；[6] 與 [7] 同為 NXP，對應 p025 |
| p072–p074 | 卡片收到電馬上拿去回答；手機送進電池存起來晚點用 | 正確 | [7]；[8] | C02、C07、C09、C10 的整理 |
| p075–p076 | 卡片的水車敲鈴；手機的水車接幫浦把水打進瓶子存著 | 正確（比喻） | — | 比喻，不教錯 |
| p077–p078 | 瓶子滿了；手機會傳話給充電板，電池滿了可以停了 | 正確 | [8] How Qi Works | "the phone must be able to shut down the transmitter when the battery is full. The phone, therefore, needs to send control signals to the charging station." |
| p079–p081 | 小問想把卡片放上去充；做手機的公司寫中間別夾東西，晶片可能會壞 | 正確 | [11] | "Don't place anything between your iPhone and the charger. … might reduce performance or damage magnetic strips or RFID chips like those found in some credit cards, security badges, passports, and key fobs." 用「可能」 |
| p082 | 卡片沒有電池，本來就不用充電 | 正確 | [7] | 回呼 p025 |
| p083–p084 | 手機會變熱嗎；會一點點，說明寫可能稍微變暖 | 正確 | [11] | "Your iPhone might get slightly warmer while it charges." |
| p085 | 線圈和整流器整理電時，有一點會變成熱 | 正確 | [9] §8.3.16；[4] | "the power loss in the Secondary Coil and series resonant capacitor, the power loss in the Shielding of the Power Receiver, the power loss in the rectifier"；損失轉成熱，[4] "e.g., heat" |
| p086 | 那鍋子為什麼那麼燙 | 正確 | — | 問句 |

### 麵煮滾了，旁邊的玻璃不燙（p087–p128）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p087 | 鍋子自己就是接收的那一端 | 正確 | [14] Steed；[12] | "The cookware is considered the transformer"；"The heat is created from within the cookware itself" |
| p088 | 電磁爐的玻璃底下也有一圈線，磁場一直在變 | 正確 | [1]；[12] | "Induction cooktops have electromagnets under their surface. The magnetic field is varied rapidly"；DOE "ceramic-glass surfaces" |
| p089–p091 | 鍋子沒有細線；磁場直接穿進鍋底的金屬，推出一圈一圈繞著跑的電流 | 正確 | [1] | "producing eddy currents in the base of the pot"；"If motional emf can cause a current loop in the conductor, we refer to that current as an eddy current"（同頁定義段） |
| p092–p093 | 在金屬裡打轉的電流叫渦電流；渦是漩渦的渦 | 正確 | [1] | 中文名詞字面說明 |
| p094–p095 | 電流要送去哪；哪裡都不去，在鍋底一直繞 | 正確 | [1] | current loop in the conductor |
| p096–p097 | 電流在金屬裡一直撞到小粒子，能量變成熱 | 正確（簡化） | [3] | "Collisions of moving charges with atoms and molecules in a substance transfer energy to the substance and limit current."（鐵鍋另有磁滯發熱，片中不講，不教錯） |
| p098–p099 | 像搓手會熱；有點像；熱從鍋子自己身上冒出來 | 正確 | [3]；[12] | "(crudely similar to friction and air resistance)"；"The heat is created from within the cookware itself" |
| p100 | 鍋子熱了再把熱傳給湯和麵 | 正確 | [1]；[14] | "causing the pot and its contents to increase in temperature"；"heat the cookware directly" |
| p101–p103 | 旁邊的玻璃怎麼不燙；磁場也穿過玻璃，可是玻璃不導電，幾乎推不出電流 | 正確 | [1] | "When an insulating material is used, the eddy current is extremely small"；玻璃是絕緣體（常識） |
| p104 | 美國大學給家庭的說明寫，鍋子周圍會保持涼 | 正確 | [14] | "The surface around it stays cool." |
| p105 | 鍋子正下方的玻璃會被熱鍋燙熱 | 正確 | [14]；[12] | "Only the pan, and what's directly under it … gets hot"；"Heat is transferred from the cooking vessel to the glass through conduction"；DOE "the glass top is only as warms as it gets when you place afrom a hot object on top of it"（原文錯字照錄） |
| p106 | 剛放過鍋子的地方千萬別摸 | 正確 | [14] | "one can never assume that it will be cool to the touch" |
| p107–p109 | 換玻璃鍋，水熱不起來；跟剛剛那塊玻璃一樣 | 正確 | [14]；[15] | "Aluminum, glass and ceramic will not work."；UC "Cookware that does not work with induction stoves include: aluminum, glass, and copper."、"If you turn on the stove but the cookware is incompatible, the stove will indicate the error and won't heat up." |
| p110 | 鍋子要是金屬，電流才繞得起來 | 正確 | [1] | "eddy currents and magnetic damping occur only in conductors" |
| p111–p112 | 金屬鍋都可以嗎；也不是，教科書說鍋底要是鐵或鋼這類材料 | 正確 | [1] | "the base of the pot needs to be ferromagnetic, iron or steel for induction to work" |
| p113 | 那份說明也寫，鋁鍋、銅鍋都不行 | 正確（見選修 S3） | [14]；[15] | "Pots and pans made from aluminum and copper aren't compatible."；UC 同上 |
| p114–p115 | 怎麼分辨；冰箱磁鐵碰鍋底，吸得住通常就能用 | 正確 | [13]；[14]；[12] | ENERGY STAR "check if your cookware is compatible with a refrigerator magnet. If the magnet sticks to the cookware, it will work with induction."；ISU "see if a magnet strongly sticks to the bottom of the pan"；DOE 另要求 "flat bottom"，片中用「通常」保留 |
| p116 | 好幾種金屬做的鍋子，看包裝標示 | 正確 | [14]；[13] | "some cookware uses a combination of materials in its construction, so its induction status isn't always obvious. Look for pots and pans marked "induction safe" or "induction compatible.""；ENERGY STAR "will have an induction logo on the box" |
| p117–p118 | 回家拿磁鐵試；要等鍋子冷了、拿下爐子再試 | 正確（安全叮嚀） | [15]；[14] | 撰稿加的叮嚀，方向跟 UC "Do not put metallic objects … on the cooktop when it's on, as they can become hot and cause burns" 一致 |
| p119–p121 | 能量都跑進鍋子了嗎；能源之星說約八成五送到鍋裡的食物，瓦斯爐只有三分之一 | 正確 | [13] | "about 85% of heating energy is transferred to what is in the cookware compared to only a third of the heating energy when using gas cooking products. [1]"（註 "Source Frontier Energy, July 2019"） |
| p122 | 剩下的多半變成熱，散到廚房裡 | 正確（推論） | [13]；[4] | 原文 "More of the heating energy is transferred to cooking and less heat is released into the kitchen"。其餘能量（鍋身、爐面、電子零件的損耗）最後幾乎都成為熱，「多半」偏保守，不教錯 |
| p123–p124 | 卡片的細線也有電在跑，為什麼卡片不會燙 | 正確 | — | 小孩的問題；「不會燙」是生活經驗，片中沒有說卡片完全不熱 |
| p125 | 卡片的電被細線送進晶片，拿去回答閘門 | 需改（F01） | [4]；[16] | 見第一節 |
| p126 | 電磁爐專門把能量灌進鍋底，讓它變成熱 | 正確 | [13]；[12] | "use electromagnetic energy to heat up ferromagnetic cookware internally"；"induction appliances only create heat through pots and pans on their surfaces" |
| p127–p128 | 手機剛剛震了一下，好像沒在充了 | 正確 | [11] | 故事情境，p130–p131 用原文解釋 |

### 手機往旁邊挪一點點（p129–p162）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p129–p131 | 震的時候滑開一點；說明寫震動可能讓手機移位，充電板可能停止供電 | 正確 | [11] | "If your iPhone vibrates—when it gets a notification, for example—your iPhone might shift position. This can cause the charging mat to stop providing power to your iPhone." |
| p132–p134 | 才一點點；水車挪到角落，轉得好慢 | 正確（比喻） | [8] Coupling Factor | 比喻錯位讓接收變少 |
| p135–p136 | 兩圈線對得越正，穿過的磁場越多；一歪掉能接到的就少 | 正確 | [8] Coupling Factor | "The more flux reaches the receiver, the better the coils are coupled."；"If coils are axially aligned, a displacement causes a decrease of k." |
| p137 | 說明要你最好把手機放在充電板正中間 | 正確 | [11] | "For best performance, place it in the center of the charger or in the location recommended by manufacturer." |
| p138–p139 | 離遠一點也一樣，越遠穿過的磁場越少 | 正確 | [8] Coupling Factor；Principle | "Depending on the distance between the transmit and receive coils, only a fraction of the magnetic flux generated by the transmitter coil penetrates the receiver coil"；"The coupling is determined by the distance between the inductors" |
| p140–p141 | 所以卡片要貼著閘門；還記得卡片要多近嗎 | 正確 | [5]；[16] | 同一原理套到卡片；[5] NFC "typical range of up to 2cm"；[16] 被動標籤 "the read range … is typically limited within a proximity distance" |
| p142–p143 | 一款做車票用的卡片晶片，規格寫最遠大約十公分，還要看卡片的線圈和閘門那一邊 | 正確 | [6]；[7] | [6] "Operating distance up to 100 mm depending on antenna geometry and reader configuration"、"Typical ticketing transaction time of < 100 ms"；[7] "operating distance up to 100 mm (depending on power provided by the PCD and antenna geometry)"。說「一款」不說「這類」，限制也照原文（見選修 S4） |
| p144–p145 | 鍋子也要放正中間；美國大學說明寫放中間才會好好加熱 | 正確 | [14]；[15] | "placing the right sized cookware in the center of the heating element in order for it to be properly activated"；UC "Arrange cookware to be centered over the stove to ensure all the food is being cooked." |
| p146 | 很多電磁爐偵測不到鍋子就會自己停 | 正確 | [12] | "most will automatically shut off if a pot or pan isn't detected" |
| p147–p148 | 鍋子拿起來；能源部說一拿開加熱就停 | 正確 | [12] | "as soon as you remove it from a burner, the heating stops" |
| p149 | 還記得卡片離開閘門嗎，一樣是收不到了 | 正確 | [7]；[12] | 回呼 p056 |
| p150–p152 | 手機太熱；電池太熱時可能先不充過八成，溫度降下來才繼續 | 正確 | [11] | "if the battery gets too warm, software might limit charging above 80 percent. Your iPhone will charge again when the temperature drops." 片中說「手機的說明」，沿用前面那份 |
| p153–p154 | 鍋子不就一直在熱；鍋子本來就要熱，手機的熱只是順便多出來的 | 正確 | [12]；[9] | 鍋子的熱是目的；手機的熱是 §8.3.16 列的損耗 |
| p155–p156 | 硬幣放上充電板，也會像鍋子一樣熱嗎 | 正確 | — | 問句 |
| p157 | 可能會；金屬待在磁場裡也會繞起電流 | 需改（F02） | [1]；[9] | 見第一節 |
| p158–p159 | 無線充電的規格要手機回報收到多少電，讓充電板發現中間是不是多了一塊會變熱的金屬 | 正確 | [9] | §8.3.16 "In order to enable a Power Transmitter to monitor the power loss across the interface as one of the possible methods to limit the temperature rise of Foreign Objects, the BQ51013B reports its Received Power to the Power Transmitter."；§3 "to allow the TX to determine if a foreign object is present within the magnetic interface" |
| p160–p161 | 小問要拿硬幣試；不行，硬幣、鋁箔、卡片都別放上充電板或爐子 | 正確（安全） | [15]；[11] | UC "Do not put magnetically charged items such as credit cards on or near the stove."、"Do not let sugar, plastic, or aluminum foil on or near the stove when it's on."、"Do not put metallic objects, such as spoons, on the cooktop when it's on"；Apple 見 p080 |
| p162 | 好啦，那電怎麼隔空過去 | 正確 | — | 問句，交給小問自己回答 |

### 麵吃完，小問想通了（p163–p175）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p163 | 你都看過了，你說呢 | 正確 | — | 引導 |
| p164–p166 | 原來如此；是一直在變的磁場，推著線圈和鍋底的電跑 | 正確 | [2]；[1] | 重述 p038–p039、p090–p091；「一直在變」保留了方向 |
| p167–p169 | 卡片拿去回答、手機存起來、鍋子把它變成熱 | 正確（簡化） | [7]；[8]；[1] | 三種用途的重述；卡片收到的量很少，若照 F01 改，p167 不必動 |
| p170–p171 | 最妙的是：同一種推法，收到的東西不同，就做了不同的事 | 正確（看法） | — | 標成所長的看法 |
| p172 | 明天刷卡要貼正一點 | 正確 | [8] Coupling Factor | 對正、靠近的推論 |
| p173–p175 | 留言題；訂閱 | 正確 | — | 片尾 |

### 標題、說明、標籤、縮圖

| 項目 | 主張 | 結論 | 依據摘要 |
| --- | --- | --- | --- |
| 標題「卡片不燙、鍋子卻熱：電怎麼隔空過去？｜原來如此事務所」 | 生活經驗＋問句 | 正確 | 「卡片不燙」是經驗描述，不是「卡片完全不熱」；問句由片中 p165–p166 回答（磁場推著接收端自己的電） |
| 說明 | 故事、水盆比喻、三樣東西的去向、對正與靠近、AI 示意插圖聲明、安全提醒、資料日期 | 正確 | 各句都對得到第二節的行；「不要把卡片、硬幣、鋁箔或其他金屬放在充電板或電磁爐上試；剛放過鍋子的爐面會燙」與 [11]、[14]、[15] 一致 |
| 標籤 | 無線充電、電磁爐、感應卡、交通卡、磁場、電磁感應、渦電流、科普、原來如此事務所 | 正確 | 都是片中內容，不點名產品 |
| 縮圖「卡片不燙／鍋子卻熱？」「電怎麼隔空跑過去」 | 同標題 | 正確 | 同上 |

## 選修建議（不影響結論）

- **S1（p009）**：大人在開著的電磁爐上摸鍋子旁邊的玻璃，台詞有 p010、p106 補救，內容也對（[14] "The surface around it stays cool"）。但畫面若真的畫出手貼在冒煙的鍋子旁，小孩可能模仿。建議 p009 的畫面不要畫手按在玻璃上，或只畫所長的手停在旁邊。
- **S2（p056–p057）**：「沒電可用」「不存電」可能讓小孩以為卡片一離開閘門就忘了裡面的資料。晶片的記憶不靠電保存（[6] "Data retention time of 10 years"、[7] "Data retention of 25 years"）。若想補，可把 p057 改成「它不存電，可是記住的東西不會忘。」（16 字），但會少掉「收到就用掉」，p073 已經有這層意思。
- **S3（p113）**：前一句 p112 講的是「教科書」，這句的「那份說明」指的是 p104 的美國大學說明，小孩不一定接得上。可改「美國大學那份說明也寫，鋁鍋、銅鍋都不行。」（20 字）。
- **S4（p140–p143）**：小問說「卡片要貼著閘門」，所長回「對」，接著又說最遠十公分，聽起來有點打架。p143 的限制已經夠，不必改；若要更順，可讓 p143 的畫面標示「閘門通常要更近」，但台灣閘門實際距離沒有公開來源，台詞不要寫數字。
- **S5（水盆比喻，C24）**：方向沒問題：轉動來自「晃」，手停、水靜、水車停（p046–p048），全片沒有說穩定的磁場能推出電（p157 的字面例外已列 F02）。提醒做畫面的人：(1) 水盆要畫成一陣陣的波，不要畫成一條往同一邊流的水流，否則小孩會記成「一直流就能轉」，等於「不變的磁場也行」；(2) 真的玩具水車在來回晃的水裡多半是來回擺，片中說「轉」可以接受，但動畫若做成持續單向旋轉，最好跟手的晃動同步、手停就停。
- **S6（p096–p097）**：鐵鍋發熱除了渦電流撞擊，也有磁滯的部分；片中不講不算錯，給翻譯或日後延伸參考。
