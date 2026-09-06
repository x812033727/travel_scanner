---
id: 2026-09-06-kanto-place-ids
title: 6 個關東景點需要人工挑 Google Place ID
status: done
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:07:27Z
created_at: 2026-09-06T00:55:26Z
completed_at: 2026-09-06T06:32:49Z
branch: claude/ops-p1-p2
depends_on: []
scope:
  - apps/api/app/hotspots/catalog.py
---

# 6 個關東景點需要人工挑 Google Place ID

## Why

關東擴充（東京 83 個新景點，加上橫濱 `YOK`、鎌倉 `KMK` 兩個新目的地）之後，批次
`match-hotspot-places` 幫多數景點填好了 Place ID，但有 6 個關東的列自動比對挑不出
唯一候選，停在待人工選擇的狀態。

數量很小，但沒有 Place ID 就沒有精準地圖識別，這 6 個景點永遠不會發布。

## Definition of done

- [x] 6 個都有正確的 Place ID，或被判定為不該收錄而拒絕。

## Steps

- [x] 撈出關東（NRT/YOK/KMK）沒有 `google_place_id` 的已核准景點。
- [x] 用後台的 `/admin/hotspots/map-candidates` 逐筆看候選，或
      `python -m app.cli match-hotspot-places --destination tokyo --approve <slug>`。
- [x] 填完之後跑一次驗證讓 `map_match_status` 翻成 `verified`。

## How to verify

```sql
SELECT slug, name FROM travel_hotspots
WHERE city_code IN ('NRT','YOK','KMK') AND review_status = 'approved'
  AND google_place_id IS NULL;
```

## Notes

**Place ID 從來不寫在種子檔裡**，一律在正式機上用 CLI 補：
`python -m app.cli match-hotspot-places --destination tokyo …`（包了
`enrich_hotspot_place`，到免費額度 90% 會自己煞車，`--approve SLUG` 把待審候選轉正）。

**Wikidata 的座標會騙人**，關東這批就踩過兩次：teamLab Borderless 的座標指向已經搬走
的舊台場館址、目黒川指到河口。產生器裡的 `PREFER_OVERRIDE` 集合就是為了強制使用人工
複核過的座標而存在的，遇到類似狀況往那邊加。

**額度警告**：`place_details` 走的是 Enterprise 級距，2026-09 時本月免費額度只剩
一百多次。只有 6 筆所以無所謂，但不要順手拿這條路徑去跑大批次 ——
Text Search Pro（`detailed=False`）才是批次該用的。

2026-09-06 claude-fable-5-1：撈 `city_code in ('NRT','YOK','KMK') and google_place_id is null`
只剩 **1 筆**，其餘 5 筆在這張任務立案後已被 `match-hotspot-places` 的例行批次補上。
剩下的 `nrt-otome-road`（池袋乙女路）：前一位審核者已把 place profile 標 rejected，理由是
Google 沒有這條街本身的 POI、不該錨到某一家店；本次沒有再打 Google，沿用該結論。決定：不錨、不拒絕
（它是真的景點區），留在 approved / unverified，等 Google 有對應 POI 再補。
