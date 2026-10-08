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
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-episode1-portraits
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference
---

# 《偶的江湖》第一集角色動畫參照：多視圖、表情與動作

## Why

畫像只固定一個角度；轉頭、側身、抬手還需要一致的幾何及表演參照。

## Definition of done

- [x] 9人各有正／背／左右側／左右3/4候選多視圖及同尺度板；沿用9張正面，不用水平翻圖偽造不對稱造型。作為2D/I2V參照，部分姿勢／透視差異已記錄，未宣稱正交轉台。
- [x] 每人表情表、典型姿態準備／動作／收勢、手／袖口／冠飾／識別道具細節，另有9人同尺度與剪影對照；殷無聲保留不能說話設定。皆為候選，未宣稱連續動畫已驗收。
- [ ] 逐張核對臉、左右、層次和道具數量，綁定採用畫像hash及實際接受狀態；標animation_reference_ready，不能宣稱rigged或動畫已驗收。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [x] 完成候選交付項，將實際證據及未決問題記入本票 scope 的成果文件；正式採用條件另列。
- [x] 實看、修訂及獨立覆核範圍已保存；正式採用未完成，release保留待辦，不寫animation_reference_ready=true。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

2026-10-09收尾：已交74張新增latest候選＋9張沿用正面，共83項用途。保留90個PNG檔，89張唯一生成圖，1個同圖別名；另有2次九參照圖請求在驗證階段被拒、3份未執行且已替換的提示草稿，未當成生成成功。姬左右霜印／背髮、包的頭向、燕持刀手與多臂、沈扇多餘飾件、長老冠留白及動作桌面等修訂均留原版。母圖及12來源SHA相符。獨立覆核實看39張版本，並非冒稱每張均由兩人覆核；全部latest由生成負責者實看。83圖解碼、9人篩選、放大、手機版與跨冊連結已過。見 [交付與限制](../../docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/README.md)、[媒體收據](../../docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/media-receipt.json)、[review](../../docs/videos/series-plans/ou-de-jianghu/visual-development/animation-reference/review.md)。剩餘為個別採用、白扇母版統一及正式動畫關卡；不重買已完成候選。

- 2026-10-08 續做：依站主「好 續繼都完成」，以現有27張畫像為候選來源平行補齊動畫參照；claim --force 僅略過尚待個別採用的畫像相依，沒有宣稱畫像已正式核准。所有新圖保持候選及來源 SHA，原圖不刪除。

本票交2D/I2V參照，不假稱分層骨架或3D模型。實際生成遵循前置包與候選預算。

- 2026-10-08建票快照：當時依站主「先補齊任務、造型規格與畫像製作清單」新增待辦，尚未生成或核准媒體；後續候選交付見2026-10-09紀錄。沒有部署或發布。
