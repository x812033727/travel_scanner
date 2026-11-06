---
id: 2026-11-06-zhong-tian-e004-r2-remake-episode
title: Zhong-tian e004 r2: remake episode 4 (r2 script), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-06T14:20:39Z
created_at: 2026-11-06T14:20:36Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e904.json
---

# Zhong-tian e004 r2: remake episode 4 (r2 script), stage 2 only, zh cut for the owner

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

站主 2026-11-06：「就這樣一直做下去：完成、更新、下一集」，每集一條分支（`claude/zt-e00N-r2`）。預算照第 2、3 集，**上限 US$28**。做法照第 3 集 r2。內部編號 904。

- 規格 `writer-tools/e004-r2/r2.py`（40 鏡、194.8 秒、40 句），配音已錄（中位 3.5 字／秒）；BUY：s03、s13、s37 長鏡 8，s10、s35 8，s14 12、s15 10（照錄好的長度）。
- `colab/runs/e904/extras.json`：秦霜這集柴刀回到腰帶，不拿掉；二牛 c27–c28 背著大鍋，拿掉 cast 的「empty-handed」，每鏡構圖自己寫手上拿什麼。
- 黑影（s38、s40）沒有定妝照、不寫名字，只寫背光、臉在暗處。
- 免費檢查 0 error、0 warning。

- [x] 規格、配音、免費檢查
- [ ] 第一段草稿（每鏡兩個種子），挑片
- [ ] 第二段精修
- [ ] 剪接、cut-qa、量成片
- [ ] `import --from`，備註「第 4 集重製版 r2」
- 草稿挑片時看到兩種新錯：s03 兩支開頭都畫出發光的系統面板（正文寫「面前空氣的淡藍光、不畫面板」）；s24 一支跳成中景、眼睛發藍光。s03 用 9040101 從 1.5 秒起剪（避開面板），s24 用 9040102（眼睛大特寫）。
  教訓落地：`storyboard-shot-spec.md`、`storyboard-brief-for-planners.md` 加一行；`preflight-prompts.py` 加 warn glow（第 2–4 集舊 prompt 會擋到 e903 s20、e904 s03）。
