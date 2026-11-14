# 素材池驗證（2026-11-13，revision `2026-11-13-pool-5125`）

由 5,069 增至 5,125 個入選核心，題案由 644 組增至 648 組，可成題長題由 103 組增至 107 組（[前版驗證](VALIDATION-5069.md) · [舊庫快照](checkpoint-5069.json)）：

1. **第三十二輪素材審視（第八十二批，`wave82-food.json` 14 筆＋`wave82-human.json` 14 筆＋`wave82-tech.json` 28 筆）**：持續針對 7 大分類中核心與長題數最少之四個分類（`飲食與廚房科學`、`人體感官與日常行為`、`建築交通與商業制度`、`數位科技與通訊工程`），由四位作者（`F156–F159`）動筆前以本機 JATS 作者群＋Europe PMC＋Crossref 逐對確認研究網互不合著（對共享出口 IP 之 OpenAlex／Crossref 429 第一次即停零重試）後從零研究四組新長題；四位未參與撰寫的獨立覆核者（`V176–V179`）核對快取雜湊、即時重抓關鍵全文、展開分裂作者 ID 與 SciELO／H2020 跨庫補查合著、修正實驗細節並重算分鐘。
2. **新增四組可成題長題（`G645–G648`）**：`G645` 油炸蒸汽阻油、同步輻射拆穿降破 100 °C 凝結吸油舊說與鹽水預泡酥脆反轉（`F156-T1`，飲食與廚房科學，14.00 條、9.85 分）、`G646` 雙腳安靜站立倒單擺 200 毫秒延遲門檻、三感官重新加權與不到 1 牛頓指尖輕觸穩身（`F157-T1`，人體感官與日常行為，14.00 條、9.85 分）、`G647` 生石灰六成濕度鈍化陷阱、古羅馬海陸混凝土雙骨架與正午比氣溫低兩度的沸石冷卻混凝土（`F158-T1`，建築交通與商業制度，13.75 條、9.72 分）、`G648` 電容觸控螢幕互電容、顯示雜訊對決、可摺疊拉伸電極與隔空靜電觸覺及吃白光無電池薄片（`F159-T1`，數位科技與通訊工程，13.25 條、9.46 分）。完整紀錄見 [`reviews/material-20261113-round32.md`](reviews/material-20261113-round32.md) 與 [`reviews/material-20261113-round32.json`](reviews/material-20261113-round32.json)。

## 本機檢查

- `node tools/video/so-thats-why/pool/cli.mjs build`、`check`：PASS（5,514 筆原題、5,354 個合併後核心、5,125 個入選、648 組題案、高相似待決 0）。
- `node tools/video/so-thats-why/pool/cli.mjs index` 連跑兩次：第二次 `UNCHANGED`（`writes: 0`）。
- `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`：34 項通過。

這些檢查不代表完整製作稿或成片驗收，沒有做搜尋頁的瀏覽器檢查，也沒有讀遠端 CI。
