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
- [x] 52：Gems 儲存重開、資料版本切換、v1／v2 各十二份實際回答。2026-09-15 已完成，另加修正版十二份；品質限制與後續文章整合見下方最新紀錄。
- [ ] 53：Canvas 實際生成與修正；本機參考 HTML 已驗證。
- [ ] 54：Gmail／Docs／Sheets 可用帳號操作、交接資料與來源可存取性。
- [ ] 55：Android、iPhone 實體裝置 Live／相機／停止分享及電腦接續。
- [ ] 56：一次手動、一次真正排程、暫停／恢復／刪除，並等待原定下一次觸發時間核對停止。
- [ ] 與其他批次及正式導覽整合，全部完成後再依限定清單發布及驗 sitemap。

authoring-review.json 凍結作者交付位元組；publishable=false。正式 guide-series.json 未加入深入篇章，沒有模型呼叫、寄信、建立 Spark 排程、資料庫匯入、push 或部署。任務保留 open，讓上述實測條件具備後接續；不要把作者完成改成整套驗收完成。

## 2026-09-15 Google Pro 真實網頁測試

使用者已開啟 Chrome／內建瀏覽器並確認 Pro；另允許 API，但費用上限 NT$0，僅可確認免費額度。這輪使用 Chrome 個人帳號的 Flash 網頁模式，保留現有個人化設定。API 金鑰環境變數只檢查存在與否，均未設定；沒有 API 呼叫或額外購買。

- [x] 51：固定題庫十題 × A/B，共二十個不同的新對話，交替順序；二十份真實回答已保存於 `docs/gemini-series/advanced/content/work/verification/live-20260915/51/`。
- [x] 題庫、兩版提示詞、rubric 及評分工具雜湊與原稿一致；所有提示詞在瀏覽器紀錄逐字核對，匯出後再核對二十筆傳輸 checksum。擷取僅取回答本文；追蹤檔把私人對話 URL 換成 SHA256。
- [x] 已提供逐題 AI 初查及獨立人工評分表；表內 `capture_status=captured`、`review_status=pending`，沒有將 AI 初查當成人工評分或宣稱 B 勝出。
- [ ] 51：人工依四項 rubric 評分及語意核准，完成後才能解除本篇完整驗收門檻。
- [x] 52：確認目前介面「設定 → Gem → 新增 Gem」，填入專用虛構助手名稱、說明與五段指示。
- [ ] 52：首次檔案功能出現「同意免責事項」；尚未同意／上傳／儲存，Chrome 草稿留待使用者處理後接續。詳細位置與下一步在 `live-20260915/52/preflight.md`。

本次只新增實測證據及本票進度，原作者交付、內容包、共享 catalogue、candidate release 及歷史 hash 收據不變；歷史收據的「未實測」是當時狀態，最新實測見上述目錄。整套仍不可發布，52–56 的原驗收項目持續待辦。沒有 push、PR、部署、資料庫匯入或公開頁改動。

本輪檢查：20 筆捕捉 audit、20 筆 browser-to-file checksum、154 個歷史作者檔案 hash、Ruff 及 428 份任務檢查通過；任務工具仍有既有其他範圍的 stale／overlap warnings。C08 兩份原始回答含行尾 tab；限定 raw/*.txt 保留位元組與行尾空白後，git diff --check 通過，不修改模型輸出以符合格式檢查。前後端程式與正式內容包未改動，沒有重跑全站測試。暫停時釋放認領，待同意視窗處理後可重新認領本票接續，勿重跑已保存的 51 題庫。

## 2026-09-15 續：第 52 篇實測與修正實驗

使用者回覆「好了」後，確認首次同意視窗已消失，沿用現有 Chrome／Pro。以下是本票最新狀態，取代上一輪「52 等待同意」的接續條件。

- [x] 建立「海風收納包教學實測 20260915」，僅上傳虛構手冊；完成兩題預覽、儲存與重開，五段指示及引用設定相符。
- [x] v1／v2 各十二份獨立回答；切換後只保留 v2，引用可開啟的兩份手冊全文與本機檔案相符。
- [x] 保留原始 24 份失敗與成功回答；另加一段能力界線、儲存重開核對，重跑完整十二題。修正版另存，沒有覆寫或重新生成原答案。
- [x] 原始及修正版共 36 筆問題／來源／對話完整性與 browser-to-file checksum 通過。原始 v2-G09／G11、修正版 G02 是無理由拒答，缺引用如實記錄；腳本通過不代表語意通過。
- [x] 保存 AI 逐題初查：修正版十一題明確說無法代為轉交，G02 仍拒答，G01／G03 重複文字，G08 的內容物句子不精確。重開 G03 文字一致，截圖也確認重複仍存在；截圖未保存或公開。
- [x] 154 個作者交付 hash 不變；只新增 live-20260915/52 證據、驗證腳本與紀錄。API 呼叫 0、額外購買 0；未寄信、建立真實客服案件、分享 Gem、建立 Spark 排程或修改公開頁。
- [ ] 把第 52 篇真實案例、不能代為轉交的指示與失敗限制整合到新版原稿／內容包，產生新驗收收據，再交共享 release 重建候選包。歷史收據不得改寫為已通過。
- [ ] 若以正式客服能力為驗收目的，拒答及重複／措辭問題仍需處理或明確限縮用途；目前僅完成教學實驗，不核准正式客服或整套發布。
- [ ] 第 51 篇人工評分，53 Canvas 真實生成／修正、54 Workspace、55 實體手機、56 真實排程及停止測試，仍依原項目接續。

入口：`docs/gemini-series/advanced/content/work/verification/live-20260915/README.md`；本篇見 `52/corrected-review.md`。私人對話 URL 只留在 git 忽略的本機暫存，追蹤紀錄改用 SHA256。不要重跑已有的 36 筆來挑選較佳答案，也不要重建另一個同名 Gem。

本輪檢查：24 + 12 筆捕捉／來源 audit、36 筆匯出校驗、154 個歷史 hash、Ruff、428 份任務檢查通過；task check 仍有其他既存範圍的 stale／overlap 警告。前後端程式與正式內容包未改動，未重跑全站測試。此次新增證據本機提交後釋放認領；沒有 push、PR、部署、匯入或公開發布。
