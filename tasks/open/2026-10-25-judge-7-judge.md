---
id: 2026-10-25-judge-7-judge
title: 免關卡作品的設定圖在 judge 沒有推薦時仍要自動選：門檻 7 高過 judge 的天花板，每個新角色都等人
status: review
priority: P2
area: api
owner: claude-fable-5.1
claimed_at: 2026-10-25T12:30:02Z
created_at: 2026-10-25T12:16:10Z
completed_at:
branch: claude/confident-chatterjee-34ca55
depends_on: []
scope:
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_reviews_admin.py
  - apps/api/tests/test_video_reviews.py
  - docs/videos/HANDS-OFF.md
---

# 免關卡作品的設定圖在 judge 沒有推薦時仍要自動選

## Why

《系統說我是 BUG》是免關卡作品（`hands_off`），設定分頁的 `auto_pick_look` 也開著，但 2026-10-25 第 1 集重做（`e001-redo1`）與第 5 集同時停在設定圖關卡，10 個審核全是「judge 沒有推薦」，等人選了一個多小時。

原因在 `settings.py` 的 `look_pick_passed`：它只在 judge 的 `suggested` 不是 null、而且分數 ≥ `judge_min_score`（7）時自動核准；工人端 `look.mjs suggestedOf` 又只在有候選圖 `passed`（分數過同一門檻、沒列問題）時才給 `suggested`。judge 給設定圖的分數天花板約 6.3（10 組 60 張最高 6.29；`2026-10-xx` keyframe judge ceiling 的票也量過 7 到不了），所以 `suggested` 永遠是 null，免關卡在這一關形同沒開。50 集每個篇章都有新配角（阿竹、老七…），而且 `series-store.mjs sheetKey` 把外貌文字算進鍵，10-24 改過卡司後舊的設定圖也不再沿用，於是每集、每個角色都要人點一次。

judge 列的問題裡有兩類是真要擋的：`no_text`（角落長字，image-01 的通病，但設定圖上有字會被 subject_reference 帶進關鍵影格）與 `clean`（重複人物、手部錯）；`appearance`／`style` 多半是 judge 對素底設定圖的誤判（它要求背景畫成落石鎮，但設定圖的 prompt 本來就要求 plain light grey background）。

## Definition of done

- [x] 免關卡作品（或 `auto_pick_look` 開著）的設定圖審核在 `suggested` 為 null 時，伺服器改選「沒有 `no_text`、沒有 `clean` 問題的候選圖裡分數最高的一張」，分數至少 `judge_min_score - 2`（7 → 5）；備註寫明是備援選法與那張的分數、略過了哪幾張與原因。
- [x] 沒有任何一張合格時照舊留給人（pending），備註不變。
- [x] 非免關卡、`auto_pick_look` 關著的影片行為不變；長篇動畫（`is_long_anime`）仍不自動選。
- [x] 關鍵影格的門檻（`keyframes.mjs` 用同一個 `judge_min_score`）不受影響。
- [x] `HANDS-OFF.md` §設定圖那列寫明備援選法。

## Steps

- [x] `settings.py`：`look_fallback_pick(payload, min_score) -> tuple[str, float, list[str]] | None`（略過 problems 以 `no_text:`／`clean:` 開頭的候選）；`auto_picks_look` 回「用哪種選法」或在 `admin_service.py` 的 look 分支加第二個 elif。
- [x] `admin_service.py`：`review.choice` 用備援的 key，備註用新的 `AUTO_PICKED_LOOK_FALLBACK_NOTE`。
- [x] 測試：suggested null＋有合格候選 → 自動選最高分；全被 `no_text` 擋 → pending；分數低於 5 → pending；非免關卡 → pending。
- [x] `uv run pytest tests/test_video_automation_settings.py tests/test_video_reviews_admin.py`、ruff、mypy。

## How to verify

部署後下一個新角色的設定圖審核（第 6–10 集的阿竹）在工人送審的同一回合就 approved、備註是備援選法；`/admin/videos/<slug>` 的 `reviews[]` 裡 `gate=look` 沒有 pending。

## Notes

- 2026-10-25 的 10 組是手選的（後台頁同源 `POST /admin/videos/<slug>/reviews/<id>/decision` `{decision, choice, note}`）：e001-redo1 江河 C、唐測 D，系統退件（六張都畫了人，備註只要空白淡藍光板）；e005 江河 A、千凜 F、唐測 D、老七 D、小鐵 A、阿桂 F、系統 D。
- 看候選圖：`reviews[].files[]` 的 `role`（candidate_a…）對 sha256，圖片位元組走前端 `/api/admin-video-files/<slug>/<sha256>`（API 的 `/admin/videos/<slug>/files/<sha>` 回的不是圖）。
- 同一角色各集設定圖不同（e002 江河 C、e003 E、e004 D、e005 A）會漂：`reuseSheets` 只沿用 `sheetKey`（id＋appearance＋sheet_prompt＋look）相同、且 `keepSheets` 存進 `<workBase>/series/<slug>/characters` 的圖；改外貌文字就會重畫。這張票不處理漂移，先讓關卡不停。

## 做法（2026-10-25，claude-fable-5.1）

PR：https://github.com/x812033727/travel_scanner/pull/1850

- `settings.py`：前置條件抽成 `_look_pick_threshold(session, series_slug) -> judge_min_score | None`
  （開關或免關卡、非長篇動畫），`auto_picks_look` 照舊回 bool；新的 `auto_look_fallback` 用同一個
  前置條件呼叫 `look_fallback_pick`，回 `(key, note)`。`look_fallback_pick` 略過 `problems` 以
  `no_text:`／`clean:` 開頭的候選（`LOOK_BLOCKING_PROBLEMS`）與沒有分數的候選，取剩下最高分、且
  ≥ `judge_min_score - LOOK_FALLBACK_SLACK`（2）的一張。備註 `AUTO_PICKED_LOOK_FALLBACK_NOTE`
  寫門檻、選了誰幾分、備援門檻、略過哪幾張與原因（問題句去掉「→ 修法」）。
- `admin_service.py` 的 look 分支加第二個 `elif`：`auto_picks_look` 沒過才問 `auto_look_fallback`，
  所以 judge 的推薦有過時備註不變。
- scope 加了 `apps/api/tests/test_video_reviews.py`：那裡兩個用真 SQLite 的測試把 `auto_picks_look`
  mock 成 False 後本來就期待 pending，新的第二個 `elif` 會真的查 `video_automation_settings`（測試庫
  沒建這張表），所以各補一行把 `auto_look_fallback` mock 成 None。沒有改其他行為。
- `judge_min_score` 沒動，關鍵影格門檻不受影響；`ruff format` 對這三個共用檔本來就會重排，CI 只跑
  `ruff check`，所以沒有套用，免得 diff 蓋到別的票。
