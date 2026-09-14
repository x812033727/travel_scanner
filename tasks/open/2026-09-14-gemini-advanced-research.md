---
id: 2026-09-14-gemini-advanced-research
title: Gemini 深入教學 57–62：NotebookLM 與研究方法
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:10:43Z
completed_at:
branch:
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-platform
  - 2026-09-14-gemini-advanced-work
scope:
  - docs/gemini-series/advanced/content/research
  - apps/api/app/guides/content/notebooklm-source-versioning.json
  - apps/web/public/guides/notebooklm-source-versioning
  - apps/api/app/guides/content/notebooklm-conflicting-sources.json
  - apps/web/public/guides/notebooklm-conflicting-sources
  - apps/api/app/guides/content/notebooklm-study-retrieval-practice.json
  - apps/web/public/guides/notebooklm-study-retrieval-practice
  - apps/api/app/guides/content/notebooklm-paper-comparison-matrix.json
  - apps/web/public/guides/notebooklm-paper-comparison-matrix
  - apps/api/app/guides/content/notebooklm-multiformat-lesson-pack.json
  - apps/web/public/guides/notebooklm-multiformat-lesson-pack
  - apps/api/app/guides/content/gemini-research-report-workshop.json
  - apps/web/public/guides/gemini-research-report-workshop
---

# Gemini 深入教學 57–62：NotebookLM 與研究方法

## Why

將 [深入課綱](../../docs/gemini-series/advanced/README.md#catalogue) 的 57–62 篇製作為完整教學。單篇規格及先修由 curriculum.json 決定；這是新作品／故障實驗，不重寫第一階段入門篇。

## Definition of done

- [ ] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [ ] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [ ] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [ ] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [ ] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 57 `notebooklm-source-versioning`：NotebookLM 資料版本管理：來源清單、更新與過期內容。成果：建立能追蹤資料版本的專題筆記本。
- [ ] 58 `notebooklm-conflicting-sources`：NotebookLM 引用查核：矛盾資料、缺證據與未知答案。成果：用證據矩陣辨識資料支持、矛盾及未回答的問題。
- [ ] 59 `notebooklm-study-retrieval-practice`：NotebookLM 備考實作：題庫、錯題分類與間隔複習。成果：由兩章教材製作可檢查答案的複習流程。
- [ ] 60 `notebooklm-paper-comparison-matrix`：NotebookLM 比較多篇研究：研究問題、方法與限制矩陣。成果：產出區分研究設計與結論強度的比較表。
- [ ] 61 `notebooklm-multiformat-lesson-pack`：NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查。成果：將同一份教材製作成可對照來源的三種學習材料。
- [ ] 62 `gemini-research-report-workshop`：Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告。成果：完成一份問題明確、引用可追查的長文報告。
- [ ] 在 docs/gemini-series/advanced/content/research/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [ ] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [ ] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

這六篇目前只是規劃，沒有可公開教學頁。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。
