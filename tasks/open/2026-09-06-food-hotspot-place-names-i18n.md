---
id: 2026-09-06-food-hotspot-place-names-i18n
title: 美食與景點頁的國家／城市名稱在 en／ja／ko 仍是繁中
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T09:29:48Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/router.py
  - apps/api/app/foods/service.py
  - apps/api/app/foods/area_catalog.py
  - apps/api/app/hotspots/router.py
  - apps/api/app/localized_names.py
  - apps/api/app/destinations/localized.py
---

# 美食與景點頁的國家／城市名稱在 en／ja／ko 仍是繁中

## Why

2026-09-06 用登出狀態的 Playwright 走正式站 `/en`、`/ja`、`/ko` 之後，UI 文案已經沒有繁中，剩下的漢字全是
API 回來的地名：

- `GET /hotspots/facets`（景點頁的國家與城市篩選）：`countries[].name` 是「香港／日本／韓國…」、
  `cities[].name` 是「曼谷／釜山…」，帶 `X-Travel-Locale: en` 也一樣；同一份回應的 `areas[].name` 卻已經是
  「Shinjuku」「Shibuya & Harajuku」——區域走了 `localized_names`，國家與城市沒有。
- `GET /foods/cities`（美食頁的城市選單）：國家名已本地化（Japan／Taiwan），城市只有 `name`（繁中），
  `local_name`／`english_name` 幾乎全是 null（33 座只有台南有），所以 `food-city-picker` 只能顯示繁中。
- `GET /destinations` 已經會依 `X-Travel-Locale` 回 Tokyo／Osaka & Kyoto（`destinations/localized.py`），
  是可以沿用的參考；首頁選單本來也看不到，是 BFF 沒把頁面語系轉給 API（同日修，見 #213）。

## Definition of done

- [ ] `/en/hotspots` 與 `/en/foods` 的國家、城市篩選在 en／ja／ko／zh-CN 顯示該語系的名稱（zh-TW 不變）。
- [ ] 沒有翻譯的城市退回英文名，再退回繁中，不要出現 null 或空字串。
- [ ] 現有的 `test_hotspot_*`／`test_food_*` 加上「換語系名稱跟著換」的案例。

## Steps

- [ ] 景點：`/hotspots/facets` 的 countries／cities 用 `country_name_for`（admin_router 已在用）與
      `destinations/localized.py` 的城市名；找不到對應 destination 的城市退回 `english_name`。
- [ ] 美食：`FoodCity` 的 `local_name`／`english_name` 由 `area_catalog`／`destinations` catalog 補齊
      （`seed_food_taxonomy` 更新既有列時只動 seed-owned 的值，比照 #198 的 source 規則），
      `/foods/cities` 依 locale 挑名稱。
- [ ] 前端 `food-city-picker.tsx`／`hotspot-explorer.tsx` 只讀 API 給的 `name`，不要在前端再做對照表。

## How to verify

```bash
curl -s -b "travel_locale=en" https://mokaair.com/api/travel/hotspots/facets | jq '.countries[0], .cities[0]'
curl -s -b "travel_locale=ja" https://mokaair.com/api/travel/foods/cities | jq '.[0].cities[0]'
```

登出狀態開 `https://mokaair.com/en/hotspots` 與 `/en/foods`，篩選選單不該有漢字（日本地名的當地寫法除外）。

## Notes

2026-09-06 claude-fable-5-1 立案。掃描方法：Playwright 新 context（無 cookie）逐頁走 `document.body` 的文字節點，
列出含 `[一-鿿]` 的節點——語言切換器的「日本語／繁體中文／简体中文」與這些地名是唯二剩下的來源。
另外 `/en/search` 在沒有航班供應商時顯示的「目前沒有可用的航班查價供應商…」是 API 的 `detail` 文字（zh-TW），
屬於 API 訊息本地化那一大類，之前的 UX 稽核決定先不做。
