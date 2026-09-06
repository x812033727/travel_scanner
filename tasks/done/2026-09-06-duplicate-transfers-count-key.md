---
id: 2026-09-06-duplicate-transfers-count-key
title: 五個語系的 trips.json 都有重複的 transfersCount 鍵
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T17:25:06Z
created_at: 2026-09-06T16:25:55Z
completed_at: 2026-09-06T17:33:16Z
branch: claude/duplicate-i18n-keys
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
  - tools/json-duplicate-keys.mjs
  - tools/json-duplicate-keys.test.mjs
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

## Result（2026-09-07 完成）

重複的不只一組。掃過 21 個 namespace × 5 個語系之後，找到**兩組**，而且第二組不是無害的。

### `trips.json` 的 `route.transfersCount`：無害，照計畫刪前面那個

執行中的值（`{count} transfers` / `乗換 {count} 回` / `환승 {count}회` / `换乘 {count} 次` /
`轉乘 {count} 次`）一個字都沒變。

### `foodAdmin.json` 的 `tabs`：整塊被丟掉，這組原本可能咬人

重複的是**物件**，所以第一個 `tabs` 整塊被 `JSON.parse` 丟掉，不是只丟掉重疊的欄位：

```json
"tabs": {"label": "Food catalog workspaces", ..., "catalog": "Food catalog", "merchants": "Merchants & maps"},
...
"tabs": {"label": "Food admin sections", ..., "merchants": "Merchants", "coordinates": ..., "taxonomy": ..., "dishes": ...},
```

第一塊有 `catalog`，第二塊沒有。只要有人寫 `t("tabs.catalog")` 就會在執行期壞掉，而且五個
語系一起壞。查過了：`admin-foods-workspace.tsx` 的 `tabKeys` 是
`["merchants", "coordinates", "taxonomy", "dishes"]`，四個都在勝出的那一塊裡，`catalog`
全站沒有任何引用。所以那塊是舊版兩分頁配置留下來的死資料，刪掉沒有任何行為變化——但它會在
下一個人加分頁時變成一顆地雷。

### 偵測

`JSON.parse` 幫不上忙：它保留最後一個而且什麼都不說，所以 `check-i18n.mjs` 原本的每一項檢查
都看不見重複鍵——它自己也是先 parse 再檢查的。改成掃描原始文字：新的
[`tools/json-duplicate-keys.mjs`](../../tools/json-duplicate-keys.mjs) 走過字串字面值與物件
巢狀，看到一個字串後面接冒號就當成鍵。九個測試在
[`tools/json-duplicate-keys.test.mjs`](../../tools/json-duplicate-keys.test.mjs)，包含實際
出過事的那一組，以及會騙過草率實作的幾種輸入：值裡面的冒號、跳脫的引號、兄弟物件的同名鍵、
陣列裡的物件、需要反跳脫的鍵名。

沒有重新格式化任何 JSON，每個檔案就是少一行。

檢查：`check:i18n`、`test:tools`（27 passed）、`lint:web`、
`test:web -- route-mode-panel admin-foods`（15 passed）全綠。
