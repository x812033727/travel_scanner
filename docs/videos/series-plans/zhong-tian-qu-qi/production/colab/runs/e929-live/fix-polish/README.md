# 第 29 集真人版 fix-polish：上架前精修重拍（2026-11-21）

`review-zt/consolidated/retakes.json` 裡 e029 列 A 或 B 的是 **s33、s26、s21（A）與 s11、s07（B）**；其他項（s10 柳葉、封面、s27–s30 糖箱與光、髮型的 s24／s27／s30／s35）不在這一輪。

- 種子 9299101、9299102；960×544 Ref2VA；5 鏡 10 支，共 60 秒（每鏡 6 秒，秒數都照 base）。
- base（`_live-e929/.../picks.json`）：s07、s21、s33 是 seed 9291101、s26 是 9291102，`motion_from: d1` → `d1/prompts/ref-sNN-SEED.txt`（d1 兩個種子的提示詞逐位元相同）；s11 是 9291201、`motion_from: fix1` → `fix1/prompts/ref-s11-9291201.txt`。
- 產生：`python3 -I ../../_scripts/polish-build.py 29` → `~/mokaair-work/videos/zhong-tian-qu-qi-e929-dh/runpod/live/fixp/`。
- 台詞一字沒改：s07 許硯原聲照說；s11、s21 許硯畫外錄音（a10、a19），畫面上只有手或指尖；s26、s33 唐小棠背影、鋪錄音（a24、a30）。
- 站主指定：s33 的帳本寫成**線裝布面帳本（同 s14），整鏡同一本**。

| 鏡 | 審片問題（現在那支） | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s33（A） | 帳本是有橫線、上緣帶線圈的現代拍紙簿，1.8 秒後在鏡內變成一疊厚線裝紙；兩顆丸子綁寬粉緞帶（`x/s33-a.jpg`、`shots/s33.jpg`） | `d1/…/ref-s33-9291101.txt`，6 秒 | 道具：「one thick stack of plain blank paper sheets stitched along one edge with cord … against her chest」→ 一本闔著的線裝帳本：大書大小、約兩指厚、前後封面是素面平滑的稻草色布、書脊白線縫、頁邊是一條平整的淡色帶；抱在胸前**右側**、外半露在右上臂外（從背後才看得到）。動作：「the stack of paper slips down … both her hands catch it」→ 闔著的帳本沿右側往下滑一掌寬、兩手把它夾回胸前，加「整鏡一直闔著、完整、從第一格到最後一格是同一本布面帳本」。景別：close-up、肩上 → medium close-up、腰上（肩上景帳本被身體擋住，模型才把它舉到臉旁攤開）。髮型（審片 8）：加正中一條直分線、「exactly two small tight round buns … as round and smooth as a ball」、粉緞帶 → 每顆丸子根部一條窄粉帶 | 不換（`set-guangchang-pm-you-wu-l1`） | ① s14 實際畫出來的是一大疊散的淡黃紙、看不到布封面（我抽了成片 60.0 秒那格看），所以「同 s14」只對得上顏色（稻草色）與大小，封面是新寫的；s14 不在這一輪。② 審片寫「thin」，我寫「兩指厚」折衷，接 s14 那疊的厚度。③ 帳本放在右側可能跟畫右緣小小的車廂擠在一邊，挑片看車廂還在不在 |
| s26（A） | 她撕的是自己手上那本白冊子上的紙，糖箱在兩公尺外沒人碰、封條自己掉；頭髮變成兩個垂環髻（`x/s26-tear.jpg`） | `d1/…/ref-s26-9291102.txt`，6 秒 | 拿掉「her left arm holding one thick stack of … paper … against her side」→ 左臂垂在身側、手張開放鬆（畫面裡只剩一張紙：封條）。糖箱：「just beyond her right hip」→ 她緊貼著箱子站，箱子貼著她右胯前、箱蓋在胯高、在畫右下，蓋上兩條空白白紙貼成大 X，右手第一格就捏著蓋子正中的交叉處。動作：「tears … off the chest in one pull」→ 往上一把撕下兩條、右肘往右上甩出、紙條飛走、箱蓋留在她胯前；再寫一次左臂一直垂著。景別：腰上 → 胯上（箱蓋才在畫內）。髮型同 s33 | 不換（`set-guangchang-zuo-l1`） | ① 圖上的箱子在畫右中、離台邊近，模型可能照圖把箱子放遠；文字寫了「touching her right hip」。② 帳本這鏡不在她手上（s24、s27 有），審片同意這樣；剪起來觀眾不太會注意。③ 撕的方向往右上，紙條可能飛到畫外看不到 |
| s21（A） | 放銀錠的是又黑又粗、滿是皺紋的老人的手；背景是紅柱大殿、紅旗與籤筒；一開始就捏著銀錠壓在案上（`x/s21-a.jpg`、`x/combo1.jpg` 左上） | `d1/…/ref-s21-9291101.txt`，6 秒 | 手：「one man's right hand in a faded blue-grey sleeve cuff」→ 年輕男子的右手、光滑細長、手指長直、膚色白淨、指甲短而乾淨、藍灰布袖口。起點：銀錠「a finger's width above」→ 在畫左、舉在布面上一掌高（才看得到放下）。動作：「sets … down and lets go」→ 一個平順的動作放下、有一點重量地落定、張開手指、往左收出畫，留銀錠立在紅布上。背景：加「案後遠而虛：廣場的黃土、一棵禿樹、低瓦屋頂、晴空」（正面寫，不寫 banners／pillars 這些否定名詞）。驚堂木那句移到前面、寫明在布的右半 | **加** `set-guangchang-shu-l1` 當案後的虛焦背景（Picture 2）；Picture 1 仍是 `set-guangchang-an-l1` | ① 加第二張圖可能讓模型把禿樹畫得太清楚或把案子縮小；挑片看背景是否虛焦。② 審片寫「從畫左進來」，我改成第一格手已在畫左拿著銀錠（插鏡第一格就是特寫、避免空鏡起手），收手才出畫 |
| s11（B） | 4.3 秒一整片糊黃的雲紋加黑點，沒有紙邊、沒有手、沒有透光，像雜訊材質圖（`shots/s11.jpg`）。fix1 為了擋掉 d1 的雪景市集，寫了「滿版、四邊超出畫框」，又只送黃紙材質圖 | `fix1/…/ref-s11-9291201.txt`，6 秒 | 構圖：「filled edge to edge … reaches past all four edges … only the dull yellowish sheet is in the frame」→ 第一格就是一張芥末黃粗紙對著低斜冬陽，約占畫面中間三分之二寬、四邊都在畫內、四周一圈藍天；紙裡的疙瘩、纖維、黑點那句保留；另起一句：年輕男子的拇指與兩指尖捏著紙的左下角，藍灰袖口邊在畫面下緣；「只有黃紙、指尖與藍天在畫裡」。開頭地點句加回「縣城廣場正午、仰看晴空」。動作：在指尖間微微一顫、陽光透過來。結尾「keeps the look of its reference picture」→「keeps the colour and grain」 | **換**：`prop-huangzhi-l1` 從唯一的圖改成 Picture 2（紙的顏色與紋理），加 `set-guangchang-shu-l1` 當 Picture 1（紙後的禿樹、瓦屋頂與晴空） | ① 材質圖仍然送，模型可能又把它鋪滿整個畫面；沒有更好的道具圖（要一張有紙邊的黃紙得再做免費圖）。② d1 曾在紙後長出雪景市集；這次送了晴空圖，應該壓得住。③ 指尖寫在紙角，手可能長大或多一隻手 |
| s07（B） | 許硯說「這張，是包那塊毒糖糕的紙」時那張是米白色，跟 s09 的白紙幾乎同色，s11 卻是深土黃（`shots/s07.jpg`、`s09.jpg`、`s11.jpg`）；也沒有一抖 | `d1/…/ref-s07-9291101.txt`，6 秒 | 紙：「one crumpled sheet of rough blank yellowish paper」→ 一張揉皺的空白粗紙，明顯是芥末黃、像舊稻草，比白紙深黃得多，約兩隻手掌大，在陽光裡。動作：「gives the crumpled yellowish sheet one sharp shake so it hangs straight down」→ 第一個字就一抖、紙垂開、整句空白暗黃地垂在陽光裡。說話、視線、冷臉那幾句照 base | **加** `prop-huangzhi-l1` 當 Picture 4（這張紙的顏色與紋理，跟 s11 同一張黃紙）；許硯 l1、angle-a、`set-guangchang-shu-l1` 照舊 | ① 加材質圖有可能被畫成背景或牆；挑片看天空是否還是藍的。② s09 左手那張摺起的黃紙也是米色，s09 不在這一輪，三鏡的黃仍可能對不齊 |

## 檢查（2026-11-21）

- `polish-build.py 29`：5 shots、10 drafts、60 s，0 錯誤
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error(s)、0 warning(s)

沒有送出任何 Colab／RunPod 工作。
