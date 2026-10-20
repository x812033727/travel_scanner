# S49 R9｜兩個來源錨點獨立覆核

2026-10-20 UTC。**結論：窄範圍 PASS。** `moon012`、`moon015` 的逐句來源錨點已指到固定原文的確切事實；相對於 [R9 來源獨立覆核](r9-source-independent.md)所審的五檔版本，只有 `claims.md` 這兩列的來源欄改動。兩列旁白、畫面欄、其餘 claims、`script.md`、`video.json` 均未改。此裁決只解除這兩個錨點的 HOLD，不代替 R9 後續敘事、音訊或媒體關卡。

| 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `e008301ee9d75073bb7370bf6251ddb3eadc83032597a7f31217006f4bd66709` |
| `script.md` | `10f912c63ba438c676372469e8e44a52a8252113efc22f3af9fb74f91ae22354` |
| `video.json` | `547409b2cb87e1ea5ba0133e3c140aa15ba4cce793e26a55d0cbde49fe1bb396` |

逐行核對的固定全文：J `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`；L `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`。J 是 1902 年的後出天文評論；L 是 Locke 名下 1859 年重印本，不把任一份當作已核對的 1835 原報影像。

| ID | 新連結所涵蓋的原文 | 裁決 |
| --- | --- | --- |
| `moon012` | [J 4129–4137](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4129-L4137) 在 4133–4135 行明寫 Herschel 於南天觀測 1,202 顆雙星及 1,708 個星雲與星團；[J 4054–4067](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4054-L4067) 在 4060–4066 行明寫這趟遠行成了《太陽報》捏造發現的基礎。 | 兩個來源欄連結各指向旁白的對應事實，**PASS**。 |
| `moon015` | [L 152–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L152-L165) 在 152–162 行印出帶 Herschel 姓名的重印標題；[L 212–254](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L212-L254) 在 212–222 行列出冒稱的月球等發現。 | 標題與其後發現各有直接錨點，反問句仍保留證據界線，**PASS**。 |

差分方法：從目前 `claims.md` 僅將上述兩列來源欄的完整新連結還原為 [R9 來源獨立覆核](r9-source-independent.md)所列舊連結，所得檔案 SHA-256 恰為 R9 審過的 `34d270d19c80e8c5f81112e32ac2e79dde386839339cf708276a0626b7c8aa92`。因此全檔逐位元差異只在這兩個來源欄；兩列旁白及畫面欄無改動。其餘四檔 SHA-256 與 R9 完全一致，包含全部 `script.md` 旁白及 `video.json` 的旁白、提示詞、字卡與 loop。未修改作者內容、票、媒體或站台。
