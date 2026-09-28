---
id: 2026-09-28-video-planner-counts-the-ai-shorts-folder
title: The video planner counts docs/videos/ai-shorts as a video it already made
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-28T04:25:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# The video planner counts docs/videos/ai-shorts as a video it already made

## Why

`tools/video/automation/flow.mjs` 的 `earlierVideos()` 把 `docs/videos` 底下**每一個資料夾**都當成一支做過的影片，不管裡面有沒有 `video.json` 或 `brief.md`。PR #871 加了 `docs/videos/ai-shorts/`（企劃、試片腳本、實驗紀錄），它不是一支影片，卻會以「代號 `ai-shorts`、標題空白、沒有來源文章」的樣子進到企劃模型看的「已經做過的影片」清單，代號也被當成已經用掉。

2026-09-28 規劃 Shorts 區時讀程式發現的，還沒有在正式站造成看得到的問題：主機工人的 `docs/videos` 是舊的 volume，裡面還沒有這個資料夾。volume 一更新（票 `2026-09-25-the-video-worker-s-docs-volume`）就會出現。

## Definition of done

- [ ] `earlierVideos()` 只收有 `video.json` 或 `brief.md` 的資料夾。
- [ ] 測試：`docs/videos` 底下放一個只有說明文件的資料夾，清單裡沒有它；有 `brief.md` 沒有 `video.json` 的草稿仍然在清單裡。

## Steps

- [ ] 改 `earlierVideos()` 的篩選。
- [ ] 加測試。

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs
```

## Notes

- `2026-09-28-video-shorts-worker-lab` 也會改 `flow.mjs`；兩張票不要同時做，誰先拿到誰順手做掉這一項並在另一張票留一句。
