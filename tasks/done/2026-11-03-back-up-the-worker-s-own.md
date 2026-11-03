---
id: 2026-11-03-back-up-the-worker-s-own
title: Back up the worker's own Shorts under video_work/_shorts
status: done
priority: P2
area: tools
owner: claude-opus-5-5-backup-rules
claimed_at: 2026-11-03T02:32:35Z
created_at: 2026-11-03T00:57:07Z
completed_at: 2026-11-03T02:34:13Z
branch: claude/video-backup-worker-shorts
depends_on:
  - 2026-11-03-fetch-every-off-host-package-onto
scope:
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - apps/api/app/video_backup/admin_status.py
  - docs/videos/BACKUP.md
---

# Back up the worker's own Shorts under video_work/_shorts

## Why

站主 2026-11-03 定的規則（之前沒備份的不追）：
1. 上架前，每支影片在 VPS 上都要有一份完整的檔案，不論在哪裡做的，除非站主放棄並刪除它。
2. 站主刪除影片時，VPS 上那支的檔案整支刪掉。
3. 上架後先備份到雲端硬碟、確認完整，才把 VPS 上那支整支刪掉。站主同意的刪除時機：上架、
   備份核對完整、所有勾選的語言都已核准或略過，三樣齊了才刪；之後要補做就從雲端還原。

2026-11-03 對 main 的稽核（三個獨立讀者，結論抽查過程式）找出的缺口，這張票負責其中幾條。

這張：worker 自己做的 Shorts（lab、cut）放在 `video_work/_shorts/<slug>/<build>/`
（`automation/shorts.mjs`、`shorts/lab.mjs`、`shorts/build.mjs`），備份只讀 `video_work/<slug>/`，
tidy 也跳過 `_` 開頭的名字，所以它們從沒備份過，也從沒清過；網站一直顯示 `not_queued`。
`admin_status.py` 與 BACKUP.md 說它們「本來就在 video_work」是錯的。

## Definition of done

- [x] 備份找得到 worker 做的 Shorts 的最新一版，照 Shorts 的上傳包（final、字幕、封面、titles.json）加完整層級備份。
- [x] 網站的備份狀態對它們正確顯示。

## Steps

- [x] `backup.mjs` 依 slug 找 `_shorts/<slug>/` 的最新 build。
- [x] 測試、BACKUP.md。

## How to verify

`node --test tools/video/automation/backup.test.mjs`

## Notes
- 2026-11-03 認領用 `--force`：backup.mjs 與舊的 review 狀態票重疊，查無開著的 PR。
- 做法：`backup.mjs` 新增 `videoDir(base, slug, fs)`，`job.workdir` 改用它：`<base>/<slug>/` 不存在時讀
  `_shorts/<slug>/lab.json` 的 `build`，必須在 `_shorts/<slug>/` 裡、有 `upload/final.mp4` 才用。備份紀錄寫在該 build 內，
  新 build 會再備份一次。`admin_status.py` 不用改：worker 的 Shorts 沒有 `hand_pushed`，本來就不列 `review_package`。
- 沒做：主機上用 `shorts build`／`from-drama` 手動做、放在 `<base>/<slug>/<build-ts>/` 的 Short（稽核第 11 點），
  那種資料夾沒有 `upload/final.mp4` 在頂層，仍然不會備份；之後若有需要另開票。
- 驗證：`node --test tools/video/automation/backup.test.mjs`（24 passed，新測試涵蓋選對 build、拒絕跑出 `_shorts/<slug>/` 外與
  沒有成片的 build、不在工作根目錄多建資料夾）、tidy／review-package／backup-between-units 52 passed。
