# 12. `phuket-old-town-big-buddha-viewpoints`

普吉不出海的那一天：老城的中葡街屋與週日步行街、查龍寺與普吉大佛、南端的卡隆觀景台與神仙半島，一條從北往南的路線

| 欄位 | 值 |
| --- | --- |
| kind | `howto` |
| destination_id | `phuket` |
| topics | `itinerary`, `culture`, `nature` |
| valid_until | `null` |
| featured | `true` |
| display_order | `1320` |

規格 2026-09-20 定稿：研究檔的 11 個數字全部重新打開官方頁核對過，另外新讀了 Lard Yai 週日步行街、蘭山觀景台、Jui Tui 神廟與 Phuket Smart Bus 改版後的官網與班表圖。
已對照 main 上的 `phuket-airport-transport-where-to-stay` 與 `phuket-phi-phi-james-bond-island-hopping` 全文。官方來源的數字是規劃時讀到的，撰稿當天要再打開一次核對，`checked_on` 填實際打開那天。
通用規則見第七批 [README](../travel-guides-batch-7/README.md) 與 [ERRATA](../travel-guides-batch-7/ERRATA.md)，第六批的 [ERRATA](../travel-guides-batch-6/ERRATA.md) 仍然適用。

`topics` 照指派訊息抄，三個都在 `apps/api/app/guides/taxonomy.py` 的 `SEED_TOPICS` 裡。研究檔原本建議的 `viewpoint` 也在清單上（站上已有 7 篇在用），
以本篇的切角（兩個觀景台 ＋ 夕陽）其實比 `nature` 貼題；要換就換成 `itinerary`, `culture`, `viewpoint`，由協調者決定，撰稿者照這張表寫。

## 切角與段落

回答一件事：**在普吉不出海的那一天，從老城往南怎麼排、每一段怎麼移動**。
站上兩篇普吉文章一篇只寫機場到飯店與住哪一區、一篇只寫四個跳島方向，**兩篇都沒有寫過任何一個陸上景點**；
`phuket-airport-transport-where-to-stay` 把老城寫成一個住宿選項（block 24 的表格、block 28 的 Route 2 與 Dragon Line），本篇把它展開成一整天。

本篇最有用、別人沒寫的一點是：**這條路線上真正有公車的只有老城與西岸沿線，查龍寺與普吉大佛沒有任何一條 Smart Bus 路線到得了**，
所以一天的行程其實是「老城走路 ＋ 中段包車 ＋ 傍晚在南端看夕陽」。全文要繞著這句話寫。

明確不寫（留給別篇或刻意不寫）：

- **跳島、國家公園門票、瑪雅灣與斯米蘭封閉期**——全部留給 `phuket-phi-phi-james-bond-island-hopping`，一個數字都不重複。
- **機場到飯店、住哪一區、Smart Bus 的完整班表與日票**——留給 `phuket-airport-transport-where-to-stay`，本篇只寫這條路線用得到的票價與那三班延駛車。
- **寺廟服裝與參拜規矩**——只寫一句，連到同批的 `thailand-temple-etiquette-dress-code`，不在本篇重寫清單。
- **娘惹博物館（Peranakan Phuket Museum）**——它在他朗、離普吉鎮開車約 30 分，不是老城步行範圍，本篇不寫（見「撰稿時要小心」第 6 點）。
- **芭東夜生活、按摩、秀場、購物中心、餐廳名**——餐廳一律交給美食目錄，正文不點名店家。

字數 3,000 到 3,600（正文含 summary 與 FAQ、不含 sources），上限 4,200。表格兩張（都是 4 欄），callout 兩個（一個 warning、一個 tip），自繪圖解一張，內文照片 1 到 2 張，offer 兩個。
建議的 H2 順序與字數上限：一天怎麼排（約 500）→ 普吉老城（約 600）→ 查龍寺與普吉大佛（約 620）→ 南端看夕陽（約 480）→ 怎麼移動（約 410）→ 行前檢查（約 220）→ FAQ（約 230）；加 summary 約 230、開頭約 250，合計約 3,540。**哪一段寫超過就砍那一段，不要靠砍別段補。表格與 callout 的字都算在該段的字數裡。**
（2026-09-20 審查微調：H2-3 從 560 加到 620——那一段要寫引言、查龍寺 H3、普吉大佛 H3 再加一句「兩個官方時間」的交代，560 塞不下；加的 60 字從開頭 280→250 與 H2-5 440→410 挪過來，合計不變。
**真的超過就先砍普吉大佛那個 H3**——規格本來就把它排成可以整段刪掉的支線，砍掉之後這一段大約 340 字。）

(1) summary 區塊（第一個區塊，4 句，每句 ≤300 字，只重述正文有的事實，數字逐字照正文）：

- 第一句是要做什麼：普吉不出海的那一天從北往南走一條線——普吉老城、查龍寺、普吉大佛、卡隆觀景台，傍晚收在島最南端的神仙半島看夕陽。
- 第二句是本篇的重點：這條線上只有老城與西岸沿線有公車，查龍寺與普吉大佛兩站 Smart Bus 的班表上都沒有，中段要包嘟嘟車、租車或叫車。
- 第三句是錢與時間：老城的泰華博物館 200 泰銖、09:00 到 17:00、週一休館，查龍寺 08:00 到 17:00、參拜免費，老城的 Dragon Line 循環巴士免費、07:00 到 19:00 每 30 分鐘一班。
- 第四句是注意事項：普吉大佛 2024 年 8 月山崩之後曾經關閉，官方網址現在直接轉到臉書專頁，出發前先確認當天是否開放；週日的他朗路 16:00 到 22:00 是步行街，車進不去。

(2) 開頭 paragraph（第二個區塊，兩段）：

- 第一段給結論：普吉的陸上景點不集中，老城在島的東邊、查龍寺與普吉大佛在中南部、觀景台與神仙半島在最南端，**排成一條由北往南的直線最省車程**，最後一站放在看夕陽的神仙半島。票價、開放時間與班表 2026 年 9 月依泰國觀光局東京辦事處的景點頁、查龍寺官網與 Phuket Smart Bus 官網查證。
- 第二段放兩個 article inline：機場到飯店、住哪一區、Smart Bus 完整班表看普吉機場交通篇（howto，`phuket-airport-transport-where-to-stay`）；想出海的那一天看普吉跳島篇（howto，`phuket-phi-phi-james-bond-island-hopping`），本篇一個跳島數字都不重複。泰國的免簽天數與 TDAC 數位入境卡出發前以外交部領事事務局泰國頁與泰國移民局公告為準（**不連 `thailand-entry-2026-tdac`，2026-12-31 到期**）。

(3) H2-1「一天怎麼排：從老城往南走」（第一個 H2；offer 不放這裡）：

- 先寫一句定位：四個點在同一條南北軸線上，老城最北、神仙半島最南，全程沒有捷運也沒有一條公車串得起來，**行程是照日光排的**：上午走老城（室內博物館避開正午）、中午過查龍、下午上普吉大佛、傍晚到南端等夕陽。
- 表格（表一，4 欄）「站／在哪／開放時間與費用／怎麼過去」，五列：
  - 普吉老城（他朗路一帶）｜島的東邊，普吉鎮中心｜街道免費；泰華博物館 200 泰銖、09:00 到 17:00、週一休館｜Dragon Line 免費循環巴士，07:00 到 19:00 每 30 分鐘一班
  - 蘭山觀景台（Rang Hill）｜普吉鎮西北的小丘｜官方頁只寫「無休」，沒有列費用｜老城叫車上山，沒有公車路線
  - 查龍寺｜普吉鎮西南約 8 公里｜08:00 到 17:00、參拜免費｜普吉鎮開車約 15 到 20 分、芭東約 30 分
  - 普吉大佛｜查龍北邊的 Nakkerd 丘頂｜觀光局頁寫 08:00 到 19:00；是否開放出發前確認｜普吉鎮開車約 20 到 30 分、芭東約 30 到 40 分
  - 卡隆觀景台與神仙半島｜卡塔南邊的山路上、島的最南端｜官方頁沒有列開放時間與費用｜包車；Smart Bus Route 1 只有三班延駛神仙半島
- 表後補三句表格塞不下的：
  - **時間怎麼抓**：老城走路要留 2 到 3 小時（含一座博物館），查龍寺 40 分到 1 小時，普吉大佛（如果開放）含上下山 1 小時起，南端的兩個觀景台各 30 分鐘，夕陽前 40 分鐘要人在神仙半島上。
  - **半天版**：只有半天就砍南端，老城走完接蘭山觀景台看普吉鎮全景，車程最短。
  - **反過來走不划算**：從南往北走，最後一站是老城，夕陽就看不到了；要看夕陽就照本篇的方向。
- 圖解 `diagram-1.svg` 放在表一之後、H2-2 標題之前。

(4) H2-2「普吉老城：街屋、博物館與週日步行街」：

- 第一段寫老城是什麼：普吉在 16 世紀到 18 世紀靠錫礦與國際貿易起家，來的是葡萄牙、荷蘭與福建的商人，留下的是中葡式（Sino-Portuguese）街屋；現在很多改成博物館、精品旅館、咖啡館與雜貨店。這一段照觀光局東京辦事處的普吉鎮頁寫，**不要加「最美老街」「網美必拍」這類沒有來源的形容**。
- 第二段寫怎麼走：主街是他朗路（Thalang Road），旁邊的 Soi Romanee 是一整排粉色與藍色街屋，側巷裡有壁畫，地圖在咖啡店可以拿；街上還有 1907 年的渣打銀行舊址。**這一段的出處是 Phuket Smart Bus 官網的老城導覽（營運者的導覽頁，不是觀光主管機關），行文要寫成「Smart Bus 官網的老城導覽寫」**，而且不要寫「泰國最古老的銀行建築」這種最高級敘述（見「撰稿時要小心」第 4 點）。
- 第三段寫博物館：泰華博物館（Phuket Thaihua Museum）就在老城裡的 Krabi 路上，1934 年蓋、2001 年之前是華文學校，展的是福建移民與錫礦的歷史，200 泰銖、09:00 到 17:00、**週一休館**；正面屋頂上的紅蝙蝠在中文裡是吉祥的意思。觀光局的頁面建議先看完博物館再走街，本篇照這個順序寫。
- 第四段寫神廟與素食節：老城裡有三座當地人常拜的華人神廟，官方頁的拼法是 Chui Tui（Jui Tui）、Put Jaw、Saeng Tham，分別以消災、姻緣、學業與生意聞名；Jui Tui 是 1907 年當地華人建的，供道教斗母，也是每年約 10 月、為期九天的普吉素食節主場之一，從市中心走路約 10 到 15 分鐘。**素食節的日期每年不同、本次查不到官方公布的年度日期，一律寫「日期每年不同，以神廟與觀光局公告為準」，不要寫任何一組月日。**
- warning callout（第一個）「週日的他朗路是步行街」：Lard Yai 週日步行街每週日 16:00 到 22:00 在他朗路舉行，2013 年 9 月 29 日開辦；那個時段他朗路封街、車開不進去，包車要改在外圍下車。週日下午排老城剛好，其他天來就沒有這個市集。
- `activities` offer 放在這一段的最後、H2-3 標題之前。

(5) H2-3「查龍寺與普吉大佛」：一個引言段落加兩個 H3。

- 引言段只寫兩件事：這兩個點都在島的中南部、彼此開車十幾分鐘，**而且 Smart Bus 的三條路線班表上都沒有它們**，所以這一段一定要包車、租車或叫車。服裝規定只寫一句加 article inline：**進殿要遮肩過膝、脫鞋**（這一句是協調者 2026-09-20 指定的逐字寫法，和同批第 13 篇 `pattaya-koh-larn-day-trip-from-bangkok` 一字不差），細節看泰國寺廟禮儀篇（howto，`thailand-temple-etiquette-dress-code`），**本篇不重寫清單、不列可以租腰布的地點**。
- H3「查龍寺：普吉信仰最集中的一座」：08:00 到 17:00、參拜免費，在普吉鎮西南約 8 公里，普吉鎮開車約 15 到 20 分、芭東約 30 分。**時間那一句後面要加一句交代兩個官方數字**：「查龍寺官方網站的 FAQ 寫的是 07:00 到 17:00，泰國觀光局東京辦事處寫 08:00 到 17:00；本文照觀光局的 08:00 排，早到的人以現場告示為準。」（理由與寫法見「撰稿時要小心」第 9 點，**要和同批第 14 篇一字不差**。）看什麼：1876 年錫礦工人暴動時救助村民的高僧像，信眾在像上貼滿金箔；寺內 60 公尺高的舍利塔分三層，最上層的平台可以俯瞰整片寺區，塔內有玻璃展示的佛骨（這一段的出處是查龍寺官網）。**正式名稱兩個官方頁拼法不同**：觀光局寫 Wat Chaithararam、寺方官網寫 Wat Chaiyathararam，正文寫「查龍寺」，括號註明正式名稱兩種拼法都是官方頁上的寫法。
- H3「普吉大佛：出發前先確認開不開」——**這個 H3 要寫成可以整段刪掉、上下文仍然讀得通的支線**（見「撰稿時要小心」第 1 點）：
  - 先寫是什麼：坐落在 Nakkerd 丘頂的大佛公園，高 45 公尺、寬 25.454 公尺，外面貼了一萬多塊大理石，從平台可以看到查龍灣與拉威海灘，黃昏也看得到夕陽。
  - 再寫開放狀態，這是本段的重點：觀光局東京辦事處的景點頁到 2026 年 9 月 20 日仍寫 08:00 到 19:00，但**那一頁沒有提到 2024 年 8 月山崩之後的封閉與後續**，頁上留的官方網址 mingmongkolphuket.com 現在會直接轉到臉書專頁，本次查不到任何可引用的官方開放公告。所以正文寫：「觀光局頁寫 08:00 到 19:00，但這一頁沒有反映 2024 年 8 月山崩後的狀況，出發前請先看官方臉書專頁或問飯店是否開放。」
  - 最後寫替代方案，好讓整段刪掉也不影響行程：普吉大佛沒開就把這一格換成蘭山觀景台或直接南下，當天的路線不會斷。
  - **絕對不要寫任何第三方部落格或媒體說的重開日期、新開放時間或門票**（網路上流傳 2026 年 3 月重開、09:00 到 18:00 這一組，本次沒有任何官方頁佐證，一個字都不能寫）。

(6) H2-4「南端看夕陽：卡隆觀景台與神仙半島」：

- 卡隆觀景台（Karon View Point）：在卡塔海灘南側的山路上，從那裡一次看得到卡塔亞伊、卡塔諾伊與卡隆三個海灘，**以前叫卡塔觀景台、現在官方頁已經改名**；再往南就接到島最南端的神仙半島。官方頁沒有列開放時間與費用，正文寫「路邊的觀景平台，開放時間與費用以現場為準」。
- 神仙半島（Phromthep Cape）：普吉島的最南端，官方頁寫它是泰國最有名的夕陽點之一，乾季到熱季天空與海最清澈；觀景台旁邊有為紀念拉瑪九世在位 50 週年而建的 Kanchanaphisek 燈塔，還有一座四面佛（Phra Phrom）祠，祠邊那一排大象雕像是還願的人供上去的。普吉市區包嘟嘟車過去約 40 分、芭東約 30 分。
- **Smart Bus 延駛班次**（這是本篇最實用的一段，別漏）：Route 1 的班表圖上有三班用黃色標示會延駛到神仙半島，拉威發車 17:22、17:47、19:02，從神仙半島往卡塔、卡隆、芭東與機場是 17:23、17:48、19:03；對應的是機場 14:00、15:00、16:00 發的那三班。Smart Bus 官網的夕陽導覽頁也把這三班列成建議班次。班表註明**時刻為約略值、會受交通影響**，看夕陽不要壓最後一班。
- 季節那一句放 article inline：乾季 11 月到 3 月、熱季 4 月到 5 月、綠季 6 月到 10 月，綠季有陣雨、夕陽不一定看得到；泰國、越南、新加坡、香港的月份對照看東南亞季節篇（howto，`southeast-asia-seasons-when-to-go`）。**這三個季節的月份要和既有兩篇普吉文章一字不差**（見「撰稿時要小心」第 3 點）。
- tip callout（第二個）「夕陽前 40 分鐘要到位」：神仙半島與卡隆觀景台都沒有遮蔭也沒有座位區，人多的時候停車位先滿；抓夕陽前 40 分鐘到，順路先停卡隆觀景台再下神仙半島。要搭 Smart Bus 回去的人，先確認回程那三班的時間。

(7) H2-5「怎麼移動：哪一段有公車、哪一段沒有」：

- 表格（表二，4 欄）「路線／從哪到哪／票價／班次與注意」，四列：
  - Dragon Line（老城循環）｜Central Festival、老城與 OTOP 市集｜免費｜07:00 到 19:00、每 30 分鐘一班；路線圖上停泰華博物館與普吉巴士總站 1
  - Smart Bus Route 2｜普吉巴士總站 1 到芭東｜50 泰銖單一票價｜班表圖上總站首班 06:00、末班 20:00，芭東回程首班 06:00、末班 21:00，單程約 1 小時到 1 小時 10 分
  - Smart Bus Route 1｜機場經芭東、卡隆、卡塔到拉威｜100 泰銖單一票價｜只有三班延駛神仙半島，班表上沒有卡隆觀景台這一站
  - 雙條車｜普吉鎮市場前往各海灘｜以現場為準｜每天約 07:00 到 18:00、約 30 分鐘一班
- 表後三句：
  - **中段沒有公車**：查龍寺與普吉大佛不在上面任何一條路線上，要包嘟嘟車、租車或叫車；觀光局的普吉頁寫島內移動靠租車或包嘟嘟車、**價錢是議價制**，跳表計程車數量少。上車前先講好價錢與等候時間。
  - **從芭東來老城**：搭 Route 2 到普吉巴士總站 1，Smart Bus 官網的老城導覽寫從總站往北走約 10 分鐘就到老城。
  - **日票與付款方式**不在本篇寫，接一句 article inline 指回普吉機場交通篇（howto，`phuket-airport-transport-where-to-stay`）。
- `transport` offer 放在這一段的最後、H2-6 標題之前（和前一個 offer 中間隔了整個 H2-4 與 H2-5，不會相鄰）。

(8) H2-6「行前檢查」，list 區塊（6 項）：

- 先查普吉大佛開不開：官方網址已轉到臉書專頁，出發前看一次公告或請飯店幫忙問。
- 挑星期：想逛週日步行街就排週日下午；泰華博物館週一休館，週一來就把博物館換成走街與神廟。
- 中段的車先訂：查龍寺與普吉大佛沒有公車，前一天談好包車或確認叫車 App 在飯店這一區叫得到。
- 服裝：進殿要遮肩過膝、脫鞋，穿方便穿脫的鞋；細節看泰國寺廟禮儀篇。
- 夕陽時間：抓夕陽前 40 分鐘到神仙半島；要搭 Smart Bus 就確認回程那三班。
- 綠季 6 月到 10 月有陣雨，把室內的（博物館）和室外的（觀景台）先想好怎麼互換。

(9) faq 區塊（3 題，答案純文字，只重述正文的事實）：

- 「普吉大佛現在開放嗎？」：泰國觀光局東京辦事處的景點頁寫 08:00 到 19:00，但那一頁沒有反映 2024 年 8 月山崩之後的狀況，頁上的官方網址現在會轉到臉書專頁，本文查不到可引用的官方開放公告；出發前請看官方臉書專頁或問飯店。沒開就換成蘭山觀景台或直接南下。
- 「這一天可以不租車嗎？」：老城靠走路加免費的 Dragon Line 就夠，芭東來回老城有 Route 2 的 50 泰銖單一票價；但查龍寺與普吉大佛不在任何一條 Smart Bus 路線上，中段一定要包車或叫車。神仙半島只有三班延駛車，拉威發車 17:22、17:47、19:02。
- 「他朗路的週日步行街幾點？」：每週日 16:00 到 22:00，在老城的他朗路上，2013 年 9 月 29 日開辦；那個時段封街，包車要改在外圍下車。

(10) 結尾：`related`（最多 4）：`phuket-airport-transport-where-to-stay`、`phuket-phi-phi-james-bond-island-hopping`、`thailand-temple-etiquette-dress-code`、`southeast-asia-seasons-when-to-go`。
`aliases`（zh-TW）：「普吉老街」「普吉大佛寺」「卡塔觀景台」「塔朗路」——後兩個分別是卡隆觀景台的舊名與他朗路的常見寫法，讀者會這樣搜。
**`aliases` 不要收單獨的「大佛寺」**：本批第 13 篇寫的「芭達雅大佛寺（Wat Phra Yai）」是另一座，單寫「大佛寺」會讓兩篇互相搶同一個搜尋詞。
最後放兩個 link 區塊：城市頁 `https://mokaair.com/zh-TW/destinations/phuket`、美食目錄 `https://mokaair.com/zh-TW/foods?destination_id=phuket`（**用 `destination_id`，不要用 `?city=`**；`apps/api/app/foods/area_catalog.py` 裡普吉有「普吉老城」這一區，連結文字可以寫成「普吉美食目錄：老城與海灘周邊的餐廳」）。

照片：hero 用 Commons 的橫幅實景照（老城的中葡式街屋立面、查龍寺舍利塔或神仙半島的夕陽都可以）。
內文照片 1 到 2 張，建議一張老城街景或泰華博物館建築、一張查龍寺或神仙半島。
**既有的 `phuket-airport-transport-where-to-stay` 已經用掉一張「普吉老城街角的白色中葡式建築與一排彩色街屋」（photo-2）與一張普吉機場國內線航廈內部（photo-1），`phuket-phi-phi-james-bond-island-hopping` 用掉 James Bond 島與斯米蘭巨岩兩張，四張都不能重複**；hero 也不能和任何一篇的 hero 同檔。授權與挑法照第七批 README。

## 官方來源

撰稿時寫進 sources，`checked_on` 填實際打開那天。以下全部是 2026-09-20 用 curl 讀到的（`-A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`），標「本次新讀」的是寫規格時第一次打開的頁。

(1) 泰國政府觀光局東京辦事處：普吉大佛 https://www.thailandtravel.or.jp/phra-phutthaminmongkol-akenakkeeree-big-buddha-image/ （200）：「営業時間 08:00～19:00」「URL https://www.mingmongkolphuket.com/Index」「アクセス プーケット・タウンから車で約20～30分。パトン・ビーチからは約30～40分。」「ナーグート丘の頂上にある大仏公園から、島全体を見守るように鎮座しています。」「この仏像は、寄付によって建立されたもので1万個以上の大理石が使用されています。幅25.454m、高さ45m」「この大仏公園からはチャロン湾、ラワイ・ビーチなどプーケットの美しい島々を見渡すことができます。また、夕暮れ時には夕日の壮大な景色を眺めることができる」「住所 42/14 Moo 2, Thepkrasattri Road, Rasada Sub-district, Muang District Phuket 83000」（**這個地址是聯絡地址，不是丘頂的位置，正文不要寫地址**）。頁上沒有任何封閉或重開的公告。

(2) 普吉大佛官方網址 https://www.mingmongkolphuket.com/Index （本次新讀）：`HTTP/1.1 301 Moved Permanently`、`Location: https://www.facebook.com/mingmongkolphuket`。整站已經改成轉址到臉書專頁，curl 取到的是臉書的登入殼（`<title>Facebook</title>`），**讀不到開放時間或公告**。研究檔寫「curl 200，站台可讀」是把臉書的 200 當成站台可讀，**規格已更正**。

(3) 泰國政府觀光局東京辦事處：查龍寺 https://www.thailandtravel.or.jp/wat-chalong/ （200）：「営業時間 08:00～17:00」「料金 参拝自由」「アクセス プーケット・タウン中心部より車で約15～20分、パトン・ビーチより車で約30分」「プーケット・タウンの南西約8kmのところにあります。」「名称(英) Wat Chaithararam (Wat Chalong) ※正式名称はWat Chaithararam」「1876年にアンイーと呼ばれる錫採掘者が反乱を起こした際に、地元の村人たちを救った高僧らの像が安置されています…彼らの像の全身には、参拝に訪れた人が寄進した金箔がびっしりと貼り付けられています。」

(4) 查龍寺官網 https://www.wat-chalong-phuket.com/index.html （200，本次新讀）：「Wat Chalong, or Chalong Temple, built at the beginning on 19th century, Its real name is Wat Chaiyathararam」「The most recent building on the grounds of Wat Chalong is a 60 meters tall 'Chedi' sheltering a splinter of bone from Buddha.」「Wat Chalong Chedi is built on three floors so feel free to climb all the way to the top floor terrace to get a nice bird view on the entire temple grounds. Few more steps will lead you to a glass display where the fragment of bone can be contemplated.」「70 Moo 6 Chaofa Road ( West ) Chalong Phuket 83000 Tel. 076 381-226」。首頁與 `wat-chalong-temple.html`（Information 頁）都沒有開放時間，Information 頁另寫「Wat Chalong is Free Entrance and plenty of Free parking for cars and motorbikes.」。

(4b) 查龍寺官網 FAQ https://www.wat-chalong-phuket.com/faq.html （200，**2026-09-20 審查時新讀，(3) 的 TAT 頁 URL 欄指向的就是這個站**）：「Q: What are the opening hours for Wat Chalong　A: The Phuket Wat Chalong Temple is accessible all year round because it is open daily from 7:00 a.m. to 5:00 p.m.」「Q: When is the best time to visit?　A: Early morning (7:00 a.m. - 9:00 a.m.) is best to avoid crowds, intense heat, and to see monks performing morning rituals.」「Q: Entry fee for Wat Chalong　A: Although there is no charge to enter the temple, donations and offerings are welcome.」「Q: Is photography allowed?　A: Yes, photography is allowed」。
**兩處 07:00 都在可見內容裡、不在 HTML 註解內**（審查時逐頁確認過）。**規格原本寫「這個站沒有開放時間頁」是錯的——那是只讀了 `index.html` 的結果，FAQ 這一頁有**。08:00 到 17:00 的出處是 (3)，07:00 到 17:00 的出處是這一頁，取捨見「撰稿時要小心」第 9 點。服裝與鞋子那幾條也在這一頁，但**本篇不寫、全部留給第 14 篇**。

(5) 泰國政府觀光局東京辦事處：普吉鎮 https://www.thailandtravel.or.jp/phuket-town/ （200）：「16世紀から18世紀にかけて、錫の採掘と国際貿易で栄えたプーケット。当時はポルトガルやオランダ、福建省からの商人などで賑わっていました。」「シノポルトガル様式の建築物が点在。ミュージアムとして保存・公開されている邸宅のほか、ブティック・ホテルやカフェにアイスクリームショップ、ポップでキュートな雑貨店などにリノベートされたタウンハウス」「アクセス プーケット国際空港から車で約45分、パトン・ビーチから約30分」。

(6) 泰國政府觀光局東京辦事處：Lard Yai 週日步行街 https://www.thailandtravel.or.jp/lard-yai-walking-street/ （200，本次新讀）：「ラート・ヤイ・ウォーキングストリートは、プーケット・タウンのタラン通りで毎週日曜日に開催されるナイトマーケットです。」「「SML」と呼ばれる村やコミュニティの可能性開発プロジェクトの一環として2013年9月29日に始まりました。」「営業時間 毎週日曜日16:00～22:00」「住所 Talang Road, Muang, Phuket 83000」「アクセス プーケット国際空港から車で約40分。プーケット・タウンのタラン通りで開催。」

(7) 泰國政府觀光局東京辦事處：泰華博物館 https://www.thailandtravel.or.jp/phuket-thaihua-museum/ （200）：「営業時間 09:00～17:00／月曜休館」「料金 200バーツ」「住所 28 krabi Road, Tambon Talat Nua, Muang District, Phuket 83000」「1934年に建てられ、2001年まで中国語の学校として使われていた建物をリニューアルしてつくられた、プーケットのチャイニーズカルチャーを紹介する博物館。福建省からプーケットへ渡った中国人移民と錫採掘の歴史、食文化などが写真パネルで紹介されています。」「建物の正面の屋根には、中国では吉祥の縁起物と信じられる赤いコウモリの像があり」「プーケット・タウンではまずこの博物館を訪れて、その歴史と文化を学んでから街歩きを楽しむのもおすすめです。」

(8) 泰國政府觀光局東京辦事處：Jui Tui 神廟 https://www.thailandtravel.or.jp/chui-tui-chinese-shrine/ （200，本次新讀）：「プーケット・タウン内にある道教の女神・斗母が祀られている中国系の神社。地元の中国系住民によって1907年に建立され、毎年10月頃に9日間に渡って開催される「プーケット・ベジタリアン・フェスティバル」のメイン会場となる寺院のひとつです。」「アクセス プーケット・タウンの中心部から徒歩約10～15分」。**頁上沒有開放時間與費用，也沒有年度日期。**

(9) 泰國政府觀光局東京辦事處：蘭山觀景台 https://www.thailandtravel.or.jp/rang-hill/ （200，本次新讀）：「名称(英) Rang Hill View Point（Khao Rang View Point)」「営業時間 無休」「町の北西に位置する小高い丘にあるビューポイントで、プーケットタウンの素晴らしい景色を一望できます。」「頂上の公園では、地元の人々が午前と午後に運動するレクリエーションパークであり、昼間はピクニックなどを楽しむ家族連れの憩いの場として、また夜間は美しい夜景スポットとして地元のカップルたちでにぎわっています。」「住所 Wichit, Muang Phuket, Phuket 83000, Thailand」。**只有「無休」，沒有時間也沒有費用。**

(10) 泰國政府觀光局東京辦事處：卡隆觀景台 https://www.thailandtravel.or.jp/karon-view-point/ （200）：「カタ・ビーチの南側にある山道を登るとカロン・ビューポイント（展望台）があります。以前はカタ・ビューポイントと呼ばれていましたが、名称が変わっています。」「ビューポイントからはカタ・ヤイ・ビーチ、カタ・ノイ・ビーチ、カロン・ビーチと３つのビーチを一望できる景勝地です。」「さらに南に進むとプーケット島最南端にあるプロムテープ岬があります。」**基本情報欄只有名稱與地圖，連地址都沒有**（研究檔寫「只有地址」，本次核對後更正）。

(11) 泰國政府觀光局東京辦事處：神仙半島 https://www.thailandtravel.or.jp/laem-phromthep/ （200）：「プーケット島の最南端に位置するプロムテープ岬(レムプロムテープ)は、タイで最も綺麗な夕日が見られるといわれる人気スポット。」「ビューポイントの傍にある、故プミポン前国王(ラーマ9世)の在位50周年を記念して建てられたカンチャナーピセーク灯台や、プラ・プロム(ブラフマー神)の祠があり…プラ・プロムの祠を囲むように並ぶ象の置物は、願いが叶ったお礼に人々がお供えをしたものです。」「住所 Rawai, Mueang Phuket District, Phuket 83100」「アクセス プーケット市内からトゥクトウクなどをチャーターして約40分、パトン・ビーチからは約30分。」

(12) 泰國政府觀光局東京辦事處：普吉區域頁 https://www.thailandtravel.or.jp/areainfo/phuket/ （200）：「乾期は11月～3月で、4月～5月が暑期、6月～10月がグリーンシーズンです」「プーケットタウンから各ビーチへは、ソンテウが毎日7時から18時頃まで30分間隔で運行されていて、プーケットタウンの市場前がソンテウ乗り場になっています。」「島内を回るには、レンタカーかトゥクトゥク(料金は交渉制)をチャーターできます。」「タクシーの中には、メータタクシーもあるものの台数が少なく、多くは運賃交渉制です。」「無病息災にご利益のあるジュイトゥイ神社や恋愛運をもたらすといわれるプッジョー神社、学問や商売繁盛のセーンタム神社」。

(13) Phuket Smart Bus：Timetable https://www.phuketsmartbus.com/timetable （200，本次新讀，**官網 2026 年改版過**）：三個分頁「Airport → Rawai 100฿」「Bus Terminal → Patong 50฿」「Dragon Line Free」；「Bus Terminal 2 → Patong Beach 50 ฿ flat fare」；「Dragon Line — City Shuttle FREE｜Free circular city shuttle connecting Central Festival, Old Town and OTOP Market.」；「Note: Times are approximate and may vary with traffic.」。頁面的 `meta description` 寫「Hourly departures Airport → Rawai (06:30–17:30) and Rawai → Airport (06:00–17:00)」，**和同一頁掛的班表圖（08:15 到 23:30）互相矛盾，以班表圖為準**（見「撰稿時要小心」第 7 點）。

(14) Phuket Smart Bus：Route 1 班表圖（機場往拉威，圖上標「Start 16 January 2026 Onwards／Last update, 16 Jan 2026」）https://www.phuketsmartbus.com/storage/timetables/rawai/cyNL6jUamPSb6d76JiMqZgpNXXLNLcIqUUwIou62.jpg （200，本次以 Read 開圖逐格核對）：站序 Phuket Airport、Thalang Public Health Office、Baan Khian、Cherngtalay School、Lotus Cherngtalay、Surin Beach、Kubur Kamala、Phuket Fantasea、Big C Kamala、PEA Patong、Karon Circle、Kata Night Plaza、Kata Palm、Sai Yuan、Rawai Beach；圖下方方框「Rawai >> Phromthep Cape 17:22 / 17:47 / 19:02」「Phromthep Cape >> Kata/Karon/Patong/Airport 17:23 / 17:48 / 19:03」，圖例「黃色＝ไปแหลมพรหมเทพ Go To Phromthep Cape」，黃色標示的是機場 14:00、15:00、16:00 那三班。**班表上沒有卡隆觀景台、查龍寺或大佛的站。**

(15) Phuket Smart Bus：Route 2 班表圖（普吉鎮⇄芭東，圖上標「Start 15 January 2026 Onwards／Last update, 15 January 2026」）https://www.phuketsmartbus.com/storage/timetables/patong/QW294Wua2G6sv4FBPJvi77RQ5SR88Lw9VbDpQpKW.jpg （200，本次以 Read 開圖）：起點欄寫「สถานีขนส่งภูเก็ต 1 ／ Phuket Bus Terminal 1」，終點「Patong Beach Bus Stop」；總站發車 06:00 起，整點一班到 15:00，之後 15:30、16:00、16:30、17:00、17:30、18:00、19:00、20:00，全程約 1 小時；芭東回程 06:00 到 21:00、到總站約 1 小時 10 分。

(16) Phuket Smart Bus：Dragon Line 路線圖 https://www.phuketsmartbus.com/storage/timetables/dragon/QYMy59fUx13buCq7xoNF46NCprwoAAHUfSuNwByQ.jpg （200，本次以 Read 開圖）：圖下方泰文「รถออกทุก 30 นาที เริ่มตั้งแต่ 07.00 - 19.00 น.」（每 30 分鐘一班、07:00 到 19:00）；圖上的站名包含 พิพิธภัณฑ์ไทยหัว（泰華博物館）、บขส.1（巴士總站 1）、ถนนดีบุก、ตลาดดาวน์ทาวน์、วงเวียนสุริยเดช 等，路名標「THALANG ROAD」「PHANG-NGA ROAD」。

(17) Phuket Smart Bus：Sunset Trip 導覽頁 https://www.phuketsmartbus.com/blog/sunset-trip-with-phuket-smart-bus （200，本次新讀，頁上日期 June 15, 2026）：「Recommended buses passing Promthep Cape: 14:00 / 15:00 / 16:00」「Phuket Town – Patong Route… Recommended departures: 16:00 / 16:30 / 17:00」。

(18) Phuket Smart Bus：老城導覽頁 https://www.phuketsmartbus.com/blog/phuket-old-town-walking-tour （200，本次新讀，頁上日期 April 14, 2026）：「Thalang Road — the main artery of the old town.」「Soi Romanee — once the most notorious street in Phuket, now a row of pink and blue shophouses.」「Standard Chartered Bank (1907) — the oldest bank building in Thailand.」「Street art — over 20 murals scattered around the side sois. Pick up a free map at any café.」「Take the Bus Terminal ⇄ Patong route and get off at the bus terminal — the old town is a 10-minute walk north. Fare: 50฿.」**這是營運者的導覽部落格，不是觀光主管機關**，引用要註明出處，最高級敘述不寫。

(19) 泰國政府觀光局東京辦事處：娘惹博物館 https://www.thailandtravel.or.jp/peranakan-phuket-museum/ （200，本次新讀，**本篇不寫，列在這裡是為了防止寫錯**）：「営業時間 09:00〜18:00／無休」「料金 大人300バーツ／小人150バーツ」「住所 124/1 Moo 1 Sri Soonthorn, Thalang Phuket 83110」「アクセス プーケット・タウンから車で約30分。」——**在他朗、不在老城**。

讀不到（撰稿時可以再試一次，讀到就補進正文並在 `notes.md` 記下）：

- `https://www.tourismthailand.org/Attraction/phra-phuttha-ming-mongkhon-ek-nakkhiri-phuket-big-buddha`：寫規格時 curl 回 200 但內容是 Nuxt build error 殼（整頁 eslint 訊息、`<title>` 是站名），WebFetch 回 403。泰文版 `thai.tourismthailand.org/Attraction/...` 同一個殼。
  **2026-09-20 審查再試一次：改成 `403` ＋ Cloudflare 驗證頁（`<title>Just a moment...</title>`、可見文字只有「Enable JavaScript and cookies to continue」，共 5,785 bytes）。**
  兩次都讀不到，只是理由變了。**TAT 主站的景點深層頁這台機器讀不到，普吉大佛沒有第二個可引用的官方時間來源**；下次重查時看到 200 也要先確認不是驗證頁或 build error 殼。
- `https://www.phuket.go.th/`、`https://www.phuket.go.th/webpk/default.php`（普吉府政府）：403。
- `https://phuketcity.go.th/travel`、`/travel/detail/76`：404（研究檔記的 `phuketcity.go.th` 只有 1,263 bytes 進站頁仍然成立）。
- TAT Newsroom WP REST API（`https://www.tatnews.org/wp-json/wp/v2/posts?search=...`）查 `Big Buddha`、`Phuket landslide`、`Nakkerd` 三個關鍵字：**沒有任何一篇關於山崩、封閉或重開的稿**。素食節只查到 2023、2024、2025 三年的稿，2026 年的還沒出。
- `https://www.facebook.com/mingmongkolphuket`：curl 回 200 但是登入殼，讀不到貼文。**正文只能寫「請自行看官方臉書專頁」，不要引用任何一則貼文內容。**
- 素食節的年度日期：TAT 東京的 2026 年祝祭日行事曆只列國定假日，沒有素食節；TAT Newsroom 2026 年的稿還沒出。**一個月日都不寫。**

## 合作區塊（offer）

兩個，都在第一個 H2 之後，中間隔了整個 H2-3 與 H2-4，不會相鄰。`destination_id` 留 null（沿用文章的 `phuket`）。

- module `activities`：放在 H2-2「普吉老城」的最後、H2-3「查龍寺與普吉大佛」標題之前。heading 用通用說法，例如「普吉的一日遊與門票先比價」，不點名查龍寺包車、普吉大佛接送這些不一定畫得出來的商品。
- module `transport`：放在 H2-5「怎麼移動」的最後、H2-6「行前檢查」標題之前。heading 例如「普吉包車與機場接送先比價」。

不放 hotel（住哪一區是 `phuket-airport-transport-where-to-stay` 的事，本篇是一日行程）、不放 flight、不放 connectivity。
正式站目前只有 tokyo、osaka-kyoto、seoul、busan、taipei 的 activities 與 transport 有核准方案，phuket 上線時大概畫不出東西，區塊照放，等後台核准。

## 站內連結

完整網址前綴是 `https://mokaair.com/zh-TW/`。文章連結一律用 `rich_paragraph` 的 `article` inline（填對方的 kind 與 slug），城市頁與美食目錄用 `link` 區塊。每一句都要寫成拿掉連結後仍讀得通。

1. 開頭第二段 → `phuket-airport-transport-where-to-stay`（howto，既有，長青，zh-TW）：連結文字講「機場到飯店、住哪一區、Smart Bus 完整班表」。
2. 開頭第二段 → `phuket-phi-phi-james-bond-island-hopping`（howto，既有，長青，zh-TW）：連結文字講「出海那天：皮皮島、攀牙灣還是斯米蘭」。
3. H2-3 引言的服裝那一句 → `thailand-temple-etiquette-dress-code`（howto，**本批第 14 篇**）：連結文字講「進泰國寺廟該穿什麼、不該做什麼」。這一句只寫「遮肩過膝、脫鞋進殿」，其餘交給對方。
4. H2-4 季節那一句 → `southeast-asia-seasons-when-to-go`（howto，既有，長青，zh-TW）：連結文字講「泰國、越南、新加坡、香港的乾季雨季月份對照」。
5. H2-5 表後的日票那一句 → 再次指回 `phuket-airport-transport-where-to-stay`（同一篇可以出現兩次 inline，`related` 只算一個）。
6. 結尾 `link`：`destinations/phuket`（城市頁）。
7. 結尾 `link`：`foods?destination_id=phuket`（美食目錄）。

不連：`thailand-entry-2026-tdac`（intel，2026-12-31 過期，依 README 的時效規則不連，入境只寫一句以外交部領事事務局與泰國移民局公告為準）、`thailand-esim-sim-wifi`（上網不是本篇主題，也不放 `related`）、`krabi-airport-transport-where-to-stay`（普吉接喀比是機場交通篇與跳島篇已經寫過的事，本篇不重複）、本批其他 18 篇（主題無關）。台灣那 20 篇沒有 zh-TW 版，不連。
**同批互連的不對稱是刻意的，兩邊都要有交代**（2026-09-20 審查補）：本批第 13 篇 `pattaya-koh-larn-day-trip-from-bangkok` 在它的「不連」清單裡寫「同批的清邁兩篇與普吉篇：跟芭達雅沒有動線關係，不連也不放 `related`」，
本篇同樣不連第 13 篇——普吉在南、芭達雅在東，不同一趟行程，硬連會變成連結列表。本批第 10 篇 `chiang-mai-airport-transport-where-to-stay` 也只把本篇列在它的「不連」清單裡，不是連結。
**`related` 四篇維持不動**（機場交通、跳島、寺廟禮儀、東南亞季節），其中只有寺廟禮儀篇是同批、而且雙向互列。

## 圖解

`diagram-1.svg`，viewBox `0 0 1600 900`，放在 H2-1 的表一之後、H2-2 標題之前。字型串照 `docs/life-ai-series-brief.md` 第 6 節的預設串**加 Noto Sans Thai**（圖上有泰文地名的英文拼法就好，泰文字不上圖；泰國主題照第七批 README 加這個字型串）。
所有 `font-size` ≥15，不外連，右下角 `© Mokaair 製圖 2026`，要有 `role="img"`、`<title>`、`<desc>`。一張圖只講一件事：**普吉島上這四站由北往南的相對位置，以及哪一段有公車、哪一段沒有**。註明「示意圖，方向與距離非比例」。

- 畫一個直立的島形色塊，由上到下依序標四站：
  1. 「普吉老城 Phuket Old Town」，底下小字「他朗路｜泰華博物館 200 泰銖」
  2. 「查龍寺 Wat Chalong」，底下小字「參拜免費」
  3. 「普吉大佛 Big Buddha」，底下小字「Nakkerd 丘頂｜出發前確認開放」
  4. 「神仙半島 Phromthep Cape」，底下小字「島的最南端｜夕陽」
- 左側在老城旁邊拉一個小圈：「蘭山觀景台 Rang Hill」，標「半天版的替代站」。
- 右側在第 3 站與第 4 站之間拉一個小圈：「卡隆觀景台 Karon View Point」，標「卡塔、卡隆盡收眼底」。
- 站與站之間畫三段連線，**用線型分「有公車」與「沒有公車」**：
  - 老城內部與老城周邊：實線，標「Dragon Line 免費」
  - 老城（巴士總站 1）到芭東：實線，標「Route 2｜50 泰銖」
  - 老城 → 查龍寺 → 普吉大佛：**虛線**，標「沒有公車，要包車」
  - 卡隆觀景台 → 神仙半島：實線細一點，標「Route 1｜100 泰銖，只有三班到神仙半島」
- 右下角圖例（實線＝有公車、虛線＝要包車）與版權字樣；右上角一行小字「開放時間與班次見內文表格」。
- **圖上的數字只有這些，全部要出現在正文：200、50、100、三班。** 不要畫開放時間、不要畫 17:22／17:47／19:02、不要畫 45 公尺、不要畫班距分鐘數。
- 標籤用中文加英文；英文只用官方頁上的拼法（Phuket Old Town、Thalang Road、Wat Chalong、Big Buddha、Phromthep Cape、Karon View Point、Rang Hill、Dragon Line）。

## 撰稿時要小心

(1) **普吉大佛那一段要寫成「可以整段刪掉」的支線。** 2024 年 8 月 23 日 Nakkerd 丘發生山崩之後大佛曾經關閉，本次**沒有讀到任何可引用的官方開放公告**：TAT 主站景點頁讀不到（Nuxt 殼／403）、普吉府政府 403、TAT Newsroom 三個關鍵字都沒有稿、大佛官網已轉址到臉書、臉書 curl 只拿得到登入殼。
規格的做法是：把它寫成 H2-3 底下的一個 H3，段落裡不放任何其他站的動線資訊，並在表一那一格與 H2-1 的「半天版」句子裡先寫好替代站（蘭山觀景台或直接南下），**這樣哪天要整段拿掉，只需刪掉那個 H3 與表一那一列，其他段落一個字都不用改**。
正文對開放狀態只能這樣寫：「泰國觀光局東京辦事處的景點頁寫 08:00 到 19:00，但那一頁沒有反映 2024 年 8 月山崩之後的狀況，官方網址現在會直接轉到臉書專頁；出發前先確認當天是否開放。」
**不准寫的**：任何第三方部落格／媒體講的重開日期（網路上流傳 2026 年 1 月 1 日短暫重開、3 天後又關、2026 年 3 月 3 日正式重開）、第三方講的新時間（09:00 到 18:00、最後入場 17:30）、第三方講的「免費入場」，以及「林業廳 25 項條件」這類轉述。一個字都不能寫，因為本次沒有讀到任何官方頁。

(2) **研究檔說「大佛官網 curl 200、站台可讀」是錯的。** `https://www.mingmongkolphuket.com/Index` 回 `301 → https://www.facebook.com/mingmongkolphuket`，curl 最後拿到的 200 是臉書的頁。sources 可以列這個網址並註明「已轉址到官方臉書專頁」，**但不要寫成「官網寫 XXX」**。

(3) **季節的月份用區域頁那一組，不要用神仙半島頁那一組。** `areainfo/phuket` 寫「乾期は11月～3月で、4月～5月が暑期、6月～10月がグリーンシーズン」，這和既有的 `phuket-airport-transport-where-to-stay`（block 31）與 `phuket-phi-phi-james-bond-island-hopping`（block 34）一字不差。
但 `laem-phromthep` 那一頁寫的是「乾期(11～2月)から暑期(3～5月)」，**月份切法不一樣**。同一個官方站兩頁不一致時，本篇照區域頁寫，以免和既有兩篇打架；神仙半島頁那句只用來支持「乾季到熱季天空與海最清澈」，不引用它的月份。

(4) **Smart Bus 的老城導覽是營運者的部落格，不是觀光主管機關。** 「Thalang Road 是老城主街」「Soi Romanee 是一排粉藍街屋」「1907 年渣打銀行」「側巷有二十多幅壁畫、咖啡店可拿地圖」這四條都出自那一頁，引用時要在句子裡寫明出處（例如「Smart Bus 官網的老城導覽寫」）。
**「the oldest bank building in Thailand」不要翻成正文**——那是營運者自己下的最高級敘述，沒有主管機關背書。那一頁點名的餐廳（Tu Kab Khao、Mee Ton Poe）**一律不寫**，餐廳是美食目錄的事。

(5) **地名照目的地目錄。** `apps/api/app/hotspots/areas.py` 的 HKT 分區是「普吉老城」「芭東」「卡隆」（Karon，**不是卡倫**）「卡塔」「查龍／大佛」「拉威／神仙半島」「他朗／斯里納斯國家公園」；`apps/api/app/hotspots/bootstrap.json` 的熱點名是「普吉老城」「查龍寺」「普吉大佛」「神仙半島」。
- **Karon 一律寫「卡隆」**，所以觀景台寫「卡隆觀景台」，不要寫「卡倫觀景台」。
- **Thalang 在目錄裡是「他朗」**，所以老城主街寫「他朗路（Thalang Road）」，「塔朗路」放 `aliases`。順帶在正文括號註一句「島北邊的他朗是另一個行政區，和老城這條他朗路不是同一個地方」，避免讀者混淆。
- 神仙半島的英文：`hotspots/bootstrap.json` 的熱點名是「神仙半島」、`names.en` 是 **Phromthep Cape**、`aliases` 收 **Promthep Cape**，Smart Bus 班表圖也寫 Phromthep Cape，TAT 寫 Laem Phromthep；本篇正文寫「神仙半島（Phromthep Cape）」。
  **注意 `hotspots/areas.py` 的區域標籤寫的是「拉威／神仙半島」＝`Rawai & Promthep Cape`（少一個 h）**，所以「目的地目錄一律寫 Phromthep」並不成立——同一套目錄裡兩種拼法都有，只是熱點那一筆以 Phromthep 為主名。既有的 `phuket-airport-transport-where-to-stay` `blocks[24]` 寫 Promthep Cape，是目錄收的 alias、不是錯字，統一與否列在下一節。
- **「大佛」一律寫全稱「普吉大佛」**（協調者 2026-09-20 裁決）：本批第 13 篇 `pattaya-koh-larn-day-trip-from-bangkok` 寫的是另一座「芭達雅大佛寺（Wat Phra Yai）」，在春武里府，和普吉這一座無關。
  **正文、summary、表格、list、FAQ 與圖解標籤任何一處都不要只寫「大佛」**（「查龍寺與大佛」要寫成「查龍寺與普吉大佛」）。唯一的例外是 TAT 頁上的專有名詞「大佛公園」，而且它只出現在 H3 內文、上下文已經是普吉大佛那一段。`hotspots/bootstrap.json` 的熱點名就是「普吉大佛」（`names.en` 是 Phuket Giant Buddha），TAT 的英文名是 Phra Phutthamingmongkhol-akenagakhiri Buddha Image，**正文不要用這兩個英文長名當標題**，括號要附英文就寫 Big Buddha。

(6) **娘惹博物館不是老城景點。** `peranakan-phuket-museum` 的官方地址是 124/1 Moo 1 Sri Soonthorn, Thalang，官方寫「プーケット・タウンから車で約30分」。它和老城步行路線是兩回事，**本篇不寫它，也不要把它的 300／150 泰銖與 09:00 到 18:00 混進老城那一段**。老城裡那一座是泰華博物館（200 泰銖、週一休館）。
同理，塔朗國立博物館（Thalang National Museum）也在他朗，而且 TAT 頁的開放時間欄明顯是資料錯誤（「9時半から／21時半(1日2回)」），**整筆不寫**。

(7) **Smart Bus 官網改版了，而且自己跟自己打架，兩處都要照班表圖寫。**
- 分頁標題寫「Bus Terminal 2 → Patong Beach」，但同一頁掛的班表圖（2026-01-15 起）第一欄是「สถานีขนส่งภูเก็ต 1 ／ Phuket Bus Terminal 1」，Dragon Line 路線圖上也標 บขส.1。**照班表圖寫「普吉巴士總站 1」**，並在句子裡留一句「官網分頁的文字寫 Bus Terminal 2，兩處不一致，以現場站牌為準」。第七批 ERRATA 已經為既有那篇做過同樣的判斷。
- 頁面的 `meta description` 寫「Hourly departures Airport → Rawai (06:30–17:30)」，**和班表圖的 08:15 到 23:30 完全對不上**。Route 1 的時刻本篇本來就不寫（交給機場交通篇），**千萬不要把 06:30–17:30 這一組寫進任何地方**。

(8) **查龍寺與普吉大佛沒有公車這件事，要寫成「班表上沒有這些站」，不要寫成「絕對沒有任何交通工具」。** 依據是 Route 1／Route 2／Dragon Line 三張班表圖與路線圖上都沒有查龍寺或普吉大佛的站名。用語寫「Smart Bus 的三條路線班表上都沒有它們」最安全。

(9) **查龍寺的正式名稱兩個官方頁拼法不同**：TAT 寫 Wat Chaithararam、寺方官網寫 Wat Chaiyathararam。正文用「查龍寺」，括號可以寫「正式名稱官方頁上有 Wat Chaithararam 與 Wat Chaiyathararam 兩種拼法」，**不要挑一個說成唯一正確**。
另外 60 公尺舍利塔、三層、頂層平台、玻璃展示佛骨這四點只有查龍寺官方網站有，兩邊的出處要分開記進 `notes.md`。
**查龍寺的開放時間有兩個官方數字，取的是觀光局那一邊，理由要寫出來**（2026-09-20 審查覆核，與同批第 14 篇 `thailand-temple-etiquette-dress-code` 同一套裁決）：
查龍寺官方網站的 FAQ 兩處都寫 07:00 到 17:00（開放時間那一問，以及「最佳時段 07:00–09:00」那一問，不是單一筆誤），泰國觀光局東京辦事處寫 08:00 到 17:00。
**表一、summary 第三句、H3 與 FAQ 一律寫 08:00 到 17:00**，正文用一句話交代另一個數字並寫「以現場告示為準」。理由三條：
(a) `wat-chalong-phuket.com` 是觀光局頁面 URL 欄列出的該寺網址，但站上同時在賣普吉市區觀光行程、形式上像委外經營，開放時間這種會變的數字以政府觀光機構的頁為基準比較穩；
(b) 08:00 是兩個數字裡較晚的那一個，照它排不會提早到現場吃閉門羹，早到的人也只是多等；
(c) 第 14 篇的表格與 summary 也是 08:00 到 17:00，兩篇一字不差。
**不要把理由寫成「那個站不算官方」**——參拜免費那一條它也寫得到（「no charge to enter the temple」），引用時寫「查龍寺官方網站」，**不要寫成「寺方公告」**。
順帶注意兩個官方頁對 1876 年那件事的說法不同：TAT 寫「錫採掘者が反乱を起こした際に、地元の村人たちを救った高僧ら」，查龍寺官方網站寫僧人「led the citizens of Chalong Sub district fighting against the Chinese rebellion in 1876」。**正文照 TAT 那一句寫（規格 H3 用的就是它），不要把兩種說法混成一句。**

(10) **「查龍」有兩個東西容易混**：本篇寫的是查龍寺（Wat Chalong），既有的 `phuket-phi-phi-james-bond-island-hopping` block 29 寫的「查龍港（Chalong）搭快艇約 20 分」是碼頭，兩者是同一區的不同地點。正文提到查龍時，要讓讀者看得出講的是寺還是港。

(11) **大佛的尺寸寫法**：TAT 東京寫「幅25.454m、高さ45m」「1万個以上の大理石」「大理石造り」。正文可以寫「高 45 公尺、寬 25.454 公尺，外面貼了一萬多塊大理石」，**不要寫成「整座用大理石雕成」**；TAT 頁上那個 42/14 Moo 2, Thepkrasattri Road 的地址是聯絡地址、不是丘頂位置，**地址整筆不寫**。

(12) **卡隆觀景台改過名，這是最容易寫錯的一條。** 官方頁原文寫「以前はカタ・ビューポイントと呼ばれていましたが、名称が変わっています」——舊名是卡塔觀景台。正文寫「卡隆觀景台」，可以加一句「舊名卡塔觀景台」，並把「卡塔觀景台」放進 `aliases`。它看得到的三個海灘是卡塔亞伊、卡塔諾伊與卡隆，**名字裡是卡隆、看到的海灘有三個，不要寫成「只看得到卡隆海灘」**。

(13) **神仙半島那三班延駛車的方向要寫對。** 班表圖的方框是兩行：往程是「Rawai >> Phromthep Cape 17:22 / 17:47 / 19:02」，回程是「Phromthep Cape >> Kata/Karon/Patong/Airport 17:23 / 17:48 / 19:03」。
**回程那一組只差 1 分鐘，是同一班車掉頭**，不要寫成「一小時後才有回程」；也不要把黃色標示的機場發車時間（14:00、15:00、16:00）和拉威發車時間（17:22、17:47、19:02）寫混。班表圖上同時標著「Last update, 16 Jan 2026」，撰稿當天要確認圖有沒有換版。

(14) **素食節不寫日期。** 官方頁只寫「毎年10月頃に9日間」，沒有年度日期；TAT Newsroom 2026 年的稿還沒出。正文寫「約在每年 10 月、為期九天，日期每年不同」，**不要寫任何一組月日，也不要寫「今年是幾月幾日」**。

(15) **三座華人神廟不要自創中文譯名。** 官方頁只有 Chui Tui（Jui Tui）、Put Jaw、Saeng Tham 三個拼法和日文片假名，目的地目錄裡沒有它們。正文寫成「官方頁的拼法是 Chui Tui、Put Jaw、Saeng Tham」，功能照 `areainfo/phuket` 的原文（消災、姻緣、學業與生意），**不要寫成「斗母宮」「觀音廟」這類自己找的中文名**。

(16) **蘭山觀景台的開放資訊只有「無休」。** 官方頁的基本情報欄就只有這一項，沒有時間、沒有費用。正文寫「官方頁只寫『無休』，沒有列開放時間與費用」，**不要補「24 小時開放」或「免費」**。同理卡隆觀景台與神仙半島的頁上都沒有時間與費用，一律寫「以現場為準」。

(17) **幣別與單位**：一律寫泰銖（不寫 THB、฿、泰幣）；公里、公尺、分鐘照官方頁的數字；時間全文用 24 小時制，和既有兩篇普吉文章一致。表格 4 欄上限、每格 ≤300 字。

(18) **數字要四處一致**（標題、summary、兩張表、圖解、FAQ）：200（泰華博物館）、09:00–17:00、週一休館、08:00–17:00（查龍寺，觀光局；查龍寺官方網站的 07:00 只出現在正文交代兩個數字的那一句）、08:00–19:00（普吉大佛，TAT 頁）、45 公尺、25.454 公尺、60 公尺（舍利塔）、8 公里、15 到 20 分、30 分、20 到 30 分、30 到 40 分、40 分（市區到神仙半島）、16:00–22:00（週日步行街）、2013 年 9 月 29 日、07:00–19:00（Dragon Line）、每 30 分鐘、50 泰銖、100 泰銖、06:00、20:00、21:00、1 小時、1 小時 10 分、17:22／17:47／19:02、17:23／17:48／19:03、14:00／15:00／16:00、07:00–18:00（雙條車）、1876 年、1907 年、1934 年、2001 年、10 到 15 分、九天、40 分鐘（夕陽前）。改一處要全改。
**注意三個「30 分」不是同一件事**：查龍寺到芭東約 30 分（車程）、神仙半島到芭東約 30 分（車程）、Dragon Line 每 30 分鐘一班（班距）；還有兩個「1907 年」（渣打銀行舊址、Jui Tui 神廟）也別寫混。

## 上線後與交叉檢查

- **補反向連結（同一個 PR）**：`phuket-airport-transport-where-to-stay` 的 `blocks[24]` 是 `table`（住哪一區），**表格的 rows 放不了 inline**，不要動它。要補連結就改 `blocks[25]`——那是 `paragraph`（「Route 1 有部分班次從拉威延駛神仙半島…」開頭那一段），整塊改成 `rich_paragraph`（原文拆成 `text` inline，在「神仙半島」後面插 `article` inline 連 `guides/howto/phuket-old-town-big-buddha-viewpoints`，連結文字講「老城、查龍寺、大佛與南端觀景台一天怎麼排」），**文字一個字都不改**。
  次選是 `blocks[28]`（Route 2 與 Dragon Line 那一段，也是 `paragraph`）。**兩處只做一處就好**，首選 `blocks[25]`。
- **可選**：`phuket-phi-phi-james-bond-island-hopping` 的 `blocks[41]` 已經是 `rich_paragraph`（連喀比交通篇），上線後可以在它之前新增一個 `rich_paragraph`，講「不出海的那一天怎麼過」連本篇；不是必要，版面允許再加。
- **既有文章待修（列進「既有文章補連第八批」那張票，不要在本篇的 PR 裡順手改數字）**：
  1. ~~`phuket-airport-transport-where-to-stay` 的 `blocks[37]` 用舊參數 `foods?city=phuket`，要改成 `destination_id`~~ **——2026-09-20 審查撤銷這一條，不要開票。**
     票 `2026-09-14-food-links-city-param-ignored` 與 `2026-09-19-foods-page-drops-city-on-server` 都已結案（在 `tasks/done/`），`apps/web/lib/foods.ts` 現在兩個參數都讀
     （`const destinationId = (params.get("destination_id") ?? "").trim() || (params.get("city") ?? "").trim();`，註解寫明是為了既有 60 個內容包裡的 `?city=` 連結）。
     所以 `blocks[37]` 的 `?city=phuket` **能正常篩選、不是錯**，同城的 `phuket-phi-phi-james-bond-island-hopping` `blocks[43]` 寫 `?destination_id=phuket` 也對。
     **本篇這種新文章仍然統一用 `destination_id`**（見「站內連結」第 7 條），但不要把既有文章的 `?city=` 列成待修項。
  2. 同一篇 `blocks[28]` 寫「Smart Bus Route 2 從 Phuket Bus Terminal 1 出發」——今天官網分頁的文字改寫成 Bus Terminal 2，班表圖仍是 Terminal 1。**結論不變（照班表圖），但正文可以補一句官網文字與班表圖不一致**。
  3. 同一篇 `blocks[24]` 的神仙半島英文寫 `Promthep Cape`，`hotspots/bootstrap.json` 的主名與 Smart Bus 班表圖寫 `Phromthep Cape`。
     **這不是錯字**：`bootstrap.json` 的 `aliases` 收了 `Promthep Cape`，`hotspots/areas.py` 的區域標籤也寫 `Rawai & Promthep Cape`。
     **協調者 2026-09-20 裁決：全站統一拼法不在本批範圍**（會動到 `apps/api/app/hotspots/areas.py`）。
     **本篇照目的地目錄現況寫「神仙半島（Phromthep Cape）」就好，撰稿者不要去改既有文章、也不要改 `areas.py`**；
     「目錄與既有機場篇拼法不一致」只留一條低優先的後續事項，由協調者之後開票。
  4. 同一篇 `blocks[18]`、`blocks[19]` 的 Route 1 首末班（08:15 到 23:30）出自班表圖，今天仍然成立；但**官網改版後的 `meta description` 寫 06:30–17:30，和班表圖矛盾**，下一次重查那篇時要確認官方到底以哪一組為準。
- **每次改版重查**：Phuket Smart Bus 的官網 2026 年改版過，班表圖的「Last update」目前是 2026-01-15（Route 2）與 2026-01-16（Route 1、含神仙半島延駛那三班）。
  **每條路線的分頁掛的是兩張圖（去程一張、回程一張），規格的「官方來源」只列了去程那張**，撰稿當天兩張都要開：
  Route 1 北上（拉威→機場）是 `storage/timetables/rawai/uxwoQs6R9i1cR4IiiOF8hUPCfm2nTMucYMO7ihat.jpg`，Route 2 的第二張是 `storage/timetables/patong/aQIvCoPZ1KHn2wYMOanIqtJVlG0RbBtMJStKIszc.jpg`。
  2026-09-20 審查時確認：**神仙半島延駛的那個方框只在 Route 1 的去程圖上**，北上圖沒有神仙半島這一欄，兩張圖都沒有卡隆觀景台、查龍寺或普吉大佛的站。圖一換版，本篇的表二、H2-4 的三班延駛與圖解的「只有三班到神仙半島」都要跟著改，`phuket-airport-transport-where-to-stay` 也要同一個 PR 一起看。
- **2026 年 10 月**：普吉素食節在 10 月、為期九天，TAT Newsroom 每年 10 月初會出年度稿（2023、2024、2025 都有）。稿一出就回頭把老城那一段的「日期每年不同」換成「2026 年是 X 月 X 日到 X 月 X 日」，並在 sources 補那一篇。
- **大佛的開放狀態（最優先的追蹤項）**：只要下列任何一個出現可引用的官方說法，就把 H2-3 那個 H3 的「出發前先確認」改成明確的開放時間，並同步改表一那一列、summary 第四句與 FAQ 第一題：
  - `www.tourismthailand.org/Attraction/phra-phuttha-ming-mongkhon-ek-nakkhiri-phuket-big-buddha` 變成讀得到（目前是 Nuxt build error 殼／WebFetch 403）；
  - TAT Newsroom 出關於大佛的稿（WP REST API `?search=Big+Buddha` 目前查不到）；
  - 普吉府政府 `phuket.go.th` 不再回 403；
  - TAT 東京的大佛頁換掉 `https://www.mingmongkolphuket.com/Index` 這個已經轉址的網址，或補上封閉／重開的說明。
  反過來，**如果撰稿或上線當天查到官方確認大佛仍然關閉**，就把那個 H3 整段刪掉、表一刪掉那一列，其他段落不動（規格就是照這樣排的）。
- **同批互連（第八批清單第 12 條）**：本篇連出去的四篇裡，`thailand-temple-etiquette-dress-code` 是本批第 14 篇，**兩篇必須同一批上線**，不然 `guides-links-check` 會紅。兩篇要一字不差的共用事實有兩條：
  **(a) 進殿要遮肩過膝、脫鞋**（協調者 2026-09-20 指定的逐字寫法，**只有本篇與第 13 篇要一字不差**；第 11 篇清邁夜市一個服裝字都不寫）——本篇只寫這一句，其餘（大皇宮十一條清單、參拜四點組、女性不得碰觸僧侶）全部在對方那篇，本篇一個字都不重複；
  **(b) 查龍寺 08:00 到 17:00、參拜免費**——第 14 篇的表格與 summary 也是這一組，兩篇同時要有那句「查龍寺官方網站的 FAQ 寫 07:00 到 17:00」的交代。任何一邊改時間，兩篇同一個 PR 一起改。
- **與本批第 13 篇的「大佛」不能混**（2026-09-20 審查補）：第 13 篇 `pattaya-koh-larn-day-trip-from-bangkok` 寫的是春武里府的「芭達雅大佛寺（Wat Phra Yai）」，每天 10:00 到 20:00；本篇寫的是普吉的「普吉大佛」。
  兩篇都不簡稱「大佛」，`aliases` 也不收單獨的「大佛寺」。上線後用站內搜尋確認這兩個詞不會互相撈到對方。
- 自檢時確認 `destinations/phuket` 與 `foods?destination_id=phuket` 都通過（`apps/api/app/foods/area_catalog.py` 的普吉分區有「普吉老城」，美食目錄的連結文字可以點名老城）。
- phuket 的 activities 與 transport 合作方案在後台核准後，打開正式站本文確認兩個 offer 真的畫得出來、heading 與商品對得上。
