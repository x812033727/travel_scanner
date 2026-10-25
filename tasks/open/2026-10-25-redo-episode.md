---
id: 2026-10-25-redo-episode
title: 單集漫劇也能用新規則重做：redo_episode 收單集，觀念解說（奇聞檔案局）可以上架的集從故事聖經重做
status: in-progress
priority: P1
area: api
owner: claude-fable-eloquent-hypatia
claimed_at: 2026-10-25T09:50:46Z
created_at: 2026-10-25T09:49:43Z
completed_at:
branch: claude/eloquent-hypatia-fxsz7j
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
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
---

# 單集漫劇也能用新規則重做：redo_episode 收單集，觀念解說（奇聞檔案局）可以上架的集從故事聖經重做

## Why

站主 2026-10-25：「將目前觀念解說的可以上架狀態用新的規則全部重製一次，如果已經有用新的規則就不用重製，
目前已知應該是 s30 跟 h24 而已。」新規則是 #1838（開場五步、說給一個人聽、13 分鐘、4.5 字／秒、燒錄繁中字幕、
bold 縮圖）；PR #1844 的 `curio-h24` 與 `curio-s30-v2` 是第一批照它做的兩集（本機做、推上站），所以站主說的
「已經用新規則的只有 s30 跟 h24」就是這兩支；其他在「可以上架」的觀念解說都還是舊規則。

重做有兩種影片：
1. **主機建的單集**（站主在後台「新的漫劇」建的 cute-mystery／flat-explainer 單集）：`redo_episode` 只收品牌故事與
   作品的集，單集 409 `video_series_redo_story_only`「請放棄那支影片再發起一支」。單集照核准的故事聖經寫，同一份
   聖經用現在的撰稿規則再做一次就是新規則的影片，沒有理由擋。這張票開放它。
2. **容器做、`review-push` 推上站的集**（S 軸 S01–S40 這類在 `docs/videos/` 有自己稿子資料夾的）：沒有作品列，
   沒有重做鈕；照 PR #1844 的做法開新 slug `-v2` 重寫稿子再重做，另開票 `2026-10-25-curio-v2-remake-batch`。

## Definition of done

- [x] 單集頁的那一集（`done`／`started` 有影片，或影片已放棄）有「重做」：伺服器放棄舊影片（工作區與已付費素材留著）、
      集回 `ready`、slug `<planned>-redo<n>`，工人下一輪照 `next_job_for` 從劇本重做；上限照 `STORY_REDO_LIMIT`。
- [x] 重做的單集沒有 queued 請求列：`start_episode` 照這支單集最後一列請求（站主的表單）填 premise、title、
      source_guide、note；長度與畫風用作品列現在的值。
- [x] 長篇動畫仍 409；沒做過影片的單集 409 `video_series_episode_not_dropped`。
- [x] 測試：`apps/api/tests/test_video_drama_redo.py`（單集可以上架 → 重做 → 工人用計畫的 slug 開工 → 新請求列帶表單 →
      第二次 409 limit）、`apps/web/components/admin-video-series.test.tsx`（單集頁的重做與確認文字）。
- [x] 文件：BINGE.md §重做一集、SERIES.md 路由表、curio-episode skill 選路線（`.agents` 與 `.claude` 兩份一致）。
- [ ] 時長收據 DURATION_ONLY 增量由獨立代理 `claude-pr-review-one-off-redo-20261025` 做（series.py、
      admin-video-series.tsx／.test.tsx、五個 admin.json 都在 `REVIEW_FILES`）。
- [ ] 部署後：站主在 `/admin/videos` 把「可以上架」裡分類是觀念解說、由主機建的單集逐支按「重做」
      （要 13 分鐘先 `PATCH …/series/{slug}` 把 `target_minutes` 改 13；後台單集頁目前沒有改長度的欄位）。

## Steps

- [x] 讀 `redo_episode`、`can_redo`、`start_episode`（queued 列的用法）、`drop_project`／`_skip_abandoned_episode`。
- [x] `can_redo` 放行單集；`start_episode` 的 else 分支對單集抄最後一列請求。
- [x] 後台按鈕去掉 `!oneOff`，確認文字分單集版（`redoConfirmOneOff`，五語）。
- [x] `uv run ruff check .`（剩的 6 條都是 `.agents/skills` 底下既有腳本的 RUF100／FURB167／EXE001，不是這張票的檔案）、
      `uv run mypy app`、`uv run mypy tests`、`uv run pytest tests/test_video_drama_redo.py tests/test_video_story_redo.py`；
      `npm run lint:web`、`npm run typecheck:web`、`npm run check:i18n`、vitest `admin-video-series.test.tsx` 32 過；`npm run check:tasks`。
- [ ] `npm run test:tools` 全綠（等收據增量）→ 開 PR。

## How to verify

後台單集頁對一支可以上架的 cute-mystery 單集按「重做」→ 集 `ready`、slug `one-off-…-e001-redo1`、舊影片在影片頁顯示已放棄
（備註「站主重做」）；工人 log「one-off <slug>: <slug>-e001-redo1 started from the approved story bible」；
新請求列的 premise 是站主當初填的前提。`cd apps/api && uv run pytest tests/test_video_drama_redo.py -q`。

## Notes

- 從這個雲端容器讀不到正式站的「可以上架」清單（沒有影片工具權杖、沒有 SSH）；哪些觀念解說還在可以上架要站主在
  `/admin/videos` 看（最上面「可以上架」那組，分類篩「觀念解說」）。repo 能確定的：已上架的 14 支是 H01–H07 v2、L08 v2、
  U02 v2、H10–H12、M09、U09（`channel-review-20261025-story-series`）；S 軸在 10-21 做到上架確認與八語的有 S01 S06 S08 S09
  S11 S14 S18 S38 S39（票 `2026-10-20-remake-ten-curio-episodes-in-the`）與 Codex 的 S02 S03 S04 S05 S23 S26 S28 S30 S34 S40
  （票 `2026-10-21-curio-s02-s03-s04-s05-s23`），這些多半就是可以上架裡的舊規則片；S10 S13 S17 S24 S25 S27 S29 做到哪裡不確定。
- 這張票的 scope 跟 `2026-10-25-drama-series-episodes-can-be-redone`（#1840 已合併，只剩主機上按重做）與多張 in-progress 票
  共用 admin.json 等檔案，用 `--force` 認領。
- `redo_slug` 對單集：`planned` 是第一次開工的 slug（工人固定叫 `<series>-e001`），所以重做叫 `one-off-xxxxxxxx-e001-redo1`。
- 單集的 `target_minutes` 可以 `PATCH`（`patch_series`，解說 8–20），但後台單集頁沒有這個欄位；要 13 分鐘的重做先用 API 改，
  或另開票加欄位。`EXPLAINER_DEFAULT_MINUTES` 仍是 10（#1838 說改它要動時長收據綁的 schemas.py）。
