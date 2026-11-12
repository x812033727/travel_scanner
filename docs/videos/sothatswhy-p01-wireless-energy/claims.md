# 主張與來源（sothatswhy-p01-wireless-energy）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說（行號）、來源原文與注意事項，並標出它是
**官方說明**、**教材**、**廠商規格**、**推廣教育**、**撰稿推論**、**常識**，還是**比喻／示意**。撰稿只用「可用說法」裡的數字與說法；逐行查核等另一個代理寫 `verify-1.md`。

**行號**以現行 `video.json` 為準（p001–p165，verify-1 修正與四輪盲評改寫後的版本；verify-1 查的第一版是 p001–p175）；`script.md` 是它的可讀版。2026-11-12 由 `verify-2.md` 的查核代理把各列行號換成現行編號，引文不動。第一版的 C21（能源之星的效率比較）與 C27（電池太熱先不充過八成）兩段在現行版整段刪掉，標成「現行版未使用」；C15、C28、C29 也有部分句子刪掉或改寫，在該列註明。

## 先看這裡：找不到來源、因此沒講或小心講的事

- **鍋底材質「為什麼」要鐵或鋼**（鐵磁性、磁滯、集膚效應）：OpenStax 只寫「the base of the pot needs to be ferromagnetic, iron or steel」，沒有寫原因；能讀到的其他頁也沒有給小孩聽得懂的原因。**片中只說「教科書說，鍋底要是鐵或鋼這類材料」（p111），不解釋為什麼鋁鍋、銅鍋不行**；小問也沒有問「為什麼鋁不行」，免得答不出來。
- **複合鍋底**：只找到 Iowa State 推廣教育一句「some cookware uses a combination of materials in its construction, so its induction status isn't always obvious. Look for pots and pans marked "induction safe"…」。片中只照這句說（p115），**不說哪種複合結構可以、哪種不行**，也不說不鏽鋼一定行或不行（UC 寫的是「stainless steel containing some iron」）。
- **爐面受熱**：有來源（Iowa State「Heat is transferred from the cooking vessel to the glass through conduction」「one can never assume that it will be cool to the touch」；DOE「the glass top is only as warm as … a hot object on top of it」）。片中說「鍋子周圍會保持涼」之後，立刻補「鍋子正下方的玻璃，會被熱鍋燙熱」「剛放過鍋子的地方，千萬別摸」（p103–p105）。
- **台灣交通卡用哪一種晶片、哪一個標準、閘門的實際距離**：官方沒公開（舊查核 `topic-checks/s3-A64-A75.md` A68 也這樣寫）。ISO/IEC 14443 要付費，沒有讀。片中**不點名卡片品牌或晶片**，只說「一家做感應卡晶片的廠商」「一款做車票用的卡片晶片」，數字只引 NXP 規格書，並照規格書加上「還要看卡片的線圈，和閘門那一邊」（p137–p138）。p034 的 13.56 MHz 也說成「這類感應卡用的磁場」，不說「悠遊卡」或「這個閘門」。
- **卡片收到多少電、卡片會不會發熱**：沒有找到數字或說法。片中不說「卡片完全不熱」，也不比較卡片和電磁爐的功率大小；現行版 p120 照 verify-1 F01 改成「因為卡片收到的電，只有一點點」，依據是 verify-1 另找的 Microchip DS21299E「very small power (~ µw)」（見 C16 注意；它不在 `video.json` 的 `sources` 裡，見 verify-2.md），仍不給數字，p121 再對比電磁爐把能量灌進鍋底。片名「卡片不燙」是小孩的生活經驗。
- **無線充電的效率、速度、瓦數排行**：企劃要求刪掉；片中一個瓦數都不說，也不說無線一定比較慢。
- **晶片怎麼「回話」**：TI 應用說明寫被動模式的一方「load modulates the initiator's RF field」，NXP 規格書有「Load Modulation Strength」的設定；這兩份都沒有用小孩的話解釋。片中的「一下多拿一點、一下少拿一點」（p051–p052）是**撰稿的簡化**，見 C08。
- **電磁爐的頻率**：沒有找到官方或教材的數字，片中不說。無線充電的頻率也不說。

## 當天重讀的來源（2026-11-12，curl GET；HTML 去標籤轉純文字後逐段讀；PDF 用 `pdftotext -layout`）

- [1] OpenStax《College Physics 2e》23.4〈Eddy Currents and Magnetic Damping〉：200（374,219 bytes），讀全文含最後一段電磁爐。
- [2] OpenStax《College Physics 2e》23.2〈Faraday's Law of Induction: Lenz's Law〉：200（391,492 bytes），讀「Faraday's and Lenz's Law」兩段與 Applications 段。
- [3] OpenStax《College Physics 2e》20.2〈Ohm's Law: Resistance and Simple Circuits〉：200，讀電阻定義段。
- [4] HyperPhysics（R. Nave，Georgia State University）〈Faraday's Law〉與〈Electric Power〉：http 200（5,344 bytes 等）。網站沒有可用的 https（憑證不符），所以 `video.json` 的 `sources` 不列它（lint 要 https），只在這裡當交叉核對。
- [5] NFC Forum〈NFC Technology〉Technical Overview：200（47,823 bytes），讀 Technical Overview、Designed for Contactless、Operating Modes。
- [6] NXP〈MIFARE Classic EV1 1K〉產品規格書 MF1S50YYX_V1 Rev. 3.2（2018-05-23）：200（472,343 bytes），讀 §1.1–1.2、§2 Features、§8.1 Block description、§11 Load Modulation Strength Option。用一般 User-Agent 會 404，用 curl 預設可讀。
- [7] NXP〈MIFARE DESFire EV3〉product short data sheet MF3D(H)x3 Rev. 3.1（2024-01-11）：200（435,243 bytes），讀 §2.1.1、§7.2、交易計時器段。
- [8] Wireless Power Consortium〈Principle of Inductive Power〉、〈Coupling Factor〉、〈How Qi Works〉：皆 200（65,284／68,247／66,010 bytes），讀正文。〈Foreign Object Detection〉舊網址 404，改用 [9]。
- [9] Texas Instruments〈BQ51013B〉無線充電接收端規格書 SLUSB62D（2013-03，2020-09 修訂）：200（5,005,156 bytes），讀 §1 Features、§3 Description、§8.3.15、§8.3.16。
- [10] Texas Instruments 應用報告 SLOA192B〈NFC active and passive peer-to-peer communication using the TRF7970A〉（2014-04，2019-03 修訂）：200（949,118 bytes），讀 §1。
- [11] Apple 支援〈How to wirelessly charge your iPhone〉108377（Published 2024-04-24）：200（163,085 bytes），讀全文。
- [12] 美國能源部 DOE〈Making the Switch to Induction Stoves or Cooktops〉（2023-05-11）：200（124,386 bytes），讀全文。
- [13] ENERGY STAR〈Electric Cooking Products〉：200（53,127 bytes），讀 Consider the benefits of induction、Additional product features、Tips 段。
- [14] Iowa State University Extension AnswerLine 標籤頁〈Induction cooking〉：200（89,461 bytes），內含 Marlene Geiger〈Induction Cooking – What You Need to Know〉（2022-06-07）與 Marcia Steed〈Portable Induction Burners〉（2019-09-30）兩篇全文。
- [15] UC Cooperative Extension〈Safety Note #14: Induction Stove Safety〉（UCCE Solano County，PDF）：200（116,492 bytes），讀全文。
- 舊素材（A68 的 `topic-checks/s3-A64-A75.md`、A45 的 `season2/A45.md` 與 `topic-checks/s2-A39-A50.md`、S78 的 `refresh-20261101/new-topics.json`）只當線索；上面每一筆都是今天重開。A45 舊查核用過的 Qi2 新聞稿、iFixit 實測、Apple 120619 屬於速度與效率排行，企劃要刪，這次沒有重讀、片中沒用。

---

## C01 三樣東西都隔空收到能量；能量的白話【常識＋教材】

- **可用說法**：p011–p016（第一版 p017「可是收到以後，它們做的事完全不一樣」在現行版刪掉）
- **來源**：[8] Principle、[1]
- **原文**：[8]「An alternating current in the transmitter coil generates a magnetic field which induces a voltage in the receiver coil. This voltage can be used to power a mobile device or charge a battery.」[1]「The magnetic field is varied rapidly producing eddy currents in the base of the pot, causing the pot and its contents to increase in temperature.」
- **注意**：p016「讓燈會亮、東西會動、會變熱的那份本事」是給八歲小孩的**簡化**，不是物理定義。p001–p010 的捷運、手機、煮麵是故事設定。p003 現行版改成「我用電磁爐煮麵，快好了」，一開場就點明是電磁爐。p009 現行版是「我把手靠近鍋子旁邊的爐面玻璃，一點都不熱」（第一版是「碰了一下……不燙」，改成只靠近不碰），由 C18 支持，並在 p104–p105 補上限制。

## C02 感應卡晶片不需要電池；卡片裡是幾圈細線接一顆晶片【廠商規格】

- **可用說法**：p021–p025（p023 小問的錯猜由這裡推翻）
- **來源**：[7]、[6]
- **原文**：[7] §7.2「the MIFARE DESFire EV3 is connected to a coil consisting of a few turns embedded in a standard ISO/IEC smart card. A battery is not needed.」[6] §8.1「Energy and data are transferred via an antenna consisting of a coil with a small number of turns which is directly connected to the MF1S50yyX/V1.」
- **注意**：片中說「一家做感應卡晶片的廠商」，不說台灣的交通卡用這家的晶片（官方未公開）。p027「會記東西、會照規則回話的電子零件」是晶片的白話（[6] 有 1 kB EEPROM 與數位控制單元）。

## C03 卡片的電從閘門來；閘門讀卡處也有一圈線，線裡的電來回跑【廠商規格＋業界組織】

- **可用說法**：p028–p030
- **來源**：[5]、[7]、[8] Principle
- **原文**：[5]「In addition to data connections, NFC is unique in that one side can also transmit power over the connection allowing for battery-less operating modes.」「NFC must start, … power up the remote device, and then transmit…」[7]「When the card is positioned in the proximity of the PCD antenna…」（PCD＝讀卡機）[8]「An alternating current in the transmitter coil generates a magnetic field」
- **注意**：「來回跑」＝交流電（alternating current）。WPC 這句講的是無線充電的發射線圈；讀卡機天線同樣靠交變的場，[6] 的工作頻率 13.56 MHz 即為證（C05）。NFC Forum 說的是 NFC，它也寫 NFC 裝置能跟「ISO/IEC 14443 Type A/B compliant Readers and Cards」溝通；片中不說閘門用哪個標準。

## C04 磁場的白話【常識／簡化】

- **可用說法**：p031–p033
- **注意**：「磁鐵旁邊那圈看不見、能吸住鐵的範圍」是**簡化**：閘門和電磁爐的磁場是線圈的電流造出來的，不是磁鐵；片中先用磁鐵讓小孩有畫面，p030–p031 已經說明是線圈裡來回跑的電造出來的。

## C05 這類感應卡用的磁場，一秒鐘來回變一千三百多萬次【廠商規格＋業界組織】

- **可用說法**：p034
- **來源**：[6]、[5]
- **原文**：[6]「Operating frequency of 13.56 MHz」[5]「operating over a radio using a base frequency of 13.56 MHz」
- **注意**：13.56 MHz＝每秒 1,356 萬個週期，片中說「一千三百多萬次」。限定「這類感應卡」，不說台灣某一張卡或某一座閘門。

## C06 一直在變的磁場穿過線圈，就推著線裡的電跑起來；磁場不變就推不動【教材】

- **可用說法**：p035–p038、p045–p047、p061–p062
- **來源**：[2]、[1]、[4]
- **原文**：[2]「the emf induced by a change in magnetic flux depends on only a few factors. First, emf is directly proportional to the change in flux ΔΦ. Second, emf is greatest when the change in time Δt is smallest」[1]「When the metal plate is completely inside the field, there is no eddy current if the field is uniform, since the flux remains constant in this region.」[4] Faraday's Law「Any change in the magnetic environment of a coil of wire will cause a voltage (emf) to be "induced" in the coil.」
- **注意**：p047「要一直變，才推得動電」對應「沒有變化就沒有感應電動勢／渦電流」。片中用「推著電跑」代替「感應電動勢」。p047 同時回收 p020「電是飛過去的」：電荷沒有從閘門飛到卡片，是變化的磁場在卡片的線圈裡推動電（能量經由磁場傳過去）。

## C07 晶片醒過來，跟閘門交換資料【廠商規格】

- **可用說法**：p048–p049
- **來源**：[6]
- **原文**：「Contactless transmission of data and energy supply」；Figure 1 標示 CARD 與 PCD 之間 energy 與 data 雙向。§8.1 RF interface 含「Power-On Reset (POR)」「Voltage regulator」。
- **注意**：「醒過來」＝上電啟動（power-on reset）的白話。「閘門才嗶一聲讓你過」是故事情境，片中不講交通卡的扣款或安全機制。

## C08 卡片不用自己發訊號，而是讓閘門的磁場被它一下多拿、一下少拿；閘門感覺到變化就讀懂【應用說明＋廠商規格＋撰稿簡化】

- **可用說法**：p050–p053
- **來源**：[10]、[6]
- **原文**：[10]「The initiator always generates the RF field for both active and passive communication modes. However, the target generates its own RF field only for active mode (while the initiator's RF field is disabled) and load modulates the initiator's RF field in passive mode.」[6] §11「Load Modulation Strength Option」（卡片可以設定 load modulation 的強弱）。
- **注意**：[10] 講的是 NFC 點對點的被動模式，原理同卡片回應讀卡機（被動的一方不自己產生場，只做負載調變）。「一下多拿一點、一下少拿一點」是**撰稿對負載調變的簡化**，請查核代理特別看；若認為不妥，可改成「它輕輕改變閘門的磁場，閘門就讀得到」。

## C09 卡片離開磁場就沒電可用；不存電，收到就用【撰稿推論，依廠商規格】

- **可用說法**：p054–p056、p144（「還記得卡片離開閘門嗎？一樣是收不到了」）
- **來源**：[7]、[5]
- **原文**：[7]「A battery is not needed.」以及交易計時器段「prevent a Man-in-the-Middle (MitM) attack where the attacker delays the conclusion of a transaction by keeping the card powered after it left the legitimate reader device」[5]「battery-less operating modes」
- **注意**：沒有一句原文直接寫「離開就沒電」；[7] 說攻擊者要另外「keeping the card powered after it left the legitimate reader」，表示正常情況下卡片離開讀卡機就不再有電。屬**推論**。

## C10 手機和充電板各有一圈線；收到的電可以讓手機用，也可以存進電池【業界組織】

- **可用說法**：p057–p062
- **來源**：[8] How Qi Works、Principle
- **原文**：「You need two coils, a transmitter coil and a receiver coil. An alternating current in the transmitter coil generates a magnetic field which induces a voltage in the receiver coil. This voltage can be used to power a mobile device or charge a battery.」
- **注意**：p059「不只用掉，手機還會把電存起來」＝ power a device or charge a battery。片中說「無線充電」「充電板」，不念標準名稱。

## C11 推出來的電一下往這邊、一下往那邊；電池要往同一邊的電；手機裡的整流器整理成同一邊；卡片晶片裡也有整流器【廠商規格＋常識】

- **可用說法**：p064–p070
- **來源**：[9]、[6]、[8]
- **原文**：[9]「The BQ51013B devices provide the receiver (RX) AC-to-DC power conversion and regulation」「Full synchronous rectifier」；方塊圖「AC to DC … Rectification」。[6] §8.1 RF interface「Rectifier」。[8]「An alternating current in the transmitter coil…induces a voltage in the receiver coil」
- **注意**：p066「電池要的，是一直往同一邊走的電」是**常識**（電池用直流充電），[9] 的 AC-to-DC 轉換是它的直接證據。[9] 是一款手機無線充電接收晶片（Applications：Cell phones and smart phones），片中不點名，只說「手機裡有一個零件，叫做整流器」。p070「剛剛那家廠商說」指 NXP（[6] 與 [7] 同一家），對應 p024「一家做感應卡晶片的廠商」。

## C12 卡片收到就用、手機收到再存（小水車敲鈴 vs 幫浦打水進瓶子）【撰稿整理＋比喻】

- **可用說法**：p071–p075
- **來源**：C02、C07、C09、C10 的組合
- **注意**：鈴鐺與瓶子是比喻（C24）。

## C13 電池滿了，手機會傳話給充電板，可以停了【業界組織】

- **可用說法**：p076–p077
- **來源**：[8] How Qi Works
- **原文**：「For energy-efficient power transfer the phone must be able to shut down the transmitter when the battery is full. The phone, therefore, needs to send control signals to the charging station.」

## C14 卡片別夾在手機和充電板中間，晶片可能會壞【官方說明】

- **可用說法**：p078–p081（小問想把卡片放上去充電，所長說不行）
- **來源**：[11]
- **原文**：「Don't place anything between your iPhone and the charger. Magnetic mounts, magnetic cases, or other objects between your iPhone and the charger might reduce performance or damage magnetic strips or RFID chips like those found in some credit cards, security badges, passports, and key fobs.」
- **注意**：Apple 舉的是信用卡、門禁卡、護照、遙控鑰匙裡的 RFID 晶片；交通卡也是靠感應的晶片卡，片中說「可能會壞掉」，不說一定壞。「做手機的公司」＝ Apple，不念品牌名。p081「卡片沒有電池，本來就不用充電」回呼 C02，用「還記得嗎？」開頭。

## C15 充電時手機可能稍微變暖；線圈和整流器整理電時有一點變成熱【官方說明＋廠商規格】

- **可用說法**：p082–p084（第一版 p154「手機的熱，只是順便多出來的」在現行版刪掉）
- **來源**：[11]、[9]
- **原文**：[11]「Your iPhone might get slightly warmer while it charges.」[9] §8.3.16「The Received Power equals the power that is available from the output of the Power Receiver plus any power that is lost in producing that output power (the power loss in the Secondary Coil and series resonant capacitor, the power loss in the Shielding of the Power Receiver, the power loss in the rectifier).」
- **注意**：「損失的功率變成熱」是常識（[4] Electric Power：能量轉成「heat, mechanical energy…」）。

## C16 鍋子自己就是接收的一端；爐面下有線圈、磁場一直變；鍋底的金屬裡推出一圈一圈的電流（渦電流）；熱從鍋子自己冒出來，再傳給湯和麵【教材＋官方說明】

- **可用說法**：p085–p092、p098–p099、p120–p121
- **來源**：[1]、[12]、[14]
- **原文**：[1]「Induction cooktops have electromagnets under their surface. The magnetic field is varied rapidly producing eddy currents in the base of the pot, causing the pot and its contents to increase in temperature.」[1]「If motional emf can cause a current loop in the conductor, we refer to that current as an eddy current.」[12]「Induction cooking uses an electromagnetic field that transfers currents directly to the cookware placed on the glass surface. The heat is created from within the cookware itself」[14]（Portable Induction Burners）「The cookware is considered the transformer」
- **注意**：「也有一圈線」＝ electromagnets（線圈）。「渦電流，渦就是漩渦的渦」是中文名詞的字面說明。p094「哪裡都不去，就在鍋底一直繞」＝ 渦電流在導體內自成迴路（[1] 的 current loop in the conductor）。p121「電磁爐卻是專門把能量灌進鍋底，讓它變成熱」依 [13]「Induction cooktops and ranges use electromagnetic energy to heat up ferromagnetic cookware internally」與 [12]「induction appliances only create heat through pots and pans on their surfaces」。p120「因為卡片收到的電，只有一點點」是 verify-1 F01 的改法，依 Microchip〈microID 13.56 MHz RFID System Design Guide〉DS21299E（2004，https://ww1.microchip.com/downloads/en/DeviceDoc/21299E.pdf）「Because the passive tag is remotely powered by the reader's RF signal, it deals with very small power (~ µw).」；這份不在 `video.json` 的 `sources` 裡，verify-2.md N03 建議補上。

## C17 電流在金屬裡跑會撞到裡面的小粒子，能量變成熱；像搓手【教材】

- **可用說法**：p095–p098
- **來源**：[3]、[4]
- **原文**：[3]「The electric property that impedes current (crudely similar to friction and air resistance) is called resistance R. Collisions of moving charges with atoms and molecules in a substance transfer energy to the substance and limit current.」[4] Electric Power「the rate at which energy is converted from the electrical energy of the moving charges to some other form, e.g., heat」
- **注意**：「小粒子」＝原子與分子。p097 小問的「像我搓手會熱一樣」由 [3] 的「crudely similar to friction」支持，所長回「有點像」，不說一模一樣。

## C18 磁場也穿過玻璃，但玻璃不導電，幾乎推不出電流；鍋子周圍保持涼，正下方會被熱鍋燙熱；剛放過鍋子的地方別摸【教材＋推廣教育＋官方說明】

- **可用說法**：p100–p105（回收 p010 的「等一下告訴你為什麼」）
- **來源**：[1]、[14]、[12]、[13]
- **原文**：[1]「When an insulating material is used, the eddy current is extremely small」[14]「Only the pan, and what's directly under it, on an induction range gets hot. The surface around it stays cool.」「Caution – Cooktops can get hot. Heat is transferred from the cooking vessel to the glass through conduction, much as a hot pan would transfer heat to a countertop if you set it down to rest. The glass surface never gets as hot as it would on a traditional radiant electric range but one can never assume that it will be cool to the touch.」[12]「the glass top is only as warms as it gets when you place afrom a hot object on top of it」（原文錯字照錄）[13]「the cooking top surface will not be hot to the touch without a pot or pan in place」
- **注意**：「玻璃不導電」是常識（玻璃是絕緣體）。「美國大學給家庭的說明」＝ Iowa State University Extension 的 AnswerLine。p009 所長只把手靠近「鍋子旁邊」的爐面玻璃、沒有碰（現行版），p010 叫小孩先別碰，p105 再叮嚀剛放過鍋子的地方別摸。

## C19 玻璃鍋放上電磁爐，水熱不起來【推廣教育＋教材】

- **可用說法**：p106–p108（回收 p018「這口麵煮完，我再拿一口玻璃鍋上來」）
- **來源**：[14]、[15]、[1]
- **原文**：[14]「Aluminum, glass and ceramic will not work.」[15]「Cookware that does not work with induction stoves include: aluminum, glass, and copper.」[1] 絕緣體渦電流極小（見 C18）。
- **注意**：所長示範的是一口裝水的玻璃鍋（不是金屬、不是鋁箔），沒有安全疑慮；片中不說爐子會顯示什麼。p108 小問「跟剛剛那塊玻璃一樣！」用「剛剛那」回呼 p102。

## C20 鍋子要是金屬；不是每口金屬鍋都行：鍋底要鐵或鋼這類材料，鋁鍋、銅鍋不行；磁鐵吸得住通常能用；複合材料看包裝標示【教材＋推廣教育＋官方說明】

- **可用說法**：p109–p117
- **來源**：[1]、[14]、[15]、[13]、[12]
- **原文**：[1]「the base of the pot needs to be ferromagnetic, iron or steel for induction to work」[14]「Require cookware containing ferrous iron. Specifically, that means stainless steel, cast iron, and carbon steel. Pots and pans made from aluminum and copper aren't compatible. Most confusing of all, some cookware uses a combination of materials in its construction, so its induction status isn't always obvious. Look for pots and pans marked "induction safe" or "induction compatible." An easy test to see if cookware is compatible is to see if a magnet strongly sticks to the bottom of the pan.」[13]「you can check if your cookware is compatible with a refrigerator magnet. If the magnet sticks to the cookware, it will work with induction.」[12]「Any pots or pans with a flat bottom that a magnet sticks to will work with an induction cooktop.」
- **注意**：S78 舊企劃的限制是「磁鐵測試不能取代型號與尺寸規格」：片中加「通常」並補包裝標示（p114–p115），不說「一定」。平底的條件（[12]、[14]）片中沒說，屬刪減。p117 磁鐵測試要等鍋子冷了、拿下爐子再做（安全叮嚀，撰稿加的）；[15] 寫「Do not put magnetically charged items such as credit cards on or near the stove」，所以片中不讓磁鐵或卡片靠近開著的爐子。

## C21 電磁爐送出的能量約八成五到鍋裡的食物，瓦斯爐約三分之一；其餘多半變熱散進廚房【官方說明＋撰稿推論】（現行版未使用）

- **現行版未使用**：第一版 p119–p122（「能量都跑進鍋子了嗎？」「美國能源之星的網站說，大約八成五……用瓦斯爐，只有三分之一」「剩下的，多半變成熱，散到廚房裡」）在盲評後整段刪掉，現行版沒有任何一句用到這條。ENERGY STAR [13] 仍是 C16（p121）、C18 與 C20（p114「冰箱上的磁鐵」、p115 包裝標示）的來源，`sources` 要留著。
- **第一版的可用說法**：p119–p122
- **來源**：[13]
- **原文**：「When using induction, about 85% of heating energy is transferred to what is in the cookware compared to only a third of the heating energy when using gas cooking products.[1]」（註：Source Frontier Energy, July 2019）「More of the heating energy is transferred to cooking and less heat is released into the kitchen」
- **注意**：數字是 ENERGY STAR 引 Frontier Energy 2019 的測試，第一版片中說「美國能源之星的網站說，大約八成五」。第一版 p122「剩下的，多半變成熱，散到廚房裡」是**推論**（原文只寫比較少熱散進廚房），用「多半」標示。

## C22 手機震動可能移位，充電板就可能停止供電；最好放在正中間【官方說明】

- **可用說法**：p122–p126、p132
- **來源**：[11]
- **原文**：「If your iPhone vibrates—when it gets a notification, for example—your iPhone might shift position. This can cause the charging mat to stop providing power to your iPhone.」「For best performance, place it in the center of the charger or in the location recommended by manufacturer.」
- **注意**：p122–p123 小問發現手機震了一下、沒在充，是故事情境；p125–p126 照原文保留「可能」。

## C23 兩圈線對得越正、離得越近，穿過的磁場越多；歪了、遠了就少【業界組織】

- **可用說法**：p128–p135（回收 p017「手機要是往旁邊挪一點點，還充得到嗎？我們等等試」）
- **來源**：[8] Coupling Factor、Principle
- **原文**：Coupling Factor「Depending on the distance between the transmit and receive coils, only a fraction of the magnetic flux generated by the transmitter coil penetrates the receiver coil and contributes to the power transmission. The more flux reaches the receiver, the better the coils are coupled.」「The coupling factor is determined by the distance between the inductors and their relative size. It is further determined by the shape of the coils and the angle between them. If coils are axially aligned, a displacement causes a decrease of k.」
- **注意**：片中不說耦合係數、不說衰減的倍數或「平方反比」。p135 小問「所以卡片要貼著閘門！」是把同一原理套到卡片的推論，由 C25 的規格書數字支持。

## C24 比喻：晃水盆與小水車（比喻的限度）【比喻／示意】

- **可用說法**：p039–p047、p063、p074–p075、p128–p129
- **對應**：所長的手＝發送端的線圈（閘門、充電板、電磁爐）；晃動的水＝一直在變的磁場；小水車＝接收的線圈；手停、水靜、水車停＝磁場不變就推不出電（C06）；水車挪到角落、離得很遠就轉得慢＝錯位與距離讓耦合變小（C23）；卡片的水車敲鈴＝收到就用；手機的水車接幫浦打水進瓶子＝收到再存。
- **限度**（片中不講，寫在這裡給查核與翻譯）：
  1. 磁場不是水，沒有東西從閘門「流」到卡片；水波會傳很遠，近場感應隨距離減弱得比水波快得多。比喻只說明「要一直變」「越近越正越好」。
  2. 小水車是靠水推動葉片；線圈是被變化的磁場在導線裡推出電動勢，沒有轉動的零件。
  3. 鍋子那一段不用水車比喻（鍋子沒有小水車），改用「電流在鍋底打轉、撞來撞去變熱」（C16、C17）；水晃動產生的熱可以忽略，不能拿來說明鍋子為什麼熱。
  4. 示範只用一盆水和玩具水車，不用電；所長在洗手台示範，沒有叫小朋友去做任何有電的實驗。

## C25 一款做車票用的卡片晶片，規格寫最遠大約十公分，還要看卡片的線圈和讀卡機【廠商規格】

- **可用說法**：p136–p138（回收 p019「你那張卡片，離閘門多遠就不嗶了？」與 p020 小問的錯猜「要貼著才嗶」；p135–p136 的接法見 verify-2.md N02）
- **來源**：[6]、[7]
- **原文**：[6]「Operating distance up to 100 mm depending on antenna geometry and reader configuration」「Typical ticketing transaction time of < 100 ms」[7]「Low Hmin enabling operating distance up to 100 mm (depending on power provided by the PCD and antenna geometry)」
- **注意**：「做車票用」依 [6] 的 ticketing 字樣。NFC Forum [5] 另寫 NFC「typical range of up to 2cm」「The Certified Compliant range of NFC Forum connections is 5mm」，那是 NFC 規格的典型與認證距離，跟晶片規格書的「最遠」不是同一件事，片中只用規格書一個數字，不混講。

## C26 鍋子要放在爐子中間才會好好加熱；很多電磁爐偵測不到鍋子會自己停；鍋子一拿開加熱就停【推廣教育＋官方說明】

- **可用說法**：p139–p144
- **來源**：[14]、[15]、[12]、[13]
- **原文**：[14]「placing the right sized cookware in the center of the heating element in order for it to be properly activated」「the heating element may cut off prematurely or shut off without warning when the pan is shaken or moved」[15]「Arrange cookware to be centered over the stove to ensure all the food is being cooked.」[12]「most will automatically shut off if a pot or pan isn't detected」「as soon as you remove it from a burner, the heating stops」[13]「cookware sensors that generate heat based on the size and location of the cookware」
- **注意**：p141「很多」對應 DOE 的「most」。p144 用「還記得」回呼卡片（C09）。

## C27 電池太熱時，可能先不充過八成；溫度降下來才繼續【官方說明】（現行版未使用）

- **現行版未使用**：第一版 p150–p154（「那手機太熱會怎樣？」「電池太熱時，可能先不充過八成」「等溫度降下來，才會繼續充」與 C15 的「手機的熱，只是順便多出來的」）在盲評後刪掉，現行版沒有任何一句用到這條。Apple [11] 仍是 C14、C15、C22 的來源。
- **第一版的可用說法**：p150–p152
- **來源**：[11]
- **原文**：「To extend the lifespan of your battery, if the battery gets too warm, software might limit charging above 80 percent. Your iPhone will charge again when the temperature drops.」
- **注意**：這是 Apple 對 iPhone 的說明；片中說「手機的說明寫」，沿用前面「做手機的公司」的那份說明，不推到所有手機。

## C28 硬幣放上充電板可能會熱；規格要手機回報收到多少電，讓充電板發現多出來的金屬；硬幣、鋁箔、卡片都別放上充電板或爐子【教材＋廠商規格＋推廣教育＋官方說明】

- **可用說法**：p145–p151
- **來源**：[1]、[9]、[15]、[11]
- **原文**：[1]「Since eddy currents and magnetic damping occur only in conductors」（金屬在變化的磁場中會有渦電流，見 C16）[9]「In order to enable a Power Transmitter to monitor the power loss across the interface as one of the possible methods to limit the temperature rise of Foreign Objects, the BQ51013B reports its Received Power to the Power Transmitter.」「In the WPC1.2 specification, foreign object detection (FOD) is enforced.」[15]「Do not let sugar, plastic, or aluminum foil on or near the stove when it's on.」[11] 見 C14。
- **注意**：「可能會」照 [9] 的「limit the temperature rise of Foreign Objects」（金屬異物會升溫，所以要偵測）。「無線充電的規格」＝ WPC 1.2，不念名稱。p150 小問想試，p151 所長明說不行（現行版是「不行喔。金屬會變燙，硬幣、鋁箔都別放上去。」，「放上去」指充電板；第一版的「卡片」與「或爐子」拿掉了，卡片不放充電板由 C14 的 p078–p081 講，說明欄仍寫卡片、硬幣、鋁箔與其他金屬都別放在充電板或電磁爐上）。p147 照 verify-1 F02 改成「金屬在一直變的磁場裡」。片中**沒有**任何建議把金屬、卡片或鋁箔放上充電板或電磁爐的說法。

## C29 收尾、看法與留言題【撰稿／示意】

- p152–p159：小問用自己的話說答案（p155–p156 一直在變的磁場推著線圈和鍋底的電；現行版 p157–p159 改成「卡片、手機、鍋子，接收的東西不一樣，做的事就不一樣！」，第一版的「卡片拿去回答、手機存起來、鍋子變成熱」刪掉；p158 的說法見 verify-2.md N01），回收 p012、p013。
- p160–p161：現行版是「同一種推法，能讓卡片說話，也能把麵煮滾」，標成所長的看法（「我覺得最妙的是」）；「卡片說話」回呼 p050–p053 的回話。
- p162–p165：片尾三張；留言題「你家還有什麼東西，不插線也能收到能量？」不點名產品。
- 所有插圖（閘門、卡片透視、手機、充電板、電磁爐、鍋子、水盆）是 AI 生成的示意，不是實際產品或結構圖；說明欄寫明。

## 來源

1. OpenStax, *College Physics 2e*, 23.4 Eddy Currents and Magnetic Damping, https://openstax.org/books/college-physics-2e/pages/23-4-eddy-currents-and-magnetic-damping
2. OpenStax, *College Physics 2e*, 23.2 Faraday's Law of Induction: Lenz's Law, https://openstax.org/books/college-physics-2e/pages/23-2-faradays-law-of-induction-lenzs-law
3. OpenStax, *College Physics 2e*, 20.2 Ohm's Law: Resistance and Simple Circuits, https://openstax.org/books/college-physics-2e/pages/20-2-ohms-law-resistance-and-simple-circuits
4. R. Nave, HyperPhysics, Faraday's Law（http://hyperphysics.phy-astr.gsu.edu/hbase/electric/farlaw.html）與 Electric Power（http://hyperphysics.phy-astr.gsu.edu/hbase/electric/elepow.html）；只有 http，交叉核對用，`video.json` 未列
5. NFC Forum, NFC Technology – Technical Overview, https://nfc-forum.org/learn/nfc-technology/
6. NXP, MF1S50YYX_V1 MIFARE Classic EV1 1K product data sheet, Rev. 3.2, 2018-05-23, https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf
7. NXP, MF3D(H)x3 MIFARE DESFire EV3 product short data sheet, Rev. 3.1, 2024-01-11, https://www.nxp.com/docs/en/data-sheet/MF3D_H_X3_SDS.pdf
8. Wireless Power Consortium, Principle of Inductive Power／Coupling Factor／How Qi Works, https://www.wirelesspowerconsortium.com/knowledge-base/magnetic-induction/principle-of-inductive-power/ 、…/coupling-factor/ 、…/how-qi-works/
9. Texas Instruments, BQ51013B data sheet SLUSB62D (rev. 2020-09), https://www.ti.com/lit/ds/symlink/bq51013b.pdf
10. Texas Instruments, SLOA192B NFC active and passive peer-to-peer communication using the TRF7970A (rev. 2019-03), https://www.ti.com/lit/an/sloa192/sloa192.pdf （見 C08）
11. Apple Support, How to wirelessly charge your iPhone (108377, 2024-04-24), https://support.apple.com/en-us/108377
12. U.S. Department of Energy, Making the Switch to Induction Stoves or Cooktops (2023-05-11), https://www.energy.gov/articles/making-switch-induction-stoves-or-cooktops
13. ENERGY STAR, Electric Cooking Products, https://www.energystar.gov/products/electric_cooking_products
14. Iowa State University Extension and Outreach, AnswerLine: Induction Cooking – What You Need to Know (M. Geiger, 2022-06-07); Portable Induction Burners (M. Steed, 2019-09-30), https://blogs.extension.iastate.edu/answerline/tag/induction-cooking
15. UC Cooperative Extension (Solano County), Safety Note #14: Induction Stove Safety, https://www.ccfruitandnuts.ucanr.edu/sites/default/files/2017-09/270568.pdf
