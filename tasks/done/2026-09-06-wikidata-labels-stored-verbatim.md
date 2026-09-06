---
id: 2026-09-06-wikidata-labels-stored-verbatim
title: Wikidata 標籤原封不動存入，消歧義括號會顯示給使用者
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T14:24:14Z
created_at: 2026-09-06T13:15:10Z
completed_at: 2026-09-06T14:36:05Z
branch: claude/seed-label-hygiene
depends_on: []
scope:
  - apps/api/app/hotspots/wikidata_labels.py
---

# Wikidata 標籤原封不動存入，消歧義括號會顯示給使用者

## Why

2026-09-06 稽核發現 `apply_labels`（`app/hotspots/wikidata_labels.py`）把 Wikidata 標籤
逐字存進 seed 的 `names`，沒有任何清洗。維基百科的消歧義括號與 MediaWiki 命名空間前綴
因此會直接出現在 en／ja／ko 的顯示名稱裡，以及每個語系的原文欄位。

## Definition of done

- [x] 存入前去掉結尾的消歧義括號與命名空間前綴。
- [x] 有測試涵蓋這兩種形狀。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_wikidata_labels.py
```

```sql
SELECT locale, name FROM hotspot_localizations WHERE name LIKE '%(%)' OR name LIKE '%:%' LIMIT 20;
```

## Notes

從 2026-09-06 的部署稽核分出來。同一個檔案剛修過另一個 bug（PR #227：重建整個 names map
會刪掉它不負責的語系），改動時留意不要退回那個行為。

## Result

實測 7 筆帶有來源痕跡的標籤，全部清乾淨：

| seed | locale | 修正前 | 修正後 |
|---|---|---|---|
| 흰여울문화마을 | en | Category:Huinnyeoul Culture Village | Huinnyeoul Culture Village |
| 弘大 | en | Hongdae (area) | Hongdae |
| 牛車水 | ja | チャイナタウン (シンガポール) | チャイナタウン |
| 八公山 | ja | 八公山 (慶尚北道・大邱広域市) | 八公山 |
| 達城公園 | ja | 達城公園 (大邱広域市) | 達城公園 |
| 孝陵 | ja | 孝陵 (ベトナム) | 孝陵 |
| 順化太和殿 | en | Hall of Supreme Harmony (Imperial City of Huế) | Hall of Supreme Harmony |

`clean_label` 放在 `site_labels`，也就是所有標籤進入 seed 的唯一入口，所以之後抓的也會清。
只移除兩種確定不是名稱的形狀：開頭的 MediaWiki 命名空間、結尾的一個括號限定詞。
名稱中間的括號不動（可能是名稱的一部分），只由限定詞構成的標籤保持原樣（否則會變空）。

測試除了逐筆斷言，還有一條掃過所有 seed 檔，確認沒有任何殘留的來源痕跡。
