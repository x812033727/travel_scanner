# Codex 教學中心正式發布紀錄（2026-09-20）

五語 [Codex 教學總目錄](https://mokaair.com/zh-TW/life/codex-learning-hub)與 60 篇獨立教學已上架。共 61 個內容包、305 份語言文件；總目錄與每篇互相連結，搜尋、篩選與分享網址可在重新整理後保留。

| 語言 | 公開總目錄 |
| --- | --- |
| 繁體中文 | [開啟](https://mokaair.com/zh-TW/life/codex-learning-hub) |
| 簡體中文 | [開啟](https://mokaair.com/zh-CN/life/codex-learning-hub) |
| English | [Open](https://mokaair.com/en/life/codex-learning-hub) |
| 日本語 | [開く](https://mokaair.com/ja/life/codex-learning-hub) |
| 한국어 | [열기](https://mokaair.com/ko/life/codex-learning-hub) |

教學內容由 [PR #578](https://github.com/x812033727/travel_scanner/pull/578) 合併；總目錄帶參數網址的修正由 [PR #583](https://github.com/x812033727/travel_scanner/pull/583) 合併。正式服務運行精確提交 `6532eaa6e7e9d5a34b94cfe8f8a62ed2e0fba9a1`，其主分支五項工作流程全部成功。映像建置後主分支又前進至 `e9f1d1e0cc7b3f972bfaee4ff2b37b2f6e0577c0`；啟用前已核對兩版間僅 `docs/`、`tasks/` 路徑變更，未將尚未驗證的新程式混入本次部署。

正式匯入先發布 60 篇文章的 300 份語言文件（297 筆新增、3 筆更新），再發布總目錄的 5 份語言文件。部署新程式後，針對全部 61 包重新執行匯入預覽：305 份均為 `unchanged`，待發布數為 0；Codex 站內連結在五語的檢查結果都是 0 筆問題。

部署前暫停八項應用寫入服務，建立 `/root/mokaair-release-codex-6532eaa6e7e9/predeploy.dump`。備份為 PostgreSQL custom format，123,585,075 bytes，權限 `0600`，SHA-256 `f15f491a9a50afcec1abf73c42ffd56695b242fe4710db0383bc94a68d61a4cb`，已用 `pg_restore --list` 檢查可列出索引。遷移前後九個受保護資料表的指紋相同；資料庫版本是 `0082_travel_food_subtopics`，15 個旅遊子主題存在。PostgreSQL 與 Redis 容器身分維持不變，應用映像、環境指紋及零重啟檢查通過，正式網站與 API 連續三次健康檢查通過。這是備份格式與索引驗證，未宣稱完成整庫還原演練。

未登入的 Windows / Edge 153.0.4234.32 正式站深度驗收檢查 300 個文章頁與 5 個總目錄頁：逐篇比對已發布文字及程式碼、複製結果、返回總目錄、語言替代連結及 390px 橫向溢出，並檢查目錄搜尋／單元條件的重新整理與瀏覽器返回。317 筆檢查通過，頁面腳本錯誤 0。另以 390px／1280px 抽查五語目錄與文章共 10 個組合，並檢查兩種寬度的獨立網站練習頁；錯誤 0。Codex 與 Claude Code 目錄帶查詢參數的直接請求都回 200，Claude Code 的搜尋與難度篩選在重新整理後保留，該互動頁不載入廣告腳本。正式驗收的[結構化收據](evidence/public-production-qa-2026-09-20.json)、[逐頁報告](evidence/public-depth-browser-2026-09-20.json)及[響應式報告](evidence/public-responsive-browser-2026-09-20.json)均可審閱，原件與備份另存於主機本次發布目錄。

公開測試曾遇到 11 次頁面 HTTP 429 與 1 次剪貼簿未更新；依正式站限流等待重試後，內容與複製值皆正確。響應式抽查另有 3 次 429 等待重試。繁中全站連結檢查尚有 11 筆既有非 Codex 問題，其他四語為 0；本系列五語均為 0。實體 iOS／Android、macOS 與 Linux 產品操作未親自實測，文章以官方文件查證並標示限制；Windows Edge 的響應式視窗不等於實體手機。
