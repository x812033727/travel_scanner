# Till the Verdict Do Us Part｜第 31–40 集系列設定（第四章 Remelt）

寫第 31–40 集分鏡（`docs/videos/till-the-verdict-e031/script.md` … `…-e040/script.md`）的共用帳，讓十集可以同時寫。
劇情照 `../season-01.json` 第 31–40 集（2026-11-10 審稿後的改版），名字、地點與程序照 `../GLOSSARY.md`，外貌、聲音、場景、道具的英文提示詞照 `cast.json`，
審稿決定照 `../review/2026-11-10-ch4.md`、`../review/2026-11-10-season-01.md`，分鏡的教訓照 `../review/2026-11-12-*.md` 與 `screen-test/README.md`。
接在第 21–30 集的 bible 後面。**章界已對齊（2026-11-12）**：30→31 照第 21–30 集 bible 的接點表，錢、天數與星期、誰手上有什麼都接第三章的帳；第 33–36、38 集為了避開國慶連假與週六挪了天數（見〈時間線〉）。Remelt 的格局、三號爐、玻璃管、十二格架與 Remelt 裡的道具句，第 41–60 集都照這份。
這份跟細綱、`GLOSSARY.md` 或 `cast.json` 不一樣的地方，以這份為準。這十集要用的新造型、路人、場景、道具**已加進 `cast.json`（2026-11-12 對齊）**，id 見最後一節；站主要決定的事彙整在 `s1-decisions-e021-e060.md`。

## 全劇固定

全劇固定照第 1–3 集 bible〈全劇固定〉與〈2026-11-12 重審後補定的事〉（台詞用模型原聲、Gemini 只給電話、電視、畫外與心裡話；種田拍法；尺度只守黃標；可讀的字一律不生成；表情寫部位；一鏡最多兩個動作；一鏡最多三張有名字的臉；Grant 的說話句不寫 warm、keynote、smooth），
第 4–10 集 bible〈全劇固定〉（文件與螢幕只拍背面或紙邊、簽名連後製也不上、手機只寫側面的白光、車沒有廠徽與車牌、閃的光寫慢、時間跳躍不用字卡），
第 11–20 集 bible〈全劇固定〉（Elias 的左手、短喊、數字寫成字、Nora 不笑）。以下只列新的、或第 31–40 集特有的：

- **Dr. Brandt 的熱爐禁令**（第 33 集定，GLOSSARY 程序第 2 條）：從失去孩子那晚（第 2 天）算六個月，**不碰熱、不吸煙與粉塵、不提重物**，到第二季初才解。
  第 33–40 集每一鏡照這條演：Nora **從不拿沾著熱玻璃的吹管、從不開爐門、從不搬沙袋與麻袋**；她站在黃色安全線外面喊口令、用手勢比；第 36 集試爐前她已經退到大門口，煙從她身邊湧出去；第 40 集調料在**倉庫**裡（離爐子一面牆），戴防塵口罩與藍色丁腈手套。
  她唯一一次越線是第 33 集的懸念，第 34 集被 Gus 一把拉回、吼她，之後再也不越線。第 40 集她抱著跑進渡輪站的樣品片約兩公斤（一本大精裝書大小），不算重物。
- **吹玻璃的安全，畫面上一律看得到**（setting.json advertiser_safety：爐邊的工作一律有防護）：
  - 拿吹管、開爐門、加料的人：Sparks 戴透明護目鏡（道具句 `clear wraparound safety glasses`）、前臂有隔熱護套（外貌句裡）；Gus 戴皮圍裙、長隔熱手套、面罩（三個道具句，見〈道具的樣子〉）。Gus 穿無袖汗衫、Sparks 穿短袖 T 恤照外貌句，但**手套與眼睛的防護一定寫**。
  - 熱玻璃只落在黑色鋼板或鋼桌上，從不碰到人；燙傷、紅腫、水泡一律不拍、不寫。第 34 集那團玻璃落在她靴尖前**一臂遠**的鋼板上。
  - 火只寫爐口的橘光與門縫的光，不寫火舌朝人竄；第 36 集回火是「爐口噴出一口橘色的火、一秒就收」，那時所有人已經在大門口。煙寫 `thin grey-black smoke drifting under the high roof`，沒有人咳到彎腰。
  - 玻璃不砸（全季規則：只有贗品才在手套、護目鏡、鋼桶裡砸）。Sparks 的歪杯子回爐是用鋼桶倒上長柄加料鏟、推進爐口，不是摔。
  - Sparks 騎機車進廠一定戴安全帽，停好才摘。
- **疤**：Elias 左手背的疤到第 60 集前不出現。這十集 Elias 只穿基本款西裝（不穿 `furnace`；那個造型第 55 集起才用，句子已拿掉手套與疤），左手一律在褲子左口袋或畫框外；簽字、遞東西、拿手機一律右手。
  第 34 集回憶裡把十九歲的 Nora 拉回來的那隻手，**只拍右手**（滿是煤灰的右手抓住她皮圍裙的肩帶），左手、臉、那團熱玻璃落在哪裡都不入鏡（m12 第五季才揭）。
  Gus 的外貌句寫了「兩條前臂與手上滿是舊燙疤」：試鏡證明細的疤會被畫成紅點與傷口，**這十集照〈要站主決定的〉第 5 條的建議寫成風吹日曬的手、不寫疤**；`cast.json` 的外貌句已照這樣改（2026-11-12 對齊），每鏡不必再補。
- **可讀的字**（第四章特別多，審稿 ch4〈全章〉）：**生成一律不出字，後製也不上字**，要觀眾知道的一律有人念出來：
  Pell Glassworks 的招牌（"Pell's."）、Claire Quinn Glass 的招牌（"Mom's studio."）、玻璃管上的六個階段（第 36 集 Nora 念一次 "Report. Charges. Investigation. Arraignment. Trial. Sentencing."，之後只念珠子停的那一格 "Report."）、
  十二格架（"One panel per slot."）、Sparks 的粉筆計數（他每次大聲報數）、第 37 集黑板上的 "Remelt"、第 38 集渡輪站的公告、租約、保付支票、修爐估價單、Hank 的收據、Lyle 部落格的圖說（Grant 念）、報名表、麻袋上的字、牆上的鐘（沒有數字，只有刻度）。
  粉筆字寫成「從黑板側邊拍、只見粉筆與手，或黑板背對鏡頭」；粉筆計數寫成 `short white chalk strokes on the red brick, soft focus`，不寫正字記號的數目。細綱的 "(text added in post)"、"(labels added in post)" 一律取消（理由見〈要站主決定的〉第 3 條）。
- **電話**：照第 11–20 集，兩頭都在畫面上的人用原聲、各自在自己的地方、後製加電話濾波，台詞只放在說話的人自己的鏡上：第 34 集 Dana（在法院走廊）、第 38 集 Hank 打給 Grant（只拍 Hank，Grant 的聲音不出現）、第 39 集 Hank（在他的櫃台）。
  **Gemini 只給電話那頭從不露臉的人**：第 39 集其他砂料行的老闆（新增 extras `supplier-phone`，見〈要加進 cast.json 的〉）。Nora 聽電話的鏡她的嘴不動或嘴不入鏡。
- **回憶**：第 31 集（十二年前 Pell's 門口）與第 34 集（十二年前爐邊，兩秒）。回憶用 `nora` 的 `nineteen` 與 `grant` 的 `young`（`cast.json` 已有外貌句，**都還沒有定妝照**），光寫「溫暖、偏金、微微霧」的夏天下午，跟現在的冷光分開；不用字卡、不用黑白。
  Grant 年輕版的眼鏡照第 1–3 集〈補定〉寫細的圓金屬框（細綱寫的 rimless 不用）。
- **不笑**（接第 21 集 Theo 的 "No smile."，s01-t18 到第 45 集才收）：**Nora 這十集一鏡都不笑**。第 35 集細綱的 "the first hint of certainty at her mouth"、第 37 集的 "color in her face" 都寫成部位：`lips pressed together, corners level, chin lifted`、`colour high in her cheeks from the heat`，加 `no smile at any moment, until the last frame`。
  可以笑的只有：Grant 練過的閉嘴微笑（第 31 集回憶遞名片、第 35 集看照片前那一刻、第 39 集門口 "Need sand, Nor?"）；Hank 收錢時嘴角一提的閉嘴笑（第 38 集）；Sparks 露齒的大笑（第 33 集騎車進來、第 37 集 "Great name!"）。其餘每張臉照第 1–3 集寫 `no smile at any moment, until the last frame`；Theo、Gus、Fiona、Elias、Dana 不笑。
- **季節與天氣**：七月，太平洋西北的夏天。清晨常有海霧，白天乾、陰轉晴，夜裡乾、**這十集不下雨**；沒有人穿大衣（Elias 的大衣道具句這十集不用）。清早寫 `cool marine-layer light`，第 37 集清晨寫 `morning fog`。
- **方位**：Kiln Row 沿著港，**港在街的東邊**：Pell's 的大門朝東，清晨的太陽從水面上照進大門與門上那排高窗（第 31 集的光束、第 37 集 Elias 的逆光、第 40 集的藍光都靠這個）。

## 時間線

第 1 天是 3/17（週二），第 99 天是 6/23（週二）。第 30 集停在第 108 天（7/2 週四）20:58，第 31 集從第 109 天 05:20 開始（2026-11-12 對齊，照第 21–30 集 bible）。
**對齊時挪過的天數**：季細綱把第 33 集放在第 110 天，那天是 7/4 國慶（週六），婦產科門診不開；第 38 集的第 117 天是週六，渡輪站的專案辦公室不開。所以 **第 33 集挪到第 112 天（7/6 週一）**、第 34 集隔天、第 35 集第 114 天、第 36 集整集在第 115 天，**第 37 集點爐仍是第 116 天**（第 41–60 集的爐子天數靠它），**第 38 集挪到點爐當天**（第 116 天週五），截止仍是第 127 天。星期只用來排程，畫面與台詞都不說。
日期：第 109 天 = 7/3（週五，國慶補假）、第 112 天 = 7/6（週一）、第 113 天 = 7/7（週二）、第 114 天 = 7/8（週三）、第 115 天 = 7/9（週四）、第 116 天 = 7/10（週五）、第 126 天 = 7/20（週一）、第 127 天 = 7/21（週二）。
日出日落（西雅圖一帶）：7/3 日出約 05:16、日落約 21:10；7/6 日落約 21:09；7/10 日出約 05:22；7/20 日落約 21:00；7/21 日出約 05:34。

| 集 | 時間 | 天氣與光 | 主要事件 |
| --- | --- | --- | --- |
| 31 | 第 109 天 05:20 → 06:10（現在）；回憶：十二年前夏天下午 | 清晨海霧正在散，太陽很低、從港那邊（東）照過來，Kiln Row 的紅磚與鏽門一面金一面冷藍；廠裡只有門上高窗斜進來的光柱與灰塵；回憶是溫暖偏金的下午 | 黑車停在 Pell's 門前，副駕駛座的門被推開，Nora 下車回頭吼："You stood there!"；她轉身，愣在一扇鏽紅的大鐵門下，抬頭看褪到認不出的招牌："Pell's."；Elias 從駕駛座下車，兩人隔著車頂：她 "He shoved that paper in my face, and you stood there!"，他不看她 "Clause two. You signed it."，她 "I know what I signed!"；他："Dana's filing the forgery report this morning." "With the police. It goes to the prosecutor." "Experts cost money. Lawyers cost money." "You need to work again." "You need a place."；回憶：十九歲的她從同一扇門走出來，一個戴細金屬框眼鏡的年輕男人笑著遞名片："Grant Whitlock. Sales manager."；回到現在："How do you own this place?" "Bought it at a sheriff's sale."；隔壁是一間積灰的小店面，她念："Mom's studio."，抓住生鏽的掛鎖用力搖，放手；Elias 的手機震，他右手接起、走回車邊："I'll wait here."；她推開一扇鐵門，十二年的灰湧出來；深處一座蓋著帆布的大爐子；手電筒的光打在她臉上，一個粗啞的聲音："Who's there?" |
| 32 | 第 109 天 06:10 → 06:40 | 同第 31 集的廠內：高窗光柱、灰塵、冷；大門開著，門外是金色的清晨 | 光束放低，一個駝背的老人穿汗衫站在爐邊，看了她很久："You're the girl from the courthouse steps."；她："Walter signed everything he made. Nobody listened."，聲音破掉："I was nineteen. They laughed at me."，哭出聲；Gus 本來轉身要走，停住、回頭："I didn't laugh. I was there."；她擦臉："You've been here this whole time?" Gus 聳肩："New owner pays the power. Never met him."，眼睛卻越過她、往門外那輛黑車多停了一拍；他扯下三號爐的帆布，十二年的灰像雪一樣落下，黑色的爐口像一口井；他拍拍冰冷的磚："Nobody's lit her in twelve years."；她把手掌平貼在磚上，閉眼 |
| 33 | 第 112 天（7/6 週一）10:00（診間）→ 10:20（走廊）→ 跳 → 14:00 → 16:40（Pell's） | 診間窗外陰、灰白的天光，桌燈冷白；走廊日光燈；下午 Pell's：右牆高窗的白光加小練習爐的橘光 | 診間（只有人與桌，沒有醫療器材）：Brandt "Your body's still healing." "No heat, no fumes, no heavy lifting." "Six months."；Nora 看著自己的手："So ten more weeks."；候診區一個大肚子的孕婦在織一頂很小的淡黃色帽子；Nora 撐到走廊，背貼牆滑坐下去哭出聲；Brandt 跟出來蹲在她旁邊，一句話都不說；下午 Pell's：一部機車轟進大門，平頭、耳釘、兩條前臂隔熱護套的年輕人摘下安全帽："Grandpa! Who's this?" Gus："Your teacher." Sparks："Huh?"；小練習爐前 Sparks 吹第一個杯子，杯子往一邊塌，「啵」一聲：Gus "Crooked." Sparks "I know it's crooked!"，他在磚牆上畫一筆粉筆："One!"；Nora 站在黃線外面喊轉速與換氣，發現每個動作都記得；懸念：Sparks 握錯吹管，她衝過安全線去扳他的手，他一慌甩太快，一團橘紅的熱玻璃滑下管口、往她腳前掉 |
| 34 | 第 112 天 16:40 → 跳 → 第 113 天（7/7 週二）17:30 → 18:30 | 第 112 天同上；第 113 天傍晚，太陽在西、廠裡暗下來，高窗是淡金，練習爐熄了，Peg 角落長椅上方的臨街窗是最亮的光 | Gus 從後面揪住她衣領往回一拽，玻璃落在鋼板上「嘶」地冒白煙、從橘變暗紅："Behind the line! You want to lose your feet?"；她喘著，閃回十九歲：一隻滿是煤灰的右手抓住她圍裙的肩帶往後拉（兩秒）；"Somebody pulled me back before." Gus 什麼都不說；跳到隔天傍晚：Peg 坐在角落長椅上記帳、頭也不抬："Twenty cups. Two days." "Sand's thirty-two bucks a bag."；Sparks 在牆上補一筆："Twenty!"；Nora 的手機響，Dana 在法院走廊："Reyes will review it." Nora："Same Reyes who said half a pill wasn't enough?" Dana："Same Reyes. Different evidence."；Nora 看著光禿禿的紅磚牆："Then I need a glass tube."；Theo 來了（她要的市價租約）："Market rate. Eleven thousand a month."，平板轉向她；Peg 從她肩後看一眼，倒抽一口氣，鉛筆掉在水泥地上 |
| 35 | 第 114 天（7/8 週三）10:00（當鋪）→ 跳 → 14:00 → 14:45（Ashford Construction 頂樓會議室；同時 Grant 的辦公室） | 當鋪暖黃燈，門外港邊晴；會議室整面落地窗外是晴天的港；Grant 的辦公室白、冷、亮 | 第 15 集那間當鋪、同一個玻璃櫃：Nora 把 Grant 給的婚戒放上玻璃，手指不肯鬆開；Peg 的食指把戒指推過去："I pawned mine so you'd keep yours." "Now sell it."；Nora："Sell. Not pawn."；老闆拿放大鏡看："Eleven-eight."；Sparks 瞪大眼："That's a month?"；（保付支票在銀行換，不拍）；會議室：她把保付支票放在長桌上："Clause two. I pay for my own doors."，簽租約："His ring. My furnace."；Elias 站著、右手簽，左手在褲袋裡；插一場 Grant 的辦公室：他手機的白光照在臉上，插一格 Lyle 拍的照片（她走出當鋪），他念圖說："Ex-Mrs. Whitlock cashes out."，練過的笑掉下來；回會議室：她把三號爐的燃燒器估價單放到桌上（她付不起），Elias 把它推回去："Repairs are the landlord's. It's in the lease." "The furnace is mine. The fire's yours."；她套上筆蓋，把紙推回去："Not until my lawyer reads it." |
| 36 | 第 115 天（7/9 週四）09:00 → 跳 → 14:00 → 18:00 → 跳 → 23:30 → 23:45 | 早上晴，臨街窗與高窗的白光；下午太陽移到西邊、廠裡暗一半，紅磚牆在工作燈下；深夜只有工作燈與爐口 | Dana 讀修繕條款，食指點兩下："Landlord fixes his own furnace." "That's not fighting for you. Clause two holds."；Nora 簽估價單；（Ashford 的人當天修燃燒器，不拍）；下午她站上梯子把一根長玻璃管釘上左牆，Nora 念六個階段，一顆琥珀色的玻璃珠放進管口，「叮」，停在第一個銅環："Report."；她在管子下面掛一個舊的十二格樣品架："One panel per slot." "Only what holds up in court." Sparks："And when all twelve are full?" "Then he's sentenced."；整個下午，對街一輛珍珠白轎車怠速停著，方向盤上一隻白手套；Nora 在臨街窗前："That's Cole. Grant's driver."；深夜試爐：Gus 叫大家到門口（"Everybody at the door."），老燃燒器咳出黑煙、「砰」一聲，火從爐口噴出一口；戴面罩的 Gus 一把關掉瓦斯："It backfired. Line's shot."，廠裡都是煙 |
| 37 | 第 116 天（7/10 週五）03:30 → 04:30 → 05:25 | 天亮前：窗外深藍，工作燈冷白；04:30 點爐後整廠是橘光；05:20 日出，門外是被晨光照亮的霧 | 一個穿素面深藍工作外套的技師收工具："Landlord's crew. Lease says so."；Gus 接過扳手，親手把新接頭轉最後一圈："Again."；「轟」：三號爐醒了，橘光淹過 Gus、Sparks、Peg、Nora、紅磚、玻璃管與十二格空架；Gus 在爐前兩步跪下、哭出聲："Walter. She's lit. You hear me? She's lit."；Peg 過去抓住他的肩，自己也哭了；Nora 在一塊舊黑板上寫一個字，念出來："Remelt. Anything we ruin goes back in."；Sparks："Great name!" Peg 擦著眼睛："Inside voice."；她轉身：Elias 站在大門外，背後是亮起來的霧，左手在褲袋裡；他的人做的工，他知道是今晚；她還沒開口，他轉身走進晨霧 |
| 38 | 第 116 天（7/10 週五）08:30 → 跳 → 11:00 → 11:30（渡輪站）→ 跳 → 14:00（Remelt）→ 16:00（Doyle Sand & Batch） | 晴、乾；廠裡三號爐的橘光加門外的白天；新渡輪站三層樓高的空大廳，天窗的白光落在正中央一個空的吊點；Doyle's 下午的太陽、白色的沙塵 | 工作台上一張公告壓在一塊綠玻璃下；Theo 站在門口："Boss said leave it here."；Nora 拿起來念："Ferry terminal chandelier. Blind competition. No names."；渡輪站的專案辦公室，Fiona 抱著厚規格夾："We judge the work, not the names." "Drawings and one sample panel." "Nine a.m., eleven days from today."；空的大廳，她抬頭看那個吊點（顏值鏡頭）；回 Remelt，她攤開草圖：很多片藍玻璃一層層像浪往下落，Sparks："How blue?" "The harbor. Right at dawn."；Doyle's：她訂二十袋，Hank 收了現金、嘴角一提："Truck's Thursday."；她走出去，他拿起電話、壓低聲音："Mr. Whitlock? Yeah. She just ordered sand."，抬眼看她的背影 |
| 39 | 蒙太奇第 119–126 天 → 第 126 天（7/20 週一）19:00 → 19:30 → 20:30（Doyle's）→ 22:00 → 23:59（Remelt） | 蒙太奇每格換光（早上灰、下午亮、傍晚黃）；第 126 天 20:30 Doyle's 的院子是低低的金色夕照；22:00 之後 Remelt 只有三號爐的橘光與一盞工作燈 | 十天的拖："Thursday." "Thursday." "Monday, swear."；截止前一晚 Hank 終於說："Out of stock."，Nora："Then refund me." "Store credit."，喀；她一家一家打，電話那頭（Gemini）："All sold out."；最後一家老闆嘆氣："Whitlock Home's our biggest client." "Portland's got it. Opens at eight."，Nora："I'm due at nine."；她走過轉角到 Doyle's 的院子，指著一整排棧板："That's sand. Right there." Hank："It's spoken for."；Grant 斜倚在後面辦公室的門框上、手裡一杯咖啡："Need sand, Nor? Just ask."；她把 Hank 那張不退錢的收據拍在櫃台上："Keep your credit."，走出去；回 Remelt，她把手機砸進空砂桶、對著爐火的轟聲吼到沒聲音，Peg 不攔她："Let it out, honey."；她背靠紅磚坐在空砂桶邊的地上；午夜，Sparks 一腳踢翻一個空桶："No sand. What are we melting?"；門上那座舊鐘的兩根針在十二點重合，離截止九個鐘頭 |
| 40 | 第 126 天 24:00 → 第 127 天（7/21 週二）00:10 → 01:00 → 03:30 → 04:00 → 05:35 → 跳 → 08:15 → 08:58（渡輪站） | 夜裡三號爐的橘光、倉庫一顆燈泡；05:35 日出，金光從大門與高窗進來；08:58 渡輪站大廳天窗的晴天白光 | Sparks 把一桶歪杯子倒上加料鏟、推進爐口："Remelt, right?" Gus："Not enough for a panel."；Gus 從倉庫拖出一排十二年沒動的舊麻袋："Pell's batch. I still remember the recipe."（Sparks："Is that ours?" Gus："Came with the lease."，選用）；Nora 綁上防塵口罩、捲起袖子："Then we mix our own."；她跪在倉庫的舊天平前，一匙一匙秤深藍色的鈷粉，Gus 念一行配方，她改："Cobalt. Two grams less."；Gus 與 Sparks 分三次把料加進三號爐，她在倉庫門口喊；03:30 第一團是藍的，Sparks 舀、Gus 澆進鋼框模，進退火爐；04:00 Peg 抱著帳本睡在長椅上，Sparks 把自己的外套蓋在她身上、踮腳走回爐邊；05:35 日出，退火爐打開，第一片藍玻璃；她把它舉到大門的晨光裡，一塊港口清晨的藍光滑過紅磚、玻璃管與十二格空架；她低聲念母親的話："Glass cools slowly. So do people."；（她把圖畫完、捲進紙筒，不拍或一鏡）；08:15 Gus 的舊紅色小貨車；08:58 她抱著用灰色搬家毯包著的樣品片衝進渡輪站大廳，Fiona 看錶、蓋章："Entry nine. Just made it."；大廳另一頭，一個戴白手套的人看著那片藍接住天窗的光，舉起手機 |

第 41 集接第 128 天（7/22 週三）的 Remelt：燈箱、地上的草稿（見〈伏筆與回收〉〈第 41 集要接的〉）。

**細綱自相矛盾或站不住、挑了哪一邊**：

- **日期**：細綱第 38 集 Fiona 說 "Nine a.m., the tenth."，可是截止是第 127 天（7/21），「十號」不成立。第 38 集對齊時挪到第 116 天，改成 **"Nine a.m., eleven days from today."**（不說日期）。
  季細綱的第 110 天是 **7/4 週六（國慶日）**，婦產科門診不會開：對齊時把第 33 集挪到第 112 天（週一），第 34–36 集跟著排（見〈時間線〉開頭、〈要站主決定的〉第 9 條）。畫面上沒有煙火與國旗，台詞不說星期與日期。
- **"Six months" 與 "So ten more weeks."**：六個月從失去孩子那晚（第 2 天，3/18）算，到 9/18（第 186 天）；第 112 天還剩 74 天，約十週半。"ten more weeks" 是她往少的那邊算（她急著回爐），**不改**。
- **"Dana filed the forgery report with police this morning."**：第 31 集是清晨五點半，「今天早上已經報了」不成立。改成 Elias 說 **"Dana's filing the forgery report this morning." "With the police. It goes to the prosecutor."**（GLOSSARY 程序第 3 條：先報警、再由檢察官審）。
- **第 31 集的吵架在哪裡**：細綱鉤子寫「車門被推開、她吼、轉身愣在鐵門下」，衝突欄又寫「在車上爆發」。照鉤子：吵架在車外、**隔著車頂**，第一句 "You stood there!" 是她下車那一刻吼的；"He shoved that paper…" 那一段在她認出 Pell's 之後、Elias 下車時接著吵完（她剛認出這裡，火更大：他偏偏把她帶到這裡）。回憶放在吵完、他說 "You need a place." 之後。
- **第 31 集的 "Who's there?"**：Gus 從第 32 集起在畫面上說話（原聲），這句不能用 Gemini 畫外。寫在他自己的鏡上：手電筒在他右手、齊胸，往下漏的光只照到他的下巴與嘴（鼻子以上在暗裡），原聲；第 32 集第一鏡光束放低，才看到整張臉。
- **Peg 當掉的戒指錢**：細綱第 34 集寫她「手上只有 Peg 當戒指剩下的錢」，可是第 11–20 集 bible 的帳裡那 $400 第 9–15 天就用完了，之後靠 Peg 的退休金與 Nora 賣畫。改成「Peg 的現金」（第 107 天退休金進帳後約 $1,400，見〈帳〉），不說出口。
- **第 35 集戒指誰推**：戒指在 Nora 的卡夾裡（第 15 集 Peg 推回給她）。改成 Nora 自己把戒指放上玻璃、手指不肯鬆，Peg 的食指替她把戒指推完最後一段，同時說那兩句。
- **第 35 集戒指賣多少**："That's a month?" 要先有人說出價錢，Sparks 才有得驚訝。當鋪老闆說 **"Eleven-eight."**（$11,800）：
  一顆跟鉛筆一樣寬（約 8 公釐、約兩克拉）的圓鑽加鉑金戒台，當鋪直接收購付得出這個數；剛好比一個月房租多一點，"That's a month?" 才好笑也才痛（帳見〈帳〉）。
- **第 34 集 Peg 的筆**：她記帳用的是插在帳本書脊的鉛筆（第 4–10 集道具）。掉在地上的是那支**鉛筆**。
- **第 36 集 Cole 的車**：細綱寫「一輛黑色轎車怠速」。第 10–20 集的黑車是 Elias 的，再來一輛黑車，觀眾會以為 Elias 回來守著。改成 **Grant 的珍珠白轎車**（`grant-car`，第 5–9、18 集觀眾認得），方向盤上一隻白手套；第 40 集 Cole 在渡輪站大廳是本人（站主可推翻，見〈要站主決定的〉第 2 條）。
- **第 36 集的玻璃管**：細綱 "six stages etched along it (labels added in post)"。改成六個素面的小銅環（`cast.json` 的 `case-tracker` 也是銅色記號）、沒有字；六個階段由 Nora 掛好時念一次。
  珠子是**琥珀色**（`cast.json` 寫 clear：透明珠子在透明管裡，手機螢幕上看不見）。
- **第 37 集的技師**：照審稿：換瓦斯管要有執照，是房東（Ashford Construction）派的值班技師，Gus 盯著、最後一圈自己轉。技師的外套沒有字，身分靠他那句 "Landlord's crew. Lease says so."。
- **第 37 集 Gus「在爐口」哭**：開著的爐口前不能跪。改成：爐子點著後 Gus 把爐門推到只剩一道發光的縫，退兩步、跪在黃線上哭；手套與皮圍裙還穿著，面罩推到頭頂。
- **第 39 集「她開車去 Hank 的砂場」**（審稿 ch4 第 39 集）：她沒有車。Doyle Sand & Batch 就在 Kiln Row 轉角（細綱 "off Kiln Row"），走路三分鐘。
- **第 39 集她摔的手機**：細綱要她有一支手機（第 34 集接 Dana 的電話、第 39 集一家一家打）。季細綱第 23 集寫她「把 Grant 那支的 SIM 拔掉、有了自己的號碼」，可是 Grant 給的白手機第 12 集起鎖在 Bev 的抽屜，第 21–30 集 bible 把第 23 集的新號碼換給了 Peg 的手機，Nora 第三章沒有手機。
  **對齊後**：第 111 天 Peg 在山腳便利店替她買一支便宜的預付手機（$40，記在帳本 Nora 那一欄，不拍、不念），道具句 `nora-own-phone`；第 34 集起用它，第 39 集砸進空的鋼砂桶、螢幕裂了；截止之後她從桶底撿回來，還能用（不拍；第 41–60 集同一支，畫面只拍側面白光與背面）。
- **第 40 集九個鐘頭做得出一片嗎**：新料進爐要熔、要澄清，退火也要時間。這份照戲的需要壓到最緊、但每一步都說得通：00:10 拖出麻袋，00:20–01:00 秤料，01:00–02:30 分三次加料（爐子已經熱了十一天），03:30 第一團是藍的、澆進鋼框模，進退火爐跑短程（Gus："Short soak. She'll hold."，選用），05:35 日出時打開。
  **為什麼拖到 8:58**：玻璃要慢慢冷到能拿（母親那句 "Glass cools slowly. So do people." 就是答案），而且她整夜在秤料，比賽要的「圖」還沒畫完：日出之後她在工作台上畫完、捲進紙筒（一鏡或不拍）；08:15 Gus 開他的舊小貨車，早上塞車，08:58 到。
- **第 40 集用 Pell's 的舊料算不算 Elias 給的**：這間廠連同裡面的設備與存料，是她照市價租的（租約寫「含設備與存料，照現況」，見〈帳〉）。料是她租來的，不違反第二條；Gus 一句 "Came with the lease." 交代（選用，見〈要站主決定的〉第 6 條）。
- **第 40 集的白粉**：照審稿：一律寫**深藍色**的鈷粉、大麻袋、玻璃廠背景，她戴防塵口罩與丁腈手套；不拍白色粉末的特寫；麻袋裡倒出來的沙料寫 `pale grey sand`，只在大鏡位裡出現。
- **第 40 集 Claire 的回憶**：細綱角色欄列了 Claire，轉折欄只寫 "Nora whispers her mother's words"。這份照轉折欄：**沒有 Claire 的回憶鏡**，Nora 自己低聲念（原聲）；理由見〈要站主決定的〉第 4 條。
- **第 32 集的爽點標籤**：細綱標 public_vindication，可是只有 Gus 一個人在場（審稿）。分鏡照「被認出來」（recognition）寫，沒有旁人、沒有掌聲。

## 接點表

| 集 | 最後一鏡（= 下一集第一鏡的同一刻；跳時間的寫用什麼畫面交代） |
| --- | --- |
| 30 → 31 | **2026-11-12 對齊，照第 21–30 集 bible 的接點表**：Whitlock Home 旗艦店的後台走廊中段，第 108 天 20:58。鐵網燈泡下，Nora（`gown`，眼睛濕，左手無名指 Elias 的戒指，右手拿著疊在一起的兩張影本、紙背朝鏡頭，手拿包夾在左腋下）面向走廊盡頭；Peg（`visit`，喘著、眼鏡上有淚）在她左邊半步；鐵門關著；Grant 已經走出畫面；走廊盡頭最後一盞頂燈下，Elias（基本款，左手插在褲子左口袋）站著沒動，Theo（基本款，平板在左手）在他左邊，Elias 剛說完 "Clause two."。**第 31 集第一鏡跳到第 109 天 05:20 的 Kiln Row**（約八個半小時）：交代時間的是剛出海面的低太陽與散開的海霧；副駕駛座的門從裡面推開，Nora 換成 `shoulder`（奶油色毛衣、深色長褲、短靴）外罩道具句 `nora-jacket`（她回過 Ashford 家、一夜沒睡；這是她婚前的舊工作外套，第 7 集別人替她收的行李裡就有），Elias 基本款、沒有大衣、自己開車，Theo 與 Peg 不在。兩張影本天亮前由 Theo 送到 Dana 那裡（Dana 當天早上報案；第 41 集帶來 Remelt）。 |
| 31 → 32 | Pell's 廠內，第 109 天約 06:10。從大門往裡拍：Nora（`shoulder`、外套敞開）站在剛推開的那扇鐵門裡三步，背後是金色的清晨與灰塵的光柱，右手舉到眉前擋光，臉朝畫面深處；深處正中蓋著灰色帆布的三號爐，爐前約兩步是一束手電筒的白光直直打在她臉上；拿手電筒的人（Gus）在光後面，只見齊胸的手電筒、右手、被漏光照到的下巴與嘴。門外（畫面外）黑車停在門前，Elias 在駕駛座講電話。**第 32 集第一鏡**：光束放低、落到地上。 |
| 32 → 33 | Pell's 廠內，三號爐前，第 109 天約 06:40。帆布堆在爐腳，灰塵還在高窗的光柱裡往下落；Nora（`shoulder`）面對爐子站著，右手手掌平貼在冰冷的紅磚上、手指張開，眼睛閉著，臉上有淚痕，頭髮垂在臉邊；Gus（基本款）在她左邊一步，右手剛從磚上拿開，看著她的手。**第 33 集跳到第 112 天 10:00 的診間**（三天後，國慶連假之後的週一）：第一鏡是她的兩隻手掌平放在膝蓋上（跟上一集貼在磚上的手同一個姿勢的跳接，鉤子），交代時間地點的是診間的白天窗光、桌燈，與她換成新造型 `henley`（灰色亨利領長袖、低馬尾）。 |
| 33 → 34 | Pell's 右牆的小練習爐前，第 112 天約 16:40，右牆高窗的白光加練習爐的橘光。Sparks（基本款、透明護目鏡、隔熱護套）在畫面右，兩手握著吹管、管子剛甩過頭，管口那團橘紅的熱玻璃滑下來、正落在半空；Nora（`work`，護目鏡推在頭頂、圍裙、袖子捲到手肘）**左腳已經跨過黃線一步**，兩手伸向 Sparks 握管的手，臉朝畫面右；她靴尖前一臂遠是那塊黑色鋼板；Gus（基本款加皮圍裙、面罩推到頭頂）在她右後方一步，右手正伸向她的後衣領。**第 34 集第一鏡**：Gus 的手揪住衣領、往後一拽。 |
| 34 → 35 | Pell's 前左角的長椅旁，第 113 天約 18:30，傍晚，練習爐已熄，臨街窗是最亮的光，高窗淡金。Theo（基本款）站在畫面右，兩手捧著平板、螢幕轉向 Nora（背對鏡頭），剛說完 "Eleven thousand a month."；Nora（`work`，護目鏡推在頭頂）在他面前一步，背半對鏡頭；Peg（`visit`，眼鏡戴在臉上）坐在她右後方的長椅上，帳本攤在左膝，嘴張著倒抽一口氣，右手空著、手指還保持拿筆的形狀；那支鉛筆在她腳邊的水泥地上。**第 35 集跳到第 114 天 10:00 的港邊當鋪**：交代時間的是當鋪的暖黃燈與門外晴天的港、Nora 換成 `henley` 加外套、Peg 的帆布袋在左肩，Sparks 也在。 |
| 35 → 36 | Ashford Construction 頂樓會議室，第 114 天約 14:45，整面落地窗外晴天的港。長桌一端：Nora（`henley`，外套搭在椅背）坐著，右手剛套上筆蓋，左手（Elias 的戒指）把那張淡黃色估價單沿桌面推回去，剛說完 "Not until my lawyer reads it."，下巴抬著；Elias（基本款）站在桌對面，右手停在桌面上那張保付支票旁，左手在褲袋裡，看著她；Theo 在桌尾、平板抱在胸前（虛焦）；租約在 Nora 手邊（紙背）。**第 36 集跳到第 115 天 09:00 的 Pell's**：第一鏡是 Dana 的食指在租約那一頁上點兩下（紙邊、側拍），交代的是廠裡早上的光、Dana 的卷宗、Nora 換回 `work`。 |
| 36 → 37 | Pell's 廠內，第 115 天約 23:45。廠裡一層灰黑的煙浮在高屋頂下，一盞工作燈的冷白光穿過煙；三號爐的鐵門半開，爐口黑著，一縷煙還往外飄；Gus（基本款加皮圍裙、長隔熱手套、**面罩拉下**）站在爐右邊，右手剛把瓦斯閥的紅色把手扳下來，剛說完 "It backfired. Line's shot."；Nora（`work`，左前臂擋在口鼻前）與 Sparks 擠在敞開的大門口（畫面前景、背影與側臉），門外是夜；Peg 這晚不在（第 37 集 03:30 前才來）。**第 37 集跳到第 116 天 03:30**：交代的是煙散了、空氣清了、一盞三腳架工作燈、地上一段發亮的新黃銅接頭、窗外是天亮前的深藍。 |
| 37 → 38 | Pell's 大門內，第 116 天約 05:25。從廠裡往大門拍：前景是 Nora（`work`，護目鏡推在頭頂）的右肩與後腦，被身後三號爐的橘光照亮；敞開的大門外是被日出照亮的白霧，Elias（基本款）的背影已經走出門外三步、往霧裡走，左手在褲袋裡，愈來愈淡；畫面左前，Peg 的手還搭在 Gus 的肩上（虛焦）。**第 38 集跳到同一天 08:30**（三小時後）：交代的是白天的光、三號爐還燒著、工作台上多了一張壓著的紙。 |
| 38 → 39 | Doyle Sand & Batch 的櫃台，第 116 天約 16:15，午後太陽從院子斜進來、空氣裡白色的沙塵。Hank（基本款）在積灰的櫃台後，右手把一支刮花的黑手機貼在右耳，剛說完 "She just ordered sand."，抬眼看畫面左外；從他身後開著的門看出去，院子裡 Nora（`henley`、外套）的背影正走向街，越來越小。**第 39 集第一鏡跳到幾天後**：同一個櫃台、同一個姿勢，Hank 拿著電話，但光換成灰白的早上（"Thursday."）。 |
| 39 → 40 | Remelt 廠內，第 126 天 23:59→24:00。三號爐開著一道發光的門縫、轟轟地燒；爐右邊那排空的鋼砂桶，一個剛被踢翻、側躺著還在晃；Sparks（基本款、護目鏡掛在 T 恤領口）站在它旁邊，剛吼完 "What are we melting?"；Nora（`work`，護目鏡推在頭頂，臉上有乾掉的淚痕）背靠紅磚坐在空桶旁的地上，兩手搭在膝上；Gus 站在爐邊；Peg（`visit`）坐在前左角長椅上；大門上方那座舊鐘的兩根針剛在十二點重合（只見刻度，沒有數字）。**第 40 集第一鏡是同一刻**：Sparks 提起一個裝著歪杯子的鋼桶。 |
| 40 → 41 | （2026-11-12 對齊：第 41–50 集 bible 的 40→41 照這格。）新渡輪站大廳，第 127 天 08:58，天窗的晴天白光。報名桌（一張摺疊桌）後，Fiona（基本款）右手剛把日期章從報名表上提起，左手腕的錶面朝著她自己，剛說完 "Entry nine. Just made it."；Nora（`henley`，袖子捲到手肘、前臂上一層藍粉，喘著，頭髮從馬尾散出幾縷）站在桌前，兩手扶著桌上半拆開的灰色搬家毯，裡面那片藍玻璃接住天窗的光、在桌面投下一塊藍；紙筒在她左腋下；大廳另一頭（畫面右後、很遠、虛焦）Cole（黑西裝、白手套）把手機舉到耳邊。**第 41 集跳到第 128 天的 Remelt**：交代時間的是燈箱從下往上的白光、地上鋪滿的草稿、Nora 換回 `work`，那片藍玻璃不在廠裡（交出去了）。 |

## 帳

**錢**（數字只在標「念」的地方說出口；2026-11-12 對齊，接第 21–30 集 bible 的帳）

第 30 集結束時：Peg 約 **$1,403**（第 107 天退休金剛進），Nora 自己約 **$26**；帳本的 Nora 欄記著她欠 Peg 的一半菜錢約 $80，"Owed to Ashford" 一欄是一件禮服（第四章不還、不提）。
兩人照住 Ashford 家、不付房錢；菜由 Peg 買、Peg 煮，Nora 的一半記在 Nora 欄。通勤坐公車：山腳的站走路 10 分鐘，山腳 → Kiln Row 轉一次車約 35 分鐘、一人 $2；Nora 付不出來的公車錢也記 Nora 欄。

| 天 | 誰的錢 | 進 | 出 | 說明 |
| --- | --- | --- | --- | --- |
| 109 | — | | | Elias 開車，不花錢 |
| 111 | Peg | | Nora 的預付手機 $40（記 Nora 欄） | 山腳便利店，不拍、不念 |
| 112 | Peg | | 砂兩袋 $64 | Gus 打電話叫 Doyle's 送兩袋給小練習爐（不拍）；Peg 付現給送貨的人 |
| 113 | Peg | | 砂兩袋 $64 | 同上，不拍。Peg 念："Sand's thirty-two bucks a bag."（四袋 $128，總數不念）；Theo 念："Market rate. Eleven thousand a month." |
| 114 | Nora | 賣戒指 **$11,800**（念："Eleven-eight."） | 保付支票 **$11,000**（第一個月房租）；還 Peg 砂錢 $128 | 當鋪老闆開公司支票，她在銀行存進自己的戶頭、換保付支票（不拍）；Peg 的帳本記一行（選用念 "Sand. Paid back."） |
| 114 | Peg | 收回 $128 | | |
| 115–116 | — | | | 燃燒器與瓦斯管：房東修（租約條款），Nora 不花錢 |
| 116 | Nora | | 砂二十袋 **$640**（現金給 Hank，不念總數） | 付完她身上約 $40（$26 加這章淨增的 $32，扣掉第 114–116 天自己的公車），**比一袋砂多一點**，這就是細綱的「最後的錢」 |
| 126 | Nora | | （$640 變成 Doyle's 的「店內抵用」，退不出來） | Hank 念 "Store credit."；那張收據第 39 集她拍在櫃台上、留在那裡 |
| 127 | — | | | 舊料是租約裡的存料；Gus 的小貨車油錢不提；報名不收費 |

- **這章結束（第 127 天）**：Nora 身上只剩幾塊錢（第 117–127 天的公車）；帳本 Nora 欄欠 Peg 約 **$330**（第三章的菜錢 $80、手機 $40、第 109–113 天的公車、這章的一半菜錢）。Peg 約 **$930**（扣掉手機、這章的菜錢約 $380 與兩人的公車；砂錢已收回）；下一筆退休金第 138 天（8/1）。
  Doyle's 那 $640 的店內抵用，帳上算資產、用不出去，之後不回收。
- **Gus 與 Sparks 的工錢**：這章 Nora 付不出來，Gus 說先做（不拍、不說）；第 142 天渡輪站的訂金進來時一次補（第 41–50 集 bible）。
- **租約**（第 35 集簽）：照市價 **$11,000／月**，按月續租、每月預付；起算日寫第 112 天（她第一天用練習爐），所以第 33–34 集不是白用。押金不提（審稿沒問、觀眾也不會問）。
  **全包價**：含水電瓦斯（Gus 第 32 集那句 "New owner pays the power." 之後也一樣）、**含廠內設備與存料，照現況**（三號爐、練習爐、退火爐、倉庫裡的舊料與舊燈箱都在租約裡）；**設備的修繕歸房東**（第 35 集 Elias 那一行、第 36 集 Dana 定案）。這些條款都不念出來，只念 "Repairs are the landlord's. It's in the lease."。
  第一個月付到第 141 天，**第 142 天要付第二個月**，第三個月第 172 天（第一季之後）。
- **Peg 的當票**：一直夾在帳本書頁裡；每三十天續一次 $40（第 38、68、98 天已續），下一次是第 128 天（第 41 集，Peg 付）。這十集不續、不拍。Peg 的左手無名指一直是那圈淡色的皮膚。

**戒指**

- **Nora 的婚戒（Grant 給的）**：從第 15 集起在卡夾的拉鍊袋裡。第 35 集當鋪：她從卡夾拿出來、放上玻璃櫃（`a polished platinum wedding ring set with one round diamond as wide as a pencil, lying on the glass counter`），手指按著不鬆；Peg 的食指把它推過去；老闆用放大鏡看、念 "Eleven-eight."。之後歸當鋪，不再出現。
- **Elias 給的戒指**：第 20 集起在她左手無名指，**每一鏡拍到她的左手都寫**。第 40 集秤料時戴丁腈手套，戒指在手套下（寫 `blue nitrile gloves` 就好，不寫戒指）。
- Peg 自己的婚戒在當鋪後面（不展示），第 35 集她不看櫃子、也不問（她只看 Nora 的手）。

**砂與二十個歪杯子**

- 砂一袋 **$32**（Peg 念）。小練習爐第 112–113 天用了四袋，袋子不入鏡。
- **二十個做壞的**：都是 Sparks 吹歪的小杯子。每一個進小退火爐冷好，排在練習爐旁那層鋼架上；他每次在架子旁的紅磚柱上補一筆粉筆、大聲報數（"One!"……"Twenty!"）。
  第 34 集租金一報出來，Peg 就定了規矩：房租沒著落前不再練（不拍）。所以第 34 集之後架上停在二十個。所以第 36–39 集架上一直是那一排、粉筆一直是那一片，第 40 集 Sparks 才把整排倒進鋼桶、回爐。
- **二十袋**（第 38 集訂）：從沒送來。Hank 第 39 集說 "Out of stock."、不退錢、只給店內抵用。
- **空砂桶**：三號爐右邊靠後牆一排四個齊腰高的鋼桶，第 37 集點爐後就是空的（點爐用的是 Gus 留著的最後一點料，不拍）；第 39 集她把手機砸進最左邊那個、Sparks 午夜踢翻右數第二個。
- **Pell's 的舊料**：倉庫後牆一排六個舊麻袋（`old burlap sacks…`），十二年沒動；第 40 集 Gus 與 Sparks 一袋一袋拖出來（Nora 不搬）。用掉四袋，第 41 集還剩兩袋靠在倉庫牆邊。
- **鈷粉**：倉庫架上一個舊玻璃罐裡的深藍色粉；Nora 用小鋼匙一匙一匙秤；她改的那行 "Cobalt. Two grams less." 只念，天平的刻度看不清。

**玻璃管、珠子與十二格架**

- 玻璃管：第 34 集她說 "Then I need a glass tube."；Gus 從倉庫拿出一根舊的長玻璃管（不拍）。第 36 集她站上梯子、用兩個素面鋼架把它**水平**釘在左牆靠大門那一段、比頭高一點；管上一排六個小銅環，間距一樣，沒有字。
- 珠子：一顆指尖大的琥珀色玻璃珠。第 36 集她從管口放進去，「叮」，滾到第一個銅環停住，她念 "Report."。**第 36–40 集一直停在第一格**（第 49 集前不動，`cast.json` 的 `case-tracker` 註記）。
- 十二格架：一個舊的鋼製樣品架，一排十二格直立的空槽、每格一本精裝書大小，第 36 集掛在玻璃管正下方、她胸口到頭頂的高度；**一直是空的**（evidence wall 0/12），寫 `a long row of empty upright slots`，不寫數目。
- 第 37 集點爐的橘光、第 40 集那塊藍光，都要照到管子與空架（細綱的華麗鏡頭）。

**文件**（一律背面或紙邊；誰拿著都寫哪隻手）

- 偽造案的報案：第 31 集只用說的（Dana 今天早上去報）；不拍警局。追蹤管上的珠子停在 Report 就是它。
- 渡輪站的公告：第 38 集壓在工作台上一塊綠玻璃下（正面朝下），她拿起來時紙背朝鏡頭、她念出標題。之後釘在工作台旁的木板上（紙背或很遠）。
- 租約、保付支票、估價單：第 35 集會議室長桌上排一列（細綱的華麗鏡頭），只拍側面與紙背；租約 Nora 簽、Elias 右手簽（只拍筆與手）；支票是她從外套內袋拿出來放上桌；估價單她推回去、第 36 集 Dana 讀過後她在 Pell's 的工作台上簽（只拍筆尖在紙邊動）。之後租約與估價單在 Dana 的卷宗裡。
- Hank 的收據：第 38 集他撕給她（淡粉紅複寫聯），她收進外套口袋；第 39 集拍在他櫃台上，留在那裡。
- 比賽的圖：第 38 集她攤在工作台上的草圖（水彩，可以拍正面，沒有字）；第 40 集日出後她畫完正式的圖、捲進灰色紙筒，08:58 夾在左腋下交出去。報名表 Fiona 蓋章（紙遠遠虛焦）。
- 第 30 集的兩張影本（財產協議簽名頁影本、設計權轉讓書影本，`photocopy`）在 Dana 那裡（第 109 天天亮前 Theo 送去）；婚前草圖資料夾、裝三張紙的牛皮紙信封在 Nora 的行李箱（Ashford 家客房）。這十集**都不入鏡**；第 41 集 Dana 帶影本、Nora 帶資料夾到 Remelt（2026-11-12 對齊）。

**手機**

- Nora 的手機（`nora-own-phone`，第 111 天 Peg 替她買的預付手機，見〈細綱自相矛盾〉）：`a plain black phone in a clear case, no logo, about the size of her palm`。第 34 集接 Dana（螢幕只見側面白光，她右手貼右耳）；第 39 集打給 Hank 與各家砂料行，22:00 砸進最左邊的空砂桶（「咚」一聲），螢幕裂了；第 40 集一直在那個桶底，不拿出來；之後她撿回來、還能用（第 41–60 集同一支）。
- Elias 的手機：`a black phone with no logo, about the size of his palm`（第 2 集原句），第 31 集右手接、走回車邊。
- Grant 的手機：同一句，第 35 集右手拿著、螢幕的光從側面照在他臉上；Lyle 的照片用全畫面插鏡（不拍手機，照第 19 集 Sienna 貼文的做法）。
- Hank 的手機：`a scratched black phone with no logo, about the size of his palm`，第 38、39 集。
- Cole 的手機：`a black phone with no logo, about the size of his palm`，第 40 集最後一鏡。
- Dana 的手機：第 34 集她在法院走廊，右手拿著貼右耳（同 Elias 那句，換成 `her palm`）。

**車**

- Elias 的黑車（`black-car`）：`a long black luxury sedan with no badge, number plate out of frame`。第 31–32 集停在 Pell's 門前的路邊，車頭朝畫面左（往 Rosa's 那個街角），副駕駛座那側靠人行道；第 32 集結尾他開走（不拍，第 33 集不在）。第 37 集他走路來、走路走（車停在街角，不入鏡）。
- Grant 的珍珠白轎車：`a long pearl-white luxury sedan with tinted rear windows, no badge, number plate out of frame`。第 36 集停在 Pell's **對街**（港那側）的路邊、車頭朝畫面左，Cole 在駕駛座，只見方向盤上一隻白手套與黑袖口；從臨街窗看出去寫 `, idling at the far curb across the street`。
- Gus 的小貨車（新）：`an old faded red pickup truck with no badge, number plate out of frame`，平常停在 Pell's 旁的小巷；第 40 集 08:15 載 Nora、Sparks 與樣品片去渡輪站（Peg 留在廠裡睡；Gus 開車，車裡不拍）。
- Sparks 的機車（新）：`an old black motorbike with no badge, number plate out of frame`，第 33 集騎進大門、停在門內右邊，之後一直停在那裡（拍到大門內右側就寫）。

**Peg 的帳本、鉛筆、眼鏡與袋子**

- 帳本：第 34 集攤在她左膝；第 35 集在帆布袋裡；第 37 集在長椅上；第 39–40 集抱在胸前、睡著時也抱著。字從不入鏡，只念：第 34 集 "Twenty cups. Two days." "Sand's thirty-two bucks a bag."（選用：第 35 集 "Sand. Paid back."）。
- 鉛筆：插在帳本書脊；第 34 集掉在地上，第 35 集起又插回去（不拍撿）。
- 眼鏡：玳瑁框，**每一鏡都戴在臉上**，包括第 40 集睡著。
- 帆布袋：出門在左肩；在廠裡放在長椅上她身邊。收據（第 52 集的證物）一直在帳本封皮夾層；當票在書頁裡。

**Elias 的左手、Nora 的左手**

- Elias：每一鏡寫左手在哪（褲子左口袋，或在畫框外）。第 31 集開車時左手在車窗下緣以下；第 35 集站著簽約；第 37 集門外背影也寫 `his left hand in his trouser pocket`。
- Nora：左手拍到就寫 Elias 的戒指（`a plain narrow white-gold band with no stone, on her left ring finger`）。

**路程與花費**

- Ashford 家（山腰）→ Kiln Row：公車（山腳轉一次）約 35 分鐘、一人 $2；開車約 20 分鐘（2026-11-12 對齊，四章同一個數）。Nora 與 Peg 坐公車；第 31 集是 Elias 開車。
- Kiln Row → Merrow General：公車約 25 分鐘。
- Kiln Row → 港邊當鋪：公車約 15 分鐘（當鋪在汽車旅館那一帶的港邊，第 15 集）。
- Kiln Row → Ashford Construction（市中心的大樓）：公車約 15 分鐘。
- Pell's → Doyle Sand & Batch：走過 Kiln Row 的右邊街角，**走路三分鐘**；二十袋要卡車送（"Truck's Thursday."）。
- Pell's → 新渡輪站：Gus 的小貨車平常 20 分鐘，第 40 集早上塞車約 40 分鐘（08:15 出發、08:55 停車、08:58 衝進大廳）。
- Pell's → Whitlock Home 旗艦店：這十集沒人去；Grant 的辦公室在旗艦店樓上。

## 場景格局

| 場景 | 參考圖 | 格局 |
| --- | --- | --- |
| Kiln Row（Pell's 門前的街） | 待畫（`pell-ext`，句子已改成直式、時間與天氣寫在鏡上；這章畫清晨版） | 一條沿港的窄街，舊紅磚廠房一整排、鐵門都鏽成深紅。**鏡頭在港這邊往街裡拍**：Pell's 在正中，兩層樓高的紅磚，正面一扇高大的鏽紅色**雙開鐵門**（一扇門板跟一個人張開雙臂一樣寬，寬到過得了卡車），門上方一條褪到認不出字的漆招牌，招牌上面一排高窗（有幾格破了）；**大門左邊一扇齊眼高的髒臨街窗**。Pell's 右邊緊鄰 Claire Quinn Glass（見下）；左邊是另一間死掉的玻璃廠；畫面最左遠處的街角是 Rosa's 的小店（清晨關著、鐵捲門拉下，這十集不拍人）。右邊街角轉進去是 Doyle's。黑車停在 Pell's 門前、車頭朝畫面左。港在鏡頭後方（東），清晨的太陽從鏡頭這邊照在廠房正面。 |
| Pell's 門口（十二年前，回憶） | 待畫（新增 `pell-door-flashback`） | 同一扇雙開鐵門，十二年前漆成深紅、乾淨，門開著，裡面是爐火的橘光；招牌是新的（字在畫框外或虛焦）；夏天下午溫暖偏金的光、微微霧；人行道上停著一台舊的白色廂型車（不入字）。 |
| Claire Quinn Glass（隔壁） | 待畫（併在 `pell-ext`；搖鎖的近景從同一張參考圖取景） | Pell's 右邊一間單層紅磚小店面：一扇積灰的展示窗（裡面隱約幾個空的木架），一扇窄木門，門上一副生鏽的搭扣與掛鎖；窗上方褪色的手漆店名，認不出字。Nora 站在門前搖鎖時，鏡頭在她左後方、店名在畫框上緣外。 |
| Pell Glassworks／Remelt 主廠房 | `assets/refs/set-remelt.jpg` **只當色調與材質的參考**（橫式、爐子是圓的鋼殼、爐上有可讀的 "Number Three" 字樣、桌上有一個有字的框，都不能照用）；要畫直式：`remelt-cold`（第 31–35 集，冷、灰塵）與 `remelt`（第 36–60 集同一個 id、同一句；白天、夜、天亮、黃昏開門幾版，架上放什麼、燈箱、吊燈、木架都寫在鏡上） | **這一格是第 31–60 集 Remelt 唯一的格局（2026-11-12 對齊，第 41–60 集的 bible 照這格）。從大門往裡拍是標準方向**（鏡頭背對大門、看向後牆）：<br>**後牆正中**：三號爐，一座巨大的圓頂爐，深紅耐火磚、外面箍著鏽鋼帶，大約兩個人高，一根鋼煙囪往上穿出屋頂；胸口高度一個圓爐口，掛一扇鉸鍊鐵門（門上一個小窺孔）；爐口前地上一塊黑色鋼板；離爐口約三大步，地上一條磨舊的**黃色安全線**橫過整個廠，練習爐那區也在線內。瓦斯管沿後牆離地一膝高，接到爐子右邊一個紅色把手的閥。<br>**後牆右段**：大退火爐（齊胸的鋼箱、站在腳架上）；它右邊一排四個齊腰高的空鋼砂桶。<br>**後牆左段**：倉庫的木門（半開）；門與爐子之間靠牆一個吹管架（`blowpipe-rack`）。第 55 集起爐口旁兩張圓鋼凳（`steel-stool`）。<br>**右牆**：上半一排高窗；下面是小練習爐（齊腰高的圓爐、站在鋼腳上，爐口一個餐盤大）、旁邊一張吹玻璃的長凳與一張鋼面滾料台、小退火爐、一層鋼架（Sparks 的歪杯子）、架旁一根紅磚柱（粉筆計數）。第 46 集起右牆靠大門那段立一排木架放藍面板（`blue-panel-row`）。一個紅色滅火器掛在爐邊的牆上（沒有字）。<br>**左牆**（長的紅磚牆）：靠大門那一段，比頭高一點是第 36 集釘上的玻璃管，正下方是十二格架；左牆中段一座舊黑板靠著（第 37 集）；第 54–56 集行軍床靠在黑板旁、安全線外。<br>**前牆**（大門那面，從裡面看）：大門（兩扇鏽紅的鉸鍊鐵門，往裡開）在中間偏右；大門左邊是那扇臨街窗，窗下是 Peg 的**長木椅**（前左角）；大門上方掛一座舊圓鐘（白面、黑色刻度、沒有數字）；鐘上面是高窗。<br>**中間**：一張很重的長木工作台，前後向擺（公告、草圖、估價單都在這裡；第 41 集起靠爐子那一頭放燈箱 `light-box`、上方吊一盞工作燈 `work-lamp`、桌下一層放資料夾的層板）。Sparks 的機車停在大門內右邊。<br>**光**：清晨的太陽從大門與門上高窗照進來（東），白天右牆高窗是冷白光，晚上是爐口的橘光加一盞三腳架工作燈。<br>**反打**（從爐口往大門拍）：大門在正中、背光；Peg 的長椅在畫面**右**前、玻璃管與十二格架在畫面**右**牆、練習爐在畫面**左**。 |
| 倉庫 | 待畫（新增 `pell-storeroom`） | 三號爐左邊那扇木門進去：沒有窗、一顆燈泡；木架上積灰的舊玻璃罐（標籤都掉了、沒有字），後牆一排六個舊麻袋；一個倒放的木箱上擺著一台舊的鋼製天平（黃銅秤盤、滑砣）；架子旁靠著一台積灰的舊描圖燈箱（第 41 集搬到工作台上，就是 `light-box`）。第 40 集 Nora 跪在木箱前秤料，**門開著**，從門縫看得到三號爐的橘光；她喊口令時站在門檻上，不出門。 |
| Merrow General 婦產科診間 | 待畫（`exam-room`，第 11–20 集清單已有白天版） | 照第 11–20 集：窗在畫面左、門在畫面右；Brandt 坐書桌後、Nora 坐書桌前；**這集桌上只有檯燈與病歷夾的邊，診療床的簾子拉著、不入鏡，沒有任何儀器或螢幕**（審稿 ch4：提示詞寫 `no medical equipment, no screens`）。 |
| 婦產科候診區 | 待畫（`clinic-waiting`） | 照第 11–20 集：一排灰色軟椅貼牆、矮桌、診間的淺木門在畫面左。第 33 集那個織帽子的孕婦坐在離門最遠的那張。 |
| 婦產科門外的走廊 | 待畫（新增 `clinic-hallway`；**不是**七樓那條） | 二樓，候診區旁一條短走廊：淺米色的牆、木扶手、一扇窗的白天光從走廊盡頭（畫面右）進來；沒有閃燈、沒有長椅、沒有任何醫療設備。Nora 背貼左牆滑坐下去，Brandt 從畫面左（候診區那頭）走來、蹲在她右邊。 |
| 港邊當鋪 | 待畫（`pawnshop`，第 11–20 集清單） | 照第 11–20 集：門在畫面左、門上一個鈴；玻璃櫃從門口往裡延伸；老闆在櫃台後，暖黃燈。第 35 集 Nora 站櫃台前、Peg 在她**右邊**、Sparks 在她們身後靠門（第 15 集是 Peg 在左、Nora 在右；這次換邊，因為是 Nora 的戒指）。 |
| 港邊人行道（當鋪外） | 待畫（`harbor-sidewalk`） | 照第 11–20 集。第 35 集 Lyle 的照片從**對街**、長焦拍她走出當鋪門口。 |
| Ashford Construction 頂樓會議室 | 待畫（`ashford-boardroom`，要直式） | 一張很長的深色木桌，一整面落地窗對著港（窗在畫面左），沒有標誌、沒有字。Nora 坐在靠門那端（畫面右），Elias 站在桌子對面靠窗，Theo 站在桌尾（遠端）。長桌上一列：租約、保付支票、估價單（華麗鏡頭從桌面高度側拍）。 |
| Whitlock Home，Grant 的辦公室 | 待畫（新增 `whitlock-office`） | 旗艦店樓上一間白色、很亮的轉角辦公室：兩面玻璃，外面是港邊的天；一張白色大桌，桌後的矮櫃上一只奶油白的 Forever 花瓶（道具句照第 1–3 集）；冷光。Grant 站在窗前（窗在畫面右），手機的光從側面照臉。 |
| 法院走廊（Dana 的電話） | 待畫（`courthouse-hallway`，第 11–20 集清單） | 照第 11–20 集；第 34 集 Dana 站在高窗前（窗在畫面右）、卷宗夾在左腋下，右手拿手機。 |
| Kiln Row 對街（Cole 的車） | 同 `pell-ext`（白天版） | 從 Pell's 臨街窗往外拍：前景是髒的窗框與 Nora 的右肩，對街港那側的路邊停著珍珠白轎車、車頭朝畫面左，低矮的海堤與灰綠的水在它後面。 |
| 新渡輪站大廳 | 待畫（`ferry-lobby`，第 56 集 Fiona 的電話也用它；`ferry-terminal` 是第 57 集掛好吊燈的夜版，**不能用**） | 剛蓋好、還沒開放的三層樓高大廳：淺色石地板、整片玻璃牆外是港與渡輪碼頭、屋頂一大片天窗；**大廳正中天花板上一個空的鋼吊點**（一個鋼環與一段短鋼索，什麼都沒掛）；沒有人、沒有指標字。第 40 集吊點正下方擺一張摺疊報名桌，Fiona 在桌後；Cole 站在大廳另一頭的玻璃牆邊。 |
| 渡輪站專案辦公室 | 待畫（新增 `ferry-office`） | 大廳旁一間小辦公室：一張會議桌、牆上釘著幾張建築圖（線條，沒有字或虛焦）、一扇玻璃門看得到空大廳。Fiona 站著、規格夾抱在胸前；Nora 坐在會議桌邊。 |
| Doyle Sand & Batch | 待畫（`sand-supply`，要直式、白天與傍晚兩版） | Kiln Row 右邊街角轉進去：一片碎石院子、一整排木棧板上疊著素面沙袋（`plain unlabeled sand sacks`）、一台堆高機；院子後面一間鐵皮小屋：進門一張積灰的長櫃台，櫃台後牆有一扇門通往後面的小辦公室。Hank 在櫃台後；第 39 集 Grant 斜倚在**那扇辦公室門的門框**上（Hank 的左後方）；Nora 在櫃台前。從櫃台往外看，開著的門外是院子與棧板。 |

## 道具的樣子

每一鏡的英文正文**一字不差**照抄（大小用身體比）。第 1–20 集已經有的句子不改；拿在手上的照第 1–3 集〈補定〉：抄到描述為止，再接手的位置。
新道具**已加進 `cast.json`（2026-11-12 對齊）**，id 見最後一節；Remelt 裡的東西第 41–60 集照這張表的同一句。

| 道具 | 每鏡照抄的英文 | 備註 |
| --- | --- | --- |
| 三號爐 | `a huge round furnace of dark red firebrick bound with rusted steel bands, about twice as tall as a man, a steel flue rising from its dome, a round mouth at chest height behind a hinged steel door, no lettering` | 冷的時候接 `, cold and grey with dust`；蓋著時接 `, under a huge dusty grey canvas tarp`；點著以後接 `, an orange glow pouring from the gap of its half-open door`。 |
| 帆布 | `a huge dusty grey canvas tarp` | 第 31–32 集；扯下後 `…, heaped at the foot of the furnace`。 |
| 黃色安全線 | `a worn yellow safety line painted across the concrete floor` | 第 33 集起有人在爐前就寫；寫清楚人在線的哪一邊。 |
| 鋼板 | `a black steel plate on the floor in front of the furnace mouth` | 第 33–34 集練習爐前也有一塊，同一句。 |
| 小練習爐 | `a small round practice furnace on steel legs, about waist high, its mouth the size of a dinner plate glowing orange` | 第 33–34 集。 |
| 吹管 | `a long steel glassblowing pipe about as long as a person is tall` | `blowpipe`，四章同一句（2026-11-12 對齊）；沾著料接 `, a glowing orange gather of molten glass at the far end`。 |
| 掉下來的那團 | `a glob of glowing orange molten glass the size of an egg` | 第 33 集在半空；第 34 集接 `, hissing on the black steel plate in a puff of white steam, fading from orange to dark red`。 |
| 歪杯子 | `a small clear hand-blown cup about the size of her fist, leaning to one side, its rim lopsided` | 一排寫 `a row of small clear lopsided hand-blown cups on a steel shelf`；第 40 集 `…, piled in a steel bucket`。 |
| 粉筆計數 | `short white chalk strokes on the red brick, soft focus` | `chalk-tally`，右牆紅磚柱上，第 41–60 集同一句；不寫數目，Sparks 念；第 56 集新的一筆接 `, and one fresh chalk stroke set apart at the end`。 |
| 手電筒 | `a heavy old black flashlight as long as his forearm` | 第 31–32 集，Gus 右手。 |
| 掛鎖 | `a rusted padlock on a rusted hasp, about the size of her palm` | 第 31 集。 |
| 名片（回憶） | `a plain white business card, held so only its blank back shows` | 第 31 集，年輕的 Grant 右手遞出。 |
| Nora 的外套 | `a dark olive waxed-cotton work jacket, worn open` | 第 31–40 集出門時；在廠裡掛在長椅上方的釘子上。 |
| Nora 的手機 | `a plain black phone in a clear case, no logo, about the size of her palm` | `nora-own-phone`，第 111 天 Peg 替她買的預付手機，第 34–60 集同一支；亮起寫 `its screen a soft white glow, seen from the side`；第 39 集砸進桶裡後接 `, its screen cracked, lying at the bottom of an empty steel bin`。 |
| 護目鏡（Nora） | 在 `work` 外貌句裡（`clear safety goggles pushed up on her head`） | 第 34 集被拉回時寫 `her goggles knocked down onto her forehead`。 |
| 護目鏡（Sparks） | `clear wraparound safety glasses` | `sparks-glasses`，第 41–60 集同一句；在熱爐前一定戴；不用時 `…, hanging from the collar of his T-shirt`。 |
| Gus 的爐邊裝備 | `a scuffed brown leather apron` / `long tan heat-resistant gloves reaching his elbows` / `a clear face shield on a headband` | 面罩接 `, flipped up` 或 `, pulled down over his face`；在熱爐前三樣都寫。 |
| 安全帽 | `a scuffed black open-face motorbike helmet` | 第 33 集 Sparks。 |
| 機車 | `an old black motorbike with no badge, number plate out of frame` | 第 33 集起停在大門內右邊。 |
| 丁腈手套 | `blue nitrile gloves` | 第 11 集原句；第 40 集 Nora 秤料。 |
| 防塵口罩 | `a grey half-face dust respirator over her nose and mouth` | 第 40 集；推下來時 `…, pulled down under her chin`。 |
| 舊麻袋 | `old burlap sacks about the size of a pillow, tied at the neck with twine, faded and blank` | 第 40 集；一個寫 `an old burlap sack…`。打開時裡面寫 `pale grey sand`。 |
| 天平 | `a small old steel beam balance with a brass pan and sliding weights, its scale a soft pale blur` | 第 40 集，倉庫的木箱上。 |
| 鈷粉 | `a small glass jar of fine deep-blue powder` / `a small steel measuring spoon` | 第 40 集；不寫白粉、不推到粉的特寫。 |
| 鋼桶與加料鏟 | `a steel bucket` / `a long-handled steel charging shovel` | 第 40 集；第 55 集加料接 `, heaped with pale cullet`。只有 Gus、Sparks 拿。 |
| 鋼框模 | `a shallow square steel frame mould on a flat steel table` | 第 40 集，倒進去的藍玻璃寫 `molten deep blue glass`。 |
| 退火爐 | `a steel annealing oven on legs, about chest high, its door shut` | 打開時 `…, its door swung open, warm air shimmering`。 |
| 藍色樣品片 | `a flat panel of clear deep blue glass like the harbor at dawn, about the size of a large hardcover book, as thick as her little finger, a few tiny seed bubbles inside` | `blue-panel`，第 46–57 集的吊燈面板同一句；第 40 集；舉到光裡寫 `…, held up in both hands to the low morning sun`；投在牆上寫 `a patch of deep blue light sliding across the red brick`。 |
| 搬家毯 | `a grey quilted moving blanket` | 第 40 集，包著樣品片。 |
| 紙筒 | `a plain grey cardboard drawing tube as long as her arm` | 第 40 集，她左腋下。 |
| 空砂桶 | `a row of waist-high empty steel bins` | `sand-bins`，退火爐右邊；第 37 集起；踢翻寫 `…, one tipped on its side`。 |
| 舊鐘 | `an old round wall clock with a white face and plain black bar markers, no numerals, about as wide as a man's shoulders` | `wall-clock`，掛在大門上方，第 41–60 集同一句；第 39 集十二點寫 `both hands pointing straight up`；整點會敲（第 54 集十下）。 |
| 黑板與粉筆 | `an old wooden-framed blackboard about as wide as her outstretched arms, leaning on the workbench, seen edge-on` / `a stub of white chalk` | 第 37 集；寫字的鏡從黑板側邊或背後拍。 |
| 長椅 | `a long worn wooden bench against the brick wall` | Peg 的位置；第 40 集她睡在上面。 |
| Sparks 的外套 | `a worn black zip-up work jacket` | 平常掛在機車把手上；第 40 集 `…, laid over her like a blanket`。 |
| 玻璃管 | `a long clear glass tube about as long as her outstretched arms and as thick as her wrist, mounted level on the red brick wall on two plain steel brackets, a row of small plain brass bands clamped around it at even spacing, no letters` | `case-tracker`（已改句），第 36–60 集同一句；靠大門那一端開口。 |
| 珠子 | `one small amber glass bead about the size of a fingertip` | `tracker-bead`；停在第一格寫 `…, resting inside the tube against the first brass band`（第 50 集起第二格 `…, against the second brass band`）。 |
| 十二格架 | `an old steel sample rack bolted to the red brick wall below the tube, a long row of empty upright slots, each slot about the size of a hardcover book, no labels` | `evidence-rack`，第 36–50 集一直空著；第 51 集起的句子見 `cast.json`（兩片刻好的面板在最左兩格）。 |
| 梯子 | `a paint-spattered wooden stepladder taller than she is` | 第 36 集。 |
| 瓦斯閥 | `a gas valve with a red lever handle and a round dial gauge on a black pipe at knee height beside the furnace, the dial a pale blur` | `gas-valve`（2026-11-12 對齊，加上第 55–60 集要的壓力錶）；爐子右邊；第 36–37 集，第 55 集起 Elias 戴手套扳。 |
| 新接頭與扳手 | `a new brass gas fitting on a black pipe` / `a heavy steel pipe wrench as long as his forearm` | 第 37 集。 |
| 技師的工具箱與工作燈 | `a red steel toolbox` / `a portable work light on a short tripod, cold white light` | 第 36–37 集。 |
| 煙 | `thin grey-black smoke drifting under the high roof` | 第 36 集。 |
| 滅火器 | `a red fire extinguisher on a wall bracket` | 拍到爐右邊的牆就寫。 |
| Nora 的婚戒（Grant 給的） | `a polished platinum wedding ring set with one round diamond as wide as a pencil` | 第 35 集；放在櫃上接 `, lying on the glass counter`。 |
| 卡夾 | `a slim tan leather card wallet about the size of her palm` | 同第 4–10 集。 |
| 當鋪的玻璃櫃、放大鏡 | `a long glass display counter of old wristwatches, silver lockets and rings under warm light` / `a small black pocket magnifier about the size of his thumb` | 同第 11–20 集。 |
| 保付支票 | `a pale green cashier's check about the size of his hand, held so only the back shows` | 第 35 集；平放在桌上寫 `…, lying face down on the table`。 |
| 租約 | `a stapled lease of several white pages about the size of a magazine, held so only the backs or edges show` | 第 35–36 集。 |
| 估價單 | `a single pale yellow estimate sheet about the size of a magazine page, held so only its back shows` | 第 35–36 集；故意跟化驗報告（白色）分開。 |
| Nora 的筆 | `a plain black rollerball pen as long as her hand` | 同第 17 集 Dana 的筆那一句（同一款）；第 35–36 集。 |
| Elias 的手機 | `a black phone with no logo, about the size of his palm` | 同第 2 集原句。 |
| Theo 的平板 | `a slim tablet in a plain grey case, its screen turned away` | 同第 11–20 集；第 34 集「轉向她」也是這句（鏡頭在平板背後）。 |
| Dana 的卷宗 | `three thick plain buff case files held against her chest` | 同第 11–20 集；第 34 集夾在左腋下寫 `…, tucked under her left arm`。 |
| Peg 的帳本 | `a small worn brown pocket ledger about the size of her palm, a pencil tucked in its spine` | 同第 4–10 集。 |
| Peg 的鉛筆 | `a short yellow pencil as long as her finger` | 第 34 集；掉了寫 `…, lying on the concrete floor`。 |
| Peg 的帆布袋 | `a plain beige canvas tote bag with no print, hanging from her left shoulder` | 同第 1–3 集；放下寫 `…, on the bench beside her`。 |
| Peg 的無名指 | `a faint pale band of skin on her left ring finger where a ring used to be` | 同第 11–20 集。 |
| Elias 給的戒指 | `a plain narrow white-gold band with no stone, on her left ring finger` | 同第 20 集。 |
| 黑車 | `a long black luxury sedan with no badge, number plate out of frame` | `black-car`，同第 11–20 集；接 `, parked at the curb in front of the steel doors`。 |
| Grant 的車 | `a long pearl-white luxury sedan with tinted rear windows, no badge, number plate out of frame` | 同第 4–10 集；第 36 集接 `, idling at the far curb across the street, a white-gloved hand on the wheel`。 |
| Grant 的咖啡 | `a white paper coffee cup with a lid, no logo` | 第 39 集，他右手。 |
| Lyle 的照片（插鏡） | `a slightly grainy long-lens photo taken from across a harbor street: Nora in a grey henley and an open dark olive jacket stepping out of a narrow pawnshop door onto the sidewalk, head down` | 第 35 集全畫面插一格（不拍手機）。 |
| 公告 | `a single printed notice sheet held so only its back shows` | 第 38 集；壓著時 `…, lying face down on the workbench under a fist-sized lump of rough green glass`。 |
| 草圖 | `a large watercolor drawing on heavy white paper about the size of a newspaper page, many deep blue glass panels hanging in overlapping rows like falling waves, no writing` | 第 38 集；可以拍正面，不寫數目。 |
| Fiona 的規格夾 | `a thick black spec binder about the size of a hardcover book, held against her chest, nothing on its spine` | 第 38 集；`cast.json` 外貌句裡的規格夾與識別證要拿出來（見最後一節）。 |
| Fiona 的識別證與錶 | `an ID badge on a lanyard, turned toward her chest` / `a plain steel wristwatch on her left wrist, its face turned toward her` | 第 38、40 集。 |
| 報名表與日期章 | `a single white form lying on the table, far out of focus` / `a rubber date stamp coming down on the top page, the page far out of focus` | 第 40 集；日期章那句同第 19 集。 |
| Hank 的收據 | `a small pale pink carbon receipt about the size of her palm, folded so only its blank back shows` | 第 38–39 集。 |
| Hank 的手機 | `a scratched black phone with no logo, about the size of his palm` | 第 38–39 集。 |
| 素面沙袋 | `pallets stacked with plain unlabeled sand sacks` | 第 38–39 集 Doyle's 的院子。 |
| 小帽子（候診區） | `a tiny pale yellow baby hat, half-knitted on two wooden knitting needles as long as her forearm` | 第 33 集；故意不是奶油色（Nora 那頂在 Peg 那裡，觀眾不會以為是同一頂）。 |
| Gus 的小貨車 | `an old faded red pickup truck with no badge, number plate out of frame` | 第 40 集。 |
| Forever 花瓶 | `a tall cream-white hand-blown glass vase about as tall as a forearm, its body gently swelling` | 同第 1–3 集；第 35 集 Grant 辦公室的矮櫃上。 |

## 人物與參考圖

| 角色 | 參考圖 | 第 31–40 集的樣子 |
| --- | --- | --- |
| Nora | `assets/refs/nora-portrait.jpg`（r3）、`assets/refs/nora-work.jpg`（r3） | 第 31–32 集 `shoulder`（奶油色毛衣、深色長褲、短靴）加外套道具句；**第 33 集起出門 `henley`**（新：灰色亨利領長袖、深色工裝褲、工作靴、低馬尾，就是 `work` 拿掉圍裙與護目鏡）加外套道具句；在廠裡 `work`（`nora-work.jpg`）。第 40 集 08:58 是 `henley`、袖子捲到手肘（正文另寫 `a faint dusting of blue powder on her forearms`）。回憶 `nineteen`。**要畫兩張全身參考圖**：`henley`（從 `nora-work.jpg`，`latent: image1`，exactly one change：拿掉圍裙與護目鏡）、`work` 全身；**`nineteen` 要畫定妝照**（從 `nora-portrait.jpg` 改年輕、高馬尾）。原聲。一鏡都不笑。左手寫 Elias 的戒指。 |
| Elias | `assets/refs/elias-portrait.jpg` | 第 31、35、37 集：基本款（炭灰窗格紋三件式、白襯衫開領、白口袋巾），**沒有大衣**；左手在褲袋或畫框外，右手做事。`elias-furnace.jpg` 這十集不用（他不上爐）；`furnace` 的外貌句已拿掉手套與疤（第 55 集起用）。原聲。 |
| Grant | `assets/refs/grant-portrait.jpg`（平臉 r3） | 第 35、39 集：基本款（淺石色西裝、淡藍襯衫、細圓金屬框眼鏡、玻璃袖扣）；第 31 集回憶 `young`（**要畫定妝照**：25 歲、廉價灰西裝、識別證掛繩、同一副眼鏡）。說話句不寫 warm、keynote、smooth。原聲。 |
| Peg | `assets/refs/peg-portrait.jpg` | 第 34、35、37、39、40 集：`visit`（燕麥色開襟衫）；七月不穿 `coat`。眼鏡每一鏡戴在臉上；左手無名指一圈淡色皮膚。原聲。 |
| Gus Moretti | **待畫，必須最先畫** | 第 31（只有下巴與嘴）、32、33、34、36、37、39、40 集。外貌句照 `cast.json`（已拿掉疤、老花眼鏡寫 `small steel reading glasses low on his nose`）；爐邊另加皮圍裙、長手套、面罩三個道具句。70 歲、駝背、頭頂禿、兩側白髮、白色無袖汗衫、舊工作褲。原聲。 |
| Rocco "Sparks" Moretti | **待畫，必須先畫** | 第 33–40 集（第 35 集在當鋪）：基本款（平頭、小銀耳釘、黑 T 恤、灰工作褲、前臂褐色隔熱護套）；熱爐前加護目鏡道具句；第 33 集安全帽。原聲；大聲、急；可以露齒大笑的只有他（第 33、37 集）。 |
| Dr. Helen Brandt | **待畫**（第 1–3、11–20 集清單已有） | 第 33 集：基本款（白袍、深藍刷手服、銀金色短鮑伯、方框眼鏡）。原聲。 |
| Theo Park | **待畫**（第 11–20 集清單） | 第 34、35、38 集：基本款；平板道具句、寫哪隻手。原聲；面無表情。 |
| Dana Okafor | **待畫**（第 11–20 集清單） | 第 34 集（法院走廊、電話）、第 36 集（Pell's）：基本款；卷宗道具句。原聲。 |
| 當鋪老闆 | **待畫**（第 11–20 集清單，extras `pawnbroker`） | 第 35 集：同第 15 集。只說 "Eleven-eight."。原聲。 |
| Ashford 的技師 | **待畫，必須先畫**（新增 extras `ashford-tech`） | 第 37 集：38 歲墨西哥裔男性、短黑髮、修齊的小鬍子、素面深藍工作外套（沒有字）、工具腰帶。原聲（"Landlord's crew. Lease says so."）。 |
| Fiona Marsh | **待畫，必須先畫** | 第 38、40 集：40 歲華裔女性、光滑的低馬尾、白襯衫外罩深藍西裝外套；規格夾、識別證、錶用道具句。原聲。 |
| Hank Doyle | **待畫，必須先畫** | 第 38、39 集：50 歲白人男性、平頭、灰色工作夾克、指縫裡有白沙；「不看人」寫在每鏡的眼睛（不在外貌句）。原聲。 |
| Cole | **待畫**（第 1–3 集清單） | 第 36 集：只有方向盤上的白手套與黑袖口（車裡暗、看不到臉）；第 40 集：渡輪站大廳另一頭，遠、虛焦也要認得出（黑西裝、白手套、短髮）。不說話。 |
| Lyle Becker | 不畫 | 第 35 集只有他拍的照片（插鏡），他本人不入鏡。 |
| 織帽子的孕婦 | 不畫（新增 extras `waiting-mother`） | 第 33 集候診區：約 30 歲、懷孕很大、深色捲髮、寬鬆的鼠尾草綠洋裝；臉只在虛焦或側面，不說話。鏡頭重點是她的手與那頂淡黃色的小帽子。 |
| 其他砂料行老闆（電話） | 只有聲音（新增 extras `supplier-phone`） | 第 39 集：Gemini、電話濾波，從不露臉："All sold out."、最後一家 "Whitlock Home's our biggest client." "Portland's got it. Opens at eight."。 |
| Claire Quinn | — | 這十集不入鏡（見〈要站主決定的〉第 4 條）。第 40 集那句是 Nora 自己念。 |
| Rosa、Walter、Victor Crane、Sienna、Fisk、Reyes | — | 這十集不出現。Reyes 只在台詞裡（第 34 集）；Rosa's 只在第 31 集的街角背景、關著。 |
| Soot（回憶） | 不畫臉 | 第 34 集回憶只有一隻滿是煤灰的**右手**與前臂，抓住十九歲 Nora 圍裙的肩帶往後拉（`elias` 的 `soot` 外貌句寫的是左手的繃帶，這鏡不用那一句）。 |

**同框撞臉**（一鏡最多三張有名字的臉）：

- **Gus 與 Peg**（都六、七十歲、都戴眼鏡）：第 37 集 Peg 抓他的肩會同框，可以，寫清楚分得開的地方：Gus 男、駝背、禿頂、白色無袖汗衫外罩皮圍裙、老花眼鏡低在鼻樑上；Peg 女、直的短灰髮往一邊梳、玳瑁框、燕麥色開襟衫、木珠項鍊。
- **Sparks 與 Hank**（都是平頭）：不同框（第 38–39 集 Sparks 在 Remelt、Hank 在 Doyle's）。**Sparks 與 Cole**：第 36 集 Cole 只有手；第 40 集渡輪站 Sparks 在小貨車上（不進大廳）。
- **Grant 與 Elias**（細圓金屬框 vs 細銀絲框、都穿灰西裝）：這十集不同場（第 35 集一個在辦公室、一個在會議室，交叉剪接；第 39 集 Elias 不在）。
- **Theo、Gus、Peg、Elias、Grant、Brandt 都戴眼鏡**：每鏡寫清楚是哪一副（Theo 圓玳瑁框、Gus 小鋼框老花低在鼻樑、Peg 玳瑁框、Elias 細銀絲框、Grant 細圓金屬框、Brandt 方框）。
- **Fiona 與 Dana**：不同集同場（Dana 在第 34、36 集，Fiona 在第 38、40 集）。
- **年輕的 Grant 與年輕的 Nora**（第 31 集回憶）：同框一鏡就好，其餘正反打；年輕 Grant 的臉要跟現在的 Grant 認得出是同一人（同一副眼鏡、同樣的側分沙金髮），這是定妝照要驗的。
- 第 37、40 集人最多（Nora、Gus、Sparks、Peg，加第 37 集的技師與門外的 Elias）：交代位置的全景用背影與爐光的剪影，臉的鏡一鏡一到兩人。

**先畫順序**（台詞在畫面上、用原聲的人最先，照第一次出場排）：
1. Gus → 2. Nora `nineteen` → 3. Grant `young` → 4. Sparks → 5. Nora `henley`（全身）→ 6. Nora `work`（全身）→ 7. Ashford 的技師 → 8. Fiona → 9. Hank；
Dr. Brandt、Theo、Dana、當鋪老闆、Cole 在第 1–20 集的清單裡，若還沒畫，Brandt 排在 5 之前、Theo 與 Dana 排在 6 之後、Cole 排在 9 之後。
場景：10. Kiln Row 直式清晨版（含 Claire Quinn Glass）→ 11. Pell's 主廠房冷的版本（`remelt-cold` 直式，帆布蓋著爐子）→ 12. Pell's 門口回憶版 → 13. 婦產科門外走廊 → 14. 主廠房（`remelt`，白天與夜、點爐前後）→ 15. 倉庫 → 16. 頂樓會議室直式 → 17. Grant 的辦公室 → 18. 渡輪站大廳（空、吊點）→ 19. 渡輪站專案辦公室 → 20. Doyle's 院子與櫃台（白天、傍晚）。
道具若要參考圖：先畫三號爐（冷、蓋帆布、點著三種）、玻璃管加珠子加十二格架（一張）、藍色樣品片（顏色要整章一致，也是第 46、57 集的吊燈色）。

## 細綱必修（每集一行）

- **第 31 集**：開場 10 秒四鏡：副駕駛座的門從裡面被推開（手與車門、清晨的街）→ Nora 下車回頭吼 "You stood there!"（短喊，原文寫進說話句）→ 她轉身、腳步停住、抬頭（剪在轉身一半）→ 從她腳下往上仰拍那扇鏽紅的雙開鐵門與認不出字的招牌，她低聲 "Pell's."。
  吵架隔著車頂、Elias 不看她（眼睛看畫面左外的街角）；"Dana's filing…" 改成未來式（見〈細綱自相矛盾〉）；Elias 那四句錢的話一句一鏡、在他自己的鏡上。回憶照〈全劇固定〉：溫暖偏金、Grant 練過的閉嘴微笑、她十九歲不笑、名片只拍背面；回憶進出用同一扇門的對剪（現在的鏽門 → 十二年前的乾淨門 → 現在）。
  招牌與 Claire 的店名**不上後製字**，"Pell's." "Mom's studio." 念出來；搖鎖兩下就放手（不拍手受傷）。懸念的 "Who's there?" 照〈細綱自相矛盾〉：只見手電筒、右手與被漏光照到的下巴與嘴，原聲。華麗鏡頭：她在鐵門下，海風吹起齊肩的髮，眼睛還紅。
- **第 32 集**：開場 10 秒四鏡：光束放低、落到地上 → Gus 的臉（駝背、汗衫、老花眼鏡）看她 → 她的臉（瞇眼、灰塵在光裡）→ Gus "You're the girl from the courthouse steps."。
  崩潰照審稿演滿："I was nineteen. They laughed at me." 之後她哭出聲（哭的鏡 4–5 秒，不切碎）；Gus 本來轉身要走，停、回頭 "I didn't laugh. I was there."（他自己的鏡）。"New owner pays the power. Never met him." 之後插一鏡他的眼睛越過她看門外的黑車（車停在門外、Elias 在駕駛座講電話、看不清臉），多停一拍（第 60 集回收）。
  扯帆布：他拉一角的繩子，帆布整片滑下、灰塵像雪（不寫慢動作，寫「灰塵在光柱裡往下落」）；手掌貼磚是華麗鏡頭：`her right palm flat on the cold brick`、淚痕、頭髮垂在臉邊、閉眼一拍。細綱的「手腕內側細燙痕」刪掉（審稿）。
- **第 33 集**：開場 10 秒四鏡：她的兩隻手掌平放在膝上（插鏡，跟上一集貼磚的手跳接）→ Brandt "Your body's still healing." → Brandt "No heat, no fumes, no heavy lifting. Six months." → Nora 看著手 "So ten more weeks."。
  診間與走廊**只拍人、桌、牆**，提示詞寫 `no medical equipment, no screens`；Brandt 不碰她、不做任何檢查。候診區一鏡：孕婦的手織淡黃色小帽（插鏡），Nora 的眼睛停在帽子上；走廊：她背貼牆滑坐、哭出聲（4–5 秒），Brandt 蹲在她右邊、一隻手放在自己膝上、不說話（兩人同框中景）。
  Pell's：機車進門要戴安全帽、停好才摘；"Grandpa! Who's this?" 時他露齒笑。第一個杯子塌掉的「啵」用音效；"One!" 時他在磚柱上畫一筆（粉筆計數那句）。她在黃線外喊口令（兩三句短的：`"Turn. Keep turning."`、`"Breathe. Short."`，原聲），華麗鏡頭：護目鏡推在頭頂、圍裙綁緊、爐光在眼裡。
  懸念照審稿：她**自己越線**（左腳跨過黃線一步）去扳他的手，他一慌甩太快，那團玻璃滑下管口——剪在半空，下一集才落地。
- **第 34 集**：開場 10 秒四鏡：Gus 戴手套的手揪住她後衣領往後拽 → 那團玻璃落在鋼板上、嘶一聲冒白煙（離她靴尖一臂遠）→ Gus（面罩推在頭頂）"Behind the line! You want to lose your feet?" → 她的臉，護目鏡被撞落到額頭，喘。
  閃回兩秒：十九歲的她、一隻滿是煤灰的**右手**抓住她圍裙肩帶往後拉（暖金光，沒有臉、沒有左手、不拍那團玻璃落在哪）；"Somebody pulled me back before." 之後 Gus 一鏡：嘴閉著、眼睛移開、轉身去關練習爐的門。
  跳一天不用字卡：光變成傍晚、Peg 第一次出現在長椅上、架上一整排歪杯子、粉筆一片（"Twenty!"）。Peg 那兩句寫在她自己的鏡上、頭不抬、鉛筆在動。
  Dana 的電話兩頭剪接（她在法院走廊、原聲）；"Same Reyes who said half a pill wasn't enough?" 寫成 Nora 的一口氣。Theo：她要照第二條付市價（補一句 Nora："Market rent. Clause two."，選用），所以他來報數；平板轉向她時鏡頭在平板背後。懸念：Peg 從她肩後看、倒抽一口氣、**鉛筆**掉在水泥地上（插鏡，鉛筆彈一下）。
- **第 35 集**：開場 10 秒四鏡：戒指放上玻璃、她的手指按著不鬆（插鏡）→ Peg 的食指把戒指推過去 "I pawned mine so you'd keep yours." → Peg "Now sell it." → Nora "Sell. Not pawn."；接著老闆放大鏡 "Eleven-eight."、Sparks "That's a month?"（他的鏡，嘴張大，不笑）。
  會議室：保付支票從她外套內袋拿出來放上桌；"Clause two. I pay for my own doors." 與 "His ring. My furnace." 各一鏡；她簽租約的最後一筆往外一挑（只拍筆尖與紙邊；細綱的華麗鏡頭：像拉玻璃棒），臉寫 `lips pressed together, corners level, chin lifted`、不笑。Elias **站著**右手簽、左手在褲袋。
  Grant 的辦公室：照片是全畫面插鏡（不拍手機）；他念圖說（原聲），練過的閉嘴笑在念完那一刻掉下來（兩個部位：嘴角落下、下巴收緊）。估價單：她拿出來是因為燃燒器壞了、她付不起；Elias 先說 "Repairs are the landlord's. It's in the lease."（補的台詞），再說 "The furnace is mine. The fire's yours."；懸念照審稿只停在她不簽。
- **第 36 集**：開場 10 秒四鏡：Dana 的食指在租約那頁點兩下（側拍、紙邊）→ Dana "Landlord fixes his own furnace." → Dana "That's not fighting for you. Clause two holds." → Nora 在工作台上簽估價單（筆尖在紙邊）。
  掛管子是華麗鏡頭：她在梯子上、袖子捲到手肘、護目鏡在頭頂，回頭答 Sparks 時頭髮一甩；梯子 Sparks 扶著。六個階段她念一次（在梯子上，一口氣），珠子「叮」停在第一格她再念 "Report."（珠子的插鏡從管子側面平拍）。十二格架那三句照細綱。
  Cole：她在臨街窗前（從窗內往外拍，見〈場景格局〉），白車、白手套；"That's Cole. Grant's driver." 寫她自己的鏡。深夜試爐：Gus 先叫所有人到大門口（"Everybody at the door."，補的台詞），Nora 不在線內；回火一秒、黑煙浮在屋頂下、Gus 戴面罩扳閥 "It backfired. Line's shot."（審稿把 flashback 改 backfire）。
- **第 37 集**：開場 10 秒四鏡：技師的手把扳手收進紅色工具箱（插鏡）→ 技師 "Landlord's crew. Lease says so." → Gus 從他手裡接過扳手 → Gus 轉最後一圈 "Again."。
  點爐：Gus 戴手套與面罩點火、Sparks 開閥，Nora 與 Peg 在黃線外；「轟」一聲後橘光從爐口淹過每一張臉、紅磚、玻璃管與空架（華麗鏡頭：她額頭上的護目鏡反著火光、熱氣把頭髮吹起、兩頰被熱氣烘紅，不笑）。
  Gus 哭照〈細綱自相矛盾〉：爐門推到一道縫、退兩步跪在黃線上，"Walter. She's lit. You hear me? She's lit." 哭出聲（4–5 秒）；Peg 走過去抓住他的肩，她自己的臉在下一鏡哭。黑板那個字從側邊拍；"Great name!" Sparks 露齒笑；Peg "Inside voice." 一邊擦眼睛。
  懸念：她轉身，從她右肩後拍大門：Elias 在門外的霧裡逆光、左手在褲袋，看她一拍、轉身走；他不進門、不說話。
- **第 38 集**：開場 10 秒四鏡：工作台上壓著的公告（綠玻璃塊，插鏡）→ 門口的 Theo "Boss said leave it here."（平板抱在胸前，說完就走）→ 她拿起公告（紙背朝鏡頭）→ 她念 "Ferry terminal chandelier. Blind competition. No names."。
  Fiona 三句照〈細綱自相矛盾〉改成 "Nine a.m., eleven days from today."；空大廳的華麗鏡頭：她抬頭看吊點，天窗的光落在她仰起的臉上，齊肩髮、工作外套。草圖可以拍正面（水彩、沒有字）；"How blue?" "The harbor. Right at dawn."。
  Doyle's：她說 "Twenty bags."（補）；Hank 收現金時嘴角一提（閉嘴）、眼睛不看她；"Truck's Thursday."；懸念：她走出去、他打電話，**只拍 Hank 這頭**，Grant 的聲音不出現。
- **第 39 集**：開場 10 秒四鏡（蒙太奇，每格換光）：Hank 在櫃台講電話 "Thursday."（早上）→ Nora 在 Remelt 工作台邊聽、下巴繃緊（下午）→ Hank "Monday, swear."（另一天）→ 第 126 天晚上 Hank "Out of stock."。之後 "Then refund me." "Store credit." 與「喀」。
  一家一家打：Nora 的鏡嘴不動或嘴不入鏡、電話那頭是 Gemini（`supplier-phone`）；最後一家那兩句在她的臉上（她在聽），"I'm due at nine." 是她的原聲鏡。
  Doyle's：Grant 斜倚門框、咖啡在右手、閉嘴微笑 "Need sand, Nor? Just ask."（他自己的鏡）；她把收據拍在櫃台上 "Keep your credit."（補，選用），轉身就走、不回頭。Hank 整場眼睛看櫃台。
  回 Remelt：砸手機一鏡（手機進桶的插鏡）、吼的鏡寫 `screaming, no words` 對著爐子（4 秒），Peg 坐在長椅上不起身 "Let it out, honey."；華麗鏡頭：她背靠紅磚坐在空桶邊、聲音啞了、爐火在臉上跳、淚痕，不笑。午夜：Sparks 踢桶、鐘的兩根針重合（插鏡，沒有數字）。細綱裡 "won't quite look her in the voice" 不用。
- **第 40 集**：開場 10 秒四鏡：Sparks 提起裝歪杯子的鋼桶 → 倒上加料鏟、推進爐口 "Remelt, right?"（他戴護目鏡與手套）→ Gus "Not enough for a panel." → Gus 推開倉庫的門、拖出第一個麻袋。
  "Pell's batch. I still remember the recipe."；（選用）Sparks "Is that ours?" Gus "Came with the lease."；她綁口罩、捲袖子 "Then we mix our own."；倉庫裡跪在天平前（華麗鏡頭：口罩、捲起的袖子、前臂一層藍粉、從門縫進來的爐光照著專注的側臉），鈷粉一匙一匙、Gus 念一行、她改 "Cobalt. Two grams less."。
  加料與澆模是 Gus 與 Sparks（全套防護）；她站在倉庫門檻上喊。四點：Peg 抱著帳本睡、Sparks 蓋外套、踮腳回去（一鏡兩個動作就好）。日出：退火爐門打開、她舉起那片藍到大門的光裡，藍光滑過紅磚、玻璃管與空架（審稿：是一塊藍光，不是整面牆變藍）；"Glass cools slowly. So do people." 她自己低聲念、原聲，不拍 Claire。
  送件：08:15 小貨車一鏡（或不拍），08:58 她抱著搬家毯衝進大廳（`clear deep blue` 在天窗光裡）；Fiona 看錶、蓋章 "Entry nine. Just made it."（補 "Entry nine."，第 41 集要用）；最後一鏡大廳另一頭的 Cole 舉起手機，遠、虛焦也認得出白手套。這是第四章結尾，140 秒。

## 伏筆與回收

| 伏筆 | 埋在 | 收在 | 這十集裡的寫法 |
| --- | --- | --- | --- |
| Elias 為什麼買下 Pell's、他是誰（m08） | 31 | 第三季 | 31 "Bought it at a sheriff's sale."；32 Gus 看黑車多停一拍；37 他知道今晚點爐、站在門外不進來 |
| 檢察官會不會受理偽造案（s01-t31） | 31 | 34 | 31 "Dana's filing the forgery report this morning."；34 "Reyes will review it." "Same Reyes. Different evidence."；36 珠子停在 Report |
| Gus 為什麼守了十二年 | 32 | 第三季（第 54–56 集起） | 32 "I was there." "New owner pays the power. Never met him."；37 "Walter. She's lit." |
| 三號爐點不點得著（s01-t25） | 32 | 37 | 32 "Nobody's lit her in twelve years."；36 回火；37 點著 |
| Sparks 什麼時候吹得直（s01-t26） | 33 | 56 | 33 "Crooked." "One!"；34 "Twenty!"；40 歪杯子回爐 "Remelt, right?" |
| 熱爐禁令 | 33 | 第二季 | 33 "Six months." "So ten more weeks."；34 被拉回；40 她只秤料、不碰爐 |
| 是誰把她拉回來的（m12） | 34 | 第五季 | 34 閃回一隻煤灰的右手、"Somebody pulled me back before."，Gus 不說 |
| 付不付得起市價租金（s01-t27） | 34 | 35 | 34 "Eleven thousand a month."、鉛筆掉地；35 "Eleven-eight." "That's a month?" "I pay for my own doors." |
| Nora 的婚戒 "It'll come in handy."（第 15 集） | 15 | 35 | 35 "I pawned mine so you'd keep yours." "Now sell it." |
| 修爐算不算替她出頭（第二條） | 35 | 36 | 35 "The furnace is mine. The fire's yours." "Not until my lawyer reads it."；36 "Clause two holds." |
| 工作室叫什麼（s01-t28） | 35 | 37 | 37 "Remelt. Anything we ruin goes back in."；40 "Remelt, right?" |
| Grant 回到戲裡 | 35 | 39 | 35 看到當鋪照片、笑掉下來；36 Cole 守著 Kiln Row；38 Hank 打給他；39 本人 "Need sand, Nor? Just ask." |
| 追蹤管與十二格架 | 36 | 49–51、60 | 36 珠子停 Report、架上全空；37、40 光照過管子與空架 |
| 渡輪站盲審（s01-t29） | 38 | 46 | 38 "No names."；40 "Entry nine. Just made it." |
| 砂從哪裡來（s01-t30） | 39 | 40 | 39 "Store credit." "Portland … Opens at eight."；40 Pell's 的舊料 |
| Cole 的那通電話 | 40 | 第五章 | 40 他看見那片藍、舉起手機 |
| 母親的話 | 40 | 第四季（玻璃磚裡的紙條） | 40 "Glass cools slowly. So do people." |
| Nora 什麼時候笑（s01-t18） | 21 | 45 | 31–40 一鏡都不笑 |
| Elias 的左手（s01-t15） | 16 | 60 | 31、35、37 每一鏡寫左手在哪 |

**第 41 集要接的**（2026-11-12 對齊，第 41–50 集 bible 照這段寫）：第 128 天（7/22 週三），Remelt；三號爐點著第 13 天；追蹤管的珠子在 Report；十二格架 0/12；渡輪站的件是「九號」（"Entry nine."），結果約兩週後（約第 141 天，s01-t29 第 46 集收）；那片藍玻璃在渡輪站，不在廠裡；Cole 已經打電話給 Grant（第五章用）。
倉庫裡還剩兩袋 Pell's 的舊料；Doyle's 欠她 $640 的店內抵用（不回收）；Nora 身上只剩幾塊錢、帳本 Nora 欄欠 Peg 約 $330；Peg 約 $930（下一筆退休金第 138 天）；Gus 與 Sparks 的工錢欠著；**下個月房租第 142 天到期**；Peg 的當票第 128 天要續（$40，Peg 付，選用一句帳）；Nora 的手機她從砂桶撿回來了（裂了、還能用）。
第 41 集的燈箱：倉庫那台舊描圖燈箱搬到工作台靠爐子那頭（`light-box`）；兩張影本 Dana 帶來、婚前草圖資料夾 Nora 從 Ashford 家帶來。熱爐禁令還在（到第 186 天）。Elias 最後一次露面是第 37 集；Dana、Sparks 在第 41 集。

## 每集鏡數目標

照種田拍法：沒有台詞的鏡 2–3 秒、剪在動作中間；說話的鏡照台詞長度（英文每秒約 2.5 字，加動作與 0.5 秒），原聲鏡買 6 秒、剪到台詞長度；開場 10 秒至少四鏡（各集的四鏡見〈細綱必修〉）；超過 6 秒標「長鏡」。

| 集 | 細綱秒數 | 台詞約 | 說話的鏡約 | 目標鏡數 | 備註 |
| --- | --- | --- | --- | --- | --- |
| 31 | 125 | 75 字 | 16 | 41–45 | 三個時空（街、回憶、廠內）；回憶 3–4 鏡；吵架隔著車頂正反打 |
| 32 | 120 | 50 字 | 10 | 40–44 | 一個地方；哭的鏡與扯帆布有幾鏡 4–5 秒，不切碎 |
| 33 | 115 | 50 字 | 13 | 39–43 | 四個地方（診間、候診區、走廊、Pell's）；走廊哭 4–5 秒 |
| 34 | 120 | 60 字 | 13 | 40–44 | 跳一天；電話兩頭交叉剪；閃回 2 秒 |
| 35 | 120 | 65 字 | 14 | 39–43 | 三個地方（當鋪、會議室、Grant 辦公室）交叉剪；照片插鏡 2 秒 |
| 36 | 125 | 55 字 | 13 | 42–46 | 三段時間；掛管子的動作鏡多；回火 2 鏡、各 2 秒 |
| 37 | 130 | 25 字 | 7 | 46–50 | 台詞最少、動作與光最多；點爐那一刻與 Gus 哭各 4 秒；Elias 在門外的鏡留 3 秒 |
| 38 | 120 | 55 字 | 11 | 41–45 | 四個地方（Remelt、專案辦公室、大廳、Doyle's）；大廳顏值鏡 3 秒 |
| 39 | 120 | 60 字 | 14 | 40–44 | 蒙太奇四鏡各 2 秒；電話多；吼的鏡 4 秒 |
| 40 | 140 | 45 字 | 10 | 49–53 | 章結尾；夜裡四段、日出、送件；藍光那一鏡 3–4 秒 |

## 要站主決定的

（2026-11-12 起彙整在 `s1-decisions-e021-e060.md`，與其他三章的同類問題合併；這裡保留原文與理由。）

1. **錢**：戒指賣 **$11,800**（老闆念 "Eleven-eight."），保付支票付第一個月 $11,000、還 Peg 砂錢 $128、二十袋砂 $640，**Nora 這章淨增 $32**（剛好一袋，就是細綱「最後的錢」）。
   租約按月、全包（含水電瓦斯）、含設備與存料、修繕歸房東，條款都不念。**建議照這份**：一枚鑽戒剛好換一個月，"That's a month?" 才好笑也才痛；數字只在 "Eleven-eight."、"Eleven thousand a month."、"thirty-two bucks a bag" 三處說出口。開頭的餘額（Peg 約 $1,403、Nora 約 $26）與通勤（公車一人 $2）已在章界對齊時接上第 21–30 集的帳。
2. **第 36 集 Cole 的車**：細綱寫黑色轎車。**建議改成 Grant 的珍珠白轎車**：第 10–20 集的黑車是 Elias 的，再來一輛黑車觀眾會以為 Elias 回來守著；白車加白手套，Nora 一眼認得。另一個做法是照細綱用黑車，但要另畫一輛跟 Elias 的分得開的車（多一個道具）。
3. **可讀的字一律不上後製**：細綱與審稿 ch4 都說「後製上字」（Pell's 招牌、Claire 的店名、管子上的六個階段、黑板上的 Remelt、公告）。**建議全部念出來、後製也不上**：
   跟第 4–10 集的簽名、第 11–20 集的化驗報告一樣（那兩章已經把 "added in post" 全部取消），三種語言的字幕與縮圖也不用另做字卡；六個階段由 Nora 掛管子時念一次。
4. **第 40 集 Claire 的回憶**：細綱角色欄列了 Claire，但只有一句話。**建議不拍 Claire**，那句由 Nora 自己低聲念：Claire 要多畫一張定妝照，她的外貌句還寫了指尖的燙痕（試鏡會畫成紅點）；而且日出舉起藍玻璃那一鏡留給 Nora 一個人比較有力。
   要拍的話，只拍一鏡兩秒：Claire 的手（沒有燙痕）把一片玻璃放進退火爐、她的聲音（Gemini Vindemiatrix，回憶的畫外）。
5. **Gus 的疤**：外貌句寫兩條前臂與手上滿是舊燙疤，試鏡證明細的疤會畫成紅點與傷口。**建議外貌句改成 `weathered sun-spotted forearms and thick-knuckled hands`、不寫疤**；他的十二年用台詞與眼睛交代。不改的話，每鏡要寫 `faint flat pale patches, no redness`，而且要先試一張。
6. **細綱沒有、這份補上或改掉的台詞**：第 31 集 "Dana's filing the forgery report this morning." "With the police. It goes to the prosecutor."（改時態）；第 33 集 Nora 喊的口令 "Turn. Keep turning." "Breathe. Short."；
   第 34 集（選用）Nora "Market rent. Clause two."；第 35 集老闆 "Eleven-eight."、Elias "Repairs are the landlord's. It's in the lease."、（選用）Peg "Sand. Paid back."；第 36 集 Nora 念六個階段、Gus "Everybody at the door."；
   第 38 集 Fiona "Nine a.m., eleven days from today."（取代 "the tenth"）、第 34 集 Peg "Twenty cups. Two days."（取代 "Three days."，第 33 集挪到第 112 天的結果）、Nora "Twenty bags."；第 39 集（選用）Nora "Keep your credit."；第 40 集（選用）Sparks "Is that ours?" Gus "Came with the lease."、（選用）Gus "Short soak. She'll hold."、Fiona "Entry nine."。建議照收：都是補漏洞或讓動作看得懂；"Came with the lease." 守住第二條，建議收。
7. **Nora 的新造型 `henley`**：第 33 集起出門穿（`work` 拿掉圍裙與護目鏡），工作外套是道具。建議收：從 `nora-work.jpg` 只改一處就畫得出來，跟第 31–32 集的奶油色毛衣分開，看得出「她回去工作了」。
8. **回憶要兩張新定妝照**（Nora `nineteen`、Grant `young`，審稿 ch4 第 31 集）：第 31 集回憶兩人露臉、Grant 說話。**建議畫**：這兩張之後的回憶（第 34 集、第 52 集以後、第三季）還會用；第 34 集的回憶只用 `nineteen` 與一隻手。
9. **日曆**（2026-11-12 對齊時已照做）：季細綱的第 110 天是 7/4 週六（國慶），婦產科不開；第 117 天是週六，渡輪站辦公室不開。已把第 33 集挪到第 112 天（週一）、第 34–36 集跟著排、第 38 集挪到第 116 天（週五），點爐（第 116 天）與截止（第 127 天）不動；跟著改兩句台詞（"Twenty cups. Two days."、"Nine a.m., eleven days from today."）。**建議照這樣**；台詞照細綱的話，得讓 Sparks 的第一天落在第 110–111 天的連假（站主另給理由）。
10. **三號爐的樣子**：`set-remelt.jpg` 的爐子是圓鋼殼、爐上有可讀的 "Number Three"，桌上還有一個有字的框，又是橫式；細綱寫「兩個人高的磚爐」。**建議照這份重畫直式**（深紅耐火磚圓頂、鏽鋼帶、沒有字），`set-remelt.jpg` 只當色調與材質的參考。
11. **候診區那頂帽子的顏色**：細綱 "a tiny hat, like the one Nora never finished"。**建議淡黃色**（形狀一樣、顏色不同）：Nora 那頂奶油色的在 Peg 那裡，同色會讓觀眾以為是同一頂。

## 寫稿時補定的事

（寫分鏡時發現、定下來的事寫在這裡，照第 11–20 集 bible 的格式；寫稿者補。）

## 要加進 cast.json 的

**已加進 cast.json（2026-11-12 對齊）**，英文跟上面一字不差；跟其他三章重複的東西只留一個 id（括號裡是對齊時改的地方）。

- **造型**：`nora` 新增 `henley`（從 `nora-work.jpg`，exactly one change：拿掉圍裙與頭上的護目鏡）；`work` 的袖子改成 `a grey henley with long sleeves`（`nora-work.jpg` 的袖子放到手腕，捲袖寫在鏡上；護目鏡留在句子裡，跟參考圖一致）；notes 寫進第 21–60 集的造型。`elias` 的 `furnace` 改成第 51–60 集 bible 的句子（拿掉手套與疤）。
- **角色的修正**：`gus`（拿掉燙疤、老花眼鏡寫位置；站主第 5 條待確認）、`claire`（拿掉指尖燙痕）、`hank`（拿掉 avoids eye contact）、`fiona`（拿掉識別證與規格夾，改道具 `fiona-badge`、`fiona-binder`、`fiona-watch`）、`cole`（拿掉 eyes down，`s1_episodes` 補到 57）、`grant`、`sparks`、`fiona` 的 `s1_episodes`。
- **路人**：新增 `ashford-tech`、`waiting-mother`、`supplier-phone`（Gemini Algenib；Gus 在畫面上用原聲，這個名字只是他的備案）。
- **場景**：`pell-ext` 改成直式、不寫時間（原稿的 `kiln-row-dawn` 併進來，清晨寫在鏡上）；`remelt` 改成〈場景格局〉那一格（原稿的 `remelt-ch4` 併進來，第 36–60 集同一個 id）；`remelt-cold` 改句（拿掉地上的砂袋、換成三號爐）；`sand-supply` 改句；新增 `pell-door-flashback`、`pell-storeroom`（舊燈箱桌改成舊描圖燈箱）、`clinic-hallway`、`whitlock-office`、`ferry-lobby`、`ferry-office`。原稿的 `claire-studio-door` 不另立，從 `pell-ext` 取景。
- **道具**：新增 `furnace-no3`、`furnace-tarp`、`safety-line`、`steel-plate`、`practice-furnace`、`hot-glob`、`crooked-cup`、`chalk-tally`、`gus-flashlight`、`claire-padlock`、`young-grant-card`、`nora-jacket`、`nora-own-phone`、`sparks-glasses`、`gus-apron`、`gus-gloves`、`gus-face-shield`、`sparks-helmet`、`sparks-motorbike`、`dust-respirator`、`pell-batch-sacks`、`beam-balance`、`cobalt-jar`、`measuring-spoon`、`steel-bucket`、`charging-shovel`、`casting-mould`、`annealer`、`blue-panel`、`moving-blanket`、`drawing-tube`、`sand-bins`、`wall-clock`、`blackboard`、`chalk-stub`、`long-bench`、`sparks-jacket`、`tracker-bead`、`evidence-rack`、`stepladder`、`gas-valve`、`gas-fitting`、`pipe-wrench`、`tech-toolbox`、`tripod-work-light`、`smoke`、`fire-extinguisher`、`cashiers-check`、`lease`、`burner-estimate`、`grant-coffee`、`lyle-photo`、`ferry-notice`、`chandelier-sketch`、`fiona-binder`、`fiona-badge`、`fiona-watch`、`entry-form`、`date-stamp`、`hank-receipt`、`hank-phone`、`sand-pallets`、`waiting-hat`、`gus-pickup`。
  改：`case-tracker` → 玻璃管那一句（銅環、沒有字、水平；珠子另立 `tracker-bead`，琥珀色）；`blowpipe` → 四章同一句；`nora-ring` 的 note。原稿的 `elias-heat-gloves` 用第 51–60 集的 `heat-gloves`。
- `set-remelt.jpg` 只當色調參考（〈要站主決定的〉第 10 條）；`ferry-terminal` 改成第 57 集的夜版，第 38、40、56 集用 `ferry-lobby`。

## 寫稿時補定的事（2026-11-12）

- **第 34–35 集**（寫稿者定）：Gus 在爐邊戴長隔熱手套（第 33 集最後一鏡起）；Sparks 在爐邊也戴一副，道具句 `a pair of long grey heat-resistant gloves reaching to the elbow`（已加進 `cast.json`）。練習爐有一扇小鐵門；Nora 的手機放在圍裙前袋；
  Peg 的帳本與鉛筆分開寫兩句（鉛筆在手上時帳本句只寫到 `about the size of her palm`）。第 35 集補一鏡從對街長焦拍她低頭走出當鋪（晴天的 `harbor-sidewalk`），就是 Lyle 那張照片的角度，c26 的照片從這鏡截一格。
  當鋪老闆用一小塊黑絨布包走戒指；支票、筆與對摺的估價單放在 Nora 外套內袋；Peg 用左手食指推戒指。**Peg 站在 Nora 右邊**（第 15 集分鏡就是這樣；本 bible 若有寫左邊的地方以這條為準）。
  寫稿者新加、站主 2026-11-12 照建議定案：第 34 集 c24 Dana 句前 "Prosecutor's office called."（Reyes 的名字沒人說過）；第 35 集 c09 "One month. It's enough."、c31 "Number Three's burner is shot. I can't cover it."。
- **第 39–40 集**（寫稿者定）：39→40 Nora 坐在**黃線外的右牆根**（不是黃線內的空砂桶旁）；Sparks 在第 39 集 23:50 就把歪杯子掃進鋼桶，第 40 集 c01 直接提起那個桶。
  Remelt 的黃線在倉庫門前留一條一人寬的通道（倉庫門在黃線靠爐子那側）。第 39 集照時間線放兩聲 "Thursday."，蒙太奇五鏡；Nora 整集穿 `work`，收據從掛在牆上的外套口袋拿；供應商電話三句用 Gemini（`supplier-phone`），那幾鏡 Nora 的嘴不入鏡。
  藍色鈷粉寫 "even dusting"（避免畫成瘀青，第一批草稿先看）。第 40 集台詞照 bible："Pell's batch. I still remember the recipe."（outline 原句是 "I still remember the Pell recipe."）。
  寫稿者新加、站主 2026-11-12 照建議定案：Gus "Walter's blue. Cobalt, twelve grams."、Nora "Third charge! Now!"；選用句 "Keep your credit." 收進第 39 集。
- **第 31–33 集**（寫稿者定）：吵架隔著車頂，鏡頭守在車頭那一側；Elias 用**右手**從西裝內袋拿手機（`cast.json` 的 `elias-phone` note 已改）。她推開的是從街上看的左扇鐵門；手電筒放在工作台靠爐子那一端。
  帆布一角綁一條舊繩 `a frayed rope tied to one corner of the tarp`，扯下後堆在爐腳，第 33 集起收進倉庫、不入鏡。第 33 集："Huh?" 的回答是 Nora 遞一根冷的吹管給 Sparks；長凳、滾料台、還熱著的杯子另有英文句；第一筆粉筆 `a single short white chalk stroke…`。
  Sparks 在線外拿冷吹管時不戴手套，在爐邊每一鏡都戴。鞋：Gus 舊的棕色工作靴、`nineteen` 的 Nora 工作靴、Brandt 白色軟底鞋、Sparks 黑色工作靴。回憶的廂型車 `a plain old white van with no lettering`。
- **第 36–38 集**（寫稿者定）：**Peg 03:30 怎麼到 Remelt**：約 03:00 Elias 從 Ashford 家自己開車載 Peg 一個人下山，車停在 Rosa's 那個街角，他留在車裡；不拍、Peg 也不提。Nora、Gus、Sparks 回火後整夜沒走；Gus 打報修電話，技師約 01:00 到；大門整夜開著散煙。
  道具句：螺絲起子 `a plain wooden-handled screwdriver as long as her hand`；點火鈕 `a round red push button on a small black steel box on the side of the furnace, just above the valve`。第 37 集技師把扳手移到工具箱上方，Gus 從那裡拿走。
  **`remelt` 場景圖要多畫一版左牆還沒掛玻璃管的**（第 36 集掛管以前），或那段鏡頭背對左牆。十二格架由 Gus 與 Sparks 抬；黑板靠在工作台靠爐子那頭的左側；Hank 的電話不加濾波（他在自己店裡露臉）；第 38 集沒人叫 Fiona 的名字。
  寫稿者新加、站主 2026-11-12 照建議定案：第 36 集 c25 Sparks "That white car's been there all afternoon."；第 38 集 c10 Nora "You really don't look at names?"。

## 審稿後補定（2026-11-12，`../review/2026-11-12-e031-e035-storyboard.md`）

- 新場景版本 `remelt-cold-open`：帆布已扯下、三號爐冷且蒙灰，有練習爐、黃線、鋼板（已加進 `cast.json`）；第 32 集 c28 起到第 34 集都用這一版，不用蓋帆布的 `remelt-cold`。
- 第 34 集 Theo 的名字第一次被叫之前沒鋪：c34 改成 "Charge me market rent. Clause two."。平板只從 Theo 左肩後或正側面拍，螢幕側成一條細邊。
- 第 35 集 Elias 右手把筆推到估價單旁、指尖點一下簽名處（"Not until my lawyer reads it." 的起因）；估價單最後回到 Nora 手邊、對摺收進外套內袋；保付支票連同租約、筆一起推過去。
- 說話的臉用穩定的光：Brandt `soft grey window light across her face from frame left`，檯燈只照桌面；Elias 背窗時 `face evenly lit by soft daylight off the table`。
- 帳本那句是 "Twenty cups. Two days."（跟 decisions 一致）。
- **第 35–40 集審稿後補定**（`../review/2026-11-12-e035-e040-storyboard.md`）：黃線通道句 `the worn yellow safety line turns along the back wall, leaving a narrow walkway to the storeroom door`，有 Nora 在場的 Remelt 鏡都寫她在通道那側或線外；
  退火後的玻璃由 Gus 脫右手套赤手按一下再遞給她（玻璃涼到能拿，熱玻璃從不碰到人）；第 36 集玻璃管朝裡端微微傾斜、第一個銅環位置管內有一個小擋點（珠子才滾得過去、停得住，畫面不解釋）；熔融的玻璃一律橘光，藍色在冷下來後才出現。

