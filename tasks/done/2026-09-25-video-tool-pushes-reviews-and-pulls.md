---
id: 2026-09-25-video-tool-pushes-reviews-and-pulls
title: 影片審核：工具送審與讀回站主的決定
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-25T05:56:05Z
created_at: 2026-09-25T05:12:48Z
completed_at: 2026-09-25T05:56:32Z
branch: claude/video-review-tool
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

- [x] `review-push --slug S [--gate outline|audio|final|publish]`：回報狀態（status 的 checklist，轉成中文標籤），把該關的內容轉成預覽（旁白 AAC 96k、成片 720p H.264 CRF 26＋faststart）、分段上傳（4 MiB）、送審；沒指定就送下一個等待中的關卡。
- [x] `review-pull --slug S`：讀回決定；核准且雜湊與本機檔案一致才寫進 `approvals.json`（附「在 /admin/videos 核准」與時間），大綱記下選的選項；退回印出原因；還有待審時結束碼 3。
- [ ] `status` 在等站主時指向後台頁 → 沒做：`status` 在 `core/state.mjs`（別張票的 scope），現在的 todo 文字仍指向 `approve`；skill 已說明改走 `review-push`／`review-pull`。
- [x] skill（SKILL.md、`automated.md`）改寫四個關卡的做法：一律走後台頁，對話只作備援；順手更新 #743 之後過期的 40 dB 坑。

## Steps

- [x] `tools/video/review/sync.mjs`、`review/cli.mjs` 分派、`cli.mjs` 新增指令與說明、`approvals.mjs` 加 `publish` 關卡（綁 `upload/metadata.json`）、測試 `review/sync.test.mjs`（大綱解析、進度與 Jev 摘要、上傳檢查表、送審與讀回、雜湊不符不記、兩段上傳、沒權杖要站主）。
- [x] `.agents/skills/youtube-video/` 與 `.claude/skills/youtube-video/SKILL.md` 逐字複本。

## How to verify

`npm run test:tools`；對試作片實際送審一次，在後台看到並核准，`review-pull` 之後 `status` 顯示核准。

## Notes

- 依賴 API 那張先合併並部署；實際對試作片送審要等 #744、#746 部署後做，結果記在試作片的票。
- 預覽編碼可換（`ctx.encode`）：CI 沒有 ffmpeg，測試用假的編碼器寫檔。
- 檔案用內容雜湊命名，同一個檔案重送時伺服器直接回 complete，不會重傳。
- 大綱選項從 brief 的 `### 選項 X：標題` 解析，一行說明與開場鉤子一併帶上；「（推薦）」字樣拿掉，避免頁面替站主選邊。
