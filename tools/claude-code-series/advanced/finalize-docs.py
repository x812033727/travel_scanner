"""Create the review index and per-lesson evidence map from existing local receipts."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DOC=ROOT/'docs/claude-code-series/advanced'
plan=json.loads((DOC/'curriculum.json').read_text(encoding='utf-8'))
sources=json.loads((DOC/'evidence/source-checks.json').read_text(encoding='utf-8'))
rows=[]
for entry in plan['entries']:
    number=entry['number']
    rows.append(f"| [{number}．{entry['title']}](../lessons/{number}.md) | {entry['outcome']} | [ZIP](../../../apps/web/public/tutorials/claude-code/advanced/lesson-{number}.zip) |")
groups='\n'.join(f"- [{g['title']}：{g['lab']}](../../../apps/web/public/tutorials/claude-code/advanced/{g['lab']}.zip)" for g in plan['groups'])
routes='\n'.join(f"- **{p['title']}**："+' → '.join(f"[{n}](../lessons/{n}.md)" for n in p['numbers']) for p in plan['paths'])
readme='''# Claude Code 深入教學：第二階段交付

新增 **36 篇完整教學（61–96）、36 份獨立練習包、六組合集**，整合到同一個 Claude Code 教學目錄。全系列現在有 **96 篇教學加 1 個總目錄，共 97 頁**。內容與本機預覽已製作；Claude 帳號及外部環境的實測仍有待辦，狀態見下表。

[第一階段紀錄](../README.md) · [作者任務書](lesson-briefs.md) · [編輯清單](curriculum.json) · [來源與驗證界線](source-review.md) · [本次驗收紀錄](evidence/delivery-checks.json) · [逐篇驗證表](evidence/lesson-verification.json)

本批沿用繁體中文、生活分享、AI／教學主題與原有文章格式。網址沒有加入篇號，舊篇網址保留。正式部署、資料庫匯入與公開發布均未執行。

## 開啟 97 頁預覽

在儲存庫根目錄執行；需要 Node.js 22 以上與已安裝的網站依賴：

```powershell
npm run build:web
node --experimental-strip-types tools/claude-code-series/preview.mjs
```

開啟命令印出的 `/zh-TW/life/claude-code-tutorials` 網址。预覽使用真正的 Next.js 公開呈現元件與本機唯讀資料服務，將全部內容包視為可閱讀，不更動任何資料庫發布狀態。按 Ctrl+C 停止本次預覽；修改內容後重啟，修改網站程式後重新建置。

目錄支援主題、程度、平台和推薦路線，搜尋與篩選保存在網址。每篇包含章節目錄、先備連結、內文交叉引用及上一篇／回目錄／下一篇。新增七條深入路線，原有五條路線保留；公開服務仍依目前語系與發布狀態過濾。

## 36 篇完整內容

下列連結直接開啟文章原稿；網站格式的 `article:` 引用由內容包與公開解析器轉成對應網址，可在上述預覽檢查。一般篇正文約 2,500–2,700 字，綜合實作約 4,000 字，程式碼另計。

| 完整教學 | 學習成果 | 獨立材料 |
|---|---|---|
'''+ '\n'.join(rows)+'''

## 推薦路線

'''+routes+'''

各篇先備知識另列於文章開頭；推薦順序不取代真正的依賴條件。

## 六組合集

'''+groups+'''

每份 lesson ZIP 都有 README、文章、預期結果、停止／重新開始說明、starter 與 reference；fixtures 放在兩個專案裡。使用 Node.js 22 以上，核心測試不需要額外套件。MCP 材料附固定依賴與 lockfile，執行 `npm ci --ignore-scripts` 後可跑整套測試。Agent SDK 在 automation/sdk 另行安裝。

第 85 篇 starter 刻意含錯誤，核心測試預期失敗；reference 與相同回歸測試應通過。第 96 篇 reference 附完整待辦網站。參考檔案不是帳號、手機或外部服務已完成操作的證明。

## 驗證狀態

| 層級 | 證據／限制 |
|---|---|
| 文件核對 | 2026-09-14 核對 19 個官方來源；另核對 GitHub Action 固定提交的輸入契約 |
| 本機程式 | 模型、Skill 參數、Hook 固定事件、實際 MCP stdio、HTTP 假授權、故障與恢復案例；見下載測試紀錄 |
| Git | 在臨時儲存庫建立兩個 worktree、製造並解決衝突、重跑整合測試；沒有修改遠端儲存庫 |
| 網站 | 97 頁、導覽、篩選、手機寬度、原始內容複製、下載版綜合實作；見瀏覽器紀錄 |
| API | SQLite 發布狀態與跨第 60／61 篇導覽測試；未啟用隔離 PostgreSQL 的案例列為 skipped |
| Claude CLI | 2.1.233 實際嘗試 61、67、73、79、91，皆遇 OAuth 到期，未算通過；需重新登入後補測 |
| 外部環境 | 真實 MCP OAuth、手機接續、Agent Teams、外部 GitHub Actions、排程與 SDK 呼叫仍待實測；本機替代材料不取代此項 |
| 發布 | 本批尚未開 PR、合併、部署、匯入或公開 |

[內容檢查](evidence/content-validation.json) · [封面與圖解檢查](evidence/art-validation.json) · [36 包核心測試](evidence/downloads-quick-tests.json) · [六篇試作完整工具測試](evidence/downloads-tests.json) · [瀏覽器結果與重驗紀錄](evidence/browser-verification.json) · [Claude 實測未通過紀錄](evidence/claude-live-all.json)

## 重建與驗收

```powershell
python tools/claude-code-series/advanced/build.py
python tools/claude-code-series/advanced/verify-downloads.py --quick
python tools/claude-code-series/advanced/verify-downloads.py --only 61 67 73 79 88 91
node --test tools/claude-code-series.test.mjs
npx playwright test --config tools/claude-code-series/advanced/playwright.config.mjs
```

首次使用 Playwright 需安裝對應瀏覽器。build.py 只重建本批擁有的 43 組內容／圖片（總目錄、六篇舊文章與 36 篇新文章），不改寫第一階段其他文章或歷史驗收紀錄。第一階段的 validation.json 保留原意；本資料夾的 validation.json 也是先前「課程規劃一致性」紀錄，不能當作本次執行結果。

內容包保持未發布。後續先補真實環境驗證，再依網站既有的預覽、審查、匯入與發布流程逐步記錄結果。
'''
supplement=DOC/'evidence/live/verification-summary.json'
if supplement.exists():
    checked=json.loads(supplement.read_text(encoding='utf-8'))
    api=checked.get('api',{});web=checked.get('web',{})
    if api.get('passed'):
        readme=readme.replace('SQLite 發布狀態與跨第 60／61 篇導覽測試；未啟用隔離 PostgreSQL 的案例列為 skipped',f"隔離 PostgreSQL {api['postgresql_version']} 與 SQLite：{api['tests']} 項通過、{api['skipped']} 項跳過；包含發布狀態、文章版本與系列導覽")
    if web.get('passed'):
        readme=readme.replace('## 驗證狀態',f"## 驗證狀態\n\n補驗：整站前端 {web['files']} 個測試檔、{web['tests']} 項通過。執行環境與原始結果見[補充驗收紀錄](evidence/live/verification-summary.json)；此前未完成的執行保留於歷史紀錄。")
live_path=DOC/'evidence/live/real-operations-summary.json'
live=json.loads(live_path.read_text(encoding='utf-8')) if live_path.exists() else {}
if live.get('cli',{}).get('passed'):
    readme=readme.replace('2.1.233 實際嘗試 61、67、73、79、91，皆遇 OAuth 到期，未算通過；需重新登入後補測','2.1.233 已透過內建瀏覽器重新授權；61、67、73、79、91 的五個主流程全部通過，故障情境另列待辦')
    readme=readme.replace('真實 MCP OAuth、手機接續、Agent Teams、外部 GitHub Actions、排程與 SDK 呼叫仍待實測；本機替代材料不取代此項','真實 MCP OAuth、手機接續、Agent Teams、外部 GitHub Actions、產品排程與完整故障演練仍待實測')
    readme=readme.replace('[Claude 實測未通過紀錄](evidence/claude-live-all.json)','[最新真實操作](evidence/live/real-operations-summary.json) · [首輪 OAuth 失敗歷史](evidence/claude-live-all.json)')
if live.get('sdk',{}).get('passed'):
    readme=readme.replace('| Claude CLI |','| SDK | 0.3.270 的原範例 query、同一 session resume 通過；另用串流输入探針驗證 AbortController 取消。原 runner 的 Ctrl+C 與故障恢復仍待測 |\n| Claude CLI |'.replace('输入','輸入'))
if live.get('web',{}).get('passed'):
    readme=readme.replace('| Claude CLI |','| 雲端網頁 | 使用者指定 travel_scanner，實際 Node.js 計算通過；工具輸出與 No changes to show 均已在內建瀏覽器確認 |\n| Claude CLI |')
if live.get('cli_boundaries',{}).get('passed'):
    readme=readme.replace('| Claude CLI |','| CLI 邊界案例 | 七項通過：子目錄規則、Skill 缺參數／自動選用、Read 權限拒絕、Hook 拒絕 Write、MCP 啟動失敗、只讀子代理。只涵蓋指定案例，不代表各功能所有情境 |\n| Claude CLI |')
if live.get('sdk',{}).get('recovery_passed'):
    readme=readme.replace('原 runner 的 Ctrl+C 與故障恢復仍待測','原 runner 另通過缺少／無效 session、執行檔啟動失敗及全新 query 恢復；實體 Ctrl+C 與中斷 session 恢復仍待測')
if live.get('github_actions',{}).get('local_workflow_prepared'):
    readme=readme.replace('| 發布 |','| GitHub Actions | [儲存庫驗證流程](../../../.github/workflows/claude-tutorial-validation.yml)已備妥；12 項系列測試與 8 項基礎測試通過。尚未合併或遠端執行；[設定與驗證步驟](github-actions-validation.md) |\n| 發布 |')
if live.get('capstone',{}).get('passed'):
    readme=readme.replace('| 發布 |','| 第 96 篇實際開發 | Claude 從 starter 完成篩選、畫面與保存；9 項專案測試、3 項獨立斷言、10 個內建瀏覽器案例、故障紅綠與乾淨解壓重驗通過。[實際成果 ZIP](evidence/live/capstone-result.zip)；一處交接文字由驗收者更正，真實手機仍待測 |\n| 發布 |')
if live.get('sdk',{}).get('terminal_cancel_resume_passed'):
    readme=re.sub(r'\| SDK \|[^\n]+', '| SDK | 0.3.270、runner v2：query、resume、錯誤狀態、啟動恢復、實際終端機 Ctrl+C 取消及同一中斷 session 恢復通過。[紀錄](evidence/live/sdk-terminal-recovery.json) |', readme)
if live.get('teams',{}).get('passed'):
    readme=readme.replace('| 外部環境 |','| 互動式產品 | 兩位 Teams 隊友的讀檔、任務、訊息與後續接續；一次性 Cron 真實觸發及清單清空。[紀錄](evidence/live/interactive-products.json)。僅驗證所列範圍，未宣稱完整雙角色功能開發 |\n| 外部環境 |')
    readme=re.sub(r'\| 外部環境 \|[^\n]+','| 外部環境 | 真實手機、遠端 MCP OAuth、Bash sandbox 與 Actions 模型 job 尚未通過；Remote Control 瀏覽器要求裝置重新驗證。完整待辦見最新操作紀錄 |',readme)
if live.get('extra_boundaries',{}).get('passed'):
    readme=readme.replace('| CLI 邊界案例 | 七項通過：','| CLI 邊界案例 | 另六項涵蓋規則衝突、Skill 材料與缺檔、Hook 程式失敗、MCP 不可信輸出及無效參數；原七項通過：')
if live.get('workflow_comparison',{}).get('passed'):
    readme+='\n[單代理／Teams 流程觀察](evidence/live/workflow-observations.json)：各一次、相同合成輸入，保存版本、模型與計時。模型組合與協調流程不同，不據此宣稱效能排名或節省費用。\n'
readme=readme.replace('補驗：整站前端','較早來源快照的本機補驗：整站前端').replace('2,500–2,700','2,500–2,800')
if (DOC/'evidence/live/post-main-checks.json').exists():
    readme=readme.replace('## 驗證狀態\n','## 驗證狀態\n\n同步 main 後，Node.js 24.15.0 的建置、lint、i18n、型別、52 項工具測試、Ruff 與 mypy 通過；9 類瀏覽器案例重跑通過。相關前端共 73 項斷言通過：第一輪有工作程序逾時，缺少的 23 項以 forks 單獨補跑。API 本次 18 通過、12 項 PostgreSQL 跳過，完整資料庫紀錄屬較早快照。[目前檢查與失敗重試紀錄](evidence/live/post-main-checks.json)。\n')
readme=readme.replace('需要 Node.js 22 以上與已安裝的網站依賴','需要符合儲存庫依賴的 Node.js 版本與已安裝的網站依賴（本次使用 24.15.0）')
release_path=DOC/'evidence/live/release-state.json'
if release_path.exists():
    release=json.loads(release_path.read_text(encoding='utf-8'))
    pr=release['pull_request']
    state=f'[PR #{pr["number"]}]({pr["url"]})：'+('已合併' if pr['merged'] else '審查中')
    readme=re.sub(r'\| 發布 \|[^\n]+',f'| 發布 | {state}；正式部署、資料庫匯入與公開發布未執行 |',readme)
    actions=release.get('baseline_workflow')
    if actions:
        readme=re.sub(r'\| GitHub Actions \|[^\n]+',f'| GitHub Actions | [基礎工作流程]({actions["url"]})：{actions["conclusion"]}，run_model=false；模型 job 未執行，不能當作模型審查通過。詳見[執行與設定](github-actions-validation.md) |',readme)
if live.get('teams_feature',{}).get('passed'):
    readme=readme.replace('僅驗證所列範圍，未宣稱完整雙角色功能開發','另完成第 89 篇雙角色功能、阻塞回報、契約決策、文案變更及最終測試／瀏覽器驗收，見 [Teams 完整實作](evidence/live/team-feature-validation.json)')
readme=readme.replace('Claude 帳號及外部環境的實測仍有待辦','部分裝置及外部環境實測仍有待辦')
if live.get('sandbox',{}).get('passed'):
    readme=readme.replace('、Bash sandbox 與 Actions','與 Actions')
    readme=readme.replace('| 外部環境 |','| Bash sandbox | WSL2／CLI 2.1.270：專案內讀寫、指定路徑讀取拒絕、專案外寫入拒絕、主機 loopback 隔離通過；HTTP 在主機前後皆可連線。[紀錄](evidence/live/sandbox-validation.json)。未驗證所有網域規則或 Unix socket |\n| 外部環境 |')
if (DOC/'evidence/live/final-ci-summary.json').exists():
    readme=readme.replace('## 驗證狀態\n','## 驗證狀態\n\n**PR 合併前的最終 CI：** 14 個工作全部成功。Linux Web 為 258 檔／2,809 項測試，另有 497 項瀏覽器測試；API 為 4,182 通過／16 跳過，Ruff、mypy 及必要整站檢查通過。[CI 紀錄與適用提交](evidence/live/final-ci-summary.json)。下列本機與歷史結果分別保留。\n')
(DOC/'README.md').write_text(readme.replace('预覽','預覽'),encoding='utf-8')
brief=DOC/'lesson-briefs.md'
text=brief.read_text(encoding='utf-8')
text=text.replace('以下是課程規劃，不是已完成或已公開的文章。每個章節編號均可直接連結；先備篇連至既有本機原稿。未來站內連結一律經發布狀態解析，不直接把下列預定網址公開。','以下保留原課程設計與验收目標；36 篇正文與練習包已製作，請由各章的「完整原稿」或總目錄開啟。實際測試狀態以交付紀錄為準，未將預覽稿公開發布。'.replace('验收','驗收'))
for entry in plan['entries']:
    heading=f"### {entry['number']}．{entry['title']}"
    link=f"[完整原稿](../lessons/{entry['number']}.md)"
    if link not in text:text=text.replace(heading,heading+'\n\n'+link)
brief.write_text(text,encoding='utf-8')
source_table='\n'.join(f"| [{s['title']}]({s['url']}) | {s['checked_on']} | 文件核對 |" for s in sources)
(DOC/'source-review.md').write_text('''# 官方來源與驗證界線

[回第二階段總目錄](README.md)

製作時重新取得以下 19 個官方來源，保存日期、頁名、網址、狀態及 SHA-256；完整頁面僅作本機查閱，不附入教材。此清單是文件核對，不能證明真實帳號的操作成功。

| 官方來源 | 核對日期 | 證據類型 |
|---|---|---|
'''+source_table+'''

另核對 [GitHub Action 的固定提交與輸入契約](https://github.com/anthropics/claude-code-action/blob/9cdae7f0d995e3ba7c33f226087fdf82a59cd520/action.yml)，確認 structured_output、show_full_output、display_report 等欄位。範例是手動觸發、預設分支、固定假 diff 的實驗；不宣稱外部 CI 已跑過。

MCP 材料固定 @modelcontextprotocol/client、@modelcontextprotocol/server 2.0.0 與 zod 4.6.5，附 lockfile 並執行實際 stdio 工具呼叫。Agent SDK 固定 0.3.270；狀態解析測試與真正模型呼叫分開。CLI 曾以 2.1.233 嘗試五個主要流程，OAuth 到期，因此這些流程尚未實測通過。

## 撰稿時採用的範圍

- CLAUDE.md 提供指引，settings／權限控制行為；AGENTS.md 透過 CLAUDE.md 引用。
- Skill allowed-tools 用於預先授權，不能把它單獨描述成全面工具禁止清單。
- Hook 的 Write／Edit 路徑保護不覆蓋所有 shell 或外部操作；Stop 設計有重複事件的停止條件。
- 原生 Windows 的權限練習和支援平台的 Bash sandbox 分開。
- 本機 HTTP 假服務只能示範狀態碼，沒有實作或驗證完整遠端 MCP OAuth。
- Agent Teams 採文件當日的實驗功能與自然語言分工方式；Worktree 替代練習通過不表示 Teams 已使用。
- 手機篇區分本機 Remote Control、雲端工作與 Dispatch；資格、連線與休眠在讀者實際入口確認。
- CLI JSON 外層執行結果與內層結構資料分開驗證；故障輸出不能當成空結果成功。
- 排程結果、每次嘗試、取消與去重各自留證；本機去重不承諾外部副作用必定只執行一次。
- 比較資料為明示的合成案例，沒有把範例數字當成模型排名或真實費用。

## 發布前仍需補做

重新登入 Claude 後，先跑 61、67、73、79、91 的主流程及故障演練，再依逐篇驗證表完成其餘模型操作。第 81 篇需真正遠端服務授權，第 90 篇需手機與電腦，第 92 篇需測試儲存庫外部執行，第 94 篇需 SDK 呼叫與工作階段恢復。記錄環境、版本、輸入、輸出、退出碼和停止方式；不保存憑證。

每個結果標示「官方文件核對」「本機程式／固定事件」「Claude 實際操作」「真實裝置／服務」其中一種。未測項目保持待測，預覽、PR 合併、部署、匯入及公開狀態分開記錄。
''',encoding='utf-8')
base=ROOT/'docs/claude-code-series/README.md'
if live.get('cli',{}).get('passed'):
    source_path=DOC/'source-review.md'
    source_text=source_path.read_text(encoding='utf-8')
    source_text=source_text.replace('CLI 曾以 2.1.233 嘗試五個主要流程，OAuth 到期，因此這些流程尚未實測通過。','CLI 2.1.233 首輪因 OAuth 到期失敗，之後已使用內建瀏覽器重新授權，61、67、73、79、91 五個主流程全部通過；兩輪紀錄分開保存。')
    source_text=source_text.replace('重新登入 Claude 後，先跑 61、67、73、79、91 的主流程及故障演練，再依逐篇驗證表完成其餘模型操作。第 81 篇需真正遠端服務授權，第 90 篇需手機與電腦，第 92 篇需測試儲存庫外部執行，第 94 篇需 SDK 呼叫與工作階段恢復。','五篇 CLI 主流程與網頁雲端工作已通過，SDK 原範例 query／resume 與另建串流取消探針通過；故障演練、權限情境、Skill 自動選用、多代理與完整實作仍依逐篇表補齊。第 81 篇需真正遠端服務授權，第 90 篇需手機與電腦，第 92 篇已指定 travel_scanner，但仍缺 claude-lab 環境與 Anthropic CI 憑證；第 94 篇原 runner 的 Ctrl+C 與故障恢復仍待測。')
    source_text+='\n補充核對：[SDK Streaming Input](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)（2026-09-14）。取消探針採串流輸入，確認開始收到文字後呼叫 AbortController，沒有完整成功結果。早期單次輸入探針的競態／普通成功回覆不算取消通過，原始嘗試均保留於 evidence/live/。\n'
    if live.get('cli_boundaries',{}).get('passed'):
        source_text=source_text.replace('故障演練、權限情境、Skill 自動選用、多代理與完整實作仍依逐篇表補齊','另通過七個 CLI 邊界案例，包含 Read 權限、Hook 寫入拒絕、Skill 自動選用、MCP 啟動失敗及只讀子代理。其餘故障、Bash sandbox、Agent Teams 與完整實作仍依逐篇表補齊')
        source_text+='\nHook 初測先被 Write 的讀檔前提拒絕，不能算 Hook 成功；更正後先 Read，再確認 Hook 回傳 protected fixture directory 且檔案未改變。子代理初測超時，後續使用 Haiku 在 33.84 秒完成一次只讀審查；保留初次失敗與模型差異，不能將其當作模型比較結果。\n'
    if live.get('sdk',{}).get('recovery_passed'):
        source_text=source_text.replace('第 94 篇原 runner 的 Ctrl+C 與故障恢復仍待測','第 94 篇原 runner 已補測缺少／無效 session、執行檔啟動失敗與重新建立 query；實體 Ctrl+C 與中斷 session 恢復仍待測')
    if live.get('capstone',{}).get('passed'):
        source_text=source_text.replace('其餘故障、Bash sandbox、Agent Teams 與完整實作仍依逐篇表補齊','其餘故障、Bash sandbox、Agent Teams 與真實比較仍依逐篇表補齊')
        source_text+='\n第 96 篇另完成實際 Claude 開發驗證：Sonnet 從 starter 製作篩選、畫面與保存；指定比較符號故障由 Haiku 修正，同一組獨立斷言先紅後綠。內建瀏覽器驗證 10 個指定案例，另從實際成果 ZIP 乾淨解壓縮重驗。驗收者更正原 handoff 對部分無效資料處理的一句說明；完整原始模型輸出保留，不把驗收者的修正歸因給模型。尺寸模擬不代表真實手機。\n'
    if live.get('sdk',{}).get('terminal_cancel_resume_passed'):
        source_text=source_text.replace('實體 Ctrl+C 與中斷 session 恢復仍待測','runner v2 已用串流輸入完成終端機 Ctrl+C 取消，且同一中斷 session 恢復通過；輸入由驗收工具送進真實 PTY，不宣稱真人按鍵')
    if live.get('teams',{}).get('passed'):
        source_text=source_text.replace('其餘故障、Bash sandbox、Agent Teams 與真實比較仍依逐篇表補齊','已另驗證兩位具名 Teams 隊友、任務與訊息、一次性 Cron 觸發及一組流程觀察；完整 UI 團隊整合與 Bash sandbox 仍未通過')
    source_text=source_text.replace('仍缺 claude-lab 環境與 Anthropic CI 憑證','claude-lab 已建立並限制 main，仍缺 Anthropic CI 憑證')
    if live.get('extra_boundaries',{}).get('passed'):
        source_text+='\n補驗六項：規則衝突、Skill 資料材料選用／缺檔、Hook 執行失敗、真正 MCP 不可信輸出與無效參數。手動輸入斜線 Skill 會直接展開，不以缺少另一筆 Skill 工具呼叫判成失敗；判讀修正與原始結果均保留。\n'
    if live.get('teams_feature',{}).get('passed'):
        source_text=source_text.replace('完整 UI 團隊整合與 Bash sandbox 仍未通過','第 89 篇雙角色功能整合已另補測通過；Bash sandbox 仍未通過')
    if live.get('headless_boundary',{}).get('passed'):
        source_text+='\nCLI 自動更新後，另以 2.1.270 驗證一回合上限：真實 -p 執行退出 1，回傳 error_max_turns/is_error=true；保持錯誤結果，未當成空白成功。新舊版本的結果分開保存。\n'
    if live.get('sandbox',{}).get('passed'):
        source_text=source_text.replace('Bash sandbox 仍未通過','WSL2 Bash sandbox 的指定檔案及主機 loopback 案例已通過')
        source_text+='\n沙箱补驗（2026-09-14）：使用官方 Linux CLI 2.1.270、bubblewrap 與 socat，保留 failIfUnavailable／禁止沙箱外重試。實際 Bash 顯示 Permission denied 與 Read-only file system，外部檔案保持原樣。HTTP 主機前後控制均成功，沙箱內 Connection refused；不採信模型自行歸因為網域代理，也不宣稱 Unix socket 或所有外連規則通過。原始工具結果見 sandbox-events.json。\n'.replace('补驗','補驗')
    if release_path.exists() and release.get('pull_request',{}).get('merged'):
        source_text+='\n合併後狀態：PR #501 已合併，適用提交與 14 個成功 CI 工作見 evidence/live/release-state.json。手動 GitHub Actions baseline 成功，model-review 依 run_model=false 跳過；付費模型審查、真實手機與遠端 MCP OAuth 尚未完成。先前「待合併／未遠端執行」敘述為歷史紀錄。\n'
    source_path.write_text(source_text,encoding='utf-8')
text=base.read_text(encoding='utf-8')
notice='> 第二階段已新增 36 篇，現在可預覽 97 頁；請見[深入教學交付目錄](advanced/README.md)。下列 60／61 篇與驗證數量保留第一階段的歷史紀錄。\n\n'
if notice not in text:text=text.replace('\n\n','\n\n'+notice,1)
base.write_text(text,encoding='utf-8')
