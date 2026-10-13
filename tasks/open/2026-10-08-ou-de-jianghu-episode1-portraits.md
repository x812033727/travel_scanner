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
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-art-direction
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/episode1-portraits
  - docs/videos/series-plans/ou-de-jianghu/visual-development/README.md
---

# 《偶的江湖》第一集9位角色畫像與全身定妝

## Why

第一集9人都需要固定身份，僅主角海報不足以接續動畫。

## Definition of done

- [x] 9人齊：沈歸鶴、姬無霜、寂聞、包三錢、殷無聲、燕迴、聶孤鐵、玄門長老、洛青衍；每人中性正面頭像、3/4半身畫像及完整全身定妝候選。已完成27張生成與實看覆蓋；正式採用及規格差距仍在下一項。
- [ ] 三位主角沿用定調採用臉，其他6人同風格；冠、鞋足、衣擺與必要道具完整，不同視圖同臉同衣裝；27份採用用途是規劃數，並非生成次數。
- [x] 逐人保存圖檔／來源SHA、候選與接受狀態；說書人不畫肖像，黑風不使用褚無常正臉，不自行寫runtime manifest。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [ ] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [x] 依驗收要求獨立核對本輪候選；完成才 done，停止則 release，不把待執行標為完成。完整採用條件尚未滿足，仍保留本票。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

2026-10-09 第二次續作：沈歸鶴白扇修訂選全身 v3、半身 v2、概念 v5；完整原件及提示保留，現行 27 視圖＋9 概念 SHA 另列 finalized-views-receipt.json，舊收據不覆寫。18 張低於舊建議長邊的圖已限定作身份／服裝參照，PNG 原生尺寸與格式均有效；不以放大或尺寸建議充作正式影格驗收。概念小全身的拳下細線仍不可判接點，不能作扇拓撲母版；白扇結構固定到兩張清楚細節／道具圖。根總覽同步現行 146 張與 v4 入口。剩餘個別採用／正常 look 核准不代填，本票 release 留待該關卡。

2026-10-09收尾：27張獨立候選本輪沿用，未重買；側背面／表情／動作／細節與同尺度板已另由動畫參照票補齊。9張全身原圖實際隔離pending匯入、重跑去重及SHA通過，未產生judge／choice／正式look核准。根README已整合最新139張候選清冊與歷史快照界線。個別採用、18張半／全身尺寸差距及沈白扇母版統一仍留本票／交接票，不以畫風接受冒充完成；收尾release。

### 2026-10-08 續作：27 張獨立視圖

使用者「繼續」後，沿既有概念參照分別生成九人各三視圖，共27張；另修正殷無聲、燕迴、洛青衍的半身指尖裁切，保留三張舊版，共30個原生PNG。已逐張實看30版本，最新版27張完整覆蓋9人×3。詳見[獨立視圖交付清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode1-portraits/independent-views.md)、[三主角審查](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode1-portraits/independent-main-review.md)、[六配角及v2覆核](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode1-portraits/independent-supporting-review.md)。

媒體在 `<VIDEO_WORKDIR>/ou-de-jianghu-e001/portraits/20261008/`，圖冊 `gallery.html` 展示27張目前候選。30份提示、30媒體SHA、參照圖與12個來源檔SHA均保留並交叉核對；沒有從拼板裁切充數，也未修改production/e001來源。姬的雙手／雙鞋與三張半身指尖已補清楚，殷的完整劍鞘仍待側後／背面圖。

規格：9頭像1254×1254；沈／姬半身1003×1568，較建議4:5窄长；其餘7半身1122×1402約4:5；9全身1024×1536。18張半身／全身低於原編輯建議長邊，未放大冒充原生尺寸。共同風格已接受，個別臉與服飾細節、尺寸／留白差距及正式採用仍未決；不勾第二驗收項，不寫runtime manifest或approval。後續先固定採用母版及輸出用途，再沿動畫參照票補側背面、表情、手與道具，不重複生成已有27份候選。本輪結束release交接。

### 同日較早：九人概念

[九人畫像索引](../../docs/videos/series-plans/ou-de-jianghu/visual-development/episode1-portraits/README.md)保留概念階段：9張概念拼板候選，另5早期版，共14 PNG；沈v3合扇、洛v2低冠、殷v2素鐵環與垂手站姿已獨立實看。當時尚未生成27份獨立視圖，現在由上述續作補齊候選。

本票 scope 補入前期總覽 README.md，同步九人概念、27張獨立候選、方向接受和定調票移到done後的連結；不修改造型規格或來源清冊。重新claim確認scope無其他活票重疊。

採用 production-list.md 的規格和asset-inventory.json清單。圖片需逐張打開檢查，不能以prompt或生成成功代替。

- 2026-10-08 建票時：依站主要求「先補齊任務、造型規格與畫像製作清單」新增本票，當時尚未生成媒體；後續概念與獨立視圖成果見上方紀錄。未授權額外服務付費、部署或發布。
