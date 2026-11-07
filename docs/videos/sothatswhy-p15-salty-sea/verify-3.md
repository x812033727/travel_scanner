# 查核報告 3（sothatswhy-p15-salty-sea）

- 查核者：Claude（第三輪獨立查核代理，未參與撰稿與前兩輪）
- 日期：2026-11-07
- 方法：逐句讀現行 `video.json`（commit d2495b13 之後的版本，第五版）的 175 句台詞（id p001–p175），加上 YouTube 標題、說明與縮圖 headline／sub。先用 git 比對 verify-2 查過的版本，找出新寫或改寫的句子（p032–p034、p046、p048、p052–p053、p060–p061、p068–p069、p087、p135–p136、p155、p157–p158、p163、p167–p168），再加上協調者點名的 p014–p015、p020、p035–p036、p086、p110–p121、p124、p143、p171，全部重讀來源；其餘沒改的句子也逐句對過一次。不沿用 claims.md、verify-1、verify-2 的引文，用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新抓下來源、轉成文字後讀原文：NOAA whysalty／riversnotsalty／drinksw、USGS why-ocean-salty／saline-water-and-salinity／how-much-water-there-earth、USGS Oceans and Seas and the Water Cycle、USGS Evaporation and the Water Cycle（新增，p060–p061 用）、USGS Precipitation and the Water Cycle、NASA Earth Observatory A Measure of Salt／A Global Accounting of Earth's Rivers、LibreTexts 8.9 Residence Time、Gale〈Ocean Chemical Processes〉（encyclopedia.com）、HELCOM Salinity（archive.iwlearn.org）、水產試驗所 107 年度監測報告 PDF（pdftotext），以及 Wikipedia Red Sea、Baltic Sea、Dead Sea、Evaporite（raw wikitext）。全部回 200（USGS water-cycle-schools-and-kids 回 404，改用上面兩頁 USGS 水循環頁）。
- 沒有開的來源：WHOI 熱泉頁。p112「帶出石頭裡的一些金屬」NOAA whysalty 原文已經寫明（"pick up metals such as iron, zinc, and copper"），不需要它。
- 字數：所長台詞只有 p163 為 26 字（含標點），超過 25 字上限一字；小問台詞只有 p051 為 16 字（verify-2 已列）。不是事實問題，列在第一節附註給撰稿參考。
- 對來源清單的建議（不是台詞的 FIX）：
  - p060–p061「有的直接下回海上」只有 USGS〈Evaporation and the Water Cycle〉直接支撐："Most of the water that evaporates from the oceans falls back into the oceans as precipitation. Only about 10 percent of the water evaporated from the oceans is transported over land and falls as precipitation." 建議補進 `video.json` 的 `sources` 與 claims.md〈來源〉（https://www.usgs.gov/special-topics/water-science-school/science/evaporation-and-water-cycle）。
  - p116「海灣」與 Gale 的 "isolated bodies of sea water" 之外，Wikipedia Evaporite（"a closed basin, or one with restricted outflow"）可以一起列進 claims.md C16。
  - `youtube.tags` 還有「七股鹽山」，正片已經拿掉七股；標籤不是事實主張，留不留由撰稿決定。
- 結論統計（台詞 175 句）：OK 172、FIX 3、NOT FOUND 0。標題、說明、縮圖 headline、縮圖 sub 共 4 項：OK 4。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 建議改成 | 理由與來源 |
| --- | --- | --- | --- | --- | --- |
| F01 | p115 | 它要從鍋邊出去，就像湯熬乾時，鍋邊那一圈鹽。 | FIX（說得太滿） | 「有一條路在鍋邊，就像湯熬乾時，鍋邊那一圈鹽。」（22 字） | 「它要從鍋邊出去」聽起來是廚房那種鹽唯一（或主要）的出口。來源只支撐「蒸發岩收走大量的鹽」：Gale "Evaporation of isolated bodies of sea water accounts for removal of large amounts of salt from the ocean … mined for table salt"，沒有說它是鈉、氯唯一或最大的出口。NOAA riversnotsalty 反而把每年等量的鹽放在鍋底："About the same tonnage of salt from ocean water probably is deposited as sediment on the ocean bottom"。p121「鹽的出口在鍋底和鍋邊」本身是對的，所以 p115 改成「有一條路」，跟 p121 一致，也回到 verify-2 時「有一條很慢的出口」的分寸 |
| F02 | p120 | 對，只是收得很慢。還記得你找的排水孔嗎？ | FIX（會誤導平衡） | 「對，收走的大概跟送來的差不多。還記得排水孔嗎？」（24 字） | 小問問「河送進來的鹽，海也一直在收？」，回答「只是收得很慢」容易被聽成「收的比送的少」，那海就該一直變鹹，跟 p122「一邊加一點鹽，一邊結一點鍋巴」、p124「大概已經沒有再越變越鹹」打架。來源說的是收送相當：NOAA riversnotsalty "About the same tonnage … yearly gains may offset yearly losses … balanced salt input and output"；Gale "steady state — that is, operating so that the input of salt equals the output"。「慢」只在單一顆鹽的停留時間上成立（Gale 鈉 80 × 10⁶ 年），p081 已經講過「泡上幾千萬年」，這裡不必再說。「大概」對上 NOAA 的 "probably" |
| F03 | p167 | 海底和海邊，再慢慢把鹽收走！ | FIX（比喻換成了實景） | 「海底和鍋邊，再慢慢把鹽收走！」（14 字） | 正片裡的「鍋邊」指的是很久以前跟大海隔開、被曬乾埋進地底的鹽層（p115–p117；Gale 蒸發岩），不是今天的海邊。小問改說成實景的「海邊」，孩子會以為現在的沙灘在收鹽，也跟 p155「岸邊的海水……會淡一點」方向相反；p168「完全正確！」又替這句背書。改回比喻的「鍋邊」，跟 p086、p121 的用詞一致，p168 照留 |

附註（不計入 FIX，不改也不算錯）：

- p163（26 字，超過所長 25 字上限）：意見句，內容對（收鹽：NOAA riversnotsalty；送水上天：USGS Evaporation and the Water Cycle）。若要縮短，可改成「就是它一邊收河送來的鹽，一邊把水送上天。」（20 字），只拿掉修辭「從來沒停過」，沒有新增事實。
- p116「海灣」：Gale 只說 "isolated bodies of sea water"，Wikipedia Evaporite 說 "a closed basin, or one with restricted outflow"。被隔開的海灣、潟湖是其中一種，台詞用「有些」，沒有說全部都是海灣，可以接受；想更貼原文，可改回 verify-1 F05 的「很久很久以前，有些海水跟大海隔開了，」（17 字）。
- p024「那些鹽，是從山上的石頭來的」：NOAA、USGS 都這樣說，OK。Gale 另提到海水裡的氯大多被認為來自火山氣體溶進雨水（"most of the chloride … believed to have come from volcanic gases that were dissolved in rain"），這是比兒童片更細的層次，不改。
- p111「會冒出一些。你一開始說的鹽山，說對了一點點。」：OK。NOAA 把熱泉列為鹽的來源（"Another source of salts in the ocean is hydrothermal fluids"），同頁也提到海底鹽丘（"Salt domes also contribute … found underground and undersea"）。嚴格說來最像「鹽山」的是鹽丘，但台詞只說「一點點」，兩者都是 NOAA 的海底來源，不算錯。

## 二、verify-2 之後新寫與改寫句子的確認

| 行 | 現行句子 | 結論 | 依據 |
| --- | --- | --- | --- |
| p014–p015 | 鹽山？／不過海底真的藏著一個祕密，等一下告訴你。 | OK | 「鹽山？」只是反問，沒有否定。NOAA whysalty：鹽丘 "found underground and undersea"、熱泉與 brine seep，所以不說「沒有鹽山」是對的。祕密在 p086–p087 揭曉（鍋底和鍋邊），p111 再回收鹽山 |
| p020 | 其實河水身上，偷偷帶著鹽。 | OK | NOAA riversnotsalty "rivers carry an estimated four billion tons of dissolved salts"；USGS "carries salts and minerals along in a dissolved state as ions" |
| p032–p033 | 對，看不見，也嘗不太出來。／其中有一些，就是廚房那種鹽的材料。 | OK | Gale 表 1：平均河水 Na⁺ 0.23、Cl⁻ 0.16 mM/l，確實帶著鈉和氯；但以 HCO₃⁻ 0.86、Ca²⁺ 0.33 為主，所以「其中有一些」的分寸正確 |
| p034–p036 | 那鹽不會在河裡越積越多嗎？／因為雨一直下，河水一直被新的雨水換掉，鹽還來不及變多，就被帶進海裡了。 | OK | NOAA riversnotsalty "Rain replenishes freshwater in rivers and streams, so they don't taste salty. However, the water in the ocean collects all of the salt"。「來不及變多」是白話推論，方向與原文一致 |
| p046–p049 | 現在海裡的鹽，多到如果全部撈上來，鋪在陸地上，會有大約四十層樓那麼厚。 | OK | USGS why-ocean-salty "By some estimates, if the salt in the ocean could be removed and spread evenly over the Earth's land surface it would form a layer more than 500 feet (166 meters) thick, about the height of a 40-story office building"。「大約」涵蓋 "by some estimates"；不唸公尺，避開頁面 500 英尺與 166 公尺不一致 |
| p052–p053 | 河一直在倒水，這沒錯，可是海從來沒有滿出來。 | OK | 回應小問 p050–p051；海平面的長期小變化不在孩子的尺度，「沒有滿出來」可以 |
| p060–p061 | 水氣變成雲，下成雨，有的直接下回海上，有的下到山上，再從河裡流回海。 | OK | USGS Evaporation and the Water Cycle "Most of the water that evaporates from the oceans falls back into the oceans as precipitation. Only about 10 percent … transported over land and falls as precipitation"；"over the land, precipitation routinely exceeds evaporation"。「從河裡流回海」略過地下水，是簡化（USGS how-much-water "water in the ground continually recharges rivers"） |
| p068–p070 | 那我也可以在家曬一碟鹽水？／可以。放在太陽下幾天，水不見了，碟子上就剩一圈鹽。 | OK | Gale "the water added to the ocean evaporates but the dissolved salts do not"；在家曬、不用火、不用喝，安全 |
| p086–p087 | 鹽的出口，在鍋底，還有鍋邊。這就是我一開始說的那個祕密。 | OK（比喻） | 鍋底：NOAA riversnotsalty 沉積在海床、Gale 沉積物吸附與生物殼掩埋；鍋邊：Gale 蒸發岩。兩者都有來源 |
| p110–p113 | 那熱泉會冒出鹽嗎？／會冒出一些。你一開始說的鹽山，說對了一點點。／熱泉會帶出石頭裡的一些金屬，也會把海水裡的一些東西，留在石頭裡。 | OK | NOAA whysalty "Another source of salts in the ocean is hydrothermal fluids … lose oxygen, magnesium, and sulfates, and pick up metals such as iron, zinc, and copper from surrounding rocks"；USGS "some of the dissolved salts react with the rock and are removed from seawater"；Gale "loses all its O₂ and all its Mg … gains Ca, Si, Fe, and Mn" |
| p114–p115 | 那廚房那種鹽，要怎麼出去？／它要從鍋邊出去…… | FIX（F01） | 見第一節 |
| p116–p117 | 很久很久以前，有些海灣跟大海隔開了，裡面的海水被曬乾，留下厚厚的鹽層，埋進地底下。 | OK（附註） | Gale "Evaporation of isolated bodies of sea water … Salt deposits occur through the geologic record as layers of gypsum, rock salt"；Wikipedia Evaporite "closed basin, or one with restricted outflow"。「海灣」見第一節附註 |
| p118–p120 | 所以河送進來的鹽，海也一直在收？／對，只是收得很慢。 | FIX（F02） | 見第一節 |
| p121–p122 | 水的出口在天上，鹽的出口在鍋底和鍋邊。一邊加一點鹽，一邊結一點鍋巴。 | OK | 同 p086；NOAA 收送相當 |
| p124 | 海洋學家認為，現在的海，大概已經沒有再越變越鹹了。 | OK | NOAA riversnotsalty "the ocean today probably has a balanced salt input and output (and so the ocean is no longer getting saltier)"，「認為」「大概」對上 "probably" |
| p135–p137 | 先別急，我們先去一片很熱的海看看。像紅海，旁邊幾乎都是沙漠，太陽很大，很少下雨，也幾乎沒有河流進來。 | OK | Wikipedia Red Sea "between arid land, desert and semi-desert"；"high evaporation and low precipitation; no significant rivers or streams drain into the sea"；"scarcity of rainfall"。「幾乎都是沙漠」貼近原文。「很熱的海」：同頁 "relatively hot water in the south"、蒸發 "as high as 2050 mm per year"，可以 |
| p142–p143 | 北邊的波羅的海剛好相反，很多河流進來，下的雨也比曬走的多。 | OK | Wikipedia Baltic Sea "More than 250 streams drain a basin …"；"precipitation less evaporation, which is positive" |
| p155 | 岸邊的海水，就像你看到的河口，會淡一點。 | OK | 水產試驗所 107 年度報告「夏季降雨量高河川淡水輸入較多，在較近岸測站有低鹽水出現」；河口較淡見 NASA A Measure of Salt "runoff from rivers … does make water fresher" |
| p157–p158 | 有一個很有名的，叫死海。它其實是一個湖，水流不出去，只能被太陽熬，熬到比海水鹹快十倍。 | OK | Wikipedia Dead Sea "an endorheic lake, meaning there are no outlet streams"；"342 g/kg, or 34.2% (in 2011) … 9.6 times as salty as the ocean"。「快十倍」對上 9.6 |
| p162–p163 | 我覺得，海最厲害的地方，就是它一邊收河送來的鹽，一邊把水送上天，從來沒停過。 | OK（意見；字數附註） | 有「我覺得」；裡面的事實見 NOAA riversnotsalty、USGS Evaporation and the Water Cycle |
| p165–p167 | 河水帶一點點鹽進海裡，太陽只把水熬走，海底和海邊，再慢慢把鹽收走！ | p165–p166 OK；p167 FIX（F03） | 見第一節 |
| p168 | 完全正確！對了，你昨天喝到的那口海水， | OK（F03 改後） | 套用 F03 後，「完全正確」背書的是正確的說法 |
| p171 | 就知道那是好幾千萬年留下來的味道。 | OK（詩意說法） | LibreTexts 氯 "about 87 million years"、鈉 "about 55 million years"；Gale 鈉 80 × 10⁶ 年 |

## 三、逐段核對（現行 id）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p009 | 小問海邊喝到海水很鹹；所長也喝過；河一直流進海、河水淡，海怎麼沒被沖淡 | OK | — | 開場、角色玩笑與問題 |
| p010–p011 | 全世界的河每天把好多淡水倒進海；你嘗到的海從來沒有變淡過 | OK | NASA Global Accounting of Earth's Rivers | "global discharge to the ocean, which averaged 37,411 cubic kilometers … per year from 1980 to 2009"。「你去海邊嘗到的」限定在孩子嘗得出的尺度 |
| p012–p013 | 海底有一座鹽山一直在冒鹽 | OK（錯猜） | — | 由後文修正 |
| p014–p015 | 鹽山？海底真的藏著一個祕密 | OK | NOAA whysalty | 見第二節 |
| p016–p019 | 河水真的一點鹽都沒有嗎；把海想成一鍋一直在熬的湯 | OK（比喻） | Gale | "the water added to the ocean evaporates but the dissolved salts do not" |
| p020–p023 | 河水偷偷帶著鹽；非常少，嘗不出來 | OK | NOAA riversnotsalty；USGS | 見第二節；"Rain replenishes freshwater … so they don't taste salty" |
| p024–p028 | 鹽從山上的石頭來；雨帶一點點酸，慢慢啃石頭；石頭裡的小東西溶進水裡 | OK（附註） | NOAA whysalty；USGS | "Rainwater that falls on land is slightly acidic, so it erodes rocks. This releases ions"；USGS "slightly acidic due to carbonic acid"。氯的來源見第一節附註 |
| p029–p031 | 看不見的小東西跟著河水流下山；像糖溶在水裡 | OK | NOAA whysalty；USGS | "carried away to streams and rivers that eventually feed into the ocean"；糖只比「看不見」 |
| p032–p036 | 嘗不太出來；其中有一些是廚房那種鹽的材料；雨一直換掉河水 | OK | Gale 表 1；NOAA riversnotsalty | 見第二節 |
| p037–p038 | 淡水的鹽連海水的三十分之一都不到 | OK（定義） | USGS saline-water-and-salinity | "Fresh water - Less than 1,000 ppm"；"ocean water contains about 35,000 ppm of salt" |
| p039–p045 | 全世界的河一年大約帶四十億公噸溶掉的鹽進海 | OK | NOAA riversnotsalty | "an estimated four billion tons of dissolved salts to the ocean annually"，「大約」涵蓋英制或公制 |
| p046–p049 | 鹽鋪在陸地上大約四十層樓厚 | OK | USGS why-ocean-salty | 見第二節 |
| p050–p055 | 河一直倒，海沒有滿；空的海光靠河倒大約三萬多年就滿 | OK（自行換算） | USGS Oceans and Seas；NASA rivers | 1,338,000,000 km³ ÷ 37,411 km³／年 ≈ 35,765 年；假設語氣 |
| p056–p059 | 排水孔？水的出口在天上；太陽一曬變水氣飛上天 | OK | USGS Oceans and Seas | "the oceans supply about 90 percent of the evaporated water that goes into the water cycle" |
| p060–p062 | 成雲、下雨，有的下回海上、有的下到山上再從河流回海 | OK | USGS Evaporation and the Water Cycle | 見第二節 |
| p063–p067 | 鹽沒有跟著飛；太陽只搬得動水；雨幾乎就是被熬出來的淡水 | OK | Gale；NOAA riversnotsalty | 蒸發只帶走水；「幾乎」涵蓋雨裡極少量的海鹽氣溶膠（Gale "sea-spray residues"）與陸地蒸散 |
| p068–p070 | 在家曬一碟鹽水，剩一圈鹽 | OK | Gale | 見第二節 |
| p071–p075 | 像媽媽熬湯；河水是加進去帶一點鹽的水；太陽是爐火 | OK（比喻） | Gale；NOAA | 與前文一致 |
| p076–p080 | 海會不會變一大片鹽巴；一滴水平均待三千年左右就被熬走 | OK | LibreTexts 8.9 | "a water molecule spends 3,100 years floating around in the world ocean reservoir before it's evaporated" |
| p081–p083 | 鹽可以泡上幾千萬年；水只是在鍋裡轉一圈 | OK | LibreTexts；Gale 表 2 | 氯約 8,700 萬年、鈉約 5,500 萬年；Gale 鈉 80 × 10⁶ 年 |
| p084–p087 | 鹽也不是永遠留在湯裡；出口在鍋底和鍋邊；這就是祕密 | OK | NOAA riversnotsalty；Gale | 見第二節 |
| p088–p092 | 溶著的一些東西沉下去，跟泥沙變成一層層泥和石頭；鍋巴 | OK | Gale；NOAA riversnotsalty | "adsorb dissolved material from sea water and cause them to be buried in ocean floor sediments, thus removed from the ocean" |
| p093–p098 | 貝殼和珊瑚拿做殼的材料蓋家；死掉後殼留在海底，材料離開海水 | OK | Gale；NOAA whysalty | "remove calcium or silicon from sea water to make calcium carbonate shells"；"buried in the sediment and thus removed from sea water for many millions of years" |
| p099–p100 | 河水帶來的很多正是做殼的材料，被拿走得比鹽快很多 | OK | Gale 表 1、表 2 | 河水以 HCO₃⁻、Ca²⁺ 為主；Ca 約 1 × 10⁶ 年，Na 80 × 10⁶ 年 |
| p101–p103 | 做殼用不到廚房那種鹽，所以留在海裡最多的就是它 | OK | NOAA whysalty；Gale | "Many of the dissolved ions are used by organisms … Others are not removed, so their concentrations increase over time" |
| p104–p105 | 一百份裡大約八十五份是廚房那種鹽的材料 | OK | NOAA whysalty | "chloride and sodium. Together, they make up around 85 percent of all dissolved ions"（USGS 寫 "over 90%"，按顆數；Gale 按重量約 86%） |
| p106–p109 | 鍋底的熱泉；海水鑽進石頭縫被煮熱再噴出；一千到兩千萬年整個鑽過一次 | OK | NOAA whysalty；USGS；Gale | "Ocean water seeps into cracks in the seafloor and is heated by magma"；USGS "could circulate through hydrothermal vent systems every 10-20 million years"，台詞有「科學家估計」 |
| p110–p113 | 熱泉冒出一些鹽；鹽山說對一點點；帶出金屬，也把東西留在石頭裡 | OK（附註） | NOAA whysalty；USGS；Gale | 見第二節 |
| p114–p115 | 廚房那種鹽要從鍋邊出去 | FIX（F01） | Gale；NOAA riversnotsalty | 見第一節 |
| p116–p117 | 有些海灣跟大海隔開，海水被曬乾，留下厚鹽層埋進地底 | OK（附註） | Gale；Wikipedia Evaporite | 見第二節 |
| p118–p120 | 海也一直在收；只是收得很慢 | FIX（F02） | NOAA riversnotsalty；Gale | 見第一節 |
| p121–p124 | 出口在天上與鍋底鍋邊；一邊加一邊結鍋巴；大概已經沒有再越變越鹹 | OK | NOAA riversnotsalty；Gale | 見第二節 |
| p125–p128 | 全世界的海都一樣鹹嗎；平均一公斤大約三十五公克 | OK | NOAA whysalty；NASA A Measure of Salt；Gale | "The average salinity is about 35 parts per thousand"；NASA "30 to 40 grams per kilogram, with 35 grams being the average" |
| p129–p134 | 海連在一起，但各地的火和水不一樣；猜台灣 | OK（比喻） | NOAA whysalty | "salinity varies with temperature, evaporation, and precipitation" |
| p135–p140 | 很熱的紅海；幾乎都是沙漠、少雨、幾乎沒有河；比平均多大約五公克 | OK | Wikipedia Red Sea；NASA | 見第二節；"average of 40 ‰"，"Average salinity for the world's seawater is ~35 ‰"，差 5 |
| p141–p146 | 波羅的海很多河、雨比曬走的多；最北邊一公斤只有幾公克鹽 | OK | Wikipedia Baltic Sea；HELCOM | 見第二節；HELCOM "1–2 PSU in the northernmost Bothnian Bay" |
| p147–p149 | 那條河流進海的地方，附近的海水也會淡一點 | OK | NASA A Measure of Salt | "Rivers such as the Amazon carry tremendous amounts of fresh runoff from land and spread plumes far into the sea" |
| p150–p155 | 兩種都不太像；台灣附近平常一公斤大約三十四公克多；夏天雨多、河水多，岸邊會淡一點 | OK（量測值） | 水產試驗所 107 年度報告 | 春季「33.72~34.78psu」、冬季「32.19~34.70psu」、夏季「31.35~34.35psu」；「夏季降雨量高河川淡水輸入較多，在較近岸測站有低鹽水出現」 |
| p156–p158 | 死海是湖，水流不出去只能被熬，比海水鹹快十倍 | OK | Wikipedia Dead Sea | 見第二節 |
| p159–p161 | 每片海鹹不鹹看加多少水、熬走多少水；下次去海邊猜猜看 | OK | NOAA whysalty | 與 "evaporation, and precipitation" 一致 |
| p162–p163 | 我覺得海最厲害的是一邊收鹽、一邊送水上天 | OK（意見；字數附註） | — | 有「我覺得」 |
| p164–p167 | 小問整理：河帶一點點鹽進海；太陽只把水熬走；海底和海邊再慢慢把鹽收走 | p164–p166 OK；p167 FIX（F03） | NOAA；Gale | 見第一節 |
| p168–p169 | 完全正確；那口海水別拿來解渴；身體要用更多的水排鹽，越喝越渴 | OK | NOAA drinksw | "to get rid of all the excess salt taken in by drinking seawater, you have to urinate more water than you drank. Eventually, you die of dehydration even as you become thirstier." |
| p170–p171 | 那口鹹是好幾千萬年留下來的味道 | OK（詩意說法） | LibreTexts；Gale | 見第二節 |
| p172–p175 | 原來如此；留言與訂閱 | OK | — | 片尾 |
| youtube.title | 河水一直流進海裡，海為什麼還是鹹？｜原來如此事務所 | OK | — | 問題 |
| youtube.description | 河從石頭帶走一點點鹽；太陽只搬得走水；貝殼、泥沙、熱泉、古老鹽層把海水裡的東西收走；紅海特別鹹、波羅的海淡淡的；AI 插圖聲明；不要喝海水 | OK | 同上各段 | 已改成「把海水裡的東西收走」，涵蓋熱泉收走的鎂與硫酸根，沒有說過頭 |
| thumbnail.headline | 河水一直倒／海還是鹹 | OK | NOAA riversnotsalty | 問題的濃縮 |
| thumbnail.sub | 太陽只搬走水，搬不走鹽 | OK | Gale | "the water … evaporates but the dissolved salts do not" |
