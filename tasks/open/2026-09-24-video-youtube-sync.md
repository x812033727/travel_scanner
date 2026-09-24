---
id: 2026-09-24-video-youtube-sync
title: 影片產線 T8：YouTube API 同步五語系中繼資料與 CC
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:17Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-captions-i18n
scope:
  - tools/video/youtube
  - .agents/skills/youtube-video/references/publish.md
---

# 影片產線 T8：YouTube API 同步五語系中繼資料與 CC

## Why

未通過 YouTube 稽核的 API 專案用 `videos.insert` 上傳的影片會被鎖成私人、不能申訴也不能改公開，所以 mp4 由站主在 Studio 上傳；這張只做 API 補齊：`videos.update`（五語系 `localizations`、標籤、分類）、`captions.insert`×5、`thumbnails.set`。一支約 2,100 配額單位，每日預設 10,000。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `youtube-sync --slug <slug> --video-id <id> --dry-run` 印出要送的內容與配額估計；實送需要 `--apply`，且站主已核准、雜湊一致。
- [ ] `videos.update` 先讀現值再合併整段送，帶 `snippet.defaultLanguage`（沒送的欄位會被清掉）。
- [ ] OAuth：桌面應用程式＋loopback，scope 只有 `youtube.force-ssl`；token 存在 `<VIDEO_WORKDIR>/.secrets/`，不進 repo（repo 是公開的）。
- [ ] 兩個實測寫進 `publish.md`：未驗證專案能否對 Studio 上傳的影片 `captions.insert`；中文 CC 語言碼要用 `zh-TW`／`zh-CN` 還是 `zh-Hant`／`zh-Hans`（上傳測試軌後用 `captions.list` 讀回）。
- [ ] 公開與排程仍由站主在 Studio 自己按；工具不改隱私狀態。

## Steps

- [ ] 站主：Google Cloud 專案啟用 YouTube Data API v3、建立「桌面應用程式」OAuth 用戶端（OAuth 在「測試中」狀態時 refresh token 7 天過期）。
- [ ] `tools/video/youtube/`：OAuth、請求組裝（純函式＋測試）、dry-run。
- [ ] 用試作影片（私人）實測。

## How to verify

```bash
node --test tools/video/youtube/*.test.mjs
node tools/video/cli.mjs youtube-sync --slug ai-model-choice --video-id <id> --dry-run
```

## Notes
