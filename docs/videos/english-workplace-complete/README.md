# Sunny 與 Pip：職場英文系列

四季、每季 12 集，共 48 集原創英文微課程，承接高中階段的閱讀、推論與寫作能力。每集設計約 3–5 分鐘，重點是具體情境中的表達與判斷；四個階段依主題與先備能力選擇，不等同特定年級、職級或完整專業課程。

目前原稿已合併、凍結並完成交叉審稿；影音製作與最終封裝驗收仍在進行。下列檔案數、頁數與格式是交付要求，不代表所有成品已完成。最終完成情況應核對輸出目錄中的驗證報告。

[課程序列](planning.txt) · [製作契約](authoring-contract.txt) · [完整原稿](lessons.json) · [作者交叉審稿紀錄](authoring-review.json)

## 學習內容

| 季別 | 集數 | 主題 | 內容 |
| --- | --- | --- | --- |
| 第 1 季 | 01–12 | 求職與入職 | 職缺判讀、履歷證據、面試、角色與入職優先順序 |
| 第 2 季 | 13–24 | 日常職場溝通 | 郵件、進度、期限、會議與顧客服務 |
| 第 3 季 | 25–36 | 協作與問題處理 | 交接、依賴、風險、回饋、範圍變動與復原計畫 |
| 第 4 季 | 37–48 | 提案簡報與職涯發展 | 選項比較、建議、執行、問答、資源與職涯發展 |

每集 10 幕，包含兩段引導跟讀、三題聽讀選句與複習；每季最後一集整合前面內容。一般回應等待五秒，聽讀選句等待六秒再揭答。選句時可以看見英文選項，屬於有提示的聽讀練習，不作獨立閱讀或純聽力評量。

課後另有一篇 140–180 詞閱讀、三題獨立理解／分析題，以及 100–140 詞寫作任務與例答。人物、組織、事件與數據均為原創虛構或明示的假設案例；不使用真實個資、客戶資料或內部紀錄。責任分工、核准流程與服務規則都限定在例子的虛構組織；真實工作需確認所屬單位的規定。課程不保證求職結果，也不取代專業證照或企業特定訓練。

## 預期交付與使用

輸出位於 `/workspace/workplace-series-output`，影片、音訊、字型、快取與 ZIP 均不加入公開 Git。

- 四個分季 ZIP：`Sunny_Pip_Workplace_Season_01.zip` 至 `Sunny_Pip_Workplace_Season_04.zip`；每包 12 集、209 個檔案。
- 全集 ZIP：`Sunny_Pip_Workplace_48_Episodes.zip`；48 集、821 個檔案。
- 各包含離線 `index.html`、使用說明、課程目錄、`Practice.html` 與 `Practice.pdf`。全集目錄為 `職場英文48集課程目錄.csv`，分季為 `本季課程目錄.csv`，皆使用 UTF-8 BOM。
- 每集 17 個檔案：`final.mp4`、無聲 `picture.mp4`、`poster.jpg`、`checks.json`、五個 M4A，以及四語各一份 SRT 和 VTT。
- 成片為 1280×720、H.264、30 fps；畫面以 15 fps 渲染後編碼。每集有英文、繁體中文、簡體中文、日文、韓文五音軌，以及繁中、簡中、日文、韓文四種 CC。英文固定顯示在畫面，沒有英文 CC；四語教學聲軌使用相同的英文示範音訊片段。
- 全集 PDF 145 頁：封面 1 頁、48 頁閱讀與理解、48 頁寫作、後置答案 48 頁。每季 PDF 37 頁；活動與答案分開，全文共 48 篇閱讀、144 題問答及 48 項寫作任務。開放式回答與寫作例答並非唯一正解。

完整解壓縮後保留資料夾結構，以瀏覽器開啟 `index.html`；配音與 CC 可獨立選擇。也可用 VLC 開啟 `epXX/final.mp4` 切換音軌與字幕；瀏覽器若限制本機音訊，可改用 VLC。試製使用 Microsoft Edge 合成聲音，尚未接入後台正式配音，也未在後台發布。

## 重製流程

以下命令從 repository 根目錄執行。需要 Python 3.10+、PATH 中的 `ffmpeg`／`ffprobe`（H.264、AAC 支援）、Pillow 或 Pillow-SIMD、`edge-tts`、ReportLab。PNG／SVG 圖表功能另需 Matplotlib；本套凍結原稿未使用圖表。畫面需 `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` 與 `DejaVuSans-Bold.ttf`，PDF 需靜態繁體中文 TrueType 字型。

本次環境從 `/tmp/preschool-simd` 與 `/tmp/preschool-tts` 載入 Pillow-SIMD 12.1.1.post0、edge-tts 7.2.8，並使用 ReportLab 4.4.9；圖表環境另備 Matplotlib 3.10.8。這些 `/tmp` 路徑不隨 repository 提供；其他環境須先安裝相應套件與字型，再調整 `PYTHONPATH`。渲染器、相依原始碼、字型及繪圖函式庫版本受指紋約束，變更後須重新渲染與驗證受影響的產物。

```bash
cd /workspace/travel_scanner
export PYTHONPATH=/tmp/preschool-simd:/tmp/preschool-tts:tools/video
export ADULT_SOURCE=docs/videos/english-workplace-complete/lessons.json
export ADULT_OUTPUT=/workspace/workplace-series-output
export ADULT_ENGLISH_PRACTICE_FONT="$ADULT_OUTPUT/.fonts/NotoSansTC-Regular.ttf"
```

先驗證完整作者稿。這一步不需要網路或第三方 Python 套件。

```bash
python3 -S -m adult_english.verify_series \
  --source "$ADULT_SOURCE" --course workplace --structure-only
```

共用 `preschool/audio.py` 的 CLI 說明仍保留舊 preschool 名稱，但會讀取指定的成人原稿並保留課程識別。先以 `--plan-only` 產生計畫而不連線；移除該旗標才會透過 Edge 產生音訊、量測時長並寫入 `lessons.resolved.json`。同一輸出目錄只啟動一個音訊程序，兩套課程使用各自的目錄與快取。

```bash
python3 tools/video/preschool/audio.py \
  --source "$ADULT_SOURCE" --output "$ADULT_OUTPUT" \
  --cache-dir "$ADULT_OUTPUT/.tts-cache" --plan-only

python3 tools/video/preschool/audio.py \
  --source "$ADULT_SOURCE" --output "$ADULT_OUTPUT" \
  --cache-dir "$ADULT_OUTPUT/.tts-cache"
```

在音訊完成後執行批次渲染，或在另一個終端重新設定上方環境變數後以 `--watch-audio` 同時等待已就緒的音訊。批次最多三個 worker，重跑會驗證來源與成片雜湊後才略過已有產物。

```bash
python3 -m adult_english.batch \
  --source "$ADULT_SOURCE" --output "$ADULT_OUTPUT" --course workplace \
  --workers 3 --fps 15 --watch-audio --wait-timeout 7200
```

兩個製作程序都成功結束後，執行嚴格的 48 集驗證，再封裝四季及全集。`--resolved` 必須指向同一輸出目錄的量測稿；封裝會再次檢查目前作者稿、課程識別、音訊、字幕、成片與練習內容。不要在最終交付命令中加入 `--allow-partial` 或 `--seasons-only`。

```bash
python3 -m adult_english.verify_series \
  --source "$ADULT_SOURCE" --output "$ADULT_OUTPUT" --course workplace

python3 -m adult_english.package_series \
  --source "$ADULT_SOURCE" --resolved "$ADULT_OUTPUT/lessons.resolved.json" \
  --output "$ADULT_OUTPUT" --course workplace
```

作者逐季製作時，可對完整單季稿使用 `--structure-only --allow-season-subset`；串流批次亦有 `--allow-season-subset`，但這些模式不表示完成全部 48 集。兩套課程都使用 `ep01`–`ep48`，必須維持各自的 `course`、輸出目錄與快取，不可互換檢查紀錄。

## 驗證範圍

離線回歸測試可用 `node --test tools/video/adult_english/pipeline.test.mjs` 執行；它呼叫 Python `-S` 測試，不需 Pillow、ReportLab、網路、TTS 或影音編碼器。正式成品另由 `curriculum-checks.json` 與 `package-checks.json` 記錄來源與 renderer 指紋、影音檢查、ZIP CRC／清單與教材檔案雜湊；最終獨立驗收另檢查實際 ffprobe、封裝內容及 PDF 頁面文字。

播放器的自動控制檢查採 jsdom 並模擬媒體事件，可驗證配音／CC 獨立選擇、暫停、結束與錯誤處理。此環境先前的實際瀏覽器 `file://` 播放檢查遭政策拒絕，未改用其他路由重試；目前沒有實際瀏覽器播放通過的宣稱。影音檢查與模擬控制測試不等同各瀏覽器的人工播放驗收。
