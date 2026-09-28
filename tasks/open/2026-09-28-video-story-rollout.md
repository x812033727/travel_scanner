---
id: 2026-09-28-video-story-rollout
title: 品牌故事上線：每天一支七天，再調成每天兩支
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-28T03:31:16Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-pilot
  - 2026-09-28-video-story-tidy-finished
scope:
  - docs/videos/STORY.md
---

# 品牌故事上線：每天一支七天，再調成每天兩支

## Why

站主要的是每天兩支。試作（票 `2026-09-28-video-story-pilot`）量過單支之後，還要確認連續運轉撐得住：單一工人、訂閱額度、主機磁碟、站主每天上傳的流程。直接開到兩支，出問題時會一次堆一排卡住的影片。

## Definition of done

- [ ] 每天一支連續七天：每天都有一支進「可以上架」，沒有卡住超過一天的影片，磁碟與額度沒有持續惡化。
- [ ] 每日支數調成 2 之後連續三天都做出兩支。
- [ ] `docs/videos/STORY.md` 記下這十天的數字：每天完成幾支、平均製作時間、每支花費、卡住的原因與處理。
- [ ] 50 天排程的起始日定下來，寫進 `STORY.md` 與企劃清單的 `README.md`。

## Steps

- [ ] 每日支數 1，觀察七天；每天看一次後台與工人日誌。
- [ ] 確認上架後清工作區的票已上線（票 `2026-09-28-video-story-tidy-finished`）。
- [ ] 每日支數 2、同時進行的集數 2，觀察三天。
- [ ] 寫紀錄。

## How to verify

後台「可以上架」每天新增的支數；主機磁碟用量；`/video/media/status` 的本月用量與估計花費；工人日誌沒有重複出現的錯誤。

## Notes

- 同時在做長篇漫劇時，兩條線共用一個工人，故事會被排擠；要不要加第二個工人由站主決定。
- YouTube 對量產內容的政策是最大的外部風險：上架後留意後台通知，任何警告都先停下來問站主。
