---
id: 2026-09-06-area-circles-electronics-districts
title: 區域目錄缺龍山電子商街與光華商圈兩個圈
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T20:29:31Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/areas.py
  - apps/api/tests/test_hotspot_areas.py
---

# 區域目錄缺龍山電子商街與光華商圈兩個圈

## Why

購物店家種子批次進來後，30 筆裡有 2 筆在市區卻落在所有區域圈之外：

| slug | 差多少 | 最近的圈 |
| --- | --- | --- |
| `icn-yongsan-electronics-market` 龍山電子商街 | 800 m | `yongnidan` 龍理團街（半徑 600 m） |
| `tpe-syntrend-creative-park` 三創生活園區 | 160 m | `taipei-station` 台北車站（半徑 1.2 km） |

兩個都是市內的電子商圈，說它們「在郊外」並不誠實，所以它們被記在
`tests/test_hotspot_areas.py::AREA_NO_CIRCLE_YET_SEEDS`，而不是塞進出城清單。

實務後果：這兩筆在熱門景點頁沒有區域標籤，也不會出現在區域篩選裡。

## Definition of done

- [ ] 兩筆都 `resolve_area(...)` 有值，`AREA_NO_CIRCLE_YET_SEEDS` 清空並刪除。
- [ ] `test_seed_spot_checks` 既有的對應關係一個都沒變。

## Steps

- [ ] `apps/api/app/hotspots/areas.py`：ICN 加一個圈涵蓋龍山電子商街（37.533, 126.963 一帶），
      TPE 加一個涵蓋光華商圈／華山（25.045, 121.531 一帶）。
- [ ] **加圈之前先列出會被新圈吃掉的既有種子**：resolver 取「相對距離最小」的圈，新的小圈可能
      把鄰近種子從原本的圈搶過來。
- [ ] 五語名稱照既有 area 的寫法（`zh-TW` 與 `en` 必填）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_areas.py tests/test_shopping_bootstrap.py -q
```

## Notes

- 也可以改成把 `yongnidan` 的半徑放大，但那會把龍理團街的名字掛到電子商街上，寧可另立一圈。
