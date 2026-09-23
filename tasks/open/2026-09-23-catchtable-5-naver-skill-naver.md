---
id: 2026-09-23-catchtable-5-naver-skill-naver
title: CatchTable 兩批收尾：5 家只差座標或 Naver 條目的店，與 skill 的 Naver 分工修正
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-23T10:10:43Z
completed_at:
branch: claude/catchtable-leftovers
depends_on: []
scope:
  - docs/catalog-content-reviews/catchtable-batch-2.md
  - docs/catalog-content-reviews/catchtable-seoul-batch-1.md
  - .agents/skills/catchtable-discovery
  - .claude/skills/catchtable-discovery
---

# CatchTable 兩批收尾：5 家只差座標或 Naver 條目的店，與 skill 的 Naver 分工修正

## Why

CatchTable 榜單反推的兩批（票 `2026-09-22-catchtable-ranking-discovery-batch-1`、`2026-09-23-catchtable-batch-2-seoul-busan`）把 39 家建成 pending，
34 家已公開；剩 5 家各差一樣東西，都要站主或外部資料才能補，不該留在聊天紀錄裡：

| slug | 差什麼 | 現況 |
| --- | --- | --- |
| `seoul-sancheongstar`（산청숯불가든 을지로 2호점） | 耐久座標 | Naver 頁已存（`1069950349`）；母公司門市頁的地圖是前端即時地理編碼、沒有座標，OSM 沒有 을지로14길 12 |
| `seoul-koreahouse-kohojae`（한국의집 고호재） | 自己的 Naver 條目 | 座標已有（OSM 한국의집園區 way）；站主兩次貼的短網址都解到 `11715055`＝한국의집主頁，與 `seoul-korea-house` 撞號 |
| `seoul-haechen-obu`（해천어부） | 耐久座標 | Naver 頁已存（`1295127958`）、平台列 verified；OSM 沒有 수표로28길 11 |
| `busan-jejugan-seomyun`（제줏간 부산서면점） | 耐久座標 | Naver 頁已存（`1142753247`）；OSM 沒有 중앙대로691번가길 11 |
| `busan-solsot-gwangan`（솔솥 광안리점） | 耐久座標 | Naver 頁已存（`1422399262`）；OSM 沒有 광남로 78 |

站主 2026-09-23 說先跳過。另外第二批學到一件要寫回 skill 的事：給站主的 Naver 搜尋連結（percent-encoded 的
`map.naver.com/p/search/…`）在站主那邊打不開，站主最後是自己搜的；skill 的 Naver 分工要改成給「編號｜店名｜地址」的表。

## Definition of done

- [ ] skill `catchtable-discovery` 的 `references/admin.md` 不再教人給 percent-encoded 搜尋連結，改成給表讓站主自己搜、回貼「編號 短網址」；同園區另一間餐飲要搜那間的名字。
- [ ] 5 家的去向各有一個明確結果：補上耐久座標（OSM 出現門牌物件、觀光局頁出現座標、或站主自填並在報告註明依據）並在後台驗證＋核准；
      或站主決定維持 pending／退掉，寫進兩份報告的「還沒做完的」。
- [ ] 公開 API 計數與兩份報告的「後台操作紀錄」一致。

## Steps

- [x] admin.md 的 Naver 分工修正（本票開出時已一起改）。
- [ ] 每季或 OSM 更新後重查四個地址的 Nominatim／Overpass（skill `references/admin.md` 的座標一節）；有門牌物件就照後台順序補。
- [ ] 고호재：請站主在 Naver 地圖搜「고호재」（不是「한국의집」）；有獨立條目就填後台核准，沒有就請站主裁示退掉或維持 pending。
- [ ] 站主若決定自填座標：座標來源類型「人工查核」、來源網址填該店 Naver 精準頁，報告註明依據是站主人工查核（違反「地圖平台座標不當耐久來源」的慣例，要站主點頭）。

## How to verify

```bash
npm run test:tools
curl -s -H 'X-Travel-Locale: zh-TW' "https://mokaair.com/api/travel/foods/merchants?destination_id=seoul&limit=50" | python -m json.tool | grep -c '"slug"'
```

後台「待審」＋目的地篩選：首爾應只剩 `seoul-sancheongstar`、`seoul-koreahouse-kohojae`、`seoul-haechen-obu`（加上不相干的 `seoul-gwanghwamun-gukbap`），釜山只剩兩家。

## Notes

- Naver 地圖在 session 的兩個瀏覽器都被安全政策擋，短網址只能讀 307 轉址標頭取 id；座標讀不到。
- 2026-09-23 座標代理的查法與結果在 `docs/catalog-content-reviews/catchtable-batch-2.md` 的「後台操作紀錄」。
