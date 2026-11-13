# 查核報告 2（sothatswhy-p26-plane-window）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有寫 verify-1.md）
- 日期：2026-11-13
- 範圍：verify-1.md 之後改寫或新增的台詞（現行 `video.json` 的 44 句，見下），每句連前後一句讀；verify-1 的 F01–F07 是否照改；刪掉的段落有沒有讓別句失去前提；彗星號段落是否仍沒有單一原因結論、是否清楚說「疲勞的結論是對從厄爾巴島外海撈回的那一架」；YouTube 說明欄、標籤、縮圖與參考資料是否跟片子一致；字數與拉丁字母；`claims.md` 各列行號對不對得上現行 p-id。其餘台詞沒有重查，結論沿用 verify-1.md。
- 比對方法：把 verify-1 查的第一版（session 暫存的 `p26/v0.json`，176 句，p001–p176）跟現行版（170 句，p001–p170）逐句 diff（difflib 對台詞文字）。撰稿方的 `changed.txt` 只當線索；逐條對過，**沒有漏列**，也沒有清單外的改動。`script.md` 逐句比對也跟 `video.json` 一致。
  - 改寫或新增的 44 句：p001、p002、p003、p005、p009、p020、p021、p022、p031、p039、p047、p048、p051、p052、p057、p061、p068、p069、p071、p078、p087、p096、p098、p105、p112、p113、p114、p115、p117、p126、p130、p131、p132、p133、p135、p140、p141、p143、p144、p145、p148、p150、p163、p164。
  - 沒有對應舊句的新句：p002（舊 p001 拆成兩句）、p021、p051、p112；舊 p117 拆成 p113＋p114。
  - 刪掉：舊 p045–p051（三層窗、中層小洞、外層撐壓差、中層接手，含 verify-1 F01 那一句）、舊 p076（併入 p071）、舊 p135–p137（「航空總署的教訓」併入 p131；五項清單刪掉）。各區塊增減 +1 +1 −7 +1 −1 +1 −2 = −6，176 − 6 = 170。
- verify-1 的七項必改：F01 那一句隨三層窗整段刪掉（已解決，但 `claims.md` 文首仍寫「機長」，見 F02）；F02 p069 照建議句；F03 p163 改成「力就像繞過圓石頭的水！」，不是建議句，但不再說「不會擠」，沒有過度宣稱，可以；F04 p052 照建議句，並新增 p051 交代「被撐開→金屬被拉緊」；F05 p009 照建議句（**實拉紀錄仍是空的**，見選修 S6）；F06 p020 照建議句；F07 說明欄照建議句。選修 S1、S2、S3、S4、S5、S6 也照改；S8 刪了「去找外婆」。
- 來源：`claims.md` 只當線索，不採用它的引文。今天在新的空目錄重新 curl GET（全部 200），HTML 去掉 script／style 與標籤轉純文字後 grep 並讀上下文，PDF 用 `pdftotext -layout`：
  - FAA《Pilot's Handbook of Aeronautical Knowledge》第 7 章（200，18,237,698 bytes），讀 p.7-34 到 7-36
  - FAA〈Lessons Learned … de Havilland DH-106 Comet 1〉（`.../accidents/G-ALYV`，200，151,954 bytes；頁尾 "Last updated: Tuesday, January 6, 2026"），讀全文
  - M. E. Tuttle〈Stress Concentrations〉講義（200，1,600,137 bytes）
  - DoITPoMS〈Inglis and the crack tip stress idea〉（200，19,825 bytes）
  - UNSW Sydney Crack theory：Introduction、Fatigue failure、Fracture mechanics、Brittle fracture、Ductile fracture（皆 200）
  - P. A. Withey 1997〈Fatigue failure of the de Havilland Comet I〉（IIT Madras 網址，200，199,329 bytes），讀全文
  - P. A. Withey 2019 RAeS Hamburg 演講（200，3,489,479 bytes）
  - 14 CFR 25.571（eCFR renderer API，200，18,314 bytes）
- 結論統計（44 句）：**正確 43、需改 1、錯誤 0**。說明欄、標籤、縮圖、參考資料 4 項：**正確 4**。`claims.md`：行號大致對得上，但有 4 處要同步（F02）。另有 6 處選修建議（不影響結論，見文末）。
- 字數：全部 170 句含標點計算（NFC 後的字元數），小問最長 14 字（p003），所長最長 25 字（p009、p115），沒有超過上限（小問 15、所長 25）。台詞沒有拉丁字母與阿拉伯數字，`build_scenes.py` 的 SAY 表是空的，符合。下文建議句也照同一算法。

## 一、需改的地方與理由

| 編號 | 行 | 現行台詞 | 結論 | 依據與理由 |
| --- | --- | --- | --- | --- |
| F01 | p140（所長） | 對，它斷之前會先變形，吸收很多力氣。 | 需改（新加的「對」把一根銅棒的單次實驗說成「金屬不怕缺口」） | 前句 p139 小問「銅會彎，所以不怕缺口？」。UNSW〈Ductile fracture〉只講一次施力：「If we apply a force to a copper rod that contains a small notch the rod plastically deforms and the notch does not decrease the force required to break the rod.」第一版 p146–p147 沒有「對」，而且有「這只是這兩根的比較，不是所有金屬和玻璃」；第二版把但書刪了，又在開頭加「對」，等於所長確認「銅（金屬）不怕缺口」。這跟本集的主線正好相反：機身是金屬，片中 p096、p122、p126 才說疲勞裂縫從金屬上力最擠的地方、鉚釘孔長出來（UNSW〈Fatigue failure〉"Cracks create stress concentrations…"；Withey 1997 "All the observed cracks in the pressure cabin emanated from bolt or rivet holes near the cut-out areas"）。後句 p141「可是挑好了，還是可能疲勞」救回一半，但沒有說缺口在反覆拉時仍然要緊。`claims.md` C24 自己的規則也是「片中只講這兩根，不說金屬都會彎」。把「對」限定成「拉一次」即可，p141 接得更順（拉一次不怕，拉很多次還是可能疲勞） |

## 二、逐句核對

| 行 | 現行台詞 | 結論 | 來源 | 依據摘要與前後文 |
| --- | --- | --- | --- | --- |
| p001（小問） | 所長！事務所有膠帶嗎？ | 正確（故事） | — | 沒有事實主張。第一句就把地點放在事務所；圖 `tube-tear` 桌上有一卷膠帶，相符。後句 p002 |
| p002（小問） | 我做的飛機裂開了！ | 正確（故事） | — | 舊 p001 的後半。後句 p003 |
| p003（小問） | 明天要坐飛機，我先做了一架。 | 正確（故事） | — | 前句 p002，後句 p004「你看，從窗戶的角裂開的」。14 字 |
| p005（所長） | 有。先讓我看看。你剪的窗戶，是方方的？ | 正確（故事） | — | 「有」回答 p001 的膠帶，p001 不會沒人接。前句 p004，後句 p006「對啊，跟我家的窗戶一樣」 |
| p009（所長） | 我這裡有兩條硬紙，一條剪方洞，一條剪一樣寬的圓洞。 | 正確（verify-1 F05 照改；示範未實測） | 示範；UNSW Brittle | 照 F05 建議句，25 字到上限。「兩條硬紙」沒有說一樣寬，但圖與 `claims.md` C15 都寫明兩條同寬，台詞可以不念。實拉紀錄見選修 S6。後句 p010「哪一條先破？」在 p075–p076 回收 |
| p020（所長） | 就是飛機那一整條長長的身體，外面多半包著金屬。 | 正確（verify-1 F06 照改） | Boeing（verify-1 已讀） | 「多半」涵蓋 787 這類複合材料機身。前句 p019「機身是什麼？」，後句 p021 |
| p021（小問） | 它幹嘛要飛那麼高？ | 正確（提問） | — | 「它」＝p020 的飛機，「那麼高」回指 p013「飛機飛高以後」，前提在。讓 p022–p023 的手冊句變成回答，不再突兀 |
| p022（所長） | 美國聯邦航空總署的飛行手冊說， | 正確 | PHAK | 手冊全名 Pilot's Handbook of Aeronautical Knowledge，「飛行手冊」是合理譯法。後句 p023「飛得高比較省油，還能飛在暴風雨上面」＝"consumes less fuel for a given airspeed … more efficient at a high altitude"、"flying in relatively smooth air above the storms" |
| p031（所長） | 通常讓機艙裡的空氣， | 正確 | PHAK p.7-35 | 接 p032「像在大約兩千四百公尺的山上」＝"typically maintains a cabin pressure altitude of approximately 8,000 feet at the maximum designed cruising altitude"（8,000 ft ≈ 2,438 m）。拿掉「手冊說」後主詞是前句 p030 的加壓，聽得懂；p025 已掛名手冊，「通常」保留 typically |
| p039（所長） | 對。所以飛很高時，機艙不會加到跟地面一樣。 | 正確（verify-1 S4 照改；撰稿推論） | PHAK p.7-35、7-36 | 前句 p038「氣球吹太多，會破掉！」。手冊 "the fuselage is designed to withstand a particular maximum cabin differential pressure"，加上約 8,000 ft 的艙壓高度，推得出來；「飛很高時」把低空時艙壓等於地面的情況排除了。後句 p040 手冊的壓差上限 |
| p047（所長） | 會。手冊還說，機身能撐多大的壓差， | 正確 | PHAK p.7-36 | 「會」回答 p046「那窗戶也被推嗎？」（裡外壓差當然也作用在窗戶上）。「還」接 p040 的「手冊說」 |
| p048（所長） | 常要看窗戶和門這些地方。 | 正確（簡化，保留 often） | PHAK p.7-36 | "This differential pressure is determined by the structural strength of the cabin and often by the relationship of the cabin size to the probable areas of rupture, such as window areas and doors."「常」＝often。第一版的「要看它多強」刪掉，結構強度沒念出來，見選修 S5；不算錯。後句 p049「窗戶跟門，有什麼特別？」 |
| p051（所長） | 機身被撐開時，外面那層金屬被拉得緊緊的。 | 正確（verify-1 F04 的橋） | Withey 1997；Withey 2019 | 前句 p050「它們都是在機身上，開的一個洞」，前提 p036「裡面的空氣，把機身往外推」。Withey 1997 分析的就是彗星號蒙皮的拉應力："a uniaxial tensile stress … This may not have been the case for the Comet skin, and a biaxial tensile stress field may be closer to reality"；Withey 2019 "The hoop stress can be calculated – 128 MPa for the general skin"。`claims.md` C10 把它記成「常識白話」，可以補上這兩句當依據（選修 S4）。「外面那層金屬」回指 p020 |
| p052（所長） | 洞那裡沒有金屬，機身裡的拉力只好繞過去。 | 正確（verify-1 F04 照改） | FAA Comet；UNSW Fracture mechanics | FAA "the stress flows freely around the curved edges"；UNSW "The stress cannot be transferred through the crack, and therefore stress is concentrated at either side of the crack."主詞從「推力」改成「機身裡的拉力」，小孩不會再想成空氣繞過窗戶。後句 p053「繞過去？怎麼繞？」，同一個鏡頭 `hole-skin`（圓角窗加鉚釘的機身側面），相符 |
| p057（小問） | 水到角那裡，擠得好急！ | 正確（比喻；verify-1 S2 照改） | FAA Comet | 前句 p056「換成一塊方方的水泥塊呢？」。「擠得好急」不會被想成水堆住不動，跟 FAA "cannot smoothly flow around the abrupt corners" 的「不順」一致。後句 p058「航空總署說，機身裡的力，也有點像這樣」 |
| p061（所長） | 方窗戶的尖角，力轉得太急，就擠在角上。 | 正確（verify-1 S3 照改） | FAA Comet | "stress cannot smoothly flow around the abrupt corners. This creates stress concentrations."「轉得太急」＝不能順順地繞過，比「轉不過去」準。前句 p060「那方方的窗戶呢？」，後句 p062「擠在角上，會怎樣？」 |
| p068（所長） | 也會。工程講義算過，一大片被拉的薄板開個圓洞， | 正確 | Tuttle | 前句 p067「那圓洞就不會擠嗎？」。Kirsch "a solution for the elastic stresses near a circular hole in an isotropic 'infinitely large' thin plate"——「算過」照解析解，用詞準 |
| p069（所長） | 洞邊應力最大的地方，大約是遠處的三倍。 | 正確（verify-1 F02 照改） | Tuttle；Withey 1997 | "Stresses at the edge of the hole (at x = a): σθθ = σyy = 3σo"、"Kt = σyy/σo = 3"；Withey 1997 "The stress around a cut-out was shown to be over 3 times the remote stress"。「最大的地方」守住只在兩側。後句 p070「那尖尖的角呢？」 |
| p071（所長） | 更厲害。裂縫或角越尖，尖端的應力就越大。 | 正確（教材＋撰稿推論） | DoITPoMS；FAA Comet | DoITPoMS "σt = σ(1 + 2c/b) … For a sharp crack, i.e. c >> b, the stress would be much greater at the crack tip"。「或角」把裂縫推到轉角，是 verify-1 已接受的推論（FAA abrupt corners 方向一致），沒有給倍數。「更厲害」比的是 p069 圓洞的三倍，邏輯通。拿掉「劍橋大學的教材說」後，DoITPoMS 仍在 `sources`（只靠這句用到），沒問題 |
| p078（所長） | 對。還記得方水泥塊的角嗎？你剪的就是那種角。 | 正確（回呼） | — | 前句 p077「跟我的飛機一樣！」；「還記得」點名回呼 p056–p057，前提在。後句 p079 轉到真的飛機。示範依據見 p009 |
| p087（所長） | 那是比喻。材料學的教材說， | 正確 | UNSW Fatigue | 前句 p086「金屬也會累喔？」，後句 p088–p089「裂縫常常先從表面冒出一點點，每拉一次，就往前長一點」＝"Initially, a crack is nucleated, usually at the surface"、"progressive stepwise crack growth"。不念學校名可以 |
| p096（所長） | 對。疲勞的裂縫，常從力最擠的地方長出來。 | 正確（verify-1 S1 照改） | FAA Comet；UNSW Introduction／Fatigue | FAA "Production airplanes … were found to form fatigue cracks near the corners of the windows"；UNSW "crack growth occurs from the presence of stress concentrations"。「常」是適當的保留。前句 p095「窗戶的角！」，後句 p097「小裂縫會一直長嗎？」 |
| p098（所長） | 裂縫還短的時候，材料撐得住。 | 正確 | UNSW Fatigue | "the crack propagates over time until a critical crack length is reached"；後句 p099「長到某個長度，它會突然很快地裂過去」。拿掉「教材說」不影響，p087 已掛名 |
| p105（所長） | 一九五四年，有兩架在飛行中出事，掉進海裡。 | 正確 | FAA Comet；Withey 1997 | Elba："crashed into the Mediterranean Sea near the Island of Elba"、"saw the aircraft fall into the sea in flames"；Naples："crashed into the sea near Naples"。不講人數，不提 1953 加爾各答。讓 p112–p113 的「海裡撈回」有前文 |
| p112（小問） | 那掉進海裡的飛機呢？ | 正確（提問） | — | 前句 p111 水槽測試機從艙口窗的角裂開；問句接回 p105 的「掉進海裡」，前提在 |
| p113（所長） | 其中一架，大部分的碎片從海裡撈了回來。 | 正確 | FAA Comet；Withey 1997 | FAA "By the end of August 1954, 70% of the Elba crash had been recovered"；拿坡里 "Very minimal wreckage of the Naples aircraft was able to be recovered due to the great depth"；Withey "about 70% of the aircraft was recovered"。「其中一架」「大部分」都照原文 |
| p114（所長） | 它最先裂的地方，在機頂兩個方方的天線窗。 | 正確 | FAA Comet；Withey 1997 | FAA "the aircraft's Automatic Direction Finder (ADF) windows, also squarish … on the very top of the fuselage … This piece of Elba wreckage, containing the two ADF windows and adjacent material bore the 'unmistakable fingerprint of fatigue,' and was determined to be the first fracture of the Elba crash."第一版的「那裡」拿掉了；FAA 講的是含兩個天線窗的那一塊，Withey 精確到「後面那個天線窗右後角的螺栓孔」，跟 p122 的螺栓孔一致，可以 |
| p115（所長） | 對撈回來的這一架，結論是：加壓機艙因金屬疲勞壞掉。 | 正確（只講厄爾巴島那架） | FAA Comet（引 RAE、MTCA） | RAE "We have formed the opinion that the accident at Elba was caused by structural failure of the pressure cabin, brought about by fatigue. … Owing to the absence of wreckage, we are unable to form a definite opinion on the cause of the accident near Naples"。「撈回來的這一架」＝p113 的「其中一架」＝厄爾巴島那架（拿坡里那架幾乎沒撈到），指涉明確；沒有說拿坡里那架同因，也沒有說不同因（RAE 說同一解釋 "appears to be applicable"），守住。25 字到上限 |
| p117（所長） | 有。做飛機的公司，拿一個機身， | 正確（數字見選修 S1） | FAA Comet | 前句 p116「造飛機時，沒有先測嗎？」。FAA "de Havilland went back and tested the same prototype fuselage with another 16,000 pressurization cycles"。拿掉「航空總署說」後，下一句的「一萬六千次」不再掛名，而 Withey 1997 寫的是前段艙段 "18,000 cycles"，見 S1 |
| p126（所長） | 對，還記得嗎？洞的旁邊，力也會擠。 | 正確（回呼） | Tuttle | 前句 p125「釘的孔，也是洞耶！」；回呼 p067–p074（"near holes"）。後句 p127 Withey 的看法 |
| p130（所長） | 還記得圓石頭旁邊的水嗎？角圓了，力也順多了， | 正確（回呼；比喻） | FAA Comet | 前句 p129「那幹嘛還要做圓角？」；回呼 p054–p055。FAA "flows freely around the curved edges with minimal build up"，「順多了」沒有說不擠 |
| p131（所長） | 裂縫就比較難冒出來。可是光靠形狀，還不夠。 | 正確（撰稿推論＋FAA 教訓） | FAA Comet Lessons Learned；UNSW Introduction | 「比較難」是 C10＋C17 的推論，有保留。「光靠形狀還不夠」＝"Detailed attention must be paid to aspects such as material choice, thickness, geometry, stress levels, maintenance, and usage."五項清單刪掉後，材料（p132–p141）、厚度（p143）、檢查（p155）接著一件一件講，前提沒有斷 |
| p132（小問） | 那換一種不會裂的材料？ | 正確（提問） | — | 接 p131「光靠形狀還不夠」，小孩的直覺問法；答案 p133–p141 沒有說有不會裂的材料 |
| p133（所長） | 材料真的有差。大學的材料教材，比過兩根棒子： | 正確 | UNSW Brittle／Ductile | 兩頁各一根有缺口的棒。後句 p134 銅棒與玻璃棒 |
| p135（所長） | 玻璃棒有了缺口，力小很多就斷了， | 正確（verify-1 S6 照改） | UNSW Brittle | "the force required to cause fracture is greatly reduced, and the rod breaks"。後句 p136「裂口就從缺口那裡開始」＝"Observe how the fracture originates from the notch." |
| p140（所長） | 對，它斷之前會先變形，吸收很多力氣。 | **需改**（見 F01） | UNSW Ductile | 後半句正確（"a lot of plastic deformation, and significant energy is absorbed before the fracture"）；問題在開頭的「對」確認了 p139 的「不怕缺口」 |
| p141（所長） | 所以材料要挑；可是挑好了，還是可能疲勞。 | 正確 | FAA Lessons Learned；UNSW Fatigue | "material choice"；"These materials are found to fail after a large number of applications of the stress even though the cyclic stress that is applied is below their yield strength."「可能」守住。回答 p132「不會裂的材料」：沒有這種材料。F01 改了以後接得更順 |
| p143（所長） | 那位學者寫到，後來窗戶周圍的金屬加厚了， | 正確 | Withey 1997 | "de Havilland subsequently redesigned the windows and increased the thickness of the skin in these areas to prevent this occurring on later Comet aircraft"。前句 p142「那彗星號後來怎麼改？」 |
| p144（所長） | 新的型號，也換了窗戶的設計，少打鉚釘。 | 正確 | Withey 2019 | "The Comet flew again as the Comet IV – Different window design to reduce riveting – Fewer manufacturing cracks" |
| p145（所長） | 有一款改良型，窗戶就改成了橢圓形。 | 正確（出處歸屬見選修 S2） | FAA Comet | "It wasn't until the next model, the Comet 1XB, that the window shape was changed from squarish to the now-conventional oval shape."只講彗星號，不說全業界改圓窗。拿掉「航空總署也說」後，聽起來像 p143 的「那位學者」也這樣寫；Withey 兩份都沒有講橢圓窗 |
| p148（所長） | 像是讓力，有別條路可以走， | 正確 | FAA Comet | "alternate load paths"；前句 p147「現在的設計，會先想好萬一裂了怎麼辦」＝damage tolerance。後句 p149「像小溪分成好幾條？」 |
| p150（所長） | 有點像。也要讓裂縫能停下來，或轉個方向。 | 正確 | FAA Comet | "provisions for cracks to be stopped and turned, should they occur"。「也」比「還」只是語氣 |
| p163（小問） | 力就像繞過圓石頭的水！ | 正確（verify-1 F03 已解決；小孩的總結） | FAA Comet（比喻） | 前句 p162「窗戶的角剪圓圓的，」。不再說「不會擠」，只回呼比喻；p058「也有點像這樣」已把比喻標成比喻。跟 p069「也會擠，最大約三倍」不衝突 |
| p164（小問） | 還有剛剛說的，要定期檢查！ | 正確（回呼；語境見選修 S3） | 14 CFR 25.571(a)(3) | "inspections or other procedures must be established … Instructions for Continued Airworthiness"；「定期」出自 p156 小問自己的「像定期去看牙醫」，前提在 |

## 三、刪句、彗星號與說明欄的檢查

### 刪掉的句子有沒有讓別句失去前提

| 刪掉的內容 | 會受影響的句子 | 結論 |
| --- | --- | --- |
| 舊 p045–p051 三層窗、中層小洞、外層撐壓差、中層接手 | p046「那窗戶也被推嗎？」、p047–p048、說明欄 | 沒問題。p047「會」直接回答 p046，再接手冊的「窗戶和門」。用 grep 查過 `video.json`、`script.md`、`build_scenes.py`：「三層」「中間那層」「最外層」「機長」都不在了；說明欄本來就沒講三層窗。Slate 已從 `sources` 拿掉，片中確實沒有一句用到它 |
| 舊 p052–p053「要看它多強」 | p048 | 沒問題，但結構強度沒念出來，見選修 S5 |
| 舊 p075「劍橋大學的教材說」與 p076 | p071、p073「剛剛那份講義說」 | 沒問題。p073 的「講義」指 p068 的「工程講義」（同一份 Tuttle），指涉清楚 |
| 舊 p135–p137 航空總署的教訓與五項清單 | p131、p165–p166 | 沒問題。p131「光靠形狀，還不夠」自己成立，後面依序講材料、厚度、做法、萬一有裂縫、檢查；p166「一整套設計和檢查」仍有前文 |
| 舊 p147「這只是這兩根的比較」 | p139–p141 | **有問題**：但書拿掉後，p140 又加了「對」，見 F01 |
| 各處拿掉的「航空總署說」「教材說」 | p031、p098、p117–p118、p145、p148 | 大多沒問題（同一段前面已掛名）。p118 的數字與 p145 的歸屬見選修 S1、S2 |

### 彗星號段落（p102–p145）

| 項目 | 結論 |
| --- | --- |
| 單一原因結論 | 沒有。p120「所以都是方窗害的！」由 p121「沒那麼簡單」推翻；p122 是 Withey 的觀察（"All the observed cracks … emanated from bolt or rivet holes near the cut-out areas"），p127 是「那位學者認為……可能」（"It was probably not the shape…"），p128「形狀、孔和做法，是連在一起的」，p130–p131 再說圓角有用但不夠；FAA 的方窗角應力集中（p058–p061）也保留 |
| 疲勞結論只對厄爾巴島那架 | 正確。p105 兩架掉進海裡 → p112 小問問海裡的飛機 → p113「其中一架，大部分的碎片從海裡撈了回來」→ p114 最先裂在機頂天線窗 → p115「對撈回來的這一架，結論是……」。片中沒有念「厄爾巴島」，但「撈回來的這一架」只可能是厄爾巴島外海那架（FAA：Elba 撈回 70%，Naples "Very minimal wreckage"）；說明欄寫明「厄爾巴島外海那一架」，兩者一致 |
| 業界改圓窗 | 沒有說。p143–p145 只講彗星號自己的改法 |
| 畫面 | `kid-sea-q`、`chief-adf`、`chief-comet` 都是人物鏡頭，沒有事故或殘骸畫面 |

### YouTube 說明欄、標題、標籤、縮圖、參考資料

| 項目 | 結論 | 依據 |
| --- | --- | --- |
| 標題「飛機窗戶的圓角，怎麼改變機身受力？｜原來如此事務所」 | 正確 | 同 verify-1 |
| 說明第 1 段（故事設定） | 正確 | 硬紙飛機、方窗、從角裂開、「她帶著它跑來事務所」對應 p001–p008；「去找外婆」已刪（verify-1 S8）。「捲了一架」台詞沒說，但圖 `tube-tear`、`kid-main-q` 畫的是捲起來的紙機身，可以 |
| 說明第 2 段 | 正確，跟現行片子一致 | 稀薄空氣、加壓、撐一下鬆一下（p024–p045）；力繞過洞（p050–p052，不再說「推力」）；小溪（p054–p061）；應力集中（p064）；金屬疲勞（p084–p085）；「調查對厄爾巴島外海那一架的結論」（p113–p115，verify-1 F07 照改）；學者指出鉚釘孔、螺栓孔、「窗戶怎麼固定也很要緊，不能只怪窗角」（p121–p128，說明欄的「也很要緊」比片中的「可能比形狀還要緊」更保守，可以）；材料、厚度、怎麼做、萬一有裂縫、定期檢查（p132–p157）。沒有任何已刪掉的內容（三層窗、機長、五項清單） |
| 說明第 3 段（AI 示意插圖、沒有事故畫面） | 正確 | 飛機、窗戶、水槽、小溪都還在片中 |
| 標籤（飛機、飛機窗戶、圓角、應力集中、金屬疲勞、加壓、彗星號、科普、原來如此事務所） | 正確 | 每一個都還在片中講到 |
| 縮圖「飛機窗戶／為何圓角？」「方角會讓力擠在一起」，鏡頭 `kid-main-q` | 正確 | p061；`kid-main-q` 仍是現行鏡頭 |
| 參考資料（`sources` 13 筆） | 正確 | 13 筆片中都還用到：PHAK（p022–p048）、FAA Comet（p058–p061、p096、p103–p119、p145–p150）、Tuttle（p068–p074、p126）、DoITPoMS（p071）、UNSW Introduction（p096、p131）、Fatigue（p084–p099、p141）、Fracture mechanics（p052、p100–p101）、Fracture toughness（p100–p101 的背景）、Brittle（p135–p136）、Ductile（p138–p140）、Withey 1997（p121–p128、p143）、Withey 2019（p144）、25.571（p152–p155）。Slate 已移除，正確；NTSB 與 25.775 沒加進來也正確（三層窗不在片中） |

## 四、claims.md 的同步

C01–C29 的「可用說法」行號逐條對過現行台詞，大致對得上（C01 p021–p023、C09 p046–p049、C10 p050–p052／p058–p061、C12 p067–p069、C13 p070–p071、C20 p107–p115、C21 p116–p119、C24 p132–p141、C25 p142–p145、C27 p151–p157／p164、C28 p130／p149／p163 等都對）。要改的 4 處見 F02。本報告依指示只寫 verify-2.md，`claims.md` 沒有改。

## 建議修改

必改：

1. F01 p140（所長）：「對，它斷之前會先變形，吸收很多力氣。」 → 「拉一次是這樣：它斷之前會先變形，吸收很多力氣。」（23 字）
   （前句 p139「銅會彎，所以不怕缺口？」得到「只限拉一次」的回答；後句 p141「所以材料要挑；可是挑好了，還是可能疲勞。」變成「拉一次不怕，拉很多次還是可能疲勞」，正好接回金屬疲勞的主線。圖 `chief-energy` 不用改。）
2. F02 `claims.md` 同步（不是台詞，沒有字數限制）：
   - 文首第 11 行「Slate 專欄（作者是航空公司機長）引……三層窗說明（[14]）」：Slate 第二版沒用，而且「機長」正是 verify-1 F01 指出的錯；改成「……14 CFR 25.571（[13]）。三層窗整段第二版未使用（C08）」或刪掉 Slate 那半句。
   - 來源清單第 39 行「[14] Mark Vanhoenacker（航空公司機長）」→「（民航機飛行員，文中自稱 airline pilot；第二版未使用）」。
   - C02 注意欄「p022 小問問『外面的空氣』」→「p024 小問問」（現行 p022 是所長的手冊句）。
   - C24 注意欄配合 F01：寫明 p140「拉一次是這樣」限定在一次施力（[10] 只講一次施力），疲勞時缺口仍然要緊（[6]、C17）。C10 標題的「力轉不過去」也可順手改成 p061 現行的「力轉得太急」。

選修（不影響本輪結論）：

- S1 p118「一萬六千次」：第一版掛在「航空總署說」底下（verify-1 S7 因此可留），第二版拿掉掛名後變成平鋪直敘，而 FAA 寫 prototype 16,000 次、Withey 1997 寫前段艙段 "18,000 cycles"。改成兩個來源都涵蓋的說法：「測過一萬多次。可是它之前被加過兩倍的壓力，」（21 字）。
- S2 p145 出處歸屬：p143–p144 是「那位學者」（Withey），p145 的 Comet 1XB 橢圓窗其實出自 FAA。要分清楚可改「航空總署也提到，有一款改良型改成橢圓窗。」（20 字）。不改也不算錯。
- S3 p164「還有剛剛說的，要定期檢查！」：前句是在回答「我的紙飛機要怎麼剪」，拿掉「真的飛機」後，聽起來像紙飛機也要定期檢查。可改「真的飛機，還要定期檢查！」（12 字；「定期」仍回呼 p156 的看牙醫）。
- S4 p051 的依據：`claims.md` C10 把「外面那層金屬被拉得緊緊的」記成常識白話；Withey 1997（"a biaxial tensile stress field may be closer to reality" for the Comet skin）與 Withey 2019（"The hoop stress can be calculated – 128 MPa for the general skin"）可補成來源。台詞不用改。
- S5 p047–p048 拿掉「要看它多強」：手冊原句先講 structural strength，再講 often 窗戶和門。現在聽起來像壓差上限主要看窗戶和門。要補回可改 p048「看它多強，也常看窗戶和門這些地方。」（17 字）。不改也不算錯，「常」已保留。
- S6 紙條示範仍未實測：`claims.md` C15 的實測紀錄寫「尚未實測（2026-11-13）」。verify-1 F05 的台詞改了，但條件是開拍前照「兩條紙一樣寬、兩個洞一樣寬」實拉三次以上並記錄；結果不同就改 p075–p078 與 `strips-pull`。這不是台詞錯，是開拍前的前提，提醒一下。
