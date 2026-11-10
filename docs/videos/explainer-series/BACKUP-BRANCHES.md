# 旁白解說系列的備份分支

適用：在雲端 session 製作的奇聞檔案局（`curio-*`）與原來如此事務所（`sothatswhy-*`）。容器隨時會被收掉，
本機檔案只有推到 GitHub 才算安全。主機上影片的雲端硬碟備份是另一條路線，見 [`../BACKUP.md`](../BACKUP.md)。
AI 劇的同類文件是 [`../drama/BACKUP-BRANCHES.md`](../drama/BACKUP-BRANCHES.md)（PR #2047），命名與核對方式跟它一致。

## 站主定下的原則

- **所有檔案都要備份，不挑檔**：「不是叫你都要備份到分支嗎?」「要把如果真的需要重製的檔案跟所有上傳的檔案都備份起來」
  （2026-11-07，原來如此 P07／P14 刪了沒備份的配音，差點整條重錄）；「備份＝所有上架用的檔案＋重製會用到的所有檔案」
  （2026-11-07，奇聞 W03 刪除時只推了文字檔，旁白原檔和配音沒留下）。
- **重製時什麼都不用重做**：「備份要之後如果要重製就可以不用重新做的都要備份到」；「八國跟繁體中文 縮圖 語音 字幕 敘述都要」
  （2026-11-08）。判斷標準是「這個檔不見了，重製時要不要再花錢、再跑一次、再審一次」：要的就放。工作目錄以外的也算
  （改過還沒進 main 的稿子、scratchpad 的腳本與紀錄、片頭片尾素材包、當時的工具版本）。
- **交給站主或送上後台的檔案，一律先進分支**（2026-11-07）。
- **之後才產生或補上的檔案也要補進同一條分支**（2026-11-07）。
- **沒備份完、沒核對完不准刪**（2026-11-07）。

## 備份推到哪個 repo（2026-11-09 起）

主 repo `travel_scanner` 已接近 GitHub 的容量上限（推送時出現 `Repository is approaching its size quota`），
站主 2026-11-09 決定每個系列各開一個備份 repo，分支命名與核對方式照舊，只是推到下面的 repo：

| 系列 | 備份 repo |
| --- | --- |
| 奇聞檔案局（`curio-*`） | `x812033727/mokaair-video-backup` |
| 原來如此事務所（`sothatswhy-*`） | `x812033727/mokaair-video-backup-sothatswhy` |
| 種田（`zt-*`） | `x812033727/drama-backup-zt` |
| 祖媽（`tn-*`） | `x812033727/drama-backup-tn` |

- **不要再把 `transfer/*` 推到 `travel_scanner`。** 工具推到「執行時所在 checkout 的 `origin`」，所以在備份 repo 的 clone 裡執行
  （見 [`backup/README.md`](backup/README.md)）。雲端 session 要先把那個 repo 加進 session（推送權限）再 clone。
- 已經在 `travel_scanner` 上的 `transfer/*` 分支，用逐個 commit 推送的方式原樣搬到對應的備份 repo（commit 編號相同，
  兩邊分支頭一致就是內容一致；`tobranch.sh` 每個 commit 不超過約 1.5 GB，所以逐個推不會碰到 2 GB 的單次上限）。
  搬完、核對一致之後，要不要從 `travel_scanner` 刪掉由站主決定。

也可以不 clone：兩支工具用環境變數 `BACKUP_REMOTE` 指定 repo（remote 名稱或網址，不設就是 `origin`）：

```bash
git remote add backup-sothatswhy https://github.com/x812033727/mokaair-video-backup-sothatswhy.git   # 一次
BACKUP_REMOTE=backup-sothatswhy docs/videos/explainer-series/backup/tobranch.sh transfer/<slug> ~/mokaair-work/videos/<slug> <slug> "<slug>: <關卡>"
BACKUP_REMOTE=backup-sothatswhy docs/videos/explainer-series/backup/coverage.sh transfer/<slug> ~/mokaair-work/videos/<slug> <slug>
```

## 分支怎麼命名

| 分支 | 放什麼 |
| --- | --- |
| `transfer/<slug>` | 一支影片的全部檔案，一支一條（例：`transfer/curio-h24`、`transfer/sothatswhy-p08-popcorn-pressure`） |
| `transfer/<系列>-shared` | 系列跨集共用、又不在 repo 裡的檔案（`transfer/curio-shared`、`transfer/sothatswhy-shared`） |

- 解說片的 slug 本身就是集數，不另外編號；重做的 `-v2` 是另一支片，用它自己的 slug。
- 每次備份在同一條分支上加一個 commit，只 fast-forward，**不強推**。舊版本留在歷史裡。
- 已有的分支保留不動，不搬也不刪：`claude/backup-sothatswhy-p02-p05`、`claude/backup-sothatswhy-p07-p14`、
  `claude/backup-sothatswhy-p08-popcorn-pressure`、`claude/backup-sothatswhy-p11-old-battery`、
  `claude/backup-sothatswhy-p15-salty-sea`、`claude/backup-sothatswhy-p23-quake-alert`、奇聞 W03 在
  `claude/eloquent-hypatia-fxsz7j` 的 `docs/videos/curio-w03-garmin-smartphone-pivot/media/`。
- 已經在舊名字上推過的那一集，做完前繼續推同一條，免得一集拆在兩條分支（原來如此 P11）。之後新開的集數用 `transfer/<slug>`。

## 分支裡的路徑

路徑一律相對於 `~/mokaair-work/videos/`，不存含 session id 的絕對路徑（換 session 就還原不回去）：

| 路徑 | 內容 |
| --- | --- |
| `<slug>/…` | 整個工作目錄，原樣 |
| `_site/<slug>/…` | `review-files` 從站上抓回的檔案（含換版保留的 `retained/`） |
| `_repo/docs/videos/<slug>/…` | 實際拿來做這支的那份 checkout 裡、這支的稿子（**含未提交的修改**；`video.json`、`script.md`、`i18n/`、`claims.md`、`panel/` 等）。不是 main 上的版本 |
| `_repo/BASE` | 做這支時工具所在 checkout 的 commit（`git rev-parse HEAD`），以及那份 checkout 有沒有未提交的修改 |
| `_scratchpad/<slug>/…` | 這支用到的 scratchpad 檔案：自己寫的腳本（`.py`、`.sh`、`.mjs`）、改稿前的備份、放大檢查的報告與裁圖、import 清單、執行紀錄（`*.log`）、換版候選目錄 |
| `README-backup.md` | 這一版放了什麼、沒放什麼（以及在哪裡）、怎麼還原、檔案數與大小 |

超過 95 MB 的檔案切成 90 MiB 的 `X.part00`、`X.part01`…，旁邊放 `X.SPLIT`：原檔 sha256 與還原指令
`cat X.part* > X`。

## 分集分支放什麼

整個工作目錄不挑檔，下面是「至少要有」的檢查清單，少一樣就不算完整：

| 類別 | 內容 |
| --- | --- |
| 稿子與時間軸 | `timeline.json`、`state.json`、`approvals.json`、`review/` 全部（`check.json`、`check-flags.json`、`qa.json`） |
| 旁白 | `narration.wav`、`audio/` 每一句與 `cache.json`、`speech-journal/` |
| 設定圖 | `characters/` 全部（含沒選中的候選與 `choice.json`） |
| 插圖 | `keyframes/` 每一張（**含沒選中的 take**、`-import-` 的圖）、`manifest.json`、聯絡表、`zoom/` |
| 合成 | `frames/`、`clips/`、`segments/`、`build/`（含 `body.mp4`）、`music/`、`branding.json`、`checks.json`、`watermark.json`、`final.mp4` |
| 字幕 | `captions/` 全部語言 |
| 配音 | `dubs/<locale>/` 逐句錄音、時間軸、`body.m4a`、`dubs/<locale>.m4a`；逐句錄音存無損（W03 用 FLAC，見其 `media/dub-lines/README.md`） |
| 上傳包 | `upload/` 全部：成片、`metadata.json`、`UPLOAD.md`，以及下面九語表的每一格 |
| 媒體帳本 | `media/`（`cache.json`、`jobs.json`、`ledger.json`）：重畫時吃快取不重付錢 |
| 站上檔案 | `_site/<slug>/`：送審過的每個附件，送審後用 `review-files --out` 抓回 |

### 九種語言，每一格都要有

繁體中文加八語（en、ja、ko、es、pt、id、th、vi），每種語言四樣都要在分支上，缺一格就不算完整：

| | 縮圖 | 語音 | 字幕 | 敘述（標題、說明、標籤、章節） |
| --- | --- | --- | --- | --- |
| 繁體中文 | `upload/` 的縮圖、`build/` 的縮圖 | `narration.wav`、`audio/` 逐句、`speech-journal/` | `captions/zh-TW` | `video.json` 的標題說明、`upload/` 的說明檔 |
| 八語各一 | `upload/` 的 `thumbnail_<locale>`（`render --thumbnails-only` 的結果） | `dubs/<locale>/` 逐句（無損）與時間軸、`dubs/<locale>.m4a` | `captions/<locale>` | `i18n/<locale>.json`（在 `_repo/` 快照裡）、`upload/` 的各語說明 |

送上後台的那一份（`_site/<slug>/` 的 `dub_*`、`thumbnail_*`、`captions_*`）也要在，跟本機的 sha 對得上。

**不放的**：`LEASE*`（工具的鎖檔紀錄，重製用不到）、密碼與權杖（`~/.mokaair/`）、可重裝的套件、別支片的檔案。

## 共用分支放什麼

不在 main 裡、又跨集共用的檔案。已經進 main 的不重複放。

- 兩邊：做重製時那份 checkout 的未提交修改（`_repo/BASE` 加 `_repo/worktree.patch`，`git diff --binary HEAD` 加上新增的檔），
  以及改過的稿子原樣（`_repo/docs/videos/…`）。還沒開工的集數也在這裡，改稿的功夫才不會白費。
- 奇聞：Ada 設定圖 `curio-redo-handoff/ada-sheet/`（目前只在分支 `claude/eloquent-hypatia-fxsz7j`，沒進 main）、重做的決定紀錄。

- 原來如此：系列配樂床兩條都放，README 註明哪幾集用哪一條：
  - `sothatswhy-bed-r2.m4a`（sha256 `9bb4ba6fd16feb4a7f352144b2d89e9648acbbbbaa2173c27a7eefbdb70f28c6`，全長 863.75 s；P15、P23、P11 用）與它的付費原檔；
  - `sothatswhy-p02-bed.m4a`（sha256 `54169439…`，P02 等早期集數用）。原檔目前兩邊的備份都找不到，找到再補。
- 兩邊：片頭片尾素材包 `_branding/<hash>/`（`branding --pull` 抓得回來，但素材包會換版，留一份當時用的）。

## 什麼時候推

每過一關推一次：分鏡核准後、成片送審後、上架核准後、語言送審後；之後任何新產生或補上的檔案再推一次。
交給站主或送上後台的檔案，先推再交；指令要寫成 `備份 && review-push`，備份失敗就不送（不能用 `;`）。

## 怎麼確認完整

0. **九語清單**：照上面的九語表逐格打勾，缺的補做或補抓（`review-files --out`）再推。
1. **逐檔核對**：工作目錄每個檔（切塊的檔核對 `.SPLIT` 裡的 sha256）跟分支上的 blob 比，不符要是 0。
2. **涵蓋檢查**：工作目錄每個檔都在分支上，漏的要是 0。
3. **刪工作目錄之前**：另一個沒參與製作的代理只看 GitHub（`git ls-tree`、`.SPLIT`）再核對一次 1、2，並確認站主已決定成片、上架、
   語言三關。三件都成立才刪，而且只刪那一支。

工具在 [`backup/`](backup/)：`tobranch.sh` 推分支並逐檔核對（GitHub 一次推送不能超過 2 GB，所以每約 1.5 GB 分一個
commit 推），`coverage.sh` 做涵蓋檢查。
