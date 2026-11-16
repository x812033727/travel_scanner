---
id: 2026-11-16-autodeploy-daily-window
title: Auto deploy: deploy at most once a day inside an allowed Taipei window
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-11-16T01:12:56Z
completed_at:
branch:
depends_on: []
scope:
  - ops/autodeploy
---

# Auto deploy: deploy at most once a day inside an allowed Taipei window

## Why

站主要「每天定時檢查有沒有新的 commit，有就重新部署」（2026-11-16）。`ops/autodeploy` 已經是一支
每 5 分鐘一輪的輪詢器：`origin/main` 比 live 新、該 SHA 的 `CI` 綠、沒有暫停檔／鎖／分階段發布、
沒有付費影片工作，就跑 `/root/deploy-travel-scanner.sh`。它缺的只是「一天一次、固定時段」：
現在只有反向的 `AUTODEPLOY_BLOCKED_WINDOWS`，合併之後最多 25 分鐘就上線，一天可能部署很多次，
而每次部署都重啟所有容器、hotspot-collector 重算排行並吃 YouTube／Brave 額度。

設計與理由：`docs/ops/admin-redeploy-button-and-daily-autodeploy-plan.md`。

## Definition of done

- [ ] `AUTODEPLOY_DEPLOY_WINDOWS`（Asia/Taipei，`HH:MM-HH:MM`，逗號分隔，空值＝不限，維持現行行為）：
      設了之後，自動部署只在窗內**開始**；窗外的 tick 記 `wait`（gate `schedule`），不 fetch 以外的事都不做。
- [ ] `AUTODEPLOY_MAX_AUTO_DEPLOYS_PER_DAY`（預設 0＝不限）：台北日期當天已有一次成功的自動部署就 `idle`。
- [ ] 窗結束時，當天有新 commit 卻沒部署成（CI 紅、付費工作、暫停檔、hold），發**一次**通知寫明卡在哪道 gate
      與 SHA（走既有 `AUTODEPLOY_NOTIFY_URL`），state.json 記 `last_missed_window`。
- [ ] 窗跟 `AUTODEPLOY_BLOCKED_WINDOWS` 同時設定時，blocked 優先；跨午夜的窗（`23:30-01:00`）可用。
- [ ] `autodeploy.env.example`、`ops/autodeploy/README.md` 的 gate 表與「Install and roll out」寫進這兩個設定；
      `autodeploy.py status` 印出下一個窗的開始時間。
- [ ] `python -m unittest discover -s ops/autodeploy -v` 綠，新測試覆蓋：窗外等、窗內部署、當日已部署、
      跨午夜、錯過窗只通知一次。

## Steps

- [ ] `Config.from_mapping` 讀兩個新設定，沿用 `parse_windows`；gate 放在現在的 gate 5（blocked windows）旁邊，
      但要在 gate 2（`idle`）之後，這樣沒有新 commit 時照樣是 `idle` 而不是 `wait`。
- [ ] timer 保持每 5 分鐘：窗內若 CI 還在跑或付費工作在跑，下一輪會重試；後台按鈕
      （`2026-11-16-admin-redeploy-button-via-timer`）也靠這個輪詢接單。
- [ ] 錯過窗的通知：用 state.json 記「這個台北日期已通知」，避免每輪重發。
- [ ] README、env 範例、單元測試。

## How to verify

```bash
python -m unittest discover -s ops/autodeploy -v
```

主機上（裝好之後）：`AUTODEPLOY_DEPLOY_WINDOWS=04:30-06:00`、`AUTODEPLOY_ENABLED=false` 跑一天，
`journalctl -u travel-scanner-autodeploy` 裡窗外每輪都是 `wait: schedule`，窗內第一輪是 `would_deploy`。

## Notes

- 站主待決（計畫文件第四節）：時段（建議台灣 04:30–06:00，流量最低、在 hotspot 每日排行之前或之後要再確認）、
  一天最多幾次、錯過窗要不要通知。
- 真正上線還要 `2026-10-07-autodeploy-rollout-and-skill-docs` 的主機安裝（token、乾跑週、開啟）；
  程式可以先合併，不必等那張票。
- 不改 systemd timer 的 `OnCalendar`：只靠 timer 每天跑一次的話，那一輪剛好遇到 CI 未完成或付費工作就整天不部署，
  按鈕也收不到單。
