# A01 主機匯出適配器獨立複審（2026-10-16）

## 結論與範圍

**PASS，僅限離線快照格式及交叉綁定程式；正式環境維持 HOLD。** 本次只讀取本機程式、SQL、測試、匯入器與企劃檔，沒有連線正式機，沒有安裝、付費呼叫或修改其他檔案。`LOCAL_READBACK_BINDING_PASS` 只表示提供給工具的本機檔案彼此相符；程式固定輸出 `production_status: HOLD`、`installation_allowed: false`、`paid_work_allowed: false`。

本次審查的精確檔案 SHA-256：

| 檔案 | SHA-256 |
| --- | --- |
| `inspect-export.mjs` | `9f3c3ca0c41c222efd51a9a2425ce379ece703c0ae6bef091af5d9ff29ab4c4b` |
| `readback.sql` | `b6694c17aeeb6b3c41272a153216a7e455b50acd6a2e65b94887c903cf42e54d` |
| `inspect-export.test.mjs` | `95b7fa7182a6bfd28b17db3743dc610444f8e5c71a515cef4d7d63c29027a071` |

對照來源：`../../series.json` 的 SHA-256 是 `b2cdb40dd5c6b9e7723ae76fd5fb9992ca66fc0baebabc4ae0f5caabdb38502b`；`apps/api/app/video_automation/stories.py` 的 SHA-256 是 `c56a3fb11a6da285df6f870e99857a8905611c67bd684b77a8e8ba5e73eb45e6`。這些是本機檔案雜湊，並非正式機讀回證據。

## 執行的檢查

在儲存庫根目錄執行：

```powershell
node --check docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-host-export-candidate/inspect-export.mjs
node --test docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-host-export-candidate/inspect-export.test.mjs
```

`node --check` 成功；測試結果為 **8 pass、0 fail、exit 0**（約 238.4 秒，本機檔案存取偏慢）。八項涵蓋完整合成 80 事件鏈、來源／狀態／預算漂移、重複操作及錯誤連結、SQL 工作未出現在預算 CLI、三種媒體工作缺少預算 ID、系列企劃漂移、清單路徑與未知資料庫欄位、釘選後狀態變動。測試使用合成資料，沒有驗證正式機內容。

## 重要修正的複核

- `inspect-export.mjs` 第 87–101 行對預算 CLI 與 SQL 的媒體工作 ID／狀態做雙向比對；SQL 工作若未出現在對應預算操作清單會被拒絕。每筆 A01 `image`、`clip`、`music` 工作的 `pilot_budget_operation_id` 若為 `null`，會回報 `MEDIA_BUDGET_LINK_MISSING`；測試第 129–147 行涵蓋這兩種錯誤。
- `stories.py` 第 735–749 行的匯入器 `COMPARED` 共 12 欄：`title`、`premise`、`note`、`target_minutes`、`planned_episodes`、`episodes_per_day`、`image_model`、`look`、`style_preset`、`hands_off`、`visual_tier`、`compilation`。`readback.sql` 第 7–12 行從 `video_drama_series` 投影這些欄位；`inspect-export.mjs` 第 171–181 行先核對本機原始 `series.json` 雜湊，再逐欄與資料庫投影比較，並要求 `look.preset=cute-mystery`。SQL 使用固定 A01 slug、唯讀交易與 `SELECT`，未發現動態 SQL 輸入或寫入路徑。
- `README.md` 第 48–56 行改由本機 PowerShell 把精確 `readback.sql` 經 PuTTY stdin 送入主機的 `psql`，不依賴主機根目錄有此檔；使用前仍須核對兩個指令各自的退出碼及輸出。

## 仍需正式機證據

離線工具無法驗證提供的快照確實取自授權正式機，也無法證明 `run_receipts`、媒體清單及 STOP／LEASE／工作日誌的列舉完整。`observed_at` 只檢查 UTC 格式，不能證明新鮮度；SQL 投影與預算 CLI 在不同交易讀取，需靜止窗口及第二次無漂移讀回。實際 80 鏈釘選、來源事實、敘事審核、配音與畫面、付費帳本、執行中工作及站主看片仍須各自通過原有關卡。本報告不授權 A01 安裝、付費製作、B18／後五集或 YouTube 上傳。
