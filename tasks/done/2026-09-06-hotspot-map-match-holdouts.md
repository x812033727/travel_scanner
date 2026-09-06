---
id: 2026-09-06-hotspot-map-match-holdouts
title: 52 個景點的地圖比對對不上，需要人工判斷
status: done
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:07:28Z
created_at: 2026-09-06T00:55:02Z
completed_at: 2026-09-06T06:32:49Z
branch: claude/ops-p1-p2
depends_on: []
scope:
  - apps/api/app/hotspots/places.py
---

# 52 個景點的地圖比對對不上，需要人工判斷

## Why

2026-09-04 那輪批次驗證把 132 個景點翻成 `verified`，但有 52 個被刻意留下來，因為
機器判不了：**30 筆名稱對不上**、**17 筆座標漂移超過門檻**、**5 筆 Google 查無結果**。

這些不是資料錯誤，是「需要一個人看一眼」的案例。留著不管的話，它們會一直是不可發布
的狀態，而且下一輪批次會再算一次、再留一次。

## Definition of done

- [x] 52 筆每一筆都有結論：修正座標、換掉 Place ID、判定為不同地點而拒絕，或標為
      `ambiguous` 表示人工看過但無法決定。
- [x] 不再有「每次跑批次都重新出現同一批」的情況。

## Steps

- [x] 撈出這批列（`map_match_status <> 'verified'` 且有 place profile 的）。
- [x] 名稱對不上的：多半是 Wikidata 標題與 Google 顯示名不同（例如帶行政區前綴），
      人工確認是否同一個地方。
- [x] 漂移的：確認是座標錯還是 Google 指到了別的入口／分館。最遠的一筆當時量到 170 公里。
- [x] 查無結果的：可能是已歇業或名稱只有當地語言，考慮改用當地語言查詢。

## How to verify

```sql
SELECT map_match_status, count(*) FROM travel_hotspots
WHERE review_status = 'approved' GROUP BY 1;
```

## Notes

**判準來自 `apps/api/app/hotspots/candidates.py`**，門檻是量過的：名稱分數
`NAME_THRESHOLD = 0.75`（校準時正確配對都 ≥0.83、錯誤配對都 ≤0.67）、
漂移上限 1 公里、包含關係要長度比 ≥0.6（否則「大阪市」會吞掉「大阪市立美術館」）。
不要為了清掉這 52 筆去放寬門檻 —— 那些數字是一次次被假陽性打臉之後定下來的。

具體被擋下來的例子（說明門檻在做事）：`天保山大橋`（橋）以 0.67 對上某個景點被擋、
`大阪城ホール`（體育館）只靠距離會通過但名稱擋掉了、`清水寺` 加了城市限定詞才沒有
配到 45 公里外的同名寺廟。

另外有 **6 個已知座標錯誤的種子**是分開追蹤的，記在
`tests/test_hotspot_areas.py::AREA_UNASSIGNED_SEEDS`（沖繩美國村指到大阪美國村、
首爾世宗村的座標落在麻浦、釜山흰여울的 Wikidata 條目其實是分類項⋯）。那一批修起來
會動到深度旅遊的數量契約，是另一件事，不要混在這張任務裡。

2026-09-06 claude-fable-5-1：approved 且未 verified 的列在做之前是 117（不是 52，之後的批次
又留下一批），其中 **90 筆是韓國**：守門對 KR 只認 NAVER 精準頁，不是判斷案例，見
`naver-maps-key`。非 KR 的 27 筆逐筆看過：

- 16 筆同一個地方、只是名稱寫法不同或 Google 指到入口（陶器散步道、美國村、作並溫泉、
  美塞、閣堯艾島、翡翠洞、小皮皮島、台江國家公園、Phật viện Đồng Dương、會安古城、保大宮、
  宮殿二號、河內陶瓷馬賽克壁畫、順化太和殿、古芝地道、奧南）→ `review update
  map_match_status=verified`（守門逐筆檢查 Place ID／座標／來源）。
- 2 筆是行政區不是景點（甲米府治縣、喀比府）→ `disable`。
- 4 筆沒有 Place ID：跑 `match-hotspot-places --destination chiang-rai|krabi|da-nang|hue`，
  Wat Phra That Doi Tung 直接發布；Wat Huai Pla Kang、峴港主教座堂、清水橋（Thanh Toàn
  Bridge）的候選看過是同一個地方，`PATCH place-profile approve`。
- 留下的非 KR 只剩 4 筆：`cei-doi-tung`（信心 0.08，Place ID 指向哪裡不確定，標記留人看）、
  `nrt-otome-road`（Google 無 POI，見 kanto 任務）、`retired-patong-beach`、
  `retired-phuket-old-town`（retired 列，不動）。

現況：approved 938 = verified 844 + unverified 94（90 KR + 上面 4 筆）。門檻沒有放寬。
