# X03 Netflix｜免費稿件乾跑

**範圍：文字結構和本機檢查；沒有呼叫付費語音、插圖、評審或配樂，沒有成片。**

| 項目 | 目前結果 |
| --- | --- |
| 劇本版本 | `video.json` SHA-256 `b65241c55c35f6692cac89e3af4e5aa651b6664025c33890e497846346e722a4` |
| 編譯 | `node docs/videos/story-everyday-netflix-x03/compose-video.mjs` 產生 80 句、10 組伏筆、逐句來源矩陣；`node tools/video/cli.mjs script --slug story-everyday-netflix-x03` 產生可讀劇本 |
| 體裁與長度 | 六章；估計 9.1 分鐘、開場約 51 秒；**正式 TTS 尚未量時** |
| 畫面結構 | 65 個 `shot`、12 張後製 `big` 卡與 1 張 `outro`；插圖場景占 65/78 = 83.3%，超過 70% 規格；`look` 精確為 `{"preset":"cute-mystery"}` |
| 免費驗證 | `node tools/video/cli.mjs lint --slug story-everyday-netflix-x03`：0 錯誤、0 警告；`npm run test:docs-videos`：236/236 通過；`npm run check:tasks`：通過（僅全域既有任務警告） |
| 片頭片尾 | 製作規格固定：首章濃縮開場後插入 5 秒片頭；21 秒片尾的最後 17 秒保留左／右影片連結和訂閱鈕。正式頻道動畫素材、可點的 YouTube Studio 結束畫面及整檔時長均待媒體階段驗證。 |
| 聲音與字幕 | 單人台灣語調說書、無人聲配樂提示詞、可關閉繁中 CC 已在規格；音檔與字幕尚不存在。 |
| 成本 | 仍需先對 65 張 MiniMax `image-01` 插圖、80 句語音、轉錄、評審、配樂、重做與稅費做完整報價並守住 US$25 硬上限；**本輪實際付費 US$0**。 |

正式上架時，MP4 框線不等於可點連結；私人上傳後須在 YouTube Studio 放兩個影片項目與訂閱元素，並實點驗證。沒有正式片頭片尾檔案時，本收據不聲稱書擋或連結已通過影片級 QA。
