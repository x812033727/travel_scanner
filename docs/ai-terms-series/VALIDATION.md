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

## 正式發布

正式部署版本為 `3b8df68c693eb81ccde7793a2f89d71999dbb2c2`，精確 SHA 的主分支 CI [34815324935](https://github.com/x812033727/travel_scanner/actions/runs/34815324935) 全部通過。2026-09-14 07:23:04 UTC 啟用固定映像，部署前與發布前備份皆完成並通過 pg_restore 目錄檢查；沒有宣稱完成還原演練。

83 slug／zh-TW dry-run 通過後，完整匯入 83 篇草稿。匿名 HTTP 實測確認 77 篇新文沒有公開正文，6 篇更新仍保留原公開版本。既有隱藏頁的實際契約是 HTTP 200、API status=unpublished、無 document，以及 noindex 的不可讀頁面，不能只看 HTTP 狀態判斷是否公開。

82 篇文章公開後，先核對全部正文與 166 個圖片檔案，再於 2026-09-14 15:36:30（台灣時間）最後發布索引。完成後的公開驗證已核對 83 頁的正文雜湊、canonical、索引指令、索引回連、166 個圖片位元組與 83 個 sitemap 網址。每篇提交都有持久紀錄，這批不是原子交易。

手機表格修正已部署。實際 Chrome 對曼谷交通、AI 模型分級及共用法律頁的 375/1440px 共六項檢查通過，表格與法律頁截圖經實際視覺複核。曾有 Windows 報告覆寫鎖及單張截圖逾時；覆寫檢查點改用直接寫入，截圖等待延長，僅補跑未完成案例並保留原始失敗紀錄。這不改變伺服器發布 journal 的原子寫入與 fsync。

全系列實際 Chrome 檢查完成：83 頁、166 個 375/1440px 視窗全部 passed，0 failed、0 not run。六篇代表頁的 24 張正式截圖，加上表格回歸的 8 張截圖，均實際開圖檢視並記錄 SHA256，詳見 live-visual-review.json。export_publication.py 已核對備份、發布順序、83 篇最終版本與正文雜湊、草稿及索引隱藏階段、公開 HTTP、瀏覽器與 PostgreSQL 證據，產出 status=published_and_verified 的 publication.json。

發布前兩項差異已處理並保留紀錄：另一流程先部署相同來源版本但不同映像，因此先核對環境、資料庫與 Redis 未變、保存原始狀態及回退映像，再完成本次備份與固定映像啟用；既有速查的 ai／misc 標籤則透過原管理服務更正為 ai／tutorial，正文與 locale 版本未因這項分類修正而變動。分類修正後重新 dry-run，通過後才匯入草稿。主分支期間新增的新聞收據及第六批攻略規劃均為文件變更，本次沒有把它們描述成新的程式部署。

release_host.py 與 publish_host.py 使用既有主機鎖、Compose 設定、內容模型及匯入服務，沒有新增公開 API、資料表或區塊型別。正式結果以 publication.json、public-verification.json 與 live-browser-check.json 為準。搜尋引擎實際收錄不由 sitemap 或 robots 指令推定。

審稿報告中的原始檔案 SHA256 記錄實際閱讀時的本機位元組；Windows 的 CRLF 會由 Git 正規化為 LF。發布清單使用明確 LF 位元組，並已直接核對 Git blob，避免把換行差異誤當內容改版或正式檔案不一致。
