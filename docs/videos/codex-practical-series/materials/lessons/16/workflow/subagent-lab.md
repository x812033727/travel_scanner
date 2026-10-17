# 獨立分析練習

以下是可照貼的提示，沒有預先製造代理回覆。把結果另存 docs/analysis-data.md、docs/analysis-ui.md。

代理 A：只讀 core.mjs、core.test.mjs、fixtures、tests；檢查同名ID、immutability、非法整批匯入、台北跨日、未知時間。每個發現給輸入、預期、目前結果、檔案與證據，禁止改檔。
代理 B：只讀 index.html、app.mjs、style.css、storage.mjs；檢查文字呈現、键盤焦點、390px布局、reload与损毁storage。可執行獨立瀏覽器驗收；未跑的項目標 NOT RUN，禁止改檔。
主代理：先讀兩份結果，重現可操作發現；不以兩票同意代替驗證；只將確認問題列成後續任務。
App／CLI 依你當前版本的子代理入口派發。若入口不可用，可在兩個獨立聊天手動派發並標示為「獨立聊天分析」；不能標示已用了未驗證的子代理功能。
