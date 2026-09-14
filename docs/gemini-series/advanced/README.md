# Gemini 深入教學：第二階段課綱（51–86）

狀態：**規劃完成，36 篇文章、素材與實測尚未製作或發布。** 規劃與官方文件查證日：2026-09-14。

沿用 [Gemini 教學總目錄](https://mokaair.com/zh-TW/life/gemini-guide)，保留既有 01–50 的 slug 與篇序。第二階段增加 36 篇，完成後為 **1 個總目錄＋86 篇教學，共 87 頁**。本頁連結到新題目的位置是「課綱卡片」；正式網址只列為預定 slug，尚未建立公開教學連結。

每篇讓讀者完成一個可檢查的成果，包含操作、範本、失敗案例與修正。一般使用者先走工作、研究、創作路線；想深入 MD、CLI 或 Python 的讀者再進入技術路線。這次明確擴充原生活分享總表的入門深度，並保留先修連結。

[查看六大主題](#catalogue) · [閱讀路線](#routes) · [每篇標準](#standards) · [目錄與發布設計](#navigation) · [製作順序與任務](#tasks) · [官方來源](#sources)

篇章資料集中於 [curriculum.json](curriculum.json)，本頁是相同資料的人類可讀課綱；修訂時須同步核對。它是編輯草案，不是第二份網站導覽資料。正式站繼續只讀 `apps/web/lib/guide-series.json`，到整套驗收時才整合第二階段資料。

<a id="catalogue"></a>
## 六大主題與全部篇章

這六組是第二階段的編輯主題與深入路線，**不是再增加六個網站分類**。正式目錄仍保留 A–H 八類，每篇的 `group` 指向既有分類。閱讀時間暫估每篇約 8 分鐘，正式產出後依正文計算；下面另列實際動手練習的時間，不含雲端生成、排程或批次等待。

### 日常與工作流程｜51–56

| 篇號與課綱 | 做完會得到什麼 | 動手時間 |
| --- | --- | --- |
| [51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51) | 留下能重做的提示詞 A/B 比較與評分表。 | 約 40 分鐘 |
| [52 Gems 客服知識助手：資料更新、拒答與回歸測試](#lesson-52) | 製作依商品手冊回答、遇到缺資料會轉人工的助手。 | 約 50 分鐘 |
| [53 Canvas 實作活動預算計算器：需求、除錯與驗收](#lesson-53) | 完成可調整人數、單價與備用金的預算小工具。 | 約 60 分鐘 |
| [54 Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦](#lesson-54) | 將散落信件轉成附來源、負責人與日期的交接表。 | 約 50 分鐘 |
| [55 手機現場筆記：Gemini Live、照片與回到電腦整理](#lesson-55) | 把現場觀察整理成可核對的清單與圖文筆記。 | 約 40 分鐘 |
| [56 Spark 每週資訊摘要：設定排程、檢查結果與停止任務](#lesson-56) | 建立範圍有限、來源可追查的每週摘要任務。 | 約 50 分鐘 |

### NotebookLM 與研究方法｜57–62

| 篇號與課綱 | 做完會得到什麼 | 動手時間 |
| --- | --- | --- |
| [57 NotebookLM 資料版本管理：來源清單、更新與過期內容](#lesson-57) | 建立能追蹤資料版本的專題筆記本。 | 約 45 分鐘 |
| [58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58) | 用證據矩陣辨識資料支持、矛盾及未回答的問題。 | 約 45 分鐘 |
| [59 NotebookLM 備考實作：題庫、錯題分類與間隔複習](#lesson-59) | 由兩章教材製作可檢查答案的複習流程。 | 約 60 分鐘 |
| [60 NotebookLM 比較多篇研究：研究問題、方法與限制矩陣](#lesson-60) | 產出區分研究設計與結論強度的比較表。 | 約 60 分鐘 |
| [61 NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查](#lesson-61) | 將同一份教材製作成可對照來源的三種學習材料。 | 約 70 分鐘 |
| [62 Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告](#lesson-62) | 完成一份問題明確、引用可追查的長文報告。 | 約 90 分鐘 |

### 圖片、影片與資料作品｜63–68

| 篇號與課綱 | 做完會得到什麼 | 動手時間 |
| --- | --- | --- |
| [63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63) | 製作同一原創商品的三張用途不同但風格一致的圖片。 | 約 60 分鐘 |
| [64 Gemini 修圖除錯：局部修改、文字錯誤與多輪退化](#lesson-64) | 用可追蹤的修改紀錄完成指定區域的修圖。 | 約 50 分鐘 |
| [65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65) | 完成具開場、過程與收尾的短片專案。 | 約 90 分鐘 |
| [66 Google Flow 畫面連貫：起訖影格、參考素材與轉場修正](#lesson-66) | 修正兩個片段間的主體、動作與鏡位不連貫。 | 約 70 分鐘 |
| [67 Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表](#lesson-67) | 將含錯誤的資料整理成總數正確、可追查來源的報表。 | 約 70 分鐘 |
| [68 Gemini 內容專案交付：文章、圖片與短片的版本和素材清單](#lesson-68) | 交付同一活動的文章、三張圖與短片，附完整素材記錄。 | 約 90 分鐘 |

### MD 與 CLI 設定實驗｜69–74

| 篇號與課綱 | 做完會得到什麼 | 動手時間 |
| --- | --- | --- |
| [69 GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](#lesson-69) | 以最小專案觀察每份規則何時進入上下文。 | 約 60 分鐘 |
| [70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70) | 製作可維護的共用規則加前後端專案範本。 | 約 60 分鐘 |
| [71 settings.json 設定除錯：來源優先順序與升級前後比較](#lesson-71) | 定位一項設定為何未生效，保存可重做的診斷程序。 | 約 60 分鐘 |
| [72 自訂 CLI 指令庫：程式審查、測試計畫與文件同步](#lesson-72) | 建立三個可重用、可測試的 TOML 指令。 | 約 70 分鐘 |
| [73 把 SKILL.md 打包成 Extension：安裝、更新與回退](#lesson-73) | 將文件檢查技能打包成可安裝的本機擴充套件。 | 約 90 分鐘 |
| [74 大型專案的 CLI 上下文：分段任務、Git 差異與恢復](#lesson-74) | 在含多個模組的專案只修改指定範圍並保存恢復點。 | 約 80 分鐘 |

### CLI 擴充與自動化專案｜75–80

| 篇號與課綱 | 做完會得到什麼 | 動手時間 |
| --- | --- | --- |
| [75 MCP 實作：建立本機唯讀商品查詢工具並排除連線問題](#lesson-75) | 讓 Gemini CLI 能查詢受範圍限制的合成商品資料。 | 約 90 分鐘 |
| [76 Hooks 品質檢查：事件輸入、退出碼與失敗時停止](#lesson-76) | 做出可觀察且確實會阻擋指定操作的檢查。 | 約 80 分鐘 |
| [77 Subagents 審查工作流：任務契約、工具限制與結果整合](#lesson-77) | 以兩個專門審查代理完成有證據的程式與文件檢查。 | 約 80 分鐘 |
| [78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78) | 讓 20 份文件批次整理可中斷、續跑與追查失敗。 | 約 90 分鐘 |
| [79 Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告](#lesson-79) | 在測試 repository 手動執行工作流並保存可下載的審查報告。 | 約 90 分鐘 |
| [80 CLI 完整專案：文件更新、連結檢查與人工審查交付](#lesson-80) | 將文件維護整合成能產出差異、報告及失敗記錄的流程。 | 約 120 分鐘 |

### API 工程與完整專案｜81–86

| 篇號與課綱 | 做完會得到什麼 | 動手時間 |
| --- | --- | --- |
| [81 Function calling 實作：參數驗證、工具回傳與有限次迴圈](#lesson-81) | 用 Python 建立只查詢合成訂單的工具呼叫流程。 | 約 90 分鐘 |
| [82 Gemini API 搜尋引用：Grounding 結果解析與來源呈現](#lesson-82) | 讓應用程式回傳有來源對應的公開資訊摘要。 | 約 80 分鐘 |
| [83 File Search 知識庫實作：匯入、查詢、更新與刪除驗證](#lesson-83) | 以十份合成規格文件建立有引用的檢索問答。 | 約 100 分鐘 |
| [84 API 快取實驗：隱含快取、手動快取與實際成本核對](#lesson-84) | 比較重複文件請求的使用量，理解快取是否真的有幫助。 | 約 80 分鐘 |
| [85 Batch API 批次評測：工作 ID、部分失敗與重送管理](#lesson-85) | 對固定題庫建立可追蹤、可收斂的離線批次評測。 | 約 100 分鐘 |
| [86 文件助手進階專案：有引用的問答服務、評測與交接](#lesson-86) | 完成可本機使用、有來源引用與測試資料的文件問答服務。 | 約 120 分鐘 |

<a id="routes"></a>
## 從現有文章接到深入實作

原本五條入門路線保留；增加以下六條深入路線，全部引用同一份篇章資料。路線為推薦閱讀次序，單篇仍要列出自己的完整先修條件。

- **把日常工作做成可重用流程：** [09 提示詞怎麼寫：目標、背景與輸出格式](https://mokaair.com/zh-TW/life/gemini-prompt-writing-guide) → [11 Gems 自訂助手：指令、資料與測試](https://mokaair.com/zh-TW/life/gemini-gems-custom-assistants) → [51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51) → [52 Gems 客服知識助手：資料更新、拒答與回歸測試](#lesson-52) → [53 Canvas 實作活動預算計算器：需求、除錯與驗收](#lesson-53) → [17 Gmail、Docs 與 Slides：信件、文件與簡報](https://mokaair.com/zh-TW/life/gemini-in-gmail-docs-sheets) → [18 Google Sheets：公式、整理與資料核對](https://mokaair.com/zh-TW/life/gemini-for-google-sheets-formulas) → [19 Connected Apps：Drive、日曆與地圖整合](https://mokaair.com/zh-TW/life/gemini-connected-apps-guide) → [54 Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦](#lesson-54) → [14 Gemini Live：語音、鏡頭與螢幕分享](https://mokaair.com/zh-TW/life/gemini-live-voice-camera) → [55 手機現場筆記：Gemini Live、照片與回到電腦整理](#lesson-55) → [16 Gemini Spark：任務、排程與 Skills](https://mokaair.com/zh-TW/life/gemini-spark-workflows-guide) → [56 Spark 每週資訊摘要：設定排程、檢查結果與停止任務](#lesson-56)
- **研究到有證據的報告：** [13 Deep Research：研究計畫、來源與報告](https://mokaair.com/zh-TW/life/gemini-deep-research-guide) → [20 NotebookLM 入門：資料、筆記本與引用](https://mokaair.com/zh-TW/life/notebooklm-guide) → [21 NotebookLM 進階：測驗、語音與影片摘要](https://mokaair.com/zh-TW/life/notebooklm-for-study-notes) → [57 NotebookLM 資料版本管理：來源清單、更新與過期內容](#lesson-57) → [58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58) → [59 NotebookLM 備考實作：題庫、錯題分類與間隔複習](#lesson-59) → [60 NotebookLM 比較多篇研究：研究問題、方法與限制矩陣](#lesson-60) → [61 NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查](#lesson-61) → [62 Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告](#lesson-62)
- **交付圖片、短片與資料作品：** [23 Gemini 圖片生成與修圖：提示詞與參考圖](https://mokaair.com/zh-TW/life/nano-banana-image-editing) → [24 Veo 與 Google Flow：影片、分鏡與匯出](https://mokaair.com/zh-TW/life/veo-video-generation-guide) → [63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63) → [64 Gemini 修圖除錯：局部修改、文字錯誤與多輪退化](#lesson-64) → [65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65) → [66 Google Flow 畫面連貫：起訖影格、參考素材與轉場修正](#lesson-66) → [10 讀 PDF、圖片與表格：摘要、比對與驗證](https://mokaair.com/zh-TW/life/gemini-file-analysis-guide) → [18 Google Sheets：公式、整理與資料核對](https://mokaair.com/zh-TW/life/gemini-for-google-sheets-formulas) → [67 Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表](#lesson-67) → [51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51) → [68 Gemini 內容專案交付：文章、圖片與短片的版本和素材清單](#lesson-68)
- **MD 設定與除錯：** [35 Markdown 基礎：建立 MD、標題與程式碼](https://mokaair.com/zh-TW/life/gemini-markdown-basics) → [29 Gemini CLI 安裝：第一次在終端機對話](https://mokaair.com/zh-TW/life/gemini-cli-getting-started) → [30 CLI 認證：Google 帳號、API Key 與計費](https://mokaair.com/zh-TW/life/gemini-cli-authentication) → [36 GEMINI.md 入門：建立規則與 /init](https://mokaair.com/zh-TW/life/gemini-cli-gemini-md) → [37 GEMINI.md 進階：範圍、匯入與 /memory](https://mokaair.com/zh-TW/life/gemini-cli-memory-hierarchy) → [38 settings.json：全域、專案與環境變數](https://mokaair.com/zh-TW/life/gemini-cli-settings) → [39 CLI 權限：忽略檔案、可信任資料夾與沙箱](https://mokaair.com/zh-TW/life/gemini-cli-permissions-sandbox) → [40 自訂斜線指令：TOML、參數與重新載入](https://mokaair.com/zh-TW/life/gemini-cli-custom-commands) → [69 GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](#lesson-69) → [70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70) → [71 settings.json 設定除錯：來源優先順序與升級前後比較](#lesson-71) → [72 自訂 CLI 指令庫：程式審查、測試計畫與文件同步](#lesson-72) → [41 MCP 與 Extensions：安裝、驗證與停用](https://mokaair.com/zh-TW/life/gemini-cli-mcp-extensions) → [42 Agent Skills：建立可重用的 SKILL.md](https://mokaair.com/zh-TW/life/gemini-cli-agent-skills) → [73 把 SKILL.md 打包成 Extension：安裝、更新與回退](#lesson-73) → [33 CLI 對話管理：恢復、壓縮與匯出](https://mokaair.com/zh-TW/life/gemini-cli-sessions-context) → [34 CLI 寫程式：理解、規劃、修改與測試](https://mokaair.com/zh-TW/life/gemini-cli-coding-workflow) → [74 大型專案的 CLI 上下文：分段任務、Git 差異與恢復](#lesson-74)
- **CLI 從工具到可恢復流程：** [41 MCP 與 Extensions：安裝、驗證與停用](https://mokaair.com/zh-TW/life/gemini-cli-mcp-extensions) → [43 Hooks：在指定事件執行檢查](https://mokaair.com/zh-TW/life/gemini-cli-hooks) → [44 Subagents：拆分任務與整合結果](https://mokaair.com/zh-TW/life/gemini-cli-subagents) → [45 Headless 模式：批次、JSON 與腳本](https://mokaair.com/zh-TW/life/gemini-cli-headless-automation) → [75 MCP 實作：建立本機唯讀商品查詢工具並排除連線問題](#lesson-75) → [76 Hooks 品質檢查：事件輸入、退出碼與失敗時停止](#lesson-76) → [77 Subagents 審查工作流：任務契約、工具限制與結果整合](#lesson-77) → [78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78) → [79 Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告](#lesson-79) → [80 CLI 完整專案：文件更新、連結檢查與人工審查交付](#lesson-80)
- **API 從第一次呼叫到文件服務：** [47 AI Studio 與第一個 Gemini API 呼叫](https://mokaair.com/zh-TW/life/gemini-api-ai-studio-first-call) → [48 API 檔案與 JSON：結構化輸出及驗證](https://mokaair.com/zh-TW/life/gemini-api-files-structured-output) → [49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide) → [50 完整實作：文件摘要與資料擷取工具](https://mokaair.com/zh-TW/life/gemini-api-document-assistant) → [81 Function calling 實作：參數驗證、工具回傳與有限次迴圈](#lesson-81) → [82 Gemini API 搜尋引用：Grounding 結果解析與來源呈現](#lesson-82) → [58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58) → [83 File Search 知識庫實作：匯入、查詢、更新與刪除驗證](#lesson-83) → [84 API 快取實驗：隱含快取、手動快取與實際成本核對](#lesson-84) → [51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51) → [85 Batch API 批次評測：工作 ID、部分失敗與重送管理](#lesson-85) → [86 文件助手進階專案：有引用的問答服務、評測與交接](#lesson-86)

手機讀者可從第 06／07、14 篇接第 55 篇，再接 54 的電腦交接工作。無程式基礎者可以完成 51–68；技術篇先在 29–50 補齊概念，不把 API 金鑰與一般 Google AI 訂閱混為一談。

<a id="standards"></a>
## 每篇深入教學的交付標準

1. 頁首先展示成品規格、適合讀者、先修、帳號／方案／平台及預估閱讀和操作時間。
2. 提供可下載且有授權說明的練習包：原始資料、提示詞或程式、預期結果、檢查清單、失敗案例。課綱中的檔名是交付需求，現在沒有宣稱檔案已存在。
3. 至少四個連續操作階段，寫出操作位置、實際輸入、成功的判斷方式及下一步。不可只有概念或提示詞清單。
4. 正文維持 1,800–3,000 個中文字；完整程式與大量資料放下載包，核心可複製範例留在正文。正文使用既有 `rich_paragraph.inlines` 與 `code.label`。
5. 交付一個主成果、至少一個刻意出錯的案例、修正過程、三個與本篇直接相關的 FAQ、2–4 篇延伸連結。
6. 每篇至少一張 1600×900 封面與一張手機可讀圖解；共至少 **72 張新增配圖**。圖解應呈現本篇流程、資料流或錯誤前後差異，沿用自繪圖／合規 Commons 圖片規則，避開產品標誌與介面截圖。
7. 實際生成結果與示意圖分開標註。圖片、影片篇保存真實 Gemini／Flow 成品與失敗例；不能用其他模型產出的圖冒充實測結果。引用資料與程式來源須有授權記錄。
8. 每篇來源附查證日期；技術篇另附 OS、CLI／SDK、模型 ID、API 家族與測試命令。真實雲端、SDK fixture、靜態語法、官方文件整理使用不同驗證標籤。
9. 價格、額度與費用計算集中回連第 02、49 篇。第二階段新增的索引、快取保存、Batch 等計費構成由整合任務統一補入第 49 篇，其他篇只列實驗用量與查證日。

第一階段的 CLI／SDK 驗證不能直接當作第二階段通過。新課程提到的拒答、正確引用、圖像一致性等，是需要評測的成果；實際結果未達標就說明限制或修正範例，不承諾模型必定照做。

<a id="navigation"></a>
## 總目錄、互連與整套開放

- 正式網址維持 `/zh-TW/life/gemini-guide`；可選「全部／基礎教學／深入實作」，保留八類、五條原路線與完整 SSR 連結，另加六條深入路線。
- 篇章 metadata 增加階段、編輯主題及操作時間。搜尋包含標題、用途與別名；驗收關鍵字新增 `GEMINI.md`、`/memory`、`SKILL.md`、`RAG`、`Batch`、`快取`、`引用`、`手機`。
- 頁首返回總目錄、分類與先修；正文首次出現的相關功能連到負責教學的文章；文末前後篇、2–4 篇相關教學與回目錄。站內同分頁，手機單欄、導覽換行。既有 `section-N` 錨點不能因插入新章節而無聲改指其他內容。
- `tools/gemini-series.mjs` 目前固定檢查 50 篇／51 頁與五路線。實作時改成驗證明確凍結的發布清單、數量、唯一 slug、引用及先修無循環；不能只把每個數字改成 86，或從待驗資料自己推導數量而漏掉遺失篇章。
- 建置工具支援 `advanced/content/<track>/` 的原稿、素材定義、來源與驗證資料；正式 metadata 由整合任務匯入單一 catalogue。各內容批次不搶寫共用 metadata／來源檔。
- **第二階段有新的發布風險：總目錄早已發布。** 如果部署含 86 篇的 catalogue，現有「hub 已發布」條件會立刻露出尚未匯入的 36 個連結。因此需先完成伺服器端的第二階段可見性開關，預設關閉；同一份可見篇章投影供 SSR、搜尋、路線、先修、延伸及上一篇／下一篇共同使用。不能只在瀏覽器隱藏卡片，客戶端也不能重新讀原始完整 catalogue 而洩露未開放連結。
- 在開關關閉時部署素材及功能，所有 36 篇完整驗收後才依白名單 dry-run、逐篇發布並記錄日誌。任一步失敗即停止及核對已完成項目。
- 確認新增 36 篇與原 50 篇均可讀，再更新 hub 內容、啟用第二階段開關；核對 SSR、手機／桌面、無 JavaScript、複製、全部 87 頁與 sitemap。有直接 URL 的子篇可能在匯入期間可讀，這沿用逐篇提交制度；「整套開放」指目錄與導覽全部可用，不宣稱資料庫原子切換。
- 預期在六個內容批次全部完成後一次開放深入目錄。若 Spark、實體裝置或 API 認證驗證未完成，維持待辦，不能用空白篇章或「敬請期待」湊足 36 篇。

<a id="tasks"></a>
## 製作順序與任務

優先順序以使用者最關心的 MD／CLI 為前排，同時先完成能供其他篇引用的評測方法。這是製作波次，不是分批對外發布；不承諾未評估的人力工期。

| 波次 | 工作 | 依賴與成果 |
| --- | --- | --- |
| 0 | 目錄／建置／發布批次支援 | 先修正固定數量與第二階段可見性；用合成資料驗證兩種狀態。 |
| 1 | 51–56、69–74 | 共 12 篇，建立評分表、工作素材、MD 範本與跨平台實驗。 |
| 2 | 57–62、75–80 | 共 12 篇，沿用前波素材做研究與可恢復自動化。 |
| 3 | 63–68、81–86 | 共 12 篇，交付影音、資料作品與 API 服務，需真實成品及有限成本實測。 |
| 4 | 統一內容／來源／圖解／瀏覽器驗收 | 36 篇全部完成後，再做整套發布與公開驗證。 |

- [Gemini 深入系列：可見篇章與發布批次支援](../../../tasks/open/2026-09-14-gemini-advanced-platform.md)
- [Gemini 深入教學 51–56：日常與工作流程](../../../tasks/open/2026-09-14-gemini-advanced-work.md)
- [Gemini 深入教學 57–62：NotebookLM 與研究方法](../../../tasks/open/2026-09-14-gemini-advanced-research.md)
- [Gemini 深入教學 63–68：圖片、影片與資料作品](../../../tasks/open/2026-09-14-gemini-advanced-creative.md)
- [Gemini 深入教學 69–74：MD 與 CLI 設定實驗](../../../tasks/open/2026-09-14-gemini-advanced-md.md)
- [Gemini 深入教學 75–80：CLI 擴充與自動化專案](../../../tasks/open/2026-09-14-gemini-advanced-automation.md)
- [Gemini 深入教學 81–86：API 工程與完整專案](../../../tasks/open/2026-09-14-gemini-advanced-api.md)
- [Gemini 深入系列：36 篇整套驗收與目錄開放](../../../tasks/open/2026-09-14-gemini-advanced-release.md)

每張製作任務已限定自己的篇章、內容包與圖片目錄。正式開始前先依 `tasks/README.md` 認領；若遇到資料夾、共享檔或已有任務衝突，先修正 scope 和依賴，不直接跨範圍修改。

與既有批次的分工：
- 批次 04 保留跨工具 coding 入門；69–80 僅做 Gemini CLI 的可重做實驗，不重寫第 29–46 篇。
- 批次 08 保留影音工具比較與一般創作入門；63–68 負責 Gemini／Flow 的具體作品與迭代紀錄。
- 批次 09 保留跨工具筆記、會議、提示詞庫及自動化介紹；51–62 以具體資料包、操作及驗收為界，未發布的跨工具題目不做公開連結。
- 批次 10 保留跨供應商費用、安全及政策比較；本系列引用已完成的第 02、15、39、49 篇，避免重複價格表。
- 批次 11 保留一般手機／旅行 AI 工具；55 專講 Live 現場採集與電腦整理的交接練習。

<a id="lessons"></a>
## 逐篇課綱卡片

以下全部是**待製作內容的規格**。已列出先修、操作大綱、練習包、通過條件、失敗情境與官方依據；不等於已完成教學文章。

<a id="lesson-51"></a>
### 51｜提示詞改寫實驗：用固定題庫找出有效的修改

預定 slug：`gemini-prompt-evaluation-workshop`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 40 分鐘。

**學完成果：** 留下能重做的提示詞 A/B 比較與評分表。

**先修：** [09 提示詞怎麼寫：目標、背景與輸出格式](https://mokaair.com/zh-TW/life/gemini-prompt-writing-guide)、[10 讀 PDF、圖片與表格：摘要、比對與驗證](https://mokaair.com/zh-TW/life/gemini-file-analysis-guide)。

**開始前條件：** Gemini 網頁帳號；寫作時查當日功能入口與方案。範例全部使用合成或可公開材料。

1. 建立 10 題客服摘要題庫與人工答案要點。
2. 固定帳號、模型、輸入資料與日期，分別跑 A/B 提示詞。
3. 依正確性、漏項、格式與不確定性評分。
4. 只改一項指示重做，保存原始結果與失敗題。

**練習包：** prompts-v1-v2.md、cases.csv、rubric.csv；正文示範一題完整前後差異。

**通過條件：** 10 題均有兩版原始輸出與逐項評分；結論能連到具體題目。

**故障練習：** 加入缺日期與互相矛盾的題目，不能靠補造資訊提高分數。

**官方查證起點：** [Google Workspace 提示詞](https://support.google.com/docs/answer/15013615?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [09 提示詞怎麼寫：目標、背景與輸出格式](https://mokaair.com/zh-TW/life/gemini-prompt-writing-guide)、[10 讀 PDF、圖片與表格：摘要、比對與驗證](https://mokaair.com/zh-TW/life/gemini-file-analysis-guide)、[52 Gems 客服知識助手：資料更新、拒答與回歸測試](#lesson-52)。

下一篇課綱：[52 Gems 客服知識助手：資料更新、拒答與回歸測試](#lesson-52) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-52"></a>
### 52｜Gems 客服知識助手：資料更新、拒答與回歸測試

預定 slug：`gemini-gems-support-playbook`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 50 分鐘。

**學完成果：** 製作依商品手冊回答、遇到缺資料會轉人工的助手。

**先修：** [11 Gems 自訂助手：指令、資料與測試](https://mokaair.com/zh-TW/life/gemini-gems-custom-assistants)、[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)。

**開始前條件：** Gemini 網頁帳號；寫作時查當日功能入口與方案。範例全部使用合成或可公開材料。

1. 整理虛構商品手冊、退換貨規則與更新日期。
2. 在 Gems 介面設定回答規則與參考資料。
3. 用已知、未知、過期資訊各類問題測試。
4. 更新一條規則後重跑固定題庫並記錄差異。

**練習包：** product-handbook-v1-v2.md、gem-instructions.md、12 題回歸題庫。

**通過條件：** 所有已知答案可回指資料；更新前後差異與未知題處理均留存。

**故障練習：** 加入手冊不存在的保固承諾；回答必須指出缺資料而非承諾補償。

**官方查證起點：** [Gems 使用方式](https://support.google.com/gemini/answer/15236405?hl=en-GB)、[Google Workspace 提示詞](https://support.google.com/docs/answer/15013615?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [11 Gems 自訂助手：指令、資料與測試](https://mokaair.com/zh-TW/life/gemini-gems-custom-assistants)、[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)、[53 Canvas 實作活動預算計算器：需求、除錯與驗收](#lesson-53)。

上一篇課綱：[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51) · 下一篇課綱：[53 Canvas 實作活動預算計算器：需求、除錯與驗收](#lesson-53) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-53"></a>
### 53｜Canvas 實作活動預算計算器：需求、除錯與驗收

預定 slug：`gemini-canvas-budget-calculator`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 60 分鐘。

**學完成果：** 完成可調整人數、單價與備用金的預算小工具。

**先修：** [12 Canvas：編輯文章、簡報與製作小工具](https://mokaair.com/zh-TW/life/gemini-canvas-guide)、[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)。

**開始前條件：** Gemini 網頁帳號；寫作時查當日功能入口與方案。範例全部使用合成或可公開材料。

1. 先寫欄位、公式與三組人工算好的答案。
2. 用 Canvas 產生單頁計算器並檢查程式與預覽。
3. 加入空白、負數與小數測試並根據錯誤逐項修正。
4. 匯出程式，分別在手機尺寸與桌面檢查。

**練習包：** requirements.md、test-cases.csv、完整單頁程式；不加入雲端資料庫。

**通過條件：** 三組金額均符合人工計算；重新輸入與重設可用，360px 可操作。

**故障練習：** 空值、非數字與負數有可理解提示，不能產生 NaN 或默默當成零。

**官方查證起點：** [Canvas 文件與小工具](https://support.google.com/gemini/answer/16047321?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [12 Canvas：編輯文章、簡報與製作小工具](https://mokaair.com/zh-TW/life/gemini-canvas-guide)、[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)、[54 Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦](#lesson-54)。

上一篇課綱：[52 Gems 客服知識助手：資料更新、拒答與回歸測試](#lesson-52) · 下一篇課綱：[54 Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦](#lesson-54) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-54"></a>
### 54｜Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦

預定 slug：`gemini-workspace-meeting-handoff`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 50 分鐘。

**學完成果：** 將散落信件轉成附來源、負責人與日期的交接表。

**先修：** [17 Gmail、Docs 與 Slides：信件、文件與簡報](https://mokaair.com/zh-TW/life/gemini-in-gmail-docs-sheets)、[18 Google Sheets：公式、整理與資料核對](https://mokaair.com/zh-TW/life/gemini-for-google-sheets-formulas)、[19 Connected Apps：Drive、日曆與地圖整合](https://mokaair.com/zh-TW/life/gemini-connected-apps-guide)。

**開始前條件：** 符合該功能的 Google AI / Workspace 方案與管理員設定；確認繁體中文與實際操作入口，未支援的跨產品步驟改為清楚的人工轉存。

1. 使用五封虛構會議信件與附件確認帳號可用入口。
2. 抽出決策、未定事項及承諾，逐項附原始來源。
3. 整理到 Docs，再將待辦轉成 Sheets 欄位。
4. 核對日期時區、重複項及責任人，建立人工確認流程。

**練習包：** mail-samples.md、handoff-template.md、action-items.csv。

**通過條件：** 五封信的決策均有來源；不確定負責人保留待確認；交接表可篩選。

**故障練習：** 同一事項兩封信日期不同時保留衝突，不能自動替人承諾或寄出信件。

**官方查證起點：** [Connected Apps](https://support.google.com/gemini/answer/13695044?hl=zh-Hant)、[Gemini in Sheets](https://support.google.com/docs/answer/14356410?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [18 Google Sheets：公式、整理與資料核對](https://mokaair.com/zh-TW/life/gemini-for-google-sheets-formulas)、[19 Connected Apps：Drive、日曆與地圖整合](https://mokaair.com/zh-TW/life/gemini-connected-apps-guide)、[55 手機現場筆記：Gemini Live、照片與回到電腦整理](#lesson-55)。

上一篇課綱：[53 Canvas 實作活動預算計算器：需求、除錯與驗收](#lesson-53) · 下一篇課綱：[55 手機現場筆記：Gemini Live、照片與回到電腦整理](#lesson-55) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-55"></a>
### 55｜手機現場筆記：Gemini Live、照片與回到電腦整理

預定 slug：`gemini-mobile-field-notes`。中階／Android、iPhone、電腦網頁；閱讀暫估 8 分鐘，動手約 40 分鐘。

**學完成果：** 把現場觀察整理成可核對的清單與圖文筆記。

**先修：** [06 Android 版：安裝、助理設定與手機操作](https://mokaair.com/zh-TW/life/gemini-on-android-assistant)、[07 iPhone 與 iPad：安裝、語音與照片](https://mokaair.com/zh-TW/life/gemini-ios-app-guide)、[14 Gemini Live：語音、鏡頭與螢幕分享](https://mokaair.com/zh-TW/life/gemini-live-voice-camera)、[10 讀 PDF、圖片與表格：摘要、比對與驗證](https://mokaair.com/zh-TW/life/gemini-file-analysis-guide)。

**開始前條件：** Android 與 iPhone 各有獨立帳號／OS／App 版本紀錄；只有文件查證的平台須明示未實測。

1. 準備無個資的桌面物品與觀察清單。
2. Android、iPhone 分別用 Live 與照片提問並保留觀察文字。
3. 回到電腦整理原圖、文字及待確認項目。
4. 比對實物與輸出，補上看不清楚或辨識錯誤的部分。

**練習包：** field-checklist.md、經授權的 Commons 示範照片、field-notes.md；現場自攝只作私人練習紀錄。

**通過條件：** 每項結論能連到照片或人工觀察；兩平台步驟與可用性分開記錄。

**故障練習：** 遮住物品標籤測試，不能把模糊資訊當成確定型號或價格。

**官方查證起點：** [Gemini Live（Android）](https://support.google.com/gemini/answer/15274899?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [14 Gemini Live：語音、鏡頭與螢幕分享](https://mokaair.com/zh-TW/life/gemini-live-voice-camera)、[10 讀 PDF、圖片與表格：摘要、比對與驗證](https://mokaair.com/zh-TW/life/gemini-file-analysis-guide)、[56 Spark 每週資訊摘要：設定排程、檢查結果與停止任務](#lesson-56)。

上一篇課綱：[54 Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦](#lesson-54) · 下一篇課綱：[56 Spark 每週資訊摘要：設定排程、檢查結果與停止任務](#lesson-56) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-56"></a>
### 56｜Spark 每週資訊摘要：設定排程、檢查結果與停止任務

預定 slug：`gemini-spark-weekly-digest`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 50 分鐘。另需至少觀察一次預定的每週排程，等待時間不計入 50 分鐘操作估計。

**學完成果：** 建立範圍有限、來源可追查的每週摘要任務。

**先修：** [16 Gemini Spark：任務、排程與 Skills](https://mokaair.com/zh-TW/life/gemini-spark-workflows-guide)、[13 Deep Research：研究計畫、來源與報告](https://mokaair.com/zh-TW/life/gemini-deep-research-guide)。

**開始前條件：** 依寫作與發布日重新核對 Spark 的帳號、年齡、地區、方案、活動設定與實驗狀態；無法使用時此篇維持草稿，不能改標為已完成。

1. 核對個人帳號、年齡、方案、地區與活動設定。
2. 定義三個官方來源、期間、摘要格式與停止條件。
3. 先執行一次並核對，再設定每週排程。
4. 觀察下一次排程結果，練習暫停、恢復與完全停止。

**練習包：** digest-brief.md、schedule-log.csv、缺資料時的回報範例。

**通過條件：** 至少一次手動與一次排程執行有時間與輸出證據，停止後不再有新執行。

**故障練習：** 來源不可讀時標示缺漏；不能把前週內容當本週更新或自動改用未指定來源。

**官方查證起點：** [Gemini Spark](https://support.google.com/gemini/answer/17094507?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [16 Gemini Spark：任務、排程與 Skills](https://mokaair.com/zh-TW/life/gemini-spark-workflows-guide)、[13 Deep Research：研究計畫、來源與報告](https://mokaair.com/zh-TW/life/gemini-deep-research-guide)、[55 手機現場筆記：Gemini Live、照片與回到電腦整理](#lesson-55)。

上一篇課綱：[55 手機現場筆記：Gemini Live、照片與回到電腦整理](#lesson-55) · 下一篇課綱：[57 NotebookLM 資料版本管理：來源清單、更新與過期內容](#lesson-57) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-57"></a>
### 57｜NotebookLM 資料版本管理：來源清單、更新與過期內容

預定 slug：`notebooklm-source-versioning`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 45 分鐘。

**學完成果：** 建立能追蹤資料版本的專題筆記本。

**先修：** [20 NotebookLM 入門：資料、筆記本與引用](https://mokaair.com/zh-TW/life/notebooklm-guide)。

**開始前條件：** Gemini 網頁帳號；寫作時查當日功能入口與方案。範例全部使用合成或可公開材料。

1. 為六份示範文件建立來源 ID、版本與更新日期。
2. 分別加入 Drive 與上傳檔案，記錄其更新方式。
3. 替換一份修訂文件並用同題檢查新舊答案。
4. 保存版本對照、引用位置與仍待更新的產出。

**練習包：** sources-v1-v2.csv、兩版規格書、update-checklist.md。

**通過條件：** 修訂數字能對回新來源；更新時間、舊產出是否重做均有記錄。

**故障練習：** 同時保留新舊規格時能辨識日期，不能把不同版本數字相加。

**官方查證起點：** [筆記本來源管理](https://support.google.com/gemininotebook/answer/16215270?hl=en)、[Gemini 與 Gemini Notebook 的整合差異](https://support.google.com/gemininotebook/answer/17003757)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [20 NotebookLM 入門：資料、筆記本與引用](https://mokaair.com/zh-TW/life/notebooklm-guide)、[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)。

上一篇課綱：[56 Spark 每週資訊摘要：設定排程、檢查結果與停止任務](#lesson-56) · 下一篇課綱：[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-58"></a>
### 58｜NotebookLM 引用查核：矛盾資料、缺證據與未知答案

預定 slug：`notebooklm-conflicting-sources`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 45 分鐘。

**學完成果：** 用證據矩陣辨識資料支持、矛盾及未回答的問題。

**先修：** [20 NotebookLM 入門：資料、筆記本與引用](https://mokaair.com/zh-TW/life/notebooklm-guide)、[57 NotebookLM 資料版本管理：來源清單、更新與過期內容](#lesson-57)。

**開始前條件：** Gemini 網頁帳號；寫作時查當日功能入口與方案。範例全部使用合成或可公開材料。

1. 準備三份刻意有不同日期與數字的示範資料。
2. 依問題建立主張、來源、引文與判斷欄位。
3. 點開引用核對前後文，不把引用存在視為結論成立。
4. 用資料未提供的題目檢查回答，再修訂問法。

**練習包：** evidence-matrix.csv、三份原創矛盾資料、unknown-questions.md。

**通過條件：** 五個關鍵主張都有引文及人工判斷，矛盾與缺證據分開列出。

**故障練習：** 沒有答案的問題不得補造引用；不要求系統保證每次拒答。

**官方查證起點：** [Gemini 與 Gemini Notebook 的整合差異](https://support.google.com/gemininotebook/answer/17003757)、[筆記本來源管理](https://support.google.com/gemininotebook/answer/16215270?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [20 NotebookLM 入門：資料、筆記本與引用](https://mokaair.com/zh-TW/life/notebooklm-guide)、[57 NotebookLM 資料版本管理：來源清單、更新與過期內容](#lesson-57)、[59 NotebookLM 備考實作：題庫、錯題分類與間隔複習](#lesson-59)。

上一篇課綱：[57 NotebookLM 資料版本管理：來源清單、更新與過期內容](#lesson-57) · 下一篇課綱：[59 NotebookLM 備考實作：題庫、錯題分類與間隔複習](#lesson-59) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-59"></a>
### 59｜NotebookLM 備考實作：題庫、錯題分類與間隔複習

預定 slug：`notebooklm-study-retrieval-practice`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 60 分鐘。

**學完成果：** 由兩章教材製作可檢查答案的複習流程。

**先修：** [21 NotebookLM 進階：測驗、語音與影片摘要](https://mokaair.com/zh-TW/life/notebooklm-for-study-notes)、[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)。

**開始前條件：** Gemini 網頁帳號；寫作時查當日功能入口與方案。範例全部使用合成或可公開材料。

1. 整理章節目標與關鍵概念對照。
2. 分別產生記憶卡與測驗，人工核對題目和答案。
3. 記錄錯題原因並安排重測日期。
4. 比較第一次與重測結果，回到來源修正不良題目。

**練習包：** study-plan.csv、answer-key.md、error-log.csv；提供兩章原創短教材。

**通過條件：** 至少 12 題有答案依據與概念分類；錯題重測紀錄可追蹤。

**故障練習：** 排除兩個答案都合理、超出教材或引文不支持答案的題目。

**官方查證起點：** [筆記本記憶卡與測驗](https://support.google.com/gemininotebook/answer/16958963?hl=en)、[筆記本來源管理](https://support.google.com/gemininotebook/answer/16215270?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [21 NotebookLM 進階：測驗、語音與影片摘要](https://mokaair.com/zh-TW/life/notebooklm-for-study-notes)、[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)、[60 NotebookLM 比較多篇研究：研究問題、方法與限制矩陣](#lesson-60)。

上一篇課綱：[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58) · 下一篇課綱：[60 NotebookLM 比較多篇研究：研究問題、方法與限制矩陣](#lesson-60) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-60"></a>
### 60｜NotebookLM 比較多篇研究：研究問題、方法與限制矩陣

預定 slug：`notebooklm-paper-comparison-matrix`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 60 分鐘。

**學完成果：** 產出區分研究設計與結論強度的比較表。

**先修：** [58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)、[13 Deep Research：研究計畫、來源與報告](https://mokaair.com/zh-TW/life/gemini-deep-research-guide)。

**開始前條件：** Gemini 網頁帳號；寫作時查當日功能入口與方案。範例全部使用合成或可公開材料。

1. 選三份可合法使用的研究材料並記錄來源版本。
2. 先定義問題、樣本、方法、結果與限制欄位。
3. 逐欄提問並對照原文引用。
4. 整理共識、分歧與不能推論的部分。

**練習包：** paper-matrix.csv、讀文問題清單；採方法比較，不做醫療或投資建議。

**通過條件：** 三份資料每個關鍵欄位均有依據或明示未提供；比較表保留研究限制。

**故障練習：** 不同樣本或量尺的數字不能直接排出優劣；二手摘要不能冒充全文。

**官方查證起點：** [筆記本來源管理](https://support.google.com/gemininotebook/answer/16215270?hl=en)、[Gemini 與 Gemini Notebook 的整合差異](https://support.google.com/gemininotebook/answer/17003757)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)、[13 Deep Research：研究計畫、來源與報告](https://mokaair.com/zh-TW/life/gemini-deep-research-guide)、[61 NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查](#lesson-61)。

上一篇課綱：[59 NotebookLM 備考實作：題庫、錯題分類與間隔複習](#lesson-59) · 下一篇課綱：[61 NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查](#lesson-61) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-61"></a>
### 61｜NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查

預定 slug：`notebooklm-multiformat-lesson-pack`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 70 分鐘。

**學完成果：** 將同一份教材製作成可對照來源的三種學習材料。

**先修：** [21 NotebookLM 進階：測驗、語音與影片摘要](https://mokaair.com/zh-TW/life/notebooklm-for-study-notes)、[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)。

**開始前條件：** 用具該功能使用資格的帳號及有權使用的素材；記錄模型、模式、生成時間與實際耗用。素材生成與背景等待不含在操作估計內。

1. 整理一份原創教材與關鍵事實清單。
2. 在筆記本 Studio 產生講義相關內容、語音及影片摘要。
3. 逐項核對人名、數字與概念在不同產出的差異。
4. 以勘誤表記錄修改與重新生成，保存可用的下載格式。

**練習包：** lesson-facts.csv、handout.md、語音與影片範例及勘誤表。

**通過條件：** 10 個關鍵事實逐一核對，生成格式、語言及下載限制均記錄。

**故障練習：** 語音或影片省略必要限定詞時標示修訂；不能宣稱 Gemini 聊天入口等同 Studio。

**官方查證起點：** [筆記本語音摘要](https://support.google.com/gemininotebook/answer/16212820?hl=en)、[Gemini 與 Gemini Notebook 的整合差異](https://support.google.com/gemininotebook/answer/17003757)、[筆記本影片摘要](https://support.google.com/gemininotebook/answer/16454555?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [21 NotebookLM 進階：測驗、語音與影片摘要](https://mokaair.com/zh-TW/life/notebooklm-for-study-notes)、[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)、[62 Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告](#lesson-62)。

上一篇課綱：[60 NotebookLM 比較多篇研究：研究問題、方法與限制矩陣](#lesson-60) · 下一篇課綱：[62 Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告](#lesson-62) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-62"></a>
### 62｜Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告

預定 slug：`gemini-research-report-workshop`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 90 分鐘。

**學完成果：** 完成一份問題明確、引用可追查的長文報告。

**先修：** [13 Deep Research：研究計畫、來源與報告](https://mokaair.com/zh-TW/life/gemini-deep-research-guide)、[57 NotebookLM 資料版本管理：來源清單、更新與過期內容](#lesson-57)、[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)、[60 NotebookLM 比較多篇研究：研究問題、方法與限制矩陣](#lesson-60)。

**開始前條件：** Gemini 網頁帳號；寫作時查當日功能入口與方案。範例全部使用合成或可公開材料。

1. 以公開城市交通資料設定範圍、時間與研究問題。
2. 用 Deep Research 擬計畫並核對蒐集到的原始資料。
3. 將必要資料交給筆記本建立主張與證據矩陣。
4. 撰寫摘要、比較與限制，保存來源日期及更新清單。

**練習包：** research-brief.md、source-register.csv、report.md。

**通過條件：** 報告所有關鍵事實能對回來源，至少列出三個未解問題與更新項目。

**故障練習：** 官方頁面改版或資料年份不同時保留差異，不用流暢敘述掩蓋缺證據。

**官方查證起點：** [Gemini Deep Research](https://support.google.com/gemini/answer/15719111?hl=en)、[筆記本來源管理](https://support.google.com/gemininotebook/answer/16215270?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)、[60 NotebookLM 比較多篇研究：研究問題、方法與限制矩陣](#lesson-60)、[61 NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查](#lesson-61)。

上一篇課綱：[61 NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查](#lesson-61) · 下一篇課綱：[63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-63"></a>
### 63｜Gemini 圖片系列製作：參考圖、風格規格與一致性評分

預定 slug：`gemini-image-consistent-series`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 60 分鐘。

**學完成果：** 製作同一原創商品的三張用途不同但風格一致的圖片。

**先修：** [23 Gemini 圖片生成與修圖：提示詞與參考圖](https://mokaair.com/zh-TW/life/nano-banana-image-editing)、[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)。

**開始前條件：** 用具該功能使用資格的帳號及有權使用的素材；記錄模型、模式、生成時間與實際耗用。素材生成與背景等待不含在操作估計內。

1. 建立主體外觀、配色、鏡位與禁止變動項目。
2. 用自有參考圖生成第一張並記錄完整提示詞。
3. 逐次改變情境，維持其餘條件。
4. 對照原圖評分，保存失敗結果與修訂原因。

**練習包：** style-guide.md、三張成品、三張失敗案例、image-scorecard.csv。

**通過條件：** 三張圖均附主體特徵與比例核對；一致性是評分結果，不保證生成必然一致。

**故障練習：** 商品外形、字樣或數量改變時列為失敗，不以漂亮代替符合需求。

**官方查證起點：** [Gemini 圖片生成與編輯](https://support.google.com/gemini/answer/14286560?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [23 Gemini 圖片生成與修圖：提示詞與參考圖](https://mokaair.com/zh-TW/life/nano-banana-image-editing)、[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)、[64 Gemini 修圖除錯：局部修改、文字錯誤與多輪退化](#lesson-64)。

上一篇課綱：[62 Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告](#lesson-62) · 下一篇課綱：[64 Gemini 修圖除錯：局部修改、文字錯誤與多輪退化](#lesson-64) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-64"></a>
### 64｜Gemini 修圖除錯：局部修改、文字錯誤與多輪退化

預定 slug：`gemini-image-editing-debugging`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 50 分鐘。

**學完成果：** 用可追蹤的修改紀錄完成指定區域的修圖。

**先修：** [23 Gemini 圖片生成與修圖：提示詞與參考圖](https://mokaair.com/zh-TW/life/nano-banana-image-editing)、[63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63)。

**開始前條件：** 用具該功能使用資格的帳號及有權使用的素材；記錄模型、模式、生成時間與實際耗用。素材生成與背景等待不含在操作估計內。

1. 圈定修改目標並列出必須保留的區域。
2. 每輪只改一件事，保存輸入與輸出。
3. 比較文字、邊緣、比例及未要求變動的背景。
4. 若品質退化回到原始圖重做並交付前後對照。

**練習包：** edit-log.csv、原創基準圖、逐輪輸出與差異說明。

**通過條件：** 修改項目逐條可見；保留區域失真如實記錄，必要時回到原稿。

**故障練習：** 刻意加入小字修正任務，顯示失敗和人工補正方法，不保證精準局部遮罩。

**官方查證起點：** [Gemini 圖片生成與編輯](https://support.google.com/gemini/answer/14286560?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [23 Gemini 圖片生成與修圖：提示詞與參考圖](https://mokaair.com/zh-TW/life/nano-banana-image-editing)、[63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63)、[65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65)。

上一篇課綱：[63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63) · 下一篇課綱：[65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-65"></a>
### 65｜Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成

預定 slug：`google-flow-storyboard-workshop`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 90 分鐘。

**學完成果：** 完成具開場、過程與收尾的短片專案。

**先修：** [24 Veo 與 Google Flow：影片、分鏡與匯出](https://mokaair.com/zh-TW/life/veo-video-generation-guide)、[63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63)。

**開始前條件：** 用具該功能使用資格的帳號及有權使用的素材；記錄模型、模式、生成時間與實際耗用。素材生成與背景等待不含在操作估計內。

1. 先寫三鏡頭腳本與每鏡驗收條件。
2. 依當日模型對照選擇素材、影格與畫面比例。
3. 逐鏡生成並記錄失敗原因與使用點數。
4. 編排場景、下載成品，必要時用明示的外部剪輯工具接合。

**練習包：** storyboard.csv、三鏡頭提示詞、素材清單與實際輸出。

**通過條件：** 三鏡頭次序、主體與敘事可辨識；下載格式、實際長度和總成本均留存。

**故障練習：** 選用模型不支援該輸入模式時更換流程，不能把其他模型操作直接套用。

**官方查證起點：** [Google Flow 建立影片](https://support.google.com/flow/answer/16353334?hl=en)、[Flow 模型與功能對照](https://support.google.com/flow/answer/16352836?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [24 Veo 與 Google Flow：影片、分鏡與匯出](https://mokaair.com/zh-TW/life/veo-video-generation-guide)、[63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63)、[66 Google Flow 畫面連貫：起訖影格、參考素材與轉場修正](#lesson-66)。

上一篇課綱：[64 Gemini 修圖除錯：局部修改、文字錯誤與多輪退化](#lesson-64) · 下一篇課綱：[66 Google Flow 畫面連貫：起訖影格、參考素材與轉場修正](#lesson-66) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-66"></a>
### 66｜Google Flow 畫面連貫：起訖影格、參考素材與轉場修正

預定 slug：`google-flow-shot-continuity`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 70 分鐘。

**學完成果：** 修正兩個片段間的主體、動作與鏡位不連貫。

**先修：** [65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65)。

**開始前條件：** 用具該功能使用資格的帳號及有權使用的素材；記錄模型、模式、生成時間與實際耗用。素材生成與背景等待不含在操作估計內。

1. 從前一篇選取相鄰片段與連貫性問題。
2. 以當日模型支援的起訖影格或參考素材重做。
3. 逐格核對主體、光線、動作方向與接點。
4. 記錄哪種方法改善或失敗，再輸出比較版本。

**練習包：** continuity-checklist.md、基準片段、修訂片段、版本對照。

**通過條件：** 兩段片的接點有逐項評分與實際對照，不能只展示成功的一格。

**故障練習：** 模型不支援終點影格或素材組合時給替代步驟並明示限制。

**官方查證起點：** [Google Flow 建立影片](https://support.google.com/flow/answer/16353334?hl=en)、[Flow 模型與功能對照](https://support.google.com/flow/answer/16352836?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65)、[67 Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表](#lesson-67)。

上一篇課綱：[65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65) · 下一篇課綱：[67 Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表](#lesson-67) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-67"></a>
### 67｜Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表

預定 slug：`gemini-sheets-data-audit-dashboard`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 70 分鐘。

**學完成果：** 將含錯誤的資料整理成總數正確、可追查來源的報表。

**先修：** [10 讀 PDF、圖片與表格：摘要、比對與驗證](https://mokaair.com/zh-TW/life/gemini-file-analysis-guide)、[18 Google Sheets：公式、整理與資料核對](https://mokaair.com/zh-TW/life/gemini-for-google-sheets-formulas)。

**開始前條件：** 符合該功能的 Google AI / Workspace 方案與管理員設定；確認繁體中文與實際操作入口，未支援的跨產品步驟改為清楚的人工轉存。

1. 匯入 50 列合成銷售資料並保存原表。
2. 處理日期、空值、重複列與幣別，記錄清理規則。
3. 用 Gemini 協助公式及圖表，再用人工基準核對。
4. 建立來源列、計算欄與圖表範圍的追蹤關係。

**練習包：** sales-dirty.csv、expected-totals.csv、cleaning-log.md、Sheets 模板。

**通過條件：** 有效列數、分組金額及圖表總數均與基準吻合；每個排除項有理由。

**故障練習：** 重複資料和空白金額必須被發現；不能讓模型自行刪除異常但真實的交易。

**官方查證起點：** [Gemini in Sheets](https://support.google.com/docs/answer/14356410?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [10 讀 PDF、圖片與表格：摘要、比對與驗證](https://mokaair.com/zh-TW/life/gemini-file-analysis-guide)、[18 Google Sheets：公式、整理與資料核對](https://mokaair.com/zh-TW/life/gemini-for-google-sheets-formulas)、[68 Gemini 內容專案交付：文章、圖片與短片的版本和素材清單](#lesson-68)。

上一篇課綱：[66 Google Flow 畫面連貫：起訖影格、參考素材與轉場修正](#lesson-66) · 下一篇課綱：[68 Gemini 內容專案交付：文章、圖片與短片的版本和素材清單](#lesson-68) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-68"></a>
### 68｜Gemini 內容專案交付：文章、圖片與短片的版本和素材清單

預定 slug：`gemini-content-production-handoff`。中階／電腦網頁；閱讀暫估 8 分鐘，動手約 90 分鐘。

**學完成果：** 交付同一活動的文章、三張圖與短片，附完整素材記錄。

**先修：** [51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)、[63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63)、[65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65)。

**開始前條件：** 用具該功能使用資格的帳號及有權使用的素材；記錄模型、模式、生成時間與實際耗用。素材生成與背景等待不含在操作估計內。

1. 從單一活動資料表定義受眾、規格與不可變更的事實。
2. 分別製作文章、圖片與影片，保存提示詞及版本。
3. 核對各格式的日期、名稱、尺寸與素材來源。
4. 整理交付資料夾、修改單與已知限制。

**練習包：** brief.md、asset-register.csv、handoff.md、完整範例成果包。

**通過條件：** 每個成品可追到輸入、版本、素材與核對人；同一活動資訊無矛盾。

**故障練習：** 活動日期變更後能找出所有受影響成品，不能只改文章漏掉影片字卡。

**官方查證起點：** [Gemini 圖片生成與編輯](https://support.google.com/gemini/answer/14286560?hl=en)、[Google Flow 建立影片](https://support.google.com/flow/answer/16353334?hl=en)、[Google Workspace 提示詞](https://support.google.com/docs/answer/15013615?hl=en)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [63 Gemini 圖片系列製作：參考圖、風格規格與一致性評分](#lesson-63)、[65 Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](#lesson-65)、[67 Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表](#lesson-67)。

上一篇課綱：[67 Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表](#lesson-67) · 下一篇課綱：[69 GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](#lesson-69) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-69"></a>
### 69｜GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則

預定 slug：`gemini-cli-memory-scope-lab`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 60 分鐘。

**學完成果：** 以最小專案觀察每份規則何時進入上下文。

**先修：** [36 GEMINI.md 入門：建立規則與 /init](https://mokaair.com/zh-TW/life/gemini-cli-gemini-md)、[37 GEMINI.md 進階：範圍、匯入與 /memory](https://mokaair.com/zh-TW/life/gemini-cli-memory-hierarchy)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 建立隔離測試家目錄與含兩個子目錄的示範專案。
2. 放入不同標記的 GEMINI.md 與匯入檔。
3. 依序檢查啟動、檔案存取與 /memory show、reload。
4. 修改與移走一份規則，記錄載入範圍及信任邊界差異。

**練習包：** memory-lab/、expected-context.csv、PowerShell 與 shell 操作表。

**通過條件：** 每步載入內容、CLI 版本及工作目錄均有紀錄；區分載入證據與模型是否遵循。

**故障練習：** 刻意製造衝突或缺檔，不能宣稱下層規則必定覆寫上層或每次被模型遵守。

**官方查證起點：** [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [36 GEMINI.md 入門：建立規則與 /init](https://mokaair.com/zh-TW/life/gemini-cli-gemini-md)、[37 GEMINI.md 進階：範圍、匯入與 /memory](https://mokaair.com/zh-TW/life/gemini-cli-memory-hierarchy)、[70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70)。

上一篇課綱：[68 Gemini 內容專案交付：文章、圖片與短片的版本和素材清單](#lesson-68) · 下一篇課綱：[70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-70"></a>
### 70｜GEMINI.md 團隊範本：拆分規則、匯入與維護責任

預定 slug：`gemini-cli-modular-project-rules`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 60 分鐘。

**學完成果：** 製作可維護的共用規則加前後端專案範本。

**先修：** [69 GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](#lesson-69)、[35 Markdown 基礎：建立 MD、標題與程式碼](https://mokaair.com/zh-TW/life/gemini-markdown-basics)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 列出共用語言、檢查命令與目錄責任。
2. 拆成精簡主檔、開發規範與任務專用說明。
3. 設定匯入並用同一範例專案驗證。
4. 加入規則變更紀錄與新成員接手流程。

**練習包：** GEMINI.md、rules/style.md、rules/testing.md、rules/ownership.md。

**通過條件：** 所有匯入可解析，命令在範例專案可執行；每條規則有適用目錄與維護理由。

**故障練習：** 失效檔案路徑或互相矛盾的命令要被檢查找出，不把規則堆疊當成穩定性保證。

**官方查證起點：** [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [69 GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](#lesson-69)、[35 Markdown 基礎：建立 MD、標題與程式碼](https://mokaair.com/zh-TW/life/gemini-markdown-basics)、[71 settings.json 設定除錯：來源優先順序與升級前後比較](#lesson-71)。

上一篇課綱：[69 GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](#lesson-69) · 下一篇課綱：[71 settings.json 設定除錯：來源優先順序與升級前後比較](#lesson-71) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-71"></a>
### 71｜settings.json 設定除錯：來源優先順序與升級前後比較

預定 slug：`gemini-cli-settings-debug-lab`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 60 分鐘。

**學完成果：** 定位一項設定為何未生效，保存可重做的診斷程序。

**先修：** [38 settings.json：全域、專案與環境變數](https://mokaair.com/zh-TW/life/gemini-cli-settings)、[69 GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](#lesson-69)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 鎖定 CLI 版本並建立乾淨的全域及專案設定。
2. 一次改一項設定，記錄環境變數與命令列影響。
3. 加入格式錯誤、未知欄位與舊版設定觀察診斷。
4. 依官方 schema 比較版本，驗證後才搬回真實專案。

**練習包：** settings-cases/、effective-settings.csv、migration-checklist.md。

**通過條件：** 至少六組案例記錄預期與實際行為；有效設定能追到來源。

**故障練習：** 未知欄位可能被忽略或拒絕，必須依實際版本記錄，不能一概當成成功。

**官方查證起點：** [CLI 設定參考](https://geminicli.com/docs/reference/configuration/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [38 settings.json：全域、專案與環境變數](https://mokaair.com/zh-TW/life/gemini-cli-settings)、[69 GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](#lesson-69)、[72 自訂 CLI 指令庫：程式審查、測試計畫與文件同步](#lesson-72)。

上一篇課綱：[70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70) · 下一篇課綱：[72 自訂 CLI 指令庫：程式審查、測試計畫與文件同步](#lesson-72) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-72"></a>
### 72｜自訂 CLI 指令庫：程式審查、測試計畫與文件同步

預定 slug：`gemini-cli-custom-command-library`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 70 分鐘。

**學完成果：** 建立三個可重用、可測試的 TOML 指令。

**先修：** [40 自訂斜線指令：TOML、參數與重新載入](https://mokaair.com/zh-TW/life/gemini-cli-custom-commands)、[70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 定義 review、test-plan、docs-sync 三種輸入與輸出契約。
2. 撰寫命名清楚的 TOML 並處理參數及檔案引用。
3. 在乾淨專案載入後測試空參數、空格與中文路徑。
4. 區分純讀取與會執行 shell 的命令，整理版本與使用說明。

**練習包：** commands/review.toml、test-plan.toml、docs-sync.toml、cases.md。

**通過條件：** 三個命令均能載入且輸出符合契約；跨平台差異有對應範例。

**故障練習：** 含引號或 shell 特殊字元的參數不能被不安全地串接成命令。

**官方查證起點：** [自訂斜線指令](https://geminicli.com/docs/cli/custom-commands/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [40 自訂斜線指令：TOML、參數與重新載入](https://mokaair.com/zh-TW/life/gemini-cli-custom-commands)、[70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70)、[73 把 SKILL.md 打包成 Extension：安裝、更新與回退](#lesson-73)。

上一篇課綱：[71 settings.json 設定除錯：來源優先順序與升級前後比較](#lesson-71) · 下一篇課綱：[73 把 SKILL.md 打包成 Extension：安裝、更新與回退](#lesson-73) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-73"></a>
### 73｜把 SKILL.md 打包成 Extension：安裝、更新與回退

預定 slug：`gemini-cli-skill-extension-package`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 90 分鐘。

**學完成果：** 將文件檢查技能打包成可安裝的本機擴充套件。

**先修：** [41 MCP 與 Extensions：安裝、驗證與停用](https://mokaair.com/zh-TW/life/gemini-cli-mcp-extensions)、[42 Agent Skills：建立可重用的 SKILL.md](https://mokaair.com/zh-TW/life/gemini-cli-agent-skills)、[72 自訂 CLI 指令庫：程式審查、測試計畫與文件同步](#lesson-72)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 設計一個明確的文件檢查技能及所需資源。
2. 依官方格式加入 SKILL.md、腳本與擴充 manifest。
3. 從隔離目錄安裝、確認啟用並執行範例。
4. 測試升級、停用、卸載與回到前版的流程。

**練習包：** doc-check-extension/、CHANGELOG.md、安裝與回退操作表。

**通過條件：** 乾淨環境可安裝，停用後能力消失；重裝或回退結果可驗證。

**故障練習：** 技能與一般 GEMINI.md 指示用途不同；腳本失敗要能被看見而非只回報成功。

**官方查證起點：** [建立 CLI Extensions](https://geminicli.com/docs/extensions/writing-extensions/)、[Agent Skills](https://geminicli.com/docs/cli/skills/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [42 Agent Skills：建立可重用的 SKILL.md](https://mokaair.com/zh-TW/life/gemini-cli-agent-skills)、[72 自訂 CLI 指令庫：程式審查、測試計畫與文件同步](#lesson-72)、[74 大型專案的 CLI 上下文：分段任務、Git 差異與恢復](#lesson-74)。

上一篇課綱：[72 自訂 CLI 指令庫：程式審查、測試計畫與文件同步](#lesson-72) · 下一篇課綱：[74 大型專案的 CLI 上下文：分段任務、Git 差異與恢復](#lesson-74) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-74"></a>
### 74｜大型專案的 CLI 上下文：分段任務、Git 差異與恢復

預定 slug：`gemini-cli-large-project-context`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 80 分鐘。

**學完成果：** 在含多個模組的專案只修改指定範圍並保存恢復點。

**先修：** [33 CLI 對話管理：恢復、壓縮與匯出](https://mokaair.com/zh-TW/life/gemini-cli-sessions-context)、[34 CLI 寫程式：理解、規劃、修改與測試](https://mokaair.com/zh-TW/life/gemini-cli-coding-workflow)、[39 CLI 權限：忽略檔案、可信任資料夾與沙箱](https://mokaair.com/zh-TW/life/gemini-cli-permissions-sandbox)、[70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 先以檔案清單與依賴圖確認本次修改範圍。
2. 明確選擇所需上下文並切分調查與修改。
3. 查看 Git 差異、測試與未提交變更，避免覆蓋既有工作。
4. 中斷再恢復，對照對話狀態與檔案狀態差異。

**練習包：** sample-repo/、task-scope.md、resume-log.md。

**通過條件：** 指定模組完成修改，其他檔案差異可解釋；恢復後能辨識已做與未做工作。

**故障練習：** 對話恢復不等於檔案回滾；不要把 .geminiignore 當成安全存取邊界。

**官方查證起點：** [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/)、[CLI 工作階段與歷史](https://geminicli.com/docs/cli/tutorials/session-management/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [39 CLI 權限：忽略檔案、可信任資料夾與沙箱](https://mokaair.com/zh-TW/life/gemini-cli-permissions-sandbox)、[70 GEMINI.md 團隊範本：拆分規則、匯入與維護責任](#lesson-70)、[73 把 SKILL.md 打包成 Extension：安裝、更新與回退](#lesson-73)。

上一篇課綱：[73 把 SKILL.md 打包成 Extension：安裝、更新與回退](#lesson-73) · 下一篇課綱：[75 MCP 實作：建立本機唯讀商品查詢工具並排除連線問題](#lesson-75) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-75"></a>
### 75｜MCP 實作：建立本機唯讀商品查詢工具並排除連線問題

預定 slug：`gemini-cli-mcp-server-workshop`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 90 分鐘。

**學完成果：** 讓 Gemini CLI 能查詢受範圍限制的合成商品資料。

**先修：** [41 MCP 與 Extensions：安裝、驗證與停用](https://mokaair.com/zh-TW/life/gemini-cli-mcp-extensions)、[30 CLI 認證：Google 帳號、API Key 與計費](https://mokaair.com/zh-TW/life/gemini-cli-authentication)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 依官方 MCP SDK 建立唯讀查詢工具與資料結構。
2. 以合成 CSV 作資料來源並限制可查範圍。
3. 設定 Gemini CLI，確認工具探索與正確參數。
4. 逐一測試啟動失敗、逾時、空結果與移除工具。

**練習包：** local-catalog-mcp/、products.csv、connection-cases.md。

**通過條件：** 正確、不存在、無效參數三類查詢均有工具紀錄；停用後不可再查。

**故障練習：** 工具不得把參數當檔案路徑任意讀取；回傳文字不能被當成新的高權限指示。

**官方查證起點：** [CLI MCP 伺服器](https://geminicli.com/docs/tools/mcp-server/)、[MCP 官方 Python SDK](https://github.com/modelcontextprotocol/python-sdk)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [41 MCP 與 Extensions：安裝、驗證與停用](https://mokaair.com/zh-TW/life/gemini-cli-mcp-extensions)、[30 CLI 認證：Google 帳號、API Key 與計費](https://mokaair.com/zh-TW/life/gemini-cli-authentication)、[76 Hooks 品質檢查：事件輸入、退出碼與失敗時停止](#lesson-76)。

上一篇課綱：[74 大型專案的 CLI 上下文：分段任務、Git 差異與恢復](#lesson-74) · 下一篇課綱：[76 Hooks 品質檢查：事件輸入、退出碼與失敗時停止](#lesson-76) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-76"></a>
### 76｜Hooks 品質檢查：事件輸入、退出碼與失敗時停止

預定 slug：`gemini-cli-hooks-quality-gates`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 80 分鐘。

**學完成果：** 做出可觀察且確實會阻擋指定操作的檢查。

**先修：** [43 Hooks：在指定事件執行檢查](https://mokaair.com/zh-TW/life/gemini-cli-hooks)、[71 settings.json 設定除錯：來源優先順序與升級前後比較](#lesson-71)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 選一個官方可阻擋事件並建立最小 hook。
2. 處理 stdin JSON、stdout 回應及 stderr 診斷。
3. 加入 lint 檢查與可控的通過、拒絕案例。
4. 測試格式損壞、逾時與停用行為，記錄是否 fail-open 或 fail-closed。

**練習包：** hooks/quality-check.py、event-fixtures/、expected-decisions.json。

**通過條件：** 每個案例的 CLI 行為與事件規格一致，拒絕有可理解原因。

**故障練習：** 不能把一般 shell 非零退出碼想當然視為阻擋；須逐事件驗證實際語意。

**官方查證起點：** [CLI Hooks](https://geminicli.com/docs/hooks/)、[CLI Hooks 事件規格](https://geminicli.com/docs/hooks/reference/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [43 Hooks：在指定事件執行檢查](https://mokaair.com/zh-TW/life/gemini-cli-hooks)、[71 settings.json 設定除錯：來源優先順序與升級前後比較](#lesson-71)、[77 Subagents 審查工作流：任務契約、工具限制與結果整合](#lesson-77)。

上一篇課綱：[75 MCP 實作：建立本機唯讀商品查詢工具並排除連線問題](#lesson-75) · 下一篇課綱：[77 Subagents 審查工作流：任務契約、工具限制與結果整合](#lesson-77) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-77"></a>
### 77｜Subagents 審查工作流：任務契約、工具限制與結果整合

預定 slug：`gemini-cli-subagent-review-workflow`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 80 分鐘。

**學完成果：** 以兩個專門審查代理完成有證據的程式與文件檢查。

**先修：** [44 Subagents：拆分任務與整合結果](https://mokaair.com/zh-TW/life/gemini-cli-subagents)、[74 大型專案的 CLI 上下文：分段任務、Git 差異與恢復](#lesson-74)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 定義程式與文件兩種審查輸入、輸出格式及工具範圍。
2. 配置子代理並先以固定範例分別執行。
3. 保存各自結果，主代理逐條核對檔案與行號。
4. 處理相反建議、失敗與重複問題，彙整人工可審查清單。

**練習包：** agents/、review-contract.md、兩份原始回報與合併報告。

**通過條件：** 每個採納問題都可定位，重複合併且不採納無依據建議；實際並行與否明示。

**故障練習：** 不假設代理必定並行或自動隔離寫入；無法確保唯讀時使用可丟棄副本。

**官方查證起點：** [CLI Subagents](https://geminicli.com/docs/core/subagents/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [44 Subagents：拆分任務與整合結果](https://mokaair.com/zh-TW/life/gemini-cli-subagents)、[74 大型專案的 CLI 上下文：分段任務、Git 差異與恢復](#lesson-74)、[78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78)。

上一篇課綱：[76 Hooks 品質檢查：事件輸入、退出碼與失敗時停止](#lesson-76) · 下一篇課綱：[78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-78"></a>
### 78｜Headless 批次處理：JSONL、續跑與避免重複輸出

預定 slug：`gemini-cli-resumable-batch-pipeline`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 90 分鐘。

**學完成果：** 讓 20 份文件批次整理可中斷、續跑與追查失敗。

**先修：** [45 Headless 模式：批次、JSON 與腳本](https://mokaair.com/zh-TW/life/gemini-cli-headless-automation)、[49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 建立文件 ID、內容雜湊及處理狀態清單。
2. 以 headless 執行並分開解析結果、事件與錯誤。
3. 由自行撰寫的腳本保存檢查點，限制並行與重試。
4. 中途停止、重啟及修改一份輸入，核對是否重做正確項目。

**練習包：** batch-runner/、20 份合成文件、manifest.jsonl、run-report.csv。

**通過條件：** 中斷重跑不重複寫成品，修改一份只重做對應輸入；失敗保留原因。

**故障練習：** stream-json 的工具事件或局部文字不是最終成功；CLI 退出成功也需驗證輸出契約。

**官方查證起點：** [Headless 模式](https://geminicli.com/docs/cli/headless/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [45 Headless 模式：批次、JSON 與腳本](https://mokaair.com/zh-TW/life/gemini-cli-headless-automation)、[49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)、[79 Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告](#lesson-79)。

上一篇課綱：[77 Subagents 審查工作流：任務契約、工具限制與結果整合](#lesson-77) · 下一篇課綱：[79 Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告](#lesson-79) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-79"></a>
### 79｜Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告

預定 slug：`gemini-cli-github-actions-artifacts`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 90 分鐘。

**學完成果：** 在測試 repository 手動執行工作流並保存可下載的審查報告。

**先修：** [39 CLI 權限：忽略檔案、可信任資料夾與沙箱](https://mokaair.com/zh-TW/life/gemini-cli-permissions-sandbox)、[78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78)。

**開始前條件：** 使用獨立測試 repository；依可用認證方式驗證 GitHub Actions、用量與權限，第三方 Action 釘選完整 commit SHA。發文、合併與部署不屬於此練習。

1. 建立 workflow_dispatch 與受限的檔案輸入範圍。
2. 固定 CLI 版本、最小權限及秘密金鑰使用方式。
3. 執行 headless，把報告保存為 artifact。
4. 檢查逾時、失敗與無憑證情境，避免非受信任程式拿到金鑰。

**練習包：** workflow.yml、sample-change.diff、report-contract.json。

**通過條件：** 手動觸發可取回報告，workflow 權限與用量可查；不自動合併、部署或留言。

**故障練習：** fork 或不受信任內容不能取得秘密；未核對 API 用量前不啟用無限制自動觸發。

**官方查證起點：** [Headless 模式](https://geminicli.com/docs/cli/headless/)、[Google 官方 run-gemini-cli Action](https://github.com/google-github-actions/run-gemini-cli)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [39 CLI 權限：忽略檔案、可信任資料夾與沙箱](https://mokaair.com/zh-TW/life/gemini-cli-permissions-sandbox)、[78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78)、[80 CLI 完整專案：文件更新、連結檢查與人工審查交付](#lesson-80)。

上一篇課綱：[78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78) · 下一篇課綱：[80 CLI 完整專案：文件更新、連結檢查與人工審查交付](#lesson-80) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-80"></a>
### 80｜CLI 完整專案：文件更新、連結檢查與人工審查交付

預定 slug：`gemini-cli-docs-maintenance-project`。進階／Windows、macOS、Linux；閱讀暫估 8 分鐘，動手約 120 分鐘。

**學完成果：** 將文件維護整合成能產出差異、報告及失敗記錄的流程。

**先修：** [72 自訂 CLI 指令庫：程式審查、測試計畫與文件同步](#lesson-72)、[76 Hooks 品質檢查：事件輸入、退出碼與失敗時停止](#lesson-76)、[78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78)。

**開始前條件：** 第一階段 CLI 0.59.0 是既有基準；第二階段重新選定並鎖定版本。PowerShell、macOS、Linux 逐平台標示實測／文件整理；JSON、TOML、路徑與退出碼要實際驗證。

1. 建立十篇互連 Markdown 文件與故意損壞的連結。
2. 以自訂指令提出修訂，再檢查 Markdown 與連結。
3. 使用 headless 執行並保留每篇輸入、輸出與檢查結果。
4. 輸出差異與交接說明，人工確認後才套用。

**練習包：** docs-maintenance-project/、fixtures/、report.md、變更前後對照。

**通過條件：** 已知斷鏈可找到，修改符合範圍，重跑可分辨未變更與需處理文件。

**故障練習：** 測試不過或資料不存在時停止產出可發布標記，不讓模型憑空建立來源網址。

**官方查證起點：** [自訂斜線指令](https://geminicli.com/docs/cli/custom-commands/)、[CLI Hooks](https://geminicli.com/docs/hooks/)、[Headless 模式](https://geminicli.com/docs/cli/headless/)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [76 Hooks 品質檢查：事件輸入、退出碼與失敗時停止](#lesson-76)、[78 Headless 批次處理：JSONL、續跑與避免重複輸出](#lesson-78)、[79 Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告](#lesson-79)。

上一篇課綱：[79 Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告](#lesson-79) · 下一篇課綱：[81 Function calling 實作：參數驗證、工具回傳與有限次迴圈](#lesson-81) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-81"></a>
### 81｜Function calling 實作：參數驗證、工具回傳與有限次迴圈

預定 slug：`gemini-api-function-calling-workshop`。進階／Windows、macOS、Linux、Python；閱讀暫估 8 分鐘，動手約 90 分鐘。

**學完成果：** 用 Python 建立只查詢合成訂單的工具呼叫流程。

**先修：** [47 AI Studio 與第一個 Gemini API 呼叫](https://mokaair.com/zh-TW/life/gemini-api-ai-studio-first-call)、[48 API 檔案與 JSON：結構化輸出及驗證](https://mokaair.com/zh-TW/life/gemini-api-files-structured-output)、[49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)。

**開始前條件：** Python 為主；按寫作日鎖定 SDK、模型與 API 家族，金鑰只在後端。先用 fixture 驗證，再於可用帳號和明確成本上限下做最小真實呼叫；未做的步驟不得寫成實測。

1. 定義查詢工具 schema 與允許的訂單 ID。
2. 接收工具要求後自行驗證參數並執行本機函式。
3. 把工具結果送回同一 API 家族的後續請求。
4. 設定迴圈上限、逾時與查無訂單的回覆。

**練習包：** function-loop/、orders.json、tool-cases.json。

**通過條件：** 正常、查無資料、非法參數與迴圈達上限皆有可判斷的結果。

**故障練習：** 模型提出工具要求不等於已執行；不允許任意函式名稱或自動重複具副作用操作。

**官方查證起點：** [Function calling](https://ai.google.dev/gemini-api/docs/function-calling)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [48 API 檔案與 JSON：結構化輸出及驗證](https://mokaair.com/zh-TW/life/gemini-api-files-structured-output)、[49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)、[82 Gemini API 搜尋引用：Grounding 結果解析與來源呈現](#lesson-82)。

上一篇課綱：[80 CLI 完整專案：文件更新、連結檢查與人工審查交付](#lesson-80) · 下一篇課綱：[82 Gemini API 搜尋引用：Grounding 結果解析與來源呈現](#lesson-82) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-82"></a>
### 82｜Gemini API 搜尋引用：Grounding 結果解析與來源呈現

預定 slug：`gemini-api-search-grounding-citations`。進階／Windows、macOS、Linux、Python；閱讀暫估 8 分鐘，動手約 80 分鐘。

**學完成果：** 讓應用程式回傳有來源對應的公開資訊摘要。

**先修：** [47 AI Studio 與第一個 Gemini API 呼叫](https://mokaair.com/zh-TW/life/gemini-api-ai-studio-first-call)、[48 API 檔案與 JSON：結構化輸出及驗證](https://mokaair.com/zh-TW/life/gemini-api-files-structured-output)。

**開始前條件：** Python 為主；按寫作日鎖定 SDK、模型與 API 家族，金鑰只在後端。先用 fixture 驗證，再於可用帳號和明確成本上限下做最小真實呼叫；未做的步驟不得寫成實測。

1. 選可重做的官方網站問題並確認模型與工具支援。
2. 發出 Google Search grounding 請求並保存回應。
3. 解析引用與支援片段，依官方要求呈現搜尋相關內容。
4. 測試沒有引用、來源失效及模型未啟動搜尋的結果。

**練習包：** grounding-demo/、response-fixtures/、citation-view.html。

**通過條件：** 摘要中的引用能對到回應來源；缺引用時明示不能追查，不捏造 URL。

**故障練習：** 搜尋有回應不代表每個結論正確，須逐一核對支援片段並防止不安全連結。

**官方查證起點：** [Google Search grounding](https://ai.google.dev/gemini-api/docs/google-search)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [47 AI Studio 與第一個 Gemini API 呼叫](https://mokaair.com/zh-TW/life/gemini-api-ai-studio-first-call)、[48 API 檔案與 JSON：結構化輸出及驗證](https://mokaair.com/zh-TW/life/gemini-api-files-structured-output)、[83 File Search 知識庫實作：匯入、查詢、更新與刪除驗證](#lesson-83)。

上一篇課綱：[81 Function calling 實作：參數驗證、工具回傳與有限次迴圈](#lesson-81) · 下一篇課綱：[83 File Search 知識庫實作：匯入、查詢、更新與刪除驗證](#lesson-83) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-83"></a>
### 83｜File Search 知識庫實作：匯入、查詢、更新與刪除驗證

預定 slug：`gemini-api-file-search-rag-project`。進階／Windows、macOS、Linux、Python；閱讀暫估 8 分鐘，動手約 100 分鐘。

**學完成果：** 以十份合成規格文件建立有引用的檢索問答。

**先修：** [48 API 檔案與 JSON：結構化輸出及驗證](https://mokaair.com/zh-TW/life/gemini-api-files-structured-output)、[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)。

**開始前條件：** Python 為主；按寫作日鎖定 SDK、模型與 API 家族，金鑰只在後端。先用 fixture 驗證，再於可用帳號和明確成本上限下做最小真實呼叫；未做的步驟不得寫成實測。

1. 建立 File Search store 並記錄原始檔與索引文件 ID。
2. 上傳、等待匯入完成，建立可查詢狀態。
3. 查詢後逐項核對引用與來源版本。
4. 更新及刪除一份資料，驗證查詢與資源生命週期。

**練習包：** file-search-demo/、10 份規格書、resource-ledger.json、citation-cases.json。

**通過條件：** 匯入完成後可追到正確來源，更新與刪除步驟均可查證且能清理測試資源。

**故障練習：** 查無證據不補造答案；File Search 與 Google Search 分次呼叫，不假設能同請求混用。

**官方查證起點：** [File Search](https://ai.google.dev/gemini-api/docs/file-search)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [48 API 檔案與 JSON：結構化輸出及驗證](https://mokaair.com/zh-TW/life/gemini-api-files-structured-output)、[58 NotebookLM 引用查核：矛盾資料、缺證據與未知答案](#lesson-58)、[84 API 快取實驗：隱含快取、手動快取與實際成本核對](#lesson-84)。

上一篇課綱：[82 Gemini API 搜尋引用：Grounding 結果解析與來源呈現](#lesson-82) · 下一篇課綱：[84 API 快取實驗：隱含快取、手動快取與實際成本核對](#lesson-84) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-84"></a>
### 84｜API 快取實驗：隱含快取、手動快取與實際成本核對

預定 slug：`gemini-api-context-cache-experiment`。進階／Windows、macOS、Linux、Python；閱讀暫估 8 分鐘，動手約 80 分鐘。

**學完成果：** 比較重複文件請求的使用量，理解快取是否真的有幫助。

**先修：** [47 AI Studio 與第一個 Gemini API 呼叫](https://mokaair.com/zh-TW/life/gemini-api-ai-studio-first-call)、[49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)。

**開始前條件：** Python 為主；按寫作日鎖定 SDK、模型與 API 家族，金鑰只在後端。先用 fixture 驗證，再於可用帳號和明確成本上限下做最小真實呼叫；未做的步驟不得寫成實測。

1. 先區分 Interactions 與 generateContent 的快取支援。
2. 固定模型、文件版本與一組重複問題建立未快取基準。
3. 分別量測隱含快取；手動快取另用 generateContent 範例。
4. 核對用量、保存時間與過期行為，清理測試快取。

**練習包：** cache-lab/implicit/、explicit/、usage-log.csv、文件版本雜湊。

**通過條件：** 兩種 API 路徑各自可執行，實際用量有來源；未命中也如實保存。

**故障練習：** 短輸入不保證命中或省錢；不把手動快取建立語法放進 Interactions 範例。

**官方查證起點：** [Context caching](https://ai.google.dev/gemini-api/docs/caching)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [47 AI Studio 與第一個 Gemini API 呼叫](https://mokaair.com/zh-TW/life/gemini-api-ai-studio-first-call)、[49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)、[85 Batch API 批次評測：工作 ID、部分失敗與重送管理](#lesson-85)。

上一篇課綱：[83 File Search 知識庫實作：匯入、查詢、更新與刪除驗證](#lesson-83) · 下一篇課綱：[85 Batch API 批次評測：工作 ID、部分失敗與重送管理](#lesson-85) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-85"></a>
### 85｜Batch API 批次評測：工作 ID、部分失敗與重送管理

預定 slug：`gemini-api-batch-recovery`。進階／Windows、macOS、Linux、Python；閱讀暫估 8 分鐘，動手約 100 分鐘。批次工作可能跨日完成；等待時間不計入 100 分鐘操作估計，不能保證即時回傳。

**學完成果：** 對固定題庫建立可追蹤、可收斂的離線批次評測。

**先修：** [48 API 檔案與 JSON：結構化輸出及驗證](https://mokaair.com/zh-TW/life/gemini-api-files-structured-output)、[49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)、[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)。

**開始前條件：** Python 為主；按寫作日鎖定 SDK、模型與 API 家族，金鑰只在後端。先用 fixture 驗證，再於可用帳號和明確成本上限下做最小真實呼叫；未做的步驟不得寫成實測。

1. 以 generateContent 相容請求建立 20 題 JSONL 與固定 key。
2. 提交一次後立即保存 job ID，觀察工作狀態。
3. 下載每項結果，將成功、失敗與缺漏分開。
4. 只重送核對後仍需執行的項目，彙總品質與成本。

**練習包：** batch-eval/、cases.jsonl、job-ledger.json、evaluation.csv。

**通過條件：** 每個 key 只有一個採納結果；部分失敗與重送對照清楚，成本可查。

**故障練習：** 建立 Batch 並非冪等；網路逾時後先核對工作，不能盲目再送整批。

**官方查證起點：** [Batch API](https://ai.google.dev/gemini-api/docs/batch-api)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)、[51 提示詞改寫實驗：用固定題庫找出有效的修改](#lesson-51)、[86 文件助手進階專案：有引用的問答服務、評測與交接](#lesson-86)。

上一篇課綱：[84 API 快取實驗：隱含快取、手動快取與實際成本核對](#lesson-84) · 下一篇課綱：[86 文件助手進階專案：有引用的問答服務、評測與交接](#lesson-86) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="lesson-86"></a>
### 86｜文件助手進階專案：有引用的問答服務、評測與交接

預定 slug：`gemini-api-document-service-capstone`。進階／Windows、macOS、Linux、Python；閱讀暫估 8 分鐘，動手約 120 分鐘。

**學完成果：** 完成可本機使用、有來源引用與測試資料的文件問答服務。

**先修：** [50 完整實作：文件摘要與資料擷取工具](https://mokaair.com/zh-TW/life/gemini-api-document-assistant)、[81 Function calling 實作：參數驗證、工具回傳與有限次迴圈](#lesson-81)、[83 File Search 知識庫實作：匯入、查詢、更新與刪除驗證](#lesson-83)、[85 Batch API 批次評測：工作 ID、部分失敗與重送管理](#lesson-85)。

**開始前條件：** Python 為主；按寫作日鎖定 SDK、模型與 API 家族，金鑰只在後端。先用 fixture 驗證，再於可用帳號和明確成本上限下做最小真實呼叫；未做的步驟不得寫成實測。

1. 以十份合成文件定義單一使用者服務的功能與限制。
2. 建立後端金鑰管理、文件索引及受限工具查詢。
3. 以 20 題評測資料檢查正確、缺證據與不合法輸入。
4. 加入資源清理、錯誤紀錄及啟動文件，交給他人重做。

**練習包：** document-service/、.env.example、golden-cases.json、README.md；Python 為主。

**通過條件：** 全新環境能啟動，瀏覽器收不到 API Key，引用與錯誤路徑均可核對。

**故障練習：** 資料中夾帶指示不能改變工具權限；本機單人範例不宣稱已具多租戶或公開上線能力。

**官方查證起點：** [File Search](https://ai.google.dev/gemini-api/docs/file-search)、[Function calling](https://ai.google.dev/gemini-api/docs/function-calling)、[Batch API](https://ai.google.dev/gemini-api/docs/batch-api)。本課綱查閱日 2026-09-14，正式寫作與發布前重查。

**接著閱讀：** [83 File Search 知識庫實作：匯入、查詢、更新與刪除驗證](#lesson-83)、[85 Batch API 批次評測：工作 ID、部分失敗與重送管理](#lesson-85)、[49 API 額度與錯誤：費用、重試與成本控制](https://mokaair.com/zh-TW/life/gemini-api-cost-errors-guide)。

上一篇課綱：[85 Batch API 批次評測：工作 ID、部分失敗與重送管理](#lesson-85) · [返回本課綱目錄](#catalogue) · [返回已上線 Gemini 總目錄](https://mokaair.com/zh-TW/life/gemini-guide)

<a id="sources"></a>
## 官方來源與功能邊界

完整查閱紀錄在 [sources.json](sources.json)，共 34 個官方來源。課程的題庫、資料集、評分表、去重帳本與交付流程是教學設計，不宣稱產品內建這些機制。

| 需特別區分 | 對課綱的影響 | 官方依據 |
| --- | --- | --- |
| Gemini Notebook 與 Gemini | 57–62 分開檢查引用範圍與 Studio 入口；搜尋別名保留 NotebookLM、Gemini Notebook。 | [Gemini 與 Gemini Notebook 的整合差異](https://support.google.com/gemininotebook/answer/17003757) |
| GEMINI.md、SKILL.md、Gems | 69–73 的本機規則／技能不假設會被網頁 Gems 讀取。 | [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/)、[Agent Skills](https://geminicli.com/docs/cli/skills/)、[Gems 使用方式](https://support.google.com/gemini/answer/15236405?hl=en-GB) |
| Spark 排程與一般排程動作 | 56 依可用性和實際執行紀錄驗收。 | [Gemini Spark](https://support.google.com/gemini/answer/17094507?hl=en) |
| Interactions 與 generateContent | 84 的手動快取、85 的 Batch 使用獨立 generateContent 範例，不混用 SDK 請求欄位。 | [Context caching](https://ai.google.dev/gemini-api/docs/caching)、[Batch API](https://ai.google.dev/gemini-api/docs/batch-api) |
| File Search 與 Google Search | 82、83 分開教學；86 的整合不能假設內建 grounding 工具可同請求混用。 | [File Search](https://ai.google.dev/gemini-api/docs/file-search) |
| 載入、模型行為及工具權限 | 69 驗上下文，76 驗事件結果，77 驗工具範圍，三種證據分開記錄。 | [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/)、[CLI Hooks](https://geminicli.com/docs/hooks/)、[CLI Subagents](https://geminicli.com/docs/core/subagents/) |

完成判斷分成「課綱已定」「原稿與素材完成」「測試完成」「網站發布」「公開瀏覽器驗證」五個狀態。本次只完成第一個狀態。
