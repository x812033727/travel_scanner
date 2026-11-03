---
id: 2026-11-03-review-push-sends-the-full-backup
title: review-push sends the full backup tier with the upload confirmation
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-11-03T00:57:06Z
completed_at:
branch:
depends_on:
  - 2026-11-03-fetch-every-off-host-package-onto
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/automation/review-package.mjs
  - tools/video/automation/review-package.test.mjs
  - apps/api/app/video_reviews/clips.py
  - apps/api/app/video_reviews/schemas.py
  - docs/videos/BACKUP.md
---

# review-push sends the full backup tier with the upload confirmation

## Why

站主 2026-11-03 定的規則（之前沒備份的不追）：
1. 上架前，每支影片在 VPS 上都要有一份完整的檔案，不論在哪裡做的，除非站主放棄並刪除它。
2. 站主刪除影片時，VPS 上那支的檔案整支刪掉。
3. 上架後先備份到雲端硬碟、確認完整，才把 VPS 上那支整支刪掉。站主同意的刪除時機：上架、
   備份核對完整、所有勾選的語言都已核准或略過，三樣齊了才刪；之後要補做就從雲端還原。

2026-11-03 對 main 的稽核（三個獨立讀者，結論抽查過程式）找出的缺口，這張票負責其中幾條。

這張：完整層級要 `clips/`、`keyframes/`、`characters/`、`timeline.json`、`narration.wav`（加上逐句錄音），
但 `review-push --gate publish` 只送 `upload/` 的檔案，`review-package.mjs` 的 `placeOf` 也沒有這些角色的位置；
所以在 VPS 以外做的片永遠湊不齊完整層級。`import --publish` 已經有 `clip_*`、`recording_*` 的做法可以照抄。
網站的完整性核對（`target.py` `missing_files`）也不數這些。

## Definition of done

- [ ] `review-push --gate publish` 一併送 keyframes、characters、timeline、旁白原檔、逐句錄音（照 import 的角色與上限）。
- [ ] worker 抓回後放到完整層級的位置，備份照常複製。
- [ ] 審核區的檔數與大小上限（每關 48 個、單檔 1.5 GB、總量 20 GB）對這些檔有交代，不會讓上架確認被拒。

## Steps

- [ ] 定角色名稱與上限（`schemas.py`、`clips.py`）。
- [ ] `sync.mjs` publish 送出；`review-package.mjs` 放檔。
- [ ] 測試。

## How to verify

`node --test tools/video/review/sync.test.mjs tools/video/automation/review-package.test.mjs`；API 的 review 測試。

## Notes
