---
id: 2026-09-06-merchant-coordinate-backlog
title: 271 家店家沒有永久座標，全部無法發布
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-06T00:53:26Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/coordinate_queue.py
  - apps/web/components/admin-merchant-coordinate-queue.tsx
---

# 271 家店家沒有永久座標，全部無法發布

## Why

目錄裡有 272 家店家，**只有 1 家是公開的**（`tokyo-sushi-dai`）。其餘 271 家全部卡在
同一個地方：沒有耐久座標。發布守門要求 approved + active + `map_match_status='verified'`
+ 耐久座標（型別在 curated/wikidata/official_tourism/merchant_official/admin_verified
且來源網址是 https）+ 精準地圖識別 + 至少一個來源 + 至少一個分類。前面幾項多半有了，
座標是唯一普遍缺的一項。

工具都已經在了，只是沒有人去跑：
- `fill-food-merchant-coordinates`（別的 session 在 #172 修好首列就崩的 bug）可以從
  店家自己引用的頁面抓座標，**不需要人工**。
- 後台的「座標佇列」分頁（我在 #152 做的）把商家和 Google 找到的地點並排，一致的預先
  勾選，批次核准就寫入 `admin_verified`。

## Definition of done

- [ ] 271 家裡的絕大多數拿到耐久座標，剩下的每一家都有明確理由（Google 查無結果、
      韓國等 NAVER、名稱對不上需要人工找）。
- [ ] 公開的美食目錄不再是只有 1 家店。

## Steps

- [ ] 先跑不需要人工的那條：`fill-food-merchant-coordinates`，把能從自家頁面抓到的先填掉。
- [ ] 後台 → 美食 → 座標佇列，一頁一頁批次核准（綠標「一致」的可以直接送，黃標的看一眼）。
- [ ] 韓國店家會停在 `coordinates_saved`（座標有了但等 NAVER）—— 那是設計如此，見
      2026-09-06-naver-maps-key。
- [ ] 有座標之後才輪到發布：後台批次 `verify_activate`（仍會逐項檢查守門）。

## How to verify

```sql
SELECT count(*) FILTER (WHERE review_status='approved' AND is_active AND map_match_status='verified') AS published,
       count(*) FILTER (WHERE latitude IS NULL) AS no_coords
FROM food_merchants;
```

公開頁 `/zh-TW/foods` 選一個城市，商圈籤上的數字要對得起來。

## Notes

**佇列的成本模型**（重要，不要無腦刷新）：每開一頁佇列會對 Google 送最多 10 次
Text Search Pro 查詢（免費額度 5,000/月，和行程規劃共用）。查得到的結果會進 Redis
快取 24 小時，查不到的我另外寫了 24 小時負快取（`foods:coordinate_queue:no_result:*`），
所以同一頁重複開不會重複計費。**不要**動到 Place Details Enterprise（免費額度本月只剩
一百多次）。

**核准是伺服器端重新解析的**：瀏覽器送上來的只有 `merchant_id` + `place_id`，伺服器
會用同一個查詢再問一次 Google，答案變了就回 `candidate_changed` 拒寫。所以寫進去的
座標一定是人看過的那一份。

**為什麼不直接存 Google 的座標**：`google_places` 依設計永遠不是耐久來源（Places 結果
最多快取 30 天）。人工看過並排比對後記成 `admin_verified` + 公開的 Google 地圖頁網址，
才是這個專案認可的做法。不要為了省事去放寬 `DURABLE_COORDINATE_SOURCES`，
`test_precise_locations.py` 會擋。

**佇列排除的列**：`review_status` 是 rejected/disabled、或 `map_match_status` 是
ambiguous/disabled 的不會出現（管理員的判斷不該被批次核准推翻），核准端也會再檢查一次
（回 `not_eligible`），因為過期的瀏覽器分頁還是可能送上來。

**如果要提高吞吐**：目前一頁固定 10 筆、上限 20。可以考慮加一個「只顯示綠標」的模式，
或做一個全佇列的自動核准（僅限 `agree` 且距離為 0 的），但那等於放棄人工把關，要先想清楚。
