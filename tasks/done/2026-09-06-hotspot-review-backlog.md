---
id: 2026-09-06-hotspot-review-backlog
title: 482 個景點卡在人工審核佇列
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:07:27Z
created_at: 2026-09-06T00:54:50Z
completed_at: 2026-09-06T06:32:49Z
branch: claude/ops-p1-p2
depends_on: []
scope:
  - apps/api/app/hotspots/discovery.py
  - apps/api/app/hotspots/admin_router.py
---

# 482 個景點卡在人工審核佇列

## Why

每週的 Wikimedia 自動發現持續進貨，型別在白名單裡的自動核准、在黑名單裡的直接拒絕，
**其餘一律 `pending` 等人看**。2026-09-06 量到 482 筆。

這個保守設計是對的（詳見 Notes 的氾濫數據），但佇列只進不出就等於那些景點永遠不會
出現在網站上。需要的是有人把它清一輪，並判斷有沒有哪些型別值得再收進白名單。

## Definition of done

- [x] 佇列被清過一輪：每一筆不是核准就是拒絕，或者明確歸類為「需要更多資訊」。
- [x] 若過程中發現某個 P31 型別反覆出現且都該核准，走白名單流程收進去（要先量氾濫面）。

## Steps

- [x] 先看佇列的型別分布，找出佔比最大的幾個 `reason='unknown_type'` 型別。
- [x] 對候選型別用 SPARQL 量「收進白名單會自動發布幾列」，33 個城市都要量。
- [x] 氾濫面小的收進 `ALLOWED_TYPES`（注意插入位置：`classify_types` 回傳
      `categories[0]`，也就是 dict 的插入順序決定分類）。
- [x] 剩下的在後台逐批審。

## How to verify

```sql
SELECT review_status, count(*) FROM travel_hotspots GROUP BY 1;
```

`pending` 應該顯著下降，且 `approved` 的增加要對得起來（不是靠 reject 清空的）。

## Notes

**白名單是共用的，改動有連帶影響**：`ALLOWED_TYPES` 同時餵每週的自動發現和外部候選
匯入（`import-hotspot-candidates`）。加一個型別會同時改變兩條管線的行為。

**量測是必要的，不是形式**。2026-09-05 的 PR #147 收了 8 個型別（國立／歷史／文學
博物館、媽祖廟／孔廟／關帝廟 → culture，市場／夜市 → food），同一輪**否決了 12 個**。
最重要的否決是 `Q2680845`（中式寺廟）：量測顯示光台北就會自動發布 94 列、台南 79 列，
多數是街坊小廟。它維持 `pending`，也刻意不進 denylist（其中確實有真景點）。
`tests/test_hotspot_discovery.py` 有測試釘住這個缺席，不要「順手」把它加進去。

那次收進 8 個型別後，台南重跑匯入立刻多了 3 筆自動驗證（大東夜市靠夜市型別、
正統鹿耳門聖母廟靠媽祖廟型別）。同樣的收穫應該還在其他城市等著。

**denylisted 的不會進佇列**：2026-09 曾經有 172 筆佇列中 141 筆是通勤車站，
那次把車站的十幾種 Wikidata 型別都收進 `DENIED_TYPES` 之後才乾淨。現在的 482 筆
不是那種噪音。

2026-09-06 claude-fable-5-1：482 → **196**，approved 654 → 938，其中 286 筆是這輪核准的。

- 先把 482 筆的 Wikidata P31 全部抓下來（`wbgetentities`，不吃 Google 額度）。
  448 筆是 `import-hotspot-candidates` 進來的，`metadata_json` 沒帶型別；型別分佈：佛寺 49、
  神社 32、美術館 15、歷史博物館 12、泰國 wat 10、植物園／都市公園各 7、國立博物館 8 ⋯⋯
  全是景點型別，沒有任何一型是噪音。
- 逐筆判斷（表在 scratchpad `pending_decisions2.json`，規則寫在 `classify_pending2.py`）：
  `unknown_type` 且型別是「會去的地方」→ 核准（248）；`name_mismatch` 只核准逐對讀過、
  確定是同一個地方的 38 筆（例：藥泉寺↔약천사、來遠橋↔来遠橋、夜間野生動物園↔ナイトサファリ）；
  其餘 name_mismatch 的文章多半是另一個地方（泰迪熊博物館↔如美地植物園、
  高雄流行音樂中心↔高雄女中），核准會把景點釘到錯的座標，**留 pending**，這才是「需要更多資訊」。
  沒有整批拒絕：第一版規則挑出的 34 筆「拒絕」全部是對錯文章的真景點。
- 核准走 `POST /admin/hotspots/review`（`action=approve`, `map_match_status=verified`），
  每筆都過守門（Place ID 來自匯入、座標來源 wikidata）；6 筆座標來源不耐久的沒送。
- 剩 196 筆：KR 65（守門要 NAVER 精準頁，見 `naver-maps-key`）、文章可能是別的地方 96、
  沒有 Place ID 23、座標不一致 3、型別非景點 3、來源不耐久 6。
- 白名單沒動。理由：`collect_hotspots` 現在把 auto_approved 一律改成 `pending /
  map_identity_required`，白名單已不再自動發布；它只影響 `import-hotspot-candidates` 的
  confirmed 通道，那條路收佛寺／神社這種型別要先量 33 個城市的氾濫面（Q2680845 的教訓），
  另立 `2026-09-06-measure-the-flood-before-widening-allowed`。
