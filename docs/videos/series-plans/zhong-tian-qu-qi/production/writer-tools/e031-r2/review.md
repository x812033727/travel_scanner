# 第 31 集重製版 r2（e031-r2，內部 931）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿：沒參與寫稿的獨立代理，2026-11-17，開拍前（d1 還沒產生、錄音還沒錄）。只寫這一個檔；沒改 `r2.py` 或別的檔、沒用 Colab／RunPod／付費服務、沒 commit。
- 審的對象：`writer-tools/e031-r2/r2.py`、`docs/videos/zhong-tian-qu-qi-e031-r2/{script.md,storyboard.md,video.json,overlays.json}`、`hailuo/clips-dh-e931.json`（精修文字）、`hailuo/ff-dh-e931.json`。
  `colab/runs/e931/extras.json`、`e931-live/{mkspec.py,spec.json}`、`prep931.sh`、`colab-jobs.json` 都還沒做，所以 d1 的機械掃描（分隔句、`shown in <Picture` 外漏、`prompt_sha256`）**還不能跑**，列在最後要做的事。
- 對照：`r2-bible-e031-e040.md`（拍法 1–43、〈場景〉〈接點〉30→31〔2026-11-17 照第 30 集 s41 fix2 更正的那列〕與 31→32、〈道具〉〈人物〉〈小角色〉、好感帳、原版必修、〈還沒解決的〉）、`r2-bible-e011-e060.md`、
  任務檔 `tasks/open/2026-11-07-zhong-tian-live-action-remake.md`（e920／e925／e928 注意與第 21–30 集教訓）、`writer-tools/e030-r2/review.md`、原版 `docs/videos/zhong-tian-qu-qi-e031/{brief,storyboard}.md`、`assets/refs-live/README.md` 第 4 篇章段。
- 參考圖：本集要送的場景圖全部縮圖看過、加格線看座標；`set-xujia-yuan-ye-dong-l1` 屋門與院門一帶放大 2 倍；`-han-l1` 依 s18 的 crop 試裁兩種；
  **`set-shangyou-ba-l1` 在審稿途中歸檔（20:47，37042 加 `clean_shangyou_box.py`）**，已用實際歸檔的檔案看過原圖、水平翻轉版與六個候選裁切（scratchpad，用完即刪）。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| 台詞 | 47 句全部在 `script.md` 原文裡逐字找到；c29 三句拆成 s29（心裡話＋系統）／s29b（心裡話），c21 後加無台詞的 s21b，共 43 鏡 |
| open／否定名詞／會長字的名詞 | `video.json` 43 支提示詞沒有 `open`、`lantern`、`sign`、`plaque`、`banner`、`crowd`、`villagers`、`table`、`bench`、`saddle`、`water wheel`；`Tang Xiaotang` 只出現在 s21b（正臉鏡） |
| 人數 | 43 鏡每鏡都有 `exactly N people`／`the only person`／插鏡的 `only … are in the frame` |
| 畫外說話 | 對畫外說的鏡都寫 `toward someone out of sight beyond the left/right edge`＋那一側只有景＋只有他一個人；不點名唐家、唐萬金、鄭伯、秦霜、小禾、白馬、畫外家丁；過肩前景都是不點名、不送圖的背影 |
| 朝鏡頭的臉在畫外句時閉嘴 | s04、s05、s07、s08、s14、s15、s16、s22、s24、s28、s29、s29b、s30、s31、s32、s33、s41 都寫 `say(s) nothing … lips stay pressed together` 或 `SILENT_HE` |
| 唐小棠 | 背影鏡 s05、s06、s19、s20、s22、s30 與全景 s04、s24 都是 TBACK：正背對、頭不動、剛好兩顆丸子、`every strand … combed smooth`、緞帶是 `wrapped around each bun`（沒有垂下的東西）；只有 s21b 送她的圖。精修文字：背影鏡把名字換成 `the young woman seen only from behind`、加 `back to us`，s21b 留名字、拿掉立領句（`clips-dh-e931.json` 掃過：沒有 `stand-up collar`，背影鏡沒有 `Tang Xiaotang`） |
| 魏少卿 | s02–s04 扇子 FAN 合著、三鏡不笑；白馬一個字都沒有 |
| 阿令面巾 | s01 VEIL_BLOWN（第 21 條實物寫法、左耳）＋沒面巾的定妝照與 angle-a；s03、s04 VEIL＋`aling-veil-portrait-l1`；夜裡 GAUZE_KNEE。她朝畫左時左耳在靠鏡頭這側，看得到 |
| 二牛與村民 | 二牛每鏡 `not smiling`、咬牙或喘；全集只有他一把 HOE，s24、s31、s33、s41 寫 `the only hoe in the frame`；村民五人五種年紀與擔子、沒有鋤頭（原版必修兩條）；畫面上沒有水車（原版必修） |
| 面板與好感帳 | `overlays.json` 只有 s14「阿令 好感 +4 → 32」（第 30 集結束 28 → 32，聖經好感帳第 31 集列相同）與 s28「旱災任務：十日內讓柳溪的田見水」「失敗：稻種枯死」（聖經〈系統〉第 31 集列相同、`penalty` 紅框）；s15、s28 沒寫藍光（第 11 條） |
| 參考圖檔 | 在 refs-live：`aling-portrait-l1`、`aling-veil-portrait-l1`、`angles/aling-angle-a-l1`、`weishaoqing-portrait-l1`（沒有角度圖，FOOT 寫 l1 only，對）、`xuyan-portrait-l1`＋`angles/xuyan-angle-a-l1`、`erniu-portrait-l1`＋angle-a、`qianyuanwai-portrait-l1`＋angle-a、`tangxiaotang-portrait-l1`＋angle-a；場景 `-dong-qing2`、`-dong-jing`、`-dong-men2`、`-dong-wu2`、`-ye-dong`、`-ye-dong-jing`、`-han`、`-han-jing`、`-han-wu`、`-han-qiang`、`-han-men`、`set-ganxi-l1`、`set-shangyou-ba-l1`（剛歸檔）。**還沒有**：`set-xujia-yuan-han-shu-l1`（s18）、`set-xujia-yuan-han-di2-l1`（s21）、壩的近景裁切（s33–s40，見必改 1）、可選的 `-ye-dong2`（見必改 3：改成要做） |
| 接點 30→31 | s01 送 `-dong-jing`、s02 `-dong-men2`、s04 `-dong-qing2`；s04 照第 30 集 s41 fix2 站位（唐小棠前景正中背對抱木盒、阿令前右井邊、許硯畫左屋前三分之二背面朝院門、魏少卿後牆中間院門口）；魏少卿往院門外右邊走出畫、不上馬；c07 不拍大車與燈籠、改陶油燈。通過 |
| 30→31 的動作接法 | 第 30 集 s41 收在阿令手扶轆轤；s01 第一格她左手已經捏著紗尾（「把水桶放上井沿」在第一格前完成），中間是全景切中近景，可以接受 |

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| s21b 唐小棠的正臉：留還是拿掉？ | **留**。聖經第 40 條明寫建議用在「c21→c22 看到稻芽」，每集上限兩鏡、本集只用一鏡；不說話、嘴閉著；前一鏡是插鏡、後一鏡 s22 是中景背影，景別不同；眼神方向對（s22 許硯朝畫右看她，s21b 她朝畫左看碗）。已知風險是正臉畫成一個髻＋長緞帶、跟 s22 的雙丸子不一樣（第 22、23 集接受過）。**退路**：挑片時兩個種子都不是雙丸子或嘴動，就整鏡拿掉——s21（「發芽了！」）直接接 s22 劇情不缺，只少 5 秒 | 建議 1 |
| s18 送哪張圖 | **送 `-han-l1` 的裁切，但不要用 `-dong-shu-l1` 的 crop**。`crop=480:270:560:0` 把太陽圓盤整個裁進右邊的枝椏裡（試裁看過）：插鏡的主體是枝頭的小新芽，逆光下會變成黑剪影，還會起光暈。改裁 `crop=320:180:480:0`（太陽在框外右邊，只剩發亮的淡奶油色天空、清楚的禿枝、左下一小角瓦簷），放大到 1312×736，新 id `set-xujia-yuan-han-shu-l1` 不變 | 必改 6 |
| s37 的動作簡化 | **簡化得對，接受**。稿子 c37 一鏡五個動作（甩鞭、車往右走、回頭揮手、家丁點頭握棍、兩人丟鐵鍬拔棍）；只留「錢員外平掌往畫左一揮」、車走交給音效、家丁拿棍子放到 s41 第一格，符合第 32、34 條。要配合新的壩圖改兩處文字（壩頂沒有土路；車夫照寫背影），見必改 1 | 必改 1 |
| 壩圖還沒歸檔 | **已歸檔，跟提示詞的地理不合**，s32–s41 十鏡都要照圖改，詳見必改 1（含聖經 31→32 那列要不要改、近景要哪些裁切） | 必改 1 |
| `-ye-dong-l1` 屋門右邊的空白木板：寫素牆還是塗掉 | **塗掉**（免費）。放大看是一塊深色方板，跟第 27 集塗了又長回字的那種一樣；而且同一張圖院門右柱上方還有一團沒有燈體的暖光（燈籠塗掉後留下的光），s07、s08 是全景，兩處都會被讀成掛著的東西 | 必改 3 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 31 | s32–s41（壩）與聖經 31→32 | **實際歸檔的 `set-shangyou-ba-l1` 跟提示詞寫的不是同一個地方**。圖上（1312×736）：一長排麻袋土埂從**左下前景**（x 0–700、y 520–736）往**右後**斜著退到 x≈1060、y≈370，盡頭接右岸一塊石砌平台（x 1050–1250、y 370–420）；黃泥水塘在土埂**後面、畫左**（x 0–900、y 340–520），水塘遠端還有一道低石線；土埂**右腳**是一條石邊土路（x 700–1050、y 430–736），再右是一條流向鏡頭的泥水小溝（x 940–1130）、最右是青秧田（x 1200 起）；兩邊是竹林山谷。相機站在土埂上。**沒有乾溪床、沒有壩前的大石堆、土埂頂是一顆顆圓鼓的麻袋、沒有能站人與騾車的土路**。所以：(1) `B0`「At the upper end of the dry stream bed」、`DAM` 的「across the stream bed」「along its right end … on the right」、`ba_c` 的「cracked earth of the gully floor」、s34「beaten earth path along the top of the dam」、s35「big rough rock before the dam」、s37「beaten earth path along the dam top」、s38「the dry gully」、s39 `SIDE_GULLY`「dry cracked bank」、s40「low heap of rough rocks」都畫不出來（場景圖壓過文字，第 19 條），或會讓模型自己另長一條乾溝；(2) 左右反了：照原圖，柳溪的人只能站在右邊那條土路上、往**畫左**看土埂，跟本集所有近鏡（許硯、二牛朝畫右看壩、錢員外朝畫左下看、二牛往右衝）與 31→32、第 32 集 c01（秦霜從畫面左跑進來）相反；(3) s41 原文「家丁在壩頂一排、面向我們」放到整張圖上，靠右前那一段的家丁會變成近景大人（第 34 條：家丁只在遠景） | 第 19、29、34、35、42 條；〈接點〉「新圖挑定後若左右跟這裡不同，照圖改這張表」；第 9 條只禁止翻轉交領**人物**，場景圖沒有字、沒有人，可以翻 | **(A) 建議做法：場景圖水平翻轉一張新 id，聖經 31→32 的左右不用改。** `ffmpeg -i set-shangyou-ba-l1.png -vf hflip set-shangyou-ba-fx-l1.png`（免費、新 id，第 19 條；第 32 集第一場同一個壩也送這張）。翻過來：麻袋土埂從**右下前景**往**左後**退、水塘在右後、石邊土路與小溝與青秧在**左**——柳溪的人站在左邊土路上、壩在右，所有近鏡與第 32 集照原寫法。翻轉後的座標（以下都是 `-fx` 上的 crop，`crop=W:H:X:Y,scale=1312:736:flags=lanczos`，新 id；括號是原圖上的等價 crop）：<br>• `set-shangyou-ba-fx-ding-l1` = `512:288:500:60`（原圖 `512:288:300:60`）：霧白的天、竹林山谷、遠處一點青田——s34、s36 錢員外的低角度鏡背後。<br>• `-fx-tang-l1` = `640:360:672:200`（原圖 `640:360:0:200`）：竹坡、遠端石線、黃泥水塘、左下一角麻袋頂——s37。<br>• `-fx-jiao-l1` = `480:270:150:420`（原圖 `480:270:682:420`）：左邊泥水小溝、中間石邊土路、右邊麻袋坡——s35 俯拍壩腳的許硯。<br>• `-fx-lu-l1` = `640:360:150:376`（原圖 `640:360:522:376`）：同上再寬一點、右邊麻袋往後延伸——s38、s40。<br>• `-fx-shan-l1` = `448:252:0:100`（原圖 `448:252:864:100`）：整片虛焦竹坡（y 不要超過 352，下緣會切到土埂盡頭的麻袋）——s33、s39 背景。<br>• s32、s41 送整張 `-fx`。<br>**文字照圖改（r2.py）**：<br>• `B0` = `In the bamboo valley upstream of the dry Liuxi stream on the same hot afternoon, at the Qian family's dam`；<br>• `DAM` = `a long rough bank of stacked brown hemp sacks of earth on a footing of rough fieldstones, running from the right foreground away to the far left of the valley, uneven and handmade, its top a row of round lumpy sacks; behind it on the right a wide still pond of muddy brown water held back to a low line of stones at its far end; along its left foot a narrow stone-edged earth path and beside it a narrow ditch of muddy water flowing toward us, and at the left edge a strip of bright green young rice; steep green bamboo hills on both sides`；<br>• `ba_c` = `{B0}, on the narrow stone-edged earth path at the foot of the bank of brown hemp sacks; {BAKE}`；`SIDE_GULLY` 換成 `the soft green bamboo slope of the valley`。<br>• s32：`along its top … two men … stacking brown hemp sacks with iron spades` 改成 `two men … shovelling earth onto the sacks with iron spades, and ten more men dressed the same, each holding one plain wooden staff, standing in a loose row along the far half of the crest`；騾車改 `on the crest a little right of the middle, one plain wooden cart bed with five brown hemp grain sacks, one carter seen only from behind at its front, and beside it one stout man in a dark gold brocade robe`，人數 `exactly fourteen people`（車夫要算進去，s37 他在）。<br>• s34：`standing on the beaten earth path along the top of the dam` → `standing on the flat crest of the bank of brown hemp sacks`；`behind him, soft, the still muddy pond and the bright green field beyond it` → `behind him, soft, only the hazy white sky and the green bamboo slopes of the valley`（`-fx-ding`）。<br>• s35：`already standing on a big rough rock before the dam` → `already standing on the narrow stone-edged earth path at the foot of the bank of sacks`；背景 → `behind and below him, soft, the narrow ditch of muddy water beside the path`（`-fx-jiao`）。<br>• s37：`that side of the frame is only the beaten earth path along the dam top and the hazy sky` → `that side of the frame is only the crest of the bank of sacks and the muddy pond`（`-fx-tang`）。<br>• s38：`on the cracked earth of the gully floor` → `on the narrow stone-edged earth path at the foot of the bank of sacks`；背景 → `behind them, soft, the bank of brown hemp sacks rising at the right and the narrow muddy ditch at the left`（`-fx-lu`）。<br>• s39：背景 → `behind him, soft, only the green bamboo slope of the valley`（`-fx-shan`）。<br>• s40：`close to the cracked earth of the gully floor` → `close to the stone-edged earth path`；`ahead at the right a low heap of rough rocks before the dam, the dam beyond them` → `ahead at the right the slope of the bank of brown hemp sacks rising from the path, its crest out of the frame`；`GAZE_REFINE["s40"]` 同改 `his face toward the bank of sacks at the right of the frame, his eyes on it`。<br>• s41：`in the left foreground, cut at the waist` → `in the lower left foreground, on the stone-edged path at the foot of the bank of sacks, cut at the waist`；家丁 `standing in one row along the top of the dam` → `standing in one row along the far half of the crest of the bank of sacks, from the middle of the frame away to the left, all small and far, facing us`（前景右邊那段麻袋頂不站人）。<br>• `zh` 欄與 HEAD／FOOT 的「乾溪床盡頭」「壩前的大石」「壩頂土路」照改；FOOT 的「還沒有的圖」換成上面六個 id。<br>**聖經 31→32 那列**：左右不用改（柳溪這邊左、壩與家丁右），只改地形字：「午後，乾溪床盡頭的壩前」→「午後，上游竹林山谷裡錢家的麻袋壩（`set-shangyou-ba-fx-l1`，左右照翻轉後的圖）：柳溪的人在壩腳左邊的石邊土路上、壩在右」；「二牛舉鋤頭往右衝到壩下」→「二牛在左下前景的土路上舉著鋤頭、背對鏡頭衝向壩，壩頂遠處十二個家丁的棍子舉起」。第 32 集 c01「秦霜從畫面左跑進來」照舊（她從土路後面上來），被抽扁擔的村民要在 c01 第一格（第 31 集 s41 沒拍村民，不衝突）。〈場景〉表的「上游錢家的壩」那列也補一句實際的格局。<br>**(B) 不翻圖的話**：要把 s33–s41 的每個方向反過來（許硯、二牛朝畫左看壩、錢員外朝畫右下看、二牛往左衝、s35／s36 的過肩前景左右對調、`GAZE_REFINE` s33、s34、s37、s39、s40 跟著反），聖經 31→32 寫成「柳溪這邊在右、壩在左」，第 32 集 c01 秦霜改「從畫面右跑進來」。改動多、第 32 集也要跟，不建議 |
| 31 | s07–s17（夜、井邊） | **越軸**。s07、s08 全景照圖：屋在左，許硯從屋門出來往右前的井走，到井邊時他在阿令的**畫左**；可是近鏡寫成他在她右邊——s09、s11、s12、s17 阿令朝畫右看他，s10 過肩他在右半、朝畫左看，s13、s15 他朝畫左，s16 雙人井沿上阿令左、許硯右。從 s08 切到 s09 觀眾會看到他突然換到另一邊。CG 稿是屋在右（原版 brief：「許硯從右邊屋門走來、蹲在井的右邊」），真人圖屋在左，這裡沒有跟著翻。圖也支持翻：`-ye-dong-jing-l1` 井的左邊是空地（兩塊磚、一個石槽），右邊緊貼牆角，蹲人放不下 | 第 29、42 條（場景圖說了算）；任務檔「screen direction and eyelines across cuts」；第 24 集 s34 越軸重拍 | 夜裡近鏡整組左右對調：s09、s11、s17 阿令 `three-quarter to screen left`、`off('left', …)`；s09 動作 `rise once to the moon above`（不寫哪一邊）；s12 `turns her face away toward the right edge of the frame`；s14 `turns her face back toward the left edge`；s17 `holds the empty bowl out toward the left edge`；s10 `BACK_ALING` 改成 `at the right edge of the frame, cut by it, …`、許硯 `in the left half of the frame … three-quarter to screen right toward the woman in the foreground`；s13 `off('right', SIDE_NWALL)`；s15 `his eyes on a spot beyond the right edge`、動作 `flicking to the right edge of the frame and back`；s16 `on the left {XU_COAT} … tipped up three-quarter to screen left toward the moon` 與 `on the right … {ALING}`。`GAZE_REFINE`：s09、s11、s17 改 `her face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, her eyes on that spot`；s12 改 `…turning away toward the right edge…`；s13 改 `_R`。`zh` 與 r2.py 開頭〈THE AXES〉的夜裡那句照改（「許硯蹲在她左邊，雙人鏡她在右」）。s08 不動 |
| 31 | s07、s08（`set-xujia-yuan-ye-dong-l1`） | 圖上屋門右邊、窗左邊有一塊深色空白木板（README 記的 x 251–302、y 306–373），院門右柱上方簷下還有一團沒有燈體的暖光（x≈650–700、y≈270–320，原燈籠的光）；s07、s08 是全景、整張送。提示詞只寫 `the plain stone wall` 擋不住圖（第 19 條），木板會長字、光團會長回燈籠，正是 c07 要拿掉的那盞 | 第 33 條（場景圖上掛著的東西免費塗掉，用旁邊同材質柔邊接過去）；第 27 集塗掉的牌子留下暗方塊又長回來 | 開拍前照 `e930tools/clean_yard.py` (a) 的做法免費做 `set-xujia-yuan-ye-dong2-l1`：(a) 木板用左右同一排石牆接過去、柔邊；(b) 院門右柱上方那團光往周圍牆色拉回、亮度降到跟左柱一樣。s07、s08 改送它；`-ye-dong-jing-l1` 的 crop 不含這兩處，不用重裁。塗完放大 3 倍看沒有方框輪廓再歸檔，寫進 refs-live README 第 4 篇章段 |
| 31 | s06 | 構圖段同時寫 `his face three-quarter to screen right toward her` 與 `his eyes on the house door beyond the left edge of the frame at first`：臉朝右、眼睛看左外，互相打架；而且 `-dong-wu2-l1` 的屋門**就在畫面裡**（他身後左邊），「畫左外的屋門」不存在，模型會讓他回頭、或在畫左另長一扇門 | 第 29 條；一鏡一個動作、第一格寫清楚（第 32 條） | 第一格改 `his face three-quarter to screen right toward her, his eyes lowered to the earth between them at first, never the lens`；動作改 `Xu Yan's eyes lift from the earth to the young woman as he speaks; {HEADSTILL}`。`zh` 的「眼睛從畫左外的屋門收回來」改「眼睛從地上抬起來看她」 |
| 31 | s31 | `set-ganxi-l1` 的溪床是**從前景直直往遠方延伸**（消失點約 x 830、y 390），中間鋪著一條長長的木板走道（x 590–850），左岸是房子與柳樹、右岸是草與金黃稻田。(1) 「walking from the left toward the right」等於橫越溪床、從村子那岸走到稻田那岸，不是往上游；(2) `the low plank bridge with nothing under it` 圖上沒有橫過溪的橋，模型會另畫一座 | 第 19、29 條（照圖寫）；試鏡一挑片紀錄（README：溪床跟岸幾乎齊平、泥板像鋪石） | `LOC["ganxi"]` 的橋句改 `the long plank walk laid down the middle of the bed, the willows and village roofs on the left bank, the grass bank and the field on the right`；構圖改 `walking away from us along the dry bed toward its far misty end, on the cracked mud plates to the right of the plank walk, in a loose line, all framed full figure, small: at the front {ERNIU}, … his head turned back over his left shoulder toward the others, his face in profile, never the lens; just behind him {XU_UP}, …`；動作 `the seven of them walk steadily away from us along the cracked mud of the stream bed`。往遠方走是中性方向，接 s32（看上游）與之後的左右都不衝突 |
| 31 | s18（圖） | 見上表：照寫稿的 crop 太陽圓盤在枝椏裡，新芽逆光成黑剪影 | 第 10、35 條（插鏡第一格就是主體） | `set-xujia-yuan-han-shu-l1` = `-han-l1` `crop=320:180:480:0,scale=1312:736:flags=lanczos`；`SKY_LIGHT` 改 `bright hazy afternoon light from the right, the sun beyond the right edge of the frame` |
| 31 | s04–s41 村民（`VILLAGERS`）、s33 | 村民五人寫 `grey-blue`（faded grey-blue、dark grey-blue、pale grey-blue、slate blue），許硯是 `faded blue-grey` 書生袍：英文對模型幾乎是同一個顏色。s31 全景七個小人、s33 中景兩個在二牛身後，正是「群眾長成主角分身」的條件。聖經〈小角色〉寫「灰藍（跟二牛的褐色分開）」只顧到二牛，跟第 34 條「許硯藍灰…都不能給群眾」自相矛盾 | 第 34 條；任務檔第 26 集 s35（衣色不寫就長成賴三分身） | 五人改成避開藍灰、褐、深褐、灰白、桃粉的顏色：`a white-haired old man in a faded undyed hemp-beige jacket`、`a lean middle-aged man in a dark charcoal jacket`、`a thin boy of fifteen in a faded indigo jacket`、`a broad middle-aged man in a dull olive-green jacket`、`a middle-aged woman in a dark grey jacket with a faded indigo head cloth`（擔子照舊）；開頭的 `in Song-dynasty grey-blue cross-collared homespun short jackets` 改 `in Song-dynasty cross-collared homespun short jackets, each a different colour`。s33 改 `two more people in homespun jackets, a white-haired old man in faded undyed hemp-beige … and a thin boy of fifteen in faded indigo …`。聖經〈小角色〉「村民（壩前）」那列同步改（第 32 集 c01 照用） |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 31 | s21b | 留（見上表）；正臉與背影髮型不同是已知毛病 | 第 40 條 | 挑片條件寫進 `extras.json` 的 note：兩個種子都看「雙丸子、嘴閉著、沒有轉向鏡頭」；都不行就整鏡拿掉、不重拍（剪接 s21 直接接 s22），本集正臉額度留給第 35 集 |
| 31 | s11、s19 | BUY 照「19 字以上買 8 秒」估，但第 30 集的實際錄音是每秒 2.6–3.3 字（a05 18 字 6.20 秒、a14 15 字 6.44 秒、a34 16 字 5.80 秒），6 秒的鏡放得下約 6.27 秒。s11「他是在一道很高的牆裡，見過我的。」14 字但標「很輕，一字一字」，慢讀會到 6.5 秒以上；s19 唐小棠 18 字、「聲音悶」，估 6.2–6.9 秒 | 第 43 條；第 30 集 BUY 註解的容量算法 `(buy − 0.3) × 1.1` | s11、s19 先列 8 秒；錄音後照 `span930.sh` 量人聲長度再定（s20、s23、s27、s33 是 15–17 字，量出來超過 6.2 秒也改 8）。s29（15＋13 字）估 7.2–7.8 秒，8 秒放得下；s29b 15 字心裡話約 4 秒，5 秒可以 |
| 31 | s24 | `chars=["erniu"]`，但構圖點名 `{XU_UP}`（左前景、三分之二背面），精修文字也寫「Wang Erniu and Xu Yan shown in <Picture 1>」；許硯沒有參考圖，全景裡的他可能換一張臉 | 任務檔「refs 清單跟提示詞點名的人要一致」；FOOT「全景只送 l1」 | `chars=["erniu", "xuyan"]`，spec 只送 `xuyan-portrait-l1`（不送角度圖），跟 s04、s31 一樣 |
| 31 | s32 | `exactly thirteen people` 沒算車夫，s37 卻有車夫；`stacking brown hemp sacks with iron spades` 動作不通 | 接戲；第 34 條寫實際人數 | 見必改 1 的 s32 改寫（車夫背影、十四人、鏟土） |
| 31 | s30 | `-han-wu-l1` 的院門在**畫面右緣裡面**（x≈1150–1312），許硯「往畫右外的院門一揮」又寫二牛站在右三分之一，院門會被二牛擋住或被推出框 | 第 29 條 | 動作改 `Xu Yan sweeps his flat right hand once toward the yard gate at the right of the frame as he speaks`；二牛 `in the right third of the frame, just left of the yard gate` |
| 31 | s05 | s04 全景裡唐小棠在前景正中、許硯在畫左屋前，兩人隔好幾步；s05 她已經伸手拉他的右袖（只隔一步）。剪接上是小跳 | 接戲 | 可以接受（換機位、中景）。要更順的話 s04 把唐小棠寫在 `in the middle foreground, a little left of centre, a few steps to the right of Xu Yan`，但不要動 30→31 的站位定案；不改也行 |
| 31 | s19 | `both her hands already on the rope of the wooden windlass` 與「泥水桶已經提上井沿」同時成立時，手該在轆轤的木柄上，不是繩上 | 一鏡一個動作，道具與手寫在第一格 | `both her hands resting on the wooden handle of the windlass from the first frame` |
| 31 | s31 光 | `set-ganxi-l1` 是粉紫晨霧（試鏡底圖 `set-liuxi-he-l1` 的光），提示詞寫 `hazy white afternoon sunlight`；右岸稻田金黃、左岸柳樹翠綠，旱象只在溪床 | 第 19 條（圖定地點、不定光）；README 挑片紀錄 | 不擋開拍；挑片時看光有沒有跟著文字變白。照聖經「溪床跟岸」的毛病接受；金黃稻田不寫（寫了也不會消失），劇情靠台詞與 s24 的乾裂 |
| 31 | s32、s41 | 翻轉後的壩圖裡，家丁站在圓鼓的麻袋頂上，模型可能把他們放到水塘邊或土路上 | 第 34 條 | 挑片時看家丁是否都在遠段麻袋頂、都拿一根棍、沒有正臉近景；不行就 fix1 的 s41 改送 `-fx` 的 `crop=800:450:256:180`（只剩遠段土埂、水塘與山谷；這個框左右對稱，原圖上也是 `800:450:256:180`），二牛背影仍寫在左下 |
| 31 | 插鏡 s18、s21 | `video.json` 裡兩支插鏡的提示詞還以 `H0:` 開頭（「In the courtyard of the Xu farmhouse three months later…」），要靠還沒寫的 `mkspec.py` 拿掉 | 第 35 條；第 30 集必改 3 | `mkspec.py` 寫好後掃 d1：s18、s21 不能有 `courtyard`、`farmhouse`、`yard`；s21 送 `-han-di2` 前照 `clean_di.py` 塗掉左下葉形石片並放大確認 |
| 31 | s01 精修文字 | 精修句寫 `her lips, jaw and cheeks moving clearly with every syllable`，但她是拉上紗之後「隔著面紗」說 | 第 21 條 | 不擋開拍；挑片時看紗有沒有被嘴型吹穿、或紗沒拉上就開口。精修若嘴型穿紗，s01 精修句可加 `her lips moving under the gauze` |

## 接受（看過、不用改）

- 第一場白天 s01–s06：院子左右照圖（屋左、院門後牆中間、井前右）；阿令朝畫左看院門、魏少卿朝畫右看井，跟第 30 集 s39／s40 一致；s03 腰以上、井沿在下緣（第 32 條）；s05 拿木盒的右臂與拉袖子的左手都不越過身體。
- s04 魏少卿往院門外右邊走出畫、馬蹄交給音效（〈還沒解決的〉第 2 條）。
- s07 陶油燈 LAMP 放在門前石階上、s08 仍在石階上沒人拿（第 33 條）；夜裡許硯披舊灰外衣、阿令沒戴面巾、灰紗摺在膝上（〈道具〉）。
- s12 耳尖整片泛紅（第 12 條）；s14 好感鏡全程閉嘴、面板由剪接疊；s16 喝湯改捧碗低頭（不動嘴）。
- 第二場 s19–s30：`-han` 一組裁切位置對（井、屋前、牆與裂土、院門）；「正午」改午後斜陽（〈還沒解決的〉第 6 條）；沒有矮木桌，碗拿在許硯手上；s21 寫 `lifts`、s25 寫 `uncurls`（第 36 條）；二牛左拳乾泥（〈人物〉）；s24 二牛停在許硯右邊（第 42 條）；s26／s27 過肩反打左右一致。
- s29 拆成 s29／s29b：s29 兩句估 7.2–7.8 秒，8 秒放得下；s29b 眼睛往畫右（上游）接第三場。
- s33 稿子「一手指著壩頂」不拍（單指會讀錯）；s36 稿子「爬上騾車」放到第一格完成；s37 的簡化（見上表）；s38 許硯左手抓二牛右前臂，兩人側面、手不越過身體；s40 整個衝的動作留在畫面、剪在半途；s41 許硯的喊聲放錄音、畫面上的人嘴都閉著。
- 騾子只寫頭頸在畫右緣（第 41 條）；車夫背影、灰布包頭、**不寫草帽**（落水真相的線索）。
- 錢員外錦袍胸前素的、三個金戒指；s34 假笑、s36 冷笑照稿子；家丁只在 s32、s41 遠景（第 34 條）。
- 原版必修三條（二牛報壞消息笑、背景兩個二牛、水車）都有擋。
- 接點 31→32：s41 停在棍子舉起、鋤頭在半空；第 32 集 c01 秦霜從畫左進來照舊可用（翻圖做法下）。

## 小結

- **必改 7 條**：(1) 壩：實際歸檔的圖跟 s32–s41 的地形與左右都不合——建議免費水平翻轉成 `set-shangyou-ba-fx-l1`（聖經 31→32 的左右不用改，只改地形字），出 5 個近景裁切（`-fx-ding` s34／s36、`-fx-tang` s37、`-fx-jiao` s35、`-fx-lu` s38／s40、`-fx-shan` s33／s39；s32、s41 送整張），十鏡的地點句、`DAM`、`B0`、`ba_c` 照圖改；(2) 夜裡 s09–s17 越軸：許硯從左邊屋門來，近鏡整組左右對調；(3) `-ye-dong-l1` 的空白木板與院門柱上的光團免費塗掉成 `-ye-dong2-l1`，s07、s08 改送；(4) s06 臉朝右、眼看左外的屋門互相打架，改成從地上抬眼；(5) s31 照圖改成沿溪床往遠方走、木板走道不是橋；(6) s18 換 crop `320:180:480:0`，避開太陽圓盤；(7) 村民不能穿灰藍（撞許硯的藍灰），五人換五種顏色，聖經小角色列同步。
- 寫稿者三個問題：**s21b 留**（有退路）；**s18 換裁切**；**s37 簡化接受**。
- 好感（阿令 28 → 32）、面板文字、台詞逐字、Tang Xiaotang 的名字與背影寫法、不寫 open／掛著的東西、畫外不點名，都通過。
- 開拍前還要做（照 `prep930.sh`）：做 `-fx` 與五個裁切、`-han-shu`、`-han-di2`、`-ye-dong2`（全部免費、新 id、絕對路徑 swap）；`extras.json`、`mkspec.py`、`spec.json`、`prep931.sh`；錄音後照 `span930.sh` 重核 BUY（s11、s19 先列 8 秒）；重建 d1 後跑第 30 集審稿那張機械檢查表（分隔句各一次、沒有 `shown in <Picture`、`prompt_sha256` 相符、兩個種子逐位元相同、s18／s21 沒有地點字）與 `preflight-prompts.py`。

## 寫稿者照改的紀錄（2026-11-17，協調者決定：必改 7 條全改、壩用做法 A、s21b 留、重要建議照收）

| 項目 | 處理 | 在哪裡 |
| --- | --- | --- |
| 必改 1 壩 | **照改（做法 A）**。`live-action/free-e031-e040/shangyou_fx.sh`：`set-shangyou-ba-fx-l1`（hflip）與 `-fx-ding`／`-fx-tang`／`-fx-jiao`／`-fx-lu`／`-fx-shan`（照本審稿的框），兩次逐位元一樣、全尺寸看過。`B0`、`DAM`、`ba_c`、`SIDE_GULLY`、s32–s41 照本審稿的英文改；s32 鏟土、車夫背影、十四人；s41 家丁在土埂遠段、從畫面中間往左後；`GAZE_REFINE["s40"]` 看麻袋坡；zh 欄、HEAD、FOOT、script.md〈真人版的改動〉照改。聖經 31→32 那列左右不動、只改地形字，〈場景〉壩那列補實際格局 | `r2.py`、`refs-live/README.md`、`r2-bible-e031-e040.md` |
| 必改 2 夜裡越軸 | **照改**：s09、s11、s17 朝畫左；s12 別到畫右；s14 轉回畫左；s10 背影在右緣、許硯在左半朝畫右；s13、s15 朝畫右；s16 許硯左、阿令右；`GAZE_REFINE` s09、s11、s12、s13、s17 跟著改 | `r2.py` |
| 必改 3 夜圖 | **照改**：`ye_dong2.py` 出 `set-xujia-yuan-ye-dong2-l1`（木板連它的投影、院門右柱一帶的燈籠光與暗縫光紋），s07、s08 改送 | `r2.py`、README |
| 必改 4 s06 | **照改**：第一格眼睛看兩人之間的地、動作抬眼看她 | `r2.py` |
| 必改 5 s31 | **照改**：沿溪床往遠方走、在木板走道右邊；地點句的橋換成長木板走道 | `r2.py` |
| 必改 6 s18 | **照改**：`han_extra.sh` 出 `set-xujia-yuan-han-shu-l1`（`crop=320:180:480:0`）；`SKY_LIGHT` 照改 | `r2.py`、README |
| 必改 7 村民 | **照改**：五人五種衣色（本色麻、炭灰、褪色靛藍、暗橄欖綠、深灰），s33 兩人同步；聖經〈小角色〉村民列與第 39 集村民甲、原版必修第 31 集列同步 | `r2.py`、聖經 |
| 建議 s21b | **照收**：留；挑片退路（兩個種子都看雙丸子、嘴閉著、沒轉向鏡頭，都不行就整鏡拿掉、不重拍）寫進 `colab/runs/e931/extras.json` 的 `_note` 與 HEAD | extras、`r2.py` |
| 建議 s11、s19 BUY | **照收**：都買 8 秒；錄音後照 `span930.sh` 重核（s20、s23、s27、s33 量出超過 6.2 秒也改 8） | `r2.py` BUY |
| 建議 s24 | **照收**：`chars` 加 `xuyan`，spec 只送 `xuyan-portrait-l1` | `r2.py`、`mkspec.py` |
| 建議 s32 | **照收**（併入必改 1） | `r2.py` |
| 建議 s30 | **照收**：院門在畫面右邊裡面、二牛在院門左邊 | `r2.py` |
| 建議 s19 手 | **照收**：兩手扶在轆轤的木柄上 | `r2.py` |
| 建議 s18／s21 地點字 | **照收**：`mkspec.py` 把兩支插鏡 d1 的 `H0: ` 拿掉，`prep931.sh` 掃 `courtyard`、`farmhouse`、`yard` | `mkspec.py`、`prep931.sh` |
| 建議 s05 | **不改**：審稿說不改也行；30→31 的站位定案不動，換機位中景的小跳接受 | — |
| 建議 s31 光 | **不改**（審稿：不擋開拍）；挑片時看光有沒有跟著文字變白 | — |
| 建議 s32、s41 家丁站位 | **不改文字以外的事**：照建議挑片時看；不行 fix1 的 s41 改送 `-fx` 的 `crop=800:450:256:180` | — |
| 建議 s01 精修 | **不改**（審稿：不擋開拍）；挑片看紗有沒有被嘴型吹穿 | — |
