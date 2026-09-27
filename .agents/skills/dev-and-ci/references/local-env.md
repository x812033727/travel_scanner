# Windows 上的本機環境

這裡的每一條都是在 Windows 11（ARM64）＋ Git Bash 的 Claude Code／Codex 環境踩過的。Linux／macOS 上大多不會發生，但規則照樣無害。

## Node 與 web

- `apps/web` 是 npm workspace，**lock 檔只有根目錄的 `package-lock.json`**，`npm ci` 要在 repo 根目錄跑，裝進根目錄的 `node_modules`（`apps/web` 底下沒有自己的 `node_modules` 是正常的，除非 lock 把某個版本放進去，見 dependabot.md 的 TypeScript 兩套並存）。
- **worktree 沒裝 `node_modules` 時，tsc／eslint／vitest 會往上找到主 checkout 的 `node_modules`**，而它可能落後好幾個大版本。實例：主 checkout 的 vitest 4.1.11，lock 已是 5；某個 `it.each` 共用一個 `vi.fn()` 的測試在 4 紅、在 5 綠，失敗訊息完全沒提版本。另一例：eslint／vitest 都「過」，只有 tsc 報 `Cannot find module 'qrcode'`。相信本機紅燈前先比對：

  ```bash
  node -p "require('./node_modules/vitest/package.json').version"
  grep -A2 '"node_modules/vitest"' package-lock.json
  ```

  eslint、typescript 同理。不一致就在 worktree 根目錄 `npm ci`（快取熱的話約 50 秒）。
- `next dev`（Turbopack）拒絕解析 workspace 根目錄以外的 `next`，所以 worktree 沒 `npm ci` 就起不了 dev server。
- Next 16 一個專案目錄只允許一個 `next dev`（鎖在 `.next/dev`）：跑 e2e 前先關掉自己在同一個 worktree 起的 dev server，否則 Playwright 的 webServer 起不來。
- rebase 搬動過 route 檔之後，跑過 `next dev` 的 worktree 會在 typecheck 報 `TS2307 Cannot find module '../../../app/[locale]/.../page.js'`，來源是 `.next/dev/types/validator.ts`。那是 git 忽略的舊產物，不是程式錯：在 `apps/web` 裡 `rm -rf .next/dev` 再跑一次。
- 本機 Node 版本要滿足 lock 裡套件的 `engines`（例如 jsdom 30 要 `^24.15.0`）。npm 只印 `EBADENGINE` 警告、不會失敗，所以要自己看 `node -v`。
- Playwright：`playwright.config.ts` 的 webServer 會起 `tools/e2e-runtime-api.mjs`（:8000 的假 API）與 `next dev`（:3000）；專案名是 `desktop-chromium`、`mobile-chromium`（Pixel 7）。`PLAYWRIGHT_SERVE_BUILD=true` 在 `npm run build:web` 之後改用 `next start`，跟 CI 一樣。本機裝的 chromium build 可能比 `@playwright/test` 要的舊，那時 e2e 只能靠 CI。
- scratchpad 裡臨時的 Playwright 量測腳本要用 `createRequire("<worktree>/apps/web/package.json")("playwright")` 解析套件。
- 完整版 Playwright Chromium 在 Windows ARM64 可能起不來（WinError 14001 side-by-side），同一個 build 的 headless shell 可以。要 Chromium 的後端程式（例如 `app.guides.pack_ingest.render_svg` 讀 `CHROMIUM_BIN`）指向 `$LOCALAPPDATA/ms-playwright/chromium_headless_shell-<rev>/chrome-headless-shell-win64/chrome-headless-shell.exe`。

## Python 與 API

- 首選跟 CI 一樣：`cd apps/api && uv sync --frozen`，在這個 worktree 建出 git 忽略的 `.venv`，裝的是這個 worktree 的程式；之後 `uv run ruff check .`、`uv run mypy app`、`uv run pytest`。
- uv 管理的直譯器拒絕 `pip install`（PEP 668）。不用 uv 時自建 venv：`python3.13 -m venv <scratchpad>/venv`，在 `apps/api` 裡 `<venv>/Scripts/python.exe -m pip install -e . --group dev`。
- **不要用主 checkout 的 `.venv` 驗 worktree 的改動**：它裝的是主 checkout 的程式，而且可能缺依賴（曾缺 `unidecode`，於是有檔案收集不到、`mypy app` 多出十幾個與你無關的錯）。
- 印中文的 Python 要 `PYTHONIOENCODING=utf-8`（或 `PYTHONUTF8=1`），否則 cp1252 下 `UnicodeEncodeError`。
- 本機沒有 PostgreSQL／Redis：`RUN_INTEGRATION_TESTS=1` 的測試全 skip。本機全綠不代表 CI 綠。
- 2026-09-25 重驗：以前要在 Windows 排除的 `test_deployment_center.py`、`test_deployments_integration.py`、`test_integration_postgres_redis.py`、`test_warning_codes.py` 現在都能收集、能過（deployment agent 在沒有 `UnixStreamServer` 的平台退回 TCP）。完整跑不需要 `--ignore`；若又有檔案收集不到，先看它是不是該加 `posix_only` 標記。
- 需要 PTY、Unix socket 的測試用 `pytest.mark.skipif(sys.platform == "win32", ...)`（例：`tests/test_ai_accounts_agent.py` 的 `posix_only`），Windows 上 skip。改到它們時進 WSL 驗：
  - WSL 裡沒有 pip／venv：把 worktree `.venv/Lib/site-packages` 裡的 `pytest _pytest pluggy iniconfig packaging py.py` 複製到 `/tmp/x-site`，程式與測試複製到 `/tmp/x`，`PYTHONPATH=/tmp/x-site:/tmp/x python3 -m pytest`。
  - 互相 import 的測試（`from tests.test_ai_accounts_agent import ...`）要照原本的佈局放：`/tmp/x/apps/api/{ai_accounts_agent,tests}`，讀 `parents[3]` 的測試還要 `/tmp/x/ops/...`，從 `/tmp/x/apps/api` 跑。
  - WSL 的 `/tmp` 可能在兩次呼叫之間被清掉：複製與執行放在同一個指令裡。
  - Git Bash 的 `tar` 會把 `C:/...` 當成遠端主機：先 `cd` 再用相對路徑。
  - `wsl.exe` 在 Claude Code 的沙箱裡會靜默失敗（exit -1073741571）：用 PowerShell 並關掉沙箱跑。回 `Wsl/Service/E_UNEXPECTED` 就 `wsl.exe --shutdown` 再試。

## 用 fakeredis 重現「只在 CI 壞」的 Redis 問題

症狀：本機過、CI 報 `RuntimeError: Event loop is closed`。成因：`app.infra.get_redis()` 是 `lru_cache` 單例，pytest-asyncio 每個測試一個 event loop；CI 有真的 Redis，第一個碰到 Redis 的測試留下綁在它 loop 上的連線，後面的測試透過真的 client 寫入就爆。本機沒有 Redis，同一個寫入變成被吞掉的 `ConnectionError`（`record_rate_limit_hit` 只接 `RedisError` 那一類），所以看不到。

本機重現：
1. 寫一個排序在最前面的測試檔，在 daemon thread 起 `fakeredis.TcpFakeServer(("127.0.0.1", 6399))`，並設 `daemon_threads = True`（否則 pytest 結束時卡住），測試裡 ping 一次 `infra.get_redis()`。
2. 帶 `REDIS_URL=redis://127.0.0.1:6399/0`，把這個檔排在可疑測試前面一起跑，外面包 `timeout`。

修法在測試：把那條路徑上**每一個** Redis 寫入都 stub 掉，不只是計數器。

## Bash 工具與檔案編碼

- **heredoc 會改寫內容**：含撇號、反引號時包裝層會重新引號；Python 字串裡的 `\n` 會變成真的換行。含跳脫、非 ASCII 的腳本一律用 Write 工具寫進 scratchpad 再執行。
- **`perl -0pi -e`／`sed -i` 配非 ASCII 取代字串會寫壞編碼**（中文變亂碼、混進無效位元組），反斜線與 Windows 路徑也會被吃掉。它們只用來改純 ASCII 的單行；含中文的編輯走 Write 工具或 Python。寫壞了就 `read_text(errors="replace")` 讀回重寫那幾行。
- **Write 工具偶爾把分隔字元寫成隱形位元組**：regex 字元類裡的 U+2028／U+2029 變成字面字元（`splitlines()` 在那裡斷行）、`" "` 變成 NUL（git 把 .ts 當二進位）。測試照樣全過。規則：控制字元與分隔符寫成跳脫序列；新檔 commit 後看 `git show --stat`，`Bin 0 -> N bytes` 就是有 NUL；要掃就用 Python 讀位元組找 `b"\x00"` 與 U+2028／U+2029。
- repo 檔案在 index 裡是 LF：Python 寫檔用 `newline=""`，別讓 CRLF 混進去。
- **背景指令的 `> log` 指向還不存在的目錄時，命令根本不會跑**，而「完成」通知回報的是後面那個 `echo` 的 exit code。先 `mkdir -p`，並讀 log 再相信通知。
- `cd "$D" && (A > a.log) & (B > b.log) & wait` 裡的 `cd` 只屬於第一個背景工作，B 會在原目錄跑、log 落在 worktree 根目錄（被 `*.log` 忽略，`git status` 看不到）。背景指令一律用絕對路徑。
- 這台機器的 Bash 沒有 `jq`，而且在管線裡靜默失敗：`n=$(... | jq length)` 變空字串，`[ "$n" != "0" ]` 反而成立，曾讓輪詢 CI 的腳本回報「全部完成、失敗 0」。用 `gh ... -q` 或 Python。
- `gh run list --commit <sha>` 會漏掉剛建立的 run，`gh pr checks` 在 check-run 掛上前回「no checks reported」；要確認 CI 有沒有被觸發，用 `gh api "repos/{owner}/{repo}/actions/runs?head_sha=<完整 sha>"`。
- 中文的 commit 訊息、PR 內文用檔案傳（`-F`、`--body-file`），不要當命令列參數。

## 內建瀏覽器（Browser pane）的假象

- 截圖只在 `scrollY` 為 0 時正常，捲動後回黑畫面：用 `resize_window` 模擬高視窗（例如 1000x2000、手機 390x2400），狀態用 `javascript_tool` 讀。滾輪 `scroll` 曾觸發上一頁。
- `element.click()`／`dispatchEvent` 是同步派送，會落在 React concurrent render 中間，state 更新被丟掉並噴 `Cannot update a component (X) while rendering a different component (Y)`；真人點擊不會。看 stack 裡是不是你自己的 handler 才算數。
- `read_console_messages` 會把 `%s` 參數配錯行，同一則訊息不同次讀取指名不同元件；`get_page_text` 偶爾回傳舊快照，以 `javascript_tool` 讀 DOM 為準。
- `read_page` 的無障礙樹會把 `<button><span>文字</span><span>數字</span></button>` 顯示成無名按鈕、`find` 搜不到，但瀏覽器算得出名稱。
- 面板隱藏時 IntersectionObserver 不觸發，lazy 區塊不掛載；別把「沒出現」當成被擋。
- 版面位移（CLS）在這裡量不到，見 browser-measurement.md。

## 預覽與假 API

- 沒有資料庫也能看後台頁：照 `tools/e2e-runtime-api.mjs` 的樣子寫一個一次性的 Node mock，`/api/v1/auth/me` 回 `is_admin: true` 再加你要的後台端點；web 的 `API_INTERNAL_URL` 指到它（寫在 `apps/web` 的 `.env.local`，`.env*` 已被忽略）。
- :8000、:8010 常被別的 session 佔住：先 `netstat -ano | grep ":<port> .*LISTENING"` 挑空的。
- `preview_start` 只讀 session 所在 worktree 裡 `.claude` 目錄下的 `launch.json`（git 不追蹤）。要看別的 worktree 的站：自己背景跑 `npm run dev --workspace @travel-scanner/web`，在 session worktree 放一個只有 `name`、`url`、`port`、沒有 command 的設定（會 attach 到現成的 server），用完刪掉。
- dev server 第一次編譯很慢（單一請求看過 7 秒以上）：量測前先確認頁面真的載完。
