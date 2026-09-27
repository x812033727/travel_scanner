# 後台頁、權限與設定

總則在 `docs/admin-operations-center.md`：導覽由 `GET /api/v1/admin/bootstrap` 回傳，前端不從角色名推權限，每個後台 API 自己再檢查一次。

## 為什麼只加前端 fallback 會是 forbidden

`apps/web/lib/admin-operations.ts` 的 `visibleAdminNavigation` 只要 API 回了導覽就**只用 API 的**，不看 `fallbackAdminNavigation`；`apps/web/app/[locale]/admin/layout.tsx` 再用 `canAccessAdminPath` 比對 href。所以 API 的 `NAVIGATION_REGISTRY` 沒有那一列，正式站打開就是「你沒有這個後台的權限」，本機（API 沒回導覽、走 fallback）卻看得到。曾經有一整個後台頁因此在正式站空了好幾天。

## 新後台頁的登記點

| # | 哪裡 | 改什麼 | 誰會抓到漏改 |
| --- | --- | --- | --- |
| 1 | `apps/api/app/admin/operations_service.py` 的 `NAVIGATION_REGISTRY` | `AdminNavigationItem(id, group, href, label_key, capability, badge_key?)`；group 只能是 overview／content／community／operations／system | `apps/api/tests/test_admin_operations.py`（加一條斷言） |
| 2 | `apps/web/lib/admin-operations.ts` 的 `fallbackAdminNavigation` | 同一列（key 用 camelCase）；API id 是 snake_case 時在 `navigation()` 的 `aliases` 加對照 | 無自動比對；只在 API 沒回導覽時用得到 |
| 3 | `apps/web/e2e/admin-operations-full-stack.spec.ts` | `OWNER_NAVIGATION` 與 `ROLE_NAVIGATION` 裡有該能力的角色，順序照 registry | full-stack e2e（`ADMIN_OPERATIONS_E2E=1`） |
| 4 | `tools/e2e-runtime-api.mjs` 的 `adminNavigation` ＋ `apps/web/e2e/admin-operations.spec.ts` 的 `ADMIN_PAGES`／`ROLE_NAVIGATION` | 兩邊一起加或一起不加（隔離 fixture 目前沒有 news 與 videos，兩邊一致） | `admin-operations.spec.ts` 用 `toEqual` 比對 |

另外要做：

- 頁面：`apps/web/app/[locale]/admin/<slug>/page.tsx`（薄殼，內容元件放在 `apps/web/components/` 下以 `admin-` 開頭的檔案）。
- 側欄圖示：`apps/web/components/admin-nav.tsx` 的圖示對照。
- 標籤：五語 `apps/web/messages/<locale>/admin.json` 的 `navigation.<key>`。`apps/web/lib/admin-operations-copy.ts` 的 `copy.nav` 是硬編碼五語的舊表，缺鍵時側欄退回 `admin.navigation`；新頁只加 messages，不要在 TS 裡加中文（`check:i18n` 會擋）。
- 有 badge：在同檔 `_live_pending_counts` 算數、需要時加進 `pending_total`，並把 `pending_counts` 的快取鍵版本號加一（`admin:operations:pending:vN`），否則舊快取讓 badge 不出現。
- 頁內分頁、區段與篩選一律放 URL：`apps/web/lib/admin-workspace-navigation.ts` 的 `useAdminWorkspaceNavigation(config)`（tabs、defaultTab、legacy 舊書籤對照）、`useAdminQueryValue`、`useAdminQueryState`、`adminNavigate`（一次寫多個鍵）。這個檔案不是側欄導覽的登記處。

## API 權限

- 每個 router 用 `require_capability("<cap>")`（`apps/api/app/auth/service.py`）宣告要的能力，讀寫分開（`*.read`／`*.manage`）。
- 用泛用的 `AdminUser` 依賴的路由，能力由同檔 `_admin_path_capability` 依路徑推；**沒列到的 `/admin/...` 路徑落到 `roles.manage`（只有 owner）**。新路徑要嘛明確用 `require_capability`，要嘛加進這個對照，並在 `apps/api/tests/test_admin_rbac.py` 的 `test_existing_admin_paths_resolve_to_least_privilege_capability` 參數表加一列。
- 新能力或角色改動：`ADMIN_ROLE_CAPABILITIES` 與 `docs/admin-operations-center.md` 的 `admin-role-capabilities` 表是機器比對的（`test_documented_role_capability_matrix_matches_runtime`），兩邊一起改；`tools/e2e-runtime-api.mjs` 的 `adminCapabilities` 也要跟上。
- 只給 owner 的操作（例如 AI 帳號）用 `roles.manage`。

## 破壞性操作：step-up

- `POST /api/v1/admin/step-up` 驗目前密碼，發五分鐘、綁操作 scope、綁使用者與 `auth_version` 的 HttpOnly cookie。路由裡呼叫 `await require_admin_step_up(request, user, "<scope>")`。
- 新 scope 要改三處：`apps/api/app/admin/user_schemas.py` 的 `StepUpScope`、`apps/api/app/auth/service.py` 的 `STEP_UP_SCOPE_CAPABILITY`（scope 對應的能力），以及前端呼叫 step-up 的面板（參考 `apps/web/components/admin-users-panel.tsx`、`apps/web/components/admin-database-panel.tsx`）。
- 帳號層的破壞性操作還要：`Idempotency-Key` 標頭、原因、打字確認；拒絕移除最後一個 owner。細節在 `docs/admin-operations-center.md`。
- 內容層的「隱藏」類操作不走 step-up，而是原因＋確認＋版本鎖（例如文章 `POST /hide|/unhide|/batch`）；不要再開第二條寫入路徑去改同一個狀態欄位。

## 設定欄位的歸屬

- 每個設定只有一個可編輯的擁有者。正本是 `apps/web/lib/admin-settings-ownership.ts`（`settingsOwner`、`domainConfig`、`settingsHref`），說明在 `docs/admin-domains.md`「One editable owner per setting」。
- 金鑰（secret）一律歸共用供應商頁；不認得的欄位留在共用擁有者。非擁有者的頁面只顯示連結，不能有第二個可編輯表單。
- AI 類的供應商（`AI_SETTINGS_PROVIDERS`：ai_vendors、ai_planner、ai_guide_search、hotspot_intros、azure_speech、gemini_guides）在 `/admin/ai-accounts`，不在 `/admin/settings`。
- 儲存只送改過的欄位加 `expected_updated_at`；過期的寫入拿 409、保留草稿。
- 領域 API 的隔離規則（hotels 只動 hotel 子集、catalog AI 的 `scope`）在 `docs/admin-domains.md`「API isolation」。

## 新增一個供應商

1. API：`apps/api/app/admin/service.py` 的 `PROVIDER_DEFINITIONS` 加定義；它必須屬於同檔 `CONNECTION_TESTED_PROVIDERS` 或 `LOCAL_ONLY_PROVIDERS` 其中之一（`apps/api/tests/test_admin_readiness.py` 檢查）。
2. 分類：`apps/web/components/admin-settings-panel.tsx` 的 `providerCategoryOf` 加 key → 類別（auth、ai、maps、content、travelData、affiliate）。沒登記的會掉進「其他」（`met_norway` 目前就是這樣）。新類別要加進 `providerCategories` 順序陣列與五語 `admin.json` 的 `providerTabs.categories.*`。
3. 欄位：同檔 `fieldMeta` 標型別（number／boolean）與 `localized`，五語 `admin.json` 的 `providerFields.<field>.label`。
4. 歸屬：若該欄位屬於某個領域工作區，登記在 `admin-settings-ownership.ts`。
5. 測試：`apps/web/components/admin-settings-panel.test.tsx` 選供應商前要先點類別分頁（用 regex 比對標籤，因為分頁上還有「已就緒／總數」計數）。
6. 若是搜尋資料的 adapter，另照 `README.md`「Adding a provider」：實作 `apps/api/app/providers/base.py` 的 protocol、正規化到 `providers/schemas.py`、向 orchestrator 註冊。

## 前端寫後台時踩過的坑

- `npm run check:i18n`（`tools/check-i18n.mjs`）擋 `apps/web/(app|components|lib)` 下非測試 `.ts/.tsx` **新增**的漢字，按「每個檔案每段漢字出現次數」算，所以複製一段已有的中文也會被擋。它只在 `CI` 有設、或有 staged 變更時才比對：沒 stage 的本機執行只印「Validated 5 locales」，什麼都沒檢查。commit 前先 `git add` 再跑，或 commit 後 `CI=1 npm run check:i18n`（比對 `HEAD^..HEAD`）。
- ESLint `react-hooks/set-state-in-effect` 擋 effect 裡同步 `setState`：URL 狀態用 `useSyncExternalStore`（`apps/web/lib/use-client-search.ts` 或上面的 admin 工作區 hook），抓資料寫成 `api(...).then(setState)`，「重設」改成以 key 記錄載入結果（`loaded.key === key ? loaded.data : undefined`）。
- 不要用 `json.load`／`json.dump` 改 messages 檔：有些檔案把巢狀物件寫在同一行，來回一次會重排整個檔案。當文字改那一行。
- vitest 一律在 `apps/web` 裡跑（`npm run test:web`）；在 repo 根目錄 `npx vitest run` 會用錯設定、幾乎全紅。
- `getAllByLabelText` 回傳的順序是 label 關聯優先、aria-label 其次，不是 DOM 順序；對話框內的查詢用 `within(screen.getByRole("dialog"))` 限縮。
- 後台以 URL 參數帶 id 的頁面（例如文章編輯器的 `?article=` 只收 UUID），vitest fixture 的 id 要用 UUID。

翻譯流程、e2e 的完整做法走 skill `web-i18n-e2e`；本機環境與 CI 讀法走 skill `dev-and-ci`。
