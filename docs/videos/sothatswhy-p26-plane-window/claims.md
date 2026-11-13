# 主張與來源（sothatswhy-p26-plane-window）

對應 [`brief.md`](brief.md) 的「查核清單」。每一條列出片中怎麼說（行號）、來源原文與注意事項，並標出它是
**主管機關手冊**、**主管機關事故教材**、**法規**、**大學教材**、**研究論文**、**專業人士文章**、**撰稿推論**、**常識／示範**，還是**比喻／示意**。
撰稿只用「可用說法」裡的數字與說法；逐行查核等另一個代理寫 `verify-1.md`。

**行號**以現行 `video.json` 為準（p001–p176，第一版，2026-11-13）；`script.md` 是它的可讀版。

## 先看這裡：找不到來源、因此沒講或小心講的事

- **素材審視點名的兩個缺口都補了**：(1) 客艙加壓與壓差——美國聯邦航空總署（FAA）《Pilot's Handbook of Aeronautical Knowledge》第 7 章〈Pressurized Aircraft〉（[1]），含壓力換算表與壓差定義；(2) 彗星號以外的現代設計與檢查——FAA 事故教材的 fail-safe／damage tolerance 段落（[2]）、美國聯邦法規 14 CFR 25.571（[13]，設計、製造瑕疵與檢查），以及 Slate 專欄（作者是航空公司機長）引窗戶製造商 GKN Aerospace 技術總監的三層窗說明（[14]）。
- **「方角比圓角集中幾倍」沒有數字**：只有「被拉的大薄板上開圓洞，洞邊約是遠處的三倍」（[3]，Kirsch 解）有來源；方角、尖角只說「大得多」「越尖越厲害」（[2]、[4]），不給倍數，也不畫應力色圖（企劃的畫面規則）。
- **紙條拉一拉（p080–p081）沒有實測**：是撰稿的桌上示範，照 [4]、[9]「缺口／裂縫尖端應力集中、玻璃棒從缺口斷」寫成「方洞那條從角裂開」。插圖是示意。若站主要證據，開拍前實際拉一次並記錄；結果不同就改這兩句。
- **迴紋針（p087–p088）是常識示範**，而且所長在 p095 說明它和機身不一樣：機身每次被撐，不會像迴紋針那樣被扳彎（[6]：疲勞發生在低於降伏強度的反覆應力）。
- **彗星號只短引**，全部照 FAA 事故教材（[2]）與 Withey（[11]、[12]）：不講罹難人數，不畫事故、殘骸或人；兩架出事（p110）只講一句。只有厄爾巴島那架（G-ALYP）有確定結論，片中說「這一架的結論是」（p119）；拿坡里那架調查沒有下確定意見，片中不說它同因。
- **不說「只是窗角」**：p124 小問的錯猜由 p125–p132 推翻：Withey 1997 說所有觀察到的裂縫都從開口附近的螺栓或鉚釘孔長出、「可能不是開口形狀，而是窗戶與加強板的固定方法」，片中標成「那位學者認為……可能」。FAA 自己也寫方窗角的應力集中是關鍵（p062–p065、[2]），兩邊並列，不下單一原因結論。
- **FAA 的「一千次」沒有用**：FAA 教材一方面寫水槽測試機 G-ALYU 撐了約 3,060 次加壓飛行，一方面寫量產機「只到約 1,000 次」；兩個數字放在一起小孩會以為矛盾，片中只用 3,060（說「三千多次」並說明含以前真的飛過的）。
- **「彗星號之後全世界改圓窗」不說**（舊查核 `week4/T07.md` 已列為需修正）；只說彗星號自己後來的改法（p149–p151）。
- **窗戶小洞會減少起霧**（[14]）本集不講，免得岔題；小洞只用來說明平常是外層撐壓差（p047–p049）。
- **不讀到的**：FAA 舊網址 `lessons_learned/.../G-ALYP` 回 404，同一份教材現在在 `.../G-ALYV`（[2]）；FAA 機務手冊 Airframe 第 1 章（窗框加強）本輪找不到現行 PDF 網址，改用 Withey 2019（[12]）的「Thicker skin around the windows」。

## 當天重讀的來源（2026-11-13，curl GET；HTML 去標籤轉純文字後逐段讀；PDF 用 `pdftotext -layout`）

- [1] FAA, *Pilot's Handbook of Aeronautical Knowledge*（FAA-H-8083-25），Chapter 7 Aircraft Systems：200（18,237,698 bytes），讀 Pressurized Aircraft 全節（p.7-34 到 7-36，含 Figure 7-41 壓力表）。
- [2] FAA, *Lessons Learned from Transport Airplane Accidents*: de Havilland DH-106 Comet 1：200（151,954 bytes），讀全文（Accident Overview、Fuselage Testing、Stress Concentrations at Window Corners、Accident Board Findings、Resulting Safety Initiatives、Airworthiness Directives、Lessons Learned）。頁尾 Last updated: Tuesday, January 6, 2026。
- [3] M. E. Tuttle（University of Washington），*Stress Concentrations* 講義：200（1,600,137 bytes），讀前 12 頁（定義、Kirsch 圓孔解、Inglis 橢圓孔）。
- [4] DoITPoMS（University of Cambridge），Brittle Fracture: Inglis and the crack tip stress idea：200（19,825 bytes），讀全頁。
- [5] UNSW Sydney School of Materials Science and Engineering, Crack theory: Introduction：200，讀全頁。
- [6] UNSW, Fatigue failure：200，讀全頁。
- [7] UNSW, Fracture mechanics：200，讀全頁。
- [8] UNSW, Fracture toughness：200，讀全頁（公式是圖，不引用）。
- [9] UNSW, Brittle fracture（glass rod）：200，讀全頁（素材池 H3061）。
- [10] UNSW, Ductile fracture（copper rod）：200，讀全頁（素材池 H3061）。
- [11] P. A. Withey, *Fatigue failure of the de Havilland Comet I*（Failure Analysis Case Studies II／Engineering Failure Analysis, 1997）：200（199,329 bytes），讀結論段。
- [12] P. A. Withey, *The de Havilland Comet*（RAeS Hamburg Branch 演講投影片，2019-01-24，HAW Hamburg 網站）：200（3,489,479 bytes），讀 Comet I 改裝、Modern Analysis、Comet 4。
- [13] 14 CFR 25.571 Damage-tolerance and fatigue evaluation of structure（eCFR renderer API）：200（18,314 bytes），讀 (a)。
- [14] Mark Vanhoenacker（航空公司機長），Slate〈What's That Thing: Why are there holes in airplane windows?〉（2015-05）：200（240,515 bytes），讀全文。
- 素材池 H3060（[7]、[8]、[5]）與 H3061（[9]、[10]）在 2026-11-13 重開讀過；舊查核 `so-thats-why/week4/T07.md` 只當線索。

---

## C01 飛得高比較省油、能飛在壞天氣上面【主管機關手冊】

- **可用說法**：p020–p021
- **來源**：[1] p.7-34
- **原文**：「an aircraft flown at high altitude consumes less fuel for a given airspeed than it does for the same speed at a lower altitude because the aircraft is more efficient at a high altitude. Second, bad weather and turbulence may be avoided by flying in relatively smooth air above the storms.」
- **注意**：「省油」是「同樣空速下較省油」的白話；「暴風雨上面」照 above the storms。

## C02 約八千五百公尺高，空氣壓力只剩地面三分之一左右【主管機關手冊＋換算】

- **可用說法**：p022–p024（回收開場 p012–p013 的「外面跟裡面不同」）
- **來源**：[1] Figure 7-41
- **原文**：「Sea level 14.7」「28,000 4.8」「At an altitude of 28,000 feet, standard atmospheric pressure is 4.8 psi.」
- **注意**：28,000 英尺 ≈ 8,534 公尺，說「大約八千五百公尺」；4.8 ÷ 14.7 ≈ 0.33，說「三分之一左右」。這是標準大氣，不是某一班飛機的實測。p022 小問問「外面的空氣」，所長答「很稀」是壓力低的白話。

## C03 機艙封起來、打進空氣、壓力比外面高，叫加壓【主管機關手冊】

- **可用說法**：p027–p028、p031（小問複述）
- **來源**：[1] p.7-34
- **原文**：「In a typical pressurization system, the cabin, flight compartment, and baggage compartments are incorporated into a sealed unit capable of containing air under a pressure higher than outside atmospheric pressure. On aircraft powered by turbine engines, bleed air from the engine compressor section is used to pressurize the cabin.」「Pressurization of the aircraft cabin is necessary in order to protect occupants against hypoxia.」
- **注意**：「空氣比外面多」是「壓力比外面高」的白話；p026 小問「會喘不過氣嗎？」→「不會」照 protect occupants against hypoxia。

## C04 通常讓機艙像大約兩千四百公尺的山上，人待著舒服【主管機關手冊＋換算】

- **可用說法**：p029–p030
- **來源**：[1] p.7-35
- **原文**：「A cabin pressurization system typically maintains a cabin pressure altitude of approximately 8,000 feet at the maximum designed cruising altitude of an aircraft.」「occupants can be transported comfortably and safely for long periods of time, particularly if the cabin altitude is maintained at 8,000 feet or below」
- **注意**：8,000 英尺 ≈ 2,438 公尺，說「大約兩千四百公尺」；保留 typically（「通常」）。

## C05 裡面的空氣把機身往外推；裡外的差叫壓差【主管機關手冊＋比喻】

- **可用說法**：p033–p035（氣球是比喻）
- **來源**：[1] p.7-35
- **原文**：「Differential pressure—the difference in pressure between the pressure acting on one side of a wall and the pressure acting on the other side of the wall. In aircraft air-conditioning and pressurizing systems, it is the difference between cabin pressure and atmospheric pressure.」
- **注意**：「往外推」是裡面壓力較高的結果（[14] 也說 the pressure inside the aircraft during flight is typically much greater than the pressure outside）。氣球只說明「裡面空氣多就把外皮撐開」；氣球皮會大幅伸長，機身不會，片中不說兩者一樣。

## C06 機身設計時定好最多撐多大的壓差，加壓不能超過；所以機艙不會加到跟地面一樣【主管機關手冊＋撰稿推論】

- **可用說法**：p036–p039
- **來源**：[1] p.7-35、7-36
- **原文**：「When an aircraft reaches the altitude at which the difference between the pressure inside and outside the cabin is equal to the highest differential pressure for which the fuselage structure is designed, a further increase in aircraft altitude will result in a corresponding increase in cabin altitude. Differential control is used to prevent the maximum differential pressure, for which the fuselage was designed, from being exceeded.」「Primarily, the fuselage is designed to withstand a particular maximum cabin differential pressure.」
- **注意**：p037「所以機艙不會加到跟地面一樣」是 C04（約 8,000 英尺）加本條推出來的**撰稿推論**，手冊沒有這句。p036 氣球吹太多會破是常識。

## C07 每飛一趟就是撐一下、鬆一下【主管機關事故教材＋撰稿推論】

- **可用說法**：p040–p043、p097（還記得）
- **來源**：[2] Fuselage Testing
- **原文**：「additional water was pumped into the cabin until the pressure inside the fuselage reached 1P, the equivalent of flight. This was then cycled to simulate many flights over the life of an aircraft.」「The Elba aircraft had experienced 1,290 pressurized flights.」
- **注意**：教材把「一次加壓循環」當成「一趟飛行」。「落地前把壓放掉」是一趟加壓循環的白話（**撰稿推論**，不講機上實際洩壓程序）。

## C08 客機窗戶通常三層；中間那層的小洞讓夾縫和機艙等壓，平常是最外層撐壓差；中間那層也撐得住，外層壞了接手【專業人士文章，引製造商】

- **可用說法**：p044–p051
- **來源**：[14]
- **原文**：「If you look closely at a typical passenger cabin window, you'll see three panes, typically made of acrylic materials.」「Both the middle and the outer panes are strong enough to withstand the difference on their own, but under normal circumstances it's the outer pane that bears this pressure—thanks to the breather hole.」Marlowe Moncur（GKN Aerospace 技術總監）：「the purpose of the small bleed hole in the [middle] pane is to allow pressure to equilibrate between the passenger cabin and the air gap between the panes, so that the cabin pressure during flight is applied to only the outer pane.」「In the extraordinarily unlikely event that the outer pane fails, the middle pane takes over.」
- **注意**：作者在文中自稱 airline pilot（「You're an airline pilot, they say」），片中說「一位機長寫的文章，問過做飛機窗戶的公司」。保留「通常」（typical）。這是窗戶本身的設計，不是機身開口周圍的金屬；C09 之後講的是機身。

## C09 機身能撐多大的壓差，看結構強度，也常看窗戶和門這些地方【主管機關手冊】

- **可用說法**：p052–p054
- **來源**：[1] p.7-36
- **原文**：「This differential pressure is determined by the structural strength of the cabin and often by the relationship of the cabin size to the probable areas of rupture, such as window areas and doors.」
- **注意**：保留 often（「常」）。p055「它們都是在機身上開的一個洞」是常識。

## C10 洞那裡沒有金屬，力只好繞過去；圓角讓力順著邊走、不太堆積，方角的尖角力轉不過去、擠在角上【主管機關事故教材＋大學教材】

- **可用說法**：p055–p056、p062–p065
- **來源**：[2] Stress Concentrations at Window Corners；[7]
- **原文**：[2]「A stress concentration is a very localized area of much higher stress than the surrounding area. The stress concentrations were high specifically because of the squarish shape of the windows and window frames which is very different from the round/oval shapes of modern airplane windows. With modern windows, the stress flows freely around the curved edges with minimal build up. But with the Comets' squarish windows, stress cannot smoothly flow around the abrupt corners. This creates stress concentrations.」[7]「The stress cannot be transferred through the crack, and therefore stress is concentrated at either side of the crack.」
- **注意**：[7] 講的是裂縫，p056「洞那裡沒有金屬，推力只好繞過去」是同一個道理用在開孔上的**撰稿推論**，[2] 的 flows around 支持。「推力」接 C05 的空氣推力，進到機身後改說「力」。

## C11 那一小塊金屬撐的力比旁邊多很多，叫應力集中；應力是金屬每一小塊撐著的力【主管機關事故教材＋大學教材】

- **可用說法**：p066–p070
- **來源**：[2]、[3]
- **原文**：[2]「A stress concentration is a very localized area of much higher stress than the surrounding area.」[3]「A "stress concentration" refers to an area in a object where stress increases over a very short distance」
- **注意**：「應力」定義成「每一小塊撐著的力」是給八歲小孩的**簡化**（應力是單位面積上的內力）。

## C12 一大片被拉的薄板上開圓洞，洞邊的應力約是遠處的三倍【大學教材】

- **可用說法**：p071–p073
- **來源**：[3]
- **原文**：「In 1898 Ernst Kirsch … published a solution for the elastic stresses near a circular hole in an isotropic "infinitely large" thin plate」「Stresses at the edge of the hole (at x = a): … σθθ = σyy = 3σo」「The stress concentration factor for a circular hole in an infinite plate: Kt = σyy/σo = 3」
- **注意**：條件是「很大的薄板、單向拉、彈性範圍」，片中說「一大片被拉的薄板」；不把三倍說成飛機窗戶的實際數字。

## C13 裂縫越尖，尖端應力大得多；角越尖擠得越厲害【大學教材＋撰稿推論】

- **可用說法**：p074–p076
- **來源**：[4]；[2]
- **原文**：[4]「In 1913, Inglis calculated what the stresses and strains were in an elastic plate containing an elliptical crack … For a sharp crack, i.e. c >> b, the stress would be much greater at the crack tip」[2]（同 C10，方角的 abrupt corners 造成高應力集中）
- **注意**：[4] 講的是橢圓形裂縫越扁越尖；p076「角越尖，力就擠得越厲害」把它用到轉角，是**撰稿推論**，[2] 的方窗角說法支持方向，但沒有給倍數，片中也不給。

## C14 洞、轉角、溝槽、裂縫旁邊常有應力集中；鉚釘孔也是洞【大學教材】

- **可用說法**：p077–p079、p129–p130（回收）
- **來源**：[3]
- **原文**：「Stress concentrations typically occur due to some localized change in geometry (near holes, filets, corners, grooves, cracks, etc)」
- **注意**：p130 把鉚釘孔接回「洞」是本條的直接應用（**撰稿推論**），C19 Withey 的觀察支持。

## C15 方洞那條紙從角裂開；你剪的方角就是力最擠的地方【示範＋大學教材】

- **可用說法**：p080–p083（回收開場 p003 的紙飛機裂口）
- **來源**：示範（未實測）；[9]
- **原文**：[9]「if the rod has a small notch, the force required to cause fracture is greatly reduced, and the rod breaks. Observe how the fracture originates from the notch.」
- **注意**：見文首。紙不是金屬，示範只說明「裂口從力最擠的角開始」。

## C16 金屬被一次又一次拉，就算每次都不大也可能裂開，叫金屬疲勞；裂縫常從表面冒出、每拉一次往前長一點；機身每次被撐不會像迴紋針被扳彎【大學教材＋示範】

- **可用說法**：p086–p097
- **來源**：[6]
- **原文**：「Many applications exist where a material is subjected to a repeated cyclic stress. These materials are found to fail after a large number of applications of the stress even though the cyclic stress that is applied is below their yield strength. This mode of failure is termed fatigue.」「the material fails due to progressive stepwise crack growth through the sample.」「Initially, a crack is nucleated, usually at the surface of the component.」
- **注意**：p086「撐一次不會」是常識（機身設計就是要撐住一次加壓，C06）。迴紋針斷掉（p088）是常識示範；它被扳到彎曲變形，屬於比機身嚴重得多的情況，所長在 p095 說明不一樣（below their yield strength 的白話）。「金屬也會累」所長回「那是比喻」（p092）。「澳洲一所大學」＝ UNSW Sydney。

## C17 疲勞的裂縫從應力集中的地方長起來【大學教材】

- **可用說法**：p098–p101
- **來源**：[5]；[6]
- **原文**：[5]「In both fast fracture and fatigue, crack growth occurs from the presence of stress concentrations where there is a localised build up of stress around the crack tip.」[6]「Cracks create stress concentrations that raise the level of stress to a level above the yield strength of the material in the vicinity of the crack.」
- **注意**：p100 小問答「窗戶的角」是從 C10 推的；彗星號的實際起點在 C19、C20。

## C18 裂縫短時撐得住，長到某個長度會突然很快裂過去；什麼時候快裂，看裂縫多長、拉得多用力（還有材料）【大學教材，素材池 H3060】

- **可用說法**：p102–p106；材料接 C22
- **來源**：[5]、[6]、[7]、[8]
- **原文**：[6]「Subsequently, the crack propagates over time until a critical crack length is reached. Finally, the crack is large enough that the material cannot support the nominal applied stress and the material undergoes fast fracture.」[7]「When an increasing stress is applied to a material containing a crack of length a, a stress is reached at which the crack will propagate. Or, for a given applied stress, there is a crack size at which the crack will propagate.」[8]「fast fracture occurs when a critical stress intensity factor, Kc, is reached … Kc is referred to as the fracture toughness of the material.」[5]「Ultimate failure occurs when the crack has a length greater than the critical crack length for which the material can support its load.」
- **注意**：不引用公式，不給任何安全數值，不由外觀判斷實物安全（素材池 H3060 的範圍）。

## C19 彗星號：FAA 教材的例子；世界第一種載客的加壓噴射客機；1954 年兩架在飛行中出事【主管機關事故教材】

- **可用說法**：p107–p111
- **來源**：[2]
- **原文**：「The de Havilland DH-106 Comet 1 became the world's first pressurized civilian jet transport with its inaugural flight on May 2, 1952」「On January 10, 1954, Comet G-ALYP departed Ciampino Airport, Rome for London … indicating a failure of the aircraft with "catastrophic suddenness."」「on April 8, 1954, Comet G-ALYY … experienced a catastrophic in-flight break-up and crashed into the sea near Naples.」
- **注意**：只說「有兩架在飛行中出事」，不講人數、不重演；1953 年加爾各答那架官方原因是雷雨，不提。

## C20 水槽加壓測試，加上以前真的飛過的共三千多次，從方方的艙口窗角裂開；撈回那架最先裂在機頂兩個方方的天線窗；這一架的結論是加壓機艙因疲勞而壞【主管機關事故教材】

- **可用說法**：p112–p119
- **來源**：[2]
- **原文**：「a water tank was constructed to encase the fuselage. The fuselage was submerged and filled with water, and then additional water was pumped into the cabin until the pressure inside the fuselage reached 1P, the equivalent of flight. This was then cycled to simulate many flights」「G-ALYU had undergone 1,230 pressurized flights before testing and 1,830 tank "flights" before the fuselage failed at the corner of a squarish forward escape hatch window.」「G-ALYU withstood about 3,060 pressurized "flights," whether in the air or in the water tank.」「the aircraft's Automatic Direction Finder (ADF) windows, also squarish, were recovered within hours. The ADF windows are on the very top of the fuselage … bore the "unmistakable fingerprint of fatigue," and was determined to be the first fracture of the Elba crash.」RAE：「We have formed the opinion that the accident at Elba was caused by structural failure of the pressure cabin, brought about by fatigue. … Owing to the absence of wreckage, we are unable to form a definite opinion on the cause of the accident near Naples」
- **注意**：「三千多次」＝ about 3,060（含 1,230 次實飛）。Withey 1997（[11]）寫水槽機的破口從前左逃生艙口附近的鉚釘孔長出；FAA 寫 at the corner，兩者都指向開口轉角附近，片中照 FAA。「天線窗」＝ ADF windows。p119 只說「這一架」，不延伸到拿坡里那架。

## C21 工廠拿一個機身測過一萬六千次，但它先被加過兩倍壓力，角上的金屬因此改變，次數太樂觀【主管機關事故教材】

- **可用說法**：p120–p123
- **來源**：[2]
- **原文**：「De Havilland tested their prototype to 2P, twice the expected operating pressure. The pressure overload combined with the very high stress levels at the window corners, created stress levels at the concentrations great enough to change the material characteristics at these locations.」「The prototype fuselage withstood 16,000 cycles before failure, due in large part to the fundamentally different material characteristics of the cold-worked material at the window corners. This characteristic change actually improved the fatigue properties at these locations, which would mask the true fatigue vulnerability of the production Comet.」
- **注意**：「太樂觀」＝ mask the true fatigue vulnerability。FAA 的 Lessons Learned：test specimens must be representative of the production airplane（片中沒有念出來）。

## C22 不是只怪方窗：裂縫都從開口旁邊的鉚釘孔、螺栓孔長出；那位學者認為窗戶怎麼固定可能比形狀還要緊【研究論文】

- **可用說法**：p124–p132；p128 鉚釘的白話
- **來源**：[11]；[12]
- **原文**：[11]「All the observed cracks in the pressure cabin emanated from bolt or rivet holes near the cut-out areas. It was probably not the shape of the cut-outs that was so damaging to the fatigue life of the cabin, rather the method of fixing the windows and doubler plates onto the pressure cabin. Had the windows not been square then the "Redux" glueing method might have been applied to these areas, and the failure avoided.」[12]「The manufacturing process of punch riveting (rather than drill, rivet and glue) caused small cracks which grew under the repeated loading of the pressure cabin」
- **注意**：標成「那位學者認為……可能」，不是官方結論；p132「形狀、孔和做法是連在一起的」照 [11] 的 Had the windows not been square … Redux。作者 P. A. Withey 在伯明罕大學（[11] 署名 School of Metallurgy and Materials, The University of Birmingham），片中說「一位英國學者」。

## C23 圓角讓力不那麼擠；FAA 的教訓：材料、厚度、形狀、受力、保養都要仔細顧到【主管機關事故教材＋撰稿推論】

- **可用說法**：p133–p137
- **來源**：[2] Lessons Learned
- **原文**：「Not knowing enough about the fatigue properties of complex structures can have catastrophic results. Detailed attention must be paid to aspects such as material choice, thickness, geometry, stress levels, maintenance, and usage. Even large static strength margins do not negate the effects of fatigue.」
- **注意**：p134「裂縫比較難冒出來」是 C10＋C17 的**撰稿推論**。usage（怎麼使用）片中沒有念。

## C24 同樣有缺口：玻璃棒很小的力就從缺口斷；銅棒先彎、缺口沒讓它比較容易斷，斷前變形吸收很多能量；只是這兩根的比較【大學教材，素材池 H3061】

- **可用說法**：p138–p147
- **來源**：[9]、[10]
- **原文**：[9]「It takes a lot of force to deform a glass rod. … But if the rod has a small notch, the force required to cause fracture is greatly reduced, and the rod breaks. Observe how the fracture originates from the notch.」「Brittle fracture is characterised by low plastic deformation and small amounts of energy absorption at failure」[10]「If we apply a force to a copper rod that contains a small notch the rod plastically deforms and the notch does not decrease the force required to break the rod. … In ductile fracture there is a lot of plastic deformation, and significant energy is absorbed before the fracture.」
- **注意**：「力氣」＝能量的白話。p147 照素材池範圍：不把所有金屬或玻璃一概分類。片中沒有說飛機用銅（飛機機身不是銅），只用來說明「材料也有差」。

## C25 彗星號的改法：窗戶周圍金屬加厚；新型號換窗戶設計、少打鉚釘；有一款改良型窗戶改成橢圓形【研究演講＋主管機關事故教材】

- **可用說法**：p148–p151
- **來源**：[12]；[2]
- **原文**：[12]「The Comet I was grounded until changes were made to the pressure cabin – Thicker skin around the windows – Altered shape to allow 'Redux' fixing」「The Comet flew again as the Comet IV – Different window design to reduce riveting – Fewer manufacturing cracks」[2]「It wasn't until the next model, the Comet 1XB, that the window shape was changed from squarish to the now-conventional oval shape.」
- **注意**：「那位學者整理過」＝ Withey 2019 演講。不說全業界從此規定圓窗。

## C26 現在的設計先想好萬一有裂縫怎麼辦：力有別條路可走、裂縫能停下或轉向【主管機關事故教材＋比喻】

- **可用說法**：p152–p156（p155「像小溪分成好幾條」所長答「有點像」）
- **來源**：[2] Resulting Safety Initiatives
- **原文**：「In fail-safe design, a critical part has redundancies, alternate load paths, and provisions for cracks to be stopped and turned, should they occur. … Today, both the fail-safe and safe-life philosophies have evolved into "damage tolerant" standards, which integrates attributes of each approach into one objective standard. Damage tolerance involves a structural capability that provides safe operation with specific failure or damage conditions which may exist」
- **注意**：fail-safe 是 707 那一代的設計哲學，今天演進成 damage tolerance；片中「現在的設計，會先想好萬一裂了怎麼辦」是 damage tolerance 的白話，後兩句的做法出自 fail-safe 段（今天的標準整合了它）。

## C27 美國法規：要證明在使用年限內不會因疲勞出大事，製造瑕疵也算，還要訂好檢查讓維修的人照著做【法規】

- **可用說法**：p157–p163
- **來源**：[13] §25.571(a)
- **原文**：「An evaluation of the strength, detail design, and fabrication must show that catastrophic failure due to fatigue, corrosion, manufacturing defects, or accidental damage, will be avoided throughout the operational life of the airplane.」「Based on the evaluations required by this section, inspections or other procedures must be established, as necessary, to prevent catastrophic failure, and must be included in the Airworthiness Limitations section of the Instructions for Continued Airworthiness」
- **注意**：這是美國運輸類飛機（Part 25）的適航規定，片中說「美國的法規」；「讓維修的人照著做」＝ Instructions for Continued Airworthiness 的白話。看牙醫是小問的比喻，所長答「有點像」。插圖 `inspector` 是示意，不是某家公司的實際檢查程序。

## C28 溪流比喻【比喻／示意】

- **可用說法**：p057–p065、p155
- **注意**：比喻只說兩件事：(1) 力遇到開口要繞過去；(2) 繞過圓邊順、在尖角擠。依據是 [2] 的 flows freely around the curved edges／cannot smoothly flow around the abrupt corners。**限度**：機身裡的力不是流動的水，沒有流速；水在方塊角前「擠成一團」是示意，不代表應力的分布形狀。插圖不畫應力色圖。

## C29 故事設定與片尾【故事】

- p001–p007、p165–p173 的紙飛機、明天坐飛機、靠窗是故事設定。p168–p170 小問的答案是 C10、C27 的白話；p171–p172 所長的看法標成「我覺得」，依據 C23、C25–C27。p174 留言題。

---

## 來源

1. FAA, Pilot's Handbook of Aeronautical Knowledge (FAA-H-8083-25), Chapter 7 Aircraft Systems. https://www.faa.gov/sites/faa.gov/files/09_phak_ch7.pdf
2. FAA, Lessons Learned from Transport Airplane Accidents: de Havilland DH-106 Comet 1 (last updated 2026-01-06). https://www.faa.gov/lessons_learned/transport_airplane/accidents/G-ALYV
3. M. E. Tuttle, University of Washington, Stress Concentrations (lecture notes). https://courses.washington.edu/mengr556/StressConcentrations.pdf
4. DoITPoMS, University of Cambridge, Brittle Fracture: Inglis and the crack tip stress idea. https://www.doitpoms.ac.uk/tlplib/brittle_fracture/crack_tip_stress.php
5. UNSW Sydney School of Materials Science and Engineering, Crack theory: Introduction. https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/introduction
6. UNSW Sydney, Fatigue failure. https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/fatigue-failure
7. UNSW Sydney, Fracture mechanics. https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/fracture-mechanics
8. UNSW Sydney, Fracture toughness. https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/fracture-mechanics/fracture-toughness
9. UNSW Sydney, Brittle fracture (glass rod). https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/introduction/brittle-facture
10. UNSW Sydney, Ductile fracture (copper rod). https://www.unsw.edu.au/science/our-schools/materials/engage-with-us/high-school-students-and-teachers/online-tutorials/crack-theory/introduction/ductile-fracture
11. P. A. Withey, Fatigue failure of the de Havilland Comet I (1997). https://ae.iitm.ac.in/~nidish/courses/as3020/files/mod2/dehavcomet.pdf （出版頁 https://research.birmingham.ac.uk/en/publications/fatigue-failure-of-the-de-havilland-comet-i/ ）
12. P. A. Withey, The de Havilland Comet, RAeS Hamburg lecture (2019-01-24). https://www.fzt.haw-hamburg.de/pers/Scholz/dglr/hh/text_2019_01_24_Comet.pdf
13. 14 CFR 25.571 Damage-tolerance and fatigue evaluation of structure. https://www.ecfr.gov/current/title-14/section-25.571
14. Mark Vanhoenacker, Slate, "Why are there holes in airplane windows?" (2015-05). https://slate.com/human-interest/2015/05/whats-that-thing-why-are-there-holes-in-airplane-windows.html
