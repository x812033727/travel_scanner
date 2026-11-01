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
| 成片、字幕、配音、縮圖、上架說明 | 站主雲端硬碟 `AI/備份/<系列資料夾>/<集>/`（`G:\我的雲端硬碟\AI\備份\`） | 上架包核准後，主機 worker 先從審核區把整包抓進 `video_work/<slug>/`，再照「完整」層級複製（`docs/videos/BACKUP.md`〈匯入的影片〉）。**這條要等票 `2026-10-31-zhong-tian-clip-backup` 的改動部署後才有**；之前匯入的影片從來沒進過 `AI/備份`（主機沒有東西把審核區的檔案搬進 `video_work`），審核區的 mp4 在上 YouTube 7 天後就刪掉。狀態看 `/admin/videos?tab=settings#video-backup-settings` |
| 每鏡 1080p 片段（第 31 集起約 300 MB／集） | `AI/備份/<系列資料夾>/<集>/clips/` | `import --publish` 自動帶 `<from>/clips`（或 `--clips <workdir>/zhong-tian-qu-qi-eNNN-dh/clips`），跟上架包一起送。**要在站主核准上架包之前送**：核准後的包加不進片段 |

## 2. 只存在工作資料夾、沒有備份的東西

| 東西 | 工作資料夾裡的位置 | 沒了會怎樣 |
| --- | --- | --- |
| 第一段草稿、第二段 refine 的中間檔 | `zhong-tian-qu-qi-eNNN-dh/colab/a/` | 不需要保留；成品片段在就好 |
| 錄音的原始 wav | `zhong-tian-qu-qi-eNNN-dh/audio/` | 可以照 `dub.*.json` 和 `video.json` 重錄，聲音會有些不同 |

逐鏡片段原本只在工作資料夾裡；站主 2026-10-31 選了讓 `import` 連片段一起送上主機（票 `2026-10-31-zhong-tian-clip-backup`）。第 31、32 集是另一個帳號的 session 做的，片段可能已經沒了。

## 3. 新的對話怎麼接手

1. 讀這一頁、`colab/README.md` 與 skill `minimax-h3-colab`（含 `references/lessons.md`）。
2. 還原工作資料夾：照 `assets/README.md` 的〈還原到工作資料夾〉把 `refs-dh/`、`music/`、封面複製過去、合成音效。
3. 拿 `npm run tasks -- list` 找這部劇沒人認領的票。每一集做到哪裡，看第 4 節的表和那一集的票。
4. 新畫的劇照、新的配樂、新角色：當天就加進 `assets/` 並重算 `SHA256SUMS`、登記進 `cast.json`，然後提交。每跑完一段、每次重抽，就把那一集的 `colab/a/` 文字檔複製進 `colab/runs/eNNN/`。只放在工作資料夾裡的東西，下一個對話拿不到。
5. **上架的順序不能換**（2026-11-01 第 32、34 集踩到）：成片核准 → 站主在語言面板勾語言 → `import --from <dir> --languages` 送語言批次 → 站主核准語言 →
   `import --from <dir> --publish --clips <workdir>/zhong-tian-qu-qi-eNNN-dh/clips` 送上架包 → 站主核准。先送上架包的話，之後 `--languages` 會拒絕，
   影片就既不能「可以上架」、也進不了雲端備份（主機只備份已上 YouTube 或可以上架的影片：要有核准的上架包、語言已決定、勾的語言都不在製作中）。
   第 32、34 集就卡在這裡；修法（票 `2026-11-01-import-publish-sends-an-upload-package`）：`import --languages --force` 補送語言批次，站主核准後再送一次 `--publish --clips …`，站主再核准。現在 `--publish` 會擋住反過來的順序。
6. **雲端硬碟的位置**：這部劇沒有設系列 slug，所以每集在 `AI/備份/drama/zhong-tian-qu-qi-eNNN/`（跟第 1–30 集的合集同一個 `drama` 資料夾），片段在其中的 `clips/`。
   備份狀態看 `/admin/videos?tab=settings#video-backup-settings`。
7. **工作資料夾每個 session 各一份**：另一個 session 說的 `~/mokaair-work/videos/...` 是它自己容器裡的，這邊讀不到。要交接影片檔就推一條暫存分支
   （`transfer/...`，例如 2026-11-01 的 `transfer/zt-e031-e032-media`），對方 `git archive` 解開放回原本的名字；交接完分支可以刪。
   能送上站台的（成片、片段）優先直接用 `import` 送，不用搬檔。
8. **兩個 session 不要畫同一張圖**：畫參考圖之前先看 repo 的 `assets/refs-dh/` 與票有沒有人在畫。已經被某一集用掉的圖（例如第 42 集用了另一個 session
   畫的許大郎、周員外、州城客棧、貢院）後面的集數就得沿用那一張，另外畫的版本作廢。
9. 換帳號或新的雲端環境：Colab 權杖是環境的 secret `COLAB_CLI_TOKEN_JSON`（skill `minimax-h3-colab` 的〈配對〉），影片工具權杖每個 session 跟後台配對一次（`node tools/video/cli.mjs login`）。這兩樣是密碼，不進 repo。

## 4. 第一季每一集到哪裡了

| 集 | 稿 | 片段 | 成片匯入 | 配音 | 路線 |
| --- | --- | --- | --- | --- | --- |
| 1–30 | 有 | 海螺 | 看 `/admin/videos` | 看 `/admin/videos` | 海螺網頁（3D 國漫版） |
| 31–32 | 有 | Colab Ref2VA（工作資料夾從 `transfer/zt-e031-e032-media` 取回；紀錄在 `colab/runs/e031`、`e032`） | 2026-11-01 已備份到 `AI/備份/drama/zhong-tian-qu-qi-e031/`、`e032/`（含片段 47、44 段；第 32 集先送上架包，用 `--languages --force` 補救） | 八語 | 路線 B 小樣（另一個帳號的 session 做的） |
| 33 | 有 | 路線 A | 上架包含 41 段片段已核准；2026-11-01 已備份到 `AI/備份/drama/zhong-tian-qu-qi-e033/`（縮圖漏掉，票 `2026-11-01-video-backup-an-imported-video-s`） | 八語 | 路線 A（三段式） |
| 34 | 有 | 路線 A | 2026-11-01 已備份到 `AI/備份/drama/zhong-tian-qu-qi-e034/`（含 41 段片段；用 `--languages --force` 補救） | 八語 | 路線 A |
| 35 | 有 | 路線 A | 2026-11-01 已備份到 `AI/備份/drama/zhong-tian-qu-qi-e035/`（含 41 段片段） | 八語 | 路線 A |
| 36–39 | 有 | 路線 A（第 36、37 集火把重拍；第 38、39 集重抽見 `colab/runs/eNNN/takes.tsv`） | 已匯入，等站主審成片 | 八語 | 路線 A |
| 40 | 有 | 路線 A（RunPod；片段在本機 `runpod/a/picked/final`，沒有進 `colab/runs/`） | 已匯入，等站主審成片 | 未做 | 路線 A（RunPod）；首次走完「RunPod 片段→錄音→剪接→匯入」 |
| 41–42 | 有（PR 待審） | 未做；第 42 集要先畫四張圖 | | | |
| 43 | 有 | 路線 A（RunPod，雲端 session；重抽 15 鏡，紀錄在 `colab/runs/e043/`，`takes.tsv`、`review-st1.md`）；US$18.26 | 2026-11-01 已匯入，等站主審成片 | 未做 | 路線 A（RunPod） |
| 44–60 | 有（2026-10-31 寫完並做過連戲檢查） | 未做；參照圖都在 repo，配角定妝照（巡兵、衙役、魏管家、報榜人、通判、知府夫人、信差、少年、禁軍統領、書吏妻）第 44 集開機時一起畫 | | | |

第 60 集收在禁軍包圍許家、老太監跪喊阿令「長公主殿下」，接第二季（`season-02.json`：黑鳳山）。站主 2026-10-31 定兩季照第 60 集統一：跪下的是真的老太監常公公（被相府押來作保），帶假禁軍的是他身邊的紫袍太監韓七；許硯手上拿的是配婚令。第二季的伏筆：12 條長線謎團
（`setting.json` 的 `mysteries`）裡第一季沒揭的，與 `season-01.json` 的 `end_state`。

這張表每做完一個階段就更新並提交。
