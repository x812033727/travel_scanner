---
id: 2026-09-26-video-drama-settings-and-look-gates
title: Video drama: settings row, drama fields and look/storyboard review gates
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-26T01:53:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/migrations/versions/0095_video_drama.py
  - apps/api/app/video_automation
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/models.py
  - apps/api/tests/test_migration_0095_video_drama.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_reviews_integration.py
---

# Video drama: settings row, drama fields and look/storyboard review gates

## Why

漫劇路線（`docs/videos/DRAMA.md`）要伺服器記住站主的媒體設定（圖片與片段用哪家哪個模型、解析度、每月預算、單支上限、judge 門檻、風格預設、聲音池），並多兩種審核關卡：`look`（每個角色選一張設定圖）與 `storyboard`（看分鏡）。現有的 `video_automation_settings` 只有文字階段與旁白；`video_reviews` 的取代規則是「同關卡的待審被新送的取代」（`apps/api/app/video_reviews/admin_service.py` 的 `submit_review`），一個角色一張審核需要 `subject`。這張票是伺服器端其他票的前提，也是唯一會碰 `apps/api/app/models.py` 的票。

## Definition of done

- [ ] migration `0095_video_drama` 在 Postgres 上 upgrade、再 upgrade（冪等）、downgrade 都過；有 `look`／`storyboard` 列時 downgrade 拒絕。
- [ ] `GET/PUT /api/v1/admin/video-automation/settings` 帶 `drama` 物件；沒送 `drama` 的 PUT 保留舊值；`settings_problems` 擋掉退役模型、沒金鑰的供應商、模型不支援的秒數與解析度、不在允許清單的聲音。
- [ ] 工人的 `GET /api/v1/video/automation/settings` 也帶 `drama`。
- [ ] `POST /video/reviews` 收 `gate=look`（帶 `subject`）與 `gate=storyboard`；同關卡同 subject 才互相取代；look 沒有 `choice` 不能核准；storyboard 在 `auto_approve_storyboard` 開且 judge 過時到站自動核准；`files` 上限 48。
- [ ] `uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest` 綠。

## Steps

- [ ] migration：`video_automation_settings` 加 DRAMA.md §設定 的欄位（NOT NULL＋server_default，CHECK 命名 `ck_video_drama_*`）；`video_reviews` 加 `subject String(40)`、放寬 `ck_video_review_gate`。
- [ ] `video_automation/models.py`：欄位與 `DEFAULT_*`；`schemas.py`：`DramaSettings`、`SettingsSave.drama: DramaSettings | None = None`、`SettingsView.media_options`、`style_presets`、`UsageView.media`（先 None，S2 填）。
- [ ] `settings.py`：`settings_values`／`settings_view`／`settings_problems`／`update_settings` 處理 `drama`；`auto_approves_storyboard()` 比照 `auto_approves_audio`。
- [ ] `video_reviews/schemas.py`：`Gate` 加 `look`、`storyboard`；`ReviewIn.subject`；`files` 48。`admin_service.py`：`CHOICE_GATES`、依 subject 取代、`decision_problem` 對 CHOICE_GATES 要求 choice、storyboard 自動核准。
- [ ] 測試：migration 整合測試（照 `.agents/skills/backend-conventions/references/migration-tests.md`）、settings 的問題清單、reviews 的 subject 取代與 choice。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_automation_settings.py tests/test_video_reviews.py -q
RUN_INTEGRATION_TESTS=1 DATABASE_URL=... uv run pytest tests/test_migration_0095_video_drama.py tests/test_video_reviews_integration.py -q
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 文字階段不加新名字（`StageRunIn.stage` 是固定 Literal）：工具把 drama 的提示詞送在 planner／writer／verifier 底下。旁白聲音沿用現有 `voice` 欄位；角色聲音在 `character_voice_pool`。
