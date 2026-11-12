# Till the Verdict Do Us Part：試鏡（2026-11-10）

站主 2026-11-10 點頭（報價約 8–10 CU，上限 12）。路線照《恁祖媽今年18》的試鏡：Colab G4，
Qwen-Image-Edit 畫定妝照與場景，H3 Ref2VA 三段式的前兩段（960×544 hero → σ0.5 補到 1312×736），不放大。

## 跑了什麼

| 輪 | 內容 | 選定 |
| --- | --- | --- |
| r1 定妝照 | Nora、Elias、Grant、Peg 各兩張（灰底胸像） | Nora **b**（a 的脖子多了紅點）、Elias **a**、Grant **a**（b 在笑）、Peg **a** |
| r1 場景 | 玻璃屋客廳、玻璃屋外觀、Remelt 工作室 | 三張都可用；工作室偏 CG、偏暗 |
| r2 換裝 | 在選定的基本款上只換衣服（`latent: image1`）：Nora 工作圍裙、Elias 爐邊、Peg 大衣 | 三張臉都守住 |
| st1 片段 | 4 支 6 秒 Ref2VA hero 960×544 | 見下 |
| st2 補細節 | 4 支 σ0.5、10 步、1312×736 | 見下 |

片段（正文在 `runs/st1-prompts/`）：

| 鏡 | 內容 | 結果 |
| --- | --- | --- |
| e001-sweet | Nora（懷孕）咬藥、說 "My pill tastes sweet today." | 臉、懷孕的身形、咬藥、皺眉、拿著半顆藥都對；嘴在說話 |
| e001-grant | Grant 講電話 "They changed the coating, babe."，放下電話笑容收掉 | 臉對、嘴在說話；窗外是藍天，不是設定的陰天；笑容收得不夠明顯 |
| e008-peg | Peg 拖行李停下、回頭 "I'm going with her."、轉身走 | 臉、大衣、行李、帳本都對；回頭與轉身照寫 |
| e060-scar | Elias 摘手套露疤 "Hello, Sales." | 第一版疤畫成紅色縫線的傷口（像受傷，廣告有風險），改寫後重跑一支：疤變成銀白的一塊，但 σ0.5 補細節後周圍又帶紅；手太大、擋住半個畫面 |

## 學到的

1. **英文嘴型**：三支說話鏡的嘴都在動、節奏像在說話。是否對得上實際配音，要等配音後對嘴才知道；這次只證明「會說話」，沒證明「對得上」。
2. **細小的傷痕會被畫成紅色**：Nora 的「手腕內側細小燙痕」在定妝照與片段裡變成脖子、手腕、臉上的紅點；Elias 的疤第一版是紅色縫線。建議：Nora 的外貌拿掉燙痕（只在插鏡裡講）；Elias 的疤改用獨立的手部插鏡、手放小，正文寫成淡色平疤，且補細節那一段也要寫「no redness」。
3. **陰天要寫進每一鏡的正文**：場景圖是陰天，Grant 那支仍出現藍天。
4. 坑：`h3.sh batch` 的 `prompt_file` 相對於**目前目錄**（要先 `cd` 到 manifest 所在目錄）；給了 `--session` 就要先 `h3.sh start` 開好那個 session。

## 站主決定（2026-11-10）

- **台詞與嘴型照《種田》《恁祖媽》的內建做法**：H3 出無聲片段，聲音用站台的 Gemini 語音另外合成；不另接對嘴模型。
  分鏡照 `storyboard-shot-spec.md`：說話的人在畫面上寫「嘴在說話」、其他人「嘴閉著」；台詞放在反應鏡上標「畫外」；心裡話標「心裡話，嘴閉著」。
  嘴是「在說話」，不是逐字對上；說話的正臉大特寫少用、短句為主。

- **聲音與定妝照照預設**（站主「照內建的」）：聲音用 `cast.json` 的預設（Nora Despina、Elias Charon、Grant Algieba、Peg Gacrux）；定妝照用這次選的 Nora b、Elias a、Grant a、Peg a，與三套換裝、三個場景一起存進 `../assets/refs/`。

## 點數

帳號 b 餘額 2,297.22 → 2,278.22（−19.0）。但同一帳號另有一個不是這次開的 runtime 一直在跑（`rate_per_hour` 10.05、`active_assignments` 1，試鏡前後都在），
一小時約 10 CU；扣掉它，**這次試鏡約 9 CU**（兩個 session 合計約 60 分鐘：出圖 32 分、片段 28 分）。

## 聲音試聽

站台 Gemini TTS，四個主角各三個候選（台詞在 `audition/`，風格是 `cast.json` 的 voice.style）：
Nora Despina／Kore／Aoede、Elias Charon／Alnilam／Orus、Grant Algieba／Achird／Schedar、Peg Gacrux／Vindemiatrix／Sulafat。
共 2,820 個計費字元。樣本已交站主；站主 2026-11-10 定用預設。

## 重跑

```bash
B=docs/videos/series-plans/top40-2025-2026/2025-15-xingde-xiangyu/western/production/screen-test
K=$PWD/.agents/skills/minimax-h3-colab/scripts
W=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/till-the-verdict/screen-test
P="--pick nora=b --pick elias=a --pick grant=a --pick peg=a"
bash $K/bootstrap.sh && bash $K/h3.sh usage
python3 -I $B/build.py r1 && bash $K/h3.sh start --session ttv-st --gpu G4
bash $K/h3.sh images --detached --manifest $W/r1.json --output-dir $W --progress $W/r1.progress.json --session ttv-st
python3 -I $B/build.py r2 $P && bash $K/h3.sh images --detached --manifest $W/r2.json --output-dir $W --progress $W/r2.progress.json --session ttv-st
bash $K/h3.sh stop --session ttv-st
python3 -I $B/build.py st1 $P && H3_PROFILE=hero bash $K/bootstrap.sh patch && bash $K/h3.sh start --session ttv-st1 --gpu G4
(cd $W/st1 && bash $K/h3.sh batch --manifest $W/st1/st1.json --output-dir $W/st1/out --progress $W/st1/progress.json --session ttv-st1)
python3 -I $B/build.py st2 && (cd $W/st2 && bash $K/h3.sh refine --manifest $W/st2/st2.json --output-dir $W/st2/refined --session ttv-st1)
bash $K/h3.sh stop --session ttv-st1 && bash $K/bootstrap.sh patch && bash $K/h3.sh usage
```

`runs/` 是這次送出的 manifest、進度檔與正文（`<W>` 是工作資料夾）；圖與片段不進 repo（repo 容量接近上限）。
圖、片段、錄音與 log 的備份在雲端硬碟 `AI/備份/AI劇/婚約到他判刑那天為止（歐美版）/_共用/製作檔/`（站主 2026-11-12）；
之後各集的製作檔放同一部劇的 `第001集/製作檔/<工作資料夾名>/`，照 `docs/videos/AI-DRAMA-DRIVE.md` 用 `todrive.sh` 傳。

## 直式小樣（2026-11-10，站主點頭，上限 6 CU）

第 1 集 c06–c08（`vpilot.py`），全程直式三段式：Ref2VA hero 544×960 → σ0.5 補細節 736×1312 → SeedVR2 7B 到 1080×1920（PR #2067 修好的放大筆記本）。
場景圖先畫直式臥室 1088×1920 兩張，選 a（玻璃牆在右、床頭櫃在床與玻璃之間、陰天灰海）。參考圖：`assets/refs/nora-portrait.jpg` ＋直式臥室。

| 鏡 | 草稿第一次 | 改寫後重跑 | 成片 |
| --- | --- | --- | --- |
| c06 咬藥、說 "My pill tastes sweet today." | 先喝水才咬，杯裡的水變褐色 | 寫「不喝水、杯子留在腿上、水保持清澈」後正確：咬、停、皺眉、說話 | 可用 |
| c07 吐半顆藥在面紙 | 可用 | — | 可用；藥片被畫成小花形、中間帶黃，正式拍要寫「plain white, no markings, no colour」 |
| c08 對著光看半顆藥 | 「half white tablet」被畫成**平板電腦** | 改寫「a tiny half of a white pill, smaller than a fingernail (a medicine pill, not a device)」後正確 | 可用；尾端有一點笑，正式拍再加強「not smiling」 |

- **直式構圖成立**：臉、懷孕的身形、玻璃屋與陰天在 9:16 裡都守住；三支成片都是 1080×1920、124 格（5.17 秒）。
- **教訓**：`tablet` 這個字會被讀成平板，藥一律寫 pill 並寫大小；「不喝水」要寫成水杯在哪、水是什麼顏色。
- **時間**（G4）：出圖 session 約 12 分鐘；片段 session 約 28 分鐘（草稿 3 支＋重跑 2 支、補細節 3 支、SeedVR2 每支 123–236 秒）。
- **點數**：帳號 b 餘額 2,271.34 → 2,263.56（−7.8），其中有一段同帳號另一個 runtime 也在跑（16:34 時 `active_assignments` 2）；這次小樣本身約 5–6 CU，在 6 CU 上限內。

## 備份（2026-11-12）

照 `docs/videos/AI-DRAMA-DRIVE.md`，用 `docs/videos/ai-drama-drive/todrive.sh` 傳到站主的雲端硬碟（劇名資料夾 `婚約到他判刑那天為止（歐美版）`，試鏡與小樣跨集共用，放 `_共用`）：

- `AI劇/婚約到他判刑那天為止（歐美版）/_共用/製作檔/till-the-verdict/`：工作資料夾全部（橫式試鏡的原圖 PNG、4 支草稿與 4 支補細節、直式臥室圖、直式三鏡三段的每一版、配音試聽原檔、manifest、進度檔、log），180 個檔，`todrive: 180 files, 0 differences`。
- `AI劇/婚約到他判刑那天為止（歐美版）/_共用/製作檔/交給站主的檔案-20261110/`：交給站主看的拼圖、合成片、聲音 mp3，17 個檔，0 differences。
- 2026-11-10 先用雲端硬碟連接器傳過一份聲音 `voices-mp3.zip` 到舊位置 `AI/備份/drama/till-the-verdict/screen-test-20261110/`（新規則出來之前），內容已包含在上面。

## 定妝照修圖 r3（2026-11-12，站主點頭）

分鏡二審（`../../review/2026-11-12-e001-e003-storyboard-r2.md`）抓到參考圖會蓋過文字：`nora-portrait.jpg` 左頰與頸部的小紅痕（像傷口），
`nora-work.jpg` 同樣的紅痕，`grant-portrait.jpg` 閉嘴微笑。`build.py r3`：Qwen-Image-Edit，`latent: image1`，每張「exactly one change」兩個種子。

| 圖 | a | b | 建議 |
| --- | --- | --- | --- |
| Nora 定妝照 | 紅痕沒了，但右頰多出一片紅點 | 臉頰與脖子都乾淨，其他照原圖 | **b** |
| Grant 定妝照 | 嘴角仍微微上揚 | 嘴閉著、嘴角平、眼鏡不變 | **b** |
| Nora 工作服 | 脖子乾淨，兩頰的雀斑帶一點紅 | 兩頰的紅更明顯 | **a** |

- Colab 這次分到 A100（RTX PRO 6000），每小時約 10 CU；出圖 session 約 15 分鐘，帳號 b 餘額 2,020.63 → 2,019.08（約 −1.6）。
- 圖在雲端硬碟 `AI/備份/AI劇/婚約到他判刑那天為止（歐美版）/_共用/製作檔/screen-test/`（`todrive.sh` 23 files, 0 differences）。
- 站主 2026-11-12 照建議選 Nora b、Grant b、Nora 工作服 a，已換進 `../assets/refs/`、重算 `SHA256SUMS`。

## 原聲小樣（2026-11-12，站主點頭，上限 6 CU）

站主改用模型原聲之後，先驗 H3 會不會照寫的英文講、同一個角色跨鏡的聲音一不一致、短喊怎麼做。`voicepilot.py st1`：Ref2VA hero 第一段草稿 544×960、6 秒，
只給定妝照一張（場景用文字寫），7 支取自 2026-11-12 審過的分鏡；同一個角色每支都寫同一句聲音描述。

| 支 | 台詞（寫的） | Whisper 聽到的 | 音高中位數 |
| --- | --- | --- | --- |
| e001-c07-a Nora | My pill tastes sweet today. | 同 | 198 Hz |
| e001-c07-b Nora（同上，另一個種子） | 同上 | 同 | 189 Hz |
| e001-c44 Nora | The score line's too faint. That's not right. | 同 | 198 Hz |
| e003-c27 Nora | Your phone died? Then what's that? | 同 | 205 Hz |
| e002-c13 Nora 短喊 | Help! Somebody! | **Help! Help! Somebody!** | 340 Hz（喊） |
| e003-c12 Grant | We're still young, Nor. We'll try again. | 同 | 93 Hz |
| e001-c36 Peg | Soup's in the fridge. Salt it yourself. | 同 | 176 Hz |

- **台詞**：七支都照寫的英文講，沒有亂編、沒有多講；只有短喊多喊了一聲 "Help!"。說話在片段第 1.1–3.9 秒開始（前面是寫在台詞前的動作），講完到片尾還有 0.6–1.2 秒安靜。
- **同一個角色**：Nora 四支（含兩個種子）音高都在 189–205 Hz；音高相近不等於音色相同，**要站主聽**（`review/till-the-verdict-voicepilot.mp4`，46 秒）。
- **短喊**：原文寫進說話句，畫面上**沒有**燒出字幕或文字；但會多喊一兩個字。所以原聲的短喊照寫原文，剪接時剪掉多的那一聲。
- **表情**：Grant 寫了 `no smile at any moment`，四格都在笑：說話句裡的 `warm`、`like a keynote` 把笑帶出來了。Grant 的說話句不寫 warm、keynote、smooth，改寫他的臉（眉心提高、嘴角平）與「聲音平穩、低」。其他六支沒有不該有的笑。
- **景別**：寫 close-up 的短喊拍成全身、c07 拍成中景：只給定妝照、沒有場景圖時景別會拉遠；正式拍照分鏡給場景圖，並寫「第一格就是○○的臉與肩膀，整鏡不拉遠」。
- **時間與點數**：Colab 又分到 A100（RTX PRO 6000，每小時約 10 CU）；7 支草稿約 16 分鐘，帳號 b 餘額 2,018.25 → 2,015.74（約 −2.5，入帳可能延遲）。
- 備份：`AI/備份/AI劇/婚約到他判刑那天為止（歐美版）/_共用/製作檔/voicepilot/`（草稿、提示詞、進度、轉錄腳本、給站主的合輯）。


## 第一批參考圖（第 1–10 集）

站主 2026-11-12 點頭（上限 35 CU）。`art.py` 照 `../art-plan-people.md`、`../art-plan-sets.md`、`../art-plan-props.md` 把第 1–10 集要的人、場景、道具排成 12 輪 manifest；
場景與道具的英文提示詞在建 manifest 時從企劃的表讀出來（企劃改了，下一次建的 manifest 就跟著改），人物的外貌句讀 `../cast.json`（跟企劃不同時以 `cast.json` 為準）。
Qwen-Image-Edit、`lora: false`、20 步、CFG 4，每項兩個種子；場景的「改自」版本只畫一個種子（企劃〈估價〉）。輸出檔名是 `<輪>-<id>.png`，後面的輪從工作資料夾讀選定的那張。

| 輪 | 內容 | 張數 | 約 CU | 要等 |
| --- | --- | --- | --- | --- |
| a1 | Cole、Nora `night-coat` 全身、Nora `hospital`、Dr. Brandt、Nurse Kim、工頭 | 12 | 3.24 | — |
| a2 | Grant `rain`、值班醫生、Nora `discharge` 全身、Fisk、Sienna、副警長 | 12 | 3.24 | — |
| a3 | Sienna 全身（從選定的 Sienna 胸像）、Bev | 4 | 1.08 | `--pick sienna=` |
| s1 | #2 臥室夜（改自已有的直式臥室 a）、#5 客廳白天、#7 大門屋裡白天、#9 嬰兒房白天、#12 大門外夜雨、#14 救護車 | 11 | 2.97 | — |
| s2 | #15 走廊、#16 病房夜、#19 白車後座、#20 大門外金光、#21 客廳金光 a、#24 大門屋裡金光 | 12 | 3.24 | — |
| s3 | #27 書房、#28 坡道、#29 白車坡底、#30 公車站、#31 汽車旅館櫃台、#32 汽車旅館房間 | 12 | 3.24 | — |
| s4 | 「改自」：#3、#6、#17、#18、#22、#25、#33 | 7 | 1.89 | `--pick liv-day= room-night= liv-gold-a= nur-day= mroom-night=`（#3 讀 s1 的 #2） |
| s5 | 「改自」的「改自」：#23、#26 | 2 | 0.54 | s4 驗收過（單一種子，不用選） |
| s6 | 優先 3：#8、#10、#11、#13、#34（站主可以刪） | 7 | 1.89 | `--pick door-in-day= liv-day=` |
| p1 | 半顆藥、毛線帽、玻璃磚、Nora 與 Peg 的行李箱、No. 1 花瓶 | 12 | 3.24 | — |
| p2 | 白車、黑車（1920×1088）、帳本、Peg 的戒指、帆布袋、駝色大衣 | 12 | 3.24 | — |
| p3 | 工廠版花瓶（第 1 集電視廣告；在選定的 No. 1 上 exactly one change） | 2 | 0.54 | `--pick forever-no1=` |
| 合計 | 不含 s6 | **98** | **26.46** | |
| | 含 s6 | 105 | 28.35 | |

- **沒排的**：調度員（只有聲音）、另一個工人（只拍背影）、Nora `pregnant` 全身（企劃標「選」）、`real-pill`（第 11 集）、`receipt`（第 5、9 集摺著照文字，圖要等 `light-box`）。
  No. 1 花瓶第一次是第 26 集，排在 p1 是因為第 1 集的工廠版要從它改。
- **全身照**：照企劃〈怎麼畫〉，image 1 是 `assets/refs/` 的胸像、`latent: empty`、1088×1920（〔FULL〕〔FACE1〕）；a1 的 `night-coat` 是這個做法的試驗，臉跑掉就先停。
- **跟企劃的字不一樣的地方**（`cast.json` 為準）：Nora `night-coat` 寫 `soft slippers`（企劃寫 `soft cream slippers on her feet`）、Sienna 全身沒有 `clearly visible`；
  Nora `hospital` 的 `cast.json` 句子同時有 `with natural light makeup` 與 `no makeup`，企劃拿掉了前者，manifest 照 `cast.json` 留著，**要改 `cast.json`**。
  照企劃改的：副警長只留上衣、`night-coat` 拿掉 `pain only in her face and posture`，胸像另外拿掉 `wrist`（Sienna 的錶）等 `bust()` 漏掉的字。
- s1 的 #2 從已有的直式臥室早晨版改：`art.py` 先找 `assets/refs/`，沒有就從 vpilot 的工作資料夾（`set-bedroom-v-a.png`）複製；兩處都沒有就從雲端硬碟拿回來。
- 種子：人物 714000 起（企劃的順序，每張加一）、場景 `740000 + 格號 × 10`、道具 `760000 + 表裡的列 × 10`。

```bash
B=docs/videos/series-plans/top40-2025-2026/2025-15-xingde-xiangyu/western/production/screen-test
K=$PWD/.agents/skills/minimax-h3-colab/scripts
W=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/till-the-verdict/art
python3 -I $B/art.py --list                                  # 每一輪的張數、要選的圖、約 CU
bash $K/bootstrap.sh && bash $K/h3.sh usage
# 不用選圖的輪（a1 a2 s1 s2 s3 p1 p2）可以在同一個 session 連跑，只冷啟動一次
bash $K/h3.sh start --session ttv-art --gpu G4
for r in a1 a2 s1 s2 s3 p1 p2; do
  python3 -I $B/art.py $r && bash $K/h3.sh images-check --manifest $W/$r.json &&
  bash $K/h3.sh images --detached --manifest $W/$r.json --output-dir $W --progress $W/$r.progress.json --session ttv-art
done
bash $K/h3.sh stop --session ttv-art                          # 等站主挑圖時不要開著 runtime
# 站主挑完：選定的照 ../assets/refs/README.md 存進 assets/refs/，再跑要選圖的輪
python3 -I $B/art.py a3 --pick sienna=b
python3 -I $B/art.py s4 --pick liv-day=a --pick room-night=b --pick liv-gold-a=a --pick nur-day=a --pick mroom-night=b
python3 -I $B/art.py p3 --pick forever-no1=a
bash $K/h3.sh images --detached --manifest $W/a3.json --output-dir $W --progress $W/a3.progress.json --session ttv-art2 --new-session --stop-on-complete
python3 -I $B/art.py s5                                       # s4 驗收過之後
```

離線試跑（不連網、不花錢）：`python3 -I $B/art.py <輪> --work <暫存資料夾> --placeholders --pick …`，選定的圖還沒畫就寫灰色替身；
真的跑時 `art.py` 會擋下工作資料夾裡留著的替身（小於 50 KB 的檔）。2026-11-12 十二輪都試跑過、`images-check` 0 錯誤（警告只有「不是 16:9」，胸像與直式本來就不是）。
每輪跑完照企劃的〈驗收〉挑圖，原圖照 `docs/videos/AI-DRAMA-DRIVE.md` 用 `todrive.sh` 傳到 `_共用/製作檔/`。

### 進度與交接（2026-11-12 15:35 UTC）

站主 2026-11-12「參考圖 你建議決定」：選圖由 Claude 決定，每張選定的理由寫在 `../assets/refs/README.md`〈First batch〉，`adopt.py` 轉 JPEG、補列與 `SHA256SUMS`。

- **已跑完**：a1＋a2 合成一份 `a12`（22 張）、s1（11）、s2（12）。選定 19 張已進 `assets/refs/`。
- **a12 的兩個錯**：Sienna 用了全身範本、沒有臉的參考（`art.py` 現在的 a2 是對的胸像，合併清單哪裡出錯沒查到）；Nora `hospital` 兩張都畫成淡藍 V 領刷手服，跟 Nurse Kim 撞色，
  `cast.json` 與企劃改成「白底淡藍小菱格病人袍、圓領按扣、短袖」。Dr. Brandt 與副警長選定的那張有編出來的字。新的 **a4** 輪重畫前兩者、在後兩者上只改一處擦字（8 張）。
- **工頭** 從 a1 移到 a3（a12 沒畫到）；a3 的 Sienna 全身讀 a4 選定的胸像（`drawn()` 依 a4、a2、a1、a12 的順序找）。
- **排隊中**（`~/mokaair-work/.../art/chain2.sh`，session `ttv-art`）：s3 → p1 → p2 → a4 → s4 → p3，跑完自動 `h3.sh stop`。s4、p3 的 manifest 要在選完 s3、p1 之後寫進工作資料夾，`chain2.sh` 跑到時有檔才跑。
  已選：`liv-day=a nur-day=b door-in-day=a room-night=a liv-gold-a=a`（工作資料夾 `picks.txt`）；還缺 `mroom-night`（s3）、`forever-no1`（p1）。
- **之後**：a4 選定後跑 a3（Sienna 全身、工頭、Bev）與 s5；s6 是優先 3，可不跑。全部約 30 CU，在 35 CU 上限內。
- **備份**：2026-11-12 15:33 工作資料夾整包傳到 `videobackup:AI劇/婚約到他判刑那天為止（歐美版）/_共用/製作檔/till-the-verdict`（268 個檔；12 個差異是當時正在寫的 p1 暫存檔）。每輪選完再傳一次，同一指令。
- **2026-11-12 稽核後**：第 1–20 集分鏡逐鏡對照選定的圖（`../../review/2026-11-12-ref-audit-e001-e020.md`），格局錯的場景與幾處人物、道具由 `redraw.py`（s7、s8、a5、p4，34 張）重畫，排在 `chain2.sh` 的 s4 位置；
  改光線的 s4 等新底圖選定後再建。站主同日「品質為主」：第一批因此約 36.7 CU，超過原本 35 CU 的上限，照做。
- **重跑紀錄**：
  - chain2 跑到背景任務的 2 小時上限被停掉，chain3 接手。
  - p3 那批在第 8 張遇到 Colab 端送出逾時（600 秒），整批停下；剩下的 31 張改成 p6，由 chain4 在同一台機器上補跑。
  - 半顆藥第三次仍畫成整顆或兩半連著，p6 改用 p1 那張整顆藥做「只剩一半」的單處修改。
  - Nora 定妝照的雀斑修圖（f1 a）額頭乾淨了，但構圖被拉近、臉有點變，右下角還多了像浮水印的字，所以**不換**鎖定的定妝照，留作候選給站主看。
- **session 中斷時**：Colab runtime 會一直燒點數，先 `bash $K/h3.sh stop --session ttv-art`；工作資料夾在雲端硬碟上，拿回來放回 `$W` 就能接著用 `art.py` 建下一輪。
