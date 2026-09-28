---
id: 2026-09-28-video-shorts-knock-long-rounds-and
title: 工人的 Shorts 敲門：長輪次誤報沉默、STOP 檔不停敲門
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-09-28T15:33:40Z
completed_at:
branch:
depends_on: []
scope:
  - ops/video/worker.sh
  - docs/videos/AUTOMATION.md
  - .agents/skills/youtube-video/references/automated.md
  - .claude/skills/youtube-video/references/automated.md
---

# 工人的 Shorts 敲門：長輪次誤報沉默、STOP 檔不停敲門

## Why

#925（`f67b83715`）在 `ops/video/worker.sh:24-28` 加了 Shorts 的「敲門」：每一輪開頭跑 `node tools/video/shorts/cli.mjs tick`，API 端（`apps/api/app/video_shorts/tick.py:93`）鎖定到期的時段、送 YouTube、讀成效，並寫 `video_shorts_settings.last_tick_at`。2026-09-28 部署 `50b3cb55` 後的稽核確認了兩個問題：

1. **長輪次會誤報「工人沒有回報」。** 敲門只在迴圈開頭跑一次，接著是 `node tools/video/cli.mjs auto`，再睡 300 秒。`auto` 一輪最多做 40 個單位（`tools/video/automation/cli.mjs:15`），`docs/videos/AUTOMATION.md:39` 自己說一輪會跑幾十分鐘。`apps/api/app/video_shorts/rules.py:29` 的 `WORKER_SILENT_AFTER` 是 15 分鐘，`overview.py:74-80` 在活動進行中超過這個時間沒敲門，就在「需要你」列出「主機工人已經 N 分鐘沒有回報」。所以 `auto` 只要超過約 10 分鐘，工人明明健康，Shorts 分頁也會誤報，到期時段的鎖定與送出也要等這輪跑完。（鎖定在開始前至少 1 小時，`slots.py:279`，所以很少真的錯過時段。）
2. **STOP 檔停不了敲門。** 敲門前沒有檢查 `$VIDEO_WORKDIR/STOP`，只有 `auto` 會看（`automation/cli.mjs:93`）。但 `docs/videos/AUTOMATION.md:73` 與 skill 的 `automated.md:151` 都說放一個 STOP 檔可以讓工人整個停下來。敲門不花錢，Shorts 分頁也有自己的暫停與撤回，但照手冊操作的人會以為一切都停了，而敲門仍可能送 Shorts 上 YouTube（`tick.py:111`）。

## Definition of done

- [ ] `auto` 跑很久時，Shorts 分頁不再誤報工人沉默（擇一：敲門獨立計時、在 `auto` 的單位之間也敲門，或把門檻與實際輪次長度對齊，並在 `rules.py` 的註解寫明）。
- [ ] STOP 檔與 Shorts 敲門的關係只有一種說法：要嘛敲門也看 STOP 檔，要嘛 AUTOMATION.md 與 automated.md（兩份 skill 複本）寫清楚「STOP 不停 Shorts，用 Shorts 分頁的暫停」。

## Steps

- [ ] 決定兩個問題各自的做法（第一個若要改 `rules.py`，先把它加進 scope）。
- [ ] 改 `worker.sh` 或文件；skill 的兩份複本一起改，`npm run test:tools` 會比對。

## How to verify

```bash
npm run test:tools
```

部署後：`docker compose -f docker-compose.prod.yml logs --timestamps --since 3h api | grep 'shorts/tick'`，兩次敲門的間隔不再超過 15 分鐘；放 STOP 檔後的行為符合文件。

## Notes

`docs/videos/SHORTS.md:205` 刻意讓敲門不受長影片的「啟用」開關影響，但沒提 STOP 檔。

正式站已經看到第一個問題（2026-09-28，部署 `50b3cb55` 之後）：video-worker 15:05:23Z 起來，第一次敲門在 15:05:41Z 因 API 還在啟動而失敗，下一次成功的 `POST /api/v1/video/automation/shorts/tick` 200 是 15:43:36Z，再下一次 15:48:37Z。中間 38 分鐘就是一輪 `auto` 的長度，遠超過 15 分鐘的門檻；當時沒有 Shorts 活動在跑，所以分頁沒有真的誤報。
