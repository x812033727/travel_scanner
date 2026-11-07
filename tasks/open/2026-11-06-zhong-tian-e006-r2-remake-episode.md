---
id: 2026-11-06-zhong-tian-e006-r2-remake-episode
title: Zhong-tian e006 r2: remake episode 6 (r2 script), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-06T23:19:44Z
created_at: 2026-11-06T23:19:43Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e906.json
---

# Zhong-tian e006 r2: remake episode 6 (r2 script), stage 2 only, zh cut for the owner

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

站主 2026-11-06：「就這樣一直做下去：完成、更新、下一集」，每集一條分支。預算**上限 US$28**。做法照第 5 集 r2。內部編號 906。

- 規格 `writer-tools/e006-r2/r2.py`（40 鏡、194.7 秒、41 句），配音已錄（中位 3.7 字／秒；錢員外兩句重錄一次，第一次 10.6 秒太拖）。
- 場景：院子 `set-xujia-yuan-t1`、縣衙 `set-xianya-t1`、市集 `set-shiji-t1`（第一季的圖，不另畫）；市集的茶樓寫成「tea house」，免得對到 `set-chalou-t1`。
- BUY：s09 10、s12/s25/s35/s36 8（長鏡）、s40 12、s38 10、s14 8。
- 照新規則：c01 手上的皂屑拿掉；婚書永遠摺著或背面朝鏡頭，印只有一塊紅印、沒有字；錢員外的白瓷小酒杯寫成白陶小杯。
- 免費檢查 0 error、0 warning。

- [x] 規格、配音、免費檢查
- [ ] 第一段草稿（每鏡兩個種子），挑片
- [ ] 第二段精修
- [ ] 剪接、cut-qa、量成片
- [ ] `import --from`，備註「第 6 集重製版 r2」
- 第 6 集的草稿開抽前規格還沒有 smile 檢查：s02、s04、s23、s29、s37 唐小棠只寫了 unsmiling，挑片時特別看，在笑就照第 5 集的寫法重抽。
- 2026-11-07 04:30 草稿 80 支抽完。新流程第一次用：挑片交給獨立審片代理（每鏡兩個種子的整段格子對照稿子），26 鏡選定（`colab/runs/e906/picks.tsv`、`review-picks.tsv`），14 鏡兩支都不行要重抽：
  s01、s06、s07 等秦霜出現兩次；s02、s04、s23、s29、s37 唐小棠在笑（preflight smile 事先標的正是這 5 鏡），s29 一支立領下開口；s21、s30 婚書變白紙；s35、s36 市集攤子沒釘木板、告示轉正露假字、皂像高麗菜；s27、s28 紅紙包變軟枕／紅包；s16 紅布沒斜綁胸前。
  跨鏡要統一的寫成常數：紅布斜綁胸前、婚書紅紙、白皂、紅紙包、攤子釘木板、髮邊紅紙花、「只有一個秦霜」。改寫交給子代理（`colab/runs/e906/fix1`）。裁剪：s15 約 4 秒、s17 5.2 秒前、s22 最後 0.5 秒、s34 約 4 秒。
