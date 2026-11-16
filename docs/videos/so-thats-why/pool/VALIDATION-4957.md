# 素材池驗證（2026-11-13，revision `2026-11-13-pool-4957`）

由 4,909 增至 4,957 個入選核心，題案由 633 組增至 637 組，可成題長題由 92 組增至 96 組（[前版驗證](VALIDATION-4909.md) · [舊庫快照](checkpoint-4909.json)）：

1. **第二十九輪素材審視（第七十九批，`wave79-earth.json` 1 筆＋`wave79-life.json` 33 筆＋`wave79-physics.json` 14 筆）**：一位作者（`F144`）補讀跨章整合潛力最高的生物發光後備長題（`M2-T1`）並重驗既有 19 核心全量合著關係，三位作者（`F145–F147`）動筆前以 Europe PMC＋Crossref（polite pool）＋OpenAlex 逐對確認研究網互不合著後從零研究三組新長題；四位未參與撰寫的獨立覆核者（`V164–V167`）核對快取雜湊、重抓來源、補查合著、修正物理與生物機制誤讀並重算分鐘。
2. **新增四組可成題長題（`G634–G637`）**：`G634` 生物發光（`M2-T1`，13.50 條、9.59 分）、`G635` 黏菌無腦迷宮與管徑記憶（`F145-T1`，13.75 條、9.72 分）、`G636` 萊頓弗羅斯特效應（`F146-T1`，13.75 條、9.72 分）、`G637` 13 與 17 年質數週期蟬（`F147-T1`，13.50 條、9.59 分）。完整紀錄見 [`reviews/material-20261113-round29.md`](reviews/material-20261113-round29.md) 與 [`reviews/material-20261113-round29.json`](reviews/material-20261113-round29.json)。

## 本機檢查

- `node tools/video/so-thats-why/pool/cli.mjs build`、`check`：PASS（5,346 筆原題、5,186 個合併後核心、4,957 個入選、637 組題案、高相似待決 0）。
- `node tools/video/so-thats-why/pool/cli.mjs index` 連跑兩次：第二次 `UNCHANGED`（`writes: 0`）。
- `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`：33 項通過。

這些檢查不代表完整製作稿或成片驗收，沒有做搜尋頁的瀏覽器檢查，也沒有讀遠端 CI。
