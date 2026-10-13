---
id: 2026-10-08-ou-de-jianghu-supporting-looks
title: 《偶的江湖》後續角色畫像、16種命名造型與隱藏身份清冊
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-08T10:52:20Z
completed_at:
branch:
depends_on:
  - 2026-10-08-ou-de-jianghu-art-direction
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/supporting-looks
---

# 《偶的江湖》後續角色畫像、16種命名造型與隱藏身份清冊

## Why

cast已有19人和16種命名造型，setting另有5人未進cast；需要按出場及狀態分批，不提早劇透。

## Definition of done

- [ ] 按清單分批補第一季尚餘14人的畫像及動畫參照；setting-only角色須由當集主編確認當時外觀，不把後期狀態回灌cast。
- [ ] 16種shot_looks逐一做base→variant差分圖，保留同臉／角色ID；寫適用集鏡、持物、傷勢、禁用狀態與來源hash。
- [ ] 另列姬無霜鬼燈偽裝、胎記、手背印和化身淡影等shot prompt細節；褚無常第二季正臉延期、第一集黑風另列，不自動加ID或露真面目。
- [ ] 對照 character-design.md 第6節逐項追蹤尚缺造型：第一季後段的白髮／重生／合魂／持劍交接、岳嵐宮主装；第二季旅行、腕繩、禁武器、布繩束髮、路塵與腰帶分開排期。每項列所需劇本決定及交付狀態；未決項保留本票未完成，不能漏到聊天裡。

## Steps

- [ ] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [ ] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [ ] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

24人union完整覆蓋：第一季23人＋第二季保留1人。第8集劇本及傳單知情已有票，不重開、不假填核定。後續角色不阻塞第一集9人交付。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
