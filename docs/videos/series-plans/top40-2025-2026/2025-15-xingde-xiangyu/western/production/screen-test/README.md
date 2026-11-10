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
