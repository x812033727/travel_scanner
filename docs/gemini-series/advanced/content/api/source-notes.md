# 官方查證及資料來源

查證日期：2026-09-14。逐篇 URL 在 sources.json 與 meta.json；沒有引用第三方文章或把本機示例當成 Google 實際輸出。使用的合成訂單、十份杯子規格、題庫、JSONL 與 SVG 皆為作者原創。

- Function calling / Interactions：目前教學採 input、steps、function_call/function_result；stateless store=False 時保留完整步驟與 thought signature。generateContent 仍支援，但物件不可混用。
- Google Search：確認搜尋 call/result、模型文字 annotations、Search Suggestions。SDK 的 URL citation index 欄位標為 UTF-8 bytes，官方教學有簡單文字 slicing 示例；本篇明確採 byte 邊界並測中文與 emoji，真實回應另驗。
- Grounding 使用條款限制原始 Grounded Results 及 Suggestions 的保存與重製。教材只分發作者合成 fixture；真實回應留 RAM，僅向同一請求的使用者提供本機短期檢視。原始 widget 若不符合被動 HTML 支援範圍，整個 live 顯示停止，不刪除 widget 後聲稱完整展示。這是本篇對一般「保存原始結果」課綱的具體調整。
- File Search：原始 Files 上傳、File Search 文件與匯入 Operation 分開追蹤。新版建立→完成索引→刪除舊版→查詢核對，避免同名多版本。原始檔過期不代表索引已刪。
- Cache：Interactions 僅隱含快取；generateContent 手動 cache 另建另查。缺少用量為 unknown，不補零。TTL 是實驗設定，沒有實測命中、過期或帳單。
- Batch：key/request JSONL、工作 ID、成功後結果檔。成功工作仍須逐題核對。重送僅使用父工作實際輸出推導的暫時故障，核對原始檔雜湊。刪除只處理本帳本列出的已終止工作與檔案。
- SDK：PyPI google-genai 2.23.0，官方專案 https://github.com/googleapis/python-genai 與 https://googleapis.github.io/python-genai/。本機固定 wheel SHA256 1e63211d44d188b8069c2b354d92b9bde25c1e821513fdbe1948b7c0d9f6b922。套件最低 Python 3.10，本機實際 3.13.15。

## SDK 相容性實驗

2.23.0 的 _api_client retry_args 將 attempts=0 正規化為1，而 _gaos/google_genai.py 的 _translate_retry_config 又將 attempts 當重試次數，導致 Interactions 503 多送一次。未改套件私有屬性；範例透過 HttpOptions.httpx_client 公開介面及 request hook，為單次 interactions.create 限制一次實際 POST。測試確認 Interactions 與 generateContent 各只送一次。這是本機線路觀察，不是 Google 遠端執行證據。

真實 SDK 本機序列化亦檢查 ImportFileOperation.document_name、cache TTL/引用、Batch metadata.output.responsesFile。測試不靠猜測 HTTP 結果欄位；現行型別與線路回應一致後才記錄通過。

## 發布限制

模型名稱與帳號可用性以實際執行當天為準。本篇未取得金鑰與費用上限，Google 呼叫零次，索引/cache/batch 資源零個。後續真實驗證回寫新的獨立收據，不能修改作者 fixture 成功紀錄充當遠端結果。所有內容包仍是未發布草稿。

