# codex-practical-12-app：換一段對話也能接著做：用檔案交接，先驗過期說法（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

上個對話寫『週報全部完成』，新對話沒有那些細節。本集的handoff故意含過期宣告，教你以現有檔案和真相接手。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：11。本片自己包含完整準備，不要求觀眾先看 `codex-practical-12-cli` 或使用它的成果。

1. 寫出含來源版本、實際狀態、未完成項與下一步的handoff。
2. 讓新對話先核對程式和測試，識別教材故意過期的完成宣告。
3. 把接手的第一個任務限制為可驗收的小步，不依賴上一段對話記憶。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 12 集](../../lessons/12.md)。當集材料：[README](../../materials/lessons/12/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/12/acceptance.md)、[答案](../../materials/lessons/12/answers.md)。

只從自己的 `12-app` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-12-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/12`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\12-app'
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

在同一個當集本機專案新開聊天，只提供 docs/handoff.md 路徑。讓新聊天自行讀現有檔案與測試，畫面取證要顯示新的聊天及來源，不把 CLI resume 或舊聊天答覆當成 App 接手。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
你是新的接手對話。先讀docs/handoff.md，再自行核對node --test與固定週報命令。不把檔案中的『已完成』當成事實；逐條標記已驗證、過期、未驗證，並附檔案或輸出。先修正交接狀態，再提出一個最小下一步；不得重新搭建專案或補造舊任務時間。
```



## 主案例操作與驗收

1. 在第一段對話整理任務、範圍、實際測試、尚未做的UI與來源，寫入docs/handoff.md；保留日期與當前本機commit（若有）。
2. 結束這一段工作，開本入口的新對話，明確只從檔案接手，不貼上整份舊聊天。
3. 新對話讀現有handoff、跑測試和報表；對照固定真相找出過期宣告，列清何者有證據。
4. 把核對後的狀態寫回handoff，附可複製的下一步與未完成項；另一入口仍用自己的副本。

讀者親自重跑，而不是只讀模型回報：

```powershell
node --test
$LASTEXITCODE
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11
```

網站確認：

```powershell
py -m http.server 4173 --bind 127.0.0.1
```

另開瀏覽器至 `http://127.0.0.1:4173/`。這是本機練習，先開乾淨的瀏覽器 profile／該來源的練習資料；不要清除其他網站的資料。服務所在目錄必須是這個入口的工作副本。用 Ctrl+C 停服務後，才換另一份副本佔用相同 port。

- handoff不把作者reference、檔案預期、測試綠與原生UI驗收混在一起。
- 新對話能指出過期項並根據實際原始檔繼續，不依賴口頭宣稱。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`docs/handoff.md`、`core.mjs`、`report.mjs`、`fixtures/tasks.json`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 新對話接手與過期偵測未實跑；docs/handoff.md只是作者用於演練的輸入。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

新模型重複『前一位已驗證』卻沒跑；要求引用當前命令與輸出。若無法執行，標未驗證並保留下一步，不把讀稿當驗收。

```text
你沿用了handoff中的過期『全部通過』。請重新按現有core、fixture、node --test與報告輸出核對，修訂狀態；沒有執行證據就寫未驗證，保持其他專案內容不動。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

故意把handoff中的一個區間或檔名改成舊值，新開對話核對它是否發現，並記錄修正前後文字。

完整材料與答案：answers.md 的第 12 集；答案含來源、狀態、驗證命令、未完成項與下一步，過期說明必須以現存證據修正。 亦見 [answers.md](../../materials/lessons/12/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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
