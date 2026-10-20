# S51 R6｜重述與調查證據排比的作者凍結

2026-10-20 UTC。R5 [獨立史料與書面畫面](review/r5-source-independent.md)判 PASS；但兩位新讀者的[合併敘事裁決](review/r5-official-panel.md)為 **FAIL**：共同 `no_recap` No，A 指 `cal135` 重講 `cal080` 的摩斯指示，B 指片尾重講 `cal132` 的未起航結果；B 另判 `cal108–112` 的「先／再／最後」證據列舉使 `no_toc` No。R6 是回應這些診斷的**作者候選**，並非獨立來源、畫面或敘事 PASS。

## R5 → R6 精確差分

| 位置 | R6 改動與界線 |
| --- | --- |
| `cal108–114` | `cal108` 直接說遠船停住與撞冰山同時；`cal110–112` 讓火箭時段、數量和船影消失沿夜間時間往前走，去掉「先／再／最後」口吻；刪去只重講相鄰句的 `cal109`、`cal113`。`cal114` 仍只把船名識別歸於後來英國報告。原文 G [L3525–3542](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3542)逐項支持時間、火箭數量及報告推論；沒有把調查歸納寫成船員當夜認出船名。 |
| `cal135` | 改為「史東說，船長讓他有新消息就派實習生來報；當下沒有起航指示。」去掉 `cal080` 已說的摩斯命令，保留**史東版本**中尚未說的實習生回報細節。G [L3428–3435](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3428-L3435)明寫 `He states` 與派實習生條件；不推論船長心態。`cal136` 的船長只記得一枚與史東五枚的回呼、不能證明當夜認出船名的界線保持原文。 |
| `cal137`／`outro` | 刪除正文 `cal137` 的反事實救援人數未解句，移成片尾第一句「若當夜出航，究竟能救多少人，史料無法回答。」代替 R5 重說 `cal132` 未起航的片尾句。正文 `cal132` 仍載英國報告「未嘗試」結論；片尾卡文字同步改為「能救多少人，無法回算」。G [L3543–3550](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3543-L3550)只說**可能**救下多人，不提供可證人數。片尾仍三句，沒有預告下一支。 |
| 畫面／伏筆 | 刪去三景時一併刪其提示詞；`cal106` 只把後來日間證據「desk」改為同義「table」，保持無字海圖與兩艘無標記模型，讓視覺多樣性 lint 維持零警告。`cal135` 既有匿名日間符號卡不變。16 組伏筆的 setup/payoff ID 不變，只同步兩組指向 `cal135` 的描述。 |

`brief.md` 頂端同步 R5 結果與 R6 待覆核狀態；`research.md` 與固定 G/B/A 原文未改。其餘旁白和提示詞不變。R5→R6 由 138 景／140 句變成 **135 景／137 句**，其中 **134 景正文 shot**；不以重述補時。

| 內容檔 | R6 SHA-256 |
| --- | --- |
| `brief.md` | `3d3213283fa06ebd671fef248b2aed176b7765b70eddffc23d24edf981d4fb29` |
| `research.md`（未改） | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `41edfcf6ec849ac29e13a6289b58d8b481562bf1ecf94d8e729b9d2fdb1a3385` |
| `script.md`（CLI 重生） | `ab53cca8be8c2e5bd89146ad16df053f5692219d180d0dfc087c0699c967de86` |
| `video.json` | `7bba596263852359697d41ecdbb747a3e8211592caddeebc6addcbf7bfdee2bc` |

作者本地核對：`claims.md` 與 JSON **137/137** 同 ID、同序、同文，CLI `screenplay(doc)` 與 `script.md` 逐位元相同；**134/134** 個正文 `shot` 提示詞非空，伏筆 16/16 指向仍存在的句子。`node tools/video/cli.mjs lint --slug curio-s51 --json` 為 **0 errors／0 warnings**；`git diff --check` 通過。`estimateTimeline` 在 250／300／325 CPM 時，首 8 景開場為 **44.80／38.60／36.37 秒**，其後正文為 **652.00／562.80／531.30 秒**；最快仍為 **8:51.30**，不是 TTS 實長。

**下一關：**另一位工作者按本表**精確五檔 hash**獨立核 R6 改句的 G 錨點、主張與書面畫面差分；兩名真正隔離的新讀者只讀同版 `script.md` 按固定 13 題盲評。R5 來源 PASS 不自動繼承到 R6；R6 作者檢查也不當敘事 PASS。政策、站台大綱／劇本、TTS、付費插畫、配樂、成片及上傳均未開始。
