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

## 第二輪挑片（2026-11-17，`--r2`，種子 37039／37040，`out-r2/`，比較圖 `sheets/r2-01`–`03.jpg`）

24/24 支都出圖。每張兩個種子都全尺寸看過，放大看臉、邊緣、像字的痕跡與人影；刁七跟 refs-live 的定妝照（二牛、許硯）比過，馬跟第 30 集 s36 的 9301101 抽格比過。
挑定的照抄成 `../assets/refs-live/<id>.png`（1312×736 RGB，保留 PNG 的 prompt 欄）。**7 張挑定、5 張進第三輪。**

| id | 挑 | 理由 |
| --- | --- | --- |
| `diaoqi-portrait-l1` | **REDO**（第三輪灰底重畫） | 以第一輪 37037 為底的編輯**兩張都沒有換掉盤扣**（只有紅腰帶變成麻繩）。37039 的疤變成額頭到臉頰好幾道紅色抓痕；37040 是一道暗紅的新傷，在他的**右**臉頰、從眼下開始，另一側臉頰原本的疤被抹掉，留下一片灰色顆粒。第三輪改灰底重畫：三十八歲、粗脖子、眼角深紋、風吹日曬的皮膚（跟二牛的年輕光臉分開），疤寫成「a thin pale line lighter than his skin」從左眉尾到左顴骨，短褐寫成交領、靠衣襟自己闔上、麻繩腰帶；負面加 knot buttons、frog buttons、toggles、buttons、red cut、claw marks、several scars、young man |
| `prop-zaohongma-l1` | **REDO**（第三輪） | 兩張的毛色都對（全身紅棕、鬃尾同色、額頭素的，接近 s36 9301101），但**又是英式馬鞍加絎縫鞍墊**（37040 鞍墊藍色滾邊）、現代馬鐙，整匹像數位繪圖、塑膠亮面。第一、二輪四張馬只要寫到 saddle 就畫英式鞍，所以第三輪**不寫 saddle 這個字**：背上「one thick square of dark brown felt folded double, and on the felt a low old Chinese riding seat of dark leather stretched over a wooden frame, with one low rounded wooden arch at the front and one at the back, held on by one plain leather strap round its belly; two round iron rings hang on plain leather straps」，畫風寫「documentary photograph on film… natural matte coat with real hair and a little dust」；負面加 English／western／dressage saddle、saddle pad、numnah、piping、modern stirrup irons、glossy plastic coat、digital painting |
| `set-gucang-ye-l1` | **37039** | 玻璃提燈變成**陶碗油燈放在圓鐵盤上**、一盞火，麻袋、木梯、木桶、稻草地、小窗都跟第一輪 37038 一樣。毛病：燈盤仍用一條細繩**吊在**左上的木臂下（不是釘在柱子上的鐵片）；陶碗沒有可以長字的面，接受，鏡頭寫「one small clay oil lamp on a round iron plate hanging from a wooden arm on the post」。37040 是一只帶把手的茶杯，左下牆角一團像人影的黑影，不用 |
| `set-jingkeng-l1` | **37040** | 一排井坑從左前斜到右後、每口一堆褐色土，前面一口有橫木與垂下的麻繩、一個木桶；田、柳樹、遠處村子跟 `set-hantian-l1` 一樣。毛病：坑壁像磚砌的、裂土像磚（底圖本來就偏 CG）；只有第一口有橫木麻繩，其他的寫在鏡頭。37039 的土堆是黃色顆粒、像一堆馬鈴薯 |
| `set-shangyou-ba-l1` | **REDO**（第三輪，**最急**：第 31 集 c32 起） | 37039 畫面正中站著一個藍袍男人；37040 沒有人，但乾溪床又畫成**鵝卵石鋪的路**，壩是一道水泥似的矮牆、中間一個現代水泥溢洪口，後面是一大片湖。第一輪 37037、乾溪床 37037 也都是「riverbed … stones」畫成鋪石路，所以第三輪寫「a dry gully … bare brown earth split by deep dry cracks, with a few loose fist-sized rocks」，壩寫成「a rough farmers' dam … a long heaped bank of brown earth faced with piled rough fieldstones and stacked brown hemp sacks, uneven and handmade」；負面加 paved road、cobblestones、flagstones、concrete、spillway、sluice gate、modern dam、retaining wall、lake、reservoir |
| `set-shentan-l1` | **REDO**（第三輪） | 兩張又是**空拍**，而且都有現代人（37039 兩個、37040 一個穿藍 T 恤的）；潭是石砌圓池。第三輪把水車當主體寫成「seen exactly from the side, from the bank of a small pond, the wheel filling the middle of the frame」（馬、長槍正側面都畫對了），負面加 stone-lined pool、round stone basin、tourist、man in a blue shirt |
| `set-cunkou-l1` | **37040** | 左邊一座小瓦頂木柵門、斜撐木條、柳樹、門外一座木板小橋跨乾溝、右邊土路與三間泥屋、遠山、橘紅天；沒有魚眼、沒有木桿、沒有人。毛病：柵門是單獨一座、兩邊沒有籬笆；偏 3D 算圖。放大看第一間屋門邊一條亮塊是半開的門板，不是牌子。37039 柳枝像一串串珠子、門開著 |
| `set-shanjiao-qu-l1` | **REDO**（第三輪） | **兩張都有人**（37039 俯拍、正中一個穿藍襯衫的；37040 左前一個穿長袍的男人），37040 還有村子。第二輪的鏡頭句「A real photograph taken by a person standing on the ground」把人叫進畫裡（壩 37039 也是），第三輪改成「from a camera on a tripod at standing eye height … the place empty and still」 |
| `set-guandao-ye-l1` | **37039** | 月夜、楊樹兩排黑影、土路、楊樹影子橫過路面、沒有人影、沒有車燈。毛病：路仍直直往畫面中間消失（不是由右往左），整張像 3D 算圖；騎馬的側面鏡從這張裁一段路面或寫在鏡頭。37040 路面是磚、更像算圖 |
| `set-yiguan-men-ye-l1` | **37039** | 窄石板街、右邊一排關著的木門板、兩級石階、門前兩根**方石拴馬樁**（頂上有圓孔）、冷藍月光，沒有十字架、沒有人影、沒有暖光、門楣素木。毛病：偏 3D 算圖；門板很長一排，醫館是哪一間要在鏡頭寫（靠近鏡頭、有石階的那一間）。37040 右上角一個白色小圓圈、樁上刻紋像字 |
| `set-hantian-yang-l1` | **37039** | 只有田埂前那塊田灌了淺水、稀疏青秧倒映著天與柳樹，田埂後面照舊乾裂；跟 `set-hantian-l1` 同一個格局。37040 水漫過左邊的田埂、秧苗發黃 |
| `set-hantian-shou-l1` | **37039** | 同一塊田長滿金黃稻穗，田埂後面仍是乾的褐土。37040 金黃一路延伸到左後、看不出四周乾裂。兩張的稻穗都偏卡通 |

免費衍生圖：這輪挑定的沒有聖經列在〈免費圖〉等它的（`set-shentan-qu-l1` 要等 `set-shentan-l1`、`set-gucang-men-ye-l1` 要等 `set-gucang-wai-l1`）；各張的門閂、石階、穀袋等裁切等到用的那一集再做。

## 第三輪要跑什麼（程式已改，`ROUND=3 DRY=1` 跑過）

`screen-test-e031-e040.py --r3` 改寫成第二輪的 5 張 REDO 加 `set-gucang-wai-l1`（底圖已歸檔的 `set-hantian-yang-l1`）：6 張 × 種子 **37041／37042**＝12 支，`r3.json`、`prompts-r3/`、`out-r3/`、`sheets/r3-NN.jpg`。
`check_images_manifest.py` 0 錯誤 2 警告（刁七直式）；`DRY=1`：12/12 支待做、沒有開 VM。約 15–30 分鐘、2.5–5 CU。
原本第三輪的 `set-shentan-gongdi-l1`、`set-shanjiao-qu-ye-l1` 移到 `--r4`（種子 37043／37044，`ROUND=4`），要等第三輪挑定 `set-shentan-l1`、`set-shanjiao-qu-l1` 歸檔；沒歸檔時程式會停下來說缺哪張。
第二輪的 `--r2` 現在不能再產生清單（挑定的已在 refs-live），`--r2 --sheet` 照舊能用。

## 第三輪挑片（2026-11-17，`--r3`，種子 37041／37042，`out-r3/`，比較圖 `sheets/r3-01`–`02.jpg`）

12/12 支都出圖，每張全尺寸看過、放大看人影與像字的痕跡；刁七跟二牛、許硯比過，馬跟 s36 9301101 比過。**id 一律不變**（第 31 集 `r2.py` 已在引用）。
4 張挑定（其中 2 張加免費修圖）、1 張免費衍生、2 張進第四輪。

| id | 挑 | 理由 |
| --- | --- | --- |
| `set-shangyou-ba-l1` | **37042**（免費塗掉一個小方塊） | 第一次沒有人、沒有鋪石路、沒有水泥：前景一長排麻袋土埂擋著一大片黃泥水、右邊一條小溝引水到青秧田、兩旁竹林山谷；相機在土埂上、人眼高、水平。遠處田埂上方一個**深色小方塊**（x 509–524、y 310–327，像空白的小牌子或小屋），用 `free-e031-e040/clean_shangyou_box.py` 補掉（調和擴散加旁邊的紋理），放大 5 倍只剩一片淡淡的模糊。毛病：沒有「壩前的乾溪床」，壩是沿著畫面縱向的一長排麻袋（不是橫過河道）；麻袋上的綁帶有點 CG。c32–c41 站位寫「人站在麻袋土埂上、水在左、溝與秧田在右」。37041 是空拍、壩是光滑的圓石牆加水泥邊 |
| `set-shentan-l1` | **37041** | 第一次是人眼高的正側面：一架大木水車立在潭邊、木軸架、輪緣與輪輻清楚，左邊木架與麻繩、木台階與一小段木板、右下大灰石、後面乾裂的田；沒有人。毛病：輪上看不出葉板與竹斗（寫在鏡頭）；木槽畫成一根架在兩根柱上的平樑；潭邊是石塊砌的；地平線上有幾根細小的像電線桿的豎線（很遠、很小）。37042 輪軸是一顆圓球、輪輻戳出輪緣外、背景沙丘 |
| `diaoqi-portrait-l1` | **37041**（免費改成舊疤） | 灰底重畫有用：三十多到四十、方臉、眼角深紋、交領**右衽**、靠衣襟闔上、麻繩腰帶、沒有盤扣、破布條紮髻；跟二牛（年輕光臉）、許硯（書生）分得開。疤仍是左顴骨上**一小道新的紅割傷**，用 `free-e031-e040/diaoqi_old_scar.py` 改成舊疤：把紅傷用周圍皮膚補掉，再沿原傷的方向（延長兩端各 25%）畫一條約 2 px 寬、比皮膚亮一點的淡線。放大 3 倍看：一道淡色細疤，沒有紅色、沒有方塊；比規格短（從顴骨上緣斜到顴骨下，沒到眉骨），接受。37042 兩頰與脖子都是新紅傷 |
| `set-gucang-wai-l1` | **37042** | `set-hantian-yang-l1` 只加了一座灰木板穀倉，兩扇門板往外開、門內暗，穀倉在青秧田右邊的乾地上，柳樹、遠處村子都還在。毛病：門內後牆一扇亮的小窗（白天，接受）。37041 把柳樹換成了穀倉、穀倉的倒影在水田裡 |
| `set-gucang-men-ye-l1` | **免費**（`set-gucang-wai-l1` 的門那一塊） | `free-e031-e040/gucang_men_ye.py`：裁 560×315（752, 190）放大 2.34 倍，整張轉成冷藍月夜（亮度 1.15 次方 ×0.30、偏藍、留 18% 原色），天空用柔邊遮罩再壓暗一半，門洞裡壓到門洞的第 30 百分位（後牆小窗不亮）。全尺寸看：讀得出月夜的木板穀倉、兩扇門板開著、門洞全黑；毛病：柳樹在夜裡變成一片淡灰的枝、天空上半有一條較暗的帶子、偏軟。門柱上的火把寫在鏡頭（第 33 條） |
| `prop-zaohongma-l1` | **REDO**（第四輪：37042 只把背上清空） | 不寫 saddle 也一樣：**兩張又是英式鞍加絎縫鞍墊**、現代馬鐙，模型的「馬＋鞍」就是這一種。37042 的馬最像真的（霧面毛、額頭素的、鬃尾紅棕，跟 s36 9301101 同一型），第四輪以它為底只改一件事：背上什麼都沒有（裸背，只留轡頭）。鞍不進參考圖，騎馬鏡照第 41 條在鏡頭寫素鞍，參考圖沒有英式鞍的形狀可以拉 |
| `set-shanjiao-qu-l1` | **REDO**（第四輪：37041 只改渠） | 37041 是唯一沒有人、沒有村子、像實拍的：一條往遠處延伸的渠、左邊挖出的土堆與一捆乾草、右邊青秧田、左邊一排樹；但**渠裡有水**、渠頭是一道木板橋（不是土埂加閘板）。第四輪以它為底只改渠：溝底乾土、木板橋的位置換成三步寬的土埂、中間立一塊木閘板。37042 背景有房子、溝底像一顆顆圓石、一根長管子 |

`set-shentan-qu-l1`：挑定的 `set-shentan-l1` 裡**沒有土渠可以裁**（木槽是一根平樑、右邊那條淺色帶是一條墊高的路），所以免費先裁那一段（`crop=412:232:900:330`，由程式產生在 `OUT_DIR/base/set-shentan-l1-qu-crop.png`），第四輪用一次編輯把淺色帶挖成一條乾土渠。

## 第四輪要跑什麼（`ROUND=4 DRY=1` 跑過）

`--r4`：4 張 × 種子 **37043／37044**＝8 支，`r4.json`、`prompts-r4/`、`out-r4/`、`sheets/r4-NN.jpg`；`check_images_manifest.py` 0 錯誤；`DRY=1` 8/8 支待做、沒有開 VM。約 12–25 分鐘、2–4 CU。
- `prop-zaohongma-l1`：第三輪 37042 只把背上清空。
- `set-shanjiao-qu-l1`：第三輪 37041 只改渠（乾、土埂、閘板）。
- `set-shentan-gongdi-l1`：挑定的 `set-shentan-l1` 只把水車改成造到一半（木架與軸、一半輪輻、沒有輪緣，木料與竹竿堆在岸上）。
- `set-shentan-qu-l1`：`set-shentan-l1` 的免費裁切只加一條乾土渠。
第五輪（`--r5`，種子 37045／37046，`ROUND=5`）：`set-shanjiao-qu-ye-l1`，等第四輪挑定 `set-shanjiao-qu-l1` 歸檔後跑（只改光成夜）。

## 第四輪挑片（2026-11-17，`--r4`，種子 37043／37044，`out-r4/`，比較圖 `sheets/r4-01.jpg`）

8/8 支都出圖，全尺寸看過、放大看過。id 不變。3 張挑定、1 張免費衍生、1 張進第五輪。

| id | 挑 | 理由 |
| --- | --- | --- |
| `prop-zaohongma-l1` | **37043** | 背上清空成功（裸背，只剩轡頭與韁繩）；正側面、四蹄著地、全身紅棕、鬃尾同色、**額頭與臉素的**，沒有白星、白鼻樑。跟第 30 集 s36 9301101 抽格比：同樣是棗紅、鬃尾同色，這張顏色深一點、偏紅，s36 在夕照下偏橘、鬃毛較亮，接受（騎馬鏡照第 41 條寫 chestnut-red）。毛病：轡頭有幾個亮的金屬環扣（現代馬術轡頭的樣子，鏡頭寫 plain dark leather bridle）；皮毛有一點塑膠光、放大看有細點狀的紋理。鞍寫在每一鏡（「a plain dark brown leather saddle」，第 41 條），參考圖裡沒有英式鞍。37044 幾乎一樣、光澤更亮 |
| `prop-zaohongma-head-l1` | **免費**（挑定的 `prop-zaohongma-l1` 頭頸） | `crop=480:270:140:10,scale=1312:736:flags=lanczos`。聖經原本要從第 30 集 s36 截頭頸，但 s36 每一格馬頭都跟秦霜的身體、拉韁繩的手疊在一起，截不出乾淨的頭；挑定的馬就是照 s36 的毛色挑的，所以從它裁。放大 2.7 倍偏軟，看得到 Qwen 的細點紋理；轡頭金屬環扣同上 |
| `set-shanjiao-qu-l1` | **37044** | 渠裡的水沒了、溝底乾裂；渠中間立一塊**木閘板**、一道木板橫過渠（土埂沒畫出來）；左邊土堆與乾草、右邊青秧田、左邊一排樹；沒有人、沒有房子。毛病：溝底裂土像一片片磚；渠不到一人深；沒有山（左邊是一排樹）；第 37 集的「土埂陣地」寫成閘板旁邊那道木板與兩岸的土堆。37043 只有一塊木板斜靠在土堆上（像一塊空白的牌子，第 33 條），沒有閘板 |
| `set-shentan-qu-l1` | **37043** | 免費裁切上挖出一條乾土渠，從兩根木柱之間往右上通到旱田，乾的；c26 水頭寫在鏡頭。毛病：放大 3.2 倍再編輯，很軟、對比很硬、偏 CG。37044 渠裡有一灘藍色積水 |
| `set-shentan-gongdi-l1` | **REDO**（第五輪） | 兩張都**沒有拆輪子**：水車整個還在，只在右岸多了一堆竹竿。第五輪改寫成「把大輪子拿掉」（移除比「造一半」好編）：原處只剩水裡的木架與一根光禿的木軸，右岸放著三段弧形輪緣、一捆輪輻、一疊葉板 |

## 第五輪要跑什麼（`ROUND=5 DRY=1` 跑過）

`--r5`：2 張 × 種子 **37045／37046**＝4 支，`r5.json`、`prompts-r5/`、`out-r5/`、`sheets/r5-NN.jpg`；`check_images_manifest.py` 0 錯誤；`DRY=1` 4/4 支待做、沒有開 VM。約 10–15 分鐘、1.5–2.5 CU。
- `set-shentan-gongdi-l1`：挑定的 `set-shentan-l1` 只把輪子拿掉、零件放在岸上。
- `set-shanjiao-qu-ye-l1`：挑定的 `set-shanjiao-qu-l1`（第四輪 37044）只改光成晴夜、細月。
這兩張挑定後，第 4 篇章的試鏡就全部完成。
