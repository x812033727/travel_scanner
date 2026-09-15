把 Gemini CLI 放進 GitHub Actions，可以保留固定環境、執行紀錄與可下載報告，但不應一開始就讓它自動修改所有文件。本篇從手動觸發、單份合成資料與固定版本開始，先跑不需要金鑰的測試模式，再說明如何接上受控的模型呼叫。

## 成品、先修與驗證範圍

先完成 [[39|權限與沙箱]] 及 [[78|可續跑批次程式]]。本篇提供獨立的工作流範例、兩份測試文件與執行器。將下載包放入新的測試 repository，先逐檔閱讀；不要直接把工作流複製進正式網站，因為工作流執行的是它所取出的程式。

2026-09-14 的驗證涵蓋 Windows、Python 3.13.15 的本機執行器、YAML 結構、參數限制及無憑證反例。Actions 版本與完整提交識別已由各官方 repository 查證，但尚未在 GitHub hosted runner 實際觸發，也沒有真實雲端模型用量；這兩項是發布前待驗工作。

## 第一階段：建立最小且可讀的 repository

將 79 資料夾內的 runner.py、pipeline.py、no-tools.toml 及 docs/ 放在測試 repository 根目錄，再把 review.yml 放到 .github/workflows/review.yml。先確認 repository 只有教材需要的資料，README 清楚註明內容為合成範例。工作流檔若不在指定目錄，GitHub 不會把它當成可執行工作流。

先在本機執行下面命令，預設會使用 fixture 模式處理 doc01.md。成功後打開 out/workflow.json 與 out/report/results，確認模式標記與文件 ID。這一步可以在沒有 API 金鑰時完成，也方便在未啟用 Actions 前發現路徑或程式錯誤。

```bash 終端機：從教材 repository 根目錄執行
python runner.py
```

本機第二次執行會遇到已存在的 selected 目錄，這是刻意保留的界線：工作流的每次 hosted run 通常使用新工作目錄，本機複驗則應複製到另一份教材目錄或先保存舊輸出。不要把不同執行的報告混在一起，再從檔名猜哪一份是最新結果。

## 第二階段：閱讀手動觸發與權限設定

範例只有 workflow_dispatch，沒有 push、排程或 pull request 觸發。輸入可選 fixture 或 live，文件只允許 doc01.md、doc02.md。選項在介面上受限，Python 執行器還會再驗證一次，因此不能只因網頁提供下拉選單，就假設任何事件資料都可信任。

!include-code examples/79/review.yml

工作流只申請 contents: read，並停用 checkout 的憑證保留。它僅允許預設分支的手動事件，checkout 使用該事件的提交識別，避免開始執行時才重新取可能已移動的分支。報告要保留相應 commit 與 run 網址，否則日後不容易確認驗證的是哪份程式。

Actions 的 uses 欄位固定完整提交識別，旁邊註明查證時的版本。更新時先核對官方來源與變更，再在新分支跑一次 fixture。固定識別提供可重現的版本選擇，不是永久安全保證；讀者仍須依自己的 GitHub 組織政策與 runner 支援狀況維護。

## 第三階段：建立 Environment 並跑 fixture

在 repository 的 Settings 建立名為 gemini-tutorial 的 Environment，查看帳號方案提供哪些審核與分支限制。若可以設定必要審核人員，依團隊流程啟用；如果方案不提供某項控制，應記錄實際條件，不要因為 YAML 寫了 environment 名稱，就宣稱已經存在人工核准關卡。

進入 Actions，選擇 Gemini tutorial report，再選 Run workflow。先保留 fixture 與 doc01.md。確認使用預設分支，查看每個步驟的執行狀態；完成後下載 artifact，比對 mode、document、batch 的處理數量與結果檔內容。單看綠色勾號還不能證明下載包裡有正確報告。

| 位置 | 要核對的內容 | 不能直接推論 |
| --- | --- | --- |
| Actions 執行頁 | run、commit、步驟結果 | 不等於模型品質已測 |
| workflow.json | 模式、文件、整體狀態 | 不等於正式文件已更新 |
| run-summary.json | 處理、跳過及失敗 | 不等於零成本 |
| results | 文件 ID 與模式標記 | fixture 不是模型回答 |

artifact 只包含工作流摘要、批次摘要與結果 JSON，沒有整包上傳 runtime 家目錄或原始環境。保留期限設定為三天，適合短期教學驗收；需要長期保留時，另行保存審閱過的證據。檔名包含執行識別與嘗試次數，避免重跑後把不同產物看成同一份。

## 第四階段：有條件地加入模型呼叫

fixture 通過後，再決定是否配置 API 金鑰。將 GEMINI_API_KEY 放進指定 Environment 的秘密設定，不能寫進 repository、工作流正文或模型輸出。金鑰只傳給 live 那個步驟，安裝依賴與 fixture 步驟都不需要它；也不要在除錯時印出完整環境。

執行 live 時輸入帳號可用的模型名稱，先處理一份文件。程式使用前篇的外層 CLI 與內層內容契約驗證，失敗就留下狀態，不會替你自動留言、提交、合併或部署。使用 API 金鑰會走相應計費管道，需到 [[49|API 用量與費用教學]] 核對，不以 Gemini 訂閱費推論已包含呼叫。

工作流的五分鐘上限與單份輸入能縮小一次執行的範圍，但不是帳號的金額硬上限。重複手動觸發、SDK 內部重試或其他程式仍可能使用同一把金鑰。第一次成功後先查用量，再決定是否增加資料，不要直接把 fixture 的二十份測試規模搬到付費環境。

## 故障練習與處理方式

第一個反例是不提供金鑰卻選 live。本機執行器已驗證會以失敗狀態結束，原因明確指出缺少模型或金鑰，不會把空檔案當成完成。第二個反例是傳入 ../private.txt，即使字串來自工作流輸入，也會被文件允許名單拒絕。

第三個反例是模型回答格式錯誤。批次程式即使看到 CLI 退出成功，仍會檢查 response 與文件契約；不符合就保留失敗。上傳 artifact 的步驟使用 always，讓失敗時仍有機會取得摘要，但 artifact 存在不代表工作流成功，判讀時要一起看 job 結果。

若工作流根本沒有開始，先確認檔案是否已在預設分支、Actions 是否允許執行、Environment 是否存在及事件分支是否符合條件。若卡在等待審核，應由既定負責人處理，不要為了讓教學變綠而刪掉控制。本文沒有替使用者變更任何 GitHub 設定或觸發遠端工作。

> 本批完成 YAML 與本機 adapter 驗證，實測 fixture、缺金鑰及越界輸入。GitHub 遠端執行、artifact 下載及真實模型用量尚待驗收，不能用本機成功取代它們。

## 常見問題

### 為什麼 Run workflow 沒出現？

先確認有 workflow_dispatch，且工作流位於預設分支的 .github/workflows。再查看 repository 的 Actions 權限，避免只修改介面顯示名稱。

### 可以直接改成 pull request 自動觸發嗎？

需要重新設計信任與秘密的邊界。本篇只涵蓋手動、預設分支與教材輸入，不能把這份驗證直接套用到外部 fork 或未審查程式。

### 想產出文件修正而非摘要，下一步是什麼？

接著做 [[80|文件維護完整專案]]，讓候選修改先經過連結與範圍檢查，再產生可審閱的差異。報告產出與修改被套用應維持可分辨的狀態。
