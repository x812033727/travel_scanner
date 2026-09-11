---
id: 2026-09-11-merchant-coordinate-queue-i18n
title: 店家座標佇列面板整個沒有 i18n
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T21:30:23Z
created_at: 2026-09-11T18:24:45Z
completed_at: 2026-09-11T21:43:11Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/admin-merchant-coordinate-queue.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/components/admin-merchant-coordinate-queue.test.tsx
---

# 店家座標佇列面板整個沒有 i18n

## Why

`admin-merchant-coordinate-queue.tsx` 完全沒有 `useTranslations`，整個面板的文字都是寫死的繁體中文：欄名（`COLUMNS`）、「Google Places 金鑰未設定，無法解析候選。」、按鈕與狀態文字。

做 `2026-09-11-admin-tables-unusable-on-phone` 時發現的：要給每個 `<td>` 補欄名，只能直接引用那四個中文字串。當時把它們抽成一個 `COLUMNS` 常數讓 `<th>` 與 `data-label` 共用，避免把同樣的漢字再寫一次（`tools/check-i18n.mjs` 的漢字增量守門會擋），但面板本身仍然只有中文。

## Definition of done

- [x] 面板沒有寫死的使用者可見中文。
- [x] 五語系 catalog 齊全，`npm run check:i18n` 通過。

## Steps

- [x] 字串搬進 `messages/*/admin.json`（照其他後台面板的做法，例如 `hotspotPlacesPanel.*`）。
- [x] `COLUMNS` 改成從 catalog 取，`data-label` 跟著改。
- [x] 加一個跨語系測試：catalog 回傳 key 時畫面零漢字（做法見 `components/account-list-i18n.test.tsx`）。

## How to verify

```bash
cd apps/web && npm run check:i18n && npm run test:web -- merchant-coordinate
```

## Notes

- 標 P2 是因為這是後台單一佇列面板，站主自己看得懂中文；但它和其他後台面板不一致，而且 `admin.json` 的 UI 文案編輯器編不到它。

## claim 用了 --force，理由（claude-opus-5, 2026-09-11）

`messages/*/admin.json` 同時在兩張 in-review 的任務 scope 裡，兩張的工作都已經合併進 main，
只是沒標 `done`：

- `2026-09-11-food-reservation-platforms`（codex-food-reservation-platforms）——遠端分支
  `codex/food-reservation-platforms` 已不存在，工作是 `19a9429 feat(foods): 獨立儲存訂位平台與多平台支援 (#392)`。
- `2026-09-11-travel-guides-web`（claude-opus-5-guides）——遠端分支已不存在，工作是
  `1da7850 feat(guides): 旅遊情報與攻略專區——第一方內容 API、公開頁面與後台編輯器 (#398)`。

用側 catalog（像 `lib/itinerary-messages/`）可以完全避開這個衝突，但這張任務的重點之一就是
「`admin.json` 的 UI 文案編輯器編不到它」——放進側 catalog 等於沒解決那一半。

## 完成紀錄（claude-opus-5, 2026-09-11）

三十一個 key 進 `messages/*/admin.json` 的 `merchantCoordinateQueue`（含七個 `outcome.*`），
面板改用 `useTranslations("admin.merchantCoordinateQueue")`。整個檔零漢字。

放進 `admin.json` 而不是側 catalog，是因為 Notes 說的那半件事：站主的 UI 文案編輯器只編得到
`admin.json` 裡的東西。側 catalog 可以完全避開 scope 衝突，但會讓那個編輯器仍然編不到它。

### 三個順手處理掉的細節

- **`OUTCOME_LABELS` 改成 `OUTCOMES` 白名單。** 原本 `OUTCOME_LABELS[x] ?? x`：查不到就印
  後端送來的代碼。現在是「認得的翻譯，不認得的照樣印代碼」——**刻意保留這個行為**，因為這是
  後台：站主需要看到「有東西被略過」以及略過的理由，即使理由來自比這個版本新的伺服器。
  （這和前端 `translateWarnings` 把不認得的代碼丟掉相反，那邊是給旅客看的。）
- **略過理由的分隔符改用 `Intl.ListFormat`。** 原本 `join("、")`——那是中文的頓號，在英日韓
  都不對。
- **`COLUMNS` 改成 `COLUMN_KEYS`**，表頭與每個 `<td>` 的 `data-label` 都從同一個翻譯後的
  陣列取。`2026-09-11-admin-tables-unusable-on-phone` 當時抽出 `COLUMNS` 常數就是為了不要把
  同樣的漢字寫兩次；現在那個理由消失了，但共用同一份清單仍然是對的——手機版的欄名不會和
  表頭對不上。測試裡直接斷言 `columnheader` 的文字序列等於 `data-label` 的序列。

### 驗證

`components/admin-merchant-coordinate-queue.test.tsx`：照 `account-list-i18n.test.tsx` 的做法
把 next-intl 換成「回傳 key 本身」的假 catalog，以英文讀者的身分渲染，斷言畫面零漢字。
fixture 是韓國店家 + `verdict: "check"` + `place_id_taken`，把所有分支都渲染到。
把其中一句改回寫死的中文，這條轉紅（實測）。
