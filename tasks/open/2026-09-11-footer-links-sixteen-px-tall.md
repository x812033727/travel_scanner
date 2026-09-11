---
id: 2026-09-11-footer-links-sixteen-px-tall
title: 頁尾五個連結全站每頁都只有十六像素高
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T13:05:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/site-footer.tsx
---

# 頁尾五個連結全站每頁都只有十六像素高

## Why

實測 162 個頁面的可互動元素尺寸，共 945 處低於 44px 的觸控標準。**數量最多的就是頁尾**：

| 連結 | 實測尺寸 | 出現頁數 |
| --- | --- | --- |
| 隱私權政策 | **16 × 70 px** | 74 |
| 服務條款 | **16 × 56 px** | 74 |
| 目的地 | **16 × 42 px** | 74 |
| 關於 Mokaair | **16 × 88 px** | 72 |
| 聯絡我們 | **16 × 56 px** | 72 |

16px 高度不到房規 44px 的四成，而且**每一頁都有**。房規本身是清楚的：`min-h-11` / `h-11` 在 96 個檔案裡出現 673 次，`globals.css:407-410` 的 `.app-icon-button` 是 2.75rem 見方——頁尾是漏網之魚。

第一輪稽核的 `2026-09-11-form-validation-and-touch-targets` 列了七處過小的目標，但**完全沒掃到頁尾**，因為那一輪是讀程式碼，沒有實際量測渲染後的尺寸。

## Definition of done

- [ ] 頁尾五個連結的可點擊區域達到 44px 高。
- [ ] 視覺密度不要因此大幅改變（頁尾不該變成主要區塊）。

## Steps

- [ ] `site-footer.tsx` 的連結加上 `min-h-11` 與適當的 `inline-flex items-center`，讓點擊區長高但文字基線不動。
- [ ] 這五個連結在 `/about`、`/privacy`、`/terms`、`/contact` 上同時也被底部導覽列蓋住（見 `2026-09-11-bottom-nav-covers-page-content`），兩張一起做比較有效率。

## How to verify

```bash
cd apps/web && npx playwright test --project="Pixel 7"
```

量測方式：`getBoundingClientRect()` 取實際高寬，不是看 class。

## Notes

- 其餘實測到的過小目標，優先度低於頁尾（出現頻率低很多）：社群子導覽 42×82px（22 頁）、「發佈」40×52px（22 頁）、訊息 42×54px。這些與第一輪 `form-validation-and-touch-targets` 的 scope 重疊，留在那張處理。
