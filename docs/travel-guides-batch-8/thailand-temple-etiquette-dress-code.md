# 14. `thailand-temple-etiquette-dress-code`

泰國寺廟與王宮的服裝與禮儀：大皇宮官網那份十一條禁止清單、進殿脫鞋與拍照的官方規定、女性不可碰觸僧侶，以及一次完整的參拜流程

| 欄位 | 值 |
| --- | --- |
| kind | `howto` |
| destination_id | `null` |
| topics | `etiquette`, `culture` |
| valid_until | `null` |
| featured | `true` |
| display_order | `1340` |

規格 2026-09-20 定稿：研究檔（`research-thailand.md` 第 6 節）列的 13 個核心數字全部重新打開官方頁核對過，另外補讀了四份研究檔沒有的官方來源（大皇宮官網 FAQ 與 schedules 頁、王室辦公室 2567 年參觀與攝影法規 PDF、臥佛寺官網的 Visit plan 與 Tips for Visitors、查龍寺官網 FAQ）。
已對照 main 上的既有文章（`bangkok-4-day-itinerary`、`ayutthaya-day-trip-from-bangkok`、`chiang-mai-3-day-itinerary`、`chiang-rai-2-day-itinerary`、`chiang-mai-old-city-slow-day`）與本批第 11、12、13 篇。撰稿當天要再打開一次核對，`checked_on` 填實際打開那天。
通用規則見本批 README；第七批的 [README](../travel-guides-batch-7/README.md)、[ERRATA](../travel-guides-batch-7/ERRATA.md) 與第六批的 [ERRATA](../travel-guides-batch-6/ERRATA.md) 仍然適用。

站上的泰國文章沒有一篇是禮儀主題。既有文章零散寫過「遮肩過膝、脫鞋進殿」，但沒有大皇宮那份逐條的禁止清單、沒有參拜四點組與五步驟、沒有王室與國歌的規矩、沒有女性不得碰觸僧侶，也沒有玉佛寺大殿內不能拍照這條有法規依據的規定。
**本篇是全站泰國文章的禮儀總表**：本批第 11、12、13 篇各寫一句並連過來，所以各寺的具體服裝規定一律集中在本篇，那三篇不重列。

## 切角與段落

回答一件事：進泰國的寺廟與王宮該穿什麼、不該做什麼，讓讀者在出門前就把衣服穿對、進門後知道每一步要做什麼，不用在門口租腰布或被擋回去。
字數 1,800–4,200，**目標 3,400–3,600**，每個 H2 的約略字數寫在標題後面。配額逐項攤開（審查時補的，寫作時照這張對）：summary 250 ＋ 開頭 260 ＋ H2-1 620 ＋ H2-2 620 ＋ H2-3 460 ＋ H2-4 700 ＋ H2-5 380（四點組＋五步驟＋離開前三件事）＋ 行前檢查 `list` 90 ＋ 結尾兩句 50 ＋ FAQ 230 ＋ 兩個城市頁 `link` 36 ＝ **3,696**，**已經略高於 3,600 目標上緣（上限 4,200 還有空間），撰稿時要主動砍到 3,600 以內**。**寫超了就照這個順序砍**：先砍 H2-4 表後三段的大皇宮實務句（語音導覽與線上票那兩件事可以各縮成半句）、再砍 H2-1 王室辦公室法規那一段的鋪陳；**十一條清單、五個步驟、六列表格的數字、女性不碰觸僧侶那三條一個字都不能砍。** 表格一張（4 欄 6 列），callout 三個，圖解一張，**offer 一個都不放**（`etiquette` 主題，照第六、七批原則——第七批 README 第 145 行明列 `etiquette` 原則上不放）。
`destination_id` 是 null，但**結尾要放兩個城市頁 `link` 區塊**：`https://mokaair.com/zh-TW/destinations/bangkok` 與 `https://mokaair.com/zh-TW/destinations/chiang-mai`；**美食目錄的 `link` 一個都不放**。依據是協調者 2026-09-20 的全批裁決：`destination_id` 是 null 的文章，只要正文點名到具體城市、而那些城市又在目的地目錄裡，就在結尾放**最多兩個**城市頁 link（main 上 41 篇 null 旅遊文有 34 篇這樣做）；美食目錄的 link 需要 id，null 文章一律不放。本篇 H2-4 的六座寺廟裡曼谷佔三座（大皇宮與玉佛寺、臥佛寺、鄭王廟）、清邁佔素帖山雙龍寺，兩個 id 都在 `apps/api/app/destinations/catalog.py`（`BKK: bangkok`、`CNX: chiang-mai`）。清萊與普吉也在目錄裡，但**裁決上限是兩個，不要加第三、第四個**；大城不在目錄裡，本來就放不了。兩個 link 的字數（各一句，合計約 36 字）已算進下面的配額。

**全篇最重要的寫法規則：分清楚「規定」與「建議」。**
- 寫成「規定」的，只有官方頁明文禁止或明文要求的條目：大皇宮官網的 Dress Code 清單與王室辦公室 2567 年法規、臥佛寺官網 Tips for Visitors 的 `required` 與 `prohibited`、查龍寺官網 FAQ 的 `required` 與 `never allowed`。
- 泰國觀光局東京辦事處那兩頁用的是「避けてください」「好ましくありません」「気をつけましょう」，**一律寫成「泰國觀光局建議」「照泰國的通則」**，不要寫成「規定」「禁止」「違者罰款」。唯一的例外是禁菸那一句，原文自己寫了罰款。
- **機構名稱的寫法**：第一次出現寫「泰國觀光局東京辦事處」，之後一律簡稱「泰國觀光局」（既有 `bangkok-4-day-itinerary`、`chiang-mai-3-day-itinerary` 寫「泰國觀光局東京辦事處（TAT 東京）」，`chiang-rai-2-day-itinerary` 寫「泰國觀光局（TAT）東京辦事處」，兩種都指同一個單位，本篇不用 TAT 這個縮寫）。大皇宮那邊的主管機關寫「泰國王室辦公室」（Bureau of the Royal Household）。
- 查不到官方出處的常識（例如「用右手遞東西」「不要背對佛像走出大殿」「女生要帶絲巾」）可以寫成建議，但要寫成建議句，不要寫成規定句，也不要掰出處。

(1) summary 區塊（第一個區塊，4 句，每句 ≤300 字，只重述正文有的事實，數字逐字照正文）：
- 第一句是答案：進泰國的寺廟與王宮，最保險的穿法是有袖上衣加長褲或過膝裙、可以脫的鞋；泰國最嚴的一份官方服裝清單是大皇宮官網的十一條，只要這十一條都避開，全泰國的寺廟都進得去。
- 第二句是決定條件：大皇宮外國人 500 泰銖、每天 08:30 到 16:30、售票只到 15:30，臥佛寺 300 泰銖、08:00 到 19:30，鄭王廟 200 泰銖、08:00 到 18:00，清萊白廟 200 泰銖、08:00 到 17:00，清邁素帖山雙龍寺 30 泰銖、05:00 到 21:00，普吉查龍寺免費。
- 第三句是文章給的數字：進殿一律脫鞋，參拜用的花、線香、蠟燭、金箔四點組在寺廟門口常見約 20 泰銖，最慎重的禮拜要叩三次；玉佛寺大殿內不能拍照，全泰國的寺廟都禁菸、違反會罰款。
- 第四句是注意事項：女性不可碰觸僧侶的身體、僧衣與隨身物，在街上與大眾運輸上也一樣；每天早上 8 點與傍晚 6 點公共場所播國歌時，多數人會停下起立。
正文改了 summary 要跟著改。

(2) 開頭 paragraph（第二個區塊，2 段，約 260 字）：
第一段：泰國的寺廟是觀光景點，也是還在運作的宗教場所與王室場域，服裝與行為的規定是真的會在門口擋人的，不是客套話。全泰國沒有一份通用法規，但大皇宮官網列了十一條不能穿的衣服，那是最嚴的一份；只要按它挑衣服，從曼谷舊城到清萊、清邁、普吉都不會被擋。
第二段：這篇先講穿什麼，再講進門之後的每一個動作（脫鞋、坐姿、拍照、碰觸），接著是僧侶與王室這兩件不能靠感覺的事，最後把六座最常去的寺廟的門票、時間與官方寫明的規定整理成一張表，加上一次完整的參拜流程。
第二段最後要交代來源與查證日：規定與票價 2026 年 9 月依泰國王室辦公室的大皇宮官網與 2567 年參觀攝影法規、臥佛寺官網、查龍寺官網與泰國觀光局東京辦事處查證；鄭王廟、白廟、素帖山雙龍寺沒有可讀的官方網站，票價與開放時間引泰國觀光局。
**開頭不寫「本文介紹」這類後設句，不寫任何一座寺廟的行程建議**（行程歸各城市的文章）。

(3) H2-1「先看衣服：大皇宮的十一條，是全泰國最嚴的一份官方清單」（約 620 字）
- 先一段：大皇宮官網 Dress Code 區塊的原文是「Visitors to The Grand Palace must dress appropriately because The Grand Palace is a place of reverence for the Thai people」，後面接十一條不能穿的衣服。把十一條寫成 `list`（一項一行，中文在前、官網英文在後的括號可省，但十一條一條都不能漏）：無袖上衣、背心、露肚上衣、透膚上衣、熱褲與短褲、破洞褲、緊身褲、單車褲、迷你裙、褲裙、睡衣式服裝。
- 接一段：王室辦公室 2567 年（2024 年）的參觀與攝影法規寫得比英文頁更細，多了兩件英文頁沒有的：**七分褲也不行**，穿泰式披肩（สไบ）的人裡面要加長袖上衣；同一條的開頭寫「必須穿著端莊整潔，或穿自己國家正確的傳統服裝」。這兩句要寫，**但不要逐條翻譯整段泰文法規**，也不要自己替泰文詞彙發明中文名稱（詳見「撰稿時要小心」第 3 條）。
- 再一段：一般寺廟沒有這麼細的清單，泰國觀光局的通則是「男女都要避免無袖、短褲、破洞牛仔褲這類露出多的衣服」；查龍寺官網講得最具體，**肩膀、胸口與膝蓋都必須遮住**，避免無袖上衣、短裙與露腰上衣。臥佛寺官網則是「請穿著端莊，不要穿短褲，長褲可以」，另外一句寫**女性不可穿膝蓋以上的短褲**。實務上的結論：有袖上衣＋長褲或過膝裙＋容易脫的鞋，一套走遍。
- 放一個 warning callout：**不要指望門口租得到腰布。** 泰國觀光局的原文是「有些地方可以付費租腰巾，但穿不合適的衣服也可能被拒絕入場」——是「有些地方」，不是每一座；大皇宮官網從頭到尾沒有提供租借服務這件事，別把「到現場再租」當成計畫。帶一條薄圍巾或一條長褲在包包裡最省事。
- 段末一句 article inline → `bangkok-4-day-itinerary`（howto，既有）：連結文字講「曼谷舊城那天怎麼排：大皇宮、臥佛寺、鄭王廟與河邊日落」，**本文不寫行程**。

(4) H2-2「進門之後：脫鞋、坐姿、拍照，哪幾條有官方依據」（約 620 字）
- 脫鞋：臥佛寺官網寫「進入宗教建築前必須脫鞋，並放到鞋架上」，查龍寺官網寫「寺廟建築內絕對不可以穿鞋」。這是兩份官方頁都明文寫的規定，不是禮貌問題。實務一句：穿好脫好穿的鞋，別穿要綁鞋帶的。
- 坐姿與腳：泰國觀光局寫腳底和左手一樣被視為「不淨」，參拜時注意坐的方向、**不要把腳底朝著佛像**；也不要跨過別人的腳，在車上或劇院非過不可時先出聲請對方挪一下。這兩條寫成「泰國觀光局的通則」。
- 碰觸：王室辦公室法規明文禁止碰觸、拿取或在建築裝飾上塗寫，例子舉的是壁畫、彩繪玻璃與各種塑像；查龍寺官網也寫「不要碰觸塑像或其他佛教聖物」。
- 拍照，分兩層寫，**這一段是本篇最有價值的地方**：
  - 一般寺廟可以拍。臥佛寺官網寫「在寺廟與古蹟裡可以拍照，但**絕對不可以踩上佛像**，只有獲准的人員才能爬上佛像清潔與供奉」；查龍寺官網 FAQ 直接寫照片與錄影都允許。
  - 大皇宮與玉佛寺是另一套。王室辦公室法規准許一般遊客用一般相機拍觀光照，但**准許拍攝的範圍是「玉佛寺周邊，不含大殿內部」**——也就是供奉玉佛的那間大殿裡不能拍。同一份法規還禁止：用照明器材、吊臂、滑軌、相機用無線麥克風與裝了相機的無人機（大皇宮官網另有一塊 No Drone Zone，寫明禁止無人機飛越大皇宮上空）；禁止拍成帶商業或機構宣傳看板的畫面；**禁止觀光以外目的的拍攝，法規舉的例子就是婚紗照**。另外也禁止帶武器、仿製武器與寵物進入，禁止雷射筆與指示棒。
- 放一個 info callout：**「可以拍照」和「可以進去拍」是兩件事。** 大皇宮與玉佛寺的規定寫在王室辦公室 2567 年的法規裡，拍不拍得成以現場人員與告示為準；其他寺廟多半可以拍，但殿內若貼了禁止攝影的圖示就是不行，看圖示不要看別人有沒有在拍。
- 段末：這一段之後放 diagram-1。

(5) H2-3「僧侶與王室：兩件不能靠感覺的事」（約 460 字）
- 僧侶（三條，兩份官方頁都寫）：臥佛寺官網寫「僧侶與男性可以有肢體接觸，但**女性禁止與僧侶或沙彌有肢體接觸**」，同一段還寫**女性不可進入保留給僧侶做法事的所有區域**；泰國觀光局寫女性不可直接碰觸僧侶的身體、僧衣與隨身物品，托缽供養時把供品直接放進缽裡，或放在僧侶遞出的黃布上，**在街上與大眾運輸上也要一樣注意**。對僧侶說話要客氣。
- 王室（三句）：泰國觀光局寫泰國人對王室抱著很深的敬意，跟泰國人聊到王室要注意不要傷到對方感情；每天早上 8 點與傍晚 6 點，車站等公共場所會播國歌，多數人會停下手邊的事起立聽完；電影院放映前會播國王讚歌與王室影片，**包含外國人在內全體起立**。
- 頭與腳（兩句）：泰國人把頭視為「精靈棲息的地方」，摸別人的頭非常失禮；**但泰國觀光局同一段寫明，摸小孩子的頭疼愛一下沒有問題**，不要寫成「絕對不能碰任何人的頭」。
- **不寫**：泰國的王室相關刑責、條號與案例，本篇沒有可讀的官方法規頁，一個字都不寫（見「撰稿時要小心」第 9 條）。

(6) H2-4「六座最常去的寺廟：門票、時間與官方寫明的規定」（約 700 字）
- 先放表格，4 欄「寺廟／外國人門票（2026 年 9 月）／開放時間／官方寫明的規定與備註」，六列：
  - 大皇宮與玉佛寺（曼谷）｜500 泰銖，含玉佛寺與詩麗吉王后紡織博物館｜每天 08:30 到 16:30，售票只到 15:30｜十一條服裝禁止清單；身高 120 公分以下兒童免費；玉佛寺大殿內不能拍照；有王室典禮或公務的日子停止開放
  - 臥佛寺（曼谷）｜300 泰銖｜每天 08:00 到 19:30｜請穿著端莊、不要穿短褲，女性不可穿膝上短褲；進殿前脫鞋放鞋架；120 公分以下兒童免費
  - 鄭王廟（曼谷）｜200 泰銖｜08:00 到 18:00｜沒有可讀的官方網站，票價與時間出自泰國觀光局；服裝照泰國通則
  - 白廟 Wat Rong Khun（清萊）｜200 泰銖｜08:00 到 17:00｜離清萊市區約 14 公里；服裝照泰國通則
  - 素帖山雙龍寺（清邁）｜30 泰銖，纜車另收一人 50 泰銖｜05:00 到 21:00，纜車約 06:00 到 18:00｜從清邁市中心開車約 40 分；服裝照泰國通則
  - 查龍寺（普吉）｜免費參拜，歡迎隨喜｜08:00 到 17:00｜官網寫肩膀、胸口與膝蓋都必須遮住；寺廟建築內絕對不可穿鞋
- 表後四段（審查時把臥佛寺與查龍寺拆成兩段，因為取的是不同一邊、理由不一樣；**正文的份量不變，兩座各一句話交代差異，理由不必寫進正文**）：
  - 大皇宮的實務三句：2024 年 1 月 10 日起遊客改從 Mani Noppharat 門進場（王室辦公室公告）；官網可以先線上買票，最多提早一個月，**線上票不能退、不能改期**；租語音導覽 200 泰銖、八種語言（含中文），要押護照或信用卡。**當天開不開看官網的 schedules 頁**，2026 年 9 月 20 日那一頁三個欄位都寫 Open all day。
  - 兩個官方頁對臥佛寺打架的那件事：臥佛寺自己的官網寫 08:00 到 19:30，泰國觀光局寫 08:30 到 20:00、最後入場 19:30。**正文採寺方官網的 08:00 到 19:30，並用一句話揭露兩邊不一致、以現場告示為準**，不要兩個數字並陳當成「彈性時間」。理由照本批 README 的通則「數字預設以營運者為準」：`watpho.com` 就是臥佛寺自己的網站（頁尾「Copyright : 2018 watpho.com」、聯絡信箱 `watpho.th@gmail.com`）、維護正常，同一組數字也和既有 `bangkok-4-day-itinerary` 一致。
  - 查龍寺是同一條規則跑出不同結果，**不是另一套原則**：`wat-chalong-phuket.com` 的 FAQ 兩處都寫 07:00 到 17:00（「open daily from 7:00 a.m. to 5:00 p.m.」與「Early morning (7:00 a.m. - 9:00 a.m.) is best」），泰國觀光局寫 08:00 到 17:00。那個站是泰國觀光局頁面列出的該寺網址，但同時在賣普吉觀光行程，**是委外經營的宣傳站**，所以照本批 README 的通則把時間與票價換成政府觀光機構的；08:00 到 17:00 也正好是兩組裡較窄的時段，當規劃基準不會提早到現場吃閉門羹。**表格與 summary 採 08:00 到 17:00**，正文一句話揭露寺方網站寫的是 07:00，並寫「以現場告示為準」。這一組和本批第 12 篇 `phuket-old-town-big-buddha-viewpoints` 的「08:00 到 17:00」一字不差。**不要把理由寫成「那個站不算官方」**——服裝與鞋子那兩條還是引它。
  - 一句 article inline 各連一篇，三句分開寫、不要連成一串：白廟與藍廟怎麼排 → `chiang-rai-2-day-itinerary`（howto，既有）；素帖山雙龍寺怎麼上山 → `chiang-mai-3-day-itinerary`（howto，既有）；普吉老城、普吉大佛與查龍寺怎麼走 → `phuket-old-town-big-buddha-viewpoints`（howto，本批第 12 篇）。**「大佛」一律寫全稱**（協調者 2026-09-20 裁決）：普吉那一座寫「普吉大佛」，芭達雅那一座寫「芭達雅大佛寺（Wat Phra Yai）」，本篇任何地方都不單寫「大佛」。
- 放一個 tip callout：**遺址與王室園區比寺廟嚴。** 大城的遺址與 Bang Pa-In 夏宮另有一套更嚴的服裝規定（連露腳跟的鞋都不行，穿錯要換上宮方準備的罩衫或筒裙），門票也不是本篇這一套，那些數字全部在大城那篇（callout 內文用純文字寫，`article` inline 放在 callout 之後的段落裡，callout 不能放 inline）。緊接著一句 article inline → `ayutthaya-day-trip-from-bangkok`（howto，既有）。

(7) H2-5「一次完整的參拜：四點組、五個步驟，和離開前的三件事」（約 380 字）
- 四點組：泰國觀光局寫供養用的「花、線香、蠟燭、金箔」四點組，常在寺廟入口附近販售，**價格常見約 20 泰銖**（原文寫的是「多在 20 泰銖左右販售」，不是官方定價，正文要照這個語氣寫）。
- 五個步驟寫成 `list`，一項一行，照泰國觀光局的原文順序，**不要加自己的動作**：
  1. 在入口附近請一份花、線香、蠟燭、金箔的四點組。
  2. 在指定的地方點燃蠟燭與線香，蠟燭立到燭台上，線香拿在手上進到下一步。
  3. 雙手拿著花與線香，在臉或胸前合掌（手肘輕靠身體、指尖對齊），祈願後把花與線香放到各自的位置。
  4. 進大殿行最慎重的那種禮拜：跪坐（男性腳跟立起、女性一般跪坐），胸前合掌，略低頭把合掌的手抬到額前，再張開手肘與手掌貼地、額頭觸地，**這個動作做三次**，最後在額前合掌結束。
  5. 把金箔貼到大殿的佛像或專供貼金箔的佛像上；有出生星期守護佛的寺廟，貼在自己那一尊也很常見。
  後面接一句：各寺作法不同，看周圍的人怎麼做最準（泰國觀光局原文就這麼寫）。
- 離開前三件事：全泰國的寺廟都禁菸，違反會罰款（泰國觀光局原文）；不要碰壁畫、彩繪玻璃與塑像；寺內牽手勾肩、大聲笑、奔跑、跳躍、跳舞都不合適（這一條原文是「不好」，寫成建議句）。
- 行前檢查 `list`（5 到 6 項）：有袖上衣加長褲或過膝裙、好脫的鞋、包包裡一條薄圍巾、小額現金（四點組與隨喜都收現金）、當天先看大皇宮官網的 schedules 頁、遇到國歌就停下來站好。
- 結尾兩句 article inline（兩句分開、連結文字不一樣）：清邁白天逛完寺廟、晚上的夜市看星期幾 → `chiang-mai-night-markets-walking-streets`（howto，本批第 11 篇）；從曼谷去芭達雅與格蘭島那天怎麼安排 → `pattaya-koh-larn-day-trip-from-bangkok`（howto，本批第 13 篇）。**Koh Larn 一律寫「格蘭島」**（協調者 2026-09-20 裁決，與第 13 篇同一套；「可蘭島」「閣蘭島」只放第 13 篇的 `aliases`，本篇不用）。
- **結尾的 `link` 區塊放在 faq 區塊之後、全篇最後**（順序：H2-5 的結尾兩句 article inline → `faq` → 兩個 `link`），**兩個，都是城市頁**：
  1. `https://mokaair.com/zh-TW/destinations/bangkok`，文字寫通用說法，例如「曼谷城市頁：大皇宮、臥佛寺、鄭王廟一帶怎麼安排」。
  2. `https://mokaair.com/zh-TW/destinations/chiang-mai`，例如「清邁城市頁：古城寺廟與素帖山雙龍寺怎麼排」。
  **美食目錄的 `link` 一個都不放**（需要 `destination_id`，本篇是 null）。上限兩個，不要為了清萊、普吉再加。依據見「切角與段落」開頭那段的協調者 2026-09-20 全批裁決。

(8) faq 區塊（3 題，答案純文字、內容都要在正文出現，約 230 字）：
1. 「穿短褲真的會被擋在門口嗎」→ 會。大皇宮官網的十一條裡短褲、熱褲、迷你裙、褲裙都在內，臥佛寺官網寫女性不可穿膝蓋以上的短褲，查龍寺官網寫肩膀、胸口與膝蓋都要遮住。泰國觀光局只寫「有些地方」可以付費租腰巾，不是每一座都有，直接穿對最省事。
2. 「寺廟裡可以拍照嗎」→ 多數寺廟可以：臥佛寺官網寫可以拍，但絕對不能踩上佛像；查龍寺官網寫照片與錄影都允許。大皇宮與玉佛寺依王室辦公室 2567 年的法規，准許拍攝的範圍是玉佛寺周邊、不含大殿內部，也禁止婚紗照、照明器材與無人機。
3. 「女生要注意什麼」→ 不可碰觸僧侶的身體、僧衣與隨身物，在街上與大眾運輸上也一樣；臥佛寺官網另寫女性不可進入保留給僧侶做法事的區域。托缽供養時把東西放進缽裡，或放在僧侶遞出的黃布上。

`related`（最多 4）：`bangkok-4-day-itinerary`、`ayutthaya-day-trip-from-bangkok`、`chiang-rai-2-day-itinerary`、`chiang-mai-3-day-itinerary`。
**為什麼 `related` 沒有同批那三篇**（本批第 11、12、13 篇的 `related` 都列了本篇，這裡是刻意的不對稱，第七批 README 的對稱規則要有說明才算過）：四個名額給的是 H2-4 那張表裡六座寺廟所在城市的行程篇（曼谷、大城、清萊、清邁），讀者從本篇往下一步最需要的是那四篇；同批第 11、12、13 篇本篇都已經在正文用 `article` inline 連了（第 12 篇在 H2-4、第 11 與第 13 篇在結尾），比 `related` 的位置更顯眼，不必再占名額。**這個安排若協調者要改成對稱，就把 `ayutthaya-day-trip-from-bangkok` 與 `chiang-rai-2-day-itinerary` 換掉——但那兩篇各有一座本篇表上的寺廟（大城遺址、白廟），換掉會讓讀者找不到出處，所以本規格建議維持現狀。**
`aliases`：`{"zh-TW": ["泰國寺廟服裝", "大皇宮服裝規定", "玉佛寺", "拜拜禮儀"]}`。「玉佛寺」放別名而不寫進 slug，是因為正文本來就會寫到它；**別名不要放「白龍寺」**，那是 `chiang-rai-2-day-itinerary` 的別名。

照片：hero 用 Commons 的橫幅實景照，要找的是泰國寺廟的入口或殿前實景（山門、告示牌、殿前的鞋架都可以），**畫面裡不要有可辨識的人臉**，授權與挑法照 README；同一張照片不能當兩篇的 hero，和本批第 11、12、13 篇的撰稿人先對一下用哪張。
內文照片 1 到 2 張：(a) 寺廟入口的服裝規定告示牌（泰國寺廟常見的圖示看板），放在 H2-1 的 list 之後；(b) 殿前的鞋架或成排脫下的鞋子，放在 H2-2 脫鞋那一段之後。找不到告示牌的照片就改找寺廟大殿門口的全景。

## 官方來源

已確認讀得到（2026-09-20 規格撰寫時重讀；curl 一律帶 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一個站每個請求間隔 1 秒以上）：

(1) 泰國王室辦公室 大皇宮官網 Practical Information https://www.royalgrandpalace.th/en/visit/practical-information （curl 200）：
  「For Foreigners　500 baht for Foreigners. Inclusive of access to Wat Phra Kaew and Queen Sirikit Museum of Textile, which are located within The Grand Palace compound.」
  「Dress Code　Visitors to The Grand Palace must dress appropriately because The Grand Palace is a place of reverence for the Thai people. Inappropriate clothes for entry into The Grand Palace are as follows:」後接 **十一條**：「No sleeveless shirts / No vests / No short top / No see through tops / No short hot pants or short pants / No torn pants / No tight pants / No bike pants / No mini skirts / No pants skirts / **No sleeping suit**」。
  **研究檔只記到十條，漏了 `No pants skirts`（褲裙）。** 既有 `bangkok-4-day-itinerary` 也只寫十項、漏掉褲裙（見「上線後與交叉檢查」）。
  「No Drone Zone　Drone is not allowed flying over the area of the Grand Palace」。
  頁尾固定區塊：「Opening Hours　Daily 8:30 AM - 4:30 PM」「Price　Tickets sold from 8:30 AM - 3:30 PM and cost 500 baht」。
  交通：「BTS Saphan Taksin Station Exit 2 … Chao Phraya Express Boat, orange flag. Take the boat at Tha Chang (N9).」「MRT Sanam Chai Station Exit 1」（本篇不寫交通，數字留給既有文章）。
(2) 大皇宮官網 FAQ https://www.royalgrandpalace.th/en/visit/faq （curl 200）：
  「Children under 120 cm are free.」
  「The bureau of the royal household would like to announce the changing of the entrance to the grand palace and the emerald buddha temple from 10 january 2024 onwards the entrance to the grand palace will be changed from viset chaisri gate to mani noppharat gate」（連到 https://www.royaloffice.th/en/2024/01/05/ 的泰文公告）。
  「You can buy online ticket up to 1 month in advance before your visit date.」「All Online Tickets purchases cannot be refunded, nor can details be amended or changed for an alternate date or time.」
  「you can rent personal audio guide for other languages, 200 Baht. The audio guide available in 8 languages such as English, French, German, Japanese, Mandarin, Russian, Spanish and Thai. Passport or Credit Card (Amex, Master, Visa) is also required for rental」
  **同一頁的「What are the opening time」答案寫的是「The Grand Palace is open daily 8:30 AM - 3.30 PM」，和頁尾的 4:30 PM 不一致**（見「撰稿時要小心」第 1 條）。
(3) 大皇宮官網 Schedules https://www.royalgrandpalace.th/en/schedules （curl 200）：2026-09-20 當天三列（Temple of The Emerald Buddha／The Grand Palace／The Chapel of The Emerald Buddha）都是「Open all day」；頁上附註「Note: The date on the calendar might be change or added. Pleased, Call +66-2-623-5500 Ext. 2171」。這一頁就是「今天開不開」的官方查法。
(4) **王室辦公室 2567 年參觀與攝影法規（PDF，7 頁）** https://cdn.royalgrandpalace.th/images/visit/ระเบียบหน่วยราชการฯเข้าชมวัดวัง2567.pdf （curl 200，1,390,835 bytes；連結掛在 (1) 那一頁的「Regulations of the Bureau of the Royal Household Regarding Visits, Filming, Video Recording, and Photography within the Grand Palace B.E. 2024／Download the file」）。
  **是掃描檔，`pdftotext` 抽不出任何文字**（輸出 7 bytes），要用 `pymupdf` 把每頁轉成 PNG 再讀（`page.get_pixmap(dpi=140)`，規劃時的圖存在 `spec-raw/thailand-temple-etiquette-dress-code/reg-p1.png` 到 `reg-p7.png`）。標題：「ระเบียบส่วนราชการในพระองค์ ว่าด้วยการเข้าชมพระบรมมหาราชวัง และเขตพระราชฐานต่าง ๆ เกี่ยวกับการปฏิบัติในการถ่ายทำภาพยนตร์ วีดิทัศน์ และภาพนิ่ง พ.ศ. ๒๕๖๗」。
  - ข้อ ๖(๑)：「อนุญาตให้เข้าชมได้ทุกวันไม่เว้นวันหยุดราชการ ตั้งแต่เวลา ๐๘.๓๐ - ๑๖.๓๐ น. หยุดจำหน่ายบัตรตั้งแต่เวลา ๑๕.๓๐ น.」→ 每天開放不分國定假日，08:30 到 16:30，15:30 起停止售票。**這一條就是 (1)(2) 兩頁打架時的裁決依據。**
  - ข้อ ๖(๒)：有王室典禮或公務的日子，當天停止開放參觀。
  - ข้อ ๗(๒)：免費入場者包含「เด็กชาวต่างประเทศที่มีความสูงไม่เกิน ๑๒๐ เซนติเมตร」（身高不超過 120 公分的外國兒童）。
  - ข้อ ๗(๕)：服裝條。原文（逐字）：「ต้องแต่งกายสุภาพเรียบร้อย หรือแต่งกายตามประเพณีนิยมที่ถูกต้องของแต่ละชาติ ห้ามแต่งกายลักษณะที่ไม่เหมาะสม หมายความรวมถึง การห้ามสวมเสื้อแขนกุด เสื้อรัดรูป เสื้อเปิดหน้าท้อง เสื้อผ้าบางเห็นเรือนร่าง กระโปรงสั้น กางเกงยืดรัดรูป กางเกงขาสั้น กางเกงขาดตามแฟชั่น กางเกงขาบวม กางเกงขาสามส่วน หรือหากเป็นชุดโจงกระเบนสำเร็จรูปต้องมีความยาวใต้เข่าพอสมควร หากเป็นชุดห่มสไบเฉียงต้องสวมเสื้อแขนยาวด้านใน」
  - ข้อ ๑๐(๒)：「ห้ามสัมผัส หยิบจับหรือขีดเขียน สิ่งประดับอาคารสถานที่ เช่น จิตรกรรมฝาผนัง กระจกสี และรูปปั้นต่าง ๆ」；(๓) 禁雷射筆與指示棒；(๕) 禁政治性宣誓、符號與活動；(๖) 禁武器與仿製武器；(๗) 禁寵物。
  - ข้อ ๑๑(๑)：一般遊客可用一般相機拍觀光用途的照片，不得用照明器材（ไฟแสงสว่าง）、吊臂（เครน）、滑軌（อุปกรณ์ล้อเลื่อน）、相機用無線麥克風、裝相機的無人機（อากาศยานไร้คนขับติดกล้อง）。
  - ข้อ ๑๑(๓)：「ห้ามไม่ให้มีการบันทึกภาพเพื่อวัตถุประสงค์ที่นอกเหนือไปจากการท่องเที่ยว เช่น การบันทึกภาพก่อนสมรส (pre-wedding)」→ 禁止觀光以外目的的拍攝，舉例就是婚紗照。
  - ข้อ ๑๒(๑)：允許拍攝的地點是「บริเวณวัดพระศรีรัตนศาสดารามโดยรอบ **ยกเว้นภายในพระอุโบสถ**」→ 玉佛寺周邊可以，**大殿（พระอุโบสถ）內不可以**。
  - ข้อ ๑๓ 之後是商業拍攝的申請程序（提前 60 天、正本一份副本十三份等），**與一般遊客無關，一個字都不要寫進正文**。
(5) 臥佛寺官網 Visit plan https://www.watpho.com/en/contact/plan （curl 200）：
  「Operating hour: 08:00 – 19:30」「Admission fee: 300 Baht」「Free entry for children under the height of 120 cm.(4 feet)」「Tourists are appreciated to dress politely, no shorts, although trousers are permitted.」
  Tips for Visitors 四段（逐字）：
  「Once entering the precincts of any temple please keep calm and be polite since the temple is a sacred place where religious rites and activities are performed.」
  「Traditional or polite dress is required, while shorts above the knees are prohibited for woman. It is required to take off your shoes and put them on the shelf before entering religious buildings. Women are also prohibited from all areas set aside for monks to perform their rites.」
  「The Buddha image is respected by all Buddhists. In temples and ancient monuments, photos can be taken, but never step on the image. Only permitted officer is allowed to climb up the image to clean and place the offerings.」
  「For monks, visitors are asked to be polite and gentle in both manners and words since monks are representatives for the Lord Buddha. Practically, monks and men can touch physically, but it is prohibited for women to have a physical contact with monks or novices.」
  按摩（本篇不寫，留給曼谷篇）：「Thai massage ; 30/60/120 mins. (340/520/1,040 Baht)」等四列。
(6) 臥佛寺官網 Trip to Wat Pho https://www.watpho.com/en/contact/trip （curl 200）：「MRT Blue Line: Exit 1 (Wat Pho Station)」、公車路線清單、「Parking is available on Chetuphon Road , with a service fee of 20 Baht per hour .」、「By Chao Phraya Express Boat: Get off at Tha Chang Pier or Wat Arun Pier , then take a cross-river ferry to Tha Tien Pier .」（交通不寫進本篇，列在這裡是因為官網把 MRT 站名寫成 Wat Pho Station，見「撰稿時要小心」第 8 條）。
(7) 泰國觀光局東京辦事處 寺院の参拝方法とマナー https://www.thailandtravel.or.jp/visiting-temples/ （curl 200）：
  服裝：「寺院を観光する際は、男女ともに ノースリーブやショートパンツ、破れたジーンズなど、肌の露出が多い服装は避けてください 。場所によっては腰巻などを有料で借りられる場合もありますが、不適切な服装では入場を断られることもございます。」
  寺內行為：「男女が手をつないだり肩を組んだりする行為 は好ましくありません。また、参拝中や撮影中に 大声で笑う、走り回る、飛び上がる、踊る といった行為も控えてください。」
  女性：「女性は僧侶の体や衣、持ち物に直接手を触れてはいけません 。托鉢の際などは、お供え物を直接鉢に入れるか、僧侶が差し出した黄色い布の上に置いてください。街中や公共交通機関においても、接触しないよう十分な配慮が必要です。」（**最後那句「街上與大眾運輸上也要注意」研究檔沒記到**）
  四點組：「お供え用の「花、線香、ろうそく、金箔」の4点セットを購入してください。 ポイント： 寺院の入り口付近で20バーツほどで販売されていることが多いです。」
  五步驟與禮拜動作（研究檔沒記到，本篇的 H2-5 全靠這一段）：「2. ろうそくと線香に火を灯します」「3. 「ワイ（合掌）」をしてお供えします…ひじを軽く身体につけ、顔や胸の前で指先を揃えて両手を合わせます」「4. 本堂で「ベンチャーンカプラディット」と呼ばれる、最も丁寧な礼拝を行います…正座をします。（男性はかかとを上げた正座、女性は通常の正座）…この動作を計3回繰り返した後、額で手を合わせて終わります」「5. 最後に金箔を本堂の仏像または金箔専用の仏像に貼ります…ご自身の誕生曜日の守護仏がある場合は、そちらに貼るのも一般的です」「※寺院によって作法が異なる場合がございます。周囲の方々の動きを参考にしてください。」
  腳底：「タイでは足の裏は「不浄」とされています。参拝の際は、 仏前に足の裏を向けない よう、座り方に注意を払ってください。」
  禁菸：「なお、すべての寺院は禁煙であり、違反した場合は罰金が科せられます。」
(8) 泰國觀光局東京辦事處 エチケット https://www.thailandtravel.or.jp/about/etiquette/ （curl 200）：
  「毎朝8時と夕方6時になると駅などの公共の場で国歌が流れますが、多くの人々は仕事の手を止めて起立し、聞き入ります。」
  「映画館では上映前に国王賛歌と王室の映像が流れますので、外国人も含めて全員が起立することになっています。」
  「タイの人々は王室に対してとても深い尊敬の念を抱いています。タイの人々と王室について話題にするときは相手の感情を害さないように注意しましょう。」
  「タイでは人の頭は「精霊が宿る場所」として神聖視されています。そのため、他人の頭を触ることは大変失礼にあたるので気をつけましょう。**小さな子どもの頭をなでてかわいがるのは問題ありません。**」（粗體那句研究檔沒記到）
  「左手と同様に足の裏も「不浄」とされています。」「他人の足をまたぐのも失礼な行為とされています。公共の乗り物や劇場などではどうしても通らなければならないこともありますが、必ず一声かけて足をずらしてもらいましょう。」
  「ツーリスト・ポリス （英）TEL:（局番なし）1155/ 02-535-1641（日本語・英語可）」（本篇只在行前檢查或 FAQ 需要時寫 1155，不展開治安內容）。
(9) 泰國觀光局東京辦事處 ワット・アルン（暁の寺）https://www.thailandtravel.or.jp/wat-arun/ （curl 200）：営業時間「08:00～18:00」、料金「200バーツ」、住所「34 Arunamarin Rd., Wat Arun, BangkokYai, Bangkok 10600」、電話「02-891-2185 (Wat Arun Central Office)」。**鄭王廟票價的唯一官方出處。**
(10) 泰國觀光局東京辦事處 ワット・ポー https://www.thailandtravel.or.jp/wat-pho/ （curl 200）：営業時間「08:30～20:00（最終入場19:30）」、料金「300バーツ」。**與寺方官網的 08:00–19:30 不一致**，正文採寺方官網。同一頁另寫「毎週土曜日の朝8時から約30分間、タイ式健康法 ルーシーダットン の無料体験も可能です。(ワット・ポーの参拝料300バーツがかかります)」（本篇不寫，留給曼谷篇）。
(11) 泰國觀光局東京辦事處 ワット・ロンクン（ホワイト・テンプル）https://www.thailandtravel.or.jp/white-temple/ （curl 200）：営業時間「08:00～17:00」、料金「200バーツ」、アクセス「チェンライ市内から約14km」、電話「053-673-579」。與既有 `chiang-rai-2-day-itinerary` 一致。
(12) 泰國觀光局東京辦事處 ワット・プラタート・ドイ・ステープ https://www.thailandtravel.or.jp/wat-phra-that-doi-suthep/ （curl 200）：営業時間「05:00～21:00 (有料ケーブルカーは06:00～18:00頃まで運行）」、料金「30バーツ (ケーブルカーは一人50バーツ）」、アクセス「チェンマイ中心部から車で約40分」。與既有 `chiang-mai-3-day-itinerary` 一致。
(13) 泰國觀光局東京辦事處 ワット・チャイタララーム（ワット・チャロン）https://www.thailandtravel.or.jp/wat-chalong/ （curl 200）：営業時間「08:00～17:00」、料金「参拝自由」，URL 欄列的官方網站是 https://www.wat-chalong-phuket.com/index.html 。
(14) 查龍寺官網 FAQ https://www.wat-chalong-phuket.com/faq.html （curl 200；即 (13) 的 TAT 頁所列的官方網站）：
  「Q: Dress Code for Wat Chalong　A: Modest dress is required. Shoulders, chests, and knees must be covered. Avoid sleeveless tops, short skirts, or midriffs.」
  「Q: Wearing Shoes　A: Shoes are never allowed inside a temple buildings.」
  「Q: Entry fee for Wat Chalong　A: Although there is no charge to enter the temple, donations and offerings are welcome.」
  「Q: Talking and Respect at Wat Chalong　A: Certain level of respect is expected, Speak in a quiet tone within the temple and don't touch the statues or other Buddhist relics.」
  「Q: Is photography allowed?　A: Yes, photography is allowed」「Q: Is Video allowed?　A: Yes, Video is allowed」
  「Q: What are the opening hours for Wat Chalong　A: The Phuket Wat Chalong Temple is accessible all year round because it is open daily from 7:00 a.m. to 5:00 p.m.」
  「Q: When is the best time to visit?　A: Early morning (7:00 a.m. - 9:00 a.m.) is best to avoid crowds, intense heat, and to see monks performing morning rituals.」
  → **這一頁兩處都寫 07:00，與 (13) 的 08:00 不一致**（2026-09-20 審查覆核，兩句都在可見內容裡、不在 HTML 註解內）。取捨與理由見「撰稿時要小心」第 (11) 條。同時要知道：本批第 12 篇只讀了 `index.html`（該頁確實沒有開放時間），**FAQ 這一頁有**，兩篇的來源敘述不能互相打架。
(15) 既有文章 `apps/api/app/guides/content/bangkok-4-day-itinerary.json`（blocks 5、18）：大皇宮 500 泰銖、08:30 到 16:30、售票到 15:30、120 公分以下免費、2024-01-10 改 Mani Noppharat 門；臥佛寺 300 泰銖、08:00 到 19:30、女性不可穿膝上短褲、進殿脫鞋；鄭王廟「以官網為準」。本篇除了鄭王廟那一格之外與它完全一致（差異見「上線後與交叉檢查」）。

**讀不到或不可用的頁（撰稿時再試一次，仍讀不到就照本規格寫）：**
- **`watrongkhun.org`（白廟舊官網）今天不是白廟的網站，`sources` 與正文一個字都不能出現這個網域。** 2026-09-20 規格撰寫時與同日審查覆核各驗一次，結果相同：`https://watrongkhun.org/en/` 回 `308 Permanent Redirect`（Cloudflare）到 `https://www.watrongkhun.org/en/`，最終 200、57 KB，但 `<title>` 是 **Padaeng Industry**（鋅業公司），可見導覽列第一排就掛著 `คาสิโนออนไลน์`（線上賭場）、`แทงบอลออนไลน์`（足球投注）、`โป๊กเกอร์ออนไลน์`（線上撲克）三個連結，全頁 **"Rong Khun" 與 "White Temple" 零命中**；裸網域 `http://www.watrongkhun.org/` 301 到 `https://www.watrongkhun.org/`（規格撰寫時那次導到 `https://rw24s.com/` 回 403）。第七批 README 把它列在「讀不到」，現在的狀況更糟：**它會回 200，很容易被當成讀到了。** 白廟的票價與時間只能引泰國觀光局（第 (11) 條）。**這個網域不得進入本篇的 `sources`、不得出現在正文或圖說、也不要在 `notes.md` 以外的地方留可點的連結。**
- 鄭王廟沒有可讀的官方網站：`www.watarun1.com` DNS 解析不到，`watarun.net` 與 `www.watarun.net` 連線逾時。票價與時間只能引泰國觀光局（第 (9) 條），正文要寫明出處是泰國觀光局。
- `www.doisuthep.com` 是 “This domain is coming soon.” 的停放頁（curl 200，1,397 bytes），不是素帖山雙龍寺的官網，不可引用。
- 普吉大佛 `https://www.mingmongkolphuket.com/Index` curl 200、323 KB，但正文全靠 JavaScript 產生，抽出來的純文字只有 8 個字元，**沒有任何可引用的內容**。普吉大佛的規定本篇不寫，留給本批第 12 篇；本篇在普吉這一格只寫查龍寺。
- 佛像出境許可（泰國藝術廳 `finearts.go.th`）：研究檔已標「查不到對應說明頁」，本規格維持**不寫**，連「買佛像前先問店家」這種暗示性的句子也不要放（沒有官方依據，且與本篇切角無關）。
- 泰國政府觀光局本站 `tourismthailand.org`（含 `thai.` 子網域）整站在這台機器讀不到，第六、七批 README 已記錄；泰國觀光局的內容一律引東京辦事處那個網域。

## 圖解

`diagram-1.svg`，1600×900，放在 H2-2 那段文字之後、H2-3 標題之前。`role="img"`、`<title>`、`<desc>`、所有 `font-size` ≥15、不外連、右下角「© Mokaair 製圖 2026」。配色與字型串照 `docs/life-ai-series-brief.md` 第 6 節，**泰國主題加 'Noto Sans Thai'**。
一張圖只講一件事：**從出門前到走出寺門，七個關卡各要做什麼**。畫成由左到右（或上下兩排）的七格流程，每格一個標題加一到兩行小字：

1. 出門前｜有袖上衣、長褲或過膝裙、好脫的鞋
2. 門口｜大皇宮列了 11 條不能穿的衣服；腰布不一定租得到
3. 買票｜外國人付費；身高 120 公分以下免費
4. 脫鞋｜進殿一律脫鞋，放到鞋架上
5. 請四點組｜花、線香、蠟燭、金箔，常見約 20 泰銖
6. 大殿｜跪坐、腳底不朝佛像；最慎重的禮拜叩 3 次
7. 離開前｜不碰壁畫與塑像、不踩上佛像、全寺禁菸

右側（或下方）另開一個小欄「兩件隨時適用的事」：女性不碰觸僧侶的身體、僧衣與隨身物；每天 08:00 與 18:00 國歌響起就站好。
第 6 格旁邊加一個小標籤：「玉佛寺大殿內不能拍照」。
**圖上只有這幾個數字，全部要在正文出現：11、120、20、3、08:00、18:00。** 不畫票價、不畫各寺開放時間、不畫電話號碼——票價與時間留在表格裡。
泰文只用官方頁上出現過的：พระอุโบสถ（玉佛寺大殿那個標籤可以加註，也可以不加）。除此之外不要在圖上放泰文。

## 撰稿時要小心

(1) **大皇宮的開放時間官網自己打架，而且「15:30 那一組」出現三次，不只在 FAQ。** 2026-09-20 覆核：Practical Information 頁的頁尾固定區塊寫「Opening Hours　Daily 8:30 AM - 4:30 PM」與「Price　Tickets sold from 8:30 AM - 3:30 PM」，**但同一頁中段的 Annoucement 區塊寫「The Grand Palace is open daily from 8:30 AM - 3:30 PM」**，FAQ 的「What are the opening time…」也寫「8:30 AM - 3.30 PM」。以王室辦公室 2567 年法規 ข้อ ๖(๑) 為準：**08:30 到 16:30，15:30 停止售票**，和既有 `bangkok-4-day-itinerary` 一致。不要把 15:30 寫成閉館時間，也不要兩個並陳；撰稿時看到 Annoucement 區塊那一句不要以為讀錯頁。
(2) **服裝清單是十一條，不是十條。** 研究檔與既有曼谷篇都漏了「褲裙（No pants skirts）」。十一條一條都不能少，順序照官網。
(3) **不要自己翻譯泰文法規裡沒有把握的詞。** ข้อ ๗(๕) 裡的 `กางเกงขาบวม` 沒有通行的中文對應（字面是「褲管鼓起來的褲子」），**正文不要寫這一項**，也不要寫成「泰式燈籠褲」「大象褲」之類的猜測。可以寫的只有兩項：`กางเกงขาสามส่วน`（七分褲）與 `ชุดห่มสไบเฉียง`（披肩式服裝要內搭長袖）。整段法規不要逐條翻譯。
(4) **「有些地方可以租腰布」不等於「門口都租得到」。** 泰國觀光局原文是「場所によっては」，而且同一句接著寫穿不合適也可能被拒絕入場。大皇宮官網完全沒有提到租借服務。不要寫成「到了現場再租一條就好」。
(5) **拍照要分兩套寫。** 一般寺廟可以拍（臥佛寺與查龍寺官網都明文允許），**唯一不能做的是踩上佛像**；大皇宮與玉佛寺依王室辦公室法規，准許的範圍是玉佛寺周邊、不含大殿內部，另禁婚紗照、照明器材、吊臂、滑軌、相機用無線麥克風與無人機。**不要把「玉佛寺大殿內不能拍」寫成「泰國寺廟都不能拍照」，也不要反過來寫成「哪裡都能拍」。**
(6) **法規 ข้อ ๑๑(๑) 那句關於社群直播的敘述泰文本身就有歧義**（「…ที่ไม่ใช่เพื่อการโฆษณาหรือการพาณิชย์ รวมถึงทางการเมือง การถ่ายทอดสดด้วยการสื่อสารทาง Social Media…」可以讀成「直播也不准」，也可以讀成「直播屬於一般拍攝」）。**本篇不寫直播能不能做**，只寫確定的三件事：一般相機的觀光照可以、商業與政治用途不可以、照明器材／吊臂／滑軌／相機無線麥克風／無人機不可以。
(7) **不要把商業拍攝的申請程序寫進正文。** 法規 ข้อ ๑๓ 以後的 60 天、正本一份副本十三份、ข้อ ๒๔ 的著作權歸屬，都是給申請拍攝許可的人看的，和一般遊客無關。
(8) **臥佛寺官網把 MRT 站寫成「Wat Pho Station」，實際站名是 Sanam Chai（สนามไชย）。** 本篇不寫交通，但如果要提一句，站名照大皇宮官網與既有曼谷篇寫「MRT Sanam Chai 站」。
(9) **王室的部分只寫泰國觀光局寫過的三句**（談論時注意、國歌時起立、電影院全體起立）。**不要寫刑法條號、刑度、案例或「外國人也會被判刑」這類話**——這台機器上沒有可讀的官方法規頁，第六批 ERRATA 已經有「WebFetch 摘要自己加料」的前例。
(10) **「摸小孩的頭沒問題」這句要寫。** 泰國觀光局在同一段明文寫了，漏掉就會變成「泰國人的頭一律不能碰」的過度規則。
(11) **臥佛寺與查龍寺的開放時間各有兩個官方說法，取的是不同一邊，但走的是同一條規則**（臥佛寺：寺方 08:00–19:30／觀光局 08:30–20:00 最後入場 19:30；查龍寺：寺方網站 07:00–17:00／觀光局 08:00–17:00）。**表格各取一個、正文一句話揭露另一個，並寫「以現場告示為準」**，不要在表格裡塞兩組數字。
  規則照本批 README（協調者 2026-09-20 裁決）：**數字預設以營運者為準；營運者的站疏於維護、自相矛盾或只是委外經營的宣傳站時，時間與票價改採政府觀光機構，並在正文用一句話揭露另一邊的說法；開放時間有疑義時以較窄的時段當規劃基準。**
  - 臥佛寺 → 取寺方的 08:00–19:30：`watpho.com` 就是該寺自己的網站、維護正常，而且和既有 `bangkok-4-day-itinerary` 一致。
  - 查龍寺 → 取觀光局的 08:00–17:00：`wat-chalong-phuket.com` 是觀光局列出的網址但同時在賣普吉行程，屬於「委外經營的宣傳站」（見第 (12) 條），所以換成政府觀光機構；08:00–17:00 也是較窄的那一組，符合規劃基準那一句，並與本批第 12 篇一致。
  **正文不要寫成「一律以寺方為準」或「一律以觀光局為準」，也不要寫成「這兩座用了不同標準」**——寫成上面那一條規則的兩個結果。2026-09-20 覆核時查龍寺 FAQ 的 07:00 出現兩次（開放時間那一問，與「最佳時段 07:00–09:00」那一問），不是單一筆誤。
(12) **查龍寺官網（`wat-chalong-phuket.com`）要交代它的身分。** 它是泰國觀光局頁面列出的該寺 URL，但站上同時在賣普吉市區觀光行程，形式上像委外經營。正文引它的服裝與鞋子規定沒問題（那是該寺的官方網站），**但不要把它寫成「寺方公告」**，寫「查龍寺官方網站」就好；撰稿當天若該站的 FAQ 內容變了，就改寫成「以現場告示為準」。
(13) **白廟的官網今天是別家公司的網站。** 見「官方來源」的讀不到清單。**看到 `watrongkhun.org` 回 200 不要當成讀到了**，打開內容確認是不是白廟。白廟只引泰國觀光局的 200 泰銖與 08:00–17:00，和既有清萊篇一字不差。
(14) **鄭王廟 200 泰銖要寫明出處。** 既有 `bangkok-4-day-itinerary` 寫的是「以官網為準」，因為鄭王廟沒有可讀的官網。本篇寫 200 泰銖，出處是泰國觀光局東京辦事處的景點頁，正文要把這件事寫出來（「鄭王廟沒有可讀的官方網站，票價與時間依泰國觀光局」），不要寫成「官網寫 200 泰銖」。
(15) **素帖山雙龍寺與白廟的數字，和既有文章必須一字不差**：素帖山雙龍寺 30 泰銖、纜車一人 50 泰銖、05:00 到 21:00、纜車約 06:00 到 18:00（`chiang-mai-3-day-itinerary`）；白廟 200 泰銖、08:00 到 17:00、離市區約 14 公里（`chiang-rai-2-day-itinerary`）。改一邊就要同一個 PR 改另一邊。
(16) **地名照目的地目錄**：`catalog.py` 與 `areas.py` 用的是「大皇宮」「臥佛寺」「鄭王廟」「素帖山雙龍寺」「查龍寺」。白廟目錄裡沒有，照既有清萊篇寫「白廟（Wat Rong Khun）」。「玉佛寺」指的是曼谷大皇宮園區內那座；**清萊另有一座同名的玉佛寺（Wat Phra Kaew）**，泰國觀光局東京辦事處的 `wat-phra-kaew` 那一頁講的是清萊那座，不要抓錯頁。
(17) **不寫行程、不寫交通、不寫按摩、不寫周邊。** 大皇宮怎麼排一天、臥佛寺按摩多少錢、素帖山怎麼上山、白廟怎麼去，全部連既有文章。本篇只有一個例外：門票與開放時間放在表格裡，因為它們是「會不會白跑」的判斷依據。
(18) **這一批的三篇不重複**：本批第 11 篇（清邁夜市）、第 12 篇（普吉老城與普吉大佛）、第 13 篇（芭達雅與格蘭島）各只寫一句服裝提醒並連過來，**所以那三篇不會再出現任何服裝條列或寺廟門票表**；本篇也不寫那三篇的景點細節。
(19) **不放 offer，但要放兩個城市頁 `link`。** `etiquette` 主題照第六、七批原則不放分潤區塊，一個都不放。`destination_id` 是 null **不等於不能放城市頁 link**：照協調者 2026-09-20 的全批裁決，結尾放 `destinations/bangkok` 與 `destinations/chiang-mai` 兩個 `link`（上限兩個），**美食目錄的 `link` 因為需要 id 才一個都不放**。不要把「null 文章」直接寫成「不放任何 link 區塊」。
(20) **禁菸那一句要寫完整**：「所有寺廟都禁菸，違反會罰款」是泰國觀光局的原文，可以寫成規定句；但**罰款金額沒有官方數字，不要寫金額**。
(21) **summary、表格、list、FAQ 與圖上的數字要一致**：500、300、200、30、50、20、11、120、3、08:30、16:30、15:30、08:00、19:30、18:00、17:00、05:00、21:00、06:00、08:00 與 18:00（國歌）、1155。改一處要全改。
  **另外三個「另一邊」的數字只在正文各出現一次，不進 summary、表格、圖解或 FAQ**：臥佛寺的觀光局版 08:30 到 20:00（最後入場 19:30）、查龍寺的寺方版 07:00、大皇宮官網自己那組 15:30 閉館。這三個出現第二次就是寫錯了。

## 上線後與交叉檢查

- **本批互連（2026-09-20 審查把三篇的實際寫法都打開對過，原本寫「四篇一字不差」並不成立，改成下面這樣）**：本篇在 H2-4 連第 12 篇、在結尾連第 11 與第 13 篇；三篇都連本篇，雙向對稱。三篇各自的份量不一樣，**不要求四篇同一句話**：
  - 第 11 篇 `chiang-mai-night-markets-walking-streets` **一個服裝字都不寫**，只在週日步行街沿路寺院那一句連過來（它的規格明寫「本篇不重寫遮肩過膝、脫鞋、租沙龍那一套，一句都不寫」）。不要求它加那句共用句。
  - 第 12 篇 `phuket-old-town-big-buddha-viewpoints` 與第 13 篇 `pattaya-koh-larn-day-trip-from-bangkok` 各寫一句加連結。**那一句要一字不差，統一寫成「進殿要遮肩過膝、脫鞋」**（第 12 篇規格已經是這個寫法，第 13 篇只寫「連結文字講進泰國寺廟的服裝與規矩」，要補成同一句）。
  - 第 11、12、13 篇都不得再列服裝條列或寺廟門票表；本篇不寫那三篇的景點細節。任何一篇改那句共用句，同一個 PR 改另一篇。
- **反向連結（上線 PR 開成「既有文章補連第八批」的票）**，四筆：
  1. `bangkok-4-day-itinerary` `blocks[5]`（第一天舊城那一段，`paragraph`）→ 整塊改成 `rich_paragraph`，原文拆成 `text` inline，在「服裝規定嚴：…長褲加有袖上衣最省事」之後插一個 `article` inline 連本篇（連結文字「大皇宮的十一條禁止清單與進殿要注意什麼」）。**同一次編輯要把該段的服裝清單從十項補成十一項**：2026-09-20 審查逐項數過，現在寫的是「無袖上衣、背心、露肚上衣、透膚上衣、短褲、破洞褲、緊身褲、單車褲、迷你裙、睡衣式服裝」共十項，**要在「迷你裙」與「睡衣式服裝」之間補「褲裙」**（官網順序 No mini skirts → No pants skirts → No sleeping suit）。並順手把 `blocks[18]` 表格裡鄭王廟那一列的「以官網為準／以官網為準」改成「200 泰銖／08:00 到 18:00（泰國觀光局，2026 年 9 月）」——兩篇不能一篇寫 200、一篇寫「以官網為準」。
     同一篇 `blocks[15]` 由本批第 13 篇補反向連結，**與本篇的 `blocks[5]`、`blocks[18]` 不衝突**（2026-09-20 審查確認過）。另外 `blocks[19]` 寫「大皇宮加臥佛寺一個人就是 800 泰銖，兩個人 1,600 泰銖」是 500＋300 的加總，**日後任一張票調價，那兩個數字要同一個 PR 一起改**。
  2. `ayutthaya-day-trip-from-bangkok` `blocks[25]`（H2「服裝、天氣、回程末班」底下第一段，「遺址也是宗教場所：遮肩膝…穿短褲就帶條大圍巾。」那段 `paragraph`）→ 整塊改成 `rich_paragraph`，插 `article` inline 連本篇（連結文字「泰國寺廟的服裝與參拜規定」），文字與數字一個都不改。
     本篇 H2-4 的 tip callout 引的「Bang Pa-In 夏宮連露腳跟的鞋都不行、穿錯要換上宮方準備的罩衫或筒裙」出自同一篇的 `blocks[21]`（2026-09-20 審查逐字核對：「服裝比寺廟嚴：無袖、高於膝蓋的褲裙、緊身褲、露腳跟的鞋都不行，穿錯要換上宮方準備的罩衫或筒裙。」），**本篇只摘述、不改那一段**；`blocks[30]` 的 `list` 第 4 項也重複了露腳跟那一句，若日後要改夏宮的服裝規定，三處（`blocks[21]`、`blocks[30]`、本篇 callout）同一個 PR 改。
     同一篇 `blocks[28]` 由本批第 13 篇 `pattaya-koh-larn-day-trip-from-bangkok` 補反向連結，**與本篇的 `blocks[25]` 不衝突**（2026-09-20 審查確認過）。
  3. `chiang-mai-3-day-itinerary` `blocks[9]`（Day 1 古城那一段 `paragraph`，實際內容是兩段：第一段講三座寺廟與塔佩門、結尾是「短褲短裙的人可以在門口租沙龍圍上」，第二段講三個市集、最後一句是「從古城搭雙條車約 10 分鐘。」）→ 整塊改成 `rich_paragraph`（原文拆成 `text` inline）並插 inline。**同一次編輯把「可以在門口租沙龍圍上」改成照泰國觀光局原文的「有些寺廟可以付費租腰布，不是每一座都有」**——現在那句沒有官方依據，而且和本篇的 warning callout 互相矛盾。
     ⚠️ **這一塊本批有兩份規格都要改，必須合併成一次編輯**：本批第 11 篇 `chiang-mai-night-markets-walking-streets` 也要改 `blocks[9]`，在第二段最後一句「…從古城搭雙條車約 10 分鐘。」後面插一個連它的 `article` inline。合併後的 `rich_paragraph` 依序是：`text`（第一段到「…遮肩過膝、脫鞋進殿，」）＋`text`（改寫後的「有些寺廟可以付費租腰布，不是每一座都有。」）＋`article` inline 連**本篇**（連結文字「大皇宮的十一條禁止清單與進殿要注意什麼」）＋`text`（第二段原文到「…從古城搭雙條車約 10 分鐘。」，**一個字都不改**）＋`article` inline 連**第 11 篇**（連結文字「哪個市集星期幾開、白天的市場怎麼排」）。兩個 inline 一前一後、不相鄰放在同一句裡。**不要拆成兩次編輯，也不要兩篇各自改一次 `blocks[9]`。**
  4. `chiang-mai-old-city-slow-day` `blocks[16]`（最後一個 H2「把寺院、午餐與休息串成一個街區」底下第一段，「規劃示例可以從一座你感興趣的寺院開始…先查寺院的實際開放與參觀資訊，確認服裝、攝影及入內規定」那段 `paragraph`）→ 整塊改成 `rich_paragraph` 並插 inline。
     同一篇另有兩個第八批的反向連結，**三處不可以撞在同一個 block**：本批第 11 篇進 `blocks[10]`（「市集和街區活動不要當成每天都有」那段），本批第 10 篇 `chiang-mai-airport-transport-where-to-stay` 進 `blocks[8]`（「需要更少步行的人，可先確認住宿附近的單一目的地，並研究可靠的來回交通」那段）。本篇只動 `blocks[16]`。
  `chiang-rai-2-day-itinerary` 的服裝那一條在 `blocks[31]` 的 `list` 裡（第 2 項「寺廟服裝：遮肩過膝、脫鞋進殿，白廟與藍廟都一樣，免費參拜的藍廟也不例外。」，純字串），**`list` 的 items 放不了 inline**，要在那個 `list` 之後新增一個 `rich_paragraph`（一句話＋inline），不要去改 list。注意 `blocks[32]` 已經是一個 `rich_paragraph`（連泰國上網篇），新增的那一個要插在 `blocks[31]` 與 `blocks[32]` 之間，兩個 `rich_paragraph` 不要黏成一塊。
  **順手修（同一張票，與本篇無關但同一篇文章）**：`ayutthaya-day-trip-from-bangkok` `blocks[34]` 是一個只有 `article` inline 的 `rich_paragraph`，連的是 `thailand-entry-2026-tdac`（intel，`valid_until` 2026-12-31）。因為整塊只有那一個連結、沒有句子依賴它，**2027-01-01 之後整塊刪掉就好**，不必改寫別的句子；那篇的 `related` 是 `null`，不必動。
- **2027 年 1 月以前（上線 PR 同時開票並寫明日期）**：重讀大皇宮官網的 Practical Information 與 FAQ、王室辦公室 2567 年法規 PDF 的連結是否還在，確認 500 泰銖、08:30–16:30、15:30 停售、十一條清單與 120 公分免費都沒變；泰國的門票通常在年初調。
- **每次要用白廟或鄭王廟的數字時**：先確認 `watrongkhun.org` 是不是還被別家公司佔著、`watarun1.com`／`watarun.net` 是不是恢復了。**任何一天這兩個網域恢復成真正的寺方官網**，就把本篇、`chiang-rai-2-day-itinerary` 與 `bangkok-4-day-itinerary` 的票價出處同一個 PR 換掉。
- **臥佛寺與查龍寺的兩組時間**：之後任一邊改了，本篇 H2-4 的表格、表後那兩句與 summary 第二句要一起改；臥佛寺的 08:00 到 19:30 同時出現在 `bangkok-4-day-itinerary`，兩篇同一個 PR 改。
- **大皇宮 schedules 頁**：正文只寫「當天開不開看官網的 schedules 頁」，不要寫任何具體的休館日期。上線後每次有讀者回報被擋，先回去看那一頁。
- **口徑衝突另記一筆（不影響本篇，但要進票）**：`chiang-rai-2-day-itinerary` `blocks[17]` 寫清萊玉佛寺「開放時間與門票沒有官方公告」，但泰國觀光局東京辦事處的 `wat-phra-kaew` 頁（https://www.thailandtravel.or.jp/wat-phra-kaew/ ）**2026-09-20 審查時逐字讀到**「営業時間　07:00～17:00」「料金　拝観自由」「アクセス　チェンライ市内中心部より車で約20分」（可見內容，不在 HTML 註解內）。要嘛把那句補成官方數字（07:00 到 17:00、免費參拜、市中心車程約 20 分），要嘛在該篇註明為什麼不採用。**注意抓頁陷阱**：同一個網域的 `wat-phra-kaew` 是清萊那座，曼谷大皇宮園區那座玉佛寺沒有獨立的 TAT 東京景點頁，本篇寫曼谷玉佛寺時不能引這一頁。
- **ingest 自檢**：確認 `article` inline 的 slug 與 kind 都存在（本篇會連 `bangkok-4-day-itinerary`、`ayutthaya-day-trip-from-bangkok`、`chiang-rai-2-day-itinerary`、`chiang-mai-3-day-itinerary`、`phuket-old-town-big-buddha-viewpoints`、`chiang-mai-night-markets-walking-streets`、`pattaya-koh-larn-day-trip-from-bangkok`，後三篇是本批第 12、11、13 篇，要同一批進站）；確認全篇**沒有 offer 區塊**；確認結尾**剛好兩個 `link` 區塊、都是城市頁**（`destinations/bangkok`、`destinations/chiang-mai`，兩個網址都要打得開）、**沒有 `foods?…` 的 link**；確認表格是 4 欄；確認 summary 的每一個數字都逐字出現在正文。
