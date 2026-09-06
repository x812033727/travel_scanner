---
id: 2026-09-06-seed-category-shopping-mistakes
title: 四個景點的分類被標成 shopping，其實是公園、城跡與神社
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T15:32:50Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/catalog.py
  - apps/api/tests/test_hotspot_seed_categories.py
---
# 四個景點的分類被標成 shopping，其實是公園、城跡與神社

## Why

種子檔把四個明顯不是購物的地方標成 `category: "shopping"`：

| slug | 名稱 | 實際是什麼 | 合理分類 |
| --- | --- | --- | --- |
| `sdj-q11541912` | 榴岡公園（仙台） | 賞櫻公園 | `nature` |
| `hij-q41977` | 廣島城 | 城跡與歷史博物館 | `culture` |
| `hij-q191763` | 嚴島神社 | 世界遺產神社 | `culture` |
| `tae-q624313` | 八公山（大邱） | 山與國立公園 | `nature` |

影響有三個：熱門景點頁的「購物」篩選會混進四個非購物景點；卡片的分類文字直接寫錯；AI 規劃器把 `shopping` 興趣對應到 `category="shopping"`（`apps/api/app/hotspots/service.py:63-71`），所以說「想逛街」的旅客會被排進嚴島神社。

發現於 2026-09-06 加季節主題時——這四個地方都要掛賞櫻或賞楓，一看分類就不對。主題是另一個維度，已經照實掛好，不受這張任務影響。

## Definition of done

- [ ] 四筆的 `category` 改成上表的值，`/hotspots?category=shopping` 不再回傳它們。
- [ ] 有一個測試擋住同類錯誤再發生。

## Steps

- [ ] 在 `apps/api/app/hotspots/catalog.py` 的 `CATEGORY_CORRECTIONS` 加這四個名稱（那張表就是為了這種事存在的），或直接改對應 bootstrap JSON 的 `category`。兩者擇一，別兩邊都寫。
- [ ] 順手看一遍其餘 81 筆 `shopping`，確認沒有第五個。
- [ ] `tests/test_hotspot_seed_categories.py`（新）：`shopping` 的種子名稱不得出現「神社」「寺」「城」「公園」「山」這類字樣，例外要逐筆寫進允許清單並附理由。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_seed_categories.py tests/test_kanto_expansion.py -q
cd apps/api && uv run python -c "from app.hotspots.catalog import HOTSPOT_SEEDS; print([s.name for s in HOTSPOT_SEEDS if s.category=='shopping'])"
```

## Notes

- 改分類會動到 `search_text`（`catalog.py` 用分類組出來的），下一次 collect run 會自己刷新，不用資料遷移。
- 這四筆的季節主題（`theme_bootstrap.json`）不必動：主題和分類互相獨立。
