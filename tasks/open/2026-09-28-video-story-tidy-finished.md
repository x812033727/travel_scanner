---
id: 2026-09-28-video-story-tidy-finished
title: 影片上架後清掉工人的工作檔
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-video-story-tidy
claimed_at: 2026-09-28T11:20:25Z
created_at: 2026-09-28T03:31:14Z
completed_at:
branch: claude/video-story-tidy-finished
depends_on: []
scope:
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
  - tools/video/automation/cli.mjs
  - tools/video/automation/cli.test.mjs
  - tools/video/cli.mjs
  - docs/videos/AUTOMATION.md
---

# 影片上架後清掉工人的工作檔

## Why

工人的工作區（volume `video_work`）沒有任何清理。一支品牌故事約留下 1.3–2 GB（音檔、關鍵影格、每鏡一段的片段、成片），每天兩支一個月就是幾十 GB（`docs/videos/STORY.md` §上限與成本），主機磁碟會先滿。

## Definition of done

- [ ] 影片已經記下 YouTube id（狀態 `done`）而且超過保留天數時，刪掉它工作區裡可以重做的大檔：`segments/`、`build/`、`audio/`、`keyframes/`、`clips/`、`final.mp4` 與預覽；留下 `auto.json`、`state.json`、`checks.json`、帳本與核准紀錄。
- [ ] 還在製作、卡住、等站主的影片一個檔都不刪。
- [ ] 每一輪最多清一支，印出刪了什麼、釋放多少空間；`--dry-run` 只列不刪。
- [ ] 測試涵蓋：已上架、剛上架未滿保留天數、製作中、已放棄四種狀態。

## Steps

- [ ] `tidy.mjs`：判斷與刪除；保留天數預設 7 天，與審核檔案區刪 mp4 的規則一致。
- [ ] 在工人每輪的最後呼叫一次。
- [ ] 測試。

## How to verify

```bash
node --test tools/video/automation/tidy.test.mjs
npm run test:tools
```

## Notes

- 已放棄的影片照同一條規則清（放棄滿保留天數）。
- 作品的共用存檔 `_series/<作品>/`（設定圖、風格錨定圖）與 `_music/` 不清。
- 2026-09-28 認領時拿掉 `depends_on: 2026-09-28-video-story-worker`：清理在 `auto` 每一輪的最後呼叫一次（`tools/video/automation/cli.mjs`），不在故事的流程裡，也不讀故事工人寫的任何東西，所以不必等那張票。
- scope 加上：`automation/cli.mjs`（每輪最後的呼叫）與它的測試 `automation/cli.test.mjs`、`tools/video/cli.mjs`（指令表加 `tidy` 讓人手動跑與 `--dry-run`，`status` 遇到已清理的影片不再寫「下一步：assemble」）、`docs/videos/AUTOMATION.md`（工人的環境變數）。`flow.mjs`、`series.mjs`、`prompts.mjs` 只讀不改（#897、#904 正在改）。
- 以 `--force` 認領，原因：`2026-09-26-video-dubs-worker`、`2026-09-27-video-drama-room-worker`、`2026-09-27-video-split-settings-worker`、`2026-09-27-video-drama-room-skill-docs` 四張票停在 `review`，scope 含 `tools/video/automation` 或 `docs/videos/AUTOMATION.md`，但它們的工作已在 #870（79e26fcdf，2026-09-27）合併進 main，只是票沒有移到 done；沒有開著的 PR 或分支在做清理（`git ls-remote`、`gh pr list` 都查過）。這四張票不動。
