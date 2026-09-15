# 本批實際驗證與重做方式

本包保存 75–80 的原創合成資料與驗證程式，不含帳號或模型金鑰。2026-09-14 使用 Windows、Node 24.19.0、Gemini CLI 0.59.0、Python 3.13.15 與 MCP Python SDK 2.2.0。

## CLI 與 MCP

先在自己的虛擬環境安裝 `examples/75/requirements.txt`，另安裝固定 CLI 版本。從包含 `verify-cli.mjs` 的資料夾執行：

```text
node verify-cli.mjs "CLI 套件根目錄絕對路徑" "有 MCP 2.2.0 的 Python 執行檔絕對路徑"
```

第一個路徑包含 package.json 及 bundle/，不是 gemini.cmd。內部入口鎖定 0.59.0，其他版本必須重新驗證。程式只使用自己建立的暫存資料及本機 stdio，禁止 fetch 模型請求，不讀取或更新原有個人 CLI 設定。

實際驗證涵蓋 MCP 工具探索與十種連線／查詢觀察、十一種 hook／停用計畫觀察、三種代理定義觀察、四種工具政策判斷。它沒有執行模型，不以底層模組成功代表互動 CLI 全部通過。Hook 逾時反例可能另印清理已退出程序的訊息，應以紀錄的逾時與決策判讀。

## Python fixture

驗證程式使用標準函式庫及 PyYAML（只用於閱讀 Actions 範例）。在自己的驗證環境安裝 PyYAML，再執行：

```text
python verification/test_exercises.py
```

測試涵蓋二十份文件續跑、資料更動、成品損壞、寫入鎖、失敗停止、JSON／JSONL 判讀、審查證據與衝突、Actions 本機 adapter、十份文件連結與 Git patch 檢查。fixtures.json 的通過數由實際執行結果產生。

## 沒有宣稱完成的事項

- CLI 模型選 MCP 工具與互動停用流程。
- 模型真正觸發 BeforeTool 並核對磁碟寫入前後。
- 兩個子代理的實際回答、工具使用與並行方式。
- 真實 Headless 模型呼叫、品質、時間與費用。
- GitHub hosted runner 執行、Environment 審核及 artifact 下載。

fixture、作者參考答案及概念圖都各自標示；它們不是雲端對話或介面截圖。
