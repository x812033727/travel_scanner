# Sunny 與 Pip：我的英文小教室

使用者在幼兒 48 集完成、建立 [PR #1376](https://github.com/x812033727/travel_scanner/pull/1376) 後，明確選擇「開始國小英文系列」。本次製作國小低年級第一季 12 集；本季已完成本機影片、播放器與 ZIP，實測結果見下方交付紀錄。

## 教學範圍與進階

適合約 6–8 歲、已接觸幼兒系列基礎詞彙的孩子，也可由陪伴者先示範再參與。以完整句子、課堂互動與句子跟讀銜接幼兒階段；不把看過影片等同正式英語程度或獨立閱讀能力。

國小階段後續可依低、中、高年級推進：低年級從自我與教室出發，延伸家庭、日常生活與簡短故事；中年級增加時間、地點、生活任務與段落理解；高年級練習敘述經驗、比較、說明理由與小型專題。每季以 12 集為單位，依上一季的實際學習回饋調整；本次只有低年級第一季進入製作。

| 集數 | 中文標題 | 英文標題 | 主要句型／任務 |
|---|---|---|---|
| 01 | 走進英文小教室 | Hello, Class! | My name is Sunny / Pip. |
| 02 | 今天的心情 | How Are You Today? | I'm happy / sad today. |
| 03 | 教室裡的禮貌用語 | Please, in Our Classroom | Please stand up / sit down / clap your hands. |
| 04 | 這是什麼？ | What's This? | It's a book / pencil. |
| 05 | 有禮貌地提出請求 | Asking Politely | May I have…? / Here you are. / Thank you. |
| 06 | 它是什麼顏色？ | What Color Is It? | It is red / blue / yellow. |
| 07 | 有幾塊餅乾？ | How Many Cookies? | There are two / three / four cookies. |
| 08 | 你會做什麼？ | What Can You Do? | I can… / Can you…? / Yes, I can. |
| 09 | 球在哪裡？ | Where Is the Ball? | The ball is on / under the table / in the box. |
| 10 | 看圖跟讀小句子 | Let's Read a Sentence | I see a red ball / a blue ball / three cookies. |
| 11 | 英文教室小故事 | A Tiny Classroom Story | 自介→請求文具→道謝→顏色問答 |
| 12 | 我的英文小教室任務 | My English Classroom Mission | 整合物品請求、數量、位置與自介 |

每集十幕、至少三題聽力選圖及一幕句子跟讀。一般練習留白 5 秒，聽力題在英文提示結束後完整留白 6 秒，再揭示英文答案與翻譯。句子跟讀保留英文示範，屬有示範的閱讀教學活動；聽力題仍是聽力評量。第 10 集另外引導觀察大寫、字間空格與句末句點，不把字母名稱當成音素教學。

目標每集約 3–4 分鐘；最終時長由五語實測配音決定，驗證範圍為 3–5 分鐘，不裁短英文發音以硬塞進預設秒數。這是沿用既有兒童短課程的製作格式，與一般長片流程分開。

## 字幕、配音與畫面契約

- 英文固定燒錄在影片畫面，沒有獨立英文 CC。
- 五組音軌：原英文、繁體中文、簡體中文、日文、韓文。四種翻譯語言與後台語言選項一致。
- 四組可選 CC：繁體中文、簡體中文、日文、韓文；配音與 CC 可獨立選擇。
- 只翻譯教學指令；每一段英文示範使用相同英文音檔放入五組音軌。
- 聽力題的指令、英文畫面、翻譯 CC、角色姓名與答案框均不能提早洩漏目標。選項位置輪替。
- 沿用 Sunny／Pip 原創角色，新增教室背景、書本、鉛筆與單獨角色選項。位置圖中的 on／under 使用同一張矮桌，in 使用箱子。
- 接受指圖或口頭回應代替起身、跳躍等動作；不把 sad 說成錯誤心情，也不要求孩子提供姓名等個人資料。

本機試製使用 Microsoft Edge read-aloud 合成語音（Jenny、HsiaoChen、Xiaoxiao、Nanami、SunHi），不是後台設定的正式聲音。切換正式聲音時須重新量測、對時與驗證；本次不包含後台整合或發布。

## 來源與製作流程

- `part01-04.json`、`part05-08.json`、`part09-12.json`：各四集的五語作者來源。
- `lessons.json`：依集數合併的唯一製作輸入；不得只改分檔或只改合併檔。
- `tools/video/elementary/`：國小畫面 profile、CLI、驗證與單季打包；重用幼兒配音與媒體處理函式。
- 媒體：`/workspace/elementary-season01-output`，位於公開 repository 外。幼兒原成片與 ZIP 不改寫。

每集保留來源指紋、renderer profile 與相依檔雜湊、Pillow 版本、獨立音檔／字幕與最終成片的完整性收據。續跑、重封裝與打包均核對來源及實際檔案，不把不同輪次的畫面、音檔或字幕混用。國小 profile 與幼兒預設 renderer 分開；共享工具的預設行為必須維持既有 48 集收據可驗證。

## 重建命令

從 repo 根目錄執行，使用 Python 3、Pillow、FFmpeg／FFprobe 與 `edge-tts`。`--plan-only` 不發出語音請求。可沿用既有內容雜湊語音快取；同一輸出目錄只開一個配音 producer。

```bash
python3 tools/video/preschool/audio.py \
  --source docs/videos/english-elementary-series/lessons.json \
  --output /workspace/elementary-season01-output --plan-only

# 配音；先完成此步，也可在另一個終端啟動下方 --watch-audio 渲染。
PYTHONPATH=/tmp/preschool-simd:/tmp/preschool-tts \
python3 tools/video/preschool/audio.py \
  --source docs/videos/english-elementary-series/lessons.json \
  --output /workspace/elementary-season01-output \
  --cache-dir /workspace/preschool-pilot-output/.tts-cache

PYTHONPATH=/tmp/preschool-simd:/tmp/preschool-tts \
python3 tools/video/elementary/batch.py \
  --source docs/videos/english-elementary-series/lessons.json \
  --output /workspace/elementary-season01-output --workers 3 --watch-audio

PYTHONPATH=/tmp/preschool-simd:/tmp/preschool-tts \
python3 tools/video/elementary/verify_series.py \
  --source docs/videos/english-elementary-series/lessons.json \
  --output /workspace/elementary-season01-output

python3 tools/video/elementary/package_series.py \
  --resolved /workspace/elementary-season01-output/lessons.resolved.json \
  --output /workspace/elementary-season01-output

node tools/video/preschool/check-player.mjs \
  /workspace/elementary-season01-output/index.html \
  --expect-episodes 12 --expect-seasons 1 --expect-per-season 12
```

`/tmp/preschool-simd`、`/tmp/preschool-tts` 是本次環境的套件位置；在其他環境換成實際安裝位置。一般 Pillow 也能重建；新渲染會以實際版本建立不同快取。固定本季渲染 15 fps、成片 720p／30 fps。

`verify_series.py --allow-partial` 可看製作中進度，缺集仍保留 `passed:false`；`--report /tmp/…json` 可將報告寫至其他位置。`package_series.py --check-only` 只驗證不打包。可選的 `check-browser.mjs <output>` 使用本機 Chromium 與實際媒體做播放抽測；瀏覽器禁止 `file://` 時會非零退出並保存失敗原因，不會宣稱實播通過。

## 驗證與交付紀錄

完成日期：2026-10-08。12 集、120 幕、36 題聽力與 15 幕句子跟讀，總長 **2,162.36 秒，約 36.04 分鐘**；各集約 3 分鐘。第 7、8、11 集依完整語音略微延長，未截短示範或作答時間。

- 交付包：`/workspace/elementary-season01-output/Sunny_Pip_Elementary_Season_01.zip`，**157,405,581 bytes（157.4 MB）**，207 個檔案。
- 全季播放器：`/workspace/elementary-season01-output/index.html`。下載包完整解壓後，開啟 `Elementary_Season_01/index.html`；影片也可用 VLC 切換五音軌與四 CC。
- 課程目錄：`國小低年級英文第一季12集課程目錄.csv`，UTF-8 BOM，共 12 列課程。
- `curriculum-checks.json`：12/12 全部通過，0 errors；包含來源、共用英文示範、實測時序、字幕留白與揭答、五音軌／四 CC、renderer、成片及獨立檔案完整性。每集製作時已完整 FFmpeg 解碼所有影音串流，驗證核對目前檔案 SHA-256 與成功解碼收據一致。
- `package-checks.json`：ZIP CRC、內容數量及 SHA-256 通過。已從實際 ZIP 取出播放器作 jsdom 操作檢查，並核對其全部 84 個相對影片、音軌、封面路徑存在；報告在 `packaged-player-checks.json`。外部全季播放器檢查在 `player-checks.json`。
- `source-checks.json`：12 集來源合併一致、五語文稿交叉審查、相同英文句的翻譯一致。`art-validation.json`：92 種支持圖像、120 個正式場景、360 條文字及 36 題揭答前畫面檢查通過；已目視檢查畫面集與代表性成片截圖。
- `audio-level-checks.json`：第 11 集五語音檔全長音量抽查有有效聲音、無樣本峰值削波。這不等於逐集人耳發音審查。
- 第 5 集採中性標題 “Asking Politely”，避免原標題 “May I Have a Pencil?” 在聽力題上方提示答案；已依修正後來源重製並驗證。
- `browser-checks.json` 保留 `passed:false`：Chromium 151 啟動後被此環境的管理員政策擋住 `file://` 頁面（`ERR_BLOCKED_BY_ADMINISTRATOR`），未執行實際瀏覽器播放，不以 jsdom 檢查冒充實播。
- repository 檢查：`npm run test:tools` 2,008 passed／3 skipped，其中含 10 個國小 profile／batch 與 10 個幼兒完整性回歸；`npm run check:tasks` 通過。原幼兒 48 集唯讀相容性核對仍為 48/48、0 errors，紀錄為 `preschool-compatibility-checks.json`。

媒體、ZIP 與快取均留在公開 repo 外。尚未接後台正式聲音、上傳或發布；未宣稱完成逐集人耳全程聽審。
