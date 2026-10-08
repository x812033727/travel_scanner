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
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-animation-reference
  - 2026-10-08-ou-de-jianghu-scene-prop-design
  - 2026-10-08-ou-de-jianghu-external-look-import
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/handoff
---

# 《偶的江湖》角色資產鎖定與第一集動畫試播交接

## Why

把採用圖、參照和正常look綁到同一來源，第一集試播才能沿用同一張臉；production README仍寫過期14人。

## Definition of done

- [x] 9人資產manifest含來源commit／SHA、角色／look ID、用途、版本、媒體hash、judge與站主接受狀態；額外綁shot_looks目錄hash，不冒稱原生lookHash已有。
- [ ] 經正式匯入走正常look／choice／series-store；用少量已授權關鍵影格核對真正讀入的reference及當鏡造型文字，保存實際結果，不假填。
- [ ] 劇本／look／audio／storyboard／plan lock分別列；前期畫像完成不等於動畫完成。完成原持有人交接後更新production README，將前置條件接回既有試播票，保留連續三鏡及站主接受後放量。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [x] 完成可審交接文件，將實際證據及未決問題記入本票 scope；正式採用／正常runtime與原持有人接線仍保留待辦。
- [x] 候選實看與獨立核對範圍、匯入收據、SHA及圖冊驗證已整合；正式製作條件尚未滿足，收尾release。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

2026-10-09收尾：[交接包](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/README.md)與 [asset-manifest](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/asset-manifest.json)已備妥。12來源SHA、139張唯一latest候選（9概念＋27畫像＋74新角色參照＋29場景道具）、9張正面沿用關係、16種shot_looks獨立hash、9張隔離pending匯入及16份交付來源文件SHA已核對。正常lookHash為9b3e6914dbc8d109，僅來自隔離工作提案，不冒稱涵蓋shot_looks或正常runtime。455鏡v3／v3.1、全長文字animatic觀看、兩期預算及a02-s035～s037連續小樣計畫可直接審。白扇母版、紙窗近景、棋盤、原生尺寸及23:23.533估時差異均明列。剩餘兩DoD保留：正式個別採用／judge與正常關卡、當鏡真實參照驗證，以及production／原試播票持有人交接；沒有paid動畫或假approval。

- 2026-10-08 續做：本票 scope 收窄為 handoff/，先完成可審閱的第一集交接包；production/README.md 的原持有人交接及正式 runtime 選用/付費小樣仍列待辦，不占用其 scope。who-is-on-it 對 handoff/ 查無 active claim 或其他 PR。依站主「好 續繼都完成」授權，使用 --force 僅略過同一分工中尚未結案的三張相依票，並非覆蓋別人持有者、預算或站主接受。

第8集持有人占production scope，不能強行claim／覆寫。本輪未改既有試播票depends_on；接線仍待辦，要改它時先將精確路徑加入scope並完成所有權交接。後續14人／16狀態按同流程分批，不阻塞第一集。

- 2026-10-08建票快照：當時依站主「先補齊任務、造型規格與畫像製作清單」新增待辦，尚未生成或核准媒體；後续交付見2026-10-09紀錄。沒有部署或發布。
