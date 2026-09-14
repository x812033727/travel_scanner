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
branch:
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-platform
  - 2026-09-14-gemini-advanced-md
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

- [ ] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [ ] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [ ] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [ ] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [ ] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 75 `gemini-cli-mcp-server-workshop`：MCP 實作：建立本機唯讀商品查詢工具並排除連線問題。成果：讓 Gemini CLI 能查詢受範圍限制的合成商品資料。
- [ ] 76 `gemini-cli-hooks-quality-gates`：Hooks 品質檢查：事件輸入、退出碼與失敗時停止。成果：做出可觀察且確實會阻擋指定操作的檢查。
- [ ] 77 `gemini-cli-subagent-review-workflow`：Subagents 審查工作流：任務契約、工具限制與結果整合。成果：以兩個專門審查代理完成有證據的程式與文件檢查。
- [ ] 78 `gemini-cli-resumable-batch-pipeline`：Headless 批次處理：JSONL、續跑與避免重複輸出。成果：讓 20 份文件批次整理可中斷、續跑與追查失敗。
- [ ] 79 `gemini-cli-github-actions-artifacts`：Gemini CLI 接 GitHub Actions：受控觸發與產生審查報告。成果：在測試 repository 手動執行工作流並保存可下載的審查報告。
- [ ] 80 `gemini-cli-docs-maintenance-project`：CLI 完整專案：文件更新、連結檢查與人工審查交付。成果：將文件維護整合成能產出差異、報告及失敗記錄的流程。
- [ ] 在 docs/gemini-series/advanced/content/automation/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [ ] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [ ] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

這六篇目前只是規劃，沒有可公開教學頁。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。
