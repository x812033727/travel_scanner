# codex-practical-15-app：兩個工作同時做：用 worktree 隔離，再整合驗收（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

同時改介面提示與週報輸出時，需要把兩個工作區分開，再將有證據的提交收回。本集完成一項看得見的 UI 變更、一項可執行的 CLI 變更，觀察隔離、整合與還原。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：08、14。本片自己包含完整準備，不要求觀眾先看 `codex-practical-15-cli` 或使用它的成果。

1. 從同一Git基線建立兩個獨立工作目錄，確認路徑與分支。
2. 讓介面提示與週報 --compact 分別提交，核對每個提交只含自己的範圍，再逐一整合。
3. 整合後跑完整測試與瀏覽器核對，識別並修復衝突。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 15 集](../../lessons/15.md)。當集材料：[README](../../materials/lessons/15/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/15/acceptance.md)、[答案](../../materials/lessons/15/answers.md)。

只從自己的 `15-app` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-15-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/15`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\15-app'
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

先在當集新工作副本建立基線；以下只操作這份練習 repo：

```powershell
git init -b main
git config --local user.name "Codex Practice"
git config --local user.email "practice@example.invalid"
git add -A
git commit -m "Practice baseline"
Add-Content -LiteralPath style.css -Value '/* KEEP-MY-NOTE */'
git status --short
git diff -- style.css
```

建立兩個 worktree 後，A/B 都先確認 `Select-String -LiteralPath style.css -Pattern 'KEEP-MY-NOTE'` 沒有結果。A 提交使用 `git add -- index.html`，B 使用 `git add -- report.mjs tests/report-compact.test.mjs`，再分別 `git commit -m "Explain filter intersection"`／`git commit -m "Add compact report format"`。記錄 `git rev-parse HEAD` 與 `git show --stat HEAD` 的真實輸出。回原工作區先記下兩個 SHA，在 PowerShell 以 `$uiCommit = Read-Host '貼上 A 的完整 SHA'`、`$reportCommit = Read-Host '貼上 B 的完整 SHA'` 設定，再依序 `git cherry-pick $uiCommit`、`git cherry-pick $reportCommit`；不貼假的示例 SHA。最後重看 `git status --short` 和 `git diff -- style.css`。 記錄 cherry-pick 後真正的整合 SHA；還原演練以 `$reportIntegration = Read-Host '貼上 report 整合 SHA'`、`$uiIntegration = Read-Host '貼上 UI 整合 SHA'` 設定，執行 `git revert --no-edit $reportIntegration $uiIntegration`。逆向提交保留歷史，不刪未提交 CSS；完成後重新跑基線測試與預設週報，--compact 應回到基線未提供的狀態。


先把當集副本建立成 Git repo 與 baseline。原生新聊天選 Worktree、同一基線分支，分別給 A/B 的完整任務；實際目錄由 App 回傳，逐個記錄，不寫假的固定 managed 路徑。用 Create branch here 給各工作區不同分支，核對 diff 與測試，再在整合工作區收回提交。需要轉移聊天時才用 Hand off，先核對目的地與狀態。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
按 docs/worktree-lab.md 分工。A 只改 index.html，在篩選附近新增 p#filter-hint 可見提示「搜尋會與目前狀態篩選一起套用。」；不得改報表、core、CSS 或 fixture。B 只改 report.mjs，新增 --compact：stdout 與 --out 都輸出單行 JSON 加一個尾端 LF，預設仍為兩空格縮排 JSON；新增 tests/report-compact.test.mjs，用 subprocess 比較兩格式、固定 5/2/1/1 真值與來源不變。不得改 index、core、CSS 或 fixture。各自先回報工作區絕對路徑、分支、基線 commit，提交只含自己的範圍。主工作區逐一 cherry-pick 後核對 UI 和兩種報表，原有 KEEP-MY-NOTE 不提交。
```



## 主案例操作與驗收

1. 在獨立練習 repo 建立 baseline commit，再在原工作區 style.css 加入未提交的 KEEP-MY-NOTE 註解。以同一 HEAD 準備 A/B 工作區；各自核對 cwd、分支、HEAD，確認兩份新工作區都沒有該註解。
2. A 只改 index.html，實際瀏覽器核對新提示。B 只改 report.mjs 和新增 tests/report-compact.test.mjs，比較預設 pretty 與 --compact 單行輸出；JSON 值皆是 5/2/1/1，stdout/--out 格式與來源不變均要測。各自只暫存獲派檔案，提交後檢查 git show --stat HEAD。
3. 回到原工作區，確認 KEEP-MY-NOTE 仍未提交；用真實 commit SHA 逐一 cherry-pick A/B。git diff -- style.css 應保留註解，兩個提交分別只改 index.html，以及 report.mjs/tests/report-compact.test.mjs。
4. 整合目錄執行 node --test、預設與 --compact 週報，瀏覽器核對新提示和搜尋/狀態交集；檢查 worktree 清單、整合提交與未提交註解。保存兩個整合後 SHA，另做 git revert 逆向提交，再驗證 UI 提示與 compact 變更已回退、基線行為及 KEEP-MY-NOTE 保留。

讀者親自重跑，而不是只讀模型回報：

```powershell
node --test
$LASTEXITCODE
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11 --compact
node report.mjs fixtures/tasks.json --from 2026-10-05 --to 2026-10-11 --compact --out compact.json
```

網站確認：

```powershell
py -m http.server 4173 --bind 127.0.0.1
```

另開瀏覽器至 `http://127.0.0.1:4173/`。這是本機練習，先開乾淨的瀏覽器 profile／該來源的練習資料；不要清除其他網站的資料。服務所在目錄必須是這個入口的工作副本。用 Ctrl+C 停服務後，才換另一份副本佔用相同 port。

- A/B 實體目錄與分支不同；A 只提交 index.html，B 只提交 report.mjs 與 tests/report-compact.test.mjs。未提交 KEEP-MY-NOTE 沒有進入兩個新工作區。
- 整合後 UI 提示可見，預設/compact JSON 值一致 5/2/1/1；compact 單行且有一個尾端 LF。逆向提交可還原兩項行為，KEEP-MY-NOTE 全程未提交。分支完成、整合完成與還原分開記錄。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`docs/worktree-lab.md`、`index.html`、`report.mjs`、`tests/report-compact.test.mjs`（B 待新增）、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | worktree建立、並行改動、提交與整合都待原生執行；作者工作區說明不是隔離成功證明。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

嘗試讓同一分支同時checkout兩處或兩個任務仍寫同一路徑；先用git worktree list與cwd糾正。衝突解決後只跑一邊測試不算整合通過。

```text
請先停止新的修改。列出兩個worktree的絕對路徑/分支/HEAD與本次提交diff，找出範圍重疊。按docs/worktree-lab.md的契約解決衝突，最後在整合目錄跑完整測試，不刪除未確認工作區。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

完成主流程後從相同已整合基線另開兩個 worktree，讓 A/B 都改 index.html 那句提示而產生文案衝突；保留必要資訊，解釋最終文字和解衝突步驟，重跑 UI/報表驗收，KEEP-MY-NOTE 仍未提交。

完整材料與答案：answers.md 的第 15 集；核對 UI/report 範圍、真實 SHA、cherry-pick/revert、KEEP-MY-NOTE 隔離、文案衝突與完整驗收。 亦見 [answers.md](../../materials/lessons/15/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [原生 App Git worktree](https://learn.chatgpt.com/docs/environments/git-worktrees)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
