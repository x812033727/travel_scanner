# 三支工具同題試跑：可重現紀錄

記錄日期：2026-09-27。這是一次小型實作示範，不是模型能力排名。三份資料夾以相同的 `fare.mjs`、`fare.test.mjs`、`CHALLENGE.md` 建立獨立 Git 起點；對三支工具都送出同一句英文提示：`Read CHALLENGE.md and complete the task. Report what changed and the test result.`。起始的兩個測試均通過，但 `100` 分給 `3` 人會產出 `[33,33,33]`，少了一分。事後才加入的 `acceptance.test.mjs` 沒有交給工具看。

| 工具 | 本機版本與執行方式 | 結果 | 工具自寫測試 | 事後驗收測試 | 輸出所報用量 |
| --- | --- | --- | --- | --- | --- |
| Claude Code | 2.1.270；`-p`、JSON、`acceptEdits`，只允許 `node --test` 命令 | 修改 `fare.mjs`、測試；約 55 秒，程式以商數與餘數分配 | 9/9 通過 | 4/4 通過 | JSON 的 `total_cost_usd` 為 0.297987 美元，這是工具估算值，不代表訂閱帳戶實際扣款；快取讀入 77,334 token，寫入 19,388 token，輸出 2,576 token |
| Codex CLI | 0.158.0-alpha.2.1；非互動、workspace-write、JSONL | 修改同兩檔；約 174 秒，程式也以商數與餘數分配 | 5/5 通過 | 4/4 通過 | `turn.completed` 記載輸入 198,740 token，其中快取 176,384，輸出 3,466；輸出沒有美元帳單數字 |
| Gemini CLI | 0.61.0；非互動、`auto_edit`、JSON；使用本機既有個人帳戶登入狀態，未試 API 金鑰或企業授權 | 在讀題前登入失敗，`IneligibleTierError: UNSUPPORTED_CLIENT`；錯誤文字明示個人帳戶已不受支援；約 32 秒、未改檔 | 起始的 2/2 通過，非其產出 | 起始的 1/4 通過，非其產出 | 無模型執行用量 |

事後驗收包含：`100/3` 必須為 `[34,33,33]`、餘數順序與零金額、0–500 分與 1–20 人的總和及差額性質、非法輸入。三份拷貝的原始 CLI 記錄、完整 `git diff` 與實際測試輸出保留在本機製作工作區；可公開且已檢視的兩份差異在 `demo/claude.patch` 與 `demo/codex.patch`。

`demo/claude-acceptance.png` 是本機 Claude 修補資料夾重跑 `node --test --test-reporter=spec acceptance.test.mjs` 的**真實標準輸出視覺化**；它是由文字重排生成的圖，不是原生終端機螢幕擷取。完整逐字輸出放在旁邊的 `demo/claude-acceptance-output.txt`；製作時使用的截圖腳本留在本機工作區。影片字卡也明示「原始輸出重排」。

比較限制：三工具使用當時預設模型，帳戶與授權模式不同，且執行有重疊；用時與 token 不可當公平跑分。[Google Developers 棄用說明](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals)指出，2026-06-18 起個人 free／Pro／Ultra 帳戶無法再以 Login with Google 使用 Gemini CLI；Standard／Enterprise 不受影響。[Gemini CLI 團隊公告](https://github.com/google-gemini/gemini-cli/discussions/28017)另指出 API 金鑰認證未受影響。現行登入教學仍列個人免費層，與棄用公告牴觸；本片依具體棄用公告及本機錯誤解釋，不推論 Gemini 修程式能力。正式影片若要主張「三支都完成同一題」，須以支援的授權重新跑 Gemini 並更新紀錄與畫面。影片可以如實呈現這一次的「兩支完成、一支無法開始」，並說明可用性也是選工具時要先查的一關。價格應在上架當天另查官方頁；這次不把訂閱方案硬折算成每次成本。

重跑步驟：把 `demo/fare.mjs`、`fare.test.mjs`、`CHALLENGE.md` 各複製進三個空資料夾，分別 `git init` 並提交起始檔；以相同提示各執行 CLI；保留原始結果和 `git diff`；跑 `node --test`，再複製 `demo/acceptance.test.mjs` 進各資料夾跑 `node --test acceptance.test.mjs`。
