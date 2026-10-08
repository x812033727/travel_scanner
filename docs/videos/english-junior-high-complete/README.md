# Sunny 與 Pip：國中英文系列

本系列承接既有國小英文基礎，規劃六季、72 集，每季十二集。S1–S2 對應國一（`grade: 7`）、S3–S4 對應國二（`grade: 8`）、S5–S6 對應國三（`grade: 9`）。課程從完整句子的組織，進階到時態、理由、經驗、觀點與閱讀寫作；可依學習者的實際程度選季。這是一套分級基礎課程，不宣稱完整取代各地學校課綱或正式程度測驗。

| 階段 | 季數／集數 | 主題 | 主要進階 |
|---|---|---|---|
| 國一 | S1／01–12 | 句子的基礎 | be、代名詞、所有格、位置、習慣與當下動作、校園訊息 |
| 國一 | S2／13–24 | 日常交流 | 請求、規則與選擇、食物數量、問路、過去事件及問答 |
| 國二 | S3／25–36 | 故事與比較 | 過去進行式、過去習慣、比較、能力限制、預測、計畫與安排 |
| 國二 | S4／37–48 | 理由與經驗 | 動詞搭配、因果與讓步、時間順序、條件句、現在完成式 |
| 國三 | S5／49–60 | 連結與觀點 | 建議與可能性、被動語態、關係子句、間接問句、轉述與假設 |
| 國三 | S6／61–72 | 閱讀寫作與溝通 | 連接、指代、主旨、證據推論、實用資訊、訊息與段落、修訂及討論 |

逐集學習重點見 [curriculum.txt](curriculum.txt)，原始序列規劃見 [planning.txt](planning.txt)，作者規格見 [authoring-contract.txt](authoring-contract.txt)。每季第十二集只整合該季已學內容；第 72 集以閱讀、寫作和口說小專題統整系列。

## 短課與獨立練習

每集十幕，以實測約三至五分鐘的短課程為製作目標。每集至少三題「聽讀選句」及兩幕有英文示範的引導跟讀。選句題會先播放正確英文示範，畫面提供可比較的英文選項；一般練習留白五秒、選句題六秒，之後才揭答及顯示翻譯。固定標題和題目指令保持中性，不提前標示答案。這些活動用於學習與練習，不視為獨立閱讀或純聽力評量。

獨立閱讀與寫作放在課後練習。每集包含一篇虛構短文、恰好三題閱讀或句型應用，以及一項短文寫作。國一短文 30–50 詞、國二 40–60 詞、國三 50–75 詞；國一、國二通常寫三至五句，國三依任務可寫四至六句。閱讀題須能根據短文或已教句型回答；推論要有文本證據。寫作可使用虛構人物與情境，不需要提供真實姓名、住址等個人資料。答案與英文寫作示例另放後方，示例不是所有開放式題目的唯一答案。

英文固定在畫面，沒有英文 CC。聲音有英文、繁體中文、簡體中文、日文、韓文五軌；各聲軌共用同一段英文示範原音。翻譯 CC 有繁中、簡中、日文、韓文四種，可與配音分開選擇。時間軸依完整語音的實測長度建立，不截斷語音或慢播湊時。本機沿用 Microsoft Edge read-aloud 試製聲音，尚未宣稱採用後台正式聲音。

六季統一使用 `sunny-pip-junior-high-v1` renderer，畫面以適合國中學習的英文句卡、閱讀資訊和清楚的選項為主。國中作者原稿、renderer 與製作入口獨立放在本目錄和 `tools/video/junior_high/`；共用已存在的語音及底層媒體 runtime，保留原幼兒／國小作者資料、工具與媒體。

## 作者來源與環境

從 repository 根目錄 `/workspace/travel_scanner` 執行下方命令。媒體、語音快取、字型、PDF 與 ZIP 輸出到 `/workspace/junior-high-series-output`，不收入公開 repository。本流程製作離線交付檔；後台整合、上傳及發布另行處理。

需要 Python 3、FFmpeg／FFprobe、系統 DejaVu Sans／DejaVu Sans Bold 字型（`/usr/share/fonts/truetype/dejavu/`），以及 Pillow、`edge-tts`、ReportLab、fontTools。可在 repo 外建立專用環境；已有這些依賴時，也可改用既有環境的 Python：

```bash
python3 -m venv /workspace/junior-high-tools-venv
/workspace/junior-high-tools-venv/bin/python -m pip install Pillow edge-tts reportlab fonttools
```

語音和字型下載需網路；沿用環境代理與受信任 CA，不停用 TLS 驗證。實際 Pillow 版本、renderer 相依檔和字型來源會影響畫面指紋，換環境後須重新驗證，不假定影片位元組相同。

`season01.json` 至 `season06.json` 是分季作者來源，`lessons.json` 是合併後的製作輸入。Top-level 固定 `series_title: Sunny & Pip: Junior High English`、`version: 3`。`practice` 同時保存閱讀、三題問答、寫作題目與示例。課程有修改時，先同步分季原稿與合併檔，再重建受影響成品；不直接改輸出目錄的 `lessons.resolved.json`。語音開始後的來源變更須先協調，避免同一集混用新舊素材。

合併六季並檢查連續集號、季別與年級；此命令不製作影音：

```bash
/workspace/junior-high-tools-venv/bin/python - <<'PY'
import json
from pathlib import Path

directory = Path('docs/videos/english-junior-high-complete')
episodes = []
for season in range(1, 7):
    document = json.loads((directory / f'season{season:02d}.json').read_text(encoding='utf-8'))
    assert document['series_title'] == 'Sunny & Pip: Junior High English'
    assert document['version'] == 3
    assert len(document['episodes']) == 12
    episodes.extend(document['episodes'])
assert [episode['id'] for episode in episodes] == [f'ep{n:02d}' for n in range(1, 73)]
assert all(episode['season'] == index // 12 + 1 for index, episode in enumerate(episodes))
assert all(episode['grade'] == 7 + index // 24 for index, episode in enumerate(episodes))
source = {'series_title': 'Sunny & Pip: Junior High English', 'version': 3, 'episodes': episodes}
(directory / 'lessons.json').write_text(json.dumps(source, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
PY
```

只做作者結構檢查，不要求已完成的媒體：

```bash
PYTHONPATH=tools/video /workspace/junior-high-tools-venv/bin/python - <<'PY'
import json
from pathlib import Path
from junior_high.verify_series import verify_structure

source = json.loads(Path('docs/videos/english-junior-high-complete/lessons.json').read_text(encoding='utf-8'))
print(verify_structure(source))
PY
```

結構檢查之外仍須人工核對句型、翻譯、指代、選項唯一性及課後問題的文本依據。

## 語音、渲染與續跑

語音使用共用的 `tools/video/preschool/audio.py`，輸入與輸出均指向國中新資料。先檢查語音請求計畫，不連線合成：

```bash
/workspace/junior-high-tools-venv/bin/python tools/video/preschool/audio.py \
  --source docs/videos/english-junior-high-complete/lessons.json \
  --output /workspace/junior-high-series-output \
  --plan-only
```

移除 `--plan-only` 產生五聲軌、四語字幕與實測時間軸：

```bash
/workspace/junior-high-tools-venv/bin/python tools/video/preschool/audio.py \
  --source docs/videos/english-junior-high-complete/lessons.json \
  --output /workspace/junior-high-series-output
```

同一輸出目錄只啟動一個語音 producer，最多兩個並行語音請求。預設快取在輸出目錄的 `.tts-cache`；需要共用既有內容雜湊快取時，可加 `--cache-dir /外部目錄/.tts-cache`。中斷後重跑相同命令，工具按來源、時間軸與音訊／字幕收據判斷續跑，不只看檔案是否存在。

音訊完成後，啟動國中渲染入口，最多三個 worker：

```bash
/workspace/junior-high-tools-venv/bin/python tools/video/junior_high/batch.py \
  --source docs/videos/english-junior-high-complete/lessons.json \
  --output /workspace/junior-high-series-output \
  --workers 3 \
  --fps 15
```

語音 producer 已在執行時，可於另一個終端替同一批次命令加 `--watch-audio`，讓音訊備妥的集數進入渲染。預設無進度等待上限為 1800 秒，可用 `--wait-timeout` 調整；批次入口本身不合成語音。製作完整分季子集時，可使用 `--allow-season-subset`；最後驗證與全套打包仍要求完整 72 集。

批次狀態在 `batch-status.json`，逐集記錄在 `build-logs/epNN.log`。成功續跑須符合當前作者來源、renderer 與媒體指紋；只複製 MP4 不能建立完整製作收據。原稿與 renderer 相依檔凍結後再大量渲染，避免不必要的重建。

單集重做先替語音命令加 `--episode ep17`，再從實測 resolved 渲染：

```bash
/workspace/junior-high-tools-venv/bin/python tools/video/junior_high/build.py \
  --source /workspace/junior-high-series-output/lessons.resolved.json \
  --output /workspace/junior-high-series-output \
  --episode ep17 \
  --skip-valid \
  --fps 15
```

`build.py` 使用實測 `lessons.resolved.json`；`audio.py`、`batch.py` 與驗證／打包入口使用目前作者原稿。`--mux-only` 只適用於來源、時序、renderer 和雜湊均有效的既有畫面；改稿後不可用重封裝掩蓋舊畫面。只更新離線播放器，可用上述 `build.py` 命令移除 `--episode`、`--skip-valid`，改加 `--player-only`。

## 可列印練習與 PDF 字型

每個分季包及整套包包含 `Practice.html` 與 `Practice.pdf`。每集作答頁保留英文閱讀、三題英文理解或應用題、英文寫作題與繁中說明，附三個閱讀回答區和五條寫作留白；各題答案與寫作示例統一另置後方。HTML 可直接閱讀並用「列印練習」列印。

PDF 採 A4 固定配置，預期每季 17 頁（1 頁說明、12 頁練習、4 頁答案），整套 97 頁（1 頁說明、72 頁練習、24 頁答案）。答案每頁放三集；實際交付須核對頁數並檢查有無溢出或缺字，HTML 經不同瀏覽器列印的頁數不作相同保證。

PDF 以 ReportLab 嵌入靜態 TrueType 繁中字型，閱讀端不需另裝字型或 CMap。以下把 Noto Sans TC 變動 TrueType 固定為 `wght=400`，字型留在 repo 外：

```bash
mkdir -p /workspace/junior-high-series-output/.fonts
curl --fail --location \
  --user-agent 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' \
  --output /workspace/junior-high-series-output/.fonts/NotoSansTC-VF.ttf \
  https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/Variable/TTF/Subset/NotoSansTC-VF.ttf
/workspace/junior-high-tools-venv/bin/python - <<'PY'
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

directory = Path('/workspace/junior-high-series-output/.fonts')
font = TTFont(directory / 'NotoSansTC-VF.ttf')
instantiateVariableFont(font, {'wght': 400}, inplace=True)
font.save(directory / 'NotoSansTC-Regular.ttf')
font.close()
PY
export JUNIOR_HIGH_PRACTICE_FONT=/workspace/junior-high-series-output/.fonts/NotoSansTC-Regular.ttf
```

`practice.py` 優先使用 `JUNIOR_HIGH_PRACTICE_FONT`，亦會向輸出目錄及父目錄尋找 `.fonts/NotoSansTC-Regular.ttf`。找不到可用字型就停止 PDF 製作。下載 URL 的 `main` 可能更新，每次製作須記錄實際字型雜湊並檢視繁中及英文，不沿用另一套課程的驗證結論。

打包會自動產生練習檔。只要預覽教材，可獨立執行以下命令；練習產生成功不表示影音已完成驗證：

```bash
PYTHONPATH=tools/video /workspace/junior-high-tools-venv/bin/python - <<'PY'
import json
from pathlib import Path
from junior_high.practice import write_practice

source = json.loads(Path('docs/videos/english-junior-high-complete/lessons.json').read_text(encoding='utf-8'))
write_practice(source['episodes'], Path('/workspace/junior-high-series-output/practice-preview'))
PY
```

## 驗證與打包

美術檢查輸出到 repo 外，核對句卡／選項／跟讀字形範圍，並以負向對照確定能偵測遮字：

```bash
PYTHONPATH=tools/video /workspace/junior-high-tools-venv/bin/python -m junior_high.art_qa \
  --source docs/videos/english-junior-high-complete/lessons.json \
  --output /workspace/junior-high-series-output/art-qa
```

完整系列驗證要求 72 集全部完成，並對照當前作者來源：

```bash
/workspace/junior-high-tools-venv/bin/python tools/video/junior_high/verify_series.py \
  --source docs/videos/english-junior-high-complete/lessons.json \
  --output /workspace/junior-high-series-output
```

製作途中可加 `--allow-partial`；缺集時仍是 `passed: false`／`status: partial`。可加 `--report /外部目錄/report.json` 另存檢查報告。完整驗證包含作者欄位與 `practice`、實測共用英文、回應留白、四語字幕時序、統一國中 renderer、媒體雜湊及成功完整解碼收據。

先檢查打包輸入而不替換 ZIP：

```bash
/workspace/junior-high-tools-venv/bin/python tools/video/junior_high/package_series.py \
  --source docs/videos/english-junior-high-complete/lessons.json \
  --resolved /workspace/junior-high-series-output/lessons.resolved.json \
  --output /workspace/junior-high-series-output \
  --check-only
```

移除 `--check-only` 產生六個分季包及整套包；加 `--seasons-only` 可略過整套 ZIP。打包必須通過完整影音准入，且 resolved 保留當前所有作者欄位；舊 resolved 和舊影片彼此一致，也不能取代目前原稿。工具先建立暫存 ZIP、核對成員與 CRC，再於來源與 resolved 指紋仍相符時替換交付檔。

預定交付名稱：

- `Sunny_Pip_Junior_High_Season_01.zip` 至 `Sunny_Pip_Junior_High_Season_06.zip`
- `Sunny_Pip_Junior_High_72_Episodes.zip`
- `國中英文72集課程目錄.csv`
- `Practice.html`、`Practice.pdf`

每個季包只含該季十二集、相應離線播放器、課程目錄及練習；不放入語音快取、字型原檔或製作日誌。打包紀錄在 `package-checks.json`。程式檢查沿用 `npm run test:tools` 與 `npm run check:tasks`；合成 fixture 的單元測試不能代替真實媒體解碼，播放器模擬也不能代替瀏覽器實播。

## 交付記錄

本文件描述課程範圍、製作方法與驗證要求。完成集數、實測總時長、包大小、字型與交付雜湊、PDF 頁數及實播檢查結果，應於最終交付後依報告補入；此處不預先宣告製作完成。
