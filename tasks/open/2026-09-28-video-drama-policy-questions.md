---
id: 2026-09-28-video-drama-policy-questions
title: 漫劇成片的立場檢查仍問「有示範」
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-28T13:07:50Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/tests/test_video_automation_judge.py
---

# 漫劇成片的立場檢查仍問「有示範」

## Why

成片品管（`node tools/video/cli.mjs qa`）對每一支影片都跑 `policy` 項：工人把旁白送到 `POST /video/automation/judge/policy`，Jev 回答幾個是非題，`passed` 就是那一項的結果；成片要自動核准，`policy` 必須過（`apps/api/app/video_automation/judge.py` 的 `QA_ITEMS`）。

那組題目是為教學影片寫的（`docs/videos/HANDS-OFF.md` §自動品管），其中一題是「旁白帶觀眾跟著做一個示範、設定或實算」，門檻 0.6。漫劇是故事，沒有示範，所以漫劇的成片（包括免關卡的一鍵合集作品，`docs/videos/BINGE.md`）幾乎一定在這一項不過，落回站主手動核准。

票 `2026-09-28-video-story-api-policy-languages` 只替品牌故事（作品 `kind: "story"`）換了題組；brief 明定漫劇與教學的行為不動，所以這一點留在這張票。

## Definition of done

- [ ] 站主決定漫劇的成片要問哪些題（例如沿用故事版的五題，或另寫一組：照立場、沒有建議、沒有業配、沒有貶損，不問示範與觀察），門檻寫成常數。
- [ ] 題組仍由伺服器從影片所屬的作品或格式決定（`judge.policy_questions_for`），工人不能指定；教學影片的四題一字不動，有測試。
- [ ] `ruff`、`mypy`、`pytest` 通過。

## Steps

- [ ] 先問站主漫劇的成片要不要自動核准、要問哪些題。
- [ ] `judge.py`：漫劇的題組與規則；`policy_questions_for` 依影片的格式（`video_projects.format`）或作品選題組。
- [ ] 測試：漫劇、故事、教學各自問到自己的題組。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_automation_judge.py tests/test_video_story_policy.py
```

## Notes

- 2026-09-28 開票（claude-opus-5-5-video-story-policy）：在做故事版題組時看到的。題組的選擇在 `judge.py` 的 `policy_questions_for(session, slug)`，現在只分 `story` 與其他；回應的 `PolicyVerdict.questions` 說明問了哪一組。
- Jev 只讀文字、不會算數也讀不準日期（`apps/api/app/ai/jev.py` 開頭）：題目只能問措辭，不能問事實對不對。
