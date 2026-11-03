---
id: 2026-11-03-restore-a-purged-video-from-drive
title: Restore a purged video from Drive onto the host for late work
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-03T00:57:15Z
completed_at:
branch:
depends_on:
  - 2026-11-03-purge-a-video-from-the-host
scope:
  - tools/video/automation/restore.mjs
  - tools/video/automation/restore.test.mjs
  - tools/video/automation/cli.mjs
  - docs/videos/BACKUP.md
---

# Restore a purged video from Drive onto the host for late work

## Why

站主 2026-11-03 定的規則（之前沒備份的不追）：
1. 上架前，每支影片在 VPS 上都要有一份完整的檔案，不論在哪裡做的，除非站主放棄並刪除它。
2. 站主刪除影片時，VPS 上那支的檔案整支刪掉。
3. 上架後先備份到雲端硬碟、確認完整，才把 VPS 上那支整支刪掉。站主同意的刪除時機：上架、
   備份核對完整、所有勾選的語言都已核准或略過，三樣齊了才刪；之後要補做就從雲端還原。

2026-11-03 對 main 的稽核（三個獨立讀者，結論抽查過程式）找出的缺口，這張票負責其中幾條。

這張：整支刪除之後，補新語言、重試配音、從長片剪 Shorts 都要檔案；目前 tidy 之後這些都會失敗，也沒有從雲端還原的功能
（BACKUP.md §還原 只有手動步驟）。

## Definition of done

- [ ] `node tools/video/automation/cli.mjs restore <slug>` 依 `AI/備份/<系列>/<集>/backup.json` 下載回 `video_work/<slug>/`，逐檔比對 sha256。
- [ ] 需要檔案的後續工作（補語言、重試配音、剪 Shorts）遇到已清的片時，提示或自動先還原。

## Steps

- [ ] restore 指令與測試。
- [ ] 後續工作的接點。
- [ ] BACKUP.md §還原。

## How to verify

`node --test tools/video/automation/restore.test.mjs`

## Notes
