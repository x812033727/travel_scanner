---
id: 2026-09-26-video-stage-instructions-api
title: Video stage instructions: the owner's standing instructions per stage and the prompts the worker last sent
status: done
priority: P1
area: api
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T15:27:35Z
created_at: 2026-09-26T15:26:09Z
completed_at: 2026-09-26T15:41:00Z
branch: claude/video-stage-instructions
depends_on: []
scope:
  - apps/api/migrations/versions/0098_video_stage_instructions.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_automation_ai.py
---

# Video stage instructions: the owner's standing instructions per stage and the prompts the worker last sent

## Why

站主 2026-09-26 問：企劃、劇本、查核、翻譯、字幕審核應該也有可以設定的 UI 吧？現況是各階段只能選模型（AI 設定 › 各功能模型），提示詞本身在 skill 的 Markdown 檔，站主每次都要講的話只能每集在備註重打。站主決定：加「常設指示」（每階段一段文字，工人接在提示詞後面）與「目前的提示詞」唯讀區（工人實際送出的完整指示）。這張票是伺服器端；工具端在 `2026-09-26-video-stage-instructions-tools`，後台頁在 `2026-09-26-video-stage-instructions-ui`。

## Definition of done

- [x] `video_automation_settings.stage_instructions`（JSON，stage → 文字，每段 ≤ 4000 字，去頭尾空白，清空即刪）；設定 API 的讀寫都帶它，舊網頁沒送就保留原值（同 `stage_models`／`drama` 的規則）；工人的 `GET /video/automation/settings` 也帶。
- [x] `POST /video/automation/run` 多收 `format`（預設 slides），把送來的 `instructions` 依（stage, format）存進 `video_stage_prompts`（每組只留最新一份），在跑模型之前就 commit，廠商拒絕也留得下來。
- [x] `GET /admin/video-automation/prompts`（content.read）回 `{prompts:[{stage, format, slug, instructions, sent_at}]}`，依階段順序、投影片在漫劇前。
- [x] migration `0098_video_stage_instructions`：欄位與表都「不存在才建」，downgrade 兩個都刪。

## Steps

- [x] models、schemas、settings、admin_api。
- [x] 測試：驗證與去空、沒送保留、prompts 讀取與排序、run 路由留下提示詞。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_automation_settings.py tests/test_video_automation_ai.py -q
```

## Notes

2026-09-26（claude-fable-5-1-video-drama）：分支 `claude/video-stage-instructions`，三張票同一支 PR。提示詞不能由 API 讀 repo 的 skill 檔（api 映像的 build context 是 `./apps/api`），所以「目前的提示詞」是工人送到 `/run` 時的原文，跑過該階段才有；固定文字改法仍在 `.agents/skills/youtube-video/references/prompts/*.md` 與 `tools/video/automation/prompts.mjs`。部署要跑 0098。
