# codex-practical-13-cli：把驗收流程做成 Skill：能被找到，也真的做完檢查（CLI）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；CLI 模型操作與結果 pending_run；真實執行後另記收據。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

每次交付都重貼三段檢查。這裡用一份小Skill儲存驗收流程，教你先看它有沒有被使用，再看檢查有沒有完成。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：12。本片自己包含完整準備，不要求觀眾先看 `codex-practical-13-app` 或使用它的成果。

1. 將重複的測試、週報真相與UI清單寫成專案範圍的verify-delivery技能。
2. 分別確認檔案有效、被發現、被選擇與檢查完成四種狀態。
3. 用一個失敗案例驗證技能會保留問題與待驗證項，不把提醒寫成強制關卡。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在終端機與 Codex CLI TUI／非互動命令；網站行為另外用真正瀏覽器確認。不能用 App 的畫面或聊天替代 CLI 的工具與退出狀態。

完整共通教案：[第 13 集](../../lessons/13.md)。當集材料：[README](../../materials/lessons/13/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/13/acceptance.md)、[答案](../../materials/lessons/13/answers.md)。

只從自己的 `13-cli` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-13-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/13`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\13-cli'
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

在互動 TUI 用 /skills 檢視，輸入 $verify-delivery 明確叫技能；若用 / 互動選單，核對選中的真實名稱。執行紀錄要包含 node --test 與固定報告，單一『已使用』答覆不算驗收。

互動 TUI 啟動前執行 `codex --version` 和 `codex --help`，保留本機版本。斜線指令如 `/plan`、`/agent` 屬於 TUI；`codex exec` 不具相同互動控制。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
請使用本專案的 $verify-delivery，驗證當前任務與週報工具。遵照技能中的node --test、固定報告真相與瀏覽器檢查；逐項記錄實際、失敗與未驗證。如果無法操作瀏覽器，不寫UI通過。只驗收與回報，不修改程式、資料或使用者全域設定。
```



## 主案例操作與驗收

1. 先讀SKILL.md frontmatter的name/description與步驟，核對它只用於當前專案交付，並指向真實命令與fixture。
2. 在本入口重新整理發現技能（若未出現則重啟），顯式選verify-delivery並送完整要求；保留髮現與選擇紀錄。
3. 核對實際工具執行與結果表，不能只憑『已呼叫技能』確認完成；UI看不到就留待驗證。
4. 在全新challenge副本再驗證一項錯誤；觀察技能是否記失敗，而不是改測試或替你靜默修好。

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

- 技能包含name/description，清楚說明何時用；專案目錄是.agents/skills/verify-delivery。
- 結果分別列測試、報告數值、UI；未知、失敗與未驗證不會合併成通過。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`.agents/skills/verify-delivery/SKILL.md`、`core.test.mjs`、`fixtures/tasks.json`、`report.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 技能檔案由作者提供；在App或CLI出現、被選擇、完成驗收與失敗案例均待該入口實跑。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

技能看不到；核對目錄層級、frontmatter和當前repo範圍，按官方文件重啟再看。看得到但沒執行檢查，屬於使用或遵循失敗，不是安裝問題。

```text
verify-delivery已被選擇，但結果沒有實際測試/報告命令。請只執行技能中已有的可用檢查，逐項給實際輸出；無法驗證的UI保留未驗證，不改產品程式碼。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

把某一項固定報告預期寫錯，執行技能並要求以fixtures真相定位差異，再修技能說明而不是改fixture。

完整材料與答案：answers.md 的第 13 集；核對發現/選擇/執行分開，以及錯誤預期需回到源資料的處理。 亦見 [answers.md](../../materials/lessons/13/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [技能目錄、發現與使用](https://learn.chatgpt.com/docs/build-skills)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
