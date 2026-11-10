# S59 R3｜作者窄修與五檔凍結收據

2026-10-21 UTC。A 案〈1878 年科學院聽見留聲機說話，為何有人懷疑腹語？〉的 **R3 作者候選**。R2 [正式雙盲](r2-merge/summary.md)因必過 `no_recap` 為 HOLD；[獨立來源／書面畫面](r2-source-independent.md)則是來源逐句 PASS、畫面 HOLD。R2 的票和來源結論不能替 R3 放行；本版沒有執行 TTS、付費媒體或站主核准。

| 凍結檔 | R3 SHA-256 |
| --- | --- |
| `research.md` | `ad5baec33ae786da9d103eecadca9f16c9f23f00d4041bde158e1e2697958efb` |
| `brief.md` | `f2086e64ffd56c5c2d8ea072d7122ffd7d7a2c2290c3413cf54a8ea2a8e35b4f` |
| `claims.md` | `75f3c81a1cfba0250c8fe2d291765acdeb098dd6f37e8fc34bb17632e62356e9` |
| `video.json` | `542c5d17330d2344fd588bfe839b636642f37da80c97a9f34d29ace013c75ec5` |
| `script.md` | `86d6b9883dc24ba55b2c4c66ad390755610999a84dd354e1c02aa8c0f8cbc1f3` |

`research.md` 的 SHA 與 R2 相同，因固定來源和 P01–P16 界線沒有變。其餘四檔有 R3 差分。`script.md` 由 `node tools/video/cli.mjs script --slug curio-s59` 生成，narrative hash `a68b3aee6456c265`；`visualHash(video.json)` 為 `273dd951c9f3d93d`。六章、109 句、12 組 `loops`，100 張插圖景與 9 張工具排字卡。濃縮開場 9 句、196 漢字，工具估約 56 秒；正文 2,622 漢字，按最快每分鐘 325 漢字約 **8.07 分鐘**；CLI 全片旁白估 13.14 分鐘，實長待語音。仍規劃 5 秒頻道片頭及 21 秒 `v4-endscreen`，說明欄保留兩份固定原文與頻道連結；Short 等長片核准後擷取，不造假回連。

## 修正範圍

- 讀者 B 的 s59013→s59014 紙盤點劃重述，改為直接問接點能否從另一台機器讀回訊號；s59016 即答。
- 讀者 A 的杜蒙塞爾失敗後重述，縮成結果→懷疑者反應→嘴與話筒距離疑問→院士如何重試，移除一整句重複總結。加入 D6899–6909 記載的支架轉開／螺絲調壓兩個不同機械步驟，使正文仍達八分鐘。
- 依 R2 獨立畫面覆核修六個鏡頭：懷疑者圖只見一人、電報圖是圓紙盤不是紙帶、距離圖只做說話一動作。前段新增一景造成來信中兩張圖的 ID 由 R2 s59070／s59071 變為 R3 s59071／s59072。縮圖星號與過期額度註記也已修。[差分逐景稽核](r3-author-delta-audit.md)列真正覆蓋的原文行段與畫面界線；[全句 ID／來源組稽核](r3-source-citation-audit.md)核 109／109 句及 D／E 原檔 SHA。

作者按 13 題自檢，R2 其餘 12 題的主要結構仍在；本版仍需**兩位新的無前情讀者**逐項評票、固定 OR 合併與官方 `narrative --answers`。新增機械步驟及六個改寫畫面亦需**非作者**按本版五檔 SHA 重審來源／畫面，不能沿用 R2 來源 PASS。

驗證：`node tools/video/cli.mjs lint --slug curio-s59 --json` **0 errors／0 warnings**；`npm run test:docs-videos` **236／236**；`node tools/tasks.mjs check` 退出 0；凍結後再次 SHA 重算與表格相同。若任一五檔再變，必須重新凍結並重做獨立覆核。
