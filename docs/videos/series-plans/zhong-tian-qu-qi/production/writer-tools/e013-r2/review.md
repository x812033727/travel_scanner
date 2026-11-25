# 第 13 集重製版（e013-r2，內部編號 913，真人版）分鏡與提示詞：開拍前獨立審稿

- 審稿：沒參與寫稿的獨立審稿代理，2026-11-14，只讀（只寫本檔）；沒用 Colab、RunPod 或任何付費服務，沒有 git commit。
- 審的版本：`docs/videos/zhong-tian-qu-qi-e013-r2/{script.md, storyboard.md, video.json, overlays.json}`、`writer-tools/e013-r2/r2.py`、
  `colab/runs/e913/extras.json`、`colab/runs/e913-live/{spec.json, mkspec.py}`，以及**實際要送 Colab 的**
  `~/mokaair-work/videos/zhong-tian-qu-qi-e913-dh/runpod/live/d1/colab-jobs.json` 與 `prompts/ref-s01…s42-913110{1,2}.txt`
  （兩個種子的提示詞逐位元相同；`preflight-prompts.py` 跑過：0 錯 0 警告）。錄音長度用 `…/e913-dh/audio/zq913a01–a36.wav` 量。
- 對照：`r2-bible-e011-e020.md`（拍法 1–17、場景格局、接點）、`r2-bible-e011-e060.md`、`season-01.md` 第 13 集、
  `writer-tools/e011-r2/review.md`、`e012-r2/review.md`、`colab/runs/e911-live/{review-picks-a.tsv, review-picks-b.tsv, pick-review.md}`、
  第 12 集 r2 s32–s35、`assets/refs-live/`（逐張看過 `set-xujia-yuan-l2`、`set-xujia-yuan-ye-l1`、`set-mujiang-fang-l1`、`set-zhulin-fen-l1`、`shimujiang-portrait-l1`）、
  `animation-preproduction/references/{storyboard-shot-spec.md, script-to-storyboard.md}`、`animation-camera/SKILL.md`。

## 總評

台詞、劇情、好感與接點都照細綱，兩頭接點（12→13 熄了的火把在畫左石桌角、許硯披舊灰外衣站原地；13→14 柴刀在喉前、許硯左手燈籠右手舉起、墳在她身後紙錢在燒）都對。
第 12 集審稿的寫法（畫外句不補、不說話的人寫硬、紙空白正面打光、過肩前景不點名不送圖、唐小棠拿掉臉部圖）幾乎都照做了，一鏡最多三個有名字的人、參考圖送法、秒數都放得下錄音。
問題集中在三處：**場景圖本身**（竹林那張是插畫風、墳後一座有匾有紅燈籠的大屋；白天院子是油菜花田、滿樹柿子、左邊斜靠一束長竿——e911 的紅纓槍架正是長在這個位置）、
**幾鏡的提示詞自相矛盾**（s35 讓別人進畫、s32 同時要笑與不笑還要背影轉頭、s25 站位在場景圖上站不下去），以及**拿東西的手沒寫成畫面左右**（柴刀與唐小棠的幾鏡）。

必改 **9** 條、建議 **18** 條。**要重畫（改圖）的參考圖兩張**：`set-zhulin-fen-l1`（重畫，影響 s35–s42 共 8 鏡）與 `set-xujia-yuan-l2`（照圖改一版 l3，影響 s01–s12）。

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 13 | s35–s42（參考圖 `set-zhulin-fen-l1`） | **竹林場景圖要重畫**。(1) 畫風是插畫／3D 卡通（平塗的竹、卵石堆），跟其他真人場景圖與 "Photorealistic live-action" 打架，Ref2VA 會把整場拉成動畫質感。(2) 墳正後方是一座有屋脊、**匾上有假字**、**兩盞紅燈籠**的大屋，大屋佔畫面中央三分之一；s38、s40、s41、s42 從畫左往畫右拍秦霜，背景正好就是這座屋。提示詞只在全景 LOC 寫「every lantern there dark and unlit, its board blank」，模型照圖會點亮燈籠、長出匾字，正是原版第 13 集「竹林遠景多一個提燈籠的人影」與 e911「紙長字」的條件；劇情上竹林無名墳後面冒出一座祠堂也說不通。(3) 墳是一堆圓卵石，不是「土墳」；木牌是一塊大招牌立在柱上，像路標，空白大木面也最容易長字。 | bible〈要試鏡的新場景〉第 13 集竹林：「密竹、窄土路、小空地、小土墳、墳前一塊空白木牌、無月、星光冷藍」，沒有屋；bible 原版必修第 13 集；拍法第 7、8 條；e911 pick-review（紙與匾長字）。 | 用 `set-zhulin-fen-l1` 做 Qwen-Image-Edit 改一張 `set-zhulin-fen-l2`（或重抽兩個種子由站主挑），改圖提示：`Photorealistic night photograph shot on a cinema camera, real bamboo, real soil. Remove the building completely: its roofs, walls, doorway, the plaque and both red lanterns are gone, replaced by more dense tall dark bamboo and deep black shadow. Replace the heap of rounded stones with one small low mound of bare packed brown earth with a few dry bamboo leaves on it. Replace the signboard on the tall post with one short weathered wooden plank, knee high, stuck upright in the earth at the right front of the mound, its face completely blank and in shadow. No moon, faint cold blue starlight from above, no light source anywhere, no fire, nobody.` 改好前不拍 s35–s42。若站主不改圖：s37–s40、s42 近景不送這張圖（`drop_pictures: ["set-zhulin-fen-l1.png"]`），只靠文字。 |
| 13 | s37、s38、s39、s40、s42（`grove_c`）；s36、s41（`grove`） | 近景的場景句 `grove_c` 只有「deep night with no moon, cold blue starlight」，沒有一句說背景沒有建築、沒有燈。這幾鏡送的都是同一張有兩盞紅燈籠的圖，秦霜的近景背景就是那兩盞燈。全景 `grove` 的「the low dark roofs of an old empty hall far behind the clearing」等於叫模型把屋畫出來。 | 同上；bible 拍法第 8 條「寫明光源」；原版必修第 13 集（多一個提燈籠的人影）。 | `grove_c` 末尾加：`behind them only dense dark bamboo and black night: no building, no roof, no doorway, no lantern and no lit window anywhere in the background; the only warm light is the little paper fire low on the ground`（s37、s42 再加 `and the one lantern in the young man's hand`）。改圖後 `grove` 把 hall 那句整句刪掉，換成 `beyond the clearing only more dense bamboo fading into black`。 |
| 13 | s35 | 實際提示詞是「**Besides him, only the other people the composition names are in the frame**; no second copy of anyone appears.」——builder 的單人句被換成容許「其他人」的句子（構圖裡又出現 "only Xu Yan is in the frame" 這個字串，換錯了）。這是本集原版必修「竹林遠景多一個提燈籠的人影」的那一鏡，等於開門讓第二個人進來。 | `prompts/ref-s35-9131101.txt`；bible 原版必修第 13 集；script 場頭「竹林裡只有這兩個人」。 | 在 `spec.json` 的 s35 用 `replace` 把那句換成：`He is the only person in the frame and the only person in the whole grove; nobody else, no second lantern and no other light anywhere among the bamboo; no second copy of anyone appears.`（或修 builder，構圖文字不要寫 "only Xu Yan is in the frame"，改成 `Xu Yan alone`）。 |
| 13 | s32 | 三件事。(1) **同一鏡要笑又不笑**：comp 寫「pleased: a small closed-lipped smile」，motion 尾巴的 `quiet('Xu Yan')` 又寫「no smile at any moment」。(2) **背影轉頭**：許硯點了名、送三張圖，卻要「seen from behind at first, then his face turning to her in profile」——e911 選片的「背影轉頭」就是這種寫法，轉到一半會露出半張臉、轉過頭也可能直接回頭看鏡頭；唐小棠在他旁邊，模型也常把兩人一起轉。(3) 他轉頭看左邊的她，她「頭始終朝前」，兩人背影並排、一個轉一個不轉，最容易互相傳染。 | `prompts/ref-s32`；bible 拍法第 3、14 條；e911 review-picks（背影轉頭、笑場）；e012 審稿 s32。 | 兩人都只拍背影、都不轉頭，他的得意交給手勢：comp 改成 `on the right one young man seen only from behind, appearing only once: the back of his black topknot and his faded blue-grey robe, his head facing straight down the lane the whole shot, his ear, cheek and profile never visible`；motion 改成 `as they walk she pats the account book under her left arm (on screen left) twice; he lifts his left hand (on screen left, the hand next to her) beside her shoulder in a small thumbs-up without turning his head; neither of them turns their head at any moment`；刪掉 "small closed-lipped smile"；`chars` 拿掉 xuyan（不送他的圖），`spec.json` 加 `besides(...)` 那種只寫背影的句子。 |
| 13 | s41、s42 | **柴刀的手沒寫成畫面左右**。提示詞只寫「in her right hand」「held level in her right hand」。s41 她面向畫左（3/4 to screen left）、s42 她正對我們偏右：這時她的**右手在畫面左邊**（離許硯近的那邊）；bible 第 5 條卻寫「秦霜畫面右邊那隻手（寫 screen RIGHT）」。照 bible 字面寫 screen RIGHT，刀會在離他喉嚨遠的那一側、得橫過身體才碰得到；照現在只寫 right hand，模型分不清解剖右手與畫面右側（第 9 集阿令的匕首就是因此改寫成畫面側）。兩個寫法必須選一個、全片與第 14 集開頭一致。 | bible 拍法第 5、9 條；e009 r2.py（匕首寫死一側的手、不換手）；接點 13→14。 | 本集站位（許硯前景畫左、秦霜畫右正對我們）建議寫畫面左：s41 `the knife in her right hand, which is the hand on the screen-left side of her body, nearest him; it stays in that same hand on screen left the whole shot`；s42 `the knife held level in her right hand, the hand on the screen-left side of her body nearest him, its edge stopped one finger's width from the side of his neck on screen left, its blunt back toward the lens`。同時把 bible 第 5 條的「screen RIGHT」改註為「依站位寫畫面側；13 集 s41–s42 與 14 集開頭是 screen-left side of her body」，交給第 14 集照抄。 |
| 13 | s07、s10、s12、s21、s23（唐小棠背影）；s26 | **拿東西、動作的手沒寫畫面左右**。s23 最嚴重：「holds one account book … straight up … then raises one small round red lacquered box … in her other hand」——兩隻手都沒指定，而 s12 才剛寫書夾左臂、印泥盒塞右袖。s07「sets one hand on her hip」、s10「her right hand」、s12「left arm / right sleeve」、s21「her right arm」都只有解剖左右。從背後拍時解剖左右等於畫面左右，寫明就不會翻；寫不明模型會讓她轉身去找手。 | bible 拍法第 9 條；storyboard-shot-spec〈連戲〉「道具在誰手上」；使用者交代「手上拿什麼寫成畫面左右」。 | s23：`she holds the account book open in her left hand (on screen left), its blue cloth back cover toward us so no page faces the lens, then raises the small round red lacquered box in her right hand (on screen right) beside it`（「page turned edge-on」刪掉：從她背後拍本來就只看得到封底）。s07：`sets her right hand (on screen right) on her hip`。s10：`raises her right hand (on screen right) beside her head`。s12：`tucks the top account book under her left arm (on screen left) and slips the small red box into her right sleeve (on screen right)`。s21：`her right arm (on screen right) reaches straight forward`。s26：`one man's right hand entering from screen right`。 |
| 13 | s25（與 s27、s29 的背景） | **站位在場景圖上站不下去**。圖上的工作台貼著屋牆、在簷下，台後沒有站人的空間；提示詞卻寫石木匠「on screen right **across the bench**」，s27、s29 又讓他背後是「the dark wooden wall with tools」——等於他站在台子與牆之間。模型照圖會讓他穿牆、或把台子挪到巷子中間，三人戲的開場鏡（本場唯一交代三人位置的一鏡）會讀不懂。 | `set-mujiang-fang-l1`；bible〈場景格局〉「不要寫跟圖衝突的位置」；script 真人版改動「c24–c30 改在簷下工作台」。 | 三人都站在巷子這側、台子在他們面前：comp 改成 `medium shot from the lane side: the workbench stands against the wooden wall of the workshop under the eave, and everyone stands on the lane side of it; on screen left at its left end Xu Yan …; on screen right at its right end beside the bundle of bamboo poles Carpenter Shi, turned three-quarter to screen left toward him, leaning in over the board …; a step behind Xu Yan further to screen left Tang Xiaotang …`。s27、s29 背景照留（他在台子右端、斜對鏡頭，牆在身後是對的）；s28 許硯背後「the sunny lane」也對。 |
| 13 | s01、s03、s33（`yard`、`nyard`） | **院門位置寫得跟圖與 bible 都不一樣**。兩張院子圖的院門都在**後牆、屋子右邊緊鄰、門上一小片瓦頂（畫面中偏右）**；右邊那道牆上只有井與靠牆木板。LOC 卻寫「the packed-earth yard wall … on screen right with the plain wooden yard gate in it」。s01 全景秦霜牽馬「toward the yard gate on screen right」、s33 主觀鏡「walks on to the yard gate on screen right」，模型會在右牆另開一扇門（多出第二個院門），或讓人走向井。第 12 集沿用了同一句，但 bible〈場景格局〉明寫「院門在後面土牆上（中偏右、門上一小片瓦頂）」「不要寫跟圖衝突的位置」。 | bible〈場景格局〉許家院子；`set-xujia-yuan-l2`、`-ye-l1`。 | `yard`、`nyard` 改成：`the plain wooden yard gate in the back wall just right of the house, under its own small grey-tiled roof, the only gate in the yard; the packed-earth wall running along the right side with the stone well before it`。s01 motion：`Qin Shuang leads the horse past Xu Yan toward the yard gate at the back, right of center`；s03 `at the open yard gate at the back`；s33 `walks on to the yard gate at the back, right of center`。近景與中景的「toward the gate off screen right」可以照留（中偏右，方向一致）。 |
| 13 | s01–s12（參考圖 `set-xujia-yuan-l2`）；s33 次要（`-ye-l1`） | **白天院子圖要改一版**。(1) **畫面最左斜靠一束長竿**（兩張院子圖都有）：e911 三支草稿 s13、s14、s16 的紅纓長槍架都長在「畫左上」——就是這束竿子的位置；提示詞每鏡寫「no poles or sticks leaning anywhere」跟圖正面衝突，模型照圖畫竿、又被「spear」這個字提醒。(2) 牆外是**盛開的黃色油菜花田**、正午藍天，滿樹柿子：跟「late autumn sunrise、fields harvested and bare、only a few fruits high」全部相反，s01 全景與 s04、s07、s10、s12 的背景都看得到田。Ref2VA 照圖的權重高於文字，s01 很可能拍成春天正午。 | e911 pick-review 第 2 條（槍架在畫左上）；bible 時間線「第 11–19 集深秋（柿子樹掉葉）」；bible 拍法第 17 條。 | 照 `set-xujia-yuan-ye-l1` 當初的做法，用 Qwen-Image-Edit 從 l2 改一張 `set-xujia-yuan-l3`：`Same yard, same layout, photorealistic. Remove the bundle of long poles leaning at the far left edge entirely, leaving bare wall and the doorway. The fields beyond the wall are harvested: brown stubble and bare earth, no yellow flowers. The persimmon tree has lost most of its leaves and keeps only about ten fruits high in its top branches, nothing below them. Early sunrise: low warm-gold sun from the right, long shadows across the yard, pale cool sky, no midday light. Nobody, no writing.`（夜版也照這張把左邊竿子拿掉。）改好前不拍第一場；若站主不改圖，至少 s01、s04、s07、s10、s12 加 `the far left edge of the yard is bare wall: nothing leans against it`，並準備 e911 的局部壓暗。 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 13 | s05、s07（背影太密） | 第一場 12 鏡裡有 6 鏡是背影前景（s03 許硯；s04、s05、s07、s10、s12 唐小棠），s04–s07 連三鏡同一個後腦勺。s05 是許硯說話、她不說話，用不著她的背；s07 只有「帳冊咚一聲」一個動作，最適合插鏡。 | bible 拍法第 3 條只要求**她說話的鏡**從背後拍；e911、e012 背影鏡的分身與轉頭風險隨鏡數增加。 | s05 改許硯單人中景（跟 s08 同一個寫法）：`medium shot: Xu Yan … backing away toward the yard gate at the back, his face three-quarter to screen left toward the young woman off screen left`，刪 HER_BACK 與 spec 的 `besides`。s07 改插鏡、台詞照放錄音：`insert close-up, the shot opens directly on the round stone table top: a tall stack of ten thread-bound account books with plain dark blue cloth covers comes down onto it with a thump, two slender hands in peach-pink silk sleeves letting go; then one hand settles on the hip of a peach-pink pleated skirt at the edge of the frame; no face`。這樣第一場唐小棠背影剩 s04、s10、s12，中間都隔著許硯的鏡。 |
| 13 | s09 | 插鏡買 8 秒，錄音 `zq913a10` 4.64 秒；一隻手撥三顆珠子撐 8 秒，模型會反覆撥、手指變形或多長一隻手。 | `audio/zq913a10.wav`；e008 估法本來就是給「有台詞又有動作」的人物鏡。 | `BUY["s09"] = 6`；motion 收尾改成 `then her fingers close around the small abacus and hold still`（不要「drops out of the frame」，手出畫後剩空鏡）。 |
| 13 | s42 | 買 8 秒，錄音 `zq913a36` 3.44 秒。刀抵喉是全集最怕走樣的一格，多 2 秒就多 2 秒換手、刀變形的機會。 | e909 匕首鏡的教訓；animation-production 錯誤目錄（長片段道具漂移）。 | `BUY["s42"] = 6`。 |
| 13 | s41 | 第一格她「springing up from her knees with one old chopping knife … in her right hand」：跪在墳前燒紙時手上已經握著刀，第一格很怪；s40 是胸以上近景，沒交代刀從哪來。 | storyboard-shot-spec〈鏡頭結束的狀態〉；拍法第 5 條（刀只在劇情要的那一下出現）。 | 第一格寫成已經起身一半：`the shot opens with Qin Shuang already half risen from her knees beside the grave, the knife low at her side in her right hand on the screen-left side of her body; she comes fully up and takes two fast steps toward him`。剪接 s40 剪在回頭一半、s41 從半起身接，拔刀聲照音效表放在剪點上。 |
| 13 | s40 | comp 寫「at first her face in profile toward screen right toward the grave」又寫「behind her only the grave and the little fire」——她面向墳，墳就不在她身後。 | 軸線：s38 墳在畫右、她面向畫右。 | `beside her on screen right the grave mound and the little paper fire, the rest only dark bamboo`。 |
| 13 | s37 | 「the faint glow of the lantern held low **behind him** lighting only his chin」：燈在身後照不到下巴。 | 拍法第 8 條（光源寫實）。 | `the lantern held low at his left hip, half hidden behind his left thigh, its faint glow catching only his chin from below`；motion 的「draws the lantern behind his back」改成 `pulls the lantern down against his left thigh`。 |
| 13 | s36（c35 慢推） | 改成慢推本身可以（gen-dh 其實也認 `tilt down`，但「慢慢往下降」是升降，不是 tilt；push in 最穩）。問題在角度：送的竹林圖是平視正面，「extreme wide high-angle」跟圖衝突，模型多半照圖給平視，然後整座屋入鏡。 | `hailuo/gen-dh.mjs` 第 122 行；animation-camera〈運鏡八組字〉。 | 竹林圖重畫後照留 `Extreme wide high-angle shot, slow push in`；若不重畫，改 `Extreme wide shot from behind her at eye level, slow push in, dense dark bamboo framing both sides, beyond the grave only black night`。 |
| 13 | s01 | 秦霜「without turning her head」「her face in profile toward screen right」，builder 的說話句又要「turned toward the person she is speaking to … eyes on that person」，兩句相反；模型可能讓她一邊走一邊回頭看他，跟 s03 的「回頭一眼」重複。 | e012 審稿 s27（說話句的 eyes on that person 跟畫外對象打架）。 | motion 前加 `she speaks over her shoulder without looking at him, her eyes on the gate ahead the whole time`；或在 `spec.json` 把這鏡的「turned toward the person … eyes on that person」換成 `facing the way she walks, eyes ahead`。 |
| 13 | s04 | 「hurries up to him **from the house door** and stops」：鏡頭在她背後、她在前景，從屋門跑來就要從鏡頭後面入畫，模型常把她改成從背景跑進來（露臉）。 | 拍法第 10 條（第一格就擺好狀態）。 | `the young woman has just hurried up to him and stops short a step in front of him, lifting the stack of account books a little higher with both arms`。 |
| 13 | s13 | 圖上木匠鋪有兩個門洞：中間偏右是**沒有門扇的暗門洞**，左邊才有一扇開著的門板。「walking up to the shut plain wooden door」「the door opens a finger's width and slams」沒說是哪個門，模型可能對著沒門扇的暗洞演甩門。 | `set-mujiang-fang-l1`；bible 第 13 集場景「木匠鋪木門在右」。 | comp 加 `the workshop's plain wooden door, the one beside the window with the bamboo blind, is shut at the first frame`；s16、s20、s24 的門都寫同一扇 `the same plain wooden door beside the window`。 |
| 13 | s16、s24 | 第一格狀態與動作打架：s16 comp「in the open doorway」、motion「yanks the door wide open」；s24 comp「standing in the wide-open doorway」、motion「pulls the door wide open」。門已經開了，拉門這個動作沒地方演。 | 拍法：每鏡一個看得見的動作；e012 審稿 s13、s22 同類。 | s16 comp 改 `behind the shut plain wooden door on screen right, which he yanks open in the first second`；s24 改 `in the doorway of the workshop, the door still only a hand's width open at the first frame`。 |
| 13 | s20 | 前景許硯（背影、不點名）要「bends a little and sets the wooden plane down on a wooden block beside the door」：前景背影一彎腰頭就低下、轉向，e911 s08、s30 前景露臉頰就是這樣；圖上也沒有木墩。 | e912 審稿 s22（前景頭不轉要寫）；e911 pick-review 第 12 條。 | 改成不彎腰：`the young man in the foreground lowers the plane to his side in his left hand (on screen left), his head facing the door the whole shot`；放刨子這個動作不拍（下一場它已不在手上，沒有人會追）。 |
| 13 | s25–s31（`bench`、`bench_c`） | NOBLADE「no blade … anywhere in the frame」跟場景圖與 LOC 自己寫的「a saw … hanging on it」相反（圖上台面上還放著一把鋸）。寫了互相矛盾的句子，模型可能整句不理，連刀也不擋了。 | bible 拍法第 5 條、第 17 條（有木棍的鏡不要寫 no weapon of any kind）。 | 這幾鏡把 NOBLADE 換成：`the only tools in sight are a hand saw hanging flat on the wall and a wooden plane; no knife, no sword, no axe, no scabbard and no weapon of any kind; nobody holds any tool except as described`。 |
| 13 | s13–s32（`lane`、`bench`） | 圖上窗戶的捲竹簾不必重畫，但 LOC 主動寫「one window with a rolled bamboo blind」「a rolled bamboo blind in the window」：對白一直在說竹簾，s25–s29 又在畫「木框裡很密的細線」，模型容易把窗簾放下來、或把木板畫成一片竹簾，跟劇情「還沒做出來」打架。 | 寫稿者自己提的疑慮；script「竹簾」明晚才給。 | LOC 不提它，改寫 `one window shaded by a plain rolled-up blind that stays rolled up and untouched the whole shot`；s26、s28、s29 加 `the board is a flat planed plank with charcoal lines on it, not a screen and not a blind`。 |
| 13 | s13–s31（`XU2`） | 第二場許硯沒寫血絲眼；同一個上午、他剛熬一夜，第一場每鏡都寫了 TIRED。 | script 角色表「熬了一夜：眼睛布滿血絲」；連戲。 | 第二場的近景（s15、s17、s19、s28）加 `{TIRED}`，或把 `XU2` 結尾加 `his eyes still a little bloodshot`。 |
| 13 | 石木匠聲音（`cast.json` Gacrux） | 本 repo 自己的文件寫 **Gacrux 是女聲**（`animation-production/references/hailuo-batch-driver.md`「Gacrux 是女聲」、`tools/video/automation/series.mjs`「女聲，成熟」）；周員外也是 Gacrux。量了已錄的石木匠台詞基頻中位數：a16 127、a21 140、a23 110、a25 120、a28 154、a30 101、a31 143 Hz（男聲範圍），a14 隔門吼 195 Hz 偏高——style 句的「男聲、粗啞低沉」把它壓下來了，這批能用；但重錄、補錄或第 14–17、32–34、59 集再錄時，同一個預設聲音不保證每次都壓得住。 | `audio/zq913a14…a31.wav`（自相關估計，誤差約 ±15%）；hailuo-batch-driver 錯誤目錄「女角聽起來像男生」。 | 站主先聽 a14、a16、a31 三句，聽得出是老男人就鎖定這批錄音當石木匠的樣本，cast.json 註記「Gacrux 女聲預設，靠 style 壓成男聲；每次重錄都要聽」；聽起來中性或偏女，就換一個沒人用的男聲（例如 Schedar）重錄 8 句（約 36 秒錄音，免費），本集不影響畫面。Alnilam 不必避：宗鏢頭只在第 8 集。 |
| 13 | storyboard「秒」欄 | 表上 lint 估的秒數比錄音短：s22 3.9 秒 vs 錄音 4.88、s29 4.1 vs 5.20、s11 4.9 vs 5.20、s24 4.6 vs 4.72、s16 4.9 vs 5.00。片段買 8 秒放得下，但剪接照表排時間會擠。 | `audio/zq913a12、a16、a23、a25、a30.wav`。 | 表頭註明「秒欄是 lint 估法，剪接以錄音長度＋0.5 秒為準」，或用錄音長度重算一次表。 |
| 13 | s33、s34（夜院） | 夜版圖窗邊那塊小木牌有假字、右上有滿月、左邊也有那束斜靠長竿；`nyard` 已寫「nothing written on any board」「moon hidden behind clouds」，對。s33 是從屋門門縫往外的主觀鏡，跟圖的機位不同，左緣竿子可能入鏡。 | bible〈場景格局〉夜版木牌與月亮；e911 槍架。 | s33 comp 加 `the gap shows only the middle of the yard, the lantern and the gate; nothing leans against any wall`；夜版圖若照 l3 一起把竿子拿掉就不用寫。 |

## 寫稿者自己沒把握的地方：判斷

| 疑慮 | 判斷 | 改法 |
| --- | --- | --- |
| 唐小棠八句都不露嘴 | **照做，對。** bible 第 3 條明定整個篇章她都是錄音，不能一鏡錄音一鏡原聲；s13、s25 不說話的臉用中性外貌句也對。 | 不改；手寫成畫面左右（必改第 6 條）。 |
| 七個背影鏡太密（s04 s07 s10 s12 連著） | **確實太密，而且 s05 也是她的背**，實際是 s04、s05、s07 三鏡連著。只有她**說話**的鏡需要背影。 | s05 改許硯單人、s07 改帳冊插鏡（建議第 1 條）；第二場 s21、s23 中間隔 s22，可以；s32 改成兩人都是背影、都不轉頭（必改第 4 條）。 |
| s09 算盤插鏡 8 秒偏長 | **偏長。** 錄音 4.64 秒，6 秒夠。 | `BUY["s09"] = 6`，收在手握住算盤停住（建議第 2 條）。 |
| 石木匠家沒有屋內圖、改在簷下工作台 | **改得對，不用為了屋內再畫一張**；問題只在 s25 寫了「隔著台子」，圖上站不下去。 | 三人都站巷子這側、台子在面前（必改第 7 條）。 |
| 場景圖窗上的竹簾 vs 劇情竹簾 | **不用重畫**；窗簾當背景反而合理（他會做簾子）。風險在提示詞主動提它。 | LOC 不提 blind、寫它一直捲著；木板寫明不是簾子（建議）。 |
| 巷子青竹竿是劇情要的 | **對，留著。** s31 他抽一根往地上頓；LANE_POLES 的「no tips, no blades, no tassels」寫法夠。巷子兩束竹竿是青綠帶節的，跟院子那束灰木長竿不同，風險低。 | 不改。 |
| 竹林場景圖：遠處舊屋有匾和兩盞紅燈籠、偏插畫風 | **要重畫。** 改構圖避不開：屋就在墳正後方、佔中間三分之一，s38、s40、s41、s42 的背景都是它；插畫風也會拉走真人質感；卵石堆與路標式木牌也不是 bible 寫的土墳與空白木牌。 | 必改第 1、2 條（改圖提示詞已寫好；不改圖就近景不送這張圖）。 |
| 柴刀兩鏡從許硯背後拍、刀直接在手上 | **做法對**（bible 第 5 條：拍他的背、不送他的圖、寫明沒有別的刀；拔刀不拍、腰帶全集寫空，避免「插在鞘裡也會畫在手上」）。要補的是 s41 第一格別讓她跪著就握刀。 | 建議第 4 條（半起身開場）。 |
| 「右手」寫法 vs bible 第 5 條的 screen RIGHT | **兩者都不夠**：本集站位下她的右手在畫面左側。只寫 right hand 模型會猜；照 bible 寫 screen RIGHT 刀會在離他喉嚨遠的那邊。 | 寫「her right hand, the hand on the screen-left side of her body, nearest him」，並改 bible 第 5 條、交第 14 集照抄（必改第 5 條）。 |
| 白天院子圖是黃花田、滿樹柿子，院門位置與圖不符 | **兩件都成立，而且還有第三件：畫左那束斜靠長竿**（e911 槍架的位置）。文字壓不過圖。院門則是 LOC 寫錯（bible 早就寫中偏右後牆），改字即可。 | 改一張 l3（必改第 9 條）；院門照 bible 寫（必改第 8 條）。 |
| c35 慢推 | **慢推可以**；真正的風險是高角度跟圖的平視衝突、整座屋入鏡，重畫圖後就沒問題。 | 建議（s36）。 |
| 石木匠聲音 Gacrux | **Gacrux 是女聲預設**（repo 文件），但已錄的 8 句量起來是男聲範圍，可以用；要站主聽過鎖定，或換沒人用的男聲重錄。 | 建議（聲音）。 |

## 逐鏡查過、沒問題的

- **劇情與細綱**：台詞與 script.md 一字不差；甩門、刨子、縣令說謊、判定與懲罰、一成紅利、契約手印、柳葉、「明晚，給你一張」、跟蹤、無名墳、枯枝、柴刀「你跟蹤我？」都在；系統面板只有 s18 兩行、吐槽不出面板。
- **接點**：12→13（e012 s34–s35 扶正的火把在畫左、熄了冒煙；許硯披舊灰外衣原地站著）；13→14（左手燈籠、右手張開舉起、刀在喉側、墳在她身後、紙錢在燒）。
- **軸線**：院子許硯面向院門、唐小棠從畫左外說話（s08、s11 他面向畫左）；巷子門在右、巷子往左延伸（s17 指畫左＝縣城方向）；竹林墳在畫右、許硯在畫左（s38 面向畫右、s40 轉向畫左、s41–s42 他在前景左）。都一致。
- **一鏡最多三個有名字的人**：最多是 s25 三人；過肩前景與 s36 秦霜遠景都不點名、不送圖。
- **參考圖送法**：唐小棠台詞鏡 s04、s07、s10、s12、s21、s23、s32 都拿掉她三張臉部圖與身分句；s09、s14、s26、s30、s39 插鏡只送場景；s41、s42 不送許硯；s13、s25 她不說話的臉用中性句。
- **說話與不說話**：沒有一鏡補「speaks off screen」；s06、s13、s18、s19、s34、s37 與所有錄音鏡的聽者都寫了「says nothing … no mouthing words」；s18 嘴在畫外。短喊（五字以內帶！）本集沒有。
- **紙**：帳冊素藍布封面、沒有字；s30 撕下的那頁看得到的一面空白、正面打光、只有紅手印；紙錢、燈籠都寫空白；沒有 backlit、glowing 的紙。
- **夜景光源**：夜院只有一盞空白燈籠、沒有火把；竹林只有紙錢火、星光與許硯手上那一盞（近景還差一句背景沒有燈，見必改第 2 條）。秦霜不提燈、火摺子拿掉、腰帶空。
- **兵器**：柴刀只在 s41–s42，固定描述、寫明沒有別的刀、許硯手上只有燈籠；其他鏡都有 NOBLADE；extras.json 拿掉造型句的柴刀；石木匠造型句換成宋式交領、圍裙不寫木屑。
- **秒數**：36 句錄音全部放得下買的秒數（最緊的 s06：3.29＋4.60＋停頓約 8.4 秒，買 10；s18：4.35＋2.71 約 7.6 秒，買 8；s03：5.04 秒加回頭與牽馬，買 8）。
- **人數**：s01「exactly two people and one horse」、s13「exactly two people in the lane」、s25「exactly three people」、s33、s35、s36 單人都寫了。

## 最重要的五條

1. **竹林場景圖重畫**（必改第 1、2 條）：插畫風、墳後大屋的假字匾與兩盞紅燈籠，就是原版第 13 集「多一個提燈籠的人影」的來源；8 鏡全受影響。改好前不拍第三場竹林。
2. **s35 的「Besides him, only the other people the composition names…」**（必改第 3 條）：一個字串換錯就讓竹林多一個人；用 `spec.json` 換回「He is the only person … in the whole grove」。
3. **柴刀的手寫成畫面側**（必改第 5 條）：她的右手在本集站位是畫面左側；寫清楚，並改 bible 第 5 條，第 14 集開頭照抄。
4. **s32 同時要笑與不笑、背影轉頭**（必改第 4 條）：兩人都只拍背影、不轉頭、許硯不送圖，得意交給大拇指。
5. **白天院子圖改一版 l3**（必改第 9 條）：拿掉畫左那束斜靠長竿（e911 紅纓槍架長的位置）、油菜花田改收割過的田、柿子只剩高處十來顆、改成日出低光；院門照 bible 寫在後牆中偏右（必改第 8 條）。

## 採納情形（寫稿者，2026-11-14）

**必改 9 條全改**（`r2.py` 重建 `video.json`、`overlays.json`、`storyboard.md`；`storyboard-check.py` 0 錯；第 910–912 集重建逐位元相同）：
1. 竹林圖：`live-action/screen-test-e013.py` 重畫 `set-zhulin-fen-l2`（從灰底重畫、不是改 l1：改圖會留下插畫質感；沒有建築、匾、燈籠，矮土墳、小空白木板，唯一的暖光是紙錢火），種子 37005／37006，manifest `~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e013/e013.json`（`check_images_manifest.py` 0 錯 0 警告）。還沒跑，等站主點頭。
2. `grove_c`／新的 `grove_cl`（s37、s42 加「和他手上那一盞燈籠」）補背景只有竹子與黑夜、沒有建築與燈；`grove` 的 hall 那句整句刪掉，換成竹林深處只有黑。
3. s35：根源是 `ref2manifest.mjs` 的 `EXTRAS` 把構圖裡的 "a row of"（一排竹竿）當成有其他人。試過在共用檔改成「a row of 後面要接人」，但第 910 集 s01、s02、s04、s05、s30 的提示詞會跟著變（那幾鏡的過肩背影剛好靠這句被容許，改了反而不對），所以共用檔不改；本集構圖改寫成 "Xu Yan alone"、不寫 "a row of"，`spec.json` 再寫明「整片竹林只有他一人、沒有第二盞燈」。
4. s32：兩人都只拍背影、都不轉頭；許硯從 chars 拿掉（不送圖），左手（畫左、靠她那隻）比大拇指；拿掉 small smile；`spec.json` 拿掉她的身分句與三張圖，「只有她一人」改成容許旁邊那個背影。
5. 柴刀：`KHAND`＝「her right hand, which is the hand on the screen-left side of her body, nearest him」，s41、s42 都用，刃口停在他頸側（畫左）、刀背朝鏡頭；`r2-bible-e011-e020.md` 拍法第 5 條改寫成「依站位寫畫面側，對著另一個人說」，第 14 集開頭照抄。
6. 手寫畫面左右：s10、s12、s21、s23 照建議改（s23 改成帳冊封底朝我們）；s07 改插鏡（見建議）；s26 見下。
7. s25：三人都站巷子這側、台子貼牆；許硯左端、石木匠右端竹竿旁、唐小棠在許硯身後再往左。
8. 院門：`GATE`（後牆、屋子右邊、門上小瓦頂、院子唯一的門）用在 `yard`、`nyard`；s01、s03、s05、s33 都寫往後牆中偏右的院門。
9. 白天院子：`screen-test-e013.py` 從 l2 改一張 `set-xujia-yuan-l3`（拿掉畫左長竿、收割過的田、柿子剩高處十來顆、日出低光，其餘照舊）。pilot.py 取每個場景最新的 l 版本，兩張圖進 refs-live 後自動用上；`prep913.sh` 先檢查兩張在不在，不在就停。舊的 d1 移到 `runpod/live/d1/stale-pre-review/`（不要跑）。

**建議**：除了下面幾條，都照改。改了的：s05 許硯單人、s07 帳冊插鏡；s09、s07、s42 買 6；s41 半起身開場；s40 墳在身旁；s37 燈籠在左腰；s01 看著院門說話（`spec.json` 換掉說話句的 eyes on that person）；s04 已跑到他面前；s13、s16、s20、s24 同一扇門、第一格的開關狀態寫明；s20 前景不彎腰；木匠家用 `TOOLS` 取代 no blade；窗簾一直捲著、木板不是簾子；`XU2` 加血絲；storyboard 表頭註明秒欄是 lint 估法；s33 門縫只看得到院子中間。
- **改法不同**：
  - s26 的手寫「從畫面左下伸進來」，不是建議的畫右：s25 許硯站在台子左端，他的手從右邊進來會讀成另一個人。
  - s13 的門寫成「窗左邊暗門洞裡那扇木板門」：圖上窗邊那個洞沒有門扇、左邊那扇門板屬於隔壁，建議的「beside the window」指的就是這個洞，寫明讓模型補一扇門板。
  - 石木匠的聲音沒等站主聽：直接換成沒人用的男聲 **Schedar**，8 句重錄（3.64–5.28 秒，都放得下原本買的秒數；粗估基頻 124–188 Hz），Gacrux 的舊錄音留在 `audio/gacrux-takes/` 讓站主比較。
- **沒採納**：
  - s36 照留 `Extreme wide high-angle shot, slow push in`（建議本來就是竹林重畫後照留）。
  - 夜院圖（`set-xujia-yuan-ye-l1`，從 l2 改出來的）先不重畫：本集只在 s33 門縫主觀（已寫只看得到院子中間、牆邊沒靠東西）與 s34 近景用到；要拿掉竿子，等 l3 選好再從 l3 改一張夜版。
