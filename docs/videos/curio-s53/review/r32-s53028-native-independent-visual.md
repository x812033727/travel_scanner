# S53 R32｜`s53028` 首張原生圖非作者原尺寸驗收

2026-10-22 UTC。**HUMAN REJECT。**我不是本景提示詞、生成或機器驗收作者；獨立查看錯置於巢狀私有目錄的未裁原圖及所選裁圖，對照現行稿件與固定 1913 年 *San Francisco Relief Survey* D 段。本收據只裁定這一張圖；沒有改動稿件或私有媒體，也沒有購買媒體。

| 核對對象 | SHA-256／狀態 |
| --- | --- |
| 巢狀私有 `curio-s53/keyframes/s53028-1.jpg`，1280×720 | `422357339ab4a2ab4267593c1c33c44f73dec3013773009dbc7577b287466010` |
| 巢狀私有 `curio-s53/keyframes/s53028-1-trim.jpg`，1280×720 | `d4a06299fb0b6bd023478bdebb33c8e4bbde1e737979d007576f65336cbe0db5` |
| `docs/videos/curio-s53/video.json` | `b9ce6cc426d547642ff7f6a7ee8c3a2564aad2439ff4b659c0f337ba19e9fea6` |
| `docs/videos/curio-s53/claims.md` | `9be8b979eb0594e9244886811926878d894065872b561262a490c586f05b6e9b` |
| 固定 `56217-0.txt` | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| 有效私有 `keyframes/manifest.json` | `b080a08e4ddecaf1dfd84ebb67fb436cbecc542e3cf4ff5983fc0b66dc04971b` |
| 合併後有效私有 `media/ledger.json` | `a29940cf76954de8595a3eaacd1a56da94a22a2a2508537dffc96661a384cc8b` |

`s53028` 口播是「九月十日，小屋工程開始。」；提示詞指定 1906 年火災後的避難地點、一名匿名木匠在木屋工地**量一塊普通木板**。`claims.md` 對應 [Survey D L4848–4870](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4848-L4870)。固定原文 L4858–4864 說土地及建築部負責建造取代帳棚的小屋、8 月 1 日公布計畫並發包、**9 月 10 日開始建造**，直到 **9 月 16 日**才有 Hamilton Square 首批 20 間完工。

兩張 1280×720 圖中央都是童貌、身形很小的人物，戴醒目的青綠色現代安全硬帽，雙手扶著直立木板上緣。畫面沒有尺、記號或量測動作，人物也不清楚像正在工作的成年木匠。左右兩側各有屋頂、牆面、門窗均已齊全的木屋；裁圖沒有去掉這些物件。這種已完工木屋夾著現代硬帽人物的工地畫面，會把「工程剛開始」傳成已建成的小屋街景，且硬帽不合 1906 年時代。即使兩側屋子可被解作既有背景建物，現代硬帽和缺失的量測行為仍使圖像不能兌現本景提示詞；沒有足夠根據把它們認作 9 月 10 日已完成的救濟小屋。

巢狀圖單的機器 judge 給 **9.29／10、`passed=true`、`details=7`**，只指出構圖比要求的 medium shot 更寬；這沒有解決原尺寸可見的年代、施工階段及動作問題。依 Curio 的來源／旁白矛盾驗收界線，我判本圖 **HUMAN REJECT**，不得把機器 PASS 當成本景 KEEP。

本次 CLI 工作目錄錯誤把一張 image 和一次 judge 的付費產物寫到 `/workspace/.video-work/curio-s53/curio-s53/`。其巢狀圖單 SHA `bcfb127e05b3431bfcebdad17c672e5ea4ef2eef6bccbe896d0cad844a0829ff`，只有 `s53028` 一筆；巢狀 ledger SHA `9862f2d17c939c0ee5eef8bdb8159a5d321e0b258149e519026e0318173d5f57`，兩筆費用合計 US$0.0135。作者已把這兩筆**原樣、僅一次**接到有效 ledger：前 89 筆與 R31 前備份逐項相同，末兩筆與巢狀 ledger 逐項相同；重新加總為 **US$0.6075／46 image／45 judge／0 預約**。有效 18 KEEP manifest 與 R32 前備份逐位元組相同，沒有 `s53028`，所以此圖未進入有效選片。有效 `media/jobs.json` SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`，`jobs={}`；`STOP` 在位。
