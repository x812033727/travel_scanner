# 每部劇的紀錄、劇照與備份放哪裡

站主 2026-10-31（《種田娶妻打天下》第一季做到一半時）：「劇情、分鏡、劇照那些的還有該紀錄的都要記錄起來，如果有其他對話才不用
另外去下載跟交代，應該都要知道從那邊來；如果需要備份也都要被分到同一個地方。之後其他的劇本跟其他的不同的劇也是一樣，不然第一季做完後
過了半年要做第二季，東西都不見了？」

雲端 session 的工作資料夾（`VIDEO_WORKDIR`）在 session 結束時消失，也不跨帳號；站台媒體庫是快取，沒有工作
引用就清掉；海螺、Kling 的作品網址會失效。所以每部劇都照下面這個排法，任何一個新對話只要看 repo 就接得下去。

## 一部劇的固定排法

`docs/videos/series-plans/<series>/` 底下：

| 放什麼 | 位置 |
| --- | --- |
| 企劃、設定、每季細綱、寫法規則 | 資料夾根目錄（`setting.*`、`outline.*`、`season-NN.*`、`authoring.md`） |
| **總索引**：每一樣東西在哪、從哪來、誰改、備份在哪、每集做到哪裡、新對話怎麼接手 | `production/README.md` |
| 角色與場景（外貌、聲音、參考圖對照） | `production/cast.json`（或該劇的同等檔） |
| 劇照（定妝照、角度臉、場景圖）、配樂、季封面等重做不出一樣結果的檔 | `production/assets/`，附 `SHA256SUMS` 與一份 README 寫每個檔的來源（哪個 session、哪張票、哪個模型與設定） |
| 每鏡的提示詞清單、剪接表、上架用的多語標題說明 | `production/<路線>/` |

每一集的稿（brief、劇本、分鏡、`video.json`、疊字、配音稿）在 `docs/videos/<slug>/`。

## 規則

1. **當天提交。** 新畫的劇照、新生的配樂、新角色、新場景，做出來的那一天就放進 `production/assets/`、重算 `SHA256SUMS`、登記進
   `cast.json`、寫進 assets 的 README（來源）。只留在工作資料夾裡的東西，下一個對話拿不到。
2. **寫來源。** 每個檔都要寫得出從哪來：哪個 session 或票、什麼工具與設定、原始網址（會失效的網址只當參考，以 repo 裡的檔為準）。
3. **大檔走雲端硬碟備份。** 成片、字幕、配音、縮圖由主機 worker 在「可以上架」時複製到站主雲端硬碟 `AI/備份/<系列>/<集>/`
   （`docs/videos/BACKUP.md`）。所以每一集做完都要匯入站台，別只留在 session 裡。repo 不放影片。
   **一集重剪要的東西都要跟著上架包走**（站主 2026-11-05：「以後備份也要一起備份」；第 31–48 集的剪接紀錄與配樂曾經只在雲端
   工作資料夾，是事後一集一集從別的 session 撈回來的）。送上架包一律這樣：

   ```bash
   node tools/video/cli.mjs import --from <dir> --publish --clips <workdir>/<slug>-dh/clips --edit docs/videos/series-plans/<series>/production/<路線>/edit-dh-eNNN.json
   ```

   它從 `--clips` 的上一層帶走：片段 `clips/`、逐句配音 `audio/`、`audio-<語言>/`（與 `segments-v4/` 對時後的版本）、剪接紀錄
   `cut/final.log`、配音對時 `cut/dub-<語言>.log`、配樂 `music/`、首格 `first-frames/`，加上 `--edit` 的剪接設定。輸出有
   「build data not found」就是少了哪樣，**站主核准之前補齊**（核准後的包只收得進只給備份讀的檔，但要同一份 metadata.json）。
   雲端硬碟上的位置：`clips/`、`recordings/`、`recut/`、`keyframes/`（`docs/videos/BACKUP.md`〈匯入的影片〉第 3–6 步）。
   **系列共用的參考圖與音效**不屬於哪一集，上傳包不帶：新增或改了 `production/assets/refs*`、`_series/<series>/sfx` 之後，
   在掛著雲端硬碟的電腦跑 `node tools/video/import/series-backup.mjs <來源資料夾> "<雲端硬碟>/AI/備份/<分類>/<series>/_series"`
   （第 7 步）；雲端 session 掛不到雲端硬碟，就把圖提交進 `production/assets/`，並在交接寫明要同步。
   **放進 git 的紀錄檔要 `git add -f`**：根目錄 `.gitignore` 有 `*.log`，`final.log`、`dub-*.log` 一般 `git add` 會被默默略過
   （PR #2017 就這樣漏了，#2018 補），推完用 `git ls-tree -r --name-only HEAD | grep -c '\.log$'` 數一次。
4. **沒備份的要列出來，而且自己去數。** 別的 session 說「補好了」不算，打開分支或雲端硬碟數檔案（#2017 說放進了第 31–39 集的
   剪接紀錄，實際 0 個）。總索引要有一節列出「只在工作資料夾、沒有備份」的東西與沒了的代價，並為它開票，不要默默假設它還在。
5. **每集的進度寫在總索引的表裡**，做完一個階段就更新並提交；票記細節，表記全貌。
6. **留下實際送出的東西。** 生成工具會改版，重跑產生器得到的提示詞不一定是當時那一份；每一集實際送出的 manifest、提示詞（含重抽時手改的）與「每鏡用了哪個 take」都複製進 `production/<路線>/runs/eNNN/`（只收文字）。
7. **教訓寫進 skill**（例如 `minimax-h3-colab/references/lessons.md`），不寫在對話裡。

《種田娶妻打天下》的總索引是範例：`docs/videos/series-plans/zhong-tian-qu-qi/production/README.md`。
