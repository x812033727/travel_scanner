# Gemini 可見目錄與導覽元件

這份交付完成接收可見資料的 UI，尚未接入正式文章頁。正式目錄 JSON 仍只有 50 篇；本票沒有部署、公開新篇章或修改另一個任務持有的 guides 元件。

## 使用方式

```tsx
import { GeminiDirectory } from "@/components/gemini-series/directory";
import { GeminiNavigation } from "@/components/gemini-series/navigation";
import { geminiSeriesCopy } from "@/lib/gemini-series-copy";

// visible 在 article-page 的 server 部分由 getVisibleGeminiSeries 產生。
<GeminiDirectory series={visible} copy={geminiSeriesCopy} />
<GeminiNavigation series={visible} number={50} position="bottom" copy={geminiSeriesCopy} />
```

兩元件沒有預設 catalogue。directory 只匯入純投影 helper 與文案型別；navigation 從同一可見集合找目前、先修、前後篇與延伸。copy 檔只含文案，沒有編輯資料。完整資料下的 UI 提供全部／基礎／深入、六種實作主題，且把閱讀時間與動手時間分開顯示。初始 server HTML 含所有可見文章與路線；route 仍包含原課綱的先修順序，使用者選階段後才按條件縮小。

五種篩選採交集；沒有結果時提供清除入口。指令也只顯示符合階段、主題與路線的目的文章，指令文字另做關鍵字比對。50 篇狀態不顯示深入篩選控制，也不傳入深入文章、路線與指令。

## 已驗證

- 48 個相關單元測試通過，涵蓋兩個 server 集合與原共用文章的複製／內文連結回歸。
- 型別、五語系相同 key、ESLint 通過。
- [Chromium 紀錄](evidence/browser.json)：50／86 篇各驗 1200px 有 JS、360px 有 JS、360px 停用 JS，共六組。查六個關鍵字、階段與主題交集、清除、沒有結果、返回目錄、50→51 與最後一篇、複製原始範例均通過。
- 每篇 server HTML 檢查上一／下一篇，共 136 頁。client build 的模組清單明確拒絕 guide-series.json、curriculum.json、server loader 與 test fixture；50 篇 HTML／序列化資料及 bundle 逐一核對所有 36 個隱藏 slug 均不存在。
- 使用產品實際全域 CSS；六情境無整頁橫向溢出。Windows 剪貼簿把換行轉成 CRLF，核對只正規化換行，保留 tab、引號、標籤與長行。

人工目視：[360px 目錄](evidence/86-360-js.png)、[桌面深入篩選](evidence/filtered-1200.png)、[手機複製與前後篇](evidence/lesson-86-360.png)。文字可讀、選單單欄、導航正常換行，程式長行只在程式區塊內水平捲動。畫面是隔離測試頁，不是公開站截圖。

```powershell
node docs/gemini-series/advanced/platform/visible-ui/verify-browser.mjs
```

測試器使用既有 Vite／React SSR、Playwright 與 Tailwind；只啟動 127.0.0.1 臨時伺服器，結束後關閉。fixture、client、server、.build 都在此驗證目錄；實際產品沒有新增測試 API 或查詢參數開關。`.build` 與暫存失敗紀錄不提交。

## 接線仍由原 platform 任務完成

PR #485 已合併，但 `2026-09-14-claude-code-tutorial-center` 仍處於別人持有的 review；修正該任務狀態需依已提出的確認處理。原任務可認領後：

1. article-page 核對 hub 已發布，產生一次 getVisibleGeminiSeries，將 nullable visible 傳給 GuideArticle。
2. GuideArticle 的 Gemini 區域改用本票元件；停止從 gemini-series.ts 直接或間接匯入未過濾 JSON。原 series-index／navigation 可保留為薄 wrapper 或移除重複實作。
3. Gemini 首頁入口也使用 server 判定。保留 Claude 系列與既有 rich_paragraph／code 行為。
4. 另檢查 hub 正文、章節 links 與 RSC payload，關閉深入時不能只隱藏卡片卻保留正文深入網址。
5. 以實際 Next 文章頁做兩狀態 E2E；本票的獨立 SSR 不取代 Next routing、RSC、發布狀態與 API 整合驗收。

雲端帳號、費用上限、真實模型回答與影片操作仍按各作者任務待驗。本票不以 UI 測試通過宣布整套深入系列完成。
