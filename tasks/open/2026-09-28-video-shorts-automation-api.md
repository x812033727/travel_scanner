---
id: 2026-09-28-video-shorts-automation-api
title: Video shorts A3: the topic library, the weekly plan, the next job and the weekly report on the server
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-28T03:40:00Z
completed_at:
branch:
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
  - apps/api/app/video_shorts/automation_api.py
  - apps/api/app/video_automation/ai.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/models.py
  - apps/api/migrations/versions
  - apps/api/tests/test_video_shorts_automation.py
  - apps/api/tests/test_video_automation_ai.py
---

# Video shorts A3: the topic library, the weekly plan, the next job and the weekly report on the server

## Why

第二期要讓主機工人自己做 Shorts。工人需要伺服器回答三件事：下一件要做什麼、這一題的規格是什麼、做完寫回哪裡。現在這些都不存在：15 題企劃只在 repo 的 `docs/videos/ai-shorts/campaign/campaign.json`，而工人讀不到 repo 的文件（`video_docs` volume 只在第一次建立時從映像填一次）；伺服器也沒有「下一件工作」的規則，教學影片的排程是工人自己算的。

設計全文在 `docs/videos/SHORTS.md`（§排片與時段、§三條內容線、§端點、§資料模型）。

## Definition of done

- [ ] 遷移：新表 `video_shorts_topics`、`video_shorts_assets`、`video_shorts_reports`；`ck_video_stage_prompt_format` 重建成收 `shorts`；`ck_video_stage_prompt_stage` 重建成多收 `subject`。
- [ ] `PromptFormat` 加 `shorts`；`StageRunIn.stage` 多收 `subject`，`variant` 是 `a` 或 `b`。`subject` 的供應商與模型來自 `video_shorts_settings.subject_models`，呼叫端不能指定；回應帶實際用的供應商與模型名稱。帶 `variant` 的呼叫不算月草稿數（既有規則），Shorts 另有自己的每月上限。
- [ ] 題庫：後台的 `GET`／`POST /admin/video-shorts/topics`、`PATCH …/{slug}`；`POST …/topics/import` 讀一份 `campaign.json` 的內容（請求本體），把 15 題建成 `origin: "campaign"`，重複匯入不會產生第二份；題目的 `brief` 要有測試規格的七個欄位、真值核對、完成條件，缺了就是 `idea` 不是 `ready`。
- [ ] 素材：`POST /admin/video-shorts/topics/{slug}/assets`（分段上傳，檔案進媒體庫），必填拍攝者與授權說明；`assets_needed` 都補齊時題目從 `needs_assets` 變 `ready`。
- [ ] 自動生題：教學長片公開（有影片 id、`publish_at` 已過）時建立 1–2 筆 `cut` 題目；漫劇的集數成片核准時建立 1 筆 `drama` 題目；`origin: "auto"`，同一個來源不重複。
- [ ] `GET /video/automation/shorts/next`（純函式 `next_job_for` 加一層讀寫）：依序回 `report`（週一而且上週的報告還沒寫）、`plan`（週一或庫存低於 `stock_days`，而且下週還有沒排題目的時段）、`brief`（題庫裡可做的題目不夠兩週）、`make`（最早一個排了題目、還沒有影片的時段；帶題目的完整規格、內容線、素材清單、來源影片的資訊、頻道立場），或沒有。Shorts 關著、暫停、預算該停（付費題目）、本月已達上限時不給 `make`。
- [ ] 寫回：`POST …/shorts/plan`（檢查每個題目存在而且可做、一格一題、各內容線配額）、`POST …/shorts/topics`（企劃模型的新題目，先存成 `idea`，規格齊了才 `ready`）、`POST …/shorts/{slug}/start`（題目變 `making`、建立影片）、`POST …/shorts/{slug}/done`、`POST …/shorts/report`（一週一份，重送是更新）。
- [ ] 每週報告的 `rows` 只存 YouTube 回報的原值與它的來源、讀取時間；伺服器不從這些數字算任何分數、排名或中位數。
- [ ] pytest：匯入的冪等、題目狀態的轉換、`next_job_for` 的每一個分支與停止條件、配額、`subject` 的模型選擇與回報、報告的重送。

## Steps

- [ ] 讀 `app/video_automation/series.py` 的 `next_job_for`（純函式的寫法）與 `ai.py` 的預算檢查。
- [ ] models、遷移、schemas。
- [ ] `topics.py`、`assets.py`、`plan.py`、`jobs.py`、`reports.py`。
- [ ] `ai.py` 與 `schemas.py` 的 `subject` 階段。
- [ ] `automation_api.py`（A1 已經把這個空的路由檔掛進 `main.py`）。
- [ ] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_shorts_automation.py tests/test_video_automation_ai.py -q
```

## Notes

- 工人端點的網站轉送在 `2026-09-28-video-shorts-web-routes`，已經照 `SHORTS.md` 的路徑建好；這張票改了路徑的話要回去改那邊。
- 照片可能超過 API 的請求上限（約 5 MiB）與 nginx 的上限：素材上傳用跟審核檔案一樣的分段方式，4 MiB 一段。
- 受測模型用訂閱帳號跑時，既有的 runner 是關掉所有工具、只收文字只回文字；圖片輸入的題目（04、08、10、11）要走有金鑰的視覺模型，這張票先只支援文字與 HTML 產出的題目，圖片題目留 `needs_assets` 並在 Notes 寫下之後要接哪個供應商。
- `GET /video/automation/videos` 的 `shorts=only|exclude` 在 A1。
