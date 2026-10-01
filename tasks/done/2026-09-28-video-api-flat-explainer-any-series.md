---
id: 2026-09-28-video-api-flat-explainer-any-series
title: API 讓任何系列都能設 flat-explainer
status: done
priority: P3
area: api
owner: claude-opus-5-5-flat-explainer
claimed_at: 2026-10-01T05:05:53Z
created_at: 2026-09-28T16:51:44Z
completed_at: 2026-10-01T05:18:23Z
branch: claude/flat-explainer-series-guard
depends_on: []
scope:
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_series.py
---

# API 讓任何系列都能設 flat-explainer

## Why

#904（`26a5bfb95`）把 `flat-explainer` 加進 `StylePreset`。`apps/api/app/video_automation/schemas.py:559` 的 `SeriesIn`（kind 為 series 或 story）與 :646 的 `SeriesPatchIn`（任何既有系列，包括故事聖經已經帶著角色核准的單集）都接受它。只有 web 表單把長篇系列限制在故事用的預設（`apps/web/components/admin-video-series.tsx:74-77`）；`patch_problem`（`series.py:1101-1131`）不看 `style_preset`，資料庫的 `ck_video_drama_series_style` 也對每種 kind 都允許。

長篇系列一旦被設成 `flat-explainer`，會用 `episode` 的提示詞寫出角色（`flow.mjs:78`、:394-397 的 `variantOf`），`settle` 留著角色，`validateDrama` 再擋下（`drama.mjs:301`），每一集都會卡在 lint。只有直接呼叫 API 才碰得到，所以是 P3。

2026-09-28 部署 `717e1628` 後的稽核找到的（兩個代理獨立確認）。

## Definition of done

- [x] 建立或修改非單集的系列時，`style_preset: "flat-explainer"` 回 422，並附上說明。
- [x] 已核准聖經的單集，不能被 PATCH 成 `flat-explainer`（或改了之後聖經要重審，擇一，寫進 docstring）。
- [x] 其他預設照舊。

## Steps

- [x] 在 `patch_problem` 與建立系列的檢查裡加上這條規則（`is_explainer`，`series.py:186`，已經有判斷單集的寫法）。
- [x] `test_video_series.py` 加建立與 PATCH 兩個被拒的案例。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_series.py -q
```

## Notes

- 2026-10-01（claude-opus-5-5-flat-explainer）：認領時用了 `--force`。擋住的是 codex-ten-drama 的四張（PR #978 已合併）與
  `2026-09-27-video-drama-room-withdraw-a-one`（claude-fable-5-1-video-languages，`review`、認領超過 24 小時，
  它的分支 `claude/video-review-manga-workflow-fp1rpz` 是已合併的 PR #870，`withdraw_series` 已在 main 上）。
- 前提確認無誤：「原來如此事務所」每一集都是單集作品（`docs/videos/so-thats-why/README.md` 第 118 行：表單建
  one-off、風格選 `flat-explainer`），worker 端的 `isExplainerOneOff`（`tools/video/automation/series.mjs`）
  也只認單集。沒有任何長篇或品牌故事合法地用這個預設，所以規則不需要例外。
- 建立：`SeriesIn` 的 model validator 對 `kind` 不是 `one-off` 的 `flat-explainer` 丟 ValueError，路由回 422，
  訊息是 `style_preset "flat-explainer" is for a one-off explainer only: ...`（照這個 validator 既有的英文訊息寫法）。
  品牌故事匯入（`stories.py`）也走 `SeriesIn`，一樣擋。常數 `EXPLAINER_PRESET` 搬到 `schemas.py`，`series.py` 改從那裡 import。
- 修改：`patch_problem` 多一個 `docs` 參數（預設空）。非單集改成 `flat-explainer` → 422
  `video_series_explainer_one_off`。單集選了「擇一」的第一案：worker 寫出任何一版故事聖經之後（審查中、已核准、
  被退回都算），不能跨過解說這條線（進或出都擋）→ 409 `video_series_explainer_fixed`，要換就撤回重建
  （`DELETE /series/{slug}`）。理由：審查中的聖經同樣是另一個變體；被退回後重寫時 worker 會把舊版當 previous
  帶進提示詞，換邊也對不上。故事預設之間（例如 cinematic-3d → ink-wash）照舊可改。`patch_series` 只在單集且有
  改 `style_preset` 時才讀 docs。
- 這兩個 code 走 `SeriesRefused` → `AppError`，在 admin 路由裡，`test_error_localization.py` 不要求四語訊息。
- 已有的長篇若在資料庫裡已經是 `flat-explainer`，改回其他預設不會被擋。web 表單不用動（已只給長篇故事預設）。
- 驗證：新測試在沒有改程式時 3 個失敗；ruff、兩次 mypy、`test_video_series.py`、`test_video_story*.py`、
  `test_error_localization.py` 都過（整合測試需要 PostgreSQL，本機略過）。部署後才生效。
