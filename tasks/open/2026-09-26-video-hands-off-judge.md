---
id: 2026-09-26-video-hands-off-judge
title: 影片交給 AI 決定：Jev 挑大綱、成片品管的自動核准規則
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-26T16:18:27Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-hands-off-settings
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_automation_judge.py
  - apps/api/tests/test_video_reviews.py
  - apps/web/app/api/video/automation/judge
---

# 影片交給 AI 決定：Jev 挑大綱、成片品管的自動核准規則

## Why

選大綱改由 Jev 決定，看成片改由自動品管決定（`docs/videos/HANDS-OFF.md` §Jev 挑大綱、§自動品管）。判斷與核准規則都在伺服器端，和旁白、分鏡的自動核准用同一套做法：工具送來的 payload 帶著判斷結果，伺服器依規則在送達時核准。

## Definition of done

- [ ] `POST /video/automation/judge/outline`（影片工具權杖）：
  - 收 `slug`、`brief`，以及 2–3 個 `options`（每個有 key、標題、說明、鉤子）；
  - 讀設定裡的頻道立場，用一次 Jev 呼叫問：`pick`（choice 題）、每個選項的 `stance_<key>` 與 `demo_<key>`（noul 題）、整份企劃的 `advice`（noul 題）；
  - 回傳原始答案與 `passed`；
  - 立場空白或 `auto_pick_outline` 關著時，回 409 `video_judge_not_enabled`。
- [ ] `POST /video/automation/judge/policy`：收 `slug`、`script`（旁白全文）、`viewpoint`（企劃的站主觀點），問 `stance`、`demo`、`advice`、`sponsored`，回傳答案與 `passed`。
- [ ] 伺服器端的三條規則：
  - `outline_pick_passed(payload)`：Jev 選的選項 `stance` ≥ 0.6、`demo` ≥ 0.6，而且 `advice` ≤ 0.3；
  - `final_qa_passed(payload, sha)`：`qa.ok` 為真、`qa.final_sha256` 等於這份審核的雜湊，而且伺服器列出的必要項目都在、都過；
  - `publish_package_passed(payload, sha)`：上傳包的檢查。
- [ ] `submit_review` 依規則自動核准：
  - 大綱過關時核准，`choice` 用 `pick.choice`；
  - 成片與「確認上架」過關、而且 `auto_approve_final` 開著時核准；
  - 備註寫出理由，例如「Jev 挑了 B（0.74）：符合立場 0.81、有示範 0.92」；
  - 寫稽核紀錄 `video_review_auto_approved`。
- [ ] 同一個雜湊再送一次時：既有那筆還在等站主，就換上新的 payload、summary 與 files，再跑一次規則；已經決定的，照舊回傳既有那筆。
- [ ] Jev 失敗（逾時、額度、驗證）時回 502 或 429，不核准。每次呼叫都計入 Jev 的每日次數。
- [ ] 網站的 BFF 路由 `apps/web/app/api/video/automation/judge/{outline,policy}/route.ts`，照 `speech/judge` 的寫法。

## Steps

- [ ] `app/video_automation/judge.py`：組題目與解析答案都寫成純函式，加上測試。
- [ ] 兩個端點與規則，加上測試（用假的 Jev client）。
- [ ] `submit_review` 的自動核准與重新判斷，加上測試。
- [ ] BFF 路由。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_automation_judge.py tests/test_video_reviews.py -q
cd apps/web && npm run lint && npm run typecheck
```

## Notes

- Jev 不會算數，日期也讀不準（`apps/api/app/ai/jev.py` 開頭的說明），所以只問文字判斷。
- 門檻先訂成常數。第一批五支做完之後，對照站主自己會怎麼選，再決定要不要調整。
- 第二批三支已經送審、還在等站主的成片，這張上線後可以用 `review-push --gate final` 補上品管結果，讓伺服器重新判斷。
