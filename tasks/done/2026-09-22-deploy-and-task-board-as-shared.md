---
id: 2026-09-22-deploy-and-task-board-as-shared
title: Deploy and task board as shared Codex/Claude skills
status: done
priority: P2
area: tools
owner: claude-fable-5-1
claimed_at: 2026-09-22T15:05:18Z
created_at: 2026-09-22T15:05:09Z
completed_at: 2026-09-22T15:25:15Z
branch: claude/deploy-task-board-skills
depends_on: []
scope:
  - .agents/skills/deploy
  - .claude/skills/deploy
  - .agents/skills/task-board
  - .claude/skills/task-board
  - AGENTS.md
---

# Deploy and task board as shared Codex/Claude skills

## Why

`content-pipeline`（PR #664）之後站主要求把另外兩套流程也做成 Codex 與 Claude Code 共用的 skill：

- **部署**：怎麼判斷暫停檔背後的分階段發布是活的還是被遺棄的、部署腳本的旗標、包裝腳本（nohup、`DEPLOY_EXIT`）、
  auto 模式分類器擋什麼、SSH 一次跑一個腳本、`ps` 自我比對、磁碟在 containerd 而不在 docker、nginx 的假陽性檢查。
  這些只在 Claude 的個人記憶裡（27 KB 部署記憶加六個相關記憶檔），主機預檢與包裝腳本只在某個 session 的 scratchpad。
- **任務看板**：claim 不是鎖、`+` 分支才是檢查、在 PR 內結案、strict 分支保護下的 rebase 與 `--match-head-commit`、
  怎麼證明 squash 合併過的分支已落地、過期認領鎖住哪些票。同樣只在記憶裡（14 KB 看板記憶加五個相關記憶檔），
  每次總整理都重寫一次「誰在做什麼」的唯讀腳本。

## Definition of done

- [x] `.agents/skills/deploy/` 與 `.agents/skills/task-board/` 存在，各有逐字複本在 `.claude/skills/`，`npm run test:tools` 過。
- [x] 兩個 skill 都通過 Codex 的 `quick_validate.py`（`PYTHONUTF8=1`）。
- [x] 腳本可執行：`host-preflight.sh`、`host-deploy.sh`、`merge-when-green.sh` 過 `bash -n`；`who-is-on-it.mjs` 對這個 repo 跑得出報告；
      `merge-when-green.sh` 用的 check-run 查詢對 #664 的 head 回 `completed/success` ×4。
- [ ] 主機端腳本在真正的部署上跑過一次（下一次部署時驗）。
- [ ] Claude 端的記憶縮短、指向 skill（合併後做）。

## Steps

- [x] 開票、認領、從 origin/main 開分支。
- [x] deploy：SKILL.md（92 行）、preflight／runbook／post-deploy／pitfalls 四份 reference、`host-preflight.sh`、`host-deploy.sh`、`agents/openai.yaml`。
- [x] task-board：SKILL.md（71 行）、collisions／merge／ticket-template 三份 reference、`who-is-on-it.mjs`、`merge-when-green.sh`、`agents/openai.yaml`。
- [x] AGENTS.md 那一句補上兩個 skill 名。
- [ ] PR、合併。
- [ ] 下一次部署用 `host-preflight.sh` 與 `host-deploy.sh` 跑，把實際結果記回 `references/runbook.md`。
- [ ] 合併後縮短記憶：部署（27 KB）、看板（14 KB）改成歷史＋指標；MEMORY.md 的 hook 縮成一行。

## How to verify

```bash
npm run test:tools
cd apps/api && PYTHONUTF8=1 .venv/Scripts/python.exe "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ../../.agents/skills/deploy
cd apps/api && PYTHONUTF8=1 .venv/Scripts/python.exe "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ../../.agents/skills/task-board
bash -n .agents/skills/deploy/scripts/host-preflight.sh .agents/skills/deploy/scripts/host-deploy.sh .agents/skills/task-board/scripts/merge-when-green.sh
node .agents/skills/task-board/scripts/who-is-on-it.mjs --scope AGENTS.md
```

主機端腳本沒有本機可跑的目標；下一次部署照 `.agents/skills/deploy/SKILL.md` 的指令跑，`host-preflight.sh` 應印出暫停檔、規則 1 標記、鎖、live HEAD 與 origin/main、磁碟、最後一份 log。

## Notes

- `who-is-on-it.mjs` 第一次跑就抓到板子的實況：43 張持有中的票，其中大多數 `review` 超過 50 小時、分支已經不存在（合併後 GitHub 自動刪），
  各自鎖住 1 到 9 張未認領的票。這是下一次總整理的清單，不在本票 scope。
- 兩種「hold」要分清：主機的 `/root/travel-scanner-deploy.hold` 擋部署；repo 的 `apps/api/app/guides/publish_holds.json` 擋發布特定 slug。
  skill 裡明寫。
- 主機連線方式（PuTTY session、金鑰路徑）刻意不進 skill，`tools/skills.test.mjs` 也擋機器路徑；用 `<SSH>` 佔位。
- `ops/deployer/` 的第三條部署路徑還不認暫停檔（`ops/release/README.md` 自己說是另一張票）；skill 只註明，不擴 scope。
- `docs/travel-guides.md` 第 589 行附近寫的部署後匯入沒有 `--slug`，照做會把刻意保留的文章全部發布；skill 一律指向
  `content-pipeline` 的 publish-runbook，不指那一段。
