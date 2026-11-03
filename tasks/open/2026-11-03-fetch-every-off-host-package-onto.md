---
id: 2026-11-03-fetch-every-off-host-package-onto
title: Fetch every off-host package onto the host before upload; prune review mp4s only after the Drive backup
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-backup-rules
claimed_at: 2026-11-03T00:58:18Z
created_at: 2026-11-03T00:57:01Z
completed_at:
branch: claude/video-backup-review-push
depends_on: []
scope:
  - apps/api/app/video_backup/admin_status.py
  - apps/api/app/video_backup/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_backup.py
  - apps/api/tests/test_video_reviews.py
  - tools/video/automation/review-package.mjs
  - tools/video/automation/review-package.test.mjs
  - docs/videos/BACKUP.md
---

# Fetch every off-host package onto the host before upload; prune review mp4s only after the Drive backup

## Why

站主 2026-11-03 定的規則（之前沒備份的不追）：
1. 上架前，每支影片在 VPS 上都要有一份完整的檔案，不論在哪裡做的，除非站主放棄並刪除它。
2. 站主刪除影片時，VPS 上那支的檔案整支刪掉。
3. 上架後先備份到雲端硬碟、確認完整，才把 VPS 上那支整支刪掉。站主同意的刪除時機：上架、
   備份核對完整、所有勾選的語言都已核准或略過，三樣齊了才刪；之後要補做就從雲端還原。

2026-11-03 對 main 的稽核（三個獨立讀者，結論抽查過程式）找出的缺口，這張票負責其中幾條。

這張：在雲端 session 或本機做、用 `review-push` 送上來的長片，檔案只在 API 的審核區
（`/var/lib/mokaair/video-reviews/<slug>/`），worker 的 `video_work/<slug>/` 什麼都沒有，所以備份跳過它
（`backup.mjs` 找不到 `auto.json`、`upload/final.mp4` 或 `review-package.json`）。`sync.mjs` 對沒有
`auto.json` 的片每一關都標 `hand_pushed: true`，但 `admin_status.py` `review_packages()` 只對 Shorts 認這個
標記，長片只認 `imported`。2026-11-03 查網站：curio-s*-v2 26 集與 curio-b01、b02 的 `backup` 全是 null。

另外：
- 語言批次（`--gate languages`，上架後才核准的配音與字幕）從來不抓：抓取只認核准的 `publish`。
- `prune_published_previews` 在上架確認核准 7 天後、一有 YouTube ID 就刪審核區的 mp4，完全不看備份；
  每次開 `/admin/videos` 列表就跑。核准後拖超過 7 天才上架的片，一上架 mp4 就沒了，worker 還沒抓，
  之後記成 `package_gone` 不再試。

## Definition of done

- [ ] 手動推送（`hand_pushed`）的長片，核准的上架確認也帶 `review_package`，worker 抓回 `video_work/<slug>/`，照一般流程備份。
- [ ] 核准的語言批次的檔案（配音、字幕、說明、各語縮圖）也被抓回同一個資料夾，排成上傳包的樣子；新批次核准時再抓。
- [ ] `prune_published_previews` 只刪備份已經 `done` 的影片的 mp4；備份關閉、沒設定、或沒 done 的一律不刪。
- [ ] BACKUP.md 改寫相關段落（含「`review-push` 的包本來就在 video_work」這句錯誤）。

## Steps

- [ ] `review_packages()`：長片也認 `hand_pushed`；worker 自己做的（有 `auto.json`）照舊不列。
- [ ] 語言批次：`ReviewPackage` 加上最新核准的 `languages` 審核；`review-package.mjs` 一併抓、放檔、記錄。
- [ ] 刪 mp4 的條件加上 `project.backup` 的 state 為 `done`。
- [ ] 測試：API（test_video_backup、test_video_reviews）、tools（review-package.test.mjs）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_backup.py tests/test_video_reviews.py -q
node --test tools/video/automation/review-package.test.mjs tools/video/automation/backup.test.mjs
```
部署後用影音權杖讀 `/api/video/automation/backup/config`：curio-b01、b02 帶 `review_package`；下一輪 worker 之後 `backup` 不再是 null。

## Notes
- 2026-11-03 認領時用了 `--force`：`2026-10-31-zhong-tian-clip-backup` 與 `2026-11-02-video-backup-shorts-sent-by-hand`
  （owner `claude-opus-5.5-zt-e033`）也蓋到 `apps/api/app/video_backup`、`test_video_backup.py`、BACKUP.md。兩張的程式都已合併
  （#1957、#1987、#1991），剩下的勾項是部署後驗證與回填，沒有開著的 PR 動這些檔；這張接在 #1991 之上改，不動它們的票。
