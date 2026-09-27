---
id: 2026-09-26-video-hands-off-settings
title: 影片交給 AI 決定：頻道立場與自動開關的設定
status: done
priority: P1
area: api
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T22:16:15Z
created_at: 2026-09-26T16:17:36Z
completed_at: 2026-09-26T22:34:17Z
branch: claude/video-hands-off-settings
depends_on: []
scope:
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/models.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/migrations/versions/0100_video_hands_off.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_migration_0100_video_hands_off.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 影片交給 AI 決定：頻道立場與自動開關的設定

## Why

站主 2026-09-27 決定：影片產線除了上架時間，其他決定都交給 AI 或 Jev（設計在 `docs/videos/HANDS-OFF.md`）。第一步是給站主一個地方寫「頻道立場」，再加三個開關，決定哪些關卡可以自動核准。企劃模型寫站主觀點時，頻道立場是唯一的依據；立場還是空白時，不會自動挑大綱。

## Definition of done

- [x] `video_automation_settings` 新增四個欄位。舊網頁沒送這些欄位時保留原值，做法同 `stage_instructions`。
  - `channel_stance`：text，最多 4000 字，去掉頭尾空白；
  - `auto_pick_outline`：預設開；
  - `auto_approve_final`：預設開；
  - `auto_pick_look`：預設關。
- [x] `video_projects` 新增兩個欄位，給「可以上架」清單與 T8 用：
  - `youtube_video_id`：可空，限 11 字元的 YouTube id 格式；
  - `youtube_publish_at`：可空。
- [x] 工具讀取端點 `GET /video/automation/settings` 帶出 `channel_stance` 與三個開關。
- [x] 設定分頁新增「頻道立場」多行欄位與三個開關，文案五種語言。欄位不預填內容；說明文字指向 HANDS-OFF.md 的草稿。

## Steps

- [x] 開工前 `git fetch`，查 main 最新的遷移號碼。等 #814 的 `0098_video_stage_instructions` 合併後才開始，這張接在它後面；檔名以實際號碼為準，scope 跟著改。
- [x] 遷移與遷移測試（照 `test_migration_0097_video_drama_requests.py` 的寫法）。
- [x] schemas、settings 的讀寫與測試。
- [x] 設定分頁與 vitest。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_automation_settings.py tests/test_migration_0100_video_hands_off.py -q
cd apps/web && npx vitest run components/admin-video-settings && npm run lint && npm run typecheck && cd ../.. && npm run check:i18n
```

## Notes

- 遷移編號改成 `0100`：`0099` 被長篇作品的 `0099_video_drama_series`（PR #822，票 2026-09-26-video-series-api）先用了；`down_revision` 接 `0099_video_drama_series`。
- 頻道立場和 #814 的「各階段常設指示」分開：常設指示寫的是怎麼寫，立場寫的是這個頻道相信什麼（HANDS-OFF.md §頻道立場）。
- 部署時要跑遷移；工人與 API 要在同一次部署換成新版。
- 2026-09-27（claude-fable-5-1-video-drama）：做完。`video_projects.youtube_video_id` 本來就有（String(32)，工人的 status upsert 寫入），所以「限 11 字元」做成兩層：`ProjectIn` 的 pattern 改成剛好 11 字（檔案在 hands-off-web 的 scope，只改這一行，已加進本票 scope），DB 加 `ck_video_project_youtube_id`（`char_length = 11`，遷移用 `postgresql_not_valid=True` 建，舊列不回頭檢查、新寫入才擋）。`auto_pick_look` 放在 `drama` 物件裡（舊網頁把整個物件原樣送回，不會被重設）；`channel_stance`、`auto_pick_outline`、`auto_approve_final` 在頂層，`SettingsSave` 沒收到就沿用存的值（跟 `stage_instructions` 同一套）。scope 原本寫的 `apps/api/app/video_reviews/models.py` 不存在，`VideoProject` 在 `apps/api/app/models.py`。遷移測試只在 CI 的 Postgres 跑；本機沒有 PG。
