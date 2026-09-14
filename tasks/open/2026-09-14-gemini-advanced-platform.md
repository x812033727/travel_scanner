---
id: 2026-09-14-gemini-advanced-platform
title: Gemini 深入系列：可見篇章與發布批次支援
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-14T11:10:39Z
completed_at:
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
scope:
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.tsx
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
  - apps/web/app/(ads-public)/[locale]/life/[slug]/page.tsx
  - apps/web/app/(ads-public)/[locale]/life/[slug]/page.test.tsx
  - apps/web/lib/gemini-series.server.ts
  - apps/web/lib/gemini-series.server.test.ts
  - apps/web/lib/gemini-series-content.ts
  - apps/web/lib/gemini-series-content.test.ts
  - apps/web/components/guides/gemini-page.test.tsx
  - apps/web/lib/gemini-series.ts
  - apps/web/components/guides/series-index.tsx
  - apps/web/components/guides/gemini-series-navigation.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/e2e/gemini-series.spec.ts
  - apps/web/lib/gemini-series.test.ts
  - apps/web/components/guides/series.test.tsx
  - apps/web/components/guides/article.test.tsx
  - tools/gemini-series.mjs
  - tools/gemini-series.test.mjs
  - docs/gemini-series/build.py
  - docs/gemini-series/render-art.mjs
  - docs/gemini-series/advanced/platform
---

# Gemini 深入系列：可見篇章與發布批次支援

## Why

既有 Gemini 總目錄已發布，工具固定驗證 50 篇／51 頁。第二階段擬新增 36 篇，必須先支援可見篇章投影及受限發布批次，避免部署新 catalogue 就提前露出未發布連結。完整規格見 [深入課綱](../../docs/gemini-series/advanced/README.md#navigation)。

## Definition of done

- [x] 保留 01–50、八類及五條既有路線；支援 stage、track、操作時間與六條深入路線資料。
- [x] 伺服器端開關預設不開放第二階段；SSR、客戶端搜尋、路線、前後篇、先修與延伸全部使用相同可見清單。客戶端不能自行重讀未過濾 catalogue。
- [x] 凍結發布 manifest 的預期篇號、slug 與雜湊；驗證遺漏、重複、未知引用與先修循環。不得只用清單自身長度當完整性證明。
- [x] 支援 advanced/content/<track>/ 的草稿／來源／素材，能逐批檢查和建置，不把未完成篇章加入正式 catalogue；不新增資料表。
- [x] 發布可限定第二階段 36 篇及明示的 hub／計費更新；逐篇記錄、失敗停止，保留第一階段收據。
- [x] 合成 50 篇與 86 篇狀態的桌面、手機、360px 無 JS、複製及導航測試通過；未開放時不洩露新篇 URL，已開放時無缺漏。
- [x] 維持原 rich_paragraph / code 區塊與共用 Claude Code 系列正常；介面文案五語系同 key。

## Steps

- [x] 認領並核對目前主線元件、測試與環境變數慣例；新增檔案前補足 scope。
- [x] 實作可見性與草稿建置介面，將確定的操作命令記錄在 advanced/platform/。
- [x] 增加必要失敗案例測試，凍結傳給內容作者的 manifest 與素材格式。
- [x] 完成局部測試、型別、i18n、相關 E2E 與任務檢查後交接；此票不提前發布文章。

## How to verify

先跑相應 series/article 單元測試，再跑 npm run typecheck:web、npm run check:i18n、npm run lint:web、node --test tools/gemini-series.test.mjs、npm run check:tasks。依既有 E2E 協定啟動隔離 fixture，再驗開關兩種狀態。記錄實際命令與結果。

## Notes

目前硬編碼位於 tools/gemini-series.mjs 的 validateCatalogue 與摘要文字；正式 catalogue 保留在 apps/web/lib/guide-series.json，整合由 release 任務最後處理。本票只用 fixture 測新增資料。若需增加 server-only 輔助檔，先把確切路徑加入 scope。

## 2026-09-15 本機接線紀錄（台灣時間）

使用者本輪「繼續」允許修正已合併 PR #485 的任務狀態。重新核對 PR 為 MERGED、merge commit `35a2d258b51d2a1ac9aff91dc5f7ed5a8df823ec` 是本分支祖先後封存舊票，成功認領本票；未強制覆蓋其他 active scope。封存後原 open 檔殘留的再次觀察合併到既有 tasks-done-retains-open-copy 票。

article-page 重用 hub 發布狀態，一次產生 visible props；共用文章、目錄、導航與 life 入口接線完成。原 gemini-series module 不再讀 JSON。server 另過濾正文 rich/link/article、list/table/code 等文字參照及 article_links，保持二級標題位置；生活卡片與 ItemList 也使用相同集合。Claude 系列與原區塊有回歸覆蓋。

完整 Next 16.3.3 建置揭露兩個既有文章 route 的 generateMetadata 使用可選 parent，不符合 generated route type checks。已先擴 scope，再依本地 Next 文件改成必要 ResolvingMetadata，測試傳入空 parent；未關閉建置型別檢查。Node 24.19.0 的 production build、來源型別、ESLint、五語系鍵值均通過。

相關前端 13 檔／160 項全過，系列工具 17 項全過；87 份草稿包的清單、字數、素材與內部連結全過。原 50 篇 catalogue SHA-256 維持 `1f6afed7f3bf7f05a407b8d5af4647938cf6d91df6b42a381a904b1f6d697bb2`。隔離 fixture 的 893 份來源與 87 份文章包已逐一核對；86 篇資料僅存在忽略的 Next 副本。

實際 Next E2E 與最終結果見 `docs/gemini-series/advanced/platform/next-integration/README.md`，包括初次 loopback ECONNRESET 的診斷摘要與重跑。測試代理僅對 GET ECONNRESET 重試一次，HTTP 錯誤與產品斷言未變更。

本票沒有改正式 catalogue、公開內容或環境變數，沒有 PR／推送／合併／部署／資料庫匯入。深入內容的真實 Google 帳號、收費與模型／影片操作仍按作者票及 release 票驗收；不得將本機網站測試視為整套發布。

最終 50 篇 10／10、86 篇重跑 10／10 全過；桌面與手機共逐篇核對 272 次正文，另驗 hub、無 JS、RSC、所有隱藏 slug、生活卡片與 client bundle。無整頁橫向溢出，真實 code 剪貼簿通過。截圖與初次失敗摘要均保留，詳細限制見 next-integration/verification.json。所有本票檢查項已在本機完成，尚未 PR／合併；釋出供後續整合，不標記 done。
