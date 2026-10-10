# 本機唯讀 MCP

node --test tests/mcp.test.mjs 會真正啟動 stdio 子程序並驗 JSON-RPC，但不代表已連入 Codex。
手動協定檢查：啟動 node mcp-server.mjs，輸入每行一個 JSON：

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"practice","version":"1"}}}
{"jsonrpc":"2.0","id":2,"method":"resources/list"}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read_weekly_report","arguments":{"from":"2026-10-05","to":"2026-10-11"}}}
```
URI: practice://tasks、practice://weekly-report；工具 list_tasks(noargs)、read_weekly_report(from,to)。write_task 与任意路徑會拒絕。stdout 只輸出協定；Ctrl+C 停止。
連到 Codex 時，用你版本的 MCP 設定介面註冊 command=node、args=[絕對 mcp-server.mjs 路徑]；CLI 可在確認當前 help 後用 codex mcp add small-steps -- node ABSOLUTE_SERVER_PATH。只在錄製用設定環境示範，讀回列表，再實際讀資源；教材沒有替你安裝全域設定。
