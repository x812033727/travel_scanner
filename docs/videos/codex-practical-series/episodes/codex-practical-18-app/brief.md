# codex-practical-18-app：綜合實作：先預覽、再歸檔，還能從備份恢復（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

任務變多以後想整理舊完成項，這次會將完成任務分成歸檔與保留資料。本集用完整開發流程做歸檔：需求、計畫、測試、預覽、執行、恢復與交付都要有人能核對。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：17。本片自己包含完整準備，不要求觀眾先看 `codex-practical-18-cli` 或使用它的成果。

1. 把歸檔需求拆成截止時間、保留規則、預覽/執行與備份恢復契約。
2. 按明確cutoff只歸檔已知時間且不晚於界限的完成任務，保留待辦與未知時間。
3. 跑完整驗收並實際恢復，對照原始資料證明可回退。
4. 交出新對話能複驗的完成包，分別記錄作者參考、模型成果與入口證據。

片長目標 18–25 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 18 集](../../lessons/18.md)。當集材料：[README](../../materials/lessons/18/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/18/acceptance.md)、[答案](../../materials/lessons/18/answers.md)。

只從自己的 `18-app` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

只改 `core.mjs`、`archive.mjs`、`restore.mjs`、`.github/workflows/practice.yml`，可新增 `tests/archive-boundary.test.mjs`；不改既有測試、fixture 或來源檔案。`core.mjs` 的 `archiveTasks` 是待實作 TODO；歸檔／恢復 CLI 接線與 CI 例子是作者已提供的支架，模型成果只依本入口實際 diff 與驗收判定。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-18-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/18`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\18-app'
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

在原生 App 先開 Plan 規劃歸檔，確認後切回可實作模式。檢查窄 diff、測試紅綠與預覽；讀者核對 preview 才執行含 --apply 的本機命令。原生畫面要顯示 preview/apply/恢復三段真實狀態，最後把交接記錄存檔，不能用『完成』聊天文字替代恢復證據。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
從本課 start 自行實作 core.mjs 的 archiveTasks TODO；archive.mjs、restore.mjs 的 CLI 輸入輸出接線與 .github/workflows/practice.yml 是作者已提供的支架，不把它們當成模型新生成的成果。只改 core.mjs、archive.mjs、restore.mjs、.github/workflows/practice.yml，可新增 tests/archive-boundary.test.mjs；不改既有測試、fixture，來源不覆寫。先讀 README/acceptance、確認工作路徑，執行 node --test 並保留 archive-not-implemented 基準。
實現本地歸檔契約：node archive.mjs fixtures/tasks.json --cutoff 2026-10-04T15:59:59.999Z --out archive-run。預設只預覽，加 --apply 才執行；只歸檔 completed=true 且 completedAt 已知、有效且 <=cutoff 的任務。未知時間與待辦全部保留，按 ID 保持輸入順序。apply 前把來源原始位元組備份到 archive-run/backup.json，輸出可核對的歸檔/保留檔案；用 node restore.mjs archive-run/backup.json restored.json 恢復到新檔；不覆蓋已有 run 目錄。固定 fixture 預期歸檔 1、保留 4。先在新增的 tests/archive-boundary.test.mjs 測未提供的時間邊界，再實作並跑完整驗收，以 SHA-256 核對備份、恢復與執行前來源。列出實際命令、exit code、diff 和未驗證；CI 沒有真實 run 就寫 NOT RUN，本機測試通過不能寫成 CI PASS。
```



## 主案例操作與驗收

1. 從當集獨立start讀需求並進入Plan，先確認cutoff是UTC時刻、<=包含界限、未知/待辦保留，不把『舊的』當日期。
2. start 的 TODO/throw 在 `core.mjs` 的 `archiveTasks`，challenge 才是未知時間誤歸檔缺陷。先執行 `node --test` 保留 `archive-not-implemented`；在待新增的 `tests/archive-boundary.test.mjs` 用自建測試資料斷言精確 cutoff、晚 1 毫秒、未知時間與待辦，先紅再實作 `archiveTasks`。必要時只在允許範圍調整 CLI／CI 支架；既有測試、fixture 與原始來源保持不變。
3. 執行不含--apply的命令，核對歸檔1保留4與來源位元組不變；讀者核對後以新輸出目錄執行--apply。
4. 檢查 archive-run/backup.json 與產物；執行 node restore.mjs archive-run/backup.json restored.json，恢復到另一份檔案。以 SHA-256 比對 restored.json、備份與執行前來源，確認原始位元組一致；重跑 node --test、週報與交接核對。
5. 讀 `.github/workflows/practice.yml`，核對 Node 測試、週報、歸檔與恢復命令符合本課契約。這是可放入自己練習 repo 的 CI 例子；實際推送與 GitHub run 未執行就記 `NOT RUN`，只有保存該次 run、commit 與結果才可記 CI 通過。

讀者親自重跑，而不是只讀模型回報：

```powershell
node --test
$LASTEXITCODE
Get-FileHash -LiteralPath fixtures/tasks.json -Algorithm SHA256
node archive.mjs fixtures/tasks.json --cutoff 2026-10-04T15:59:59.999Z --out archive-preview
Get-FileHash -LiteralPath fixtures/tasks.json -Algorithm SHA256
node archive.mjs fixtures/tasks.json --cutoff 2026-10-04T15:59:59.999Z --out archive-run --apply
node restore.mjs archive-run/backup.json restored.json
Get-FileHash -LiteralPath archive-run/backup.json,restored.json -Algorithm SHA256
node report.mjs restored.json --from 2026-10-05 --to 2026-10-11
```

網站確認：

```powershell
py -m http.server 4173 --bind 127.0.0.1
```

另開瀏覽器至 `http://127.0.0.1:4173/`。這是本機練習，先開乾淨的瀏覽器 profile／該來源的練習資料；不要清除其他網站的資料。服務所在目錄必須是這個入口的工作副本。用 Ctrl+C 停服務後，才換另一份副本佔用相同 port。

- cutoff=2026-10-04T15:59:59.999Z，已知完成時間<=cutoff歸檔；時間未知與待辦不動。
- 預覽來源不變；apply歸檔1保留4；備份恢復到 restored.json 後回到原五筆與原週報 5/2/1/1，且 SHA-256 與執行前來源相同。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt；只改 `core.mjs`、`archive.mjs`、`restore.mjs`、`.github/workflows/practice.yml`，可新增 `tests/archive-boundary.test.mjs`；既有測試與 fixture 只讀 | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | archive作者reference預期歸檔1/保留4；模型實作、紅綠、preview/apply與恢復都待本入口實際執行。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

預覽寫了資料、已有輸出被覆蓋、未知時間被歸檔或恢復不等原始；這是未通過的交付，先停止進一步apply，保留輸入/輸出/備份。按斷言定位，不靠刪除證據重跑。

```text
歸檔驗收失敗，請只分析這份輸入、cutoff、預覽/apply產物與備份。指出違反哪項契約；先給可驗證的恢復方法，確認來源恢復後只修 core.mjs、archive.mjs、restore.mjs、.github/workflows/practice.yml 與新增的 tests/archive-boundary.test.mjs，再使用新的輸出目錄重跑。不改既有測試或 fixture，不覆寫來源或舊結果；未跑檢查寫 NOT RUN。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

在新增的邊界測試中自建一筆 completedAt 恰等於 cutoff、一筆晚 1 毫秒、一筆 completed=true/null，不改原 fixture；預測前者歸檔、後兩者保留，再以測試產生的暫存輸入執行預覽、用新目錄 apply 並完整恢復。另驗壞備份不得產生恢復結果、既有輸出目錄不得覆蓋。

完整材料與答案：answers.md 的第 18 集；邊界<=、預覽不寫、未知/待辦保留、備份位元組/語義恢復與已存在輸出拒絕均需對照。 亦見 [answers.md](../../materials/lessons/18/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [互動式 /plan 與開發指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)；2026-10-11 實際開啟官方頁。
- [審查與開發指令](https://learn.chatgpt.com/docs/developer-commands?surface=cli)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
