---
id: 2026-11-13-explainer-pool-drive-categories
title: 奇聞與原來如此：題庫與雲端硬碟分類架構、雙資料夾整併、總表同步與下一輪擴充
status: done
priority: P1
area: docs
owner: antigravity-pool-expansion-20261113
claimed_at: 2026-11-13T17:20:37Z
created_at: 2026-11-13T17:20:03Z
completed_at: 2026-11-13T21:54:23Z
branch: claude/pool-expansion-20261113
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - tools/video/curio/pool
  - tools/video/so-thats-why/pool
  - docs/videos/AI-DRAMA-DRIVE.md
  - docs/videos/BACKUP.md
  - docs/videos/ai-drama-drive
  - docs/videos/explainer-series
  - docs/videos/rules-sync
  - apps/api/app/video_backup/target.py
  - apps/api/tests/test_video_backup.py
---

# 奇聞與原來如此：題庫與雲端硬碟分類架構、雙資料夾整併、總表同步與下一輪擴充

## Why

兩個解說系列的成題與集數持續成長（奇聞檔案局入選 1,472、雲端 56 個集數資料夾；原來如此事務所入選 5,013、可成題長題 99 組、雲端 29 個資料夾且 12 集出現 `P07` 與 `第007集` 雙資料夾分家），全部擠在 `AI劇/<系列>/` 第一層難以管理，且原來如此素材池 `domain` 累積超過 200 種自由文字、題案無統一分類。

站主 2026-11-13 核定：
1. **奇聞檔案局分 9 類（字母代號-中文名）**：`H-歷史懸案`、`S-歷史人物與名場面`、`M-奇異現象與自然`、`F-童話神話與怪談原版`、`L-都市傳說與消失地名`、`G-靈異與超自然公案`、`P-預言與末日`、`U-外星太空與未知訊號`、`W-商業與品牌奇聞`（`B01–B03` 歸入 `W`）。
2. **原來如此事務所分 7 類（純中文名稱）**：`物理化學與日常材料`、`生物動物與植物`、`地球天氣與太空`、`數位科技與通訊工程`、`飲食與廚房科學`、`人體感官與日常行為`、`建築交通與商業制度`。
3. **原來如此雲端雙資料夾整併**：將 `P06～P29` 與 `第006集～第029集` 無損整併為各分類下的 `P06～P29`，並修正 `apps/api/app/video_backup/target.py` 讓主機自動備份與 `moved_from` 對齊新路徑，不再分家。
4. **PR 集中**：將 PR #2092（雲端備份紀錄與各集總表）併入同一個 PR #2093 一次改完並關閉 #2092；分類與搬移驗證完成後，接著跑下一輪同步擴充（奇聞 `wave51` ＋ 原來如此第 31 輪 `wave81`）。

## Definition of done

- [x] 奇聞檔案局與原來如此事務所素材池的所有單核與題案皆具備正規分類（9 類／7 類，不改動歷史 `raw_records`），檢視頁（`QUESTIONS.md`、`THEMES.md`、`index.html`、`PRODUCIBLE.html`）支援依分類瀏覽與篩選。
- [x] `apps/api/app/video_backup/target.py`、`docs/videos/rules-sync/sync.mjs`、`docs/videos/ai-drama-drive/catalog.py`、`BACKUP.md`、`AI-DRAMA-DRIVE.md` 對齊 `AI劇/<系列>/<分類>/<代碼>/`，且既有備份路徑透過 `moved_from` 自動指向新分類資料夾。
- [x] 雲端硬碟 `AI/備份/AI劇/奇聞檔案局/`（56 集）與 `AI/備份/AI劇/原來如此事務所/`（29 個資料夾整併為 17 集 `Pxx`）完成無損分類搬移；重產 `CATALOG.md` / `catalog.json` 並更新雲端 `_總表/` 與題庫快照，核對 0 差異。
- [x] PR #2092 併入 PR #2093 並說明關閉。
- [x] 完成下一輪同步擴充（奇聞 `wave51` ＋ 原來如此第 31 輪 `wave81`），通過雙池 `build`/`check`/`index`/單元測試與後端 `pytest`、`ruff`、`mypy`、`check:tasks`。

## Steps

- [x] 併入 `origin/main` 與 PR #2092 變更至 `claude/pool-expansion-20261113`。
- [x] 建立雙系列分類對照與工具更新（`tools/video/curio/pool`、`tools/video/so-thats-why/pool`、兩邊 `themes.json` 與輸出視圖）。
- [x] 更新雲端備份與同步路徑（`target.py`、`test_video_backup.py`、`sync.mjs`、`sync.test.mjs`、`catalog.py`、`AI-DRAMA-DRIVE.md`、`BACKUP.md`）。
- [x] 在 Google Drive 無損建立分類資料夾、整併 `Pxx`／`第0xx集`、搬移全部集數，重跑總表與快照備份。
- [x] 執行下一輪雙池同步擴充（奇聞 `wave51` ＋ 原來如此第 31 輪 `wave81`）並完成全套驗證。

## How to verify

- `node tools/video/curio/pool/cli.mjs check && node --test tools/video/curio/pool/pool.test.mjs`（PASS，24 項通過，雙次 `index` 第二次 `writes: 0`）
- `node tools/video/so-thats-why/pool/cli.mjs check && node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（PASS，34 項通過，雙次 `index` 第二次 `writes: 0`）
- `node --test docs/videos/rules-sync/sync.test.mjs`（9 項通過）
- `cd apps/api && uv run ruff check app/video_backup tests/test_video_backup.py && uv run mypy app/video_backup tests/test_video_backup.py && uv run pytest tests/test_video_backup.py`（63 項通過）
- `npm run check:tasks`

## Notes

- 以 `--force` 認領：`2026-10-23-video-backup-when-ready-to-upload` 與 `2026-11-02-video-backup-shorts-sent-by-hand` 的程式碼早已合併，僅留部署後人工核對項目，無開啟分支或 PR。
- 第四輪雙池同步擴充（2026-11-13）：
  - **奇聞檔案局 `wave51`**：4 組研究者（`ZG1–ZG4`）＋ 4 組非作者獨立覆核（`R511–R514`），新增 20 題入選（`N5701–N5765`，首度開收 `W-商業與品牌奇聞` 5 題非鎖定新題，並補強 `U`、`P`、`G`、`F`、`L`），入選總數 `1,472 → 1,492`。
  - **原來如此事務所第 31 輪（`wave81`）**：4 組研究者（`F152–F155`）＋ 4 組非作者獨立覆核（`V172–V175`），補強核心與長題數最少之四類，新增 56 筆核心（`5,013 → 5,069`）與 4 組可成題長題 `G641–G644`（`99 → 103` 組，同步登記至 `apps/api/app/video_backup/target.py`）。
  - 搬移期間並行上傳完成的 `S10/製作檔/curio-s10-v2` 已無損歸入 `S-歷史人物與名場面/S10/製作檔/curio-s10-v2-20261113`，並重產 `CATALOG.md` / `catalog.json`、同步備份雙池快照與 `session240faf7e` 研究審稿原稿至 Google Drive。
