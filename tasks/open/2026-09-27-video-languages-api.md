---
id: 2026-09-27-video-languages-api
title: Video languages API: each video's languages (metadata, captions, dub), the languages gate and ready-to-upload
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-27T06:16:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/migrations
  - apps/api/app/video_reviews
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_reviews_integration.py
  - apps/api/tests/test_migration_0105_video_locales.py
---

# Video languages API: each video's languages (metadata, captions, dub), the languages gate and ready-to-upload

## Why

站主 2026-09-27：教學影片先做好繁體中文，再由站主決定要不要做哪些語言（不同語言的標題與說明、CC、配音），決定後再發布。現在五語 CC 與五語說明是全域自動做的，只有配音每支勾（`dub_locales`）。設計在 `docs/videos/LANGUAGES.md`。這張做伺服器端。

## Definition of done

- [ ] 遷移（接 main 的 head；平行的遷移票見 DRAMA-FLOW.md）：`video_projects.locales`（JSON，`'{}'`）、`locales_decided_at`；把 `dub_locales` 搬進 `locales`（三個部件都 true）；已有 `youtube_video_id` 或 `dub_locales` 非空的影片 `locales_decided_at` 設成遷移時間；`ck_video_review_gate` 加 `languages`。`dub_locales` 欄位留著不讀寫。
- [ ] `PUT /admin/videos/{slug}/languages` `{"locales": {...}}`：只收 en、ja、ko、zh-CN；每語 `metadata`、`captions`、`dub` 三個布林；`dub` 為 true 時 `captions` 也為 true；漫劇拒收 `dub`；第一次寫 `locales_decided_at`；audit `video_locales_set`；已放棄的影片拒絕。`PUT …/dubs` 拿掉（web 票同步）。
- [ ] `Gate` 加 `languages`（`dubs` 留著讓舊列讀得出來）。payload 照 LANGUAGES.md §資料模型；沒有 `dub` 部件的 `languages` 審核送達即核准（備註寫明），有配音的等站主；`decision_problem` 不收選項。
- [ ] `ProjectSummary`／`ProjectOut`：`locales`、`locales_decided_at`、`languages`（每語每部件 `ready`｜`working`｜`skipped`｜`uploaded`，從最新 `languages` 審核與 `locales` 算）、`ready_to_upload`（上傳包核准 ∧ 已決定 ∧ 勾了的部件都 ready／skipped／uploaded ∧ 沒有影片 id）；`list_projects` 的排序用它。
- [ ] 測試：PUT 的規則、遷移搬家與時間戳、gate 的自動核准、`ready_to_upload` 的五種狀態。

## Steps

- [ ] 遷移與 model。
- [ ] schemas、admin_service、admin_api。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && PYTHONUTF8=1 uv run pytest tests/test_video_reviews.py tests/test_schema.py tests/test_migration_sql_dialect.py -q
# 只在 CI 跑（要 PostgreSQL）：tests/test_video_reviews_integration.py 與遷移的整合測試
```

## Notes

- `link_youtube` 不變；T8（`2026-09-24-video-youtube-sync`）讀 `ready_to_upload` 決定何時送 `publishAt`。
- api 落地後第二批三支（成片已核准、`locales_decided_at` 為 `null`）會出現在「需要你」等語言決定，這是預期的。
