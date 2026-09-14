---
id: 2026-09-14-gemini-advanced-api
title: Gemini 深入教學 81–86：API 工程與完整專案
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:10:55Z
completed_at:
branch:
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-platform
  - 2026-09-14-gemini-advanced-work
  - 2026-09-14-gemini-advanced-research
scope:
  - docs/gemini-series/advanced/content/api
  - apps/api/app/guides/content/gemini-api-function-calling-workshop.json
  - apps/web/public/guides/gemini-api-function-calling-workshop
  - apps/api/app/guides/content/gemini-api-search-grounding-citations.json
  - apps/web/public/guides/gemini-api-search-grounding-citations
  - apps/api/app/guides/content/gemini-api-file-search-rag-project.json
  - apps/web/public/guides/gemini-api-file-search-rag-project
  - apps/api/app/guides/content/gemini-api-context-cache-experiment.json
  - apps/web/public/guides/gemini-api-context-cache-experiment
  - apps/api/app/guides/content/gemini-api-batch-recovery.json
  - apps/web/public/guides/gemini-api-batch-recovery
  - apps/api/app/guides/content/gemini-api-document-service-capstone.json
  - apps/web/public/guides/gemini-api-document-service-capstone
---

# Gemini 深入教學 81–86：API 工程與完整專案

## Why

將 [深入課綱](../../docs/gemini-series/advanced/README.md#catalogue) 的 81–86 篇製作為完整教學。單篇規格及先修由 curriculum.json 決定；這是新作品／故障實驗，不重寫第一階段入門篇。

## Definition of done

- [ ] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [ ] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [ ] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [ ] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [ ] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 81 `gemini-api-function-calling-workshop`：Function calling 實作：參數驗證、工具回傳與有限次迴圈。成果：用 Python 建立只查詢合成訂單的工具呼叫流程。
- [ ] 82 `gemini-api-search-grounding-citations`：Gemini API 搜尋引用：Grounding 結果解析與來源呈現。成果：讓應用程式回傳有來源對應的公開資訊摘要。
- [ ] 83 `gemini-api-file-search-rag-project`：File Search 知識庫實作：匯入、查詢、更新與刪除驗證。成果：以十份合成規格文件建立有引用的檢索問答。
- [ ] 84 `gemini-api-context-cache-experiment`：API 快取實驗：隱含快取、手動快取與實際成本核對。成果：比較重複文件請求的使用量，理解快取是否真的有幫助。
- [ ] 85 `gemini-api-batch-recovery`：Batch API 批次評測：工作 ID、部分失敗與重送管理。成果：對固定題庫建立可追蹤、可收斂的離線批次評測。
- [ ] 86 `gemini-api-document-service-capstone`：文件助手進階專案：有引用的問答服務、評測與交接。成果：完成可本機使用、有來源引用與測試資料的文件問答服務。
- [ ] 在 docs/gemini-series/advanced/content/api/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [ ] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [ ] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

這六篇目前只是規劃，沒有可公開教學頁。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。
