# 查核報告 1（sothatswhy-p08-popcorn-pressure）

- 查核者：Claude Opus 5.5（獨立查核代理，未參與撰稿）
- 日期：2026-11-07
- 方法：逐句讀 `video.json` 的 224 句台詞（p001–p224，與 `script.md` 的 125 個場景一一對應），加上 YouTube 標題、說明與縮圖文字。對照 `claims.md` 的 C01–C17，並重新打開來源讀原文：PMC4345489 全文（curl 抓頁面轉成文字）、Wikipedia Popcorn／High-altitude cooking／Yushan（raw wikitext）、OpenStax Chemistry 2e 10.3、Popcorn Board 頁面。
- 打不開的來源：NOAA JetStream Air Pressure 頁面抓得到但內文由腳本載入，轉成文字後沒有正文。它支撐的「越高氣壓越低」（p039–p053）另由 Wikipedia High-altitude cooking（"the boiling point of water is lower at higher altitudes due to the decreased atmospheric pressure"）與 OpenStax（Leadville 68 kPa）支撐，結論不受影響。
- 撰稿者標成推論、請查核者判斷的三處：C11「被壓得太緊，變不了」（見 F01）、C15 是否排除水氣推力（論文明文排除，見第二節 p157–p158）、C16 瓶口吹氣類比（可留，見第二節）。
- 結論統計（台詞 224 句）：OK 219、FIX 5、NOT FOUND 0。另外標題、說明、縮圖共 3 項：OK 3。

## 一、要改的地方與理由

| # | 行 | 原句 | 結論 | 理由與來源 |
| --- | --- | --- | --- | --- |
| F01 | p115（所長） | 對，它們被壓得太緊，變不了。 | FIX（說得比來源絕對） | 論文："Pieces of popcorn contain around 20 mg of water … only a small part (less than 1 mg) is in the vapour phase, which means that there is also a liquid phase in the popcorn before explosion." 原文是水與水氣在飽和蒸氣壓下平衡，已經有一小部分是水氣；「變不了」說成完全不能變，也把「平衡」講成「被擠住」。改成「大部分只能先當水」，保留壓力的因果（OpenStax：外壓越高沸點越高），不說全部。p116「等殼一破、壓力一鬆，它們才急著變成水氣」有 Wikipedia "sudden drop in pressure … rapid expansion of the steam" 支撐，照留 |
| F02 | p218（所長） | 那聲啵，是水氣從小空洞裡衝出來的聲音。 | FIX（假說說成定論，機制也走樣） | 論文："it is reasonable to hypothesize that the 'pop' sound is triggered by the vapour release. More precisely, the pressure drop excites cavities inside the popcorn as if it were an acoustic resonator"；結論段也只稱 "scenario"。p187–p188 已正確寫「研究的人推測」，結尾回呼卻改成肯定句，而且說成「水氣從空洞衝出來的聲音」，與論文「壓力下降激起空洞共鳴」不同。結尾是小朋友最會記住的一句，要保留「猜」 |
| F03 | p200（所長） | 玉米是關著的，壓著水的是硬殼。 | FIX（跟片中自己的說法打架） | p104 剛說過「在殼裡，壓著水的不是棉被，是越擠越多的水氣」；論文與 Wikipedia 都是殼關住水氣、水氣的壓力升高（"The steam pressure increases until the breaking point of the hull is reached"）。硬殼是關住的牆，壓著水的是水氣 |
| F04 | p205（小問） | 可以是空氣，也可以是殼？ | FIX（跟著 F03） | 同 F03。p206–p207「誰在壓都一樣」照留 |
| F05 | p197（小問） | 先裂、再跳、再響！ | FIX（順序與來源相反） | 論文："We first see that the 'pop' sound is not caused by the rebound because it occurs before any jump"；聲音在第二次破裂後 6 ms 開始，當時 "the leg of starch continues its course towards the hot plate"，還沒跳。順序是裂、響、跳。小問的整理是觀眾最會記住的一句，要照來源排 |

## 二、逐段核對（OK 的句子與依據）

| 段落／行 | 主張 | 結論 | 來源 | 依據摘要 |
| --- | --- | --- | --- | --- |
| p001–p020 | 露營煮麵慢、瓦斯不夠力（錯猜）、微波爆米花、水滾就是一百度（錯猜）、碗底不爆的玉米 | OK | — | 開場鋪陳、錯猜與問題；答案在後段 |
| p021–p024 | 山上滾水和家裡長得一樣；海邊附近大約一百度；平地差不多 | OK | OpenStax 10.3；Wikipedia High-altitude cooking | 1 atm 下水 100 °C 沸騰；表的海平面為 100 °C。「大約」「差不多」恰當 |
| p025–p028 | 水越燙越多水想變成水氣；燙到夠了鼓出水氣泡泡 | OK | OpenStax 10.3 | "When the vapor pressure increases enough to equal the external atmospheric pressure, the liquid reaches its boiling point." 片中只講大泡泡，避開溶解空氣的小泡 |
| p029–p036 | 水滾後溫度停住；火大只是滾更兇；多的熱拿去把水變成水氣；天花板 | OK | OpenStax 10.3 | "the temperature remains constant despite the continued input of heat"；"the water temperature does not rise, but instead the boiling becomes more vigorous (rapid)"。天花板是比喻 |
| p037–p049 | 天花板看水上面有多少空氣壓著；空氣會壓東西；空氣棉被；泡泡要推開棉被；水要熱到夠；海邊棉被最厚 | OK | OpenStax 10.3；Wikipedia High-altitude cooking | 外壓決定沸點。「推開棉被」是比喻，不描述表面張力。「海邊最厚」指片中比較的地點（平地對高山），不談低於海平面的地方，可以 |
| p050–p055 | 越往上空氣越少、棉被越薄；泡泡不用那麼熱就推得開 | OK | Wikipedia High-altitude cooking | "boiling point of water is lower at higher altitudes due to the decreased atmospheric pressure" |
| p056–p057 | 三千公尺左右大約九十度滾 | OK | Wikipedia High-altitude cooking；OpenStax | 表 3,048 m 89.8 °C；OpenStax Leadville（約 3,100 m）"at about 90 °C … water will boil" |
| p058–p059、p062 | 玉山將近四千公尺；山頂滾水不到九十度；八十幾度 | OK（附註） | Wikipedia Yushan；High-altitude cooking | Yushan 3,952 m。表 3,658 m 87.6 °C、4,267 m 85.5 °C，內插約 86.6 °C，沒有山頂實測值。「不到九十度」離 90 °C 約差 3 °C，天氣造成的氣壓變化（約 ±1 °C）推不翻；「八十幾度」是小問的話，範圍夠寬。台詞沒有給一個精確數字，沒有把估計說成量測，可以。若之後有人想說「八十六度」，要寫成「算起來大約」 |
| p060–p061 | 山上煮麵、蛋、飯常要多等一會兒 | OK | Wikipedia High-altitude cooking | "Means of compensation include extending cooking times"。「常常」恰當 |
| p063–p068 | 煮熟麵的是水的熱，不是泡泡；水沒那麼燙熱鑽得慢；不是瓦斯不夠力 | OK | Wikipedia High-altitude cooking；OpenStax | 沸點低，食物要煮更久。推翻開場的錯猜，與 p031 一致 |
| p069–p072 | 火轉最大也停在那個溫度；只能煮久一點 | OK | OpenStax 10.3 | 同 p031。「只能」緊接著被 p073 的壓力鍋補充，前後不矛盾 |
| p073–p078 | 蓋子壓緊水會更燙；壓力鍋；很高的山上常有人用 | OK | Wikipedia High-altitude cooking | "A pressure cooker is often used to compensate for the low atmospheric pressure at very high elevations"；"higher pressure inside the cooking vessel and thus higher temperatures" |
| p079–p082 | 壓力鍋要大人照說明用，不自己在家關水氣做實驗；看玉米這個小壓力鍋 | OK | — ；論文 | 安全叮嚀，符合 EPISODES.md。論文自己也說 "as in a pressure cooker"。全片沒有引導孩子自己做加壓或加熱實驗；p217「先聽一聽」、p222「碗底剩幾顆」只是吃爆米花時觀察，不需要額外操作 |
| p083–p088 | 殼又硬又亮，水氣幾乎鑽不出去；爆米花用特別的玉米，殼特別硬、不太透水，跟大多數穀物不一樣 | OK | Wikipedia Popcorn | "Unlike most other grains, the outer hull of the popcorn kernel is strong and impervious to moisture"；"the cultivated strain for popcorn is Zea mays everta"。p085–p086 小問問玉米棒能不能爆，回答沒說「不會爆」，避開了 Wikipedia "the kernels of some other types will pop" 的例外，可以。「幾乎」也照顧到尖端漏氣（p127） |
| p089–p096 | 殼裡是軟澱粉，中間藏一小滴水；好爆的玉米一百份裡約十四份是水 | OK | Popcorn Board；Wikipedia Popcorn | Popcorn Board "Each kernel of popcorn contains a small drop of water stored inside a circle of soft starch"、"13.5-14% moisture"；Wikipedia "14–15% moisture by weight"。「十四份左右」落在兩個來源之間 |
| p097–p100 | 鍋子熱，水想變成水氣，硬殼關住；水氣越擠越多，像越吹越緊的氣球 | OK | Wikipedia Popcorn；論文 | "The steam pressure increases until the breaking point of the hull is reached"。氣球是比喻 |
| p101–p107 | 殼裡壓著水的是越擠越多的水氣；壓越用力，水得熱過平地的滾水，天花板升高；跟山上相反 | OK | 論文；OpenStax | 論文 "When the popcorn temperature exceeds 100°C, its water content (moisture) boils and reaches a thermodynamic equilibrium at the vapour pressure"，用 Clausius–Clapeyron 由壓力推溫度 |
| p108 | 研究的人量過，玉米大多在一百八十度左右爆開 | OK | 論文 | "only 34% of popcorn are popped at 170°C (17 out of 50). Instead, 96% of popcorn are popped at 180°C (48 out of 50)"。「量過」對（烤箱實測），「大多」對 96 %。Popcorn Board 寫約 347 °F（約 175 °C），仍在「左右」內 |
| p109–p110 | 那時殼裡壓力大約是外面空氣的九到十倍 | OK（附註：估計值） | 論文；Wikipedia Popcorn | 論文的 p_c ∼ 10 bar 是用殼厚與半徑算的估計，不是量的；Wikipedia "approximately 930 kPa (135 psi)"（約 9.2 倍）。台詞用「大約」且沒說「量過」，與 p108 的「量過」分開，可以 |
| p111–p114 | 研究的人算過，殼破前大部分的水還是液體 | OK | 論文 | "less than 1 mg is in the vapour phase … there is also a liquid phase"。「算過」對（論文是估算） |
| p115 | 被壓得太緊，變不了 | 見 F01 | — | — |
| p116 | 殼一破壓力一鬆才急著變成水氣 | OK | Wikipedia Popcorn | "a sudden drop in pressure inside the kernel and a corresponding rapid expansion of the steam" |
| p117–p118 | 這段時間澱粉被燙得又軟又黏，像麵糊 | OK | Wikipedia Popcorn；Popcorn Board | "the starch inside the kernel gelatinizes and softens"；Popcorn Board "superheated gelatinous substance"。麵糊是比喻 |
| p119–p122 | 火開超大不好：外面水氣太早撐破殼，中間澱粉還沒燙軟，變中間硬的半顆 | OK | Wikipedia Popcorn | "If heated too quickly, the steam in the outer layers of the kernel can reach high pressures and rupture the hull before the starch in the center … can fully gelatinize, leading to partially popped kernels with hard centers" |
| p123–p126 | 碗底不爆的常見原因是太乾，水太少撐不破殼 | OK | Wikipedia Popcorn | 未爆的玉米 "do not have enough moisture to create enough steam for an explosion"；"If the kernels are over-dried … the percentage of kernels that pop" 會降。「常見的原因」沒說唯一 |
| p127–p130 | 尖端接玉米棒，不太擋水氣，加熱太慢水氣漏走；跟山上那鍋水一樣 | OK | Wikipedia Popcorn | "the tip of the kernel, where it attached to the cob, is not entirely moisture-proof, and when heated slowly, the steam can leak out"。小問的比較：水氣跑掉、壓力上不去，與 C02 一致 |
| p131–p134 | 為什麼跳；水氣像火箭推（錯猜） | OK | — | 問題與錯猜，p157–p158 推翻 |
| p135–p140 | 二〇一五年法國兩位研究者；熱鐵板；一秒將近三千張的高速相機 | OK | 論文 | Virot（École Polytechnique）與 Ponomarenko（Grenoble），J. R. Soc. Interface 2015；"high-speed camera Phantom v9 at 2900 frames per second. The hot plate is set at 350°C"。小問 p139 的「一秒三千張」是口語取整，可以 |
| p141–p142 | 殼先裂一條縫，軟澱粉從裂縫鼓出來 | OK | 論文 | "After the fracture of the popcorn hull and the beginning of starch expansion (see the snapshot at 6.9 ms)" |
| p143–p146 | 關了很久的水氣一下放開，把軟澱粉吹成白泡泡 | OK | Wikipedia Popcorn | "rapid expansion of the steam, which expands the starch and proteins of the endosperm into an airy foam"。論文寫 "the starch granules expand adiabatically"，膨脹的推手仍是水氣，兩者不衝突 |
| p147–p148 | 黃色只在殼上，裡面澱粉本來就是白的 | OK | Wikipedia Popcorn | "the popped corn is always off-yellow or white as it is only the hull (or pericarp) that is colored" |
| p149–p150 | 白泡泡離開熱鍋變涼、馬上變硬變脆 | OK | Wikipedia Popcorn | "As the foam rapidly cools, the starch and protein polymers set into the familiar crispy puff" |
| p151–p156 | 澱粉一塊壓在鍋上像小腳；先被壓扁再彈回去，把玉米踢離鍋子 | OK | 論文 | "we observe the formation of a 'leg' which is compressed on the plate (at 13.8 ms). This leg bounces and the popcorn jumps (at 20.7 ms)"。彈簧是比喻，論文也寫動物 "use instead their legs as springs" |
| p157–p158 | 讓它跳的主角是澱粉腳，不是水氣像火箭噴 | OK | 論文 | 論文明文排除："We do not observe motion during the ejection of vapour (no rocket effect)"；結論 "a leg of starch is responsible for the observed motion"。claims.md C15 的疑問可以結案 |
| p159–p162 | 先蹲再跳；跳法有點像跳蚤，也有點像會彈出種子的植物 | OK | 論文 | "popcorn is midway between two categories of moving systems: explosive plants using fracture mechanisms and jumping animals using muscles"；拿跳蚤與 Hura crepitans 比較。小問的跳遠是她自己的比較 |
| p163–p167 | 從殼裂到跳起只有百分之幾秒，眼睛只看到一閃 | OK | 論文 | 6.9 ms 到 20.7 ms；摘要 "in some hundredths of a second" |
| p168–p173 | 只靠那一踢估計約一公分；看到的跳法差不多同一個大小 | OK | 論文 | "it would reach a height h = E0/(mk g) ∼ 1 cm … These orders of magnitudes are consistent with our observations"。「估計」「差不多同一個大小」準確對上「order of magnitude」；引言也說實際 "a few millimetres high to several centimetres high" |
| p174–p178 | 啵是殼破的聲音嗎；旁邊放麥克風，聲音和畫面對在一起 | OK | 論文 | "The microphone is set 30 cm away … The acoustic recording is synchronized with a high-speed camera Phantom Miro 4 (2000 frames per second)"。片中沒有說這組的張數，不跟 p138 混 |
| p179–p181 | 啵大約二十分之一秒 | OK | 論文 | "lasts approximately 50 ms" |
| p182–p185 | 是殼裂開（錯猜）；聲音沒在殼裂那一瞬間出來，晚了千分之幾秒 | OK | 論文 | "the popcorn first opens part of the starch without emitting any sound. Then, after 100 ms, a second fracture starts, followed by the start of the 'pop' sound 6 ms later"；"most part of fractures … are not correlated to any sound"。「千分之幾秒」對 6 ms（相對第二次破裂），第一次破裂根本沒聲音，台詞的方向都對 |
| p186–p188 | 小腳踢鍋子（錯猜）；也不是；研究的人推測，水氣衝出來時讓玉米裡的小空洞一起被震響 | OK | 論文 | "the 'pop' sound is not caused by the rebound because it occurs before any jump"；"it is reasonable to hypothesize … the pressure drop excites cavities inside the popcorn as if it were an acoustic resonator"。「推測」對上 hypothesize |
| p189–p192 | 像對著瓶口吹氣會嗚嗚叫；有一點像，都是空氣在空洞裡被推動就發出聲音 | OK（附註：撰稿者類比） | 論文 | 論文用的是 "acoustic resonator"，並舉香檳瓶塞的 "pop"，瓶口吹氣同屬空腔共鳴，「有一點像」恰當。論文說 "without a clear dominant frequency"，瓶子有明顯音高；所長只說「有一點像」而且沒說聲音一樣，可以留。若要更貼原文可改成開香檳，但不是必要 |
| p193–p196 | 殼裂、跳起、發出啵是三件不同的事，快到黏在一起；一串啵啵啵是好多顆各自走完三步 | OK | 論文 | 時序：破裂、6 ms 後聲音、之後才跳。p193 只列舉三件事，沒說順序，可以。好多顆各自爆是常識推論 |
| p197 | 先裂、再跳、再響 | 見 F05 | — | — |
| p198–p199 | 把山上那鍋水和玉米擺一起；山上鍋子開著，壓著水的只有薄棉被 | OK | — | 回顧 |
| p200 | 玉米關著，壓著水的是硬殼 | 見 F03 | — | — |
| p201–p203 | 規矩同一條：壓著水的力氣越小，不用很熱就滾；越大，要熱得多才滾 | OK | OpenStax；論文 | 蒸氣壓等於外壓即沸騰；Clausius–Clapeyron |
| p204–p205 | 壓著水的可以是空氣也可以是殼 | 見 F04 | — | — |
| p206–p207 | 誰在壓都一樣；越輕天花板越低，越重越高 | OK | OpenStax | 同上 |
| p208–p210 | 我覺得泡泡最會騙人：只告訴你滾了，沒說多燙 | OK | — | 意見句有「我覺得」，內容與 p056–p059 一致 |
| p211–p216 | 小問的總結：山上棉被薄、不到一百度就滾、麵煮得慢；玉米把水關在硬殼裡，越熱越擠，最後炸開 | OK | 同前 | 與前面已核的說法一致 |
| p217 | 下次吃爆米花可以先聽一聽 | OK | — | 觀察邀請，不是實驗 |
| p218 | 那聲啵是水氣從小空洞衝出來的聲音 | 見 F02 | — | — |
| p219–p220 | 微波爐爆米花袋剛拿出來很燙，讓大人打開，別把臉湊過去 | OK | — | 安全常識提醒，claims.md C17 不當成查核主張 |
| p221–p224 | 原來如此；留言碗底剩幾顆；訂閱 | OK | — | 片尾 |
| YouTube 標題 | 山上滾水煮得慢，玉米為什麼又會爆開？ | OK | — | 問題句 |
| YouTube 說明 | 熱不上去的天花板、山上變低、殼裡熱過一百度、2015 年高速攝影分開三件事；數字是大約、壓力鍋不要自己做加壓實驗 | OK | 同前 | 與台詞一致，已說明數字是大約與 AI 插圖是示意 |
| 縮圖 | 山上的滾水不到一百度／玉米卻把水關到快一百八十度 | OK | Wikipedia High-altitude cooking；論文 | 「快一百八十度」對 96 % 在 180 °C 爆、34 % 在 170 °C |

## 建議修改

必改（F01–F05）：

- p115：對，它們被壓得太緊，變不了。 → 對，殼裡壓力太大，大部分只能先當水。
- p200：玉米是關著的，壓著水的是硬殼。 → 玉米是關著的，硬殼把水氣關在裡面。
- p205：可以是空氣，也可以是殼？ → 可以是空氣，也可以是水氣？
- p218：那聲啵，是水氣從小空洞裡衝出來的聲音。 → 研究的人猜，那聲啵跟水氣衝出來有關。

- p197：先裂、再跳、再響！ → 先裂、再響、再跳！（字數相同）

選修（不影響本輪結論）：

- p193：所以殼裂開、跳起來、發出啵， → 所以殼裂開、發出啵、跳起來，（列舉順序跟 p197 一致；原句沒說順序，不算錯）
- （給 claims.md 的維護者）C15 補記論文原文 "We do not observe motion during the ejection of vapour (no rocket effect)"，「不是火箭噴」的疑問可結案；C11 補記水與水氣是平衡共存（不到 1 mg 是水氣），不是「變不了」。

## 來源

只列查核者這次實際打開並讀到原文的頁面。

```json
[
  {"title": "Virot & Ponomarenko (2015), Popcorn: critical temperature, jump and sound, J. R. Soc. Interface 12: 20141247 (PMC full text)", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4345489/", "checked_on": "2026-11-07"},
  {"title": "OpenStax Chemistry 2e, 10.3 Phase Transitions", "url": "https://openstax.org/books/chemistry-2e/pages/10-3-phase-transitions", "checked_on": "2026-11-07"},
  {"title": "Wikipedia: High-altitude cooking", "url": "https://en.wikipedia.org/wiki/High-altitude_cooking", "checked_on": "2026-11-07"},
  {"title": "Wikipedia: Popcorn", "url": "https://en.wikipedia.org/wiki/Popcorn", "checked_on": "2026-11-07"},
  {"title": "Popcorn Board: What Makes Popcorn Pop?", "url": "https://www.popcorn.org/All-About-Popcorn/What-Makes-Popcorn-Pop", "checked_on": "2026-11-07"},
  {"title": "Wikipedia: Yushan (mountain)", "url": "https://en.wikipedia.org/wiki/Yushan_(mountain)", "checked_on": "2026-11-07"}
]
```
