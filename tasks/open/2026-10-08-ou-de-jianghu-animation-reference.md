---
id: 2026-10-08-ou-de-jianghu-animation-reference
title: 《偶的江湖》第一集角色動畫參照：多視圖、表情與動作
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T10:52:18Z
completed_at:
branch:
depends_on:
  - 2026-10-08-ou-de-jianghu-episode1-portraits
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference
---

# 《偶的江湖》第一集角色動畫參照：多視圖、表情與動作

## Why

畫像只固定一個角度；轉頭、側身、抬手還需要一致的幾何及表演參照。

## Definition of done

- [ ] 9人各有正／背／左右側／左右3/4多視圖，統一足底線與比例；可複用合格視圖，不用水平翻圖偽造不對稱造型。
- [ ] 每人表情表、典型姿態準備／動作／收勢、手／袖口／冠飾／識別道具細節，另有9人同尺度與剪影對照；殷無聲保留不能說話設定。
- [ ] 逐張核對臉、左右、層次和道具數量，綁定採用畫像hash及實際接受狀態；標animation_reference_ready，不能宣稱rigged或動畫已驗收。

## Steps

- [ ] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [ ] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [ ] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

本票交2D/I2V參照，不假稱分層骨架或3D模型。實際生成遵循前置包與候選預算。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
