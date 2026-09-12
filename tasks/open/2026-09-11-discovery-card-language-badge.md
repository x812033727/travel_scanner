---
id: 2026-09-11-discovery-card-language-badge
title: 推薦流卡片標示內容語言（語言方向 1）
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-11T22:04:42Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/discovery/card.tsx
  - apps/web/components/discovery/card.test.tsx
---

# 推薦流卡片標示內容語言（語言方向 1）

## Why

`2026-09-11-discovery-feed-language-and-dedup` 列了三個方向處理推薦流的語言混雜：

1. **標示**：卡片標出內容語言，使用者自己決定要不要點。
2. **排序**：符合使用者語系的往前排，其他仍然看得到。
3. **過濾**：只給符合語系的。

那張任務做了 **2**（後端排序鍵加一項 `item.locale == locale`），**沒有做 1**，因為那要動
`apps/web/components/discovery/card.tsx`——版面決定不是後端能代勞的，而且那個檔常被其他任務
持有。方向 3 明確排除：內容量是這個產品的命脈，過濾掉外語來源會讓小語系的頁面幾乎空掉。

排序解決了「最相關的那批裡，自己看得懂的排前面」；標示解決的是另一半——**點進去之前就知道
這篇是日文**。繁中讀者在首頁看到六張卡，就算已經按語系排過，第三張之後仍然可能是日文或韓文，
而卡片上沒有任何線索。

## Definition of done

- [ ] 內容語言和讀者語言不同時，卡片上看得出來。
- [ ] 標示本身也是多語系的（不能寫死「日文」三個字）。
- [ ] 相同語言時不要加噪音——大多數卡片不該多一個標籤。

## Steps

- [ ] `DiscoveryItem.locale`（`apps/api/app/discovery/schemas.py:52`）每筆都有，前端已經拿得到，
      不需要動後端。
- [ ] 決定樣式：一個小 badge？來源那一行後面加一句？先看 `card.tsx` 現有的密度再決定。
- [ ] 語言名稱用 `Intl.DisplayNames(readerLocale, { type: "language" })`，不要自己寫五份對照表。

## How to verify

```bash
cd apps/web && npm run test:web -- discovery/card && npm run check:i18n
```

## Notes

- 動工前先確認 `card.tsx` 沒有被別的 in-progress 任務押著。
- 這是三個方向裡最小的一個，而且和方向 2 是互補的，不是二選一。
