---
id: 2026-09-06-admin-panels-i18n
title: 後台面板文案硬編碼繁中
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T00:53:41Z
completed_at:
branch:
depends_on:
  - 2026-09-06-stale-gemini-model-help
scope:
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 後台面板文案硬編碼繁中

## Why

後台面板加起來有數百句寫死的繁中：`admin-settings-panel.tsx` 257 句、
`admin-hotspot-places-panel.tsx` 55、`admin-hotspots-panel.tsx` 54、
`admin-food-merchants-panel.tsx` 52、`admin-deployments-panel.tsx` 51、
`admin-users-panel.tsx` 47。切到 `/en/admin` 是中英夾雜。

**優先度刻意壓到 P3**：後台目前是站長一個人在用，繁中對他不是問題。列出來是為了讓
「站台支援五語言」這句話有一天能成立，不是因為現在很痛。

scope 只寫了最大的三個面板 —— 一次做完六個檔案太大，而且會擋住其他人所有 admin 任務。
做完這三個之後，剩下的用同樣手法另開一張。

## Definition of done

- [ ] scope 內三個面板在 `/en/admin` 沒有繁體中文（資料本身除外）。
- [ ] 新字串進 `messages/*/admin.json`，五語系鍵一致。
- [ ] 三個面板各自的 `.test.tsx` 通過（它們大量用中文 accessible name 查詢）。
- [ ] `CI=1 npm run check:i18n`、`lint:web`、`typecheck:web`。

## Steps

- [ ] 一個檔案一個 commit，不要一次三個。
- [ ] `admin.json` 已經有 `navigation`／`providerTabs`／`hotspotTabs`／`usage`／
      `analytics`／`layout` 幾個物件，新字串照面板分組加，別全塞在頂層。
- [ ] 同步改測試裡的中文查詢字串。

## How to verify

```bash
cd apps/web && npx vitest run components/admin-settings-panel components/admin-hotspots-panel components/admin-food-merchants-panel
cd ../.. && npm run lint:web && npm run typecheck:web && CI=1 node tools/check-i18n.mjs
```

## Notes

**2026-09-06 這幾個檔案剛被改過**，接手前先讀那些註解：

- `admin-food-merchants-panel.tsx`：加了分頁（`PAGE_SIZE = 50`，用 API 既有的 `page` 參數；
  之前寫死 `limit=100` 完全沒有分頁），以及 `saveError` —— 儲存失敗的訊息現在顯示在
  **編輯視窗內**，因為頁面層的 banner 在 `z-[90]` 遮罩後面看不到。
  分頁的 `pageState` 綁著 `filterSignature`，換篩選會自動回第 1 頁；
  這個寫法是為了避開 `react-hooks/set-state-in-effect` 這條 lint 規則，不要改回 effect 裡 setState。
- `admin-hotspots-panel.tsx`：深度分數四個欄位的標籤從變數名改成
  `hotspotAdmin.depthScores.*`（在 `messages/*/hotspotAdmin.json`，不是 `admin.json`）。
- 所有 `admin-*.tsx` 都在 2026-09-06 補過 optional chaining（`data?.items?.map`），
  避免部分 payload 讓整頁白畫面。翻譯時不要把那些 `?.` 拿掉。

**JSON 編輯注意**：`messages/*/admin.json` 不要 JSON round-trip 回寫（會重排整份檔案、
默默吃掉重複鍵）。用純文字插入。

**Scope 重疊**：`admin-settings-panel.tsx` 也在 `2026-09-06-stale-gemini-model-help` 的 scope 裡（那張只改一段說明文字）。先讓它落地，這張再把那段文字一起搬進 catalog，免得兩邊改同一行。
