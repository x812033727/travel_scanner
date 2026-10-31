# 種田娶妻打天下：東西都在哪裡、從哪裡來

站主 2026-10-31：「劇情、分鏡、劇照那些的還有該紀錄的都要記錄起來，如果有其他對話才不用另外去下載跟交代，應該都要知道從那邊來；
如果需要備份也都要被分到同一個地方……不然第一季做完後過了半年要做第二季，東西都不見了？」

這一頁是這部劇的總索引。新的對話、換帳號、半年後開第二季，都從這裡開始：先看第 1 節找到東西，再照第 3 節把工作資料夾還原。
**雲端 session 的工作資料夾（`~/mokaair-work/videos`）在 session 結束時就沒了，不跨帳號；站台媒體庫是快取，會被清掉。**
所以每一樣「之後還要用、又重做不出一樣結果」的東西，不是在 repo 裡，就是在站主的 Google 雲端硬碟 `AI/備份/` 裡；兩邊都沒有的，第 2 節列出來。

## 1. 每一樣東西放哪裡

路徑相對於 repo 根目錄；`P` = `docs/videos/series-plans/zhong-tian-qu-qi`。

| 東西 | 位置 | 從哪來、誰改 |
| --- | --- | --- |
| 企劃：世界、人物、五季總綱、逐集細綱 | `P/setting.*`、`P/outline.*`、`P/season-01.json`～`season-05.json`（`.md` 由 `build.mjs` 產生）、`P/episodes.csv` | 2026-10-16 企劃包；改細綱要過 `P/validate.mjs` |
| 寫法規則 | `P/authoring.md`、`P/production/storyboard-rules.md` | 每一集都照它寫 |
| 每集的稿：brief、劇本、分鏡、`video.json`、疊字、八語配音稿 | `docs/videos/zhong-tian-qu-qi-eNNN/` | 第 1–42 集已寫；第 43–60 集見第 4 節 |
| 角色與場景的外貌、聲音、Ref2VA 參考圖對照 | `P/production/cast.json`、`P/production/refs.json` | 新角色登記在這裡，再同步到 `gen-dh.mjs`、`colab/ref2manifest.mjs`、`hailuo/dub-glossary.json` |
| 每鏡的首格與片段提示詞（鎖定稿） | `P/production/hailuo/ff-dh-eNNN.json`、`clips-dh-eNNN.json`（`gen-dh.mjs` 產生） | 改分鏡就重跑 `gen-dh.mjs`，雜湊會變 |
| 剪接表 | `P/production/hailuo/edit-dh-eNNN.json` | 每集剪完提交 |
| 劇照：定妝照、角度臉、場景圖 | `P/production/assets/refs-dh/`（`SHA256SUMS` 核對） | 第 31 集起的路線；第 1–30 集的海螺原圖網址在 `hailuo/refs-dh-urls.json`（海螺網址會失效，以 repo 裡的檔為準） |
| 配樂、季封面 | `P/production/assets/music/`、`assets/season1-thumb.png` | 見 `assets/README.md`；音效用 `hailuo/local/sfx-synth.sh` 重新合成 |
| 八語 YouTube 標題與說明 | `P/production/hailuo/youtube-locales/` | 每集上架前提交 |
| 配音的人名與用詞對照 | `P/production/hailuo/dub-glossary.json`、`dub-glossary-additions.<語言>.json` | 新角色要同步加 |
| Colab 三段式（路線 A）的腳本 | `P/production/colab/`、`colab/route-a/` | 第 33 集起；說明在 `colab/README.md` |
| 每一集**實際送出**的 manifest、提示詞（含重抽手改的）、每鏡用了哪一份草稿 | `P/production/colab/runs/eNNN/`（`takes.tsv`）、`colab/runs/README.md` | 從工作資料夾原樣複製；每集做完、每次重抽後都要再複製一次並提交 |
| 海螺網頁路線（第 1–30 集）的工具與坑 | `P/production/hailuo/README.md`、`.agents/skills/animation-production/references/hailuo-batch-driver.md` | |
| 做法與教訓 | `.agents/skills/minimax-h3-colab/references/lessons.md`、`three-stage.md` | 每次踩到新坑就寫進去 |
| 票與進度 | `tasks/open/`、`tasks/done/` 裡 `zhong-tian` 開頭的票 | `npm run tasks -- list` |
| 成片、字幕、配音、縮圖、上架說明 | 站主雲端硬碟 `AI/備份/<系列資料夾>/<集>/`（`G:\我的雲端硬碟\AI\備份\`） | 匯入站台後，主機 worker 在「可以上架」時自動複製；做法見 `docs/videos/BACKUP.md`，狀態看 `/admin/videos?tab=settings#video-backup-settings` |

## 2. 只存在工作資料夾、沒有備份的東西

| 東西 | 工作資料夾裡的位置 | 沒了會怎樣 |
| --- | --- | --- |
| 每鏡 1080p 成品片段（第 31 集起約 300 MB／集） | `zhong-tian-qu-qi-eNNN-dh/clips/sNN-t1.mp4` | 重剪、做 Shorts 或合集時要重跑三段（每集約 4–6 小時 G4）。`import --from` 只送整集成片，不送片段，所以 `AI/備份` 裡沒有它們 |
| 第一段草稿、第二段 refine 的中間檔 | `zhong-tian-qu-qi-eNNN-dh/colab/a/` | 不需要保留；成品片段在就好 |
| 錄音的原始 wav | `zhong-tian-qu-qi-eNNN-dh/audio/` | 可以照 `dub.*.json` 和 `video.json` 重錄，聲音會有些不同 |

逐鏡片段的備份還沒有做：要嘛讓 `import` 連片段一起送上主機，讓「完整」層級把 `clips/` 帶進 `AI/備份`；要嘛另開一條上傳。票
`tasks/open/2026-10-31-zhong-tian-clip-backup.md` 記著這件事。

## 3. 新的對話怎麼接手

1. 讀這一頁、`colab/README.md` 與 skill `minimax-h3-colab`（含 `references/lessons.md`）。
2. 還原工作資料夾：照 `assets/README.md` 的〈還原到工作資料夾〉把 `refs-dh/`、`music/`、封面複製過去、合成音效。
3. 拿 `npm run tasks -- list` 找這部劇沒人認領的票。每一集做到哪裡，看第 4 節的表和那一集的票。
4. 新畫的劇照、新的配樂、新角色：當天就加進 `assets/` 並重算 `SHA256SUMS`、登記進 `cast.json`，然後提交。每跑完一段、每次重抽，就把那一集的 `colab/a/` 文字檔複製進 `colab/runs/eNNN/`。只放在工作資料夾裡的東西，下一個對話拿不到。
5. 換帳號或新的雲端環境：Colab 權杖是環境的 secret `COLAB_CLI_TOKEN_JSON`（skill `minimax-h3-colab` 的〈配對〉），影片工具權杖每個 session 跟後台配對一次（`node tools/video/cli.mjs login`）。這兩樣是密碼，不進 repo。

## 4. 第一季每一集到哪裡了

| 集 | 稿 | 片段 | 成片匯入 | 配音 | 路線 |
| --- | --- | --- | --- | --- | --- |
| 1–30 | 有 | 海螺 | 看 `/admin/videos` | 看 `/admin/videos` | 海螺網頁（3D 國漫版） |
| 31–32 | 有 | Colab Ref2VA | 看 `/admin/videos` | 看 `/admin/videos` | 路線 B 小樣（另一個帳號的 session 做的） |
| 33 | 有 | 路線 A | 已匯入，等站主核准上架包 | 八語 | 路線 A（三段式） |
| 34–39 | 有 | 路線 A，製作中 | 製作中 | 製作中 | 路線 A |
| 40 | 有 | 未做（站主：做到第 39 集就停） | | | |
| 41–42 | 有（PR 待審） | 未做；第 42 集要先畫四張圖 | | | |
| 43–60 | 有（PR 待審；2026-10-31 寫完並做過連戲檢查） | 未做；先畫 25 張圖（`s01-e043-e060-registry.md`） | | | |

第 60 集收在禁軍包圍許家、老太監跪喊阿令「長公主殿下」，接第二季（`season-02.json`：黑鳳山）。站主 2026-10-31 定兩季照第 60 集統一：跪下的是真的老太監常公公（被相府押來作保），帶假禁軍的是他身邊的紫袍太監韓七；許硯手上拿的是配婚令。第二季的伏筆：12 條長線謎團
（`setting.json` 的 `mysteries`）裡第一季沒揭的，與 `season-01.json` 的 `end_state`。

這張表每做完一個階段就更新並提交。
