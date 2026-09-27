# 檢查：指令、本機與 CI 的差、會騙人的綠燈

## 推 PR 前的清單（`AGENTS.md` §Checks before you push）

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run test:tools && npm run check:tasks
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest
```

跑你動到的那幾組。`&&` 串起來只在互動終端機裡看得清楚；在代理工具裡請用 `.agents/skills/dev-and-ci/scripts/run-checks.sh`，它每個檢查一個 log、印 exit code、最後彙總。

| 指令 | 實際跑什麼 | 備註 |
| --- | --- | --- |
| `npm run lint:web` | `eslint . --max-warnings=0` | 警告也算失敗 |
| `npm run check:i18n` | `node tools/check-i18n.mjs` | 鍵的規則在 skill `web-i18n-e2e` |
| `npm run typecheck:web` | `tsc --noEmit` | 唯一會抓到「套件其實沒裝」的檢查 |
| `npm run test:web` | `vitest run`（jsdom，setup 在 `apps/web/vitest.setup.tsx`） | 單檔：`cd apps/web && npx vitest run <files>` |
| `npm run test:tools` | `node --test tools/*.test.mjs "tools/video/**/*.test.mjs"` | 需要 `npm ci`（js-yaml、pinyin-pro、字型套件）；skill 的複本比對也在這裡 |
| `npm run check:tasks` | `node tools/tasks.mjs check` | 票的格式、狀態對資料夾 |
| `uv run ruff check .` | ruff lint | CI **不跑** `ruff format --check`，repo 也不是 format-clean：只 format 你新建的檔 |
| `uv run mypy app`、`uv run mypy tests` | strict mypy；tests 的放寬規則在 `apps/api/pyproject.toml` 的 override | 分兩行，失敗會指名是哪一邊 |
| `uv run pytest` | 單元測試；整合測試沒有 `RUN_INTEGRATION_TESTS=1` 就 skip | CI 是 `pytest --cov=app` 且帶該變數 |

## 讀 exit code 的正確寫法

```bash
mkdir -p "$SCRATCH"                     # 目錄不存在時，重導向失敗、命令根本沒跑
npm run lint:web > "$SCRATCH/lint.log" 2>&1; code=$?; echo "lint exit=$code"
grep -n "error\|warning" "$SCRATCH/lint.log" | head -40
```

- 不要 `cmd 2>&1 | tail -40 && next`：exit code 是 `tail` 的，`&&` 也照 `tail` 走。必要時先 `set -o pipefail`。
- 背景指令的「完成」通知只說最後一個命令的狀態；讀完整的 log。
- 讀 CI 的檢查狀態也一樣：永遠不要 `gh pr checks --watch | tail`，照 skill `task-board` 用 check-runs API。

## 只有 CI 驗得到的東西

- **整合測試**（真的 PostgreSQL 17、Redis 7.4、MinIO）：寫之前先想清楚，一輪約 15–18 分鐘。常見坑：
  - `httpx.AsyncClient` 預設保存 cookie，而 `POST /auth/register` 會設登入 cookie，同一個 client 送的「匿名」請求其實是登入身分。要驗 401 就另開一個乾淨的 client（`tests/test_ui_text_integration.py` 有註解）。
  - Redis 單例跨 event loop 的 `Event loop is closed`：見 local-env.md 的 fakeredis 重現。
- **e2e**：`web` job 的隔離清單與 `full-stack-smoke` 的旅程。本機可以跑 `npx playwright test <spec> --project=desktop-chromium`（在 `apps/web`，約 2 分鐘），前提是 chromium build 對得上。
- **containers**：compose 與映像建置，本機通常不跑。

## 會騙人的綠燈（本機過、CI 或未來會紅）

- **兩個各自會過的 PR 合在一起才壞**：例如 sitemap import 了 `server-only` 模組後，任何會載入 sitemap 的 vitest 都得 `vi.mock("@/lib/community/server")`，照 `apps/web/app/sitemaps/sitemap.test.ts`。rebase 到最新 main 後再跑一次受影響的測試。
- **日期算術**：`start.replace(day=min(start.day + 2, 28))` 在 29–31 號會紅、`date.today().replace(year=...)` 在 2 月 29 日會丟例外。測試裡一律用 `timedelta`。
- **午夜 UTC 換日**：用「今天」算期望值的測試在 UTC 00:00 前後跑會紅（還有一張開著的票在追 `test_ai_trip_parser_llm`）。
- **ruff E501 用顯示寬度算**：CJK 字元算 2，70 個漢字的行會是「107 > 100」。拆行用 `unicodedata.east_asian_width`，不是 `len()`。
- **vitest 的 next-intl mock 每個 namespace 快取一個 translator**（`apps/web/vitest.setup.tsx`）：元件可以把 `t` 放進 effect 的 dependencies；自己寫的 mock 若每次回新函式，effect 會無限重跑。
- **舊的 `node_modules`**：本機紅或綠都可能是版本不對，見 local-env.md。
- 完整跑一次 API 測試（Windows、worktree 自己的 `.venv`）應該沒有失敗；有的話先確認不是環境（編碼、路徑分隔符 `\` 對 `/`）再修。
