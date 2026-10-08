機場英文系列：本機預覽

1. 完整解壓縮預覽包。請保留 START_HERE.html、lessons.js、播放器檔案與各 day 資料夾的相對位置。
2. 本機需 Python 3（https://www.python.org/downloads/）。在此資料夾開啟終端機，執行：
   python3 serve.py
   Windows 如沒有 python3 指令，可改用：py -3 serve.py
3. 開啟終端機顯示的 http://127.0.0.1:8765/START_HERE.html 網址。
   此服務只接受本機連線；播放不需連線至外部網站。
   若連接埠已被使用，可加上 --port 8768。
4. 終端機保持開啟。看完後按 Ctrl+C 結束。

直接以 file:// 開啟 HTML 不是支援的方式，請使用上述本機網址。
播放器支援英文主音軌、四語教學音軌及四語 CC。英文已固定顯示在影片內，
CC 顯示在影片下方專用區域；字幕和音軌可各自選擇。
切換集數會暫停播放並回到英文音軌，保留 CC、音量、靜音與播放速度。
如果替代音軌無法載入，播放器會切回英文，保留使用者的靜音設定。
此為本機檢視器；YouTube 音軌選單仍需頻道具備多語音軌功能且完成匯入。

給製作流程：
- 將此資料夾內的檔案與 lessons.js 放在預覽包根目錄，不必更改播放器程式。
- lessons.js 定義 window.LESSONS，陣列每一項格式：
  { day: 1, title: "本集名稱", master: "day01/master.mp4",
    audio: { "zh-Hant": "day01/zh-Hant.m4a", "zh-Hans": "day01/zh-Hans.m4a",
             "ja": "day01/ja.m4a", "ko": "day01/ko.m4a" },
    captions: { "zh-Hant": [[0, 3.5, "字幕文字"]], "zh-Hans": [], "ja": [], "ko": [] },
    chapters: [{ start: 0, title: "開場" }],
    files: [{ name: "master.mp4", url: "day01/master.mp4" }] }
- 字幕起訖以秒為單位；chapters 與 files 可省略。所有路徑皆相對於預覽根目錄。
- chapters 應從最終影片時間軸產生；播放器不自行假設章節時間。
- 不應將尚未通過製作檢查的影片標為正式完成。

回歸驗證（從 repository 根目錄執行）：
  node --test tools/video/airport_english/preview.test.mjs
  python3 tools/video/airport_english/preview/browser_check.py --bundle /path/to/unpacked-days-01-10 --report /tmp/preview-check.json
第二個指令需要 Python Playwright 與系統 Chromium。它使用臨時包裝目錄、
本機 HTTP 和原有 Day02/03 影音；不修改原有影片、不連外、不測試 file://。
功能測試通過不代表測試用影片已通過正式製作檢查。
