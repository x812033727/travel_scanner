---
id: 2026-09-14-gemini-advanced-work
title: Gemini 深入教學 51–56：日常與工作流程
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:10:41Z
completed_at:
branch:
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-platform
scope:
  - docs/gemini-series/advanced/content/work
  - apps/api/app/guides/content/gemini-prompt-evaluation-workshop.json
  - apps/web/public/guides/gemini-prompt-evaluation-workshop
  - apps/api/app/guides/content/gemini-gems-support-playbook.json
  - apps/web/public/guides/gemini-gems-support-playbook
  - apps/api/app/guides/content/gemini-canvas-budget-calculator.json
  - apps/web/public/guides/gemini-canvas-budget-calculator
  - apps/api/app/guides/content/gemini-workspace-meeting-handoff.json
  - apps/web/public/guides/gemini-workspace-meeting-handoff
  - apps/api/app/guides/content/gemini-mobile-field-notes.json
  - apps/web/public/guides/gemini-mobile-field-notes
  - apps/api/app/guides/content/gemini-spark-weekly-digest.json
  - apps/web/public/guides/gemini-spark-weekly-digest
---

# Gemini 深入教學 51–56：日常與工作流程

## Why

將 [深入課綱](../../docs/gemini-series/advanced/README.md#catalogue) 的 51–56 篇製作為完整教學。單篇規格及先修由 curriculum.json 決定；這是新作品／故障實驗，不重寫第一階段入門篇。

## Definition of done

- [ ] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [ ] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [ ] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [ ] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [ ] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 51 `gemini-prompt-evaluation-workshop`：提示詞改寫實驗：用固定題庫找出有效的修改。成果：留下能重做的提示詞 A/B 比較與評分表。
- [ ] 52 `gemini-gems-support-playbook`：Gems 客服知識助手：資料更新、拒答與回歸測試。成果：製作依商品手冊回答、遇到缺資料會轉人工的助手。
- [ ] 53 `gemini-canvas-budget-calculator`：Canvas 實作活動預算計算器：需求、除錯與驗收。成果：完成可調整人數、單價與備用金的預算小工具。
- [ ] 54 `gemini-workspace-meeting-handoff`：Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦。成果：將散落信件轉成附來源、負責人與日期的交接表。
- [ ] 55 `gemini-mobile-field-notes`：手機現場筆記：Gemini Live、照片與回到電腦整理。成果：把現場觀察整理成可核對的清單與圖文筆記。
- [ ] 56 `gemini-spark-weekly-digest`：Spark 每週資訊摘要：設定排程、檢查結果與停止任務。成果：建立範圍有限、來源可追查的每週摘要任務。
- [ ] 在 docs/gemini-series/advanced/content/work/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [ ] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [ ] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

這六篇目前只是規劃，沒有可公開教學頁。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。
