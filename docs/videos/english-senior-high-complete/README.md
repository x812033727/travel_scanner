# Sunny 與 Pip：高中英文系列

承接國中系列，共六季、72 集，每季十二集。高一至高三各兩季，從精確句型和段落組織，進入論點、證據、批判閱讀及整合寫作，最後銜接大學學習所需的提問、討論、簡報和書信。可依先備能力選季；這套分級微課程不宣稱完整取代各地高中課綱或提供正式程度認證。

| 年級 | 季／集數 | 主題 | 核心練習 |
|---|---|---|---|
| 高一 | S1／01–12 | 精確表達 | 時間關係、關係子句、名詞子句、完整人物介紹 |
| 高一 | S2／13–24 | 組織段落 | 主題句、支持、比較、因果、條件、提案與修訂 |
| 高二 | S3／25–36 | 觀點與證據 | 主張、理由、反方觀點、引述、虛構數據及推論界線 |
| 高二 | S4／37–48 | 批判閱讀與跨情境溝通 | 目的、語氣、文本推論、來源用途、圖文資訊與正式交流 |
| 高三 | S5／49–60 | 整合閱讀與寫作 | 摘要、雙來源比較與整合、論述組織、精確修訂 |
| 高三 | S6／61–72 | 大學銜接與學術溝通 | 筆記、解釋、討論、簡報問答、學術書信及小型探究 |

逐集目標以 `season01.json` 至 `season06.json` 為準；`lessons.json` 是合併製作輸入。[planning.txt](planning.txt) 保存課程序列，[authoring-contract.txt](authoring-contract.txt) 保存格式與教學要求。每季最後一集整合已學內容。

每集十幕，保留英文示範、兩幕以上跟讀及三題聽讀選句。選句會先播放正確英文示範，等待六秒再揭答；一般回應時間五秒。這些是有提示的練習。獨立理解及分析另放在課後教材，不把跟讀選句當成獨立程度評量。

每集另有原創閱讀、三題理解／分析及一項寫作。高一閱讀 90–130 詞、寫作 60–90 詞；高二閱讀 120–160 詞、寫作 80–110 詞；高三閱讀 140–180 詞、寫作 100–140 詞。數據情境明示為虛構，不冒充真實研究。PDF 每集分成閱讀理解頁、寫作頁和後置答案頁；完整教材 217 頁，各季 37 頁。例答不是開放式任務的唯一答案。

英文固定在畫面，沒有英文 CC。音訊提供英文、繁體中文、簡體中文、日文、韓文五軌；四語教學音訊共用同一段英文示範原音。CC 提供繁中、簡中、日文、韓文，可與配音分開選擇。目前使用 Microsoft Edge read-aloud 試製聲音，尚未整合後台正式聲音，也未發布。

新來源和工具只位於本目錄與 `tools/video/senior_high/`，既有幼兒、國小及國中系列保持不變。影片、語音快取、字型、PDF 和 ZIP 均在公開 repository 之外，預設輸出 `/workspace/senior-high-series-output`。

## 重建與續跑

從 repository 根目錄執行。需要 Python 3、FFmpeg／FFprobe、DejaVu Sans Regular／Bold、Pillow、edge-tts、ReportLab、Matplotlib 和 fontTools。Matplotlib 為圖表閱讀教材繪製同一組數字的兩種縱軸比較圖；不參與影片 renderer。實際畫面雜湊綁定 renderer 相依檔、字型及 Pillow 版本；換環境須重新驗證。語音和字型下載沿用環境代理與 CA，維持 TLS 驗證。

```bash
python3 -m venv /workspace/senior-high-tools-venv
/workspace/senior-high-tools-venv/bin/python -m pip install Pillow edge-tts reportlab matplotlib fonttools
source /workspace/senior-high-tools-venv/bin/activate
```

下列 `python` 代表已安裝上述相依的環境。先合併作者來源並檢查；所有作者欄位都會與實測 resolved 資料比對。

```bash
PYTHONPATH=tools/video python - <<'PY'
import json
from pathlib import Path
from senior_high.verify_series import verify_structure

directory = Path('docs/videos/english-senior-high-complete')
episodes = []
for season in range(1, 7):
    document = json.loads((directory / f'season{season:02d}.json').read_text(encoding='utf-8'))
    verify_structure(document, allow_season_subset=True)
    episodes.extend(document['episodes'])
source = {'series_title': 'Sunny & Pip: Senior High English', 'version': 4, 'episodes': episodes}
print(verify_structure(source))
(directory / 'lessons.json').write_text(json.dumps(source, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
PY
```

先審查語意、翻譯、文本依據及題目答案，再啟動語音。可先加 `--plan-only` 檢查請求計畫。同一輸出目錄只執行一個 audio producer，最多兩個並行語音請求。

```bash
python tools/video/preschool/audio.py \
  --source docs/videos/english-senior-high-complete/lessons.json \
  --output /workspace/senior-high-series-output

python tools/video/senior_high/batch.py \
  --source docs/videos/english-senior-high-complete/lessons.json \
  --output /workspace/senior-high-series-output --workers 3 --fps 15
```

語音進行中可在另一終端執行 batch 並加 `--watch-audio`。分季製作時將來源改為 `seasonNN.json`，batch 加 `--allow-season-subset`；最終驗證和打包仍要求完整 72 集。狀態見 `batch-status.json`，單集記錄見 `build-logs/epNN.log`。成功續跑依當前作者來源、時序、renderer 與檔案雜湊，不只看檔案存在。

改稿後先同步分季檔與合併檔，再對 audio 命令加 `--episode epNN --force` 重新組裝該集。即使只改課後題目也須如此，才能同步所有 authored 欄位；原語音片段可從內容雜湊快取重用。之後重跑 batch，自動驗證並重建失效成品。不要直接修改 `lessons.resolved.json`，也不要在批次渲染途中改 renderer 相依檔。

PDF 需要可嵌入的繁中文字型。設定 `SENIOR_HIGH_PRACTICE_FONT` 指向靜態 Noto Sans TC TrueType；或放在輸出目錄 `.fonts/NotoSansTC-Regular.ttf`。本次從 Noto CJK 官方 `Sans/Variable/TTF/Subset/NotoSansTC-VF.ttf` 以 fontTools `instantiateVariableFont(..., {'wght': 400})` 產生靜態字型，SHA-256 為 `b1f977a91bf3d0eab029a2b713ed9ad14eda085a15ca8ed202e35c66731f23cf`，只嵌入 PDF 子集，不把字型二進位加入 Git。

```bash
PYTHONPATH=tools/video python -m senior_high.art_qa \
  --source docs/videos/english-senior-high-complete/lessons.json \
  --output /workspace/senior-high-series-output/art-qa

python tools/video/senior_high/verify_series.py \
  --source docs/videos/english-senior-high-complete/lessons.json \
  --output /workspace/senior-high-series-output

python tools/video/senior_high/package_series.py \
  --source docs/videos/english-senior-high-complete/lessons.json \
  --resolved /workspace/senior-high-series-output/lessons.resolved.json \
  --output /workspace/senior-high-series-output

npm run test:tools
npm run check:tasks
```

打包前要求當前原稿、完整配音、精確 CC、全部成片和完整解碼收據一致；只納入允許的成品。六個分季 ZIP 和一個全集 ZIP 均包含離線播放器、課程目錄、練習 HTML／PDF 及必要媒體。

解壓 ZIP 並保留資料夾結構後開啟 `index.html`；也可用 VLC 開啟每集 `final.mp4` 切換聲軌和字幕。`picture.mp4` 是無聲畫面，`audio/` 為五語 M4A，`captions/` 為四語 SRT／VTT。

## 驗證範圍

品質檢查包括作者交叉審稿、固定英文與選項版面、揭答前畫面不洩漏正解、字形與字幕保留區、source-bound 全片解碼收據、實際 FFprobe、逐檔與 ZIP 雜湊，以及獨立教材內容和播放器控制檢查。交叉審稿不是五語認證母語教師審定；選取成片畫面檢查也不宣稱逐集人工觀看或逐聲軌人工聽完。

先前實際 Chromium 本機檔案播放被管理員政策阻擋，因此不繞過限制重試。本次以真實媒體解碼及模擬媒體的 jsdom 控制檢查驗證；不宣稱已完成實際瀏覽器影音播放。
