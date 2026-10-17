# CLI 試製 brief｜實跑綁定補記

此 brief 複製自系列 01 CLI 企劃，保留其教案；以下實際選用 **exec 只讀檢查**。TUI 流程仍為可選待拍 runbook，不能宣稱已錄製。真實基線模型執行已完成，逐項證據在 author-evidence.json。網站和 reference 驗證是作者另跑，沒有本輪模型實作修補。獨立重做、查核與媒體的最新狀態見 [PRODUCTION-STATE.md](PRODUCTION-STATE.md)。

## 站主觀點

已會用 Codex 的觀眾需要判斷工作是否真的完成的方法。先讓觀眾在相同五檔起點讀出責任分界、解讀已知失敗，理解核心測試與瀏覽器驗證各自的界線；不能拿參考答案代替模型成果。

## 製作大綱

### 選項 A：從真實只讀检查，完成接手報告（推薦）
一行說明：先看2通過1失敗的成果與驗收，再準備五檔、讀分工、送精確提示、核對內外退出碼，啟動HTTP並與作者參考比較，最後交出下一輪範圍與變式。
開場鉤子：Codex說檢查完成，為什麼測試還有一個紅燈？先把這兩種完成分清楚，才能放心交辦下一步。

1. 用真實24事件、測試2/1和未改五檔展示可核對的成果。
2. 準備本課獨立材料，核對路徑、版本、五檔分工及精確只讀提示。
3. 執行只讀exec，逐項讀測試、退出碼與未驗證事項。
4. 從file://失敗換到HTTP預覽；網站另驗，作者reference另比。
5. 寫窄範圍下一輪契約，完成全新start/reference比較練習並說明理由。

### 選項 B：用一個紅燈，學會判斷專案現況
一行說明：以「刻意篩選失敗是否代表全部壞掉」帶出相同完整流程，依序核對五檔、精確提示、實際測試、HTTP操作、作者對照及下一輪交接。
開場鉤子：一個測試失敗，網站就不能用嗎？用同一份五檔教材，說清楚已證明、尚未完成和還沒驗的部分。

兩個編排共用已實測的相同材料與驗收，不增加未實跑的比較或介面。A符合本系列先看成果、完整跟做的主線；B強調同一紅燈的判斷問題。既有稿件包含两種問題與同一完整順序，只有開場重點不同。既有審核工具需要2個選項才能自動評估，這不變更使用者批准的課程範圍。

## 觀眾看完能做到的事

在自己的 CLI 起點執行只讀檢查，核對五檔、2 通過 1 失敗與退出碼；用 HTTP 預覽核對既有功能；把篩選缺口交成有目標、範圍與驗收的下一輪任務；用全新副本完成兩版比較。

---

# codex-practical-01-cli：接手專案先建立基準：知道哪裡能跑、哪裡還沒做（CLI）

企劃／查核基準日：2026-10-11（Asia/Taipei）。exec只讀模型操作與結果已取得；獨立查核及媒體依 PRODUCTION-STATE 記錄。TUI仍是未錄製的可選入口。製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；系列企劃與本片作者稿均不等於已完成媒體。

## 觀眾問題與學習成果

第一次請 AI 做網站，回覆說完成，卻不知道應該先看什麼。本集從五個檔案與一個有理由的紅燈開始，讓第一項工作有起點、差異與終點。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：無。本片自己包含完整準備，不要求觀眾先看 `codex-practical-01-app` 或使用它的成果。

1. 建立只含本集起始五檔的工作副本，跑出並解讀教材基準 2 通過／1 失敗。
2. 分辨起始版刻意未完成的篩選、作者參考版 3 通過與模型實作成果三種狀態。
3. 用本機 HTTP 預覽驗證已存在的新增、完成與儲存，寫出第 03 集要接手的範圍。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在終端機與 Codex CLI TUI／非互動命令；網站行為另外用真正瀏覽器確認。不能用 App 的畫面或聊天替代 CLI 的工具與退出狀態。

完整共通教案：[第 01 集](../codex-practical-series/lessons/01.md)。當集材料：[README](../codex-practical-series/materials/lessons/01/README.md)、ZIP根目錄的 `start/`、`reference/`、`challenge/`、[驗收](../codex-practical-series/materials/lessons/01/acceptance.md)、[答案](../codex-practical-series/materials/lessons/01/answers.md)。

只從自己的 `01-cli` 工作副本開始，reference 保留在另一個目錄。01 使用原 Small Steps 的 `mokaair-codex-todo-v1`。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js22以上相容版本、Python3與Codex CLI；沒有npm dependencies，本片exec不要求Git。完整解壓本課ZIP到新的資料夾，再把下方 `$lessonSource` 換成該目錄；它應直接包含start、reference、challenge與baseline-prompt.txt。repository只保存說明，不包含snapshot目錄。

```powershell
$lessonSource = 'C:\codex-practice\01-materials' # 本課ZIP完整解壓目錄；請換成自己的路徑
if (-not (Test-Path -LiteralPath (Join-Path $lessonSource 'start'))) { throw '先產生或解壓教材，再指定真正的01教材包。' }
$lessonWork = 'C:\codex-practice\01-cli'
if (Test-Path -LiteralPath $lessonWork) { throw '副本已存在；保留它，選新的路徑。' }
New-Item -ItemType Directory -Path $lessonWork | Out-Null
Get-ChildItem -LiteralPath $lessonSource -Force | Copy-Item -Destination $lessonWork -Recurse
Set-Location -LiteralPath (Join-Path $lessonWork 'start')
Get-Location
Get-ChildItem -Name
node --version
node --test core.test.mjs
$LASTEXITCODE
```

完整01包的baseline-prompt.txt保留在start上一層，与主稿exec命令一致；別只複製五檔後漏掉提示檔。

保留起始資料和舊副本；需重新演練就用新路徑。不直接在 repository 的 start 或 reference 修改，避免混淆題目與答案。

## 原生入口與完整輸入

本片實際使用exec讀取baseline-prompt.txt，完整argv、事件與報告已保存。主稿提供PowerShell可重做命令；既有TUI入口僅供另外跟做的未錄製runbook。reference對照在另一個副本，不能冒充模型修復。首次登入由讀者完成。

互動 TUI 啟動前執行 `codex --version` 和 `codex --help`，保留本機版本。斜線指令如 `/plan`、`/agent` 屬於 TUI；`codex exec` 不具相同互動控制。
本段是系列的**未執行建議提示**；本片真實執行的精確提示另見baseline-prompt.txt與author-evidence.json。對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
先只讀，不修改任何檔案。讀 index.html、style.css、app.js、core.mjs、core.test.mjs，指出畫面、資料邏輯與測試分工。執行 node --test core.test.mjs，列出實際通過、失敗與退出碼，確認 visibleTasks 的篩選是教材刻意留給第03集的工作。不要修復或修改測試。最後交出當前基準、尚未完成項及我應操作的瀏覽器清單。
```



## 主案例操作與驗收

1. 在 start 工作副本跑 node --test core.test.mjs；教材預期 2 通過、1 失敗與非零退出碼，照實記錄，沒有修程式。
2. 讀 core.test.mjs 的 filters 斷言與 core.mjs 的 visibleTasks，說明失敗對應尚未完成的功能，不把刻意紅燈當環境壞掉。
3. 啟動 start 的 HTTP 預覽，新增 Read/Build、完成 Read、重新整理；Active/Completed 尚未正確過濾是起始限制，記到待做。
4. 另複製 reference 到不同資料夾，跑相同測試作作者答案對照：預期3通過。記下第03集只補篩選與搜尋的下一步，不把reference當模型成果。

讀者親自重跑，而不是隻讀模型回報：

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
| 主操作 | baseline-prompt.txt與五檔只讀起點 | 檔案責任、測試基線、未驗證與下一輪 | exec真實完成，24事件；無改檔 |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | start 核心測試預期2通過/1失敗，作者reference預期3通過；本集不實作篩選。exec基準已取得，作者網站另外實跑；TUI未錄製。 | author-evidence.json |
| 故障對照 | file://兩個錯誤與HTTP操作 | 修正開啟方式後重做 | 作者Edge13項紀錄；目錄錯誤仍為條件式runbook |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能證明檔案寫了什麼，不能證明此入口實作。

## 常見失敗與修復

找不到檔案或測試不是 2/1；先用 Get-Location 與 Get-ChildItem 查根目錄，不為了湊結果改測試。若瀏覽器看得到網站卻不載入模組，確認使用 http://127.0.0.1:4173 而不是 file://。

```text
我的工作目錄或HTTP預覽不對。先不要改程式；核對Get-Location、五份起始檔、node --version和啟動命令，指出應重做哪一步。測試2通過1失敗是本集預期，不要為它改測試。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

在兩份全新副本分別執行 start 與 reference 的同一測試，說明為什麼只有起始版紅燈，再寫一段給第03集的窄範圍交接。

完整材料與答案：answers.md 的第 01 集；核對 start=2通過/1失敗、reference=3通過、兩份目錄及第03集待做scope，不修改產品程式碼。 亦見 [answers.md](../codex-practical-series/materials/lessons/01/answers.md) 和 `01/challenge/`（教材包）。
觀眾先說結果與原因，再操作；新資料的真相需自行重算。只複製參考成品不算完成變式。

## 大綱、證據前提與交付

固定章序：前 30 秒展示本例有用結果／已知缺口 → 為何選此做法 → 起始材料與完整輸入 → 逐步操作 → 核對證據 → 常見失敗 → 變式和留下／停止。依這個順序寫稿，不把安裝與功能名佔滿主要篇幅。

正式撰稿及製作前須取得：

- 此入口的新副本、完整 prompt、日期、工具版本、model、起始/修改雜湊與實際 diff；沒有修改的回合保留無變更證據。
- 命令原文、標準輸出／錯誤、exit/status 與來源資料真相；模型完成文字不足。
- CLI TUI／exec／review 的真實事件與結果；同時儲存對應檔案、測試和瀏覽器證據。
- 未參與撰稿者只憑本片材料重做：完成二到四項成果、解釋原因、排一次錯、完成變式。未能執行時如實記待驗，不把讀稿查核當學習完成。

通過後才寫正式稿、逐項 claims、獨立查核與聽稿，再走旁白、畫面、字幕、成片 QA。站主觀看、上傳、發布與程式部署各有自己的狀態；本 brief 不新增任何這些動作的核準。

## 官方來源

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日檔案，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
