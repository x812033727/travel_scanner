# Sunny 與 Pip：完整國小英文系列

使用者在第一季完成後要求「繼續完成所有國小系列」。完整系列定為六季、共 72 集，低、中、高年級各兩季；第一季原稿及已交付影片保留，其餘 60 集接續製作。這是一套分級基礎英文影片課程，不宣稱取代各地完整學校課綱或正式程度測驗。

| 階段 | 季數／集數 | 主題 | 學習進階 |
|---|---|---|---|
| 低年級 | S1／01–12 | 我的英文小教室 | 自介、課堂用語、文具問答、完整短句 |
| 低年級 | S2／13–24 | 我的單字與一天 | 字母名稱、單字家族、拼字觀察、物品、數量、喜好與請求 |
| 中年級 | S3／25–36 | 人物與地方 | 人稱、持有物、單複數、場所位置、方向、購物 |
| 中年級 | S4／37–48 | 日子與計畫 | 時間、星期、作息、頻率、天氣、正在做的事與計畫 |
| 高年級 | S5／49–60 | 故事與理由 | 過去式、問答、順序、比較、因果與短文重點 |
| 高年級 | S6／61–72 | 閱讀寫作與分享 | 時態對比、連接詞、數量、建議邀請、細節閱讀與段落寫作 |

逐集規劃見 `curriculum.txt`，製作規格見 `authoring-contract.txt`。各季末集複習該季內容；第 72 集整合國小系列。依孩子的實際程度選季，不以年齡強制推進。

每集十幕、至少三次聽力或聽讀選擇、至少一次有英文示範的句子跟讀。新季另有口說或紙筆延伸活動，搭配示例答案；示例不是唯一正解。英文單字與句子卡用來學拼字、文法和閱讀，題目中看得到各個候選答案，但不預先圈選正確答案。這些活動不冒充沒有示範的獨立閱讀測驗。

英文固定在畫面，沒有英文 CC。聲音有英文、繁體中文、簡體中文、日文、韓文五軌；其中英文示範使用完全相同的音檔。翻譯 CC 有繁中、簡中、日文、韓文四種，與配音分開選擇。一般練習留白五秒，題目六秒，之後才揭示英文目標及翻譯。

新畫面延續原創 Sunny／Pip 教室，加入數量卡、時鐘、星期與場所，以及可清楚閱讀的英文單字／句子卡。原有第一季與幼兒 renderer 不修改；第二季起使用獨立 profile，避免新美術讓已交付的檔案失去可核對的來源。

媒體輸出在 `/workspace/elementary-series-output`，影片、音檔與 ZIP 不收進公開 repository。第一季原輸出在 `/workspace/elementary-season01-output`。本機配音仍使用 Microsoft Edge read-aloud 試製聲音，尚未套用後台正式聲音；本次不包含後台整合、上傳或發布。

## 製作環境與作者來源

以下命令從 repository 根目錄 `/workspace/travel_scanner` 執行。需要 Python 3、FFmpeg／FFprobe，以及 Python 套件 Pillow、`edge-tts`、ReportLab、fontTools；Node 檢查使用 repo 既有依賴。套件、字型、語音快取與媒體都放在 repo 外。可建立專用環境：

```bash
python3 -m venv /workspace/elementary-tools-venv
/workspace/elementary-tools-venv/bin/python -m pip install Pillow edge-tts reportlab fonttools
```

下方統一使用這個 Python；既有環境已安裝依賴時，可換成該環境的 Python。Pillow 版本會寫入各集 renderer 收據，重建結果以實際版本與驗證為準，不假定換環境後的影片位元組相同。語音與字型下載需要網路，沿用環境設定的代理與受信任 CA，不停用 TLS 驗證。

`season01.json` 至 `season06.json` 保存分季作者資料，`lessons.json` 是合併後的 72 集製作輸入。修改課程或 `practice` 時同步更新兩者，不直接改輸出目錄的 `lessons.resolved.json`。可用下列命令重新合併並檢查集數；它不製作影音：

```bash
/workspace/elementary-tools-venv/bin/python - <<'PY'
import json
from pathlib import Path

directory = Path('docs/videos/english-elementary-complete')
path = directory / 'lessons.json'
document = json.loads(path.read_text(encoding='utf-8'))
episodes = [
    episode
    for season in range(1, 7)
    for episode in json.loads(
        (directory / f'season{season:02d}.json').read_text(encoding='utf-8')
    )['episodes']
]
assert [episode['id'] for episode in episodes] == [f'ep{n:02d}' for n in range(1, 73)]
assert all(episode['season'] == (index // 12) + 1 for index, episode in enumerate(episodes))
document['episodes'] = episodes
path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
PY
```

## 語音、渲染與續跑

先檢查語音請求計畫，不連線合成：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/preschool/audio.py \
  --source docs/videos/english-elementary-complete/lessons.json \
  --output /workspace/elementary-series-output \
  --plan-only
```

正式製作五語音軌與四語字幕；英文示範共用同一段 PCM，時間軸按實測語音長度建立：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/preschool/audio.py \
  --source docs/videos/english-elementary-complete/lessons.json \
  --output /workspace/elementary-series-output
```

同一輸出目錄只啟動一個語音 producer，最多兩個並行語音請求。預設快取在輸出目錄的 `.tts-cache`；可加 `--cache-dir /外部目錄/.tts-cache` 共用既有內容雜湊快取。中斷後重跑相同命令：來源、時間軸與音訊／字幕收據一致的集數會跳過，不只依檔案存在判斷完成。本次第一季已沿用先前成品及相應收據；單獨複製 MP4 不能建立可續跑的完整輸出。

音訊完成後，啟動最多三個渲染 worker：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/elementary_series/batch.py \
  --source docs/videos/english-elementary-complete/lessons.json \
  --output /workspace/elementary-series-output \
  --workers 3 \
  --fps 15
```

也可在語音 producer 已啟動後，於另一個終端執行同一批次命令並加 `--watch-audio`；每集音訊完成即可渲染，預設無進度等待上限為 1800 秒，可用 `--wait-timeout` 調整。批次工具本身不啟動第二個語音 producer。失敗／中斷後仍用同一命令續跑；狀態見 `batch-status.json`，逐集錯誤見 `build-logs/epXX.log`。成功狀態須等影片驗證與播放器寫入都完成。

第一季使用原 `elementary` profile，第二至六季使用 `elementary_series` profile。每集按來源、renderer、實際圖片／音訊／字幕及最終 MP4 收據核對，不把一季的 renderer 收據套到另一季。已開跑時不要變動美術與 renderer 相依檔；需要更動時，後續驗證會要求重建受影響成品。

單集重做先用前面的語音命令加 `--episode ep17`，再渲染該集：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/elementary_series/build.py \
  --source /workspace/elementary-series-output/lessons.resolved.json \
  --output /workspace/elementary-series-output \
  --episode ep17 \
  --skip-valid \
  --fps 15
```

`build.py` 的 `--source` 是實測 resolved，`audio.py`／`batch.py` 的 `--source` 則是作者原稿。只有既有 picture 的來源、時序、renderer 與雜湊全部有效時才可使用 `--mux-only`；改過原稿後不要靠重封裝沿用舊畫面。只更新離線播放器可執行：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/elementary_series/build.py \
  --source /workspace/elementary-series-output/lessons.resolved.json \
  --output /workspace/elementary-series-output \
  --player-only
```

## 可列印練習與 PDF 字型

每個分季包及整套包都附 `Practice.html` 與 `Practice.pdf`，題目先列出、示例答案另放後方。第二至六季逐字使用作者來源的 `practice.prompt_en`、`practice.prompt_zh_TW`、`practice.sample_answer_en`；第一季由原本跟讀場景取得示範句，不修改已交付原稿。HTML 可在瀏覽器閱讀並按「列印練習」；PDF 以 A4 排版，每集一頁作答區，後附答案頁。兩種格式都保留英文題目、繁中說明與英文示例。

PDF 使用 ReportLab 嵌入靜態 TrueType 繁中字型，閱讀端不需另裝字型或 CMap。本次使用 [Noto Sans TC 變動 TrueType 字型](https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/Variable/TTF/Subset/NotoSansTC-VF.ttf)，透過 fontTools 固定 `wght=400`。可重建外部字型檔：

```bash
mkdir -p /workspace/elementary-series-output/.fonts
curl --fail --location \
  --user-agent 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' \
  --output /workspace/elementary-series-output/.fonts/NotoSansTC-VF.ttf \
  https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/Variable/TTF/Subset/NotoSansTC-VF.ttf
/workspace/elementary-tools-venv/bin/python - <<'PY'
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

directory = Path('/workspace/elementary-series-output/.fonts')
font = TTFont(directory / 'NotoSansTC-VF.ttf')
instantiateVariableFont(font, {'wght': 400}, inplace=True)
font.save(directory / 'NotoSansTC-Regular.ttf')
font.close()
PY
export ELEMENTARY_PRACTICE_FONT=/workspace/elementary-series-output/.fonts/NotoSansTC-Regular.ttf
```

`practice.py` 優先使用 `ELEMENTARY_PRACTICE_FONT`，未指定時向輸出目錄及其父目錄尋找 `.fonts/NotoSansTC-Regular.ttf`；找不到會停止 PDF 製作，不以缺字的替代字型交付。本次靜態字型 SHA-256 為 `b1f977a91bf3d0eab029a2b713ed9ad14eda085a15ca8ed202e35c66731f23cf`，來源與檢查記錄位於輸出目錄的 `practice-font-checks.json`。下載 URL 的 `main` 可能更新，日後重建須重新記錄雜湊並檢視繁中及英文是否完整顯示。

打包會自動製作練習檔。只要預覽練習、暫不打包影音，可從目前原稿獨立生成；這不代表影音已完成或驗證通過：

```bash
/workspace/elementary-tools-venv/bin/python - <<'PY'
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path('tools/video').resolve()))
from elementary_series.practice import write_practice

source = json.loads(Path('docs/videos/english-elementary-complete/lessons.json').read_text(encoding='utf-8'))
write_practice(source['episodes'], Path('/workspace/elementary-series-output/practice-preview'))
PY
```

## 驗證與打包命令

完整驗證須以當前作者來源執行，要求 72 集全部完成：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/elementary_series/verify_series.py \
  --source docs/videos/english-elementary-complete/lessons.json \
  --output /workspace/elementary-series-output
```

製作途中可加 `--allow-partial`：缺集時報告仍是 `passed: false`／`status: partial`，只代表已完成部分沒有查到錯誤。`--report /外部目錄/report.json` 可將報告另存，不覆寫輸出目錄的報告。完整驗證核對作者來源、實測共用英文示範、回應留白、四語字幕、分季 renderer、sidecar 與 final 收據；成片必須與先前成功完整解碼的 SHA-256 一致。

先只檢查打包輸入，不產生或替換 ZIP：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/elementary_series/package_series.py \
  --source docs/videos/english-elementary-complete/lessons.json \
  --resolved /workspace/elementary-series-output/lessons.resolved.json \
  --output /workspace/elementary-series-output \
  --check-only
```

移除 `--check-only` 即產生六個分季 ZIP、整套 72 集 ZIP、課程目錄及 HTML／PDF 練習：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/elementary_series/package_series.py \
  --source docs/videos/english-elementary-complete/lessons.json \
  --resolved /workspace/elementary-series-output/lessons.resolved.json \
  --output /workspace/elementary-series-output
```

`--source` 是必要參數，`--resolved` 必須位於指定 output 下。打包先核對全部作者欄位（含 practice）與來源指紋，完整影音驗證通過才建立暫存 ZIP；對每包檢查成員與 CRC，並在替換交付檔前再次確認作者原稿及 resolved 的 SHA-256 未變。舊 resolved 即使與舊影片彼此一致，也不能取代當前作者原稿。加 `--seasons-only` 可只產生六季包。

輸出名稱為 `Sunny_Pip_Elementary_Season_01.zip` 至 `Sunny_Pip_Elementary_Season_06.zip`、`Sunny_Pip_Elementary_72_Episodes.zip`、`國小英文72集課程目錄.csv`、`Practice.html`、`Practice.pdf`，打包紀錄在 `package-checks.json`。每個季包只含該季十二集與自己的離線播放器；不放入語音快取、字型原檔或製作日誌。

程式與任務檢查沿用 repo 指令；測試中的媒體 fixture 只驗證准入與失敗行為，不代表真實媒體解碼。播放器模擬檢查也不能當成瀏覽器實播：

```bash
npm run test:tools
npm run check:tasks
node tools/video/preschool/check-player.mjs /workspace/elementary-series-output/index.html \
  --expect-episodes 72 \
  --expect-seasons 6 \
  --expect-per-season 12
```

跟讀文字的實際像素檢查另用製作環境的 Pillow 執行，包含舊版遮字畫法的負向對照；不增加純標準庫 CI 的依賴：

```bash
/workspace/elementary-tools-venv/bin/python tools/video/elementary_series/check_guided_pixels.py \
  --source docs/videos/english-elementary-complete/lessons.json \
  --report /workspace/elementary-series-output/art-guided-pixel-checks.json
```

## 製作與交付狀態

2026-10-08 完成六季 72 集，成片總長 **13,049.675 秒，約 3 小時 37 分 30 秒**。每集約 3 分鐘，最長約 3 分 13 秒。第一季原有 12 集的作者內容及 228 個媒體／側錄檔案經 SHA-256 核對完全保留。

| 下載包 | 檔名 | 大小（十進位） |
|---|---|---:|
| 第 1 季（12 集） | `Sunny_Pip_Elementary_Season_01.zip` | 157.5 MB |
| 第 2 季（12 集） | `Sunny_Pip_Elementary_Season_02.zip` | 147.0 MB |
| 第 3 季（12 集） | `Sunny_Pip_Elementary_Season_03.zip` | 149.1 MB |
| 第 4 季（12 集） | `Sunny_Pip_Elementary_Season_04.zip` | 148.3 MB |
| 第 5 季（12 集） | `Sunny_Pip_Elementary_Season_05.zip` | 158.8 MB |
| 第 6 季（12 集） | `Sunny_Pip_Elementary_Season_06.zip` | 158.6 MB |
| 全套（72 集） | `Sunny_Pip_Elementary_72_Episodes.zip` | 919.0 MB |

所有檔案位於 `/workspace/elementary-series-output`。各季包附 15 頁練習 PDF，整套包附 85 頁 PDF；另有 HTML 練習、72 列課程目錄及離線播放器。下載後完整解壓縮，再開啟包內 `index.html`；也可用 VLC 切換 MP4 內的音軌與 CC。整套另保留 360 個獨立 M4A、288 個 SRT 與 288 個 VTT，沒有英文 CC。

驗證摘要見 `delivery-verification.json`。72 集成片都成功完整解碼，完整課程驗證 72/72 通過、零錯誤，來源、共用英文示範、回應時間、字幕、分季 renderer 與所有媒體 SHA 均相符。七 ZIP 通過獨立 CRC／成員 SHA／播放器資產／字幕 cue／CSV／練習內容檢查；每季 209 個檔案，全集 1,229 個檔案。

全套及六個分季播放器共七組 jsdom 操作檢查通過，配音與 CC 可分開切換。此環境先前以管理員政策禁止本機瀏覽器開啟 `file://`；本次未做真實瀏覽器實播，jsdom 媒體事件和解碼為模擬，實際檔案解碼另由 FFmpeg 驗證。

新五季美術檢查涵蓋 600 幕、2,400 張畫面、180 題揭答前不洩答、106 幕帶讀文字像素保留及 86 次多行間距檢查。已從實際成片抽查選句、數量、07:30 時鐘與兩個多行跟讀場景。練習冊的 432 項來源欄位匹配，打包後 PDF 全文與已目視抽查版本一致。

本機 `npm run test:tools`：2,012 項，2,009 通過、3 略過、0 失敗；最新獨立 pipeline 的 17 項測試全部通過。實際媒體與字型、快取及 ZIP 均不收進公開 repository；配音仍為前述 Microsoft Edge 試製聲音。
