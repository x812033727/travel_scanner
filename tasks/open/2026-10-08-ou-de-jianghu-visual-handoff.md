---
id: 2026-10-08-ou-de-jianghu-visual-handoff
title: 《偶的江湖》角色資產鎖定與第一集動畫試播交接
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T10:52:24Z
completed_at:
branch:
depends_on:
  - 2026-10-08-ou-de-jianghu-animation-reference
  - 2026-10-08-ou-de-jianghu-scene-prop-design
  - 2026-10-08-ou-de-jianghu-external-look-import
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/handoff
  - docs/videos/series-plans/ou-de-jianghu/production/README.md
---

# 《偶的江湖》角色資產鎖定與第一集動畫試播交接

## Why

把採用圖、參照和正常look綁到同一來源，第一集試播才能沿用同一張臉；production README仍寫過期14人。

## Definition of done

- [ ] 9人資產manifest含來源commit／SHA、角色／look ID、用途、版本、媒體hash、judge與站主接受狀態；額外綁shot_looks目錄hash，不冒稱原生lookHash已有。
- [ ] 經正式匯入走正常look／choice／series-store；用少量已授權關鍵影格核對真正讀入的reference及當鏡造型文字，保存實際結果，不假填。
- [ ] 劇本／look／audio／storyboard／plan lock分別列；前期畫像完成不等於動畫完成。完成原持有人交接後更新production README，將前置條件接回既有試播票，保留連續三鏡及站主接受後放量。

## Steps

- [ ] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [ ] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [ ] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

第8集持有人占production scope，不能強行claim／覆寫。本輪未改既有試播票depends_on；接線仍待辦，要改它時先將精確路徑加入scope並完成所有權交接。後續14人／16狀態按同流程分批，不阻塞第一集。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
