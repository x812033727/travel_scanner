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

### 2026-11-10 上午：第 2、4 集站主看片後的修正，第 6 集首格定案

- 第 6 集首格五輪定案 27 張；拿掉 c16、c17、c20、c33、c37（共 32 鏡）。c41 是月棠站在小滿**身後**扶肩（側面相對的版本三輪都失敗），c01 托盤上只有 1 只杯：兩個都是已知瑕疵，交站主看片。
- **教訓：新機器先跑 Qwen 畫圖、再在同一台跑 H3 片段會失敗**（`ComfyUI 缺少節點：['VHS_VideoCombine']`，畫圖的筆記本裝的 ComfyUI 沒有 VideoHelperSuite，H3 的筆記本又「重用」它）。第 6 集第二批 4 支因此白跑約 3 CU。片段要在新機器或先跑過 H3 的機器上跑；畫圖可以接在 H3 後面。要寫進 `minimax-h3-colab/references/lessons.md`。
- **教訓：獨立審片要逐 0.5 秒對照音量與畫面，抓「嘴在動、在笑卻只有配樂」**。第 2 集 c18（模型讓林美鳳講了劇本沒有的話）、c33（大笑沒笑聲：精修去掉了聲音、組片只把有台詞的鏡放回原聲），第 4 集 c12、c40、c45 都是同一類，之前的審片沒抓到。沒有台詞但畫面在笑的鏡，用草稿自己的笑聲當音效（`sfx-own/<鏡>-laugh.wav`）。
- 第 2 集：拿掉 c18、c33／c34 補草稿笑聲、c10 字幕對齊 27.46 秒；獨立審片通過，10:29 匯入後台（158.7 秒）。c22、c48 兩句之間嘴微張沒聲音，判斷是笑與喘，沒有插草稿畫質的反應鏡。
- 第 4 集：獨立審片＋草稿比對，**精修沒有弄壞**（c04、c19、c29、c43、c45 草稿就是這樣）。不花錢的修正寫在 `drama-backup-tn` 的 `_scratchpad/e004-post/v2/edit-v3fix.json`；白天兩場改 lift 調色；重拍 c29、c30、c36（`session-tools/e004/fix2_stills.py`，首格路線）。站主選「免費修＋重拍 3 鏡」。
- 站主：第 2、4 集修完後新檔推回 `drama-backup-tn` 的 `transfer/tn-e002`、`transfer/tn-e004`（雲端硬碟還在搬）。這個 session 的 add_repo push 被自動權限檢查擋下，要站主放行。
