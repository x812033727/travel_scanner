# codex-practical-11-app：重構不要順手改行為：把重複週報邏輯收回核心（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

頁面和命令列各算一次完成數，遲早會修好一邊忘了另一邊。本集把重複邏輯收回核心，教你在行為不變的條件下重構。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：09、10。本片自己包含完整準備，不要求觀眾先看 `codex-practical-11-cli` 或使用它的成果。

1. 找到UI與CLI重複計算週報的位置，說明一個權威邏輯來源的用途。
2. 重構後以相同fixture證明欄位、區間與結果保持一致。
3. 用未知時間、區間邊界與輸入不變的測試守住外部行為。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 11 集](../../lessons/11.md)。當集材料：[README](../../materials/lessons/11/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/11/acceptance.md)、[答案](../../materials/lessons/11/answers.md)。

只從自己的 `11-app` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-11-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/11`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\11-app'
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

在原生桌面 App 加入這份本機資料夾 `C:\codex-practice\11-app`，新開屬於此專案的 Local 聊天。先請模型回報 cwd 和當集檔案，再貼本集完整任務。讀工具紀錄、開啟實際修改檔與 diff；自行執行驗收，在瀏覽器操作，而不是用模型的完成文字替代。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
這是行為不變的重構。report.mjs 有重複週報計算，改成呼叫 core.mjs 的 weeklyReport，讓UI與CLI共用。保留 CLI 引數、輸出欄位、timezone、含首尾規則與嚴格日曆錯誤行為；重構前後 2026-02-30 都須拒絕，不能順便放寬或加改行為；不得改fixture來通過。先記錄固定命令的before，再改、跑node --test與同命令after，逐欄位比對並確認原資料不變。
```



## 主案例操作與驗收

1. 先跑固定報告儲存before，並把日期/未知分類對到程式碼位置。
2. 找出report.mjs內的重複計算與core.weeklyReport邊界，確定抽取後誰負責解析引數、誰負責業務計算。
3. 讓Codex窄重構；對照diff確認沒有改輸出契約或新增套件。
4. 跑完整測試和同一報告儲存after，比較關鍵欄位與錯誤情況，UI再檢視相同周區間。

讀者親自重跑，而不是只讀模型回報：

```powershell
node --test
$LASTEXITCODE
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11
node report.mjs fixtures/tasks.json --from 2026-02-30 --to 2026-03-01
$LASTEXITCODE
```

網站確認：

```powershell
py -m http.server 4173 --bind 127.0.0.1
```

另開瀏覽器至 `http://127.0.0.1:4173/`。這是本機練習，先開乾淨的瀏覽器 profile／該來源的練習資料；不要清除其他網站的資料。服務所在目錄必須是這個入口的工作副本。用 Ctrl+C 停服務後，才換另一份副本佔用相同 port。

- before/after同fixture仍total5、completedInWeek2、pending1、unknownCompleted1、timezone一致。
- CLI仍能讀取同路徑與引數，輸入資料沒有被寫回或排序。

額外錯誤驗收：2026-02-30 的報告在 before/after 皆須非零，保留原始 stderr 與 exit code，不把改變錯誤接受條件稱作純重構。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`core.mjs`、`report.mjs`、`app.mjs`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 作者reference展示共用函式，Codex重構、before/after與相容驗收皆待實跑。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

模型順手升級schema或換欄位名；用before/after與原引數揭露相容性變化。測試綠但舊CLI指令碼不能用也是失敗，須恢復契約。

```text
這次是重構，不接受欄位/引數變化。恢復原CLI介面，只抽業務計算到weeklyReport；用原fixture與相同命令證明before/after一致，再列出真正減少的重複部分。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

加入「全部任務待辦」與「全部完成但時間未知」兩份小輸入，確認UI與CLI共用函式不會憑空算出本週完成。

完整材料與答案：answers.md 的第 11 集；對照weeklyReport與report入口職責、零完成情況和輸入不變。 亦見 [answers.md](../../materials/lessons/11/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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
