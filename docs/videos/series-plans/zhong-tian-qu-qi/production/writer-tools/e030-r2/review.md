# 第 30 集重製版 r2（e030-r2，內部 930）獨立審稿：真人版分鏡與 d1 提示詞

- 審稿：沒參與寫稿的獨立代理，2026-11-17，開拍前最後一關。只寫這一個檔；沒改別的檔、沒用 Colab／RunPod／付費服務、沒 commit；沒碰 e928、e929 的檔（只讀）。
- 審的對象：`docs/videos/zhong-tian-qu-qi-e030-r2/{script.md,storyboard.md,video.json,overlays.json}`、`writer-tools/e030-r2/r2.py`、`colab/runs/e930/extras.json`、`colab/runs/e930-live/{mkspec.py,spec.json}`、`hailuo/clips-dh-e930.json`（精修文字），以及實際要送的 `~/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/runpod/live/d1/colab-jobs.json`（84 支＝42 鏡 × 2 種子）與 `prompts/`；錄音 `audio/`（`README-retakes.txt`、`fw930*.txt`、`f0y930*.txt`、`span930*.txt`、wav）。
- 對照：`r2-bible-e021-e030.md`（拍法 1–30、接點 29→30／30→31、小角色、道具表、好感帳）、`r2-bible-e011-e060.md`（第 31 集時間線、30→31 補定、第 38／51／53 集的馬）、`season-01.md` 第 30 集、`writer-tools/e029-r2/review.md`、`colab/runs/e926-live`～`e929-live` 的挑片檔、任務檔最後幾則（e923 霧圖長室內、e925 畫外女子半張臉、e926 群眾分身、e928 精修句漏進 d1）、第 29 集 s32–s35、第 31 集 r2 稿 c01–c04、`assets/refs-live/README.md` 第 30 集段。
- 參考圖：七張新圖、母圖 `set-xujia-yuan-dong-l1`、唐萬金／鄭伯／阿令（面巾、沒面巾、angle-a）縮成小 jpg 放大看過，屋頂、塗改處、院門外各再放大一次；用完已刪。
- 錄音：a28-p79、a13、a32、a23、a23-p126、a17、a29、a31、a12、a09 用 YIN 重量一次（40 ms 窗、10 ms 步、門檻 0.15，numpy 陣列，一次一支），跟 `f0y930.txt` 一致（a28-p79 257、a23 83、a23-p126 117、a17 233、a29 206、a31 243 Hz）。a23 用 faster-whisper medium（numpy、cpu_threads=2、一次一支、跑完結束）取字的時間：「哈哈」0.00–0.80、停頓到 1.28，「鄉」1.28 起、「真」收在 5.58。

## 機械檢查（都通過的）

| 項目 | 結果 |
| --- | --- |
| 分隔句 | 84 支 d1 每支 `never the mood. ` 與 `One continuous shot.` 剛好一次；`prompt_sha256` 全部跟檔案相符；兩個種子的提示詞逐位元相同。clips-dh 42 鏡每鏡 `the set layout stays as it is. ` 剛好一次 |
| d1 漏進精修句 | **沒有**。沒有任何 `... shown in <Picture 1> keep(s) the same ...`；s17、s22、s32 三支插鏡裡的 `Throughout the shot the set layout stays as it is. The pictures fix the place and the objects only, never the mood.` 是插鏡標準句（e926–e929 都有），不是漏句 |
| 參考圖路徑 | 84 支全部絕對路徑、檔案都在；`set-guangchang-l1`、`set-xujia-yuan-l3`、`set-xujia-yuan-dong-l1` 母圖一支都沒送（`retake.json` 裡的舊名已被 swap 換掉）；唐小棠的圖八個背影鏡與 s41 都沒送；`xuyan-angle-b-l1` 整集沒送；s09 只送面巾圖、s38／s39 送沒面巾的定妝照＋angle-a、s41 只送定妝照 |
| open／否定名詞／會長字的名詞 | 提示詞沒有 `open`、`lantern`、`plaque`、`sign`、`banner`、`brush`、`table`、`bench`、`saddle`、`crowd`、`Tang Xiaotang`；否定只剩各集共用的 `no subtitles`、`no second copy`、`no talking, no mouthing words`、`never the lens`、`not smiling` |
| 畫外的人 | 對畫外說話全寫 `someone out of sight beyond the left/right edge`，並寫那一側到邊緣只有景、畫面裡只有他一個人（s34 低頭別臉、s39 看院門除外，見建議）；看的地方寫成大車、碗、院門、井；不點名、不描述不在畫裡的人 |
| 掛著的東西 | 沒有匾、燈籠、旗、吊牌；母圖的空白木板、門楣紅點、兩片吊牌葉都已塗掉（放大看過：石牆接得上、門楣素淨、樹全禿） |
| 人數 | 每鏡都寫 exactly N people／only these N；本集沒有群眾 |
| 一鏡一動作 | 42 鏡都只有一個主動作；前置動作都放在第一格已完成 |
| 唐小棠 | 九個鏡（s02、s08、s13、s14、s20、s28、s29、s33、s41）都是正背對、頭不動、剛好兩顆丸子、`every strand ... combed smooth`（防垂辮）；s41 小小的背影在許硯右邊 |
| 魏少卿 | 扇子每鏡合著（`its dark bamboo ribs pressed tight together like a short slim stick`）；s26、s30、s34、s37、s40 `not smiling`；s05、s10、s15、s23 照稿子可以笑 |
| 唐萬金 | s01–s06 哭相不笑、s25–s29 不笑、s35 笑；腰間金鑰匙每鏡照寫 |
| 面板 | `overlays.json` 只有 s20（「唐小棠 好感 +6 → 42」「突破四十」）與 s21（開箱獎勵），跟聖經好感帳第 30 集列相同；s20、s21 沒寫藍光 |
| 接點 29→30 | s01 唐萬金張著手停在一步外、朝畫左（第 29 集 s34 他往畫左奔）；s02 跟第 29 集 s35 同構圖（她右手抓許硯左袖、帳本夾左臂、許硯在右三分之一朝畫右）。通過 |
| 軸線 | 廣場：唐萬金看許硯與女兒朝畫左、看大車與魏少卿朝畫右；許硯朝畫右；魏少卿朝畫左。院子：唐萬金看女兒朝畫左（s18）、看魏少卿朝畫右（s25、s27）；魏少卿朝畫左（s15、s23、s26、s30）；許硯在屋前朝畫右；井邊阿令朝畫左看院門、院門口魏少卿朝畫右看井（s39↔s40）。院子各鏡都朝後牆拍，背景是 `-qiang` 的牆與田，地理說得通。通過 |
| 光源 | 母圖太陽在右上、牆後，影子往左下朝鏡頭；院子各鏡寫 `from the upper right behind`（院門、屋前、井、全景）或 `from the right`（泥牆近景），s30 寫太陽在禿枝後的右邊，都跟圖一致 |
| 錄音長度 | 每鏡都放得下。6 秒的鏡實際出片約 6.58 秒（e929 挑片的 `end-before@6.584`）：最緊的 s05（a05 人聲到 5.70）、s35（a34 到 5.62）、s37（a36 到 5.66）、s34（a33 到 5.42）都還有 0.9 秒以上；s23 見下 |

## 寫稿者沒把握的地方：逐一判斷

| 問題 | 判斷 | 見 |
| --- | --- | --- |
| 院子圖：牆外金田 | **本集接受**（聖經已接受、提示詞照圖寫 golden field）。但第 31 集「三個月後」早春旱田**不能再用這張**（見接點） | 建議 14 |
| 院子圖：太陽入畫 | **接受**。只在全景 s31、s37、s41 與 s30 的 `-shu` 入畫，提示詞都寫右上、背光，跟圖一致；近景裁切都沒有太陽 | — |
| 院子圖：屋頂橘點 | **建議免費塗掉**。`-men-l1` 左上放大 2.6 倍後是十來顆清楚的橘色圓球（像柿子擺在草頂上），院門口六鏡（s07、s08、s10、s35、s36、s40）人頭就在它旁邊；`-wu-l1` 上緣也有。不是字，風險中低，但塗掉零成本 | 建議 1 |
| 院子圖：兩只桶 | **接受**。院子中間那只空桶只在 `-qing` 全景；`-jing` 已裁掉。s41 阿令手上一桶、地上一桶，畫面合理；提示詞不寫第二只桶是對的 | — |
| 院子圖：塗掉處會不會長回方板 | **不會**。三處放大看過：屋門右邊是接得上的石牆（比對過亮度，沒有方框輪廓）、門楣素淨、樹上只剩一小段抹平的細枝。`-wu-l1` 看得到那面牆，也乾淨 | — |
| `-qiang-l1` 用 15 鏡、偏軟、單調 | **接受，不必重裁**。院子的戲都是對著後牆右段站（唐萬金在中、魏少卿在右牆邊、唐小棠背對鏡頭面向他們），15 鏡同一片牆與田是正確的地理，接戲也穩；放大 4.6 倍偏軟反而像虛焦背景。真想分開唐萬金與魏少卿的單人鏡，見建議 15（免費） | 建議 15 |
| s41 提示詞長 | 從 `Initial composition` 起 3,938 字，全文 5,683 字，是系列最長的一支（e929 最長全文 4,906，有跑出可用的片）。產線沒有 4,000 字的硬上限（`preflight-prompts.py` 不查長度）。**長度可接受，但有一處句子黏錯必改**，順便可刪約 250 字的院子格局 | 必改 5 |
| s37 井邊不點名的女子背影 | **要改寫**。「長成第二個阿令」風險低（沒送阿令的圖）；「露臉」風險高：她在右前景畫緣、又寫了 `the thin ties of a pale grey gauze veil behind her ears`（耳朵與面巾都在臉的周圍），正是 e924 s35、e926 s23「畫緣她的臉頰」那一型 | 必改 4 |
| s38 送沒面巾的圖，面巾直接不見 | **會，要補**。s38、s39、s41 只寫 `the veil hangs from her left ear only`——人物句與兩張圖都沒有面巾，模型不知道「the veil」是什麼東西，最可能整條不畫。要把面巾的材質顏色寫成實物 | 必改 1 |
| s24 鄭伯擋嘴耳語 | **可以拍**（鄭伯定妝照確實高瘦長臉，不跟圓臉的唐萬金撞臉）。補兩件事：鄭伯在畫面哪一側、手是「擋在嘴與唐萬金耳朵之間」而不是舉在嘴邊（後者容易演成喊話或吃東西） | 建議 3 |
| s36 馬沒有參考圖 | **本集照文字寫一匹就好**（只見頭頸、秦霜右手牽、在她畫右，寫法對）。第 31 集（魏少卿的白馬，CG 稿 c04 上馬）、第 38、51、53 集（棗紅馬要人騎）需要全身，建議在第 4 篇章試鏡加馬；本集挑片後先免費截一格當顏色與轡頭的參照 | 建議 13 |
| s05、s23 6 秒剛好裝錄音 | **不必改買 8 秒**。6 秒的片實際約 6.58 秒；s05 a05 人聲 0.25–5.70；s23 a23 的「哈哈」在 0.00–0.80、台詞 1.28–5.58，畫面上說的是片中原聲（提示詞沒有哈哈），錄音只是備援，要用就從 1.20 秒切 | 建議 11 |
| s20 背影只有肩膀一提 | **能用但偏弱**（第 25 集同一做法、面板撐劇情）。從背後看得出的害羞是手：改成腰以上、兩手在背後絞一下 | 建議 2 |
| 錄音 a28 用降調檔 | **接受**。p79 是 257 Hz，同場 a13 253、a32 238，對得上；formant 保留、帶上下文聽寫 r1.00；她背影、放的就是錄音。仍要人耳聽一次「抵押……」的氣音有沒有被拉怪 | 建議 11 |
| 唐萬金 a17／a29／a31 留原錄高音 | 三鏡他都在畫面上說（s18 近景、s29 中景、s31 全景），**片中原聲優先，錄音是備援**。要用錄音時：a29（傻囡囡，放軟的一句）206 Hz 比同樣放軟的 a12（131 Hz）高約 8 個半音，改用 `-p84`；a17（驚訝的問句）用 `-p75`；a31 是吼，243 Hz 可留原錄 | 建議 11 |
| a23 魏少卿 82 Hz 帶笑聲 | 82 Hz 低於他第 27–29 集的 93–163 Hz，而且只有 55 個有聲格（多是氣聲與嘎音），**不要當主聲**。s23 用片中原聲；要備援就用 `-p126`（117 Hz，在他的範圍內），從 1.20 秒切掉不在字幕上的「哈哈」 | 建議 11 |

## 必改

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 30 | s38、s39、s41 | 面巾只寫 `the veil hangs from her left ear only, blown out to her left side, her whole face bare`。送的是沒面巾的 `aling-portrait-l1`（s38、s39 再加 angle-a，也沒面巾），人物句也沒有面巾；「the veil」沒有任何實物描述，模型最可能整條不畫，第 31 集 c01「從左耳拉回來」就接不上 | 拍法 19（參考圖壓過文字）、21；寫稿者的疑慮；面巾定妝照是一條長到胸口、半透明的灰紗 | 三鏡的構圖段把那句換成：`a long strip of soft, half-transparent pale grey gauze hangs from a thin grey tie looped over her left ear only, its free end blown out past her left cheek and shoulder in the wind, her nose, mouth and chin bare from the first frame`；動作段 s38、s41 的 `the loose veil` 換成 `the loose strip of pale grey gauze`。她朝畫左時左耳在靠鏡頭這一側，掛著的紗看得到，不必改方向 |
| 30 | s38 | `medium close-up ... framed from the chest up`，但這一鏡唯一的動作是右手把井沿上的桶提起來；井沿在她腰的高度，胸以上的框裡看不到手、桶與井沿，模型只能把桶抬高或自己改構圖 | 道具與接觸寫在第一格、一鏡一動作要看得見（第 29 集審稿）；`-jing-l1` 井沿高度 | 構圖改成：`medium shot of A-ling, framed from the waist up, the round stone rim of the well along the bottom of the frame, her right hand already gripping the rope handle of one round wooden bucket of well water standing on the rim from the first frame`；`cam` 改 `Medium shot, slow push in`。s09 同樣的井沿與桶，見建議 7 |
| 30 | s17、s22、s32 | 三支只送 `-di-l1`（一片土）的插鏡，構圖段一開頭寫 `In the courtyard of the Xu farmhouse at the end of the same cold clear early-winter day, the sun low in the west`，s17、s22 又寫 `from a low side angle`。第 29 集同樣寫法：只送道具圖的 s10、s11 長出「有積雪的熱鬧市集」（s11 整鏡重拍），只送土的 s15、s21 另一個種子長出殿宇、石燈籠、紅旗；低角度正好把背景抬進畫面。這裡會長出另一座農舍、一條村路或太陽 | 拍法 10（插鏡第一格就是主體）；e929 挑片 s10、s11（RETAKE）、s15、s21；任務檔 e923 | 三支的地點句整句刪掉，構圖段直接從光與主體開始，改從上方拍。s17：`Warm golden low evening light from the right: insert close-up seen from slightly above, looking down, the very first frame is already a close view of the edge of one thick stack of plain blank paper sheets stitched along one edge with cord, held level in two plump hands in deep purple silk sleeve cuffs woven with small gold ingot shapes, one plain gold ring on the right hand; far below, soft and out of focus, only packed yellow earth with long evening shadows fills the background to every edge`。s22 同法：`... seen from slightly above, looking down, the very first frame is already a close view of a man's right hand in a faded blue-grey sleeve cuff, palm up ...; far below, soft and out of focus, only packed yellow earth fills the background to every edge`。s32：`... insert close-up seen from above, looking down, the very first frame is already ... two torn halves ... tumbling down a hand's width above packed yellow earth; the earth fills the frame to every edge` |
| 30 | s37 | 右前景井邊的女子寫 `the grey-white cotton shoulder and the high black bun with one plain wooden hairpin of one slim woman, the thin ties of a pale grey gauze veil behind her ears, unnamed`：人在畫緣、又點出耳朵與面巾細繩，模型會把她轉成側臉或露出臉頰與面巾（第 31 集要她這時還戴著、背對） | 任務檔 e925（畫緣長出半張臉）；e924 fix1 s35、e926 s23「畫緣她的臉頰」；拍法 2、21 | 換成：`at the very right edge of the frame, cut by it, soft and out of focus beside the round stone well, only the back of one grey-white cotton shoulder and the back of a high black bun with one plain wooden hairpin, turned fully away from us toward the yard gate, the back of her head toward us the whole shot`（拿掉耳朵與面巾細繩）；魏少卿那句補 `the back of his head toward us`。`Besides him, only the one woman ...` 那句留著 |
| 30 | s41 | (1) 句子黏錯：`Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves down on the left and on his right one young woman ...`——「on the left」黏到袖子上，許硯在左、唐小棠在他右邊這個接點（30→31 補定「唐小棠在許硯右邊」）沒寫清楚。(2) 阿令 `her face three-quarter to screen left toward the yard gate`：她在前右、院門在後中，朝院門就是背向鏡頭偏左，「三分之四正臉」跟「朝院門」互相打架，模型會讓她轉向鏡頭 | 接點 30→31（兩份聖經）；第 31 集 r2 稿 c01 | (1) 改成：`in the middle of the yard, small, side by side with their backs to us, facing the yard gate: on the left Xu Yan, in his faded blue-grey scholar's robe patched at one elbow, its sleeves down, and on his right one young woman seen only from behind, appearing only once: ...`。(2) 改成：`her body turned toward the yard gate, her face in left profile, her eyes on the gate`，面巾照必改 1（左耳在鏡頭這側）。可順便把院子格局那串（屋、院門、樹、井）縮成 `the yard exactly as in the picture: the farmhouse on the left, the yard gate in the middle of the back wall, the well in the front right`，省約 250 字 |

## 建議

| 集 | 鏡 | 問題 | 依據 | 建議怎麼改 |
| --- | --- | --- | --- | --- |
| 30 | 參考圖 `-qing`、`-men`、`-wu` | 草頂上約十顆橘色小圓球（像擺著的柿子），在 `-men-l1` 放大 2.6 倍後非常顯眼，就在院門口六鏡人物的頭旁邊；院門外麥田裡也有幾點橘花 | 母圖歸檔時就記了「草頂上有幾顆橘點」；第 21–24 集掛飾、吊燈籠長出來的教訓 | **免費修圖**：照 `e930tools/clean_yard.py` 的做法再加一處 (d)，每顆圓點用旁邊同一排草頂的像素蓋過（遮罩高斯 1.5 px），出新 id `set-xujia-yuan-dong-qing2-l1`，再用同樣的 `crop` 命令重出 `-men`、`-wu`（新 id 加 2），spec 的 swap 跟著換。不想換 id 就在院門口六鏡的背景句寫成實物：`a few dried persimmons lying on the thatch` |
| 30 | s20 | 好感 +6 只靠肩膀一提；從背後看不太出「害羞」 | 好感帳第 30 集要演出來的反應；拍法 3 | 改中景腰以上：`framed from the waist up, both her hands clasped behind her back at her waist`；動作：`her clasped fingers twist together once behind her back and her shoulders lift a little, only her hands and shoulders moving` |
| 30 | s24 | 鄭伯 `close behind his right shoulder ... his right hand already raised beside his mouth`：沒寫在畫面哪一側；「手舉在嘴邊」常演成喊話或掩口咳嗽，也可能嘴從指縫露出來動 | 拍法 1、15；寫稿者的疑慮 | `at the left of the frame, close behind Tang Wanjin's right shoulder and bent down to his right ear, Steward Zheng ..., his right hand already cupped against the side of his own mouth from the first frame, the cupped hand between his mouth and Tang Wanjin's ear, his lips hidden behind it`；唐萬金的 `his face warm and pleased` 改 `his face mild and at ease`，免得一開始就是大笑、退不乾淨 |
| 30 | s25 | 唐萬金帳本在右手，動作卻是夾到左腋下（右手越過身體） | 手與道具位置寫在第一格 | `one thick stack ... held in his left hand at his side`；動作 `tucks the stack of paper up under his left arm` |
| 30 | s08 | 秦霜在左三分之一，唐小棠用右手往左越過身體去拉她的袖子（左臂抱帳本） | 同上 | 帳本換手：`one thick stack ... held against her chest in her right arm`，`her left arm already reaching out to the sleeve of the woman beside the gatepost`；動作 `Her left hand tugs once at ...` |
| 30 | s09 | 跟 s38 一樣胸以上的框看不到井沿上的桶；另外面巾寫 `falling to just below her jaw`，定妝照的面巾長到胸口 | 參考圖壓過文字；必改 2 | `framed from the waist up, the round stone rim of the well along the bottom of the frame`；面巾句改 `hanging down to the middle of her chest`（人物句與構圖段兩處） |
| 30 | s31 | 魏少卿 `both his hands empty and half raised`：扇子在 s30 還在右手、s34 又捏在拳裡，中間這鏡不見；井邊空著而 s37 阿令在井邊（全景看得到井） | 接戲 | `his left hand empty and half raised, the closed fan held down at his side in his right hand`；井邊空著可以接受（第三場是另一個時刻），不要加第四個人 |
| 30 | s06 | `at the right edge the black lacquered carriage body and the head and neck of one horse at the right edge, its door already swung back`：重複 at the right edge，`its door` 會讀成馬的 | 句子清楚 | `at the right edge the black lacquered carriage body with its door already swung back, and beyond it the head and neck of one horse` |
| 30 | s27 | `two stiff fingers together` 指向畫外：比單根手指好，但兩指併攏仍可能被畫成比「V」或兩根分開 | 任務檔第 16 集（單根手指被讀成不雅手勢，寫張開手掌） | `Tang Wanjin thrusts his open right hand, fingers together and palm down, toward the right edge of the frame as he speaks` |
| 30 | clips-dh（精修文字） | 20 鏡的說話句仍是通用的 `turned toward the person he/she is speaking to ... eyes on that person`，而這些鏡畫面裡沒有那個人；s12 他看的是碗、s34 看的是地 | e929 審稿同一條；任務檔「還沒解決 (2)」；e925 畫外女子半張臉 | 不擋開拍。挑片後精修若畫緣多出人，把該鏡精修句換成 d1 的方向句，例如 s12 `his eyes on the chipped rim of the bowl in his hands`、s34 `his eyes on the earth at his feet, his face turning away toward the right edge of the frame` |
| 30 | 錄音 | 見上表：a23 82 Hz 帶「哈哈」、a17／a29 偏高、a28 降調、還沒有人耳聽過 | `README-retakes.txt`；YIN 重量；a23 字的時間 | 剪接表 `_note` 寫明：s23 片中原聲優先，備援 `zq930a23-p126.wav` 從 1.20 秒起放；s29 備援用 `-p84`、s18 用 `-p75`、s31 留原錄；s28 用 `-p79`。精修前請人耳聽 a28-p79、a23-p126、a29-p84 三支 |
| 30 | s05、s23、s35 | 6 秒的鏡裝 5.6–5.9 秒的台詞，片中原聲若念得慢會被片尾切到（第 29 集 s07、s22 就貼著片尾） | e929 挑片 s07、s22 | 不改 BUY；挑片時耳聽句尾，切到就鋪錄音（s05 a05、s35 a34 都從 0.25 秒內起音，放得下） |
| 30→38 | s36（馬） | 本集照文字寫一匹，可以。第 31 集 r2 稿 c04 魏少卿在籬笆外解韁上**白馬**、第 38 集阿令騎棗紅馬、第 53 集兩人共騎，都要全身的馬 | 拍法 19（劇情靠的東西先有圖）；`r2-bible-e011-e060.md` 第 31、38、53 集 | (1) 免費：本集挑片後，從 s36 選定那支截一格最乾淨的馬頭頸，存成 `prop-zaohongma-head-l1` 當毛色與轡頭的參照。(2) 第 4 篇章試鏡加兩張全身側面、灰底：`prop-zaohongma-l1`（`one chestnut-red horse, full body side view, a plain brown leather bridle and a plain brown leather saddle, grey studio background`）與魏少卿的白馬（第 31 集）；照站主 2026-11-15 授權由製作端定，只有加購點數要先問 |
| 30→31 | s41、聖經 | 聖經的院門位置寫「後牆中偏右」（拍法 29）、「魏少卿在後右院門口」（接點 30→31），圖上院門在後牆中間（全寬約 46–52%），本集提示詞照圖寫「middle」 | 拍法 29（場景圖說了算） | 本集照圖不改；交給第 31 集時把接點寫成「院門在後牆中間；阿令在前右井邊朝畫左看院門；魏少卿在院門口朝畫右看井」（本集 s39↔s40 的方向）。第 31 集 c01–c06 同一刻可以照用 `-qing`／`-jing`／`-men`；當夜那場與「三個月後」早春（樹冒新芽、地乾裂、牆外不是金黃麥田）都要新圖，`-dong` 這張不能延用 |
| 30 | `-qiang-l1`（可選） | 15 鏡同一片牆與田，唐萬金與魏少卿的單人鏡背景完全一樣 | 寫稿者的疑慮 | 可以不改。想分開的話免費多裁一張給唐萬金（他站在院子中間，背後是院門右邊的樹幹與牆）：`ffmpeg -i set-xujia-yuan-dong-qing-l1.png -vf crop=320:180:700:230` 出 `set-xujia-yuan-dong-qiang-shu-l1`，放大看過右下那片靠牆木板的柄是否入框再定；魏少卿、唐小棠背影照用 `-qiang-l1` |

## 小結

- **必改 5 條**：(1) s38、s39、s41 面巾寫成實物；(2) s38 構圖放到腰以上、井沿入框；(3) s17、s22、s32 插鏡刪地點句、改從上方拍；(4) s37 右緣的女子只留肩背與髻；(5) s41 許硯與唐小棠的句子黏錯、阿令朝院門寫成左側臉。
- 參考圖：**不需要重裁或調色**；建議免費塗掉草頂的橘色圓球並重出 `-men`、`-wu`（新 id）。不需要試鏡；馬的參考圖留到第 4 篇章試鏡，本集挑片後先免費截一格。
- 改完照 `prep930.sh` 重建 d1，重跑分隔句、精修句外漏、否定名詞、open、掛著的東西掃描與 `preflight-prompts.py`；必改 3 改了三支插鏡的構圖段，提示詞雜湊會變，`colab-jobs.json` 要重算 `prompt_sha256`。
