# 獨立查核第 2 輪：同題比較

查核日：2026-09-28。查核者未撰寫腳本、CLI 執行紀錄或第一輪查核。本輪針對第一輪四類事實修正及後續新增場景，重新讀取來源、示範檔、差異與原始結果；未將一次執行解讀為產品能力排名。

## 判定

**通過內容查核；成片關卡仍待旁白與實際時間軸。** `video.json` 的標題、描述和口播均明示 Claude Code、Codex 完成這次小題，Gemini CLI 個人帳戶在讀題前無法登入。Gemini 的起始碼測試失敗沒有被算作 Gemini 模型輸出。事後驗收的撰寫時間也明確說成在三支 CLI 嘗試之後，沒有稱為事前盲測。

英文字幕審稿指出 `v30030` 的「三支工具收到問題」可能被讀成 Gemini 模型已讀題。本輪改為「我接著送給三支 CLI 的同一個題目」，英文字幕同步改為 `sent to all three CLIs`；其後仍明示 Gemini 在模型接手前卡在登入。

## 獨立證據

| 項目 | 本輪核對結果 |
| --- | --- |
| Google 登入政策 | [Google Developers 棄用頁](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals)（2026-09-02 更新）明列 2026-06-18 起個人 free／Pro／Ultra 帳戶的 Gemini CLI Login with Google 停止服務；Standard／Enterprise 不受影響。[Gemini CLI 團隊公告](https://github.com/google-gemini/gemini-cli/discussions/28017)也說 API 金鑰認證不受影響。兩頁於本輪可讀。現行 [登入教學](https://geminicli.com/docs/get-started/authentication/)仍列個人帳戶，與具體棄用頁牴觸；影片依棄用頁及本機錯誤解釋，保留上架前重查條件。 |
| 本機登入錯誤 | 外部 `comparison-20260927/gemini-result.json` 逐字包含 `IneligibleTierError`、個人帳戶不再受此用戶端支援的說明與 `UNSUPPORTED_CLIENT`。未看到模型產生修補；`gemini/fare.mjs` 是起始碼。沒有 API 金鑰或企業授權的實測資料。 |
| 同一任務與驗收時間 | `demo/CHALLENGE.md` 列出分配總額、餘數順序、保留輸入檢查及相同提示；三份外部執行資料夾的起始檔相同。第一輪查核記錄了 CLI 結束後才寫入 `acceptance.test.mjs` 的本機檔案時間；本輪只確認檔案內容與旁白已如實標作**事後驗收**，檔案時間不是不可竄改的稽核紀錄。 |
| 真實差異 | `demo/claude.patch`、`demo/codex.patch` 各只改 `fare.mjs` 與 `fare.test.mjs`。兩份程式都保留原有輸入檢查，以商數及餘數把剩餘的分依序給前面的索引。畫面中的節錄與 patch 對得上；完整 patch 供逐行查核。 |
| 獨立重跑 | 在外部三份執行資料夾重新跑 `node --test`：Claude 13／13，Codex 9／9；Gemini 資料夾 3／6，但那是**未經 Gemini 修改的起始碼**（舊測試 2／2、事後驗收 1／4）。工具自寫測試及事後測試數目與旁白相符。 |
| 用量與付款 | Claude 原始 JSON 的 `total_cost_usd` 為 0.297987；Codex 原始 JSONL 的 `turn.completed.usage` 為輸入 198740、快取 176384、輸出 3466 token，沒有美元帳單。本片只稱前者工具估算、後者用量，不推斷訂閱實扣，也不拿用時或 token 排名。 |
| 執行輸出畫面 | `demo/claude-acceptance-output.txt` 保留一次真正執行 `node --test --test-reporter=spec acceptance.test.mjs` 的逐字標準輸出；`demo/claude-acceptance.png` 將它重排成可閱讀的終端樣式。畫面註記與 `comparison.md` 均明示**重排**，不是原生終端擷取。無帳戶密鑰或個資。 |

## 待後續關卡

- 四語 CC、旁白轉寫、實際 8–12 分鐘時長、1080p 成片、11 項品管及上架包，要在旁白合成後核對。
- 公開當日再查工具版本、登入政策、方案價格，並點開上傳說明中的來源與示範連結。這次沒有 Gemini API 金鑰／企業授權路線的模型結果，不補寫第三份能力結論。
