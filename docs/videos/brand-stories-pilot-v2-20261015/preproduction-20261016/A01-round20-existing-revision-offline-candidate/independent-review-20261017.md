# A01 81→82 離線修訂工具獨立審查 — HOLD

日期：2026-10-17。審查範圍是此目錄的離線 fixture，以及它與當前 `tools/video/automation/story.mjs` 的接續關係。沒有操作正式機、帳務、模型或媒體。此報告不構成候選稿的事實審查，也不是正式 `script-review.json`。

## 核對的位元組與結果

| 檔案 | SHA-256 |
| --- | --- |
| `revision-fixture.mjs` | `6f008f862320cdc82ba06649476d333b00de4695f6684aeb300c4d3227c6fac6` |
| `revision-fixture.test.mjs` | `dc36203bfd490fc2eba266126b57e6a4fea15a421f0829453b161d7e97896848` |
| `README.md` | `ff98821e3ddedfb41936224e2f7d894b8cb0b1244eaf3629d8a58f6aec81a19c` |
| `independent-verifier-cap-probe.test.mjs` | `7801d2aa331c4d77830776d78493a4b64a3261cac89415d0a43c39950cb944e7` |
| round20 `manifest.json` | `4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549` |

Bundled Node 24.19：原離線測試 **7/7 通過**，約 101 秒；獨立的實際工人函式探針 **1/1 通過**。七項測試只證明合成快照、80→81→82 鏈、精確位元組、常見中斷與回滾情境的本機行為。

## 阻擋正式套用的問題

**P1 — 重查旗標和輪數不一致，可能跳過必要的第二次查核。** `revision-fixture.mjs:177–183` 把六章 `checked`、`listened` 及總旗標改為 false，卻保留舊的 `check_rounds`。合成狀態與測試明確把六章設為 2 輪，並在套用後要求仍為 2（`revision-fixture.test.mjs:55,187–189`）。實際工人在 `story.mjs:1291,1316–1317` 用 `round = entry.check_rounds + 1`，且在 `round >= max_verify_rounds` 時，不論本輪有多少 `CHANGED`／`ATTRIBUTED`／`NOT FOUND` 主張，都設 `checked=true`；預設上限為 3。獨立探針抽取並執行同一個 `checkChapter` 函式：4 項變動、舊輪數 2 → 第 3 輪後 `checked=true`；舊輪數 0 → 第 1 輪後 `checked=false`。六章都被標記後，`story.mjs:1321–1326` 會產生 `verify-1.md` 並設 `verified=true`。這個 fixture 不能作為安全的 82nd event 套用候選。

最小修正：在新來源修訂的 `auto.json` 中，六章的**本次重查輪數**從 0 開始；把原輪數逐章寫入不可變的 82nd event 計畫／收據，不能抹掉歷史。加上工人接續測試：第一個 verifier payload 是 round 1，當 `changed > 3` 時維持 `checked=false`、`verified=false`，下一輪才繼續。對到達最大輪數而仍超過門檻的情況，另核對既有「輪數到頂即 checked」政策是否允許進入旁白；不可把該 `checked` 位元當成獨立事實 PASS。

**正式機前提仍未成立。** `fixtureRoot()` 只驗證 Temp 路徑與 marker；`safety()` 接受呼叫者提供的合成狀態。`baseline()` 可由呼叫者傳入 `pins80`，因此合成鏈測試不等於固定的正式機歷史釘選。這些是離線測試的合理設計，並非身份驗證、真實主機鎖、兩個掛載點的交易、當前 DB／額度／工作進程讀回或站主授權。`README.md` 已清楚寫明此界線。正式安裝須另有新快照、固定歷史釘選、所有寫入者共同遵守的排他窗口、真實工人接續試驗、窄範圍核准及寫後讀回；本次沒有執行。

結論：**HOLD_FOR_OPERATIONAL_ADOPTION**。本機鏈與中斷測試成功，但輪數漏洞使它目前不能帶動 A01 的真實 verifier。也沒有實際的 82nd event、重新審稿、配音、插畫、成片、B18 或後五集製作。
