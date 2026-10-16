# A01 round19 年份近距離重複窄修候選 — HOLD

本資料夾從已凍結的 [round18](../A01-round18-n14-provenance-candidate/README.md) 衍生，按[獨立整稿閱讀](../A01-round17-source-bound-candidate/independent-full-script-review-20261017.md)只修 `origin-01/zc7k` 一句。前一句 `r12o01` 已交代「1928 年出發前」，因此將 `zc7k` 的「據館方記載，**1928 年**安妮塔……」改成「據館方記載，安妮塔……」。同步改 `origin.json` 的 `o22.claim` 和 `source-map.json` active `zc7k.text`；來源索引 8、事實索引 5、`PENDING`、歷史 `previous_text` 全保留。

六章 79 景／108 句的順序不變；除上述一句，其他旁白及全部畫面不變。`hook`、`idea`、`engine`、`turn`、`now` 五章及 `candidate/series.json` 與 round18 逐位元組相同。`r12o01`、series 原章企劃、`must_verify[5]`、來源 8 中的 **1928 年事實**原樣保留，沒有把出發年份從證據或企劃刪掉。round14–18 原候選不變。

## 凍結版本

| 內容 | SHA-256 |
| --- | --- |
| round18 基底 `manifest.json` | `df5908caec1b88147b19a50b42ea992f88388750eecf4ffd681cb394707d60da` |
| round19 `delta.json` | `8d9ded432ebb705b04a078fc29450f172d207597db4fc4f2b56bab2d3902c47f` |
| round19 `manifest.json` | `a8bd87c659f536b92acd7563ba89c34912802dbf73e6b48717edb0d7e5a44469` |
| `candidate/chapters/origin.json` | `0686434d49bdc076445b30a9f2daf90a34f44bf396ba193649d97abaa1a32589` |
| `source-map.json` | `352b056e5a9c516ac1c89c9d2f74a53c9b6f1e7f730ec247514fc099a28cd19a` |
| `validation.json` | `63869d1a48ecab7a4692e558fb985aa4f43b287cd8d5f3c5a88d8e7966f3ff14` |
| 合成旁白列 | `af2ff39f523bcbd029e79f4ab2a4d84698c6ed4600ae8c22d9bb9ffcb80879f4` |

`manifest.json` 另釘選六章、series、來源表、validation 的檔案雜湊；`build.mjs` 在寫入前核對 round18 manifest 和每個輸入的雜湊，並要求除了 `zc7k` 的旁白、`o22.claim` 及 active 來源列文字以外，其他欄位完全一致。

## 已做檢查與後續關卡

`node --check build.mjs`、`node build.mjs --write`、`node build.mjs --check` 退出碼均為 0。builder 重新 compose 79 景／108 句並跑 `lintVideo` 和 `cuteStoryVisualProblems`：**0 lint error、40 warning、0 cute-story error**。`validation.json` 列出警告及純文字片長估算；估計 250 units/min 為 650.93 秒、300 units/min 為 556.1 秒，**不是實際 TTS 時長**。既有 round9 三項敘事 FAIL 仍是歷史紀錄，這份機械檢查沒有改寫它們。

2026-10-17 後續：[獨立來源差異複核](independent-review-20261017.md)確認只有預定的一句與相應 claim／來源列改動；[獨立整稿閱讀](independent-full-script-review-20261017.md)把 13 題敘事規則重綁到本輪精確雜湊，未找出新的確定旁白阻擋。兩份結論只涵蓋離線編輯稿，不是工人審稿通過。

**正式製作仍 HOLD：** 新旁白 SHA 尚未經正式 verifier／listener／盲讀 narrative panel，也沒有綁定此稿的 `story/reviews/script-review.json`。後續仍須量實際 TTS 片長、檢查 MiniMax 真圖及成片播放。不得據此寫正式主機、啟動任何付費工作、匯入 B18／後五集或上傳 YouTube。這裡沒有審稿收據或付費媒體。
