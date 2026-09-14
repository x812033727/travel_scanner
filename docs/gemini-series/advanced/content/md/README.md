# Gemini 深入教學：MD 與 CLI 設定實驗

[返回深入系列課綱](../../README.md)

本批為第 69–74 篇的完整原稿、內容包、配圖與下載練習。六篇已在本機建置並完成文字、連結與素材檢查；仍是未公開內容，正式 Gemini 目錄維持原本 50 篇。

| 篇號 | 教學原稿 | 讀完能做到 | 本機證據 |
| --- | --- | --- | --- |
| 69 | [GEMINI.md 載入實驗](69/lesson.md) | 分開判讀全域、專案、JIT、show 與 reload | 五組載入觀察 |
| 70 | [團隊規則範本](70/lesson.md) | 拆分規則、驗證引用與測試入口 | 正常與故障四組 |
| 71 | [settings.json 設定除錯](71/lesson.md) | 從實際有效值追到來源與錯誤 | 八組設定案例 |
| 72 | [自訂 CLI 指令庫](72/lesson.md) | 建立審查、測試計畫與文件比對指令 | 三命令、十八組參數展開 |
| 73 | [技能與擴充套件打包](73/lesson.md) | 檢查文件、管理兩個套件版本 | 三種腳本結果與模組生命週期 |
| 74 | [大型專案上下文](74/lesson.md) | 限定修改範圍、保留草稿、記錄恢復點 | 故障測試、參考修正與 Git 差異 |

每篇正文 2,282–2,657 字，皆有四階段操作、故障練習、三個 FAQ、正文互連與返回總目錄。六組封面及圖解為原創 SVG，另有 1600×900 JPEG 封面與 360px 預覽。SVG 是教學概念圖，沒有偽裝成官方 UI 截圖。

## 下載與驗證

- [第 69 篇練習包](examples/lesson-69.zip)
- [第 70 篇練習包](examples/lesson-70.zip)
- [第 71 篇練習包](examples/lesson-71.zip)
- [第 72 篇練習包](examples/lesson-72.zip)
- [第 73 篇練習包](examples/lesson-73.zip)
- [第 74 篇練習包](examples/lesson-74.zip)
- [六組練習與可重做的 CLI 模組驗證](examples/md-verification.zip)

下載包已核對 CRC、每個檔案與作者來源一致，並解壓最後一包重跑實際驗證程式。結果見 [delivery.json](verification/delivery.json)、[local-cli.json](verification/local-cli.json) 與 [重做方式](verification/README.md)。合計 48 筆分步觀察，使用 Windows、Node 24.19.0、Gemini CLI 0.59.0，沒有雲端模型呼叫。

本批審閱快照見 [authoring-review.json](verification/authoring-review.json)，逐張圖檢紀錄見 [visual-review.json](verification/visual-review.json)。快照核對六篇內容包、原稿、公開資產副本及 ZIP 的雜湊，不是整套發布許可或網站驗收紀錄。

## 發布前仍要完成

1. 補驗第 72 篇的三個模型回答、第 73 篇的模型技能觸發，以及第 74 篇已登入會話的恢復。本文已清楚分開實測結果與官方文件操作。
2. 複驗 Windows 的原生 `gemini extensions` 終端入口。曾先印成功文字，再因 libuv 斷言以非零狀態退出；[失敗紀錄](verification/native-cli-limitations.json) 保留原結果。實際 ExtensionManager 模組測試成功，不能當成終端異常已解決。
3. 跟其餘五批文章一起整合正式 catalogue、公開開關、導覽與整套發布驗收。不要從本批工具通過推論 36 篇都已完成。

不同 CLI 版本與 macOS／Linux 尚未實機測試。第 71 篇提供升級比較方法，沒有捏造第二個 CLI 版本的測量結果。資料庫整合測試中需要隔離 PostgreSQL 的 15 項在本環境跳過，其餘相關 31 項通過。

## 作者重新建置

```powershell
& apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py --track md
node tools/gemini-series.mjs check --draft --track md
```

原稿資料夾已附審閱後的 hero.jpg，可不重新啟動瀏覽器。改 SVG 時再使用 `--render` 與 `render-art.mjs --track md`，重新逐張檢視。修改練習資料後須重跑 CLI 驗證、產生下載包、檢查解壓執行，再重建內容；不要讓網站上的 ZIP 停留在舊版本。

完整工具說明見 [內容建置文件](../../platform/README.md)。本批驗收與未完成項目持續保存在對應 MD 任務票，沒有把未驗證的操作標成通過。
