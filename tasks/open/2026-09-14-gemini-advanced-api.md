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
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-content-tooling
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

- [x] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [x] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [x] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [x] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [x] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [x] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 81 `gemini-api-function-calling-workshop`：Function calling 實作：參數驗證、工具回傳與有限次迴圈。成果：用 Python 建立只查詢合成訂單的工具呼叫流程。
- [ ] 82 `gemini-api-search-grounding-citations`：Gemini API 搜尋引用：Grounding 結果解析與來源呈現。成果：讓應用程式回傳有來源對應的公開資訊摘要。
- [ ] 83 `gemini-api-file-search-rag-project`：File Search 知識庫實作：匯入、查詢、更新與刪除驗證。成果：以十份合成規格文件建立有引用的檢索問答。
- [ ] 84 `gemini-api-context-cache-experiment`：API 快取實驗：隱含快取、手動快取與實際成本核對。成果：比較重複文件請求的使用量，理解快取是否真的有幫助。
- [ ] 85 `gemini-api-batch-recovery`：Batch API 批次評測：工作 ID、部分失敗與重送管理。成果：對固定題庫建立可追蹤、可收斂的離線批次評測。
- [ ] 86 `gemini-api-document-service-capstone`：文件助手進階專案：有引用的問答服務、評測與交接。成果：完成可本機使用、有來源引用與測試資料的文件問答服務。
- [x] 在 docs/gemini-series/advanced/content/api/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [ ] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [x] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

這六篇已有完整本機作者交付，但尚未通過真實雲端驗收，沒有公開入口。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。

2026-09-14：認領 API 81–86，active scope 交集零。作者工具、工作與研究批次的本機交付已提交，故依賴改為 curriculum/content-tooling；跨批真實雲端驗收仍由原批次保留，不能視為已全部完成。本批固定 google-genai 2.23.0，獨立虛擬環境，不改 API 應用相依。優先完成無金鑰的 SDK 序列化、故障測試、本機服務及六篇原稿；沒有授權金鑰與費用上限時不執行真實模型、匯入或批次作業。

2026-09-14 作者交付完成：六篇正文 2169–2519 字，六包／十二 SVG／六 JPEG／七 ZIP，官方來源與本機 SDK 2.23.0 紀錄齊備。29 項本機測試與解壓後29項通過，服務 HTTP20題及1200/360px瀏覽器操作通過，24文章+6介面預覽逐張檢視。六包lint／草稿連結／原51頁／Ruff／tasks通過；相關API45通過7跳過（PostgreSQL未啟動）。authoring-review.json凍結檔案；原50篇catalogue與原51包、先前30篇草稿未改。

81–86 Steps 刻意保留未勾：所有真實 Google 工具問答／搜尋／十份索引生命週期／快取命中到期帳單／Batch恢復／20題模型評測皆 not_run。沒有授權金鑰與成本上限，不做真實模型或付費操作；也沒有部署、匯入或發布。交付 details 見 docs/gemini-series/advanced/content/api/README.md。
