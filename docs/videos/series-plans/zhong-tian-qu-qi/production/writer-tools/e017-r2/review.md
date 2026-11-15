# 第 17 集重製版（e017-r2，內部編號 917，真人版）分鏡與提示詞：開拍前獨立審稿

- 審稿：沒參與寫稿的獨立審稿代理，2026-11-15。只讀，只寫本檔；沒用 Colab、RunPod 或任何付費服務，沒有 git commit。
- 審的版本：`docs/videos/zhong-tian-qu-qi-e017-r2/{script.md, storyboard.md, video.json, overlays.json}`、`writer-tools/e017-r2/r2.py`、
  `colab/runs/e917/extras.json`、`colab/runs/e917-live/{mkspec.py, spec.json}`，以及代用圖試跑的
  `…/scratchpad/e917/w/zhong-tian-qu-qi-e917-dh/runpod/live/d1/colab-jobs.json`（80 支，s01–s40 × 9171101／9171102，兩個種子的提示詞逐位元相同，40 鏡逐鏡讀完、送圖清單逐鏡核過）。
  場景試鏡 `live-action/screen-test-e017.py` 與 `~/mokaair-work/…/live-screen-test-e017/prompts/` 六個檔（**注意：`out/progress-1.json` 已在寫，試鏡正在跑**）。
- `preflight-prompts.py` 重跑：0 error、8 warn（s07、s24、s25 的 carrying pole，s21 的 paper）。否定名詞：40 支只剩允許的
  「no second copy」「no talking / no mouthing words」「nothing tucked in it」「no subtitles…」，沒有新的被否定名詞。台詞 40 句對過 script.md，一字不差。
- 錄音：`audio/zq917a01–a40.wav` 用 wave 讀長度、silencedetect 看停頓、faster-whisper（scratchpad 的 fwenv）重聽 a07、a20–a22、a24、a26、a27，自相關估基頻。
  BUY 都放得下（最緊 s20 a18 5.56 秒／6 秒、s34 a32 5.44 秒；s25 a23 7.08 秒／8 秒；s28 a26 的「一、二、起」三段在 0–3.4 秒，整句 6.43 秒／8 秒；s39 9.57 秒／10 秒）。
- 放大看過：`set-dukou-l2`、`set-xujia-yuan-l3`、`set-gongpeng-l3`、`set-gongpeng-ye-l2`（三張新圖的底圖），阿令、許硯、二牛、石木匠、韓伯、小禾、秦霜的 l1 與角度圖。
- 對照：`r2-bible-e011-e020.md` 拍法 1–18（尤其 5、8、15–18）、`r2-bible-e011-e060.md`、`season-01.md` 第 17 集、`e016-r2/review.md`、
  `colab/runs/e91{3,4,5}-live/picks-merged.tsv`、`hailuo/edit-dh-e914-live.json` 的 `_note`、第 16 集 r2 s39–s42、`animation-preproduction/references/shot-risk.md`。

## 總評

做到的：唐小棠四句都背拍、spec 拿掉她的圖與身分句；秦霜 s04 背拍；兩人接觸（s04、s13）寫成第一格狀態；插鏡 s20、s21 不送場景圖；群眾縮成三、四個已站好的人；
OFFSCREEN_SPEECH 關掉；s30 不咬飯糰；s38 不寫紅光；火都寫在牆外、沒有人著火、沒有血。

問題集中在四處：

1. **參考圖的狀態壓過文字**（第 15 集 s25、第 16 集必改 1 的同一個教訓），本集三處：
   院子 `set-xujia-yuan-l3` 是日出暖光、右牆外是收割過的田與遠山，**沒有房子、沒有火、沒有煙**，院子 12 鏡的「牆外紙坊在燒」只靠文字；
   夜骨架試鏡畫的是**四柱兩梁完整**的骨架，但 s27–s28 還在立柱；天亮骨架從另一張底圖（`set-gongpeng-l3`）獨立生成，柱子位置不會跟夜版一樣。
   兩張底圖右邊都有**一張木桌**（夜版桌上還有蠟燭）、左前大桶裡有攪棒，負面詞沒擋，編輯很可能留下。
2. **阿令散髮**：三張參考圖都是頭頂高髻加木簪、長髮已經垂在背後，散髮跟參考圖唯一的差別是「頭頂沒有髻和簪」——這點文字幾乎贏不了三張圖，
   s11–s14、s17 照現在送圖，草稿大概會留髻留簪，s17 撿木簪就沒道理。
3. **方向與手的寫法自相矛盾**：s15 秦霜面向畫左卻往畫左倒退；s24 二牛走向畫左卻「回頭」喊；s25 二牛背影朝畫右，跟 s24 走向相反（跳軸）；
   s26 他面向畫右、竹簾夾在左臂卻寫在畫面左下，從左緣伸進來的手要橫過他身體。
4. **extras 的「the air is clear and still」**跟火場每鏡的濃煙寫在同一支提示詞裡，s11、s12、s16 更是「濃煙填滿畫面」。

寫稿者最沒把握的事，結論：

| 問題 | 判斷 | 怎麼做 |
| --- | --- | --- |
| 阿令散髮能不能壓過參考圖的挽髮 | **壓不過**。差別只在頭頂，三張圖都清楚畫出髻與簪，側面圖 angle-b 最明顯 | s11–s14、s17 拿掉 angle-b；近景 s12、s14 只送 angle-a，s11、s13、s17 只送 portrait；散髮寫成跟參考圖看得出差別的樣子（髮落到胸前、幾縷貼在濕臉上）；挑片把「頭頂有髻或簪」列為退件。見必改 10 |
| 三張紙坊新圖會留原屋頂或桌子；夜版與天亮版骨架對不上 | **都會發生**。三張是各自從兩張不同底圖獨立編輯，桌子、桶、攪棒、蠟燭不在負面詞裡 | 燒毀版照跑、負面詞補桌椅；夜版改成「骨架只立一半」；天亮版改成**以挑好的夜版為底圖**的換光編輯（只改光與篝火、補齊柱梁、加梯子）。見必改 3、4 |
| s27–s28 還在立柱但夜圖骨架已完整 | **衝突，而且在同一支提示詞裡**（場景句四柱兩梁都立著，構圖句又一根柱子斜靠在右邊） | 夜圖畫兩根後柱加一根橫梁、兩根柱子平放在地上；s27、s28、s31 的場景句照改。見必改 3 |
| s15 草頂遠處塌下火星 | 可以留，但現在院子圖牆外沒有屋子，塌頂多半畫不出來；火星屬特效、不算 `physics.fluid` | 先做院子起火版的圖（必改 1），第一格就看得到牆外燒著的草頂；塌下寫成「往下沉、一陣火星往上」，大重音交給音效。沒有新圖就把塌頂改在 s16 身後的火光裡 |
| s07 二牛往牆外潑水（液體加火） | 現在一鏡裡有「扁擔下肩→抓桶→潑出長弧→伸手拿第二桶」四拍，扁擔還吊兩桶，`physics.fluid` B 加 `hands.small-prop` C | 第一格扁擔已平放地上、一桶已在兩手，只拍桶口越過牆頭一倒，水落在牆後看不到的地方，見必改 9 |
| s01 三人小全景加跳躍 | `action.fast` 加 `cast.three` 兩個 B；跳在半空的第一格最容易糊、落點接不上 | 第一格許硯已落在棧橋上往右跑，秦霜一腳跨上棧橋，不寫半空。見必改 14 |
| 院子圖沒有火，「牆外的火」被圖壓過（s02 s06 s09） | **會被壓過**。圖上右牆外是田與遠山，日出光反而會被讀成「晴朗早晨」 | 加一張 `set-xujia-yuan-huo-l1`：從 l3「只改一件事」的加法編輯（README 第 16 集的做法），院子 12 鏡都換送這張。見必改 1 |
| s12、s26 手的交接；s30 拍頭 | s12 可以（她面向畫左、手從左緣進來，方向對）；**s26 方向錯**；s30 手第一格已在頭上，可以，但兩下輕拍改一下 | s26 見必改 8；s30 見建議 |
| 小禾與二牛錄音語氣 | 小禾 a27 聽寫正確、基頻中位數約 290 Hz、5.04 秒，奶聲合理。二牛 a07 中位數約 320 Hz，是他 a22（172）、a26（195）的近兩倍，像尖叫；a22「跛子」三句都被聽成「脖子／箔」 | 見建議：a07 聽一次、必要時照 e914 的 PITCH 做法壓回他的音域；a20–a22 確認「跛」念第三聲 bǒ |
| s21 地點句 paper workshop 警告 | 是誤報（paper 是地名的一部分，畫面只有灰與鞋印），但不送場景圖的插鏡多一個 paper 字沒好處 | 正面補一句「blank」的灰地，警告就消，見建議 |

## 必改（14 條）

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 917 | s02–s10、s13–s15（院子 12 鏡） | 送的 `set-xujia-yuan-l3` 右牆外是收割過的田與遠山，沒有屋、沒有火、沒有煙；太陽在畫右柿子樹後。提示詞說牆外紙坊在燒，圖說是晴朗日出，圖會贏 | 第 15 集 s25、第 16 集必改 1「參考圖狀態壓過文字」；README 第 16 集「大物件靠『只改一件事』的編輯」 | **場景試鏡加第四張** `set-xujia-yuan-huo-l1`（以 l3 為底，種子照 37019／37020）：正面提示詞 `image 1 is a photograph of the place: keep exactly everything in it, its camera position, the farmhouse, the gate, the persimmon tree, the well and the low mud wall; change one thing only: beyond the low mud wall on the right, where the field was, the thatched roof of a small work shed stands just behind the wall and is on fire, tall orange flames on its roof and thick grey smoke rolling up and drifting to the right, the sun hidden behind the smoke, the whole yard lit warm orange by the fire.` 負面：`people, person, flames in the yard, fire on the farmhouse, fire on the tree, text, watermark`。挑好之前院子這 12 鏡不拍；`gen-dh.mjs`／spec 的院子鏡改送這張 |
| 917 | s02–s16（尤其 s11、s12、s16）、s17、s27–s35 | extras 每鏡補「the air is clear and still」，火場同一支提示詞又寫「thick grey smoke filling the air」；s17 有白煙、夜場有篝火煙。自相矛盾，模型會把煙減掉或拍得一團糊 | 拍法 18 的乾淨句是為了擋霧氣雜訊，沒預期火場；同一句前後矛盾 | `extras.json` 不動，在 `mkspec.py` 對 s02–s16 加 replace：把 `the air is clear and still, a clean natural film image.` 換成 `the smoke rolls slowly and evenly and stays where it is described, a clean natural film image.`；s17–s26 換成 `the thin white smoke rises straight and slowly, a clean natural film image.`；s27–s35 換成 `the bonfire smoke rises thin and straight, a clean natural film image.` |
| 917 | s27、s28、s31（夜骨架）＋場景試鏡 `set-zhifang-gujia-ye-l2` | 試鏡與場景句都是「四根柱立好、兩根橫梁」，但 s27 還在挖柱洞、s28 兩人拉繩立柱；s28 同一支提示詞前寫四柱都立著、後寫一根柱斜靠在右 | 參考圖狀態壓過文字；script 第三場「一根根立起來，c36 立成骨架」 | **改試鏡提示詞**第 (3) 點為：`(3) in the middle the new frame is half built: two thick round posts of freshly peeled pale yellow pine stand upright at the back with one round crossbeam laid across their tops, and two more peeled pine posts lie on the swept ground in front of them, open to the sky;`（5）改 `two plain round pale paper lanterns hang from the crossbeam at the back`。s27、s28、s31、s32–s35 的場景句同步改成同一句；s28 構圖寫 `the rope running up to the top of one peeled pale pine post leaning at the right, its foot in a post hole` |
| 917 | s36–s40（天亮骨架）＋場景試鏡 `set-zhifang-gujia-chen-l1`、三張共用負面詞 | 天亮版從 `set-gongpeng-l3`、夜版從 `set-gongpeng-ye-l2` 各自生成，柱子位置、篝火位置一定對不上；兩張底圖右邊都有木桌（夜版桌上一支蠟燭）、左前大桶插攪棒，負面詞沒有 table、candle、tub、stirring stick | README 第 14–16 集「桶裡攪棒、左邊長竿一直留著」；README 第 16 集「拿上一輪的好圖當底」 | 天亮版**等夜版挑好後**再跑，底圖改成挑好的 `set-zhifang-gujia-ye-l2`：`image 1 is a photograph of the place at night: keep exactly its camera position, the walls, the stone ring at the front left and the two back posts with their crossbeam where they stand; change it to first light of dawn: the two posts that lay on the ground now stand upright at the front, a second crossbeam across their tops, one plain wooden ladder leaning against the right-hand front post, the bonfire burnt down to a bed of grey embers with one thin thread of smoke, the sky pale, cool dawn light with low gold light from the right on the new pine.` 三張負面詞都補 `table, bench, furniture, candle, wooden tub, stirring stick`；燒毀版的 `walls of a house` 拿掉（跟 KEEP 要留的石牆衝突）。正在跑的 ye、chen 四支結果不用 |
| 917 | s15 | 秦霜 `face three-quarter to screen left` 又 `walks backward toward screen left`：面向左走就是往前，不是倒退；倒退會走向畫右的火 | 拍法 9 位置寫死；同句矛盾 | `in the middle Qin Shuang, her back to the wall and the fire, faces screen left toward Wang Erniu with both arms spread wide; she steps forward toward screen left, herding him back, and Wang Erniu backs away toward screen left in front of her, the empty bucket in his right hand.` |
| 917 | s24 | 一人長的扁擔「gripped in his right hand」「swinging」，又是要去抓人的怒氣——第 15 集犁畫成兵器、preflight prop 警告；臉朝畫左走卻 `shouting over his shoulder`，句中的「turned toward the person he is speaking to」沒有聽的人，會看鏡頭 | e915 picks s21（農具畫成兵器）；拍法 18 道具寫樣子；e916 審稿 gaze | 扁擔改扛肩上、不揮：`the plain flat wooden carrying pole as long as a man resting across his right shoulder, his right hand on it, its two short ropes hanging loose` ；動作 `Wang Erniu strides three long steps toward screen left, the pole steady on his shoulder, shouting ahead toward the yard gate`；spec 加 replace，把 SPEAK_GAZE_HE 換成 `his face three-quarter to screen left toward the yard gate ahead of him, his eyes on the gate`（拿掉 over his shoulder） |
| 917 | s25 | s24 二牛往畫左走，s25 他的背影在畫左前景、面朝畫右的韓伯——方向反了（跳軸）。韓伯「staff … in his right hand」又「holding the staff crosswise in both hands」，身分句還寫「leaning on」 | 拍法 9；script 軸線「院門在左」；同句矛盾 | 前景換邊：`past one big broad-shouldered young man seen only from behind in the right foreground, facing screen left, the carrying pole on his right shoulder; facing us a step in front of him, a little left of the middle, Elder Han, his face three-quarter to screen right toward him`；竹杖寫一次：`his polished bamboo walking staff held level across his chest in both hands, a hand's width in front of the young man`；spec 對 s25 把身分句的 `leaning on a polished old bamboo walking staff` 換成 `with a polished old bamboo walking staff` |
| 917 | s26 | 許硯臉 3/4 朝畫右（看韓伯），左臂在他身體的畫面右側，提示詞卻把竹簾寫在「bottom left」、阿令的手從左緣伸進來接——手要橫過他胸前，正是 e915 s01、s30「東西給錯人」的條件 | 拍法 5 的「手依站位寫成畫面側」；e915 picks s01、s30 | 竹簾換到畫面右下、手從右緣進：`the bamboo mat clamped under his left arm, which is on the screen-right side of his body, at the bottom right of the frame … one slender hand in a grey-white sleeve reaches in at the right edge, takes the mat from under his left arm and draws it away past the right edge`；mkspec 的 `besides("him", …at the left edge)` 同改 right edge |
| 917 | s07 | 一鏡四拍：扁擔吊兩桶從肩上放下→雙手抓桶→長弧潑過牆→伸手拿第二桶。`physics.fluid` B 加道具換手 C；扁擔在身分句外又出 prop 警告 | shot-risk.md `physics.fluid`、`hands.small-prop`；騙鏡第 1 招「切在動作兩端」 | 第一格：`the carrying pole already lying on the ground at his feet with one full bucket beside it, the other bucket held up in both his hands by its rim and bottom at chest height against the top of the wall`；動作：`Wang Erniu heaves the bucket up and tips it over the top of the wall; the water pours out over the wall top and falls away behind the wall out of sight; after the last word he lowers the empty bucket, teeth gritted` |
| 917 | s11、s12、s13、s14、s17 | 阿令散髮靠文字，送 portrait＋angle-a＋angle-b 三張高髻插簪的圖（angle-b 側面最清楚）；參考圖本來就長髮垂背，文字寫的「hanging straight down her back」跟圖幾乎一樣，唯一差別（頭頂沒有髻）最容易被圖蓋掉。s17 她撿木簪，頭上若還插著簪就不成立 | 「參考圖狀態壓過文字」；e913–e915 挑片同類 | spec `drop_pictures`：s11、s13、s17 留 `aling-portrait-l1`、拿掉兩張角度圖；s12、s14 只留 `aling-angle-a-l1`（她 3/4 朝畫左，跟 angle-a 同向）。ALING_HAIR 的新句改成看得出差別：`long glossy black hair, in this shot let down completely: the crown of her head smooth and bare, the wet hair falling loose over both shoulders and down her chest, a few strands stuck to her damp cheek`。挑片把「頭頂有髻或木簪」列為退件 |
| 917 | s20、s26、s35、s37、s39、s40 | 銅片寫成「the outline of one round coin with a square hole」：模型畫方孔錢幾乎一定加四個字（通寶錢文），s20 還要轉過來正對鏡頭 | 拍法 7、17「紙上與物上的字一律不拍」；shot-risk `text.readable` | 道具句改成只寫形狀：`one small round copper plate as small as a thumbnail, with one raised plain ring around a small square hole cut through its centre, the metal smooth and polished between the ring and the hole`（六鏡同一句；r2.py 的燈籠常數改一次） |
| 917 | s09 | 「wide shot past one wooden bucket held up in the right foreground」：桶沒有主人，script 自己的規定是每個木桶都拿在一個人手裡；浮空的桶會多長一個人或分身 | script「火」條；storyboard-shot-spec「群眾拿的東西沒人拿」 | `wide shot past one wooden bucket held up in the right foreground by two hands in coarse brown sleeves at the right edge, the villager's face out of the frame`；只有一句改 mkspec 的 only 句：`Besides him, only the other people the composition names and the two hands at the right edge are in the frame; no second copy of anyone appears.` |
| 917 | s16 | 說話句帶「turned toward the person he is speaking to … eyes on that person」，但畫面沒人、構圖也沒寫聽的人；動作又「stares back over his shoulder at the glow」，同鏡兩個視線方向，容易看鏡頭 | e916 審稿 gaze；s07、s08 已用同法改 | spec 加 replace：把 SPEAK_GAZE_HE 換成 `his face three-quarter to screen left toward Xu Yan off screen left, his eyes on him`；動作改 `Carpenter Shi drags the back of his right hand once across his eyes and lets it fall, his eyes going back to Xu Yan off screen left` |
| 917 | s01 | 第一格「already in mid-leap」：三個有名字的人都小、又是跳在半空；落點接 s02 不接得上 | shot-risk `action.fast`、`cast.three`；騙鏡第 5 招「進場改成在場」 | `Xu Yan … already landed on the jetty planks, running along them toward the bank at the right`；`Qin Shuang stepping off the raft onto the jetty, one boot on the raft and one on the planks, the punting pole falling from her right hand onto the raft`；動作句的 `jumps onto the jetty` 改 `steps up onto the jetty and runs after him` |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 917 | s15 | 塌頂在牆外遠處，現在的院子圖上沒有屋頂可塌 | 參考圖狀態 | 有起火院子圖後，第一格寫 `beyond the low mud wall at the right the burning thatched roof of the work shed shows above the wall top`；動作 `the burning roof sinks down behind the wall and a cloud of orange sparks rises into the smoke`。沒有新圖就把塌頂放到 s16：`behind him, far off in the smoke, a burning roof sinks down with a burst of orange sparks` |
| 917 | s11、s12、s13 | s11、s12 在「紙坊旁」，s13 在院子土牆前；院子圖右牆是一整面，阿令怎麼從牆外的火裡到院子裡交簾子沒交代 | script 軸線 | s11 場景句：`at a gap in the low mud wall between the yard and the burning shed`；s12 背景跟 s13 一樣寫 `behind her only the low mud wall and the grey smoke lit orange` |
| 917 | s03 | 身分句後的服裝句寫「her black hair pinned up **again**」：火災之前沒有散過；她也還沒進火場卻「grey with soot」 | 連戲 | `her black hair pinned up with one plain wooden hairpin`；衣服寫 `her plain grey-white cotton dress clean`（灰從 s11 起） |
| 917 | s06 | 秦霜面向畫左（院門），右手揮向畫右的牆——右臂在她身體遠側，揮向身後很彆扭 | 拍法 9 | `her head turned over her left shoulder toward the yard gate, her right arm stretched out toward the wall and the fire at the right`（身體朝右、頭轉向門） |
| 917 | s28 | 「beside him on his right Xu Yan」：兩人面向畫右時，他的右邊在遠側，可讀成畫左或前後 | 拍法 9 | `and just to screen right of him Xu Yan` |
| 917 | s30 | 拍頭兩下是兩人接觸（C）；竹盤寫「six rice balls」，但 s29 已遞出一個 | shot-risk `contact.two-person`；道具連戲 | 手第一格已在頭上可以保留，動作改 `pats the top of her head once, slowly, and lifts his hand away`；竹盤 `five plain white rice balls` |
| 917 | s21 | preflight `paper` 誤報（地點句 burnt paper workshop）；插鏡不送場景圖，地點句多一個 paper 沒好處 | preflight PAPER | 地點句加正面一詞：`In the burnt paper workshop on the morning after the fire, smooth blank grey ash and charred posts, bright morning sunlight from the right:` 警告即消，gen-dh 的地點對應不變 |
| 917 | s23 | s17、s18 唐小棠坐在畫左石階，s23 背拍改到右前景站起；背拍反打可以，但同一場她左右換邊，又是背影鏡，觀眾難認 | 拍法 3「固定在哪一側」 | 留在左前景：`rising from the low blackened stone step in the left foreground … she stays in the left foreground from the first frame to the last`（mkspec 的 ALONE 不用改） |
| 917 | s11 | only 句重複兩次（「she is the only person in the frame. She is the only person…」） | 文字整潔 | r2.py 的 s11 構圖去掉尾端 `she is the only person in the frame` |
| 917 | s31 | 膝上素木算盤，腰間又有身分句的小金算盤，同畫面兩把算盤 | e916 必改 11（錢袋與算盤合成一樣）；拍法 4 | 腰間那句改 `the small gold abacus hanging at her right hip, still`；素木算盤寫 `on her knees, the only thing her hands touch` |
| 917 | 院子 l3 | 圖上右牆邊斜靠一塊木板與一根長木棍；第 11–13 集背景長槍的來源之一就是斜靠的長竿 | README 第 14 集、拍法 18 | 做起火院子圖時**不**順手拿掉（只改一件事），挑片時看那根棍有沒有變成槍；若長成兵器，再做一次「只把木板與木棍拿掉」的去除編輯 |
| 917 | a07（s07） | 二牛 a07 基頻中位數約 320 Hz，是他 a22（約 172）、a26（約 195）的近兩倍，大吼可能像尖叫或憨笑（cast 聲音「愛憨笑」） | 自相關估算；e914 `_note` 的 PITCH 做法 | 人耳聽一次；偏尖就照 e914 用 rubberband 保共振峰降到他的音域，或重錄「大吼、粗、低」 |
| 917 | a20、a21、a22（s22、s23、s24） | faster-whisper 三句都把「跛子」聽成「脖子／箔字」，a22 那個字的基頻 112→167 Hz 往上走，可能被念成第二聲 bó；這是本集破案關鍵字 | 錄音核對 | 人耳聽三句；若是 bó，重錄時在提示裡寫「跛，ㄅㄛˇ」 |
| 917 | 共用設定 | `r2-bible-e011-e020.md` 道具表寫燈籠骨架是「燒剩的紙上一個圓圈裡一道斜槓」、第 17 集許硯撿；本集與第 18、19 集稿都是底座銅片、秦霜撿 | 設定一致 | 共用設定道具表改成「底座拇指甲大小的素銅片（一圈凸環、中間方孔）、秦霜從灰裡拉出、c26 起在許硯右手」 |
| 917 | s14、s05 | 近景送院子圖，現在的院子圖是金色日出；有起火版後一起換送 | 必改 1 | 跟必改 1 同步 |
| 917 | season-01 | 季綱前 3 秒是石木匠嘶喊與阿令衝進濃煙；r2 開頭是 3 秒無台詞的竹筏。整季合成一支，問題不大 | 季綱 | 若必改 14 的 s01 草稿仍不穩，照稿子「先刪 c01」直接從 s02 開始，接第 16 集 s42 的竹筏衝岸沒有斷 |

## 場景試鏡要改的（明確）

試鏡正在跑（`live-screen-test-e017/out/progress-1.json`）。

- `set-zhifang-shao-l2`：可以照跑、照挑；下一輪若要重跑，負面詞補 `table, bench, furniture, candle, wooden tub, stirring stick`、拿掉 `walls of a house`。挑的時候放大看右邊有沒有完好的桌子、左前桶裡有沒有攪棒。
- `set-zhifang-gujia-ye-l2`：**要改**（必改 3、4）：骨架只立一半（兩後柱一橫梁、兩根柱平放在地）、燈籠掛在後面那根橫梁、負面詞補桌子蠟燭桶攪棒。這一輪的結果不用。
- `set-zhifang-gujia-chen-l1`：**要改**（必改 4）：等夜版挑好，以挑好的夜版為底圖做換光編輯，補齊前柱與第二根橫梁、加梯子。這一輪的結果不用。
- **新增** `set-xujia-yuan-huo-l1`（必改 1）：以 `set-xujia-yuan-l3` 為底，只加牆外燒著的工棚草頂與煙。
