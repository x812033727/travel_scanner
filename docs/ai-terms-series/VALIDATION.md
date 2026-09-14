# AI 名詞系列驗收

搜尋截止及來源查證日期：2026-09-14。81 個獨立概念全部收錄，76 篇新增、5 篇保留網址補強；另新增總索引、更新既有 50 詞速查，共 83 個變更頁面（77 新增、6 更新、0 排除）。完整清單見 ARTICLES.md，來源與別名見 catalogue.json。

## 內容與圖文

- 四份跨作者審稿涵蓋全部 83 頁；必要修正已收斂至零。新興用語標明採用來源與定義分歧，案例均明示為原創教學情境，未宣稱實測。
- 81 篇概念文章與索引皆通過 1,800–3,000 字正文範圍、來源日期、分類、網址、相關連結及結構檢查。正文計數排除標題、圖說、比較表及來源欄位。
- 164 張原創向量插圖實際視覺複核通過；封面另經既有匯入工具轉為 JPEG。保留既有速查的兩張圖片。
- 真實 ContentBlocks 元件搭配 production CSS，83 頁各以 375px 和 1440px 渲染。166 個表格視窗已逐張看過，表格在自身容器橫向捲動，頁面沒有橫向溢出，預期圖片皆成功載入。此項是離線元件驗證，正式網址仍須另驗。
- release-manifest.json 固定 83 個 JSON 與 166 個實際引用圖片檔案。文字檔先依 .gitattributes 轉為 LF，再計算 SHA256；249 份 Git blob 與清單雜湊一致。public 中另保留封面 SVG 原稿。

## 系統

- 完整內容 lint/schema：0 錯誤、0 警告。
- 真實匯入流程在可拋棄的 SQLite 資料庫驗證：77 個新增草稿隱藏；6 個更新草稿保留舊公開文；83 個發布後可讀取；83 個未翻譯英文路徑隱藏；重跑 83 個內容全部 unchanged。
- 既有內容包與圖片匯入測試：29 passed、5 PostgreSQL-dependent skipped。
- 發布器測試：本機 SQLite／檔案範圍 4 項及隔離 PostgreSQL 17.11 的 4 項全部通過；包含完整 83 篇流程、寫入前中斷、提交後未記錄的續跑、既有草稿及並行變更拒絕、精確範圍與檔案雜湊。跨 SSH 的未完成測試另列 interrupted，未冒充通過；沒有把未選取的 SQLite 競態版本列成 skipped。
- 索引最後提交前鎖住相依文章資料列的測例已在隔離 PostgreSQL 實跑：另一個 READ COMMITTED 交易撤下文章時得到 SQLSTATE 55P03，之後索引正常提交且 83 篇公開 hash 一致。測試容器、專屬網路、映像標籤及 SSH tunnel 均已清理，正式十項容器 ID 與運作狀態未變。詳見 postgresql-validation.json。
- 相關網頁測試：90 passed。工具測試：39 passed。網頁建置、ESLint、5 語系翻譯鍵檢查與任務格式檢查通過。
- 整合主分支後修正 tools/workflow-pins.test.mjs 的 Windows file URL 路徑解析；使用 fileURLToPath，沒有改動 Actions 的固定版本。

## 發布邊界

這份文件記錄準備與驗收，並不代表文章已公開。正式動作依序為：精確版本與 CI 核對、備份、部署、83 slug／zh-TW dry-run、匯入草稿、發布 82 篇、最後發布索引、逐頁公開驗證。每篇提交都有持久紀錄；失敗時保留已完成結果，依 journal 核對後續跑，不能把整批描述成原子交易。

release_host.py 與 publish_host.py 使用既有主機鎖、Compose 設定、內容模型及匯入服務，沒有新增公開 API、資料表或區塊型別。正式結果以 publication.json、public-verification.json 與 live-browser-check.json 為準。搜尋引擎實際收錄不由 sitemap 或 robots 指令推定。

審稿報告中的原始檔案 SHA256 記錄實際閱讀時的本機位元組；Windows 的 CRLF 會由 Git 正規化為 LF。發布清單使用明確 LF 位元組，並已直接核對 Git blob，避免把換行差異誤當內容改版或正式檔案不一致。
