---
id: 2026-11-16-deploy-skill-host-timer-button
title: Deploy skill: admin button and daily window run through the auto deploy timer
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-16T01:58:55Z
completed_at:
branch:
depends_on:
  - 2026-11-16-admin-redeploy-button-via-timer
scope:
  - .agents/skills/deploy
  - .claude/skills/deploy
---

# Deploy skill: admin button and daily window run through the auto deploy timer

## Why

skill `deploy` 的主機表與規則還把「後台部署中心」寫成 `ops/deployer` 的代理（第四條路徑，預設關、不認暫停檔）。
2026-11-16 起正式站的後台按鈕改由 autodeploy timer 執行（`DEPLOYMENT_EXECUTOR=host_timer`），而且自動部署只在
台灣時間 04:30–06:00 一天一次。代理不知道這些的話，會以為合併後 25 分鐘就上線，或誤判按鈕走的是代理。

## Definition of done

- [ ] `.agents/skills/deploy/SKILL.md`（與 `.claude/skills/deploy/SKILL.md` 逐字相同）：主機表的四條路徑改寫；
      規則 9 的「最多 25 分鐘」改成「下一個部署時段」；`button-<ts>.log`、`deployment_host_status` 列進表。
- [ ] `references/runbook.md`、`references/preflight.md` 補按鈕請求被拒絕的錯誤碼怎麼讀。
- [ ] `npm run test:tools` 通過。

## Steps

- [ ] 讀 `ops/autodeploy/README.md` 的 "Once a day"、"The admin button"、"The heartbeat" 三節，只寫指標，不重抄規則。

## How to verify

```bash
npm run test:tools
```

## Notes

- 主機安裝本身仍在 `2026-10-07-autodeploy-rollout-and-skill-docs`。
