---
id: 2026-10-08-ou-de-jianghu-art-direction
title: 《偶的江湖》角色美術定調：三位主角候選與共同畫風
status: done
priority: P1
area: docs
owner: codex-ou-de-jianghu-art
claimed_at: 2026-10-08T11:03:16Z
created_at: 2026-10-08T10:52:15Z
completed_at: 2026-10-08T12:35:45Z
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-preflight-plan
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/art-direction
---

# 《偶的江湖》角色美術定調：三位主角候選與共同畫風

## Why

把人設轉成可比較的視覺基準，先用不同輪廓的三人定調，再擴到全體。

## Definition of done

- [x] 以沈歸鶴、姬無霜、寂聞做少量候選；服從 character-design.md 的原創2D武俠、臉部／冠髮／服裝錨點，候選數依前置包。
- [x] 一致背景、光線和構圖比較臉型、線條、明暗、布／金屬材質與裝飾密度；保存實圖、prompt、來源／媒體SHA及未採用理由。
- [x] 提供並排包，完成獨立視覺審查及站主對採用方向的實際接受紀錄；生成、審查、接受與正常look核准分開記。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [x] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [x] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

2026-10-08 完成：[定調成果](../../docs/videos/series-plans/ou-de-jianghu/visual-development/art-direction/README.md)、獨立實圖審查、prompts 與 media-receipt 已保存；三人共5 PNG（3目前候選、2早期版本），來源12檔SHA未改，圖冊保存在repo外。使用者原話「保留目前華麗古裝與細緻人物風格」只接受共同方向。本票以美術方向定調結案；合扇、手足、冠鏈/衣紋母版和正式27視圖等仍在 episode1-portraits 任務，未把它們勾成完成。內建工具未回傳帳單，不宣稱成本為零。

2026-10-08 站主在前期包交付後說「開始」。本次先以內建 imagegen 做沈歸鶴、姬無霜、寂聞各一張概念候選，不呼叫 Hailuo、正式站圖片／動畫API、TTS 或影片judge。前置包仍在製作，故使用 --force 只提前進行這個有界的概念比較；未替整集寫 plan lock、不把「開始」當成整集預算或look核准。剩餘候選、採用、外部製作與全季擴量仍依正常前置與接受流程。

不將後期傷勢、武器、胎記常露或偽裝混入第一集。媒體與私有收據留repo外；沒有圖不能標定調完成。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
