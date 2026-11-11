# 2026-11-03 YouTube 檢討後的縮圖

頻道自然流量的縮圖點閱率 0.7–0.8%（YouTube 說一半的頻道在 2–10%），觀看幾乎都來自付費宣傳。站主 2026-11-03 把排程中的
六集（curio-s02／s04／s05／s06／s09／s17-v2）標題改成名字在前，縮圖用 layout d 在本機重畫；之後的集數照這樣出，不用手修：

- `headline` 兩行：**第一行是大家認得的名字**（周瑜、諸葛亮、信長、華佗），**第二行（`**` 強調）是反轉，帶問號**
  （「周瑜\n**早死了？**」）。舊的「史書裡沒有他」「早死了？11 年」「誰先上門？」沒有點名，讀起來像猜謎。仍然 ≤ 6 字。
- `sub` 補 headline 沒說的硬事實：數字、年份或那件東西（「2000 打 25000」「史書只寫『巴丘病卒』」），不重複標題。`sub` 是第二行白字大標（≤12 字），不是註腳。
- `shot` 選**一張大臉、表情明顯**的格（臉約占畫面 1/4–1/3）。預設的 layout e 把臉放在右邊圖框裡，用 `focus` 對到框中間；
  寫 `"layout": "d"` 的舊版集數，臉要在畫面右邊 55% 內，左邊的字欄才蓋不到眼睛和嘴。不選空景、群像或只有東西的格。
- qa 會警告：curio- 的 headline 不是兩行、或第二行沒有問號；`sub` 跟標題重複。

來源：YouTube 說明 CTR 基準 https://support.google.com/youtube/answer/7628154 、縮圖 A/B 測試 https://support.google.com/youtube/answer/16391400 、vidIQ 人臉統計 https://vidiq.com/blog/post/youtube-thumbnail-design-tips/ 。
