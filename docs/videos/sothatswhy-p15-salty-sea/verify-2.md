# 查核報告 2（sothatswhy-p15-salty-sea）

- 查核者：Claude（第二輪獨立查核代理，未參與撰稿與第一輪）
- 日期：2026-11-07
- 方法：逐句讀第二版 `video.json` 的 191 句台詞（現行 id p001–p191），加上 YouTube 標題、說明與縮圖 headline／sub。`claims.md` 的行號是第一版的，這次一律以台詞文字對照。不沿用 claims.md 或 verify-1 的引文，用 curl（User-Agent `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`）重新抓下每個來源，轉成文字後讀原文：NOAA whysalty／riversnotsalty／drinksw、USGS why-ocean-salty／saline-water-and-salinity／how-much-water-there-earth、NASA Earth Observatory A Measure of Salt／A Global Accounting of Earth's Rivers、LibreTexts 8.9 Residence Time、Gale〈Ocean Chemical Processes〉（encyclopedia.com）、HELCOM Salinity（archive.iwlearn.org）、觀光署七股鹽山、水產試驗所 107 年度監測報告 PDF（pdftotext），以及 Wikipedia Dead Sea、Red Sea、Baltic Sea、中文維基〈鹽田〉、英文維基 Salt evaporation pond（raw wikitext）。全部回 200。
- 沒有開的來源：NSIDC Science of sea ice。第二版已經拿掉海冰與極地的句子，沒有任何台詞再用到它。
- 字數：另外跑了一次長度檢查，所長台詞全部 ≤ 25 字、小問台詞只有 p047「海不是應該越來越滿、越來越淡嗎？」16 字（含標點；不含標點 14 字），其餘都 ≤ 15 字。這不是事實問題，列出來給撰稿參考。
- 對來源清單的建議（不是台詞的 FIX）：
  - `video.json` 的 `sources` 沒有 Wikipedia Red Sea 與 Wikipedia Baltic Sea，但 p147–p148（沙漠、少雨、幾乎沒有河）、p151（平均 40‰，多大約五公克）與 p154（降水減蒸發為正）只有這兩頁能直接支撐。建議補進 `sources` 與 claims.md〈來源〉。中文維基〈鹽田〉（p076 的曬鹽方法）也建議一起補。
  - `sources` 裡的 NSIDC 已經沒有台詞用到，可以留著也可以拿掉；claims.md C21 仍以 NSIDC 為第一個來源，跟現行稿子不符。
  - claims.md C19 寫「紅海……查核時請確認一個來源」：Wikipedia Red Sea 寫 "no significant rivers or streams drain into the sea"，可結案。C20 的 F07 依據（Wikipedia Baltic Sea）也應列進〈來源〉。
- 結論統計（台詞 191 句）：OK 191、FIX 0、NOT FOUND 0。標題、說明、縮圖 headline、縮圖 sub 共 4 項：OK 4。verify-1 的 F01–F07 七項全部已套用，套用後的句子也都對得上來源。

## 一、要改的地方與理由

這一輪沒有必須改的句子。下面幾句是「可以更好、但不改也不算錯」，只列在第三節的附註裡，不計入 FIX：p011（「從來沒有變淡過」是孩子嘗得出來的尺度）、p106–p107（因果只講了生物這一半）、p119–p120（「很久很久以前」與「一直在收」的時間感）、p132（「才停下來」）、p147（「都是沙漠」）、youtube.description（「怎麼把鹽收走」）。

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| — | — | （無） | — | — |

## 二、verify-1 的 F01–F07 確認

| # | verify-1 建議 | 現行稿子 | 結論 | 依據 |
| --- | --- | --- | --- | --- |
| F01 | 「海裡的鹽，大部分是從陸地來的。」 | p014 同句 | 已套用，OK | NOAA whysalty "Rocks on land are the major source of salts dissolved in seawater."；同頁 "Salt domes also contribute … found underground and undersea"，所以 p117「說對了一點點」接得上 |
| F02 | 「對。牠們死掉以後，殼就留在海底，」 | p100 同句 | 已套用，OK | 貝殼與珊瑚都說得通；Gale 殼 "buried in the sediment and thus removed from sea water for many millions of years" |
| F03 | 「被拿走得比鹽快很多。」 | p104 同句 | 已套用，OK | Gale 表 2：Ca²⁺ 滯留約 1 × 10⁶ 年，Na⁺ 80 × 10⁶ 年；LibreTexts 氯約 8,700 萬年 |
| F04 | 「科學家估計，全世界的海水大約一千到兩千萬年，」 | p113 同句；p114 照留 | 已套用，OK | USGS "could circulate through hydrothermal vent systems every 10-20 million years"；Gale "a reasonable estimate of once every 10 million years" |
| F05 | 「很久很久以前，有些跟大海隔開的海水被曬乾了，」 | p120 同句；p121 照留 | 已套用，OK | Gale "Evaporation of isolated bodies of sea water accounts for removal of large amounts of salt … Salt deposits occur through the geologic record as layers of gypsum, rock salt" |
| F06 | p143「海洋學家認為，現在的海，」＋ p144「大概已經沒有再越變越鹹了。」 | 合成一句 p129「海洋學家認為，現在的海，大概已經沒有再越變越鹹了。」（25 字） | 已套用，OK | NOAA riversnotsalty 兩個 "probably"："the ocean today probably has a balanced salt input and output (and so the ocean is no longer getting saltier)"。「認為」「大概」都在 |
| F07 | p165「北邊的波羅的海剛好相反，」＋ p166「很多河流進來，下的雨也比曬走的多。」 | p153、p154 同句 | 已套用，OK | Wikipedia Baltic Sea "More than 250 streams drain a basin …"、"precipitation less evaporation, which is positive"；HELCOM "fresh water from rivers and rainfall"。「天氣涼」已拿掉 |

## 三、逐段核對（現行 id）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p009 | 小問海邊喝到海水很鹹；所長也喝過；河一直流進海、河水淡，海怎麼沒被沖淡 | OK | — | 開場、角色玩笑與問題 |
| p010–p011 | 全世界的河每天把好多淡水倒進海；你嘗到的海從來沒有變淡過 | OK（附註） | NASA Global Accounting of Earth's Rivers | 全球入海年流量 "averaged 37,411 cubic kilometers … per year"。p011 的「從來沒有變淡過」限定在「你去海邊嘗到的」，是孩子嘗得出來的尺度；後面 p158–p159、p165–p166 講河口與夏天近岸會淡一點，屬於嘗不出來的小差異，不算自相矛盾 |
| p012–p013 | 小問猜海底有鹽山一直冒鹽 | OK（錯猜） | — | 由 p014 修正 |
| p014 | 海裡的鹽大部分是從陸地來的 | OK（F01） | NOAA whysalty；USGS why-ocean-salty | "Rocks on land are the major source"；USGS "Salt in the ocean comes from rocks on land." 用「大部分」，沒有否定海底來源 |
| p015 | 海底真的藏著一個祕密 | OK | — | 鋪陳，p090–p091 收回 |
| p016–p019 | 河水真的一點鹽都沒有嗎；把海想成一鍋一直在熬的湯 | OK（比喻） | Gale | 方向與 "the water added to the ocean evaporates but the dissolved salts do not" 一致 |
| p020–p023 | 河水偷偷帶著鹽，少到嘗不出來 | OK | USGS saline-water；NOAA riversnotsalty | 河水含溶解鹽類（NOAA "rivers carry … dissolved salts"）。附註：p020「你說河水是淡的？」與 p016 重複，屬於寫作，不是事實問題 |
| p024–p027 | 鹽從山上的石頭來；雨帶一點點酸，慢慢啃石頭 | OK | NOAA whysalty；USGS | "Rainwater that falls on land is slightly acidic, so it erodes rocks."；USGS "slightly acidic due to carbonic acid"。「啃」「不是一天熬好的」是比喻 |
| p028–p033 | 石頭裡的小東西溶進水裡，跟著河流下山；像糖溶在水裡看不見，但真的在 | OK | NOAA whysalty；USGS | "This releases ions that are carried away to streams and rivers"；USGS "carries salts and minerals along in a dissolved state as ions"。糖只比「看不見」 |
| p034–p036 | 河水一直被新的雨水換掉，鹽來不及變多 | OK | NOAA riversnotsalty | "Rain replenishes freshwater in rivers and streams, so they don't taste salty." 後半是白話推論 |
| p037–p038 | 淡水的鹽連海水的三十分之一都不到 | OK（定義） | USGS saline-water-and-salinity | "Fresh water - Less than 1,000 ppm"；"ocean water contains about 35,000 ppm of salt"。1／35，說的是「我們叫淡水的那種水」 |
| p039–p045 | 全世界的河一年大約帶四十億公噸溶掉的鹽進海 | OK | NOAA riversnotsalty | "rivers carry an estimated four billion tons of dissolved salts to the ocean annually"。tons 未註明英制或公制，「大約」涵蓋 |
| p046–p051 | 河一直倒，海沒有滿；空的海光靠河倒大約三萬多年就滿 | OK（自行換算） | USGS how-much-water；NASA rivers | 1,338,000,000 km³ ÷ 37,411 km³／年 ≈ 35,765 年。用「如果」「光靠」「大約」，是假設題 |
| p052–p058 | 水的出口在天上；太陽曬成水氣，成雲、下雨、回河、再進海 | OK | USGS how-much-water（水循環）；NOAA riversnotsalty | USGS "the oceans provide evaporated water to the water cycle"；"rain fell to the Earth and ran over the land"。「雲飄到山上下成雨」是簡化 |
| p059–p062 | 鹽沒有跟著飛；太陽只搬得動水；水曬走鹽留下 | OK | Gale | "the water added to the ocean evaporates but the dissolved salts do not" |
| p063–p065 | 一小碟鹽水放太陽下幾天，留下一圈白鹽 | OK | Gale；中文維基〈鹽田〉 | 蒸發後溶質留下；〈鹽田〉「利用太陽能蒸發鹵水中的水分，以取得鹽的結晶」。不用火、不用喝，安全 |
| p066–p070 | 像熬湯越熬越鹹；河水是加進去帶一點鹽的水；太陽是爐火 | OK（比喻） | Gale；NOAA riversnotsalty | 與前文一致 |
| p071–p072 | 雨不是鹹的；你淋到的雨幾乎就是被太陽熬出來的淡水 | OK（附註：簡化） | Gale；NOAA riversnotsalty；USGS how-much-water | 蒸發只帶走水（Gale），雨是淡水（NOAA "Rain replenishes freshwater"），海洋提供水循環的蒸發水（USGS）。「幾乎」涵蓋兩件事：雨裡仍有極少量鹽（Gale 提到 "sea-spray residues" 氣溶膠會隨雨落下），以及陸地蒸發與植物蒸散也貢獻水氣（USGS "evaporate or transpire"）。「熬」指太陽讓水蒸發，比喻一致 |
| p073–p074 | 台灣以前用太陽曬海水做鹽 | OK | 觀光署七股鹽山 | 「結束臺灣338年曬鹽歷史」，所以「以前」正確 |
| p075 | 台南七股曾經是台灣最大的曬鹽場 | OK | 觀光署七股鹽山 | 原文「七股鹽場過去是臺灣最大的曬鹽場」，「曾經」對上「過去」；2002 年廢曬，第二版不唸年份，沒有問題 |
| p076 | 海水引進鹽田，曬乾以後剩下白白的鹽 | OK（附註：簡化） | 中文維基〈鹽田〉；英文維基 Salt evaporation pond | "seawater or brine is fed into artificially created ponds from which water is drawn out by evaporation"。實際鹽田是曬到鹽結晶後收鹽，不一定整池曬乾，對孩子的說法可以 |
| p077–p078 | 廚房的鹽也有海裡來的；曬出來的海鹽就是海裡留下的 | OK | 中文維基〈鹽田〉；Gale | 「也有」沒說全部（Gale：蒸發岩也 "mined for table salt"） |
| p079–p081 | 海每天被熬，最後不就變成一大片鹽巴；好像會 | OK | — | 問題與鋪陳 |
| p082–p084 | 一滴水在海裡平均待三千年左右就被太陽熬走 | OK | LibreTexts 8.9 | "a water molecule spends 3,100 years floating around in the world ocean reservoir before it's evaporated" |
| p085 | 鹽卻可以在湯裡泡上幾千萬年 | OK | LibreTexts 8.9；Gale 表 2 | 氯 "about 87 million years"、鈉 "about 55 million years"；Gale 鈉 80 × 10⁶ 年。海鹽大約八成六是鈉與氯（Gale 表 2：Cl⁻ 19.353＋Na⁺ 10.781 g／kg，S = 35），所以拿鈉、氯代表「鹽」可以；「可以」也讓句子不必涵蓋滯留較短的鈣（約一百萬年） |
| p086–p087 | 三千年好久；跟鹽比，水只是在鍋裡轉一圈 | OK（比喻） | LibreTexts；Gale | 3,000 年對幾千萬年，相差上萬倍，「轉一圈」是比喻，沒有說成具體的循環次數 |
| p088–p091 | 鹽也不是永遠留在湯裡；鹽的出口在海底；就是開頭說的祕密 | OK | NOAA riversnotsalty；Gale | "About the same tonnage of salt … probably is deposited as sediment on the ocean bottom" |
| p092–p096 | 溶著的一些東西慢慢沉下去，跟泥沙變成一層層泥和石頭；鍋巴 | OK | Gale；NOAA riversnotsalty | Gale 顆粒 "adsorb dissolved material from sea water and cause them to be buried in ocean floor sediments, thus removed from the ocean"。用「一些東西」，沒有說過頭 |
| p097–p099 | 貝殼和珊瑚拿水裡做殼的材料蓋家；家是用海水蓋的 | OK | Gale；NOAA whysalty | Gale "remove calcium or silicon from sea water to make calcium carbonate shells"；NOAA "Many of the dissolved ions are used by organisms in the ocean and are removed from the water." p099 小問的「用海水蓋的」是孩子的說法，p098 已經說清楚是「水裡做殼的材料」 |
| p100–p102 | 死掉以後殼留在海底，材料離開海水；貝殼在幫海搬東西 | OK（F02） | Gale | 殼 "buried in the sediment and thus removed from sea water for many millions of years" |
| p103 | 河水帶來的有很多正是做殼的材料 | OK | Gale 表 1 | 河水最多的兩種離子是 HCO₃⁻ 0.86 與 Ca²⁺ 0.33 mM／L（Na⁺ 0.23、Cl⁻ 0.16） |
| p104 | 被拿走得比鹽快很多 | OK（F03） | Gale 表 2；LibreTexts | Ca²⁺ 約 1 × 10⁶ 年，Na⁺ 80 × 10⁶ 年、氯約 8,700 萬年，差幾十倍 |
| p105–p107 | 為什麼不把鹽也拿走；因為做殼用不到廚房那種鹽；所以留在海裡最多的就是它 | OK（附註） | NOAA whysalty；USGS；Gale | 殼是碳酸鈣或矽（Gale），用不到鈉與氯，p106 正面回答了 p105 的問題。p107 的「所以」跟 NOAA 的因果一模一樣："Many of the dissolved ions are used by organisms … removed from the water. Others are not removed, so their concentrations increase over time."（USGS 同義）。完整的原因還包括鈉、氯本身「很好溶、不容易反應」（Gale "Elements with long residence times … tend to be very soluble in sea water"），台詞只講了生物這一半，但有官方頁面的同一個因果撐著，不算錯 |
| p108–p109 | 溶著的小東西一百份裡大約八十五份是廚房那種鹽的材料 | OK | NOAA whysalty；Gale 表 2 | NOAA "chloride and sodium. Together, they make up around 85 percent of all dissolved ions"。用 Gale 表 2 自行核算：按重量 (19.353＋10.781)／35 ≈ 86%；按顆數約九成（USGS "over 90%"）。「一百份裡大約八十五份」跟著 NOAA，落在兩種算法之間，可以。「廚房那種鹽的材料」指鈉與氯，說法正確 |
| p110–p112 | 廚房那種鹽要怎麼出去；先看鍋底的熱泉；海水鑽進石頭縫被煮熱再噴出 | OK | NOAA whysalty；USGS | "Ocean water seeps into cracks in the seafloor and is heated by magma … released through vents in the seafloor" |
| p113–p115 | 科學家估計全世界的海水大約一千到兩千萬年從熱泉的石頭縫整個鑽過一次 | OK（F04） | USGS；Gale | 見第二節 F04 |
| p116–p118 | 海底真的在冒東西；鹽山說對一點點；熱泉帶出東西也把一些東西留在石頭裡 | OK | NOAA whysalty；USGS；Gale | NOAA 熱泉與海底鹽丘都 "contribute to the ocean's saltiness"；USGS "some of the dissolved salts react with the rock and are removed from seawater"；Gale "loses all its O₂ and all its Mg … gains Ca, Si, Fe, and Mn"。p118 沒有說熱泉收走的是廚房那種鹽，跟 p119 的「至於」分得清楚 |
| p119 | 至於廚房那種鹽，它有一條很慢的出口 | OK（附註） | Gale；LibreTexts | 「很慢」對上鈉約 8,000 萬年、氯約 8,700 萬年的滯留時間。「一條」是「有一條」，沒有說「只有一條」。claims.md 寫明不說它是最大的出口，台詞也沒有說 |
| p120–p121 | 很久很久以前，有些跟大海隔開的海水被曬乾，留下厚厚的鹽層埋進地底下 | OK（F05，附註） | Gale；Wikipedia Red Sea；Wikipedia Dead Sea | Gale "Evaporation of isolated bodies of sea water accounts for removal of large amounts of salt … Salt deposits occur through the geologic record as layers of gypsum, rock salt"；Wikipedia Red Sea 也記載紅海曾整片蒸乾成鹽底。附註：Gale 說鹽層出現在整個地質紀錄裡，不只「很久很久以前」；台詞挑了一個孩子聽得懂的例子，沒有說「現在沒有」，可以 |
| p122–p127 | 河送進來的鹽海底也一直在收；水的出口在天上、鹽的出口在鍋底；一邊加一邊結鍋巴，湯一直差不多一樣鹹 | OK | NOAA riversnotsalty；Gale | "About the same tonnage of salt … probably is deposited as sediment on the ocean bottom … yearly gains may offset yearly losses"；Gale "steady state — that is, operating so that the input of salt equals the output"。「差不多」恰當。p123 是小問的問句，p124「對」承接的是 NOAA 的「沉積在海床」，這裡的「鹽」是廣義的溶解鹽類 |
| p128–p129 | 海會不會變成一大片鹽巴；海洋學家認為現在的海大概已經沒有再越變越鹹 | OK（F06） | NOAA riversnotsalty | 見第二節 F06 |
| p130–p131 | 剛出現的海可能只有一點點鹹 | OK | NOAA riversnotsalty | "In the beginning, the primeval seas were probably only slightly salty."，「可能」對上 probably |
| p132 | 後來越來越鹹，一直到進來和出去差不多，才停下來 | OK（附註：簡化） | NOAA riversnotsalty；Gale | NOAA "over time … the ocean has become saltier"；Gale "sea water must have had roughly the same chemistry over hundreds of millions of years … steady state"。前一句 p129 有「大概」、p131 有「可能」帶著，這句是兩者之間的簡化。Gale 結論段提到主要元素的比例在七億年間可能變過約兩倍，那是成分比例，不是總鹹度，不影響這句 |
| p133–p137 | 海裡的鹽全部鋪在陸地上大約四十層樓厚 | OK | USGS why-ocean-salty | "it would form a layer more than 500 feet (166 meters) thick, about the height of a 40-story office building"。不唸公尺，避開頁面 500 英尺與 166 公尺不一致 |
| p138–p141 | 全世界的海不太一樣；平均一公斤大約三十五公克 | OK | NOAA whysalty；NASA A Measure of Salt；Gale | "The average salinity is about 35 parts per thousand"；NASA "30 to 40 grams per kilogram, with 35 grams being the average"；Gale "about 35 grams per kilogram" |
| p142–p145 | 海連在一起，但各地的火和水不一樣；有的熬得兇、有的一直加水 | OK（比喻） | NOAA whysalty | "salinity varies with temperature, evaporation, and precipitation" |
| p146 | 先猜猜台灣旁邊的海比較像哪一種 | OK | — | 問題，p162 回答 |
| p147–p148 | 紅海旁邊都是沙漠、太陽很大、很少下雨、幾乎沒有河流進來 | OK（附註） | Wikipedia Red Sea | "between arid land, desert and semi-desert"；"rainfall … extremely low, averaging 60 mm per year"；"high evaporation and low precipitation; no significant rivers or streams drain into the sea"。附註：原文是乾燥地、沙漠與半沙漠，「都是沙漠」對孩子是可以接受的概括；如果想更貼原文，可以說「旁邊幾乎都是沙漠」（非必要） |
| p149–p151 | 爐火開大又不加水；紅海比較鹹，每公斤比平均多大約五公克 | OK | Wikipedia Red Sea；NASA A Measure of Salt | "ranges from between ~36 ‰ in the southern part and 41 ‰ in the northern part … with an average of 40 ‰"，40 − 35 = 5；NASA "strong evaporation and other processes do make the Red and Mediterranean Seas saltier" |
| p152–p155 | 波羅的海剛好相反，很多河流進來，下的雨也比曬走的多；一直加水湯就淡了 | OK（F07） | Wikipedia Baltic Sea；HELCOM | 見第二節 F07 |
| p156–p157 | 最北邊的海水一公斤只有幾公克鹽，嘗起來淡淡的 | OK | HELCOM；Wikipedia Baltic Sea | "1–2 PSU in the northernmost Bothnian Bay and the easternmost Gulf of Finland"；Wikipedia 波的尼亞灣 "around 0.3%"。「幾公克」涵蓋 1–3。沒有叫孩子去喝 |
| p158–p160 | 那條河流進海的地方，附近的海水也會淡一點 | OK | NASA A Measure of Salt | "Rivers such as the Amazon carry tremendous amounts of fresh runoff from land and spread plumes far into the sea."；"runoff from rivers … does make water fresher" |
| p161–p164 | 答案是兩種都不太像；台灣附近的海水平常一公斤大約三十四公克多，跟平均差不多 | OK（量測值） | 水產試驗所 107 年度報告 | 冬季「鹽度介於32.19~34.70psu」、春季「33.72~34.78psu」、夏季「31.35~34.35psu」。各季上緣都在 34 多，受黑潮影響的外海測站是這個值；跟平均 35 只差不到 1，所以「兩種都不太像」「跟平均差不多」成立。psu 與每公斤公克數相差不到百分之一，對孩子可以直接說「公克」 |
| p165–p166 | 夏天雨多、河水多，靠近岸邊的海水就會淡一點 | OK | 水產試驗所 107 年度報告 | 「夏季降雨量高河川淡水輸入較多，在較近岸測站有低鹽水出現」，幾乎是原文直譯 |
| p167–p171 | 死海是湖，水流不出去只能被太陽熬走；湖水比海水鹹快十倍；人躺上去會浮起來 | OK | Wikipedia Dead Sea | "an endorheic lake, meaning there are no outlet streams"；"342 g/kg, or 34.2% (in 2011) … 9.6 times as salty as the ocean"，另一處 "fluctuates around 31.5%"（約九倍），「快十倍」兩者都涵蓋；"Anyone can easily float in the Dead Sea" |
| p172–p177 | 小問想去浮；每片海鹹不鹹看加進多少水、熬走多少水；下次去海邊猜猜看 | OK | NOAA whysalty | 與 "varies with temperature, evaporation, and precipitation" 一致；p172 只是願望 |
| p178–p179 | 我覺得海最厲害的是一邊收一邊送 | OK（意見） | — | 有「我覺得」 |
| p180–p183 | 小問整理：河帶一點點鹽進海；太陽只把水熬走；海底再慢慢把鹽收走 | OK | NOAA whysalty／riversnotsalty；Gale | 與前文一致 |
| p184–p185 | 那口海水別拿來解渴；身體要用更多的水排鹽，越喝越渴 | OK | NOAA drinksw | "to get rid of all the excess salt taken in by drinking seawater, you have to urinate more water than you drank. Eventually, you die of dehydration even as you become thirstier." 安全叮嚀到位 |
| p186–p187 | 那口鹹是好幾千萬年留下來的味道 | OK（詩意說法） | LibreTexts 8.9；Gale | 鈉、氯滯留 5,500 萬到 8,700 萬年。滯留時間是平均值，海水裡鈉、氯的平均停留時間就在這個範圍，所以拿「好幾千萬年」形容那一口的味道站得住 |
| p188–p191 | 原來如此；留言與訂閱 | OK | — | 片尾 |
| youtube.title | 河水一直流進海裡，海為什麼還是鹹？｜原來如此事務所 | OK | — | 問題 |
| youtube.description | 河從石頭帶走一點點鹽；太陽只搬得走水；貝殼、泥沙、熱泉、古老鹽層把鹽收走；紅海特別鹹、波羅的海淡淡的；AI 插圖聲明；不要喝海水 | OK（附註） | 同上各段 | 「鹽」在這裡是廣義的溶解鹽類（NOAA、USGS 都這樣用），不算錯。正片 p106 已經分出「廚房那種鹽」，若想用詞一致，可把「怎麼把鹽收走」改成「怎麼把海水裡的東西收走」（非必要，verify-1 也提過）。「潛到海底」後面接「古老的鹽層」：鹽層是「埋進地底下」，不一定在海底，屬於概括，可以 |
| thumbnail.headline | 河水一直倒／海還是鹹 | OK | NOAA riversnotsalty | 問題的濃縮 |
| thumbnail.sub | 太陽只搬走水，搬不走鹽 | OK | Gale | "the water … evaporates but the dissolved salts do not" |
