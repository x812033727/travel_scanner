# GitHub Actions 實測入口

[回深入教學目錄](README.md) · [第 92 篇](../lessons/92.md) · [驗證紀錄](evidence/live/ci-workflow-validation.json)

使用者指定的測試儲存庫為 [x812033727/travel_scanner](https://github.com/x812033727/travel_scanner)。本批提供 [Claude tutorial validation](../../../.github/workflows/claude-tutorial-validation.yml)，配合 monorepo 內的練習檔路徑。它目前只在工作分支，尚未合併或在 GitHub 執行。下載包中的 review.yml 仍供獨立練習專案使用。

## 現在已確認什麼

本機系列測試 12 項與 workflow 使用的基礎測試 8 項全部通過，包含 YAML 解析、手動觸發、分支限制、唯讀權限、固定 Action 提交及 JSON 輸出路徑。這些結果不等於 GitHub runner 已執行成功。

2026-09-14 唯讀預檢查得儲存庫 secrets 為 0、environments 為 0，沒有已登錄的 Claude workflow。本機 Claude CLI 登入已恢復；GitHub Actions 仍需自己的 CI 憑證。

## 合併後的操作

1. 在 GitHub 的儲存庫 **Actions → Claude tutorial validation → Run workflow**，選擇預設分支，保持 `run_model=false`。工作會固定讀取這次 dispatch 的提交，執行待辦模型、自動化與 SDK 狀態測試。成功判準是 baseline 綠燈，model-review 顯示 skipped。
2. 在儲存庫 **Settings → Environments** 建立 `claude-lab`，將部署分支限制為預設分支；若方案支援且需要人工放行，可加入 required reviewers。這裡的 environment 是驗證工作的控制點，workflow 沒有部署步驟。
3. 在 `claude-lab` 的 **Environment secrets** 儲存專用 `ANTHROPIC_API_KEY`。在 GitHub 輸入框操作，不將值寫入教材、工作流程、提交或聊天。這是該範例選用的 API 計費方式，與本機訂閱登入分開。
4. 再次手動執行，選 `run_model=true`。baseline 通過且環境條件滿足後，Claude 只讀取合成的 toggle.diff 與 model.js，回傳正體中文摘要及 findings。呼叫限制為 6 turns、0.50 美元與 10 分鐘工作逾時。
5. 下載 `claude-tutorial-review-<run_id>` artifact，確認 JSON 含非空白 summary 與字串陣列 findings。人工確認指出 `===` 變成 `!==` 會切換其他待辦而非指定待辦；缺少該發現時只能算流程有跑完，不能宣稱審查品質通過。

需保存 run URL、dispatch SHA、兩個 job 的結論、JSON 結果及人工判讀。artifact 預設保留 7 天，僅含驗證後的結果。不要將模型自己的「測試通過」敘述當作實際測試紀錄。

## 失敗與停止

- `Set ANTHROPIC_API_KEY ...`：環境尚未設定可用憑證；模型呼叫尚未開始。
- baseline 失敗：先查看測試失敗項目，model-review 不執行。
- 模型認證、預算或 JSON 失敗：保留失敗結論；不產生假的成功 artifact。
- 需要停止：在該次 Actions run 點 **Cancel workflow**。同一分支的新一輪會取消前一輪；不要把取消視為成功。
- 暫停使用：停止手動 dispatch；若要停用憑證，在 GitHub 刪除專用 environment secret。已下載的結果仍應獨立保存。

2026-09-14 核對 [Anthropic Action 固定提交的輸入與輸出](https://github.com/anthropics/claude-code-action/blob/9cdae7f0d995e3ba7c33f226087fdf82a59cd520/action.yml)、[GitHub 手動執行流程](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)及[環境與 secret 設定](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)。正式部署、文章匯入與公開發布不在此 workflow 內。
