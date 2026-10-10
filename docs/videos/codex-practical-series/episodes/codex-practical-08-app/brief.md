# codex-practical-08-app：把改動留下、也能還原：從差異到本機提交（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

模型改完十個檔案，你只打算交出兩個。本集用沒有遠端的練習 repo 教你看清楚差異、選定檔案與安全還原。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：07。本片自己包含完整準備，不要求觀眾先看 `codex-practical-08-cli` 或使用它的成果。

1. 在獨立練習 repo 讀懂工作區、暫存區與提交差異，只提交本次任務。
2. 用檔案還原修正一個未提交的錯字，保留其他合理修改。
3. 交出有觸發、結果與驗收紀錄的 PR 草稿，而不把本機 commit 當成已發布。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 08 集](../../lessons/08.md)。當集材料：[README](../../materials/lessons/08/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/08/acceptance.md)、[答案](../../materials/lessons/08/answers.md)。

只從自己的 `08-app` 工作副本開始，reference 保留在另一個目錄。02–08 使用獨立練習鍵 `mokaair-codex-practical-v1`，資料為 `id/title/completed`。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-08-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/08`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\08-app'
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

原生 diff 中逐檔檢視，再暫存選定檔案；暫存差異仍須核對。若版本沒有對應暫存控制項，使用 App 內建終端機的 git add／git diff --cached，但保留 App 主聊天、差異與回覆證據。單檔還原之前先讀該檔差異；只提交本機練習，不按遠端推送或合併。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
這是沒有遠端的練習 repo。先檢查 git status --short 與 git diff；只把本次已確認的小變更和它的測試整理成提交建議，不執行 push、merge 或部署。產出 docs/pull-request.md，包含問題、改後行為、實際驗證和未完成項目。指出不該混入的修改，提交由我核對後在本機做。
```

```powershell
git init
git config user.name "Codex Practice"
git config user.email "practice@example.invalid"
git add -A
git commit -m "Baseline practice"
git status --short
git diff
git diff --cached
```

## 主案例操作與驗收

1. 在全新副本讀 docs/git-lab.md，先執行 node git-lab.mjs 看暫存練習庫的真實狀態。手動重做時建立只屬於本包的 baseline repo，在 index.html 改頁面標題，style.css 另留 KEEP-MY-NOTE 練習註記。
2. 讀 git status --short、git diff，逐個檔案判斷是否屬於本次工作。
3. git add -- index.html，只暫存標題；核對 git diff --cached 只有 index，git diff -- style.css 仍有註記。寫 docs/pull-request.md 的觸發、結果與真實驗收，尚未完成檢查標未驗證。
4. 只提交 index.html，讀 git show --stat HEAD；以 git revert --no-edit HEAD 還原已提交標題、保留逆向歷史和 CSS 註記。最後先保存這份練習註記，查看其 diff，再以 git restore -- style.css 還原指定未提交檔案；PR 筆記與其他路徑保留。

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

- 暫存差異只含選定檔案，未選修改仍在工作區；還原只影響核對過的檔。
- PR 草稿寫實際測試，不宣稱 push、合併、部署、影片發布。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`README.md`、`docs/pull-request.md`、`app.mjs`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | Git 指令的本機狀態待讀者實跑；沒有計畫進行遠端提交、PR 建立或部署。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

git commit 提示缺少身分；只在練習repo設local user.name/user.email，不改全域。若已暫存錯檔，先 git restore --staged -- 檔名，再重新選，不能刪除整個專案。

```text
我只要還原 README.md 的這個未提交錯字。先列出該檔差異和其他未提交檔；確認不會影響其他檔後，給單檔還原命令與核對命令。不要 reset --hard。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

保留 core.test.mjs 的新增測試、排除 docs 的未完成筆記，核對 staged diff 後寫一則一句話提交摘要。

完整材料與答案：answers.md 的第 08 集；答案含工作區/暫存區分開核對、單檔restore與localcommit，不包括遠端發布。 亦見 [answers.md](../../materials/lessons/08/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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
