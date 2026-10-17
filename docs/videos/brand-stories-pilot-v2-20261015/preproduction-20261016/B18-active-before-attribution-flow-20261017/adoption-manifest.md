# B18 來源承接口播版本：本機企劃採用收據

2026-10-17。**只採用本機企劃 row 與 row review，未匯入正式機、未啟動工人或付費製作。**來源是 [`B18-attribution-flow-candidate-20261017`](../B18-attribution-flow-candidate-20261017/README.md)；其 `sha256.json` 為 `8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754`。候選的獨立[兩句口播複核](../B18-attribution-flow-candidate-20261017/INDEPENDENT-FLOW-REVIEW.md)與[六來源 row 審核](../B18-attribution-flow-candidate-20261017/ROW-REVIEW-METHOD.md)已讀取；新 `review-candidate.json` 為 `verdict: pass`、`reviewer_only: [4]`，只核准 canonical story SHA `d0a9e19d311def1130c50cf6ba83a9ffb7f58c435e7c2460901abb211fe03648` 的企劃 row。

替換前，將三個 active 檔原始位元組複製到此目錄；來源與備份的 SHA-256 各自相同，索引見 [`backup.json`](backup.json)。

| 原 active 檔 | 此處備份 | 替換前 SHA-256 |
| --- | --- | --- |
| `episodes/B18.json` | `episodes-B18.json` | `21122b7db5f97957ca89399b249a02e47e0b4465003e3653efbbf422b6043e9d` |
| `episodes/reviews/B18.json` | `reviews-B18.json` | `06012b65e0e3a9b911dda1432c9de61f73f01f28a91fb5b23a7fad0354e794ed` |
| `stories.json` | `stories.json` | `16e314adf3c94953ac17ea5f15e9cc9f96b2e51ab5489be524c16b762cfaa055` |

只將候選的 `B18.json` 和新 `review-candidate.json` 複製到 active `episodes/`，再使用既有 `build.mjs --write` 重編雙集 `stories.json`，沒有手改編譯結果。

| 採用後 active 檔 | SHA-256 |
| --- | --- |
| `episodes/B18.json` | `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681` |
| `episodes/reviews/B18.json` | `6e06d5ddd1d4d836a105450e15b49fc98203e7ea0a595c7bba1596630fb73dc8` |
| `stories.json` | `c02fa490725c169c5cb84c0bf05ae9afa1a0c9bac65d8e17d7c602aafed9871b` |

本機讀回：新收據 `reviewProblems` 零項，B18 canonical story SHA 與收據相符；編譯後 `must_verify[4]` 是唯一 `reviewer_only`。編譯前後 A01 資料列的 `JSON.stringify` 位元組相同，SHA-256 `eac94808e982a122420bedf2b8d3cb0e06db4ac7858502cb98f224cc0b81a356`。候選六章是 85 景、88 句、65 筆主張，65 筆判定仍全部是 `UNCHECKED`。既有 builder 重跑兩次得到相同 `stories.json` SHA；API `check_story_file` 回傳 A01/B18 兩列，`problems`、`refused`、`ignored` 都是空陣列。

**剩餘關卡：** 本次 row 審核不核准完整逐字稿。歷史 `scripts/B18.md` 與舊審稿沒有更動，也不能當本版 PASS；最後完整稿須對齊 I03/I04 及全部企劃修正，另經來源、listener 與敘事審查。65 筆逐景主張仍待正式 worker verifier；接著才是 TTS 試聽、圖像、可關閉繁中 CC、成片與站主看片。這份本機資料也不是正式匯入授權或正式機狀態證明。
