---
id: 2026-09-27-video-split-settings-api
title: Video split settings API: the drama's own instructions, voice, rounds, gates, models and language defaults
status: done
priority: P1
area: api
owner: codex-p1-audit
claimed_at: 2026-09-29T02:12:00Z
created_at: 2026-09-27T06:16:00Z
completed_at: 2026-09-29T02:12:04Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/video_automation
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/migrations
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_migration_0105_video_split_settings.py
---

# Video split settings API: the drama's own instructions, voice, rounds, gates, models and language defaults

## Why

站主 2026-09-27：「影片審核的漫劇跟教學設定應該也要分開」。伺服器上 `video_automation_settings` 只有一份常設指示、旁白聲音、字幕語系、查核與重錄輪數、旁白與成片的自動核准開關，漫劇與教學共用；設定分頁要拆成三個子分頁各自儲存，`SettingsSave` 卻要求教學的欄位全到。設計在 `docs/videos/DRAMA-FLOW.md` §一（欄位歸屬表、資料模型）。

## Definition of done

- [x] 遷移接在 main 的 head 之後（開票時是 `0101_video_dub_locales`；編號與 scope 裡的測試檔名依實作時的 head 改）：`video_automation_settings` 加 `drama_stage_models`（JSON，NULL）、`drama_stage_instructions`（JSON，`'{}'`，遷移時複製 `stage_instructions`）、`drama_voice`（JSON，NULL）、`drama_caption_locales`（JSON，`'[]'`）、`drama_auto_approve_audio`、`drama_auto_approve_final`（bool，遷移時複製教學的值）、`drama_max_verify_rounds`（3）、`drama_max_retake_rounds`（2），CHECK 同教學的上下限；照 skill `backend-conventions` 寫遷移的整合測試。
- [x] `DramaSettings` 多這些欄位，舊頁面沒送就保留存值（同 `auto_pick_look` 的做法）；`drama_stage_models` 是 `dict[Stage, StageModel] | None`，有值時六個階段都要有；`drama_voice` 走 `_voice_problem`；`settings_problems` 檢查漫劇的模型是廠商有的。
- [x] `SettingsSave` 每個欄位都可省略（省略＝不改），`update_settings` 只覆寫送來的鍵，audit 的 `changed` 照實列；`PUT /settings/models` 也收 `drama_stage_models`（含 `null`）。
- [x] `ai.stage_choice(row, stage, format)`：`format == "drama"` 且 `drama_stage_models` 有值時用它；`run_video_stage` 傳 `request.format`。
- [x] `auto_approves_audio`、`auto_approves_final` 依 `video_projects.format` 讀漫劇的開關（`video_reviews.admin_service.submit_review` 傳 format）。
- [x] `ToolSettingsView` 帶出全部新欄位（工人票 `2026-09-27-video-split-settings-worker` 靠它）。
- [x] 測試：遷移複製值；部分儲存不清掉其他欄位；依格式選模型；依格式的自動核准。

## Steps

- [x] 遷移與 model。
- [x] schemas、settings.py、ai.py、admin_service。
- [x] 測試與檢查。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_automation_settings.py tests/test_video_automation_ai.py tests/test_video_reviews.py tests/test_schema.py tests/test_migration_sql_dialect.py -q
# 要 PostgreSQL（CI 一定跑）：
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_migration_0105_video_split_settings.py tests/test_video_automation_settings.py -q
```

## Notes

- 欄名就是 `DramaSettings` 的鍵（`settings.py` 的 `_flat` 攤到欄位），跟 `drama_enabled`、`drama_aspect` 一樣。
- `drama_topic_scope` 目前工人沒讀（`flow.mjs` 的 `planPayload` 對漫劇也送 `topic_scope`）；改讀的地方在工人票。
- 跟 `2026-09-27-video-drama-room-one-off-series`、`2026-09-27-video-drama-room-messages-api`、`2026-09-27-video-languages-api` 各自帶一支遷移，平行做會撞號，後落地的改號。
- 2026-09-27（claude-fable-5-1-video-split）做完，在分支 `claude/video-review-manga-workflow-fp1rpz`：
  - 遷移是 `0105_video_split_settings`（`down_revision = 0104_video_retry_request`；併 main 時從 0102 重新編號）：八個欄位「不在才加」，`drama_stage_instructions`、`drama_auto_approve_audio`、`drama_auto_approve_final` 只在剛建立時從教學的欄位複製（第二次 upgrade 不會蓋掉站主之後改的值）；CHECK `ck_video_drama_rounds` 與 model 同名。
  - `SettingsSave` 改成每個欄位都可省略、沒有上下限；合併後用 `SettingsWrite` 驗（上下限與一致性都在那裡），驗不過回 422（`admin_api._validated`），不是 500。`SettingsSave.merged_over(current)` 是合併規則：省略或 `null` 保留；`drama` 逐欄合併（`exclude_unset`），所以舊頁面送沒有新欄位的 drama 物件不會重設它們。要讓這件事成立，`DramaSettings` 的八個新欄位都有預設值（舊欄位維持必填）。
  - `PUT /settings/models` 多收 `drama_stage_models`：送 `null` ＝ 跟教學一樣；沒送 ＝ 不改（用 `model_fields_set` 分辨）。
  - `stage_choice(row, stage, format)`：漫劇有自己的模型才用，沒有那一階就退回教學的，再退回預設；`run_stage` 傳 `request.format`。`auto_approves_audio`／`auto_approves_final` 多一個 `format` 參數（預設 `slides`），`submit_review` 傳 `project.format or "slides"`。
  - 測試：`test_video_automation_settings.py`（漫劇模型與聲音的檢查、兩個開關、部分儲存的四種情況、合併後不一致回 422、models 路由的三種送法、工人讀得到）、`test_video_automation_ai.py`（依格式選模型）、`test_migration_0102_video_split_settings.py`（種一列舊形狀的設定 → upgrade 複製 → 第二次 upgrade 不蓋 → downgrade 不動教學欄位）。本機用 scratch 的 PostgreSQL 16 跑過整合測試（CI 是 17）；影片相關 17 個測試檔 196 個案例全過，ruff、mypy app、mypy tests 綠。
  - 接下來：`2026-09-27-video-split-settings-web`（三個子分頁）與 `2026-09-27-video-split-settings-worker`（工人依格式讀值）現在可以認領。web 未落地前，現在的設定分頁照舊送整個物件，行為不變。


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：claude-fable-5-1-video-split；原分支：claude/video-review-manga-workflow-fp1rpz。

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- apps/api/app/video_automation/schemas.py:223 SettingsSave; migration 0105_video_split_settings.py and tests/test_migration_0105_video_split_settings.py present.
- Task Notes contain partial-save validation, independent drama models/voice, integration results; current test_video_automation_settings.py present.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

Close stale review task.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
