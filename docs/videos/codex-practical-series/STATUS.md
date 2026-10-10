# 狀態與接續點

狀態日期：2026-10-11（Asia/Taipei）。這份狀態不把企劃或參考程式算成36支成片。

| 項目 | 当前狀態 | 驗收依據 |
| --- | --- | --- |
| 18課／36版規格 | 已完成規格 | 18／36 completeness及獨立教材一致性覆核 |
| 18份教材包 | 已打包並驗證 | 54份快照、source23／23、整合11／11、18ZIP兩次重建hash一致 |
| 第01課CLI產品操作 | 已實跑，只讀 | 真實Codex session；測試2PASS／1FAIL；五檔未變 |
| App原生操作截圖 | 待取得 | 当前文字工作階段 native computer API 不可用 |
| 第01課CLI稿件 | 已撰寫／独立查核通過 | 60卡162行，20主張PASS，outline核准讀回 |
| 第01課CLI媒體 | 音訊／靜態畫面通過，合成中 | 正文13分27秒，162句0flags且audio核准讀回；字幕與成片QA待完成 |
| 其餘課產品操作／媒體 | 尚未開始 | 首批教學模板驗收後依序製作 |
| 站主首課跟做 | 待驗收 | 完成主案例、變式及原因說明 |
| YouTube上傳／公開 | 尚未進行 | 上傳包、站主操作與公開讀回另行記錄 |

最新教材在 `C:/Users/x8120/mokaair-work/codex-practical-series/build-07/delivery`；build-08是重建對照，兩者18ZIP bytes相同。這版補清01的外層提示檔位置；18課五檔／來源實作未變。先前build與delivery保留為歷史，不作最新教材。

CLI第01課原始執行在 `runs/lesson-01-cli`；媒體父目錄為 `media`，工具附上影片slug。原生App素材仍是首課兩版及下一批製作的必要条件；CLI聲音／技術品管通過也不能替代你的跟做回饋。

2026-10-11旁白檢查遇到 Windows confirmed journal rename EPERM。已從完整臨時回覆核對request及answer hash、備份原sent紀錄，恢復同一筆已知轉寫結果，沒有重送那筆provider請求。收據在 `runs/known-transcript-recovery`；續跑只接未檢查段落。問題已有看板票 `2026-10-09-windows-speech-journal-rename-failures`。

完整教材驗證與尚未通過的全 tools 檢查見 [VALIDATION.md](VALIDATION.md)。

接續時先讀本表、`evidence`、工作目錄的收據及看板票，確認目前文件與素材hash。未完成或未知的provider呼叫不得直接重送。只續做已核對尚缺的階段。
