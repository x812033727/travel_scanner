# 第 34 集重製版 r2（e034-r2，內部 934）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿：沒參與寫稿的獨立代理，2026-11-19，開拍前（d1 還沒跑、錄音還沒錄）。只寫這一個檔；沒改 `r2.py` 或別的檔、沒開 Colab／RunPod（沒碰 `zt-live3`）、沒用站台 TTS、沒 commit。
  沒讀前置代理的自審 `writer-tools/e034-r2/review.md` 與 scratchpad 的 `e934prep/PROGRESS.md`。
- 審的對象：`writer-tools/e034-r2/r2.py`、`docs/videos/zhong-tian-qu-qi-e034-r2/{script.md,video.json,overlays.json}`、
  d1 提示詞 `~/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live/d1/prompts/*.txt`（80 支）與 `colab-jobs.json`、`colab/runs/e934-live/{mkspec.py,PREP.md}`、
  `colab/runs/e934/extras.json`、`hailuo/{clips,ff}-dh-e934.json`、`hailuo/gen-dh.mjs` 的 `SET` 表、`live-action/free-e031-e040/shentan_xi.sh`。
- 對照：`r2-bible-e031-e040.md`（拍法 1–43、〈接點〉33→34 與 34→35、〈道具〉水車列與蝗群列、〈人物〉〈小角色〉〈場景〉、〈原版必修〉第 34 集）、
  第 33 集 `writer-tools/e033-r2/r2.py`（s35–s40）與 `review-independent.md`（格式與通則）、第 23 集 `colab/runs/e923-live/mkspec.py`（逐鏡換掉 extras 的 clear-air 句的前例）。
- 參考圖全尺寸打開看過：`set-shentan-l3`、`-an-l3`、`-bian-l3`、`-lun-l3`、`-tian-l3`、`-shi-l3`、`-xi-l3`、`-xi-an-l3`、`-xi-lun-l3`、`-xi-ye-l3`、`set-shentan-qu-xi-l1`；
  `set-hantian-l1`、`-geng-l1`、`-tian-l1`、`-liu-l1`、`-di-l1`、`-hui-l1`、`-hui-tian-l1`、`-hui-geng-l1`。另在 scratchpad 放大看了 `set-hantian-l1`、`-tian-l1`、`-liu-l1`、`-di-l1` 的地平線，
  也用 ffmpeg 試裁了一張較寬的大石框（必改 2），看完都刪了。
- 接點 33→34：第 33 集成片還沒有（`_live-e933/` 不存在；`e933-dh/runpod/live/d1/out` 只跑到 s09），只能對照第 33 集 `r2.py` 的 s35、s40 的文字與送的圖。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| 台詞 | `video.json` 40 句都能在 `script.md` 原文裡逐字找到，id 不重複；40 鏡＝c01–c40 |
| 面板 | `overlays.json` 只有 s08「旱災任務，今日日落到期」、s33「旱災任務完成，稻種保住」，跟系統念的一字不差；本集沒有好感變化 |
| d1 清單 | 80 支（兩種子各 40）、共 564 秒；兩種子的提示詞去掉種子後逐鏡一樣；每支 `never the mood. `、`One continuous shot.` 各剛好一次；BUY 加總 282 秒，跟 `colab-jobs.json` 的秒數逐鏡相符（s24、s26 5 秒，s01、s23 6 秒） |
| 送圖與點名 | 許硯 angle-b 全集沒送；全景 s19 只送許硯 l1；s08、s09、s33 先 l1 後 angle-a；阿令 angle-b 沒送、全景 s14 只送 l1、s36 s38 先 l1 後 angle-a；錢員外 angle-b 沒送、全景 s30 只送 l1；s03、s23、s24、s26、s40 不送人；場景圖逐鏡照 `PLACE` 表換成絕對路徑 |
| 田與渠的潭字 | s26–s40 的 d1 提示詞**沒有** `pool`、`pond`、`deep pool`；s26 的地點句換成 `On the flat dry fields of Liuxi … beside a new dry earthen channel`（見逐一判斷第 3 項） |
| 人數 | 全景都寫 exactly N 且跟描述的人對得上：s12 七人（一班四、二班二、秦霜）、s15 四人、s19 五人、s26 四人、s27 三人、s30 三人、s40 三個背影；有名字的臉每鏡最多三張（s19 石木匠、秦霜、許硯） |
| 會長字／兵器／泥／open | 沒有 `mud`、`caked`、` open`、`crowd`、`villager`、`chopper`、`smoke`、`storm`、`bucket`、`trough`；`cloud` 只在 s27 的 `cloudy brown water` |
| 道具每鏡同一款 | 鐵錘只在 s13（許硯手上）、木槌只在 s19（石木匠）、竹籃只在 s14–s15、紙風車 s01 s02 s03 s14 s15 s22 s34 s37 同一句、閘門與閘繩只在 s20–s22 同一句；水車每鏡同一句 `exactly as in the picture … twelve flat wooden paddles`，送的都是 `set-shentan-l3` 一族 |
| 韓伯的竹杖 | s07 右手拄著；s20 左手、離鏡頭那側、跟繩子 `well apart`；s21 不在框裡（身分句的竹杖拿掉）；s22 靠在閘邊石沿、離繩子遠；s27 丟在田埂草上；s28、s29 不寫 |
| 布鞋句 | 只在全景 s12、s14、s19、s26、s30；s12、s19 換成秦霜皮靴；s23（沒人）、s40（背影到肩）沒有 |
| 笑 | 寫了笑的只有 s14、s18、s25、s34、s35，加 s31 的冷笑（稿子 c31 准「本鏡可以冷笑」，見〈接受〉）；s30 寫 `not smiling`、笑容僵住臉發白 |
| 軸線 | s05／s06 許硯在左、石木匠在右（過肩背影一左一右上，接得上）；s20／s21 韓伯在左朝右、許硯在右；s28／s29 韓伯在左仰頭朝右上、許硯從右邊來；s30／s31／s32 錢員外在右（大樹下）、秦霜在他左邊朝右、錢員外往右走從右肩回頭；s35／s36 阿令在左、秦霜在右，s36 阿令再往左轉開＝轉離秦霜；s37–s39 北邊都在畫右，s40 主觀 |
| 視線句 | 對畫外、對葉板、日頭、水車、水、遠山說話的 18 鏡都在 `GAZE_REFINE`，d1 與精修文字同一句；精修文字開頭的 `3D CG` 跟第 33 集一樣（管線處理，不在本集範圍） |

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| (1) c35–c40 從潭邊改到田邊（為了遠山） | **合理，而且比稿子好**。看過圖：`set-shentan-l3` 的地平線是平的、只有一線淡樹影；`set-hantian-l1` 整條地平線都是遠山。台詞「蝗蟲過山了」要山，稿子場頭也寫「北邊的山在畫面右上」，在潭邊拍不出來。另一個好處是稿子本身 c27–c34 已經在田邊、c35 再跳回潭邊沒有交代，改了以後第三場後半一路在田邊、少一次跳。代價有三：(a) 阿令「是水光晃到妳眼睛了」原本靠潭面反光，田壟裡一薄層褐水的反光弱（建議 5）；(b) 連續 14 鏡都在那張金黃垂柳、紅樹的秋景圖上，聖經〈時間線〉寫早春、〈場景〉第 330 行還寫「第 34 集旱田挑圖時避開金柳與紅樹」，跟實際挑定的圖相反（建議 8）；(c) s37–s39 背景也有遠山，人卻朝畫右看「遠山」（建議 4）。都不推翻這個決定 | 建議 4、5、8 |
| (2) c24 竹斗改輪頂葉板帶水 | **合理，也是唯一照圖的寫法**。聖經〈道具〉水車列定了 `set-shentan-l3`：十二片平葉板、沒有竹斗與木槽，文字也不寫；看 `-xi-ye-l3`，輪頂就是五、六片平葉板對著天，畫得出「一片片轉上來、帶一片水往下瀉」。劇情上「水車把水提上來」改由這一鏡的畫面＋s26 渠水撐，觀眾讀得到。文字沒寫 trough、bucket（d1 掃過 0）。要注意兩件小事：s24 的地點句還寫「on the stone edge of the pond … standing in the pond」，跟「only the wheel and the sky」打架（建議 1）；s23 與 s24 的轉向沒寫，挑片時兩支挑同一方向。稿子說刪鏡先刪 c24，d1 讀不出就剪掉，不用補拍 | 建議 1 |
| (3) 田與渠的場景句帶 deep pool、`mkspec.py` 在 d1 拿掉 | **合理的權宜，d1 乾淨**。`gen-dh.mjs` 的 `SET` 表沒有田的樣式（`On the three small dry fields` 什麼都比不到），沒有 SET 圖就沒得 `swap_pictures`（`retake.py` 只能換或拿掉圖、不能加），所以要讓它先選到 `dh-set-shentan-t1` 再換。掃過：s26–s40 的 d1 一個 `pool`／`pond` 都沒有，s26 的 `At the deep pool …, beside` 換成 `On the flat dry fields …, beside`；`sluice` 雖然也比得到 `dh-set-xinqu-t1`，但 `deep pool` 排在前面、沒有問題。殘留在三個地方：`video.json`／`storyboard.md` 的人看的提示詞、`hailuo/ff-dh-e934.json` 的 s26–s40（CG 首格路線，真人版不用）、以及**之後的 fix／retake spec**——第 23 集 `fix1/spec.json` 是自己再寫一次 replace 清單的，fix 若沒帶 `POOLMARK`／`XQ_GEN` 的替換，「below the deep pool」會回來、模型會在田裡畫出潭 | 建議 6 |
| s01 接第 33 集 s35／s40 | 第 33 集最後一鏡是 s40 錢員外（`-tian-l3`，天空與高木架橫梁），第 34 集 s01 切回許硯，中間隔著集與集的斷點，換景別不算跳。但寫稿說「keeps s35's frame」不完全對：第 33 集 s35 是**近景、胸以上、兩手平掌**按葉板（`-bian-l3`），s01 是中景、腰以上、只有右手。聖經〈接點〉33→34 寫的是右手，跟第 33 集 `r2.py` 不一致。光、地點、許硯在左半朝右、送 `-bian-l3` 都接得上 | 建議 2 |
| s22 拉閘（鉤子） | 側面、兩手第一格已經握繩、一個動作，寫法對；但**閘門在框裡哪一側沒寫**，動作句又寫「the pond water rushing through it toward the wheel」——水車就立在潭裡，潭水穿過潭邊的閘「流向水車」說不通，下一鏡 s23 寫的又是水「沿石邊從左邊衝**進**潭裡」 | 必改 4 |
| s23 水車顛一下再越轉越快 | 固定鏡、結果先寫、整架輪子第一格就在、不送人、沒有布鞋句，跟第 33 集 s34 同一套。葉板外伸、不對稱，比第 33 集的直輻條好讀「顛四分之一圈」。`side-on` 與圖上看到的是輪子正面有點歧義，第 33 集 s34 同一句、接受 | 接受 |
| s40 蝗群 | 照聖經〈道具〉的正面寫法（無數小黑點組成的低褐黑帶子、壓過遠山、前緣散開），不寫煙與火山的否定句，對。**但每支 d1 都帶 extras 的「the air is clear and still, a clean natural film image」**，正好叫空氣乾淨、什麼都沒飄；遠處 960×544 的「無數小黑點」本來就容易糊成一片煙，再加這句更難 | 必改 1 |
| 送的圖跟文字合不合 | `-xi` 一族：調色比較像暖色濾鏡，天還是淡藍、日頭還高、影子是正午的短影；`SUNSET` 不寫影子長度是對的，讀起來像金黃的傍晚前，可以接受。`set-shentan-qu-xi-l1`：橘與黑、對比極重、田壟巨大，很 CG（README 記過）。`set-hantian-*`：秋葉大柳樹、田是乾的，水寫在文字（PREP 第 5 節已列）。`-hui` 一族：讀起來像入夜前的藍灰，天是乾淨的，蝗群只能靠文字。**`-shi-l3` 比例不對、許硯站的地方是水**（必改 2）；`-tian-l1`、`-liu-l1` 地平線上 delogo 留下看得到的灰色柔邊方塊（建議 7） | 必改 2、建議 7、9 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 34 | s40；s01、s02、s03、s34（s38 順手） | **extras 的 clean 句「the air is clear and still」跟劇情要的東西打架**。s40 要空中壓過一條小黑點組成的帶子，這句叫空氣乾淨靜止；s01–s03 的戲是「一陣熱風把紙風車吹得呼呼轉」（倒著轉是整集的起點）、s34 是「風車轉對了」，`NOON` 也寫 `a hot dry wind`，同一支提示詞前面要風、結尾說空氣靜止。模型會把風車轉慢或不轉、把蝗群洗掉 | 〈原版必修〉第 34 集（蝗群）；聖經〈道具〉紙風車列（c01–c03 倒著轉、c34 轉對了）；第 23 集 `e923-live/mkspec.py` 的 `CLEAR` 逐鏡替換前例 | `mkspec.py` 加一組逐鏡替換：`CLEAR = "the air is clear and still, a clean natural film image"`；s40 → `"a clean natural film image"`（只留這半句）；s01、s02、s03、s34 → `"the air is clear, a steady wind blowing, a clean natural film image"`；s38（阿令「風是冷的」）可一起換成 `"a cold wind rising, a clean natural film image"`。`prep934.sh` 的檢查改成這五、六鏡沒有 `clear and still` |
| 34 | s10、s18（`set-shentan-shi-l3`） | **大石框的比例放不下人，s10 許硯「在大石腳下、畫面左半」那裡是潭水**。`-shi-l3` 是 `set-shentan-l3` 裡 560×315 的一小塊放大 2.34 倍（`shentan_xi.sh`：`560:315:752:421`），大石佔滿右下三分之二、石頂在全高約 23%；s10 要秦霜在石頂「膝以上」、s18 也是膝以上，石頂上面只剩約 170 像素，照圖畫不下，模型只能縮石頭或把人擺到旁邊。s10 又寫許硯 `at the foot of the boulder in the left half of the frame … framed from the waist up`，圖的左半是綠水與石牆，他會站在水裡。這張也因為放大太多，看起來過銳、過飽和 | 拍法 29、42（場景圖說了算）；第 33 集獨立審稿必改 7（位置句照圖）；拍法 19（新圖一律新 id） | **免費**：在 `shentan_xi.sh` 加一個較寬的框，新 id，例如 `c "$A" set-shentan-shi2-l3 800:450:512:286`（我在 scratchpad 試裁過：左邊是輪子右下的葉板與輪架、中間是石牆上方的沙岸與高木架兩根柱、右邊大石約佔全高四成、石頂上方留得出人），`mkspec.py` 的 `PLACE` 把 s10、s18 改送它，README 記一行。s10 的位置句改成：`at the foot of the boulder, on the flat sandy bank just behind the stone edge in the middle of the frame, {XU_WORN}, framed from the waist up`；`beside them, soft, the lower paddles of the still wheel at the left edge and the posts of the tall frame` 照新框不用改 |
| 34 | s30 | **「從田裡往上拍高起的田埂」跟圖與聖經不合**。`cam="Wide shot, low angle"`、comp `wide shot from low in the field, looking up at the grassy bank`、`looking down toward the water in the furrows below`；送的 `set-hantian-liu-l1` 是人眼高、平的長草田邊，沒有高起的埂。聖經〈接點〉33→34 已改成「圖上沒有高起的田埂」，本檔 docstring 也寫「no raised field ridge」，本集 s19 也照這個原則把稿子的低角度「照圖的高度」——只有 s30 沒照 | 第 33 集獨立審稿必改 7；拍法 29、42；本集 s19 的寫法 | `cam="Wide shot, slow push in"`；comp 開頭改成 `wide shot at standing eye height across the furrows toward the grassy bank under the big old tree at the right, like the picture:`；`looking down toward the water in the furrows below` → `looking toward the water in the furrows before him`；`GAZE_REFINE["s30"]` 同步改成 `his face three-quarter to screen left toward the water in the furrows before him, his eyes on it`。zh 的「低角度，從田裡往上拍」改「照圖的高度」 |
| 34 | s22 | **鉤子的閘門沒有位置、水從哪來寫反了**。comp 只寫韓伯 `in the left foreground at the narrow gap … his face toward the gate`，閘門在框裡哪一側沒寫；motion `the sluice gate is pulled up out of the gap, the pond water rushing through it toward the wheel`：水車立在潭裡，「潭水穿過閘流向水車」說不通，下一鏡 s23 寫的是水 `rushing along the stone edge from the left into the pond under the wheel`。鉤子要一眼讀得出「拉起閘板→水衝出去」 | 原版必修第 33、34 集（拉閘、水車轉）；第 32 集 fix2（鉤子側面、結果先寫）；接戲 s22→s23 | comp：`… gripping the thick rope tied to the top of the small wooden sluice gate of three plain wet planks set upright in the narrow gap between the two flights of stone steps just beyond him …`（`-xi-an-l3` 兩段石階中間正好有那道暗缺口）；motion 改成 `Elder Han throws his weight back on the rope, the sluice gate is pulled up out of the gap and a white rush of water pours through the gap toward the wheel at the right; {quiet('Elder Han')}`（拿掉 `the pond water`） |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 34 | s24 | 地點句 `xi_c` 寫「on the stone edge of the pond beside the big wooden water wheel …, standing in the pond against the far stone edge」，構圖卻是輪頂對天、`only the wheel and the sky are in the frame`；送的 `-xi-ye-l3` 也只有天與輪頂。地點句會把鏡頭往下拉出潭與石邊 | 拍法 35（只拍道具的插鏡不寫地點句；這鏡是沒有人的特寫，同一個道理） | 加一個 `xi_e = f"{X1}; {SUNSET}"`（照 `nn_e`、`af_e`），s24 改用它；`WHEEL` 句不必帶 |
| 34 | s01 | 接點：第 33 集 s35 是兩手平掌按葉板、近景；s01 是右手、中景。聖經〈接點〉33→34 寫右手，跟第 33 集 `r2.py` 不一致；`flat right hand … slowly tightens on the paddle` 平掌「收緊」也有點自相矛盾 | 〈接點〉；拍法 32 | 先照第 33 集 `r2.py` 改成 `both flat hands still resting on one wet wooden paddle`，動作 `his fingers slowly curl against the paddle`；中景保留（小禾的手要在左下角）。第 33 集成片後照實拍（哪隻手、景別）再核一次，並把聖經〈接點〉那格改成跟實拍一致 |
| 34 | s12 | 秦霜喊「第一片下來了」，左前景卻已經疊著「三片拆下的葉板」（稿子 c12 前景的寫法，本身就跟台詞矛盾）；另外一班四人齊腰站在水裡，`Qin Shuang wears her leather boots and every other person … dark cloth shoes` 叫水裡的人也要畫鞋 | 接戲；第 33 集獨立審稿必改 6（看不到腳的不寫鞋） | 前景改成 `three new plain wooden planks lying in a low stack`（新料，不是拆下的葉板），或整句拿掉；鞋句改成 `Qin Shuang wears her leather boots and the two men on the stone edge dark cloth shoes on both feet.`。s19 同理（三班兩人齊腰在水裡）：`Qin Shuang wears her leather boots.`；s19 秦霜及膝、旁邊的人齊腰，可寫兩人 `a step further out` |
| 34 | s37、s38（s39） | 背景寫 `only the darkening grey sky and the far hills`，人卻朝畫右看「the far hills beyond the right edge」：山同時在背後又在畫右。s38 的 comp 第一格已經朝右，motion 又寫 `turns her head sharply toward the hills`，模型會先把她轉到別處再轉回來 | 拍法 32（前置動作第一格完成）；〈接點〉34→35（近景裡北邊是畫右） | s37、s38 背景改成 `only the darkening grey sky`（`-hui-tian-l1` 上半本來就是天；低角度、胸以上的框山會在下緣外）；s38 motion 改 `A-ling tilts her head sharply to listen and holds still as she speaks`。s39 背景已經是田與屋，不用改 |
| 34 | s35、s36 | 搬到田邊以後，「水光映在臉上」「水光晃到妳眼睛」的水只剩田壟裡一薄層褐水，`-geng-l1`／`-di-l1` 是乾的 | 逐一判斷 (1)；台詞要讀得通 | s35 前景寫成 `at their feet the brown channel water running in along the nearest furrow, glinting in the low sun, its rippling light playing on their faces`；s36 背景 `the brown water running along the furrows, glinting in the low golden light`。d1 若兩支都看不出水，fix 用 PREP 第 5 節第 2 項的 `set-hantian-shui-l1`（Qwen 只改一件事，約 **1.5–2 CU**），s27、s29、s34、s35、s36 一起受益 |
| 34 | fix／retake、`video.json` | d1 的潭字拿得乾淨，但 fix spec 若自己重寫 replace 清單（第 23 集 `fix1/spec.json` 就是這樣），沒帶 `POOLMARK`／`XQ_GEN` 會把「below the deep pool」帶回 s26–s40；`video.json`／`storyboard.md` 的提示詞也還寫著，之後的人照抄會誤會 | 逐一判斷 (3)；第 33 集必改 7 | PREP 第 6 節加一條：「s26–s40 的每個 fix／retake spec 都要帶 `[R2.POOLMARK, ""]` 與 `[R2.XQ_GEN, R2.XQ_LIVE]`，`prep` 的『田裡沒有潭字』檢查照跑」；`storyboard.md` 表頭加一行說明這是給 `gen-dh` 的 `SET` 用的字 |
| 34 | `set-hantian-tian-l1`（s28、s33）、`-liu-l1`（s30–s32）、`-di-l1`（s36） | `hantian_crops.sh` 的 delogo 在地平線留下看得到的灰色柔邊方塊：`-tian-l1` 約 x 545、850、1020（y 440–490）三塊，`-liu-l1` 約 x 180、y 420 一塊，`-di-l1` 上緣兩塊。不是暗方塊，但模型可能補成一根竿、一個人影或一團霧 | 拍法 33（免費塗掉要用旁邊同材質接過去、柔邊，不能留方塊） | **免費**：在 `set-hantian-l1` 上改用旁邊的樹列與田的紋理接過去（例如 OpenCV `inpaint` 或從左右各取一段同高的地平線覆蓋，柔邊），重做所有裁切與 `-hui` 調色，`prep934.sh` 的逐位元比對跟著更新。不擋 d1：草稿那個位置長東西的就不挑 |
| 34 | 聖經〈場景〉第 330 行、〈時間線〉第 124 行 | 聖經寫「第 34 集旱田挑圖時避開金柳與紅樹」、時令是早春冒芽；實際挑定的 `set-hantian-l1` 右邊就是一整棵金黃垂柳、遠處紅樹。本集 14 鏡都在這張圖上 | 拍法 19（參考圖壓過文字） | 聖經改成實情（「`set-hantian-l1` 有金柳與紅樹，挑圖時接受，文字不寫葉色」），免得第 35、39、40 集的人照文字以為圖上沒有。改圖（Qwen「大樹與遠處的樹變光禿枯枝」約 **1.5–2 CU**，第 35、39、40 集的 `-yang`、`-shou`、穀倉也要重做）我同意 PREP 的判斷：**不改** |
| 34 | s26（`set-shentan-qu-xi-l1`） | 橘與黑、對比極重、田壟巨大，跟前後鏡的寫實潭邊和田接不起來；渠是中間一道黑影，讀不讀得出「渠」要看草稿 | 第 32 集 fix3（橘光下的材質會變成金箔感）；README 記過「很軟、偏 CG」 | 免費先試：`shentan_xi.sh` 對 `-qu-l1` 用比較輕的調色（降對比、降飽和，不加 `colorbalance` 的紅），新 id；d1 讀不出就照稿子刪 c26（「要刪鏡先刪 c24、c26」）。重畫約 **1.5–2 CU**，不建議 |
| 34 | s40 | 文字寫得對，但 960×544 的遠景「無數小黑點」最可能被畫成一團褐色煙或沙塵 | 原版必修第 34 集 | 同意 PREP 第 5 節第 5 項：d1 兩支都像煙就先用免費合成的參考（在 `-hui-l1` 遠山上用 Pillow 撒小黑點組成帶子，前緣散開），新 id；必改 1 的 clear-air 句先改掉再看 |
| 34 | s14 | 小禾 `toward the wheel beyond the right edge of the frame`，送的 `-an-l3` 右三分之一就是輪子 | 拍法 29 | 改 `toward the wheel at the right of the frame`；`GAZE_REFINE["s14"]` 同步 |
| 34 | s10、s18 參考圖 | 必改 2 若不做，至少把 s10、s18 的 `framed from the knees up` 改成 `framed full figure, small` 讓模型照圖的比例 | 拍法 29 | 只在必改 2 沒做時用 |

## 接受（看過、不用改）

| 項目 | 為什麼 |
| --- | --- |
| c35–c40 改到田邊 | 見逐一判斷 (1)：只有田的圖有遠山，台詞要山；還少一次潭↔田的跳 |
| c24 改輪頂葉板帶水 | 見逐一判斷 (2)：聖經定的水車沒有竹斗與木槽；`-xi-ye-l3` 畫得出 |
| deep pool 給 `SET`、mkspec 拿掉 | 見逐一判斷 (3)：`gen-dh` 的限制下唯一能送田的圖的辦法，d1 已乾淨 |
| 錢員外、家丁、秦霜柴刀、阿令 | 錢員外只在 s30–s32、胸前素面、`not smiling`；家丁只在 s30 遠景、空手；秦霜柴刀全集沒寫；阿令不戴面巾、長袖蓋腕、木簪、送 `aling-portrait-l1` |
| s31 秦霜冷笑 | 提示列的「可以笑」沒有 s31，但稿子 c31 明寫「本鏡可以冷笑」，`cold curl at one corner of her mouth` 不是笑場的笑 |
| 系統與心裡話（s08、s09、s33） | 全程嘴閉著、`SILENT_HE`、不寫淡藍光、面板交給剪接；BUY 10 秒放得下（約 24–28 字加停頓） |
| BUY | 照第 33 集量到的語速逐鏡算過：最緊的 s12（秦霜 16 字約 4.4 秒）、s22（小禾 11 字加刪節號約 4.5 秒）、s34（14 字約 4.2 秒）、s36、s38（阿令慢，約 4.5–4.8 秒）都在 6 秒鏡的 5.9 秒以內；8 秒鏡的石木匠、韓伯、阿令長句都在 7.3 秒以內。錄音後照 `span934.sh` 重核即可 |
| s03 插鏡 | 第一格就是紙風車、不寫地點句、天空圖只當顏色（拍法 10、35），同第 33 集 s27 |
| s23 鉤子 | 見逐一判斷；固定、結果先寫、沒人、沒鞋句 |
| s05／s06 的反打背景 | 反打照理背景應換到另一側；送 `-an-l3`（石階那側）是照現有的圖，許硯的位置本來就在石階旁，觀眾讀得通 |
| s40 主觀鏡的方向 | s37–s39 朝畫右看、s40 從背後望圖上的遠山，其實差了約 90 度；但「看向畫右→切主觀」是慣例，只有一張田的圖，接受 |

## 小結

- **必改 4 項**，都是改字或免費重裁，不花錢：(1) s40 與 s01–s03、s34 的「the air is clear and still」逐鏡換掉；(2) s10、s18 換一張較寬的免費大石裁切、s10 許硯改站石邊後的沙岸；(3) s30 拿掉低角度仰拍高田埂；(4) s22 寫出閘門位置、把「潭水流向水車」改成水從閘口衝出去。
- **建議 12 項**；要付費的只有 s35–s36 等鏡的「田壟有水」圖（約 1.5–2 CU，看 d1 再決定）與不建議做的秋葉改圖、新渠重畫（各約 1.5–2 CU）。
- 三個寫稿決定（c35–c40 搬到田邊、c24 改葉板帶水、田與渠的 deep pool 給 `SET` 再由 mkspec 拿掉）**都合理**；第三項只要記得 fix 也帶同一組替換。
- 改完 `r2.py`、`mkspec.py`（與 `shentan_xi.sh`）後重跑 `build934.sh`、`prep934.sh`；第 33 集成片後照實拍重核 s01。
