# A01 round20 `i17` 事實索引中繼資料候選 — HOLD

本資料夾由已凍結的 [round19](../A01-round19-origin-year-repeat-candidate/README.md) 衍生，只補 `source-map.json` active `idea-07b/76ur`（`claim_id: i17`）的 `fact_index: 4`。原列已有 `source_index: 6`，其來源 URL 與 `candidate/series.json` 的來源 6 一致；`candidate/chapters/idea.json` 的 `i17` 原已綁定 `fact: 4`、`source: 6`。本輪沒有改那一句旁白、主張、來源歸屬或 `PENDING` 狀態。

六章檔、`series.json`、`validation.json` 與 round19 **逐位元組相同**，因此仍是 79 景／108 句，旁白 SHA 未變。來源矩陣仍有 27 條 active rows，僅上述一列新增事實索引；其他列、`n14` 現行／歷史來源分界及所有歷史 verdict 都與 round19 相同。round14–19 原候選不變。

## 凍結版本

| 內容 | SHA-256 |
| --- | --- |
| round19 基底 `manifest.json` | `a8bd87c659f536b92acd7563ba89c34912802dbf73e6b48717edb0d7e5a44469` |
| round20 `delta.json` | `27a358f38b79f2af6ce67a6fc90993a7880b9cf36b99174244e77682c8a29830` |
| round20 `manifest.json` | `4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549` |
| `source-map.json` | `7ed35cecd3d581bac3f73a4d90abba9e5efafba71afc038481f363dc11494559` |
| 未改的 `validation.json` | `63869d1a48ecab7a4692e558fb985aa4f43b287cd8d5f3c5a88d8e7966f3ff14` |
| 未改的合成旁白列 | `af2ff39f523bcbd029e79f4ab2a4d84698c6ed4600ae8c22d9bb9ffcb80879f4` |

`manifest.json` 另釘選六章與 series 的 SHA-256。`build.mjs` 驗 round19 manifest 及每個輸入的雜湊，核對 `i17.fact=4`、`source=6`、series `must_verify[4]` 的來源關聯，並要求刪除新增的 `fact_index` 後，來源表與基底逐欄相同。

`node --check build.mjs`、`node build.mjs --write`、`node build.mjs --check` 均退出碼 0。round19 在完全相同的六章與 series 上已重新 compose 79 景／108 句、跑 lint 和可愛插畫規則，結果為 0 lint error、40 warning、0 cute-story error；本輪是來源中繼資料修正，沿用其 validation，**沒有把此結果當成新一輪整稿審核**。

[獨立來源差異複核](independent-review-20261017.md)已確認本輪只有 `i17` 的事實索引補欄；[round19 的獨立整稿閱讀](../A01-round19-origin-year-repeat-candidate/independent-full-script-review-20261017.md)綁定相同的旁白 SHA，本輪六章與企劃逐位元組不變。這兩份結果是離線編輯與來源表局部審查。

**正式製作仍 HOLD：** 新來源表與旁白尚未經正式 verifier／listener／盲讀 narrative panel，也沒有綁此稿的 `story/reviews/script-review.json`。仍須量實際 TTS 片長、檢查 MiniMax 真圖及成片播放。不得據此寫正式主機、啟動任何付費工作、匯入 B18／後五集或上傳 YouTube。round9 的三項敘事 FAIL 仍為歷史紀錄。
