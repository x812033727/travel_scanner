---
id: 2026-09-06-search-results-i18n
title: 搜尋結果頁整頁文案寫死繁中
status: done
priority: P1
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T03:32:52Z
created_at: 2026-09-06T00:53:02Z
completed_at: 2026-09-06T04:03:30Z
branch: claude/web-i18n-p1
depends_on: []
scope:
  - apps/web/components/search-experience.tsx
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
---

# 搜尋結果頁整頁文案寫死繁中

## Why

`/search` 是首頁精靈送出後的落地頁，也是查價流程的核心。整頁約 77 句可見文字寫死在
`search-experience.tsx`，五個語系看到的都是同一種畫面。

2026-09-05 的全站健檢已經把首頁精靈（`search-workbench.tsx`）翻完，所以現在的體驗是：
訪客用英文填完五步精靈，按下送出，落到一個全繁中的結果頁。這個落差比整頁都是繁中更難堪。

## Definition of done

- [x] 以 `/en/search?...` 跑完一次搜尋，從載入中、進度、結果卡到錯誤狀態都沒有繁體中文。
- [x] 新增字串在 `messages/*/search.json`（首頁精靈已建立 `workbench` 物件，
      這個頁面建議放在同層的另一個物件，例如 `results`，不要混在一起）。
- [x] `CI=1 npm run check:i18n`、`lint:web`、`typecheck:web` 通過。

## Steps

- [x] 列出待翻字串（方法見 `2026-09-06-trip-editor-i18n` 的 Notes）。
- [x] 先翻使用者一定會遇到的路徑：進度四模組、結果卡、`search.failed` 的錯誤句、
      「重新載入結果」、空結果。
- [x] 再翻少見路徑：SSE 中斷警告、解析失敗救援區塊、次數不足導向。
- [x] 帶數字的句子改 ICU。

## How to verify

```bash
cd apps/web && npx vitest run components/search-experience
cd ../.. && npm run lint:web && npm run typecheck:web && CI=1 node tools/check-i18n.mjs
```

## Notes

**2026-09-06 完成。** 102 個字面（含模板字串與 JSX 文字）搬進 `messages/*/search.json` 的 `results` 物件
（與 `workbench` 同層，五語系 121 鍵），元件用 `useTranslations("search.results")`。模組層級的
`stages`／`sourceLabels` 改成 key stem 在渲染處翻（`stages.${key}`、`source.${mode}`）；
`flightTimeSummary`／`titleFor`／`detailsFor`／`recheckUrl` 多一個 `t: Translate` 參數，不搬進元件。
帶數字的句子全部 ICU 簡單參數（`{count}`、`{minutes}`…，不用 plural——vitest 的 mock 只做 replaceAll）。
國家名放在 `results.country.*`（七國都有），`destination-catalog-labels-i18n` 可以直接沿用。
刻意留下的繁中：`parseInterests` 的中文→代碼對照與 `rawInterests.includes("紅眼")`，那是解析查詢參數的輸入，不是顯示文字。
測試：`search-experience.test.tsx` 用 zh-TW 查字串，值沒變所以不必改；lint／tsc／`CI=1 check:i18n` 過。

**這個檔案 2026-09-06 剛改過兩處**，接手前先看那兩段的註解，不要把它們改壞：

1. `stream.onerror` 現在會判斷 `stream.readyState === EventSource.CLOSED`：連線關掉就
   `setBusy(false)` 並 `loadFinal()`。在這之前，切到別的 App 再回來會永遠停在轉圈。
2. 救援區塊的條件從 `{!parsed && !text && …}` 改成 `{!parsed && (!text || error) && …}`，
   讓 `/ai/parse-trip` 失敗時也有「回首頁設定條件」可按。

**注意**：`messages/*/search.json` 目前有 `workbench` 物件（77 鍵，2026-09-06 加的）。
`check:i18n` 會比對五語系的鍵集合與 ICU 參數，插入新鍵時用純文字插入，
不要 JSON round-trip（會重排整份檔案）。
