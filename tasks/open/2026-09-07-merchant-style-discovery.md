---
id: 2026-09-07-merchant-style-discovery
title: 網美與文青店家風格篩選、審核及首批來源資料
status: review
priority: P1
area: api
owner: codex
claimed_at: 2026-09-08T00:29:59Z
created_at: 2026-09-07T23:14:18Z
completed_at:
branch: codex/merchant-style-batch-02
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/app/i18n.py
  - apps/api/app/foods
  - apps/api/app/cli.py
  - apps/api/migrations/versions/0061_merchant_styles.py
  - apps/api/tests/test_merchant_styles.py
  - apps/api/tests/test_trend_import.py
  - apps/api/tests/test_schema.py
  - apps/web/components/food-browser.tsx
  - apps/web/components/food-browser.test.tsx
  - apps/web/components/food-merchant-card.tsx
  - apps/web/components/food-merchant-card.test.tsx
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/components/admin-merchant-styles.tsx
  - apps/web/components/admin-merchant-styles.test.tsx
  - apps/web/lib/foods.ts
  - apps/web/lib/foods.test.ts
  - apps/web/messages
  - docs/merchant-styles.md
  - README.md
  - apps/web/e2e/merchant-styles.spec.ts
  - .github/workflows/ci.yml
---

# 網美與文青店家風格篩選、審核及首批來源資料

## Why

使用者要求網美／文青分類篩選，以及實際蒐集與審核店家。現有分類是料理種類，
不能將風格塞成主菜分類，也不能靠風格跳過店家發布條件。

## Definition of done

- [x] 獨立雙風格可與城市、商圈、料理及文字交叉篩選；僅核准標籤公開。
- [x] 管理員審核需來源、日期、理由，保留版本衝突檢查與稽核。
- [x] 五語系前台卡片、篩選與後台審核表單。
- [x] 首批 5 家來源查核（4 新候選、1 既有），可重跑匯入且不覆寫舊審核。
- [x] 新舊遷移、API/Web、桌面/Pixel 7 驗證；完整 CI 以 PR 最新 SHA 檢查為準。
- [x] PR #345 合併、部署及首批預覽／正式匯入／重播驗證。
- [x] 第二批 8 家官方來源查核及 9 個風格提案，備份後加入正式環境待審清單。
- [ ] 第二批資料／測試／查核交接 PR 完成 CI 與合併（本輪沒有新的合併授權）。
- [ ] 逐家補齊地圖與永久座標、管理員風格審核，再另行發布店家。

## Steps

- [x] 從 main 的獨立工作目錄建立 codex/merchant-style-discovery；保留 #343。
- [x] 新增 0061、公開與管理 API、僅待審匯入路徑及稽核。
- [x] 獨立審核元件、草稿、錯誤狀態、五語系文字。
- [x] 完成程式驗證與 PR #345 交付；上架狀態不可描述成已完成。

## How to verify

API: Ruff、mypy、pytest；Windows 不支援 UnixStreamServer，完整 deployment_agent 測試由 Linux CI 執行。
Web: 單工 Vitest、TypeScript、lint、check:i18n、production build；merchant-styles.spec.ts 跑 desktop/Pixel 7。
匯入及人工查核記錄見 docs/merchant-styles.md。

## Notes

新候選缺精準地圖與可永久保存座標時保持 pending/inactive/unverified，不用來源文字推造識別。
先完成原始來源審查，再於已部署的後台逐一記錄操作人及風格核准；資料檔不能偷帶 approved。
PR #345 已依上一輪授權合併部署；本輪「繼續新增」只補正式待審候選，不代表核准發布。
未啟動付費模型或地圖批次，第二批資料 PR 的合併仍需新授權。

## PR 與驗證交接

- PR: https://github.com/x812033727/travel_scanner/pull/345 ，base `main`。
- Linux CI（92ecde8）：API 1792 passed / 3 skipped，含 PostgreSQL、全套遷移及同時首次審核衝突測試；Ruff、mypy、containers、全端 smoke 通過。
- Web 全套 133 files / 785 tests 通過；TypeScript、lint、五語系檢查與 tools 27 tests 通過。
- 本機 production webpack build 通過；預設 Turbopack 的正式建置由 Linux CI 驗證。本機 node_modules junction 跨 root 不支援 Turbopack，不修改專案設定繞過。
- 最新 UI 的 merchant-styles.spec.ts：22 passed（五語系、深淺模式、desktop / Pixel 7、後台草稿及獨立儲存）；已檢查手機深色及審核成功截圖。此套為 API mock UI 證據，不是正式資料。
- 早期瀏覽器測試使用錯誤的按鈕／select label locator，已改用實際按鈕名稱及具名審核群組的 combobox；不是放寬驗證或延長 timeout。
- #345 合併為 `b3e49a325edcc41e167653e9fe13619403248507`，main CI `34171987990` 全綠，8 個應用服務部署同版本；資料庫 `0061_merchant_styles`。
- 首批正式匯入為 4 新候選＋1 既有店家補標籤，5 pending 風格；既有 FAbULOUS 狀態不變，重播零新增。

## 第二批交接（2026-09-08）

- PR: https://github.com/x812033727/travel_scanner/pull/346 ，base `main`，保留開啟、不自行合併。
- 從上述最新 main 建立 `codex/merchant-style-batch-02`；未碰原 checkout 的 mobile-planner-app-ui 或 PR #343。
- 新增台中2家、京都2家、東京1家、新加坡2家、曼谷1家，9個標籤（網美5、文青4）。完整分店、來源及排除理由見 docs/merchant-styles.md。
- 正式環境比對名稱與地址零重複；JSON checksum 一致、取得兩個部署鎖、備份可讀後套用成功，8 家 pending/inactive/unverified，所有地圖／座標／商圈欄位留空。
- 稽核恰為建立8店及提案9風格各一筆，actor=NULL 系統匯入；再次預覽0店／0標籤。未呼叫管理核准 API。
- 正式伺服器受控批次目錄 `/root/mokaair-merchant-batch-02-ZJOQ5uHv` 保留來源、preview/applied/replay JSON、pre-import.dump 及索引；備份權限600，不刪除舊備份。
- 只匯入資料、不重建映像、不跑新遷移；/ready 正常、公開風格仍0、foods頁200。待審清單在 `/zh-TW/admin/foods`。
- 本機 API 40 passed / 1 skipped（PostgreSQL row-lock 專屬），涵蓋實際第二批 preview/apply/replay、欄位隔離、公開隱藏與稽核；Ruff 全套與 mypy 255 files 通過。
- 新測試初版误用了不存在的 naver_place_id，已按真實模型改為 naver_map_url 並重跑通過；沒有修改產品邏輯或放寬斷言。
- 無 Web 程式或資料庫結構變更；Linux PostgreSQL 與完整 CI 結果查看第二批 PR checks。
