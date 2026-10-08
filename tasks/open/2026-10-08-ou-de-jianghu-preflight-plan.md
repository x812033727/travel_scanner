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
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-visual-preproduction
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan
---

# 《偶的江湖》第1集開拍前置包：文字動態分鏡、路線與美術預算

## Why

已有第1集劇本及 Hailuo 試播票；角色設定圖、配音與動畫的分項预算及 P0–P7 尚未集中。

## Definition of done

- [x] 完成 P0–P7 可審閱包：條件卡、現有劇本及關卡盤點、分場與鏡位、風險、文字卡 animatic、獨立觀看紀錄與連續三鏡小樣計畫。P7正式採用另列下項；觀看方法限制如實保留。
- [x] 將本批角色畫像／動畫參照納入分項期望、上限、預留及take上限，報價附當日來源；核對 production profile 與 Hailuo 匯入相容性。
- [ ] 整理可審閱鎖定包並記錄站主對具體包的決定；實際確認後才寫正常 plan lock，未核准不啟動付費生成；已有效授權則沿用原證據。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [x] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [x] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

2026-10-09 00:03（Asia/Taipei）最後文件補訂：依主控授權重新認領本票，只更新本scope的v3說明及離線基線入口。74張新增角色參照與29張場景／道具已交付候選，現鏈實物收據；預算的一次／期望／上限仍保留原規劃數，不冒稱實際生成或帳單。正常look明列每角色一張基底，其餘參照按鏡提供並驗SHA。首次offline-preflight加歷史基線標示，v3移除整案「未commit／push」推斷；Git交付由主控另記。本代理未執行commit、push或付費操作，未改核心video／animatic／台詞／時間／預算；檢查結果見[自己的驗證收據](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/package-verification.json)之documentation_refresh。下列2026-10-08 Notes均為當時的交付紀錄，不覆蓋本次狀態；正式採用DoD仍未勾，完成補訂後release。

2026-10-08續作交付：[P0–P7審閱包v3](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/preproduction-package-v3.md)、[455鏡ledger](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/camera-and-risk-ledger.json)、[分項／兩期預算](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/budget-and-batches.json)。有來源SHA保護的可執行builder，未改e001／production；原10C逐鏡裁定，掌冠s036人工C、s037藏印首格與露印末格已修。實際setup 447→343；420clip／30still／5cut。當日Hailuo／Google費率已查，帳戶一次可見27000不當未来餘額或付款授權。已在另一repo外目錄重建，六份核心產物SHA相同。

獨立代理v3從14:57:29.189Z播至15:20:53.239Z：全長1倍速、373卡即時觀察＋86卡停格補看，459卡全覆蓋；如實保留工具觀察間隙及AX預曝全表限制，不稱完全盲看。其發現still通用句缺資訊，v3.1只補原首格／末格卡面、資料逐byte不變；23卡獨立停格複看已驗主要線索可讀，非第二次全長。[獨立報告](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/cold-review-independent.md)與[呈現收據](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/presentation-review.json)保存證據。舊v2真實15.7秒播放器故障與上游HTML保留，共用源修復另有 [精確追蹤票](2026-10-08-animatic-title-gap-subtitle-boundary.md)，本scope wrapper已修。

真實check：lint0、shot_reading strict0；craft strict1僅三反應列（逐列理由已寫）；shot_plan strict1僅整集期望超單月，兩期每期上限＋10%各≤27000的算術assert0；ready1為1過／429後續媒體項尚未到位。P0–P7包已形成，不能因尚無TTS／首格把前期永遠判未做，也不能反過來寫假媒體關卡。具體包尚待站主整體採用，故本票第三DoD維持未勾、未寫native lock、未送任何付費provider請求，未commit／push。

2026-10-08 部分交付：[分場與小樣](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/scene-and-pilot.md)、[離線檢查](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode-plan/offline-preflight.md)。已生成455鏡文字卡animatic與分鏡JSON/Markdown、readiness真實診斷。P3仍447組setup／455鏡；掌冠接觸與分髮露胎記的前後狀態需修，10個程式C級須人工裁定。費率僅歷史常數，未補齊即時全包預算、未完成animatic冷看或plan lock，因此三項DoD維持未勾。來源及既有e001/production持有人檔案未改。美術方向接受及九人概念先行已另有票記錄，不能當完整開拍核准。本輪結束release，不標完成。

依 animation-preproduction 執行離線 shot_plan、shot_reading、craft、animatic、plan_lock --ready。先文字前置包，再角色圖，再正式關鍵影格與動畫；不要因圖尚未生成偽造關卡。不重写e001或接管既有試播票。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
