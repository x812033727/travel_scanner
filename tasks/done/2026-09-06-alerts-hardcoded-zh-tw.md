---
id: 2026-09-06-alerts-hardcoded-zh-tw
title: 價格通知頁的副標與 LINE 卡片在四個語系都是繁中
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T18:01:17Z
created_at: 2026-09-06T17:32:56Z
completed_at: 2026-09-06T18:18:57Z
branch: claude/alerts-i18n
depends_on: []
scope:
  - apps/web/components/line-connection-panel.tsx
  - apps/web/app/[locale]/alerts/page.tsx
  - apps/web/messages/en/alerts.json
  - apps/web/messages/ja/alerts.json
  - apps/web/messages/ko/alerts.json
  - apps/web/messages/zh-CN/alerts.json
  - apps/web/messages/zh-TW/alerts.json
---

# 價格通知頁的副標與 LINE 卡片在四個語系都是繁中

## Why

`/en/alerts`、`/ja/alerts`、`/ko/alerts`、`/zh-CN/alerts` 四個語系的 body 裡都有這三句
繁體中文，而且就在已經翻好的標題（Price alerts / 価格通知 / 가격 알림 / 价格提醒）底下：

- 「集中查看追蹤進度、調整目標價格與 LINE 通知狀態。」
- 「LINE 到價通知」
- 「加入官方帳號並連結網站帳號，達到價格條件時直接通知。」

半翻譯比全中文更難讀：讀者會以為自己按錯語言。

## Definition of done

- [x] `/alerts` 在五個語系底下沒有任何一句寫死的繁中。
- [x] `check:i18n` 通過，且 CI 的 Han guard 不會擋（新字串放 `messages/*/alerts.json`）。

## Result（2026-09-07 完成）

任務點名三句，實際上整個 `line-connection-panel.tsx` 都是寫死的繁中——十三句，包含按鈕、
狀態訊息與一個 `aria-label`。全部搬進 `messages/*/alerts.json` 的 `alerts` 與 `alerts.line`，
頁面標題與副標改用 `getTranslations`。

**有一個詞刻意不翻：LINE 的綁定關鍵字。** `apps/api/app/line/router.py` 判斷綁定意圖的條件是
完全比對三個繁體中文詞，所以把日文或韓文文案裡的關鍵字翻掉，等於叫讀者傳一句 bot 不會回應的話，
而且失敗是無聲的。做法是把關鍵字定成元件裡的常數，用 `{keyword}` 參數傳進訊息，五個語系的
`keywordHint` 與 `blocked` 都只寫參數不寫那兩個字，並加測試逐語系釘住——免得將來有人好心把它翻掉。

**後端才是真正該修的地方**，但那不屬於這張任務的 scope，另開
[[2026-09-06-line-link-keyword-chinese-only]]：關鍵字要收各語系的等價詞，而且收到不認得的
訊息時要回話而不是靜默。

`check:i18n` 的 Han guard 擋過一次，擋的是我寫在註解裡的中文詞（`連結帳號`、`綁定帳號`）。
它掃的是原始碼文字，註解也算，所以註解改成引用檔名而不是列出那些詞。這是合理的行為，不是誤判。

JSON 用純文字插入而不是重寫——`alerts.json` 第一行原本是壓在一起的長行，重新排版會讓 diff
變成整檔改寫。每個語系檔只有一行被動到。

檢查：`lint:web`、`check:i18n`（含 staged Han guard）、`typecheck:web`、
`vitest run line-connection`（7 passed）全綠。
