# S05 插圖、敘事與分鏡送審收據

2026-10-20。此收據綁定 `video.json` SHA-256 `361d2836d0891a6994383cafb576c8761523056ddd7840f7b748000a5777e863`；劇本 SHA-256 `8e9632a4d1cce5a25a2876db16ea8d7c66de1d5d0544c367541b2cd845ae8121`，旁白 WAV SHA-256 `3abbbf59d17d87cb6e1b4445b0198cd081cf71bce0cad1068ad030361d3514d0`，時間線 SHA-256 `8ce9fe5b9e928298ac7f7dcc5e867dbaa7ea3239782c9369fb1e6cdaa1e878c1`。`lint` 為 **0 errors、3 個反覆人物／年代提示詞警告**；提示詞中的 `timber`、`late`、`adult` 用來限制已觀察到的時代與人物漂移。

## 插圖與來源界線

最終 keyframes manifest SHA-256 `6209e55e8fa48a89c199d12348e18ae9c47f30684396825b7245e303737e7344`；**78/78** 插圖已有選片、`needs_review` 為零。88 個訪談分鏡中 78 景為插圖（88.6%），另 10 景為可追到固定《三國志》卷三十五的來源／短引文卡，最多連續兩張卡。各景選片經原生尺寸人物、動作、古代物件、假字與時代背景覆核；大眼與短身是系列卡通畫風，沒有單靠此點付費重畫。來源卡 `visit-020` 引 `因屏人曰`，取代帶現代徽記的失敗圖。其餘卡的引文與解說、所有修補後提示詞在套入前經獨立 exact SHA 審核。口播、場景順序與時間線未因插圖修補而變。

`visit-057a` 的最終付費重畫仍出現吊燈、後世櫃子、裝飾性懸掛卷軸等錯置；改用相距 20 景的 `visit-071` 已通過原生尺寸查核之同主題圖。兩景共用圖片 SHA-256 `f0cd188a0585ddac0849f85d3ca5fa4b1fd0119bdb84d0d5aa942d6f4e4a1216`，畫面是一位裴松之時代的註者對照兩份分開、沒有字的書卷，不暗示兩份完整實物仍存或已知先後；只逐字複用該景 prompt／camera，快取重新驗證 `visit-057a` 得 9.29/10，**沒有新的付費圖片**。其餘最後修補 `visit-065`、`visit-065a` 分別經原生尺寸覆核：散置葦席、無浮水印，以及人物背向穿過無字土牆城門；第二景評審 10/10。末輪獨立原尺寸審核已清空史料／材質 HARD 問題。

媒體帳本 `media/ledger.json` 計 **US$2.321**，含 165 個 ready 圖片請求 US$0.5775、166 次 judged US$1.66、既付配樂 US$0.08，以及 2026-10-19 的舊 `visit-002` reserved US$0.0035。該舊預留不是成品，也未擅改帳本；保守合計仍低於整集 **US$3.56** 上限。最後一次帳本動作是 `visit-057a` 的快取評審，沒有待啟動的新 S05 圖片請求。

## 敘事與畫面關卡

10 景字卡改變視覺敘事指紋後，舊敘事收據確實過期。另一位讀者只讀現行劇本和正式問題，先封存 13 題答案，再由 `narrative --answers` 對本頁精確 `video.json` 產生 **round 26，13/13 通過、0 failed、0 advisory**；正式收據 SHA-256 `43ea7ae81a2dca84862eeeb94a282ce03daefc3ccbc684267f4ab5465b165035`，答卷 `/tmp/curio-s05-final-blind-answers.json` SHA-256 `0979394e755ffc7f5e9ab728c346107a58a506e2cf668360e1e5da80bfa85b3e`。讀者披露此前偶然看過本集預算片段與一個插圖例子，但未讀本集劇本、來源、claims 或舊敘事評語；本輪判斷仍只依劇本／正式題目。`status` 目前顯示 storytelling panel passed；原有 97/97 旁白零標記與本機音訊核准仍綁定未改的時間線。

`render` 產出 11 個文字畫面與縮圖。聯絡表 `/workspace/.video-work/curio-s05/contact-sheet.png` SHA-256 `18f9217ade246863f963b1025bcfa7e894d07b4eec3b266f56ae5bfcdf70b11d`；縮圖 `/workspace/.video-work/curio-s05/thumbnail.jpg` SHA-256 `664de30a9ed07806dce466d5365ea8561ad93847ee651590b7d71c931185794f`。縮圖畫面與文字已目視檢查，左下 `MOKAAIR` 是模板既有頻道品牌字，不是生成的歷史文字。`review-push --gate storyboard` 已送站台，`review-pull` 仍回 **waiting for the owner**；`clips --dry-run` 因此拒絕進入製片。這是站台真實待審狀態，不能用本地偽造核准替代。畫面批准後再生成 clips、組裝、字幕、完整 QA 與上架包；尚未宣稱成片完成。

開場第一章實測 1,388/30 幀＝46.27 秒，可作片頭濃縮段。現有本機原創品牌素材是 150/30 幀＝5 秒 intro（SHA-256 `a5ae205fcf6fa7c92998ac4991225e54206fff482cf03493a60cfb2519e8fcef`）與 630/30 幀＝21 秒 outro（SHA-256 `275475470f1b7b5d93a2948f561d6e300d0406f9a5b2ab17cfb0dfe4bb3f34ee`，最後 16 秒預留 YouTube Studio 元素）。這些素材**尚未組入 S05 final**；分鏡核准後須驗證 intro 在第一章後、outro 尾段、配樂循環接點、字幕及說明欄來源／頻道連結與 UPLOAD 時碼。
