---
id: 2026-09-25-video-tool-pushes-reviews-and-pulls
title: 影片審核：工具送審與讀回站主的決定
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-25T05:12:48Z
completed_at:
branch:
depends_on:
  - 2026-09-25-video-review-api-storage-and-endpoints
scope:
  - tools/video/review
  - tools/video/cli.mjs
  - tools/video/core/approvals.mjs
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
---

# 影片審核：工具送審與讀回站主的決定

## Why

站主在 /admin/videos 審核（見 `2026-09-25-video-review-api-storage-and-endpoints`）；本機工具要把每一關的東西送上去、把站主的決定讀回來，核准才會落到 `approvals.json`。

## Definition of done

- [ ] `review-push --slug S [--gate outline|audio|final|publish]`：回報狀態（status 的 checklist），把該關的內容轉成預覽（旁白 AAC、成片 720p H.264＋faststart）、分段上傳、送審。
- [ ] `review-pull --slug S`：讀回決定；核准且雜湊與本機檔案一致才寫進 `approvals.json`（附「後台核准」與時間），大綱記下選的選項；退回印出原因，結束碼 3。
- [ ] `status` 在等站主時指向後台頁。
- [ ] skill（`automated.md`）改寫四個關卡的做法：一律走後台頁，對話只作備援。

## Steps

- [ ] `tools/video/review/sync.mjs`、`cli.mjs` 新增指令、測試。
- [ ] `.agents/skills/youtube-video/` 與 `.claude/skills/youtube-video/SKILL.md` 逐字複本。

## How to verify

`npm run test:tools`；對試作片實際送審一次，在後台看到並核准，`review-pull` 之後 `status` 顯示核准。

## Notes

- 依賴 API 那張先合併並部署。
