# A01 round20 `i17` 事實索引獨立複核 — 局部 PASS／整片 HOLD

日期：2026-10-17（台北）。此覆核只比較 round19 → round20 的一個來源表欄位，不是新旁白的整片 verifier、listener、narrative panel 或正式 `script-review.json`。

## 精確檔案與差異

| 檔案 | 本機重算 SHA-256 |
| --- | --- |
| round19 基底 `manifest.json` | `a8bd87c659f536b92acd7563ba89c34912802dbf73e6b48717edb0d7e5a44469` |
| round20 `delta.json` | `27a358f38b79f2af6ce67a6fc90993a7880b9cf36b99174244e77682c8a29830` |
| round20 `source-map.json` | `7ed35cecd3d581bac3f73a4d90abba9e5efafba71afc038481f363dc11494559` |
| round20 `manifest.json` | `4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549` |

`node build.mjs --check` 退出碼 0，報 79 景／108 句、旁白改動 0、active source row 改動 1，來源表共 27 行。manifest 的旁白 SHA-256 仍為 `af2ff39f523bcbd029e79f4ab2a4d84698c6ed4600ae8c22d9bb9ffcb80879f4`；未改的 `validation.json` SHA-256 為 `63869d1a48ecab7a4692e558fb985aa4f43b287cd8d5f3c5a88d8e7966f3ff14`。

另以獨立逐位元組比較驗證六章 `candidate/chapters/*.json`、`candidate/series.json`、`validation.json` 全部與 round19 相同；再逐欄比較來源表，只有第 24 條 active `idea-07b/76ur` 增加 `fact_index: 4`。其他 26 條 active 行、全部 `inherited_claim_reconciliation`（含已消歧的 `n14`）、27 行順序與所有舊 verdict 完全相同。

## `i17` 來源對位

未改的 `candidate/chapters/idea.json` 原已將 `i17` 綁為 `source: 6`、`fact: 4`、`verdict: PENDING`，其 claim 與 `idea-07b/76ur` 旁白一致。新來源表這一行保留 `source_index: 6`、原 ABC URL、`PENDING_INDEPENDENT_REVIEW` 與原文字，只補 `fact_index: 4`。series 的 `must_verify[4].sources` 包含 6，內容涵蓋 Macy's 先拒、後由副總裁下單與 1970 年開賣；`sources[6]` 是 [Sadow 本人接受 ABC News 訪談的報導](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)。該報導記他回憶副總裁 Jerry Levy 試走樣品並叫採購進貨，也記十月陳列。此索引是把既有旁白與企劃事實對齊，沒有增加顧客購買或銷量的獨立證明。

**PASS_METADATA_DELTA_ONLY**：`fact_index: 4` 的指向與現有章 claim、series 事實和來源 6 相符，未見旁支改動。round20 仍是 `HOLD_UNREVIEWED_OFFLINE_CANDIDATE`；round19/20 共同的新旁白 SHA 尚待獨立整稿閱讀及正式 verifier／listener／盲讀敘事審核，之後仍需實際 TTS 片長、MiniMax 真圖與成片播放。round9 敘事 FAIL 是歷史結果。此局部結論不授權正式審稿收據、主機寫入、付費工作或 YouTube 上傳。
