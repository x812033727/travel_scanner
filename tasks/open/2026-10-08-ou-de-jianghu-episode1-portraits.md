---
id: 2026-10-08-ou-de-jianghu-episode1-portraits
title: 《偶的江湖》第一集9位角色畫像與全身定妝
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T10:52:17Z
completed_at:
branch:
depends_on:
  - 2026-10-08-ou-de-jianghu-art-direction
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/episode1-portraits
---

# 《偶的江湖》第一集9位角色畫像與全身定妝

## Why

第一集9人都需要固定身份，僅主角海報不足以接續動畫。

## Definition of done

- [ ] 9人齊：沈歸鶴、姬無霜、寂聞、包三錢、殷無聲、燕迴、聶孤鐵、玄門長老、洛青衍；每人中性正面頭像、3/4半身畫像及完整全身定妝。
- [ ] 三位主角沿用定調採用臉，其他6人同風格；冠、鞋足、衣擺與必要道具完整，不同視圖同臉同衣裝；27份採用用途是規劃數，並非生成次數。
- [ ] 逐人保存圖檔／來源SHA、候選與接受狀態；說書人不畫肖像，黑風不使用褚無常正臉，不自行寫runtime manifest。

## Steps

- [ ] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [ ] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [ ] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

採用 production-list.md 的規格和asset-inventory.json清單。圖片需逐張打開檢查，不能以prompt或生成成功代替。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
