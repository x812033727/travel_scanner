# 事實與示範來源

查核日期：2026-10-09（Asia/Taipei）。本表供新片獨立查核，不能沿用舊計數器的核准。

| ID | 主張 | 來源／範圍 |
| --- | --- | --- |
| c1 | Mod 是 Claude Code 的外掛程式，可回應事件及擴充介面；不是換一個語言模型 | https://code.claude.com/docs/en/plugins/mods/overview |
| c2 | 官方建立指南要求 Claude Code 2.1.287 或更新版，讀本機版本應以實際執行輸出為準 | https://code.claude.com/docs/en/plugins/mods/create |
| c3 | claude --plugin-dir 可為該次對話載入本機外掛目录，不需要先發布 marketplace | https://code.claude.com/docs/en/plugins/mods/create |
| c4 | plugin validate 為靜態分析，列出註冊事件與 API，不能證明工作成果或內容品質 | https://code.claude.com/docs/en/plugins/mods/create |
| c5 | Mod 使用使用者權限，其啟動的程序不受 Claude Code Bash sandbox 的同一層保護 | https://code.claude.com/docs/en/plugins/security |
| c6 | 本例透過資料夾 stat 及單層 fs.list 檢查三個約定檔名；不讀內容，不寫檔，不呼叫模型 | 隨附 delivery-check v2 原始碼；官方生成型別及 https://code.claude.com/docs/en/plugins/mods/api |
| c7 | v2 原生核心工作流程已由站主驗證：兩份存在／封面缺少，补檔後按刷新三份存在，時間更新 | 外部 owner-v2-workflow-completed-20261009.json；文字回報，沒有螢幕錄影 |
| c8 | 路徑存在不表示內容已完成：空白檔、同名資料夾可存在；錯檔名不符合約定清單 | 原創檔案練習與 Node harness；沒有把這些額外案例標為已完成原生 UI 測試 |
| c9 | 面板保留上次手動查詢結果，不會因畫面重繪自動讀檔；關閉視窗不等於卸載 | 本例 register.mjs；關閉/卸載語意以程式與官方單次載入文件說明，未宣稱已錄影驗收 |
| c10 | 一次提示適合單次工作，固定面板適合經常重複的同一套清單 | 教學建議與情境判斷，不是性能或費用保證 |

讀書會內容、日期與封面需求皆為本片自製練習資料，不是真實活動通知；片中日期變更練習不代表 Claude 已做過該次修改。
