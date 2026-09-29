# AI 與真實世界｜第一季製作包

這份交付把已確認的六集企劃落成完整腳本、來源登錄、分鏡、A/B 標題縮圖、發布文案與可播放審片版。

**Git / PR 範圍：** 此目錄提交腳本、來源、縮圖、字幕、工具與歷史驗證紀錄。MP4、WAV、ZIP、音訊快取及中間影格只保留在原製作工作目錄，未上傳 GitHub；新 checkout 的影片播放與 ZIP 下載連結需先依下方步驟重建，或從本機交付包還原。`local-artifacts.json` 記錄本機 18 支影片與 2 個 ZIP 的大小及 SHA-256，並非遠端下載網址。驗證 JSON 描述製作當時的輸出，不代表新 checkout 已包含影片。

**先開啟 [index.html](index.html)**：同一頁比較十二張原創縮圖，播放長片與 Shorts，開啟各集文件。

打包下載：[腳本與縮圖包](scripts-and-thumbnails.zip)（不含影片／WAV）、[18 支審片影片與字幕](review-videos.zip)。影片壓縮包中的 README 描述完整本機目錄；未包含的來源檔請使用前一個製作包。

## 交付界線

- 6 份完整中文旁白稿，每份約 2,000 字；每集 10 個敘事段落。
- 6 支 1920×1080 圖解審片影片，Windows 繁體中文合成旁白，實際片長見 `validation.json`。
- 12 支 1080×1920 衍生 Shorts 審片影片；短片不算入單支長片百萬目標。
- 12 張內建 image_gen 產生的原創縮圖，A/B 各六張；提示與原始檔名保留在 `assets/thumbnail-prompts.json`。
- 逐段 SRT/ASS 字幕、WAV 旁白、實測時間軸與章節、YouTube 說明欄草稿、置頂留言文案。
- 16 筆公開來源登錄，逐段區分研究事實、虛構示例與編輯建議；沒有偽裝成產品實測。
- 90 天擬定發布表、48 小時／7 天／28 天追蹤欄位、預算與最後驗收表。

**審片版不等於最終上架版。** 本機影片採三階段圖解卡與合成旁白，供確認內容、時長、字幕及方向。詳細的場景分鏡另附；目前未逐鏡製作電影式 B-roll、未經人耳配音與整片節奏驗收。沒有上傳、公開發布、訂閱付費工具或安排自動發布。尚無觀眾數據，也沒有取得百萬觀看。

標題是可測試的包裝假設，不是觀看保證。影片 A 標題中的「永遠」「都是」為疑問情境；正片明確否定全體化結論。若希望更保守的首發包裝，使用該集 B 組標題。

## 檔案位置

| 位置 | 用途 |
|---|---|
| `episodes/*.json` | 六集內容主檔；修改這裡後重建，避免直接改衍生字幕造成不同步 |
| `sources.json` | 原始來源、可支持的主張、年代和限制 |
| `assets/` | 生成縮圖 A/B、提示與來源紀錄 |
| `media/<集數>/script-storyboard.md` | 完整旁白、畫面設計、逐段來源與實際章節時間 |
| `media/<集數>/review.mp4` | 有旁白與燒錄字幕的圖解審片版 |
| `media/<集數>/short-1/`、`short-2/` | 兩支直式審片版及各自字幕與音訊 |
| `media/<集數>/upload-draft.json` | 標題、描述、置頂留言與發布狀態草稿 |
| `operations.md` | 90 天操作與發布前驗收標準 |
| `schedule.csv`、`analytics.csv`、`budget.csv` | 日期建議、空白成效紀錄、預算上限；不是已發布／已支出紀錄 |
| `validation.json`、`media/<集數>/probe.json` | 檔案結構、音訊、片長與字幕時間驗證 |

## 本機重建

**2026-09-29 Shorts 修正版：** 直式短片改用
[`tools/rebuild_shorts.py`](tools/rebuild_shorts.py)，詳見
[`shorts-corrections.md`](shorts-corrections.md)。新輸出使用 x=78–902 的安全區、上移字幕與揭露、
保留完整英文詞，並重新量測實際編碼響度。原始 `media/` 時軸與 `local-artifacts.json`
仍是歷史產物紀錄；不要把它們當成新版核准或新版檔案雜湊。

需求：Python 與 Pillow、Windows `System.Speech` 的 `Microsoft Hanhan Desktop` 聲線、ffmpeg、ffprobe。這些在製作環境已可用；沒有修改全域套件或聲線設定。

```powershell
python docs\ai-video-season-01\tools\build.py --docs-only
python docs\ai-video-season-01\tools\build.py --episode 01 --rate 0
python docs\ai-video-season-01\tools\build.py --episode 02,03,04,05,06 --rate 0
python docs\ai-video-season-01\tools\build.py --validate
python docs\ai-video-season-01\tools\operations.py
python docs\ai-video-season-01\tools\check_media.py
python docs\ai-video-season-01\tools\package.py
```

合成以短句為單位，音訊快取檔名包含文字與聲線參數的雜湊，修改文字會重新生成對應片段。字幕起訖取自每段 WAV 的實際取樣數，非按字數猜測。`--rate 0` 為本次版本。聲線雖已成功輸出，仍需要人耳確認多音字、英文縮寫與自然度。

## 來源與製作方式

英文影片只用於選題參考；未下載、翻譯拼接或沿用他人的影片、音樂、縮圖。已查到的英文觀看數來自先前搜尋索引快照，保留歷史性質，不當成現在的即時排行榜。

內建 image_gen 製作縮圖；影片內為本次原創的程式圖解。沒有假造新聞截圖、研究圖表、產品介面或真人對話。因擬真生成素材的使用而需要揭露時，依實際上架日的 [YouTube 規則](https://support.google.com/youtube/answer/14328491?hl=en-GB)填寫。是否可營利需由平台審查，不能由此製作包保證。

字幕、音訊和審片影片皆留在本機。此工作沒有修改 Travel Scanner 的產品程式、資料庫或正式站。
