---
id: 2026-09-28-video-story-api-policy-languages
title: 故事版立場檢查、自動語系、釋放名額、媒體每小時上限與 Flash 單價
status: done
priority: P1
area: api
owner: claude-opus-5-5-video-story-policy
claimed_at: 2026-09-28T11:46:43Z
created_at: 2026-09-28T03:31:13Z
completed_at: 2026-09-28T14:26:42Z
branch: claude/video-story-api-policy-languages
depends_on:
  - 2026-09-28-video-story-api-series-kind
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/catalog.py
  - apps/api/app/video_media/jobs.py
  - apps/api/tests/test_video_story_policy.py
---

# 故事版立場檢查、自動語系、釋放名額、媒體每小時上限與 Flash 單價

## Why

品牌故事要全自動（`docs/videos/STORY.md`），但伺服器有五個地方會讓它停下來或算錯：

1. 成片品管的立場檢查要求「有示範或實算」（`apps/api/app/video_automation/judge.py` 的 policy 題組），那是教學影片的標準；故事沒有示範，每一支都會不過而落回站主。
2. PR #870 之後每支影片都等站主選語系；免關卡的故事沒有人會去選。
3. 站主放棄一支影片時，那一集仍是 `started`，同時進行的名額永遠不釋放。
4. 送圖每小時上限 60、judge 120（`apps/api/app/video_media/admin_api.py`）：一支故事約 120 張圖，光圖片就要兩小時以上。
5. 目錄把 Gemini 3.1 Flash Image 登記成每張 US$0.045（`apps/api/app/video_media/catalog.py`），那是 0.5K 的價格；adapter 只送 `aspectRatio`，實際輸出 1K，官方價目是 US$0.067。帳本與每支上限都會少算三成。

## Definition of done

- [x] 影片屬於 `kind: "story"` 的作品時，立場檢查用故事版題組：照頻道立場寫、留給觀眾一個觀察、沒有投資醫療法律政治建議、沒有業配、沒有貶損特定人；門檻與規則寫成常數並有測試。題組由伺服器從影片所屬的作品決定，工人不能指定。
- [x] 免關卡的故事在開始時由伺服器照設定的字幕語系寫入語系決定，不等站主。
- [x] 放棄一支屬於作品的影片時，那一集標成 `skipped`。
- [x] 送圖與 judge 的每小時上限提高到 240 與 360。
- [x] 媒體工作依影片所屬作品的 `image_model` 決定圖片模型；沒有覆寫時照設定。
- [x] 目錄的 Flash 單價是實際輸出尺寸的價格，備註寫明尺寸與查價日期；`/video/media/status` 的估計跟著對。
- [x] `ruff`、`mypy`、`pytest` 通過（本機的限制見 Notes 最後一條）。

## Steps

- [x] `judge.py`：故事版題組與過關規則；`judge_video_policy` 依作品類型選題組。
- [x] `video_reviews/admin_service.py`：語系自動決定；放棄時釋放名額。
- [x] `video_media`：每小時上限、作品的圖片模型覆寫、目錄單價。
- [x] 測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_story_policy.py tests/test_video_automation_judge.py tests/test_video_media_api.py tests/test_video_reviews.py
```

## Notes

- Jev 只讀文字、不會算數也讀不準日期（`apps/api/app/ai/jev.py` 開頭），題組只問文字判斷；事實對不對是查核階段的事。
- 改單價前再讀一次官方價目頁，數字與日期寫進目錄的備註。2026-09-28 讀到的是：Flash 0.5K US$0.045、1K US$0.067、2K US$0.101、4K US$0.151；Pro 1K–2K US$0.134。
- 如果試作發現 1K 放大後不夠清楚，要在 adapter 送尺寸參數改成 2K；那會讓每支成本從約 US$9 變成約 US$13，改之前先問站主。
- 2026-09-28 認領（claude-opus-5-5-video-story-policy）：`claim` 因為相依的 `2026-09-28-video-story-api-series-kind` 還沒結案而拒絕。那張票的工作已經做完並推上去（PR #910，草稿），它的代理只在等整套測試跑完才 `done`；這個分支從 `origin/claude/video-story-api-series-kind`（`20a5af61`）開出、再併入 main（`5b35df86`），所以用 `--force` 認領。認領前查過：沒有 `policy-languages` 的遠端分支與開著的 PR。之後 #910 在 11:49Z、#918（兩個 alembic head 接成一條、`start_episode` 在鎖住作品列時重查故事配額）在 12:34Z 併進 main，這個分支再併了 main（最後一次是 `b48c8b1b`），PR 只剩這張票的改動。那張票在 main 上仍在 `tasks/open`、狀態 `in-progress`，由它的代理結案。
- **scope 加了 `apps/api/app/video_automation/admin_api.py`**：立場檢查的路由 `judge_video_policy` 在那裡，伺服器要從影片找作品，路由必須把 session 與影片的 slug 交給 `judge_policy`，沒有別的辦法。改動只有那一個呼叫（多了 `session=session, slug=payload.slug`），沒有動 import。這個檔也在 `2026-09-28-video-story-admin-import-api` 的 scope 裡、同時有人在改；兩邊的改動不在同一段。`series.py` 沒有改。
- **立場檢查**：題組由 `judge.policy_questions_for(session, slug)` 決定：影片的 slug 等於某一集的 slug、那一集的作品 `kind` 是 `story`，就問故事版五題；其他影片（教學、長篇漫劇的一集、單集漫劇）照舊問教學的四題，題目、門檻、`note` 一字不變（測試逐字釘住）。`JudgePolicyIn` 不收不認得的欄位，工人送 `questions` 會 422。
  - 故事版五題都是 noul，順序與規則在 `STORY_POLICY_RULE`：`stance` ≥ 0.6（沿用教學原句）、`observation` ≥ 0.6（留給觀眾一個帶得走的觀察，而不是買什麼、做什麼的建議）、`advice` ≤ 0.3（沿用教學原句）、`sponsored` ≤ 0.3（推薦觀眾購買或使用，或讀起來像那家公司自己的廣告；不問「稱讚」，因為故事本來就整支在講一個品牌）、`disparage` ≤ 0.3（嘲弄、辱罵、貶低點名的人、公司或品牌，或用自己的口吻說對方不誠實、無能，而不是轉述判決、官方紀錄或具名來源的說法）。只問措辭，沒有一題問事實、數字或日期（有測試）。
  - 回應 `PolicyVerdict` 多了 `questions`（`tutorial`／`story`）、`observation`、`disparage`；故事的 `demo` 是 null，教學的 `observation`、`disparage` 是 null。故事的 `note` 是「Jev（故事）：符合立場 0.81、留下觀察 0.77、建議 0.05、業配 0.10、貶損 0.02，通過」，沒過時列出哪一項低於或高於門檻。
  - **給 `video-story-worker`**：`tools/video/qa/policy.mjs` 只讀 `passed` 與 `note`，不用改。旁白的 `owner_viewpoint` 取自 `brief.md` 的 `## 站主觀點`；故事版的 stance 題問「照頻道立場與站主觀點寫」，把企劃的 `takeaway` 寫進站主觀點，observation 題比較對得準。
  - 看到但沒改：長篇與單集漫劇的成片仍問「有示範」，照 brief 維持原狀，所以免關卡漫劇的成片 `policy` 項幾乎一定不過、落回站主。另開票 `2026-09-28-video-drama-policy-questions`。
- **語系**：故事影片第一次回報（`PUT /video/reviews/{slug}`，`admin_service.upsert_project`）時，伺服器寫入語系決定，內容就是語言面板對漫劇按「照預設勾選」會得到的：設定裡漫劇的「語言面板預先勾選」`drama_caption_locales`，每個語系勾標題說明與 CC、不勾配音，照頁面順序；空的就是「只出繁體中文」，也算已決定。紀錄跟站主儲存的是同一筆：`video_projects.locales`、`locales_decided_at`、audit `video_locales_set`，`actor_user_id` 是 null，metadata 多了 `"decided_by": "server"`、`"from": "drama_caption_locales"`。只寫一次，已決定的不動，站主之後仍可在面板改。其他影片照舊等站主（有測試：長篇一集、單集、教學，以及回報自稱是故事作品、但伺服器的集數列找不到它的影片）。
  - 判斷方式：回報要帶 `series_slug`（工人本來就會帶，`tools/video/automation/flow.mjs`、`tools/video/review/sync.mjs`），伺服器再用自己的集數列（slug 等於影片 slug 的那一集）確認作品是 `story`。回報不帶 `series_slug` 的故事影片會照舊等站主，不會被誤判成別的。
  - **給站主（部署前）**：STORY.md 要五語 CC，但 `drama_caption_locales` 預設是空的，這樣每個故事都會是「只出繁體中文」。要在漫劇設定的「語言面板預先勾選」勾 en、ja、ko、zh-CN；這也是其他漫劇語言面板「照預設勾選」的預設。
  - **給 `video-story-admin`**：`ProjectSummary` 沒有新欄位；要標示「伺服器決定」可以讀 audit 的 `decided_by`，或把故事作品的影片直接當成已決定。
- **放棄影片**：`drop_project` 放棄的影片若是某一集（回報帶過 `series_slug`，伺服器用 slug 找到那一集，先鎖作品列再鎖集數列，順序同 `series.py`），還沒完成的集數（`planned`、`ready`、`queued`、`started`）標成 `skipped`，寫 audit `video_series_episode_skipped`（metadata 有 `number`、`dropped_video`）；那是作品最後一集時，照 `skip_episode` 的規則把作品標成 `finished`。已經 `done` 的集數（上架確認已核准）維持 `done`。
  - 其他類型不受害：長篇作品的下一集本來就等上一集 done 或 skipped，所以放棄後下一集照常開始，跟在作品頁按「略過」一樣；有測試（第 2 集放棄前第 3 集等著、放棄後開始；第 1 集已 done，放棄它的影片不改狀態）。
  - `finish_if_complete` 與 `EPISODE_OPEN` 在函式裡 import：`series.py` 在模組層 import 了 `admin_service`。
  - **給 `video-story-admin` 與 `video-story-admin-import-api`**：放棄的故事是 `skipped` 而且 `started_at` 有值，所以「恢復略過的故事」（只恢復從沒開始的）不會讓它回來；它的 slug 也已經是 `/admin/videos` 上的一支影片，匯入會把同一個 slug 當成問題。要重做同一個題目，得在企劃清單給它新的 id 與 slug。
  - 看到但沒改：那一集的請求列（`video_drama_requests`）仍是 `started`，後台清單會一直顯示製作中。另開票 `2026-09-28-video-dropped-episode-request`。
- **每小時上限**：圖片另有自己的計數 `video_media_submit_image`，每小時 240（新常數 `IMAGE_SUBMITS_PER_HOUR`）；judge 360。片段與配樂維持共用的 60（`SUBMITS_PER_HOUR`，計數名不變）：它們每一個都要等廠商幾分鐘，60 從來不是瓶頸，而片段是最貴的一種，一起放寬只會讓失控時燒得更快。這是 ticket 沒有明說的決定（ticket 寫「送圖」）。
  - 還限住花費的：每月預算（圖片、judge、片段秒數、配樂），伺服器在呼叫廠商前用 Redis 原子預留，超過就 429，廠商拒絕或失敗才退回（`video_media/meter.py`、`jobs.submit_job`）；每支影片的上限 `max_usd_per_video` 只有工人端擋（`tools/video/media/ledger.mjs` 加總伺服器給的 `usd_estimate`），伺服器不擋。每小時上限只決定失控時多快把月預算燒完：圖片 240 張／時約 US$16（Flash 1K）或 US$32（Pro），judge 360 次／時約 US$3.6；預設的 1,500 張月預算約 6 小時用完（原本 25 小時）。STORY.md 建議把圖片與 judge 的月預算調到各 9,000：Flash 下最多約 US$603＋US$90，那才是一個月的上限。
- **圖片模型**：`jobs.series_image_model(session, slug)`：影片是某一集、作品的 `image_model` 有值，圖片就用它；廠商優先用設定分頁的圖片廠商（它有這個 id 的話），否則用有這個 id 的那個。作品寫入時就擋掉目錄沒有的名字（series-kind 票的 `image_model_problem`）；寫入之後才退役的，送圖時回 422 `video_media_model_not_allowed`，訊息說是作品指定的模型。片段與配樂照設定。
  - **給 `video-story-worker`**：`/video/media/status` 的 `image` 仍是設定分頁的選擇（預設 Pro）。故事的圖片實際用 `job.series.image_model`；工人事前估價（`tools/video/media/stages.mjs` 的 `imagePrice(status)`）、快取鍵與帳本的 model 名，要改用作品的模型，單價在 `status.models.images.<廠商>` 裡查。每個工作回來的 `JobOut.model`、`usd_estimate` 才是實際的。
- **單價**：2026-09-28 用 WebFetch 讀 Google 的 Gemini API 價目頁（`https://ai.google.dev/gemini-api/docs/pricing`，頁面寫 last updated 2026-09-24 UTC）：Flash 0.5K US$0.045、1K US$0.067、2K US$0.101、4K US$0.151；Pro 1K／2K US$0.134、4K US$0.24。跟 brief 與上面那條一樣，沒有差異。圖片生成文件寫 Gemini 3 的圖片模型預設出 1K；adapter（`providers/gemini_images.py`）只送 `aspectRatio`，沒有動，所以兩個都用 1K 價：Flash 改成 US$0.067，Pro 維持 US$0.134；備註寫了尺寸與查價日期。有一個測試釘住 adapter 不送尺寸，之後改尺寸會提醒一起改價。
  - 已經建立的工作的 `usd_estimate` 不回頭改；本月估計（`/video/media/status` 的 `estimated_usd`）是工作列加總，之後的 Flash 工作都用新價。設定分頁的預設是 Pro；如果正式站曾把設定改成 Flash，那些舊工作仍以 US$0.045 計（沒查正式站，這張票不碰正式站）。
- 本機檢查（2026-09-28，Windows，這個分支併過 main `b48c8b1b` 之後）：`uv run ruff check .` exit 0；`uv run mypy app` exit 0（443 個檔案）；`uv run mypy tests` exit 1，只有既有的 `tests/support/e2e_deploy_agent.py:244`（Windows 沒有 `socketserver.UnixStreamServer`，這張票沒動那個檔），改用 CI 的平台 `uv run mypy tests --platform linux` exit 0（325 個檔案）；brief 的四個測試檔 exit 0（64 passed）；整套 `uv run pytest` exit 1：1 failed、3 errors、4,909 passed、415 skipped，失敗的全是 `tests/test_guides_autolink.py`，Windows 的 cp1252 預設編碼讀寫中文（既有的票 `2026-09-26-guides-autolink-tests-windows-encoding`），同一個檔帶 `PYTHONUTF8=1` 重跑 exit 0（6 passed）；`node tools/tasks.mjs check` exit 0。這台沒有 PostgreSQL，`RUN_INTEGRATION_TESTS=1` 的測試只在 CI 跑。
- 反向驗證：把十三處各自改回去（永遠問教學題組、語系對每一種作品都決定、語系不決定、放棄不動集數、done 也改成 skipped、圖片不看作品模型、片段也看作品模型、Flash 回到 US$0.045、圖片回到共用的 60、judge 回到 120、放寬貶損門檻、故事改問教學的業配題、伺服器的決定不標作者），每一處都有新測試變紅，而且紅的是對應的那一個。
