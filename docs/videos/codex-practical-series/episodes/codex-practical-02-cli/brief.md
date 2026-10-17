# codex-practical-02-cli：先把需求講清楚：用 Plan 寫出能開工的計畫（CLI）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；CLI 模型操作與結果 pending_run；真實執行後另記收據。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

上一個任務能跑了，下一個需求是『加搜尋』。如果不先決定搜尋物件與它和篩選的關係，模型可以做好另一個功能，卻沒有做好你的功能。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：01。本片自己包含完整準備，不要求觀眾先看 `codex-practical-02-app` 或使用它的成果。

1. 把搜尋與篩選需求寫成範圍、輸入、可觀察結果，去掉『做漂亮一點』這種不可驗收的要求。
2. 在真正的 Plan 模式先讀專案，再得到可執行的步驟與待確認事項。
3. 用不改產品程式的差異檢查，區分計畫、實作與驗收。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在終端機與 Codex CLI TUI／非互動命令；網站行為另外用真正瀏覽器確認。不能用 App 的畫面或聊天替代 CLI 的工具與退出狀態。

完整共通教案：[第 02 集](../../lessons/02.md)。當集材料：[README](../../materials/lessons/02/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/02/acceptance.md)、[答案](../../materials/lessons/02/answers.md)。

只從自己的 `02-cli` 工作副本開始，reference 保留在另一個目錄。02–08 使用獨立練習鍵 `mokaair-codex-practical-v1`，資料為 `id/title/completed`。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-02-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/02`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\02-cli'
if (Test-Path -LiteralPath $lessonWork) { throw '這個副本已存在；保留它，選一個新的工作路徑。' }
New-Item -ItemType Directory -Path $lessonWork | Out-Null
Get-ChildItem -LiteralPath $lessonSource -Force | Copy-Item -Destination $lessonWork -Recurse
Set-Location -LiteralPath $lessonWork
Get-Location
node --version
git --version
node --test
$LASTEXITCODE
```

保留起始資料和舊副本；需重新演練就用新路徑。不直接在 repository 的 start 或 reference 修改，避免混淆題目與答案。

## 原生入口與完整輸入

先啟動互動 TUI：codex -C . --sandbox read-only，再輸入 /plan 並確認模式。貼規劃 prompt；產品程式不得變更。/plan 是 TUI 控制，不放到 codex exec 的 prompt 裡當成切換模式。

互動 TUI 啟動前執行 `codex --version` 和 `codex --help`，保留本機版本。斜線指令如 `/plan`、`/agent` 屬於 TUI；`codex exec` 不具相同互動控制。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
這一回合只規劃，不修改任何檔案。讀 docs/task-brief.md 與 app.mjs、core.mjs、core.test.mjs。目標：標題搜尋 trim 後不分大小寫，和 All/Active/Completed 取交集；空搜尋保留現有篩選，無結果顯示空狀態。列出要改的範圍、測試與瀏覽器驗收；明說目前哪些步驟尚未執行，不加入後端、登入或新套件。
```



## 主案例操作與驗收

1. 先讀 docs/task-brief.md，寫下搜尋範圍與三個篩選的交集；使用三筆固定任務 Read、Build、Review 作輸入。
2. 進入本入口的 Plan 模式，核對模式提示，再送完整規劃要求；單寫『先規劃』不是切換模式的證據。
3. 把回覆依需求、檔案、步驟、測試四欄核對；若漏空字串或 Completed 交集，在同一規劃對話補問。
4. 將採用的計畫文字記入教材的 docs/plan.md，註明由讀者記錄；核對產品程式沒有變更，後續實作放到第 03 集。

讀者親自重跑，而不是只讀模型回報：

```powershell
node --test
$LASTEXITCODE
```

網站確認：

```powershell
py -m http.server 4173 --bind 127.0.0.1
```

另開瀏覽器至 `http://127.0.0.1:4173/`。這是本機練習，先開乾淨的瀏覽器 profile／該來源的練習資料；不要清除其他網站的資料。服務所在目錄必須是這個入口的工作副本。用 Ctrl+C 停服務後，才換另一份副本佔用相同 port。

- Read 未完成、Build 未完成、Review 完成；搜尋 re 配 Completed 預期只剩 Review。
- 本集只產生計畫與讀者的記錄；沒有聲稱搜尋已實作或瀏覽器已驗收。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`docs/task-brief.md`、`docs/plan.md`、`app.mjs`、`core.mjs`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 預期得到決策完整的計畫；模型文字、模式畫面與產品差異皆待本入口實跑，reference 計畫是作者範本。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

模型在 Plan 回合提出執行或程式已變更；先確認實際模式與變更範圍，將計畫記錄與產品變更分開。漏規格時回到完整輸入補條件，不只要求『更仔細』。

```text
請修訂計畫：目前漏了空搜尋、無結果與搜尋加 Completed 的交集。仍只規劃；逐條對應驗收案例，最後列出尚未執行的工作。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

把需求改成只搜尋 title，保留大小寫不敏感，但關鍵字為空時不過濾；自行給兩個正例、一個反例，判斷計畫是否包含它們。

完整材料與答案：answers.md 的第 02 集；核對搜尋不讀 id、trim 空白與交集，不以計畫篇幅評分。 亦見 [answers.md](../../materials/lessons/02/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [互動式 /plan 與開發指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
