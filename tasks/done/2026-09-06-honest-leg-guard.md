---
id: 2026-09-06-honest-leg-guard
title: 誠實路段守衛：拒絕 0 分鐘路段與漏掉步行段的轉乘方案
status: done
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T02:24:53Z
completed_at: 2026-09-06T10:23:27Z
branch:
depends_on: []
scope:
  - apps/api/app/trips/routing.py
  - apps/web/components/route-mode-panel.tsx
---

# 誠實路段守衛：拒絕 0 分鐘路段與漏掉步行段的轉乘方案

## Why

`docs/planning-flow-spec.md` §6 PR 10。去趣的評測者 hansphoto 抱怨首爾出現 0 分鐘路段；我們的路線也可能把很短的
路段四捨五入成 0 分鐘，或轉乘方案漏掉 250 公尺以上的步行段。`details_available`（月台／出口／建議車廂）
的資料已經在 API 回應裡，但 `route-mode-panel.tsx` 沒有把它變成可見的標籤。

## Definition of done

- [x] 任何路段的顯示分鐘 ≥ 1；轉乘方案若漏掉 ≥ 250 m 的步行段就被拒絕，退回既有的 `external_only` 狀態。
- [x] `details_available` 的月台／出口／建議車廂在路線面板顯示為標籤。

## Steps

- [x] `apps/api/app/trips/routing.py`：候選方案驗證（四捨五入前用秒判斷；步行段缺漏用 step 座標距離估）。
- [x] `route-mode-panel.tsx`：標籤渲染，五語系。
- [x] 測試：造一個 30 秒路段 → 顯示 1 分鐘；造一個缺步行段的 transit 方案 → 被拒。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_trip_routing.py -q
```

## Notes

250 m 是規格作者的推估值，不是量過的門檻；上線後看 warnings 再調。韓國轉乘仍被 `routing.py:2154` 的
`region == "KR"` 擋著（需要 ODsay／Kakao 合約），這張不處理。

2026-09-06 claude-opus-5：

- 0 分鐘：`RouteStep.duration_minutes` 與 `RouteSegment.duration_minutes` 各加一個 `field_validator`，
  把 0 提成 1。放在模型層而不是各 provider，因為 Google 早就有 `max(1, round(...))`，
  NAVITIME／Ekispert／ODsay 三家的總分鐘各自算法不同（`totalTime`、`timeOnBoard+timeOther+timeWalk`、
  步驟加總），從資料庫讀回來的路段也走同一個模型。
- 漏掉的步行段：新增 `hides_a_transfer_walk(steps)`，四家 provider 的候選建構都會呼叫，
  「前一段搭到 A 站、下一段從 B 站上車、中間沒有 WALK 步驟」就丟掉這個候選（回 None），
  由既有的 external_only 流程接手。站名比較會去掉「駅／station／站／역」字尾，
  所以「東京」與「東京駅」算同一站，不會誤殺。
  **與規格的差異**：規格寫 250 公尺，但 `RouteStep` 沒有座標欄位（四家 provider 都沒帶），
  無法在不改資料形狀的情況下量距離；改用「不同站名」這個可觀察的版本，note 裡本來也說 250 m 是推估值。
  要真的量距離就得把停靠站座標帶進 `RouteStep`，那是另一張票的規模。
- 月台／出口／建議車廂標籤：**本來就有了**。`route-segment-card.tsx` 每個步驟都渲染
  `月台 {platform}`／`出口 {exit_name}`／`建議車廂 {recommended_car}`，而 `route-mode-panel.tsx`
  右欄一直都掛著這張卡（`route-panel-detail`）。`route-mode-panel.test.tsx` 既有的斷言就在找「月台 1」——
  我一度在面板摘要列另外加一排標籤，跑測試才發現畫面上會出現兩份，已經撤掉。
  真正缺的是那些標籤只有繁中，另開 `2026-09-06-route-copy-i18n`。
