# 雲端硬碟備份紀錄：題庫與各集總表

每一次把題庫、研究原稿或總表傳上雲端硬碟，都在這裡記一列：什麼時候、傳了什麼、從哪個 commit、放在哪裡、
`todrive.sh` 的核對結果。之後要重做一集、重開題庫或查以前的決定，先從這裡找到位置，再看
[`../explainer-series/CATALOG.md`](../explainer-series/CATALOG.md)（各集總表）。

雲端路徑都從 `AI/備份/` 算起（`videobackup:` remote 的起點），站主電腦上是 `G:\我的雲端硬碟\AI\備份\`。
怎麼傳、怎麼核對見 [`../AI-DRAMA-DRIVE.md`](../AI-DRAMA-DRIVE.md)。

## 放在哪裡

| 東西 | 原件 | 雲端備份 |
| --- | --- | --- |
| 奇聞檔案局題庫 | repo `docs/videos/history-curiosity/pool`（工具 `tools/video/curio/pool`） | `AI劇/奇聞檔案局/_共用/製作檔/題庫-奇聞檔案局-<日期>/`（`pool/`、`tools/`、`README.md` 寫 commit） |
| 原來如此事務所題庫 | repo `docs/videos/so-thats-why/pool`（工具 `tools/video/so-thats-why/pool`） | `AI劇/原來如此事務所/_共用/製作檔/題庫-原來如此事務所-<日期>/` |
| 題庫研究原稿（子代理的題案、審稿、下載的來源原檔、整合腳本） | 只在做研究的 session 的 scratchpad，session 結束就沒了 | 奇聞：`AI劇/奇聞檔案局/_共用/製作檔/題庫研究-<session>/`；原來如此：`AI劇/原來如此事務所/_共用/製作檔/題庫研究-<session>/`；名稱看不出系列的：`AI劇/奇聞檔案局/_共用/製作檔/題庫研究-雜項-<session>/` |
| 各集總表 | repo `docs/videos/explainer-series/CATALOG.md`、`catalog.json`，由 `catalog.py` 產生 | `AI劇/<系列>/_總表/`（唯讀副本，連同這份紀錄） |

repo 是題庫與總表的原件；雲端的快照是唯讀備份，不要在雲端改。要還原題庫：把快照的 `pool/` 放回原位，跑
`node tools/video/<curio|so-thats-why>/pool/cli.mjs check`。

## 紀錄

| 日期（UTC） | 內容 | 來源 | 雲端位置 | 核對 |
| --- | --- | --- | --- | --- |
| 2026-11-13 | 奇聞檔案局題庫快照（wave47 收尾後，入選 1,412） | main `f7090658`（PR #2090 合併；題庫內容與分支 commit `c3b2897d` 相同） | `AI劇/奇聞檔案局/_共用/製作檔/題庫-奇聞檔案局-20261113/` | `todrive: 155 files, 0 differences` |
| 2026-11-13 | 原來如此事務所題庫快照（第二十七輪後，入選 4,860、可成題長題 88） | 同上 | `AI劇/原來如此事務所/_共用/製作檔/題庫-原來如此事務所-20261113/` | `todrive: 1318 files, 0 differences` |
| 2026-11-13 | 奇聞題庫研究原稿（`curio26`–`curio48`、`curio38int` 整合腳本） | session `017c4Q` 的 scratchpad | `AI劇/奇聞檔案局/_共用/製作檔/題庫研究-session017c4Q/` | 傳送中 |
| 2026-11-13 | 原來如此題庫研究原稿（`stw6`–`stw27`、`stwNNint` 整合腳本，第 6–27 輪） | 同上 | `AI劇/原來如此事務所/_共用/製作檔/題庫研究-session017c4Q/` | 傳送中 |
| 2026-11-13 | 兩個題庫未標系列的子代理工作資料夾（`r*`、`v*`、`f*`、`*dl`、`*tools` 等） | 同上 | `AI劇/奇聞檔案局/_共用/製作檔/題庫研究-雜項-session017c4Q/` | 傳送中 |
| 2026-11-13 | 各集總表第一版（93 列）與這份紀錄 | `catalog.py` | `AI劇/奇聞檔案局/_總表/`、`AI劇/原來如此事務所/_總表/` | 傳送中 |

比上面更早的研究原稿（奇聞 `curio26` 以前、原來如此 `stw6` 以前）沒有傳過雲端：做那些的 scratchpad 已經收掉，
只剩 repo 裡的批次檔（`batches/`）、審稿紀錄（`reviews/`）與 `SOURCES.md`。

## 下一次要做的事

- 題庫每跑完一輪（或一波），在推 PR 的同時把快照與該輪的研究資料夾傳上去，在上面加一列。
- 有集數上架、重做或換配音後，重跑 `python3 docs/videos/ai-drama-drive/catalog.py`，把總表與雲端 `_總表/` 一起更新。
