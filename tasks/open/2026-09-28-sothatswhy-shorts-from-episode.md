---
id: 2026-09-28-sothatswhy-shorts-from-episode
title: So That's Why: cut two Shorts from each long episode's keyframes and script
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T09:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/
---

# So That's Why: cut two Shorts from each long episode's keyframes and script

## Why

「原來如此事務所」每集長片搭 2 支 Shorts（濃縮版、一個驚人事實；見 `docs/videos/so-thats-why/README.md` 的 Shorts 一節），要重用長片的關鍵影格，不另外生圖。現在的 `tools/video/shorts/` 只收獨立寫的 JSON：`series` 只能是 `daily|blind|prompts`、素材要是綁 SHA-256 的 evidence、聲音是本機 Windows 聲音，沒辦法從長片的 `video.json` 與關鍵影格切出來，也沒有正式頻道聲音。

## Definition of done

- [ ] Shorts 規格接受 `series: "sothatswhy"`，場景可以引用長片的關鍵影格（直式重新構圖）。
- [ ] 旁白可以用正式頻道聲音（伺服器 TTS）或長片已錄好的句子。
- [ ] 最後一格固定導回長片；說明欄第一行留長片連結的位置。
- [ ] 測試涵蓋新 series 與關鍵影格引用。

## Steps

- [ ] 讀 `tools/video/shorts/core.mjs` 的 schema 與 `docs/videos/ai-shorts/README.md`。
- [ ] 加欄位、構圖、聲音來源；補測試。

## How to verify

`node --test tools/video/shorts/*.test.mjs`；對一支試片跑 `validate` 與 `build`。
