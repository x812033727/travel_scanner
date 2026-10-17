# M09 私人影片與四語試播讀回

2026-10-17 03:32 UTC，以本機影片工具權杖對 `GET /api/video/reviews/curio-m09` 做唯讀讀回；以下後台欄位與站主回覆分開記錄。

## 後台記錄

- 最新 `publish` 卡 `3fa63c7c-4b46-4289-bd68-7c629758b90b`，內容 SHA-256 `14939dccac842ff400c493301bbef04039cea00b6473c0b2e25f483a9fe94802`，狀態 `approved`；最新 `languages` 卡 `cc8e7ea3-3164-466c-8ee1-473850532ecd`，內容 SHA-256 `db2141c20319dde0dde300e3c38300a3a53c6b63d0aa02691b6849ca6945749f`，狀態 `approved`。兩個雜湊與本機已拉回的核准相符。
- `stage=on YouTube`，`youtube_video_id=yGF95x3O9U0`，`youtube_publish_at=null`。後台影片連結可由此 ID 組成：<https://www.youtube.com/watch?v=yGF95x3O9U0>。
- `youtube_sync.status=done`，完成於 2026-10-17 10:06:32（台灣時間）。該請求的 `mode=upload`、`visibility=private`、`accept_private_lock=true`；上傳步驟註明「專案還沒通過稽核，YouTube 會鎖成私人」。因此後台證據顯示由網站 API 上傳、目前私人鎖定，不足以稱為 Studio 上傳或已排程／公開。
- 同一筆同步的 `details`、繁中／英／日／韓 `captions`、主縮圖步驟均記為 `done`。英／日／韓的 `dub` 各記為 `uploaded`；這是後台操作狀態，API 無法獨立驗證 Studio 音軌播放。

## 站主試播回覆與未解的對位

站主回覆「已上傳並四語試播正常」。這是站主對四語播放的驗收，與上面的後台同步狀態分開；本次未取得站主試播頁的影片 ID 或 Studio 畫面，因此尚不能獨立證明試播的是後台 ID `yGF95x3O9U0`。後續交接只需核對這個 ID 與站主試播的影片相同；本次不替站主進入 Studio 或更改發布設定。

本機 `docs/videos/curio-m09/video.json` 的 `youtube.video_id` 仍為 `null`，故本機 `status --slug curio-m09` 暫列 `[ ] on YouTube`。這是本機 ID 同步缺口，不推翻後台持久化的影片 ID；避免改動現版已核准稿件，本次只記錄差異，不修改 `video.json`。另有手動影片 ID 同步任務處理此類缺口。
