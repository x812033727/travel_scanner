---
id: 2026-09-24-video-obs-import
title: 影片產線 T11：匯入 OBS 錄影片段並對齊旁白
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:19Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-pilot-ai-model-choice
scope:
  - tools/video/obs
---

# 影片產線 T11：匯入 OBS 錄影片段並對齊旁白

## Why

需要登入的網站或桌面程式，Playwright 不適合自動操作，由站主用 OBS 錄（1920×1080 畫布、不受 Windows 顯示縮放影響）。工具負責把錄影片段接進自動產線：一場景一段、轉成固定 30 fps、用 `tpad=stop_mode=clone` 或變速對齊旁白。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `video.json` 的場景可以指向一段錄影，assemble 把它轉成與其他片段相同的編碼設定並對齊旁白長度。
- [ ] 錄影秘密清查的檢查表（通知、分頁、帳單、提示字元）在 skill 裡。
- [ ] 用一段實際錄影跑通。

## Steps

- [ ] 錄影片段的格式檢查（解析度、畫格率、長度）。
- [ ] 對齊策略（延長最後一格、變速）與 ffmpeg 參數。

## How to verify

```bash
node --test tools/video/obs/*.test.mjs
```

## Notes
