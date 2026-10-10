# codex-practical-04-app：寫一份有用的 AGENTS.md：每次都能照規矩交付（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

每次都要重說『不要加套件、保留儲存資料、列出測試』。本集只寫這個小專案真正需要的規則，再用一次變更驗證效果。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：03。本片自己包含完整準備，不要求觀眾先看 `codex-practical-04-cli` 或使用它的成果。

1. 把經常重貼的範圍、測試與回報要求寫成當集專案的 AGENTS.md。
2. 在新對話只讀驗收，核對規則是否被讀取、資料真相與實際回報是否相符。
3. 區分當次需求、專案指示與強制測試，避免把 Markdown 當成硬性阻擋。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 04 集](../../lessons/04.md)。當集材料：[README](../../materials/lessons/04/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/04/acceptance.md)、[答案](../../materials/lessons/04/answers.md)。

只從自己的 `04-app` 工作副本開始，reference 保留在另一個目錄。02–08 使用獨立練習鍵 `mokaair-codex-practical-v1`，資料為 `id/title/completed`。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-04-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/04`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\04-app'
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

在原生桌面 App 加入這份本機資料夾 `C:\codex-practice\04-app`，新開屬於此專案的 Local 聊天。先請模型回報 cwd 和當集檔案，再貼本集完整任務。讀工具紀錄、開啟實際修改檔與 diff；自行執行驗收，在瀏覽器操作，而不是用模型的完成文字替代。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
只改 AGENTS.md 和 docs/data-contract.md。把目前 v1 的 id/title/completed、同名可用但 ID 唯一、篩選不改來源、儲存鍵、node --test 與瀏覽器 PASS/FAIL/NOT RUN 回報寫成可核對規則；先讀 core.mjs/app.mjs，不能憑空添加已實作功能。完成文件後新開對話，只讀驗收：列出實際讀取的規則、執行測試、解釋同名 ID 刪除與篩選真相，不改產品或測試。
```



## 主案例操作與驗收

1. 讀 AGENTS.md、docs/data-contract.md 與現有 core/app，把範圍、資料不變條件、檢查命令和未跑回報寫清楚；只修改這兩份文件。
2. 在同一副本的新對話送唯讀驗收要求；保留規則真正載入/讀取和測試的紀錄，不靠『我讀了』文字判定。
3. 比較 diff 只含 AGENTS.md/docs/data-contract.md；自己重跑 node --test，確認產品、既有測試和資料都沒有變更，未操作的瀏覽器條件保持 NOT RUN。
4. 在 challenge 副本讀 docs/rules-review.md，指出 title 當 ID 的規則與源程式/測試衝突，修文件規則並重新核對；不改產品去迎合錯誤規則。

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

- 只更新文件規則；產品、任務資料、localStorage 鍵與既有測試保持一致。
- 規則讀取、差異範圍、實際測試三種證據分開記錄。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`AGENTS.md`、`docs/data-contract.md`、`app.mjs`、`core.mjs`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 指示發現規則已由官方文件查核；當集的載入、遵循與對照結果未實跑。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

新對話沒有反映規則；查工作目錄及祖先目錄的指示、是否使用當集副本、是否已開新工作階段。檔案有要求但沒有執行，只能算遵循失敗，不能改口成強制關卡成功。

```text
請先停止新增變更。列出本次實際讀到的專案指示與來源路徑，再核對 diff、node --test 和未跑的瀏覽器檢查；有偏離範圍就只修偏離部分。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

讀 challenge 的 docs/rules-review.md 候選規則，指出以 title 當識別與穩定 ID/允許同名的衝突；只修 AGENTS.md/docs/data-contract.md，再用同名不同 ID 案例說明正確規則，不改產品。

完整材料與答案：answers.md 的第 04 集；答案含可操作的規則、一次小任務和成果核對，不用複製個人的全域設定。 亦見 [answers.md](../../materials/lessons/04/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [專案 AGENTS.md 發現與層級](https://learn.chatgpt.com/docs/agent-configuration/agents-md)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
