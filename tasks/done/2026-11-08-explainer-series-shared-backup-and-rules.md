---
id: 2026-11-08-explainer-series-shared-backup-and-rules
title: Explainer series share one backup and rule set for curio and so that's why
status: done
priority: P1
area: docs
owner: claude-opus-5-5-curio-redo-20
claimed_at: 2026-11-08T07:18:40Z
created_at: 2026-11-08T07:18:32Z
completed_at: 2026-11-08T13:14:43Z
branch: claude/curio-redo-20-episodes-ldnrq0
depends_on: []
scope:
  - docs/videos/explainer-series
  - .agents/skills/curio-episode
  - .claude/skills/curio-episode
---

# Explainer series share one backup and rule set for curio and so that's why

## Why

奇聞檔案局與原來如此事務所用同一套工具、同一條關卡，但備份方式、誰核准前四關、何時能刪工作目錄、插圖放大檢查的做法各寫在不同地方，
而且彼此不同。站主 2026-11-07 兩邊都刪過沒備份完的檔（原來如此 P07／P14 配音、奇聞 W03 旁白原檔），2026-11-08 要求比照
AI 劇的 PR #2047 把兩個系列的備份與共同規則統一，並在 PR 裡跟原來如此那邊討論。

## Definition of done

- [x] `docs/videos/explainer-series/` 有共用規則（README.md）與備份分支規則（BACKUP-BRANCHES.md），命名與核對方式跟 #2047 一致。
- [x] `backup/` 有可用的推分支（tobranch.sh）與涵蓋檢查（coverage.sh），不寫死 session 與絕對路徑。
- [x] 原來如此那邊在 PR 裡看過、沒有異議或已改好（2026-11-08 10:31，已推 `transfer/sothatswhy-shared`）。
- [x] 站主確認 README 最後一節的三點（2026-11-08：1 分開、2 可以、3 好）。

## Steps

- [x] 讀 #2047 的 drama 文件、原來如此的 README 第 9、10 節、HANDOFF.md、tools/tobranch.sh。
- [x] 寫統一表、兩邊都踩過的坑、不統一的項目、待站主確認的三點。
- [x] 寫並測試 backup/ 的兩支腳本（本機 bare repo：一般檔、含空白的路徑、200 MB 與 100 MB 切塊、重推、竄改後抓得到）。
- [x] curio-episode skill 加一行連到這裡。
- [x] PR 討論後的修改（分批推送、對照表更正、三個坑、配樂床、既有分支、LEASE、暫存物件目錄）。

## How to verify

```bash
bash -n docs/videos/explainer-series/backup/*.sh
npm run check:tasks && npm run test:tools
```

推一條測試分支到本機 bare repo，`tobranch.sh` 印 `verify mismatches: 0`，`coverage.sh` 印 `missing: 0  mismatches: 0`；
把工作目錄某個檔改一個位元組，`coverage.sh` 要報 MISMATCH 並回非 0。

## Notes

- 原來如此自己的文件（`docs/videos/so-thats-why/…`）與 `docs/videos/BACKUP.md` 不動，避免跟 #2047 與另一個 session 衝突；
  系列文件跟共用區衝突時以共用區為準，寫在 README 開頭。
- 原來如此原本的 tobranch.sh 寫死另一個 session 的 id 與 `/home/user/travel_scanner`，切塊門檻 90 MB；新版改成署名從
  `TOBRANCH_TRAILERS` 讀、從 `git rev-parse --show-toplevel` 找 repo、95 MB 以上才切（跟 #2047 相同），並核對切塊重組後的 sha256。
