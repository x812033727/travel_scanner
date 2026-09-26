---
id: 2026-09-26-video-drama-media-api
title: Video drama: media generation API (images, clips, music, judge) behind the video tool token
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-26T01:53:23Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-settings-and-look-gates
scope:
  - apps/api/app/video_media
  - apps/api/migrations/versions/0096_video_media_jobs.py
  - apps/api/app/main.py
  - apps/api/app/cli.py
  - apps/api/Dockerfile
  - .env.example
  - apps/api/tests/test_video_media_catalog.py
  - apps/api/tests/test_video_media_providers.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/api/tests/test_video_media_api.py
  - apps/api/tests/test_video_media_storage.py
  - apps/api/tests/test_video_media_integration.py
  - apps/api/tests/test_migration_0096_video_media_jobs.py
---

# Video drama: media generation API (images, clips, music, judge) behind the video tool token

## Why

漫劇的圖片、片段、音樂都由伺服器代呼叫廠商（金鑰不出 API 容器），工具只持有影片工具權杖，做法比照旁白的 `apps/api/app/video_speech/`。廠商一段片段要 30 秒到 6 分鐘，而 API 沒有背景執行程序，所以做成輪詢驅動的狀態機：工作存 Postgres，工具每次 `GET /jobs/{id}` 就向廠商查一次、完成就串流下載入媒體庫。第一版只接站上已有金鑰的 Gemini 與 MiniMax，不碰 `config.py` 與 `admin/service.py`（正被另一張票鎖住）。

## Definition of done

- [ ] `apps/api/app/video_media/` 提供 `GET /video/media/status`、`POST /images`、`POST /clips`、`POST /music`、`GET /jobs/{id}`、`PUT|GET /files/{slug}/{sha256}`、`POST /judge`，錯誤碼與訊息照 DRAMA.md §伺服器；套件裡只有 `admin_api.py` 出現 `AppError(`（有守門測試）。
- [ ] 預算（片段秒數、圖片、音樂、judge 次數）在呼叫廠商之前預留，超過回 429 `video_media_budget_exhausted`；廠商拒收或判失敗才釋放。
- [ ] 同一支影片重送同一個請求（`request_hash`）回同一個工作；`failed` 三次後 409。
- [ ] API 重啟後 `submitted` 的工作下一次輪詢照常推進；下載邊寫邊算 sha256、驗 magic bytes、單檔與總量上限。
- [ ] `video-media-prune` CLI 與每小時的順手清理會刪過期、已放棄、已上架專案的檔案。
- [ ] Gemini 下載只在主機是釘住的 `generativelanguage.googleapis.com` 時附金鑰。
- [ ] ruff、mypy、pytest 綠；migration `0096_video_media_jobs` 有整合測試。

## Steps

- [ ] `catalog.py`：`MediaModel`、`MEDIA_CATALOG`（模型 id、秒數、解析度、參考圖張數、單價；**對官方頁核對一次再寫**）、`PRICES`。
- [ ] `providers/`：協定與 gemini_images、gemini_video（Omni／Veo 共用 predictLongRunning）、gemini_music（Lyria）、minimax_images、minimax_video；錯誤對映。
- [ ] `models.py`＋migration `0096`：`video_media_jobs`；`jobs.py`：submit／advance／lock／expiry；`storage.py`：`MediaStore(ReviewStore)`、`put_stream`、`sniff_type`、`prune`。
- [ ] `meter.py`：包 `usage_meter` 的計數器（provider 字串 `video-media-*`）、`media_usage_view`。
- [ ] `judge.py`：rubric → JSON（`responseSchema`），片段過大走 Files API。
- [ ] `admin_api.py`＋`schemas.py`；`main.py` 掛 router；`cli.py` 加 `video-media-prune`；`Dockerfile` 的 `mkdir -p`；`.env.example` 的 `VIDEO_MEDIA_*`。
- [ ] 測試：catalog、providers（`httpx.MockTransport`）、jobs（fakeredis）、api（ASGI client）、storage、integration、migration。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_media_*.py -q
RUN_INTEGRATION_TESTS=1 DATABASE_URL=... uv run pytest tests/test_migration_0096_video_media_jobs.py tests/test_video_media_integration.py -q
```

部署後：帶權杖 `GET /api/v1/video/media/status` 看供應商、預算、`store.writable`。

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 合約（工具端照這份做）：參考圖永遠以媒體庫的 sha256 引用；judge 分數 0–10、`pass` 由伺服器依 `judge_min_score` 算；`JobOut.retry_after_seconds` 是輪詢間隔。
