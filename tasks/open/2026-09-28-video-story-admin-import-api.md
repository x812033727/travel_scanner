---
id: 2026-09-28-video-story-admin-import-api
title: 故事企劃清單的後台 API：從頁面匯入、恢復略過的故事
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-video-story-admin-api
claimed_at: 2026-09-28T12:05:07Z
created_at: 2026-09-28T10:56:09Z
completed_at:
branch: claude/video-story-admin-import-api
depends_on:
  - 2026-09-28-video-story-api-series-kind
scope:
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/stories.py
  - apps/api/tests/test_video_story_admin.py
---

# 故事企劃清單的後台 API：從頁面匯入、恢復略過的故事

## Why

站主的原則是一切在後台做、不碰命令列（票 `2026-09-28-video-story-admin`）。票 `2026-09-28-video-story-api-series-kind` 做好了匯入本身（`app/video_automation/stories.py` 的 `import_story_rows`），但只接在主機指令 `python -m app.cli video-story-import` 上；後台沒有端點可以貼上 `stories.json` 試跑再寫入。後台票也要能「恢復」一個略過的故事，現在只有 `POST /admin/video-automation/series/{slug}/episodes/{number}/skip`，沒有反方向。後台票的 Steps 寫明：API 本身缺的另開票，就是這張。

改每日支數不用新端點：`PATCH /admin/video-automation/series/{slug}` 已經收 `episodes_per_day`（1–12，null 表示不限）、`image_model`、`look`，只有故事作品收。

## Definition of done

- [x] `POST /admin/video-automation/series/{slug}/stories/import`：內文是編譯好的 `stories.json` 加 `apply`、`limit`、`episodes_per_day`，回傳 `StoryImportReport.as_dict()` 同樣的欄位；預設試跑；`apply` 要 `content.manage`（建立作品的權限），有問題時不寫入並回 422 帶報告。檔案大小上限寫成常數（100 個故事約 1.3 MB）。
- [x] 恢復略過的故事：`skipped` 且從沒開始過（`started_at` 是 NULL）的集數回到 `ready`；開始過的拒絕並說明；只限故事作品或也給一般作品，實作時決定並寫進 Notes。
- [x] 測試照 `tests/test_video_story.py` 的 SQLite 做法，本機就能跑。
- [ ] `ruff`、`mypy app`、`mypy tests`、`pytest` 通過。

## Steps

- [x] 路由與權限（`require_capability`），沿用 `SeriesRefused` 轉成問題回應的寫法。
- [x] `series.py` 加恢復集數的函式與稽核紀錄。
- [x] 測試：試跑不寫、apply 寫入、壞檔 422、沒有權限 403、恢復與拒絕恢復。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_story_admin.py tests/test_video_story.py
```

## Notes

- 報告欄位與判斷都在 `stories.py`，端點只做轉接；不要在路由裡再寫一次驗證。
- 經網站轉送時注意 `apps/web` 的 BFF 與 nginx 的請求大小上限（後台票負責轉送路由）。
- 2026-09-28 認領（claude-opus-5-5-video-story-admin-api）：`claim` 因為相依的票 `2026-09-28-video-story-api-series-kind` 還沒 `done` 而拒絕。它的 PR #910 已在 2026-09-28T11:49Z squash 合併進 main（`3156370b8`），票只是還在 `tasks/open`、狀態 `in-progress`（它的代理還沒跑 `done`），所以用 `--force` 認領；那張票的 scope 與這張重疊的 `admin_api.py`、`series.py`，內容都已在 main 上，那張票沒有動。原本的計畫是從 #910 的分支開、疊在它上面；開工時 #910 已經合併，所以這個分支直接從 main 開，PR 不帶別人的 commit。
- scope 加了 `apps/api/app/video_automation/stories.py`：匯入的稽核紀錄要記下 `limit`（誰匯入、新增／更新／略過幾列、`limit`），而那筆紀錄是 `import_story_rows` 自己寫的；只在 `metadata_json` 多一個鍵，主機指令的匯入也會一起記下它的 `--limit`，其他行為不變。
- **給票 `video-story-admin`：匯入端點** `POST /admin/video-automation/series/{slug}/stories/import`（頁面經網站轉送打 `/api/travel/admin/video-automation/series/{slug}/stories/import`）。
  - 內文：`{"file": <整份 stories.json 解析後的 JSON>, "apply": false, "limit": null, "episodes_per_day": null}`，後三個可省略；多出的鍵、沒有 `file` 是框架的 422 `validation_error`。`file` 在路由裡不檢查（什麼 JSON 都收），規則全在 `stories.py`：不是物件、壞故事、路徑的 `slug` 不是檔案的 `series.slug`、`limit` 小於 1、`episodes_per_day` 不在 1–12，都變成報告裡的問題。
  - 權限：試跑要 `content.read`（跟讀作品清單一樣）；`"apply": true` 要 `content.manage`（跟建立作品一樣），沒有就 403 `admin_capability_required`，沒有後台角色是 403 `admin_required`。viewer 可以試跑、不能寫入；content 與 owner 都能寫入。不要 step-up：旁邊的作品端點（建立、修改、撤回、略過）都只看能力，step-up 只用在帳號角色、永久停權、清除帳號與資料庫維護（`STEP_UP_SCOPE_CAPABILITY`）。
  - 200 的內文就是 `StoryImportReport.as_dict()`：`series`、`dry_run`、`accepted`、`written`、`series_exists`、`series_created`、`stories_in_file`、`stories_imported`、`create`、`update`、`leave_alone`、`refuse`、`rows`（`create`、`update`、`renumbered`、`unchanged`、`started`、`refused`，都是故事代號）、`series_differs`、`problems`、`notes`。回應的 schema `StoryImportOut` 禁止多餘欄位，`as_dict()` 多一個或少一個鍵，路由的測試就紅。
  - 有任何問題：422 `application/problem+json`，`code` 是 `video_story_import_refused`，`detail` 是「企劃清單有 N 個問題，整份都沒有寫入。第一個：…」，旁邊是報告的全部欄位（`accepted: false`、`written: false`），什麼都沒寫；試跑與 `apply` 一樣。`problems` 與 `notes` 是 `stories.py` 的英文句子，跟主機指令印的一樣。網站的 `api()`（`apps/web/lib/api.ts`）遇到非 2xx 只留 message、status、code，要列出每個問題，頁面得自己讀 422 的內文。
  - 試跑什麼都不寫：沒有作品、沒有集數、沒有稽核紀錄（測試數過前後的列數，新作品與已有的作品都測）。`apply` 寫入時留一筆 `video_story_imported`：`actor_user_id` 是按下的人，`metadata_json` 是 `series_created`、`created`／`updated`／`renumbered`（故事代號）、`left_alone`（數目）、`limit`；建立作品時另有 `video_series_created`，`created_by_user_id` 是同一個人。什麼都沒改的 `apply` 回 `written: false`、不寫稽核，跟主機指令一樣。
  - 漫劇的開關關著時不拒絕，`notes` 會說 “the drama route is switched off…”，跟主機指令一樣（`POST /series` 會 409 `video_drama_disabled`，這裡照的是匯入指令的行為）。兩個人同時第一次寫入同一部作品時，後到的可能是 409 `video_series_slug_taken`（`add_series` 的拒絕）。
- **大小上限** `admin_api.STORY_IMPORT_MAX_BYTES = 4 MiB`（4,194,304 位元組），量的是整個請求內文，超過回 413 `video_story_import_too_large`。main 上真實的 `docs/videos/story-plans/brand-stories-100/stories.json`：磁碟上 1,414,653 位元組；`JSON.stringify({file})` 送出時 1,185,561 位元組，上限是它的 3.5 倍。一路上的關卡：
  - nginx：`ops/nginx/mokaair.conf.example` 在 server 層是 `client_max_body_size 6m`（2026-09-23 的安全審查也記 6m），`/api/` 有 `limit_req zone=mokaair_api burst=20 nodelay` 與 `proxy_read_timeout 300s`。正式站的設定檔是主機自己的，這裡沒有連主機去確認；超過時是 nginx 自己的 413。
  - Next.js：`apps/web/proxy.ts` 的 matcher 排除 `/api`，proxy 不碰這個請求，沒有它的 body 上限。
  - 網站轉送 `apps/web/app/api/travel/[...path]/route.ts`：`API_PROXY_MAX_BODY_BYTES` 預設 5 MiB（`docker-compose.prod.yml` 也是預設 5242880），邊讀邊數，超過回 413 `request_too_large`；回應上限 `API_PROXY_MAX_RESPONSE_BYTES` 10 MiB；上游逾時 `API_PROXY_TIMEOUT_MS` 15 秒（`upstreamTimeout` 只替 translations、media complete、ai-accounts 放寬）。這個 catch-all 已經轉送任何 `admin/...` 路徑，**後台票不必另寫轉送路由**，除非要給匯入更長的逾時。
  - API：`RequestBodyLimitMiddleware`（`API_MAX_REQUEST_BYTES`，預設 5 MiB）超過回 413 `request_too_large`，之後才輪到這個端點的 4 MiB。所以 4–5 MiB 的檔案聽到的是這個端點有名字的 413，更大的是轉送或 middleware 的 413。
  - 時間：記憶體 SQLite 上，真實檔案第一次試跑 1.35 秒（含暖機），之後試跑與寫入每次約 0.1 秒，遠低於轉送的 15 秒。
- **恢復略過的故事** `POST /admin/video-automation/series/{slug}/episodes/{number}/restore`：沒有內文，要 `content.manage`（跟 `/skip` 一樣），回 `SeriesOut`（跟 `/skip` 一樣，帶 `quota`）。函式是 `series.py` 的 `restore_episode`，放在 `skip_episode` 後面，不碰 `start_episode`。
  - **只給故事作品（決定）**：故事彼此獨立，照號碼開始、不等前一個，恢復的故事只是重新排回佇列。長篇漫劇的每一集接著前一集寫、讀前幾集的前情，略過那一集之後做的集數已經當它不存在；恢復後它是最小的待做號碼，會在那些集數之後才做，劇情接不上；作品已經 `finished` 的，還牽涉到合集。單集漫劇只有一集（要重來是撤回）。其他類型回 409 `video_series_restore_story_only`，說明原因；`/skip` 對所有類型不變。
  - 只有 `skipped` 而且 `started_at` 是 NULL 的故事：不是略過的回 409 `video_series_episode_not_skipped`；開始過的（影片放棄時被標成略過，票 `video-story-api-policy-languages` 做的）回 409 `video_series_episode_was_started`，說明寫開始的日期（台北）與影片代號：代號屬於那支放棄的影片，恢復了永遠開始不了，而它又是最小的待做號碼，會卡住後面每一個故事。沒有這一集或這部作品是 404。
  - 恢復後集數是 `ready`。略過它讓作品變成 `finished` 的（略過的是最後一個還開著的故事），作品回到 `active`；暫停的作品維持暫停。稽核 `video_series_episode_restored`：`{number, story, reopened}`。
  - 每日上限與工人：`story_quota` 與 `next_job_for` 都讀資料列，恢復當下就看得到：`quota.ready` 加一，原因從 `none_ready` 或 `not_active` 消失；今天的名額用完時仍是 `per_day`，台北午夜後它是最小的待做號碼就先開始，而且 `start_episode` 開得起來（測試都走過）。PR #918 在 `start_episode` 加的配額重查，恢復的故事一樣要過，測試裡的開始在那個檢查下也成立。
- 驗證：新的 `tests/test_video_story_admin.py` 8 個測試，全部在記憶體 SQLite 上，本機可跑。反向驗證：讓路由一律寫入（`apply=True`）時，試跑的測試在數列數那行變紅。權限與大小上限沒有做反向驗證；它們的測試各自同時測了兩邊：同一個寫入請求 viewer 403、content 200，上限減一 413、剛好等於上限 200。另外用 main 上真實的 `stories.json` 在記憶體 SQLite 上走過端點：試跑 200、問題 0、create 100；`apply`、`limit 2`、每天 1 支建立作品與 2 集；同樣再送一次 `written: false`；不帶 `limit` 補 98 集；再試跑 `leave_alone 100`；稽核三筆（`video_series_created` 與兩筆 `video_story_imported`，`limit` 各是 2 與 null）。
