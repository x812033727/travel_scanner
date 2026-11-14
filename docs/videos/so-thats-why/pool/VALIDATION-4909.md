# 素材池驗證（2026-11-13，revision `2026-11-13-pool-4909`）

由 4,861 增至 4,909 個入選核心，題案由 629 組增至 633 組，可成題長題由 88 組增至 92 組（[前版驗證](VALIDATION-4861.md) · [舊庫快照](checkpoint-4861.json)）：

1. **第二十八輪素材審視（第七十八批，`wave78-life.json` 40 筆＋`wave78-physics.json` 8 筆）**：四位作者（`F140–F143`）動筆前以 Europe PMC＋Crossref（polite pool）＋OpenAlex 逐對確認研究網互不合著，再由四位未參與撰寫的獨立覆核者（`V160–V163`）核對快取雜湊、重抓來源、剔除會議摘要與超譯細節、補查合著並重算分鐘。
2. **新增四組可成題長題（`G630–G633`）**：`G630` 寄生操控（`F122-T1`，11.75 條、8.69 分）、`G631` 水熊蟲隱生極限與弱點（`F141-T1`，12.50 條、9.07 分）、`G632` 冬眠週期覺醒與能量帳（`F142-T1`，12.25 條、8.94 分）、`G633` 貽貝與藤壺水下生物黏著（`F143-T1`，13.00 條、9.33 分）；`F132-T1` 橋的晃動重算 8.17 分，誠實留後備。完整紀錄見 [`reviews/material-20261113-round28.md`](reviews/material-20261113-round28.md) 與 [`reviews/material-20261113-round28.json`](reviews/material-20261113-round28.json)。

## 本機檢查

- `node tools/video/so-thats-why/pool/cli.mjs build`、`check`：PASS（5,298 筆原題、5,138 個合併後核心、4,909 個入選、633 組題案、高相似待決 0）。
- `node tools/video/so-thats-why/pool/cli.mjs index` 連跑兩次：第二次 `UNCHANGED`（`writes: 0`）。
- `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`：33 項通過。

這些檢查不代表完整製作稿或成片驗收，沒有做搜尋頁的瀏覽器檢查，也沒有讀遠端 CI。
