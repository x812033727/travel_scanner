---
id: 2026-09-07-ui-text-loader
title: 後台可改前台文案：前台載入器把資料庫覆寫疊上 next-intl
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T01:40:18Z
created_at: 2026-09-07T00:33:46Z
completed_at: 2026-09-07T02:06:23Z
branch: claude/ui-text-loader
depends_on:
  - 2026-09-07-ui-text-overrides-api
scope:
  - apps/web/i18n/request.ts
  - apps/web/lib/ui-text.ts
  - apps/web/lib/ui-text.test.ts
  - apps/web/lib/ui-text.server.ts
  - apps/web/lib/ui-text.server.test.ts
  - tools/check-i18n.mjs
  - tools/e2e-runtime-api.mjs
---

# 後台可改前台文案：前台載入器把資料庫覆寫疊上 next-intl

## Why

前一張任務（`2026-09-07-ui-text-overrides-api`）已經把資料表與 API 上線了，但前台還沒
接，所以後台就算存了覆寫也不會顯示。這張把兩層接起來：`apps/web/messages` 的 JSON 仍是
版本控管的預設值，資料庫只回覆寫，在 `i18n/request.ts` 回傳前疊上去。

合併點選在 `request.ts` 是因為伺服器端（`getTranslations`、21 個 `generateMetadata`）與
客戶端（唯一的 `NextIntlClientProvider`）都從那一份設定取訊息，**所以任何元件都不用改**。

## Definition of done

- [x] `i18n/request.ts` 在回傳前疊上覆寫，元件零改動
- [x] 合併是 copy-on-write，不動 `import()` 回來的 JSON 模組
- [x] 覆寫永遠不新建 key；鎖定／未知 namespace、孤兒 key、非葉節點、參數不符都跳過並記錄理由
- [x] API 掛掉、逾時、回傳格式錯 → fail-open，前台照常顯示 JSON 預設
- [x] `tools/check-i18n.mjs` 守住 API 與前台兩份 namespace 允許清單跟 catalog 目錄一致
- [x] `tools/e2e-runtime-api.mjs` 有 `/runtime/ui-text` 的空 stub

## Steps

- [x] `lib/ui-text.ts`：純函式（允許清單、`messageParameters`、`bracesBalanced`、
      `hasAdvancedIcu`、`overrideProblem`、`flattenMessages`、`isUiTextPayload`、`chunk`、
      `applyUiTextOverrides`）——編輯器（任務 C）直接 import 這一份
- [x] `lib/ui-text.server.ts`：鏡射 `site-visibility.server.ts`，`cache()` 包住
- [x] `i18n/request.ts` 合併點
- [x] `tools/check-i18n.mjs` 允許清單守衛；`tools/e2e-runtime-api.mjs` stub
- [x] 兩個測試檔（21 個案例）

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run test:tools && npm run check:tasks
cd apps/web && npx vitest run lib/ui-text.test.ts lib/ui-text.server.test.ts
```

部署後手動驗一次整條鏈（這是第一次看得到效果）：

```bash
# 以管理員身分覆寫一句，再看前台
curl -X PUT "$SITE/api/travel/admin/ui-text/zh-TW/navigation/home" \
  -H 'Content-Type: application/json' -b "travel_access=$TOKEN" \
  -d '{"value":"回首頁","default_value":"首頁"}'
curl -s "$SITE/api/travel/runtime/ui-text?locale=zh-TW"   # 看得到 navigation.home
# 重新載入 /zh-TW，導覽列應該變成「回首頁」；/en 不受影響
curl -X DELETE "$SITE/api/travel/admin/ui-text/zh-TW/navigation/home" -b "travel_access=$TOKEN"
# 再載入一次應該變回「首頁」——不用重啟（這證明 copy-on-write 是對的）
```

## Notes

- **copy-on-write 不是可選的。** `request.ts` 的 `import()` 回傳的是 Node 模組快取裡的
  同一個物件，跨請求共用。原地寫入會把 bundle 裡的預設值永久蓋掉到重啟為止，「還原預設」
  就會失效，而且下一次的參數比對會拿已被覆寫的值當預設。測試用 `toBe` 斷言輸入物件與沒
  動到的 namespace 保持同一引用。
- **沒有覆寫時零成本**：`applyUiTextOverrides(messages, {})` 直接回原物件，不複製。
- **`cache()` 是每請求記憶，不是跨請求快取。** next-intl 依 `(config, locale)` 快取 request
  config，但 `generateMetadata` 帶明確 locale 呼叫、layout 不帶，同一請求可能建兩次設定；
  包了 `cache()` 就只打一次 API。刻意不做 TTL 快取：API 端每次寫入就清自己的 Redis，所以
  存檔後下一次渲染就生效，也沒有多實例不一致要推理。
- **`check-i18n.mjs` 的新守衛**用正規表示式從 `apps/api/app/ui_text/schemas.py` 與
  `apps/web/lib/ui-text.ts` 各挖出允許清單，跟 `messages/en` 目錄減 `legacy` 比對。**已實測
  它會失敗**（暫時拿掉 `usage` → 正確報 `missing: usage`），不是永遠會過的裝飾。
- **`overrideProblem` 的兩態順序**：先驗大括號再驗參數。`en` 有 7 個 ICU plural，少一個 `}`
  仍然抓得到 `count` 這個參數名，所以只有大括號檢查擋得住，否則 next-intl 會在頁面上印出
  key 路徑。
- **踩到的型別坑**：`let key = namespace` 會被推斷成 `EditableNamespace` 聯合字面型別
  （因為 `isEditableNamespace` 收窄過），後面塞路徑片段就編譯失敗；要寫 `let key: string`。
- 任務 C（編輯器）只需 `import` 這份 `lib/ui-text.ts`，不要另外複製一份參數 regex。
