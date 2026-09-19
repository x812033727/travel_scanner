---
id: 2026-09-11-discovery-card-language-badge
title: 推薦流卡片標示內容語言（語言方向 1）
status: review
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:09:26Z
created_at: 2026-09-11T22:04:42Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
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

- [x] 內容語言和讀者語言不同時，卡片上看得出來。
- [x] 標示本身也是多語系的（不能寫死「日文」三個字）。
- [x] 相同語言時不要加噪音——大多數卡片不該多一個標籤。

## Steps

- [x] `DiscoveryItem.locale`（`apps/api/app/discovery/schemas.py:52`）每筆都有，前端已經拿得到，
      不需要動後端。
- [x] 決定樣式：一個小 badge？來源那一行後面加一句？先看 `card.tsx` 現有的密度再決定。
- [x] 語言名稱用 `Intl.DisplayNames(readerLocale, { type: "language" })`，不要自己寫五份對照表。

## How to verify

```bash
cd apps/web && npm run test:web -- discovery/card && npm run check:i18n
```

## Notes

- 動工前先確認 `card.tsx` 沒有被別的 in-progress 任務押著。
- 這是三個方向裡最小的一個，而且和方向 2 是互補的，不是二選一。

### 2026-09-19 done in repo (claude-fable-5-1)

- 樣式：來源那一行（來源種類 · 作者／來源 · 日期）最後面加一顆 11px、`--line` 細框、繼承 `--muted`
  字色的小圓角 badge，只用 Tailwind utility——`discovery.module.css` 不在 scope，裡面也沒有合適的
  小 badge class（`.chip` 是 44px 的篩選 chip）。看得到的字只有語言名稱；螢幕閱讀器另外聽到
  `getDiscoveryCopy(locale).language`（「內容語言」／"Content language"）當前綴，沿用 `reason` 那行的
  sr-only 寫法，所以不需要新的 message key，scope 不變。
- 語言名稱：`contentLanguageName(readerLocale, item.locale)`（從 `card.tsx` export）先用
  `Intl.getCanonicalLocales` 正規化兩邊再比較完整 tag——和後端排序鍵 `item.locale == locale`
  同一個判準，所以 zh-TW 讀者看 zh-CN 內容仍會標「中文（中國）」；不同才用
  `Intl.DisplayNames(reader, { type: "language", fallback: "none" })` 取名，每個讀者語系共用一個
  formatter。tag 解析不了、沒有名字（xx／und）、空值、或執行環境沒有 `Intl.DisplayNames`，都回
  null，卡片維持原樣。
- 測試 `card.test.tsx`（新檔）：相同語系（含大小寫、前後空白差異）無 badge；zh-TW 讀者看 ja 是
  「日文」、en 讀者是 "Japanese"，其餘組合直接和 CLDR 的答案比對；badge 在來源行最後、日期之後，
  不進第一行的 topic meta；空／未知／非法 locale 不加也不炸。
- 驗證：`cd apps/web && npx vitest run components/discovery/card.test.tsx` 23 passed；
  `npx vitest run components/discovery` 11 files、125 passed；root `npm run check:i18n`
  Validated 5 locales across 25 namespaces；`npm run typecheck:web` 通過（第一次跑時撞到別的 agent
  正在改的 `admin-settings-panel.test.tsx` 暫時報錯，重跑乾淨）；`npm run lint:web` 通過。
- 順手發現但不在這張票裡：詳情頁「原文語言」那一行仍印 locale code（`原文語言: ja`），另開
  `2026-09-19-discovery-details-name-the-original-language`。
