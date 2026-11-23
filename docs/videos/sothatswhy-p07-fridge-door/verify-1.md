# 查核報告 1（sothatswhy-p07-fridge-door）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-06
- 方法：逐句讀 `video.json` 的 240 句台詞（p001–p240，與 `script.md` 的 130 個場景一一對應），加上 YouTube 標題、說明與縮圖文字，並看過重點場景的畫面提示詞。本集沒有卡片（全部是 `shot`）。對照 `claims.md` 的 C01–C16；claims.md 沒寫到的句子（背後「熱熱的風」、壓縮機是「馬達」、門開著時壓縮機「停不下來」、室外機的熱「是從你的房間搬出來的」、冷暖氣機「從外面搬來好幾份」）也另外查。每一條都重新打開來源讀原文（curl 抓頁面轉成文字、Wikipedia 用 raw wikitext、雪梨大學 PDF 用 pdftotext），不只沿用 claims.md 的引文。
- 打不開的來源：沒有。雪梨大學 Bar Fridge PDF 第一次 curl 被重設連線，重抓後讀到全文。11 筆來源全部讀到原文。
- 撰稿者標成推論的兩處：claims.md C02 註明 p038–p039（門口冷空氣把臉上的熱帶走）是把 C01 規則套在門口那團冷空氣上；C11 註明 p170–p171（開著門的冰箱帳上像電暖器）是把 Wikipedia Dehumidifier 的說法套到冷熱兩頭都在同一個房間的冰箱。兩處推論都成立，見第二節。
- 字數：照 `build_scenes.py` 的 `length()`（不算標點）用程式數過，替換句每句等長或更短；小問 ≤15 字、所長 ≤25 字。
- 結論統計（台詞 240 句）：OK 235、FIX 5、NOT FOUND 0。另外標題、說明、縮圖共 3 項：OK 3。畫面提示詞沒有必須修改的地方。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| F01 | p199–p200（所長） | 一般的冷氣，用一份電，／大約能搬走三份以上的熱。 | FIX（倍數講得比來源硬） | 「三份以上」只有次要來源撐：Wikipedia COP "Most air conditioners have a COP of 3.5 to 5"，引的是澳洲一家冷氣公司的網頁，也沒說是制冷還是制熱。主要的教學來源 HyperPhysics 給的數字不一樣：「A typical CP for a commercial heat pump is between 3 and 4」是**熱泵制熱**，算的是送到熱的那頭的熱，裡面含那份電；Wikipedia COP 自己寫 "COP_heating = COP_cooling + 1"，換成「搬走」只有 2–3 份。同頁講冷氣的 EER 段落還說 "The range of EER's for air conditioners is typically about 5.5 to 10.5 … This is a range of 1.6 to 3.1 in CP"（數字偏舊，但仍是本集引用的來源）。新的變頻冷氣多半超過 3，可是依本集列出的來源，「三份以上」只靠一條廠商引用撐，跟 P14 verify-1 F01 一樣，小朋友會把一個取法記成定值。改成「好幾份」，跟 p214 用詞一致，在每個來源下都成立。p203–p204「要看冷氣和天氣」照留 |
| F02 | p201（小問） | 一份電搬三份熱？ | FIX（跟著 F01） | 小問把「三份以上」照念成「三份」，數字更像定值。改成跟 F01 一致。畫面 kid-bargain（一隻手比一、一隻手比三）與 one-to-three（三顆球加一顆小的）仍對得上「好幾份」，不必重畫 |
| F03 | p105–p106（所長） | 它跑進一顆圓圓的馬達裡。／這顆馬達叫做壓縮機。 | FIX（機制說錯） | 壓縮機不是馬達。它是一個把氣體壓緊的泵，家用冰箱的壓縮機是密封的鐵殼，馬達裝在裡面帶動它。HyperPhysics："Then it is compressed and forced to condense in the hot area"；EGEE 102："it uses a compressor to ramp up the pressure on the gaseous refrigerant"、"the compressor needs energy to do the work of compressing the refrigerant"。說它「叫做壓縮機」的那個東西就是馬達，會讓觀眾以為壓縮機只是讓冷媒轉圈的動力，下一句 p107「擠得緊緊的」講的才是它的工作。畫面 compressor 是 "a small round black metal compressor"，改成「鐵罐」跟畫面一致；p119–p120「吃電才轉得動」已經交代它要用電 |
| F04 | p074（小問） | 有一股熱熱的風！ | FIX（說得太強） | 來源只說比室溫暖：HyperPhysics "you will notice that this area is warmer than the room temperature"；伊利諾大學 "it will usually be warm if the unit is running"。所長下一句 p076 也說管子「摸起來是溫的」，p079 說「溫溫的風」。「熱熱的」會讓小朋友以為冰箱背後燙手，也跟所長的話對不上。畫面 coils 畫的是背後外露的散熱管（"faint warm shimmering air"），這種沒有風扇，只會有溫溫的空氣往上飄，「熱熱的風」更誇張。改成「溫溫的」 |

## 二、逐段核對（OK 的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p011 | 開冰箱門臉涼涼的；想用開著的冰箱代替冷氣；請觀眾猜會變涼還是變熱 | OK | — | 開場鋪陳與小問的錯猜，沒有事實主張 |
| p012–p013 | 冰箱背後摸起來一點都不冷 | OK | HyperPhysics Refrigerator | "If you place your hand behind an operating refrigerator, you will notice that this area is warmer than the room temperature." |
| p014–p021 | 陽台那台嗡嗡轉的大箱子吹冷風還是熱風；答案都在同一台冰箱裡 | OK | — | 問題與承諾句。答案在 p182–p184 |
| p022–p029 | 冷從冰箱跑出來（錯猜）；熱茶變溫、冰塊融化 | OK | — | 小問的錯猜與日常觀察，claims.md C01 說明不另列來源 |
| p030–p031 | 冰塊融化是旁邊空氣的熱跑進冰塊；熱自己走只會從熱的地方跑到冷的地方 | OK | HyperPhysics Refrigerator | "internal energy will not spontaneously flow from a cold region to a hot region"。「自己走」限定了是沒有做功的情況，p054 的「一定」接在「照剛剛那條規矩」後面，意思相同 |
| p032–p035 | 冷就是熱比較少；冷不是一種會跑出來的東西 | OK | EGEE 102 | "\"Create cold\" (cold is simply the absence of heat)" |
| p036–p040 | 冰箱的冷空氣流出來碰到臉，臉上的熱跑進冷空氣（**撰稿者標的推論 1**） | OK | HyperPhysics；雪梨大學 | 推論成立：門口流出來的空氣比臉冷，熱照 C01 的規則從臉流向冷空氣。雪梨大學 "it may be slightly cooler directly in front of the fridge door" 支持門口確實有冷空氣。台詞只說「流出來」，沒有說冷空氣往下沉（claims.md 註明找不到教學來源），守住了界線。p040「熱被偷走」是小問的比喻 |
| p041–p044 | 畫圈、熱畫成紅球 | OK | — | 片中的記帳方式，沒有事實主張 |
| p045–p046 | 冷藏大約三到五度，比夏天的廚房冷一大截 | OK | Wikipedia Refrigerator | "A refrigerator maintains a temperature a few degrees above the freezing point of water. The optimal temperature range for perishable food storage is 3 to 5 °C"；另說 "a refrigerator does not usually need to be colder than 4 °C"。原文是建議範圍，台詞用「大約」，可以 |
| p047–p048 | 冷凍庫多半在零下十八度，甚至更冷 | OK | Wikipedia Refrigerator | "Most household freezers maintain temperatures from −23 to −18 °C"。「多半」「甚至更冷」恰好對上範圍。「下面的冷凍庫」指畫面那台，claims.md 已說明 |
| p049–p050 | 比台灣的冬天冷多了 | OK | — | 小問的反應；台灣平地冬天遠高於零下十八度（玉山的歷史極端低溫接近這個數字，但一般說「台灣的冬天」不會指那裡） |
| p051 | 裡外差得越多，熱越急著往裡面鑽 | OK | HyperPhysics Thermal Conductivity | "The rate of heat transfer depends upon the temperature gradient and the thermal conductivity of the material." |
| p052–p055 | 廚房的熱會想鑽進冰箱；門擋了它一下 | OK | HyperPhysics | 同 C01 |
| p056–p058 | 門又厚又重，邊上一圈軟膠條；跟保溫瓶一樣厚 | OK | Wikipedia Refrigerator | "Modern units use a magnetic door gasket that holds the door sealed"。「跟保溫瓶一樣厚」是小問自己的比較 |
| p059–p060 | 門和牆裡塞了擋熱的材料，叫做隔熱，讓熱跑得慢一點 | OK | Wikipedia Refrigerator | "consisting of a thermally insulated compartment"；同頁提到 "replacing insulation"、"CFC-bearing insulation"。說「慢一點」不是「擋住」，正確 |
| p061–p066 | 熱還是會溜進去；冰箱一直那麼冷，表示有東西一直把熱搬出去 | OK | Wikipedia Refrigerator；HyperPhysics | "a heat pump … that transfers heat from its inside to its external environment"。推理正確 |
| p067–p072 | 冰箱把熱吃掉（錯猜）；熱不會憑空變不見，只會換個地方待 | OK | Wikipedia COP | 第一定律："after a full cycle of the process Q_H + Q_C + W = 0"。說法對能量成立 |
| p073 | 後面暖暖的 | OK（p074 見 F04） | HyperPhysics | "warmer than the room temperature" |
| p075 | 手靠近就好，背後有電線 | OK | — | 安全提醒，一般常識，claims.md 不當成查核主張 |
| p076–p078 | 背後一排彎彎的管子摸起來是溫的；冰箱裡少掉的熱從這裡吐回廚房 | OK | HyperPhysics Refrigerator | "taking energy from the freezing compartment, making it colder, and exhausting that heat to the room, making it warmer"。「這一排」指畫面那台，散熱管位置因機型不同，claims.md 已說明 |
| p079–p082 | 有的冰箱從底下吹溫風，站在前面腳邊吹得到；腳暖臉涼 | OK | HyperPhysics Refrigerator | "you may notice that the refrigerator blows warm air on your feet as you stand in front of it"。「有的」措辭恰當；「從底下」是從「吹到腳」推出的位置，合理 |
| p083–p086 | 冰箱管子裡有一種繞圈子跑的東西叫冷媒 | OK | HyperPhysics；EGEE 102 | "a refrigerant liquid is forced to evaporate … Then it is compressed and forced to condense"；EGEE "a refrigerant that constantly changes from …" |
| p087–p089 | 冷媒不一定冷，但會變身 | OK | HyperPhysics | "forced to evaporate and then condense"。冷媒在循環中溫度高低都有，「不一定冷」正確 |
| p089–p094 | 洗完熱水澡濕濕地出來會冷得發抖；身上的水變水氣飛走時把熱帶走 | OK | EGEE 102 | "That's the reason you feel chilly getting out of the shower … The water has to absorb heat to evaporate. And it carries that heat away from you." |
| p095–p096 | 冷媒在冰箱裡從液體變成氣體，把裡面的熱帶進管子裡 | OK | HyperPhysics | "a refrigerant liquid is forced to evaporate and extract energy from the cold area" |
| p097–p102 | 冷媒是特別挑過、很容易沸騰的液體；冰箱裡那點熱就夠它變成氣體 | OK | EGEE 102 | "The refrigerant has a low boiling point, so the heat from the interior air is enough to make it turn into a gas"；"A refrigerant needs to have a pretty low boiling point, and one that can be adjusted … by changing the pressure"。附註：沸點低還要靠降壓（膨脹閥），本集依語速刪了膨脹閥，台詞沒有說錯，只是沒講全 |
| p103–p104 | 帶著熱的氣體接著跑去哪 | OK | — | 問題 |
| p105–p106 | 壓縮機 | 見 F03 | — | — |
| p107–p110 | 壓縮機把冷媒氣體擠緊；擠緊的冷媒流進背後的管子變回液體，把熱交給廚房；再流回冰箱重新跑一圈 | OK | HyperPhysics；EGEE 102 | "Then it is compressed and forced to condense in the hot area, dumping its heat of vaporization into the hot area"；EGEE "so much that it can condense into a liquid again, even though it's at the warmer outside temperature. As it condenses, the refrigerant loses heat to the air around it"。沒有說「擠到比廚房還燙」，守住 claims.md 的界線 |
| p111–p112 | 像搬熱的小火車，一圈一圈把熱從裡面載到外面 | OK | HyperPhysics | 比喻，"\"pump\" energy from a cold region to a hotter region" |
| p113–p117 | 背後別貼死，留空隙熱才散得出去；清管子上的灰塵 | OK | Wikipedia Refrigerator | "Cleaning condenser coils to remove dust impeding heat flow, and ensuring that there is space for air flow around the condenser can improve efficiency." |
| p118–p121 | 推小火車的是電；把氣體擠緊很費力，壓縮機要吃電才轉得動 | OK | EGEE 102 | "the compressor needs energy to do the work of compressing the refrigerant" |
| p122–p124 | 冰箱一變暖壓縮機開工，夠冷就停；所以有時安安靜靜 | OK | Wikipedia Refrigerator | "When the refrigerator gets too warm, the thermostat starts the cooling process" |
| p125–p133 | 電去哪、吐的熱跟搬的一樣多嗎；把整間廚房圈進來 | OK | — | 問題與記帳設定 |
| p134–p136 | 先假設一組好算的數字：搬兩顆熱、吃一份電 | OK | — | 明說是假設（「我們先假設一組好算的數字」），說明欄也再寫一次「為了好算的假設數字」。兩顆對一份等於制冷 COP 2，量級合理，而且沒有被說成實測。這組數字是假設，所以不需要另找來源 |
| p137–p140 | 背後吐三顆：搬出的兩顆加上電變的一顆；吐的比搬的多 | OK | Wikipedia COP；HyperPhysics Heat Pump；伊利諾大學 | COP 頁 "COP_heating = (Q_C + W)/W"、第一定律 Q_H + Q_C + W = 0；伊利諾大學 "more heat gets dumped outside the fridge than gets pumped out"。三顆是從假設算出來的，跟假設綁在一起 |
| p141 | 電用完不會變不見，最後也變成熱 | OK | Wikipedia COP；伊利諾大學 | 第一定律。伊利諾大學說 "some of the electrical energy gets converted to heat"，是指冰箱不可能完美；就整個循環來說，壓縮機做的功最後都在冷凝器變成熱放出，「最後也變成熱」成立，台詞也沒有說「百分之百」 |
| p142–p147 | 門關著時，從牆和門邊溜進去的熱被搬回廚房，加上電；冰箱只要在跑，廚房就被加熱一點點 | OK | 伊利諾大學 | "when a fridge is running it is really warming up the room a little bit"。溜進去的熱搬回來，抵銷之後廚房淨多出來的就是那份電，帳正確 |
| p148–p152 | 門打開：廚房的熱從門口灌進冰箱，被搬到背後吐回廚房；熱在繞圈 | OK | 伊利諾大學；雪梨大學 | "The refrigerator of course pumps heat around, from its inside to its coils, but … it still ends up dumping net energy into the room" |
| p153–p158 | 那兩顆熱只在圈裡轉，廚房的熱沒少；每轉一圈閃電多變出一顆熱；門開著廚房反而變熱 | OK | 伊利諾大學；雪梨大學 | 伊利諾大學 "The average room temperature in the room will rise"；雪梨大學 "The nett effect of leaving the fridge door open is to make the room hotter"。「每轉一圈多一顆」接的是前面假設的帳，比例跟著假設走。前提是門窗關著的房間（伊利諾大學問的就是 closed room）；片中廚房沒有開窗，claims.md 已說明 |
| p159–p162 | 站在門口真的涼涼的；門口前面那一小塊是會涼一點，走開就跟你沒關係 | OK | 雪梨大學；伊利諾大學 | "although it may be slightly cooler directly in front of the fridge door"；"Of course there will be hotter spots and colder spots but we are talking about the average"。「一小塊」「一點」措辭恰當 |
| p163–p165 | 門一開冰箱裡一直變暖，壓縮機停不下來、一直吃電 | OK | 伊利諾大學 | "with the door open the temperature will start to rise inside the refrigerator. The thermostat will kick in and try to cool it back down. This means the motor is running"。門一直開著時冰箱裡回不到設定溫度，溫控不會讓它停，「停不下來」可以 |
| p166–p167 | 吃的電越多，多變出的熱越多；電費也跟著變多 | OK | 第一定律；伊利諾大學 | "the motor is running, which means heat is being added to the room"。電費是常識 |
| p168–p171 | 開著門的冰箱像電暖器：算起帳來很像，吃進去的電最後都變成熱留在廚房（**撰稿者標的推論 2**） | OK | Wikipedia Dehumidifier；伊利諾大學；雪梨大學 | 推論成立。Dehumidifier："since all components of the dehumidifier are in the same room, no heat energy is removed. Instead, the electric power consumed by the dehumidifier remains in the room as heat, so the room is actually heated, just as by an electric heater that draws the same amount of power."。開著門的冰箱，冷的那頭（打開的冰箱裡面）和熱的那頭（背後）都在同一個房間，跟這段描述的情形一樣；伊利諾大學的 "dumping net energy into the room" 也是同一筆帳。「算起帳來很像」把相似處限在帳上，沒有說發熱的位置或快慢一樣 |
| p172–p174 | 我覺得冰箱是搬熱的機器，不是做冷的機器 | OK | EGEE 102 | 意見句有「我覺得」；"An AC is a heat pump, not a cold generator" 同義，HyperPhysics 說冰箱與冷氣原理相同 |
| p175–p178 | 冷氣和冰箱是同一種機器，也有冷媒、壓縮機，也吃電 | OK | HyperPhysics；EGEE 102 | "The statements about refrigerators apply to air conditioners and heat pumps, which embody the same principles"；"Air conditioning -- and refrigeration, which is the same thing just in a slightly smaller box" |
| p179–p182 | 陽台的室外機吹出來的是熱風 | OK | EGEE 102；Wikipedia Dehumidifier | EGEE 逐字稿說熱由風扇往外吹（"…blows outside"）；Dehumidifier "its condenser coil releases heat outside" |
| p183–p184 | 室外機吹的熱是從你的房間搬出來的 | OK | EGEE 102 | "Only heat energy is moved or pumped by the air conditioner from a low temperature environment (inside the building) to a high temperature environment (outside the building)"。電變的那份熱在 p197 才補上，這裡先講搬出來的熱，前後不矛盾 |
| p185–p188 | 冷氣是把外面空氣變冷吹進來（錯猜）；其實吹的是房間自己的空氣 | OK | EGEE 102 | "Contrary to what is generally assumed, outside air is not cooled inside the air conditioner and then supplied inside"；"Filter and recirculate indoor air"；不做 "Bring in large amounts of outdoor air (unless designed for ventilation)" |
| p189–p190 | 牆上那台把空氣吸進去、拿走熱、再吹回來；和陽台那台中間連著兩條管子 | OK | EGEE 102；Wikipedia Air conditioning | EGEE "The liquid refrigerant flows through a series of coils exposed to the air in your home … A fan blows that colder air into your room"；分離式 "indoor unit … single outdoor unit"。兩條冷媒管（一進一出）是常見做法，台詞說的是畫面上那台 |
| p191–p196 | 冷媒在兩台之間繞圈；房間是冰箱裡面，冰箱背後搬到了牆外；熱的那頭在外面 | OK | HyperPhysics；EGEE 102 | 比喻，原理同 C13 |
| p197–p198 | 冷氣吃的電大部分也變成熱，在室外機一起吐到圈外 | OK | Wikipedia COP；Wikipedia Dehumidifier | 第一定律加 "its condenser coil releases heat outside"。壓縮機在室外機裡，室內機風扇的電留在室內，說「大部分」是正確的取捨 |
| p199–p201 | 一份電大約搬三份以上的熱 | 見 F01、F02 | — | — |
| p202 | 好會搬！ | OK | — | 小問的反應 |
| p203–p204 | 確切搬多少看冷氣和天氣，外面越熱通常越吃力 | OK | Wikipedia COP；Wikipedia Air conditioning | "The COP is highly dependent on operating conditions, especially absolute temperature and relative temperature between sink and system"；Carnot 上限 T_C/(T_H − T_C) 隨溫差變大而下降。「通常」措辭恰當 |
| p205–p208 | 冷暖氣機在冬天可以倒過來跑，從外面的冷空氣把熱搬進房間 | OK | Wikipedia Air conditioning；HyperPhysics | "Some air conditioning systems can reverse the refrigeration cycle and act as an air source heat pump … reverse cycle air conditioners"；"when the heat pump is in heating mode … the outdoor condenser unit … discharges cold air (colder than the ambient outdoor air)"；HyperPhysics "\"pump\" 3 kWh of energy from the cooler outside environment into your house" |
| p209–p212 | 外面那麼冷也有熱可搬：冷只是熱比較少 | OK | EGEE 102；Wikipedia Air conditioning | "cold is simply the absence of heat"；室外機在制熱時吐出比室外更冷的空氣，表示確實從冷空氣裡拿走了熱 |
| p213–p214 | 電暖器一份電只給一份熱；冷暖氣機一份電可以從外面搬來好幾份 | OK | HyperPhysics Heat Pump | "an electric resistance heater using one kilowatt-hour of electric energy can transfer only 1 kWh … But 1 kWh of energy used in an electric heat pump could \"pump\" 3 kWh of energy from the cooler outside environment into your house"；"typical CP … between 3 and 4"。附註：照本集自己的帳，送進房間的 3–4 份裡有 1 份是電，從外面搬來的是 2–3 份；天冷時效率也會下降（Wikipedia Air conditioning "less efficient in outdoor temperatures lower than 4 °C"）。「好幾份」加上「可以」，在這個範圍內成立 |
| p215 | 用搬的比用做的划算 | OK | HyperPhysics；Wikipedia COP | "Less work is required to move heat than to generate heat." |
| p216–p219 | 開冷氣時關窗、拉窗簾，就是幫房間關上一道厚門 | OK | 香港機電工程署 | "Keep windows and doors closed when an air conditioner is turned on, and use curtains or blinds to shade against sunlight." 厚門是本片的比喻 |
| p220–p222 | 冷氣負責搬熱，隔熱讓外面的熱慢一點溜回來 | OK | 香港機電工程署；Wikipedia Refrigerator | 建議本身有來源；「慢一點」跟 p060 一致，沒有說擋住 |
| p223–p224 | 開著冷氣又開著窗，就像開著冰箱門，冷氣只好搬個不停 | OK | 伊利諾大學（同理）；香港機電工程署 | 跟 p163–p164 同一個道理，不給耗電數字 |
| p225–p227 | 開冷氣的房間就是一台大冰箱，你住在冰箱裡面 | OK | — | 比喻 |
| p228–p232 | 回廚房；收回好方法；冰箱門開著，熱的那頭還留在廚房 | OK | 同 p148–p158 | 小問自己說出答案 |
| p233–p234 | 冰箱和冷氣是同一種搬熱的機器，差在熱的那頭放在圈裡還是圈外 | OK | HyperPhysics；Wikipedia Dehumidifier | "embody the same principles"；"A standard air conditioner transfers heat energy out of the room because its condenser coil releases heat outside" |
| p235–p236 | 摸摸冰箱背後：那一點溫溫的，是搬出來的熱再加上它吃的電 | OK | HyperPhysics；伊利諾大學 | 同 p137–p141 |
| p237–p240 | 原來如此；留言題；訂閱 | OK | — | 沒有事實主張 |
| `youtube.title` | 冰箱門打開，房間為什麼不會變涼？ | OK | 伊利諾大學；雪梨大學 | — |
| `thumbnail` | 冰箱門開著 **廚房更熱**／冰箱只是把熱搬到背後 | OK | 雪梨大學；HyperPhysics | "make the room hotter"。副標沒提電，但「只是搬」的意思是不做冷，跟正片一致 |
| `youtube.description` | 圈越畫越大；「兩顆熱加一份電」是假設；冷氣搬熱的倍數是教學資料裡的大約數字，實際看機型與天氣 | OK | 同上 | 照 F01 改成「好幾份」後，說明欄的寫法仍然對，不必動 |

## 三、畫面提示詞

沒有發現畫出錯誤事實的提示詞。逐項看過的重點：

- coils：背後黑色之字形管子、溫溫的空氣往上飄、紅球飄進廚房，與 HyperPhysics 一致。也是 F04 改「溫溫的」的理由之一（外露散熱管沒有風扇）。
- compressor：「small round black metal compressor」低低地放在背後角落、接兩條銅管，正確；F03 的「鐵罐」對應這個畫面。
- two-plus-one：兩顆紅球加一道閃電進去、出來三顆，與假設的帳一致。
- plan-extra：門開著時一道閃電變成一顆多出來的紅球，與 p155–p156 一致。
- indoor-unit：分離式冷氣室內機，兩條細管穿牆到外面，與 p190 一致。
- one-to-three、kid-bargain：一道閃電對三顆多一點的紅球、一根手指對三根手指。F01、F02 改成「好幾份」後仍對得上（三是「好幾」之一），不必重畫。
- fridge-open：冷霧飄到臉上，對應 p036–p039 的推論；只畫門口一小塊，沒有畫成整間廚房變冷。

## 建議修改

- p074：有一股熱熱的風！ → 有一股溫溫的風！（7 字，與原句同長）
- p105：它跑進一顆圓圓的馬達裡。 → 它跑進一顆圓圓的鐵罐裡。（11 字，與原句同長）
- p106：這顆馬達叫做壓縮機。 → 這顆鐵罐叫做壓縮機。（9 字，與原句同長）
- p200：大約能搬走三份以上的熱。 → 大約能搬走好幾份的熱。（10 字，原句 11 字）
- p201：一份電搬三份熱？ → 一份電搬好幾份？（7 字，與原句同長）
- （給 claims.md 的維護者）C15 的「可用說法」改成「好幾份」，並補記：HyperPhysics 的 3–4 是熱泵**制熱**，含那份電，換成搬走是 2–3（Wikipedia COP "COP_heating = COP_cooling + 1"）；同頁冷氣 EER 段落換算成 CP 是 1.6–3.1；Wikipedia 的 3.5–5 引的是廠商網頁。C07／C08 補一句：壓縮機是把氣體壓緊的泵，馬達在它裡面帶動它，台詞不說它「是馬達」。C06 補一句：小問的反應用「溫溫的」，不說「熱熱的」。

## 來源

只列查核者這次實際打開並讀到原文的頁面，格式可直接放進 `video.json` 的 `sources`。`video.json` 現有的 11 筆來源都重新讀過，本輪沒有新增。

```json
[
  {"title": "HyperPhysics (Georgia State University): Refrigerator", "url": "https://hyperphysics.gsu.edu/hbase/thermo/refrig.html", "checked_on": "2026-11-06"},
  {"title": "HyperPhysics (Georgia State University): Heat Pump, Air Conditioners and Heat Pumps, Coefficient of Performance", "url": "https://hyperphysics.gsu.edu/hbase/thermo/heatpump.html", "checked_on": "2026-11-06"},
  {"title": "University of Illinois Physics Van: Open Refrigerator", "url": "https://van.physics.illinois.edu/ask/listing/1790", "checked_on": "2026-11-06"},
  {"title": "University of Sydney School of Physics: Bar Fridge (thermal physics activity)", "url": "https://www.physics.usyd.edu.au/super/physics_tut/activities/Thermal_Physics/Bar_Fridge.pdf", "checked_on": "2026-11-06"},
  {"title": "Penn State EGEE 102: 10.4 How Air Conditioners Work", "url": "https://courses.ems.psu.edu/egee102/node/2426", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Refrigerator", "url": "https://en.wikipedia.org/wiki/Refrigerator", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Coefficient of performance", "url": "https://en.wikipedia.org/wiki/Coefficient_of_performance", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Air conditioning", "url": "https://en.wikipedia.org/wiki/Air_conditioning", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Dehumidifier", "url": "https://en.wikipedia.org/wiki/Dehumidifier", "checked_on": "2026-11-06"},
  {"title": "HyperPhysics (Georgia State University): Thermal Conductivity", "url": "https://hyperphysics.gsu.edu/hbase/thermo/thercond.html", "checked_on": "2026-11-06"},
  {"title": "Electrical and Mechanical Services Department, Hong Kong: Energy Saving Tips For Home, Air Conditioner", "url": "https://emsd.gov.hk/energyland/en/tips/home/air_conditioner.html", "checked_on": "2026-11-06"}
]
```
