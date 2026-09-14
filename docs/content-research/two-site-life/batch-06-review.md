# 第六批：20 篇內容包驗收

查證與驗收日期：2026-09-14。完成本機可匯入內容包，未執行正式站匯入、發布或部署。

catalogue.json 第 101–120 篇皆有原創正文、操作步驟、比較表、提醒、至少兩個相關內容包連結、官方來源與查證日。各篇提供 1600×900 hero.jpg、原始 hero.svg 及 diagram-1.svg。

## 驗證證據

- 20 篇各自執行 guides.pack_cli ingest 成功，結果保留在工具工作紀錄；沒有虛構整批 ingest 日誌。
- 每篇限定 slug lint、圖片渲染通過；40 張 QA PNG 均逐張檢視，未發現缺字、重疊或裁切。圖片為原創向量製圖，沒有外部素材授權缺項。
- 整批限定 20 個 slug lint 通過：20 entries checked，見 batch-06-lint.log。
- 內容包測試：9 passed、5 skipped，7.23 秒，見 batch-06-tests.log。5 項 PostgreSQL 整合測試因未提供資料庫測試環境而略過，不當成正式匯入驗證。
- 任務檢查通過：Validated 402 task file(s)，見 batch-06-tasks-prearchive.log；封存後另存 batch-06-tasks.log。其他任務既有的過期認領及範圍警告仍保留。
- batch-06-audit.json 核對正文 1,800–3,000 字、至少兩個本機 life 內容包連結、查證日期與每篇七項檔案雜湊。與 230 篇本機內容包比較，本批沒有 50 字以上完全相同段落。
- batch-06-live-inventory.json 重查 230 篇本機內容包、220 個 AI 規劃題目與 46 個文章相關任務。題庫外新增內容包及未對照任務 slug 均為空。
- 全批草稿繁體用字掃描通過。相關連結核對本機內容包存在，正式發布時仍需安排被引用文章一起可用。

## 編輯與主題界線

網站外包需求書以交付與驗收為主，與前批 SEO 公司服務評估分開。反向連結以引用與垃圾連結判斷為主，權重分數以第三方資料定義為主；沒有把 DA、DR 或 Authority Score 當作 Google 的排名分數。搜尋演算法歷史標示年份，現行維護建議另查官方指南。

Search Console、Sitemap、canonical、轉址、網址分區與 hreflang 分別處理帳號與資料、網址清單、內容版本、HTTP 行為、路由決策及語言地區對照。Sitemap 提交不保證索引，轉址保留方法區分 301/302 與 307/308，多語頁面沒有任意指向同一語言 canonical。

Schema、分享預覽與圖片 SEO 分別處理結構化實體、平台分享欄位及圖片可讀性。Google 搜尋功能資格不等於保證顯示；LinkedIn 更新分享快取不修改已存在貼文；WordPress 區塊替代文字與媒體庫預設值分開。

Core Web Vitals、PageSpeed、快取層、效能外掛及延遲載入各有不同操作目的與案例。INP、LCP、CLS 的真實資料與 Lighthouse 分數分開；no-cache 與 no-store 不混用；Cloudflare 快取清除不等於清除使用者瀏覽器。NitroPack Test Mode 關閉會套用最佳化設定，先回復不想保留的修改；首屏 LCP 圖片避免延遲載入。未提供虛構效能測試或改善百分比。

AMP 以網站模式、讀者入口、維護及退場為主。WordPress.org AMP 外掛查閱當日顯示最近三個主要版本未測試提醒，未推論已證實漏洞或 AMP 技術全面終止。Google 2021 Top Stories 公告只作歷史依據。SEO 外掛選擇依需求與資料遷移，核對免費與付費界線、語言分析支援及設定檔格式；不推薦為分數而換工具。

前六批共 120/232 篇完成本機驗收；其餘 112 篇仍待製作，整體計畫尚未完成。

本批封存重現既有 Windows tasks done 殘留 open 檔問題。確認 open/done 只差 status 與 completed_at、清單全數完成後，移除重複 open 檔；原因由既有 2026-09-14-investigate-windows-task-archive-leftover-open 任務追蹤。
