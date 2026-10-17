# codex-practical-01-app：接手專案先建立基準：知道哪裡能跑、哪裡還沒做（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

第一次請 AI 做網站，回覆說完成，卻不知道應該先看什麼。本集從五個檔案與一個有理由的紅燈開始，讓第一項工作有起點、差異與終點。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：無。本片自己包含完整準備，不要求觀眾先看 `codex-practical-01-cli` 或使用它的成果。

1. 建立只含本集起始五檔的工作副本，跑出並解讀教材基準 2 通過／1 失敗。
2. 分辨起始版刻意未完成的篩選、作者參考版 3 通過與模型實作成果三種狀態。
3. 用本機 HTTP 預覽驗證已存在的新增、完成與儲存，寫出第 03 集要接手的範圍。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 01 集](../../lessons/01.md)。當集材料：[README](../../materials/lessons/01/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/01/acceptance.md)、[答案](../../materials/lessons/01/answers.md)。

只從自己的 `01-app` 工作副本開始，reference 保留在另一個目錄。01 使用原 Small Steps 的 `mokaair-codex-todo-v1`。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-01-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/01`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\01-app'
if (Test-Path -LiteralPath $lessonWork) { throw '這個副本已存在；保留它，選一個新的工作路徑。' }
New-Item -ItemType Directory -Path $lessonWork | Out-Null
Get-ChildItem -LiteralPath $lessonSource -Force | Copy-Item -Destination $lessonWork -Recurse
Set-Location -LiteralPath $lessonWork
Get-Location
node --version
git --version
node --test core.test.mjs
$LASTEXITCODE
```

保留起始資料和舊副本；需重新演練就用新路徑。不直接在 repository 的 start 或 reference 修改，避免混淆題目與答案。

## 原生入口與完整輸入

先在原生 App 的本機專案確認五個檔案，送出只讀要求。開啟它真正讀檔與執行測試的紀錄；在內建終端機或附屬終端機自行重跑。主畫面要能看到 start 的 2 通過／1 失敗，並把 reference 的 3 通過標成作者比較；沒有任何實作完成的宣稱。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
先只讀，不修改任何檔案。讀 index.html、style.css、app.js、core.mjs、core.test.mjs，指出畫面、資料邏輯與測試分工。執行 node --test core.test.mjs，列出實際通過、失敗與退出碼，確認 visibleTasks 的篩選是教材刻意留給第03集的工作。不要修復或修改測試。最後交出當前基準、尚未完成項及我應操作的瀏覽器清單。
```



## 主案例操作與驗收

1. 在 start 工作副本跑 node --test core.test.mjs；教材預期 2 通過、1 失敗與非零退出碼，照實記錄，沒有修程式。
2. 讀 core.test.mjs 的 filters 斷言與 core.mjs 的 visibleTasks，說明失敗對應尚未完成的功能，不把刻意紅燈當環境壞掉。
3. 啟動 start 的 HTTP 預覽，新增 Read/Build、完成 Read、重新整理；Active/Completed 尚未正確過濾是起始限制，記到待做。
4. 另複製 reference 到不同資料夾，跑相同測試作作者答案對照：預期3通過。記下第03集只補篩選與搜尋的下一步，不把reference當模型成果。

讀者親自重跑，而不是只讀模型回報：

```powershell
node --test core.test.mjs
$LASTEXITCODE
```

網站確認：

```powershell
py -m http.server 4173 --bind 127.0.0.1
```

另開瀏覽器至 `http://127.0.0.1:4173/`。這是本機練習，先開乾淨的瀏覽器 profile／該來源的練習資料；不要清除其他網站的資料。服務所在目錄必須是這個入口的工作副本。用 Ctrl+C 停服務後，才換另一份副本佔用相同 port。

- start 已有新增、完成、刪除及儲存；篩選尚未完成，切Active/Completed仍會顯示全部是要交接的缺口。
- reference 預期3通過；它是作者寫好的比較材料，沒有在本集請Codex實作。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`index.html`、`style.css`、`app.js`、`core.mjs`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | start 核心測試預期2通過/1失敗，作者reference預期3通過；本集不實作篩選。模型的只讀基準核對與本入口畫面仍待實跑。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

找不到檔案或測試不是 2/1；先用 Get-Location 與 Get-ChildItem 查根目錄，不為了湊結果改測試。若瀏覽器看得到網站卻不載入模組，確認使用 http://127.0.0.1:4173 而不是 file://。

```text
我的工作目錄或HTTP預覽不對。先不要改程式；核對Get-Location、五份起始檔、node --version和啟動命令，指出應重做哪一步。測試2通過1失敗是本集預期，不要為它改測試。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

在兩份全新副本分別執行 start 與 reference 的同一測試，說明為什麼只有起始版紅燈，再寫一段給第03集的窄範圍交接。

完整材料與答案：answers.md 的第 01 集；核對 start=2通過/1失敗、reference=3通過、兩份目錄及第03集待做scope，不修改產品程式碼。 亦見 [answers.md](../../materials/lessons/01/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
觀眾先說結果與原因，再操作；新資料的真相需自行重算。只複製參考成品不算完成變式。

## 大綱、證據前提與交付

固定章序：前 30 秒展示本例有用結果／已知缺口 → 為何選此做法 → 起始材料與完整輸入 → 逐步操作 → 核對證據 → 常見失敗 → 變式和留下／停止。依這個順序寫稿，不把安裝與功能名佔滿主要篇幅。

正式撰稿及製作前須取得：

- 此入口的新副本、完整 prompt、日期、工具版本、model、起始/修改雜湊與實際 diff；沒有修改的回合保留無變更證據。
- 命令原文、標準輸出／錯誤、exit/status 與來源資料真相；模型完成文字不足。
- 原生 App 專案、模式或功能動作與結果的真實畫面。現在工具不能讀原生 UI，保持 pending_capture，不能以 CLI 或網頁檔案補位。
- 未參與撰稿者只憑本片材料重做：完成二到四項成果、解釋原因、排一次錯、完成變式。未能執行時如實記待驗，不把讀稿查核當學習完成。

通過後才寫正式稿、逐項 claims、獨立查核與聽稿，再走旁白、畫面、字幕、成片 QA。站主觀看、上傳、發布與程式部署各有自己的狀態；本 brief 不新增任何這些動作的核準。

## 官方來源

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
