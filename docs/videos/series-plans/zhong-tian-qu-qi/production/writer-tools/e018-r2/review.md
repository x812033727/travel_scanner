# 第 18 集重製版（e018-r2，內部編號 918，真人版）分鏡與提示詞：開拍前獨立審稿

- 審稿：沒參與寫稿的獨立審稿代理，2026-11-16。只讀，只寫本檔；沒用 Colab、RunPod 或任何付費服務，沒有 git commit。
- 審的版本：`docs/videos/zhong-tian-qu-qi-e018-r2/{script.md, storyboard.md, video.json, overlays.json}`、`writer-tools/e018-r2/r2.py`、
  `colab/runs/e918/extras.json`、`colab/runs/e918-live/{mkspec.py, spec.json}`，以及實際要送的
  `/root/mokaair-work/videos/zhong-tian-qu-qi-e918-dh/runpod/live/d1/colab-jobs.json`（82 支 = 41 鏡 × 9181101／9181102）與 `prompts/`。
- 機械檢查（本審稿自己跑）：兩個種子的提示詞逐位元相同；82 支的參考圖全部是絕對路徑、檔案都在；台詞 39 句都在 script.md 裡、一字不差；
  overlays 兩個面板（s01、s29）跟系統句一致。否定詞掃描：除了允許的「no second copy / no talking / no mouthing words / nothing tucked in it / no subtitles」，
  **只剩一個被否定的名詞：紅手句的「clean of any wound」**（s26、s28、s29、s30，見必改 10）。
- 錄音：`audio/zq918a01–a39.wav` 用 ffprobe 量長度、silencedetect 看停頓；faster-whisper medium（scratchpad 的 `fw` 環境）重聽 a03（處理後與 raw-tts）、
  現在的 a34、a36、a07。BUY 全部放得下：6 秒鏡最緊是 s30 a29 6.08 秒（人聲 0.35–5.76）、s32 a31 6.04 秒（人聲 0.26–5.77）、s37 a36 5.92 秒；
  8 秒鏡 s25 a24 7.08、s31 a30 6.88、s36 a35 6.40、s37b a37 6.16；s02 三句 10.39 秒（含邊界靜音）。
- 放大看過：`set-chalou-l1`、`set-qianfu-houmen-ye-l1`、`set-xianya-gongtang-l1`、`set-xianya-ceting-l1`，唐小棠 l1 與 angle-a／b、錢員外 l1 與 angle-a／b、胡縣令 l1、賴三 l1；
  另外在 scratchpad 試裁了建議用的三張衍生圖（見〈參考圖〉）。
- 對照：`r2-bible-e011-e020.md` 拍法 1–18（尤其 2、3、5、7、9、12、15、18）、`r2-bible-e011-e060.md`（第 18 集時間線、交接表 17→18、18→19、第 482 行原版問題「錢員外藏手的戲，手卻一直露出來」）、
  `season-01.md` 第 18 集、`writer-tools/e017-r2/review.md`、`colab/runs/e91{4,5,6}-live/{review-picks-a,review-picks-b,picks-merged}.tsv` 與 `e916-live/fix1/`、
  任務檔第 13–15 集教訓、第 17 集 r2 s35–s40、第 19 集 r2 script c01。

## 總評

做到的：唐小棠五句都背拍、spec 拿掉她的臉部圖與身分句；帳房只有背影與手；兩人接觸（s21、s28、s30、s40）都寫成第一格狀態；紙一律紙背或摺著；
沒有衙役、沒有兵器、秦霜腰帶空著；s33、s35 攤手不指人；胡縣令與錢員外不同框；OFFSCREEN_SPEECH 關掉、每個不說話的人都寫了閉嘴；c37 拆成兩鏡的理由（11.4 秒裝不進 10 秒）成立。

問題集中在五處：

1. **參考圖的狀態壓過文字**（第 15 集 s08「空工棚全景硬切到插鏡」、第 16 集 s39、第 17 集審稿必改 1 的同一個教訓），本集三處：
   插鏡 s05、s12 送的是茶樓全景；公堂 s31、s33–s38 送的公堂圖正中是**空著的公案與官椅**、上方是**一面畫著東西的匾**（不是空白）；
   s24 的後院圖裡**沒有門板**、圓石桌在**很遠的小亭裡**，提示詞卻寫「中景、從膝蓋以上、臉被右門板擋一半」。
2. **唐小棠背影的寫法沒有用第 16 集修好的版本**：`TBACK` 還是「兩條長粉緞帶從丸子頭垂到肩上」，第 16 集 s32 1102 就是這兩條長緞帶畫成兩條棕色長馬尾，
   `e916-live/fix1/mkspec.py` 改成「兩顆高丸子、各繞一條短緞帶、後頸露出」後才乾淨。六支背影鏡（s03、s04、s06、s08、s09、s13）全部要換。
3. **錢員外白天的手**：s37「袖裡的手腕抵在額頭上」、s40「袖裡的手腕勾住許硯前臂」都要手舉起來，模型最容易讓手從袖口滑出來——
   原版第 18 集的必修問題正是這個（共用設定第 482 行）。
4. **方向與數量自相矛盾**：s39→s40 錢員外與許硯左右對調（跳軸）；s30 秦霜的手按在賴三離她遠的那一邊肩膀；s17 箱子同時「蓋著」又「打開」；s25 箱裡三個布包加手上一個是四個；
   s07、s03 寫了「嘴唇張開」「頭偏一下」又寫「嘴不動」「頭不動」。
5. **狀態在鏡頭裡改變**：s18 吹熄油燈要在一支 6 秒裡從暖光掉進冷藍，s26 的紅在暖燈籠光下、又在袍子上「用力擦」，最容易讀成血；
   紅手句裡還寫了被否定的名詞「wound」（拍法 18）。

**必改 16 條、建議 18 條。** 參考圖：**不必重畫**，但要做三張**免費的裁切衍生圖**（茶樓長凳、公堂地面、公堂公案），s24 的門縫改在剪接做遮罩；
唐小棠背影參考圖是可選的「只改一件事」編輯（見文末）。

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 改法 |
| --- | --- | --- |
| s04、s09 只送茶樓圖、沒有唐小棠的圖，丸子頭可能走樣 | **會走樣，但原因不在少送圖**：六支背影鏡（s03、s06、s08、s13 也一樣）都沒有她的圖，這是拍法 3 的既定代價（第 8 集送臉部圖就冒分身）。真正的風險是長緞帶句（第 16 集 s32 變馬尾）。 | 必改 1：換成第 16 集 fix1 的「兩顆高丸子、短緞帶、後頸露出」，並寫她看前方的固定視線。另可選：做一張背影參考圖先在 s09 試（文末）。 |
| 紙坊夜景、錢府後巷不送圖，夜景與骨架能否接第 17 集 | **可以接**。第 17 集最後是天亮的四根淺色剝皮松木柱（`set-zhifang-gujia-chen-l1`），本集文字寫同樣四根白松柱、兩天後蓋了半邊草頂，梯子、大木桶不在了合理；白天圖拿去拍夜戲會變白天（拍法 8），夜骨架圖是第 17 集的篝火狀態，不送是對的。第 16 集 s39、第 17 集 s17–s26 不送場景圖都沒出事。 | 不用改；建議 9、10 補兩處站位與柴堆寫法。 |
| s31 公堂圖正中公案長出一個官、匾額長假字 | **風險很高**。公堂圖是正面對稱構圖、正中一把空官椅；圖上的匾**不是空白**（藍金色的一片畫，放大像字）。提示詞的 `HALL` 句又把平台、公案、官椅、匾全寫進全景，還用了「the magistrate's raised desk」這個會叫出縣令的字。 | 必改 12、13：地面鏡送裁掉公案的「地面」衍生圖、場景句只寫柱子窗戶地磚、不寫 magistrate；胡縣令兩鏡送裁掉匾的「公案」衍生圖。 |
| s05、s12 帳房的手長成整個人露臉 | **風險高**，而且有前例：第 15 集 s08 送工棚全景給插鏡，兩支都在片中從全景硬切到插鏡。茶樓全景圖裡長凳離鏡頭遠、整間房都在，插鏡一推就可能拉回全景、把坐在凳上的人補出來。 | 必改 3：送長凳特寫的裁切衍生圖，構圖寫成往下看凳面、袖子在前臂處被畫框切掉。 |
| s24 從門縫看但圖上沒有門板 | **門板畫不出來**（圖上沒有、文字要兩側各一片），而且圖上的石桌在遠處小亭裡，「從膝蓋以上、臉被右門板擋一半」跟圖打架。 | 必改 8：門縫改在剪接用柔邊黑遮罩做；提示詞照圖寫成走道盡頭小亭裡的小人。 |
| s18 吹熄油燈變暗、s26 手上橘紅讀成血 | **兩個都會出事**。一支片段裡大幅改光，模型常常不熄、或熄了又亮、或整支曝光抽動；熄了之後的「嘴角一揚」也看不到。s26 暖燈籠光把橘紅推向血色，「用力擦」會在金袍上留下紅痕，像抹血；「clean of any wound」是被否定的名詞。 | 必改 7：剪在吹氣那一下、燈還亮著，熄滅交給音效與 s19 第一格。必改 10：紅寫成啞光柿子橘紅、像布上的染料，擦過的金袍寫明保持乾淨，拿掉 wound／unbroken。 |
| s37 拆成 s37／s37b 後錢員外在畫面上說原本「畫外，急」的錄音 | **拆鏡本身可以**（兩句 11.4 秒裝不進 10 秒），錄音 a36 實際是慢的、帶停頓（0.68 秒才開口，中間兩段各 0.36、0.23 秒），正好配「裝頭暈」，在畫面上說沒問題。**問題在拍法**：s36 與 s37 是同一人、同景別、同方向的兩個近景，接起來是跳接；s37「袖裡的手腕抵額頭」會讓手露出來。 | 必改 14：s37 改中景（腰以上）、手不離開肚前的袖口。 |
| a03、a34 錄音 | **a03**：raw-tts 聽寫是「宿主天天喝茶」，處理後（1.3 倍＋電子音）聽寫成「宿主**甜甜合**茶」，處理把聲調抹平了；這是系統聲全季的做法（a01「剩五日」也被聽成「聖武日」），不算錯，但「天天／甜甜」會改意思。**a34**：新錄的「錢員外」聽成「前院外」（員的聲調），比第一次的「秦雲外」好；但新的「人證」聽成「任正」，第一次錄的「人證」是對的。 | 建議 16、17：a03 由人耳聽一次，聽得出「甜甜」就改用 1.15–1.2 倍處理；a34 可以把 take1 的 0–1.56 秒（「人證就在衙門外」）接上新錄的 1.98 秒起（「錢員外……」），同一個 TTS 聲音、免費。 |
| 帳房聲音 Puck 只寫在 r2.py | **製作上沒問題**：`build-r2.py` 把 `MINOR` 併進 `video.json` 的 `characters`（已核：zhangfang 的 voice 是 Puck），剪接與九語配音讀的是 video.json；第 8 集宗鏢頭、門房也是這樣。**要注意的是 Puck 在 `cast.json` 已經是許大郎（第 41 集起）**。 | 建議 18：在 `r2-bible-e011-e060.md` 的人物表（或 `cast.json` 旁的說明）記一行「錢府帳房 zhangfang：Puck，只有第 18 集 s05 一句」，第 41 集選聲時知道撞聲。 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 18 | s03、s04、s06、s08、s09、s13 | `TBACK` 寫「two long pink silk ribbons hanging from the buns down over her shoulders」，第 16 集 s32 1102 就是長緞帶變成兩條棕色長馬尾；`only_tang`／`HEADSTILL_TANG` 也只說「buns and pink ribbons」。六支都沒送她的圖，頭髮全靠這一句。 | `e916-live/picks-merged.tsv` s32、`e916-live/fix1/mkspec.py` 第 26–28、96–100 行（fix1 1202 取用：兩顆高丸子、短緞帶、後頸露出）；拍法 3 | `TBACK` 換成：「one young woman seen only from behind, appearing only once: the back of her head with all of her black hair gathered up into two round buns set high on her head, a short pink silk ribbon wrapped around each bun and one pearl pin in each, the nape of her neck bare above a pink inner collar, and her light peach-pink silk shoulders; the back of her head toward us the whole time, her ear the furthest round her head we ever see」。`only_tang` 與 `HEADSTILL_TANG` 的「two buns and pink ribbons」改成「two high round buns」。每支加一句固定視線：s03／s06／s08／s13「she looks straight ahead across the table at the young man the whole shot」，s04「she looks straight ahead at the man's back」，s09「she looks down at her right sleeve the whole shot」。 |
| 18 | s03 | 動作寫「tips her head a little toward the right」，同一句後面又寫「keeps her head still」；偏頭正是背影轉頭露臉的起手（第 14 集 s24 四支全轉頭）。 | `e914-live/picks-merged.tsv` s24；拍法 3 | 動作改成：「the young woman holds the cup still in front of her face, her right elbow lifting a little toward the window; the young woman with the two high round buns keeps her head still, the back of her head toward us the whole shot」。往窗邊點的意思交給許硯的眼睛（已寫）。 |
| 18 | s05、s12 | 插鏡只送 `set-chalou-l1` 全景：整間房、樓梯、長凳在畫右後方。第 15 集 s08 送全景給插鏡，兩支都從全景硬切到插鏡；全景裡坐在長凳上的人也會被補出來，帳房就露臉了。 | `e915-live/picks-merged.tsv` s08（fix：不送工棚圖）；拍法 10 | 改送裁切衍生圖 `set-chalou-bench-l1`（`ffmpeg -i set-chalou-l1.png -vf "crop=656:368:656:368,scale=1312:736"`，只有右半張茶桌、長凳、窗台與屋瓦，已在 scratchpad 試過），spec 用 `swap_pictures` 換、絕對路徑。構圖句開頭改成：「insert close-up looking down onto the seat of the plain wooden bench under the window from its very first frame, the bench seat filling the lower two thirds of the frame, the window sill and grey roof tiles at the top edge;」，手的句子後面加「the frame cuts the dark green sleeve at the forearm at the right edge」（顏色見建議 2）。 |
| 18 | s07 | 構圖寫「lips parting and then pressing shut」，動作又寫「his lips stay pressed together from the first frame to the last」。這鏡是唐小棠的錄音、他不能動嘴；第 10 集 s16 就是畫外句時畫面上的人張嘴、整鏡重拍。 | 拍法 15；同一支提示詞前後矛盾 | 表情句改成：「the colour leaving his face: brows drawing together hard, eyes widening a little, lips pressed together」。 |
| 18 | s09 | 構圖寫「beyond her across the table only the empty chair」：圖上茶桌旁根本沒有椅子（模型會另畫），而且「空位」等於說許硯走了，s08、s10 他都坐在那裡，接不上。 | `set-chalou-l1`（低茶桌、沒有椅凳）；接戲 | 構圖改成：「close medium shot from just behind her right shoulder and a little low: her right shoulder, her right arm, the folded slip in her right hand and the near edge of the tea table fill the frame; beyond the table edge only soft dark shadow, out of focus」。`only` 句不變（她是畫面裡唯一的人）。 |
| 18 | s17 | 兩處：秦霜「framed from the waist up with clear space above **his** head」（代名詞錯）；`BOX` 句帶著「its lid shut」，後面又寫「open in front of her」、箱裡放石頭——同一個箱子又關又開。 | 同一支提示詞前後矛盾；拍法 10 | 改成：「standing at the table, framed from the waist up with clear space above her head, one dark brown wooden box as long as a forearm and a half and half a forearm high standing open in front of her, its lid raised and leaning back on its hinges, one small plain brass hasp on the front edge of the lid, two fist-sized stones wrapped in squares of plain grey cloth already lying inside it」。 |
| 18 | s18 | 「after the last word he blows the small flame out and the frame goes to cool blue darkness」：一支 6 秒裡大幅改光，模型常不熄、熄了又亮、或曝光抽動；熄燈後才寫的「嘴角一揚」也看不到。LIGHT 句「the deep dark night around him stays unchanged」又跟變暗打架。 | 第 15 集以來「狀態在鏡頭裡改變」的失敗；r2.py 第 318 行自己也寫「the cut falls before the dark」，提示詞卻寫了變暗 | 動作改成：「Xu Yan drops the brush into the bowl; after the last word one corner of his mouth lifts a little, then he leans down toward the lamp and purses his lips at the small flame, and the flame bends away from his breath」；LIGHT 用 `work`（「the small warm lamp flame and the deep night stay unchanged」）。剪在吹氣那一下，「吹熄油燈」音效接 s19 第一格的冷藍（s19 已寫燈熄）。 |
| 18 | s24 | 圖上沒有門板，提示詞要「兩片黑門板的邊塞滿左右兩緣」；圖上圓石桌在走道盡頭的小亭裡、很小，提示詞要錢員外在「中景、從膝蓋以上」、臉被右門板擋一半。圖贏文字的結果會是：沒有門縫、或人站到走道中間沒有桌子、或桌子被搬到前景。 | 第 17 集審稿必改 1、第 16 集 s39（參考圖狀態壓過文字）；拍法 2（主觀鏡寫明前景沒有人、沒有手） | 提示詞拿掉門板，照圖寫：「point-of-view wide shot straight down the long passage inside the back gate: at the far end, in the small open pavilion under the warm lantern light, Qian Yuanwai … standing at the round stone table, framed full length, small, half turned, one thin bent iron wire … in his right hand at the brass hasp of one dark brown wooden box … lying on the stone table, his face three-quarter to screen right toward the box; beside him on the left Lai San …, framed full length, small, standing still with his empty hands at his sides; the near half of the passage empty stone paving」。門縫在剪接做：兩條柔邊黑遮罩（左約 18%、右約 22%、邊緣羽化、跟著推鏡輕微收窄），臉擋一半由遮罩決定。 |
| 18 | s25 | 「inside it three fist-sized bundles」又寫兩手「already lifting one bundle out」：箱裡三個加手上一個是四個，跟 s17 的三塊石頭不符；道具數量錯，模型常會照「三個在箱裡」再補一個在手上。 | 道具接戲（script 第二場「三塊用布包著的石頭」） | 改成：「inside it two fist-sized bundles of plain grey cloth, and the third bundle already lifted in his two hands just above the box」。 |
| 18 | s26、s28、s29、s30 | `RED` 句寫「bright orange-red … the skin unbroken, clean of any wound」：wound 是被否定的名詞（拍法 18：寫了就會畫）；「bright orange-red」在暖燈籠光下就是血色；s26「rub hard against the dark gold silk」會在金袍上擦出紅痕，像抹血。 | 拍法 12、18；第 13 集「否定名詞被畫出來」 | `RED` 改成：「stained an even matte persimmon orange-red from the fingertips to the wrists, the colour sitting evenly in the skin like dye in cloth, the skin smooth, whole and dry」。s26 動作後加「where the hands rub, the dark gold silk of the robe stays clean and bright」；s26 的燈光句改成「soft warm lantern light from above and a cool pale glow from the white wall on the left, so the orange of the hands reads clearly」。剪接照 script 把紅手降一點飽和。 |
| 18 | s30 | 秦霜在畫右，「her left hand holding his right shoulder to the wall」：賴三背靠牆正對鏡頭，他的**右肩在畫左**，秦霜要越過他整個人去按——模型會換手、換位，或讓她站到他左邊（變成 s28 的鏡像）。 | 拍法 9（每鏡用畫左畫右寫死站位與手） | 改成：「on screen right Qin Shuang …, framed from the waist up, her right hand pressing his left shoulder, the shoulder on her side, flat against the wall」。 |
| 18 | s31、s33、s34、s35、s36、s37、s38 | 公堂地面鏡送整張 `set-xianya-gongtang-l1`：正中一張空官椅、公案、上方一面畫了東西的匾；`HALL` 句又把「platform … desk … armchair … gilt-framed board」寫進場景，s31、s33、s37 還寫「the magistrate's raised desk」。空椅加「magistrate」很可能補出一個官，跟錢員外同框（兩個胖圓臉中年男人，錢員外的定妝照還戴高黑帽）。 | 共用設定〈同框撞臉〉第 396 行；第 9 集「主觀鏡會讓拍攝者坐進畫面」、第 15 集 s08（全景壓過插鏡）；拍法 18 | 改送裁切衍生圖 `set-xianya-gongtang-floor-l1`（`crop=480:270:0:330,scale=1312:736`：左側兩根柱子、格窗、白色裙板、地磚，沒有公案、官椅、匾，已試過）。這七鏡的場景句改成：「In the court hall of the county yamen on a grey overcast morning: a floor of large grey stone tiles, thick round dark red-brown wooden pillars, tall dark wooden lattice windows along the side wall above a low white panel; soft even grey daylight from the tall lattice windows」；所有「the magistrate's raised desk above the frame」改成「the high dais above the top of the frame」。s31 構圖開頭寫「wide shot across the stone floor along the side of the hall, the pillars and the lattice windows behind them」。 |
| 18 | s32、s37b | 胡縣令低角度近景，身後寫「only the plain white panels」，但送的整張圖白屏板上方就是那面匾（畫的不是空白），低角度推鏡最容易把匾帶進畫面、長出假字；`HALL` 句還寫「one gilt-framed board above the panels with a plain blank face」把匾叫出來。 | 拍法 7、17（匾額寫空白也會長字；圖上的匾本來就不空白）；`refs-live/README.md`（書院 37001 匾額有字的教訓） | 改送裁切衍生圖 `set-xianya-gongtang-dais-l1`（`crop=650:366:330:250,scale=1312:736`：白屏板、官椅、公案、左邊一塊驚堂木、右邊筆架，匾在畫外，已試過）。場景句改成：「…: at the back one long dark wooden desk with one dark wooden armchair behind it, before a wall of plain white panels; on the desk one flat oblong block of dark wood at the left and a small brush rack at the right」，拿掉 gilt-framed board；構圖加「the top of the frame at the top edge of the white panels」。 |
| 18 | s36→s37 | s36 與 s37 是同一個人、同樣「close-up, chest up, three-quarter to screen left」，接起來是跳接。s37 又寫「the back of his left sleeve-covered wrist already pressed to his forehead」再放下：手舉到額頭、放下，正是手從袖口滑出來的動作。原版第 18 集的必修就是「藏手的戲手一直露出來、還是正常膚色」。 | 共用設定第 482 行；拍法 12（白天手不入鏡）；剪接（同人同景別連接） | s37 改中景：「medium shot of Qian Yuanwai, kneeling, framed from the waist up with clear space above his cap, both his hands pushed deep inside his wide dark gold sleeves, the two sleeves joined in front of his belly, his hands hidden inside them the whole time, his face tipped up three-quarter to screen left toward the high dais above the frame, never the lens; pleading and sly: brows drawn up, eyes fluttering half shut, mouth drooping between words」；動作：「Qian Yuanwai sways on his knees as if dizzy, presses his joined sleeves against his belly, then bows his head toward the dais; after the last word he stays bowed, his eyes sliding sideways」。storyboard 與 script〈真人版的改動〉的「手腕抵額頭」一起改。 |
| 18 | s40 | 「his left wrist, wrapped in the wide dark gold sleeve with the hand hidden inside it, already hooked over Xu Yan's right forearm」：勾住要用到手，模型會讓手從袖口伸出來（紅的或正常膚色都斷戲）。 | 同上，共用設定第 482 行；script c40「手不露出來」 | 改成：「his left forearm, in the long wide dark gold sleeve whose cuff hangs well past his fingertips, already laid over Xu Yan's right forearm from the first frame, the long cuff folded over Xu Yan's sleeve, gold silk lying on blue-grey cloth」；動作：「Qian Yuanwai draws Xu Yan's forearm toward himself with his sleeve-covered forearm and leans in to his ear」。 |
| 18 | s39→s40 | 跳軸：s39 許硯在畫右、錢員外從畫左布簾進來走向他；s40 許硯在畫左、錢員外在畫右。第 19 集 c01 接 s40 的站位（許硯左、往畫左的布簾走），所以要改的是 s39。 | 軸線；第 19 集 r2 script c01；`r2-bible-e011-e060.md` 交接表 18→19 | s39 構圖改成：「medium-wide shot: a little left of the middle Xu Yan …, standing beside the near end of the long table, framed full length with clear space above his head, his face three-quarter to screen right toward the window, never the lens; guarded: brows drawn, eyes narrowed, lips closed; at the far left behind him Qian Yuanwai …, framed full length, already just inside the curtained doorway, the long grey curtain still swinging behind his shoulder, …」；動作：「Qian Yuanwai hurries in three short steps along the table behind Xu Yan, glancing back once at the curtain, and stops close to him on screen right of him, turning to face him; Xu Yan turns his head toward him」。這樣 s40 錢員外在畫右、許硯在畫左，接得上第 19 集。 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 18 | s03–s13 背影鏡 | 可選：給背影一張自己的參考圖。六支背影鏡只靠文字，第 16 集 fix 後一半種子仍有小走樣（s37 四個垂下小丸子）。 | `e916-live/picks-merged.tsv` s37 | 只在 s09（畫面只有她）先試：以 `angles/tangxiaotang-angle-b-l1.png` 為底做「只改一件事」編輯，提示詞只寫「the same young woman seen from directly behind, the back of her head and shoulders toward the camera」，產出 `tangxiaotang-back-l1`；s09 送它、寫「her hair and costume as in <Picture 1>, seen only from behind」。若冒分身就退回純文字。 |
| 18 | s01、s04、s05、s11、s12 | 帳房「plain dark blue cotton long gown」跟許硯「faded blue-grey scholar's robe」太像；s01、s11 兩人同框，「同一人出現兩次」的風險（第 15 集 s02 四隻手＝兩個許硯）。台詞本來就叫他「青衫先生」。 | 任務檔第 15 集教訓；script「青布長衫」 | `CLERK_BACK`、`CLERK_SLEEVE`、`MINOR` 外貌句的「plain dark blue cotton」改成「plain dark green cotton」（帳房的袖子、長衫全集一致）。 |
| 18 | s04、s05、s12、s31、s33 | 線裝帳冊常有一條白籤條、會長淡假字（第 14 集 s23）。 | `e914-live/picks-merged.tsv` s23 | `CLERK_LEDGER`、`TLEDGER` 改成「its cover one even plain dark blue cloth from edge to edge」。 |
| 18 | s11 | 中景畫左許硯、右後窗下帳房，但唐小棠坐在茶桌右邊、正好在兩人之間——提示詞沒有她，模型會讓她消失或畫出空位。 | 接戲；`set-chalou-l1` 的位置關係 | 兩個做法擇一：（a）拿掉帳房，改成許硯單人中近景、臉朝畫右的窗，帳房的「一僵」交給 s12 的手；（b）保留帳房，加「the young woman's shoulder and one high bun at the right edge of the frame, soft」並寫背影句。建議 (a)，比較乾淨。 |
| 18 | s07 | 許硯近景的背景：s02、s10、s14 寫「只有空白屏風」，s07 寫「只有木樓梯」，同一個近景機位背景跳。 | 接戲 | s07 改「behind him only the plain cream-white panels of the folding screen」。 |
| 18 | s01、s03、s06、s08、s13、s14 | 茶樓圖的低茶桌旁沒有任何椅凳，「sitting」每支會補出不同的坐具（s09 已經寫出 chair）。 | `set-chalou-l1` | 坐著的人一律寫「sitting on a low plain wooden stool at the left／right side of the low tea table」。 |
| 18 | s01、s11 | 「far behind them at the right, small and soft」：圖上長凳就在茶桌右邊一兩步，不是遠處。 | `set-chalou-l1` | 改成「a few steps behind her at the right, soft」（s11 改「a few steps away at the right, soft」）。 |
| 18 | s06 | 「taps one spot on its back once with her right forefinger」：單獨伸出的手指（第 16 集 s26 讀成比中指）；兩手舉紙又一手點，手不夠用。 | `e916-live/picks-merged.tsv` s26 | 改成「the young woman holds the sheet steady toward him with both hands and gives it one small shake」。 |
| 18 | s19 | 柴堆後兩個頭頂沒寫左右；s21 秦霜朝畫右看許硯、s22 許硯朝畫左看秦霜，所以應該是秦霜在左。 | 軸線 | `WOODPILE_TOPS` 改「one with a high ponytail on the left and one with a topknot on the right」。 |
| 18 | s15、s19、s21 | 「split firewood」一堆劈柴，旁邊最容易補一把斧頭（第 15 集農具畫成兵器）。 | `e915-live/picks-merged.tsv` s21；拍法 18 | `WORK` 的柴堆寫成「a low neat stack of short split logs, their cut ends pale, the stack and the bare stone floor around it」。 |
| 18 | s16、s25、s26 | 手部插鏡只送主人的半身定妝照（臉佔大半張），沒有寫畫框切在哪裡，模型可能往上帶出臉。 | 第 17 集 s20、s21 的寫法；拍法 10 | 構圖加一句：s16「the frame cuts the grey sleeve at the forearm at the left edge」，s25、s26「the frame cuts the two wide sleeves at the forearms at the bottom edge; above the hands only the dark open box and the stone paving」。 |
| 18 | s32 | 驚堂木先拍、再開口，a31 人聲 5.51 秒，加上拍案約 0.7 秒就超過 6 秒片段（(6−0.3)×1.1 = 6.27 秒）；s37b 同理已買 8 秒。 | r2.py BUY 註解（e013 的算法） | s32 改買 8 秒，或把拍案寫成第一秒內：「in the first second Magistrate Hu brings the wooden block down flat on the desk with one sharp knock, then speaks」。 |
| 18 | s35 | 「moves his open hand from the doorway at the left」：公堂圖上沒有門（r2.py 自己也寫了）；前景錢員外的背影寫「small black cap」，但錢員外定妝照戴的是**高的圓頂黑帽**，s34、s36 會照圖畫高帽，s35 的背影會不一樣。 | `qianyuanwai-portrait-l1`、`set-xianya-gongtang-l1` | 改成「Xu Yan moves his open hand from his side toward the man's joined sleeves」；前景寫「only the back of his tall rounded black cap, his thick neck and his right shoulder and wide sleeve」。順帶：`QIAN` 句寫「cross-collared robe … small black cap」，定妝照是圓領、高帽，全季跟著圖走，`QIAN` 句可改成「round-collared dark gold silk robe with roundel patterns and a tall rounded black cap」（跟胡縣令的有翅幞頭仍分得開）。 |
| 18 | s24 | 圖上的燈籠是白紙燈籠下掛紅流蘇；文字寫「blank faces」沒寫流蘇，模型可能另加紅色裝飾。另外圖左牆那排屋簷影子像人頭。 | `set-qianfu-houmen-ye-l1`；README | 燈籠寫「round white paper lanterns with blank faces and short red tassels」；可另做裁切 `crop=752:422:560:120,scale=1312:736`（裁掉大部分牆影，已試過，牆根仍留幾個齒影），用它取代整張。 |
| 18 | s22、s27 | 許硯說賣關子的話，「quiet and sure」容易在句尾笑（第 16 集 s10）。現在 s22 句尾有點頭、s27 有點頭，夠用。 | 拍法 18（不笑寫成動作） | s27 表情句加「lips pressed flat between words」，鞏固。 |
| 18 | a03（s02） | 處理後的系統句聽寫成「宿主甜甜合茶」（raw-tts 是「天天喝茶」）：1.3 倍加速與電子音把聲調抹平，「天天／甜甜」會改意思。 | faster-whisper 重聽（本審稿）；a01「剩五日」→「聖武日」同類 | 剪接前人耳聽一次；聽得出「甜甜」就把 a03 改用 1.15–1.2 倍處理（字幕照舊）。 |
| 18 | a34（s35） | 新錄的「錢員外」比第一次好（聽成「前院外」，只差聲調），但「人證」聽成「任正」；第一次錄的「人證就在衙門外」是對的。 | faster-whisper 重聽（現在的 a34：人聲 0.33–1.36「人證就在衙門外」、1.98 起「錢員外……」；take1 0.36–1.56 是「人證就在衙門外」） | 可接：take1 0–1.56 秒＋新錄 1.98 秒到結尾，中間留 0.5 秒（同一個 TTS 聲音），總長約 5.4 秒，s35 的 6 秒放得下。不接也可以接受。 |
| 18 | s05（帳房聲） | Puck 只在 r2.py 的 `MINOR`：video.json 已有（已核），製作沒問題；但 `cast.json` 的許大郎（第 41 集起）也是 Puck。 | `cast.json` 第 255 行 | 在 `r2-bible-e011-e060.md` 人物表加一行「錢府帳房 zhangfang（只有第 18 集 s05 一句畫外）：Puck，與許大郎同聲，第 41 集前不再用」。 |

## 參考圖

- **不用重畫任何一張**。要做三張**裁切衍生圖**（ffmpeg，免費、不換種子；前例：`set-biaoju-l1` 裁角、`set-gongpeng-l3` `crop=918:516:394:200`），放 `assets/refs-live/`、在 README 記來源與裁切參數，spec 用 `swap_pictures`（絕對路徑）換：
  - `set-chalou-bench-l1` = `set-chalou-l1` `crop=656:368:656:368,scale=1312:736`（s05、s12；s04 也可用）。
  - `set-xianya-gongtang-floor-l1` = `set-xianya-gongtang-l1` `crop=480:270:0:330,scale=1312:736`（s31、s33–s38）。放大 2.7 倍會偏軟，只當背景圖可以接受；
    若挑片覺得太軟，退路是以 `set-xianya-gongtang-l1` 為底的「只改一件事」編輯：「the long desk and the armchair on the platform are gone, the platform bare」。
  - `set-xianya-gongtang-dais-l1` = `set-xianya-gongtang-l1` `crop=650:366:330:250,scale=1312:736`（s32、s37b，匾在畫外）。
    退路同上：「the gilt-framed board above the white panels becomes one plain dark wooden beam」。
- s24 不做門板圖：門縫用剪接遮罩（必改 8）。可選裁切見建議 14。
- 唐小棠背影：可選「只改一件事」編輯（建議 1），先在 s09 一鏡試。
- 側廳 `set-xianya-ceting-l1` 照用：布簾在左、條桌兩椅、右窗，跟提示詞一致；右窗旁牆上有一小片反光圖案，近景 s40 身後「only the plain grey wall」不會帶到。

## 改完要重跑

`r2.py` → `build-r2.py` → `mkspec.py`（swap_pictures 加三張衍生圖）→ `prep918.sh`（DRY）→ 查每張圖絕對路徑、s05／s12／s31–s38／s37b 送的是衍生圖 →
`preflight-prompts.py` → 否定名詞掃描（應該連「wound」都沒有）→ 兩個種子提示詞逐位元相同。storyboard.md 與 script.md〈真人版的改動〉的 s37、s39、s24、s18 敘述跟著改。
