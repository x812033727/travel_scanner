# Windows 擴充命令追加驗證

2026-09-14，CLI 0.59.0 原版 bundle，沒有修改 CLI 或攔截 process.exit。

| 入口與 Node | 實際結果 |
| --- | --- |
| node bundle/gemini.js，24.13.0 | list 為 0；install 顯示成功且副本存在，但結束碼 3221226505，停止後續命令 |
| node bundle/gemini.js，24.19.0 | install、list 為 0；工作區 disable 顯示成功後結束碼 3221226505，停止 |
| node bundle/gemini.js，22.23.2 | 十四步均為 0，含安裝、工作區停用／啟用、更新、卸載及回退 |
| Windows PowerShell 5.1 → npm gemini.cmd，22.23.2 | 十四步均為 0，另核對每個安裝來源檔位元組及 list 的 Workspace false／true |

[三版本紀錄](native-cli-followup-20260914.json)與[PowerShell 紀錄](native-cli-powershell-20260914.json)保留逐步輸出、結束碼、版本及隔離副本狀態。所有暫存家目錄已移除，未更動個人 CLI 設定、登入或發送模型請求。測試使用重導標準輸入輸出，沒有可視終端視窗或雲端會話證據。

最初的測試腳本未提供 update 的技能確認，等待 45 秒後中止，尚未產生完整收據。修正測試器後，僅對已閱讀的原創本機套件提供一次 y；CLI 本身、確認流程與範例內容均維持原版。不要將這個測試器變成任意第三方套件的自動批准器。

綜合 ZIP 解壓後可重做：

```powershell
python verify-native.py --node "C:/你的 Node 22.23.2/node.exe" --cli "C:/你的 node_modules/@google/gemini-cli" --powershell "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe" --output "新的驗證紀錄.json"
```

--cli 使用含 package.json 與 bundle 的套件目錄。PowerShell 模式另要求同一 node_modules/.bin/gemini.cmd 存在；PATH 僅在子程序中指向指定 Node。輸出檔若已存在即拒絕覆寫。新版測試器在錯誤或逾時後停止後續寫入；逾時只終止自己啟動的程序樹。

上游有[相同斷言回報 #13167](https://github.com/google-gemini/gemini-cli/issues/13167)，於本次查證時可讀；這只能佐證有人回報同類症狀，不表示本文測試組合已由上游修復。Node 22.23.2 通過也不是所有 Node 22 版本的保證。尚待驗證的是模型是否真的觸發技能與呈現腳本結果，以及其餘需要已登入會話的操作。
