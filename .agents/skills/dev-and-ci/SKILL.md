---
name: dev-and-ci
description: travel_scanner 的本機開發與 CI 檢查：Windows 上的環境（每個 worktree 根目錄 npm ci、API 用 uv sync 或 venv、POSIX 測試進 WSL、fakeredis 重現 Redis 問題、Bash heredoc 與編碼的坑），API 的 ruff／mypy／pytest 與 web 的 lint／typecheck／vitest 怎麼跑、怎麼正確讀 exit code，CI 紅燈分診與已知 flake（映像拉取 125、keep-alive ECONNRESET、site-pages disposed、passive effect 空檔、cgr.dev 的 403），Playwright 手機 viewport 被撐寬、CLS 量測，以及每週 Dependabot PR 怎麼判斷。i18n 鍵與寫 e2e 走 web-i18n-e2e，合併流程走 task-board，部署走 deploy，主機維運走 prod-host-ops，後端寫法走 backend-conventions，這裡不重講。要在本機跑檢查、推 PR 前驗證、查 CI 為什麼紅、判斷是不是 flake、量版面或 CLS、審 Dependabot PR 時，先讀這個 skill。Run and read the local and CI checks on Windows, triage red CI and known flakes, and judge weekly Dependabot pull requests.
metadata:
  short-description: 本機檢查、CI 分診、已知 flake、Dependabot
---

# 本機開發與 CI（dev-and-ci）

> 本文提到的 `references/…`、`scripts/…` 都在 `.agents/skills/dev-and-ci/` 底下；`.claude/skills/dev-and-ci/` 只放這份 SKILL.md 的逐字複本。

這個 skill 只放指令、判斷順序、去哪裡讀。CI 真正跑什麼以 `.github/workflows/ci.yml` 為準；推 PR 前的清單在 `AGENTS.md` §Checks before you push；四個必要檢查與怎麼讀在 `.github/BRANCH_PROTECTION.md`。合併、rebase、BEHIND 走 skill `task-board`。

## 不變的規矩

1. **exit code 才算數，不是輸出的最後幾行。** Bash 工具沒有 `pipefail`，`cmd | tail` 的狀態是 `tail` 的，lint 與 typecheck 曾在本機「通過」、CI 紅。每個檢查寫進 log、印 `exit=$?`，再 grep log；背景指令讀完整個 log。用 `scripts/run-checks.sh`。
2. **每個 worktree 自己 `npm ci`（在 repo 根目錄）。** 沒裝時 tsc／eslint／vitest 會往上找到主 checkout 的 `node_modules`，版本可能落後好幾個大版本，於是「本機紅、CI 綠」或反過來，失敗訊息不會提到版本。相信本機紅燈前先比對版本（`references/local-env.md`）。
3. **本機全綠不等於 CI 綠。** 本機沒有 PostgreSQL／Redis，`RUN_INTEGRATION_TESTS=1` 的測試全部 skip；e2e 要的 chromium build 本機可能沒有。只有 CI 驗得到的，推之前先想清楚，一輪 CI 約 15–18 分鐘。
4. **含非 ASCII、反斜線、引號、反引號的腳本或檔案編輯，用 Write 工具寫進 scratchpad 再執行。** Bash 的 heredoc 會改寫它們，`perl -pi`／`sed -i` 會把中文寫壞。新檔 commit 後看 `git show --stat`，出現 `Bin` 就是寫進了 NUL。
5. **紅燈先分類再動手**：環境（重跑）、已知 flake（對照表）、自己的錯（修）。一個「單獨跑永遠過」的 web 測試在負載下紅，先想 passive effect 空檔，不要加 `waitFor` 或 timeout 掩蓋。
6. **量到完美的數字先證明儀器量得到不完美的**：CLS 0、scrollWidth 等於 innerWidth，都可能是量法根本不可能給別的答案。

## 主幹

| # | 階段 | 做什麼 | 關卡 |
| --- | --- | --- | --- |
| 1 | 準備 | worktree 根目錄 `npm ci`；`apps/api` 裡 `uv sync --frozen` | `node_modules` 與 `.venv` 都在這個 worktree 裡 |
| 2 | 跑檢查 | 只跑你動到的那幾組：`bash .agents/skills/dev-and-ci/scripts/run-checks.sh web api tools` | 每組都印 `exit=0`；失敗就讀那個 log |
| 3 | 推、等 CI | 推之後照 `task-board` 讀四個必要檢查 | `api`、`web`、`containers`、`full-stack-smoke` 都 `completed success` |
| 4 | 紅了 | 存完整 job log、比對 `references/ci-triage.md` 的表 | 分出環境／flake／自己的錯；flake 才重跑 |
| 5 | 修 flake | 寫一個確定會紅的測試再修（helper 見 ci-triage） | 換回舊程式紅、修正版綠 |

## 指令

```bash
# 準備（每個新 worktree 一次；背景跑時 log 目錄要先存在）
npm ci
(cd apps/api && uv sync --frozen)

# 檢查：每組寫 log、印 exit code、最後彙總
bash .agents/skills/dev-and-ci/scripts/run-checks.sh web      # lint:web、check:i18n、typecheck:web、test:web
bash .agents/skills/dev-and-ci/scripts/run-checks.sh api      # ruff、mypy app、mypy tests、pytest
bash .agents/skills/dev-and-ci/scripts/run-checks.sh tools    # test:tools、check:tasks
CHECK_LOG_DIR=/tmp/checks bash .agents/skills/dev-and-ci/scripts/run-checks.sh web api

# 單一檔案
(cd apps/web && npx vitest run components/route-mode-panel.test.tsx)
(cd apps/api && uv run pytest tests/test_x.py -q)
(cd apps/web && npx playwright test e2e/navigation.spec.ts --project=desktop-chromium)

# 手動跑一個檢查的正確寫法
npm run typecheck:web > "$LOG" 2>&1; echo "exit=$?"; grep -n "error" "$LOG" | head

# CI：讀失敗的 job log（run 還在跑時 --log-failed 拿不到東西）
gh api --allow-escape-sequences "repos/{owner}/{repo}/actions/jobs/<job-id>/logs" | sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g' > job.log
gh api "repos/{owner}/{repo}/check-runs/<job-id>/annotations"   # vitest 失敗立刻可讀
gh run rerun <run-id> --failed                                   # 整個 run 結束後才能用
```

`--allow-escape-sequences` 是 `gh api` 的旗標，`gh run view --log` 沒有；不加的話 gh 拒絕印出含跳脫序列的 log。這台機器的 Bash 沒有 `jq`，而且在管線裡是靜默失敗（變數變空字串、判斷式反而成立）；剖 JSON 用 `gh ... -q '<運算式>'`（gh 內建 jq）或 Python。

## CI 跑什麼（與本機的差別）

| job | 內容 | 本機做不到的部分 |
| --- | --- | --- |
| `api` | `uv sync --frozen`、ruff、`mypy app`、`mypy tests`、migration 單一 head、PostgreSQL 升級驗證、`pytest --cov=app`（帶 `RUN_INTEGRATION_TESTS=1`、真的 Postgres 17／Redis 7.4／MinIO） | 整合測試 |
| `web` | `npm ci`、lint、`check:i18n`、`check:tasks`、typecheck、vitest、`test:tools`、`build:web`、隔離的 Playwright 清單 | e2e（chromium build） |
| `containers` | compose config、build、nginx 設定驗證、prod compose、SHA 映像 | 全部 |
| `full-stack-smoke` | 真的 API＋worker＋`next start`，桌面與 Pixel 7 旅程、社群、後台矩陣 | 全部 |

PR 只跑 `pull_request` 事件（`push` 只在 main），同一個 PR 的新 push 會取消舊 run；被取消的 run 不是紅燈。`npm audit`／`pip-audit` 在 ci.yml 裡是 advisory。

## 去哪裡讀

| 問題 | 讀 |
| --- | --- |
| Windows 環境、worktree、venv、WSL、fakeredis、Bash 與編碼的坑、內建瀏覽器的假象 | `.agents/skills/dev-and-ci/references/local-env.md` |
| 每個檢查的指令、本機與 CI 的差、會騙人的綠燈 | `.agents/skills/dev-and-ci/references/checks.md` |
| CI 紅燈分診、已知 flake 對照、passive effect 空檔與它的重現 helper | `.agents/skills/dev-and-ci/references/ci-triage.md` |
| Playwright 手機點擊落空、CLS 量測 | `.agents/skills/dev-and-ci/references/browser-measurement.md` |
| 每週 Dependabot PR 怎麼判斷、被擋住的大版本 | `.agents/skills/dev-and-ci/references/dependabot.md` |
| 合併、rebase、BEHIND／DIRTY | skill `task-board` |
| i18n 鍵、寫 e2e spec | skill `web-i18n-e2e` |
| migration、Redis／session helper 的寫法 | skill `backend-conventions` |

## 這個 skill 的檔案

- `scripts/run-checks.sh`：依組別跑檢查，每個檢查一個 log，印 exit code 與彙總，有任何失敗就非零結束。
- `references/*.md`：上表五份。
- `.claude/skills/dev-and-ci/SKILL.md` 是這一份的逐字複本，`npm run test:tools` 會比對；references 與 scripts 只放在 `.agents/` 這一份。
