# 第 36 集重製版 r2（e036-r2，內部 936）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿：沒參與寫稿的獨立代理，2026-11-20，開拍前（d1 還沒跑；錄音只有 3／35 句）。只寫這一個檔；沒改 `r2.py` 或別的檔、沒開 Colab／RunPod（沒碰 `zt-live2`、`zt-live3`）、
  沒用站台 TTS、沒付費圖、沒 commit。沒讀前置代理的自審 `writer-tools/e036-r2/review.md` 與 scratchpad 的 `e936prep/PROGRESS.md`。
- 審的對象：`writer-tools/e036-r2/r2.py`、`docs/videos/zhong-tian-qu-qi-e036-r2/{script.md,storyboard.md,video.json,overlays.json}`、
  d1 提示詞 `~/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/runpod/live/d1/prompts/*.txt`（80 支）與 `colab-jobs.json`、`colab/runs/e936-live/{mkspec.py,PREP.md}`、
  `colab/runs/e936/extras.json`、`hailuo/clips-dh-e936.json`、`live-action/free-e031-e040/{shanjiao_qu.sh,xujia_yuan_ye_e936.sh,cunkou_zha2_e936.sh,cunkou_zha2_crops.sh}`。
- 對照：`r2-bible-e031-e040.md`（拍法、〈接點〉35→36、36→37、〈道具〉〈小角色〉〈場景〉）、任務檔 2026-11-20 的教訓、第 35 集 `review-independent.md`、
  `colab/runs/e935-live/{fix1,fix3,fix4}/plan.md`、`final-check.md`，第 35 集 `video.json` 的 s26–s35。
- 參考圖全尺寸打開看過：`set-cunkou-zha2-l1`、`-men`、`-wai`、`-ding`、`-dao`、`-kong`、`-zha`、`-di`；`set-shanjiao-qu-l1`、`-zhuo`、`-an`、`-di`、`-tian`、`-xi`、`-xi-an`；
  `set-xujia-yuan-ye-dong2-l1`、`-qiang`、`-chai`、`-shan`、`-wu`、`-zhong`。在 scratchpad `e936rev/` 自己抽了第 35 集成片最後 15 秒（`tail/sheet.jpg`、`t01–t15.jpg`），
  也試裁了兩張不帶關門的村口圖（`try-ding2.png`、`try-wai2.png`，必改 3）。
- 語速：錄到的 3 句加上第 30–35 集**已錄**的人聲長度（各集 `audio/span93N.txt`、scratchpad `tools/span935.txt`），照角色算字／秒（本審稿寫的 scratchpad `e936prep/rates.py`），見必改 9 與〈小結〉。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| 台詞 | `video.json` 35 句逐字在 `script.md` 裡；40 鏡＝c01–c38 加 s11b、s12b；`overlays.json` 只有 s29「以工代賑，達成」，跟系統念的一字不差 |
| d1 清單 | 80 支，每種子 258 秒（5 秒 4、6 秒 27、8 秒 7、10 秒 2），跟 `r2.py` 的 `BUY` 與 `colab-jobs.json` 逐鏡相符 |
| 唐小棠的名字與圖 | 80 支提示詞、`colab-jobs.json` 的送圖都沒有 `Tang Xiaotang`、沒有她的三張圖；沒有 `stand-up collar`、`apricot`；`gold abacus` 只在 s05 插鏡 |
| 精修文字 | `clips-dh-e936.json` 40 筆沒有她的名字、沒有立領句；背影鏡寫 `the young woman seen only from behind`；留著通用說話視線的 s06 s08 s09 s12 s12b s13 s20 s21 s25 s30，聽的人都在畫裡，可以 |
| 送圖 | 許硯、阿令、秦霜、錢員外都沒送 angle-b；s01 s02 s09 s13 s29 只送許硯 l1；s28 錢員外背影不送圖不點名；插鏡 s05 s15 s17 s22 s23 與 s14 s27 s32 s36 不送人 |
| 會長字、會畫錯的字 | 0 個 `pool`、`pond`、`mud`、` open`、`crowd`、`villager`、`hundreds`、`cinema camera`、`stubble`、`shrewd`、兵器字、`ink`／`stroke`／`register`、`candle`、`lantern`、`smoke`、`fog`（`ink`／`writ` 的命中都是 `pink`、`written`） |
| clear-and-still 替換 | s01 s02 火把句、s03–s12b 晚風、s13 塵土、s31–s38 夜氣與油燈；s05 與 s14–s30 照舊（白天乾地、傍晚，跟畫面不打架，接受） |
| 人數 | s01 五、s02 十一（八個流民含被牽著的小男孩＋守門兩人＋許硯）、s09 八、s13 九、s29 七、s30 五、s31 十、s32 兩個睡著的人：`exactly N` 都跟描述對得上；有名字的臉每鏡最多兩張 |
| 火把 | s02：流民四支＋守門兩人各一支＝六支（拍法 37）；**誰拿沒寫**，見必改 2 |
| 笑 | 寫了冷笑的只有 s10；s20 寫「a faint easy look in his eyes」不寫笑字；其他有臉的鏡都寫了表情與 `not smiling` |

## 寫稿者的決定：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| 接點 35→36 | 成片 218.93 秒（15:24 版）最後 15 秒：s33 阿令正面（**頭髮是半披，長髮垂到腰**）→ s34 從背後朝**關著**的木門：阿令在許硯左、唐小棠在右略後（桃粉短衫、粉裙、兩顆丸子垂粉緞帶）、**暗青短打在左端、深酒紅在右端**；s34 開頭兩人各拿一支火把，**到 s34 最後一格手是空的**（火光變成柵外兩座火盆與右邊石燈籠）→ s35 右手按門縫鐵件旁的橫木到片尾。**s01 接得上**：同一個背後機位、同站位、門關著、許硯兩手在門閂上；中間隔 s35 插鏡，守門人手上的火把照 s34 開頭寫可以接受。兩個小落差（守門人左右沒寫、阿令頭髮）見建議 1 | 建議 1 |
| 接點 36→37 | s38 鏡頭朝後牆、院門在背景中間，許硯在畫左三分之一、唐小棠在他右邊抓右袖、阿令在左邊屋門（s37）、秦霜在後牆右段牆頭（s33／s35）：給第 37 集「二牛從後牆中間的院門撞進來、朝鏡頭跑」**接得上**。只是 `-ye-dong2` 圖上**院門本來就半開**（門扇往內靠），第 37 集要「撞進來」得先處理（建議 12） | 建議 12 |
| 柵門 s01 | 結果寫兩次（構圖 `closed from the first frame to the last`、動作 `while the two gate leaves stay closed`），送 `-men`（關著），圖文一致，合理 | 接受 |
| 柵門 s02 | **圖文打架**：送的 `-men` 是關著的門扇佔畫面六成，文字寫已推開到底、人穿過門口朝鏡頭走來。模型只能二選一：照圖門關著、八個人擠在門前（＝門內，或像沒開門）；或照字在片中把門拉開（第 35 集 fix1 s34、fix3 s32 就是這樣自己動門）。而且 `-men` 的視角斜看門扇正面，看不穿門口 | 必改 1 |
| s02 之後還有關著的門嗎 | **有**。r2.py 寫「s02 之後不送門扇關著的圖」，但 **`-ding`（s03、s04、s10）**下半是關著的兩扇門扇、橫木與門縫鐵件（錢員外腰以上只蓋住中間）；**`-wai`（s06、s07、s09、s12b）**左緣一成是關著的右門扇板子、橫木與斜撐 | 必改 3 |
| 唐小棠（拍法 3、4、20、40） | 五個說話鏡從背後、正中、`HEADSTILL`，四鏡只動腿或手臂，寫法擋得住轉頭；**s18 例外**：第一格就「上身往桌左端傾」、又在看阿令的紙說「這字……」，最容易轉成左側臉 | 必改 4 |
| 唐小棠的金算盤插鏡 s05、畫外 s16 | 合理：拍法 20 本來就要金算盤只在插鏡；s16 她在畫外帳桌右端叫人，聽的是阿令，畫面給阿令。不寫淡杏外衣、高立領：80 支都沒有 | 接受 |
| 錢員外 | s03、s04 低角度正面喊、逐部位寫不笑（第 35 集 s31 喊的鏡過關），錄到的 a02、a03 都在 8 秒內；s10 冷笑（稿子准）；s27 他不入鏡、s28 背影＋錄音（第 34、35 集 fix4 的解法）。**合理**。風險最大的是 s26：正面、10 秒長、又急又不信——第 34 集 s30、第 35 集 s23 都是這種長的正面笑場（建議 10） | 建議 10 |
| 軸線：村口 | s03／s04／s10 錢員外朝右下、s06／s07／s12b 許硯在左朝右、s08／s09／s11 朝左（流民與門口）：接得上。s09 送 `-wai` 的問題見建議 3 | 建議 3 |
| 軸線：新渠 | 渠往深處、帳桌在左岸、秦霜與許硯在右岸：s21／s24／s25 一左一右接得上；s26 錢員外從右來朝左下、s27 唐小棠背影、s28 背影走遠，接得上。帳桌兩人其實**坐在桌子兩側**（唐小棠背對鏡頭在近側、阿令在遠側面向鏡頭），s16 與 s19 阿令臉的方向左右相反、s19 背景不對（建議 5） | 建議 5 |
| 軸線：夜院子（拍法 42） | 屋與柴堆在左、院門在後牆中間、後牆右段、井在前右，s31→s33→s34→s35→s37→s38 方向一致；**s35 回頭的肩膀寫反** | 必改 5 |
| (1) 兩個拆鏡 s11b、s12b | 合理。s11 心裡話 18 字＋系統 9 字已約 7.4–9.1 秒，第三句放不進 10 秒；s12 兩人各說一句，拆成兩鏡各一個動作 | 接受 |
| (2) c05 改金算盤插鏡 | 合理（拍法 20）；`set-cunkou-zha2-di-l1` 是 5 倍放大的土路，只當插鏡的地面，夠用 | 接受 |
| (3) 名冊空白、筆尖不落、帳冊不寫 | 不落筆、不寫帳冊合理（拍法 7、27、38）。但 s17 是**對焦清楚的空白紙**特寫，下一鏡唐小棠說「這字工整得像宮裡的帖子」，觀眾看到的是一張白紙（原版建議要的是「虛焦、看得出端正」） | 建議 4 |
| (4) 柴刀、短刀不寫 | 合理（拍法 5、22）；手按、勒緊寬皮帶，手縮進袖子，讀得出 | 接受 |
| (5) 夜院子改格局、秦霜第一格在牆頭背對 | 合理：井不在牆下，蹬井沿翻牆在這張圖上拍不出；s31 走向牆、s33 已在牆頭，剪接讀得出翻上去 | 接受 |
| (6) `POOLMARK` | 合理：d1 已拿乾淨（0 個 `pool`）；PREP §6 已寫明 fix／retake 都要帶 `[R2.POOLMARK, ""]`，照做 | 接受 |
| (7) 12 張免費圖 | `-tian`、`-an`、`-di`（渠）、`-qiang`、`-chai`、`-wu`、`-zhong` 取景給得出各鏡要的東西。**問題**：`-zhuo` 中景有一道**白色護欄**（現代公路欄杆）與分層擋土坡，送 7 鏡（必改 7）；**`-xi` 不像傍晚斜陽**：天頂偏青綠、整張是橄欖褐濾鏡、看不到太陽，影子跟白天那張一樣短（建議 7）；`-shan` 左三分之一是樹幹與院門瓦頂，文字寫只有牆頭、田、山，而且 640×270 拉成 1312×736 是**垂直拉長 1.33 倍**（建議 8）；`-xi-an` 是俯看的土堆，s30 要的「遠處三個背影」沒有地平線可以站（建議 9）；渠中段那塊**直立木板**是會長字的平板（建議 6） | 必改 7、建議 6–9 |
| (8) 唐小棠本集沒有正臉 | 合理：稿子沒有她不說話的反應鏡；c18「看呆了」交給語氣 | 接受 |
| 新渠的圖跟文字 | **渠的深度寫錯**：`CHANNEL` 寫「about a man's depth」，圖上渠底只比兩岸低半人不到（右岸土埂約膝高），s13 又要渠底的許硯全身入框 | 必改 6 |
| 草蓆 | `SLEEPERS` 寫十二張「頭尾相接」沿後牆排、人臉朝牆睡＝順著牆躺，一張約一人長，十二張要二十幾公尺；圖上院門到右牆角那段牆只有十公尺上下、右前方還有井。s32 的「三張空蓆」近景若也順著牆排，三張就五公尺寬，近景框不下，鉤子會變成一兩張 | 必改 8 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 36 | s02（鉤子：開門） | **送的圖門關著、文字寫門已推開到底**（逐一判斷）。另外 `one against the log fence at the left` 也不成立：籬笆跟門扇在同一條線上，往內開的門扇只會轉到跟籬笆垂直 | 拍法 29（圖說了算）；第 35 集 fix1 s34、fix3 s32（H3 自己動門）；第 33–35 集通則：參考圖要跟文字一致 | **免費**：`cunkou_zha2_e936.sh` 加 `c set-cunkou-zha2-wai2-l1 680:383:440:222`（我在 scratchpad 試裁過 `e936rev/try-wai2.png`：左上角只剩一角瓦簷、左緣一根斜靠的圓木（可當靠在門柱邊的門閂）、垂柳、石溝與木板橋、土路、右邊兩間屋與短籬笆，**沒有門扇**），新 id，`PLACE` 把 s02 改送它。構圖改成：`wide shot at standing eye height just inside the gateway, the gateway itself just beyond the left edge of the frame, the thick crossbar leaning upright at the left edge: coming in from the left edge one after another along the dirt road past the willow, {REF8} …; one at the left edge, {GUARDS 之一} …`（守門兩人改成一人在左緣、一人在畫外，或兩人都在左緣前景背影），`exactly` 照改；剪接照舊從人已走進來開始。要看到門扇推開就要付費改圖（建議 2） |
| 36 | s02 | **六支火把沒寫誰拿**：`four of the walking people each hold up one burning pine torch` 讓模型自己挑；最可能落到排頭的老人手上，而老人是要「兩手合抱作揖」的那個人；牽小男孩的婦人、彎腰的老婦也空不出手 | 拍法 37（每支火把在一個寫明的人手上）；`HANDS` 句 | `TORCHES4` 改成點名：`the lean middle-aged man in charcoal, the stocky man in olive-green, the thin young man in ochre and the boy in mustard-yellow each hold up one burning pine torch in one hand at walking height; the old man in front and the young woman holding the boy's hand carry no torch`（後半是否定句，若掃描擋就改成 `the old man's two hands are empty and free`、`the young woman's other hand holds her bundle strap`） |
| 36 | s03、s04、s10（`-ding`）；s06、s07、s09、s12b（`-wai`） | **s02 之後又出現關著的門**（逐一判斷）。`-ding` 下半是關著的門扇、齊腰橫木與門縫鐵件；`-wai` 左緣是關著的右門扇與斜撐 | r2.py 自己定的規則（s02 之後不送門扇關著的圖）；拍法 29；第 35 集 fix1 s34 | **免費兩張新裁切**（試裁在 `e936rev/try-ding2.png`、`try-wai2.png`）：`c set-cunkou-zha2-ding2-l1 448:252:60:12`（只有瓦頂與橘紅天、下緣一點梁木，沒有門扇）給 s03 s04 s10；`set-cunkou-zha2-wai2-l1`（必改 1）給 s06 s07 s09 s12b。文字跟著改：`GATE_BACK` 的 `the right post of the gate at the left edge` → `the corner of the gate's small tiled roof at the top left and a leaning log at the left edge`；s03 s04 s10 的 `behind him, soft, the small tiled roof of the gate` 不變（圖上就是瓦頂） |
| 36 | s18 | **唐小棠會轉頭**：`her upper body already leaning a little toward the left end of the table from the first frame`，她在看阿令的紙說「這字……」，身體往左傾＋看左邊的東西，模型最常做的是把頭轉成左側臉（第 31、33 集的臉頰露出就是這樣來的） | 拍法 40（正背對、頭不動）；第 33–35 集通則 | 拿掉傾身：`her shoulders square to the table, facing straight away from us like the rest of her, her right hand resting on {ABACUS} before her`；動作只留 `her right hand stops still on the beads of the abacus, only her arm moving`。阿令在左三分之一照舊 |
| 36 | s35（與 `GAZE_REFINE["s35"]`） | **回頭的肩膀寫反**：秦霜蹲在後牆右段牆頭、背對院子面向牆外的山，許硯在她左下（院子中間）。背對鏡頭時她的右肩在畫右，`turned back over her right shoulder, looking down toward … the lower left` 要把頭往右後轉再看左下，做不出來，模型會挑一邊（多半往右看畫外空處或直接回頭看鏡頭） | 拍法 31（視線方向要做得出來）；軸線 | 構圖與 `GAZE_REFINE["s35"]` 的 `over her right shoulder` → `over her left shoulder`；動作 `speaks down over her shoulder` → `speaks down over her left shoulder` |
| 36 | `CHANNEL`（s13、s29） | **渠的深度跟圖不一樣**：`about a man's depth`；圖上渠底只比兩岸低一截，右岸土埂約膝高。一人深的渠，s13 渠底四個人會只露上半身或模型把渠挖深、跟圖不像；s29 許硯「站在木板上」也會變成架在深溝上 | 拍法 29；第 34、35 集必改（位置照圖） | `a freshly dug dry channel about a man's depth` → `a freshly dug dry channel about knee-deep, wide and flat-bottomed`；script.md 的「渠溝約一人深」可以不改（給人讀的），但 `r2.py` 照圖 |
| 36 | `set-shanjiao-qu-zhuo-l1`（s14 s16 s18 s20 s26 s27 s28） | **背景有一道白色的現代護欄**（中景橫過整張，連同分層的擋土坡），s28 是朝松樹走遠的中遠景、護欄在正中；H3 會照畫成公路欄杆。不能用文字否定（拍法 18） | 拍法 18、29；第 35 集 `hantian_yang_clean.py` 的做法（地平線小竿塗掉） | **免費**：照 `hantian_yang_clean.py` 寫 `shanjiao_qu_clean.py`，在 `set-shanjiao-qu-l1` 上把護欄那一帶（約 y 320–345、x 0–560）用上下的坡土與乾黃地補掉，存新 id 再重裁 `-zhuo`（`-xi` 一族同樣從乾淨版調色）；README 記一行 |
| 36 | `SLEEPERS`（s31）、s32（鉤子：三張空蓆） | **十二張頭尾相接放不下**（逐一判斷），三張空蓆的近景也框不下 | 拍法 29；鉤子要讀得出（原版：三張空蓆） | `SLEEPERS`：`a row of twelve straw mats laid side by side along the foot of the back wall from just right of the bare tree to the right corner, running behind the well, their heads to the wall, nine men in ragged homespun curled asleep on them under ragged blankets with their backs to us, the three mats in the middle of the row empty`；s32：`three empty straw mats lying side by side, their heads against the foot of the low earth-and-stone wall`，左右緣兩個睡著的人照舊 |
| 36 | s30（BUY） | **最可能放不下的一句在畫面上說**：秦霜「渠通了，那三個人還沒走。今晚我守院子。」16 字、兩句兩個停頓，本鏡她還要看一眼遠處、兩手勒皮帶。秦霜（Autonoe）第 30–34 集實測 22 句：中位 **3.7 字／秒**、慢的句子 2.3–2.9（`span930`–`span934`）→ 本句 **4.3–6.2 秒**，6 秒片段放得下約 5.9 秒；而她在畫面上說，不能像畫外錄音那樣靠慢放救 | 聖經〈每集鏡數〉（6 秒放 5.9 秒、8 秒放 7.3 秒）；拍法 43 | `BUY` 加 `"s30": 8`（兩種子多 4 秒，約 0.2 CU）。不改的話錄音後超過 5.9 秒只能剪停頓 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 36 | s01 | 第 35 集成片 s34：**暗青短打在左端、深酒紅在右端**；阿令頭頂插簪、**長髮披在背後垂到腰**。`GUARDS` 沒寫左右，`ALING_TIED` 寫 `pinned up`，背影鏡可能變成盤髮 | 接點同一刻（〈接點〉35→36 第 35 集成片實拍） | s01 構圖寫 `the broad young man in dark teal at the left end, the wiry man in deep wine-red at the right end`；阿令那句後加 `the long rest of her black hair hanging straight down her back to the waist` |
| 36 | s02 起 | 必改 1、3 是免費的繞法：s02 看不到門扇推開，開門靠 s01 抬門閂＋s02 人已走進來。要讓鉤子「門開了」真的被看見 | 拍法 19、29 | **付費**：Qwen 只改一件事「the two gate leaves swung wide open inward, standing at right angles to the fence, the gateway open onto the dirt road outside」，新 id `set-cunkou-zha2-kai-l1` 再免費重裁，約 **1.5–2 CU**（上限約 4）；s02、s06、s07、s09、s12b 改送它。第 37 集以後若不再回村口，免費版就夠 |
| 36 | s09 | 送 `-wai`：那塊垂柳、石溝、木板橋前的空地，就是第 35 集 s29 流民**在門外**跪著的地方（同一張圖、同一個角度）。許硯站上那裡的石頭，等於站到門外，跟 s08「門內」不合 | 接戲（第 35 集 s29 用 `-wai` 當門外） | 改送 `-dao`（同 s08 的三間屋與遠山），`behind, soft, the willow, the plank bridge …` → `behind, soft, the three small earthen-walled houses and the far hills`；或接受（門開了以後那塊地算門口） |
| 36 | s17 | 對焦清楚的空白紙特寫，下一鏡唐小棠讚字工整：看起來像白紙一張 | 原版建議（名冊虛焦、看得出端正）；拍法 38 | 紙改成虛焦：`a short stack of plain white paper soft and out of focus at the lower part of the frame, lit warmly from the side`，**對焦在阿令的指尖與筆尖**；或照稿子〈刪鏡〉的原則拿掉 s17（沒台詞、不推劇情），s16 直接接 s18 |
| 36 | s16、s19 | 阿令坐在桌的遠側面向鏡頭：s16 臉朝**畫右**看紙、s19 朝**畫左**（`GAZE_REFINE["s19"]` 同），相鄰兩鏡同一人看同一張紙方向相反；s19 背景送 `-an`（渠邊土堆），但從近側往她拍，土堆在她前面、她身後是乾黃地與松樹 | 接戲；拍法 29 | s19 的臉與 `GAZE_REFINE` 改 `three-quarter to screen right toward the blank paper below the frame`；背景改送 `-zhuo`、`behind her, soft, only the flat dry yellow field and the line of dark pines` |
| 36 | 新渠（s13、s21、s29） | 渠中段那塊**直立的木板**（架著橫板）是一面平的板子，第 35 集 fix1 s30 柵門橫梁上的木牌就長出兩個像字的記號，1–9 秒都在 | 拍法 33（立著的板子會長字）；第 35 集 fix1 | 免費：必改 7 的清理一起把直立板改成一根細木樁（同遮罩做法）；不改就看 d1，s13、s29 長字再修 |
| 36 | s29（`-xi`） | 讀起來是橄欖褐的復古濾鏡，天頂青綠、看不到太陽，影子跟白天一樣短，跟文字 `low warm orange sunlight from the right, long shadows stretching to the left` 對不上，又跟第 35 集 `-zong` 同一個毛病 | 第 35 集獨立審稿逐一判斷 (7)、建議 3 | 免費重調：`colorbalance` 的 `gh`／`gm` 降到 0、`bh` 降更多、天空上半加一層橘粉漸層（`geq` 或 `gradients` 疊 screen）、亮部再暖一點，新 id；或文字照圖改成 `warm amber evening light, the sky hazy`（不寫長影子） |
| 36 | s36（`-shan`） | 左三分之一是光禿樹幹與院門瓦頂，文字寫 `only the wall top, the fields, the hills and the small far flames`；640×270 拉成 16:9，山與田**垂直拉長 1.33 倍**（第 35 集的 `-dao` 也是 640×270，已經用了） | 拍法 29；圖不要變形 | 免費重裁 `c set-xujia-yuan-ye-dong2-shan2-l1 520:292:792:120`（16:9，避開樹幹與瓦頂，含牆頭、暗田與遠山）；新 id |
| 36 | s30（`-xi-an`） | 俯看的土堆，沒有地平線，`far beyond them at the left … three men … walking away together, small` 沒有地方站 | 拍法 29 | 免費：`c "$O/set-shanjiao-qu-xi-l1.png" set-shanjiao-qu-xi-zhuo-l1 640:360:0:200`（傍晚版的左岸平地與松樹），s30 改送它，背景句改 `behind them, soft, the flat dry field and the line of dark pines` |
| 36 | s26 | 錢員外正面、10 秒長、又急又不信：第 34 集 s30、第 35 集 s23 這種長的正面三輪都笑或張嘴亂說，最後靠背影＋錄音 | 任務檔 2026-11-20（錢員外不笑的正面常失敗） | 先照寫跑 d1；**預先把 s28 的背影寫法當備案**（他第一格已背對、平掌拍桌、竹籌跳起，臉不入鏡，台詞錄音），d1 兩支都笑就直接用備案重拍。錄音 a02 a03 的音高偏高（258／214 Hz），a26 錄完照 PREP 降調 |
| 36 | 錄音後（BUY） | 錄音只有 3 句。照角色實測（秦霜中位 3.7、慢句 2.3–2.9；唐小棠中位 3.5、慢 2.9；阿令 3.4、很輕 2.9；錢員外 2.0–2.9，a02 量到 2.0；許硯 4.0；系統 4.3），**除必改 9 的 s30 外**最緊的是：s23（秦霜 16 字「冷」畫外，4.3–6.2／5.9，錄音蓋插鏡可慢放 1.1 倍）、s12（阿令 16 字「很輕」還要收竹哨，4.7–5.6／5.9）、s14（唐小棠 16 字，4.6–5.5／5.9）、s10（錢員外 14 字冷笑，5.6–7.0／7.3）、s11（心裡話 18＋系統 9，7.4–9.1／9.2）、s38（唐小棠 13 字帶刪節號、聲音發抖，4.1–5.3／5.9） | 聖經〈每集鏡數〉 | 錄齊後照 `span936.sh` 先核這六鏡；s23 超過 6.5 秒、s12 超過 5.9 秒就各改買 8 秒（各約 0.2 CU） |
| 37 | 第一鏡 | `set-xujia-yuan-ye-dong2-l1` 上**院門本來就半開**（門扇往內靠），第 37 集「二牛撞進來」若照圖會從開著的門走進來，撞門的那一下沒了；本集 s38 背景也是這扇半開的門 | 〈接點〉36→37；拍法 29 | 第 37 集寫稿時決定：照圖寫「二牛從半開的院門衝進來、一把推得門扇撞上牆」，或免費把門扇補成關著（新 id）並讓本集 s38 一起改送。本集不用改 |

## 接受（看過、不用改）

| 項目 | 為什麼 |
| --- | --- |
| s01 抬門閂 | 第一格兩手已握住門閂、一個動作（抬起、重量拖肩、橫抱），轉身靠門柱交給 s02；門關著寫兩次；唐小棠小背影不點名不送圖 |
| 拆鏡與一鏡一動作 | s02 第一格門已開、s08 第一格已站上石頭、s10 第一格已轉身、s20 第一格已上岸、s34 第一格已到院子中間：稿子的走位都放到第一格，合理 |
| 秦霜 | 柴刀全集不寫（extras 拿掉身分句的刀）；s21 從右邊秧田來、s24 背景秧田、s33 背對、s35 冷臉；s31 全景與 s33 背影只送 l1 |
| 三個探子 | 只有 s22 腳（三雙新黑布鞋白鞋底夾在草鞋中間）、s23 手（反手、拇指扣柄頂、黃色硬皮、指節舊疤，不寫刀字與 calloused）、s30 背影、s32 空蓆；s22、s23 第一格就是主體 |
| 鉤子 | s22 三雙新鞋、s23 反手握鋤、s36 火光拐彎下山（拍法 37 的寫法、不寫人與數字）、s38 抓袖子（懸念）都讀得出；s02、s32 見必改 1、8 |
| 阿令 | 第一場照第 35 集（布條、綁腿、竹哨），s12 收哨後各鏡不再寫；第二場起長袖放下；s37 手縮進袖、不寫短刀；不寫紅唇 |
| 許硯 | 沒有鬍渣字；第二場「沾泥」寫成淡淡的乾土；第三場外衣與陶油燈只在 s34、s38；s20 眼神放鬆不寫笑字 |
| 錢員外 s28 | 不送圖、不點名、服裝句（深金團花錦袍、小黑帽、矮胖），第一格起背對、甩袖走遠＋錄音，照第 35 集 fix4 |
| 夜院子的光 | 圖上後牆被一道沒有光源的暖光照著（e931 塗掉的燈籠留下的），文字寫冷月光加屋牆暖光；s32、s33、s35 的牆會偏暖，可以接受（PREP §5.1 已記，先看 d1） |
| 錄到的三句 | a01 許硯 3.02／6、a02 錢員外 6.02／8、a03 4.44／8，都放得下；a02 a03 降調的處理合理 |

## 小結

- **必改 9 項**，全部是改字或免費重裁，不花錢（BUY 一鏡多約 0.2 CU）：(1) s02 送的圖門關著、文字寫已推開——改送免費裁切 `-wai2`（沒有門扇），從門口旁邊拍人走進來；
  (2) s02 六支火把要點名誰拿，別落到要作揖的老人手上；(3) s02 之後又出現關著的門（`-ding` 給 s03 s04 s10、`-wai` 給 s06 s07 s09 s12b）——換成免費裁切 `-ding2`、`-wai2`；
  (4) s18 拿掉唐小棠「往左傾身」，免得她轉成側臉；(5) s35 秦霜回頭要從**左肩**看左下的許硯（`GAZE_REFINE` 一起改）；(6) 渠照圖寫成約膝深，不是一人深；
  (7) `-zhuo` 背景有一道白色的現代護欄，送 7 鏡，要免費塗掉再重裁；(8) 十二張草蓆改成並排、頭朝牆，s32 的三張空蓆才框得下；(9) BUY：s30 改 8 秒。
- **建議 12 項**；要付費的只有一項：把村口改成門扇已推開的圖（約 1.5–2 CU），s02 才看得到「門開了」；不做就照必改 1、3 的免費繞法。
- 八個寫稿決定都合理；要補的是：(3) s17 空白紙對焦清楚，會跟「這字工整」打架（建議 4）；(7) 12 張免費圖裡 `-zhuo` 有護欄（必改 7），`-xi` 不像傍晚斜陽，`-shan` 有樹幹而且被拉長，`-xi-an` 沒有地平線（建議 7–9）。
- **接點**：35→36 s01 接得上（守門人左右、阿令頭髮見建議 1）；36→37 s38 的站位接得上，但院門在圖上本來就半開，要交給第 37 集處理（建議 12）。
- **最可能放不下的句子**：s30（秦霜 16 字兩句、在畫面上說，4.3–6.2 秒／6 秒），其次 s23、s12、s14、s10、s11、s38。
- 改完 `r2.py`、`mkspec.py`、`cunkou_zha2_e936.sh`（`-wai2`、`-ding2`）、`shanjiao_qu.sh`（加清理）後重跑 `build936.sh`、`prep936.sh`、`e936d1.sh DRY=1`；錄音補完照 `span936.sh` 重核 BUY。
