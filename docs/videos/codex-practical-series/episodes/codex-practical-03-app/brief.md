# codex-practical-03-app：新增搜尋與篩選：讓需求、程式和畫面對得上（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

有計畫之後不能只驗一個搜尋函式。本包已備好輸入框與事件接線，模型補核心函式後，仍要確認真正瀏覽器上的搜尋、空結果與資料保留。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：02。本片自己包含完整準備，不要求觀眾先看 `codex-practical-03-cli` 或使用它的成果。

1. 用固定任務驗證搜尋和完成狀態取交集，保留原始任務順序與資料。
2. 讓 Codex 依已定計畫只修改 core.mjs，讀既有測試與畫面接線，逐項核對差異。
3. 分別核對核心測試、瀏覽器搜尋、空結果與資料保留，說明各項證據能證明的範圍。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 03 集](../../lessons/03.md)。當集材料：[README](../../materials/lessons/03/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/03/acceptance.md)、[答案](../../materials/lessons/03/answers.md)。

只從自己的 `03-app` 工作副本開始，reference 保留在另一個目錄。02–08 使用獨立練習鍵 `mokaair-codex-practical-v1`，資料為 `id/title/completed`。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-03-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/03`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\03-app'
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

在原生桌面 App 加入這份本機資料夾 `C:\codex-practice\03-app`，新開屬於此專案的 Local 聊天。先請模型回報 cwd 和當集檔案，再貼本集完整任務。讀工具紀錄、開啟實際修改檔與 diff；自行執行驗收，在瀏覽器操作，而不是用模型的完成文字替代。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
依本課 README 的固定需求實作標題搜尋，搜尋文字 trim 後不分大小寫，與 All/Active/Completed 取交集；保持原資料與順序。主任務只改 core.mjs；讀既有 index.html、app.mjs、core.test.mjs 與 feature 測試，執行空搜尋、無結果與交集案例。挑戰纔在自己的副本新增 Unicode 斷言，主流程不得修改既有測試。不新增套件，不改 localStorage 鍵。自己跑 node --test，再列出供我操作的瀏覽器核對步驟。
```



## 主案例操作與驗收

1. 開始前執行 node --test，確認當集基線；固定資料為 Read、Build、Review，Review 標成完成。
2. 把計畫與完整任務交給 Codex，先看它把資料過濾放哪裡，再讀既有搜尋欄位與 render 接線；本包畫面控制項已就位，主流程只補資料函式。
3. 跑搜尋 re＋All／Active／Completed，預期分別為 Read+Review／Read／Review；改成 xyz 預期為空。
4. 清空關鍵字應回到目前篩選；重新整理確認儲存與既有新增／刪除未被破壞。

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

- 搜尋的結果與完成篩選取交集，空白與大小寫的處理相同。
- 無結果仍保留完整資料；清空搜尋可找回任務，不因搜尋而刪檔或刪資料。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`index.html`、`app.mjs`、`core.mjs`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 搜尋與交集的函式、測試、UI 結果皆為預期；作者 reference 只能作比較，不能證明模型完成。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

核心測試通過但輸入不改畫面；先查 index.html 的搜尋控制項、app.mjs 事件與 render 的引數。若搜尋後刪錯任務，保留案例，交給第 05 集的 ID 診斷。

```text
資料函式測試已通過，但我在瀏覽器輸入 re 沒有更新。只讀畫面輸入到 render 的接線；指出實際檔案與事件。先核對 HTTP 是否服務這份副本及瀏覽器快取，保留本課只改 core.mjs 的範圍；若確實是題外 UI 缺陷，列待修項與重現步驟，不自行重寫網站。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

改成搜尋「 報告 」並加入「寫報告、報告校對、買午餐」；一筆完成，核對三個篩選，不讓文字前後空白影響結果。

完整材料與答案：answers.md 的第 03 集；測試應比較回傳 id 與原資料不變，瀏覽器還需確認輸入事件。 亦見 [answers.md](../../materials/lessons/03/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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
