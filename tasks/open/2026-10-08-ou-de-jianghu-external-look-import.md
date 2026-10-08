---
id: 2026-10-08-ou-de-jianghu-external-look-import
title: 《偶的江湖》角色設定圖外部匯入：採用畫像接入正常look與跨集參照
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-08T10:52:23Z
completed_at:
branch:
depends_on:
  - 2026-10-08-ou-de-jianghu-visual-preproduction
scope:
  - tools/video/media/look.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/series-store.mjs
  - tools/video/media/series-store.test.mjs
  - tools/video/cli.mjs
  - docs/videos/series-plans/ou-de-jianghu/visual-development/import-contract
---

# 《偶的江湖》角色設定圖外部匯入：採用畫像接入正常look與跨集參照

## Why

目前look沒有PNG匯入；--file讀video.json，sheetPrompt只使用base appearance。外部採用圖還不能被證明進入實際動畫流程。

## Definition of done

- [ ] 設計及實作窄範圍base角色設定圖匯入：明確分開專案JSON與PNG參數，驗角色、格式／尺寸、來源及媒體hash，不悄悄觸發生成。
- [ ] 走正常look judge／選用／核准／series-store，保留來源；不手寫通過分數或繞過關卡。同hash安全重跑，換圖／appearance／style時舊核准與下游正確失效。
- [ ] 測試非法角色／壞檔、重跑去重、hash變更失效、跨集reuse及reference選取；清楚寫明shot_looks仍為文字覆寫，沒有每造型獨立圖像引用。

## Steps

- [ ] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [ ] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [ ] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

執行 Notes 所列測試及相關 tools 檢查。

`npm run check:tasks`

## Notes

可用離線測試圖與美術並行。驗證：node --test tools/video/media/look-keyframes.test.mjs tools/video/media/series-store.test.mjs，及相關tools檢查。新增檔/schema/API前先擴窄scope及查碰撞，不顺手擴成多參考架構；本輪只開票。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
