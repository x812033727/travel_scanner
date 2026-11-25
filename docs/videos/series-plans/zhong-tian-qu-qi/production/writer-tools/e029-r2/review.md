# 第 29 集重製版 r2（e029-r2，內部 929）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿：沒參與寫稿的獨立代理，2026-11-17，開拍前最後一關。只寫這一個檔；沒改別的檔、沒用 Colab／RunPod／付費服務、沒 commit。
- 審的對象：`docs/videos/zhong-tian-qu-qi-e029-r2/{script.md,storyboard.md,video.json,overlays.json}`、`writer-tools/e029-r2/r2.py`、`colab/runs/e929/extras.json`、`colab/runs/e929-live/{mkspec.py,spec.json}`、`hailuo/clips-dh-e929.json`（精修文字），以及實際要送的 `~/mokaair-work/videos/zhong-tian-qu-qi-e929-dh/runpod/live/d1/colab-jobs.json`（70 支＝35 鏡 × 2 種子）與 `prompts/`；錄音 `audio/`（`README-retakes.txt`、`fw929.txt`、`fw929-retake.txt`、`f0y929.txt`、32 個 wav、`take1/`、`take2/`）。
- 對照：`r2-bible-e021-e030.md`（拍法 1–30、接點 28→29／29→30、小角色、道具表、好感帳）、`r2-bible-e011-e060.md`、`season-01.md` 第 29 集、`writer-tools/e028-r2/review.md`、`colab/runs/e925-live`～`e927-live` 的 `review-picks-{a,b}.tsv` 與 `picks-merged.tsv`、任務檔 `tasks/open/2026-11-07-zhong-tian-live-action-remake.md` 第 14–25 集的教訓、第 28 集 d1 的 s37–s39、`assets/refs-live/README.md` 第 29 集段。
- 參考圖：本集要送的 20 張（十張新圖、正午五張舊裁切、五張定妝照）全部縮成小 jpg 放大看過，`prop-huangzhi-l1` 另外 1:1 看了中央一塊；午後四張裁切與正午版逐張算了平均 RGB。用完已刪。
- 錄音：a04、a05、a07、a09、a10、a18、a31、a32 用 YIN 另外量了一次（40 ms 窗、10 ms 步、門檻 0.15，numpy 陣列，一次一支），跟 `f0y929.txt` 一致（a09 164、a10 177、a18 200、a31 262、a32 260 Hz）。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| 分隔句 | 70 支 d1 提示詞每支 `never the mood. ` 與 `One continuous shot.` 都剛好一次；`prompt_sha256` 全部跟檔案相符；兩個種子的提示詞與參考圖逐位元相同。clips-dh 35 鏡每鏡 `the set layout stays as it is. ` 剛好一次 |
| d1 漏進精修句 | **沒有**。第 28 集那種 `... the young woman seen only from behind shown in <Picture 1> keep(s) the same ...` 一支都沒有。s10、s11、s15、s21、s28 五支插鏡 d1 裡的 `Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood.` 是插鏡的標準句（e926 有 10 支、e927 6 支、e928 4 支同一句），不是漏句 |
| 參考圖路徑 | 70 支全部是絕對路徑、檔案都在；`set-guangchang-l1`（gen-dh 的 SET 句）一支都沒送；唐小棠的圖九個背影鏡都拿掉了；`xuyan-angle-b-l1` 整集沒送 |
| open／畫外的人 | 提示詞與精修文字都沒有 `open`、`lantern`、`plaque`、`sign`、`banner`、`brush`、`Tang Xiaotang`、`stand-up collar`、`Constable`；沒有「朝畫外那個年輕女子」；`young woman` 只出現在她自己的九個背影鏡。點名的視線只有 s01 `toward Xu Yan`（他在畫面裡）。其餘對畫外說話都寫「someone out of sight」或地點（the platform、the square、the earth below the platform） |
| 縣令 | s01、s05、s06、s12、s25 都寫 `black gauze futou hat with two short stiff flat wings`；驚堂木都寫長方形木塊；跟孫掌櫃不同鏡；第二場不入鏡 |
| 魏少卿 | 扇子每鏡合著（s05、s08、s12、s13、s22、s30、s31）；s22 `cold and blank, not smiling ... the corners of his mouth pulled down`；s08、s13、s31 照稿子可以笑 |
| 人數與衣服 | s01 四人、s05／s12 十二人（八個鎮民八套衣服）、s18 兩人、s27 八人（六個客人六套衣服）；寬景都寫 `dark cloth shoes` |
| 一鏡一動作 | 35 鏡都只有一個主動作；s03 吞下、s07 一抖、s23 跪下都在第一格前把前置動作做完 |
| 面板 | `overlays.json` 只有 s29 兩塊，跟聖經好感帳第 29 集列相同（「物證：柳葉水印」「毒糖批號：查無此批」照聖經拿掉）；本集沒有好感面板 |
| 接點 28→29 | s01 跟第 28 集 s39 同一刻：胡縣令在紅布案後、賴三跪著的背影「tied hands lowered」、魏少卿坐台右木椅、許硯在台左；s05 鎮民第一格舉著手、慢慢放下，正好接第 28 集 s39 的指向。通過 |
| 接點 29→30 | s35 唐小棠在許硯身後、抓他的左袖、帳本夾左臂，許硯挺肩朝畫右（唐萬金來的方向；s34 他往畫左奔，反打方向對）。通過（「往許硯身後退一步」見建議 12） |
| 錄音長度 | 照 `r2.py` 的 BUY 與 `fw929*.txt` 的人聲終點逐鏡核過，每鏡都放得下：最緊的 s07（a07 5.92 秒、人聲到 5.74）、s22（a20 5.84、到 5.52）、s25（a23 7.12 秒買 8）、s31（a29 7.08 買 8）。**s04 的 a04＋a05 放得下**：兩句實際人聲 2.30＋0.5＋2.30 ≈ 5.1 秒，s04 是不說話的鏡、a04 可以從第 0 秒放，6 秒片還有約 0.9 秒餘裕 |
| 光源方向 | 正午五張裁切的影子都往左、略朝鏡頭（`-zuo-l1` 木箱影、`-tai-l1` 木箱與椅子影），跟提示詞「from the upper right behind, long shadows falling to the left」一致；s09「low sun at the upper right」與 `-shu-l1`、`-tai-l1` 母圖右上的太陽一致 |

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| `prop-huangzhi-l1` 細纖維像筆畫 | **會。要重做（免費）**。1:1 看中央：九十條深色細纖維裡有好幾處互相交叉或分岔，成「十」「丁」「人」形的接點（例如中央偏右一個十字），顏色又是近黑的深褐；H3 放大 1.8 倍後最容易把它們連成筆畫——而這一鏡的劇情正是「什麼都沒有」 | 必改 1 |
| `-di-l1`、`-pm-di-l1` 當插鏡底圖會不會把東西放到地上、長出廣場 | **s28 會把東西放到地上，要改；s15 有可能，要改字**。兩張都是由上往下看的一片土（`-di` 還偏粉紅、滿是小點，縮小看像皮膚毛孔）。s28 寫的是「木箱的箱底」，送的卻只有土，照第 16 集教訓「場景圖的狀態會壓過文字」，最可能畫成土地上一包紙；s15 帳本「舉在地面上方」也可能被放到地上。長出廣場的風險低（圖本身沒有遠景），可以接受 | 必改 2、8 |
| 午後調色很輕、天空仍藍、暖金斜陽靠文字 | **可以開拍，不必重調**。算過平均 RGB：午後四張裁切的藍色比正午低 26–31（`-zuo` 81→55、`-shu` 189→158、`-tai` 127→100、`-you-wu` 81→56），地面確實偏橘；天空仍藍是對的（冬天下午三四點不是黃昏，s31 魏少卿才說「日落才算」）。暖金色靠提示詞、配樂與台詞「下午」交代，接受。若想更明顯，見建議 13（免費，但不要把天空推成橘色） | 建議 13 |
| s30 唐小棠背影＋遠處台上魏少卿 | **可以，補一句位置**。風險是她在畫面正中、他在她頭後面被擋住，或模型把他畫大。寫明他在她右肩外、小小的、整個人不跟她重疊 | 建議 1 |
| s35 背影雙人鏡：轉頭、被擠到畫緣 | **要改**。現在寫她在畫面正中、從近背後拍到腰，他在她前方「半步、稍偏右」——鏡頭在她背後，他正好落在她的頭與丸子後面；模型要讓他看得見，只能把他推到畫緣或把她挪開。另外「turns his head」沒有寫肩膀不動，容易整個人轉過來 | 必改 6 |
| s27 六客人加許硯與她的背影（分身） | **要改**。六個客人面向鏡頭，其中兩位女客只寫衣服、沒寫年紀與髮型，最可能長出一個梳雙丸子的年輕女子正臉（第 27 集挑片 s05 丸子盤錯、第 25 集正臉分身）；許硯「side-on to us」又「face three-quarter to screen left toward the line」自相矛盾（他在她右邊，朝畫左看的是她，不是隊伍）；only 句把她算成 named people | 必改 5 |
| s01、s05、s12 三張臉加跪著的背影 | **照寫，可以開拍**。s05、s12 的寫法跟第 28 集審稿必改給 s39 的那句逐字一樣、人在全景裡都很小，第 1 條只算看得到臉的三人；s01 是 `-tai-zhong-l1` 的中景、四張圖剛好對應台上四個位置。只補 s01 魏少卿手上的扇子（s05 他膝上有扇，兩鏡之隔不能憑空出現） | 建議 2 |
| a09、a10 許硯偏高（164／177 Hz，畫外句） | **要處理**。s10、s11 兩支插鏡沒有片中原聲，放的就是錄音；同一段的 a07 120、a16 100、a19 122 Hz（s21 也是畫外插鏡），三支畫外句前兩支比第三支高 5–6 個半音，連著聽會像換了人 | 必改 7 |
| a18 孫掌櫃 199 Hz | **片中原聲為主，錄音當備援要先處理**。他同集 a21 是 106 Hz、第 28 集 114–117 Hz；a18 若用上，比 a21 高約 11 個半音 | 建議 9 |
| a31 唐萬金 261 Hz 與唐小棠重疊 | **片中原聲為主；錄音備援要降**。s34 緊接 s35 的 a32（唐小棠 260 Hz），父女同一個音高連著播 | 建議 10 |
| a04＋a05 5.60 秒放 6 秒片 | **放得下**（見上表「錄音長度」） | — |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 29 | s11（圖 `prop-huangzhi-l1`） | 黃紙的九十條細纖維是近黑的深色細線，有幾處交叉、分岔成十字或丁字；放大成影片最容易被畫成筆畫或字，而這一鏡要證明的是「這張黃紙什麼都沒有」。提示詞的 `only lumpy fibres and small dark specks` 也把觀眾的眼睛引到纖維上 | 拍法 7、27（紙上的記號會長字）；`refs-live/README.md` 自己寫「挑片時仍看有沒有被畫成字」；1:1 看中央 560×315 一塊 | **重做這張圖（免費，Pillow）**：同一個裁切與調黃（`crop=408:230:772:116,scale=1312:736`，RGB × 0.97／0.85／0.56）、同一層低頻疙瘩；纖維改成 40 條、每條一段平滑弧線 15–40 px、顏色取當地紙色 × 0.80（淺褐，不用深色）、不透明度 0.5、高斯 1.2 px，**放之前檢查外框不跟已放的任何一條相交**（沒有交叉、沒有分岔）；黑點保留但減到 35 個。做完 4 倍放大逐格看沒有十字與接點，id 照樣 `prop-huangzhi-l1`（還沒送過，覆蓋不影響別集）。提示詞構圖段換成：`the sheet fills the frame, the sunlight coming through it dull and uneven, only soft lumps in the pulp, a few short pale hair-thin fibres lying apart from each other and small dark specks scattered through it, plain all over`；動作段的 `the lumpy fibres and dark specks showing and nothing else` 換成 `the soft lumps and specks showing and nothing else` |
| 29 | s28（圖 `set-guangchang-pm-di-l1`） | 鏡頭寫的是「糖箱裡的箱底」，送的卻只有一片由上往下看的土；場景圖會壓過文字，最可能畫成土地上一包紙、旁邊伸進一隻手，「箱底空了」就看不出來 | 第 16 集教訓「場景圖的狀態會壓過文字」；第 23 集「只送單色圖的近鏡會自己長東西」；第 28 集 s28 食盒插鏡換 `-di-zuo-l1` 的理由 | 圖照送 `-pm-di-l1`（土只當箱外的地），把箱子寫進第一格，構圖段換成：`insert close-up looking straight down into the open plain wooden chest standing on the packed pale earth, the very first frame is already a close view from above, from its very first frame: the four pale plank walls of the chest run along the four edges of the frame, its bare pale wooden bottom fills the middle, one small packet of plain blank white paper lying alone on that wooden bottom, a slender hand in a peach-pink silk sleeve cuff already resting on the packet; the packed pale earth shows only in the four corners outside the chest's rim; only the inside of the chest, the packet, the hand and its sleeve cuff are in the frame.` 動作段不變。挑片仍看紙包是不是在土上；兩支都在土上時 fix1 加第二張圖：`-pm-zuo-l1` 免費裁 `crop=448:252:640:330,scale=1312:736:flags=lanczos`（只有木箱與地，已看過），寫 `the chest shown in <Picture 2>, its lid lifted off` |
| 29 | s10 | 動作句自相矛盾：`slowly grows clearer as the sunlight strengthens through it ... and the hard winter sunlight stays unchanged`——同一句裡光既變強又不變，模型可能讓光閃一下或乾脆不動。另外 `prop-liuye-zhi-xin-l1` 葉子兩邊有兩束很粗的波浪纖維線，沒寫出來，容易被畫成橫過紙前的枝條或藤 | 一鏡一個動作、光源與圖一致；放大看 `-xin-l1` | 構圖段 `one faint willow-leaf shape in the middle, the soft fibres of the paper glowing` 換成 `one faint willow-leaf shape in the middle, two soft wavy bands of paper fibre running across the sheet behind it as part of the paper itself, the soft fibres of the paper glowing`；動作段整句換成 `As the camera pushes in, the faint willow-leaf shape in the middle of the sheet shows a little clearer in the light coming through, its thin veins showing one by one, and the hard winter sunlight stays unchanged.` |
| 29 | s34 | 唐萬金哭喊「囡囡」朝畫左外，提示詞寫了 `toward someone out of sight beyond the left edge of the frame`，**卻沒有寫那一側到邊緣只有景**（其他十二支對畫外說話的鏡都有）。他是全集最想撲向某人的一鏡，畫左緣最可能長出唐小棠的半張臉或背影 | 任務檔 e925 注意（「朝畫外那個年輕女子」畫出半張臉，改寫成看不到的人並寫明那一側只有景）；第 28 集審稿必改 3 | 構圖段 `his face three-quarter to screen left toward someone out of sight beyond the left edge of the frame, never the lens;` 之後補 `the left side of the frame is only the packed pale earth and the plank doors all the way to the edge, and he is the only person in the frame;`，並刪掉後面重複的 `he is the only person in the frame.`（改成 `the long low tiled building in the warm afternoon sun.` 結尾）。精修文字不用改（只描述他） |
| 29 | s27 | (1) 六個客人面向鏡頭，兩位女客只寫衣服（`a woman in a dull blue jacket and long skirt`、`a woman in a faded green jacket`），沒寫年紀與髮型——最可能長出一個梳雙丸子的年輕女子正臉，等於唐小棠的分身露臉；(2) 許硯 `side-on to us` 又 `face three-quarter to screen left toward the line`：他站在她右邊，朝畫左看的是她，隊伍在桌子那頭的縱深裡；(3) only 句寫 `Only these 2 named people, the young woman seen only from behind and Xu Yan`，把不點名的她算成 named | 拍法 3（她不露臉）；第 25 集正臉分身、第 27 集挑片 s05（丸子盤成四個髻）、第 26 集挑片 s35（客人分身）；拍法 25「群眾的反應用背影或側臉代表」 | 客人那段換成：`beyond the table, soft and a little out of focus, six customers in a short line facing us, each a different age and dress: an old man with a grey beard in a brown robe, a grey-haired old woman in a dull blue jacket with a dark head cloth, a stout bald man in an indigo robe, a middle-aged woman with greying hair under a faded green head cloth, a boy in a patched tan jacket and a man in an ochre robe, only the first of them sharp, their lips closed;`。許硯那段換成：`at her right and half a step back from the table, Xu Yan, ..., standing, framed from the waist up, one plain brown cloth money pouch tied at its neck in his left hand, his face in profile to screen left toward the first customer across the table, never the lens, a small closed-lip smile, his lips pressed shut;`。only 句換成：`Only Xu Yan, the young woman seen only from behind and the six customers the composition describes are in the frame; she is the only young woman in the frame; no second copy of anyone appears.` |
| 29 | s35 | 構圖會擠人：她在畫面正中、從近背後拍到腰，許硯在她前方「半步、稍偏右」——正好被她的頭與兩顆丸子擋住，模型要讓他看得見只能把他推到畫緣或把她挪開；`Xu Yan turns his head over his left shoulder` 沒寫肩膀不動，常會整個人轉過來（變成正面對鏡頭、她也跟著轉） | 第 28 集審稿（s08、s16 背影雙人鏡的推力）；第 25 集挑片 s08、s15（側臉在畫緣）；拍法 3 | 構圖段 `half a step beyond her and a little right of the middle, Xu Yan, ...` 換成 `one step beyond her in the right third of the frame, his upper body clear of her head and shoulders, Xu Yan, ...`；`she stays in the middle of the frame the whole shot, close behind his left shoulder` 換成 `she stays in the middle of the frame the whole shot, her right arm reaching out to his left sleeve`；動作段換成 `Only Xu Yan's head turns over his left shoulder and he looks down at her once, steady and not smiling, his shoulders staying squared toward screen right;` |
| 29 | s10、s11（錄音 a09、a10） | 兩支畫外插鏡放的就是錄音：a09 164 Hz、a10 177 Hz，同一場許硯 a07 120、a16 100、a19 122 Hz（a19 也是畫外插鏡 s21）。s10→s11→（s21）三句連著聽，前兩句高 5–6 個半音，會像換了一個人 | YIN 另量一次：a09 164（p10 105、p90 185）、a10 177（p10 140、p90 199）；README-retakes 本身建議降 2–3 個半音；第 25、28 集用過的濾鏡 | 兩支都降（formant 保留、長度不變）：a09 `rubberband=pitch=0.84:formant=preserved`（−3 st → 約 138 Hz），a10 `rubberband=pitch=0.79:formant=preserved`（−4 st → 約 140 Hz）；另存新檔（例如 `zq929a09-p84.wav`、`zq929a10-p79.wav`）、原檔不動，剪接表指新檔。降完再用 YIN 量一次（目標 125–145 Hz）、faster-whisper 帶上下文聽寫一次（變調錄音一律帶上下文，第 21 集教訓），再請人耳聽 |
| 29 | s15（圖 `set-guangchang-di-l1`） | (1) `resting one fingertip`、`The fingertip slides` 是單根手指的動作，第 16 集教訓會被讀成比中指；(2) 帳本只寫 `held level in the sun above the packed pale earth`，沒寫拿在哪裡，送的圖又是一片由上往下看的土，帳本最可能被放到地上（她在 s14、s16 都抱在身上） | 任務檔第 16 集「單根手指的手勢會被讀成比中指，寫張開手掌」；第 16 集「場景圖的狀態會壓過文字」；道具與手的位置寫在第一格 | 構圖段換成：`insert close-up from a low side angle, the very first frame is already a close view of the edge of one thick stack of plain blank paper sheets stitched along one edge with cord, lying open along her left forearm in a peach-pink silk sleeve at waist height, from its very first frame, its top sheet blank and pale, a slender right hand in a peach-pink silk sleeve cuff already resting two fingertips together near the top of the sheet; far below, soft and out of focus along the bottom edge, the packed pale earth with the long thin shadows of bare branches; only the stack of blank sheets, her forearm, the hand and their sleeve cuffs are in the frame.` 動作段換成：`Her two fingertips slide slowly down the blank sheet together and tap it twice, and the hard winter sunlight stays unchanged.` |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 29 | s30 | 她在畫面正中、從背後拍到腰，魏少卿在「beyond her」沒寫左右，可能被她的頭擋住或被畫大；他站在台右木椅旁，照母圖本來就在她右肩外 | 背影雙人鏡的推力；`-pm-tai-l1` 的椅子在台右 | `beyond her, small and soft on the low stone platform, standing beside the dark wooden armchair` 換成 `beyond her right shoulder, small and soft on the right side of the low stone platform, standing beside the dark wooden armchair, his whole figure clear of her head and shoulders` |
| 29 | s01 | 魏少卿手上沒寫扇子（`their hands hold only what is described here` 會讓他空手），兩鏡後 s05 他「closed fan on his knee」 | 接戲；拍法 30 | 魏少卿那段 `sitting back, small, his lips closed, never the lens` 換成 `sitting back, small, his closed fan resting on his knee, his lips closed, never the lens` |
| 29 | s16、s24 | 從背後拍她、背景卻是「禿樹的枝與晴空」，沒寫低角度；鏡頭在人眼高從她背後拍，眼前應該是台子與台上的人，模型可能自己補出台上的臉 | 第 28 集 `-shu-l1` 都配低角度近景；拍法 25 | 兩鏡 `close-up from close behind one young woman` 換成 `low-angle close-up from close behind one young woman, the camera a little below her shoulders looking up past her head` |
| 29 | s20 | `two hands ... reaching in from behind his shoulders, already pressed flat on his back`：從正面拍到胸口，按在背上的手看不到；模型會讓手從他肩後冒出來，常連帶長出手主人的臉 | 第 25 集挑片 s02（兩隻手像兩個人）；拍法 1、25 | 換成 `two hands in plain grey cotton sleeves already gripping the tops of his shoulders from behind, the arms coming in from the upper left and upper right edges of the frame, unnamed`；動作段不變 |
| 29 | s25 | `his face three-quarter to screen right toward the middle of the platform below`：賴三在台中央前，從案後看是正前方，不是畫右；畫右下是孫掌櫃所在的台下（s19、s22 都朝畫右下） | 軸線（s19 賴三朝畫右下指孫掌櫃、s22 魏少卿朝畫右下） | 兩處換成 `his face three-quarter to screen right toward the square below at the lower right` |
| 29 | s12 | `points up at the white sheet` 單手一指，第 16 集教訓；她是背影、虛焦，風險小 | 第 16 集教訓 | 換成 `raises her open hand toward the white sheet` |
| 29 | s29 | 錢袋 s27 在許硯左手、s29 在右手 | 接戲 | s29 `in his right hand` 換成 `in his left hand`（或照必改 5 的 s27 寫法把兩鏡都定成左手） |
| 29 | s32 | 只有鄭伯一人卻寫 `behind them the long low tiled building` | 文字一致 | `behind them` 換成 `behind him` |
| 29 | s20（錄音 a18） | 199 Hz，同集 a21 106 Hz、第 28 集 114–117 Hz；s20 是畫面上說話、以片中原聲為主，但若原聲不能用，備援差 11 個半音 | YIN 另量 200 Hz；第 19 集「變調大的句子調到聽寫開始錯字就停」 | 先免費再錄一次（站台 TTS 沒有扣費）：情緒寫「臉色發白、急著否認、聲音低沉發緊、不笑，句首不要笑聲」；沒有更好的才用 `rubberband=pitch=0.75:formant=preserved`（約 150 Hz）、帶上下文聽寫、耳聽 |
| 29 | s34（錄音 a31） | 261 Hz，緊接 s35 唐小棠 a32 260 Hz；父女同音高連播 | YIN 另量 262 Hz；第 25 集唐萬金字條與鄭伯同音高的處理 | 以片中原聲為主；用到錄音時 `rubberband=pitch=0.71:formant=preserved`（−6 st，約 185 Hz）、帶上下文聽寫（「囡囡」容易聽成「難難」）、耳聽 |
| 29 | s33 | 她說「那是唐家的車」，畫面裡只有瓦屋與木板門，看不到車；s32 剛拍過車在畫右 | 接戲（s32 車在畫右緣） | 背景段 `beyond her, soft, the long low tiled building and its plank doors` 換成 `beyond her, soft, the long low tiled building and its plank doors, and the black lacquered carriage body small at the right edge, its door swung back`（只寫車廂，馬與人照拍法 26 不寫） |
| 29 | s35 | 季綱與接點 29→30 寫「唐小棠往許硯身後退一步」，分鏡改成她已在他身後、由他回頭；可以接受，但若必改 6 改完仍被擠到畫緣，換她做動作更穩 | `season-01.md` 第 29 集結尾；聖經接點 29→30 | 備案（fix1 用）：動作段換成 `She steps half a step back behind his left shoulder, her right hand keeping its grip on his sleeve, her head still; Xu Yan stays still, his shoulders squared toward screen right` |
| 29 | 午後五張圖 | 調色輕、天空仍藍（判斷見上表，接受）。若想讓午後更明顯 | 聖經〈挑定以後要做的免費圖〉 | 可選、免費：在 `set-guangchang-pm-l1` 上再疊一次 `colorbalance=rm=0.05:bm=-0.05:rh=0.04:bh=-0.06,eq=gamma=0.95`，照原命令重裁五張（`-pm-tai`、`-pm-zuo`、`-pm-shu`、`-pm-you-wu`、`-pm-di`）；看 `-pm-shu` 的天空仍是藍、不是橘，才換 |
| 29 | clips-dh（精修文字） | 15 鏡的說話句仍是通用的 `turned toward the person he is speaking to`（例如 s03、s06、s34 畫面裡沒有那個人）；第 28 集 17 鏡同樣，精修有首格撐著，風險低 | 任務檔「還沒解決 (2)：d1 鏡的精修文字跟草稿拍攝時的不同」 | 不擋開拍；挑片後精修若畫面邊緣多出人，fix 時把該鏡精修句換成 d1 的方向句（例如 s34 `his face three-quarter to screen left, his eyes beyond the left edge of the frame`） |

## 參考圖要做的事（都是免費的）

- **重做**：`prop-huangzhi-l1`（必改 1：纖維變淺、變少、不交叉、不分岔；同 id 覆蓋，還沒送過）。
- **不用重裁或新增**：`-di-l1`、`-pm-di-l1` 照用，改的是 s15、s28 的提示詞（必改 8、2）；s28 兩支都失敗時 fix1 才加 `-pm-zuo-l1` 的木箱裁切 `crop=448:252:640:330`（新 id，例如 `set-guangchang-pm-xiang-l1`）。
- **可選調色**：午後五張（建議 13），不做也可以開拍。
- 其餘七張新圖（`prop-liuye-zhi-xin-l1`、`set-guangchang-an-l1`、`-pm-l1` 與四張午後裁切）放大看過照用：`-xin-l1` 沒有燈架、攝影機、人與手，四邊都在紙裡（葉子是寬卵形不是細長柳葉，聖經已挑定，接受）；`-an-l1` 上緣兩根黑色細腳是台後高架，沒有字、沒有人。

## 總結

- **必改 8 條**，全部是改提示詞文字、免費重做一張圖、免費變調兩句錄音，不花 Colab 點數、不用試鏡。
- 最重要的五條：
  1. **s11 黃紙圖重做**：深色細纖維有交叉與分岔，最容易長成字，而這一鏡的劇情就是「什麼都沒有」。
  2. **s28 箱底送的是土**：會畫成土上一包紙；把木箱四壁寫進第一格。
  3. **a09、a10 降調**：兩支畫外插鏡放的就是錄音，比同場許硯高 5–6 個半音（×0.84、×0.79，formant 保留，量過再用）。
  4. **s27 客人分身與許硯方向**：兩位女客寫年紀與頭巾、客人虛焦、只有第一位清楚；許硯改側臉朝第一位客人。
  5. **s34 補「那一側只有景」**：全集最想撲向某人的一鏡，獨缺這句，畫左緣最可能長出唐小棠。
- 寫稿者的十個疑問：黃紙要重做；`-di` 系列 s28 要改、s15 改字；午後調色接受；s30 補位置；s35 要改；s27 要改；s01／s05／s12 照寫（s01 補扇子）；a09／a10 要降；a18、a31 以片中原聲為主、備援要處理；a04＋a05 放得下。
- 機械檢查全過：分隔句各一次、沒有精修句漏進 d1、絕對路徑、沒有 open、不點名畫外的人、縣令帽翅、沒有掛著的東西、人數與衣服、一鏡一動作、扇子合著、s22 不笑。
