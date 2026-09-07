---
id: 2026-09-07-ui-text-admin-editor
title: 後台可改前台文案：/admin/ui-text 編輯器
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T02:20:45Z
created_at: 2026-09-07T00:34:05Z
completed_at: 2026-09-07T06:40:32Z
branch: claude/ui-text-admin-editor
depends_on:
  - 2026-09-07-ui-text-overrides-api
  - 2026-09-07-ui-text-loader
scope:
  - apps/web/app/[locale]/admin/ui-text
  - apps/web/components/admin-ui-text-panel.tsx
  - apps/web/components/admin-ui-text-panel.test.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/components/admin-nav.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
---

# 後台可改前台文案：/admin/ui-text 編輯器

## Why

前兩張任務把 API（`2026-09-07-ui-text-overrides-api`）與前台載入器
（`2026-09-07-ui-text-loader`）都上線了，整條鏈已經能動，但只能用 `curl` 操作。這張補上
營運者真正會用的介面：瀏覽某個語系某個文案群組的所有鍵、看到預設值與參考語系、寫覆寫、
一鍵還原、批次儲存。

## Definition of done

- [x] `/admin/ui-text` 頁面，導覽列有「前台文案」入口
- [x] 一列一個鍵：鍵名、預設值（同時是 textarea 的 placeholder）、參考語系、參數 chips、
      徽章（已覆寫／未儲存／儲存後還原預設／孤兒覆寫／含複數規則）、更新者與時間
- [x] 客戶端即時驗證參數與大括號，有錯就擋住儲存並指出缺哪個參數
- [x] 批次儲存（≤100 筆一批，超過自動分批）；清空欄位＝還原預設，送 `value: null`
- [x] 孤兒覆寫（catalog 已無此鍵）唯讀顯示並可還原，這是唯一能清掉它們的地方
- [x] 篩選（全部／已覆寫／未儲存／有參數／孤兒）、搜尋、50 列分頁
- [x] 載入失敗分類：401/403 給 `ADMIN_EMAILS` 提示且不給重試；連不上給重試
- [x] 有未儲存變更時切換群組／語系會先確認
- [x] 五個語系的 `admin.json` 都有完整的 `uiText` 群組與 `navigation.uiText`

## Steps

- [x] 五份 `admin.json` 加 `navigation.uiText` 與 `uiText` 群組（16 個子群、含 21 個
      namespace 的中文說明）
- [x] `components/admin-ui-text-panel.tsx`
- [x] `app/[locale]/admin/ui-text/page.tsx`
- [x] `components/admin-nav.tsx` 加項目（`layout` 與 `system` 之間）＋ `legacyCurrentHref`
- [x] 三個測試檔（面板 12、頁面 5、導覽 3）

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
cd apps/web && npx vitest run components/admin-ui-text-panel.test.tsx \
  "app/[locale]/admin/ui-text/page.test.tsx" components/admin-nav.test.tsx
```

部署後：`/zh-TW/admin/ui-text` →「導覽與頁尾」群組 → 改 `home` → 儲存 → 重新載入前台首頁
看到新文字 → 回編輯器按「還原預設」→ 儲存 → 前台變回原文（不用重啟）。

## Notes

- **預設值從哪來**：API 沒有 catalog，所以頁面（server component）自己
  `import(\`../../../../messages/${locale}/${namespace}.json\`)`，用 `flattenMessages` 攤平後
  傳給面板。跟 `i18n/request.ts` 同一種「固定目錄上的樣板字串」模式，而且 `ns` 與 `locale`
  都先過允許清單，沒有路徑穿越。只載入正在編輯的那一份，不是全部 165 KB。
- **`key` prop 是必要的**：`router.push` 到同一路由只會換 props，沒有
  `key={namespace/locale/ref}` 的話 React 會保留上一個群組的草稿。
- **query 參數靜默回退不 redirect**：`ns=legacy`、`locale=xx`、`ns=../../etc/passwd` 都回到
  `common/zh-TW/en`，選單顯示的就是實際生效的值，過期書籤也不會在兩個網址之間彈跳。
- **參考語系永遠不等於編輯語系**：編 zh-TW 時預設參考 en，其餘預設參考 zh-TW。
- **不重用 `LocalizedNameFields`**：那是「一個實體 × 五語系」，這裡是「一個語系 × 幾百個
  鍵」；只借用它「placeholder = 預設值」的作法。
- **只用 `GET` 與 `POST /batch`**，`PUT`/`DELETE` 留給腳本：一條寫入路徑、一種回應、一個
  錯誤分支，而且單列還原＝「清空再儲存」，存檔前都可以反悔。
- **儲存失敗後會重新 GET** 並修剪掉已等於伺服器值的草稿，未存的文字留在表單裡，所以中途
  失敗不會讓畫面說謊。
- **測試踩到的兩個坑**：(1) 徽章文字與篩選膠囊同名（「已覆寫」「孤兒覆寫」），
  `getAllByText` 會多抓到膠囊，要加 `{ selector: "span" }`；(2) 同一個測試裡多次 `render()`
  時 Testing Library 不會自動清 DOM（只在測試之間清），helper 裡要先 `cleanup()`。
- **型別坑**：測試 helper 的預設參數 `= [{ namespace: "common" as const }]` 會把型別窄化成
  `"common"`，傳別的 namespace 就編譯失敗；要明寫 `EditableNamespace`。
- `Languages` 這顆 lucide icon 存在（1.37.0）；我一開始用 `ls .../icons/languages.js` 檢查
  誤判成缺，dist 其實是 `.mjs`，用 `node -e "require('lucide-react').Languages"` 才準。
