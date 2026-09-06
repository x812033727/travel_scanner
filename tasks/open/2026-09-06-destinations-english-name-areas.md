---
id: 2026-09-06-destinations-english-name-areas
title: destinations 的 english_name 存繁中、areas 不隨語系
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T09:56:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/destinations/localized.py
---

# destinations 的 english_name 存繁中、areas 不隨語系

## Why

2026-09-06 正式站實測 `GET /destinations`（`X-Travel-Locale: en`）：

```json
{"id":"tokyo","city":"Tokyo","local_name":"東京","english_name":"東京",
 "areas":["新宿","上野／淺草","東京站／銀座","澀谷"]}
```

- `city` 本地化正確（Tokyo），但 `english_name` 裝的是「東京」而不是英文名，欄位名與內容不符；
  用到這個欄位的地方會拿到中文。
- `areas[]` 在 en／ja／ko 都維持繁中，和同一支回應裡已經本地化的 `city` 不一致。
  （`/hotspots/facets` 的 areas 反而是本地化的，兩邊行為不一樣。）

## Definition of done

- [ ] `english_name` 是英文，或這個欄位被移除／改名成它實際代表的意思。
- [ ] `/destinations` 的 `areas[]` 依 `X-Travel-Locale` 回該語系，與 `/hotspots/facets` 一致。

## How to verify

```bash
curl -s -H 'X-Travel-Locale: en' http://127.0.0.1:8090/api/v1/destinations | head -c 400
```

## Notes

國家與城市名稱在 `/hotspots/facets`、`/foods/cities` 完全沒本地化，是另一張票
`2026-09-06-food-hotspot-place-names-i18n`，兩者可能共用同一套 `localized_names` 修法。
