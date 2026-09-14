一段可重用提示詞、一本技能說明與可安裝的擴充套件，各自解決不同問題。本篇把「檢查 Markdown 是否有主標題與來源章節」做成小型技能，再包成 Extension，使用兩個教材版本練習安裝、停用、更新與回退，並保留程式真正的錯誤結果。

## 成品與驗證範圍

先完成 [[42|Agent Skills 入門]] 與 [[72|自訂指令庫]]，準備 CLI 0.59.0、Node 與文字編輯器。練習包有 doc-check-1.0.0、doc-check-1.1.0 與 samples。所有內容為本篇原創，不連接外部服務、不包含金鑰；來源與格式於 2026-09-14 對照官方文件。

本篇已在 Windows、Node 24.19.0 使用實際 CLI ExtensionManager 模組完成生命週期驗證，並執行檢查腳本。另以終端命令測試時，在 Node 24.13.0 與 24.19.0 都曾遇到 libuv 異常退出。兩種證據分開保存：不能把模組測試通過，當成終端安裝流程已穩定通過。

## 第一階段：把技能限制在一件事

doc-check 只檢查兩項文字結構：有沒有一級標題，以及有沒有名為「來源」的二級標題。它不查引用真偽、不生成文章，也不自動修檔。這種明確範圍適合練習；如果要求「全面確保文章正確」，兩個正規表示式不可能提供足夠證據。

開啟 skills/doc-check/SKILL.md，頂端 YAML 放 name 與 description，正文寫啟用後應怎麼工作。description 用來說明何時適合使用；它不是每次必然觸發的保證。一般 GEMINI.md 提供專案長期指示，技能則保存特定工作的步驟與資源，不能因為兩者都用 Markdown 就當成同一種檔案。

!include-code examples/73/doc-check-1.0.0/skills/doc-check/SKILL.md

## 第二階段：先把腳本單獨跑通

進入 doc-check-1.0.0/skills/doc-check，執行下面三次。範例相對路徑會回到 73/samples；如果你改過解壓層級，先核對檔案存在，再執行。路徑有空格時，把整個路徑當成一個引數，用引號包住，避免把它拆成多個輸入。

```bash 終端機：從 skills/doc-check 執行
node scripts/check-doc.mjs ../../../samples/good.md
node scripts/check-doc.mjs ../../../samples/bad.md
node scripts/check-doc.mjs missing.md
```

good.md 有兩個必要標題，回傳空 errors 與結束碼 0。bad.md 缺少兩者，回傳 missing_title、missing_sources，結束碼 1。missing.md 不存在，回報 ENOENT 與結束碼 2。這三組都已實際執行；它們是程式輸出，不是請模型模仿的訊息。

| 結束碼 | 意義 | 下一步 |
| --- | --- | --- |
| 0 | 兩項結構檢查通過 | 另外核對引用內容 |
| 1 | 文件缺必要標題 | 查看 errors 並修文件 |
| 2 | 引數或讀檔失敗 | 核對命令與路徑 |

不要把所有非零結束碼都改寫成「請再試一次」。缺來源章節與檔案不存在需要不同修正；保留原始錯誤，才能讓使用者知道該改文件還是命令。若技能由模型呼叫腳本，最後回應也應呈現真正的結束碼，不可以只說「檢查完成」。

## 第三階段：加入套件清單並檢查安裝

回到 doc-check-1.0.0 根目錄，確認 gemini-extension.json、skills/ 與 CHANGELOG.md。最小清單只有名稱和版本，沒有 MCP 伺服器、Hooks 或額外的自動執行設定。安裝前仍要逐檔閱讀；套件一旦加入腳本或其他能力，應重新評估其用途與存取需求。

!include-code examples/73/doc-check-1.0.0/gemini-extension.json

先把 doc-check-1.0.0 完整複製成新的 extension-source 資料夾，保留原始兩個版本。另開 PowerShell 視窗，從解壓後的 73 資料夾執行下列準備步驟。它會建立新的測試家目錄；如果同名資料夾已存在，先停下核對用途，不要覆蓋。完成後關閉視窗即可結束這次環境變數設定。

!include-code examples/73/prepare.ps1

macOS／Linux 的子 shell 隔離方式見 [[69|載入實驗的環境準備]]，本篇未在這兩個平台實測。確認 GEMINI_CLI_HOME 指向新的 isolated-user 後，再執行以下命令。install 使用來源目錄，disable、enable、uninstall 使用 manifest 的套件名稱；不要把它們貼進 Gemini 對話輸入框。

```bash 終端機：從解壓後的 73 資料夾執行
gemini extensions install ./extension-source
gemini extensions list
gemini extensions disable mokaair-doc-check --scope workspace
gemini extensions list
gemini extensions enable mokaair-doc-check --scope workspace
```

閱讀安裝確認內容後再繼續。一般使用者不必加略過確認的參數。本文的模組測試只對自己建立、已讀取的最小本機套件提供同意，沒有對任意第三方擴充套件設定全面核准。重新開啟 CLI 後，核對套件與技能清單，再以指定樣本要求文件檢查，查看是否真的呼叫腳本。

本機模組實測中，安裝後版本為 1.0.0、isActive 為 true，停用後為 false，重新啟用後回到 true。這裡驗的是套件管理狀態；真實模型是否選對技能、是否正確呈現腳本結果，仍需另存互動紀錄，不能用 metadata 取代工具呼叫證據。

## 第四階段：更新與可理解的回退

官方本機安裝會建立副本，因此編輯來源檔案不代表已安裝版本同步改變。教材的 1.1.0 補充驗證限制說明，程式行為維持不變。用編輯器把 1.1.0 的清單、SKILL.md 與 CHANGELOG.md 複製到 extension-source 對應位置，保留原始版本資料夾，再執行 update 並重新核對。

```bash 終端機：更新後重新核對
gemini extensions update mokaair-doc-check
gemini extensions list
```

回退時先記下目前狀態，卸載這個指定套件，再從保留的 1.0.0 目錄安裝。回退不是把顯示的 version 字串改小；真正的腳本、SKILL.md 與資料都要回到已保存版本。再跑 good、bad、missing 三個樣本，確認行為與先前紀錄一致。

```bash 終端機：只移除教材套件
gemini extensions uninstall mokaair-doc-check
gemini extensions install ./doc-check-1.0.0
gemini extensions list
```

## 遇到成功訊息後異常退出

本次 Windows 終端測試曾先印出 installed successfully 或 successfully disabled，隨後出現 UV_HANDLE_CLOSING 斷言，結束碼為 3221226505。因此這個操作的程序結果屬失敗，不能只截取前半段成功文字。先停下後續寫入，再檢查目前清單與實際套件檔案，避免未核對狀態就重複安裝。

這個現象保留在本篇驗證紀錄中，尚未宣稱已修正。模組測試使用獨立暫存家目錄重新驗證安裝、停用、更新、卸載與回退；它幫助確認套件格式與管理行為，但無法替代失敗的終端入口。正式推廣前，應在目標 Node／CLI／作業系統組合補做完整命令驗收。

> 本篇已驗證技能檔解析、三種腳本結果與擴充管理模組。終端生命週期仍有 Windows 異常退出待複驗，模型觸發與回應品質未測；兩項都保留在發布前清單。

## 常見問題

### 停用後來源資料夾會消失嗎？

停用控制套件是否啟用，不會把你保留的來源文件當成要刪除的內容。卸載與刪除自己保存的版本也不同；回退需要原始版本，完成驗證前先保留它。

### 修改腳本後為何仍跑到舊邏輯？

先核對是來源副本還是已安裝副本，再核對更新與重新啟動結果。把版本號、實際腳本位置與結束碼一起記錄，避免只比較回應措辭。

### 可以用這個技能自動改整個專案嗎？

本教材只檢查單一文件，不包含批次修改。需要跨模組工作時，先依 [[74|大型專案上下文教學]] 定義修改範圍、保存 Git 差異與恢復紀錄，再設計相應工具與驗證。
