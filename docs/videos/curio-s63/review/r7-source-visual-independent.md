# S63 R7｜獨立史料與書面畫面覆核

2026-10-22 UTC。**PASS：R7 凍結候選的逐句來源及書面畫面關卡；無阻擋 ID。**本回條只審固定旁白、來源錨點、資訊卡語義與尚未生成的插圖提示；不評正式敘事 13 題、實際圖像、聲音或成片。

| 凍結材料 | SHA-256 |
| --- | --- |
| 提交 `d8ad5276aaac50e388469a5f0fc962669d899e68` 的 `video.json` | `423f78e9ff18b5b77b14a0ad2fbfe71053cf08aba051a640c53038aa012c2263` |
| `script.md` | `0b5f9bad1330cf0ffbb30998a6e3799b3f88386ffda70867fc047b6a8f4ab408` |
| `claims.md` | `ac6a96737c7e84bff49991801874285de2d2a78b637f4e98899e8b16a37942d7` |
| 固定 Brown／Stearns 原文 `/tmp/curio-s63-box-brown-1849.txt` | `6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2` |

固定原文為 174,750 bytes、2,817 行，對應 `research.md` 所釘 [GITenberg commit `a92658e80effa4cce03bb19c13e96ffaaae5fa2b`](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt)。[題名頁 L50–56](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L50-L56) 說明正文是 Brown 自述事實經 Charles Stearns 筆寫的出版敘事；書末編者註與 Samuel J. May 演說摘錄是另外的聲音，不是獨立貨運或法律紀錄。

## 比較範圍

直接比對 R6 父版 `bf249e524` 與 R7：R6 三檔雜湊分別為 `video.json` `8f8903a7ec270c61636953a7d675840a838604c268132722658c05b26f2dbf68`、`script.md` `dfafdb178646575cc4cefab9c14621284835299caf1c75f3eea86e7835d82bd9`、`claims.md` `10a28deb76976f1b7c32eb4ab0188c6fda33e93d1914d2d1536c1ecd7eb9c18e`，均吻合 [R6 獨立覆核](r6-source-visual-independent.md)。JSON 頂層只有 `scenes` 改動；127 個同序場景中僅 `s63001`–`s63004`、`s63009`、`s63062`、`s63067`、`s63123`–`s63124` 九個完整物件變動，**118 個逐欄相同**。`claims.md` 逐句列也只改這九個 ID；`script.md` 只改其中八個旁白／章名，`s63009` 僅換畫面。故 R6 對 118 個未變場景的來源及書面畫面結論，按此精確差異沿用；下列九個重新查核。

## 九個變動 ID

| ID | 固定文本、旁白、書面畫面及卡片判定 |
| --- | --- |
| `s63001` | [B05 L1494–1499](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1494-L1499) 明說木箱做好後 Brown 搬到承諾協助的朋友面前；先交箱、後問箱內裝甚麼、最後同意釘蓋。首鏡及事件章名符合這一步。未封釘、無字木箱與畫外朋友不預演入箱。里奇蒙是下文所述的上下文定位，不是該小段明寫的房間地址。 |
| `s63002` | 同一 [B05 L1494–1499](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1494-L1499)：朋友先問是否裝衣服，顯示此刻不知箱要裝 Brown；Brown 想藉箱逃離的意圖另由 [L1490–1492](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1490-L1492) 明說。單人看未封箱、表情不確定只作插畫示意，不把想像表情當有照片佐證。 |
| `s63003` | [B05 L1494–1498](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1494-L1498) 有釘蓋的決定；[B07 L1516–1545](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1516-L1545) 有途中數次翻向。旁白以「如果」預問，畫面只示尚未釘上的蓋與空箱，不把後來的倒置提早演出。 |
| `s63004` | [B09 L1569–1572](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1569-L1572) 的順序是費城接收者先遲疑，再有人敲問，Brown 回答。開場只問他屆時能否應聲；里奇蒙空箱旁的人物未提前演出費城敲問或給答案。 |
| `s63009` | [B09 L1564–1577](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1564-L1577) 支持抵費城與出箱；[B10 L1620–1638](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1620-L1638) 支持出箱後仍疑慮安全。旁白保持疑問。畫面退回啟程前的里奇蒙街道與箱旁人物；朝北方望是目的地的插畫暗示，並非聲稱有可考的特定道路、推箱路線或費城已抵達。 |
| `s63062` | [B04 L1480–1482](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1480-L1482) 明寫他懇切祈求困境中的援助，隨後想到箱子。旁白與低頭祈禱的示意保留其自述的宗教經驗，未宣稱外部驗證的神蹟。 |
| `s63067` | [B05 L1488–1492](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1488-L1492) 連寫木匠警告、Brown 因追求自由仍決定嘗試；改後旁白正對這一步。插圖的成箱取自緊接的 [L1494](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1494)，在交給朋友之前；不重演交箱。`claims.md` 此列所連 L1488–1493 足夠支持旁白，但「做好」落在下一行，已由 `s63001` 的 L1494–1499 連結與本回條補足；若再修此列，可把範圍延到 L1494。 |
| `s63123` | 書末[編者註 [8] L2452–2455](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L2452-L2455) 明說家人的索價是 `Twelve hundred dollars`，也說 Brown 正籌款，沒有說已支付。旁白明指編者腳註而非 Brown 親述。錢袋是無字示意，未用四張空椅假定家人面貌、座次或已重逢。 |
| `s63124` | 同一[編者註 [8] L2452–2455](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L2452-L2455) 用現在進行語態記籌款；固定文本沒有其後湊足、付款或團圓結果。旁白只說此書未交代是否湊齊。資訊卡 `編者腳註／布朗籌錢想買下妻兒｜結果未見於本書` 保留說話人與未知結果，不把 1,200 美元寫成已付金額。 |

里奇蒙定位有明確但分散的上下文：Brown 說自己被帶去[里奇蒙菸草工廠 L912–914](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L912-L914)，妻子後來被賣給[里奇蒙的馬具匠 L1200–1203](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1200-L1203)，書末所收 May 演說更明說[木箱在里奇蒙上快運車 L2358–2364](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L2358-L2364)。因此啟程前場景可標里奇蒙，但室內擺設、日光、街道、散放箱蓋、錢袋與人物表情都是原創卡通示意；`brief.md`、`research.md`、`visual-plan.md` 亦將這些畫面與史料、May 摘錄及編者註分開。開場 `s63005`–`s63008` 為跨事件預告，`s63009` 返回里奇蒙；正文 `s63068`–`s63070` 才順序演出朋友問衣物、Brown 答自己、朋友同意釘蓋，`s63106`–`s63109` 才敲問、回答、開蓋。無提早出箱或已獲法律安全的畫面。

## 對齊與機械檢查

- `video.json`、`script.md`、`claims.md` 各有 127 個同序 ID，127 句旁白逐字一致；121 個 `shot` 提示與 claims 表逐字一致，另有 6 張獨立資訊卡。九個變動 ID 的來源連結均指向固定 Git commit 且行號在 2,817 行內。
- `node tools/video/cli.mjs lint --slug curio-s63 --json` 完成：**0 errors／0 warnings**、127 lines；`git diff bf249e524 d8ad5276a --check` 通過。

**結論：上述精確雜湊的 R7 旁白、固定來源、資訊卡與書面畫面可通過獨立史料關卡。**R6 來源 PASS 只對 R6 雜湊有效；本回條是 R7 新查核，不代表 R7 敘事盲讀已通過。若再改旁白、來源錨點或畫面提示，須按新雜湊重查。尚無生成插圖、配音或成片供實物驗收。
