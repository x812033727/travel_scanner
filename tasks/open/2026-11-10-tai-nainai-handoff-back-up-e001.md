---
id: 2026-11-10-tai-nainai-handoff-back-up-e001
title: tai-nainai handoff: back up e001-e005 production files to Drive, then shoot episode 6
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-10T06:56:17Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/session-tools
---

# tai-nainai handoff: back up e001-e005 production files to Drive, then shoot episode 6

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Context
The session that made 《恁祖媽今年18》 episodes 1–5 ended on 2026-11-10. Read
`docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/session-tools/README.md` first.

- Episodes 1–5 are imported and wait for the owner at /admin/videos.
- Their production files were never copied to Google Drive (the old session could not read the rclone variables).
  Their latest copies are on the retired backup branches in `drama-backup-tn`; the host is moving those branches to Drive.
  Branches `transfer/tn-e001`, `tn-e004`, `tn-e005`, `tn-shared` match the final local files (independently checked).
  `transfer/tn-e002` and `transfer/tn-e003` are older than the final local files (e002: about 34 files — the new c15 take,
  the v3 cut and the import folder; e003 not checked). Whatever the old session decided about those is recorded below.
- Episode 6 is storyboarded and reviewed (37 shots) and nothing has been spent; the prepared manifests are in `session-tools/e006/`.
- Cap from episode 6: 40 CU (owner 2026-11-10).

- [ ] confirm the host migration put `transfer/tn-e00N` and `tn-shared` under `AI劇/恁祖媽今年18/` on Drive
- [ ] episode 6: pictures → stills → clips → pick → fix → refine → cut → review → import → todrive.sh

## 2026-11-10 第 6 集進度（接手的 session）

- 站主 2026-11-10：**第 6 集上限放寬到 55 CU**（首格兩輪後 28 張只定 22 張、已用 10.7 CU 時問的；選「上限再放寬到 55 點」）。RULES.md 第四節在 #2047 分支，合併後補一列。
- 場景圖：正廳白天 zt-day-2、飯廳 fanting-1、托盤 tray-1，已進 `assets/refs/`（舊飯廳在 `assets/refs/orig/`）。
- 首格：第一輪 56 張定 17 鏡，第二輪（`redo_stills.py`）22 張定 5 鏡，第三輪（`redo3_stills.py`，c41 從 c38 修圖）6 鏡各三個種子。挑圖都交獨立代理。
- 整集反覆的錯：飯廳燈畫成紅流蘇燈籠、鐘面數字、月棠臉太正面、前景虛焦肩膀寫在句尾就畫不出來、眼淚畫成紅色。
- CU：場景圖＋首格第一輪 7.54、第二輪 2.34（含關機後補扣 0.82），累計 10.70（2384.25 → 2373.55）。
- 錄音 25 句在 `$TN_WORK/e006voice/`（只有 t006012 用錄音，其餘用原聲）。
