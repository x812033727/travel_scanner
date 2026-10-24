# S52 R6｜R5 限縮 HOLD 的作者定點修補

2026-10-20 UTC。[R5 獨立逐句來源及書面畫面](r5-source-independent.md)對當時精確五檔為 **HOLD／HOLD**，指向一處秒數口播量詞、一處主張表漏引 Cook、一處畫面時段相反。R6 只修這三項；R5 已完成的敘事主線修稿沒有回退。下列是作者本地凍結，**不是** R6 由另一人完成的來源、畫面或敘事簽核。

| R6 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `31b4a238af41093392dad81f303ec06512ada452bea37d66eeffa57408ed00d7` |
| `research.md` | `8a2bdbb0767089b1dd5c71397a325618ff3d55437de2bf45815eac3962e7a7a1` |
| `claims.md` | `7caba4680fb2d7db561124b298152eb28606b4e4670b7ce6cd766c9ce1e4c95f` |
| `video.json` | `a515ca252e09d656771f6a4b6ccd510fced1f723211d62f23d52d43644173366` |
| `script.md`（CLI 重生） | `aeae2ec0be77ec3fe229ac42b561d434136c9b2d7a73b30c1f689b88b5ae0b6f` |

| 定點位置 | R5 → R6 |
| --- | --- |
| `s52204` | 口播及主張表同步把「下午三點三十二分**十分秒**」改為「下午三點三十二分**十秒**」，使 Kippis 末格 **15:32:10** 能逐字唸清楚；其餘三個時刻與上午 18:22、下午 18:02、兩段差 20 秒的算術均未改。[K L1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178) |
| `s52205` | 旁白原句不改。主張表保留 Kippis 四格時刻的行錨，另補 Cook [C L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)，支撐「**庫克說**兩次內接觸尤其難判」；不再以 Kippis 表單獨支撐 Cook 的說法。 |
| `s52074` | 書面畫面由六月二日出發的 `late afternoon light` 改為 `cool early-morning light`，對齊旁白「隔天清早」與 Cook 當日 `Very early this morning` [C L5957–5960](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5957-L5960)。不主張精確日出時刻。 |

`brief.md`／`research.md` 僅同步 R6 版本與 R5 HOLD 狀態；沒有新史料或新故事線。固定 Cook／Kippis 全文 SHA 仍為 `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`、`c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`，來源層級見 [research.md](../research.md)。

作者本地檢查：**119 景**（114 插畫、4 卡、1 片尾）、**121/121** 句與主張表依 ID、順序、字面對齊，工具重生 `script.md` 與當前分鏡逐位元一致，**19 組** setup/payoff 有效；`lint --slug curio-s52 --json` **0 errors／0 warnings**。`estimateTimeline` 在 250／300／325 CPM 的開場 **42.90／37.00／34.90 秒**，正文 **557.37／481.60／455.00 秒**；較快估值仍低於八分鐘，真實語音仍須實測。`npm run test:docs-videos` **236/236**、`npm run check:tasks` **2,124 票**、`git diff --check` 通過。沒有呼叫 S52 付費語音、插圖或配樂。

下一手按上述精確五檔由另一位工作者重核逐句來源及書面畫面，尤其三個定點差分；兩位此前未讀 R6 的隔離讀者各只讀新 `script.md` 依固定 13 題盲評。新版來源／畫面和雙人敘事均過後，才走政策、站台劇本卡、真實 TTS／音檢與付費畫面。
