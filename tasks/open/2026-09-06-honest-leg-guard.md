---
id: 2026-09-06-honest-leg-guard
title: 誠實路段守衛：拒絕 0 分鐘路段與漏掉步行段的轉乘方案
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T02:24:53Z
completed_at:
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

- [ ] 任何路段的顯示分鐘 ≥ 1；轉乘方案若漏掉 ≥ 250 m 的步行段就被拒絕，退回既有的 `external_only` 狀態。
- [ ] `details_available` 的月台／出口／建議車廂在路線面板顯示為標籤。

## Steps

- [ ] `apps/api/app/trips/routing.py`：候選方案驗證（四捨五入前用秒判斷；步行段缺漏用 step 座標距離估）。
- [ ] `route-mode-panel.tsx`：標籤渲染，五語系。
- [ ] 測試：造一個 30 秒路段 → 顯示 1 分鐘；造一個缺步行段的 transit 方案 → 被拒。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_trip_routing.py -q
```

## Notes

250 m 是規格作者的推估值，不是量過的門檻；上線後看 warnings 再調。韓國轉乘仍被 `routing.py:2154` 的
`region == "KR"` 擋著（需要 ODsay／Kakao 合約），這張不處理。
