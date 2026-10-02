---
id: 2026-10-02-video-shorts-next-stops-offering-the
title: Video shorts: next stops offering the make job of a blocked Short
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-02T08:20:24Z
created_at: 2026-10-02T06:44:43Z
completed_at: 2026-10-02T08:22:32Z
branch: claude/shorts-skip-blocked
depends_on: []
scope:
  - apps/api/app/video_shorts/jobs.py
  - apps/api/tests/test_video_shorts_automation.py
---

# Video shorts: next stops offering the make job of a blocked Short

## Why

工人做實測 Shorts（`tools/video/shorts/lab.mjs`，票 `2026-09-28-video-shorts-worker-lab`）時，同一步連續兩輪失敗就把影片卡住：`PUT /video/reviews/{slug}` 送 `stage: "blocked"`，分頁把它列進「需要你」。但 `apps/api/app/video_shorts/jobs.py` 的 `next_job_for` 只略過影片被放棄（`project_dropped`）的 `making` 題目，所以卡住的那支只要它的時段還沒到，`GET /video/automation/shorts/next` 每一輪都回同一個 `make`。工人收到之後什麼都不做（卡住的影片等站主按重試），結果排在它後面的每一支 Shorts 都等到那一格過了才輪得到——一支卡住擋住整個月曆，跟 `docs/videos/SHORTS.md` §自動品管 說的「這支 Shorts 不會擋住月曆」相反。

## Definition of done

- [x] `next_job_for` 遇到題目在 `making`、它的影片 `stage` 是 `blocked`、而且沒有還沒被工人確認的重試請求（`retry_request_id` 有值且不等於 `retry_acknowledged_id`）時，跳過它看下一格；`holds` 寫一句「「…」卡住了，等站主處理」。
- [x] 站主按了重試（`retry_request_id` 是新的）時照樣回那支的 `make`，工人才接得到重試。
- [x] `apps/api/tests/test_video_shorts_automation.py` 加上這兩種情況的測試。

## Steps

- [x] `TopicFacts` 加 `project_blocked`（`stage == "blocked"` 且沒有待確認的重試），`next_job` 載入時算好。
- [x] `next_job_for` 的 `make` 迴圈跳過它並記 hold。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts_automation.py -q
```

## Notes

- 工人端在 PR（票 `2026-09-28-video-shorts-worker-lab`）已經處理重試：收到卡住那支的 `make` 時，讀 `GET /video/automation/videos?shorts=only&state=needs_you` 的 `retry_request_id`，是新的才繼續，並在 `PUT /video/reviews/{slug}` 帶 `retry_acknowledged_id`。
- 沒有這張票之前的對策：站主在分頁放棄那支（`dropped_at`）或按重試，月曆就會往下走。
- 2026-10-02 (claude-opus-5-5): `TopicFacts.project_blocked` is true when the topic's
  video has `stage == "blocked"` and no retry is waiting for the worker
  (`retry_request_id` set and different from `retry_acknowledged_id`); `_waits_for_owner`
  computes it when `next_job` loads. The make loop skips such a topic with the hold
  「「slug」卡住了，等站主處理」, so the next slot is offered. Tests: the calendar moves past
  a blocked Short and comes back to it on a retry; `_waits_for_owner` for no retry, an
  acknowledged retry, a new retry, a first retry and a non-blocked stage. 29 passed;
  ruff, format and mypy clean.
