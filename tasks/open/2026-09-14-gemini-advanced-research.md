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
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-content-tooling
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
- [x] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [x] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [x] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [x] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [x] 57 `notebooklm-source-versioning`：NotebookLM 資料版本管理：來源清單、更新與過期內容。成果：建立能追蹤資料版本的專題筆記本。
- [ ] 58 `notebooklm-conflicting-sources`：NotebookLM 引用查核：矛盾資料、缺證據與未知答案。成果：用證據矩陣辨識資料支持、矛盾及未回答的問題。
- [ ] 59 `notebooklm-study-retrieval-practice`：NotebookLM 備考實作：題庫、錯題分類與間隔複習。成果：由兩章教材製作可檢查答案的複習流程。
- [ ] 60 `notebooklm-paper-comparison-matrix`：NotebookLM 比較多篇研究：研究問題、方法與限制矩陣。成果：產出區分研究設計與結論強度的比較表。
- [ ] 61 `notebooklm-multiformat-lesson-pack`：NotebookLM 多格式教材：講義、語音與影片摘要一致性檢查。成果：將同一份教材製作成可對照來源的三種學習材料。
- [ ] 62 `gemini-research-report-workshop`：Deep Research 加 NotebookLM：完成有證據與更新紀錄的專題報告。成果：完成一份問題明確、引用可追查的長文報告。
- [x] 在 docs/gemini-series/advanced/content/research/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [x] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [x] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [x] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

2026-09-14 作者原稿、內容包與參考練習已完成本機建置，尚未通過全部真實操作驗收，沒有新增可公開教學頁。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。

2026-09-14：依使用者「繼續」認領本批，active scope 交集為零。--force 僅越過舊波次依賴；已完成的 content-tooling 支援隔離作者作業，51–56 作者材料亦已提交。57–62 的單篇先修只依賴原入門與本研究批次，作者依賴改為 content-tooling；共同導覽及所有真實驗收仍是 release 門檻。瀏覽器狀態再次回報 User unavailable，未建立筆記本或生成媒體；繼續製作原稿、公開／原創練習資料及本機檢查，保留雲端與影音驗收待辦。

## 2026-09-14 作者交付與剩餘驗收

- [x] 57–62 六篇完整原稿／內容包，正文 2055–2219 字；正文互連、四階段、故障與三個 FAQ 已查。
- [x] 12 張 SVG 與六張 1600×900 封面 JPEG；24 張桌面／手機預覽逐張檢視。
- [x] 六份單篇 ZIP 與一份整合 ZIP，原創教材、參考矩陣／題庫、三份 CC BY 4.0 原始論文、政府授權 JSON 快照、作者報告與標準函式庫檢查器。
- [x] 22 項 fixture 測試通過，解壓整合包再跑 22 項通過；ZIP CRC／來源 bytes 一致。九張論文相關頁面已檢視。
- [x] 六篇 pack lint、內容／連結檢查、Ruff、tasks 通過；先前 18 篇與原 51 頁檢查通過。相關 API 測試 38 passed／8 skipped，跳過需獨立 PostgreSQL 的分支；SQLite 已驗。
- [x] 57 Drive 與上傳各 v1/v2 真實同步、引用、回答與舊產出重做紀錄。
- [ ] 58 真實模型五列證據矩陣、引用點擊、未知回答及故障修正。
- [ ] 59 Studio 題庫、實際十二題作答與間隔重測，不把預排日期當完成。
- [ ] 60 模型論文矩陣、逐欄引用與錯誤跨指標排名修正。
- [ ] 61 實際生成講義、音檔與影片、下載副檔名、30 筆一致性觀察。現只有作者教材／腳本，未完成真實媒體成品。
- [ ] 62 真實研究計畫、模型報告、Notebook 引用與更正。作者公開資料報告及 1800 筆快照計算已完成。

交付索引與凍結雜湊見 docs/gemini-series/advanced/content/research/README.md、verification/authoring-review.json。瀏覽器 User unavailable；零模型呼叫、零媒體生成、未發布。原 DoD 的完整練習成果與最終交付仍未勾選，需完成以上真實操作後才可交給 release。此次只提交作者批次並 release 認領，不將任務標 done。


## 2026-09-15 第 57 篇實測與修訂交付

使用者決定「手機先跳過」，實體裝置測試仍保留 work 票，不列為通過。本輪改做桌面研究流程；個人 Google AI Pro，API 零次、額外支出 NT$0。

- [x] 第 57 篇兩個獨立筆記本：上傳／Drive 各 v1 與 v2，四輪名額為 24→30，CAP 引用點擊核對。
- [x] 五份其他來源兩邊逐份比對，共十四份來源檢視；第五題同時選取兩版，辨識替代關係並排除 54 人。
- [x] 四份新舊筆記保存，更新後舊筆記仍 24 人，新筆記 30 人。Drive 舊引用預覽保留 v1，當前來源面板顯示 v2，分開記錄。
- [x] Drive 首次匯入失敗，更多→重新匯入後成功；同一份 Doc 改 v2，手動同步後原文與回答一致。沒有把此結果標為定期自動同步延遲已驗。
- [x] 重開後五份回答校驗值一致。上傳版舊來源重新勾選，已再取消並在教學提醒每次開始前檢查來源。
- [x] 保存自動來源指南的無根據「法律效力」補述與回答 Markdown 標題層級誤差，不把局部名額通過當作全部語意通過。
- [x] 證據位於 research/verification/live-20260915/57；瀏覽器擷取 FNV、凍結雜湊、Google 文件兩版匯出、來源正規化比對通過。原研究作者 176 個檔案原樣保存。
- [x] research/revisions/20260915 提供第 57 篇 2,777 字完整修訂稿、隔離內容包與新版練習 ZIP；23 個來源檔案通過解壓檢查，ArticlePack／pack lint／正文與章節連結通過。
- [ ] 58–62 真實操作仍照前述清單接續。整套 release 整合、公開頁面與 sitemap 驗證未做。

私人筆記本及 Doc 連結在 verification/live-20260915/private/57-links.json（gitignored）；保留兩個筆記本和 Doc 為使用者成果，分享權限未改。原作者原稿與 runtime pack 不覆寫，發布時應採用新 revision 收據。所有原創配圖沿用並更新圖說，沒有新增未驗圖片。第 57 篇手動同步已驗，失去存取權、定期自動同步等待、手機與額外 Studio 媒體沒有實測。
