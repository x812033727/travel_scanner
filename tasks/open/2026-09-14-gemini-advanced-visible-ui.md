---
id: 2026-09-14-gemini-advanced-visible-ui
title: Gemini 深入目錄：接收可見清單的介面與瀏覽器驗證
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-14T15:18:21Z
completed_at:
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
scope:
  - apps/web/components/gemini-series
  - apps/web/lib/gemini-series-copy.ts
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - docs/gemini-series/advanced/platform/visible-ui
---

# Gemini 深入目錄：接收可見清單的介面與瀏覽器驗證

## Why

共用 guides 元件仍被 Claude 任務的 review 狀態占用。其 PR #485 已於 2026-09-14T05:58:11Z 合併（35a2d258），但依 tasks/README.md 不修改別人持有的任務檔。本票完成可獨立驗證的目錄／導覽元件與接入說明，原頁面接線仍留在 platform 票，沒有強制取得共用 scope。

## Definition of done

- [x] 新元件只使用 server 傳入的 VisibleGeminiSeries；客戶端 bundle 無正式 catalogue、課綱或 test fixture。
- [x] 保留八分類、五基礎路線；完整資料增加六深入路線、stage／track、閱讀與動手時間；搜尋與篩選可交集並清除。
- [x] 50 篇狀態不含任何深入 URL；86 篇狀態連續、先修與相關沿用同一集合，50→51 與末篇邊界正確。
- [x] 實際 Chromium 驗兩狀態的桌面 1200px、手機 360px、360px 無 JS；搜尋、複製、連結與無橫向溢出通過。
- [x] 文案五語系相同 key，單元、型別、i18n、lint 與任務檢查；交接文說明尚未接入 Next 正式文章頁。

## Steps

- [x] 認領無重疊 scope，建立 directory／navigation 與僅含文案的 module。
- [x] 用真實 50 篇與課綱合成 fixture，server 投影後送到獨立 SSR／hydration 瀏覽器；不改 runtime JSON。
- [x] 保存瀏覽器報告、來源雜湊與畫面，將接線缺口留給既有 platform 任務。

## How to verify

node docs/gemini-series/advanced/platform/visible-ui/verify-browser.mjs

npm run test --workspace apps/web -- components/gemini-series/visible-ui.test.tsx components/guides/series.test.tsx lib/gemini-series-projection.test.ts lib/gemini-series.server.test.ts --pool=threads --maxWorkers=1

npm run typecheck:web、npm run check:i18n、npm run lint:web、npm run check:tasks。

## Notes

2026-09-14：相關 48 項測試、型別、五語系鍵與 lint 通過。Chromium 6 種情境通過，server 逐篇驗 50 + 86 = 136 個導航頁；實際 clipboard 在 Windows 回 CRLF，僅正規化換行後逐字比對，沒有移除縮排。目視檢查桌面深入篩選、360px 目錄與複製／導航畫面均正常。

初版測試 fixture 的 Vite library 未替換 process.env.NODE_ENV，造成無法 hydration；已在測試器固定 production，並等待實際 useEffect 就緒，不再以靜態 HTML 當互動通過。修正測試器的學習路線 selector 與 Windows 剪貼簿換行預期後重跑六種情境全部通過；這些不是修改產品以迎合測試。

尚未接到 GuideArticle／article-page／life 首頁，沒有正式 Next routing／RSC 或公開站 E2E 證據。詳見 docs/gemini-series/advanced/platform/visible-ui/README.md。共用接線的權限確認已提出，使用者尚未回覆時不變更別人任務。未改 50 篇 catalogue、環境開關、資料庫、發布／部署或 sitemap。本票本機完成，尚未合併，交回 open。
