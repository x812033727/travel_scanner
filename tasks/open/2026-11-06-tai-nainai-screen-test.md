---
id: 2026-11-06-tai-nainai-screen-test
title: 祖奶奶今年十八 角色與試鏡：Colab 真人與 3D 試鏡、聲音試聽
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5
claimed_at: 2026-11-06T14:24:38Z
created_at: 2026-11-06T14:24:37Z
completed_at:
branch: claude/intelligent-gates-9n92xm
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/screen-test
---

# 祖奶奶今年十八 角色與試鏡：Colab 真人與 3D 試鏡、聲音試聽

## Why

《祖奶奶今年十八》第一季的 `cast.json` 寫的是真人電影感（photorealistic live-action），但 repo 裡還沒有任何一次真人風格的實測：
《種田》在 Colab 做過整季的是 3D CG，而且 Qwen-Image-Edit 的首格臉到不了定妝照的質感。站主 2026-11-06 要先評估真人劇再開角色，
同意的試鏡：Colab 上畫四個角色的定妝照（真人，另畫一版 3D 對照），用第 1 集的鏡頭跑 Ref2VA 三段式片段，再用站台試聽月棠的聲音。
過了才畫全季 30 個角色；沒過退回 3D CG 路線。

## Definition of done

- [ ] 站主看過試鏡結果，定下畫風（真人或 3D）與月棠兩個聲音，寫進這張票，bible〈要站主決定的〉另開改單。
- [ ] 試鏡的提示詞、seed、每段 CU 與取捨留在 `production/screen-test/`，選中的定妝照可以給下一個 session 用。

## Steps

- [x] 影片工具權杖配對（route C，`login --colab`，2026-11-06 站主允許），`bootstrap.sh` 驗 `colab usage`：餘額 68.31 CU。
- [ ] `screen-test/build.py`：從 `cast.json` 產生各輪 manifest 與提示詞；離線 `images-check`、`h3.sh check` 過。
- [ ] 第一輪定妝照：真人 月棠（壽衣）、林美鳳、福伯各兩個 seed，祠堂、正廳；3D 對照各一張。
- [ ] 第二輪：以選中的十八歲為 image 1 畫九十六歲（一人兩貌）；手背細紋插鏡。
- [ ] 片段：第 1 集 c14（林美鳳說話）、c17（九十六歲閉眼）、c20（看手、戒指）、c23（十八歲近景）真人四支，c14 的 3D 一支；Ref2VA 960×544 hero → σ0.5 → SeedVR2 7B。
- [ ] 聲音試聽：月棠十八歲 Kore／Despina／Achernar、九十六歲 Gacrux 等；`cli.mjs audition`。
- [ ] 冷看一次，交站主。

## How to verify

```bash
python3 -I docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/screen-test/build.py r1 --placeholders
bash .agents/skills/minimax-h3-colab/scripts/h3.sh images-check --manifest <work>/r1.json
```

## Notes

- 預估（推算，未實測）：G4 約 8 CU／小時；整個試鏡約 1.5 小時、10–14 CU。花 CU 前後抄 `h3.sh usage`。
- Colab 出圖至少要一張參考圖，這部還沒有定妝照：第一輪用一張空白灰底當 image 1（沒試過，先 `--only` 兩張驗）。
- 分支疊在 PR #2030（`claude/confident-galileo-vfq0j3`）上，要 #2030 先合。
