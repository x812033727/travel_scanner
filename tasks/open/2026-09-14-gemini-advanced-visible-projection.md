---
id: 2026-09-14-gemini-advanced-visible-projection
title: Gemini 深入系列：伺服器可見清單與投影驗證
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-14T14:39:09Z
completed_at:
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
scope:
  - apps/web/lib/gemini-series-projection.ts
  - apps/web/lib/gemini-series-projection.test.ts
  - apps/web/lib/gemini-series.server.ts
  - apps/web/lib/gemini-series.server.test.ts
  - apps/web/vitest.config.ts
  - docs/gemini-series/advanced/platform/visible-projection.md
---

# Gemini 深入系列：伺服器可見清單與投影驗證

## Why

深入篇作者交付已具備，但原平台任務的 guides 元件 scope 被 Claude Code 教學中心認領中，claim 拒絕。先交付不衝突的純資料投影與 server-only 入口，讓後續共用元件只收到可見篇章，避免關閉開關時序列化未發布連結。

## Definition of done

- [x] 預設50篇，明確伺服器開關與完整86篇時才提供深入資料。
- [x] 相同投影支援路線、先修、相關、前後篇、關鍵字與安全站內 href；不傳遞原始 metadata。
- [x] 真實50篇與完整86篇fixture及錯誤案例測試通過，型別／i18n／lint／任務檢查通過。
- [x] 記錄未接線的共用介面及實際E2E限制，原catalogue與原頁面不改。

## Steps

- [x] 完成projection純函式與server-only loader。
- [x] 加入測試與交接文件，保留平台元件整合待辦。

## How to verify

在apps/web執行 npx vitest run lib/gemini-series-projection.test.ts lib/gemini-series.server.test.ts components/guides/series.test.tsx，再跑 npm run typecheck:web、npm run check:i18n、npm run lint:web、npm run check:tasks。

## Notes

2026-09-14：只接手本票列出的獨立檔案，不強制認領共用guides元件。Vitest無Next的server-only解析別名，新增測試環境alias指向Next自帶empty模組；正式建置仍使用server-only的框架邊界。擴scope前核對vitest.config.ts無active交集。

2026-09-14 本機交付完成：可見清單與原Gemini系列相關測試36項通過；完整前端260檔／2834項通過（523.91秒），typecheck／i18n五語系／lint／tasks通過。87份Gemini草稿內容包的字數、圖片與全部連結檢查通過；六批作者收據1001個檔案雜湊核對沒有變動。原50篇catalogue、全部內容包、其他任務元件沒有修改。沒有PR／合併／部署／匯入／發布。

交接見 docs/gemini-series/advanced/platform/visible-projection.md。主平台票仍需在共用元件可認領後接線，移除client原catalogue匯入，並跑真正50/86頁面與無JS E2E；本票測試不能視為該整合已通過。本票先釋出為本機完成待整合狀態。

2026-09-15 更新（台灣時間）：使用者允許封存已合併的 Claude 共用元件票後，主平台票已完成正式文章／目錄／生活頁接線。Next production build、160 項相關測試及 50／86 兩狀態各 10 項實際瀏覽器測試通過，包含 HTML、RSC、正文與 client bundle 不洩漏隱藏 slug。新的收據見 `docs/gemini-series/advanced/platform/next-integration/verification.json`；原正式 50 篇 catalogue 未變，沒有部署或發布。本票及主平台票均為本機完成尚未合併，保留 open。
