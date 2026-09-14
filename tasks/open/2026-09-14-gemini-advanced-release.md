---
id: 2026-09-14-gemini-advanced-release
title: Gemini 深入系列：36 篇整套驗收與目錄開放
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T11:11:05Z
completed_at:
branch: codex/gemini-advanced-platform
depends_on:
  - 2026-09-14-gemini-advanced-platform
  - 2026-09-14-gemini-advanced-work
  - 2026-09-14-gemini-advanced-research
  - 2026-09-14-gemini-advanced-creative
  - 2026-09-14-gemini-advanced-md
  - 2026-09-14-gemini-advanced-automation
  - 2026-09-14-gemini-advanced-api
scope:
  - docs/gemini-series/advanced/README.md
  - apps/web/lib/guide-series.json
  - apps/api/app/guides/content/gemini-guide.json
  - apps/api/app/guides/content/gemini-plans-ai-pro-ultra-2026.json
  - apps/api/app/guides/content/gemini-api-cost-errors-guide.json
  - docs/gemini-series/lessons/00.md
  - docs/gemini-series/lessons/02.md
  - docs/gemini-series/lessons/49.md
  - docs/gemini-series/sources.json
  - docs/gemini-series/README.md
  - docs/gemini-series/advanced/release
  - docs/life-ai-series.md
---

# Gemini 深入系列：36 篇整套驗收與目錄開放

## Why

第二階段六個內容批次全部完成後，把 36 篇整合進既有 Gemini 總目錄，確保 1 hub＋86 篇完整可讀。此票涵蓋凍結清單、驗收、整合與受控開放；不能以部分內容替代整套完成。

## Definition of done

- [ ] 核對六批共 36 個唯一 slug、完整素材與逐篇驗證紀錄；必要真實執行沒有被 fixture 或官方文件整理冒充。
- [ ] 將 51–86 的資料一次加入正式 guide-series.json，保留 01–50 的 slug／篇序、八類、原五路線，新增 stage 與六條深入路線。
- [ ] hub 文案、導覽及第 02／49 篇價格與新計費構成依發布日重查；僅修改明列篇章，保留既有 section-N 連結。
- [ ] 全部 87 頁連結、錨點、先修 DAG、搜尋、手機／桌面、無 JS、複製、sitemap 與至少 72 張新增圖解／封面驗收。
- [ ] 完成相關前後端、工具、型別、i18n 與任務檢查；保存確切 Git SHA 與證據。
- [ ] 確認本次對正式環境的發布授權仍適用；正式變更依既有發布流程，預設深入可見性關閉，先 dry-run 再限定 slug 逐篇匯入。
- [ ] 發布任一步失敗即停，按 starting/verified 記錄核對已完成部分；所有新舊子文章均可讀後才更新 hub 及開放深入目錄。
- [ ] 公開瀏覽器和 sitemap 驗證後記錄完整推出；第一階段 2026-09-14 的歷史收據保留不覆寫。

## Steps

- [ ] 閱讀各依賴任務的驗證與限制，取得經審查的發布 manifest。
- [ ] 整合單一 catalogue、hub 與必要計費說明；來源資料逐篇保存查證日。
- [ ] 用 platform 提供的開關驗證不開放與全開放狀態，特別測舊第 50 篇的下一篇與既有 hub 的 SSR。
- [ ] 在 advanced/release/ 保存 dry-run、發布日誌、逐篇公開比對、資產與瀏覽器證據。
- [x] 更新系列 README 與 AI 編輯總表的真正狀態；不把課綱或本機完成寫成上線。

## How to verify

使用 platform 任務交付的白名單發布命令及原有內容包／前後端／E2E 檢查。總數須為 87 頁，第二階段為 36 篇，全部通過且沒有重複或不明 slug；發布前後對照現有 51 頁與收據。實際命令與完成時間寫入本票。

## Notes

第二階段開關是必要順序保護：舊 hub 已發布，不能再沿用「hub 是否發布」作為新增連結的唯一條件。子文章逐篇匯入不具有原子性，發現失敗先核對而非整批盲目重送。


## 2026-09-15 本機候選整合（codex-gemini-release）

本次因七個依賴票尚有真實操作／合併待辦，正常 claim 被依賴檢查拒絕；使用 --force 僅認領本機候選準備，不跳過任何內容驗收或發布條件。scope 增加 advanced/README.md，以修正過期的「尚未製作」狀態。完成這段後 release 回 open，保留所有未完成依賴及上方發布勾選。

- [x] 在 advanced/release/ 建立 86 篇＋hub 的非發布候選；三個 overlay 是 hub、02、49，其餘 84 頁與原素材引用現有檔案。預定寫入限定 39 個 slug，子篇核對清單為 86。
- [x] 87 份 ArticlePack、正文／字數、來源日期、連結、下載與圖解檢查通過；三篇 h2 文字及順序完整保留。
- [x] 1,239 個不同內容／作者證據檔案 raw SHA-256 通過；六批共 72 張原創圖與 144 張文章預覽的歷史審查證據仍一致。
- [x] 更新總目錄閱讀方法與深入路線，02 保留 09-14 台灣價格紀錄並分開標出 09-15 用量／管理文件複核；49 補入 Function calling、搜尋工具、File Search、快取保存及 Batch 成本差異。
- [x] 新候選三頁在既有已驗證 Next 生產建置上，以候選 API 內容跑 18 次瀏覽器驗證：開關兩態、桌面／手機／無 JS。h2、正文隱藏連結、複製、無整頁橫向溢出通過。沒有重寫原 platform 證據。
- [x] 新增證據檢查回歸 7 項、原工具 17 項、選定 Python Ruff、tasks check 通過；計算器輸出 0.003375。--require-ready 正確退出 1，表示待驗收而非可發布。
- [ ] 真實帳號／模型／裝置操作：51–68、72–86 共 33 篇，具體成果及環境列於 advanced/release/ACCEPTANCE.md；69–71 只記現有 Windows CLI 模組範圍，沒有聲稱其他平台或另一版本通過。
- [ ] 發布日台灣價格與帳號條件：本次 Google One 網頁金額未載入，獨立未登入 Chromium 也逾時；沒有更新歷史價格查證日。
- [ ] 取得可用的 Google 測試環境與費用上限：瀏覽器控制回報 User unavailable，已向使用者詢問環境及上限，未收到回覆；沒有建立 Spark 排程或 Google 付費呼叫。
- [ ] 完成審查／合併、正式檔整合、真正凍結 manifest、資料庫 dry-run、部署／逐篇匯入、目錄開放及公開 sitemap 驗收。

證據入口：docs/gemini-series/advanced/release/README.md、local-verification.json、candidate/review.json、candidate/schema-validation.json、readiness.json、browser/verification.json。候選 schema 刻意不能交給發布工具；原 runtime catalogue raw SHA-256 仍為 1f6afed7f3bf7f05a407b8d5af4647938cf6d91df6b42a381a904b1f6d697bb2，50 篇未改動。

檢查來源 HEAD：b2f9dbc9；本次沒有 push、PR、merge、deploy、database import 或 publish。預設 Node 24.13.0 跑候選準備無輸出退出，改用 bundled Node 24.19.0 後成功；未修改 CLI 本體或隱藏這個本機工具限制。
