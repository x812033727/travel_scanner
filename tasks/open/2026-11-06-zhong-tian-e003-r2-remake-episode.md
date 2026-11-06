---
id: 2026-11-06-zhong-tian-e003-r2-remake-episode
title: Zhong-tian e003 r2: remake episode 3 (r2 script), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-06T06:12:58Z
created_at: 2026-11-06T06:12:57Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e903.json
---

# Zhong-tian e003 r2: remake episode 3 (r2 script), stage 2 only, zh cut for the owner

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

站主 2026-11-06：「就這樣一直做下去：完成、更新、下一集」，每集一條分支（`claude/zt-e00N-r2`）。預算照第 2 集，**上限 US$28**，超過先停下來回報。
做法照第 2 集 r2（`tasks/open/2026-11-06-zhong-tian-e002-r2-remake-episode.md`）。內部編號 903，`docs/videos/zhong-tian-qu-qi-e903` 是本機連結。

- 規格 `writer-tools/e003-r2/r2.py`（40 鏡、185 秒、35 句），配音已錄（中位 3.6 字／秒，所以 s04、s07、s08、s11、s13、s15 買 8 秒、s21 8、s22 10）。
- `colab/runs/e903/extras.json` 多一條：拿掉秦霜 cast 裡「腰帶插柴刀」，因為第 3 集開頭柴刀釘在門框上（s02、s03、s16 腰帶空著，s29 插回去）。
- 免費檢查 0 error、0 warning。

- [x] 規格、配音、免費檢查
- [ ] 第一段草稿（每鏡兩個種子），挑片
- [ ] 第二段精修
- [ ] 剪接、cut-qa、量成片
- [ ] `import --from`，備註「第 3 集重製版 r2」
- 2026-11-06 08:03 草稿開跑；容器約 08:20 前後重啟，跑完 4 支就斷，pod 空轉到被站台 60 分鐘停掉（約 US$2.6 白花）。10:30 重跑（已有的跳過），EU-CZ-1 沒貨，`scratchpad/chain903d.sh` 最多等 8 小時，抽完接真人版試拍的定妝照（同一個 pod）。
