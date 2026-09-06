---
id: 2026-09-06-wikidata-labels-stored-verbatim
title: Wikidata 標籤原封不動存入，消歧義括號會顯示給使用者
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T13:15:10Z
completed_at:
branch:
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

- [ ] 存入前去掉結尾的消歧義括號與命名空間前綴。
- [ ] 有測試涵蓋這兩種形狀。

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
