# Claude Code 待辦清單練習

需要 Node.js 22 或以上；不需要 npm install，也沒有資料庫或 API 金鑰。

1. 在終端機切到這個資料夾。
2. 執行 `npm test`，先記下測試基準。
3. 執行 `npm start`，開啟終端機印出的本機網址。
4. 在另一個終端機的同一資料夾執行 `claude`，或用桌面 Code 開啟此資料夾。
5. 結束網站伺服器時，在原終端機按 Ctrl+C。

起始版可以新增、勾選與刪除待辦；重新整理後清空是起始版的預期行為。
所有檔案都是練習材料，可另複製一份再開始修改。
參考完成版增加篩選與本機儲存；不包含雲端帳號或跨裝置同步。

完整教學：https://mokaair.com/zh-TW/life/claude-code-tutorials

## 檔案

- index.html：頁面元素。
- style.css：樣式。
- app.js：畫面與事件。
- model.js：純資料操作。
- tests/model.test.mjs：Node 內建測試。
- server.mjs：只監聽 127.0.0.1 的練習伺服器。

© Mokaair。本練習程式採 MIT License，詳見 LICENSE。
