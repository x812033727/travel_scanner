---
id: 2026-09-28-video-shorts-api
title: Video shorts A1: Shorts on the server: projects, slots, metrics, costs, settings and the auto-approval rule
status: done
priority: P1
area: api
owner: claude-fable-5-1-shorts
claimed_at: 2026-09-28T03:39:52Z
created_at: 2026-09-28T03:10:00Z
completed_at: 2026-09-28T05:16:27Z
branch: claude/video-shorts-api
depends_on: []
scope:
  - apps/api/app/video_shorts/__init__.py
  - apps/api/app/video_shorts/models.py
  - apps/api/app/video_shorts/schemas.py
  - apps/api/app/video_shorts/settings.py
  - apps/api/app/video_shorts/slots.py
  - apps/api/app/video_shorts/costs.py
  - apps/api/app/video_shorts/rules.py
  - apps/api/app/video_shorts/overview.py
  - apps/api/app/video_shorts/errors.py
  - apps/api/app/video_shorts/admin_api.py
  - apps/api/app/video_shorts/admin_publish_api.py
  - apps/api/app/video_shorts/admin_automation_api.py
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/app/admin/operations_service.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/judge.py
  - apps/api/migrations/versions
  - apps/api/tests/test_video_shorts.py
  - apps/api/tests/test_video_shorts_integration.py
  - apps/api/tests/test_migration_0109_video_shorts.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_automation_judge.py
  - apps/api/tests/test_admin_operations.py
  - docs/videos/SHORTS.md
---

# Video shorts A1: Shorts on the server: projects, slots, metrics, costs, settings and the auto-approval rule

## Why

站主 2026-09-28 決定在 `/admin/videos` 加一個 Shorts 分頁，而且要全自動：製作、品管、排時段、上架都不等站主。現在 Shorts 只有本機產線（PR #871 的 `tools/video/shorts`），伺服器完全不認得它：

- `video_projects.format` 只收 `slides` 與 `drama`（CHECK、`VideoFormat`、清單的 `format` 參數都寫死這兩個值）。
- 沒有時段、沒有成效、沒有花費帳；排程與追蹤都靠 repo 外的 CSV。
- 成片的自動核准只認長片的 11 項品管，Shorts 永遠過不了。
- `list_projects` 只回最新的 200 支，後台清單與工人讀的清單都是它。90 天 120 支 Shorts 加進來，教學影片與漫劇會被擠出清單。

這張票是其他 Shorts 票的地基。設計全文在 `docs/videos/SHORTS.md`（站主的決定、名稱、狀態、品管項目、排片規則、資料模型、端點都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [x] 遷移（編號接當時的 head；今天 main 是 `0104_video_retry_request`，PR #870 先合併的話從 `0109` 起；一律「不存在才建」；revision id 不超過 32 個字元）：
  - `video_projects`：`ck_video_project_format` 照 `0095`、`0099` 的寫法重建成收 `shorts`；新增 `shorts_line`（CHECK `lab`、`cut`、`drama`）、`shorts_series`、`source_slug`。
  - 新表 `video_shorts_settings`（一列）、`video_shorts_slots`、`video_shorts_metrics`、`video_shorts_costs`，欄位照 `SHORTS.md` §資料模型。
  - 降級在有任何 `format = 'shorts'` 或 `shorts_line` 不是空的影片時拒絕。
- [x] `VideoFormat` 加 `shorts`；`ProjectIn` 收 `shorts_line`、`shorts_series`、`source_slug`（省略就保留原值）；`ProjectSummary`／`ProjectOut` 帶出這三欄加 `shorts_state` 與 `slot_at`。
- [x] 清單：`GET /admin/videos` 與工人的 `GET /video/automation/videos` 都收 `shorts=only|exclude`，`format` 參數收 `shorts`；不帶參數時行為不變。`shorts=only` 時另收 `state=` 與 `limit`／`before`，已公開的預設只回最近 60 支。
- [x] `judge.py`：`SHORTS_QA_ITEMS`（12 項）、`SHORTS_PACKAGE_ITEMS`（4 項）、`shorts_qa_passed(payload, sha)`；`submit_review` 對 `shorts_line` 不是空的影片的 `final` 與 `publish` 審核套用它們，開關讀 `video_shorts_settings.auto_approve`；每筆自動核准寫 `video_review_auto_approved`。報告的 `kind` 不是 `shorts`、少一項、雜湊不對，都不過。長片與合集的規則一個位元組都不變。
- [x] 成片審核的 `payload.usage`（工具回報的旁白秒數與字數、各階段的呼叫次數）在核准時寫進 `video_shorts_costs`；同一份成片重送不會重複記帳。
- [x] 時段：`campaign/start` 照 `daily_pattern` 與 `slot_times` 建出時段（預設 30／45／45 共 120 格，Asia/Taipei）；`assign_slot`（純函式）把核准的 Shorts 指到它排定的那一格，或最早的空格；`lock_due`（純函式）在時段前 `lock_hours` 鎖定，沒有排定的影片時從片庫補，片庫空就記 `missed`。
- [x] `shorts_state`（純函式）算出 `SHORTS.md` §一支 Shorts 的一生 的八種狀態。
- [x] 後台端點（明確宣告 capability）：`overview`、`slots`（GET、PATCH）、`costs`（GET、POST）、`metrics`（GET）、`settings`（GET、PUT，`settings.manage`）、`campaign/start`、`autopublish`（POST、DELETE，`settings.manage`）、`pause`、`resume`。授權記下同意的人、時間、條文雜湊、範圍與到期日；範圍變了（頻道、內容線、每天上限、時段）授權自動失效。
- [x] `admin_publish_api.py` 與 `admin_automation_api.py`（原本寫的是 `publish_api.py`、`automation_api.py`，改名的原因見 Notes）先建成空的路由檔並掛進 `main.py`，之後 Y1 與 A3 各改自己的檔，不用再動 `main.py`。
- [x] 花費：`reserved` 轉 `confirmed` 是更新同一筆；有 `unknown` 或到上限時 `overview` 回報付費工作該停，數字照 `SHORTS.md` §花費與預算。
- [x] 側欄的待辦數字把 Shorts「需要你」裡不是審核的項目（授權到期、連續錯過時段）也算進去，快取的鍵換版本。
- [x] pytest 涵蓋：格式與篩選、清單上限、品管規則（全過、少一項、舊工具、雜湊不符、長片不受影響）、時段建立、指派與鎖定、狀態、授權的失效條件、花費的上限與不重複記帳；遷移有整合測試（先刪、升級、再升級一次、降級）。

## Steps

- [x] 先讀 skill `backend-conventions`（遷移編號、CHECK 重建、整合測試的慣例）。
- [x] 查 main 的 head 與開著的 PR 佔了哪些遷移編號。
- [x] models、遷移、schemas。
- [x] `rules.py`（狀態、指派、鎖定、預算，都是純函式）、`slots.py`、`costs.py`、`settings.py`。
- [x] `judge.py` 的常數與規則、`admin_service.submit_review` 的分支、清單的篩選。
- [x] `admin_api.py` 與兩個空的路由檔，在 `main.py` 註冊。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_shorts.py tests/test_video_reviews.py tests/test_video_automation_judge.py tests/test_admin_operations.py -q
```

整合測試（遷移、端點）要 PostgreSQL，交給 CI 的 `api` 工作。

## Notes

- 新模組放 `apps/api/app/video_shorts`，設定用自己的表：不要加欄位到 `video_automation_settings`，PR #870 正在改那張表與它的儲存方式。
- 路徑式的權限檢查沒有列影片的路徑，沒宣告 capability 的後台路徑會落到 `roles.manage`；每個端點都要自己宣告 `content.read`、`content.manage` 或 `settings.manage`。
- `AppError` 只在檔名含 `admin` 的檔或 `*_api.py` 的後台路由裡用；模組丟 `ShortsRefused`（`errors.py`）。不這樣做，`test_error_localization.py` 會要求四語訊息。
- audit 的 metadata 鍵名不要含 `token`、`secret`、`password`、`api_key`：顯示時會被濾掉。
- JSON 欄位是 `json` 不是 `jsonb`；新的 NOT NULL 欄位要有 `server_default`。
- 提示詞的格式（`PromptFormat`、`ck_video_stage_prompt_format`）在 `2026-09-28-video-shorts-automation-api` 放寬，這張票不動。
- 這張票不碰 YouTube：送出、認領、成效讀取在 `2026-09-28-video-shorts-youtube-auto`。它用到的表（`video_shorts_metrics`）在這裡建好。
- 題庫、素材、每週報告的表在 `2026-09-28-video-shorts-automation-api`。
- 遷移整合測試的檔名跟著編號走；認領時把那個檔名加進 scope。

做完之後（2026-09-28）：

- 遷移是 `0109_video_shorts`，接在 PR #870 的 `0108_video_drama_messages` 後面。除了票上列的，還多了 `video_projects.youtube_removed_at`（Y1 每 30 天驗證時寫）與設定表的 `consent_id`、`last_tick_at`、`last_tick`，讓 Y1 不用為了幾個欄位再開一支遷移。
- **路由檔改名**：`tests/test_error_localization.py` 只靠檔名裡有沒有 `admin` 分辨後台的錯誤碼，`publish_api.py` 裡丟的 `AppError` 會被要求補四語訊息。所以兩個空的路由檔叫 `admin_publish_api.py`、`admin_automation_api.py`；Y1 與 A3 的票、`SHORTS.md` 一起改了。
- **成效表的欄位叫 `period`**，不是 `window`：`window` 是 PostgreSQL 的保留字，手寫的 SQL 每次都要加引號。
- **時段的唯一索引是部分索引**（`uq_video_shorts_slot_project`，只算狀態不是 `missed`、`skipped` 的列）：錯過的那一格留著當時排的代號，Shorts 的狀態才算得出「錯過時段」，它也才能再被排進下一格。
- **CHECK 算出 NULL 會放行**：`status <> 'unknown' AND amount >= 0` 在 `amount` 是 NULL 時整個式子是 NULL，資料庫照收。花費表的 CHECK 把 `IS NOT NULL` 明寫出來，SQLite 的測試與 PostgreSQL 的遷移測試都種了一列去撞它。
- 多了票上沒寫的端點：`PATCH`／`DELETE /admin/video-shorts/costs/{id}`（不然 `unknown` 的帳補不了金額，付費工作會一直停著）、工具讀的 `GET /video/automation/shorts/settings`（T1 合成旁白前要知道聲音；A2 的票補了對應的轉送路由）。
- Shorts 不等語言面板：`ready_to_upload` 對 Shorts 只看上傳包核准、沒有影片 id、沒有被放棄。語言來自 Shorts 設定的 `locales`。
- 用 `format: "shorts"` 回報卻沒帶 `shorts_line` 會被拒絕（422 `video_shorts_line_missing`）：清單靠 `shorts_line` 分辨 Shorts，少了它那支影片會混進「影片」分頁。
- 規劃時漏掉的一件事：第一期沒有任何一張票讓工人呼叫 `tick`（原本寫在第二期的 T2）。補進 T1 了，T2 的票也跟著改。
- 旁白的價目是 2026-09-28 讀官方定價頁的數字，2027-01-01 起價格加倍，兩段都寫在 `costs.py`。
- 側欄的數字多算的是「需要你」裡不是審核的項目，一項算一，不是一支影片算一（「等你上傳 5 支」是一項）。
- 本機沒有 PostgreSQL：`test_migration_0109_video_shorts.py` 與 `test_video_shorts_integration.py` 只在 CI 跑過。整合測試整個包在一個會回滾的交易裡，因為設定只有一列、月曆只有一張表，留在共用的測試資料庫會影響別的測試。
