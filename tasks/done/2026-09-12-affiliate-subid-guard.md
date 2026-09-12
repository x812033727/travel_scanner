---
id: 2026-09-12-affiliate-subid-guard
title: 聯盟 sub_id 不得帶使用者身分：防護套用到全部夥伴
status: done
priority: P1
area: api
owner: claude-opus-5-guides
claimed_at: 2026-09-12T03:37:52Z
created_at: 2026-09-12T03:37:52Z
completed_at: 2026-09-12T04:27:39Z
branch:
depends_on: []
scope:
  - apps/api/app/affiliates/sub_id.py
  - apps/api/app/affiliates/service.py
  - apps/api/app/affiliates/router.py
  - apps/api/app/trips/stay_router.py
  - apps/api/app/travel_services/channels.py
  - apps/api/app/search/router.py
  - apps/api/tests/test_affiliate_sub_id.py
  - docs/privacy-data-map.md
  - docs/affiliate-configuration.md
---

# 聯盟 sub_id 不得帶使用者身分：防護套用到全部夥伴

## Why

`sub_id` 是送給聯盟網路、也寫進 `affiliate_clicks` 的歸因資料。它應該描述「這次點擊」，
不是「按的人是誰」。隨使用者變動的值讓聯盟網路能把我們的流量併進一個跨站個人檔案。

盤點（`docs/privacy-data-map.md`）原本只找到一個產生點。實際上有**兩個**：

- `affiliates/router.py`（`/affiliates/options`）：`uuid5(..., user.id, search_或_trip_id, partner, module)`
- `trips/stay_router.py`（住宿區點擊外連）：`uuid5(..., user.id, trip.id, partner, hotel, area)`

`uuid5` 是決定性的，不是加鹽雜湊——知道命名空間字串的人可以拿猜測的 `user.id` 重算驗證。

防護只有 Klook 有，而且有兩個洞：

1. **住宿路徑上從未生效。** `klook` 不在 `STAY_PARTNER_ORDER`（只有 agoda、booking、
   trip_com、travelpayouts），所以那條路徑上四家全部收得到綁使用者＋綁行程的值。
2. **對 travelpayouts 不可達。** `service.py` 的防護寫在 travelpayouts 分支**之後**，
   而該分支自己就 `return`，所以唯一總是傳送該值的夥伴反而繞過它。

## Definition of done

- [x] 沒有任何夥伴收得到由 `user.id`／`trip.id`／`search_id` 衍生的 `sub_id`。
- [x] 兩個出口都設閘門（`resolve_partner_target` 與 `channels.resolve_offer_target`）。
- [x] 新增產生點或新增夥伴時，CI 會失敗而不是靜默通過。
- [x] 文件更正——`privacy-data-map.md` 與 `affiliate-configuration.md` 都還在描述舊行為。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/ -q
```

## Notes

**替代值刻意在沒有目的地時省略該段**，所以 `coarse_sub_id("aff","hotel",None,"zh-TW")`
正好等於 `aff_hotel_zh-TW`——Klook 本來就在送的那個值。因此
`test_klook_affiliates.py:245` 不必改，而它那句 `assert "private-user-id" not in target`
現在適用於全部夥伴而不只 Klook。

**閘門是形狀與內容檢查，不是來源證明。** 它擋掉不像我們標籤的值，以及任何帶 16 位以上
連續 16 進位的值（本專案出現過的每種 UUID 拼法），但分辨不出 `aff_hotel_tokyo_zh-TW`
是程式建的還是手打的。所以真正持久的保證是測試：原始碼掃描擋新產生點，夥伴測試照
註冊表參數化所以新夥伴自動有案例。三種回歸都先植入確認會失敗才留下。

**順手修掉的兩件事**：`search/router.py` 原本寫 `sub_id=uuid4().hex`（每列隨機、從不傳送、
讓 `sub_id` 索引失效），改成目錄標籤；`affiliates/router.py` 的 `source` 變數在移除 uuid5
後成為死變數——它唯一的用途就是餵那個 uuid5。

**仍然會離站的東西，不在這張票的範圍**：`_render` 仍會把 `{destination}`、`{query}`、
`{hotel_name}`、`{departure_date}`、`{return_date}` 代入夥伴樣板，住宿路徑上這些來自行程
本身。那是旅行內容不是身分，也是聯盟深層連結的必要成分，但已記進
`privacy-data-map.md` 讓政策照實說。`travel_services/stay22.py:128` 的 `campaign` 是
另一個名字的 sub-id、在 `AffiliateContext` 之外組出來，不帶身分，這次沒動它。

**收尾（#421 已合併，commit efb4cd8）。** 站主指示「把防護套用到全部」，做法先用一個
四階段 workflow 查清楚才動手（盤點 → 三個獨立設計 → 評分 → 三個對抗視角推翻）。

那次盤點推翻了我先前給站主的回報：**綁使用者的產生點是兩個，不是一個**，而漏掉的那個
（住宿區點擊外連）因為 `klook` 不在 `STAY_PARTNER_ORDER` 裡，防護從未生效。對抗驗證
另外抓到 `channels.resolve_offer_target` 這條直通 Travelpayouts API 的旁路，原設計漏了它。

**沒有宣稱 fail-closed。** 閘門是形狀與內容檢查，`SUB_ID_RE` 會讓
`aff_hotel_<uuid4hex>` 這種東西通過形狀檢查——所以另外加了長串 16 進位的拒絕規則，
並在 docstring 裡照實寫明它分辨不出標籤的來源。持久的保證在測試不在閘門。
