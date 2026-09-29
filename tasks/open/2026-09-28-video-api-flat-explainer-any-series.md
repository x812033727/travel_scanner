---
id: 2026-09-28-video-api-flat-explainer-any-series
title: API 讓任何系列都能設 flat-explainer
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-28T16:51:44Z
completed_at:
branch:
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

- [ ] 建立或修改非單集的系列時，`style_preset: "flat-explainer"` 回 422，並附上說明。
- [ ] 已核准聖經的單集，不能被 PATCH 成 `flat-explainer`（或改了之後聖經要重審，擇一，寫進 docstring）。
- [ ] 其他預設照舊。

## Steps

- [ ] 在 `patch_problem` 與建立系列的檢查裡加上這條規則（`is_explainer`，`series.py:186`，已經有判斷單集的寫法）。
- [ ] `test_video_series.py` 加建立與 PATCH 兩個被拒的案例。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_series.py -q
```
