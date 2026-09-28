---
id: 2026-09-28-video-story-tidy-finished
title: 影片上架後清掉工人的工作檔
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:31:14Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-worker
scope:
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
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
