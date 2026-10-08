# 交稿範例的驗證範圍

2026-10-09。候選 Mod、起始材料與教案已提供；站主已貼回 Claude Code 原生靜態驗證通過結果。面板操作錄影及新版成片仍未完成。

## 站主手動完成：原生靜態驗證

站主在 PowerShell 對 `demo/delivery-check` 執行 `plugin validate`，貼回 `Validation passed with warnings`。唯一警告為未提供 author 資訊；為保留這次受驗證的程式，沒有為消除警告修改 manifest。

驗證器辨識 `session.start`、`session.end`、`command.run{command=deliverables}`、`ui.render{component=Pane}`，並辨識這份 Mod 自行回答 deliverables 指令。列出的 API 為 `$.clock.now`、`$.command.register`、`$.fs.stat`、`$.ui.close`、`$.ui.invalidate`、`$.ui.open`、`$.ui.resolve`，與原始碼的預期能力相符。

原始回報保存在 `<home>/mokaair-work/mods-clarity-20261009/demo-evidence/owner-native-validate-20261009.txt`，相鄰 JSON 紀錄原始回報、目前程式及執行檔雜湊。這是站主提供的原生工具結果，沒有 exit code、實際執行時間或代理直接錄下的畫面；不補造這些資料。它支持靜態分析通過，**不代表已執行事件、顯示面板、取得正確缺件結果或通過 plugin test**。

## 已執行：普通 Node 與真實練習檔案

使用 `verify-delivery-logic.mjs`，在 repo 外建立獨立練習副本。只匯入 `delivery-logic.mjs` 純資料函式，檔案操作使用普通 Node；沒有匯入 Mod 接線、模擬 Claude 主機或啟動 CLI。

| 驗證 | 實際結果 |
| --- | --- |
| 含空格、繁中、反斜線的完整路徑 | 保留原值；Windows 與 POSIX 路徑組合分開處理 |
| 不完整引號、相對路徑、網路／裝置路徑、提示欄位、控制字元 | 拒絕，不能悄悄猜其他目錄 |
| 起初只有文章與資料依據 | 兩項存在，封面需求缺少 |
| 複製完整封面需求後重新查詢 | 三項存在；另外兩份檔案雜湊不變 |
| 封面需求是空白檔 | 路徑存在，內容待審閱 |
| 使用底線錯檔名，然後改成連字號 | 改名前仍缺少，改名後存在 |
| 同名路徑其實是資料夾 | 只報路徑存在，沒有宣稱文件有效 |
| 注入拒絕、未知錯誤及只有 ENOENT 文字的錯誤 | 無法檢查；不猜測文字、不冒充真實 OS 權限測試 |
| 時間格式及教材原檔 | 無效時間不生成時間；所有起始材料雜湊保持不變 |

上述分成 9 組驗證，全部通過。平台為 Windows ARM64，Node v24.19.0。原始 JSON 含每組結果、實際檔案路徑、前後快照及程式／材料 SHA-256，保存在 `<home>/mokaair-work/mods-clarity-20261009/demo-evidence/delivery-logic-20261009.json`；練習副本同樣保留。

在可執行普通 Node 的環境重做時，從本目錄執行下列指令，把輸出位置換成 repo 外尚不存在的絕對路徑：

```text
node verify-delivery-logic.mjs "<新的完整 JSON 報告路徑>"
```

程式拒絕覆寫既有報告，會在報告旁建立並保留練習副本。這條指令不是 `claude plugin validate` 或 `claude plugin test` 的替代品。

## 獨立原始碼覆核

另一位未參與候選程式撰寫的覆核者檢查固定版本官方型別及接線，找到並修正 `ui.open` 回傳值誤用：固定型別為 `Promise<void>`，不能讀取其回傳值的放置資訊。程式也阻止較早的非同步查詢覆蓋新資料夾的結果。最終原始碼覆核通過；覆核者另以普通 Node 執行同一驗證程式，9/9 通過。

完整雜湊與覆核範圍存於同一外部證據目錄的 `independent-delivery-source-review-20261009-01.json`，SHA-256 為 `378cea59544b584db868101e8d31bf0e5fe9700e2a8839d72cd49d82ad9de0ad`。接線程式 SHA-256 為 `a584d7ba0f6256f59e631709814002ad44866138192ae1fac65820cfa7023dca`，純邏輯為 `d62fe38bae54c329bece9dfdaa37a02bbcb820553892d7677947b089deb78f74`。覆核沒有啟動或模擬 Claude 主機。

另由未讀作者驗證程式與報告的代理，只照教案和材料做普通檔案演練：完成缺件、補件、空白、錯名修正、單改日期與課程變式，並回答六題結果判斷。沒有發現純檔案流程的阻斷缺步；提出的「正文應直接教關閉及停止單次載入」已補進教案，仍標待原生實錄。完整記錄在 `demo-evidence/learner-walkthrough/independent-20261009/REVIEW.md` 與 `file-operation-facts.json`。這是代理教材演練，不是人類學員驗收或 Claude 操作實測。

## 還不能證明的部分

普通 Node 的 `stat` 錯誤有明確 `code`，不代表 Claude API 一定以相同形式傳遞錯誤。候選版只把明確 `ENOENT` 當缺少，其餘顯示無法檢查；原生相容性待確認。

指令註冊的實際行為、面板、按鈕、時間取得、重載與其他 Mod 共存仍需真正的 Claude Code 驗收。第一次接觸教材的人能否只照步驟完成，也尚未完成實測。

先前代理的隔離 CLI 版本／驗證／測試命令遭自動審查拒絕，回傳原因僅 `blocked by policy`，當時沒有程序啟動或測試結果。後續站主手動驗證另行記錄；代理沒有重試，也不把站主回報視為執行限制已解除。9 組普通 Node 檢查與此次靜態驗證均不等於 Mod 安裝或互動示範成功。
