# C04｜獨立來源與書面配鏡差分查核

查核日：2026-10-26。查核者：`/root/approved_visual_source_delta`，未參與作者稿。

**SOURCE PASS／WRITTEN VISUAL PASS。** 110句、101景。僅核來源與書面同圖計畫；`actualasset_verified=false`，未實測TTS及12–14分鐘。

## 本次四輸入

| 檔案 | SHA-256 |
| --- | --- |
| video.json | `8549eb766873b65cb3453d03edfb5c2d151a3a9209578f3383cdc321c9620a75` |
| script.md | `6aac163b264501ae0ea87bb2a49b874bd288632c33bacc313d5a4a3c4dda9228` |
| narration-only.json | `b6897d452d1a2b051bcce76184a02100f8e50e4fa61a9f5fd8e3a756e8d5a8b2` |
| claims.json | `ecac34dc628e6be94b207baab5103438ede4d42002146e8850d413e2e193f38a` |

image-reuse-plan.json：`666ce7c8ac4f41efa1c65c7d57ac0cf5a638a170558bca3b216abbe37240def2`。完整逐句收據：[reviews/source-teaser-visual-independent.json](reviews/source-teaser-visual-independent.json)。

## 不可變來源基線與實際差分

已核來源基線video SHA：`46999917780dc1ce4f2c18d8b36f27143bdee68fae0952ba2b78fafc3324d94e`；`history/before-teaser-image-plan/reviews/source-r2-delta.json` SHA `307ac3802ecf49843183949b66864f58730aad11ed44ad2970f9827305970369`；原verify SHA `193cb84f12e2cb518923c882d73fdd606b8802d1f07d72d02606ba2b14d916b1`。每句ID、scene、文字SHA逐句實比全同，script/narration/claims JSON、brief、series逐bytes未變。全物件差分只有3個prompt/camera leaf；所有卡片完整物件未變。claims.md僅加製片書面附錄。全部60個archive、51個auxiliary與原批53檔實SHA核對全同，歷史HOLD保留。

本輪直接重開P57核發原文（HTTP200，SHA `15a6818c7ad6faa8b522aa8fafbd5c310a275fd8f8b11af059fecb4082ef3599`）及P59核發原文（HTTP200，SHA `f4b926bc4661eb185e27fb73273a44e3ed6e7743b739092788737451927c4281`）。P59明載加熱至融合溫度再令表面接觸；新h05/e07共圖只畫匿名技術人員拿住兩片膜的搭接與旁置凸起樣本，沒有熱源、熔融接縫或設備設定，熱融合答案仍在正文揭曉。它是概念插圖，不當作可確認的歷史實廠照片或工廠採用證據。

## 原生實算與停止條件

官方screenplay新舊及已批runtime逐bytes相同，SHA `d363a2d4486549ead4e444455df4af5f9e80d72693bf34fc91f028a851b2d884`。唯讀現有runtime字典 `da52e497e0721531dfa8e8043ec8ad1b0b39992472c4bfbba1c8b654685e8580`，narrative/speech/look/mix均相同，pictures由`3dee2b3ea4f722e5`變為`34c8e122b8db8835`。既存native record只作narrativeReviewMatches，新舊均true，未讀新盲票、未新判敘事。原生lint新舊均0 errors、6 soft warnings；producer只memory replay，四輸入與claims.md逐bytes重現。

| 共圖pair | 完整composed prompt SHA | seed1 1K key | seed1 2K key |
| --- | --- | --- | --- |
| two-film-seam | `f976f4c1b86586c811ec57c02494272fa7c81a197e24a00d78ba49c623d646d1` | `a1ef14ae5ad920ab` | `dde95d8ba1ab71e6` |

resolveLook、完整composeShotPrompt、camera/cast/references/size/seed及Stage.imageKey兩端等值。對應live cache目前全missing，沒有實圖：**第二teaser命令現在必須停，不得派送另買。** 正常驗收payoff後，第二命令前先重查live cache及accepted實檔SHA；任一judge/retake差異停pair。最終官方manifest、trim後selected衍生實檔、render及assembly引用與實檔SHA相同，才可聲稱實際共圖。

## 既有原件來源表

未變事實依精確來源基線逐句接鏈，不冒稱本輪重開全部原件。

| 代號 | 原件 | 定位與範圍 |
| --- | --- | --- |
| P57 | https://patents.google.com/patent/US3026231A/en | metadata; Description 175–218; claims；核發文本與設計主張；不是原始申請稿、上市或工廠實採證據 |
| P59 | https://patents.google.com/patent/US3142599A/en | metadata; Description 225–231, 425–439, 460–485；核發文本、製程及材料受力主張；不證明1959年上市或所有市售氣泡形狀 |
| P60 | https://patents.google.com/patent/US3208898A/en | metadata; Description 416–424, 649–662；連續加熱、展膜、貼合、冷卻設備之專利示範；不證明實廠落地或產能 |
| SA13 | https://www.sealedair.com/company/media-center/press-releases/sealed-air-announces-finalists-bubble-wrap-appreciation-day-hall-of-fame | dated January 6, 2013; paragraphs More On Bubble Wrap, web lines 901–904；公司多年後回顧；不是獨立見證或同期訂單 |
| SAH | https://www.sealedair.com/products/brand/bubble-wrap | About BUBBLE WRAP, web line 892；公司回顧1957牆面方向、1960創立及之後IBM 1401包裝關聯 |
| SA17 | https://www.sealedair.com/content/dam/protective-materials/inflatables/newair-ib/NewAir%20I.B.%20Extreme%20H160%20Brochure.pdf | PDF page 2, date10/17; web lines7–12,26–38,49–54 and specifications table；2017年後期另一產品的廠商說明；沒有獨立性能試驗；12英吋屬所列XLIB規格，手冊另列3.6英吋款 |
| SEC12 | https://www.sec.gov/Archives/edgar/data/1012100/000119312513087879/d452256d10k.htm | Item1 Business, web line174；成立年1960，未給成立月份 |
| IBM | https://www.ibm.com/support/pages/zvm/history/360rev.pdf | PDF page17, lines613–616；IBM1401於1960開始出貨，不支持其包材供應商 |
| IBM_H | https://www.ibm.com/history/1401 | opening history, introduced1959；1959發表；未提氣泡片供應商 |
| EDITORIAL | editorial | ；觀眾假想、問題、標明的旁白反應或CTA；不是特定歷史事件、客戶或性能實驗 |

本查核沒有付費、後台呼叫、runtime/approval/media或Git操作；不授權發布。生成圖QA、實際共圖、12–14分鐘媒體實長與成片驗收仍未完成。
