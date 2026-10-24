# C20 Zippo v8｜機器專案獨立逐項覆核

2026-10-24；非作者 `/root` 唯讀核對基準：PR #1808 `ed27c8f1624afe9bf15c94e23dad92e28f6ca778`。此收據只查核已核准稿件至機器專案的投影，不重做舊稿的史料審查，也不代表音訊、影片或付費驗收。

## 凍結輸入

- 劇本 `v8-short-script-candidate-20261024.md` SHA-256 `8BF33F7F733D5ACB8C7AC64186B5932C43E6BB06867A6FFBF2ECC6BF0E68D82D`。
- 純旁白 `v8-short-blind-plain-20261024.txt` SHA-256 `358000A1EBA0DEF8D2C3FBE0C7DDB8276BBACAB74F82C534750BBBEAC40814E5`。
- 分鏡 `v8-short-visual-plan-candidate-20261024.json` SHA-256 `D30CBE9F9E92BF8339D82671879EF465538D1691885B5161CA85D7E10D571419`。

## 檢查與判定

獨立程式讀取三份凍結輸入和新專案 `video.json`，對每一鏡核對 `line_id`、旁白原文、來源標籤、`claims`、插圖 prompt 或字卡文字及順序。結果 **36／36 PASS**；33 鏡 `still`、3 張 `big` 字卡，`look.preset=cute-mystery`，slug 為 `story-everyday-zippo-c20-short-v8`。顯示與字幕用的 `text` 逐字維持站主核准稿。

只有 `c200102` 設 `say`：將該句的 `Zippo` 展開為「之寶」，其餘字不變；`say_for` 等於原句 UTF-8 SHA-256 前 12 位。Zippo 中國官方[常見問題](https://china.zippo.com.cn/wap-cn/support/faq.html)明示「Zippo（之宝）」為中文名稱，故這項文字讀音提示有品牌來源。繁中實際發音是否自然，仍須聽生成音檔判定。

## 尚未通過

現行 lint 的短版時長兩項錯誤仍有效，紙上估時不能代替實際配音。C20 預算帳戶與可歸因付費路由、實際供應商價格、配音人耳驗收、實際片格插圖時間、後台匯入及成片均未完成。此收據不授權供應商請求、上傳或發布。
