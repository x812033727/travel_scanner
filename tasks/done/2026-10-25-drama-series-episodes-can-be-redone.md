---
id: 2026-10-25-drama-series-episodes-can-be-redone
title: 漫劇作品的集可以用新規則重做：redo_episode 只給品牌故事，《系統說我是 BUG》第 1–4 集重做不了
status: done
priority: P1
area: api
owner: claude-fable-quizzical-moore
claimed_at: 2026-10-25T04:06:11Z
created_at: 2026-10-25T04:40:00Z
completed_at: 2026-10-25T05:50:36Z
branch: claude/quizzical-moore-a1b717
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/tests/test_video_drama_redo.py
  - apps/api/tests/test_video_story_redo.py
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/BINGE.md
  - docs/videos/SERIES.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# 漫劇作品的集可以用新規則重做

## Why

站主 2026-10-24 看《系統說我是 BUG》第 1 集說單調、節奏慢；三個修正（#1834 policy、#1835 集不包片頭片尾、#1836 manga 運鏡／每 2–3.5 秒一張／說書聲音）2026-10-24 19:47Z 部署後，第 5 集起用新規則做。站主要第 1–4 集也用新規則重做（「等那三個修完再修原本的」）。

但 `apps/api/app/video_automation/series.py` 的 `redo_episode` 只允許品牌故事（`is_story`），漫劇回 409 `video_series_redo_story_only`「漫劇一集接著一集寫，後面的劇情已經當這一集不存在，重做了會接不上」。這個理由對照細綱做的作品不成立：每一集的節拍來自站主核准的篇章文件（`beats`），不是接著前一集即興寫；前情（recap）是從細綱與前一集成片的劇本來的，重做同一集的節拍不會讓後面接不上。

主機上重做一集還有另一條半套路：重跑 `assemble`（新運鏡）再 `final-renewal` 換版，但切法與旁白聲音要新劇本才會變，站主要的是節奏，所以要整集重做。

## Definition of done

- [x] 作品頁對漫劇的集（`done`／`started`／`skipped` 且開過）有「重做」：伺服器把那一集的舊影片放棄（dropped，工作區與審核紀錄保留，付費檔不重買不刪）、集回到 `ready`、slug 用 `redo_slug`（`<planned>-redo<n>`），工人下一輪照 `next_job_for` 的規則從劇本開始重做（新卡司快照、新規則）；重做次數照 `STORY_REDO_LIMIT`。
- [x] 合集（`compile`）用重做後的影片：`start_compilation` 給的集列表取每集最新的 `done` 影片（舊的 dropped 不進）。
- [x] 品牌故事的 redo 行為不變；單集漫劇（one-off）不開放；長篇動畫不開放（有自己的流程）。
- [x] 測試：漫劇集 redo 後 `status: ready`、`slug` 帶 `-redo1`、舊 request 標 cancelled／dropped；第二次 redo 用 `-redo2`；超過上限 409。
- [x] 部署後《系統說我是 BUG》第 1–4 集各重做一次，第 5 集之後不動。

## Steps

- [x] 讀 `redo_episode`、`restore_episode`、`skip_episode`、`finish_episode`、`start_compilation`（`_episodes`／`done` 影片怎麼挑）與 `drop_project`（`video_reviews/admin_service.py`）。
- [x] 放寬 `redo_episode` 的 `is_story` 檢查為「story 或 production drama series（非 one-off、非長篇動畫）」；漫劇的「已放棄」條件改成：集 `done`／`started` 且有影片 → 先 `drop_project` 那支影片（備註「站主重做」），再照 story 的路徑讓集回 `ready`。
- [x] 作品頁的集列表加「重做」鈕（五語字串）；`npm run check:i18n`。
- [x] `uv run pytest`、`ruff`、`mypy`；開 PR。
- [x] 部署後：作品頁對第 1–4 集各按一次「重做」（第 3 集 `started` 也能按），看工人 log 開 `-redo1`。

## How to verify

後台作品頁對第 1 集按「重做」→ 集 `ready`、工人 log「episode 1 (xitong-shuo-wo-shi-bug-e001-redo1) started from the chapter outline」→ 新影片的劇本每鏡 ≤ 3.5 秒、旁白 style 是說書式；合集 dry-run 列的是 `-redo1`。

## Notes

- 發現於票 2026-10-24-bug-1-4（第 1–4 集的卡點紀錄與重做路徑討論）。
- 舊影片 e001／e002／e004 已 `done`（上架確認自動核准，沒上 YouTube），e003 做到一半；重做時這四支的工作區（各 1.5–2 GB）可留給之後清理。
- 2026-10-25 做法（claude-fable-quizzical-moore）：
  - **工人不用改。**工人固定用 `<作品>-e001` 叫 `episodes/{n}/start`（`tools/video/automation/series.mjs` 的 `episodeSlug`），`start_episode` 看到集的 slug 是它的重做（`is_redo_of`）就改用集的 slug；工人的 `draftEpisode` 從回來的 `request.slug` 取工作區名，所以工作區與影片自然叫 `-redo1`。
  - 放棄舊影片走 `drop_project`（審核區預覽清掉、工作區不動）：它會 commit，所以在它之前先算完重做次數與新 slug（上限或 slug 被占就 409，不會先放棄了才拒絕），之後重新鎖作品與集再改狀態。審核區的 `ReviewStore` 由路由懶給（`admin_api._review_store`，只有要放棄時才讀設定）；直接呼叫 `redo_episode` 沒給 store 而影片還在 → 409 `video_series_redo_video_live`。
  - `done` 集的請求列留 `done`（影片做過了），`started` 的標 `cancelled`（`drop_project` → `_skip_abandoned_episode` 做的）；`finished_at` 也清掉。
  - 合集已開始做（`compilation_slug` 有值）就 409 `video_series_compiled`：一部作品只有一部合集，重做的集進不了。
  - `start_compilation` 多查 `VideoProject.dropped_at`：站主直接在影片頁放棄一支 `done` 集的影片，集仍 `done`（`_skip_abandoned_episode` 不動 done），這支不進合集。
  - 時長收據：series.py、admin-video-series.tsx／.test.tsx、五個 admin.json 都在 `REVIEW_FILES`，由獨立代理 `claude-pr-review-drama-redo-20261025` 做 DURATION_ONLY 增量。
  - 沒做：主機上的重做（部署後站主自己按）；e001–e004 工作區清理。
- 2026-10-25 部署與重做（claude-fable-quizzical-moore）：
  - 05:40:47–05:44:18Z 部署 `52628d860`（#1838、#1839、#1840，無 migration，alembic 仍 0139）從 `9e1f2c213`；預檢乾淨（timer 沒裝、鎖空、沒 running 的付費工作、沒有未完成的 cute-mystery 單集）。Auto 模式擋了 `host-deploy.sh`（[Production Deploy]），站主選「按允許、重送」後同一指令通過。`host-verify.sh` 15/15（四項專屬：api `def can_redo(`、`def _review_store(`、合集 `VideoProject.dropped_at.is_not(None)`、工人 `STORY_OPENING_RULE` 6 檔）。
  - 05:47:53–05:48:26Z 在內建瀏覽器的作品頁對第 1、2、3、4 集各按一次「重做」（頁面的 `window.confirm` 先用 JS 改成回 true，不然內建瀏覽器會自動關掉）：四集都回 `ready`、slug `-e00n-redo1`，四支舊影片 `dropped_note` 都是「站主重做」。工人下一輪 log：`series xitong-shuo-wo-shi-bug: episode 1 (xitong-shuo-wo-shi-bug-e001-redo1) started from the chapter outline`，`e001-redo1` 工作區已建（寫手跑中）。第 5 集沒動。
  - 順帶看到：第 5 集（新規則下第一集）卡在 `lint still fails after 3 fixes: characters[3].voice: must be an object with provider and name`，工作區沒有 video.json。不在這張票的範圍，另開票追（重做的四集用同一本設定集 v5，可能撞到同一個問題）。
