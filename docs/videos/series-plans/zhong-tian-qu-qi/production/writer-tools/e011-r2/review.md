# 第 11 集重製版（e011-r2，真人版）分鏡與提示詞：開拍前獨立審稿

- 審稿：沒參與寫稿的獨立審稿代理，2026-11-14，只讀。
- 審的版本：`docs/videos/zhong-tian-qu-qi-e011-r2/{script.md, storyboard.md, video.json, overlays.json}`、`writer-tools/e011-r2/r2.py`。
- 對照：`r2-bible-e011-e020.md`（〈真人版的拍法〉1–14 條、時間線、接點、道具）、`r2-bible-e011-e060.md`（11→12 接點：胡縣令在許硯**左耳**）、`season-01.md` 第 11 集、
  `storyboard-shot-spec.md`、`script-to-storyboard.md`〈拍法〉、`animation-camera/SKILL.md`、第 10 集 `e010-r2/r2.py` 與 storyboard s32–s40、
  `assets/refs-live/README.md`、任務檔 Steps（第 6–9 集）、`colab/runs/e910-live/review-picks-a.tsv`、`review-picks-b.tsv`，
  以及實際組提示詞的程式：`e001-r2/build-r2.py`（畫外句自動補 `X speaks off screen`、說話句帶引號台詞）、`hailuo/gen-dh.mjs`、
  `colab/ref2manifest.mjs`（依 chars 人數補「He is the only person in the frame」或「Only these N people」）、`live-action/pilot.py`、`_scripts/preflight-prompts.py`。

## 總評

劇情照細綱與 r2 稿走完（抓人→婚書→名冊→律條→印→喝退→錢員外出主意→送州府核查→系統警告→耳語「交出她一個」），
問答有頭有尾，好感帳無加減、面板文字與系統念的一字不差，參考圖都在 `refs-live`，s01 接第 10 集 s40 的同一刻成立。
第 7–10 集的大教訓（過肩前景不點名、唐小棠背後拍、紙不寫字、夜景寫光源、交領寫死左右）也都寫進去了。

開拍前要改的集中在三類：
1. **畫外句**：`build-r2.py` 自動在提示詞尾巴補「`… speaks off screen`」或「`the system voice speaks off screen`」。第 10 集 s16 兩支都因此重拍（嚴重），s31、s33 也是。s29 甚至把**心裡話**寫成「Xu Yan speaks off screen」。
2. **兵器**：`ZHAO` 把寫稿備註「no sword written」漏進提示詞；`NOSHARP` 沒寫刀鞘；趙捕頭腰間鐵尺還在 s17 的動作裡。第 10 集 s22、s32、s37、s40 都畫出了帶鞘的刀。
3. **幾鏡的空間與接戲寫不通**：s05、s22 的全景漏了在場的主角；s19 阿令沒被架著；s32、s35 耳語的視線與站位；s35 前景冒出「一個男人的拳頭」。

**必改 16 條、建議 18 條。**

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 11 | s28 | 許硯近景 10 秒、三句全是畫外（系統兩句、心裡話一句），可是 `video.json` 的 prompt 結尾被補上「`; the system voice speaks off screen`」。模型會讓畫面上唯一的人張嘴對嘴型。 | e910 picks-b s16：「規格是許硯嘴閉著、系統句畫外，兩支他都在張嘴說話」→ RETAKE（嚴重）。改法是拿掉提到聲音的句子，寫成不說話。build-r2.py 第 96–97 行會自動補這句。 | 在 `spec.json` 的 s28 `replace` 拿掉「`; the system voice speaks off screen`」（或在 r2.py 的 comp 裡先寫出「off screen」，讓 builder 不補）。comp 結尾、motion 開頭都加：`He says nothing in this shot: his lips stay pressed together from the first frame to the last, his jaw still, no talking, no mouthing words; he is thinking, not speaking` |
| 11 | s29 | 許硯的台詞是**心裡話**（`inner`），因為他不在 chars，builder 在 prompt 尾巴補了「`; Xu Yan speaks off screen`」。主觀鏡裡三個女人嘴閉著，再加這句，就是第 10 集「畫外句時畫面上的人張嘴」的條件。 | build-r2.py 第 93–95 行（`offs` 沒有排除 inner）；e910 picks-b s31、s33（畫外句時畫面上的人張嘴，嚴重／中等）。 | `spec.json` 的 s29 `replace` 拿掉「`; Xu Yan speaks off screen`」。comp 的「`A-ling still, lips closed`」後面加：`none of the three women says anything in this shot; all three keep their lips pressed together from the first frame to the last, no talking, no mouthing words`。另外開一張票修 build-r2.py：`offs` 要排除帶 inner 旗標的台詞，不在本稿範圍。 |
| 11 | s24 | 錢員外畫外，prompt 尾巴被補上「`; Qian Yuanwai speaks off screen`」。畫面上的胡縣令只寫「his lips stay closed」，第 10 集 s33 同樣寫法下，錢員外在許硯畫外句時嘴沒閉好。 | e910 picks-b s33（中等）、s16（嚴重）；build-r2.py 第 94–95 行。 | `spec.json` 的 s24 `replace` 拿掉「`; Qian Yuanwai speaks off screen`」。motion 改成：`the plump hand settles on the magistrate's shoulder; Magistrate Hu says nothing in this shot, his lips pressed together from the first frame to the last, no mouthing words; he tilts his ear toward screen right, his eyes rolling once and lighting up` |
| 11 | s04、s12、s23 | 畫外句（許硯）落在不說話的人臉上：阿令近景、胡縣令近景、屋門前三女。現在只寫「lips closed」「lips stay closed」，第 10 集同樣寫法還是張嘴。這三鏡的 prompt 已有「off screen」字樣，builder 沒補畫外句，所以只差把沉默寫硬。 | e910 picks-b s31（1102 張嘴說話，這鏡是許硯畫外，嚴重）、s33；`r2-bible-e011-e020.md` 拍法第 3 條「反應給對面的人」。 | 三鏡的 motion 開頭各加一句（s23 用複數）：`She says nothing in this shot: her lips stay pressed together from the first frame to the last, her jaw still, no talking, no mouthing words` ／ s12：`He says nothing in this shot: …` ／ s23：`None of the three women says anything: …` |
| 11 | s02 | 「住手！」五個字以內、帶「！」，`speak_clause` 把它原樣放進 motion：「`speaks a short Mandarin line, 「住手！」`」。preflight 的 `shout` 會警告，因為這種短喊會被畫成字幕（e053 s05）。script.md〈配音〉也寫明「製作端寫成『張嘴喊』，不放進畫面描述」。 | script.md〈配音〉第 3 條；preflight-prompts.py `warn shout`；e910 有兩支燒進字幕（s13、s30）。 | r2.py s02 加 `nospeak=["xuyan"]`（錄音照放），motion 開頭寫：`at a sound from the house Xu Yan whips round to face screen left and shouts one short word, his mouth opening wide once, then drops his arms and breaks into a run toward the house door`。 |
| 11 | s05、s13、s16、s17 | `ZHAO` 常數的結尾是「`, no sword written`」，這是寫稿備註，不是畫面描述，已經進了 4 鏡的 prompt（video.json 出現 4 次）。模型讀到 sword 這個字，就有理由畫一把刀。 | `r2-bible-e011-e020.md` 拍法第 5 條「兵器不寫就不會出現，寫了插在鞘裡也會畫在手上」；e010 的 `ZHAO` 沒有這半句。 | `ZHAO = "in his black futou cap and plain black round-collared constable's robe, a plain black cloth sash at his waist with nothing hanging from it"`；兵器只靠每鏡的 NOSHARP／NOBLADE 去寫「沒有」。 |
| 11 | s17 | 動作寫「`his left hand presses the iron ruler at his belt down`」。鐵尺已經從定妝照拿掉（pilot.py `LIVE_LOOK`），這裡又把腰間長條鐵器寫回來。s17 的 comp 也是全集唯一一鏡有官府的人、卻沒有 NOSHARP／NOBLADE 的。第 10 集的衙役腰間長棍就被畫成刀鞘。 | 任務檔 Step 0「定妝照拿掉道具（趙捕頭的鐵尺）」；e910 picks-b s22、s32、s37、s40（佩刀、帶鞘的刀）；bible 拍法第 5 條。 | motion 改：`Constable Zhao's eyes slide away and his left hand presses flat against his plain cloth sash; he stammers, then lowers his head`；comp 結尾加 NOBLADE（改過的，見下一列）。storyboard 中文同步改成「左手按著腰帶」。 |
| 11 | s05、s09、s13、s14、s16、s22、s25、s26、s31、s32、s35（凡用 NOSHARP 的鏡） | `NOSHARP` 寫的是「no blade, no knife, no sword and no spear … only torches and plain wooden sticks」：沒寫刀鞘，又主動把「木棍」塞到衙役手上。第 10 集的衙役兩種錯都出現過：帶鞘的刀，還有「像刀鞘的黑長棍」。 | e910 picks-a s22（「前排幾人腰側另拿一根黑色長棍…輪廓接近刀鞘」）、picks-b s22、s32、s37、s40（佩刀、帶鞘的刀）；storyboard 開頭「衙役家丁只有火把」。 | `NOSHARP = "no blade, no knife, no sword, no scabbard, no sheathed weapon at anyone's waist and no spear anywhere in the frame; every runner wears a plain black cloth sash with nothing hanging from it and holds only one burning torch, his other hand empty"`。 |
| 11 | s06 | 唐小棠從背後拍（TBACK），可是動作裡她「hurries up to him … holds it out to him」，許硯在畫右「turning toward her」，motion 也寫「Xu Yan turns to her」。第 10 集 s30 的修法是拿掉所有提到轉頭的句子；遞東西給畫右的人，頭一定往右轉、露側臉。另外「letting go of a runner's wrist」跟「exactly two people in the frame」互相矛盾：手腕是誰的？ | e910 picks-b s30（6.0–7.5 秒她轉頭，側臉入鏡；修法「拿掉所有提到說話與轉頭的句子」）；e908 fix1。 | 把許硯放在她**正前方**、畫面中間偏右的深處，她的手直直往前伸。comp：`on the far side of her, straight ahead of her and facing us, Xu Yan, …, his face three-quarter to screen left toward her hands, never the lens`。motion：`she walks straight away from us toward him and holds one small folded oiled-paper packet straight out in front of her with her right hand; she keeps her head still and never turns it, the back of her head toward us the whole shot; Xu Yan lowers his right hand from the edge of the frame and holds it out open, palm up`。「runner's wrist」整句拿掉。 |
| 11 | s14 | 胡縣令的臉寫成「`mouth falling half open … lips closed`」，同一句互相矛盾（storyboard 也是「嘴半張、嘴閉著」）。唐小棠的錄音一放，半張的嘴就會跟著動，讀成縣令在說話。motion 又寫「the magistrate leans back」，第 10 集特地「不寫 leans」，因為頭會出畫。她「lifts her chin」也是背影鏡轉頭的起點。 | e010 storyboard s39「頭肩往前一探（不寫 leans）」；e910 picks-b s30；bible 拍法第 3 條。 | comp：`thrown: eyes widening, brows jerking up, his lips pressed together, no smile; he says nothing in this shot`。motion：`the young woman stands still, her head never turning, the back of her head toward us the whole shot; the magistrate's head jerks back a little, his whole head staying in the frame, his eyes going wide; his lips stay pressed together`。 |
| 11 | s06、s14、全集 | 開拍前**一定要有**的兩個檔都還沒建（storyboard 頁尾自己也列了）：`colab/runs/e911/extras.json`（秦霜柴刀、胡縣令官服換宋代寫法、拿掉「臉頰會抖」、畫面不放字幕）與 `colab/runs/e911-live/spec.json`（s06、s14 拿掉唐小棠三張臉部圖與身分句；s02、s23、s27、s29、s34 換中性外貌句）。沒有這兩個檔，Ref2VA 會照 `cast.json` 送她的臉、寫「small gold abacus hanging at her waist」與「cheeks shaking when he smiles」。 | storyboard 頁尾；`colab/runs/e910/extras.json`、`e910-live/spec.json`；bible 拍法第 3、5 條。 | 照 e910 兩檔複製後改鏡號。s06、s14 的 `replace` 也照 e910 s23 的寫法，把「`Only these 2 people are in the frame`」換成「`Only these 2 people are in the frame, the young woman seen only from behind`」。另外把上面 s24、s28、s29 的 `speaks off screen` 刪除寫進同一份 spec.json。preflight 0 ERROR 才拍。 |
| 11 | s19 | 阿令到 s22 才被兩個衙役鬆開（s22「the two runners let go of A-ling's arms」），s19 卻只寫「`behind him on screen left {ALING}, {SLEEVES}`」。SLEEVES 還寫「both hands empty」，看起來就是自由站著，接戲斷了。 | s08、s11、s22 都寫「held by two runners」；storyboard-shot-spec〈連戲〉「前一鏡在、這一鏡不在的人」。 | comp 改：`behind him on screen left {ALING}, {SLEEVES}, her arms still held by two {RUNNERS}, each runner's other hand holding one burning torch, lips closed`。不想多畫人，就把阿令拿出畫面：`behind him only the dark yard`，chars 改成 `["xuyan"]`。 |
| 11 | s22 | 全景、胡縣令在右、阿令在左後屋門前，中間的許硯卻不見了（s19、s20 他舉著婚書往右逼近，s23 他從畫外說話）。chars 只有兩人，還有第三個名額。觀眾會以為許硯離開了院子。 | 拍法：全景交代每個人的位置；bible 拍法第 1 條（三人以內）。 | chars 改成 `["huxianling", "xuyan", "aling"]`。comp 加：`in the middle of the yard, small in the frame, Xu Yan, {XU}, standing side-on to us with {CERTS} in his right hand, his face three-quarter to screen right toward the magistrate, never the lens, lips closed`；motion 加 `Xu Yan does not move; his lips stay closed`。 |
| 11 | s05 | 全景從籬笆後拍院門，可是「about four more coming round the back of the house at the back left」把鏡頭帶到屋門那一帶。那裡正是許硯扣著衙役手腕、阿令被架著的地方（s03→s06），comp 沒寫他們，模型不是畫空就是補不明人物。 | 拍法：全景交代每個人的位置；連戲：前一鏡在的人。 | 讓鏡頭只朝院門：`wide shot past {STICKTIPS} in the foreground, the camera facing the yard gate on screen right, the house door out of the frame off screen left`；「coming round the back of the house at the back left」改成 `about four more walking in from the left edge of the frame`。人數寫死（見建議 s05）。 |
| 11 | s32、s35 | 耳語的站位與視線寫不通：許硯「face three-quarter to screen right, eyes fixed straight ahead past the official」，胡縣令卻在**畫右**「bending toward his ear」。許硯面向的那一側正是縣令，「不轉頭、眼睛看前面」就變成兩人面對面，模型多半畫成許硯看著他。r2 bible 的 11→12 接點寫的是縣令在許硯**左耳**；第 12 集第一鏡也要「許硯直起身、正眼看胡縣令」，所以 s35 結束時他不能已經在看縣令。 | `r2-bible-e011-e060.md` 11→12 接點「胡縣令湊在許硯左耳邊」；script c32「許硯…眼睛看前面，沒轉頭」；`animation-camera`：畫外視線寫明看畫面外哪裡。 | s32、s35 共用一句站位：`Xu Yan facing almost toward us, turned only a little to screen right, his eyes fixed on a point off screen right beyond the lens, never the lens; Magistrate Hu a half step behind Xu Yan's left shoulder on screen right, bending his head to Xu Yan's left ear, his face in profile toward screen left`。s33「close to a young man's ear」那一側照這個站位，耳朵在畫左緣、縣令朝左。 |
| 11 | s35 | 「`medium shot past {CERTS} gripped in a man's right fist in the foreground: Xu Yan, framed from the chest up`」：前景一個「a man」的拳頭，加上中景胸以上的許硯，是兩個人。模型會多畫一個男人，或讓拳頭變成別人的。第 9 集教訓：手上的東西要寫明是誰、畫面哪一邊。 | 任務檔第 9 集條目（『from screen RIGHT』、誰手上拿什麼寫左右）；bible 拍法第 2 條（過肩前景冒分身）。 | 不要前景，改成：`medium close-up: Xu Yan, {XU}, framed from the chest up, his own right fist raised in front of his chest at the lower left of the frame, gripping {CERTS}`，再接上一列 s32 的站位句。 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 11 | s02 | 空間寫不通：「past the edge of the open yard gate in the foreground on screen right」又寫許硯「standing in the gateway … his back to us」。門板在前景，人就不可能站在門口。秦霜、唐小棠「behind him inside the gate on screen left」夾在鏡頭與他之間，而且一開始就「face … toward the house door」，還沒聽到聲音就已經轉頭了。第 10 集 s36 是從門外往裡拍：秦霜在畫左、唐小棠在畫右；本鏡反拍，兩人的左右應該對調。zh「刀尖朝地」是木棍，應作「棍尖朝地」。 | e010 r2.py s36；接點表 10→11。 | `medium shot from inside the yard looking at the open yard gate: Xu Yan in the gateway, his back to us, both arms spread across it, facing out to the dark road; just inside the gate between him and us, Tang Xiaotang on screen left and Qin Shuang on screen right, both facing the gate`；motion：`they turn their heads toward the house door after him`。 |
| 11 | 全集 LOC | 月亮三處說法不一：`nyard` 寫「a pale moon half hidden behind cloud」；第 10 集 `nyard` 寫「the moon hidden behind clouds」、`road` 寫「no moon」；兩份 bible 的時間線都寫「晴、無月」；script.md〈剪接〉也寫「沒有月亮」。 | r2-bible 時間線第 11 集；e010 r2.py LOC。 | 跟第 10 集相同：`the moon hidden behind clouds, the sky black`。真人夜院圖有月亮的話，在 bible 記一筆，接受畫出一點月光，但不寫「pale moon」。 |
| 11 | s09、s12、s17、s21、s24、s31、s33 | 近景只寫「behind him only (flickering) torchlight」。第 10 集近景背景反覆長出插在架子上、地上、三腳架上沒人拿的火把與火盆。 | e910 picks-a s36、s39，picks-b s37、s38、s39（火把沒人拿、一人兩支）；bible 拍法第 8 條。 | 近景背景統一：`behind him only darkness and the orange flicker of torches held by people out of the frame; no torch on a stand, in the ground or on a wall, no brazier`。 |
| 11 | s05、s11、s22 | 人數沒寫死：s05 家丁「crowding」沒數字，s11「a line of runners」、s22「among yamen runners」也沒數字。第 10 集草稿火把二十到三十支、村民多於八人。 | e910 picks-a s22、s27、s29，picks-b s22；bible 拍法第 13 條。 | s05：`six household servants … two of them holding one burning torch each, the others empty-handed, outside the gate`；s11：`four yamen runners seen from behind`；s22：`among four yamen runners`。每鏡加 `no more than eight torches in the frame`。 |
| 11 | s08、s09、s26、s30、s31、s33 | 過肩前景（HU_BACK、`him(...)`）只寫「his face never in the frame」，第 10 集幾乎每支過肩鏡都露出耳朵、臉頰、鼻樑。中文寫了「胡縣令右肩後」，英文沒寫哪一邊；而且從右前景拍到左邊的許硯，看到的其實是**左肩**。 | e910 picks-a s02、s05、s09、s12，picks-b s37、s38（前景露臉頰）；bible 拍法第 2、9 條。 | HU_BACK 改：`… seen only from behind, his head turned fully away from us toward the man he faces, only the back of his hat, the back of his neck and his left shoulder, his ear, cheek and profile never visible, soft and dark`；HIM_BACK 同樣加 `his head turned fully away from us, ear, cheek and profile never visible`。storyboard 中文改「左肩後」。 |
| 11 | s24、s26、s30、s33 | 這幾鏡 chars 只有一人，畫面卻有不點名的第二人（胖手、肩、耳朵）。ref2manifest 會補「He is the only person in the frame」，跟 comp 打架，可能把手畫成縣令自己的，或把前景的人刪掉。 | ref2manifest.mjs 第 110–112 行（`official`、`young man` 都不在 EXTRAS）。 | 在 spec.json `replace` 改成：`Besides him, only the hand / shoulder / ear the composition describes is in the frame, belonging to someone whose face is out of the frame; no second copy of anyone appears`。 |
| 11 | s21 | 13 字、結巴（「這、這是……」停頓）再加退半步，BUY 沒給 8 秒，會用 gen-dh 預設。r2.py 自己的規則是 13 字有動作給 8；s17 的「有……」就給了 8。 | r2.py BUY 註解。 | `BUY["s21"] = 8`。 |
| 11 | s01、s34 | `action_seconds` 2：s01 是抓、扯、半轉身，s34 是三人同時往前半步、停、各自一個手勢。稿子估 3.5 秒、4 秒，2 秒剪不完整個動作。 | script.md c01、c34；拍法「剪點放在動作中間」。 | r2.py s01、s34 加 `act=3`。 |
| 11 | s28–s29 | 心裡話與系統句共約 41 字，系統句加快 1.3 倍，估 9.5–10.7 秒，再加真人語速一成，會超過 s28 的 10 秒（剪接 1.1 倍約 11 秒）。s29 還有自己 16 字的心裡話，沒辦法 spill 過去。另外 inner 的 emotion 被疊成「內心獨白，嘴閉著，心裡話，嘴閉著，沉」。 | 拍法〈心裡話與畫外音〉；build-r2.py 第 76–77 行會自動加前綴。 | 錄音後量長度；超過就把 s29 的 BUY 拉到 10，s28 第三句的尾巴延到 s29 開頭，s29 的心裡話往後放。r2.py 的 emotion 改成只寫「沉」，前綴交給 builder。 |
| 11 | s18–s20 | 三份婚書攤開一份（s18–s20），另外兩份在哪隻手沒寫。s18 的袖口寫「faded blue-grey cuffs」，少了 s07 的「under an old grey cloth sleeve」。 | bible 道具表（三份婚書）；拍法：手上拿什麼要寫。 | s18：`held open by two hands in faded blue-grey cuffs under old grey cloth sleeves, the other two folded red certificates pinched against the back of the sheet by his left thumb`；s19、s20 照抄同一句。 |
| 11 | s24 | s22 官帽歪了、s25 雙手扶正，夾在中間的 s24 沒寫帽子。 | 連戲。 | comp 加：`his official hat still knocked a little askew`。 |
| 11 | s15 | 「framed from the chest up」，動作卻是木棍敲左掌心，手多半在畫框外。 | 拍法：每鏡一個看得見的動作。 | 改成 `framed from the waist up`（本鏡沒有刀，不需要像第 6 集那樣框到胸口以上）。 |
| 11 | s06 | 遞出去的是「oiled-paper packet」，s07 放進掌心的卻是三份摺起的紅紙婚書，中間少了打開的一步。 | script c06–c07（抖開油紙包、抽出三份）。 | 簡化成 s06 直接遞紅紙：`pulls three folded red paper certificates from inside her jacket with her right hand`。油紙包與配婚令留在台詞與設定裡，不拍。 |
| 11 | s02、s23、s27、s29、s34 | 唐小棠的身分句含「a small gold abacus hanging at her waist」，每鏡又抱一把素木算盤。s23 只寫「an abacus hugged to her chest」，沒用 ABACUS 的固定描述，兩把算盤可能混成一把。 | bible 角色表（腰間小金算盤＋抱素木算盤）；道具固定描述每鏡照抄。 | s23 改用 `holding {ABACUS} against her chest`；五鏡都加 `the small gold abacus stays hanging at her waist`。 |
| 11 | s27 | 畫右緣「one young woman's grey-white cotton shoulder」不點名。第 10 集遠處或邊緣不點名的人，會照前景人物的配色長成分身。 | e910 picks-b s30（遠處的人變第二個唐小棠）。 | `at the right edge, soft and out of focus, only one grey-white cotton sleeve and shoulder of a third woman whose head is outside the frame`。 |
| 11 | 全集 extras | 第 10 集兩個種子各有一支整段霓虹線、紅色珠串、閃電般的條紋（seed 故障）。e910 的 extras 只補了「no subtitles」。 | e910 picks-a s02、s05、s29、s35，picks-b s02、s05、s27、s29、s33、s35、s38。 | e911 extras.json 的 `One continuous shot.` 替換句加：`no neon lines, no glowing streaks, no light rain, no strings of beads and no glitch effects anywhere`。 |
| 11 | 全集 Xu 嚴肅鏡 | 許硯整集不笑，第 10 集 s04、s13、s36 還是帶笑。preflight 的 `smile-ref` 只認 t1 的檔名，抓不到 l1。 | bible 角色表（嚴肅鏡用 `drop_pictures` 拿掉帶笑那張）；e910 picks-a s04、s13。 | 草稿第一輪就看 s03、s08、s10、s19、s20、s28、s30 有沒有笑；有就在 spec.json 對那幾鏡 `drop_pictures` 帶笑的角度圖。preflight 的 `smile-ref` 改認 l1 檔名，另開票。 |
| 11 | s16 | 胡縣令原本面向畫左，「turning to his right」會先背對鏡頭才轉到畫右；這是一個沒必要的背影。 | 拍法：講話的人面向聽的人。 | `turning toward screen right, his face in profile toward the constable` |

## 本集避開了的原版必修

- 婚書的「囍」字印：s18、s19 寫空白紅紙＋空方印框，避開了。
- 三女在「交出她一個」時甜笑：s27、s29、s34 寫 NOSMILE＋驚慌；s35 三女拿掉。避開了。
- 縣令「退後！」沒揮袖：s22 寫兩袖連揮兩下、官帽歪。避開了。
- 唐小棠舊版齊胸裝：改用 l1 交領，避開了。前提是 spec.json 照上面必改那一列建好。

## 最重要的五條

1. **s28、s29、s24（加 s04、s12、s23）畫外句與心裡話**：拿掉 builder 自動補的 `speaks off screen`，s29 的心裡話尤其不能寫成說話；每鏡都寫硬「He／She says nothing… no mouthing words」。第 10 集 s16 就是這樣整鏡重拍。
2. **兵器三處**：`ZHAO` 的「no sword written」漏進 4 鏡；`NOSHARP` 補刀鞘，並拿掉衙役手上的木棍；s17 的鐵尺改成按腰帶。
3. **s06、s14 唐小棠背影鏡**：拿掉轉頭與遞向畫右的寫法，讓她正對畫面深處；s14 縣令「嘴半張又嘴閉著」二選一；先建好 e911 的 extras.json 與 spec.json 再拍。
4. **s32、s35 耳語**：站位改成縣令在畫右、許硯左肩後耳語，許硯幾乎正面、看畫右鏡外。這樣對上 bible 的「左耳」與第 12 集「正眼看胡縣令」。s35 拿掉前景「a man's right fist」。
5. **全景與接戲**：s22 補許硯（第三個名額），s05 鏡頭只朝院門，s19 阿令仍被架著。

## 採納情形（寫稿者，2026-11-14）

**必改 16 條全改**（`r2.py` 重建 `video.json`、`overlays.json`、`storyboard.md`；`storyboard-check.py` 0 錯）：
- s24、s28、s29 畫外句：`build-r2.py` 加開關 `OFFSCREEN_SPEECH`，本集設 `False`，提示詞不再補「… speaks off screen」「the system voice speaks off screen」（不靠 spec.json 刪）。s04、s12、s23、s24、s28、s29 的 motion 都寫「says nothing … no mouthing words」（放在動作後面，放開頭會被 shot_reading 判成只有反應）。e910 照舊（沒設開關），重建後三個檔逐位元相同。
- s02：`nospeak=["xuyan"]`，寫成張嘴喊一聲。
- `ZHAO` 改成腰間只有黑布帶；`NOSHARP` 照建議改寫（刀鞘、布帶、另一手空著）；s17 改按布帶，加 NOBLADE。
- s06、s14 照建議改寫；s19 阿令仍被架著；s22 補許硯（三人）；s05 鏡頭只朝院門；s32、s35 用同一句站位（`WHISPER`），s33 耳朵在畫左緣；s35 改成他自己的右拳。
- `colab/runs/e911/extras.json`、`colab/runs/e911-live/spec.json` 已建：s06、s14 拿掉唐小棠三張臉部圖與身分句、「Only these 2 people…seen only from behind」；s02、s23、s27、s29、s34 用 e910 s36 的中性外貌句。

**建議**：
- 採納：s02 鏡位；月亮照第 10 集；近景背景（`DARK`）；人數寫死；HU_BACK／HIM_BACK 頭整個轉開、左肩；s01、s04、s24、s26、s27、s30、s31、s33 的「only person」句在 spec.json 改寫；s21 買 8；s01、s34 `act=3`；inner 的 emotion 只寫「沉」；s18–s20 另兩份婚書；s24 官帽歪；s15 改中近景（腰以上）；s06 直接遞紅紙；小金算盤每鏡寫、s23 用 ABACUS；s27 第三人的袖與肩；extras 加不要霓虹線與故障效果；s16 朝畫右轉。
- s28–s29 長度：錄音後量過，s28 三句 11.9 秒，超過 10 秒能裝的量，最後一句系統吐槽延到 s29 開頭；另外 s25（9.1 秒）改買 10、s09 改買 8。
- 沒採納或延後：
  - s05「畫面火把不超過八支」：這鏡寫死了九個衙役、趙捕頭、兩個家丁各一支（共十二支）。台詞是「攔得住幾個」，人要多；s11、s22 有寫上限。
  - 許硯嚴肅鏡帶笑：要看草稿才知道，第一輪挑片時看 s03、s08、s10、s19、s20、s28、s30。
  - preflight 的 `smile-ref` 改認 l1 檔名：共用工具，不在本集範圍，要另開票。CG 那一層的 st1 預檢對 s06 仍報這條（送的是 CG 的 `xuyan-portrait-t1`），真人那一層（d1）0 警告。
