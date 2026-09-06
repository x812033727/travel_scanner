---
id: 2026-09-06-non-chinese-seed-names-as-chinese-labels
title: seed 的韓文假名泰文名稱被當成中文標籤輸出
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T13:15:08Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/catalog.py
  - apps/api/app/localized_names.py
---

# seed 的韓文假名泰文名稱被當成中文標籤輸出

## Why

2026-09-06 稽核發現：26 筆 seed 的策展 `name` 本身就不是中文（韓文諺文、日文假名、泰文），
但 `name` 同時是 zh-TW 標籤、也是 zh-CN 沒有轉換時的退回值，所以中文讀者看到的是諺文或泰文。
沒有 Wikidata 標籤的那幾筆（例如 사려니숲길）連 en 與 ja 也是同一個字串。

另外 45 筆完全沒有中文名稱，zh-TW 與 zh-CN 顯示拉丁字母、諺文或越南文。

## Definition of done

- [ ] 分辨「本來就沒有中文名稱」與「有但沒填」，前者補上，後者接受並記錄。
- [ ] 中文語系不再出現整串諺文或泰文，除非那確實是該地點唯一的名稱。

## How to verify

```sql
SELECT h.name, l.locale, l.name FROM hotspot_localizations l JOIN travel_hotspots h ON h.id=l.hotspot_id WHERE l.locale IN ('zh-TW','zh-CN') AND l.name ~ '[가-힣ก-๛ぁ-ヿ]' LIMIT 30;
```

## Notes

從 2026-09-06 的部署稽核分出來。相關：[[2026-09-06-ko-ja-names-fall-back-to-english]]。
