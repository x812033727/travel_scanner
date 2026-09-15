# Gemini 深入教學逐篇驗收

本機 36 篇原稿、配圖、練習包與作者證據已核對；仍有 33 篇需要真實帳號、模型或裝置操作。本表列出需要取得的成果，並非已完成實測。

69–71 已有 Windows CLI 0.59.0 實際模組證據；73 另有 Node 22 原生 CLI 安裝、更新與回退紀錄，但模型啟用 Skill 仍待驗。跨系統及另一 CLI 版本未宣稱通過。

| 篇號 | 本機可追查證據 | 待取得的實測成果 | 所需環境 |
| --- | --- | --- | --- |
| 51 | [提示詞改寫實驗：用固定題庫找出有效的修改](../content/work/51/lesson.md)；[作者紀錄](../content/work/verification/authoring-review.json) | 20 次 Gemini 實際輸出、相同題庫的改寫前後人工評分 | 可登入 Gemini／Gems／Canvas／Workspace；55 另需 Android 與 iPhone；56 需 Spark 資格與排程等待 |
| 52 | [Gems 客服知識助手：資料更新、拒答與回歸測試](../content/work/52/lesson.md)；[作者紀錄](../content/work/verification/authoring-review.json) | Gems v1/v2 各 12 題實際輸出、資料更新與重新開啟後狀態 | 可登入 Gemini／Gems／Canvas／Workspace；55 另需 Android 與 iPhone；56 需 Spark 資格與排程等待 |
| 53 | [Canvas 實作活動預算計算器：需求、除錯與驗收](../content/work/53/lesson.md)；[作者紀錄](../content/work/verification/authoring-review.json) | Canvas 真正產生的預算工具、錯誤版本與修正後驗收 | 可登入 Gemini／Gems／Canvas／Workspace；55 另需 Android 與 iPhone；56 需 Spark 資格與排程等待 |
| 54 | [Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦](../content/work/54/lesson.md)；[作者紀錄](../content/work/verification/authoring-review.json) | Gmail 來源到 Docs／Sheets 的實際流程與權限核對 | 可登入 Gemini／Gems／Canvas／Workspace；55 另需 Android 與 iPhone；56 需 Spark 資格與排程等待 |
| 55 | [手機現場筆記：Gemini Live、照片與回到電腦整理](../content/work/55/lesson.md)；[作者紀錄](../content/work/verification/authoring-review.json) | Android 與 iPhone Live、鏡頭停止、照片及電腦交接紀錄 | 可登入 Gemini／Gems／Canvas／Workspace；55 另需 Android 與 iPhone；56 需 Spark 資格與排程等待 |
| 56 | [Spark 每週資訊摘要：設定排程、檢查結果與停止任務](../content/work/56/lesson.md)；[作者紀錄](../content/work/verification/authoring-review.json) | Spark 手動與真正排程結果，暫停／恢復／刪除及下一次執行時間觀察 | 可登入 Gemini／Gems／Canvas／Workspace；55 另需 Android 與 iPhone；56 需 Spark 資格與排程等待 |
| 57 | [NotebookLM 資料版本管理：來源清單、更新與過期內容](../content/research/57/lesson.md)；[作者紀錄](../content/research/verification/authoring-review.json) | Drive 同步、上傳來源替換與版本差異紀錄 | 可登入 NotebookLM／Drive／Deep Research；61 需媒體產生額度 |
| 58 | [NotebookLM 引用查核：矛盾資料、缺證據與未知答案](../content/research/58/lesson.md)；[作者紀錄](../content/research/verification/authoring-review.json) | 實際問答、逐一點開引用、矛盾與缺證據案例 | 可登入 NotebookLM／Drive／Deep Research；61 需媒體產生額度 |
| 59 | [NotebookLM 備考實作：題庫、錯題分類與間隔複習](../content/research/59/lesson.md)；[作者紀錄](../content/research/verification/authoring-review.json) | Studio 測驗、學習者重測與錯題分類紀錄 | 可登入 NotebookLM／Drive／Deep Research；61 需媒體產生額度 |
| 60 | [NotebookLM 比較多篇研究：研究問題、方法與限制矩陣](../content/research/60/lesson.md)；[作者紀錄](../content/research/verification/authoring-review.json) | 實際多篇論文比較矩陣及原文回查 | 可登入 NotebookLM／Drive／Deep Research；61 需媒體產生額度 |
| 61 | [NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查](../content/research/61/lesson.md)；[作者紀錄](../content/research/verification/authoring-review.json) | 真正生成的講義、語音、影片摘要及 30 項一致性觀察 | 可登入 NotebookLM／Drive／Deep Research；61 需媒體產生額度 |
| 62 | [Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告](../content/research/62/lesson.md)；[作者紀錄](../content/research/verification/authoring-review.json) | Deep Research 計畫與報告、NotebookLM 引用及更新紀錄 | 可登入 NotebookLM／Drive／Deep Research；61 需媒體產生額度 |
| 63 | [Gemini 圖片系列製作：參考圖、風格規格與一致性評分](../content/creative/63/lesson.md)；[作者紀錄](../content/creative/verification/authoring-review.json) | 3 張實際 Gemini 系列圖、3 個失敗結果與一致性評分 | 可登入 Gemini／Flow／Sheets；需圖片與影片額度 |
| 64 | [Gemini 修圖除錯：局部修改、文字錯誤與多輪退化](../content/creative/64/lesson.md)；[作者紀錄](../content/creative/verification/authoring-review.json) | Gemini 多輪修圖的每一版輸入、成品與退化核對 | 可登入 Gemini／Flow／Sheets；需圖片與影片額度 |
| 65 | [Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成](../content/creative/65/lesson.md)；[作者紀錄](../content/creative/verification/authoring-review.json) | Flow 三段實際影片、組合成片與逐鏡驗收 | 可登入 Gemini／Flow／Sheets；需圖片與影片額度 |
| 66 | [Google Flow 畫面連貫：起訖影格、參考素材與轉場修正](../content/creative/66/lesson.md)；[作者紀錄](../content/creative/verification/authoring-review.json) | 原版與修正版連貫影片、起訖影格及比較紀錄 | 可登入 Gemini／Flow／Sheets；需圖片與影片額度 |
| 67 | [Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表](../content/creative/67/lesson.md)；[作者紀錄](../content/creative/verification/authoring-review.json) | Google Sheets 匯入與 Gemini 實際資料整理、公式核對 | 可登入 Gemini／Flow／Sheets；需圖片與影片額度 |
| 68 | [Gemini 內容專案交付：文章、圖片與短片的版本和素材清單](../content/creative/68/lesson.md)；[作者紀錄](../content/creative/verification/authoring-review.json) | 實際文章、3 張圖片、短片、更新日期素材與完整交付清單 | 可登入 Gemini／Flow／Sheets；需圖片與影片額度 |
| 69 | [GEMINI.md 載入實驗：親手驗證全域、專案與子目錄規則](../content/md/69/lesson.md)；[作者紀錄](../content/md/verification/authoring-review.json) | 既有 Windows 0.59.0 載入／重新載入／範圍模組證據已具備；如新增系統聲明需補測 | Windows、指定 CLI 0.59.0；72–74 需可用 CLI 認證 |
| 70 | [GEMINI.md 團隊範本：拆分規則、匯入與維護責任](../content/md/70/lesson.md)；[作者紀錄](../content/md/verification/authoring-review.json) | 既有 Windows 0.59.0 規則匯入與維護檢查已具備；如新增系統聲明需補測 | Windows、指定 CLI 0.59.0；72–74 需可用 CLI 認證 |
| 71 | [settings.json 設定除錯：來源優先順序與升級前後比較](../content/md/71/lesson.md)；[作者紀錄](../content/md/verification/authoring-review.json) | 既有 Windows 0.59.0 設定優先序證據已具備；尚未聲稱另一 CLI 版本通過 | Windows、指定 CLI 0.59.0；72–74 需可用 CLI 認證 |
| 72 | [自訂 CLI 指令庫：程式審查、測試計畫與文件同步](../content/md/72/lesson.md)；[作者紀錄](../content/md/verification/authoring-review.json) | 三個自訂指令的實際模型回覆、參數與錯誤路徑 | Windows、指定 CLI 0.59.0；72–74 需可用 CLI 認證 |
| 73 | [把 SKILL.md 打包成 Extension：安裝、更新與回退](../content/md/73/lesson.md)；[作者紀錄](../content/md/verification/authoring-review.json) | 模型真的啟用 Skill 的紀錄；原生 CLI 安裝／更新／回退已在 Node 22 驗證 | Windows、指定 CLI 0.59.0；72–74 需可用 CLI 認證 |
| 74 | [大型專案的 CLI 上下文：分段任務、Git 差異與恢復](../content/md/74/lesson.md)；[作者紀錄](../content/md/verification/authoring-review.json) | 已登入 CLI 的跨段對話恢復、上下文與指定修改範圍核對 | Windows、指定 CLI 0.59.0；72–74 需可用 CLI 認證 |
| 75 | [MCP 實作：建立本機唯讀商品查詢工具並排除連線問題](../content/automation/75/lesson.md)；[作者紀錄](../content/automation/verification/authoring-review.json) | 實際 CLI 工具選擇、/mcp 停用及查詢結果 | 可認證 CLI 0.59.0；79 另需指定測試 repository 與 Actions |
| 76 | [Hooks 品質檢查：事件輸入、退出碼與失敗時停止](../content/automation/76/lesson.md)；[作者紀錄](../content/automation/verification/authoring-review.json) | 實際模型到工具的 Hook 允許／拒絕完整流程 | 可認證 CLI 0.59.0；79 另需指定測試 repository 與 Actions |
| 77 | [Subagents 審查工作流：任務契約、工具限制與結果整合](../content/automation/77/lesson.md)；[作者紀錄](../content/automation/verification/authoring-review.json) | 實際 Subagents 回覆、指派限制及結果整合 | 可認證 CLI 0.59.0；79 另需指定測試 repository 與 Actions |
| 78 | [Headless 批次處理：JSONL、續跑與避免重複輸出](../content/automation/78/lesson.md)；[作者紀錄](../content/automation/verification/authoring-review.json) | 真實模型 Headless 批次、中斷續跑與不重複輸出 | 可認證 CLI 0.59.0；79 另需指定測試 repository 與 Actions |
| 79 | [Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告](../content/automation/79/lesson.md)；[作者紀錄](../content/automation/verification/authoring-review.json) | 指定測試 GitHub repository 的 hosted workflow 執行與可下載 artifact | 可認證 CLI 0.59.0；79 另需指定測試 repository 與 Actions |
| 80 | [CLI 完整專案：文件更新、連結檢查與人工審查交付](../content/automation/80/lesson.md)；[作者紀錄](../content/automation/verification/authoring-review.json) | 實際模型提出文件維護差異、檢查與交付報告 | 可認證 CLI 0.59.0；79 另需指定測試 repository 與 Actions |
| 81 | [Function calling 實作：參數驗證、工具回傳與有限次迴圈](../content/api/81/lesson.md)；[作者紀錄](../content/api/verification/authoring-review.json) | Google API 真實工具呼叫、引數拒絕與有限迴圈結果 | 指定 Google API 測試專案、金鑰環境與費用上限 |
| 82 | [Gemini API 搜尋引用：Grounding 結果解析與來源呈現](../content/api/82/lesson.md)；[作者紀錄](../content/api/verification/authoring-review.json) | Google API 真實 grounding 回應、引用對應及來源可讀性 | 指定 Google API 測試專案、金鑰環境與費用上限 |
| 83 | [File Search 知識庫實作：匯入、查詢、更新與刪除驗證](../content/api/83/lesson.md)；[作者紀錄](../content/api/verification/authoring-review.json) | 10 份文件的真實索引、查詢、更新與刪除確認 | 指定 Google API 測試專案、金鑰環境與費用上限 |
| 84 | [API 快取實驗：隱含快取、手動快取與實際成本核對](../content/api/84/lesson.md)；[作者紀錄](../content/api/verification/authoring-review.json) | 真實快取命中、到期、用量與帳單核對 | 指定 Google API 測試專案、金鑰環境與費用上限 |
| 85 | [Batch API 批次評測：工作 ID、部分失敗與重送管理](../content/api/85/lesson.md)；[作者紀錄](../content/api/verification/authoring-review.json) | 真實 Batch 工作 ID、部分失敗與只重送失敗項目 | 指定 Google API 測試專案、金鑰環境與費用上限 |
| 86 | [文件助手進階專案：有引用的問答服務、評測與交接](../content/api/86/lesson.md)；[作者紀錄](../content/api/verification/authoring-review.json) | 真實 20 題文件問答、引用、評分及服務交接結果 | 指定 Google API 測試專案、金鑰環境與費用上限 |

發布前還要完成：當日台灣價格、候選稿審查與合併、資料庫 dry-run、限定篇章逐篇發布、新舊 86 篇核對後開放目錄，以及公開頁面／sitemap 驗收。

完整機器可讀紀錄：[readiness.json](readiness.json)。
