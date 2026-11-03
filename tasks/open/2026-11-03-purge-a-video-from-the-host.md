---
id: 2026-11-03-purge-a-video-from-the-host
title: Purge a video from the host only after Drive holds all of it, then purge all of it
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-11-03T00:57:14Z
completed_at:
branch:
depends_on:
  - 2026-11-03-fetch-every-off-host-package-onto
  - 2026-11-03-back-up-the-worker-s-own
scope:
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - apps/api/app/video_backup/target.py
  - apps/api/app/video_reviews/admin_service.py
  - docs/videos/BACKUP.md
---

# Purge a video from the host only after Drive holds all of it, then purge all of it

## Why

站主 2026-11-03 定的規則（之前沒備份的不追）：
1. 上架前，每支影片在 VPS 上都要有一份完整的檔案，不論在哪裡做的，除非站主放棄並刪除它。
2. 站主刪除影片時，VPS 上那支的檔案整支刪掉。
3. 上架後先備份到雲端硬碟、確認完整，才把 VPS 上那支整支刪掉。站主同意的刪除時機：上架、
   備份核對完整、所有勾選的語言都已核准或略過，三樣齊了才刪；之後要補做就從雲端還原。

2026-11-03 對 main 的稽核（三個獨立讀者，結論抽查過程式）找出的缺口，這張票負責其中幾條。

這張：上架後的清理（`tidy.mjs`）與審核區的 mp4 刪除，跟規則 3 不合：
- tidy 等的是「上架後 7 天」，不是「備份核對完整後」；而且只刪大檔，明文拒絕刪整個工作資料夾，
  其他檔案（auto.json、captions、i18n、media、review、upload 的小檔、backup 紀錄…）永遠留著。
- 審核區只刪 mp4，字幕、配音、縮圖、錄音永遠留著（也會逐漸塞滿 20 GB 上限）。
- 備份關閉、設定沒存、或系列層級設成「關閉」時，tidy 照刪、不備份。
- 完整層級沒備份逐句錄音（`audio/`、各語配音的逐句檔），tidy 卻會刪。
- 網站的「完整」只核對上傳包；片段、分鏡、旁白、錄音不核對；刪之前不回雲端再核一次。
- 匯入的片、手動做的資料夾、手動推的 Shorts 備份後永遠不清；已上架又被放棄的片清理不等備份。

## Definition of done

- [ ] 刪除條件：已上 YouTube、備份 worker 與網站都 `done`、完整層級每一類都核對過（含片段、分鏡、旁白、錄音）、
      刪之前 `rclone check` 再核一次雲端、所有勾選的語言已核准或略過。
- [ ] 條件齊了就把 `video_work/<slug>/` 整個刪掉，審核區 `<slug>/` 的檔案也全部刪掉（資料庫列保留）。
- [ ] 備份關閉、沒設定、層級「關閉」、配額不足、網站連不上：一律不刪。
- [ ] 逐句錄音進完整層級。
- [ ] 匯入、手動、手動推送的 Shorts 一樣適用；已上架又放棄的片也要先備份完成。

## Steps

- [ ] 擴充 `target.py` 的完整性核對到完整層級。
- [ ] tidy 改成上述條件並整支刪除；審核區刪除改由同一條件觸發。
- [ ] 測試、BACKUP.md。

## How to verify

`node --test tools/video/automation/tidy.test.mjs tools/video/automation/backup.test.mjs`；API 測試。

## Notes

tidy.mjs 在 2026-11-03 被 `2026-10-19-worker-video-languages-five`（review）與 `2026-10-29-daily-brief-on-the-host-worker`
（in-progress）持有；認領前先確認它們落地或釋出。
