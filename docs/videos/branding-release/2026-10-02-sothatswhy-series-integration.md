# 原來如此系列片頭接入（2026-10-02）

站主在選定 6.9 秒加速穿插版後要求「接入」，並補充「也新增只有原來如此動畫可以搭配shorts」。

## 選擇與時間軸

`branding --series sothatswhy` 為原來如此建立獨立 current。新 `flat-explainer` drama
長片選用 357 格／11.9 秒合併開場，保留 90 格／3 秒原片尾。
其他長片使用全頻道 current；Shorts 保留原流程。既有 pin 與受保護影片不採新版本。
既有共用時間軸處理字幕、章節與外語音軌，字幕偏移 11900 ms，章節零仍為 0。
合集去除各集片頭後只加一次自己的片頭；現有合集無 explainer look，沿用全頻道設定。

## 已選素材

長片素材包：`~/mokaair-work/so-thats-why-intro-20261002/v2-7s-interleaved/approved/`。
bookends hash：`047ff12a4888185d8fb1cb0cd520f7a2e23b9c3538fe3f2e8d4cb35afb0720bb`。
媒體個別雜湊及站主選用原話見 [素材定案](2026-10-02-sothatswhy-intro-approval.md)。

Shorts 獨立素材位於同一外部工作目錄的 `shorts/`，採直式重新排版，沒有原頻道開場或片尾。
保留 14 個國家／地區、7 女聲與 7 男聲、配樂與後段加速穿插。
這份素材可供 Shorts 剪輯搭配；不代表已替既有 Shorts 重製或送入上傳排程。

## 驗證紀錄

使用 bundled Node 24.19.0 通過 13 個核心／安裝測試，涵蓋系列路由、disabled、pin、
已核准／已上傳保護、範圍隔離、來源竄改拒絕與 11.9 秒偏移。
完整 tools suite：1247 total、1244 pass、0 fail、3 環境 skip。
本機實際素材安裝完成，全頻道 current bytes 保持不變，新 explainer 選到 357 格。

實際媒體 smoke 把原素材包接在 300 格／10 秒測試正文前後：747 格／24.9 秒，
雙聲道每聲道 1195200 samples。逐段解碼比較 intro／body／outro 為 0 mismatch，
正文 SHA 不變；字幕為 11900–21900 ms，章節零為 0，保存接點截圖及完整 probe。
證據位於 git 外同一工作目錄的 `integration-smoke/evidence.json`、`approved/local-integration.json`。

Shorts 主檔 `shorts/so-thats-why-shorts-6.9s.mp4` SHA-256：
`d7a988cfc5d194078fff7c5c32fef48b9a74fa44cc1372c9cfbac4f906ead5bf`。
1080×1920、30 fps、207 格／6.9 秒，全片解碼與 Edge 原生播放到結束通過，
390 px 預覽無水平溢出；-14.0 LUFS、-1.8 dBFS peak。
另保留同尺寸音樂版、無聲版、可重現來源、manifest 及剪輯 ZIP。

程式 PR 為 [#1129](https://github.com/x812033727/travel_scanner/pull/1129)。
正式部署與安裝的實際結果以主機 `/root/mokaair-sothatswhy-intro-20261002/`
內的 `completed.json`、`installed.json`、`readback.json`、`routing-verified.json`、
來源 hash 對照及部署 log 為準；本機副本留在外部素材工作目錄 `approved/production-receipts/`。
安裝器檢查 merged commit 已在 live HEAD 內、worker image 來源 SHA 與 checkout 一致，
再以系列 CLI 安裝；全頻道 current 前後 bytes 必須相同，回讀後再次驗證新片路由與 11900 ms 偏移。
這些證據區分程式合併、部署與素材安裝，檔案存在前不描述為正式啟用。
素材選用與任何單支影片的 final／publish
審核仍分開；本次接入不重製既有影片、不生成新語音、不啟用 uploader，也不發布 YouTube 影片。
