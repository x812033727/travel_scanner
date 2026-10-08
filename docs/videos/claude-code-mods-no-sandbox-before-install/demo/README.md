# 工具呼叫計數器：可讀教學來源

這份最小範例依 [Create a mod](https://code.claude.com/docs/en/plugins/mods/create) 的四個事件設計，2026-10-09 查核。程式為教學改寫；不含外部 dependencies，不自行讀檔、不開程序、不連網、不呼叫模型。

**狀態：來源已寫好，未在本機 Claude runtime 執行、未驗證通過。** 本機初次讀取是 2.1.285，低於文件要求的 terminal 2.1.287。主協調者另備妥隔離的 2.1.293 CLI；執行 validate/test 被 automatic approval review 拒絕，原因只有 `blocked by policy`；不能改用另一條路徑繞過。這裡沒有偽造 pass 記錄。

`first-mod/` 三份 runtime 檔案分別提供 manifest、模組入口、四個 hook。`tests/counter.test.ts.example` 只是離線邏輯測試的來源模板，不會被測試工具發現或執行，也不是真正讀示範檔。

後續有適用且已獲授權的可執行環境時，先把整個 `first-mod/` 複製到 repo 外的示範工作區，確認 CLI 版本。**在執行 plugin test 以前**，於那個外部工作區將 `tests/counter.test.ts.example` 複製成 `tests/counter.test.ts`；不要在本 repo 留下這份可被發現的測試副本。準備完成後，才從外部 `first-mod/` 的上一層執行：

```text
claude plugin validate ./first-mod
claude plugin test ./first-mod
claude --plugin-dir ./first-mod
```

最後一條會啟動 session 並執行這份 Mod，不能把它當純讀檔檢查。操作前仍要自行審查原始碼。

成功核對順序：

1. validate hooks 應列出 session.start、tool.call、command.run{command=tally}、ui.render{component=Spinner}；calls 應只有 command.register、ui.invalidate。
2. test 用 stub 回答工具事件，兩次事件後 tally 應回傳 `Tool calls since load: 2`；不會真正讀檔，也沒有模型回合。
3. 在互動 session 確認外掛啟用，輸入 `/tally`；剛載入且無事件時預期為 0。
4. 經適用的模型用量授權後，才請 Claude 讀自製的示範檔；保存實際工具事件、工作前後計數與畫面；自載入起累計，以差值核對這次工作。不要強制輸出必須為 2。
5. 編輯 spinner suffix 並保存；單次資料夾載入會 hot reload，calls 從 0 重算。

這裡計數的是收到的 tool.call，不是成功次數，也不是任務進度百分比。進階持久狀態應另行實作與測試。
