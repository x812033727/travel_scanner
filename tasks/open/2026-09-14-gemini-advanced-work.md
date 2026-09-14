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
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-curriculum
  - 2026-09-14-gemini-advanced-content-tooling
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

- [x] 六篇原稿、zh-TW 內容包、可複製範例與可下載練習包完整，正文每篇 1,800–3,000 字。
- [x] 六組原創封面與教學圖解完成；hero.jpg 1600×900，每張渲染並逐張檢查手機可讀性，附來源／授權。
- [x] 每篇依課綱提供四階段操作、明確成品、至少一個故障練習與修正、三個 FAQ、2–4 篇互連。
- [x] 官方來源於寫作當天重查，附 checked_on；平台／帳號／CLI／SDK／模型及 API 家族條件清楚。
- [x] 預期結果與實際輸出分開標註；語法、fixture、真實雲端、實體裝置及文件整理分別記錄，沒有做的驗證不能標通過。
- [ ] 凍結內容雜湊、範例驗證與逐張配圖檢視紀錄；交付整合任務前全部已完成。

## Steps

- [ ] 51 `gemini-prompt-evaluation-workshop`：提示詞改寫實驗：用固定題庫找出有效的修改。成果：留下能重做的提示詞 A/B 比較與評分表。
- [ ] 52 `gemini-gems-support-playbook`：Gems 客服知識助手：資料更新、拒答與回歸測試。成果：製作依商品手冊回答、遇到缺資料會轉人工的助手。
- [ ] 53 `gemini-canvas-budget-calculator`：Canvas 實作活動預算計算器：需求、除錯與驗收。成果：完成可調整人數、單價與備用金的預算小工具。
- [ ] 54 `gemini-workspace-meeting-handoff`：Gmail 到 Docs、Sheets：把會議信件整理成可交接的待辦。成果：將散落信件轉成附來源、負責人與日期的交接表。
- [ ] 55 `gemini-mobile-field-notes`：手機現場筆記：Gemini Live、照片與回到電腦整理。成果：把現場觀察整理成可核對的清單與圖文筆記。
- [ ] 56 `gemini-spark-weekly-digest`：Spark 每週資訊摘要：設定排程、檢查結果與停止任務。成果：建立範圍有限、來源可追查的每週摘要任務。
- [x] 在 docs/gemini-series/advanced/content/work/ 保存原稿、分批來源／素材定義、examples/ 與 verification/，格式依 platform 任務交接。內容包與公開圖片只寫 scope 所列位置。
- [ ] 依單篇 prerequisites 的拓樸次序製作；所依賴的另一批次交付後再做整合測試。
- [x] API 及需付費生成的操作只在已有授權、可用帳號與明確成本上限下執行；缺條件時記錄待辦，不能用示意輸出替代課綱要求的實測。
- [x] 更新本票實際驗證及限制；不修改共享 catalogue、原 51 頁收據或其他批次文章。

## How to verify

依 platform 任務交付的限定篇章建置／檢查指令驗六個 slug，再以既有 guides-pack lint 和 API 內容包測試檢查。實際 CLI / SDK / 生成結果按每篇 acceptance 測試；不以 lint 代替教學效果。最後 npm run check:tasks。

## Notes

這六篇已有完整作者原稿、內容包與素材，仍沒有可公開教學頁。共享來源與篇序由 release 任務最後整合；需要更改原課綱或共用程式時另行協調 scope。未完成驗證的篇章保留明確未勾選項目，六批全完成後一起開放深入目錄。

2026-09-14：使用者要求開始後續實作。API 的 83／85 篇尚依賴未寫的 58／51，故先補 51–56。認領前 sharedScope 核對所有 active 任務零重疊，--force 僅跨過已拆分的原 platform 依賴；作者階段改依賴已完成的 content-tooling，共用 UI 仍是整套發布門檻。Chrome 開啟 Gemini 逾時，重取環境回報 User unavailable；停止介面操作，保留帳號／裝置／排程實測待辦，不改其他批次及正式 catalogue。

## 2026-09-14 作者交付與實際驗證

51–56 六篇原稿、內容包、12 張原創配圖、7 個 ZIP 已完成；正文 2,226–2,687 字。51 有十題與二十列 A/B 記錄；52 有兩版手冊與十二題回歸；53 有完整本機 HTML 與三組人工答案；54 有五封合成信與四筆附引用待辦；55 有 CC0 原始照片及分裝置清單；56 有固定來源、期間檢查與六步排程觀察表。入口：docs/gemini-series/advanced/content/work/README.md。

- [x] Python 3.13.15 的 20 項資料檢查測試通過，解壓完整 ZIP 後再跑也通過。
- [x] 作者預算 HTML 在 Chromium 151.0.7922.34、Node 24.13.0，以 360／1440px 完成 28 筆操作；無網路請求或頁面例外。
- [x] 7 個 ZIP 的 CRC、成員路徑及來源位元組一致。
- [x] 24 張桌面／手機配圖預覽、2 張工具畫面、1 張授權照片逐張檢視；檢視紀錄另存。
- [x] 本批6篇、既有MD6篇、自動化6篇與原51頁的篇序／內容／資產／站內連結檢查通過；新6篇 pack lint 通過。
- [x] 相關 API 測試 38 passed、8 skipped；跳過的是未提供獨立 PostgreSQL 服務的整合分支。
- [x] Ruff 與 check:tasks 通過；任務工具既有其他範圍的逾時及重疊警告未改動。

以下仍是發布前驗收，不能用作者示例、fixture 或手動操作替代：

- [ ] 51：真實二十份模型回答及人工評分，確認環境、原始輸出與題庫一致。
- [ ] 52：Gems 儲存重開、資料版本切換、v1／v2 各十二份實際回答。
- [ ] 53：Canvas 實際生成與修正；本機參考 HTML 已驗證。
- [ ] 54：Gmail／Docs／Sheets 可用帳號操作、交接資料與來源可存取性。
- [ ] 55：Android、iPhone 實體裝置 Live／相機／停止分享及電腦接續。
- [ ] 56：一次手動、一次真正排程、暫停／恢復／刪除，並等待原定下一次觸發時間核對停止。
- [ ] 與其他批次及正式導覽整合，全部完成後再依限定清單發布及驗 sitemap。

authoring-review.json 凍結作者交付位元組；publishable=false。正式 guide-series.json 未加入深入篇章，沒有模型呼叫、寄信、建立 Spark 排程、資料庫匯入、push 或部署。任務保留 open，讓上述實測條件具備後接續；不要把作者完成改成整套驗收完成。
