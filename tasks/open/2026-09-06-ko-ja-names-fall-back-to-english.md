---
id: 2026-09-06-ko-ja-names-fall-back-to-english
title: ko 與 ja 的景點名稱多半退回英文
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T10:10:29Z
created_at: 2026-09-06T09:56:52Z
completed_at:
branch: claude/wikidata-locale-labels
depends_on: []
scope:
  - apps/api/app/hotspots/wikidata_labels.py
  - apps/api/tests/test_wikidata_labels.py
  - apps/api/tests/test_trip_item_localization.py
---

# ko 與 ja 的景點名稱多半退回英文

## Why

2026-09-06 正式站實測，`hotspot_localizations` 568 筆中與英文逐字相同的比例：

| locale | 與 en 相同 | 佔比 |
|---|---|---|
| ko | 487 | 86% |
| ja | 354 | 62% |

也就是韓文使用者有近九成的景點看到英文名（例：Rainbow Bridge、Ocean Park Hong Kong），
日文使用者也有六成。ja 有正確翻譯時會顯示（レインボーブリッジ、中野ブロードウェイ），
所以是資料覆蓋率問題而非讀取問題。

有些條目本來就沒有在地名稱（西方品牌、英文原名），退回英文是對的；要先分辨哪些是
「真的沒有」哪些是「還沒填」。

## Definition of done

- [ ] 有一份清單分出「應該有在地名稱但目前是英文」與「本來就用英文」。
- [ ] 前者補上 ja／ko 名稱，覆蓋率有可量測的提升。

## Steps

- [ ] 用 Wikidata 標籤（`app/hotspots/wikidata_labels.py` 已有這條路）先補能自動對上的。
- [ ] 剩下的列出來，決定是人工補還是接受英文。

## How to verify

```sql
SELECT l.locale, count(*) FILTER (WHERE l.name = e.name) FROM hotspot_localizations l JOIN hotspot_localizations e ON e.hotspot_id=l.hotspot_id AND e.locale='en' GROUP BY 1;
```

## Notes

zh-CN 是不同的問題（整批複製繁體），見 [[2026-09-06-zh-cn-names-are-traditional]]。
