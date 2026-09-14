---
id: 2026-09-14-claude-advanced-live-validation
title: Claude Code 進階：補齊真實環境驗證
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T12:32:44Z
completed_at:
branch: codex/claude-code-advanced-tutorials
depends_on: []
scope:
  - docs/claude-code-series/advanced/evidence/live
---

# Claude Code 進階：補齊真實環境驗證

## Why

36 篇文章與 97 頁本機預覽已完成，檔案及固定事件測試通過。CLI 到期登入已透過內建瀏覽器排除，五篇主流程、七個 CLI 邊界案例、SDK 與第 96 篇本機實作已取得真實證據；其餘裝置、外部服務與故障範圍仍需補齊。

## Definition of done

- [x] 使用內建瀏覽器完成 CLI 重新授權，61、67、73、79、91 五個主流程全部通過
- [x] 五篇各有實際故障／邊界案例（規則衝突、缺參數、Hook 失敗、MCP 失敗、CLI 回合上限），只宣稱所列情境
- [x] 子目錄規則、Read 拒絕、Skill 缺參數／自動選用、Hook Write 拒絕、MCP 啟動失敗、只讀子代理七個案例通過
- [x] 規則衝突、Skill 附屬材料／缺檔、Hook 故障、MCP 無效參數及不可信輸出
- [x] 互動式 Teams：兩位具名隊友、任務分派、訊息回覆與後續訊息接續
- [x] 第 89 篇完整雙角色功能整合、受控阻塞／決策、文案更新、10 項專案與 3 項獨立斷言、內建瀏覽器驗收
- [x] 支援平台 Bash sandbox：WSL2 的指定檔案與主機 loopback 案例（不宣稱所有網域或 Unix socket）
- [ ] 第 81 篇取得測試 MCP HTTP／OAuth 服務，完成授權、操作、撤銷與恢復
- [ ] 第 90 篇在真實手機與電腦完成接續、斷線、休眠及恢復測試
- [ ] 第 92 篇在明確授權的測試儲存庫執行 GitHub Actions，保存 run URL、輸入與產物；不在正式儲存庫任意觸發
- [x] 第 93 篇完成產品一次性排程；第 94 篇修正 runner 串流輸入後，實際終端機 Ctrl+C 與中斷 session 恢復
- [x] 第 94 篇原 runner 補測缺少／無效狀態、啟動失敗與全新 query 恢復
- [x] 第 94 篇原 SDK runner 的 query、同 session resume 通過；另建串流輸入探針實測 AbortController 取消
- [x] 第 95 篇加入明示版本的真實流程觀察：每種一次，模型與協調成本不同，不宣稱效能優劣
- [x] 第 96 篇實際 Claude 開發、獨立斷言、瀏覽器、指定故障修復及乾淨解壓重驗
- [ ] 發布前重查高變動功能與來源日期
- [x] 完成 PR 所需完整前端測試：Windows 258 檔、2,809 項全部通過
- [x] 完成隔離 PostgreSQL 檢查：164 passed、0 skipped，測試 schema 清空且資料庫已停止
- [x] 在使用者指定的 travel_scanner 建立網頁雲端驗證，核對真實 Node.js 工具輸出及 No changes to show

## How to verify

先閱讀 docs/claude-code-series/advanced/README.md 與 evidence/lesson-verification.json。
五篇 CLI 驗證工具：tools/claude-code-series/advanced/verify_live.py。原始失敗紀錄在 evidence/claude-live-all.json。
新的實機紀錄保存到本任務 scope 的 evidence/live/，包含版本、OS、材料 SHA、實際輸入／結果、退出碼、停止方式與未驗證項目，不保存憑證。若需要修改正文或程式，另認領對應窄範圍任務。

## Notes

- 已通過：97 頁內容檢查、36 包共 81 個命令檢查、六篇各 21 個工具測試、9 類瀏覽器驗收、73 個相關前端測試、51 個工具測試，build/lint/typecheck/i18n/Ruff/mypy。
- API：87 passed / 77 skipped；跳過的是尚未啟用隔離 PostgreSQL 的案例。整站 258 檔前端測試曾啟動，為收尾已停止，未得到完整結果；不能引用為整站通過。
- 本機 HTTP 模擬、固定 Hook 事件、工作階段狀態解析與 Worktree 替代練習，都不取代真實帳號／裝置實測。
- 目前沒有第二階段 PR、合併、部署、資料庫匯入或公開發布。此任務是未完成實測清單，不代表自動取得發布授權。
- 主工作已請使用者重新登入；未收到回覆前不要無限重試相同 OAuth 失敗。

2026-09-14 補驗：使用官方 PostgreSQL 17.11 Windows 二進位套件，在臨時目錄建立僅綁定 127.0.0.1 的獨立資料庫，執行文章／系列測試得到 164 passed、0 skipped；測試 schema 為 0，pg_ctl stop 成功。原始紀錄在 evidence/live/postgres-validation.json、postgres-tests.xml。後續暫存目錄清理被自動核准審查拒絕（blocked by policy），資料庫已停止，剩餘檔案保留。

完整前端補驗已完成：Windows Vitest 258 檔、2,809 項通過，退出碼 0；原始 JSON 為 evidence/live/web-full.json。WSL 使用相同 2,761 檔來源快照與 lockfile 啟動備援測試；Windows 全套完成後停止重複執行，退出 143，不宣稱 Linux 全套通過。新摘要為 evidence/live/verification-summary.json，先前 87 passed／77 skipped 與未完成全套的紀錄保留為歷史。Claude 憑證仍待使用者重新登入，不重試同一個到期 OAuth 工作流程。

2026-09-14 13:20 UTC 後續：使用者要求使用內建瀏覽器，已透過官方 OAuth 完成既有 CLI 重新授權，auth status 為 loggedIn=true。上段登入阻塞已排除。61、67、73、79、91 主流程全部通過；第 73 篇保存真實 PostToolUse/Read 事件。SDK 0.3.270 的 query、resume 與獨立串流取消探針通過，兩次不足以證明取消的初期嘗試保留，不計入成功。

使用者已指定 https://github.com/x812033727/travel_scanner 作為網頁版與 GitHub Actions 實測儲存庫。網頁工作「Mokaair 合成資料計算驗證」已完成，工具輸出為 total=3、completed=1、pendingIds=[b,c]；Changes 顯示 No changes to show，沒有對應遠端分支或 PR。Actions 預檢查得 repository secrets=0、environments=0，仍缺範例的 ANTHROPIC_API_KEY／claude-lab；沒有將本機登入憑證移交 GitHub。

最新資料：evidence/live/real-operations-summary.json、browser-validation.json、claude-live-all.json、sdk-query-resume.json、sdk-cancel.json。瀏覽器實測不取代真實手機／休眠／Remote Control 測試。後續不需要再次要求使用者登入，除非新的 auth status 或操作證據顯示登入失效。

2026-09-14 後續：七個 CLI 邊界案例最終全部通過。Hook 初測先遇 Write 讀檔前提、不能歸因 Hook；先 Read 後重驗確認 protected fixture directory 且檔案未改變。子代理首輪 100 秒超時；Haiku 重驗在 33.84 秒完成一次只讀審查。失敗與更正保留於 cli-boundaries-first-attempt.json。

SDK 原 runner 四種狀態／啟動案例通過（sdk-recovery.json）。第 96 篇由 Sonnet 從 starter 完成篩選、畫面與保存，9 項專案測試、3 項獨立斷言、10 項內建瀏覽器案例通過。指定故障由 Haiku 修正，相同斷言先紅後綠；capstone-result.zip 在乾淨目錄重驗通過。驗收者修正 handoff 一句部分無效資料的說明，原始模型輸出保留。臨時伺服器已停止。

GitHub 專用 workflow 已在 .github/workflows/claude-tutorial-validation.yml 準備，由 claude-tutorial-ci-validation 任務管理，預設只做 baseline；尚未合併／dispatch，仍需 claude-lab 與專用 ANTHROPIC_API_KEY。相關系列測試 12 項、workflow baseline 8 項及工具全套 52 項通過。最新審查包含 380 個檔案；425 個文件連結無失效。資料與動作紀錄在 real-operations-summary.json、ci-workflow-validation.json 及 capstone-*.json。

2026-09-14 收尾補驗：六個額外 CLI 案例通過，見 extra-boundaries.json。手動斜線指令直接展開，初次誤要求另一個 Skill 工具事件的判準已更正，原始失敗判讀保留。

SDK runner v2 已改為串流輸入，真實 PTY 在首段輸出後送出 Ctrl+C，29.418 秒內保存 cancelled；同一 session 隨後正確回覆先前標記。query/resume 與四種失敗／恢復重驗皆通過。此為工具送入實際終端機的按鍵，不宣稱真人鍵盤。

兩位具名 Teams 隊友讀檔、任務與訊息完成；lead 曾把隊友錯叫普通 subagent，也重複完成已由隊友結束的任務，原始 trace 和判讀更正保留。一次性 Cron 在 22:06 Asia/Taipei 實際觸發，回覆 total=3/completed=1，後續 CronList 清空；工作階段正常退出。各一次單代理與 Teams 流程觀察已保存，不能據此當成模型排名。

目前外部阻塞：claude-lab 已建立並限制 main，但沒有 ANTHROPIC_API_KEY；真實手機未提供；真實遠端 MCP OAuth 服務未提供。Remote Control 本機已啟動，瀏覽器可見歷史，但要求 device_key_missing 的裝置重新驗證，Google 登入沒有跳轉，未送出遠端操作。WSL 設定期間連唯讀 process list 也無回應，僅停止本次 Windows WSL 客戶端，未 shutdown 共用 WSL；安裝結果未知，不算 sandbox 通過。

主分支已同步至 8c83e90a，先前全套前端／PostgreSQL 證據保留為歷史快照；本次採用官方 SHA 驗證的 Node 24.15.0 更新依賴並重驗，CI／PR 狀態另記。正式部署、匯入和公開均未執行。

2026-09-14 PR #501 已建立，完成 Teams 功能實作與 CLI error_max_turns 補驗，版本因自動更新為 2.1.270；較早 2.1.233 結果保留。Teams 同兩位角色依範圍修改，實際回報阻塞後更新未知 mode 契約及指定文案。10 項專案測試、3 項獨立斷言及內建瀏覽器功能／360px 畫面通過，工作階段和測試伺服器已停止；見 team-feature-validation.json。

CI 找到 Windows 封裝 CRLF 與 Linux Git 原稿 LF 的差異；已修正產生器為文字 LF，保留二進位內容，重新製作 42 ZIP 並補回歸驗證。這是封裝一致性修正，真實 Teams 原始 starter 與新版 starter 經換行正規化完全一致。CI 尚待最終提交完成，不能把初版 web 失敗算通過。

2026-09-14 WSL2 已恢復回應，官方 Linux CLI 2.1.270 安裝與既有帳號登入完成，bubblewrap/socat 可用。實際 Bash 五個命令驗證專案內讀寫、指定路徑 Permission denied、專案外 Read-only file system，外部檔案仍為 UNCHANGED。主機 HTTP 前後控制皆成功、沙箱內 Connection refused；模型的代理歸因不作證據。保持 failIfUnavailable 與禁止沙箱外重試，伺服器與驗證工作已停止。見 sandbox-validation.json、sandbox-events.json；先前 WSL 阻塞是歷史狀態。
