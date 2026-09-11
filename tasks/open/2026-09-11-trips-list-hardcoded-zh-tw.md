---
id: 2026-09-11-trips-list-hardcoded-zh-tw
title: 我的旅程整頁硬編碼繁中含刪除確認框
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:20:35Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/account-list.tsx
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

- [ ] `account-list.tsx` 不再有任何寫死的使用者可見中文字串。
- [ ] 刪除確認框在五語系都正確顯示。
- [ ] 日期與數字依 locale 格式化，不再寫死 `zh-TW`。

## Steps

- [ ] 把上列所有字串搬進 `messages/*/trips.json`，用 `useTranslations("trips")`。
- [ ] `:335` 的 `toLocaleString("zh-TW")` 改用 `useLocale()`。
- [ ] aria-label 也要走 catalog——`legacy-ui-localizer` 雖然會改寫 `aria-label`，但不該依賴它。
- [ ] 跑 `npm run check:i18n` 確認五語系 key 對齊。

## How to verify

```bash
cd apps/web && npm run check:i18n && npm run test:web -- account-list
```

手動：`/en/trips`、`/ja/trips`、`/ko/trips` 各開一次，包含空狀態與刪除確認框，畫面上不應出現中文。

## Notes

- 這是既有 i18n 遷移的一部分：`tasks/done/2026-09-07-i18n-inline-dicts.md` 記錄的基線是「前台還有 34 個檔、1,178 段硬編碼中文完全不在 catalog 裡」。大約十張已完成的任務啃掉了一部分，但**目前沒有任何 open 任務在推進剩下的**，而 `/trips` 是剩餘檔案中流量最高的之一。
- `back-to-back-fare-search.tsx`（98 行）已被既有任務明確降級，屬低流量 `/labs/airlines` 且多為航空／城市代碼表，不要順手一起做。
