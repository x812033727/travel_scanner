# A01 80→81 離線轉換匯出閘門：獨立程式覆核

2026-10-17（台北）。結論：**PASS_OFFLINE_BINDING_ONLY；正式機 HOLD**。本次只審查本機唯讀 inspector、合成測試及其依賴，沒有取得新主機快照、執行主機命令、安裝腳本、寫入稽核鏈或啟動付費工作。沒有發現此限定範圍內須先修的程式問題。

## 精確檔案

| 檔案 | 本次重算 SHA-256 |
| --- | --- |
| `inspect-transition-export.mjs` | `81c5b5eae082165bd51d9bb4b6b9c83c6bcaba27580bf4d86b1c0e9fb3745f82` |
| `inspect-transition-export.test.mjs` | `258ff602cec7b5c76c76831332653d11ba9b52834b4750f109fdc904da175b82` |
| `README.md` | `f517d64702526385d02b3a33bccbe887895ce4004e904fe9e9c0837717b9e8b7` |
| 依賴 `A01-lexicon-rebaseline-candidate/rebaseline.mjs` | `3fc95650b906d265c23e1d103db4ef58c21dbed3f2edb311c7e50dfb694136dd` |
| 依賴 `A01-host-inspect-candidate/inspect.mjs` | `ad7059772c4076d0c036fb483699b68d1f25b9c9af8924261f042854c1c9f818` |
| 對照 `A01-host-export-candidate/inspect-export.mjs` | `9f3c3ca0c41c222efd51a9a2425ce379ece703c0ae6bef091af5d9ff29ab4c4b` |

## 閘門核對

- **外部釘選。** CLI 只接受六個固定旗標；根目錄、舊 lexicon、前後 pinset 與 state 均須由呼叫者提供絕對本機路徑。`before-pins` 要有且只能有六欄、`links=80`，除記錄用的 `id` 外，其餘值逐一等於程式內固定的 `HISTORICAL_PINS`。`after-pins` 要有且只能有七欄、`links=81`，六個轉換欄位與重新計算結果完全相同；`state_sha256` 必須等於讀入狀態檔的原始位元組 SHA。這些檢查只綁定檔案，不能替呼叫者證明它們取自正式機。
- **80→81 與來源。** `verifyProposedTransition` 先用舊 inspector 核 80 鏈，僅允許已知 `ebfa590a…→835e09df…` lexicon 漂移及 `pull`、`request` 兩個 `null` 新詞；六章與合稿的實際朗讀字串不得使用兩詞。前後目錄不得相同；after 的 81 個 event ID 必須剛好是原 80 個加指定事件。原 80 個 index、journal 和手動修訂收據的檔案清單及雜湊需逐一相同，新事件的 review、record-only receipt、author manifest 和 index 必須等於依 before 與外部輸入重建的精確位元組，after 來源雜湊需等於第 81 筆 tip。舊 `inspect.mjs` 對 81 鏈仍回 `LINK_COUNT_MISMATCH`；未藉修改舊 pin 使它誤過。
- **讀回契約。** 與舊 `inspect-export.mjs` 做逐行 diff：STOP/LEASE、檔案清單、系列／集數／project、release 格式、stage/media jobs、US$25 預算十進位計算和媒體工作雙向連結的檢查段沒有變動；新程式只把來源／tip 改由已通過的 81 鏈結果提供。成功仍固定輸出 `production_status: HOLD`、`installation_allowed: false`、`paid_work_allowed: false`；清單完整性、新鮮度、站主核准及排他寫入窗口的驗證欄位均為 `false`。主機出處同樣未被此工具證明。
- **合成覆寫與寫入邊界。** 正式形狀的 CLI 沒有 lexicon hash 或 `syntheticFixture` 覆寫旗標。程式呼叫若使用合成覆寫，兩個根都須在 OS Temp 下有指定 marker，結果標 `synthetic_fixture: true`；非合成呼叫明確拒絕 hash 覆寫。Inspector 本身只匯入讀檔 API，沒有 host、DB、瀏覽器、供應商、STOP/LEASE、安裝或付費指令。測試的本機 Temp 寫入不屬於 inspector 的執行路徑。

## 重跑結果與仍待證明的事

以儲存庫記載的 bundled Node **v24.19.0** 執行 `--check` 及 `--test`，兩者退出碼 0；合成測試 **6 pass／0 fail**。測試涵蓋正常 80→81、舊閘門拒絕 81、舊索引／journal 與新事件／receipt 竄改、缺少或額外 event、前後 pin 漂移、state 來源／預算／工作／STOP／清單路徑／release 錯誤及合成 marker 缺失。這些測試沒有建立真實主機證據。

本工具仍無法證明兩份快照的主機出處、所有清單的完整性與同時性、review／owner-reference 字串的真實身分，或 shared lexicon 和 A01 稽核寫入者之間已有排他鎖；其輸出也**不授權**把第 81 筆寫入正式機。正式採用須另有新鮮完整主機唯讀捕捉、獨立人審及站主指定寫入核准，並處理共同寫入鎖和重讀；A01 round19 稿件採用、正式 verifier/listener/panel、TTS、MiniMax 圖片和成片仍各自待完成。
