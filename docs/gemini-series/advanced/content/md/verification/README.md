# 本機 CLI 模組與練習驗證

2026-09-14，Windows，Node 24.19.0，Gemini CLI 0.59.0。需要先安裝 Node、Git 與這個確切版本的 CLI。腳本只使用自己產生的暫存家目錄、假資料與已檢查的本機套件，不需要模型金鑰，不會替你登入或發送模型請求。

從解壓後包含 `verify-cli.mjs` 與 `examples/` 的資料夾執行：

```text
node verify-cli.mjs "你的 @google/gemini-cli 套件資料夾絕對路徑"
```

傳入路徑需含 package.json 與 bundle/。全域安裝時，可先執行 `npm root -g` 找到 node_modules，再接上 `@google/gemini-cli`；不要把 gemini.cmd 的路徑當成套件資料夾。本驗證依 0.59.0 的內部模組入口鎖定，其他版本會先拒絕；這些入口不是穩定 API。

程式真正呼叫已安裝 CLI 的記憶管理、設定載入、指令展開、技能解析與 ExtensionManager。它建立隔離資料、執行 Node 測試、在暫存專案操作 Git，最後移除自己建立的暫存目錄；輸出只保留非秘密標記。成功時寫入 `verification/local-cli.json`，每組精簡結果也存於 `examples/<篇號>/verified-local.json`。

本批共有 48 筆分步觀察（69:5、70:4、71:8、72:19、73:9、74:3），並含其他斷言。這不是 48 次模型呼叫。69 的 `/memory show` 常駐內容與 JIT 工具新增內容分開記錄。72 的 18 種展開結果是最終提示詞，不是模型回答。74 的修正是作者參考答案，不是 AI 生成結果。

以下仍未通過完整驗收，不能用本地 PASS 取代：

- Windows 終端 `gemini extensions` 曾顯示成功後以 libuv 斷言異常退出；見各包 native-cli-limitations.json。ExtensionManager 模組生命週期通過，終端入口仍須複驗。
- 模型是否遵循指示、三個命令的回答品質、是否實際觸發技能，尚未進行雲端對話測試。
- 已登入會話的 `/resume` 與壓縮流程尚未實測。
- macOS／Linux 執行與不同 CLI 版本的升級比較尚未實測。

單篇操作請參考網站教學；本程式供進階讀者與編輯重做底層驗證，不是日常啟動 Gemini 的替代入口。
