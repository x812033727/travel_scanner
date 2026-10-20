# Crocs 本機試看片

`local-preview.mjs` 只讀這集已生成的旁白、90 張關鍵影格、7 張渲染圖卡及配樂，在媒體工作區的 `review/local-preview/preview.mp4` 合成 **1920×1080、30 fps 的未審核試看片**。前 30–60 秒是濃縮開場，接著有 5 秒**本機概念片頭**；正文結束後有 21 秒**本機概念片尾**，最後 17 秒留兩個影片框與一個訂閱位置。兩段動畫畫面直接標明「本機概念試看片」，供檢查節奏和版位，**不是站主選定的正式素材**。字幕不燒進畫面。

正式頻道片頭、片尾及 `manifest.json` 留在主機的 repository 外；本機沒有取得它們，因此試片不能通過正式 branding QA。工具不執行正式 `clips`／`assemble`，不寫批准紀錄、`clips/manifest.json`、`checks.json` 或 `final.mp4`。正式成片仍須接入既定 5 秒片頭與 21 秒 v4 片尾，逐項驗收。

先在專案根目錄執行，`--workdir` 傳入**媒體工作區基底**，影片素材實際位於其下的 `story-everyday-crocs-c01/`：

```bash
node docs/videos/story-everyday-crocs-c01/local-preview.mjs --workdir /workspace/crocs-media --dry-run
```

顯示 `ready` 後執行：

```bash
node docs/videos/story-everyday-crocs-c01/local-preview.mjs --workdir /workspace/crocs-media
```

若要取代既有的試看片，加 `--force`。中斷後重跑會重用已完成、按內容雜湊命名的分鏡片段。需先以正常製作步驟完成 `tts`、`keyframes`、`render` 與 `music`；正式生圖與配樂仍須遵守整批預算核准。試片使用與正式合成器相同的運鏡、BT.709 編碼和配樂混音函式，並檢查輸出影格數與影音格式。概念片頭片尾另用同一首已授權配樂，不產生額外付費素材。

本集的四條 SEC 原始資料連結已列於 [`video.json`](video.json) 的 `sources`，正式上架包會自動把它們加進 YouTube 說明欄「參考資料」。片尾畫面上的影片框與訂閱位置**不是可點連結**；私人上傳後仍須在 YouTube Studio 最後 17 秒設定「最符合觀眾喜好」影片、訂閱、「最新上傳」影片，並在播放器實點驗證。試看片及本機稿件不能代替這一步。

工具會同時在試片目錄輸出 `preview.zh-TW.srt`、`preview.zh-TW.vtt`。字幕以實測 TTS 時間軸製作，片頭前維持原時間、片頭後延後 5 秒，可在播放器選開。正式 `captions` 指令須等正式品牌成片完成後再執行；本機字幕不是正式上架包。

## 2026-10-20 本機輸出紀錄

實際檔案位於 `/workspace/.brand-video-workdir/story-everyday-crocs-c01/review/local-preview/`：`preview.mp4`、`preview.zh-TW.srt`、`preview.zh-TW.vtt`。這些約 189 MiB 的媒體留在本次雲端工作區，沒有提交至 Git；上方命令可在持有已生成素材的工作區重建。`preview.mp4` SHA-256 為 `5ba761f9cb0b68cdaa96da4855b6c66e35cb0414f57c26a49a15bb1f1b432322`。

輸出有 19,553 格、影片長 651.77 秒：H.264 High、1920×1080、30 fps、BT.709；AAC-LC、48 kHz、雙聲道，整片約 −14.0 LUFS。第一章濃縮開場在 45.233 秒接 5 秒概念片頭，第二章第一句字幕於 50.233 秒開始；21 秒概念片尾從 630.767 秒開始，最後 17 秒保留結束畫面版位。109 則繁中字幕沒有時間或閱讀速度警告；抽查開場、片頭後、片尾卡位和最後一秒畫面均正常。這是本機技術 QA，仍待站主看片與正式頻道素材接入。
