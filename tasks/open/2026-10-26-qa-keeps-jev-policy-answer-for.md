---
id: 2026-10-26-qa-keeps-jev-policy-answer-for
title: QA keeps Jev's policy answer for films whose site books each Jev request once
status: review
priority: P1
area: tools
owner: claude-opus-5-5-happy-brahmagupta
claimed_at: 2026-10-26T23:04:41Z
created_at: 2026-10-26T23:03:58Z
completed_at:
branch: claude/happy-brahmagupta-ibjkpd
depends_on: []
scope:
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# QA keeps Jev's policy answer for films whose site books each Jev request once

## Why

2026-10-26 C11 UCC remake（`story-everyday-ucc-c11-remake-20261025`）成片：第一次 `qa` 拿到 Jev 的立場判斷（0.55，沒過），接著 `review-push --gate final` 重跑 `qa`，又把同一份請求送給 Jev。有整片預算帳戶的片（每支 `story-everyday-*`）在 API 端每份 Jev 請求只記一筆，第二次回 409 `video_budget_operation_reused`（`apps/api/app/video_automation/admin_api.py`）。`qa` 只記住「答案遺失」（`policy_lost`），沒記住拿到的答案，於是 policy 變成 `the judge call failed`、`who: service`……而 review-push 把它當站主要處理的錯誤停下：這類片的成片永遠送不上去。

## Definition of done

- [x] `qa` 把每次 Jev 的回答存成 `policy_judged`（`request_sha256`、`ok`、`detail`）。
- [x] 只有伺服器回 409 `video_budget_operation_reused`、且記錄的雜湊正是這份請求時，才沿用那個回答；其他情況照舊重問（沒過的判斷下一輪仍重問，既有測試守著）。
- [x] 測試：拿到答案會存、被拒重送時沿用、別份請求的記錄不沿用。
- [x] 中間一輪以別的方式失敗（Jev 連不上、沒權杖、答案遺失、404 等）時，同一份請求的回答照樣留在 qa.json，下一輪被拒重送仍能沿用（獨立審查的第 1 點）。
- [x] 長片時長收據（`docs/videos/long-form/review.md`／`review.json`）重新綁定兩檔：獨立審查 `claude-pr-review-qa-policy-judged-20261026`，兩段都是 PASS - DURATION_ONLY。

## Notes

- `node --test tools/video/qa/*.test.mjs tools/video/review/*.test.mjs tools/video/automation/*.test.mjs`：960 pass。
- C11 的 qa.json 已被第二次的失敗蓋掉；那次的回答（`Jev：符合立場 0.55、有示範：不適用（解說）、建議 0.01、業配 0.09；沒過（符合立場低於 0.6）`）還在當時的 qa 輸出裡，照新格式以同一份請求的雜湊 `c1bbcd70…` 補回 `policy_judged` 後，`review-push --gate final --manual-review` 送出成片（pending，站主決定）。
- 認領時與 `2026-10-26-qa-warns-when-a-long-video`（in-progress，scope 含 `tools/video/qa/cli.mjs`）重疊，用 `--force`：那張的 QA 警告已在 #1862（`0b2ce0ab9`）合併，剩下的「重做 PHP2Shell」不碰 `tools/video/qa/`；本票只改 `policyItem` 與 `heldPolicy` 一段。
- PR：https://github.com/x812033727/travel_scanner/pull/1888
- 審查留下、刻意不改的兩點：(1) 這類片只要旁白與 brief 不變，沒過的判斷會一直沿用，因為站方不收同一份請求；要換答案得改旁白或 brief。(2) 沿用的回答來自本機 qa.json，沒有向伺服器核對；`policy_lost` 原本也是這樣信任的。
- 第一次推上去 CI 紅在 `tools/video/long-form/review.test.mjs`（時長收據綁著 qa 兩檔的雜湊），所以收據跟著這張票一起改。
