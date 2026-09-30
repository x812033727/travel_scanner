---
id: 2026-09-28-video-story-light-series-read
title: 故事作品的輕量讀法：清單不帶每個故事的企劃全文
status: done
priority: P3
area: api
owner: claude-fable-5-1-story-read
claimed_at: 2026-09-30T04:08:11Z
created_at: 2026-09-28T15:24:24Z
completed_at: 2026-09-30T04:23:25Z
branch: claude/story-series-light-read
depends_on:
  - 2026-09-28-video-story-admin
scope:
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/tests/test_video_story_admin.py
---

# 故事作品的輕量讀法：清單不帶每個故事的企劃全文

## Why

後台的故事作品頁（票 `2026-09-28-video-story-admin`，`apps/web/components/admin-video-stories.tsx`）讀的是 `GET /admin/video-automation/series/{slug}`，每集都帶 `beats` 全文（六段要點、必查事實、來源、查核者的提醒）。100 個故事匯入後，這一次讀取是 1,197,209 位元組（2026-09-28 在記憶體 SQLite 上用真實的 `stories.json` 量的），而頁面跟其他作品頁一樣每分鐘重讀一次。清單本身只要每個故事的 `id`、`category`、`region`、`publish` 與狀態、影片；企劃全文只有站主打開一個故事時才要。

## Definition of done

- [x] 故事作品有一種讀法，每集只帶清單要的 `beats` 欄位（`id`、`category`、`region`、`subject`、`publish`），回應在 100 個故事時小於 150 KB；原本的讀法不變（工人與其他頁面照舊）。
- [x] 一個故事的企劃全文可以單獨讀（例如 `GET /admin/video-automation/series/{slug}/episodes/{number}`，要 `content.read`）。
- [x] 測試照 `tests/test_video_story_admin.py` 的 SQLite 做法。

## Steps

- [x] 決定參數或新路徑（例如 `?beats=summary`），寫進這張票的 Notes。
- [x] 路由、schema、測試；之後另開 web 的票讓 `admin-video-stories.tsx` 改用它。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_story_admin.py tests/test_video_story.py
```

## Notes

- 量法：`tests/test_video_story_admin.py` 的 `_client` 與 `tests/test_video_story.py` 的 `db`，POST 真實檔案（`apply`、不帶 `limit`）後 `GET /series/brand-stories` 數 `len(response.content)`。
- 影片頁的 `OneOffBible` 也為每一集漫劇（含故事）每分鐘讀一次整部作品，另有票 `2026-09-28-video-page-reads-whole-series-for`。
- 2026-09-30，claude-fable-5-1-story-read 用 `--force` 認領：這個 scope 被 codex-ten-drama 的幾張 `review` 票鎖著（例如 `2026-09-28-drama-manual-edit-structured-data`、`2026-09-28-drama-revised-document-readiness`），認領都超過 24 小時，它們的 PR #978 已在 2026-09-29 合併，沒有人在改這幾個檔。
- 選的做法：同一條路由加查詢參數，`GET /admin/video-automation/series/{slug}?beats=summary`（`schemas.SeriesBeatsRead = Literal["full", "summary"]`，預設 `full`）。summary 時每集的 `beats` 只留 `series.SUMMARY_BEAT_KEYS`＝`id`、`category`、`region`、`subject`、`publish`（有的才留），其餘欄位（狀態、影片、配額、docs）與完整讀法逐欄相同。不帶參數或 `beats=full` 跟以前一樣，工人與漫劇頁不受影響；不認得的值回 422 `validation_error`。
- 單集全文：`GET /admin/video-automation/series/{slug}/episodes/{number}`，要 `content.read`，回一個 `SeriesEpisodeOut`（完整 `beats` 與 `video`），跟完整讀法裡那一集一模一樣；沒有這集回 404 `video_series_episode_not_found`，沒有這部作品回 404 `video_series_not_found`。讀的時候不鎖列（`_episode(..., lock=False)`；寫入路由照舊 `FOR UPDATE`）。
- 量到的大小（2026-09-30，記憶體 SQLite、真實 `docs/videos/story-plans/brand-stories-100/stories.json` 100 個故事、還沒有影片）：完整讀法 1,197,209 位元組，`?beats=summary` 58,767 位元組。測試 `test_the_light_read_of_the_real_backlog_is_under_150_kb` 斷言小於 150,000、完整讀法仍大於 1 MB。
- 留意：每集的 `video`（`ProjectSummary`，估計每支 1–3 KB，未實測）在輕量讀法裡照舊保留。100 個故事都做出影片後，輕量讀法會隨之變大；若超過 150 KB，再讓 summary 也精簡 `video`。
- 內部把 `episode_view` 的 `beats: bool` 改成 `"full" | "summary" | "none"`；工人的 `SeriesContextOut` 仍對故事作品的其他集給空 `beats`（原本的 `beats=False`）。
- web 改用它的票：`2026-09-30-story-admin-page-uses-the-light`（series 讀取其實在 `admin-video-series.tsx`，那張票的 scope 已含它）。
