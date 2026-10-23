---
id: 2026-10-07-preschool-english-complete-series
title: 完成幼兒英文全系列 48 集
status: done
priority: P2
area: docs
owner: codex-preschool-series
claimed_at: 2026-10-07T23:06:19Z
created_at: 2026-10-07T23:06:15Z
completed_at: 2026-10-08T00:08:59Z
branch: work
depends_on: []
scope:
  - docs/videos/english-preschool-series
  - tools/video/preschool
---

# 完成幼兒英文全系列 48 集

## Why

幼兒英文前 5 集試播交付後，使用者要求完成全部幼兒系列。已確認幼兒階段為 4 季、每季 12 集，共 48 集；固定英文字幕直接放進畫面，另有繁中、簡中、日文、韓文配音與 CC，保留英文音軌、不提供英文 CC。本任務補齊第 6–48 集，延續 Sunny 與 Pip 的幼兒教學形式，交付可下載、按季觀看的完整本機影片包。

## Definition of done

- [x] 48 集全部有可播放成品；第 1–5 集按既有內容重用，第 6–48 集完成新增影音，每集目標約 3 分鐘，以實測時間軸為準。
- [x] 每集含固定英文畫面文字、英文加繁中／簡中／日／韓 5 音軌，以及四語 CC；沒有英文 CC，聽力題揭答前不洩漏目標詞或翻譯。
- [x] 全部成片完成串流、長度、檔案完整性與影音解碼驗證；英文與四語文稿完成交叉審查，畫面語意抽查、音軌解碼及音量抽查結果有紀錄。
- [x] 全系列離線播放器可選 4 季、48 集，音軌與 CC 可獨立切換；播放器操作檢查及實播範圍分別留有紀錄。
- [x] 交付 48 集整套 ZIP、4 個各含 12 集與獨立播放器的 ZIP、48 集課程目錄 CSV 及打包檢查紀錄，解壓後媒體路徑完整。
- [x] 文件和交付說明明確標示 Edge 試製合成語音、未接後台正式聲音、未上傳或發布；媒體與快取留在公開 repo 外。

## Steps

- [x] 沿用使用者已確認的 4 季、48 集範圍與五音軌／四 CC 規格，讀取 repo 與影片製作規範。
- [x] 完成四季課程 JSON 並整合 `lessons.json`，共 48 集、480 景；新增集數含完整五語講解、四語示範翻譯與聽力練習。
- [x] 保留第 1–5 集課程文字與 token，僅加季數，帶入既有試播檔案供重用。
- [x] 第 28 集納入 Mom／Dad 家人主題，課綱與圖像設計避免假定所有家庭構成相同。
- [x] 完成 README 的課綱表、輸出規格、重建命令與驗證流程。
- [x] 完成第 6–48 集五音軌與四語字幕，量測共同時間軸並確認聽力題延後揭答。
- [x] 完成第 6–48 集畫面渲染、封裝與逐集完整解碼；核對重用的第 1–5 集檔案完整。
- [x] 完成全系列與分季播放器檢查，記錄 JS DOM 模擬、音量與畫面抽查，以及未做真實瀏覽器實播／逐集人耳聽審的界線。
- [x] 產生四季 ZIP、`幼兒英文48集課程目錄.csv` 和 `package-checks.json`，核對下載檔案與交付連結。
- [x] 將最終成品數、各包檔案大小和驗證範圍補入 Notes，再結束任務。

## How to verify

完整課綱、工具使用與逐項驗證見 [`README.md`](../../docs/videos/english-preschool-series/README.md)。以下命令從 repo 根目錄執行：

```bash
python tools/video/preschool/audio.py \
  --source docs/videos/english-preschool-series/lessons.json \
  --output /workspace/preschool-series-output \
  --plan-only
node tools/video/preschool/check-player.mjs /workspace/preschool-series-output/index.html
npm run check:tasks
```

語音計畫命令僅驗證資料與列出請求，並不代表成品完成。JS DOM 播放器檢查模擬媒體介面，不能代替瀏覽器實播；應另開啟全系列及各季 `index.html`，驗證選集、換季、音軌／CC 獨立切換、關閉 CC、跳轉和聲畫同步。

`build.py` 封裝時自動以 FFprobe 確認 1280×720、5 音軌、4 CC、沒有英文 CC、180–300 秒與實測時間軸一致，再以 FFmpeg 完整解碼影像與全部音軌。逐集檢查 `/workspace/preschool-series-output/epXX/checks.json` 的 `full_decode`、來源與成品雜湊；另核對所有字幕檔存在、時間未越界、quiz 在 `reveal_at` 前沒有答案文字。

完成媒體後打包：

```bash
python tools/video/preschool/package_series.py \
  --resolved /workspace/preschool-series-output/lessons.resolved.json \
  --output /workspace/preschool-series-output
```

四包應為 `Sunny_Pip_Season_01.zip` 至 `Sunny_Pip_Season_04.zip`，集數依次為 01–12、13–24、25–36、37–48；對照 `package-checks.json`，解壓抽查每包的獨立播放器及所有相對媒體路徑。本次另用 `--all-zip` 提供 48 集整套包。

## Notes

- 來源：`docs/videos/english-preschool-series/season01.json` 至 `season04.json`，整合來源為 `lessons.json`；實測時間軸為輸出目錄的 `lessons.resolved.json`。
- 輸出目錄：`/workspace/preschool-series-output`。原 5 集試播：`/workspace/preschool-pilot-output`。影片、音訊、語音快取與暫存檔不進公開 repo。
- 製作工具在 `tools/video/preschool`。`audio.py` 使用可續跑語音快取；`batch.py` 監督一個語音 producer 與最多 3 個 renderer，已完成部分經雜湊核對後可重用。若已有外部語音 producer，使用 `--watch-audio`；音訊全備妥後只渲染用 `--render-only`，不要同時啟動多個 producer 寫同一 manifest。
- `batch-status.json`、`audio-manifest.json`、各集 `checks.json` 與 `build-logs` 記錄實際進度和失敗原因；中斷可續跑，不能將未完成字幕或未驗證檔案包入交付。
- 本次沿用使用者已確認的約 3 分鐘幼兒試播規格，不套用一般長篇解說影片的 8 分鐘要求；五語時間軸以實際合成長度為準，必要時延長場景以保留完整語音。
- 語音來源為 Microsoft Edge read-aloud 試製合成聲音：Jenny／HsiaoChen／Xiaoxiao／Nanami／SunHi。未接後台、未套用後台正式聲音、未上傳或發布。四語講解不取代英文示範。
- 字幕規格為英文固定在畫面，繁中／簡中／日／韓各有可切換 CC；聽力題等待時只顯示中性指令，揭答後才出現目標英文與翻譯。
- `art-validation.json` 記錄圖像 token 與 quiz揭答機制檢查；它不是完整成片觀看或語音驗證結果。播放器 JS DOM 檢查與真實瀏覽器實播結果須分別紀錄。

## 本次交付紀錄

- 完成時間：2026-10-08T00:08:58.805292+00:00。
- 48 集、4 季、480 景；總長約 144.09 分鐘。第 1–5 集與既有試播成品 SHA-256 相同；第 6–48 集為新增成品。
- 48 集全部通過 `verify_series.py`，0 errors；逐集完整解碼、五音軌／四 CC、字幕留白、來源與成品雜湊均通過。
- 全系列與五個 ZIP 內的播放器皆通過 JS DOM 操作檢查；ZIP CRC、集數、媒體相對路徑及課程目錄通過。
- 五語文稿交叉審查；畫面 token、揭答前後及代表性成片畫面抽查；第 28 集五音軌音量抽查通過。未進行逐集人耳全程聽審或真實瀏覽器實播。JS DOM 的媒體解碼與事件為模擬；成片影音解碼另由 FFmpeg 驗證。
- 輸出目錄為 `/workspace/preschool-series-output`；影片、ZIP 與快取均未放進公開 repo，未上傳後台或 YouTube。

| 下載檔 | 集數 | 大小（十進位） |
|---|---:|---:|
| `Sunny_Pip_Season_01.zip` | 12 | 160.2 MB |
| `Sunny_Pip_Season_02.zip` | 12 | 158.2 MB |
| `Sunny_Pip_Season_03.zip` | 12 | 152.9 MB |
| `Sunny_Pip_Season_04.zip` | 12 | 161.0 MB |
| `Sunny_Pip_48_Episodes.zip` | 48 | 632.4 MB |

另附 `幼兒英文48集課程目錄.csv`。`package-checks.json`、`packaged-player-checks.json`、`player-checks.json`、`curriculum-checks.json`、`audio-level-checks.json` 留存驗證範圍與結果。
