---
id: 2026-09-28-video-shorts-automation-api
title: Video shorts A3: the topic library, the weekly plan, the next job and the weekly report on the server
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-shorts-a3
claimed_at: 2026-10-01T13:42:09Z
created_at: 2026-09-28T03:40:00Z
completed_at:
branch: claude/video-shorts-automation-api
depends_on:
  - 2026-09-28-video-shorts-api
scope:
  - apps/api/app/video_shorts/models.py
  - apps/api/app/video_shorts/schemas.py
  - apps/api/app/video_shorts/topics.py
  - apps/api/app/video_shorts/assets.py
  - apps/api/app/video_shorts/jobs.py
  - apps/api/app/video_shorts/plan.py
  - apps/api/app/video_shorts/reports.py
  - apps/api/app/video_shorts/admin_automation_api.py
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/models.py
  - apps/api/migrations/versions
  - apps/api/tests/test_video_shorts_automation.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/api/app/video_shorts/settings.py
  - apps/api/app/video_shorts/slots.py
  - apps/api/app/video_media/jobs.py
  - apps/api/tests/test_migration_0117_video_shorts_topics.py
  - apps/api/tests/test_video_shorts.py
  - apps/api/tests/test_video_shorts_publish.py
  - apps/api/tests/test_video_review_renewal.py
---

# Video shorts A3: the topic library, the weekly plan, the next job and the weekly report on the server

## Why

第二期要讓主機工人自己做 Shorts。工人需要伺服器回答三件事：下一件要做什麼、這一題的規格是什麼、做完寫回哪裡。現在這些都不存在：15 題企劃只在 repo 的 `docs/videos/ai-shorts/campaign/campaign.json`，而工人讀不到 repo 的文件（`video_docs` volume 只在第一次建立時從映像填一次）；伺服器也沒有「下一件工作」的規則，教學影片的排程是工人自己算的。

設計全文在 `docs/videos/SHORTS.md`（§排片與時段、§三條內容線、§端點、§資料模型）。

## Definition of done

- [x] 遷移：新表 `video_shorts_topics`、`video_shorts_assets`、`video_shorts_reports`；`ck_video_stage_prompt_format` 重建成收 `shorts`；`ck_video_stage_prompt_stage` 重建成多收 `subject`。
- [x] `PromptFormat` 加 `shorts`；`StageRunIn.stage` 多收 `subject`，`variant` 是 `a` 或 `b`。`subject` 的供應商與模型來自 `video_shorts_settings.subject_models`，呼叫端不能指定；回應帶實際用的供應商與模型名稱。帶 `variant` 的呼叫不算月草稿數（既有規則），Shorts 另有自己的每月上限。
- [x] 題庫：後台的 `GET`／`POST /admin/video-shorts/topics`、`PATCH …/{slug}`；`POST …/topics/import` 讀一份 `campaign.json` 的內容（請求本體），把 15 題建成 `origin: "campaign"`，重複匯入不會產生第二份；題目的 `brief` 要有測試規格的七個欄位、真值核對、完成條件，缺了就是 `idea` 不是 `ready`。
- [x] 素材：`POST /admin/video-shorts/topics/{slug}/assets`（分段上傳，檔案進媒體庫），必填拍攝者與授權說明；`assets_needed` 都補齊時題目從 `needs_assets` 變 `ready`。
- [x] 自動生題：教學長片公開（有影片 id、`publish_at` 已過）時建立 1–2 筆 `cut` 題目；漫劇的集數成片核准時建立 1 筆 `drama` 題目；`origin: "auto"`，同一個來源不重複。
- [x] `GET /video/automation/shorts/next`（純函式 `next_job_for` 加一層讀寫）：依序回 `report`（週一而且上週的報告還沒寫）、`plan`（週一或庫存低於 `stock_days`，而且下週還有沒排題目的時段）、`brief`（題庫裡可做的題目不夠兩週）、`make`（最早一個排了題目、還沒有影片的時段；帶題目的完整規格、內容線、素材清單、來源影片的資訊、頻道立場），或沒有。Shorts 關著、暫停、預算該停（付費題目）、本月已達上限時不給 `make`。
- [x] 寫回：`POST …/shorts/plan`（檢查每個題目存在而且可做、一格一題、各內容線配額）、`POST …/shorts/topics`（企劃模型的新題目，先存成 `idea`，規格齊了才 `ready`）、`POST …/shorts/{slug}/start`（題目變 `making`、建立影片）、`POST …/shorts/{slug}/done`、`POST …/shorts/report`（一週一份，重送是更新）。
- [x] 每週報告的 `rows` 只存 YouTube 回報的原值與它的來源、讀取時間；伺服器不從這些數字算任何分數、排名或中位數。
- [x] pytest：匯入的冪等、題目狀態的轉換、`next_job_for` 的每一個分支與停止條件、配額、`subject` 的模型選擇與回報、報告的重送。

## Steps

- [x] 讀 `app/video_automation/series.py` 的 `next_job_for`（純函式的寫法）與 `ai.py` 的預算檢查。
- [x] models、遷移、schemas。
- [x] `topics.py`、`assets.py`、`plan.py`、`jobs.py`、`reports.py`。
- [x] `ai.py` 與 `schemas.py` 的 `subject` 階段。
- [x] `admin_automation_api.py`（A1 已經把這個空的路由檔掛進 `main.py`；檔名帶 `admin` 是為了 `tests/test_error_localization.py`）。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_shorts_automation.py tests/test_video_automation_ai.py -q
```

## Notes

- 工人端點的網站轉送在 `2026-09-28-video-shorts-web-routes`，已經照 `SHORTS.md` 的路徑建好；這張票改了路徑的話要回去改那邊。
- 照片可能超過 API 的請求上限（約 5 MiB）與 nginx 的上限：素材上傳用跟審核檔案一樣的分段方式，4 MiB 一段。
- 受測模型用訂閱帳號跑時，既有的 runner 是關掉所有工具、只收文字只回文字；圖片輸入的題目（04、08、10、11）要走有金鑰的視覺模型，這張票先只支援文字與 HTML 產出的題目，圖片題目留 `needs_assets` 並在 Notes 寫下之後要接哪個供應商。
- `GET /video/automation/videos` 的 `shorts=only|exclude` 在 A1。
- 2026-10-01（claude-opus-5-5-shorts-a3）認領時被兩張舊認領擋住：`2026-09-27-video-drama-room-withdraw-a-one`（PR #870 已合併）與 `2026-09-28-drama-preloaded-document-approval-order`（codex-ten-drama，PR #978 已合併），都是範圍重疊的過期認領，所以用 `--force`。
- 做法與決定：
  - 遷移 `0117_video_shorts_topics`：三張新表；`video_shorts_settings` 多 `max_per_month`（預設 60，`ck_video_shorts_settings_month` 0–400）、`last_plan_at`、`last_brief_at`；兩個提示詞 CHECK 照 0109 的做法在原名重建，舊值全保留（遷移測試逐一核對）。降版先刪掉新值的提示詞紀錄（它們只是工人送來的鏡像，0098 的說法）再換回窄的 CHECK。`app/models.py` 不用改：影片的表都在各自模組，0001 也不建它們。
  - 「Shorts 自己的每月上限」做成設定 `max_per_month`：一個月（UTC，跟 AI 用量同一個月）最多開始幾支；`next` 不給新的 `make`、`start` 回 409 `video_shorts_month_full`。已經在做的照樣可以續做。Shorts 的模型呼叫一律要帶 `variant`（`StageRunIn` 驗證），所以永遠不算教學的月草稿數。
  - `subject`：不是 `Stage` 的一員（`Stage` 要求教學設定每個階段都有模型），另立 `RunStage`；只收 `format: shorts`、`variant` a 或 b。模型只從 `video_shorts_settings.subject_models` 來，`b` 沒設就測 `a` 的模型（大多數題目是同一個模型兩種問法），`a` 沒設就 409 `video_ai_subject_not_chosen`，`next` 也不給實測線的 `make`。Shorts 的其他階段先看 `video_shorts_settings.stage_models`，沒有就跟教學。`SettingsWrite` 多 `subject_models` 與 `max_per_month`（W2 的設定畫面直接用 `PUT /admin/video-shorts/settings`），所以 `settings.py` 的 `settings_values` 加了兩行。
  - 題目狀態由內容算：規格缺（實測線缺七欄、真值核對或完成條件；精華與漫劇缺來源影片）是 `idea`；規格齊但缺站主素材或缺網站沒有的工具是 `needs_assets`；其餘 `ready`。`making`／`made`／`dropped` 不再自動變。企劃模型送來的 slug 是新的就建 `planner` 題目，是還在 `idea` 的題目就補上規格（站主的想法由下一輪 `brief` 補完），其餘回 `exists`。
  - 15 題匯入：`campaign.json` 本身沒寫哪幾題要素材或工具，伺服器依代號補（`topics.CAMPAIGN_NEEDS`）：04 三張景點照片＋`vision`、08 靜物原片＋`image_edit`、10 菜單清晰版與反光版＋`vision`、11 手繪線稿＋`vision`＋`sandbox`、05 `sandbox`、12 `image_generation`（付費，受預算管）。結果 10 題 `ready`、5 題 `needs_assets`；重複匯入 0 題新增。
  - 圖片題之後要接的供應商：受測模型要看圖（04、10、11）建議接 Gemini 的看圖模型——網站已經有 Gemini 金鑰，`app/video_media/judge.py` 已經用內嵌圖片（20 MB 內）呼叫它；08 的「修圖」建議走既有的 `/video/media/images`（Gemini 圖片模型帶參考圖），同樣是金鑰計費、受 Shorts 預算管。05 與 11 的成品要執行模型寫的程式並錄手機操作，要先有隔離的執行環境。這些題目在 `requires` 改成支援之前一律停在 `needs_assets`，就算素材補齊也一樣（`topics.UNSUPPORTED`）。
  - 素材：`POST /admin/video-shorts/topics/{slug}/assets?sha256&part&parts&size&need&filename&author&rights_note[&taken_on]`，本體是 4 MiB 以內的一段；每段都要帶拍攝者與授權說明。只收 PNG、JPEG、WebP（看檔頭）。檔案放媒體庫的 `<題目代號>/<sha256>`，工人用 `/video/media/files/...` 讀。媒體庫原本會在 14 天後清掉沒有工作引用的檔案，所以 `video_media/jobs.py` 的 `prune` 改成永遠保留站主的素材（影片公開或放棄後也只清其他檔）。
  - 自動生題：在 `next` 裡做（只有 Shorts 開著時）。教學長片（`slides`、不是 Shorts）有影片 id、`publish_at` 已過而且在 60 天內 → 2 筆 `cut`（`<來源>-cut-1`、`-cut-2`；第二支不能講同一件事，工人找不到值得單獨成片的段落時用 `done` 帶 `outcome: dropped` 放棄）；漫劇集數（`drama`、不是 Shorts）60 天內有核准的 `final` → 1 筆 `drama`（`<來源>-vertical`，付費）。`dedupe_key` 唯一，同一個來源不會再生。60 天是為了第一次部署不要把整個舊片庫變成題目。
  - `next_job_for` 的順序：Shorts 關著什麼都不給；`report`（上週的報告還沒寫，而且開跑日在上週日之前；週一起整週都會給，工人週一停機也不會漏）；`plan`（週一或庫存低於 `stock_days`，本週剩下與下週有空的時段，而且題庫有能排的題目；寫過之後 12 小時內不再給）；`brief`（能排的題目少於兩週配額，或有站主的想法；12 小時一次）；`make`（最早一格排了題目、還沒有影片的時段）。暫停、每月上限、付費題目遇到預算停、實測線沒選受測模型時不給 `make`，原因寫在 `holds`；不花錢的題目照常做。暫停照 DoD 擋 `make`（`settings.py` 的 docstring 說暫停只擋上架，這張票之後製作也停），排片、補題、報告照常。
  - 排片的檢查：時段要是本週剩下或下週的空格，題目要 `ready`、內容線有開、沒排在別的未來時段、付費題目要預算允許；精華與漫劇不能超過自己的每週配額，各週合計不能超過各線配額的總和（沒有來源的線把配額讓給實測）。全部檢查完才寫，錯了整批 422 `video_shorts_plan_invalid`。
  - `start`：題目變 `making`、建立影片（代號用題目代號，被用掉就加 `-2`、`-3`；格式 `shorts`，漫劇線是 `drama`；帶 `shorts_line`、`shorts_series`、`source_slug`）；同一題在做時再叫一次回同一支影片。`done`：`made` 或 `dropped`，重送不變。站主可以放棄在做的題目、之後取回再做（會是新的影片代號）。
  - `slots.assign_approved` 原本不帶題目，做好的 Shorts 會跑去最早的空格而不是排給它的那一格；現在用 `video_shorts_topics.project_slug` 找回題目，進它被排的那一格。因為多讀一張表，三個用 SQLite 建表的測試檔（`test_video_shorts.py`、`test_video_shorts_publish.py`、`test_video_review_renewal.py`）的 `MODELS` 各加了 `VideoShortsTopic`。
  - 每週報告：`rows` 只收引用（影片 id、時間窗、來源），伺服器在收到時照 `video_shorts_metrics` 抄出原值、來源與讀取時間；引用了沒有的快照就 422。請求本體不能帶數字（`ReportRowIn` 是 strict）。同一週重送是更新同一列。伺服器不算任何分數、排名或中位數。
  - 錯誤碼都在 `admin_automation_api.py`（後台檔，免四語）或經 `StageFailed` 轉出，`tests/test_error_localization.py` 照過。
- 驗證：`uv run ruff check .`、`uv run mypy app`、`uv run mypy tests` 全過；`pytest tests/test_video_shorts_automation.py tests/test_video_automation_ai.py tests/test_video_shorts*.py tests/test_schema.py tests/test_error_localization.py tests/test_migration_sql_dialect.py` 全過；`alembic upgrade 0116:0117 --sql` 的離線 SQL 看過。`tests/test_migration_0117_video_shorts_topics.py` 要 PostgreSQL，本機沒有，靠 CI。
- 只在部署（含遷移 0117）之後生效；工人那一端（`shortsStep()`、提示詞、實測製作）是 T2（`2026-09-28-video-shorts-worker-lab`），後台的題庫、素材箱與報告畫面是 W2。
