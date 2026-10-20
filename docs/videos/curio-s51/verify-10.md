# S51 R10｜七列主張來源錨點作者修補

2026-10-20 UTC。[R9 獨立來源覆核](review/r9-source-independent.md)對旁白史料、書面畫面判 PASS，但指出 `cal015/017/018/019/046/095/096` 七列的既有來源欄未完全覆蓋原句，逐句主張錨點為窄 HOLD。本次只改 `claims.md` 這七列的**來源欄**，不改台詞、研究、插畫提示詞或其他內容檔。這是作者修補候選，須由另一位工作者核七格差分才能解除 HOLD。

| ID | 補上的固定英國調查 G 原文與界線 |
| --- | --- |
| `cal015` | [L3362–3364](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3362-L3364)、[L3399–3401](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3399-L3401)：格羅夫斯至史東的船橋值班交接；原 R01 繼續支持無乘客。 |
| `cal017/018` | [L3362–3373](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3362-L3373)：格羅夫斯見兩盞桅燈，主觀判為客輪；不把判斷當已證船型或船名。 |
| `cal019` | [L3379–3383](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3379-L3383)：格羅夫斯證詞轉述船長上橋後說不像客輪。 |
| `cal046` | [L3525–3528](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3528)：正式報告列 23:40 鐵達尼號撞冰，與所見遠船停下同時。 |
| `cal095/096` | [L3470–3474](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3470-L3474)：史東自述 02:40 再報、船長追問顏色、自己再稱全白；證詞與船長記憶有歧異。 |

固定 G 原文位元組 `/tmp/s51-independent-sources/british-report.txt` SHA-256 `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；提交位址與史料限制見 [research.md](research.md)。

| 內容檔 | R10 SHA-256 |
| --- | --- |
| `brief.md`（未改） | `ad22f35f5d9ff6a17e055f27b4b6eaaf921f22856b15445531db5a4caf087837` |
| `research.md`（未改） | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `c7fa85a186f070f17a679798f2d04c54defc4c79fbfaa1773ffb98acf67778a5` |
| `script.md`（未改） | `5a874c0efa3e321a8d17a868d20ba2790128ffa79bc86cae3d8ba740c245ff80` |
| `video.json`（未改） | `4f2b24cfbc81e403c0f76c436cdfbb839d2a90affec72701b30701388e022777` |

將七格新來源欄逐一還原成 R9 原文後，`claims.md` SHA 重得 `640575ed6604e891accedb8d3febac8091c830f99d42e3740719975716e27f6b`，證明其餘位元組未改。作者本地檢查：`claims.md` 與 JSON **134/134** 句同 ID、同序、同文；CLI `screenplay(doc)` 與 `script.md` 逐位元一致；**131/131** `shot` 提示詞非空、**16/16** 伏筆有序；`lint --slug curio-s51 --json` 為 **0 errors／0 warnings**，`git diff --check` 通過。R9 未改的 325 CPM 最快文字估時，首八景 **36.37 秒**、後續正文 **516.60 秒（8:36.60）**；不是實際 TTS 時長。

下一關是另一位工作者按精確 R10 五檔、七格來源欄與固定 G 原文獨立核對。R9 的兩位全新隔離讀者仍需只讀未變的劇本，完成固定 13 題盲評；合併放行前不開始站台、政策或付費媒體。
