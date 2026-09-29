---
id: 2026-09-28-video-story-light-series-read
title: 故事作品的輕量讀法：清單不帶每個故事的企劃全文
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-28T15:24:24Z
completed_at:
branch:
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

- [ ] 故事作品有一種讀法，每集只帶清單要的 `beats` 欄位（`id`、`category`、`region`、`subject`、`publish`），回應在 100 個故事時小於 150 KB；原本的讀法不變（工人與其他頁面照舊）。
- [ ] 一個故事的企劃全文可以單獨讀（例如 `GET /admin/video-automation/series/{slug}/episodes/{number}`，要 `content.read`）。
- [ ] 測試照 `tests/test_video_story_admin.py` 的 SQLite 做法。

## Steps

- [ ] 決定參數或新路徑（例如 `?beats=summary`），寫進這張票的 Notes。
- [ ] 路由、schema、測試；之後另開 web 的票讓 `admin-video-stories.tsx` 改用它。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_story_admin.py tests/test_video_story.py
```

## Notes

- 量法：`tests/test_video_story_admin.py` 的 `_client` 與 `tests/test_video_story.py` 的 `db`，POST 真實檔案（`apply`、不帶 `limit`）後 `GET /series/brand-stories` 數 `len(response.content)`。
- 影片頁的 `OneOffBible` 也為每一集漫劇（含故事）每分鐘讀一次整部作品，另有票 `2026-09-28-video-page-reads-whole-series-for`。
