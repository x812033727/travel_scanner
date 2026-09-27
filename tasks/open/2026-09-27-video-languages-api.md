---
id: 2026-09-27-video-languages-api
title: Video languages API: each video's languages (metadata, captions, dub), the languages gate and ready-to-upload
status: review
priority: P1
area: api
owner: claude-fable-5-1-video-languages
claimed_at: 2026-09-27T07:22:30Z
created_at: 2026-09-27T06:16:03Z
completed_at:
branch: claude/video-review-manga-workflow-fp1rpz
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

- [x] 遷移（接 main 的 head；平行的遷移票見 DRAMA-FLOW.md）：`video_projects.locales`（JSON，`'{}'`）、`locales_decided_at`；把 `dub_locales` 搬進 `locales`（三個部件都 true）；已有 `youtube_video_id` 或 `dub_locales` 非空的影片 `locales_decided_at` 設成遷移時間；`ck_video_review_gate` 加 `languages`。`dub_locales` 欄位留著不讀寫。
- [x] `PUT /admin/videos/{slug}/languages` `{"locales": {...}}`：只收 en、ja、ko、zh-CN；每語 `metadata`、`captions`、`dub` 三個布林；`dub` 為 true 時 `captions` 也為 true；漫劇拒收 `dub`；第一次寫 `locales_decided_at`；audit `video_locales_set`；已放棄的影片拒絕。`PUT …/dubs` 拿掉（web 票同步）。
- [x] `Gate` 加 `languages`（`dubs` 留著讓舊列讀得出來）。payload 照 LANGUAGES.md §資料模型；沒有 `dub` 部件的 `languages` 審核送達即核准（備註寫明），有配音的等站主；`decision_problem` 不收選項。
- [x] `ProjectSummary`／`ProjectOut`：`locales`、`locales_decided_at`、`languages`（每語每部件 `ready`｜`working`｜`skipped`｜`uploaded`，從最新 `languages` 審核與 `locales` 算）、`ready_to_upload`（上傳包核准 ∧ 已決定 ∧ 勾了的部件都 ready／skipped／uploaded ∧ 沒有影片 id）；`list_projects` 的排序用它。
- [x] 測試：PUT 的規則、遷移搬家與時間戳、gate 的自動核准、`ready_to_upload` 的五種狀態。

## Steps

- [x] 遷移與 model。
- [x] schemas、admin_service、admin_api。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && PYTHONUTF8=1 uv run pytest tests/test_video_reviews.py tests/test_schema.py tests/test_migration_sql_dialect.py -q
# 只在 CI 跑（要 PostgreSQL）：tests/test_video_reviews_integration.py 與遷移的整合測試
```

## Notes

- `link_youtube` 不變；T8（`2026-09-24-video-youtube-sync`）讀 `ready_to_upload` 決定何時送 `publishAt`。
- api 落地後第二批三支（成片已核准、`locales_decided_at` 為 `null`）會出現在「需要你」等語言決定，這是預期的。
- 2026-09-27（claude-fable-5-1-video-languages）做完，在分支 `claude/video-review-manga-workflow-fp1rpz`（接在設定分開三張票之後）：
  - 遷移是 `0103_video_locales`（`down_revision = 0102_video_split_settings`）：`video_projects.locales`（json，`'{}'`）與 `locales_decided_at`；欄位剛建立時用純 SQL（`json_array_elements_text` ＋ `json_object_agg`，不碰 jsonb 運算子）把 `dub_locales` 搬成三個部件都開的語言，並把已有 YouTube id 或勾過配音的影片標成已決定；`ck_video_review_gate` 重建加 `languages`；downgrade 有 `languages` 審核時拒絕。整合測試 `test_migration_0103_video_locales.py` 在本機的 PostgreSQL 16 跑過（三種影片：勾過配音、已上架、還在做）。
  - `LocalesIn`：`{"locales": {"en": {"metadata", "captions", "dub"}}}`；勾 dub 自動勾 captions；沒勾任何部件的語言丟掉；照頁面順序存；多餘的欄位照其他路由的慣例忽略。`PUT /admin/videos/{slug}/languages`（content.manage）→ `set_locales`：漫劇勾 dub 回 422 `video_locales_dub_not_for_drama`；第一次儲存（含空的「只出繁體中文」）寫 `locales_decided_at`，之後不動；同樣的選擇再存不寫 audit；audit `video_locales_set`；已放棄拒絕。
  - **`PUT …/dubs` 沒拿掉**：舊頁面（web 票落地前）還在用，改成疊在 `locales` 上（勾的語言三個部件都開、取消的只關 dub）；`ProjectSummary.dub_locales` 也改成從 `locales` 推導。web 票把面板換掉之後，這條路由與欄位可以一起刪。`dub_locales` 資料欄不再讀寫。
  - 每支影片的 `languages` 狀態：從 `languages` 審核（pending／approved）由舊到新讀，後一批蓋前一批指名的部件；「ready」／「skipped（原因）」照工人回報，approved 批次裡 ready 的 dub 變 `uploaded`；沒回報的部件是 `working`；被退回的批次不算。`ready_to_upload` ＝ 上傳包核准 ∧ 已決定 ∧ 勾了的部件都不是 working ∧ 沒有影片 id ∧ 沒放棄。列表用一次查詢把所有影片的 `languages` 審核帶進來算。
  - 送審規則：`languages` 批次裡沒有 `dub: "ready"` 的部件就送達即核准（備註「這一批沒有要你上傳的配音，依規則自動核准」）；有配音等站主。payload 兩種寫法都收：部件值是字串（`"ready"`）或 `{status, reason}`，語言層也可放 `reason`。
  - `link_youtube` 不變；T8 讀 `ready_to_upload`。
  - 驗證：ruff、mypy app、mypy tests 綠；影片相關 14 個測試檔（含 `RUN_INTEGRATION_TESTS=1` 的整合測試與三支遷移測試）全過。
  - 接下來：`2026-09-27-video-languages-web`（語言面板、`languages` 卡片、上架卡五個狀態，拿掉 `DubLanguages`／`DubsBody`），然後改寫後的 `2026-09-26-video-dubs-worker`。
