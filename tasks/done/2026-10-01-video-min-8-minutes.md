---
id: 2026-10-01-video-min-8-minutes
title: 影片每集至少 8 分鐘（漫劇除外，原來如此事務所也要）
status: done
priority: P2
area: tools
owner: claude-opus-5-5-video-min-length
claimed_at: 2026-10-01T15:41:28Z
created_at: 2026-10-01T15:41:09Z
completed_at: 2026-10-01T16:07:19Z
branch: claude/video-min-8-minutes
depends_on: []
scope:
  - .agents/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/automated.md
  - .agents/skills/youtube-video/references/formats.md
  - .claude/skills/youtube-video/SKILL.md
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/migrations/versions/0117_video_min_8_minutes.py
  - apps/api/tests/test_migration_0117_video_min_8_minutes.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_drama_requests.py
  - apps/api/tests/test_video_series.py
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-settings-tutorial.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/DESIGN.md
  - docs/videos/KNOWLEDGE-STORIES.md
  - docs/videos/README.md
  - docs/videos/so-thats-why/README.md
  - tools/video/assemble/smoke.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/cli.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/explainer.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/narration-locale.test.mjs
  - tools/video/core/stages.test.mjs
  - tools/video/core/state.test.mjs
  - tools/video/dubs/captions-package.test.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/qa/checks.mjs
  - tools/video/qa/checks.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/screencast/screencast.test.mjs
  - tools/video/templates/terminal/terminal.test.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/dubs/dubs.test.mjs
  - tools/video/dubs/freshness.test.mjs
  - tools/video/dubs/plan.test.mjs
  - tools/video/tts/batch-recovery.test.mjs
  - tools/video/tts/tts.test.mjs
---

# 影片每集至少 8 分鐘（漫劇除外，原來如此事務所也要）

## Why

站主 2026-10-01 定：YouTube 影片每集都要 8 分鐘以上，漫劇（單集、長篇作品、一鍵合集）除外；
站主確認「原來如此事務所」（flat-explainer 純旁白解說，技術上是 drama 格式）也要 8 分鐘以上。
之前後台的投影片長度下限可設到 3 分鐘、`lint` 只警告、成片品管不量長度；原來如此事務所預設 3 分、上限 8 分，規格寫 7–9 分。

## Definition of done

- [x] 投影片、螢幕錄影、原來如此事務所估計或量到不足 8 分鐘時，`lint` 報錯、成片品管 `assemble` 項不過；漫劇、品牌故事、合集不受影響。
- [x] 後台投影片長度設定下限 8（API 驗證、DB 約束、表單），正式站既有的低設定由 migration 0117 拉到 8。
- [x] 原來如此事務所的請求與單集作品 8–12 分鐘，沒填長度時從 8 開始；改成解說風格時自動拉到 8，改回漫劇時壓回 8 以內。
- [x] 工人提示詞與長度預設、文件、youtube-video skill 寫明這條規矩。

## Steps

- [x] tools/video：`MIN_EPISODE_MINUTES`／`minEpisodeMinutes()`（schema.mjs）、`needsMinimumLength`（drama.mjs）、lint 與 qa 的檢查、flow.mjs 的長度下限、prompts.mjs。
- [x] API：schemas.py（`EPISODE_MIN_MINUTES`、`EXPLAINER_MAX_MINUTES`、`episode_minutes_problem`）、series.py 的 patch、models.py 約束、migration 0117 與整合測試。
- [x] Web：設定表單下限 8、漫劇請求表單依風格切換長度範圍、五語系標籤。
- [x] 文件與 skill。

## How to verify

```bash
npm run test:tools
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest
```

## Notes

- 測試用範例影片只有幾秒；各測試檔與 `assemble/smoke.mjs` 開頭設 `VIDEO_MIN_EPISODE_MINUTES ??= "0"` 關掉這條規矩，下限本身在 `core/lint.test.mjs` 與 `qa/checks.test.mjs` 測。正式環境不設這個變數。
- 比對方式：每個 `tools/**/*.test.mjs` 檔各在這條分支與 main 的 worktree 跑一次，只看「分支失敗、main 通過」的檔案。先 `npm ci`，不然有些檔案在 main 上就載入失敗，會蓋掉真正的差異。
- migration 0117 的第一版先後兩句 UPDATE，設定 (3, 5) 時會撞舊約束的 min <= max；整合測試抓到後改成一句 `GREATEST`。在本機 PostgreSQL 16 跑過 upgrade → downgrade → upgrade。
- 認領時以 `--force` 蓋過四張還開著的票（2026-09-27-video-drama-room-withdraw-a-one、2026-09-28-drama-preloaded-document-approval-order、2026-09-28-sothatswhy-shorts-from-episode、2026-09-30-video-worker-blocks-on-scene-data）在 schemas.py、lint.mjs、prompts.mjs、so-thats-why/README.md 的範圍；這裡對每個檔只動幾行，合併時注意。
