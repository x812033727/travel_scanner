# 第 39 集重製版 r2（e039-r2，內部 939）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿人：沒參與寫稿的獨立代理，2026-11-24，開拍前（d1 還沒跑；**錄音 0／40**，`audio/` 是空的）。只寫了這一個檔；沒改 `r2.py`、`mkspec.py`、`check939.py` 或任何別的檔，沒開 Colab／RunPod，
  沒用站台 TTS，沒付費生圖，沒 commit、沒 push。沒讀寫稿者的自審 `writer-tools/e039-r2/review.md`。
- 審的對象：`writer-tools/e039-r2/r2.py`（只看到需要對照的段落：`off()`、各鏡 `comp`、`BUY`、`GAZE_REFINE`）、`docs/videos/zhong-tian-qu-qi-e039-r2/{script.md,storyboard.md,video.json,overlays.json}`、
  d1 提示詞 `~/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live/d1/prompts/*.txt`（84 支，42 鏡逐鏡讀完種子 9391101，兩種子比對過）與 `colab-jobs.json`（逐鏡送圖）、
  `colab/runs/e939-live/{mkspec.py,spec.json,PREP.md}`、`colab/runs/e939/extras.json`、`hailuo/clips-dh-e939.json`、`live-action/free-e031-e040/{xujia_tangfang_e939.sh,gucang_wai_e939.sh}`（也對照 `kong_e938.sh` 的裁切框）、
  scratchpad `e939prep/{prep939.sh,check939.py,prep939.log,lines-table.md}`。
- 對照的文件：`r2-bible-e031-e040.md`（拍法 1–43，〈接點〉38→39 與 39→40，〈道具〉〈人物〉〈小角色〉〈場景〉〈原版必修〉第 38、39 集；第 41、33、42、34 條逐句看過）、任務檔第 33–38 集的教訓
  （「第 38 集送上後台」的配鞍馬圖 `prop-zaohongma-an-l1`）、`OWNER-CHECK-20261122.md`、第 38 集 `colab/runs/e938-live/{PREP.md,cut-review.md,cut-review-2.md,cut-review-3.md,fix5/plan.md,fix6/plan.md}`、
  第 38 集 `review-independent.md`（格式照它）。
- 參考圖都開全尺寸看過：東街 `set-yiguan-men-ye-l1`、`-men`、`-jie`；官道 `set-guandao-ye-l1`、`-shu`；病房 `set-xujia-tangfang-kong-l1`、`-kong-chen-l1` 與六張裁切 `-kong-{chuang,men,zhen}`、`-kong-chen-{chuang,men,zhen}`、本集的 `-kong-bei`；
  穀倉前 `set-gucang-wai-l1` 與本集的 `-men`、`-tian`、`-qiang`；`prop-zaohongma-an-l1`、`duizhang-portrait-l1`、`prop-changqiang-l1`、`baidaifu-`／`hanbo-`／`qianyuanwai-`（加 `angle-a`）／`diaoqi-`／`erniu-portrait-l1`。
  放大拼圖放在 scratchpad `e939rev/`（審完已刪）。
- 接點：我自己從第 38 集定版成片 `e938-live.mp4`（188.43 秒）抽 172.4 秒到片尾，每秒一格拼成 4×4。看到的：隊長右手短刀平指 → 阿令背影兩手按著門板、門板關著、**畫左緣露出拴著的棗紅馬頭頸**、前景一把端平的弩 → 隊長中景、短刀垂在身側 → 隊長**右手**舉過頭頂吼「放——」。
- 語速：錄音還沒有（PREP §4b：站台 429），只能照 PREP §4 的估法核（見〈機械檢查〉最後兩列與建議 14）。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| d1 清單 | 84 支、538 秒（5 秒 6、6 秒 58、8 秒 20），一個種子 269 秒，跟 `r2.py` 的 `BUY` 逐鏡相符；84 支的 `prompt_sha256` 我重算都相符，送的圖都存在；兩個種子的提示詞除了種子號一字不差（抽 s17 diff）；s36 的 `<Picture 5>` 等於送圖張數 |
| 分隔句 | 每支剛好一次 `never the mood. `、一次 `One continuous shot.`；d1 裡沒有 `as the first frame`、`3D CG`（拍法 39） |
| 風格句與許硯 | 84 支都有「with the look of a feature film」，`cinema camera` 0；`stubble` 0 |
| 唐小棠 | `Tang Xiaotang` 0，沒送她的任何圖，本集不入鏡（照稿子：灶房看火） |
| 跪姿 | 跪著的只有刁七 s36、s39，兩鏡都是 `framed full figure with both knees on the ground`；s40 近景不寫跪；病房許硯一律坐床沿或站 |
| 柴刀、兵器 | `chopper`、`sword`、`blade`、`saber`、`dagger` 0；長槍只在 s34、s36、s39（加送 `prop-changqiang-l1`）；隊長的短刀只在 s03（已在鞘裡）；弩只在第一場 |
| 掛著的東西（拍法 33） | `lantern`、`sign`、`plaque`、`banner`、`milestone`、`tablet`、`hook` 0；白大夫是左手一盞陶油燈（s01–s05），s07 放在門檻上；s13 不寫石碑；四張母圖上沒有招牌、燈籠、石碑 |
| 會長字或會畫錯的字 | `open`、`fog`、`mist`、`smoke`、`mud`、`crowd`、`villagers`、`hundreds`、`leap`、`jump`、`deep pool` 0；`saddle` 只出現在 `felt saddle pad`（10 次，照配鞍馬圖） |
| 配鞍馬（任務檔「第 38 集送上後台」） | 馬在畫面裡的 s08 s09 s10 s11 s13 都把 `prop-zaohongma-an-l1` 加在最後一張，文字寫「a folded dark grey-brown felt saddle pad girthed with rope」、加圖句「exactly its folded … felt saddle pad and rope girth as the picture shows them」；我看圖：灰褐毛氈墊、毛邊、腹下一條繩，**沒有鐙、沒有高鞍頭**，對得上 |
| 第 41 條 | s08 s10 s11 側面腰以上加馬頭頸，s09 s13 全景；s08–s13 的 zh 都寫兩人在馬上；去程不在本集，回程 s08–s11 都寫 `head toward the right`／`toward the right`，`check939.py` 擋 `from right to left`。**例外見必改 3**（s11、s12） |
| 病房圖文 | 夜 `-kong`／天亮 `-kong-chen` 都沒有桌子，床尾左前一張矮凳加一根白蠟燭；s17 舉的是凳上那根蠟燭，s20 起「the one small flame on the low stool」，s24 起寫熄著；阿令坐床尾床沿（s22 s23 s26）、矮凳在她身邊：跟圖一致 |
| 穀倉前格局 | 穀倉在右、兩扇有 Z 字撐的門板貼在正面兩側、黑門洞、門前踩實的土地、左半水田青秧、遠處乾田、村屋、山：s36 照圖寫對了（聖經〈場景〉試鏡表寫「一扇門開著」，寫稿者照圖改成兩扇，對） |
| 人數 | s01 二、s02 九、s03 三、s04 二、s08 二人一馬、s09 十人一馬、s10 s13 二人一馬、s14 二、s16 二、s17 三、s20 三、s23 二、s30 三、s35 三、s36 十（刁七、鐵鏽紅衣拉繩的年輕人、村民甲、五個村民、二牛、秦霜，每人一種衣色）、s37 三：`exactly N` 都跟描述對得上，`Only…` 句再寫一次；單人鏡寫 `is the only person` 加 `No second copy of anyone appears`（同第 38 集）。**例外見必改 5**（s38、s39） |
| 笑 | 有臉的鏡幾乎都逐部位寫 `not smiling`；s24 稿子允許「最後可以笑一下」；s40 冷笑是稿子要的。漏的是 s30 的許硯（建議 6） |
| 精修文字 | `clips-dh-e939.json` 42 筆，沒有 `Tang Xiaotang`、`cinema camera`、`deep pool`；s02 寫了 `keeps the back of his head toward us the whole shot`（開頭仍點名、說 face，見建議 12） |
| 光線與時間 | 第一場冷藍月光加門裡暖光、遠處一支舉著的火把（拍法 37）；官道只有月光；病房夜只有凳上一朵燭火、天亮灰白；穀倉前低低的暖金斜光；插鏡 s19 不寫地點、第一格就是藥箱與碗（拍法 10、35） |
| 面板 | `overlays.json` 三鏡（s25 任務完成、s28 好感 +12 → 44、s28b 兩行）跟系統念的一致（+12 → 44 是本系列好感面板的固定寫法） |
| 檢查工具 | `prep939.log`：st1／d1 preflight 與 `check_manifest` 0／0；否定名詞、舊寫法、容易長字的名詞、掛著的東西都是 0 |
| BUY（照 PREP §4 估） | 估下來都放得下；最緊的是 s32 小禾 16 字（6 秒）與 s19、s21 白大夫 14 字（6 秒），見建議 14。錄音後一定要照 `span939-buy.txt` 重核 |

## 寫稿者的決定：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| 接點 38→39 | 第 38 集最後是隊長右手高舉「放——」切黑；s01 同一刻、門板已往裡推開、白大夫跨出門檻、阿令讓到門左邊上一級石階；s02 隊長右手第一格還舉著：**接得上**。兩個小差：第 38 集阿令身邊（畫左）看得到拴著的馬，s01–s07 都沒寫馬（建議 13）；第 38 集弩手就在她背後幾步，s02 寫成「far up the street, small」，距離拉遠了，可以接受 | 接受；建議 13 |
| s02 稿子的過肩改成從背後拍白大夫（`nospeak`、送定妝照） | 從背後拍、不點名過肩前景，照拍法 2，對；`the back of his head toward us the whole shot` 也寫了。但這不完全是「唐小棠背影的做法」：她的背影鏡是**拿掉臉部圖、加髮型背影圖**，這裡送的是正臉定妝照，8 秒裡他回頭露臉的機率不小 | 接受，先看 d1；建議 12 |
| s07 油燈放在門檻上（不掛鉤子） | 照拍法 33，對；放下的動作在第一格前完成，油燈從此不入鏡，交代清楚 | 接受 |
| s09 跟拍改慢推 | 跟拍會把街轉掉，改慢推對。但 `set-yiguan-men-ye-l1` 的街是從畫面中間偏左的遠處斜著退到右下近處，「head toward the right … gallops toward the right edge」照圖其實是**朝鏡頭右下角衝出來**，不是側面橫過；另外拴馬樁在圖上是中偏右（x≈718–758），不是「right foreground」，石階只有一級 | 接受；建議 2 |
| s13 不寫坡與村子、路的盡頭一盞小燈 | 照圖（官道整張是一條直直退到消失點的路，兩排楊樹在遠處左右橫過、路從中間穿過），不寫石碑，對；從背後往遠處走的全景是側後，畫面方向中性，可以接受。動作寫了三段（一指、回頭、再催馬） | 接受；建議 8 |
| s17 舉的是凳上那根蠟燭 | 圖上唯一的光源，對；s18 那朵燭火卻沒人拿（見建議 4） | 接受 |
| s19 用木湯匙攪藥 | 拍法 32，對；`lid lifted` 不寫 open，對 | 接受 |
| s22 阿令坐床尾的床沿（矮凳上有蠟燭） | 照圖，對 | 接受 |
| s28b、s29b 拆鏡 | s28 兩句系統 28 字確實放不進一支 8 秒；s29 系統 15 字加心裡話 15 字也放不進 8 秒。拆鏡換景別（近景／中近景），接受。但 s28b、s29b 跟 s28、s29 的背景都是有床的圖，床上沒寫小禾（必改 4） | 接受；必改 4 |
| s35 阿令不寫（一鏡最多三張臉） | 拍法 1，對；`-kong-chen-chuang` 床尾左端在框外，她站在框外說得通 | 接受 |
| s36 許硯不入鏡 | 二牛、秦霜、刁七已三張臉，對；39→40 他在第 40 集第一鏡入鏡 | 接受 |
| **醫館門板推開只寫在文字（圖是關的；付費改圖列 PREP §5、沒做）** | `set-yiguan-men-ye-men-l1` 上兩扇門板整片關著、門閂在中間。s01、s04、s05、s07 寫「both plank leaves pushed inward … warm lamplight in the doorway」，s08 又寫「the shut plank shopfronts behind」而送的是同一扇門的圖。這就是第 38 集必改 3 的同一類問題（圖關、字開），而 s01 是接點、門開是這一場的拍點 | **不接受**；必改 1 |
| 房門（寫稿者沒列） | `-kong-men`、`-kong-chen-men` 上房門是整片關著的木板門。s15 寫 shut（對），**s16 寫 `standing ajar behind them`、s34 寫 `already pushed inward against the wall`**，跟圖相反；s22、s23、s26 圖上有門卻沒寫開關 | 必改 2 |
| s08–s13 兩人一馬（原版必修） | s08 s09 s10 s13 照第 41 條寫齊（兩人、腰帶繞兩圈、抱腰、藥箱、配鞍馬圖）。**s11 沒寫腰帶；s12 沒有馬、沒有腰帶，構圖在馬上不成立** | 必改 3 |
| 病房「床在畫面就寫小禾」 | zh 列的 s14 s17 s18 s20 s24 s30 s35 都寫了她。但另外十鏡送的圖裡床、枕頭就在人背後，文字卻寫「behind him only the window／the pink quilt／the bed head」，床會是空的 | 必改 4 |
| s14 濕布 | 許硯手上一塊、小禾額頭上又寫一塊：第 38 集 cut-review-2「濕布兩條」的老問題 | 必改 6 |
| BUY：長句、慢的老人、喘的句子一律 8 秒 | 方向對；錄音後重核 | 接受；建議 14 |
| 圖：本集免費新做的 4 張 | `-kong-bei`（空床的粉被與床欄，插鏡只當背景，可以）、`-men`、`-tian` 可以；`-qiang` 是穀倉山牆頂加天空與黃柳，放在跪著的刁七背後要寫仰角（建議 10） | 接受；建議 10 |
| 白大夫的定妝照 | 圖上是米白**立領盤扣的絎棉短襖**，文字寫「moon-white old long gown under a plain quilted cotton vest」，s07 還寫「vest now done up」。圖壓過字，畫面會照圖，不會壞片；只是 s07 那句沒有對應 | 接受；建議 11 |

## 必改

| # | 鏡 | 問題與證據 | 依據 | 具體改法 |
| --- | --- | --- | --- | --- |
| 1 | s01 s04 s05 s07（s08 跟著改） | **醫館門板：圖關、字開**。`set-yiguan-men-ye-men-l1` 兩扇門板整片關著；s01「both plank leaves already pushed inward from the first frame, warm lamplight glowing in the dark doorway」、s04「both plank leaves standing pushed inward with warm lamplight in the doorway」、s05「behind him, soft, only the plank leaves pushed inward and the warm lamplight」、s07「in the doorway … both plank leaves standing pushed inward」。模型照圖會把門畫成關的（白大夫從關著的門板前「跨出門檻」），照字會在門上自己挖一個門洞；s08 送同一張圖、寫「the shut plank shopfronts behind」，等於 s07 開、s08 關。s01 是接點，「門開了」是第 38 集切黑後的第一個拍點 | 拍法 19、29（參考圖壓過文字）；第 38 集必改 3、第 35 集 fix3「門關」；站主「門寫明開關」 | **A（建議，要花錢約 1 CU，d1 前做，協調者定）**：照 PREP §5-1，Qwen 用 `set-yiguan-men-ye-men-l1` 當底圖，照 e938 qwen step3「加東西做得好」只改一件事：`the two plank leaves of the middle door now stand pushed inward into a dark room, a warm orange oil-lamp glow spilling out of the doorway onto the stone step; the stone hitching post, the step, the paving, the other doors and the moonlight stay exactly the same`，兩個種子，存成新 id `set-yiguan-men-ye-kai-l1`，s01 s04 s05 s07 s08 改送它；s08 的「the shut plank shopfronts behind」改成 `behind them, soft, the warm glow of the clinic doorway`。比起 d1 後重拍四到五鏡（8–10 支加精修），這一張圖便宜。**B（不花錢）**：保留 s01 原樣當開門那一下（只有這一鏡賭）；s04 s05 s07 改成門洞在畫緣：s04 `the doorway at the right edge of the frame, warm lamplight spilling from it onto the step`，s05 背景改成 `behind him, soft, only the dark planks of the shopfront and a warm glow from the right edge`，s07 `standing on the top step at the right edge of the doorway`；s08 拿掉「shut」改成 `behind them, soft, the dark planks of the shopfronts and a warm glow at the right edge`。走 B 的話 `check939.py` 第 202 行斷言跟著改 |
| 2 | s16 s34（s22 s23 s26 補寫） | **房門：圖上關著，s16 寫半掩、s34 寫推開到牆**。`-kong-men`、`-kong-chen-men` 左邊是整片木板門、門把在右緣、門框裡沒有縫。s16「the plank door standing ajar behind them」、s34「the plank door already pushed inward against the wall from the first frame; in the doorway, Qin Shuang … already stopped on the threshold」：秦霜要站在門檻上，圖上那裡是一片關著的門板。s22、s23、s26 圖上有門卻沒寫開關。第 38 集必改 3 的同一個問題、同一扇門 | 拍法 19；第 38 集必改 3；站主「門寫明開關」 | 照第 38 集必改 3 的改法（不花錢）：s16 `the plank door standing ajar behind them;` → `the plank door at the left shut behind them;`。s34 `the plank door already pushed inward against the wall from the first frame; in the doorway, Qin Shuang …, already stopped on the threshold from the first frame, out of breath, … her left hand gripping the door frame` → `just inside the shut plank door at the left, Qin Shuang …, already one step into the room from the first frame, out of breath, …, her left hand pressed flat on the shut plank door behind her`；動作 `braces herself in the doorway with her hand on the frame and leans in toward the room` → `pushes off from the door with her left hand and leans in toward the room`。s22、s23、s26 的背景加 `the plank door at the left shut`。`check939.py` 第 203–204 行改成斷言 `shut`。若必改 1 走 A，同一輪也可以順便做 `-kong-chen` 的開門版，但「秦霜衝進來」用關著的門也演得出來，不必花這筆 |
| 3 | s11 s12 | **兩人一馬有兩鏡沒寫齊**。s11：寫了「the old man tied on behind her … his two hands gripping her waist」，**沒有腰帶**（只剩 identity 裡「tailored close at the waist with a cloth sash」）。s12：**整支沒有馬、沒有腰帶**（`horse` 0 次、`sash` 0 次），而且構圖不成立：「in the lower left foreground … only the back of a young woman's head … toward us; beyond it, just behind her shoulder, Doctor Bai … his chin pressed against the back of her shoulder」：兩人同向坐在馬上、他在她後面，能看到她後腦的機位一定在他身後，看不到他的臉；看得到他臉的機位一定在她前面，看到的是她的臉。模型多半會把他畫到她前面、或兩人面對面、或站在地上 | 聖經第 41 條（兩人一馬每鏡都在馬上、腰帶寫在第一格、腰以上加馬頭頸）；原版必修第 39 集「白大夫從馬背上消失」；拍法 2 | s11：在「behind her shoulder, close and soft, …」之後加 `her long grey cloth sash wound twice round both their waists and knotted at her front`。s12 改成側面中近景（不送她的圖照舊，只露半邊後腦與肩）：`medium close-up riding alongside, side-on, framed from the chest up with the top of the horse's red-brown mane bobbing at the bottom right corner: at the right edge, cut by it and soft, only the shoulder and the back of the pinned-up head of the young woman riding in front, turned forward toward the right; just behind her, Doctor Bai … tied on behind her with her long grey cloth sash wound round both their waists, his chin pressed against the back of her shoulder, his face three-quarter toward us, the strap of the medicine chest across his chest, his eyes shut tight from the first frame`；only 句改成 `Besides him, only the shoulder and the back of the head of the young woman in front at the right edge, and the top of the one horse's mane, are in the frame`；加送 `prop-zaohongma-an-l1` 與馬圖句（`HORSE_SH`、`HORSEPIC` 加 s12），`GAZE_REFINE` s12 照新構圖改。`check939.py` 第 170 行的 `TWO_UP_SH` 斷言加一條：s08–s13 每鏡都要有 `sash wound` |
| 4 | s15 s21 s25 s27 s28 s28b s29 s29b s31 s33 | **床在畫面裡、文字沒寫小禾，床會是空的**。這十鏡送的裁切都有床：夜 `-kong-chuang`（s15 s21）、天亮 `-kong-chen-chuang`（s25 s27 s28b s29 s33）、`-kong-chen-zhen`（**枕頭就在畫面中間**，s28 s29b s31）。文字卻寫「behind him, soft, only the dark blue window and the plaster wall」（s15）、「only the dark wooden bed head and the grey plaster wall」（s28）、「the pink quilt and the small window」（s27 s28b）、s31「that side of the frame is only the pink quilt and the dark wooden bed head」（那一側正是小禾）、s21 白大夫坐在枕頭那頭的床沿，「that side … only the pink quilt」。模型照圖畫出床與枕頭、照字不放人，就是一張空床、一顆空枕頭 | 原版必修第 38 集「小禾從床上消失兩次」、第 39 集「白大夫進門時床是空的」；第 38 集 cut-review-2 必修 M1（s09 s10 s13 床上沒有小禾）；聖經〈原版必修〉「床在畫面裡的鏡就寫她」 | **A（不花錢，建議）**：近景不要床。從 `-kong-l1`／`-kong-chen-l1` 免費裁兩張只有窗與牆的新圖：`set-xujia-tangfang-kong-chuang2-l1`／`-kong-chen-chuang2-l1` = `crop=560:315:620:60`（窗與後牆，床欄與粉褥都在框外），`-kong-qiang-l1`／`-kong-chen-qiang-l1` = `crop=480:270:820:100`（窗的右半與枕頭上方的牆，枕頭在框外）；加進 `xujia_tangfang_e939.sh` 與 refs README。s15 s21 s25 s29 s33 改送 `-chuang2`，s28 s29b s31 改送 `-qiang`，文字的「behind him, soft, only the … window and the plaster wall」就跟圖一致；s31 的 off 句改成 `that side of the frame is only the grey plaster wall all the way to the edge`，s21 改成 `that side of the frame is only the dark plaster wall`。**中景、中近景的 s27、s28b 床一定在框裡**，寫她：s27 `behind him, soft, little Xiaohe asleep in the bed under the pink quilted cover, her face its own healthy colour, her eyes shut, her lips closed, and the small window glowing grey-white`，s28b 同句；兩鏡加送 `xiaohe-portrait-l1`、人數改 `exactly three people`（s27 含前景的後腦）／`exactly two people`（s28b），only 句照改。**B**：十鏡都照 A 的句子把小禾寫進背景、加送她的圖（較多改動，也多一張臉的風險） |
| 5 | s38 s39 | **同一支提示詞裡人數互相矛盾**。s38：「…and he is the only person in the frame; …exactly three people, the two at the edges seen only from behind and the side」；s39：「…and she is the only person in the frame; …behind her at the right, Diao Qi … kneeling…; exactly two people. Only these 2 people are in the frame」。是 `r2.py` 的 `off()`（第 250–254 行）固定加「is the only person in the frame」，用在有別人入鏡的鏡就自相矛盾；s38 還寫「that side of the frame is only the trampled earth and the grey plank wall of the barn」，送的 `-tian` 右邊是遠田、村屋與一角水田，沒有穀倉 | 一定要查「人數與 exactly N 對得上」；拍法 31；拍法 19 | `off()` 加一個參數讓它不加 only 句，或這兩鏡改寫：s38 `that side of the frame is only the far ploughed fields and the edge of the rice field all the way to the edge, and the only face seen whole is his`；s39 `that side of the frame is only the trampled earth and the green rice field all the way to the edge, and no one else stands on that side`（只描述那一側，不說全畫面只有一人）。`check939.py` 加一條斷言：同一支不能同時有 `is the only person in the frame` 與 `exactly (two\|three\|…) people` |
| 6 | s14 | **兩塊濕布**。許硯「one folded damp white cloth, freshly wrung, already in his right hand just above her forehead … lays the damp cloth gently across her forehead」，同一支裡小禾又是「a folded damp white cloth on her forehead」。第 38 集 cut-review-2 列過「濕布兩條」 | 第 38 集 cut-review-2（s01 濕布兩條）；拍法 32 | s14 小禾那句改成 `along the bottom of the frame, little Xiaohe, eight years old, lying in the bed under the pink quilted cover, her face flushed deep red, her forehead bare and damp with sweat, her eyes shut, her lips closed`；s17 起照舊（布已經蓋上） |

## 建議

| # | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 1 | s08 s09 s10 s11 s13（必改 3 後加 s12） | 配鞍馬圖 `prop-zaohongma-an-l1` 的馬**頭朝左**；本集回程一律馬頭朝右。第 38 集去程朝左剛好跟圖同向，這次反過來，H3 有照參考圖方向畫的傾向（第 38 集 s20 已經吃過方向的虧） | 聖經第 41 條（回程一律由左往右）；拍法 9 只限交領的人，馬沒有這個問題 | 免費做水平翻轉版 `prop-zaohongma-an-fx-l1`（`ffmpeg -vf hflip`，轡頭、毛氈墊、繩肚帶左右對稱、沒有字），這五（六）鏡改送它；refs README 記一句 |
| 2 | s09 | 整張東街的街是往畫面中偏左遠處退進去的，醫館在右邊近處；「side-on with its head toward the right … gallops toward the right edge」照圖是朝鏡頭的右下角衝出來。拴馬樁寫成「soft in the right foreground」，圖上在中偏右（x≈718–758）；「two stone steps」圖上只有一級（s01–s07 的「top step」「lower step」也一樣） | 拍法 19、29 | 動作改成 `the horse lunges off from the step and gallops down the street along the foot of the shopfronts toward us and out past the lower right corner of the frame, the stone paving ringing`，拿掉 `side-on`；樁改成 `the square stone hitching post just left of the nearest door`；全集「two stone steps」改 `one wide low stone step`，「top step／lower step」改 `the stone step`／`the paving below the step` |
| 3 | s08 | （必改 1 走 B 時）s07 門開、s08 背後同一扇門寫成關的 | 接戲 | 見必改 1 的 B |
| 4 | s18 | 燈光句「the one small candle flame held up beside the bed」、構圖「the small warm candle flame soft at the edge of the frame」，畫面裡沒有人拿它（許硯不入鏡）：模型會在畫緣長出一隻手或半個人，或讓蠟燭飄著 | 拍法 31 | 燈光句改成 `warm candlelight from beyond the left edge of the frame the only warm light`，構圖那句改成 `the warm candlelight falling on them from the left` |
| 5 | s27 | s26 阿令坐在床尾床沿、臉朝鏡頭右；s27 是「back of a young woman's head … toward us」的過肩，背景卻是正對後牆的 `-kong-chen-chuang`（窗、床）：坐在床沿的人不可能背對一台看得到窗的攝影機，模型會把她挪到床前、背對床，兩鏡之間她換了位置 | 接戲；拍法 29 | 改成單人近景 `off('left', 'the foot of the bed and the grey plaster wall')`，「the young woman at the left edge draws the coat tighter」交給 s26；或保留過肩、改送 `-kong-chen-men`（床尾那一角）讓她背對鏡頭坐在床尾、許硯在畫右遠一點。必改 4 的小禾句照加 |
| 6 | s30 | 許硯沒寫 `not smiling`，動作句還寫「and Xu Yan's smile is gone」：等於叫他第一格在笑。原版必修的「the smile gone」是 s31 的事 | 拍法 14、預設不笑 | 許硯那句加 `not smiling, brows drawing together`；動作句的 `and Xu Yan's smile is gone` 改成 `and Xu Yan goes still` |
| 7 | s28 | 第一格「his eyes already turned to the empty air before him」，動作又是「turns his head back from the left」：第一格已經轉好了還要轉 | 拍法 32 | 第一格改成 `his face still turned three-quarter to screen left toward the foot of the bed from the first frame`，動作改成 `turns his head back to the front and one of his brows lifts slowly` |
| 8 | s13 s35 | 一鏡三段動作。s13：平掌一指、回頭說話、「then drives the horse on down the road」；s35：雙手抱拳、一拜、轉身往門 | 拍法 32 | s13 拿掉 `then drives the horse on down the road`（馬本來就在走）；s35 第一格寫 `both hands already raised before his chest, one cupped over the other, from the first frame`，動作留 `bows once to the old man and turns away toward the door at the left`（剪點照舊剪在轉身的一半） |
| 9 | s36 | (1) 「the dry grass of the field bank soft in the lower left foreground」：圖的左下前景是水田的水與秧，沒有田埂草；(2) 十個人站在「the edge of the rice field」，踩實的土地在圖上只是右下一塊楔形，模型可能讓人站進水裡；(3) 「a stout man in dark olive green」沒寫年紀；(4) 韓伯、錢員外在全景裡不見，s37、s38 才出現（聖經 39→40 寫韓伯在村民前、錢員外在村民後） | 拍法 19、34；〈接點〉39→40 | (1) 改成 `the still water of the rice field with its rows of young seedlings soft in the lower left foreground`；(2) 加 `all of them standing on the dry trampled earth right at the edge of the water`；(3) 改成 `a stout man of fifty in dark olive green`；(4) 可以把五個村民之一換成背影的韓伯（`an old man with a white topknot in a faded grey long robe leaning on a bamboo staff, seen only from behind`），錢員外留到 s38 推開人擠進來（稿子本來就是這樣），人數不變 |
| 10 | s40 | `-qiang` 裁的是穀倉山牆頂（屋脊、天空、黃柳），放在跪著的刁七頭後面，等於他站得比門洞還高；構圖又寫「soft blurred figures at the left edge … behind him」，可是他背後只有穀倉，村民在他前面 | 拍法 19、29 | 開頭寫 `close-up from a little below`（仰角就看得到山牆與天）；「behind him … soft blurred figures at the left edge」改成 `at the left edge of the frame, soft and faceless, the shoulders of a few people turning their heads toward the right`（在他前側，不在牆前） |
| 11 | 白大夫各鏡；s07 | 定妝照是立領盤扣的絎棉短襖，文字寫長衫加棉背心；s07「his quilted cotton vest now done up」在畫面上沒有對應 | 拍法 19 | 不改也不會壞片；s07 那句拿掉，動作只留甩背帶與深吸一口氣 |
| 12 | s02 | 背影鏡送正臉定妝照，8 秒裡回頭露臉的風險；精修開頭「Doctor Bai shown in <Picture 1> keeps the same face」又點名、提臉 | 拍法 2、3 的經驗（唐小棠背影） | 先看 d1。兩支都回頭的話，fix 拿掉定妝照、身分靠文字（白髮小髻、月白長衫）；`clips-dh` s02 開頭照第 38 集換成 `The old man seen only from behind in <Picture 1> keeps the same hair and costume as the first frame` |
| 13 | s01（s04） | 第 38 集最後幾格阿令左邊露出拴著的馬頭頸；s01–s07 都沒寫馬，`-men` 圖左邊就是那根拴馬樁。s08 寫「already untied from the post」，馬突然出現 | 接戲；聖經〈接點〉38→39（馬拴在門前拴馬樁）、第 41 條（拴著的馬寫在哪一側） | s01 加 `at the left edge of the frame, soft, the head and neck of one chestnut-red horse tied by its reins to the square stone hitching post, well apart from her`，加送馬圖（必改 1 若用新圖一樣），人數加 `and one horse` |
| 14 | BUY（錄音後） | 照 PREP 的估法：s32 小禾「戴一頂草帽，帽子綁著紅繩，我沒看見臉」16 字、小聲努力回想、兩個停頓，6 秒可能放不下（約 5.5–6.2 秒）；s19、s21 白大夫 14 字約 5.0–5.5 秒，緊 | 聖經〈每集鏡數〉、拍法 43（5.9 秒以內） | s32 先改 8 秒（多 2 秒×2 種子，約 0.2 CU），或錄音後照 `span939-buy.txt` 定；s19、s21 錄音後量 |
| 15 | 錄音後的音高 | PREP §4 列的組合都要量；我再補兩組最可能撞的：s02 白大夫（第 38 集 143 Hz）→ s03 隊長（第 38 集成片降到約 149）只差不到 1 個半音；s37 韓伯（90–135）→ s38 錢員外（115–175）。另外隊長的聲音最好跟第 38 集成片最後幾句一致（a22 r5 約 150 Hz） | 拍法 43 | 量完照第 38 集 §4 處理；s02→s03 若撞，動隊長不動白大夫（白大夫第二場還有八句） |
| 16 | s24、s31、阿令的 identity | s24「the one white candle … burnt out and unlit」：圖上是一整根沒燒短的白蠟燭；s31「his hands closing round something small below the frame」會長出一件小東西；阿令 identity 從 s07 起還是「tailored close at the waist with a cloth sash」，s08–s13 腰帶在兩人腰上、s16 搭在臂上，可能畫成兩條 | 拍法 19、32 | s24 改 `its wick dark and unlit`；s31 改 `his two hands closing together below the frame`；`extras.json` 對 s07 起的鏡把 identity 的 `with a cloth sash and long sleeves` 換成 `and long sleeves` |
| 17 | s38 | 錢員外正面不笑在第 34、37 集常失敗（任務檔），本鏡是正面略仰、嘴張大尖叫，張大的嘴容易讀成大笑 | 任務檔第 34、37 集；站主規則 | 先看 d1；兩支都像笑，fix 改成側後背影＋錄音（第 34 集 fix4 的做法：不送臉部圖、不點名） |

## 不用改的（看過、接受）

| 項目 | 為什麼 |
| --- | --- |
| 接點 39→40 | s39 秦霜站在刁七左前、槍桿橫在套繩前、刁七跪在她右後；s40 刁七抬頭往右看、身後人影一齊往右轉：跟聖經 39→40「所有人回頭看跑到的許硯」接得上 |
| 白大夫 | 第一次露臉送 `baidaifu-portrait-l1`；鬚修到下巴，跟韓伯垂胸的長鬚分開；第二場在病房、第三場不出現，跟韓伯不同場（聖經〈人物〉）；藥箱 s07 起斜挎、s19 放在被上 |
| 阿令 | 騎馬的樣子（布條紮袖、綁腿、幾縷髮絲散出木簪）從 s01 起；腰帶 s06 抽出、s16 搭臂、s22 摺好放床上；s23 起披外衣、s30 摺好搭前臂；髻與木簪照圖（第 38 集成片後段她是長髮披背，聖經寫髻與木簪照圖，接受） |
| 隊長與弩手 | 加送 `duizhang-portrait-l1`、句子跟圖一致（開面盔、紅纓、黑甲紅釘）；s03 地點句開頭、補了表情句與分隔句；弩手同一身制服、遠、臉在盔影裡（拍法 34）；一支舉著的火把拿在一個人手上（拍法 37） |
| 官道 | 只有月光、天全黑（原版必修）；s10 s11 跟拍、側面、腰以上加馬頭頸；`-shu` 的路只在右下角，跟拍時背景滑過去沒問題 |
| 病房站位 | 許硯坐床沿（全集沒有跪的許硯）、白大夫坐枕頭那頭的床沿、阿令坐床尾床沿靠床柱、進門的人從左邊來：照新圖與聖經第 42 條（e938 必改 1 後） |
| 系統（拍法 11） | s25 s28 s28b s29 不寫淡藍光、嘴全程閉著；面板剪接時疊 |
| 穀倉前的群眾（拍法 34） | 十個人每人一種衣色（芥黃、炭灰、褪色靛藍、暗橄欖綠、深灰加靛藍頭巾、本色麻布、鐵鏽紅），沒有主角的顏色；村民甲只拍背影、舉拳、放錄音；s37 s38 的村民只到背影與肩 |
| 小禾 | 病中滿臉通紅、s24 起退燒、s30 起半坐兩手拿草兔子（`extras` 拿掉 hugging）；s32 平掌比帽簷、草帽不入鏡（聖經〈伏筆〉） |
| 刁七 | 破布短褐、黑綁腿、不穿皮甲、麻繩綁身、套繩、臉上一道石灰白粉；疤照定妝照寫在左顴骨（圖上畫右那一側，對） |
| 免費新圖的腳本 | `xujia_tangfang_e939.sh`、`gucang_wai_e939.sh` 都是 lanczos、bitexact、新 id；`prep939.log` 逐位元重建 4 張＋e938 裁切 9 張都相同 |

## 小結

- **必改 6 項**：
  1. 醫館門板圖是關的、s01 s04 s05 s07 寫推開，s08 又寫關：建議 d1 前花約 1 CU 用 Qwen 做開門圖（PREP §5-1）；不花錢的退路是只讓 s01 賭、其他鏡把門洞放到畫緣。
  2. 房門圖是關的、s16 寫半掩、s34 寫推開：照第 38 集必改 3 改成關著（秦霜一手按著身後關上的門）；s22 s23 s26 補寫門關著。
  3. s11 沒寫綁兩人的腰帶；s12 沒有馬、沒有腰帶，而且「她的後腦在前景、他的臉在後面」在同向騎馬時拍不出來：改側面、補腰帶與馬鬃、加送配鞍馬圖。
  4. 十鏡送的圖裡床或枕頭就在人背後、文字沒寫小禾，床會是空的（原版必修、第 38 集 M1）：近景改送免費裁的窗牆圖，s27 s28b 把熟睡的小禾寫進背景。
  5. s38、s39 同一支裡寫「他／她是畫面裡唯一的人」又寫 `exactly three／two people`：修 `off()`。
  6. s14 兩塊濕布：小禾額頭改成沒有布。

  除了 1 的 A 方案，都是改字或免費重裁。
- **建議 17 項**，都是免費或先看 d1：配鞍馬圖翻成頭朝右、s09 街的方向與樁的位置、s18 沒人拿的蠟燭、s27 過肩的機位、s30 許硯的笑、s28 第一格、s13 s35 動作太多、s36 田埂與站位、s40 背景與人影、白大夫的衣服、s02 背影送臉圖、s01 拴著的馬、s32 的 BUY、錄音後兩組音高、幾個小字、錢員外正面的笑。
- **站主 11-21～23 的規則**：風格句、許硯不寫鬍渣、柴刀、唐小棠不入鏡、跪姿拍到膝蓋、不掛東西、配鞍馬圖、精修文字沒漏進 d1 都做到了。門的開關兩處跟圖相反（必改 1、2）；only 句有兩鏡自相矛盾（必改 5）；第 41 條的腰帶與馬有兩鏡漏（必改 3）；同場相鄰說話者音高要等錄音。
- **接點 38→39 接得上**（缺拴著的馬，建議 13）；**BUY** 照估法都放得下，s32 最緊，錄音後重核。
- 改完 `r2.py`、`mkspec.py`、`extras.json`、`check939.py`、`xujia_tangfang_e939.sh`（新裁切、新 id）以後，重跑 `build939.sh`、`prep939.sh`（rc 0）、`DRY=1 e939d1.sh`；必改 1 走 A 的話先跑 Qwen、挑圖，再重跑。

## 寫稿者怎麼套（2026-11-24，前置代理；協調者定：必改 1 走 A，其餘必改照審稿、建議能免費做的都做）

改前的檔在 scratchpad `e939prep/*-before-review.*`。改完重跑 `build939.sh`、`STANDIN=1 prep939.sh`（rc 0；84 支 538 秒不變；st1／d1 preflight、`check_manifest`、`h3r` 0／0；掃描全 0；免費圖 9 張＋e938 裁切 9 張逐位元相同）、`DRY=1 e939d1.sh`（0 錯，提醒 manifest 是替身圖、真跑會拒絕）。

| 項目 | 怎麼處理 |
| --- | --- |
| 必改 1 | **A**：付費 Qwen 改圖的清單寫好、**沒跑**：`colab/runs/e939-live/qwen/{jobs-a.json,door-open.txt,negative-door-open.txt}`（底圖整張 `set-yiguan-men-ye-l1`、只改最近那扇門：兩扇門板往裡推開、門內油燈暖光灑到石階；種子 9391201–9391204；`check_images_manifest` 0／0），驅動 scratchpad `e939qwen.sh`（`STEP=a`／`STEP=pick-a PICK=<seed>`，DRY 0 錯）。挑定後裝成 `set-yiguan-men-ye-kai-l1`，免費 `yiguan_kai_e939.sh` 照 e938 `-men` 的框（`640:360:672:300`）裁 `-kai-men-l1`。s01 s04 s05 s06 s07 s08 送 `-kai-men`、s09 送整張 `-kai`；s08 身後寫『醫館兩扇門板仍往裡推開、門口暖光』（照新圖：白大夫剛出門，門沒關）。在圖裝好前 `prep939.sh` 要 `STANDIN=1`（替身＝關門的原圖），`e939d1.sh` 真跑會拒絕替身 manifest |
| 必改 2 | s16 門在身後關著；s34 秦霜第一格已經進門一步、左手按在身後關上的門板、推門往屋裡一探（運鏡改慢推）；s22 s23 s26 補寫門關著。`check939` 斷言 |
| 必改 3 | s11 補腰帶；s12 改側面中近景（畫右緣她的肩與後腦、他在她身後、腰帶、畫右下角馬鬃），加送配鞍馬圖、`GAZE_REFINE` 跟著改；`check939` 斷言 s11 s12 有 `sash wound twice` |
| 必改 4 | 免費新裁 `set-xujia-tangfang-kong-chuang2-l1`／`-kong-chen-chuang2-l1`（`560:315:620:60`，窗與後牆）、`-kong-qiang-l1`／`-kong-chen-qiang-l1`（`480:270:820:100`，窗右半與牆；夜的 `-kong-qiang` 備用）；s15 s21 送 `-kong-chuang2`、s25 s29 s33 送 `-kong-chen-chuang2`、s28 s29b s31 送 `-kong-chen-qiang`，s21 s31 的畫外句只寫牆，s29 s29b 身後拿掉床頭。s27 s28b 身後寫熟睡的小禾（加送她的圖、兩人）。`check939` 斷言這八鏡『behind him』裡沒有床字 |
| 必改 5 | `off()` 加 `only=False`；s27 用它；s38 s39 照審稿改寫畫外那一側、不寫『唯一的人』；`check939` 斷言同一支不同時有 `is the only person in the frame` 與 `exactly N people` |
| 必改 6 | s14 小禾額頭寫 `her forehead bare and damp`，濕布只有許硯手上那一塊；`check939` 斷言 |
| 建議 1 | 免費 `prop_flip_e939.sh` → `prop-zaohongma-an-r-l1`（頭朝右；看過：毛氈墊、繩肚帶、轡頭左右對稱、沒有字），s08–s13 改送它；s01 拴著的馬送原向 |
| 建議 2 | s09 照圖寫沿店門往鏡頭右下角衝出去、拿掉 side-on；拴馬樁『just left of the nearest door』；全場石階改『one wide low stone step』、不寫 top／lower step（`check939` 斷言） |
| 建議 3 | 只在必改 1 走 B 時需要：走 A，不適用 |
| 建議 4 | s18 光句改『warm candlelight from beyond the left edge』、構圖『falling on them from the left』 |
| 建議 5 | s27 改單人中景（朝畫左外的阿令點頭），身後床上的小禾；『把外衣拉緊』拿掉 |
| 建議 6 | s30 許硯寫不笑、動作句改 `goes still` |
| 建議 7 | s28 第一格臉還朝左，動作轉回正面、挑眉 |
| 建議 8 | s13 拿掉『再催馬』；s35 抱拳在第一格完成 |
| 建議 9 | 四點都做：前景改水田、人站在水邊乾土上、壯漢五十歲、芥黃衣老漢換成背影的韓伯（白髮髻、灰長袍、竹杖；不點名、不送圖，十個人不變）；錢員外留到 s38 |
| 建議 10 | s40 寫略仰、轉頭的人影在畫左緣、他的前側 |
| 建議 11 | s07『背心穿好』拿掉 |
| 建議 12 | 精修文字 s02 開頭換成『The old man seen only from behind … his back to us』（`live_clips`／`anchor_form`）；d1 照舊送定妝照，先看 d1 |
| 建議 13 | s01 畫左緣加拴在樁上的馬頭頸、加送配鞍馬圖（原向）、二人一馬 |
| 建議 14、15 | **錄音後**（錄音還是 0／40，站台額度 429）：s32 BUY、s19 s21 照 `span939-buy.txt` 定；s02→s03、s37→s38 量音高，撞了動隊長 |
| 建議 16 | s24 起寫『its wick dark and unlit』；s31『his two hands closing together below the frame』；`extras.json` 把阿令身分句的『with a cloth sash』拿掉（全集：腰帶各鏡寫在構圖） |
| 建議 17 | **d1 後**：兩支都像笑就 fix 改側後背影＋錄音 |
