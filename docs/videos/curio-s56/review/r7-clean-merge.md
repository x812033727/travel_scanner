# S56 R7｜乾淨雙讀者正式敘事合併（HOLD）

2026-10-20 UTC。這次正式合併只適用於 [R7 作者凍結](r7-author-fix.md)：`script.md` SHA-256 `1612cbe85e9add3f1c4b9b4be490a3fe9a6ef23588f080ed4f16d135369d1e2d`、`video.json` SHA-256 `451fd61d81b93ba3290d314c5b3b408d4a1b59a7c40287d3d03ad5e6df315f8a`。合併前五檔雜湊均與作者表及 [R7 獨立史料、主張與書面畫面 PASS](r7-source-independent.md)一致；來源覆核檔 SHA-256 為 `5f38b356891a4f198b1ed134011ab66ffc26673aa904752e6496da35287810a8`。這是敘事關卡，不重判來源。

| 獨立讀者答卷 | SHA-256 | 是／否 | 唯一否票 |
| --- | --- | ---: | --- |
| [A 答卷](r7-clean-blind-a/ballot.json) | `83d36c6fdaf1f31a81bb0e1f8e1f735ab2faf952e36e1a439133ea31e11e9716` | 12／1 | `no_recap` |
| [B 答卷](r7-clean-blind-b/narrative-answers.json) | `9ab100aa9d9ce624c39db4f66f91f026634fac76c4bd3b20849f2884971a1f40` | 12／1 | `no_recap` |
| [逐題 OR 合併答卷](r7-clean-merged-answers.json) | `501b2a0bc582b4441d326c08fee69c4dd8654f772a66ee3678fabb61b099b545` | **12／1** | **`no_recap`** |

兩位讀者在相同 R7 劇本雜湊上各自凍結 13 題答卷，個別正式紀錄分別是 [A](r7-clean-blind-a/official-narrative.json)及[B](r7-clean-blind-b/narrative-cli-receipt.json)。合併前核對 26／26 個答卷引句，均與當時凍結 `video.json` 的逐句口說完全相同。兩人都在 `[s56132] 他認為，天氣乾燥、路面有焦油，加上飛落木塊，能解釋剛才那一幕。` 投 `no_recap=no`：乾燥、焦油路面和飛落燃燒木塊已分別在 `s56034`、`s56038`、`s56053` 說過，該句沒有明示回呼。因此逐題 OR 後這道**必答題仍是 no**；其餘 12 題是 yes。這些是讀者的敘事判斷，不推翻該句的史料來源 PASS。

正式執行 `VIDEO_WORKDIR=/tmp/s56-r7-official-merge NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s56 --answers docs/videos/curio-s56/review/r7-clean-merged-answers.json --json`，預期的失敗出口碼為 **1**。[原樣 CLI 回條](r7-clean-cli-receipt.json) SHA-256 `cda359576e617dff637e327d41ec5c722727f6651335f662cea4aa3b91bd76a9`：`passed:false`、`failed:[no_recap]`、`advisory:[]`。正式紀錄 `/tmp/s56-r7-official-merge/curio-s56/review/narrative.json` SHA-256 `ff4d55e6199f3286844315a878a02df03b6b7ad8800a2b1fccf6f0e2bc370938`，其中 `round=1`、`narrative_hash=0af74e3174cb3b72`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。輸入、兩卷、合併和命令的雜湊另見 [機器稽核](r7-clean-merge.json)。

**R7 敘事關卡 HOLD。** 本輪沒有送 Jev 政策請求；[政策停點](r7-policy.md)另記。任何 R8 文字改動都需新雜湊、新獨立判定與新正式敘事合併，不能沿用此 R7 結論。
