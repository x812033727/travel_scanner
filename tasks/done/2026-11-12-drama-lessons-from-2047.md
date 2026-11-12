---
id: 2026-11-12-drama-lessons-from-2047
title: 把 #2047 的 AI 劇教訓、審片規則與工具收進 main（分支規則只留作紀錄）
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-11-12T01:50:31Z
created_at: 2026-11-12T01:49:50Z
completed_at: 2026-11-12T02:03:03Z
branch: claude/drama-lessons-from-2047
depends_on: []
scope:
  - .agents/skills/animation-preproduction/references/script-to-storyboard.md
  - .agents/skills/animation-preproduction/references/storyboard-shot-spec.md
  - .agents/skills/minimax-h3-colab/references/lessons.md
  - .agents/skills/minimax-h3-runpod/references/route-a.md
  - docs/videos/AI-DRAMA-DRIVE.md
  - docs/videos/drama/BACKUP-BRANCHES.md
  - docs/videos/drama/README.md
  - docs/videos/drama/REVIEW.md
  - docs/videos/drama/WRITING.md
  - docs/videos/lessons/shared.md
  - docs/videos/lessons/tai-nainai.md
  - docs/videos/lessons/zhong-tian-qu-qi.md
  - docs/videos/rules-sync/manifest.tsv
  - docs/videos/rules-sync/watch.txt
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/REVIEW.md
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/RULES.md
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/cast.json
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/s1-bible-e001-e060.md
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools/compile.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/REVIEW.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/RULES.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/README.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/audio-qa.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/continuity-sheets.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/cut-jumps.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/cut-qa.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/independent-review.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/preflight-prompts.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/cut-review-2.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/cut-review.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/expression-review.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/assemble-v4.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e901-live.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/gen-dh.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/live-action-plan.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/live-action/pilot.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/live-action/refine-prep.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/live-action/screen-test.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/live-action/stage.py
  - docs/videos/series-plans/zhong-tian-qu-qi/production/storyboard-brief-for-planners.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/storyboard-rules.md
---

# 把 #2047 的 AI 劇教訓、審片規則與工具收進 main（分支規則只留作紀錄）

## Why

#2047（`claude/drama-branch-backup`，2026-11-08）掛名「AI 劇備份分支規則」，但 49 個檔裡大半是 main 沒有的製作內容：
共用區的分鏡寫法、審片流程、依主題整理的教訓（440 行），種田與祖媽各自的規則、審片項目與教訓，e901 真人版審片紀錄，
審片與 QA 工具，以及兩個 skill references 的教訓。main 上 `docs/videos/lessons/zhong-tian-qu-qi.md`、`tai-nainai.md` 只有表頭。
分支備份 2026-11-10 起停用、舊分支 2026-11-11 搬完刪除，#2047 不能照原樣合併；站主 2026-11-12：「照你建議的做，開新 PR 收進來」。

## Definition of done

- [x] 共用區 `docs/videos/drama/`（README、WRITING、REVIEW、BACKUP-BRANCHES）進 main；BACKUP-BRANCHES 標停用，「要備份什麼」的清單仍是 `AI-DRAMA-DRIVE.md` 引用的依據。
- [x] 三份 LESSONS 併進 `docs/videos/lessons/shared.md`、`zhong-tian-qu-qi.md`、`tai-nainai.md`（AGENTS.md：教訓只寫在 lessons/），所有連結改指過去。
- [x] 種田、祖媽的 `production/RULES.md`、`REVIEW.md`、e901 審片紀錄、審片與 QA 工具、live-action 工具進 main；對 main 已有檔的修改以三方合併套上。
- [x] 不收：`production/backup/` 推分支工具、`GAPS-20261108.md`（PR 分支自己的缺口檢查，已在 PR 內處理）、`BACKUP.md` 的分支鏡像段、鏡像分支的任務檔。
- [x] `docs/videos/drama/*.md` 加進規則同步（watch.txt、manifest.tsv → `AI劇/_共用規則/規則/drama/`）。
- [x] 合併後關閉 #2047，附上本 PR 連結（PR 合併後由同一個 session 關）。

## How to verify

```bash
npm run test:docs-videos && npm run test:tools && npm run check:tasks
```

## Notes

- 認領時與五張逾期（>24h）的票範圍重疊（`2026-10-29-32-40-colab-ref2va`、`2026-11-06-tai-nainai-*`），只重疊在 `minimax-h3-colab/references/lessons.md`、祖媽 `cast.json`、`s1-bible-e001-e060.md`；#2047 對這些檔的修改本來就來自同一批工作，所以 `--force`。
- 併進 lessons 的內容放在各檔〈依主題整理（2026-11-08 收進來…）〉一節，章節號照原檔；新教訓照 lessons 的寫法加在那一節上面。
- 本機驗證：`npm run test:tools` 3029 個 0 失敗；`npm run test:docs-videos` 6 個失敗，與同一台主機上的 origin/main 完全相同（imported-long-languages 的 runner 測試，環境因素）；`check:tasks` 通過。
- `minimax-h3-colab/references/lessons.md` 提到的祖媽 `production/post/review-e001.md` 只在 `claude/intelligent-gates-9n92xm`，改寫成指向那條分支（skills 測試要求提到的路徑存在）。
