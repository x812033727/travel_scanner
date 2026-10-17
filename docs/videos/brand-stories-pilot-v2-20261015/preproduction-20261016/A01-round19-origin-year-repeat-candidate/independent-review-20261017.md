# A01 round19 一句年份重複窄修獨立覆核 — 局部 PASS／整片 HOLD

日期：2026-10-17（台北）。本覆核只比較 round18 → round19 的 `origin-01/zc7k` 及其來源綁定，不重用 round18 其他審查結果作為新旁白 SHA 的正式 PASS，也不是主機 `story/reviews/script-review.json`。

## 精確檔案與差異

| 檔案 | 本機重算 SHA-256 |
| --- | --- |
| round18 基底 `manifest.json` | `df5908caec1b88147b19a50b42ea992f88388750eecf4ffd681cb394707d60da` |
| round19 `delta.json` | `8d9ded432ebb705b04a078fc29450f172d207597db4fc4f2b56bab2d3902c47f` |
| round19 `manifest.json` | `a8bd87c659f536b92acd7563ba89c34912802dbf73e6b48717edb0d7e5a44469` |
| round19 `source-map.json` | `352b056e5a9c516ac1c89c9d2f74a53c9b6f1e7f730ec247514fc099a28cd19a` |
| round19 `origin.json` | `0686434d49bdc076445b30a9f2daf90a34f44bf396ba193649d97abaa1a32589` |
| round19 `validation.json` | `63869d1a48ecab7a4692e558fb985aa4f43b287cd8d5f3c5a88d8e7966f3ff14` |

`node build.mjs --check` 退出碼 0，回報 79 景／108 句、改一行旁白、一條 active 來源列，lint 0 error／40 warning、cute-story 0 error。新旁白列 SHA-256 為 manifest 所綁的 `af2ff39f523bcbd029e79f4ab2a4d84698c6ed4600ae8c22d9bb9ffcb80879f4`；這是離線 compose 的雜湊，不是正式 panel 收據。

我另以獨立 JSON 遞迴差異比對兩版：`candidate/series.json` 和 `hook`、`idea`、`engine`、`turn`、`now` 五章完全相同；`origin.json` **只有** `scenes[2].lines[0].text`（`origin-01/zc7k`）和 `claims[0].claim`（`o22`）兩個值變動；來源表 **只有** `lines[17].text`（同一 `zc7k`）變動。27 條 active 行數與順序不變，其餘 26 行逐欄相同，`inherited_claim_reconciliation[n14]` 亦完全相同。全部畫面提示詞、場景順序、角色、loops 和企劃沒有旁支更動。

## 來源與聽感界線

舊句為「據館方記載，**1928 年**安妮塔拉著兒子做的輪子箱出發；它仍是一家人的自製品。」新句只刪除加粗的重複年份。前一景 `origin-r12-01/r12o01` 已說「1928 年出發前」；後接兒子製箱兩句，再到這句出發，年份在同一小段可承接，不會改成無年代的另一趟旅行。[Winnetka Historical Society 的館藏記述](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)支持館方歸屬、兒子造自製輪子箱與 1928–1930 第二次旅行；新句沒有宣稱 1928 是製作年，也沒有把 1927 館藏品和當年旅途示意箱斷定為同一件。館方頁本次直接擷取不穩，來源文字與界線沿用已記錄的官方全文索引及[前輪逐句來源覆核](../A01-round14-source-bound-loop-candidate/independent-source-map-review-20261017.md)，不聲稱今天重新取得網站 HTTP 200。

`o22.claim` 和 active `zc7k.text` 與新句逐字一致；`o22.source=8`、`fact=5`、`verdict=PENDING`，來源行 `source_index=8`、`fact_index=5`、`verdict=PENDING_INDEPENDENT_REVIEW` 原樣保留。series `origin.point`、`must_verify[5]` 與 `sources[8].supports` 的 1928 年事實未刪。round18 已分開處理的 `n14` 歷史 ABC／現行物理敘述仍維持：現行來源 `null`、舊 ABC 在 `prior_source`、歷史 `NOT FOUND` 未變。

## 結論

**PASS_DELTA_ONLY**：刪去一次近距離重複年份沒有擴大史實主張，三處文字對位，版本雜湊與局部差異通過；未發現其他旁支改動。round19 整稿仍需針對新旁白 SHA 做獨立閱讀與正式 verifier／listener／盲讀 narrative panel，並量實際 TTS 片長、驗 MiniMax 真圖與成片播放。round9 三項敘事 FAIL 仍是歷史結果。此局部覆核不授權正式審稿收據、主機寫入、付費製作或上架。
