# e913-live 挑片後、精修前的獨立審查（第 13 集真人版）

- 審查者：沒有參與製作的獨立代理，2026-11-15。只寫這份檔，沒有改任何專案檔，沒有用 Colab、RunPod 或任何付費服務，沒有 commit。
- 這是 `_scripts/independent-review.md` 的第一次審查（挑片後、精修前）。還沒有成片，所以 cut-qa、cut-jumps、audio-qa 與音效量測都跳過；遞接物件與拿刀的鏡（s07、s09、s10、s14–s19、s23、s26、s30、s41、s42）逐 0.25 秒或逐格看過。
- 對照：
  - 稿子：`docs/videos/zhong-tian-qu-qi-e013-r2/script.md`（以〈真人版的改動（2026-11-14）〉與〈2026-11-14 獨立審稿後的修改〉為準）；`writer-tools/e013-r2/r2.py`、`review.md`。要點：唐小棠整集只拍背後、頭不轉；柴刀只在 s41、s42，在她右手（她身體畫左那側）；可以笑的只有 s03（嘴角一勾）、s11 與 s15（嘴閉著的苦笑）、s20（冷笑）、s32；紙、帳冊、木牌都空白；竹林只有星光、紙錢火與許硯的一盞燈籠。
  - 選定的草稿：`/root/mokaair-work/videos/_live-e913/zhong-tian-qu-qi-e913-dh/runpod/a/st1/out/sNN.mp4`，960×544，24 fps。42 支逐支比過 md5，跟 `picks.json` 的 `draft` 都是同一支（s05 s08 s15 s22 s27 s29 是 fix1，s35 s37 s38 s42 是 fix2，其餘 d1）。
  - 剪點 `picks.json`；挑片表 `picks-merged.tsv`、`review-picks-a.tsv`、`review-picks-b.tsv`、`fix1/review-picks.tsv`、`fix2/review-picks.tsv`；備用 `/root/mokaair-work/videos/zhong-tian-qu-qi-e913-dh/runpod/live/{d1,fix1,fix2}/out/`。
  - 每支送的參考圖從 `runpod/live/{d1,fix1,fix2}/colab-jobs.json` 讀：院子 s01–s12 是 `set-xujia-yuan-l3`；竹林 **s36 s39 s40 s41 是舊圖 `set-zhulin-fen-l2`**，s35 s37 s38 s42 是新圖 `l3`。
  - 參考圖 `production/assets/refs-live/`；第 12 集最後一鏡 `_live-e912/.../clips/s35-t1.mp4`；第 14 集 s01 的寫法 `writer-tools/e014-r2/r2.py`（SHOTS[0]、`KNIFE`、`KHAND`、`LANTERN`）。
- 做法：
  - 42 支每 0.5 秒一格的總表 `sheet-sNN.jpg`；全解析度抽格 `f-sNN*.jpg`；放大 `z-*.jpg`、`mouth-s20/s22/s27/s29.jpg`、`f-s10-hand*.jpg`（手指）、`f-s14-fall.jpg`（刨子逐格）、`f-s12-spear.jpg`（逐 0.25 秒）、`z-s23-book.jpg`、`z-s23-open.jpg`、`grid-s04/s07/s08.jpg`（40 px 格線量座標）。
  - 遮罩試做（左原片、右處理後）：`try-s01.jpg`、`try-s02.jpg`、`try-s03.jpg`、`try-s11.jpg`、`try-s12.jpg`、`try-s23.jpg`、`try-s36.jpg`、`try-s40.jpg`；`try-s02b.jpg` 是第一版（整條手臂被糊、不採用）。e912 用的「壓暗去色＋boxblur」在白天逆光的院子會變成一塊灰方塊（第一版 `try-s11.jpg` 已覆蓋），所以本集改用只做 `gblur` 不調色、四邊羽化。
  - 竹林兩張場景圖並排 `refs-grove-l2-l3.jpg`；接第 12 集 `join-e912s35-s01.jpg`。
  - 逐格跳動：每支整片做相鄰格相位相關位移（`jitter.json`，480×272 上量），再對 s26、s05、s32 裁背景區重量（只取不動的那一塊）；s26 試了 vidstab（`s26-stab.mp4`）。
  - 草稿人聲：每支 `silencedetect -35 dB / 0.2 s`（高通 120 Hz、低通 5 kHz）量有聲段，對剪點有沒有切進字；s01、s02、s28、s42 另量 0.05 秒包絡。faster-whisper 套件沒裝（安裝被拒），所以沒有逐字對；字是否完整要在精修後用耳朵再聽一次。
  - 抽格都在 `/tmp/claude-0/-home-user/e6a64eea-98ea-5986-b96b-5cdbc5d1572e/scratchpad/e913/pick-review/`。
- 秒數一律是草稿原片秒數。座標是 960×544 草稿像素，寫成 `寬:高:x:y`。剪點都是 1/24 秒的整數倍（除了下面說的 s17、s42）。挑片表已寫過、這裡確認還在的標「已知」。

## 先講結論

- **嚴重**：
  1. **s06：整個背景是兩座兵器架、紅纓長槍、槍頭**（新，挑片表說「只有畫頂露出槍頭」不對）。1.0–4.0 秒槍頭與紅纓在焦內、就在他頭兩側（`f-s06.jpg`：x 140–270 與 660–900、y 0–330）；7.0 秒後槍頭推出畫頂，紅纓與架子仍在兩側到最後一格（10.0 秒）。紅纓貼著頭髮，遮罩蓋不住；這是 10 秒長鏡（系統句＋心裡話 8.4 秒），剪點也躲不開。**重拍 s06**（提示詞見一、1）。另一支 1101 一樣有槍。
  2. **s41（舊竹林圖 l2）跟 s38、s42（新圖 l3）接不上**（新）。s41 的墳是一個尖沙堆、頂上點一支蠟燭、旁邊一塊直立木牌**有一行假字**（`f-s41.jpg`，0.25–3.95 秒都清楚）；背景是一條寬的空地小路、天空藍亮；許硯的燈籠是高圓筒形、舉在頭旁，左手**另捧一盞碟裝蠟燭**；秦霜的刀是方頭寬菜刀。下一鏡 s42 是 l3：墳是一堆石塊似的矮土丘、立一塊素木板、紙錢火在地上；燈籠是**圓球形**、低低垂在她手腕下；沒有蠟燭。兩鏡相連，墳、燈籠、光源三樣都換掉。**重拍 s41**（送 `qinshuang-portrait-l1` 與 `set-zhulin-fen-l3`，提示詞見一、2）。
  3. **s42 的最後一格跟第 14 集 s01 第一格不同**（新，挑片表已點到「右手沒舉」）。s42 末格（6.54 秒，`f-s42.jpg`）：許硯在畫左只見後腦、灰外衣肩與一點耳朵臉頰；**他的手伸在畫面中間、握著燈籠的竹柄，就在她握刀的手腕下面**，圓燈籠垂在刀下方畫面中下；**沒有手舉在頭旁**；刀身寬約三、四指、方頭（第 14 集 `KNIFE` 寫「兩指寬」）；她在畫右偏中、胸以上、嘴閉著盯他；遠處畫右是石塊矮丘、直立素木板、地上紙錢火。第 14 集 s01 的 `comp` 寫「his right hand raised open beside his head on screen right」，照現在寫會從無手跳到舉手、燈籠從刀下跳到他身側。**建議改第 14 集 s01（不重拍 s42）**，英文見一、3。
- **中等**（不花錢能處理）：
  4. **s02：井後一排三、四支長槍、槍頭在焦內**（已知，但挑片表寫「虛焦」偏輕）。3.0–8.0 秒都在 x 600–790、y 195–500，槍頭在 y 200–260。gblur 遮罩可用（`try-s02.jpg`；5.5–6.6 秒他伸出的手臂在 y 430 以下，框只到 y 425，手臂不受影響；框下緣下面剩幾根斜木腳，讀不成槍）。可選重拍（一、4）。
  5. **s11：畫右一排紅纓長槍、槍頭在焦內**（已知「虛焦」偏輕）；另外 2.5–8.0 秒一路**露齒**笑著說（稿子許「苦笑」，r2 寫嘴閉著的半笑、不露牙）。遮罩 `try-s11.jpg` 蓋掉大半，框左緣 x 700 外仍留一兩個槍尖（2.5、4.0 秒），7.9 秒框左緣貼著他的耳朵，再往左會糊到頭髮；勉強可用。**可選重拍 s11**（一、5），不重拍就用遮罩。
  6. **s03：屋牆斜靠三、四支槍（槍頭清楚）**（已知）。位置 0.5–1.5 秒在 x 290–365（他的後腦在 x 0–260），2.0 秒後在 x 185–310。分兩段的 gblur 遮罩可用（`try-s03.jpg`，1.5 秒還留一點細影）。她 4.3–6.3 秒露牙笑（已知，稿子只許嘴角一勾）：接受。
  7. **s01：2.5–3.5 秒畫右緣兵器架腳**（已知），x 870–960、y 324–544；右緣不羽化的 gblur 遮罩 `try-s01.jpg`，乾淨。另：**草稿人聲 2.25–3.35 秒是秦霜那句的開頭，`start@2.5` 切掉第一個字**（`env` 量到 2.25 秒 −21 dB 起）。這是全景、她大半背對，**建議 s01 走 voice_off、鋪錄音 a01**（3.40 秒＋0.5≤4.0），剪點不動；若要用草稿原聲，就改 `start@2.25`（54 格，剩 4.25 秒），架腳框的 `enable` 一樣到 3.5。
  8. **s12：3.5–4.0 秒畫左緣一支長槍（槍頭清楚）**（新，`f-s12-spear.jpg`；4.25 秒出畫）。不能往後剪（a13 4.36 秒，剩 3.75 秒不夠）。左緣不羽化的細條遮罩 `0:50` 寬 50、到 4.25 秒（`try-s12.jpg`）。
  9. **s23：帳冊白籤條上一行假字，5.75 秒起帳冊翻開、露出內頁直行假字**（已知，`z-s23-book.jpg`、`z-s23-open.jpg`）。剪點躲不開（a24 4.76 秒）。遮罩 `335:335` 210×165 從 3.0 秒到底（`try-s23.jpg`），帳冊變成一塊糊的藍與米黃、粉緞帶經過的那段也一起糊，讀得通。可選重拍（一、6）。
  10. **s26：畫面一格一格上下跳**（已知）。背景區量：剪點內 95 格有 64 次上下方向反轉、最大 ±4 px（480 寬）；vidstab `smoothing=12:zoom=3` 後反轉降到 12 次、最大 3 px（`s26-stab.mp4`）。**剪接前加穩定**（vf 在文末）。其他 41 支沒有這種一格一正一負的跳：s05、s11、s15–s18、s21、s22 的位移是人動或慢推；s32 是跟拍走路的上下晃（8–10 格一個週期），不是逐格跳。s30 4.25 秒指印一下子跳出（已知，一格）。
  11. **s40：背景竹林裡兩點暖色燈火**（已知，`f-s40.jpg`；0.5 秒在 x 490、y 90，3.5 秒移到 x 564、y 150），稿子竹林沒有別的光；紙錢火燒在墳頂上（l2）。兩段 gblur＋壓暗的遮罩（`try-s40.jpg` 只做了 gblur，光點變成柔的光斑，仍看得出，所以文末的 vf 加了 `eq=brightness=-0.12`）。可選用 l3 重拍（一、7）。
  12. **s36：木牌上有似字的墨痕**（已知，`z-s36.jpg`，x 535–565、y 225–300）；小遮罩 `try-s36.jpg`。s36 用 l2：墳是一個發光的光滑土丘、木牌是橘紅細條；跟 s38、s42 的石塊矮丘不同，但這是高角度大全景、很小、在 s37（許硯近景）前面，接受。
- **輕微、接受**：s09 撥算盤的手骨節粗、青筋重，像年長的人（插鏡，已知）；s14 的刨子是素木塊、s15 是有把手的木刨、s16 是金屬刀片的長刨（偏現代西式）、s17 是帶孔方塊、s19 是一塊平板，道具前後不一（他一直抱著，觀眾多半不追）；s07 一疊十本、s08 桌上是兩疊（輕微）；s20 石木匠 3.0–4.5 秒一邊說一邊和氣地笑（稿子許冷笑，已知）；s29 4.0–5.4 秒露一點牙的服氣笑（已知）；s34 的燈籠是高圓筒、s35 起是圓球（夜裡換景，接受）；s35 燈籠沒用袖子遮、偏亮（已知，調色壓）；s04、s10、s12 唐小棠 4 秒後露耳朵與臉頰外緣，眼、嘴都沒露（對）。
- **建議重拍**：**s06**（必拍）、**s41**（必拍）；可選 s11、s02、s23、s40。s42 不重拍，改寫第 14 集 s01。
- **每場的結尾**：
  - 第一場（s12）：唐小棠背影抽一本帳冊夾在左臂，許硯在她正前方，讀得懂。
  - 第二場（s32）：兩人背影、許硯 4.0–5.0 秒在她肩旁比大拇指，讀得懂（兩人是往前方店面走，不是沿巷走遠，已知）。
  - 第三場（s42）：柴刀停在他頸側、她冷冷說完盯著他，讀得懂；接第 14 集見嚴重 3。
- **接第 12 集**（`join-e912s35-s01.jpg`）：第 12 集 s35 是天快亮的近景、正面；本集 s01 是清晨逆光的全景，院子、屋子、井、石桌對得上，時間跳一個時辰。熄火把畫成「桿上冒煙的金屬碗」（已知，像小火盆），接受。

## 一、嚴重與重拍

1. **s06 重拍**（送 `xuyan-angle-a-l1`、`xuyan-angle-b-l1`；**不送場景圖**——`set-xujia-yuan-l3` 井邊那塊斜靠的木板加一根竿子，正是 s02、s06、s11 背景長出槍架的位置，近景用不到場景圖；買 10 秒；新種子例如 9131401／9131402）：
   > Close-up of Xu Yan, in his old plain grey cloth outer coat over his faded blue-grey scholar's robe, eyes red-rimmed after a sleepless night, framed from the chest up with clear space above his topknot, his face three-quarter to screen right, never the lens; slow push in. Behind him only a low woven fence of thin pale bamboo stakes tied with twine, soft and out of focus, its top below the line of his shoulders, and beyond it an open field of cut stubble and a wide pale sunrise sky that fills the whole upper half of the frame around his head; cool golden morning light from screen right rims his cheek.
   >
   > Motion: he stops mid-step; his eyes roll up once toward the sky; then he closes his eyes and lets out one long slow breath through his nose, his shoulders sinking; then he opens his eyes, brows drawn together, tired and stubborn; his lips stay pressed together from the first frame to the last, no talking, no mouthing words, no smile.
   - 挑片時逐格看：背景有沒有任何直立的桿子、紅色穗子；2.0 秒翻白眼、3–6 秒閉眼吐氣、7 秒後睜眼；嘴整鏡閉著。
2. **s41 重拍**（送 `qinshuang-portrait-l1`、`set-zhulin-fen-l3`；許硯不點名、不送圖；買 6 秒；種子例如 9131401／9131402）。刀的寫法改成跟 s42 一樣寬，免得 s41→s42 刀變窄：
   > Medium shot, locked off, the whole action inside the frame, deep in the bamboo grove at night, lit only by cold blue starlight, a small fire of blank paper burning on the bare earth, and one paper lantern. In the left foreground, from close behind, one young man seen only from behind: the back of his black topknot and the shoulders of his old plain grey cloth coat, his face never in the frame, his back against a thick bamboo stalk at the left edge, one round white paper lantern hanging from its bamboo handle low in his left hand, a small candle glowing inside it. On screen right a few steps away, beside the low grave mound of piled earth and stones with one small upright blank wooden plank, Qin Shuang, in her dark brown cross-collared short jacket, wide leather belt, black trousers and boots, high ponytail, already half risen from her knees, her face three-quarter to screen left toward him, never the lens; cold and fierce: brows drawn down, eyes locked on him, lips pressed shut. In her right hand, which is the hand on the screen-left side of her body nearest him, one old chopping knife with a short plain wooden handle and a dark iron blade about three fingers wide and a little longer than a palm, a thick blunt back and a squared tip, held low at her side. Behind her only dense dark bamboo stalks fading into black night; the paper fire on the bare earth in front of the mound and his lantern are the only lights.
   >
   > Motion: she springs up to her full height and takes two fast steps toward him, the knife rising level in the same right hand; he jerks back and his shoulders hit the bamboo stalk, the lantern swinging once in his left hand; both mouths stay closed the whole shot; the knife stays in her right hand.
   - 挑片時看：墳是不是 s38、s42 那種石塊矮丘＋素木板、火在地上；燈籠是不是圓球、只有一盞；有沒有蠟燭碟；木板上有沒有字；刀在她身體畫左那側。
3. **s42 接第 14 集 s01**：s42 不動（`start@1.5`，到片尾）。改 `writer-tools/e014-r2/r2.py` SHOTS[0]（由寫稿端決定，這裡只提建議）：
   - `comp` 的手與燈籠改成接 s42 末格：
     > …from close behind {HE_BACK}, the round white paper lantern hanging from its bamboo handle in his left hand, which is held up in the middle of the frame just under her wrist, the lantern low below the knife; his right hand not yet in the frame; facing us a little right of the middle Qin Shuang…
   - `motion` 的開頭改成在第一聲鼓時舉手（第 14 集 s02、s04 要的「右手舉在頭旁」由這一鏡交代）：
     > at the first of three slow distant drumbeats his open right hand rises slowly into the frame on screen right and stops beside his head, below the line of her eyes; at the third beat his shoulders jerk once…
   - `KNIFE` 的「two fingers wide」跟 s41、s42 畫出來的刀（三、四指寬、方頭）不一樣。建議第 14 集改寫成「a dark iron blade about three fingers wide with a squared tip」，或接受第 14 集起刀變窄。
   - 其他已一致：從他背後拍、她右手（她身體畫左那側）平舉、刃口在他頸側、遠處墳與快燒完的紙錢火、嘴閉著。
4. **s02 可選重拍**（送 `xuyan-portrait-l1`、angle a/b；不送場景圖或送一張畫掉竿子的院子圖；6 秒）：
   > Medium shot, slow push in, the morning yard of the Xu farmhouse at sunrise, low cool golden light from screen right: Xu Yan, in his old plain grey cloth outer coat over his faded blue-grey scholar's robe, eyes red-rimmed, framed from the waist up, turns toward the yard gate off screen right and takes one step after the woman leaving, his face three-quarter to screen right, never the lens; worried, brows drawn together, no smile. Behind him only the plain packed-earth yard wall running straight across the frame, its whole length bare and smooth, and above it the pale sunrise sky and the stubble field.
   >
   > Motion: he raises his right hand toward screen right as if to stop her and speaks a short Mandarin line, 「妳一個人去？路上要是碰到錢家的人呢？」, his lips, jaw and cheeks moving clearly with every syllable; after the last word his lips close into a firm line and his hand stays raised.
5. **s11 可選重拍**（送 angle a/b；背景照 fix1 s08 成功的寫法；6 秒）：
   > Close-up of Xu Yan, in his old plain grey cloth outer coat over his faded blue-grey scholar's robe, eyes red-rimmed, framed from the chest up, his face three-quarter to screen left toward the young woman off screen left, never the lens; wry and rueful: one corner of his mouth tucked in, lips together between words, teeth showing only while forming a word. Behind him only the bare earthen house wall with its small lattice window and the stacked woodpile below it, soft and out of focus; the wall is completely bare.
   >
   > Motion: first he scratches the back of his neck with his right hand and glances once toward the yard gate on screen right; then he lowers the hand and speaks a short Mandarin line, 「他最恨秀才？那我上門，不是送去挨罵嗎？」, his lips, jaw and cheeks moving clearly with every syllable; after the last word he presses his lips together in a small closed-mouth half smile.
6. **s23 可選重拍**：照 r2 原意寫「帳冊封底朝我們、合著」，背景不變；不重拍就用遮罩。
7. **s40 可選重拍**（送 `qinshuang-portrait-l1`、`set-zhulin-fen-l3`；6 秒）：
   > Close-up of Qin Shuang, in her dark brown cross-collared short jacket, high ponytail, kneeling with the small paper fire burning on the bare earth just beside her on screen right and the low grave mound of piled earth and stones behind it; the warm firelight from below and cold starlight from above; behind her only dense dark bamboo stalks fading into black night. Motion: she snaps her head round toward screen left, a glint of tears in her eyes, and in the next instant her gaze turns cold and hard; her lips stay pressed together the whole shot.

## 二、兵器、紙、道具（逐鏡）

| 鏡 | 看到的 | 處理 |
| --- | --- | --- |
| s01 | 0–3.5 秒右緣兵器架（剪點後只剩 2.5–3.5 的架腳） | 遮罩（文末） |
| s02 | 井後三、四支長槍、槍頭在焦內，全程；屋簷下垂一排深色穗串 | 遮罩；可選重拍 |
| s03 | 屋牆三、四支槍＋辣椒串（辣椒是實物） | 分兩段遮罩 |
| s04 | 0–2.5 秒左緣架子（剪掉）；帳冊白籤條三個小點 | 接受；要糊見文末 |
| s05 | 井後牆外一根素木棍＋板 | 接受 |
| s06 | 兩座兵器架、紅纓、槍頭 | **重拍** |
| s07 | 最上一本籤條淡淡似字 | 可選糊（文末） |
| s08 | 籤條空白；兩疊帳冊 | 接受 |
| s09 | 0–0.458 秒院子全景（有長槍），0.5 起剪掉 | 對 |
| s10 | 豎的是食指（`f-s10-hand2.jpg`，拇指收在左、中指無名指小指彎在右），不是中指 | 對 |
| s11 | 一排紅纓長槍 | 遮罩；可選重拍 |
| s12 | 3.5–4.0 秒左緣長槍 | 左緣細條遮罩 |
| s13、s16、s20、s21、s24 | 牆上木牌只有孔，沒有字（`f-s16-plaque.jpg`）；牆上鋸子 | 對 |
| s14–s19 | 刨子五種樣子 | 接受 |
| s22、s25、s27、s29、s31 | 素竹竿、鋸子、夾具，沒有刀斧 | 對 |
| s23 | 籤條假字、5.75 秒後內頁假字 | 遮罩；可選重拍 |
| s26 | 木框＋密線＋柳葉，沒有字 | 對；加穩定 |
| s30 | 紙空白、一個紅指印 | 對 |
| s36 | 木牌似字墨痕 | 小遮罩 |
| s40 | 竹林兩點燈火 | 遮罩＋壓暗；可選重拍 |
| s41 | 木牌一行假字、墳頂蠟燭、多一盞蠟燭碟、筒形燈籠 | **重拍** |
| s42 | 刀在她右手（畫左側）；刀寬、方頭；燈籠吊在她手腕下 | 接受；改第 14 集 s01 |

## 三、人、紅串、閃粒、笑、看鏡頭

- **分身、多出來的人**：選中的 42 支沒有。
- **紅珠串、閃粒**：選中的都沒有。看到的紅串只有 s03 簷下的辣椒串與玉米（實物）；s02 簷下是深色穗串（不是紅珠）。fix2 s37 選中的 1301 沒有珠串（1302 有，落選，對）。
- **唐小棠背影**：s04、s10、s12、s21、s23、s32 頭不轉；s04 5.5 秒後、s10 4.5 秒後、s12 5.0 秒後露耳朵、下顎線與臉頰外緣，沒有眼、嘴（`f-s04-tang.jpg`、`f-s10-tang.jpg`、`f-s12-left.jpg`），接受。s13、s25 她露臉、不笑，對。
- **石木匠笑場**（逐 0.5 秒看嘴）：s16 咬牙不笑；s20 3.0–4.5 秒邊說邊笑（准冷笑，偏和氣，接受）；s22（fix1）整鏡皺眉、嘴角下拉、5.25 秒哼一聲，**不笑，對**（`mouth-s22.jpg`）；s24 7.6 秒後一點得意（輕微）；s27（fix1）瞇眼瞪、罵人的嘴型，**不笑，對**（`mouth-s27.jpg`）；s29（fix1）0.5–3.0 皺眉看板、3.5 秒起服氣地笑、4.0–4.5 秒露一點牙（`mouth-s29.jpg`，接受）；s31 不笑。
- **許硯笑**：s11 露齒（中等 5）；s15 嘴閉的半笑（准）；s28 4.5、6.5 秒嘴角微揚（准）。
- **秦霜**：s03 露牙笑（已知，接受）；s38、s40、s42 不笑。
- **看鏡頭**：s08 0.5–4.0 秒臉近正面、眼神近鏡頭（`f-s08-face.jpg`，中等偏輕，接受）；s10 他正對她（也就是鏡頭），接受；s18 大特寫，接受；s40 1.0–1.5 秒（接受）。
- **柴刀手**：s41、s42 都在她右手、她身體畫左那側（s41 `f-s41.jpg` 低握在畫左側；s42 平伸到他頸側）。s41 重拍時照寫。

## 四、竹林 s35–s42 前後接戲

| 鏡 | 場景圖 | 墳 | 火 | 燈籠 | 背景 |
| --- | --- | --- | --- | --- | --- |
| s35 | l3 | 不入鏡 | 遠處一排暖光點 | 圓球，竹柄吊著，未遮光 | 密竹＋藍夜 |
| s36 | **l2** | 發光的光滑土丘＋橘紅細木牌（似字） | 墳前地上 | — | 高角度小路兩側密竹 |
| s37 | l3 | 不入鏡 | — | 圓球 | 密竹＋藍夜 |
| s38 | l3 | 石塊矮丘＋斜靠的素木板 | 地上 | — | 密竹 |
| s39 | l2 | 插鏡 | — | — | 落葉地 |
| s40 | **l2** | 光滑土丘，火在墳頂 | 墳頂 | — | 竹子＋**兩點燈火** |
| s41 | **l2** | **尖沙堆＋假字木牌＋頂上蠟燭** | 蠟燭 | **筒形＋另一盞蠟燭碟** | 寬空地、亮藍天 |
| s42 | l3 | 石塊矮丘＋直立素木板 | 地上 | 圓球，吊在她手腕下 | 密竹 |

- s36、s39 能接：一個高角度大全景、一個地面插鏡，墳的樣子在 s36 很小。
- s40 勉強：火在墳頂、兩點燈火；遮罩後接受，或重拍。
- **s41 不能接**（嚴重 2）：重拍。
- 墳的形狀、木板直立或斜靠，在 l3 的三鏡（s38 斜靠、s42 直立）之間也有一點不同，接受。

## 五、各場檢查結果

- **第一場（s01–s12，院子清晨）**：逆光晨光、柿子樹、井在右、屋子在左，軸線一致。槍架出現在 s01（剪剩右緣）、s02、s03、s06、s11、s12（3.5–4.0），根源是 `set-xujia-yuan-l3` 井邊斜靠的木板＋一根竿子（`refs-live/set-xujia-yuan-l3.png` x 860–1000），加上提示詞裡的否定名詞；fix1 的 s05、s08 用正面寫背景就沒有槍。院門在屋子右邊（後牆中偏左），s01 秦霜牽馬從那裡出去，對。
- **第二場（s13–s32，巷子與簷下工作台）**：門在畫右、巷子往畫左延伸；唐小棠在畫左、石木匠在畫右，s21、s23 軸線對。許硯第二場沒披灰外衣，對。
- **第三場（s33–s42，夜）**：s33 門縫主觀、s34 取燈籠，夜色對；竹林見第四節。

## 六、每鏡處理總表

| 鏡 | 種子 | 等級 | 做法 |
| --- | --- | --- | --- |
| s01 | 9131102 | 中等 | 照 picks.json；**voice_off 鋪 a01**（或 `start@2.25` 用原聲）；右緣遮罩到 3.5 秒 |
| s02 | 9131101 | 中等 | 照 picks.json；遮罩；可選重拍 |
| s03 | 9131102 | 中等 | 照 picks.json；兩段遮罩；露牙笑接受 |
| s04 | 9131101 | 輕微 | 照 picks.json；籤條可選糊 |
| s05 | 9131201 | — | 照 picks.json |
| s06 | 9131102 | **嚴重** | **重拍**（10 秒） |
| s07 | 9131102 | 輕微 | 照 picks.json；籤條可選糊 |
| s08 | 9131201 | 輕微 | 照 picks.json |
| s09 | 9131102 | 輕微 | 照 picks.json |
| s10 | 9131101 | — | 照 picks.json |
| s11 | 9131101 | 中等 | 照 picks.json；遮罩；可選重拍 |
| s12 | 9131101 | 中等 | 照 picks.json；左緣遮罩到 4.25 秒 |
| s13–s16 | 照 picks | — | 照 picks.json |
| s17 | 9131101 | — | 剪點寫成整格：`start@2.75`，不寫 end（6.583 不是整格，158/24＝6.5833 就是片尾） |
| s18–s22 | 照 picks | 輕微 | 照 picks.json（s20 笑接受） |
| s23 | 9131101 | 中等 | 照 picks.json；遮罩 3.0 秒起；可選重拍 |
| s24、s25 | 照 picks | — | 照 picks.json |
| s26 | 9131101 | 中等 | 照 picks.json；**加穩定** |
| s27–s35 | 照 picks | 輕微 | 照 picks.json |
| s36 | 9131101 | 輕微 | 照 picks.json；木牌小遮罩 |
| s37–s39 | 照 picks | — | 照 picks.json |
| s40 | 9131101 | 中等 | 照 picks.json；燈火遮罩＋壓暗；可選重拍 |
| s41 | 9131101 | **嚴重** | **重拍**（l3，6 秒） |
| s42 | 9131302 | 嚴重（接點） | 剪點寫成整格：`start@1.5`，不寫 end；改第 14 集 s01 |
| 水平翻轉 | — | — | 不建議：每一鏡都有交領的人 |

剪點對草稿人聲：除了 s01（見中等 7），沒有剪點切進有聲段；s33、s34 的起點落在草稿雜音裡，但那兩鏡畫面沒有人說話、原聲會被靜音，不影響。s02、s28 的句尾在 7.85 秒前降到 −40 dB 以下，片尾 8.0 沒有切字。長度：各鏡剪後長度都 ≥ 錄音＋0.5 秒（挑片表已核），s01 voice_off 時 4.0 ≥ 3.90。

## 給 refine-prep.py 的 review2-trims.tsv（建議）

只列要改的；其餘照 `picks.json`。

```
shot	choice	reason
s06	RETAKE	pick-review：兩座兵器架、紅纓、槍頭在焦內貼著頭，整鏡 10 秒躲不開也遮不掉；不送場景圖、背景寫成低竹籬笆與天空重拍
s17	9131101	start@2.75 pick-review：end 6.583 不是整格（片尾就是 158 格），拿掉 end
s41	RETAKE	pick-review：舊竹林圖 l2 的尖沙堆、假字木牌、墳頂蠟燭、筒形燈籠＋蠟燭碟，跟 s38、s42 的 l3 接不上；用 l3 重拍，刀寫成跟 s42 一樣寬
s42	9131302	start@1.5 pick-review：end 6.583 不是整格（片尾就是 158 格），拿掉 end；接第 14 集 s01 改寫第 14 集，不重拍
```

若 s01 決定用草稿原聲，加一列 `s01	9131102	start@2.25 end-before@6.5 pick-review：草稿人聲 2.25 秒起，2.5 切掉第一個字`。

剪接時另外套（不放進 TSV；座標是 960×544 草稿，時間是草稿原片秒數。若先剪再套，`enable` 的秒數要減掉 `start`；精修放大後再套，座標與 sigma 乘上倍數；已試做的看 `try-sNN.jpg`）：
- s01（右緣不羽化）：
  `split[a][b];[b]crop=90:220:870:324,gblur=sigma=12,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(X\,min(Y\,H-Y))/20)'[c];[a][c]overlay=870:324:enable='lt(t,3.5)'`
- s02：
  `split[a][b];[b]crop=230:255:580:170,gblur=sigma=16,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/40)'[c];[a][c]overlay=580:170`
- s03（兩段）：
  `split[a][b];[b]crop=160:200:270:105,gblur=sigma=12,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/30)'[c];[a][c]overlay=270:105:enable='lt(t,2.0)',split[a][b];[b]crop=150:200:180:105,gblur=sigma=12,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/30)'[c];[a][c]overlay=180:105:enable='gte(t,2.0)'`
- s11（不重拍時）：
  `split[a][b];[b]crop=250:350:700:40,gblur=sigma=16,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/40)'[c];[a][c]overlay=700:40`
- s12（左緣不羽化）：
  `split[a][b];[b]crop=50:380:0:50,gblur=sigma=10,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(W-X\,min(Y\,H-Y))/15)'[c];[a][c]overlay=0:50:enable='lt(t,4.25)'`
- s23：
  `split[a][b];[b]crop=210:165:335:335,gblur=sigma=10,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=335:335:enable='gte(t,3.0)'`
- s36：
  `split[a][b];[b]crop=50:90:527:218,gblur=sigma=6,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/12)'[c];[a][c]overlay=527:218`
- s40（兩段；試做只做了 gblur，這裡加了壓暗，精修後再看一次）：
  `split[a][b];[b]crop=110:110:470:40,eq=brightness=-0.12,gblur=sigma=10,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=470:40:enable='lt(t,2.5)',split[a][b];[b]crop=90:110:520:90,eq=brightness=-0.12,gblur=sigma=10,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,min(Y\,H-Y))/25)'[c];[a][c]overlay=520:90:enable='gte(t,2.5)'`
- s04、s07 籤條（可選，沒試做，框是從 `grid-s04.jpg`、`grid-s07.jpg` 量的）：s04 `crop=100:50:450:400` 套在 `lt(t,4.5)`、`crop=110:54:415:490` 套在 `between(t,4.5,7.0)`；s07 `crop=200:80:270:195` 套在 `gte(t,1.0)`；都用上面的 gblur sigma 6、羽化 12。
- s26 穩定（剪後的 4.0–8.0 那段，`s26-stab.mp4` 試過）：
  `vidstabdetect=shakiness=8:accuracy=15:result=s26.trf`，第二遍 `vidstabtransform=input=s26.trf:smoothing=12:zoom=3:optzoom=0`。
- 遮罩一律在精修後、剪接時套，套完逐 0.25 秒看框邊（s02 5.5–6.6 秒的手臂、s11 7–8 秒的耳朵、s03 1.5–2.0 秒的換框）。
