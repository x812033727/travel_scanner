---
id: 2026-10-24-policy-qa-asks-a-drama-for
title: 自動品管的 policy 把漫劇當教學片問「有示範」：每一集成片都不過、免關卡作品永遠停在成片審核
status: done
priority: P1
area: api
owner: claude-fable-5-1-drama-policy
claimed_at: 2026-10-24T15:53:32Z
created_at: 2026-10-24T15:30:00Z
completed_at: 2026-10-24T16:21:53Z
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/judge.py
  - apps/api/tests/test_video_automation_judge.py
  - docs/videos/HANDS-OFF.md
  - tasks/open/2026-09-28-video-drama-policy-questions.md
  - apps/api/tests/test_video_judge.py
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# 自動品管的 policy 把漫劇當教學片問「有示範」：每一集成片都不過、免關卡作品永遠停在成片審核

## Why

《系統說我是 BUG》第 1 集（`xitong-shuo-wo-shi-bug-e001`，免關卡作品）2026-10-24 11:45Z 成片送審，`qa` 十一項十項 ok，`policy` 沒過：「Jev：符合立場 0.71、有示範 0.08、建議 0.01、業配 0.02；沒過（有示範低於 0.6）」。成片因此停在待審等站主，免關卡的 BINGE 流程（成片自動核准 → 上傳包 → 上架確認自動核准 → 下一集）在這裡斷掉，50 集會停 50 次。

`apps/api/app/video_automation/judge.py` 的 `judge_policy` 用 `policy_questions_for(session, slug)` 看 `VideoProject.category` 決定問哪一組：story → 品牌故事三題、cut／explainer → 不問示範、其他 → 教學片四題（含「有示範」，門檻 `POLICY_MIN_DEMO` 0.6）。漫劇影片的 `category` 是 null（format 是 drama），所以被當教學片問示範；一部爽文漫劇當然沒有「可以照做的示範」。

另外 drama 分頁的 `drama_auto_approve_final` 在主機是 false（DRAMA-FLOW.md：遷移時複製教學片的值；教學片現在是 true）。這張票只修 policy；開關由站主在設定分頁勾（2026-10-24 從 session 改設定被分類器擋）。

## Definition of done

- [x] format 為 drama 的影片（單集、作品的集、合集）跑 policy 時不問「有示範」，用 explainer 那一組三題（符合立場、建議、業配），判讀用 `read_policy_answers(answers, "explainer")`；品牌故事照舊走 story。
- [x] 教學片、解說、Shorts 的 policy 行為不變。
- [x] 測試：drama 專案的 `policy_questions_for` 回不問示範的一組；教學片仍問。
- [ ] 部署後 e001 若還 pending，站主核准一次；之後的集在 `drama_auto_approve_final` 開著時自動過。（部署與站上審核不在這張票的 session 做）

## Steps

- [x] `policy_questions_for`：除了 category，也讀 `VideoProject.format`（或 series_slug／`video_drama_requests`）判 drama → "explainer"。
- [x] `uv run pytest tests/test_video_automation_judge.py`、`ruff`、`mypy`；開 PR。

## How to verify

e005 起（部署後開做的集）成片送審時 `policy` 顯示「有示範：不適用」且 ok，成片備註「自動品管十一項全過，依設定自動核准」。

## Notes

- 發現於票 2026-10-24-bug-1-4；記憶 travel-scanner-video-ai-shopping-agents 也記過「policy 示範分數卡 0.5」（時事片同一個問題）。
- 2026-10-25 做法（claude-fable-5-1-drama-policy）：`policy_questions_for` 多查 `VideoProject.format`，新常數 `NO_DEMO_FORMATS = {"drama"}`，格式在裡面就回 `"explainer"`（在 `cut` 之後、分類之前判）；品牌故事作品的集仍先由 `video_series_kind == "story"` 回 `story`。合集影片（`<作品>-full`）的 `qa` 是 `COMPILATION_QA_ITEMS` 六項、沒有 `policy`，所以本來就不會卡；這條規則對它只是一致。`outline_demo_asked`／`demo_asked_of` 只看分類，沒動：漫劇不走選大綱（SERIES.md）。
- 測試用 aiosqlite 建 `video_projects`／`video_drama_series`／`video_drama_episodes` 三張表，九種 slug 一次比對；另一個測試 monkeypatch `_ask`，確認 `judge_policy` 只問三題、`demo` 是 None、備註「有示範：不適用（解說）」且通過。`HANDS-OFF.md` §自動品管那段「只看分類、不看格式」改掉；票 `2026-09-28-video-drama-policy-questions` 問的就是這個決定，一併結案。
