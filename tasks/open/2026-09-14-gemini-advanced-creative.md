---
id: 2026-09-14-gemini-advanced-creative
title: Gemini 深入教學 63–68：圖片、影片與資料作品
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:10:45Z
completed_at:
branch:
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-content-tooling
scope:
  - docs/gemini-series/advanced/content/creative
  - apps/api/app/guides/content/gemini-image-consistent-series.json
  - apps/web/public/guides/gemini-image-consistent-series
  - apps/api/app/guides/content/gemini-image-editing-debugging.json
  - apps/web/public/guides/gemini-image-editing-debugging
  - apps/api/app/guides/content/google-flow-storyboard-workshop.json
  - apps/web/public/guides/google-flow-storyboard-workshop
  - apps/api/app/guides/content/google-flow-shot-continuity.json
  - apps/web/public/guides/google-flow-shot-continuity
  - apps/api/app/guides/content/gemini-sheets-data-audit-dashboard.json
  - apps/web/public/guides/gemini-sheets-data-audit-dashboard
  - apps/api/app/guides/content/gemini-content-production-handoff.json
  - apps/web/public/guides/gemini-content-production-handoff
---

# Gemini 深入教學 63–68：圖片、影片與資料作品

## Why

將 [深入課綱](../../docs/gemini-series/advanced/README.md#catalogue) 的 63–68 篇製作為完整教學。單篇規格及先修由 curriculum.json 決定；這是新作品／故障實驗，不重寫第一階段入門篇。

## Definition of done

- [x] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [x] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [x] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [x] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [x] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 63 `gemini-image-consistent-series`：Gemini 圖片系列製作：參考圖、風格規格與一致性評分。成果：製作同一原創商品的三張用途不同但風格一致的圖片。
- [ ] 64 `gemini-image-editing-debugging`：Gemini 修圖除錯：局部修改、文字錯誤與多輪退化。成果：用可追蹤的修改紀錄完成指定區域的修圖。
- [ ] 65 `google-flow-storyboard-workshop`：Google Flow 三鏡頭短片：腳本、分鏡與逐鏡生成。成果：完成具開場、過程與收尾的短片專案。
- [ ] 66 `google-flow-shot-continuity`：Google Flow 畫面連貫：起訖影格、參考素材與轉場修正。成果：修正兩個片段間的主體、動作與鏡位不連貫。
- [ ] 67 `gemini-sheets-data-audit-dashboard`：Gemini 與 Sheets 資料報表：清理 CSV、核對公式與圖表。成果：將含錯誤的資料整理成總數正確、可追查來源的報表。
- [ ] 68 `gemini-content-production-handoff`：Gemini 內容專案交付：文章、圖片與短片的版本和素材清單。成果：交付同一活動的文章、三張圖與短片，附完整素材記錄。
- [x] 在 docs/gemini-series/advanced/content/creative/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [x] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [x] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [x] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

六篇作者稿與練習附件已建置，但真實生成與平台驗收未完成，尚不可公開。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。

2026-09-14：使用者繼續後認領，active scope 交集零。--force 僅越過舊依賴；work 51 與 content-tooling 作者交付已提交，因此作者依賴改為 curriculum/content-tooling，真實生成與共享平台驗收仍保留。63–68 依單篇先修順序編寫，67 可獨立完成資料與本機 XLSX 模板；模板為文章下載附件，未要求建立使用者雲端試算表。圖片／影片參考素材明確標作者設計，不冒充 Gemini 或 Flow 實際輸出。


2026-09-14 作者交付：六篇 2,043–2,181 字，十二張 SVG／六張 JPEG、十四張 SVG／PNG 原創練習參考、七個 ZIP 與本機 XLSX 已完成。二十項故障／資料測試與解壓後同組測試通過；報表 43 列採用／7 列隔離、TWD 45,340 與 USD 50，變更單價會重算。Saved XLSX 的公式、型別、空白及圖表另外讀 XML 核對。24 張文章預覽、28 張參考預覽、六張工作表預覽已逐張檢查；鏡頭方向修正後重新渲染核對。

新六篇與先前二十四篇／原五十一頁內容、資產和連結檢查通過；guide pack lint 六篇通過。相關 API 測試最終 45 passed、7 skipped，跳過項需獨立 PostgreSQL 整合服務；此前一項圖上數字缺正文對照已修正圖說重測通過。Ruff 與 check:tasks 通過，僅有其他既有任務警告。來源、環境、限制與檔案凍結見 creative/README.md、verification/authoring-review.json。

尚未達成的課綱成品：63 真正三張生成圖片與三張失敗圖片；64 真實多輪局部修圖；65 三段影片及合片；66 基準／修訂影片與真實影格；67 Google Sheets 匯入與 Gemini 操作；68 文章／三張實際圖／短片及更新後交付。本次瀏覽器回報 User unavailable，模型呼叫及付費生成皆為零。not_run 不當作測試通過，作者插畫不當作模型輸出。六篇 Steps 因這些實測仍保持未勾選；本次只完成作者交付，不關閉任務、不發布。
