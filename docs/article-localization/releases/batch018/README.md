# Batch018 網站基礎文章五語上架紀錄

2026-09-23 已補齊以下 4 篇的簡中、英文、日文、韓文，共 16 份完整正文與 48 張語言圖片。連同保留的繁中，20 個語言網址均通過正文、圖片、canonical、hreflang、站內連結及桌面／手機瀏覽器驗收。本紀錄只涵蓋第 018 批，不代表全站語言缺稿已全部完成。

| 文章 | 內容完成 | 草稿匯入 | 公開發布 | 瀏覽器驗證 | 五語網址 |
|---|---|---|---|---|---|
| 網域註冊 | 新增四語圖文完成 | 4/4 已匯入 | 5/5 已公開 | 五語桌面／手機通過 | [繁中](https://mokaair.com/zh-TW/life/domain-registration-guide) · [簡中](https://mokaair.com/zh-CN/life/domain-registration-guide) · [EN](https://mokaair.com/en/life/domain-registration-guide) · [日本語](https://mokaair.com/ja/life/domain-registration-guide) · [한국어](https://mokaair.com/ko/life/domain-registration-guide) |
| 主機類型 | 新增四語圖文完成 | 4/4 已匯入 | 5/5 已公開 | 五語桌面／手機通過 | [繁中](https://mokaair.com/zh-TW/life/hosting-types-explained) · [簡中](https://mokaair.com/zh-CN/life/hosting-types-explained) · [EN](https://mokaair.com/en/life/hosting-types-explained) · [日本語](https://mokaair.com/ja/life/hosting-types-explained) · [한국어](https://mokaair.com/ko/life/hosting-types-explained) |
| CMS 選擇 | 新增四語圖文完成 | 4/4 已匯入 | 5/5 已公開 | 五語桌面／手機通過 | [繁中](https://mokaair.com/zh-TW/life/website-cms-choice) · [簡中](https://mokaair.com/zh-CN/life/website-cms-choice) · [EN](https://mokaair.com/en/life/website-cms-choice) · [日本語](https://mokaair.com/ja/life/website-cms-choice) · [한국어](https://mokaair.com/ko/life/website-cms-choice) |
| 網站維護 | 新增四語圖文完成 | 4/4 已匯入 | 5/5 已公開 | 五語桌面／手機通過 | [繁中](https://mokaair.com/zh-TW/life/website-maintenance-routine) · [簡中](https://mokaair.com/zh-CN/life/website-maintenance-routine) · [EN](https://mokaair.com/en/life/website-maintenance-routine) · [日本語](https://mokaair.com/ja/life/website-maintenance-routine) · [한국어](https://mokaair.com/ko/life/website-maintenance-routine) |

內容 PR [#676](https://github.com/x812033727/travel_scanner/pull/676) 在 `e17895e3c12ce19fe421536dd2ba543afbdc233c` 通過全部 8 項 CI，合併為 `5a1682a1c62280b99cf7e21f4f583c9cad78a470`。首次部署在執行主機部署腳本前，因 main 已前進而停止；舊備份、失敗紀錄與發布目錄全部保留，沒有執行該次部署或匯入。

重新核對 [PR #679](https://github.com/x812033727/travel_scanner/pull/679) 的 8 項成功 CI 與合併內容後，正式部署 `38ebec88c91db6ae0f6c8cd812bf04c5e1da9c95`。新增差異只有 CatchTable 資料、文件與任務；79 份發布所需 Git 匯出與原先審核版本一致。發布暫停檔在四把鎖保護下轉移至新的本批目錄，接著另做新資料庫備份並以 `pg_restore --list` 驗證，才執行部署、匯入預演及發布。

16 份新增語言於臺灣時間 17:10 發布，均為 locale／published v2。20 份完整資料模型、4 份既有繁中完整資料列與文章 metadata 均完成前後比對；繁中正文、分類、排序、可見性與 12 張原始圖片保留。發布 journal 包含 16 次建稿及 16 次文章發布，本批沒有總目錄發布。草稿保護依明確四篇／四語清單及版本衝突機制執行，未對全站其他草稿做逐筆驗收。

48 張新圖片包括 32 張 SVG 與 16 張 1600×900 JPG。正式站全部 60 張新舊圖片通過 MIME、尺寸相關檢查及完整檔案 SHA256 比對。公開頁面驗收涵蓋 40 個五語桌面／手機案例及 20 個圖片說明／來源案例；80 張頁首與示意圖截圖逐張獨立檢查。手機示意圖使用可橫向捲動的 1180px 圖，公開截圖涵蓋中央位置，完整標籤另由桌面圖、原始本機渲染及檔案雜湊驗收。這是瀏覽器 viewport 驗收，未宣稱實體裝置測試或每段全文截圖。

sitemap API 讀完 1,000＋928 筆並取得終止游標；1,928 個文章／語言網址全部存在於 XML sitemap。五筆日文數字格式等價情況有明確審閱紀錄（CMS 四筆、網站維護一筆），沒有誤報為零警告。既有桌面搜尋圖示與提示字重疊仍由任務 `2026-09-22-fix-desktop-global-search-placeholder-icon` 追蹤，未阻擋本批文章閱讀。

最終證據封存並通過驗收後，於臺灣時間 17:34 解除本批 hold。17:34:28 的唯讀檢查確認主機仍為同一個 `38ebec88` 提交、工作目錄乾淨、無 hold，三個健康端點均為 200。其後的文件 PR 無須為此重新部署應用。

資料庫快照、備份、journal、原始截圖與逐筆收據保留在版本庫外的 `C:/Users/x8120/.codex/article-localization-release/`。[evidence.json](evidence.json) 收錄每篇五語網址、發布時間、版本、正文雜湊，以及 29 份外部證據的精確路徑、SHA256 與 JSON pointers。核心 pins：

| 證據 | SHA256 |
|---|---|
| final-evidence.json | `90f407364456a582b118c7c5b6f4697933bd0d840f5bccbbafd9dc824ba3f40a` |
| final-acceptance.json | `0e340684df166e324e16aead8934100ba5531ff39aacb09c94b31977c8daaa2f` |
| 解除 hold 後唯讀檢查 | `cd7d6bb1e8e4d00df0fe9cb9ec91d98207d11b470bafcf9f7083dc679238d7b3` |
