# A01 81→82 計數修正獨立複核 — 離線局部 PASS／正式 HOLD

日期：2026-10-17。這份覆核只評估前一份 [`independent-review-20261017.md`](independent-review-20261017.md) 提出的重查輪數問題；保留原報告及其舊版雜湊，不把當時的 HOLD 判決改寫成當時已通過。本次沒有主機、模型、媒體或帳務操作。

## 本次精確版本

| 檔案 | SHA-256 |
| --- | --- |
| `revision-fixture.mjs` | `daf9cecf1e124b2c1358a2b875b350d29aaa0e8cf5d7b0808c01fa7b6f4ed49b` |
| `revision-fixture.test.mjs` | `829fe4cff147f7e705ee5040dd423761d1b41d872e91844550592264698fd864` |
| `README.md` | `ef44244c91100c1a139c179cc3222072dd4afca3e9883cea1591c22e9c3dcffe` |
| 前次獨立探針 `independent-verifier-cap-probe.test.mjs` | `7801d2aa331c4d77830776d78493a4b64a3261cac89415d0a43c39950cb944e7` |
| round20 `manifest.json` | `4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549` |

## 核對結果

- `revisedState()` 要求六章原狀態為已寫、已查、已聽，舊 `check_rounds` 和 `lint_fixes` 為非負整數；它逐章保存舊 `check_rounds`、`lint_fixes`、`changed`，再把修訂狀態的 `checked`／`listened` 改為 false、兩種輪數歸零，並移除舊 `changed`。`verified`／`listener_done` 也歸 false，舊 round9 敘事 FAIL 與 `narrative_fixes=2` 未改。
- 六章舊計數記在方案的 `previous_chapter_counters`，同一欄進入第 82 筆事件的 `author-manifest.json`；來源交易另保存精確的 `before/auto.json`。方案／事件由既有雜湊鏈核對，修訂後來源檢查要求八個目標檔案位元組吻合。沒有修改前 81 筆事件。
- 修正後的測試直接抽取目前工人 `story.mjs` 的 `checkChapter()` 函式：用修訂後 `auto.json` 的章節狀態，4 筆 `CHANGED` 會送第 1 輪且保持 `checked=false`；用先前第 2 輪狀態，會送第 3 輪並因既有上限設 `checked=true`。這證實本次修正消除了前一份報告指出的**立即跳過重查**問題。
- 本次以 bundled Node 24.19 獨立重跑：`revision-fixture.mjs` 與其測試檔語法均通過；針對 81→82 的定向測試 **1/1 通過**；前次獨立工人上限探針 **1/1 通過**。製作者另回報完整 fixture **7/7 通過**；本次沒有重跑完整七項，因此不把它寫成獨立重跑結果。

## 判決與保留條件

**PASS_OFFLINE_COUNTER_DELTA_ONLY。** 前次 P1 計數缺陷在上述精確位元組中已修正。工人既有政策仍會在後續達最大輪數時，對含未解 `CHANGED`／`ATTRIBUTED`／`NOT FOUND` 的章節設 `checked=true`；該位元與總 `verified` 不等於事實審查 PASS，須按逐項來源及獨立審查決定能否前進。

**正式機維持 HOLD。** 這仍是標有 `production_status: HOLD`、`installation_allowed: false`、`paid_work_allowed: false` 的 Temp fixture。無真實 81-event 最新快照、共同排他寫入窗口、兩掛載點主機適配器、正式工人接續與中斷測試、站主核准的精確寫入、寫後讀回、付費媒體或成片。若正式機狀態、共享 lexicon 或候選稿位元組改變，必須重新提案與審查。
