# 第五批：20 篇內容包驗收

查證與驗收日期：2026-09-14。僅完成本機內容包驗收，未執行正式站匯入、發布或部署。

catalogue.json 第 81–100 篇全部完成，每篇正文 1,800–3,000 字，含操作步驟、比較表、提醒、至少兩個相關內容包連結、官方來源及查證紀錄。各篇提供 1600×900 hero.jpg、原始 hero.svg 及 diagram-1.svg。

## 驗證證據

- 每篇個別執行 guides.pack_cli ingest 成功，產生 JSON 與三個圖片檔；個別結果保留在工具工作紀錄，未虛構整批 ingest 日誌。
- 每篇限定 slug lint 與圖片渲染通過，40 張 QA PNG 均已逐張檢視，未發現缺字、重疊或裁切。圖解與正文一致，所有圖片為原創向量製圖，無外部素材。
- 整批限定 20 個 slug 的 lint 通過：20 entries checked，見 batch-05-lint.log。
- 內容包測試：9 passed、5 skipped，39.53 秒，見 batch-05-tests.log。5 項 PostgreSQL 整合測試因沒有資料庫測試環境而略過，未視為正式匯入驗證。
- 任務檢查通過：Validated 402 task file(s)，見 batch-05-tasks-prearchive.log；封存後另存 batch-05-tasks.log。既有其他任務過期認領與範圍警告未由本批新增。
- batch-05-audit.json 核對正文長度、至少兩篇本機 life 相關文章、查證日期及每篇七項檔案雜湊。與 210 篇本機內容包比較，本批沒有 50 字以上完全相同段落。
- batch-05-live-inventory.json 重查 210 篇本機內容包、220 個 AI 規劃題目與 46 個文章相關任務；題庫外新增內容包及未對照任務 slug 均為空。
- 繁體用字掃描未發現待修用字。相關連結只核對本機內容包存在，正式發布時需一併處理被引用文章。

## 編輯與主題界線

WooCommerce 願望清單與詢價分別處理收藏資料、商品需求；訂單信設計與出貨通知分別處理客戶端呈現、訂單狀態與作業核對。稅金設定區分平台計算與個別商家的稅務義務。課程平台、預約系統及電商通路各以學生、時段容量、經營責任為主題。

SEO 學習路線、爬蟲辨識、抓取效率、技術稽核與單頁工作流分別處理學習順序、來源身分、伺服器需求、錯誤分級和內容實作。意圖、關鍵字、重複文章、標題、品質、可信度與公司評估各有獨立原創例子與圖解，未沿用來源推薦排名、優惠或測試結論。

特別保留的限制包括：TI Wishlist 收藏不鎖庫存；報價不等於付款；YayMail 模板與 WooCommerce 通知啟用分開；Order Notify 使用目前 Messaging API 流程而非已停用 LINE Notify；手動修改退款狀態不等於實際退款；列印明細不當成台灣合法電子發票。

稅額與商店成本均標示假設算例；課程匯出保留原始資產；Amelia 狀態、容量、緩衝與 Bookly 同步模式分開。搜尋爬蟲與 OpenAI 爬蟲依官方文件區分；Google Extended 不視為搜尋排名控制；抓取次數不當成索引或成效。

關鍵字規劃工具的廣告競爭度不當自然排名難度，Google Trends 指數不當搜尋次數；Search Console 匿名查詢和資料列限制明示。Canonical 不等於任意合併不同問題；Google 沒有指定最佳文章字數或標題固定字數。作者背景、E-E-A-T 與 YMYL 不當成可保證排名的分數。SEO／GEO 公司評估以提案、證據、費用與驗收為主，未背書個別公司。

前五批共 100/232 篇完成本機驗收；其餘 132 篇仍待製作，整體計畫尚未完成。

本批封存重現既有 Windows tasks done 殘留 open 檔問題。確認 open/done 只差 status 與 completed_at、清單已全數完成，才移除重複 open 檔；原因由 2026-09-14-investigate-windows-task-archive-leftover-open 既有任務追蹤。
