# 查核報告 1（sothatswhy-p02-cloud-rain）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-03
- 方法：逐句讀 `video.json` 的台詞、每張卡片的 `data`、YouTube 標題、說明與縮圖文字，對照 `claims.md` 的 C01–C31（行號以實際台詞 id 為準，與 claims.md 的約略行號不同）。每一條都打開一手或官方／教育來源核對原文（NOAA JetStream、NWS 詞彙、USGS 水科學學校、NASA GPM／Earth Observatory／Glenn、UCAR、WMO 國際雲圖、中央氣象署、大學教科書與課程頁）。需要計算的數字（雲重、空氣重、終端速度、落地時間）用來源給的公式或數值自行重算。
- 打不開的來源：AMS Glossary of Meteorology（glossary.ametsoc.org 回 403，web.archive.org 也無法取用），UCAR「How much does a cloud weigh」（scied.ucar.edu 該頁 404），NASA GPM 降水 FAQ（503）。這三個都沒有列入下方來源，凡是原本預期引用它們的主張，改用其他已打開的來源。**卡片上寫「AMS 氣象學詞彙」「UCAR／NCAR 估算方式」「NOAA JetStream：降水的形成」的出處標示，查核者沒能打開對應頁面，建議改標（見建議修改）。**
- 結論統計（C01–C31）：OK 27、FIX 4、CUT 0。另外標題、縮圖、卡片與 1 句台詞有 9 處額外建議修改（E01–E09），沒有需要整句刪除的內容。

| # | 主張 | 行 | 結論 | 來源（網址） | 依據摘要 |
| --- | --- | --- | --- | --- | --- |
| C01 | 真正的水蒸氣看不見；壺嘴外白霧是凝結的小水滴 | p015–p018 | OK | https://www.noaa.gov/education/multimedia/video/cooking-up-storm-atmospheric-science-in-your-kitchen ；https://www.usgs.gov/water-science-school/science/condensation-and-water-cycle | NOAA："steam is water vapor — water in the form of a gas — which is not visible"；"we can't see it until we drop the temperature"。USGS：空氣裡充滿水氣 "although most of the time we can't see it" |
| C02 | 雲是很多很小的水滴，有時是小冰晶 | p019；卡片 vapour-vs-cloud | OK | https://www.noaa.gov/jetstream/clouds | 雲由 "minute particles of water and/or ice" 組成 |
| C03 | 被曬熱的空氣比旁邊輕，會往上浮 | p012、p021 | OK | https://www.noaa.gov/jetstream/thunderstorms/ingredients-for-thunderstorm | "As the Sun heats the Earth's surface, some heat is transferred to the air, which creates different air densities"；"The propensity for air to rise increases with decreasing density" |
| C04 | 空氣上升、氣壓變小而膨脹，膨脹就變冷 | p024 | OK | https://www.noaa.gov/jetstream/clouds/how-clouds-form | 上升氣塊因氣壓降低而膨脹，"This expansion results in cooling" |
| C05 | 未凝結時每公里約冷 10°C（乾絕熱 9.8°C/km） | p025；卡片 lapse-rate | OK | https://forecast.weather.gov/glossary.php?word=dry%20adiabatic%20lapse%20rate ；https://www.noaa.gov/jetstream/clouds/how-clouds-form | NWS："5.5°F per 1000 ft or 9.8°C per km"；NOAA 同值，稱 dry lapse rate。「約 10 度」為合理取整 |
| C06 | 水氣在灰塵、海鹽、煙等小顆粒上凝結 | p029–p030 | OK | https://www.usgs.gov/water-science-school/science/condensation-and-water-cycle ；https://www.noaa.gov/jetstream/clouds/how-clouds-form | USGS："tiny particles of dust, salt, and smoke in the air"。NOAA：煙、海浪飛沫、風吹起的土壤 |
| C07 | 積雲平底的高度是空氣冷到開始凝結的高度 | p031 | OK | https://www.noaa.gov/jetstream/clouds/four-core-types-of-clouds ；https://forecast.weather.gov/glossary.php?word=lifting%20condensation%20level | NOAA："The base of cumulus clouds are generally flat and occurs at the altitude where the moisture in rising air condenses." |
| C08 | 1 立方公里積雲、每立方公尺約 0.5 公克、共約 500 公噸 | p035–p039；卡片 cloud-weight；標題、說明、縮圖 | OK（台詞）；標題與卡片出處需改，見 E01、E02、E05 | https://www.usgs.gov/water-science-school/science/how-much-does-a-cloud-weigh | USGS："A 1 cubic kilometer (km3) cloud contains 1 billion cubic meters"；"density of about 0.5 gram per cubic meter"；"about 500,000 kilograms or 1.1 million pounds"。注意：1 km³ 與 0.5 g/m³ 都是**假設**，晴天積雲常更小，正在長高的積雲含水量可到 1 g/m³ 以上，所以「約 500 公噸」只是一朵假想積雲的數量級。台詞已用「假設」「大概」，可以；標題沒有「約」，要補 |
| C09 | 約等於一百頭大象 | p040 | OK（數量級） | https://ielc.libguides.com/sdzg/factsheets/african_elephant/summary | 聖地牙哥動物園資料：草原象公象平均 6,000 kg、母象平均 2,800 kg。500 公噸÷100＝每頭 5 公噸，落在公母之間；按母象算約 180 頭。台詞用「差不多」，可接受 |
| C10 | 同一立方公里空氣約 100 萬公噸；水占約兩千分之一 | p043；卡片 air-weight | OK | https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html | 用 NASA Glenn 對流層公式 T＝15.04－0.00649h、p＝101.29[(T+273.1)/288.08]^5.256、ρ＝p/[0.2869(T+273.1)] 算：1.5 公里高 ρ≈1.06 kg/m³，1 km³ 約 106 萬公噸；500 公噸÷106 萬公噸≈1/2100，「約兩千分之一」成立 |
| C11 | 典型雲滴直徑約 0.02 公釐，比頭髮細好幾倍 | p046；卡片 droplet-size | OK | https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/ ；https://www.epa.gov/pm-pollution/particulate-matter-pm-basics | 夏威夷大學教科書："The average cloud droplet is very small with an average diameter of about 20 micrometers"。EPA："The average human hair is about 70 micrometers in diameter"→約 3.5 倍，「好幾倍」可以（最細的金髮約 17 µm，所以只能說一般頭髮） |
| C12 | 雲滴在靜止空氣中每秒約落 1 公分 | p052；卡片 fall-speed 左 | OK（卡片出處需改，見 E06） | https://atmos.uw.edu/academics/classes/2003Q2/101/lect21_overheads.pdf ；https://geo.libretexts.org/Bookshelves/Meteorology_and_Climate_Science/Atmospheric_Processes_and_Phenomena/07%3A_Precipitation_Processes/7.02%3A_Cloud_Droplets | 華盛頓大學 ATMS 101 表："20 microns 0.01 m s-1 (cloud droplet)"。LibreTexts 斯托克斯公式 w＝1.19×10⁸·r²，r＝10 µm 得約 1.2 cm/s |
| C13 | 照此速度從 1 公里高落地要超過一天；半路會蒸發 | p054–p055 | OK | https://geo.libretexts.org/Bookshelves/Meteorology_and_Climate_Science/Atmospheric_Processes_and_Phenomena/07%3A_Precipitation_Processes/7.02%3A_Cloud_Droplets | 1000 m÷0.01 m/s＝10 萬秒≈28 小時。教科書："it takes hours, if not days, for a cloud droplet to fall from even low altitudes" |
| C14 | 正在長高的積雲裡上升氣流每秒可達好幾公尺 | p058–p059 | OK | https://courses.ems.psu.edu/meteo3/node/2024 ；https://courses.ems.psu.edu/meteo3/node/2231 | 賓州州立大學：積雲階段上升氣流 "accelerate to roughly 10 meters per second"；晴天積雲 "less than 1 meter per second"；積雨雲 "can reach near 50 meters per second" |
| C15 | 常見雨滴約 2 公釐，直徑約為雲滴的 100 倍 | p063 | OK | https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/ | "The average raindrop has a diameter of 2 mm"；雲滴平均 20 µm→100 倍 |
| C16 | 一顆雨滴約需 100 萬顆雲滴（數量級） | p066–p068；卡片 hundred-cubed；說明 | OK | https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/ ；https://www.usgs.gov/water-science-school/science/precipitation-and-water-cycle | 教科書："it takes 1 million cloud droplets (10 μm radius) to combine together to make one single raindrop"。USGS："millions of cloud droplets are required to produce a single raindrop"。台詞已說「數量級」 |
| C17 | 碰撞合併：較大水滴落得快，追撞小水滴而長大 | p071–p074 | OK | https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/ ；https://www.usgs.gov/water-science-school/science/precipitation-and-water-cycle | 教科書：較大的滴落得較快、掃過較小的雲滴；暖雲中 "the collision-coalescence process is the primary mechanism" |
| C18 | 零度以下常有過冷水滴；冰晶比水滴更會搶水氣 | p075–p078 | OK | https://weather.cod.edu/sirvatka/cloudsrain.html ；https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/ ；https://www.usgs.gov/water-science-school/science/precipitation-and-water-cycle | College of DuPage："Liquid water that is cooler than 0°C is called supercooled"；"the saturation vapor pressure with respect to ice is less than the saturation vapor pressure with respect to water"。夏威夷教科書：冷雲 "contain many more liquid cloud droplets than ice crystals, even at sub-freezing temperatures"。USGS：Bergeron-Findeisen process |
| C19 | 冰晶長大落下，在較暖低空融化成雨 | p079–p080 | OK | https://www.nssl.noaa.gov/education/svrwx101/winter/types/ ；https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/ | NSSL："snowflakes descend into a warmer layer of air and melt completely"。教科書："Outside of the tropics, the ice phase process of rain formation is the primary mechanism" |
| C20 | 夏天很高的雷雨雲裡，兩條路常常都有 | p081；卡片 two-routes | FIX | https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/ ；https://weather.cod.edu/sirvatka/cloudsrain.html | 來源只說兩條路分別在暖雲（熱帶）與冷雲（熱帶以外）為主，沒有找到官方或教科書頁面直接說「高聳雷雨雲裡兩條路**常常**同時都有」。依 claims.md 的規則改成「都可能」。卡片出處「NOAA JetStream：降水的形成」查核者找不到該頁，見 E07 |
| C21 | 2 公釐雨滴每秒約落 6–7 公尺，比雲滴快好幾百倍 | p087；卡片 fall-speed 右 | OK（卡片出處需改，見 E06） | https://atmos.uw.edu/academics/classes/2003Q2/101/lect21_overheads.pdf ；https://geo.libretexts.org/Bookshelves/Meteorology_and_Climate_Science/Atmospheric_Processes_and_Phenomena/07%3A_Precipitation_Processes/7.02%3A_Cloud_Droplets | 華盛頓大學表：1 mm 滴 4 m/s、5 mm 滴 9 m/s，2 mm 落在中間。教科書雨滴公式 w＝220·(ρ₀/ρ·r)^½，r＝1 mm 得約 7 m/s。Gunn & Kinzer 實測 2 mm 約 6.5 m/s（原表未能直接打開，AMS 頁 403）。6.5÷0.01≈650 倍，「好幾百倍」成立 |
| C22 | 小而扁的晴天積雲長不高，水滴未長大就在邊緣蒸發 | p092 | FIX | https://cloudatlas.wmo.int/en/species-cumulus-cu.html ；https://science.nasa.gov/earth/earth-observatory/fair-weather-clouds-sri-lanka-81833/ ；https://courses.ems.psu.edu/meteo3/node/2231 | WMO：淡積雲 "small vertical extent and appearing generally as if flattened"；"Cumulus humilis clouds never produce precipitation"。NASA：晴天積雲 "can last between five and forty minutes"。「在邊緣蒸發」的機制（夾卷蒸發）沒有在打開的官方頁面找到明文，改成只講已證實的部分：長不高、壽命短、來不及下雨就散 |
| C23 | 雷雨雲頂可超過 10 公里，與客機巡航高度差不多 | p093–p094 | FIX（小修） | https://www.noaa.gov/jetstream/thunderstorms/life-cycle-of-thunderstorm ；https://scied.ucar.edu/learning-zone/atmosphere/troposphere | NOAA：成熟期 "often reaching 40,000 to 60,000 feet (12 to 18 km)"。UCAR：對流層頂約 10 km，近赤道可到 20 km；"Jet aircraft often fly just above the tropopause"。雲頂常**高於**客機巡航高度；「飛機」要寫「客機」（小飛機飛很低） |
| C24 | 地面與空氣最熱通常在中午之後 | p097–p099 | OK | http://www.meteo.psu.edu/wjs1/Meteo3/Html/temperature.htm | "the maximum temperature doesn't occur until a few hours later"（相對於太陽最高的 solar noon） |
| C25 | 台灣夏季午後雷陣雨與日射加熱、海風、地形有關，常在下午、山區 | p100–p101；卡片 day-steps | OK（卡片一處用字見 E08） | https://climate.cwa.gov.tw/SeasonalClimate?subpage=Summer ；https://edu.cwa.gov.tw/PopularScience/wt/wt_31.html | 氣候服務入口網：「夏季陽光直射地表……空氣塊被加熱後上升」；「臺灣由於地勢陡、山區多，在午後海風環流建立後，容易在陸地上形成對流作用而造成雷陣雨」；臺北盆地「午後海風從淡水河及基隆河的河口進入臺北盆地交會並舉升」。數位科普網：「容易發生在山區，因為相較於平地，山區的地表加熱速度更快」；「下雨時間可能從中午之後開始，有時甚至也會出現在剛入夜」 |
| C26 | 雲又高又厚、陽光透不過來，底部看起來是灰的 | p103 | OK | https://www.noaa.gov/jetstream/clouds/color-of-clouds | "As clouds thicken, sunlight passing through them will diminish or be blocked, giving the cloud a gray color." |
| C27 | 降雨拖曳空氣下沉、蒸發冷卻，形成下沉冷空氣；雷雨前涼風常是它 | p106–p107、p117 | OK | https://courses.ems.psu.edu/meteo3/node/2024 | 下沉氣流來自雨滴拖曳空氣與 "cooling associated with the evaporation of small raindrops"；下沉氣流觸地散開，前緣是 "gust front or, more formally, an outflow boundary" |
| C28 | 下沉冷空氣切斷上升氣流，單一雷雨胞消散 | p109 | OK | https://www.noaa.gov/jetstream/thunderstorms/life-cycle-of-thunderstorm ；https://courses.ems.psu.edu/meteo3/node/2024 ；https://www.noaa.gov/jetstream/tstrmtypes | NOAA："The downdraft cuts off the updraft."。PSU：outflow "cuts off the inflow of warm, humid air into the storm's updraft" |
| C29 | 單一雷雨胞從發展到消散常約一小時 | p110；卡片 hour | FIX | https://www.noaa.gov/jetstream/thunderstorms/life-cycle-of-thunderstorm ；https://courses.ems.psu.edu/meteo3/node/2024 | NOAA："The thunderstorm cell has a distinct life-cycle that lasts about 30 minutes."。PSU：整個生命 "typically takes less than 45 minutes"。「常常一個小時左右」偏長；改成「常常不到一個小時」，與說明欄「一個小時以內」也一致 |
| C30 | 花椰菜頂代表仍在上升；砧狀頂代表已達很難再往上的高度（對流層頂） | p115–p116 | OK | https://courses.ems.psu.edu/meteo3/node/2024 ；https://forecast.weather.gov/glossary.php?word=ANVIL ；https://scied.ucar.edu/image/cumulus-clouds | PSU：上升空氣到對流層頂比周圍平流層冷而停止上升，對流層頂像 "lid"，空氣水平攤開形成砧。NWS："The flat, spreading top of a cumulonimbus cloud"。UCAR："Watch for rain showers when the cloud's tops look like cauliflower heads." |
| C31 | 小雨滴近球形；大雨滴底部扁平像漢堡麵包；太大會破裂 | p119–p122；卡片 drop-shapes | OK | https://www.usgs.gov/water-science-school/science/are-raindrops-shaped-teardrops ；https://gpm.nasa.gov/resources/students-and-educators/the-shape-of-a-raindrop | USGS："Small raindrops (radius < 1 millimeter (mm)) are spherical; larger ones assume a shape more like that of a hamburger bun"；半徑約 4.5 mm 以上變成降落傘狀 "and then it breaks up into smaller drops"。NASA GPM：變得像 "the top half of a hamburger bun"；過大 "will eventually break apart" |
| E01 | YouTube 標題「一朵雲裡有 500 公噸的水」 | youtube.title | FIX | https://www.usgs.gov/water-science-school/science/how-much-does-a-cloud-weigh | 500 公噸是假設 1 km³、0.5 g/m³ 的估算，標題把估算說成定值 |
| E02 | 縮圖「500 噸的水」 | thumbnail.data.headline | FIX | 同上 | 同上；縮圖空間有限，至少加「約」 |
| E03 | 片尾卡「雲有水，但碎成一百萬分之一的小顆」 | 卡片 outro lines[0] | FIX | https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/ | 「一百萬分之一」是一顆雲滴相對**一顆雨滴**的體積，這樣寫會被讀成「整朵雲的一百萬分之一」，意思錯 |
| E04 | 「空氣裝不下那麼多水氣」 | p026 | FIX | https://www.noaa.gov/jetstream/clouds/how-clouds-form | NOAA 的說法是氣塊冷到飽和（100% 相對濕度）後水氣凝結。「空氣裝水」是氣象教學常要糾正的比喻（飽和取決於溫度，不是空氣當容器） |
| E05 | 卡片 cloud-weight 出處「UCAR／NCAR 估算方式」 | 卡片 cloud-weight.source | FIX | https://www.usgs.gov/water-science-school/science/how-much-does-a-cloud-weigh | UCAR 頁 404，查核者沒能打開；同一套假設與數字在 USGS 頁有完整原文 |
| E06 | 卡片 fall-speed 出處「AMS 氣象學詞彙：終端速度」 | 卡片 fall-speed.source | FIX | https://atmos.uw.edu/academics/classes/2003Q2/101/lect21_overheads.pdf | AMS 詞彙 403 打不開，未能核對 |
| E07 | 卡片 two-routes 出處「NOAA JetStream：降水的形成」 | 卡片 two-routes.source | FIX | https://www.usgs.gov/water-science-school/science/precipitation-and-water-cycle | 查核者找不到這個 NOAA 頁面；USGS 降水頁同時講到碰撞與 Bergeron-Findeisen 兩條路 |
| E08 | 卡片 day-steps「下午：雲長到最高，開始下大雨」 | 卡片 day-steps.steps[2] | FIX（小修） | https://edu.cwa.gov.tw/PopularScience/wt/wt_31.html | 氣象署說「可能從中午之後開始，有時甚至也會出現在剛入夜」，卡片寫成必然，改「常常」 |
| E09 | 卡片 hour 文字「常常 約 1 小時」 | 卡片 hour.text | FIX | 同 C29 | 隨 C29 一起改 |

其他已核對但未列為主張的句子：p051（越小的東西相對空氣阻力越大）、p086（雨滴落速超過上升氣流才落出雲，USGS："If enough collisions occur to produce a droplet with a fall velocity which exceeds the cloud updraft speed"）、p112（濕度、上層溫度、風場任一不對雲就長不起來，屬一般條件陳述，有「只要」的語氣但未給數字，可接受）、說明欄「夏天下午兩點還大太陽，三點就下大雨」是示意情境，不是統計，保留即可。

## 建議修改

- p081：有可能。夏天長得很高的雷雨雲裡，兩條路常常都有。 → 有可能。夏天長得很高的雷雨雲裡，兩條路都可能發生。
- p092：天氣好時那種小小、扁扁的白雲，長不高，水滴還沒時間長大，就在邊緣蒸發掉了。 → 天氣好時那種小小、扁扁的白雲，長不高，水滴還來不及長大，雲就散掉了。
- p093：會下大雨的，是一路往上衝的雲。它的雲頂可以超過十公里，跟飛機飛的高度差不多。 → 會下大雨的，是一路往上衝的雲。它的雲頂可以超過十公里，跟客機飛的高度差不多，甚至更高。
- p110：一個單獨的雷雨雲，從長大、下雨到散掉，常常一個小時左右。 → 一個單獨的雷雨雲，從長大、下雨到散掉，常常不到一個小時。
- 卡片 hour（scene `hour`）`data.text`：常常 **約 1 小時** → 常常 **不到 1 小時**
- p026：冷到某個高度，空氣裝不下那麼多水氣，多出來的就會凝結。 → 冷到某個高度，水氣就飽和了，多出來的就會凝結。
- youtube.title：一朵雲裡有 500 公噸的水，為什麼不會掉下來？｜原來如此事務所 → 一朵雲裡約有 500 公噸的水，為什麼不會掉下來？｜原來如此事務所
- thumbnail.data.headline：500 噸的水\n**浮在天上** → 約 500 噸的水\n**浮在天上**
- 卡片 outro `data.lines[0]`：雲有水，但碎成一百萬分之一的小顆 → 雲有水，但碎成數不完的小水滴
- 卡片 day-steps `data.steps[2].detail`：雲長到最高，開始下大雨 → 雲長到最高，常常開始下雨
- 卡片 cloud-weight `data.source`：UCAR／NCAR 估算方式 → USGS 水科學學校：一朵雲有多重
- 卡片 fall-speed `data.source`：AMS 氣象學詞彙：終端速度 → 華盛頓大學大氣科學課程；夏威夷大學大氣教科書
- 卡片 two-routes `data.source`：NOAA JetStream：降水的形成 → USGS 水科學學校：降水與水循環

## 來源

只列查核者實際打開並讀到原文的頁面，格式可直接放進 `video.json` 的 `sources`。

```json
[
  {"title": "USGS Water Science School: How Much Does a Cloud Weigh?", "url": "https://www.usgs.gov/water-science-school/science/how-much-does-a-cloud-weigh", "checked_on": "2026-11-03"},
  {"title": "USGS Water Science School: Condensation and the Water Cycle", "url": "https://www.usgs.gov/water-science-school/science/condensation-and-water-cycle", "checked_on": "2026-11-03"},
  {"title": "USGS Water Science School: Precipitation and the Water Cycle", "url": "https://www.usgs.gov/water-science-school/science/precipitation-and-water-cycle", "checked_on": "2026-11-03"},
  {"title": "USGS Water Science School: Raindrops are Different Shapes", "url": "https://www.usgs.gov/water-science-school/science/are-raindrops-shaped-teardrops", "checked_on": "2026-11-03"},
  {"title": "NASA GPM: The Shape of a Raindrop", "url": "https://gpm.nasa.gov/resources/students-and-educators/the-shape-of-a-raindrop", "checked_on": "2026-11-03"},
  {"title": "NOAA JetStream: Clouds", "url": "https://www.noaa.gov/jetstream/clouds", "checked_on": "2026-11-03"},
  {"title": "NOAA JetStream: How Clouds Form", "url": "https://www.noaa.gov/jetstream/clouds/how-clouds-form", "checked_on": "2026-11-03"},
  {"title": "NOAA JetStream: The Four Core Types of Clouds", "url": "https://www.noaa.gov/jetstream/clouds/four-core-types-of-clouds", "checked_on": "2026-11-03"},
  {"title": "NOAA JetStream: Color of Clouds", "url": "https://www.noaa.gov/jetstream/clouds/color-of-clouds", "checked_on": "2026-11-03"},
  {"title": "NOAA JetStream: Ingredients for a Thunderstorm", "url": "https://www.noaa.gov/jetstream/thunderstorms/ingredients-for-thunderstorm", "checked_on": "2026-11-03"},
  {"title": "NOAA JetStream: Life Cycle of a Thunderstorm", "url": "https://www.noaa.gov/jetstream/thunderstorms/life-cycle-of-thunderstorm", "checked_on": "2026-11-03"},
  {"title": "NOAA JetStream: Types of Thunderstorms", "url": "https://www.noaa.gov/jetstream/tstrmtypes", "checked_on": "2026-11-03"},
  {"title": "NOAA Education: Cooking up a storm — atmospheric science in your kitchen", "url": "https://www.noaa.gov/education/multimedia/video/cooking-up-storm-atmospheric-science-in-your-kitchen", "checked_on": "2026-11-03"},
  {"title": "NOAA NSSL Severe Weather 101: Winter Weather Types", "url": "https://www.nssl.noaa.gov/education/svrwx101/winter/types/", "checked_on": "2026-11-03"},
  {"title": "NWS Glossary: Dry Adiabatic Lapse Rate", "url": "https://forecast.weather.gov/glossary.php?word=dry%20adiabatic%20lapse%20rate", "checked_on": "2026-11-03"},
  {"title": "NWS Glossary: Lifting Condensation Level", "url": "https://forecast.weather.gov/glossary.php?word=lifting%20condensation%20level", "checked_on": "2026-11-03"},
  {"title": "NWS Glossary: Anvil", "url": "https://forecast.weather.gov/glossary.php?word=ANVIL", "checked_on": "2026-11-03"},
  {"title": "University of Hawaiʻi, Atmospheric Processes and Phenomena, Chapter 7: Precipitation Processes", "url": "https://pressbooks-dev.oer.hawaii.edu/atmo/chapter/chapter-7-precipitation-processes/", "checked_on": "2026-11-03"},
  {"title": "LibreTexts Geosciences, Atmospheric Processes and Phenomena 7.2: Cloud Droplets", "url": "https://geo.libretexts.org/Bookshelves/Meteorology_and_Climate_Science/Atmospheric_Processes_and_Phenomena/07%3A_Precipitation_Processes/7.02%3A_Cloud_Droplets", "checked_on": "2026-11-03"},
  {"title": "University of Washington ATMS 101, Lecture 21 overheads (drop sizes and fall speeds)", "url": "https://atmos.uw.edu/academics/classes/2003Q2/101/lect21_overheads.pdf", "checked_on": "2026-11-03"},
  {"title": "Penn State METEO 3: Single-Cell Thunderstorms", "url": "https://courses.ems.psu.edu/meteo3/node/2024", "checked_on": "2026-11-03"},
  {"title": "Penn State METEO 3: Stability, Clouds, and Precipitation", "url": "https://courses.ems.psu.edu/meteo3/node/2231", "checked_on": "2026-11-03"},
  {"title": "Penn State Meteorology 3: Temperature (daily cycle)", "url": "http://www.meteo.psu.edu/wjs1/Meteo3/Html/temperature.htm", "checked_on": "2026-11-03"},
  {"title": "College of DuPage: Cloud Physics (collision-coalescence and Bergeron process)", "url": "https://weather.cod.edu/sirvatka/cloudsrain.html", "checked_on": "2026-11-03"},
  {"title": "UCAR Center for Science Education: The Troposphere", "url": "https://scied.ucar.edu/learning-zone/atmosphere/troposphere", "checked_on": "2026-11-03"},
  {"title": "UCAR Center for Science Education: Cumulus clouds", "url": "https://scied.ucar.edu/image/cumulus-clouds", "checked_on": "2026-11-03"},
  {"title": "WMO International Cloud Atlas: Cumulus species", "url": "https://cloudatlas.wmo.int/en/species-cumulus-cu.html", "checked_on": "2026-11-03"},
  {"title": "NASA Earth Observatory: Fair-Weather Clouds, Sri Lanka", "url": "https://science.nasa.gov/earth/earth-observatory/fair-weather-clouds-sri-lanka-81833/", "checked_on": "2026-11-03"},
  {"title": "NASA Glenn Research Center: Earth Atmosphere Model", "url": "https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html", "checked_on": "2026-11-03"},
  {"title": "US EPA: Particulate Matter (PM) Basics", "url": "https://www.epa.gov/pm-pollution/particulate-matter-pm-basics", "checked_on": "2026-11-03"},
  {"title": "San Diego Zoo Wildlife Alliance Library: African Elephant fact sheet", "url": "https://ielc.libguides.com/sdzg/factsheets/african_elephant/summary", "checked_on": "2026-11-03"},
  {"title": "中央氣象署 氣候服務入口網：夏季", "url": "https://climate.cwa.gov.tw/SeasonalClimate?subpage=Summer", "checked_on": "2026-11-03"},
  {"title": "中央氣象署數位科普網：午後，雨會下在哪？", "url": "https://edu.cwa.gov.tw/PopularScience/wt/wt_31.html", "checked_on": "2026-11-03"}
]
```
