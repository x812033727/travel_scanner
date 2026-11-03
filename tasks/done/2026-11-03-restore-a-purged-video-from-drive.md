---
id: 2026-11-03-restore-a-purged-video-from-drive
title: Restore a purged video from Drive onto the host for late work
status: done
priority: P2
area: tools
owner: claude-opus-5-5-backup-rules
claimed_at: 2026-11-03T05:55:31Z
created_at: 2026-11-03T00:57:15Z
completed_at: 2026-11-03T05:55:32Z
branch: claude/video-restore-from-drive
depends_on:
  - 2026-11-03-purge-a-video-from-the-host
scope:
  - tools/video/automation/restore.mjs
  - tools/video/automation/restore.test.mjs
  - tools/video/automation/cli.mjs
  - tools/video/cli.mjs
  - tools/video/automation/tidy.mjs
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

- [x] `node tools/video/automation/cli.mjs restore <slug>` 依 `AI/備份/<系列>/<集>/backup.json` 下載回 `video_work/<slug>/`，逐檔比對 sha256。
- [ ] 需要檔案的後續工作（補語言、重試配音、剪 Shorts）遇到已清的片時，提示或自動先還原。

## Steps

- [x] restore 指令與測試。
- [ ] 後續工作的接點。
- [x] BACKUP.md §還原。

## How to verify

`node --test tools/video/automation/restore.test.mjs`

## Notes
- 2026-11-03 認領用 `--force`（tidy.mjs、cli.mjs 與舊的 review／in-progress 票重疊，查無開著的 PR）。
- 做法：`tools/video/automation/restore.mjs` 的 `restoreVideo`，指令是 `node tools/video/cli.mjs restore --slug S [--dry-run] [--workdir D]`
  （上層 cli 的 COMMANDS 對到 automation）。讀雲端 `backup.json`（沒有就用主機留下的），`rclone copy` 到 `video_work/_restore-stage/<slug>/`，
  逐檔比 sha256／大小，`workPathOf`（planFiles 的反向）放回去；worker 影片把 `upload/final.mp4` 硬連結回根目錄 `final.mp4`；
  `auto.json` 拿掉 `tidied_at`／`tidied`、寫 `restored_at`（手動資料夾寫 `tidied.json`）。tidy 在 `RESTORE_HOLD_DAYS`（14 天）內保留還原的影片。
- 沒做：「後續工作遇到已清的片時自動先還原」。flow.mjs 受長片時長審查綁定，且自動花 Drive 流量要站主決定；
  目前 worker 對已清的影片照舊把新勾的語言回報為「工作檔已清」，要先手動 restore（或請 AI 下指令）。要自動的話另開票。
- 驗證：`node --test tools/video/automation/restore.test.mjs`（3 passed：路徑對照；備份→整支清除→還原逐位元組相同、tidy 保留 14 天後再清；
  雲端檔案對不上時不放、回報）；backup、tidy、cli、backup-between-units、review-package、tools/video/cli.test.mjs 共 93 passed。
