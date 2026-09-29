# 2026-09-29 Shorts 送審修正

新版本針對十二支「AI 與真實世界」長片精華的實際送審畫面修正安全區、字幕、片長與響度。
產物寫到 repo 外的新版本資料夾，不覆寫歷史 MP4、WAV、舊時軸或先前的審核收據。

## 修改內容

- 標題和卡片限制在 x=96–880，所有內容字形與外框逐一量測，必須位於 x=78–902、底部 y≤1380。
- 字幕以實際 Pillow 字形邊界和黑底邊界量測，底部低於 y=1600 並保留餘量；資料日期與合成旁白揭露移到內容區。
- 第一支用三張重點卡；第二支用大重點卡加三步上下文，`script.json` 的 `big`、`body` 如實描述畫面。
- 影像信任第二支標題改為「沒有來源憑證，就代表照片是假的？」，避免將 AI 標記與 C2PA 來源憑證混稱。
- Gemini 那一句以完整詞重新分句，沿用 Microsoft Hanhan Desktop 聲線，只重合成受影響的三個短語。
  其餘語音重用原始語音快取，記錄來源和新 48 kHz WAV 的 SHA-256。
- 自動旁白檢查標記的短語修正在 `shorts-repairs.json`，保留原句、改寫句與原因；重建前核對原句，
  同步更新新腳本、描述、字幕與對應語音。其餘語音不重錄。斷行避免標點出現在行首或獨占一行。
- 不足 26 秒的片尾保留最後一句與摘要卡供閱讀，不拉慢旁白、不新增事實主張。
- 音訊以兩遍 loudnorm 正規化至 −14 LUFS、目標 true peak −1.5 dBTP；完成 AAC 編碼後再次測量並完整解碼影音。

## 重建

需要 Python/Pillow、ffmpeg、ffprobe；Gemini 修補與 `shorts-repairs.json` 的逐句重錄會使用
Windows `System.Speech` 與 `Microsoft Hanhan Desktop`。`--source-media` 是保留的原始 `media` 目錄，須包含每支
`speech-input.json`、`timing.json` 和 `voice-cache`；`--import-root` 是原 `season1-import` 目錄。

```powershell
python docs/ai-video-season-01/tools/rebuild_shorts.py `
  --source-media '<原始製作包>/media' `
  --import-root '<原始 season1-import 目錄>' `
  --output '<repo 外的新修正版目錄>'
```

使用 `--only <slug1>,<slug2>` 指定重建，或 `--skip <slug1>,<slug2>` 跳過已完成影片。
`--repairs <檔案>` 可指定另一份逐句修正計畫；預設讀取此目錄的 `shorts-repairs.json`。
每次建立新時間戳資料夾。`completed-builds.json` 只列完成完整技術檢查的版本；每次執行另留一份 manifest。

每支原生 build 包含：

- `script.json`、`timeline.json`、`narration.txt`、`audio/000.wav` 等逐句音訊。
- `upload/final.mp4`、`upload/zh-TW.srt`、標題、封面、含雜湊的 manifest。
- `checks.json` 的逐 cue 實際 bbox、`layout-evidence.json` 的成片雜湊綁定、輸入及編碼後的響度紀錄。
- `audio-provenance.json` 的語音重用／重合成來源，`contact.png` 的編碼後九格取樣，`probe.json` 與完整影音解碼紀錄。

這是實際自有 renderer 的原生 build，所以 `checks.imported=false`；它不是把匯入品管的缺少測量旗標改掉。
字形與外框座標取自此次渲染，成片雜湊也綁定此次輸出。

工具不產生 `verify.json` 或 `check.json`，不呼叫正式站 API，不核准、不推送、不發布。
獨立事實查核與自動逐句旁白檢查必須對新 build 重新執行，人工聽審仍待站主；
來源長片尚無公開網址時，仍須保留連結待補的狀態。
