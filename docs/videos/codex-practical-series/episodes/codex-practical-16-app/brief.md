# codex-practical-16-app：把獨立檢查交給代理：回報要核對，主對話要負責（原生 App）

企劃／查核基準日：2026-10-11（Asia/Taipei）。狀態：brief 已撰寫；原生 App 操作 pending_capture，模型成果 pending_run。 製作路線：教學卡片＋真實步驟紀錄，`format: slides`，`category: tutorial`；不是已完成的 video.json 或影片。

## 觀眾問題與學習成果

另一個模型說沒問題，也不等於你可以交。這裡讓兩位代理獨立讀不同方面，再由主對話負責確認，而不是增加兩份肯定的文字。

觀眾需能開資料夾、輸入命令及核對檔案，不預設會寫程式。概念先備：15。本片自己包含完整準備，不要求觀眾先看 `codex-practical-16-cli` 或使用它的成果。

1. 把資料/測試和鍵盤/UI審查拆成兩個不重疊的只讀子任務。
2. 檢視真實代理活動與回報，區分已啟動、已完成和已採納。
3. 用主對話複驗代理發現，合併成帶來源與待驗證項的交付結論。

片長目標 12–18 分鐘，正文至少 8 分鐘。核心操作、原因、失敗與變式支撐長度，不加重複提醒或空白湊時。

## 示範或實算：範圍與起點

製作路線：教學卡片。主操作發生在原生桌面 App：選專案、送任務、模式／技能／代理／差異或排程。終端機只是執行本機測試；不能用 CLI 的已完成狀態替代 App 演示。

完整共通教案：[第 16 集](../../lessons/16.md)。當集材料：[README](../../materials/lessons/16/README.md)、`start/`（本課 ZIP 根目錄）、`reference/`（本課 ZIP 根目錄）、`challenge/`（本課 ZIP 根目錄）、[驗收](../../materials/lessons/16/acceptance.md)、[答案](../../materials/lessons/16/answers.md)。

只從自己的 `16-app` 工作副本開始，reference 保留在另一個目錄。09–18 使用 `mokaair-codex-practical-v2`。v2 不存在才讀經驗證的 v1 轉移，保留原 v1 鍵；`completedAt` 為 canonical UTC 字串或 null，未知時間不能補今天。 另一入口可共用材料版本與真相，不共用聊天、實作目錄、模型結果或核准。作者 reference 不宣稱由本入口的 Codex 生成。

Node.js 22 以上相容版本、Python 3、Git；沒有 npm dependencies。先將 `codex-practical-16-materials.zip` 解壓到新的資料夾；把 `$lessonRoot` 換成直接包含 `README.md`、`start`、`reference`、`challenge` 的本課解壓根目錄。下方從根目錄的 `start` 複製新工作副本，保留原始教材。每課 ZIP 已是完整一課，不需再接 `lessons/16`。

```powershell
$lessonRoot = '<本課 ZIP 解壓目錄>'
$lessonSource = Join-Path -Path $lessonRoot -ChildPath 'start'
if (-not (Test-Path -LiteralPath $lessonSource -PathType Container) -or -not (Test-Path -LiteralPath (Join-Path -Path $lessonRoot -ChildPath 'README.md') -PathType Leaf)) { throw '把 lessonRoot 換成本課 ZIP 解壓後直接含 README.md 和 start 的根目錄。' }
$lessonWork = 'C:\codex-practice\16-app'
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

在主聊天貼恰好兩位代理的分工要求，展開真正的代理活動／對話，保留 A/B 的開始、來源範圍、完成與回報。主聊天最後自行驗證；代理活動尚未錄到時不能畫成兩位已完成。

在 App 的真實專案聊天送下段文字，不送到終端機。
本段是**待執行提示**，模型與瀏覽器結果均未驗證；對話中需核對自己的實際 cwd，不能貼佔位路徑後讓模型猜：

```text
請使用恰好兩位只讀子代理：A 審 core.mjs、core.test.mjs、fixtures/tasks.json 與週報資料邊界，核對 5/2/1/1 並指出舊說明 completedInWeek=3 的錯誤；B 審 index.html、app.mjs、style.css 與 localStorage 的鍵盤及窄屏條件，實際操作才寫觀察，未操作寫 NOT RUN。兩位都不得改檔或呼叫付費外部工具，發現須附檔案/函式、觸發條件和核對方式。主對話收齊後自行復驗可跑專案，合併重複發現；沒有瀏覽器證據的UI寫未驗證。
```



## 主案例操作與驗收

1. 讀docs/subagent-lab.md，寫清任務A/B的輸入、範圍、輸出與完成條件，先說明為什麼兩項可獨立。
2. 明確要求恰好兩位代理，觀察本入口的真實活動，不把普通兩個回答段落當代理。
3. 分別核對代理回報的檔案位置、斷言與證據；主對話自己跑測試/報告，UI須實際操作或留待驗證。
4. 整理共同結論與下一步，附是否實際啟動/結束/複驗；一次沒發現不推論所有情境安全。

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

- 有真實代理活動與不同任務，兩個回報保持只讀範圍。
- 結論能回溯原始檔與主對話複驗，代理意見、作者真相、使用者UI確認分別標記。

| 示範 | 輸入與動作 | 預期 | 實際／證據 |
| --- | --- | --- | --- |
| 起點 | 當集 start 與上列基準命令 | 依當集 acceptance，刻意失敗需明列 | 待本入口執行 |
| 主操作 | 本片完整 prompt 與限定檔案：`docs/subagent-lab.md`、`core.mjs`、`core.test.mjs`、`app.mjs`、`style.css`、`core.test.mjs` | 完成本片成果並核對外部行為 | pending_run |
| 結果 | 同一輸入、驗收命令、瀏覽器操作 | 兩位代理的啟動、輸出、完成與主對話複驗皆未實跑；模板只是計畫輸入；reference 的分析是作者撰寫範例，沒有宣稱代理曾執行。 | 尚無原生結果 |
| 故障對照 | 下一節具體失敗案例與修復提示 | 能區分原因並重做 | 待實跑 |
| 變式 | 換一個需求並先寫預測 | 與答案及真相一致 | 待獨立重做 |

要在卡片呈現 terminal／原生畫面，必須照真實紀錄節錄，標日期、版本與來源；未執行只寫「預期」，不畫假成功。官方頁 screencast 只能示範官方文件描述的操作，不能證明此入口實作。

## 常見失敗與修復

模型自行做完並沒啟動代理，或代理寫了同一檔案；如實記入口/策略結果，不偽造排程。發現不可重現先讓提供固定輸入，不因多人一致就採納。

```text
目前沒有可驗證的兩位代理活動。請按A/B獨立只讀任務實際委派（入口不可用則明說），完成後給每位的範圍與原始發現；主對話複驗再下結論，不補造代理對話。
```

修復前保留失敗輸入、檔案差異與輸出；修後用相同條件重做，不靠重建答案或放寬測試讓失敗消失。機器或模式不可用就回報那個真正缺口，先不進媒體階段。

## 變式練習與答案

故意給其中一位過期說明，讓它以源程式核對；主對話辨認未執行的畫面結論並要求進一步證據。

完整材料與答案：answers.md 的第 16 集；答案看委派範圍、真實活動、來源與複驗，不看代理人數或報告長度。 亦見 [answers.md](../../materials/lessons/16/answers.md) 和 `challenge/`（本課 ZIP 根目錄）。
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

- [子代理與 /agent](https://learn.chatgpt.com/docs/agent-configuration/subagents)；2026-10-11 實際開啟官方頁。
- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli)；2026-10-11 實際開啟官方頁。
- [原生 App 功能與入口](https://learn.chatgpt.com/docs/features)；2026-10-11 實際開啟官方頁。

這些官方頁已實際開啟；產品能力與入口依當日文件，固定真相與使用者資料規則由本教材定義。錄製當天再核對 UI／命令可用性及版本，App 與 CLI 可能不同。價格、額度、速度不作本片成果，沒有實測就不編數字。
