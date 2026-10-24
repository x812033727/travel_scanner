---
id: 2026-10-24-storyboard-check-passed-problems-manga-details
title: 免關卡漫劇的分鏡永遠不會自動核准：storyboard_check_passed 要每鏡 problems 為空，manga 是非題過關的鏡頭常帶 details 備註
status: in-progress
priority: P1
area: api
owner: claude-opus-5.5
claimed_at: 2026-10-24T08:05:34Z
created_at: 2026-10-24T07:15:00Z
completed_at:
branch: claude/sad-hertz-987888
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

- [x] 免關卡（或開了 `auto_approve_storyboard`）的 manga 漫劇，每鏡 `needs_review` false、分數 ≥ `judge_min_score` 時分鏡自動核准，即使鏡頭帶第二眼扣分題的備註；重畫級的問題仍擋。
- [x] 舊的打分數路徑（slides、clips 等級）行為不變。
- [x] `apps/api` 測試涵蓋：帶 `details:` 備註、分數過門檻 → 核准；帶重畫級備註或 `passed: false` → 不核准。

## Steps

- [x] 決定判準：工人送的 shot 已有 `needs_review` 與 `judge.overall`；manga 是非題時可以改看「分數 ≥ 門檻且 needs_review false」，或由工人在 payload 標出哪些 problems 是重畫級（`keyframeChecks` 的 `cost: 10`）。
- [x] 改 `storyboard_check_passed`，補測試，跑 `uv run pytest`、`ruff`、`mypy`。
- [ ] 部署後 e001 的分鏡若還 pending，由站主核准或重送。

## How to verify

後台 `GET /api/travel/admin/videos/<slug>` 的 storyboard 審核在送出時就是 approved（備註依作品設定自動核准）。

## Notes

- 發現於票 2026-10-24-bug-1-4（系統說我是 BUG 第 1–4 集的關鍵影格修正）。
- 2026-10-24 claude-opus-5.5 的判準（只改伺服器，工人不用改）：
  - 重畫級與第二眼的分別，伺服器自己就有：是非題的分數在 `app/video_media/judge.py` 算，`cost: 10` 的題答有，該項 0 分、低於 4 分的地板，`passed` 就是 false；工人把 `passed` false 的鏡頭送成 `needs_review: true`（`tools/video/review/sync.mjs` storyboardSubmission）。所以 `needs_review` false 的鏡頭本來就沒有重畫級的錯。
  - 但光看 `needs_review` 不夠：clips 等級的打分數路徑，一鏡可以過關但某項低於門檻（≥ 4）而列出問題，現在擋、票要它照擋。所以要知道這一鏡是用是非題判的。
  - 伺服器知道作品的 `visual_tier`；manga 的關鍵影格一律問是非題（keyframes.mjs `checks = (slides || isCuteExplainer(doc) || manga) && limits.judge_checks`，伺服器永遠給 `judge_checks: 1`）。`auto_approves_storyboard` 本來就會讀作品那一列（開關開時看長篇動畫、關時看免關卡），不多查一次，只把 `visual_tier == "manga"` 傳進 `storyboard_check_passed(..., second_look_remarks=True)`。
  - 第二眼的題用問題行開頭的鍵認：`judge.py` `_line` 自己寫 `f"{key}: "`，不是模型的自由文字。允許的鍵是 manga 會問的 `details`、`awkward`、`subtitle_band`（`SECOND_LOOK_CHECKS`）；`generated` manga 不問（craft false），沒放。其他鍵、沒有 `key: ` 的行、非字串一律擋（工人哪天加新題，預設是等站主）。
  - 分鏡層的 `judge.problems` 照舊要空（工人只放待修鏡頭的問題）。slides 不傳這個參數，行為不變；沒有作品的 drama、clips／hybrid／stills 等級也不變。
  - 核准備註原本寫「沒有列出問題」，manga 帶備註過關時就不是真的，改成「沒有要重畫的問題」（`AUTO_APPROVED_STORYBOARD_NOTE`，測試都比對常數）。
  - 規則只在送審時判（`app/video_reviews/admin_service.py` submit_review）。e001 已經 pending 的那一份部署後不會自己變 approved：要站主按，或工人重送分鏡。
