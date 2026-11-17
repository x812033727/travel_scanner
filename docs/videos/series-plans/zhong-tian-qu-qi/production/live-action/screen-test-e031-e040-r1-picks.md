# 第 4 篇章（第 31–40 集）試鏡第一輪挑片

2026-11-17，協調者照站主授權挑（`r2-bible-e031-e040.md`〈站主的決定〉：試鏡挑圖、重拍由製作端定）。
來源 `~/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-e031-e040/out/<id>-<種子>.png`（`screen-test-e031-e040.py`，種子 37037／37038），
比較圖 `../sheets/r1-01.jpg`–`r1-05.jpg`。每張兩個種子都全尺寸看過，臉、手、邊緣、像字的痕跡放大 2–4 倍看；定妝照跟 refs-live 裡全部 19 張定妝照並排比過，免得撞臉。
挑定的照抄成 `../assets/refs-live/<id>.png`（864×1152 或 1312×736 RGB，跟之前的試鏡挑片一樣不轉檔、保留 PNG 的 prompt 欄）；
`set-chengmen-ye-l1` 是挑定的種子再免費塗掉一塊匾。歸檔與免費衍生圖的命令寫在 `../assets/refs-live/README.md`〈第 4 篇章挑片〉。

**REDO** 的照下表的「第二輪改寫」重跑（寫的是畫面上**要有**什麼，第 18 條；要避開的放負面）。第二輪的清單與程式還沒寫，見文末。

| # | id | 挑 | 理由 |
| --- | --- | --- | --- |
| 1 | `diaoqi-portrait-l1` | **REDO** | 37037 方臉濃眉、年紀對、跟二牛分得開，但疤是一道**新的紅色割傷**，只在顴骨一小段（規格：淡色舊疤從左眉骨斜到左顴骨），短褐是**盤扣斜襟**加紅腰帶、無袖毛邊；37038 臉年輕，褐色交領、髮髻、臉型都跟 `erniu-portrait-l1` 太像（同篇同框會撞臉），疤一樣是新紅傷。第二輪改寫：以 37037 為底圖編輯（臉、髮、光、灰底不動），改成「one long old scar, healed smooth and paler than the skin around it, a single slightly raised line that starts at the outer end of his left eyebrow and runs down across his left cheekbone to the middle of his cheek」與「a ragged earth-brown hemp tunic with a crossed collar wrapped left over right and tied shut with a plain rope belt, short ragged sleeves」；負面加 fresh wound、blood、red cut、knot buttons、frog buttons、red sash、sleeveless。不行就灰底重畫，人寫三十八歲、風吹日曬的粗皮膚、眼角深紋、粗脖子（跟二牛的年輕光臉分開） |
| 2 | `baidaifu-portrait-l1` | **37037** | 寫實照片感、白髮小髻、白鬚修到下巴（跟韓伯垂胸長鬚、鄭伯灰鬚分得開）、眼神亮。毛病：衣服是米白絎縫**立領盤扣**短衣（沒有外面那件背心，像襖不像長衫；立領盤扣定妝照小禾、鄭伯也有，接受）；臉比「清瘦」圓；**嘴角微微上揚**，嚴肅的鏡（第 39 集救人）照第 1–30 集的做法寫 `lips pressed together`，草稿照笑就 `drop_pictures`。37038 交領對、鬍子尖長過下巴，但整張偏 3D 塑膠皮膚，不用 |
| 3 | `duizhang-portrait-l1` | **37037** | 兩個種子同一張臉；37037 寫實、黑甲紅釘、盔頂一撮紅纓、內襯黑底暗花（放大看是布紋，沒有字）；37038 內襯是金色捲雲紋（大片花紋會長假字）、偏 CG。盔兩側有護耳片，臉露在外面，接受。跟錢員外（八字鬍、圓胖、黑帽）分得開 |
| 4 | `prop-zaohongma-l1` | **REDO**（灰底重畫） | 第一輪的白星版移到 `../star/`、不用。不帶白星的重畫（2026-11-17 19:19–20:00）**只出了 37037**（37038 是 Colab 筆記本出錯，兩次都沒出圖）。37037 跟第 30 集 s36 的 9301101 是同一種毛色（全身紅棕、鬃尾同色，比 s36 略深），但**不能用**（協調者同意）：鞍是現代英式馬鞍、絎縫鞍墊、現代馬鐙，額頭到鼻樑前緣有一道小白痕。第二輪灰底重畫，正面改寫：「an old plain Chinese country saddle, a simple wooden-tree saddle under one plain dark leather cover with a low rounded front and back, one plain dark felt cloth cut square under it, simple round iron ring stirrups hanging on plain dark leather straps; a plain dark leather bridle of plain narrow straps…, the leather smooth and unadorned; its forehead, face and nose the same even red-brown as its neck and body, its mane and tail the same red-brown」，毛色照 s36 9301101 寫成明亮的紅棕；負面加 English saddle、quilted saddle pad、modern stirrups、metal studs、brass fittings、white star、blaze、white mark on the forehead |
| 5 | `prop-changqiang-l1` | **37038** | 槍頭完整、素鐵、沒有纓，素木槍桿，地板較像實拍；槍尾出了左緣（參考圖只管形狀，接受）。37037 槍頭被右緣切掉、地板像貼圖 |
| 6 | `set-xujia-yuan-han-l1` | **37038** | 只改了牆外：乾裂黃土、幾根枯桿，院子、屋、樹、井、木板、兩個陶罐跟底圖一樣（37037 多一塊木板、院門外多一塊石板地、整張更橘）。裂土塊大而規則、有點像鋪石，偏 CG（底圖本來就偏 CG）。佈局沒變，`-dong-*` 的裁切直接套用 |
| 7 | `set-ganxi-l1` | **37038** | 溪床是一塊塊乾裂泥板、縫是黑的，放大看讀得出乾泥；木板橋、柳樹、兩岸不變。37037 的溪床變成六角形石板步道。毛病：溪床跟岸幾乎齊平、沒有「只剩石頭」；右岸金黃稻田照舊（底圖不變，第 31 集 c31 寫午後熱氣） |
| 8 | `set-hantian-l1` | **37038** | 一行行乾裂土壟、殘稻樁，前景有一道田埂把近處一塊田分出來（第二輪 `-yang`、`-shou` 改「中間那塊田」正好用）。37037 壟溝裡一條條藍色（反光或天色），不像旱地。兩張都偏 CG；柳樹仍是秋天金黃（底圖不變） |
| 10 | `set-shangyou-ba-l1` | **REDO** | 兩張都畫了**車**（規格不畫騾車）；37037 是一大片梯田與水、看不到乾溪床、石頭像枕頭；37038 背景是桂林式尖峰、卡通、壩是一排圓石。第二輪改寫：「in the foreground the dry riverbed of grey cracked mud and loose river stones runs straight away from the camera; in the middle distance a low dam, about chest high, of piled grey field stones and stacked brown hemp sandbags, crosses the riverbed from the left bank to the right bank; on top of the dam a flat packed-earth path; behind the dam a still pool of brown water; on the right bank a fresh earth ditch carries the water off to a small field of bright green young rice; low rounded hills far behind, the same gentle hills as the village valley」；負面加 cart、wagon、karst peaks、steep pointed mountains、terraces、rice terraces |
| 11 | `set-jingkeng-l1` | **REDO** | 37037 是城裡的石板廣場、房子，麻繩打成**絞索圈**；37038 俯拍（不是人眼高）、整張發藍、像畫。第二輪改寫：**以挑定的 `set-hantian-l1` 為底只加一件事**（同一片旱田、人眼高已經對）：「a single row of twelve square well pits, each one stride wide, runs from the near left diagonally away to the far right across the cracked field; beside each pit one heap of fresh yellow earth and one bamboo basket; across each pit one short wooden beam with a thick hemp rope tied on it, hanging straight down into the dark pit; the middle pit the deepest, its earth heap the biggest; a low grey morning haze」；負面加 noose、rope loop、paving、tiles、street、houses、top-down view、aerial view |
| 12 | `set-citang-l1` | **37038** | 門在左（格子門向內推開）、供桌在右、五塊素面深色牌位**立在桌上**、香爐、兩支白蠟燭、上方一根深色主梁、青石地；放大看牌位只有一圈細框、沒有字。37037 的牌位**懸在牆上**（像掛著的牌子）、牆上滿是刮痕線條（會長字）、偏 CG。毛病：門外是另一進院子的白天，不是黃昏天光；牆上一片從格子門透進來的條紋光 |
| 13 | `set-shentan-l1` | **REDO** | 本篇最重要的道具，兩張都不行：37037 是一條筆直的石砌水渠、水車小、上面多一捲竹筒；37038 空拍俯視、CG、水車架子怪。第二輪改寫：「a real photograph from standing eye height on the left bank, camera level, horizon straight in the upper quarter: at the bottom of a shallow gully a round deep green pond fills the right half of the frame; standing in the pond near its left edge, one large wooden waterwheel seen from the side, as tall as three men, twelve flat wooden paddles evenly around the rim, a ring of small bamboo tubes tied along the rim, its thick round wooden axle resting on two heavy wooden A-frames planted one on each side of the wheel; a short stone channel runs from a wooden sluice board on the left side of the pond to under the wheel; from the top of the wheel a long open wooden trough on posts carries water to a narrow earth ditch climbing to the upper right toward cracked dry fields; a bare flat patch of earth on the left bank; one big grey boulder on the right bank; a field ridge along the top right; bright midday light」；負面加 aerial view、top-down、high angle、drone shot、canal、brick channel、paving、small wheel |
| 14 | `set-cunkou-l1` | **REDO** | 37037 純 3D 算圖、沒有柵門與門樓；37038 **魚眼**（暗角、右邊電線桿似的十字木桿一路彎）、遠處幾個紅色小人影或燈籠。第二輪改寫：「the entrance of a small Song-dynasty farming village at dusk under an orange-red sky; on the left two heavy gates of rough vertical logs stand shut with one thick wooden bar laid across their middle, under a small gate roof of dark grey tiles on two log posts; outside the gate a dirt road in the foreground leads to a short plank footbridge over a dry ditch; beside the gate one old willow with long drooping branches; on the right a dirt village lane goes away past three low mud-brick houses with thatched roofs; low hills behind」；負面加 fisheye、vignette、poles with crossbars、utility poles、power lines、red figures、lanterns、render |
| 15 | `set-shanjiao-qu-l1` | **REDO** | 37037 卡通沙漠、金字塔形的山；37038 渠裡有水、整片村子與大片青秧、不在山腳。第二輪改寫：「a freshly dug empty irrigation ditch as deep as a man is tall, its bottom dry brown earth, runs from the near right away to the left and ends at the foot of a steep scrubby hillside that fills the left background; near the hill end a raised earth bank three strides wide crosses the ditch, one plain wooden sluice board standing in a slot in the bank and a heap of dry straw on top of it; both banks cracked yellow earth with fresh heaps of dug soil; far away on the right one small patch of green young rice; flat white morning light」；負面加 water in the ditch、village、houses、pyramids、desert dunes |
| 16 | `set-xujia-houmen-ye-l1` | **37038** | 冷藍月光、牆邊柴堆、窄木板門半掩、門外小巷往左；寫實。37037 下雪（第 37 集是晚春）、遠處有一根電線桿與電線。毛病：右邊屋簷下一根淺灰的扁木（x 1030–1130、y 230–270），放大看是一段梁頭、不是牌子，留意長字；門裡有暖光（屋裡點燈，可以照寫）；牆是石牆不是泥牆 |
| 17 | `set-guandao-ye-l1` | **REDO** | 37037 沒有路、像柵欄；37038 月夜楊樹道很好，但**路中間一個人影**（拍的人的影子），路直直往畫面中間消失，地平線上一點車燈似的亮點。第二輪改寫：「a wide yellow earth road crosses the frame from the right foreground and runs away to the far left; dry bare fields on both sides; a line of tall poplars along the far side of the road, black against the sky; the moon high in the upper right of the frame, in front of the camera, cold blue moonlight, the poplars' long shadows falling toward the camera across the road; the road empty」；負面加 shadow of a person、human shadow、silhouette of a person、car lights、distant lights、street lamps |
| 18 | `set-chengmen-ye-l1` | **37038**（免費塗掉匾） | 灰磚城門洞、釘鐵釘的大門、兩支插在鐵架上的火把、牆邊一排拒馬木柵、月亮；寫實。左上門洞上方有一塊**匾，放大看有幾個淡淡的假字**，免費塗掉（見 refs-live README）。37037 的匾字更清楚、偏 CG。毛病：是一扇大門開了一半，不是「門洞旁一扇小門半掩」；拒馬柵沿著牆擺，不是橫在門前路上（第 38 集「衝向木柵」照圖寫木柵在城門右邊的牆前） |
| 19 | `set-yiguan-men-ye-l1` | **REDO** | 37037 牆上**掛一塊告示牌**、CG；37038 拴馬樁長成一個**十字架**，牆上一團像人的影子，門面被一片沒有光源的暖光照著（不是冷藍月光），日式長屋。第二輪改寫：「one short plain stone hitching post, a square grey stone pillar waist high with a round hole through its top, stands at the edge of the street in front of the shop; the shop front is two plain wooden door boards shut, two worn stone steps up to them; the plain wooden lintel above the door bare wood; on both sides the next shops' door boards are shut; cold blue moonlight on the stone-paved street and the fronts」；負面加 cross、crucifix、wooden post with crossbar、notice board、sign、shadow of a person、warm light on the walls、Japanese architecture |
| 20 | `set-gucang-ye-l1` | **REDO**（以 37038 為底只改一件事） | 37038 寫實、疊起的麻袋、木梯、籮筐、稻草地、高處小窗深藍，好；但左邊是一盞**掛在木架上的玻璃提燈**（吊著的燈籠、而且是西式煤油燈）。37037 也是玻璃煤油燈、偏 CG。第二輪改寫（底圖 37038，其他不動）：「change only one thing: the hanging glass lantern and the wooden arm it hangs from are gone; in their place, on the wooden post at shoulder height, one small open clay oil lamp with a single small flame sits on a flat iron plate fixed to the post; it stays the only light」；負面加 hanging lantern、glass lantern、hurricane lamp、kerosene lamp、chain |

（第 9 張 `set-xujia-tangfang-chen-l1` 用免費調色、沒進試鏡。）

## 歸檔與免費衍生圖（2026-11-17，全尺寸看過）

- 照抄：`baidaifu-portrait-l1`、`duizhang-portrait-l1`、`prop-changqiang-l1`、`set-xujia-yuan-han-l1`、`set-ganxi-l1`、`set-hantian-l1`、`set-citang-l1`、`set-xujia-houmen-ye-l1`。
- `set-chengmen-ye-l1`（37038 塗匾）、`set-citang-ye-l1`、`set-xujia-yuan-han-men-l1`、`-han-jing-l1`、`-han-qiang-l1`、`-han-wu-l1`、`-han-di-l1`：腳本在 `free-e031-e040/`，命令與看到的寫在 refs-live README。
- 還不能做：`set-shentan-qu-l1`（`set-shentan-l1` 要重畫）、`set-gucang-men-ye-l1`（等 `set-gucang-wai-l1`）、`prop-zaohongma-head-l1`（等第 30 集 s36 挑片）。

## 第二輪要跑什麼

**程式已寫（2026-11-17）**：`screen-test-e031-e040.py --r2`（清單 `OUT_DIR/r2.json`、提示詞 `OUT_DIR/prompts-r2/`、出圖 `OUT_DIR/out-r2/`、比較圖 `--r2 --sheet` → `sheets/r2-NN.jpg`），
跑法 scratchpad `st31r2.sh`（照 `st31r1.sh`：session `zt-live2`、每次只送還沒出圖的、一次加重試一次、放掉 VM、最後出比較圖）。
`check_images_manifest.py`：0 錯誤、2 警告（刁七的直式畫布，跟第一輪一樣）；`DRY=1` 跑過，24/24 支待做、沒有開 VM。
第一輪的清單照跑過的留著；第一輪挑定的圖歸檔後，**第一輪不能再重新產生**（程式拒絕 refs-live 裡已有的 id），`--sheet` 照舊能用。

第二輪（12 張 × 種子 37039／37040＝24 支）：
- 以第一輪的種子為底只改那一處：`diaoqi-portrait-l1`（`out/diaoqi-portrait-l1-37037.png`：臉、髮、光不動，改疤與衣襟腰帶）、`set-gucang-ye-l1`（`out/set-gucang-ye-l1-37038.png`：吊著的玻璃燈換成柱上鐵片托著的陶油燈）。
- 以挑定的 `set-hantian-l1` 為底：`set-jingkeng-l1`（只加一排井坑、土堆、竹筐、橫木與麻繩）、`set-hantian-yang-l1`、`set-hantian-shou-l1`（田埂前面那塊田灌水插秧／金黃稻穗，田埂後面照舊乾裂）。
- 灰底重畫 7 張：`prop-zaohongma-l1`（老式素鞍、素轡頭、臉與鬃尾全紅棕，照第 30 集 s36 9301101；跟第一輪同一個 50 mm 側面鏡頭句）與 `set-shangyou-ba-l1`、`set-shentan-l1`、`set-cunkou-l1`、`set-shanjiao-qu-l1`、`set-guandao-ye-l1`、`set-yiguan-men-ye-l1`。第一輪的提示詞其實已經寫了大部分規格，模型照樣畫成空拍、CG、魚眼，
  所以第二輪換了鏡頭句（`REAL_LENS`：「站在地上的人、眼睛高度、鏡頭朝前水平」），負面詞每張都加空拍、俯視、3D 插畫、概念圖、遊戲場景、過飽和、暗角，再加上表裡各張的毛病。
- 重畫的 id 不變、仍是 l1（第一輪沒歸檔）。

第三輪（`--r3`，3 張 × 2＝6 支，`r3.json`、`out-r3/`；`ROUND=3 bash st31r2.sh`）：`set-shentan-gongdi-l1`（底圖 `set-shentan-l1`）、`set-shanjiao-qu-ye-l1`（底圖 `set-shanjiao-qu-l1`）、`set-gucang-wai-l1`（底圖 `set-hantian-yang-l1`）。
程式已寫；底圖還沒歸檔前它會停下來說缺哪張（用假底圖試過：6 支、0 錯誤）。第二輪還不行的重畫再加進第三輪。
之後免費：`set-shentan-qu-l1`、`set-gucang-men-ye-l1`、各張的裁切。

時程：第 31 集第二場要的 `-han`、乾溪床已經有，**壩（`set-shangyou-ba-l1`）還沒有，第 31 集 c32–c41 拍之前第二輪要跑完**；第 32 集要井坑、祠堂（祠堂已有）；第 33–34 集要水車。
第一輪的馬重畫 2026-11-17 20:00 收工（37/38，VM 已放掉），session `zt-live2` 空著，可以跑第二輪。
