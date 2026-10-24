---
id: 2026-10-20-s52-r19-clean-pr-integration
title: Integrate S52 R19 preproduction and audio receipts into clean PR
status: done
priority: P1
area: docs
owner: codex-gpt6-s52-r19-audio
claimed_at: 2026-10-20T21:54:11Z
created_at: 2026-10-20T21:54:09Z
completed_at: 2026-10-20T21:55:12Z
branch: codex/curio-preproduction-s46-s56-20261020
depends_on: []
scope:
  - docs/videos/curio-s52
  - tasks/done/2026-10-20-curio-s52
  - tasks/done/2026-10-20-s52
  - tasks/open/2026-10-20-curio-s52-tahiti-venus-transit.md
  - tasks/open/2026-10-20-s52-r18-narrow-narrative-repair.md
---

# Integrate S52 R19 preproduction and audio receipts into clean PR

## Why

PR #1632 的乾淨工作樹尚無 S52；原工作樹已完成 S52 R19 的史料、雙盲、政策與機器音檢，需只把 S52 文件及其任務紀錄加入 PR，不帶入其他集或私有媒體。

## Definition of done

- [x] PR 分支收錄整個 `docs/videos/curio-s52` 與所有 scope 指向該集的任務檔，且不收錄其他集、語音 WAV、權杖或 `node_modules`。
- [x] S52 lint、文件影片測試、任務板及已暫存差異檢查通過。

## Steps

- [x] 在乾淨工作樹認領本任務，核對來源與目標分支狀態。
- [x] 搬入 154 份 S52 文件及 22 份既有 S52 任務檔。
- [x] 執行檢查，僅暫存、提交及推送 S52 差異。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s52 --json`：0 error、0 warning、115 句。`npm run test:docs-videos`：236/236 PASS。`npm run check:tasks`：退出碼 0；`git diff --cached --check`：退出碼 0。`git show --stat --oneline HEAD` 應只含 S52 文件及任務。

## Notes

來源語音留在 `/workspace/.video-work/curio-s52/`，不入 Git；文件有 SHA 與驗證收據。工作樹原有未追蹤 `node_modules`，未暫存也未刪除。任務板仍有其他集的既有 stale claim／scope overlap 警告，無本任務的結構錯誤。
