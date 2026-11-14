# 素材池驗證（2026-11-13，revision `2026-11-13-pool-5013`）

由 4,957 增至 5,013 個入選核心，題案由 637 組增至 640 組，可成題長題由 96 組增至 99 組（[前版驗證](VALIDATION-4957.md) · [舊庫快照](checkpoint-4957.json)）：

1. **第三十輪素材審視（第八十批，`wave80-life.json` 42 筆＋`wave80-physics.json` 14 筆）**：四位作者（`F148–F151`）動筆前以 Europe PMC＋Crossref（polite pool）＋OpenAlex 逐對確認研究網互不合著後從零研究四組新長題；四位未參與撰寫的獨立覆核者（`V168–V171`）核對快取雜湊、重抓來源、展開分裂作者 ID 補查合著、修正機制與統計細節並重算分鐘。
2. **新增三組可成題長題（`G638–G640`），一組誠實留後備（`F151-T1`）**：`G638` 蜘蛛絲液態紡絲與遇水超收縮（`F148-T1`，12.75 條、9.20 分）、`G639` 墨西哥鈍口螈斷肢再生位置記憶與神經／巨噬細胞開關（`F149-T1`，13.50 條、9.59 分）、`G640` 荷葉與超疏水雙層氣墊、凝結水滴自彈射除塵與刺穿失效（`F150-T1`，13.75 條、9.72 分）；`F151-T1` 水下超高速彈射與空蝕護甲經覆核查獲兩組跨網合著橋樑併網後下修為 `10.75` 條、`8.17` 分，留後備、14 個開放全文核心入池備用。完整紀錄見 [`reviews/material-20261113-round30.md`](reviews/material-20261113-round30.md) 與 [`reviews/material-20261113-round30.json`](reviews/material-20261113-round30.json)。

## 本機檢查

- `node tools/video/so-thats-why/pool/cli.mjs build`、`check`：PASS（5,402 筆原題、5,242 個合併後核心、5,013 個入選、640 組題案、高相似待決 0）。
- `node tools/video/so-thats-why/pool/cli.mjs index` 連跑兩次：第二次 `UNCHANGED`（`writes: 0`）。
- `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`：33 項通過。

這些檢查不代表完整製作稿或成片驗收，沒有做搜尋頁的瀏覽器檢查，也沒有讀遠端 CI。
