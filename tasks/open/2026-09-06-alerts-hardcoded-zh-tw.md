---
id: 2026-09-06-alerts-hardcoded-zh-tw
title: 價格通知頁的副標與 LINE 卡片在四個語系都是繁中
status: in-progress
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T17:56:37Z
created_at: 2026-09-06T17:32:56Z
completed_at:
branch: claude/ux-batch-3
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

## Notes

2026-09-07：頁面標題、副標與整張 LINE 卡（14 句，含錯誤與狀態訊息）都搬進
`messages/*/alerts.json` 的 `title`／`subtitle`／`line.*`。原本只有 h1 會被
`LegacyUiLocalizer` 在瀏覽器端換掉——那支元件是用 `legacy.json` 做 DOM 級替換的
權宜之計，只收了 54 句，所以同一張卡有的翻有的沒翻。新字串一律走正規 catalog。
