---
id: 2026-09-14-gemini-advanced-automation
title: Gemini 深入教學 75–80：CLI 擴充與自動化專案
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:10:50Z
completed_at:
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-content-tooling
scope:
  - docs/gemini-series/advanced/content/automation
  - apps/api/app/guides/content/gemini-cli-mcp-server-workshop.json
  - apps/web/public/guides/gemini-cli-mcp-server-workshop
  - apps/api/app/guides/content/gemini-cli-hooks-quality-gates.json
  - apps/web/public/guides/gemini-cli-hooks-quality-gates
  - apps/api/app/guides/content/gemini-cli-subagent-review-workflow.json
  - apps/web/public/guides/gemini-cli-subagent-review-workflow
  - apps/api/app/guides/content/gemini-cli-resumable-batch-pipeline.json
  - apps/web/public/guides/gemini-cli-resumable-batch-pipeline
  - apps/api/app/guides/content/gemini-cli-github-actions-artifacts.json
  - apps/web/public/guides/gemini-cli-github-actions-artifacts
  - apps/api/app/guides/content/gemini-cli-docs-maintenance-project.json
  - apps/web/public/guides/gemini-cli-docs-maintenance-project
---

# Gemini 深入教學 75–80：CLI 擴充與自動化專案

## Why

將 [深入課綱](../../docs/gemini-series/advanced/README.md#catalogue) 的 75–80 篇製作為完整教學。單篇規格及先修由 curriculum.json 決定；這是新作品／故障實驗，不重寫第一階段入門篇。

## Definition of done

- [x] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [x] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [x] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [x] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [x] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 75 `gemini-cli-mcp-server-workshop`：MCP 實作：建立本機唯讀商品查詢工具並排除連線問題。成果：讓 Gemini CLI 能查詢受範圍限制的合成商品資料。
- [ ] 76 `gemini-cli-hooks-quality-gates`：Hooks 品質檢查：事件輸入、退出碼與失敗時停止。成果：做出可觀察且確實會阻擋指定操作的檢查。
- [ ] 77 `gemini-cli-subagent-review-workflow`：Subagents 審查工作流：任務契約、工具限制與結果整合。成果：以兩個專門審查代理完成有證據的程式與文件檢查。
- [ ] 78 `gemini-cli-resumable-batch-pipeline`：Headless 批次處理：JSONL、續跑與避免重複輸出。成果：讓 20 份文件批次整理可中斷、續跑與追查失敗。
- [ ] 79 `gemini-cli-github-actions-artifacts`：Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告。成果：在測試 repository 手動執行工作流並保存可下載的審查報告。
- [ ] 80 `gemini-cli-docs-maintenance-project`：CLI 完整專案：文件更新、連結檢查與人工審查交付。成果：將文件維護整合成能產出差異、報告及失敗記錄的流程。
- [x] 在 docs/gemini-series/advanced/content/automation/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [ ] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [x] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

六篇完整原稿、內容包、配圖與下載練習已交付本地分支，尚無公開教學頁。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。

2026-09-14：使用者指示直接開始。認領前以 sharedScope 核對所有 active 任務零重疊；--force 只跨過舊的整合先修，未跨他人 scope。內容建置工具已完成，69–74 原稿已交付，故作者階段先修改為已完成的 content-tooling。MD 尚欠的模型／會話驗收與共用 UI 仍是整套整合及發布的條件，不會用本批原稿取代它們。


## 2026-09-14 實作交付

- [x] 75–80 六篇完整文章，正文 2,449–2,846 字；四階段、故障練習、三個 FAQ 與互連完整。作者入口為 docs/gemini-series/advanced/content/automation/README.md。
- [x] 十二張原創 SVG、六張 1600×900 JPEG，二十四份桌面／360px 預覽均逐張檢視；素材為 Mokaair 原創，練習程式與合成資料 MIT。
- [x] 六個獨立練習 ZIP 與一個可重做驗證 ZIP，CRC、成員與來源位元組一致；解壓後重跑成功。
- [x] CLI 0.59.0／Node 24.19.0／Windows：實際 MCP stdio 10、Hook 11、代理解析 3、policy 4，共 28 筆。Python 3.13.15 fixture 23 項通過。MCP 以官方 SDK 2.2.0 的 MCPServer 實作，沒有混用舊 FastMCP API。
- [x] 本批六篇 catalogue／字數／資產／正文與先修連結，以及 pack lint 通過；前批六篇與原始 51 頁檢查通過。API 相關測試 38 passed、8 skipped（需要隔離 PostgreSQL）；不當成完整資料庫發布驗收。
- [x] 官方來源、四個 Actions 完整提交識別、逐圖檢視、下載驗證與作者雜湊快照存於 verification/。先前一次暫存清理錯誤及一次未重現的 fixture 前置失敗保存在 local-limitations.json，沒有臆測已修復根因。

## 保留未勾選的驗收

- [ ] 75：已登入 CLI 由模型選 MCP 工具；惡意資料文字不被當成指示；互動停用／重啟及清單確認。
- [ ] 76：完整模型觸發 BeforeTool，核對拒絕後原檔不變與正常寫入。模組支援絕對／相對路徑且拒絕外部 docs 目錄連結已實測；不能替代這項互動驗收。
- [ ] 77：兩個真實子代理輸出、讀取工具、是否並行與問題辨識效果；作者 fixture 不算模型結果。
- [ ] 78：一份試跑及二十份真實 Headless 續跑，保存延遲、用量、成本與摘要品質；程式不自動重試模型，CLI 內部重試仍應觀察。
- [ ] 79：在指定測試 repository 手動跑 hosted workflow，核對帳號的 Environment 條件及下載 artifact；目前僅 YAML／官方 pins／本機 adapter。
- [ ] 80：真實 CLI 修正提案與完整文件維護流程。十份文件、作者參考修正、錯誤提案、來源保留與 Git patch 檢查已通過。
- [ ] 取得可用測試帳號／模型與明確成本範圍後補模型驗收；尚未讀取帳密、呼叫付費模型或觸發 GitHub 遠端工作。
- [ ] 複驗 macOS／Linux，與 MD 批待驗項及其他四批文章整合；原始 runtime catalogue 維持 50 篇，不部署、不發布、不開深入入口。

作者程式與下載包修改後需重跑 build-data.py、verify-delivery.py，再重建六個 pack。visual-review.json 是逐圖檢視；authoring-review.json 是本批位元組快照，均不是發布許可。工作保留在目前分支，釋出認領讓後續能接續驗收。
