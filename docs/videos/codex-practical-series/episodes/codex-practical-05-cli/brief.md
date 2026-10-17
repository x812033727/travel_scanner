# codex-practical-05-cli：兩筆同名任務一起消失：用 ID 修對真正的 bug（CLI）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；CLI 模型操作與結果 pending_run；真實執行後另記收據。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

畫面上只刪一筆『寫報告』，另一筆同名任務也消失。這是一個有清楚真相的 bug，比要求模型『檢查所有問題』更能教會排錯。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：04。本片自己包含完整準備，不要求觀眾先看 `codex-practical-05-app` 或使用它的成果。

1. 從同名但不同 ID 的兩筆任務重現錯刪，寫出預期與實際差異。
2. 辨認位置、標題與穩定 ID 的用途，限制刪除只命中選定 ID。
3. 用既有 identity 回歸測試與篩選後再次刪除，確認修復涵蓋同名情境。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在終端機與 Codex CLI TUI／非互動命令；網站行為另外用真正瀏覽器確認。不能用 App 的畫面或聊天替代 CLI 的工具與退出狀態。

完整共通教案：[第 05 集](../../lessons/05.md)。當集材料：[README](../../materials/lessons/05/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/05/acceptance.md)、[答案](../../materials/lessons/05/answers.md)。

只從自己的 `05-cli` 工作副本開始，reference 保留在另一個目錄。02–08 使用獨立練習鍵 `mokaair-codex-practical-v1`，資料為 `id/title/completed`。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-05-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/05`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\05-cli'
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

在 `C:\codex-practice\05-cli` 的 PowerShell 開互動 TUI，命令為 `codex -C . --sandbox workspace-write`；先貼要求確認 cwd，再送本集完整任務。退出 TUI 後自己跑驗收，將實際 exit code 與輸出和來源檔核對。保留原本的核準規則，不使用繞過核准或沙盒的捷徑。

互動 TUI 啟動前執行 `codex --version` 和 `codex --help`，保留本機版本。斜線指令如 `/plan`、`/agent` 屬於 TUI；`codex exec` 不具相同互動控制。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
本集 start 的刪除錯把 title 當身分。同名不同 ID 的兩筆任務，刪除第一筆應保留第二筆。先重現並執行既有 tests/identity.test.mjs，再只修 core.mjs 的刪除邏輯；只讀 app.mjs 核對傳入的是 task.id；不要禁止同名任務，不改資料格式。跑 node --test，回報觸發條件、根因與修復證據。
```



## 主案例操作與驗收

1. 新增兩筆『寫報告』，確認它們的 id 不同；先只刪第一筆，記錄本入口真正結果。
2. 閱讀 tests/identity.test.mjs 的同名三筆固定輸入，執行它並保留實際失敗；另用兩筆 id=a/b 的命令列案例核對刪 a 後應剩 b，不改既有測試。
3. 看 Codex 是否沿刪除控制項→ID→核心函式找到根因；拒絕用禁同名或重建全部資料遮掩錯誤。
4. 修後重跑測試；將其中一筆標完成，在 Completed 篩選內刪除，再回 All 核對另一筆仍在。

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

- delete a 只移除 a；未選中的 b 的 title、completed 與順序維持。
- 新增兩個同名任務仍然允許，篩選位置不被當成原始索引。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`app.mjs`、`core.mjs`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 起始缺陷是作者刻意放入；模型重現、修復、回歸紅綠與瀏覽器操作待本入口實跑。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

模型改成禁止同名，或測試用唯一標題所以看似通過；拿固定 a/b 同名輸入重跑。畫面仍錯就查 dataset/taskId 與事件閉包，不只看核心函式。

```text
這個修法改成禁止同名，沒有修到身分錯誤。保留允許同名的原需求；用 id=a/b、同 title 的案例修刪除，只變更需要的函式與回歸測試。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

在三筆任務中加入兩筆同名，其中一筆完成；搜尋後刪未完成那筆，核對另一筆與第三筆都留下。

完整材料與答案：answers.md 的第 05 集；參考實作應以穩定 id 比較，測試必須包含同名、不同 ID 與篩選後行為。 亦見 [answers.md](../../materials/lessons/05/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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
