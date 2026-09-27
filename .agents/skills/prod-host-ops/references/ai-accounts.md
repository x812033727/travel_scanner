# 主機的 AI 帳號代理（/admin/ai-accounts）

安裝、信任邊界、復原的全文在 `ops/ai-accounts/README.md`；代理的程式在 `apps/api/ai_accounts_agent/`，API 端在 `apps/api/app/admin_ai_accounts/`。這裡是日常使用。

## 它是什麼

主機上以 root 跑的 Claude Code、Codex CLI 與 Antigravity CLI（`agy`）用站主的訂閱計費。systemd 服務 `mokaair-ai-accounts` 在 Unix socket `/run/mokaair-ai-accounts/agent.sock` 上回答固定幾種 HMAC 簽章的請求，api、worker、news-worker 容器掛著這個 socket。每個工具（`claude`、`codex`、`agy`）有五個帳號槽 `a`–`e`，後台 `/admin/ai-accounts` 的「訂閱帳號」分頁（只有站主看得到）可以登入、選預設帳號、看 email、方案與剩餘額度。容器裡永遠沒有 CLI、token 或憑證檔。

## 在主機上用哪個帳號

- 互動式 root shell 裡的 `claude`、`codex`、`agy` 用**預設帳號**；帳號在指令啟動時決定，執行中的 session 不會因為換預設而換帳號。
- `claude-b`、`codex-c`、`agy-d` 這類指令固定用那個槽，任何 shell 或腳本都一樣。
- 不經過 shell 函式、直接跑 `/root/.local/bin/claude`、`/usr/local/bin/codex`、`/root/.local/bin/agy` 的（cron、`nohup`、非互動的 `ssh host cmd`）一律是 **A 槽**，因為 `/root/.claude`、`/root/.codex`、`/root/.gemini/antigravity-cli` 連到 A。
- 帳號資料在 `/var/lib/mokaair-ai-accounts/<工具>-<槽>`，預設槽的字母在 `default-claude`／`default-codex`／`default-agy`。

## 登入壞了

後台完成不了登入（例如 CLI 更新改了登入畫面）時，在主機上登入：`claude-b auth login`、`codex-b login --device-auth`，或跑 `agy-b` 選 Google OAuth。Antigravity 第一次啟動可能有首次使用頁（條款、配色），代理不會替站主回答，要站主透過 SSH 跑一次 `agy-<槽>`。`AI_ACCOUNTS_ALLOWED_EMAILS`（在 `/etc/travel-scanner/ai-accounts.env`）有設時，登入到清單外的帳號會立刻被登出；清單空著時頁面會警告。

## 額度從哪裡來

| 工具 | 來源 | 注意 |
| --- | --- | --- |
| Codex | `codex app-server` 的 `account/rateLimits/read`，快取 5 分鐘 | 讀額度可能刷新 token，太頻繁會和互動 session 撞出「refresh token already used」；要新值按頁面的重新整理 |
| Claude | 狀態列的 `rate_limits.five_hour`／`seven_day`，由 `statusline-record claude-<槽>` 記進該帳號的 `mokaair-usage.json` | 有人在 SSH 上用 Claude 就會更新；快照缺或超過 30 分鐘、按重新整理（每帳號每分鐘最多一次）、剛登入時，代理會用 `--restricted --model haiku` 開一次 Claude Code 自己去讀。專案自己的 Claude 設定檔（專案目錄下的 settings.json）若設了 `statusLine` 會蓋過它。API 計費的帳號不探測 |
| Antigravity | TUI 的「Models & Quota」頁（`/usage`），代理開 `agy`、打 `/usage`、用小型終端模擬器讀畫面 | 失敗原因會顯示在頁面：`signed_out`（停在登入選擇）、`setup_needed`（首次使用頁）、`unreadable`（找不到額度列，畫面內容以遮蔽 email 的形式寫進 `journalctl -u mokaair-ai-accounts`，版面變了就從那裡改解析器） |

## 網站怎麼用這些帳號

`POST /v1/runs` 以關掉所有工具的 `claude -p` 跑一個 prompt，挑在用量上限以下、剩最多額度的 Claude 帳號。影片產線一直用它；「AI 供應商與金鑰」卡的 Claude 連線方式選「訂閱帳號」後，介紹搜尋、介紹撰寫、介紹審查、簡體名稱與新聞各階段的 Claude 呼叫也改走它（`apps/api/app/ai/subscription.py`），行程規劃與行程文字解析不走。

- 每個帳號一次只跑一個 prompt，不同帳號並行；請求最多等它的 `queue_seconds`，等不到回 `subscription_busy`。
- 撞到用量上限的帳號休息 30 分鐘；全部到上限回 `subscription_quota_paused`，網站有 MiniMax 金鑰就改用 MiniMax。上限百分比是 `ai_vendors` 卡的 `ai_subscription_max_usage_percent`。
- Codex 不提供（`codex exec` 關不掉它的 shell，唯讀沙箱仍讀得到 `.env`）；Antigravity 也不提供（條款禁止把它接到別的產品，代理只驅動官方 binary、從不讀它的 token）。

## 檢查

```bash
systemctl status mokaair-ai-accounts
# 沒簽章的請求要被拒
curl -s --unix-socket /run/mokaair-ai-accounts/agent.sock http://agent/v1/accounts
# 簽章的請求列出每個槽（email 已遮蔽）
set -a; . /etc/travel-scanner/ai-accounts.env; set +a
cd /opt/mokaair-ai-accounts && python3 -m ai_accounts_agent.client GET /v1/accounts
journalctl -u mokaair-ai-accounts --since '1 hour ago'
```

改主機上 root 的 CLI 設定（安裝、升級代理、移動登入）都要站主同意，而且要先關掉所有 `claude`／`codex`／`agy` session；那是 `ops/ai-accounts/README.md` 的 Install 段。
