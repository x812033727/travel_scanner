---
id: 2026-10-25-drama-series-episodes-can-be-redone
title: 漫劇作品的集可以用新規則重做：redo_episode 只給品牌故事，《系統說我是 BUG》第 1–4 集重做不了
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-25T04:40:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/tests/test_video_automation_series.py
  - apps/web/components/admin-video-series.tsx
  - docs/videos/BINGE.md
---

# 漫劇作品的集可以用新規則重做

## Why

站主 2026-10-24 看《系統說我是 BUG》第 1 集說單調、節奏慢；三個修正（#1834 policy、#1835 集不包片頭片尾、#1836 manga 運鏡／每 2–3.5 秒一張／說書聲音）2026-10-24 19:47Z 部署後，第 5 集起用新規則做。站主要第 1–4 集也用新規則重做（「等那三個修完再修原本的」）。

但 `apps/api/app/video_automation/series.py` 的 `redo_episode` 只允許品牌故事（`is_story`），漫劇回 409 `video_series_redo_story_only`「漫劇一集接著一集寫，後面的劇情已經當這一集不存在，重做了會接不上」。這個理由對照細綱做的作品不成立：每一集的節拍來自站主核准的篇章文件（`beats`），不是接著前一集即興寫；前情（recap）是從細綱與前一集成片的劇本來的，重做同一集的節拍不會讓後面接不上。

主機上重做一集還有另一條半套路：重跑 `assemble`（新運鏡）再 `final-renewal` 換版，但切法與旁白聲音要新劇本才會變，站主要的是節奏，所以要整集重做。

## Definition of done

- [ ] 作品頁對漫劇的集（`done`／`started`／`skipped` 且開過）有「重做」：伺服器把那一集的舊影片放棄（dropped，工作區與審核紀錄保留，付費檔不重買不刪）、集回到 `ready`、slug 用 `redo_slug`（`<planned>-redo<n>`），工人下一輪照 `next_job_for` 的規則從劇本開始重做（新卡司快照、新規則）；重做次數照 `STORY_REDO_LIMIT`。
- [ ] 合集（`compile`）用重做後的影片：`start_compilation` 給的集列表取每集最新的 `done` 影片（舊的 dropped 不進）。
- [ ] 品牌故事的 redo 行為不變；單集漫劇（one-off）不開放；長篇動畫不開放（有自己的流程）。
- [ ] 測試：漫劇集 redo 後 `status: ready`、`slug` 帶 `-redo1`、舊 request 標 cancelled／dropped；第二次 redo 用 `-redo2`；超過上限 409。
- [ ] 部署後《系統說我是 BUG》第 1–4 集各重做一次，第 5 集之後不動。

## Steps

- [ ] 讀 `redo_episode`、`restore_episode`、`skip_episode`、`finish_episode`、`start_compilation`（`_episodes`／`done` 影片怎麼挑）與 `drop_project`（`video_reviews/admin_service.py`）。
- [ ] 放寬 `redo_episode` 的 `is_story` 檢查為「story 或 production drama series（非 one-off、非長篇動畫）」；漫劇的「已放棄」條件改成：集 `done`／`started` 且有影片 → 先 `drop_project` 那支影片（備註「站主重做」），再照 story 的路徑讓集回 `ready`。
- [ ] 作品頁的集列表加「重做」鈕（五語字串）；`npm run check:i18n`。
- [ ] `uv run pytest`、`ruff`、`mypy`；開 PR。

## How to verify

後台作品頁對第 1 集按「重做」→ 集 `ready`、工人 log「episode 1 (xitong-shuo-wo-shi-bug-e001-redo1) started from the chapter outline」→ 新影片的劇本每鏡 ≤ 3.5 秒、旁白 style 是說書式；合集 dry-run 列的是 `-redo1`。

## Notes

- 發現於票 2026-10-24-bug-1-4（第 1–4 集的卡點紀錄與重做路徑討論）。
- 舊影片 e001／e002／e004 已 `done`（上架確認自動核准，沒上 YouTube），e003 做到一半；重做時這四支的工作區（各 1.5–2 GB）可留給之後清理。
