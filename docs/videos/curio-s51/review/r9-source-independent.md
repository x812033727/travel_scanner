# S51 R9｜史料、主張錨點與書面畫面獨立覆核

2026-10-20 UTC。對下表**精確 R9 五檔**，裁決為 **旁白史料 PASS、書面畫面 PASS、逐句主張錨點窄 HOLD**。R9 只刪除一個重述句，沒有發現口播失實或新的畫面風險；但逐一核對沿用主張表時，找到七列舊有來源錨點未涵蓋該句全部事實。這是內容檔引用的缺口，須由作者限縮修正後再由另一人核對，不能把舊版 PASS 自動搬到 R9。此審核不代替雙讀者敘事、圖片原尺寸、政策或語音關卡。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `ad22f35f5d9ff6a17e055f27b4b6eaaf921f22856b15445531db5a4caf087837` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `640575ed6604e891accedb8d3febac8091c830f99d42e3740719975716e27f6b` |
| `script.md` | `5a874c0efa3e321a8d17a868d20ba2790128ffa79bc86cae3d8ba740c245ff80` |
| `video.json` | `4f2b24cfbc81e403c0f76c436cdfbb839d2a90affec72701b30701388e022777` |

三份固定原文重算吻合 `research.md`：正式英國調查 G `/tmp/s51-independent-sources/british-report.txt` SHA `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；Beesley B SHA `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`；Gracie A SHA `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。固定提交連結在 `research.md`。原文 G 將證人所說與報告最終歸納放在同一章，片中仍須維持兩者分界。

## R8→R9 差分與畫面

我以 R8 官方敘事輸入快照 `/tmp/s51-r8-narrative-current.json` 的實際 payload 位元組 SHA `3fd72ea2b2e9349075224b8f1d64834fd36a2070386ad591982591e5766565f4`（與 [R8 合併裁決](r8-official-panel-merged.json)記錄相同）逐 ID 比 R9：R8 的 132 個 `shot` 句減去 `cal061`「加州人號的船橋仍有人值班，可以看見海面。」後，**其餘 131 句文字與 ID 未改**。G [L3182–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3197)說唯一無線電員睡了、沒收到求救電文，支持保留的 `cal060` 對 `cal004` 耳機休班的回呼；G [L3362–3364](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3362-L3364)、[L3399–3401](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3399-L3401)與 [L3420–3442](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3442)則證明船橋仍有人值班、見白火箭。刪掉第二次說船橋有人，不會把無線電艙休班誤說成整艘船無人。

對照 SHA `1e8feed428c617ced77d251a328f1b75ba8d498cf103e11bee51720a6ee59b22` 的 R5 原始 `video.json` 快照 `/tmp/s51-r5-baseline-video.json`，R5→R9 的 137 個 `shot` 只刪 `cal032/034/061/109/113/137`，餘下 131 景**只有** `cal060` 與 `cal106` 的 `desk`→`table`；R5→R8 這五個刪景、`cal106` 同義詞與其他保留提示詞已見 [R7](r7-source-independent.md)、[R8](r8-source-independent.md)獨立差分。R9 的 `cal061` 瞭望鏡景隨句刪去；`cal060` 現為「1912 evidence table by day、anonymous clerk、blank signal slip」，是後來白日的無字證據示意，沒有畫成當夜有人讀到電文、可讀虛構原件、船員已辨船名或固定船距。**R9 書面畫面 PASS**；生成圖片仍須原尺寸逐張審。

## 沿用主張表的窄缺口

下列台詞本身有 G 原文支持；`claims.md` 對它們的**現有**研究錨點卻只覆蓋部分或其他事。這些列均非 R9 新增；修補可限於該表的來源欄，不需改口播或畫面。

| ID | 現在的錨點缺甚麼 | 足以補齊的固定 G 原文 |
| --- | --- | --- |
| `cal015` | R01／G L3292–3334 支持「沒乘客」，未記當晚船橋值班員。 | [L3362–3364](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3362-L3364)與 [L3399–3401](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3399-L3401)列 Groves／Stone 接班；可加 R04。 |
| `cal017/018/019` | 三句均只連 R02／G L3334–3353；該段說遠船燈與 Evans 的無線電推測，未記 Groves 兩盞桅燈、客輪判斷或 Lord 反對。 | [L3362–3373](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3362-L3373)、[L3379–3383](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3379-L3383)；可加 R04。 |
| `cal046` | R04／G L3357–3419 講船燈，未直接寫鐵達尼號 23:40 碰冰。 | [L3525–3528](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3528)；可加 R11。 |
| `cal095/096` | R10／G L3484–3510、L3531–3536 記晨船及夜船消失，未記 Lord 追問火箭顏色、Stone 回答全白。 | [L3470–3474](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3470-L3474)；宜加直接 G 錨點。 |

對其餘沿用台詞，我逐列核 `claims.md` 與 `research.md` 的 R01–R15 範圍，並抽讀高風險 G [L3163–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3163-L3197)、[L3420–3481](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3481)、[L3525–3550](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3550)：五枚／一枚是不同證人說法，約八枚與船名是報告歸納，五英里不是確定距離，能救多少人沒有可證答案。未見其他需要改旁白的失實。

獨立解析 R9 得 **134/134** 台詞 ID 唯一、`claims.md` 同 ID 同序逐字對齊、CLI `screenplay(doc)` 與 `script.md` 逐位元一致；**131/131** 正文 `shot` 提示詞非空、**16/16** 伏筆 setup/payoff 存在且有序。`lint --slug curio-s51 --json` **0 errors／0 warnings**；`git diff --check` 通過。`estimateTimeline(doc, 325)` 為首八景 **36.37 秒**、其後正文 **516.60 秒（8:36.60）**，非真實 TTS。

**下一步：**作者只補上表七列 `claims.md` 錨點，保留腳本與 JSON；重新固定 claims SHA，請另一位審核者按這七列及全檔對齊解除窄 HOLD。兩位全新讀者可同時盲讀 R9 劇本，但在精確來源包與敘事合併都過關之前，不應開始政策、網站核准或付費媒體。
