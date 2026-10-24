---
id: 2026-10-24-storyboard-check-passed-problems-manga-details
title: 免關卡漫劇的分鏡永遠不會自動核准：storyboard_check_passed 要每鏡 problems 為空，manga 是非題過關的鏡頭常帶 details 備註
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-24T07:15:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/settings.py
  - apps/api/tests/test_video_automation_settings.py
---

# 免關卡漫劇的分鏡永遠不會自動核准：storyboard_check_passed 要每鏡 problems 為空，manga 是非題過關的鏡頭常帶 details 備註

## Why

《系統說我是 BUG》第 1 集（`xitong-shuo-wo-shi-bug-e001`，免關卡作品）2026-10-24 06:46Z 關鍵影格 46 鏡全部過關、分鏡送審，判分最低 7.33（`judge_min_score` 7、`auto_approve_storyboard` true），卻一直停在 pending 等站主。

`apps/api/app/video_automation/settings.py` 的 `storyboard_check_passed` 對每一鏡要求 `verdict.problems in (None, [])`。#1791 之後 manga 等級的關鍵影格改問是非題（`keyframeChecks`）：重畫級的題（text、anatomy、identity…）答有才算沒過，`details`、`awkward`、`subtitle_band` 是「第二眼才看得到」的扣分題，答有仍可能過關，判詞就留在 `problems`。e001 的 46 鏡裡大多數帶一兩條 `details:` 備註（例：s01「monitor and objects visible on desk top edge」），所以分鏡永遠不自動核准，免關卡的作品每集都要站主手動按。

## Definition of done

- [ ] 免關卡（或開了 `auto_approve_storyboard`）的 manga 漫劇，每鏡 `needs_review` false、分數 ≥ `judge_min_score` 時分鏡自動核准，即使鏡頭帶第二眼扣分題的備註；重畫級的問題仍擋。
- [ ] 舊的打分數路徑（slides、clips 等級）行為不變。
- [ ] `apps/api` 測試涵蓋：帶 `details:` 備註、分數過門檻 → 核准；帶重畫級備註或 `passed: false` → 不核准。

## Steps

- [ ] 決定判準：工人送的 shot 已有 `needs_review` 與 `judge.overall`；manga 是非題時可以改看「分數 ≥ 門檻且 needs_review false」，或由工人在 payload 標出哪些 problems 是重畫級（`keyframeChecks` 的 `cost: 10`）。
- [ ] 改 `storyboard_check_passed`，補測試，跑 `uv run pytest`、`ruff`、`mypy`。
- [ ] 部署後 e001 的分鏡若還 pending，由站主核准或重送。

## How to verify

後台 `GET /api/travel/admin/videos/<slug>` 的 storyboard 審核在送出時就是 approved（備註依作品設定自動核准）。

## Notes

- 發現於票 2026-10-24-bug-1-4（系統說我是 BUG 第 1–4 集的關鍵影格修正）。
