---
id: 2026-10-08-ou-de-jianghu-scene-prop-design
title: 《偶的江湖》第一集場景與道具美術參照及連戲細節
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-08T10:52:21Z
completed_at:
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-art-direction
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/scene-prop-design
---

# 《偶的江湖》第一集場景與道具美術參照及連戲細節

## Why

角色還需進入一致的空間，持物的形狀／數量和出入口決定關鍵影格是否能接起來。

## Definition of done

- [x] 由e001實際分場枚舉主場景與常用鏡位，交空景、出入口／軸線、尺度與光色卡；場景燈光不寫入全域角色style。
- [ ] 逐shot核對白扇、念珠、刀劍、三枚銅錢、鍛鉗、無歸箭／斷弦等，列大小、左右、數量與狀態；可讀字卡另做後製。
- [x] 胎記／手背印、黑風及偽裝受控細節獨立列，記高冠長袖／持物遮擋風險、來源與媒體hash及接受紀錄。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [ ] 完成上述交付項，將實際證據及未決問題記入本票 scope 的成果文件。
- [ ] 依驗收要求獨立核對；完成才 done，停止則 release，不把待執行標為完成。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

跟e001 video.json/script.md及cast-notes逐項核對，不提前揭第8集未決答案；先離線清單，生成依前置包。

- 2026-10-08：本票是站主要求「先補齊任務、造型規格與畫像製作清單」新增的待執行工作；本次沒有生成或核准媒體，也沒有授權額外付費、部署或發布。
- 2026-10-08 後續授權「首集製作前置全補完」：已用內建imagegen生成並實看29個latest（19空景/狀態、7道具板、3受控卡），40原PNG全保留；成果見[場景包](../../docs/videos/series-plans/ou-de-jianghu/visual-development/scene-prop-design/README.md)。未调用其他付費供應商、未改e001/production、未寫owner採用。
- `build-artifacts.mjs`：7來源SHA、9appearance pointer、25參照輸入SHA、40原圖複製SHA、455/455 shot+4字卡來源索引通過。`npm run check:tasks`通過（1691檔，6既有過期claim warning）。逐鏡原文字已完整保存，道具命中為機械索引，重要狀態人工核對；仍不把它稱作逐影格動畫QA。
- ep1_scene_plan獨立抽看5圖，右手/月牙/四箭/門方向未見立即硬錯。cold圖source已收窄到a05-s031/s035/s042（翻盤之後）。客房master v3/cold v2仍殘留淡月輪，須在紙窗近景前修，不能稱全部定稿；棋盤PNG格線不可作母版，另附精確19路SVG點位提案。剩餘持物/接觸/選母版與逐鏡畫面核對在成果review/prop-continuity明列，因此本票不done。
- 收尾：收據媒體根改為可攜的 `<VIDEO_WORKDIR>/ou-de-jianghu-e001`；整理器以 `OU_DE_JIANGHU_WORKDIR` 接受實際路徑。README 與圖廊已對 master v3、angle-b v2、cold v2 三張一致標明紙窗殘影，只作空間／光線提案，不准用為紙窗 CU 母圖。重建再次核對 7 來源、40 原圖／副本、29 latest、455 鏡均通過；本票的待修與逐鏡核對仍保留。
- 最後路徑核對：repo 收據／prompt／工作紀錄的 170 個個人絕對路徑改成 `<IMAGEGEN_ORIGINAL>` 或單集 `<VIDEO_WORKDIR>` 代號；原始本機工作紀錄另保留於 repo 外。整理器用 `IMAGEGEN_ORIGINAL` 解析生成原圖根目錄。40 PNG 的 SHA／尺寸及 2 SVG SHA 與修改前逐筆一致，沒有重生或改動媒體；scope JSON／MD／整理器掃描無個人路徑，證據見 portability-verification.json。
- 2026-10-09 續作：本輪內建imagegen共6修訂，累計46原圖、28工作候選；master v4／angle-b v4紙窗已不透景，personal-prop-states v3移除藍色扇墜，全部raw保留20261009。cold兩修仍月輪，依製作重設計取消所有cold獨立母圖（禁止作模型輸入），三鏡s031/s035/s042改乾淨master v4綁SHA加cold-state-spec；這是尚未渲染的狀態規格，並未宣稱失敗圖修好。
- 首集棋局固定為editorial continuity decision：保留原16點，依s051白(4,3)/s062黑(5,4)/s071白(15,3)/s079白(5,5)由12逐步至16；末a05-s091只加白(1,17)成17。6階段加前後兩份19路SVG已保存，非原作棋譜／owner核准。未改source劇本。
- 送茶索引修正：原稿與v3/v4均是s017沈咳嗽、s018送茶、s019左托右敲、s022開門，已修本scope MD與builder規則；455鏡原文索引仍保存原稿。主代理要求先保留claim，待最後review回覆再交回。
