# codex-practical-07-app：Codex 說做完了：審查差異，找出測試沒看到的問題（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

核心邏輯全綠，候選版卻把使用者標題塞進 innerHTML。這集教你閱讀真正 diff 與畫面行為，避免只接收『看起來不錯』的回覆。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：06。本片自己包含完整準備，不要求觀眾先看 `codex-practical-07-cli` 或使用它的成果。

1. 在先不改檔的審查中，給每項發現觸發條件、位置、影響與驗證方式。
2. 用任務標題包含 HTML 的固定資料證明 innerHTML 插入的錯誤呈現。
3. 把審查意見轉成窄修復，再以原案例與完整測試驗收。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 07 集](../../lessons/07.md)。當集材料：[README](../../materials/lessons/07/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/07/acceptance.md)、[答案](../../materials/lessons/07/answers.md)。

只從自己的 `07-app` 工作副本開始，reference 保留在另一個目錄。02–08 使用獨立練習鍵 `mokaair-codex-practical-v1`，資料為 `id/title/completed`。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-07-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/07`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\07-app'
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

開啟 App 的 diff／review 面板，先讀候選版。若目前沒有 Git 變更，直接用只讀 prompt 審當集 app.mjs，不說成審查不存在的 PR；有變更時用原生 /review 選未提交範圍。點回發現位置與原始程式，再實際輸入 <b>Read</b> 核對；確認後才送窄修復。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
先只審查不改檔。讀本集候選 app.mjs 與 core.mjs，重點是 task.title 顯示方式；固定輸入為 <b>Read</b>。每項可重現問題附檔案/函式、觸發條件、影響、修法與核對方式。不要把測試通過當成無問題，沒有可證實發現就明說。等我核對後再修。
```



## 主案例操作與驗收

1. 先跑 node --test；本教材 start/challenge 的 Node 測試預期綠，沒有瀏覽器文字呈現證據。準備標題 <b>Read</b>，以真正 diff 與網站畫面找出不安全 innerHTML，不能按關鍵字檢查假裝已審完。
2. 啟動本入口的只讀審查，先讀發現與原始位置，不立即接受模型修改。
3. 預覽網站，核對應顯示字面 <b>Read</b>，而不是變成粗體元素；這是簡單可重做的對照。
4. 採用確認的發現，另送窄修復要求，改用安全的文字呈現；重跑測試與同一畫面輸入。

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

- HTML 字串以文字顯示，不生成 b 元素；普通中文標題仍正常。
- 審查結論至少能對到一個實際位置、固定輸入及驗收，不用問題數量作成績。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`app.mjs`、`core.mjs`、`core.test.mjs`、`docs/data-contract.md` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 審查是否找到問題、修復差異與HTML字串畫面都未實跑；作者故障不算模型審查成果。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

模型只提供泛泛風險或直接改全站；要求回到固定候選檔和輸入。若 review 命令沒有 diff，先閱讀當集檔案版作只讀審查，不能宣稱審過不存在的變更。

```text
只修已確認的 task.title 呈現：用文位元組點取代 innerHTML，保留現有事件與資料。新增能驗證需求的檢查，並列出測試和瀏覽器結果；未跑瀏覽器就寫未驗證。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

把標題改成 <img src=x> 與『中文 & 符號』，說明為何資料存得下與畫面安全呈現是兩項驗收。

完整材料與答案：answers.md 的第 07 集；答案指向文位元組點或 textContent，另外保留資料/DOM兩個層級的檢查。 亦見 [answers.md](../../materials/lessons/07/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [審查與開發指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
