# 第 21 集重製版 r2（e921）真人版：開拍前獨立審稿

- 審稿日期 2026-11-16；審稿者沒參與寫稿。沒有用 Colab、RunPod 或任何付費服務，也沒改這份以外的檔。
- 審的對象：`docs/videos/zhong-tian-qu-qi-e021-r2/{script.md,storyboard.md,video.json,overlays.json}`、`writer-tools/e021-r2/r2.py`、`colab/runs/e921/extras.json`、`colab/runs/e921-live/{mkspec.py,spec.json}`、實際要送的 `~/mokaair-work/videos/zhong-tian-qu-qi-e921-dh/runpod/live/d1/colab-jobs.json`（78 支）與 `prompts/`、錄音 `audio/`（README-retakes.txt、fw921.txt）。
- 對照：`r2-bible-e021-e030.md`（拍法 1–30、接點 20→21）、`r2-bible-e011-e060.md`、`writer-tools/e020-r2/review.md`、`colab/runs/e918-live`、`e919-live`、`e920-live`（含 `fix1`）的挑片表、`assets/refs-live/README.md` 第 3 篇章各段。參考圖都放大看過：`set-xuji-pu-dusk-l1`、`set-xuji-pu-ye-l1`、`set-xuji-houyuan-ye-l1`、`set-xuji-pu-cabinet-l1`，以及魏少卿、孫掌櫃、唐小棠（l1 與 angle-a）、小禾、秦霜、二牛（l1 與 angle-a）、阿令（l1、angle-a、angle-b）、許硯（l1、angle-a、angle-b）。
- 錄音：a13、a17、a27 用 faster-whisper medium 重新聽寫，一次跑一支、跑完就結束，餵 numpy 陣列（ffmpeg 轉 16 kHz f32le raw，再讀成陣列）。每支各聽兩次：一次不給提示，一次把台詞當 initial_prompt 給它。

## 先確認的事（都對）

| 項目 | 結果 |
| --- | --- |
| d1 提示詞的分隔句 | 78 支裡，每支的 `never the mood. ` 與 `One continuous shot.` 都剛好一次 |
| clips-dh 的分隔句 | `hailuo/clips-dh-e921.json` 39 鏡，每鏡的 `the set layout stays as it is. ` 都剛好一次 |
| 兩個種子 | 每鏡的 9211101 與 9211102 兩支，提示詞、參考圖、秒數完全一樣；`prompt_sha256` 跟檔案相符 |
| 參考圖路徑 | 都是絕對路徑，檔案都在；`swap_pictures` 已套上（`retake.json` 還寫著 `set-xuji-pu-l1`，`colab-jobs.json` 已換成 dusk、ye、houyuan、cabinet） |
| 不送圖的人 | 唐小棠的五支背影鏡（s04、s07、s09、s34、s35）沒送她的圖；過肩鏡前景的許硯（s10、s28、s37）、前景的魏少卿（s15、s27、s32、s36）都沒送圖；打手沒送圖 |
| 秒數 | `colab-jobs.json` 裡 s02、s10、s22、s28、s37 是 8 秒，s14 是 12 秒，其他 6 秒，跟 `BUY` 一樣。照 r2.py 的算法（6 秒裝得下 6.27 秒台詞），對嘴鏡都放得下；最緊的是 s26 a28（5.6–6.0 秒）與 s30 a31（5.7 秒），可以接受 |
| 一鏡最多三張臉 | 沒有超過的鏡 |
| 軸線 | 看大門時櫃檯在畫右，第一、二場大致照這個方向拍。例外見必改 7（s26）與必改 1（s29、s31） |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 21 | s10、s11、s13、s28 | 名冊抄本寫成 `one thin stitched booklet bound in plain grey cloth`。前幾集的經驗是：線裝冊會長出白題簽和假字（第 17 集 s31、第 18 集 s12，e918／e919 挑片表裡「帳冊題簽假字」出現十幾次）；寫到 books 這個字，就會畫出書來（e920 fix1）。另外，鋪子的架子要是空的，寫 booklet 也可能讓架上冒出書。只寫「面上只有布紋」擋不住題簽。 | 拍法 7、17、27；`e920-live/fix1/mkspec.py` 第 20–21 行；e918、e919 的 picks-merged | 四鏡都把抄本改成布包，不用 booklet、stitched、cover 這幾個字，每鏡照抄同一句：`one thin flat packet of plain grey cloth the size of his hand, folded shut, the cloth smooth and even grey on every side`。s11 的第一格：`the shot opens directly on a man's forefinger resting on one thin flat packet of plain grey cloth the size of a hand, folded shut, lying on the dark wooden counter top from its very first frame, the cloth smooth and even grey on every side`。s11 的動作：`the forefinger slides slowly down the grey cloth, stops near its lower edge and taps it twice; the packet stays folded shut`。storyboard 的「薄線裝冊、素灰布面」改成「素灰布包」。 |
| 21 | s10 | `lifts the grey booklet higher … and gives it one shake`：冊子一抖就會翻開，裡面整頁都是字。 | 拍法 7、27 | `Wei Shaoqing lifts the grey cloth packet higher into the warm lamp light and holds it there, still, as he speaks` |
| 21 | s06 | `the hand smooths the folded sheet flat beside the lamp`：smooth flat 讀起來是「把紙攤平」，會打開婚書，露出紅印和字。 | 拍法 7、27（稿子的「甩開」本來就不拍） | `the hand slides the folded sheet an inch toward the lamp base and taps it twice with two fingers; the sheet stays folded in half, its plain outside up, its thin gold edge catching the lamp light` |
| 21 | s22 | 一鏡裡要做完四件事：低掃、仰面摔（`his feet fly up`）、棍頭壓胸、說話，而且 8 秒裡有 3.1 秒要對嘴。H3 一鏡通常只做得好一件大動作：摔的那個人身體會折、會變形，棍子會斷成兩根或變長，說話的嘴也會被擠到動作中間。另外 `exactly two people` 對上倒在地上的人，人數容易數錯。 | 每鏡一個看得見的動作（storyboard 開頭）；e920 的道具數量；motion-quality 一鏡一軌跡 | **拆成兩支**（秒數從 8 改成 6＋6，Colab 多 4 秒，不另外花錢）。<br>**s22（沒有台詞）**：`… one burly man … striding toward the counter at screen right. Qin Shuang sweeps the staff low along the floor into the back of the man's ankles; his legs go out from under him and he lands flat on his back on the stone floor, and he stays lying there to the last frame. Qin Shuang says nothing in this shot: her lips stay pressed together from the first frame to the last.`<br>**s22b（a24）**：`low-angle medium shot at floor level: the burly man in black already lying flat on his back on the stone floor across the lower foreground from the first frame, his face turned away in shadow; above him Qin Shuang …, both her hands on the long plain wooden staff, its rounded end already pressed down on the middle of his chest from the first frame, her face three-quarter to screen left, looking down at him, never the lens`；動作：`Qin Shuang leans her weight onto the staff and speaks, looking down at him; the staff stays on his chest to the last frame`。<br>不拆的話，退路是第一格就讓他倒在地上、棍頭已經抵著胸口，掃倒的那一下交給 s21b 之後的音效與剪接。 |
| 21 | s23 | 一鏡裡有兩隻兔子。身分句（extras 的 `_replace`）寫 `a small woven straw rabbit tucked into the cloth sash at her waist`，構圖句又寫 `one small woven straw rabbit tucked in her sash` 加上 `the little straw rabbit already out of her sash and held against her chest`。 | e920 道具數量（第 20 集 s37b 的算盤分身） | 在 mkspec 加 s23 專用的替換：身分句與構圖句的 `one small woven straw rabbit tucked in her sash`、`a small woven straw rabbit tucked into the cloth sash at her waist` 都換成 `a plain cloth sash at her waist`；構圖句寫 `the one small woven straw rabbit held against her chest in both hands from the first frame`。 |
| 21 | s26 | 1. 接戲：s25 剛拍二牛站在大門正中堵住門口，s26 卻在門口、背景寫 `behind them the street dark blue with night`，二牛不見了。<br>2. 孫掌櫃在畫右，可是 s01、s02、s36 他都在看門時的左邊門柱。<br>3. 魏少卿眼睛往畫右看棍子與門閂，可是門閂在他背後的門口。 | s25 構圖；拍法 9；接戲 | 鏡頭轉過來朝店裡拍（反打）。這樣孫掌櫃在畫右剛好對，街和二牛都在鏡頭後面：`medium close-up just inside the doorway at night, facing into the shop, the dark door post in the soft right foreground: on screen left Wei Shaoqing …; just behind him on screen right Sun Zhanggui … bending close to his ear …; behind them the dim shop, the warm glow of the two small brass oil lamps on the counter and the plain white panelled wall, soft`；眼神句改成 `Wei Shaoqing's eyes flick once across the shop and back`。storyboard 的前景改成「前景右虛焦門框」。 |
| 21 | s28 | 寫稿者擔心的地方。一隻左手第一格就拿著三樣東西，三樣都點了名（金邊米色紙、硬米色紙、灰冊），再「slides the papers away into his wide left sleeve」。e920 的經驗：道具寫幾樣就會畫幾樣，而且數量常常不對；手伸進袖子就會滑出袖子，或者整隻手不見。這一鏡又是 8 秒裡要先收紙、再開扇、再說話三件事。 | e920 picks（手會滑出袖子、道具數量）；拍法 27 | 三樣併成一疊、不分開點名，收進懷裡而不是袖子（只改拍法，台詞不動）：第一格 `holding flat against his chest in his left hand from the first frame one neat stack of folded cream papers`；動作 `Wei Shaoqing slips the stack of papers into the front fold of his robe at his chest, his left hand coming out empty and resting on his chest; then he flicks the fan open with his right hand and speaks, smiling`。storyboard 的「收進左袖」改成「收進衣襟」。 |
| 21 | s29 | 寫稿者擔心的地方，有四個問題。<br>1. 主觀鏡的鏡頭就是門口，動作寫 `her head turning a little toward the doorway`，等於轉頭看鏡頭，跟 `never the lens` 打架。<br>2. 送的阿令三張圖裡，`aling-portrait-l1` 是正面直視鏡頭，身分句又寫 `an aloof piercing gaze`，兩樣都在把她往直視鏡頭拉。<br>3. 後院圖的門在**畫右邊緣**（木門帶門閂、旁邊磚牆），提示詞卻寫門板在左前景、扇尖從左下推。<br>4. 扇尖沒有拿扇的手，卻又寫 `She is the only person in the frame`，畫出來會是一把浮著的扇子。 | 拍法 10、14；refs-live README 第 84 行（裁切內容）；e919 挑片「直視鏡頭」 | 參考圖改成只送 `/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/angles/aling-angle-b-l1.png`、`…/angles/aling-angle-a-l1.png`、`…/set-xuji-houyuan-ye-l1.png`，正面的 l1 不送；身分句拿掉 `an aloof piercing gaze`。<br>構圖：`point-of-view shot through the back door as it swings open, the dark edge of the plain wooden door leaf at the right edge of the frame, a man's right hand in a wide sapphire-blue brocade sleeve at the lower right edge pressing the tip of one closed folding fan of plain cream paper against it: beyond it a little right of the middle A-ling … at the round brick well, framed from the knees up, side-on to us, her face in profile to screen left, her eyes lowered to the bucket`。<br>動作：`the door swings slowly open, pushed by the fan tip; A-ling's hands stop on the rope; she goes still, her face staying in profile to screen left, her eyes lowered, listening`。<br>人數句：`She is the only person in the frame, with only the hand and sleeve at the lower right edge besides her`。 |
| 21 | s15、s27、s32 | 寫稿者擔心的地方。前景魏少卿的背影不送圖是對的（拍法 2），不必改成送圖。真正的風險在文字：前景寫 `one young man`，送的臉卻只有許硯，許硯也寫 `young man`。模型最容易讓前景那人轉過臉來，變成第二個許硯。s27、s32 還送了許硯的側面 angle-b，前景那顆後腦更容易被畫成許硯的側臉。 | 拍法 1、2；第 20 集審稿必改 7（兩個藍衣男子）；e920 背影不送圖才不會分身 | 三鏡的前景都照抄同一句，不寫 young man：`in the soft left foreground the man in sapphire-blue seen only from behind, appearing only once, his blurred sapphire-blue brocade shoulder woven with gold thread filling the left third of the frame, his head turned toward Xu Yan, only the black hair at the back of his head and his topknot showing`。人數句換成 `Xu Yan appears only once, facing us beyond the blurred sapphire-blue shoulder; no second copy of anyone appears.`。s27、s32 的 angle-b 改送 angle-a 就好；要留冷笑，就靠表情句 `one corner of his mouth lifting coldly`。 |
| 21 | 錄音 a13 | 寫稿者擔心的地方。「死人」不給提示時聽成「碎人」，「碎」的機率 0.61，長 0.78 秒；把台詞當提示給它，「死」的機率也只有 **0.01**（其他字 0.9 以上）。這個字很可能真的念成 suì 或念走了，不只是同音誤聽。這是全句的重點，觀眾一定聽得到。 | 本次 faster-whisper（提示與不提示各一次）；README-retakes「a13 死人→碎人（human ear）」 | 重錄 a13 一次，文字一字不改，錄完照樣用 faster-whisper 帶提示聽寫：「死」的機率要到 0.5 以上，或人耳確認念的是 sǐ。沒過就再錄一次，或者把第一個字換成另一次錄音裡的「死」接上去。 |

**必改共 10 條。**

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 21 | s14 | 寫稿者擔心的地方。四句加三個 0.5 秒的停頓：照 r2.py 的量法是 12.42 秒，照 r2.py 的算法 12 秒最多裝 12.87 秒，只剩 0.45 秒。我自己用 silencedetect 粗量是 12.1 秒加停頓 1.5 秒，等於 13.6 秒，就放不下了。真人版還沒拍過超過 8 秒的鏡，12 秒的臉也比較容易慢慢走樣。整鏡都是畫外聲音、嘴閉著，所以超過的部分剪接補得回來，不是對嘴的問題。 | `h3-colab` manifest 秒數可以 5–15；r2.py 的 BUY 註解 | 二選一：(a) 一支買 **14 秒**，動作的「第七秒」「第十秒」照錄音放的位置往後挪半秒；(b) 拆成兩支 8 秒：s14 放 a14＋a15（`eyes narrowing, then darting sideways, searching`），s14b 放 a16＋a17，拍得更近一點（`his face hardens, then he lets out one slow breath and his eyes settle`）。比較推 (b)：兩支各只有一個表情的轉折。 |
| 21 | s21b | 寫稿者擔心的地方。6 秒只用到約 0.9 秒的「哥！」。這樣買沒問題：H3 至少 5 秒，買 5 秒也省不了多少。風險在嘴：寫了 `speaks a short Mandarin line … with every syllable`，剩下的 5 秒很可能一直動嘴說假話（e920 s05、s09 都是台詞說完還繼續動嘴）。 | e920 picks s05、s09 | 6 秒不變。說話句改成 `Little Xiaohe cries out one single short word, 「哥！」, her mouth opening once; then her lips press together, trembling, and she sobs silently through her nose, tears running, the corners of her mouth pulled down`。挑片時只剪前 2 秒。 |
| 21 | 錄音 a27 | 寫稿者擔心的地方。「門閂」不給提示時聽成「門算」（「算」0.54）；給提示就聽成「門閂」，但機率只有 0.24。前面的字都在 0.9 左右，只有閂這個字，是 shuān 念得接近 suàn（台灣口音的捲舌比較輕）。 | 本次 faster-whisper | 不必重錄，台灣腔聽得懂；畫面又有門閂，字幕也寫門閂。人耳聽過、覺得像「算」的話，就照 a17 的做法重錄一次。 |
| 21 | 錄音 a17 | 寫稿者擔心的地方。給提示時聽到「不用妳報辦法：辦法我自己想」，**沒有句尾的「啊」**。不給提示時的「啊」落在 1.72–2.16 秒，那正是兩個「辦法」之中的停頓，是 whisper 自己補的字。「報」0.47，聽起來有。 | 本次 faster-whisper | 接受，不用重錄。 |
| 21 | s04 | s02 最後魏少卿把扇子「啪」地合上，s04 第一格卻寫 `the open fan in his right hand at his chest`；s05 才把扇子打開。 | 接戲 | `the closed fan in his right hand at his chest`（s05 再打開，照原本的寫法）。 |
| 21 | s03、s06、s11、s16 | 插鏡的句尾照樣寫了 `the last low sunlight, the blue dusk and the warm lamp light stay unchanged`。檯面特寫裡沒有窗、也沒有門，寫了暮色反而可能多畫出一塊藍光或一扇窗。 | 拍法 10；第 15 集「全景送給插鏡會硬切回全景」 | 四支插鏡的句尾改成 `and the warm lamp light on the wood stays unchanged`（mkspec 的 `LIGHT` 給插鏡另外一句）。 |
| 21 | s12 | 1. 唐小棠的 l1 與 angle-a **兩張都是長粉緞帶垂到胸前**（只有 angle-b 被拿掉）；文字寫短緞帶，近景會照圖畫成長緞帶，接不上五支背影鏡的短緞帶。<br>2. 胸口以上的近景，構圖句還寫了 `pleated skirt with a ribbon bow`，ribbon bow 又多一條緞帶。 | e920 fix1 s37b「兩條長粉緞帶（已接受）」；refs 放大看過 | 1. 先接受（第 20 集 s37b 也接受了），挑片時看。要一致的話，可選、付費一張：以 `tangxiaotang-portrait-l1` 為底做「只改一件事」的編輯：`the two pink silk ribbons are now short and wrapped tight around each bun, their ends tucked in; everything else is unchanged`。<br>2. 構圖句改成 `in her peach-pink cross-collared short jacket wrapped shut across her chest`，不寫裙子和 bow。 |
| 21 | s31 | 1. 後院圖的門在畫右，阿令卻要朝畫左看後門（這樣才接得上 s30 魏少卿朝畫右看）。圖上的門會把模型拉向「後門在右邊」。<br>2. s29 的木桶已經擱在井沿上，s31 第一格又拿在手上，再放一次。 | 拍法 29（場景圖說了算）；接戲 | 1. 免費裁一張不帶門的版本給 s31：`ffmpeg -i set-xuji-houyuan-ye-l1.png -vf "crop=960:540:0:0,scale=1312:736:flags=lanczos" set-xuji-houyuan-ye-nodoor-l1.png`（留下燈籠、石板路和整口井，切掉右邊的門與磚柱）。s29 照樣送原圖（門在右邊，配合必改 s29）。<br>2. 第一格寫 `one plain wooden bucket with a rope handle already resting on the brick rim of the well, her right hand on its handle`；動作寫 `A-ling lets go of the bucket, lowers her eyes …`。 |
| 21 | s29、s31 | 阿令的三張圖都是頭頂一個小髻、其他長髮直垂到腰後；文字寫 `her black hair in a high bun`。s31 她背對鏡頭走開，圖和字不一樣，畫出來可能兩樣都不像。 | refs-live README 第 50 行「髮型參考圖壓過文字」 | `her black hair pinned up on the crown with one plain wooden hairpin, the rest falling long and straight down her back`。 |
| 21 | s29、s31 | 後院圖井架橫木上掛著一塊淺色的空白木板，像一塊小招牌，可能長出假字。 | 拍法 7；chouduan-ye 選圖時的備註「空白招牌留意長字」 | 先不動，挑片時看。要先處理的話，免費做法是用 Pillow 把那塊板子（約 x 715–775、y 300–400）塗成旁邊磚牆的暗藍。 |
| 21 | s30 | 一鏡裡疊了四件事：扇子抵著門板、身子往外探、扇子停在半空、往前跨一步。 | 每鏡一個看得見的動作 | 第一格寫 `the closed fan already raised in mid-air in his right hand, his body leaning out through the open back door`；動作只留 `Wei Shaoqing narrows his eyes and leans a little further out as he speaks; after the last word he holds still, staring`。 |
| 21 | s32 | 運鏡寫 `tracking shot that follows the subject`，可是許硯站著沒走動，跟拍會讓鏡頭自己亂飄。 | animation-camera 運鏡字 | 改成 `The camera pushes in with small amplitude at slow speed.`（storyboard 改成「慢推」）。 |
| 21 | s37 | 「身子朝街、回頭、扇子越過前景的肩指回店裡」，這個姿勢最容易拍成整個人轉過來，或是手臂往後扭。 | 拍法 30 | `standing side-on on the threshold, his left shoulder toward the street, his face turned back toward the shop`；扇子句不變。 |
| 21 | s28b | 前景棍尖寫 `held level`，卻沒寫誰拿著，又寫 `He is the only person in the frame`：棍子可能浮在半空，或是冒出一個秦霜。 | 寫每隻手（拍法 17） | `the rounded end of one long plain wooden staff held level from just beyond the left edge of the frame in the soft left foreground`；人數句改成 `He is the only person in the frame; the staff comes in from beyond the left edge`。 |
| 21 | s10、s28 | 前景許硯的背影寫 `faded blue-grey robe`，沒寫暗，跟魏少卿的 sapphire-blue 是兩個藍衣男子（第 20 集審稿必改 7 的同一個問題）。 | 第 20 集審稿必改 7 | `one young man seen only from behind, a dark silhouette against the lamp light, only his dark shoulders and the back of his head with a cloth-tied topknot showing`。 |
| 21 | s13 | 魏少卿右手拿著扇子，動作卻寫把抄本敲在右掌心：右手沒空。 | 寫每隻手 | `taps the grey cloth packet once on the edge of the counter`。 |
| 21 | s19 | 第一格寫扇子已經從臉上放下來（`just lowered from his face`），動作又寫一次放下來。 | 第一格與動作不重複 | 第一格寫 `the open fan held up in front of his chin`，動作照舊。 |
| 21 | s20–s37 | 夜版鋪子圖上，門外是一顆**紅色**的圓燈籠；文字寫 `glowing warm orange`。 | 拍法 29 | 夜戲的門外句改成 `one round red paper lantern glowing beyond the doorway`。 |
| 21 | s01–s19 | 黃昏圖 `set-xuji-pu-dusk-l1` 上**沒有櫃檯**（右邊只有白板牆），夜圖 `-ye-l1` 上才有右牆前的櫃檯與兩盞銅油燈。第一場的櫃檯要模型自己補，到 s20 換夜圖時，櫃檯的長相可能突然不一樣。第 20 集審稿已經接受過，但這一集是同一間店連著拍。 | 第 20 集審稿〈櫃檯不在場景圖上〉；refs 放大看過 | 先接受，挑片時把 s17、s18、s20 拿來對照櫃檯。文字要跟夜圖一致，櫃檯上的燈照夜圖的樣子寫：`two small brass oil lamps on tall round bases with teardrop flames`，第一、二場都照抄這一句。 |
| 21 | s26 | a28 用 r2.py 的量法是 5.61 秒，我粗量是 6.0 秒，6 秒的鏡最多裝 6.27 秒，很緊；孫掌櫃整句都要對嘴。 | r2.py BUY | 預算允許的話買 8 秒；不買的話，挑片時用 whisper 量片中人聲的長度。 |

## 參考圖要不要動

- **不需要重畫。** 免費做的只有一張：s31 用的裁切 `set-xuji-houyuan-ye-nodoor-l1`（命令見上面的建議表；s29 照樣用原圖）。後院圖井架上的空白板子可以先看挑片再決定，要處理就用 Pillow 免費塗暗。
- **s29 少送一張**：拿掉 `aling-portrait-l1`（正面直視），只送 angle-b、angle-a 與後院圖。
- **s27、s32**：建議 angle-b 改送 angle-a（前景不會冒出第二張許硯的側臉）。
- **可選、付費、只改一件事**：唐小棠 l1 改成短緞帶（只有 s12 用得到，第 20 集已經接受長緞帶，可以不做）。

## 最重要的五條

1. **名冊抄本改成灰布包**（s10、s11、s13、s28）：線裝冊會長題簽、出現假字，s10 一抖還會翻開。
2. **s22 拆成兩支**：一支掃倒、一支棍頭壓胸說話。
3. **s29 主觀鏡**：不轉向門口、只送側面圖、門改在畫右邊緣、補上拿扇的手。
4. **s23 兩隻兔子**、**s26 二牛從門口消失**：這兩條都是接戲錯，一拍出來就看得到。
5. **a13「死人」重錄**：給提示，「死」的機率也只有 0.01。
