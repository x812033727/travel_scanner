---
id: 2026-09-19-foreign-place-reason
title: foreign_place 的三種誤判形狀：短片假名國名、含國名的地標名與別名缺口、reason 寫錯國家
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-19T08:51:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/guides.py
  - apps/api/tests/test_hotspot_guides.py
---

# foreign_place 的三種誤判形狀：短片假名國名、含國名的地標名與別名缺口、reason 寫錯國家

## Why

`guides-foreign-place-scan`（PR #559）掃出 165 筆，人工逐筆判讀 117 筆（`2026-09-19-review-117-flagged-foreign-guides`）
之後，`docs/catalog-content-reviews/2026-09-19-foreign-guides-review.md` 記下三種會重複出現的誤判形狀，
不是單一列的問題：

1. **短的假名國名用子字串比對**：「タイ」在 タイム／スタイル／タイプ 裡也會命中；再加上標題把店名改寫
   （「MEGA(メガ)ドン・キホーテ 渋谷本店」對不上 ja 名稱）、只寫區名（渋谷区 不在東京的別名裡），NAVITIME
   自家的店頁 `6da32c2d` 就被判成泰國。
2. **地標名本身含另一個國家的名字**（日本橋／來遠橋、玉山），加上景點名拼法變體（古城 vs 古鎮）與缺少的別名
   （會安古城沒有 會安／Hội An／ホイアン），hoiana.com 真正寫會安的文章 `c4706b00` 兩次被判成日本。
3. **判斷對了但 `elsewhere` 寫錯國家**：同一個部落格首頁在不同列被寫成 台灣／台南／沖繩，同一頁指南宮被寫成
   泰國與台灣——寫進 `review_reason` 的國名不可靠。

## Definition of done

- [ ] 短假名國名（タイ、韓国 之外的兩字詞）要求假名邊界或改用詞表比對；`6da32c2d` 那種標題不再命中。
- [ ] `country_mentions` 之前先剝掉已知的含國名地標（日本橋、玉山……可列在一張小表裡）；會安古城補上別名。
- [ ] `elsewhere` 取「最常被提到的國家」或「標題裡的國家」而不是第一個命中，測試涵蓋文件裡的例子。
- [ ] 上面每一條在 `tests/test_hotspot_guides.py` 有一個以文件例子寫成的測試。

## Steps

- [ ] 讀 `2026-09-19-foreign-guides-review.md` 的三節與例子 id，先把例子寫成會紅的測試。
- [ ] 改 `foreign_place` / `country_mentions` / `mentions_place`，測試轉綠，既有測試不動。
- [ ] 用 `guides-foreign-place-scan`（list only）在主機重跑一次，確認 keep 清單裡的列不再命中。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_guides.py -q
```

## Notes

- 來源文件與例子：`docs/catalog-content-reviews/2026-09-19-foreign-guides-review.md`。
- 「市場」的雙義（釜山國際市場 → JNTO／JETRO 的「市場分析」）與部分名稱同音（第二市場→二条市場、豐南門→台南）
  是探索端的問題，不在這張票；那些列已在 117 筆裡退掉。
