---
id: 2026-09-06-duplicate-transfers-count-key
title: 五個語系的 trips.json 都有重複的 transfersCount 鍵
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T17:27:19Z
created_at: 2026-09-06T16:25:55Z
completed_at: 2026-09-06T17:33:15Z
branch: claude/duplicate-transfers
depends_on: []
scope:
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/en/foodAdmin.json
  - apps/web/messages/ja/foodAdmin.json
  - apps/web/messages/ko/foodAdmin.json
  - apps/web/messages/zh-CN/foodAdmin.json
  - apps/web/messages/zh-TW/foodAdmin.json
  - tools/check-i18n.mjs
  - tools/duplicate-keys.mjs
  - tools/duplicate-keys.test.mjs
---

# 五個語系的 trips.json 都有重複的 transfersCount 鍵

## Why

`apps/web/messages/*/trips.json` 的 `editor` 區塊裡，`transfersCount` 出現兩次，五個語系
都一樣：

```json
"transfersCount": "{count} 次",      // 前面這個
...
"transfersCount": "轉乘 {count} 次",  // 後面這個
```

`JSON.parse` 保留最後一個，所以**畫面現在顯示的是對的**（en 是 `{count} transfers`、
ja 是 `乗換 {count} 回`、ko 是 `환승 {count}회`、zh-CN 是 `换乘 {count} 次`）。這不是使用者
看得到的缺陷，所以是 P3。

真正的代價是檔案本身壞掉：任何工具只要把 JSON 讀進來再寫回去（格式化、排序、批次改一個鍵），
重複鍵就會被折疊，diff 裡就會多出兩行看起來像文案變更、其實只是折疊產物的雜訊。
2026-09-06 做 `2026-09-06-ai-warning-copy` 時就撞到一次：那次是用 Python 讀 JSON、加一個
鍵、再寫回去，結果五個檔案各多出一組 `transfersCount` 的假變更。當時改成純文字插入繞開了，
但下一個人會再撞一次。

`tools/check-i18n.mjs` 沒有抓到，因為它也是用 `JSON.parse` 讀檔——解析器早就把重複鍵吃掉了，
檢查器看到的是折疊後的結果。

## Definition of done

- [x] 五個 `trips.json` 各只有一個 `transfersCount`，值是目前實際生效的那個（後面那個）。
- [x] `tools/check-i18n.mjs` 會在任何 message 檔出現重複鍵時失敗，所以這件事不會再發生。
- [x] 畫面文案完全不變。

## Steps

- [x] 刪掉五個檔案裡**前面**那個 `transfersCount`，保留後面那個（就是現在生效的值）。
- [x] 在 `tools/check-i18n.mjs` 加重複鍵偵測。`JSON.parse` 幫不上忙，要用
      `JSON.parse(raw, reviver)` 之外的方式——最簡單是逐檔用一個記錄 key 路徑的
      `reviver` 抓不到重複，所以改用逐行掃描同層縮排的 `"key":` 或引入一個會保留重複的
      解析方式。實作前先確認選的做法真的抓得到，用一個故意放重複鍵的 fixture 驗證。
- [x] 順手確認其他 20 個 namespace 有沒有同樣問題（同一個掃描一次跑完）。

## How to verify

```bash
node tools/check-i18n.mjs
npm run test:web -- route-mode-panel
```

重複鍵的計數（修好之後每個檔案都應該是 1）：

```bash
grep -c '"transfersCount"' apps/web/messages/*/trips.json
```

## Notes


不要順手把整份 JSON 重新格式化，那會製造一個沒人想 review 的大 diff。只刪那五行。

這張票是 `2026-09-06-ai-warning-copy` 的副產物，那張票刻意沒有一起修，因為折疊重複鍵會讓
它的 diff 混進五組看起來像文案變更的假變更。

### 做完之後（2026-09-07，claude-opus-5）

**「順手確認其他 20 個 namespace」有結果**：`foodAdmin.json` 的 `tabs` 五個語系都重複。
前面那個是四個分頁（美食目錄工作區／catalog／merchants），後面那個是六個（美食管理分頁／merchants／
coordinates／taxonomy／dishes）。`AdminFoodsWorkspace` 用的 `tabKeys` 只有後面那組有，
所以生效的一直是後面那個，前面那組整組是死的——刪掉畫面不變。scope 因此多了那五個檔案。

偵測寫成獨立模組 `tools/duplicate-keys.mjs`，理由是 `check-i18n.mjs` 在 import 時就會執行檢查
並 `process.exit`，測試沒辦法直接 import 它。掃描器逐字走原始文字（`JSON.parse` 看不到重複鍵），
需要正確處理三件事，測試各釘一條：值裡面的冒號（`"來源：內閣府"`、URL）、跳脫的引號、
陣列裡的字串不能被當成鍵。路徑要記 `lastKey`——`:` 那一步會把 `pendingKey` 清掉，
所以進 `{` 的時候得用另一個變數才知道自己在哪個鍵底下。

`tools/check-i18n.mjs` 現在對五個語系 × 21 個 namespace 都跑這個掃描。
