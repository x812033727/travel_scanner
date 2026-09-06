---
id: 2026-09-06-zh-cn-area-labels-traditional
title: zh-CN 的 390 個區域名稱全是繁體，區域目錄沒有簡體欄位
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T13:14:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/areas.py
---

# zh-CN 的 390 個區域名稱全是繁體，區域目錄沒有簡體欄位

## Why

2026-09-06 稽核部署後的語系修正時發現：景點**名稱**已經正確簡體化，但**區域**名稱沒有。
`apps/api/app/hotspots/areas.py` 的 `_area()` 只有一個中文欄位，zh-CN 直接沿用繁體字串，
33 個城市共 390 個區域全部受影響。

`GET /hotspots/facets`（`X-Travel-Locale: zh-CN`）實際回傳：
澀谷／原宿、秋葉原／神田 —— 應為 涩谷／原宿、秋叶原／神田。

這不在任何現有票裡：`2026-09-06-food-hotspot-place-names-i18n` 的 Why 反而把 facets 的
areas 當成「已經正確」的對照組，DoD 只涵蓋國家與城市；
`2026-09-06-destinations-english-name-areas` 要求 /destinations 的 areas 對齊
/hotspots/facets，等於會把這個 zh-CN 缺口一併繼承過去。

順帶：ko 有 319/390、ja 有 245/390 的區域退回英文（所有非該國城市）。那是覆蓋率問題，
可以分開處理。

## Definition of done

- [ ] zh-CN 的區域名稱是簡體字，且與 zh-TW 不再逐字相同。
- [ ] `/destinations` 若要對齊 `/hotspots/facets`，對齊的是修好之後的版本。

## How to verify

```bash
curl -s -H 'X-Travel-Locale: zh-CN' http://127.0.0.1:8090/api/v1/hotspots/facets | jq '.areas[0:4]'
```

## Notes

景點名稱是用 `app/hotspots/simplified_names.py` 從繁體轉換的（見
[[2026-09-06-zh-cn-names-are-traditional]]），同一條路可以沿用；區域名稱在程式碼裡而不是
seed JSON，所以是改 `areas.py` 的資料結構而非跑轉換 CLI。
