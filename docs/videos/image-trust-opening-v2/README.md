# 照片信任：長片開場新版

本版把「選哪張照片」的真假測驗式包裝，改成「同一張圖如何因說明不同而被理解成不同故事」。這是第一支長片的獨立審片修改，不包含 Shorts。

標題：**照片是真的，故事就是真的？轉傳前先查這3件事**。

新開場第一段實測 **23.158 秒**；完整長片 **7 分 47.55 秒**，原版約 8 分 29 秒。沒有為了湊滿八分鐘添加旁白。91 段旁白中，75 段沿用原聲線的本機快取，16 段依新稿重新合成。最終數值與雜湊見輸出資料夾的 `technical-report.json`。

## 交付

- `long-video.json`：只含長片的稿件、逐句開場與畫面指示，沒有 shorts 欄位。
- `assets/thumbnail-v2.jpg`：1280×720、268,369 bytes 的審片縮圖。PNG 是 image_gen 原始輸出。
- `editorial-review.md`：修改理由、官方來源複核與驗收界線。
- `thumbnail-provenance.md`：使用的 image_gen 完整提示與來源紀錄。
- `local-artifacts.json`：本機產物的大小、雜湊與本輪驗證摘要；`assets/contact-sheet.jpg` 為抽幀紀錄。
- `build.py`：獨立重建工具，所有媒體與快取輸出到 repo 外。

本機媒體在 `C:/Users/x8120/mokaair-work/long-revisions/image-trust-20260929/`：

| 檔案 | 用途 |
| --- | --- |
| `preview-first30.mp4` | 快速比較新版開場 |
| `review.mp4` | 新版完整長片 |
| `contact-sheet.jpg` | 關鍵時間點的抽幀 |
| `captions.srt`、`timing.json` | 依實際語音長度重建的字幕與時間 |
| `upload-metadata.json` | 新標題、說明與章節 |
| `technical-report.json` | 解碼、時間、音訊與素材檢查 |

Git 不包含 MP4/WAV 或語音快取；讀取原審片環境的現有快取可節省合成。原版影片、既有後台核准與 Shorts 檔案均不被這個工具改寫。

## 重建

需要 Python/Pillow、ffmpeg、ffprobe 與 Windows System.Speech 的 Microsoft Hanhan Desktop 聲線。使用整季來源目錄只為唯讀取得既有助手、來源表和語音快取；工具先普通複製到新輸出資料夾，再載入副本。

```powershell
python -B docs/videos/image-trust-opening-v2/build.py --source-season "C:/Users/x8120/OneDrive/文件/ChatGPT/travel_scanㄐ/docs/ai-video-season-01" --output "C:/Users/x8120/mokaair-work/long-revisions/image-trust-20260929"
```

加 `--prepare-only` 只合成及量測旁白。新建輸出路徑可保存另一版本；不要指向原季別媒體或 Shorts 目錄。

## 審片與後續

已修正開頭、銜接段、呼應句和一張來源憑證卡片。其他中段仍沿用原本的圖解卡敘事；本版不代表整季最終剪輯完成。

技術通過不代表人耳聽審或上架驗收。需完整觀看／聆聽修訂版、確認合成內容揭露，再把新檔案與新雜湊送回正式審核。舊版核准不能當作新版核准。本次未替換正式後台、上傳 YouTube 或公開發布，也沒有可證明點閱提升的觀眾數據。

這份獨立審片包只輸出繁中旁白與字幕。正式版若已勾選其他語言，需依新版稿件重做相關翻譯、字幕時軸和配音；不能把舊語言包接到新片上。
