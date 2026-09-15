# 本機與真實驗證分開

test_materials.py 使用固定作者資料與本機回應，驗證工具 allowlist、完整回傳歷史、UTF-8 引用範圍、缺失/危險來源、索引版本、建立不確定狀態、快取 API 家族、Batch 部分故障/有限重試/唯一採用，以及二十題本機服務。

SDK 測試以 google-genai 2.23.0 發送真正 HTTP 至 127.0.0.1，金鑰為測試佔位，不連 Google。503 測試發現 Interactions 的 retry 轉換會重送；公共 httpx_client request hook 限制每個明確 create 只有一個 POST，第二次在傳送前停止。此測試不能證明遠端 API 接受所有欄位，升版需重跑。

尚未實測：81 真實工具問答；82 真實搜尋與 Search Suggestions；83 十份遠端索引、更新及刪除；84 命中、到期、帳單；85 真實工作完成/失敗/恢復/清理；86 真實二十題問答、引用語意、帳單。以上必須有可用帳號、授權金鑰與費用上限，不以本機 fixture 補填。

