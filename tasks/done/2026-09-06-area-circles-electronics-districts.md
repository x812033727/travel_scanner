---
id: 2026-09-06-area-circles-electronics-districts
title: 區域目錄缺龍山電子商街與光華商圈兩個圈
status: done
priority: P3
area: api
owner: codex-gpt6-electronics-areas
claimed_at: 2026-09-30T11:24:51Z
created_at: 2026-09-06T20:29:31Z
completed_at: 2026-09-30T11:39:34Z
branch: codex/electronics-area-circles
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

- [x] 兩筆都 `resolve_area(...)` 有值，`AREA_NO_CIRCLE_YET_SEEDS` 清空並刪除。
- [x] `test_seed_spot_checks` 既有的對應關係一個都沒變。

## Steps

- [x] `apps/api/app/hotspots/areas.py`：ICN 加一個圈涵蓋龍山電子商街（37.533, 126.963 一帶），
      TPE 加一個涵蓋光華商圈／華山（25.045, 121.531 一帶）。
- [x] **加圈之前先列出會被新圈吃掉的既有種子**：resolver 取「相對距離最小」的圈，新的小圈可能
      把鄰近種子從原本的圈搶過來。
- [x] 五語名稱照既有 area 的寫法（`zh-TW` 與 `en` 必填）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_areas.py tests/test_shopping_bootstrap.py -q
```

## Notes

- Pre-PR refresh: 28 open PRs, 60 remote heads and 175 other accessible worktrees
  still have no competing scope. Updated to main 4793de77; its new commit only
  documents the verified Windows runtime and moves that unrelated ticket.
  Reran all 19 affected tests successfully after this update. Task checks passed
  for 1,195 files, with only existing unrelated stale-claim/overlap warnings.

- Implemented the two circles and removed the missing-circle exception. Existing
  region values, resolver logic and seed coordinates remain unchanged. New payload
  regressions cover all five locales: Yongsan uses its reviewed Japanese/Korean
  seed names, and Guanghua follows the existing Taipei English locale fallback.
- Final local validation: 19 areas/shopping-bootstrap tests passed, zero skips.
  Full API Ruff passed; mypy app passed 444 files and tests passed 335 files.
  The independent post-change comparison confirms exactly two seed changes:
  `icn-yongsan-electronics-market`: null -> yongsan-electronics;
  `tpe-syntrend-creative-park`: null -> guanghua; all other 591 are unchanged.
- The Huashan regression uses the rounded P625 location in Wikidata Q14594864
  (https://www.wikidata.org/wiki/Q14594864), with its OpenStreetMap relation
  5177809 reference: (25.044609, 121.529183). This non-seed point now belongs to
  guanghua, matching the combined name; the 591-seed stability claim does not
  assert unchanged classification of every live coordinate.

- 2026-09-30 claimed normally on main d7787f51 after checking 28 open PRs, 61
  remote heads, 401 local branches and 175 other accessible worktrees. No valid
  overlapping edits or claims; the three historical P: whole-checkout deletion
  states are untouched. Other candidate web tickets had live worktree owners.
- Before editing, compared all 593 seeds against candidate circles. Only the two
  target slugs change from no area; the other 591 mappings remain identical.
  ICN: (37.533, 126.963), 0.6 km. TPE: (25.045, 121.531), 0.4 km.
  TPE radii 0.4 / 0.5 / 0.6 / 0.8 km have the same seed delta; choose the smaller
  range. It also covers the adjacent Huashan core, so the name explicitly includes
  Huashan. The Yongsan circle does not reach the Yongnidan-gil circle's center.
- Naming checked against official tourism descriptions: Seoul's Yongsan Electronics
  Market page (https://english.visitseoul.net/shopping/Yongsan%20Electronics%20Market/ENP009672)
  and Taipei's linked Huashan–Syntrend–Guanghua itinerary
  (https://www.travel.taipei/en/fun/tour/details/1197). Positions use the existing
  reviewed catalog coordinates; these circles are filtering areas, not legal boundaries.
- Independent baseline/candidate evidence is in a local scratch file, not a
  production snapshot. No production data access, import, merge or deployment.

- 也可以改成把 `yongnidan` 的半徑放大，但那會把龍理團街的名字掛到電子商街上，寧可另立一圈。
