# S05 本機長片與上傳包驗收（2026-10-20）

現行 `final.mp4` 與 `upload/final.mp4` 的 SHA-256 同為 `349e716a174dd5fa28ab8ac687b426f04d3a0e665ede3d7a4b1a822be85eb5c6`。影片 1920×1080、30 fps、18,524 格、約 10:17.5；音訊整體 -14.1 LUFS，真峰值 -1.9 dBFS。`checks.json` 的 `ok=true` 且 `problems=[]`，品牌 pin 為 `d15370edfc0760da6e23f10a80f080ae4b8f6311b191ddc0a45a1f93beb23340`。

獨立唯讀抽驗者從**現行 MP4**抽出 13 個原尺寸畫格，確認 46.27 秒濃縮開場後接 150 格／5 秒原創片頭，21 秒／630 格片尾從故事結束後開始，最後 16 秒兩個影片框與訂閱圓框清晰保留至片末；音訊接點沒有異常長靜音。抽驗圖保存在 Git 外的 `/workspace/.video-work/curio-s05/review/bookends-contact.jpg`。片尾框是影片畫面，**可點區尚未安裝**；`upload/UPLOAD.md` 列出私人上傳後匯入 Studio 範本 `oxEtlA8GWas`，三元素由 `10:01:14` 到 `10:17:14` 的步驟。

繁中 SRT 有 104 條，片頭 5 秒沒有錯放字幕；六章時間碼為 00:00、00:51、03:07、05:45、06:36、08:41。`qa` 為 **10/11**：頻道網址 `https://www.youtube.com/channel/UCR0rRWT4blMDUwEMx-TZ57Q` 在本雲端遭 CONNECT 403 而無法開啟，其餘項目通過；固定版《三國志》史料網址另已查核。上傳包 `package` 為 **4/4**，`upload/metadata.json` SHA-256 `9aaf8e8328fcfe87e0972087844a5416781fdd9099fe4f721709e183fee744b0`；包內有現行 MP4、縮圖、繁中字幕、說明欄及章節、頻道與史料 URL。

站台 `review-push --gate final` 與 `--gate publish` 都以 `hand_pushed` 提交並回報 **pending，等站主在 /admin/videos 決定**。為依本對話「用推薦的決定，不用問我」繼續做完本機交付，代理在上述 QA 與獨立抽驗後，以註記記錄了現行 MP4 的**本機委派 final 驗收**，才執行 `package`；這不聲稱站主親自看過、站台 final/publish 已核准、已私人上傳，或有可點的 YouTube 片尾元素。待站台決定及私人上傳後，須以真實網址回填並複核本集 Short。
