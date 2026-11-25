# e912-live 挑片後、精修前的獨立審查（第 12 集真人版）

- 審查者：沒有參與製作的獨立代理，2026-11-15。只寫這份檔，沒有改任何專案檔，沒有用 Colab、RunPod 或任何付費服務，沒有 commit。
- 這是 `_scripts/independent-review.md` 的第一次審查（挑片後、精修前）。還沒有成片，所以 cut-qa、cut-jumps、audio-qa 與音效量測都跳過；遞接物件的鏡（s14、s15、s17、s18、s22、s24、s29、s33、s34）仍然逐格看過。
- 對照：
  - 稿子：`docs/videos/zhong-tian-qu-qi-e012-r2/script.md`（以〈真人版的改動（2026-11-14）〉與〈2026-11-14 獨立審稿後的修改〉為準）、`storyboard.md`、`video.json`；`writer-tools/e012-r2/review.md`、`r2.py`。真人版要點：唐小棠台詞鏡（s06、s14、s29）只拍背後、頭不轉；兵器都不拍；紙上沒有字；畫外句（s02、s10、s28、s30–s35）畫面上的人整鏡不動嘴；可以笑的只有 s04（冷笑）、s11、s21（乾笑，嘴角抽動、幾乎不露牙）、s22（嘴角一點壞笑、不露牙）、s31；其他一律不笑；交領角色不翻轉。
  - 選定的草稿：`/root/mokaair-work/videos/_live-e912/zhong-tian-qu-qi-e912-dh/runpod/a/st1/out/sNN.mp4`，960×544，24 fps。35 支逐支比對過 md5，跟 `picks.json` 的 `draft` 都是同一支（s02 s04 s22 s24 s26 s33 是 fix1，其餘 d1）。
  - 剪點：`/root/mokaair-work/videos/_live-e912/zhong-tian-qu-qi-e912-dh/picks.json`。
  - 挑片表：`picks-merged.tsv`、`fix1/review-picks.tsv`、`review-picks-a.tsv`、`review-picks-b.tsv`；重拍規格 `fix1/spec.json`。
  - 備用草稿：`/root/mokaair-work/videos/zhong-tian-qu-qi-e912-dh/runpod/live/{d1,fix1}/out/`（重拍六鏡兩個種子全看；s01、s05、s21 另看了 1102）。
  - 錄音：`/root/mokaair-work/videos/zhong-tian-qu-qi-e912-dh/audio/zq912aNN.wav`（32 句，silencedetect −40 dB 量出每句最後一個字的結束秒數）。
  - 參考圖：`production/assets/refs-live/`（9 張人物定妝照並排 `refs-people.jpg`、夜院 `refs-set.jpg`）。
  - 第 11 集最後一鏡：`/root/mokaair-work/videos/_live-e911/zhong-tian-qu-qi-e911-dh/clips/s35-t1.mp4`（1312×736，4.75 秒）。
- 做法：
  - 35 支選定草稿每 0.5 秒一格的總表 `sheet-sNN.jpg`；重拍六鏡兩個種子每 0.5 秒並排 `pair-sNN-01/02.jpg`（左 1201、右 1202）。
  - 嘴與笑逐 0.125 秒或逐格（1/24 秒）放大：`mouth-s04-1201*.jpg`、`mouth-s22-120{1,2}.jpg`、`mouth-s24-1201*.jpg`、`mouth-s26-120{1,2}.jpg`、`mouth-s33-1201.jpg`、`mouth-s01.jpg`、`mouth-s21.jpg`、`mouth-s13.jpg`、`f-s13.jpg`、`face-s02-120{1,2}.jpg`、`aling-s02-1201.jpg`、`tang-s02-end.jpg`、`tang-s24-1201.jpg`、`face-s05.jpg`、`hair-s01.jpg`。
  - 帽子：`z-s22-hat.jpg`（s22 前景帽子三支並排）、`hat-s26-2.0.jpg`、`s26-1201-six.jpg`、`hat-compare-s12-s23-s26.jpg`。
  - 兵器與背景：`grid-s04-*.jpg`、`f-s04-1201.jpg`、`grid-s22-1202.jpg`、`f-s22.jpg`、`f-s26-1201.jpg`、`z-s08-right.jpg`、`z-s01-right.jpg`、`grid-s01-1.0.jpg`、`f-s25.jpg`、`f-s30-34.jpg`、`z-red-strings.jpg`（紅串放大）、`z-s22-plaques.jpg`（屋牆小框）、`z-s03-hand.jpg`、`f-s17.jpg`、`f-s02-1202.jpg`。
  - 遮罩試做（左原片、右處理後）：`try-s04.jpg`、`try-s26.jpg`、`try-s08.jpg`、`try-s01.jpg`、`try-s22-crop.jpg`（s22 遮罩蓋不住紅纓，不採用）、`try-s22-crop736.jpg`（s22 退路裁切）。
  - 接第 11 集：`join-e911s35-s01.jpg`、`sheet-e911-s35.jpg`。
  - 逐格跳動：每支整片做相鄰格相位相關位移（`jitter.txt`），再對每支取一條背景橫線做時間切片（`slit/sNN-row.jpg`，總覽 `slit-rows-a.jpg`、`slit-rows-b.jpg`）；靜止背景的線都是平滑的，沒有一格一格左右抖的鋸齒（第 10 集 s13 那種）。
  - 抽格與放大圖都在 `/tmp/claude-0/-home-user/e6a64eea-98ea-5986-b96b-5cdbc5d1572e/scratchpad/e912/pick-review/`。
- 秒數一律是草稿原片的秒數（有 `start@` 的鏡沒有扣掉）。座標用 960×544 草稿像素，寫成 `寬:高:x:y`。剪點寫成 1/24 秒的整數倍（四位小數，floor／ceil 後不會偏一格）。
- 挑片表已經寫過、這裡確認還在的問題標「已知」。

## 先講結論

- **嚴重**：
  1. **s22：fix1 要修的帽子沒修好**（新）。fix1 重拍 s22 的理由是「前景官帽是布巾帶兩條長垂帶、不是胡縣令的展翅幞頭」；選中的 1202（和 1201）前景帽子後面**仍然垂下兩條長黑帶**，一路垂到肩上（`z-s22-hat.jpg`，0–9 秒都在畫右 x 750–960），跟 s12、s23、s26 胡縣令的平翅官帽接不上。另外：
     - 背景畫左一整排紅纓長槍（四、五支，0–5.5 秒，x 30–230、y 50–200），畫右還有一支單獨的從 x 390 慢慢移到 180（0–8 秒）；3.0 秒起畫左有一個三腳火盆在燒。
     - 前景的人 6.5 秒起轉頭，臉頰、鼻樑、下巴的鬍子露出來（稿子寫頭始終不轉）。
     - 遮罩蓋不乾淨：紅纓在 y 150–215，下面就是火盆的火和許硯的肩（`try-s22-crop.jpg`）。
     - **修法：重拍 s22**（英文提示詞見嚴重 1）。退路：1202 整支 `crop=736:414:0:30` 放大 1.30 倍把帽子與垂帶裁掉（`try-s22-crop736.jpg`），代價是變成許硯單人、4 秒後頭頂和錢袋貼邊、槍與火盆還在。
  2. **s04：1.375 秒切進去還在大笑，背景整排紅纓長槍**（新）。fix1 挑片寫「開頭咧嘴，1.4 秒後收住」；逐格看，咧嘴露齒笑一直到 2.5 秒，2.25–2.625 秒張大嘴笑（`mouth-s04-1201.jpg`、`mouth-s04-1201b.jpg`），2.875 秒起才轉成側臉、嘴型正常。背景畫右整排六支紅纓長槍從頭到尾都在（x 760–960、y 75–200，`grid-s04-3.0.jpg`）。兩個種子都有槍架（1202 還更多、而且大笑到 4.5 秒）。
     - **修法（不花錢）**：`start@2.75`（2.75 秒嘴張成「好」的口型，可以當成開口喊）；剩 7.375 秒，錄音最後一個字在 7.85 秒，本鏡放慢約 1.07 倍（`slow_max` 1.1 以內），或讓句尾 0.5 秒蓋到 s05 開頭。槍架用局部模糊去色（vf 在文末，`try-s04.jpg` 試過：刃和紅纓變成看不清的灰影；框在天空那一段比原本略灰，精修後再看一次）。
  3. **s26：選中的 1202 笑場，1201 才對**（新，跟 fix1 挑片相反）。
     - 1202：1.5–2.5 秒咧嘴露齒、3.25–4.25 秒露齒笑、5.5–6.25 秒嘴角上揚，眼睛大半時間直視鏡頭（`mouth-s26-1202.jpg`）。稿子寫不笑。
     - 1201：整段皺眉齜牙、嘴角下撇（`mouth-s26-1201.jpg`），就是 fix1 要的「皺眉咬緊下顎嘴角下撇」；5.0–6.75 秒眼睛往下別開，7.0 秒往畫右出畫。
     - fix1 挑片說「1201 沒有帽翅」不對：1201 的帽子兩邊都有展翅（`hat-s26-2.0.jpg`、`hat-compare-s12-s23-s26.jpg`），只是暗、略往下彎，0–0.5 秒右翅在暗背景裡看不太出來。
     - **修法：換 1201**，整支用（錄音 4.96 秒）。兩支畫右上都有紅纓長槍加辣椒串（1201 在 x 730–880、y 0–200），用局部模糊去色（vf 在文末，`try-s26.jpg` 試過）。
- **中等**：
  4. **s02：換 1202、`start@2.0`**（新）。1201 的阿令 3.0–6.5 秒直視鏡頭、唐小棠也近乎看鏡頭（`aling-s02-1201.jpg`、`face-s02-1201.jpg`），畫右一個三腳火盆在燒（規格寫畫面裡不能有火，`full-s02-1201-3.0.jpg`）。1202 三人四分之三側臉朝畫右、眼睛不看鏡頭（`face-s02-1202.jpg`），2.0 秒以後畫面裡沒有火盆（`f-s02-1202.jpg`）。剩 4.583 秒，錄音 4.01 秒。兩支都沒有笑：唐小棠結尾是咬唇要哭（`tang-s02-end.jpg`）。代價見中等 4。
  5. **s24：5.417 秒起許硯笑**（新）。1201 逐格看 5.458 秒起嘴角上揚、閉嘴微笑到片尾（`mouth-s24-1201-f.jpg`），稿子寫不笑。**修法**：`end-before@5.4167`（130 格，剩 5.417 秒，錄音 4.32 秒）。
  6. **s01：許硯說「不換」時一直直視鏡頭**（新）。0–4.4 秒臉正對鏡頭、眼珠也正對（`mouth-s01.jpg`、`grid-s01-1.0.jpg`），4.4 秒才轉頭看胡縣令；稿子寫正眼看胡縣令說。1102 一樣看鏡頭、背景槍更多（`alt-s01-1102.jpg`）。接第 11 集 s35（他在那支也正對鏡頭）讀得通。**接受**；若站主在意，**可選重拍 s01**（英文提示詞見中等 6）。畫右背景黑衣人腰間一把帶鞘的刀（0–4.6 秒，x 820–945、y 345–425），可選局部模糊（`try-s01.jpg`）。
  7. **s05：唐小棠整鏡直視鏡頭**（新）。0.25–6.5 秒臉和眼睛都正對鏡頭（`face-s05.jpg`），0.75–1.25、3.25–3.75 秒嘴微張（沒有說話的口型）。1102 一樣。**接受**。
  8. **s21：錢員外笑得太開心**（新）。1.0–1.5、3.0、4.75–6.0 秒咧嘴露齒笑（`mouth-s21.jpg`），超過稿子的「嘴角抽動、幾乎不露牙」；1102 一樣（`alt-s21-1102.jpg`）。有冒汗、擦額頭，乾笑還讀得出。**接受**。
  9. **s08：院門邊一支長槍**（已知）。2.375–5.25 秒在畫右 x 880–955、y 150–330，5.5 秒推出畫。用局部模糊（vf 在文末，`try-s08.jpg`）。火把九、十支（稿子不超過八支），接受。
- **建議重拍**：
  - **s22**（嚴重 1）：必拍；fix1 的主要目標（帽子）沒有達成，遮罩救不了。
  - 可選 **s01**（中等 6）：眼神改看胡縣令。
  - 其他都能用剪點、換種子、局部處理解決。
- **重拍六鏡的逐格確認**（協調者只看每 1.43 秒一格）：

  | 鏡 | 選中 | 確認結果 | 另一支 |
  | --- | --- | --- | --- |
  | s02 | 1201 | 不笑（唐小棠 3.0 秒起要哭）；阿令 3.0–6.5 秒直視鏡頭，唐小棠近乎看鏡頭；畫右火盆在燒 | **1202 較好**：側臉朝畫右、2.0 秒後沒有火盆；0–2.0 秒左上一支火把、0–0.5 秒右緣半個人，用 `start@2.0` 剪掉；畫右玉米辣椒串（實物，非故障） |
  | s04 | 1201 | 不是「1.4 秒後收住」：笑到 2.625 秒；背景整排紅纓長槍全程 | 1202 更糟：笑到 4.5 秒、也有槍架與三腳火盆 |
  | s22 | 1202 | 不咧嘴（6.0–6.5 秒閉嘴壞笑，准）；**帽子仍有兩條長垂帶**；畫左紅纓槍架、火盆；前景 6.5 秒起轉頭露臉 | 1201 帽子一樣有垂帶，5.7 秒起笑、背景也有槍 |
  | s24 | 1201 | 錢袋暗紅、算盤不變（對）；5.458 秒起許硯笑 | 1202 結尾唐小棠咬唇像笑、許硯 5.5 秒還張嘴 |
  | s26 | 1202 | **笑場**（1.5–2.5、3.25–4.25 秒露齒），眼睛直視鏡頭 | **1201 較好**：不笑、有帽翅 |
  | s33 | 1201 | 對：坐→彈起抓頭→轉背→轉回→手放下肩垮；全程閉嘴；5–10 秒正面但眼睛往下、不看鏡頭；背景曬衣竿上紅辣椒（實物） | 1202 開頭正面、7 秒後正對鏡頭較多 |

- **每場的結尾**：
  - 第一場（s13）讀得懂：秦霜擋在小禾前面，畫右緣伸進來的藍綠官袖胖手，秦霜冷冷說完。6.375 秒起嘴角一點笑意（輕微）。
  - 第二場（s27）讀得懂：阿令近景，先聽、再轉向畫右輕聲說；身後兩個三腳火盆（已知類型）。
  - 第三場（s35）讀得懂：許硯站在院子中間、畫左那支直立快熄的火把，5.0 秒起瞪眼僵住；6.0 秒收在眼神靠近鏡頭之前。天色發青，對。
- **接第 11 集**：第 11 集 s35 末格是許硯胸以上、右拳握三份紅紙包在畫面左下、正對鏡頭，胡縣令在他左肩後（畫右）湊近；本集 s01 第一格是同一刻、同一軸線、同一服裝道具，景別從胸以上變成腰以上（`join-e911s35-s01.jpg`）。同一角度換景別稍有跳的感覺，但人物位置、紅紙包、背景房子與火把都一致，接得上。

## 一、嚴重

1. **s22 帽子、槍架、前景轉頭**（重拍）
   - 稿子：前景右只有胡縣令的官帽後腦、後頸與左肩，頭始終不轉；兵器都不拍；身後只有暗處與畫外人手上的火光，沒有火盆。
   - fix1 已經寫了「a stiff black hat with two short flat wings … nothing hanging from it, no ribbons and no cloth tails」，結果兩個種子都還是軟腳幞頭的長帶。spec.json 的 s22 只送許硯的參考圖，模型自己畫帽子，再寫一次帽子大概也一樣；所以改成**前景只拍肩膀、頭在畫框上緣外**，帽子根本不入鏡。
   - **重拍 s22**（送 `xuyan-portrait-l1`、`set-xujia-yuan-ye-l1`，不送胡縣令；買 10 秒；新種子例如 9121301／9121302）：
     > In the night yard of the Xu farmhouse before the fourth watch, deep night, the sky black, lit only by the warm glow of one blank paper lantern and the orange flicker of torches held by people outside the frame: low-angle over-the-shoulder shot. In the right foreground, soft and dark and out of focus, only the back of one plump man's left shoulder and upper arm in a blue-green robe; his head is above the top edge of the frame the whole shot and never enters it, so no hat, no hat wings, no ribbons and no face of his are ever visible. On screen left Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe, rising from a crouch to his full height, framed from the waist up with clear space above his head, a small blank slip pinched between the first two fingers of his right hand at chest height and a palm-sized dark red silk drawstring pouch smeared with mud held low in his left hand, his face three-quarter to screen right toward the man in the foreground, never the lens; cool and pointed: brows drawn slightly down, eyes hard and narrowed, jaw set, he speaks low and level, between words his lips close into a firm flat line, no grin, no smile, teeth never showing. Behind him only the dark bamboo fence and the dark earth wall of the house, soft and out of focus; nothing leans against the fence or the wall; no racks, no poles, no spears, no tassels, no red tassels, no weapons of any kind; no brazier, no fire bowl, no torch on a stand, no flame anywhere inside the frame; nobody else stands behind him. Exactly one face in the frame.
     >
     > Motion: Xu Yan speaks a short Mandarin line, 「大人，錢府的銀票從您袖裡掉出來。這名冊，還查嗎？」, his lips, jaw and cheeks moving clearly with every syllable, eyes on the man in the foreground, never looking at the camera; he rises to his full height and takes one step toward the man, stopping an arm's length away, the slip raised a little; the shoulder in the foreground keeps still and the head above it never comes into the frame; the deep night, the flickering torchlight and the lantern glow stay unchanged.
   - 挑片時逐格看：帽子或臉有沒有掉進畫框、背景有沒有槍與火盆、6 秒後有沒有咧嘴。
   - 退路（不重拍）：1202 整支加 `crop=736:414:0:30`（放大 1.30 倍，`try-s22-crop736.jpg`），帽子、垂帶、轉過來的臉都裁掉；0–2 秒畫右緣還有一條暗色的頭部邊緣；4 秒後頭頂貼上緣、錢袋出下緣；左邊槍架與火盆照舊（接受）。

2. **s04 笑場與槍架**（改剪點＋局部處理）
   - 稿子：可以冷笑；先冷笑退一步、轉身甩袖、再說。身後只有暗土牆。
   - 畫面（1201，`mouth-s04-1201*.jpg`）：1.0–2.0 秒咧嘴露齒笑、2.25–2.625 秒張大嘴笑、2.75 秒張口（像喊「好」）、2.875 秒起側臉、說話、不笑；4.5–5.25 秒嘴角有一點笑意（冷笑，准）；8.5–9.25 秒往畫右指人。
   - 槍架位置（`f-s04-1201.jpg`）：2.75 秒 x 770–920、y 80–200；6.0 秒 x 780–940；10.0 秒 x 790–960。刃在 y 75–135（天空裡），紅纓在 y 140–200（土牆上）。胡縣令的帽翅最右到 x 690，指人的手在 y 280 以下，都碰不到框。
   - **修法**：`start@2.75`、放慢約 1.07 倍；局部處理 vf 在文末。

3. **s26 換 1201**（換種子＋局部處理）
   - 1201 的槍在 x 730–870、y 0–190（0–7 秒都在），旁邊辣椒串一起模糊也無妨。火盆在 x 640–700、y 260 以下，碰不到框。
   - 1201 6.5–7.3 秒快步往畫右出畫（相鄰格位移大是人出畫，不是畫面抖）。

## 二、中等

4. **s02 換 1202、`start@2.0`**：見結論。
   - 代價：秦霜「木棍往地上一頓」在 0.5–1.5 秒，剪掉後只剩握棍；唐小棠 4.0 秒後咬唇要哭、露一點上牙，讀成哭不是笑。
   - 畫右玉米與辣椒串掛在竹架上（`z-red-strings.jpg` 同類），是實物，不是第 11 集那種紅色珠串故障。
   - 不換的話：1201 整支用，阿令看鏡頭接受；火盆可用 `split[a][b];[b]crop=180:300:780:180,…` 壓暗，但它是亮的火，壓暗會變一團暗影，不建議。

5. **s24 `end-before@5.4167`**：見結論。另：3.5–5.4 秒許硯臉朝鏡頭偏右一點，眼睛靠近鏡頭（輕微）；把錢袋往左遞給唐小棠（3.5–4.5 秒）不是「頭不回、手往後」，讀得懂，接受。0–1.0 秒畫右緣有半個拿火把的暗影，接受。

6. **s01 直視鏡頭**（可選重拍）
   - 重拍提示詞（送 `xuyan-portrait-l1`、`huxianling-portrait-l1`、`set-xujia-yuan-ye-l1`；第一格要接第 11 集 s35，所以先低眼、再轉頭）：
     > Medium two-shot on the night yard of the Xu farmhouse, deep night, the sky black, slow push in; the shot opens on the same moment as the shot before: Xu Yan, in an old plain grey cloth outer coat over his faded blue-grey scholar's robe, framed from the chest up, his own right fist raised in front of his chest at the lower left of the frame gripping three small folded packets of plain blank red paper, his body almost facing us but his eyes lowered to the red packets in his fist, never the lens; Magistrate Hu, in a black futou hat with two stiff flat wings and a blue-green robe, half a step behind Xu Yan's left shoulder on screen right, bending his head to Xu Yan's left ear, his face in profile toward screen left. First Xu Yan slowly straightens up and lowers his fist; then he turns his head to screen right and looks Magistrate Hu straight in the eyes, his face in three-quarter profile toward screen right from that moment to the last frame; only then he speaks, low and firm, brows level, eyes hard, no smile. Magistrate Hu straightens, his face hardening, lips pressed together, no smile. Behind them only darkness and the orange flicker of torches held by people outside the frame; nobody in the background carries a sword, a scabbard or a spear; no brazier, no torch on a stand.
   - 不重拍的話整支照 `picks.json` 用（4.46 秒起前額掉下幾縷頭髮，後面 s07、s17、s19 他本來就有這幾縷，接得上）。

7. **s05 唐小棠看鏡頭**：接受。

8. **s21 錢員外露齒笑**：接受（兩支都一樣，再拍多半也一樣）。

9. **s08 院門長槍**：vf 在文末。

## 三、兵器、紙、道具（逐鏡）

| 鏡 | 人或位置 | 看到的 | 處理 |
| --- | --- | --- | --- |
| s01 | 畫右背景黑衣人 | 腰間帶鞘的刀（0–4.6 秒，x 820–945、y 345–425） | 可選局部模糊（`try-s01.jpg`）；不做就接受 |
| s02 1201 | 畫右 | 三腳火盆在燒 | 換 1202（中等 4） |
| s03 | 阿令左手 | 拳下那條淺色直條是裙褶，不是刃（`z-s03-hand.jpg`）；手指慢慢鬆開 | 對 |
| s04 | 背景畫右 | 整排六支紅纓長槍 | 局部模糊（嚴重 2） |
| s08 | 院門右側 | 一支長槍斜靠 | 局部模糊，2.375–5.25 秒 |
| s13 | 秦霜 | 右手木棍；3.0 秒後木棍不見（插地那一下沒拍清） | 接受 |
| s16、s20 | 二牛、村民 | 木棍 | 對 |
| s22 | 背景 | 畫左紅纓槍架、單支長槍、三腳火盆 | 重拍（嚴重 1） |
| s23 | 背景 | 一個穿褐色袍的人舉火把（別鏡衙役是黑衣） | 接受 |
| s25 | 趙捕頭、黑衣人 | 2.5–3.25 秒趙捕頭右手拿一根沒點的短棍（像沒點的火把），沒看到刀；衙役只拿火把 | 接受 |
| s26 | 畫右上 | 紅纓長槍兩支、辣椒串、玉米串 | 換 1201 後局部模糊 |
| s30、s33、s34 | 背景 | 斜靠牆的是竹竿，沒有刃（`f-s30-34.jpg`） | 對 |

- 紙：s01、s07、s17、s29 的婚書是三個空白紅紙包，沒有字；s14、s15 銀票空白米黃紙、不透光，對；s18、s19、s22 字條空白，對。
- 錢袋：s09 掉下的錢袋偏洋紅，s10、s11、s22、s24 是暗紅（調色時把 s09 的飽和度降一點即可，輕微）；s17 唐小棠手上的錢袋摺得扁平，像一張紅紙（輕微）；s17 剪在 4.834 秒，遞錢袋給許硯那一下（5.0 秒起）沒有進片（已知，s18、s19 讀得通）。
- 草兔：s06 小禾 0–1.5 秒抱著草兔，剪點 1.583 秒之後兔子不見；s05、s10、s11 兔子塞在腰間。接受（輕微）。
- 算盤：s02、s05、s14、s17、s24 都是素木算盤，沒有雕花。
- s34：火把從第一格就是直立的，許硯「扶正」只是扶著（輕微）。

## 四、人、字、紅串、故障、嘴

- **分身、多出來的人**：選中的 35 支都沒有分身。s02 1202 0–0.5 秒右緣半個人（`start@2.0` 剪掉）；s24 0–1.0 秒右緣半個拿火把的暗影；s27 4.5 秒起她右肩後背景一個模糊人影（輕微）。s16 籬笆後的村民比稿子的八人多（約十二人，接受）。
- **字**：s22 屋牆上的小方框放大看是格柵小窗，不是字（`z-s22-plaques.jpg`）；燈籠都空白；沒有看到招牌或紙上的字。
- **紅珠串**：沒有故障式的紅色珠串。看到的紅串都是掛在竹架、晾衣竿或牆上的辣椒串，旁邊常有玉米串（s02 兩支、s04、s22、s24、s26、s32 右上、s33 晾衣竿，`z-red-strings.jpg`、`z-s33-redline.jpg`）。農家實物，接受。
- **故障特效、閃粒**：沒有。
- **火盆、三腳火把架**：s02 1201、s03、s05、s10、s12、s13、s15、s17、s18、s19、s21、s22、s26、s27 背景都有（規格寫不要，已知類型），都在背景。只有 s02 1201 換掉；其他接受。
- **畫外句時的嘴**：
  - s02 1202：三人整段閉嘴（唐小棠咬唇），對。
  - s06 小禾閉嘴，對；s10 小禾閉嘴，對；s14 小禾、秦霜閉嘴，對；s29 許硯、阿令閉嘴，對。
  - s30–s35 許硯閉嘴，對（s31 閉嘴笑，准）。
- **唐小棠背影不轉頭**：s06、s14、s29 從頭到尾只有後腦、丸子頭、粉緞帶與衣肩，頭不轉，對。s07 前景她 3.0 秒起露出臉頰與耳朵側面（輕微，同第 11 集）。
- **笑場**：s04（嚴重 2，剪點）、s26（嚴重 3，換 1201）、s24（中等 5，剪點）、s21（中等 8，接受）、s13 6.375 秒起嘴角一點笑意（輕微；錄音要到 6.815 秒，不能再收）、s19 0–1.0 與 6.0 秒後笑（已剪掉）、s07 5.0–6.0 秒閉嘴壞笑（已知，稿子寫不笑，輕微）。
- **看鏡頭**：s01（中等 6）、s05（中等 7）、s02 1201（換 1202）、s26（兩支都有，1201 後段看下面）、s24 3.5–5.4 秒（輕微）、s35 5.75 秒起（已剪掉）。
- **逐格跳動**：沒有發現。相位相關分數高的 s01、s10、s23、s25、s33 是人移動或搖鏡造成，背景時間切片是平滑曲線（`slit-rows-a.jpg`、`slit-rows-b.jpg`、`slit-s01-row.jpg`）。

## 五、各場檢查結果

- **第一場（s01–s13，院子夜）**：
  - 天全黑、火把與燈籠，沒有像白天的光。
  - 軸線：院門在右、屋門在左後。s08 胡縣令往畫右院門走、s09 官靴往畫右出畫、s10 小禾由左往右跑、s11 小禾朝畫右的胡縣令舉錢袋、s12 胡縣令朝畫左撲手、s13 胖手從畫右緣伸進來，方向都一致。
  - s01 → s02：三位妻子在 s02 1202 朝畫右看院子中間的許硯，接得上；1201 看鏡頭（換掉）。
  - s04：fix1 拿掉了身後的黑衣人，但背景換成院牆加槍架（嚴重 2）。
  - 人數與火把：s08 九、十支火把（已知）。
- **第二場（s14–s27，院子夜）**：
  - s14 → s15：s14 銀票舉到頭頂、s15 插鏡在胸前，插鏡接受。
  - s20：院門在中間、二牛左、錢員外右，二牛不笑，對；錢員外和胡縣令不同框，對。
  - s22 → s23：前景帽子（垂帶）與 s23 胡縣令的平翅帽接不上（嚴重 1）。
  - s25：胡縣令 0–2.0 秒往畫右出畫、趙捕頭回身喊、阿令留在畫左石桌旁，前景石桌角插著那支火把，對；火把約六支。
  - s26（換 1201）在院門下回頭、說完往畫右出畫，接 s25 方向一致。
- **第三場（s28–s35，院子天快亮）**：
  - 天色發青，只剩那支火把，對；s28 一長串火把沿村路走遠，對。
  - s29：許硯正對唐小棠遞紅紙包、阿令在他右後，對；秦霜與小禾不在畫面裡，對。
  - s30 → s31 → s32：s30 坐在石桌邊，s31、s32 反打背景是籬笆與田，構圖兩鏡相同（1102），接得上。
  - s33 → s34 → s35：s33 背後的火把在畫左，s34 蹲到畫左的火把旁，s35 火把在他畫左，方向一致。

## 六、每鏡處理總表

| 鏡 | 種子 | 等級 | 做法 |
| --- | --- | --- | --- |
| s01 | 9121101 | 中等 | 照 picks.json；直視鏡頭接受或可選重拍（中等 6）；可選刀鞘模糊 |
| s02 | **9121202** | 中等 | 換種子，`start@2.0` |
| s03 | 9121101 | — | 剪點寫成整格 `start@2.7917 end-before@5.8333` |
| s04 | 9121201 | 嚴重 | `start@2.75`，放慢約 1.07 倍；槍架局部模糊 |
| s05 | 9121101 | 中等 | 照 picks.json；唐小棠看鏡頭接受 |
| s06 | 9121101 | 輕微 | 整格 `start@1.5833 end-before@7.4167`；草兔消失接受 |
| s07 | 9121101 | 輕微 | 照 picks.json |
| s08 | 9121101 | 中等 | 照 picks.json；院門長槍局部模糊 |
| s09 | 9121101 | 輕微 | 整格 `start@0.875 end-before@4.2083`；錢袋顏色調色時往暗紅拉 |
| s10 | 9121101 | — | 照 picks.json |
| s11 | 9121101 | — | 整格 `start@2.5833 end-before@7.9167` |
| s12 | 9121102 | — | 照 picks.json |
| s13 | 9121102 | 輕微 | 照 picks.json（6.375 秒起一點笑意，接受） |
| s14 | 9121101 | — | 整格 `end-before@5.9167` |
| s15 | 9121101 | — | 整格 `end-before@4.2083` |
| s16 | 9121101 | — | 照 picks.json |
| s17 | 9121102 | 輕微 | 整格 `start@0.2917 end-before@4.8333` |
| s18 | 9121101 | — | 照 picks.json |
| s19 | 9121101 | — | 整格 `end-before@5.8333` |
| s20 | 9121101 | — | 照 picks.json |
| s21 | 9121101 | 中等 | 照 picks.json；露齒笑接受 |
| s22 | 9121202 | 嚴重 | **重拍**；退路 `crop=736:414:0:30` |
| s23 | 9121101 | — | 整格 `start@1.1667 end-before@6.4167` |
| s24 | 9121201 | 中等 | `end-before@5.4167` |
| s25 | 9121101 | — | 整格 `end-before@4.8333` |
| s26 | **9121201** | 嚴重 | 換種子，整支；槍局部模糊 |
| s27 | 9121101 | — | 照 picks.json |
| s28 | 9121102 | — | 照 picks.json |
| s29 | 9121101 | — | 照 picks.json |
| s30 | 9121102 | — | 整格 `start@0.2917` |
| s31 | 9121102 | — | 整格 `end-before@3.4167` |
| s32 | 9121102 | — | 整格 `end-before@4.4167` |
| s33 | 9121201 | — | 照 picks.json（fix1 確認可用） |
| s34 | 9121102 | 輕微 | 照 picks.json |
| s35 | 9121102 | — | 整格 `start@2.5833` |
| 水平翻轉 | — | — | 沒有建議。每一鏡都有交領的人 |

剪點長度都核過錄音（每句最後一個字的結束秒數）：除了 s04 改剪點後要放慢 1.07 倍，其他鏡的長度都大於整句錄音。

## 給 refine-prep.py 的 review2-trims.tsv（建議）

只列要改的；其餘照 `picks.json`。整格那幾列只是把三位小數寫成 1/24 秒的整數倍（floor／ceil 後不會多吃一格），數值本身沒變。s22 若決定走退路而不重拍，把那一列換成 `s22	9121202	crop=736:414:0:30 pick-review：…`。

```
shot	choice	reason
s02	9121202	start@2.0 pick-review：1201 阿令與唐小棠看鏡頭、畫右火盆在燒；1202 側臉朝畫右，2.0 秒後沒有火盆與右緣半個人；剩 4.583 秒，錄音 4.01 秒
s03	9121101	start@2.7917 end-before@5.8333 pick-review：剪點寫成整格（67–140）
s04	9121201	start@2.75 pick-review：1.0–2.625 秒咧嘴大笑，2.875 秒起才側臉說話；剩 7.375 秒，錄音最後一字 7.85 秒，剪接時本鏡放慢約 1.07 倍
s06	9121101	start@1.5833 end-before@7.4167 pick-review：剪點寫成整格（38–178）
s09	9121101	start@0.875 end-before@4.2083 pick-review：剪點寫成整格（21–101）
s11	9121101	start@2.5833 end-before@7.9167 pick-review：剪點寫成整格（62–190）
s14	9121101	start@2.0 end-before@5.9167 pick-review：剪點寫成整格（48–142）
s15	9121101	start@1.0 end-before@4.2083 pick-review：剪點寫成整格（24–101）
s17	9121102	start@0.2917 end-before@4.8333 pick-review：剪點寫成整格（7–116）
s19	9121101	start@1.125 end-before@5.8333 pick-review：剪點寫成整格（27–140）
s22	RETAKE	pick-review：fix1 兩支前景帽子仍垂兩條長帶（跟 s23 平翅官帽接不上）、畫左紅纓槍架與火盆、6.5 秒起前景轉頭露臉；改成前景只拍肩、頭在畫框外重拍
s23	9121101	start@1.1667 end-before@6.4167 pick-review：剪點寫成整格（28–154）
s24	9121201	end-before@5.4167 pick-review：5.458 秒起許硯閉嘴微笑；剩 5.417 秒，錄音 4.32 秒
s25	9121101	start@0.75 end-before@4.8333 pick-review：剪點寫成整格（18–116）
s26	9121201	pick-review：1202 在 1.5–2.5、3.25–4.25 秒露齒笑；1201 皺眉齜牙不笑，帽子兩邊有展翅（fix1 說沒有，不對）；整支用，錄音 4.96 秒
s30	9121102	start@0.2917 end-before@7.0 pick-review：剪點寫成整格（7–168）
s31	9121102	start@0.5 end-before@3.4167 pick-review：剪點寫成整格（12–82）
s32	9121102	start@0.5 end-before@4.4167 pick-review：剪點寫成整格（12–106）
s35	9121102	start@2.5833 end-before@6.0 pick-review：剪點寫成整格（62–144）
```

剪接時另外套（不放進 TSV；座標是 960×544 草稿，時間是草稿原片秒數。若先剪再套，`enable` 的秒數要減掉 `start`；精修放大後再套，座標乘上倍數，建議精修後在剪接時套）：
- s04（9121201，`try-s04.jpg`；框在天空那一段略灰，精修後若明顯，把 `saturation` 提到 0.4）：
  `split[a][b];[b]crop=205:150:755:55,eq=brightness=-0.06:saturation=0.15,boxblur=7,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(X\,min(Y\,H-Y))/25)'[c];[a][c]overlay=755:55`
- s26（9121201，`try-s26.jpg`）：
  `split[a][b];[b]crop=170:210:720:0,eq=brightness=-0.06:saturation=0.15,boxblur=7,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(min(X\,W-X)\,H-Y)/25)'[c];[a][c]overlay=720:0`
- s08（9121101，`try-s08.jpg`；草稿時間 5.25 秒前，剪後是 `lt(t,2.875)`）：
  `split[a][b];[b]crop=95:200:865:140,eq=brightness=-0.06:saturation=0.15,boxblur=6,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(X\,min(Y\,H-Y))/20)'[c];[a][c]overlay=865:140:enable='lt(t,5.25)'`
- s01（9121101，可選，`try-s01.jpg`）：
  `split[a][b];[b]crop=145:100:815:340,eq=brightness=-0.06:saturation=0.15,boxblur=6,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1\,min(X\,min(Y\,H-Y))/20)'[c];[a][c]overlay=815:340`
- 碰到畫框邊的那一側不做羽化（alpha 式子少掉那一項），所以邊緣的槍尖也蓋得到。
- s22：重拍後用新片取代，剪點另定；走退路就在 TSV 用 `crop=736:414:0:30`。
