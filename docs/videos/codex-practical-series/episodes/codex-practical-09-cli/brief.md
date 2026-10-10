# codex-practical-09-cli：完成時間不能用猜的：升級資料並做出可信週報（CLI）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；CLI 模型操作與結果 pending_run；真實執行後另記收據。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

以前只存 completed=true，現在要問『這週完成幾件』。沒有時間的舊任務不能算成今天完成，本集把資料遷移、時間邊界與週報接成一個可信流程。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：08。本片自己包含完整準備，不要求觀眾先看 `codex-practical-09-app` 或使用它的成果。

1. 把 v1 任務升級成有 completedAt 的 v2，舊完成任務保持時間未知。
2. 用臺灣日曆日的含首尾週區間算週報，區分已知完成、待辦、未知時間。
3. 用固定五筆真相核對報表與資料儲存，避免把現在時間補給舊任務。
4. 分別匯入合法 JSON/CSV 與非法 CSV，核對整批拒絕不造成部分寫入，且既有任務保留。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在終端機與 Codex CLI TUI／非互動命令；網站行為另外用真正瀏覽器確認。不能用 App 的畫面或聊天替代 CLI 的工具與退出狀態。

完整共通教案：[第 09 集](../../lessons/09.md)。當集材料：[README](../../materials/lessons/09/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/09/acceptance.md)、[答案](../../materials/lessons/09/answers.md)。

只從自己的 `09-cli` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-09-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/09`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\09-cli'
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

在 `C:\codex-practice\09-cli` 的 PowerShell 開互動 TUI，命令為 `codex -C . --sandbox workspace-write`；先貼要求確認 cwd，再送本集完整任務。退出 TUI 後自己跑驗收，將實際 exit code 與輸出和來源檔核對。保留原本的核準規則，不使用繞過核准或沙盒的捷徑。

互動 TUI 啟動前執行 `codex --version` 和 `codex --help`，保留本機版本。斜線指令如 `/plan`、`/agent` 屬於 TUI；`codex exec` 不具相同互動控制。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
先核對作者提供的 v2/JSON/CSV/儲存與 UI 接線支架；它們不是本次模型生成成果。檢查 v1 的 id/title/completed 遷移為 v2 的 completedAt 契約：canonical UTC 字串或 null。舊 completed=true 但無時間的任務保持 null，另列時間未知；不能補現在時間。新完成記時間，取消完成清成 null。週報 --from 2026-10-05 --to 2026-10-11 依 Asia/Taipei 日曆日含首尾；讀固定五筆 fixture，驗 total5、completedInWeek2、pending1、unknownCompleted1，保留來源資料。主修改只限 core.mjs、report.mjs；可新增 tests/data-boundary.test.mjs 測未覆蓋的日期邊界，既有測試與來源檔保持不變。用 fixtures/tasks.json/tasks.csv 核對合法整批匯入，用 fixtures/invalid.csv 核對整批拒絕；先保存基準再修週報台北日期邊界缺陷。作者 IO 支架、核對既有契約與模型真正新增/修正分別回報，實際 diff 才能支持成果。
```



## 主案例操作與驗收

1. 先讀 fixtures/tasks.json 的五筆資料，手算兩筆本週完成、一筆待辦、一筆完成時間未知、一筆週前完成。
2. 核對 v1→v2 遷移：完成標記不被抹掉，未知時間仍null；驗證與移轉完成才寫v2，保留v1鍵。
3. 執行固定週報核對 5/2/1/1；另查 --from 2026-10-11 --to 2026-10-11，boundary 的 2026-10-10T22:00:00.000Z 是台北 11 日，預期本日已知完成 1。新增 data-boundary 測試先紅再修，UTC 儲存不改。
4. 瀏覽器新增完成記時間、取消完成清時間；reload後核對 v2，舊完成未知仍排除於本週完成數。


JSON／CSV 與遷移的固定輸入：

- 唯讀 `fixtures/legacy-v1.json`；既有 `core.test.mjs` 與 `tests/storage.test.mjs` 核對 v1→v2，舊完成時間保持 null、v1 鍵保留。
- 用新的練習瀏覽器資料，點「匯入 JSON 或 CSV」選 `fixtures/tasks.json`，週報日期 2026-10-05／2026-10-11，點「產生週報」；預期 total 5、completedInWeek 2、pending 1、unknownCompleted 1、timezone Asia/Taipei。
- 先匯出或保存目前虛構資料，再以新 profile 或本頁「重設目前練習資料」準備空清單，選 `fixtures/tasks.csv`；相同資料應得到相同週報。CLI 的 report.mjs 讀 JSON，不把 CSV 檔直接交給 JSON CLI。
- 在合法五筆仍存在時匯入 `fixtures/invalid.csv`；預期整批拒絕，原五筆 ID、內容與順序不變。紀錄實際錯誤、UI 訊息與重跑週報；不修改 fixture 讓它成功。

讀者親自重跑，而不是只讀模型回報：

```powershell
node --test
$LASTEXITCODE
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11
node report.mjs fixtures/tasks.json --from 2026-10-11 --to 2026-10-11
```

網站確認：

```powershell
py -m http.server 4173 --bind 127.0.0.1
```

另開瀏覽器至 `http://127.0.0.1:4173/`。這是本機練習，先開乾淨的瀏覽器 profile／該來源的練習資料；不要清除其他網站的資料。服務所在目錄必須是這個入口的工作副本。用 Ctrl+C 停服務後，才換另一份副本佔用相同 port。

- 週報 total=5、completedInWeek=2、pending=1、unknownCompleted=1，timezone=Asia/Taipei。
- 週區間含10月5日00:00與10月11日23:59:59.999臺灣時間；未知時間不落入任意週。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`core.mjs`、`app.mjs`、`report.mjs`、`fixtures/tasks.json`、`fixtures/tasks.csv`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 固定 fixture 真相是作者制定；模型遷移、週報輸出與瀏覽器持久化結果仍待當集實跑。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

週報把未知當本週或出現時區差一天；先對照原 fixture、日期到UTC的邊界及 completedAt，不拿locale字串比大小。遷移出錯時保留v1並拒寫v2，不清空原資料。

```text
週報目前把舊 completed=true/null 算成本週。只修分類與遷移，不給舊任務補時間；加未知、週前、首尾邊界測試，再用固定命令核對四個數字與timezone。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

把查詢改成 --from 2026-10-12 --to 2026-10-18；先手算既有五筆應為本週0，另加一筆落在臺灣週一00:00的完成任務驗證邊界。

完整材料與答案：answers.md 的第 09 集；原fixture的下一週completedInWeek=0，新增邊界要與canonical UTC相符，unknown仍1。 亦見 [answers.md](../../materials/lessons/09/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
