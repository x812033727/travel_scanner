---
id: 2026-11-10-drive-ai-drama-layout
title: AI 劇雲端硬碟備份改成 AI劇/<名稱>/<集數>/，製作檔由 session 直接傳
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-11-10T01:25:17Z
created_at: 2026-11-10T01:25:09Z
completed_at:
branch: claude/drive-ai-drama-layout
depends_on: []
scope:
  - apps/api/app/video_backup
  - apps/api/tests/test_video_backup.py
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - docker-compose.prod.yml
  - docs/videos/BACKUP.md
  - docs/videos/AI-DRAMA-DRIVE.md
  - docs/videos/ai-drama-drive
  - AGENTS.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - .agents/skills/minimax-h3-runpod/references/route-a.md
  - docs/videos/explainer-series
  - docs/videos/so-thats-why/dialogue-pilot-20261103
  - docs/videos/series-plans/zhong-tian-qu-qi/production/README.md
  - docs/videos/zhong-tian-qu-qi-e001-r2/brief.md
---

# AI 劇雲端硬碟備份改成 AI劇/<名稱>/<集數>/，製作檔由 session 直接傳

## Why

站主 2026-11-10 重新規劃 AI 劇（種田、祖媽、原來如此、奇聞）的備份：

- 「每部劇統一放 AI劇/<劇名>/<集數>/」，在 `AI/備份/` 底下；集數寫成 `第033集`，沒有集數的用代碼（`H01`）。
- 種田的真人重拍版（`-r2`）當成另一部劇；同一集的 `-v2`、`-v3` 放同一個資料夾，舊版進 `_舊版/`。
- 「備份都要備份到所有東西，之後需要重製可能的所有東西」，參照 #2047、#2048 的分支規則。
- 製作檔由做片的 session 直接傳雲端硬碟（不經主機 worker）；舊的 `transfer/*` 分支照對照表搬過去，
  雲端硬碟核對完整後刪除分支。

之前影片備份把種田放在 `drama/<劇>/<slug>/`、奇聞在 `奇聞檔案局/<slug>/`；製作檔只在四個備份 repo 的分支上，
雲端硬碟沒有。`-r2` 不被認成種田，平放在 `drama/` 底下。

## Definition of done

- [x] 網站給 worker 的資料夾是 `AI劇/<名稱>/<集數>/`；`-r2` 是「種田娶妻打天下（真人版）」；較舊的版本在 `<集數>/_舊版/<slug>/`。
- [x] 之前放在別處的備份，worker 在雲端硬碟搬過來一次；搬進已有檔案的資料夾時不覆蓋任何檔。
- [x] worker 的分支鏡像關掉（從沒成功跑過：`fs.copyFileSync is not a function`）。
- [ ] `docs/videos/AI-DRAMA-DRIVE.md`：要備份什麼、放哪裡、session 怎麼傳（`todrive.sh`）、怎麼核對、何時刪分支。
- [ ] 舊分支照 `docs/videos/ai-drama-drive/legacy-branches.tsv` 搬到雲端硬碟，逐檔核對 0、另一個代理涵蓋檢查 0。
- [ ] 站主同意後刪除已核對的分支。

## Steps

- [x] `target.py`、`admin_status.py`：新的排法與版本判斷；測試。
- [x] `backup.mjs`：合併搬移（`lsf` → 空的用 `moveto`，有檔用 `move --backup-dir _舊版/<時間>-搬移`）；測試。
- [x] compose：`VIDEO_BRANCH_MIRROR: "off"`。
- [x] 文件與 `todrive.sh`。
- [x] 叫所有製作影片的 session 不要再推分支：AGENTS.md、curio-episode、route-a、舊規則文件加停用標記，`tobranch.sh`／`coverage.sh` 改成拒絕。
- [ ] PR、站主合併與部署。
- [ ] 一次性搬家（主機跑，`gh` 讀私人 repo、主機的 rclone 寫雲端硬碟）。
- [ ] 核對、刪分支。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_backup.py
node --test tools/video/automation/backup.test.mjs
```

部署後：後台「備份位置」卡的資料夾欄位顯示 `AI劇/…`；worker log 有 `moved <舊> to AI劇/…`。

## Notes

- 對照表（132 條分支、約 158 GB）站主 2026-11-10 確認：一條多集的依路徑拆到各集、看不出集數的放 `_共用/`；
  整個 repo 副本的五條只取比 main 多的檔；`tn-series-assets` 裡的種田音效庫照搬；奇聞只用代碼不加標題。
- `zt-e9NN-media*`、`zt-e001-r2-media`、`zt-cg-e001`～`e006` 是 r2 slug 先做的 3D 重做（路徑都在 `runpod/`），歸 3D 版。
- session 寫雲端硬碟：Colab 用 `drive.mount()`；Claude Code session 用主機那把 `videobackup`（站主 2026-11-10「用同一把就好」，放雲端環境變數，不進 repo）。
  那把是整個雲端硬碟的完整權限，外洩時撤銷會連主機一起停，站主接受。
- 搬移與同一輪的複製都會用 `_舊版/<時間>/`；搬移改用 `_舊版/<時間>-搬移/`，否則複製會蓋掉搬移移進去的檔（測試抓到的）。
- 搬家（2026-11-10 01:35 UTC 起，主機 `/root/drive-migration/`）：前 45 條約每小時 4 GB，小檔多的分支被 `--tpslimit 5` 卡住；
  03:07 起主機那份改成 `--tpslimit 10 --transfers 8 --checkers 16` 重跑（帳本跳過已完成的）。repo 的 `migrate.py` 仍是保守值。
