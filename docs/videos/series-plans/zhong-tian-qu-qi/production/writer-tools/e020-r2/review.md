# 第 20 集重製版（e020-r2，內部編號 920，真人版）分鏡與提示詞：開拍前獨立審稿

- 審稿：沒參與寫稿的獨立審稿代理，2026-11-16。只讀，只寫本檔；沒用 Colab、RunPod 或任何付費服務，沒有 git commit。
  試做的調色圖與聽寫只放在 scratchpad（`rv920/`），repo 的參考圖、錄音、spec 一個都沒動。
- 審的版本：`docs/videos/zhong-tian-qu-qi-e020-r2/{script.md, storyboard.md, video.json, overlays.json}`、`writer-tools/e020-r2/r2.py`、
  `colab/runs/e920/extras.json`、`colab/runs/e920-live/{mkspec.py, spec.json}`，以及實際要送的
  `/root/mokaair-work/videos/zhong-tian-qu-qi-e920-dh/runpod/live/d1/colab-jobs.json`（74 支）、`colab-jobs-wait.json`（4 支：s16、s37）與 `prompts/`；
  道具試鏡 `live-action/screen-test-e020.py` 與它的清單（Colab 上還在跑，`out/` 還沒有圖）。
- 機械檢查（本審稿自己跑）：
  - 78 支 = 39 鏡 × 9201101／9201102；兩個種子的提示詞、參考圖與秒數逐鏡相同；`prompt_sha256` 全部對得上提示詞檔。
  - 參考圖全是絕對路徑、檔案都在。會長四鏡（s19、s21、s22、s23）送的是 `hanghui-huizhang-portrait-l1`，提示詞是他自己的外貌句；
    `colab-jobs*.json` 裡沒有佔位圖 `mianshiguan`（`prep920.sh` 也有 assert）。只有中間檔 `retake.json` 還留著 8 次佔位圖（建議 13）。
  - 唐小棠十二支背影鏡都沒送她的圖；s37b 才送她三張。過肩前景（s20 會長、s35 孫掌櫃、s38 許硯）都沒送圖。
  - 否定詞掃描：只有允許的 never the lens／no second copy／no talking／no mouthing words／nothing tucked in it／nothing hanging from it／no subtitles，
    沒有被否定的物件名詞，也沒有本身會長字的名詞（letter、notice、sign 之類）。
  - `overlays.json` 兩個面板跟系統句一字不差。
- 錄音：`audio/zq920a01–a38.wav` 用 ffprobe 量長度、silencedetect（−40 dB）看人聲。faster-whisper medium（scratchpad 的 `fw` 環境）一次只跑一支、
  跑完就結束，餵 ffmpeg 轉的 16 kHz f32le numpy 陣列。重聽 a34（重錄版與 take1）、a24（後製版與 raw）、a27（後製版與 raw）、a37；
  另外用 voice-post.json 的濾鏡把 a24 raw 以 1.2 倍重做一次試聽（只在 scratchpad）。**注意 `fw920.txt` 記的 a08、a32、a34 是 take1 的結果，不是現在的檔。**
- 放大看過：`set-xuji-pu-l1` 全圖與門洞（4 倍）、`set-xuji-pu-floor-l1`、道具試鏡的底圖 `set-xuji-pu-l1-cabinet.png`、魏少卿、孫掌櫃、行會會長、
  小禾 l1 與 angle-a／b、唐小棠 l1 與 angle-a／b。
- 對照：`r2-bible-e011-e020.md` 拍法 1–18、道具表、接點 19→20 與 20→21；`season-01.md` 第 20 集與第 21 集；`e021-r2/script.md` c01；
  `writer-tools/e019-r2/review.md`；`colab/runs/e91{6,7,8}-live/picks-merged.tsv`；第 15–17 集 `extras.json`；第 19 集 s40、s41 實際送出的提示詞；
  任務檔第 13–17 集的教訓。

## 總評

做到的：唐小棠十句都背拍、她的圖與身分句都拿掉，頭都有寫固定；秦霜腰帶空著、沒有任何兵器字；紙一律「紙繩紮好、每面空白」；招牌不入鏡；
沒有手指指人；OFFSCREEN_SPEECH 關掉；s01 接第 19 集 s41 的站位與月光方向對；屋頂近鏡不送 3D 圖；長鏡秒數都放得下錄音；
會長的佔位換圖在實際清單裡是對的。

問題集中在五類：

1. **打烊那場的軸線翻了**：白天的鏡（s17、s19、s29、s33）都是「看向大門時櫃檯在畫右」（也就是圖上右牆前），s37b 唐小棠朝畫左看門；
   可是 s35–s38 把櫃檯放到看門時的畫左（s38 前景左是櫃檯角、魏少卿朝畫左看櫃檯），s37b 與 s38 兩人都朝畫左看，視線對不上。
   這是照第 21 集 CG 稿 c01（櫃檯左、魏少卿右）寫的，但跟本集的格局相反。
2. **`extras.json` 少了兩條沿用的替換**：小禾的外貌句還是「hugging a small woven straw rabbit」（s05、s25、s29 都要她兩手做事），
   二牛的還是「empty-handed」（s04 抓紅布、s29 與 s34 拿門板）。第 15、17 集的 extras 都有這兩條，本集漏了。
3. **會長的帳冊**寫成線裝帳冊加素藍布面：第 17 集 s31、第 18 集 s12 的線裝冊都長出題簽假字，本集四鏡近距離拿著。
4. **圖跟時段不合**：鋪子圖是正午般的硬白光條、門外藍天；s34–s38 寫黃昏轉藍。兩支插鏡的地磚圖也是白亮光條，s37 又寫「櫃檯邊緣」，圖上沒有櫃檯；
   道具圖做好後 mkspec 的句子寫「地點是灰石地」，可是道具圖的底是深色木櫃面。
5. **寫法的小錯會讓手、肩、表情出錯**：s05 兩手左右寫反、大娘「從街上進來卻只拍背」；s12 靠門柱的肩寫反；`quiet()` 的「the face set and still」
   跟反應鏡要的表情（s18、s22、s24、s32、s37b）打架；s10、s30 第一格的狀態跟動作互相矛盾；s38 摺扇那句接錯，讀成「右手裡什麼都沒有」。

錄音：**a27「宿主」連原始檔都聽成「數字」**（README 寫原始檔對，不對），要重錄；a24 後製後「許記」聽成「隨機」，用 1.2 倍重做就好；
a34 重錄版不給提示時聽成「燒門板」，要人耳確認。

**必改 17 條、建議 23 條。** 參考圖不用重畫；要做的都是**免費**的調色或裁切（下面〈參考圖〉）。付費的只有兩件可選、各「只改一件事」：鋪子圖加櫃檯、（挑片若 3D 感太重）鋪子圖改成實拍感。

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 改法 |
| --- | --- | --- |
| 櫃檯不在場景圖上，靠模型補 | **可以靠模型補，風險中等**。櫃檯多半出現在過肩鏡的前景，模型會自己放；真正的毛病不是「補不補得出來」，而是**本集自己把它放在兩邊**（s35–s38 跟白天相反，必改 4–7），以及每支長相可能不同（第 17 集燈籠骨架五種樣子）。 | 必改 4–7 統一站位。建議 1：櫃檯句寫得更具體、每鏡照抄。建議 2（可選、付費 2 支、可以搭正在跑的道具試鏡）：鋪子圖「只改一件事」加上櫃檯，存成 `set-xuji-pu-l2`。 |
| 唐小棠背影 12 鏡（轉頭、分身、丸子頭） | **拍法 3 要求，寫法對**：每鏡都有 TBACK、`only_tang`、HEADSTILL，大部分有「低頭看櫃檯上的東西」這種把頭定住的錨點。剩下三個風險：(1) 群眾裡的女子髮型沒寫，s06、s08、s14 最容易冒第二個丸子頭（第 15 集 s26、s41 的分身）；(2) s25 兩手高舉加原地一跳，最容易轉頭、丸子走樣（第 18 集 s03 變三四團髻）；(3) s37b 的定妝照是長緞帶加珍珠簪，背影鏡寫短緞帶、不寫珍珠，緊接 s32 會不一樣。 | 必改 12：群眾女子寫成低髻包頭巾。建議 7：s25 拿掉跳。建議 8：s14 可以改成沒有人的架子插鏡，背影少一鏡。建議 9：s37b 緞帶接受，挑片時看。 |
| s38 前景許硯背影沒送圖會不會變第二個人；魏少卿全景說話的嘴形 | **不送圖是對的**（拍法 2）。風險在文字：許硯寫「faded blue-grey」、魏少卿「sapphire-blue」，兩個藍色的男人，前景那個最容易被畫成魏少卿的分身或轉過臉。嘴形：全身全景、逆光，臉不到 40 像素，又是全集最後一句。另外摺扇那句接錯了。 | 必改 7：許硯寫成暗的剪影，只露肩與髮髻；景別改成膝上的中全景；摺扇句重寫。建議 4：櫃檯上放一盞點著的小陶油燈，照亮門口兩人的臉，也接第 21 集 c01 前景那盞油燈。 |
| 鋪子圖偏 3D、很亮；傍晚到黃昏要接第 21 集的暮色 | **亮度要處理，3D 感先接受**。第 16 集學到「場景圖的狀態壓過文字」：正午的白光條加門外藍天，s34–s38 的「最後一點夕照、門外轉藍」很可能被拍成白天。調色是免費的、不動格局。3D 感：第 1–19 集都送過 3D 場景圖，人物是真人就還行；挑片若整支像 CG，再做「只改一件事」的實拍感編輯。 | 必改 11：s34–s38、s37b 改送免費調色版 `set-xuji-pu-dusk-l1`。建議 3：s14–s24 送 `-pm-l1`、s25–s33 送 `-eve-l1`。建議 4：油燈。建議 23（可選付費）：實拍感編輯。 |
| 門外 s04、s11 不送圖，街景各支不同；s15 燈籠、s38 摺扇長假字 | **不送圖對**（菜市圖有假字）。但文字寫的街（灰瓦木店面、素面木板）跟鋪子圖門洞裡看得到的街（白牆深木框、灰瓦、大石板鋪的街）不一樣，s15 主觀鏡又送了那張圖，三支會是三種街。燈籠：小、在門洞間一段段晃過，風險低，寫成「像紅綢球一樣光滑」更穩。摺扇：「tiny gold dots」在扇面上最像一行小字。 | 建議 5：s04、s11、s15 的街照門洞裡的樣子寫成同一句。建議 6：燈籠句。必改 7：摺扇改成「幾片大金箔」。 |
| 行會會長用佔位 id 換圖沒驗證過 | **驗證過，實際清單是對的**：四鏡都送會長定妝照，提示詞是 extras 的會長外貌（八字鬍、山羊鬍、黑紗網巾、髮簪、灰圓領綢袍，跟定妝照一致），s20 的前景文字跟他對得上，`prep920.sh` 有 assert。只有中間檔 `retake.json` 還是佔位圖。 | 建議 13：重拍時一律重跑 `prep920.sh`（或 mkspec 的 swap），不要直接送 `retake.json`；送出前 `grep -c mianshiguan colab-jobs*.json` 要是 0。 |
| 小禾定妝照沒有草編兔子 | **照第 10、12、17 集的寫法「塞在腰帶上」就拍得出來**（第 10、12 集挑片都有兔子在腰上）。問題是本集 extras 漏了替換，三鏡的外貌句還寫「hugging」：抱著兔子就不能揮手、拍手、兩手拿掃帚。 | 必改 1。 |
| a34、a24、a27 錄音 | a34：重錄版不給提示聽成「二牛，燒門板」，給提示才是「上門板」；take1 是「上門吧」。**要人耳聽「上」**。a24：raw「徐季開張」（同音，對），1.3 倍後製後成「隨機開張」；我用同一濾鏡改 1.2 倍重做，聽成「許濟開張，首日壽慶」（同音，對），2.69 秒。a27：**raw 聽成「數字」、後製聽成「叔叔」**，是 TTS 本身把「宿主」念歪，不是後製。 | 必改 15–17。都不擋開拍（台詞長度只差零點幾秒，鏡頭都有餘裕），但要在剪接前做完。 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 20 | s04、s05、s11、s25、s29、s34（`extras.json`） | 1. 小禾的外貌句還是 `hugging a small woven straw rabbit`：s05 要揮手攤掌、s25 要拍手、s29 要兩手拿掃帚。<br>2. 二牛的外貌句尾是 `tied with a cloth sash, empty-handed`：s04 要抓紅布、s29 與 s34 要拿門板。<br>第 15、17 集的 extras 都有這兩條替換，本集漏了。 | 第 15、17 集 `extras.json`；第 10、12 集挑片（兔子塞腰上拍得出來）；拍法 10「手與道具寫在第一格」 | `extras.json` 的 `_replace` 加兩條：<br>`", hugging a small woven straw rabbit": ", a small woven straw rabbit tucked into the cloth sash at her waist"`<br>`"tied with a cloth sash, empty-handed": "tied with a cloth sash"`<br>重跑 `prep920.sh` 後 `grep -c "hugging\|empty-handed" prompts/*.txt` 要全是 0。 |
| 20 | s05 | 1. 小禾臉朝畫右（四分之三），她的**左手在畫右那側**、右手在畫左那側；稿子寫右手朝畫右的大娘揮、左手往畫左的架子引，兩隻手都要橫過身體。<br>2. 大娘「從街上走進來」卻「只拍背影」：大門在小禾身後，走進來的人是朝著鏡頭的。 | 拍法 9、10；第 19 集審稿必改 5、6（寫錯肩） | 構圖裡大娘那段換成：`her face three-quarter to screen right toward one plump middle-aged woman in a plain blue cotton jacket who has just stepped in through the doorway at the right edge of the frame, the woman's face soft and turned toward the shelves at screen left, never the lens`<br>動作換成：`Xiaohe rises on her tiptoes and waves her left hand, the hand on the screen-right side of her body, at the woman, then sweeps her open right hand, palm up, toward the shelves at screen left as she speaks; the woman turns toward the shelves`<br>storyboard 改成「踮腳揮左手，再攤開右手掌往畫左的架子一引」。 |
| 20 | s12 | 許硯在畫左、臉四分之三朝畫右：他的**右肩**才在畫左、靠著左邊門柱；寫「left shoulder against the left door post」照字面要背過身去。第一格已經靠著，動作又寫「leans back against the door post」。 | 拍法 9；第 19 集審稿必改 5；第 18 集審稿「第一格與動作自相矛盾」 | 構圖：`leaning his right shoulder, the one on the screen-left side of his body, against the left door post from the first frame`<br>動作：`Xu Yan brushes the dust off his left sleeve with his right hand, then tilts his head at her as he speaks`<br>storyboard「右肩靠著左邊門柱」。 |
| 20 | s34 | 軸線（見總評 1）：白天各鏡與 s33 都是「看向大門時，櫃檯在畫右」。s34 孫掌櫃在畫右、朝畫左看進店，看的是左牆的空架子，不是櫃檯前的許硯；接下來 s35–s38 照這個方向一路錯下去。 | 拍法 9；s17、s19、s29、s33 的站位；s37b 朝畫左看門 | 左右對調：`medium shot at the wide front doorway at dusk, the dark door post in the soft right foreground: on screen right, just inside the doorway, Wang Erniu …, lowering one long plain wooden shutter board … into the groove at the foot of the doorway with both hands; just outside the doorway on screen left Sun Zhanggui …, framed from the waist up, his left hand, the one on the screen-right side of his body nearest the board, in its wide green satin sleeve already resting flat on the top edge of the board from the first frame; his face three-quarter to screen right, looking past the big young man into the shop toward the counter beyond the right edge of the frame, never the lens`<br>mkspec 的 s34 視線句改成 `his face three-quarter to screen right, his eyes on the counter past the big young man`。 |
| 20 | s35 | 同一條軸線：孫掌櫃在門口，許硯在櫃檯前，所以許硯看孫掌櫃要朝**畫左**（s33 他朝畫左喊二牛，門在他畫左）；現在寫朝畫右，背景寫「櫃檯與空架子」，架子在對面的左牆。 | 同上；拍法 2 | `over-the-shoulder medium shot from close behind one tall thin man in a green satin robe seen only from behind, appearing only once, in the left foreground, only the back of his head with a topknot and his green satin shoulder showing, soft; facing us a little right of the middle Xu Yan …, standing in front of the long dark counter with both hands on its edge from the first frame, framed from the waist up with clear space above his head, his face three-quarter to screen left toward the man, never the lens; … behind him the plain white panelled wall in the dim dusk, soft`<br>動作的 `steps half a step toward the man` 不變。 |
| 20 | s36 | 反打要跟新的 s35 相反：孫掌櫃朝**畫右**看許硯；側身讓路也往另一邊，s38 他才站在左邊門柱。 | 同上 | 構圖：`his face three-quarter to screen right toward Xu Yan off screen right, never the lens`<br>動作：`Sun Zhanggui gives one slow nod and speaks; then he steps aside to screen left, out of the middle of the doorway, and holds his left hand open, palm up, toward the empty doorway`<br>mkspec 的 s36 視線句同改；storyboard「往畫左一側身、左手掌心朝上」。 |
| 20 | s38 | 1. 軸線：櫃檯角與許硯背影在左前景、魏少卿朝畫左看櫃檯；s37b 唐小棠也朝畫左看門，兩人視線同向、對不上。<br>2. 摺扇句接錯：`… flecked with tiny gold dots, nothing else on it in his right hand at his chest`，讀得成「右手裡什麼都沒有」；「tiny gold dots」在扇面上最像一行小字。<br>3. 前景許硯「faded blue-grey」跟魏少卿「sapphire-blue」都是藍衣男子，沒送圖的那個最容易變成魏少卿的分身或轉過臉。<br>4. 全身全景、逆光，說話的臉不到 40 像素；「small jade crown」而定妝照是髮髻前一塊綠玉。 | 拍法 1、2、7、9；第 19 集審稿必改 7（全景臉太小）；定妝照 | 構圖換成：`low-angle medium-wide shot from inside the shop, the dark corner of the long counter in the soft right foreground: in the soft right foreground one young man seen only from behind, appearing only once, standing in front of the counter, a dark silhouette against the glow of the doorway, only his dark shoulders and the back of his head with a plain cloth-tied topknot showing; beyond him the wide front doorway at the back: at the left door post Sun Zhanggui, in his green satin robe with a jade belt hook, standing aside, framed from the knees up, his face three-quarter to screen right, eyes half closed, lips closed; in the middle of the doorway Wei Shaoqing, in his sapphire-blue brocade robe woven with gold thread, a small green jade ornament at the front of his topknot, stepping over the threshold from the first frame, framed from the knees up with clear space above his head, holding open in his right hand at his chest one folding fan of plain cream paper with a few large flecks of gold leaf; his eyes passing over the young man's shoulder toward the counter beyond the right edge of the frame, never the lens; amused and arrogant: …`<br>mkspec 的 s38 視線句改成 `beyond the right edge of the frame`；storyboard「前景右許硯的暗背影、孫掌櫃在左邊門柱、魏少卿朝畫右外的櫃檯看」。<br>**第 21 集真人版 c01 要照這個方向寫**（CG 稿 c01 是櫃檯左、魏少卿右，相反）。 |
| 20 | s19–s23（`LEDGERS`） | 線裝帳冊加布面：第 17 集 s31、第 18 集 s12 的線裝冊都長出題簽與類字筆畫（後製模糊）。本集四鏡近距離抱著、夾著、按著；s19 還有一處接錯 `closed held against his chest`。 | 拍法 7、17；`e917-live`、`e918-live` 的 picks-merged（帳冊題簽） | `LEDGERS` 換成包袱：`one flat bundle of three books wrapped in one plain dark blue cotton cloth and tied with a cloth strip, the cloth smooth and even on every side`；各鏡寫 `holding the blue cloth bundle against his chest in both arms`（s19）、`the blue cloth bundle tucked under his left arm`（s21）、`his right palm pressed flat on the blue cloth bundle lying on the counter from the first frame`（s23）；s20 前景寫 `the edge of a blue cloth bundle under his arm`。storyboard「三本書用素藍布包成一包」。 |
| 20 | s02、s12、s18、s22、s24、s29、s32、s33、s34、s37b、s38（`quiet()`） | `quiet()` 句尾的 `the face set and still` 跟同鏡寫的反應打架：s02、s32「his eyes soften」、s18「A-ling's eyes search her」、s22「smile freezing … brows jumping」、s24「the corners of his mouth ease」、s37b「lips … trembling」。模型二選一，反應鏡最怕選到「不動」。 | 第 18 集審稿「頭偏一下又寫頭不動」；拍法 14 | `quiet()` 改成只管嘴：`f"{who} {verb} nothing in this shot: {pr} lips stay pressed together from the first frame to the last, no talking, no mouthing words"`（拿掉 `the face set and still`）。表情交給各鏡已經寫的眉、眼、嘴角。 |
| 20 | s16、s37（插鏡的圖與 `PROP_CLAUSE`） | 1. s37 第一格是「櫃檯邊緣的金算盤，下面是地」，送的卻是 `set-xuji-pu-floor-l1`：只有地磚、沒有木頭邊緣，又是正午的白亮光條，跟「dim dusk light」相反。<br>2. 道具圖做好後，mkspec 的 `PROP_CLAUSE` 寫 `the location is the grey stone floor of a shop`，但道具圖的底是左牆**深色木櫃面**（`crop=448:252:0:400`），圖文打架。<br>3. s16 寫 `warm afternoon light`，地磚圖是冷白光條。 | 第 15 集 s08「全景送給插鏡會硬切回全景」；第 16 集「場景圖的狀態壓過文字」；拍法 10 | **道具圖挑定前**：s37 改送免費的木櫃面裁切（道具試鏡已經裁好：`~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e020/set-xuji-pu-l1-cabinet.png`，深色木櫃邊緣、右下是地磚、光線本來就暗，存成 `refs-live/set-xuji-pu-cabinet-l1.png`）；s16 改送暖色調的地磚 `set-xuji-pu-floor-pm-l1`（見〈參考圖〉）。<br>**挑定後**：s37 只送道具圖，句子 `The small gold abacus shown in <Picture 1> is the one abacus in this shot, keeping exactly its shape, its thin gold frame, its rods and its rows of small round gold beads; it lies on the dark wooden counter top shown in <Picture 1>.`；s16 送道具圖加 `set-xuji-pu-floor-pm-l1` 兩張，句子 `… beads; the grey stone floor shown in <Picture 2> is the floor it falls onto.` |
| 20 | s34–s38、s37b（場景圖的光） | 鋪子圖是硬白的正午光條、門洞外藍天白牆；這六鏡寫「最後一點夕照、門外轉藍、屋簷燈籠點亮」。照第 16 集的教訓，圖的狀態會贏，結尾會拍成白天，接不上第 21 集的暮色。 | 第 16 集 s39「場景圖的狀態壓過文字」；拍法 8；接點 20→21 | 改送免費調色版 `set-xuji-pu-dusk-l1`（試做過，命令見〈參考圖〉；只動亮度與色溫、格局一點不變），用 swap_pictures 絕對路徑送。文字不變。門洞外的深藍交給文字與調色，不在圖上硬塗（試過遮罩塗藍，門扇邊變成一塊平藍、很假）。 |
| 20 | s06、s08、s14（群眾裡的女子） | 背影鏡對面的群眾女子沒寫髮型。第 15 集 s26、s41 唐小棠背影旁冒出第二個她；s08 十五個人、s06 有婦人、s14 兩個客人，任何一個梳兩顆髻就是分身。 | 拍法 3、13；`only_tang` 的由來（e915） | `CROWD` 的女子改成：`women in plain cotton cross-collared jackets and long skirts, their hair in one low knot at the nape under a plain cloth head wrap`；s06 的 `a woman in a blue cotton jacket`、s14 的 `two customers` 也各加 `her hair in one low knot under a plain cloth head wrap`。 |
| 20 | s10 | 第一格已經 `standing on the threshold`，動作又寫 `steps up onto the threshold`；第一格與動作矛盾，模型常讓人退下再上、或在原地抖。 | 第 18 集審稿「自相矛盾」；第 19 集審稿 s11 | 構圖改成：`standing one step inside the doorway, just behind the stone threshold, framed from the knees up …`；動作保留 `steps up onto the threshold and sweeps her right hand out flat, palm down, toward the street at screen left as she shouts`。 |
| 20 | s30 | `walking past the end of the long dark counter … and stopping there from the first frame`：又走又第一格已停。 | 同上 | 換成：`standing still at the end of the long dark counter from the first frame, one empty plain wooden bucket hanging by its rope handle from her right hand`；動作拿掉 `stops by the counter`，改成 `A-ling lowers her eyes once, then lifts them to her and speaks very quietly`。 |
| 20 | s26（a24 錄音） | `zq920a24.wav`（1.3 倍電子後製）聽成「隨機開張，首日受慶」：「許記」變「隨機」。raw 是「徐季開張」（同音，對）。 | README-retakes；本審稿聽寫；第 18 集 a03 的做法（改 1.2 倍） | 用 raw 以 1.2 倍、其餘濾鏡照 voice-post.json 重做：`ffmpeg -i zq920a24.raw-tts.wav -af "atempo=1.2,<voice-post.json 的 xitong filter>" zq920a24.wav`。我在 scratchpad 試過：2.69 秒，聽寫「許濟開張，首日壽慶」（同音）。舊檔放 `take1/`，README 記一行；人耳再聽一次。 |
| 20 | s27（a27 錄音） | 「宿主」**raw 就聽成「數字」**、後製聽成「叔叔」：是 TTS 把字念歪，不是後製。README 說「原始檔對」不對。只有把正確句子當提示時才聽得出「宿主」，那是提示帶的。 | 本審稿聽寫（不給提示，raw 與後製各一次） | 先人耳聽 raw 的「宿」。不對就重錄：送 TTS 的文字改用同音字 `嫌少？速主可以回去試試百分之零。`（只在 TTS 輸入；字幕、面板與稿子仍是「宿主」），錄完照季的 1.3 倍後製（或照 a24 用 1.2 倍），**不給提示**聽寫要讀出「宿主／速主／宿助」這類 sù zhǔ 的音。s27 的時間見建議 11。 |
| 20 | s33（a34 錄音） | 重錄版不給提示聽成「二牛，燒門板，今天打烊了」（「上」聽成「燒」，2.22–2.62 秒）；take1 是「上門吧」（「板」被吞）。兩版各錯一個字。 | 本審稿聽寫；README-retakes | 人耳聽重錄版 2.2–2.7 秒的「上」。若聽得出是 shàng 就留；聽不出就再錄一次，TTS 文字加停頓 `好，明天說。二牛，上……門板。今天打烊了。`，**不給提示**聽寫要讀出「上門板」。s33 買 6 秒、人聲 3.75 秒，長度差一點都放得下，不擋開拍。 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 20 | 全場（櫃檯句） | 櫃檯只寫 `one long plain dark wooden counter`：高度、檯面、正面都沒寫，二十多鏡各自補，長相可能每支不同。 | 第 17 集燈籠骨架五種樣子 | `SHOP` 與各鏡的櫃檯都照抄同一句：`one long waist-high counter of plain dark wood with a thick flat top and a plain panelled front, standing along the white panelled wall on the right`。 |
| 20 | 全場（可選、付費） | 櫃檯在圖上沒有。 | refs-live/README「只改一件事的編輯奏效」 | 搭正在跑的道具試鏡加兩支 Qwen：以 `set-xuji-pu-l1` 為底，提示詞只寫 `one long waist-high counter of plain dark wood with a thick flat top and a plain panelled front now stands along the white panelled wall on the right, from the big pillar toward us; everything else is unchanged`。挑定存 `set-xuji-pu-l2`，再照它做必改 11 與建議 3 的調色版。 |
| 20 | s14–s24、s25–s33 | 同必改 11 的理由，午後與傍晚也比圖暖、暗。 | 第 16 集教訓；第 19 集審稿建議 4（光跟圖打架會一支亮一支暗） | s14–s24 送 `set-xuji-pu-pm-l1`、s25–s33 送 `set-xuji-pu-eve-l1`（命令見〈參考圖〉）；早上 s05–s13 照原圖。 |
| 20 | s34–s38 | 黃昏逆光，門口兩人的臉最暗；第 21 集 CG 稿 c01 前景就是「櫃檯上的油燈」。 | 接點 20→21；e021-r2 c01 | s33 起櫃檯上加一盞：`one small clay oil lamp burning on the counter, its warm light on the faces near it`（s33 許硯喊打烊時點的，s35、s37b、s38 照抄同一句）。 |
| 20 | s04、s11、s15 | 文字的街（灰瓦木店面、素面木板）跟鋪子圖門洞裡的街（白牆、深色木框、灰瓦、大石板鋪的路）不同，s15 又送了那張圖。門洞右邊那棟有一扇拱形窗、右上角有幾條像電線的彎線。 | 放大看 `set-xuji-pu-l1` 門洞 4 倍 | `STREET` 與 s15 的對街改成同一句：`whitewashed shop fronts with dark wooden frames, square lattice windows and grey tiled roofs, the street paved with large grey stone slabs`；s15 加 `above the roofs only the pale sky`。 |
| 20 | s15 | 1. 燈籠可能長「福」字。2. 拍法 2 要寫明主觀鏡前景空著。3. s14 有兩個客人、s19 還有排隊的人，這鏡整間店全空。 | 拍法 2、7；s14、s19 | 燈籠：`two small round lanterns of smooth plain red silk, each as smooth as a red silk ball, a thin gold rim at top and bottom`；前景：`the near edge of the frame is the empty grey floor`；s19 的 `queuing townspeople` 改成 `two or three customers in the doorway`（午後人少），兩鏡就接得上。 |
| 20 | s25 | 兩手高舉加原地一跳，是背影鏡裡最容易轉頭、丸子走樣的動作（第 18 集 s03、第 17 集 s17）。 | 拍法 3；挑片紀錄 | 動作改成：`the young woman bounces once on her heels, her arms still raised and her head level, the back of her head toward us`。 |
| 20 | s14 | 十二支背影鏡裡，這支只是「看著架子撥算盤」，換成沒有人的鏡也說得通。 | 拍法 3（反應交給別的東西）；減少背影鏡的風險 | 可選：改成架子的插鏡（從 `set-xuji-pu-l1` 免費裁左牆架子 `crop=440:248:0:150`，寫三刀紙、一小排肥皂），她的錄音放在上面。不改也可以。 |
| 20 | s37b | 定妝照是長緞帶垂肩加珍珠簪；十二支背影寫短緞帶、不寫珍珠，s32 直接接 s37b。 | 第 19 集審稿建議（s38→s39 同樣的事） | 接受（第 16 集 fix1 的取捨）；挑片時選緞帶收在肩後、看不太到的那支。 |
| 20 | s07 | 阿令臉朝畫右，右手在畫左那側，要橫過身體把肥皂放進畫右的竹籃。 | 拍法 9 | `one pale cream bar of soap the size of a palm in her left hand, the hand nearest the woman`；動作同改左手。 |
| 20 | s27 | 三句檔長 3.00＋2.80＋4.60＝10.40 秒，比 10 秒長；人聲 2.42＋2.37＋3.94＝8.73 秒。剪接要把句首句尾的靜音削到約 0.3 秒，「不嫌」大約從 5.7 秒開始，提示詞寫「第七秒起」晚了一秒多。 | silencedetect −40 dB；r2.py BUY | 動作改成 `from the sixth second he lifts both palms a little in front of his chest, eyes wide, like a man taking it back`；剪接表註明 a26 從 0.41、a27 從 0.19、a28 從 0.24 起放。 |
| 20 | s36 | a37 前 2.0 秒是「哈哈哈哈」，人聲 2.10–6.90；提示詞是「點頭、說、再側身」，連笑一起放 8 秒片段放不下側身。 | 本審稿聽寫 | 剪接從 a37 的 1.95 秒起放（笑交給畫面上的笑咪咪）；提示詞不用改。若要留笑，就在動作前加 `for the first two seconds he chuckles softly, lips parted in a thin smile`，再把側身拿掉。 |
| 20 | s19、s21–s23（佔位圖） | 實際清單是對的，但 `retake.json` 還有 8 次 `mianshiguan-portrait-l1.png`。重拍時若從中間檔直接做清單，會送錯臉。 | 本審稿 grep | 重拍一律重跑 `prep920.sh`；送出前 `grep -c mianshiguan colab-jobs*.json` 必須是 0。 |
| 20 | s11 | 六個年輕人寫「plain hemp cross-collared short jackets, cloth head wraps」，跟二牛的褐色粗布短打幾乎一樣，最容易冒二牛的分身。 | 拍法 1；「同一人只出現一次」 | `six young men in dark blue-grey hemp cross-collared short jackets …`，加一句 `Wang Erniu is the only man in brown`。 |
| 20 | s33 | 阿令右手提桶，「手第一格已經在門上」沒說哪隻手。 | 拍法 10 | `her left hand already flat on the door from the first frame, the empty bucket in her right hand`。 |
| 20 | s34→s36 | 二牛在 s34 扶著門板站在門口，s36 孫掌櫃站在門口正中，二牛去哪了沒交代；第 21 集 c01 他又在門邊扶著門板。 | 接戲；e021-r2 c01 | s34 句尾加：`after the last word Wang Erniu steps back inside past the right edge of the frame, the board in his hands`；s38 可加 `one shutter board standing in the groove at the right side of the doorway`。 |
| 20 | s04 | 二牛站在凳上不移動，鏡頭卻寫 `tracking shot that follows the subject`；往前推軌時模型常往上搖，招牌就入鏡了。 | 拍法 7 | 改成 `Wide shot, slow push in`，構圖加 `the camera stays level, the top edge of the frame stays just below the eave`。 |
| 20 | s26、s27、s13、s37b | 近景送了 3D 的鋪子全景圖；背景本來就虛焦，送圖只帶進 3D 質感（第 19 集必改 15 的理由）。 | 第 19 集審稿必改 15 | 可選：這四鏡 `drop_set`，背景照現在的文字（`behind him only the bare shelves, soft`、`behind her only the plain white panelled wall in the dim dusk`）。s37b 若保留送圖，改送 `set-xuji-pu-dusk-l1`。 |
| 20 | s27 | 許硯這鏡是嫌少、不笑，但送了 angle-b（preflight 標記的帶笑角度圖）。 | preflight smile-ref；mkspec 已經對 s01–s03、s31–s35 這樣做 | mkspec 的 drop 清單加 `s27`。 |
| 20 | s16 | 第一格「從指間滑落、離地一手高」：她站在櫃檯後，手不會在離地一手高的地方。 | 拍法 10 | `the shot opens directly on the small gold abacus in mid-air, a forearm's length above the grey stone floor, falling, a small hand in a light peach-pink silk sleeve cuff open at the top edge of the frame where it slipped` |
| 20 | 道具句 `ABACUS` | 道具試鏡的提示詞是「五根細金桿、一道金橫樑、每桿上一下四顆珠」，`ABACUS` 寫「five rows of small round gold beads on thin gold rods」，沒有橫樑。 | `screen-test-e020.py` | 挑定道具圖後，照圖改成同一句，例如 `one small gold abacus the size of her palm: a thin flat gold frame, five thin gold rods, a thin gold crossbar, one small round gold bead above it and four below on every rod`。 |
| 20 | 唐小棠十句錄音 | 第 16 集學到唐小棠的錄音整集比片段原聲小約 3 dB；本集她十句全是錄音。 | 任務檔第 16 集 | 剪接時量同場響度，錄音句與原聲句對齊。 |
| 20 | 全場（可選、付費） | 鋪子圖是 3D 渲染。 | 第 19 集審稿〈可選付費〉 | 挑片若整支看起來像 CG，再以 `set-xuji-pu-l1`（或 l2）為底做一次「只改一件事」：`make it a real photograph of an old wooden shop interior, same layout, same light`。 |

## 參考圖：要做什麼

- **免費調色**（只動亮度與色溫、格局不變；試做在 scratchpad `rv920/`，放大看過，接受；做好放進 `refs-live/`，在 `README.md` 記一行，spec 用 `swap_pictures` 絕對路徑送）：
  - `set-xuji-pu-pm-l1` = `ffmpeg -i set-xuji-pu-l1.png -vf "eq=contrast=0.9:gamma=0.85,colorbalance=rs=0.06:bs=-0.06:rm=0.08:bm=-0.08:rh=0.06:bh=-0.10"`（s14–s24）
  - `set-xuji-pu-eve-l1` = `… -vf "eq=contrast=0.85:gamma=0.72:saturation=1.1,colorbalance=rs=0.10:bs=-0.12:rm=0.15:gm=0.03:bm=-0.15:rh=0.12:bh=-0.20"`（s25–s33）
  - `set-xuji-pu-dusk-l1` = `… -vf "eq=contrast=0.8:gamma=0.55:saturation=1.05,colorbalance=rs=0.10:bs=-0.05:rm=0.14:gm=0.02:bm=-0.10:rh=0.10:bh=-0.05"`（s34–s38、s37b；**必改 11**）
  - `set-xuji-pu-floor-pm-l1` = `ffmpeg -i set-xuji-pu-floor-l1.png -vf "eq=contrast=0.85:gamma=0.85,colorbalance=rs=0.08:bs=-0.08:rm=0.1:bm=-0.1:rh=0.08:bh=-0.14"`（s16；**必改 10**）
- **免費裁切，已經存在**：道具試鏡裁好的木櫃面 `~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e020/set-xuji-pu-l1-cabinet.png`
  （`set-xuji-pu-l1` `crop=448:252:0:400`，深色木櫃邊、右下地磚、暗），照抄成 `refs-live/set-xuji-pu-cabinet-l1.png` 給 s37（**必改 10**）。
- **不用重畫**：魏少卿（綠玉在髮髻前，文字照圖寫，必改 7）、孫掌櫃、行會會長（八字鬍與山羊鬍、網巾、髮簪，文字對得上）、小禾（兔子靠「塞在腰帶」文字，必改 1）、唐小棠。
- **可選、付費、只改一件事**：鋪子圖加櫃檯（建議 2）；鋪子圖改實拍感（建議 23）。道具圖 `prop-jinsuanpan-l1` 照現在的試鏡做，挑定後照必改 10 送。
- **門洞那塊**：放大 4 倍看，街上沒有字；右邊一扇拱窗、右上幾條彎線，靠建議 5 的文字蓋過去，不塗。

## 最重要的五條

1. **打烊那場的軸線（必改 4–7）**：s34–s36、s38 左右對調，櫃檯與許硯一律在看門時的畫右，魏少卿朝畫右外看櫃檯，跟 s37b 唐小棠朝畫左看門對得上；第 21 集真人版 c01 照這個方向寫。
2. **`extras.json` 補回兩條替換（必改 1）**：小禾的兔子塞在腰帶、二牛拿掉「empty-handed」；不然 s05、s25、s29 小禾抱著兔子，s04、s29、s34 二牛手上的東西會掉。
3. **s38 最後一鏡（必改 7）**：摺扇句重寫成「右手拿著一把素米色紙、幾片大金箔的摺扇」，前景許硯寫成暗剪影，魏少卿改膝上中全景、綠玉照圖。
4. **會長的帳冊改成藍布包袱（必改 8）**：線裝冊的題簽兩集都長出假字。
5. **圖跟時段（必改 10、11）**：s34–s38 送免費調色的黃昏版鋪子圖；s37 送木櫃面裁切、s16 送暖色地磚，道具圖做好後的句子照圖寫（木櫃面，不是灰石地）。

開拍前一定要先做的：必改 1–14（都是改字或免費做圖）。錄音的必改 15–17 不擋開拍，剪接前做完；其中 **a27 要重錄**。
