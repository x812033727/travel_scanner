# 資料契約

v1 是 `{version:1,tasks:[{id,title,completed}]}`。v2 增加 completedAt，已知值必須是能精確 roundtrip 的 UTC ISO，例如 `2026-10-05T02:00:00.000Z`。
pending 項目的 completedAt 必須是 null。v1 轉換時不查歷史、不猜日期；原本 completed=true 保留，completedAt=null。
ID 唯一但 title 可以相同。原有資料順序保留；回報與篩選是純函式。
瀏覽器載入 v1 只轉成記憶體中的 v2，不立即写儲存；第一次變更才保存 v2。儲存寫失敗需明確提示。v2 reset 寫空 v2 文件，保留 v1 但阻止下次 reload 回填舊資料。

JSON 用帶 version 的文件。CSV 標頭固定 `id,title,completed,completedAt`，布林只能 true/false，未知時間是空欄位；支援逗號、引號、換行的正確 quoting。
CSV 的列分隔可為 LF 或 CRLF，可帶 UTF-8 BOM；引號內標題的 CRLF/LF 原樣保留，不做全域換行正規化。引號外裸 CR 不是有效列分隔。
非法列、重複 ID、與現有 ID 衝突時整批拒絕，不留下半批新資料。

週報的 from/to 是包含整天的台北日曆日期，使用 +08:00 邊界。未知完成日期另列 unknownCompleted；completedInWeek 只算已知日期在期間內、目前仍完成的項目。
這是「目前清單的週報」，不是事件紀錄；取消完成或刪除會改變統計。沒有歷史事件資料就不聲稱歷史生產力。

封存只選 completed=true、completedAt 已知且 <= 明確 UTC cutoff 的項目。unknown 及 pending 保留。先列清單，再於新目錄保存完整來源備份與結果；restore 是寫入另一個新檔。
