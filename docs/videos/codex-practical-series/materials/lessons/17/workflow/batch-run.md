# CLI 一次性批次

node exec-run.mjs --dry-run 只列 argv/schema 與實際 input/from/to，不讀來源、不用模型。可加 --input FILE、--from DATE、--to DATE；預設 fixtures/tasks.json、2026-10-05 到 2026-10-11，日期為包含整天的台北日曆。

node exec-run.mjs --run run-01 會建立全新資料夾，先驗來源與日期，再真正呼叫 codex exec；須先完成登入與額度核對。Windows 若需要可加 --codex NATIVE_CODEX_EXE，不執行 .cmd/.bat wrapper。input 必須位於本課專案內，CLI 不會讀 localStorage。
node verify-result.mjs run-01 對照 input.json/status.json 的实际 input/from/to/timezone/sourceSha256，確認來源未變，再独立計算真值；不相信模型 JSON 的日期或數字。

次週主變式：
node exec-run.mjs --dry-run --from 2026-10-12 --to 2026-10-18
node exec-run.mjs --run run-next-week --from 2026-10-12 --to 2026-10-18
node verify-result.mjs run-next-week
預期 total5/completedInWeek0/pending1/unknownCompleted1。第二條是真模型請求，沒跑須記 NOT RUN；dry-run 和 synthetic 單元測試不能替代它。

缺檔失敗演練（確定性、沒有provider呼叫）：
node exec-run.mjs --run run-missing --input fixtures/missing.json --from 2026-10-12 --to 2026-10-18
預期 exit1，run-missing/status.json state=preflight_failed、modelInvoked=false、errorCode=ENOENT，保留 input/prompt/schema、空 events.jsonl、stderr，沒有 final.json。先確定此檔本來不存在，不刪正常fixture來湊錯誤。恢復後只用新 run ID，舊run拒覆寫。

120秒 timeout、launch_failed、缺 turn.completed、錯數都拒絕；所有真實 events/stderr 保留、不自動重試。模型啟動後的 modelInvoked 表示runner已嘗試呼叫CLI，不等於API成功或完成。synthetic events只在單元測試臨時資料夾，明標非模型證據。
