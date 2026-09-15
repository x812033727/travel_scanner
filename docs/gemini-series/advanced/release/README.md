# Gemini 深入系列本機候選包

> 後續進度與第一版 PR 交接見 [2026-09-15 整理紀錄](pr-review-20260915/README.md)。以下是早期候選的歷史結果；整合最新主線後，部分引用文章已變動，舊候選雜湊不再全部符合目前檔案。發布前需整合新版實測文章並重新建立候選，不可直接使用此收據。

2026-09-15：87 頁（總目錄＋86 篇）的候選內容已完成本機檢查。正式 catalogue 仍是 50 篇；本資料夾沒有修改資料庫、部署網站或開放新增目錄。六批作者紀錄均仍標示不可發布，33 篇需要真實帳號、模型或裝置實測，明細在 [逐篇驗收表](ACCEPTANCE.md)。

## 可檢查的內容

- [86 篇目錄資料](candidate/guide-series.json)：沿用全部 slug、八類與原五條路線，加入六條深入路線。
- 三篇更新原稿：[總目錄](lessons/00.md)、[02 方案](lessons/02.md)、[49 API 計費](lessons/49.md)。編譯內容在 candidate/content/，其餘 84 頁引用 repository 的既有內容包，不另複製維護。
- [候選收據](candidate/review.json)：420 個內容與素材檔案雜湊、來源 Git SHA、87 頁檢查及預定 39 個寫入 slug（36 新篇＋02／49＋hub）。hub 必須最後寫入，寫入前仍需重新確認全部 86 篇子文章。
- [來源查證](source-checks.json)：各篇各自保存日期。2026-09-15 的 Google One 文字頁與獨立未登入瀏覽器未取得價格金額；02 篇保留 2026-09-14 的價格及 Flow 點數紀錄，不冒充發布日複核。API 工具、File Search、快取保存與 Batch 依官方文件補充。
- [證據核對](readiness.json)：1,239 個不同檔案、六批作者紀錄、72 張原創 SVG 與 144 張文章桌面／手機預覽均符合既有雜湊。這次是重查保存的證據，並非重新執行所有模型工作或重新逐張審圖。

candidate/review.json 使用獨立的 gemini-review-candidate-v1 格式，刻意沒有 releaseId，既有發布工具會拒絕把它當成凍結發布 manifest。不要把 publishable 改成 true 代替實測與審查。它只列出可檢查的候選內容。

## 本機驗證

| 項目 | 結果與範圍 |
| --- | --- |
| 內容、連結與素材 | 87 頁通過；章節定位、下載檔、先修與延伸連結檢查通過。 |
| 後端內容格式 | 87 份通過既有 ArticlePack；[逐篇字數](candidate/schema-validation.json)。02 為 2,368 字、49 為 2,656 字。 |
| 章節穩定 | 三篇原有全部 h2 文字及順序保留，原 section-N 不變。 |
| 新候選瀏覽器 | [18 次頁面驗證](browser/verification.json)：三篇 × 兩種開關 × 桌面／手機／無 JS。章節、隱藏連結、複製與整頁不溢出通過。 |
| 既有平台完整驗證 | [原 50／86 篇整合證據](../platform/next-integration/README.md) 保留。候選測試重用該次 Next 生產建置，API 換成本機候選包；瀏覽器外部網路封鎖。 |
| 證據檢查回歸 | 7 項測試涵蓋檔案變動、缺檔、路徑越界、空收據與換行差異；工具既有 17 項回歸通過。 |
| 計費範例 | 本地計算器得到 0.003375，沒有 Google API 呼叫或真實帳單。 |
| 發布就緒檢查 | --require-ready 回傳 1，表示目前仍不可發布；不是結構檢查失敗。 |

手機程式區塊允許在區塊內水平捲動；整頁沒有橫向溢出。[方案範例](browser/mobile-2-copy.png) 與 [計費範例](browser/mobile-49-copy.png) 已人工檢視，標籤與複製按鈕可讀，頁尾固定導覽會覆蓋截圖底部部分內容，不能將截圖當作完整程式。

## 重跑

從 repository 根目錄執行，使用已安裝 Next／Playwright 的 Node 24.19.0 及 API Python 環境。此機預設 Node 24.13.0 執行候選準備曾無輸出退出，改用 bundled Node 24.19.0 成功；這是本機工具紀錄，不代表 Gemini CLI 的版本相容性測試。

```powershell
node docs/gemini-series/advanced/release/prepare-candidate.mjs
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/release/audit-readiness.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/release/test-readiness.py
node --test tools/gemini-series.test.mjs
node docs/gemini-series/advanced/release/check-candidate-browser.mjs
```

prepare 只寫本資料夾，組合完整 87 頁到忽略追蹤的 .workspaces/ 副本。它不做 API 資料庫 dry-run。瀏覽器測試需要先有 platform/next-integration/prepare.mjs 與 build.mjs 的成功建置；換環境時先重建，不借用其他版本的編譯結果。

## 尚待完成

Google 瀏覽器控制本次回報 User unavailable，尚未取得可登入測試環境與總費用上限。不要把 fixture 輸出填成 Google 實際結果。請依 [逐篇驗收表](ACCEPTANCE.md) 保存模型／裝置／帳號條件、實際輸入輸出、失敗例、修正與用量；有排程或批次工作時，保存真正完成的事件與結果。

完整真實驗收及當日來源複核後，將核准的三篇原稿、來源與內容包以及 catalogue 整合回正式位置，再產生真正的凍結 manifest。後續依原發布程序完成審查合併、部署、資料庫 dry-run、限定 slug 逐篇匯入、全部子文章核對、hub／開關開放與公開頁面及 sitemap 驗證。歷史發布日誌與作者紀錄保持不覆寫。
