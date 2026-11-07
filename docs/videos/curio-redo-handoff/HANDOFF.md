# 奇聞檔案局重做：交接（2026-11-07）

前一個對話負責 W03、B02 和 B03，其他 20 支交給新的對話做。
這個資料夾和同一分支上的 `docs/videos/<slug>/` 就是要接手的全部東西。

分支是 `claude/eloquent-hypatia-fxsz7j`。它以 main 為基底，另外加了：
- W03 的完整媒體備份：`docs/videos/curio-w03-garmin-smartphone-pivot/media/`，是備份應該長什麼樣子的範例；
- 本次交接的檔案。

## 要做的 20 支（`queue.txt`）

| 影片 | 狀態 | 新稿在哪 |
|---|---|---|
| curio-b01 | 新稿的 script 與 look 已在 11-07 核准；舊版成片在 11-02 核准過。新稿的關鍵影格、旁白和後面的流程都還沒做 | `docs/videos/curio-b01/` |
| curio-h24 | 新稿寫好，還沒開始製作 | `docs/videos/curio-h24/` |
| curio-s10-v2 … s40-v2（14 支） | 新稿寫好，還沒開始製作 | `docs/videos/<slug>/` |
| curio-s42、curio-w01-dolby-licensing、curio-w02-michelin-guide-stars | 新稿寫好，還沒開始製作。這三支的資料夾來自還沒合併的 PR #2016，所以新稿放在 `production/<slug>/`；#2016 合併後再蓋回 `docs/videos/<slug>/` | `production/<slug>/` |

各檔案的用途：
- `docs/videos/<slug>/video.json`：生產用的定稿，lint 跑過。
- `docs/videos/<slug>/script.md`：從 video.json 產生的稿子。
- `drafts/<slug>/`：撰稿時的人看版本，包括 script.md 草稿、照黑貓 10 步的 structure-map.md、和 changes.md。changes.md 記錄改了什麼、【待查】、建議刪的景、要加進 lexicon 的詞。
- `docs/videos/lexicon.json`：已補上這批稿子要用的英文原名，值是 null，表示照英文念。

## 開工前一定要先處理（程式還沒進 main）

新稿用到兩個還沒合併的功能。沒有它們，lint、keyframes 和 assemble 會失敗：

1. **PR #2016**（`claude/curio-pictured-cast`）：讓只有旁白的解說片可以列只畫不說話的角色 Ada，用設定圖固定她的長相。
2. **分支 `claude/curio-beat-motion`**（還沒開 PR）：讓 video.json 可以用 `still_motion: "beat"`（插圖停住再推近、平移、拉遠，換圖淡入淡出）和 `pauses`（縮短句間停頓）。6 支稿子用了 still_motion。

請先問站主要不要合併這兩個，或在本機合併後再做。
前一個對話是在本機把 main、beat-motion 和 pictured-cast 合在一起生產的，那份合併沒有推上去。
片頭在前（`defaultIntroAt`）已經由 #2036 進 main，不用再改。

## 站主定下的規則

全部寫在 `RULES.md`，一定要先讀。重點：
- 用黑貓研究院的 10 步結構（`HEIMAO-STRUCTURE.md`），一開場不放濃縮劇情。
- 片頭動畫先播，接著是本片，片尾不變。
- 畫面要跟旁白對上、梗要接得上。不用卡片，畫面上完全沒有字。
- 不畫貓。英文名照原文念。1956 年後還在世或過世的真人不畫成人像。
- 會長字的東西照 B 方案畫：
  - 螢幕只能有一條藍色路線、一個白色轉彎箭頭或一個紅色定位釘；手錶只能有一顆紅心。
  - 報告畫成一本很厚、素色封面的書；箱子畫成素灰色。
  - 數字改用感受來畫：鼓或扁的錢包、升起或洩氣的氣球、幼苗、飛鏢靶。
- 整個系列固定用同一張 Ada 設定圖：W03 的候選 E，檔案在 `ada-sheet/`（B03 工作資料夾的 characters/）。
  - 站主說不用每支片都去按 look 關卡，可以用 `approve --gate look --note "owner 2026-11-07: Ada sheet is fixed for the series (W03 sheet E); approve without per-video clicks"`。
- 品質優先，長度可以依內容拉長或縮短：
  - S31-v2 的目標是 15–16 分鐘；
  - S14-v2 照時間順序，把《五輪書》放在前面。
- 一次最多做兩支。每支的流程：分鏡審查 → 成片審查 → 上架包和八語送審 → 站主確認完成 → **備份到分支** → 刪掉工作資料夾 → 下一支。

## 製作流程（前一個對話實際的做法）

- 生產腳本在 `scripts/`。上面的路徑是前一台機器的，要改成你自己的：
  - `prod-runner.sh`：同時最多跑兩支，讀 `prod-queue.txt`；
  - `prod-one.sh`：先跑 `keyframes --takes 3`，再跑 `tts`；
  - `retake.sh`：用新種子重畫沒過的景（`--seed-offset 3`），已經通過的景會保留。
- 環境變數：`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 PLAYWRIGHT_BROWSERS_PATH=<pw>`；工作資料夾是 `/root/mokaair-work/videos/<slug>`。
- 背景工作在對話閒置時會被砍掉，要一直留在對話裡盯著。
- **關鍵影格**：第一輪大約有三到四成的景過不了審圖，正常。處理順序是：
  1. 先用新種子重畫一次；
  2. 還沒過的，照審圖意見改提示詞。B03 的經驗：
     - 硬幣改寫成 `smooth blank gold discs`，避免被畫上錢號；
     - 小豬撲滿和鐵桶會被畫上臉，改成灰色錢箱或玻璃罐；
     - 無人景出現人或船，改成澡盆裡的紙船；
     - Ada 被畫成全身時，鏡頭不要用 tilt 或 pull out，改成 push in 或 drift，道具最多一個；
  3. 改完一定要跑 lint，例如同一種運鏡不能連續三景。
- 全部景都過了以後，交給一個**獨立代理**逐張放大檢查（找字、找臉、找人），沒問題才 `review-push --gate storyboard`。

## 一定要記得的教訓（W03 踩過的）

1. **刪工作資料夾之前**，要把上架用的檔案和重製會用到的所有檔案推到分支，用 `git ls-tree` 逐檔對指紋，確認後才刪。範圍包括：
   - 每句錄音（主要是八語配音的逐句錄音；W03 的配音逐句錄音存成無損 FLAC，見 `media/dub-lines/README.md`）；
   - 每景插圖和 manifest、配音、字幕、時間軸；
   - approvals、languages、checks.json、branding.json；
   - 縮圖（含八語縮圖）、成片（超過 100 MB 切成約 90 MB 一段，附 sha256）。
   - 另外，語言關卡（languages）要先送審，才能刪。
2. **上架包自檢**一律用 `package/check.mjs` 的 `readPackageReport(workdir)`，也就是 review-push 用的那一支。不要自己呼叫 `checkPackage`：它的 brandingMatches 預設是 true，會漏掉 checks.json 遺失的問題。後台就是因此出現「upload package does not match the selected and applied branding」。
3. **配音的片頭片尾**要讓 `dub` 工具自己加（它需要 checks.json 的 branding 和 speech_hash），不要手動接進 `upload/dubs`。languages 關卡讀的是 `dubs/<locale>.m4a`。
4. **送審之後**，用 `review-files --slug S --dry-run` 把網站上每個 `dub_*`、`thumbnail_*`、`captions_*` 的 sha 跟本機檔案逐一比對。
5. **各語說明**要用 `composeMetadata` 加上 `presentationTimeline`（片頭 150 格、片尾 630 格，intro_at_frame 0）產生，才會有章節和來源。各語字幕要跟著片頭往後移 5 秒。
6. 後台「上架包」頁面顯示的是**最近一次已核准**的上架送審。新版要等站主核准後才會出現在那裡。

## 前一台機器上沒有備份的東西

前一台機器上，這 20 支還留有舊版（重做前）的工作資料夾：
- B01、H24、S27、S31、S42、W01、W02 各有舊的成片、旁白和插圖，每支 0.1–2.7 GB；
- 其他各支只有幾百 KB。

這些不屬於新稿，又太大推不上分支，所以**沒有備份**。審核網站上還留有各支目前的審核附件，可以用 review-files 取回。
