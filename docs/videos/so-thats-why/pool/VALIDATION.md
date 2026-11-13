# 素材池驗證（2026-11-13，revision `2026-11-13-pool-5069`）

由 5,013 增至 5,069 個入選核心，題案由 640 組增至 644 組，可成題長題由 99 組增至 103 組（[前版驗證](VALIDATION-5013.md) · [舊庫快照](checkpoint-5013.json)）：

1. **第三十一輪素材審視（第八十一批，`wave81-food.json` 14 筆＋`wave81-human.json` 14 筆＋`wave81-tech.json` 28 筆）**：針對 7 大分類中核心與長題數最少之四個分類（`飲食與廚房科學`、`人體感官與日常行為`、`建築交通與商業制度`、`數位科技與通訊工程`），由四位作者（`F152–F155`）動筆前以 Europe PMC＋Crossref（polite pool）＋OpenAlex 逐對確認研究網互不合著後從零研究四組新長題；四位未參與撰寫的獨立覆核者（`V172–V175`）核對快取雜湊、即時重抓關鍵全文、展開分裂作者 ID 地毯式複查合著、修正實驗細節並重算分鐘。
2. **新增四組可成題長題（`G641–G644`）**：`G641` 麵包揉混麵團液氣泡微熱管與同步中子／中紅外線三階段老化時鐘（`F152-T1`，飲食與廚房科學，13.75 條、9.72 分）、`G642` 人類立體空間聽覺 1,450 Hz 鎖相陡牆、房間駐波距離反轉與轉眼珠前耳膜預擺動（`F153-T1`，人體感官與日常行為，13.25 條、9.46 分）、`G643` 路面動態水壓坑洞、爐石水泥遇融雪鹽百倍化學侵蝕反轉與微膠囊感應加熱自癒（`F154-T1`，建築交通與商業制度，14.00 條、9.85 分）、`G644` 光纖散射非線性極限、電漿光纖保險絲與中空反共振空氣光纖（`F155-T1`，數位科技與通訊工程，13.75 條、9.72 分）。完整紀錄見 [`reviews/material-20261113-round31.md`](reviews/material-20261113-round31.md) 與 [`reviews/material-20261113-round31.json`](reviews/material-20261113-round31.json)。

## 本機檢查

- `node tools/video/so-thats-why/pool/cli.mjs build`、`check`：PASS（5,458 筆原題、5,298 個合併後核心、5,069 個入選、644 組題案、高相似待決 0）。
- `node tools/video/so-thats-why/pool/cli.mjs index` 連跑兩次：第二次 `UNCHANGED`（`writes: 0`）。
- `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`：34 項通過。

這些檢查不代表完整製作稿或成片驗收，沒有做搜尋頁的瀏覽器檢查，也沒有讀遠端 CI。
