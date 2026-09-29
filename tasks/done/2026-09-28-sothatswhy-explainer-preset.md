---
id: 2026-09-28-sothatswhy-explainer-preset
title: So That's Why: flat-illustration explainer preset for the drama route (narrator only, all still shots)
status: done
priority: P2
area: tools
owner: claude-opus
claimed_at: 2026-09-28T07:40:48Z
created_at: 2026-09-28T06:00:00Z
completed_at: 2026-09-28T09:34:48Z
branch: claude/knowledge-series-planning-v84n79
depends_on: []
scope:
  - tools/video/core/
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/review/sync.mjs
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/migrations/versions/0109_video_flat_explainer.py
  - apps/api/tests/test_migration_0109_video_flat_explainer.py
  - apps/api/tests/test_video_drama_requests.py
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/
  - .agents/skills/youtube-video/references/drama.md
  - docs/videos/DRAMA.md
  - docs/videos/so-thats-why/README.md
---

# So That's Why: flat-illustration explainer preset for the drama route (narrator only, all still shots)

## Why

「原來如此事務所」（`docs/videos/so-thats-why/README.md`）每集 7–9 分鐘、約 90–120 張插圖，全部是 `visual: "still"` 鏡頭，只有旁白、沒有角色對白、沒有影片片段，畫風是扁平編輯插畫而不是漫劇的 3D 寫實。現在的漫劇路線預設是有角色、有對白、有 clip 的故事，企劃與撰稿提示也是寫故事；每集都手改會漂移。

## Definition of done

- [x] 有一個解說用的風格預設（扁平插畫、固定色盤；不需要角色參考圖，`characters` 留空、只有旁白，畫風見 `docs/videos/so-thats-why/look.md`），`video.json` 可以指定它：`look.preset: "flat-explainer"`。
- [x] 純旁白、全 still 的集數過 `lint`；沒有角色的漫劇跳過 look 步驟與關卡。
- [x] 撰稿提示有「解說」變體（planner／writer／verifier `:explainer`），後台發起時選這個風格就用它。
- [x] 站主在後台選得到（API 的 Literal、三張表的 CHECK＝migration 0109、設定頁與發起表單、五語文案）。
- [x] 有一份 fixture 與測試。

## Steps

- [x] 決定：沿用 `format: "drama"`，新增風格預設 `flat-explainer`，不開新 format（still 鏡頭、合成、字幕、配音全部沿用）。
- [x] tools：預設、`isExplainer`／`hasCast`、lint（無角色、全 still、`big`／`stats`／`compare` 卡、brief 章節）、look 關卡跳過、提示詞變體、工人選 variant、`settle` 固定預設並清空角色。
- [x] API：`STYLE_PRESETS`、`StylePreset`、migration 0109 與整合測試、請求 API 測試。
- [x] 後台：發起漫劇表單與設定頁的選單、五語標籤。
- [x] 文件：`docs/videos/DRAMA.md`、skill 的 `references/drama.md`、系列 README。
- [x] 部署後在後台發起第一集：交給票 `2026-09-28-sothatswhy-pilot-3`。

## How to verify

- `npm run test:tools`；`node tools/video/cli.mjs lint --file tools/video/core/fixtures/explainer/video.json` 零錯誤零警告。
- `cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_drama_requests.py tests/test_video_automation_settings.py`；有 Postgres 時 `RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_migration_0109_video_flat_explainer.py`。
- `npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web`。

## Notes

- 規格來源：`docs/videos/so-thats-why/README.md` 的「一集長什麼樣」「畫面風格」與 `look.md`。
- 系列作品（series、一鍵合集）的表單**不**提供這個預設：系列跑的是有角色的故事提示詞。資料庫與 API 仍接受它（同一份清單），只是後台不給選。
- migration 0109 的 downgrade 在還有列用 `flat-explainer` 時會拒絕（同 0103 的做法），先把那些列改成別的預設。
- 2026-09-28 在本機 Postgres 16 跑過 `alembic upgrade head`、`downgrade -1`、再 `upgrade head`，以及 0105、0103 的整合測試，都綠。
- 2026-09-28 合併 main 時與 main 的 0105–0108 撞號，改成 `0109_video_flat_explainer`（接在 `0108_video_drama_messages` 後）。
- 2026-09-28 再併 main：main 同時合進 `0109_video_shorts` 與 `0111_video_story_series`，兩支都接 0108，main 變成兩個 head（`tests/test_schema.py` 會紅）。0111 改接 `0109_video_shorts`（main 的 #918 也做了同樣的修正，併進來後以 main 為準），這個 PR 自己改號 `0112_video_flat_explainer` 接在 0111 後，測試檔同步改名。上面列的 0109 檔名現在是 0112。
- 2026-09-28 第三次：#927 的 `0112_news_evidence_body_hash` 也接 0111，照站主在 PR 上的指示改號 `0113_video_flat_explainer`，接在 `0112_news_evidence_body_hash` 後，測試檔改名 `test_migration_0113_video_flat_explainer.py`。
