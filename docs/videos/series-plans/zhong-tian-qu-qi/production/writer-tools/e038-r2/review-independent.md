# 第 38 集重製版 r2（e038-r2，內部 938）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿人：沒參與寫稿的獨立代理，2026-11-23，開拍前（d1 還沒跑；錄音 33 句已錄齊）。只寫了這一個檔；沒改 `r2.py`、`mkspec.py`、`check938.py` 或別的檔，沒開 Colab／RunPod（`zt-live2`、`zt-live3` 都沒碰），
  沒用站台 TTS，沒付費生圖，沒 commit。沒讀寫稿者的自審 `writer-tools/e038-r2/review.md`，也沒讀 scratchpad 的 `e938prep/PROGRESS.md`。
- 審的對象：`writer-tools/e038-r2/r2.py`、`docs/videos/zhong-tian-qu-qi-e038-r2/{script.md,storyboard.md,video.json,overlays.json}`、
  d1 提示詞 `~/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live/d1/prompts/*.txt`（80 支）與 `colab-jobs.json`（逐鏡送圖，含 `append_pictures`）、
  `colab/runs/e938-live/{mkspec.py,spec.json,PREP.md}`、`colab/runs/e938/extras.json`、`hailuo/clips-dh-e938.json`、
  `live-action/free-e031-e040/{xujia_tangfang_e938.sh,roads_e938.sh}`、scratchpad `tools/{prep938.sh,check938.py,prep938.log}`。
- 對照的文件：`r2-bible-e031-e040.md`（拍法 1–43，〈接點〉37→38 與 38→39，〈道具〉〈人物〉〈小角色〉〈場景〉，〈原版必修〉第 38 集；第 41、33、42 條逐句看過）、任務檔第 33–37 集的教訓、
  `OWNER-CHECK-20261122.md`、第 37 集 `colab/runs/e937-live/{PREP.md,cut-review.md,cut-review-2.md,final-check.md}`、第 37 集 `review-independent.md`（格式照它）。
- 參考圖都開全尺寸看過：病房 `set-xujia-tangfang-l2`、`-chen-l1`、`-xi-l1`，以及九張裁切（`-chen-/-xi-/（夜）{chuang,men,zhen}`）；院子 `set-xujia-yuan-ye-dong2-l1`、`-wu`、`-zhong`；
  官道 `set-guandao-ye-l1`、`-ce`、`-shu`；城門 `set-chengmen-ye-l1`、`-zha`、`-qiang`、`-men`、`-lu`；醫館 `set-yiguan-men-ye-l1`、`-men`、`-feng`、`-jie`、`-di`；
  `prop-zaohongma-l1`、`duizhang-portrait-l1`、`prop-changqiang-l1`、`tangxiaotang-back-shuangji-e929-w3`（白天原檔與 `-ye`）。
  我自己放大看的圖在 scratchpad `e938rev/`：`room-table.png`（病房的桌子擋在枕頭前）、`gate-arch.png`（城門拱洞裡兩扇門都關著，半開的是拱洞右邊另一扇小門）、`gate-barrier.png`（拒馬柵貼著城牆），以及 `props.png`。
- 接點：我自己從第 37 集定版成片 `e937-live.mp4`（205.81 秒）抽了 190.8 秒到片尾，每秒一格（scratchpad `e938rev/tail/sheet.jpg`），最後一格存成 `end.jpg`。
- 語速：33 句錄音都在 `audio/`。我用 `silencedetect`（−40 dB）重量了最緊的幾句，也核對了 `tools/span938-buy.txt` 與 `f0y938*.txt`，沒有再用估的。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| d1 清單 | 共 80 支，每個種子 247 秒（5 秒 9 支、6 秒 23 支、8 秒 8 支），兩個種子合計 494 秒，跟 `r2.py` 的 `BUY` 和 `colab-jobs.json` 逐鏡對得上；兩個種子的提示詞除了種子號一字不差；80 支的 `prompt_sha256` 都相符，送的圖都在；`<Picture N>` 的最大編號等於送圖張數 |
| 分隔句 | 每支剛好一次 `never the mood. `、一次 `One continuous shot.`；d1 裡沒有精修句（`as the first frame`、`3D CG`）漏進來（拍法 39） |
| 風格句與許硯 | 每支都寫「with the look of a feature film」，沒有 `cinema camera`；沒有 `stubble` |
| 唐小棠 | 80 支都沒有 `Tang Xiaotang`、`stand-up collar`、`apricot`、`abacus`；她的三張臉部圖一張都沒送；五個背影鏡（s02 s04 s07 s16 s18）都把雙丸子背影圖加在最後一張（白天送原檔、夜裡送 `-ye`），也都寫了「that picture fixes the hairstyle only」；本集沒有她的正臉 |
| 跪姿拍到膝蓋 | 許硯跪著的只有 s01、s19，兩鏡都寫 `framed full figure with both knees on the floor`；s03 改成坐在床沿；s06 是近景，不寫跪 |
| 柴刀、兵器 | 沒有 `chopper`、`sword`、`blade`、`saber`、`dagger`；隊長的長矛（s23–s26）和短刀（s35–s37）、弩（s32 起）都只出現在劇情要的鏡 |
| 掛著的東西（拍法 33） | 沒有 `milestone`、`tablet`、`notice`、`sign`、`plaque`、`banner`、`lantern`；四張母圖上也沒有招牌、告示板或石碑（城門的匾在試鏡時已經塗掉） |
| 會長字或會畫錯的字 | 沒有 `open`、`crowd`、`hundreds`、`villager`、`fog`、`mist`、`smoke`、`candle`、`leap`、`jump`、`deep pool`；搜到的一個 `mud` 是 s33 的 `smudge`，不算 |
| 人數 | s01 二人、s02 二人、s04 三人、s12 三人、s16 三人加一匹馬、s18 二人加一匹馬、s27 與 s27b 二人加一匹馬、s32 九人、s35 與 s37 三人：`exactly N` 都跟描述對得上，`Only…` 句也再寫一次；單人鏡寫一次 `is the only person`，另加 `No second copy of anyone appears`（跟第 37 集同樣做法） |
| 笑 | 有臉的鏡都逐部位寫 `not smiling`。沒寫的是背影鏡（s07 s18 s36）、插鏡（s31 s34）、全景動作鏡（s20 s27 s27b）；s24 年輕守軍的 `laughing` 是稿子要的，而且臉朝外 |
| 精修文字 | `clips-dh-e938.json` 40 筆，都沒有 `Tang Xiaotang`、`stand-up`、`cinema camera`、`deep pool`；背影鏡的名字已換成「the young woman seen only from behind」；17 個 `GAZE_REFINE` 方向句跟 d1 一致 |
| 光線句 | 病房分清晨、正午、傍晚、入夜四種；院子、官道、城門、東街都是月光；`clear and still` 逐鏡換成 `AIR` 句；插鏡不寫地點（拍法 35） |
| 錄音對 BUY | 33 句都放得下。我重量的：s31 a28 有聲部分到 5.64 秒（檔長 5.96）／8；s09 a09 5.18／8；s06 a06 5.10／8；s23 a22 4.83／8；s19 a20＋a21 約 5.3／8；6 秒鏡裡最長的是 s24 a23 約 4.05 秒 |
| 相鄰說話者音高（拍法 43） | PREP §4 列的組合我都用 `f0y938*.txt` 重算過，都 ≥ 3 個半音（最小 s14 許硯 124 → s15 系統 153，3.6）。**漏列的一組**是 s18 唐小棠 281 → s19 小禾 277，見建議 7 |
| 檢查工具 | `prep938.log`：preflight 與 `check_manifest` 都是 0／0；否定名詞、舊寫法、容易長字的名詞、掛著的東西都是 0 |

## 寫稿者的決定：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| 接點 37→38：站位 | 第 37 集最後一格（`e938rev/tail/end.jpg`）：許硯在畫左，舊灰外衣，袍子上有石灰白；小禾躺在他右臂彎裡，**頭在畫右**、臉頰通紅、閉眼。s01 照聖經寫成病房：同一個清晨、小禾已經在床上、頭在枕頭那頭（畫右）、許硯跪在靠鏡頭這一側、臉朝畫右、右手按在她額頭上，**接得上**。但圖上的桌子擋住了這個站位 | 接受；圖見必改 1 |
| 病房用唐小棠房間的圖（門在左、床靠後牆、枕頭在右、小桌在右前） | 房間的格局、光、門的方向都照圖寫，也照聖經第 42 條。**可是我全尺寸看圖後發現，小桌就緊貼在床前，從 x≈790 一直到右牆，枕頭（x 1015–1150）整個在桌子後面**（`e938rev/room-table.png`）。小禾的頭擺在枕頭上，許硯就沒有地方跪；s03「坐在床沿、她的頭枕在他右前臂」、s04「許硯靠在枕頭那頭的床柱」、s05「枕上的臉」都會跟桌子撞在一起。`-chen-chuang`、`-chen-zhen`、`-xi-zhen`、`-chuang`、`-zhen` 這幾張裁切，下半部都是桌面、兩疊紙包和蠟燭 | 必改 1 |
| 傍晚用免費調色的 `-xi` | 整張偏暖、偏褐，讀得出傍晚。窗是乳白色，不是文字寫的橘光，但差得不多。`-chen` 和 `-xi` 右牆靠蠟燭那一帶還留著一片橘光，熄掉的蠟燭頂上有一團灰白光暈，模型可能把蠟燭點亮 | 接受；建議 11 |
| 唐小棠五鏡從背後拍、加雙丸子背影圖 | 照站主 11-22 的規則。白天的原檔是藍天加兩棟屋，送進室內的 s02、s04、s07（第 37 集建議 1 說的是夜裡，這次是室內） | 接受；建議 10 |
| s01、s19 寫全景跪姿；s03 改坐床沿 | 照站主的跪姿規則，寫法也對；跟桌子的衝突算在必改 1 | 接受 |
| s02 送門那張裁切（`-chen-men`） | **鏡頭在她背後、她往床走，背景應該是床，送的卻是門**：圖上門就在正前方，等於她背對鏡頭朝門走，像要出門；文字又寫「behind them, soft, the bed under the small window」，圖跟字對不上。門也沒寫是開是關 | 必改 2 |
| s09、s12 的門往內推開靠牆，門外看得到院子／阿令 | `-xi-men` 和 `-men` 這兩張圖上，**木板門都關著**（門扇整片、門把在右緣）。s12 寫「門開著、門外阿令在聽」，下一鏡 s13 又寫「身後是關著的門」，相鄰兩鏡門一開一關；`check938.py` 第 192 行斷言的也是「推開」，跟圖相反 | 必改 3 |
| c12「門外阿令在門檻外聽」 | 這是稿子 2026-11-06 審稿補的，s13 的「← 因為 c12」要靠它成立。保留，但她的位置改成門內門邊（見必改 3） | 改後接受 |
| s13 用手拉緊布條、s14 遞馬鞭、s15b 拆鏡 | 都是一鏡一個動作。量過以後，s15＋s15b 兩句錄音合起來約 5.8 秒，加上停頓其實塞得進一支 8 秒；不過拆成兩鏡可以換景別（近景與中近景），品質比較好，所以接受 | 接受 |
| 院子 s16：上馬、原地轉半圈不寫、人與馬不重疊 | 第一格左腳已經踩進馬鐙、兩手按著鞍；馬頭朝左，她從馬的左側上馬，方向是對的。秦霜在左、唐小棠在左下前景背對鏡頭，都跟圖一致 | 接受 |
| 院子 s18：馬從院門左半空著的門洞衝出去 | 院門門扇掛在右邊門柱、往內半開，照第 37 集必改 1 寫對了。但門洞左半在圖上只有約 60 px 寬（全寬 1312），容不下一匹馬加騎馬的人；唐小棠背影在**正中**、腰以上，而院門在 `-zhong` 這張圖的中偏左，她會把門洞和馬擋住 | 建議 3 |
| 官道照圖、s20 慢推、s21 跟拍 | s21 跟拍（全集只有這一鏡）、側面、腰以上加馬頭頸，接受。**s20 不行**：`-ce` 上的路是從右下前景往遠處消失點斜著退進去，不是「從右邊橫到左邊」；馬照文字由右往左跑，就是踩在犁過的田上橫越，照圖跑就是往遠處跑，兩種都不是「沿著官道由右往左」 | 必改 4 |
| 城門照圖：「左扇關、右扇往外半開」 | 我放大看了（`e938rev/gate-arch.png`）：**拱洞裡兩扇大門都關著**，兩個獸面門環就在門縫兩邊。往外半開的是**拱洞右邊牆上另一扇比較小的門**，門後的門洞被它自己擋住，看不到。這扇小門剛好就是稿子寫的「門洞旁一扇小門」。可是文字把它寫成大門的右扇，模型可能把拱洞右半打開，跟圖打架；s27b、s28 寫的「門扇後面的黑暗」，圖上也沒有 | 必改 5 |
| 城門照圖：拒馬柵沿著牆擺 | 拒馬柵貼著城牆根，從小門右邊的火把一路往右延伸到遠處（`gate-barrier.png`），**沒有擋住路**。路在柵外的石板地上，直接通到小門。所以「躍過木柵」在這張圖上沒有理由：從右邊來的馬沿著石板路就能跑到小門。s27 寫成側面、馬頭朝左往柵衝，馬其實跟柵平行。這一下是本集片名和縮圖（`THUMB` 是 s27） | 必改 6 |
| s27／s27b 拆鏡（聖經第 41 條） | 拆得對。但 s27 動作句的結尾寫「gathers itself at its foot, its forelegs just lifting from the ground」，等於把起跳寫進去；5 秒的片段裡，模型會照慣性把跳躍做完（第 41 條要避開的就是這一下） | 必改 7 |
| s27b 隊長的位置 | s27 他在柵後（柵與牆之間），s27b 第一格卻「on the paving at the right」，跑到柵外右邊去了 | 建議 4 |
| c23 隊長身後兩個守軍、c28 弩手從城門洞跑出，都不拍 | 減少人數（拍法 34）；弩手第三場才出現，接受 | 接受 |
| s24 年輕守軍改用矛尾敲地 | `-men` 那張圖上沒有柵，改得合理；側後拍、只露臉頰一角、放錄音 | 接受 |
| s25 改成中景、腰以上加馬頭頸 | 照第 41 條；`-lu` 是柵的尾端加來路，她面向左，方向一致 | 接受 |
| 東街：醫館就是最近那間、門左邊有方石拴馬樁 | 圖上最近那扇門有門閂、一級寬石階，左邊一根方石樁，對得上（「兩級石階」圖上只看得到一級，影響不大）。s30 馬在畫左緣、只到頭頸、韁繩繞在樁上，寫法對。**但 s32 的全景把那根樁放在右前景，馬卻沒寫**：馬從畫面上消失了（聖經 38→39 寫著棗紅馬拴在拴馬樁上） | 必改 8；s33、s36 見建議 6 |
| s32 弩手寫「seen side-on and from the front at a distance」 | 〈小角色〉寫弩手「只拍背影、側後」，但拍法 34 的原則是「正臉近景不拍」，遠景可以。這裡人小、臉在盔的陰影裡，可以接受 | 接受 |
| s21 的跟拍；隊長用加圖的方式送（`duizhang-portrait-l1` 加在最後一張，補表情句與分隔句） | 跟拍見上一列。隊長那張圖是開面盔、護耳、紅纓、黑甲紅釘，跟 `CAPTAIN` 的句子一致；單獨拍他的鏡由場景句開頭，補了 `FACES`；本集他每鏡都送同一張圖，原版必修「同一張臉、同一頂盔」做到了 | 接受 |
| 插鏡 s31（門縫）、s34（弩） | 第一格就是主體，不寫地點；送的裁切只當地面和光 | 接受 |
| c34 拉弦改成舉平、c35 第一格短刀已在手上、s38 隊長身後不帶弩手 | 都是一鏡一個動作；s38 背景少了弩手，但近景裡看不出來 | 接受 |
| BUY：長句一律 8 秒 | 都放得下。s12、s13、s18、s23 這四鏡用 6 秒其實也夠，可以省一點（建議 12） | 接受 |
| POOLMARK（官道、城門、東街的提示詞為了選圖帶「below the deep pool」，d1 再拿掉） | d1 裡是 0；PREP §6 提醒了之後每支 fix／retake 都要帶同一組替換 | 接受 |

## 必改

| # | 鏡 | 問題與證據 | 依據 | 具體改法 |
| --- | --- | --- | --- | --- |
| 1 | s01 s03 s04 s05 s19（s06–s08 也受影響） | **病房的小桌擋在枕頭那頭的床前**。母圖 `set-xujia-tangfang-l2`／`-chen`／`-xi`：桌面從 x≈790 一直到右牆，緊貼著床的前緣，枕頭（x 1015–1150）整個在桌子後面（`e938rev/room-table.png`）。照現在的文字，小禾的頭在枕頭上，許硯「跪在床前、右手按她額頭」（s01、s19）就會跪進桌子裡；s03「坐在她旁邊的床沿」坐的地方正是桌面；s04 他「靠在枕頭那頭的床柱上」，人會在桌子後面；s05 的下巴以上近景送的 `-xi-zhen`，下半部 60% 都是桌面、紙包和蠟燭。模型如果照圖，就會把人擠變形；如果照字，就會把桌子吃掉 | 拍法 19、29（參考圖壓過文字）、42；第 39 集第二場「白大夫坐床頭（右）」也會撞到同一個問題 | **建議 A（要花錢，約 0.5–1 CU）**：Qwen 用 `set-xujia-tangfang-l2` 當底圖，「只改一件事」：`the small wooden table with its candle and the two paper packets is moved back against the right wall beyond the pillow end of the bed, leaving the floor in front of the whole bed clear; the bed, the quilt, the pillow, the window, the door and the walls stay exactly the same`，跑兩個種子，存成新 id `set-xujia-tangfang-kong-l1`；再照 refs README 的清晨調色做 `-kong-chen-l1`，照 `xujia_tangfang_e938.sh` 的 `-xi` 調色做 `-kong-xi-l1`，三組裁切照原本的框重裁（新 id）。文字的 `ROOMLAY` 改成「…a small wooden table against the right wall beyond the pillow end」；s04 的「the empty clay medicine bowl … on the small table at the right」可以保留。第 39 集第二場也用這組圖。**建議 B（免費的退路）**：把小禾的頭改到床的**左**端：`XIAOHE_BED` 開頭改成「lying on her back with her head at the LEFT end of the bed by the slatted bed rail, on a folded cloth, under the pink quilted cover…」，畫右那顆枕頭寫成「the quilted pillow at the far right end, beyond her feet」；s01 s03 s08 s19 改成許硯臉朝**畫左**（`GAZE_REFINE` 一起改）；s05 改送新裁切 `-xi-zhen2`（`crop=480:270:440:240`，左床欄加床的空白段，不含桌面）。另外也要確認第 37 集最後一格（她頭在畫右）跟這個左右換過來的版本可以接受 |
| 2 | s02 | **送的圖跟文字不一致，人也走反了**。送 `-chen-men`：門就在正前方。鏡頭在她背後、她「往床走」，背景應該是床；照這張圖，她會變成背對鏡頭往門走。文字又寫「behind them, soft, the bed under the small window」。門也沒寫是開是關（r2.py 開頭說每次入鏡的門都寫明開關） | 拍法 19、35；站主「門寫明開關」 | `mkspec.py` 的 `PLACE` 把 s02 改送 `-chen-chuang-l1`（必改 1 走 A 就送 `-kong-chen-chuang`）；`loc` 從 `rm_d` 改成 `rm_c`；`alone()` 的 where 改成 `just in from the doorway beyond the left edge of the frame, walking in toward the bed,`；「one step beyond her … by the foot of the bed」保留（`-chen-chuang` 的床尾就在畫左）。**床一入鏡就要寫小禾**（原版必修「床在畫面裡的鏡就寫她」）：背景句改成 `behind them, soft, in the bed under the small window, {XIAOHE_BED_SHORT}, her eyes shut, her lips closed`，`chars` 加 `xiaohe`（送她的定妝照），人數改成 `exactly three people`，`mkspec` 的 `TANG_BACK["s02"]` 改用 `ONLY_3` 那一型，寫明 little Xiaohe in the bed |
| 3 | s09 s12（s13 s15 s15b 跟著改） | **圖上的房門是關著的，文字寫推開**。`-xi-men`、`-men`：整片木板門、門把在右緣、沒有門縫。s09 寫「the plank door standing swung back inward against the wall, the dusky yard beyond the doorway」；s12 寫「which stands swung back inward … through the doorway … a young woman … just outside the threshold」；下一鏡 s13 送同一張圖，寫的是「the shut plank door」，連續兩鏡門一開一關。第 35 集的教訓已經寫了「提示詞要明寫門扇關著」 | 拍法 19；任務檔第 35 集 fix3「s32 門關」 | s09：`the plank door standing swung back inward against the wall, the dusky yard beyond the doorway;` → `the plank door at the left standing shut behind her;`；`her right hand gripping the door frame` → `her right hand pressed flat on the shut plank door behind her`；長槍改成 `already leaning upright against the plaster wall beside the shut door, well apart from her`。s12：`standing just inside the plank door, which stands swung back inward against the wall` → `standing just inside the shut plank door`；門外的阿令改成 `behind her at the far left, soft and out of focus, a young woman in grey-white standing still with her back to the shut plank door, only her head and shoulders, listening, her lips closed`；動作改成 `Qin Shuang glances back once over her shoulder at the young woman by the door and turns back, pressing her free left fist against the plaster wall`；`mkspec` s12 的 only 句跟著把 `beyond the doorway` 改成 `by the shut door`。s13 的「already stepped in … and stopped in the middle of the room」改成 `already stepped forward from the shut plank door`。s15、s15b 的 `the dark doorway` 改成 `the shut plank door`。`check938.py` 第 192 行的斷言改成斷言 `shut` |
| 4 | s20 | **官道的路是往遠處退進去的，不是橫過畫面**。`-ce`（`crop=720:405:0:210`）：路從右下前景斜著退到右上的消失點，左邊三分之二是犁過的田。文字寫「the wide pale dirt road running across the frame from the right edge to the left; on the road … gallops across the frame from right to left」。照圖跑就是往遠處跑（違反第 41 條「去程一律右往左」）；照字跑就是踩著田橫過去，畫面上還有一條往裡走的路 | 拍法 19；聖經第 41 條；原版必修（方向相反） | 免費：重裁新 id `set-guandao-ye-ce2-l1`（`crop=520:292:0:228`：只有楊樹一排、樹腳的平地和夜空，退進去的路幾乎全裁掉，右下角留下一小段路肩）；文字改成 `a long line of tall dark poplars across the frame against the deep blue night sky and a pale beaten earth track along their foot running across the frame from the right edge to the left; on the track, …`，動作改成 `the horse gallops across the frame from right to left along the track at the foot of the poplars`（`G1` 的「wide dirt road to the county town」留在地點句當交代）。s21 的 `-shu` 路只在右下角，跟拍時背景會滑過去，可以照舊 |
| 5 | s22 s24 s27 s27b s28（s23 s26 也有入鏡） | **城門寫錯了：拱洞裡兩扇大門都關著，半開的是旁邊的小門**（`e938rev/gate-arch.png`）。`GATE` 寫「its left leaf … shut and its right leaf … standing half swung back outward」，s24、s28 寫「the shut left leaf of the gate」，等於告訴模型大門右扇是開的；s27b、s28 寫「the dark gap behind the half-swung leaf」，圖上沒有這個缺口。s23、s26 送的 `-qiang` 左緣就是那扇小門，文字卻沒寫它開著或關著 | 拍法 19、29；站主「城門兩扇寫明開關」；稿子 c22「門洞旁一扇小門開著」 | `GATE` 改成：`the big arched gate in the grey brick city wall at the left, both its tall leaves of dark studded planks shut, two iron ring knockers at their middle; just right of the arch, a smaller side door of studded planks standing swung out toward us from the wall, its dark doorway hidden behind it; one torch fixed upright in an iron holder left of the arch and one right of the side door, nobody holding them, …`。s22：`at the left edge the swung-out small side door of studded planks with one torch …`；s24：`leaning one shoulder against the swung-out small side door … behind him, soft, the two shut leaves of the big gate under the brick arch`；s27：`at the left the swung-out small side door …`；s27b：`running on toward the swung-out small side door … plunges past the edge of the side door into the dark doorway behind it`；s28：`toward the dark doorway behind the swung-out side door`、`behind him, soft, the two shut leaves of the big gate`；s23、s26 的背景加 `at the left edge, soft, the edge of the swung-out small side door`。`check938.py` 第 194–195 行跟著改；r2.py 的 zh、PREP §1、聖經〈場景〉城門那一列寫成「大門兩扇關、旁邊小門往外開」 |
| 6 | s22 s27 s27b（s23 s25 s26 跟著重裁） | **拒馬柵貼著城牆，沒有擋路，「躍過木柵」沒有理由**（`gate-barrier.png`）。從右邊來的馬沿石板路就能直接跑到小門；s27 寫成側面、馬頭朝左往柵衝，馬跟柵其實是平行的，衝刺看不出是要跳柵。這一下是本集片名（「她一騎躍過城門木柵」）也是縮圖（`THUMB = s27`），PREP §5-1 已經提出可以付費修 | 稿子 c22「木柵橫在城門前的路上」；聖經〈道具〉「城門的木柵：一道齊腰高的木頭拒馬柵」；品質優先（站主 11-21） | **建議（要花錢，約 0.5–1 CU，d1 前做）**：Qwen 用 `set-chengmen-ye-l1` 當底圖，「只改一件事」：`the waist-high barrier of crossed wooden stakes now stands across the paved road, running from the foot of the wall just right of the small side door straight out toward the lower right of the frame, blocking the road to the side door; the gate, the side door, the torches, the wall and the moon stay exactly the same`，兩個種子，存成新 id `set-chengmen-ye2-l1`。`roads_e938.sh` 的四張城門裁切照新圖重裁（新 id）；文字「along the foot of the wall」改成 `standing across the road just right of the small side door`；守軍站在柵的城門那一側；s27 改成 `seen from the side and a little behind, charging toward the barrier across the road`。**不花錢的退路**：照圖拍，把 s27 改成從側後拍、馬斜著往牆和柵衝，接受觀眾不一定看得出為什麼要跳（要協調者決定） |
| 7 | s27 | **動作句把起跳寫進去了**：「gathers itself at its foot, its forelegs just lifting from the ground」。5 秒片段裡，馬衝到柵前只要一兩秒，剩下的時間模型多半會把跳躍做完。第 41 條要的是「衝向木柵」和「已經落地」兩鏡，空中那一下交給剪接 | 聖經第 41 條；第 37 集 s27 挑刀只做一半的教訓（拍法 32） | 動作改成：`the horse pounds across the paving straight toward the barrier, closing in stride by stride, still two strides short of the stakes with all four hooves on the ground as the shot ends, while the guard captain throws himself aside`；zh 從「衝到柵腳、馬蹄剛要離地就剪」改成「剪在離柵還有兩步」；`check938.py` 加一條斷言：s27 不能出現 `lifting`、`forelegs` |
| 8 | s32 | **全景裡馬不見了**。s30 寫明韁繩繞在醫館門左邊的方石拴馬樁上；s32 送的 `-jie`，右緣那根方石樁就是同一根（母圖 x≈718–758），文字也寫了「the square stone hitching post soft in the right foreground」，卻沒寫馬。聖經 38→39 寫著棗紅馬拴在門前的拴馬樁上，第 39 集第一場還要用到這匹馬（原版必修的同一類問題：東西從畫面上消失） | 聖經第 41 條（拴著的馬寫在哪一側、拴在什麼上）、〈接點〉38→39 | s32 構圖在 A-ling 前面加一句：`at the right edge beside the steps, {HORSE}, tied by its reins to the square stone hitching post, standing side-on with its head toward the left, well apart from her`；人數改成 `exactly nine people and one horse`；`mkspec` 的 only 句加上 `and the one horse tied at the post`，`HORSE_SH` 加 s32（第 4 張圖）。PREP、FOOT「馬在畫面裡的鏡」也加 s32 |

## 建議

| # | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 1 | s01 | 一鏡裡寫了四個小動作：拿起濕布、在水盆裡沾濕、擰乾、再蓋回去，水盆還在前景地上，6 秒裡模型常常只做一半 | 拍法 32 | 第一格寫成 `his right hand already holding the folded damp cloth, freshly wrung, just above her forehead`，動作只留 `he lays the cloth gently across her forehead and smooths it down with his palm as he speaks`；水盆照舊放在前景 |
| 2 | s22 | 「the horse's forelegs lift off the paving」是半人立。人立的馬腿和騎馬的人最容易變形，也很接近第 41 條要避開的那類鏡頭 | 聖經第 41 條 | 改成 `the horse tosses its head and stamps its forefeet on the spot, snorting, all four hooves staying on the paving, while A-ling holds the reins tight` |
| 3 | s18 | 唐小棠背影在正中、腰以上，而院門在 `-zhong` 的中偏左，她會擋住門洞和馬；門洞左半只有約 60 px 寬，馬穿不過去 | 拍法 41（人與馬不重疊）、29 | 景別改成全景從背後拍：`wide shot from behind`，她 `framed full figure, small, in the lower middle of the frame`，門和馬在她頭頂上方看得到。動作改成 `the horse bursts out through the gateway, its shoulder knocking the half-swung slatted gate leaf back against the wall`（第 37 集審稿列過這個選項），門扇就不會擋住 |
| 4 | s27b | 隊長 s27 在柵後，s27b 第一格卻在「on the paving at the right」（柵外） | 接戲 | 改成 `on the paving just behind the near end of the barrier, at the left of the frame, the guard captain … already sprawled …`（必改 6 若走付費版，照新圖寫成「柵的城門那一側」） |
| 5 | s10 s11 | 背景句跟送的裁切對不上。s10 寫「that side of the frame is only the shut plank door and the cracked plaster wall」，送的卻是 `-xi-chuang`（床尾、窗、桌角）；s11 寫「behind him, soft, only the plaster wall」，送的 `-xi-zhen` 前景是桌面、紙包和熄了的蠟燭 | 拍法 19、35 | s10：`off('left', 'the cracked plaster wall and the foot of the bed')`。s11：背景改成 `only the pillow end of the bed and the plaster wall`，或改送必改 1 新做的、不含桌面的裁切 |
| 6 | s33 s36 | 送的 `-men` 左邊就是那根拴馬樁，文字沒寫馬。近景與越過弩看過去的鏡，背景是虛的，觀眾不太會追 | 接戲 | s36：`at the left, soft and dark beyond the crossbow, the hindquarters of the horse tied at the post`，可以不送馬圖；s33 背景虛焦，照舊也可以 |
| 7 | s19（a20） | 錄音裡小禾的「哥……」是 277 Hz，緊接在 s18 唐小棠 281 Hz 後面，兩句只差 0.2 個半音，又在稿子的同一場（第一場）。這組 PREP §4 沒列到；而且聖經寫小禾說話在 300–360 Hz，277 偏低 | 拍法 43；聖經〈人物〉小禾 | 用 `rubberband=pitch=1.22:formant=preserved` 調成約 338 Hz，跟 281 差約 3.2 個半音，也回到她的音域；調完人耳聽氣音像不像（這一句 whisper 解不準，PREP 已記「要人耳聽」） |
| 8 | s26 → s28（a25-p85 → a26） | 隊長 s26 為了跟阿令拉開，降到 149 Hz，隔一鏡 s28 是 213 Hz：同一個人前後差約 6 個半音 | 拍法 43（同一個人要像同一個人） | 剪接時聽一次；不像同一個人的話，把 a26 稍微降一點（`pitch=0.92`，約 196 Hz），s28 跟 s30 阿令 270 Hz 仍差約 5.5 個半音 |
| 9 | 全集的 `HORSE`／`HORSE_SENT` | 馬圖的轡頭是**黑色**（英式水勒、有鼻革），文字寫「plain brown leather bridle」，兩者不一致 | 拍法 19 | `HORSE` 與 `HORSE_SENT` 改寫成 `a plain dark leather bridle`（聖經〈道具〉「素皮轡頭」不寫顏色，可以這樣改） |
| 10 | s02 s04 s07 | 白天那張雙丸子背影圖是**藍天加兩棟屋**，送進室內鏡。s02 共送 4 張圖，這張佔四分之一的份量，可能讓窗外變藍天，或背景長出屋子 | 拍法 8、19；第 37 集建議 1 | 先看 d1。發生的話（站主指定的檔，要協調者同意）免費做一張室內版：藍天（b > r+60）換成灰白的土牆色、屋子壓暗加模糊，新 id，句子不變 |
| 11 | s01–s11（`-chen`、`-xi`） | 右牆靠蠟燭那一帶還留著一片橘光；熄掉的蠟燭頂上有一團灰白光暈（`-chen-zhen`、`-xi-zhen` 上很明顯）。模型可能在白天把蠟燭點亮。房門的圓門把是現代的樣式（第 3 篇章起這間房一直是這樣） | 拍法 19 | 先看 d1。蠟燭被點亮的話，免費把光暈那一塊用旁邊的牆色柔邊蓋掉（新 id）；門把接受 |
| 12 | BUY | 實測 s12 4.34 秒、s13 4.01、s18 4.16、s23 4.83，6 秒（可放約 5.9 秒）都放得下。四鏡改成 6 秒，可以省 16 秒，約 0.8 CU | 聖經〈每集鏡數〉 | 品質優先，可以不改；點數吃緊再改（`e938d1.sh` 的支數與秒數要一起改） |
| 13 | s29 | 「already reined in from the first frame」和「before the horse has quite stopped」互相矛盾 | 拍法 32 | 改成 `already slowing to a halt from the first frame` |
| 14 | 聖經〈場景〉、〈拍法〉第 42 條 | 「白大夫坐床頭（右）、阿令坐床尾的矮凳（左）」也撞上必改 1 的桌子 | 第 39 集前置 | 必改 1 走 A，第 39 集就照新圖寫；走 B 的話，第 39 集的床頭改成在左，聖經第 42 條要跟著改 |

## 不用改的（看過、接受）

| 項目 | 為什麼 |
| --- | --- |
| 接點 37→38 的人物狀態 | 舊灰外衣、袍子下半截有石灰白粉、小禾滿臉通紅、草兔子從腰間換到枕邊，跟第 37 集最後一鏡一致 |
| 小禾一直在床上（原版必修） | 床入鏡的 s01、s03、s04、s05、s07、s08、s19 都寫了她；s02 改送床那張圖以後，也要寫她（已併入必改 2） |
| 秦霜 | 柴刀全集不寫；長槍沒有紅纓，s09、s12、s16、s17 都加送道具圖；s09 長槍第一格就跟她分開；「臉上沾灰」不寫細點（拍法 12） |
| 阿令 | 騎馬的樣子（布條紮袖口、綁腿、灰布長腰帶）從 s13 開始；馬鞭從 s14 在手、s16 起插在腰帶；第二、三場寫幾縷髮絲散出來，髻和木簪照圖；沒有短刀、沒有面巾 |
| 騎馬鏡的景別（第 41 條） | s20、s22、s27、s27b、s29 全景；s21、s25 腰以上加馬頭頸；s18 側後（見建議 3）；s30 馬是拴著的，在畫左、拴在方石樁上、跟她分開；一鏡一匹馬，只寫 `one … horse`，馬鞍寫在文字裡（馬圖上沒有鞍） |
| 去程右往左 | s21、s22、s25、s27、s27b 都是馬頭朝左；s20 見必改 4；第三場在城裡，方向照醫館那張圖，可以 |
| 守軍與弩手 | 年輕守軍只拍側後、放錄音；弩手同一身黑甲、遠、小、臉在盔影裡；只有一支舉著的火把，拿在一個人手上；城門兩支火把都寫「fixed upright in an iron holder, nobody holding them」（拍法 23、37） |
| 不掛東西（拍法 33） | 稿子的石碑、告示板、空白招牌全都拿掉了；四張母圖上也沒有 |
| 系統（拍法 11） | s11、s15 的淡藍光不寫，面板剪接時疊上，字跟系統念的一字不差 |
| 錄音 | 33 句逐字照稿；重錄 3 句、變調 6 句；守軍隊長、年輕守軍、白大夫第一次量的數字已經補進聖經 |
| 精修開頭（`heads938.py`） | 單獨拍隊長的鏡和過肩的 s12、s14，精修開頭另外處理，PREP §3 有寫 |

## 小結

- **必改 8 項**：
  1. 病房的小桌擋在枕頭那頭的床前，許硯跪、坐、靠的位置都撞上桌子。建議花約 0.5–1 CU 用 Qwen 把桌子移到右牆（第 39 集也能用）；不花錢的退路是把小禾的頭改到床的左端。
  2. s02 送了門那張裁切，人等於朝門走：改送床那張。
  3. s09、s12 圖上的房門是關著的：改寫成關著，門外的阿令改站在門內門邊。
  4. s20 官道的路是往遠處退進去的：重裁、改寫成沿著楊樹腳那條土路由右往左。
  5. 城門拱洞裡兩扇大門都關著，半開的是旁邊的小門：`GATE` 等七鏡改寫。
  6. 拒馬柵貼著牆沒有擋路，片名那一跳沒有理由：建議 d1 前花約 0.5–1 CU 用 Qwen 把柵移到路上；不花錢的話，要協調者決定接受。
  7. s27 動作句把起跳寫進去了：改成剪在離柵還有兩步的時候。
  8. s32 全景裡拴著的馬不見了：補上馬，加送馬圖。

  除了 1 和 6，都是改字或免費重裁。
- **建議 14 項**，都是免費或先看 d1 再說：s01 動作太多、s22 半人立、s18 門洞被擋、s27b 隊長的位置、s10 與 s11 背景句、s33 與 s36 的馬、a20 小禾音高（跟唐小棠只差 0.2 個半音）、隊長前後音高、轡頭顏色、白天的雙丸子背影圖送進室內、蠟燭光暈、BUY 可以省的秒數、s29 用字、第 39 集病房站位。
- **站主 11-21～23 的規則**都做到了：風格句、許硯不寫鬍渣、only 句兩次、柴刀、唐小棠背影加髮型圖、跪姿拍到膝蓋、不掛東西、精修文字沒漏進 d1。門的開關有三處寫錯或漏寫（必改 2、3、5）。同場相鄰說話者有一組沒列到（建議 7）。
- **接點 37→38 接得上**，問題在圖上的桌子（必改 1）。**BUY** 照實測 33 句全部放得下。
- 改完 `r2.py`、`mkspec.py`、`check938.py`、`roads_e938.sh`／`xujia_tangfang_e938.sh`（都用新 id）以後，重跑 `build938.sh`、`prep938.sh`、`DRY=1 e938d1.sh`。必改 1、6 若走付費版，先跑 Qwen（約 1–2 CU）、挑好圖，再重裁、重跑。
