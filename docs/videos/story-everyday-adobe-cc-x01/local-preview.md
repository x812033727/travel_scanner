# X01 Adobe Creative Cloud｜本機概念試看片

`local-preview.mjs` 會從本集旁白、74 張 MiniMax 關鍵影格、13 張後製卡與一首配樂合成 1920×1080／30 fps 試看片。最終 TTS 正文時間軸是 **18,076 影格／602.53 秒**；第一章濃縮開場是 **1,577 影格／52.57 秒**，後接 5 秒**本機概念片頭**。正文後接 21 秒**本機概念片尾**，最後 17 秒顯示左右兩個影片框及訂閱版位。兩段動畫均在畫面上標示「本機概念試看片」，繁中字幕輸出為獨立 `.srt` 和 `.vtt`，不燒進畫面。

正式頻道片頭、片尾及其 manifest 位於本雲端取不到的主機工作區。本機工具不寫 `clips/manifest.json`、正式核准紀錄、`checks.json` 或 `final.mp4`。正式工人接手時，須換成站主選定的同長度動畫，再完成正式音訊與成片 QA；若動畫長度改變，字幕也須依最終時間軸重算。

在儲存庫根目錄執行，`--workdir` 是**媒體工作區基底**：

```bash
node docs/videos/story-everyday-adobe-cc-x01/local-preview.mjs --workdir /workspace/.brand-video-workdir --dry-run
node docs/videos/story-everyday-adobe-cc-x01/local-preview.mjs --workdir /workspace/.brand-video-workdir
```

中斷後重跑會沿用按內容雜湊命名的已完成分鏡片段；只有要取代既存整支試片時才加 `--force`。素材須先完成 `tts`、`check-audio`、`keyframes`、`render` 和 `music`。本機合成器沿用專案的運鏡、BT.709 色彩及配樂混音設定（-20 dB 背景、旁白時再壓 10 dB），並在輸出時核對影格數與影音格式。概念片頭片尾重用本集配樂，不另買一首。

四份 SEC 原始申報已在 [`video.json`](video.json) 的 `sources` 與 YouTube 說明欄；逐句矩陣與獨立審核分別見 [`source-matrix.md`](source-matrix.md) 和 [`reviews/verify-1.md`](reviews/verify-1.md)。試片畫出的影片框與訂閱鈕版位**不會在 MP4 內自行變成可點連結**；私人上傳後，須在 YouTube Studio 最後 17 秒設定「最符合觀眾喜好」、「最新上傳」及訂閱鈕，實際點擊驗證。WebVTT 字幕依實測 TTS，在概念片頭後延後 5 秒。

第二輪逐句自動複查仍有 4 句近義轉錄差異，見 [`reviews/audio-check.md`](reviews/audio-check.md)。本機試片僅供檢視敘事、畫面、字幕與版位；音訊沒有人工聽核，不作正式 QA 通過宣稱。

## 實際輸出與核驗

2026-10-20 本機概念版已輸出至 `/workspace/brand-story-preview/adobe-x01/`：`preview.mp4`、`preview.zh-TW.srt`、`preview.zh-TW.vtt`、`thumbnail.jpg`、`contact-sheet.png`。此路徑是雲端工作區的交付檔，不屬於 Git PR 內的二進位影片；可重跑上方命令，原始合成檔留在 `/workspace/.brand-video-workdir/story-everyday-adobe-cc-x01/review/local-preview/`。

| 檔案 | SHA-256 |
| --- | --- |
| `preview.mp4` | `66de600b1cd48a635f1543a1088a7e6dc45713fb4debe2c8eb1730d6aef08d3e` |
| `preview.zh-TW.srt` | `6df0e2eb233b3244d8202d9f9c18a4da009b7c240fd45f334240e1a2c2635368` |
| `preview.zh-TW.vtt` | `323ecc75a1939432f9aa89bba8dcb621b81fbcd0fbfb7c2111be007569d8075d` |

FFprobe 量到 18,856 影格／30 fps（影像 628.53 秒；容器 628.60 秒）、1920×1080 H.264 High／yuv420p／BT.709，雙聲道 48 kHz AAC；SRT、VTT 各 96 則，和現行時間軸重新產生的字幕逐位元相同，漏句 0、時序或閱讀速度警告 0。整支 `ffmpeg -xerror` 影音解碼無錯誤；整體音量 −14.0 LUFS、真峰值 −0.9 dBFS，符合專案的 −14±1 LUFS／≤−0.5 dBFS 目標。最終畫面選圖 74 張、後製卡 13 張的靜態覆核見 [最終視覺 QA](reviews/final-visual-qa.md)；獨立整檔與實際 MP4 抽圖紀錄見 [試片 QA](reviews/local-preview-qa.md)。四句近義轉錄旗標仍待人工聽核，這份技術 QA 不代表正式音訊或上架核准。

目前可見媒體台帳為 225 次圖片請求（224 次完成、1 次逾時／失敗）、224 次評審與 1 首配樂，合計 **US$3.104**。此數字不含尚未拆帳的語音、轉錄、模型複查、稅費或供應商可能追列的逾時請求，不能稱為全片結算費用；整支 US$25 上限仍以最終帳務核對。[成本紀錄](production-quote.md)列出細項。
