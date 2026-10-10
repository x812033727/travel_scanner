# codex-practical-17-cli：把週報變成可重複工作：App 排程、CLI 非互動各自完成（CLI）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；CLI 模型操作與結果 pending_run；真實執行後另記收據。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

把提示放進排程，不等於每天會得到可信週報。本集先把一次執行講清楚，再處理無人看著時的失敗、記錄和停止方式。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：13、16。本片自己包含完整準備，不要求觀眾先看 `codex-practical-17-app` 或使用它的成果。

1. 先手動跑通固定週報與驗收，再為重複工作設定輸入與輸出記錄。
2. 在本入口完成一次真實執行並核對狀態、結果和失敗處理。
3. 區分App原生排程與CLI exec指令碼；兩套教材分別儲存證據，不拿一種成功代替另一種。

片長目標 18–25 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在終端機與 Codex CLI TUI／非互動命令；網站行為另外用真正瀏覽器確認。不能用 App 的畫面或聊天替代 CLI 的工具與退出狀態。

完整共通教案：[第 17 集](../../lessons/17.md)。當集材料：[README](../../materials/lessons/17/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/17/acceptance.md)、[答案](../../materials/lessons/17/answers.md)。

只從自己的 `17-cli` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-17-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/17`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\17-cli'
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

先 node exec-run.mjs --dry-run 核對 argv/schema（不呼叫模型）。登入與版本確認後，以 node exec-run.mjs --run run-01 執行一次；接著 node verify-result.mjs run-01 驗收。這個 runner 會儲存實際事件、最後回覆與 exit/status，120秒逾時仍保留。CLI 沒有 App 的 Scheduled 管理介面；本集的非互動執行是獨立實作，另加系統排程需保留它自己的工作目錄與日誌。

Windows 非互動 runner 需要原生執行檔。先以目前安裝的命令清單找 `.exe`，再記錄版本；不能把 `.ps1/.cmd` shim 直接當 spawnSync 的原生 binary。

```powershell
Get-Command codex -All | Select-Object CommandType, Source
$codexApplication = Get-Command codex -All | Where-Object { $_.CommandType -eq 'Application' -and $_.Source -match '\.exe$' } | Select-Object -First 1
if (-not $codexApplication) { throw '尚未找到原生 codex.exe；先核對安裝與路徑，不啟動模型。' }
$codexBinary = $codexApplication.Source
& $codexBinary --version
node exec-run.mjs --dry-run
node exec-run.mjs --run run-01 --codex $codexBinary
node verify-result.mjs run-01
```

本機查核例為 `<home>/AppData/Local/OpenAI/Codex/bin/0e65bed3f58320a4/codex.exe`（0.162.0-alpha.17.2）；hash 目錄與版本只作查核紀錄，讀者以自己的 Application 路徑和 --version 為準。先前 run-01 已存在就選新 run ID，不能覆蓋。

互動 TUI 啟動前執行 `codex --version` 和 `codex --help`，保留本機版本。斜線指令如 `/plan`、`/agent` 屬於 TUI；`codex exec` 不具相同互動控制。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
僅對這份練習任務資料製作2026-10-05到2026-10-11的Asia/Taipei週報，核對total5、completedInWeek2、pending1、unknownCompleted1。保留輸入、執行時間、工具版本、實際檢查和結果狀態。讀取或測試失敗就報告失敗，不猜數字、不修改資料、不傳送外部訊息。重複安排前先手動驗證一次；原生排程/exec的執行狀態需獨立核對。
```

```powershell
node exec-run.mjs --dry-run
node exec-run.mjs --run run-01
node verify-result.mjs run-01
```

## 主案例操作與驗收

1. 先跑node --test與固定報告，確保確定性任務本身正確；先用固定週區間，不在第一次加入動態『本週』計算。
2. 按本入口的完整流程手動執行一次，儲存prompt、執行記錄與結果，再獨立verify。
3. 演練讀不到fixture或輸出不完整的失敗，保留失敗記錄；恢復後使用新runID，不能覆蓋失敗證據。
4. App按docs/app-schedule.md設定、看真實執行後暫停；CLI執行exec-run並驗收，若另有系統排程只說明其獨立環境與日誌，不冒充App排程。

讀者親自重跑，而不是只讀模型回報：

```powershell
node --test
$LASTEXITCODE
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11
node exec-run.mjs --dry-run
```

網站確認：

```powershell
py -m http.server 4173 --bind 127.0.0.1
```

另開瀏覽器至 `http://127.0.0.1:4173/`。這是本機練習，先開乾淨的瀏覽器 profile／該來源的練習資料；不要清除其他網站的資料。服務所在目錄必須是這個入口的工作副本。用 Ctrl+C 停服務後，才換另一份副本佔用相同 port。

- 一次真實執行結果與fixture四個數字一致；來源、區間、timezone與執行狀態都有證據。
- 失敗沒有成功報告，歷史執行不被覆蓋；完成演練後App任務可暫停並讀回狀態。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`docs/app-schedule.md`、`exec-run.mjs`、`verify-result.mjs`、`report.mjs`、`fixtures/tasks.json` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | App排程與CLI模型執行均未建立/執行；只規劃固定輸入和驗證條件。結果生成前保持pending_run。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

App安排存在卻沒執行、電腦休眠、本地目錄不可用，或CLI exit0卻缺結果；分別查執行記錄、當前路徑與verify結果。預演dry-run沒有模型呼叫，不能稱自動週報完成。

```text
本次重複任務沒有可驗收結果。請保留當前runID與輸入，逐項核對啟動、fixture讀取、模型/指令碼輸出與verify；區分沒有執行與執行失敗，不覆蓋舊記錄、不自動補成功。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

把區間改為 2026-10-12..18，真跑一次並核對 completedInWeek 0、pending 1、unknownCompleted 1、total 5；再用不存在的來源製造保留紀錄的缺檔失敗，分清預檢失敗未呼叫模型與真正模型失敗。

新日期與新來源是獨立真批次變式；先核對原 fixture，使用全新 run ID。下面 --codex 使用前段已驗證的 `$codexBinary`：

```powershell
node report.mjs fixtures/tasks.json --from 2026-10-12 --to 2026-10-18
node exec-run.mjs --dry-run --input fixtures/tasks.json --from 2026-10-12 --to 2026-10-18
node exec-run.mjs --run run-next-week --input fixtures/tasks.json --from 2026-10-12 --to 2026-10-18 --codex $codexBinary
node verify-result.mjs run-next-week
node exec-run.mjs --run run-missing --input fixtures/missing.json --from 2026-10-12 --to 2026-10-18 --codex $codexBinary
$LASTEXITCODE
Get-Content -LiteralPath run-missing/status.json -Raw
node verify-result.mjs run-missing
$LASTEXITCODE
```

下一週結果預期 5/0/1/1；缺檔預期非零、status state=preflight_failed、modelInvoked=false、errorCode=ENOENT，保留 input/prompt/schema、空 events 和 stderr，verify 拒絕。缺檔在 provider 前被攔下；不宣稱模型跑失敗，不重新使用既有 run ID。input 必須在本課專案內，來源 hash、from/to/timezone 及實際 inputPath 留在本次收據。執行前均 pending_run。

CLI 的確定性失敗演練先執行 `node --test tests/automation.test.mjs`；測試內 synthetic events 是驗證器測試資料，不能當模型執行證據。真正 run-01 成功後可另做以下資料副本；這是明標的錯誤注入，保持原始 run-01 不變：

```powershell
if (Test-Path -LiteralPath verifier-wrong3) { throw '保留已有演練，改用新名字。' }
Copy-Item -LiteralPath run-01 -Destination verifier-wrong3 -Recurse
$candidate = Get-Content -LiteralPath verifier-wrong3/final.json -Raw | ConvertFrom-Json
$candidate.completedInWeek = 3
$candidate | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath verifier-wrong3/final.json -Encoding utf8
node verify-result.mjs verifier-wrong3
$LASTEXITCODE
```

預期是非零與 Report does not match source truth；執行前不填實際結果。runner 支援 --from/--to/--input，預設原固定週與 fixtures/tasks.json；驗證器使用本次 input/status 的實際參數、來源 hash 與事件核對真相，不硬編預設日期。上面錯數注入只作附加驗證器教學，真正遷移仍須完成下列新日期/缺檔流程。

完整材料與答案：answers.md 的第 17 集；按App執行/暫停讀回或CLI exec/verify的各自收據核對，dry-run與真實run分開。 亦見 [answers.md](../../materials/lessons/17/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [App 排程與執行條件](https://learn.chatgpt.com/docs/automations?surface=app)；2026-10-11 實際開啟官方頁。
- [非互動 exec 引數](https://learn.chatgpt.com/docs/developer-commands?surface=cli)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。

公開定位說明：`<home>` 與 `<repo>` 是去識別佔位，不供直接執行。精確路徑與未遮罩原始收據保存在 repo 外；既有收據 SHA-256 仍綁定原始位元組。
