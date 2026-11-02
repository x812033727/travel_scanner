---
id: 2026-11-02-youtube-reporting-api
title: YouTube Reporting API: daily channel reports kept on the site and read by paired AI tools
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-youtube-reporting
claimed_at: 2026-11-02T17:25:48Z
created_at: 2026-11-02T17:23:43Z
completed_at:
branch: claude/youtube-reporting-api
depends_on: []
scope:
  - apps/api/app/video_youtube/reporting.py
  - apps/api/app/video_youtube/reports.py
  - apps/api/app/video_youtube/admin_reports_api.py
  - apps/api/app/video_youtube/models.py
  - apps/api/app/video_youtube/client.py
  - apps/api/app/video_youtube/connection.py
  - apps/api/app/video_youtube/schemas.py
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/migrations/versions/0145_video_youtube_reports.py
  - apps/api/tests/test_video_youtube_reports.py
  - apps/api/tests/test_migration_0145_video_youtube_reports.py
  - apps/web/app/api/video/youtube-reports
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/components/admin-video-youtube.test.tsx
  - apps/web/components/admin-video-youtube-reports.tsx
  - apps/web/lib/youtube-reports-copy.ts
  - apps/web/lib/youtube-reports-messages
  - tools/video/youtube-reports
  - docs/videos/YOUTUBE-REPORTS.md
  - .agents/skills/youtube-channel-reports
  - .claude/skills/youtube-channel-reports
---

# YouTube Reporting API: daily channel reports kept on the site and read by paired AI tools

## Why

站主要 AI 看得到頻道的數據，才能分析哪些影片、題材、標題縮圖有效，回頭改進。之前站台只有
Data API 的公開計數（Shorts 的 `stats.py`），AI session 手上沒有觀看時間、平均觀看百分比、縮圖
曝光與點閱率、流量來源這些數字。YouTube Reporting API 每天為頻道產生 CSV 報表，但每份只留 60
天、要頻道的 OAuth 授權才拿得到；AI session 不該拿 Google 憑證。所以由站台下載保存，AI 用它已經
有的影片工具權杖（`mkv_`）從站台讀。

## Definition of done

- [x] 連結頻道時同意畫面多要 `yt-analytics.readonly`；卡片分得出授權有沒有 Analytics，沒有時說要重新連結，上架照常。
- [x] 站台為十種頻道報表各建一個 job（每個家族挑 YouTube 提供的、未棄用的最新版本），下載新報表，CSV 原樣 gzip 保存；同一天重新產生時較新的取代較舊的。
- [x] 影片工具權杖能讀 overview（涵蓋日期、欄位、站台影片與 YouTube id 的對照）、觸發同步、讀某家族某段日期（可篩影片）的原始列。
- [x] 伺服器不算任何衍生指標；解除連結或換頻道後，舊報表在下一次讀取時刪除。
- [x] `tools/video/youtube-reports/cli.mjs`：overview、sync（有剩就續跑）、rows（slug 對 id、自動分段）、export。
- [x] 給 AI 的 skill `youtube-channel-reports` 與設計文件 `docs/videos/YOUTUBE-REPORTS.md`。
- [ ] 部署後：站主在 Google Cloud 啟用 YouTube Reporting API、同意畫面加範圍、在卡片「重新連結」，按「立即下載報表」；一兩天後 `overview` 有 30 天的資料。

## Steps

- [x] API：`reporting.py`、`reports.py`、`admin_reports_api.py`、`models.py`、migration 0145、scope。
- [x] 網站轉送與卡片的一段（文案在 `apps/web/lib/youtube-reports-messages`，不動 `messages/*/admin.json`）。
- [x] 工具與測試、skill、文件。
- [ ] 部署與站主重新授權（上面最後一項）。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_youtube_reports.py tests/test_video_youtube.py tests/test_migration_0145_video_youtube_reports.py -q
cd apps/web && npx vitest run components/admin-video-youtube app/api/video/youtube-reports
node --test tools/video/youtube-reports/cli.test.mjs tools/skills.test.mjs
```

部署後：`node tools/video/youtube-reports/cli.mjs sync && node tools/video/youtube-reports/cli.mjs overview`。

## Notes

- 官方文件 2026-11-02 讀過：報表保留 60 天、建 job 時回補 30 天、晚 48–72 小時、太平洋日；2025-06-30 起 a2→a3（`engaged_views`），2026-01-15 加觸及報表。`media.download` 的參考頁 404，照範例直接帶 token GET `downloadUrl`，並只對 `youtubereporting.googleapis.com` 送。
- **還沒有排程**：主機的影片 worker 沒有固定敲 `sync`。`ops/video/worker.sh` 在 `2026-10-24-bug-1-4` 的範圍內（stale 認領），這張票沒動它。該加一行
  `MOKAAIR_SITE="${VIDEO_INTERNAL_SITE:-}" node tools/video/youtube-reports/cli.mjs sync || echo ...`（伺服器自己 12 小時才真的跑一次）；在那之前 60 天內要有人同步一次。
- 解除連結時沒有在 `connection.unlink` 直接刪報表：`tests/test_video_youtube.py`（別張票的範圍）的 SQLite 沒有這三張表。改成每次讀取與同步先 `forget_other_channels`，卡片在解除連結後立刻讀一次。
- `apps/web/messages/*/admin.json` 被 `docs/videos/long-form/review.json` 以雜湊綁住、也在別的票範圍內，卡片步驟 4 那句「只加這一個範圍」沒改，第二個範圍另起一行說明。
- 權杖不另設權限旗標：報表只描述站主自己的頻道，讀它不花錢也不改東西。若站主想限制，照 `colab_access`／`runpod_access` 加一個欄位即可。
