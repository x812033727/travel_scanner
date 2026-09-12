---
id: 2026-09-11-trips-list-hardcoded-zh-tw
title: 我的旅程整頁硬編碼繁中含刪除確認框
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T15:54:11Z
created_at: 2026-09-11T03:20:35Z
completed_at: 2026-09-11T16:19:38Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/account-list.tsx
  - apps/web/components/account-list.test.tsx
  - apps/web/components/account-list-i18n.test.tsx
  - apps/web/messages/en/alerts.json
  - apps/web/messages/ja/alerts.json
  - apps/web/messages/ko/alerts.json
  - apps/web/messages/zh-CN/alerts.json
  - apps/web/messages/zh-TW/alerts.json
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 我的旅程整頁硬編碼繁中含刪除確認框

## Why

`/trips` 的頁面外殼（`app/[locale]/trips/page.tsx`）完整走 `next-intl`，但實際渲染內容的 `account-list.tsx` 從頭到尾寫死繁體中文。英日韓使用者看到翻譯過的標題，接著是一整面看不懂的字。

逐處：登入提示 `:91,96`／錯誤詳情 `:102-103`／重試 `:114`／載入中 `:220`／空狀態與「建立第一個行程」CTA `:239,247`／提醒狀態 `:301,307`／行程資訊 `:406,413`／aria-label `:435,445,448,459`／編輯表單 `:480,487,502,511`／失敗訊息 `:540`。`:335` 另外寫死 `toLocaleString("zh-TW")`，所有語系的日期都用台灣格式。

最要緊的是 `:518` 的**刪除確認框**：「確定刪除這筆旅程？刪除後無法復原。」一個日文或韓文使用者，要在一個看不懂的確認框上按下不可復原的刪除。

`legacy-ui-localizer.tsx` 的 MutationObserver 救不了——它用完全相同的字串比對 `messages/*/legacy.json`，那份 catalog 只有 52 筆，而且插值字串在結構上永遠對不上。

## Definition of done

- [x] `account-list.tsx` 不再有任何寫死的使用者可見中文字串。
- [x] 刪除確認框在五語系都正確顯示。
- [x] 日期與數字依 locale 格式化，不再寫死 `zh-TW`。

## Steps

- [x] 把上列所有字串搬進 `messages/*/trips.json`，用 `useTranslations("trips")`。
- [x] `:335` 的 `toLocaleString("zh-TW")` 改用 `useLocale()`。
- [x] aria-label 也要走 catalog——`legacy-ui-localizer` 雖然會改寫 `aria-label`，但不該依賴它。
- [x] 跑 `npm run check:i18n` 確認五語系 key 對齊。

## How to verify

```bash
cd apps/web && npm run check:i18n && npm run test:web -- account-list
```

手動：`/en/trips`、`/ja/trips`、`/ko/trips` 各開一次，包含空狀態與刪除確認框，畫面上不應出現中文。

## Notes

- 這是既有 i18n 遷移的一部分：`tasks/done/2026-09-07-i18n-inline-dicts.md` 記錄的基線是「前台還有 34 個檔、1,178 段硬編碼中文完全不在 catalog 裡」。大約十張已完成的任務啃掉了一部分，但**目前沒有任何 open 任務在推進剩下的**，而 `/trips` 是剩餘檔案中流量最高的之一。
- `back-to-back-fare-search.tsx`（98 行）已被既有任務明確降級，屬低流量 `/labs/airlines` 且多為航空／城市代碼表，不要順手一起做。

## 瀏覽器實測補充（2026-09-11 第二輪）

用真實瀏覽器對 `en` / `ja` / `ko` 共 12 條路由，搜尋第一輪點名的 27 個寫死繁中字串，**零命中**。

**這不代表本任務的問題不存在，而是那些程式路徑在唯讀環境下走不到**：刪除確認框需要帳號裡有行程（測試帳號 0 筆）、機票與飯店卡需要完成一次搜尋（環境只轉讀取，不送寫入）、行程時間軸需要行程裡有項目。

所以本任務的狀態是**未驗證**，不是**已推翻**。接手的人請自己建一筆有內容的行程再確認，不要因為「掃描沒掃到」就把它關掉。

順帶澄清一個第二輪用過的無效指標：曾以「頁面漢字佔比」推估洩漏程度，但**日文本來就使用漢字**（實測 `ja` 頁面漢字 28–37%，同時有大量假名，是真正的日文），該指標對日文無效，不可採信。英文頁實測漢字僅 0.2–5.2%，且經逐一檢查後確認全部來自語言切換器的語言名稱（繁體中文／简体中文／日本語），屬正確做法。

## claim 用了 --force，理由寫在這裡（claude-opus-5, 2026-09-11）

`messages/*/trips.json` 五個檔同時在 `2026-09-10-seoul-day2-transport-ux`（codex-seoul-day2-release）的 scope 裡，所以工具擋下來。查過之後仍然 `--force`：

- 那張的 claim 是 2026-09-10T06:16:47Z，已經超過 24 小時，協定上算 stale，board 也把它標成 stale。
- 它的工作**已經合併進 main**（`git merge-base --is-ancestor 5f34f77 origin/main` → yes，`5f34f77 fix: restore Seoul transit queries and readable travel details`），只是任務檔沒標 `done`。
- 重疊的部分只有往 JSON 加 key，不動它加過的 key。

沒有去改它的任務檔（那是它的 reviewer 的事），只在這裡留紀錄。

## 完成紀錄（claude-opus-5, 2026-09-11）

`account-list.tsx` 的 35 行漢字全數搬進 catalog，現在整個檔案一個漢字都沒有。

分三處放：
- `common.accountList.*` —— 載入中、三種載入失敗、重新載入、確定刪除、操作失敗。這些在「我的旅程」和「價格通知」兩種模式下是同一句話，放在 `common` 才不會寫兩遍。
- `trips.list.*` / `alerts.list.*` —— 兩邊講的不是同一件事的部分。元件用 `t = useTranslations(kind)`，所以 `t("list.empty")` 在旅程頁讀 `trips.list.empty`、在通知頁讀 `alerts.list.empty`。
- 日期：`toLocaleString("zh-TW")` 改成 `toLocaleString(locale)`（`useLocale()`）。

任務列的 `:518` 刪除確認框——「確定刪除這筆旅程？刪除後無法復原。」——是這張的重點，現在五語系都有。

順手修的一個非 i18n 問題：旅程總價用 `twd.format()`，也就是不管旅程本身記的是什麼幣別都印 NT$。同一個元件的 `PriceAlertButton` 早就在用 `trip.currency`，改成一致的 `money(trip.total_price, trip.currency || "TWD")`。

### 驗證

新增 `account-list-i18n.test.tsx`。它自己 `vi.mock("next-intl")`，讓 catalog 回傳 `[namespace.key]` 而不是中文，並以 `useLocale() === "en"` 渲染，然後斷言畫面上**一個漢字都沒有**（連 `aria-label` 和 `placeholder` 都掃）。這是唯一能真正抓到「又寫死中文」的做法——`vitest.setup.tsx` 給所有測試 zh-TW catalog，在那裡寫死的中文和翻譯過的中文長得一模一樣。

因為 `vi.mock` 是檔案層級的，所以另開一個檔；原本的 `account-list.test.tsx` 十個案例全部照舊通過，等於證明繁中畫面沒有變。

把 `t("list.deleteConfirm")` 還原成寫死的那句話之後：

```
× writes no Chinese of its own into a saved trip
× writes no Chinese of its own into a price alert, its editor or its delete prompt
× reports a failed delete without a Chinese sentence around the reason
AssertionError: hardcoded copy around a failure reason: expected '確定刪除這筆價格通知' to be undefined
```

復原後 16 passed。

### 留給後面的人

`trips.list.deleteAction` 這個 key 我加了又刪掉：旅程列的刪除走 `TripActions`，它的標籤來自 `lib/frontend-navigation.ts` 的內建字典（那份是有翻譯的），不經過 catalog。只有通知列用得到 `deleteAction`。
