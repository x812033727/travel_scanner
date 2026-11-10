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
- [x] 站主 2026-11-09「舊分支先搬過去再刪」：104 條全部搬到各系列 repo，逐條 `git ls-remote` 確認同一個 commit（清單 `docs/videos/explainer-series/backup/moved-20261109.tsv`）。
- [ ] 從 travel_scanner 刪掉這 104 條：雲端 session 的 git proxy 不准刪分支（HTTP 403），要站主在自己電腦跑下面的指令或在 GitHub Branches 頁刪。

## Steps

- [x] 改兩支腳本，以本機 bare repo 當 `BACKUP_REMOTE` 測：兩次推送 fast-forward、`coverage.sh` missing 0、origin 沒有新分支。

## How to verify

`BACKUP_REMOTE=<bare repo> tobranch.sh transfer/test <dir> test-slug msg` 兩次，再 `BACKUP_REMOTE=<bare repo> coverage.sh transfer/test <dir> test-slug`。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- 2026-11-09：建 repo 的 API 回 403（GitHub App 不能建 repo），站主自己給了四個系列的備份 repo。
  不必 clone 備份 repo：在 travel_scanner 加 remote（`git remote add backup-sothatswhy <url>`）直接推，省磁碟；session 要先 `add_repo` push 權限。
  `tobranch.sh` 的暫存物件在整次執行結束才刪，3.5 GB 的工作目錄要留約 3.5 GB 空間。

- 2026-11-09 搬移：82 條種田分支另一個 session 已搬好（同 commit）；其餘 22 條逐 commit 推（每次 < 1.5 GB，避開 2 GB 上限），
  暫存物件目錄每條用完即刪。目標已有同名但不同 commit 的 8 條，放在 `archive/travel_scanner/<分支>`，不覆蓋。
  `claude/backup-from-review-store`、`claude/backup-repos-per-series` 是程式碼分支，不搬不刪。
  **坑**：對沒有 fetch refspec 以外的 remote 推送會建 `refs/remotes/<remote>/...`，指向已刪的暫存物件，之後每次 fetch 都失敗（bad object）。
  備份 remote 一律拿掉 `remote.<名>.fetch`。另一個 session（`claude/backup-repos-per-series`）也改了 BACKUP-BRANCHES.md，合併時要統一。
- 刪除指令（在 travel_scanner 的 checkout 裡跑；分支被動過就不會刪）：

```bash
grep -v '^#' docs/videos/explainer-series/backup/moved-20261109.tsv | while IFS=$'\t' read -r b sha repo dest; do
  git push --force-with-lease="refs/heads/$b:$sha" origin ":refs/heads/$b"
done
```
