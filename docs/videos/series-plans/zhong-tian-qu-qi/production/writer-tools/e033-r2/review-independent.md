# 第 33 集重製版 r2（e033-r2，內部 933）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿：沒參與寫稿的獨立代理，2026-11-19，開拍前（d1 還沒跑、錄音還沒錄）。只寫這一個檔；沒改 `r2.py` 或別的檔、沒開 Colab／RunPod、沒用站台 TTS、沒 commit。
  沒讀前置代理的自審 `review.md` 與 scratchpad 的 `PROGRESS.md`。
- 審的對象：`writer-tools/e033-r2/r2.py`、`docs/videos/zhong-tian-qu-qi-e033-r2/{script.md,storyboard.md,video.json,overlays.json}`、
  d1 提示詞 `~/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/runpod/live/d1/prompts/*.txt`（80 支）與 `colab-jobs.json`、`colab/runs/e933-live/{mkspec.py,PREP.md}`。
- 對照：`r2-bible-e031-e040.md`（拍法 1–43、〈接點〉32→33 與 33→34、〈道具〉〈人物〉〈小角色〉〈場景〉〈原版必修〉）、任務檔第 32 集教訓（泥、鉤子換構圖、兩根長東西第一格不相連、背景人寫手上拿什麼、否定名詞）、
  `writer-tools/e032-r2/review.md`（格式）、`assets/refs-live/README.md` 第 222 行（`set-shentan-l1` 挑片紀錄）。
- 參考圖全尺寸打開看過：`set-citang-huang-l1`、`-huang-zuo2`、`-huang-zuo`、`-huang-liang`、`-huang-qiang`、`set-citang-ye2-l1`、`-ye2-men`、`-ye2-tang`；
  `set-shentan-gongdi-l1`、`-gongdi-an`／`-mu`／`-tian`／`-geng`；`set-shentan-l1`、`-an`、`-lun`、`-geng`、`set-shentan-chen-l1`、`-chen-an`、`-chen-lun`。
  另在 scratchpad 放大看了 `-an` 左上與 `-geng` 地平線（用完即刪）。
- 接點 32→33：抽了 `e932-live.mp4` 183–218 秒每秒一格，另看 209 秒（s36）與 215 秒（s37）全格。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| 台詞 | `video.json` 41 句都能在 `script.md` 原文裡逐字找到；40 鏡＝c01–c40 |
| 面板 | `overlays.json` 只有 s08「旱災任務，剩七日」、s30「旱災任務，今日到期」，跟系統念的一字不差；本集沒有好感變化（42／41／32 照接） |
| d1 清單 | 80 支（兩種子各 40）、共 582 秒；每支 `prompt_sha256` 相符；兩種子的提示詞與送的圖逐鏡一樣；每支 `never the mood. `、`One continuous shot.` 各剛好一次；送的圖每張都在磁碟上（絕對路徑） |
| 送圖與點名 | s17 唐小棠三張臉都拿掉、只送石木匠；s19 只送錢員外（風水先生、唐小棠背影不送）；s20、s27、s34 不送人；許硯 angle-b 全集沒送；全景 s01、s28 許硯只送 l1；s14 二牛換 l1；錢員外 angle-b 沒送、全景 s19、s39 只送 l1 |
| 人數 | 全景都寫 exactly N 且跟描述的人對得上：s01 十人、s05 七人、s06 四人、s07 三人、s12 十人、s22 四人、s24 七人、s31 九人、s39 三人；有名字的臉每鏡最多三張（s31 韓伯、秦霜、小禾） |
| 會長字／掛著／兵器／泥 | 沒有 `open`、`lantern`、`banner`、`sign`、`plaque`、`villager`、`sword`、`knife`、`chopper`、`blade`、`spear`、`mud`、`caked`、`abacus`；`flag` 只出現在 flagstones；`yellow` 只在衣色（芥黃）；沒有 `channel` 搶在 deep pool 前面 |
| 背景人手上 | 拉繩三人兩手在繩上、舉火把兩人各一支、壯丁與岸上六人兩手空著、家丁空手；s22 兩個壯丁合抬一根木料 |
| 唐小棠 | s17 背影正中、頭不動、雙丸子、桃粉肩、`pink inner collar`，沒有 t2 立領；s19 只露左下後腦；全集沒有她的正臉 |
| 秦霜／二牛／風水先生 | 柴刀全集不寫；竹竿 `bare from end to end`、不綁旗；冊子 `plain grey cover, closed`；二牛除 s24 外每鏡 not smiling；風水先生不點名、不送圖、s19 在錢員外身後、s20 側面全景 |
| 祠堂村民 | s01 八人八色，老漢改布包頭短灰鬚；s05 拉繩三人、舉火把兩人取自同一批；s07 扛梁兩人另換深酒紅與褪色綠；第三場岸上六人也取自祠堂那批 |
| 夾在中間的鏡 | s27 插鏡拿掉地點句、天空圖只當顏色；s20、s34 開頭是 `The location shown in <Picture 1>` |

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| 水車照圖、文字只加「十二片葉板」 | **圖上的輪子沒有葉板**：`set-shentan-l1` 是雙層輪緣加十幾根直輻條的大木輪（README 第 222 行挑片時就記了「輪上看不出葉板與竹斗」），文字卻在 11 支提示詞寫 `its twelve flat wooden paddles round its rim`，s30、s35、s38 的手都要按在「葉板」上，s34 的水要打在「最下面的葉板」上。模型只能自己加葉板，加法每鏡不同，這正是原版必修「每鏡外型不一樣」的來源。第 34 集還要許硯釘葉板 | 必改 1 |
| s30、s35 的 `-lun` 裁切 | 輪子在裁切的左邊三分之二，右邊三分之一是旱田與高木架的柱；提示詞要許硯的手按在「畫面右緣的葉板」、臉朝畫右看輪子，圖上那裡沒有輪子 | 必改 2 |
| 祠堂的素牆 `-huang-qiang` 黃昏與夜共用 | 共用可以，但這張裁切**左上角就是那根主梁**（約 x 0–540、y 0–190）。s07 梁壓在許硯肩上、s11 梁已經放在地上，背景牆頂還有梁 | 必改 4 |
| 閘門寫在 `-an` 的石邊缺口 | 位置可以：兩段石階中間正好有一道暗的缺口。但同一張裁切左邊有一條**場景本身的粗麻繩**，從矮木架左柱斜拉到岸上，就在石木匠往後仰的那一側 | 必改 5 |
| s34 鉤子（轉半圈停住） | 固定鏡、結果先寫、整架輪子從第一格就在、不送人，寫法對。缺點是 s34 的提示詞多了一句全景通用的 `Every person in the frame wears dark cloth shoes`（第 32 集沒人的 s32 沒有這句），另外輪輻左右對稱，轉半圈前後看起來一樣，只能靠「轉起來再停住」讀 | 必改 6、建議 9 |
| s33 鉤子（拉閘） | 側面、膝以上、繩與手第一格已經握著、一個動作，讀得出來；風險在必改 5 的麻繩，跟右邊「那一側只有石邊與水」與圖上的輪子打架（建議 7） | 必改 5、建議 7 |
| s05 放梁 | s05 的動作是拉繩結加吼，梁本身沒有一鏡看得到從牆頂下來，要靠 s06 放繩、s07 梁頭壓肩。三鏡連起來讀得出，但 s07 只拍到「一根粗木頭」 | 建議 6 |
| 清晨版 `-chen` | 降飽和加偏灰金，讀起來比較像老照片濾鏡，影子仍是硬的；薄霧寫在光線句。不擋開拍，挑片時看讀不讀得出清晨 | 接受 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 33 | `WHEEL`（s28–s38 的 11 支）、s30、s34、s35、s38 | **文字寫十二片葉板，圖上的輪子沒有葉板**。`set-shentan-l1` 與所有裁切是雙層輪緣加直輻條的木輪，沒有葉板、沒有竹斗；`WHEEL` 寫 `its twelve flat wooden paddles round its rim`，s30 `flat right hand already resting on one wet wooden paddle`、s35 `both flat hands … pressed against one wet wooden paddle`、s38 `gripping the edge of one wet wooden paddle`、s34 `the rushing water strikes the lowest paddles`。參考圖壓過文字，模型要嘛不畫、要嘛每鏡自己加一種，就是原版必修的那個錯。台詞也說「水明明打在葉板上」「十二片葉板」，而第 34 集的戲（重釘葉板、鐵錘）全靠葉板 | 第 19、29、42 條；聖經〈道具〉水車列與〈原版必修〉第 33 集；README 第 222 行 | **建議 A（要花一點點數，照站主常設授權由協調者定）**：開拍前用 Qwen「只改一件事」，以 `set-shentan-l1` 為底，只在輪緣外加十二片平的木葉板，做 `set-shentan-l2`，再重做所有正午與清晨的裁切（`-an`、`-lun`、`-geng`、`-tian`、`-chen*`），`spec.json` 改送新 id。第 33、34 集一起受益。**B（不花錢）**：文字照圖寫，`WHEEL` 改成 `the big spoked wooden water wheel exactly as in the picture: a thick double wooden rim on many straight wooden spokes round a round wooden hub`；s30、s35、s38 的「葉板」一律改成 `the thick wet wooden rim`（s38 改成 `one thick spoke near the rim`）；s34 改成 `the rushing water slaps white against the bottom of the rim`。台詞不動，觀眾聽「葉板」看到輪緣可以接受。B 的話要寫進聖經，第 34 集照用 |
| 33 | s30、s35 | **手按「畫面右緣的葉板」，送的 `-chen-lun`／`-lun` 右邊沒有輪子**。這張裁切的輪子在左邊三分之二（輪緣右端約在全寬 70%），右邊三分之一是旱田、高木架的柱子與一段路。提示詞寫許硯 `standing on the stone edge right beside the wheel`、手在 `the right edge of the frame`、臉朝畫右往上看輪子，背景又寫 `behind him … the spokes and paddles of the wheel`：輪子同時在他背後又在他右手邊，照圖他只能背對輪子、手按在空氣或柱子上。s35 是鉤子之後的第一個反應鏡（推不動），讀不出來就白轉了 | 第 19 條；任務檔「提示詞寫圖上真的有的東西」 | 免費做一張輪子在右邊的裁切：從 `set-shentan-l1` 取 `crop=640:360:60:230`（輪子落在右邊約四成、輪緣切在右緣，左邊是石階一帶的石邊），清晨版同框位取自 `set-shentan-chen-l1`，新 id 例如 `-lun2`／`-chen-lun2`，全尺寸看過再寫進 README。s30、s35 改送它，文字寫許硯在左三分之一到中間、面向畫右、手按在右緣的輪緣（照必改 1 的寫法），背景寫 `beside him at the right, the near rim and spokes of the wheel`。不想多一張圖就直接送 `-chen-an`（s30）／`-an`（s35），它們的右緣本來就是輪子。`-lun` 只留給 s38（石木匠在輪架上、朝畫左） |
| 33 | s25 | **從錯的肩膀回頭，臉會轉離鏡頭**。錢員外 `already turning away to the right`（身體朝畫右走），又 `his face looking back over his left shoulder toward the worksite beyond the lower left edge`。面向畫右時，右肩在靠鏡頭那一側、左肩在離鏡頭那一側；從左肩回頭，頭要經過背對鏡頭的方向才轉到畫左，拍到的是後腦（第 32 集審稿必改 4 同一類） | 第 31 條；第 32 集審稿必改 4 | `comp` 與 `GAZE_REFINE["s25"]` 兩處的 `over his left shoulder` 都改成 `over his right shoulder`，`zh`「從左肩回頭」改「從右肩回頭」；mkspec 照 `GAZE_REFINE` 重產即可 |
| 33 | s07、s11 | **背景的素牆裁切裡還有那根主梁**。`set-citang-huang-qiang-l1` 左上角斜過一段深色主梁（約 x 0–540、y 0–190）。s07 梁頭已經壓在許硯肩上、s11 梁已經放倒在地上，腰以上的中景會把牆頂那段梁照畫進去：s07 畫面裡兩根梁（兩根長東西），s11 梁根本沒拆 | 第 19 條；第 32 集 fix2（長東西第一格不相連） | 免費做一張不含梁的牆：例如從 `set-citang-ye2-l1` 取 `crop=432:242:880:88`（梁右段下方、牌位頂上方那塊燭光牆；要全尺寸看底緣有沒有切到牌位頂），或把 `-huang-qiang` 左上那段梁用旁邊的牆色柔邊塗掉，新 id 例如 `-ye2-qiang`；s07、s11 改送它，文字的「plain candle-warmed back wall」不用改 |
| 33 | s32、s33 | **場景本身的麻繩會跟閘繩連成一條**。`set-shentan-an-l1` 左邊有一條粗麻繩，從矮木架左柱頂（約 x 470、y 90）斜拉到左邊岸上（約 x 0、y 430），就在石階缺口的左上方。石木匠站在缺口、兩手握閘繩、側面往後仰（往畫左仰），他手上的繩跟場景那條繩在第一格就會疊在一起；模型很可能讓他拉的是木架上那條，閘門拉不起來，鉤子讀不出（第 32 集鋤頭柄與扁擔畫成一根就是這樣） | 第 32 集 fix2；第 19 條 | 免費把 `-an-l1`（與 `-chen-an-l1`）左邊那條繩用旁邊的岸土色柔邊塗掉，做新 id（例如 `-an2`、`-chen-an2`），s31–s33、s36、s37（與 s29）改送它；文字不再提那條繩。若不塗，至少在 s32、s33 加一句實寫的位置：`the old rope slanting down from the low frame lies along the bank at the far left, well apart from him`，並把閘繩寫成短的 `a short thick rope from the top of the gate up to his hands` |
| 33 | s34 | **沒有人的鉤子鏡多了一句「畫面裡每個人穿布鞋」**。s34 的 d1 有 `Every person in the frame wears dark cloth shoes on both feet.`（全景通用句；第 32 集沒人的 s32 沒有這句）。這一鏡寫的是 `only the wheel, its frames, the pond, the stone edge and the fields are in the frame`，再加一句「每個人」等於邀人入鏡，岸邊多一個人就毀了這個揭曉 | 第 18、34 條；第 32 集 s32 的寫法 | `mkspec.py` 對 s34 加一條 `replace`：`["Every person in the frame wears dark cloth shoes on both feet. ", ""]`；重跑 mkspec 與 prep，再掃一次確認 s34 沒有 `Every person` |
| 33 | `D0`、`E0`、`E1`（s12–s40 的 28 支） | **場景句寫「溝底的深潭」，圖是平地上的潭**。三句都寫 `At the deep pool in the gully below the dry fields of Liuxi`；兩張潭圖都是一片平的旱田，潭在地面上、四周石邊、沒有溝谷。全景 s12、s28、s34 最可能照文字把潭拉進一道溝裡，或把旱田抬高成坡 | 第 19、42 條；第 32 集審稿必改 5（背景文字跟送的圖不合） | 三句改成 `At the deep pool on the flat dry fields of Liuxi …`；`LOC["gd_g"]`／`["nn_g"]` 的 `the dry furrowed field above the pool` 改成 `beyond the pool` |
| 33 | s12 | **群眾寫了集合名詞**：`WORKERS … standing about in a loose crowd` | 第 34 條（不寫 crowd、villagers 這類集合名詞） | 改成 `standing about here and there on the sand`（九個人已經逐一寫了） |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 33 | s25（風水先生的位置） | s19、s21 風水先生都在錢員外右邊（錢員外朝左，身後是右）；s25 他變成畫左緣的黃袖子，中間只隔 s24，人換了邊 | 接戲 | s25 用 `FENG_EDGE_R` 的寫法改成 `at the right edge of the frame, cut by it, soft, only one wide mustard-yellow sleeve of a tall thin man already walking out beyond the right edge`，錢員外跟著往右走、從右肩回頭（必改 3）。稿子「跟著走出畫面右」也照得到 |
| 33 | s22 | 二牛 `in front at the left … his face turned back over his shoulder toward the men behind him`：說話的人轉頭看景深裡的人，臉會轉離鏡頭；另外韓伯的竹杖、兩人合抬的木料、二牛的木槌三根長東西在同一個中景 | 第 31 條（臉朝鏡頭可見）；第 32 集 fix2 | 二牛改 `his face in profile to screen right, turned toward the two men behind him at the right`；木料句加 `held low behind them, well apart from the staff` |
| 33 | s13 | 秦霜竹竿 `its far end held out low toward the left` 再從左到右一劃，背後的 `-gongdi-mu` 是一堆長木料與兩根高木架的柱子，竿子低低掃過去會跟木料、柱子疊成一根（第 32 集 fix2 同類） | 第 32 集 fix2 | 第一格竹竿豎著（`held upright in her right hand, its foot on the boulder`），動作改成竿頭在她頭頂的天空裡從左到右一劃；或改低角度讓竿子背後只有天 |
| 33 | s15 | s12、s13 秦霜右手有竹竿，s15 沒寫，加上 `HANDS` 句竹竿就消失 | 接戲（道具每鏡同一件） | 加 `{BAMBOO} held upright in her right hand, its top beyond the upper edge of the frame`（背景是天與高木架頂梁，竿子寫在人的右邊、離木架遠一點） |
| 33 | s29 | 石木匠在右、朝左，右手（離鏡頭那隻）拍許硯的背；許硯面向他，背在另一側，要繞過去才拍得到，模型常畫成拍胸或手穿過身體 | 第 32 條（手在不越過身體那一側） | 改 `claps Xu Yan once on the shoulder with his flat right hand`（稿子「拍在背上」改肩，意思一樣） |
| 33 | s05、s07（放梁） | (1) s05 木梯寫在 `against the back wall at the right, under the right end of the beam … on the flagstones`，但夜版全景右邊整片後牆前就是供桌（一直到右緣），梁的右端在畫外右上：木梯只能立在供桌上或供桌前，跟台詞「別砸了供桌」打架。(2) 全集沒有一格看得到梁離開牆頂，s07 中景只拍到一根粗木頭壓在肩上 | 第 19 條；鉤子要讀得出（第 32 集 fix2） | (1) 木梯改 `standing on the flagstones just beyond the right end of the altar table, clear of it`，或改到供桌左端外、梁的左段下面；(2) s07 加 `the long dark beam slanting up out of the upper right corner of the frame`，讓人看得出是整根梁在往下放（只有這一根長東西，木梯不入鏡） |
| 33 | s33、s36 | 送 `-an`，右緣就是輪子與輪架；提示詞卻寫 `that side of the frame is only {SIDE_STONE}`（石邊與綠水）。s33 寫水衝向畫右外的輪子，圖上輪子就在畫裡 | 第 19 條 | s33、s36 的 `SIDE_STONE` 改 `the stone edge, the water and the near rim of the still wheel at the very edge`（s33 水衝過去看得到輪子，也幫鉤子讀）；s37 朝左，那一側照舊 |
| 33 | `LOC["ye"]`、`["ye_men"]`、s10 | 夜版門洞裡跟黃昏版一樣，是一條門廊與另一扇格子門（只是壓暗了），不是夜空；文字寫 `the dark night beyond them`、`beyond them only the blue-black night`，模型可能另開一片夜空（第 32 集審稿建議對 `-huang-men` 已經改過黃昏版） | 第 19 條 | 改 `beyond them a dark passage and another lattice door, blue-black with the night` |
| 33 | s34 | 輪輻左右對稱，轉半圈前後兩格一樣；只有「動起來、慢下來、停住」讀得出，「半圈」靠錢員外的台詞 | 鉤子要讀得出 | 走必改 1 的 A（有葉板就看得出轉了多少）；B 的話動作句加 `the water slaps white against the bottom of the rim … the spokes sweep slowly round, slow, and stand still`，6 秒照舊、挑片時看停住後的兩秒不再動 |
| 33 | `-an`、`-gongdi-an`、`-chen-an`；`-geng`、`-gongdi-geng`、`-tian` | 放大看：`-an` 一族左上角（約 x 40–90、y 90–120）是一座**輸電鐵塔加電線**的小影子；`-geng` 一族與 `-tian` 的地平線上有幾根細的豎桿。裁切是兩倍放大，現在很糊，但模型重畫時可能畫清楚（第 31 集挑片就說過「地平線有幾根細小的豎線」） | 第 13 條（宋代）；第 14 集「挑圖要放大看全圖」 | 跟必改 4、5 的免費圖一起做：用旁邊天色柔邊塗掉鐵塔與豎桿，再全尺寸看；不做的話挑片時看 s14、s16、s22、s24、s26、s29、s31–s33、s36、s37、s19–s21、s25、s39、s40 的遠景有沒有長出電線桿 |
| 33 | s01 | (1) 跪著的八人沒寫手（第 32 集實拍 s36 是兩手按在膝上）；(2) 韓伯寫 `at the front of them by the altar`，第 32 集 s36 實拍他在門與村民中間、離供桌有一段 | 接點 32→33；「背景人寫手上拿什麼」 | 村民加 `their hands resting on their knees`；韓伯改 `kneeling in the middle of the floor in front of them`，竹杖句照舊（靠在供桌邊；第 32 集實拍看不到竹杖，可以） |
| 33 | s19 | 錢員外與風水先生很小，`-gongdi-geng` 前景有三根高木架的柱子，小人容易站在柱子後面或跟柱子疊在一起 | 第 34 條（人數讀得清） | 加 `standing in the gap between the middle and right posts of the tall frame` |
| 33 | s17 | `-gongdi-mu` 的下半是潭水與石邊，從她背後拍、「站在沙岸上」會讓模型把她擺在石邊或水上 | 第 19 條 | 改 `standing on the stone edge of the pond`，或拍法照舊、挑片看腳下 |
| 33 | 參考圖（秦霜、小禾） | `refs-live/angles/` 有 `qinshuang-angle-a/b-l1`、`xiaohe-angle-a/b-l1`；第 32 集送過秦霜 angle-a，本集全部只送 l1。FOOT 寫「秦霜沒有角度圖」「小禾送角度圖」，兩句都跟實際不符 | 第 32 集審稿機械表；FOOT 要跟 spec 一致 | 近景與中景（s13、s15 秦霜；s23、s26 小禾）加送 angle-a（不笑的鏡不送 angle-b）；不加就把 FOOT 的兩句改成「秦霜、小禾只送 l1」 |
| 33 | 聖經〈接點〉33→34 | 表上寫「水車在右」「錢員外在右上田埂」；挑定的 `set-shentan-l1` 輪子在畫面中間偏左，沒有高起的田埂，錢員外站在高木架右邊遠處的田邊 | 聖經〈接點〉開頭：照圖改這張表 | 33→34 那列改成「水車在畫面中間偏左、轉半圈停住；錢員外在高木架右邊遠處的田邊」，第 34 集 r2.py 照這個寫；必改 1 選 A 或 B 也一起寫進〈道具〉水車列 |

## 接受（看過、不用改）

- **接點 32→33**：第 32 集 s36 實拍是胸口高的全景、門在左、許硯站在門內、右手圖卷、韓伯跪在中間回頭、村民跪在右半臉朝門口；s37 許硯在門口腰以上、圖卷在腰前。s01 送同一張 `set-citang-huang-l1`、同一個機位，第一格許硯已經跨進門一步、圖卷橫在腰前、往右走，村民臉朝他。實拍裡長得像韓伯的是穿暗橄欖綠的灰髮老漢，本集照審片把老漢改成布包頭短灰鬚；同一刻跨集換了樣子，觀眾不會在意，接受。實拍門口兩個人影（REVIEW 3 模糊掉的石木匠與二牛）本集不寫，接受。
- **第一場軸線**：門在左、供桌在右；s02、s04 從供桌左端拍側面跪拜、臉朝畫右的牌位（第 32 集 s34–s35 用 `-zuo` 實拍成功過）；s04 許硯在左、韓伯在右，許硯轉頭看他仍朝畫右，臉看得到；s06 二牛順著繩子朝畫右上（自審改過的越軸是對的）；s08 許硯轉向畫右、s09 過肩許硯背在左、石木匠在右朝左、s10 反打石木匠背在右、許硯在左朝右、s11 石木匠朝左。過肩前景都是不點名、不送圖的背影。
- **第二場軸線**：潭在前、工地與壯丁在左岸、秦霜在右邊大石上朝左（s12、s13）；s14 二牛朝右上、s15 秦霜朝左下、s16 許硯朝右看大石；s17 背影唐小棠正中、石木匠右三分之一朝左，s18 石木匠朝左；s19–s21 錢員外在右邊遠處田邊朝左、風水先生在他身後（右）；s23 小禾朝右上田邊；s26 小禾朝左桌邊的許硯（s16 許硯在左）。
- **第三場軸線**：村民在左邊石邊、水車在他們右邊；s31、s36 韓伯朝右看輪子；s32 石木匠在左閘邊、許硯在右；s33 側面朝右；s37 秦霜朝左喊閘邊的石木匠、s38 石木匠在輪架上朝左回她（中間他從閘邊跑到輪子，照稿子 2026-11-06 的修改，剪在動作外）。
- **拿東西的手**：s09 石木匠朝左、左手（靠鏡頭）握圖卷、右手拍梁；s10 許硯朝右、右手（靠鏡頭）按梁；s11 左手夾到左腋；s14 二牛朝右、木槌在右肩（靠鏡頭）；s20 風水先生朝左、羅盤在左手（靠鏡頭）；s23 小禾朝右、右手紙風車；s31 韓伯朝右、右手舉杖。都不越過身體。
- **道具每鏡同一件**：圖卷 `ROLL`（s01、s09、s11，紙背朝外）、羅盤 `COMPASS`（素面一根針）、麻袋 `SACK`、鐵釘、紙風車 `PINWHEEL`（s23、s26、s27、s31、s37 一字不差）、木槌 `MALLET`、閘門 `SLUICE`、冊子闔著、竹竿光的；兩把木梯（祠堂、水車）分在不同場。
- **不笑的鏡**：二牛 s06、s14、s22 寫咬牙、皺眉；可以笑的只有 s16 許硯一點笑意、s17 不拍臉、s21 錢員外冷笑、s24 二牛、s26 小禾、s29 石木匠一點、s39–s40 錢員外，都照稿子。
- **系統與心裡話**：s08、s16、s30 不寫淡藍光、面板剪接時疊；s16、s30 `SILENT_HE`；畫外句不補（`OFFSCREEN_SPEECH = False`）。
- **風水先生**：照聖經〈小角色〉改稿子 c20 的正面中景為側面全景、c19 錢員外在前；聲音 Charon 寫在 `MINOR`；不改共用檔。
- **時間與光**：第一場 s01–s04 黃昏、s04→s05 剪接入夜；第二場合成正午一種光（同一張圖）；第三場 s27→s28 換成立好的水車、s30→s31 清晨到正午，都在剪點。
- **BUY**：s08、s16、s30 買 10 秒；s32 五字 5 秒；s01、s34 沒台詞 6 秒；其餘 6／8 秒照字數與慢的人估。錄音後照 `span932.sh` 重核，照 PREP 寫的流程。
- **d1 前置的其他寫法**：s27 插鏡天空只當顏色、拿掉地點句；s01、s04 韓伯跪著沒有竹杖（身分句拿掉 staff）；s12、s31 秦霜皮靴句；only 句點名畫裡不具名的人（s01、s09、s10、s17、s19、s21、s25）。

## 小結

- **必改 8 條**：(1) 圖上的水車沒有葉板，文字卻寫十二片葉板、三鏡的手按在葉板上、s34 的水打在葉板上：開拍前要選，A 花一點點數加葉板重做 `set-shentan-l2` 與裁切（第 34 集也要），B 免費把文字改成輪緣與輻條；
  (2) s30、s35 的 `-lun` 輪子在左、右緣是田與柱，手按「右緣的葉板」不成立：改送輪子在右的免費新裁切（或 `-chen-an`／`-an`）；(3) s25 錢員外往右走、從左肩回頭會背對鏡頭：改右肩（comp 與 `GAZE_REFINE`）；
  (4) s07、s11 的素牆裁切左上角就是主梁，梁同時在肩上與牆頂：免費做不含梁的牆；(5) s32、s33 的 `-an` 左邊有一條場景麻繩，會跟閘繩連成一條：免費塗掉；
  (6) s34 沒人的鉤子鏡多了「每個人穿布鞋」：mkspec 拿掉；(7) 場景句寫「溝底的深潭」，圖是平地上的潭：改 `on the flat dry fields`；(8) s12 寫了 `crowd`：改掉。
- **鉤子**：s33 拉閘（側面、一個動作）與 s34 轉半圈停住（固定、結果先寫）的寫法對，但都被上面的圖文不合拖累（麻繩、葉板、布鞋句）；s05 放梁要靠三鏡連起來，建議 s07 拍出整根梁斜出畫面。
- **建議 15 條**：s25 風水先生換了邊、s22 二牛回頭看景深、s13 竹竿低掃過木料、s15 竹竿消失、s29 拍背改拍肩、s05 木梯會立在供桌上、s33／s36 那一側其實有輪子、夜版門洞是門廊不是夜空、s34 對稱輪輻、遠景的電塔與豎桿、s01 村民的手與韓伯的位置、s19 小人站在柱子之間、s17 腳下、秦霜與小禾的角度圖、聖經 33→34 接點照圖改。
- 台詞逐字、面板、d1 清單（雜湊、分隔句、兩種子一致、送圖絕對路徑）、人數、會長字與兵器與泥的詞、唐小棠背影、風水先生小角色、二牛不笑、秦霜不寫柴刀與旗、接點 32→33，都通過。
- 照必改改完後要做：做免費圖（不含梁的牆、塗掉麻繩與電塔的 `-an2`／`-chen-an2`、輪子在右的 `-lun2`／`-chen-lun2`，選 A 的話先做 `set-shentan-l2` 再全部重裁），全尺寸看、寫進 refs-live README；改 `r2.py` → `build933.sh` → `mkspec.py`（s34 布鞋句、新 id 的 `PLACE`）→ `prep933.sh`，再掃一次 d1：沒有 `crowd`、`gully`、s34 沒有 `Every person`、s25 是 `right shoulder`、（選 B 的話）沒有 `paddle`。
