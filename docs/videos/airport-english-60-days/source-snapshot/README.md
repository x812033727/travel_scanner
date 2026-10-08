# 機場英文 60 天：歷史來源快照

**狀態：未核准的試製版，禁止把這份快照當成可上架成品。** 這裡保留既有 60 集的文字來源，供重新查核、比對與修正使用。缺失與重製條件以 [AUDIT.md](../AUDIT.md) 為準；本次存檔不代表內容、翻譯、聲音、畫面或上架檢查已通過。

舊產物使用試製語音與影音設定，缺少正式流程的查核及核准證據，且已找到題目重播片段不含答案的教學問題。歷史來源中的 `script_ready: true`、`translation_status`、`publication_status` 等值按原樣保留，**不是目前的核准狀態**。[provenance.json](provenance.json) 將整份快照標為 `release_status: "blocked"`。

## 收錄範圍

| 位置 | 內容 |
| --- | --- |
| `curriculum.json` | Day 02–60 的原始英文課程、A／B 對話與三道測驗；共 59 集，不含 Day 01。 |
| `coach.json` | Day 02–60 共用的 13 段五語教學引導，原檔位於外部工作區的 `airport_series/scripts/coach.json`。 |
| `episodes/day02/` 至 `episodes/day60/` | 各集的 `script.json`、`timeline.json`、`metadata.txt` 與五條 SRT。 |
| `episodes/day01/` | 最終交付目錄中的 `metadata.txt` 與五條 SRT，加上 Day 01 獨立製作流程的七份 JSON 來源。 |

共保存 **487 份文字來源**：59 份課程腳本、59 份時間軸、60 份上架文字、300 份 SRT、兩份共用 JSON，以及 Day 01 的七份獨立 JSON。影片、聲音、縮圖、ZIP、憑證、私人部署資料、既有的完成宣告與試製程式均未納入。

SRT 語系為 `en`、`zh-Hant`、`zh-Hans`、`ja`、`ko`。它們是舊版輸出的證據，不能由檔案存在推論翻譯正確、讀速適當或音畫同步。`metadata.txt` 也是歷史草稿，尚未成為正式上架包。

## 原始格式

Day 02–60 的 `script.json` 包含各六句的 `A`／`B` 情境對話、三道 `quiz`、標題及翻譯。`all`、`title_all`、`answer_all` 等五語陣列的順序是英文、繁體中文、簡體中文、日文、韓文。角色 `T` 是旅客，`S` 是服務人員。

各集 `timeline.json` 記錄試製版實際採用的教學／對話順序、五語 `texts`、聲音選擇、速度，以及以秒表示的 `start`／`end`。它有助於查明某道題前重播了什麼，但不符合正式產線的 `video.json` 格式，也沒有明確的測驗證據 ID。修正重播選段時，應另建正式來源並逐題查核，不要改寫這份歷史紀錄。

Day 01 在系列批次流程之前獨立製作，沒有 Day 02–60 格式的 `script.json` 或 `timeline.json`。其原始資料分為：

- `data.json`：情境台詞、介面文字及語系資料。
- `narration.json`：早期教學旁白資料；不能假設每一項均用在最終英文版。
- `youtube_narration_en.json`：YouTube 英文教學旁白。
- `youtube/narration.localized.json`：對應教學旁白的四語翻譯。
- `youtube/synchronized_timeline.json`：最終同步時間軸，包括英文文字、講者、題目選項與起訖秒數。
- `youtube/timing_report.json`：原流程的分段秒數與速度紀錄，並非正式品質核准。
- `youtube/series_standard.json`：歷史上記錄的系列需求；私人預覽網址已遮除，詳見下段。

## 來源與遮除紀錄

[provenance.json](provenance.json) 逐檔列出外部工作區的相對來源路徑、快照內的相對路徑、來源與複本的 SHA-256、位元組數及遮除理由。**486 份逐位元組相同；一份有明確遮除**：`episodes/day01/youtube/series_standard.json` 的 `/review_player` 私人預覽網址改為 `[REDACTED: private preview URL]`，並重新序列化 JSON。清單保留原檔雜湊，不保存該網址。

複製前對所有來源做 UTF-8／JSON 檢查，並掃描常見憑證、token、私人 Site 識別碼與網址、絕對本機路徑及電子郵件模式。唯一命中是上述私人預覽網址，已遮除；這是有界的模式檢查，不是涵蓋所有秘密形式的保證。

快照不包含可重跑的生成器。保留來源的目的是讓正式重製有可追溯的起點，不是把原本不合規的製作流程安裝成正式工具。新的正式稿件、查核與核准紀錄應與這份歷史快照分開維護。
