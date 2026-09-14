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
branch:
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
scope:
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

- [ ] 保留 01–50、八類及五條既有路線；支援 stage、track、操作時間與六條深入路線資料。
- [ ] 伺服器端開關預設不開放第二階段；SSR、客戶端搜尋、路線、前後篇、先修與延伸全部使用相同可見清單。客戶端不能自行重讀未過濾 catalogue。
- [ ] 凍結發布 manifest 的預期篇號、slug 與雜湊；驗證遺漏、重複、未知引用與先修循環。不得只用清單自身長度當完整性證明。
- [ ] 支援 advanced/content/<track>/ 的草稿／來源／素材，能逐批檢查和建置，不把未完成篇章加入正式 catalogue；不新增資料表。
- [ ] 發布可限定第二階段 36 篇及明示的 hub／計費更新；逐篇記錄、失敗停止，保留第一階段收據。
- [ ] 合成 50 篇與 86 篇狀態的桌面、手機、360px 無 JS、複製及導航測試通過；未開放時不洩露新篇 URL，已開放時無缺漏。
- [ ] 維持原 rich_paragraph / code 區塊與共用 Claude Code 系列正常；介面文案五語系同 key。

## Steps

- [ ] 認領並核對目前主線元件、測試與環境變數慣例；新增檔案前補足 scope。
- [ ] 實作可見性與草稿建置介面，將確定的操作命令記錄在 advanced/platform/。
- [ ] 增加必要失敗案例測試，凍結傳給內容作者的 manifest 與素材格式。
- [ ] 完成局部測試、型別、i18n、相關 E2E 與任務檢查後交接；此票不提前發布文章。

## How to verify

先跑相應 series/article 單元測試，再跑 npm run typecheck:web、npm run check:i18n、npm run lint:web、node --test tools/gemini-series.test.mjs、npm run check:tasks。依既有 E2E 協定啟動隔離 fixture，再驗開關兩種狀態。記錄實際命令與結果。

## Notes

目前硬編碼位於 tools/gemini-series.mjs 的 validateCatalogue 與摘要文字；正式 catalogue 保留在 apps/web/lib/guide-series.json，整合由 release 任務最後處理。本票只用 fixture 測新增資料。若需增加 server-only 輔助檔，先把確切路徑加入 scope。
