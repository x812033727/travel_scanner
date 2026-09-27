---
id: 2026-09-26-video-drama-media-api
title: Video drama: media generation API (images, clips, music, judge) behind the video tool token
status: done
priority: P1
area: api
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T04:41:44Z
created_at: 2026-09-26T01:53:23Z
completed_at: 2026-09-26T05:21:16Z
branch: claude/video-drama-media-api
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
  - apps/api/tests/test_video_media_judge.py
  - apps/api/tests/test_migration_0096_video_media_jobs.py
---

# Video drama: media generation API (images, clips, music, judge) behind the video tool token

## Why

漫劇的圖片、片段、音樂都由伺服器代呼叫廠商（金鑰不出 API 容器），工具只持有影片工具權杖，做法比照旁白的 `apps/api/app/video_speech/`。廠商一段片段要 30 秒到 6 分鐘，而 API 沒有背景執行程序，所以做成輪詢驅動的狀態機：工作存 Postgres，工具每次 `GET /jobs/{id}` 就向廠商查一次、完成就串流下載入媒體庫。第一版只接站上已有金鑰的 Gemini 與 MiniMax，不碰 `config.py` 與 `admin/service.py`（正被另一張票鎖住）。

## Definition of done

- [x] `apps/api/app/video_media/` 提供 `GET /video/media/status`、`POST /images`、`POST /clips`、`POST /music`、`GET /jobs/{id}`、`PUT|GET /files/{slug}/{sha256}`、`POST /judge`，錯誤碼與訊息照 DRAMA.md §伺服器；套件裡只有 `admin_api.py` 出現 `AppError(`（`tests/test_video_media_api.py` 的守門測試）。
- [x] 預算（片段秒數、圖片、音樂、judge 次數）在呼叫廠商之前預留，超過回 429 `video_media_budget_exhausted`；廠商拒收或判失敗才釋放（下載失敗不退，因為廠商已計費）。
- [x] 同一支影片重送同一個請求（`request_hash`）回同一個工作（200 而非 202）；`failed` 三次後 409。
- [x] API 重啟後 `submitted` 的工作下一次輪詢照常推進（狀態在 Postgres，Redis 只放 240 秒的鎖）；下載邊寫邊算 sha256、從位元組判型別、單檔與總量上限。
- [x] `video-media-prune` CLI 與每小時的順手清理會刪過期、已放棄、已上架專案的檔案。
- [x] Gemini 下載只在主機是釘住的 `generativelanguage.googleapis.com` 時附金鑰（`GeminiVideo.fetch`）。
- [x] ruff、mypy app 綠；媒體、設定、審核、schema、錯誤訊息測試綠；migration `0096_video_media_jobs` 與工作表的整合測試只在 CI 跑。

## Steps

- [x] `catalog.py`（S1 先建）：`MediaModel`、`MEDIA_CATALOG`、`PRICES`；Veo 的 id 標 preview，實作 T5 第一鏡時核對。
- [x] `providers/`：協定與 gemini_images、gemini_video（Omni／Veo 共用 predictLongRunning）、gemini_music（Lyria）、minimax（image-01 與 Hailuo task）；HTTP 與 `base_resp` 的錯誤對映；下載網址必須是 https 的真實主機。
- [x] `models.py`＋migration `0096`：`video_media_jobs`（含 `request` JSON，重啟後才能重送）；`jobs.py`：submit／advance／lock／expiry／prune；`storage.py`：`MediaStore(ReviewStore)`、`put_stream`、`sniff_type`、`prune_files`。
- [x] `meter.py`：包 `usage_meter` 的計數器（provider 字串 `video-media-*`）、`budgets_view`、`month_usd`、`slug_usd`（`UsageView.media` 給 S4 接後台時再加）。
- [x] `judge.py`：rubric → JSON（`responseSchema`），加權總分伺服器重算；片段超過 20 MB 回 413（Files API 留到需要時再做，T5 先送 720p 代理檔）。
- [x] `admin_api.py`＋`schemas.py`；`main.py` 掛 router；`cli.py` 加 `video-media-prune`；`Dockerfile` 的 `mkdir -p`；`.env.example` 的 `VIDEO_MEDIA_*`；`settings.py` 的 `MediaSettings`（`config.py` 解鎖後併入）。
- [x] 測試：catalog、providers（`httpx.MockTransport`）、judge、jobs（fakeredis＋假廠商）、api（ASGI client）、storage、integration、migration。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_media_*.py -q
RUN_INTEGRATION_TESTS=1 DATABASE_URL=... uv run pytest tests/test_migration_0096_video_media_jobs.py tests/test_video_media_integration.py -q
```

部署後：帶權杖 `GET /api/v1/video/media/status` 看供應商、預算、`store.writable`。

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 合約（工具端照這份做）：參考圖永遠以媒體庫的 sha256 引用；judge 分數 0–10、`pass` 由伺服器依 `judge_min_score` 算；`JobOut.retry_after_seconds` 是輪詢間隔。

- 2026-09-26 做完。給 T2（媒體用戶端）的形狀：`JobOut {id, slug, kind, status, provider, model, seconds, file{sha256,size,content_type}|null, error{code,detail}|null, retry_after_seconds, attempts, polls, usd_estimate, created_at, submitted_at, ready_at, expires_at}`；`JudgeOut {scores, overall, passed, problems, notes, model}`（欄位叫 `passed`，不是 `pass`）；`PUT /files/{slug}/{sha256}?part&parts&size` 與審核的分段上傳相同（4 MiB）；`POST /images` 的 `references[].role` 是 character|style|previous_frame，`POST /clips` 的 `first_frame`／`last_frame` 是 sha256。
- 廠商欄位名（Gemini `predictLongRunning` 的 `instances`／`parameters`、Lyria 的 `responseModalities: AUDIO`、MiniMax `subject_reference`）是依 2026-09-26 的文件寫的；T5 第一鏡先在正式主機單獨跑一次，回應形狀不對就在 adapter 改。
- 有意不做：Files API（judge 只收 20 MB 內的 inline；T5 送 720p 代理檔）、`UsageView.media`（S4 接後台時加）、`video_media` volume（S5，等衝突票；掛上之前檔案在容器層，重部署會掉）。
- 坑：SQLAlchemy 的 python `default=` 只在 flush 時套用，用假 session 的測試會看到 None，所以 `VideoMediaJob(...)` 建構時 `polls=0` 等欄位要寫明。`MediaProvider` 協定的 `name` 要宣告成 property，frozen dataclass 的欄位才符合。
