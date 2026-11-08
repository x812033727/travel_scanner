# 旁白解說系列的備份分支

適用：在雲端 session 製作的奇聞檔案局（`curio-*`）與原來如此事務所（`sothatswhy-*`）。容器隨時會被收掉，
本機檔案只有推到 GitHub 才算安全。主機上影片的雲端硬碟備份是另一條路線，見 [`../BACKUP.md`](../BACKUP.md)。
AI 劇的同類文件是 [`../drama/BACKUP-BRANCHES.md`](../drama/BACKUP-BRANCHES.md)（PR #2047），命名與核對方式跟它一致。

## 站主定下的原則

- **所有檔案都要備份，不挑檔**：「不是叫你都要備份到分支嗎?」「要把如果真的需要重製的檔案跟所有上傳的檔案都備份起來」
  （2026-11-07，原來如此 P07／P14 刪了沒備份的配音，差點整條重錄）；「備份＝所有上架用的檔案＋重製會用到的所有檔案」
  （2026-11-07，奇聞 W03 刪除時只推了文字檔，旁白原檔和配音沒留下）。
- **交給站主或送上後台的檔案，一律先進分支**（2026-11-07）。
- **之後才產生或補上的檔案也要補進同一條分支**（2026-11-07）。
- **沒備份完、沒核對完不准刪**（2026-11-07）。

## 分支怎麼命名

| 分支 | 放什麼 |
| --- | --- |
| `transfer/<slug>` | 一支影片的全部檔案，一支一條（例：`transfer/curio-h24`、`transfer/sothatswhy-p08-popcorn-pressure`） |
| `transfer/<系列>-shared` | 系列跨集共用、又不在 repo 裡的檔案（`transfer/curio-shared`、`transfer/sothatswhy-shared`） |

- 解說片的 slug 本身就是集數，不另外編號；重做的 `-v2` 是另一支片，用它自己的 slug。
- 每次備份在同一條分支上加一個 commit，只 fast-forward，**不強推**。舊版本留在歷史裡。
- 已有的分支保留不動，不搬也不刪：`claude/backup-sothatswhy-p02-p05`、`claude/backup-sothatswhy-p07-p14`、
  `claude/backup-sothatswhy-p08-popcorn-pressure`、奇聞 W03 在 `claude/eloquent-hypatia-fxsz7j` 的
  `docs/videos/curio-w03-garmin-smartphone-pivot/media/`。下一次備份起用新名字。

## 分支裡的路徑

路徑一律相對於 `~/mokaair-work/videos/`，不存含 session id 的絕對路徑（換 session 就還原不回去）：

| 路徑 | 內容 |
| --- | --- |
| `<slug>/…` | 整個工作目錄，原樣 |
| `_site/<slug>/…` | `review-files` 從站上抓回的檔案（含換版保留的 `retained/`） |
| `_repo/docs/videos/<slug>/…` | 備份當下 repo 裡這支的稿子快照（`video.json`、`script.md`、`i18n/` 等），還原時才知道是哪一版稿子做的 |
| `_scratchpad/<slug>/…` | 這支用到的 scratchpad 檔案（放大檢查的報告、還原清單、換版候選目錄） |
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
| 上傳包 | `upload/` 全部：成片、八語配音、字幕、說明、縮圖（含八語）、`metadata.json`、`UPLOAD.md` |
| 媒體帳本 | `media/`（`cache.json`、`jobs.json`、`ledger.json`）：重畫時吃快取不重付錢 |
| 站上檔案 | `_site/<slug>/`：送審過的每個附件，送審後用 `review-files --out` 抓回 |

**不放的**：密碼與權杖（`~/.mokaair/`）、可重裝的套件、別支片的檔案。

## 共用分支放什麼

不在 repo 裡、又跨集共用的檔案。已經進 repo 的（奇聞 Ada 設定圖、原來如此 `series-sheets/`）不重複放。

- 原來如此：系列配樂床 `sothatswhy-p02-bed.m4a`（sha256 `54169439…`）。
- 兩邊：片頭片尾素材包 `_branding/<hash>/`（`branding --pull` 抓得回來，但素材包會換版，留一份當時用的）。

## 什麼時候推

每過一關推一次：分鏡核准後、成片送審後、上架核准後、語言送審後；之後任何新產生或補上的檔案再推一次。
交給站主或送上後台的檔案，先推再交。

## 怎麼確認完整

1. **逐檔核對**：工作目錄每個檔（切塊的檔核對 `.SPLIT` 裡的 sha256）跟分支上的 blob 比，不符要是 0。
2. **涵蓋檢查**：工作目錄每個檔都在分支上，漏的要是 0。
3. **刪工作目錄之前**：另一個沒參與製作的代理只看 GitHub（`git ls-tree`、`.SPLIT`）再核對一次 1、2，並確認站主已決定成片、上架、
   語言三關。三件都成立才刪，而且只刪那一支。

工具在 [`backup/`](backup/)：`tobranch.sh` 推分支並逐檔核對，`coverage.sh` 做涵蓋檢查。
