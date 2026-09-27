---
id: 2026-09-25-video-auto-subscription-runner-writing-stages
title: Video auto subscription runner: writing stages through a signed-in Claude Code account on the host
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T08:30:38Z
created_at: 2026-09-25T08:30:27Z
completed_at: 2026-09-25T08:43:47Z
branch: claude/video-auto-subscription
depends_on:
  - 2026-09-25-video-auto-model-runner-the-server
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/app/admin_ai_accounts/agent.py
  - apps/api/app/video_automation
  - apps/api/migrations/versions/0092_video_subscription_limit.py
  - apps/api/tests/test_video_automation_subscription.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - docs/videos/AUTOMATION.md
---

# Video auto subscription runner: writing stages through a signed-in Claude Code account on the host

## Why

2026-09-25 站主原本選「API 金鑰，預設 Sonnet 寫、Opus 查」。後來問到主機上的訂閱帳號，我說明了兩點：
- 2026-09-24 那張票記錄，把網站的自動化放在個人訂閱上，可能違反 Anthropic／OpenAI 的消費者條款，出事的是站主每天在用的帳號；
- 額度會用完。

站主回應：
- 額度可以到上限就不跑；
- 條款他自己看過，決定「用訂閱全自動」。

所以寫稿、查核、翻譯改走主機上登入的 Claude 訂閱帳號，API 金鑰留著當每個階段都能改選的選項。

## Definition of done

- [x] 主機代理 `POST /v1/runs`（`ai_accounts_agent.runs`）：
  - 從登入的 Claude 訂閱帳號裡，挑 5 小時與每週額度中「最滿的那個窗」最空、而且低於門檻的帳號；用量未知的帳號放最後才試。
  - 執行 `claude -p --output-format json --model … --tools "" --strict-mcp-config --no-session-persistence --system-prompt-file …`，提示詞從 stdin 送；每次只跑一個。
  - 執行環境從零建立，帶不到 HMAC 金鑰；工作資料夾用完就刪。
  - 全部帳號都超過門檻時回 429 `subscription_quota_paused`，附最早重置的時間；沒有帳號登入時回 409。
  - CLI 回「hit your weekly limit」也算暫停，不算失敗。
- [x] Codex 不提供：`codex exec` 關不掉 shell，read-only 沙箱仍然讀得到 `.env`。
- [x] API：
  - `AiAccountsAgentClient.run_prompt` 的讀取逾時是 960 秒，代理本身在 900 秒停掉。
  - 影片階段的新選項 `claude_code`，六個階段的預設都改成它；遷移 0092 把還沒有人存過的設定列換成新的預設。
  - 門檻欄位 `subscription_max_usage_percent`，預設 80。
  - 每月 token 上限只算 API 金鑰的呼叫；訂閱用量另外記、另外顯示；草稿數上限兩邊都算。
  - 暫停時不記呼叫，工人下一輪再試。
- [x] 設定分頁：
  - 「Claude Code（訂閱帳號）」選項，主機代理沒設定時會標出來；
  - 門檻欄位；
  - 用量說明。
- [x] `docs/videos/AUTOMATION.md` 記下決定與做法。

## Steps

- [x] 代理的執行與路由。
- [x] API 用戶端與影片階段接上。
- [x] 遷移、設定分頁、五語系文字。

## How to verify

- `uv run pytest tests/test_ai_accounts_agent_runs.py tests/test_video_automation_subscription.py tests/test_video_automation_ai.py`：
  - 假的 claude 腳本記下它實際收到的參數、stdin 和環境變數；
  - 測試證明所有工具都關了、提示詞原樣送出、環境裡沒有代理的金鑰、工作資料夾有刪掉。
- 部署後要在主機上：
  1. 重新安裝代理（`ops/ai-accounts/install.sh`），要站主同意；
  2. 重新啟動 `mokaair-ai-accounts`；
  3. 用一個短提示詞打 `/v1/runs`，確認選到帳號、有回應、token 有記下來。

## Notes

- **代理要重裝才會生效**：程式在主機的 `/opt/mokaair-ai-accounts`。正式站的部署腳本只重建容器，不會更新代理；這一步放在 `video-auto-rollout`。
- **用量快照可能舊到 30 分鐘**：`claude -p` 不會更新狀態列快照（2026-09-24 實測），用量靠總覽觸發的探測更新。門檻預設 80% 留了餘裕。
- **工人還要一個小改動**：`tools/video/automation/client.mjs` 要把 `video_ai_subscription_paused` 當成「這輪先停」、不要連重試四次。這在 orchestrator 的分支做。
