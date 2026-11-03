---
id: 2026-11-03-back-up-the-worker-s-own
title: Back up the worker's own Shorts under video_work/_shorts
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-03T00:57:07Z
completed_at:
branch:
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

- [ ] 備份找得到 worker 做的 Shorts 的最新一版，照 Shorts 的上傳包（final、字幕、封面、titles.json）加完整層級備份。
- [ ] 網站的備份狀態對它們正確顯示。

## Steps

- [ ] `backup.mjs` 依 slug 找 `_shorts/<slug>/` 的最新 build。
- [ ] 測試、BACKUP.md。

## How to verify

`node --test tools/video/automation/backup.test.mjs`

## Notes
