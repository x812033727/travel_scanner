---
id: 2026-10-08-ou-de-jianghu-preflight-plan
title: 《偶的江湖》第1集開拍前置包：文字動態分鏡、路線與美術預算
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T10:52:14Z
completed_at:
branch:
depends_on:
  - 2026-10-08-ou-de-jianghu-visual-preproduction
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan
---

# 《偶的江湖》第1集開拍前置包：文字動態分鏡、路線與美術預算

## Why

已有第1集劇本及 Hailuo 試播票；角色設定圖、配音與動畫的分項预算及 P0–P7 尚未集中。

## Definition of done

- [ ] 完成 P0–P7：條件卡、現有劇本及關卡盤點、分場與鏡位、風險、文字卡 animatic、獨立冷看與連續三鏡小樣計畫。
- [ ] 將本批角色畫像／動畫參照納入分項期望、上限、預留及take上限，報價附當日來源；核對 production profile 與 Hailuo 匯入相容性。
- [ ] 整理可審閱鎖定包並記錄站主對具體包的決定；實際確認後才寫正常 plan lock，未核准不啟動付費生成；已有效授權則沿用原證據。

## Steps

- [ ] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [ ] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [ ] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

依 animation-preproduction 執行離線 shot_plan、shot_reading、craft、animatic、plan_lock --ready。先文字前置包，再角色圖，再正式關鍵影格與動畫；不要因圖尚未生成偽造關卡。不重写e001或接管既有試播票。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
