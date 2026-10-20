# S51 R10｜七格主張來源錨點獨立差分覆核

2026-10-20 UTC。對下表**精確 R10 五檔**，前版 [R9 的逐句主張錨點窄 HOLD](r9-source-independent.md)已解除：**旁白史料 PASS、逐句主張 PASS、書面畫面 PASS**。本次只審作者的七格來源欄修補；R9 的未變旁白與提示詞依 R9 獨立審核判斷。這不是 R9 劇本的新讀者敘事裁決，也不是圖片或語音驗收。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `ad22f35f5d9ff6a17e055f27b4b6eaaf921f22856b15445531db5a4caf087837` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `c7fa85a186f070f17a679798f2d04c54defc4c79fbfaa1773ffb98acf67778a5` |
| `script.md` | `5a874c0efa3e321a8d17a868d20ba2790128ffa79bc86cae3d8ba740c245ff80` |
| `video.json` | `4f2b24cfbc81e403c0f76c436cdfbb839d2a90affec72701b30701388e022777` |

我將 `claims.md` 的七列來源欄還原為 R9 原文，其餘位元組不動，獨立重得 R9 claims SHA `640575ed6604e891accedb8d3febac8091c830f99d42e3740719975716e27f6b`；改動 ID 精確為 `cal015/017/018/019/046/095/096`。其餘四檔 SHA 與 [R9 凍結](../verify-9.md)逐位元相同，故無新旁白、JSON 分鏡或提示詞變動。

固定英國調查 G `/tmp/s51-independent-sources/british-report.txt` 重算 SHA `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；Beesley B 與 Gracie A 亦重算為 `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`、`d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`，符合固定研究。七格逐一對原文：

| ID | 獨立核對 |
| --- | --- |
| `cal015` | [G L3292–3298](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3292-L3298)支持當時無乘客；[L3362–3364](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3362-L3364)與 [L3399–3401](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3399-L3401)支持 Groves 在第一更、Stone 接中更。新來源欄兩半均覆蓋，未把無線電室休班當船橋無人。 |
| `cal017/018` | [G L3362–3373](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3362-L3373)說 Groves 看見兩盞桅燈，並以**自己的判斷**說是客輪；兩列新欄均限定為他的看法，沒有說當夜已證船型或船名。 |
| `cal019` | [G L3379–3383](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3379-L3383)以 Groves 證詞記 Lord 上橋後說「不像客輪」；新欄明示證詞層級。 |
| `cal046` | [G L3525–3528](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3528)記 23:40 撞冰與加州人號所見船停時序。新欄將此歸於正式調查，不冒充船橋即時辨船。 |
| `cal095/096` | [G L3470–3474](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3470-L3474)直記 Stone 稱 02:40 再報、Lord 追問顏色、自己再保證全白。新欄兩列均標為 Stone 自述，並對船長不同記憶留了界線。 |

`claims.md` 與 `video.json` **134/134** 同 ID、同序、同口播；CLI `screenplay(doc)` 與 `script.md` 逐位元相同。**131/131** 個 `shot` 提示詞非空、**16/16** 伏筆 setup/payoff 有序；`lint --slug curio-s51 --json` **0 errors／0 warnings**，`git diff --check` 通過。首八景與最快 325 CPM 正文估長仍為 **36.37 秒、8:36.60**，尚非真實 TTS。

**裁決：R10 精確來源包三項 PASS。** 下一關是兩位全新隔離讀者對未變的 R9 `script.md` 做固定 13 題盲評並合併；其後才可走政策、站台與付費媒體。
