---
id: 2026-09-11-footer-links-sixteen-px-tall
title: 頁尾五個連結全站每頁都只有十六像素高
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T14:39:07Z
created_at: 2026-09-11T13:05:04Z
completed_at: 2026-09-11T14:45:04Z
branch: claude/mokaair-website-access-k7xiku
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

- [x] 頁尾五個連結的可點擊區域達到 44px 高。
- [x] 視覺密度不要因此大幅改變（頁尾不該變成主要區塊）。

## Steps

- [x] `site-footer.tsx` 的連結加上 `min-h-11` 與適當的 `inline-flex items-center`，讓點擊區長高但文字基線不動。
- [ ] 這五個連結在 `/about`、`/privacy`、`/terms`、`/contact` 上同時也被底部導覽列蓋住（見 `2026-09-11-bottom-nav-covers-page-content`），兩張一起做比較有效率。

## How to verify

```bash
cd apps/web && npx playwright test --project="Pixel 7"
```

量測方式：`getBoundingClientRect()` 取實際高寬，不是看 class。

## Notes

- 其餘實測到的過小目標，優先度低於頁尾（出現頻率低很多）：社群子導覽 42×82px（22 頁）、「發佈」40×52px（22 頁）、訊息 42×54px。這些與第一輪 `form-validation-and-touch-targets` 的 scope 重疊，留在那張處理。

## 完成紀錄

五個連結加上 `inline-flex min-h-11 items-center`，點擊區由 **16px 變成 44px**，文字基線不動。清單原本的 `gap-2` 同步收斂為 0，否則連結長高後頁尾會鬆散得不成比例。

實測（Playwright，390px）：

```
修正前：隱私權政策 16×70px  display=inline    padding=0/0
修正後：隱私權政策 44×70px  display=inline-flex padding=0/0
```

`e2e/readability.spec.ts` 補了一個斷言「the footer links are big enough to tap」防止再犯。

**這個斷言在本機跑不起來**：repo 釘 `@playwright/test@1.62.1`（需要 chromium revision 1234），容器只有 1194，而環境規定不得執行 `playwright install`。斷言的量測邏輯與上面實測所用的完全相同，CI 有自己的瀏覽器安裝，會實際執行它。

## 為何既有測試沒抓到

`e2e/readability.spec.ts` 原本檢查的是**字級**（`MIN_FONT_PX = 13`）與**對比**，不是點擊區高度。頁尾文字 14px 是合格的，只有命中區不足——兩者是不同的東西，新斷言補上了後者。
