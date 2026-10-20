# WD-40 X06 v4｜套用後獨立差異及媒體橋接覆核

**PASS（提示詞差異與零成本橋接；主影片仍 STOP）。** 以 v3 主片 SHA-256 `931efad38297c832fd11a2aedfc12cc2ef5c61373e36632a1fcd916dbdf0fc68` 對照 v4 `acfeb244c3d67578223516a749617c89b2dad8f3df28766f85bae4e6f460ccb4`，逐欄 JSON 比對全數場景，只有 `x06-b03-s12`、`x06-b03-s16`、`x06-b04-s02` 的 `data.prompt` 三處不同；文字與已 PASS 的離線提案（SHA-256 `b697f096e66f2e82eda849ea16166049dc66443aba26346f6554e070212d9219`）逐字相符。`drafts/visual-safety.mjs` 同步替換這三段，場景順序、旁白、數字、來源、相機、look 與 Shorts 未改。v3 原審查可以在這個範圍內沿用。

獨立讀取媒體工作區 `review/local-preview/v4-bridge.json` SHA-256 `fc0054acbb4ac8f95dee244c0d6b3191fda77772383171b778b49bb7d9075ae8`，核對橋接前 manifest SHA-256 `efd4feabc68b8567104b3169308751a4f40d0aa84d2303521725c94818de5422` 與當前 manifest SHA-256 `39635fc22fc2dec9b71e736fc61137d0f50c22baff1adbcac127a821e5488080`。34/34 保留鏡頭的完整選圖記錄相同，實際圖檔 SHA 全部匹配；三個舊 HOLD 均已從當前 manifest 撤下而保留舊證據。已付費未評審的 `x06-b04-s02b` 原圖仍在；總帳 SHA-256 `f74f080e0c970330826a0176f719f537ab9208fe2fc41cb6655df799a2d16679`，US$1.1105／83 圖／82 評審／未結 0，均未變。

主媒體工作區 `STOP` 仍在，當前人工 gate SHA-256 `c48c604145128b5b98bb02ba9d3a5b2ba31ab6f478a2aba9541e9b248d6b7b5d`。v4 只有 **34/78 暫可用**，其餘 44 鏡待畫，三鏡舊 HOLD 不可因新提示詞獲得通過。共享額度餘裕仍不足，這份覆核**不核准新付費圖、媒體完成或發布**。
