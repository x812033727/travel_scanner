---
id: 2026-11-09-video-backups-go-to-a-separate
title: Video backups go to a separate repository (one per series)
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-focused-hopper
claimed_at: 2026-11-09T10:54:27Z
created_at: 2026-11-09T10:54:16Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/explainer-series/backup
  - docs/videos/explainer-series/BACKUP-BRANCHES.md
---

# Video backups go to a separate repository (one per series)

## Why

travel_scanner 推送時 GitHub 警告 "Repository is approaching its size quota"：每集的 `transfer/<slug>` 備份分支（一集 1–3 GB）都推在主 repo。站主 2026-11-09 要求另開備份 repo，並給了每個系列的 repo（奇聞 `mokaair-video-backup`、原來如此 `mokaair-video-backup-sothatswhy`、種田 `drama-backup-zt`、祖媽 `drama-backup-tn`）。

## Definition of done

- [x] `tobranch.sh`、`coverage.sh` 用 `BACKUP_REMOTE` 推到／讀自另一個 repo，不設時行為不變（`origin`）。
- [x] `BACKUP-BRANCHES.md` 寫明各系列的備份 repo 與用法。
- [x] P17 備份推到 `mokaair-video-backup-sothatswhy` 並通過 `coverage.sh`（a75a3734，missing 0、mismatches 0）；系列配樂（r2 與漏掉的 P02 bed）推到同一 repo 的 `transfer/sothatswhy-shared`（05143595，核對 0）。
- [ ] AI 劇的 `docs/videos/drama/BACKUP-BRANCHES.md` 也改指向 `drama-backup-*`（另開票，不在本票 scope）。
- [ ] 主 repo 上已有的 `transfer/*`、`claude/backup-*` 要不要搬、要不要刪：等站主決定。

## Steps

- [x] 改兩支腳本，以本機 bare repo 當 `BACKUP_REMOTE` 測：兩次推送 fast-forward、`coverage.sh` missing 0、origin 沒有新分支。

## How to verify

`BACKUP_REMOTE=<bare repo> tobranch.sh transfer/test <dir> test-slug msg` 兩次，再 `BACKUP_REMOTE=<bare repo> coverage.sh transfer/test <dir> test-slug`。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- 2026-11-09：建 repo 的 API 回 403（GitHub App 不能建 repo），站主自己給了四個系列的備份 repo。
  不必 clone 備份 repo：在 travel_scanner 加 remote（`git remote add backup-sothatswhy <url>`）直接推，省磁碟；session 要先 `add_repo` push 權限。
  `tobranch.sh` 的暫存物件在整次執行結束才刪，3.5 GB 的工作目錄要留約 3.5 GB 空間。
