---
id: 2026-11-10-drive-rules-sync
title: 規則與教訓同步到雲端硬碟（AI劇/_共用規則、各劇 _規則與教訓）
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5
claimed_at: 2026-11-10T13:18:12Z
created_at: 2026-11-10T13:18:10Z
completed_at:
branch: claude/drive-rules-sync
depends_on: []
scope:
  - docs/videos/rules-sync
  - docs/videos/lessons
---

# 規則與教訓同步到雲端硬碟（AI劇/_共用規則、各劇 _規則與教訓）

## Why

站主 2026-11-10：「幫我規劃將教訓與規則都放雲端，共用區與每一個的個別的；共用區又有分是奇聞跟原來如此，還有個別的 AI劇」
「這樣以後只要有一個更新就不怕漏了」。規則和教訓散在 skill、`docs/videos/` 各處和單集的 NOTES，雲端硬碟上沒有；
沒有一個地方能一次看到某部劇要遵守什麼、學過什麼。

## Definition of done

- [x] repo 是唯一正本；`docs/videos/rules-sync/manifest.tsv` 寫明每份規則／教訓放雲端哪裡（第 0 層共用、解說系列共用兩邊各一份、各劇、各集）。
- [x] `watch.txt` 範圍內的檔沒有去處時 `npm run test:docs-videos` 失敗（不會漏）。
- [x] `docs/videos/lessons/` 每層一份教訓檔。
- [ ] 主機第一次同步完成、核對 0 差異；每小時的 cron 裝好。

## Steps

- [x] `sync.mjs`（讀 origin/main、staging、`rclone sync` 只動同步專用資料夾、`--backup-dir`、`rclone check`）與測試。
- [x] 對照表、watch、教訓檔、README。
- [ ] PR、站主合併。
- [ ] 合併後：主機跑第一次同步（等分支搬家結束，免得搶上傳）、裝 cron。

## How to verify

```bash
node --test docs/videos/rules-sync/sync.test.mjs
node docs/videos/rules-sync/sync.mjs --dry-run
```

主機同步後：雲端 `AI/備份/AI劇/_共用規則/目錄.md` 列出所有副本；log 有 `0 differences`。

## Notes

- 站主選雲端只當唯讀副本（不雙向）；解說系列共用（`explainer-series/README.md`、`lessons/explainer.md`）照計畫在奇聞、原來如此各放一份。
- 用 `rclone sync` 而不是 copy：只限三種同步專用資料夾（filter），被換掉或刪掉的檔進 `AI劇/_舊版-規則同步/<時間>/`，沒有東西真的被刪。
- 副本開頭的說明不放 commit 碼，否則每次合併每個檔都會變、`_舊版` 會塞滿。
- AGENTS.md 的指引另外補在 #2059（那個任務的 scope 有 AGENTS.md）。
