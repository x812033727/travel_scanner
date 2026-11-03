---
id: 2026-11-03-deleting-a-dropped-video-removes-its
title: Deleting a dropped video removes its whole host work directory and its Shorts
status: done
priority: P2
area: api
owner: claude-opus-5-5-backup-rules
claimed_at: 2026-11-03T05:47:36Z
created_at: 2026-11-03T00:57:15Z
completed_at: 2026-11-03T05:47:52Z
branch: claude/video-delete-host-workdir
depends_on:
  - 2026-11-03-purge-a-video-from-the-host
scope:
  - apps/api/app/video_backup/admin_status.py
  - apps/api/app/video_backup/schemas.py
  - apps/api/tests/test_video_backup.py
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - docs/videos/BACKUP.md
  - apps/api/app/video_reviews/admin_deletion.py
  - apps/api/tests/test_video_reviews_delete.py
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
  - tools/video/automation/flow.mjs
---

# Deleting a dropped video removes its whole host work directory and its Shorts

## Why

站主 2026-11-03 定的規則（之前沒備份的不追）：
1. 上架前，每支影片在 VPS 上都要有一份完整的檔案，不論在哪裡做的，除非站主放棄並刪除它。
2. 站主刪除影片時，VPS 上那支的檔案整支刪掉。
3. 上架後先備份到雲端硬碟、確認完整，才把 VPS 上那支整支刪掉。站主同意的刪除時機：上架、
   備份核對完整、所有勾選的語言都已核准或略過，三樣齊了才刪；之後要補做就從雲端還原。

2026-11-03 對 main 的稽核（三個獨立讀者，結論抽查過程式）找出的缺口，這張票負責其中幾條。

這張：站主在 /admin/videos 放棄再刪除一支影片時（`admin_deletion.delete_project`），網站刪掉資料庫列、審核區與素材區，
但 VPS 的 `video_work/<slug>/` 不刪；worker 只在它看到放棄時把狀態改成 dropped，7 天後由 tidy 刪大檔，資料夾本身與其他檔永遠留。
worker 沒看到放棄的情況（已做完的片、不在網站最新 200 支裡、自動化關著時刪的）永遠殘留。
由這支剪出的 Shorts（`source_slug`）與主機的 `docs/videos/<slug>/` 也不刪。

## Definition of done

- [x] 刪除時網站留一筆待刪紀錄；worker 下一輪照紀錄把 `video_work/<slug>/`（與 `_shorts/` 底下由它剪出的 Shorts）整個刪掉，回報完成。
- [x] 不依賴 worker 有沒有在清單上看過放棄。
- [ ] 已上架的片被刪除：先確認備份完成（或站主明確選擇不備份）再刪。（沒做：站主 2026-11-03 的規則是「刪除就整支刪」，見 Notes）

## Steps

- [x] API：待刪紀錄與 worker 讀取、回報的路由。
- [x] worker：照紀錄刪除，守住只刪 work base 底下的那個 slug。
- [x] 測試。

## How to verify

API 的 `test_video_reviews_delete.py`；`node --test tools/video/automation/tidy.test.mjs`。

## Notes

admin_deletion.py 在 2026-11-03 被 `2026-10-30-admin-video-delete-dropped`（review，PR #1943 已合併）持有。
- 2026-11-03 認領用 `--force`（admin_deletion.py 等與舊的 review 票重疊，查無開著的 PR）。
- 做法：不加 migration。`delete_project` 本來就寫一筆 `video_project_deleted` 稽核紀錄（metadata 有 slug）；
  `admin_status.deleted_slugs` 讀近 60 天的這些紀錄、扣掉目前有影片列的 slug，放進 worker 的 `/backup/config` 的 `deleted`。
  worker 的 `backupRound` 不論備份開關都把它放進 gate；`tidyRound` 先對每個 slug 刪 `<base>/<slug>/` 與 `<base>/_shorts/<slug>/`
  整個資料夾（真的資料夾、父目錄正確、不跟連結、不碰 repo），印一行；那一輪不再評估這些 slug。
- 「已上架的片要先備份完成再刪」沒做：站主的規則二是「如果我刪除應該就要刪除整個該影片的完整」，刪除不等雲端。已上架影片
  本來就會在上架後備份；刪除前沒備份完的，雲端就沒有那一份。
- 沒做：從這支剪出的 Shorts（`source_slug`）是另外的影片列，要各自放棄、刪除；主機的 `docs/videos/<slug>/` 不刪（是 repo 同步的文件）。
- 後台文案 `previewsGone`、`mp4Retired`（五語 admin.json）還寫「上架滿 7 天從審核區刪除」，2026-11-03 起改成備份完成後整支刪；
  另開票改文案。
- 驗證：`node --test` backup、tidy、cli、backup-between-units 77 passed（新測試：刪除的影片與它的 `_shorts` 資料夾整個刪掉、
  連結不跟、乾跑不刪、下一輪不再出現）；API `test_video_backup`、`test_video_reviews_delete` 66 passed，ruff、mypy 過。
