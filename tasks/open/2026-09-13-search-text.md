---
id: 2026-09-13-search-text
title: 部署後清掉三筆搬過家的景點殘留的舊城市 search_text
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-09-13T03:45:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/hotspot-review-next-batch.md
---

# 部署後清掉三筆搬過家的景點殘留的舊城市 search_text

## Why

`2026-09-12-search-text`（PR #441，已合併）修好了「改目的地時 `search_text` 沒跟著換」，但那個
修法**只在搬家當下生效**：它是把舊目的地的識別 token 換成新的，而已經搬完的列，舊城市 token
已經不在比對範圍內了。

2026-09-13 的審核批次搬動了三筆，它們現在仍然掛著舊城市，用舊城市名在
`/hotspots/rankings?q=` 搜得到：

| 景點 | 現在的目的地 | 殘留 |
|---|---|---|
| 新福宮 | `taipei` | 台中 |
| 新營美術園區 | `tainan` | 高雄 |
| Thác Mây Treo | `da-nang` | 順化 |

要等 PR #441 部署到正式站之後才做得了。

## Definition of done

- [ ] 三筆的 `search_text` 不再含舊城市名。
- [ ] 下面那句 SQL 回傳 0 列。

## Steps

- [ ] 確認正式站已經跑在含 PR #441 的版本上。
- [ ] 以管理員身分對每一筆呼叫兩次 `POST /api/travel/admin/hotspots/review`：先搬回舊目的地，
      再搬回正確的目的地。第二次結束時 `search_text` 就乾淨了。

```
{"ids":["<id>"],"action":"update","destination_id":"taichung"}   // 再來 taipei
{"ids":["<id>"],"action":"update","destination_id":"kaohsiung"}  // 再來 tainan
{"ids":["<id>"],"action":"update","destination_id":"hue"}        // 再來 da-nang
```

## How to verify

```sql
select name, city_name, search_text from travel_hotspots
where review_status in ('approved','pending')
  and position(lower(city_name) in search_text) = 0;
```

## Notes

代價要知道再做：每筆會留下兩筆稽核紀錄，而且中間那幾秒該列會掛在錯的城市底下（三筆都已經
上架）。挑離峰時間做。

排名走快照，`hotspot-collector` 每 21,600 秒重建一次，所以公開面的搜尋結果不會立刻反映。

背景見 `docs/hotspot-review-next-batch.md` 第四批與 `tasks/done/2026-09-12-search-text.md`。
