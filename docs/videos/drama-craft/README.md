# 參考片量測紀錄

這個資料夾放**從 YouTube 上的參考片量出來的數字**：剪接節奏、開場、景別、台詞、動作量，以及量法本身的限制。`.agents/skills/youtube-video/references/drama-craft.md` 的目標表引用這裡的數字；表裡每個「量到的」都要能在這裡找到是哪支片、哪一段、怎麼量的。紀錄一份一份加，不覆寫舊的：舊的量法改了，舊的數字還要能比。

## 有哪些紀錄

| 檔案 | 量什麼 | 怎麼量 | 用在哪 |
| --- | --- | --- | --- |
| `reference-study-20261003.md`、`.json` | 五支以「AI漫剧」搜尋選出的中文對話劇（含站主指定的《山海经之万兽图鉴》）前 240 秒：鏡長分布、開場、鏡位、台詞長度、包裝 | 瀏覽器探針 `yt_shot_probe.js`，每 0.25 秒一格；A 片前 120 秒由另一個代理獨立重量 | `drama-craft.md` 的目標表與 `drama_craft_check.mjs` 的 `TARGETS`、`REFERENCE` |
| `reference-study-20261004-budaimiao.md`、`.json` | 真一隻布袋喵七支打鬥特效片從頭到尾：逐鏡的景別、主體、人數、字幕、轉場，AI 弱點怎麼處理 | 瀏覽器探針加逐鏡目視標記；A、B 兩支由另外兩個代理交叉裁定剪點 | `animation-preproduction` 的 `shot-risk.md` 與 `animation-camera` 的 `budaimiao-style.md` |

md 寫結論、方法與「量到／目視／推論／沒驗」的分界；json 放數字與原始鏡長（或逐鏡表），讓下一個人不用重看影片就能重算。

## 兩種量法

| | 瀏覽器探針 `.agents/skills/youtube-video/scripts/yt_shot_probe.js` | 離線分析 `.agents/skills/youtube-video/scripts/reference_analysis.mjs` |
| --- | --- | --- |
| 下載 | 不下載，在內建瀏覽器的觀看頁上跳格讀畫面 | 本機檔案，或由站主決定後呼叫 yt-dlp 下載到暫存目錄、量完刪掉；進 repo 的只有數字 |
| 格距 | 0.25 秒一格（布袋喵 B 片 0.125） | 剪點逐格；動作每 0.25 秒一格（`--step`） |
| 長度 | 面板藏著時 seek 在 60 秒後失敗；最多量過 240 秒 | 任何長度、任何區段（`--range`，可重複） |
| 剪點規則 | 兩格亮度差 ≥ 26/255 加突變或直方圖位移（`cuts()`，沒改過，舊紀錄可比） | `select='gt(scene,0.3)'`：相鄰兩格平均亮度差 ≥ 30/255 且比前一對多跳 30（`--scene`；0.1 以上的候選分數都留在 `scene_scores`） |
| 特效片 | 短鏡連在一起被併成一個剪點，閃光被算成剪點；`stats()` 的 `suspected_multi_cut_runs` 標出來 | 逐格所以不併，但閃光、爆炸、甩鏡一樣會多算；兩種量法在特效片都只能寫範圍 |
| 看得到畫面內容 | 看得到：每鏡一格的聯絡表、字幕帶，景別、臉、插鏡、台詞都從這裡來 | 看不到：只有數字 |
| 動作 | `near_frozen_share`、`high_motion_share`（鏡內取樣格的亮度差 <1、≥20 的比例） | 同名同義，加 frozen／slow／active 四種比例與平均差（`signalstats` 的 YDIF，64×64、去掉底部 26%） |
| 亮度、色彩 | 沒有 | `picture`：YAVG 的平均、p10、p90，SATAVG 的平均 |
| 聲音 | 沒有（面板靜音） | `sound`：`silencedetect` 的靜音段與有聲音的比例；有配樂時是台詞密度的上限，不是台詞 |
| 網頁資料 | `meta()`：片名、頻道、觀看數、畫質、CC 軌 | `--url` 時從 yt-dlp 的 metadata 填同樣的欄位；本機檔案是 null |
| 什麼時候用 | 要看畫面內容、不想下載、前幾分鐘就夠 | 要量全片或後段、要動作量或聲音、探針到不了 60 秒之後 |

兩種量法互補。一份完整的紀錄通常兩個都用：探針的聯絡表標景別與台詞，離線分析給全片的鏡長分布與動作量。`--compare` 讓兩邊對答案（見下）。

## JSON 的形狀（`schema_version` 1）

頂層：`schema_version`、`checked_on`（量測日）、`method`（工具、在哪量、每個數字的規則、`not_checked`）、`videos[]`。布袋喵那份另有 `channel`（頻道盤點）與 `cross_check[]`（交叉裁定）。

`videos[]` 的每一支：`id`、`url`、片名（`series` 或 `title`）、`channel`、`published`、`duration_seconds`、`views_at_check`、`frame`（`16:9`、`9:16`、`2.33:1`）、`highest_quality`、`caption_tracks`，然後是 `ranges[]`（探針與離線分析）或逐鏡表 `shots[]` 加 `shot_columns`（布袋喵）。離線分析多一個 `source`（檔名、大小、sha256、容器、編碼、有沒有聲音、是不是下載的）。

`ranges[]` 的每一段，兩種量法算法相同（探針的 `stats()`；`tools/reference-analysis.test.mjs` 拿 2026-10-03 紀錄的四段鏡長反算回每個已發表的數字）：

| 欄位 | 意思 |
| --- | --- |
| `range` | `[起, 迄]` 秒 |
| `shots`、`lengths` | 鏡頭數與每個鏡頭的秒數（兩位小數；探針是 0.25 的倍數） |
| `mean`、`median`、`p10`、`p90`、`longest` | 平均、中位數、第 10／90 百分位、最長；分位數是 `sorted[floor(p × n)]` |
| `over_6s` | 超過 6 秒的鏡頭數 |
| `opening_10s`、`opening_30s` | 前 10／30 秒開始的鏡頭數（含第一個） |
| `spread_p90_over_p10` | 長短差，p90 ÷ p10 |
| `near_frozen_share`、`high_motion_share` | 鏡內取樣格裡亮度差 <1／≥20 的比例 |
| `cuts` | 剪點秒數（探針是取樣格，離線是新鏡頭第一格） |

離線分析再加：`scene_threshold`、`scene_scores`（`[[秒, 分數], …]`，0.1 以上的候選）、`motion`（`samples`、`inside_shots`、`step_seconds`、`frozen_share`、`slow_share`、`active_share`、`high_motion_share`、`mean_difference`）、`picture`（`luma_mean`、`luma_p10`、`luma_p90`、`saturation_mean`）、`sound`（`silence_db`、`min_silence_seconds`、`silent_seconds`、`silent_share`、`non_silent_share`、`silences`、`longest_silence`、`silence_times`；沒有音軌是 null）。

`--compare` 另寫 `comparison[]`：對每一段、對紀錄裡同一支片的每份剪點清單（`ranges[].lengths` 累加、`shots[]` 的起點、`cross_check[].verifier_cut_times`），在兩邊都涵蓋的秒數內以 ±0.3 秒一對一配對：`recorded`、`here`、`matched`、`only_here`、`only_recorded`。

## 怎麼新增一份紀錄

1. 至少三支、同題材；先讀 `drama-craft.md` 第八節的規矩（記片名、頻道、網址、查閱日、觀看數；畫面可見、推論、沒驗分開寫；引用只到說明結構所需）。
2. 瀏覽器探針照 `yt_shot_probe.js` 檔頭的步驟；離線分析：

   ```bash
   node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url <id 或網址> [--range 0-240] --out <OUT>/<id>.json [--compare <既有紀錄.json>]
   node .agents/skills/youtube-video/scripts/reference_analysis.mjs --file <本機影片> [--range A-B]... --out <OUT>/<id>.json
   ```

   需要 ffmpeg（`FFMPEG_PATH`、PATH 或 Windows 的 winget 套件）；`--url` 另需 yt-dlp（`pip install yt-dlp`、`winget install yt-dlp.yt-dlp`，或 `--yt-dlp <路徑>`）。yt-dlp 是外部程式，repo 不內含；要不要下載是站主的決定（YouTube 服務條款），下載到暫存目錄、量完刪掉（`--keep` 留著），影片不進 repo、不進素材。
3. 引用數字之前對過答案：探針拿聯絡表對剪點、請另一個代理重量一支；離線分析用 `--compare` 對既有的清單，對話劇要對得上才引用，特效片兩邊都會錯、只寫範圍。
4. 寫成 `reference-study-<YYYYMMDD>[-<題材>].md` 與 `.json`，加進上面的表；目標改了回去改 `drama-craft.md` 的表與 `drama_craft_check.mjs` 的 `TARGETS`、`REFERENCE`。

## 還沒量的

探針在 2026-10-05 只重量到前 60 秒（`2026-10-05-re-run-yt-shot-probe-past`）；離線分析開出來的環境連不到 YouTube，沒有下載任何影片。站主決定下載後跑：

```bash
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url xVXEefk1vWs --range 0-120 --out <OUT>/xVXEefk1vWs-0-120.json --compare docs/videos/drama-craft/reference-study-20261003.json
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --url m2qhz2n9618 --out <OUT>/m2qhz2n9618-full.json --compare docs/videos/drama-craft/reference-study-20261004-budaimiao.json
```

要看的：xVXEefk1vWs 對上 2026-10-03 那 46 個剪點裡的幾個、`high_motion_share` 是否仍遠低於 0.1；m2qhz2n9618 在 19.75–26 與 213.5–220.5 秒各量到幾個剪點（裁定各 8 個以上）、全片的 `high_motion_share`。數字寫成新的一份紀錄，再回去改 `drama-craft.md` 第八節。
