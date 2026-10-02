---
id: 2026-10-02-video-shorts-next-stops-offering-the
title: Video shorts: next stops offering the make job of a blocked Short
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-02T06:44:43Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_shorts/jobs.py
  - apps/api/tests/test_video_shorts_automation.py
---

# Video shorts: next stops offering the make job of a blocked Short

## Why

工人做實測 Shorts（`tools/video/shorts/lab.mjs`，票 `2026-09-28-video-shorts-worker-lab`）時，同一步連續兩輪失敗就把影片卡住：`PUT /video/reviews/{slug}` 送 `stage: "blocked"`，分頁把它列進「需要你」。但 `apps/api/app/video_shorts/jobs.py` 的 `next_job_for` 只略過影片被放棄（`project_dropped`）的 `making` 題目，所以卡住的那支只要它的時段還沒到，`GET /video/automation/shorts/next` 每一輪都回同一個 `make`。工人收到之後什麼都不做（卡住的影片等站主按重試），結果排在它後面的每一支 Shorts 都等到那一格過了才輪得到——一支卡住擋住整個月曆，跟 `docs/videos/SHORTS.md` §自動品管 說的「這支 Shorts 不會擋住月曆」相反。

## Definition of done

- [ ] `next_job_for` 遇到題目在 `making`、它的影片 `stage` 是 `blocked`、而且沒有還沒被工人確認的重試請求（`retry_request_id` 有值且不等於 `retry_acknowledged_id`）時，跳過它看下一格；`holds` 寫一句「「…」卡住了，等站主處理」。
- [ ] 站主按了重試（`retry_request_id` 是新的）時照樣回那支的 `make`，工人才接得到重試。
- [ ] `apps/api/tests/test_video_shorts_automation.py` 加上這兩種情況的測試。

## Steps

- [ ] `TopicFacts` 加 `project_blocked`（`stage == "blocked"` 且沒有待確認的重試），`next_job` 載入時算好。
- [ ] `next_job_for` 的 `make` 迴圈跳過它並記 hold。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts_automation.py -q
```

## Notes

- 工人端在 PR（票 `2026-09-28-video-shorts-worker-lab`）已經處理重試：收到卡住那支的 `make` 時，讀 `GET /video/automation/videos?shorts=only&state=needs_you` 的 `retry_request_id`，是新的才繼續，並在 `PUT /video/reviews/{slug}` 帶 `retry_acknowledged_id`。
- 沒有這張票之前的對策：站主在分頁放棄那支（`dropped_at`）或按重試，月曆就會往下走。
