# 完成條件

- 能說出本課問題、輸入、允許改動和成功條件。
- 保留開始版本與真正測試結果；故障課先失敗再修正。
- 確認路徑、檔案地圖、執行既有測試；把失敗當作觀察，不先改程式。
- completed 篩選仍是錯的，辨認 actual/expected。
- node --test core.test.mjs 回傳實際狀態；reference 應全過，01 start 故障由原測試看出。
- 瀏覽器步驟另記 PASS/FAIL/NOT RUN；不能把靜態原始碼或 Node 綠燈當已看畫面。
- 交付只有授權路徑 diff，來源、舊輸出与其他儲存鍵保留。
- 独立完成 challenge 后再比對答案。

## 固定變式與補充案例

主變式：不讀前一輪報告，用全新 start/reference 重跑同一 node --test core.test.mjs，解釋差異並交第03課範圍。另做 challenge：只讀診斷 Completed 失敗，不實作。
