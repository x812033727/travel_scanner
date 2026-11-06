---
id: 2026-11-06-zhong-tian-e005-r2-remake-episode
title: Zhong-tian e005 r2: remake episode 5 (r2 script), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-06T20:20:03Z
created_at: 2026-11-06T20:19:58Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e905.json
---

# Zhong-tian e005 r2: remake episode 5 (r2 script), stage 2 only, zh cut for the owner

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

站主 2026-11-06：「就這樣一直做下去：完成、更新、下一集」，每集一條分支（`claude/zt-e00N-r2`）。預算**上限 US$28**。做法照第 4 集 r2。內部編號 905。

- 規格 `writer-tools/e005-r2/r2.py`（40 鏡、189.5 秒、39 句），配音已錄（中位 3.7 字／秒）；BUY s07、s24、s32、s37 8（照錄好的長度），s29 6。
- 照今天的新規則改寫：稿子的「手上沾著灰」「手上沾白色皂屑」拿掉（改寫在衣襬擦手）；c17 不寫眼裡藍光，只寫反應；只有 c36 眼睛大特寫寫瞳孔很淡的紅色反光（稿子寫紅光）。
- 秦霜這集腰帶空著（c03–c07），`extras.json` 拿掉 cast 的柴刀；灶棚沿用第 4 集寫法，對到院子場景圖，不用另畫夜景。
- `build-r2.py` 的 EN 表加 `laisan`（賴三）。免費檢查 0 error、0 warning。

- [x] 規格、配音、免費檢查
- [ ] 第一段草稿（每鏡兩個種子），挑片
- [ ] 第二段精修
- [ ] 剪接、cut-qa、量成片
- [ ] `import --from`，備註「第 5 集重製版 r2」
