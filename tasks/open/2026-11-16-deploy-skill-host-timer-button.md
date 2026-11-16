---
id: 2026-11-16-deploy-skill-host-timer-button
title: Deploy skill: admin button and daily window run through the auto deploy timer
status: review
priority: P2
area: docs
owner: claude-opus-5-5-autodeploy
claimed_at: 2026-11-16T04:15:42Z
created_at: 2026-11-16T01:58:55Z
completed_at:
branch: claude/fervent-wright-70jrlh
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

- [x] `.agents/skills/deploy/SKILL.md`（與 `.claude/skills/deploy/SKILL.md` 逐字相同）：主機表的四條路徑改寫；
      規則 9 的「最多 25 分鐘」改成「下一個部署時段」；`button-<ts>.log`、`deployment_host_status` 列進表。
- [x] `references/runbook.md`、`references/preflight.md` 補按鈕請求被拒絕的錯誤碼怎麼讀。
- [x] `npm run test:tools`：skill 鏡像檢查（`tools/skills.test.mjs`）7/7 過；見 Notes。

## Steps

- [x] 讀 `ops/autodeploy/README.md` 的 "Once a day"、"The admin button"、"The heartbeat" 三節，只寫指標，不重抄規則。

## How to verify

```bash
npm run test:tools
```

## Notes

- 主機安裝本身仍在 `2026-10-07-autodeploy-rollout-and-skill-docs`。
- 2026-11-16 claude-opus-5-5-autodeploy（PR x812033727/travel_scanner#2124）：SKILL.md 主機表的四條路徑改成
  一次性腳本／自動部署 timer（部署時段）／後台按鈕（經 timer）／分階段驅動，部署代理降為未啟用的替代方案；
  自動部署檔案列加 `button-<ts>.log`、兩個新設定與 `deployment_host_status`；規則 9 改成「下一個部署時段，急就請站主按按鈕」；
  「規則在哪裡」加 autodeploy README 三節的指標。`runbook.md` 加按鈕拒絕碼表與「按鈕請求在跑時先等」，
  `preflight.md` 的自動部署暫停檔改成也擋按鈕。`.claude/skills/deploy/SKILL.md` 逐字同步。
  `npm run test:tools` 在這個容器有 16 個失敗，全在 `tools/deploy-host-verify.test.mjs`（awk 的 `REcompile() - panic`，
  容器的 awk 版本問題），把本票改動 stash 掉之後一樣 16 個失敗，和本票無關；CI 上這支測試是綠的。
