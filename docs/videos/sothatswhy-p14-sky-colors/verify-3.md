# 查核報告 3（sothatswhy-p14-sky-colors）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿，也沒有做第 1、2 輪）
- 日期：2026-11-06
- 範圍：`git diff HEAD~1 -- script.md`（commit 593314a2e「round 2 revision (chapter link, recaps, orphans)」）改動或新增的台詞。大部分差異只是場景重新編號（加了 8. kid-milk-guess，刪了舊 65–66 兩場紫光），下表用**現在** `script.md` 的場景編號與 id。沒改動的句子沿用 verify-1、verify-2 的結論。
- 方法：用 `--word-diff` 挑出內容有變的 27 句，逐句對來源。來源都重新打開讀原文（curl 抓頁面轉成文字）：HyperPhysics Blue Sky、Corfidi（NOAA/NWS SPC）、Gibbs、Wikipedia「Rayleigh scattering」「John William Strutt, 3rd Baron Rayleigh」「Storm Prediction Center」（raw wikitext）「1991 eruption of Mount Pinatubo」。JetStream 沿用 verify-2 讀到的原句。
- 字數上限：照 `build_scenes.py` 的 `length()` 數過改動的句子，都在上限內；FIX 的替換句與原句同長（18 字）。
- 結論統計（內容有變的台詞 27 句）：OK 26、FIX 1、NOT FOUND 0。刪掉的 2 句（舊 65–66 場紫光）不需查核。

## 逐項核對

| 場景 | 句子 | 結論 | 依據摘要 |
| --- | --- | --- | --- |
| 8. kid-milk-guess | 牛奶水？應該白白的吧？ | OK | 小問的錯猜，沒有事實主張；答案在 93–94 場 |
| 10. kid-cloud-teaser | 說到天上，還有雲！天空是藍的，雲怎麼是白的？ | OK | 只是問題 |
| 33. earth-layer | 美國空軍從大約兩萬公尺高的飛機上拍照 | OK | HyperPhysics Blue Sky："It was taken from a U.S. Air Force U-2 craft at about 70,000 feet."（≈21,300 公尺，「大約兩萬公尺」可以） |
| 49. chief-rayleigh | 十九世紀，英國科學家瑞利，把這件事算清楚了。所以這種散射，就叫做瑞利散射。 | OK | Wikipedia「Rayleigh scattering」："named after the 19th-century British physicist Lord Rayleigh"；"In 1871, Lord Rayleigh published two papers on the color and polarization of skylight to quantify Tyndall's effect"；Gibbs：Rayleigh "showed that the amount of light scattered is inversely proportional to the fourth power of wavelength"。Corfidi："the nineteenth century English physicist"。「這件事」接 47–48 場短波多彈、紅光直走，正是 λ⁻⁴ 的內容。下一場說瑞利當時以為是灰塵與水滴（1871 年論文確實以微粒立論，1899 年才推到分子），兩場不矛盾 |
| 51. chief-einstein | 後來的科學家發現：要是靠灰塵，天空的藍應該跟著天氣變很多 | OK | Gibbs："Later scientists realised that if this were true, there would be more variation of sky colour with humidity or haze conditions than was actually observed"。只改了「人」→「科學家」，更貼原文 |
| 68. kid-sun-q | 很多藍光被彈到天上了 | OK | 由「都」改「很多」，修掉過頭的說法；與 71–73 場「一部分」「不算多」一致 |
| 71. chief-yellowish | 是因為一部分藍光，半路被彈走了 | OK | HyperPhysics Red Sunset、NASA Goddard（verify-1 已查）；「一部分」措辭恰當 |
| 72. kid-bright-q | 藍光少了一些，太陽怎麼還這麼亮？ | OK | 問題 |
| 73. chief-half | 少掉的不算多。晴天時，一半以上的陽光，還是直直照到地面。 | OK | 第二句未改（verify-2 F03 已 OK）。「少掉的不算多」：JetStream "over one-half of the sun's white light continues through the atmosphere reaching the Earth's surface"；PVEducation 晴天太陽高時直射約為大氣外的 70%（AM1.5 約少 28%）。換算到藍光，天頂方向瑞利光學厚度約 0.2（450 nm），少掉約兩成，「不算多」對白天成立；這段講的是白天（72 場「還這麼亮」），不必加限制 |
| 78. chief-path | 對，距離沒變，變的是光在路上要穿過的空氣，厚了很多。 | OK | 回應 77 場「太陽又沒有變遠」。一天之內日地距離的變化可忽略；「厚了很多」接 79–81 場與「三十多倍」（verify-2 F04 已 OK） |
| 90. chief-quote | 美國國家氣象局的科學家科菲迪這樣說 | OK | Corfidi 頁面署名 "Stephen F. Corfidi, NOAA/NWS Storm Prediction Center"。Wikipedia「Storm Prediction Center」："part of the National Centers for Environmental Prediction (NCEP), operating under the control of the National Weather Service (NWS)"。他是 SPC 的氣象學家，「科學家」是上位說法，可以；引文 "sunsets are red because the daytime sky is blue" 已在原文核對 |
| 111. kid-dust-guess | （所長）水滴會把天空的顏色換掉，空氣裡飄的灰塵也會。（小問）那灰塵越多，天空就越藍？ | OK | 前句接 99–110 場雲的段落（水滴把各色一樣彈開，雲白、厚雲灰）；灰塵：UCAR "When there are lots of aerosols, the sky might even look white in the middle of the day"、Corfidi "hazy daytime skies … appear grayish or even white"。小問那句是錯猜，112 場會反駁 |
| 118. kid-plane | 坐傍晚班機的人會看到：地上的夕陽淡淡的；飛機一爬過那層霾，天上的顏色就鮮豔起來。 | OK | Corfidi："This effect is most noticeable in an airplane, shortly after take-off on a hazy evening: A seemingly bland sunset at the ground gives way to vivid color aloft as soon as the plane ascends beyond the haze." 原文限定在有霾的傍晚；台詞第二句「那層霾」接 116 場「灰塵多的時候」，有交代。附註（可選）：若怕聽成每班傍晚班機都看得到，可改「霾多的傍晚坐飛機，會看到：地上的夕陽淡淡的；」（20 字，比原句短） |
| 120. chief-high-cloud | （小問）高的雲，紅得最漂亮！ | OK | Corfidi："spectacular shades of scarlet, orange, and red most often grace cirrus and altocumulus layers"。採用 verify-2 的可選建議 |
| 121. chief-volcano-q | 一九九一年，菲律賓的皮納圖博火山大爆發。 | OK | Wikipedia「1991 eruption of Mount Pinatubo」（verify-1 已查），只是從 122 場搬上來 |
| 122. volcano | 火山噴出的氣體，在高空變成細細的小水滴， | **FIX** | 「氣體在高空變成小滴」有來源：Wikipedia "Sulfur dioxide oxidized in the atmosphere to produce a haze of sulfuric acid droplets"；Corfidi "thin veils of dust or sulfuric acid droplets"。但那些小滴是**硫酸**液滴，不是水滴；片中 50、99–111 場的「小水滴」都指水，這裡用同一個詞會讓觀眾以為火山造出了高空的水雲。改「小液滴」 |
| 122. volcano | 慢慢飄散在大約二、三十公里高的地方。 | OK | Corfidi "at altitudes of 12 to 18 miles"（約 19–29 公里）；Wikipedia "gradually spread throughout the stratosphere over the year following the eruption"，「慢慢飄散」貼切 |
| 128. chief-moon-back | 空氣多一點，顏色就變；那幾乎沒有空氣呢？還記得開頭那個問題嗎？站在月球上，白天抬頭看。 | OK | 轉場；月球「幾乎沒有空氣」與 verify-1 已查的 NASA Dark Sky, Bright Sun、NASA Science 月球南極一致 |
| 134. kid-got-it | 還記得我在頂樓看到的藍和紅嗎？ | OK | 回顧開頭，沒有新主張；135 場接「是同一道光」（verify-2 已 OK） |

## 建議修改

- **F01**（122. volcano，所長，18 字 → 18 字）：
  「火山噴出的氣體，在高空變成細細的小水滴，」→「火山噴出的氣體，在高空變成細細的小液滴，」
  claims.md C13 的「可用說法」也要同步。
- （可選）118. kid-plane：「坐傍晚班機的人會看到：地上的夕陽淡淡的；」→「霾多的傍晚坐飛機，會看到：地上的夕陽淡淡的；」

## 來源

本輪重新讀到原文的頁面都已在 `video.json` 的 `sources` 裡，另外用到兩頁可以加進去（41–49 場與 90 場的依據）：

```json
[
  {"title": "Wikipedia: Rayleigh scattering", "url": "https://en.wikipedia.org/wiki/Rayleigh_scattering", "checked_on": "2026-11-06"},
  {"title": "Wikipedia: Storm Prediction Center", "url": "https://en.wikipedia.org/wiki/Storm_Prediction_Center", "checked_on": "2026-11-06"}
]
```
