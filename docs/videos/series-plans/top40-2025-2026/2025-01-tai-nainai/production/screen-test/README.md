# 《祖奶奶今年十八》角色與試鏡：開拍前的計畫

站主 2026-11-06 要先評估真人劇，再開角色。這份是試鏡的計畫，**還沒花任何 compute units**。票是 `tasks/open/2026-11-06-tai-nainai-screen-test.md`。
跑之前站主要點頭；聲音的樣本已經錄好，站主下次聽完再確認。

## 為什麼要試鏡

`cast.json` 的 look 寫的是真人電影感，但 repo 裡沒有任何一次真人風格的實測。《種田》在 Colab 做完整季的是 3D CG，
而且 Qwen-Image-Edit 畫的首格臉，到不了定妝照的質感（`minimax-h3-colab/references/lessons.md` 第 1 節）。
市場上有真人風的 AI 劇做到幾十萬觀看（`docs/videos/drama-craft/reference-study-20261003.md` 的 A 片），所以值得試。

這部劇本會讓真人路線特別難的地方：

| 風險 | 為什麼 | 試鏡怎麼看 |
| --- | --- | --- |
| 臉的一致性 | 1,577 鏡、30 個角色，真人臉一漂就像換了演員 | c20、c23 兩支同一個人，對定妝照 |
| 老化記號太細 | 進度條是右手背一道細紋、淡一線、右鬢一縷白髮（bible〈燈帳〉） | 第二輪的手背插鏡：看得見嗎、畫得準嗎 |
| 嘴型 | 說話的人嘴要動，H3 不照配音對嘴 | c14 林美鳳說話 |
| 一人兩貌 | 九十六歲與十八歲要認得出是同一人 | 第二輪用十八歲當 image 1 畫九十六歲；c17 對 c23 |
| 手拿小道具 | 戒指印面朝掌心、翻手、五根手指 | c20 看手 |
| 未成年與像真人 | 小滿、何曉陽是寫實的十七歲；生成的臉可能撞到明星 | 選定妝照時看；這次不畫學生 |

## 試鏡內容

全部從 `cast.json` 照抄外貌、場景與燈的英文，提示詞由 `build.py` 產生，不手改。

| 輪 | 做什麼 | 張數／支數 | 尺寸 |
| --- | --- | --- | --- |
| r1 定妝照與場景 | 真人：月棠（十八歲壽衣 `shouyi`）、林美鳳、福伯各兩個 seed；祠堂（燈 3）、正廳。3D 對照：三人各一張、正廳一張 | 12 張 | 胸像 1248×1664；場景 1920×1088 |
| r2 一人兩貌、細紋 | 以選中的十八歲當 image 1 畫九十六歲：真人兩個 seed、3D 一張；手背細紋插鏡一張 | 4 張 | 1248×1664；插鏡 1312×736 |
| 片段 | 第 1 集真人 c14（林美鳳說話）、c17（九十六歲閉眼，燈 1）、c20（看手、戒指，燈 3）、c23（十八歲近景）；3D 的 c14 | 5 支 | Ref2VA 960×544 `hero` → σ0.5 補到 1312×736 → SeedVR2 7B 到 1920×1080（《種田》第 33 集起的路線 A） |
| 聲音 | 月棠十八歲：Kore（暫定）、Despina、Achernar；九十六歲：Gacrux（暫定）、Vindemiatrix、Achernar | 6 個樣本，**已錄** | 站台 Gemini，各 111 字 |

聲音樣本在這個 session 的 `~/mokaair-work/videos/_audition/2026-11-06T14-28-41-378Z/`（十八歲）與 `…T14-29-02-733Z/`（九十六歲），
台詞與 style 在 `audition/`。容器回收就沒了；要重錄照下面的指令跑，約 222 字。注意：九十六歲選 Achernar 的話，春桃阿婆要換聲音（bible〈聲音〉），撞聲檢查要重跑；
十八歲與九十六歲不能都選 Achernar。

## 過關條件（站主看並排、再找一個沒參與的人冷看）

1. 臉：同一個角色在片段裡跟定妝照是同一張臉，c20 與 c23 之間不漂。
2. 實速看不假、不詭異（不是逐格看）。
3. 嘴：c14 的嘴型站主能接受；不能接受的話，真人路線要把說話鏡大量改成聽者反應鏡，這會改到劇本規格第 10 項。
4. 一人兩貌：不告訴觀眾的情況下，認得出九十六歲與十八歲是同一人。
5. 手：c20 十根手指、戒指在左手無名指。
6. 細紋：插鏡看得見一道細紋、其他地方不老。看不見就改設計（記號做大、只用插鏡與光交代），不是放棄真人。

真人過 1–5 才走真人；3D 也照同樣幾條比。兩個都不過，就把結果帶回來重想（例如改鏡頭設計），不硬上。

## 成本（推算，未實測）

| 段 | 時間 | CU |
| --- | --- | --- |
| r1＋r2 圖（16 張，約 1.3 分／張，含一次冷啟動 10–15 分） | 約 35 分 | 約 5 |
| 片段三段式（5 支，暖機後約 7 分／支，三段各一次冷啟動） | 約 45 分 | 約 5（三段式實測約 0.9 CU／支） |
| 合計 | 約 1.5 小時 | **約 10–12 CU**，上限 15 CU（含幾張重畫） |

2026-11-06 帳號 A 餘額 68.31 CU（`h3.sh usage`）。G4 約 7.6–8.4 CU／小時（`three-stage.md` 第三節）。
到 15 CU 就停下來回報，不再重抽。

## 怎麼跑（站主點頭之後）

```bash
B=docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/screen-test
K=.agents/skills/minimax-h3-colab/scripts
W=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/tai-nainai/screen-test
bash $K/bootstrap.sh && bash $K/h3.sh usage                     # 每個新 session；抄下餘額

# r1：先試兩張（空白灰底當 image 1 沒試過），對了再整批
python3 -I $B/build.py r1
bash $K/h3.sh images-check --manifest $W/r1.json
bash $K/h3.sh start --session tn-st --gpu G4
bash $K/h3.sh images --detached --manifest $W/r1.json --output-dir $W --progress $W/r1.progress.json --session tn-st --only yuetang-18-a,set-citang-a
bash $K/h3.sh images --detached --manifest $W/r1.json --output-dir $W --progress $W/r1.progress.json --session tn-st

# 選 take（看圖），r2
python3 -I $B/build.py r2 --pick yuetang-18=a --pick yuetang-18-3d=a
bash $K/h3.sh images --detached --manifest $W/r2.json --output-dir $W --progress $W/r2.progress.json --session tn-st
bash $K/h3.sh stop --session tn-st

# 片段第一段（hero），審草稿；第二、三段
python3 -I $B/build.py st1 --pick meifeng=a --pick yuetang-18=a --pick yuetang-96=a --pick meifeng-3d=a
H3_PROFILE=hero bash $K/bootstrap.sh patch
COLAB_GPU=G4 bash $K/h3.sh batch --manifest $W/st1/st1.json --output-dir $W/st1/out --progress $W/st1/progress.json --session tn-st1
python3 -I $B/build.py st2 && python3 $K/refine.py --manifest $W/st2/st2.json --check
bash $K/h3.sh refine --manifest $W/st2/st2.json --output-dir $W/st2/refined --session tn-st2
bash $K/h3.sh upscale --input-dir $W/st2/refined --output-dir $W/final --session tn-st2
bash $K/h3.sh stop --session tn-st2 && bash $K/bootstrap.sh patch && bash $K/h3.sh usage
```

聲音重錄（站台 Gemini，要影片工具權杖）：

```bash
node tools/video/cli.mjs audition --text-file $B/audition/yuetang-18.txt --voices gemini:Kore,gemini:Despina,gemini:Achernar --style "$(cat $B/audition/yuetang-18.style)"
node tools/video/cli.mjs audition --text-file $B/audition/yuetang-96.txt --voices gemini:Gacrux,gemini:Vindemiatrix,gemini:Achernar --style "$(cat $B/audition/yuetang-96.style)"
```

收工：選中的定妝照、場景圖放進 `production/assets/refs/`（照《種田》`assets/README.md` 的做法加 `SHA256SUMS`），seed 與取捨寫進這份與票。

## 要站主決定的

1. **可以開跑試鏡嗎**（約 10–12 CU，上限 15）？
2. **聲音**：月棠十八歲選哪個、九十六歲選哪個（樣本已傳，下次聽）。
3. 試鏡之後：真人或 3D；之後才畫全季（bible〈先畫順序〉第 1 批：還有建業、建邦、小滿、阿凱與換裝 look）。

## 還沒驗的事

- Qwen-Image-Edit 拿空白灰底當 image 1 會不會照提示詞畫出人（r1 先試兩張）。
- H3 Ref2VA 吃真人定妝照，臉與皮膚守不守得住；SeedVR2 補的皮膚紋理在真人上是加分，3D 上要盯。
- 每支片段實際的 CU 與時間（照《種田》3D 的數字推算）。
