# 查核報告 1（sothatswhy-p18-pencil-diamond）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-09
- 方法：逐句讀 `video.json` 的 230 句台詞（p001–p230），加上 YouTube 標題、說明與縮圖文字（headline「都是碳／差在哪？」、sub「鉛筆芯和鑽石」）。對照 `claims.md` 的 C01–C23，但不採用它的引文，每個來源都重新打開讀原文：
  - USGS PP1802-J（Graphite）：用 curl 下載 `https://pubs.usgs.gov/pp/1802/j/pp1802j.pdf`，`pdftotext` 讀 Abstract、Introduction、Uses、Mineralogy、表 J2、圖 J1。注意：`claims.md` 來源 1 寫的網址 `pp1812j.pdf` 會回 USGS 的 Page Not Found，正確檔名是 `pp1802j.pdf`。
  - USGS *Gemstones*（Mineral Gemstones，curl 讀全文）；*Handbook of Mineralogy* 的 Graphite 條（curl 下載 PDF 讀）；Webmineral Graphite（curl 讀）。
  - Chemistry LibreTexts 兩頁（Covalent Network Solids；Tro 13.7）；Geosciences LibreTexts《GEOS: A Physical Geology Lab Manual》3.02 硬度活動（指甲、玻璃的硬度值）。
  - GIA 五頁：Diamond Care and Cleaning Guide、More than the Mohs Scale、Digging into Diamond Types、Gems & Gemology 2018 夏季號〈Natural-Color Blue, Gray, and Violet Diamonds〉、〈Blue Diamonds Have Surprise Origin〉；另讀 GIA Jade Description 與 IGS〈Jade Toughness and Care〉（預覽）。
  - Bradt, Newnham & Biggers (1973) "The Toughness of Jade", *American Mineralogist* 58: 727–732（minsocam.org PDF 全文，curl 下載後讀摘要、表 1、表 2 與內文）。
  - Science Museum Group〈Graphite circuits〉；STAEDTLER 加拿大產品頁；University of Iowa Libraries 工程分館部落格〈pencil〉文（Conté 與石墨黏土比例，作為 STAEDTLER 之外的獨立來源）；美國專利 US2986472A "Pencil clays"（筆芯用的黏土種類）。
  - Wikipedia Graphite、Diamond（raw wikitext，只用來找二級文獻與交叉比對，結論不只靠它）。
- 打不開／沒讀到原文的：Windows to the Universe 硬度頁與 RSC 碳元素頁（curl 403，改用 LibreTexts 地質實驗手冊）；Mindat Graphite（403，改用 *Handbook of Mineralogy* 與 Webmineral）；ACS C&EN〈Pencils & Pencil Lead〉（403）、Argonne「Ask A Scientist」鉛筆頁（503）、Notre Dame 硬度講義（回 HTML 錯誤頁），改用 University of Iowa 部落格與專利；Bradt 1973 的 studylib／anyflip 轉載（429／403），已改讀 minsocam 原 PDF；Ramaseshan (1946) "The cleavage properties of diamond"（Springer 要登入、IAS 典藏回 404），只從搜尋結果讀到摘要轉述，只當輔助，不當主要依據。
- 結論統計（台詞 230 句）：正確 228、需改 2、錯誤 0。另外標題、說明、縮圖 3 項：正確 2、需改 1。

## 一、需改的地方與理由

| # | 行 | 原句 | 結論 | 理由與讀到的原文 |
| --- | --- | --- | --- | --- |
| F01 | p146（所長） | 他們說，鑽石裡有幾個方向，碳跟碳離得比較遠， | 需改（簡化會誤導，跟本集模型打架） | GIA Care Guide 原文："Diamonds are tougher in the directions where the atoms are bonded tightly together." "The weakest directions are the ones where the atoms are farthest apart." "It's easier to break a diamond in those directions, which are called cleavage directions." GIA 說的「離得最遠」指的是原子面（{111} 面）之間的間距，不是哪一根 C–C 鍵比較長；鑽石裡每一根鍵都一樣長。片中 p083–p087 剛教小朋友「每顆球四隻手全部牽滿、伸向四個方向」，木棍都一樣，這時聽到「碳跟碳離得比較遠」，最自然的理解是有些木棍比較長，這是錯的。GIA 同頁的另一句「bonded tightly together」的方向較牢，正好可以用模型的語言說成「那幾個方向，跨過去牽著的手比較少」（Ramaseshan 1946 的摘要轉述也說，沿寬間距 {111} 面切開時每單位面積要切斷的鍵大約只有窄間距面的三分之一；這篇只讀到轉述，只當輔助）。改成模型講得通的說法，p147「順著那些方向，就比較容易裂開。」照留 |
| F02 | p195（所長） | 量出來，沿著層走，大約比穿過層，好走上百倍。 | 需改（數量級偏低） | USGS PP1802-J 表 J2：Electrical resistivity (Ω-cm×10⁴) "a axis: 1 to 100"、"c axis: 10,000"，也就是沿層比穿層好導電 100 到 10,000 倍，一百倍是**最低**的那一端。Wikipedia Graphite（引 Pierson《Handbook of Carbon, Graphite, Diamond and Fullerenes》）："Electrical conductivity perpendicular to the layers is consequently about 1000 times lower." 「大約……上百倍」會讓人記成「大概一百倍」，實際常見的是上千倍。`claims.md` C20 說取保守值，但「大約」把下限說成了典型值。改成涵蓋兩個來源的範圍，去掉「大約」 |
| F03 | 縮圖 headline | 都是碳／差在哪？（sub：鉛筆芯和鑽石） | 需改（跟片中說法打架） | 片中 p019–p025 明說筆芯是石墨和黏土「兩樣東西混在一起」；USGS："graphite (mixed with clay) for the "lead" in pencils"；Science Museum Group："Pencil 'lead' is made of graphite mixed with clay."；US2986472A："The main ingredients in pencil lead are clay and graphite"，硬芯黏土可高到 "70%"。縮圖把「鉛筆芯」和「都是碳」擺在一起，跟片中第一章自己打架。YouTube 標題已經用「都含碳」，縮圖改成一致即可 |

## 二、逐段核對（正確的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p003 | 畫糊了、手黑黑的 | 正確 | — | 開場情境 |
| p004–p005 | 手上那層大部分是筆芯磨下來的 | 正確 | LibreTexts Covalent Network Solids | "When you use a pencil, sheets are rubbed off and stick to the paper."「大部分」交代了筆芯還有黏土 |
| p006 | 筆芯怎麼這麼容易掉 | 正確 | — | 問題句，答案在 p101–p109 |
| p007–p008 | 黑黑的東西跟鑽石都是碳組成 | 正確（附註） | USGS PP1802-J；USGS Gemstones | "Graphite, which is a soft form of elemental carbon"；"Diamond (hardness: 10 Mohs) Carbon"。附註：黑的那一部分是石墨，黏土本身不黑（p024「土自己寫不黑」）；第一章緊接著交代混合物，可留 |
| p009–p012 | 不可能（錯猜）；跟鑽石是親戚 | 正確 | 同上 | 「親戚」是比喻 |
| p013 | 最硬的鑽石也有怕的東西 | 正確 | GIA Care Guide | 回收在 p143–p153："a hard blow can still cleave a diamond" |
| p014 | 鉛筆線能做到一件鑽石做不到的事 | 正確（附註） | LibreTexts；GIA Diamond Types | 指導電。附註：藍色 IIb 鑽石會導電，片中 p184–p188 用「一般的鑽石」「很少見」收回，前面的預告可留 |
| p015–p017 | 跟著鉛筆查到鑽石；全片問題 | 正確 | — | 問題句 |
| p018–p022 | 筆芯是兩樣東西：石墨和黏土；「可以捏陶的那種土」 | 正確（附註） | USGS；Science Museum Group；US2986472A | "the long use of graphite (mixed with clay) for the "lead" in pencils"；"Pencil 'lead' is made of graphite mixed with clay."。專利寫筆芯用 "Georgia kaolin of ultrafine particle size" 與鈣、鎂膨潤土。高嶺土（kaolin）就是做瓷器的土，「可以捏陶的那種土」對兒童是可以接受的說法，不必改成「很細的土」 |
| p023–p025 | 土自己寫不黑；黏土把石墨黏成一根，有形狀、比較牢 | 正確 | STAEDTLER；US2986472A | "The clay acts as a binding agent and gives the lead its shape and strength, while graphite produces the characteristic silvery black color on the page." 製造商說法與專利一致 |
| p026–p031 | 有的筆特別黑特別軟；石墨多；黏土越多越硬、線越淡 | 正確 | STAEDTLER；Science Museum Group；University of Iowa Libraries 部落格；US2986472A | "The more clay in the pencil lead, the harder the pencil." "The more graphite … the softer and blacker"；"Softer pencils, such as a 4B, have a greater graphite-to-clay ratio than harder pencils, such as a 4H."；Iowa："By varying the ratio of graphite to clay, Conté discovered that he could manufacture a pencil for a specific hardness"、"No.1 is the softest graphite and leaves a darker, smudgier mark, and No.3 pencils leave a fainter mark."；專利 "clay percentages as high as 70% … resulted in a pencil of 9H hardness"。獨立來源已補上 |
| p032–p034 | 黑黑的是石墨，石墨由碳組成 | 正確 | USGS | 同 p007 |
| p035–p036 | 摸起來滑；有點滑、帶一點金屬亮光 | 正確 | USGS PP1802-J；*Handbook of Mineralogy* | "Well-crystallized graphite flakes have a black metallic luster"；"a greasy feel, and self-lubricating properties"；HoM "Greasy feel"、"Luster: Metallic" |
| p037 | 混進黏土做筆芯，已經用了很久 | 正確 | USGS；University of Iowa | "the long use of graphite (mixed with clay)"；"Conté's 1795 patent is the basic process for manufacturing pencils today."（兩百多年） |
| p038–p043 | 鑽石是別的東西（錯猜）；鑽石幾乎全部都是碳 | 正確 | USGS Gemstones；GIA Diamond Types | "Carbon"；GIA "trace elements, such as nitrogen or boron"，「幾乎」恰當 |
| p044–p048 | 碳就是碳，一顆一顆比一模一樣；成分 | 正確（附註） | USGS | "Graphite is one of four forms of crystalline elemental carbon"。附註：碳有碳-12、碳-13 等同位素，兩種材料裡都有，「一模一樣」是「同一種原子」的兒童說法，可接受 |
| p049–p052 | 差在怎麼排、怎麼牽手 | 正確 | LibreTexts | 同素異形體的兒童說法 |
| p053–p057 | 積木：木球是碳、木棍是牽著的手 | 正確 | — | 比喻；p092–p095 有交代是模型 |
| p058–p060 | 猜鑽石的碳擠得比較緊；是真的 | 正確（附註） | USGS；*Handbook of Mineralogy*；USGS Gemstones | 以密度看成立（見 p117–p118）。附註：同一層裡石墨的 C–C 距離（1.415–1.42 Å）其實比鑽石短；「擠得緊」說的是整體每單位體積的碳比較多，片中後面也只拿密度驗證，可留 |
| p061–p062 | 每顆碳最多牽四隻手 | 正確 | LibreTexts | "In diamond, each carbon shares electrons with four other carbon atoms - forming four single bonds." |
| p063–p064 | 石墨每顆球牽三顆、在同一平面、一張平網 | 正確 | LibreTexts Tro 13.7；USGS 圖 J1 | "bonded to three others"；"Each carbon atom within a sheet is connected to its three nearest neighbors by covalent bonds" |
| p065–p068 | 空著一隻手；等一下回來看 | 正確（附註，簡化） | LibreTexts | "These "spare" electrons in each carbon atom become delocalized over the whole of the sheet"。真實情形是第四個電子離域成整層共有，不是一隻「空手」；但 LibreTexts 自己就叫它 "spare" electron，片中 p092–p095 又明說模型的限度，對兒童可以接受 |
| p069–p070 | 一張網很牢，石墨是很多張網疊起來 | 正確 | USGS | "The intraplanar (a axis) covalent bonding in graphite sheets is strong"；"parallel-stacked … planar honeycomb-lattice sheets" |
| p071–p075 | 層間沒有木棍，只靠很弱的力；離得比較遠，約網內兩球距離的兩倍多 | 正確 | USGS 圖 J1；LibreTexts | 鍵長 "1.415 angstroms"、層距 "3.354 Å"（約 2.37 倍），層間 "weak intermolecular van der Waals' forces"；LibreTexts "The distance between the layers is about 2.5 times the distance between the atoms within each layer." 「兩倍多」兩來源都對得上 |
| p076–p082 | 離遠會怎樣；軟的地方在層與層之間 | 正確 | USGS | "the electrostatic interlayer (c axis) forces holding the sheets together are weak" |
| p083–p091 | 鑽石四隻手全牽滿、伸向四個方向；一隻空手都沒有；攀爬架 | 正確 | LibreTexts Tro 13.7 | "each bonded to four other carbon atoms in a tetrahedral array to create a giant network"。攀爬架是比喻 |
| p092–p098 | 這只是模型；拿來猜，再去量，猜對才算數 | 正確 | — | 方法說明；p097 用「我覺得」標成意見 |
| p099–p104 | 推石墨：層間輕輕吸住、離得遠，一推整片滑開 | 正確 | USGS；LibreTexts | "allows them to slide across one another easily"；"the layers can easily slide past one another because of the weak interlayer interactions" |
| p105–p106 | 寫字：紙面粗，筆芯一磨，外面幾層滑下來留成黑線 | 正確 | LibreTexts | "the friction between graphite and a piece of paper is sufficient to leave a thin layer of carbon on the paper" |
| p107–p109 | 手一擦，薄薄的石墨又滑到手上，畫就糊了 | 正確（附註） | LibreTexts；University of Iowa | 同一機制的推論；Iowa 寫軟芯留下 "darker, smudgier mark"，與日常觀察一致。可接受的兒童說法 |
| p110–p113 | 石墨粉吹進卡卡的鎖裡，鎖變順 | 正確 | LibreTexts；Wikipedia Graphite | "used in pencils and as a dry lubricant for things like locks"；Wikipedia "to lubricate locks … It can be used as a dry powder"。「吹進」是一般做法的描述 |
| p114–p116 | 模型猜：疊網中間空隙大，同樣大小石墨比較輕 | 正確 | LibreTexts | "Graphite has a lower density than diamond." "This is because of the relatively large amount of space that is "wasted" between the sheets." 不只是撰稿推論，教科書也這樣解釋 |
| p117–p118 | 量出來，同樣大小的鑽石約比石墨重一半多 | 正確 | USGS PP1802-J；*Handbook of Mineralogy*；USGS Gemstones | 石墨 "2.09 to 2.26 grams per cubic centimeter"、HoM "D(calc.) = 2.26"；鑽石 "Specific gravity: 3.51"。3.51÷2.26≈1.55、3.51÷2.09≈1.68，「重了一半多」正確 |
| p119–p122 | 鑽石每顆四面八方牽住，沒有一層能滑開；刮一點要扯斷很多牢的手 | 正確 | LibreTexts | "very hard. This is again due to the need to break very strong covalent bonds operating in 3-dimensions." |
| p123–p124 | 石墨只要讓一層滑開，網裡的手一隻都不用斷 | 正確（附註，簡化） | USGS | "The ratio of force required to induce gliding of graphite sheets relative to compression force is low"。真實磨損時薄片邊緣也會斷一些鍵，「一隻都不用斷」是模型層次的說法；對比的重點（石墨不必斷強鍵、鑽石必須）正確，可留 |
| p125–p126 | 科學家說的硬就是不容易被刮傷 | 正確 | USGS Gemstones；GIA 4Cs | "Hardness of a gemstone is its resistance to scratching"；"based on the relative ease or difficulty with which one can be scratched by another"（礦物學的硬度；材料科學另有壓痕硬度，對兒童不必提） |
| p127–p128 | 誰刮得傷誰就比較硬，從一排到十 | 正確 | USGS Gemstones；GIA 4Cs | "Talc is 1 … Diamond is 10"；"a scale of 1 (least hard – talc) to 10 (hardest of all – diamond)" |
| p129 | 石墨大約一到二，用指甲就刮得動 | 正確（附註） | *Handbook of Mineralogy*；Webmineral；USGS PP1802-J；LibreTexts 地質實驗手冊 | HoM "Hardness = 1–2"；Webmineral "Hardness: 1.5-2"；USGS 正文 "a hardness of 1 to 2 on the Mohs scale and is thus extremely soft"，但同一份文件的 Mineralogy 段落與表 J2 寫 "0.5 to 1"（USGS 自己有兩種寫法）。兩本礦物手冊都給 1–2，「大約一到二」可留。指甲：LibreTexts 實驗手冊表 3.1 "2.5 - fingernail"，並寫 "if your fingernail scratches your sample … a hardness value of less than 2.5"。石墨不論取 0.5–1 或 1–2 都低於 2.5，「指甲刮得動」成立 |
| p130–p131 | 鑽石最上面的十；只有鑽石刮得動鑽石 | 正確 | GIA Care Guide | "Diamond rates highest on the Mohs hardness scale, at number 10."；"Only a diamond can scratch a diamond." |
| p132–p133 | 鑽石在戒指上鬆了，會把抓住它的金屬慢慢磨掉 | 正確 | GIA Care Guide | "diamond can also scratch any of the precious metals used for settings"；"a diamond that's loose in its setting can wear through a prong over time" |
| p134–p139 | 最硬一定打不破（錯猜）；硬和不容易碎是兩回事；耐敲是被重重敲一下會不會裂 | 正確 | GIA 4Cs；GIA Care Guide | "Diamond is the hardest gemstone, but not necessarily the toughest."；"Toughness is a measure of how well a gem can survive an impact and resist breaking, chipping, or cracking." |
| p140–p142 | 玻璃杯：指甲刮不出痕跡，掉地上卻可能摔碎 | 正確 | LibreTexts 地質實驗手冊 | 表 3.1 "5.5 - Glass plate or knife blade" 高於 "2.5 - fingernail"，所以指甲刮不動玻璃；摔碎是常識 |
| p143–p145 | 研究寶石的機構說，鑽石被重敲還是可能裂開或缺角 | 正確 | GIA 4Cs；GIA Care Guide | "diamonds can be cleaved or fractured by a hard blow"；"even after cutting, a hard blow can still cleave a diamond" |
| p146 | 碳跟碳離得比較遠 | 見 F01 | — | — |
| p147 | 順著那些方向就比較容易裂開 | 正確 | GIA Care Guide | "It's easier to break a diamond in those directions, which are called cleavage directions." |
| p148 | 切鑽石的人有時順著這種方向故意敲開 | 正確 | GIA Care Guide；Wikipedia Diamond | "A cutter can cleave a diamond by hitting it sharply in the cleavage direction."；"Diamond cutters use this attribute to cleave some stones before faceting them."「有時」恰當（現在多用鋸或雷射） |
| p149–p153 | 別以為敲不碎；小心別撞；尖角要好好保護才不會缺角 | 正確 | GIA Care Guide | "Cutting styles with pointed corners or ends are often set with prongs to protect the corners from chipping." |
| p154–p158 | 有一種玉比鑽石軟得多，卻比鑽石難敲碎很多 | 正確（附註） | GIA 4Cs；Bradt et al. 1973；USGS Gemstones；GIA Jade | GIA："Values range from 225,000 for nephrite and 120,000 for jadeite"、鑽石 "5,000 along the stone's cleavage planes to over 8,000"，並說明 "The toughness scale measures the work required to separate two surfaces of a crystal along a certain crystallographic plane"。GIA 沒寫單位，但軟玉 225,000 這個數字出自 Bradt 1973："about 120,000 ergs/cm² for jadeite and 225,000 ergs/cm² for nephrite"（斷裂表面能，單位 erg/cm²），作者並寫 "jade is about an order of magnitude tougher than most ceramic materials"、"Jadeite is the harder of the two minerals, but nephrite is the tougher and the stronger"。照 GIA 的同一把尺，軟玉約為鑽石的三十倍上下。附註：若改用斷裂韌性（K_IC），Bradt 給軟玉 77×10⁷ dyne·cm⁻³ᐟ²（≈7.7 MPa·m½），差距會縮小到一兩倍，但仍是軟玉較韌；片中不念數字、只說「難上很多」，方向正確，可留。硬度：USGS "Jade (hardness: 6 Mohs) Nephrite"，對鑽石 10，「軟得多」正確 |
| p159–p164 | 硬和耐敲是兩回事；回收鉛筆線能做到的事 | 正確 | 同前 | — |
| p165–p166 | 軟一點的鉛筆，用力畫又粗又黑不斷的線，接電池和小燈 | 正確（附註） | Science Museum Group | "Make sure you draw one continuous line, and press quite hard to make the lines thick."；用 4B 或 6B、9V 電池、LED。「兩頭接上」是接法的簡化 |
| p167–p170 | 鉛筆不是金屬（錯猜）；科學博物館教這個實驗，燈真的亮了 | 正確 | Science Museum Group | "You should see the LED light up." |
| p171–p175 | 為什麼石墨可以；電流可以想成帶電的小東西往前跑，叫電子 | 正確 | Science Museum Group | "the carbon atoms' electrons can move within the material"；兒童說法 |
| p176–p180 | 空著的手讓一個電子能沿整張網跑；鉛筆線是電子的路 | 正確（附註，簡化） | LibreTexts；USGS | "The delocalized electrons are free to move throughout the sheets."；USGS "These delocalized interlayer electrons also give graphite its high electrical and thermal conductivity." 「空著的手」見 p065 附註 |
| p181–p184 | 鑽石四隻手牽滿，電子被牢牢抓住；一般的鑽石幾乎不導電 | 正確 | LibreTexts；Wikipedia Diamond | "doesn't conduct electricity. All the electrons are held tightly between the atoms, and aren't free to move."；"most diamonds, which are excellent electrical insulators" |
| p185–p188 | 很少見的藍色鑽石混了一點別的東西，會導一點電；非常少見 | 正確 | GIA Diamond Types；GIA G&G 2018；GIA Blue Diamonds Origin | "Type IIb: These diamonds are known to conduct electricity. The trace element boron is responsible for most diamonds that are blue or grayish blue in color."；"boron was unambiguously identified as the natural dopant causing the observed color and semi-conductivity"；"the (extremely rare) geological conditions that produce natural type IIb diamonds"；"Type IIb diamonds are a rare variety of diamond"。片中說「有一種」藍鑽，沒說所有藍鑽都導電（G&G：硼只佔 GIA 所見天然藍鑽的一半多），恰當。GIA 頁面都沒有給 IIb 的百分比，片中也不念數字 |
| p189–p190 | 有人說碳會導電，問他是哪一種排法 | 正確 | 同前 | 收束句 |
| p191–p194 | 沿著網很順，跳到下一層難多了 | 正確 | LibreTexts；USGS 表 J2 | "its electrical conductivity is very high parallel to the planes of carbon atoms"；a 軸對 c 軸電阻率見 F02 |
| p195 | 大約好走上百倍 | 見 F02 | — | — |
| p196–p199 | 線畫很長燈還亮嗎；博物館說石墨只是還不錯的導電材料，線越長電越難走，燈越暗 | 正確 | Science Museum Group | "Graphite is only a fairly good conductor, and longer circuits have more resistance to current flow." "That's why touching the crocodile clip at different points along the line can make the LED brighter or dimmer." |
| p200–p202 | 比比看軟硬鉛筆；「我猜是軟的那支，因為石墨比較多。不過要量了才算。」 | 正確（意見已標明） | Science Museum Group；STAEDTLER | 博物館把 "What happens if you make the drawing with harder (eg 4H) or softer (eg 6B) pencils?" 留成開放題。台詞用「我猜」開頭、「要量了才算」收尾，猜測與理由（石墨比較多，有來源）分得清楚，小朋友不會聽成定論 |
| p203–p204 | 只能用小電池，插座絕對不要拿來玩 | 正確 | Science Museum Group | 實驗用 9V 電池；安全提醒，不當查核主張 |
| p205–p219 | 排法一換性質跟著變；小問總結；所長意見「我覺得這是材料最有意思的地方」；同一盒積木兩種搭法 | 正確 | 同前 | 與已核說法一致；意見句有「我覺得」 |
| p220–p226 | 畫以後還會糊；一黑一淡各塗一小塊擦擦看 | 正確 | University of Iowa | 觀察題，片中不給答案；軟芯 "smudgier" 與題目方向一致 |
| p227–p230 | 片尾 | 正確 | — | — |
| YouTube 標題 | 都含碳，鉛筆芯和鑽石怎麼差這麼多？ | 正確 | USGS | 「含」碳，正確交代筆芯還有黏土 |
| YouTube 說明 | 石墨和黏土；平網與攀爬架；滑、硬、打不打得破、導電；插圖與積木是示意、數字是大約、只用小電池 | 正確 | 同前 | 「一個最難刮傷」對上 GIA "Only a diamond can scratch a diamond"；模型限度與安全都有交代 |
| 縮圖 | 都是碳／差在哪？／鉛筆芯和鑽石 | 見 F03 | — | — |

## 三、撰稿者標出的疑點

| 項目 | 結論 |
| --- | --- |
| 1. 指甲約 2.5、玻璃約 5.5 | 正確。LibreTexts 地質實驗手冊表 3.1："2.5 - fingernail"、"5.5 - Glass plate or knife blade"。p129、p140 可留 |
| 2. 石墨硬度一到二或 0.5–1 | USGS PP1802-J 自己兩種寫法都有（正文 1–2；Mineralogy 段落與表 J2 0.5–1）。*Handbook of Mineralogy* 1–2、Webmineral 1.5–2。「大約一到二」可留，兩種數字都低於指甲 |
| 3. 軟玉比鑽石難敲碎得多 | 正確（附註）。GIA 數字的單位查到了：出自 Bradt 1973 的斷裂表面能，erg/cm²；照這把尺約三十倍。改用斷裂韌性差距較小，但方向不變。「難上很多」可留 |
| 4. 藍鑽（IIb，含硼）導電、少見 | 正確。GIA 三頁都說 rare／extremely rare；台詞只說「有一種」 |
| 5. 筆芯＝石墨＋黏土；黏土越多越硬越淡 | 正確。獨立來源：Science Museum Group（4B 對 4H）、University of Iowa（比例決定硬度、軟芯較黑較易糊、硬芯較淡）、US2986472A（黏土到 70% 為 9H） |
| 6. 密度 | 正確。3.51÷2.26≈1.55，「重了一半多」；LibreTexts 也用層間空隙解釋密度低 |
| 7. 沿層導電好上百倍 | 需改（F02）。USGS 範圍 100–10,000 倍，Pierson 約 1000 倍；「大約上百倍」把下限說成典型值 |
| 8. 鑽石沿特定方向劈開；切割者順著敲開 | 正確（p147、p148）；p146 的說法需改（F01） |
| 9a. 「空著的手＝能跑的電子」 | 可接受。LibreTexts 用 "spare" electrons；p092–p095 交代了模型限度 |
| 9b. 碳原子「一模一樣」 | 可接受。同位素差異對本集無關 |
| 9c. 「可以捏陶的那種土」 | 可接受，甚至比「很細的土」準：筆芯常用高嶺土（瓷土）與膨潤土（US2986472A） |
| 9d. 石墨滑到手上 | 可接受，同一機制的推論，符合日常觀察 |
| 9e. 「碳跟碳離得比較遠」的劈開方向 | 會誤導（F01）。跟本集「每根木棍一樣」的模型打架；改成「跨過去牽著的手比較少」 |
| 10. 所長猜軟鉛筆燈比較亮 | 正確，p201 以「我猜」開頭、「要量了才算」結尾，清楚標成猜測 |

## 建議修改

必改（F01–F03）：

- p146：他們說，鑽石裡有幾個方向，碳跟碳離得比較遠， → 他們說，鑽石裡有幾個方向，跨過去牽著的手比較少，（22 字；p147 照留。若 `cameras.json` 或插圖提示詞 `chief-weak-way`／`cleave-line` 畫了「拉長的木棍」，一起改）
- p195：量出來，沿著層走，大約比穿過層，好走上百倍。 → 量出來，沿著層走，比穿過層好走幾百到上千倍。（22 字）
- 縮圖 headline：都是碳／**差在哪？** → 都含碳／**差在哪？**（與標題一致；sub「鉛筆芯和鑽石」照留）

選修（不影響本輪結論）：

- （給 `claims.md` 的維護者）來源 1 的網址改成 `https://pubs.usgs.gov/pp/1802/j/pp1802j.pdf`（現寫的 `pp1812j.pdf` 會 404）；C13 補記 USGS 同一份文件的 Mineralogy 段落也寫 "softness (0.5 to 1 on the Mohs scale)"，並補上 *Handbook of Mineralogy*「Hardness = 1–2」；C13／C15 的指甲、玻璃改引 LibreTexts 地質實驗手冊；C17 補記 GIA 數字出自 Bradt 1973，單位 erg/cm²；C11 補記 LibreTexts 的 "wasted space between the sheets"；C02／C03 補 University of Iowa 與 US2986472A 作為非製造商來源；C20 的倍數依 F02 更新。

## 來源

只列查核者這次實際打開並讀到原文的頁面。

```json
[
  {"title": "Robinson, Hammarstrom & Olson (2017), Graphite, USGS Professional Paper 1802-J（PDF 全文）", "url": "https://pubs.usgs.gov/pp/1802/j/pp1802j.pdf", "checked_on": "2026-11-09"},
  {"title": "USGS, Gemstones: Mineral Gemstones", "url": "https://pubs.usgs.gov/gip/gemstones/mineral.html", "checked_on": "2026-11-09"},
  {"title": "Handbook of Mineralogy, Graphite（Mineralogical Society of America，PDF）", "url": "https://www.handbookofmineralogy.org/pdfs/graphite.pdf", "checked_on": "2026-11-09"},
  {"title": "Webmineral, Graphite Mineral Data", "url": "https://webmineral.com/data/Graphite.shtml", "checked_on": "2026-11-09"},
  {"title": "Chemistry LibreTexts, Covalent Network Solids", "url": "https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Supplemental_Modules_and_Websites_(Inorganic_Chemistry)/Crystal_Lattices/Lattice_Basics/Covalent_Network_Solids", "checked_on": "2026-11-09"},
  {"title": "Chemistry LibreTexts, 13.7 Network Covalent Atomic Solids: Carbon and Silicates（Tro）", "url": "https://chem.libretexts.org/Bookshelves/General_Chemistry/Map%3A_Structure_and_Properties_(Tro)/13%3A_Phase_Diagrams_and_Crystalline_Solids/13.07%3A_Network_Covalent_Atomic_Solids-_Carbon_and_Silicates", "checked_on": "2026-11-09"},
  {"title": "Geosciences LibreTexts, GEOS: A Physical Geology Lab Manual, 3.02 Activity 3A Assessing Hardness Values of Minerals", "url": "https://geo.libretexts.org/Bookshelves/Geology/GEOS%3A_A_Physical_Geology_Lab_Manual_for_California_Community_Colleges_(Branciforte_and_Haddad)/03%3A_Minerals_and_Mineral_Identification/3.02%3A_Activity_3A-_Assessing_Hardness_Values_of_Minerals", "checked_on": "2026-11-09"},
  {"title": "GIA, Diamond Care and Cleaning Guide", "url": "https://www.gia.edu/diamond-care-cleaning?lang=en", "checked_on": "2026-11-09"},
  {"title": "GIA 4Cs, More than the Mohs Scale: Gem Durability", "url": "https://4cs.gia.edu/en-us/blog/more-than-mohs-scale-gem-durability/", "checked_on": "2026-11-09"},
  {"title": "GIA 4Cs, Digging into Diamond Types", "url": "https://4cs.gia.edu/en-us/blog/digging-diamond-types/", "checked_on": "2026-11-09"},
  {"title": "GIA Gems & Gemology (Summer 2018), Natural-Color Blue, Gray, and Violet Diamonds", "url": "https://www.gia.edu/gems-gemology/summer-2018-natural-color-blue-gray-violet-diamonds", "checked_on": "2026-11-09"},
  {"title": "GIA, Blue Diamonds Have Surprise Origin and Link to Ocean", "url": "https://www.gia.edu/articles/blue-diamonds-have-surprise-origin-and-link-to-ocean", "checked_on": "2026-11-09"},
  {"title": "GIA, Jade Description", "url": "https://www.gia.edu/jade-description", "checked_on": "2026-11-09"},
  {"title": "International Gem Society, Jade Toughness and Care（預覽）", "url": "https://www.gemsociety.org/article/jade-toughness-and-care", "checked_on": "2026-11-09"},
  {"title": "Bradt, Newnham & Biggers (1973), The Toughness of Jade, American Mineralogist 58: 727–732", "url": "http://www.minsocam.org/ammin/AM58/AM58_727.pdf", "checked_on": "2026-11-09"},
  {"title": "Science Museum Group Learning, Graphite circuits", "url": "https://www.sciencemuseumgroup.org.uk/learning/resources/graphite-circuits", "checked_on": "2026-11-09"},
  {"title": "STAEDTLER Canada, Pencils and accessories（製造商頁面）", "url": "https://www.staedtler.com/ca/en/products/pencils-and-accessories/", "checked_on": "2026-11-09"},
  {"title": "University of Iowa Libraries, Engineering Library blog: pencil（Conté 與石墨黏土比例）", "url": "https://blog.lib.uiowa.edu/eng/?p=1057", "checked_on": "2026-11-09"},
  {"title": "US Patent 2,986,472, Pencil clays", "url": "https://patents.google.com/patent/US2986472A/en", "checked_on": "2026-11-09"},
  {"title": "Wikipedia: Graphite（raw wikitext；導電異向性引 Pierson）", "url": "https://en.wikipedia.org/wiki/Graphite", "checked_on": "2026-11-09"},
  {"title": "Wikipedia: Diamond（raw wikitext）", "url": "https://en.wikipedia.org/wiki/Diamond", "checked_on": "2026-11-09"}
]
```
