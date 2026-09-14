# Codex 深入教學製作進度

更新：2026-09-14。有效規格為[總目錄＋60 篇、五語](depth-plan.md)。**60 篇五語深入稿已編譯，總目錄加分篇共 61 個內容包、305 份語言文件。最終預覽驗收仍未完成；沒有 push、PR、匯入、正式發布或部署。**

依使用者「全部完成後再開 PR 部署」指示，完整驗收前不開部分 PR。ready 只表示內容包存在，正式公開狀態由 API 的當前語言發布資料決定。

## 已完成的製作

- 60 個穩定 ID、十單元、三批各 20 篇，保留原 32 個網址；沒有短稿或待寫空篇。
- 55 份四語平行作者模組，加原 5 份代表篇 Markdown；簡中轉換保留程式碼。
- 上下返回目錄、同單元前後篇、相關文章及正文引用。表格／清單／提示框的作者連結另呈現可點擊的結構化引用，舊純文字不解析為 Markdown。
- 目錄包含程度、平台、需求、單元、路線及指令別名搜尋，URL 保存篩選條件。
- 待辦網站 start／broken／expected，CSV、Skills、Git、MCP、JSON 與 CI 的虛構材料及參考檢查。
- 原創圖解、明確標示環境的參考網頁截圖，以及新增五檔 CSV 下載包。

最後一批已補齊子代理品質、平行整合、瀏覽器與圖片、排程、exec、JSON／JSONL、CI、恢復、網站／CSV 實戰、維護、資料安全、用量及排錯索引。

## 本輪檢查

| 項目 | 結果 | 可支持的結論 |
| --- | --- | --- |
| [全系列完整性](evidence/series-integrity.json) | 60 篇／300 份分篇通過 | 每個作者連結保留、目標存在、五語程式碼相同、來源與圖片存在 |
| [內容稽核](evidence/content-audit.json) | 0 錯誤、24 個編輯提示 | 集合頁格式與語言篇幅提示保留，沒有 schema 或圖解錯誤 |
| 作者編譯器 | 9 項通過 | 精確程式碼、巢狀 fence、用途標籤、全批驗證、過期內容、表格／提示框連結保留 |
| API／系列／內容包相容性 | 59 passed／18 skipped | 本機未啟動 PostgreSQL 的案例略過；五語 SQLite 發布／撤回及格式檢查通過 |
| 受影響前端 | 11 個檔案／168 項通過 | 分批 3＋50＋115；含目錄、文章、複製、管理編輯、系列及生活分享 |
| lint／型別／建置 | 通過 | 全站 ESLint；Next.js 16.3.3 正式 build 含 TypeScript，產生 293 靜態路由 |
| API 靜態檢查 | 通過 | Ruff；Mypy guides 12 個來源檔 |
| i18n／工具／任務 | 通過 | 五語 25 命名空間；39 項工具測試；412 個任務檔，其他任務既有警告保留 |
| [來源網址](evidence/source-health.json) | 65 個唯一來源回應通過 | Android 改引 Pixel 官方頁並更新操作文字；Google 的 HEAD 回覆 404、GET 正常，保留兩次回應並核對實際內容。另補 Python subprocess 官方來源；此檢查只證明網址回應 |

首次整批 Vitest 啟動後停滯，確認為本任務程序後中止；三個分批重跑均通過，中止執行不算成功。建置通過不是瀏覽器或發布通過。

## 參考練習證據

| 範圍 | 檢查數 | 證據 |
| --- | --- | --- |
| 工作階段、Plan、模型及交接 | 16 | [session-plan-practice.json](evidence/session-plan-practice.json) |
| Git 保留與還原 | 9 | [git-practice.json](evidence/git-practice.json) |
| Worktree 隔離、占用及清理 | 7 | [worktree-practice.json](evidence/worktree-practice.json) |
| Skills 與故意破壞後恢復 | 6 | [skill-practice.json](evidence/skill-practice.json) |
| MCP 設定、公開服務與文件讀取 | 6 | [mcp-practice.json](evidence/mcp-practice.json) |
| 子代理品質參考 | 6 | [subagent-reference.json](evidence/subagent-reference.json) |
| 平行成果整合、真實受控衝突及 abort | 6 | [integration-practice.json](evidence/integration-practice.json) |
| exec／JSON／CI 資料驗證 | 11 | [exec-reference.json](evidence/exec-reference.json) |
| CSV、維護及路徑 | 7 | [workshop-reference.json](evidence/workshop-reference.json) |

共 74 項參考檢查。Git 操作只在暫存庫，沒有改動網站正式分支；MCP 使用獨立 child-process 設定，真實使用者設定不變；exec 使用模擬程序，CI 的精確 Python 驗證器在本機執行。沒有呼叫付費模型、觸發 GitHub 工作流程、安裝帳號插件、建立排程或子代理。這些結果不證明每個讀者帳號或所有平台都已實測。

CSV 的三項測試能抓到取消覆寫保護，還原後再次全過。維護練習是 3 pass → 新需求 3 pass／3 fail → 6 pass，刻意改錯計數再抓到失敗，最後還原五份檔案與原三項測試。

JSON 包裝器另拒絕布林／浮點退出碼及重複、倒序的回合邊界。Windows 明列獨立版 codex.exe 前提；本機 Python 呼叫 codex --version 成功，版本 0.154.0-alpha.6.2。這只驗證程序啟動，不代表已執行模型工作。

## 語言、圖片與篇幅

五語程式碼逐區塊一致；日文已整理混用的中文術語。繁中操作正文大多約 1,800–3,000 字，表格與程式碼另外計算。ID 58（約 1,743）以完整新測試及兩檔重構為主；59（約 1,661）以虛構文件、來源界線及分享驗收為主；60（約 1,669）是兩次唯讀任務比較，避免填充價格與效能假數字。這三篇仍有輸入、操作、預期、失敗與還原。集合頁短正文由互動課程清單補足。

本輪新增[定向編輯審核](evidence/editorial-review.json)：掃描全系列日文，修正 26 篇的用語，包括函式、全域設定、子代理、跨裝置交接與檔名；依原文區分 API／網路代理（proxy）與 AI 代理（agent）。另外目視核對既有的 6 張 390／1280px 練習圖，補上五語替代文字，並讓圖說尺寸與圖片一致。沒有新增截圖或將圖像檔審核當成新瀏覽器操作。

相對本機提交 d3f28a25，300 份分篇的程式碼、站內外連結目標與來源未變，非日文正文也未變；只更正日文及圖片文字。最終重新編譯後的全系列完整性、9 項 API 內容檢查與 9 項編譯器測試通過，稽核仍為 0 錯誤／24 提示。這輪是定向用語與圖片審核，不能替代全篇五語終審。

390px／1280px 附圖是 Windows Edge 響應式視窗，不是 iPhone／Android 實機。網站與圖片篇使用已存在的參考版畫面，不代表每次生成或最新重構成果。其他平台及產品限制依官方文件標記，代表篇產品操作證據與最後圖文終審仍待完成。

## 共用系統整合

已唯讀確認「規劃 Claude Code 教學目錄」的 PR #485 合併，沒有改動對方 1cff 工作目錄或傳送任務訊息。本機先保存 5f5b0b11，再以 7abe6057 將精確 main 3b8df68c693eb81ccde7793a2f89d71999dbb2c2 合入本分支。這不是本系列合併到 main。

共用 inlines、article 引用、必填 code label、系列 API、導覽及後台已統一；Shell／TOML／CSV 相容。正文撤回／缺語系／讀取失敗時不推測可公開，集合頁 ItemList 只列公開項目。

## 尚未通過的最終關卡

1. 完整瀏覽器驗收未完成。早期 39 篇整頁測試在 572 項後，韓文 IDE 桌面頁等待程式碼區塊逾時；[報告保持 failed](evidence/depth-browser-shared-integration.json)，不當成最新 60 篇全過。
2. 本機 Next 正式預覽啟動被自動核准審查拒絕，回覆 blocked by policy；限制到 127.0.0.1 仍被拒，未提供具體理由。沒有換啟動方式、服務或連接埠繞過拒絕。原 fixture API 是舊快照，最終驗收要在可用環境載入完整資料。
3. 代表篇及圖文終審尚未簽核。需要以最終可見頁面核對 360／390／1280px、五語切換、複製、搜尋分享、前後篇、正文引用及產品介面證據。series-integrity.json 的 previewAccepted 全為 false，最終深入驗收維持 0/60。
4. 全部關卡完成後才接續最新 main、確認差異與檢查、開 PR、核對精確 head 的 CI、合併，再進行有備份的匯入／發布／部署及公開頁驗證。既有授權的完成條件有效，不提前開部分 PR。

主任務 tasks/open/2026-09-14-codex-learning-series.md 的本輪工作由 codex-integration-fc2e 完成。保存本機提交後，任務釋放持有並標記 blocked，等待可用預覽環境與操作證據；沒有標記 done。剩餘工作保存在任務與本文件。
