# codex-practical-10-app：用畫面條件改 UI：手機寬度與鍵盤操作都能驗收（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

桌機看起來正常，style.css 的 min-width:900px 卻把手機撐寬。本集只改這個真實可測的版面問題，讓視覺改善也有驗收。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：09。本片自己包含完整準備，不要求觀眾先看 `codex-practical-10-cli` 或使用它的成果。

1. 把『手機能用』拆成窄屏不溢位、長標題換行與控制項可觸及三項條件。
2. 用390px寬度與Tab/Enter完成一次任務操作，不只看桌機截圖。
3. 修CSS的固定最小寬度，保留資料邏輯與週報結果。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 10 集](../../lessons/10.md)。當集材料：[README](../../materials/lessons/10/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/10/acceptance.md)、[答案](../../materials/lessons/10/answers.md)。

只從自己的 `10-app` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-10-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/10`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\10-app'
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

在原生桌面 App 加入這份本機資料夾 `C:\codex-practice\10-app`，新開屬於此專案的 Local 聊天。先請模型回報 cwd 和當集檔案，再貼本集完整任務。讀工具紀錄、開啟實際修改檔與 diff；自行執行驗收，在瀏覽器操作，而不是用模型的完成文字替代。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
只改善UI，不更改core.mjs、儲存鍵、報表或資料格式。移除造成390px橫向頁面滾動的min-width:900px，讓長中文標題換行、輸入與按鈕適應窄屏。保留label、鍵盤操作及可見焦點。用390px與1280px檢查；不能截圖時明確寫未驗證，先給我完整操作清單。
```



## 主案例操作與驗收

1. 在瀏覽器開發工具設390px，記錄整頁橫向滾動與fixed min-width，不靠截圖縮小掩蓋。
2. 讓Codex把視覺要求落實到CSS；逐項看diff是否只影響UI，測試資料邏輯與週報不變。
3. 輸入長中文標題，用Tab移動到新增/完成/刪除，用Enter或Space操作，觀察焦點能否看見。
4. 回1280px核對layout，再重新整理確認持久化；同樣命令核對週報四個固定數字。

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

- 390px不出現整頁橫向滾動，長標題可讀，按鈕不被裁切。
- Tab焦點可見；輸入標記與按鈕名稱清楚；鍵盤能新增、完成與刪除。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`index.html`、`style.css`、`app.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 390px、1280px、Tab焦點與持久化畫面待真實瀏覽器驗收；CSS reference為作者示範。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

只縮小字型使全部擠進去，或移除outline讓截圖變整潔；回到觸達和可讀條件。若只改螢幕截圖沒有程式碼diff，不能寫成UI實現。

```text
請保留字型可讀與鍵盤焦點；只修造成390px整頁溢位的寬度與換行，逐項說明我應檢查哪個CSS和哪個操作，不使用隱藏overflow遮蔽控制項。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

加入100字以內的長中文標題，在360px與390px各核對；同時用鍵盤完成並刪除篩選內的任務。

完整材料與答案：answers.md 的第 10 集；答案含可重做的窄屏與鍵盤檢查，不以靜態截圖推斷資料或焦點行為。 亦見 [answers.md](../../materials/lessons/10/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
