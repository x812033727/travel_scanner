# 深入篇伺服器可見清單

這份交付提供伺服器資料邊界，現已接到正式文章、目錄、導航與生活分享元件。原 `guide-series.json` 仍是50篇；六批36篇作者交付已存在，真實雲端驗收與發布仍有待辦。[實際 Next 整合及驗證](next-integration/README.md) 記錄目前接線；下方早期測試結果保留為歷史證據。

## 入口與資料流

`apps/web/lib/gemini-series.server.ts` 使用 `server-only`，只讀原正式 JSON，不讀課綱、作者草稿或第二份清單。文章頁核對 hub 狀態後呼叫：

```tsx
const visible = getVisibleGeminiSeries({
  locale,
  hubPublished: geminiHub?.status === "published" && Boolean(geminiHub.document),
});
```

只有 `GEMINI_ADVANCED_SERIES_ENABLED=true` 精確值會要求第二階段；沒有 NEXT_PUBLIC 版本，不接受 query、cookie或header切換。未發布hub或其他語系回傳null。正式JSON仍只有50篇時，即使設true也不會讀課綱或產生虛構篇章。

完整86篇JSON部署後，開關關閉時只回傳原50篇、八類、五路線。文章先修、相關、指令目標與學習路線都依同一集合過濾；不會將隱藏slug藏在另一個傳給client的metadata欄位。開關開啟且存在深入資料時，要求連續01–86，少一篇直接報錯。完整固定slug、路線與內容正確性仍由既有 release contract 檢查，投影不取代發布驗收。

`gemini-series-projection.ts` 沒有原始JSON、環境或伺服器匯入，可供client僅操作收到的可見資料：

- `filterVisibleGeminiLessons`：搜尋、階段、主題、路線與編輯主題交集；不存在路線回空結果。
- `visibleGeminiMember`：限定語系與life類型，未可見slug不回傳文章。
- `visibleGeminiNavigation`：以可見篇序找前後篇，50篇狀態的第50篇沒有下一篇；完整狀態接51，86篇結尾不循環。
- `visibleGeminiHref`：只為可見文章或本系列hub產生站內網址，可附既有章節anchor。

每篇可見資料包含stage、編輯track與動手時間labMinutes。UI可以顯示全部／基礎／深入，並將閱讀minutes與動手時間分開，不將模型等待時間當成閱讀時間。

## 共用元件接線

早期原平台任務認領被 `2026-09-14-claude-code-tutorial-center` 的 active/review scope 拒絕。後續使用者已允許修正任務狀態；核對 PR #485 已合併且其 merge commit 是本分支祖先後封存該票，原平台票已正式認領並完成以下接線。

接線與驗證項目：

1. `article-page.tsx` 重用已查到的hub發布狀態，產生一次visible props；傳給文章、目錄與導航。
2. `series-index.tsx` 只收visible，不再從gemini-series匯入原catalogue。用純投影helper搜尋／路線／階段。初始SSR輸出完整可見分類；沒有JavaScript仍可瀏覽全部連結。
3. `gemini-series-navigation.tsx` 用同一visible與nav helper，不再以全catalogue重查先修或前後篇。
4. `article.tsx` 和生活入口使用相同已過濾身分。UI文案移交原平台票，五語系同key。Client若仍從舊gemini-series.ts間接匯入JSON，視為未完成。
5. 檢查hub正文、rich_paragraph、一般list/link及其RSC payload是否殘留未開放深入URL；不能只驗卡片數量。開關關閉時已發布的新版hub正文若含深入連結，必須有一致的正文呈現策略，或保持原hub包至啟用時刻。
6. 用實際Next頁面跑50/86兩種狀態的桌面、手機、360px無JS、複製、前後篇與完整頁面連結。新的資料helper單元測試不是這些E2E已通過。

目前未設置production環境變數，未更新JSON、公開入口、hub內容、sitemap、資料庫或部署。直接URL於逐篇匯入期間的可讀性沿用既有發布制度；這份helper主要限制目錄與導覽。

## 驗證

```powershell
# apps/web 目錄
npx vitest run lib/gemini-series-projection.test.ts lib/gemini-series.server.test.ts components/guides/series.test.tsx
# 儲存庫根目錄
npm run typecheck:web
npm run check:i18n
npm run lint:web
npm run test:web
npm run check:tasks
```

單元測試從真實原50篇與課綱合成完整86篇，對照既有frozen身份清單，驗證雙狀態、缺篇、重複身分、偽造stage、未知track、序列化不洩漏、所有前後篇與關鍵字。server-only測試中由Vitest對應Next自帶empty marker；正式Next仍保有框架的client/server邊界。

2026-09-14 早期投影階段：相關36項通過；完整前端260檔、2834項全通過（523.91秒）。型別、五語系鍵值、ESLint、任務檢查均通過，任務工具僅回報其他既有scope／逾期警告。當時全部87份草稿包檢查通過，六批共1001個已記錄檔案雜湊核對一致。該批結果尚未涵蓋共用接線；後續實際 Next 頁面 50／86 驗證結果見 [next-integration](next-integration/README.md)，不可將歷史資料測試當作發布證明。
