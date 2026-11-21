# 第 18 集真人版 fix-polish：上架前精修重拍（2026-11-21）

照 `/root/mokaair-work/review-zt/RETAKE-BRIEF.md`。重拍清單：`consolidated/retakes.json` 裡 e018 的 B 級 5 鏡（本集沒有 A；s29、s08、s31、s40 是 C，不在這批）。
種子 9189101、9189102，960×544 Ref2VA，5 鏡 10 支、共 68 秒草稿。只寫了提示詞與 spec，沒有送出任何工作。

- 產出：`spec.json`、`prompts/sNN.txt`；`python3 -I ../../_scripts/polish-build.py 18` 寫出
  `~/mokaair-work/videos/zhong-tian-qu-qi-e918-dh/runpod/live/fixp/{prompts/,retake.json,colab-jobs.json}`。
- base：五鏡現用的都是 d1（`_live-e918/.../picks.json` 的 `draft` 都在 `d1/out/`；picks.json 沒有 `motion_from` 欄，從 draft 的資料夾判斷）。
- **參考圖每鏡都寫了 `pictures`，沒有用 `null`**：`polish-build.py` 先讀 `d1/retake.json`，那份是 `swap_pictures` 之前的圖（`set-xianya-l1`、`set-qianfu-ting-l1`）；
  真正送出去的是 `d1/colab-jobs.json`（`prep918.sh` 換成 `set-xianya-gongtang-dais-l1`、`-floor-l1`、`set-qianfu-houmen-ye-l1`）。寫 `null` 會拿到錯的場景圖。
- 本集不拍柴刀（分鏡〈真人版的改動〉），五鏡都沒有刀的句子。
- 寫法：只用正面描述，否定句只剩 base 原有的固定句（`no second copy`、`no subtitles`、s24 賴三的 `no talking, no mouthing words`）與 s36 新加的 NOSMILE 句（`REVIEW.md` 第八節的固定寫法）。

| 鏡 | 級 | 審片問題（看畫格條） | base | 改了哪些句子（舊 → 新） | 圖 | 拿不準 |
| --- | --- | --- | --- | --- | --- | --- |
| s26 | B | 紅手是膚色加後製橘色色塊（硬邊、手背與拇指側沒色）；掌心一顆小卵石，接不上 s25 兩手捧的大扁石；背景幾十盞燈籠排成格子 | `d1/prompts/ref-s26-9181101.txt` | 手的主人句改成「三個金戒指的胖手從 <Picture 1> 的暗金團花袖子伸出、臉在畫框上緣外」；紅 `palms and fingers stained … to the wrists` → 兩手整片同一個柿子橘紅、像泡過染料一直到袖口：每根手指與指尖、兩根拇指、兩掌、兩手背、兩腕；石頭 `one plain grey stone in the right palm` → 兩掌寬的扁灰石橫在兩掌上，第一秒兩手分開、石頭從下緣落出；地點 → 同一座小亭、從胸口往下看、手下只有亭子石板地（虛焦）、燈在上方畫外（不寫成排燈籠）；動作仍是一個：擦袍子兩下、再攤開；加 `The picture fixes the cloth of his sleeves only, never the mood.`（base 沒有這個分隔句，polish-build 要求） | `qianyuanwai-portrait-l1` → `qianyuanwai-sleeve-l1`（沒有臉的袖子裁切，圖 README 第 19 集手部插鏡的教訓） | 模型上一輪就是不肯把手畫紅，這是文字能做的最強寫法；仍是膚色的話只能再補色（剪接照稿降飽和）。審片改寫句的「翻過來看手背」沒做成動作（一鏡一個動作），手背的紅寫在第一格。重拍後封面要用新片兩掌全紅那一格重做 |
| s37b | B | 胡縣令長臉、老一截、帽更高，身後多一張條案與椅背、筆架跑到身後；跟 s32（圓臉、案上右邊筆架、身後屏板）不像同一人同一間 | `d1/prompts/ref-s37b-9181102.txt` | 景別 `medium close-up … from the chest up` → 照 s32 成片的樣子：`medium shot … from the waist up`、案緣橫在下緣、坐在官椅上；筆架寫成「三支筆掛著的深色小筆架、在案上畫右」（場景句與構圖句各一次）；身後「只有白屏板與左緣一條格窗」；加 `his round full face clean-shaven`；動作：第一格右手拿著木塊懸在案上一指高、第一秒輕輕放下，說最後幾個字時左手寬袖往畫右一揮（base 是「拿起再放」加「揮袖」兩個大動作）；說完兩手放在案上 | 照 d1 實送（`huxianling-portrait-l1`、`set-xianya-gongtang-dais-l1`） | s32 與 s37b 本來就是同一張圖同一段外貌句，臉的差別是抽籤；外貌錨句照 brief 沒改（仍寫 48 歲、雙下巴），只在構圖補「圓臉無鬚」。木塊落案的聲音大小要剪接再壓（審片不花錢那一項照做） |
| s24 | B | 畫面八成黑、遠處兩個沒有五官的小公仔、看不出錢員外開箱；賴三白衣黑帽；天上有星 | `d1/prompts/ref-s24-9181101.txt` | 長走道全景（`framed full length, small`）→ 站在後門口直看幾步外的小亭：四根深色柱、簷口橫在上緣（不露天空）、一張圓石桌、左上一盞白紙燈籠、亭後白牆在暗處；兩人膝上入鏡、錢員外佔畫高一半、兩人與桌子都在畫面中間一半（給剪接的左右門縫遮罩留位置）；錢員外在中偏右、臉四分之三朝畫左看箱子（base 朝畫右），賴三在中偏左、空手站著；拿掉賴三 `left foot dragging in a limp`；動作：第一格鐵絲已插進鎖扣，第一秒彈開，再兩手抓蓋掀開 | 拿掉 `set-qianfu-houmen-ye-l1`（長走道圖會把人拉回走道盡頭變小），剩錢員外三張與賴三一張 | 沒有場景圖，亭子只靠文字，夜裡的亭子可能長得跟 s25、s26 不一樣（s25、s26 本來也沒送場景圖）。賴三白衣黑帽是模型在遠景裡沒照圖，膝上景別應該會照圖；賴三的臉像許硯是定妝照的問題（審片中等 10，交站主），這次沒處理 |
| s36 | B | 錢員外整鏡 7 秒咧嘴大笑、眼睛彎，像被逗樂 | `d1/prompts/ref-s36-9181102.txt` | `caught and flustered: eyes darting, a stiff forced laugh pulling at his mouth, sweat on his upper lip` → 縮脖聳肩、`caught and scared`：眉頭往上擠在中間、額頭皺、小眼睛睜大往旁邊亂瞟、上唇與太陽穴冒汗、臉頰僵白、字與字之間抿嘴嘴角往下、下巴發抖；說話句加 `stumbling on the first word`；說完 `the forced laugh drops off his face` → 嘴抿上、嘴角往下、眼睛滑到地上，加 NOSMILE 句；仍跪著、胸口以上（接 s37 跪姿） | 照 d1 實送（`qianyuanwai-angle-a/b-l1`、`set-xianya-gongtang-floor-l1`） | 分鏡寫「乾笑」，這版畫面一點笑都不給，乾笑只靠錄音 a35 的聲音；審片改寫句寫站著，分鏡與 s37 的接點是跪著，照分鏡 |
| s09 | B | 唐小棠一個人站著對窗外講話、許硯不在畫面；變單髻戴耳環 | `d1/prompts/ref-s09-9181102.txt` | 照同集 s13（成片髮型對、許硯在）的過肩構圖：她在畫右前景背影、坐矮凳、頭轉向隔桌的他；髮型句加 `wrapped tight … with its ends tucked in`；許硯隔桌在畫中偏左、腰以上、往前湊著聽、左手按在桌上的藍布包（接 s08、s10）、眉頭皺、眼睛盯著她、嘴閉著；「整鏡看自己右袖」→ 整鏡看著許硯；動作仍一個：點頭、把已摺好的帳頁塞進右袖、左手撫平；「只有她一人」句 → s13 的「只有這 2 人」句；加許硯錨句 | 加 `xuyan-portrait-l1`、`xuyan-angle-a-l1`、`xuyan-angle-b-l1`（同 s13），茶樓圖照舊 | 審片改寫句要她「摺兩摺再塞」，摺紙與塞袖是兩個動作，照分鏡「第一格已經摺好」只塞；許硯整鏡沒動作，模型可能讓他開口（錄音鏡，他嘴動要剪或重挑） |

## 檢查（2026-11-21）

- `polish-build.py 18`：5 鏡、10 支、68 秒，0 錯。
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error、0 warning。第一次有 s09 `eye-glow` ERROR（`eyes on her face, his left hand flat on the blue cloth bundle` 的 eyes 與 blue 相距不到 40 字），改成 `his left hand flat on the cloth bundle, his gaze steady on her face`；
  s36 `gaze`（`his eyes flicking to him` 不算 eyes on）改回 `his eyes on him, then darting away`；s24 `headroom`（leans over，寫成 `space above his cap` 沒被認得）改成 `space above his head`。
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error、0 warning。
- 自己掃：新句子沒有 smile／laugh／grin（只有 s36 的 NOSMILE 固定句）、沒有 sword／blade／knife、沒有 star／moon、沒有 blood。

## 拍完要看

- s26：第一格兩手是不是整片橘紅（手背、拇指、手腕到袖口），還是又是膚色；石頭大小接 s25；背景有沒有又長出成排燈籠；有沒有長出臉。
- s37b：臉跟 s32 並排看；筆架在案上畫右；身後沒有條案椅背；木塊放下的聲音。
- s24：兩人大小、臉看不看得到五官；錢員外的手開箱在遮罩後的中間 60% 內；賴三衣服顏色；亭子跟 s25、s26 的光。
- s36：每 0.5 秒看嘴角，有一格上揚就不能用。
- s09：她的頭髮（兩丸子短帶）、她有沒有轉成側臉、許硯有沒有開口。
