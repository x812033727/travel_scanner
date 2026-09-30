# Mokaair 頻道片頭片尾 v1 正式啟用紀錄

2026-09-30 03:31:00 UTC（台灣 11:31）完成部署與品牌預設啟用。新製長片採用 5 秒無標語片頭及 3 秒按讚、分享、開啟小鈴鐺片尾；既有影片保留自己的品牌選擇。本次現場沒有符合重製資格的成片，因此沒有重製影片、POST 成片審核、核准或發布影片。

**版本與部署證據**

| 項目 | 結果 |
|---|---|
| 實作 PR | [#1003](https://github.com/x812033727/travel_scanner/pull/1003)，03:20:32 UTC 合併 |
| 實際部署 merge SHA | `64f132e1c1d19deca9c8ea52c8ad8b76ebd3a8b8` |
| CI 通過的 PR head | `eb9541cbfc57ed36cf7a7521068fe3b7cd492885` |
| 兩者 Git tree | 均為 `2b263664afe84b1750fc50030be698c25f4bf06e`；diff 為空 |
| CI | 10 項均為 completed/success：api、web、containers、full-stack-smoke、food-map-reservations、planner-browser、lighthouse、discovery-browser、smoke、image |
| 部署前 SHA | `cb4d0b44572541fd9068bb469ef958ed752ce61a` |
| 執行 exit code | 首次 deploy `1`；經檢查的 deploy-resume `0`；activate `0`；finish `0` |
| worker image | `sha256:a86b96984a191affeace30b695af82b3ca9dbd9ede2ea2a9ae80bfaf4dd43440` |

首次部署在等待 worker 結束當前工作時，因 `docker top -eo args` 的程序欄位不符合主機需求而停止，尚未建立資料庫備份或切換版本。保留本次 hold／STOP 後，續跑先確認原 checkout、容器與映像均未改變，改用 `pid,args`，重新取得鎖並建立備份，再完成同一個 exact SHA 的部署。原 `/root/deploy-travel-scanner.sh` 未修改；執行的是經檢查、具 SHA 保護及 worker scale-zero 的副本。

新鮮 `pg_dump -Fc` 備份為 **169,594,264 bytes、mode 600**，已執行 `pg_restore --list` 及 checksum 驗證；沒有宣稱完成還原演練。SHA-256：`b4900eab84c452599f3fd587842e0a67ae4ecf3cf8d125767a4de58d080c6509`。備份本體只留在主機，未下載至本機或提交 repo；api、web、video-worker 的回滾映像保留於 `branding-rollback-64f132e1c1d1` tags。

收尾時 13 個服務容器均為 running。PostgreSQL、Redis 的 container ID 與 restart count 前後相同；其他服務隨部署更新。worker 已使用上述新映像恢復，本次擁有的 release hold 與 STOP 已清除。`alembic current` 與唯一 head 均為 **`0114_video_slides_media`**；此版本不包含後續 PR #996 的 0115 migration。health／ready 檢查完成，公開首頁回應 200。

**正式品牌預設**

安裝時間為 03:29:36.826 UTC，啟用階段於 03:29:38 UTC 完成。套件 `mokaair-brand-package-v1` 已通過素材 SHA 與媒體規格驗證，寫入正式 work volume 的 `_branding/current.json`。

| 項目 | 值 |
|---|---|
| branding hash | `0e1274bf0277762abb210e9e4c30848df88cd849c7af2d2630ee1c084e5b4e40` |
| 片頭 | 150 frames／5 秒；SHA-256 `96ad5f64030248403692d2f65cee4492abcd6ac3a4b7e71c5df8a1adea203b11` |
| 片尾 | 90 frames／3 秒；SHA-256 `8d9546a6042bdc30e0ac597d4eb1452d9e84edc588424027df8f7378ccecf6b1` |
| 規格與位置 | 30 fps；`/var/lib/mokaair/video-work/_branding/<branding hash>/intro.mp4`、`outro.mp4` |

worker 與部署 checkout 的 `tools/video/core/branding.mjs`、`tools/video/review/sync.mjs` SHA 逐一相同，確保單次維護與恢復後 worker 使用本次程式。

**重製範圍與驗收界線**

03:29:38.123 UTC 的即時盤點為 **21 protected／0 candidate／13 first-build**。原規劃候選 `gemini-connected-apps-permissions` 已成為 `publish-approved`，因此受保護、未重製。13 個 first-build 項目表示尚待首次製作，不代表已產出 13 支帶品牌影片。Shorts、已核准或已發布成片與六支已核准的匯入原片均未因本次啟用而重製；沒有更改全域自動核准政策。

由於沒有候選成片，本次沒有逐片 before/after 成片 SHA、字幕或配音重製、manual-review POST 或新的 pending review；這些項目為不適用，並非以空收據宣稱通過。

03:31:02 UTC 已在登入中的瀏覽器重新載入 `/zh-TW/admin/videos`，確認後台與影片清單可用，Gemini Connected Apps 顯示「on YouTube」。此次瀏覽器驗證只涵蓋已部署頁面與清單；**新的正式品牌成片播放器、手機播放及站主耳機聆聽尚未驗收**。素材的機械檢查與部署成功不替代上述播放驗收。

**外部證據索引**

主機紀錄根目錄為 `/root/mokaair-channel-branding-20260930-64f132e1c1d1`。去敏後的操作收據下載於 `~/mokaair-work/channel-intro-20260930/production-receipts/`；媒體、完整私有影片清單、帳戶材料與資料庫備份不納入 repo。

- 版本／瀏覽器：上層 `merged-pr-ci.json`、`browser-verification.json`；本地 Git objects 核對 tested head 與 merge tree。
- 部署／備份：`target.sha`、`before.sha`、`deploy.exit`、`deploy-resume.exit`、`deploy-source.sha256`、`predeploy.sha256`；主機另存 `predeploy.dump` 與 `predeploy.list`，大小及權限由執行者於主機核對。
- 啟用／收尾：`activate.exit`、`finish.exit`、`activation.json`、`completed.json`、`video-worker-image.id`、`worker-image.json`。
- 獨立收尾回讀：上層 `post-finish-checks.txt` 記錄 03:33:54 UTC 的實際素材 SHA、worker running／restart=0、hold／STOP 已清除，以及備份大小／權限、1,216 行 restore 清單與 checksum。四個 `*64f132e1c1d1.log` 保留初次部署、續跑、啟用和收尾輸出。
- 容器／migration：`containers-before.txt`、`containers-resume-preflight.txt`、`evidence/containers-after.txt`、`evidence/alembic-current.txt`、`evidence/alembic-heads.txt`、`evidence/public-health.txt`。
- 品牌／範圍：`evidence/branding-dry-run.json`、`evidence/branding-installed.json`、`evidence/current-branding-final.json`、`evidence/worker-source.sha256`、`evidence/checkout-source.sha256`、`evidence/live-inventory.json`。此處僅記錄必要統計與排除原因，不複製完整影片清單。
