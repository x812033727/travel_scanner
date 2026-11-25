# 第 19 集重製版（e019-r2，內部編號 919，真人版）分鏡與提示詞：開拍前獨立審稿

- 審稿：沒參與寫稿的獨立審稿代理，2026-11-16。只讀，只寫本檔；沒用 Colab、RunPod 或任何付費服務，沒有 git commit。
  試裁的圖只放在 scratchpad（`rv919/`），repo 的參考圖一張都沒動。
- 審的版本：`docs/videos/zhong-tian-qu-qi-e019-r2/{script.md, storyboard.md, video.json, overlays.json}`、`writer-tools/e019-r2/r2.py`、
  `colab/runs/e919/extras.json`、`colab/runs/e919-live/{mkspec.py, spec.json}`，以及實際要送的
  `/root/mokaair-work/videos/zhong-tian-qu-qi-e919-dh/runpod/live/d1/colab-jobs.json`（82 支 = 41 鏡 × 9191101／9191102）與 `prompts/`。
- 機械檢查（本審稿自己跑）：
  - 兩個種子的提示詞、參考圖與秒數逐鏡相同。
  - 82 支的參考圖全部是絕對路徑、檔案都在；`swap_pictures` 有換到（`retake.json` 還是 `set-xianya-l1`，`colab-jobs.json` 已是 ceting／floor／dais／steps／eave）。
  - overlays 四個面板（s25、s33 四行、s34、s35）跟系統句一字不差。
  - 提示詞裡沒有「X speaks off screen」：出現的 off screen 都是「Qian Yuanwai off screen right」這類位置句。
  - 否定詞掃描：只有允許的「never the lens／no second copy／no talking／no mouthing words／nothing tucked in it／nothing hanging from it／nothing showing through it／no subtitles」，
    沒有被否定的物件名詞。另外找到一個**本身就會長字的名詞**：s18 的「its writing turned toward the dais」（必改 10）。
- 錄音：`audio/zq919a01–a45.wav` 用 ffprobe 量長度、silencedetect（−40 dB）看停頓。faster-whisper medium（scratchpad 的 `fw` 環境）
  一次只跑一支、跑完就結束，餵的是 ffmpeg 轉成 16 kHz f32le 再用 numpy 讀進來的陣列。重聽了這四支：
  - a42 take1：讀成「審章」；加了含「十本帳」的 initial_prompt 還是「審章」。「十／本／帳」三個字只佔 1.98–2.34 秒，「本」被吞掉了。
  - a42 take2：讀成「是不是」。
  - a43：讀成「十本帳早兌完了」，唐小棠那句是對的。
  - a26：0–0.94 秒是「呵呵」冷笑，人聲 0.94–5.68。
- 放大看過：
  - 新裁的 `set-xianya-steps-l1`，並把鼓架後那塊紅色花紋放大 4 倍看；`set-wuding-eave-l1` 與它下緣的瓦當放大 2 倍看；
  - 來源圖 `set-xianya-l1`、`set-wuding-l1`；`set-xianya-gongtang-floor-l1`、`-dais-l1`、`set-xianya-ceting-l1`；
  - 錢員外 l1 與 angle-a／b、唐小棠 l1 與 angle-a／b、賴三 l1。
- 對照：
  - `r2-bible-e011-e020.md` 拍法 1–18（尤其 1、2、3、5、7、9、15–18）、道具表、接點 18→19 與 19→20；`r2-bible-e011-e060.md` 第 19 集時間線與好感帳；
  - `season-01.md` 第 19 集；`writer-tools/e018-r2/review.md`；
  - `colab/runs/e91{6,7,8}-live/{review-picks-a,review-picks-b,picks-merged}.tsv`、`e918-live/fix1/review-picks.tsv`、`fix1/mkspec.py`、`fix2/mkspec.py`
    （fix2 的 s37 背影版還沒拍，結果未知）；任務檔第 12–16 集的教訓。

## 總評

做到的：
- 唐小棠五句都背拍，spec 拿掉她的臉部圖與身分句；
- 錢員外 s12 以前兩手都在袖裡、畫面外，紅寫成第一格的狀態；
- 帳頁一律紙背或摺著，帳冊是素封面；
- 沒有衙役的人、沒有兵器，秦霜腰帶空著；
- s14、s20 攤手不指人；胡縣令與錢員外不同框，胡縣令只在公案裁切圖上；
- OFFSCREEN_SPEECH 關掉，每個不說話的人都寫了閉嘴；
- 手部插鏡不送全景圖；s01 照第 18 集 fix1 的接點寫；
- 三位妻子的好感、獎勵與主線跟聖經一致。

問題集中在五類：

1. **一鏡裡的事情太多，或幾何上做不到**：
   - s12 兩隻黑袖手從左右緣抓一個朝畫左的人的前臂，還要再推一次袖子，接著先閉嘴、再吼，而且沒有時間錨點；
   - s34、s36 一支裡有兩、三句，都沒有寫「第幾秒開始說」；
   - s28 衙役的手在畫左緣放開木匣，可是木匣在她胸前、她背對我們；
   - s11 第一格掌心已經朝上，動作又要「翻成掌心朝上」。
2. **臉會跑出來**：
   - s23 認罪鏡送了錢員外三張臉部參考圖，第 18 集 s37 寫「低頭」照樣露齒笑；
   - s13 兩張定妝照拿來當手的主人；
   - s26 寫「over his right shoulder」：他朝畫左走，右肩在離鏡頭遠的那一邊，照字面回頭會把臉轉走；s37 秦霜同樣寫錯肩；
   - s26 寫「sneer」，就是冷笑變咧嘴笑的來源。
3. **軸線**：s06 唐小棠站在許硯畫左；s07、s20、s27 她都在許硯畫右，所以 s06→s07 跳軸。
4. **參考圖本身會長東西**：
   - `set-xianya-steps-l1` 鼓架後那塊紅色方塊，放大看是一排黑色的字形筆畫；
   - `set-wuding-eave-l1` 下緣的瓦當上有字形浮雕，s38 又剛好寫「屋簷瓦在前景」；整張是 3D 渲染；
   - 錢員外 angle-b 的帽子後面有一個垂下的小黑結，angle-a／b 的帽子是兩層的，像幞頭——這就是「帽後垂帶像官帽」的來源。
     s09、s15、s17、s19 只送 angle-a 加 angle-b，沒有送正面定妝照。
5. **錄音**：a42「十本帳」兩次都不對。這不是聽寫的問題：take1 的「本」字被吞掉了。

**必改 18 條、建議 14 條。** 參考圖都不用重畫，要做四張**免費**的衍生圖：
- `set-xianya-steps-l2`：塗掉紅色方塊；
- `set-wuding-eave-l2`：重裁，切掉瓦當；
- `laisan-sleeve-l1`、`qianyuanwai-sleeve-l1`：從定妝照裁出領口以下，給 s13 的手部插鏡用。

可選的付費編輯是「只改一件事」：錢員外 angle-a／b 改成整圈平滑的高圓帽，見文末。

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 改法 |
| --- | --- | --- |
| s12 一支 10 秒裡兩隻黑袖手推袖子，加上錢員外先閉嘴、再吼 | **照現在寫會出事。**三個原因：(1) 他身體朝畫左、兩臂往畫左伸，右緣那隻手抓不到；(2) 第一格袖子已經在手肘，動作又寫「再推過手肘」，等於在畫面裡演推袖，手最容易多出來、袖子滑下來蓋住紅手；(3) 沒寫秒數，模型會從第一秒就動嘴。錄音 a11＋a12 是 10.52 秒，人聲 4.39＋5.05 秒，照 r2.py 的算法 10 秒鏡裝得下，但沒有餘裕。 | 必改 2：身體正對鏡頭、臉四分之三朝畫左；左緣的手抓他右前臂，右緣的手抓他左前臂，兩隻黑袖都只「抓著」；前三秒閉嘴瞪眼，第四秒起往後掙、吼。剪接把胡縣令的 a11 提前約 1.3 秒，蓋在 s11 尾巴（賴三的手、a10 講完之後）。 |
| s13 送兩人的定妝照當手的主人，可能冒臉 | **會冒**。兩張都是胸像，送兩個人比 s11 只送一個人風險大（第 15 集 s02「四隻手＝兩個許硯」）。這鏡要的只是袖口的布料與顏色。 | 必改 3：從定妝照免費裁出領口以下（沒有臉）當參考圖。 |
| s23 臉朝地說話，會不會被畫成抬頭 | **會。**送了三張臉部圖，「kneeling」「high-angle」擋不住，第 18 集 s37 的「低頭」也一樣露齒笑。而且構圖句裡有一段錯位的文字（cap … rim from in front and above）。 | 必改 4：照第 18 集 fix2 的做法拿掉三張臉部圖與名字，改寫一句衣著；鏡頭在前上方往下看，帽頂在畫面正中、帽簷蓋住整張臉，紅手平貼在帽簷前。 |
| s26 冷笑變咧嘴笑 | **會。**「sneer」一字加上 a26 開頭的「呵呵」嘴型，很容易變成咧嘴；「回頭」寫成右肩，臉會轉走。 | 必改 5：改寫左肩；表情寫閉嘴、唇抿薄、一邊嘴角下拉；開頭寫閉著嘴從鼻子哼一聲。秒數見建議 3。 |
| s39、s41 唐小棠背影的丸子頭 | s39 下巴擱在膝上，頭被固定住，**可以拍**。s41 只寫「抱緊膝蓋」，問句又是全集情緒最高的地方，最容易轉頭露頰（第 14 集 s24、第 16 集 s32）。丸子頭走樣（第 16 集變兩條馬尾、第 17 集 s17 變四團花簇）的主因是長緞帶句；這裡用的已經是第 16 集 fix1 的短緞帶寫法。 | 必改 18：s41 也寫下巴擱在膝上、從第一格到最後一格。建議 7：拿掉 TBACK 的「one pearl pin in each」，或保留但挑片時特別看。 |
| 兩張新裁切圖：屋頂偏 3D、門口鼓架後的紅色花紋可能長假字 | **都要處理，都免費**。紅色方塊放大 4 倍看是一排黑色的字形筆畫，要塗掉。屋頂圖是 3D 渲染，下緣一排瓦當有字形浮雕，s38 又寫「屋簷瓦在前景」。 | 必改 14：做 `set-xianya-steps-l2`（ffmpeg drawbox 塗成近黑）。必改 15：做 `set-wuding-eave-l2`（重裁、切掉瓦當，竹梯頂留著），只送 s38；s39–s41 這幾個近一點的鏡不送屋頂圖，背景照文字寫成暗瓦與黑夜空，免得帶進 3D 質感。 |
| s04 押人跪下、三張臉的全景會不會擠 | **會**。三個人都寫全身，960×544 的中全景裡每張臉不到 40 像素，身分最容易跑掉；還要在 6.58 秒裡走進來、按跪、說 4.24 秒的錄音。 | 必改 7：第一格賴三已經站在地中間、秦霜已經揪著他；錢員外改成畫右緣一個跪著的背影（不點名、不送圖），臉只剩兩張；他的那一驚交給 s09。 |
| s37 唐小棠不在這一鏡的接戲 | **接不上**：s36 她還湊在許硯面前，s37 三個人走、她不見了，觀眾會問。三張小臉的低角度全景也一樣擠。 | 必改 6：改成秦霜單人中全景，回頭（左肩）朝畫右外催一句，其他三人在畫外。這樣唐小棠的去向不用交代，臉也只剩一張。 |
| a42「十本帳」錄音 | **兩次都不對**。take1 的「本」字被吞了（聽寫用含「十本帳」的提示仍是「審章」），take2 是「是不是」。人耳也救不回來。 | 必改 16：重錄，台詞不改，只在輸入加停頓；錄完聽寫確認。 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 19 | s12 | 1. 兩隻黑袖手從左右緣抓一個身體朝畫左、兩臂往畫左伸的人，右緣那隻手抓不到；<br>2. 第一格袖子已經在手肘，動作又寫「把袖子再推過手肘」，等於在畫面裡演推袖；<br>3. 「先閉嘴、再吼」沒有秒數。<br>錄音 a11＋a12 共 10.52 秒，人聲 9.44 秒。 | 拍法 10、16–18；第 18 集 fix1「手與道具寫在第一格構圖」；第 18 集 s35、s40 的手 | 構圖換成：`medium shot of Qian Yuanwai kneeling on the stone floor, framed from the knees up, his body square to the camera and his face three-quarter to screen left, both forearms held out in front of his belly toward us from the first frame, his wide gold sleeves already bunched at his elbows; from the left edge one hand in a plain black cotton sleeve grips his right forearm, from the right edge one hand in a plain black cotton sleeve grips his left forearm; the left and right edges of the frame cut both black sleeves at the forearm.`<br>動作換成：`For the first three seconds his lips stay pressed together, his eyes go wide and dart between the two black-sleeved hands, and the hands only hold him, steady. From the fourth second he jerks back against their grip and shouts the line; after the last word he leans away, his orange-red hands still held out by the wrists.`<br>剪接：a11 從 s11 片尾往前約 1.3 秒開始（a10 講完以後），s12 的第四秒接 a12。 |
| 19 | s06 | 唐小棠站在許硯畫左。s07 她在畫左卻朝畫左看許硯（他在她左邊）；s20 她在許硯畫右、s27 她的手從畫右伸進來。所以 s06→s07 跳軸。 | 拍法 9；s07、s20、s27 的站位 | 唐小棠一律站在許硯的畫右後方：`one step behind him on screen right, half behind his right shoulder, Tang Xiaotang … her face three-quarter to screen left toward him`；許硯的動作改成 `then turns his head toward screen right, past her shoulder, toward Qian Yuanwai off screen right`。script 的軸線也改成「唐小棠在許硯右後」。 |
| 19 | s13 | 送賴三、錢員外兩張胸像定妝照當手的主人，兩張臉、兩個人都可能被畫出來。這鏡只需要袖口的布料。 | 第 15 集 s02「四隻手＝兩個許硯」；第 16 集「場景圖的狀態壓過文字」；拍法 10 | 免費裁兩張，沒有臉（試裁過）：<br>`qianyuanwai-sleeve-l1` = `qianyuanwai-portrait-l1` `crop=864:472:0:680`<br>`laisan-sleeve-l1` = `laisan-portrait-l1` `crop=864:412:0:740`<br>s13 只送這兩張。身分句換成：`The two thin hands come out of grey-brown hemp cuffs of the cloth shown in <Picture 1>; the two plump hands with three gold rings come out of the dark gold silk sleeves with roundel patterns shown in <Picture 2>; the arms leave the frame at the bottom edge.` |
| 19 | s23 | 1. 送三張臉部圖，模型最可能讓他抬頭（第 18 集 s37 三支都露齒笑）；<br>2. 構圖句有錯位的文字：`plain and smooth all the way round down to its rim from in front and above, kneeling`。 | 拍法 2、14、15；`e918-live/fix2/mkspec.py` 的做法；挑片教訓「求情時露齒笑」 | 拿掉三張錢員外圖，只送 floor。身分句換成：`The one man in this shot is a short, portly man in a dark gold silk round-collared robe with roundel patterns, a white inner collar, long wide sleeves bunched at his elbows, and a tall round smooth black cap, plain and smooth all the way round down to its rim; the location`<br>構圖換成：`high-angle medium shot from in front of him and well above, looking down on him: he kneels and leans forward with his forehead lowered almost to the backs of his hands from the first frame, the round crown of his tall black cap in the middle of the frame and its brim toward the camera covering his whole face; both plump hands planted flat on the grey tiles in front of his knees, stained an even matte persimmon orange-red …, three gold rings on his fingers; the crown of the cap, his round shoulders and his two hands are all we see of him.`<br>動作：`His shoulders sag lower and his back heaves twice; his orange-red fingers spread on the stone; the crown of his cap stays low over his hands the whole shot.` |
| 19 | s26 | 1. 他朝畫左被拖，右肩在離鏡頭遠的那一邊，「over his right shoulder」照字面回頭會把臉轉走；<br>2. 「in a cold sneer」容易變咧嘴；<br>3. a26 開頭 0–0.94 秒是「呵呵」，要是畫成張嘴笑，就跟稿子要的冷笑相反。 | 拍法 14、18「不笑寫成具體動作」；挑片教訓「求情時露齒笑」；README-retakes 的 a26 | 兩處的 right shoulder 都改成：`his head turned back over his left shoulder toward screen right, his face three-quarter toward us`<br>表情：`cold and spiteful: eyes narrowed to slits, brows drawn low, lips closed and pressed thin, one corner of his mouth pulled hard down`<br>動作開頭加：`first he huffs once through his nose with his lips closed, then speaks slowly`<br>句尾換成：`after the last word he presses his lips together, one corner pulled hard down, his eyes still on Xu Yan, as he is pulled toward the left edge` |
| 19 | s37 | 1. 唐小棠在 s36 還在，s37 不見了，接不上；<br>2. 三張全身小臉的低角度全景（每張臉約 30 像素）；<br>3. 「looking back over her right shoulder」：她朝畫左走，回頭會把臉轉走。 | 拍法 1、9；稿子「四人走回柳溪」 | 改成秦霜單人，只送秦霜與 steps 圖：`medium full shot at the foot of the stone steps: Qin Shuang …, framed from the knees up with clear space above her head, the small plain dark brown wooden box tucked under her left arm from the first frame, walking toward screen left, her head turned back over her left shoulder toward screen right, toward the others coming down the steps behind her off screen right, never the lens; brisk: brows level, lips moving crisply between words; behind her only the pale stone steps and the gate hall, soft. She is the only person in the frame; no second copy of anyone appears.`<br>動作：`she calls back over her left shoulder, then faces front and quickens her pace toward screen left.` |
| 19 | s04 | 三張全身小臉（拍法 1 的上限，臉太小，身分最容易跑掉）；從左邊走進來、按跪、說 4.24 秒，6.58 秒的片段放不下；「her left hand on his left shoulder」是離她遠的那一邊。 | 拍法 1、2、10 | 第一格就在地中間；錢員外改成畫右緣的背影，拿掉他的兩張圖：`medium shot on the stone floor, framed from the knees up: a little left of the middle Lai San … standing hunched, his tied orange-red hands in front of his belly; close behind him on screen left Qin Shuang …, her right hand gripping the back of his collar and her left hand on his near shoulder from the first frame; at the right edge, soft, one portly man in dark gold silk and a tall round smooth black cap kneeling with his back to us, seen only from behind.`<br>動作：`In the first second she presses down on his shoulder and he drops to his knees; then she lifts her face toward the high dais above the top of the frame and speaks.`<br>錢員外那一驚交給 s09 開頭：`his eyes flick to the kneeling man at screen left, then his chin jerks up`。 |
| 19 | s11 | 第一格寫「held out palms up」，動作又寫「turn them palms up toward us」，兩句互相矛盾，手會扭成怪角度。 | 拍法 10；第 18 集審稿必改 4「自相矛盾」 | 動作改成：`the slim hands pull the thin hands a hand's length forward by the wrists, the palms still turned up toward us; the thin orange-red hands tremble all the time in their grip`。 |
| 19 | s16 | 句子錯接：`a raised ring round a small square hole, plain and smooth in both hands, sets it down`，會讀成「銅片在兩手裡」。銅片也沒寫比例（第 17 集 s20 畫成手掌大的金屬籠）。 | 第 17 集挑片 s20；道具表 | 換成：`Xu Yan opens the blue cloth and lifts out with both hands one charred lantern frame: a ring of blackened bamboo ribs two hands wide, its paper burnt away to a few brown scorched edges, and at its base one small plain copper plate the size of a thumbnail, far smaller than his palm, a raised ring round a small square hole, smooth and plain; he sets it down on the stone floor in the middle of the frame and stands up beside it, speaking;` |
| 19 | s18 | 「its writing turned toward the dais」：提示詞裡出現 writing 這個名詞（紙長假字的來源）。 | 拍法 7、17、18 | 換成：`holding up one unfolded sheet of thick opaque paper at shoulder height in both hands, facing the dais beyond the right edge of the frame; the side toward us is plain, blank and evenly lit from our side, thick and opaque, nothing showing through it` |
| 19 | s34、s36 | 一支裡有兩、三句，都沒有寫「第幾秒開始說」，模型會從第一格就動嘴。s34 人聲 3.30＋3.96＋1.71 秒，s36 1.95＋3.46 秒。 | 拍法 15；第 10 集 s16 整鏡重拍 | s34：`For the first four seconds Xu Yan's lips stay pressed together while his eyes grow wider; from the fourth to the eighth second he bursts out laughing and speaks the line through the laugh; from the eighth second he claps the back of his right hand over his mouth and keeps it there to the last frame, his eyes still creased.`<br>s36：`For the first two and a half seconds Xu Yan's lips stay closed while the young woman leans in; from the third second he waves his right hand once and speaks lightly.` |
| 19 | s01 | 許硯把手臂從金綢下抽走以後，錢員外那條金袖手臂怎麼放沒寫，手最容易從袖口滑出來。 | 第 18 集 s35、s40 重拍原因；挑片教訓「錢員外的手滑出袖子」 | 在 `the silk slides off it;` 後面加：`Qian Yuanwai's gold-sleeved arm drops straight down past the bottom edge of the frame, the long sleeve closed round his hand;` |
| 19 | s02、s09、s12、s15、s17、s19、s26 | 這幾鏡都送 `angles/qianyuanwai-angle-b-l1`（側面，帽後垂一個小黑結，帽子兩層像幞頭）。s09、s15、s17、s19 只送 angle-a 加 angle-b，沒有正面定妝照，帽子會照角度圖畫。 | 第 18 集 fix1 s40「帽後垂一條長黑帶，像官帽帶」；拍法 4；挑片教訓「參考圖的髮型壓過文字」 | 每鏡拿掉 angle-b；s09、s15、s17、s19 換成 `qianyuanwai-portrait-l1` 加 angle-a。文字照舊寫 `tall round smooth black cap, plain and smooth all the way round down to its rim`。可選的付費編輯見文末。 |
| 19 | s28–s37 | `set-xianya-steps-l1` 鼓架後的門裡有一塊紅色方塊（約 x952–1050、y424–472），放大是一排黑色字形筆畫。每支背景都看得到。 | 第 16 集 s29「木牌假字」；拍法 7、17 | 免費做 `set-xianya-steps-l2` = `ffmpeg -i set-xianya-steps-l1.png -vf "drawbox=x=952:y=424:w=98:h=48:color=0x0c0a0a@1:t=fill"`（試做過，近黑跟周圍的暗門內接得上），swap 換掉 l1，再放大確認一次。 |
| 19 | s38–s41 | `set-wuding-eave-l1` 是 3D 渲染，下緣一排瓦當有字形浮雕。s38 又寫 `the edge of the eave tiles soft in the foreground`，正好把它們拉到前景。 | 拍法 7、18；聖經記「原圖偏 3D」；第 16 集「場景圖的狀態壓過文字」 | 1. 免費做 `set-wuding-eave-l2` = `set-wuding-l1` `crop=800:450:0:96,scale=1312:736:flags=lanczos`（試裁過：瓦當切掉，竹梯兩根頂端留著，滿月與柿子樹不在）。<br>2. s38 改寫：`low-angle wide shot up the long slope of plain dark grey tiles, the two bamboo poles of the ladder top at the bottom left`。<br>3. s39、s40、s41 不送屋頂圖，背景只寫 `behind him only the dark grey tiles and the black night sky`（三鏡本來就這樣寫）。 |
| 19 | s38（a42） | 「十本帳」take1 的「本」被吞掉，聽寫成「審章」（給了「十本帳」的提示仍是），take2 成了「是不是」。 | README-retakes；本審稿重聽 | 重錄，台詞一字不改，只在輸入加停頓：`大半夜坐在屋頂上，十本帳，又不對了？`；不行就把「十 本 帳」用空格隔開或放慢 0.9 倍。錄完照例一次一支聽寫，要讀出「十本帳」；人耳也聽一次。 |
| 19 | s28 | 衙役的黑袖手在「畫左緣」放開木匣，可是木匣在她胸前、她背對我們、人在畫右前景，那隻手要橫過整個畫面，最容易補出整個衙役。 | 拍法 2、16–18；第 18 集「接觸寫成第一格就已經的狀態」 | 拿掉黑袖手（交匣子交給音效與台詞），木匣第一格就在她手上：`camera a little above her right shoulder, looking down over it: she holds one small plain dark brown wooden box the size of two hands in both hands in front of her chest from the first frame, its lid raised a finger's width, a soft gleam of silver inside, the box clearly visible past her right shoulder`<br>only 句改成：`She is the only person in the frame, seen only from behind the whole shot; the young woman with the two high round buns appears only once; no second copy of anyone appears.` |
| 19 | s41 | 背影只寫「抱緊膝蓋、看著他」，頭沒被固定。全集情緒最高的問句，最容易轉頭露頰。 | 拍法 3；第 14 集 s24、第 16 集 s32 | 構圖加：`her chin resting on her knees from the first frame to the last, the back of her head and the two high buns still`；動作的第一句換成 `the young woman hugs her knees tighter, her chin pressed down on them;` |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 19 | s17 | a17 檔長 6.32 秒，人聲 0.00–6.09（−40 dB）。r2.py 量的是 5.79 秒（−35 dB），6 秒鏡只能裝 6.27 秒，加上句首要先「瞄一眼地上」，幾乎沒有餘裕。 | r2.py 的 BUY 算法 | 改買 8 秒：`"s17": 8`。 |
| 19 | s22 | 先拍案（第一秒），再說 4.77 秒，最後還要擦額頭，6.58 秒放不下。 | BUY 算法 | 拿掉 `after the last word he wipes his forehead with his left sleeve`，改成 `after the last word he stays leaning forward, sweat on his brow`；或改買 8 秒。 |
| 19 | s26 | a26 加上冷笑共 5.46 秒，句尾還要被拖到左緣，很緊。 | BUY 算法 | 改買 8 秒；或剪接從 a26 的 0.85 秒起放（剪掉「呵呵」），配合必改 5 的閉嘴哼一聲。 |
| 19 | s28–s37 | 文字寫 `low warm late-afternoon sunlight from the left, long soft shadows`，steps 圖是陰影裡的平光、沒有斜陽。文字跟圖打架，會一支亮一支暗。 | 第 16 集「場景圖的狀態壓過文字」 | 改成 `soft warm late-afternoon light, the gate hall in soft shade`，暖調留給剪接調色。 |
| 19 | s04–s27 | 公堂兩張裁切圖的光是冷灰色，文字寫 warm afternoon。 | 同上 | 可以接受；剪接統一往暖調，挑片時不要因為偏冷就落選。 |
| 19 | 許硯各鏡 | 每一鏡都寫 `one small corner of dark red silk showing at the edge of the collar`，s21「拍一下才露出一角」的那一拍就沒了。 | 稿子 c21；道具表 | 除了 s21，其他鏡只寫 `a small rounded bulge at the left breast of his robe`；s21 照留。 |
| 19 | s18、s28、s36、s39、s41 | TBACK 的 `one pearl pin in each` 從背後看，可能長成第 17 集 s17 的「四團花簇」。 | 第 17 集挑片 s17 | 可以拿掉珍珠簪，只留 `a short pink silk ribbon wrapped round each bun`；要留就在挑片時逐支看丸子的數目。 |
| 19 | s38→s39 | s38 送了她的定妝照：長緞帶垂到肩、有珍珠簪。s39 的背影寫短緞帶。兩鏡相連，緞帶長短會不一樣。 | 第 16 集 fix1 的取捨 | s38 她在全景裡很小，接受；挑片時看 s38 的緞帶，太長就收短一點。 |
| 19 | s19 文件 | storyboard 與 r2.py 寫「s12 約 9.9 秒」：那是去掉頭尾靜音的長度，檔長是 10.52 秒。 | 本審稿量測 | 註明「人聲 9.4 秒、檔長 10.5 秒，剪接把 a11 提前到 s11 尾巴」。 |
| 19 | s11 | 只送賴三的胸像當手的主人（第 18 集 s25、s26 也是這樣做，結果可以）。 | 同必改 3 | 可以改送 `laisan-sleeve-l1`，跟 s13 同一個做法。 |
| 19 | s02 | 前景的年輕男子同時寫了 `turning away toward the left` 與 `keeps his head still`。 | 第 18 集審稿「頭偏一下又寫頭不動」 | 改成 `his body half turned toward the left, the back of his head toward us and still the whole shot`。 |
| 19 | s38 | 寫唐小棠 `on screen right near the ridge`，可是裁切圖的屋脊從左上斜到右邊中間。 | 放大看 eave 圖 | 改成 `on screen right, high on the slope just below the ridge line`。 |
| 19 | s41 | 第 19 集大綱的結尾要「她眼睛紅了一圈」，真人版背拍後看不到她的臉。 | season-01 第 19 集；拍法 3 | 不違規，可以接受；若站主要那張臉，第 20 集第一鏡（她把下巴埋進膝蓋，不說話）可以給她中性的臉。 |
| 19 | s05、s24 | s05 先拍案再說 7.99 秒人聲（10 秒鏡），s24 先拍案再說 6.52 秒（8 秒鏡），都還放得下。 | BUY 算法 | 不改；剪接把驚堂木的音效對到片中拍下那一格。 |

## 參考圖：要做什麼

- **免費裁切或塗改**（都試做過，放在 scratchpad 的 `rv919/`，不是 repo）：
  - `set-xianya-steps-l2`：drawbox 塗掉鼓架後的紅色字形方塊。s28–s37 用。
  - `set-wuding-eave-l2`：`set-wuding-l1` `crop=800:450:0:96,scale=1312:736:flags=lanczos`，切掉有字形浮雕的瓦當。只給 s38。
  - `qianyuanwai-sleeve-l1`：`crop=864:472:0:680`。給 s13。
  - `laisan-sleeve-l1`：`crop=864:412:0:740`。給 s13，可選 s11。
  - 都照第 18 集的做法登記在 `refs-live/README.md`，由 spec 的 `swap_pictures` 用絕對路徑送。
- **不送就好**：s39–s41 不送屋頂圖；s23 不送錢員外的圖；s04、s37 拿掉多出來的人的圖；全集拿掉錢員外 angle-b。
- **可選、付費、只改一件事**：
  - 錢員外 angle-a、angle-b 各做一次 Qwen 編輯，以原圖當底，提示詞只寫：`make his black cap one tall smooth round cylinder, plain all the way round down to its rim, like a plain tall drum`。
    做了之後 angle-b 可以再送。
  - 屋頂圖的 3D 質感若挑片時太明顯，再對 `set-wuding-eave-l2` 做一次「只改一件事」：`make it a real night photograph of old clay roof tiles`。
- **不用重畫**：ceting、floor、dais、唐小棠、賴三、胡縣令的圖都對得上文字。

## 最重要的五條

1. **s12**：改成兩手只抓、不推，身體正對鏡頭，前三秒閉嘴、第四秒才吼；a11 提前到 s11 尾巴。
2. **s23**：拿掉三張臉部圖與名字，前上方往下拍，帽簷蓋住整張臉，紅手平貼在地上。
3. **s26 與 s37**：回頭寫左肩；拿掉「sneer」，改成閉嘴抿唇、一邊嘴角下拉；s37 改成秦霜單人，唐小棠的接戲問題就沒了。
4. **s06**：唐小棠站到許硯畫右後方，跟 s07、s20、s27 同一邊。
5. **s13 與錢員外的帽子**：插鏡改送沒有臉的袖口裁切圖；全集拿掉帽後有結的 angle-b。

另外有兩條**開拍前一定要先做**：塗掉 steps 圖的紅色字形方塊（必改 14），重錄 a42（必改 16）。
