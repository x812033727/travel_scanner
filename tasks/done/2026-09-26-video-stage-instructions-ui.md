---
id: 2026-09-26-video-stage-instructions-ui
title: Video stage instructions: the settings tab edits the standing instructions and shows the prompts read-only
status: done
priority: P1
area: web
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T15:27:40Z
created_at: 2026-09-26T15:27:17Z
completed_at: 2026-09-26T15:41:06Z
branch: claude/video-stage-instructions
depends_on:
  - 2026-09-26-video-stage-instructions-api
scope:
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video stage instructions: the settings tab edits the standing instructions and shows the prompts read-only

## Why

同 `2026-09-26-video-stage-instructions-api`：站主要在 `/admin/videos` 的「設定」分頁寫每個階段的常設指示，並看到工人實際送出的完整提示詞。

## Definition of done

- [x] 「各階段的常設指示」區：六個階段各一個多行欄位（≤ 4000 字），隨「儲存設定」一起送 `stage_instructions`；沒有管理設定權限的人只能看。
- [x] 「目前的提示詞（唯讀）」區：讀 `GET /admin/video-automation/prompts`，每個階段、每種格式一個可展開的區塊，標題帶 slug 與時間，內文是完整指示；沒紀錄時說明第一次跑過才會出現；舊站回 404 時區塊留空不擋頁面。
- [x] 五語文案；vitest、lint、typecheck、check:i18n 綠。

## Steps

- [x] admin-video-settings.tsx：型別、`SETTINGS_KEYS`、兩個新區塊。
- [x] 測試：既有欄位顯示、改寫後 body 帶 `stage_instructions`、提示詞區顯示。

## How to verify

```bash
cd apps/web && npx vitest run components/admin-video-settings && npm run lint && npm run typecheck && cd ../.. && git add -A && CI=1 npm run check:i18n
```

## Notes

2026-09-26（claude-fable-5-1-video-drama）：分支 `claude/video-stage-instructions`。欄位標籤用 `stages.<stage>` 的全名（例如「企劃（選題與大綱）的常設指示」），測試也要用全名找。
