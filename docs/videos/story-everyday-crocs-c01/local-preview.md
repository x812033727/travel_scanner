# Crocs 本機試看片

`local-preview.mjs` 只讀這集已生成的旁白、93 張關鍵影格、7 張渲染圖卡及配樂，在媒體工作區的 `review/local-preview/preview.mp4` 合成 **1920×1080、30 fps 的未審核正文試片**。它不執行正式 `clips`／`assemble`，也不寫批准紀錄、`clips/manifest.json`、`checks.json` 或 `final.mp4`。試片不含正式 5 秒片頭與 21 秒片尾；字幕不燒進畫面。

先在專案根目錄執行，`--workdir` 傳入**媒體工作區基底**，影片素材實際位於其下的 `story-everyday-crocs-c01/`：

```bash
node docs/videos/story-everyday-crocs-c01/local-preview.mjs --workdir /workspace/crocs-media --dry-run
```

顯示 `ready` 後執行：

```bash
node docs/videos/story-everyday-crocs-c01/local-preview.mjs --workdir /workspace/crocs-media
```

若要取代既有的試看片，加 `--force`。中斷後重跑會重用已完成、按內容雜湊命名的分鏡片段。需先以正常製作步驟完成 `tts`、`keyframes`、`render` 與 `music`；正式生圖與配樂仍須遵守整批預算核准。試片使用與正式合成器相同的運鏡、BT.709 編碼和配樂混音函式，並檢查輸出影格數與影音格式。正式成片仍須走分鏡審核、`clips`、`assemble` 與後續驗收。

如需選開的繁中 CC，可由目前的 TTS 時間軸另產生 `captions/zh-TW.srt`：

```bash
node tools/video/cli.mjs captions --slug story-everyday-crocs-c01 --workdir /workspace/crocs-media
```
