---
id: 2026-09-07-i18n-inline-dicts
title: 文案搬進 catalog：兩個自帶五語系字典的元件
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T07:18:53Z
created_at: 2026-09-07T07:18:52Z
completed_at: 2026-09-07T07:38:10Z
branch: claude/i18n-migrate-batch
depends_on: []
scope:
  - apps/web/components/travel-card-actions.tsx
  - apps/web/components/travel-card-actions.test.tsx
  - apps/web/components/account-saved-items.tsx
  - apps/web/components/account-saved-items.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/account.json
  - apps/web/messages/ja/account.json
  - apps/web/messages/ko/account.json
  - apps/web/messages/zh-TW/account.json
  - apps/web/messages/zh-CN/account.json
---

# 文案搬進 catalog：兩個自帶五語系字典的元件

## Why

後台改文案的三張任務（#311 / #316 / #323）已經上線，但只有進了 next-intl catalog 的
字串改得到。前台還有 34 個檔、1,178 段硬編碼中文完全不在 catalog 裡。

計畫原本按「Han 段數」排序決定搬遷順序，實際掃過內容後發現那不是最好的順序。有兩個檔
**自己內建了完整的五語系字典**，用 `labels[locale].x` 取值、繞過 next-intl：

- `travel-card-actions.tsx`（收藏／加入行程／分享，用在景點與美食小卡）
- `account-saved-items.tsx`（帳號頁的「我的收藏」）

搬這種檔**不需要翻譯任何一個字**，是純機械搬移，而且搬完立刻可在後台編輯。相比之下
段數最多的 `back-to-back-fare-search.tsx`（213 段）多半是航空公司與城市代碼對照表，而且
在低流量的 `/labs/airlines` 實驗頁，價值低得多。

## Definition of done

- [x] 兩個元件不再有任何硬編碼中文，也不再有自己的 locale 字典
- [x] 五個語系的顯示文字與搬移前逐字相同
- [x] 這些文案現在可在 `/admin/ui-text` 編輯

## Steps

- [x] `travel-card-actions.tsx` 的 16 個 key → `common.cardActions`
- [x] `account-saved-items.tsx` 的 8 個 key（含巢狀 `filters`）→ `account.savedItems`
- [x] 移除兩個檔的 `useLocale` 與字典常數

## How to verify

```bash
npm run check:i18n && npm run typecheck:web && npm run lint:web && npm run test:web
```

搬移前後的顯示文字相同，由既有的 `travel-card-actions.test.tsx` 與
`account-saved-items.test.tsx` 保證——它們斷言的是 zh-TW 的實際畫面文字。

## Notes

- **字串是從原始碼取值的，不是手抄**：腳本用 `new Function` 求值那個物件字面量，再逐一
  比對寫入後的值，所以搬移不可能改動任何一個字。
- **`account-saved-items` 原本在元件裡判斷標點**：`locale.startsWith("zh") ? "：" : ": "`。
  既然文案已經進 catalog，改成帶參數的 `savedItems.errorWithDetail`，讓各語系自帶標點，
  locale 判斷整個拿掉。**輸出維持完全相同**——ja/ko 沿用原本的半形冒號，沒有順手「修正」
  成日文慣用的全形冒號，那是內容決定不是搬遷決定。
- **eslint 的 exhaustive-deps 會咬**：原本 deps 陣列裡是 `text.error` 這個字串常數，換成
  `tAccount("savedItems.error")` 就變成函式呼叫、不能靜態檢查。要先抽成變數再放進 deps。
- **`common.json` 與 `account.json` 都已有 `save` / `title` 這類頂層鍵**，所以各自開
  `cardActions` / `savedItems` 群組，不要往頂層攤平。
- 下一批候選（**同樣不需要翻譯的機械搬移已經沒有了**，接下來都要真的寫五語系翻譯）：
  `account-panel.tsx`（70）、`flight-offer-card.tsx`（69）、`flight-status-search.tsx`（54）
  是使用者最常看到的；`back-to-back-fare-search.tsx`（213）與 `airline-fare-lab.tsx`（96）
  在 `/labs` 實驗頁、優先度低；`lib/api.ts`（98）要先把 `apiProblemMessage` 改成執行期
  查表，是另一種工作。
- 這批之後：32 檔、1,082 段。
