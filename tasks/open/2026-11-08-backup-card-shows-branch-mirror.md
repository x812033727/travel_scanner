---
id: 2026-11-08-backup-card-shows-branch-mirror
title: 後台備份卡顯示每條 transfer 分支的鏡像狀態
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-11-08T09:06:13Z
completed_at:
branch:
depends_on:
  - 2026-11-08-drive-mirrors-transfer-branches
scope:
  - apps/api/app/video_backup
  - apps/api/tests/test_video_backup_branch_mirror.py
  - apps/web/components/admin-video-backup.tsx
  - apps/web/components/admin-video-backup.test.tsx
  - apps/web/lib/video-backup-messages
  - apps/web/app/api/video/automation/backup
  - tools/video/automation/branch-mirror.mjs
  - tools/video/automation/branch-mirror.test.mjs
---

# 後台備份卡顯示每條 transfer 分支的鏡像狀態

## Why

站主 2026-11-08 同意主機 worker 把 AI 劇的 `transfer/zt-*`、`transfer/tn-*` 分支鏡像到雲端硬碟
（票 `2026-11-08-drive-mirrors-transfer-branches`，`tools/video/automation/branch-mirror.mjs`）。那張票沒有動 API 與 web，
所以每條分支鏡像到哪個 commit、什麼時候、核對結果，今天只在 worker 的 log（`branch mirror:` 開頭的行）與
`video_work/_branch-mirror/branch-mirror.json`。站主要開 shell 才看得到，違反「推完分支後，等後台顯示這條分支已鏡像」。

## Definition of done

- [ ] `/admin/videos?tab=settings#video-backup-settings` 的備份卡多一個「分支」區塊：每條分支一列，顯示分支名、最後鏡像的 commit（短）、
      時間、檔數與大小、核對結果（已核對／有差異／失敗與原因），以及還在等的分支（遠端有新 commit、還沒鏡像）。
- [ ] worker 每條分支做完（成功或失敗）就回報網站；網站存最後一筆，不存歷史。
- [ ] 五個語系的文案（`npm run check:i18n`）。

## Steps

- [ ] API：`apps/api/app/video_backup` 加 `POST /api/video/automation/backup/branches/report`（影片工具權杖，跟其他 backup 路由一樣），
      body `{branch, commit, folder, mirrored_at, files, bytes, check, error}`；存在 `ProviderConfig("video_backup")` 旁邊或一張小表
      （走 backend-conventions：migration 接 head、整合測試）。後台狀態 API 帶出這些列。
- [ ] web：`apps/web/app/api/video/automation/backup/` 加對應的 BFF 路由；`admin-video-backup.tsx` 加「分支」區塊與測試。
- [ ] worker：`branch-mirror.mjs` 每條分支做完呼叫 `backupClient` 的新方法回報；網站沒有這條路由（404）時照舊只寫 log。

## How to verify

1. API 與 web 的單元測試；`node --test tools/video/automation/branch-mirror.test.mjs` 加一個假網站收回報的案例。
2. 部署後在備份卡看到 `zt-live-e001` 等分支的 commit 與「已核對」，跟 `branch-mirror.json` 一致。

## Notes

- worker 端的狀態格式見 `branch-mirror.mjs` 的 `branchMirrorRound`：`state.branches[<分支>] = {commit, mirrored_at, attempted_at, folder, check, files, bytes, joined, failures, error, pending_commit}`。
- 開票時只開了 `apps/web/app/api/video/automation/backup` 這個資料夾；動手前把 scope 縮到實際要改的檔。
