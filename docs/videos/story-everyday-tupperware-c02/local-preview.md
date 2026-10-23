# C02 特百惠｜本機試看片

`local-preview.mjs` 從本集已生成的旁白、84 張關鍵影格、8 張資料卡和配樂，合成 **1920×1080、30 fps 的本機試看片**。實測旁白時間軸為 18,389 影格（約 10 分 13 秒），第一章濃縮開場約 45 秒；開場後插入 5 秒**本機概念片頭**，正文後插入 21 秒**本機概念片尾**。片尾最後 17 秒留兩個影片框與一個訂閱位置。兩段動畫均在畫面上明示「本機概念試看片」，不是站主選定的正式頻道動畫。繁中字幕另附 `.srt` 和 `.vtt`，不燒進畫面。

正式頻道片頭、片尾及其 `manifest.json` 位於目前拿不到的主機工作區，故本機試片不能通過正式 branding QA。這個工具不執行正式 `clips`／`assemble`，不寫批准紀錄、`clips/manifest.json`、`checks.json` 或 `final.mp4`。正式成片仍須替換成站主選定的 5 秒片頭與 21 秒片尾，再做正式驗收。

在儲存庫根目錄執行，`--workdir` 應傳入**媒體工作區基底**：

```bash
node docs/videos/story-everyday-tupperware-c02/local-preview.mjs --workdir /workspace/.brand-video-workdir --dry-run
node docs/videos/story-everyday-tupperware-c02/local-preview.mjs --workdir /workspace/.brand-video-workdir
```

中斷後重跑會重用按內容雜湊命名的已完成分鏡片段；取代整支已存在試片需加 `--force`。素材須先以正式步驟完成 `tts`、`check-audio`、`keyframes`、`render` 和 `music`。試片使用專案合成器的運鏡、BT.709 色彩與配樂混音函式，並在輸出時核對影格數與影音格式。概念片頭片尾重用本集配樂，不再另買一首。

七份 SEC 原始文件網址已在 [`video.json`](video.json) 的 `sources` 與 YouTube 說明欄稿中；來源矩陣見 [`source-matrix.md`](source-matrix.md)。試片片尾的影片框和訂閱位置**無法點擊**；私人上傳後，須在 YouTube Studio 最後 17 秒設定「最符合觀眾喜好」影片、「最新上傳」影片與訂閱鈕，並在播放器實點驗證。字幕會根據實測 TTS 時間軸，在概念片頭後延後 5 秒；正式片仍要用最終品牌動畫重新核對時間。

旁白自動檢查目前尚有十句待核，其中三句的自動轉錄可能改變原意；逐句證據見 [`reviews/audio-check.md`](reviews/audio-check.md)。本機試看片因此僅供檢視敘事、畫面、字幕與版位，不表示音訊已通過正式 QA。正式交付前，須先聽核這些短音檔，再按結果重錄或取得合格的獨立核對。

## 2026-10-20 實際輸出與核驗

- 試片：`/workspace/brand-story-preview/tupperware-c02/preview.mp4`（163,204,884 bytes；SHA-256 `f146606206290086cec6215f46250bf0cbaf6ec3e3795950deac1e82eaa1f9da`）。原始輸出留在媒體工作區 `review/local-preview/preview.mp4`，不進 Git。
- 縮圖：`/workspace/brand-story-preview/tupperware-c02/thumbnail.jpg`（SHA-256 `f63c6de3797e381ec8e7235261c8ea685e01ef463975e61177160e14f63655d4`）。初版縮圖裁切後保鮮盒不明顯，已改用 `c02-b19-s04` 的現成插圖，重新渲染並目視確認盒子入鏡；84 張原選圖全部重用，沒有新增圖片費。
- 繁中 CC：`preview.zh-TW.srt` 與 `preview.zh-TW.vtt` 各 **119 則**，產生器報 **0** 個時序或閱讀速度警告。SRT SHA-256 `90c91afa9e983bb954f1e547150b1965b529acf764ba23747590e3db528fdb34`；VTT SHA-256 `4207c52d32f9141d7480f95bd4767dff1c462751e579e24a4284d6175ca4ed0a`。兩檔已複製到上列交付目錄。
- `ffprobe`：H.264、1920×1080、30 fps、BT.709，**19,169 影格＝10:38.97**；AAC 雙聲道 48 kHz；MP4 容器時長 **10:39.00**。第 46 秒片頭、第 620 秒片尾、第 636 秒影片卡版位已抽圖目視確認；片頭及片尾結束畫面有本機概念版與 YouTube Studio 設定提醒。`ffmpeg -v error -xerror -i preview.mp4 -f null -` 整檔影音解碼零錯誤；這不表示旁白已通過正式音訊驗收。

可見媒體台帳為 **US$2.3615**：170 次圖片請求 US$0.5915、169 次插畫評審 US$1.69、一首配樂 US$0.08；語音、轉錄與其他未拆帳費用仍不得算成零，詳見 [`production-quote.md`](production-quote.md)。
