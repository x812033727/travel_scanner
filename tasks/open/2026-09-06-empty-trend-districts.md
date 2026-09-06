---
id: 2026-09-06-empty-trend-districts
title: 21 個潮流街區還沒有任何店家
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:53:14Z
completed_at:
branch:
depends_on:
  - 2026-09-06-trend-import-scripts
scope:
  - apps/api/app/foods/data/trend_merchants.json
---

# 21 個潮流街區還沒有任何店家

## Why

57 個潮流商圈裡只有 36 個拿到店家，另外 21 個是空的。空商圈在公開頁會被自動隱藏
（`count === 0` 的籤不顯示），所以旅客看不到 —— 但這也表示那些街區等於不存在，
補街區的整件事只做完六成。

缺口集中在幾個目的地：大阪／京都 6 個街區只有 1 家店（只有西陣的鶴屋吉信過關）、
台北 3 個街區只有 1 家、香港 5 個街區 0 家、新加坡 2 個 0 家、河內／胡志明市／峴港
各 1 個街區 0 家。

## Definition of done

- [ ] 每個潮流商圈至少有 3 家可查證、現在還在營業的店家，或是有一行寫下來的理由說明
      為什麼這個街區找不到（例如街區以選品店為主、沒有值得收的餐飲）。
- [ ] 新增的店家和第一批同樣是 `pending` + 未啟用，附官方或觀光局來源。

## Steps

- [ ] 列出 21 個空商圈（見 Notes 的 SQL）。
- [ ] 針對這些街區再跑一次研究 + 反駁的掃描，只掃空的，不要重掃已有店家的。
- [ ] 過人工眼一遍，用第 1 張任務的匯入指令 dry-run → apply。
- [ ] 把新的一批併進倉庫裡的資料檔。

## How to verify

```sql
SELECT a.names_json->>'zh-TW' AS area, count(m.id)
FROM food_areas a LEFT JOIN food_merchants m ON m.area_id = a.id
WHERE a.source = 'admin'
GROUP BY 1 HAVING count(m.id) = 0 ORDER BY 1;
```

跑完應該剩下的只有「明確判定沒有值得收的餐飲」那幾個。

## Notes

**上一輪的成績與教訓**（2026-09-06，50 個 agent：25 研究 + 25 反駁）：
244 家提名 → 101 家存活 → 99 家寫入。淘汰 143 家，理由分布是證據不足 100、
來源不合格或失效 17、連鎖店 15、已歇業 6、不在街區內 5。淘汰率 58% 是刻意的，
反駁者被要求「證據薄弱一律刷掉」，不要為了填滿而放寬。

**為什麼日本的成績特別差**：大阪／京都提了一堆名店（一乗寺的拉麵、中崎町的咖啡）
卻幾乎全被刷掉，主因是「來源必須是店家自己或官方機構的頁面」—— 很多日本個人店只有
Instagram 或食べログ，而食べログ屬於彙整站不算數。下一輪可以考慮把「店家官方
Instagram 帳號頁」明確列為可接受來源（目前的提示詞其實已允許，但研究員多半沒去找），
或者接受各地觀光協會的店家頁。

**提示詞與 schema** 在當次 session 的 workflow 腳本裡：scratchpad 的
`trend-merchant-sweep.js`（run id `wf_333381b8-e78`）。裡面的規則值得沿用：
每區 3-5 家、必須在街區中心幾百公尺內、獨立店優先於連鎖、寧可空著也不要湊數。

**被刷掉的 143 家清單**在 scratchpad 的 `trend-merchants-dropped.json`，含每一家的
理由。重掃之前先看一眼，避免把同一批已經判定不合格的店家再提名一次。
