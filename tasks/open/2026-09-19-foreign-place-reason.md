---
id: 2026-09-19-foreign-place-reason
title: foreign_place 的三種誤判形狀：短片假名國名、含國名的地標名與別名缺口、reason 寫錯國家
status: review
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:37:37Z
created_at: 2026-09-19T08:51:01Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/hotspots/guides.py
  - apps/api/tests/test_hotspot_guides.py
  - apps/api/app/destinations/localized.py
  - apps/api/tests/test_destinations_localized.py
  - apps/api/app/hotspots/bootstrap.json
---

# foreign_place 的三種誤判形狀：短片假名國名、含國名的地標名與別名缺口、reason 寫錯國家

## Why

`guides-foreign-place-scan`（PR #559）掃出 165 筆，人工逐筆判讀 117 筆（`2026-09-19-review-117-flagged-foreign-guides`）
之後，`docs/catalog-content-reviews/2026-09-19-foreign-guides-review.md` 記下三種會重複出現的誤判形狀，
不是單一列的問題：

1. **短的假名國名用子字串比對**：「タイ」在 タイム／スタイル／タイプ 裡也會命中；再加上標題把店名改寫
   （「MEGA(メガ)ドン・キホーテ 渋谷本店」對不上 ja 名稱）、只寫區名（渋谷区 不在東京的別名裡），NAVITIME
   自家的店頁 `6da32c2d` 就被判成泰國。
2. **地標名本身含另一個國家的名字**（日本橋／來遠橋、玉山），加上景點名拼法變體（古城 vs 古鎮）與缺少的別名
   （會安古城沒有 會安／Hội An／ホイアン），hoiana.com 真正寫會安的文章 `c4706b00` 兩次被判成日本。
3. **判斷對了但 `elsewhere` 寫錯國家**：同一個部落格首頁在不同列被寫成 台灣／台南／沖繩，同一頁指南宮被寫成
   泰國與台灣——寫進 `review_reason` 的國名不可靠。

## Definition of done

- [x] 短假名國名（タイ、韓国 之外的兩字詞）要求假名邊界或改用詞表比對；`6da32c2d` 那種標題不再命中。
- [x] `country_mentions` 之前先剝掉已知的含國名地標（日本橋、玉山……可列在一張小表裡）；會安古城補上別名。
- [x] `elsewhere` 取「最常被提到的國家」或「標題裡的國家」而不是第一個命中，測試涵蓋文件裡的例子。
- [x] 上面每一條在 `tests/test_hotspot_guides.py` 有一個以文件例子寫成的測試。

## Steps

- [x] 讀 `2026-09-19-foreign-guides-review.md` 的三節與例子 id，先把例子寫成會紅的測試。
- [x] 改 `foreign_place` / `country_mentions` / `mentions_place`，測試轉綠，既有測試不動。
- [ ] 用 `guides-foreign-place-scan`（list only）在主機重跑一次，確認 keep 清單裡的列不再命中。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_guides.py -q
```

## Notes

- 來源文件與例子：`docs/catalog-content-reviews/2026-09-19-foreign-guides-review.md`。
- 「市場」的雙義（釜山國際市場 → JNTO／JETRO 的「市場分析」）與部分名稱同音（第二市場→二条市場、豐南門→台南）
  是探索端的問題，不在這張票；那些列已在 117 筆裡退掉。

### 2026-09-19 done in repo (claude-fable-5-1)

用 `--force` 從同一個 owner 手上的 `2026-09-19-api-keys-in-logged-urls`（狀態 review，程式已合併，只剩站主換金鑰）
接過 `guides.py`；scope 加了 `localized.py`（三個判斷都住在那裡）、它的測試，與 `bootstrap.json`（會安別名）。

三種形狀各一個機制，都在 `app/destinations/localized.py`：

1. **片假名詞要整個詞才算。** `_pattern()` 對全片假名的詞加前後不是片假名的邊界（中點「・」與空白算分隔，
   長音「ー」算同一個詞）：「タイムセール」「スタイル」不再是泰國，「タイ人」「バンコク・タイ」還是。
   順帶「ソウルフード」不再是首爾。`6da32c2d` 的標題 + タイムセール 現在完全不命中任何國家。
2. **含國名的地標先讀掉。** `FOREIGN_NAMED_LANDMARKS = (日本橋, 日本庭園, 韓國街, 韓国街, 韓國城)`，
   `country_mentions` / `named_country` 讀文字之前先拿掉；`mentions_country`（本國提示）仍讀整段。
   `c4706b00` 那篇列了「來遠橋（日本橋）」的文章不再命中。會安古城在 `bootstrap.json` 補了別名
   會安、會安古鎮、Hội An、Hoi An、Hoi An Ancient Town、ホイアン、호이안——seed 的 aliases 會在
   `seed_catalog` 每次跑時寫回每個 locale 的 `HotspotLocalization.aliases`（`service.py`），
   之後掃描的 own_terms 就帶著它們。
3. **回報被提到最多次的國家。** 新的 `named_country(text)` 數每個國家所有詞的出現次數，平手取最早出現的
   （標題在摘要前面）；`foreign_place` 改用它。指南宮那頁（台北 ×2、泰國 ×1）回 台北；青青小熊首頁
   （台南、台北、沖繩）回 台南。`country_mentions` 本身不變（照目錄順序），其他呼叫者不受影響。

另外兩個文件建議也做了：`mentions_place` 多比一次「去掉括號與空白」的版本（NAVITIME 的
「MEGA(メガ)ドン・キホーテ 渋谷本店」對得上 ja 名稱）；`district_words(city_code)` 把 `HOTSPOT_AREAS`
的區名（澀谷／渋谷／Shibuya……）算成本國提示，`foreign_place` 讀 `hotspot.city_code`。

測試：`tests/test_destinations_localized.py` 五個新測試（假名邊界、地標、named_country、括號空白、區名）、
`tests/test_hotspot_guides.py` 三個新測試用文件裡的 id 例子（6da32c2d、c4706b00、d469749d/c7aac200、
57823a26/25a519a0）；既有測試全綠、沒有改動。

**站主在主機上跑的（票的第三步）：** 部署後先讓 seed 把會安的別名寫進資料庫（每日 `collect_hotspots` 會跑
`seed_catalog`；不想等的話跑一次景點更新），再用 keep 清單重跑一次只列不寫的掃描：

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-foreign-place-scan \
  --skip-id 6da32c2d-96a5-48ac-bde3-edee52eb28d6 \
  --skip-id c4706b00-7c1d-4eac-9d5e-96229a20f0be \
  --skip-id eff4dc8f-6ea0-4392-abed-f7bf7d6e0e72 --verbose
```

預期：拿掉 `--skip-id` 再跑一次時，`6da32c2d` 與 `c4706b00` 都不再出現在 findings 裡（兩者現在靠規則本身
就是 keep）；已退的 115 筆不會回來（退件不在掃描的 statuses 裡）。
